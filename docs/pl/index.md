# Dokumentacja po polsku

Dokumentacja opisuje **EEG Neurolyze** od instalacji na Windows 11 po odtwarzalną analizę i zapis EEG-BIDS.

## Od czego zacząć?

1. [Pierwsze uruchomienie](quickstart.md): syntetyczny eksperyment oczy otwarte/zamknięte (EO/EC), archiwum `.eegz` i raport.
2. [Proces przetwarzania](workflow.md): dane źródłowe, metadane, QC, filtracja, analiza PSD, weryfikacja.
3. [EEG-BIDS](bids.md): eksport syntetycznego nagrania i formalna walidacja.
4. [Rzeczywiste EEG](real-eeg.md): zapis EDF+ z PhysioNet i ewentualne własne pomiary.
5. [Prezentacja](presentation.md): krótsza prezentacja EEG-BIDS oraz rozszerzone materiały wykonawcze.

## Aktualny status

- **Dostępne:** deterministyczny eksperyment syntetyczny EO/EC, archiwizacja ze SHA-256, analiza widmowa, raport HTML, eksport syntetycznych sygnałów do EEG-BIDS, interfejs rejestracji Muse S Athena (kod).
- **Wymaga sprawdzenia:** jakość realnych zapisów Muse S Athena, referencja, jednostki i znaczniki czasu, transmisja BLE, zgodność eksportu *rzeczywistych* nagrań do BIDS.
- **Osobny przykład:** analiza rzeczywistych EDF z PhysioNet przez MNE, bez automatycznego importu EDF do wewnętrznego `.eegz`.

Pełny zakres bramek: [roadmap projektu](../architecture/ROADMAP.md).
