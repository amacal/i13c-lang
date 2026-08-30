from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.addresses import Address, AddressId
from i13c.semantic.typing.entities.displacements import DisplacementId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.semantic.typing.entities.indices import IndexId
from i13c.semantic.typing.resolutions.addresses import (
    AddressAcceptance,
    AddressRejection,
    AddressResolution,
)
from i13c.semantic.typing.resolutions.indices import IndexAcceptance
from i13c.semantic.typing.resolutions.displacements import DisplacementAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span


def configure_address_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_address_resolution,
        constraint=None,
        produces=("resolutions/addresses",),
        requires=frozenset(
            {
                ("addresses", "entities/addresses"),
                ("indices", "resolutions/indices/accepted"),
                ("registers", "resolutions/registers/accepted"),
                ("references", "resolutions/references/accepted"),
                ("displacements", "resolutions/displacements/accepted"),
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
    indices: OneToOne[IndexId, IndexAcceptance],
    registers: OneToOne[RegisterId, RegisterAcceptance],
    references: OneToOne[ReferenceId, ReferenceAcceptance],
    displacements: OneToOne[DisplacementId, DisplacementAcceptance],
) -> OneToOne[AddressId, AddressResolution]:
    resolutions: dict[AddressId, AddressResolution] = {}

    for aid, entry in addresses.items():
        resolution = AddressResolution(
            ref=entry.ref,
            id=aid,
            accepted=[],
            rejected=[],
        )

        # assume no displacement nor registers are available
        disp, base, indx = None, None, None

        # resolve base register
        if entry.base is not None:
            match resolve_register(aid, entry.ref, entry.base, registers, references):
                case AddressRejection() as rejection:
                    resolution.rejected.append(rejection)
                case RegisterAcceptance() as register:
                    base = register
                case ParameterAcceptance() as register:
                    base = register

        # resolve index register, if present
        if entry.indx is not None:
            indx = indices.get(entry.indx)

        if isinstance(indx, RegisterAcceptance):
            if indx.name == b"rsp":  # noqa: SIM102
                resolution.rejected.append(
                    AddressRejection(
                        ref=entry.ref,
                        id=aid,
                        reason="invalid-index",
                    )
                )

        # resolve displacement, if present
        if entry.disp is not None:
            disp = displacements.get(entry.disp)

        if len(resolution.rejected) == 0:
            resolution.accepted.append(
                AddressAcceptance(
                    ref=entry.ref,
                    id=aid,
                    base=base,
                    indx=indx,
                    disp=disp,
                )
            )

        resolutions[aid] = resolution

    return OneToOne[AddressId, AddressResolution].instance(resolutions)


def resolve_register(
    aid: AddressId,
    ref: Span,
    target: RegisterId | ReferenceId,
    registers: OneToOne[RegisterId, RegisterAcceptance],
    references: OneToOne[ReferenceId, ReferenceAcceptance],
) -> RegisterAcceptance | ParameterAcceptance | AddressRejection:

    if isinstance(target, RegisterId):
        register = registers.get(target)

        if register.kind != "64bit":
            return AddressRejection(
                ref=ref,
                id=aid,
                reason="invalid-register",
            )

        return register

    else:
        reference = references.get(target)

        if (
            not isinstance(reference.target, ParameterAcceptance)
            or reference.target.bind == "literal"
        ):
            return AddressRejection(
                ref=ref,
                id=aid,
                reason="invalid-register",
            )

        return reference.target


def check_address_resolution_accepted(
    rule_e3022: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3022) == 0


def build_address_resolution_accepted(
    resolutions: OneToOne[AddressId, AddressResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[AddressId, AddressAcceptance]:
    accepted: dict[AddressId, AddressAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[AddressId, AddressAcceptance].instance(accepted)


def validate_address_resolution_e3022(
    addresses: OneToOne[AddressId, Address],
    resolutions: OneToOne[AddressId, AddressResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

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
        message=f"Address resolution failed {entry!s}, reason: {rejection.reason}.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[AddressId, AddressResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[AddressId, AddressResolution]]:
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
    def rows(key: AddressId, entry: AddressResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[AddressId, AddressAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[AddressId, AddressAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "base": "Base",
            "indx": "Index",
            "disp": "Displacement",
        }

    @staticmethod
    def rows(key: AddressId, entry: AddressAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "base": entry.base.name.decode() if entry.base else "",
            "indx": str(entry.indx) if entry.indx else "",
            "disp": str(entry.disp) if entry.disp else "",
        }
