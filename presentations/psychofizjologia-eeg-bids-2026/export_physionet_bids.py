#!/usr/bin/env python3
"""Export PhysioNet EEGMMIDB baseline EDF to a BIDS candidate.

Output needs official BIDS Validator review. No electrode coordinates are
invented: a template montage must not be used as measured positions.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import mne


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", type=int, default=1)
    parser.add_argument("--cache", type=Path, default=Path("data/external/eegbci"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--line-frequency", type=float,
                        help="Measured/confirmed mains frequency in Hz; leave unset if unknown")
    args = parser.parse_args()
    if not 1 <= args.subject <= 109:
        raise ValueError("subject must be 1..109")
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError(f"Expected new/empty BIDS destination: {args.output}")
    try:
        from mne_bids import BIDSPath, write_raw_bids
    except ImportError as error:
        raise SystemExit("Install project optional dependencies: pip install '.[bids]'") from error
    from mne.datasets import eegbci
    args.cache.mkdir(parents=True, exist_ok=True)
    paths = eegbci.load_data(args.subject, [1, 2], path=args.cache, update_path=False)
    by_run = {int(Path(item).stem[-2:]): Path(item) for item in paths}

    for run_id, task in ((1, "eyesopen"), (2, "eyesclosed")):
        raw = mne.io.read_raw_edf(by_run[run_id], preload=False, verbose="ERROR")
        eegbci.standardize(raw)
        # Do NOT attach a template montage: BIDS electrodes.tsv is for measured coordinates.
        if args.line_frequency is not None:
            raw.info["line_freq"] = args.line_frequency
        dest = BIDSPath(subject=f"{args.subject:03d}", task=task,
                        datatype="eeg", root=args.output)
        write_raw_bids(raw, dest, format="BrainVision", overwrite=False,
                       verbose="ERROR")
        print(f"BIDS candidate for run {run_id}: {dest}")

    print("Run the official BIDS Validator and review sidecars/unknown metadata.")
    print("No physical acquisition or scientifically validated EEG is claimed.")


if __name__ == "__main__":
    main()
