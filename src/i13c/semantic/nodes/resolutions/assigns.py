from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.assigns import Assign, AssignId
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.resolutions.assigns import (
    AssignAcceptance,
    AssignResolution,
)
from i13c.semantic.typing.resolutions.types import TypeAcceptance


def configure_assign_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_assign_resolution,
        constraint=None,
        produces=("resolutions/assigns",),
        requires=frozenset(
            {
                ("assigns", "entities/assigns"),
                ("values", "entities/values"),
                ("types", "resolutions/types/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_assign_resolution_e3007,
        constraint=None,
        produces=("rules/e3007",),
        requires=frozenset(
            {
                ("assigns", "entities/assigns"),
                ("resolutions", "resolutions/assigns"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_assign_resolution_accepted,
        constraint=check_assign_resolution_accepted,
        produces=("resolutions/assigns/accepted",),
        requires=frozenset(
            {
                ("rule_e3007", "rules/e3007"),
                ("resolutions", "resolutions/assigns"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_assign_resolution(
    assigns: OneToOne[AssignId, Assign],
    values: OneToOne[ValueId, Value],
    types: OneToOne[TypeId, TypeAcceptance],
) -> OneToOne[AssignId, AssignResolution]:
    resolutions: Dict[AssignId, AssignResolution] = {}

    for aid, entry in assigns.items():
        resolution = AssignResolution(
            accepted=[],
            rejected=[],
        )

        value = values.get(entry.destination)
        type = types.get(value.type)

        resolution.accepted.append(
            AssignAcceptance(
                ref=entry.ref,
                id=aid,
                name=value.name,
                type=type,
                destination=entry.destination,
                expression=entry.expression,
            )
        )

        resolutions[aid] = resolution

    return OneToOne[AssignId, AssignResolution].instance(resolutions)


def check_assign_resolution_accepted(
    rule_e3007: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3007) == 0


def build_assign_resolution_accepted(
    resolutions: OneToOne[AssignId, AssignResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[AssignId, AssignAcceptance]:
    accepted: Dict[AssignId, AssignAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[AssignId, AssignAcceptance].instance(accepted)


def validate_assign_resolution_e3007(
    assigns: OneToOne[AssignId, Assign],
    resolutions: OneToOne[AssignId, AssignResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(report_assign_resolution_e3007(assigns.get(id)))

    return diagnostics


def report_assign_resolution_e3007(entry: Assign) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3007",
        message=f"Invalid assign {entry}, reason: unknown.",
    )
