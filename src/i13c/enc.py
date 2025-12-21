from typing import List, Dict, Callable, Type, TypeVar
from i13c import ir


def encode(instructions: List[ir.Instruction]) -> bytes:
    bytecode = bytearray()

    for instruction in instructions:
        DISPATCH_TABLE[type(instruction)](instruction, bytecode)

    return bytes(bytecode)


def encode_mov_reg_imm(instruction: ir.MovRegImm, bytecode: bytearray) -> None:
    # REX.W + B8+rd io
    rex = 0x40   | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0xB8 | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(8, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, *imm])


def encode_syscall(instruction: ir.SysCall, bytecode: bytearray) -> None:
    bytecode.extend([0x0F, 0x05])


Encoded = TypeVar("Encoded", bound=ir.Instruction)
Encoder = Callable[[Encoded, bytearray], None]

DISPATCH_TABLE: Dict[Type[ir.Instruction], Encoder] = {
    ir.MovRegImm: encode_mov_reg_imm,
    ir.SysCall: encode_syscall,
}
