# SETU — Gujarat Police Innovation Challenge 2026
### Complete Analysis, Architecture Decision & Build Plan

**Document status:** Analysis complete. No code written yet (implementation paused at user request).
**Prepared:** 2 September 2026
**Deadline:** 7 September 2026 — **5 days**
**Event:** 10–11 September 2026, i-Hub Gujarat

---

## ⚠ READ THIS FIRST — THREE FACTS THAT SHAPE EVERYTHING

1. **This is not a weekend hackathon.** Phase 1 is a *remote submission* due **7 Sep**. The on-site event (10–11 Sep) is only for the 6 shortlisted teams. You have five days to produce a working platform **plus six graded documents/videos**.
2. **This is an integration problem, not an AI problem.** Four of the five official reference models are architectural. Three of seven evaluation criteria are about architecture, scalability and platform maturity. ANPR is the mandatory *proof*, not the prize.
3. **The team's PDF was never reviewed** — it did not reach the analysis session. All critique below targets the *baseline tech stack* that was pasted in the prompt, used as a proxy. Re-run the gap analysis against the real PDF.

---

# 1. THE OFFICIAL PROBLEM STATEMENT (VERIFIED)

**Primary source of truth:** https://sentinel.gujarat.gov.in
(Pages consulted: `/`, `/about`, `/problems`, `/phases`, `/resource`, `/schedule`, `/faqs`)

## 1.1 Event facts

| Item | Official value |
|---|---|
| Name | **Gujarat Police Innovation Challenge 2026** (portal brand: "Sentinel") |
| Organiser | Gujarat Home Department / Gujarat Police, State Crime Record Bureau, Sector 18, Gandhinagar |
| Partners | i-Hub Gujarat (technology); DA-IICT & NFSU (knowledge) |
| Deliverable | An **"Integrated Video Management & Analytics Platform"** |
| Scale context | ~**26 independent** government CCTV systems · ~**80,000 cameras** · dispersion up to **1,000 km** · **5 departments** (Health, Police, GSRTC, Panchayat, Municipal) |
| Sandbox | ~**50 geographically distributed** simulated feeds from **30+ cameras**, ~**12 h** footage each, recorded footage restreamed via Python middleware |
| Categories | Cat 1: students + small/medium startups · Cat 2: large startups + established companies |
| Structure | Phase 1 Sandbox → top 3 per category → **6 teams** → Phase 2 Grand Finale |
| Prize pool | **₹51,00,000** (Phase 1 ₹18L · Phase 2 ₹31L) |
| Contact | sentinel.hackathon@gujarat.gov.in · +91 95370 89982 |

**Prize discrepancy:** press coverage (ANI, IANS, Gujarat Samachar, Aug 2026) says ₹37 lakh. **The portal says ₹51 lakh. The portal wins.** Treat all news figures as stale.

## 1.2 Timeline

| Date | Milestone |
|---|---|
| 4 Aug 2026 | Registration opens |
| **7 Sep 2026** | **Application + submission deadline** |
| 7 Sep 2026 (evening) | Shortlisting announced |
| 10–11 Sep 2026 | Hackathon event at i-Hub Gujarat |
| 11 Sep 2026 | Results & prize distribution |

## 1.3 Prize breakdown

**Phase 1 — ₹18,00,000**

| Position | Category 1 | Category 2 |
|---|---|---|
| 1st | ₹4,00,000 | ₹5,00,000 |
| 2nd | ₹2,00,000 | ₹3,00,000 |
| 3rd | ₹1,00,000 | ₹2,00,000 |

Consolation: ₹25,000 × 4 teams = ₹1,00,000

**Phase 2 — ₹31,00,000**

| Position | Prize |
|---|---|
| 1st (Grand Winner) | ₹16,00,000 |
| 2nd (Runner Up) | ₹8,00,000 |
| 3rd (2nd Runner Up) | ₹7,00,000 |

Plus ₹50,000 × 3 non-top-three finalists, and a ₹50,000 Special Jury Award.

## 1.4 ⭐ THE OFFICIAL TEST CASE (the single most important paragraph)

Participants must:

1. Onboard approximately **50 geographically distributed heterogeneous cameras**
2. Demonstrate **centralised monitoring and AI-powered analytics**
3. **Identify and trace a government-provided vehicle registration** across the integrated network
4. Present **timestamped movement history with location-wise tracking**
5. **Cross-reference live feeds against a representative watchlist database**
6. **Generate automated real-time alerts** upon successful matches

> Everything you build must serve these six lines. If a feature does not serve them or a named bonus, cut it.

## 1.5 The five official reference models

| # | Model | Essence |
|---|---|---|
| 1 | Centralised CCTV Registry & GIS Mapping | Metadata/asset visibility only. Onboarding, GIS, health, gap analysis. No central video. |
| 2 | Unified Viewing & Metadata Analytics | Central viewing via RTSP/ONVIF, no middleware. ANPR metadata + event tagging. |
| 3 | VMS Federation & Middleware Integration | Vendor adapters, metadata exchange, event correlation. Departments retain control. |
| 4 | Central VMS | Full centralised ingest, recording, storage, playback + ANPR, face recognition, statewide tracking. |
| 5 | Hybrid / Innovative | Combine models or propose something novel. |

**Model 4 is the trap.** It is the easiest to demo and arithmetically impossible at 80,000 cameras (see §6.2).

## 1.6 The seven official evaluation criteria

1. **Successful Test Case** — operation on government CCTV feed + required analytics output
2. **Solution Presentation** — clarity of problem understanding and proposed model
3. **Solution Architecture** — technical soundness, security, interoperability, HLD clarity
4. **Working Platform & Demonstration** — maturity on participant and government feeds
5. **Video Analytics Output** — quality of ANPR, detection, recognition, timestamps, reporting
6. **Scalability & PoC Readiness** — capability to scale toward ~80,000 cameras
7. **Submission Completeness** — accessibility and consistency of all required documents

> **Scoring weights are NOT published. "Not confirmed by the official problem statement."**
> Note that 3 of 7 criteria (3, 6, and arguably 4) are architecture/scale — not AI accuracy.

## 1.7 Official bonus considerations

- Innovative hybrid or customised architecture with operational value
- **Advanced cross-camera vehicle tracking or multi-camera correlation**
- Additional reliable analytics **beyond mandatory ANPR**
- Strong **edge processing / bandwidth optimisation** for low-connectivity scenarios
- Enhanced **cybersecurity, privacy protection, auditability, RBAC**
- Operational dashboards, automated alerts, **health monitoring**, integration-ready APIs

## 1.8 Mandatory submission deliverables (all six are graded)

1. **Solution Presentation (PPT/PDF)** — model justification, architecture, analytics approach, technologies, scalability/security, operational impact
2. **High-Level Design Document** — architecture diagrams, CCTV integration approach, video stream processing, watchlist correlation methodology, alert workflows, interoperability
3. **Own-Feed Demonstration Video** — **2–3 minutes max**, screen recording: onboarding → AI detection → watchlist correlation → alert → visualisation, on your own CCTV footage
4. **Government-Feed Demonstration** — onboarding, live/recorded viewing, analytics output, screen recording **+ output report showing detected vehicles/plates with timestamps**
5. **Video & Output Reports** — documented results from government-feed analysis
6. **Submission Links** — unlisted YouTube, Google Drive/OneDrive, **hosted platform URL with credentials**, GitHub/GitLab repo

> FAQ is explicit: demos must show **actual working software, not mockups**.

## 1.9 ⭐ Official technology mandate

> **"All solutions should use open-source technologies"** — including **React, Python, Node.js, PostgreSQL, PostGIS, WebRTC, RTSP, Kafka, TensorFlow, PyTorch, FFmpeg.**

This list is not a suggestion. It is a statement about what the police can maintain after the hackathon ends. Deviating requires justification; matching it is free credibility.

## 1.10 ⭐ Sandbox integration spec (from `/resource`)

**Protocols**

| Protocol | URL pattern | Use |
|---|---|---|
| RTSP | `rtsp://<host>:8554/stream/<id>` | AI inference (OpenCV, GStreamer, FFmpeg, DeepStream) |
| WebRTC (WHEP) | `http://<host>:8889/stream/<id>/whep` | Low-latency browser preview |
| HLS | `http://<host>/live/stream/<id>/index.m3u8` | Dashboards, mobile |

**Camera catalogue API:** `GET http://<host>/api/ingest` → camera IDs, locations, codecs, live status, stream properties, all URLs.

**Hard constraints (each one is a way to fail):**

- Real-time delivery only — **one second of video takes one second to arrive**
- **No seeking, no byte-range fetching, no ahead-of-time playback**
- Monotonic presentation timestamps (PTS) on all frames
- **H.264 *and* H.265** — mixed across cameras
- **Variable frame rates and resolutions** across cameras
- **Force RTSP over TCP** (UDP fails across NAT/firewalls)
- **Automatic reconnection with exponential backoff (~2 s → ~30 s)**
- **Do not assume constant frame rate; do not use `CAP_PROP_FPS`**
- **Feeds loop continuously** → handle scene discontinuities
- Decoder warnings on connect must not cause failure

**Official pre-submission checklist:** TCP transport enforced · no timing logic dependent on `CAP_PROP_FPS` · pipeline tolerates inter-frame gaps · decoder warnings non-fatal · mixed H.264/H.265 and variable resolutions supported.

## 1.11 NOT confirmed by the official problem statement

- Scoring weights per criterion
- **Team size limits** (schedule page is silent)
- Whether Phase 1 is purely remote (strongly implied by the deliverables, not stated)
- Whether GPUs/hardware are provided at i-Hub for the finale
- The actual sandbox `<host>` (issued after registration)
- Any face-recognition requirement in the **test case** (it appears only inside *Model 4's description*)
- Any suspicious-activity / behaviour-detection requirement (appears only in **press coverage**, not the portal)

---

# 2. THE PROBLEM IN PLAIN LANGUAGE

Gujarat has ~80,000 government CCTV cameras, bought at different times by different departments — Health for hospitals, GSRTC for bus depots, municipalities for junctions, panchayats for villages, police for their own premises. Each department bought a different vendor, a different VMS, a different network, a different video format.

The result is **26 separate islands of surveillance**. A camera in Ahmedabad sees a suspicious car. A camera in Gandhinagar sees the same car 40 minutes later. Nobody knows they are the same car, because the two systems cannot talk. Today an investigator physically travels to a control room, asks an operator to scrub footage, and repeats that per jurisdiction. Answering *"where has this car been today?"* takes days. By then the trail is cold.

**Gujarat Police do not want new cameras and do not want to replace 26 working systems.** They want a **layer above** the existing systems that ingests whatever video those systems already emit, reads number plates automatically, checks them against a wanted list, alerts instantly, and stitches sightings from *different departments' cameras* into one map and timeline.

**Users:** control-room operator · investigating officer · watchlist administrator · system administrator · senior officer.
**Input:** ~50 heterogeneous live RTSP streams (mixed codecs, variable fps/resolution) + a watchlist of registrations + a camera catalogue.
**Output:** timestamped plate detections with snapshots and confidence · real-time watchlist alerts · a per-vehicle movement timeline drawn on a GIS map.

**Why it is hard:** decoding 50 simultaneous real-time streams is genuinely expensive; you cannot rewind a live feed; Indian plates are small, dirty, angled and motion-blurred; OCR *will* read `B` as `8`; naive string-equality matching produces so many false alerts that officers stop trusting the system; and the whole design must be believable at 1,600× the demo scale.

### One-sentence summary

> **The actual problem we need to solve is turning 26 incompatible, multi-vendor government CCTV islands into one searchable, vendor-neutral intelligence layer that can answer "where has this vehicle been?" in seconds instead of days — and prove that answer scales to 80,000 cameras.**

---

# 3. CORE PROBLEM ANALYSIS

## 3.1 What the core problem IS

A **heterogeneous-systems integration problem**, with **ANPR-based cross-camera correlation as its proof**. Two inseparable halves:

1. **Vendor interoperability & scale-out ingestion** — the hard, differentiating part
2. **Cross-camera vehicle correlation** — the part the test case actually measures

**Evidence (from official text, not opinion):** the challenge is titled around integrating 26 systems / 80,000 cameras · four of five reference models are architectural · three of seven criteria are integration/scale while only one is analytics quality · the test case's verb is *"trace across the integrated network"*, not *"detect a plate"*.

## 3.2 What the core problem is NOT

| Not the core problem | Why |
|---|---|
| "Build a better ANPR model" | Mandatory but commodity. 94% vs 91% wins nothing. Everyone will have ANPR. |
| Real-time video streaming performance | The sandbox hands you WHEP and HLS. Consume them; don't rebuild them. |
| Suspicious-activity detection | In **press coverage only**. The official test case does not require it. Press ≠ problem statement. |
| Building a VMS | The statement explicitly frames the goal as working *with* existing departmental systems. |

## 3.3 Why this framing wins

At 50 cameras ANPR is easy and ingestion is hard. At 80,000 cameras ANPR is still easy per-stream and ingestion is *impossible* unless the architecture is metadata-first and federated. The jury includes Gujarat Police leadership who own the 26-island problem operationally.

> **The team that wins is the one whose 50-camera demo is visibly a scaled-down instance of an 80,000-camera design — not a great demo with a scalability slide bolted on.**

---

# 4. REQUIREMENT MATRIX

Classification: **MANDATORY** = explicit in test case/deliverables · **EXPECTED** = explicit in evaluation criteria · **BONUS** = named in bonus list · **INFERRED** = follows necessarily · **ASSUMPTION** = ours.

| # | Requirement | Official Source | Class | Priority |
|---|---|---|---|---|
| 1 | Onboard ~50 heterogeneous cameras | Test case | MANDATORY | P0 |
| 2 | RTSP over TCP + exponential backoff reconnect | Resources | MANDATORY | P0 |
| 3 | Mixed H.264/H.265, variable fps/resolution | Resources | MANDATORY | P0 |
| 4 | PTS-driven timing, never `CAP_PROP_FPS` | Resources | MANDATORY | P0 |
| 5 | Consume camera catalogue via `/api/ingest` | Resources | MANDATORY | P0 |
| 6 | Handle looping feeds / scene discontinuity | Resources | MANDATORY | P0 |
| 7 | ANPR with timestamps | Criteria + Models | MANDATORY | P0 |
| 8 | Watchlist cross-reference | Test case | MANDATORY | P0 |
| 9 | Real-time alerts on match | Test case | MANDATORY | P0 |
| 10 | Trace a given plate across cameras | Test case | MANDATORY | P0 |
| 11 | Timestamped, location-wise movement history | Test case | MANDATORY | P0 |
| 12 | GIS visualisation of route | Guide Step 4 | MANDATORY | P0 |
| 13 | 80,000-camera scalability plan | Guide Step 6 | MANDATORY | P0 |
| 14 | Open-source technologies only | About page | MANDATORY | P0 |
| 15 | Six submission artefacts | Deliverables | MANDATORY | P0 |
| 16 | Hosted platform URL **with credentials** | Deliverables | MANDATORY (implies auth) | P0 |
| 17 | Vendor-neutral adapter layer | Models 2/3 | EXPECTED | P1 |
| 18 | Live viewing in dashboard | Models 2/4 | EXPECTED | P1 |
| 19 | Searchable vehicle records | Model 2 | EXPECTED | P1 |
| 20 | Camera health monitoring | Model 1 + bonus | EXPECTED/BONUS | P1 |
| 21 | Security · RBAC · audit · privacy | Criteria + bonus | EXPECTED/BONUS | P1 |
| 22 | Advanced cross-camera correlation | Bonus | BONUS | P1 |
| 23 | Edge processing / bandwidth optimisation | Bonus | BONUS | P1 |
| 24 | ONVIF discovery | Model 2 | EXPECTED | P2 |
| 25 | Analytics beyond ANPR (colour/type) | Bonus | BONUS | P2 |
| 26 | Face recognition | Model 4 description only | OPTIONAL | **P3 — DROP** |
| 27 | Recording / storage / playback | Model 4 only | OPTIONAL | **P3 — DROP** |
| 28 | Vehicle Re-ID | — | OUR ASSUMPTION | **P3 — DROP** |

## 4.1 MUST BUILD

1. Multi-stream RTSP ingest — 50 concurrent, TCP, backoff, mixed codecs, adaptive frame sampling
2. Camera registry from `/api/ingest`, lat/long in PostGIS, live health status
3. ANPR pipeline: vehicle detect → plate detect → OCR → normalise → confidence
4. Watchlist store + **fuzzy, confidence-scored matching** (never string equality)
5. Sighting event store: plate, camera, timestamp, snapshot, confidence
6. Real-time alert generation + WebSocket push
7. Investigation search: plate in → sighting timeline + snapshots out
8. GIS map: camera locations, sighting pins, ordered route polyline
9. Auth + 3-role RBAC
10. Docker Compose one-command deploy
11. **The six submission artefacts**

## 4.2 SHOULD BUILD

12. Vendor adapter abstraction + ≥2 concrete adapters + 1 stub (proves extensibility)
13. Camera health dashboard: online/offline/degraded, last-frame age, reconnects, fps drift
14. Kafka (KRaft, single broker) as the event spine
15. Multi-frame plate voting within a ByteTrack track
16. Explainable confidence breakdown in the alert UI
17. Audit log on every search, watchlist edit, alert view
18. Edge deployment profile (same container, `EDGE_MODE=1`, metadata only)

## 4.3 NICE TO HAVE

19. Vehicle colour/type attributes
20. Topology-aware time/distance plausibility
21. Route anomaly / cloned-plate flag
22. Prometheus + Grafana
23. Evidence hash-chain
24. PDF investigation report export

## 4.4 ⛔ DO NOT BUILD

| Item | Why not |
|---|---|
| **Face recognition** | Not in the test case. DPDP Act 2023 exposure. Eats the GPU budget ANPR needs. Address as an HLD roadmap item with privacy safeguards — that scores better than a shaky demo. |
| **Full VMS** (recording/storage/playback) | Weeks of work, zero test-case credit. |
| **Vehicle Re-ID / appearance embeddings** | Plate identity is the official tracing key. Research rabbit hole. |
| **Elasticsearch** | `pg_trgm` does fuzzy plate search. One less service to break. |
| **Kubernetes** | Docker Compose. K8s belongs in the *production* diagram only. |
| **Custom mobile app** | Responsive web is enough. |
| **Training a detector from scratch** | Fine-tune pretrained, or use a pretrained plate model as-is. |
| **Any LLM in the detection path** | Conventional CV is the correct and faster solution. |
| **Suspicious-activity detection** | Press-only requirement. Costs days, earns bonus points at best. |

---

# 5. CRITIQUE OF THE PROPOSED STACK

> ⚠ **The team PDF was not available.** This critiques the *baseline stack pasted in the prompt*, treated as a proxy. **Re-run against the real PDF.**

## 5.1 What is right

The core stack maps almost one-for-one onto the officially named open-source list: React/TS/Vite, FastAPI, PyTorch+YOLO, plate detector + PaddleOCR, PostgreSQL+PostGIS, Redis, MapLibre, WebSockets, Docker, RTSP+ONVIF. Choosing a dedicated plate detector over generic OCR is correct. **The foundation is sound — the criticism below is refinement, not replacement.**

## 5.2 What is wrong

| # | Issue | Why it matters | Fix |
|---|---|---|---|
| 1 | **ByteTrack assigned to cross-camera tracking** | ByteTrack is intra-camera only. It contributes *nothing* to the mandatory cross-camera test case. | Repurpose to multi-frame plate voting + dedup. Cross-camera = plate identity + topology. |
| 2 | **Implicit string-equality watchlist matching** | Single biggest quality risk. `GJ01A81234 != GJ01AB1234` → missed alert on a wanted vehicle. | Position-aware normalisation + weighted fuzzy match + confidence bands. |
| 3 | **Face recognition treated as in-scope** | Appears only in Model 4's description. Legal + GPU cost. | Cut from build; keep as HLD roadmap with privacy safeguards. |
| 4 | **"OpenCV + FFmpeg" is not a concurrency strategy** | `cv2.VideoCapture` will not survive 50 concurrent mixed-codec streams. At this scale the concurrency model *is* the engineering. | FFmpeg subprocess per camera at sampled fps; OpenCV only for image ops. |
| 5 | **Kafka ranked SHOULD** | Officially named; carries two evaluation criteria; decouples the team under deadline. | Promote to MUST. |

## 5.3 What is missing entirely

Camera registry + health monitoring · security/RBAC/audit · **the mandatory 80,000-camera scalability document** · concrete vendor-adapter design · reconnection/PTS/backoff engineering · **the six submission artefacts** · the data model · a demo script · a local sandbox replica.

## 5.4 What is over-engineered

Face recognition · Model-4 VMS ambitions · Prometheus/Grafana before the core flow works · full ONVIF discovery (the sandbox is RTSP-only — design it, don't build it).

## 5.5 The one change that matters most

> **Reframe the proposal from "AI CCTV system" to "vendor-neutral federated integration layer that happens to run ANPR."**
> Same code. Radically better story. Matches four of the five official reference models.

---

# 6. ARCHITECTURE DECISION

## 6.1 Options compared

| Criterion | A: Centralised | B: Pure Edge | **C: Hybrid Edge+Central** | D: Pure Federated |
|---|---|---|---|---|
| Scalability to 80k | ✗ Fails (160 Gbps) | ✓ Excellent | ✓ Excellent | ✓ Excellent |
| Bandwidth | ✗ ~160 Gbps | ✓ Minimal | ✓ Metadata only | ✓ Minimal |
| Latency | ✗ WAN round-trip | ✓ Sub-second | ✓ Sub-second | ~ Vendor-dependent |
| GPU usage | ✗ Central farm | ✓ Distributed | ✓ Distributed + burst | ~ Depends |
| Cost | ✗ Highest | ~ Many units | ✓ Best total | ✓ Low |
| Reliability | ✗ SPOF | ✓ Survives WAN loss | ✓ Survives + aggregates | ~ Dies with vendor API |
| Vendor independence | ✗ Needs replacement | ~ | ✓ Adapters at edge | ✓ Its purpose |
| Cross-camera correlation | ✓ | ✗ **No central join** | ✓ | ✓ |
| Hackathon feasibility | ✓ Easiest | ~ Needs 2 machines | ✓ Same code, 2 profiles | ✗ No vendor APIs exist |
| Production feasibility | ✗ | ~ | ✓ Best | ~ Blocked on 26 contracts |

## 6.2 ✅ SELECTED: Architecture C — Hybrid Edge + Central, metadata-first

Formally: **Official Model 5 (Hybrid)**, built on a **Model 3 federation skeleton**, delivering **Model 2 capability**.
*Say exactly that in the presentation — it shows you read all five models and chose deliberately.*

**Why, and why not the others:**

- **Not A (Centralised / Model 4):** 80,000 × 2 Mbps = **160 Gbps sustained**, ≈1,728 TB/day ingress. Arithmetically dead. Any jury member who signs a network budget knows it. It is the trap option.
- **Not B (Pure Edge):** the mandatory test case is *cross-camera* correlation. Correlation is inherently central — pure edge has nowhere to join Ahmedabad and Palanpur.
- **Not D (Pure Federation):** the right long-term answer for 26 systems, but you cannot build 26 vendor adapters in five days and no vendor APIs exist in the sandbox. Take its *principle* (adapters, departmental autonomy, metadata exchange) without its *prerequisite*.
- **C wins** because it is the only option where the five-day demo is **architecturally identical** to the 80,000-camera system. Same container, same event schemas, same adapter interface — only deployment topology changes. That is a scalability claim you can **demonstrate**, and "Scalability & PoC Readiness" is one of seven criteria.

### Architectural thesis (one sentence)

> **Video stays local; only metadata travels; correlation happens centrally.**

## 6.3 System diagram

```
   Dept A VMS      Dept B RTSP      Dept C ONVIF      GSRTC / Municipal
   (Health)        (Police)         (Panchayat)       (existing systems)
        |               |                |                  |
        +---------------+----------------+------------------+
                                |
                  +-------------v--------------+
                  |   VENDOR ADAPTER LAYER     |  <- pluggable, one class per vendor
                  |  RTSP . ONVIF . VMS API    |
                  +-------------+--------------+
                                |  normalised CameraDescriptor + FrameSource
                  +-------------v--------------+
                  |   EDGE / REGIONAL NODE     |  <- runs near cameras; GPU here
                  |  decode -> sample -> ANPR  |
                  |  ONLY METADATA LEAVES -----+--> ~400 B + 30 KB snapshot
                  +-------------+--------------+      (not 2 Mbps of video)
                                |
                        +-------v--------+
                        |  KAFKA (KRaft) |   plate.detected . camera.status
                        +-------+--------+
                                |
        +-----------------------+------------------------+
        |                       |                        |
+-------v--------+   +----------v---------+   +----------v---------+
| NORMALISE +    |   | CROSS-CAMERA       |   | CAMERA HEALTH      |
| CONFIDENCE     |   | CORRELATOR         |   | MONITOR            |
+-------+--------+   +----------+---------+   +----------+---------+
        |                       |                        |
+-------v--------+              |                        |
| WATCHLIST      |              |                        |
| FUZZY MATCH    |              |                        |
+-------+--------+              |                        |
        |                       |                        |
+-------v-----------------------v------------------------v---------+
|        PostgreSQL + PostGIS   (sightings . routes . audit)       |
+-------+-----------------------+------------------------+---------+
        |                       |                        |
+-------v--------+   +----------v---------+   +----------v---------+
| ALERT ENGINE   |   | INVESTIGATION API  |   | HEALTH API         |
+-------+--------+   +----------+---------+   +----------+---------+
        | WebSocket             | REST                   |
+-------v-----------------------v------------------------v---------+
|              REACT POLICE DASHBOARD  +  MapLibre GIS             |
|   live video via WHEP  ---- DIRECT from source, bypasses backend |
+------------------------------------------------------------------+
```

**Two decisions encoded in this diagram that most teams will miss:**
1. The adapter layer is the **entry contract** — vendor neutrality is structural, not a slide.
2. **Video never traverses the backend.** The browser pulls WHEP directly; only metadata flows through the platform. *This is the 80,000-camera scalability argument, made visible.*

## 6.4 Scale arithmetic (put this on a slide)

**Naive centralisation (Model 4 at full scale):**
```
80,000 cameras x 2 Mbps (H.264 720p) = 160 Gbps sustained
                                     = 1,728 TB/day ingress
```

**SETU metadata-first:**
```
One ANPR event ~ 400 bytes JSON + ~30 KB JPEG snapshot
Assume 20,000 ANPR-relevant cameras x 2,000 plate events/day
   metadata  : 20,000 x 2,000 x 400 B  ~   16 GB/day
   snapshots : 20,000 x 2,000 x 30 KB  ~  1.2 TB/day
   total                                ~  1.2 TB/day
```
> **≈1,400× less WAN data — and video never leaves the department that owns it.**
> That is simultaneously the bandwidth answer *and* the data-sovereignty answer.

---

# 7. CCTV INTEGRATION STRATEGY

## 7.1 The adapter contract (put this verbatim on a slide)

```python
class CameraAdapter(Protocol):
    vendor: str
    async def discover(self) -> list[CameraDescriptor]: ...
    async def open(self, cam: CameraDescriptor) -> FrameSource: ...
    async def health(self, cam: CameraDescriptor) -> HealthStatus: ...
    def view_url(self, cam: CameraDescriptor) -> ViewURLs: ...  # WHEP/HLS for browser


@dataclass(frozen=True)
class CameraDescriptor:
    camera_id: str; vendor: str; department: str
    lat: float; lon: float
    codec: Literal["h264", "h265"]
    rtsp_url: str; whep_url: str | None; hls_url: str | None
    site_name: str; capabilities: set[str]
```

## 7.2 Build exactly three adapters

| Adapter | Purpose | Effort |
|---|---|---|
| `SentinelCatalogAdapter` | Reads `GET /api/ingest`. **This is the one the jury's test case runs through.** | 2 h |
| `GenericRtspAdapter` | Plain RTSP URL + credentials. Covers most real departmental cameras. | 1 h |
| `OnvifAdapter` | WS-Discovery + GetStreamUri via `onvif-zeep`. Build thin or leave a documented stub. **Do not let it eat a day.** | 3 h max |

## 7.3 Adding a 27th vendor without touching the core

> Write one class implementing `CameraAdapter`, register it in `ADAPTERS = {...}`, add a row to the `vendors` table. **Zero changes** to ingest, ANPR, correlation, alerting, GIS or UI.

Demonstrate this live — it takes 20 seconds and proves vendor neutrality more convincingly than any slide.

## 7.4 ⭐ Ingest engineering (the item most likely to sink the project)

**Do not use `cv2.VideoCapture` for 50 streams.** One FFmpeg subprocess per camera; let C do the decoding; Python only consumes sampled frames:

```
ffmpeg -loglevel error \
       -rtsp_transport tcp \          # MANDATORY per official guide
       -timeout 5000000 \
       -i <rtsp_url> \
       -vf fps=5,scale=1280:-2 \      # 5 fps is plenty for ANPR
       -f rawvideo -pix_fmt bgr24 -
```

Wrap in a supervisor with:
- exponential backoff 2 s → 30 s **with jitter**
- "no frame for 15 s" → mark degraded, do not crash
- timestamps anchored to server wall-clock at ingest (document this assumption; PTS-via-`showinfo` is the upgrade path)
- loop-discontinuity detection → **reset tracker state** (feeds loop; otherwise you produce nonsense tracks across the seam)

**Why 5 fps, not 25:** a vehicle is in frame 1–3 seconds → 5–15 read attempts, ample for voting. **5× compute reduction, no accuracy loss.** This is why 50 cameras fit on one consumer GPU.

**Rough GPU arithmetic (verify on your own hardware on Day 1):** 50 × 5 fps = 250 inferences/sec of YOLOv8n @640px — comfortable on an RTX 3060/4060. Plate detection + OCR run only on frames containing vehicles.
> **Your bottleneck will be H.264/H.265 decode, not inference. Measure it first.**

---

# 8. AI / COMPUTER VISION

## 8.1 Component decisions

| Component | Needed? | Rationale |
|---|---|---|
| Vehicle detection | ✅ YES | Restricts plate search region; enables colour/type attributes |
| Plate detection | ✅ YES | Core |
| OCR | ✅ YES | Core |
| Multi-object tracking (ByteTrack) | ✅ SHOULD | Multi-frame voting + dedup. Halves OCR error for ~2 h work |
| Person detection | ❌ NO | Not in the test case |
| Face recognition | ❌ NO | Model 4 only; DPDP risk; GPU cost |
| Vehicle Re-ID | ❌ NO | Plate is the official tracing key |
| Colour/type attributes | ~ NICE | Cheap corroboration; "additional analytics" bonus |

## 8.2 The pipeline

```
RTSP frame (sampled 5 fps, wall-clock anchored)
        |
Vehicle Detection  -- YOLOv8n/s, conf >= 0.4  --> [colour, type]  (optional)
        |
Plate Detection    -- plate-specific YOLO on the vehicle crop, conf >= 0.35
        |
Plate Crop -> deskew (minAreaRect) -> upscale -> CLAHE contrast
        |
OCR -- PaddleOCR RECOGNITION ONLY (skip its detector; you already have the box)
        |
Position-aware Normalisation  -- Indian plate grammar + confusion table
        |
ByteTrack multi-frame vote  -- weighted per-character majority across the track
        |
Composite Confidence Score (explainable, 0-100)
        |
Watchlist Fuzzy Match
        |
sighting event -> Kafka
```

**Two-stage (vehicle → plate) rather than plate-direct** because the vehicle crop yields a higher-resolution plate region, gives colour/type free, and cuts false plate detections on signage dramatically.

---

# 9. ⭐ OCR NORMALISATION & FALSE-POSITIVE HANDLING

> `ocr_result == watchlist_plate` is unacceptable. This section is **differentiator #1**.

## 9.1 Position-aware normalisation (the key trick)

Indian registrations follow a grammar:
```
[2 alpha state][1-2 digit RTO][0-3 alpha series][4 digit number]
GJ 01 AB 1234
```

Once you know a character's **position**, you know whether it must be a letter or a digit. Correction becomes **deterministic, not a guess**.

| Confusion pair | When position demands ALPHA | When position demands DIGIT |
|---|---|---|
| `0` ↔ `O`/`D`/`Q` | `0` → `O` | `O`,`D`,`Q` → `0` |
| `1` ↔ `I`/`L` | `1` → `I` | `I`,`L` → `1` |
| `8` ↔ `B` | `8` → `B` | `B` → `8` |
| `5` ↔ `S` | `5` → `S` | `S` → `5` |
| `2` ↔ `Z` | `2` → `Z` | `Z` → `2` |
| `6` ↔ `G` | `6` → `G` | `G` → `6` |
| `4` ↔ `A` | `4` → `A` | `A` → `4` |
| `7` ↔ `T` | `7` → `T` | `T` → `7` |

**Worked example:** OCR reads `GJ01A81234`. Position 5 must be alphabetic. `8`→`B` is a known confusion at low char-confidence (0.62). Result: **`GJ01AB1234`**, correction logged with reason.

**Additionally validate:**
- **State code** against the 36-entry list (`GJ`, `MH`, `RJ`, `DL`, …) — `GG01AB1234` is provably wrong
- **RTO district** against Gujarat's valid range (GJ-01 … GJ-39)

**Refinement:** weight correction cost by OCR character confidence — correcting a *high*-confidence character should be expensive; correcting a *low*-confidence one should be cheap.

## 9.2 Multi-frame voting

Within one ByteTrack track, collect every OCR read. Take the **per-character weighted majority** (weight by that character's OCR confidence). Record:
```
frame_agreement = winning_votes / total_votes
```
Two frames agreeing is weak; 7 of 8 is strong. **This alone typically halves plate error rates** and costs almost nothing.

## 9.3 Weighted fuzzy matching

Levenshtein with **non-uniform substitution costs**:

```python
def sub_cost(a: str, b: str) -> float:
    if a == b:                       return 0.0
    if (a, b) in KNOWN_CONFUSIONS:   return 0.3   # 8<->B is nearly free
    if a.isdigit() == b.isdigit():   return 0.7   # same class, plausible
    return 1.0                                     # implausible

# alert if weighted_distance <= 1.0
# review-queue if <= 1.8
# discard above
```

> **Never alert on a distance-2 match of two implausible substitutions.** That is where false positives come from.

## 9.4 The explainable composite score

```
match_score = 100 x ( 0.20 * plate_det_conf
                    + 0.25 * ocr_char_conf
                    + 0.15 * frame_agreement
                    + 0.15 * format_validity      # state + RTO + pattern legal
                    + 0.15 * string_similarity    # 1 - weighted_dist/len
                    + 0.10 * topology_plausibility )
```

| Band | Range | Action |
|---|---|---|
| **CONFIRMED** | ≥ 85 | Auto-alert |
| **PROBABLE** | 65–84 | Alert, marked for verification |
| **POSSIBLE** | 45–64 | Review queue, **no alert** |
| Discard | < 45 | Dropped |

## 9.5 ⭐ The differentiator is SHOWING it

Every alert card expands to:

```
GJ01AB1234 . CONFIRMED . 91/100
|- Plate detection      0.86   ########__
|- OCR character conf   0.89   #########_
|- Frame agreement      5/7    #######___
|- Format validity      VALID  GJ=Gujarat, RTO 01=Ahmedabad  OK
|- String match         exact after 1 normalisation (pos 5: 8->B)
+- Route plausibility   111 km/h from CAM-014  OK plausible
```

> An officer can see **why** the system is confident and defend the alert in court.
> A black-box `0.91` is not evidence. This is.
> It also directly answers the "Video Analytics Output" criterion, which asks about **quality**, not mere presence.

## 9.6 Deduplication (do not skip)

One vehicle passing one camera generates many frames. Emit **one sighting per (plate, camera, 60-second window)**, keeping the highest-confidence frame as evidence. Enforce it with a **database unique index**, not just application logic.
> Without this, your alert list drowns and judges *will* notice 40 identical alerts.

---

# 10. CROSS-CAMERA TRACKING

## 10.1 Is ANPR alone sufficient? **Yes — and it is the officially correct answer.**

The test case says *"identify and trace a government-provided vehicle registration"*. **The tracing key IS the plate.** A plate is a globally unique identifier — which is exactly what makes cross-camera correlation tractable without Re-ID.

| Technique | Required for MVP? | Verdict |
|---|---|---|
| ANPR plate identity | ✅ Yes | Primary correlation key — sufficient |
| Camera topology (locations + distances) | ✅ Yes | Needed for GIS *and* plausibility; cheap via PostGIS |
| Time/distance constraints | ✅ Yes | ~15 lines of code, large credibility payoff |
| Colour/type attributes | ~ Bonus | Weak corroboration when OCR is uncertain |
| Deep Vehicle Re-ID | ❌ No | Research-grade; only pays off for unplated vehicles |

## 10.2 The correlation algorithm

```python
sightings = query("""
    SELECT s.*, c.name, c.department, c.geom
    FROM sightings s JOIN cameras c USING (camera_id)
    WHERE s.plate_normalized = %s AND s.confidence >= 65
    ORDER BY s.detected_at
""", (plate,))

for prev, curr in pairwise(sightings):
    km    = st_distance_km(prev.geom, curr.geom)      # PostGIS geography
    hours = (curr.detected_at - prev.detected_at).total_seconds() / 3600
    speed = km / hours if hours > 0 else float("inf")
    curr.plausibility = ("PLAUSIBLE"   if speed <= 120 else
                         "FAST"        if speed <= 160 else
                         "IMPLAUSIBLE")   # -> OCR error, cloned plate, or clock skew
```

> ⭐ **The `IMPLAUSIBLE` branch is quietly one of the most police-valuable features in the system.** A plate appearing in two places faster than physics allows is either a misread **or a cloned plate** — a real, current crime pattern. It costs almost nothing and no other team will have it.

## 10.3 The output the jury must see

```
GJ01AB1234 - 4 sightings - 02 Sep 2026
+-------+--------------+---------+-----------+------+------------+
| Time  | Location     | Camera  | Dept      | Conf | Segment    |
+-------+--------------+---------+-----------+------+------------+
| 10:15 | Ahmedabad    | CAM-014 | Municipal |  91  | -          |
| 10:27 | Gandhinagar  | CAM-031 | GSRTC     |  88  | 111 km/h OK|
| 10:41 | Mehsana      | CAM-047 | Panchayat |  76  |  94 km/h OK|
| 11:35 | Palanpur     | CAM-009 | Police    |  84  |  98 km/h OK|
+-------+--------------+---------+-----------+------+------------+
Route: 214 km NW - heading toward Rajasthan border
>>> 4 departments, 4 vendors, 4 systems that have never exchanged data <<<
```

That last line ties the demo back to the actual problem statement. **Make sure the UI renders it.**

---

# 11. EVENT-DRIVEN ARCHITECTURE

## 11.1 Honest assessment

For 50 cameras on one machine you **do not technically need Kafka.** Direct function calls would work.

**Use it anyway — for three specific reasons, not because it sounds scalable:**

1. **Kafka is explicitly named in the official technology list.** Its absence would be conspicuous.
2. **"Solution Architecture" and "Scalability & PoC Readiness" are 2 of 7 criteria.** The event log makes the edge/central split *real* rather than notional.
3. **It decouples the team.** Agree the JSON schemas on Day 0 and nobody blocks anybody. **With five days, that is worth more than the runtime benefit.**

## 11.2 The decision

> **Apache Kafka in KRaft mode, single broker, one Docker Compose service.** No ZooKeeper. Apache 2.0. Client: `aiokafka`. Setup ≈ 45 minutes.

| Rejected | Why |
|---|---|
| **Redpanda** | Community Edition is **BSL**, not OSI open source — needless risk against a stated open-source mandate |
| **RabbitMQ** | A queue, not a replayable log. Replay is what makes the event store credible |
| **Redis Streams** | Genuinely sufficient — **keep as the documented Day-2 fallback** |

## 11.3 Topics

| Topic | Producer | Partition key | Payload |
|---|---|---|---|
| `camera.status` | Ingest supervisor | `camera_id` | state, last_frame_age, fps, reconnects |
| `vehicle.detected` | Edge ANPR | `camera_id` | bbox, class, colour, type, conf, ts |
| `plate.detected` | Edge ANPR | `camera_id` | raw + normalised plate, char confs, snapshot ref |
| `vehicle.sighting` | Normaliser | **`plate`** | plate, camera, ts, confidence, snapshot |
| `watchlist.match` | Matcher | **`plate`** | plate, watchlist_id, score, breakdown |
| `alert.created` | Alert engine | `alert_id` | alert record for WS fan-out |
| `tracking.updated` | Correlator | **`plate`** | new route segment, plausibility |

> ⭐ **Partition ingest topics by `camera_id`, correlation topics by `plate`.** Keying by plate guarantees all sightings of one vehicle land on one partition **in order** — exactly what correlation needs, and the reason this scales horizontally to 80,000 cameras.
> *Say that sentence in the architecture review. It shows you understand **why** Kafka, not just **that** Kafka.*

**Hard rule: never put video frames or images on Kafka.** Snapshots go to disk/object storage; events carry a reference.

**Circuit breaker:** if Kafka is not stable by end of Day 2, switch to Redis Streams (near-identical semantics) and note it in the HLD. **Never let the message bus threaten the mandatory test case.**

---

# 12. DATABASE

## 12.1 Decision: PostgreSQL 16 + PostGIS + pg_trgm, plus Redis/Valkey. Two data services. That is all.

| Choice | Rationale |
|---|---|
| **PostGIS** | Officially named. `ST_Distance`, `ST_MakeLine`, `ST_DWithin` do the real work |
| **pg_trgm** | GIN trigram index on `plate_normalized` → fast fuzzy search. **Replaces Elasticsearch** |
| **Redis 7.2 / Valkey** | Live camera state, dedup TTL keys, WS pub/sub fan-out. ⚠ Redis 7.4+ is RSALv2/SSPL — **use 7.2 (BSD) or Valkey (BSD, Linux Foundation)** to stay unambiguously open source |
| ❌ Timescale/Influx | PostgreSQL + BRIN on `detected_at` is fine at this scale |
| ❌ MongoDB | Relational integrity matters for evidence |
| ❌ Neo4j | Overkill |

## 12.2 Schema

```sql
CREATE EXTENSION postgis;  CREATE EXTENSION pg_trgm;

CREATE TABLE vendors (
  id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL,
  adapter_class TEXT NOT NULL, config JSONB DEFAULT '{}');

CREATE TABLE departments (        -- Health, Police, GSRTC, Panchayat, Municipal
  id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL, contact TEXT);

CREATE TABLE users (
  id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT CHECK (role IN ('VIEWER','INVESTIGATOR','ADMIN')),
  department_id INT REFERENCES departments(id));

CREATE TABLE cameras (
  camera_id     TEXT PRIMARY KEY,
  vendor_id     INT REFERENCES vendors(id),
  department_id INT REFERENCES departments(id),
  site_name     TEXT NOT NULL,
  geom          geography(Point,4326) NOT NULL,
  codec         TEXT, rtsp_url TEXT, whep_url TEXT, hls_url TEXT,
  status        TEXT DEFAULT 'unknown',        -- online|offline|degraded
  last_frame_at TIMESTAMPTZ, reconnects INT DEFAULT 0,
  observed_fps  REAL,
  geom_source   TEXT DEFAULT 'catalogue');     -- honesty flag: catalogue|assigned
CREATE INDEX ON cameras USING GIST (geom);

CREATE TABLE watchlist (
  id SERIAL PRIMARY KEY,
  plate TEXT NOT NULL, plate_normalized TEXT NOT NULL,
  reason TEXT, case_ref TEXT,
  priority TEXT CHECK (priority IN ('LOW','MEDIUM','HIGH','CRITICAL')),
  active BOOLEAN DEFAULT TRUE,
  created_by INT REFERENCES users(id), created_at TIMESTAMPTZ DEFAULT now());
CREATE INDEX ON watchlist (plate_normalized) WHERE active;

CREATE TABLE sightings (
  id BIGSERIAL PRIMARY KEY,
  plate_raw        TEXT NOT NULL,
  plate_normalized TEXT NOT NULL,
  camera_id        TEXT REFERENCES cameras(camera_id),
  detected_at      TIMESTAMPTZ NOT NULL,
  confidence       SMALLINT NOT NULL,
  score_breakdown  JSONB NOT NULL,             -- explainability, persisted
  snapshot_path    TEXT, snapshot_sha256 TEXT, -- evidence integrity
  vehicle_type     TEXT, vehicle_color TEXT,
  frames_voted     SMALLINT, frame_agreement REAL);
CREATE INDEX ON sightings USING GIN (plate_normalized gin_trgm_ops);
CREATE INDEX ON sightings (plate_normalized, detected_at DESC);
CREATE INDEX ON sightings USING BRIN (detected_at);
CREATE UNIQUE INDEX ON sightings                     -- dedup guard, enforced in DB
  (plate_normalized, camera_id, date_trunc('minute', detected_at));

CREATE TABLE alerts (
  id BIGSERIAL PRIMARY KEY,
  sighting_id BIGINT REFERENCES sightings(id),
  watchlist_id INT REFERENCES watchlist(id),
  match_score SMALLINT NOT NULL,
  band TEXT NOT NULL,                          -- CONFIRMED|PROBABLE|POSSIBLE
  status TEXT DEFAULT 'NEW',                   -- NEW|ACKED|RESOLVED|FALSE_POSITIVE
  acked_by INT REFERENCES users(id), acked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now());

CREATE TABLE audit_log (                       -- append-only
  id BIGSERIAL PRIMARY KEY, user_id INT, action TEXT NOT NULL,
  entity TEXT, entity_id TEXT, detail JSONB,
  ip INET, at TIMESTAMPTZ DEFAULT now());
```

**Routes are computed, not stored** — `ST_MakeLine` over ordered sightings at query time.

**Two small touches that impress a technical jury:** `geom_source` (honestly label coordinates assigned for demonstration) and `snapshot_sha256` + append-only `audit_log` (evidence-integrity story for two columns).

---

# 13. GIS

**Required?** Yes — Guide Step 4 says "visualising on GIS", Model 1 is entirely a GIS registry model, PostGIS is officially named.

## 13.1 Decision

| Option | Verdict |
|---|---|
| **MapLibre GL JS** | ✅ **SELECTED** — BSD, vector tiles, smooth over a 1,000 km extent, GPU-rendered, handles thousands of markers as layers |
| Leaflet | Adequate but raster-only, visibly less polished, clustering degrades |
| Mapbox GL JS | ❌ Proprietary + API key — **violates the open-source mandate** |
| OpenLayers | Powerful, steeper API, no advantage here |

**Stack:** MapLibre GL JS + OpenStreetMap tiles + PostGIS for all spatial queries. Serve GeoJSON from FastAPI. Render cameras as a **symbol/circle layer**, not DOM markers, so 50 — or 5,000 — stay smooth.

## 13.2 Features

Camera locations by status/department · sighting pins · ordered route polyline with direction arrows and per-segment speed · first/last detection emphasised · alert flash on the live map · time slider for historical movement · `ST_DWithin` nearby-camera query ("where do we look next?") · **timeline ↔ map hover sync**.

## 13.3 ⚠ Offline insurance

i-Hub venue Wi-Fi may be unreliable. **Pre-cache Gujarat tiles at zoom 6–12 locally** (or bundle a small `.pmtiles`). A demo whose map fails to load loses the room instantly. **30-minute insurance policy — take it.**

---

# 14. POLICE DASHBOARD

Design principle: **every screen answers exactly one question.** Seven screens, each justified by an official requirement or named bonus. Resist an eighth.

| # | Screen | Question it answers | Key content |
|---|---|---|---|
| 1 | **Command Center** | "Is everything OK right now?" | Counters (cameras online/total, alerts today, sightings today) · live alert feed · MapLibre map pulsing on detections · event ticker |
| 2 | **CCTV Monitoring** | "Show me the cameras." | 3×3/4×4 grid, each tile a **WHEP `<video>` connected direct to source** · filter by department/vendor · overlay: ID, dept, vendor, codec, live fps, status dot |
| 3 | **Alert Center** | "What needs my attention?" | Snapshot + plate crop · camera + location · timestamp · score with **expandable breakdown** · watchlist reason/case ref · actions: Acknowledge / **Mark False Positive** / Investigate → |
| 4 | **Vehicle Investigation** ⭐ | "Where has this vehicle been?" | Fuzzy-tolerant search · header (first/last seen, distance, departments) · **split view**: timeline left, MapLibre route right, hover-synced · Export PDF |
| 5 | **GIS View** | "Show me everything spatially." | Full-screen map, time slider, department/vendor layers, coverage heat |
| 6 | **Watchlist** | "Manage wanted vehicles." | Table + add/edit/deactivate, priority, reason, case ref, added-by/at. Admin+Investigator only |
| 7 | **Camera Health / Admin** | "Which cameras are misbehaving?" | Status, last-frame age, observed vs expected fps, reconnect count, codec, vendor, dept · sort by most reconnects · Users & roles |

> **Demo tip (screen 2):** filter Department → GSRTC, then → Municipal, and let tiles swap. In four seconds, wordlessly, you have shown multi-department integration in one pane. That is the whole problem statement, visually.

> **Why "Mark False Positive" matters:** it shows the jury you know operators must be able to correct the system. Maturity signal, 20 minutes of work.

---

# 15. SECURITY & PRIVACY

## 15.1 MVP — build it (~10 hours total)

| Control | Implementation | Cost |
|---|---|---|
| Authentication | JWT (short-lived access + refresh), `argon2` hashing | 2 h |
| RBAC | VIEWER (monitor+alerts) · INVESTIGATOR (+search, export) · ADMIN (+watchlist, users, cameras). Enforce via FastAPI dependency | 2 h |
| Audit logging | Append-only `audit_log` on login, search, watchlist change, alert action, export | 2 h |
| Camera credentials | Env vars / Docker secrets. **Never in the repo, never returned by any API** | 30 m |
| API security | Pydantic validation, rate limiting on auth+search, CORS allowlist, parameterised SQL only | 1 h |
| Evidence integrity | SHA-256 of every snapshot stored with the sighting row | 30 m |
| Least privilege | Non-root containers; runtime DB user without DDL rights | 30 m |
| Transport | HTTPS via Caddy/nginx + Let's Encrypt on the hosted URL | 1 h |

> A **police** system shipped without auth undercuts every credibility claim you make elsewhere. And the hosted URL **with credentials** is a mandatory deliverable — you need auth regardless.

## 15.2 Production — HLD only, do not build

mTLS edge↔central · secrets in Vault/HSM · KMS envelope encryption at rest · **hash-chained evidence ledger** (each sighting hash includes the previous — tamper-evident chain of custody, court-admissible) · SIEM integration · departmental camera VLAN segmentation · **DPDP Act 2023 compliance** (purpose limitation, defined retention — e.g. non-hit ANPR metadata purged at 90 days, hits retained per case — data-principal rights, DPIA before any biometric expansion) · quarterly access reviews · pen-testing · fleet certificate rotation.

## 15.3 ⭐ Say the privacy part out loud

A mass-surveillance platform proposed **without** a privacy paragraph reads as naive to senior police leadership, who carry that liability. **One honest slide** — retention limits, purpose limitation, RBAC, audit, and *why we deliberately did not build face recognition* — converts a perceived weakness into a maturity signal.

---

# 16. SCALABILITY: HACKATHON → PRODUCTION

| Layer | Hackathon (50 cameras) | Production (80,000 cameras) |
|---|---|---|
| Ingest | 1 container, 50 FFmpeg subprocesses | ~5,000 edge nodes, ~16 cameras each; **adapter layer unchanged** |
| AI | 1 consumer GPU, 5 fps sampling | Jetson Orin NX / T4 per edge node; **same container image** |
| Events | Kafka 1 broker, 3 partitions | Kafka cluster partitioned by `camera_id`/`plate`; regional clusters → central mirror |
| DB | 1 PostgreSQL | Primary + read replicas; `sightings` partitioned monthly; regional shards |
| Storage | Local disk snapshots | MinIO/S3 with lifecycle: cold at 30 d, purge non-hits at 90 d |
| Cache | 1 Redis | Redis Cluster |
| API | 1 FastAPI | Horizontally scaled behind LB (stateless + JWT) |
| Fault tolerance | Auto-reconnect, restart policies | Edge buffers metadata locally during WAN loss, replays on reconnect; regional failover; K8s |
| Health | Health monitor service | Same service sharded per region; Prometheus + Alertmanager |

## 16.1 The strongest sentence for the scalability slide

> **"The container we run on 50 cameras is byte-identical to the one we would run on an edge node covering 16 cameras in Kutch. Scaling is a deployment-topology change, not a rewrite."**

You can *demonstrate* this by running one edge container on a teammate's laptop during the demo.

## 16.2 Rollout plan (Guide Step 6 asks for this — one slide)

| Phase | Scope | Value delivered |
|---|---|---|
| A | Registry + GIS onboarding of all 26 systems, no analytics | Model 1 value in weeks |
| B | ANPR edge nodes at ~500 high-value traffic corridors | Core intelligence |
| C | Statewide expansion district by district | Full coverage |
| D | Additional analytics | Incremental |

Plus DR: regional Kafka mirroring, nightly encrypted PG backups, documented RTO/RPO.

---

# 17. FINAL TECHNOLOGY STACK

| Layer | Technology | Purpose | Why This Choice | MVP Priority |
|---|---|---|---|---|
| Frontend | React + TypeScript + Vite | Police dashboard | Officially named; fastest path to a polished real-time UI | **MUST** |
| UI | Tailwind + shadcn/ui | Interface | Control-room UI in hours; MIT; copy-in, no runtime lock-in | **MUST** |
| Backend | Python + FastAPI | APIs, WebSockets, orchestration | Officially named; async + native AI ecosystem in one language | **MUST** |
| AI | PyTorch + YOLOv8/v11 | Vehicle & plate detection | Officially named; best pretrained plate models (⚠ AGPL — note in HLD) | **MUST** |
| Video ingest | **FFmpeg** (subprocess/camera) | Decode, sample, deliver frames | Only approach that survives 50 concurrent mixed-codec streams | **MUST** |
| Image ops | OpenCV | Crop, deskew, CLAHE | Right tool for image ops — **not** for 50-stream capture | **MUST** |
| ANPR/OCR | YOLO plate detector + PaddleOCR (rec-only) | Plate reading | Apache-2.0; plate-specific pipeline beats generic OCR | **MUST** |
| Normalisation | Custom position-aware Indian-plate grammar | OCR error correction | **The core accuracy differentiator. No library does this.** | **MUST** |
| Tracking | ByteTrack | Multi-frame voting + dedup | Halves OCR error for ~2 h work (**not** cross-camera) | **SHOULD** |
| Correlation | Custom: plate identity + PostGIS topology | Cross-camera route reconstruction | Plate is the official tracing key; Re-ID unnecessary | **MUST** |
| Database | PostgreSQL 16 | Cameras, sightings, watchlist, alerts, audit | Officially named; relational integrity for evidence | **MUST** |
| GIS DB | PostGIS | Distance, routes, nearby-camera queries | Officially named; `ST_MakeLine`/`ST_DWithin` | **MUST** |
| Search | pg_trgm (GIN) | Fuzzy plate search | **Replaces Elasticsearch** — one less service to fail | **MUST** |
| Cache | Redis 7.2 / Valkey | Live state, dedup TTL, WS pub/sub | Low latency; BSD versions keep open-source compliance | **SHOULD** |
| Events | **Apache Kafka (KRaft, 1 broker)** | Event spine | Officially named; makes edge/central real; decouples the team | **MUST** |
| GIS UI | MapLibre GL JS + OSM | Maps, routes, camera layers | BSD (Mapbox is proprietary); smooth at 1,000 km extent | **MUST** |
| Real-time | WebSockets | Live alerts | Bidirectional, native to FastAPI, instant | **MUST** |
| CCTV | RTSP-over-TCP + ONVIF adapter | Camera integration | TCP explicitly mandated by the official guide | **MUST** |
| Live video | **WebRTC / WHEP direct to browser** | Camera viewing | Zero backend video bandwidth — the scalability story made visible | **MUST** |
| Security | JWT + RBAC + audit log | Access control | Hosted URL w/ credentials is mandatory; security is a named bonus | **MUST** |
| Deployment | Docker + Docker Compose | Reproducible deploy | One command; K8s is production-only | **MUST** |
| Dev sandbox | **MediaMTX + ffmpeg loop** | Local replica of the govt sandbox | Build against real conditions from day one | **MUST** (dev) |
| Monitoring | Prometheus + Grafana | Stream/GPU health | Bonus only; in-app health page covers it cheaply | **OPTIONAL** |

## 17.1 Changes from the pasted baseline

| Change | Reason |
|---|---|
| FFmpeg promoted over OpenCV for capture | `cv2.VideoCapture` will not survive 50 concurrent mixed-codec streams |
| Kafka SHOULD → **MUST** | Officially named; carries 2 evaluation criteria; decouples the team |
| ByteTrack repurposed + demoted to SHOULD | It cannot do cross-camera; it *can* halve OCR error via voting |
| Elasticsearch **dropped** → `pg_trgm` | A search cluster for one text column is unaffordable complexity |
| WHEP-direct made explicit | Zero backend video bandwidth = the scalability argument |
| Plate-normalisation engine **added as MUST** | The primary differentiator |
| Security **added as MUST** | Mandatory deliverable requires it |
| Face recognition + Re-ID **removed** | Not in the test case |

---

# 18. ⭐ THE HIGHEST-LEVERAGE ACTION AVAILABLE

The sandbox endpoints — RTSP on **8554**, WebRTC **WHEP on 8889**, HLS at `/live/stream/<id>/index.m3u8` — are the **default port and path signature of [MediaMTX](https://github.com/bluenviron/mediamtx)** (open source). The organisers describe *"recorded CCTV footage converted into live streams via Python-based middleware."* That is almost certainly MediaMTX + an ffmpeg loop publisher.

### Replicate the sandbox locally, before credentials arrive

```bash
# 1. Run MediaMTX
docker run --rm -it --network=host bluenviron/mediamtx:latest

# 2. Publish N looping streams that mimic the real thing
for i in $(seq 1 50); do
  ffmpeg -re -stream_loop -1 -i "clips/clip_$((i % 8)).mp4" \
    -c:v $( [ $((i % 3)) -eq 0 ] && echo libx265 || echo libx264 ) \
    -r $((15 + i % 15)) \
    -s $( [ $((i % 2)) -eq 0 ] && echo 1280x720 || echo 640x480 ) \
    -f rtsp -rtsp_transport tcp rtsp://localhost:8554/stream/cam$i &
done
```

Deliberately vary codec, fps and resolution — exactly the heterogeneity the official resources page warns about.

**Payoff:** every official constraint (TCP transport, timing, loop discontinuities, backoff, mixed codecs) can be engineered and *tested* before you ever touch the government host. When credentials arrive you **change one environment variable**.

> Teams that skip this will spend their first sandbox day debugging what you already fixed.

---

# 19. TOP 3 DIFFERENTIATORS

Assume every competitor ships CCTV + YOLO + ANPR + dashboard. That is table stakes.

### 1. Explainable, confidence-scored ANPR matching
Position-aware Indian-plate grammar correction + weighted-Levenshtein fuzzy matching + multi-frame voting, with **the full score breakdown visible on every alert card**.
**Attacks:** the #1 reason real ANPR deployments fail — operators drowning in false positives, unable to justify a stop.
**Demo moment:** type the *misread* plate `GJ01A81234` into search; the system still finds the vehicle; expand the alert to show exactly which character was corrected and why.
**Maps to:** Video Analytics Output. *No other team will show their working.*

### 2. Metadata-first federated architecture with a live-pluggable vendor adapter layer
Video never crosses the WAN; only ~400-byte events do. Add a 27th vendor by writing one class.
**Demo moment:** register a new adapter mid-presentation, watch cameras populate the map, then show **160 Gbps vs 1.2 TB/day (~1,400×)**.
**Maps to:** Solution Architecture + Scalability & PoC Readiness + the edge-processing bonus.
*This speaks directly to the 26-island problem the police actually own.*

### 3. Topology-aware cross-camera correlation with cloned-plate / impossible-travel detection
Every route segment validated against physics. A plate seen 200 km apart 8 minutes later is flagged **IMPLAUSIBLE — possible cloned plate or misread**.
**Demo moment:** inject one such sighting; let the system catch itself.
**Maps to:** advanced cross-camera tracking bonus + auditability.
*Every team will draw a route. You will be the only one whose system knows when its own route is wrong — and cloned plates are a crime pattern senior officers recognise instantly.*

---

# 20. DEMO SCRIPT (target 4 min, hard ceiling 5)

The own-feed video is capped at 2–3 minutes — script to the second and compress.

| # | Time | Action | What judges must see | Line to say |
|---|---|---|---|---|
| 1 | 0:00 | Open Command Center | 50 cameras on the Gujarat map, colour-coded by department | "Fifty cameras. Five departments. One screen. Today these are 26 systems that cannot talk to each other." |
| 2 | 0:20 | Filter by department | Grid swaps GSRTC → Municipal → Health | "Different vendors, different codecs, different networks — one adapter layer." |
| 3 | 0:35 | Live WHEP tiles | Sub-second video, fps + codec badges showing mixed H.264/H.265 | "Video goes straight from source to browser. Our backend carries zero video bytes — that's how this reaches 80,000 cameras." |
| 4 | 0:50 | Camera Health | Online/degraded/offline, reconnect counts, fps drift | "We monitor the fleet, not just the footage." |
| 5 | 1:05 | Add the jury's plate to the watchlist | Live insert, priority HIGH, audit entry | "You give us the registration. We've never seen it before." |
| 6 | 1:20 | Detection fires | Live bounding boxes, plate crop, alert slides in | *(silence — let it land, 3 seconds)* |
| 7 | 1:35 | **Expand confidence breakdown** | Six components; the `8→B` correction shown with its reason | "It read an 8. Position five must be a letter. We corrected it — and here's why, in writing, for the court." |
| 8 | 1:55 | Second camera, different department | Second alert; timeline count → 2 | "That was Municipal. This is GSRTC. Two systems that have never exchanged data." |
| 9 | 2:10 | Click **Investigate** | Timeline + route render together | — |
| 10 | 2:25 | Route on GIS | 4 pins, polyline, direction arrows, per-segment speeds | "Four sightings. Four departments. Four vendors. 214 km. Reconstructed in under a second." |
| 11 | 2:45 | Hover the timeline | Map pins pulse in sync; snapshots enlarge | "Every claim backed by a timestamped frame with a SHA-256 hash." |
| 12 | 3:00 | **Search the misread plate** `GJ01A81234` | System still returns the correct vehicle | "An officer types what they saw on a grainy monitor. We still find it." |
| 13 | 3:15 | **Inject the impossible sighting** | Segment flags red: IMPLAUSIBLE — possible cloned plate | "The system just told us it might be wrong. That's the difference between an alert and evidence." |
| 14 | 3:35 | Add a new vendor adapter live | New cameras appear on the map | "One class. No core changes. That's the 27th department onboarded." |
| 15 | 3:50 | Scalability slide | 160 Gbps vs 1.2 TB/day; identical container on an edge node | "The container running here is the same one that runs on an edge node in Kutch. Scaling is deployment, not a rewrite." |

> **Rehearse the failure paths.** Pre-record a backup video of the full flow. If venue Wi-Fi dies, narrate over the recording without breaking stride — and say so honestly. **Judges forgive network failures; they do not forgive fumbling.**

---

# 21. TEAM PLAN — 5 DAYS (2–7 SEPTEMBER)

Assume 4–6 people. **Team size is not stated on the portal — confirm with the helpdesk.**

## 21.1 Roles

| Role | Owns |
|---|---|
| **A — Ingest & CCTV Integration** | FFmpeg supervisor, adapter layer, `/api/ingest`, reconnection, health. **The critical path.** |
| **B — AI/CV** | YOLO detection, PaddleOCR, normalisation engine, ByteTrack voting, confidence scoring |
| **C — Backend & Data** | FastAPI, PostgreSQL/PostGIS schema, Kafka, matching, correlation, alerts, WebSockets, auth/RBAC |
| **D — Frontend & GIS** | React dashboard, MapLibre, WHEP tiles, alert UI, investigation view |
| **E — DevOps, Docs & Demo** | Docker Compose, hosted deploy, **the six deliverables**, demo script, videos |

> With four people, E's duties split across A–D — **but someone must own the deliverables from Day 0.** Perfect software with a missing HLD scores zero on "Submission Completeness", one of seven criteria.

## 21.2 Sequence — working core flow before every feature

### Day 0 — TODAY, 2 Sep (half day, everyone)
- ⚠ **Register on the portal**
- ⚠ **Email `sentinel.hackathon@gujarat.gov.in`**: sandbox credentials/host, team size limit, is Phase 1 remote, GPU availability at i-Hub
- **Stand up MediaMTX + 50 looping mixed-codec streams** (§18) — everything else depends on this
- Repo, Docker Compose skeleton, **agree the event JSON schemas** (this is what unblocks parallel work)

### Day 1 — 3 Sep · Vertical slice
- A: FFmpeg supervisor, 10 streams stable, TCP + backoff
- B: YOLO + PaddleOCR on saved frames, plate out
- C: schema + FastAPI skeleton + Kafka up
- D: React shell + MapLibre with camera pins
- E: Compose runs end-to-end
- **GATE: one camera → one plate → one database row.** *If this fails tonight, cut Kafka tomorrow.*

### Day 2 — 4 Sep · Core flow
- A: **all 50 streams stable** (the hardest day)
- B: normalisation engine + confidence scoring
- C: watchlist + fuzzy matching + alerts + WebSockets
- D: alert UI + live WHEP tiles
- E: **start the HLD and PPT — do not defer these**
- **GATE: plate → alert visible in browser in under 3 s.**

### Day 3 — 5 Sep · The test case
- A: health monitoring + adapter abstraction
- B: ByteTrack voting + dedup
- C: cross-camera correlation + plausibility + auth/RBAC + audit
- D: investigation view + route rendering
- E: deploy to the hosted URL with credentials
- **GATE: search a plate → full timeline + route on the map. THIS IS THE OFFICIAL TEST CASE. It must pass tonight.**

### Day 4 — 6 Sep · Polish, harden, record
- Morning: bug-fix only. **Feature freeze at noon.**
- A/B: accuracy tuning on real sandbox feeds if credentials arrived
- C/D: UX polish, empty states, loading states
- **ALL: record the own-feed video (2–3 min) and the government-feed demo + output report**
- E: finish PPT + HLD + scalability numbers
- **GATE: everything recorded. Never leave recording to deadline day.**

### Day 5 — 7 Sep · Submit
- Final run-through; verify **every** link works from an incognito window with the supplied credentials
- **Submit by mid-afternoon. Do not submit in the last hour — portals fail under load.**

### Days 6–8 — 8–10 Sep (if shortlisted)
Rehearse the live demo · pre-cache map tiles · build the offline fallback · prepare answers on cost, DR, privacy and rollout.

## 21.3 The cut-order rule

**If behind, cut in this order:**
Prometheus/Grafana → ONVIF → vehicle attributes → Kafka (fall back to Redis Streams) → camera health UI → ByteTrack voting

**NEVER cut:** ingest · ANPR · watchlist matching · alerts · timeline · GIS route · auth · the six deliverables

---

# 22. RISK REGISTER

| Risk | Severity | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **50 concurrent streams overwhelm decode** | 🔴 Critical | **High** | Test case fails outright | FFmpeg subprocess/camera at 5 fps; benchmark Day 1 on MediaMTX; hardware decode if available; degrade to 25 cameras before failing entirely |
| **Deliverables unfinished (5 days)** | 🔴 Critical | **High** | Zero on Submission Completeness | Owner assigned Day 0; HLD/PPT started Day 2; videos recorded Day 4 |
| **Sandbox credentials arrive late** | 🔴 Critical | Medium | No government-feed demo | MediaMTX replica → one env-var change; chase helpdesk today |
| OCR errors on Indian plates | 🟠 High | **High** | Missed/false alerts | Position-aware normalisation + multi-frame voting + fuzzy match + confidence bands |
| False positives flood the alert list | 🟠 High | **High** | Officers lose trust; jury notices | Confidence banding (only ≥65 alerts) · 60 s dedup window · review queue for 45–64 |
| RTSP instability / disconnects | 🟠 High | **High** | Coverage gaps | TCP forced · backoff 2→30 s with jitter · degraded-state tracking · health UI |
| Night / low-light footage | 🟠 High | Medium | Accuracy drops | CLAHE + upscaling; **lower confidence transparently rather than hiding it** |
| Motion blur & occlusion | 🟠 High | Medium | Missed plates | Multi-frame voting recovers most; 5 fps gives multiple attempts |
| GPU limits (yours or venue's) | 🟠 High | Medium | Throughput collapse | 5 fps sampling · YOLOv8n over v8x · ONNX/TensorRT if time · confirm venue GPU |
| Venue network fails during demo | 🟠 High | Medium | Demo collapses | Pre-cached map tiles · local Compose deployment · pre-recorded backup video |
| Kafka adds instability | 🟡 Medium | Medium | Lost time | KRaft single broker · **Day 2 go/no-go** · Redis Streams fallback ready |
| Feed looping creates false tracks | 🟡 Medium | **High** | Nonsense timelines | Detect discontinuity → reset tracker state (officially warned about) |
| Clock skew across cameras | 🟡 Medium | Medium | Wrong ordering / false implausibility | Anchor timestamps to server wall-clock at ingest; note the assumption in the HLD |
| Duplicate detections | 🟡 Medium | **High** | Cluttered UI, inflated counts | DB-level unique index on (plate, camera, minute) |
| Mixed H.264/H.265 decode failures | 🟡 Medium | Medium | Some cameras dark | Test both codecs locally Day 0; FFmpeg handles both natively |
| Cross-camera correlation errors | 🟡 Medium | Medium | Wrong routes | Confidence ≥65 threshold for route inclusion; plausibility flags |
| Snapshot storage growth | 🟢 Low | Medium | Disk fills | JPEG q=80 at reduced resolution; 24 h retention in demo |
| **Scope creep (face recognition, Re-ID)** | 🟠 High | **High** | Core flow unfinished | **Written DO-NOT-BUILD list agreed Day 0** |
| Security missing at submission | 🟡 Medium | Medium | Bonus lost; hosted URL unusable | ~10 h budgeted on Day 3 |
| Late merge chaos | 🟡 Medium | Medium | Integration failure | Event schemas frozen Day 0; Compose from Day 1 |

> **The two risks that actually decide the outcome: 50-stream decode performance, and unfinished deliverables.** Both are addressable today — benchmark the first, assign an owner to the second.

---

# 23. INPUTS NEEDED FROM THE TEAM

## 23.1 🔴 Blocking — needed before any code

| # | Input | Why it blocks | Where to get it |
|---|---|---|---|
| 1 | **The team PDF** | Gap analysis (§5) is currently against a proxy, not the real proposal | Place at `/home/cygnet/Desktop/Hackathon/` |
| 2 | **Registration confirmation + sandbox host/credentials** | Determines whether `/api/ingest` integration is real or simulated | Portal + `sentinel.hackathon@gujarat.gov.in` |
| 3 | **Category: 1 or 2?** | Different competition pool and expectations | Team decision |
| 4 | **Team size + who does what** | Determines whether the 5-role plan (§21.1) is achievable | Team decision |
| 5 | **Confirmed: is Phase 1 remote submission?** | Changes the entire 5-day plan if it is on-site | Helpdesk |

## 23.2 🟠 Needed within 24 hours

| # | Input | Why |
|---|---|---|
| 6 | **GPU availability** — ⚠ *no NVIDIA GPU detected on this machine* | Decides YOLOv8n vs v8s, batch size, whether real-time is achievable at 50 cameras. **If nobody on the team has an NVIDIA GPU, this is a P0 problem — rent a cloud GPU today.** |
| 7 | **Own CCTV footage for the 2–3 min own-feed video** | A mandatory deliverable. Indian road footage with visible plates. Phone footage of a street is acceptable if legally obtained |
| 8 | **A hosting target** for the mandatory hosted URL | VPS, cloud VM, or tunnel. Needs a public URL + credentials by Day 3 |
| 9 | **Whether ffmpeg is installed** — ⚠ *appears absent on this machine* | Blocks the MediaMTX sandbox replica. `sudo apt install ffmpeg` |
| 10 | **GitHub/GitLab repo** (can be private until submission) | Mandatory submission link |

## 23.3 🟡 Useful, not blocking

| # | Input |
|---|---|
| 11 | Real Gujarat camera locations (or permission to assign plausible ones — flagged via `geom_source`) |
| 12 | Any existing code the team has already written |
| 13 | Preferred branding/colour scheme for the dashboard |
| 14 | Whether anyone has PaddleOCR / YOLO experience (affects Day 1 estimates) |
| 15 | Sample Indian plate images for tuning the normalisation engine |

## 23.4 Environment findings (probed 2 Sep 2026)

| Check | Result | Action |
|---|---|---|
| Python | 3.10.12 ✅ | Fine |
| Docker | 29.1.3 ✅ | Fine |
| **NVIDIA GPU** | **Not detected** ⚠ | **Secure GPU access today** — cloud instance or a teammate's machine |
| **ffmpeg** | **Appears not installed** ⚠ | `sudo apt install ffmpeg` — required for both ingest and the sandbox replica |

---

# 24. FINAL DECISION SUMMARY

| # | Question | Answer |
|---|---|---|
| 1 | What Gujarat Police actually wants | A vendor-neutral, open-source integration layer unifying 26 incompatible CCTV systems (~80,000 cameras, 5 departments, 1,000 km) **without replacing them**, delivering real-time watchlist alerts and cross-camera vehicle route reconstruction |
| 2 | Core problem in one sentence | Turning 26 incompatible multi-vendor CCTV islands into one searchable intelligence layer that answers *"where has this vehicle been?"* in seconds — and proves it scales to 80,000 cameras |
| 3 | What to build | **SETU** — adapter ingest → edge ANPR → metadata-only events → explainable fuzzy matching → real-time alerts → cross-camera correlation → GIS route + investigation timeline, behind RBAC with audit |
| 4 | Recommended architecture | **Hybrid Edge + Central, metadata-first** (Model 5 Hybrid on a Model 3 skeleton delivering Model 2 capability). *Video stays local; only metadata travels; correlation happens centrally* |
| 5 | Cross-camera strategy | **Plate identity + PostGIS topology + time/distance plausibility. No Re-ID.** ByteTrack for intra-camera voting only |
| 6 | Event architecture | Apache Kafka KRaft single broker; partition by `camera_id` (ingest) and `plate` (correlation); Redis Streams as documented fallback |
| 7 | Database | PostgreSQL 16 + PostGIS + pg_trgm, plus Redis/Valkey. 8 tables. **No Elasticsearch** |
| 8 | GIS | MapLibre GL JS + OSM + PostGIS, tiles pre-cached for the venue |
| 9 | Security | MVP ~10 h (JWT, 3-role RBAC, audit, hashes, HTTPS); production in the HLD only, with DPDP Act 2023 |
| 10 | Top 3 differentiators | (1) Explainable confidence-scored ANPR matching (2) Metadata-first federated adapter architecture (3) Topology-aware correlation with cloned-plate detection |
| 11 | What to stop building | Face recognition · Re-ID · full VMS · Elasticsearch · K8s · suspicious-activity detection · mobile app |
| 12 | Biggest risks | 50-stream decode performance · unfinished deliverables |
| 13 | Highest-leverage action today | **Register**, email the helpdesk, and **stand up the MediaMTX sandbox replica** |

---

## 25. THE CLOSING ARGUMENT

Almost every competing team will read *"AI CCTV hackathon"* and build a beautiful YOLO demo on one camera.

But the police did not describe a detection problem. They described **26 systems that cannot talk to each other**. ANPR is the mandatory proof, not the prize.

The team that wins is the one whose demo makes a jury member think:

> *"This could actually be deployed on top of what we already own, without ripping anything out."*

— and then shows them a car tracked across a municipal camera, a GSRTC depot camera and two police cameras, and says:

> **"Four departments. Four vendors. Four seconds."**

---

## SOURCES

**Official (primary source of truth)**
- Portal — https://sentinel.gujarat.gov.in/
- Problem Statements & Guide — https://sentinel.gujarat.gov.in/problems
- About — https://sentinel.gujarat.gov.in/about
- Prize & Phases — https://sentinel.gujarat.gov.in/phases
- Resources / Integration Guide — https://sentinel.gujarat.gov.in/resource
- Schedule & Venue — https://sentinel.gujarat.gov.in/schedule
- FAQs — https://sentinel.gujarat.gov.in/faqs
- Gujarat Home Department — https://gujhome.gujarat.gov.in

**Secondary (context only; superseded by the portal wherever they conflict)**
- ANI — https://www.aninews.in/news/national/general-news/gujarat-police-to-host-countrys-largest-ai-based-cctv-hackathon20260817135250/
- Gujarat Samachar — https://english.gujaratsamachar.com/news/gujarat/gujarat-police-to-link-80000-cctv-cameras-in-states-largest-ai-based-video-analytics-hackathon-80179505714
- IANS Live — https://ianslive.in/gujarat-police-plans-single-network-for-80000-cctv-cameras-through-ai-based-hackathon--20260817133755
- Open Magazine — https://openthemagazine.com/india/can-80000-cameras-think-as-one-inside-gujarat-polices-mega-ai-hackathon

---

*Analysis complete. No implementation started. Awaiting the inputs in §23.*
