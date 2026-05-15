from typing import Tuple

from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.analyses import AnalysisNodes
from i13c.semantic.typing.entities import EntityNodes
from tests.semantic import prepare_program


def prepare_analyses(code: str) -> Tuple[EntityNodes, AnalysisNodes]:
    _, program = prepare_program(code)
    graph = run_graph(program).semantic_graph()

    return graph.entities, graph.analyses
