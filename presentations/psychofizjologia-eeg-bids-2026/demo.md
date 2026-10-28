# Demonstracja EEG na danych rzeczywistych (wersja 1.1.0)

## Dwie ścieżki

1. **Podstawowa: PhysioNet EEG Motor Movement/Imagery Dataset**, uczestnik S001; run 1 (EO) oraz run 2 (EC). To rzeczywiste sygnały 64-kanałowe (160 Hz, EDF+), pozyskane wcześniej przez autorów z wykorzystaniem BCI2000. Nie przedstawiamy ich jako własnej akwizycji.
2. **Alternatywna: własny zapis EEG** wyłącznie po rzeczywistym pobraniu danych oraz weryfikacji mapowania kanałów, referencji, jednostek, próbkowania, błędów transmisji i znaczników czasu. Dla Muse S Athena fizyczna walidacja w repozytorium pozostaje bramką otwartą.

## Przygotowanie środowiska Windows 11

W katalogu głównym repozytorium utwórz odrębne środowisko z Pythonem 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[bids,plot]"
```

Nie instaluj pakietów globalnie. Wymagana jest łączność internetowa przy pierwszym pobraniu publicznych EDF. Repozytorium nie powinno zawierać pobranych surowych danych uczestników.

## Uruchomienie na PhysioNet

```powershell
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source physionet --subject 1 --eegbci-cache data\external\eegbci --output data\demo\physionet-S001-EOEC-v1
```

Skrypt pobiera **tylko runy 1 i 2**, pozostawia oryginalne EDF bez zmian i zapisuje:

- `01_raw_eeg.png` – surowy sygnał w funkcji czasu (pierwsze 8 s obu sesji);
- `02_welch_psd.png` – widma EO i EC z zaznaczonym pasmem alfa;
- `03_welch_psd.csv` – tabelę częstotliwości i PSD w µV²/Hz;
- `04_manifest.json` – SHA-256 danych, ustawienia, kontrolę jakości, wersje bibliotek i ograniczenia.

Nie uruchamiaj skryptu do tego samego niepustego katalogu wynikowego: chroni przed nadpisaniem.

## Alternatywna rejestracja

Po walidacji sprzętu i jakości sygnału, np. w dwóch plikach EDF:

```powershell
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source local --eo D:\EEG\eyes-open.edf --ec D:\EEG\eyes-closed.edf --channel AF7 --output data\demo\local-EOEC-v1
```

Własne dane mogą używać `EDF`, `VHDR` lub `FIF`. Format `.eegz` z EEG Neurolyze **nie jest** akceptowany przez ten skrypt bez osobnej, prawidłowo zweryfikowanej konwersji. O ile elektrody są tylko czołowe / skroniowe, nie przypisuj wzorców z kanału Oz do innego montażu. Zapisy ludzi pozostają prywatne i poza Git.

## Metody i ograniczenia

- Screening: |amplituda| > 150 µV w jednosekundowych oknach. Flagi są raportowane, ale dane **nie są automatycznie odrzucane**. To nie jest usuwanie EOG/EMG.
- Filtr 1–40 Hz na kopii sygnału; estymacja Welcha `n_fft=256`, `n_overlap=128`; pasmo alfa 8–13 Hz.
- Jedna osoba i dwa odrębne runy, bez kontroli kolejności i wnioskowania populacyjnego.
- Wyniki nie mają wartości diagnostycznej; kontrolę jakości trzeba rozbudować przed analizą naukową.
- Własne dane wymagają odpowiedniej zgody i anonimizacji przed ewentualnym udostępnieniem.

## Wstawienie prawdziwych ilustracji na slajdy

Po zakończonej analizie zamień **tylko** obrazy na slajdach 13 i 16: wykresy ilustracyjne są podpisane „symulacja, nie PhysioNet”. Wstaw odpowiednio `01_raw_eeg.png` i `02_welch_psd.png`; na obu podaj numer uczestnika/warunki, kanał, metodę i pochodzenie. Nie usuwaj ostrzeżenia, dopóki nie zastąpisz grafiki rzeczywistymi wynikami.

## Scenariusz na żywo (8–10 min)

Pokaż schemat historycznej akwizycji BCI2000, oryginalny EDF, kontrolę sfreq/typów/jednostek, obraz przebiegu, filtrację i screening, PSD oraz manifest. Możesz dodatkowo otworzyć pliki BIDS i wynik **oficjalnego** BIDS Validator; eksport danych nie gwarantuje zgodności. W trybie awaryjnym korzystaj z wcześniej przygotowanych raportów na podstawie prawdziwych plików, a nie z nieoznaczonej symulacji.

## Test niezależny od internetu

```powershell
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\test_pipeline.py
```

Test wytwarza sztuczne FIF **wyłącznie do testowania kodu**. Nie należy prezentować ich jako rejestracji ludzkiej.
