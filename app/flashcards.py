"""Script for flashcards code."""

from typing import TYPE_CHECKING

from math import isclose
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


def make_net_weighted_errors_ordering(randomness: float):
    """Make net_weighted_errors_ordering function."""
    assert 0.0 < randomness < 1.0

    def net_weighted_errors_ordering(df_vocab: "DataFrame") -> "ndarray":
        """Flashcard ordering based on weighted net errors and randomness."""
        df = df_vocab[["ok", "not_ok"]].copy()

        df["net_errors"] = df["not_ok"] - df["ok"]
        df["net_errors"] -= df["net_errors"].min()
        ne_avg = df["net_errors"].mean()
        if not isclose(ne_avg, 0.0):
            df["net_errors"] /= 2.0 * ne_avg

        df["random"] = np.random.rand(df.shape[0])
        df["net_errors"] = randomness * df["random"] + (1.0 - randomness) * df["net_errors"]

        df = df.sort_values("net_errors", ascending=False)
        return df.index.values.copy()

    return net_weighted_errors_ordering
