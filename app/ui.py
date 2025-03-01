"""Gradio UI script."""

import gradio as gr

from components.review_cameriere import ReviewCameriere
from components.states import to_ss_states
from components.ui_funcs import feedback_click, solution_click, ITA_LABEL, TRAD_LABEL
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
                    card = gr.Textbox(
                        value=rc.current_front(),
                        label=ITA_LABEL if foreign_in_front else TRAD_LABEL,
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
                        neutral_btt = gr.Button(
                            "Più o meno 😐",
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
        review_comps = [show_btt, correct_btt, neutral_btt, wrong_btt, card]

        # Click events
        show_btt.click(
            solution_click(rc),
            outputs=review_comps,
        )
        correct_btt.click(
            feedback_click(rc, is_error=False, update=True),
            outputs=row_comps + review_comps,
        )
        neutral_btt.click(
            feedback_click(rc, is_error=False, update=False),
            outputs=row_comps + review_comps,
        )
        wrong_btt.click(
            feedback_click(rc, is_error=True, update=True),
            outputs=row_comps + review_comps,
        )

        with gr.Tab("Configure"):
            with gr.Column():
                for s_id, s in enumerate(sections):
                    gr.CheckboxGroup(
                        subsections[s],
                        value=subsections[s],
                        label=f"{s} ({sum(sss_counts[s_id])})",
                        interactive=True,
                    )

    return ui, df_vocab
