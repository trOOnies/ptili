"""Script for data handling."""

import datetime as dt
from typing import TYPE_CHECKING, Literal

import pandas as pd

from options import ORDERING

if TYPE_CHECKING:
    from numpy import ndarray

    from classes import Section, Subsection
    from components.states import SSStates

TODAY = dt.date.today()
PD_TODAY = pd.to_datetime(TODAY)


class ReviewCameriere:
    """Sets the order of the review flashcards."""
    def __init__(
        self,
        df_vocab: pd.DataFrame,
        sections: list["Section"],
        subsections: dict["Section", list["Subsection"]],
        ss_states: "SSStates",
        ordering: Literal["alphabetic", "net_errors"],
        foreign_in_front: bool,
    ):
        self.df_vocab = df_vocab
        self.sections = sections
        self.subsections = subsections
        self.ss_states = ss_states
        self.foreign_in_front = foreign_in_front

        if ordering == ORDERING.RANDOM:
            from flashcards import random_ordering
            self.get_order = random_ordering
        elif ordering == ORDERING.ALPHABETIC:
            from flashcards import alphabetic_ordering
            self.get_order = alphabetic_ordering
        elif ordering == ORDERING.NET_ERRORS:
            from flashcards import net_errors_ordering
            self.get_order = net_errors_ordering
        elif ordering == ORDERING.NET_ERRORS_WEIGHTED:
            from flashcards import make_net_weighted_errors_ordering
            self.get_order = make_net_weighted_errors_ordering(randomness_sigma=0.33)
        else:
            raise ValueError(f"Ordering not recognized: '{ordering}'")

        self.ordered_row_ids: "ndarray" = self.get_order(self.df_vocab)
        self.pointer = -1

        sss_list = self.next(is_error=False, update=False)
        self.ss_states.row_iat.value = sss_list[0]
        self.ss_states.S.value = sss_list[1]
        self.ss_states.SS.value = sss_list[2]

    def get_ss(self, s_id: int, ss_id: int) -> tuple["Section", "Subsection"]:
        """Get section and subsection."""
        s = self.sections[s_id]
        return s, self.subsections[s][ss_id]

    def current_front(self) -> str:
        """Get current word to review (front)."""
        return self.ss_states.get_word(
            self.df_vocab,
            is_foreign=self.foreign_in_front,
        )

    def current_back(self) -> str:
        """Get current word's answer (back)."""
        return self.ss_states.get_word(
            self.df_vocab,
            is_foreign=not self.foreign_in_front,
        )

    def _get_sss_list(self) -> list:
        """Get SSS list of related objects. Pointer must have already been changed."""
        row_iat = self.ordered_row_ids[self.pointer]
        row = self.df_vocab.iloc[row_iat]

        s_id = row["sezione_id"]
        ss_id = row["sottosezione_id"]
        s, ss = self.get_ss(s_id, ss_id)

        return [
            row_iat,
            {"id": s_id, "value": s},
            {"id": ss_id, "value": ss},
        ]

    def next(self, is_error: bool, update: bool) -> list:
        """Choose next word to review and return the relevant Gradio States."""
        # Feedback
        if update:
            str_status = "not_ok" if is_error else "ok"
            date_str_col = f"last_{str_status}"
            row_iat = self.ss_states.row_iat.value

            str_status_iat = self.df_vocab.columns.get_loc(str_status)
            date_str_col_iat = self.df_vocab.columns.get_loc(date_str_col)

            self.df_vocab.iat[row_iat, str_status_iat] += 1
            self.df_vocab.iat[row_iat, date_str_col_iat] = PD_TODAY

        # Next word
        self.pointer += 1
        return self._get_sss_list()
