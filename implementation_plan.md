# SETU Sentinel — Comprehensive Project Audit & Implementation Plan
### Gujarat Police Innovation Challenge 2026 ("Sentinel")

## Project Audit & Current State Assessment

We conducted a full end-to-end audit of the **SETU** codebase. Here is the operational status:

### 1. What is Completed & Verified ✅
- **Backend Architecture & Async Spine**:
  - FastAPI asynchronous engine with SQLite/PostgreSQL fallback (`backend/main.py`, [database.py](file:///d:/Hackathon/Hackathon/backend/core/database.py), [models.py](file:///d:/Hackathon/Hackathon/backend/core/models.py)).
  - Event spine with in-memory fallback for Kafka (`backend/core/kafka.py`).
  - Native WebSocket streaming for real-time alert broadcasts (`backend/core/websockets.py`).
- **AI Normalisation & Grammar Engine**:
  - Position-aware Indian license plate grammar correction ([normaliser.py](file:///d:/Hackathon/Hackathon/backend/ai/normaliser.py)) enforcing state codes, RTO districts, and position-specific character confusion repairs (`0↔O`, `8↔B`, `1↔I`, `5↔S`, `4↔A`, etc.).
  - Weighted Levenshtein fuzzy distance matching against watchlists with low penalty for known character confusions.
- **Cross-Camera Correlation & Anomaly Detection**:
  - Correlation engine ([correlation.py](file:///d:/Hackathon/Hackathon/backend/services/correlation.py)) tracking vehicle routes across Gujarat nodes.
  - Automated detection of **Impossible Travel / Cloned Plates** using Haversine distance and speed-over-time physics checks (>160 km/h or instant multi-city jumps).
- **Automated Verification Suite**:
  - [test_platform.py](file:///d:/Hackathon/Hackathon/scripts/test_platform.py) tests all 7 key criteria. **ALL 7 TESTS PASS WITH 100% SUCCESS**, including backend health, camera registry, watchlist ingestion, fuzzy OCR matching, the Official Test Case route simulation, route tracing, and impossible travel anomaly detection.
- **Frontend Foundation**:
  - React 19 + TypeScript + Vite + MapLibre GL JS builds with zero errors (`npm run build` succeeds).

---

## Gaps Identified Against Master Prompt & Competition Deliverables

To maximize scoring on **Working Platform & Demonstration**, **Video Analytics Output**, and **Solution Architecture**, the following enhancements are needed:

1. **Dashboard Screens**:
   - `MASTER_PROMPT.md` specifies 7 operational screens:
     1. **Command Center** (High-level Gujarat overview, department metrics, live alerts).
     2. **CCTV Monitoring** (Multi-camera grid with simulated direct-to-browser stream tiles, codec badges for mixed H.264/H.265).
     3. **Alert Center** (Triage list with severity filters and explainability cards).
     4. **Vehicle Investigation ("The Money Screen")** (Interactive route timeline scrub, map polyline with speed vectors, SHA-256 evidence card).
     5. **GIS View** (Full-screen map with coverage radius and department color-coding).
     6. **Watchlist Management** (Manage targets with fuzzy preview).
     7. **Camera Health & Adapter Admin** (Node uptime, reconnect logs, and live 27th vendor adapter onboarding demo).
   - *Current State*: The frontend currently has only 3 basic tabs (`search`, `watchlist`, `cameras`).
2. **Differentiator #1 — Explainable Confidence Breakdown**:
   - Visual breakdown radar/metrics on alert and search cards: Detection %, OCR Character %, Grammar Validity %, Weighted Distance, and deterministic correction notes (e.g. `Position 5 demands letter: 8 -> B`).
3. **Differentiator #2 — Multi-Department & Multi-Vendor Fleet**:
   - Representing the 5 mandated departments (Police, GSRTC, Municipal, Health, Panchayat) and multiple camera vendors across Gujarat.
4. **Jury Demonstration Controls**:
   - 1-click test triggers directly on the UI banner for the 3-step Official Test Case and Cloned Plate anomaly.
5. **Audit Logging & Chain of Custody**:
   - Visual audit trail demonstrating DPDP Act 2023 compliance and evidence hashing.

---

## User Review Required

> [!IMPORTANT]
> The backend server and verification tests are already functional. The upcoming steps focus on elevating the user interface into the **7-screen tactical dashboard**, enriching the mock camera fleet across 5 departments, implementing the live vendor adapter onboarding demo, and polishing the visual explainability tools.

---

## Proposed Changes

### Component 1: Multi-Department Fleet & Fleet Health Telemetry (Backend)
- Expand simulated camera nodes from 6 to 16+ across Gujarat covering **Police, GSRTC Bus Terminals, Municipal Corporations (AMC, SMC, VMC), Health (Civil Hospitals), and Panchayat**.
- Add department and vendor relations, codec types (`H.264`, `H.265`), and stream URLs.
- Add `/api/health/cameras` endpoint returning latency, uptime, reconnect counts, and frame rates.
- Add `/api/audit` endpoint to view append-only officer search and alert logs.

#### [MODIFY] [pipeline.py](file:///d:/Hackathon/Hackathon/backend/ai/pipeline.py)
- Expand `SIMULATED_CAMERAS` with departmental metadata and realistic GPS coordinates across Gujarat.

#### [MODIFY] [main.py](file:///d:/Hackathon/Hackathon/backend/main.py)
- Add endpoints for `/api/departments`, `/api/health/cameras`, `/api/audit`, and adapter dynamic registration (`/api/adapters/register`).
- Update camera seed logic to populate department and vendor mappings.

#### [MODIFY] [api.py](file:///d:/Hackathon/Hackathon/backend/schemas/api.py)
- Update schemas for department tags, vendor info, health statistics, and audit logs.

---

### Component 2: State-of-the-Art 7-Screen Dashboard (Frontend)
- Implement a dark glassmorphic design system matching Gujarat Police command center aesthetics.
- Implement the 7 distinct screens:
  1. **Command Center**: Gujarat map view, live ticker, active camera counts by department (Police, GSRTC, AMC, Health, Panchayat), real-time alerts drawer.
  2. **CCTV Monitoring**: Live multi-camera tile grid demonstrating direct WHEP/HLS video streaming architecture with H.264/H.265 badges and zero-backend-video bandwidth savings (~1,400× metric).
  3. **Alert Center**: Full alert triage desk with severity filters (CRITICAL, HIGH, MEDIUM), filter by alert type (`watchlist_hit`, `impossible_travel`), and audio/visual pulse cues.
  4. **Vehicle Investigation ("The Money Screen")**:
     - Vehicle plate search input with fuzzy auto-correction.
     - Chronological timeline cards with timestamp, camera name, and department badge.
     - Interactive map route polyline connecting sightings with step numbers and directional arrows.
     - Segment speed calculations (e.g., `82 km/h - PLAUSIBLE`).
     - Cryptographic SHA-256 evidence certificate for forensic chain-of-custody.
  5. **GIS View**: Fullscreen interactive map with department filter toggles and camera clustering.
  6. **Watchlist Management**: Add/remove wanted plates, reason, severity, and instant fuzzy match testing tool.
  7. **Camera Health & Adapter Admin**: Fleet monitoring table (Online/Degraded/Offline), uptime, and a live "Onboard 27th Vendor Adapter" interactive demo.

#### [MODIFY] [App.tsx](file:///d:/Hackathon/Hackathon/frontend/src/App.tsx)
- Refactor into modular screen components with navigation bar, test runner triggers, explainable confidence breakdown drawers, and synchronized map interactions.

#### [MODIFY] [App.css](file:///d:/Hackathon/Hackathon/frontend/src/App.css)
- Implement dark glassmorphism styling, alert pulses, timeline connectors, confidence score meters, and responsive grid layouts.

---

### Component 3: Verification & Presentation Deliverables
- Update [test_platform.py](file:///d:/Hackathon/Hackathon/scripts/test_platform.py) to cover newly added endpoints (audit log, camera health, multi-department queries).
- Verify end-to-end operation using browser testing and generate visual artifacts.

---

## Verification Plan

### Automated Tests
- Run `python -u scripts/test_platform.py` to confirm all 7 official test criteria pass alongside newly added endpoints.
- Run `npm run build` in `frontend` to guarantee zero compilation or type errors.

### Manual / Visual Verification
- Start frontend dev server on port `5173` and backend on port `8000`.
- Verify the 7 dashboard screens render cleanly.
- Trigger the **Official Test Case** button in the UI:
  - Confirm wanted vehicle `GJ01AB1234` triggers real-time alerts.
  - Confirm the Investigation Screen plots the route across Ahmedabad, Gandhinagar, and Vadodara with directional arrows, segment speeds, and SHA-256 evidence.
- Trigger the **Cloned Plate / Impossible Travel** button:
  - Confirm the anomaly alert highlights the physics violation (>160 km/h) in red.
