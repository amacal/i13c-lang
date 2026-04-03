from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.math import AddRegImm, AddRegReg
from i13c.llvm.typing.registers import name_to_reg64
from tests.encoding import samples


@samples(
    """
        | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
        | dst | imm32      | encoding             | *** | dst | imm32      | encoding             |
        | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
        | rax | 0x12345678 | 48 81 c0 78 56 34 12 | *** | r8  | 0x12345678 | 49 81 c0 78 56 34 12 |
        | rcx | 0x12345678 | 48 81 c1 78 56 34 12 | *** | r9  | 0x12345678 | 49 81 c1 78 56 34 12 |
        | rdx | 0x12345678 | 48 81 c2 78 56 34 12 | *** | r10 | 0x12345678 | 49 81 c2 78 56 34 12 |
        | rbx | 0x12345678 | 48 81 c3 78 56 34 12 | *** | r11 | 0x12345678 | 49 81 c3 78 56 34 12 |
        | rsp | 0x12345678 | 48 81 c4 78 56 34 12 | *** | r12 | 0x12345678 | 49 81 c4 78 56 34 12 |
        | rbp | 0x12345678 | 48 81 c5 78 56 34 12 | *** | r13 | 0x12345678 | 49 81 c5 78 56 34 12 |
        | rsi | 0x12345678 | 48 81 c6 78 56 34 12 | *** | r14 | 0x12345678 | 49 81 c6 78 56 34 12 |
        | rdi | 0x12345678 | 48 81 c7 78 56 34 12 | *** | r15 | 0x12345678 | 49 81 c7 78 56 34 12 |
        | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
    """
)
def can_encode_instructions_add_reg64_imm32(dst: str, imm32: int, encoding: bytes):
    flow: List[Instruction] = [
        AddRegImm(dst=name_to_reg64(dst), imm=imm32),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | --- | -------- | --- | --- | --- | -------- |
        | dst | src | encoding | *** | dst | src | encoding |
        | --- | --- | -------- | --- | --- | --- | -------- |
        | rax | rsp | 48 01 e0 | *** | r8  | r12 | 4d 01 e0 |
        | rcx | rbp | 48 01 e9 | *** | r9  | r13 | 4d 01 e9 |
        | rdx | rsi | 48 01 f2 | *** | r10 | r14 | 4d 01 f2 |
        | rbx | rdi | 48 01 fb | *** | r11 | r15 | 4d 01 fb |
        | rsp | r8  | 4c 01 c4 | *** | r12 | rax | 49 01 c4 |
        | rbp | r9  | 4c 01 cd | *** | r13 | rcx | 49 01 cd |
        | rsi | r10 | 4c 01 d6 | *** | r14 | rdx | 49 01 d6 |
        | rdi | r11 | 4c 01 df | *** | r15 | rbx | 49 01 df |
        | --- | --- | -------- | --- | --- | --- | -------- |
    """
)
def can_encode_instructions_add_reg64_reg64(dst: str, src: str, encoding: bytes):
    flow: List[Instruction] = [
        AddRegReg(dst=name_to_reg64(dst), src=name_to_reg64(src)),
    ]

    assert encode(flow) == encoding
