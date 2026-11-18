import hashlib
import json
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

from eeg_athenalyze.archive import load_recording, save_recording
from eeg_athenalyze.recording import SyntheticConfig, generate_synthetic_recording


class RecordingArchiveTests(unittest.TestCase):
    def setUp(self):
        self.recording = generate_synthetic_recording(
            0.25,
            config=SyntheticConfig(
                sample_rate_hz=128,
                seed=11,
                blink_rate_hz=0,
                muscle_burst_rate_hz=0,
            ),
        )
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.path = Path(self.temporary_directory.name) / "session.eegz"

    def test_archive_round_trip_preserves_raw_samples_and_metadata(self):
        save_recording(self.recording, self.path)

        self.assertEqual(load_recording(self.path), self.recording)

    def test_saving_never_overwrites_an_existing_recording(self):
        save_recording(self.recording, self.path)
        original_bytes = self.path.read_bytes()
        replacement = generate_synthetic_recording(
            0.5, config=SyntheticConfig(sample_rate_hz=128, seed=12)
        )

        with self.assertRaises(FileExistsError):
            save_recording(replacement, self.path)
        self.assertEqual(self.path.read_bytes(), original_bytes)

    def test_checksum_mismatch_is_rejected(self):
        save_recording(self.recording, self.path)
        tampered_path = Path(self.temporary_directory.name) / "tampered.eegz"
        with zipfile.ZipFile(self.path, mode="r") as source:
            members = {name: source.read(name) for name in source.namelist()}
        members["recording.json"] += b" "
        with zipfile.ZipFile(tampered_path, mode="w") as target:
            for name, content in members.items():
                target.writestr(name, content)

        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            load_recording(tampered_path)


    def _saved_members(self):
        save_recording(self.recording, self.path)
        with zipfile.ZipFile(self.path, mode="r") as archive:
            return [(name, archive.read(name)) for name in archive.namelist()]

    @staticmethod
    def _write_members(path, members):
        with zipfile.ZipFile(path, mode="w") as archive:
            for name, content in members:
                archive.writestr(name, content)

    def test_archive_accepts_reordered_members(self):
        members = self._saved_members()
        reordered_path = Path(self.temporary_directory.name) / "reordered.eegz"
        self._write_members(reordered_path, list(reversed(members)))
        self.assertEqual(load_recording(reordered_path), self.recording)

    def test_duplicate_members_are_rejected(self):
        members = self._saved_members()
        for name in ("manifest.json", "recording.json"):
            with self.subTest(duplicate=name):
                target = Path(self.temporary_directory.name) / (
                    "duplicate-" + name + ".eegz"
                )
                repeated = next(content for member, content in members
                                if member == name)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    self._write_members(
                        target, [*members, (name, repeated)]
                    )
                with self.assertRaisesRegex(ValueError, "archive members"):
                    load_recording(target)

    def test_unexpected_member_is_rejected(self):
        members = self._saved_members()
        target = Path(self.temporary_directory.name) / "unexpected.eegz"
        self._write_members(target, [*members, ("extra.txt", b"untracked")])
        with self.assertRaisesRegex(ValueError, "archive members"):
            load_recording(target)

    def test_nonobject_manifest_is_rejected(self):
        members = self._saved_members()
        for bad_manifest in (b"[]", b"null"):
            with self.subTest(manifest=bad_manifest):
                target = Path(self.temporary_directory.name) / (
                    "bad-manifest-" + str(len(bad_manifest)) + ".eegz"
                )
                changed = [(name, bad_manifest if name == "manifest.json"
                            else content) for name, content in members]
                self._write_members(target, changed)
                with self.assertRaisesRegex(ValueError, "archive manifest"):
                    load_recording(target)

    def test_oversized_manifest_is_rejected_before_json_parse(self):
        members = self._saved_members()
        target = Path(self.temporary_directory.name) / "huge-manifest.eegz"
        huge_manifest = b"{" + b" " * (64 * 1024) + b"}"
        changed = [(name, huge_manifest if name == "manifest.json"
                    else content) for name, content in members]
        self._write_members(target, changed)
        with self.assertRaisesRegex(ValueError, "manifest is too large"):
            load_recording(target)

    def test_nonobject_metadata_is_rejected_with_value_error(self):
        members = dict(self._saved_members())
        payload = json.loads(members["recording.json"])
        payload["metadata"] = []
        recording_data = json.dumps(
            payload, allow_nan=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        manifest = json.loads(members["manifest.json"])
        manifest["recording_sha256"] = hashlib.sha256(recording_data).hexdigest()
        target = Path(self.temporary_directory.name) / "bad-metadata.eegz"
        self._write_members(target, [
            ("manifest.json", json.dumps(manifest).encode("utf-8")),
            ("recording.json", recording_data),
        ])
        with self.assertRaisesRegex(ValueError, "archive content"):
            load_recording(target)


if __name__ == "__main__":
    unittest.main()
