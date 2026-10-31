# Delivery roadmap and verification gates

Statuses: **implemented** = code present; **verified** = relevant executed tests or hardware evidence; **planned** = not delivered. Each milestone builds a tested vertical slice; avoid broad speculative scaffolding.

| Milestone | Deliverables | Exit gate |
|---|---|---|
| M01 Core | Synthetic EO/EC, checksummed native archive, alpha comparison, HTML, Windows .venv launcher and PL/EN quickstart | Automated synthetic and Windows tests pass; native archive read-back; honest simulated labeling |
| M02 BIDS | MNE-BIDS BrainVision export, metadata/events, official validator and MNE read-back | Official validator reports no blocking errors; sample/channel/event integrity compared to native archive |
| M03 Hardware | Muse S Athena BrainFlow adapter, BLE diagnostics, true timestamp provenance and acquisition QC | On-device Windows 11 test with documented firmware/API, dropouts, time continuity and safe stop |
| M04 PsychoPy/LSL | Independent environment, Builder/API adapter, markers, timing logs, optional XDF | End-to-end synthetic marker alignment; documented latency experiment; no unverified timing claims |
| M05 Protocols | Stroop, N-back, extensible registry, behavior + EEG event mapping | Complete trial/response tests, valid BIDS events, validated instructional examples |
| M06 Education | Six full bilingual laboratories, MkDocs Pages, figures, Windows tutorials | PL/EN equivalence, link and executable-command checks |
| M07 Advanced | ERP/BCI/real-time features, additional devices as separately validated plugins | Scientific feasibility and hardware timing validation appropriate to each feature |

## Implementation snapshot: 2026-10-31
- M01: synthetic pipeline, protected `.eegz`, HTML reports, launchers and unit tests exist. The Core tests workflow for main SHA `41f62c4566e5c368c190ef1a971119ce9b60bfde` completed successfully on 2026-10-28; this does not qualify real EEG.
- M02: `src/eeg_athenalyze/bids.py` implements synthetic-only BrainVision export and official validator invocation. `derivatives.py` implements custom derivatives. Formal BIDS validity is dataset-specific; real-device source is not admitted.
- M03: BrainFlow Athena adapter, CLI, BLE diagnostics, acquisition journal, QC logic and automated offline tests exist. **On-device quality and source-clock reliability remain unverified**; track #40, #48, #53 and related Issues.
- M04-M07: psychoPy/LSL and advanced protocols remain planned. Separate PhysioNet processing is not an integrated M04 deliverable.
- Package imports retain `eeg_athenalyze`; public project is EEG Neurolyze. Naming migration requires ADR-0006.
- Potential public raw EEG privacy exposure: [Issue #81](https://github.com/MatPomGit/eeg-neurolyze/issues/81).

## Research-grade gates
1. **Data:** immutable original values and timing with checksums; interrupted session retained.
2. **Metadata:** explicit reference/units/channel provenance, experiment protocol and analysis configuration.
3. **Timing:** measured accuracy for stimulus-locked inference; otherwise mark uncertainty.
4. **BIDS:** formally validated dataset, read-back comparison, derivatives provenance.
5. **Reproducibility:** lock/constraints, seed, versions, documented reprocessing.
6. **Privacy:** pseudonymous identifiers; no accidental exposure through Git or reports.

## Next recommended implementation
Prioritize evidence-level consistency (#37), verification of the tracked EEGZ disclosure (#81), and physical Muse S Athena qualification (#40, #48, #53). Recheck the existing synthetic EEG-BIDS exporter against official rules for each dataset before any claim of compliance. Do not open a duplicate M02 implementation PR.
