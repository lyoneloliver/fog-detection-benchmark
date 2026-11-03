# Ringkasan hasil: cnn1d-oday2022

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 11157
- **Total waktu latih:** 1762.18 detik
- **Median waktu inferensi:** 5.37 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.8363 | 0.4925 | 0.8714 | 0.6324 | 0.5059 | 0.1378 |

## AUROC per pasien

- **Rerata ± SD:** 0.7255 ± 0.1679 (n = 26)
- **IK bootstrap 95%:** [0.6620, 0.7864]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.8391 | 0.9927 | 0.9974 | 0.1544 | 0.9827 | 0.6667 | 13.6064 | 4.6179 |
| 2 | 0.8958 | 0.9859 | 0.9890 | 0.1894 | 0.9499 | 1.0000 | 9.6198 | 5.5551 |
| 3 | 0.5624 | 0.0092 | 0.0000 | 0.8514 | nan | 0.0000 | 9.3810 | 5.9519 |
| 4 | 0.5339 | 0.1669 | 0.1996 | 0.9262 | 0.2428 | 0.2500 | 9.2724 | 5.8650 |
| 5 | 0.6138 | 0.2479 | 0.1880 | 0.9693 | 0.2554 | 0.2927 | 9.8237 | 6.3972 |
| 6 | 0.9698 | 0.1574 | 1.0000 | 0.7235 | 0.0649 | 0.0000 | 9.9690 | 4.4789 |
| 7 | 0.8822 | 0.9983 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 11.0373 | 6.6277 |
| 8 | 0.7877 | 0.8740 | 0.9767 | 0.1467 | 0.8228 | 0.6667 | 12.8326 | 6.2265 |
| 9 | 0.4786 | 0.0829 | 0.8102 | 0.1073 | 0.1451 | 0.0000 | 11.0785 | 4.6888 |
| 10 | nan | nan | nan | 0.9919 | nan | 0.0000 | 14.1289 | 4.8316 |
| 11 | 0.7542 | 0.6642 | 0.7242 | 0.4732 | 0.2718 | 0.0645 | 11.0808 | 6.6402 |
| 12 | nan | nan | nan | 0.9958 | nan | 0.0000 | 10.1443 | 6.7137 |
| 13 | nan | nan | nan | 0.0000 | nan | 0.0000 | 11.9899 | 4.7259 |
| 14 | 0.4061 | 0.2279 | 0.5280 | 0.3433 | 0.2872 | 0.0960 | 10.6475 | 7.1709 |
| 15 | 0.6397 | 0.0477 | 1.0000 | 0.1210 | 0.0727 | 0.0000 | 11.5926 | 4.3798 |
| 16 | 0.7798 | 0.5572 | 0.8677 | 0.3144 | 0.3227 | 0.1689 | 12.5987 | 4.7155 |
| 17 | nan | nan | nan | 0.4339 | nan | 0.0000 | 1312.0183 | 7.7697 |
| 18 | 0.7993 | 0.0547 | 0.7124 | 0.7407 | 0.0971 | 0.0000 | 16.1185 | 7.6073 |
| 19 | 0.9954 | 0.9999 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 10.1140 | 5.3872 |
| 20 | 0.8292 | 0.1715 | 0.7176 | 0.7738 | 0.1226 | 0.0839 | 11.3436 | 5.3187 |
| 21 | 0.8159 | 0.1927 | 1.0000 | 0.1236 | 0.0751 | 0.0000 | 12.4943 | 7.2828 |
| 22 | nan | nan | nan | 0.0042 | nan | 0.0000 | 31.1280 | 11.9466 |
| 23 | 0.9261 | 0.3646 | 1.0000 | 0.0000 | 0.0900 | 0.0000 | 31.1199 | 13.4555 |
| 24 | 0.5447 | 0.3399 | 1.0000 | 0.0000 | 0.3576 | 0.0000 | 31.3539 | 5.5425 |
| 25 | nan | nan | nan | 0.5801 | nan | 0.0000 | 14.7149 | 3.9070 |
| 26 | nan | nan | nan | 0.9642 | nan | 0.0000 | 15.9357 | 3.8640 |
| 27 | 0.7282 | 0.6434 | 0.9006 | 0.3328 | 0.5729 | 0.5076 | 9.1522 | 5.8717 |
| 28 | nan | nan | nan | 0.3460 | nan | 0.0000 | 7.8574 | 5.3674 |
| 29 | 0.6265 | 0.4505 | 0.0000 | 1.0000 | nan | 0.0000 | 12.8426 | 3.6759 |
| 30 | 0.8389 | 0.5710 | 0.8755 | 0.6710 | 0.5684 | 0.0000 | 9.1382 | 3.7617 |
| 31 | 0.4616 | 0.1398 | 0.2270 | 0.6614 | 0.0582 | 0.0000 | 9.9667 | 4.1008 |
| 32 | 0.8045 | 0.0154 | 0.0000 | 0.9987 | nan | 0.0000 | 12.5820 | 5.2970 |
| 33 | 0.5148 | 0.4095 | 0.0000 | 1.0000 | nan | 0.0000 | 14.2347 | 4.6268 |
| 34 | 0.8348 | 0.5169 | 1.0000 | 0.0106 | 0.3497 | 0.0000 | 11.3566 | 4.9364 |
| 35 | nan | nan | nan | 0.4151 | nan | 0.0000 | 9.9031 | 4.8121 |

## Kartu metode

### Hiperparameter

- **Window detik:** 2.0
- **Stride detik:** 0.5
- **Sampling rate:** 64
- **Kernel size:** 17
- **Filters:** 16
- **Dropout:** 0.5
- **Batch size:** 512
- **Lr:** 0.001
- **Max epochs:** 50
- **Patience:** 7
- **Seed:** 0
- **Final refit:** all outer-training subjects for selected epoch count
- **Threshold calibration:** held-out inner-training subjects
- **Deviasi dari metode acuan:**
  - Dataset Figshare menggunakan satu lokasi sensor tibia, sedangkan paper O'Day et al. mengevaluasi berbagai kombinasi lokasi IMU (hingga 11 sensor)
  - Arsitektur CNN 1D mempertahankan dua blok konvolusi-pooling (16 filter, kernel 17), dropout 0.5, dan fully connected layer sesuai paper.
  - Sinyal di-resample ke 64 Hz untuk kebutuhan benchmark (data asli paper dikoleksi pada 128 Hz).
  - Penambahan pembobotan sampel kelas (class weighting) untuk menangani ketimpangan kelas pada dataset Figshare[.
  - Validasi internal dan early stopping diterapkan pada subjek latih terpisah untuk mencegah kebocoran data pada pasien uji LOSO.


