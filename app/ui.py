"""Gradio UI script."""

import gradio as gr

from data import open_glossary
from ui_funcs import feedback_fn, solution_fn

glossary_tuple = open_glossary("glossario")


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
        sss_tree = gr.State(glossary_tuple[0])
        sections = gr.State(glossary_tuple[1])
        subsections = gr.State(glossary_tuple[2])

        S_id = gr.State(value=0)
        SS_id = gr.State(value=0)
        row_iat = gr.State(value=0)
        S = gr.State(sections.value[S_id.value])
        SS = gr.State(subsections.value[S.value][SS_id.value])

        gr.Markdown("# Ptili: Python Tool per Imparare L'Italiano 🇮🇹")

        with gr.Tab("Imparare"):

            with gr.Row(visible=True):
                with gr.Column():
                    gr.Markdown("Impari l'italiano! 👻")
                with gr.Column():
                    card = gr.Textbox(
                        value=sss_tree.value[S.value][SS.value]["italiano"].iat[row_iat.value],
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

        show_btt.click(
            solution_fn,
            inputs=[S, SS, row_iat, sss_tree],
            outputs=[
                show_btt, correct_btt, wrong_btt, card,
            ],
        )
        correct_btt.click(
            feedback_fn,
            inputs=[S_id, SS_id, row_iat, S, SS, sections, subsections, sss_tree],
            outputs=[
                S_id, SS_id, row_iat, S, SS, show_btt, correct_btt, wrong_btt, card,
            ],
        )
        wrong_btt.click(
            feedback_fn,
            inputs=[S_id, SS_id, row_iat, S, SS, sections, subsections, sss_tree],
            outputs=[
                S_id, SS_id, row_iat, S, SS, show_btt, correct_btt, wrong_btt, card,
            ],
        )

    return ui
