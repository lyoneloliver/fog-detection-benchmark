# Ringkasan hasil: tcn-yang-2024

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 113066
- **Total waktu latih:** 1673.09 detik
- **Median waktu inferensi:** 8.55 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9336 | 0.7746 | 0.7602 | 0.9602 | 0.7875 | 0.4094 |

## AUROC per pasien

- **Rerata ± SD:** 0.7806 ± 0.1435 (n = 26)
- **IK bootstrap 95%:** [0.7257, 0.8329]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6990 | 0.9838 | 0.9654 | 0.2105 | 0.9674 | 1.0000 | 52.4465 | 9.2361 |
| 2 | 0.8911 | 0.9809 | 0.9823 | 0.5606 | 0.9664 | 1.0000 | 50.6391 | 29.7375 |
| 3 | 0.4660 | 0.0066 | 0.0000 | 1.0000 | nan | 0.0000 | 52.8290 | 11.4625 |
| 4 | 0.6227 | 0.1715 | 0.1154 | 0.9123 | 0.1403 | 0.0000 | 40.8257 | 8.0644 |
| 5 | 0.7366 | 0.3000 | 0.1053 | 0.9988 | 0.1888 | 0.1818 | 49.2540 | 15.3087 |
| 6 | 0.9213 | 0.0563 | 0.0000 | 1.0000 | nan | 0.0000 | 49.9393 | 15.2229 |
| 7 | 0.6976 | 0.9952 | 0.9885 | 0.0680 | 0.9882 | 1.0000 | 57.4979 | 27.1195 |
| 8 | 0.8520 | 0.8847 | 0.9542 | 0.6303 | 0.8975 | 0.7692 | 54.3465 | 28.0287 |
| 9 | 0.7815 | 0.3372 | 0.3229 | 0.9377 | 0.3268 | 0.2222 | 47.0622 | 7.7709 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 50.9537 | 11.0929 |
| 11 | 0.9921 | 0.9592 | 0.7028 | 0.9997 | 0.8244 | 0.4000 | 80.0800 | 19.3183 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 63.8741 | 10.9433 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 47.1774 | 14.0251 |
| 14 | 0.6963 | 0.4835 | 0.1513 | 0.9819 | 0.2499 | 0.2000 | 48.7416 | 8.4898 |
| 15 | 0.7526 | 0.0687 | 0.0000 | 0.9741 | nan | 0.0000 | 48.7394 | 8.2704 |
| 16 | 0.8637 | 0.7062 | 0.1211 | 1.0000 | 0.2161 | 0.1538 | 44.9168 | 16.9440 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 44.7915 | 9.5640 |
| 18 | 0.9151 | 0.2643 | 0.0000 | 1.0000 | nan | 0.0000 | 39.6929 | 8.3743 |
| 19 | 0.9672 | 0.9995 | 0.9950 | 0.0000 | 0.9897 | 1.0000 | 38.4009 | 9.8560 |
| 20 | 0.7283 | 0.0387 | 0.0000 | 0.9525 | nan | 0.0000 | 40.5869 | 8.2233 |
| 21 | 0.8299 | 0.1479 | 0.0606 | 0.9936 | 0.0978 | 0.0000 | 38.8224 | 8.4188 |
| 22 | nan | nan | nan | 0.9766 | nan | 0.0000 | 41.5518 | 8.4581 |
| 23 | 0.9401 | 0.5437 | 0.2541 | 0.9962 | 0.3817 | 0.0000 | 44.9512 | 8.2976 |
| 24 | 0.4859 | 0.1983 | 0.9282 | 0.0889 | 0.3569 | 0.6667 | 43.9879 | 8.5523 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 41.4119 | 8.4709 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 47.1536 | 14.1576 |
| 27 | 0.8514 | 0.8153 | 0.7929 | 0.6569 | 0.6520 | 0.4651 | 38.6192 | 7.8918 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 49.3255 | 8.4527 |
| 29 | 0.5835 | 0.4233 | 0.1220 | 0.8361 | 0.1777 | 0.1538 | 47.7300 | 9.0176 |
| 30 | 0.9208 | 0.7998 | 0.5294 | 0.9760 | 0.6547 | 0.4615 | 50.7243 | 18.3295 |
| 31 | 0.7611 | 0.3963 | 0.3298 | 0.9935 | 0.4531 | 0.4444 | 50.3272 | 8.1323 |
| 32 | 0.8972 | 0.0231 | 0.0000 | 1.0000 | nan | 0.0000 | 40.3725 | 7.9513 |
| 33 | 0.6120 | 0.5233 | 0.0738 | 0.9859 | 0.1342 | 0.0000 | 43.6720 | 7.8337 |
| 34 | 0.8309 | 0.6329 | 0.2144 | 1.0000 | 0.3531 | 0.0000 | 46.8797 | 8.4586 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 44.7613 | 8.0463 |

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


