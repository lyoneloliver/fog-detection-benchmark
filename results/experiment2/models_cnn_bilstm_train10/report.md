# Ringkasan hasil: cnn-bilstm-attention

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 303186
- **Total waktu latih:** 1052.18 detik
- **Median waktu inferensi:** 10.32 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9075 | 0.7572 | 0.7774 | 0.8765 | 0.6742 | 0.3429 |

## AUROC per pasien

- **Rerata ± SD:** 0.7546 ± 0.1705 (n = 26)
- **IK bootstrap 95%:** [0.6851, 0.8195]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.4156 | 0.9585 | 0.8549 | 0.1544 | 0.9059 | 0.7500 | 23.9429 | 10.3191 |
| 2 | 0.8626 | 0.9771 | 0.5633 | 0.8535 | 0.7130 | 0.4000 | 31.6980 | 8.8075 |
| 3 | 0.3882 | 0.0057 | 0.0000 | 1.0000 | nan | 0.0000 | 28.0346 | 9.2593 |
| 4 | 0.5667 | 0.1574 | 0.0000 | 0.9964 | nan | 0.0000 | 24.8911 | 10.4831 |
| 5 | 0.8107 | 0.4506 | 0.1627 | 0.9993 | 0.2782 | 0.1818 | 31.8506 | 10.1587 |
| 6 | 0.9967 | 0.7604 | 0.0000 | 1.0000 | nan | 0.0000 | 37.2168 | 9.9400 |
| 7 | 0.6774 | 0.9948 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 33.9724 | 11.6846 |
| 8 | 0.8517 | 0.9272 | 0.5733 | 0.9123 | 0.7103 | 0.4308 | 30.0137 | 13.2033 |
| 9 | 0.6894 | 0.2704 | 0.6472 | 0.5119 | 0.1914 | 0.0645 | 15.0166 | 10.0901 |
| 10 | nan | nan | nan | 0.9990 | nan | 0.0000 | 27.0124 | 10.4436 |
| 11 | 0.9364 | 0.7460 | 0.4014 | 1.0000 | 0.5729 | 0.4000 | 23.9722 | 10.1023 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 31.7656 | 10.1026 |
| 13 | nan | nan | nan | 0.9893 | nan | 0.0000 | 40.1391 | 10.9056 |
| 14 | 0.7993 | 0.5334 | 0.0000 | 1.0000 | nan | 0.0000 | 25.9518 | 10.0666 |
| 15 | 0.5732 | 0.0368 | 0.2812 | 0.7543 | 0.0669 | 0.0000 | 23.9791 | 10.5010 |
| 16 | 0.8474 | 0.6093 | 1.0000 | 0.0000 | 0.2809 | 0.0000 | 47.7722 | 10.0046 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 25.4599 | 11.0362 |
| 18 | 0.8785 | 0.0897 | 0.0000 | 1.0000 | nan | 0.0000 | 31.0996 | 10.2933 |
| 19 | 0.9784 | 0.9997 | 0.9889 | 0.1780 | 0.9880 | 1.0000 | 21.6403 | 12.2423 |
| 20 | 0.6472 | 0.0292 | 0.0000 | 0.9862 | nan | 0.0000 | 22.2961 | 11.1757 |
| 21 | 0.9031 | 0.3830 | 0.9949 | 0.6759 | 0.1793 | 0.0000 | 23.6072 | 10.0430 |
| 22 | nan | nan | nan | 0.9990 | nan | 0.0000 | 38.6579 | 10.7264 |
| 23 | 0.9292 | 0.2790 | 0.0442 | 0.9899 | 0.0708 | 0.0000 | 20.3935 | 10.2368 |
| 24 | 0.5297 | 0.3294 | 0.9175 | 0.0826 | 0.3519 | 0.0000 | 36.1102 | 9.9888 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 28.2953 | 9.6551 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 32.8821 | 11.0707 |
| 27 | 0.8348 | 0.7938 | 0.4022 | 0.9709 | 0.5523 | 0.3504 | 24.4204 | 10.0169 |
| 28 | nan | nan | nan | 0.9751 | nan | 0.0000 | 44.3216 | 10.1188 |
| 29 | 0.7180 | 0.5177 | 1.0000 | 0.0000 | 0.5661 | 0.0000 | 43.9186 | 11.2552 |
| 30 | 0.9143 | 0.7824 | 0.9532 | 0.6836 | 0.6126 | 0.0000 | 20.8498 | 10.2702 |
| 31 | 0.8115 | 0.3891 | 0.2766 | 0.9826 | 0.3425 | 0.2105 | 41.3736 | 11.9729 |
| 32 | 0.6712 | 0.0075 | 0.0000 | 1.0000 | nan | 0.0000 | 20.8566 | 13.0297 |
| 33 | 0.5490 | 0.4336 | 0.0915 | 0.9606 | 0.1573 | 0.0000 | 17.1978 | 10.3584 |
| 34 | 0.8386 | 0.6794 | 1.0000 | 0.0544 | 0.3601 | 0.0000 | 40.1855 | 27.1857 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 41.3810 | 26.3149 |

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
- **Epochs trained:** 10
- **Seed:** 0
- **Deviasi dari metode acuan:**
  - Paper memakai sembilan kanal akselerometer Daphnet dari tiga posisi sensor. Figshare menyediakan enam kanal akselerometer dan giroskop dari satu sensor tulang kering; semua enam kanal digunakan dan di-resample ke 64 Hz.
  - Label Figshare hanya biner FoG/tidak-FoG, bukan tiga kelas Daphnet. Label window mengikuti mayoritas sampel di dalam window.
  - Outlier ditangani dengan median dan ambang empat simpangan baku; augmentasi rotasi arbitrer diterapkan pada triad akselerometer window FoG hanya ketika FoG menjadi kelas minoritas.
  - Normalisasi z-score memakai statistik rekaman latih saja untuk menangani perbedaan satuan akselerometer dan giroskop di Figshare.
  - Paper mengevaluasi Daphnet; hasil Figshare dengan konfigurasi ini merupakan adaptasi, bukan replikasi angka paper.
  - BiLSTM memakai dua arah secara eksplisit; attention diterapkan pada seluruh keluaran temporal dengan query gabungan state akhir arah maju dan mundur.
  - Threshold dipilih dari prediksi subjek validasi internal yang tidak dipakai untuk pembaruan bobot; jika validasi tidak tersedia karena hanya ada satu subjek latih, runner memakai fallback standarnya.


