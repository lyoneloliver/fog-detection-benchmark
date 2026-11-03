# Ringkasan hasil: deepfog

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 96522
- **Total waktu latih:** 5499.95 detik
- **Median waktu inferensi:** 23.95 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9449 | 0.8648 | 0.7796 | 0.9548 | 0.7901 | 0.3884 |

## AUROC per pasien

- **Rerata ± SD:** 0.8187 ± 0.1353 (n = 26)
- **IK bootstrap 95%:** [0.7687, 0.8685]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6855 | 0.9808 | 0.9393 | 0.3895 | 0.9571 | 0.8889 | 353.1263 | 20.6730 |
| 2 | 0.9699 | 0.9961 | 0.9913 | 0.6919 | 0.9782 | 1.0000 | 260.0572 | 21.7601 |
| 3 | 0.8435 | 0.0237 | 0.0000 | 0.9958 | nan | 0.0000 | 162.2001 | 22.9315 |
| 4 | 0.6813 | 0.2121 | 0.0549 | 0.9460 | 0.0796 | 0.0000 | 190.0979 | 38.0449 |
| 5 | 0.8759 | 0.4860 | 0.3853 | 0.9667 | 0.4551 | 0.4000 | 155.7342 | 31.7585 |
| 6 | 0.9866 | 0.2656 | 0.0000 | 1.0000 | nan | 0.0000 | 177.2784 | 24.5069 |
| 7 | 0.9549 | 0.9991 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 235.2372 | 29.6769 |
| 8 | 0.8949 | 0.9343 | 0.9832 | 0.6000 | 0.9064 | 0.7500 | 176.4054 | 32.2989 |
| 9 | 0.6825 | 0.2361 | 0.3408 | 0.9538 | 0.3735 | 0.2500 | 210.3527 | 25.0646 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 257.0579 | 27.8820 |
| 11 | 0.9830 | 0.9293 | 0.6701 | 0.9988 | 0.7985 | 0.4000 | 240.4605 | 27.9441 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 182.0861 | 20.9440 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 152.3954 | 39.2274 |
| 14 | 0.6621 | 0.3995 | 0.0986 | 0.9685 | 0.1641 | 0.0930 | 147.7727 | 29.8333 |
| 15 | 0.8298 | 0.1047 | 0.2500 | 0.9224 | 0.1429 | 0.0000 | 129.5004 | 21.8060 |
| 16 | 0.8677 | 0.6519 | 0.2765 | 0.9905 | 0.4173 | 0.1538 | 128.6320 | 23.0043 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 156.0253 | 27.2095 |
| 18 | 0.8254 | 0.1074 | 0.2965 | 0.9415 | 0.1405 | 0.1429 | 126.8340 | 22.7048 |
| 19 | 0.9789 | 0.9997 | 0.9905 | 0.2712 | 0.9896 | 1.0000 | 114.4974 | 20.4914 |
| 20 | 0.8201 | 0.0582 | 0.0000 | 0.9617 | nan | 0.0000 | 120.5855 | 25.3511 |
| 21 | 0.9259 | 0.4864 | 0.4419 | 0.9381 | 0.2778 | 0.2500 | 120.5367 | 26.6300 |
| 22 | nan | nan | nan | 0.9500 | nan | 0.0000 | 133.5552 | 24.6845 |
| 23 | 0.7650 | 0.2518 | 0.2127 | 0.9821 | 0.2702 | 0.0000 | 123.9104 | 20.5743 |
| 24 | 0.5697 | 0.3310 | 0.8074 | 0.2580 | 0.3610 | 0.0000 | 120.1470 | 34.8316 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 125.5852 | 22.6447 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 138.1978 | 22.1746 |
| 27 | 0.8977 | 0.8771 | 0.8680 | 0.7786 | 0.7612 | 0.6091 | 131.7317 | 21.4795 |
| 28 | nan | nan | nan | 0.9958 | nan | 0.0000 | 126.2456 | 22.2805 |
| 29 | 0.5378 | 0.3983 | 0.5013 | 0.5766 | 0.4663 | 0.4364 | 111.3656 | 21.2888 |
| 30 | 0.9015 | 0.7685 | 0.5683 | 0.9390 | 0.6344 | 0.4444 | 110.7582 | 27.0234 |
| 31 | 0.7798 | 0.4315 | 0.3564 | 0.9972 | 0.5050 | 0.4000 | 124.0301 | 23.1784 |
| 32 | 0.9325 | 0.0442 | 0.0000 | 0.9979 | nan | 0.0000 | 123.0562 | 21.6656 |
| 33 | 0.5756 | 0.4580 | 0.0000 | 1.0000 | nan | 0.0000 | 116.4584 | 24.2607 |
| 34 | 0.8592 | 0.6835 | 0.6828 | 0.8599 | 0.6181 | 0.5714 | 108.9958 | 23.5406 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 109.0420 | 23.9454 |

## Kartu metode

### Hiperparameter

- **Arsitektur:** dua cabang Conv1D, ACC dan GYR diproses terpisah
- **Filters per cabang:** 100, 40
- **Kernel size:** 10
- **Max pool size:** 3
- **Average pool size:** 2
- **Global average pooling:** False
- **Temporal features flattened:** True
- **Dropout:** 0.5
- **Window sec:** 3.0
- **Step sec:** 0.25
- **Target fs:** 128.0
- **Batch size:** 32
- **Learning rate:** 0.001
- **Max epochs:** 50
- **Patience:** 7
- **Epochs trained:** 10
- **Class weighted loss:** True
- **Seed:** 0
- **Deviasi dari metode acuan:**
  - Paper DeepFoG memakai satu CNN dengan enam kanal gabungan; adaptasi ini memakai dua cabang terpisah ACC dan GYR sesuai permintaan multi-cabang.
  - Paper memprediksi tiga kelas FoG, Stop, dan Walking-with-Turns dari sensor pergelangan tangan. Figshare hanya memiliki label biner FoG/tidak-FoG dan sensor tulang kering, sehingga output diadaptasi menjadi dua kelas.
  - Window 3 detik mengikuti paper. Paper menyebut overlap 0.25 detik, sedangkan benchmark memakai langkah 0.25 detik (overlap 2.75 detik) untuk mempertahankan resolusi temporal yang lebih rapat; pilihan ini bukan interpretasi literal paper. Label FoG memakai aturan episode utuh atau overlap minimal setengah panjang window.
  - Normalisasi maksimum per kanal dihitung hanya dari rekaman latih untuk menghindari penggunaan statistik pasien validasi/uji.
  - Class-weighted cross entropy ditambahkan untuk ketimpangan kelas; paper menggunakan categorical cross entropy dan tidak menyebut pembobotan kelas.
  - Threshold dipilih dari prediksi pasien validasi internal yang tidak digunakan untuk memperbarui bobot model; pasien uji LOSO tetap tidak digunakan untuk pemilihan threshold.
  - Global average pooling dihilangkan agar fitur urutan waktu dipertahankan sebelum fully connected layer, sesuai alur konvolusi-pooling-dense pada arsitektur paper.


