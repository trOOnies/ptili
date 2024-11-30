"""Main script."""

# TODO: argparse
from colors import GREEN, RED, colored
from ui import create_ui

with open("app/styles.css") as f:
    CSS = f.read()


def main() -> None:
    """Main function."""
    ui = create_ui(CSS)

    with open("app/ascii_art.txt") as f:
        ascii_art = f.readlines()
    ascii_art = [line[:-1] for line in ascii_art[:-1]] + [ascii_art[-1]]
    for line in ascii_art:
        print(
            colored(GREEN, line[:15])
            + line[15:21]
            + colored(RED, line[21:])
        )
    del ascii_art

    ui.launch()


if __name__ == "__main__":
    main()
