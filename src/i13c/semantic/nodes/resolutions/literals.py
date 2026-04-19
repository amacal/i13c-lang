from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
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
    )

    validate = GraphNode(
        builder=validate_literal_resolution_e3004,
        constraint=None,
        produces=("rules/e3004",),
        requires=frozenset(
            {
                ("literals", "entities/literals"),
                ("resolutions", "resolutions/slots"),
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
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_literal_resolution(
    literals: OneToOne[LiteralId, Literal],
) -> OneToOne[LiteralId, LiteralResolution]:
    resolutions: Dict[LiteralId, LiteralResolution] = {}

    for lid, entry in literals.items():
        resolution = LiteralResolution(
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
