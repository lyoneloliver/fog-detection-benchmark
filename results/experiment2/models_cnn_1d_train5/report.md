# Ringkasan hasil: cnn1d-oday2022

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 11157
- **Total waktu latih:** 108.12 detik
- **Median waktu inferensi:** 4.47 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.7366 | 0.3500 | 0.6947 | 0.7089 | 0.4724 | 0.1994 |

## AUROC per pasien

- **Rerata ± SD:** 0.6615 ± 0.1570 (n = 26)
- **IK bootstrap 95%:** [0.6004, 0.7212]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.7617 | 0.9891 | 0.9674 | 0.0561 | 0.9656 | 0.8889 | 4.2766 | 5.6896 |
| 2 | 0.8619 | 0.9795 | 0.9753 | 0.5101 | 0.9601 | 0.8571 | 4.1708 | 4.1277 |
| 3 | 0.6998 | 0.0133 | 0.0000 | 1.0000 | nan | 0.0000 | 2.1438 | 4.2248 |
| 4 | 0.5516 | 0.1504 | 0.0000 | 0.9757 | nan | 0.0000 | 4.1102 | 4.9177 |
| 5 | 0.6675 | 0.2548 | 0.0000 | 1.0000 | nan | 0.0000 | 2.9629 | 3.0207 |
| 6 | 0.9990 | 0.9121 | 0.0000 | 1.0000 | nan | 0.0000 | 2.4365 | 3.0351 |
| 7 | 0.8538 | 0.9978 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 2.8008 | 4.6793 |
| 8 | 0.3732 | 0.6546 | 0.6099 | 0.1984 | 0.6151 | 0.6022 | 4.4688 | 3.2398 |
| 9 | 0.4251 | 0.0731 | 0.0000 | 0.9887 | nan | 0.0000 | 4.7848 | 4.6035 |
| 10 | nan | nan | nan | 0.5814 | nan | 0.0000 | 3.3718 | 2.8885 |
| 11 | 0.7770 | 0.6901 | 0.6609 | 0.9015 | 0.5661 | 0.1429 | 6.3162 | 3.3116 |
| 12 | nan | nan | nan | 0.0247 | nan | 0.0000 | 1.8949 | 3.7632 |
| 13 | nan | nan | nan | 0.0169 | nan | 0.0000 | 3.4123 | 4.5189 |
| 14 | 0.4164 | 0.2408 | 0.0615 | 0.9608 | 0.1035 | 0.0482 | 2.4310 | 4.4703 |
| 15 | 0.6662 | 0.0504 | 1.0000 | 0.3715 | 0.0989 | 0.1111 | 1.6801 | 3.7748 |
| 16 | 0.7017 | 0.2627 | 0.0000 | 1.0000 | nan | 0.0000 | 4.2937 | 4.6653 |
| 17 | nan | nan | nan | 0.3497 | nan | 0.0000 | 1.1295 | 4.4676 |
| 18 | 0.7567 | 0.0678 | 0.6283 | 0.7271 | 0.0823 | 0.0000 | 3.6350 | 4.0682 |
| 19 | 0.6993 | 0.9926 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 3.2946 | 5.1000 |
| 20 | 0.6338 | 0.0395 | 0.0863 | 0.9625 | 0.0629 | 0.0000 | 1.9310 | 5.8492 |
| 21 | 0.7559 | 0.0670 | 1.0000 | 0.0774 | 0.0716 | 0.0000 | 3.0138 | 5.6830 |
| 22 | nan | nan | nan | 0.1164 | nan | 0.0000 | 1.7354 | 5.6601 |
| 23 | 0.8520 | 0.2309 | 1.0000 | 0.0000 | 0.0900 | 0.0000 | 2.1207 | 3.7612 |
| 24 | 0.5293 | 0.3296 | 0.7835 | 0.2337 | 0.3454 | 0.3889 | 4.4160 | 3.8228 |
| 25 | nan | nan | nan | 0.6364 | nan | 0.0000 | 4.3630 | 4.5295 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 1.8394 | 3.8272 |
| 27 | 0.6719 | 0.5757 | 0.8250 | 0.3984 | 0.5601 | 0.5053 | 2.3078 | 4.7134 |
| 28 | nan | nan | nan | 0.4928 | nan | 0.0000 | 3.1618 | 4.0320 |
| 29 | 0.6337 | 0.4532 | 0.0310 | 0.8830 | 0.0512 | 0.0000 | 3.6873 | 3.4552 |
| 30 | 0.7983 | 0.5051 | 0.8160 | 0.6448 | 0.5236 | 0.3000 | 1.3264 | 5.8203 |
| 31 | 0.6416 | 0.1654 | 0.6809 | 0.4337 | 0.1074 | 0.0000 | 5.0667 | 3.0171 |
| 32 | 0.4290 | 0.0052 | 0.0000 | 0.9610 | nan | 0.0000 | 2.4237 | 5.0338 |
| 33 | 0.5287 | 0.3474 | 0.7882 | 0.3336 | 0.5237 | 0.4103 | 2.9139 | 5.5334 |
| 34 | 0.5126 | 0.2405 | 1.0000 | 0.0000 | 0.3473 | 0.0000 | 2.7158 | 5.2533 |
| 35 | nan | nan | nan | 0.7100 | nan | 0.0000 | 1.4838 | 4.5978 |

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


