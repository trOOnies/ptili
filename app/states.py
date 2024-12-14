"""Script for Gradio States."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gradio import State as St

if TYPE_CHECKING:
    from pandas import DataFrame

    from classes import Section, Subsection


@dataclass
class SSStates:
    """Section-Subsection Gradio States."""
    row_iat: St  # int
    S: St        # dict[Literal["id", "value"], int | "Section"]
    SS: St       # dict[Literal["id", "value"], int | "Subsection"]

    def to_list(self) -> list[St]:
        return [self.row_iat, self.S, self.SS]

    def get_values(self) -> tuple:
        return tuple(state.value for state in self.to_list())

    def get_word(self, df_vocab: "DataFrame", is_foreign: bool) -> str:
        col = "italiano" if is_foreign else "traduzione"
        return df_vocab[col].iat[self.row_iat.value]


def to_ss_states(
    df_vocab: "DataFrame",
    sections: list["Section"],
    subsections: dict["Section", list["Subsection"]],
) -> SSStates:
    """To SSStates."""
    row_iat = St(0)
    row = df_vocab.iloc[row_iat.value]

    s_id = int(row.at["sezione_id"])
    ss_id = int(row.at["sottosezione_id"])

    S = St({"id": s_id, "value": sections[s_id]})
    SS = St({"id": ss_id, "value": subsections[S.value["value"]][ss_id]})

    return SSStates(row_iat, S, SS)
