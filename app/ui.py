"""Gradio UI script."""

import gradio as gr

from data import ReviewCameriere, open_glossary
from states import to_ss_states
from ui_funcs import feedback_click, solution_click

df_vocab, sections, subsections, sss_counts = open_glossary("glossario")


def create_ui(
    css: str,
) -> gr.Blocks:
    """Create the Gradio Blocks-based UI."""
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
            ordering="alphabetic",
        )

        gr.Markdown("# Ptili: Python Tool per Imparare L'Italiano 🇮🇹")

        with gr.Tab("Imparare"):

            with gr.Row(visible=True):
                with gr.Column():
                    for s_id, s in enumerate(sections):
                        gr.CheckboxGroup(
                            subsections[s],
                            value=subsections[s],
                            label=f"{s} ({sum(sss_counts[s_id])})",
                            interactive=True,
                        )
                with gr.Column():
                    card = gr.Textbox(
                        value=rc.current_word(),
                        label="Italiano 🇮🇹",
                        interactive=False,
                    )
                with gr.Column():
                    with gr.Row(visible=True):
                        show_btt = gr.Button("Soluzione", variant="secondary")
                    with gr.Row(visible=True):
                        correct_btt = gr.Button(
                            "Ho indovinato! 😊",
                            variant="primary",
                            interactive=False,
                        )
                        wrong_btt = gr.Button(
                            "Ho sbagliato... 😢",
                            variant="stop",
                            interactive=False,
                        )

        # Gradio Components
        # sss_comps = glossary_states.to_list()
        row_comps = ss_states.to_list()
        review_comps = [show_btt, correct_btt, wrong_btt, card]

        # Click events
        show_btt.click(
            solution_click(rc),
            outputs=review_comps,
        )
        correct_btt.click(
            feedback_click(rc),
            outputs=row_comps + review_comps,
        )
        wrong_btt.click(
            feedback_click(rc),
            outputs=row_comps + review_comps,
        )

    return ui
