"""Module for Gradio textboxes."""

from gradio import Textbox

from components.ui_funcs import ITA_LABEL, TRAD_LABEL


def create_question_textbox(rc, foreign_in_front: bool) -> Textbox:
    return Textbox(
        value=rc.current_front(),
        label=ITA_LABEL if foreign_in_front else TRAD_LABEL,
        interactive=False,
    )
