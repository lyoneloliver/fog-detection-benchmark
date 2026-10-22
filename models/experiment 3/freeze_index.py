from __future__ import annotations

import numpy as np
from scipy import signal

from models.base import FoGModel


class FreezeIndex(FoGModel):
    name = "freeze-index"

    def __init__(
        self,
        seed: int = 0,
        window_sec: float = 4.0,
        overlap: float = 0.5,
        threshold: float | str = "adaptive",
        locomotor_band: tuple[float, float] = (0.5, 3.0),
        freeze_band: tuple[float, float] = (3.0, 8.0),
    ):
        self.seed = seed
        self.window_sec = float(window_sec)
        self.overlap = float(overlap)
        self.step_sec = self.window_sec * (1.0 - self.overlap)
        self.threshold = threshold
        self.locomotor_band = locomotor_band
        self.freeze_band = freeze_band

    @property
    def decision_threshold(self) -> float | None:
        if self.threshold == "adaptive":
            return None
        return float(self.threshold) / (1.0 + float(self.threshold))

    def fit(self, recordings: list) -> None:
        return None

    @staticmethod
    def _band_power(
        freqs: np.ndarray,
        psd: np.ndarray,
        band: tuple[float, float],
    ) -> float:
        mask = (freqs >= band[0]) & (freqs <= band[1])
        if np.count_nonzero(mask) < 2:
            return 0.0
        band_freqs = freqs[mask]
        band_psd = np.sum(psd[mask], axis=1)
        return float(
            np.sum((band_psd[1:] + band_psd[:-1]) * np.diff(band_freqs)) / 2
        )

    def _compute_fi(self, segment: np.ndarray, fs: int) -> float:
        freqs, psd = signal.welch(
            segment,
            fs=fs,
            nperseg=len(segment),
            axis=0,
            detrend="constant",
            scaling="density",
        )
        locomotor_power = self._band_power(freqs, psd, self.locomotor_band)
        freeze_power = self._band_power(freqs, psd, self.freeze_band)
        minimum_power = np.finfo(float).tiny
        if locomotor_power <= minimum_power:
            return float("inf") if freeze_power > minimum_power else 0.0
        return freeze_power / locomotor_power

    def predict_proba(self, recording) -> np.ndarray:
        raw6 = np.asarray(recording.raw6)
        fs = int(recording.fs)
        n_samples = len(raw6)
        if n_samples == 0:
            return np.empty(0, dtype=np.float32)

        acc_si = raw6[:, 2:3].astype(np.float64, copy=False)
        win_len = max(1, int(round(self.window_sec * fs)))
        step_len = max(1, int(round(self.step_sec * fs)))

        if n_samples < win_len:
            starts = [0]
        else:
            starts = list(range(0, n_samples - win_len + 1, step_len))
            last_start = n_samples - win_len
            if starts[-1] != last_start:
                starts.append(last_start)

        centers = []
        scores = []
        for start in starts:
            segment = acc_si[start:start + win_len]
            if len(segment) < win_len:
                pad_mode = "reflect" if len(segment) > 1 else "edge"
                segment = np.pad(
                    segment,
                    ((0, win_len - len(segment)), (0, 0)),
                    mode=pad_mode,
                )
            fi = self._compute_fi(segment, fs)
            centers.append(start + (win_len - 1) / 2)
            scores.append(1.0 if np.isinf(fi) else fi / (1.0 + fi))

        sample_positions = np.arange(n_samples, dtype=np.float64)
        scores_per_sample = np.interp(sample_positions, centers, scores)
        return scores_per_sample.astype(np.float32)

    def card(self) -> dict:
        if self.threshold == "adaptive":
            threshold = "adaptive, dipilih benchmark dari data latih"
        else:
            threshold = f"FI >= {self.threshold} (skor >= {self.decision_threshold:.4f})"
        return {
            "nama": self.name,
            "n_parameter": 0,
            "hiperparameter": {
                "window_sec": self.window_sec,
                "overlap": self.overlap,
                "step_sec": self.step_sec,
                "locomotor_band": self.locomotor_band,
                "freeze_band": self.freeze_band,
                "power_axes": "ACC SI (raw6[:, 2])",
                "score_mapping": "FI / (1 + FI)",
                "threshold": threshold,
            },
            "deviasi": [
                "Durasi jendela diuji pada 1, 2, dan 4 detik.",
                "Jarak antarjendela ditentukan dari overlap 0, 50, dan 75 persen.",
                "Ambang FI tetap 1.47, 2.3, dan 3.0 dipetakan ke skala skor FI / (1 + FI); ambang adaptive dipilih benchmark dari data latih.",
                "Sumbu akselerometer ACC SI digunakan sebagai kanal analisis.",
                "Skor dihitung secara offline dan diinterpolasikan ke setiap sampel.",
                "Threshold tidak menggunakan label pasien uji.",
            ],
        }


def factory(seed: int = 0, **kwargs) -> FreezeIndex:
    return FreezeIndex(seed=seed, **kwargs)


CONFIGS = {
    f"window_{window:g}s_overlap_{int(overlap * 100)}_threshold_{threshold}": {
        "model_kwargs": {
            "window_sec": window,
            "overlap": overlap,
            "threshold": threshold,
        },
        "experiment_config": {
            "window_sec": window,
            "overlap": overlap,
            "step_sec": window * (1.0 - overlap),
            "threshold": threshold,
        },
    }
    for window in [1.0, 2.0, 4.0]
    for overlap in [0.0, 0.5, 0.75]
    for threshold in [1.47, 2.3, 3.0, "adaptive"]
}
