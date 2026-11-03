# Ringkasan hasil: cnn1d-oday2022

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 11157
- **Total waktu latih:** 163.49 detik
- **Median waktu inferensi:** 4.20 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.7313 | 0.4009 | 0.6956 | 0.7087 | 0.4727 | 0.2040 |

## AUROC per pasien

- **Rerata ± SD:** 0.7014 ± 0.1782 (n = 26)
- **IK bootstrap 95%:** [0.6356, 0.7701]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6763 | 0.9824 | 0.9413 | 0.1544 | 0.9538 | 0.8889 | 4.8136 | 4.0041 |
| 2 | 0.8887 | 0.9848 | 0.8438 | 0.7449 | 0.9009 | 0.6667 | 3.9227 | 4.1199 |
| 3 | 0.5812 | 0.0095 | 0.0000 | 1.0000 | nan | 0.0000 | 4.8980 | 4.1023 |
| 4 | 0.5599 | 0.1675 | 0.0000 | 1.0000 | nan | 0.0000 | 5.0795 | 3.9972 |
| 5 | 0.7532 | 0.3782 | 0.0920 | 0.9984 | 0.1663 | 0.0000 | 3.1890 | 4.3186 |
| 6 | 0.9316 | 0.0720 | 1.0000 | 0.7615 | 0.0745 | 0.0000 | 3.7401 | 4.3099 |
| 7 | 0.8833 | 0.9984 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 5.0253 | 4.0522 |
| 8 | 0.7702 | 0.8380 | 0.0000 | 0.9877 | nan | 0.0000 | 4.1323 | 5.0389 |
| 9 | 0.5325 | 0.1098 | 0.6786 | 0.2430 | 0.1412 | 0.0606 | 4.2943 | 4.4821 |
| 10 | nan | nan | nan | 0.9958 | nan | 0.0000 | 2.5825 | 6.2459 |
| 11 | 0.7309 | 0.6396 | 0.7835 | 0.3508 | 0.2516 | 0.1212 | 3.9372 | 4.8345 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 7.0286 | 5.3921 |
| 13 | nan | nan | nan | 0.0000 | nan | 0.0000 | 6.3790 | 5.0804 |
| 14 | 0.3964 | 0.2275 | 0.1769 | 0.6916 | 0.1618 | 0.0741 | 4.4838 | 4.2958 |
| 15 | 0.4829 | 0.0327 | 0.8203 | 0.3769 | 0.0825 | 0.0000 | 3.9446 | 3.6863 |
| 16 | 0.7529 | 0.4935 | 0.3992 | 0.8962 | 0.4135 | 0.2857 | 3.2340 | 4.1583 |
| 17 | nan | nan | nan | 0.3630 | nan | 0.0000 | 3.7015 | 5.7830 |
| 18 | 0.8695 | 0.0900 | 0.7035 | 0.8300 | 0.1380 | 0.0000 | 4.1983 | 4.2029 |
| 19 | 0.9907 | 0.9999 | 0.9915 | 0.4068 | 0.9911 | 0.7500 | 8.3062 | 4.7212 |
| 20 | 0.7504 | 0.1012 | 0.8627 | 0.2921 | 0.0521 | 0.0000 | 8.9076 | 2.8778 |
| 21 | 0.9778 | 0.5508 | 1.0000 | 0.3019 | 0.0925 | 0.0000 | 2.8597 | 4.1763 |
| 22 | nan | nan | nan | 0.8753 | nan | 0.0000 | 3.3724 | 5.1014 |
| 23 | 0.5997 | 0.0708 | 0.2541 | 0.8069 | 0.0986 | 0.0000 | 3.4158 | 4.8658 |
| 24 | 0.4590 | 0.2814 | 1.0000 | 0.0000 | 0.3576 | 0.0000 | 5.5723 | 3.7675 |
| 25 | nan | nan | nan | 0.9877 | nan | 0.0000 | 2.7824 | 3.8983 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 5.4224 | 5.2407 |
| 27 | 0.8098 | 0.7523 | 0.5150 | 0.9438 | 0.6360 | 0.4688 | 4.8199 | 3.9985 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 6.5883 | 4.9047 |
| 29 | 0.6683 | 0.4726 | 0.1900 | 0.8348 | 0.2633 | 0.0000 | 3.4819 | 3.6986 |
| 30 | 0.8065 | 0.5488 | 0.8051 | 0.6948 | 0.5509 | 0.2727 | 2.7974 | 5.0789 |
| 31 | 0.5118 | 0.1747 | 0.3918 | 0.5483 | 0.0771 | 0.0833 | 7.0252 | 4.1253 |
| 32 | 0.4761 | 0.0057 | 0.0000 | 0.9972 | nan | 0.0000 | 4.4072 | 3.6651 |
| 33 | 0.4804 | 0.3917 | 0.9764 | 0.0125 | 0.5156 | 0.0000 | 4.3579 | 3.8177 |
| 34 | 0.8966 | 0.7298 | 0.7410 | 0.8958 | 0.6949 | 0.6667 | 4.3669 | 3.9457 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 6.4244 | 4.2092 |

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


