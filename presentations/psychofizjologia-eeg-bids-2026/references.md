# Źródła i zakres twierdzeń

Dostęp do stron sprawdzono 2026-10-28. Materiały do wystąpienia, nie włączają chronionych grafik ani danych uczestników.

1. **BIDS Specification, Electroencephalography.** https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html (struktura EEG, sidecars, kanały, formaty).
2. **BIDS: Derivatives.** https://bids.neuroimaging.io/getting_started/folders_and_files/derivatives.html (oddzielanie wyników przetwarzania, provenance).
3. **MNE-BIDS: write_raw_bids.** https://mne.tools/mne-bids/stable/generated/mne_bids.write_raw_bids.html (eksport EEG i konwersja do BrainVision).
4. **MNE-Python: Welch PSD.** https://mne.tools/stable/generated/mne.io.Raw.html (analiza widmowa surowego EEG).
5. **PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0.** https://physionet.org/content/eegmmidb/1.0.0/ (64 kanały; 160 Hz; EO/EC w 1. i 2. runie; dane EDF+).
6. **EEG Neurolyze:** `README.md`, `docs/pl/bids.md`, `TODO.md`, `src/eeg_athenalyze/cli.py` w tym repozytorium. Stan funkcji zweryfikowany na bazie `main` `b2f5e164c62b8e53686bc08b46e5051e827d9a33`.

## Kontrola sformułowań
- „EEG Neurolyze odczytuje prawdziwe zapisy Muse S Athena” — **nie używać**, brak walidacji sprzętowej.
- „Eksport BIDS zakończył się sukcesem” — wyłącznie po uruchomieniu walidatora i zapisaniu jego wyniku.
- „EC zwiększa alfa zawsze” — **nie używać**; zależy od uczestnika, kanału i procedury.
- „Wykres alfa potwierdza badania ludzkie” — **nie używać**, w pokazie dane są syntetyczne.
- „BIDS = jakość naukowa” — **nie używać**; BIDS ułatwia organizację i reprodukowalność, nie zastępuje kontroli pomiaru.
