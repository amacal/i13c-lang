from typing import List, Tuple

from i13c.ast import Program
from i13c.diag import Diagnostic
from i13c.lex import tokenize
from i13c.par import parse
from i13c.res import Err, Ok
from i13c.src import SourceCode, open_text


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
