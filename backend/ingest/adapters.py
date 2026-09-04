from typing import Protocol, List
from pydantic import BaseModel

class HealthStatus(BaseModel):
    status: str
    uptime: int

class ViewURLs(BaseModel):
    rtsp: str
    whep: str
    hls: str

class CameraDescriptor(BaseModel):
    id: str
    name: str
    url: str
    vendor: str
    resolution: str
    fps: int

class CameraAdapter(Protocol):
    vendor: str
    
    async def discover(self) -> List[CameraDescriptor]:
        ...
        
    async def open(self, cam: CameraDescriptor):
        ...
        
    async def health(self, cam: CameraDescriptor) -> HealthStatus:
        ...
        
    def view_url(self, cam: CameraDescriptor) -> ViewURLs:
        ...

class SentinelCatalogAdapter:
    vendor: str = "Sentinel"

    async def discover(self) -> List[CameraDescriptor]:
        # Would fetch from http://<host>/api/ingest
        return [
            CameraDescriptor(
                id="cam_001",
                name="Sentinel Test Cam 1",
                url="rtsp://localhost:8554/stream/cam_001",
                vendor=self.vendor,
                resolution="1920x1080",
                fps=25
            )
        ]
        
    async def open(self, cam: CameraDescriptor):
        pass
        
    async def health(self, cam: CameraDescriptor) -> HealthStatus:
        return HealthStatus(status="OK", uptime=3600)
        
    def view_url(self, cam: CameraDescriptor) -> ViewURLs:
        return ViewURLs(
            rtsp=cam.url,
            whep=cam.url.replace("rtsp://", "http://").replace("8554", "8889") + "/whep",
            hls=cam.url.replace("rtsp://", "http://").replace("8554", "8888").replace("stream/", "live/stream/") + "/index.m3u8"
        )
