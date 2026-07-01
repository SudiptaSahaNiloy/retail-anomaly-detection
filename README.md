# 🏪 Retail Anomaly Detection System
> An AI-powered CCTV analysis pipeline for real-time suspicious behaviour detection in retail environments.

Built as a portfolio project and research prototype — combining computer vision, pose estimation, and behavioural analysis to detect potential theft without facial recognition or identity tracking.

---

## 📌 Project Status

| Week | Focus | Status |
|---|---|---|
| Week 1 | Environment setup, person detection, pose estimation | ✅ In Progress (Day 2) |
| Week 2 | Zone detection, dwell-time tracking, object interaction | 🔜 Upcoming |
| Week 3 | Anomaly rule engine, suspicion scoring | 🔜 Upcoming |
| Week 4 | Alert system, FastAPI backend, dashboard | 🔜 Upcoming |
| Week 5 | Live camera / RTSP stream integration | 🔜 Upcoming |
| Week 6 | Real-world pilot deployment | 🔜 Upcoming |
| Week 7 | Iteration on real data, false-positive tuning | 🔜 Upcoming |
| Week 8 | Polish, documentation, demo video | 🔜 Upcoming |

---

## 🎯 What This Does

This system takes a CCTV video feed — recorded or live — and runs a multi-layer analysis pipeline:

1. **Person detection** — identifies and tracks every individual in frame using YOLOv8
2. **Pose estimation** — extracts 17-point skeletal keypoints per person per frame
3. **Zone awareness** — monitors entry/exit of defined store zones (shelf, checkout, exit)
4. **Behavioural analysis** — flags suspicious patterns such as concealment gestures, excessive dwell time, or bypassing checkout *(coming Week 3)*
5. **Alert system** — sends real-time notifications and logs flagged clips *(coming Week 4)*
6. **Dashboard** — web interface for staff to review alerts *(coming Week 4)*

---

## 🧱 Architecture

```
CCTV Feed (MP4 / RTSP)
        │
        ▼
┌─────────────────────┐
│   Frame Processor   │  ← OpenCV — reads frames, handles rotation/resize
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   YOLOv8-Pose       │  ← Person detection + 17-point skeleton extraction
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   ByteTrack         │  ← Persistent person ID tracking across frames
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   Zone Engine       │  ← Detects zone entry/exit, dwell time per person
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   Anomaly Rules     │  ← Suspicion score per person (rule-based v1)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   Alert System      │  ← Telegram bot + clip saving on threshold breach
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   FastAPI Backend   │  ← Stores alerts in SQLite, serves dashboard API
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   Web Dashboard     │  ← Staff-facing UI with live alerts + clip playback
└─────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Object Detection | YOLOv8n (ultralytics) | Person detection, COCO class filtering |
| Pose Estimation | YOLOv8n-Pose | 17-point skeleton per person |
| Tracking | ByteTrack (built into ultralytics) | Persistent person IDs across frames |
| Video Handling | OpenCV | Frame reading, rotation, resize, display |
| Backend | FastAPI + SQLite | Alert storage, REST API |
| Notifications | Telegram Bot API | Real-time alert delivery |
| Dashboard | React (or HTML/JS) | Staff-facing alert review UI |
| Deployment | Local machine / RTSP camera | Pilot deployment |

---

## 📁 Project Structure

```
retail-anomaly-detection/
│
├── footage/                  # Local test footage (gitignored — never committed)
│
├── detect_test.py            # Day 1 — YOLOv8 person detection on video
├── pose_test.py              # Day 2 — YOLOv8-Pose skeleton extraction
│
├── utils/
│   └── frame_utils.py        # get_display_frame() — rotation + resize helper
│
├── models/                   # Downloaded .pt model weights (gitignored)
│
├── alerts/                   # Saved alert clips and screenshots (gitignored)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

**Prerequisites:** Python 3.9+, pip

```bash
# Clone the repo
git clone https://github.com/yourusername/retail-anomaly-detection.git
cd retail-anomaly-detection

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```
ultralytics
opencv-python
fastapi
uvicorn
python-telegram-bot
```

---

## 🚀 Running the Pipeline (Current State)

**Person detection on a video file:**
```bash
python detect_test.py
```

**Pose estimation with skeleton overlay:**
```bash
python pose_test.py
```

Press `Q` to exit either script.

---

## 🔑 Key Technical Notes

**Rotation handling:** Source CCTV footage exports as `(2560, 1440, 3)` — a portrait-orientation frame (9:16 aspect ratio). OpenCV ignores video metadata rotation flags that normal players (e.g. VLC) respect automatically. All frame processing includes an explicit `cv2.rotate()` call before inference to correct orientation.

**Display scaling:** Frames are resized to a fixed display height of 700px before rendering, preserving aspect ratio. Inference runs on the resized frame to match processing cost to actual displayed resolution.

**Privacy by design:** No facial recognition is used at any stage. Detection operates on skeletal pose keypoints only — behavioural signals (wrist position, zone entry, dwell time) without biometric identity. Raw footage is never committed to version control and is kept strictly local.

---

## 🗺️ Roadmap

- [x] YOLOv8 person detection on CCTV footage
- [x] Rotation and display scaling resolved for portrait-format source footage
- [x] YOLOv8-Pose skeleton extraction and keypoint data inspection
- [ ] ByteTrack persistent person ID tracking
- [ ] Zone definition and entry/exit logic
- [ ] Dwell-time tracking per person per zone
- [ ] Concealment gesture detection via wrist-to-hip proximity
- [ ] Suspicion scoring engine
- [ ] Telegram alert on threshold breach
- [ ] FastAPI backend + SQLite alert logging
- [ ] Web dashboard with clip playback
- [ ] RTSP live camera integration
- [ ] Real-world pilot deployment
- [ ] False-positive tuning on real store data

---

## 🔬 Research Context

This project is built in parallel with a PhD research proposal targeting **Video Anomaly Detection (VAD)** in retail environments, with a focus on:

- Privacy-preserving detection (pose-only, no face data)
- Fairness-aware training (equitable detection across demographic groups)
- Real-world dataset construction (genuine footage vs staged scenarios)

Key academic references:
- RD4AD — Deng & Li, CVPR 2022 (reverse distillation anomaly detection)
- PoseLift — WACV 2025 (pose-based shoplifting detection benchmark)
- UCF-Crime — Sultani et al., CVPR 2018 (surveillance anomaly dataset)
- Shopformer — 2025 (transformer-based shoplifting detection)

---

## ⚖️ Privacy & Ethics

- All development footage is stored locally and never committed to version control
- Faces are blurred in any publicly shared demo material
- Employer permission obtained before using any workplace CCTV footage
- Compliant with Australia's Privacy Act 1988 and Workplace Surveillance Act (NSW)
- No biometric data (faces, fingerprints) is collected or stored at any stage

---

## 👤 Author

**Sudipta [Last Name]**
Postgraduate AI Student — Macquarie University, Sydney, Australia
[your.email@example.com] | [LinkedIn] | [GitHub]

*Built as a portfolio project and research prototype. Not a commercial product.*
