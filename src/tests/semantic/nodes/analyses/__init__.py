from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.analyses.core import AnalysisNodes
from i13c.semantic.typing.entities import EntityNodes
from tests.semantic import prepare_program


def prepare_analyses(code: str) -> tuple[EntityNodes, AnalysisNodes]:
    _, program = prepare_program(code)
    graph = run_graph(program).semantic_graph()

    return graph.entities, graph.analyses
