"""Script for flashcards code."""

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy import ndarray
    from pandas import DataFrame


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
