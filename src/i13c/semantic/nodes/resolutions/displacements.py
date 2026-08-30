from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.displacements import Displacement, DisplacementId
from i13c.semantic.typing.resolutions.displacements import (
    DisplacementAcceptance,
    DisplacementWidth,
    DisplacementRejection,
    DisplacementResolution,
)


def configure_displacement_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_displacement_resolution,
        constraint=None,
        produces=("resolutions/displacements",),
        requires=frozenset(
            {
                ("displacements", "entities/displacements"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_displacement_resolution_e3028,
        constraint=None,
        produces=("rules/e3028",),
        requires=frozenset(
            {
                ("displacements", "entities/displacements"),
                ("resolutions", "resolutions/displacements"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_displacement_resolution_accepted,
        constraint=check_displacement_resolution_accepted,
        produces=("resolutions/displacements/accepted",),
        requires=frozenset(
            {
                ("rule_e3028", "rules/e3028"),
                ("resolutions", "resolutions/displacements"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_displacement_resolution(
    displacements: OneToOne[DisplacementId, Displacement],
) -> OneToOne[DisplacementId, DisplacementResolution]:
    resolutions: dict[DisplacementId, DisplacementResolution] = {}

    for did, entry in displacements.items():
        resolution = DisplacementResolution(
            ref=entry.ref,
            id=did,
            accepted=[],
            rejected=[],
        )

        normalized = entry.offset.lstrip(bytes(0x00))
        positive = entry.direction == "forward"

        if len(normalized) >= 4:
            if len(normalized) > 4:
                resolution.rejected.append(
                    DisplacementRejection(
                        ref=entry.ref,
                        id=did,
                        reason="overflow",
                    )
                )

            elif positive and normalized[0] > 0x7F:
                resolution.rejected.append(
                    DisplacementRejection(
                        ref=entry.ref,
                        id=did,
                        reason="overflow",
                    )
                )

            elif not positive and normalized[0] > 0x80:
                resolution.rejected.append(
                    DisplacementRejection(
                        ref=entry.ref,
                        id=did,
                        reason="overflow",
                    )
                )

        def derive_width(offset: bytes) -> DisplacementWidth:
            if len(offset) == 0:
                return 0

            if len(offset) == 1:
                return 8

            return 32

        if not resolution.rejected:
            resolution.accepted.append(
                DisplacementAcceptance(
                    ref=entry.ref,
                    id=did,
                    width=derive_width(normalized),
                    offset=normalized,
                    direction=entry.direction,
                )
            )

        resolutions[did] = resolution

    return OneToOne[DisplacementId, DisplacementResolution].instance(resolutions)


def check_displacement_resolution_accepted(
    rule_e3028: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3028) == 0


def build_displacement_resolution_accepted(
    resolutions: OneToOne[DisplacementId, DisplacementResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[DisplacementId, DisplacementAcceptance]:
    accepted: dict[DisplacementId, DisplacementAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[DisplacementId, DisplacementAcceptance].instance(accepted)


def validate_displacement_resolution_e3028(
    displacements: OneToOne[DisplacementId, Displacement],
    resolutions: OneToOne[DisplacementId, DisplacementResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(
                    report_displacement_resolution_e3028(displacements.get(id))
                )

    return diagnostics


def report_displacement_resolution_e3028(entry: Displacement) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3028",
        message=f"Invalid displacement {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[DisplacementId, DisplacementResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[DisplacementId, DisplacementResolution]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(key: DisplacementId, entry: DisplacementResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[DisplacementId, DisplacementAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[DisplacementId, DisplacementAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "offset": "Offset",
            "direction": "Direction",
        }

    @staticmethod
    def rows(key: DisplacementId, entry: DisplacementAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "offset": str(entry.offset),
            "direction": str(entry.direction),
        }
