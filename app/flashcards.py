"""Script for flashcards code."""


def alphabetic_ordering(rc) -> list:
    """Flashcard ordering based on alphabetic ordering."""
    sss_tree, sections, subsections = rc.glossary_states.get_values()
    s_id, ss_id, row_iat, s, ss = rc.ss_states.get_values()

    if row_iat + 1 < sss_tree[s][ss].shape[0]:
        # Still pending words
        row_iat += 1
    elif ss_id + 1 < len(subsections[s]):
        # No more words in subsection
        ss_id += 1
        row_iat = 0
        ss = subsections[s][ss_id]
    else:
        # No more subsections in section
        s_id += 1
        ss_id = 0
        row_iat = 0
        s = sections[s_id]
        ss = subsections[s][ss_id]

    return [s_id, ss_id, row_iat, s, ss]
