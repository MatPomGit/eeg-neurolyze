# Seminarium zaawansowane EEG-BIDS v1.2.0: metodologia i granice dowodu

## Zakres

Główna prezentacja `slides.md` ma **22 slajdy**. Zachowuje stylistykę wcześniejszej, 14-slajdowej wersji, ale usuwa wprowadzenie do podstaw EEG i opis funkcji aplikacji. Temat naukowy: **identyfikowalność wyniku EEG pod względem decyzji metodologicznych**.

Sygnał testowy w wykresach został **wygenerowany syntetycznie** przy deterministycznym ziarnie `20261028`. Nie są to pomiary ludzi ani rekonstrukcja fizjologii konkretnej osoby. Kod generujący wykresy jest dostępny w paczce źródłowej prezentacji; osobna ścieżka analizy rzeczywistego EDF znajduje się w tym repozytorium jako `real_eeg_pipeline.py`.

## Tezy analityczne

| Obszar | Co demonstrujemy | Jakich wniosków nie wyciągamy |
|---|---|---|
| 1/f a alfa | Zintegrowana moc 8–13 Hz miesza tło aperiodiczne i wąskopasmowe piki | Każdy wzrost alfa oznacza nową oscylację |
| Welch | `Δf = fs / nperseg`, kompromis rozdzielczości i liczby segmentów | Większe `nperseg` zawsze daje lepszy estymator |
| Filtracja | Przejścia i niekauzalność `filtfilt`, transjenty i ringing | Filtracja jest neutralna dla danych |
| Artefakty | Screening EOG/EMG i wpływ odrzuconych okien | Próg amplitudy automatycznie „usuwa artefakty” |
| Referencja | CAR kontra Cz jako operatory liniowe, zmiana przestrzennego rozkładu mocy | Referencja nie ma wpływu na estymatę |
| Sensitivity | Pełna siatka referencji, pasma i Welch | Można wybrać post hoc najsilniejszy efekt |
| Inferencja | Epoki i kanały tego samego uczestnika są skorelowane | 64 kanały to 64 niezależne osoby |
| BIDS | Sidecar, metadane, round-trip i walidator | Poprawny BIDS dowodzi jakości pomiaru |

## Źródła i reguły

- Pernet et al. (2019), **EEG-BIDS**, *Scientific Data* 6, 103, doi:10.1038/s41597-019-0104-8.
- [BIDS EEG Specification](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html).
- [PhysioNet EEGMMIDB v1.0.0](https://physionet.org/content/eegmmidb/1.0.0/): 109 osób, 64 kanały, 160 Hz, BCI2000; R01 EO, R02 EC, R04 motor imagery.
- [MNE preprocessing](https://mne.tools/stable/auto_tutorials/preprocessing/).
- [MNE-BIDS write_raw_bids](https://mne.tools/mne-bids/stable/generated/mne_bids.write_raw_bids.html).

## Plan podstawienia prawdziwych wyników

1. Pobierz EDF R01 i R02 dla S001 (lub użyj poprawnie zwalidowanego własnego EEG).
2. Wykonaj `real_eeg_pipeline.py`, zapisz `04_manifest.json` z SHA-256 i wynikami QC.
3. W PPTX podmień wykresy oznaczone jako syntetyczne wyłącznie na podpisane wyniki z realnego sygnału.
4. Zweryfikuj kanały, referencję, wybór pasma, artefakty, jednostki i pozycje elektrod.
5. Raportuj, które wykresy są symulacją metodologiczną, a które analizą danych empirycznych.

**Nie dodajemy żadnych wyników empirycznych bez faktycznej analizy danych.** Nie przekazujemy danych osobowych ani surowego EEG do GitHub.
