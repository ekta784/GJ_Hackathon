import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "data", "setu.db")

def query_db():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    print("Connecting to SETU Database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check Sightings
        print("\n--- Recent Vehicle Sightings ---")
        cursor.execute("SELECT id, plate_number, camera_id, timestamp, confidence_score FROM sightings ORDER BY timestamp DESC LIMIT 5")
        sightings = cursor.fetchall()
        if not sightings:
            print("No sightings found.")
        else:
            print(f"{'ID':<5} | {'Plate':<12} | {'Camera':<20} | {'Time':<22} | {'Conf'}")
            print("-" * 70)
            for row in sightings:
                print(f"{row[0]:<5} | {row[1]:<12} | {row[2][:18]:<20} | {row[3][:22]:<22} | {row[4]}")

        # Check Alerts
        print("\n--- Recent System Alerts ---")
        cursor.execute("SELECT id, alert_type, entity_id, severity, message, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 5")
        alerts = cursor.fetchall()
        if not alerts:
            print("No alerts found.")
        else:
            print(f"{'ID':<5} | {'Type':<12} | {'Entity':<10} | {'Severity':<10} | {'Message'}")
            print("-" * 80)
            for row in alerts:
                print(f"{row[0]:<5} | {row[1]:<12} | {row[2]:<10} | {row[3]:<10} | {row[4][:30]}")

    except sqlite3.OperationalError as e:
        print(f"Error reading database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    query_db()
