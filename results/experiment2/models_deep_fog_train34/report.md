# Ringkasan hasil: deepfog

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 96522
- **Total waktu latih:** 26052.06 detik
- **Median waktu inferensi:** 86.14 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9459 | 0.8638 | 0.7833 | 0.9547 | 0.7923 | 0.3987 |

## AUROC per pasien

- **Rerata ± SD:** 0.8195 ± 0.1365 (n = 26)
- **IK bootstrap 95%:** [0.7694, 0.8707]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.7008 | 0.9822 | 0.9496 | 0.3474 | 0.9617 | 1.0000 | 338.1874 | 59.4974 |
| 2 | 0.9702 | 0.9962 | 0.9866 | 0.7323 | 0.9781 | 1.0000 | 394.9233 | 63.2685 |
| 3 | 0.8596 | 0.0265 | 0.0000 | 0.9979 | nan | 0.0000 | 421.6029 | 72.1667 |
| 4 | 0.6704 | 0.2121 | 0.1941 | 0.9350 | 0.2448 | 0.2500 | 443.0844 | 74.8956 |
| 5 | 0.8723 | 0.4977 | 0.3267 | 0.9753 | 0.4202 | 0.4286 | 365.3242 | 66.8761 |
| 6 | 0.9872 | 0.2752 | 0.0000 | 1.0000 | nan | 0.0000 | 444.6122 | 70.0995 |
| 7 | 0.9564 | 0.9992 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 1352.8236 | 319.0179 |
| 8 | 0.8965 | 0.9362 | 0.9920 | 0.5402 | 0.8993 | 0.7500 | 1567.4227 | 70.1104 |
| 9 | 0.6784 | 0.2280 | 0.3528 | 0.9469 | 0.3696 | 0.2222 | 492.9491 | 102.4390 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 444.1994 | 76.1066 |
| 11 | 0.9863 | 0.9332 | 0.6374 | 1.0000 | 0.7785 | 0.4000 | 469.9370 | 74.1791 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 379.1041 | 86.1394 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 358.9108 | 79.5790 |
| 14 | 0.6741 | 0.4093 | 0.0504 | 0.9991 | 0.0957 | 0.1053 | 398.0340 | 70.4215 |
| 15 | 0.7988 | 0.0834 | 0.2500 | 0.8836 | 0.1081 | 0.0000 | 1223.3690 | 268.8000 |
| 16 | 0.8800 | 0.6581 | 0.2765 | 0.9893 | 0.4153 | 0.1538 | 1391.8755 | 279.9764 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 1615.2586 | 259.6637 |
| 18 | 0.8268 | 0.1096 | 0.2743 | 0.9701 | 0.1981 | 0.1667 | 1519.5601 | 268.8794 |
| 19 | 0.9688 | 0.9995 | 1.0000 | 0.0000 | 0.9923 | 1.0000 | 1500.9013 | 268.5583 |
| 20 | 0.8247 | 0.0594 | 0.0000 | 0.9631 | nan | 0.0000 | 1332.4000 | 264.8047 |
| 21 | 0.9231 | 0.4795 | 0.4419 | 0.9467 | 0.3007 | 0.2857 | 1481.9275 | 281.1095 |
| 22 | nan | nan | nan | 0.9271 | nan | 0.0000 | 1719.9459 | 270.8361 |
| 23 | 0.8067 | 0.1831 | 0.1243 | 0.9854 | 0.1751 | 0.0000 | 758.6336 | 87.4401 |
| 24 | 0.5996 | 0.3576 | 0.8074 | 0.2393 | 0.3556 | 0.0000 | 421.2238 | 89.3504 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 492.7555 | 139.2205 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 489.7733 | 82.8556 |
| 27 | 0.8963 | 0.8712 | 0.8862 | 0.7360 | 0.7453 | 0.5742 | 661.2048 | 97.7639 |
| 28 | nan | nan | nan | 0.9965 | nan | 0.0000 | 434.8681 | 92.8069 |
| 29 | 0.5468 | 0.4024 | 0.4189 | 0.6708 | 0.4355 | 0.4110 | 446.3838 | 104.2161 |
| 30 | 0.8976 | 0.7646 | 0.6582 | 0.9065 | 0.6580 | 0.4762 | 467.0764 | 282.8323 |
| 31 | 0.7643 | 0.4332 | 0.3528 | 0.9984 | 0.5103 | 0.4444 | 671.5744 | 55.3441 |
| 32 | 0.9659 | 0.0945 | 0.0000 | 0.9986 | nan | 0.0000 | 406.0587 | 67.8468 |
| 33 | 0.5295 | 0.4502 | 0.0000 | 1.0000 | nan | 0.0000 | 420.0484 | 71.8026 |
| 34 | 0.8267 | 0.6772 | 0.6927 | 0.8361 | 0.6001 | 0.5000 | 370.2317 | 77.6936 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 355.8698 | 80.0448 |

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
