# Ringkasan hasil: cnn1d-oday2022

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 11157
- **Total waktu latih:** 1722.37 detik
- **Median waktu inferensi:** 15.03 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.7959 | 0.4018 | 0.8912 | 0.5590 | 0.4716 | 0.1152 |

## AUROC per pasien

- **Rerata ± SD:** 0.7180 ± 0.1783 (n = 26)
- **IK bootstrap 95%:** [0.6478, 0.7833]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.8901 | 0.9952 | 0.9978 | 0.0561 | 0.9811 | 0.6667 | 74.8584 | 14.7084 |
| 2 | 0.8985 | 0.9862 | 0.9893 | 0.1869 | 0.9500 | 1.0000 | 42.6929 | 15.4971 |
| 3 | 0.3801 | 0.0066 | 0.0000 | 0.5955 | nan | 0.0000 | 51.4198 | 17.9599 |
| 4 | 0.5479 | 0.1679 | 0.2161 | 0.8901 | 0.2300 | 0.2000 | 48.6660 | 18.3457 |
| 5 | 0.5990 | 0.2294 | 0.1867 | 0.9558 | 0.2341 | 0.2553 | 45.7501 | 15.3560 |
| 6 | 0.8884 | 0.0457 | 1.0000 | 0.5366 | 0.0398 | 0.0000 | 47.3638 | 15.7365 |
| 7 | 0.8981 | 0.9984 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 36.5860 | 15.3241 |
| 8 | 0.7476 | 0.8382 | 0.9027 | 0.2893 | 0.8083 | 0.7692 | 52.3833 | 15.8822 |
| 9 | 0.5950 | 0.1240 | 1.0000 | 0.0729 | 0.1707 | 0.0000 | 69.6414 | 14.3214 |
| 10 | nan | nan | nan | 0.9714 | nan | 0.0000 | 71.7450 | 13.4817 |
| 11 | 0.8584 | 0.7543 | 0.8498 | 0.5422 | 0.3411 | 0.0375 | 58.8676 | 14.8170 |
| 12 | nan | nan | nan | 0.9958 | nan | 0.0000 | 34.6738 | 14.1458 |
| 13 | nan | nan | nan | 0.0000 | nan | 0.0000 | 44.6891 | 14.2700 |
| 14 | 0.3721 | 0.2131 | 0.4950 | 0.3132 | 0.2646 | 0.1016 | 41.7693 | 15.4062 |
| 15 | 0.5486 | 0.0384 | 1.0000 | 0.1810 | 0.0777 | 0.0000 | 51.5330 | 14.8510 |
| 16 | 0.7702 | 0.5361 | 0.8677 | 0.3519 | 0.3347 | 0.2355 | 49.8762 | 14.2250 |
| 17 | nan | nan | nan | 0.4586 | nan | 0.0000 | 54.3855 | 14.7471 |
| 18 | 0.8216 | 0.0578 | 0.9779 | 0.5533 | 0.0805 | 0.0000 | 52.3198 | 15.9771 |
| 19 | 0.9959 | 0.9999 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 38.3481 | 14.5968 |
| 20 | 0.8424 | 0.1498 | 0.7804 | 0.7150 | 0.1086 | 0.1017 | 43.8910 | 15.1272 |
| 21 | 0.7311 | 0.1212 | 1.0000 | 0.1564 | 0.0778 | 0.0000 | 62.5848 | 15.3866 |
| 22 | nan | nan | nan | 0.1289 | nan | 0.0000 | 44.3204 | 18.2282 |
| 23 | 0.9265 | 0.3667 | 1.0000 | 0.0000 | 0.0900 | 0.0000 | 51.0045 | 13.2875 |
| 24 | 0.5554 | 0.3400 | 1.0000 | 0.0000 | 0.3576 | 0.0000 | 51.5155 | 16.4354 |
| 25 | nan | nan | nan | 0.7727 | nan | 0.0000 | 72.0505 | 14.4428 |
| 26 | nan | nan | nan | 0.8643 | nan | 0.0000 | 43.0885 | 15.1582 |
| 27 | 0.7655 | 0.6948 | 0.9120 | 0.3097 | 0.5703 | 0.5000 | 37.5822 | 14.5755 |
| 28 | nan | nan | nan | 0.2972 | nan | 0.0000 | 38.7934 | 13.9558 |
| 29 | 0.6050 | 0.4400 | 0.0000 | 1.0000 | nan | 0.0000 | 64.2908 | 15.2340 |
| 30 | 0.8389 | 0.5709 | 0.8755 | 0.6711 | 0.5685 | 0.0000 | 36.1595 | 15.1548 |
| 31 | 0.4613 | 0.1398 | 0.2270 | 0.6614 | 0.0582 | 0.0000 | 33.1815 | 15.4491 |
| 32 | 0.7848 | 0.0139 | 0.0000 | 0.9973 | nan | 0.0000 | 38.5374 | 13.2778 |
| 33 | 0.5157 | 0.4247 | 0.6959 | 0.2527 | 0.4539 | 0.5333 | 55.6078 | 14.0925 |
| 34 | 0.8293 | 0.5026 | 1.0000 | 0.0155 | 0.3509 | 0.0000 | 39.5233 | 15.0335 |
| 35 | nan | nan | nan | 0.3891 | nan | 0.0000 | 42.6739 | 14.1322 |

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


