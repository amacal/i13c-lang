from typing import Dict, Protocol, Type

from i13c import ir


def encode(unit: ir.Unit) -> bytes:
    bytecode = bytearray()

    for codeblock in unit.codeblocks:
        for instruction in codeblock.instructions:
            DISPATCH_TABLE[type(instruction)](instruction, bytecode)

    return bytes(bytecode)


def encode_mov_reg_imm(instruction: ir.MovRegImm, bytecode: bytearray) -> None:
    # REX.W + B8+rd io
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0xB8 | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(8, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, *imm])


def encode_shl_reg_imm(instruction: ir.ShlRegImm, bytecode: bytearray) -> None:
    # REX.W + C1 /4 ib
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0xC1
    modrm = 0xE0 | (4 << 3) | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(1, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, modrm, *imm])


def encode_syscall(instruction: ir.SysCall, bytecode: bytearray) -> None:
    bytecode.extend([0x0F, 0x05])


class Encoder(Protocol):
    def __call__(self, instruction: ir.Instruction, out: bytearray) -> None: ...


DISPATCH_TABLE: Dict[Type[ir.Instruction], Encoder] = {
    ir.MovRegImm: encode_mov_reg_imm,
    ir.ShlRegImm: encode_shl_reg_imm,
    ir.SysCall: encode_syscall,
}  # pyright: ignore[reportAssignmentType]
