# Zaawansowane seminarium: EEG-BIDS i inferencja ze sygnału EEG

**Prezentacja główna v1.2.0 · 22 slajdy · 2026-10-28 · Psychofizjologia i pomiar EEG**

Ta wersja koncentruje się na zaawansowanej metodologii i analizie wrażliwości wyników EEG, a nie na podstawach EEG ani opisie oprogramowania.

## Materiały

- [Źródło prezentacji Marp v1.2.0 (22 slajdy)](slides.md).
- [Notatki prelegenta v1.2.0](speaker-notes-advanced-v1.2.md).
- [Metodologia, bramki weryfikacji i bibliografia](advanced-methodology.md).
- [Archiwalna krótka prezentacja v1.0.0](slides-concise-v1.0.md).
- [Archiwalna wersja techniczna v1.1.0](slides-detailed-v1.1.md).
- [Pipeline dla rzeczywistych PhysioNet EDF i lokalnego EEG](real_eeg_pipeline.py).
- [Eksport źródłowego EDF do kandydata BIDS](export_physionet_bids.py).
- [Smoke test na syntetycznych FIF](test_pipeline.py).
- [Scenariusz demonstracji danych rzeczywistych](demo.md).

## Zakres zaawansowanej analizy

Komponent aperiodiczny 1/f vs piki alfa, kompromis parametrów Welcha, IAF, artefakty EOG/EMG, cechy filtracji, odniesienie CAR/Cz, analiza multiverse, PSD z kontrolą jednostek, pseudoreplikacja, round-trip MNE-BIDS oraz walidacja pochodzenia danych.

**Wykresy metodologiczne w plikach PPTX/PDF w bieżącej wersji oparto na danych syntetycznych.** Odtwarzalny skrypt i osiem źródłowych obrazów zostały dostarczone w paczce źródłowej razem z gotową prezentacją. Żaden z nich nie jest przedstawiany jako wynik PhysioNet lub własnego badania. Gotowe pliki PPTX/PDF są oddzielnymi artefaktami rozmowy; w repozytorium przechowujemy edytowalną treść Marp i dokumentację.

## Demonstracja realnego EEG

Wariant podstawowy: S001 z PhysioNet EEGMMIDB, R01 eyes-open i R02 eyes-closed. Oryginały EDF pochodzą z pomiaru BCI2000, przeprowadzonego przez autorów zbioru. Wariant alternatywny: własny pomiar po przejściu bramek walidacji aparatury. W obu przypadkach: metadane → QC → PSD → analiza wrażliwości → raport → ewentualna walidacja BIDS.

**Nie opisujemy możliwości własnego programu na slajdach.** Oprogramowanie może jedynie prezentować zarejestrowany sygnał i wynik analizy; brak zwalidowanej akwizycji Muse S Athena pozostaje ograniczeniem.

## Windows 11

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[bids,plot]"
.\.venv\Scripts\python.exe -m pip install scipy
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source physionet --subject 1 --output data\demo\physionet-S001-EOEC-v1
```

Przy pierwszym uruchomieniu pobierane są dwa EDF. Nie zapisuj nagrań uczestników ani danych osobowych w repozytorium.
