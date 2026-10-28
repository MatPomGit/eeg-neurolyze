# Notatki do wystąpienia · wersja 1.1.0 (2026-10-28)

**Planowany czas:** 30–35 minut, w tym 8–10 minut demonstracji. 21 slajdów. Struktura: akwizycja → EEG-BIDS → Python / MNE → rzeczywiste EO/EC → EEG Neurolyze / ograniczenia.

| Slajd | Orientacyjny czas | Komentarz prelegenta |
|---|---:|---|
| 1 | 0:30 | Zapowiedz dwa warianty źródła: rzeczywisty publiczny PhysioNet i warunkowo własny pomiar. |
| 2 | 1:00 | Od źródła pomiaru do odtwarzalnego wyniku, wspólna logika wszystkich części. |
| 3 | 1:00 | Elektrody, napięcie względem referencji, artefakty. |
| 4 | 1:00 | BIDS ułatwia porządkowanie, ale nie dowodzi jakości badania. |
| 5 | 1:15 | Drzewo BIDS i format BrainVision. |
| 6 | 1:15 | Kanały, referencja, sampling, zdarzenia; nie uzupełniaj nieznanych pól arbitralnie. |
| 7 | 1:00 | Sekwencja QC → filtracja → PSD → raport. |
| 8 | 1:15 | Plan A i B, brak automatycznej równoważności sprzętowej. |
| 9 | 1:30 | 109 osób, 64 kanały, 160 Hz; run 1/2 to EO/EC, nie zadania motor imagery. |
| 10 | 1:15 | Historyczna akwizycja BCI2000; nie jest to rejestracja wykonana przez prelegenta. |
| 11 | 1:15 | Pobranie dwóch EDF i import w MNE, dane uczestnika S001. |
| 12 | 1:15 | Screen amplitudy jest tylko kontrolą przesiewową, a nie usunięciem EOG. |
| 13 | 1:00 | Rzeczywisty przebieg po wykonaniu skryptu; jeśli nie ma EDF, ilustracja pozostaje podpisana symulacją. |
| 14 | 1:15 | Filtr 1–40 Hz, ograniczenia korekcji artefaktów. |
| 15 | 1:15 | Welch, PSD µV²/Hz, pasmo alfa 8–13 Hz i zależność od parametrów. |
| 16 | 1:15 | Podobnie: podmień wynik PSD dopiero po wykonaniu analizy na realnych danych. |
| 17 | 1:30 | Eksport źródłowego EDF do BIDS, osobno oficjalny walidator; brak idealizowanych współrzędnych jako measured. |
| 18 | 1:30 | Własny pomiar: montaż, sampling, zegary, przerwy BLE, zgoda. |
| 19 | 1:00 | Podsumowanie PNG, CSV, JSON, SHA-256 i wersji bibliotek. |
| 20 | 1:00 | EEG Neurolyze ma działający tor syntetyczny. Realny PhysioNet obsługuje oddzielny skrypt MNE. |
| 21 | 0:30 | Trzy podsystemy i ograniczenia; pytania. |

Czasy sumują się do około 25 minut samego omówienia; 8–10 minut demonstracji należy rozłożyć na slajdy 11–19 zamiast dodawać pełne 10 minut do każdego z nich.

## Demonstracja rzeczywistego sygnału

1. Przed zajęciami pobierz PhysioNet S001 run 1 i run 2 skryptem `real_eeg_pipeline.py`.
2. Zachowaj `01_raw_eeg.png`, `02_welch_psd.png`, CSV i manifest; oceń jakość wykresów.
3. Zastąp poglądowe syntetyczne wykresy na slajdach 13 i 16 wyłącznie rzeczywistymi wynikami. Podaj uczestnika, kanał, pasmo, metodę i pochodzenie.
4. Jeśli konwersja jest potrzebna, uruchom `export_physionet_bids.py`, a następnie oficjalny walidator BIDS; zachowaj raport.
5. Przy braku internetu użyj wcześniejszych **prawdziwych wyników** z lokalnego katalogu. Jeśli brak rzeczywistych wyników, wyraźnie przedstaw slajdy jako ilustracyjne, bez podawania efektu empirycznego.

## Pytania wymagające rozróżnienia

- **Czy mój software mierzył EEG?** Nie w tej demonstracji: PhysioNet to cudze publiczne dane rzeczywiste, EEG Neurolyze ma oddzielny tor syntetyczny. Własna akwizycja wymaga walidacji.
- **Czy były badania z udziałem ludzi?** W źródłowej bazie PhysioNet tak; w ramach przygotowywania tej prezentacji nie przeprowadzano odrębnego pomiaru.
- **Czy alfa w EC zawsze rośnie?** Nie, zależy od osób, kanału i jakości sygnału. Dla jednego uczestnika nie ma wnioskowania populacyjnego.
- **Czy wykres z komputera jest dowodem jakości?** Nie; trzeba udokumentować jednostki, EOG/EMG, timing i parametry przetwarzania.
- **Czy BIDS gwarantuje poprawny pomiar?** Nie. Walidator sprawdza strukturę/metadane, nie wiarygodność fizjologiczną.

Odniesienia do źródeł: `references.md`. W repozytorium nie zapisujemy danych uczestników.
