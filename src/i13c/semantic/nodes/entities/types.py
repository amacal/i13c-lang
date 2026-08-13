from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.ranges import RangeId
from i13c.semantic.typing.entities.types import Type, TypeId


def configure_types() -> GraphNode:
    return GraphNode(
        builder=build_types,
        constraint=None,
        produces=("entities/types",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_types(
    graph: SyntaxGraph,
) -> OneToOne[TypeId, Type]:
    types: dict[TypeId, Type] = {}

    for nid, entry in graph.types.items():
        # derive type ID from globally unique node ID
        type_id = TypeId(value=nid.value)

        # reverse mapping to range ID if applicable
        if entry.range is not None:
            nid = graph.ranges.get_by_node(entry.range)
            range_id = RangeId(value=nid.value)
        else:
            range_id = None

        types[type_id] = Type(
            ref=entry.ref,
            name=entry.name,
            range=range_id,
        )

    return OneToOne[TypeId, Type].instance(types)


class ListExtractor:
    def __init__(self, data: OneToOne[TypeId, Type]):
        self.data = data

    def extract(self) -> Iterable[tuple[TypeId, Type]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "range": "Range",
        }

    @staticmethod
    def rows(key: TypeId, entry: Type) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "range": entry.range.identify(1) if entry.range is not None else "",
        }
