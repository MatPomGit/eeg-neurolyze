# Źródła i zakres twierdzeń (v1.1.0, 2026-10-28)

1. PhysioNet: EEG Motor Movement/Imagery Dataset v1.0.0, doi:10.13026/C28G6P, https://physionet.org/content/eegmmidb/1.0.0/ . 109 osób; 64 kanały EEG; 160 Hz; EDF+, run 1 = EO, run 2 = EC; system BCI2000. Licencja: Open Data Commons Attribution License 1.0.
2. MNE-Python: `mne.datasets.eegbci.load_data`: https://mne.tools/stable/generated/mne.datasets.eegbci.load_data.html . Numery innych runów są inne dla wykonania ruchów i wyobrażania ruchu.
3. MNE-Python: przetwarzanie i `Raw.compute_psd`, https://mne.tools/stable/generated/mne.io.Raw.html .
4. MNE-BIDS: `write_raw_bids`, https://mne.tools/mne-bids/stable/generated/mne_bids.write_raw_bids.html .
5. BIDS EEG: https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html .
6. Repozytorium `MatPomGit/eeg-neurolyze`: `README.md`, `TODO.md`, `docs/pl/bids.md`, `src/eeg_athenalyze/cli.py`.

Nie przypisuj schematu BCI2000 do konkretnej nieudokumentowanej konfiguracji sprzętowej. Nie deklaruj zbadania danych PhysioNet, dopóki pliki EDF nie zostały faktycznie pobrane i przetworzone. Dotychczasowe wykresy na slajdach 13 i 16 są syntetyczne i wyraźnie to oznaczają. EEG Neurolyze nie ma jeszcze zwalidowanej rzeczywistej akwizycji Muse S Athena.
