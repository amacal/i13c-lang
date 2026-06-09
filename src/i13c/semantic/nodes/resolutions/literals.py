from typing import Any, Dict, Iterable, List, Tuple

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
    resolutions: Dict[LiteralId, LiteralResolution] = {}

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
    rule_e3004: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3004) == 0


def build_literal_resolution_accepted(
    resolutions: OneToOne[LiteralId, LiteralResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[LiteralId, LiteralAcceptance]:
    accepted: Dict[LiteralId, LiteralAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[LiteralId, LiteralAcceptance].instance(accepted)


def validate_literal_resolution_e3004(
    literals: OneToOne[LiteralId, Literal],
    resolutions: OneToOne[LiteralId, LiteralResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

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

    def extract(self) -> Iterable[Tuple[LiteralId, LiteralResolution]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(key: LiteralId, entry: LiteralResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[LiteralId, LiteralAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[LiteralId, LiteralAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "width": "Width",
            "value": "Value",
        }

    @staticmethod
    def rows(key: LiteralId, entry: LiteralAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "width": str(entry.target.width),
            "value": str(entry.target),
        }
