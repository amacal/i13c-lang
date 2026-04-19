from typing import Any, Dict, List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.signatures import Signature, SignatureId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.signatures import (
    SignatureAcceptance,
    SignatureRejection,
    SignatureResolution,
)


def configure_signature_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_signature_resolution,
        constraint=None,
        produces=("resolutions/signatures",),
        requires=frozenset(
            {
                ("signatures", "entities/signatures"),
                ("parameters", "resolutions/parameters/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_signature_resolution_e3003,
        constraint=None,
        produces=("rules/e3003",),
        requires=frozenset(
            {
                ("signatures", "entities/signatures"),
                ("resolutions", "resolutions/signatures"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_signature_resolution_accepted,
        constraint=check_signature_resolution_accepted,
        produces=("resolutions/signatures/accepted",),
        requires=frozenset(
            {
                ("rule_e3003", "rules/e3003"),
                ("resolutions", "resolutions/signatures"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_signature_resolution(
    signatures: OneToOne[SignatureId, Signature],
    parameters: OneToOne[ParameterId, ParameterAcceptance],
) -> OneToOne[SignatureId, SignatureResolution]:
    resolutions: Dict[SignatureId, SignatureResolution] = {}

    for sid, entry in signatures.items():
        resolution = SignatureResolution(
            accepted=[],
            rejected=[],
        )

        names: Set[bytes] = set()
        accepted: List[ParameterAcceptance] = []

        for id in entry.parameters:
            parameter = parameters.get(id)

            if parameter.name not in names:
                names.add(parameter.name)

            else:
                resolution.rejected.append(
                    SignatureRejection(
                        ref=parameter.ref,
                        reason="duplicated-name",
                    )
                )

            # the parameter survived the checks
            accepted.append(parameter)

        if len(resolution.rejected) == 0:
            resolution.accepted.append(
                SignatureAcceptance(
                    ref=entry.ref,
                    id=sid,
                    name=entry.name,
                    parameters=accepted,
                )
            )

        resolutions[sid] = resolution

    return OneToOne[SignatureId, SignatureResolution].instance(resolutions)


def check_signature_resolution_accepted(
    rule_e3003: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3003) == 0


def build_signature_resolution_accepted(
    resolutions: OneToOne[SignatureId, SignatureResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[SignatureId, SignatureAcceptance]:
    accepted: Dict[SignatureId, SignatureAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[SignatureId, SignatureAcceptance].instance(accepted)


def validate_signature_resolution_e3003(
    signatures: OneToOne[SignatureId, Signature],
    resolutions: OneToOne[SignatureId, SignatureResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                if rejection.reason == "duplicated-name":
                    diagnostics.append(
                        report_signature_resolution_e3003(signatures.get(id), rejection)
                    )

    return diagnostics


def report_signature_resolution_e3003(
    entry: Signature,
    rejection: SignatureRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3003",
        message=f"Duplicated parameter name {entry}.",
    )
