from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.immediates import Immediate, ImmediateId
from i13c.semantic.typing.resolutions.immediates import (
    ImmediateAcceptance,
    ImmediateResolution,
)


def configure_immediate_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_immediate_resolution,
        constraint=None,
        produces=("resolutions/immediates",),
        requires=frozenset(
            {
                ("immediates", "entities/immediates"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_immediate_resolution_e3016,
        constraint=None,
        produces=("rules/e3016",),
        requires=frozenset(
            {
                ("immediates", "entities/immediates"),
                ("resolutions", "resolutions/immediates"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_immediate_resolution_accepted,
        constraint=check_immediate_resolution_accepted,
        produces=("resolutions/immediates/accepted",),
        requires=frozenset(
            {
                ("rule_e3016", "rules/e3016"),
                ("resolutions", "resolutions/immediates"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_immediate_resolution(
    immediates: OneToOne[ImmediateId, Immediate],
) -> OneToOne[ImmediateId, ImmediateResolution]:
    resolutions: dict[ImmediateId, ImmediateResolution] = {}

    for iid, entry in immediates.items():
        resolution = ImmediateResolution(
            ref=entry.ref,
            id=iid,
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            ImmediateAcceptance(
                ref=entry.ref,
                id=iid,
                value=entry.value,
            )
        )

        resolutions[iid] = resolution

    return OneToOne[ImmediateId, ImmediateResolution].instance(resolutions)


def check_immediate_resolution_accepted(
    rule_e3016: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3016) == 0


def build_immediate_resolution_accepted(
    resolutions: OneToOne[ImmediateId, ImmediateResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[ImmediateId, ImmediateAcceptance]:
    accepted: dict[ImmediateId, ImmediateAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ImmediateId, ImmediateAcceptance].instance(accepted)


def validate_immediate_resolution_e3016(
    immediates: OneToOne[ImmediateId, Immediate],
    resolutions: OneToOne[ImmediateId, ImmediateResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(
                    report_immediate_resolution_e3016(immediates.get(id))
                )

    return diagnostics


def report_immediate_resolution_e3016(entry: Immediate) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3016",
        message=f"Invalid immediate {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[ImmediateId, ImmediateResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[ImmediateId, ImmediateResolution]]:
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
    def rows(key: ImmediateId, entry: ImmediateResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[ImmediateId, ImmediateAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[ImmediateId, ImmediateAcceptance]]:
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
    def rows(key: ImmediateId, entry: ImmediateAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "width": str(entry.value.width),
            "value": str(entry.value),
        }
