from typing import Tuple

from i13c.graph.nodes import run as run_graph
from i13c.semantic.model import IndexEdges
from i13c.syntax.source import SourceCode
from tests.semantic import prepare_program


def prepare_indices(code: str) -> Tuple[SourceCode, IndexEdges]:
    source, program = prepare_program(code)
    return source, run_graph(program).semantic_graph().indices
