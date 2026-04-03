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
from i13c.llvm.typing.instructions.core import Immediate, Register
from tests.encoding import samples


@samples(
    """
        | --- | -------- | --- | --- | -------- |
        | dst | encoding | *** | dst | encoding |
        | --- | -------- | --- | --- | -------- |
        | rax | 48 0f c8 | *** | r8  | 49 0f c8 |
        | rcx | 48 0f c9 | *** | r9  | 49 0f c9 |
        | rdx | 48 0f ca | *** | r10 | 49 0f ca |
        | rbx | 48 0f cb | *** | r11 | 49 0f cb |
        | rsp | 48 0f cc | *** | r12 | 49 0f cc |
        | rbp | 48 0f cd | *** | r13 | 49 0f cd |
        | rsi | 48 0f ce | *** | r14 | 49 0f ce |
        | rdi | 48 0f cf | *** | r15 | 49 0f cf |
        | --- | -------- | --- | --- | -------- |
    """
)
def can_encode_instructions_bswap_reg64(dst: str, encoding: bytes):
    flow: List[Instruction] = [
        ByteSwapReg64(dst=Register.parse64(dst)),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | -------- | --- | ---- | -------- |
        | dst | encoding | *** | dst  | encoding |
        | --- | -------- | --- | ---- | -------- |
        | eax | 0f c8    | *** | r8d  | 41 0f c8 |
        | ecx | 0f c9    | *** | r9d  | 41 0f c9 |
        | edx | 0f ca    | *** | r10d | 41 0f ca |
        | ebx | 0f cb    | *** | r11d | 41 0f cb |
        | esp | 0f cc    | *** | r12d | 41 0f cc |
        | ebp | 0f cd    | *** | r13d | 41 0f cd |
        | esi | 0f ce    | *** | r14d | 41 0f ce |
        | edi | 0f cf    | *** | r15d | 41 0f cf |
        | --- | -------- | --- | ---- | -------- |
    """
)
def can_encode_instructions_bswap_reg32(dst: str, encoding: bytes):
    flow: List[Instruction] = [
        ByteSwapReg32(dst=Register.parse32(dst)),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | ----------- | --- | --- | ---- | ----------- |
        | dst | imm8 | encoding    | *** | dst | imm8 | encoding    |
        | --- | ---- | ----------- | --- | --- | ---- | ----------- |
        | rax | 0x01 | 48 d1 e0    | *** | r8  | 0x01 | 49 d1 e0    |
        | rcx | 0x01 | 48 d1 e1    | *** | r9  | 0x01 | 49 d1 e1    |
        | rdx | 0x01 | 48 d1 e2    | *** | r10 | 0x01 | 49 d1 e2    |
        | rbx | 0x01 | 48 d1 e3    | *** | r11 | 0x01 | 49 d1 e3    |
        | rsp | 0x01 | 48 d1 e4    | *** | r12 | 0x01 | 49 d1 e4    |
        | rbp | 0x01 | 48 d1 e5    | *** | r13 | 0x01 | 49 d1 e5    |
        | rsi | 0x01 | 48 d1 e6    | *** | r14 | 0x01 | 49 d1 e6    |
        | rdi | 0x01 | 48 d1 e7    | *** | r15 | 0x01 | 49 d1 e7    |
        | --- | ---- | ----------- | --- | --- | ---- | ----------- |
        | rax | 0x05 | 48 c1 e0 05 | *** | r8  | 0x05 | 49 c1 e0 05 |
        | rcx | 0x05 | 48 c1 e1 05 | *** | r9  | 0x05 | 49 c1 e1 05 |
        | rdx | 0x05 | 48 c1 e2 05 | *** | r10 | 0x05 | 49 c1 e2 05 |
        | rbx | 0x05 | 48 c1 e3 05 | *** | r11 | 0x05 | 49 c1 e3 05 |
        | rsp | 0x05 | 48 c1 e4 05 | *** | r12 | 0x05 | 49 c1 e4 05 |
        | rbp | 0x05 | 48 c1 e5 05 | *** | r13 | 0x05 | 49 c1 e5 05 |
        | rsi | 0x05 | 48 c1 e6 05 | *** | r14 | 0x05 | 49 c1 e6 05 |
        | rdi | 0x05 | 48 c1 e7 05 | *** | r15 | 0x05 | 49 c1 e7 05 |
        | --- | ---- | ----------- | --- | --- | ---- | ----------- |
        """
)
def can_encode_instructions_shl_reg64_imm8(dst: str, imm8: int, encoding: bytes):
    flow: List[Instruction] = [
        ShlReg64Imm8(
            dst=Register.parse64(dst),
            imm=Immediate.imm8(imm8),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | dst | imm8 | encoding | *** | dst  | imm8 | encoding    |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | eax | 0x01 | d1 e0    | *** | r8d  | 0x01 | 41 d1 e0    |
        | ecx | 0x01 | d1 e1    | *** | r9d  | 0x01 | 41 d1 e1    |
        | edx | 0x01 | d1 e2    | *** | r10d | 0x01 | 41 d1 e2    |
        | ebx | 0x01 | d1 e3    | *** | r11d | 0x01 | 41 d1 e3    |
        | esp | 0x01 | d1 e4    | *** | r12d | 0x01 | 41 d1 e4    |
        | ebp | 0x01 | d1 e5    | *** | r13d | 0x01 | 41 d1 e5    |
        | esi | 0x01 | d1 e6    | *** | r14d | 0x01 | 41 d1 e6    |
        | edi | 0x01 | d1 e7    | *** | r15d | 0x01 | 41 d1 e7    |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | eax | 0x05 | c1 e0 05 | *** | r8d  | 0x05 | 41 c1 e0 05 |
        | ecx | 0x05 | c1 e1 05 | *** | r9d  | 0x05 | 41 c1 e1 05 |
        | edx | 0x05 | c1 e2 05 | *** | r10d | 0x05 | 41 c1 e2 05 |
        | ebx | 0x05 | c1 e3 05 | *** | r11d | 0x05 | 41 c1 e3 05 |
        | esp | 0x05 | c1 e4 05 | *** | r12d | 0x05 | 41 c1 e4 05 |
        | ebp | 0x05 | c1 e5 05 | *** | r13d | 0x05 | 41 c1 e5 05 |
        | esi | 0x05 | c1 e6 05 | *** | r14d | 0x05 | 41 c1 e6 05 |
        | edi | 0x05 | c1 e7 05 | *** | r15d | 0x05 | 41 c1 e7 05 |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
    """
)
def can_encode_instructions_shl_reg32_imm8(dst: str, imm8: int, encoding: bytes):
    flow: List[Instruction] = [
        ShlReg32Imm8(
            dst=Register.parse32(dst),
            imm=Immediate.imm8(imm8),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | ----------- | --- | ---- | ---- | -------------- |
        | dst | imm8 | encoding    | *** | dst  | imm8 | encoding       |
        | --- | ---- | ----------- | --- | ---- | ---- | -------------- |
        | ax  | 0x01 | 66 d1 e0    | *** | r8w  | 0x01 | 66 41 d1 e0    |
        | cx  | 0x01 | 66 d1 e1    | *** | r9w  | 0x01 | 66 41 d1 e1    |
        | dx  | 0x01 | 66 d1 e2    | *** | r10w | 0x01 | 66 41 d1 e2    |
        | bx  | 0x01 | 66 d1 e3    | *** | r11w | 0x01 | 66 41 d1 e3    |
        | sp  | 0x01 | 66 d1 e4    | *** | r12w | 0x01 | 66 41 d1 e4    |
        | bp  | 0x01 | 66 d1 e5    | *** | r13w | 0x01 | 66 41 d1 e5    |
        | si  | 0x01 | 66 d1 e6    | *** | r14w | 0x01 | 66 41 d1 e6    |
        | di  | 0x01 | 66 d1 e7    | *** | r15w | 0x01 | 66 41 d1 e7    |
        | --- | ---- | ----------- | --- | ---- | ---- | -------------- |
        | ax  | 0x05 | 66 c1 e0 05 | *** | r8w  | 0x05 | 66 41 c1 e0 05 |
        | cx  | 0x05 | 66 c1 e1 05 | *** | r9w  | 0x05 | 66 41 c1 e1 05 |
        | dx  | 0x05 | 66 c1 e2 05 | *** | r10w | 0x05 | 66 41 c1 e2 05 |
        | bx  | 0x05 | 66 c1 e3 05 | *** | r11w | 0x05 | 66 41 c1 e3 05 |
        | sp  | 0x05 | 66 c1 e4 05 | *** | r12w | 0x05 | 66 41 c1 e4 05 |
        | bp  | 0x05 | 66 c1 e5 05 | *** | r13w | 0x05 | 66 41 c1 e5 05 |
        | si  | 0x05 | 66 c1 e6 05 | *** | r14w | 0x05 | 66 41 c1 e6 05 |
        | di  | 0x05 | 66 c1 e7 05 | *** | r15w | 0x05 | 66 41 c1 e7 05 |
        | --- | ---- | ----------- | --- | ---- | ---- | -------------- |
    """
)
def can_encode_instructions_shl_reg16_imm8(dst: str, imm8: int, encoding: bytes):
    flow: List[Instruction] = [
        ShlReg16Imm8(
            dst=Register.parse16(dst),
            imm=Immediate.imm8(imm8),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | dst | imm8 | encoding | *** | dst  | imm8 | encoding    |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | al  | 0x01 | d0 e0    | *** | r8b  | 0x01 | 41 d0 e0    |
        | cl  | 0x01 | d0 e1    | *** | r9b  | 0x01 | 41 d0 e1    |
        | dl  | 0x01 | d0 e2    | *** | r10b | 0x01 | 41 d0 e2    |
        | bl  | 0x01 | d0 e3    | *** | r11b | 0x01 | 41 d0 e3    |
        | spl | 0x01 | d0 e4    | *** | r12b | 0x01 | 41 d0 e4    |
        | bpl | 0x01 | d0 e5    | *** | r13b | 0x01 | 41 d0 e5    |
        | sil | 0x01 | d0 e6    | *** | r14b | 0x01 | 41 d0 e6    |
        | dil | 0x01 | d0 e7    | *** | r15b | 0x01 | 41 d0 e7    |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | al  | 0x05 | c0 e0 05 | *** | r8b  | 0x05 | 41 c0 e0 05 |
        | cl  | 0x05 | c0 e1 05 | *** | r9b  | 0x05 | 41 c0 e1 05 |
        | dl  | 0x05 | c0 e2 05 | *** | r10b | 0x05 | 41 c0 e2 05 |
        | bl  | 0x05 | c0 e3 05 | *** | r11b | 0x05 | 41 c0 e3 05 |
        | spl | 0x05 | c0 e4 05 | *** | r12b | 0x05 | 41 c0 e4 05 |
        | bpl | 0x05 | c0 e5 05 | *** | r13b | 0x05 | 41 c0 e5 05 |
        | sil | 0x05 | c0 e6 05 | *** | r14b | 0x05 | 41 c0 e6 05 |
        | dil | 0x05 | c0 e7 05 | *** | r15b | 0x05 | 41 c0 e7 05 |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
    """
)
def can_encode_instructions_shl_reg8_imm8(dst: str, imm8: int, encoding: bytes):
    flow: List[Instruction] = [
        ShlReg8Imm8(
            dst=Register.parse8(dst),
            imm=Immediate.imm8(imm8),
        ),
    ]

    assert encode(flow) == encoding
