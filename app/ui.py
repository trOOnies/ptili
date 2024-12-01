"""Gradio UI script."""

import gradio as gr
from typing import Any

from data import open_glossary

GradioUpdate = dict[str, Any]

sss_tree, sections, subsections = open_glossary("glossario")
S = sections[0]
SS = subsections[S][0]


def toggle_buttons_interactivity(done: bool) -> list[GradioUpdate]:
    return [
        gr.update(interactive=not done),  # solution btt
        gr.update(interactive=done),  # correct btt
        gr.update(interactive=done),  # error btt
    ]


def toggle_fn(sbtt: str):
    return toggle_buttons_interactivity(sbtt == "Soluzione")


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
        gr.Markdown("# Ptili: Python Tool per Imparare L'Italiano 🇮🇹")

        with gr.Tab("Imparare"):

            with gr.Row(visible=True):
                with gr.Column():
                    gr.Markdown("Impari l'italiano! 👻")
                with gr.Column():
                    card = gr.Textbox(
                        value=sss_tree[S][SS]["italiano"].iat[0],
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
            toggle_fn,
            inputs=[show_btt],
            outputs=[show_btt, correct_btt, wrong_btt],
        )
        correct_btt.click(
            toggle_fn,
            inputs=[correct_btt],
            outputs=[show_btt, correct_btt, wrong_btt],
        )
        wrong_btt.click(
            toggle_fn,
            inputs=[wrong_btt],
            outputs=[show_btt, correct_btt, wrong_btt],
        )

    return ui
