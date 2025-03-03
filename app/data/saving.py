"""Saving data functions."""

from typing import TYPE_CHECKING

from options.COLUMN import ITALIAN

if TYPE_CHECKING:
    from pandas import DataFrame


def vocab_to_history(df_vocab: "DataFrame") -> "DataFrame":
    df_history = df_vocab[[ITALIAN, "ok", "not_ok", "last_ok", "last_not_ok"]].copy()
    df_history = df_history[df_history[["ok", "not_ok"]].sum(axis=1) > 0]
    return df_history


def save_history(df_hist: "DataFrame", glossary_name: str) -> None:
    df_hist.to_csv(f"history/{glossary_name}.csv", index=False)
    print("History saved succesfully.")
