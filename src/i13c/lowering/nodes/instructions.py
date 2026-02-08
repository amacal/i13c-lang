from typing import Dict

from i13c.lowering.nodes.registers import IR_REGISTER_MAP
from i13c.lowering.typing.instructions import Instruction, MovRegImm, ShlRegImm, SysCall
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.instructions import Instruction as SemanticInstruction
from i13c.semantic.typing.entities.operands import Immediate, Operand, OperandId, Register


def lower_instruction(
    graph: SemanticGraph,
    instruction: SemanticInstruction,
    operands: Dict[OperandId, Operand],
) -> Instruction:
    if instruction.mnemonic.name == b"mov":
        return lower_instruction_mov(graph, instruction, operands)

    elif instruction.mnemonic.name == b"shl":
        return lower_instruction_shl(graph, instruction, operands)

    elif instruction.mnemonic.name == b"syscall":
        return lower_instruction_syscall()

    assert False, f"unsupported mnemonic: {instruction.mnemonic.name}"


def lower_instruction_mov(
    graph: SemanticGraph,
    instruction: SemanticInstruction,
    operands: Dict[OperandId, Operand],
) -> Instruction:

    # first try out rewritten operands
    dst = operands.get(instruction.operands[0])
    src = operands.get(instruction.operands[1])

    # fallback to original operands if not rewritten
    dst = dst or graph.basic.operands.get(instruction.operands[0])
    src = src or graph.basic.operands.get(instruction.operands[1])

    assert isinstance(dst.target, Register)
    assert isinstance(src.target, Immediate)

    dst_reg = IR_REGISTER_MAP[dst.target.name]
    src_imm = src.target.value

    return MovRegImm(dst=dst_reg, imm=src_imm)


def lower_instruction_shl(
    graph: SemanticGraph,
    instruction: SemanticInstruction,
    operands: Dict[OperandId, Operand],
) -> Instruction:

    # first try out rewritten operands
    dst = operands.get(instruction.operands[0])
    src = operands.get(instruction.operands[1])

    # fallback to original operands if not rewritten
    dst = dst or graph.basic.operands.get(instruction.operands[0])
    src = src or graph.basic.operands.get(instruction.operands[1])

    assert isinstance(dst.target, Register)
    assert isinstance(src.target, Immediate)

    dst_reg = IR_REGISTER_MAP[dst.target.name]
    src_imm = src.target.value

    return ShlRegImm(dst=dst_reg, imm=src_imm)


def lower_instruction_syscall() -> Instruction:
    return SysCall()
