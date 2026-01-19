from typing import Dict, List

from i13c import ast
from i13c.core.mapping import OneToOne
from i13c.sem.core import Identifier
from i13c.sem.infra import Configuration
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.callsites import Argument, CallSite, CallSiteId
from i13c.sem.typing.entities.expressions import ExpressionId
from i13c.sem.typing.entities.literals import LiteralId


def configure_callsites() -> Configuration:
    return Configuration(
        builder=build_callsites,
        produces=("entities/callsites",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_callsites(
    graph: SyntaxGraph,
) -> OneToOne[CallSiteId, CallSite]:
    callsites: Dict[CallSiteId, CallSite] = {}

    for nid, statement in graph.statements.items():
        arguments: List[Argument] = []

        # ignore non-call instructions
        # if not isinstance(statement, ast.CallStatement):
        #    continue

        for argument in statement.arguments:
            match argument:
                case ast.IntegerLiteral() as lit:
                    # find literal by AST node
                    lid = graph.literals.get_by_node(lit)

                    arguments.append(
                        Argument(
                            kind=b"literal",
                            target=LiteralId(value=lid.value),
                        )
                    )
                case ast.Expression() as expr:
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
            ref=statement.ref,
            callee=Identifier(name=statement.name),
            arguments=arguments,
        )

    return OneToOne[CallSiteId, CallSite].instance(callsites)
