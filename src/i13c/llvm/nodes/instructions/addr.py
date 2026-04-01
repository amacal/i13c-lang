from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.addr import LeaReg32Off, LeaReg64Off
from i13c.llvm.typing.registers import name_to_reg32, name_to_reg64
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Address,
    Operand,
    OperandId,
    OperandSymbol,
    OperandTarget,
    Register,
)


def lower_reg32_addr64(
    generator: Generator,
    destination: Register,
    source: Address,
) -> InstructionEntry:

    dst = name_to_reg32(destination.name.decode())
    src = name_to_reg64(source.base.name.decode())
    off = source.offset.value if source.offset is not None else 0

    return (
        InstructionId(value=generator.next()),
        LeaReg32Off(dst=dst, off=off, src=src),
    )


def lower_reg64_addr64(
    generator: Generator,
    destination: Register,
    source: Address,
) -> InstructionEntry:

    dst = name_to_reg64(destination.name.decode())
    src = name_to_reg64(source.base.name.decode())
    off = source.offset.value if source.offset is not None else 0

    return (
        InstructionId(value=generator.next()),
        LeaReg64Off(dst=dst, off=off, src=src),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        destination: OperandTarget,
        source: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[Tuple[OperandSymbol, OperandSymbol], InstructionHandler] = {
    (b"reg32", b"addr"): lower_reg32_addr64,
    (b"reg64", b"addr"): lower_reg64_addr64,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_lea(
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
