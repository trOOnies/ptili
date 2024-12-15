"""UI functions' script."""

import gradio as gr
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from review_cameriere import ReviewCameriere

GradioUpdate = dict[str, Any]

ITA_LABEL = "Italiano 🇮🇹"
TRAD_LABEL = "Traduzione 🇬🇧"


def toggle_buttons_interactivity(done: bool) -> list[GradioUpdate]:
    return [
        gr.update(interactive=not done),  # solution btt
        gr.update(interactive=done),  # correct btt
        gr.update(interactive=done),  # error btt
    ]


def solution_click(rc: "ReviewCameriere"):
    def solution_fn():
        """Show solution button click function."""
        return (
            toggle_buttons_interactivity(done=True)
            + [
                gr.update(
                    value=rc.current_back(),
                    label=TRAD_LABEL if rc.foreign_in_front else ITA_LABEL
                )
            ]
        )

    return solution_fn


def feedback_click(rc: "ReviewCameriere", is_error: bool):
    def feedback_fn():
        """Feedback button click function."""
        ss_states_update = rc.next(is_error, update=True)

        rc.ss_states.row_iat.value = ss_states_update[0]
        rc.ss_states.S.value = ss_states_update[1]
        rc.ss_states.SS.value = ss_states_update[2]

        return (
            ss_states_update
            + toggle_buttons_interactivity(done=False)
            + [
                gr.update(
                    value=rc.current_front(),
                    label=ITA_LABEL if rc.foreign_in_front else TRAD_LABEL
                )
            ]
        )

    return feedback_fn
