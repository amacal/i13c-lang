from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.cgraphs import CallGraph
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


def configure_call_graphs() -> GraphNode:
    return GraphNode(
        builder=build_call_graphs,
        constraint=None,
        produces=("entities/cgraphs",),
        requires=frozenset(
            {
                ("signatures", "resolutions/signatures/accepted"),
                ("callsites", "indices/callsites/signatures"),
            }
        ),
    )


def build_call_graphs(
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    callsites: OneToMany[SignatureId, CallSiteAcceptance],
) -> OneToOne[SignatureId, CallGraph]:
    cgraphs: Dict[SignatureId, CallGraph] = {}

    # identify already available backward edges
    for sid, entries in callsites.items():
        backward: List[SignatureAcceptance] = []

        for entry in entries:
            backward.append(signatures.get(entry.ctx))

        cgraphs[sid] = CallGraph(
            target=signatures.get(sid),
            backward=backward,
            forward=[],
        )

    # identify missing signatures and add them as nodes without edges
    for sid, entry in signatures.items():
        if sid not in cgraphs:
            cgraphs[sid] = CallGraph(
                target=entry,
                backward=[],
                forward=[],
            )

    # derive forward edges from backward edges
    for cgraph in cgraphs.values():
        for entry in cgraph.backward:
            cgraphs[entry.id].forward.append(cgraph.target)

    return OneToOne[SignatureId, CallGraph].instance(cgraphs)
