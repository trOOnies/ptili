"""Script for flashcards code."""

from math import isclose
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy import ndarray
    from pandas import DataFrame


def random_ordering(df_vocab: "DataFrame") -> "ndarray":
    """Flashcard ordering based on pure randomness."""
    return df_vocab.index.to_series().sample(frac=1).values.copy()


def alphabetic_ordering(df_vocab: "DataFrame") -> "ndarray":
    """Flashcard ordering based on alphabetic ordering."""
    return df_vocab.index.values.copy()


def net_errors_ordering(df_vocab: "DataFrame") -> "ndarray":
    """Flashcard ordering based on net errors."""
    df = df_vocab[["ok", "not_ok"]].copy()
    df["net_errors"] = df["not_ok"] - df["ok"]
    df["random"] = np.random.rand(df.shape[0])
    df = df.sort_values(["net_errors", "random"], ascending=False)
    return df.index.values.copy()


def make_net_weighted_errors_ordering(randomness_sigma: float):
    """Make net_weighted_errors_ordering function."""
    assert 0.0 < randomness_sigma < 5.0

    def net_weighted_errors_ordering(df_vocab: "DataFrame") -> "ndarray":
        """Flashcard ordering based on weighted net errors and randomness."""
        df = df_vocab[["ok", "not_ok"]].copy()

        df["net_errors"] = df["not_ok"] - df["ok"]
        ne_std = df["net_errors"].std()
        if not isclose(ne_std, 0.0):
            ne_avg = df["net_errors"].mean()
            df["net_errors"] = (df["net_errors"] - ne_avg) / ne_std
            df["net_errors"] += np.random.normal(loc=0.0, scale=randomness_sigma, size=df.shape[0])
            df = df.sort_values("net_errors", ascending=False)

        return df.index.values.copy()

    return net_weighted_errors_ordering
