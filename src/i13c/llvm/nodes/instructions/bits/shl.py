from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.bits import (
    ShlReg8Imm8,
    ShlReg16Imm8,
    ShlReg32Imm8,
    ShlReg64Cl,
    ShlReg64Imm8,
)
from i13c.llvm.typing.registers import (
    name_to_reg8,
    name_to_reg16,
    name_to_reg32,
    name_to_reg64,
)
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Immediate,
    Operand,
    OperandId,
    OperandSymbol,
    OperandTarget,
    Register,
)


def lower_reg8_imm8(
    generator: Generator,
    destination: Register,
    source: Immediate,
) -> InstructionEntry:

    dst = name_to_reg8(destination.name.decode())

    return (
        InstructionId(value=generator.next()),
        ShlReg8Imm8(dst=dst, imm=source.value),
    )

def lower_reg16_imm8(
    generator: Generator,
    destination: Register,
    source: Immediate,
) -> InstructionEntry:

    dst = name_to_reg16(destination.name.decode())

    return (
        InstructionId(value=generator.next()),
        ShlReg16Imm8(dst=dst, imm=source.value),
    )


def lower_reg32_imm8(
    generator: Generator,
    destination: Register,
    source: Immediate,
) -> InstructionEntry:

    dst = name_to_reg32(destination.name.decode())

    return (
        InstructionId(value=generator.next()),
        ShlReg32Imm8(dst=dst, imm=source.value),
    )


def lower_reg64_imm8(
    generator: Generator,
    destination: Register,
    source: Immediate,
) -> InstructionEntry:

    dst = name_to_reg64(destination.name.decode())

    return (
        InstructionId(value=generator.next()),
        ShlReg64Imm8(dst=dst, imm=source.value),
    )

def lower_reg64_cl(
    generator: Generator,
    destination: Register,
    source: Register,
) -> InstructionEntry:

    # verify that source is indeed cl
    assert source.name == b"cl"

    return (
        InstructionId(value=generator.next()),
        ShlReg64Cl(dst=name_to_reg64(destination.name.decode())),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        destination: OperandTarget,
        source: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[Tuple[OperandSymbol, OperandSymbol], InstructionHandler] = {
    (b"reg8", b"imm8"): lower_reg8_imm8,
    (b"reg16", b"imm8"): lower_reg16_imm8,
    (b"reg32", b"imm8"): lower_reg32_imm8,
    (b"reg64", b"imm8"): lower_reg64_imm8,
    (b"reg64", b"reg8"): lower_reg64_cl,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_shl(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    # first try out rewritten operands
    dst = rewritten.get(instruction.operands[0])
    src = rewritten.get(instruction.operands[1])

    # fallback to original operands if not rewritten
    dst = dst or operands.get(instruction.operands[0])
    src = src or operands.get(instruction.operands[1])

    # find handler and call it
    handler = DISPATCH_TABLE[(dst.target.symbol(), src.target.symbol())]
    return handler(generator, dst.target, src.target)
