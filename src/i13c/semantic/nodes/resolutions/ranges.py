from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.ranges import Range, RangeId
from i13c.semantic.typing.resolutions.ranges import (
    RangeAcceptance,
    RangeRejection,
    RangeResolution,
)


def configure_range_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_range_resolution,
        constraint=None,
        produces=("resolutions/ranges",),
        requires=frozenset({("ranges", "entities/ranges")}),
    )

    validate = GraphNode(
        builder=validate_range_resolution_e3001,
        constraint=None,
        produces=("rules/e3001",),
        requires=frozenset(
            {
                ("ranges", "entities/ranges"),
                ("resolutions", "resolutions/ranges"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_range_resolution_accepted,
        constraint=check_range_resolution_accepted,
        produces=("resolutions/ranges/accepted",),
        requires=frozenset(
            {
                ("rule_e3001", "rules/e3001"),
                ("resolutions", "resolutions/ranges"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_range_resolution(
    ranges: OneToOne[RangeId, Range],
) -> OneToOne[RangeId, RangeResolution]:
    resolutions: dict[RangeId, RangeResolution] = {}

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

        elif entry.lower.width != entry.upper.width:
            resolution.rejected.append(
                RangeRejection(
                    ref=entry.ref,
                    reason="inconsistent-widths",
                )
            )

        else:
            resolution.accepted.append(
                RangeAcceptance(
                    ref=entry.ref,
                    id=rid,
                    width=entry.lower.width,
                    lower=entry.lower,
                    upper=entry.upper,
                )
            )

        resolutions[rid] = resolution

    return OneToOne[RangeId, RangeResolution].instance(resolutions)


def check_range_resolution_accepted(
    rule_e3001: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3001) == 0


def build_range_resolution_accepted(
    resolutions: OneToOne[RangeId, RangeResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[RangeId, RangeAcceptance]:
    accepted: dict[RangeId, RangeAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[RangeId, RangeAcceptance].instance(accepted)


def validate_range_resolution_e3001(
    ranges: OneToOne[RangeId, Range],
    resolutions: OneToOne[RangeId, RangeResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_range_resolution_e3001(ranges.get(id), rejection)
                )

    return diagnostics


def report_range_resolution_e3001(
    entry: Range,
    rejection: RangeRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3001",
        message=f"Invalid range [{entry}], reason: {rejection.reason}.",
    )
