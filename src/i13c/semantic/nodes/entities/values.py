from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.entities.values import Value, ValueId, ValueTarget
from i13c.syntax import tree


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

    for nid, statement in graph.function.values.items():

        # derive value ID from globally unique node ID
        value_id = ValueId(value=nid.value)

        # derive type from value statement
        nid = graph.types.get_by_node(statement.type)
        type_id = TypeId(value=nid.value)

        # find literal by AST node
        if isinstance(statement.expr, tree.function.Literal):
            nid = graph.function.literals.get_by_node(statement.expr)
            target: ValueTarget = LiteralId(value=nid.value)

        # find expression by AST node
        else:
            nid = graph.function.expressions.get_by_node(statement.expr)
            target = ExpressionId(value=nid.value)


        values[value_id] = Value(
            ref=statement.ref,
            name=statement.name,
            target=target,
            type=type_id,
        )

    return OneToOne[ValueId, Value].instance(values)
