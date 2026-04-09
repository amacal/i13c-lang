from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.callsites import Argument, CallSite, CallSiteId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.syntax import tree


def configure_callsites() -> GraphNode:
    return GraphNode(
        builder=build_callsites,
        constraint=None,
        produces=("entities/callsites",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_callsites(
    graph: SyntaxGraph,
) -> OneToOne[CallSiteId, CallSite]:
    callsites: Dict[CallSiteId, CallSite] = {}

    for nid, statement in graph.statements.items():
        arguments: List[Argument] = []

        # accept only call statements
        if not isinstance(statement, tree.function.CallStatement):
            continue

        for argument in statement.arguments:
            match argument:
                case tree.function.IntegerLiteral() as lit:
                    # find literal by AST node
                    lid = graph.literals.get_by_node(lit)

                    arguments.append(
                        Argument(
                            kind=b"literal",
                            target=LiteralId(value=lid.value),
                        )
                    )
                case tree.function.Expression() as expr:
                    # find expression by AST node
                    eid = graph.expressions.get_by_node(expr)

                    arguments.append(
                        Argument(
                            kind=b"expression",
                            target=ExpressionId(value=eid.value),
                        )
                    )

        # derive callsite ID from globally unique node ID
        callsite_id = CallSiteId(value=nid.value)

        callsites[callsite_id] = CallSite(
            id=callsite_id,
            ref=statement.ref,
            callee=Identifier(data=statement.name),
            arguments=arguments,
        )

    return OneToOne[CallSiteId, CallSite].instance(callsites)
