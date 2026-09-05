import json
import asyncio
import datetime
import math
import logging
from sqlalchemy.future import select

from backend.core.config import settings
from backend.core.database import AsyncSessionLocal
from backend.core.models import Sighting, Watchlist, Alert, Camera
from backend.core.websockets import manager
from backend.core.kafka import publisher
from backend.ai.normaliser import normalize_plate, weighted_levenshtein

logger = logging.getLogger(__name__)

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two points on Earth in km."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

class CorrelationEngine:
    def __init__(self):
        self.consumer = None
        self._running = False
        self.is_kafka_connected = False

    async def start(self):
        self._running = True
        
        # Subscribe to local publisher for zero-kafka / fallback operation
        publisher.subscribe_local(self.process_sighting)

        try:
            from aiokafka import AIOKafkaConsumer
            self.consumer = AIOKafkaConsumer(
                settings.KAFKA_TOPIC_METADATA,
                bootstrap_servers=settings.KAFKA_BROKER_URL,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id="setu_correlation_group",
                auto_offset_reset="latest",
                request_timeout_ms=1500
            )
            await self.consumer.start()
            self.is_kafka_connected = True
            logger.info("Kafka consumer connected. Listening on camera_metadata...")
            asyncio.create_task(self._consume_loop())
        except Exception as e:
            self.is_kafka_connected = False
            logger.info(f"Kafka consumer skipped ({e}). Running on in-memory event spine.")

    async def stop(self):
        self._running = False
        if self.consumer and self.is_kafka_connected:
            try:
                await self.consumer.stop()
            except Exception:
                pass

    async def _consume_loop(self):
        try:
            async for msg in self.consumer:
                if not self._running:
                    break
                await self.process_sighting(msg.value)
        except Exception as e:
            logger.error(f"Error in Kafka consumer loop: {e}")

    async def process_sighting(self, data: dict):
        raw_plate = data.get("plate_number", "").upper().strip()
        if not raw_plate:
            return

        normalized_plate = normalize_plate(raw_plate)
        confidence_score = float(data.get("confidence_score", 0.95))
        plate_det_conf = float(data.get("plate_det_conf", 0.96))
        ocr_char_conf = float(data.get("ocr_char_conf", 0.93))
        format_validity = float(data.get("format_validity", 1.0))
        camera_name = data.get("camera_id", "Cam_Default")
        cam_lat = float(data.get("latitude", 23.0225))
        cam_lon = float(data.get("longitude", 72.5714))
        snapshot_hash = data.get("snapshot_sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

        ts_raw = data.get("timestamp")
        if isinstance(ts_raw, (int, float)):
            timestamp = datetime.datetime.fromtimestamp(ts_raw)
        else:
            timestamp = datetime.datetime.utcnow()

        async with AsyncSessionLocal() as db:
            # 1. Resolve Camera Record
            camera_result = await db.execute(select(Camera).where(Camera.name == camera_name))
            camera = camera_result.scalars().first()
            if not camera:
                camera = Camera(
                    name=camera_name,
                    latitude=cam_lat,
                    longitude=cam_lon,
                    status="ONLINE",
                    geom_source="simulated"
                )
                db.add(camera)
                await db.commit()
                await db.refresh(camera)
            else:
                # Update coordinates if provided
                if "latitude" in data and "longitude" in data:
                    camera.latitude = cam_lat
                    camera.longitude = cam_lon
                    await db.commit()

            # 2. Log Sighting Record
            new_sighting = Sighting(
                plate_number=normalized_plate,
                confidence_score=confidence_score,
                plate_det_conf=plate_det_conf,
                ocr_char_conf=ocr_char_conf,
                format_validity=format_validity,
                snapshot_sha256=snapshot_hash,
                camera_id=camera.id,
                timestamp=timestamp
            )
            db.add(new_sighting)
            await db.commit()
            await db.refresh(new_sighting)

            # 3. Check Watchlist with Fuzzy Weighted Levenshtein Matching
            watchlist_res = await db.execute(select(Watchlist))
            all_watchlist = watchlist_res.scalars().all()
            alert_triggered = False

            for item in all_watchlist:
                w_norm = normalize_plate(item.plate_number)
                dist = weighted_levenshtein(normalized_plate, w_norm)

                if dist <= 1.2:
                    alert_level = "CONFIRMED" if dist == 0.0 else "PROBABLE"
                    alert_rec = Alert(
                        sighting_id=new_sighting.id,
                        watchlist_id=item.id,
                        alert_type="watchlist_hit",
                        alert_level=alert_level,
                        details=f"Matched watchlist item '{item.plate_number}' with distance {dist:.1f}. Reason: {item.reason}"
                    )
                    db.add(alert_rec)
                    await db.commit()

                    alert_payload = {
                        "type": "watchlist_hit",
                        "plate_number": normalized_plate,
                        "raw_plate": raw_plate,
                        "watchlist_plate": item.plate_number,
                        "distance": round(dist, 2),
                        "alert_level": alert_level,
                        "confidence": confidence_score,
                        "breakdown": {
                            "plate_det": round(plate_det_conf * 100, 1),
                            "ocr_char": round(ocr_char_conf * 100, 1),
                            "grammar_validity": round(format_validity * 100, 1),
                            "composite": round(confidence_score * 100, 1)
                        },
                        "camera": camera.name,
                        "location": {"lat": camera.latitude, "lng": camera.longitude},
                        "time": timestamp.isoformat(),
                        "reason": item.reason,
                        "severity": item.severity,
                        "sha256": snapshot_hash
                    }
                    await manager.broadcast_alert(alert_payload)
                    alert_triggered = True
                    logger.info(f"🚨 WATCHLIST HIT: {normalized_plate} (Watchlist: {item.plate_number}, Dist: {dist:.1f}) at {camera.name}")
                    break

            # 4. Topology-Aware Physics Check: Cloned Plates / Impossible Travel
            last_sighting_res = await db.execute(
                select(Sighting)
                .join(Camera)
                .where(Sighting.plate_number == normalized_plate)
                .where(Sighting.id != new_sighting.id)
                .order_by(Sighting.timestamp.desc())
                .limit(1)
            )
            last_sighting = last_sighting_res.scalars().first()

            if last_sighting and last_sighting.camera_id != new_sighting.camera_id:
                last_cam_res = await db.execute(select(Camera).where(Camera.id == last_sighting.camera_id))
                last_cam = last_cam_res.scalars().first()
                if last_cam:
                    dt_seconds = abs((new_sighting.timestamp - last_sighting.timestamp).total_seconds())
                    dist_km = haversine_km(last_cam.latitude, last_cam.longitude, camera.latitude, camera.longitude)
                    
                    # If seen across cameras: calculate speed in km/h
                    # If time < 15s and dist > 1.0 km -> impossible physics
                    speed_kmh = (dist_km / (dt_seconds / 3600.0)) if dt_seconds > 0 else 9999.0
                    
                    if speed_kmh > 160.0 or (dt_seconds < 15.0 and dist_km > 0.5):
                        alert_rec = Alert(
                            sighting_id=new_sighting.id,
                            alert_type="impossible_travel",
                            alert_level="CONFIRMED",
                            details=f"Cloned plate anomaly: traveled {dist_km:.1f} km in {dt_seconds:.1f}s (~{speed_kmh:.0f} km/h) between {last_cam.name} and {camera.name}"
                        )
                        db.add(alert_rec)
                        await db.commit()

                        travel_payload = {
                            "type": "impossible_travel",
                            "plate_number": normalized_plate,
                            "speed_kmh": round(speed_kmh, 1),
                            "distance_km": round(dist_km, 2),
                            "time_diff_seconds": round(dt_seconds, 1),
                            "camera_a": last_cam.name,
                            "camera_b": camera.name,
                            "location_a": {"lat": last_cam.latitude, "lng": last_cam.longitude},
                            "location_b": {"lat": camera.latitude, "lng": camera.longitude},
                            "time": timestamp.isoformat()
                        }
                        await manager.broadcast_alert(travel_payload)
                        alert_triggered = True
                        logger.warning(f"⚠️ CLONED PLATE / IMPOSSIBLE TRAVEL: {normalized_plate} ({dist_km:.1f} km in {dt_seconds:.1f}s)")

            # 5. Broadcast Ambient Live Detection if no alert triggered
            if not alert_triggered:
                live_payload = {
                    "type": "live_sighting",
                    "plate_number": normalized_plate,
                    "raw_plate": raw_plate,
                    "confidence": confidence_score,
                    "breakdown": {
                        "plate_det": round(plate_det_conf * 100, 1),
                        "ocr_char": round(ocr_char_conf * 100, 1),
                        "grammar_validity": round(format_validity * 100, 1),
                        "composite": round(confidence_score * 100, 1)
                    },
                    "camera": camera.name,
                    "location": {"lat": camera.latitude, "lng": camera.longitude},
                    "time": timestamp.isoformat(),
                    "reason": f"Real-Time Edge Detection at {camera.name}",
                    "severity": "NORMAL",
                    "sha256": snapshot_hash
                }
                await manager.broadcast_alert(live_payload)
                logger.info(f"🟢 LIVE SIGHTING BROADCAST: {normalized_plate} at {camera.name}")

correlation_engine = CorrelationEngine()
