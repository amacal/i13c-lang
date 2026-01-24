from typing import Dict, List, Tuple

from i13c import ast
from i13c.core.mapping import OneToMany, OneToOne
from i13c.sem.core import Identifier
from i13c.sem.infra import Configuration
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.expressions import ExpressionId
from i13c.sem.typing.indices.usages import Usage, UsageId


def configure_usages_by_expression() -> Configuration:
    return Configuration(
        builder=build_usages_by_expression,
        produces=("entities/usages", "indices/usages-by-expression"),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_usages_by_expression(
    graph: SyntaxGraph,
) -> Tuple[OneToOne[UsageId, Usage], OneToMany[ExpressionId, UsageId]]:
    usages: Dict[UsageId, Usage] = {}
    mapping: Dict[ExpressionId, List[UsageId]] = {}

    for _, statement in graph.statements.items():
        assert isinstance(statement, ast.Statement)

        for argument in statement.arguments:
            # not expression must be literals
            if not isinstance(argument, ast.Expression):
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


    return (
        OneToOne[UsageId, Usage].instance(usages),
        OneToMany[ExpressionId, UsageId].instance(mapping),
    )
