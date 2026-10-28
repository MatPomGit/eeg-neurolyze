# Real EEG: public PhysioNet and conditional local recordings

## Data provenance

The [PhysioNet EEG Motor Movement/Imagery Dataset](https://physionet.org/content/eegmmidb/1.0.0/) contains recordings from 109 participants, 64 EEG channels sampled at 160 Hz. The basic demonstration uses **run 1 (eyes open)** and **run 2 (eyes closed)** from participant S001. The source acquisition was performed by the dataset investigators using BCI2000; this project only re-analyzes the archived EDF+ files.

## Windows 11: run the independent MNE example

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[bids,plot]"
.\.venv\Scripts\python.exe -m pip install scipy
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source physionet --subject 1 --output data\demo\physionet-S001-EOEC-v1
```

Only baseline EDF files are downloaded; raw data stay outside Git. The pipeline generates `01_raw_eeg.png`, `02_welch_psd.png`, `03_welch_psd.csv` and `04_manifest.json` with SHA-256, software versions, channel, frequency, QC and analysis settings.

## Scientific processing choices

- Verify sampling, channel naming, units, reference and session metadata.
- Apply a **1–40 Hz** filter only to a copy of the recording.
- Flag 1 s windows with absolute amplitude above **150 µV** as a *screening heuristic*; flagged windows are not silently removed.
- Estimate PSD using Welch with `n_fft=256` and `n_overlap=128`. Evaluate alpha power (8–13 Hz); report PSD in µV²/Hz.
- A single subject is not evidence for a population effect and the workflow is not a clinical assessment.

An optional [real EDF to BIDS candidate exporter](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/export_physionet_bids.py) needs separate official BIDS validation and metadata review; it is not the application’s synthetic-only BIDS CLI.

## Local recording alternative

```powershell
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source local --eo D:\EEG\eo.edf --ec D:\EEG\ec.edf --channel AF7 --output data\demo\own-EOEC-v1
```

For EDF, BrainVision VHDR or FIF, ensure participant consent, confidentiality, actual electrode reference, units, clock and packet continuity. Do **not** claim Muse S Athena hardware validation until on-device gates are met. Internal `.eegz` files are not directly accepted by this example.

More: [quality gates](quality.md), [presentation](presentation.md), [project roadmap](../architecture/ROADMAP.md).
