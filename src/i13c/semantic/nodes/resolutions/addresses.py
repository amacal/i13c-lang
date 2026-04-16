from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.addresses import Address, AddressId
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.semantic.typing.resolutions.addresses import (
    AddressAcceptance,
    AddressRejection,
    AddressResolution,
    OffsetAcceptance,
)
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def configure_address_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_address_resolution,
        constraint=None,
        produces=("resolutions/addresses",),
        requires=frozenset(
            {
                ("addresses", "entities/addresses"),
                ("registers", "resolutions/registers/accepted"),
                ("immediates", "resolutions/immediates/accepted"),
                ("references", "resolutions/references/accepted"),
            }
        ),
    )

    validate_e3022 = GraphNode(
        builder=validate_address_resolution_e3022,
        constraint=None,
        produces=("rules/e3022",),
        requires=frozenset(
            {
                ("addresses", "entities/addresses"),
                ("resolutions", "resolutions/addresses"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_address_resolution_accepted,
        constraint=check_address_resolution_accepted,
        produces=("resolutions/addresses/accepted",),
        requires=frozenset(
            {
                ("rule_e3022", "rules/e3022"),
                ("resolutions", "resolutions/addresses"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate_e3022, extract])


def build_address_resolution(
    addresses: OneToOne[AddressId, Address],
    registers: OneToOne[RegisterId, RegisterAcceptance],
    immediates: OneToOne[ImmediateId, ImmediateAcceptance],
    references: OneToOne[ReferenceId, ReferenceAcceptance],
) -> OneToOne[AddressId, AddressResolution]:
    resolutions: Dict[AddressId, AddressResolution] = {}

    for aid, entry in addresses.items():
        resolution = AddressResolution(
            accepted=[],
            rejected=[],
        )

        # resolve base register
        if isinstance(entry.base, RegisterId):
            register = registers.get(entry.base)

            if register.kind != "64bit":
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        reason="invalid-register",
                    )
                )

        else:
            register = references.get(entry.base)

        # resolve offset immediate, if present
        if entry.offset is not None:
            immediate = immediates.get(entry.offset.value)

            # reject 64-bit immediates
            if immediate.value.width == 64:
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        reason="invalid-offset",
                    )
                )

            # reject 32-bit immediates with the highest bit set (negative values)
            if immediate.value.width == 32 and immediate.value.highest_bit():
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        reason="invalid-offset",
                    )
                )

            offset = OffsetAcceptance(
                kind=entry.offset.kind,
                value=immediate,
            )

        else:
            offset = None

        if len(resolution.rejected) == 0:
            resolution.accepted.append(
                AddressAcceptance(
                    ref=entry.ref,
                    id=aid,
                    base=register,
                    offset=offset,
                )
            )

        resolutions[aid] = resolution

    return OneToOne[AddressId, AddressResolution].instance(resolutions)


def check_address_resolution_accepted(
    rule_e3022: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3022) == 0


def build_address_resolution_accepted(
    resolutions: OneToOne[AddressId, AddressResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[AddressId, AddressAcceptance]:
    accepted: Dict[AddressId, AddressAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[AddressId, AddressAcceptance].instance(accepted)


def validate_address_resolution_e3022(
    addresses: OneToOne[AddressId, Address],
    resolutions: OneToOne[AddressId, AddressResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_address_resolution_e3022(addresses.get(id), rejection)
                )

    return diagnostics


def report_address_resolution_e3022(
    entry: Address,
    rejection: AddressRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3022",
        message=f"Address resolution failed {str(entry)}, reason: {rejection.reason}.",
    )
