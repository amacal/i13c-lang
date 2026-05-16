from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.calls import CallId
from i13c.semantic.typing.entities.statements import Statement, StatementId
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.calls import CallAcceptance
from i13c.semantic.typing.resolutions.statements import (
    StatementAcceptance,
    StatementRejection,
    StatementResolution,
)


def configure_statement_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_statements_resolution,
        constraint=None,
        produces=("resolutions/statements",),
        requires=frozenset(
            {
                ("statements", "entities/statements"),
                ("assigns", "resolutions/assigns/accepted"),
                ("calls", "resolutions/calls/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_statements_resolution_e3026,
        constraint=None,
        produces=("rules/e3027",),
        requires=frozenset(
            {
                ("statements", "entities/statements"),
                ("resolutions", "resolutions/statements"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_statements_resolution_accepted,
        constraint=check_statements_resolution_accepted,
        produces=("resolutions/statements/accepted",),
        requires=frozenset(
            {
                ("rule_e3027", "rules/e3027"),
                ("resolutions", "resolutions/statements"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_statements_resolution(
    statements: OneToOne[StatementId, Statement],
    assigns: OneToOne[AssignId, AssignAcceptance],
    calls: OneToOne[CallId, CallAcceptance],
) -> OneToOne[StatementId, StatementResolution]:
    resolutions: Dict[StatementId, StatementResolution] = {}

    for fid, entry in statements.items():
        resolution = StatementResolution(
            accepted=[],
            rejected=[],
        )

        if isinstance(entry.target, AssignId):
            target = assigns.get(entry.target)
        else:
            target = calls.get(entry.target)

        resolution.accepted.append(
            StatementAcceptance(
                id=fid,
                ref=entry.ref,
                target=target,
            )
        )

        resolutions[fid] = resolution

    return OneToOne[StatementId, StatementResolution].instance(resolutions)


def check_statements_resolution_accepted(
    rule_e3027: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3027) == 0


def build_statements_resolution_accepted(
    resolutions: OneToOne[StatementId, StatementResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[StatementId, StatementAcceptance]:
    accepted: Dict[StatementId, StatementAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[StatementId, StatementAcceptance].instance(accepted)


def validate_statements_resolution_e3026(
    statements: OneToOne[StatementId, Statement],
    resolutions: OneToOne[StatementId, StatementResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_statements_resolution_e3026(statements.get(id), rejection)
                )

    return diagnostics


def report_statements_resolution_e3026(
    entry: Statement,
    rejection: StatementRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3026",
        message=f"Statement rejected {entry}, reason: {rejection.reason}.",
    )
