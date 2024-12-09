"""Script for flashcards code."""


def alphabetic_ordering(rc) -> list:
    """Flashcard ordering based on alphabetic ordering."""
    row_iat = rc.ss_states.row_iat.value + 1
    row = rc.df_vocab.iloc[row_iat]

    s_id = row["sezione_id"]
    ss_id = row["sottosezione_id"]
    s, ss = rc.get_ss(s_id, ss_id)

    return [
        row_iat,
        {"id": s_id, "value": s},
        {"id": ss_id, "value": ss},
    ]
