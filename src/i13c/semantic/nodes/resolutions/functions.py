from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.analyses.noreturns import NoReturn
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.functions import (
    FunctionAcceptance,
    FunctionRejection,
    FunctionResolution,
)
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.statements import StatementAcceptance


def configure_function_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_functions_resolution,
        constraint=None,
        produces=("resolutions/functions",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("signatures", "resolutions/signatures/accepted"),
                ("noreturns", "analyses/noreturns"),
                ("cflows", "analyses/cflows"),
                ("statements", "resolutions/statements/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_functions_resolution_e3026,
        constraint=None,
        produces=("rules/e3026",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("resolutions", "resolutions/functions"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_functions_resolution_accepted,
        constraint=check_functions_resolution_accepted,
        produces=("resolutions/functions/accepted",),
        requires=frozenset(
            {
                ("rule_e3026", "rules/e3026"),
                ("resolutions", "resolutions/functions"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_functions_resolution(
    functions: OneToOne[FunctionId, Function],
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    noreturns: OneToOne[SignatureId, NoReturn],
    cflows: OneToOne[FunctionId, ControlFlows],
    statements: OneToOne[StatementId, StatementAcceptance],
) -> OneToOne[FunctionId, FunctionResolution]:
    resolutions: dict[FunctionId, FunctionResolution] = {}

    for fid, entry in functions.items():
        resolution = FunctionResolution(
            ref=entry.ref,
            id=fid,
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            FunctionAcceptance(
                ref=entry.ref,
                id=fid,
                cflow=cflows.get(fid),
                signature=signatures.get(entry.signature),
                noreturn=noreturns.get(entry.signature).outcome,
            )
        )

        resolutions[fid] = resolution

    return OneToOne[FunctionId, FunctionResolution].instance(resolutions)


def check_functions_resolution_accepted(
    rule_e3026: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3026) == 0


def build_functions_resolution_accepted(
    resolutions: OneToOne[FunctionId, FunctionResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[FunctionId, FunctionAcceptance]:
    accepted: dict[FunctionId, FunctionAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[FunctionId, FunctionAcceptance].instance(accepted)


def validate_functions_resolution_e3026(
    functions: OneToOne[FunctionId, Function],
    resolutions: OneToOne[FunctionId, FunctionResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_functions_resolution_e3026(functions.get(id), rejection)
                )

    return diagnostics


def report_functions_resolution_e3026(
    entry: Function,
    rejection: FunctionRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3026",
        message=f"Function rejected {entry}, reason: {rejection.reason}.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[FunctionId, FunctionResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, FunctionResolution]]:
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
    def rows(key: FunctionId, entry: FunctionResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[FunctionId, FunctionAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, FunctionAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "params": "Parameters",
        }

    @staticmethod
    def rows(key: FunctionId, entry: FunctionAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.signature.name.decode(),
            "noreturn": str(entry.noreturn),
            "params": ", ".join([str(param) for param in entry.signature.parameters]),
        }
