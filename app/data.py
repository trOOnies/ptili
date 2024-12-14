"""Script for data handling."""

import re
from typing import TYPE_CHECKING, Literal

import pandas as pd

if TYPE_CHECKING:
    from classes import Section, Subsection
    from states import SSStates

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
    # TODO: Check if new function works

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
    # TODO: Check if new function works
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
    # TODO: Check if new function works

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
    sections, subsections, aux_dfs = create_sections_subsections(df)
    orig_ixs, start_ixs, next_start_ixs = get_ixs(aux_dfs)
    df = add_ids_to_vocab_df(df, orig_ixs, start_ixs, next_start_ixs)
    return df, sections, subsections


class ReviewCameriere:
    """Sets the order of the review flashcards."""
    def __init__(
        self,
        df_vocab: pd.DataFrame,
        sections: list["Section"],
        subsections: dict["Section", list["Subsection"]],
        ss_states: "SSStates",
        ordering: Literal["alphabetic"],
        foreign_in_front: bool,
    ):
        self.df_vocab = df_vocab
        self.sections = sections
        self.subsections = subsections
        self.ss_states = ss_states
        self.foreign_in_front = foreign_in_front

        if ordering == "alphabetic":
            from flashcards import alphabetic_ordering
            self._next = alphabetic_ordering
        else:
            raise ValueError(f"Ordering not recognized: '{ordering}'")

    def get_ss(self, s_id: int, ss_id: int) -> tuple["Section", "Subsection"]:
        """Get section and subsection."""
        s = self.sections[s_id]
        return s, self.subsections[s][ss_id]

    def current_word(self) -> str:
        """Get current word to review."""
        return self.ss_states.get_word(self.df_vocab, is_foreign=self.foreign_in_front)

    def current_translation(self) -> str:
        """Get translation of the current word."""
        return self.ss_states.get_word(self.df_vocab, is_foreign=not self.foreign_in_front)

    def next(self) -> list:
        """Choose next word to review and return the relevant Gradio States."""
        return self._next(self)
