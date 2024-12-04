"""Script for Gradio States."""

from dataclasses import dataclass

from gradio import State as St


@dataclass
class GlossaryStates:
    """Glossary related Gradio States."""
    sss_tree: St
    sections: St
    subsections: St

    def to_list(self) -> list[St]:
        return [self.sss_tree, self.sections, self.subsections]

    def get_values(self) -> tuple:
        return tuple(state.value for state in self.to_list())


@dataclass
class SSStates:
    """Section-Subsection Gradio States."""
    S_id: St
    SS_id: St
    row_iat: St
    S: St
    SS: St

    def to_list(self) -> list[St]:
        return [self.S_id, self.SS_id, self.row_iat, self.S, self.SS]

    def get_values(self) -> tuple:
        return tuple(state.value for state in self.to_list())

    def get_word(self, sss_tree: dict) -> str:
        return sss_tree[self.S.value][self.SS.value]["italiano"].iat[self.row_iat.value]

    def get_translation(self, sss_tree: dict) -> str:
        return sss_tree[self.S.value][self.SS.value]["traduzione"].iat[self.row_iat.value]


def to_glossary_states(glossary_tuple: tuple) -> GlossaryStates:
    return GlossaryStates(*[St(glossary_tuple[i]) for i in range(3)])


def to_ss_states(glossary_states: GlossaryStates) -> SSStates:
    S_id = St(value=0)
    SS_id = St(value=0)
    row_iat = St(value=0)
    S = St(glossary_states.sections.value[S_id.value])
    SS = St(glossary_states.subsections.value[S.value][SS_id.value])
    return SSStates(S_id, SS_id, row_iat, S, SS)
