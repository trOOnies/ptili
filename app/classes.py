"""Classes reference file."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame

Section = str
Subsection = str
SSSTree = dict[Section, dict[Subsection, "DataFrame"]]

ItalianWord = str
TranslatedWord = str
