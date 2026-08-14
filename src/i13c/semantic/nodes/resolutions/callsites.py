from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
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
        views=GraphViews(list=ListAllExtractor),
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
        views=GraphViews(list=ListAcceptedExtractor),
    )

    reject = GraphNode(
        builder=build_callsite_resolution_rejected,
        constraint=None,
        produces=("resolutions/callsites/rejected",),
        requires=frozenset({("resolutions", "resolutions/callsites")}),
        views=GraphViews(list=ListRejectedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract, reject])


def build_callsite_resolution(
    callsites: OneToOne[CallSiteId, CallSite],
    functions: OneToOne[FunctionId, Function],
    expressions: OneToOne[ExpressionId, Expression],
    cflows: OneToOne[FunctionId, ControlFlowAcceptance],
    literals: OneToOne[LiteralId, LiteralAcceptance],
    signatures: OneToMany[bytes, SignatureAcceptance],
) -> OneToOne[CallSiteId, CallSiteResolution]:
    resolutions: dict[CallSiteId, CallSiteResolution] = {}

    for sid, entry in callsites.items():
        resolution = CallSiteResolution(
            ref=entry.ref,
            id=sid,
            accepted=[],
            rejected=[],
        )

        function_id = entry.get_function(FunctionId.from_context)
        stmt_id = entry.get_statement(StatementId.from_context)

        environment = cflows.get(function_id).environments[stmt_id]
        rejected: CallSiteRejectionReason | None = "unknown-target"

        if len(entry.arguments) > 6:
            resolution.rejected.append(
                CallSiteRejection(
                    ref=entry.ref,
                    id=sid,
                    target=entry,
                    reason="too-many-arguments",
                )
            )

        elif found := signatures.find(entry.callee):
            for signature in found:
                rejected = None
                arguments: list[CallSiteArgument] = []

                if len(signature.parameters) != len(entry.arguments):
                    resolution.rejected.append(
                        CallSiteRejection(
                            ref=entry.ref,
                            id=sid,
                            target=entry,
                            reason="arity-mismatch",
                        )
                    )

                    continue

                for parameter, argument in zip(signature.parameters, entry.arguments):
                    target: LiteralAcceptance | ParameterAcceptance | ValueAcceptance | None

                    if isinstance(argument, LiteralId):
                        target = literals.get(argument)
                    else:
                        expr = expressions.get(argument)
                        target = environment.get(expr.name)

                    # if a symbol is not in the environment
                    if target is None:
                        rejected = "unknown-target"
                        break

                    if parameter.bind == "literal": # noqa: SIM102
                        if not isinstance(argument, LiteralId):
                            rejected = "not-literal"
                            break

                    if isinstance(target, LiteralAcceptance):
                        if not parameter.type.accepts(target):
                            rejected = "type-mismatch"
                            break

                    # parameter and value have a type field
                    elif not parameter.type.accepts(target.type):
                        rejected = "type-mismatch"
                        break

                    arguments.append(target)

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
                        id=sid,
                        target=entry,
                        reason=rejected,
                    )
                )

        if not resolution.accepted and not resolution.rejected:
            resolution.rejected.append(
                CallSiteRejection(
                    ref=entry.ref,
                    id=sid,
                    target=entry,
                    reason="unknown-target",
                )
            )

        if len(resolution.accepted) > 1:
            resolution.rejected.append(
                CallSiteRejection(
                    ref=entry.ref,
                    id=sid,
                    target=entry,
                    reason="ambiguous-target",
                )
            )

        resolutions[sid] = resolution

    return OneToOne[CallSiteId, CallSiteResolution].instance(resolutions)


def check_callsite_resolution_accepted(
    rule_e3006: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3006) == 0


def build_callsite_resolution_accepted(
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[CallSiteId, CallSiteAcceptance]:
    accepted: dict[CallSiteId, CallSiteAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[CallSiteId, CallSiteAcceptance].instance(accepted)


def build_callsite_resolution_rejected(
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
    **kwargs: dict[str, Any],
) -> OneToMany[CallSiteId, CallSiteRejection]:
    rejected: dict[CallSiteId, list[CallSiteRejection]] = {}

    for id, resolution in resolutions.items():
        rejected[id] = resolution.rejected

    return OneToMany[CallSiteId, CallSiteRejection].instance(rejected)


def validate_callsite_resolution_e3006(
    callsites: OneToOne[CallSiteId, CallSite],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

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


class ListAllExtractor:
    def __init__(self, data: OneToOne[CallSiteId, CallSiteResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[CallSiteId, CallSiteResolution]]:
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
    def rows(key: CallSiteId, entry: CallSiteResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListRejectedExtractor:
    def __init__(self, data: OneToMany[CallSiteId, CallSiteRejection]):
        self.data = data

    def extract(self) -> Iterable[tuple[CallSiteId, CallSiteRejection]]:
        for key, entries in self.data.items():
            for entry in entries:
                yield key, entry

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "callee": "Callee",
            "reason": "Reason",
        }

    @staticmethod
    def rows(key: CallSiteId, entry: CallSiteRejection) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "callee": entry.target.callee.decode(),
            "reason": entry.reason,
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[CallSiteId, CallSiteAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[CallSiteId, CallSiteAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "args": "Arguments",
            "params": "Parameters",
        }

    @staticmethod
    def rows(key: CallSiteId, entry: CallSiteAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.signature.name.decode(),
            "args": ", ".join([str(arg) for arg in entry.arguments]),
            "params": ", ".join(
                [param.name.decode() for param in entry.signature.parameters]
            ),
        }
