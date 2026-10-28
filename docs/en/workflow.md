# Acquisition and analysis architecture

EEG Neurolyze separates signal acquisition, immutable archives, preprocessing, and verifiable reports.

```mermaid
flowchart TD
 A["Synthetic eyes-open/eyes-closed"] --> D["Immutable .eegz + SHA-256"]
 B["Muse S Athena: hardware gate open"] --> D
 D --> E["Analysis and HTML report"]
 D --> F["Synthetic-only MNE-BIDS export"]
 F --> G["Official BIDS Validator and read-back"]
 C["PhysioNet EDF+ or local EDF/VHDR/FIF"] --> H["Separate MNE example"]
 H --> I["QC / 1–40 Hz / Welch PSD"]
 I --> J["PNG, CSV and JSON provenance"]
```

## Reproducibility layers

| Layer | Content | Requirement |
|---|---|---|
| Raw | EEG samples, timestamps, event source | Preserve original, never overwrite |
| Context | channel names, units, reference and sample rate | Document unknown values, do not invent |
| QC | channel integrity, artifact screening, time gaps | Explain and log exclusions |
| Analysis | filters, Welch PSD, alpha (8–13 Hz) | Log exact choices and library versions |
| Reporting | PNG, CSV, JSON / checksum and source citations | Differentiate simulation from empirical data |

The application’s BIDS exporter does **not** accept arbitrary measured recordings. The independent PhysioNet pipeline does not validate the Muse device or replace a full artifact-removal workflow.

See [real data](real-eeg.md), [quality gates](quality.md), and [project architecture](../architecture/PROJECT-CONCEPT.md).
