# Quality control and reproducibility

| Gate | Evidence | Not implied |
|---|---|---|
| Software | Executed tests, exact version | Physical EEG accuracy |
| Raw signal | Checksummed original, continuous samples | Artifact-free data |
| Metadata | Channels, sampling, reference, units | Measured timing precision |
| QC | Noise, EOG/EMG and packet-gap review | Perfect artifact correction |
| Processing | Filters, Welch PSD, segment settings | Clinical inference |
| EEG-BIDS | Official BIDS Validator and MNE read-back | Physiological validity |
| Reporting | SHA-256, source, code, version, limits | Population generalization |

!!! warning "Participant privacy"
    Do not commit participant recordings, pseudonym keys, device IDs, or sensitive reports. Keep empirical files outside Git.

## Minimal reproducible record

Document the data origin and license/consent, original-file checksums, sampling rate, montage/reference, units, EO/EC condition, QC flags and exclusions, filter parameters, Welch settings, package versions, and BIDS validation output when relevant.

**Synthetic is not empirical.** Public recordings are real data acquired by others; they do not prove local hardware functionality. The independent MNE example and the application’s synthetic BIDS exporter have separate requirements.

See [real-data analysis](real-eeg.md), [BIDS contract ADR](../architecture/adr/0002-bids-data-contract.md).
