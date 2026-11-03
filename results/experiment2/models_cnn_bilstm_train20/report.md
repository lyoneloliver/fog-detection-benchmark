# Ringkasan hasil: cnn-bilstm-attention

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 303186
- **Total waktu latih:** 1443.88 detik
- **Median waktu inferensi:** 9.05 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9106 | 0.7548 | 0.6750 | 0.9454 | 0.7072 | 0.2906 |

## AUROC per pasien

- **Rerata ± SD:** 0.7626 ± 0.1898 (n = 26)
- **IK bootstrap 95%:** [0.6887, 0.8314]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.4394 | 0.9646 | 1.0000 | 0.0000 | 0.9811 | 0.0000 | 59.7006 | 9.2516 |
| 2 | 0.9255 | 0.9902 | 0.9779 | 0.6919 | 0.9714 | 1.0000 | 60.6788 | 23.3823 |
| 3 | 0.3109 | 0.0052 | 0.0000 | 0.9837 | nan | 0.0000 | 75.9211 | 8.0649 |
| 4 | 0.6260 | 0.1760 | 0.1630 | 0.8543 | 0.1596 | 0.0000 | 74.8481 | 29.2790 |
| 5 | 0.7761 | 0.4071 | 0.2347 | 0.9922 | 0.3592 | 0.1667 | 51.1963 | 7.7550 |
| 6 | 0.9761 | 0.6522 | 0.0000 | 1.0000 | nan | 0.0000 | 35.0512 | 8.0664 |
| 7 | 0.9591 | 0.9995 | 0.2420 | 1.0000 | 0.3897 | 0.0000 | 39.4582 | 9.4538 |
| 8 | 0.8555 | 0.9212 | 0.8870 | 0.6344 | 0.8623 | 0.6522 | 36.8099 | 11.2279 |
| 9 | 0.6862 | 0.2852 | 0.0000 | 1.0000 | nan | 0.0000 | 35.2987 | 9.0240 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 31.1201 | 8.9788 |
| 11 | 0.9795 | 0.9276 | 0.4127 | 1.0000 | 0.5842 | 0.4000 | 36.6953 | 8.9951 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 29.1781 | 8.4671 |
| 13 | nan | nan | nan | 0.9255 | nan | 0.0000 | 31.2204 | 9.8269 |
| 14 | 0.6237 | 0.3670 | 0.0508 | 0.9896 | 0.0936 | 0.0526 | 39.4716 | 8.6378 |
| 15 | 0.4535 | 0.0298 | 0.0000 | 0.9741 | nan | 0.0000 | 41.3442 | 9.0454 |
| 16 | 0.8777 | 0.6754 | 0.2088 | 0.9941 | 0.3370 | 0.1538 | 36.1812 | 8.3707 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 50.5346 | 11.7647 |
| 18 | 0.9178 | 0.1554 | 0.3230 | 0.9798 | 0.2770 | 0.2857 | 42.4391 | 8.6652 |
| 19 | 0.9163 | 0.9987 | 0.9824 | 0.0000 | 0.9834 | 1.0000 | 45.9696 | 9.4854 |
| 20 | 0.6895 | 0.0366 | 0.0000 | 0.9985 | nan | 0.0000 | 36.2159 | 8.2503 |
| 21 | 0.9865 | 0.6903 | 0.9697 | 0.9554 | 0.6019 | 0.2857 | 32.1121 | 9.7806 |
| 22 | nan | nan | nan | 0.9779 | nan | 0.0000 | 36.4696 | 9.3564 |
| 23 | 0.8068 | 0.2087 | 0.4061 | 0.9483 | 0.3315 | 0.0000 | 35.0019 | 9.5267 |
| 24 | 0.6558 | 0.3995 | 0.2967 | 0.8332 | 0.3129 | 0.5263 | 42.6300 | 8.8413 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 41.2719 | 9.8228 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 34.1993 | 10.5487 |
| 27 | 0.8542 | 0.8266 | 0.6856 | 0.9305 | 0.7554 | 0.5323 | 34.7230 | 9.0155 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 32.4688 | 10.2061 |
| 29 | 0.7214 | 0.5243 | 0.5521 | 0.7788 | 0.5839 | 0.5000 | 36.5878 | 9.2031 |
| 30 | 0.9135 | 0.7778 | 0.0000 | 1.0000 | nan | 0.0000 | 38.4138 | 8.8457 |
| 31 | 0.8231 | 0.4359 | 0.0993 | 1.0000 | 0.1806 | 0.0000 | 37.2741 | 8.6890 |
| 32 | 0.8193 | 0.0197 | 0.0000 | 0.9959 | nan | 0.0000 | 48.1747 | 8.4767 |
| 33 | 0.4245 | 0.3645 | 0.0000 | 1.0000 | nan | 0.0000 | 35.4587 | 8.8573 |
| 34 | 0.8095 | 0.6031 | 0.7212 | 0.7425 | 0.5364 | 0.4706 | 33.0289 | 9.2019 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 36.7307 | 9.9316 |

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
- **Epochs trained:** 9
- **Seed:** 0
- **Deviasi dari metode acuan:**
  - Paper memakai sembilan kanal akselerometer Daphnet dari tiga posisi sensor. Figshare menyediakan enam kanal akselerometer dan giroskop dari satu sensor tulang kering; semua enam kanal digunakan dan di-resample ke 64 Hz.
  - Label Figshare hanya biner FoG/tidak-FoG, bukan tiga kelas Daphnet. Label window mengikuti mayoritas sampel di dalam window.
  - Outlier ditangani dengan median dan ambang empat simpangan baku; augmentasi rotasi arbitrer diterapkan pada triad akselerometer window FoG hanya ketika FoG menjadi kelas minoritas.
  - Normalisasi z-score memakai statistik rekaman latih saja untuk menangani perbedaan satuan akselerometer dan giroskop di Figshare.
  - Paper mengevaluasi Daphnet; hasil Figshare dengan konfigurasi ini merupakan adaptasi, bukan replikasi angka paper.
  - BiLSTM memakai dua arah secara eksplisit; attention diterapkan pada seluruh keluaran temporal dengan query gabungan state akhir arah maju dan mundur.
  - Threshold dipilih dari prediksi subjek validasi internal yang tidak dipakai untuk pembaruan bobot; jika validasi tidak tersedia karena hanya ada satu subjek latih, runner memakai fallback standarnya.


