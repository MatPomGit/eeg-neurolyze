# Prezentacja: EEG-BIDS, Python i EEG Neurolyze

**Preferowany format:** krótka, spójna prezentacja koncepcyjna; zaawansowane szczegóły kodowe i realne EDF są udokumentowane tutaj, a nie umieszczane na każdym slajdzie.

## Wariant główny: 14 slajdów

Zachowano pierwszą koncepcję graficzną i narracyjną, z trzema osiami:

1. **EEG-BIDS:** struktura zbiorów, metadane, walidacja i reprodukowalność.
2. **Praktyczna analiza:** import, filtry, artefakty, PSD, porównanie EO/EC.
3. **EEG Neurolyze:** demonstracja istniejących funkcji oprogramowania; symulacja jest jawnie oznaczona.

- [Źródła 14 slajdów (Marp)](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/slides.md).
- [Notatki prelegenta](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/speaker-notes.md).

## Materiały rozszerzone (nie zastępują głównej prezentacji)

- [21-slajdowy aneks techniczny](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/slides-detailed-v1.1.md).
- [Scenariusz demonstracji](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/demo.md).
- [Analiza PhysioNet w Pythonie](real-eeg.md), [walidacja i reprodukowalność](quality.md).

## Praktyczny pokaz

**Wariant A (pewny):** lokalny syntetyczny EO/EC + raport HTML i kontrolowany eksport do BIDS.

**Wariant B (warunkowy):** po pobraniu EDF z PhysioNet zamiana poglądowych obrazów na prawdziwe wykresy wygenerowane przez MNE. Jeżeli własne EEG zostanie poprawnie zebrane i zwalidowane, może zastąpić PhysioNet.

Nie zamieniaj na slajdzie podpisu „symulacja” na „pomiar” bez faktycznej zmiany źródła danych i udokumentowania akwizycji. Zawsze stosuj podpisy osi i jednostki.
