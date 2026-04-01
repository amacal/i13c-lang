from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.bits import (
    ByteSwapReg32,
    ByteSwapReg64,
    ShlReg8Imm8,
    ShlReg16Imm8,
    ShlReg32Imm8,
    ShlReg64Imm8,
)
from i13c.llvm.typing.registers import name_to_reg32, name_to_reg64
from tests.encoding import samples


@samples(
    """
        | ------- | -------- | --- | ------- | -------- |
        | operand | encoding | *   | operand | encoding |
        | ------- | -------- | --- | ------- | -------- |
        | rax     | 48 0f c8 | *   | r8      | 49 0f c8 |
        | rcx     | 48 0f c9 | *   | r9      | 49 0f c9 |
        | rdx     | 48 0f ca | *   | r10     | 49 0f ca |
        | rbx     | 48 0f cb | *   | r11     | 49 0f cb |
        | rsp     | 48 0f cc | *   | r12     | 49 0f cc |
        | rbp     | 48 0f cd | *   | r13     | 49 0f cd |
        | rsi     | 48 0f ce | *   | r14     | 49 0f ce |
        | rdi     | 48 0f cf | *   | r15     | 49 0f cf |
        | ------- | -------- | --- | ------- | -------- |
    """
)
def can_encode_instructions_bswap_reg64(operand: str, encoding: bytes):
    flow: List[Instruction] = [
        ByteSwapReg64(target=name_to_reg64(operand)),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | ------- | -------- | --- | ------- | -------- |
        | operand | encoding | *   | operand | encoding |
        | ------- | -------- | --- | ------- | -------- |
        | eax     | 0f c8    | *   | r8d     | 41 0f c8 |
        | ecx     | 0f c9    | *   | r9d     | 41 0f c9 |
        | edx     | 0f ca    | *   | r10d    | 41 0f ca |
        | ebx     | 0f cb    | *   | r11d    | 41 0f cb |
        | esp     | 0f cc    | *   | r12d    | 41 0f cc |
        | ebp     | 0f cd    | *   | r13d    | 41 0f cd |
        | esi     | 0f ce    | *   | r14d    | 41 0f ce |
        | edi     | 0f cf    | *   | r15d    | 41 0f cf |
        | ------- | -------- | --- | ------- | -------- |
    """
)
def can_encode_instructions_bswap_reg32(operand: str, encoding: bytes):
    flow: List[Instruction] = [
        ByteSwapReg32(target=name_to_reg32(operand)),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | --------- | ----------- | --- | --- | --------- | ----------- |
        | dst | immediate | encoding    | *   | dst | immediate | encoding    |
        | --- | --------- | ----------- | --- | --- | --------- | ----------- |
        | rax | 0x01      | 48 d1 e0    | *   | r8  | 0x01      | 49 d1 e0    |
        | rcx | 0x01      | 48 d1 e1    | *   | r9  | 0x01      | 49 d1 e1    |
        | rdx | 0x01      | 48 d1 e2    | *   | r10 | 0x01      | 49 d1 e2    |
        | rbx | 0x01      | 48 d1 e3    | *   | r11 | 0x01      | 49 d1 e3    |
        | rsp | 0x01      | 48 d1 e4    | *   | r12 | 0x01      | 49 d1 e4    |
        | rbp | 0x01      | 48 d1 e5    | *   | r13 | 0x01      | 49 d1 e5    |
        | rsi | 0x01      | 48 d1 e6    | *   | r14 | 0x01      | 49 d1 e6    |
        | rdi | 0x01      | 48 d1 e7    | *   | r15 | 0x01      | 49 d1 e7    |
        | --- | --------- | ----------- | --- | --- | --------- | ----------- |
        | rax | 0x05      | 48 c1 e0 05 | *   | r8  | 0x05      | 49 c1 e0 05 |
        | rcx | 0x05      | 48 c1 e1 05 | *   | r9  | 0x05      | 49 c1 e1 05 |
        | rdx | 0x05      | 48 c1 e2 05 | *   | r10 | 0x05      | 49 c1 e2 05 |
        | rbx | 0x05      | 48 c1 e3 05 | *   | r11 | 0x05      | 49 c1 e3 05 |
        | rsp | 0x05      | 48 c1 e4 05 | *   | r12 | 0x05      | 49 c1 e4 05 |
        | rbp | 0x05      | 48 c1 e5 05 | *   | r13 | 0x05      | 49 c1 e5 05 |
        | rsi | 0x05      | 48 c1 e6 05 | *   | r14 | 0x05      | 49 c1 e6 05 |
        | rdi | 0x05      | 48 c1 e7 05 | *   | r15 | 0x05      | 49 c1 e7 05 |
        | --- | --------- | ----------- | --- | --- | --------- | ----------- |
        """
)
def can_encode_instructions_shl_reg64_imm8(dst: str, immediate: int, encoding: bytes):
    flow: List[Instruction] = [
        ShlReg64Imm8(dst=name_to_reg64(dst), imm=immediate),
    ]

    assert encode(flow) == encoding


def can_encode_instructions_shl_ebx_imm8():
    flow: List[Instruction] = [
        ShlReg32Imm8(dst=3, imm=0x02),
    ]

    bytecode = encode(flow)
    expected = bytes([0xC1, 0xE3, 0x02])

    assert bytecode == expected


def can_encode_instructions_shl_bx_imm8():
    flow: List[Instruction] = [
        ShlReg16Imm8(dst=3, imm=0x02),
    ]

    bytecode = encode(flow)
    expected = bytes([0x66, 0xC1, 0xE3, 0x02])

    assert bytecode == expected


def can_encode_instructions_shl_bl_imm8():
    flow: List[Instruction] = [
        ShlReg8Imm8(dst=3, imm=0x02),
    ]

    bytecode = encode(flow)
    expected = bytes([0xC0, 0xE3, 0x02])

    assert bytecode == expected
