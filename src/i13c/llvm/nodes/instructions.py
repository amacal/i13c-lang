from typing import Dict

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
    if instruction.mnemonic.name == b"mov":
        return lower_instruction_mov(graph, generator, instruction, operands)

    elif instruction.mnemonic.name == b"shl":
        return lower_instruction_shl(graph, generator, instruction, operands)

    elif instruction.mnemonic.name == b"syscall":
        return lower_instruction_syscall(generator)

    assert False, f"unsupported mnemonic: {instruction.mnemonic.name}"


def lower_instruction_mov(
    graph: SemanticGraph,
    generator: Generator,
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
    graph: SemanticGraph,
    generator: Generator,
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


def lower_instruction_syscall(generator: Generator) -> InstructionEntry:
    return (InstructionId(value=generator.next()), SysCall())
