#!/usr/bin/env python3
"""Reproducible EO/EC demo: real PhysioNet EEGMMIDB or locally owned EEG.

PhysioNet: subject 1, runs 1 (eyes open) and 2 (eyes closed).
Local: two already recorded EEG files (EDF, BrainVision VHDR, or FIF).
This does NOT acquire EEG or validate EEG Neurolyze Muse S Athena hardware.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mne
import numpy as np
from scipy.integrate import trapezoid

ALPHA = (8.0, 13.0)
F_RANGE = (1.0, 40.0)
AMPLITUDE_THRESHOLD_UV = 150.0  # demonstration-only screening heuristic


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["physionet", "local"], required=True)
    parser.add_argument("--subject", type=int, default=1, help="PhysioNet participant 1..109")
    parser.add_argument("--eegbci-cache", type=Path, default=Path("data/external/eegbci"))
    parser.add_argument("--eo", type=Path, help="Local eyes-open EDF/VHDR/FIF")
    parser.add_argument("--ec", type=Path, help="Local eyes-closed EDF/VHDR/FIF")
    parser.add_argument("--channel", help="Identical EEG channel in EO and EC (e.g. Oz)")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def read_file(path: Path) -> mne.io.BaseRaw:
    if not path.is_file():
        raise FileNotFoundError(path)
    ext = path.suffix.lower()
    if ext == ".edf":
        raw = mne.io.read_raw_edf(path, preload=True, verbose="ERROR")
    elif ext == ".vhdr":
        raw = mne.io.read_raw_brainvision(path, preload=True, verbose="ERROR")
    elif ext == ".fif":
        raw = mne.io.read_raw_fif(path, preload=True, verbose="ERROR")
    else:
        raise ValueError("Expected EDF, BrainVision .vhdr or FIF; .eegz is unsupported")
    return raw


def get_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    if args.source == "physionet":
        if args.eo or args.ec:
            raise ValueError("Use either --source physionet or --source local with --eo/--ec")
        if not 1 <= args.subject <= 109:
            raise ValueError("PhysioNet subject must be within 1..109")
        from mne.datasets import eegbci
        args.eegbci_cache.mkdir(parents=True, exist_ok=True)
        # Automatically downloads ONLY baseline runs 1 and 2, if missing.
        files = eegbci.load_data(args.subject, [1, 2], path=args.eegbci_cache,
                                 update_path=False)
        by_run = {int(Path(p).stem[-2:]): Path(p) for p in files}
        return by_run[1], by_run[2]
    if args.eo is None or args.ec is None:
        raise ValueError("--source local requires both --eo and --ec")
    return args.eo, args.ec


def choose_channel(raws: dict[str, mne.io.BaseRaw], requested: str | None) -> str:
    shared = set.intersection(*(set(r.ch_names) for r in raws.values()))
    if requested:
        if requested not in shared:
            raise ValueError(f"Missing identical channel {requested!r} in EO and EC")
        return requested
    for candidate in ("Oz", "O1", "O2", "Pz", "POz", "AF7", "AF8"):
        if candidate in shared:
            return candidate
    common_eeg = set.intersection(*(set(r.copy().pick("eeg").ch_names) for r in raws.values()))
    if not common_eeg:
        raise ValueError("No shared EEG channel between EO and EC")
    return sorted(common_eeg)[0]


def amplitude_screen(raw: mne.io.BaseRaw, channel: str) -> dict:
    """Flag 1-second periods with |EEG| > 150 µV. This is NOT EOG/EMG removal."""
    sf = raw.info["sfreq"]
    window = int(round(sf))
    signal = raw.get_data(picks=[channel])[0]
    n = len(signal) // window
    if n == 0:
        raise ValueError("Recording must be at least 1 s long")
    # Annotation is not applied to PSD here: report only, to avoid silent sample loss.
    flags = [bool(np.max(np.abs(signal[k*window:(k+1)*window])) >
                  AMPLITUDE_THRESHOLD_UV * 1e-6) for k in range(n)]
    return {"screening_method": "abs amplitude threshold, 1-second windows",
            "threshold_uv": AMPLITUDE_THRESHOLD_UV,
            "flagged_windows": sum(flags), "window_count": n,
            "flagged_fraction": sum(flags)/n,
            "note": "Heuristic screening only; all data retained for illustrative PSD"}


def compute_welch(raw: mne.io.BaseRaw, channel: str):
    filtered = raw.copy().filter(l_freq=1.0, h_freq=40.0, picks="eeg",
                                 n_jobs=1, verbose="ERROR")
    spec = filtered.compute_psd(method="welch", picks=[channel],
                                fmin=F_RANGE[0], fmax=F_RANGE[1],
                                n_fft=256, n_overlap=128,
                                reject_by_annotation=False, verbose="ERROR")
    psd, freqs = spec.get_data(return_freqs=True)
    psd_uv = psd[0] * 1e12  # MNE returns V²/Hz -> µV²/Hz
    alpha = (freqs >= ALPHA[0]) & (freqs <= ALPHA[1])
    alpha_power = float(trapezoid(psd_uv[alpha], x=freqs[alpha]))
    return filtered, freqs, psd_uv, alpha_power


def chart_signal(raws: dict, channel: str, output: Path) -> None:
    fig, axs = plt.subplots(2, 1, figsize=(11, 5), sharex=True, layout="constrained")
    for ax, (name, raw) in zip(axs, raws.items()):
        sf = raw.info["sfreq"]
        length = min(raw.n_times, round(8*sf))
        v = raw.get_data(picks=[channel], start=0, stop=length)[0] * 1e6
        t = np.arange(length)/sf
        ax.plot(t, v, linewidth=.8)
        ax.set_ylabel("Amplituda [µV]")
        ax.set_title(f"{name}: kanał {channel} (pierwsze 8 s)")
        ax.grid(alpha=.2)
    axs[-1].set_xlabel("Czas [s]")
    fig.suptitle("EEG - oryginalne próbki po imporcie, bez filtracji", weight="bold")
    fig.savefig(output, dpi=160); plt.close(fig)


def chart_psd(freqs: np.ndarray, psds: dict, channel: str, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    for name, psd in psds.items():
        ax.plot(freqs, psd, label=name, linewidth=2)
    ax.axvspan(*ALPHA, alpha=.13, label="alfa 8-13 Hz")
    ax.set_xlabel("Częstotliwość [Hz]")
    ax.set_ylabel("PSD [µV²/Hz]")
    ax.set_title(f"Welch PSD: {channel} (filtr 1-40 Hz)")
    ax.grid(alpha=.25); ax.legend()
    fig.savefig(output, dpi=160); plt.close(fig)


def main() -> None:
    args = get_args()
    target = args.output
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"Output must be a new or empty directory: {target}")
    paths = get_paths(args)
    raws = {"EO": read_file(paths[0]), "EC": read_file(paths[1])}
    if args.source == "physionet":
        from mne.datasets import eegbci
        for raw in raws.values():
            eegbci.standardize(raw)
            raw.set_montage(mne.channels.make_standard_montage("standard_1005"),
                            on_missing="ignore", verbose="ERROR")
    sf = {round(float(r.info["sfreq"]), 5) for r in raws.values()}
    if len(sf) != 1:
        raise ValueError(f"Sampling frequency differs between conditions: {sf}")
    channel = choose_channel(raws, args.channel)
    target.mkdir(parents=True, exist_ok=True)
    qc = {}; psds = {}; powers = {}; freqs_last = None
    chart_signal(raws, channel, target/"01_raw_eeg.png")
    for name, raw in raws.items():
        qc[name] = amplitude_screen(raw, channel)
        _, freqs, psd, power = compute_welch(raw, channel)
        if freqs_last is not None and not np.array_equal(freqs_last, freqs):
            raise ValueError("Incompatible spectral frequency grids")
        freqs_last = freqs; psds[name] = psd; powers[name] = power
    chart_psd(freqs_last, psds, channel, target/"02_welch_psd.png")
    with (target/"03_welch_psd.csv").open("w", encoding="utf-8", newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["frequency_hz", "EO_uv2_per_hz", "EC_uv2_per_hz"])
        writer.writerows(zip(freqs_last, psds["EO"], psds["EC"]))
    outcome={
        "data_kind": ("public empirical EEG" if args.source == "physionet"
                      else "local recording, empirical status unverified"),
        "data_source": "PhysioNet EEGMMIDB v1.0.0" if args.source == "physionet" else "local recordings (provenance supplied by operator)",
        "provenance": {name: {"input_filename": path.name,"sha256":sha256(path),
                              "n_channels":len(raws[name].ch_names),
                              "sfreq_hz":raws[name].info["sfreq"],
                              "duration_seconds":raws[name].times[-1]} for name,path in zip(("EO","EC"),paths)},
        "analysis": {"channel": channel, "bandpass_hz": [1,40], "alpha_hz": [8,13],
                     "welch_n_fft":256,"welch_n_overlap":128,
                     "artifact_handling":"flagged amplitude windows, none automatically rejected",
                     "units_raw":"V", "units_psd":"µV²/Hz"},
        "qc": qc,"alpha_power_uv2":powers,
        "versions":{"python":platform.python_version(),"mne":mne.__version__,
                    "numpy":np.__version__},
        "limitations":["EO and EC are separate runs, not a randomized comparison",
                       "single participant demonstration; no statistical inference",
                       "no EOG/EMG decomposition; amplitudes only screened",
                       "bandpass and channel selection can influence PSD",
                       "not a clinical or diagnostic output"]}
    (target/"04_manifest.json").write_text(json.dumps(outcome,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"output":str(target),"channel":channel,"alpha_power_uv2":powers,
                      "flagged_windows":{k:v['flagged_windows'] for k,v in qc.items()}},ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
