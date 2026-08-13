from i13c.graph.nodes import run as run_graph
from i13c.semantic.model import ResolutionNodes, SemanticRules
from i13c.syntax.source import SourceCode
from tests.semantic import prepare_program


def prepare_resolutions(code: str) -> tuple[SourceCode, ResolutionNodes]:
    source, program = prepare_program(code)
    return source, run_graph(program).semantic_graph().resolutions


def prepare_rules(code: str) -> tuple[SourceCode, SemanticRules]:
    source, program = prepare_program(code)
    return source, run_graph(program).rules()
