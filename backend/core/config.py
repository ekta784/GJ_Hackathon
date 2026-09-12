from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SETU Sentinel - Gujarat Police ANPR Platform"
    VERSION: str = "1.0.0"
    
    CAMERA_HOST_IP: str = "127.0.0.1"
    # Default to PostgreSQL (Port 5433 on Windows host)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@127.0.0.1:5433/setu_db"
    KAFKA_BROKER_URL: str = "127.0.0.1:9092"
    KAFKA_TOPIC_METADATA: str = "camera_metadata"
    REDIS_URL: str = "redis://127.0.0.1:6379/0"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
