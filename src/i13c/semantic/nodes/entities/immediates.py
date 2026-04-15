from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.immediates import Immediate, ImmediateId


def configure_immediates() -> GraphNode:
    return GraphNode(
        builder=build_immediates,
        constraint=None,
        produces=("entities/immediates",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_immediates(
    graph: SyntaxGraph,
) -> OneToOne[ImmediateId, Immediate]:
    immediates: Dict[ImmediateId, Immediate] = {}

    for id, entry in graph.immediates.items():
        # derive immediate ID from globally unique node ID
        immediate_id = ImmediateId(value=id.value)

        immediates[immediate_id] = Immediate(
            ref=entry.ref,
            value=Hex.derive(entry.data.digits),
        )

    return OneToOne[ImmediateId, Immediate].instance(immediates)
