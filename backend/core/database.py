import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

try:
    if "postgresql" in DATABASE_URL:
        import asyncpg  # Test if driver is present
        connect_args = {}
    else:
        DATABASE_URL = "sqlite+aiosqlite:///./setu.db"
        connect_args = {"check_same_thread": False}
except (ImportError, ModuleNotFoundError):
    logger.info("PostgreSQL asyncpg not installed. Falling back to local SQLite database.")
    DATABASE_URL = "sqlite+aiosqlite:///./setu.db"
    connect_args = {"check_same_thread": False}

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

AsyncSessionLocal = async_session

async def get_db():
    async with async_session() as session:
        yield session
