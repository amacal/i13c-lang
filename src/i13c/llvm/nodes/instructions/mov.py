from typing import Dict, Protocol, Tuple, Type

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import (
    InstructionEntry,
    InstructionId,
    MovOffImm,
    MovOffReg,
    MovRegImm,
    MovRegReg,
)
from i13c.llvm.typing.registers import IR_REGISTER_FORWARD
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Address,
    Immediate,
    Operand,
    OperandId,
    OperandTarget,
    Register,
)


def lower_register_immediate(
    generator: Generator,
    destination: Register,
    source: Immediate,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD[destination.name]
    imm = source.value

    return (
        InstructionId(value=generator.next()),
        MovRegImm(dst=dst, imm=imm),
    )


def lower_register_register(
    generator: Generator,
    destination: Register,
    source: Register,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD[destination.name]
    src = IR_REGISTER_FORWARD[source.name]

    return (
        InstructionId(value=generator.next()),
        MovRegReg(dst=dst, src=src),
    )


def lower_address_immediate(
    generator: Generator,
    destination: Address,
    source: Immediate,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD[destination.base.name]
    off = destination.offset.value if destination.offset is not None else 0

    return (
        InstructionId(value=generator.next()),
        MovOffImm(dst=dst, off=off, imm=source.value),
    )


def lower_address_register(
    generator: Generator,
    destination: Address,
    source: Register,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD[destination.base.name]
    src = IR_REGISTER_FORWARD[source.name]
    off = destination.offset.value if destination.offset is not None else 0

    return (
        InstructionId(value=generator.next()),
        MovOffReg(dst=dst, off=off, src=src),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        destination: OperandTarget,
        source: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[
    Tuple[Type[OperandTarget], Type[OperandTarget]], InstructionHandler
] = {
    (Register, Immediate): lower_register_immediate,
    (Register, Register): lower_register_register,
    (Address, Immediate): lower_address_immediate,
    (Address, Register): lower_address_register,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_mov(
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
    handler = DISPATCH_TABLE[(type(dst.target), type(src.target))]
    return handler(generator, dst.target, src.target)
