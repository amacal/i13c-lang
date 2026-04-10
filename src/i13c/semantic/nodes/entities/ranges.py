from typing import Dict

from i13c.core.graph import GraphNode
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
    )


def build_ranges(
    graph: SyntaxGraph,
) -> OneToOne[RangeId, Range]:
    ranges: Dict[RangeId, Range] = {}

    for nid, entry in graph.ranges.items():
        # derive range ID from globally unique node ID
        range_id = RangeId(value=nid.value)

        ranges[range_id] = Range(
            ref=entry.ref,
            lower=Hex.derive(entry.lower.digits),
            upper=Hex.derive(entry.upper.digits),
        )

    return OneToOne[RangeId, Range].instance(ranges)
