from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind

from i13c import ast
from i13c.sem.core import Identifier
from i13c.sem.literal import LiteralId
from i13c.sem.syntax import SyntaxGraph

ArgumentKind = Kind[b"literal"]


@dataclass(kw_only=True, frozen=True)
class CallSiteId:
    value: int


@dataclass(kw_only=True)
class Argument:
    kind: ArgumentKind
    target: LiteralId


@dataclass(kw_only=True)
class CallSite:
    callee: Identifier
    arguments: List[Argument]


def build_callsites(
    graph: SyntaxGraph,
) -> Dict[CallSiteId, CallSite]:
    callsites: Dict[CallSiteId, CallSite] = {}

    for nid, statement in graph.nodes.statements.items():
        arguments: List[Argument] = []

        # ignore non-call instructions
        # if not isinstance(statement, ast.CallStatement):
        #    continue

        # derive callsite id from globally unique node id
        id = CallSiteId(value=nid.value)

        for argument in statement.arguments:
            match argument:
                case ast.IntegerLiteral() as lit:
                    # find literal by AST node
                    lid = graph.nodes.literals.get_by_node(lit)

                    arguments.append(
                        Argument(
                            kind=b"literal",
                            target=LiteralId(value=lid.value),
                        )
                    )

        callsites[id] = CallSite(
            callee=Identifier(name=statement.name),
            arguments=arguments,
        )

    return callsites
