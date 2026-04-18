from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.addr import LEA
from i13c.llvm.typing.instructions.core import (
    ComputedAddress,
    Displacement,
    Register,
    Scaler,
)
from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.operands import OperandSymbol, OperandTarget
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def lower_reg32_addr(
    generator: Generator,
    destination: RegisterAcceptance,
    source: AddressAcceptance,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        LEA(
            dst=Register.parse32(destination.name.decode()),
            src=ComputedAddress(
                base=Register.parse64(source.base.name.decode()),
                disp=Displacement.auto(source.offset),
                scaler=Scaler.none(),
                width=64,
            ),
        ),
    )


def lower_reg64_addr(
    generator: Generator,
    destination: RegisterAcceptance,
    source: AddressAcceptance,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        LEA(
            dst=Register.parse64(destination.name.decode()),
            src=ComputedAddress(
                base=Register.parse64(source.base.name.decode()),
                disp=Displacement.auto(source.offset),
                scaler=Scaler.none(),
                width=64,
            ),
        ),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        destination: OperandTarget,
        source: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[Tuple[OperandSymbol, OperandSymbol], InstructionHandler] = {
    ("reg32", "addr"): lower_reg32_addr,
    ("reg64", "addr"): lower_reg64_addr,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_lea(
    generator: Generator,
    instruction: InstructionAcceptance,
) -> InstructionEntry:

    # find operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # find handler and call it
    handler = DISPATCH_TABLE[(dst.symbol, src.symbol)]
    return handler(generator, dst.target, src.target)
