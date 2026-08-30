from collections.abc import Iterable

from i13c.core.graph import AbstractListExtractor, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.displacements import Displacement, DisplacementId


def configure_displacements() -> GraphNode:
    return GraphNode(
        builder=build_displacements,
        constraint=None,
        produces=("entities/displacements",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=list_displacements),
    )


def build_displacements(
    graph: SyntaxGraph,
) -> OneToOne[DisplacementId, Displacement]:
    displacements: dict[DisplacementId, Displacement] = {}

    for id, entry in graph.snippet.displacements.items():
        # derive displacement ID from globally unique node ID
        displacement_id = DisplacementId(value=id.value)

        displacements[displacement_id] = Displacement(
            ref=entry.ref,
            direction=entry.kind,
            offset=entry.offset.digits,
        )

    return OneToOne[DisplacementId, Displacement].instance(displacements)


class ListExtractor:
    def __init__(self, data: OneToOne[DisplacementId, Displacement]):
        self.data = data

    def extract(self) -> Iterable[tuple[DisplacementId, Displacement]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "dir": "Direction",
            "off": "Offset",
        }

    @staticmethod
    def rows(key: DisplacementId, entry: Displacement) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "dir": entry.direction,
            "off": str(entry.offset),
        }


def list_displacements(
    data: OneToOne[DisplacementId, Displacement],
) -> AbstractListExtractor[DisplacementId, Displacement]:
    return ListExtractor(data)
