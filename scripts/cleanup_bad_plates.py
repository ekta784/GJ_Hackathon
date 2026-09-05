import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect("postgresql://postgres:admin@127.0.0.1:5432/setu_db")
    count_s = await conn.fetchval("SELECT count(id) FROM sightings WHERE plate_number = 'HH12AB3456'")
    print(f"Found {count_s} sightings for HH12AB3456")
    if count_s > 0:
        await conn.execute("UPDATE sightings SET plate_number = 'MH12AB3456' WHERE plate_number = 'HH12AB3456'")
        print("Updated sightings to MH12AB3456")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
