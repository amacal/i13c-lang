from typing import Any, Dict, List, Optional, Union

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.callsites import (
    CallSiteAcceptance,
    CallSiteArgument,
    CallSiteRejection,
    CallSiteRejectionReason,
    CallSiteResolution,
)
from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance


def configure_callsite_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_callsite_resolution,
        constraint=None,
        produces=("resolutions/callsites",),
        requires=frozenset(
            {
                ("callsites", "entities/callsites"),
                ("functions", "entities/functions"),
                ("expressions", "entities/expressions"),
                ("cflows", "resolutions/cflows/accepted"),
                ("literals", "resolutions/literals/accepted"),
                ("signatures", "indices/signatures/names"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_callsite_resolution_e3006,
        constraint=None,
        produces=("rules/e3006",),
        requires=frozenset(
            {
                ("callsites", "entities/callsites"),
                ("resolutions", "resolutions/callsites"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_callsite_resolution_accepted,
        constraint=check_callsite_resolution_accepted,
        produces=("resolutions/callsites/accepted",),
        requires=frozenset(
            {
                ("rule_e3006", "rules/e3006"),
                ("resolutions", "resolutions/callsites"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_callsite_resolution(
    callsites: OneToOne[CallSiteId, CallSite],
    functions: OneToOne[FunctionId, Function],
    expressions: OneToOne[ExpressionId, Expression],
    cflows: OneToOne[FunctionId, ControlFlowAcceptance],
    literals: OneToOne[LiteralId, LiteralAcceptance],
    signatures: OneToMany[bytes, SignatureAcceptance],
) -> OneToOne[CallSiteId, CallSiteResolution]:
    resolutions: Dict[CallSiteId, CallSiteResolution] = {}

    for sid, entry in callsites.items():
        resolution = CallSiteResolution(
            accepted=[],
            rejected=[],
        )

        function_id = entry.get_function(FunctionId.from_context)
        stmt_id = entry.get_statement(StatementId.from_context)

        environment = cflows.get(function_id).environments[stmt_id]
        rejected: Optional[CallSiteRejectionReason] = "unknown-target"

        if found := signatures.find(entry.callee):
            for signature in found:
                rejected = None
                arguments: List[CallSiteArgument] = []

                if len(signature.parameters) != len(entry.arguments):
                    resolution.rejected.append(
                        CallSiteRejection(
                            ref=entry.ref,
                            reason="arity-mismatch",
                        )
                    )

                    continue

                for parameter, argument in zip(signature.parameters, entry.arguments):
                    target: Optional[
                        Union[LiteralAcceptance, ParameterAcceptance, ValueAcceptance]
                    ]

                    if isinstance(argument, LiteralId):
                        target = literals.get(argument)
                    else:
                        expr = expressions.get(argument)
                        target = environment.get(expr.name)

                    # if a symbol is not in the environment
                    if target is None:
                        rejected = "unknown-target"
                        break

                    else:
                        arguments.append(target)

                    if isinstance(target, LiteralAcceptance):
                        if not parameter.type.accepts(target):
                            rejected = "type-mismatch"
                            break

                    # parameter and value have a type field
                    elif not parameter.type.accepts(target.type):
                        rejected = "type-mismatch"
                        break

                if rejected is None:
                    resolution.accepted.append(
                        CallSiteAcceptance(
                            ref=entry.ref,
                            id=sid,
                            sig=functions.get(function_id).signature,
                            stmt=stmt_id,
                            signature=signature,
                            arguments=arguments,
                        )
                    )

            if rejected is not None:
                resolution.rejected.append(
                    CallSiteRejection(
                        ref=entry.ref,
                        reason=rejected,
                    )
                )

        if not resolution.accepted and not resolution.rejected:
            resolution.rejected.append(
                CallSiteRejection(
                    ref=entry.ref,
                    reason="unknown-target",
                )
            )

        if len(resolution.accepted) > 1:
            resolution.rejected.append(
                CallSiteRejection(
                    ref=entry.ref,
                    reason="ambiguous-target",
                )
            )

        resolutions[sid] = resolution

    return OneToOne[CallSiteId, CallSiteResolution].instance(resolutions)


def check_callsite_resolution_accepted(
    rule_e3006: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3006) == 0


def build_callsite_resolution_accepted(
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[CallSiteId, CallSiteAcceptance]:
    accepted: Dict[CallSiteId, CallSiteAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[CallSiteId, CallSiteAcceptance].instance(accepted)


def validate_callsite_resolution_e3006(
    callsites: OneToOne[CallSiteId, CallSite],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_callsite_resolution_e3006(callsites.get(id), rejection)
                )

    return diagnostics


def report_callsite_resolution_e3006(
    entry: CallSite,
    rejection: CallSiteRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3006",
        message=f"Unresolvable callsite {entry}, reason: {rejection.reason}.",
    )
