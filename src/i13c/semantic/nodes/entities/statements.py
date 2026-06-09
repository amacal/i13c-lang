from typing import Dict, Iterable, Tuple

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.calls import CallId
from i13c.semantic.typing.entities.statements import Statement, StatementId
from i13c.syntax import tree


def configure_statements() -> GraphNode:
    return GraphNode(
        builder=build_statements,
        constraint=None,
        produces=("entities/statements",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
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
            nid = graph.function.calls.get_by_node(statement.target)
            target = CallId(value=nid.value)

        statements[statement_id] = Statement(
            ref=statement.ref,
            target=target,
        )

    return OneToOne[StatementId, Statement].instance(statements)


class ListExtractor:
    def __init__(self, data: OneToOne[StatementId, Statement]):
        self.data = data

    def extract(self) -> Iterable[Tuple[StatementId, Statement]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "target": "Target",
        }

    @staticmethod
    def rows(key: StatementId, entry: Statement) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "target": entry.target.identify(1),
        }
