import asyncio
import asyncpg
import sqlite3

async def check_pg(port):
    try:
        conn = await asyncpg.connect(user='postgres', password='admin', database='setu_db', host='127.0.0.1', port=port)
        total = await conn.fetchval('SELECT count(1) FROM sightings')
        mh_count = await conn.fetchval("SELECT count(1) FROM sightings WHERE plate_number = 'MH12AB3456'")
        last_rows = await conn.fetch("SELECT id, plate_number, timestamp, camera_id FROM sightings ORDER BY id DESC LIMIT 3")
        print(f"[Postgres Port {port}] Total Sightings: {total} | MH12AB3456 Count: {mh_count}")
        for r in last_rows:
            print(f"   -> ID={r['id']}, Plate={r['plate_number']}, Time={r['timestamp']}, Cam={r['camera_id']}")
        await conn.close()
    except Exception as e:
        print(f"[Postgres Port {port}] Error: {e}")

def check_sqlite():
    try:
        conn = sqlite3.connect('setu.db')
        c = conn.cursor()
        total = c.execute('SELECT count(1) FROM sightings').fetchone()[0]
        mh = c.execute("SELECT count(1) FROM sightings WHERE plate_number = 'MH12AB3456'").fetchone()[0]
        print(f"[SQLite setu.db] Total Sightings: {total} | MH12AB3456 Count: {mh}")
        conn.close()
    except Exception as e:
        print(f"[SQLite] Error: {e}")

async def main():
    await check_pg(5432)
    await check_pg(5433)
    check_sqlite()

if __name__ == '__main__':
    asyncio.run(main())
