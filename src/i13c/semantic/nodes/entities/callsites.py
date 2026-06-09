from typing import Dict, Iterable, List, Tuple

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId, CallSiteTarget
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.syntax import tree


def configure_callsites() -> GraphNode:
    return GraphNode(
        builder=build_callsites,
        constraint=None,
        produces=("entities/callsites",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_callsites(
    graph: SyntaxGraph,
) -> OneToOne[CallSiteId, CallSite]:
    callsites: Dict[CallSiteId, CallSite] = {}

    for nid, callsite in graph.function.callsites.items():

        # derive callsite ID from globally unique node ID
        callsite_id = CallSiteId(value=nid.value)
        arguments: List[CallSiteTarget] = []

        # derive function ID from globally unique node ID
        stmt = graph.function.callsites.get_ctx(nid)
        stmt_nid = graph.function.statements.get_by_node(stmt)

        # derive statement ID from globally unique node ID
        fn = graph.function.statements.get_ctx(stmt_nid)
        fn_nid = graph.function.functions.get_by_node(fn)

        for argument in callsite.arguments:
            if isinstance(argument, tree.function.Literal):
                # derive literal ID from globally unique node ID
                lid = graph.function.literals.get_by_node(argument)
                arguments.append(LiteralId(value=lid.value))

            else:
                # derive expression ID from globally unique node ID
                eid = graph.function.expressions.get_by_node(argument)
                arguments.append(ExpressionId(value=eid.value))

        callsites[callsite_id] = CallSite(
            ref=callsite.ref,
            function=fn_nid,
            statement=stmt_nid,
            callee=callsite.name,
            arguments=arguments,
        )

    return OneToOne[CallSiteId, CallSite].instance(callsites)


class ListExtractor:
    def __init__(self, data: OneToOne[CallSiteId, CallSite]):
        self.data = data

    def extract(self) -> Iterable[Tuple[CallSiteId, CallSite]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "fn": "Function",
            "stmt": "Statement",
            "callee": "Callee",
            "args": "Arguments",
        }

    @staticmethod
    def rows(key: CallSiteId, entry: CallSite) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "fn": entry.get_function(FunctionId.from_context).identify(1),
            "stmt": entry.get_statement(StatementId.from_context).identify(1),
            "callee": entry.callee.decode(),
            "args": str(len(entry.arguments)),
        }
