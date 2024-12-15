"""Script for data handling."""

import datetime as dt
import os
import re
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from classes import Section, Subsection

NAME_PATT = re.compile(r"^[a-z][a-z0-9\-\_]*[a-z0-9]$", re.IGNORECASE)


def load_glossary_df(name: str) -> pd.DataFrame:
    """Load and preprocess glossary DataFrame."""
    df = pd.read_csv(f"glossary/{name}.csv")
    prev_len = df.shape[0]

    df = df.drop_duplicates("italiano", keep="first", ignore_index=True)
    print(f"DELETED {prev_len - df.shape[0]} DUPLICATED ROWS")

    df = df.sort_values(["sezione", "sottosezione", "italiano"], ignore_index=True)
    return df


def create_sections_subsections(
    df: pd.DataFrame
) -> tuple[
    list["Section"],
    dict["Section", list["Subsection"]],
    dict["Section", pd.DataFrame]
]:
    """Create sections and subsections of the vocabulary.
    NOTE: df must already be alphabetically ordered.
    """
    # Index: Start of tuple (s, ss) in glossary df
    df_sss = df[["sezione", "sottosezione"]].drop_duplicates(keep="first")
    n_ss = df_sss.shape[0]

    # Index: Start of s in df_sss
    df_s = df_sss["sezione"].reset_index(drop=True).drop_duplicates(keep="first")

    sections = df_s.to_list()
    ixs = df_s.index.to_list()
    ixs_next = ixs[1:] + [-1]

    aux_dfs = {
        s: df_sss.iloc[ix:(n_ss if ix_next == -1 else ix_next)]
        for s, ix, ix_next in zip(sections, ixs, ixs_next)
    }
    subsections = {s: df_aux["sottosezione"].to_list() for s, df_aux in aux_dfs.items()}

    return sections, subsections, aux_dfs


def get_ixs(
    aux_dfs: dict["Section", pd.DataFrame]
) -> tuple[dict["Section", list[int]], list[int], list[int]]:
    """Get indices for the add_ids_to_vocab_df function."""
    orig_ixs = {s: df_aux.index.to_list() for s, df_aux in aux_dfs.items()}
    start_ixs = [s_ixs[0] for s_ixs in orig_ixs.values()]
    next_start_ixs = start_ixs[1:] + [-1]
    return orig_ixs, start_ixs, next_start_ixs


def add_ids_to_vocab_df(
    df: pd.DataFrame,
    orig_ixs: dict["Section", list[int]],
    start_ixs: list[int],
    next_start_ixs: list[int],
) -> pd.DataFrame:
    """Add section and subsection ids to vocabulary df.
    NOTE: df must already be alphabetically ordered.
    """
    df = df.drop(["sezione", "sottosezione"], axis=1)
    df.loc[:, "sezione_id"] = -1
    df.loc[:, "sottosezione_id"] = -1

    sid_col_iat = df.columns.get_loc("sezione_id")
    ssid_col_iat = df.columns.get_loc("sottosezione_id")

    # We modify the original DataFrame with the information we now know
    zip_loop = enumerate(zip(orig_ixs.values(), start_ixs, next_start_ixs))
    for s_id, (ss_ixs, start_ix, next_start_ix) in zip_loop:
        end_ix = df.shape[0] if next_start_ix == -1 else next_start_ix
        df.iloc[start_ix:end_ix, sid_col_iat] = s_id

        next_ss_ixs = ss_ixs[1:] + [-1]
        for ss_id, (ss_ix, next_ss_ix) in enumerate(zip(ss_ixs, next_ss_ixs)):
            ss_end_ix = end_ix if next_ss_ix == -1 else next_ss_ix
            df.iloc[ss_ix:ss_end_ix, ssid_col_iat] = ss_id

    assert not (df["sezione_id"] == -1).any()
    assert not (df["sottosezione_id"] == -1).any()

    return df


def load_history(df: pd.DataFrame, glossary_name: str):
    path_history = f"history/{glossary_name}.csv"

    if os.path.exists(path_history):
        df_history = pd.read_csv(path_history)

        df_history["last_ok"] = pd.to_datetime(df_history["last_ok"])
        df_history["last_not_ok"] = pd.to_datetime(df_history["last_not_ok"])

        df = df.merge(df_history, how="left", on="italiano")
        del df_history

        mask_null = df["ok"].isnull()
        if mask_null.any():
            df.loc[mask_null, "ok"] = 0
            df.loc[mask_null, "not_ok"] = 0
            df = df.astype({"ok": int, "not_ok": int})

            df.loc[mask_null, "last_ok"] = pd.to_datetime(dt.date.today())
            df.loc[mask_null, "last_not_ok"] = pd.to_datetime(dt.date.today())
    else:
        df.loc[:, "ok"] = 0
        df.loc[:, "not_ok"] = 0
        df.loc[:, "last_ok"] = pd.to_datetime(dt.date.today())
        df.loc[:, "last_not_ok"] = pd.to_datetime(dt.date.today())

    return df


# * Functions


def open_glossary(
    name: str,
) -> tuple[
    list["Section"],
    dict["Section", list["Subsection"]],
]:
    """Open glossary file and convert it into Pythonic classes.
    CSV should have the columns: italiano, traduzione, sezione, sottosezione.
    """
    assert NAME_PATT.match(name)
    df = load_glossary_df(name)

    sections, subsections, aux_dfs = create_sections_subsections(df)
    orig_ixs, start_ixs, next_start_ixs = get_ixs(aux_dfs)
    df = add_ids_to_vocab_df(df, orig_ixs, start_ixs, next_start_ixs)

    df = load_history(df, glossary_name=name)

    return df, sections, subsections
