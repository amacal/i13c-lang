from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.registers import Register, RegisterId


def configure_registers() -> GraphNode:
    return GraphNode(
        builder=build_registers,
        constraint=None,
        produces=("entities/registers",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_registers(
    graph: SyntaxGraph,
) -> OneToOne[RegisterId, Register]:
    registers: dict[RegisterId, Register] = {}

    for id, entry in graph.snippet.registers.items():
        # derive register ID from globally unique node ID
        register_id = RegisterId(value=id.value)

        registers[register_id] = Register(
            ref=entry.ref,
            name=entry.name,
        )

    return OneToOne[RegisterId, Register].instance(registers)


class ListExtractor:
    def __init__(self, data: OneToOne[RegisterId, Register]):
        self.data = data

    def extract(self) -> Iterable[tuple[RegisterId, Register]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
        }

    @staticmethod
    def rows(key: RegisterId, entry: Register) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
        }
