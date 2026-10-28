---
marp: true
theme: default
size: 16:9
paginate: true
style: |
  section { font-family: 'Aptos','Arial',sans-serif; background:#F6F9FC; color:#10283F; padding:52px 70px; }
  h1 { color:#071F32; font-size:1.66em; }
  h2 { color:#0F9BB0; }
  code,pre { background:#071F32; color:#F6F9FC; border-radius:6px; font-size:.72em; }
  strong { color:#087F91; }
  blockquote { border-left:5px solid #0F9BB0; color:#36536A; }
---

<!-- _paginate: false -->
# EEG-BIDS jako warunek wiarygodnej inferencji ze sygnału EEG

**Identyfikowalność · analiza widmowa · wrażliwość na decyzje metodologiczne**

Psychofizjologia i pomiar EEG · Mateusz Pomianek · 2026 · v1.2.0

---

# To samo EEG, różne efekty statystyczne

**Pytanie:** czy EC względem EO zwiększa moc alfa w okolicy potylicznej?

**Współzmienne decyzje:** referencja, pasmo, epokowanie, artefakty, filtracja, okno i kanały.

**Kryterium:** wynik musi pozostać interpretowalny po ujawnieniu całego pipeline'u.

---

# PhysioNet EEGMMIDB: przypadek kontrolny

**109 uczestników · 64 kanały · fs = 160 Hz · EDF+ · BCI2000**.

- R01: oczy otwarte (EO)
- R02: oczy zamknięte (EC)
- R04: wyobrażanie ruchu ręki (inna procedura)

Kolejność R01/R02 jest ustalona; różnicy nie należy przypisywać wyłącznie zmianie stanu oczu bez rozważenia efektu kolejności.

Źródło: https://physionet.org/content/eegmmidb/1.0.0/

---

# Dwie ścieżki akwizycji, wspólny kontrakt

**Zbiór publiczny:** BCI2000 → EDF+ → MNE → QC → BIDS.

**Rejestracja własna:** urządzenie → dane źródłowe → weryfikacja zegara i transmisji → niezmienny zapis → eksport.

W obu wariantach: identyfikator, próbki, jednostki, odniesienie, częstotliwość, zdarzenia, checksumy.

---

# Inwarianty pomiędzy formatami

| Warstwa | Metadane krytyczne |
|---|---|
| Pochodzenie | subject, task, run, identyfikator źródła, SHA-256 |
| Czas | fs, zegar, nieciągłości, zdarzenia i ich odniesienie |
| Pomiar | kanały, jednostki, gain, EEGReference |
| Transformacja | filtracja, parametry estymacji, wersje |
| Walidacja | BIDS Validator, round-trip próbki/czas/kanały |

---

# Walidacja BIDS nie waliduje fizjologii

```json
{
  "TaskName": "eyesclosed",
  "SamplingFrequency": 160,
  "EEGReference": "n/a",
  "PowerLineFrequency": "n/a",
  "SoftwareFilters": "n/a"
}
```

Pola `n/a` są przykładem **nieznanych** wartości, nie zmierzonymi parametrami.

Oficjalny walidator ocenia standard danych, a nie jakość biologiczną zapisu.

---

# Round-trip: test semantyczny

```python
from mne_bids import BIDSPath, read_raw_bids, write_raw_bids
raw0 = mne.io.read_raw_edf(src, preload=False)
path = BIDSPath(subject="001", task="eyesopen",
                datatype="eeg", root=dst)
write_raw_bids(raw0, path, format="BrainVision")
raw1 = read_raw_bids(path, verbose=False)
assert raw1.info["sfreq"] == raw0.info["sfreq"]
assert raw1.ch_names == raw0.ch_names
```

Dalsze bramki: wartości próbek z tolerancją numeryczną, zdarzenia, format i status BIDS Validator.

---

# Składowa oscylacyjna na tle aperiodicznym

Moc pasma alfa nie jest synonimem amplitudy wyizolowanego oscylatora.

Wzrost 8–13 Hz może wynikać z piku alfa **lub** przesunięcia charakterystyki 1/f.

**Ilustracja:** model syntetyczny, wykres `07_aperiodic.png` generowany przez skrypt źródłowy.

---

# Welch: rozdzielczość kontra wariancja

\(\Delta f = f_s / N_{\mathrm{seg}}\)

Przy fs = 160 Hz: segment 256 próbek → 0,625 Hz; 1024 próbek → 0,156 Hz.

Dłuższe segmenty zapewniają lepszą rozdzielczość, ale mniej prawie niezależnych estymat.

**Ilustracja syntetyczna:** dwa pobliskie piki 9,5 i 10,4 Hz.

---

# Stałe pasmo 8–13 Hz ≠ indywidualny pik alfa

- Definicja stała ułatwia powtarzalność.
- IAF pozwala dostosować pasmo, wymaga jednak niezależnej estymacji.
- Dobór pasma po obejrzeniu efektu grozi nadmiernym dopasowaniem hipotezy.

**Ilustracja syntetyczna:** PSD EO/EC w kanale potylicznym.

---

# Artefakty zmieniają estymator

EOG, EMG i przerwy mogą wywoływać zmianę PSD większą niż porównywany efekt.

- Raportuj liczbę i frakcję odrzuconych okien.
- Odrzucanie powinno wynikać z uprzednio ustalonych kryteriów QC.
- Próg amplitudy nie jest równoważny dekompozycji EOG/EMG.

**Ilustracja syntetyczna:** sygnał z epizodem EOG i PSD przed/po wykluczeniu.

---

# Filtracja ma cenę interpretacyjną

Przy filtracji pasmowej mogą wystąpić ringing i artefakty wokół transjentów.

Filtrowanie dwukierunkowe daje odpowiedź bez przesunięcia fazowego, lecz jest niekauzalne.

Rejestruj typ filtra, rząd, częstotliwości graniczne, strategię obsługi brzegów.

**Ilustracja syntetyczna:** odpowiedź filtra 1–40 Hz na impuls.

---

# Referencja EEG jest operatorem liniowym

Średnia wspólna (CAR): \(V'_i = V_i - \overline{V}\).

Odniesienie Cz: \(V'_i = V_i - V_{Cz}\).

Różne referencje zmieniają mapę mocy alfa w tym samym modelu źródłowym.

**Topografia:** syntetyczna, pozycje elektrod `standard_1020` są szablonem, nie zmierzonymi współrzędnymi.

---

# Multiverse: ujawnić wszystkie decyzje

Definiujemy siatkę **referencja × pasmo × długość okna**, a nie wybieramy najlepszego wariantu post hoc.

Zamiast pojedynczego „p” raportujemy zakres wrażliwości efektu.

**Ilustracja:** syntetyczna macierz zmian log-ratio w dB.

---

# Python 01: import rzeczywistych EDF

```python
import mne
from mne.datasets import eegbci

paths = eegbci.load_data(1, [1, 2],
    path="data/external/eegbci", update_path=False)
eo = mne.io.read_raw_edf(paths[0], preload=True)
ec = mne.io.read_raw_edf(paths[1], preload=True)
eegbci.standardize(eo)
eegbci.standardize(ec)
assert eo.info["sfreq"] == ec.info["sfreq"]
```

Pobranie EDF wymaga sieci; wykonane wykresy syntetyczne **nie** są wynikiem tego kodu.

---

# Czas i amplituda: przed filtracją

Porównanie EO/EC wykonuj przy tej samej skali amplitudy i identycznym kanale.

**Ilustracja:** syntetyczne przebiegi Oz [µV] jako model możliwego wejścia.

Po pobraniu EDF podmień na rzeczywisty wykres i zapisz SHA-256 źródeł.

---

# Python 02: PSD i jednostki

```python
from scipy.signal import welch
import numpy as np

raw = ec.copy().pick(["Oz"]).filter(1., 40.)
x_uv = raw.get_data()[0] * 1e6
f, p = welch(x_uv, fs=raw.info["sfreq"],
             nperseg=512, noverlap=256)
band = (f >= 8) & (f <= 13)
power_uv2 = np.trapezoid(p[band], f[band])
```

Jednostki PSD: µV²/Hz, zintegrowanej mocy: µV². Odrzucenia QC udokumentuj przed oszacowaniem.

---

# Niepewność: pseudoreplikacja

\(\Delta_\alpha = 10\log_{10}(P_{\alpha, EC}/P_{\alpha, EO})\) [dB].

Okna i kanały tej samej osoby **nie są niezależnymi jednostkami biologicznymi**.

W modelu populacyjnym jednostką niezależną jest uczestnik, nie epoka.

---

# Python 03: eksport źródłowego EEG-BIDS

```python
from mne_bids import BIDSPath, write_raw_bids
raw = mne.io.read_raw_edf(paths[0], preload=False)
eegbci.standardize(raw)
bids = BIDSPath(subject="001", task="eyesopen",
                datatype="eeg", root="data/bids/ds-example")
write_raw_bids(raw, bids, format="BrainVision",
               overwrite=False)
```

Walidacja BIDS i przegląd metadanych następują **po** eksporcie. Nie zapisuj zmienionych próbek jako surowych danych.

---

# Bramki wejścia dla własnego EEG

1. Transport, zerwania transmisji i stabilność zegara.
2. Gain, jednostki, mapowanie kanałów i system referencyjny.
3. Znaczniki protokołu EO/EC i kolejność warunków.
4. Artefakty EOG/EMG i kontrola jakości fizjologicznej.
5. SHA-256, niezmienność źródła, zgoda i pseudonimizacja.

Brak dowodu poprawnego pomiaru → prezentować PhysioNet, **nie** symulację jako rejestrację.

---

# Demonstracja: jedna rejestracja, pełny ślad

**01** Otwórz EDF, metadane i checksumy.

**02** Oceń sygnał, amplitudę i artefakty.

**03** Oblicz PSD, rozważ 1/f, sprawdź alfa.

**04** Zmień pasmo, referencję i okno estymacji.

**05** Odtwórz manifest, BIDS, walidator i raport.

Oprogramowanie jest narzędziem demonstracyjnym, a nie przedmiotem wykładu.

---

# Wynik naukowy = estymata + kontrakt danych + test odporności

**Wnioski:** BIDS wspiera interoperacyjność; decyzje przetwarzania wpływają na efekt; bez danych źródłowych i manifestu nie ma pełnej reprodukowalności.

**Źródła:**

Pernet et al. (2019), *Scientific Data*, 6:103, doi:10.1038/s41597-019-0104-8.

PhysioNet EEGMMIDB v1.0.0, https://physionet.org/content/eegmmidb/1.0.0/.

MNE Preprocessing, https://mne.tools/stable/auto_tutorials/preprocessing/.

MNE-BIDS, https://mne.tools/mne-bids/stable/generated/mne_bids.write_raw_bids.html.

Wykresy: autorska symulacja, seed=20261028; brak danych uczestników.
