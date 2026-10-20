from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.signal import find_peaks, resample_poly
from scipy.stats import entropy
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from models.base import FoGModel


class RandomForestFoG(FoGModel):
    name = "random-forest"

    def __init__(self, n_estimators: int = 100, seed: int = 0, target_fs: float = 60.0):
        self.n_estimators = n_estimators
        self.seed = seed
        self.target_fs = target_fs
        self.selector = None
        self.clf = RandomForestClassifier(
            n_estimators=self.n_estimators,
            random_state=self.seed,
            class_weight="balanced_subsample",
            n_jobs=-1,
        )

    @staticmethod
    def _dtw_distance(current: np.ndarray, previous: np.ndarray) -> float:
        current = np.asarray(current, dtype=np.float64)
        previous = np.asarray(previous, dtype=np.float64)
        rows = len(current)
        cols = len(previous)
        costs = np.full((rows + 1, cols + 1), np.inf)
        costs[0, 0] = 0.0

        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                local_cost = abs(current[i - 1] - previous[j - 1])
                costs[i, j] = local_cost + min(
                    costs[i - 1, j],
                    costs[i, j - 1],
                    costs[i - 1, j - 1],
                )

        return float(costs[rows, cols] / (rows + cols))

    @staticmethod
    def _peak_width(segment: np.ndarray, dt: float) -> float:
        if len(segment) == 0:
            return 0.0
        peak_index = int(np.argmax(segment))
        peak_value = float(segment[peak_index])
        if peak_value <= 0:
            return 0.0
        half_power = peak_value / np.sqrt(2.0)
        left = peak_index
        right = peak_index
        while left > 0 and segment[left - 1] >= half_power:
            left -= 1
        while right + 1 < len(segment) and segment[right + 1] >= half_power:
            right += 1
        return float((right - left + 1) * dt)

    @staticmethod
    def _principal_width(fft_values: np.ndarray, peak_index: int, df: float) -> float:
        if len(fft_values) == 0 or fft_values[peak_index] <= 0:
            return 0.0
        half_power = fft_values[peak_index] / np.sqrt(2.0)
        left = peak_index
        right = peak_index
        while left > 0 and fft_values[left - 1] >= half_power:
            left -= 1
        while right + 1 < len(fft_values) and fft_values[right + 1] >= half_power:
            right += 1
        return float((right - left + 1) * df)

    def _extract_features(
        self,
        type_i: np.ndarray,
        type_ii: np.ndarray,
        previous_stride: np.ndarray | None,
        step_time: float,
        stride_time: float,
        fs: float,
    ) -> np.ndarray:
        dt = 1.0 / fs
        duration = len(type_ii) * dt

        std_value = float(np.std(type_i))
        range_value = float(np.ptp(type_i))
        rms_value = float(np.sqrt(np.mean(type_i**2)))

        if len(type_ii) > 2:
            angular_acceleration = np.gradient(type_ii, dt)
            angular_jerk = np.gradient(angular_acceleration, dt)
            squared_jerk = angular_jerk**2
            jerk_value = float(
                0.5
                * dt
                * (
                    0.5 * (squared_jerk[0] + squared_jerk[-1])
                    + np.sum(squared_jerk[1:-1])
                )
            )
            normalized_jerk = jerk_value / duration if duration > 0 else 0.0
        else:
            jerk_value = 0.0
            normalized_jerk = 0.0

        stride_similarity = (
            self._dtw_distance(type_i, previous_stride)
            if previous_stride is not None and len(type_i) and len(previous_stride)
            else 0.0
        )
        peak_height = float(np.max(type_ii)) if len(type_ii) else 0.0
        peak_width = self._peak_width(type_ii, dt)

        centered = type_i - np.mean(type_i)
        fft_values = np.abs(np.fft.rfft(centered))
        freqs = np.fft.rfftfreq(len(type_i), d=dt)
        power = fft_values**2
        total_power = float(np.sum(power))

        if total_power > 0:
            normalized_power = power / total_power
            spectral_entropy = float(entropy(normalized_power + 1e-12))
            low_frequency_ratio = float(
                np.sum(power[freqs <= 2.0]) / total_power
            )
            peak_index = int(np.argmax(fft_values))
            principal_amplitude = float(fft_values[peak_index])
            principal_frequency = float(freqs[peak_index])
            df = float(freqs[1] - freqs[0]) if len(freqs) > 1 else 0.0
            principal_width = self._principal_width(fft_values, peak_index, df)
            weighted_spectral_peak = principal_amplitude * principal_frequency
        else:
            spectral_entropy = 0.0
            low_frequency_ratio = 0.0
            principal_amplitude = 0.0
            principal_frequency = 0.0
            principal_width = 0.0
            weighted_spectral_peak = 0.0

        return np.asarray(
            [
                step_time,
                stride_time,
                std_value,
                range_value,
                rms_value,
                jerk_value,
                normalized_jerk,
                stride_similarity,
                peak_height,
                peak_width,
                spectral_entropy,
                principal_frequency,
                principal_amplitude,
                principal_width,
                weighted_spectral_peak,
                low_frequency_ratio,
            ],
            dtype=np.float32,
        )

    def _resample(self, recording, y: np.ndarray | None = None):
        raw = np.asarray(recording.raw6)
        fs = float(recording.fs)
        if fs == self.target_fs:
            return len(raw), raw, y, fs

        ratio = Fraction(str(self.target_fs)) / Fraction(str(fs))
        resampled = resample_poly(
            raw,
            ratio.numerator,
            ratio.denominator,
            axis=0,
        ).astype(np.float32)

        if y is not None:
            source_indices = np.rint(np.arange(len(resampled)) * fs / self.target_fs).astype(int)
            source_indices = np.clip(source_indices, 0, len(y) - 1)
            y = np.asarray(y)[source_indices]

        return len(resampled), resampled, y, self.target_fs

    def _extract_steps(
        self,
        raw: np.ndarray,
        fs: float,
        y: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray | None, list[tuple[int, int]]]:
        angular_velocity = np.asarray(raw[:, 3], dtype=np.float64)
        signal_range = float(np.ptp(angular_velocity))
        if signal_range > 0:
            angular_velocity = (
                angular_velocity - np.mean(angular_velocity)
            ) / signal_range

        maximum = float(np.max(angular_velocity))
        height_threshold = 0.2 * maximum if maximum > 0 else 0.0
        min_distance = max(1, int(0.35 * fs))
        peaks, _ = find_peaks(
            angular_velocity,
            height=height_threshold,
            distance=min_distance,
        )

        features = []
        labels = []
        bounds = []
        previous_stride = None
        dt = 1.0 / fs

        for i in range(1, len(peaks)):
            previous_peak = int(peaks[i - 1])
            current_peak = int(peaks[i])
            type_i = angular_velocity[previous_peak:current_peak]

            start = current_peak
            while start > 0 and angular_velocity[start] > 0:
                start -= 1
            end = current_peak
            while end < len(angular_velocity) and angular_velocity[end] > 0:
                end += 1
            type_ii = angular_velocity[start:end]

            stride_time = (current_peak - previous_peak) * dt
            step_time = stride_time / 2.0
            features.append(
                self._extract_features(
                    type_i,
                    type_ii,
                    previous_stride,
                    step_time,
                    stride_time,
                    fs,
                )
            )
            bounds.append((previous_peak, current_peak))
            previous_stride = type_i

            if y is not None:
                labels.append(
                    int(np.mean(y[previous_peak:current_peak]) > 0.5)
                )

        feature_array = (
            np.asarray(features, dtype=np.float32)
            if features
            else np.empty((0, 16), dtype=np.float32)
        )
        label_array = np.asarray(labels, dtype=np.int64) if y is not None else None
        return feature_array, label_array, bounds

    def fit(self, recordings: list) -> None:
        features = []
        labels = []

        for recording in recordings:
            _, raw, y, fs = self._resample(recording, y=recording.y)
            step_features, step_labels, _ = self._extract_steps(raw, fs, y)
            if len(step_features):
                features.append(step_features)
                labels.append(step_labels)

        if not features:
            return

        x_train = np.concatenate(features, axis=0)
        y_train = np.concatenate(labels, axis=0)
        tree = DecisionTreeClassifier(
            criterion="gini",
            min_samples_leaf=1,
            max_leaf_nodes=16,
            class_weight="balanced",
            random_state=self.seed,
        )
        tree.fit(x_train, y_train)
        selected = np.flatnonzero(tree.feature_importances_ > 0)
        if len(selected) == 0:
            selected = np.arange(x_train.shape[1])

        self.selector = selected
        self.clf.fit(x_train[:, self.selector], y_train)

    def predict_proba(self, recording) -> np.ndarray:
        if self.selector is None:
            return self.fallback_probabilities(recording)
        original_length = len(recording.raw6)
        n_samples, raw, _, fs = self._resample(recording)
        step_features, _, bounds = self._extract_steps(raw, fs)
        if len(step_features) == 0:
            probabilities = np.zeros(n_samples, dtype=np.float32)
        else:
            class_probabilities = self.clf.predict_proba(
                step_features[:, self.selector]
            )
            positive_class = np.flatnonzero(self.clf.classes_ == 1)
            step_probabilities = (
                class_probabilities[:, positive_class[0]]
                if len(positive_class)
                else np.zeros(len(step_features), dtype=np.float32)
            )
            centers = np.asarray(
                [(start + end) / 2 for start, end in bounds],
                dtype=np.float64,
            )
            probabilities = np.interp(
                np.arange(n_samples, dtype=np.float64),
                centers,
                step_probabilities,
            ).astype(np.float32)

        if len(probabilities) != original_length:
            source_times = np.arange(len(probabilities)) / self.target_fs
            target_times = np.arange(original_length) / float(recording.fs)
            probabilities = np.interp(
                target_times,
                source_times,
                probabilities,
                left=float(probabilities[0]),
                right=float(probabilities[-1]),
            )
        return probabilities.astype(np.float32)

    def card(self) -> dict:
        return {
            "nama": self.name,
            "n_parameter": self.n_estimators,
            "hiperparameter": {
                "n_estimators": self.n_estimators,
                "target_fs": self.target_fs,
                "peak_height_fraction": 0.2,
                "peak_min_distance_sec": 0.35,
                "feature_selection": (
                    "DecisionTree Gini, max_leaf_nodes=16, "
                    "class_weight=balanced"
                ),
                "class_weight": "balanced_subsample",
                "angular_jerk": "0.5 * integral(second_derivative(gyro_x)^2 dt)",
            },
            "deviasi": [
                "Paper Borzi memakai gyroscope angular velocity pada sumbu x dan dua sensor di kedua tulang kering; Figshare hanya menyediakan satu sensor. GYR ML dipakai sebagai pendekatan sumbu x dan step_time diperkirakan sebagai setengah stride_time.",
                "Paper menggunakan Decision Tree untuk ranking fitur dan SVM untuk klasifikasi. Sesuai permintaan, Random Forest menggantikan SVM dan memakai fitur dengan importance positif dari Decision Tree yang dilatih hanya pada data latih. Pohon seleksi diberi class weight agar fitur kelas FoG yang minoritas tidak mudah terabaikan.",
                "Validasi mengikuti LOSO benchmark, bukan prosedur repeated random holdout dan tuning internal 10-fold dalam paper.",
                "Class weighting dipakai untuk membantu ketidakseimbangan kelas; parameter Random Forest tidak dituning dengan prosedur Bayesian paper.",
            ],
        }


def factory(seed: int = 0) -> RandomForestFoG:
    return RandomForestFoG(seed=seed)
