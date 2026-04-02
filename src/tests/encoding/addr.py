from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.addr import LeaReg32Off, LeaReg64Off
from i13c.llvm.typing.registers import (
    name_to_reg64,
)
from tests.encoding import samples


@samples(
    """
        | --- | --- | ----------- | --- | --- | --- | ----------- |
        | dst | src | encoding    | *   | dst | src | encoding    |
        | --- | --- | ----------- | --- | --- | --- | ----------- |
        | rax | rsp | 48 8d 04 24 | *   | r8  | r12 | 4d 8d 04 24 |
        | rcx | rbp | 48 8d 4d 00 | *   | r9  | r13 | 4d 8d 4d 00 |
        | rdx | rsi | 48 8d 16    | *   | r10 | r14 | 4d 8d 16    |
        | rbx | rdi | 48 8d 1f    | *   | r11 | r15 | 4d 8d 1f    |
        | rsp | r8  | 49 8d 20    | *   | r12 | rax | 4c 8d 20    |
        | rbp | r9  | 49 8d 29    | *   | r13 | rcx | 4c 8d 29    |
        | rsi | r10 | 49 8d 32    | *   | r14 | rdx | 4c 8d 32    |
        | rdi | r11 | 49 8d 3b    | *   | r15 | rbx | 4c 8d 3b    |
        | --- | --- | ----------- | --- | --- | --- | ----------- |
    """
)
def can_encode_instructions_lea_reg64_disp0(dst: str, src: str, encoding: bytes):
    flow: List[Instruction] = [
        LeaReg64Off(dst=name_to_reg64(dst), src=name_to_reg64(src), off=0),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | --- | ----- | -------------- | --- | --- | --- | ----- | -------------- |
        | dst | src | disp8 | encoding       | *   | dst | src | disp8 | encoding       |
        | --- | --- | ----- | -------------- | --- | --- | --- | ----- | -------------- |
        | rax | rsp | 0x12  | 48 8d 44 24 12 | *   | r8  | r12 | 0x12  | 4d 8d 44 24 12 |
        | rcx | rbp | 0x12  | 48 8d 4d 12    | *   | r9  | r13 | 0x12  | 4d 8d 4d 12    |
        | rdx | rsi | 0x12  | 48 8d 56 12    | *   | r10 | r14 | 0x12  | 4d 8d 56 12    |
        | rbx | rdi | 0x12  | 48 8d 5f 12    | *   | r11 | r15 | 0x12  | 4d 8d 5f 12    |
        | rsp | r8  | 0x12  | 49 8d 60 12    | *   | r12 | rax | 0x12  | 4c 8d 60 12    |
        | rbp | r9  | 0x12  | 49 8d 69 12    | *   | r13 | rcx | 0x12  | 4c 8d 69 12    |
        | rsi | r10 | 0x12  | 49 8d 72 12    | *   | r14 | rdx | 0x12  | 4c 8d 72 12    |
        | rdi | r11 | 0x12  | 49 8d 7b 12    | *   | r15 | rbx | 0x12  | 4c 8d 7b 12    |
        | --- | --- | ----- | -------------- | --- | --- | --- | ----- | -------------- |
    """
)
def can_encode_instructions_lea_reg64_disp8(
    dst: str, src: str, disp8: int, encoding: bytes
):
    flow: List[Instruction] = [
        LeaReg64Off(dst=name_to_reg64(dst), src=name_to_reg64(src), off=disp8),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | --- | ---------- | ----------------------- | --- | --- | --- | ---------- | ----------------------- |
        | dst | src | disp32     | encoding                | *   | dst | src | disp32     | encoding                |
        | --- | --- | ---------- | ----------------------- | --- | --- | --- | ---------- | ----------------------- |
        | rax | rsp | 0x12345678 | 48 8d 84 24 78 56 34 12 | *   | r8  | r12 | 0x12345678 | 4d 8d 84 24 78 56 34 12 |
        | rcx | rbp | 0x12345678 | 48 8d 8d 78 56 34 12    | *   | r9  | r13 | 0x12345678 | 4d 8d 8d 78 56 34 12    |
        | rdx | rsi | 0x12345678 | 48 8d 96 78 56 34 12    | *   | r10 | r14 | 0x12345678 | 4d 8d 96 78 56 34 12    |
        | rbx | rdi | 0x12345678 | 48 8d 9f 78 56 34 12    | *   | r11 | r15 | 0x12345678 | 4d 8d 9f 78 56 34 12    |
        | rsp | r8  | 0x12345678 | 49 8d a0 78 56 34 12    | *   | r12 | rax | 0x12345678 | 4c 8d a0 78 56 34 12    |
        | rbp | r9  | 0x12345678 | 49 8d a9 78 56 34 12    | *   | r13 | rcx | 0x12345678 | 4c 8d a9 78 56 34 12    |
        | rsi | r10 | 0x12345678 | 49 8d b2 78 56 34 12    | *   | r14 | rdx | 0x12345678 | 4c 8d b2 78 56 34 12    |
        | rdi | r11 | 0x12345678 | 49 8d bb 78 56 34 12    | *   | r15 | rbx | 0x12345678 | 4c 8d bb 78 56 34 12    |
        | --- | --- | ---------- | ----------------------- | --- | --- | --- | ---------- | ----------------------- |
    """
)
def can_encode_instructions_lea_reg64_disp32(
    dst: str, src: str, disp32: int, encoding: bytes
):
    flow: List[Instruction] = [
        LeaReg64Off(dst=name_to_reg64(dst), src=name_to_reg64(src), off=disp32),
    ]

    assert encode(flow) == encoding


def can_encode_instructions_lea_ebx_off():
    flow: List[Instruction] = [
        LeaReg32Off(dst=3, src=3, off=0x12345678),
    ]

    bytecode = encode(flow)
    expected = bytes([0x8D, 0x9B, 0x78, 0x56, 0x34, 0x12])

    assert bytecode == expected
