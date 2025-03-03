"""ReviewCameriere utility functions."""

from typing import TYPE_CHECKING, Callable

from options import ORDERING

if TYPE_CHECKING:
    from numpy import ndarray
    from pandas import DataFrame

    from components.states import SSStates

OrderingFunction = Callable[["DataFrame"], "ndarray"]


def load_ordering(ordering: str) -> OrderingFunction:
    if ordering == ORDERING.RANDOM:
        from flashcards import random_ordering
        return random_ordering
    elif ordering == ORDERING.ALPHABETIC:
        from flashcards import alphabetic_ordering
        return alphabetic_ordering
    elif ordering == ORDERING.NET_ERRORS:
        from flashcards import net_errors_ordering
        return net_errors_ordering
    elif ordering == ORDERING.NET_ERRORS_WEIGHTED:
        from flashcards import make_net_weighted_errors_ordering
        return make_net_weighted_errors_ordering(randomness_sigma=0.33)
    else:
        raise ValueError(f"Ordering not recognized: '{ordering}'")


def init_ss_states(ss_states, sss_list: list) -> None:
    ss_states.row_iat.value = sss_list[0]
    ss_states.S.value = sss_list[1]
    ss_states.SS.value = sss_list[2]


def get_next_iats(
    df_vocab: "DataFrame",
    ss_states: "SSStates",
    is_error: bool,
) -> tuple[int, int, int]:
    """Returns: row_iat, str_status_iat, date_str_col_iat."""
    str_status = "not_ok" if is_error else "ok"
    date_str_col = f"last_{str_status}"
    return (
        ss_states.row_iat.value,
        df_vocab.columns.get_loc(str_status),
        df_vocab.columns.get_loc(date_str_col),
    )
