# Ringkasan hasil: deepfog

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 96522
- **Total waktu latih:** 11014.17 detik
- **Median waktu inferensi:** 271.68 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9266 | 0.7703 | 0.7797 | 0.9188 | 0.7330 | 0.3347 |

## AUROC per pasien

- **Rerata ± SD:** 0.7780 ± 0.1701 (n = 26)
- **IK bootstrap 95%:** [0.7143, 0.8414]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.5775 | 0.9723 | 1.0000 | 0.1123 | 0.9832 | 0.0000 | 136.4451 | 122.0919 |
| 2 | 0.9727 | 0.9968 | 0.9460 | 0.8838 | 0.9656 | 1.0000 | 178.3294 | 145.4610 |
| 3 | 0.8611 | 0.0433 | 0.0000 | 1.0000 | nan | 0.0000 | 148.8913 | 154.4148 |
| 4 | 0.6090 | 0.1752 | 0.0000 | 0.9757 | nan | 0.0000 | 374.2972 | 281.1636 |
| 5 | 0.8345 | 0.4683 | 0.1173 | 1.0000 | 0.2100 | 0.1818 | 485.4375 | 285.9517 |
| 6 | 0.9998 | 0.9800 | 0.0000 | 1.0000 | nan | 0.0000 | 819.7947 | 261.0451 |
| 7 | 0.2767 | 0.9830 | 1.0000 | 0.0000 | 0.9936 | 0.0000 | 310.1823 | 90.5132 |
| 8 | 0.8564 | 0.9200 | 1.0000 | 0.1902 | 0.8414 | 0.8000 | 117.7532 | 84.7638 |
| 9 | 0.6900 | 0.2642 | 0.4380 | 0.8626 | 0.3044 | 0.1429 | 85.4151 | 94.9190 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 110.2696 | 99.7818 |
| 11 | 0.9908 | 0.9394 | 0.5393 | 1.0000 | 0.7007 | 0.4000 | 114.6044 | 94.3441 |
| 12 | nan | nan | nan | 1.0000 | nan | 1.0000 | 132.9979 | 98.3976 |
| 13 | nan | nan | nan | 0.6958 | nan | 0.0000 | 109.6871 | 103.5359 |
| 14 | 0.7896 | 0.5695 | 0.0564 | 1.0000 | 0.1067 | 0.1081 | 122.6673 | 96.2572 |
| 15 | 0.6772 | 0.0796 | 0.5703 | 0.7416 | 0.1259 | 0.1538 | 112.4134 | 108.9619 |
| 16 | 0.7627 | 0.6036 | 0.3721 | 0.9843 | 0.5123 | 0.3529 | 107.9537 | 101.3264 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 98.2149 | 77.9519 |
| 18 | 0.8520 | 0.0809 | 0.0000 | 1.0000 | nan | 0.0000 | 308.5399 | 478.5674 |
| 19 | 0.9929 | 0.9999 | 0.9862 | 0.7458 | 0.9911 | 1.0000 | 582.0597 | 289.6607 |
| 20 | 0.7759 | 0.0496 | 0.0000 | 0.9382 | nan | 0.0000 | 401.1055 | 459.3219 |
| 21 | 0.9408 | 0.4354 | 1.0000 | 0.6293 | 0.1611 | 0.0000 | 352.7870 | 421.9755 |
| 22 | nan | nan | nan | 0.9896 | nan | 0.0000 | 408.1866 | 276.8170 |
| 23 | 0.6532 | 0.2326 | 0.2348 | 0.9580 | 0.2255 | 0.0000 | 329.7805 | 285.8958 |
| 24 | 0.5341 | 0.3216 | 0.7739 | 0.2833 | 0.3559 | 0.4138 | 721.1748 | 275.6087 |
| 25 | nan | nan | nan | 1.0000 | nan | 1.0000 | 362.8572 | 276.8308 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 306.2516 | 271.6801 |
| 27 | 0.8473 | 0.8337 | 0.6679 | 0.9081 | 0.7263 | 0.5964 | 473.8768 | 274.6240 |
| 28 | nan | nan | nan | 0.9979 | nan | 0.0000 | 450.4756 | 282.3338 |
| 29 | 0.6912 | 0.4939 | 0.5277 | 0.7728 | 0.5626 | 0.4706 | 403.4219 | 269.8583 |
| 30 | 0.8983 | 0.7205 | 0.7559 | 0.8497 | 0.6554 | 0.5833 | 278.9818 | 274.5881 |
| 31 | 0.7008 | 0.3840 | 0.3404 | 0.9949 | 0.4729 | 0.4000 | 621.6383 | 279.5551 |
| 32 | 0.9222 | 0.2210 | 0.0000 | 1.0000 | nan | 0.0000 | 318.4556 | 293.6447 |
| 33 | 0.6403 | 0.5109 | 0.0000 | 1.0000 | nan | 0.0000 | 236.7667 | 284.0959 |
| 34 | 0.8816 | 0.7095 | 0.7819 | 0.7491 | 0.5739 | 0.4444 | 545.0219 | 235.4312 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 347.4350 | 297.2647 |

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
- **Epochs trained:** 11
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
