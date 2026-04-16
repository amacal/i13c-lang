from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.addresses import AddressId
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.operand import Operand, OperandId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.operands import (
    OperandAcceptance,
    OperandRejection,
    OperandResolution,
)
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def configure_operand_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_operand_resolution,
        constraint=None,
        produces=("resolutions/operands",),
        requires=frozenset(
            {
                ("operands", "entities/operand"),
                ("registers", "resolutions/registers/accepted"),
                ("immediates", "resolutions/immediates/accepted"),
                ("references", "resolutions/references/accepted"),
                ("addresses", "resolutions/addresses/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_operand_resolution_e3021,
        constraint=None,
        produces=("rules/e3021",),
        requires=frozenset(
            {
                ("operands", "entities/operand"),
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
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_operand_resolution(
    operands: OneToOne[OperandId, Operand],
    registers: OneToOne[RegisterId, RegisterAcceptance],
    immediates: OneToOne[ImmediateId, ImmediateAcceptance],
    references: OneToOne[ReferenceId, ReferenceAcceptance],
    addresses: OneToOne[AddressId, AddressAcceptance],
) -> OneToOne[OperandId, OperandResolution]:
    resolutions: Dict[OperandId, OperandResolution] = {}

    for oid, entry in operands.items():
        resolution = OperandResolution(
            accepted=[],
            rejected=[],
        )

        if entry.kind == "register":
            assert isinstance(entry.target, RegisterId)
            target = registers.get(entry.target)

            if target.kind == "rip":
                resolution.rejected.append(
                    OperandRejection(
                        ref=entry.ref,
                        kind=entry.kind,
                        reason="unsupported-register",
                    )
                )

        elif entry.kind == "immediate":
            assert isinstance(entry.target, ImmediateId)
            target = immediates.get(entry.target)

        elif entry.kind == "reference":
            assert isinstance(entry.target, ReferenceId)
            target = references.get(entry.target)

        else:
            assert isinstance(entry.target, AddressId)
            target = addresses.get(entry.target)

        if not resolution.rejected:
            resolution.accepted.append(
                OperandAcceptance(
                    ref=entry.ref,
                    id=oid,
                    kind=entry.kind,
                    target=target,
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
