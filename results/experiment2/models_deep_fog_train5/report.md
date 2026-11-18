# Ringkasan hasil: deepfog

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 96522
- **Total waktu latih:** 11120.52 detik
- **Median waktu inferensi:** 166.93 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.8987 | 0.7447 | 0.6963 | 0.9379 | 0.7098 | 0.2822 |

## AUROC per pasien

- **Rerata ± SD:** 0.7517 ± 0.1693 (n = 26)
- **IK bootstrap 95%:** [0.6853, 0.8141]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.8158 | 0.9880 | 0.9826 | 0.3053 | 0.9780 | 0.7273 | 658.6353 | 73.0267 |
| 2 | 0.9374 | 0.9912 | 0.9727 | 0.6111 | 0.9643 | 1.0000 | 712.9117 | 58.7266 |
| 3 | 0.6137 | 0.0114 | 0.0000 | 1.0000 | nan | 0.0000 | 777.3668 | 69.7358 |
| 4 | 0.5758 | 0.1550 | 0.0000 | 0.9781 | nan | 0.0000 | 806.4055 | 94.3592 |
| 5 | 0.7944 | 0.3441 | 0.0000 | 1.0000 | nan | 0.0000 | 359.7730 | 74.9766 |
| 6 | 0.9988 | 0.9073 | 0.0000 | 1.0000 | nan | 0.0000 | 2055.1264 | 71.0080 |
| 7 | 0.2048 | 0.9787 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 145.7188 | 52.4176 |
| 8 | 0.8482 | 0.8972 | 0.4580 | 0.9213 | 0.6129 | 0.2500 | 373.9443 | 250.8238 |
| 9 | 0.6942 | 0.2762 | 0.3288 | 0.9618 | 0.3803 | 0.2500 | 170.9306 | 269.1350 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 324.9913 | 275.9715 |
| 11 | 0.9703 | 0.8913 | 0.4821 | 1.0000 | 0.6506 | 0.4000 | 243.7807 | 258.5964 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 134.7737 | 246.9849 |
| 13 | nan | nan | nan | 0.9708 | nan | 0.0000 | 298.6842 | 659.2762 |
| 14 | 0.7413 | 0.4451 | 0.0000 | 1.0000 | nan | 0.0000 | 595.3112 | 713.2832 |
| 15 | 0.7049 | 0.1015 | 0.0000 | 1.0000 | nan | 0.0000 | 282.9417 | 530.1342 |
| 16 | 0.7558 | 0.5512 | 0.3259 | 0.9889 | 0.4715 | 0.3529 | 270.1300 | 428.2432 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 131.0174 | 430.3915 |
| 18 | 0.7864 | 0.0602 | 0.0000 | 1.0000 | nan | 0.0000 | 319.7713 | 406.1809 |
| 19 | 0.9999 | 1.0000 | 0.9521 | 1.0000 | 0.9755 | 1.0000 | 334.4138 | 428.2601 |
| 20 | 0.8374 | 0.0697 | 0.0000 | 0.9950 | nan | 0.0000 | 142.2855 | 405.9242 |
| 21 | 0.8272 | 0.0873 | 0.0000 | 1.0000 | nan | 0.0000 | 174.1131 | 402.9493 |
| 22 | nan | nan | nan | 0.9896 | nan | 0.0000 | 190.4885 | 446.8559 |
| 23 | 0.8152 | 0.2213 | 0.5691 | 0.7876 | 0.1942 | 0.1818 | 244.0801 | 277.4767 |
| 24 | 0.6526 | 0.4150 | 0.9761 | 0.0786 | 0.3692 | 0.0000 | 277.9907 | 315.5323 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 260.5870 | 61.7843 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 37.5049 | 62.9615 |
| 27 | 0.8879 | 0.8199 | 0.5710 | 0.9585 | 0.6928 | 0.5973 | 55.8384 | 70.8755 |
| 28 | nan | nan | nan | 1.0000 | nan | 1.0000 | 87.2423 | 104.4894 |
| 29 | 0.6260 | 0.4382 | 0.0000 | 0.8795 | nan | 0.0000 | 129.4803 | 136.5522 |
| 30 | 0.9025 | 0.7370 | 0.0437 | 1.0000 | 0.0838 | 0.0000 | 87.1826 | 103.0154 |
| 31 | 0.6540 | 0.3557 | 0.2287 | 0.9979 | 0.3603 | 0.4444 | 204.4324 | 122.4946 |
| 32 | 0.6880 | 0.0187 | 0.0000 | 1.0000 | nan | 0.0000 | 74.1689 | 166.9307 |
| 33 | 0.6157 | 0.4352 | 0.7683 | 0.3759 | 0.5275 | 0.4000 | 55.5274 | 103.4151 |
| 34 | 0.5968 | 0.4151 | 0.6233 | 0.4115 | 0.3250 | 0.0000 | 54.4663 | 100.0137 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 48.5079 | 94.2252 |

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
- **Epochs trained:** 15
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

> 
