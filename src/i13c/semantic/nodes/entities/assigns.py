from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.assigns import Assign, AssignId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.values import ValueId
from i13c.syntax import tree


def configure_assigns() -> GraphNode:
    return GraphNode(
        builder=build_assigns,
        constraint=None,
        produces=("entities/assigns",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_assigns(
    graph: SyntaxGraph,
) -> OneToOne[AssignId, Assign]:
    assigns: Dict[AssignId, Assign] = {}

    for nid, statement in graph.function.assigns.items():
        # derive assign ID from globally unique node ID
        assign_id = AssignId(value=nid.value)

        # derive value ID from value statement
        nid = graph.function.values.get_by_node(statement.destination)
        value_id = ValueId(value=nid.value)

        # derive literal ID from the statement
        if isinstance(statement.expression, tree.function.Literal):
            nid = graph.function.literals.get_by_node(statement.expression)
            target = LiteralId(value=nid.value)

        # derive expression ID from the statement
        else:
            nid = graph.function.expressions.get_by_node(statement.expression)
            target = ExpressionId(value=nid.value)

        assigns[assign_id] = Assign(
            ref=statement.ref,
            destination=value_id,
            expression=target,
        )

    return OneToOne[AssignId, Assign].instance(assigns)
