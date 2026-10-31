# Autonomiczna praca agentów

[Dokumentacja](../index.md) | [AGENTS.md](https://github.com/MatPomGit/eeg-neurolyze/blob/main/AGENTS.md) | [Procedura Issues](../issue-operating-procedure.md) | [Testy](testing.md)

## Wejście i wznowienie

Nowy agent czyta AGENTS.md, cel zadania, aktywne Issue i PR, architekturę tylko gdy zmiana dotyka jej kontraktów. Identyfikuje repozytorium z GitHub, gałąź domyślną i jej SHA, lokalne zmiany i właścicieli rozpoczętych prac. Brak kontekstu rozmowy nie jest powodem do ponawiania ukończonego zadania. Odczytaj ostatni potwierdzony etap, SHA, wyniki CI, recenzje oraz stan wdrożenia z trwałych wpisów.

Jeśli dostępny jest autoryzowany Research Autopilot, używaj jego kontrolera, leasingu i rejestrów. W pozostałych przypadkach prowadź rezerwację w komentarzu Issue: wykonawca, zakres, baza SHA, data, status i następny krok. Wznawiając, odczytaj tę rezerwację, sprawdź aktualny PR i nie twórz konkurencyjnej zmiany.

## Wybór zadania

Zadanie właściciela ma pierwszeństwo w wyznaczonym zakresie. W autonomicznym trybie kolejność: ryzyko ujawnienia danych, awarie, aktywne PR, brakujące wdrożenia, blokady, Issues P0/P1, pozostałe kamienie milowe, dokumentacja i techniczny dług. Sprawdzaj zależności i typ pracy (autonomiczna, wymagająca sprzętu, wymagająca człowieka). Nie wybieraj zadania już zarezerwowanego.

Twardy limit 2 aktywnych gałęzi i 2 otwartych PR na repozytorium obejmuje wszystkie agenty i drafty. Przekroczenie limitu zastanego: nie kasuj automatycznie, zatrzymaj nową pracę i domykaj istniejącą. Preferuj 1 gałąź na 1 PR. Dla sześciu otwartych PR najpierw ustal właścicieli, priorytety i bezpieczne domknięcie. Nie twórz siódmego.

## DoR, wykonanie, checkpoint

DoR: uzasadniony cel, jedno Issue, mierzalne akceptacje, znane uprawnienia i środowisko, bazowy SHA, brak kolizji. Opracuj mały plan i przewidywane testy. Używaj istniejących modułów i zależności, nie buduj kolejnej kolejki ani schedulera.

W czasie pracy aktualizuj Issue po osiągnięciu mierzalnego etapu; utrwal identyfikator PR, commity, testy, ograniczenia, niespełnione warunki i kolejny krok. W awarii przerwij bez niszczenia częściowego archiwum; pozostaw dane do odtworzenia. Stan badania odróżniaj od stanu kodu. Nie wykonuj samoczynnie akwizycji EEG od osób badanych ani publikacji naukowej.

## Review, merge i deployment

Przed zmianą architektury odczytaj kanoniczny opis i powiązane ADR. W tym samym PR uaktualnij opis architektury; przy nowej decyzji dodaj nowy ADR lub wskaż dokument zastępujący poprzedni. Nie przepisuj historii zaakceptowanych ADR bez uzasadnienia.

Przed PR: pełny diff, ścieżki, zgodność z architekturą, dane i sekrety, testy z dokładnym SHA. Weryfikuj aktualność bazy, konflikty, status obowiązujących checks i recenzje. `COMMENT` z audytem jest dowodem przeglądu wewnętrznego, nie formalnym `APPROVED` ani niezależną recenzją osoby. Dla nowego HEAD powtórz testy adekwatne do zmiany. Nie obchodź branch protection.

Scal tylko z autoryzacją, zielonymi wymaganymi checks i znaną wersją. Po scaleniach sprawdzaj main, a osobno rzeczywiste wdrożenie, smoke, wersję i logi, jeśli obejmuje je zakres. Nie uznawaj stanu `merged` za `deployed`. Dla GitHub Pages weryfikuj sukces workflow publikacji i finalną stronę.

## DoD i porządki

DoD: wszystkie kryteria, wymagane testy, aktualne PL/EN przy zmianie zachowania, dowody i SHA, review, integracja i uprawnione wdrożenie, zakończone Issue, zwolnione rezerwacje, usunięte tylko własne zbędne gałęzie i worktrees. Zachowaj historyczne wpisy oraz wyniki badań. `NOT_RUN` i `BLOCKED` nie są sukcesem.

## Eskalacja i brak narzędzia

Przy braku narzędzia, GitHub, dostępu do sprzętu lub danych: zapisz `BLOCKED` w Issue, ostatni SHA, próbę, wymagane uprawnienie, dokładną czynność człowieka i warunek wznowienia. Instrukcja musi być wykonawcza: system/OS, numerowane kroki, bezpieczne polecenia, kontrola wyniku, co zwrócić bez danych wrażliwych. Nie zgaduj wyników i nie żądaj sekretów w publicznym Issue. Przykład rzeczywistej blokady: [klasyfikacja publicznego EEGZ #81](https://github.com/MatPomGit/eeg-neurolyze/issues/81).

Gdy agent działa tylko w trybie analizy, nie pisze commitów, nie publikuje i nie scala. Operacje płatne, zmiany uprawnień i produkcja wymagają jawnego upoważnienia.
