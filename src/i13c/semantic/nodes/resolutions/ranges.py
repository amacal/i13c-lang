from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.ranges import Range, RangeId
from i13c.semantic.typing.resolutions.ranges import (
    RangeAcceptance,
    RangeRejection,
    RangeResolution,
)


def configure_range_resolution() -> GraphNode:
    return GraphNode(
        builder=build_range_resolution,
        constraint=None,
        produces=("resolutions/ranges",),
        requires=frozenset({("ranges", "entities/ranges")}),
    )


def build_range_resolution(
    ranges: OneToOne[RangeId, Range],
) -> OneToOne[RangeId, RangeResolution]:
    resolutions: Dict[RangeId, RangeResolution] = {}

    for rid, entry in ranges.items():
        resolution = RangeResolution(
            accepted=[],
            rejected=[],
        )

        if Hex.greater(entry.lower.data, entry.upper.data):
            resolution.rejected.append(
                RangeRejection(
                    ref=entry.ref,
                    reason="lower-greater-than-upper",
                )
            )

        else:
            resolution.accepted.append(
                RangeAcceptance(
                    ref=entry.ref,
                    id=rid,
                    lower=entry.lower,
                    upper=entry.upper,
                )
            )

        resolutions[rid] = resolution

    return OneToOne[RangeId, RangeResolution].instance(resolutions)
