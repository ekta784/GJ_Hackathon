# SETU Sentinel - Complete Setup & Testing Guide

This guide covers everything you need to start the project from scratch using PostgreSQL, test it on live videos, and understand the overall architecture flow.

## 1. The Overall Architecture Flow

To test effectively, it's important to understand how the components talk to each other:

1. **The Live AI Pipeline (`backend/ai/run_live_video.py`)** 
   - Acts as an edge node (simulating a CCTV camera). It ingests an `.mp4` video file or live webcam feed.
   - It runs the YOLOv8 AI model to detect vehicles and the EasyOCR model to read the license plate.
   - It immediately sends an HTTP POST request containing the plate data to the Backend API.

2. **The Backend (`backend/main.py`)**
   - The FastAPI backend receives the plate data at its `/api/simulate/sighting` endpoint.
   - It saves this exact telemetry (Timestamp, Plate Number, Camera ID, Confidence) securely into the **PostgreSQL Database**.
   - It cross-references the plate with the Watchlist. If it's a match, it generates a high-priority Alert.

3. **The Frontend Dashboard (`React + Vite`)**
   - The dashboard continuously polls or listens to the Backend.
   - When new telemetry or Alerts arrive, it displays them instantly on the Command Center, Watchlist grids, and the GIS Map.

---

## 2. PostgreSQL & pgAdmin Setup (Run Once)

We have transitioned the backend to use a production-grade PostgreSQL database.

### Step 2.1: Install PostgreSQL & pgAdmin
If you haven't already, download and install PostgreSQL for Windows. The installer usually includes **pgAdmin 4** by default. Set the superuser password to something you remember (e.g., `admin`).

### Step 2.2: Create the Database (`setu_db`)

You can create the database either by pasting a command into your terminal OR using the pgAdmin GUI.

**Option A: Quick Terminal Command (Recommended)**
If you have PostgreSQL installed and added to your system path, open a terminal and run:
```cmd
createdb -U postgres setu_db
```
*(It may prompt you for your postgres password).*

**Option B: Using pgAdmin GUI**
1. Open **pgAdmin 4** from your Start menu and log in.
2. In the left sidebar, expand **Servers** > **PostgreSQL**.
3. Right-click on **Databases** -> **Create** -> **Database...**
4. Set the Database name exactly to: `setu_db`
5. Click **Save**.

*Note: You do not need to create any tables manually. The FastAPI backend uses SQLAlchemy to automatically create all the `cameras`, `sightings`, and `alerts` tables inside `setu_db` the first time you run it!*

### Step 2.3: Verify the Tables in pgAdmin
Once you start the backend (instructions below), you can view your data in pgAdmin:
1. Open pgAdmin 4 and expand **Databases** > `setu_db` > **Schemas** > **public** > **Tables**.
2. Right-click on `sightings` (or `alerts`) and select **View/Edit Data** -> **All Rows**.
3. You will see all live detections populated here in real-time.

---

## 3. Activation Checklist (Run Every Time)

Follow these exact steps in order whenever you want to test the project. You will need 3 separate terminal windows.

### Terminal 1: Start the Backend (FastAPI)
1. Navigate to the project root: `cd d:\Hackathon\Hackathon`
2. **Activate the Virtual Environment**: `.\venv\Scripts\activate`
3. Check the `.env` configuration. Ensure `DATABASE_URL` in `backend/core/config.py` or `.env` points to your Postgres instance.
4. **Start the API**:
   ```cmd
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```
*(Watch the logs. If it says "Creating database tables...", your Postgres connection is successful!)*

### Terminal 2: Start the Frontend (React + Vite)
1. Navigate to the project root: `cd d:\Hackathon\Hackathon`
2. **Start the dev server**:
   ```cmd
   cd frontend
   npm run dev
   ```
3. Open your browser to **http://localhost:5173** to view the dashboard.

### Terminal 3: Start the Live AI Video Test
1. Navigate to the project root: `cd d:\Hackathon\Hackathon`
2. **Activate the Virtual Environment**: `.\venv\Scripts\activate`
3. Run the AI inference script:
   ```cmd
   # To test using an "uploaded" local video file:
   python backend/ai/run_live_video.py --source "path_to_your_video.mp4"

   # To test using your laptop webcam:
   python backend/ai/run_live_video.py --source 0
   ```
*(This script will open a window showing the video, draw bounding boxes around cars, run OCR, and you will see terminal logs proving it is posting to the Backend!)*

---

## 4. Testing the Full Flow

1. Open the **Frontend Dashboard**.
2. Go to the **Watchlist Management** tab.
3. Add a license plate number that you know will appear in your test `.mp4` video (e.g., `GJ01AB1234`).
4. **Run the AI Video Script** (Terminal 3) on that `.mp4` video.
5. As the video plays, wait for the AI to recognize the vehicle.
6. The moment it detects the plate, it POSTs it to the Backend. The Backend matches it against the Watchlist in PostgreSQL.
7. Instantly, the Dashboard will light up with a flashing **Live Alert** in the Alert Center!





<!-- Step 1: Start the Live Webcam AI
Open a new terminal in your d:\Hackathon\Hackathon folder.
Activate your virtual environment: .\venv\Scripts\activate
Run the live script and tell it to use your webcam (source 0):
cmd
python backend/ai/run_live_video.py --source 0
A window will instantly pop up showing your live webcam feed!
Step 2: The Live Test
Open your Dashboard (http://localhost:5173) and go to the Watchlist tab.
Add a test license plate to the watchlist, for example: MH12AB3456
Now, take out your smartphone and Google search for a picture of an Indian license plate that says "MH12AB3456" (or just write it really clearly in dark marker on a white piece of paper).
Hold your phone (or the paper) up to your laptop's webcam!
The Magic: As soon as you hold it up, you will see the YOLO AI draw a box around it in the webcam window. EasyOCR will read the text, and you will see a Live Red Flashing Alert instantly appear on your Dashboard!
Alternative: What if I have a real live stream?
If you have an actual live IP Camera or RTSP stream, you don't need to upload anything. You just replace the 0 with the live URL!

cmd
python backend/ai/run_live_video.py --source "rtsp://192.168.1.100:554/stream"
Try the Webcam + Smartphone trick right now using --source 0. It proves to the judges that your AI pipeline is reading the physical world in real-time and pushing it to the Postgres database and React dashboard without any "uploaded files" or fake simulations! Let me know if you get the live alert!

 -->







 <!-- ## 3. Step-by-Step Manual Testing Guide Using Your UI

  Ensure both your backend and frontend are running:

  • Backend: .\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
  • Frontend: npm.cmd run dev inside frontend/
  • Open your browser to: http://localhost:5173
  ──────
  ### Step 1: Verify the Command Center (Screen 1)

  1. Look at the top navigation bar: verify the green pill says SPINE ONLINE and WS CONNECTED.
  2. Inspect the Federated Department Status Cards:
      • Police (5 cameras)
      • GSRTC (3 cameras)
      • Municipal (3 cameras)
      • Health (3 cameras)
      • Panchayat (3 cameras)
  3. Note the ~1,400× Bandwidth Savings pill, showing proof of zero-central-video federation.
  ──────
  ### Step 2: Trigger the Official Government Test Case

  1. Click the bright green button on the top banner: ⚡ Run Official Test Case Simulation.
  2. Notice what happens immediately:
      • A flashing Live Alert Banner slides down from the top: "Target Sighting: GJ01AB1234 spotted at SG Highway - ISKCON Cross Rd".
      • A quick notification confirms 3 sequential sightings were simulated across Ahmedabad.

  ──────
  ### Step 3: Test Vehicle Route Tracing on the GIS Map (Screen 4)

  1. Click on the Vehicle Investigation tab in the top navbar.
  2. In the search box on the right, ensure GJ01AB1234 is entered (or click the sample pill GJ01AB1234 (Official Test)).
  3. Click Trace.
  4. Observe the Left Side (Interactive Map):
      • The map loads OpenStreetMap/CartoDB tiles centered on Ahmedabad.
      • You will see numbered markers: #1, #2, and #3.
      • A cyan route line connects the cameras from SG Highway → C.G. Road → Sardar Patel Ring Road.
      • Click on any marker pin to open a popup showing Camera Name, Department, Exact Timestamp, and Speed.
  5. Observe the Right Side (Timeline & Forensic Certificate):
      • Chronological Waypoints list each stop with transit speeds (e.g. 68.2 km/h - PLAUSIBLE).
      • The bottom displays the Gujarat SCRB Forensic Audit Stamp with an immutable SHA-256 cryptographic evidence hash.

  ──────
  ### Step 4: Test the "Impossible Travel" / Cloned Plate Anomaly

  1. Go back to the Command Center tab.
  2. Click the red button: 🚨 Run Cloned Plate Anomaly Test.
  3. A critical red flashing banner appears at the top.
  4. Click on the Alert Center tab in the navbar:
      • You will see a priority alert titled IMPOSSIBLE TRAVEL / CLONED PLATE for vehicle GJ01XY9999.
      • Expand the alert card: It shows the car was detected in Ahmedabad and Surat (260 km apart) within 1 second — calculating a
      transit velocity of over 900,000 km/h!
  5. Now switch to the Vehicle Investigation tab and search for GJ01XY9999:
      • The route markers turn bright red.
      • The transit tag displays: ⚠️ IMPLAUSIBLE (>160 km/h).

  ──────
  ### Step 5: Test Explainable AI & Fuzzy OCR Matching (Screen 6)

  1. Click the Watchlist Management tab.
  2. Scroll to the Live Fuzzy OCR & Grammar Normalisation Playground.
  3. Type in misread plates with common optical character confusions:
      • Type: GJ 01 A8 1234 → The engine auto-detects that position 6 demands a letter, converting 8 to B (GJ01AB1234).
      • Type: GJ 01 AB 123O → The engine detects that position 10 demands a digit, converting O to 0 (GJ01AB1230).
      • Type: G3 01 AB 1234 → Converts 3 to J based on Gujarat state code syntax.
  4. You can also add a new wanted plate into the database using the + Add Target form above and verify it appears in the grid below.
  ──────
  ### Step 6: Test Multi-Vendor CCTV Monitoring (Screen 2)

  1. Click the CCTV Monitoring tab.
  2. Observe the 3×3 video grid showing feeds across Gujarat.
  3. Notice the badges on each stream tile:
      • Department badges: Police (Blue), GSRTC (Orange), Municipal (Green), Health (Pink), Panchayat (Purple).
      • Codec badges: Demonstrates handling mixed H.264 and H.265 streams.
      • Click Inspect on any feed to view its latency, RTSP endpoint, and direct WHEP browser streaming parameters.
  ──────
  ### Step 7: Test Statewide GIS Topology (Screen 5)

  1. Click the GIS Map View tab.
  2. The full-screen Gujarat map displays all 17+ camera nodes clustered across Ahmedabad, Gandhinagar, Surat, Vadodara, Rajkot, and
  Kutch.
  3. Click the department filter buttons on the top right (Police, GSRTC, Municipal, etc.):
      • The pins on the map filter in real-time to display each department's camera footprint.

  ──────
  ### Step 8: Test Dynamic Vendor Adapter Onboarding (Screen 7)

  1. Click the Camera Health / Admin tab.
  2. Review the live telemetry: Average Latency (~18ms), System Uptime (99.98%), and zero packet loss.
  3. Scroll to the "Onboard 27th Department Adapter" tool on the right.
  4. Select a vendor (e.g. Bosch Video Security), department (e.g. Municipal), and region (Gandhinagar Smart City), then click
  Register & Federate Adapter.
  5. The system instantly registers the adapter and dynamically connects the new camera nodes without stopping or restarting the
  platform. -->




  flowchart TD
    A[CCTV Stream / Live Video / Simulator] -->|Edge Video Inference| B[YOLOv8 + EasyOCR + Syntax Normaliser]
    B -->|Metadata Only: Plate, Lat/Lon, SHA-256| C[FastAPI REST /api/simulate]
    C --> D[Event Spine & Correlation Engine]
    D -->|Check Watchlist| E[PostgreSQL / SQLite Database]
    D -->|Speed > 160 km/h or Δt < Δd| F[Impossible Travel Anomaly Detector]
    D -->|Live WebSocket Broadcast /ws/alerts| G[React Dashboard]
    G --> H[1. Flashing Live Alert Banner]
    G --> I[2. Route Tracing on GIS Map]
    G --> J[3. Immutable SHA-256 Forensic Certificate]
