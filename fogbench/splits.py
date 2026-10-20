"""Pembagian data leave-one-subject-out.

Fold yang dihasilkan identik untuk semua pengguna. Itulah sebabnya modul ini ada:
kalau setiap orang membagi sendiri, angkanya tidak dapat dibandingkan.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fold:
    index: int
    test_subject: int
    train_subjects: tuple[int, ...]

    def __post_init__(self):
        assert self.test_subject not in self.train_subjects, \
            "pasien uji tidak boleh ada di daftar pasien latih"


def loso_folds(subjects) -> list[Fold]:
    """Satu fold per pasien, urutan dikunci menurut nomor pasien."""
    subs = sorted(set(int(s) for s in subjects))
    if len(subs) < 3:
        raise ValueError("perlu minimal tiga pasien untuk LOSO yang bermakna")
    return [Fold(i, s, tuple(t for t in subs if t != s)) for i, s in enumerate(subs, start=1)]


def split_recordings(recordings, fold: Fold):
    """Pisahkan daftar rekaman menjadi bagian latih dan bagian uji."""
    train = [r for r in recordings if r.subject in fold.train_subjects]
    test = [r for r in recordings if r.subject == fold.test_subject]
    assert train and test, f"fold {fold.index} kosong pada salah satu sisi"
    assert not ({r.subject for r in train} & {r.subject for r in test}), \
        "kebocoran: ada pasien yang muncul di kedua sisi"
    return train, test
