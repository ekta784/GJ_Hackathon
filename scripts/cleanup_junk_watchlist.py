import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect("postgresql://postgres:admin@127.0.0.1:5432/setu_db")
    # Plates to remove
    junk_plates = ["MH124834", "PB10AS5021", "JZ4RRC1324"]
    for p in junk_plates:
        # Get watchlist id
        row = await conn.fetchrow("SELECT id FROM watchlist WHERE plate_number = $1", p)
        if row:
            wid = row["id"]
            # Nullify any alert FKs
            await conn.execute("UPDATE alerts SET watchlist_id = NULL WHERE watchlist_id = $1", wid)
            # Delete watchlist row
            await conn.execute("DELETE FROM watchlist WHERE id = $1", wid)
            print(f"Cleanly removed junk watchlist item: {p} (id={wid})")
    
    # Print remaining watchlist items
    rows = await conn.fetch("SELECT id, plate_number, reason FROM watchlist ORDER BY id ASC")
    print("\n--- Current Clean Watchlist ---")
    for r in rows:
        print(f"ID={r['id']}: {r['plate_number']} - {r['reason']}")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
