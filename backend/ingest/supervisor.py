import asyncio
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FFmpegSupervisor:
    def __init__(self, rtsp_url: str, camera_id: str):
        self.rtsp_url = rtsp_url
        self.camera_id = camera_id
        self.process = None
        self._running = False
        self.retry_delay = 2

    async def start(self):
        self._running = True
        while self._running:
            logger.info(f"Starting FFmpeg for camera {self.camera_id}")
            
            command = [
                "ffmpeg",
                "-loglevel", "error",
                "-rtsp_transport", "tcp",
                "-timeout", "5000000",
                "-i", self.rtsp_url,
                "-vf", "fps=5,scale=1280:-2",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "-"
            ]
            
            try:
                self.process = await asyncio.create_subprocess_exec(
                    *command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                # Reset retry delay on successful start
                self.retry_delay = 2
                
                while True:
                    # Expected frame size for 1280x720 bgr24: 1280 * 720 * 3 = 2764800 bytes
                    # Note: height is scaled proportionally, so we might need to read dynamically or process differently
                    # For a robust ingest, we would pipe stdout to our AI pipeline
                    chunk = await self.process.stdout.read(65536)
                    if not chunk:
                        logger.warning(f"FFmpeg process for {self.camera_id} ended.")
                        break
                        
            except Exception as e:
                logger.error(f"FFmpeg error on {self.camera_id}: {e}")
            
            finally:
                if self.process:
                    try:
                        self.process.kill()
                    except ProcessLookupError:
                        pass
                    
            if not self._running:
                break
                
            logger.info(f"Restarting FFmpeg for {self.camera_id} in {self.retry_delay} seconds...")
            await asyncio.sleep(self.retry_delay)
            # Exponential backoff 2 -> 30s
            self.retry_delay = min(30, int(self.retry_delay * 1.5))

    async def stop(self):
        self._running = False
        if self.process:
            try:
                self.process.kill()
            except ProcessLookupError:
                pass
