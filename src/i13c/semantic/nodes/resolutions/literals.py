from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.literals import Literal, LiteralId
from i13c.semantic.typing.resolutions.literals import (
    LiteralAcceptance,
    LiteralResolution,
)


def configure_literal_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_literal_resolution,
        constraint=None,
        produces=("resolutions/literals",),
        requires=frozenset(
            {
                ("literals", "entities/literals"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_literal_resolution_e3004,
        constraint=None,
        produces=("rules/e3004",),
        requires=frozenset(
            {
                ("literals", "entities/literals"),
                ("resolutions", "resolutions/literals"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_literal_resolution_accepted,
        constraint=check_literal_resolution_accepted,
        produces=("resolutions/literals/accepted",),
        requires=frozenset(
            {
                ("rule_e3004", "rules/e3004"),
                ("resolutions", "resolutions/literals"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_literal_resolution(
    literals: OneToOne[LiteralId, Literal],
) -> OneToOne[LiteralId, LiteralResolution]:
    resolutions: dict[LiteralId, LiteralResolution] = {}

    for lid, entry in literals.items():
        resolution = LiteralResolution(
            ref=entry.ref,
            id=lid,
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            LiteralAcceptance(
                ref=entry.ref,
                id=lid,
                target=entry.target,
            )
        )

        resolutions[lid] = resolution

    return OneToOne[LiteralId, LiteralResolution].instance(resolutions)


def check_literal_resolution_accepted(
    rule_e3004: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3004) == 0


def build_literal_resolution_accepted(
    resolutions: OneToOne[LiteralId, LiteralResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[LiteralId, LiteralAcceptance]:
    accepted: dict[LiteralId, LiteralAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[LiteralId, LiteralAcceptance].instance(accepted)


def validate_literal_resolution_e3004(
    literals: OneToOne[LiteralId, Literal],
    resolutions: OneToOne[LiteralId, LiteralResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(report_literal_resolution_e3004(literals.get(id)))

    return diagnostics


def report_literal_resolution_e3004(entry: Literal) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3004",
        message=f"Invalid literal {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[LiteralId, LiteralResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[LiteralId, LiteralResolution]]:
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
    def rows(key: LiteralId, entry: LiteralResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[LiteralId, LiteralAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[LiteralId, LiteralAcceptance]]:
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
    def rows(key: LiteralId, entry: LiteralAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "width": str(entry.target.width),
            "value": str(entry.target),
        }
