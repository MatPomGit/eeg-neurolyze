# Pokaz na Windows 11: syntetyczne EO/EC → EEG-BIDS

**Przed demonstracją:** lokalnie Python 3.12, klon projektu, utworzona `.venv`, biblioteki z `.[bids,plot]`; uruchomione lokalne testy. Pokaz nie łączy się z urządzeniem EEG.

W głównym katalogu repozytorium (`PowerShell`):

```powershell
.\windows\setup_environment.bat
.\.venv\Scripts\python.exe -m pip install ".[bids,plot]"
.\.venv\Scripts\python.exe -m eeg_athenalyze experiment run eyes-open-closed --output data\demo --duration-scale 0.05 --seed 42
```

Odczytaj ze standardowego wyjścia ścieżkę pliku `.eegz` utworzonego w nowej sesji. Nie zgaduj nazwy ani nie nadpisuj istniejących plików. Wstaw rzeczywistą ścieżkę w poniższych przykładach:

```powershell
$session = "data\demo\TU_WSTAW_NOWE_NAGRANIE.eegz"
$dataset = "data\bids\ds-demo-20261028-UNIKALNY-IDENTYFIKATOR"
.\.venv\Scripts\python.exe -m eeg_athenalyze analyze --session $session
.\.venv\Scripts\python.exe -m eeg_athenalyze plot --session $session --view psd --output data\demo\demo-psd.png
.\.venv\Scripts\python.exe -m eeg_athenalyze bids export --session $session --dataset $dataset
.\.venv\Scripts\python.exe -m eeg_athenalyze bids validate --dataset $dataset
```

Opcjonalnie porównaj eksport z MNE-BIDS w osobnym skrypcie, jeśli walidator przeszedł i ścieżka do zbioru jest poprawna. Polecenie `bids derivatives` jest osobnym krokiem i dotyczy własnego formatu pochodnych alfa, nie dowodu jego pełnej zgodności ze wszystkimi konwencjami BIDS Derivatives.

## Co pokazujesz
1. Raport HTML: widok EO vs EC; podpis **dane syntetyczne**.
2. Widmo PSD: jednostki na osiach, informacja o estymatorze i zakresie pasma.
3. Katalog BIDS: `dataset_description.json`, `sub-*/eeg/`, `channels.tsv`, sidecar `eeg.json`, ewentualne zdarzenia.
4. Komunikat walidatora: kod zakończenia, liczbę błędów i ostrzeżeń, wersję narzędzia (zanotować). Nie deklaruj sukcesu przed sprawdzeniem.

## Kontrole jakości / awaryjny plan
- Uruchom całość dzień wcześniej; zachowaj **lokalnie**, poza Git, plik HTML i zrzuty ekranu lub PDF dla trybu offline.
- Jeśli brak zależności, uruchom wcześniejszy raport i omów strukturę; nie maskuj błędu.
- Jeśli BIDS Validator zgłosi błąd, potraktuj go jako demonstrację procesu kontroli, nie „mały szczegół”.
- Unikaj prawdziwych danych uczestników i danych identyfikowalnych.

## Rozszerzenie po zajęciach: prawdziwy zbiór otwarty
PhysioNet EEG Motor Movement/Imagery Dataset: https://physionet.org/content/eegmmidb/1.0.0/
Run 1 = eyes open, run 2 = eyes closed; 64 kanały, 160 Hz, EDF+. Są to **oddzielne pliki rzeczywistego zapisu**, nie pliki wejściowe `.eegz` dla powyższego polecenia. Analiza wymaga osobnego skryptu MNE, kontroli metadanych, kanałów i zgód licencyjnych; nie przypisuj wyników z danych syntetycznych do PhysioNet.
