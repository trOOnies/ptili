"""Module for data handling."""

import os
import re
from typing import TYPE_CHECKING

import pandas as pd

from data.utils import (
    check_glossary_duplicates,
    check_history_duplicates,
    concat_langs,
    handle_ok_nulls,
    loop_add_ids,
    init_empty_history,
    init_sss_counts,
    init_vocab_df,
    process_sections,
    process_sections_subsections,
)
from options import COLUMN  # TODO

if TYPE_CHECKING:
    from classes import Section, Subsection

NAME_PATT = re.compile(r"^[a-z][a-z0-9\-\_]*[a-z0-9]$", re.IGNORECASE)
GLOSSARY_COLS = [COLUMN.ITALIAN, COLUMN.CEFR, COLUMN.SPANISH, COLUMN.ENGLISH, COLUMN.SECTION, COLUMN.SUBSECTION]


def load_glossary_df(name: str) -> pd.DataFrame:
    """Load and preprocess glossary DataFrame."""
    df = pd.read_csv(f"glossary/{name}.csv", usecols=GLOSSARY_COLS, sep=";")
    had_duplicates = check_glossary_duplicates(df)

    # TODO: Implement language selection
    df[COLUMN.TRANSLATION] = df[[COLUMN.SPANISH, COLUMN.ENGLISH]].apply(concat_langs, axis=1)

    df = df.sort_values([COLUMN.SECTION, COLUMN.SUBSECTION, COLUMN.ITALIAN], ignore_index=True)
    if had_duplicates:
        df[GLOSSARY_COLS].to_csv("new_glossario.csv", index=False, sep=";")
        print("Glossary without duplicates saved.")

    df = df.drop([COLUMN.SPANISH, COLUMN.ENGLISH], axis=1)
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
    df_sss, n_ss = process_sections_subsections(df)
    sections, ixs, ixs_next = process_sections(df_sss)
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
    subsections: dict["Section", list["Subsection"]],
) -> tuple[pd.DataFrame, list[list[int]]]:
    """Add section and subsection ids to vocabulary df.
    NOTE: df must already be alphabetically ordered.
    """
    df = init_vocab_df(df)
    sss_counts, sid_col_iat, ssid_col_iat = init_sss_counts(df, subsections)

    # We modify the original DataFrame with the information we now know
    zip_loop = enumerate(zip(orig_ixs.values(), start_ixs, next_start_ixs))
    loop_add_ids(df, zip_loop, sid_col_iat, ssid_col_iat, sss_counts)

    return df, sss_counts


def load_history(df: pd.DataFrame, glossary_name: str) -> pd.DataFrame:
    """Load history DataFrame and merge it with the vocabulary DataFrame."""
    path_history = f"history/{glossary_name}.csv"

    if not os.path.exists(path_history):
        init_empty_history(df)
    else:
        df_history = pd.read_csv(path_history)
        check_history_duplicates(df_history)

        df_history["last_ok"] = pd.to_datetime(df_history["last_ok"])
        df_history["last_not_ok"] = pd.to_datetime(df_history["last_not_ok"])

        df = df.merge(df_history, how="left", on=COLUMN.ITALIAN)
        del df_history

        handle_ok_nulls(df)

    return df


# * Functions


def open_glossary(
    name: str,
) -> tuple[
    pd.DataFrame,
    list["Section"],
    dict["Section", list["Subsection"]],
    list[list[int]],
]:
    """Open glossary file and convert it into pythonic classes.
    CSV should have the columns: italiano, traduzione, sezione, sottosezione.
    """
    assert NAME_PATT.match(name)
    df = load_glossary_df(name)

    sections, subsections, aux_dfs = create_sections_subsections(df)
    orig_ixs, start_ixs, next_start_ixs = get_ixs(aux_dfs)
    df, sss_counts = add_ids_to_vocab_df(df, orig_ixs, start_ixs, next_start_ixs, subsections)

    df = load_history(df, glossary_name=name)

    return df, sections, subsections, sss_counts
