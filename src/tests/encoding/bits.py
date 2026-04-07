from i13c.llvm.typing.instructions import bits
from i13c.llvm.typing.instructions.core import Immediate, Register
from tests.encoding import encode_instruction, samples


@samples(
    """
        | --- | -------- | --- | ---- | -------- |
        | dst | encoding | *** | dst  | encoding |
        | --- | -------- | --- | ---- | -------- |
        | rax | 48 0f c8 | *** | r8   | 49 0f c8 |
        | rcx | 48 0f c9 | *** | r9   | 49 0f c9 |
        | rdx | 48 0f ca | *** | r10  | 49 0f ca |
        | rbx | 48 0f cb | *** | r11  | 49 0f cb |
        | esp | 0f cc    | *** | r12d | 41 0f cc |
        | ebp | 0f cd    | *** | r13d | 41 0f cd |
        | esi | 0f ce    | *** | r14d | 41 0f ce |
        | edi | 0f cf    | *** | r15d | 41 0f cf |
        | --- | -------- | --- | ---- | -------- |
    """
)
def can_encode_bswap(dst: str, encoding: bytes):
    encode_instruction(bits.BSWAP(dst=Register.auto(dst)), encoding)


@samples(
    """
        | --- | ---- | -------------- | --- | ---- | ---- | -------------- |
        | dst | imm8 | encoding       | *** | dst  | imm8 | encoding       |
        | --- | ---- | -------------- | --- | ---- | ---- | -------------- |
        | rbx | 0x00 | 48 c1 e3 00    | *** | r12  | 0x00 | 49 c1 e4 00    |
        | rax | 0x01 | 48 d1 e0       | *** | r8   | 0x01 | 49 d1 e0       |
        | rdi | 0x05 | 48 c1 e7 05    | *** | r15  | 0x05 | 49 c1 e7 05    |
        | ecx | 0x00 | c1 e1 00       | *** | r9d  | 0x00 | 41 c1 e1 00    |
        | edx | 0x01 | d1 e2          | *** | r8d  | 0x00 | 41 c1 e0 00    |
        | ebx | 0x05 | c1 e3 05       | *** | r10d | 0x05 | 41 c1 e2 05    |
        | ax  | 0x00 | 66 c1 e0 00    | *** | r8w  | 0x00 | 66 41 c1 e0 00 |
        | cx  | 0x01 | 66 d1 e1       | *** | r9w  | 0x01 | 66 41 d1 e1    |
        | dx  | 0x05 | 66 c1 e2 05    | *** | r10w | 0x05 | 66 41 c1 e2 05 |
        | al  | 0x00 | c0 e0 00       | *** | r8b  | 0x00 | 41 c0 e0 00    |
        | cl  | 0x01 | d0 e1          | *** | r9b  | 0x01 | 41 d0 e1       |
        | dl  | 0x05 | c0 e2 05       | *** | r10b | 0x05 | 41 c0 e2 05    |
        | spl | 0x00 | 40 c0 e4 00    | *** | ah   | 0x00 | c0 e4 00       |
        | bpl | 0x01 | 40 d0 e5       | *** | ch   | 0x01 | d0 e5          |
        | sil | 0x05 | 40 c0 e6 05    | *** | dh   | 0x05 | c0 e6 05       |
        | --- | ---- | -------------- | --- | ---- | ---- | -------------- |
    """
)
def can_encode_instructions_shl_imm8(dst: str, imm8: int, encoding: bytes):
    encode_instruction(
        bits.SHL(
            dst=Register.auto(dst),
            src=Immediate.imm8(imm8),
        ),
        encoding,
    )


@samples(
    """
        | --- | ----------- | --- | ---- | ----------- |
        | dst | encoding    | *** | dst  | encoding    |
        | --- | ----------- | --- | ---- | ----------- |
        | rbx | 48 d3 e3    | *** | r12  | 49 d3 e4    |
        | ecx | d3 e1       | *** | r9d  | 41 d3 e1    |
        | dx  | 66 d3 e2    | *** | r10w | 66 41 d3 e2 |
        | cl  | d2 e1       | *** | r9b  | 41 d2 e1    |
        | spl | 40 d2 e4    | *** | ah   | d2 e4       |
        | --- | ----------- | --- | ---- | ----------- |
"""
)
def can_encode_instructions_shl_cl(dst: str, encoding: bytes):
    encode_instruction(
        bits.SHL(
            dst=Register.auto(dst),
            src=Register.parse8("cl"),
        ),
        encoding,
    )
