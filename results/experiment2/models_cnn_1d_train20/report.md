# Ringkasan hasil: cnn1d-oday2022

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 11157
- **Total waktu latih:** 276.16 detik
- **Median waktu inferensi:** 5.81 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.8336 | 0.4613 | 0.8186 | 0.7845 | 0.5973 | 0.1750 |

## AUROC per pasien

- **Rerata ± SD:** 0.7292 ± 0.1510 (n = 26)
- **IK bootstrap 95%:** [0.6732, 0.7847]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.8767 | 0.9948 | 1.0000 | 0.0000 | 0.9811 | 0.0000 | 10.4869 | 4.0158 |
| 2 | 0.8995 | 0.9858 | 0.0000 | 1.0000 | nan | 0.0000 | 7.6159 | 5.9430 |
| 3 | 0.8479 | 0.0265 | 0.0000 | 1.0000 | nan | 0.0000 | 5.6657 | 5.8073 |
| 4 | 0.4974 | 0.1363 | 0.0458 | 0.9347 | 0.0636 | 0.0000 | 6.8801 | 4.5662 |
| 5 | 0.5773 | 0.2688 | 0.0000 | 1.0000 | nan | 0.0000 | 9.7589 | 6.2571 |
| 6 | 0.9837 | 0.3139 | 0.6712 | 0.9733 | 0.3015 | 0.2000 | 5.1485 | 6.1073 |
| 7 | 0.7938 | 0.9970 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 5.7499 | 6.0667 |
| 8 | 0.8736 | 0.9301 | 1.0000 | 0.0000 | 0.8111 | 0.0000 | 7.8958 | 4.2590 |
| 9 | 0.5583 | 0.1435 | 0.5845 | 0.4096 | 0.1504 | 0.0667 | 9.5631 | 5.9772 |
| 10 | nan | nan | nan | 0.9878 | nan | 0.0000 | 10.0341 | 6.1550 |
| 11 | 0.8017 | 0.6464 | 0.7079 | 0.8990 | 0.5900 | 0.2000 | 10.3784 | 4.4117 |
| 12 | nan | nan | nan | 0.3453 | nan | 0.0000 | 8.9332 | 5.5210 |
| 13 | nan | nan | nan | 0.0000 | nan | 0.0000 | 5.9282 | 6.6247 |
| 14 | 0.5193 | 0.2735 | 0.6593 | 0.3737 | 0.3556 | 0.1325 | 6.6355 | 5.6508 |
| 15 | 0.5349 | 0.0370 | 0.9453 | 0.3219 | 0.0875 | 0.0000 | 9.1798 | 6.0686 |
| 16 | 0.7494 | 0.5537 | 0.7418 | 0.5952 | 0.3890 | 0.1600 | 9.5936 | 5.9456 |
| 17 | nan | nan | nan | 0.4458 | nan | 0.0000 | 8.2970 | 4.4979 |
| 18 | 0.8711 | 0.0863 | 1.0000 | 0.6615 | 0.1057 | 0.0000 | 6.6965 | 5.7192 |
| 19 | 0.9899 | 0.9998 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 5.6604 | 4.3957 |
| 20 | 0.7468 | 0.1250 | 1.0000 | 0.0070 | 0.0436 | 0.0000 | 6.2653 | 5.8132 |
| 21 | 0.7282 | 0.0614 | 1.0000 | 0.2201 | 0.0837 | 0.0000 | 5.1771 | 4.3293 |
| 22 | nan | nan | nan | 0.0414 | nan | 0.0000 | 10.3114 | 5.9079 |
| 23 | 0.7382 | 0.2949 | 0.9586 | 0.1876 | 0.1043 | 0.0000 | 8.5493 | 5.8452 |
| 24 | 0.5587 | 0.3329 | 0.0000 | 1.0000 | nan | 0.0000 | 13.6291 | 4.5956 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 8.5808 | 5.8869 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 7.1794 | 4.1254 |
| 27 | 0.7657 | 0.7017 | 0.9006 | 0.3515 | 0.5793 | 0.5076 | 9.2697 | 5.5507 |
| 28 | nan | nan | nan | 0.0332 | nan | 0.0000 | 5.1662 | 4.8461 |
| 29 | 0.6590 | 0.4632 | 0.8786 | 0.4165 | 0.6337 | 0.4878 | 9.2644 | 4.6928 |
| 30 | 0.8268 | 0.5518 | 0.9205 | 0.5090 | 0.4950 | 0.1039 | 5.2273 | 6.7062 |
| 31 | 0.5704 | 0.1882 | 0.4628 | 0.6459 | 0.1110 | 0.0522 | 5.3534 | 4.3679 |
| 32 | 0.7223 | 0.0169 | 0.0000 | 0.9581 | nan | 0.0000 | 7.5378 | 6.4550 |
| 33 | 0.4835 | 0.3337 | 0.2472 | 0.6596 | 0.2642 | 0.0000 | 9.5981 | 5.9331 |
| 34 | 0.7846 | 0.3955 | 1.0000 | 0.0851 | 0.3677 | 0.0000 | 9.1967 | 4.3287 |
| 35 | nan | nan | nan | 0.2872 | nan | 0.0000 | 5.7501 | 6.1589 |

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


