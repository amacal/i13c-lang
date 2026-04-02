from typing import List

from i13c.encoding import encode
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.move import MovRegImm
from i13c.llvm.typing.registers import name_to_reg64
from tests.encoding import samples

# @samples(
#     """
#         | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
#         | dst | imm32      | encoding             | *   | dst | imm32      | encoding             |
#         | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
#         | rax | 0x12345678 | 48 c7 c0 78 56 34 12 | *   | r8  | 0x12345678 | 49 c7 c0 78 56 34 12 |
#         | rcx | 0x12345678 | 48 c7 c1 78 56 34 12 | *   | r9  | 0x12345678 | 49 c7 c1 78 56 34 12 |
#         | rdx | 0x12345678 | 48 c7 c2 78 56 34 12 | *   | r10 | 0x12345678 | 49 c7 c2 78 56 34 12 |
#         | rbx | 0x12345678 | 48 c7 c3 78 56 34 12 | *   | r11 | 0x12345678 | 49 c7 c3 78 56 34 12 |
#         | rsp | 0x12345678 | 48 c7 c4 78 56 34 12 | *   | r12 | 0x12345678 | 49 c7 c4 78 56 34 12 |
#         | rbp | 0x12345678 | 48 c7 c5 78 56 34 12 | *   | r13 | 0x12345678 | 49 c7 c5 78 56 34 12 |
#         | rsi | 0x12345678 | 48 c7 c6 78 56 34 12 | *   | r14 | 0x12345678 | 49 c7 c6 78 56 34 12 |
#         | rdi | 0x12345678 | 48 c7 c7 78 56 34 12 | *   | r15 | 0x12345678 | 49 c7 c7 78 56 34 12 |
#         | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
#     """
# )
# def can_encode_instructions_mov_reg64_imm32(dst: str, imm32: int, encoding: bytes):
#     flow: List[Instruction] = [
#         MovRegImm(dst=name_to_reg64(dst), imm=imm32),
#     ]

#     assert encode(flow) == encoding


@samples(
    """
        | --- | ------------------ | ----------------------------- | --- | --- | ------------------ | ----------------------------- |
        | dst | imm64              | encoding                      | *   | dst | imm64              | encoding                      |
        | --- | ------------------ | ----------------------------- | --- | --- | ------------------ | ----------------------------- |
        | rax | 0x1234567890abcdef | 48 b8 ef cd ab 90 78 56 34 12 | *   | r8  | 0x1234567890abcdef | 49 b8 ef cd ab 90 78 56 34 12 |
        | rcx | 0x1234567890abcdef | 48 b9 ef cd ab 90 78 56 34 12 | *   | r9  | 0x1234567890abcdef | 49 b9 ef cd ab 90 78 56 34 12 |
        | rdx | 0x1234567890abcdef | 48 ba ef cd ab 90 78 56 34 12 | *   | r10 | 0x1234567890abcdef | 49 ba ef cd ab 90 78 56 34 12 |
        | rbx | 0x1234567890abcdef | 48 bb ef cd ab 90 78 56 34 12 | *   | r11 | 0x1234567890abcdef | 49 bb ef cd ab 90 78 56 34 12 |
        | rsp | 0x1234567890abcdef | 48 bc ef cd ab 90 78 56 34 12 | *   | r12 | 0x1234567890abcdef | 49 bc ef cd ab 90 78 56 34 12 |
        | rbp | 0x1234567890abcdef | 48 bd ef cd ab 90 78 56 34 12 | *   | r13 | 0x1234567890abcdef | 49 bd ef cd ab 90 78 56 34 12 |
        | rsi | 0x1234567890abcdef | 48 be ef cd ab 90 78 56 34 12 | *   | r14 | 0x1234567890abcdef | 49 be ef cd ab 90 78 56 34 12 |
        | rdi | 0x1234567890abcdef | 48 bf ef cd ab 90 78 56 34 12 | *   | r15 | 0x1234567890abcdef | 49 bf ef cd ab 90 78 56 34 12 |
        | --- | ------------------ | ----------------------------- | --- | --- | ------------------ | ----------------------------- |
    """
)
def can_encode_instructions_mov_reg64_imm64(dst: str, imm64: int, encoding: bytes):
    flow: List[Instruction] = [
        MovRegImm(dst=name_to_reg64(dst), imm=imm64),
    ]

    assert encode(flow) == encoding
