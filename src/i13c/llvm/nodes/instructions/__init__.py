from typing import Dict, Protocol

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.nodes.instructions.addr import lower_instruction_lea
from i13c.llvm.nodes.instructions.bits import lower_instruction_bswap
from i13c.llvm.nodes.instructions.math import lower_instruction_add
from i13c.llvm.nodes.instructions.move import lower_instruction_mov
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.bits import ShlRegImm, ShlRegReg
from i13c.llvm.typing.instructions.jump import SysCall
from i13c.llvm.typing.registers import IR_REGISTER_FORWARD_64
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Immediate,
    Operand,
    OperandId,
    Register,
)


def lower_instruction(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    if instruction.mnemonic.name in DISPATCH_TABLE:
        return DISPATCH_TABLE[instruction.mnemonic.name](
            generator, operands, instruction, rewritten
        )

    assert False, f"unsupported mnemonic: {instruction.mnemonic.name}"


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

    assert isinstance(dst.target, Register)

    if isinstance(src.target, Immediate):
        dst_reg = IR_REGISTER_FORWARD_64[dst.target.name]
        src_imm = src.target.value

        return (
            InstructionId(value=generator.next()),
            ShlRegImm(dst=dst_reg, imm=src_imm),
        )

    if isinstance(src.target, Register):
        assert src.target.name == b"cl"

        return (
            InstructionId(value=generator.next()),
            ShlRegReg(dst=IR_REGISTER_FORWARD_64[dst.target.name]),
        )

    # we forgot to handle something
    assert False


def lower_instruction_syscall(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    # syscall has no operands, so we can ignore them
    return (InstructionId(value=generator.next()), SysCall())


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        operands: OneToOne[OperandId, Operand],
        instruction: SemanticInstruction,
        rewritten: Dict[OperandId, Operand],
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[bytes, InstructionHandler] = {
    b"add": lower_instruction_add,
    b"bswap": lower_instruction_bswap,
    b"lea": lower_instruction_lea,
    b"mov": lower_instruction_mov,
    b"shl": lower_instruction_shl,
    b"syscall": lower_instruction_syscall,
}  # pyright: ignore[reportAssignmentType]
