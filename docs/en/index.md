# English documentation

**EEG Neurolyze** is a local-first EEG workflow for synthetic experiments, archive integrity, quality review, spectrum analysis, and EEG-BIDS interoperability.

## Read in order

1. [Quick start](quickstart.md): synthetic eyes-open/eyes-closed recordings.
2. [Processing architecture](workflow.md): source → metadata → QC → PSD → provenance.
3. [EEG-BIDS](bids.md): synthetic-only export and the official validator.
4. [Real EEG demonstration](real-eeg.md): public PhysioNet EDF and conditional local recordings.
5. [Presentation materials](presentation.md): concise slides and supplementary live-demo workflows.

## Verification boundaries

Synthetic EO/EC generation, checksummed archives and analysis are implemented; a Muse S Athena acquisition adapter also exists but **physical acquisition quality has not been independently validated**. Real EDF analysis is supplied as a separate MNE-based pipeline and does not imply a verified real-data import feature in the main application.

See the [project roadmap](../architecture/ROADMAP.md) and [ADRs](../architecture/adr/README.md) for delivery and evidence gates.
