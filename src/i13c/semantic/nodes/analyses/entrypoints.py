from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.analyses.entrypoints import Entrypoint
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.flags import FlagsAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


def configure_entrypoints() -> GraphNode:
    return GraphNode(
        builder=build_entrypoints,
        constraint=None,
        produces=("analyses/entrypoints",),
        requires=frozenset(
            {
                ("flags", "indices/flags/nid"),
                ("signatures", "indices/signatures/nid"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_entrypoints(
    flags: OneToOne[NodeId, FlagsAcceptance],
    signatures: OneToOne[NodeId, SignatureAcceptance],
) -> OneToOne[SignatureId, Entrypoint]:
    entrypoints: dict[SignatureId, Entrypoint] = {}

    for nid, signature in signatures.items():
        if signature.name == b"main":
            if len(signature.parameters) == 0:
                if flag := flags.find(nid):
                    if flag.noreturn:
                        entrypoints[signature.id] = Entrypoint(target=signature)

    return OneToOne[SignatureId, Entrypoint].instance(entrypoints)


class ListExtractor:
    def __init__(self, data: OneToOne[SignatureId, Entrypoint]):
        self.data = data

    def extract(self) -> Iterable[tuple[SignatureId, Entrypoint]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "Id",
            "target": "Target",
            "name": "Name",
        }

    @staticmethod
    def rows(key: SignatureId, entry: Entrypoint) -> dict[str, str]:
        return {
            "ref": str(entry.target.ref),
            "id": key.identify(1),
            "target": entry.target.id.identify(1),
            "name": entry.target.name.decode(),
        }
