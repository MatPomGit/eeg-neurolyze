# Od sygnału EEG do reprodukowalnych wyników badań

**Wersja 1.1.0 · 2026-10-28 · Psychofizjologia i pomiar EEG**

Prezentacja 16:9 na około 30–35 minut. Zakres: łańcuch akwizycji EEG, EEG-BIDS, import i kontrola jakości, Python / MNE, filtracja, artefakty, PSD oraz demonstracja wyników.

## Dwa scenariusze danych

**Plan A (podstawowy):** PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0, osoba S001: run 1 = eyes open, run 2 = eyes closed. Są to dane rzeczywiste z historycznej rejestracji BCI2000 (64 EEG, 160 Hz, EDF+). Zajęcia obejmują **rekonstrukcję procesu akwizycji** i własne odtwarzalne przetwarzanie, nie fizyczne powtórzenie pomiaru.

**Plan B (warunkowy):** własne EEG. Możliwy tylko gdy przed prezentacją zostanie zebrane i zweryfikowane, z zachowanym pochodzeniem, parametrami sprzętu, zgodą, jednostkami, referencją, znacznikami czasu i kontrolą artefaktów. Nie stwierdzamy, że urządzenie Muse S Athena zostało zwalidowane.

## Pliki

- [Slajdy Marp, 20 slajdów](slides.md).
- [Notatki prowadzącego](speaker-notes.md).
- [Scenariusz przeprowadzenia pokazu i komendy](demo.md).
- [Wykonywalny pipeline dla realnego EDF lub lokalnego EEG](real_eeg_pipeline.py).
- [Offline smoke test na sygnale wytworzonym w kodzie](test_pipeline.py).
- [Źródła naukowe i prawa do danych](references.md).

## Uruchomienie end-to-end

W katalogu głównym repozytorium, z Pythonem 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[bids,plot]"
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source physionet --subject 1 --output data\demo\physionet-S001-EOEC-v1
```

Po zakończeniu powstaną 2 wykresy PNG, CSV z PSD oraz JSON z parametrami i SHA-256. Skrypt pobiera wyłącznie dwie sesje bazowe. Wymaga połączenia z PhysioNet przy pierwszym uruchomieniu. **W tym środowisku nie pobrano rzeczywistych EDF**, dlatego slajdy 13 i 16 zawierają jawnie podpisane ilustracje syntetyczne. Należy zastąpić je wygenerowanymi figurami **dopiero po faktycznym wykonaniu analizy**.

## Reprodukowalność i prywatność

Surowe pliki EEG, własne nagrania i dane uczestników pozostają lokalnie, poza kontrolą wersji. Nie nadpisuj oryginałów i nie dopisuj brakującej aparatury/referencji do metadanych. Kod, artefakty i wyniki eksperymentu nie zastępują walidacji sprzętowej ani klinicznej.

## Generowanie prezentacji

`slides.md` jest źródłem Marp (16:9), które można eksportować do PPTX/PDF darmowym Marp CLI. Graficzna wersja PPTX v1.1.0 i PDF została przygotowana jako artefakt rozmowy; repozytorium zachowuje edytowalne źródła, instrukcje oraz Python.
