"""Module for data utility functions."""

import datetime as dt
from math import isnan
from typing import TYPE_CHECKING

import pandas as pd

from options import COLUMN

if TYPE_CHECKING:
    from pandas import DataFrame

    from classes import Section, Subsection

# load_glossary_df


def check_na(val) -> bool:
    return isinstance(val, float) and isnan(val)


def check_glossary_duplicates(df: "DataFrame") -> bool:
    prev_len = df.shape[0]
    df.drop_duplicates(COLUMN.ITALIAN, keep="first", ignore_index=True, inplace=True)
    duplicated_rows = prev_len - df.shape[0]
    print(f"DELETED {duplicated_rows} DUPLICATED ROWS")
    return duplicated_rows > 0


def concat_langs(row: pd.Series) -> str:
    """Concatenate the two languages correspondingly."""
    if check_na(row[COLUMN.SPANISH]):
        return row[COLUMN.ENGLISH]
    elif check_na(row[COLUMN.ENGLISH]):
        return row[COLUMN.SPANISH]
    else:
        return f"{row[COLUMN.SPANISH]}, {row[COLUMN.ENGLISH]}"


# create_sections_subsections


def process_sections_subsections(df: "DataFrame") -> tuple["DataFrame", int]:
    # Index: Start of tuple (s, ss) in glossary df
    df_sss = df[["sezione", "sottosezione"]].drop_duplicates(keep="first")
    return df_sss, df_sss.shape[0]


def process_sections(
    df_sss: "DataFrame"
) -> tuple[list["Section"], list[int], list[int]]:
    # Index: Start of s in df_sss
    ser_s = df_sss["sezione"].reset_index(drop=True).drop_duplicates(keep="first")

    sections = ser_s.to_list()
    ixs = ser_s.index.to_list()
    ixs_next = ixs[1:] + [-1]

    return sections, ixs, ixs_next


# add_ids_to_vocab_df


def init_vocab_df(df_: "DataFrame") -> "DataFrame":
    df = df_.drop(["sezione", "sottosezione"], axis=1)
    df.loc[:, "sezione_id"] = -1
    df.loc[:, "sottosezione_id"] = -1
    return df


def init_sss_counts(
    df: "DataFrame",
    subsections: dict["Section", list["Subsection"]],
) -> tuple[list[list[int]], int, int]:
    sss_counts = [
        len(ss_list) * [0]
        for ss_list in subsections.values()
    ]
    sid_col_iat = df.columns.get_loc("sezione_id")
    ssid_col_iat = df.columns.get_loc("sottosezione_id")
    return sss_counts, sid_col_iat, ssid_col_iat


def loop_add_ids(
    df: "DataFrame",
    zip_loop,
    sid_col_iat: int,
    ssid_col_iat: int,
    sss_counts: list[list[int]],
) -> None:
    """We modify the original DataFrame with the information we now know."""
    for s_id, (ss_ixs, start_ix, next_start_ix) in zip_loop:
        end_ix = df.shape[0] if next_start_ix == -1 else next_start_ix
        df.iloc[start_ix:end_ix, sid_col_iat] = s_id

        next_ss_ixs = ss_ixs[1:] + [-1]
        for ss_id, (ss_ix, next_ss_ix) in enumerate(zip(ss_ixs, next_ss_ixs)):
            ss_end_ix = end_ix if next_ss_ix == -1 else next_ss_ix
            df.iloc[ss_ix:ss_end_ix, ssid_col_iat] = ss_id
            sss_counts[s_id][ss_id] = ss_end_ix - ss_ix

    assert not (df["sezione_id"] == -1).any()
    assert not (df["sottosezione_id"] == -1).any()


# load_history


def init_empty_history(df: "DataFrame") -> None:
    today = dt.date.today()
    df.loc[:, "ok"] = 0
    df.loc[:, "not_ok"] = 0
    df.loc[:, "last_ok"] = pd.to_datetime(today)
    df.loc[:, "last_not_ok"] = pd.to_datetime(today)


def check_history_duplicates(df_history: "DataFrame") -> None:
    dupl_words = df_history[COLUMN.ITALIAN].value_counts()
    dupl_words = dupl_words[dupl_words > 1]
    if not dupl_words.empty:
        print("DUPLICATED WORDS IN HISTORY:")
        print(dupl_words)
        raise AssertionError("Duplicated words in history.")


def handle_ok_nulls(df: "DataFrame") -> None:
    mask_null = df["ok"].isnull()
    if mask_null.any():
        df.loc[mask_null, "ok"] = 0
        df.loc[mask_null, "not_ok"] = 0
        df.astype({"ok": int, "not_ok": int}, copy=False)

        df.loc[mask_null, "last_ok"] = pd.to_datetime(dt.date.today())
        df.loc[mask_null, "last_not_ok"] = pd.to_datetime(dt.date.today())
