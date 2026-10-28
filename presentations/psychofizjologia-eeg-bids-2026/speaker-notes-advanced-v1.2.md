# Notatki prelegenta do v1.2.0

Docelowo około 30–35 minut z demonstracją w granicach czasu. Numery odnoszą się do `slides.md`.

| Slajd | Akcent naukowy |
|---|---|
| 1 | Teza: wynik jest funkcją sygnału, kontraktu danych i całego pipeline'u. |
| 2 | Przykładowa hipoteza EC/EO; na jakim etapie powstaje elastyczność analityczna? |
| 3 | PhysioNet: R01/R02 bazowe, R04 imagery; brak twierdzenia o własnej akwizycji. |
| 4 | Dwa źródła danych, to samo wymaganie jednoznacznego provenance. |
| 5 | Niezmienniki: czas, jednostki, odniesienie, SHA-256 i mapowanie kanałów. |
| 6 | BIDS Validator nie wykryje artefaktów fizjologicznych; nie wypełniaj nieznanych pól fikcją. |
| 7 | Porównanie MNE-BIDS round-trip: tolerancje, formaty, zdarzenia, sidecars. |
| 8 | Aperiodic background i komponent oscylacyjny; dopasowanie pokazowe nie jest FOOOF. |
| 9 | Welch: odpowiedź na rozdzielczość i wariancję; fs=160 Hz. |
| 10 | IAF kontra pasmo stałe: unikaj wyboru po obejrzeniu efektu. |
| 11 | Flagi QC i procent odrzuconych okien wpływają na estymator. |
| 12 | Transjenty i filtfilt; wyjaśnij niekauzalność oraz ringing. |
| 13 | CAR vs Cz na syntetycznym scalp map. Pozycje standard_1020 nie są pomiarem 3D. |
| 14 | Multiverse pokazuje zależność wyniku od legalnych decyzji. |
| 15 | Kod MNE pobiera archiwalne EDF. Nie deklaruj wykonanego przebiegu bez faktycznie pobranych plików. |
| 16 | Sygnał czasowy (symulacja), z kontrolowanymi jednostkami i skalą. |
| 17 | PSD w µV²/Hz i integracja do µV²; podaj parametry. |
| 18 | Pseudoreplikacja: jednostka biologiczna vs okno analityczne. |
| 19 | Eksportuj oryginał, odrębne BIDS Derivatives, przegląd sidecar i walidator. |
| 20 | Kryteria użycia własnych pomiarów. |
| 21 | Przejście przez jedną rejestrację: metadane → QC → PSD → sensitivity → manifest. |
| 22 | Co można niezależnie sprawdzić i co pozostaje niezweryfikowane? |

## Kontrola przed wystąpieniem

- Wszystkie dane/rysunki użyte do zilustrowania metody muszą mieć prawidłowy podpis **SYNTETYCZNE**.
- Z rzeczywistego EDF pokazuj zawsze źródło i identyfikator runu, nie dane personalne.
- Zwróć uwagę na rozróżnienie `Oz` i czterokanałowego montażu Muse S Athena. Nie oczekuj identycznej topografii alfa.
- Nie nazywaj interfejsu akwizycji zwalidowaną aparaturą bez raportu testów sprzętu.
- Nie utożsamiaj fizjologicznego efektu EC/EO z dowodem populacyjnym lub diagnozą.
