from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId


def configure_expressions() -> GraphNode:
    return GraphNode(
        builder=build_expressions,
        constraint=None,
        produces=("entities/expressions",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_expressions(
    graph: SyntaxGraph,
) -> OneToOne[ExpressionId, Expression]:
    expressions: Dict[ExpressionId, Expression] = {}

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
