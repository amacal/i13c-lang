from typing import List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.res import Err, Ok
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import SourceCode, open_text
from i13c.syntax.tree import Program


class FixtureException(Exception):
    def __init__(self, diagnostics: List[Diagnostic]) -> None:
        self.diagnostics = diagnostics
        super().__init__(diagnostics[0])


def prepare_program(code: str) -> Tuple[SourceCode, Program]:
    source = open_text(code)

    match tokenize(source):
        case Err(diagnostics):
            raise FixtureException(diagnostics)
        case Ok(tokens):
            tokens = tokens

    match parse(source, tokens):
        case Err(diagnostics):
            raise FixtureException(diagnostics)
        case Ok(program):
            return (source, program)
