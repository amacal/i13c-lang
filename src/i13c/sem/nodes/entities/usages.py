from typing import Dict

from i13c import ast
from i13c.core.mapping import OneToOne
from i13c.sem.core import Identifier
from i13c.sem.infra import Configuration
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.usages import Usage, UsageId


def configure_usages() -> Configuration:
    return Configuration(
        builder=build_usages,
        produces=("entities/usages",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_usages(
    graph: SyntaxGraph,
) -> OneToOne[UsageId, Usage]:
    usages: Dict[UsageId, Usage] = {}

    for _, statement in graph.statements.items():
        assert isinstance(statement, ast.Statement)

        for argument in statement.arguments:
            # not expression must be literals
            if not isinstance(argument, ast.Expression):
                continue

            # derive parameter ID from globally unique node ID
            nid = graph.expressions.get_by_node(argument)
            usage_id = UsageId(value=nid.value)

            usages[usage_id] = Usage(
                ref=argument.ref,
                ident=Identifier(name=argument.name),
            )

    return OneToOne[UsageId, Usage].instance(usages)
