from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.statements import Statement, StatementId
from i13c.syntax import tree


def configure_statements() -> GraphNode:
    return GraphNode(
        builder=build_statements,
        constraint=None,
        produces=("entities/statements",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_statements(
    graph: SyntaxGraph,
) -> OneToOne[StatementId, Statement]:
    statements: Dict[StatementId, Statement] = {}

    for nid, statement in graph.function.statements.items():
        # derive statement ID from globally unique node ID
        statement_id = StatementId(value=nid.value)

        # derive assign ID from value statement
        if isinstance(statement.target, tree.function.AssignStatement):
            nid = graph.function.assigns.get_by_node(statement.target)
            target = AssignId(value=nid.value)

        # derive callsite ID from call statement
        else:
            nid = graph.function.callsites.get_by_node(statement.target)
            target = CallSiteId(value=nid.value)

        statements[statement_id] = Statement(
            ref=statement.ref,
            target=target,
        )

    return OneToOne[StatementId, Statement].instance(statements)
