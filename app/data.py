"""Script for data handling."""

import re
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from classes import Section, Subsection, SSSTree

NAME_PATT = re.compile(r"^[a-z][a-z0-9\-\_]*[a-z0-9]$", re.IGNORECASE)


def open_glossary(
    name: str,
) -> tuple["SSSTree", list["Section"], dict["Section", list["Subsection"]]]:
    """Open glossary file and convert it into Pythonic classes.

    CSV should have the columns: italiano, traduzione, sezione, sottosezione.
    """
    assert NAME_PATT.match(name)

    df = pd.read_csv(f"glossary/{name}.csv")
    prev_len = df.shape[0]

    df = df.drop_duplicates("italiano", keep="first", ignore_index=True)
    print(f"DELETED {prev_len - df.shape[0]} DUPLICATED ROWS")
    print(df)

    sss_set = set(
        (row["sezione"], row["sottosezione"])
        for _, row in df[["sezione", "sottosezione"]].iterrows()
    )
    sections_set = set(tup[0] for tup in sss_set)
    sections = sorted(list(sections_set))

    sss_tree = {
        s: {
            tup[1]: df[
                (df["sezione"] == s) & (df["sottosezione"] == tup[1])
            ]
            for tup in sss_set
            if tup[0] == s
        }
        for s in sections
    }
    del df
    sss_tree = {
        s: dict(sorted(vs.items()))
        for s, vs in sss_tree.items()
    }

    print("WORD COUNTS:")
    for s, vs in sss_tree.items():
        print(s)
        print({ss: df_sss.shape[0] for ss, df_sss in vs.items()})

    subsections = {
        s: list(vs.keys())
        for s, vs in sss_tree.items()
    }

    return sss_tree, sections, subsections
