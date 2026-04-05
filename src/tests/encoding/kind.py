from typing import Optional

from i13c.encoding import kind
from i13c.encoding.core import UnreachableEncodingError
from i13c.llvm.typing.instructions import core as llvm
from tests.encoding import samples


def format_modrm_reg(reg: kind.ModRegEncoding) -> str:
    data = [
        reg.rex_w,
        reg.rex_r,
        reg.modrm_reg,
    ]

    return bytearray(data).hex(" ")


def format_modrm_rm(rm: kind.ModRMEncoding) -> str:
    data = [
        rm.rex_x,
        rm.rex_b,
        rm.modrm_mod,
        rm.modrm_rm,
        rm.sib_scale,
        rm.sib_index,
        rm.sib_base,
        rm.disp_width,
        *rm.disp_value.to_bytes(4, byteorder="little", signed=True),
    ]

    return bytearray(data).hex(" ")


@samples(
    """
        | --- | -------- | --- | --- | -------- |
        | reg | encoding | *** | reg | encoding |
        | --- | -------- | --- | --- | -------- |
        | rax | 08 00 00 | *** | r8  | 08 04 00 |
        | rcx | 08 00 01 | *** | r9  | 08 04 01 |
        | rdx | 08 00 02 | *** | r10 | 08 04 02 |
        | rbx | 08 00 03 | *** | r11 | 08 04 03 |
        | rsp | 08 00 04 | *** | r12 | 08 04 04 |
        | rbp | 08 00 05 | *** | r13 | 08 04 05 |
        | rsi | 08 00 06 | *** | r14 | 08 04 06 |
        | rdi | 08 00 07 | *** | r15 | 08 04 07 |
        | --- | -------- | --- | --- | -------- |
    """
)
def can_encode_modrm_reg64(reg: str, encoding: bytes):
    reg64 = llvm.Register.parse64(reg)
    modrm_reg = kind.encode_modrm_reg(reg64)

    assert format_modrm_reg(modrm_reg) == encoding.hex(" ")


@samples(
    """
        | --- | -------- | --- | ---- | -------- |
        | reg | encoding | *** | reg  | encoding |
        | --- | -------- | --- | ---- | -------- |
        | eax | 00 00 00 | *** | r8d  | 00 04 00 |
        | ecx | 00 00 01 | *** | r9d  | 00 04 01 |
        | edx | 00 00 02 | *** | r10d | 00 04 02 |
        | ebx | 00 00 03 | *** | r11d | 00 04 03 |
        | esp | 00 00 04 | *** | r12d | 00 04 04 |
        | ebp | 00 00 05 | *** | r13d | 00 04 05 |
        | esi | 00 00 06 | *** | r14d | 00 04 06 |
        | edi | 00 00 07 | *** | r15d | 00 04 07 |
        | --- | -------- | --- | ---- | -------- |
    """
)
def can_encode_modrm_reg32(reg: str, encoding: bytes):
    reg32 = llvm.Register.parse32(reg)
    modrm_reg = kind.encode_modrm_reg(reg32)

    assert format_modrm_reg(modrm_reg) == encoding.hex(" ")


@samples(
    """
        | --- | ----------------------------------- | --- | --- | ----------------------------------- |
        | reg | encoding                            | *** | reg | encoding                            |
        | --- | ----------------------------------- | --- | --- | ----------------------------------- |
        | rax | 00 00 03 00 00 00 00 00 00 00 00 00 | *** | r8  | 00 01 03 00 00 00 00 00 00 00 00 00 |
        | rcx | 00 00 03 01 00 00 00 00 00 00 00 00 | *** | r9  | 00 01 03 01 00 00 00 00 00 00 00 00 |
        | rdx | 00 00 03 02 00 00 00 00 00 00 00 00 | *** | r10 | 00 01 03 02 00 00 00 00 00 00 00 00 |
        | rbx | 00 00 03 03 00 00 00 00 00 00 00 00 | *** | r11 | 00 01 03 03 00 00 00 00 00 00 00 00 |
        | rsp | 00 00 03 04 00 00 00 00 00 00 00 00 | *** | r12 | 00 01 03 04 00 00 00 00 00 00 00 00 |
        | rbp | 00 00 03 05 00 00 00 00 00 00 00 00 | *** | r13 | 00 01 03 05 00 00 00 00 00 00 00 00 |
        | rsi | 00 00 03 06 00 00 00 00 00 00 00 00 | *** | r14 | 00 01 03 06 00 00 00 00 00 00 00 00 |
        | rdi | 00 00 03 07 00 00 00 00 00 00 00 00 | *** | r15 | 00 01 03 07 00 00 00 00 00 00 00 00 |
        | --- | ----------------------------------- | --- | --- | ----------------------------------- |
    """
)
def can_encode_modrm_rm_reg64(reg: str, encoding: bytes):
    reg64 = llvm.Register.parse64(reg)
    modrm_rm = kind.encode_modrm_rm(reg64)

    assert format_modrm_rm(modrm_rm) == encoding.hex(" ")


@samples(
    """
        | --- | ----------------------------------- | --- | ---- | ----------------------------------- |
        | reg | encoding                            | *** | reg  | encoding                            |
        | --- | ----------------------------------- | --- | ---- | ----------------------------------- |
        | eax | 00 00 03 00 00 00 00 00 00 00 00 00 | *** | r8d  | 00 01 03 00 00 00 00 00 00 00 00 00 |
        | ecx | 00 00 03 01 00 00 00 00 00 00 00 00 | *** | r9d  | 00 01 03 01 00 00 00 00 00 00 00 00 |
        | edx | 00 00 03 02 00 00 00 00 00 00 00 00 | *** | r10d | 00 01 03 02 00 00 00 00 00 00 00 00 |
        | ebx | 00 00 03 03 00 00 00 00 00 00 00 00 | *** | r11d | 00 01 03 03 00 00 00 00 00 00 00 00 |
        | esp | 00 00 03 04 00 00 00 00 00 00 00 00 | *** | r12d | 00 01 03 04 00 00 00 00 00 00 00 00 |
        | ebp | 00 00 03 05 00 00 00 00 00 00 00 00 | *** | r13d | 00 01 03 05 00 00 00 00 00 00 00 00 |
        | esi | 00 00 03 06 00 00 00 00 00 00 00 00 | *** | r14d | 00 01 03 06 00 00 00 00 00 00 00 00 |
        | edi | 00 00 03 07 00 00 00 00 00 00 00 00 | *** | r15d | 00 01 03 07 00 00 00 00 00 00 00 00 |
        | --- | ----------------------------------- | --- | ---- | ----------------------------------- |
    """
)
def can_encode_modrm_rm_reg32(reg: str, encoding: bytes):
    reg32 = llvm.Register.parse32(reg)
    modrm_rm = kind.encode_modrm_rm(reg32)

    assert format_modrm_rm(modrm_rm) == encoding.hex(" ")


@samples(
    """
        | ---------- | ----------------------------------- | --- | ---------- | ----------------------------------- |
        | disp32     | encoding                            | *** | disp32     | encoding                            |
        | ---------- | ----------------------------------- | --- | ---------- | ----------------------------------- |
        | 0x00000000 | 00 00 00 05 00 00 00 04 00 00 00 00 | *** | 0x000f0000 | 00 00 00 05 00 00 00 04 00 00 0f 00 |
        | 0x000000f0 | 00 00 00 05 00 00 00 04 f0 00 00 00 | *** | 0x00f00000 | 00 00 00 05 00 00 00 04 00 00 f0 00 |
        | 0x00000f00 | 00 00 00 05 00 00 00 04 00 0f 00 00 | *** | 0x0f000000 | 00 00 00 05 00 00 00 04 00 00 00 0f |
        | 0x0000f000 | 00 00 00 05 00 00 00 04 00 f0 00 00 | *** | 0xf0000000 | 00 00 00 05 00 00 00 04 00 00 00 f0 |
        | ---------- | ----------------------------------- | --- | ---------- | ----------------------------------- |
    """
)
def can_encode_modrm_rm_rel64(disp32: int, encoding: bytes):
    rel64 = llvm.RelativeAddress(disp=llvm.Displacement.auto(disp32))
    modrm_rm = kind.encode_modrm_rm(rel64)

    assert format_modrm_rm(modrm_rm) == encoding.hex(" ")


@samples(
    """
        | ---------- | ----------------------------------- | --- | ---------- | ----------------------------------- |
        | disp32     | encoding                            | *** | disp32     | encoding                            |
        | ---------- | ----------------------------------- | --- | ---------- | ----------------------------------- |
        | 0x00000000 | 00 00 00 04 00 04 05 04 00 00 00 00 | *** | 0x000f0000 | 00 00 00 04 00 04 05 04 00 00 0f 00 |
        | 0x000000f0 | 00 00 00 04 00 04 05 04 f0 00 00 00 | *** | 0x00f00000 | 00 00 00 04 00 04 05 04 00 00 f0 00 |
        | 0x00000f00 | 00 00 00 04 00 04 05 04 00 0f 00 00 | *** | 0x0f000000 | 00 00 00 04 00 04 05 04 00 00 00 0f |
        | 0x0000f000 | 00 00 00 04 00 04 05 04 00 f0 00 00 | *** | 0xf0000000 | 00 00 00 04 00 04 05 04 00 00 00 f0 |
        | ---------- | ----------------------------------- | --- | ---------- | ----------------------------------- |
    """
)
def can_encode_modrm_rm_m64_disp32_only(disp32: int, encoding: bytes):
    modrm_rm = kind.encode_modrm_rm(
        llvm.ComputedAddress(
            base=llvm.Register.none(),
            scaler=llvm.Scaler.none(),
            disp=llvm.Displacement.auto(disp32),
        )
    )

    assert format_modrm_rm(modrm_rm) == encoding.hex(" ")


@samples(
    """
        | ---- | ----------------------------------- | --- | ---- | ----------------------------------- |
        | base | encoding                            | *** | base | encoding                            |
        | ---- | ----------------------------------- | --- | ---- | ----------------------------------- |
        | rax  | 00 00 00 00 00 00 00 00 00 00 00 00 | *** | r8   | 00 01 00 00 00 00 00 00 00 00 00 00 |
        | rcx  | 00 00 00 01 00 00 00 00 00 00 00 00 | *** | r9   | 00 01 00 01 00 00 00 00 00 00 00 00 |
        | rdx  | 00 00 00 02 00 00 00 00 00 00 00 00 | *** | r10  | 00 01 00 02 00 00 00 00 00 00 00 00 |
        | rbx  | 00 00 00 03 00 00 00 00 00 00 00 00 | *** | r11  | 00 01 00 03 00 00 00 00 00 00 00 00 |
        | rsp  | 00 00 00 04 00 04 04 00 00 00 00 00 | *** | r12  | 00 01 00 04 00 04 04 00 00 00 00 00 |
        | rbp  | 00 00 01 05 00 00 00 01 00 00 00 00 | *** | r13  | 00 01 01 05 00 00 00 01 00 00 00 00 |
        | rsi  | 00 00 00 06 00 00 00 00 00 00 00 00 | *** | r14  | 00 01 00 06 00 00 00 00 00 00 00 00 |
        | rdi  | 00 00 00 07 00 00 00 00 00 00 00 00 | *** | r15  | 00 01 00 07 00 00 00 00 00 00 00 00 |
        | ---- | ----------------------------------- | --- | ---- | ----------------------------------- |
    """
)
def can_encode_modrm_rm_m64_base_only(base: str, encoding: bytes):
    modrm_rm = kind.encode_modrm_rm(
        llvm.ComputedAddress(
            base=llvm.Register.parse64(base),
            scaler=llvm.Scaler.none(),
            disp=llvm.Displacement.none(),
        )
    )

    assert format_modrm_rm(modrm_rm) == encoding.hex(" ")


@samples(
    """
        | ----- | ----- | ----------------------------------- | --- | ----- | ----- | ----------------------------------- |
        | scale | index | encoding                            | *** | scale | index | encoding                            |
        | ----- | ----- | ----------------------------------- | --- | ----- | ----- | ----------------------------------- |
        | 0x01  | rax   | 00 00 00 04 00 00 05 04 00 00 00 00 | *** | 0x08  | r8    | 02 00 00 04 03 00 05 04 00 00 00 00 |
        | 0x02  | rcx   | 00 00 00 04 01 01 05 04 00 00 00 00 | *** | 0x04  | r9    | 02 00 00 04 02 01 05 04 00 00 00 00 |
        | 0x04  | rdx   | 00 00 00 04 02 02 05 04 00 00 00 00 | *** | 0x02  | r10   | 02 00 00 04 01 02 05 04 00 00 00 00 |
        | 0x08  | rbx   | 00 00 00 04 03 03 05 04 00 00 00 00 | *** | 0x01  | r11   | 02 00 00 04 00 03 05 04 00 00 00 00 |
        | 0x01  | rsp   | !! !! !! !! !! !! !! !! !! !! !! !! | *** | 0x08  | r12   | 02 00 00 04 03 04 05 04 00 00 00 00 |
        | 0x02  | rbp   | 00 00 00 04 01 05 05 04 00 00 00 00 | *** | 0x04  | r13   | 02 00 00 04 02 05 05 04 00 00 00 00 |
        | 0x04  | rsi   | 00 00 00 04 02 06 05 04 00 00 00 00 | *** | 0x02  | r14   | 02 00 00 04 01 06 05 04 00 00 00 00 |
        | 0x08  | rdi   | 00 00 00 04 03 07 05 04 00 00 00 00 | *** | 0x01  | r15   | 02 00 00 04 00 07 05 04 00 00 00 00 |
        | ----- | ----- | ----------------------------------- | --- | ----- | ----- | ----------------------------------- |
    """
)
def can_encode_modrm_rm_m64_index_only(
    scale: llvm.ScaleValue, index: str, encoding: Optional[bytes]
):
    addr = llvm.ComputedAddress(
        base=llvm.Register.none(),
        scaler=llvm.Scaler(scale=scale, index=llvm.Register.parse64(index)),
        disp=llvm.Displacement.none(),
    )

    try:
        modrm_rm = kind.encode_modrm_rm(addr)

        assert encoding is not None
        assert format_modrm_rm(modrm_rm) == encoding.hex(" ")
    except UnreachableEncodingError:
        assert encoding is None


@samples(
    """
        | ---- | ----- | ----- | ---------- | ----------------------------------- | --- | ---- | ----- | ----- | ---------- | ----------------------------------- |
        | base | scale | index | disp32     | encoding                            | *** | base | scale | index | disp32     | encoding                            |
        | ---- | ----- | ----- | ---------- | ----------------------------------- | --- | ---- | ----- | ----- | ---------- | ----------------------------------- |
        | r15  | 0x01  | rax   | 0x00000000 | 00 01 00 04 00 00 07 00 00 00 00 00 | *** | rdi  | 0x08  | r8    | 0xffffffff | 02 00 01 04 03 00 07 01 ff ff ff ff |
        | r14  | 0x02  | rcx   | 0x000000ff | 00 01 02 04 01 01 06 04 ff 00 00 00 | *** | rsi  | 0x04  | r9    | 0xffffff00 | 02 00 02 04 02 01 06 04 00 ff ff ff |
        | r13  | 0x04  | rdx   | 0x0000ff00 | 00 01 02 04 02 02 05 04 00 ff 00 00 | *** | rbp  | 0x02  | r10   | 0xffff0000 | 02 00 02 04 01 02 05 04 00 00 ff ff |
        | r12  | 0x08  | rbx   | 0x00ff0000 | 00 01 02 04 03 03 04 04 00 00 ff 00 | *** | rsp  | 0x01  | r11   | 0xff000000 | 02 00 02 04 00 03 04 04 00 00 00 ff |
        | r11  | 0x01  | rsp   | 0xff000000 | !! !! !! !! !! !! !! !! !! !! !! !! | *** | rbx  | 0x08  | r12   | 0x00ff0000 | 02 00 02 04 03 04 03 04 00 00 ff 00 |
        | r10  | 0x02  | rbp   | 0xffff0000 | 00 01 02 04 01 05 02 04 00 00 ff ff | *** | rdx  | 0x04  | r13   | 0x0000ff00 | 02 00 02 04 02 05 02 04 00 ff 00 00 |
        | r9   | 0x04  | rsi   | 0xffffff00 | 00 01 02 04 02 06 01 04 00 ff ff ff | *** | rcx  | 0x02  | r14   | 0x000000ff | 02 00 02 04 01 06 01 04 ff 00 00 00 |
        | r8   | 0x08  | rdi   | 0xffffffff | 00 01 01 04 03 07 00 01 ff ff ff ff | *** | rax  | 0x01  | r15   | 0x00000000 | 02 00 00 04 00 07 00 00 00 00 00 00 |
        | ---- | ----- | ----- | ---------- | ----------------------------------- | --- | ---- | ----- | ----- | ---------- | ----------------------------------- |
    """
)
def can_encode_modrm_rm_m64_all(
    scale: llvm.ScaleValue,
    index: str,
    base: str,
    disp32: int,
    encoding: Optional[bytes],
):
    addr = llvm.ComputedAddress(
        base=llvm.Register.parse64(base),
        scaler=llvm.Scaler(scale=scale, index=llvm.Register.parse64(index)),
        disp=llvm.Displacement.auto(disp32),
    )

    try:
        modrm_rm = kind.encode_modrm_rm(addr)

        assert encoding is not None
        assert format_modrm_rm(modrm_rm) == encoding.hex(" ")
    except UnreachableEncodingError:
        assert encoding is None
