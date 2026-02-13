from typing import List

from i13c.diag import Diagnostic
from i13c.graph.artifacts import GraphArtifacts
from i13c.graph.nodes import run as run_graph
from i13c.lex import tokenize
from i13c.par import parse
from i13c.res import Err, Ok
from i13c.src import open_text


class FixtureException(Exception):
    def __init__(self, diagnostics: List[Diagnostic]) -> None:
        self.diagnostics = diagnostics
        super().__init__(diagnostics[0])


def prepare_artifacts(code: str) -> GraphArtifacts:
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
            program = program

    return run_graph(program)
