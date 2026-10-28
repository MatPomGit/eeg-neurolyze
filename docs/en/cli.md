# Command-line reference

Run all commands from the repository root in an isolated Python 3.12 environment:

```powershell
.\.venv\Scripts\python.exe -m eeg_athenalyze --help
```

## Synthetic data and reporting

| Command | Purpose |
|---|---|
| `synthetic-record` | Generate synthetic EEG and immutable `.eegz` archive |
| `experiment run eyes-open-closed` | Reproducible synthetic EO/EC study |
| `analyze --session FILE` | Reanalyze saved EO/EC and generate HTML |
| `plot --session FILE --view trace|psd|spectrogram|all` | Signal and spectral plots |

```powershell
.\.venv\Scripts\python.exe -m eeg_athenalyze experiment run eyes-open-closed --output data\demo --seed 42 --duration-scale 0.05
```

## EEG-BIDS

```powershell
.\.venv\Scripts\python.exe -m pip install ".[bids]"
.\.venv\Scripts\python.exe -m eeg_athenalyze bids export --session data\demo\RECORDING.eegz --dataset data\bids\ds-synthetic-v1
.\.venv\Scripts\python.exe -m eeg_athenalyze bids validate --dataset data\bids\ds-synthetic-v1
```

The exporter supports **synthetic EEG only**. An additional `bids derivatives` command writes custom alpha derivatives; full BIDS Derivatives conformity is a separate verification gate. A successful export does not replace official validation.

## Developmental hardware commands

```powershell
.\.venv\Scripts\python.exe -m pip install ".[muse]"
.\.venv\Scripts\python.exe -m eeg_athenalyze devices check --device muse-athena
.\.venv\Scripts\python.exe -m eeg_athenalyze record --device muse-athena --duration 30 --output data\local\run-new.eegz
```

The physical adapter will not silently substitute simulated EEG. Physical signal and timing quality nevertheless remain **unverified**. Additional `devices openmuse` and `devices assess` commands are available; see the [Muse guide](muse-athena.md).

Public EDF analysis is a [separate MNE Python script](real-eeg.md), not a supported import operation for the native archive.
