# Analiza rzeczywistego EEG: PhysioNet i dane własne

## Źródło podstawowe: PhysioNet EEG Motor Movement/Imagery Dataset

[Zbiór EEGMMIDB](https://physionet.org/content/eegmmidb/1.0.0/) udostępnia realne sygnały EEG z 109 osób (64 kanały, 160 Hz; EDF+). Do podstawowej demonstracji wykorzystywane są **run 1: oczy otwarte (EO)** oraz **run 2: oczy zamknięte (EC)** jednej osoby. Inne runy obejmują wykonywanie i wyobrażanie ruchu; nie należy ich mylić z EO/EC.

Autorzy pierwotnie zarejestrowali dane z pomocą BCI2000. Tutaj nie prowadzimy akwizycji, tylko **rekonstruujemy jej dokumentowany przebieg i samodzielnie analizujemy pliki EDF**.

## Instalacja i uruchomienie

W głównym katalogu projektu, w PowerShell i **Pythonie 3.12**:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[bids,plot]"
.\.venv\Scripts\python.exe -m pip install scipy
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source physionet --subject 1 --output data\demo\physionet-S001-EOEC-v1
```

**Uwaga:** pierwsze uruchomienie pobiera z Internetu tylko dwa runy; nie przechowujemy EDF w repozytorium Git. Każdy przebieg należy ocenić wzrokowo i sprawdzić metadane, zamiast uznawać gotowy wykres za dowód jakości.

Skrypt w repozytorium: [real_eeg_pipeline.py](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/real_eeg_pipeline.py).

## Etapy analizy

1. **Import:** `mne.datasets.eegbci.load_data(1, [1, 2])`, następnie `mne.io.read_raw_edf`.
2. **Sprawdzenie danych:** identyfikatory kanałów, wspólna częstotliwość próbkowania, jednostki, obecność artefaktów i ciągłość.
3. **Screening amplitudy:** próg 150 µV na oknach 1 s jest jedynie flagą przesiewową; żaden odcinek nie jest automatycznie odrzucany.
4. **Filtracja:** 1–40 Hz na kopii, bez modyfikowania źródła.
5. **PSD:** metoda Welcha, `n_fft=256`, `n_overlap=128`. Pasmo alfa 8–13 Hz; jednostka PSD µV²/Hz.
6. **Provenance:** SHA-256 oryginałów, wersje Pythona/MNE/NumPy, parametry i ograniczenia.

```python
from mne.datasets import eegbci
import mne

paths = eegbci.load_data(1, [1, 2])
raw = mne.io.read_raw_edf(paths[0], preload=True)
eegbci.standardize(raw)
filtered = raw.copy().filter(1., 40., picks="eeg")
spectrum = filtered.compute_psd(method="welch", fmin=1, fmax=40)
```

## Pliki wynikowe

```text
data/demo/physionet-S001-EOEC-v1/
  01_raw_eeg.png
  02_welch_psd.png
  03_welch_psd.csv
  04_manifest.json
```

Osie wykresów należy podpisywać w sekundach, µV, Hz i µV²/Hz. Porównanie EO/EC dla jednego uczestnika **nie uprawnia do wnioskowania populacyjnego ani klinicznego**.

## Opcjonalny eksport do EEG-BIDS

```powershell
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\export_physionet_bids.py --subject 1 --output data\bids\physionet-S001-v1
```

Skrypt jest osobnym przykładem MNE-BIDS, niezależnym od syntetycznego eksportera aplikacji. Wynik należy zwalidować oficjalnym BIDS Validator i sprawdzić pliki sidecar. Nie przypisuj szablonowych współrzędnych elektrod do rzeczywistych pomiarów.

## Własny zapis (wariant warunkowy)

```powershell
.\.venv\Scripts\python.exe presentations\psychofizjologia-eeg-bids-2026\real_eeg_pipeline.py --source local --eo D:\EEG\eo.edf --ec D:\EEG\ec.edf --channel AF7 --output data\demo\own-EOEC-v1
```

Obsługiwane są EDF, BrainVision VHDR i FIF. Aby wynik można było nazwać empirycznym, potwierdź: zgodę i prywatność uczestnika, montaż, referencję, rzeczywiste jednostki, próbkowanie, znacznik czasu, utraty pakietów, źródło zdarzeń i fizyczną jakość sygnału. **Muse S Athena nie przeszedł jeszcze pełnej walidacji sprzętowej.** Nie używaj `.eegz` jako wejścia do tego skryptu bez dedykowanej konwersji.

Dodatkowo: [kryteria jakości](quality.md), [prezentacja](presentation.md), [źródła naukowe](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/references.md).
