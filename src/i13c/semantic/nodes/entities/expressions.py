from typing import Dict

from i13c import ast
from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId


def configure_expressions() -> GraphNode:
    return GraphNode(
        builder=build_expressions,
        produces=("entities/expressions",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_expressions(
    graph: SyntaxGraph,
) -> OneToOne[ExpressionId, Expression]:
    expressions: Dict[ExpressionId, Expression] = {}

    for nid, expression in graph.expressions.items():
        assert isinstance(expression, ast.Expression)

        # derive expression ID from globally unique node ID
        expression_id = ExpressionId(value=nid.value)

        expressions[expression_id] = Expression(
            ref=expression.ref,
            ident=Identifier(name=expression.name),
        )

    return OneToOne[ExpressionId, Expression].instance(expressions)
