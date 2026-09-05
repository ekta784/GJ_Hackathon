import urllib.request
import json

def send(plate, cam):
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/simulate/sighting",
        data=json.dumps({
            "camera_name": cam,
            "plate_number": plate,
            "auto_watchlist": True
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req)
    return resp.getcode()

def main():
    print("Testing sending PB10AS0210 multiple times...")
    send("PB10AS0210", "SG Highway - ISKCON Cross Rd")
    send("PB10AS0210", "Gandhinagar CH-0 Circle")

    print("Testing sending a second unique plate GJ05JD9759 multiple times...")
    send("GJ05JD9759", "Vadodara Express Highway Exit")
    send("GJ05JD9759", "Surat Ring Road - Majura Gate")

    # Check watchlist
    resp = urllib.request.urlopen("http://127.0.0.1:8000/api/watchlist")
    items = json.loads(resp.read())
    print("\n--- Current Watchlist Targets in DB ---")
    for it in items:
        print(f" - ID={it['id']}: {it['plate_number']} ({it['reason']})")

if __name__ == "__main__":
    main()
