import asyncio
import asyncpg

async def sync():
    c3 = await asyncpg.connect(user='postgres', password='admin', database='setu_db', host='127.0.0.1', port=5433)
    c2 = await asyncpg.connect(user='postgres', password='admin', database='setu_db', host='127.0.0.1', port=5432)
    
    print("Connected to both databases...")
    
    # 1. Sync Departments
    depts = await c3.fetch("SELECT id, name FROM departments")
    for d in depts:
        await c2.execute("INSERT INTO departments (id, name) VALUES ($1, $2) ON CONFLICT (id) DO NOTHING", d['id'], d['name'])
    print(f"Synced {len(depts)} departments.")

    # 2. Sync Vendors
    vends = await c3.fetch("SELECT id, name FROM vendors")
    for v in vends:
        await c2.execute("INSERT INTO vendors (id, name) VALUES ($1, $2) ON CONFLICT (id) DO NOTHING", v['id'], v['name'])
    print(f"Synced {len(vends)} vendors.")

    # 3. Sync Cameras
    cams = await c3.fetch("SELECT id, name, url, latitude, longitude, status, fps, resolution, geom_source, codec, district, department_id, vendor_id FROM cameras")
    for c in cams:
        await c2.execute("""
            INSERT INTO cameras (id, name, url, latitude, longitude, status, fps, resolution, geom_source, codec, district, department_id, vendor_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            ON CONFLICT (id) DO NOTHING
        """, c['id'], c['name'], c['url'], c['latitude'], c['longitude'], c['status'], c['fps'], c['resolution'], c['geom_source'], c['codec'], c['district'], c['department_id'], c['vendor_id'])
    print(f"Synced {len(cams)} cameras.")

    # 4. Sync Watchlist
    watches = await c3.fetch("SELECT id, plate_number, reason, severity, added_at FROM watchlist")
    for w in watches:
        await c2.execute("""
            INSERT INTO watchlist (id, plate_number, reason, severity, added_at)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO NOTHING
        """, w['id'], w['plate_number'], w['reason'], w['severity'], w['added_at'])
    print(f"Synced {len(watches)} watchlist targets.")

    # 5. Sync Sightings (including all MH12AB3456 sightings!)
    sightings = await c3.fetch("SELECT id, plate_number, confidence_score, plate_det_conf, ocr_char_conf, format_validity, camera_id, timestamp, snapshot_sha256 FROM sightings")
    for s in sightings:
        await c2.execute("""
            INSERT INTO sightings (id, plate_number, confidence_score, plate_det_conf, ocr_char_conf, format_validity, camera_id, timestamp, snapshot_sha256)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (id) DO NOTHING
        """, s['id'], s['plate_number'], s['confidence_score'], s['plate_det_conf'], s['ocr_char_conf'], s['format_validity'], s['camera_id'], s['timestamp'], s['snapshot_sha256'])
    print(f"Synced {len(sightings)} sightings to Port 5432!")

    # Verify count on 5432
    count_5432 = await c2.fetchval("SELECT count(1) FROM sightings")
    mh_5432 = await c2.fetchval("SELECT count(1) FROM sightings WHERE plate_number = 'MH12AB3456'")
    print(f"\n[SUCCESS] PostgreSQL Port 5432 now has {count_5432} total sightings, including {mh_5432} for 'MH12AB3456'!")

    await c3.close()
    await c2.close()

if __name__ == '__main__':
    asyncio.run(sync())
