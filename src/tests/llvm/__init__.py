from typing import List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.result import Err, Ok
from i13c.graph.nodes import run as run_graph
from i13c.llvm.graph import LowLevelGraph
from i13c.semantic.model import SemanticGraph
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import open_text


class FixtureException(Exception):
    def __init__(self, diagnostics: List[Diagnostic]) -> None:
        self.diagnostics = diagnostics
        super().__init__(diagnostics[0])


class GraphFixtureException(Exception):
    def __init__(self, diagnostics: List[Diagnostic]) -> None:
        self.diagnostics = diagnostics
        super().__init__(f"LLVM Graph cannot be created: {diagnostics[0].message}")


class MissingMainInFixture(Exception):
    def __init__(self) -> None:
        super().__init__("main function is missing in fixture")


def prepare_graph(code: str) -> Tuple[SemanticGraph, LowLevelGraph]:
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

    artifacts = run_graph(program)

    if artifacts.rules().count() > 0:
        raise GraphFixtureException(list(artifacts.rules().enumerate()))

    return artifacts.semantic_graph(), artifacts.llvm_graph()


def prepare_main(code: str) -> List[str]:
    semantic, llvm = prepare_graph(code)

    # if main is found return all instructions in main
    if main := semantic.find_function_by_name(b"main"):
        return list(llvm.instructions_of(main))

    raise MissingMainInFixture()
