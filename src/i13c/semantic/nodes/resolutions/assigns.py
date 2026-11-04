from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.assigns import Assign, AssignId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.entities.usages import UsageId
from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.resolutions.assigns import (
    AssignAcceptance,
    AssignRejection,
    AssignResolution,
)
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.usages import UsageAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance


def configure_assign_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_assign_resolution,
        constraint=None,
        produces=("resolutions/assigns",),
        requires=frozenset(
            {
                ("assigns", "entities/assigns"),
                ("values", "resolutions/values/accepted"),
                ("literals", "resolutions/literals/accepted"),
                ("usages", "resolutions/usages/accepted"),
                ("callsites", "resolutions/callsites/accepted"),
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
    values: OneToOne[ValueId, ValueAcceptance],
    literals: OneToOne[LiteralId, LiteralAcceptance],
    usages: OneToOne[UsageId, UsageAcceptance],
    callsites: OneToOne[CallSiteId, CallSiteAcceptance],
) -> OneToOne[AssignId, AssignResolution]:
    resolutions: dict[AssignId, AssignResolution] = {}

    for aid, entry in assigns.items():
        resolution = AssignResolution(
            accepted=[],
            rejected=[],
        )

        # extract destination, because we need to check its compatibility
        destination = values.get(entry.destination)

        # nothing is rejected by default
        rejected = None

        # literals are directly retrieved
        # matched by their value against the destination type
        if isinstance(entry.expression, LiteralId):
            expression = literals.get(entry.expression)
            target = expression

        # usages are also directly retrieved
        # matched by their target type against the destination type
        elif isinstance(entry.expression, UsageId):
            expression = usages.get(entry.expression)
            target = expression.target.type

        # callsite propagates its call, because it contains
        # where the returned value is stored, callsite is not needed
        else:
            expression = callsites.get(entry.expression)

            # result may be null when the callsite does not produce a value
            target = (
                expression.signature.result.type
                if expression.signature.result
                else None
            )

        if target is None:
            rejected = "type-mismatch"

        elif not destination.type.accepts(target):
            rejected = "type-mismatch"

        # if we know some rejection reason
        # we need just to record the rejection
        if rejected is not None:
            resolution.rejected.append(
                AssignRejection(
                    ref=entry.ref,
                    id=aid,
                    reason=rejected,
                )
            )

        else:
            resolution.accepted.append(
                AssignAcceptance(
                    ref=entry.ref,
                    id=aid,
                    fn=entry.get_function(FunctionId.from_context),
                    stmt=entry.get_statement(StatementId.from_context),
                    destination=destination,
                    expression=expression,
                )
            )

        resolutions[aid] = resolution

    return OneToOne[AssignId, AssignResolution].instance(resolutions)


def check_assign_resolution_accepted(
    rule_e3007: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3007) == 0


def build_assign_resolution_accepted(
    resolutions: OneToOne[AssignId, AssignResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[AssignId, AssignAcceptance]:
    accepted: dict[AssignId, AssignAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[AssignId, AssignAcceptance].instance(accepted)


def validate_assign_resolution_e3007(
    assigns: OneToOne[AssignId, Assign],
    resolutions: OneToOne[AssignId, AssignResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(report_assign_resolution_e3007(assigns.get(id), _))

    return diagnostics


def report_assign_resolution_e3007(
    entry: Assign,
    rejection: AssignRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3007",
        message=f"Invalid assign {entry}, reason: {rejection.reason}.",
    )
