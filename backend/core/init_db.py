import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from backend.core.models import Base
from backend.core.database import DATABASE_URL

async def init_models():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
