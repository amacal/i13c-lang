from typing import List
from i13c import ast, ir

# fmt: off
IR_REGISTER_MAP = {
    b"rax": 0, b"rbx": 1, b"rcx": 2, b"rdx": 3, b"rsi": 4, b"rdi": 5, b"rsp": 6, b"rbp": 7,
    b"r8": 8, b"r9": 9, b"r10": 10, b"r11": 11, b"r12": 12, b"r13": 13, b"r14": 14, b"r15": 15,
}

class UnknownMnemonic(Exception):
    def __init__(self, name: bytes) -> None:
        self.name = name

def lower(program: ast.Program) -> List[ir.Instruction]:
    instructions: List[ir.Instruction] = []

    for entry in program.instructions:
        instructions.append(lower_instruction(entry))

    return instructions


def lower_instruction(instruction: ast.Instruction) -> ir.Instruction:
    if instruction.mnemonic.name == b"mov":
        return lower_instruction_mov(instruction)

    elif instruction.mnemonic.name == b"syscall":
        return lower_instruction_syscall(instruction)

    raise UnknownMnemonic(instruction.mnemonic.name)


def lower_instruction_mov(instruction: ast.Instruction) -> ir.Instruction:
    dst = instruction.operands[0]
    src = instruction.operands[1]

    assert isinstance(dst, ast.Register)
    assert isinstance(src, ast.Immediate)

    dst_reg = IR_REGISTER_MAP[dst.name]
    src_imm = src.value

    return ir.MovRegImm(dst=dst_reg, imm=src_imm)


def lower_instruction_syscall(instruction: ast.Instruction) -> ir.Instruction:
    return ir.SysCall()
