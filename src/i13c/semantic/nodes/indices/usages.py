from typing import Dict, List, Tuple

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.core import Identifier
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.indices.usages import Usage, UsageId
from i13c.syntax import tree


def configure_usages_by_expression() -> GraphNode:
    return GraphNode(
        builder=build_usages_by_expression,
        constraint=None,
        produces=("entities/usages", "indices/usages-by-expression"),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_usages_by_expression(
    graph: SyntaxGraph,
) -> Tuple[OneToOne[UsageId, Usage], OneToMany[ExpressionId, UsageId]]:
    usages: Dict[UsageId, Usage] = {}
    mapping: Dict[ExpressionId, List[UsageId]] = {}

    for _, statement in graph.statements.items():

        # for callsites we need to handle arguments
        if isinstance(statement, tree.CallStatement):
            for argument in statement.arguments:
                # not expression must be literals
                if not isinstance(argument, tree.Expression):
                    continue

                # derive parameter ID from globally unique node ID
                nid = graph.expressions.get_by_node(argument)
                usage_id = UsageId(value=nid.value)

                # map usage to expression
                expression_id = ExpressionId(value=nid.value)
                mapping[expression_id] = [usage_id]

                # map expression to usage
                usages[usage_id] = Usage(
                    ref=argument.ref,
                    ident=Identifier(name=argument.name),
                )

        if isinstance(statement, tree.ValueStatement):
            # not expression must be literals
            if not isinstance(statement.expr, tree.Expression):
                continue

            # derive parameter ID from globally unique node ID
            nid = graph.expressions.get_by_node(statement.expr)
            usage_id = UsageId(value=nid.value)

            # map usage to expression
            expression_id = ExpressionId(value=nid.value)
            mapping[expression_id] = [usage_id]

            # map expression to usage
            usages[usage_id] = Usage(
                ref=statement.expr.ref,
                ident=Identifier(name=statement.expr.name),
            )

    return (
        OneToOne[UsageId, Usage].instance(usages),
        OneToMany[ExpressionId, UsageId].instance(mapping),
    )
