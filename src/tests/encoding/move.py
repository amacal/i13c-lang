from i13c.semantic.typing.analyses.llvm import MOV
from tests.encoding import (
    ImmediateInfo,
    RegisterInfo,
    encode_instruction,
    parse_address,
    samples,
)


@samples("""
    | ---- | ------------------ | ----------------------------- | --- | ---- | ------------------ | ----------------------------- |
    | dst  | imm                | encoding                      | *** | dst  | imm                | encoding                      |
    | ---- | ------------------ | ----------------------------- | --- | ---- | ------------------ | ----------------------------- |
    | rax  | 0x123456789abcdef0 | 48 b8 f0 de bc 9a 78 56 34 12 | *** | r8   | 0x123456789abcdef0 | 49 b8 f0 de bc 9a 78 56 34 12 |
    | rcx  | 0x0000000000000001 | 48 b9 01 00 00 00 00 00 00 00 | *** | r9   | 0x0000000000000001 | 49 b9 01 00 00 00 00 00 00 00 |
    | rdx  | 0xffffffffffffffff | 48 ba ff ff ff ff ff ff ff ff | *** | r10  | 0xffffffffffffffff | 49 ba ff ff ff ff ff ff ff ff |
    | eax  | 0x12345678         | b8 78 56 34 12                | *** | r8d  | 0x12345678         | 41 b8 78 56 34 12             |
    | ecx  | 0x00000001         | b9 01 00 00 00                | *** | r9d  | 0x00000001         | 41 b9 01 00 00 00             |
    | edx  | 0xffffffff         | ba ff ff ff ff                | *** | r10d | 0xffffffff         | 41 ba ff ff ff ff             |
    | ax   | 0x1234             | 66 b8 34 12                   | *** | r8w  | 0x1234             | 66 41 b8 34 12                |
    | cx   | 0x0001             | 66 b9 01 00                   | *** | r9w  | 0x0001             | 66 41 b9 01 00                |
    | dx   | 0xffff             | 66 ba ff ff                   | *** | r10w | 0xffff             | 66 41 ba ff ff                |
    | al   | 0x12               | b0 12                         | *** | r8b  | 0x12               | 41 b0 12                      |
    | cl   | 0x01               | b1 01                         | *** | r9b  | 0x01               | 41 b1 01                      |
    | dl   | 0xff               | b2 ff                         | *** | r10b | 0xff               | 41 b2 ff                      |
    | spl  | 0x12               | 40 b4 12                      | *** | ah   | 0x12               | b4 12                         |
    | bpl  | 0x01               | 40 b5 01                      | *** | ch   | 0x01               | b5 01                         |
    | sil  | 0xff               | 40 b6 ff                      | *** | dh   | 0xff               | b6 ff                         |
    | ---- | ------------------ | ----------------------------- | --- | ---- | ------------------ | ----------------------------- |
""")
def can_encode_mov_reg_imm(
    dst: str,
    imm: bytes,
    encoding: bytes,
):
    encode_instruction(
        MOV(
            operands=(
                RegisterInfo.auto(dst),
                ImmediateInfo.auto(imm),
            ),
        ),
        encoding,
    )


@samples("""
    | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
    | dst | imm        | encoding             | *** | dst | imm        | encoding             |
    | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
    | rax | 0x10       | 48 c7 c0 10 00 00 00 | *** | r8  | 0x10       | 49 c7 c0 10 00 00 00 |
    | rcx | 0x01       | 48 c7 c1 01 00 00 00 | *** | r9  | 0x01       | 49 c7 c1 01 00 00 00 |
    | rdx | 0x7f       | 48 c7 c2 7f 00 00 00 | *** | r10 | 0x7f       | 49 c7 c2 7f 00 00 00 |
    | rbx | 0x1234     | 48 c7 c3 34 12 00 00 | *** | r11 | 0x1234     | 49 c7 c3 34 12 00 00 |
    | rsp | 0x00123456 | 48 c7 c4 56 34 12 00 | *** | r12 | 0x00123456 | 49 c7 c4 56 34 12 00 |
    | rbp | 0x12345678 | 48 c7 c5 78 56 34 12 | *** | r13 | 0x12345678 | 49 c7 c5 78 56 34 12 |
    | rsi | 0x76543210 | 48 c7 c6 10 32 54 76 | *** | r14 | 0x76543210 | 49 c7 c6 10 32 54 76 |
    | rdi | 0x7fffffff | 48 c7 c7 ff ff ff 7f | *** | r15 | 0x7fffffff | 49 c7 c7 ff ff ff 7f |
    | --- | ---------- | -------------------- | --- | --- | ---------- | -------------------- |
""")
def can_encode_mov_reg_imm_odd(
    dst: str,
    imm: bytes,
    encoding: bytes,
):
    encode_instruction(
        MOV(
            operands=(
                RegisterInfo.auto(dst),
                ImmediateInfo.auto(imm),
            ),
        ),
        encoding,
    )


@samples("""
    | ---- | ---- | ----------- | --- | ---- | ---- | ----------- |
    | dst  | src  | encoding    | *** | dst  | src  | encoding    |
    | ---- | ---- | ----------- | --- | ---- | ---- | ----------- |
    | rax  | rbx  | 48 89 d8    | *** | r8   | rbx  | 49 89 d8    |
    | rax  | r11  | 4c 89 d8    | *** | r8   | r11  | 4d 89 d8    |
    | rcx  | rdx  | 48 89 d1    | *** | r9   | r10  | 4d 89 d1    |
    | eax  | ebx  | 89 d8       | *** | r8d  | ebx  | 41 89 d8    |
    | eax  | r11d | 44 89 d8    | *** | r8d  | r11d | 45 89 d8    |
    | ecx  | edx  | 89 d1       | *** | r9d  | r10d | 45 89 d1    |
    | ax   | bx   | 66 89 d8    | *** | r8w  | bx   | 66 41 89 d8 |
    | ax   | r11w | 66 44 89 d8 | *** | r8w  | r11w | 66 45 89 d8 |
    | cx   | dx   | 66 89 d1    | *** | r9w  | r10w | 66 45 89 d1 |
    | al   | bl   | 88 d8       | *** | r8b  | bl   | 41 88 d8    |
    | al   | r11b | 44 88 d8    | *** | r8b  | r11b | 45 88 d8    |
    | cl   | dl   | 88 d1       | *** | r9b  | r10b | 45 88 d1    |
    | spl  | dil  | 40 88 fc    | *** | ah   | ch   | 88 ec       |
    | bpl  | sil  | 40 88 f5    | *** | ch   | dh   | 88 f5       |
    | ---- | ---- | ----------- | --- | ---- | ---- | ----------- |
""")
def can_encode_mov_reg_reg(
    dst: str,
    src: str,
    encoding: bytes,
):
    encode_instruction(
        MOV(
            operands=(
                RegisterInfo.auto(dst),
                RegisterInfo.auto(src),
            ),
        ),
        encoding,
    )


@samples("""
    | ---- | ----- | ----- | ---------- | ---------- | ----------------------------------- |
    | base | scale | index | disp32     | imm32      | encoding                            |
    | ---- | ----- | ----- | ---------- | ---------- | ----------------------------------- |
    | rsi  |       |       |            | 0x00000000 | 48 c7 06 00 00 00 00                |
    | rsp  |       |       |            | 0x00000001 | 48 c7 04 24 01 00 00 00             |
    | rbp  |       |       |            | 0x00000002 | 48 c7 45 00 02 00 00 00             |
    | rdi  |       |       | 0x7f       | 0x00000003 | 48 c7 47 7f 03 00 00 00             |
    | rdi  |       |       | 0x00000080 | 0x00000004 | 48 c7 87 80 00 00 00 04 00 00 00    |
    | ---  | 0x01  | rdx   |            | 0x00000005 | 48 c7 04 15 00 00 00 00 05 00 00 00 |
    | rdi  | 0x04  | rbp   |            | 0x00000006 | 48 c7 04 af 06 00 00 00             |
    | rbp  | 0x08  | rbx   |            | 0x00000007 | 48 c7 44 dd 00 07 00 00 00          |
    | ---  |       |       | 0x12345678 | 0x00000008 | 48 c7 04 25 78 56 34 12 08 00 00 00 |
    | rip  |       |       | 0x00000000 | 0x00000009 | 48 c7 05 00 00 00 00 09 00 00 00    |
    | rsi  | 0x01  | rsp   |            | 0x00000010 | !! !! !! !! !! !! !! !!             |
    | r12  |       |       |            | 0x00000011 | 49 c7 04 24 11 00 00 00             |
    | r13  |       |       |            | 0x00000012 | 49 c7 45 00 12 00 00 00             |
    | rdi  |       |       | 0xffffff7f | 0x00000013 | 48 c7 87 7f ff ff ff 13 00 00 00    |
    | ---  | 0x08  | r8    |            | 0x00000014 | 4a c7 04 c5 00 00 00 00 14 00 00 00 |
    | r12  | 0x02  | r10   |            | 0x00000015 | 4b c7 04 54 15 00 00 00             |
    | r13  | 0x02  | r10   |            | 0x00000016 | 4b c7 44 55 00 16 00 00 00          |
    | rip  |       |       | 0x12345678 | 0x00000017 | 48 c7 05 78 56 34 12 17 00 00 00    |
    | rdi  | 0x01  | r12   |            | 0x00000018 | 4a c7 04 27 18 00 00 00             |
    | ---- | ----- | ----- | ---------- | ---------- | ----------------------------------- |
""")
def can_encode_mov_mem_imm(
    base: str | None,
    scale: int | None,
    index: str | None,
    disp32: bytes | None,
    imm32: bytes,
    encoding: bytes | None,
):
    encode_instruction(
        MOV(
            operands=(
                parse_address(base, scale, index, disp32),
                ImmediateInfo.auto(imm32),
            ),
        ),
        encoding,
    )


@samples("""
    | ---- | ----- | ----- | ---------- | ---- | -------------------------- |
    | base | scale | index | disp32     | src  | encoding                   |
    | ---- | ----- | ----- | ---------- | ---- | -------------------------- |
    | rsi  |       |       |            | rax  | 48 89 06                   |
    | rsp  |       |       |            | rcx  | 48 89 0c 24                |
    | rbp  |       |       |            | rdx  | 48 89 55 00                |
    | rdi  |       |       | 0x7f       | rbx  | 48 89 5f 7f                |
    | rdi  |       |       | 0x00000080 | r8   | 4c 89 87 80 00 00 00       |
    | ---  | 0x01  | rdx   |            | r9   | 4c 89 0c 15 00 00 00 00    |
    | rdi  | 0x04  | rbp   |            | r10  | 4c 89 14 af                |
    | rbp  | 0x08  | rbx   |            | r11  | 4c 89 5c dd 00             |
    | ---  |       |       | 0x12345678 | r12  | 4c 89 24 25 78 56 34 12    |
    | rip  |       |       | 0x00000000 | r13  | 4c 89 2d 00 00 00 00       |
    | rsi  | 0x01  | rsp   |            | rax  | !! !! !! !! !! !! !! !!    |
    | r12  |       |       |            | rax  | 49 89 04 24                |
    | r13  |       |       |            | r9   | 4d 89 4d 00                |
    | rdi  |       |       | 0xffffff7f | r10  | 4c 89 97 7f ff ff ff       |
    | ---  | 0x08  | r8    |            | r11  | 4e 89 1c c5 00 00 00 00    |
    | r12  | 0x02  | r10   |            | r14  | 4f 89 34 54                |
    | r13  | 0x02  | r10   |            | r15  | 4f 89 7c 55 00             |
    | rip  |       |       | 0x12345678 | r8   | 4c 89 05 78 56 34 12       |
    | rdi  | 0x01  | r12   |            | r9   | 4e 89 0c 27                |
    | ---- | ----- | ----- | ---------- | ---- | -------------------------- |
""")
def can_encode_mov_mem_reg(
    base: str | None,
    scale: int | None,
    index: str | None,
    disp32: bytes | None,
    src: str,
    encoding: bytes | None,
):
    encode_instruction(
        MOV(
            operands=(
                parse_address(base, scale, index, disp32),
                RegisterInfo.auto(src),
            ),
        ),
        encoding,
    )


@samples("""
    | ---- | ---- | ----- | ----- | ---------- | -------------------------- |
    | dst  | base | scale | index | disp32     | encoding                   |
    | ---- | ---- | ----- | ----- | ---------- | -------------------------- |
    | rax  | rsi  |       |       |            | 48 8b 06                   |
    | rcx  | rsp  |       |       |            | 48 8b 0c 24                |
    | rdx  | rbp  |       |       |            | 48 8b 55 00                |
    | rbx  | rdi  |       |       | 0x7f       | 48 8b 5f 7f                |
    | r8   | rdi  |       |       | 0x00000080 | 4c 8b 87 80 00 00 00       |
    | r9   | ---  | 0x01  | rdx   |            | 4c 8b 0c 15 00 00 00 00    |
    | r10  | rdi  | 0x04  | rbp   |            | 4c 8b 14 af                |
    | r11  | rbp  | 0x08  | rbx   |            | 4c 8b 5c dd 00             |
    | r12  | ---  |       |       | 0x12345678 | 4c 8b 24 25 78 56 34 12    |
    | r13  | rip  |       |       | 0x00000000 | 4c 8b 2d 00 00 00 00       |
    | rax  | rsi  | 0x01  | rsp   |            | !! !! !! !! !! !! !! !!    |
    | rax  | r12  |       |       |            | 49 8b 04 24                |
    | r9   | r13  |       |       |            | 4d 8b 4d 00                |
    | r10  | rdi  |       |       | 0xffffff7f | 4c 8b 97 7f ff ff ff       |
    | r11  | ---  | 0x08  | r8    |            | 4e 8b 1c c5 00 00 00 00    |
    | r14  | r12  | 0x02  | r10   |            | 4f 8b 34 54                |
    | r15  | r13  | 0x02  | r10   |            | 4f 8b 7c 55 00             |
    | r8   | rip  |       |       | 0x12345678 | 4c 8b 05 78 56 34 12       |
    | r9   | rdi  | 0x01  | r12   |            | 4e 8b 0c 27                |
    | ---- | ---- | ----- | ----- | ---------- | -------------------------- |
""")
def can_encode_mov_reg_mem(
    dst: str,
    base: str | None,
    scale: int | None,
    index: str | None,
    disp32: bytes | None,
    encoding: bytes | None,
):
    encode_instruction(
        MOV(
            operands=(
                RegisterInfo.auto(dst),
                parse_address(base, scale, index, disp32),
            ),
        ),
        encoding,
    )
