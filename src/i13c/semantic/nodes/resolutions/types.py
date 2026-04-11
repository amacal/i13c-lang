from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.ranges import RangeId
from i13c.semantic.typing.entities.types import Type, TypeId
from i13c.semantic.typing.resolutions.ranges import RangeAcceptance
from i13c.semantic.typing.resolutions.types import (
    TypeAcceptance,
    TypeRejection,
    TypeResolution,
    TypeWidth,
)


def configure_type_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_type_resolution,
        constraint=None,
        produces=("resolutions/types",),
        requires=frozenset(
            {
                ("types", "entities/types"),
                ("ranges", "resolutions/ranges/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_type_resolution_e3009,
        constraint=None,
        produces=("rules/e3009",),
        requires=frozenset(
            {
                ("types", "entities/types"),
                ("resolutions", "resolutions/types"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_type_resolution_accepted,
        constraint=check_type_resolution_accepted,
        produces=("resolutions/types/accepted",),
        requires=frozenset(
            {
                ("rule_e3009", "rules/e3009"),
                ("resolutions", "resolutions/types"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_type_resolution(
    types: OneToOne[TypeId, Type],
    ranges: OneToOne[RangeId, RangeAcceptance],
) -> OneToOne[TypeId, TypeResolution]:
    resolutions: Dict[TypeId, TypeResolution] = {}

    mapping: Dict[bytes, TypeWidth] = {
        b"u8": 8,
        b"u16": 16,
        b"u32": 32,
        b"u64": 64,
    }

    for tid, entry in types.items():
        resolution = TypeResolution(
            accepted=[],
            rejected=[],
        )

        if entry.range is not None:
            range = ranges.get(entry.range)
        else:
            range = None

        if entry.name not in mapping:
            resolution.rejected.append(
                TypeRejection(
                    ref=entry.ref,
                    reason="unknown-type",
                )
            )

        elif range and range.width != mapping[entry.name]:
            resolution.rejected.append(
                TypeRejection(
                    ref=entry.ref,
                    reason="inconsistent-widths",
                )
            )

        else:
            resolution.accepted.append(
                TypeAcceptance(
                    ref=entry.ref,
                    id=tid,
                    name=entry.name,
                    width=mapping[entry.name],
                    range=range,
                )
            )

        resolutions[tid] = resolution

    return OneToOne[TypeId, TypeResolution].instance(resolutions)


def check_type_resolution_accepted(
    rule_e3009: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3009) == 0


def build_type_resolution_accepted(
    resolutions: OneToOne[TypeId, TypeResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[TypeId, TypeAcceptance]:
    accepted: Dict[TypeId, TypeAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[TypeId, TypeAcceptance].instance(accepted)


def validate_type_resolution_e3009(
    types: OneToOne[TypeId, Type],
    resolutions: OneToOne[TypeId, TypeResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_type_resolution_e3009(types.get(id), rejection)
                )

    return diagnostics


def report_type_resolution_e3009(entry: Type, rejection: TypeRejection) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3009",
        message=f"Invalid type {entry}, reason: {rejection.reason}.",
    )
