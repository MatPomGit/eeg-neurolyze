# Notatki prelegenta · EEG-BIDS, Python, EEG Neurolyze

Wersja 1.0.0 · 2026-10-28 · docelowo 25–30 min.

| Nr | Czas | Komentarz ustny |
|---|---:|---|
| 1 | 0:45 | Wyjaśnij, że pokaz jest technologiczny, nie kliniczny. |
| 2 | 1:15 | Zadaj pytanie: czy inna osoba odtworzy wynik z samego wykresu? |
| 3 | 2:00 | Źródła EEG, wpływ referencji; artefakty EOG/EMG. |
| 4 | 1:45 | BIDS porządkuje dane i umożliwia automatyzację, ale nie zastępuje metodyki. |
| 5 | 2:15 | Przejdź po drzewie danych; rozróżnij surowe pliki i metadane; events.tsv tylko gdy odpowiednie dla danych. |
| 6 | 2:00 | Podkreśl sampling frequency, reference, kanały i zdarzenia. |
| 7 | 1:45 | Filtracja i artefakty nie są neutralnymi operacjami. |
| 8 | 1:45 | Alfa EO/EC jest demonstracją koncepcji; nie obiecuj efektu dla każdego uczestnika i kanału. |
| 9 | 1:45 | Wyjaśnij PSD w jednostkach µV²/Hz oraz zależność estymaty od parametrów. |
| 10 | 1:00 | Kod MNE stanowi przykład; nie deklaruj uruchomienia bez danych BIDS. |
| 11 | 1:15 | Wymień dokładnie dostępne funkcje i niezweryfikowany sprzęt. |
| 12 | 8:00 | Przeprowadź pokaz z demo.md (zastępuje komentarz ustny). |
| 13 | 1:00 | Walidator BIDS nie świadczy o fizjologicznej jakości rejestracji. |
| 14 | 0:30 | Jednozdaniowe podsumowanie. |

Razem ~29 min (czasy orientacyjne).

## Pytania prowadzącej
- **Czy były rzeczywiste zapisy EEG?** W prezentowanej demonstracji nie, tylko deterministyczne dane syntetyczne. W repo istnieje tor pozyskiwania z Muse S Athena, ale pomiar sprzętowy nie przeszedł jeszcze wymaganej walidacji.
- **Czy to jest BIDS?** O zgodności konkretnego eksportu wnioskujemy dopiero po poprawnym wyniku oficjalnego BIDS Validator i sprawdzeniu odczytu danych; pokazujemy rozróżnienie między potencjalnym eksportem a potwierdzoną walidacją.
- **Czy można analizować dane rzeczywiste?** Tak, narzędziami MNE można analizować poprawnie opisany EDF/EEG-BIDS. Oddzielna integracja importu surowych PhysioNet EDF z własnym .eegz nie jest częścią tego pokazu.
- **Co oznacza alfa?** Moc widmowa 8–13 Hz jest cechą sygnału, a jej znaczenie zależy od lokalizacji, kontekstu, parametrów analizy i jakości danych.
- **Dlaczego archiwum .eegz?** To format wewnętrzny zachowujący próbki/metadane z sumami kontrolnymi; nie jest standardem BIDS.
