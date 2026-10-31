# Język i dokumentacja

[Dokumentacja](../index.md) | [Słownik](../glossary.md) | [Budżety](document-budgets.md)

Dokumentacja użytkowa EEG Neurolyze jest techniczna, zwięzła i zgodna z kodem. Nie twórz opisów hipotetycznych funkcji w czasie dokonanym. Rozdziel: plan, kod, weryfikację oprogramowania, test urządzenia, walidację naukową i publikację. Konwencje polskiego tekstu: poprawne znaki diakrytyczne, interpunkcja, pisownia zdaniowa nagłówków i cudzysłowy „…”. W nowej prozie unikaj U+2013/U+2014 i nie stosuj ozdobnych pauz.

Zachowaj uznane terminy: EEG, EO/EC, EEG-BIDS, EDF, BrainVision, MNE, PSD, LSL, BLE, BrainFlow, Muse S Athena. Przy pierwszym użyciu wyjaśnij skrót potrzebny czytelnikowi. Odróżniaj nominalną częstotliwość próbkowania od częstotliwości empirycznie potwierdzonej; clock domenę od host arrival time; channel label od lokalizacji elektrod; błąd walidatora od niepewności fizjologicznej. Korzystaj z [kanonicznego słownika](../glossary.md).

Zmiana instrukcji użytkownika wymaga sprawdzenia równoważnych wersji [PL](../pl/index.md) i [EN](../en/index.md). Dla CLI kopiuj tylko istniejące polecenia. Zachowuj kompatybilność ścieżek z Windows 11 i Pythonem 3.12. Nazwy plików i identyfikatory API pozostają angielskie, jak w kodzie. Nie zamieniaj bez potrzeby liczb, jednostek i cyfr w cytowanych wynikach.

Opracowania naukowe podają źródła, datę/wersję, status metod i rzeczywiste dowody. Nie wytwarzaj cytowań, DOI, danych ani metryk. Odróżniaj reproducibility od repeatability zgodnie z normą przyjętą dla badania, nie na podstawie polskiego podobieństwa terminów. Nie publikuj niezweryfikowanych wniosków klinicznych.

Każdy nowy dokument musi mieć jedną odpowiedzialność, budżet znaków, link z indeksu i odnośnik zwrotny. Weryfikuj działanie względnych linków, formatowanie MkDocs, polszczyznę i oba motywy strony po zmianach prezentacyjnych. Narzędzia sprawdzające pisownię angielską nie zastępują korekty tekstów polskich.
