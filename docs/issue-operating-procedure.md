# Zasady obsługi GitHub Issues

[Indeks](index.md) | [AGENTS.md](../AGENTS.md) | [Workflow agenta](development/agent-workflow.md)

GitHub Issues to kanoniczny rejestr zakresu i statusu pracy; milestones reprezentują etapy. `TODO.md` i [roadmap](architecture/ROADMAP.md) opisują plan, lecz nie zastępują aktywnego Issue. Przed nowym Issue szukaj już istniejącego, odczytaj komentarze i powiązane PR.

## Minimalna struktura Issue
1. Cel i zakres; status kodu i weryfikacji, bez obiecywania wyniku.
2. Priorytet P0/P1/P2/P3; typ pracy: kod, badania, dane, sprzęt, dokumentacja.
3. `execution_mode`: `autonomous`, `mixed` lub `human_required`. Podaj, czy potrzebne są badania uczestników, zgoda, sprzęt, dostęp lub koszt.
4. Jednoznaczne kryteria akceptacji i testy; zależności do innych Issue/PR/ADR.
5. Aktualny agent, rezerwacja, commit bazowy, etap `PLANNED`, `IN_PROGRESS`, `BLOCKED`, `WAITING_FOR_USER` lub `DONE`.
6. Wyniki kontroli: komenda, środowisko, SHA, `PASS/FAIL/BLOCKED/NOT_RUN`, dowody i następny krok.

Zachowuj komentarze i audyty; po ukończeniu zwolnij jedynie tymczasową rezerwację. Dokumentuj istotny postęp, nie produkuj wpisów pozorujących aktywność.

## Eskalacja do użytkownika
Gdy tylko właściciel może podjąć decyzję lub wykonać czynność, przeszukaj istniejące Issues i zapisz jedno zgłoszenie z: przyczyną, dowodem, priorytetem, wymaganym uprawnieniem, OS/środowiskiem, numerowanym planem czynności (konkretne kliknięcia lub gotowe sprawdzone komendy), spodziewanym wynikiem, danymi zwrotnymi **bez informacji wrażliwych**, ryzykiem/rollbackiem i dokładnym warunkiem wznowienia. Oznacz `WAITING_FOR_USER` i ostatni potwierdzony SHA. Nie publikuj haseł i surowych EEG. Jeśli Issues są niedostępne lub nieodpowiednie, skorzystaj z `docs/user-actions.md`, ale nie twórz duplikatu.

Przykład zadania z instrukcją: [Issue #81](https://github.com/MatPomGit/eeg-neurolyze/issues/81).

## Integracja
PR musi wskazywać Issue, opis zmian, potwierdzone testy, SHA, wpływ na PL/EN, architekturę i dane, wymagane review oraz status merge/deployment. `COMMENT` jest wewnętrznym audytem; nie zastępuje wymaganego zatwierdzenia platformy. Limit równoległości to dwie aktywne gałęzie i dwa otwarte PR. Zamykaj Issue dopiero po Definition of Done, nie po samym commit lub merge.
