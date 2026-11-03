# Ringkasan hasil: random-forest

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 100
- **Total waktu latih:** 6528.89 detik
- **Median waktu inferensi:** 1074.72 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.7087 | 0.3911 | 0.2262 | 0.9519 | 0.3159 | 0.1647 |

## AUROC per pasien

- **Rerata ± SD:** 0.6785 ± 0.1460 (n = 26)
- **IK bootstrap 95%:** [0.6266, 0.7341]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.8676 | 0.9943 | 0.4050 | 1.0000 | 0.5765 | 0.0000 | 228.2193 | 1584.5806 |
| 2 | 0.7216 | 0.9571 | 0.4762 | 0.7904 | 0.6348 | 0.3881 | 241.0306 | 309.0568 |
| 3 | 0.7396 | 0.0421 | 0.2907 | 0.9654 | 0.0986 | 0.0625 | 60.1959 | 885.7140 |
| 4 | 0.5556 | 0.1809 | 0.3260 | 0.7222 | 0.2172 | 0.2000 | 230.1811 | 387.4516 |
| 5 | 0.6900 | 0.1677 | 0.4720 | 0.7641 | 0.2585 | 0.2130 | 162.8938 | 261.7819 |
| 6 | 0.9527 | 0.0859 | 0.0000 | 0.9974 | nan | 0.0000 | 170.9978 | 1123.9061 |
| 7 | 0.4195 | 0.9844 | 0.0360 | 0.9524 | 0.0694 | 0.0000 | 134.9589 | 938.4854 |
| 8 | 0.7032 | 0.8193 | 0.2466 | 0.9123 | 0.3830 | 0.2449 | 129.2766 | 1297.3940 |
| 9 | 0.6077 | 0.1199 | 0.0000 | 0.9914 | nan | 0.0000 | 115.0644 | 301.5879 |
| 10 | nan | nan | nan | 0.9983 | nan | 0.0000 | 77.9894 | 331.9265 |
| 11 | 0.9225 | 0.7797 | 0.5128 | 0.9957 | 0.6649 | 0.3636 | 58.3742 | 257.6263 |
| 12 | nan | nan | nan | 0.9961 | nan | 0.0000 | 194.0446 | 206.2171 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 55.3644 | 431.3377 |
| 14 | 0.5323 | 0.2602 | 0.1194 | 0.9074 | 0.1679 | 0.0000 | 57.4231 | 918.5873 |
| 15 | 0.6426 | 0.0447 | 0.0000 | 0.9526 | nan | 0.0000 | 247.7068 | 1321.5545 |
| 16 | 0.7020 | 0.4082 | 0.1793 | 0.9801 | 0.2799 | 0.0000 | 246.2813 | 1301.2026 |
| 17 | nan | nan | nan | 0.9826 | nan | 0.0000 | 238.7626 | 856.2953 |
| 18 | 0.6383 | 0.0267 | 0.0265 | 0.9768 | 0.0243 | 0.0000 | 197.3524 | 323.5403 |
| 19 | 0.6372 | 0.9925 | 0.2388 | 1.0000 | 0.3856 | 0.0000 | 158.0119 | 2183.9862 |
| 20 | 0.5494 | 0.0258 | 0.0431 | 0.9746 | 0.0399 | 0.0000 | 227.0411 | 1097.6464 |
| 21 | 0.9281 | 0.2065 | 1.0000 | 0.8252 | 0.2894 | 0.0000 | 226.7410 | 1561.5938 |
| 22 | nan | nan | nan | 0.9471 | nan | 0.0000 | 240.2534 | 1681.5091 |
| 23 | 0.6823 | 0.0720 | 0.0414 | 0.9835 | 0.0602 | 0.0000 | 240.9724 | 1162.7194 |
| 24 | 0.4515 | 0.1968 | 0.0120 | 0.9534 | 0.0203 | 0.0000 | 232.3019 | 1419.8246 |
| 25 | nan | nan | nan | 0.9991 | nan | 0.0000 | 251.2127 | 987.6825 |
| 26 | nan | nan | nan | 0.9618 | nan | 0.0000 | 194.1710 | 927.5875 |
| 27 | 0.7691 | 0.6604 | 0.3246 | 0.9413 | 0.4528 | 0.3406 | 235.0137 | 1510.6957 |
| 28 | nan | nan | nan | 0.9786 | nan | 0.0000 | 242.0956 | 1511.3270 |
| 29 | 0.5334 | 0.4579 | 0.2210 | 0.8326 | 0.2991 | 0.1579 | 248.3474 | 1571.1496 |
| 30 | 0.7874 | 0.5868 | 0.3910 | 0.9670 | 0.5173 | 0.2564 | 245.7980 | 380.7788 |
| 31 | 0.7861 | 0.2781 | 0.2394 | 0.9889 | 0.3289 | 0.2000 | 174.4406 | 1091.6107 |
| 32 | 0.6379 | 0.0067 | 0.0690 | 0.9340 | 0.0098 | 0.0000 | 165.3960 | 229.5706 |
| 33 | 0.4460 | 0.2997 | 0.0391 | 0.8443 | 0.0591 | 0.0000 | 58.7472 | 1074.7161 |
| 34 | 0.7386 | 0.3720 | 0.0000 | 0.9980 | nan | 0.0000 | 269.7256 | 1516.9033 |
| 35 | nan | nan | nan | 0.9884 | nan | 0.0000 | 272.5048 | 1319.1455 |

## Kartu metode

### Hiperparameter

- **N estimators:** 100
- **Target fs:** 60.0
- **Peak height fraction:** 0.2
- **Peak min distance sec:** 0.35
- **Feature selection:** DecisionTree Gini, max_leaf_nodes=16, class_weight=balanced
- **Class weight:** balanced_subsample
- **Angular jerk:** 0.5 * integral(second_derivative(gyro_x)^2 dt)
- **Deviasi dari metode acuan:**
  - Paper Borzi memakai gyroscope angular velocity pada sumbu x dan dua sensor di kedua tulang kering; Figshare hanya menyediakan satu sensor. GYR ML dipakai sebagai pendekatan sumbu x dan step_time diperkirakan sebagai setengah stride_time.
  - Paper menggunakan Decision Tree untuk ranking fitur dan SVM untuk klasifikasi. Sesuai permintaan, Random Forest menggantikan SVM dan memakai fitur dengan importance positif dari Decision Tree yang dilatih hanya pada data latih. Pohon seleksi diberi class weight agar fitur kelas FoG yang minoritas tidak mudah terabaikan.
  - Validasi mengikuti LOSO benchmark, bukan prosedur repeated random holdout dan tuning internal 10-fold dalam paper.
  - Class weighting dipakai untuk membantu ketidakseimbangan kelas; parameter Random Forest tidak dituning dengan prosedur Bayesian paper.


