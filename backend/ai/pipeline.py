import random
import time
import hashlib
import asyncio
from typing import Dict, Any, Optional
from backend.ai.normaliser import normalize_plate

# Simulated multi-department camera network across Gujarat
SIMULATED_CAMERAS = [
    # 1. Gujarat Police (State Crime Record Bureau / Highway Patrol)
    {"id": "GJ_POLICE_AHM_01", "name": "SG Highway - ISKCON Cross Rd", "lat": 23.0298, "lon": 72.5074, "dept": "Police", "vendor": "Hikvision", "district": "Ahmedabad", "codec": "H.264", "res": "1920x1080"},
    {"id": "GJ_POLICE_AHM_02", "name": "Sarkhej - Sanand Toll Plaza", "lat": 22.9868, "lon": 72.4836, "dept": "Police", "vendor": "CP Plus", "district": "Ahmedabad", "codec": "H.265", "res": "1920x1080"},
    {"id": "GJ_POLICE_GNR_01", "name": "Gandhinagar CH-0 Circle", "lat": 23.2156, "lon": 72.6369, "dept": "Police", "vendor": "Axis", "district": "Gandhinagar", "codec": "H.264", "res": "1920x1080"},
    {"id": "GJ_POLICE_GNR_02", "name": "Infocity - Bhaijipura Jn", "lat": 23.1906, "lon": 72.6288, "dept": "Police", "vendor": "Dahua", "district": "Gandhinagar", "codec": "H.265", "res": "1920x1080"},
    {"id": "GJ_POLICE_BRD_01", "name": "Vadodara Express Highway Exit", "lat": 22.3107, "lon": 73.1812, "dept": "Police", "vendor": "Honeywell", "district": "Vadodara", "codec": "H.264", "res": "1920x1080"},
    {"id": "GJ_POLICE_SRT_01", "name": "Surat Ring Road - Majura Gate", "lat": 21.1702, "lon": 72.8311, "dept": "Police", "vendor": "Hikvision", "district": "Surat", "codec": "H.265", "res": "1920x1080"},
    {"id": "GJ_POLICE_RJK_01", "name": "Rajkot Kalawad Road Jn", "lat": 22.2818, "lon": 70.7698, "dept": "Police", "vendor": "Axis", "district": "Rajkot", "codec": "H.264", "res": "1920x1080"},

    # 2. GSRTC (Gujarat State Road Transport Corporation)
    {"id": "GJ_GSRTC_AHM_01", "name": "GSRTC Central Bus Port - Geeta Mandir", "lat": 23.0118, "lon": 72.5898, "dept": "GSRTC", "vendor": "CP Plus", "district": "Ahmedabad", "codec": "H.264", "res": "1280x720"},
    {"id": "GJ_GSRTC_AHM_02", "name": "GSRTC Ranip Inter-State Terminal", "lat": 23.0768, "lon": 72.5768, "dept": "GSRTC", "vendor": "Dahua", "district": "Ahmedabad", "codec": "H.264", "res": "1280x720"},
    {"id": "GJ_GSRTC_SRT_01", "name": "GSRTC Surat Central Depot", "lat": 21.2052, "lon": 72.8398, "dept": "GSRTC", "vendor": "Hikvision", "district": "Surat", "codec": "H.265", "res": "1920x1080"},

    # 3. Municipal Corporations (AMC / SMC / VMC Smart City)
    {"id": "GJ_AMC_AHM_01", "name": "AMC Riverfront West Promenade", "lat": 23.0335, "lon": 72.5742, "dept": "Municipal", "vendor": "Honeywell", "district": "Ahmedabad", "codec": "H.265", "res": "2560x1440"},
    {"id": "GJ_SMC_SRT_01", "name": "SMC Varachha Flyover Jn", "lat": 21.2185, "lon": 72.8598, "dept": "Municipal", "vendor": "Axis", "district": "Surat", "codec": "H.264", "res": "1920x1080"},
    {"id": "GJ_VMC_BRD_01", "name": "VMC Sayaji Baug North Entrance", "lat": 22.3168, "lon": 73.1905, "dept": "Municipal", "vendor": "CP Plus", "district": "Vadodara", "codec": "H.264", "res": "1280x720"},

    # 4. Health Department (Civil Hospitals / Trauma Centers)
    {"id": "GJ_HLTH_AHM_01", "name": "Civil Hospital Asarwa Trauma Gate", "lat": 23.0518, "lon": 72.6045, "dept": "Health", "vendor": "Dahua", "district": "Ahmedabad", "codec": "H.264", "res": "1920x1080"},
    {"id": "GJ_HLTH_GNR_01", "name": "GMERS Hospital Sector-12 Entry", "lat": 23.2268, "lon": 72.6512, "dept": "Health", "vendor": "Hikvision", "district": "Gandhinagar", "codec": "H.265", "res": "1920x1080"},

    # 5. Panchayat & Rural Development (Rural Checkposts)
    {"id": "GJ_PANCH_SND_01", "name": "Sanand GIDC Rural Barrier #3", "lat": 22.9712, "lon": 72.3789, "dept": "Panchayat", "vendor": "CP Plus", "district": "Ahmedabad Rural", "codec": "H.264", "res": "1280x720"},
    {"id": "GJ_PANCH_BHJ_01", "name": "Bhuj - Mundra Highway Junction", "lat": 23.2105, "lon": 69.7025, "dept": "Panchayat", "vendor": "Axis", "district": "Kutch", "codec": "H.265", "res": "1920x1080"}
]

class MockAIPipeline:
    """
    Simulated AI Pipeline representing YOLO (Vehicle + Plate Detector) + PaddleOCR.
    Produces realistic detection events with explainable confidence metrics and SHA-256 evidence.
    """
    def __init__(self):
        self.target_plates = [
            "LS15EBC",     # Real vehicle: Mercedes-AMG Sports Coupe (Police & Health CCTV)
            "DL3CBJ1384",  # Real vehicle: Silver Maruti Hatchback (AMC Riverfront Municipal CCTV)
            "DL2CAT4762",  # Real vehicle: Silver Nissan Terrano SUV (Sanand Panchayat CCTV)
            "HR26CQ6869",  # Real vehicle: Interstate Transit (GSRTC Bus Terminal CCTV)
            "GJ01XY9999"   # Anomaly test vehicle
        ]

    async def process_frame(self, camera_id: str, frame_bytes: bytes, forced_plate: Optional[str] = None) -> Optional[Dict[str, Any]]:
        await asyncio.sleep(0.02)
        
        # Determine camera details
        cam_info = next((c for c in SIMULATED_CAMERAS if c["id"] == camera_id or c["name"] == camera_id), None)
        if not cam_info:
            cam_info = {"id": camera_id, "name": camera_id, "lat": 23.0225, "lon": 72.5714}

        if forced_plate:
            raw_plate = forced_plate
        else:
            # 5% chance of vehicle detection in ambient loop
            if random.random() > 0.05:
                return None
            raw_plate = random.choice(self.target_plates)

        normalized = normalize_plate(raw_plate)
        plate_det_conf = round(random.uniform(0.92, 0.99), 2)
        ocr_char_conf = round(random.uniform(0.88, 0.98), 2)
        format_validity = 1.0 if len(normalized) in (9, 10) else 0.85
        
        # Composite score according to Master Spec:
        composite = round(0.40 * plate_det_conf + 0.40 * ocr_char_conf + 0.20 * format_validity, 2)
        
        # Evidence hash
        now = time.time()
        evidence_hash = hashlib.sha256(f"{normalized}-{now}-{cam_info['id']}".encode()).hexdigest()

        return {
            "camera_id": cam_info["name"],
            "latitude": cam_info["lat"],
            "longitude": cam_info["lon"],
            "department": cam_info.get("dept", "Police"),
            "vendor": cam_info.get("vendor", "Hikvision"),
            "plate_number": normalized,
            "raw_plate": raw_plate,
            "confidence_score": composite,
            "plate_det_conf": plate_det_conf,
            "ocr_char_conf": ocr_char_conf,
            "format_validity": format_validity,
            "snapshot_sha256": evidence_hash,
            "timestamp": now
        }

ai_pipeline = MockAIPipeline()
