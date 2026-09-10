import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect('postgresql://postgres:admin@127.0.0.1:5432/setu_db')
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    print("Postgres Tables:", [t['table_name'] for t in tables])
    for t in tables:
        count = await conn.fetchval(f"SELECT count(*) FROM {t['table_name']}")
        print(f"  {t['table_name']}: {count} rows")
    await conn.close()

if __name__ == '__main__':
    asyncio.run(check())
