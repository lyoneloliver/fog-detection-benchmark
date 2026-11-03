# Ringkasan hasil: cnn-bilstm-attention

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 303186
- **Total waktu latih:** 2142.32 detik
- **Median waktu inferensi:** 9.41 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9440 | 0.8469 | 0.7438 | 0.9659 | 0.7873 | 0.3380 |

## AUROC per pasien

- **Rerata ± SD:** 0.7854 ± 0.1864 (n = 26)
- **IK bootstrap 95%:** [0.7146, 0.8556]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6112 | 0.9732 | 0.9254 | 0.4070 | 0.9500 | 0.8889 | 54.8250 | 8.2225 |
| 2 | 0.9455 | 0.9930 | 0.9350 | 0.7980 | 0.9549 | 0.8571 | 54.7003 | 8.7728 |
| 3 | 0.3320 | 0.0052 | 0.0000 | 1.0000 | nan | 0.0000 | 54.8916 | 10.9207 |
| 4 | 0.6247 | 0.1792 | 0.0000 | 0.9663 | nan | 0.0000 | 56.1721 | 9.2045 |
| 5 | 0.8210 | 0.4938 | 0.3453 | 0.9762 | 0.4412 | 0.3582 | 55.1732 | 11.6029 |
| 6 | 0.9979 | 0.8432 | 0.0000 | 1.0000 | nan | 0.0000 | 55.3415 | 8.8486 |
| 7 | 0.9810 | 0.9997 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 71.9338 | 8.2771 |
| 8 | 0.9157 | 0.9536 | 0.9798 | 0.6287 | 0.9103 | 0.8333 | 52.5178 | 8.4213 |
| 9 | 0.7776 | 0.2941 | 0.3109 | 0.9666 | 0.3744 | 0.0000 | 56.8304 | 9.2078 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 53.0133 | 10.0168 |
| 11 | 0.9754 | 0.9303 | 0.5240 | 1.0000 | 0.6877 | 0.4000 | 53.6935 | 8.4352 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 76.0672 | 13.6246 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 104.7574 | 9.3396 |
| 14 | 0.6005 | 0.3336 | 0.0356 | 1.0000 | 0.0687 | 0.0556 | 53.6115 | 9.3005 |
| 15 | 0.6660 | 0.0622 | 0.0000 | 0.9962 | nan | 0.0000 | 78.9607 | 9.4244 |
| 16 | 0.9079 | 0.7126 | 0.0167 | 1.0000 | 0.0329 | 0.0000 | 57.6472 | 9.5088 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 62.9683 | 10.3476 |
| 18 | 0.9360 | 0.1349 | 0.0000 | 1.0000 | nan | 0.0000 | 62.0286 | 9.2195 |
| 19 | 0.9745 | 0.9996 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 61.4903 | 9.2228 |
| 20 | 0.6770 | 0.0359 | 0.0000 | 0.9992 | nan | 0.0000 | 66.6071 | 9.3027 |
| 21 | 0.9741 | 0.5466 | 0.0404 | 1.0000 | 0.0777 | 0.0000 | 62.7851 | 9.8832 |
| 22 | nan | nan | nan | 1.0000 | nan | 1.0000 | 67.0187 | 10.2563 |
| 23 | 0.9354 | 0.3377 | 0.4751 | 0.9574 | 0.4066 | 0.2222 | 54.8230 | 9.1739 |
| 24 | 0.5620 | 0.3150 | 0.3325 | 0.7290 | 0.2884 | 0.2609 | 58.7686 | 9.4067 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 54.2997 | 9.2928 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 56.4004 | 9.7358 |
| 27 | 0.8488 | 0.8200 | 0.6480 | 0.9161 | 0.7183 | 0.5517 | 63.6327 | 9.6963 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 55.7587 | 9.5120 |
| 29 | 0.5597 | 0.4148 | 0.1418 | 0.8619 | 0.2096 | 0.1622 | 89.6835 | 9.8723 |
| 30 | 0.9300 | 0.8140 | 0.3406 | 0.9947 | 0.5009 | 0.3333 | 56.5740 | 9.5534 |
| 31 | 0.8246 | 0.4384 | 0.0691 | 1.0000 | 0.1294 | 0.0000 | 58.0151 | 9.4335 |
| 32 | 0.7241 | 0.0443 | 0.0000 | 1.0000 | nan | 0.0000 | 60.4349 | 9.4721 |
| 33 | 0.4487 | 0.3751 | 0.3196 | 0.6270 | 0.3190 | 0.2000 | 55.1242 | 8.6896 |
| 34 | 0.8692 | 0.6646 | 0.0000 | 1.0000 | nan | 0.0000 | 52.5521 | 8.5584 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 53.2218 | 9.4222 |

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


