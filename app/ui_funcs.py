"""UI functions' script."""

import gradio as gr
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from data import ReviewCameriere

GradioUpdate = dict[str, Any]


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
            + [gr.update(value=rc.current_translation(), label="Traduzione 🇬🇧")]
        )

    return solution_fn


def feedback_click(rc: "ReviewCameriere"):
    def feedback_fn():
        """Feedback button click function."""
        ss_states_update = rc.next()

        rc.ss_states.row_iat.value = ss_states_update[2]
        rc.ss_states.S.value = ss_states_update[3]
        rc.ss_states.SS.value = ss_states_update[4]

        return (
            ss_states_update
            + toggle_buttons_interactivity(done=False)
            + [gr.update(value=rc.current_word(), label="Italiano 🇮🇹")]
        )

    return feedback_fn
