from typing import Any, Dict, Iterable, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.addresses import AddressId
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.operands import (
    OperandAcceptance,
    OperandRejection,
    OperandResolution,
    OperandSymbol,
)
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def configure_operand_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_operand_resolution,
        constraint=None,
        produces=("resolutions/operands",),
        requires=frozenset(
            {
                ("operands", "entities/operands"),
                ("registers", "resolutions/registers/accepted"),
                ("immediates", "resolutions/immediates/accepted"),
                ("references", "resolutions/references/accepted"),
                ("addresses", "resolutions/addresses/accepted"),
                ("binds", "indices/binds/parameters"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_operand_resolution_e3021,
        constraint=None,
        produces=("rules/e3021",),
        requires=frozenset(
            {
                ("operands", "entities/operands"),
                ("resolutions", "resolutions/operands"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_operand_resolution_accepted,
        constraint=check_operand_resolution_accepted,
        produces=("resolutions/operands/accepted",),
        requires=frozenset(
            {
                ("rule_e3021", "rules/e3021"),
                ("resolutions", "resolutions/operands"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def get_register_symbol(target: RegisterAcceptance) -> OperandSymbol:
    if target.width == 8:
        return "reg8"

    elif target.width == 16:
        return "reg16"

    elif target.width == 32:
        return "reg32"

    else:
        return "reg64"


def get_immediate_symbol(target: ImmediateAcceptance) -> OperandSymbol:
    if target.value.width == 8:
        return "imm8"

    elif target.value.width == 16:
        return "imm16"

    elif target.value.width == 32:
        return "imm32"

    else:
        return "imm64"


def get_bind_symbol(target: ParameterAcceptance, bind: BindAcceptance) -> OperandSymbol:
    if bind.mode == "register":
        return "reg64"

    if target.type.width == 8:
        return "imm8"

    elif target.type.width == 16:
        return "imm16"

    elif target.type.width == 32:
        return "imm32"

    else:
        return "imm64"


def build_operand_resolution(
    operands: OneToOne[OperandId, Operand],
    registers: OneToOne[RegisterId, RegisterAcceptance],
    immediates: OneToOne[ImmediateId, ImmediateAcceptance],
    references: OneToOne[ReferenceId, ReferenceAcceptance],
    addresses: OneToOne[AddressId, AddressAcceptance],
    binds: OneToOne[ParameterId, BindAcceptance],
) -> OneToOne[OperandId, OperandResolution]:
    resolutions: Dict[OperandId, OperandResolution] = {}

    for oid, entry in operands.items():
        resolution = OperandResolution(
            ref=entry.ref,
            id=oid,
            accepted=[],
            rejected=[],
        )

        if entry.kind == "register":
            assert isinstance(entry.target, RegisterId)
            target = registers.get(entry.target)
            symbol = get_register_symbol(target)
            kind = "register"

            if target.kind == "rip":
                resolution.rejected.append(
                    OperandRejection(
                        ref=entry.ref,
                        id=oid,
                        kind=entry.kind,
                        reason="unsupported-register",
                    )
                )

        elif entry.kind == "immediate":
            assert isinstance(entry.target, ImmediateId)
            target = immediates.get(entry.target)
            symbol = get_immediate_symbol(target)
            kind = "immediate"

        elif entry.kind == "reference":
            assert isinstance(entry.target, ReferenceId)
            reference = target = references.get(entry.target)

            if isinstance(reference.target, LabelAcceptance):
                symbol, kind = "rel", "relocation"
                target = reference.target

            else:
                kind, target = "parameter", reference.target
                bind = binds.get(reference.target.id)
                symbol = get_bind_symbol(reference.target, bind)

        else:
            assert isinstance(entry.target, AddressId)
            target = addresses.get(entry.target)
            symbol, kind = "addr", "address"

        if not resolution.rejected:
            resolution.accepted.append(
                OperandAcceptance(
                    ref=entry.ref,
                    id=oid,
                    kind=kind,
                    target=target,
                    symbol=symbol,
                )
            )

        resolutions[oid] = resolution

    return OneToOne[OperandId, OperandResolution].instance(resolutions)


def check_operand_resolution_accepted(
    rule_e3021: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3021) == 0


def build_operand_resolution_accepted(
    resolutions: OneToOne[OperandId, OperandResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[OperandId, OperandAcceptance]:
    accepted: Dict[OperandId, OperandAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[OperandId, OperandAcceptance].instance(accepted)


def validate_operand_resolution_e3021(
    operands: OneToOne[OperandId, Operand],
    resolutions: OneToOne[OperandId, OperandResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_operand_resolution_e3021(operands.get(id), rejection)
                )

    return diagnostics


def report_operand_resolution_e3021(
    entry: Operand, rejection: OperandRejection
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3021",
        message=f"Invalid operand {entry.kind}, reason: {rejection.reason}.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[OperandId, OperandResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[OperandId, OperandResolution]]:
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
    def rows(key: OperandId, entry: OperandResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[OperandId, OperandAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[OperandId, OperandAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "kind": "Kind",
            "symbol": "Symbol",
            "target": "Target",
        }

    @staticmethod
    def rows(key: OperandId, entry: OperandAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "kind": entry.kind,
            "symbol": entry.symbol,
            "target": str(entry.target),
        }
