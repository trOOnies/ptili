"""UI functions' script."""

import gradio as gr
from typing import Any

GradioUpdate = dict[str, Any]


def toggle_buttons_interactivity(done: bool) -> list[GradioUpdate]:
    return [
        gr.update(interactive=not done),  # solution btt
        gr.update(interactive=done),  # correct btt
        gr.update(interactive=done),  # error btt
    ]


def solution_fn(s, ss, row_iat, sss_tree):
    return (
        toggle_buttons_interactivity(done=True)
        + [
            gr.update(
                value=sss_tree[s][ss]["traduzione"].iat[row_iat],
                label="Traduzione 🇬🇧"
            )
        ]
    )


def feedback_fn(s_id, ss_id, row_iat, s, ss, sections, subsections, sss_tree):
    if row_iat + 1 < sss_tree[s][ss].shape[0]:
        row_iat += 1
    elif ss_id + 1 == len(subsections[s]):
        s_id += 1
        ss_id = 0
        row_iat = 0
        s = sections[s_id]
        ss = subsections[s][ss_id]
    else:
        ss_id += 1
        row_iat = 0
        ss = subsections[s][ss_id]

    return (
        [s_id, ss_id, row_iat, s, ss]
        + toggle_buttons_interactivity(done=False)
        + [
            gr.update(
                value=sss_tree[s][ss]["italiano"].iat[row_iat],
                label="Italiano 🇮🇹"
            )
        ]
    )
