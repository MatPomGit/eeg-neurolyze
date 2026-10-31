# Standardy implementacji

[Dokumentacja](../index.md) | [AGENTS.md](https://github.com/MatPomGit/eeg-neurolyze/blob/main/AGENTS.md) | [Walidacja](testing.md)

## Zakres i kontrakty

Zachowaj interfejs `eeg_athenalyze`, CLI `eeg-athenalyze`, formaty `.eegz` oraz integralność odczytu. Rozdziel moduły `recording`, `archive`, `analysis`, `muse_athena`, `bids`, `reporting`, `experiments`; nie łącz DSP z obsługą sprzętu i UI. Zmiana nazwy pakietu wymaga ścieżki migracji zgodnej z ADR-0006.

KISS, DRY, YAGNI, właściwie zastosowane SOLID i jeden kanoniczny stan. Twórz najmniejsze poprawne rozwiązanie, najpierw popraw źródło błędu. Żadnego ignorowania porażek, osłabiania testów, sztucznego formatowania całego repozytorium czy nowej zależności bez celu i kontroli ryzyka.

## Python

Docelowy Python: 3.12, deklaracja `requires-python >=3.12`. Stosuj PEP 8, 20, 257, 484 oraz PEP 517/518/621 zgodnie z rzeczywistym `pyproject.toml`. W razie potrzeby sprawdź nowsze PEP u źródła, nie twórz lockfile nieobsługiwanego przez narzędzia. Typuj nowe publiczne API i dopisuj diagnostyczne wyjątki. Nazwy funkcji i zmiennych `snake_case`, klas `CapWords`, stałych `UPPER_SNAKE_CASE`, niepublicznych pól z jednym podkreśleniem. Publiczne identyfikatory i API angielskie/ASCII. `self` i `cls` zgodnie z rolą. Miej świadomość ograniczeń typowania i zależności; nie dodawaj fałszywych stubów.

Domyślne 79 znaków kodu, 72 komentarza/docstringu, UTF-8, LF w kodzie (zachowując kompatybilność skryptów Windows). Docstringi opisują istotne kontrakty, a komentarze wyjaśniają nieoczywiste decyzje. Zachowaj lokalny styl istniejącego kodu, jeśli spójny.

## Środowisko i zależności

Uruchamiaj z katalogu repozytorium w izolowanym `.venv`, bez globalnych instalacji i automatycznych aktualizacji. `pyproject.toml` jest źródłem metadanych i zależności; `requirements-docs.txt` pinami generatora witryny. `bids`, `muse`, `plot` są opcjonalnymi grupami i nie są konieczne dla testów standardowej biblioteki.

Dla zmian w analizie dokumentuj Hz, jednostki (µV/V), referencję, filtrację i okna. W plikach archiwum zachowaj nieprzetworzone próbki, dostępny zegar, typ źródła i manifest. Nigdy nie wprowadzaj cichego przełączenia z fizycznego urządzenia na symulator. Format i kontrakty BIDS sprawdź w [ADR-0002](../architecture/adr/0002-bids-data-contract.md). Dopisz test regresyjny dla każdej naprawionej niezgodności.
