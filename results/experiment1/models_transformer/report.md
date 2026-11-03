# Ringkasan hasil: transformer

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 90065
- **Total waktu latih:** 1363.96 detik
- **Median waktu inferensi:** 9.34 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.7321 | 0.3892 | 0.9881 | 0.0050 | 0.3163 | 0.2850 |

## AUROC per pasien

- **Rerata ± SD:** 0.7272 ± 0.1998 (n = 26)
- **IK bootstrap 95%:** [0.6502, 0.8009]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.7673 | 0.9899 | 1.0000 | 0.0000 | 0.9811 | 0.0000 | 27.1119 | 7.6346 |
| 2 | 0.8745 | 0.9793 | 0.3699 | 0.9167 | 0.5363 | 0.4000 | 40.3230 | 8.1457 |
| 3 | 0.6090 | 0.0109 | 1.0000 | 0.0000 | 0.0148 | 0.0000 | 40.3067 | 8.4600 |
| 4 | 0.4769 | 0.1383 | 0.0000 | 1.0000 | nan | 0.0000 | 25.1960 | 8.1847 |
| 5 | 0.5173 | 0.2306 | 1.0000 | 0.0000 | 0.1779 | 0.0000 | 17.9130 | 8.6898 |
| 6 | 0.9998 | 0.9659 | 1.0000 | 0.0000 | 0.0188 | 0.0000 | 21.2960 | 8.0118 |
| 7 | 0.9463 | 0.9993 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 33.3585 | 8.8919 |
| 8 | 0.7164 | 0.8438 | 1.0000 | 0.0000 | 0.8111 | 0.0000 | 29.8439 | 8.8290 |
| 9 | 0.5534 | 0.1458 | 0.6936 | 0.2157 | 0.1399 | 0.0000 | 36.1152 | 11.1751 |
| 10 | nan | nan | nan | 0.0000 | nan | 0.0000 | 19.7203 | 9.0140 |
| 11 | 0.9932 | 0.9613 | 1.0000 | 0.0000 | 0.2261 | 0.0000 | 79.1030 | 8.8101 |
| 12 | nan | nan | nan | 0.0000 | nan | 0.0000 | 48.8049 | 8.4517 |
| 13 | nan | nan | nan | 0.0000 | nan | 0.0000 | 41.5235 | 13.0093 |
| 14 | 0.5151 | 0.2626 | 0.0393 | 0.9686 | 0.0688 | 0.0500 | 29.8754 | 15.3943 |
| 15 | 0.3252 | 0.0272 | 0.0000 | 0.9448 | nan | 0.0000 | 55.8124 | 11.3577 |
| 16 | 0.8336 | 0.6554 | 1.0000 | 0.0000 | 0.2809 | 0.0000 | 40.2949 | 10.4604 |
| 17 | nan | nan | nan | 0.0000 | nan | 0.0000 | 21.6818 | 8.6423 |
| 18 | 0.8845 | 0.1000 | 1.0000 | 0.0000 | 0.0385 | 0.0000 | 32.9709 | 10.9543 |
| 19 | 0.9896 | 0.9998 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 27.2132 | 10.7376 |
| 20 | 0.6272 | 0.0323 | 0.0000 | 1.0000 | nan | 0.0000 | 35.4220 | 9.3020 |
| 21 | 0.9660 | 0.5290 | 1.0000 | 0.3269 | 0.0957 | 0.0000 | 54.4438 | 9.0045 |
| 22 | nan | nan | nan | 0.0000 | nan | 0.0000 | 22.4706 | 12.5324 |
| 23 | 0.8944 | 0.3774 | 1.0000 | 0.0000 | 0.0900 | 0.0000 | 57.8224 | 9.3377 |
| 24 | 0.4918 | 0.3026 | 0.1806 | 0.8542 | 0.2119 | 0.3636 | 38.3259 | 9.4394 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 43.4077 | 8.6843 |
| 26 | nan | nan | nan | 0.0000 | nan | 0.0000 | 24.3895 | 10.7692 |
| 27 | 0.8290 | 0.7487 | 1.0000 | 0.0000 | 0.5177 | 0.0000 | 43.6088 | 12.4636 |
| 28 | nan | nan | nan | 0.0000 | nan | 0.0000 | 50.0631 | 9.4278 |
| 29 | 0.6993 | 0.5033 | 1.0000 | 0.0000 | 0.5661 | 0.0000 | 22.6079 | 12.4442 |
| 30 | 0.8555 | 0.6799 | 1.0000 | 0.0000 | 0.3532 | 0.0000 | 41.8548 | 8.7235 |
| 31 | 0.4608 | 0.0652 | 1.0000 | 0.0000 | 0.0933 | 0.0000 | 22.8992 | 10.1274 |
| 32 | 0.6392 | 0.0125 | 0.0000 | 1.0000 | nan | 0.0000 | 60.8777 | 10.4356 |
| 33 | 0.5437 | 0.4912 | 0.1328 | 0.9384 | 0.2133 | 0.0000 | 92.8297 | 8.6162 |
| 34 | 0.8980 | 0.7636 | 0.9777 | 0.5173 | 0.5157 | 0.0000 | 40.5921 | 9.6858 |
| 35 | nan | nan | nan | 0.9911 | nan | 0.0000 | 43.8768 | 11.3520 |

## Kartu metode

### Hiperparameter

- **Target fs hz:** 40
- **Lowpass order:** 2
- **Lowpass cutoff hz:** 15.0
- **Highpass order:** 3
- **Highpass cutoff hz:** 0.2
- **Normalisasi:** min-max per sumbu ke [-1, 1], dihitung dari pasien training
- **Window samples:** 128
- **Window seconds:** 3.2
- **Overlap:** 0.75
- **Fft bins:** 64
- **Spectral context windows:** 4
- **Cnn filters:** 128, 64, 32
- **Cnn kernel size:** 4
- **Cnn padding:** valid
- **Transformer blocks:** 3
- **Attention heads:** 3
- **Attention head size:** 32
- **Layer norm epsilon:** 0.001
- **Mlp units:** 80, 40, 1
- **Lr:** 0.0006
- **Batch size:** 512
- **Max epochs:** 150
- **Patience:** 7
- **Epochs trained:** 8
- **Validation split:** 20% pasien pada data training untuk early stopping
- **Loss:** BCEWithLogitsLoss dengan pos_weight=jumlah_negatif/jumlah_positif
- **Jumlah window train non fog:** 5781
- **Jumlah window train fog:** 1470
- **Pos weight fog:** 3.9326530612244897
- **Deviasi dari metode acuan:**
  - Paper memakai akselerometer pinggang 200 Hz; Figshare memakai sensor tulang kering 128 Hz yang di-resample ke 40 Hz.
  - Hanya 3 kanal akselerometer yang dipakai; kanal giroskop diabaikan sesuai domain spektral paper.
  - Label Figshare biner (FoG/non-FoG), sedangkan paper mencakup kelas tambahan (berjalan dan berdiri).
  - Window dilabeli positif jika FoG >50%, negatif jika 0%, dan window campuran dibuang.
  - Normalisasi min-max ke rentang [-1, 1] dihitung murni dari data training untuk mencegah kebocoran data.
  - Loss training menggunakan pos_weight berdasarkan rasio kelas untuk mengatasi ketidakseimbangan data.
  - Early stopping dan pemilihan threshold divalidasi pada subjek internal agar set uji LOSO tidak tercemar.
  - Runner benchmark memakai rentang threshold 0.01-0.99 (paper 0.2-0.8) demi kompatibilitas sistem.
  - Implementasi memakai padding valid sesuai default Conv1D Keras yang dirujuk paper.
  - Probabilitas level-window diproyeksikan dan dirata-ratakan pada area overlap untuk memenuhi antarmuka sampel benchmark.


