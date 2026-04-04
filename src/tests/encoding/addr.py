from typing import List, Optional

from i13c.encoding import encode
from i13c.encoding.core import UnreachableEncodingError
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.addr import LeaReg32Mem, LeaReg64Mem
from i13c.llvm.typing.instructions.core import (
    Address,
    Displacement,
    Register,
    Scaler,
    ScaleValue,
)
from tests.encoding import samples


@samples(
    """
        | --- | ---- | ----------- | --- | --- | ---- | ----------- |
        | dst | base | encoding    | *** | dst | base | encoding    |
        | --- | ---- | ----------- | --- | --- | ---- | ----------- |
        | rax | rsp  | 48 8d 04 24 | *** | r8  | r12  | 4d 8d 04 24 |
        | rcx | rbp  | 48 8d 4d 00 | *** | r9  | r13  | 4d 8d 4d 00 |
        | rdx | rsi  | 48 8d 16    | *** | r10 | r14  | 4d 8d 16    |
        | rbx | rdi  | 48 8d 1f    | *** | r11 | r15  | 4d 8d 1f    |
        | rsp | r8   | 49 8d 20    | *** | r12 | rax  | 4c 8d 20    |
        | rbp | r9   | 49 8d 29    | *** | r13 | rcx  | 4c 8d 29    |
        | rsi | r10  | 49 8d 32    | *** | r14 | rdx  | 4c 8d 32    |
        | rdi | r11  | 49 8d 3b    | *** | r15 | rbx  | 4c 8d 3b    |
        | --- | ---- | ----------- | --- | --- | ---- | ----------- |
    """
)
def can_encode_instructions_lea_reg64_base_disp0(dst: str, base: str, encoding: bytes):
    flow: List[Instruction] = [
        LeaReg64Mem(
            dst=Register.parse64(dst),
            addr=Address(
                base=Register.parse64(base),
                disp=Displacement.none(),
                scaler=Scaler.none(),
            ),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | ----- | ----- | -------------- | --- | --- | ---- | ----- | ----- | -------------- |
        | dst | base | scale | index | encoding       | *** | dst | base | scale | index | encoding       |
        | --- | ---- | ----- | ----- | -------------- | --- | --- | ---- | ----- | ----- | -------------- |
        | rax | rsp  | 1     | rdx   | 48 8d 04 14    | *** | r8  | r12  | 1     | r10   | 4f 8d 04 14    |
        | rcx | rbp  | 1     | rbx   | 48 8d 4c 1d 00 | *** | r9  | r13  | 1     | r11   | 4f 8d 4c 1d 00 |
        | rdx | rsi  | 1     | rsp   | !! !! !! !!    | *** | r10 | r14  | 1     | r12   | !! !! !! !!    |
        | rbx | rdi  | 1     | rbp   | 48 8d 1c 2f    | *** | r11 | r15  | 1     | r13   | 4f 8d 1c 2f    |
        | rsp | r8   | 1     | rsi   | 49 8d 24 30    | *** | r12 | rax  | 1     | r14   | 4e 8d 24 30    |
        | rbp | r9   | 1     | rdi   | 49 8d 2c 39    | *** | r13 | rcx  | 1     | r15   | 4e 8d 2c 39    |
        | rsi | r10  | 1     | r8    | 4b 8d 34 02    | *** | r14 | rdx  | 1     | rax   | 4c 8d 34 02    |
        | rdi | r11  | 1     | r9    | 4b 8d 3c 0b    | *** | r15 | rbx  | 1     | rcx   | 4c 8d 3c 0b    |
        | --- | ---- | ----- | ----- | -------------- | --- | --- | ---- | ----- | ----- | -------------- |
        | rax | rsp  | 2     | rdx   | 48 8d 04 54    | *** | r8  | r12  | 2     | r10   | 4f 8d 04 54    |
        | rcx | rbp  | 2     | rbx   | 48 8d 4c 5d 00 | *** | r9  | r13  | 2     | r11   | 4f 8d 4c 5d 00 |
        | rdx | rsi  | 2     | rsp   | !! !! !! !!    | *** | r10 | r14  | 2     | r12   | !! !! !! !!    |
        | rbx | rdi  | 2     | rbp   | 48 8d 1c 6f    | *** | r11 | r15  | 2     | r13   | 4f 8d 1c 6f    |
        | rsp | r8   | 2     | rsi   | 49 8d 24 70    | *** | r12 | rax  | 2     | r14   | 4e 8d 24 70    |
        | rbp | r9   | 2     | rdi   | 49 8d 2c 79    | *** | r13 | rcx  | 2     | r15   | 4e 8d 2c 79    |
        | rsi | r10  | 2     | r8    | 4b 8d 34 42    | *** | r14 | rdx  | 2     | rax   | 4c 8d 34 42    |
        | rdi | r11  | 2     | r9    | 4b 8d 3c 4b    | *** | r15 | rbx  | 2     | rcx   | 4c 8d 3c 4b    |
        | --- | ---- | ----- | ----- | -------------- | --- | --- | ---- | ----- | ----- | -------------- |
        | rax | rsp  | 4     | rdx   | 48 8d 04 94    | *** | r8  | r12  | 4     | r10   | 4f 8d 04 94    |
        | rcx | rbp  | 4     | rbx   | 48 8d 4c 9d 00 | *** | r9  | r13  | 4     | r11   | 4f 8d 4c 9d 00 |
        | rdx | rsi  | 4     | rsp   | !! !! !! !!    | *** | r10 | r14  | 4     | r12   | !! !! !! !!    |
        | rbx | rdi  | 4     | rbp   | 48 8d 1c af    | *** | r11 | r15  | 4     | r13   | 4f 8d 1c af    |
        | rsp | r8   | 4     | rsi   | 49 8d 24 b0    | *** | r12 | rax  | 4     | r14   | 4e 8d 24 b0    |
        | rbp | r9   | 4     | rdi   | 49 8d 2c b9    | *** | r13 | rcx  | 4     | r15   | 4e 8d 2c b9    |
        | rsi | r10  | 4     | r8    | 4b 8d 34 82    | *** | r14 | rdx  | 4     | rax   | 4c 8d 34 82    |
        | rdi | r11  | 4     | r9    | 4b 8d 3c 8b    | *** | r15 | rbx  | 4     | rcx   | 4c 8d 3c 8b    |
        | --- | ---- | ----- | ----- | -------------- | --- | --- | ---- | ----- | ----- | -------------- |
        | rax | rsp  | 8     | rdx   | 48 8d 04 d4    | *** | r8  | r12  | 8     | r10   | 4f 8d 04 d4    |
        | rcx | rbp  | 8     | rbx   | 48 8d 4c dd 00 | *** | r9  | r13  | 8     | r11   | 4f 8d 4c dd 00 |
        | rdx | rsi  | 8     | rsp   | !! !! !! !!    | *** | r10 | r14  | 8     | r12   | !! !! !! !!    |
        | rbx | rdi  | 8     | rbp   | 48 8d 1c ef    | *** | r11 | r15  | 8     | r13   | 4f 8d 1c ef    |
        | rsp | r8   | 8     | rsi   | 49 8d 24 f0    | *** | r12 | rax  | 8     | r14   | 4e 8d 24 f0    |
        | rbp | r9   | 8     | rdi   | 49 8d 2c f9    | *** | r13 | rcx  | 8     | r15   | 4e 8d 2c f9    |
        | rsi | r10  | 8     | r8    | 4b 8d 34 c2    | *** | r14 | rdx  | 8     | rax   | 4c 8d 34 c2    |
        | rdi | r11  | 8     | r9    | 4b 8d 3c cb    | *** | r15 | rbx  | 8     | rcx   | 4c 8d 3c cb    |
        | --- | ---- | ----- | ----- | -------------- | --- | --- | ---- | ----- | ----- | -------------- |
    """
)
def can_encode_instructions_lea_reg64_base_index_disp0(
    dst: str, base: str, scale: ScaleValue, index: str, encoding: Optional[bytes]
):
    flow: List[Instruction] = [
        LeaReg64Mem(
            dst=Register.parse64(dst),
            addr=Address(
                base=Register.parse64(base),
                disp=Displacement.none(),
                scaler=Scaler(
                    scale=scale,
                    index=Register.parse64(index),
                ),
            ),
        ),
    ]

    try:
        assert encode(flow) == encoding
    except UnreachableEncodingError:
        assert encoding is None


@samples(
    """
        | --- | ---- | ----- | -------------- | --- | --- | ---- | ----- | -------------- |
        | dst | base | disp8 | encoding       | *** | dst | base | disp8 | encoding       |
        | --- | ---- | ----- | -------------- | --- | --- | ---- | ----- | -------------- |
        | rax | rsp  | 0x12  | 48 8d 44 24 12 | *** | r8  | r12  | 0x12  | 4d 8d 44 24 12 |
        | rcx | rbp  | 0x12  | 48 8d 4d 12    | *** | r9  | r13  | 0x12  | 4d 8d 4d 12    |
        | rdx | rsi  | 0x12  | 48 8d 56 12    | *** | r10 | r14  | 0x12  | 4d 8d 56 12    |
        | rbx | rdi  | 0x12  | 48 8d 5f 12    | *** | r11 | r15  | 0x12  | 4d 8d 5f 12    |
        | rsp | r8   | 0x12  | 49 8d 60 12    | *** | r12 | rax  | 0x12  | 4c 8d 60 12    |
        | rbp | r9   | 0x12  | 49 8d 69 12    | *** | r13 | rcx  | 0x12  | 4c 8d 69 12    |
        | rsi | r10  | 0x12  | 49 8d 72 12    | *** | r14 | rdx  | 0x12  | 4c 8d 72 12    |
        | rdi | r11  | 0x12  | 49 8d 7b 12    | *** | r15 | rbx  | 0x12  | 4c 8d 7b 12    |
        | --- | ---- | ----- | -------------- | --- | --- | ---- | ----- | -------------- |
    """
)
def can_encode_instructions_lea_reg64_base_disp8(
    dst: str, base: str, disp8: int, encoding: bytes
):
    flow: List[Instruction] = [
        LeaReg64Mem(
            dst=Register.parse64(dst),
            addr=Address(
                base=Register.parse64(base),
                disp=Displacement.auto(disp8),
                scaler=Scaler.none(),
            ),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | ---------- | ----------------------- | --- | --- | ---- | ---------- | ----------------------- |
        | dst | base | disp32     | encoding                | *** | dst | base | disp32     | encoding                |
        | --- | ---- | ---------- | ----------------------- | --- | --- | ---- | ---------- | ----------------------- |
        | rax | rsp  | 0x12345678 | 48 8d 84 24 78 56 34 12 | *** | r8  | r12  | 0x12345678 | 4d 8d 84 24 78 56 34 12 |
        | rcx | rbp  | 0x12345678 | 48 8d 8d 78 56 34 12    | *** | r9  | r13  | 0x12345678 | 4d 8d 8d 78 56 34 12    |
        | rdx | rsi  | 0x12345678 | 48 8d 96 78 56 34 12    | *** | r10 | r14  | 0x12345678 | 4d 8d 96 78 56 34 12    |
        | rbx | rdi  | 0x12345678 | 48 8d 9f 78 56 34 12    | *** | r11 | r15  | 0x12345678 | 4d 8d 9f 78 56 34 12    |
        | rsp | r8   | 0x12345678 | 49 8d a0 78 56 34 12    | *** | r12 | rax  | 0x12345678 | 4c 8d a0 78 56 34 12    |
        | rbp | r9   | 0x12345678 | 49 8d a9 78 56 34 12    | *** | r13 | rcx  | 0x12345678 | 4c 8d a9 78 56 34 12    |
        | rsi | r10  | 0x12345678 | 49 8d b2 78 56 34 12    | *** | r14 | rdx  | 0x12345678 | 4c 8d b2 78 56 34 12    |
        | rdi | r11  | 0x12345678 | 49 8d bb 78 56 34 12    | *** | r15 | rbx  | 0x12345678 | 4c 8d bb 78 56 34 12    |
        | --- | ---- | ---------- | ----------------------- | --- | --- | ---- | ---------- | ----------------------- |
    """
)
def can_encode_instructions_lea_reg64_base_disp32(
    dst: str, base: str, disp32: int, encoding: bytes
):
    flow: List[Instruction] = [
        LeaReg64Mem(
            dst=Register.parse64(dst),
            addr=Address(
                base=Register.parse64(base),
                disp=Displacement.auto(disp32),
                scaler=Scaler.none(),
            ),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | dst | base | encoding | *** | dst  | base | encoding    |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
        | eax | rsp  | 8d 04 24 | *** | r8d  | r12  | 45 8d 04 24 |
        | ecx | rbp  | 8d 4d 00 | *** | r9d  | r13  | 45 8d 4d 00 |
        | edx | rsi  | 8d 16    | *** | r10d | r14  | 45 8d 16    |
        | ebx | rdi  | 8d 1f    | *** | r11d | r15  | 45 8d 1f    |
        | esp | r8   | 41 8d 20 | *** | r12d | rax  | 44 8d 20    |
        | ebp | r9   | 41 8d 29 | *** | r13d | rcx  | 44 8d 29    |
        | esi | r10  | 41 8d 32 | *** | r14d | rdx  | 44 8d 32    |
        | edi | r11  | 41 8d 3b | *** | r15d | rbx  | 44 8d 3b    |
        | --- | ---- | -------- | --- | ---- | ---- | ----------- |
    """
)
def can_encode_instructions_lea_reg32_base_disp0(dst: str, base: str, encoding: bytes):
    flow: List[Instruction] = [
        LeaReg32Mem(
            dst=Register.parse32(dst),
            addr=Address(
                base=Register.parse64(base),
                disp=Displacement.none(),
                scaler=Scaler.none(),
            ),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | ----- | ----------- | --- | ---- | ---- | ----- | -------------- |
        | dst | base | disp8 | encoding    | *** | dst  | base | disp8 | encoding       |
        | --- | ---- | ----- | ----------- | --- | ---- | ---- | ----- | -------------- |
        | eax | rsp  | 0x12  | 8d 44 24 12 | *** | r8d  | r12  | 0x12  | 45 8d 44 24 12 |
        | ecx | rbp  | 0x12  | 8d 4d 12    | *** | r9d  | r13  | 0x12  | 45 8d 4d 12    |
        | edx | rsi  | 0x12  | 8d 56 12    | *** | r10d | r14  | 0x12  | 45 8d 56 12    |
        | ebx | rdi  | 0x12  | 8d 5f 12    | *** | r11d | r15  | 0x12  | 45 8d 5f 12    |
        | esp | r8   | 0x12  | 41 8d 60 12 | *** | r12d | rax  | 0x12  | 44 8d 60 12    |
        | ebp | r9   | 0x12  | 41 8d 69 12 | *** | r13d | rcx  | 0x12  | 44 8d 69 12    |
        | esi | r10  | 0x12  | 41 8d 72 12 | *** | r14d | rdx  | 0x12  | 44 8d 72 12    |
        | edi | r11  | 0x12  | 41 8d 7b 12 | *** | r15d | rbx  | 0x12  | 44 8d 7b 12    |
        | --- | ---- | ----- | ----------- | --- | ---- | ---- | ----- | -------------- |
    """
)
def can_encode_instructions_lea_reg32_base_disp8(
    dst: str, base: str, disp8: int, encoding: bytes
):
    flow: List[Instruction] = [
        LeaReg32Mem(
            dst=Register.parse32(dst),
            addr=Address(
                base=Register.parse64(base),
                disp=Displacement.auto(disp8),
                scaler=Scaler.none(),
            ),
        ),
    ]

    assert encode(flow) == encoding


@samples(
    """
        | --- | ---- | ---------- | -------------------- | --- | ---- | ---- | ---------- | ----------------------- |
        | dst | base | disp32     | encoding             | *** | dst  | base | disp32     | encoding                |
        | --- | ---- | ---------- | -------------------- | --- | ---- | ---- | ---------- | ----------------------- |
        | eax | rsp  | 0x12345678 | 8d 84 24 78 56 34 12 | *** | r8d  | r12  | 0x12345678 | 45 8d 84 24 78 56 34 12 |
        | ecx | rbp  | 0x12345678 | 8d 8d 78 56 34 12    | *** | r9d  | r13  | 0x12345678 | 45 8d 8d 78 56 34 12    |
        | edx | rsi  | 0x12345678 | 8d 96 78 56 34 12    | *** | r10d | r14  | 0x12345678 | 45 8d 96 78 56 34 12    |
        | ebx | rdi  | 0x12345678 | 8d 9f 78 56 34 12    | *** | r11d | r15  | 0x12345678 | 45 8d 9f 78 56 34 12    |
        | esp | r8   | 0x12345678 | 41 8d a0 78 56 34 12 | *** | r12d | rax  | 0x12345678 | 44 8d a0 78 56 34 12    |
        | ebp | r9   | 0x12345678 | 41 8d a9 78 56 34 12 | *** | r13d | rcx  | 0x12345678 | 44 8d a9 78 56 34 12    |
        | esi | r10  | 0x12345678 | 41 8d b2 78 56 34 12 | *** | r14d | rdx  | 0x12345678 | 44 8d b2 78 56 34 12    |
        | edi | r11  | 0x12345678 | 41 8d bb 78 56 34 12 | *** | r15d | rbx  | 0x12345678 | 44 8d bb 78 56 34 12    |
        | --- | ---- | ---------- | -------------------- | --- | ---- | ---- | ---------- | ----------------------- |
    """
)
def can_encode_instructions_lea_reg32_base_disp32(
    dst: str, base: str, disp32: int, encoding: bytes
):
    flow: List[Instruction] = [
        LeaReg32Mem(
            dst=Register.parse32(dst),
            addr=Address(
                base=Register.parse64(base),
                disp=Displacement.auto(disp32),
                scaler=Scaler.none(),
            ),
        ),
    ]

    assert encode(flow) == encoding
