<div align="center">

# OptiKinesis

### Hands-Free Computer Access for People Who Cannot Rely on Their Hands

*Webcam-based cursor control + blink selection + voice shortcuts — with an optional IMU MotionGlass upgrade for precision.*

---

**Developed by Govind Upadhyay**

---

**Head-Pose Tracking** · **Blink-to-Click** · **Virtual Keyboard** · **Voice Commands** · **Emergency SOS**

</div>

---

## Core Thesis

> **Digital independence should not require expensive specialist hardware.**
>
> Start with software. Upgrade only when a user needs higher precision.

---

## Origin Story

During our Community Engagement course, we visited an NGO and met people living with ALS / MND-related mobility limitations. Their minds were fully present — but an interface was missing. Everyday digital actions still depended entirely on a caregiver.

We asked ourselves a single question:

> *Can we restore everyday digital independence using the hardware people already have?*

That question became **OptiKinesis**: webcam-first access today, MotionGlass precision for users who need more stability tomorrow.

---

## The Problem

### 2.5 Billion+ people need assistive products

| Statistic | Source |
|---|---|
| **2.5 Billion+** people globally need at least one assistive product today, projected to exceed **3.5B by 2050** | WHO |
| **1 Billion** people who need assistive technology are denied access, especially in low- and middle-income settings | WHO |
| **5.4 Million** Indians were recorded with movement disability in Census 2011; **26.8M** with disability overall | Census of India |
| Access to needed assistive products can be as low as **3%** in some countries | WHO |

These conditions — **ALS, Parkinson's, stroke, spinal cord injuries, cerebral palsy, muscular dystrophy** — don't take away intelligence, opinions, humour, or the desire to connect. They take away the *physical interface* to a world that has moved entirely online.

Consider what losing your hands means in 2026:

- You cannot **type a message** to your family
- You cannot **browse the internet** or read the news
- You cannot **send an email** to your doctor
- You cannot **call for help** in an emergency
- You cannot **work**, even if your mind is fully capable
- You cannot **express a single thought** without someone physically present

### The gap in existing solutions

| Solution | Cost | Limitation |
|---|---|---|
| **Tobii Eye Trackers** | $3,000 – $15,000+ | Prohibitively expensive; proprietary hardware and software |
| **Brain-Computer Interfaces** | $10,000+ / Research-only | Invasive surgery or lab-grade equipment; not consumer-ready |
| **Sip-and-Puff switches** | $200 – $800 | Extremely slow single-switch scanning; no cursor freedom |
| **Head-tracking hardware (SmartNav)** | $400 – $600 | Requires IR reflective dots; no integrated clicking mechanism |

Most families affected by MND — especially in developing countries — simply **cannot afford** these solutions.

---

## Our Solution

### A webcam. That's all you need.

**OptiKinesis** is a software-only assistive technology system that transforms any standard laptop webcam into a complete hands-free computer control system. No special hardware. No expensive sensors. No surgical implants.

The system follows a three-stage pipeline:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   UNDERSTAND │ ──▶ │   STABILISE  │ ──▶ │     ACT      │
│              │     │              │     │              │
│  MediaPipe   │     │  Smoothing   │     │  Cursor      │
│  Facial      │     │  Click       │     │  Keyboard    │
│  Landmarks   │     │  Safety      │     │  Voice       │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Layer 1: Head-Pose Cursor Control

The user moves their head to control the mouse cursor.

- **How it works:** OptiKinesis uses MediaPipe's Face Landmarker to track 478 facial points in real-time. From five key anchor points (edges of face, forehead, chin, nose), the system computes a 3D gaze ray — a direction vector that maps to screen coordinates via yaw/pitch angle decomposition.
- **Personal 5-point calibration:** On first launch the user turns comfortably toward five dots: the center, then each corner. Each point is captured automatically once the head is steady, with no blinking needed. The cursor map is then fitted to that user's own range of movement, including uneven reach to one side. Even small head movements can therefore cover the whole screen.
- **Re-centering:** After shifting position, press **F9** or use **Re-center** in Settings. This moves the calibrated map without redoing all five points. The full calibration can be rerun any time from Settings.
- **Before calibration:** A default head turn of ±25° covers the screen width.
- **Smoothness:** A 12-frame rolling average combined with Exponential Moving Average (EMA) filtering eliminates jitter, producing cursor movement that feels natural and controlled.

### Layer 2: Blink-to-Click

The user blinks to click.

- **How it works:** The system monitors the Eye Aspect Ratio (EAR) of the left eye using four facial landmarks. When the EAR drops below a configurable threshold, a deliberate blink is detected.
- **Accuracy:** The cursor position is captured *before* the blink begins (since closing your eyes disrupts face tracking). The cursor also freezes during the blink to prevent drift. The click lands exactly where the user was looking.
- **Auto-keyboard:** When the cursor detects an I-beam text cursor (text input field), the virtual keyboard opens automatically — just like on a mobile phone.

### Layer 3: Voice Commands

The user speaks to perform complex tasks instantly.

- **Why it matters:** Even with perfect cursor control, some tasks require dozens of individual clicks. Voice commands let the user say *"Search how to cook pasta on Google"* and have it executed in a single breath.
- **Supported commands:** Google search, YouTube search, send email, set reminder, set alarm.
- **Safety:** Destructive or sensitive actions require explicit confirmation before execution.

### The Overlay Interface

All interaction happens through a floating desktop overlay (PyQt5) that sits on top of all applications without stealing focus or blocking the user's view.

| Module | Purpose |
|---|---|
| **⌨ Keyboard** | Full QWERTY virtual keyboard with Shift, Caps Lock, and special characters. Typed characters go directly into the active application's text field. A row of **word suggestions** above the keys updates as you type; one blink on a suggestion finishes the word and adds a space. The **Speak** button turns speech into text: press it, talk, and it stops after a short pause (press again to stop early). Uses Google's free speech service, so it needs internet and sends the audio to Google. |
| **📷 Camera** | Live preview of the webcam feed so the user or caregiver can verify face tracking. A mini camera feed also stays visible in the bottom-right corner at all times. |
| **🚨 Emergency** | One-tap SOS actions: WhatsApp message to a saved emergency contact, automated phone call via Twilio, or direct dial to emergency services (100 police / 112 ambulance in India). |
| **⚙ Control** | Adjustable settings for cursor speed, blink sensitivity, and lock delay — so caregivers can tune the system to each user's ability. |
| **🎤 Voice** | Native mode accepts command text with confirmation dialogs. Optional web mode adds browser-provided speech recognition. |
| **🌐 Web** | **Find answers** opens a large question box with the on-screen keyboard below it, then shows the top search results as large cards; one blink opens a result. **Read this page** turns the page open in the browser into large, clean text with no ads or pop-ups, with big Up/Down and text-size buttons. Powered by the free TinyFish Search and Fetch APIs (needs `TINYFISH_API_KEY`). Voice searches and "read this page" use it too. |

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    WEBCAM (30 FPS)                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           MediaPipe Face Landmarker (478 pts)            │
│              face_landmarker.task (3.7 MB)               │
└──────┬──────────────────────────────────┬───────────────┘
       │                                  │
       ▼                                  ▼
┌──────────────────┐            ┌──────────────────────┐
│  HEAD-POSE EST.  │            │  BLINK DETECTION     │
│                  │            │                      │
│  5 landmarks →   │            │  4 eye landmarks →   │
│  3D gaze ray →   │            │  Eye Aspect Ratio →  │
│  Yaw/Pitch →     │            │  Threshold check →   │
│  Screen X,Y      │            │  Click dispatch      │
└────────┬─────────┘            └──────────┬───────────┘
         │                                 │
         ▼                                 ▼
┌──────────────────┐            ┌──────────────────────┐
│  MOUSE MOVER     │            │  GAZE CLICK BRIDGE   │
│  THREAD          │            │                      │
│                  │            │  Qt widget hit-test → │
│  pyautogui.      │            │  Route to button OR  │
│  moveTo(x,y)     │            │  fallback OS click   │
│  every 10ms      │            │                      │
└──────────────────┘            └──────────────────────┘
         │                                 │
         └────────────┬───────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 PyQt5 DESKTOP OVERLAY                    │
│                                                         │
│   ┌─────────┐ ┌──────┐ ┌────────┐ ┌───────┐ ┌──────┐  │
│   │Keyboard │ │Camera│ │Emergcy │ │Control│ │Voice │  │
│   │ Module  │ │Module│ │ Module │ │Module │ │Module│  │
│   └─────────┘ └──────┘ └────────┘ └───────┘ └──────┘  │
│                                                         │
│   ┌──────────────────────┐   ┌──────────────────────┐  │
│   │ Mini Camera Feed     │   │  Auto-Open Keyboard  │  │
│   │ (bottom-right)       │   │  (I-beam detection)  │  │
│   └──────────────────────┘   └──────────────────────┘  │
│                                                         │
│          Floating Control Bar (always on top)            │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology |
|---|---|
| Face tracking | MediaPipe Face Landmarker (Tasks API) |
| Computer vision | OpenCV (webcam capture, frame processing) |
| Desktop overlay | PyQt5 (frameless, always-on-top, translucent, non-focus-stealing windows) |
| Mouse control | PyAutoGUI (cross-platform cursor movement and clicking) |
| Voice processing | Speech recognition + NLP intent parsing |
| Emergency comms | Twilio API (calls), WhatsApp Web (messaging) |
| Backend API | Flask (REST endpoints for settings, actions, status) |

### System Requirements

- **Hardware:** Any computer with a webcam (built-in laptop cameras work perfectly)
- **OS:** Windows (primary), with macOS/Linux compatibility via PyQt5
- **Python:** 3.8+
- **Cost of additional hardware:** ₹0 (uses existing webcam)

---

## Upcoming: MotionGlass

A lightweight IMU-enabled wearable that integrates with OptiKinesis to deliver smoother, faster, and more precise hands-free control. By combining inertial sensing with computer vision:

- **6-axis IMU:** Accelerometer + gyroscope for sub-degree head motion sensing
- **Bluetooth link** to the OptiKinesis Access Engine
- **Form factor:** Works as glasses, clip-on, or headband module
- **Upgrade path:** Users start with the free software-only webcam solution. If they need higher precision, they add MotionGlass without replacing anything.

---

## What Makes OptiKinesis Different

| Feature | Tobii Eye Tracker | SmartNav | OptiKinesis |
|---|---|---|---|
| **Hardware cost** | $3,000 – $15,000 | $400 – $600 | **₹0 (existing webcam)** |
| **Additional hardware** | Proprietary sensor bar | IR dot on forehead | **None** |
| **Click mechanism** | Dwell-time (stare to click) | External switch | **Natural eye blink** |
| **Emergency SOS** | None | None | **WhatsApp, call, police/ambulance** |
| **Voice commands** | None | None | **Google, YouTube, email, reminders** |
| **Virtual keyboard** | Third-party | Third-party | **Built-in full QWERTY** |
| **Auto-keyboard on text fields** | No | No | **Yes (I-beam cursor detection)** |
| **Hardware upgrade path** | None (locked in) | None | **MotionGlass IMU wearable** |
| **Open source** | No | No | **Yes** |
| **Works in developing countries** | Rarely (cost) | Rarely (availability) | **Yes — any laptop** |

---

## Impact to Society

### For the patient
- Type **"I love you"** to their child without needing someone else
- **Search for information** about their condition, restoring a sense of agency
- **Call for help** independently in an emergency
- **Work remotely** — writers, programmers, analysts with MND can continue contributing
- **Communicate needs** — pain levels, medication timing, comfort adjustments — without frustration

### For caregivers
- Reduced burnout from constant interpretation of the patient's needs
- Peace of mind that the patient can trigger an emergency alert independently
- A tool that can be configured once and requires minimal ongoing maintenance

### For the healthcare system
- Lower cost of care when patients can self-manage basic digital tasks
- Better patient outcomes through reduced isolation and depression
- A scalable, distributable solution that doesn't require hospital visits or specialist technicians

---

## Who Is This For?

### Primary Users

| User Group | Condition | How They Benefit |
|---|---|---|
| **ALS / MND patients** | Progressive loss of voluntary muscle control | Full computer access using only head and eyes |
| **Spinal cord injury patients** | Paralysis from neck down (quadriplegia) | Cursor control without hand function |
| **Cerebral palsy patients** | Impaired muscle coordination | Smoother cursor accommodates tremors |
| **Muscular dystrophy patients** | Progressive muscle weakness | Low-effort interaction (small movements = full screen) |
| **Stroke survivors** | Partial or full paralysis | Computer access during rehabilitation |
| **Locked-in syndrome patients** | Full-body paralysis with preserved consciousness | Communication lifeline via blink-to-click |
| **Parkinson's patients** | Tremor and motor impairment | Voice commands bypass fine motor requirements |

### Secondary Stakeholders

| Stakeholder | How They Benefit |
|---|---|
| **Caregivers & family** | Reduced communication burden; emergency SOS provides safety net |
| **Hospitals & rehab centers** | Low-cost assistive tech for patient rooms |
| **NGOs & disability foundations** | Distributable at scale with zero hardware cost |
| **Government disability programs** | Cost-effective alternative to commercial assistive devices |
| **Employers** | Enable remote work for employees with motor disabilities |

---

## Market

| Segment | Size |
|---|---|
| **TAM** — Global AAC Device Market (2026) | $2.8B, growing to $5–6B by 2035 (9–11% CAGR) |
| **SAM** — People globally requiring assistive technology | 75M+ (WHO) |
| **SOM** — Initial focus on ALS & Parkinson's via hospitals, rehab, NGOs | 1–2M |

### Typical Customer Profile

A working professional (40–60 years) experiencing progressive upper-limb motor impairment who seeks to remain independent at work and in daily life. Prefers software that works with an existing laptop rather than dedicated hardware.

---

## Business Model

| Tier | What's Included |
|---|---|
| **OptiKinesis Access** (software-only, one-time purchase) | Webcam control, blink click, virtual keyboard, voice shortcuts, SOS, local diagnostics |
| **MotionGlass Kit** (hardware add-on) | IMU wearable, Bluetooth setup, Motion/Fusion mode, charger, setup guide |
| **OptiKinesis Care** (optional subscription) | Quarterly calibration, device-health check, priority support, caregiver backup |
| **Institutional Bundle** (for NGOs / Hospitals) | Multi-user profiles, training, fleet monitoring, support and replacement workflow |

---

## Author

**Govind Upadhyay** — System Architecture, Accessibility Workflow & Development

---

## Project Structure

```
OptiKinesis/
├── main.py                  # Entry point — camera loop, tracking, blink detection, Flask API
├── blink_detector.py        # Deliberate single/double-blink state machine
├── head_calibration.py      # 5-point head calibration: capture logic and personal cursor map
├── desktop_overlay.py       # PyQt5 overlay UI — all panels, keyboard, control bar, gaze bridge
├── voice_commands.py         # Voice command NLP parsing and task automation
├── web_assist.py             # TinyFish Search/Fetch client for answer cards and the clean reader
├── word_suggestions.py       # Word completion for the on-screen keyboard
├── speech_input.py           # Voice typing for the keyboard's Speak button
├── fatigue_monitor.py        # Rolling-window blink-rate analyzer for fatigue detection
├── eye_blink.py              # Standalone blink detection utilities
├── preview_overlay.py        # Live-reload preview tool for iterating on overlay UI
├── face_landmarker.task      # MediaPipe face landmark model (3.7 MB)
├── requirements.txt          # Python dependencies
├── TECHNICAL_DESIGN.md       # Technical Design Document with Mermaid architectural diagrams
├── TESTING.md                # Testing guide & sample data documentation
├── LICENSE                   # MIT License
├── OVERLAY_UI_MAP.md         # Developer reference — which code lines change which UI elements
├── PROJECT_DESCRIPTION.md    # Detailed project description document
├── sample_data/              # Sample test fixtures (calibration, settings, voice, blinks)
├── templates/                # Flask HTML templates (web dashboard)
├── static/                   # Static assets for web interface
└── tests/                    # Automated blink, calibration, fatigue, voice, and API tests
```

---

## Getting Started

### Prerequisites

- **Operating System**: Windows 10/11 (fully supported with native desktop overlay), or macOS / Linux (Web Dashboard mode)
- **Python**: Version 3.8 to 3.11
- **Hardware**: Standard integrated or USB webcam (720p @ 30 FPS minimum), working microphone for voice commands

---

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/g0dhuma1/Optikinesis-.git
cd Optikinesis-
```

#### 2. Create and Activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note on PyQt5**: The native floating desktop overlay requires PyQt5 (`pip install PyQt5`). On systems without PyQt5, OptiKinesis gracefully falls back to browser-based control mode (`--web`).

#### 4. Configure Environment Variables
Copy the sample environment file and configure any optional service integrations:
```bash
cp .env.example .env     # Linux / macOS
copy .env.example .env   # Windows
```

---

### Environment Variables (`.env`)

All environment variables are optional. The system operates locally out of the box with default fallbacks if `.env` is omitted.

| Variable | Required? | Default | Description & Usage |
|---|---|---|---|
| `TWILIO_SID` | Optional | *None* | Twilio Account SID for sending automated emergency SOS SMS / voice calls to caregivers. |
| `TWILIO_AUTH` | Optional | *None* | Twilio Auth Token for API authentication. |
| `TWILIO_PHONE` | Optional | *None* | Twilio phone number in E.164 format (e.g., `+15551234567`) registered as the sender. |
| `SMTP_SERVER` | Optional | `smtp.gmail.com` | Outgoing SMTP mail server used for voice-dictated email sending. |
| `SMTP_PORT` | Optional | `587` | Port for outgoing SMTP connections with TLS encryption. |
| `SMTP_EMAIL` | Optional | *None* | Caregiver or user Gmail/email address used to authenticate and send outgoing messages. |
| `SMTP_PASSWORD` | Optional | *None* | Email App Password (generated via Google Account App Passwords) for authentication. |
| `WHATSAPP_SEND_DELAY` | Optional | `12` | Number of seconds to wait for WhatsApp Web to load in the browser before dispatching message. |
| `TINYFISH_API_KEY` | Optional | *None* | API key for TinyFish AI Search & Fetch clean reader engine ([obtain free key](https://agent.tinyfish.ai/api-keys)). If omitted, web searches fall back directly to Google. |

---

### Running the Application

#### Option A: Native Floating Desktop Overlay (Recommended)
```bash
python main.py
```
- Launches the native transparent overlay hovering over your desktop.
- On first launch, follow the automated **5-point head calibration**: comfortably turn your head toward each dot on the screen and hold still.
- Move your head to steer the cursor; blink deliberately (two blinks within 1.5 seconds by default) to click.
- User accessibility profiles and calibration coordinates are saved automatically in `settings.json`.

**Caregiver Safety Hotkeys**:
| Key | Action |
|---|---|
| **F9** | Instantaneous re-center of the cursor on the current head pose |
| **F12** | Global safety pause / resume for all mouse control |
| **Esc** / **F12** | Cancel an active calibration run |

#### Option B: Browser Web Dashboard
```bash
python main.py --web
```
- Starts a local web server at `http://127.0.0.1:5000`.
- Provides live camera streaming with overlaid face landmark mesh, real-time yaw/pitch telemetry gauges, and a settings customization portal.

---

### Running Tests & Validating Sample Data

OptiKinesis includes an automated test suite with **83 tests** covering all algorithms, blink detectors, calibration projections, and voice parsers.

```bash
# Run all automated tests
python -m unittest discover -v

# Run sample data integration tests
python -m unittest tests/test_sample_data.py -v
```

For detailed test architecture, coverage reports, and sample data specifications, see [`TESTING.md`](TESTING.md).

---

## Documentation Links

- **[Technical Design Document](TECHNICAL_DESIGN.md)**: Full architectural diagrams, MediaPipe mathematical projections, threading models, and state machines.
- **[Testing & Sample Data Guide](TESTING.md)**: Test suites, coverage breakdown, and sample fixture documentation.
- **[Overlay UI Map](OVERLAY_UI_MAP.md)**: Detailed code-to-element mapping for the PyQt5 overlay.
- **[License](LICENSE)**: MIT License.

---

<div align="center">

*Built with the belief that the ability to communicate is a human right — not a privilege of the able-bodied.*

**Digital independence should not be limited by whether a patient can afford specialist assistive hardware.**

</div>
