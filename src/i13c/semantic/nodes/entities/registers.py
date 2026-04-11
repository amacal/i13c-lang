from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.registers import Register, RegisterId


def configure_registers() -> GraphNode:
    return GraphNode(
        builder=build_registers,
        constraint=None,
        produces=("entities/registers",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_registers(
    graph: SyntaxGraph,
) -> OneToOne[RegisterId, Register]:
    registers: Dict[RegisterId, Register] = {}

    for id, entry in graph.registers.items():
        # derive register ID from globally unique node ID
        register_id = RegisterId(value=id.value)

        registers[register_id] = Register(
            ref=entry.ref,
            name=entry.name,
        )

    return OneToOne[RegisterId, Register].instance(registers)
