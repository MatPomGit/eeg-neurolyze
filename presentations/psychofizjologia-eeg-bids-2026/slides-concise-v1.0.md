---
marp: true
theme: default
size: 16:9
paginate: true
style: |
  section { font-family: 'Aptos', 'Arial', sans-serif; color: #112136; background:#F7FAFC; padding: 56px 70px; }
  h1 { color:#073B53; font-size: 1.78em; line-height: 1.10; }
  h2 { color:#08667D; font-size: 1.25em; }
  h3 { color:#146F82; }
  strong { color:#046E83; }
  li { margin: .22em 0; font-size:.96em; }
  code, pre { background:#E8F1F5; color:#16354A; }
  blockquote { border-left: 5px solid #0B8FA1; color:#24455C; }
  footer { font-size: 12px; color:#617A8C; }
  section::after { color:#617A8C; font-size:14px; }
---

<!-- _paginate: false -->
# Od sygnału EEG do reprodukowalnych wyników badań

## EEG-BIDS · analiza w Pythonie · EEG Neurolyze

**Psychofizjologia i pomiar EEG**

Mateusz Pomianek · 2026 · wersja 1.0.0

<!-- note: Wprowadź trzy spójne wątki; zaznacz, że część live wykorzystuje symulację. -->

---

# Jedno badanie, trzy pytania

1. **Jak opisać EEG**, aby druga osoba zrozumiała zapis?
2. **Jak analizować sygnał**, aby wyniki dało się sprawdzić?
3. **Jak odtworzyć całą procedurę** przy użyciu kodu i metadanych?

**Reprodukowalność = dane + metadane + kod + parametry + wersje + kontrola jakości.**

---

# EEG: co właściwie mierzymy?

- Różnice potencjałów elektrycznych rejestrowane na powierzchni głowy.
- Sygnał zależy m.in. od montażu, odniesienia, impedancji i jakości kontaktu elektrod.
- Typowe zanieczyszczenia: EOG, EMG, ruch, zakłócenia sieciowe.
- Sama zmiana mocy pasma **nie jest rozpoznaniem klinicznym**.

**Schemat:** mózg → elektrody → wzmacniacz i ADC → próbki → analizy.

---

# Dlaczego EEG-BIDS?

**BIDS (Brain Imaging Data Structure)** porządkuje dane, nazwy plików i metadane w przewidywalnej strukturze.

- Jednoznaczny identyfikator uczestnika, zadania i sesji.
- Opis kanałów, częstotliwości próbkowania, odniesienia i zdarzeń.
- Możliwość automatycznego odczytu i walidacji.
- Oddzielenie danych pierwotnych od rezultatów przetwarzania.

Źródło: BIDS Specification, EEG modality.

---

# Struktura przykładowego zbioru EEG-BIDS

```text
ds-eeg-demo/
├── dataset_description.json
├── participants.tsv
└── sub-001/
    └── eeg/
        ├── sub-001_task-rest_eeg.vhdr
        ├── sub-001_task-rest_eeg.vmrk
        ├── sub-001_task-rest_eeg.eeg
        ├── sub-001_task-rest_eeg.json
        ├── sub-001_task-rest_channels.tsv
        └── sub-001_task-rest_events.tsv  # jeśli są zdarzenia
```

**Przykład ilustracyjny**, nie kompletny dowód zgodności. Wymagane pliki i pola zależą od danych; zgodność sprawdza oficjalny BIDS Validator.

---

# Metadane, których nie widać na wykresie

| Pole / plik | Pytanie, na które odpowiada |
|---|---|
| `SamplingFrequency` | Ile próbek na sekundę? |
| `EEGReference` | Względem czego mierzono napięcie? |
| `PowerLineFrequency` | Jakie zakłócenie sieciowe może wystąpić? |
| `channels.tsv` | Jakie kanały, jednostki i status? |
| `events.tsv` | Kiedy i co wydarzyło się podczas rejestracji? |

**Brak metadanych ogranicza interpretowalność nawet poprawnego numerycznie zapisu.**

---

# Od surowych próbek do wyniku

**Import → kontrola jakości → filtracja → ocena artefaktów → estymacja cech → raport**

- Sprawdź jednostki, kanały, częstotliwość próbkowania i zdarzenia.
- Przy filtracji jawnie zapisz typ, pasmo i parametry.
- Oceń artefakty przed interpretacją PSD.
- Zachowaj kod, wersje bibliotek i pochodzenie danych.

**Uwaga:** przetwarzanie zmienia sygnał i może wprowadzać artefakty.

---

# Przykład: oczy otwarte vs zamknięte

**Warunki:** EO (eyes open) i EC (eyes closed).

- Badamy zmiany mocy widmowej w zakresie **alfa 8–13 Hz**.
- W badaniach EEG często obserwuje się silniejszą aktywność alfa przy oczach zamkniętych, szczególnie potylicznie.
- Konieczne są jednak: wybór kanałów, kontrola artefaktów, porównywalne okna i ostrożna interpretacja.

**Pokaz EEG Neurolyze: dane syntetyczne, nie dowód empiryczny.**

---

# Analiza widmowa: metoda Welcha

1. Podziel sygnał na częściowo nakładające się okna.
2. Oblicz widmo mocy dla każdego okna.
3. Uśrednij estymaty, uzyskując PSD.
4. Porównaj moc w zdefiniowanym paśmie.

**PSD: µV²/Hz**, oś pozioma: **częstotliwość [Hz]**.

Wynik zależy od długości segmentu, okna, nakładania, odniesienia i filtracji.

---

# Python: narzędzia w praktyce

```python
import mne
from mne_bids import BIDSPath, read_raw_bids

path = BIDSPath(subject="001", task="rest",
                datatype="eeg", root="data/bids/ds-demo")
raw = read_raw_bids(bids_path=path, verbose=False)
raw.compute_psd(method="welch", fmin=1, fmax=40).plot()
```

**Warunek:** wskazany katalog zawiera poprawnie przygotowany i odczytywalny zbiór EEG-BIDS. Własny eksport należy najpierw zwalidować.

---

# EEG Neurolyze: stan faktyczny

**Dostępne w kodzie:** generowanie syntetycznego EO/EC, archiwum `.eegz` z sumami SHA-256, raport HTML, wykresy sygnału / PSD, eksport syntetycznego EEG do BrainVision-BIDS, polecenie walidatora, pochodne alfa.

**Niepotwierdzone:** pomiar rzeczywisty Muse S Athena, poprawność rzeczywistych zegarów i przerw BLE, wiarygodność kliniczna.

**Zasada:** symulacja ≠ pomiar człowieka; eksport ≠ walidacja.

---

# Demonstracja 8–10 minut

1. Uruchom syntetyczny eksperyment **EO/EC** z ustalonym ziarnem `42`.
2. Otwórz wynikowy raport HTML i archiwum `.eegz`.
3. Narysuj przebieg i PSD z `plot --view psd`.
4. Wykonaj eksport `bids export` do **nowego** katalogu.
5. Uruchom `bids validate`; omów wynik oraz strukturę plików.

Pełne polecenia i plan awaryjny: `demo.md`.

---

# Co może pójść nie tak?

- Artefakty i referencja zmieniają amplitudy i widma.
- Błędne jednostki lub zdarzenia zniekształcają interpretację.
- Poprawna struktura plików nie gwarantuje rzetelności pomiaru.
- Wynik symulacji nie jest empirycznym potwierdzeniem hipotezy.
- Walidator sprawdza standard danych, a nie prawdziwość zarejestrowanego EEG.

**Reprodukowalny wynik nie musi być automatycznie wynikiem wiarygodnym.**

---

# Wnioski

**EEG-BIDS** opisuje i porządkuje zapis.

**Python i MNE** umożliwiają jawne, odtwarzalne przetwarzanie.

**EEG Neurolyze** łączy demonstrację analizy i eksportu na danych syntetycznych; walidacja rzeczywistego pomiaru jest odrębnym zadaniem.

**Zasada końcowa:** zapisuj źródła danych, parametry, wersje i ograniczenia.

Źródła: BIDS EEG specification · MNE-BIDS documentation · PhysioNet EEGMMIDB · projekt eeg-neurolyze.
