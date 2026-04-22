from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.entities.values import Value, ValueId


def configure_values() -> GraphNode:
    return GraphNode(
        builder=build_values,
        constraint=None,
        produces=("entities/values",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_values(
    graph: SyntaxGraph,
) -> OneToOne[ValueId, Value]:
    values: Dict[ValueId, Value] = {}

    for nid, value in graph.function.values.items():
        # derive value ID from globally unique node ID
        value_id = ValueId(value=nid.value)

        # derive type ID from value statement
        nid = graph.types.get_by_node(value.type)
        type_id = TypeId(value=nid.value)

        values[value_id] = Value(
            ref=value.ref,
            name=value.name,
            type=type_id,
        )

    return OneToOne[ValueId, Value].instance(values)
