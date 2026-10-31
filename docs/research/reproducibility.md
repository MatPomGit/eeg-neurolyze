# Metodologia i reprodukowalność EEG

[Badania](index.md) | [Indeks](../index.md) | [ADR-0002](../architecture/adr/0002-bids-data-contract.md)

## Poziomy dowodów

1. `PLANNED`: hipoteza i protokół, bez danych.
2. `SOFTWARE_TESTED`: syntetyczne fixture, mock, test integracyjny z dokładnym SHA.
3. `REAL_DATA_ANALYSIS`: legalnie pozyskane EDF i odtwarzalna analiza, bez deklaracji walidacji własnego sprzętu.
4. `HARDWARE_MEASURED`: wyniki na konkretnym urządzeniu, protokół, firmware i niezależne kryteria QC.
5. `DATASET_VALIDATED`: formalna walidacja struktury EEG-BIDS oraz zgodności z archiwum źródłowym na wskazanym datasecie.

Poziomy 4 i 5 mają różne cele. Żaden wynik syntetyczny, raport z mocka lub sukces CI nie jest dowodem właściwości fizjologicznych Muse S Athena. Analiza pasma alfa EO/EC z 4 elektrod czołowych i skroniowych nie uzasadnia bez osobnej walidacji wniosków klinicznych.

## Dane i zgody

Przed analizą zapisz źródło, licencję, zgodę, ograniczenia dystrybucji, pseudonimizację i politykę retencji. Nie przekazuj surowych danych człowieka do Git, CI i publicznych stron. Zachowuj archiwum źródłowe `.eegz` w bezpiecznym magazynie oraz sumę SHA-256 i metadane wersji w bezpiecznym rejestrze. Nie zastępuj źródła pochodną wersją. Dla historii publicznego artefaktu Athena, patrz [Issue #81](https://github.com/MatPomGit/eeg-neurolyze/issues/81).

## Protokół i metadane

Przy rejestracji notuj urządzenie, firmware, wersję BrainFlow, system i sterownik BLE, preset, tryb opóźnienia, fizyczne kanały, jednostki, referencję, deklarowane/zweryfikowane Hz, czas rozpoczęcia, źródło timestampów, jitter i przerwy. Jeden właściciel połączenia BLE naraz. Odróżniaj przyjście pakietu do hosta, indeks próbki, zegar sprzętowy i zegar LSL. Zwracaj uwagę na przerwy, duplikaty czasu, artefakty i stratę ciągłości. Prawidłowy checksum nie oznacza dobrej jakości sygnału.

Przy analizie zapisz skrypt, SHA, zależności, konfigurację, ziarno losowe, pipeline MNE/PSD, filtrację, epokowanie, liczbę odrzuconych okien, miary niepewności i ograniczenia. Odróżnij planowane, nieudane i wykonane próby; nie zastępuj braku danych imputacją bez protokołu. Jeśli używasz uczenia maszynowego, podział uczestnikowy/sesyjny przed strojeniem i brak przecieku train/test są obowiązkowe.

## BIDS i raporty

Syntetyczny eksport BrainVision musi mieć rzeczywiste metadane i zdarzenia, oficjalny BIDS Validator bez blokujących błędów oraz odczyt MNE dla wskazanego datasetu. Raportuj nazwę, wersję i wynik walidatora oraz równoważność kanałów, próbek, jednostek i zdarzeń. Nie nazywaj własnego archiwum `.eegz` formatem BIDS. Raw BIDS i pochodne trzymaj oddzielnie, w pochodnych zapisuj `GeneratedBy` i parametry.

## Badania fizyczne

Obowiązuje [runbook Athena](2026-10-16-athena-hardware-validation-runbook.md). Bez urządzenia i legalnej podstawy badania status to `NOT_RUN`, a nie `PASS`. Dane i manifesty z pomiarów przechowuj poza publicznym repozytorium; do Issue przenoś tylko niesensytywne, wiarygodne metryki. Nie deklaruj uogólnienia, medycznej interpretacji ani rzeczywistej dokładności zegara z symulacji.
