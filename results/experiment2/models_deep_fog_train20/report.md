# Ringkasan hasil: deepfog

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 96522
- **Total waktu latih:** 11680.52 detik
- **Median waktu inferensi:** 82.21 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9414 | 0.8496 | 0.7391 | 0.9718 | 0.7949 | 0.3457 |

## AUROC per pasien

- **Rerata ± SD:** 0.8043 ± 0.1327 (n = 26)
- **IK bootstrap 95%:** [0.7558, 0.8572]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6186 | 0.9764 | 0.9782 | 0.3053 | 0.9758 | 0.7742 | 784.7058 | 280.6325 |
| 2 | 0.9631 | 0.9953 | 0.9890 | 0.6515 | 0.9748 | 1.0000 | 730.2963 | 275.8092 |
| 3 | 0.6029 | 0.0094 | 0.0000 | 1.0000 | nan | 0.0000 | 219.7873 | 86.5294 |
| 4 | 0.6365 | 0.2034 | 0.1795 | 0.9423 | 0.2350 | 0.2857 | 197.5167 | 84.6201 |
| 5 | 0.8501 | 0.4534 | 0.0000 | 1.0000 | nan | 0.0000 | 213.4879 | 70.1486 |
| 6 | 0.9981 | 0.9037 | 0.0000 | 1.0000 | nan | 0.0000 | 257.8695 | 91.8187 |
| 7 | 0.8899 | 0.9984 | 0.8503 | 0.6599 | 0.9169 | 1.0000 | 301.7190 | 87.3002 |
| 8 | 0.8745 | 0.9120 | 0.5244 | 0.8869 | 0.6651 | 0.4444 | 215.9913 | 77.5599 |
| 9 | 0.6974 | 0.3391 | 0.4021 | 0.9049 | 0.3352 | 0.1818 | 154.8710 | 280.7169 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 252.8962 | 71.0028 |
| 11 | 0.9953 | 0.9722 | 0.5965 | 1.0000 | 0.7473 | 0.4000 | 223.0372 | 90.0117 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 276.6128 | 76.5009 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 178.3950 | 83.3023 |
| 14 | 0.7244 | 0.4547 | 0.0679 | 0.9963 | 0.1256 | 0.0550 | 239.4030 | 89.7546 |
| 15 | 0.8038 | 0.0933 | 0.0000 | 0.9461 | nan | 0.0000 | 208.7432 | 82.2078 |
| 16 | 0.8706 | 0.6679 | 0.1857 | 0.9989 | 0.3117 | 0.0000 | 223.8957 | 75.7511 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 203.5118 | 69.4328 |
| 18 | 0.8596 | 0.1390 | 0.2035 | 0.9722 | 0.1570 | 0.0000 | 236.6279 | 71.3481 |
| 19 | 0.9943 | 0.9999 | 0.9862 | 0.8814 | 0.9922 | 1.0000 | 191.0609 | 75.8696 |
| 20 | 0.7977 | 0.0545 | 0.0000 | 0.9979 | nan | 0.0000 | 249.4683 | 73.9256 |
| 21 | 0.8597 | 0.3853 | 0.5429 | 0.8273 | 0.1698 | 0.1379 | 241.2811 | 81.4893 |
| 22 | nan | nan | nan | 0.9458 | nan | 0.0000 | 231.0082 | 70.6680 |
| 23 | 0.7702 | 0.2129 | 0.3453 | 0.9559 | 0.3086 | 0.0000 | 229.8011 | 80.8567 |
| 24 | 0.5818 | 0.3490 | 0.8325 | 0.2410 | 0.3652 | 0.2800 | 198.3631 | 86.8395 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 195.9215 | 72.0125 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 277.3132 | 74.9332 |
| 27 | 0.8914 | 0.8777 | 0.7745 | 0.9418 | 0.8227 | 0.7692 | 225.8287 | 65.3066 |
| 28 | nan | nan | nan | 0.9910 | nan | 0.0000 | 400.0088 | 254.2311 |
| 29 | 0.6536 | 0.4649 | 0.0158 | 0.8761 | 0.0263 | 0.0000 | 658.8306 | 237.9550 |
| 30 | 0.9118 | 0.7634 | 0.5294 | 0.9589 | 0.6303 | 0.4878 | 575.2541 | 268.4699 |
| 31 | 0.7462 | 0.4311 | 0.2855 | 0.9964 | 0.4215 | 0.4000 | 944.0194 | 305.0015 |
| 32 | 0.9525 | 0.0733 | 0.0000 | 1.0000 | nan | 0.0000 | 680.5848 | 269.1898 |
| 33 | 0.6058 | 0.4571 | 0.0000 | 1.0000 | nan | 0.0000 | 741.4878 | 278.9440 |
| 34 | 0.7612 | 0.5530 | 0.3792 | 0.9400 | 0.4726 | 0.4000 | 349.3931 | 62.9395 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 171.5298 | 69.0557 |

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
- **Epochs trained:** 9
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
