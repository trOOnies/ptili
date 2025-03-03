"""Loading ASCII functions."""

from colors import GREEN, RED, colored


def print_ascii_intro() -> None:
    with open("app/ascii_art.txt") as f:
        ascii_art = f.readlines()
    ascii_art = [line[:-1] for line in ascii_art[:-1]] + [ascii_art[-1]]
    for line in ascii_art:
        print(
            colored(GREEN, line[:15])
            + line[15:21]
            + colored(RED, line[21:])
        )
