import math
import unittest

from eeg_athenalyze.recording import (
    Recording,
    SyntheticConfig,
    generate_synthetic_recording,
)


class SyntheticRecordingTests(unittest.TestCase):
    def test_generation_is_repeatable_for_same_seed(self):
        config = SyntheticConfig(
            sample_rate_hz=128,
            seed=42,
            line_noise_amplitude_uv=0,
            blink_rate_hz=0,
            muscle_burst_rate_hz=0,
        )
        first = generate_synthetic_recording(1, config=config)
        second = generate_synthetic_recording(1, config=config)

        self.assertEqual(first.samples_uv, second.samples_uv)
        self.assertEqual(first.timestamps_seconds, second.timestamps_seconds)
        self.assertEqual(first.channel_names, ("TP9", "AF7", "AF8", "TP10"))
        self.assertEqual(first.metadata["data_status"], "simulated")
        self.assertEqual(len(first.samples_uv), 128)
        self.assertTrue(
            all(math.isfinite(value) for row in first.samples_uv for value in row)
        )

    def test_alpha_reactivity_increases_closed_condition_amplitude(self):
        config = SyntheticConfig(
            sample_rate_hz=128,
            seed=7,
            oscillations_uv=(),
            alpha_amplitude_uv=10,
            line_noise_amplitude_uv=0,
            noise_amplitude_uv=0,
            blink_rate_hz=0,
            muscle_burst_rate_hz=0,
        )
        eyes_open = generate_synthetic_recording(
            2, config=config, condition="eyes_open"
        )
        eyes_closed = generate_synthetic_recording(
            2,
            config=config,
            condition="eyes_closed",
        )

        open_rms = _rms(eyes_open.samples_uv, channel=0)
        closed_rms = _rms(eyes_closed.samples_uv, channel=0)
        self.assertAlmostEqual(closed_rms / open_rms, 2.0, places=10)

    def test_rejects_duration_shorter_than_one_sample(self):
        with self.assertRaises(ValueError):
            generate_synthetic_recording(
                0.001, config=SyntheticConfig(sample_rate_hz=128)
            )


class RecordingValidationTests(unittest.TestCase):
    """Source timing is preserved, including measured duplicate timestamps."""

    @staticmethod
    def _make_recording(timestamps, *, status="measured", samples=None):
        if samples is None:
            samples = tuple((1.0, 2.0) for _ in timestamps)
        metadata = {} if status is None else {"data_status": status}
        return Recording(
            recording_id="timing-regression",
            sample_rate_hz=128.0,
            channel_names=("TP9", "AF7"),
            samples_uv=samples,
            timestamps_seconds=timestamps,
            metadata=metadata,
        )

    def test_measured_duplicates_are_retained_exactly(self):
        timestamps = (100.0, 100.0, 100.0078125)
        recording = self._make_recording(timestamps)
        self.assertEqual(recording.timestamps_seconds, timestamps)
        self.assertEqual(recording.samples_uv, ((1.0, 2.0),) * 3)

    def test_measured_decreasing_time_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "timestamps"):
            self._make_recording((10.0, 9.9))

    def test_non_measured_duplicates_are_rejected(self):
        for status in ("simulated", "unknown", None):
            with self.subTest(status=status):
                with self.assertRaisesRegex(ValueError, "strictly increasing"):
                    self._make_recording((0.0, 0.0), status=status)

    def test_non_measured_strict_increase_is_valid(self):
        for status in ("simulated", "unknown", None):
            with self.subTest(status=status):
                recording = self._make_recording(
                    (0.0, 1 / 128.0), status=status
                )
                self.assertEqual(recording.timestamps_seconds[0], 0.0)

    def test_nonfinite_timestamps_are_rejected(self):
        for status in ("measured", "simulated"):
            for invalid in (float("nan"), float("inf"), -float("inf")):
                with self.subTest(status=status, invalid=invalid):
                    with self.assertRaisesRegex(ValueError, "timestamps"):
                        self._make_recording((0.0, invalid), status=status)

    def test_wrong_channel_count_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "one value per channel"):
            self._make_recording((0.0,), samples=((1.0,),))

    def test_nonfinite_sample_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "sample values must be finite"):
            self._make_recording((0.0,), samples=((1.0, float("nan")),))

    def test_timestamp_and_sample_counts_must_match(self):
        with self.assertRaisesRegex(ValueError, "counts must match"):
            self._make_recording((0.0, 1.0), samples=((1.0, 2.0),))


def _rms(samples, channel):
    return math.sqrt(sum(row[channel] ** 2 for row in samples) / len(samples))


if __name__ == "__main__":
    unittest.main()
