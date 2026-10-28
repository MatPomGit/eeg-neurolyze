# Od sygnału EEG do reprodukowalnych wyników badań

Prezentacja na przedmiot **Psychofizjologia i pomiar EEG** (2026), wersja **1.0.0, 2026-10-28**.

**Cel:** jedno 25–30-minutowe wystąpienie obejmujące EEG-BIDS, analizę EEG w Pythonie oraz demonstrację EEG Neurolyze.

## Materiały
- [Slajdy (źródło Marp Markdown)](slides.md), 14 slajdów, proporcje 16:9.
- [Notatki prelegenta i rozkład czasu](speaker-notes.md).
- [Scenariusz pokazu na Windows 11](demo.md).
- [Bibliografia i weryfikacja twierdzeń](references.md).

### Rendering
Otwórz `slides.md` w edytorze obsługującym Marp lub wykonaj `npx @marp-team/marp-cli slides.md --pptx` / `npx @marp-team/marp-cli slides.md --pdf` po świadomym zainstalowaniu darmowego Marp CLI. Źródło jest plikiem tekstowym; nie wymaga płatnego API. Na potrzeby prowadzącej można wyeksportować PDF z zachowaniem czytelnych podpisów i źródeł.

### Uczciwość demonstracji
Główny pokaz wykorzystuje **wyłącznie syntetyczny** model EEG, a nie pomiary człowieka. `eeg-neurolyze` ma eksport EEG-BIDS dla danych syntetycznych i walidator; tor rzeczywistej akwizycji Muse S Athena **nie przeszedł walidacji sprzętowej**, dlatego nie jest przedstawiany jako dowód empiryczny. Wynik walidacji BIDS należy zarejestrować dla konkretnego pliku i wersji walidatora. Publiczny zbiór PhysioNet jest opcjonalnym przykładem późniejszego ćwiczenia z rzeczywistymi danymi, nie stanowi źródła wykresów z symulacji.

### Struktura i ograniczenia
Nie umieszczaj identyfikowalnych danych osób badanych, zapisów EEG ani plików `.eegz` w repozytorium. Nie nadpisuj archiwów; zmieniaj nazwy lub katalogi wynikowe. Nie dodawaj globalnych zależności do projektu. Prezentacja nie jest poradą kliniczną.
