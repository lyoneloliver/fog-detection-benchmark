# Ringkasan hasil: tcn-yang-2024

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 113066
- **Total waktu latih:** 8678.04 detik
- **Median waktu inferensi:** 10.53 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9400 | 0.7511 | 0.7672 | 0.9621 | 0.7953 | 0.4364 |

## AUROC per pasien

- **Rerata ± SD:** 0.7820 ± 0.1638 (n = 26)
- **IK bootstrap 95%:** [0.7182, 0.8425]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.8294 | 0.9908 | 0.9694 | 0.2807 | 0.9708 | 1.0000 | 74.4087 | 7.8359 |
| 2 | 0.9066 | 0.9845 | 0.9663 | 0.5909 | 0.9599 | 1.0000 | 80.8747 | 8.4990 |
| 3 | 0.7189 | 0.0127 | 0.0000 | 1.0000 | nan | 0.0000 | 67.1739 | 10.2440 |
| 4 | 0.6145 | 0.1677 | 0.2985 | 0.7659 | 0.2203 | 0.0000 | 79.3304 | 8.2343 |
| 5 | 0.7964 | 0.3183 | 0.2947 | 0.9206 | 0.2906 | 0.2222 | 75.7390 | 8.7843 |
| 6 | 0.9322 | 0.0648 | 0.0000 | 1.0000 | nan | 0.0000 | 70.7881 | 9.4808 |
| 7 | 0.6479 | 0.9943 | 0.9785 | 0.0680 | 0.9831 | 1.0000 | 66.5516 | 8.6183 |
| 8 | 0.8608 | 0.8987 | 0.9412 | 0.6762 | 0.8998 | 0.8000 | 132.0073 | 39.3174 |
| 9 | 0.7826 | 0.3036 | 0.3109 | 0.9544 | 0.3475 | 0.2500 | 149.8624 | 8.4654 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 77.5077 | 10.5268 |
| 11 | 0.9894 | 0.9435 | 0.5812 | 1.0000 | 0.7351 | 0.4000 | 74.7516 | 9.0563 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 74.2237 | 8.2303 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 67.1308 | 23.3940 |
| 14 | 0.7052 | 0.4804 | 0.0000 | 1.0000 | nan | 0.0000 | 68.0716 | 9.5018 |
| 15 | 0.7081 | 0.0519 | 0.0000 | 0.9289 | nan | 0.0000 | 248.6030 | 39.1898 |
| 16 | 0.9020 | 0.7397 | 0.1514 | 1.0000 | 0.2630 | 0.1538 | 304.8496 | 8.3831 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 74.9739 | 10.2324 |
| 18 | 0.8539 | 0.2773 | 0.0000 | 1.0000 | nan | 0.0000 | 226.8674 | 7.5013 |
| 19 | 0.7782 | 0.9961 | 0.9856 | 0.0000 | 0.9850 | 1.0000 | 202.8279 | 45.6717 |
| 20 | 0.6826 | 0.0332 | 0.0000 | 0.9567 | nan | 0.0000 | 305.6287 | 26.5119 |
| 21 | 0.9344 | 0.3675 | 0.3359 | 0.9599 | 0.2728 | 0.3333 | 252.4428 | 27.2687 |
| 22 | nan | nan | nan | 0.9875 | nan | 0.0000 | 323.8442 | 43.9457 |
| 23 | 0.9311 | 0.5234 | 0.1657 | 1.0000 | 0.2844 | 0.0000 | 318.2812 | 50.4530 |
| 24 | 0.3371 | 0.1555 | 0.7620 | 0.2390 | 0.3389 | 0.0000 | 325.0356 | 41.1530 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 316.3367 | 40.3391 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 316.5109 | 44.1762 |
| 27 | 0.9269 | 0.8826 | 0.8218 | 0.8921 | 0.8125 | 0.7857 | 313.0450 | 45.1712 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 314.0426 | 48.7841 |
| 29 | 0.4359 | 0.3469 | 0.4565 | 0.4673 | 0.4016 | 0.2174 | 316.6149 | 39.4945 |
| 30 | 0.9343 | 0.8446 | 0.5100 | 0.9783 | 0.6417 | 0.4615 | 266.4943 | 36.4182 |
| 31 | 0.7982 | 0.4204 | 0.3227 | 0.9955 | 0.4579 | 0.4444 | 278.2918 | 24.5000 |
| 32 | 0.9031 | 0.0474 | 0.0000 | 1.0000 | nan | 0.0000 | 238.4319 | 10.9768 |
| 33 | 0.5415 | 0.4599 | 0.0000 | 1.0000 | nan | 0.0000 | 2454.9050 | 8.3338 |
| 34 | 0.8801 | 0.6820 | 0.4572 | 0.9235 | 0.5241 | 0.5714 | 57.8824 | 8.3313 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 63.7102 | 8.4212 |

## Kartu metode

### Hiperparameter

- **Hidden features:** 32
- **Tcn layers:** 5
- **Kernel size:** 3
- **Dilation:** 1, 3, 9, 27, 81
- **Window samples:** 256
- **Target fs hz:** 64
- **Batch size:** 1024
- **Epochs:** 15
- **Optimizer:** Amsgrad (beta=(0.9, 0.999))
- **Learning rate:** 0.0005
- **Learning rate decay per epoch:** 0.95
- **Loss:** class-weighted cross-entropy
- **Trained epochs:** 15
- **Refinement stages:** 4
- **Refinement layers per stage:** 8
- **Refinement dilation:** 1, 2, 4, 8, 16, 32, 64, 128
- **Refinement batch size:** 1
- **Refinement loss:** weighted cross-entropy + smoothing (tau=4, lambda=0.15)
- **Refinement epochs trained:** 15
- **Threshold calibration:** held-out training subjects
- **Deviasi dari metode acuan:**
  - Paper menggunakan lima IMU (30 kanal); adaptasi ini hanya memakai satu IMU tibia (6 kanal) sesuai ketersediaan kanal Figshare.
  - Data Figshare di-resample ke 64 Hz agar 256 sampel tetap merepresentasikan jendela waktu 4 detik seperti pada paper.
  - Model disesuaikan untuk mengembalikan probabilitas biner per sampel sesuai spesifikasi antarmuka benchmark.
  - Jumlah epoch pelatihan diturunkan menjadi 15 untuk initial TCN dan 15 untuk refiner agar komputasi CPU lebih efisien.
  - Evaluasi mengikuti kerangka LOSO benchmark, bukan partisi dan evaluasi spesifik dari paper.
  - Threshold dikalibrasi dari subjek validasi internal data latih, terpisah dari subjek uji LOSO.


