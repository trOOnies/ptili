"""Main script."""

# TODO: argparse

from data.ascii import print_ascii_intro
from data.saving import save_history, vocab_to_history
from options import ORDERING
from ui import create_ui

with open("app/styles.css") as f:
    CSS = f.read()


def main(glossary_name: str, ordering: str) -> None:
    """Main function."""
    ui, df_vocab = create_ui(CSS, glossary_name, ordering)

    print_ascii_intro()
    ui.launch()

    df_history = vocab_to_history(df_vocab)
    save_history(df_history, glossary_name)

    print("Ci vediamo dopo! 👋")


if __name__ == "__main__":
    main(glossary_name="glossario", ordering=ORDERING.NET_ERRORS_WEIGHTED)
