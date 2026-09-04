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