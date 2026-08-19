from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.shuffles import Shuffle, ShuffleCallSite
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId


def configure_shuffles_by_callsites() -> GraphNode:
    return GraphNode(
        builder=build_shuffles_by_callsites,
        constraint=None,
        produces=("indices/shuffles/callsites",),
        requires=frozenset(
            {
                ("shuffles", "analyses/shuffles"),
            }
        ),
    )


def build_shuffles_by_callsites(
    shuffles: OneToOne[FunctionId, Shuffle],
) -> OneToOne[CallSiteId, ShuffleCallSite]:
    index: dict[CallSiteId, ShuffleCallSite] = {}

    for entry in shuffles.values():
        for callsite in entry.callsites:
            index[callsite.calling.callsite] = callsite

    return OneToOne[CallSiteId, ShuffleCallSite].instance(index)
