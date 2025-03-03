"""Gradio UI script."""

import gradio as gr

from components.buttons import Buttons, create_feedback_buttons
from components.checkbox_group import create_checkbox_group
from components.review_cameriere import ReviewCameriere
from components.states import to_ss_states
from components.textbox import create_question_textbox
from data.loading import open_glossary


def create_ui(
    css: str,
    glossary_name: str,
    ordering: str,
) -> gr.Blocks:
    """Create the Gradio Blocks-based UI."""
    df_vocab, sections, subsections, sss_counts = open_glossary(glossary_name)
    foreign_in_front = False

    with gr.Blocks(
        title="PTILI",
        fill_width=True,
        css=css,
        theme=gr.themes.Default(primary_hue="green"),
    ) as ui:
        ss_states = to_ss_states(df_vocab, sections, subsections)
        rc = ReviewCameriere(
            df_vocab,
            sections,
            subsections,
            ss_states,
            ordering=ordering,
            foreign_in_front=foreign_in_front,
        )

        gr.Markdown("# Ptili: Python Tool per Imparare L'Italiano 🇮🇹")

        with gr.Tab("Imparare"):

            with gr.Row(visible=True):
                with gr.Column():
                    aux = gr.Textbox()
                with gr.Column():
                    card = create_question_textbox(rc, foreign_in_front)
                with gr.Column():
                    with gr.Row(visible=True):
                        show_btt = gr.Button("Soluzione", variant="secondary")
                    with gr.Row(visible=True):
                        correct_btt, neutral_btt, wrong_btt = create_feedback_buttons()

        # Gradio Components
        # sss_comps = glossary_states.to_list()

        buttons = Buttons(show_btt, correct_btt, neutral_btt, wrong_btt)
        buttons.set_click_events(rc, ss_states, card)

        with gr.Tab("Impostazioni"):
            with gr.Column():
                create_checkbox_group(sections, subsections, sss_counts)

    return ui, df_vocab
