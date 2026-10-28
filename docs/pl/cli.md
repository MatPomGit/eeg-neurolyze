# Interfejs CLI: dostępne polecenia

Wszystkie przykłady uruchamiaj z głównego katalogu repozytorium, w izolowanym Pythonie 3.12:

```powershell
.\.venv\Scripts\python.exe -m eeg_athenalyze --help
```

Poniższe funkcje są zaimplementowane w `src/eeg_athenalyze/cli.py`, ale nie wszystkie zostały zweryfikowane na sprzęcie.

## Symulacja i analiza

| Polecenie | Znaczenie |
|---|---|
| `synthetic-record` | Generowanie syntetycznego EEG i zapis `.eegz` |
| `experiment run eyes-open-closed` | Protokół syntetyczny EO/EC (raport + archiwum) |
| `analyze --session FILE` | Analiza archiwalnego EO/EC i raport HTML |
| `plot --session FILE --view trace|psd|spectrogram|all` | Wizualizacja sygnału lub widma |

```powershell
.\.venv\Scripts\python.exe -m eeg_athenalyze experiment run eyes-open-closed --output data\demo --seed 42 --duration-scale 0.05
```

## EEG-BIDS

```powershell
.\.venv\Scripts\python.exe -m pip install ".[bids]"
.\.venv\Scripts\python.exe -m eeg_athenalyze bids export --session data\demo\NAGRANIE.eegz --dataset data\bids\ds-synthetic-v1
.\.venv\Scripts\python.exe -m eeg_athenalyze bids validate --dataset data\bids\ds-synthetic-v1
```

Oprócz eksportu i walidacji istnieje `bids derivatives` dla własnych pochodnych alfa. Nie opisuj go jako w pełni standaryzowanego BIDS Derivatives, dopóki nie przejdzie odpowiedniej kontroli metadanych. Eksport działa wyłącznie dla syntetycznych nagrań o poprawnym próbkowaniu i jednostkach.

## Muse S Athena (rozwój)

```powershell
.\.venv\Scripts\python.exe -m pip install ".[muse]"
.\.venv\Scripts\python.exe -m eeg_athenalyze devices check --device muse-athena
.\.venv\Scripts\python.exe -m eeg_athenalyze record --device muse-athena --duration 30 --output data\local\run-new.eegz
```

Komenda `record` nie wykonuje cichej symulacji, jednak powodzenie programu nie potwierdza jakości sprzętowej. Dostępne są także `devices openmuse` i `devices assess`. Zobacz [instrukcję sprzętową](muse-athena.md).

## Rzeczywiste EDF

Oddzielny pipeline nie jest komendą `eeg_athenalyze`. Uruchom [skrypt rzeczywistego EEG](real-eeg.md) z katalogu `presentations/...`. Nie należy używać `bids export` dla rzeczywistych `.eegz`, ponieważ eksporter celowo ograniczono do danych syntetycznych.
