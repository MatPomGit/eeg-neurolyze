# Budżety dokumentacji

[Indeks](../index.md) | [AGENTS.md](https://github.com/MatPomGit/eeg-neurolyze/blob/main/AGENTS.md) | [Testowanie](testing.md)

Limity dotyczą liczby znaków Unicode treści Markdown, łącznie ze spacjami i składnią. Weryfikuj je przed utworzeniem i zmianą dokumentu. Historycznych notatek, manuskryptów i danych nie skracaj mechanicznie.

| Dokument lub kategoria | Maksymalnie znaków |
|---|---:|
| `AGENTS.md`, `README.md` | 12 000 |
| `docs/architecture/PROJECT-CONCEPT.md` (kanoniczna architektura) | 16 000 |
| `docs/architecture/ROADMAP.md`, `docs/research-schedule.md` | 12 000 |
| `docs/development/agent-workflow.md` | 16 000 |
| `docs/development/coding-standards.md`, `docs/development/writing-standards.md` | 12 000 |
| `docs/development/testing.md`, `docs/issue-operating-procedure.md` | 10 000 |
| `docs/research/reproducibility.md` | 12 000 |
| `docs/teaching-standards.md`, `docs/glossary.md` | 10 000 |
| `docs/hardware.md`, `docs/software.md`, jeśli będą potrzebne | 8 000 |
| Pojedynczy ADR | 5 000 |
| Pojedyncza nowa notatka | 3 000 |
| Inny nowy Markdown, w tym indeksy `docs/` | 10 000 |
| `docs/user-actions.md`, jeśli Issues niedostępne | 10 000 |

`CHANGELOG.md`: nowy wpis najwyżej około 2 000 znaków, bez skracania historii. Nie nakładaj limitów na `CITATION.cff`, `mkdocs.yml`, kod, surowe wyniki i manuskrypty. Jeśli wymagania nie mieszczą się w limicie, wydziel dokument o innym zakresie i połącz go linkami; nie usuwaj zabezpieczeń lub dowodów.

`AGENTS.md`: cel około 150 wierszy, miękki limit 200 oraz poniżej 32 KiB. Automatyczna kontrola lokalna: `python tools/check_agent_docs.py`. Obejmuje normatywne dokumenty utrzymywane przez agentów, a nie historyczne materiały, które wymagają osobnej decyzji o reorganizacji.
