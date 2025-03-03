"""Module for Gradio checkbox groups."""

from typing import TYPE_CHECKING

from gradio import CheckboxGroup

if TYPE_CHECKING:
    from classes import Section, Subsection


def create_checkbox_group(
    sections: list["Section"],
    subsections: dict["Section", list["Subsection"]],
    sss_counts: list[list[int]],
) -> None:
    for s_id, s in enumerate(sections):
        CheckboxGroup(
            subsections[s],
            value=subsections[s],
            label=f"{s} ({sum(sss_counts[s_id])})",
            interactive=True,
        )
