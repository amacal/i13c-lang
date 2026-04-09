from typing import Optional

from i13c.llvm.typing.instructions import bits
from i13c.llvm.typing.instructions.core import Immediate, Register, ScaleValue
from tests.encoding import encode_instruction, parse_address, samples


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
def can_encode_instructions_shl_imm8(dst: str, imm8: bytes, encoding: bytes):
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


@samples(
    """
        | ---- | ----- | ----- | ---------- | ---- | -------------------------- |
        | base | scale | index | disp32     | imm8 | encoding                   |
        | ---- | ----- | ----- | ---------- | ---- | -------------------------- |
        | rsi  |       |       |            | 0x00 | 48 c1 26 00                |
        | rsp  |       |       |            | 0x01 | 48 d1 24 24                |
        | rbp  |       |       |            | 0x02 | 48 c1 65 00 02             |
        | rdi  |       |       | 0x7f       | 0x03 | 48 c1 67 7f 03             |
        | rdi  |       |       | 0x00000080 | 0x04 | 48 c1 a7 80 00 00 00 04    |
        | ---  | 0x01  | rdx   |            | 0x05 | 48 c1 24 15 00 00 00 00 05 |
        | rdi  | 0x04  | rbp   |            | 0x06 | 48 c1 24 af 06             |
        | rbp  | 0x08  | rbx   |            | 0x07 | 48 c1 64 dd 00 07          |
        | ---  |       |       | 0x12345678 | 0x08 | 48 c1 24 25 78 56 34 12 08 |
        | rip  |       |       | 0x00000000 | 0x09 | 48 c1 25 00 00 00 00 09    |
        | rsi  | 0x01  | rsp   |            | 0x10 | !! !! !! !! !! !! !! !!    |
        | rsi  |       |       |            | 0x11 | 48 c1 26 11                |
        | r12  |       |       |            | 0x12 | 49 c1 24 24 12             |
        | r13  |       |       |            | 0x13 | 49 c1 65 00 13             |
        | rdi  |       |       | 0x00000080 | 0x14 | 48 c1 a7 80 00 00 00 14    |
        | rdi  |       |       | 0xffffff7f | 0x15 | 48 c1 a7 7f ff ff ff 15    |
        | ---  | 0x08  | r8    |            | 0x16 | 4a c1 24 c5 00 00 00 00 16 |
        | r12  | 0x02  | r10   |            | 0x17 | 4b c1 24 54 17             |
        | r13  | 0x02  | r10   |            | 0x18 | 4b c1 64 55 00 18          |
        | ---  |       |       | 0x12345678 | 0x19 | 48 c1 24 25 78 56 34 12 19 |
        | rip  |       |       | 0x12345678 | 0x1a | 48 c1 25 78 56 34 12 1a    |
        | rdi  | 0x01  | r12   |            | 0x1b | 4a c1 24 27 1b             |
        | ---- | ----- | ----- | ---------- | ---- | -------------------------- |
    """
)
def can_encode_shl_mem_imm8(
    base: Optional[str],
    scale: Optional[ScaleValue],
    index: Optional[str],
    disp32: Optional[bytes],
    imm8: bytes,
    encoding: Optional[bytes],
):
    encode_instruction(
        bits.SHL(
            dst=parse_address(base, scale, index, disp32),
            src=Immediate.imm8(imm8),
        ),
        encoding,
    )


@samples(
    """
        | ---- | ----- | ----- | ---------- | ----------------------- |
        | base | scale | index | disp32     | encoding                |
        | ---- | ----- | ----- | ---------- | ----------------------- |
        | rsi  |       |       |            | 48 d3 26                |
        | rsp  |       |       |            | 48 d3 24 24             |
        | rbp  |       |       |            | 48 d3 65 00             |
        | rdi  |       |       | 0x7f       | 48 d3 67 7f             |
        | rdi  |       |       | 0x00000080 | 48 d3 a7 80 00 00 00    |
        | ---  | 0x01  | rdx   |            | 48 d3 24 15 00 00 00 00 |
        | rdi  | 0x04  | rbp   |            | 48 d3 24 af             |
        | rbp  | 0x08  | rbx   |            | 48 d3 64 dd 00          |
        | ---  |       |       | 0x12345678 | 48 d3 24 25 78 56 34 12 |
        | rip  |       |       | 0x00000000 | 48 d3 25 00 00 00 00    |
        | rsi  | 0x01  | rsp   |            | !! !! !! !! !! !! !! !! |
        | rsi  |       |       |            | 48 d3 26                |
        | r12  |       |       |            | 49 d3 24 24             |
        | r13  |       |       |            | 49 d3 65 00             |
        | rdi  |       |       | 0x00000080 | 48 d3 a7 80 00 00 00    |
        | rdi  |       |       | 0xffffff7f | 48 d3 a7 7f ff ff ff    |
        | ---  | 0x08  | r8    |            | 4a d3 24 c5 00 00 00 00 |
        | r12  | 0x02  | r10   |            | 4b d3 24 54             |
        | r13  | 0x02  | r10   |            | 4b d3 64 55 00          |
        | ---  |       |       | 0x12345678 | 48 d3 24 25 78 56 34 12 |
        | rip  |       |       | 0x12345678 | 48 d3 25 78 56 34 12    |
        | rdi  | 0x01  | r12   |            | 4a d3 24 27             |
        | ---- | ----- | ----- | ---------- | ----------------------- |
    """
)
def can_encode_shl_mem_cl(
    base: Optional[str],
    scale: Optional[ScaleValue],
    index: Optional[str],
    disp32: Optional[bytes],
    encoding: Optional[bytes],
):
    encode_instruction(
        bits.SHL(
            dst=parse_address(base, scale, index, disp32),
            src=Register.parse8("cl"),
        ),
        encoding,
    )
