from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.ranges import Range, RangeId


def configure_ranges() -> GraphNode:
    return GraphNode(
        builder=build_ranges,
        constraint=None,
        produces=("entities/ranges",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_ranges(
    graph: SyntaxGraph,
) -> OneToOne[RangeId, Range]:
    ranges: dict[RangeId, Range] = {}

    for nid, entry in graph.ranges.items():
        # derive range ID from globally unique node ID
        range_id = RangeId(value=nid.value)

        ranges[range_id] = Range(
            ref=entry.ref,
            lower=Hex.derive(entry.lower.digits),
            upper=Hex.derive(entry.upper.digits),
        )

    return OneToOne[RangeId, Range].instance(ranges)


class ListExtractor:
    def __init__(self, data: OneToOne[RangeId, Range]):
        self.data = data

    def extract(self) -> Iterable[tuple[RangeId, Range]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "lwidth": "Lower Width",
            "lvalue": "Lower Value",
            "uwidth": "Upper Width",
            "uvalue": "Upper Value",
        }

    @staticmethod
    def rows(key: RangeId, entry: Range) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "lwidth": str(entry.lower.width),
            "lvalue": str(entry.lower),
            "uwidth": str(entry.upper.width),
            "uvalue": str(entry.upper),
        }
