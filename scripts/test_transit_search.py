import urllib.request
import json
import time

def main():
    plate = "MH12AB3456"
    now = time.time()
    route = [
        ("SG Highway - ISKCON Cross Rd", now - 2400),
        ("Gandhinagar CH-0 Circle", now - 1200),
        ("Vadodara Express Highway Exit", now)
    ]

    for cam, ts in route:
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/simulate/sighting",
            data=json.dumps({
                "camera_name": cam,
                "plate_number": plate,
                "timestamp": ts,
                "auto_watchlist": True
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req)
        print(f"Dispatched at {cam}: HTTP {resp.getcode()}")

    # Query search for MH12AB3156 (which will match via fuzzy search)
    resp = urllib.request.urlopen("http://127.0.0.1:8000/api/search/MH12AB3156")
    data = json.loads(resp.read())
    print(f"\nTotal route waypoints logged: {len(data)}")
    for idx, s in enumerate(data[-3:]):
        print(f"Stop #{idx+1}: {s['camera_name']} ({s['latitude']}, {s['longitude']}) - Plausibility: {s.get('transit_plausibility')}")

if __name__ == "__main__":
    main()
