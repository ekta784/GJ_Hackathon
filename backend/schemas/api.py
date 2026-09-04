from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SightingResponse(BaseModel):
    id: int
    plate_number: str
    confidence_score: float
    plate_det_conf: Optional[float] = 0.95
    ocr_char_conf: Optional[float] = 0.92
    format_validity: Optional[float] = 1.0
    camera_name: str
    department_name: Optional[str] = "Police"
    vendor_name: Optional[str] = "Hikvision"
    latitude: float
    longitude: float
    timestamp: datetime
    snapshot_sha256: str
    # Inter-sighting transit correlation fields
    transit_distance_km: Optional[float] = None
    transit_speed_kmh: Optional[float] = None
    transit_plausibility: Optional[str] = "PLAUSIBLE"

    class Config:
        from_attributes = True

class WatchlistCreate(BaseModel):
    plate_number: str
    reason: str
    severity: Optional[str] = "CRITICAL"

class WatchlistResponse(WatchlistCreate):
    id: int
    added_at: datetime

    class Config:
        from_attributes = True

class CameraResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    status: str
    fps: int
    resolution: str
    department: Optional[str] = "Police"
    vendor: Optional[str] = "Hikvision"
    codec: Optional[str] = "H.264"
    district: Optional[str] = "Ahmedabad"
    url: Optional[str] = None
    whep_url: Optional[str] = None
    latency_ms: Optional[int] = 24
    packet_loss: Optional[float] = 0.0

    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    id: int
    sighting_id: int
    watchlist_id: Optional[int] = None
    alert_type: str
    alert_level: str
    details: Optional[str] = None
    created_at: datetime
    camera_name: Optional[str] = "Gujarat Node"
    department: Optional[str] = "Police"
    plate_number: Optional[str] = None

    class Config:
        from_attributes = True

class SimulateSightingRequest(BaseModel):
    plate_number: str
    camera_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    camera_count: int

class VendorResponse(BaseModel):
    id: int
    name: str
    camera_count: int

class RegisterAdapterRequest(BaseModel):
    vendor_name: str
    protocol: Optional[str] = "RTSP/ONVIF"
    department: Optional[str] = "Municipal"
    cameras_to_onboard: int = 5
    region: Optional[str] = "Gandhinagar Smart City"

class AuditLogResponse(BaseModel):
    id: int
    action: str
    details: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
