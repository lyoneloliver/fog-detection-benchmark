# Ringkasan hasil: cnn-bilstm-attention

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 303186
- **Total waktu latih:** 2716.42 detik
- **Median waktu inferensi:** 9.09 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9462 | 0.8562 | 0.7500 | 0.9598 | 0.7803 | 0.3391 |

## AUROC per pasien

- **Rerata ± SD:** 0.7942 ± 0.1814 (n = 26)
- **IK bootstrap 95%:** [0.7226, 0.8612]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6112 | 0.9732 | 0.9254 | 0.4070 | 0.9500 | 0.8889 | 66.4668 | 8.4345 |
| 2 | 0.9455 | 0.9930 | 0.9350 | 0.7980 | 0.9549 | 0.8571 | 72.1294 | 9.4333 |
| 3 | 0.3320 | 0.0052 | 0.0000 | 1.0000 | nan | 0.0000 | 68.0388 | 9.1389 |
| 4 | 0.6247 | 0.1792 | 0.0000 | 0.9663 | nan | 0.0000 | 69.8798 | 9.6995 |
| 5 | 0.8210 | 0.4938 | 0.3453 | 0.9762 | 0.4412 | 0.3582 | 71.3608 | 9.2720 |
| 6 | 0.9979 | 0.8432 | 0.0000 | 1.0000 | nan | 0.0000 | 76.6698 | 9.4395 |
| 7 | 0.9810 | 0.9997 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 98.2459 | 8.3764 |
| 8 | 0.9157 | 0.9536 | 0.9798 | 0.6287 | 0.9103 | 0.8333 | 71.0320 | 8.9109 |
| 9 | 0.7679 | 0.2846 | 0.1749 | 0.9836 | 0.2597 | 0.0000 | 85.9197 | 10.5779 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 72.0778 | 9.0876 |
| 11 | 0.9754 | 0.9303 | 0.5240 | 1.0000 | 0.6877 | 0.4000 | 72.4253 | 10.9544 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 92.2243 | 8.9106 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 80.3882 | 10.8150 |
| 14 | 0.6005 | 0.3336 | 0.0356 | 1.0000 | 0.0687 | 0.0556 | 69.2017 | 8.5274 |
| 15 | 0.6660 | 0.0622 | 0.0000 | 0.9962 | nan | 0.0000 | 101.1976 | 11.2298 |
| 16 | 0.9079 | 0.7126 | 0.0167 | 1.0000 | 0.0329 | 0.0000 | 72.3236 | 8.8470 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 80.1807 | 9.3482 |
| 18 | 0.9172 | 0.1074 | 0.0000 | 1.0000 | nan | 0.0000 | 78.7890 | 10.4610 |
| 19 | 0.9717 | 0.9996 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 78.8702 | 9.4859 |
| 20 | 0.7110 | 0.0391 | 0.0000 | 0.9869 | nan | 0.0000 | 73.5537 | 8.9505 |
| 21 | 0.9741 | 0.5466 | 0.0404 | 1.0000 | 0.0777 | 0.0000 | 79.5445 | 9.2469 |
| 22 | nan | nan | nan | 1.0000 | nan | 1.0000 | 85.7487 | 11.1804 |
| 23 | 0.9354 | 0.3377 | 0.4751 | 0.9574 | 0.4066 | 0.2222 | 68.6402 | 8.6947 |
| 24 | 0.5521 | 0.3047 | 0.3792 | 0.6901 | 0.3042 | 0.2449 | 74.0015 | 8.6938 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 67.8366 | 10.5965 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 70.9351 | 8.8838 |
| 27 | 0.8609 | 0.8384 | 0.7112 | 0.9141 | 0.7601 | 0.6015 | 68.1327 | 10.4036 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 66.8395 | 8.8883 |
| 29 | 0.6697 | 0.4839 | 0.0521 | 0.8799 | 0.0843 | 0.0000 | 92.3153 | 9.0279 |
| 30 | 0.9300 | 0.8140 | 0.3406 | 0.9947 | 0.5009 | 0.3333 | 86.3803 | 8.6625 |
| 31 | 0.8529 | 0.4809 | 0.0177 | 1.0000 | 0.0348 | 0.0000 | 81.4395 | 8.9799 |
| 32 | 0.8088 | 0.0166 | 0.0000 | 1.0000 | nan | 0.0000 | 99.3401 | 9.6883 |
| 33 | 0.4487 | 0.3751 | 0.3196 | 0.6270 | 0.3190 | 0.2000 | 73.5540 | 8.6675 |
| 34 | 0.8692 | 0.6646 | 0.0000 | 1.0000 | nan | 0.0000 | 69.4100 | 8.9967 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 81.3292 | 8.9930 |

## Kartu metode

### Hiperparameter

- **Sampling rate hz:** 64
- **Window samples:** 256
- **Window seconds:** 4.0
- **Step samples:** 64
- **Step seconds:** 1.0
- **Convolution filters:** 64, 64, 64
- **Kernel sizes:** 7, 5, 3
- **Se reduction ratio:** 8
- **Lstm hidden units:** 128
- **Lstm bidirectional:** True
- **Attention features:** 256
- **Batch size:** 64
- **Learning rate:** 0.001
- **Max epochs:** 50
- **Patience:** 7
- **Rotation augmentation:** True
- **Imbalance handling:** rotate_minority_class_until_window_counts_match
- **Class weighted loss:** True
- **Epochs trained:** 8
- **Seed:** 0
- **Deviasi dari metode acuan:**
  - Paper memakai sembilan kanal akselerometer Daphnet dari tiga posisi sensor. Figshare menyediakan enam kanal akselerometer dan giroskop dari satu sensor tulang kering; semua enam kanal digunakan dan di-resample ke 64 Hz.
  - Label Figshare hanya biner FoG/tidak-FoG, bukan tiga kelas Daphnet. Label window mengikuti mayoritas sampel di dalam window.
  - Outlier ditangani dengan median dan ambang empat simpangan baku; augmentasi rotasi arbitrer diterapkan pada triad akselerometer window FoG hanya ketika FoG menjadi kelas minoritas.
  - Normalisasi z-score memakai statistik rekaman latih saja untuk menangani perbedaan satuan akselerometer dan giroskop di Figshare.
  - Paper mengevaluasi Daphnet; hasil Figshare dengan konfigurasi ini merupakan adaptasi, bukan replikasi angka paper.
  - BiLSTM memakai dua arah secara eksplisit; attention diterapkan pada seluruh keluaran temporal dengan query gabungan state akhir arah maju dan mundur.
  - Threshold dipilih dari prediksi subjek validasi internal yang tidak dipakai untuk pembaruan bobot; jika validasi tidak tersedia karena hanya ada satu subjek latih, runner memakai fallback standarnya.


