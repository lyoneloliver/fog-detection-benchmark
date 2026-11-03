# Ringkasan hasil: tcn-yang-2024

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 113066
- **Total waktu latih:** 789.16 detik
- **Median waktu inferensi:** 9.48 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.8242 | 0.5674 | 0.3912 | 0.9160 | 0.4468 | 0.2322 |

## AUROC per pasien

- **Rerata ± SD:** 0.6127 ± 0.2465 (n = 26)
- **IK bootstrap 95%:** [0.5211, 0.7017]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.8430 | 0.9932 | 0.9258 | 0.2000 | 0.9463 | 0.7500 | 14.3903 | 9.2048 |
| 2 | 0.1645 | 0.8623 | 1.0000 | 0.0000 | 0.9456 | 0.0000 | 13.7755 | 8.9110 |
| 3 | 0.3125 | 0.0061 | 0.0000 | 0.9808 | nan | 0.0000 | 14.0116 | 7.9080 |
| 4 | 0.5572 | 0.1506 | 0.0330 | 0.9614 | 0.0521 | 0.0000 | 14.1939 | 6.8173 |
| 5 | 0.5511 | 0.1553 | 0.0000 | 1.0000 | nan | 0.0000 | 10.0818 | 6.5882 |
| 6 | 0.9212 | 0.0549 | 0.0000 | 0.9833 | nan | 0.0000 | 11.1628 | 26.1445 |
| 7 | 0.3301 | 0.9812 | 0.0000 | 1.0000 | nan | 0.0000 | 17.1555 | 8.7199 |
| 8 | 0.7954 | 0.9091 | 0.0000 | 1.0000 | nan | 0.0000 | 13.7695 | 19.5607 |
| 9 | 0.6955 | 0.1646 | 0.6024 | 0.6070 | 0.2106 | 0.0741 | 12.2318 | 7.3244 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 15.9716 | 8.6165 |
| 11 | 0.9684 | 0.8572 | 0.5741 | 0.9924 | 0.7060 | 0.3636 | 15.7352 | 8.9191 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 12.2600 | 7.1223 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 16.1450 | 20.5611 |
| 14 | 0.5915 | 0.2870 | 0.0000 | 1.0000 | nan | 0.0000 | 15.0425 | 6.9389 |
| 15 | 0.2980 | 0.0280 | 1.0000 | 0.0000 | 0.0645 | 0.0000 | 12.4262 | 13.5980 |
| 16 | 0.7577 | 0.3213 | 0.0000 | 1.0000 | nan | 0.0000 | 13.3130 | 16.9393 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 8.1772 | 12.9605 |
| 18 | 0.4031 | 0.0214 | 0.0000 | 1.0000 | nan | 0.0000 | 16.0395 | 13.3072 |
| 19 | 0.9508 | 0.9992 | 0.9942 | 0.0000 | 0.9893 | 1.0000 | 14.2290 | 9.4832 |
| 20 | 0.8367 | 0.0868 | 0.0000 | 1.0000 | nan | 0.0000 | 11.0561 | 7.4021 |
| 21 | 0.9767 | 0.4433 | 0.0000 | 0.9941 | nan | 0.0000 | 9.1481 | 7.1841 |
| 22 | nan | nan | nan | 1.0000 | nan | 1.0000 | 12.8306 | 8.0731 |
| 23 | 0.4315 | 0.0526 | 0.0000 | 1.0000 | nan | 0.0000 | 44.2458 | 37.4720 |
| 24 | 0.3443 | 0.1674 | 0.9976 | 0.0726 | 0.3743 | 0.0000 | 51.2190 | 38.4456 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 39.4197 | 39.3117 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 42.4317 | 37.9068 |
| 27 | 0.7631 | 0.6169 | 0.0000 | 1.0000 | nan | 0.0000 | 39.1550 | 48.5155 |
| 28 | nan | nan | nan | 0.9667 | nan | 0.0000 | 54.9581 | 39.9746 |
| 29 | 0.3653 | 0.3600 | 0.0000 | 1.0000 | nan | 0.0000 | 70.7358 | 40.2360 |
| 30 | 0.5591 | 0.2577 | 1.0000 | 0.0000 | 0.3532 | 0.0000 | 32.1574 | 39.3301 |
| 31 | 0.9333 | 0.5097 | 1.0000 | 0.2886 | 0.1264 | 0.0000 | 53.0363 | 8.0000 |
| 32 | 0.5856 | 0.0095 | 0.0000 | 1.0000 | nan | 0.0000 | 9.2135 | 7.2486 |
| 33 | 0.6449 | 0.4625 | 0.0000 | 1.0000 | nan | 0.0000 | 8.7724 | 7.8635 |
| 34 | 0.3492 | 0.1515 | 0.0000 | 1.0000 | nan | 0.0000 | 11.5217 | 45.3783 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 39.1515 | 38.0813 |

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


