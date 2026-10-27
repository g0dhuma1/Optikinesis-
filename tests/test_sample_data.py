"""Unit tests validating that all sample data fixtures load cleanly
and execute correctly against OptiKinesis core engines.
"""

import json
import os
import unittest

from blink_detector import DeliberateBlinkDetector
from head_calibration import HeadCalibration
from voice_commands import VoiceCommandParser


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")


class SampleDataValidationTests(unittest.TestCase):

    def test_sample_calibration_loads_and_maps(self):
        calib_path = os.path.join(SAMPLE_DATA_DIR, "sample_calibration.json")
        self.assertTrue(os.path.isfile(calib_path), "sample_calibration.json missing")

        with open(calib_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        calibration = HeadCalibration.from_dict(data)
        self.assertIsNotNone(calibration, "HeadCalibration.from_dict failed on sample data")

        # Neutral position (180, 180) should map close to center (0.5, 0.5)
        cx, cy = calibration.map(180.0, 180.0)
        self.assertAlmostEqual(cx, 0.5, places=2)
        self.assertAlmostEqual(cy, 0.5, places=2)

    def test_sample_settings_validity(self):
        settings_path = os.path.join(SAMPLE_DATA_DIR, "sample_settings.json")
        self.assertTrue(os.path.isfile(settings_path), "sample_settings.json missing")

        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("emergency_contact", data)
        self.assertIn("blink_sensitivity", data)
        self.assertIn("blinks_to_click", data)
        self.assertIn("head_calibration", data)

        # Embedded calibration should also parse
        embedded_calib = HeadCalibration.from_dict(data["head_calibration"])
        self.assertIsNotNone(embedded_calib)

    def test_sample_voice_commands_parse(self):
        commands_path = os.path.join(SAMPLE_DATA_DIR, "sample_voice_commands.json")
        self.assertTrue(os.path.isfile(commands_path), "sample_voice_commands.json missing")

        with open(commands_path, "r", encoding="utf-8") as f:
            test_cases = json.load(f)

        parser = VoiceCommandParser()
        for case in test_cases:
            intent = parser.parse(case["input"])
            self.assertEqual(
                intent.action_type.value,
                case["expected_action"],
                f"Failed parsing: {case['input']}"
            )
            self.assertEqual(
                intent.requires_confirmation,
                case["requires_confirmation"],
                f"Confirmation flag mismatch for: {case['input']}"
            )
            for param_key, expected_val in case["expected_params"].items():
                self.assertIn(param_key, intent.params)
                self.assertEqual(intent.params[param_key], expected_val)

    def test_sample_blink_traces_simulation(self):
        traces_path = os.path.join(SAMPLE_DATA_DIR, "sample_blink_traces.json")
        self.assertTrue(os.path.isfile(traces_path), "sample_blink_traces.json missing")

        with open(traces_path, "r", encoding="utf-8") as f:
            trace_suite = json.load(f)

        for case in trace_suite["test_cases"]:
            detector = DeliberateBlinkDetector(
                min_duration=0.15,
                max_duration=1.2,
                blinks_required=2,
                blink_window=1.5,
                click_cooldown=0.5
            )
            triggered_click = False
            completed_blinks = 0

            for reading in case["readings"]:
                t = reading["t"]
                closed = reading["eyes_closed"]
                update = detector.update(closed, t)
                if update.blink_completed:
                    completed_blinks += 1
                if update.click_triggered:
                    triggered_click = True

            self.assertEqual(
                triggered_click,
                case["expected_click"],
                f"Blink trace '{case['name']}' click expectation mismatch"
            )
            self.assertEqual(
                completed_blinks,
                case["expected_blinks"],
                f"Blink trace '{case['name']}' blink count mismatch"
            )


if __name__ == "__main__":
    unittest.main()
