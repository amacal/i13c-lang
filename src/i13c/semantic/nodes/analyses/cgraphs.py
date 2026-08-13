from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.analyses.cgraphs import CallGraph
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


def configure_call_graphs() -> GraphNode:
    return GraphNode(
        builder=build_call_graphs,
        constraint=None,
        produces=("analyses/cgraphs",),
        requires=frozenset(
            {
                ("signatures", "resolutions/signatures/accepted"),
                ("callsites", "indices/callsites/signatures"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_call_graphs(
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    callsites: OneToMany[SignatureId, CallSiteAcceptance],
) -> OneToOne[SignatureId, CallGraph]:
    cgraphs: dict[SignatureId, CallGraph] = {}

    # identify already available backward edges
    for sid, entries in callsites.items():
        backward: list[SignatureAcceptance] = []

        for entry in entries:
            backward.append(signatures.get(entry.sig))

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


class ListExtractor:
    def __init__(self, data: OneToOne[SignatureId, CallGraph]):
        self.data = data

    def extract(self) -> Iterable[tuple[SignatureId, CallGraph]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "name": "Name",
            "forward": "Forward",
            "backward": "Backward",
        }

    @staticmethod
    def rows(key: SignatureId, entry: CallGraph) -> dict[str, str]:
        return {
            "ref": str(entry.target.ref),
            "fn": key.identify(1),
            "name": entry.target.name.decode(),
            "forward": str(len(entry.forward)),
            "backward": str(len(entry.backward)),
        }
