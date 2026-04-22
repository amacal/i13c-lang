from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId, CallSiteTarget
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

    for nid, statement in graph.function.callsites.items():
        # derive callsite ID from globally unique node ID
        callsite_id = CallSiteId(value=nid.value)
        arguments: List[CallSiteTarget] = []

        # derive function ID from globally unique node ID
        nid = graph.function.callsites.get_ctx(nid)
        ctx = graph.function.functions.get_by_node(nid)

        for argument in statement.arguments:
            if isinstance(argument, tree.function.Literal):
                # derive literal ID from globally unique node ID
                lid = graph.function.literals.get_by_node(argument)
                arguments.append(LiteralId(value=lid.value))

            else:
                # derive expression ID from globally unique node ID
                eid = graph.function.expressions.get_by_node(argument)
                arguments.append(ExpressionId(value=eid.value))

        callsites[callsite_id] = CallSite(
            ref=statement.ref,
            ctx=ctx,
            callee=statement.name,
            arguments=arguments,
        )

    return OneToOne[CallSiteId, CallSite].instance(callsites)
