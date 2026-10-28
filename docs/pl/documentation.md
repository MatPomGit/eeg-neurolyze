# Budowa dokumentacji i publikacja na GitHub Pages

## Struktura

- `mkdocs.yml`: konfiguracja, wygląd i menu.
- `docs/index.md`: strona startowa.
- `docs/pl/`, `docs/en/`: przewodniki w dwóch językach.
- `docs/architecture/`: koncepcja, roadmap i ADR.
- `docs/research/`: źródła i wyniki przeglądów.
- `.github/workflows/mkdocs-pages.yml`: budowanie i publikacja strony.

## Lokalne uruchomienie

W katalogu głównym projektu, użyj osobnego środowiska:

```powershell
py -3.12 -m venv .venv-docs
.\.venv-docs\Scripts\python.exe -m pip install -r requirements-docs.txt
.\.venv-docs\Scripts\python.exe -m mkdocs build --clean
.\.venv-docs\Scripts\python.exe -m mkdocs serve
```

Podczas edycji kontroluj w konsoli ostrzeżenia o linkach. Nie dodawaj plików EEG ani `.venv-docs` do Git. Dokumentacja ma zawierać jedynie kody, dane demonstracyjne i odnośniki do legalnie publicznych zasobów.

## Publikacja

Workflow działa **tylko na `main`**, uruchamia się ręcznie lub po zmianie plików dokumentacji na `main` (wąskie `paths`). Buduje witrynę, publikuje artefakt przez oficjalny mechanizm GitHub Pages. Nie uruchamia testów sprzętowych ani nie pobiera EDF.

**Ważne:** w repozytorium wybierz **Settings → Pages → Build and deployment → Source: GitHub Actions**, jeżeli źródło nie zostało jeszcze tak skonfigurowane. Dopiero zakończony sukcesem deployment uprawnia do potwierdzenia publicznego adresu `https://matpomgit.github.io/eeg-neurolyze/`.

## Bezpieczna aktualizacja

1. Zmodyfikuj lub dodaj stronę Markdown.
2. Dopisz ją do `nav` w `mkdocs.yml`.
3. Zweryfikuj brak martwych odnośników i poprawność poleceń.
4. Utwórz PR i porównaj z `main`. Publikacja następuje po scaleniu, nie na gałęzi roboczej.
5. Sprawdź wynik GitHub Actions oraz docelową stronę.

Źródła: [GitHub Pages - custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [MkDocs](https://www.mkdocs.org/).
