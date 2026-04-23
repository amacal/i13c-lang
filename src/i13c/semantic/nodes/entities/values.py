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
        type_nid = graph.types.get_by_node(value.type)
        type_id = TypeId(value=type_nid.value)

        # find the owning statement of this value
        stmt = graph.function.values.get_ctx(nid)
        stmt_nid = graph.function.statements.get_by_node(stmt)

        values[value_id] = Value(
            ref=value.ref,
            stmt=stmt_nid,
            name=value.name,
            type=type_id,
        )

    return OneToOne[ValueId, Value].instance(values)
