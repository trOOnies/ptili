"""Module for Gradio buttons."""

from gradio import Button

from components.ui_funcs import feedback_click, solution_click


def create_feedback_buttons() -> tuple[Button, Button, Button]:
    return (
        Button("Ho indovinato! 😊", variant="primary", interactive=False),
        Button("Più o meno 😐", interactive=False),
        Button("Ho sbagliato... 😢", variant="stop", interactive=False),
    )


class Buttons:
    """Buttons for the Gradio UI."""
    def __init__(
        self,
        show: Button,
        correct: Button,
        neutral: Button,
        wrong: Button,
    ):
        self.show = show
        self.correct = correct
        self.neutral = neutral
        self.wrong = wrong

    def to_list(self) -> list[Button]:
        return [self.show, self.correct, self.neutral, self.wrong]

    def set_click_events(self, rc, ss_states, card) -> None:
        row_comps = ss_states.to_list()
        review_comps = self.to_list() + [card]

        self.show.click(
            solution_click(rc),
            outputs=review_comps,
        )
        self.correct.click(
            feedback_click(rc, is_error=False, update=True),
            outputs=row_comps + review_comps,
        )
        self.neutral.click(
            feedback_click(rc, is_error=False, update=False),
            outputs=row_comps + review_comps,
        )
        self.wrong.click(
            feedback_click(rc, is_error=True, update=True),
            outputs=row_comps + review_comps,
        )
