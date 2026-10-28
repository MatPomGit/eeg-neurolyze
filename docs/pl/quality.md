# Kontrola jakości i reprodukowalność

## Bramki dowodowe

| Etap | Co należy potwierdzić | Co nie wynika z samego etapu |
|---|---|---|
| Uruchomienie kodu | testy i brak wyjątków | poprawność fizycznego EEG |
| Integralność | archiwum i SHA-256, ciągłość próbek | brak artefaktów |
| Metadane | kanały, Hz, referencja, jednostki, źródło zdarzeń | dokładność urządzenia |
| QC | analiza amplitud, przerw, szumów, EOG/EMG | pełne oczyszczenie sygnału |
| Przetwarzanie | filtracja, Welch, okna, parametry | kliniczna trafność wyniku |
| EEG-BIDS | BIDS Validator i odczyt porównawczy MNE | naukowa prawdziwość pomiaru |
| Wyniki | kod, manifest, wersje, SHA-256, raport | generalizacja na populację |

!!! warning "Ochrona danych"
    Nie commituj danych uczestników, identyfikatorów urządzeń ani sekretów. Poza Git powinny pozostać realne EDF, `.eegz`, raporty i manifesty potencjalnie zawierające metadane osobowe.

## Krytyczne różnice

- **Dane syntetyczne:** służą testom i demonstracji interfejsu, nie są pomiarem człowieka.
- **Publiczne EEG:** pozwala wykonać analizę empirycznych danych, ale bez roszczeń do własnej akwizycji.
- **Własna akwizycja:** musi mieć udokumentowaną weryfikację aparatury, czasu i jakości.
- **Walidator BIDS:** kontroluje strukturę i metadane, nie rozpoznaje fizjologicznej prawdziwości sygnału.

## Minimalny raport analizy

1. Źródło danych i licencja/zgoda; SHA-256 plików.
2. Liczba kanałów, Hz, referencja, jednostki i protokół EO/EC.
3. Kontrole jakości i informacje o odrzuconych lub tylko oznaczonych oknach.
4. Filtry, PSD, zakresy pasm i parametry segmentacji.
5. Wersje oprogramowania, skrypt, datę, wynik walidatora (jeżeli stosowany).
6. Ograniczenia wnioskowania, bez twierdzeń diagnostycznych.

Zobacz [pipeline rzeczywistego EEG](real-eeg.md), [ADR-0002](../architecture/adr/0002-bids-data-contract.md).
