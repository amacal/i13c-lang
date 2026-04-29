from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.calls import Call, CallId
from i13c.semantic.typing.entities.callsites import CallSiteId


def configure_calls() -> GraphNode:
    return GraphNode(
        builder=build_calls,
        constraint=None,
        produces=("entities/calls",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_calls(
    graph: SyntaxGraph,
) -> OneToOne[CallId, Call]:
    calls: Dict[CallId, Call] = {}

    for nid, call in graph.function.calls.items():

        # derive call ID from globally unique node ID
        call_id = CallId(value=nid.value)

        # derive callsite ID from call target
        callsite_nid = graph.function.callsites.get_by_node(call.target)
        callsite_id = CallSiteId(value=callsite_nid.value)

        calls[call_id] = Call(
            ref=call.ref,
            target=callsite_id,
        )

    return OneToOne[CallId, Call].instance(calls)
