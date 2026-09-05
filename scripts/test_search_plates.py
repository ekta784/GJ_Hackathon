import urllib.request
import json

def test_search(plate):
    resp = urllib.request.urlopen(f"http://127.0.0.1:8000/api/search/{plate}")
    data = json.loads(resp.read())
    print(f"\nTrace results for {plate}: {len(data)} waypoints found")
    for idx, s in enumerate(data[-4:]):
        print(f"  Stop #{idx+1}: {s['camera_name']} ({s['latitude']}, {s['longitude']}) - Plausibility: {s.get('transit_plausibility')}")

if __name__ == "__main__":
    test_search("PB10AS0210")
    test_search("GJ05JD9759")
