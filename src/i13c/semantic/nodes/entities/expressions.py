from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.statements import StatementId


def configure_expressions() -> GraphNode:
    return GraphNode(
        builder=build_expressions,
        constraint=None,
        produces=("entities/expressions",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_expressions(
    graph: SyntaxGraph,
) -> OneToOne[ExpressionId, Expression]:
    expressions: dict[ExpressionId, Expression] = {}

    for nid, expression in graph.function.expressions.items():
        # derive expression ID from globally unique node ID
        expression_id = ExpressionId(value=nid.value)

        # find the owning statement of this expression
        stmt = graph.function.expressions.get_ctx(nid)
        stmt_nid = graph.function.statements.get_by_node(stmt)

        # find the owning function of this expression
        fn = graph.function.statements.get_ctx(stmt_nid)
        fn_nid = graph.function.functions.get_by_node(fn)

        expressions[expression_id] = Expression(
            ref=expression.ref,
            name=expression.name,
            statement=stmt_nid,
            function=fn_nid,
        )

    return OneToOne[ExpressionId, Expression].instance(expressions)


class ListExtractor:
    def __init__(self, data: OneToOne[ExpressionId, Expression]):
        self.data = data

    def extract(self) -> Iterable[tuple[ExpressionId, Expression]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "fn": "Function",
            "stmt": "Statement",
        }

    @staticmethod
    def rows(key: ExpressionId, entry: Expression) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "fn": entry.get_function(FunctionId.from_context).identify(1),
            "stmt": entry.get_statement(StatementId.from_context).identify(1),
        }
