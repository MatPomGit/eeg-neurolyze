## Cel i powiązania
<!-- Powiązane Issue, baza i planowany zakres. -->
- Related issue:
- Base SHA:
- Head SHA do walidacji:

## Zmiany i ryzyko
- Kontrakty API / format danych / wpływ na EEG i prywatność:
- ADR, architektura i dokumentacja PL/EN:
- Zmiany zależności i licencji:

## Walidacja
<!-- Nie oznaczaj nieuruchomionego testu jako PASS. -->
| Kontrola i polecenie | Środowisko | SHA | Status: PASS/FAIL/BLOCKED/NOT_RUN |
|---|---|---|---|
| `python tools/check_agent_docs.py` | | | |
| `python -m unittest discover -s tests -v` | | | |
| Inne istotne / MkDocs / BIDS / urządzenie | | | |

## Review, integracja i sprzątanie
- [ ] Analiza pełnego diff i brak przypadkowych zmian lub sekretów.
- [ ] Exact-SHA zgodny z wynikami obowiązkowego CI.
- [ ] Recenzja audytowa zapisana (COMMENT może być audytem wewnętrznym, nie APPROVED).
- [ ] Potwierdzono ochronę gałęzi, uprawnienia i konflikt.
- [ ] Wdrożenie wymagane? Jeśli tak, plan i dowody po merge.
- [ ] Po zamknięciu: Issue/status/milestone, zwolnienie rezerwacji, własne gałęzie i worktrees.
