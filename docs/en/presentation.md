# Advanced EEG-BIDS seminar: traceability and robust inference

**Main presentation: v1.2.0, 22 slides, 16:9, approximately 30–35 minutes.** Introductory EEG material and software product descriptions have been removed.

The scientific focus is on reproducibility and methodological degrees of freedom: raw-data provenance, BIDS validation versus physiological validity, MNE-BIDS round-trip, oscillatory peaks versus the aperiodic 1/f component, Welch resolution and segment dependence, alpha-band definition, ocular/muscle artifacts, reference choice, filter transient behavior, multiverse sensitivity, and pseudoreplication of epochs/channels.

- [Main 22-slide Marp source](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/slides.md).
- [Advanced speaker notes](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/speaker-notes-advanced-v1.2.md).
- [Methodological safeguards and references](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/advanced-methodology.md).
- [Archived concise v1.0.0 source](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/slides-concise-v1.0.md).
- [Independent real EEG pipeline](real-eeg.md).

## Actual recordings versus illustrative figures

The eight methodological figures in the v1.2 PowerPoint/PDF were produced from **explicitly labeled synthetic model signals**. No empirical PhysioNet EDF was retrieved in this environment, so numerical model results must not be described as observations from a human participant. The source archive supplied with the deck contains the exact plotting script and the figure outputs.

During the practical demonstration, use actual PhysioNet EEGMMIDB baseline R01/R02 (BCI2000) or locally recorded EEG after hardware validation. Preserve sample-rate/reference/unit metadata, source SHA-256, QC outcomes, and processing parameters.

The research software should be a **tool for showing recordings**, not the subject of a presentation slide.
