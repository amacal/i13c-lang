from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.ranges import RangeId
from i13c.semantic.typing.entities.types import Type, TypeId


def configure_types() -> GraphNode:
    return GraphNode(
        builder=build_types,
        constraint=None,
        produces=("entities/types",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_types(
    graph: SyntaxGraph,
) -> OneToOne[TypeId, Type]:
    types: Dict[TypeId, Type] = {}

    for nid, entry in graph.types.items():
        # derive type ID from globally unique node ID
        type_id = TypeId(value=nid.value)

        # reverse mapping to range ID if applicable
        if entry.range is not None:
            nid = graph.ranges.get_by_node(entry.range)
            range_id = RangeId(value=nid.value)
        else:
            range_id = None

        types[type_id] = Type(
            ref=entry.ref,
            name=entry.name,
            range=range_id,
        )

    return OneToOne[TypeId, Type].instance(types)
