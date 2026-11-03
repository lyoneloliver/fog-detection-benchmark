# Ringkasan hasil: cnn-bilstm-attention

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 303186
- **Total waktu latih:** 607.91 detik
- **Median waktu inferensi:** 11.41 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.8065 | 0.5506 | 0.7444 | 0.8019 | 0.5743 | 0.1857 |

## AUROC per pasien

- **Rerata ± SD:** 0.7211 ± 0.1688 (n = 26)
- **IK bootstrap 95%:** [0.6593, 0.7839]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.5383 | 0.9705 | 0.9692 | 0.1018 | 0.9673 | 1.0000 | 11.8184 | 11.4058 |
| 2 | 0.9469 | 0.9936 | 0.4440 | 1.0000 | 0.6149 | 0.0000 | 21.4441 | 9.0949 |
| 3 | 0.3520 | 0.0054 | 0.0000 | 1.0000 | nan | 0.0000 | 9.7279 | 12.3915 |
| 4 | 0.6599 | 0.2195 | 0.0000 | 0.9900 | nan | 0.0000 | 26.1330 | 11.3547 |
| 5 | 0.6797 | 0.2914 | 0.6373 | 0.6163 | 0.2459 | 0.2124 | 18.3510 | 13.8640 |
| 6 | 0.9138 | 0.0503 | 0.0000 | 1.0000 | nan | 0.0000 | 28.0373 | 13.0116 |
| 7 | 0.9640 | 0.9995 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 25.2898 | 13.0567 |
| 8 | 0.8102 | 0.9054 | 0.7836 | 0.6746 | 0.8099 | 0.7483 | 26.1731 | 12.5013 |
| 9 | 0.6371 | 0.2131 | 0.7608 | 0.2312 | 0.1550 | 0.0000 | 7.4877 | 11.6364 |
| 10 | nan | nan | nan | 0.9987 | nan | 0.0000 | 18.4170 | 9.4942 |
| 11 | 0.8435 | 0.6678 | 0.9847 | 0.2079 | 0.2659 | 0.0000 | 13.5106 | 9.0074 |
| 12 | nan | nan | nan | 0.9776 | nan | 0.0000 | 8.0137 | 13.3035 |
| 13 | nan | nan | nan | 0.3008 | nan | 0.0000 | 24.4176 | 9.4421 |
| 14 | 0.6707 | 0.4208 | 0.0256 | 1.0000 | 0.0499 | 0.0000 | 29.8255 | 11.0997 |
| 15 | 0.5177 | 0.0328 | 0.0000 | 1.0000 | nan | 0.0000 | 10.2769 | 10.2333 |
| 16 | 0.8594 | 0.6982 | 0.0916 | 1.0000 | 0.1679 | 0.0000 | 19.1259 | 10.6945 |
| 17 | nan | nan | nan | 0.9919 | nan | 0.0000 | 11.6178 | 13.0408 |
| 18 | 0.7498 | 0.0359 | 0.0000 | 0.9368 | nan | 0.0000 | 7.3433 | 9.2890 |
| 19 | 0.9838 | 0.9997 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 8.9122 | 10.3119 |
| 20 | 0.7804 | 0.0641 | 0.1216 | 0.9780 | 0.1161 | 0.0000 | 9.5260 | 13.6458 |
| 21 | 0.9229 | 0.2980 | 0.3157 | 0.9726 | 0.3027 | 0.2857 | 20.4607 | 13.4026 |
| 22 | nan | nan | nan | 0.9911 | nan | 0.0000 | 8.1670 | 10.9344 |
| 23 | 0.7057 | 0.0928 | 1.0000 | 0.0846 | 0.0975 | 0.0000 | 14.2516 | 9.8639 |
| 24 | 0.6096 | 0.3019 | 1.0000 | 0.0000 | 0.3576 | 0.0000 | 22.2440 | 10.6167 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 16.4017 | 13.1979 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 15.5065 | 10.9789 |
| 27 | 0.7793 | 0.7180 | 0.7186 | 0.5980 | 0.5824 | 0.4390 | 8.8582 | 13.3051 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 35.9559 | 11.0821 |
| 29 | 0.6209 | 0.4498 | 0.0449 | 0.8821 | 0.0732 | 0.0000 | 36.7678 | 11.3872 |
| 30 | 0.7411 | 0.3390 | 0.1245 | 0.9204 | 0.1758 | 0.1558 | 11.5615 | 15.3838 |
| 31 | 0.7585 | 0.1457 | 0.0018 | 0.9882 | 0.0029 | 0.0000 | 20.8140 | 10.1304 |
| 32 | 0.5325 | 0.0049 | 0.0000 | 1.0000 | nan | 0.0000 | 15.3634 | 14.0498 |
| 33 | 0.3819 | 0.2815 | 0.5410 | 0.2986 | 0.3827 | 0.3529 | 14.4496 | 13.1747 |
| 34 | 0.7892 | 0.5822 | 1.0000 | 0.0000 | 0.3473 | 0.0000 | 21.7887 | 14.4075 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 9.8689 | 14.2376 |

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
- **Epochs trained:** 11
- **Seed:** 0
- **Deviasi dari metode acuan:**
  - Paper memakai sembilan kanal akselerometer Daphnet dari tiga posisi sensor. Figshare menyediakan enam kanal akselerometer dan giroskop dari satu sensor tulang kering; semua enam kanal digunakan dan di-resample ke 64 Hz.
  - Label Figshare hanya biner FoG/tidak-FoG, bukan tiga kelas Daphnet. Label window mengikuti mayoritas sampel di dalam window.
  - Outlier ditangani dengan median dan ambang empat simpangan baku; augmentasi rotasi arbitrer diterapkan pada triad akselerometer window FoG hanya ketika FoG menjadi kelas minoritas.
  - Normalisasi z-score memakai statistik rekaman latih saja untuk menangani perbedaan satuan akselerometer dan giroskop di Figshare.
  - Paper mengevaluasi Daphnet; hasil Figshare dengan konfigurasi ini merupakan adaptasi, bukan replikasi angka paper.
  - BiLSTM memakai dua arah secara eksplisit; attention diterapkan pada seluruh keluaran temporal dengan query gabungan state akhir arah maju dan mundur.
  - Threshold dipilih dari prediksi subjek validasi internal yang tidak dipakai untuk pembaruan bobot; jika validasi tidak tersedia karena hanya ada satu subjek latih, runner memakai fallback standarnya.


