from typing import Dict, Protocol

from i13c.core.generator import Generator
from i13c.llvm.typing.instructions import (
    InstructionEntry,
    InstructionId,
    MovRegImm,
    MovRegReg,
    ShlRegImm,
    SysCall,
)
from i13c.llvm.typing.registers import IR_REGISTER_FORWARD
from i13c.semantic.model import SemanticGraph
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
    graph: SemanticGraph,
    generator: Generator,
    instruction: SemanticInstruction,
    operands: Dict[OperandId, Operand],
) -> InstructionEntry:

    if instruction.mnemonic.name in DISPATCH_TABLE:
        return DISPATCH_TABLE[instruction.mnemonic.name](
            generator, graph, instruction, operands
        )

    assert False, f"unsupported mnemonic: {instruction.mnemonic.name}"


def lower_instruction_mov(
    generator: Generator,
    graph: SemanticGraph,
    instruction: SemanticInstruction,
    operands: Dict[OperandId, Operand],
) -> InstructionEntry:

    # first try out rewritten operands
    dst = operands.get(instruction.operands[0])
    src = operands.get(instruction.operands[1])

    # fallback to original operands if not rewritten
    dst = dst or graph.basic.operands.get(instruction.operands[0])
    src = src or graph.basic.operands.get(instruction.operands[1])

    # destination operand must be a register for now
    assert isinstance(dst.target, Register)
    dst_reg = IR_REGISTER_FORWARD[dst.target.name]

    if isinstance(src.target, Immediate):
        return (
            InstructionId(value=generator.next()),
            MovRegImm(dst=dst_reg, imm=src.target.value),
        )

    if isinstance(src.target, Register):
        return (
            InstructionId(value=generator.next()),
            MovRegReg(dst=dst_reg, src=IR_REGISTER_FORWARD[src.target.name]),
        )

    # we forgot to handle something
    assert False


def lower_instruction_shl(
    generator: Generator,
    graph: SemanticGraph,
    instruction: SemanticInstruction,
    operands: Dict[OperandId, Operand],
) -> InstructionEntry:

    # first try out rewritten operands
    dst = operands.get(instruction.operands[0])
    src = operands.get(instruction.operands[1])

    # fallback to original operands if not rewritten
    dst = dst or graph.basic.operands.get(instruction.operands[0])
    src = src or graph.basic.operands.get(instruction.operands[1])

    assert isinstance(dst.target, Register)
    assert isinstance(src.target, Immediate)

    dst_reg = IR_REGISTER_FORWARD[dst.target.name]
    src_imm = src.target.value

    return (
        InstructionId(value=generator.next()),
        ShlRegImm(dst=dst_reg, imm=src_imm),
    )


def lower_instruction_syscall(
    generator: Generator,
    graph: SemanticGraph,
    instruction: SemanticInstruction,
    operands: Dict[OperandId, Operand],
) -> InstructionEntry:

    # syscall has no operands, so we can ignore them
    return (InstructionId(value=generator.next()), SysCall())


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        graph: SemanticGraph,
        instruction: SemanticInstruction,
        operands: Dict[OperandId, Operand],
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[bytes, InstructionHandler] = {
    b"mov": lower_instruction_mov,
    b"shl": lower_instruction_shl,
    b"syscall": lower_instruction_syscall,
}  # pyright: ignore[reportAssignmentType]
