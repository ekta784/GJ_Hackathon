from fastapi import FastAPI, WebSocket, Depends, HTTPException, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update
import asyncio
import datetime
import logging
import random
import re

from backend.core.config import settings
from backend.core.database import get_db, engine, AsyncSessionLocal
from backend.core.models import Base, Watchlist, Sighting, Camera, Alert, Department, Vendor, AuditLog
from backend.schemas.api import (
    WatchlistCreate, WatchlistResponse, SightingResponse, 
    CameraResponse, AlertResponse, SimulateSightingRequest,
    DepartmentResponse, VendorResponse, RegisterAdapterRequest, AuditLogResponse
)
from backend.core.websockets import manager
from backend.core.kafka import publisher
from backend.services.correlation import correlation_engine, haversine_km
from backend.ai.pipeline import ai_pipeline, SIMULATED_CAMERAS
from backend.ai.normaliser import normalize_plate, weighted_levenshtein

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("setu-backend")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SETU - Integrated Video Management & ANPR Intelligence Network (Gujarat Police Innovation Challenge 2026)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEPARTMENTS_SEED = ["Police", "GSRTC", "Municipal", "Health", "Panchayat"]
VENDORS_SEED = ["Hikvision", "Dahua", "Axis", "Honeywell", "CP Plus"]

async def seed_initial_data():
    """Seeds Gujarat multi-department CCTV network, vendors, default watchlist, and initial audit logs."""
    async with AsyncSessionLocal() as db:
        # 1. Seed Departments
        dept_map = {}
        for d_name in DEPARTMENTS_SEED:
            res = await db.execute(select(Department).where(Department.name == d_name))
            dept = res.scalars().first()
            if not dept:
                dept = Department(name=d_name)
                db.add(dept)
                await db.commit()
                await db.refresh(dept)
            dept_map[d_name] = dept.id

        # 2. Seed Vendors
        vendor_map = {}
        for v_name in VENDORS_SEED:
            res = await db.execute(select(Vendor).where(Vendor.name == v_name))
            vend = res.scalars().first()
            if not vend:
                vend = Vendor(name=v_name)
                db.add(vend)
                await db.commit()
                await db.refresh(vend)
            vendor_map[v_name] = vend.id

        # 3. Seed / Update Camera Fleet
        logger.info(f"Synchronizing {len(SIMULATED_CAMERAS)} Gujarat CCTV Network Cameras across 5 departments...")
        for c in SIMULATED_CAMERAS:
            cam_res = await db.execute(select(Camera).where(Camera.name == c["name"]))
            cam = cam_res.scalars().first()
            
            dept_id = dept_map.get(c.get("dept", "Police"), dept_map["Police"])
            vend_id = vendor_map.get(c.get("vendor", "Hikvision"), vendor_map["Hikvision"])
            codec_val = c.get("codec", "H.264")
            dist_val = c.get("district", "Ahmedabad")
            res_val = c.get("res", "1920x1080")

            if not cam:
                cam = Camera(
                    name=c["name"],
                    url=f"rtsp://localhost:8554/stream/{c['id'].lower()}",
                    latitude=c["lat"],
                    longitude=c["lon"],
                    status="ONLINE",
                    fps=5,
                    resolution=res_val,
                    geom_source="official_police_node",
                    codec=codec_val,
                    district=dist_val,
                    department_id=dept_id,
                    vendor_id=vend_id
                )
                db.add(cam)
            else:
                cam.latitude = c["lat"]
                cam.longitude = c["lon"]
                cam.department_id = dept_id
                cam.vendor_id = vend_id
                cam.codec = codec_val
                cam.district = dist_val
                cam.resolution = res_val
        await db.commit()

        # 4. Seed Default Watchlist Item (Official Test Case vehicle)
        watch_count = await db.execute(select(Watchlist).where(Watchlist.plate_number == "GJ01AB1234"))
        if not watch_count.scalars().first():
            logger.info("Seeding Official Test Case Watchlist target GJ01AB1234...")
            test_target = Watchlist(
                plate_number="GJ01AB1234",
                reason="Wanted: Vehicle associated with Crime Branch Case #2026-SCRB",
                severity="CRITICAL"
            )
            db.add(test_target)
            await db.commit()

        # 5. Seed Initial Audit Log
        audit_check = await db.execute(select(AuditLog))
        if not audit_check.scalars().first():
            db.add(AuditLog(
                action="SYSTEM_INIT",
                details="SETU Sentinel Core initialized. Federated adapter layer active across 5 departments."
            ))
            await db.commit()

async def ambient_ingest_loop():
    """Simulates steady background traffic across Gujarat camera nodes."""
    logger.info("Ambient CCTV stream processing started across Gujarat nodes...")
    while True:
        try:
            for cam in SIMULATED_CAMERAS:
                result = await ai_pipeline.process_frame(cam["name"], b"frame")
                if result:
                    await publisher.publish_sighting(result)
            await asyncio.sleep(4.0)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in ambient ingest loop: {e}")
            await asyncio.sleep(2.0)

ambient_task = None

@app.on_event("startup")
async def startup():
    global ambient_task
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await seed_initial_data()
    await publisher.start()
    await correlation_engine.start()
    
    import os
    if os.getenv("ENABLE_AMBIENT_TRAFFIC", "false").lower() == "true":
        ambient_task = asyncio.create_task(ambient_ingest_loop())
        logger.info("Ambient CCTV stream processing started across Gujarat nodes...")
    else:
        logger.info("Ambient background traffic is OFF. Ready for explicit live webcam / video / simulation events.")
    logger.info("SETU Sentinel Platform ready.")

@app.on_event("shutdown")
async def shutdown():
    global ambient_task
    if ambient_task:
        ambient_task.cancel()
    await publisher.stop()
    await correlation_engine.stop()

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    cam_q = await db.execute(select(Camera))
    cams = cam_q.scalars().all()
    watch_q = await db.execute(select(Watchlist))
    watches = watch_q.scalars().all()
    sight_q = await db.execute(select(Sighting))
    sightings = sight_q.scalars().all()
    dept_q = await db.execute(select(Department))
    depts = dept_q.scalars().all()
    
    return {
        "status": "ONLINE",
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "active_cameras": len(cams),
        "departments_federated": len(depts),
        "watchlist_records": len(watches),
        "total_sightings_logged": len(sightings)
    }

@app.get("/api/cameras", response_model=list[CameraResponse])
async def get_cameras(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Camera)
        .options(selectinload(Camera.department), selectinload(Camera.vendor))
        .order_by(Camera.name)
    )
    cameras = result.scalars().all()
    output = []
    for c in cameras:
        d_name = c.department.name if c.department else "Police"
        v_name = c.vendor.name if c.vendor else "Hikvision"
        whep_url = f"http://localhost:8889/stream/{c.name.lower().replace(' ', '_')}/whep"
        output.append(CameraResponse(
            id=c.id,
            name=c.name,
            latitude=c.latitude,
            longitude=c.longitude,
            status=c.status,
            fps=c.fps,
            resolution=c.resolution,
            department=d_name,
            vendor=v_name,
            codec=c.codec or "H.264",
            district=c.district or "Ahmedabad",
            url=c.url,
            whep_url=whep_url,
            latency_ms=random.randint(18, 38),
            packet_loss=round(random.uniform(0.0, 0.4), 1)
        ))
    return output

@app.get("/api/departments", response_model=list[DepartmentResponse])
async def get_departments(db: AsyncSession = Depends(get_db)):
    depts_q = await db.execute(select(Department).options(selectinload(Department.cameras)))
    depts = depts_q.scalars().all()
    return [
        DepartmentResponse(
            id=d.id,
            name=d.name,
            camera_count=len(d.cameras)
        )
        for d in depts
    ]

@app.get("/api/vendors", response_model=list[VendorResponse])
async def get_vendors(db: AsyncSession = Depends(get_db)):
    vends_q = await db.execute(select(Vendor).options(selectinload(Vendor.cameras)))
    vends = vends_q.scalars().all()
    return [
        VendorResponse(
            id=v.id,
            name=v.name,
            camera_count=len(v.cameras)
        )
        for v in vends
    ]

@app.get("/api/health/cameras")
async def get_fleet_health(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Camera).options(selectinload(Camera.department), selectinload(Camera.vendor)))
    cameras = res.scalars().all()
    total = len(cameras)
    online = sum(1 for c in cameras if c.status == "ONLINE")
    
    fleet_details = []
    for c in cameras:
        fleet_details.append({
            "id": c.id,
            "name": c.name,
            "department": c.department.name if c.department else "Police",
            "vendor": c.vendor.name if c.vendor else "Hikvision",
            "status": c.status,
            "fps": c.fps,
            "resolution": c.resolution,
            "codec": c.codec or "H.264",
            "district": c.district or "Ahmedabad",
            "latency_ms": random.randint(15, 42),
            "reconnect_count": 0 if c.status == "ONLINE" else 3,
            "uptime_pct": 99.8 if c.status == "ONLINE" else 84.5
        })
    return {
        "summary": {
            "total_cameras": total,
            "online_cameras": online,
            "degraded_cameras": 0,
            "offline_cameras": total - online,
            "fleet_health_score": round((online / max(1, total)) * 100, 1),
            "bandwidth_saving_ratio": "1400x (Metadata-First Architecture)"
        },
        "fleet": fleet_details
    }

@app.post("/api/adapters/register")
async def register_new_adapter(req: RegisterAdapterRequest, db: AsyncSession = Depends(get_db)):
    """
    Demonstrates live-pluggable vendor onboarding:
    Registers a 27th vendor without restarting core services.
    """
    v_res = await db.execute(select(Vendor).where(Vendor.name == req.vendor_name))
    vendor = v_res.scalars().first()
    if not vendor:
        vendor = Vendor(name=req.vendor_name)
        db.add(vendor)
        await db.commit()
        await db.refresh(vendor)

    d_res = await db.execute(select(Department).where(Department.name == req.department))
    dept = d_res.scalars().first()
    if not dept:
        dept = Department(name=req.department)
        db.add(dept)
        await db.commit()
        await db.refresh(dept)

    created_cams = []
    base_lat = 23.2200
    base_lon = 72.6500

    for i in range(1, req.cameras_to_onboard + 1):
        cam_name = f"{req.vendor_name} - {req.region} Node #{i}"
        new_cam = Camera(
            name=cam_name,
            url=f"rtsp://localhost:8554/stream/adapter_{req.vendor_name.lower()}_{i}",
            latitude=base_lat + (i * 0.005),
            longitude=base_lon + (i * 0.005),
            status="ONLINE",
            fps=5,
            resolution="1920x1080",
            geom_source="plugged_adapter",
            codec="H.265",
            district=req.region,
            department_id=dept.id,
            vendor_id=vendor.id
        )
        db.add(new_cam)
        created_cams.append(cam_name)

    db.add(AuditLog(
        action="ADAPTER_REGISTERED",
        details=f"Onboarded new vendor adapter: {req.vendor_name} ({req.protocol}) with {req.cameras_to_onboard} cameras."
    ))
    await db.commit()

    # Broadcast real-time system event
    await manager.broadcast_alert({
        "type": "adapter_registered",
        "vendor": req.vendor_name,
        "department": req.department,
        "cameras_onboarded": req.cameras_to_onboard,
        "message": f"Live Adapter Onboarded: {req.vendor_name} added {req.cameras_to_onboard} nodes to Gujarat grid with zero downtime."
    })

    return {
        "status": "success",
        "vendor": req.vendor_name,
        "department": req.department,
        "onboarded_cameras": created_cams
    }

@app.get("/api/audit", response_model=list[AuditLogResponse])
async def get_audit_logs(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50))
    return res.scalars().all()

@app.post("/api/watchlist", response_model=WatchlistResponse)
async def add_to_watchlist(item: WatchlistCreate, db: AsyncSession = Depends(get_db)):
    norm_plate = normalize_plate(item.plate_number)
    new_entry = Watchlist(
        plate_number=norm_plate,
        reason=item.reason,
        severity=item.severity or "CRITICAL"
    )
    db.add(new_entry)
    db.add(AuditLog(
        action="WATCHLIST_ADD",
        details=f"Target {norm_plate} added to watchlist. Reason: {item.reason} | Severity: {item.severity}"
    ))
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

@app.get("/api/watchlist", response_model=list[WatchlistResponse])
async def get_watchlist(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Watchlist).order_by(Watchlist.added_at.desc()))
    return result.scalars().all()

@app.delete("/api/watchlist/{watchlist_id}")
async def delete_watchlist(watchlist_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Watchlist, watchlist_id)
    if not item:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
    plate = item.plate_number
    
    # 1. Nullify foreign key references in alerts so delete never violates constraints
    await db.execute(
        update(Alert).where(Alert.watchlist_id == watchlist_id).values(watchlist_id=None)
    )

    # 2. Delete the item
    await db.delete(item)
    db.add(AuditLog(
        action="WATCHLIST_REMOVE",
        details=f"Target {plate} removed from watchlist."
    ))
    await db.commit()

    # 3. Broadcast real-time update to all connected frontends
    await manager.broadcast_alert({
        "type": "watchlist_updated",
        "deleted_id": watchlist_id
    })

    return {"message": "Deleted successfully", "id": watchlist_id}

@app.get("/api/search/{plate_number}", response_model=list[SightingResponse])
async def search_plate(plate_number: str, db: AsyncSession = Depends(get_db)):
    norm_search = normalize_plate(plate_number)
    
    # Audit log
    db.add(AuditLog(
        action="VEHICLE_INVESTIGATION_SEARCH",
        details=f"Investigator queried vehicle plate: {norm_search} (raw input: {plate_number})"
    ))
    await db.commit()

    # 1. Fetch exact matches
    result = await db.execute(
        select(Sighting)
        .options(
            selectinload(Sighting.camera).selectinload(Camera.department),
            selectinload(Sighting.camera).selectinload(Camera.vendor)
        )
        .where(Sighting.plate_number == norm_search)
        .order_by(Sighting.timestamp.asc())
    )
    exact_sightings = list(result.scalars().all())

    # 2. Fetch fuzzy OCR matches (e.g. MH12AB3156 vs MH12AB3456)
    prefix = norm_search[:4] if len(norm_search) >= 4 else norm_search
    fuzzy_res = await db.execute(
        select(Sighting)
        .options(
            selectinload(Sighting.camera).selectinload(Camera.department),
            selectinload(Sighting.camera).selectinload(Camera.vendor)
        )
        .where(Sighting.plate_number.like(f"{prefix}%"))
        .order_by(Sighting.timestamp.asc())
    )
    candidate_sightings = fuzzy_res.scalars().all()

    seen_ids = set(s.id for s in exact_sightings)
    all_matched = list(exact_sightings)
    for s in candidate_sightings:
        if s.id not in seen_ids:
            if weighted_levenshtein(s.plate_number, norm_search) <= 1.2:
                all_matched.append(s)
                seen_ids.add(s.id)

    all_matched.sort(key=lambda s: s.timestamp)
    sightings = all_matched
    
    response_data = []
    prev_s = None
    for s in sightings:
        transit_dist = None
        transit_speed = None
        transit_plausibility = "PLAUSIBLE"

        if prev_s and prev_s.camera and s.camera:
            dist = haversine_km(prev_s.camera.latitude, prev_s.camera.longitude, s.camera.latitude, s.camera.longitude)
            transit_dist = round(dist, 2)
            dt_hours = abs((s.timestamp - prev_s.timestamp).total_seconds()) / 3600.0
            if dt_hours > 0:
                speed = dist / dt_hours
                transit_speed = round(speed, 1)
                if speed > 160.0 or (dt_hours < 0.008 and dist > 0.5):
                    transit_plausibility = "IMPLAUSIBLE (Cloned Plate)"
                elif speed > 120.0:
                    transit_plausibility = "FAST"
                else:
                    transit_plausibility = "PLAUSIBLE"

        dept_name = s.camera.department.name if s.camera and s.camera.department else "Police"
        vendor_name = s.camera.vendor.name if s.camera and s.camera.vendor else "Hikvision"

        response_data.append(SightingResponse(
            id=s.id,
            plate_number=s.plate_number,
            confidence_score=s.confidence_score,
            plate_det_conf=s.plate_det_conf,
            ocr_char_conf=s.ocr_char_conf,
            format_validity=s.format_validity,
            camera_name=s.camera.name if s.camera else "Unknown Camera",
            department_name=dept_name,
            vendor_name=vendor_name,
            latitude=s.camera.latitude if s.camera else 23.0225,
            longitude=s.camera.longitude if s.camera else 72.5714,
            timestamp=s.timestamp,
            snapshot_sha256=s.snapshot_sha256,
            transit_distance_km=transit_dist,
            transit_speed_kmh=transit_speed,
            transit_plausibility=transit_plausibility
        ))
        prev_s = s
    return response_data

@app.get("/api/alerts", response_model=list[AlertResponse])
async def get_alerts(db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(Alert)
        .options(
            selectinload(Alert.sighting).selectinload(Sighting.camera).selectinload(Camera.department)
        )
        .order_by(Alert.created_at.desc())
        .limit(30)
    )
    alerts = res.scalars().all()
    output = []
    for a in alerts:
        cam_name = a.sighting.camera.name if a.sighting and a.sighting.camera else "Gujarat Node"
        dept_name = (
            a.sighting.camera.department.name
            if a.sighting and a.sighting.camera and a.sighting.camera.department
            else "Police"
        )
        plate = a.sighting.plate_number if a.sighting else None
        output.append(AlertResponse(
            id=a.id,
            sighting_id=a.sighting_id,
            watchlist_id=a.watchlist_id,
            alert_type=a.alert_type,
            alert_level=a.alert_level,
            details=a.details,
            created_at=a.created_at,
            camera_name=cam_name,
            department=dept_name,
            plate_number=plate
        ))
    return output

@app.post("/api/simulate/sighting")
async def simulate_single_sighting(req: SimulateSightingRequest):
    """Allows manual injection of a vehicle sighting at a specific camera with optional auto-watchlist enrollment."""
    norm = normalize_plate(req.plate_number)
    
    # Auto-enroll in Watchlist only for clean standard Indian plates AND if no close match already exists
    if req.auto_watchlist:
        clean_pattern = re.compile(r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$')
        if clean_pattern.match(norm) and 8 <= len(norm) <= 11:
            async with AsyncSessionLocal() as db:
                wl_res = await db.execute(select(Watchlist))
                all_wl = wl_res.scalars().all()
                already_exists = False
                for existing in all_wl:
                    ex_norm = normalize_plate(existing.plate_number)
                    if ex_norm == norm or weighted_levenshtein(ex_norm, norm) <= 1.2:
                        already_exists = True
                        break

                if not already_exists:
                    new_wl = Watchlist(
                        plate_number=norm,
                        reason=f"Live Physical Edge Detection at {req.camera_name}",
                        severity="CRITICAL"
                    )
                    db.add(new_wl)
                    await db.commit()
                    logger.info(f"[+] Auto-enrolled clean plate {norm} into Watchlist.")
                    await manager.broadcast_alert({
                        "type": "watchlist_updated",
                        "plate_number": norm
                    })

    detection = await ai_pipeline.process_frame(req.camera_name, b"manual", forced_plate=norm)
    if req.latitude and req.longitude and detection:
        detection["latitude"] = req.latitude
        detection["longitude"] = req.longitude
    if detection:
        if req.confidence:
            detection["confidence_score"] = req.confidence
        if req.timestamp:
            detection["timestamp"] = req.timestamp
        await publisher.publish_sighting(detection)
        return {"status": "dispatched", "detection": detection}
    return {"status": "failed"}

@app.post("/api/simulate/official-test-case")
async def run_official_test_case():
    """
    Executes the Gujarat Police Innovation Challenge Official Test Case:
    Simulates wanted vehicle GJ01AB1234 moving across:
    1. SG Highway (Ahmedabad - Police Hikvision)
    2. Gandhinagar CH-0 (Gandhinagar - Police Axis)
    3. Vadodara Express Highway Exit (Vadodara - Police Honeywell)
    Demonstrating multi-department cross-camera vehicle identification, real-time alert, and route reconstruction.
    """
    test_plate = "GJ01AB1234"
    logger.info(f"Executing Official Test Case Simulation for {test_plate}...")
    
    route = [
        ("SG Highway - ISKCON Cross Rd", 23.0298, 72.5074, "Police", "Hikvision"),
        ("Gandhinagar CH-0 Circle", 23.2156, 72.6369, "Police", "Axis"),
        ("Vadodara Express Highway Exit", 22.3107, 73.1812, "Police", "Honeywell")
    ]
    
    events_dispatched = []
    base_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=45)
    
    for idx, (cam_name, lat, lon, dept, vend) in enumerate(route):
        sighting_time = base_time + datetime.timedelta(minutes=idx * 20)
        detection = await ai_pipeline.process_frame(cam_name, b"test", forced_plate=test_plate)
        if detection:
            detection["latitude"] = lat
            detection["longitude"] = lon
            detection["department"] = dept
            detection["vendor"] = vend
            detection["timestamp"] = sighting_time.timestamp()
            await publisher.publish_sighting(detection)
            events_dispatched.append({
                "step": idx + 1,
                "camera": cam_name,
                "department": dept,
                "vendor": vend,
                "location": {"lat": lat, "lon": lon},
                "timestamp": sighting_time.isoformat()
            })
            await asyncio.sleep(0.3)
            
    return {
        "status": "success",
        "description": "Official Test Case simulated successfully across 3 Gujarat camera nodes.",
        "target_plate": test_plate,
        "dispatched_steps": events_dispatched
    }

@app.post("/api/simulate/cloned-plate")
async def simulate_cloned_plate():
    """
    Injects two sightings of GJ01XY9999 simultaneously in Ahmedabad and Surat (209 km apart in 1 second)
    to trigger the topology-aware impossible travel / cloned plate anomaly detector.
    """
    cloned_plate = "GJ01XY9999"
    # Sighting 1: Ahmedabad
    det1 = await ai_pipeline.process_frame("SG Highway - ISKCON Cross Rd", b"test", forced_plate=cloned_plate)
    if det1:
        det1["latitude"] = 23.0298
        det1["longitude"] = 72.5074
        det1["timestamp"] = datetime.datetime.utcnow().timestamp()
        await publisher.publish_sighting(det1)

    await asyncio.sleep(0.4)

    # Sighting 2: Surat (209 km away, 0.4s later)
    det2 = await ai_pipeline.process_frame("Surat Ring Road - Majura Gate", b"test", forced_plate=cloned_plate)
    if det2:
        det2["latitude"] = 21.1702
        det2["longitude"] = 72.8311
        det2["timestamp"] = datetime.datetime.utcnow().timestamp()
        await publisher.publish_sighting(det2)

    return {
        "status": "success",
        "message": f"Cloned plate anomaly injected for {cloned_plate} across Ahmedabad and Surat."
    }

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
