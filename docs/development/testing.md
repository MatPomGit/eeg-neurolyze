# Walidacja, CI i bramki integracji

[Dokumentacja](../index.md) | [AGENTS.md](https://github.com/MatPomGit/eeg-neurolyze/blob/main/AGENTS.md) | [Workflow agenta](agent-workflow.md) | [Budżety](document-budgets.md)

## Kontrole lokalne

W katalogu głównym, z Pythonem 3.12 oraz lokalnym środowiskiem:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tools/check_agent_docs.py
```

Linux / macOS: zamień interpreter na `.venv/bin/python`. Testy standardowej biblioteki nie wymagają urządzenia ani pakietów opcjonalnych. Jeśli środowisko lub narzędzie niedostępne, oznacz `NOT_RUN` albo `BLOCKED`, nigdy `PASS`.

Dokumentacja:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
.\.venv\Scripts\python.exe -m mkdocs build --clean
```

Testy wymagające `.[bids]` lub `.[muse]` uruchamiaj osobno. Zmiany BIDS testuj z oficjalnym walidatorem i odczytem MNE; sam pomyślny test jednostkowy nie dowodzi zgodności konkretnego datasetu. Rzeczywiste testy Muse wymagają odrębnego protokołu, uprawnionego operatora i urządzenia. Nigdy nie odtwarzaj prywatnego EEG na publicznym runnerze.

## Rzeczywiste workflow

- `.github/workflows/core-tests.yml`: Windows i Ubuntu, obecnie `pull_request`, `push main`, `workflow_dispatch`. Stanowi już istniejący wyjątek od manual-only. Nie wyłączaj, aby pozornie uzgodnić dokumenty.
- `.github/workflows/mkdocs-pages.yml`: `main`, ręcznie lub po wybranych ścieżkach; weryfikacja i publikacja Docs/Pages.
- `.github/workflows/bids.yml`, `muse.yml` i workflow native: sprawdź aktualne YAML, wymagania i status; nie uruchamiaj hardware na CI.

Przed zmianą workflow zobacz plik YAML, wymagane checki i ochronę gałęzi. Utrzymuj `permissions: contents: read` tam, gdzie wystarcza. Publiczny niezaufany PR: tylko izolowany runner GitHub-hosted bez sekretów. Nie uruchamiaj go na stałym prywatnym runnerze. Nie dokładaj płatnych zasobów.

## Dowody i exact-SHA

Dla każdej kontroli zapisz polecenie, OS, interpreter, wersje, finalny SHA, datę i rezultat `PASS`, `FAIL`, `BLOCKED` albo `NOT_RUN`. Gdy HEAD PR zmienił się, wcześniejszy wynik wymaga oceny i retestu. Porównaj pełny diff, sprawdź review, `mergeable`, branch protection, required checks i aktualną bazę. `COMMENT` z rzeczowym raportem jest audytem wewnętrznym, ale nie GitHub `APPROVED`. Nie obchodź zabezpieczeń. Scalenie jest dozwolone wyłącznie po spełnieniu wszystkich rzeczywiście wymaganych bramek.

## Dokumenty i bezpieczeństwo

`tools/check_agent_docs.py` sprawdza wybrane dokumenty normatywne, ich limity, miejscowe linki i obecność w nawigacji. MkDocs sprawdza rendering strony. Te kontrole nie zastępują ręcznego przeglądu odnośników zewnętrznych, poufności, jakości języka i poprawności naukowej. Wyniki z symulatora nie mogą być przedstawiane jako dane fizjologiczne.
