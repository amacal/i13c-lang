from typing import Any, Dict, Iterable, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
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
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
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
        views=GraphViews(list=ListAllExtractor),
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
        views=GraphViews(list=ListAcceptedExtractor),
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
            ref=entry.ref,
            id=aid,
            accepted=[],
            rejected=[],
        )

        # assume no offset is available
        offset, register = None, None

        # resolve base register
        if isinstance(entry.base, RegisterId):
            register = registers.get(entry.base)

            if register.kind != "64bit":
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        id=aid,
                        reason="invalid-register",
                    )
                )

        else:
            reference = references.get(entry.base)

            if not isinstance(reference.target, ParameterAcceptance):
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        id=aid,
                        reason="invalid-register",
                    )
                )

            # reject base bound to immediate values
            elif reference.target.bind == "literal":
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        id=aid,
                        reason="invalid-register",
                    )
                )

            else:
                register = reference.target

        # resolve offset immediate, if present
        if entry.offset is not None:
            immediate = immediates.get(entry.offset.value)

            # reject 64-bit immediates
            if immediate.value.width == 64:
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        id=aid,
                        reason="invalid-offset",
                    )
                )

            # reject 32-bit immediates with the highest bit set (negative values)
            elif immediate.value.width == 32 and immediate.value.highest_bit():
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        id=aid,
                        reason="invalid-offset",
                    )
                )

            else:
                offset = OffsetAcceptance(
                    kind=entry.offset.kind,
                    value=immediate,
                    width=immediate.value.width,
                )

        if len(resolution.rejected) == 0:
            assert register is not None

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


class ListAllExtractor:
    def __init__(self, data: OneToOne[AddressId, AddressResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[AddressId, AddressResolution]]:
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
    def rows(key: AddressId, entry: AddressResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[AddressId, AddressAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[AddressId, AddressAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "base": "Base",
            "okind": "Offset Kind",
            "owidth": "Offset Width",
            "ovalue": "Offset Value",
        }

    @staticmethod
    def rows(key: AddressId, entry: AddressAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "base": entry.base.name.decode() if isinstance(entry.base, RegisterAcceptance) else entry.base.name.decode(),
            "okind": entry.offset.kind if entry.offset else "",
            "owidth": str(entry.offset.value.value.width) if entry.offset else "",
            "ovalue": str(entry.offset.value.value) if entry.offset else "",
        }
