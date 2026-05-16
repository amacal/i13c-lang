from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.flags import FlagsAcceptance
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
                ("flags", "resolutions/flags/accepted"),
                ("statements", "resolutions/statements/accepted"),
            }
        ),
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
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_functions_resolution(
    functions: OneToOne[FunctionId, Function],
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    flags: OneToOne[FlagsId, FlagsAcceptance],
    statements: OneToOne[StatementId, StatementAcceptance],
) -> OneToOne[FunctionId, FunctionResolution]:
    resolutions: Dict[FunctionId, FunctionResolution] = {}

    for fid, entry in functions.items():
        resolution = FunctionResolution(
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            FunctionAcceptance(
                id=fid,
                ref=entry.ref,
            )
        )

        resolutions[fid] = resolution

    return OneToOne[FunctionId, FunctionResolution].instance(resolutions)


def check_functions_resolution_accepted(
    rule_e3026: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3026) == 0


def build_functions_resolution_accepted(
    resolutions: OneToOne[FunctionId, FunctionResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[FunctionId, FunctionAcceptance]:
    accepted: Dict[FunctionId, FunctionAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[FunctionId, FunctionAcceptance].instance(accepted)


def validate_functions_resolution_e3026(
    functions: OneToOne[FunctionId, Function],
    resolutions: OneToOne[FunctionId, FunctionResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

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
