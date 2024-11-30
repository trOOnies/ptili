"""Gradio UI script."""

import gradio as gr


def create_ui(
    css: str,
) -> gr.Blocks:
    """Create the Gradio Blocks-based UI."""
    with gr.Blocks(title="PTILI", fill_width=True, css=css) as ui:
        gr.Markdown("# Ptili: Python Tool per Imparare L'Italiano 🇮🇹")

        with gr.Tab("Imparare"):
            with gr.Row(visible=True):
                gr.Markdown("Impari l'italiano! 👻")

    return ui
