"""Deterministic local smoke test; fabricated data are never empirical evidence."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import mne
import numpy as np

with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    fs = 160
    time = np.arange(fs * 10) / fs
    inputs = []
    for condition, strength in (("eo", 1.0), ("ec", 1.7)):
        matrix = np.stack([
            15e-6 * strength * np.sin(2 * np.pi * 10 * time)
            + 2e-6 * np.sin(2 * np.pi * 17 * time),
            8e-6 * strength * np.sin(2 * np.pi * 10 * time),
        ])
        raw = mne.io.RawArray(matrix, mne.create_info(["Oz", "Pz"], fs, "eeg"),
                              verbose="ERROR")
        name = base / f"{condition}.fif"
        raw.save(name, overwrite=True, verbose="ERROR")
        inputs.append(name)

    target = base / "results"
    subprocess.run([
        sys.executable, str(Path(__file__).with_name("real_eeg_pipeline.py")),
        "--source", "local",
        "--eo", str(inputs[0]), "--ec", str(inputs[1]),
        "--output", str(target),
    ], check=True)
    expected = {"01_raw_eeg.png", "02_welch_psd.png",
                "03_welch_psd.csv", "04_manifest.json"}
    assert {file.name for file in target.iterdir()} == expected
    manifest = json.loads((target / "04_manifest.json").read_text("utf-8"))
    assert manifest["alpha_power_uv2"]["EC"] > manifest["alpha_power_uv2"]["EO"]
    assert manifest["analysis"]["channel"] == "Oz"
    assert "unverified" in manifest["data_kind"]
    print("SMOKE TEST PASS: local input -> QC -> Welch -> PNG/CSV/JSON")
