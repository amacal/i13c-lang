from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.bits import SHL
from i13c.llvm.typing.instructions.core import Immediate, Register
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.operands import OperandSymbol, OperandTarget
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def lower_reg8_imm8(
    generator: Generator,
    destination: RegisterAcceptance,
    source: ImmediateAcceptance,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        SHL(
            dst=Register.parse8(destination.name.decode()),
            src=Immediate.imm8(source.value.data),
        ),
    )


def lower_reg16_imm8(
    generator: Generator,
    destination: RegisterAcceptance,
    source: ImmediateAcceptance,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        SHL(
            dst=Register.parse16(destination.name.decode()),
            src=Immediate.imm8(source.value.data),
        ),
    )


def lower_reg32_imm8(
    generator: Generator,
    destination: RegisterAcceptance,
    source: ImmediateAcceptance,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        SHL(
            dst=Register.parse32(destination.name.decode()),
            src=Immediate.imm8(source.value.data),
        ),
    )


def lower_reg64_imm8(
    generator: Generator,
    destination: RegisterAcceptance,
    source: ImmediateAcceptance,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        SHL(
            dst=Register.parse64(destination.name.decode()),
            src=Immediate.imm8(source.value.data),
        ),
    )


def lower_reg64_cl(
    generator: Generator,
    destination: RegisterAcceptance,
    source: RegisterAcceptance,
) -> InstructionEntry:

    # verify that source is indeed cl
    assert source.name == b"cl"

    return (
        InstructionId(value=generator.next()),
        SHL(
            dst=Register.parse64(destination.name.decode()),
            src=Register.parse8(source.name.decode()),
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
    ("reg8", "imm8"): lower_reg8_imm8,
    ("reg16", "imm8"): lower_reg16_imm8,
    ("reg32", "imm8"): lower_reg32_imm8,
    ("reg64", "imm8"): lower_reg64_imm8,
    ("reg64", "reg8"): lower_reg64_cl,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_shl(
    generator: Generator,
    instruction: InstructionAcceptance,
) -> InstructionEntry:

    # find operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # find handler and call it
    handler = DISPATCH_TABLE[(dst.symbol, src.symbol)]
    return handler(generator, dst.target, src.target)
