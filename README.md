# FoG Detection Benchmark

The benchmark runs eight freezing-of-gait (FoG) detection methods from the literature under one shared protocol: leave-one-subject-out (LOSO) validation on the public Figshare turning-in-place IMU dataset (De Souza et al., 2022; 35 people with Parkinson's disease, one shank IMU, 128 Hz).

## Experiments

| Experiment | Question | Runner | Results |
|---|---|---|---|
| 1 | How do the eight methods perform under LOSO, and how does that compare with the numbers in their original papers? | `scripts/run_experiment.py` | `results/experiment1/` |
| 2 | How does performance change with 5, 10, 20 or 34 training patients? (DeepFoG, CNN-BiLSTM-Attention, TCN) | `scripts/run_experiment.py --train-patients N` | `results/experiment2/`, `kurva_pasien/` |
| 3 | How sensitive is the Freeze Index to window length (1/2/4 s), overlap (0/50/75 %) and threshold (1.47 / 2.3 / 3.0 / adaptive)? | `scripts/run_experiment3.py` | `results/experiment3/` |

### Methods (`models/`)

| File | Method | Based on |
|---|---|---|
| `freeze_index.py` | Freeze Index | Moore et al. 2008; Bächlin et al. 2010 |
| `freeze_index3.py` | Freeze Index grid for Experiment 3 | as above; thresholds from Moore 2008, Moore 2013, Zach 2015 |
| `random_forest.py` | Stride features + Random Forest | Borzì et al. 2021 |
| `cnn_1d.py` | 1D CNN | O'Day et al. 2022 |
| `deep_fog.py` | DeepFoG (two-branch CNN adaptation) | Bikias et al. 2021 |
| `cnn_bilstm.py` | CNN-BiLSTM with attention | Li et al. 2020 |
| `transformer.py` | Spectral CNN-Transformer | Sigcha et al. 2022 |
| `tcn.py` | Multi-stage TCN | Yang et al. 2024 |
| `tcn_aug.py` | TCN + rotation augmentation | Yang et al. 2024 + Li et al. 2020 |
| `mds_stgcn.py` | MDS-STGCN (IMU-only adaptation; separate from the 8-method comparison) | Xia & Cao 2026 |
| `example_logreg.py` | Deliberately weak example model, used by the self-test | — |


## Protocol (`config/protocol.yaml`, `fogbench/`)

- LOSO over 35 patients, with seeds 0, 1 and 2. The fold prediction is the mean probability of the three seeds.
- Predictions are evaluated at 32 Hz.
- The decision threshold maximises F1 on the training patients' predictions of a separate seed-0 model. No test-patient data is used to choose it.
- Metrics:
  - pooled AUROC, AUPRC, sensitivity, specificity and F1;
  - episode F1 with a 50 % overlap rule;
  - per-patient AUROC, the primary metric. Only the 26 patients who have FoG are included.
- Pairwise comparisons use the Wilcoxon signed-rank test with Holm correction.

## Installation

```bash
pip install -r requirements.txt
```

For a GPU, install the PyTorch build that matches your CUDA version (see https://pytorch.org/get-started/locally/). The results in the paper used Python 3.10 and torch 2.5.1+cu121.

## Data

1. Download the Figshare dataset (De Souza et al., 2022).
2. Copy `config/paths.example.yaml` to `config/paths.local.yaml`.
3. Set `figshare:` to the folder that contains `IMU/IMU/SUB*_*.txt`.
4. Check the data:

```bash
python scripts/check_data.py --dataset figshare
```

## Running

```bash
# Check
python scripts/selftest.py

# Experiment 1: 
python scripts/run_experiment.py --model models.deep_fog --dataset figshare --out results/experiment1/models_deep_fog

# Experiment 2:
python scripts/run_experiment.py --model models.deep_fog --dataset figshare --train-patients 5 --out results/experiment2/models_deep_fog_train5

# Experiment 3: 
python scripts/run_experiment3.py --out results/experiment3

# Validate and summarise a result folder
python scripts/validate_results.py results/experiment1/models_deep_fog --n-fold 35
python scripts/summarize_results.py results/experiment1/models_deep_fog --out results/experiment1/models_deep_fog/report.md
```

Add `--resume` to continue an interrupted run; folds that are already finished are skipped.

Deep models train on the GPU when one is available. With torch 2.5.1 / cuDNN 9.1, DeepFoG's second convolution hits a very slow cuDNN kernel. If DeepFoG training is unusually slow, run it with `torch.backends.cudnn.enabled = False`. This changes only the convolution kernel used, not the model; 

## Repository layout

```
config/          dataset description, evaluation protocol, local data paths (paths.local.yaml is not tracked)
fogbench/        data loading, LOSO splits, evaluation, metrics, thresholds, reports
models/          one file per method (FoGModel interface in base.py)
scripts/         runners, validation, summaries, data checks, self-test
results/         Markdown summaries of Experiments 1-3 and MDS-STGCN
kurva_pasien/    Experiment 2 learning curves 
```
