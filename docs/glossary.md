# Terminologia EEG Neurolyze

[Indeks](index.md) | [Standard języka](development/writing-standards.md) | [Reprodukowalność](research/reproducibility.md)

| Termin | Angielski | Definicja i uwaga |
|---|---|---|
| EEG | Electroencephalography | Rejestracja aktywności elektrycznej; sam pomiar nie jest rozpoznaniem klinicznym |
| EO / EC | Eyes open / eyes closed | Warunki z otwartymi i zamkniętymi oczami; zachowaj rzeczywiste czasy warunków |
| PSD | Power spectral density | Gęstość widmowa mocy; określ jednostkę, metodę i długość okna |
| EEG-BIDS | Brain Imaging Data Structure for EEG | Ustandaryzowana struktura danych i metadanych; wymaga walidacji konkretnego zbioru |
| EDF | European Data Format | Format danych, nie dowód poprawnej rejestracji |
| LSL | Lab Streaming Layer | Transport strumieni i metadanych czasu; nie gwarantuje fizycznej synchronizacji |
| BLE | Bluetooth Low Energy | Transport radiowy; hostowy jitter nie jest automatycznie dowodem utraty pakietu |
| Znacznik czasu źródła | Source timestamp | Czas przypisany przez faktyczny podsystem; dokumentuj pochodzenie i domenę zegara |
| Pochodzenie danych | Data provenance | Źródło, transformacje, konfiguracje, wersje, checksum i ścieżka do wyniku |
| Powtarzalność | Repeatability | Ponowne wykonanie w określonych niezmienionych warunkach; definiuj według standardu badania |
| Reprodukowalność | Reproducibility | Odtworzenie wyników na podstawie udokumentowanego procesu; podaj standard rozróżniający terminy |
| QC | Quality control | Kontrola jakości: metryki i kryteria, nie utożsamiaj z walidacją aparatury |
| BrainVision | BrainVision Core Data Format | Jeden z dopuszczalnych formatów EEG w BIDS, wymaga poprawnych metadanych |

Nazwy fizycznych elektrod TP9/AF7/AF8/TP10 nie oznaczają automatycznie zweryfikowanego położenia/referencji konkretnego urządzenia. Zmiany interpretacji terminów wymagają źródła i spójnej aktualizacji tekstów PL/EN. Szczegóły: [ADR-0002](architecture/adr/0002-bids-data-contract.md).
