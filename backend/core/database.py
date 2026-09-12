import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings

logger = logging.getLogger(__name__)

import socket

def resolve_postgres_url():
    url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    # Auto-resolve active PostgreSQL port between 5433 and 5432
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.4)
            is_5433 = (s.connect_ex(("127.0.0.1", 5433)) == 0)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.4)
            is_5432 = (s.connect_ex(("127.0.0.1", 5432)) == 0)
        
        if is_5433 and not is_5432:
            url = url.replace(":5432/", ":5433/")
        elif is_5432 and not is_5433:
            url = url.replace(":5433/", ":5432/")
    except Exception:
        pass
    return url

DATABASE_URL = resolve_postgres_url()
logger.info(f"SETU Database Layer: Connected strictly to PostgreSQL ({DATABASE_URL.split('@')[-1]})")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={}
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

AsyncSessionLocal = async_session

async def get_db():
    async with async_session() as session:
        yield session
