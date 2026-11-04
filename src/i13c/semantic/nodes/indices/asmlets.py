
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.entities.callsites import CallSiteId


def configure_asmlets_by_callsites() -> GraphNode:
    return GraphNode(
        builder=build_asmlets_by_callsites,
        constraint=None,
        produces=("indices/asmlets/callsites",),
        requires=frozenset(
            {
                ("asmlets", "analyses/asmlets"),
            }
        ),
    )


def build_asmlets_by_callsites(
    asmlets: OneToOne[AsmletId, Asmlet],
) -> OneToOne[CallSiteId, Asmlet]:
    index: dict[CallSiteId, Asmlet] = {}

    for entry in asmlets.values():
        for callsite in entry.callsites:
            index[callsite.id] = entry

    return OneToOne[CallSiteId, Asmlet].instance(index)
