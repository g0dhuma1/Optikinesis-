# Testing Guide & Sample Data Documentation — OptiKinesis

This document details the test framework, automated test suites, sample data fixtures, and end-to-end verification workflows for OptiKinesis.

---

## 1. Automated Test Suite

OptiKinesis includes an automated test suite with **83 unit tests** written using Python's standard `unittest` framework. The suite executes in under **0.5 seconds** and tests all core mathematical, algorithmic, and parsing logic without requiring a physical webcam or external network services.

### Running All Tests

To run the complete test suite:

```bash
python -m unittest discover -v
```

### Running Specific Test Modules

```bash
# Test sample data fixtures and serialization
python -m unittest tests/test_sample_data.py -v

# Test 5-point head calibration engine and triangle-affine projection
python -m unittest tests/test_head_calibration.py -v

# Test deliberate single/double-blink state machine
python -m unittest tests/test_blink_detector.py -v

# Test natural language voice command parsing & task scheduling
python -m unittest tests/test_voice_commands.py -v

# Test voice speech input endpointer and audio transcription handling
python -m unittest tests/test_speech_input.py -v

# Test TinyFish web search, article reader, and text normalization
python -m unittest tests/test_web_assist.py -v

# Test predictive on-screen keyboard word suggestions
python -m unittest tests/test_word_suggestions.py -v

# Test fatigue monitor rolling blink-rate analysis
python -m unittest tests/test_fatigue_monitor.py -v

# Test Flask Web API endpoints and settings validation
python -m unittest tests/test_web_api.py -v
```

---

## 2. Sample Data Fixtures (`sample_data/`)

The `sample_data/` directory provides pre-validated test fixtures designed for automated testing, debugging, and offline evaluation.

| Fixture File | Format | Purpose & Description |
|---|---|---|
| [`sample_data/sample_calibration.json`](sample_data/sample_calibration.json) | JSON | Validated 5-point head calibration dataset mapping neutral pose (`180°, 180°`) and four corner bounds to normalized screen targets. |
| [`sample_data/sample_settings.json`](sample_data/sample_settings.json) | JSON | Production user configuration structure containing cursor sensitivity, dwell limits, blink threshold, and embedded calibration data. |
| [`sample_data/sample_voice_commands.json`](sample_data/sample_voice_commands.json) | JSON | Standardized voice command test suite covering Google queries, YouTube searches, structured email drafting, alarms, reminders, and clean reader commands. |
| [`sample_data/sample_blink_traces.json`](sample_data/sample_blink_traces.json) | JSON | High-fidelity synthetic time-series Eye Aspect Ratio (EAR) traces comparing involuntary micro-blinks (66ms), deliberate clicks, and eye rest (1.35s). |

---

## 3. Test Coverage Breakdown

### Mathematical & Algorithm Verification
- **5-Point Head Pose Calibration**:
  - Affine transformation matrix computation per screen quadrant triangle.
  - Extrapolation logic for screen edges beyond corner target insets (`TARGET_INSET = 0.10`).
  - Validation against degenerate/collinear corner points (`MIN_CORNER_SINE = 0.15`).
  - Minimum angular span requirement (`MIN_SPAN_DEG = 6.0°`).
  - Dynamic re-centering calculation shifting neutral offsets without distorting calibrated corner spans.

- **Blink State Machine (`DeliberateBlinkDetector`)**:
  - Rejection of involuntary physiological blinks (`< 0.15s`).
  - Rejection of prolonged eye closure/rest (`> 1.2s`).
  - Multi-blink aggregation window enforcement (`blink_window = 1.5s`).
  - Debounce cooldown preventing accidental double-clicking (`click_cooldown = 0.5s`).

- **Voice Command Parser (`VoiceCommandParser`)**:
  - Strict parameter extraction for email recipients, subjects, and multi-word body text.
  - Confirmation flags ensuring sensitive actions (sending email, setting alarms) require user verification.
  - Direct search fallback for conversational phrases ("What is...", "Find...", "Look up...").

---

## 4. Manual End-to-End Verification Checklist

For hardware verification with an active webcam and microphone:

1. **Webcam Head-Tracking**:
   - Run `python main.py`.
   - Verify that tilting your head slightly moves the on-screen cursor smoothly with exponential moving average (EMA) damping.
   - Press **F9** to confirm instantaneous cursor re-centering.

2. **Blink Selection**:
   - Double-blink deliberately with your eyes closed for ~200ms each.
   - Confirm a left-click is registered and the audio feedback chime (`static/sounds/click.mp3`) plays.

3. **Caregiver Safety Keys**:
   - Press **F12** to pause mouse movement; confirm the overlay displays a paused banner.
   - Press **F12** again to resume control.

4. **Web Browser Fallback Mode**:
   - Launch with `python main.py --web`.
   - Navigate to `http://localhost:5000` to verify live video stream rendering, real-time yaw/pitch indicators, and browser settings adjustments.
