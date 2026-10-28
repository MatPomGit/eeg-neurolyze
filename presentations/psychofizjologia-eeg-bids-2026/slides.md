---
marp: true
theme: default
size: 16:9
paginate: true
style: |
  section { font-family: 'Arial', sans-serif; background: #F7FAFC; color: #112136; padding: 55px 70px; }
  h1 { font-size: 1.65em; color: #073B53; }
  h2 { font-size: 1.2em; color: #08667D; }
  code, pre { background: #E6F0F5; }
  strong { color: #056F83; }
---

# Od sygnału EEG do reprodukowalnych wyników badań

Psychofizjologia i pomiar EEG · EEG-BIDS · Python / MNE · EEG Neurolyze

Mateusz Pomianek · 2026 · v1.1.0

---

# Jedno badanie, trzy pytania

**Jak pozyskano EEG?** Aparatura, kanały, referencja, protokół.

**Jak przetworzono sygnał?** QC, filtracja, artefakty i PSD.

**Jak odtworzyć wynik?** Dane, metadane, parametry, wersje i kod.

---

# Co właściwie mierzy EEG?

Sygnał stanowią różnice potencjału między elektrodami i odniesieniem.

**Bioelektryczność → elektrody → wzmacniacz/ADC → sygnał → analiza.**

Kontrolujemy referencję, montaż, jakość kontaktu, EOG, EMG i zakłócenia.

---

# Dlaczego EEG-BIDS?

- Jednolite nazewnictwo zbiorów i plików.
- Opis metod i danych za pomocą JSON/TSV.
- Automatyczne wyszukiwanie oraz walidacja.
- Reprodukowalność, a **nie gwarancja jakości klinicznej**.

---

# Jak wygląda EEG-BIDS?

~~~text
ds-eeg-demo/
  dataset_description.json
  participants.tsv
  sub-001/eeg/
    sub-001_task-rest_eeg.vhdr
    sub-001_task-rest_eeg.vmrk
    sub-001_task-rest_eeg.eeg
    sub-001_task-rest_eeg.json
    sub-001_task-rest_channels.tsv
~~~

Przykład struktury dla plików BrainVision; wymagane metadane zależą od przypadku.

---

# Metadane ważniejsze niż sama nazwa pliku

**SamplingFrequency**: Hz; **EEGReference**: system odniesienia.

**PowerLineFrequency**: Hz lub jawnie brak wiedzy.

**channels.tsv**: nazwy, typy, jednostki.

**events.tsv**: znaczniki i nazwy zdarzeń, gdy są potrzebne.

---

# Od surowych próbek do wyniku

**Import → QC → filtrowanie → ocena artefaktów → Welch PSD → raport**

Każda transformacja jest jawna i przypisana do danych źródłowych. Oryginały pozostają nienaruszone.

---

# Dwa źródła danych

**Plan A:** historyczne rzeczywiste zapisy EEG Motor Movement/Imagery Dataset z PhysioNet.

**Plan B:** własny EEG, tylko po udokumentowanej walidacji hardware i kontroli jakości.

Warianty mają wspólny pipeline, lecz różne wymagania dotyczące akwizycji.

---

# PhysioNet EEG Motor Movement/Imagery Dataset

**109 osób, 64 kanały, 160 Hz, EDF+**.

**Run 1:** spoczynek, oczy otwarte (EO).

**Run 2:** spoczynek, oczy zamknięte (EC).

**Run 4:** osobne zadanie wyobrażania ruchu dłoni, nie mylić z EO/EC.

Źródło: https://physionet.org/content/eegmmidb/1.0.0/ .

---

# Historyczny łańcuch akwizycji

**Uczestnik → elektrody → wzmacniacz/ADC → BCI2000 → EDF+**.

To rekonstrukcja na podstawie dokumentacji zbioru. Nie przeprowadziliśmy tej rejestracji.

Nie zgadujemy nieznanej referencji ani parametrów sprzętowych.

---

# Python: pobranie i import

~~~python
from mne.datasets import eegbci
import mne
paths = eegbci.load_data(1, [1, 2],
                         path='data/external/eegbci',
                         update_path=False)
raw_eo = mne.io.read_raw_edf(paths[0], preload=True)
raw_ec = mne.io.read_raw_edf(paths[1], preload=True)
eegbci.standardize(raw_eo)
eegbci.standardize(raw_ec)
~~~

Pełny wykonywalny kod: `real_eeg_pipeline.py`.

---

# Kontrola jakości przed przetwarzaniem

- Nazwy kanałów, jednostki i liczba próbek.
- Częstotliwość próbkowania oraz zgodność czasu.
- Potencjalne EOG, EMG i zakłócenia.
- Próg 150 µV: tylko heurystyka przesiewowa, nie automatyczne usuwanie artefaktów.

---

# Sygnał w dziedzinie czasu

Na wykresie: **czas [s]** i **amplituda [µV]**.

Wstaw `01_raw_eeg.png` otrzymany ze skryptu na rzeczywistych EDF. Dopóki brak pobranych EDF, każda ilustracja przebiegu jest **wyraźnie oznaczona jako syntetyczna**.

---

# Filtracja i screening artefaktów

~~~python
# Pracujemy na kopii, bez zmiany pliku źródłowego
filtered = raw.copy().filter(
    l_freq=1.0, h_freq=40.0, picks='eeg')
# Screening: |x| > 150 µV w oknach 1 s
# Zapisujemy flagi, bez usuwania okien.
~~~

Dobór filtra i referencji wpływa na wyniki analizy.

---

# Metoda Welcha i moc alfa

~~~python
spec = filtered.compute_psd(
    method='welch', picks=['Oz'],
    fmin=1, fmax=40, n_fft=256,
    n_overlap=128)
psd, freq = spec.get_data(return_freqs=True)
psd_uv2 = psd * 1e12  # V²/Hz → µV²/Hz
~~~

Alfa: **8–13 Hz**; parametry muszą znaleźć się w manifeście.

---

# Porównanie EO / EC

Dla realnych danych: `02_welch_psd.png`, `03_welch_psd.csv`.

Wykres syntetyczny, jeżeli używany wyłącznie do ilustracji, musi być tak opisany. Jeden uczestnik i dwa osobne runy nie są dowodem różnicy populacyjnej.

---

# Eksport EEG-BIDS i walidacja

~~~python
from mne_bids import BIDSPath, write_raw_bids
path = BIDSPath(subject='001', task='eyesopen',
                datatype='eeg', root='data/bids/ds')
write_raw_bids(raw_eo, path, format='BrainVision',
               overwrite=False)
~~~

Do rzeczywistego eksportu użyj `export_physionet_bids.py`. **Nie zapisuj idealizowanych pozycji elektrod jako pomierzonych.** Eksport nie zastępuje oficjalnego BIDS Validator.

---

# Własna akwizycja EEG: kryteria wejścia

1. Potwierdź identyfikator urządzenia, referencję, kanały i jednostki.
2. Sprawdź BLE/dropouts, zegar, sampling i artefakty.
3. Zachowaj oryginał, uzyskaj zgodę i pseudonimizuj.
4. Dopiero wtedy eksportuj do EDF/VHDR/FIF i uruchom pipeline.

`eegz` nie jest bezpośrednio wczytywany przez skrypt.

---

# Odtwarzalny pakiet wyników

~~~text
results/
  01_raw_eeg.png
  02_welch_psd.png
  03_welch_psd.csv
  04_manifest.json
~~~

Manifest: SHA-256, kanał, sampling, filtry, parametry Welcha, QC, wersje, ograniczenia.

---

# Od akwizycji do odtwarzalnego raportu

**Akwizycja:** BCI2000/PhysioNet albo walidowany własny sprzęt.

**Przetwarzanie:** Python/MNE, QC, filtracja, PSD.

**Udostępnianie:** EEG-BIDS + metadane + provenance.

Nie deklaruj wyników empirycznych bez faktycznej analizy EDF.