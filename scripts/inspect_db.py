import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect("postgresql://postgres:admin@127.0.0.1:5432/setu_db")
    rows = await conn.fetch("SELECT id, plate_number, timestamp, camera_id FROM sightings ORDER BY id DESC LIMIT 15")
    for r in rows:
        print(dict(r))
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
