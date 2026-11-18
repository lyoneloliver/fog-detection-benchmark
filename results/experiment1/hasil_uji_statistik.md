# Tabel Uji Statistik

Uji Wilcoxon bertanda berpasangan antarmetode pada AUROC per pasien (Eksperimen 1, LOSO 35 fold, n = 26 pasien yang memiliki kedua kelas), koreksi Holm atas seluruh 28 pasangan, ukuran efek korelasi rank-biserial berpasangan (r_rb). Selisih = metode A − metode B; IK 95% = bootstrap tingkat pasien (2000 ulangan).

## AUROC per pasien

| Metode | Rerata ± SD | Median |
|---|---|---|
| freeze-index | 0.613 ± 0.152 | 0.611 |
| random-forest | 0.679 ± 0.146 | 0.686 |
| cnn1d-oday2022 | 0.718 ± 0.178 | 0.768 |
| deepfog | 0.819 ± 0.135 | 0.851 |
| cnn-bilstm-attention | 0.794 ± 0.181 | 0.857 |
| transformer | 0.727 ± 0.200 | 0.742 |
| tcn-yang-2024 | 0.783 ± 0.163 | 0.816 |
| tcn-rotation-augmentation | 0.747 ± 0.172 | 0.785 |

## Uji berpasangan (28 pasangan)

| Metode A | Metode B | Selisih rerata ± SD [IK 95%] | A menang | W | p | p Holm | r_rb | Signifikan (Holm) |
|---|---|---|---|---|---|---|---|---|
| freeze-index | random-forest | -0.065 ± 0.193 [-0.142, +0.005] | 11/26 | 115 | 0.1291 | 1.0000 | -0.34 | tidak |
| freeze-index | cnn1d-oday2022 | -0.105 ± 0.165 [-0.166, -0.042] | 7/26 | 62 | 0.0029 | 0.0557 | -0.65 | tidak |
| freeze-index | deepfog | -0.205 ± 0.152 [-0.264, -0.149] | 2/26 | 4 | 0.0000 | 0.0000 | -0.98 | ya |
| freeze-index | cnn-bilstm-attention | -0.181 ± 0.202 [-0.255, -0.102] | 4/26 | 36 | 0.0001 | 0.0035 | -0.79 | ya |
| freeze-index | transformer | -0.114 ± 0.222 [-0.200, -0.029] | 7/26 | 82 | 0.0163 | 0.2450 | -0.53 | tidak |
| freeze-index | tcn-yang-2024 | -0.169 ± 0.180 [-0.237, -0.105] | 3/26 | 34 | 0.0001 | 0.0028 | -0.81 | ya |
| freeze-index | tcn-rotation-augmentation | -0.134 ± 0.235 [-0.219, -0.040] | 3/26 | 51 | 0.0009 | 0.0206 | -0.71 | ya |
| random-forest | cnn1d-oday2022 | -0.039 ± 0.191 [-0.113, +0.033] | 11/26 | 133 | 0.2914 | 1.0000 | -0.24 | tidak |
| random-forest | deepfog | -0.140 ± 0.134 [-0.192, -0.093] | 3/26 | 21 | 0.0000 | 0.0004 | -0.88 | ya |
| random-forest | cnn-bilstm-attention | -0.116 ± 0.177 [-0.179, -0.049] | 2/26 | 47 | 0.0006 | 0.0136 | -0.73 | ya |
| random-forest | transformer | -0.049 ± 0.184 [-0.121, +0.020] | 8/26 | 118 | 0.1499 | 1.0000 | -0.33 | tidak |
| random-forest | tcn-yang-2024 | -0.104 ± 0.105 [-0.142, -0.064] | 5/26 | 35 | 0.0001 | 0.0031 | -0.80 | ya |
| random-forest | tcn-rotation-augmentation | -0.068 ± 0.126 [-0.114, -0.018] | 4/26 | 57 | 0.0018 | 0.0356 | -0.68 | ya |
| cnn1d-oday2022 | deepfog | -0.101 ± 0.147 [-0.159, -0.044] | 5/26 | 56 | 0.0016 | 0.0337 | -0.68 | ya |
| cnn1d-oday2022 | cnn-bilstm-attention | -0.076 ± 0.131 [-0.126, -0.021] | 6/26 | 64 | 0.0036 | 0.0639 | -0.64 | tidak |
| cnn1d-oday2022 | transformer | -0.009 ± 0.116 [-0.051, +0.035] | 13/26 | 160 | 0.7078 | 1.0000 | -0.09 | tidak |
| cnn1d-oday2022 | tcn-yang-2024 | -0.065 ± 0.167 [-0.129, +0.002] | 6/26 | 103 | 0.0669 | 0.8695 | -0.41 | tidak |
| cnn1d-oday2022 | tcn-rotation-augmentation | -0.029 ± 0.224 [-0.109, +0.062] | 8/26 | 120 | 0.1651 | 1.0000 | -0.32 | tidak |
| deepfog | cnn-bilstm-attention | +0.025 ± 0.128 [-0.019, +0.080] | 14/26 | 154 | 0.5995 | 1.0000 | +0.12 | tidak |
| deepfog | transformer | +0.092 ± 0.160 [+0.032, +0.156] | 17/26 | 81 | 0.0151 | 0.2421 | +0.54 | tidak |
| deepfog | tcn-yang-2024 | +0.036 ± 0.111 [-0.007, +0.079] | 14/26 | 120 | 0.1651 | 1.0000 | +0.32 | tidak |
| deepfog | tcn-rotation-augmentation | +0.072 ± 0.165 [+0.017, +0.141] | 17/26 | 95 | 0.0407 | 0.5705 | +0.46 | tidak |
| cnn-bilstm-attention | transformer | +0.067 ± 0.146 [+0.011, +0.123] | 18/26 | 78 | 0.0120 | 0.2034 | +0.56 | tidak |
| cnn-bilstm-attention | tcn-yang-2024 | +0.012 ± 0.142 [-0.042, +0.065] | 15/26 | 159 | 0.6893 | 1.0000 | +0.09 | tidak |
| cnn-bilstm-attention | tcn-rotation-augmentation | +0.047 ± 0.185 [-0.015, +0.123] | 17/26 | 116 | 0.1358 | 1.0000 | +0.34 | tidak |
| transformer | tcn-yang-2024 | -0.055 ± 0.174 [-0.121, +0.013] | 9/26 | 106 | 0.0796 | 0.9549 | -0.40 | tidak |
| transformer | tcn-rotation-augmentation | -0.020 ± 0.213 [-0.093, +0.070] | 10/26 | 128 | 0.2370 | 1.0000 | -0.27 | tidak |
| tcn-yang-2024 | tcn-rotation-augmentation | +0.036 ± 0.117 [-0.004, +0.084] | 17/26 | 110 | 0.0993 | 1.0000 | +0.37 | tidak |

> Interpretasi |r_rb|: kecil ≈ 0,1, sedang ≈ 0,3, besar ≥ 0,5. Tabel sebelumnya hanya membandingkan freeze-index dengan tujuh metode lain (koreksi Holm atas 7 uji) dan tidak memuat ukuran efek; dengan koreksi atas 28 pasangan, freeze-index vs cnn1d-oday2022 dan freeze-index vs transformer tidak lagi signifikan.

