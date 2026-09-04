# SETU: Integrated Video Management & Analytics Platform

**Sentinel (Gujarat Police Innovation Challenge 2026)**

SETU is a metadata-first, vendor-neutral federation layer that unifies heterogeneous government CCTV islands into one searchable ANPR intelligence network. It provides real-time watchlist alerts and cross-camera vehicle route reconstruction without replacing existing departmental systems.

## 🌟 Core Architecture

- **Ingest**: Adapter-based ingest service pulling RTSP streams over TCP via one FFmpeg subprocess per camera (sampled at 5 fps).
- **AI Pipeline**: Two-stage YOLO (vehicle & plate detection) + PaddleOCR (recognition) with a position-aware Indian-plate normalisation and explainable confidence engine.
- **Event Spine**: Apache Kafka carrying only metadata (no video bytes).
- **Correlation**: PostgreSQL + PostGIS storing sightings, routes, evidence hashes, and an audit trail. Topology-aware cross-camera correlation with cloned-plate/impossible-travel detection.
- **Frontend**: React + MapLibre police dashboard with direct WHEP streaming from source to browser.
- **Security**: JWT Auth and 3-role RBAC.

## 🚀 Implementation Status (Active)

We have successfully implemented the core functional aspects:
- **Database Layer**: Initialized SQLAlchemy asynchronous models for the federated system (Departments, Vendors, Cameras, Watchlist, Sightings, Alerts, AuditLogs).
- **AI Processing Engine**: Built a simulated YOLO+PaddleOCR pipeline (`MockAIPipeline`) for the dev sandbox, engineered for zero-config startup while strictly preserving the metadata contract (plate, confidence, SHA256 evidence hash).
- **Kafka Event Spine**: `KafkaPublisher` is actively converting AI detections into lightweight metadata payloads over the `camera_metadata` topic.
- **Correlation Engine**: Background `AIOKafkaConsumer` that:
  - Consumes sightings and logs them to PostgreSQL.
  - Matches plates against the dynamic Watchlist.
  - Computes "Impossible Travel" physics checks across camera topology (Cloned Plate Detection).
  - Broadcasts live WebSocket alerts.
- **Core API Layer**: Fully functional REST API backend (`/api/watchlist`, `/api/search`) connected to PostgreSQL.
- **Frontend Dashboard**: A premium, modern React application has been built from scratch. It features:
  - Glassmorphism & dark mode aesthetics.
  - A real-time **WebSocket Alert Banner** for immediate incident response.
  - A **Watchlist Alert** management interface.
  - A **Global Search** interface designed to track vehicle route topology across the network.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 20+
- Docker & Docker Compose
- (Optional but Recommended) NVIDIA GPU for YOLO/OCR acceleration

### 1. Environment Setup

**Backend (Python)**
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Frontend (React)**
```bash
cd frontend
npm install
```

### 2. Infrastructure (Docker)
The system relies on external services which are spun up using Docker Compose:
- PostgreSQL + PostGIS (with pg_trgm)
- Apache Kafka (KRaft mode)
- Redis / Valkey
- MediaMTX (for local stream simulation)

```bash
# Start all infrastructure services
docker-compose up -d
```

### 3. Running the Application

**Backend API (FastAPI)**
```bash
source venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend Dashboard (Vite + React)**
```bash
cd frontend
npm run dev
```

### 4. Running the Camera Simulator (MediaMTX)
To test ingest, a local replica of the sandbox is provided via MediaMTX and an FFmpeg loop script that simulates 50 concurrent heterogeneous streams.
```bash
# Handled by the Docker Compose stack, or manually:
./scripts/simulate_cameras.sh
```

## 🛠️ Project Structure

```
SETU/
├── backend/               # FastAPI backend
│   ├── api/               # API routers
│   ├── core/              # Config, Security, DB
│   ├── ingest/            # FFmpeg subprocess supervisors & Adapters
│   ├── ai/                # YOLO + PaddleOCR pipeline & plate normalisation
│   ├── services/          # Business logic, tracking, event processing
│   └── main.py            # FastAPI application entrypoint
├── frontend/              # Vite + React + Tailwind + MapLibre GL JS
├── docker-compose.yml     # Infrastructure setup (Postgres, Kafka, Redis, MediaMTX)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🏆 Hackathon Specifics (Phase 1 Deliverables)
1. **Explainable confidence-scored ANPR matching**: Position-aware Indian-plate grammar correction + weighted-Levenshtein fuzzy matching.
2. **Metadata-first federated architecture**: Live-pluggable vendor adapter layer with ~1,400× bandwidth reduction.
3. **Topology-aware cross-camera correlation**: Identifies impossible travel and cloned plates.

## 📜 License
This project is built for the Gujarat Police Innovation Challenge 2026. 
*Note: Ultralytics YOLO is AGPL-3.0 licensed.*
