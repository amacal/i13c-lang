from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities import EntityNodes
from tests.semantic import prepare_program


def prepare_entities(code: str) -> EntityNodes:
    _, program = prepare_program(code)

    return run_graph(program).semantic_graph().entities
