# Ringkasan hasil: tcn-rotation-augmentation

- **Dataset:** figshare
- **Fold tersedia:** 35
- **Jumlah parameter:** 113066
- **Total waktu latih:** 45638.93 detik
- **Median waktu inferensi:** 10.01 ms

## Metrik gabungan

| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |
|---:|---:|---:|---:|---:|---:|
| 0.9314 | 0.7435 | 0.7943 | 0.9316 | 0.7611 | 0.4828 |

## AUROC per pasien

- **Rerata ± SD:** 0.7468 ± 0.1721 (n = 26)
- **IK bootstrap 95%:** [0.6809, 0.8124]

| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.7696 | 0.9852 | 0.9590 | 0.2877 | 0.9656 | 0.8571 | 1728.9281 | 16.4834 |
| 2 | 0.8763 | 0.9826 | 0.9884 | 0.4167 | 0.9617 | 0.8000 | 1763.5375 | 43.5627 |
| 3 | 0.6612 | 0.0100 | 0.0000 | 0.9389 | nan | 0.0000 | 2678.1194 | 8.0117 |
| 4 | 0.5787 | 0.1483 | 0.6136 | 0.5498 | 0.2834 | 0.0000 | 1894.3440 | 14.6530 |
| 5 | 0.8282 | 0.4172 | 0.7813 | 0.7312 | 0.3664 | 0.1231 | 1845.9090 | 12.7294 |
| 6 | 0.9587 | 0.1022 | 0.0000 | 1.0000 | nan | 0.0000 | 1240.6214 | 13.0615 |
| 7 | 0.6370 | 0.9934 | 0.9893 | 0.0000 | 0.9882 | 0.8000 | 1276.1815 | 11.9163 |
| 8 | 0.8321 | 0.8856 | 0.8630 | 0.6820 | 0.8582 | 1.0000 | 1210.5148 | 21.1962 |
| 9 | 0.6476 | 0.2249 | 0.2661 | 0.9696 | 0.3358 | 0.0000 | 1159.0250 | 11.6711 |
| 10 | nan | nan | nan | 1.0000 | nan | 1.0000 | 1175.1011 | 10.8160 |
| 11 | 0.9850 | 0.9127 | 0.6425 | 0.9907 | 0.7533 | 0.5714 | 1232.0967 | 10.0193 |
| 12 | nan | nan | nan | 0.9938 | nan | 0.0000 | 1562.4559 | 9.7715 |
| 13 | nan | nan | nan | 1.0000 | nan | 1.0000 | 1173.4772 | 10.3540 |
| 14 | 0.7267 | 0.4799 | 0.2807 | 0.9450 | 0.3844 | 0.4097 | 1150.5710 | 9.9192 |
| 15 | 0.6567 | 0.0459 | 0.0000 | 0.9933 | nan | 0.0000 | 1210.0012 | 10.4366 |
| 16 | 0.8124 | 0.5938 | 0.3888 | 0.9877 | 0.5357 | 0.4800 | 1293.2066 | 8.9996 |
| 17 | nan | nan | nan | 1.0000 | nan | 1.0000 | 1101.5764 | 9.5647 |
| 18 | 0.9086 | 0.3484 | 0.5487 | 0.9895 | 0.5288 | 0.5000 | 1051.2235 | 9.3830 |
| 19 | 0.2716 | 0.9787 | 0.7928 | 0.0000 | 0.8768 | 0.6667 | 1140.3224 | 9.9617 |
| 20 | 0.6195 | 0.0337 | 0.0000 | 0.9885 | nan | 0.0000 | 1055.2656 | 10.4042 |
| 21 | 0.9871 | 0.6561 | 1.0000 | 0.8543 | 0.3282 | 0.0000 | 1053.5589 | 15.6660 |
| 22 | nan | nan | nan | 0.9794 | nan | 0.0000 | 1090.0098 | 8.8824 |
| 23 | 0.7123 | 0.0814 | 0.0000 | 1.0000 | nan | 0.0000 | 1062.9809 | 8.9896 |
| 24 | 0.4092 | 0.1729 | 0.6675 | 0.4078 | 0.3517 | 0.4615 | 1095.3509 | 9.8812 |
| 25 | nan | nan | nan | 0.9872 | nan | 0.0000 | 1056.5415 | 9.5892 |
| 26 | nan | nan | nan | 1.0000 | nan | 1.0000 | 1057.3864 | 15.4524 |
| 27 | 0.8762 | 0.8384 | 0.8476 | 0.7580 | 0.7375 | 0.5946 | 1058.8530 | 9.3983 |
| 28 | nan | nan | nan | 0.9977 | nan | 0.0000 | 1033.4713 | 9.5495 |
| 29 | 0.6492 | 0.4893 | 0.5416 | 0.7065 | 0.5439 | 0.5932 | 1087.6828 | 9.9060 |
| 30 | 0.9180 | 0.7582 | 0.8215 | 0.8019 | 0.6451 | 0.5070 | 1067.3410 | 10.0143 |
| 31 | 0.8324 | 0.2456 | 0.4433 | 0.9378 | 0.3344 | 0.2927 | 1039.3144 | 9.8162 |
| 32 | 0.8551 | 0.0307 | 0.0000 | 1.0000 | nan | 0.0000 | 1039.3763 | 16.8904 |
| 33 | 0.6085 | 0.4030 | 0.7624 | 0.3807 | 0.5261 | 0.5714 | 1109.9234 | 10.0977 |
| 34 | 0.7997 | 0.6717 | 0.2255 | 0.9901 | 0.3572 | 0.0000 | 1108.2124 | 8.6692 |
| 35 | nan | nan | nan | 1.0000 | nan | 1.0000 | 2736.4473 | 9.7125 |

## Kartu metode

### Hiperparameter

- **Hidden features:** 32
- **Tcn layers:** 5
- **Kernel size:** 3
- **Dilation:** 1, 3, 9, 27, 81
- **Window samples:** 256
- **Target fs hz:** 64
- **Batch size:** 1024
- **Epochs:** 15
- **Optimizer:** Amsgrad (beta=(0.9, 0.999))
- **Learning rate:** 0.0005
- **Learning rate decay per epoch:** 0.95
- **Loss:** class-weighted cross-entropy
- **Trained epochs:** 15
- **Refinement stages:** 4
- **Refinement layers per stage:** 8
- **Refinement dilation:** 1, 2, 4, 8, 16, 32, 64, 128
- **Refinement batch size:** 1
- **Refinement loss:** weighted cross-entropy + smoothing (tau=4, lambda=0.15)
- **Refinement epochs trained:** 15
- **Threshold calibration:** held-out training subjects
- **Augmentasi:** Rotasi arbitrer 3D pada sampel FoG tambahan hingga jumlah kelas seimbang
- **Deviasi dari metode acuan:**
  - Li et al. (2020) mengusulkan augmentasi rotasi arbitrer untuk menyeimbangkan sampel FoG, tetapi arsitektur paper adalah SEC-ALSTM, bukan TCN; model ini memakai initial-prediction dan refinement MS-TCN Yang et al. (2024).
  - Paper Li memakai Daphnet dengan sembilan kanal akselerometer; Figshare menyediakan satu IMU dengan enam kanal; rotasi diterapkan pada triad akselerometer Figshare, bukan kanal giroskop.
  - Pembentukan sampel mengikuti antarmuka prediksi per-sampel TCN benchmark, bukan segmentasi 256-frame dengan langkah 4 yang dipakai pada eksperimen Li.
  - Augmentasi rotasi diterapkan pada training initial TCN; refinement tetap dilatih pada recording asli agar target temporal dan kontinuitas sinyal tidak berubah.
  - Evaluasi mengikuti LOSO Figshare dan protokol threshold benchmark, bukan evaluasi Daphnet Li.


