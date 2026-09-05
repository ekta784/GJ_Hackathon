import asyncio
import asyncpg

async def fix_sequences(port):
    try:
        conn = await asyncpg.connect(user='postgres', password='admin', database='setu_db', host='127.0.0.1', port=port)
        tables = ['sightings', 'cameras', 'watchlist', 'departments', 'vendors', 'alerts', 'audit_logs']
        for t in tables:
            try:
                seq = await conn.fetchval(f"SELECT pg_get_serial_sequence('{t}', 'id')")
                if seq:
                    max_id = await conn.fetchval(f"SELECT COALESCE(MAX(id), 1) FROM {t}")
                    new_val = await conn.fetchval(f"SELECT setval('{seq}', {max_id + 1}, false)")
                    print(f"[Port {port}] Sequence {seq} updated -> Next ID will be: {new_val}")
            except Exception as e:
                print(f"[Port {port}] Note on {t}: {e}")
        await conn.close()
    except Exception as e:
        print(f"[Port {port}] Error connecting: {e}")

async def main():
    await fix_sequences(5432)
    await fix_sequences(5433)

if __name__ == '__main__':
    asyncio.run(main())
