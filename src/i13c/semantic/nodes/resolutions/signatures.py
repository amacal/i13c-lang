from typing import Any, Dict, List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.signatures import Signature, SignatureId
from i13c.semantic.typing.entities.slots import SlotId
from i13c.semantic.typing.resolutions.signatures import (
    SignatureAcceptance,
    SignatureRejection,
    SignatureResolution,
)
from i13c.semantic.typing.resolutions.slots import SlotAcceptance


def configure_signature_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_signature_resolution,
        constraint=None,
        produces=("resolutions/signatures",),
        requires=frozenset(
            {
                ("signatures", "entities/signatures"),
                ("slots", "resolutions/slots/accepted"),
            }
        ),
    )

    validate_e3003 = GraphNode(
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

    validate_e3015 = GraphNode(
        builder=validate_signature_resolution_e3015,
        constraint=None,
        produces=("rules/e3015",),
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
                ("rule_e3015", "rules/e3015"),
                ("resolutions", "resolutions/signatures"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate_e3003, validate_e3015, extract])


def build_signature_resolution(
    signatures: OneToOne[SignatureId, Signature],
    slots: OneToOne[SlotId, SlotAcceptance],
) -> OneToOne[SignatureId, SignatureResolution]:
    resolutions: Dict[SignatureId, SignatureResolution] = {}

    for sid, entry in signatures.items():
        resolution = SignatureResolution(
            accepted=[],
            rejected=[],
        )

        names: Set[bytes] = set()
        registers: Set[bytes] = set()
        accepted: List[SlotAcceptance] = []

        for id in entry.slots:
            slot = slots.get(id)

            if slot.name not in names:
                names.add(slot.name)

            else:
                resolution.rejected.append(
                    SignatureRejection(
                        ref=slot.ref,
                        reason="duplicated-name",
                    )
                )

            if slot.bind.mode == "register":
                if slot.bind.target not in registers:
                    registers.add(slot.bind.target)

                else:
                    resolution.rejected.append(
                        SignatureRejection(
                            ref=slot.ref,
                            reason="duplicated-register",
                        )
                    )

            # the slot survived the checks
            accepted.append(slot)

        if len(resolution.rejected) == 0:
            resolution.accepted.append(
                SignatureAcceptance(
                    ref=entry.ref,
                    id=sid,
                    name=entry.name,
                    slots=accepted,
                )
            )

        resolutions[sid] = resolution

    return OneToOne[SignatureId, SignatureResolution].instance(resolutions)


def check_signature_resolution_accepted(
    rule_e3003: List[Diagnostic],
    rule_e3015: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3003) + len(rule_e3015) == 0


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
        message=f"Duplicated slot name {entry}.",
    )


def validate_signature_resolution_e3015(
    signatures: OneToOne[SignatureId, Signature],
    resolutions: OneToOne[SignatureId, SignatureResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                if rejection.reason == "duplicated-register":
                    diagnostics.append(
                        report_signature_resolution_e3015(signatures.get(id), rejection)
                    )

    return diagnostics


def report_signature_resolution_e3015(
    entry: Signature,
    rejection: SignatureRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3015",
        message=f"Duplicated register name {entry}.",
    )
