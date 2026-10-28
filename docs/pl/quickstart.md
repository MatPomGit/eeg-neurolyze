# Pierwsze uruchomienie na Windows 11 (syntetyczne EEG)

Instrukcja dotyczy danych **syntetycznych**. Nie łączy się z opaską Muse S Athena. Moduł rejestracji Muse S Athena istnieje, ale nie przeszedł walidacji na rzeczywistym urządzeniu; PsychoPy nie jest jeszcze zintegrowane. Eksport EEG-BIDS jest dostępny **wyłącznie dla syntetycznego EEG** i wymaga niezależnej walidacji.

## Wymagania
Zainstaluj Python 3.12 dla Windows, łącznie z programem uruchamiającym `py`, oraz Git. Standardowa instalacja projektu nie powinna wymagać uprawnień administratora.

## Procedura
1. Sklonuj repozytorium: `git clone https://github.com/MatPomGit/eeg-neurolyze.git`.
2. Otwórz folder `windows` i uruchom `setup_environment.bat`. Skrypt utworzy izolowane środowisko `.venv` i zainstaluje w nim projekt.
3. Uruchom `run_synthetic_demo.bat`. Skrypt sprawdzi środowisko i przeprowadzi skrócony eksperyment EO/EC z ustalonym ziarnem losowym 42.
4. Otwórz nowy raport `.html` w katalogu `data/demo/`. Odpowiadające mu archiwum `.eegz` zawiera oryginalne próbki syntetyczne, znaczniki czasu, metadane i manifest SHA-256.
5. Aby ponownie przeanalizować istniejące nagranie, wykonaj w głównym katalogu:

   ```powershell
   .\.venv\Scripts\python.exe -m eeg_athenalyze analyze --session "data\demo\<NAZWA_ARCHIWUM>.eegz"
   ```

   Zastąp `<NAZWA_ARCHIWUM>` rzeczywistą nazwą pliku. Surowe archiwa nie są nadpisywane.

Domyślny protokół: stabilizacja (30 s), oczy otwarte (120 s), przerwa (30 s), oczy zamknięte (120 s). Demonstracja używa `--duration-scale 0.05`, aby skrócić wykonanie.

## Interpretacja
Porównaj moc pasma alfa (8–13 Hz) dla kanałów TP9, AF7, AF8 i TP10 w warunkach EO i EC. Są to dane wygenerowane programowo, a nie pomiar uczestnika badania.

## Rozwiązywanie problemów
- **Brak `py -3.12`:** zainstaluj Python 3.12 wraz z Windows Python Launcher.
- **Brak środowiska:** uruchom `setup_environment.bat`.
- **Niepowodzenie instalacji:** sprawdź dostęp do skonfigurowanego repozytorium pakietów Python.
- **Konflikt nazw:** każda sesja otrzymuje nowy identyfikator. Nie nadpisuj ręcznie archiwów.

## Standard danych
Wewnętrzny format `.eegz` z sumą kontrolną **nie jest standardem BIDS**. Dla syntetycznych archiwów dostępny jest eksport BIDS i uruchomienie oficjalnego walidatora; zobacz [instrukcję EEG-BIDS](bids.md) oraz [przykład rzeczywistych EDF](real-eeg.md).
