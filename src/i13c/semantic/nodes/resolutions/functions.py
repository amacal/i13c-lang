from typing import Any, Dict, Iterable, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
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
    flags: OneToOne[FlagsId, FlagsAcceptance],
    statements: OneToOne[StatementId, StatementAcceptance],
) -> OneToOne[FunctionId, FunctionResolution]:
    resolutions: Dict[FunctionId, FunctionResolution] = {}

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
                signature=signatures.get(entry.signature),
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


class ListAllExtractor:
    def __init__(self, data: OneToOne[FunctionId, FunctionResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[FunctionId, FunctionResolution]]:
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
    def rows(key: FunctionId, entry: FunctionResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[FunctionId, FunctionAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[FunctionId, FunctionAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "params": "Parameters",
        }

    @staticmethod
    def rows(key: FunctionId, entry: FunctionAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.signature.name.decode(),
            "params": ", ".join([str(param) for param in entry.signature.parameters]),
        }
