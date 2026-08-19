from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
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
        views=GraphViews(list=ListExtractor),
    )


def build_calls(
    graph: SyntaxGraph,
) -> OneToOne[CallId, Call]:
    calls: dict[CallId, Call] = {}

    for nid, call in graph.function.calls.items():
        # derive call ID from globally unique node ID
        call_id = CallId(value=nid.value)

        # derive callsite ID from call target
        callsite_nid = graph.function.callsites.get_by_node(call.target)
        callsite_id = CallSiteId(value=callsite_nid.value)

        # find the owning statement of this value
        stmt = graph.function.calls.get_ctx(nid)
        stmt_nid = graph.function.statements.get_by_node(stmt)

        # find the owning function of this value
        fn = graph.function.statements.get_ctx(stmt_nid)
        fn_nid = graph.function.functions.get_by_node(fn)

        calls[call_id] = Call(
            ref=call.ref,
            fn=fn_nid,
            stmt=stmt_nid,
            target=callsite_id,
        )

    return OneToOne[CallId, Call].instance(calls)


class ListExtractor:
    def __init__(self, data: OneToOne[CallId, Call]):
        self.data = data

    def extract(self) -> Iterable[tuple[CallId, Call]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "target": "Target",
        }

    @staticmethod
    def rows(key: CallId, entry: Call) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "target": entry.target.identify(1),
        }
