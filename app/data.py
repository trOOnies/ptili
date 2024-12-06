"""Script for data handling."""

import re
from typing import TYPE_CHECKING, Literal

import pandas as pd

if TYPE_CHECKING:
    from classes import Section, Subsection
    from states import GlossaryStates, SSStates

NAME_PATT = re.compile(r"^[a-z][a-z0-9\-\_]*[a-z0-9]$", re.IGNORECASE)


def load_glossary_df(name: str) -> pd.DataFrame:
    """Load and preprocess glossary DataFrame."""
    assert NAME_PATT.match(name)

    df = pd.read_csv(f"glossary/{name}.csv")
    prev_len = df.shape[0]

    df = df.drop_duplicates("italiano", keep="first", ignore_index=True)
    print(f"DELETED {prev_len - df.shape[0]} DUPLICATED ROWS")

    df = df.sort_values(["sezione", "sottosezione", "italiano"], ignore_index=True)
    print(df)

    return df


def process_sections(
    df: pd.DataFrame
) -> tuple[
    pd.DataFrame,
    list["Section"],
    dict["Section", list["Subsection"]],
]:
    """Process sections. df must already be alphabetically ordered."""
    # TODO: Check if new function works

    # Index: Start of tuple (s, ss) in glossary df
    df_sss = df[["sezione", "sottosezione"]].drop_duplicates(keep="first")
    n_ss = df_sss.shape[0]

    # Index: Start of s in df_sss
    df_s = df_sss["sezione"].reset_index(drop=True).drop_duplicates(keep="first")

    sections = df_s.to_list()
    ixs = df_s.index.to_list()
    ixs_next = ixs[1:] + [-1]

    aux = {
        s: df_sss.iloc[ix:(n_ss if ix_next == -1 else ix_next)]
        for s, ix, ix_next in zip(sections, ixs, ixs_next)
    }
    subsections = {s: df_aux["sottosezione"].to_list() for s, df_aux in aux.items()}

    # We modify the original DataFrame with the information we now know
    orig_ixs = {s: df_aux.index.to_list() for s, df_aux in aux.items()}
    start_ixs = [s_ixs[0] for s_ixs in orig_ixs.values()]
    next_start_ixs = start_ixs[1:] + [-1]

    df.loc[:, "sezione_id"] = -1
    df.loc[:, "sottosezione_id"] = -1

    zip_loop = enumerate(zip(orig_ixs.values(), start_ixs, next_start_ixs))
    for s_id, (ss_ixs, start_ix, next_start_ix) in zip_loop:
        end_ix = df.shape[0] if next_start_ix == -1 else next_start_ix
        df["sezione_id"].iloc[start_ix:end_ix] = s_id

        next_ss_ixs = ss_ixs[1:] + [-1]
        for ss_id, (ss_ix, next_ss_ix) in enumerate(zip(ss_ixs, next_ss_ixs)):
            ss_end_ix = end_ix if next_ss_ix == -1 else next_ss_ix
            df["sottosezione_id"].iloc[ss_ix:ss_end_ix] = ss_id

    assert not (df["sezione_id"] == -1).any()
    assert not (df["sottosezione_id"] == -1).any()

    return df, sections, subsections


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
    df = load_glossary_df(name)
    df, sections, subsections = process_sections(df)
    return df, sections, subsections


class ReviewCameriere:
    """Sets the order of the review flashcards."""
    def __init__(
        self,
        glossary_states: "GlossaryStates",
        ss_states: "SSStates",
        ordering: Literal["alphabetic"],
    ):
        self.glossary_states = glossary_states
        self.ss_states = ss_states

        if ordering == "alphabetic":
            from flashcards import alphabetic_ordering
            self._next = alphabetic_ordering
        else:
            raise ValueError(f"Ordering not recognized: '{ordering}'")

    def current_word(self) -> str:
        """Get current word to review."""
        sss_tree = self.glossary_states.sss_tree.value
        return self.ss_states.get_word(sss_tree)

    def current_translation(self) -> str:
        """Get translation of the current word."""
        sss_tree = self.glossary_states.sss_tree.value
        return self.ss_states.get_translation(sss_tree)

    def next(self) -> list:
        """Choose next word to review and return the relevant Gradio States."""
        return self._next(self)
