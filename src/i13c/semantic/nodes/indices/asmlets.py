
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.signatures import SignatureId


def configure_asmlets_by_signatures() -> GraphNode:
    return GraphNode(
        builder=build_asmlets_by_signatures,
        constraint=None,
        produces=("indices/asmlets/signatures",),
        requires=frozenset(
            {
                ("asmlets", "analyses/asmlets"),
            }
        ),
    )


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


def build_asmlets_by_signatures(
    asmlets: OneToOne[AsmletId, Asmlet],
) -> OneToMany[SignatureId, Asmlet]:
    index: dict[SignatureId, list[Asmlet]] = {}

    for entry in asmlets.values():
        data = index.get(entry.signature.id)

        if data is None:
            index[entry.signature.id] = [entry]
        else:
            data.append(entry)

    return OneToMany[SignatureId, Asmlet].instance(index)


def build_asmlets_by_callsites(
    asmlets: OneToOne[AsmletId, Asmlet],
) -> OneToOne[CallSiteId, Asmlet]:
    index: dict[CallSiteId, Asmlet] = {}

    for entry in asmlets.values():
        for callsite in entry.callsites:
            index[callsite.id] = entry

    return OneToOne[CallSiteId, Asmlet].instance(index)
