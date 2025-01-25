"""Main script."""

# TODO: argparse

from colors import GREEN, RED, colored
from options import ORDERING
from ui import create_ui

with open("app/styles.css") as f:
    CSS = f.read()


def main(glossary_name: str, ordering: str) -> None:
    """Main function."""
    ui, df_vocab = create_ui(CSS, glossary_name, ordering)

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

    df_history = df_vocab[["italiano", "ok", "not_ok", "last_ok", "last_not_ok"]]
    df_history = df_history[df_history[["ok", "not_ok"]].sum(axis=1) > 0]
    df_history.to_csv(f"history/{glossary_name}.csv", index=False)
    print("History saved succesfully.")

    print("Ci vediamo dopo! 👋")


if __name__ == "__main__":
    main(glossary_name="glossario", ordering=ORDERING.RANDOM)
