from i13c.core.diagnostics import Diagnostic
from i13c.core.result import Err, Ok
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import SourceCode, open_text
from i13c.syntax.tree import Program


class FixtureException(Exception):
    def __init__(self, diagnostics: list[Diagnostic]) -> None:
        self.diagnostics = diagnostics
        super().__init__(diagnostics[0])


def prepare_program(code: str) -> tuple[SourceCode, Program]:
    source = open_text(code)

    match tokenize(source):
        case Err(diagnostics):
            raise FixtureException(diagnostics)
        case Ok(tokens):
            tokenized = tokens

    match parse(source, tokenized):
        case Err(diagnostics):
            raise FixtureException(diagnostics)
        case Ok(program):
            return (source, program)
