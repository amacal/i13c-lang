from collections.abc import Iterable

from i13c.core.graph import AbstractListExtractor, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.immediates import Immediate, ImmediateId


def configure_immediates() -> GraphNode:
    return GraphNode(
        builder=build_immediates,
        constraint=None,
        produces=("entities/immediates",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=list_immediates),
    )


def build_immediates(
    graph: SyntaxGraph,
) -> OneToOne[ImmediateId, Immediate]:
    immediates: dict[ImmediateId, Immediate] = {}

    for id, entry in graph.snippet.immediates.items():
        # derive immediate ID from globally unique node ID
        immediate_id = ImmediateId(value=id.value)

        immediates[immediate_id] = Immediate(
            ref=entry.ref,
            value=Hex.derive(entry.data.digits),
        )

    return OneToOne[ImmediateId, Immediate].instance(immediates)


class ListExtractor:
    def __init__(self, data: OneToOne[ImmediateId, Immediate]):
        self.data = data

    def extract(self) -> Iterable[tuple[ImmediateId, Immediate]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "width": "Width",
            "value": "Value",
        }

    @staticmethod
    def rows(key: ImmediateId, entry: Immediate) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "width": str(entry.value.width),
            "value": str(entry.value),
        }


def list_immediates(
    data: OneToOne[ImmediateId, Immediate],
) -> AbstractListExtractor[ImmediateId, Immediate]:
    return ListExtractor(data)
