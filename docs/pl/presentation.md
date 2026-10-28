# Seminarium zaawansowane: EEG-BIDS i wiarygodna inferencja

**Wersja główna v1.2.0:** 22 slajdy, format 16:9, około 30–35 minut. Bez rozdziałów o podstawach EEG i bez prezentowania programu EEG Neurolyze jako produktu.

## Treść seminarium

- Nieidentyfikowalność wyniku bez metadanych źródłowych i systemu referencyjnego.
- Walidacja EEG-BIDS vs fizjologiczna rzetelność zapisu.
- MNE-BIDS i semantyczna weryfikacja round-trip.
- Rozdzielenie komponentu oscylacyjnego i aperiodicznego.
- Rozdzielczość estymatora Welcha, IAF i wybór pasm.
- Artefakty EOG/EMG, reakcja filtrów na transjenty, wybór referencji.
- Analiza wrażliwości wielowariantowej i problem pseudoreplikacji.
- Wykonywalne fragmenty Python: import EDF, PSD i eksport źródłowego EEG-BIDS.

**[Źródło 22 slajdów](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/slides.md)** · [Notatki prelegenta](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/speaker-notes-advanced-v1.2.md) · [Metodologia](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/advanced-methodology.md)

Wersje archiwalne: [krótka v1.0.0](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/slides-concise-v1.0.md), [rozszerzona v1.1.0](https://github.com/MatPomGit/eeg-neurolyze/blob/main/presentations/psychofizjologia-eeg-bids-2026/slides-detailed-v1.1.md).

## Rejestracje i ilustracje

Na slajdach używamy zarejestrowanych sygnałów i własnego kodu analitycznego; nie opisujemy szczegółowo oprogramowania. Przygotowane **osiem wykresów to symulacje metodologiczne** i tak są podpisane. Nie zostały wygenerowane z rzeczywistych EDF pobranych w tej rozmowie.

Prawdziwe dane: [PhysioNet i lokalne EDF](real-eeg.md). Zastępuj obrazy symulacyjne tylko wynikami faktycznej analizy z udokumentowanym SHA-256, jednostkami i parametrami QC. Zależność od referencji i lokalizacji kanałów jest szczególnie istotna, jeśli zamiast 64-kanałowego systemu 10–10 używamy urządzenia czterokanałowego.
