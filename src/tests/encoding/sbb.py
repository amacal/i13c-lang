from tests.encoding.core import encode, exhaust


def can_exhaust_sbb():
    exhaust(
        SBB_ADDR16_IMM16,
        SBB_ADDR16_IMM8,
        SBB_ADDR16_REG16,
        SBB_ADDR32_IMM32,
        SBB_ADDR32_IMM8,
        SBB_ADDR32_REG32,
        SBB_ADDR64_IMM32,
        SBB_ADDR64_IMM8,
        SBB_ADDR64_REG64,
        SBB_ADDR8_IMM8,
        SBB_ADDR8_REG8,
        SBB_REG16_ADDR16,
        SBB_REG16_IMM16,
        SBB_REG16_IMM8,
        SBB_REG16_REG16,
        SBB_REG32_ADDR32,
        SBB_REG32_IMM32,
        SBB_REG32_IMM8,
        SBB_REG32_REG32,
        SBB_REG64_ADDR64,
        SBB_REG64_IMM32,
        SBB_REG64_IMM8,
        SBB_REG64_REG64,
        SBB_REG8_ADDR8,
        SBB_REG8_IMM8,
        SBB_REG8_REG8,
    )


SBB_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | sbb rax, 0x01 | 48 83 d8 01 | *** | sbb rax, 0x00 | 48 83 d8 00 |
    | sbb rcx, 0x01 | 48 83 d9 01 | *** | sbb rax, 0x7f | 48 83 d8 7f |
    | sbb rdx, 0x01 | 48 83 da 01 | *** | sbb rax, 0x80 | 48 83 d8 80 |
    | sbb rbx, 0x01 | 48 83 db 01 | *** | sbb rax, 0xff | 48 83 d8 ff |
    | sbb rsp, 0x01 | 48 83 dc 01 | *** | sbb rcx, 0x7f | 48 83 d9 7f |
    | sbb rbp, 0x01 | 48 83 dd 01 | *** | sbb rdx, 0x80 | 48 83 da 80 |
    | sbb rsi, 0x01 | 48 83 de 01 | *** | sbb rbx, 0xff | 48 83 db ff |
    | sbb rdi, 0x01 | 48 83 df 01 | *** | sbb rsp, 0x00 | 48 83 dc 00 |
    | sbb r8, 0x01  | 49 83 d8 01 | *** | sbb rsi, 0x7f | 48 83 de 7f |
    | sbb r9, 0x01  | 49 83 d9 01 | *** | sbb rdi, 0x80 | 48 83 df 80 |
    | sbb r10, 0x01 | 49 83 da 01 | *** | sbb r8, 0xff  | 49 83 d8 ff |
    | sbb r11, 0x01 | 49 83 db 01 | *** | sbb r9, 0x00  | 49 83 d9 00 |
    | sbb r12, 0x01 | 49 83 dc 01 | *** | sbb r11, 0x7f | 49 83 db 7f |
    | sbb r13, 0x01 | 49 83 dd 01 | *** | sbb r12, 0x80 | 49 83 dc 80 |
    | sbb r14, 0x01 | 49 83 de 01 | *** | sbb r13, 0xff | 49 83 dd ff |
    | sbb r15, 0x01 | 49 83 df 01 | *** | sbb r14, 0x00 | 49 83 de 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_sbb_reg64_imm8():
    encode(SBB_REG64_IMM8)


SBB_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | sbb rax, 0x00000001 | 48 1d 01 00 00 00    | *** | sbb rax, 0x00007fff | 48 1d ff 7f 00 00    |
    | sbb rcx, 0x00000001 | 48 81 d9 01 00 00 00 | *** | sbb rax, 0x00008000 | 48 1d 00 80 00 00    |
    | sbb rdx, 0x00000001 | 48 81 da 01 00 00 00 | *** | sbb rax, 0x0000ffff | 48 1d ff ff 00 00    |
    | sbb rbx, 0x00000001 | 48 81 db 01 00 00 00 | *** | sbb rax, 0x00010000 | 48 1d 00 00 01 00    |
    | sbb rsp, 0x00000001 | 48 81 dc 01 00 00 00 | *** | sbb rax, 0x7fffffff | 48 1d ff ff ff 7f    |
    | sbb rbp, 0x00000001 | 48 81 dd 01 00 00 00 | *** | sbb rax, 0x80000000 | 48 1d 00 00 00 80    |
    | sbb rsi, 0x00000001 | 48 81 de 01 00 00 00 | *** | sbb rax, 0xffffffff | 48 1d ff ff ff ff    |
    | sbb rdi, 0x00000001 | 48 81 df 01 00 00 00 | *** | sbb rcx, 0x0000007f | 48 81 d9 7f 00 00 00 |
    | sbb r8, 0x00000001  | 49 81 d8 01 00 00 00 | *** | sbb rdx, 0x00000080 | 48 81 da 80 00 00 00 |
    | sbb r9, 0x00000001  | 49 81 d9 01 00 00 00 | *** | sbb rbx, 0x000000ff | 48 81 db ff 00 00 00 |
    | sbb r10, 0x00000001 | 49 81 da 01 00 00 00 | *** | sbb rsp, 0x00000100 | 48 81 dc 00 01 00 00 |
    | sbb r11, 0x00000001 | 49 81 db 01 00 00 00 | *** | sbb rbp, 0x00007fff | 48 81 dd ff 7f 00 00 |
    | sbb r12, 0x00000001 | 49 81 dc 01 00 00 00 | *** | sbb rsi, 0x00008000 | 48 81 de 00 80 00 00 |
    | sbb r13, 0x00000001 | 49 81 dd 01 00 00 00 | *** | sbb rdi, 0x0000ffff | 48 81 df ff ff 00 00 |
    | sbb r14, 0x00000001 | 49 81 de 01 00 00 00 | *** | sbb r8, 0x00010000  | 49 81 d8 00 00 01 00 |
    | sbb r15, 0x00000001 | 49 81 df 01 00 00 00 | *** | sbb r9, 0x7fffffff  | 49 81 d9 ff ff ff 7f |
    | sbb rax, 0x00000000 | 48 1d 00 00 00 00    | *** | sbb r10, 0x80000000 | 49 81 da 00 00 00 80 |
    | sbb rax, 0x0000007f | 48 1d 7f 00 00 00    | *** | sbb r11, 0xffffffff | 49 81 db ff ff ff ff |
    | sbb rax, 0x00000080 | 48 1d 80 00 00 00    | *** | sbb r12, 0x00000000 | 49 81 dc 00 00 00 00 |
    | sbb rax, 0x000000ff | 48 1d ff 00 00 00    | *** | sbb r14, 0x0000007f | 49 81 de 7f 00 00 00 |
    | sbb rax, 0x00000100 | 48 1d 00 01 00 00    | *** | sbb r15, 0x00000080 | 49 81 df 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_sbb_reg64_imm32():
    encode(SBB_REG64_IMM32)


SBB_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | sbb rax, rcx | 48 19 c8 | *** | sbb rax, r8  | 4c 19 c0 |
    | sbb rcx, rcx | 48 19 c9 | *** | sbb rax, r9  | 4c 19 c8 |
    | sbb rdx, rcx | 48 19 ca | *** | sbb rax, r10 | 4c 19 d0 |
    | sbb rbx, rcx | 48 19 cb | *** | sbb rax, r11 | 4c 19 d8 |
    | sbb rsp, rcx | 48 19 cc | *** | sbb rax, r12 | 4c 19 e0 |
    | sbb rbp, rcx | 48 19 cd | *** | sbb rax, r13 | 4c 19 e8 |
    | sbb rsi, rcx | 48 19 ce | *** | sbb rax, r14 | 4c 19 f0 |
    | sbb rdi, rcx | 48 19 cf | *** | sbb rax, r15 | 4c 19 f8 |
    | sbb r8, rcx  | 49 19 c8 | *** | sbb rcx, rdx | 48 19 d1 |
    | sbb r9, rcx  | 49 19 c9 | *** | sbb rdx, rbx | 48 19 da |
    | sbb r10, rcx | 49 19 ca | *** | sbb rbx, rsp | 48 19 e3 |
    | sbb r11, rcx | 49 19 cb | *** | sbb rsp, rbp | 48 19 ec |
    | sbb r12, rcx | 49 19 cc | *** | sbb rbp, rsi | 48 19 f5 |
    | sbb r13, rcx | 49 19 cd | *** | sbb rsi, rdi | 48 19 fe |
    | sbb r14, rcx | 49 19 ce | *** | sbb rdi, r8  | 4c 19 c7 |
    | sbb r15, rcx | 49 19 cf | *** | sbb r8, r9   | 4d 19 c8 |
    | sbb rax, rax | 48 19 c0 | *** | sbb r9, r10  | 4d 19 d1 |
    | sbb rax, rdx | 48 19 d0 | *** | sbb r10, r11 | 4d 19 da |
    | sbb rax, rbx | 48 19 d8 | *** | sbb r11, r12 | 4d 19 e3 |
    | sbb rax, rsp | 48 19 e0 | *** | sbb r12, r13 | 4d 19 ec |
    | sbb rax, rbp | 48 19 e8 | *** | sbb r13, r14 | 4d 19 f5 |
    | sbb rax, rsi | 48 19 f0 | *** | sbb r14, r15 | 4d 19 fe |
    | sbb rax, rdi | 48 19 f8 | *** | sbb r15, rax | 49 19 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_sbb_reg64_reg64():
    encode(SBB_REG64_REG64)


SBB_REG64_ADDR64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | sbb rax, qword [rcx]                        | 48 1b 01                |
    | sbb rcx, qword [rcx]                        | 48 1b 09                |
    | sbb rdx, qword [rcx]                        | 48 1b 11                |
    | sbb rbx, qword [rcx]                        | 48 1b 19                |
    | sbb rsp, qword [rcx]                        | 48 1b 21                |
    | sbb rbp, qword [rcx]                        | 48 1b 29                |
    | sbb rsi, qword [rcx]                        | 48 1b 31                |
    | sbb rdi, qword [rcx]                        | 48 1b 39                |
    | sbb r8, qword [rcx]                         | 4c 1b 01                |
    | sbb r9, qword [rcx]                         | 4c 1b 09                |
    | sbb r10, qword [rcx]                        | 4c 1b 11                |
    | sbb r11, qword [rcx]                        | 4c 1b 19                |
    | sbb r12, qword [rcx]                        | 4c 1b 21                |
    | sbb r13, qword [rcx]                        | 4c 1b 29                |
    | sbb r14, qword [rcx]                        | 4c 1b 31                |
    | sbb r15, qword [rcx]                        | 4c 1b 39                |
    | sbb rax, qword [rax]                        | 48 1b 00                |
    | sbb rax, qword [rdx]                        | 48 1b 02                |
    | sbb rax, qword [rbx]                        | 48 1b 03                |
    | sbb rax, qword [rsp]                        | 48 1b 04 24             |
    | sbb rax, qword [rbp]                        | 48 1b 45 00             |
    | sbb rax, qword [rsi]                        | 48 1b 06                |
    | sbb rax, qword [rdi]                        | 48 1b 07                |
    | sbb rax, qword [r8]                         | 49 1b 00                |
    | sbb rax, qword [r9]                         | 49 1b 01                |
    | sbb rax, qword [r10]                        | 49 1b 02                |
    | sbb rax, qword [r11]                        | 49 1b 03                |
    | sbb rax, qword [r12]                        | 49 1b 04 24             |
    | sbb rax, qword [r13]                        | 49 1b 45 00             |
    | sbb rax, qword [r14]                        | 49 1b 06                |
    | sbb rax, qword [r15]                        | 49 1b 07                |
    | sbb rax, qword [rax + 1 * rcx]              | 48 1b 04 08             |
    | sbb rax, qword [rcx + 1 * rcx]              | 48 1b 04 09             |
    | sbb rax, qword [rdx + 1 * rcx]              | 48 1b 04 0a             |
    | sbb rax, qword [rbx + 1 * rcx]              | 48 1b 04 0b             |
    | sbb rax, qword [rsp + 1 * rcx]              | 48 1b 04 0c             |
    | sbb rax, qword [rbp + 1 * rcx]              | 48 1b 44 0d 00          |
    | sbb rax, qword [rsi + 1 * rcx]              | 48 1b 04 0e             |
    | sbb rax, qword [rdi + 1 * rcx]              | 48 1b 04 0f             |
    | sbb rax, qword [r8 + 1 * rcx]               | 49 1b 04 08             |
    | sbb rax, qword [r9 + 1 * rcx]               | 49 1b 04 09             |
    | sbb rax, qword [r10 + 1 * rcx]              | 49 1b 04 0a             |
    | sbb rax, qword [r11 + 1 * rcx]              | 49 1b 04 0b             |
    | sbb rax, qword [r12 + 1 * rcx]              | 49 1b 04 0c             |
    | sbb rax, qword [r13 + 1 * rcx]              | 49 1b 44 0d 00          |
    | sbb rax, qword [r14 + 1 * rcx]              | 49 1b 04 0e             |
    | sbb rax, qword [r15 + 1 * rcx]              | 49 1b 04 0f             |
    | sbb rax, qword [rax + 1 * rax]              | 48 1b 04 00             |
    | sbb rax, qword [rax + 1 * rdx]              | 48 1b 04 10             |
    | sbb rax, qword [rax + 1 * rbx]              | 48 1b 04 18             |
    | sbb rax, qword [rax + 1 * rbp]              | 48 1b 04 28             |
    | sbb rax, qword [rax + 1 * rsi]              | 48 1b 04 30             |
    | sbb rax, qword [rax + 1 * rdi]              | 48 1b 04 38             |
    | sbb rax, qword [rax + 1 * r8]               | 4a 1b 04 00             |
    | sbb rax, qword [rax + 1 * r9]               | 4a 1b 04 08             |
    | sbb rax, qword [rax + 1 * r10]              | 4a 1b 04 10             |
    | sbb rax, qword [rax + 1 * r11]              | 4a 1b 04 18             |
    | sbb rax, qword [rax + 1 * r12]              | 4a 1b 04 20             |
    | sbb rax, qword [rax + 1 * r13]              | 4a 1b 04 28             |
    | sbb rax, qword [rax + 1 * r14]              | 4a 1b 04 30             |
    | sbb rax, qword [rax + 1 * r15]              | 4a 1b 04 38             |
    | sbb rax, qword [rax + 2 * rcx]              | 48 1b 04 48             |
    | sbb rax, qword [rax + 4 * rcx]              | 48 1b 04 88             |
    | sbb rax, qword [rax + 8 * rcx]              | 48 1b 04 c8             |
    | sbb rax, qword [r8 + 1 * r9]                | 4b 1b 04 08             |
    | sbb rax, qword [r8 + 2 * r9]                | 4b 1b 04 48             |
    | sbb rax, qword [r8 + 4 * r9]                | 4b 1b 04 88             |
    | sbb rax, qword [r8 + 8 * r9]                | 4b 1b 04 c8             |
    | sbb rax, qword [1 * rcx]                    | 48 1b 04 0d 00 00 00 00 |
    | sbb rax, qword [2 * rcx]                    | 48 1b 04 4d 00 00 00 00 |
    | sbb rax, qword [4 * rcx]                    | 48 1b 04 8d 00 00 00 00 |
    | sbb rax, qword [8 * rcx]                    | 48 1b 04 cd 00 00 00 00 |
    | sbb rax, qword [1 * r9]                     | 4a 1b 04 0d 00 00 00 00 |
    | sbb rax, qword [2 * r9]                     | 4a 1b 04 4d 00 00 00 00 |
    | sbb rax, qword [4 * r9]                     | 4a 1b 04 8d 00 00 00 00 |
    | sbb rax, qword [8 * r9]                     | 4a 1b 04 cd 00 00 00 00 |
    | sbb rax, qword [r13 + 8 * r12]              | 4b 1b 44 e5 00          |
    | sbb rax, qword [rsp + 4 * r15]              | 4a 1b 04 bc             |
    | sbb rax, qword [rax + 1 * rcx + 0x00]       | 48 1b 44 08 00          |
    | sbb rax, qword [rax + 1 * rcx - 0x00]       | 48 1b 44 08 00          |
    | sbb rax, qword [rax + 1 * rcx + 0x01]       | 48 1b 44 08 01          |
    | sbb rax, qword [rax + 1 * rcx - 0x01]       | 48 1b 44 08 ff          |
    | sbb rax, qword [rax + 1 * rcx + 0x00000001] | 48 1b 84 08 01 00 00 00 |
    | sbb rax, qword [rax + 1 * rcx - 0x00000001] | 48 1b 84 08 ff ff ff ff |
    | sbb rax, qword [rax + 1 * rcx + 0x7f]       | 48 1b 44 08 7f          |
    | sbb rax, qword [rax + 1 * rcx - 0x7f]       | 48 1b 44 08 81          |
    | sbb rax, qword [rax + 1 * rcx + 0x80]       | 48 1b 84 08 80 00 00 00 |
    | sbb rax, qword [rax + 1 * rcx - 0x80]       | 48 1b 44 08 80          |
    | sbb rax, qword [rax + 1 * rcx - 0x81]       | 48 1b 84 08 7f ff ff ff |
    | sbb rax, qword [rax + 1 * rcx + 0xff]       | 48 1b 84 08 ff 00 00 00 |
    | sbb rax, qword [rax + 1 * rcx - 0xff]       | 48 1b 84 08 01 ff ff ff |
    | sbb rax, qword [rax + 1 * rcx + 0x7fffffff] | 48 1b 84 08 ff ff ff 7f |
    | sbb rax, qword [rax + 1 * rcx - 0x7fffffff] | 48 1b 84 08 01 00 00 80 |
    | sbb rax, qword [rax + 1 * rcx - 0x80000000] | 48 1b 84 08 00 00 00 80 |
    | sbb rax, qword [r10 + 0x7f]                 | 49 1b 42 7f             |
    | sbb rax, qword [r10 + 0x80]                 | 49 1b 82 80 00 00 00    |
    | sbb rax, qword [r10 - 0x80]                 | 49 1b 42 80             |
    | sbb rax, qword [r10 - 0x81]                 | 49 1b 82 7f ff ff ff    |
    | sbb rcx, qword [rdx]                        | 48 1b 0a                |
    | sbb rdx, qword [rbx]                        | 48 1b 13                |
    | sbb rbx, qword [rsp]                        | 48 1b 1c 24             |
    | sbb rsp, qword [rbp]                        | 48 1b 65 00             |
    | sbb rbp, qword [rsi]                        | 48 1b 2e                |
    | sbb rsi, qword [rdi]                        | 48 1b 37                |
    | sbb rdi, qword [r8]                         | 49 1b 38                |
    | sbb r8, qword [r9]                          | 4d 1b 01                |
    | sbb r9, qword [r10]                         | 4d 1b 0a                |
    | sbb r10, qword [r11]                        | 4d 1b 13                |
    | sbb r11, qword [r12]                        | 4d 1b 1c 24             |
    | sbb r12, qword [r13]                        | 4d 1b 65 00             |
    | sbb r13, qword [r14]                        | 4d 1b 2e                |
    | sbb r14, qword [r15]                        | 4d 1b 37                |
    | sbb r15, qword [rax + 1 * rcx]              | 4c 1b 3c 08             |
    | sbb rcx, qword [rdx + 1 * rcx]              | 48 1b 0c 0a             |
    | sbb rdx, qword [rbx + 1 * rcx]              | 48 1b 14 0b             |
    | sbb rbx, qword [rsp + 1 * rcx]              | 48 1b 1c 0c             |
    | sbb rsp, qword [rbp + 1 * rcx]              | 48 1b 64 0d 00          |
    | sbb rbp, qword [rsi + 1 * rcx]              | 48 1b 2c 0e             |
    | sbb rsi, qword [rdi + 1 * rcx]              | 48 1b 34 0f             |
    | sbb rdi, qword [r8 + 1 * rcx]               | 49 1b 3c 08             |
    | sbb r8, qword [r9 + 1 * rcx]                | 4d 1b 04 09             |
    | sbb r9, qword [r10 + 1 * rcx]               | 4d 1b 0c 0a             |
    | sbb r10, qword [r11 + 1 * rcx]              | 4d 1b 14 0b             |
    | sbb r11, qword [r12 + 1 * rcx]              | 4d 1b 1c 0c             |
    | sbb r12, qword [r13 + 1 * rcx]              | 4d 1b 64 0d 00          |
    | sbb r13, qword [r14 + 1 * rcx]              | 4d 1b 2c 0e             |
    | sbb r14, qword [r15 + 1 * rcx]              | 4d 1b 34 0f             |
    | sbb r15, qword [rax + 1 * rax]              | 4c 1b 3c 00             |
    | sbb rcx, qword [rax + 1 * rbx]              | 48 1b 0c 18             |
    | sbb rdx, qword [rax + 1 * rbp]              | 48 1b 14 28             |
    | sbb rbx, qword [rax + 1 * rsi]              | 48 1b 1c 30             |
    | sbb rsp, qword [rax + 1 * rdi]              | 48 1b 24 38             |
    | sbb rbp, qword [rax + 1 * r8]               | 4a 1b 2c 00             |
    | sbb rsi, qword [rax + 1 * r9]               | 4a 1b 34 08             |
    | sbb rdi, qword [rax + 1 * r10]              | 4a 1b 3c 10             |
    | sbb r8, qword [rax + 1 * r11]               | 4e 1b 04 18             |
    | sbb r9, qword [rax + 1 * r12]               | 4e 1b 0c 20             |
    | sbb r10, qword [rax + 1 * r13]              | 4e 1b 14 28             |
    | sbb r11, qword [rax + 1 * r14]              | 4e 1b 1c 30             |
    | sbb r12, qword [rax + 1 * r15]              | 4e 1b 24 38             |
    | sbb r13, qword [rax + 2 * rcx]              | 4c 1b 2c 48             |
    | sbb r14, qword [rax + 4 * rcx]              | 4c 1b 34 88             |
    | sbb r15, qword [rax + 8 * rcx]              | 4c 1b 3c c8             |
    | sbb rcx, qword [r8 + 2 * r9]                | 4b 1b 0c 48             |
    | sbb rdx, qword [r8 + 4 * r9]                | 4b 1b 14 88             |
    | sbb rbx, qword [r8 + 8 * r9]                | 4b 1b 1c c8             |
    | sbb rsp, qword [1 * rcx]                    | 48 1b 24 0d 00 00 00 00 |
    | sbb rbp, qword [2 * rcx]                    | 48 1b 2c 4d 00 00 00 00 |
    | sbb rsi, qword [4 * rcx]                    | 48 1b 34 8d 00 00 00 00 |
    | sbb rdi, qword [8 * rcx]                    | 48 1b 3c cd 00 00 00 00 |
    | sbb r8, qword [1 * r9]                      | 4e 1b 04 0d 00 00 00 00 |
    | sbb r9, qword [2 * r9]                      | 4e 1b 0c 4d 00 00 00 00 |
    | sbb r10, qword [4 * r9]                     | 4e 1b 14 8d 00 00 00 00 |
    | sbb r11, qword [8 * r9]                     | 4e 1b 1c cd 00 00 00 00 |
    | sbb r12, qword [r13 + 8 * r12]              | 4f 1b 64 e5 00          |
    | sbb r13, qword [rsp + 4 * r15]              | 4e 1b 2c bc             |
    | sbb r14, qword [rax + 1 * rcx + 0x00]       | 4c 1b 74 08 00          |
    | sbb r15, qword [rax + 1 * rcx - 0x00]       | 4c 1b 7c 08 00          |
    | sbb rcx, qword [rax + 1 * rcx - 0x01]       | 48 1b 4c 08 ff          |
    | sbb rdx, qword [rax + 1 * rcx + 0x00000001] | 48 1b 94 08 01 00 00 00 |
    | sbb rbx, qword [rax + 1 * rcx - 0x00000001] | 48 1b 9c 08 ff ff ff ff |
    | sbb rsp, qword [rax + 1 * rcx + 0x7f]       | 48 1b 64 08 7f          |
    | sbb rbp, qword [rax + 1 * rcx - 0x7f]       | 48 1b 6c 08 81          |
    | sbb rsi, qword [rax + 1 * rcx + 0x80]       | 48 1b b4 08 80 00 00 00 |
    | sbb rdi, qword [rax + 1 * rcx - 0x80]       | 48 1b 7c 08 80          |
    | sbb r8, qword [rax + 1 * rcx - 0x81]        | 4c 1b 84 08 7f ff ff ff |
    | sbb r9, qword [rax + 1 * rcx + 0xff]        | 4c 1b 8c 08 ff 00 00 00 |
    | sbb r10, qword [rax + 1 * rcx - 0xff]       | 4c 1b 94 08 01 ff ff ff |
    | sbb r11, qword [rax + 1 * rcx + 0x7fffffff] | 4c 1b 9c 08 ff ff ff 7f |
    | sbb r12, qword [rax + 1 * rcx - 0x7fffffff] | 4c 1b a4 08 01 00 00 80 |
    | sbb r13, qword [rax + 1 * rcx - 0x80000000] | 4c 1b ac 08 00 00 00 80 |
    | sbb r14, qword [r10 + 0x7f]                 | 4d 1b 72 7f             |
    | sbb r15, qword [r10 + 0x80]                 | 4d 1b ba 80 00 00 00    |
    | sbb rcx, qword [r10 - 0x81]                 | 49 1b 8a 7f ff ff ff    |
    | sbb rdx, qword [rax]                        | 48 1b 10                |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_sbb_reg64_addr64():
    encode(SBB_REG64_ADDR64)


SBB_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sbb eax, 0x01  | 83 d8 01    | *** | sbb eax, 0x00  | 83 d8 00    |
    | sbb ecx, 0x01  | 83 d9 01    | *** | sbb eax, 0x7f  | 83 d8 7f    |
    | sbb edx, 0x01  | 83 da 01    | *** | sbb eax, 0x80  | 83 d8 80    |
    | sbb ebx, 0x01  | 83 db 01    | *** | sbb eax, 0xff  | 83 d8 ff    |
    | sbb esp, 0x01  | 83 dc 01    | *** | sbb ecx, 0x7f  | 83 d9 7f    |
    | sbb ebp, 0x01  | 83 dd 01    | *** | sbb edx, 0x80  | 83 da 80    |
    | sbb esi, 0x01  | 83 de 01    | *** | sbb ebx, 0xff  | 83 db ff    |
    | sbb edi, 0x01  | 83 df 01    | *** | sbb esp, 0x00  | 83 dc 00    |
    | sbb r8d, 0x01  | 41 83 d8 01 | *** | sbb esi, 0x7f  | 83 de 7f    |
    | sbb r9d, 0x01  | 41 83 d9 01 | *** | sbb edi, 0x80  | 83 df 80    |
    | sbb r10d, 0x01 | 41 83 da 01 | *** | sbb r8d, 0xff  | 41 83 d8 ff |
    | sbb r11d, 0x01 | 41 83 db 01 | *** | sbb r9d, 0x00  | 41 83 d9 00 |
    | sbb r12d, 0x01 | 41 83 dc 01 | *** | sbb r11d, 0x7f | 41 83 db 7f |
    | sbb r13d, 0x01 | 41 83 dd 01 | *** | sbb r12d, 0x80 | 41 83 dc 80 |
    | sbb r14d, 0x01 | 41 83 de 01 | *** | sbb r13d, 0xff | 41 83 dd ff |
    | sbb r15d, 0x01 | 41 83 df 01 | *** | sbb r14d, 0x00 | 41 83 de 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sbb_reg32_imm8():
    encode(SBB_REG32_IMM8)


SBB_REG32_IMM32 = """
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | instruction          | encoding             | *** | instruction          | encoding             |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | sbb eax, 0x00000001  | 1d 01 00 00 00       | *** | sbb eax, 0x00007fff  | 1d ff 7f 00 00       |
    | sbb ecx, 0x00000001  | 81 d9 01 00 00 00    | *** | sbb eax, 0x00008000  | 1d 00 80 00 00       |
    | sbb edx, 0x00000001  | 81 da 01 00 00 00    | *** | sbb eax, 0x0000ffff  | 1d ff ff 00 00       |
    | sbb ebx, 0x00000001  | 81 db 01 00 00 00    | *** | sbb eax, 0x00010000  | 1d 00 00 01 00       |
    | sbb esp, 0x00000001  | 81 dc 01 00 00 00    | *** | sbb eax, 0x7fffffff  | 1d ff ff ff 7f       |
    | sbb ebp, 0x00000001  | 81 dd 01 00 00 00    | *** | sbb eax, 0x80000000  | 1d 00 00 00 80       |
    | sbb esi, 0x00000001  | 81 de 01 00 00 00    | *** | sbb eax, 0xffffffff  | 1d ff ff ff ff       |
    | sbb edi, 0x00000001  | 81 df 01 00 00 00    | *** | sbb ecx, 0x0000007f  | 81 d9 7f 00 00 00    |
    | sbb r8d, 0x00000001  | 41 81 d8 01 00 00 00 | *** | sbb edx, 0x00000080  | 81 da 80 00 00 00    |
    | sbb r9d, 0x00000001  | 41 81 d9 01 00 00 00 | *** | sbb ebx, 0x000000ff  | 81 db ff 00 00 00    |
    | sbb r10d, 0x00000001 | 41 81 da 01 00 00 00 | *** | sbb esp, 0x00000100  | 81 dc 00 01 00 00    |
    | sbb r11d, 0x00000001 | 41 81 db 01 00 00 00 | *** | sbb ebp, 0x00007fff  | 81 dd ff 7f 00 00    |
    | sbb r12d, 0x00000001 | 41 81 dc 01 00 00 00 | *** | sbb esi, 0x00008000  | 81 de 00 80 00 00    |
    | sbb r13d, 0x00000001 | 41 81 dd 01 00 00 00 | *** | sbb edi, 0x0000ffff  | 81 df ff ff 00 00    |
    | sbb r14d, 0x00000001 | 41 81 de 01 00 00 00 | *** | sbb r8d, 0x00010000  | 41 81 d8 00 00 01 00 |
    | sbb r15d, 0x00000001 | 41 81 df 01 00 00 00 | *** | sbb r9d, 0x7fffffff  | 41 81 d9 ff ff ff 7f |
    | sbb eax, 0x00000000  | 1d 00 00 00 00       | *** | sbb r10d, 0x80000000 | 41 81 da 00 00 00 80 |
    | sbb eax, 0x0000007f  | 1d 7f 00 00 00       | *** | sbb r11d, 0xffffffff | 41 81 db ff ff ff ff |
    | sbb eax, 0x00000080  | 1d 80 00 00 00       | *** | sbb r12d, 0x00000000 | 41 81 dc 00 00 00 00 |
    | sbb eax, 0x000000ff  | 1d ff 00 00 00       | *** | sbb r14d, 0x0000007f | 41 81 de 7f 00 00 00 |
    | sbb eax, 0x00000100  | 1d 00 01 00 00       | *** | sbb r15d, 0x00000080 | 41 81 df 80 00 00 00 |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
"""


def can_encode_sbb_reg32_imm32():
    encode(SBB_REG32_IMM32)


SBB_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | sbb eax, ecx   | 19 c8    | *** | sbb eax, r8d   | 44 19 c0 |
    | sbb ecx, ecx   | 19 c9    | *** | sbb eax, r9d   | 44 19 c8 |
    | sbb edx, ecx   | 19 ca    | *** | sbb eax, r10d  | 44 19 d0 |
    | sbb ebx, ecx   | 19 cb    | *** | sbb eax, r11d  | 44 19 d8 |
    | sbb esp, ecx   | 19 cc    | *** | sbb eax, r12d  | 44 19 e0 |
    | sbb ebp, ecx   | 19 cd    | *** | sbb eax, r13d  | 44 19 e8 |
    | sbb esi, ecx   | 19 ce    | *** | sbb eax, r14d  | 44 19 f0 |
    | sbb edi, ecx   | 19 cf    | *** | sbb eax, r15d  | 44 19 f8 |
    | sbb r8d, ecx   | 41 19 c8 | *** | sbb ecx, edx   | 19 d1    |
    | sbb r9d, ecx   | 41 19 c9 | *** | sbb edx, ebx   | 19 da    |
    | sbb r10d, ecx  | 41 19 ca | *** | sbb ebx, esp   | 19 e3    |
    | sbb r11d, ecx  | 41 19 cb | *** | sbb esp, ebp   | 19 ec    |
    | sbb r12d, ecx  | 41 19 cc | *** | sbb ebp, esi   | 19 f5    |
    | sbb r13d, ecx  | 41 19 cd | *** | sbb esi, edi   | 19 fe    |
    | sbb r14d, ecx  | 41 19 ce | *** | sbb edi, r8d   | 44 19 c7 |
    | sbb r15d, ecx  | 41 19 cf | *** | sbb r8d, r9d   | 45 19 c8 |
    | sbb eax, eax   | 19 c0    | *** | sbb r9d, r10d  | 45 19 d1 |
    | sbb eax, edx   | 19 d0    | *** | sbb r10d, r11d | 45 19 da |
    | sbb eax, ebx   | 19 d8    | *** | sbb r11d, r12d | 45 19 e3 |
    | sbb eax, esp   | 19 e0    | *** | sbb r12d, r13d | 45 19 ec |
    | sbb eax, ebp   | 19 e8    | *** | sbb r13d, r14d | 45 19 f5 |
    | sbb eax, esi   | 19 f0    | *** | sbb r14d, r15d | 45 19 fe |
    | sbb eax, edi   | 19 f8    | *** | sbb r15d, eax  | 41 19 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_sbb_reg32_reg32():
    encode(SBB_REG32_REG32)


SBB_REG32_ADDR32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | sbb eax, dword [rcx]                         | 1b 01                   |
    | sbb ecx, dword [rcx]                         | 1b 09                   |
    | sbb edx, dword [rcx]                         | 1b 11                   |
    | sbb ebx, dword [rcx]                         | 1b 19                   |
    | sbb esp, dword [rcx]                         | 1b 21                   |
    | sbb ebp, dword [rcx]                         | 1b 29                   |
    | sbb esi, dword [rcx]                         | 1b 31                   |
    | sbb edi, dword [rcx]                         | 1b 39                   |
    | sbb r8d, dword [rcx]                         | 44 1b 01                |
    | sbb r9d, dword [rcx]                         | 44 1b 09                |
    | sbb r10d, dword [rcx]                        | 44 1b 11                |
    | sbb r11d, dword [rcx]                        | 44 1b 19                |
    | sbb r12d, dword [rcx]                        | 44 1b 21                |
    | sbb r13d, dword [rcx]                        | 44 1b 29                |
    | sbb r14d, dword [rcx]                        | 44 1b 31                |
    | sbb r15d, dword [rcx]                        | 44 1b 39                |
    | sbb eax, dword [rax]                         | 1b 00                   |
    | sbb eax, dword [rdx]                         | 1b 02                   |
    | sbb eax, dword [rbx]                         | 1b 03                   |
    | sbb eax, dword [rsp]                         | 1b 04 24                |
    | sbb eax, dword [rbp]                         | 1b 45 00                |
    | sbb eax, dword [rsi]                         | 1b 06                   |
    | sbb eax, dword [rdi]                         | 1b 07                   |
    | sbb eax, dword [r8]                          | 41 1b 00                |
    | sbb eax, dword [r9]                          | 41 1b 01                |
    | sbb eax, dword [r10]                         | 41 1b 02                |
    | sbb eax, dword [r11]                         | 41 1b 03                |
    | sbb eax, dword [r12]                         | 41 1b 04 24             |
    | sbb eax, dword [r13]                         | 41 1b 45 00             |
    | sbb eax, dword [r14]                         | 41 1b 06                |
    | sbb eax, dword [r15]                         | 41 1b 07                |
    | sbb eax, dword [rax + 1 * rcx]               | 1b 04 08                |
    | sbb eax, dword [rcx + 1 * rcx]               | 1b 04 09                |
    | sbb eax, dword [rdx + 1 * rcx]               | 1b 04 0a                |
    | sbb eax, dword [rbx + 1 * rcx]               | 1b 04 0b                |
    | sbb eax, dword [rsp + 1 * rcx]               | 1b 04 0c                |
    | sbb eax, dword [rbp + 1 * rcx]               | 1b 44 0d 00             |
    | sbb eax, dword [rsi + 1 * rcx]               | 1b 04 0e                |
    | sbb eax, dword [rdi + 1 * rcx]               | 1b 04 0f                |
    | sbb eax, dword [r8 + 1 * rcx]                | 41 1b 04 08             |
    | sbb eax, dword [r9 + 1 * rcx]                | 41 1b 04 09             |
    | sbb eax, dword [r10 + 1 * rcx]               | 41 1b 04 0a             |
    | sbb eax, dword [r11 + 1 * rcx]               | 41 1b 04 0b             |
    | sbb eax, dword [r12 + 1 * rcx]               | 41 1b 04 0c             |
    | sbb eax, dword [r13 + 1 * rcx]               | 41 1b 44 0d 00          |
    | sbb eax, dword [r14 + 1 * rcx]               | 41 1b 04 0e             |
    | sbb eax, dword [r15 + 1 * rcx]               | 41 1b 04 0f             |
    | sbb eax, dword [rax + 1 * rax]               | 1b 04 00                |
    | sbb eax, dword [rax + 1 * rdx]               | 1b 04 10                |
    | sbb eax, dword [rax + 1 * rbx]               | 1b 04 18                |
    | sbb eax, dword [rax + 1 * rbp]               | 1b 04 28                |
    | sbb eax, dword [rax + 1 * rsi]               | 1b 04 30                |
    | sbb eax, dword [rax + 1 * rdi]               | 1b 04 38                |
    | sbb eax, dword [rax + 1 * r8]                | 42 1b 04 00             |
    | sbb eax, dword [rax + 1 * r9]                | 42 1b 04 08             |
    | sbb eax, dword [rax + 1 * r10]               | 42 1b 04 10             |
    | sbb eax, dword [rax + 1 * r11]               | 42 1b 04 18             |
    | sbb eax, dword [rax + 1 * r12]               | 42 1b 04 20             |
    | sbb eax, dword [rax + 1 * r13]               | 42 1b 04 28             |
    | sbb eax, dword [rax + 1 * r14]               | 42 1b 04 30             |
    | sbb eax, dword [rax + 1 * r15]               | 42 1b 04 38             |
    | sbb eax, dword [rax + 2 * rcx]               | 1b 04 48                |
    | sbb eax, dword [rax + 4 * rcx]               | 1b 04 88                |
    | sbb eax, dword [rax + 8 * rcx]               | 1b 04 c8                |
    | sbb eax, dword [r8 + 1 * r9]                 | 43 1b 04 08             |
    | sbb eax, dword [r8 + 2 * r9]                 | 43 1b 04 48             |
    | sbb eax, dword [r8 + 4 * r9]                 | 43 1b 04 88             |
    | sbb eax, dword [r8 + 8 * r9]                 | 43 1b 04 c8             |
    | sbb eax, dword [1 * rcx]                     | 1b 04 0d 00 00 00 00    |
    | sbb eax, dword [2 * rcx]                     | 1b 04 4d 00 00 00 00    |
    | sbb eax, dword [4 * rcx]                     | 1b 04 8d 00 00 00 00    |
    | sbb eax, dword [8 * rcx]                     | 1b 04 cd 00 00 00 00    |
    | sbb eax, dword [1 * r9]                      | 42 1b 04 0d 00 00 00 00 |
    | sbb eax, dword [2 * r9]                      | 42 1b 04 4d 00 00 00 00 |
    | sbb eax, dword [4 * r9]                      | 42 1b 04 8d 00 00 00 00 |
    | sbb eax, dword [8 * r9]                      | 42 1b 04 cd 00 00 00 00 |
    | sbb eax, dword [r13 + 8 * r12]               | 43 1b 44 e5 00          |
    | sbb eax, dword [rsp + 4 * r15]               | 42 1b 04 bc             |
    | sbb eax, dword [rax + 1 * rcx + 0x00]        | 1b 44 08 00             |
    | sbb eax, dword [rax + 1 * rcx - 0x00]        | 1b 44 08 00             |
    | sbb eax, dword [rax + 1 * rcx + 0x01]        | 1b 44 08 01             |
    | sbb eax, dword [rax + 1 * rcx - 0x01]        | 1b 44 08 ff             |
    | sbb eax, dword [rax + 1 * rcx + 0x00000001]  | 1b 84 08 01 00 00 00    |
    | sbb eax, dword [rax + 1 * rcx - 0x00000001]  | 1b 84 08 ff ff ff ff    |
    | sbb eax, dword [rax + 1 * rcx + 0x7f]        | 1b 44 08 7f             |
    | sbb eax, dword [rax + 1 * rcx - 0x7f]        | 1b 44 08 81             |
    | sbb eax, dword [rax + 1 * rcx + 0x80]        | 1b 84 08 80 00 00 00    |
    | sbb eax, dword [rax + 1 * rcx - 0x80]        | 1b 44 08 80             |
    | sbb eax, dword [rax + 1 * rcx - 0x81]        | 1b 84 08 7f ff ff ff    |
    | sbb eax, dword [rax + 1 * rcx + 0xff]        | 1b 84 08 ff 00 00 00    |
    | sbb eax, dword [rax + 1 * rcx - 0xff]        | 1b 84 08 01 ff ff ff    |
    | sbb eax, dword [rax + 1 * rcx + 0x7fffffff]  | 1b 84 08 ff ff ff 7f    |
    | sbb eax, dword [rax + 1 * rcx - 0x7fffffff]  | 1b 84 08 01 00 00 80    |
    | sbb eax, dword [rax + 1 * rcx - 0x80000000]  | 1b 84 08 00 00 00 80    |
    | sbb eax, dword [r10 + 0x7f]                  | 41 1b 42 7f             |
    | sbb eax, dword [r10 + 0x80]                  | 41 1b 82 80 00 00 00    |
    | sbb eax, dword [r10 - 0x80]                  | 41 1b 42 80             |
    | sbb eax, dword [r10 - 0x81]                  | 41 1b 82 7f ff ff ff    |
    | sbb ecx, dword [rdx]                         | 1b 0a                   |
    | sbb edx, dword [rbx]                         | 1b 13                   |
    | sbb ebx, dword [rsp]                         | 1b 1c 24                |
    | sbb esp, dword [rbp]                         | 1b 65 00                |
    | sbb ebp, dword [rsi]                         | 1b 2e                   |
    | sbb esi, dword [rdi]                         | 1b 37                   |
    | sbb edi, dword [r8]                          | 41 1b 38                |
    | sbb r8d, dword [r9]                          | 45 1b 01                |
    | sbb r9d, dword [r10]                         | 45 1b 0a                |
    | sbb r10d, dword [r11]                        | 45 1b 13                |
    | sbb r11d, dword [r12]                        | 45 1b 1c 24             |
    | sbb r12d, dword [r13]                        | 45 1b 65 00             |
    | sbb r13d, dword [r14]                        | 45 1b 2e                |
    | sbb r14d, dword [r15]                        | 45 1b 37                |
    | sbb r15d, dword [rax + 1 * rcx]              | 44 1b 3c 08             |
    | sbb ecx, dword [rdx + 1 * rcx]               | 1b 0c 0a                |
    | sbb edx, dword [rbx + 1 * rcx]               | 1b 14 0b                |
    | sbb ebx, dword [rsp + 1 * rcx]               | 1b 1c 0c                |
    | sbb esp, dword [rbp + 1 * rcx]               | 1b 64 0d 00             |
    | sbb ebp, dword [rsi + 1 * rcx]               | 1b 2c 0e                |
    | sbb esi, dword [rdi + 1 * rcx]               | 1b 34 0f                |
    | sbb edi, dword [r8 + 1 * rcx]                | 41 1b 3c 08             |
    | sbb r8d, dword [r9 + 1 * rcx]                | 45 1b 04 09             |
    | sbb r9d, dword [r10 + 1 * rcx]               | 45 1b 0c 0a             |
    | sbb r10d, dword [r11 + 1 * rcx]              | 45 1b 14 0b             |
    | sbb r11d, dword [r12 + 1 * rcx]              | 45 1b 1c 0c             |
    | sbb r12d, dword [r13 + 1 * rcx]              | 45 1b 64 0d 00          |
    | sbb r13d, dword [r14 + 1 * rcx]              | 45 1b 2c 0e             |
    | sbb r14d, dword [r15 + 1 * rcx]              | 45 1b 34 0f             |
    | sbb r15d, dword [rax + 1 * rax]              | 44 1b 3c 00             |
    | sbb ecx, dword [rax + 1 * rbx]               | 1b 0c 18                |
    | sbb edx, dword [rax + 1 * rbp]               | 1b 14 28                |
    | sbb ebx, dword [rax + 1 * rsi]               | 1b 1c 30                |
    | sbb esp, dword [rax + 1 * rdi]               | 1b 24 38                |
    | sbb ebp, dword [rax + 1 * r8]                | 42 1b 2c 00             |
    | sbb esi, dword [rax + 1 * r9]                | 42 1b 34 08             |
    | sbb edi, dword [rax + 1 * r10]               | 42 1b 3c 10             |
    | sbb r8d, dword [rax + 1 * r11]               | 46 1b 04 18             |
    | sbb r9d, dword [rax + 1 * r12]               | 46 1b 0c 20             |
    | sbb r10d, dword [rax + 1 * r13]              | 46 1b 14 28             |
    | sbb r11d, dword [rax + 1 * r14]              | 46 1b 1c 30             |
    | sbb r12d, dword [rax + 1 * r15]              | 46 1b 24 38             |
    | sbb r13d, dword [rax + 2 * rcx]              | 44 1b 2c 48             |
    | sbb r14d, dword [rax + 4 * rcx]              | 44 1b 34 88             |
    | sbb r15d, dword [rax + 8 * rcx]              | 44 1b 3c c8             |
    | sbb ecx, dword [r8 + 2 * r9]                 | 43 1b 0c 48             |
    | sbb edx, dword [r8 + 4 * r9]                 | 43 1b 14 88             |
    | sbb ebx, dword [r8 + 8 * r9]                 | 43 1b 1c c8             |
    | sbb esp, dword [1 * rcx]                     | 1b 24 0d 00 00 00 00    |
    | sbb ebp, dword [2 * rcx]                     | 1b 2c 4d 00 00 00 00    |
    | sbb esi, dword [4 * rcx]                     | 1b 34 8d 00 00 00 00    |
    | sbb edi, dword [8 * rcx]                     | 1b 3c cd 00 00 00 00    |
    | sbb r8d, dword [1 * r9]                      | 46 1b 04 0d 00 00 00 00 |
    | sbb r9d, dword [2 * r9]                      | 46 1b 0c 4d 00 00 00 00 |
    | sbb r10d, dword [4 * r9]                     | 46 1b 14 8d 00 00 00 00 |
    | sbb r11d, dword [8 * r9]                     | 46 1b 1c cd 00 00 00 00 |
    | sbb r12d, dword [r13 + 8 * r12]              | 47 1b 64 e5 00          |
    | sbb r13d, dword [rsp + 4 * r15]              | 46 1b 2c bc             |
    | sbb r14d, dword [rax + 1 * rcx + 0x00]       | 44 1b 74 08 00          |
    | sbb r15d, dword [rax + 1 * rcx - 0x00]       | 44 1b 7c 08 00          |
    | sbb ecx, dword [rax + 1 * rcx - 0x01]        | 1b 4c 08 ff             |
    | sbb edx, dword [rax + 1 * rcx + 0x00000001]  | 1b 94 08 01 00 00 00    |
    | sbb ebx, dword [rax + 1 * rcx - 0x00000001]  | 1b 9c 08 ff ff ff ff    |
    | sbb esp, dword [rax + 1 * rcx + 0x7f]        | 1b 64 08 7f             |
    | sbb ebp, dword [rax + 1 * rcx - 0x7f]        | 1b 6c 08 81             |
    | sbb esi, dword [rax + 1 * rcx + 0x80]        | 1b b4 08 80 00 00 00    |
    | sbb edi, dword [rax + 1 * rcx - 0x80]        | 1b 7c 08 80             |
    | sbb r8d, dword [rax + 1 * rcx - 0x81]        | 44 1b 84 08 7f ff ff ff |
    | sbb r9d, dword [rax + 1 * rcx + 0xff]        | 44 1b 8c 08 ff 00 00 00 |
    | sbb r10d, dword [rax + 1 * rcx - 0xff]       | 44 1b 94 08 01 ff ff ff |
    | sbb r11d, dword [rax + 1 * rcx + 0x7fffffff] | 44 1b 9c 08 ff ff ff 7f |
    | sbb r12d, dword [rax + 1 * rcx - 0x7fffffff] | 44 1b a4 08 01 00 00 80 |
    | sbb r13d, dword [rax + 1 * rcx - 0x80000000] | 44 1b ac 08 00 00 00 80 |
    | sbb r14d, dword [r10 + 0x7f]                 | 45 1b 72 7f             |
    | sbb r15d, dword [r10 + 0x80]                 | 45 1b ba 80 00 00 00    |
    | sbb ecx, dword [r10 - 0x81]                  | 41 1b 8a 7f ff ff ff    |
    | sbb edx, dword [rax]                         | 1b 10                   |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_sbb_reg32_addr32():
    encode(SBB_REG32_ADDR32)


SBB_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | sbb ax, 0x01   | 66 83 d8 01    | *** | sbb ax, 0x00   | 66 83 d8 00    |
    | sbb cx, 0x01   | 66 83 d9 01    | *** | sbb ax, 0x7f   | 66 83 d8 7f    |
    | sbb dx, 0x01   | 66 83 da 01    | *** | sbb ax, 0x80   | 66 83 d8 80    |
    | sbb bx, 0x01   | 66 83 db 01    | *** | sbb ax, 0xff   | 66 83 d8 ff    |
    | sbb sp, 0x01   | 66 83 dc 01    | *** | sbb cx, 0x7f   | 66 83 d9 7f    |
    | sbb bp, 0x01   | 66 83 dd 01    | *** | sbb dx, 0x80   | 66 83 da 80    |
    | sbb si, 0x01   | 66 83 de 01    | *** | sbb bx, 0xff   | 66 83 db ff    |
    | sbb di, 0x01   | 66 83 df 01    | *** | sbb sp, 0x00   | 66 83 dc 00    |
    | sbb r8w, 0x01  | 66 41 83 d8 01 | *** | sbb si, 0x7f   | 66 83 de 7f    |
    | sbb r9w, 0x01  | 66 41 83 d9 01 | *** | sbb di, 0x80   | 66 83 df 80    |
    | sbb r10w, 0x01 | 66 41 83 da 01 | *** | sbb r8w, 0xff  | 66 41 83 d8 ff |
    | sbb r11w, 0x01 | 66 41 83 db 01 | *** | sbb r9w, 0x00  | 66 41 83 d9 00 |
    | sbb r12w, 0x01 | 66 41 83 dc 01 | *** | sbb r11w, 0x7f | 66 41 83 db 7f |
    | sbb r13w, 0x01 | 66 41 83 dd 01 | *** | sbb r12w, 0x80 | 66 41 83 dc 80 |
    | sbb r14w, 0x01 | 66 41 83 de 01 | *** | sbb r13w, 0xff | 66 41 83 dd ff |
    | sbb r15w, 0x01 | 66 41 83 df 01 | *** | sbb r14w, 0x00 | 66 41 83 de 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_sbb_reg16_imm8():
    encode(SBB_REG16_IMM8)


SBB_REG16_IMM16 = """
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | instruction      | encoding          | *** | instruction      | encoding          |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | sbb ax, 0x0001   | 66 1d 01 00       | *** | sbb ax, 0x00ff   | 66 1d ff 00       |
    | sbb cx, 0x0001   | 66 81 d9 01 00    | *** | sbb ax, 0x0100   | 66 1d 00 01       |
    | sbb dx, 0x0001   | 66 81 da 01 00    | *** | sbb ax, 0x7fff   | 66 1d ff 7f       |
    | sbb bx, 0x0001   | 66 81 db 01 00    | *** | sbb ax, 0x8000   | 66 1d 00 80       |
    | sbb sp, 0x0001   | 66 81 dc 01 00    | *** | sbb ax, 0xffff   | 66 1d ff ff       |
    | sbb bp, 0x0001   | 66 81 dd 01 00    | *** | sbb cx, 0x007f   | 66 81 d9 7f 00    |
    | sbb si, 0x0001   | 66 81 de 01 00    | *** | sbb dx, 0x0080   | 66 81 da 80 00    |
    | sbb di, 0x0001   | 66 81 df 01 00    | *** | sbb bx, 0x00ff   | 66 81 db ff 00    |
    | sbb r8w, 0x0001  | 66 41 81 d8 01 00 | *** | sbb sp, 0x0100   | 66 81 dc 00 01    |
    | sbb r9w, 0x0001  | 66 41 81 d9 01 00 | *** | sbb bp, 0x7fff   | 66 81 dd ff 7f    |
    | sbb r10w, 0x0001 | 66 41 81 da 01 00 | *** | sbb si, 0x8000   | 66 81 de 00 80    |
    | sbb r11w, 0x0001 | 66 41 81 db 01 00 | *** | sbb di, 0xffff   | 66 81 df ff ff    |
    | sbb r12w, 0x0001 | 66 41 81 dc 01 00 | *** | sbb r8w, 0x0000  | 66 41 81 d8 00 00 |
    | sbb r13w, 0x0001 | 66 41 81 dd 01 00 | *** | sbb r10w, 0x007f | 66 41 81 da 7f 00 |
    | sbb r14w, 0x0001 | 66 41 81 de 01 00 | *** | sbb r11w, 0x0080 | 66 41 81 db 80 00 |
    | sbb r15w, 0x0001 | 66 41 81 df 01 00 | *** | sbb r12w, 0x00ff | 66 41 81 dc ff 00 |
    | sbb ax, 0x0000   | 66 1d 00 00       | *** | sbb r13w, 0x0100 | 66 41 81 dd 00 01 |
    | sbb ax, 0x007f   | 66 1d 7f 00       | *** | sbb r14w, 0x7fff | 66 41 81 de ff 7f |
    | sbb ax, 0x0080   | 66 1d 80 00       | *** | sbb r15w, 0x8000 | 66 41 81 df 00 80 |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
"""


def can_encode_sbb_reg16_imm16():
    encode(SBB_REG16_IMM16)


SBB_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sbb ax, cx     | 66 19 c8    | *** | sbb ax, r8w    | 66 44 19 c0 |
    | sbb cx, cx     | 66 19 c9    | *** | sbb ax, r9w    | 66 44 19 c8 |
    | sbb dx, cx     | 66 19 ca    | *** | sbb ax, r10w   | 66 44 19 d0 |
    | sbb bx, cx     | 66 19 cb    | *** | sbb ax, r11w   | 66 44 19 d8 |
    | sbb sp, cx     | 66 19 cc    | *** | sbb ax, r12w   | 66 44 19 e0 |
    | sbb bp, cx     | 66 19 cd    | *** | sbb ax, r13w   | 66 44 19 e8 |
    | sbb si, cx     | 66 19 ce    | *** | sbb ax, r14w   | 66 44 19 f0 |
    | sbb di, cx     | 66 19 cf    | *** | sbb ax, r15w   | 66 44 19 f8 |
    | sbb r8w, cx    | 66 41 19 c8 | *** | sbb cx, dx     | 66 19 d1    |
    | sbb r9w, cx    | 66 41 19 c9 | *** | sbb dx, bx     | 66 19 da    |
    | sbb r10w, cx   | 66 41 19 ca | *** | sbb bx, sp     | 66 19 e3    |
    | sbb r11w, cx   | 66 41 19 cb | *** | sbb sp, bp     | 66 19 ec    |
    | sbb r12w, cx   | 66 41 19 cc | *** | sbb bp, si     | 66 19 f5    |
    | sbb r13w, cx   | 66 41 19 cd | *** | sbb si, di     | 66 19 fe    |
    | sbb r14w, cx   | 66 41 19 ce | *** | sbb di, r8w    | 66 44 19 c7 |
    | sbb r15w, cx   | 66 41 19 cf | *** | sbb r8w, r9w   | 66 45 19 c8 |
    | sbb ax, ax     | 66 19 c0    | *** | sbb r9w, r10w  | 66 45 19 d1 |
    | sbb ax, dx     | 66 19 d0    | *** | sbb r10w, r11w | 66 45 19 da |
    | sbb ax, bx     | 66 19 d8    | *** | sbb r11w, r12w | 66 45 19 e3 |
    | sbb ax, sp     | 66 19 e0    | *** | sbb r12w, r13w | 66 45 19 ec |
    | sbb ax, bp     | 66 19 e8    | *** | sbb r13w, r14w | 66 45 19 f5 |
    | sbb ax, si     | 66 19 f0    | *** | sbb r14w, r15w | 66 45 19 fe |
    | sbb ax, di     | 66 19 f8    | *** | sbb r15w, ax   | 66 41 19 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sbb_reg16_reg16():
    encode(SBB_REG16_REG16)


SBB_REG16_ADDR16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sbb ax, word [rcx]                          | 66 1b 01                   |
    | sbb cx, word [rcx]                          | 66 1b 09                   |
    | sbb dx, word [rcx]                          | 66 1b 11                   |
    | sbb bx, word [rcx]                          | 66 1b 19                   |
    | sbb sp, word [rcx]                          | 66 1b 21                   |
    | sbb bp, word [rcx]                          | 66 1b 29                   |
    | sbb si, word [rcx]                          | 66 1b 31                   |
    | sbb di, word [rcx]                          | 66 1b 39                   |
    | sbb r8w, word [rcx]                         | 66 44 1b 01                |
    | sbb r9w, word [rcx]                         | 66 44 1b 09                |
    | sbb r10w, word [rcx]                        | 66 44 1b 11                |
    | sbb r11w, word [rcx]                        | 66 44 1b 19                |
    | sbb r12w, word [rcx]                        | 66 44 1b 21                |
    | sbb r13w, word [rcx]                        | 66 44 1b 29                |
    | sbb r14w, word [rcx]                        | 66 44 1b 31                |
    | sbb r15w, word [rcx]                        | 66 44 1b 39                |
    | sbb ax, word [rax]                          | 66 1b 00                   |
    | sbb ax, word [rdx]                          | 66 1b 02                   |
    | sbb ax, word [rbx]                          | 66 1b 03                   |
    | sbb ax, word [rsp]                          | 66 1b 04 24                |
    | sbb ax, word [rbp]                          | 66 1b 45 00                |
    | sbb ax, word [rsi]                          | 66 1b 06                   |
    | sbb ax, word [rdi]                          | 66 1b 07                   |
    | sbb ax, word [r8]                           | 66 41 1b 00                |
    | sbb ax, word [r9]                           | 66 41 1b 01                |
    | sbb ax, word [r10]                          | 66 41 1b 02                |
    | sbb ax, word [r11]                          | 66 41 1b 03                |
    | sbb ax, word [r12]                          | 66 41 1b 04 24             |
    | sbb ax, word [r13]                          | 66 41 1b 45 00             |
    | sbb ax, word [r14]                          | 66 41 1b 06                |
    | sbb ax, word [r15]                          | 66 41 1b 07                |
    | sbb ax, word [rax + 1 * rcx]                | 66 1b 04 08                |
    | sbb ax, word [rcx + 1 * rcx]                | 66 1b 04 09                |
    | sbb ax, word [rdx + 1 * rcx]                | 66 1b 04 0a                |
    | sbb ax, word [rbx + 1 * rcx]                | 66 1b 04 0b                |
    | sbb ax, word [rsp + 1 * rcx]                | 66 1b 04 0c                |
    | sbb ax, word [rbp + 1 * rcx]                | 66 1b 44 0d 00             |
    | sbb ax, word [rsi + 1 * rcx]                | 66 1b 04 0e                |
    | sbb ax, word [rdi + 1 * rcx]                | 66 1b 04 0f                |
    | sbb ax, word [r8 + 1 * rcx]                 | 66 41 1b 04 08             |
    | sbb ax, word [r9 + 1 * rcx]                 | 66 41 1b 04 09             |
    | sbb ax, word [r10 + 1 * rcx]                | 66 41 1b 04 0a             |
    | sbb ax, word [r11 + 1 * rcx]                | 66 41 1b 04 0b             |
    | sbb ax, word [r12 + 1 * rcx]                | 66 41 1b 04 0c             |
    | sbb ax, word [r13 + 1 * rcx]                | 66 41 1b 44 0d 00          |
    | sbb ax, word [r14 + 1 * rcx]                | 66 41 1b 04 0e             |
    | sbb ax, word [r15 + 1 * rcx]                | 66 41 1b 04 0f             |
    | sbb ax, word [rax + 1 * rax]                | 66 1b 04 00                |
    | sbb ax, word [rax + 1 * rdx]                | 66 1b 04 10                |
    | sbb ax, word [rax + 1 * rbx]                | 66 1b 04 18                |
    | sbb ax, word [rax + 1 * rbp]                | 66 1b 04 28                |
    | sbb ax, word [rax + 1 * rsi]                | 66 1b 04 30                |
    | sbb ax, word [rax + 1 * rdi]                | 66 1b 04 38                |
    | sbb ax, word [rax + 1 * r8]                 | 66 42 1b 04 00             |
    | sbb ax, word [rax + 1 * r9]                 | 66 42 1b 04 08             |
    | sbb ax, word [rax + 1 * r10]                | 66 42 1b 04 10             |
    | sbb ax, word [rax + 1 * r11]                | 66 42 1b 04 18             |
    | sbb ax, word [rax + 1 * r12]                | 66 42 1b 04 20             |
    | sbb ax, word [rax + 1 * r13]                | 66 42 1b 04 28             |
    | sbb ax, word [rax + 1 * r14]                | 66 42 1b 04 30             |
    | sbb ax, word [rax + 1 * r15]                | 66 42 1b 04 38             |
    | sbb ax, word [rax + 2 * rcx]                | 66 1b 04 48                |
    | sbb ax, word [rax + 4 * rcx]                | 66 1b 04 88                |
    | sbb ax, word [rax + 8 * rcx]                | 66 1b 04 c8                |
    | sbb ax, word [r8 + 1 * r9]                  | 66 43 1b 04 08             |
    | sbb ax, word [r8 + 2 * r9]                  | 66 43 1b 04 48             |
    | sbb ax, word [r8 + 4 * r9]                  | 66 43 1b 04 88             |
    | sbb ax, word [r8 + 8 * r9]                  | 66 43 1b 04 c8             |
    | sbb ax, word [1 * rcx]                      | 66 1b 04 0d 00 00 00 00    |
    | sbb ax, word [2 * rcx]                      | 66 1b 04 4d 00 00 00 00    |
    | sbb ax, word [4 * rcx]                      | 66 1b 04 8d 00 00 00 00    |
    | sbb ax, word [8 * rcx]                      | 66 1b 04 cd 00 00 00 00    |
    | sbb ax, word [1 * r9]                       | 66 42 1b 04 0d 00 00 00 00 |
    | sbb ax, word [2 * r9]                       | 66 42 1b 04 4d 00 00 00 00 |
    | sbb ax, word [4 * r9]                       | 66 42 1b 04 8d 00 00 00 00 |
    | sbb ax, word [8 * r9]                       | 66 42 1b 04 cd 00 00 00 00 |
    | sbb ax, word [r13 + 8 * r12]                | 66 43 1b 44 e5 00          |
    | sbb ax, word [rsp + 4 * r15]                | 66 42 1b 04 bc             |
    | sbb ax, word [rax + 1 * rcx + 0x00]         | 66 1b 44 08 00             |
    | sbb ax, word [rax + 1 * rcx - 0x00]         | 66 1b 44 08 00             |
    | sbb ax, word [rax + 1 * rcx + 0x01]         | 66 1b 44 08 01             |
    | sbb ax, word [rax + 1 * rcx - 0x01]         | 66 1b 44 08 ff             |
    | sbb ax, word [rax + 1 * rcx + 0x00000001]   | 66 1b 84 08 01 00 00 00    |
    | sbb ax, word [rax + 1 * rcx - 0x00000001]   | 66 1b 84 08 ff ff ff ff    |
    | sbb ax, word [rax + 1 * rcx + 0x7f]         | 66 1b 44 08 7f             |
    | sbb ax, word [rax + 1 * rcx - 0x7f]         | 66 1b 44 08 81             |
    | sbb ax, word [rax + 1 * rcx + 0x80]         | 66 1b 84 08 80 00 00 00    |
    | sbb ax, word [rax + 1 * rcx - 0x80]         | 66 1b 44 08 80             |
    | sbb ax, word [rax + 1 * rcx - 0x81]         | 66 1b 84 08 7f ff ff ff    |
    | sbb ax, word [rax + 1 * rcx + 0xff]         | 66 1b 84 08 ff 00 00 00    |
    | sbb ax, word [rax + 1 * rcx - 0xff]         | 66 1b 84 08 01 ff ff ff    |
    | sbb ax, word [rax + 1 * rcx + 0x7fffffff]   | 66 1b 84 08 ff ff ff 7f    |
    | sbb ax, word [rax + 1 * rcx - 0x7fffffff]   | 66 1b 84 08 01 00 00 80    |
    | sbb ax, word [rax + 1 * rcx - 0x80000000]   | 66 1b 84 08 00 00 00 80    |
    | sbb ax, word [r10 + 0x7f]                   | 66 41 1b 42 7f             |
    | sbb ax, word [r10 + 0x80]                   | 66 41 1b 82 80 00 00 00    |
    | sbb ax, word [r10 - 0x80]                   | 66 41 1b 42 80             |
    | sbb ax, word [r10 - 0x81]                   | 66 41 1b 82 7f ff ff ff    |
    | sbb cx, word [rdx]                          | 66 1b 0a                   |
    | sbb dx, word [rbx]                          | 66 1b 13                   |
    | sbb bx, word [rsp]                          | 66 1b 1c 24                |
    | sbb sp, word [rbp]                          | 66 1b 65 00                |
    | sbb bp, word [rsi]                          | 66 1b 2e                   |
    | sbb si, word [rdi]                          | 66 1b 37                   |
    | sbb di, word [r8]                           | 66 41 1b 38                |
    | sbb r8w, word [r9]                          | 66 45 1b 01                |
    | sbb r9w, word [r10]                         | 66 45 1b 0a                |
    | sbb r10w, word [r11]                        | 66 45 1b 13                |
    | sbb r11w, word [r12]                        | 66 45 1b 1c 24             |
    | sbb r12w, word [r13]                        | 66 45 1b 65 00             |
    | sbb r13w, word [r14]                        | 66 45 1b 2e                |
    | sbb r14w, word [r15]                        | 66 45 1b 37                |
    | sbb r15w, word [rax + 1 * rcx]              | 66 44 1b 3c 08             |
    | sbb cx, word [rdx + 1 * rcx]                | 66 1b 0c 0a                |
    | sbb dx, word [rbx + 1 * rcx]                | 66 1b 14 0b                |
    | sbb bx, word [rsp + 1 * rcx]                | 66 1b 1c 0c                |
    | sbb sp, word [rbp + 1 * rcx]                | 66 1b 64 0d 00             |
    | sbb bp, word [rsi + 1 * rcx]                | 66 1b 2c 0e                |
    | sbb si, word [rdi + 1 * rcx]                | 66 1b 34 0f                |
    | sbb di, word [r8 + 1 * rcx]                 | 66 41 1b 3c 08             |
    | sbb r8w, word [r9 + 1 * rcx]                | 66 45 1b 04 09             |
    | sbb r9w, word [r10 + 1 * rcx]               | 66 45 1b 0c 0a             |
    | sbb r10w, word [r11 + 1 * rcx]              | 66 45 1b 14 0b             |
    | sbb r11w, word [r12 + 1 * rcx]              | 66 45 1b 1c 0c             |
    | sbb r12w, word [r13 + 1 * rcx]              | 66 45 1b 64 0d 00          |
    | sbb r13w, word [r14 + 1 * rcx]              | 66 45 1b 2c 0e             |
    | sbb r14w, word [r15 + 1 * rcx]              | 66 45 1b 34 0f             |
    | sbb r15w, word [rax + 1 * rax]              | 66 44 1b 3c 00             |
    | sbb cx, word [rax + 1 * rbx]                | 66 1b 0c 18                |
    | sbb dx, word [rax + 1 * rbp]                | 66 1b 14 28                |
    | sbb bx, word [rax + 1 * rsi]                | 66 1b 1c 30                |
    | sbb sp, word [rax + 1 * rdi]                | 66 1b 24 38                |
    | sbb bp, word [rax + 1 * r8]                 | 66 42 1b 2c 00             |
    | sbb si, word [rax + 1 * r9]                 | 66 42 1b 34 08             |
    | sbb di, word [rax + 1 * r10]                | 66 42 1b 3c 10             |
    | sbb r8w, word [rax + 1 * r11]               | 66 46 1b 04 18             |
    | sbb r9w, word [rax + 1 * r12]               | 66 46 1b 0c 20             |
    | sbb r10w, word [rax + 1 * r13]              | 66 46 1b 14 28             |
    | sbb r11w, word [rax + 1 * r14]              | 66 46 1b 1c 30             |
    | sbb r12w, word [rax + 1 * r15]              | 66 46 1b 24 38             |
    | sbb r13w, word [rax + 2 * rcx]              | 66 44 1b 2c 48             |
    | sbb r14w, word [rax + 4 * rcx]              | 66 44 1b 34 88             |
    | sbb r15w, word [rax + 8 * rcx]              | 66 44 1b 3c c8             |
    | sbb cx, word [r8 + 2 * r9]                  | 66 43 1b 0c 48             |
    | sbb dx, word [r8 + 4 * r9]                  | 66 43 1b 14 88             |
    | sbb bx, word [r8 + 8 * r9]                  | 66 43 1b 1c c8             |
    | sbb sp, word [1 * rcx]                      | 66 1b 24 0d 00 00 00 00    |
    | sbb bp, word [2 * rcx]                      | 66 1b 2c 4d 00 00 00 00    |
    | sbb si, word [4 * rcx]                      | 66 1b 34 8d 00 00 00 00    |
    | sbb di, word [8 * rcx]                      | 66 1b 3c cd 00 00 00 00    |
    | sbb r8w, word [1 * r9]                      | 66 46 1b 04 0d 00 00 00 00 |
    | sbb r9w, word [2 * r9]                      | 66 46 1b 0c 4d 00 00 00 00 |
    | sbb r10w, word [4 * r9]                     | 66 46 1b 14 8d 00 00 00 00 |
    | sbb r11w, word [8 * r9]                     | 66 46 1b 1c cd 00 00 00 00 |
    | sbb r12w, word [r13 + 8 * r12]              | 66 47 1b 64 e5 00          |
    | sbb r13w, word [rsp + 4 * r15]              | 66 46 1b 2c bc             |
    | sbb r14w, word [rax + 1 * rcx + 0x00]       | 66 44 1b 74 08 00          |
    | sbb r15w, word [rax + 1 * rcx - 0x00]       | 66 44 1b 7c 08 00          |
    | sbb cx, word [rax + 1 * rcx - 0x01]         | 66 1b 4c 08 ff             |
    | sbb dx, word [rax + 1 * rcx + 0x00000001]   | 66 1b 94 08 01 00 00 00    |
    | sbb bx, word [rax + 1 * rcx - 0x00000001]   | 66 1b 9c 08 ff ff ff ff    |
    | sbb sp, word [rax + 1 * rcx + 0x7f]         | 66 1b 64 08 7f             |
    | sbb bp, word [rax + 1 * rcx - 0x7f]         | 66 1b 6c 08 81             |
    | sbb si, word [rax + 1 * rcx + 0x80]         | 66 1b b4 08 80 00 00 00    |
    | sbb di, word [rax + 1 * rcx - 0x80]         | 66 1b 7c 08 80             |
    | sbb r8w, word [rax + 1 * rcx - 0x81]        | 66 44 1b 84 08 7f ff ff ff |
    | sbb r9w, word [rax + 1 * rcx + 0xff]        | 66 44 1b 8c 08 ff 00 00 00 |
    | sbb r10w, word [rax + 1 * rcx - 0xff]       | 66 44 1b 94 08 01 ff ff ff |
    | sbb r11w, word [rax + 1 * rcx + 0x7fffffff] | 66 44 1b 9c 08 ff ff ff 7f |
    | sbb r12w, word [rax + 1 * rcx - 0x7fffffff] | 66 44 1b a4 08 01 00 00 80 |
    | sbb r13w, word [rax + 1 * rcx - 0x80000000] | 66 44 1b ac 08 00 00 00 80 |
    | sbb r14w, word [r10 + 0x7f]                 | 66 45 1b 72 7f             |
    | sbb r15w, word [r10 + 0x80]                 | 66 45 1b ba 80 00 00 00    |
    | sbb cx, word [r10 - 0x81]                   | 66 41 1b 8a 7f ff ff ff    |
    | sbb dx, word [rax]                          | 66 1b 10                   |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sbb_reg16_addr16():
    encode(SBB_REG16_ADDR16)


SBB_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sbb al, 0x01   | 1c 01       | *** | sbb al, 0x00   | 1c 00       |
    | sbb cl, 0x01   | 80 d9 01    | *** | sbb al, 0x7f   | 1c 7f       |
    | sbb dl, 0x01   | 80 da 01    | *** | sbb al, 0x80   | 1c 80       |
    | sbb bl, 0x01   | 80 db 01    | *** | sbb al, 0xff   | 1c ff       |
    | sbb spl, 0x01  | 40 80 dc 01 | *** | sbb cl, 0x7f   | 80 d9 7f    |
    | sbb bpl, 0x01  | 40 80 dd 01 | *** | sbb dl, 0x80   | 80 da 80    |
    | sbb sil, 0x01  | 40 80 de 01 | *** | sbb bl, 0xff   | 80 db ff    |
    | sbb dil, 0x01  | 40 80 df 01 | *** | sbb spl, 0x00  | 40 80 dc 00 |
    | sbb r8b, 0x01  | 41 80 d8 01 | *** | sbb sil, 0x7f  | 40 80 de 7f |
    | sbb r9b, 0x01  | 41 80 d9 01 | *** | sbb dil, 0x80  | 40 80 df 80 |
    | sbb r10b, 0x01 | 41 80 da 01 | *** | sbb r8b, 0xff  | 41 80 d8 ff |
    | sbb r11b, 0x01 | 41 80 db 01 | *** | sbb r9b, 0x00  | 41 80 d9 00 |
    | sbb r12b, 0x01 | 41 80 dc 01 | *** | sbb r11b, 0x7f | 41 80 db 7f |
    | sbb r13b, 0x01 | 41 80 dd 01 | *** | sbb r12b, 0x80 | 41 80 dc 80 |
    | sbb r14b, 0x01 | 41 80 de 01 | *** | sbb r13b, 0xff | 41 80 dd ff |
    | sbb r15b, 0x01 | 41 80 df 01 | *** | sbb r14b, 0x00 | 41 80 de 00 |
    | sbb ah, 0x01   | 80 dc 01    | *** | sbb ah, 0x7f   | 80 dc 7f    |
    | sbb ch, 0x01   | 80 dd 01    | *** | sbb ch, 0x80   | 80 dd 80    |
    | sbb dh, 0x01   | 80 de 01    | *** | sbb dh, 0xff   | 80 de ff    |
    | sbb bh, 0x01   | 80 df 01    | *** | sbb bh, 0x00   | 80 df 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sbb_reg8_imm8():
    encode(SBB_REG8_IMM8)


SBB_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | sbb al, cl     | 18 c8    | *** | sbb al, r10b   | 44 18 d0 |
    | sbb cl, cl     | 18 c9    | *** | sbb al, r11b   | 44 18 d8 |
    | sbb dl, cl     | 18 ca    | *** | sbb al, r12b   | 44 18 e0 |
    | sbb bl, cl     | 18 cb    | *** | sbb al, r13b   | 44 18 e8 |
    | sbb spl, cl    | 40 18 cc | *** | sbb al, r14b   | 44 18 f0 |
    | sbb bpl, cl    | 40 18 cd | *** | sbb al, r15b   | 44 18 f8 |
    | sbb sil, cl    | 40 18 ce | *** | sbb al, ah     | 18 e0    |
    | sbb dil, cl    | 40 18 cf | *** | sbb al, ch     | 18 e8    |
    | sbb r8b, cl    | 41 18 c8 | *** | sbb al, dh     | 18 f0    |
    | sbb r9b, cl    | 41 18 c9 | *** | sbb al, bh     | 18 f8    |
    | sbb r10b, cl   | 41 18 ca | *** | sbb cl, dl     | 18 d1    |
    | sbb r11b, cl   | 41 18 cb | *** | sbb dl, bl     | 18 da    |
    | sbb r12b, cl   | 41 18 cc | *** | sbb bl, spl    | 40 18 e3 |
    | sbb r13b, cl   | 41 18 cd | *** | sbb spl, bpl   | 40 18 ec |
    | sbb r14b, cl   | 41 18 ce | *** | sbb bpl, sil   | 40 18 f5 |
    | sbb r15b, cl   | 41 18 cf | *** | sbb sil, dil   | 40 18 fe |
    | sbb ah, cl     | 18 cc    | *** | sbb dil, r8b   | 44 18 c7 |
    | sbb ch, cl     | 18 cd    | *** | sbb r8b, r9b   | 45 18 c8 |
    | sbb dh, cl     | 18 ce    | *** | sbb r9b, r10b  | 45 18 d1 |
    | sbb bh, cl     | 18 cf    | *** | sbb r10b, r11b | 45 18 da |
    | sbb al, al     | 18 c0    | *** | sbb r11b, r12b | 45 18 e3 |
    | sbb al, dl     | 18 d0    | *** | sbb r12b, r13b | 45 18 ec |
    | sbb al, bl     | 18 d8    | *** | sbb r13b, r14b | 45 18 f5 |
    | sbb al, spl    | 40 18 e0 | *** | sbb r14b, r15b | 45 18 fe |
    | sbb al, bpl    | 40 18 e8 | *** | sbb r15b, ah   | !! !! !! |
    | sbb al, sil    | 40 18 f0 | *** | sbb ah, ch     | 18 ec    |
    | sbb al, dil    | 40 18 f8 | *** | sbb ch, dh     | 18 f5    |
    | sbb al, r8b    | 44 18 c0 | *** | sbb dh, bh     | 18 fe    |
    | sbb al, r9b    | 44 18 c8 | *** | sbb bh, al     | 18 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_sbb_reg8_reg8():
    encode(SBB_REG8_REG8)


SBB_REG8_ADDR8 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | sbb al, byte [rcx]                          | 1a 01                   |
    | sbb cl, byte [rcx]                          | 1a 09                   |
    | sbb dl, byte [rcx]                          | 1a 11                   |
    | sbb bl, byte [rcx]                          | 1a 19                   |
    | sbb spl, byte [rcx]                         | 40 1a 21                |
    | sbb bpl, byte [rcx]                         | 40 1a 29                |
    | sbb sil, byte [rcx]                         | 40 1a 31                |
    | sbb dil, byte [rcx]                         | 40 1a 39                |
    | sbb r8b, byte [rcx]                         | 44 1a 01                |
    | sbb r9b, byte [rcx]                         | 44 1a 09                |
    | sbb r10b, byte [rcx]                        | 44 1a 11                |
    | sbb r11b, byte [rcx]                        | 44 1a 19                |
    | sbb r12b, byte [rcx]                        | 44 1a 21                |
    | sbb r13b, byte [rcx]                        | 44 1a 29                |
    | sbb r14b, byte [rcx]                        | 44 1a 31                |
    | sbb r15b, byte [rcx]                        | 44 1a 39                |
    | sbb ah, byte [rcx]                          | 1a 21                   |
    | sbb ch, byte [rcx]                          | 1a 29                   |
    | sbb dh, byte [rcx]                          | 1a 31                   |
    | sbb bh, byte [rcx]                          | 1a 39                   |
    | sbb al, byte [rax]                          | 1a 00                   |
    | sbb al, byte [rdx]                          | 1a 02                   |
    | sbb al, byte [rbx]                          | 1a 03                   |
    | sbb al, byte [rsp]                          | 1a 04 24                |
    | sbb al, byte [rbp]                          | 1a 45 00                |
    | sbb al, byte [rsi]                          | 1a 06                   |
    | sbb al, byte [rdi]                          | 1a 07                   |
    | sbb al, byte [r8]                           | 41 1a 00                |
    | sbb al, byte [r9]                           | 41 1a 01                |
    | sbb al, byte [r10]                          | 41 1a 02                |
    | sbb al, byte [r11]                          | 41 1a 03                |
    | sbb al, byte [r12]                          | 41 1a 04 24             |
    | sbb al, byte [r13]                          | 41 1a 45 00             |
    | sbb al, byte [r14]                          | 41 1a 06                |
    | sbb al, byte [r15]                          | 41 1a 07                |
    | sbb al, byte [rax + 1 * rcx]                | 1a 04 08                |
    | sbb al, byte [rcx + 1 * rcx]                | 1a 04 09                |
    | sbb al, byte [rdx + 1 * rcx]                | 1a 04 0a                |
    | sbb al, byte [rbx + 1 * rcx]                | 1a 04 0b                |
    | sbb al, byte [rsp + 1 * rcx]                | 1a 04 0c                |
    | sbb al, byte [rbp + 1 * rcx]                | 1a 44 0d 00             |
    | sbb al, byte [rsi + 1 * rcx]                | 1a 04 0e                |
    | sbb al, byte [rdi + 1 * rcx]                | 1a 04 0f                |
    | sbb al, byte [r8 + 1 * rcx]                 | 41 1a 04 08             |
    | sbb al, byte [r9 + 1 * rcx]                 | 41 1a 04 09             |
    | sbb al, byte [r10 + 1 * rcx]                | 41 1a 04 0a             |
    | sbb al, byte [r11 + 1 * rcx]                | 41 1a 04 0b             |
    | sbb al, byte [r12 + 1 * rcx]                | 41 1a 04 0c             |
    | sbb al, byte [r13 + 1 * rcx]                | 41 1a 44 0d 00          |
    | sbb al, byte [r14 + 1 * rcx]                | 41 1a 04 0e             |
    | sbb al, byte [r15 + 1 * rcx]                | 41 1a 04 0f             |
    | sbb al, byte [rax + 1 * rax]                | 1a 04 00                |
    | sbb al, byte [rax + 1 * rdx]                | 1a 04 10                |
    | sbb al, byte [rax + 1 * rbx]                | 1a 04 18                |
    | sbb al, byte [rax + 1 * rbp]                | 1a 04 28                |
    | sbb al, byte [rax + 1 * rsi]                | 1a 04 30                |
    | sbb al, byte [rax + 1 * rdi]                | 1a 04 38                |
    | sbb al, byte [rax + 1 * r8]                 | 42 1a 04 00             |
    | sbb al, byte [rax + 1 * r9]                 | 42 1a 04 08             |
    | sbb al, byte [rax + 1 * r10]                | 42 1a 04 10             |
    | sbb al, byte [rax + 1 * r11]                | 42 1a 04 18             |
    | sbb al, byte [rax + 1 * r12]                | 42 1a 04 20             |
    | sbb al, byte [rax + 1 * r13]                | 42 1a 04 28             |
    | sbb al, byte [rax + 1 * r14]                | 42 1a 04 30             |
    | sbb al, byte [rax + 1 * r15]                | 42 1a 04 38             |
    | sbb al, byte [rax + 2 * rcx]                | 1a 04 48                |
    | sbb al, byte [rax + 4 * rcx]                | 1a 04 88                |
    | sbb al, byte [rax + 8 * rcx]                | 1a 04 c8                |
    | sbb al, byte [r8 + 1 * r9]                  | 43 1a 04 08             |
    | sbb al, byte [r8 + 2 * r9]                  | 43 1a 04 48             |
    | sbb al, byte [r8 + 4 * r9]                  | 43 1a 04 88             |
    | sbb al, byte [r8 + 8 * r9]                  | 43 1a 04 c8             |
    | sbb al, byte [1 * rcx]                      | 1a 04 0d 00 00 00 00    |
    | sbb al, byte [2 * rcx]                      | 1a 04 4d 00 00 00 00    |
    | sbb al, byte [4 * rcx]                      | 1a 04 8d 00 00 00 00    |
    | sbb al, byte [8 * rcx]                      | 1a 04 cd 00 00 00 00    |
    | sbb al, byte [1 * r9]                       | 42 1a 04 0d 00 00 00 00 |
    | sbb al, byte [2 * r9]                       | 42 1a 04 4d 00 00 00 00 |
    | sbb al, byte [4 * r9]                       | 42 1a 04 8d 00 00 00 00 |
    | sbb al, byte [8 * r9]                       | 42 1a 04 cd 00 00 00 00 |
    | sbb al, byte [r13 + 8 * r12]                | 43 1a 44 e5 00          |
    | sbb al, byte [rsp + 4 * r15]                | 42 1a 04 bc             |
    | sbb al, byte [rax + 1 * rcx + 0x00]         | 1a 44 08 00             |
    | sbb al, byte [rax + 1 * rcx - 0x00]         | 1a 44 08 00             |
    | sbb al, byte [rax + 1 * rcx + 0x01]         | 1a 44 08 01             |
    | sbb al, byte [rax + 1 * rcx - 0x01]         | 1a 44 08 ff             |
    | sbb al, byte [rax + 1 * rcx + 0x00000001]   | 1a 84 08 01 00 00 00    |
    | sbb al, byte [rax + 1 * rcx - 0x00000001]   | 1a 84 08 ff ff ff ff    |
    | sbb al, byte [rax + 1 * rcx + 0x7f]         | 1a 44 08 7f             |
    | sbb al, byte [rax + 1 * rcx - 0x7f]         | 1a 44 08 81             |
    | sbb al, byte [rax + 1 * rcx + 0x80]         | 1a 84 08 80 00 00 00    |
    | sbb al, byte [rax + 1 * rcx - 0x80]         | 1a 44 08 80             |
    | sbb al, byte [rax + 1 * rcx - 0x81]         | 1a 84 08 7f ff ff ff    |
    | sbb al, byte [rax + 1 * rcx + 0xff]         | 1a 84 08 ff 00 00 00    |
    | sbb al, byte [rax + 1 * rcx - 0xff]         | 1a 84 08 01 ff ff ff    |
    | sbb al, byte [rax + 1 * rcx + 0x7fffffff]   | 1a 84 08 ff ff ff 7f    |
    | sbb al, byte [rax + 1 * rcx - 0x7fffffff]   | 1a 84 08 01 00 00 80    |
    | sbb al, byte [rax + 1 * rcx - 0x80000000]   | 1a 84 08 00 00 00 80    |
    | sbb al, byte [r10 + 0x7f]                   | 41 1a 42 7f             |
    | sbb al, byte [r10 + 0x80]                   | 41 1a 82 80 00 00 00    |
    | sbb al, byte [r10 - 0x80]                   | 41 1a 42 80             |
    | sbb al, byte [r10 - 0x81]                   | 41 1a 82 7f ff ff ff    |
    | sbb cl, byte [rdx]                          | 1a 0a                   |
    | sbb dl, byte [rbx]                          | 1a 13                   |
    | sbb bl, byte [rsp]                          | 1a 1c 24                |
    | sbb spl, byte [rbp]                         | 40 1a 65 00             |
    | sbb bpl, byte [rsi]                         | 40 1a 2e                |
    | sbb sil, byte [rdi]                         | 40 1a 37                |
    | sbb dil, byte [r8]                          | 41 1a 38                |
    | sbb r8b, byte [r9]                          | 45 1a 01                |
    | sbb r9b, byte [r10]                         | 45 1a 0a                |
    | sbb r10b, byte [r11]                        | 45 1a 13                |
    | sbb r11b, byte [r12]                        | 45 1a 1c 24             |
    | sbb r12b, byte [r13]                        | 45 1a 65 00             |
    | sbb r13b, byte [r14]                        | 45 1a 2e                |
    | sbb r14b, byte [r15]                        | 45 1a 37                |
    | sbb r15b, byte [rax + 1 * rcx]              | 44 1a 3c 08             |
    | sbb ah, byte [rcx + 1 * rcx]                | 1a 24 09                |
    | sbb ch, byte [rdx + 1 * rcx]                | 1a 2c 0a                |
    | sbb dh, byte [rbx + 1 * rcx]                | 1a 34 0b                |
    | sbb bh, byte [rsp + 1 * rcx]                | 1a 3c 0c                |
    | sbb cl, byte [rsi + 1 * rcx]                | 1a 0c 0e                |
    | sbb dl, byte [rdi + 1 * rcx]                | 1a 14 0f                |
    | sbb bl, byte [r8 + 1 * rcx]                 | 41 1a 1c 08             |
    | sbb spl, byte [r9 + 1 * rcx]                | 41 1a 24 09             |
    | sbb bpl, byte [r10 + 1 * rcx]               | 41 1a 2c 0a             |
    | sbb sil, byte [r11 + 1 * rcx]               | 41 1a 34 0b             |
    | sbb dil, byte [r12 + 1 * rcx]               | 41 1a 3c 0c             |
    | sbb r8b, byte [r13 + 1 * rcx]               | 45 1a 44 0d 00          |
    | sbb r9b, byte [r14 + 1 * rcx]               | 45 1a 0c 0e             |
    | sbb r10b, byte [r15 + 1 * rcx]              | 45 1a 14 0f             |
    | sbb r11b, byte [rax + 1 * rax]              | 44 1a 1c 00             |
    | sbb r12b, byte [rax + 1 * rdx]              | 44 1a 24 10             |
    | sbb r13b, byte [rax + 1 * rbx]              | 44 1a 2c 18             |
    | sbb r14b, byte [rax + 1 * rbp]              | 44 1a 34 28             |
    | sbb r15b, byte [rax + 1 * rsi]              | 44 1a 3c 30             |
    | sbb ah, byte [rax + 1 * rdi]                | 1a 24 38                |
    | sbb ch, byte [rax + 1 * r8]                 | !! !! !!                |
    | sbb dh, byte [rax + 1 * r9]                 | !! !! !!                |
    | sbb bh, byte [rax + 1 * r10]                | !! !! !!                |
    | sbb cl, byte [rax + 1 * r12]                | 42 1a 0c 20             |
    | sbb dl, byte [rax + 1 * r13]                | 42 1a 14 28             |
    | sbb bl, byte [rax + 1 * r14]                | 42 1a 1c 30             |
    | sbb spl, byte [rax + 1 * r15]               | 42 1a 24 38             |
    | sbb bpl, byte [rax + 2 * rcx]               | 40 1a 2c 48             |
    | sbb sil, byte [rax + 4 * rcx]               | 40 1a 34 88             |
    | sbb dil, byte [rax + 8 * rcx]               | 40 1a 3c c8             |
    | sbb r8b, byte [r8 + 1 * r9]                 | 47 1a 04 08             |
    | sbb r9b, byte [r8 + 2 * r9]                 | 47 1a 0c 48             |
    | sbb r10b, byte [r8 + 4 * r9]                | 47 1a 14 88             |
    | sbb r11b, byte [r8 + 8 * r9]                | 47 1a 1c c8             |
    | sbb r12b, byte [1 * rcx]                    | 44 1a 24 0d 00 00 00 00 |
    | sbb r13b, byte [2 * rcx]                    | 44 1a 2c 4d 00 00 00 00 |
    | sbb r14b, byte [4 * rcx]                    | 44 1a 34 8d 00 00 00 00 |
    | sbb r15b, byte [8 * rcx]                    | 44 1a 3c cd 00 00 00 00 |
    | sbb ah, byte [1 * r9]                       | !! !! !!                |
    | sbb ch, byte [2 * r9]                       | !! !! !!                |
    | sbb dh, byte [4 * r9]                       | !! !! !!                |
    | sbb bh, byte [8 * r9]                       | !! !! !!                |
    | sbb cl, byte [rsp + 4 * r15]                | 42 1a 0c bc             |
    | sbb dl, byte [rax + 1 * rcx + 0x00]         | 1a 54 08 00             |
    | sbb bl, byte [rax + 1 * rcx - 0x00]         | 1a 5c 08 00             |
    | sbb spl, byte [rax + 1 * rcx + 0x01]        | 40 1a 64 08 01          |
    | sbb bpl, byte [rax + 1 * rcx - 0x01]        | 40 1a 6c 08 ff          |
    | sbb sil, byte [rax + 1 * rcx + 0x00000001]  | 40 1a b4 08 01 00 00 00 |
    | sbb dil, byte [rax + 1 * rcx - 0x00000001]  | 40 1a bc 08 ff ff ff ff |
    | sbb r8b, byte [rax + 1 * rcx + 0x7f]        | 44 1a 44 08 7f          |
    | sbb r9b, byte [rax + 1 * rcx - 0x7f]        | 44 1a 4c 08 81          |
    | sbb r10b, byte [rax + 1 * rcx + 0x80]       | 44 1a 94 08 80 00 00 00 |
    | sbb r11b, byte [rax + 1 * rcx - 0x80]       | 44 1a 5c 08 80          |
    | sbb r12b, byte [rax + 1 * rcx - 0x81]       | 44 1a a4 08 7f ff ff ff |
    | sbb r13b, byte [rax + 1 * rcx + 0xff]       | 44 1a ac 08 ff 00 00 00 |
    | sbb r14b, byte [rax + 1 * rcx - 0xff]       | 44 1a b4 08 01 ff ff ff |
    | sbb r15b, byte [rax + 1 * rcx + 0x7fffffff] | 44 1a bc 08 ff ff ff 7f |
    | sbb ah, byte [rax + 1 * rcx - 0x7fffffff]   | 1a a4 08 01 00 00 80    |
    | sbb ch, byte [rax + 1 * rcx - 0x80000000]   | 1a ac 08 00 00 00 80    |
    | sbb dh, byte [r10 + 0x7f]                   | !! !! !!                |
    | sbb bh, byte [r10 + 0x80]                   | !! !! !!                |
    | sbb cl, byte [r10 - 0x81]                   | 41 1a 8a 7f ff ff ff    |
    | sbb dl, byte [rax]                          | 1a 10                   |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_sbb_reg8_addr8():
    encode(SBB_REG8_ADDR8)


SBB_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sbb qword [rax], 0x01                        | 48 83 18 01                |
    | sbb qword [rcx], 0x01                        | 48 83 19 01                |
    | sbb qword [rdx], 0x01                        | 48 83 1a 01                |
    | sbb qword [rbx], 0x01                        | 48 83 1b 01                |
    | sbb qword [rsp], 0x01                        | 48 83 1c 24 01             |
    | sbb qword [rbp], 0x01                        | 48 83 5d 00 01             |
    | sbb qword [rsi], 0x01                        | 48 83 1e 01                |
    | sbb qword [rdi], 0x01                        | 48 83 1f 01                |
    | sbb qword [r8], 0x01                         | 49 83 18 01                |
    | sbb qword [r9], 0x01                         | 49 83 19 01                |
    | sbb qword [r10], 0x01                        | 49 83 1a 01                |
    | sbb qword [r11], 0x01                        | 49 83 1b 01                |
    | sbb qword [r12], 0x01                        | 49 83 1c 24 01             |
    | sbb qword [r13], 0x01                        | 49 83 5d 00 01             |
    | sbb qword [r14], 0x01                        | 49 83 1e 01                |
    | sbb qword [r15], 0x01                        | 49 83 1f 01                |
    | sbb qword [rax + 1 * rcx], 0x01              | 48 83 1c 08 01             |
    | sbb qword [rcx + 1 * rcx], 0x01              | 48 83 1c 09 01             |
    | sbb qword [rdx + 1 * rcx], 0x01              | 48 83 1c 0a 01             |
    | sbb qword [rbx + 1 * rcx], 0x01              | 48 83 1c 0b 01             |
    | sbb qword [rsp + 1 * rcx], 0x01              | 48 83 1c 0c 01             |
    | sbb qword [rbp + 1 * rcx], 0x01              | 48 83 5c 0d 00 01          |
    | sbb qword [rsi + 1 * rcx], 0x01              | 48 83 1c 0e 01             |
    | sbb qword [rdi + 1 * rcx], 0x01              | 48 83 1c 0f 01             |
    | sbb qword [r8 + 1 * rcx], 0x01               | 49 83 1c 08 01             |
    | sbb qword [r9 + 1 * rcx], 0x01               | 49 83 1c 09 01             |
    | sbb qword [r10 + 1 * rcx], 0x01              | 49 83 1c 0a 01             |
    | sbb qword [r11 + 1 * rcx], 0x01              | 49 83 1c 0b 01             |
    | sbb qword [r12 + 1 * rcx], 0x01              | 49 83 1c 0c 01             |
    | sbb qword [r13 + 1 * rcx], 0x01              | 49 83 5c 0d 00 01          |
    | sbb qword [r14 + 1 * rcx], 0x01              | 49 83 1c 0e 01             |
    | sbb qword [r15 + 1 * rcx], 0x01              | 49 83 1c 0f 01             |
    | sbb qword [rax + 1 * rax], 0x01              | 48 83 1c 00 01             |
    | sbb qword [rax + 1 * rdx], 0x01              | 48 83 1c 10 01             |
    | sbb qword [rax + 1 * rbx], 0x01              | 48 83 1c 18 01             |
    | sbb qword [rax + 1 * rbp], 0x01              | 48 83 1c 28 01             |
    | sbb qword [rax + 1 * rsi], 0x01              | 48 83 1c 30 01             |
    | sbb qword [rax + 1 * rdi], 0x01              | 48 83 1c 38 01             |
    | sbb qword [rax + 1 * r8], 0x01               | 4a 83 1c 00 01             |
    | sbb qword [rax + 1 * r9], 0x01               | 4a 83 1c 08 01             |
    | sbb qword [rax + 1 * r10], 0x01              | 4a 83 1c 10 01             |
    | sbb qword [rax + 1 * r11], 0x01              | 4a 83 1c 18 01             |
    | sbb qword [rax + 1 * r12], 0x01              | 4a 83 1c 20 01             |
    | sbb qword [rax + 1 * r13], 0x01              | 4a 83 1c 28 01             |
    | sbb qword [rax + 1 * r14], 0x01              | 4a 83 1c 30 01             |
    | sbb qword [rax + 1 * r15], 0x01              | 4a 83 1c 38 01             |
    | sbb qword [rax + 2 * rcx], 0x01              | 48 83 1c 48 01             |
    | sbb qword [rax + 4 * rcx], 0x01              | 48 83 1c 88 01             |
    | sbb qword [rax + 8 * rcx], 0x01              | 48 83 1c c8 01             |
    | sbb qword [r8 + 1 * r9], 0x01                | 4b 83 1c 08 01             |
    | sbb qword [r8 + 2 * r9], 0x01                | 4b 83 1c 48 01             |
    | sbb qword [r8 + 4 * r9], 0x01                | 4b 83 1c 88 01             |
    | sbb qword [r8 + 8 * r9], 0x01                | 4b 83 1c c8 01             |
    | sbb qword [1 * rcx], 0x01                    | 48 83 1c 0d 00 00 00 00 01 |
    | sbb qword [2 * rcx], 0x01                    | 48 83 1c 4d 00 00 00 00 01 |
    | sbb qword [4 * rcx], 0x01                    | 48 83 1c 8d 00 00 00 00 01 |
    | sbb qword [8 * rcx], 0x01                    | 48 83 1c cd 00 00 00 00 01 |
    | sbb qword [1 * r9], 0x01                     | 4a 83 1c 0d 00 00 00 00 01 |
    | sbb qword [2 * r9], 0x01                     | 4a 83 1c 4d 00 00 00 00 01 |
    | sbb qword [4 * r9], 0x01                     | 4a 83 1c 8d 00 00 00 00 01 |
    | sbb qword [8 * r9], 0x01                     | 4a 83 1c cd 00 00 00 00 01 |
    | sbb qword [r13 + 8 * r12], 0x01              | 4b 83 5c e5 00 01          |
    | sbb qword [rsp + 4 * r15], 0x01              | 4a 83 1c bc 01             |
    | sbb qword [rax + 1 * rcx + 0x00], 0x01       | 48 83 5c 08 00 01          |
    | sbb qword [rax + 1 * rcx - 0x00], 0x01       | 48 83 5c 08 00 01          |
    | sbb qword [rax + 1 * rcx + 0x01], 0x01       | 48 83 5c 08 01 01          |
    | sbb qword [rax + 1 * rcx - 0x01], 0x01       | 48 83 5c 08 ff 01          |
    | sbb qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 83 9c 08 01 00 00 00 01 |
    | sbb qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 83 9c 08 ff ff ff ff 01 |
    | sbb qword [rax + 1 * rcx + 0x7f], 0x01       | 48 83 5c 08 7f 01          |
    | sbb qword [rax + 1 * rcx - 0x7f], 0x01       | 48 83 5c 08 81 01          |
    | sbb qword [rax + 1 * rcx + 0x80], 0x01       | 48 83 9c 08 80 00 00 00 01 |
    | sbb qword [rax + 1 * rcx - 0x80], 0x01       | 48 83 5c 08 80 01          |
    | sbb qword [rax + 1 * rcx - 0x81], 0x01       | 48 83 9c 08 7f ff ff ff 01 |
    | sbb qword [rax + 1 * rcx + 0xff], 0x01       | 48 83 9c 08 ff 00 00 00 01 |
    | sbb qword [rax + 1 * rcx - 0xff], 0x01       | 48 83 9c 08 01 ff ff ff 01 |
    | sbb qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 83 9c 08 ff ff ff 7f 01 |
    | sbb qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 83 9c 08 01 00 00 80 01 |
    | sbb qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 83 9c 08 00 00 00 80 01 |
    | sbb qword [r10 + 0x7f], 0x01                 | 49 83 5a 7f 01             |
    | sbb qword [r10 + 0x80], 0x01                 | 49 83 9a 80 00 00 00 01    |
    | sbb qword [r10 - 0x80], 0x01                 | 49 83 5a 80 01             |
    | sbb qword [r10 - 0x81], 0x01                 | 49 83 9a 7f ff ff ff 01    |
    | sbb qword [rax], 0x00                        | 48 83 18 00                |
    | sbb qword [rax], 0x7f                        | 48 83 18 7f                |
    | sbb qword [rax], 0x80                        | 48 83 18 80                |
    | sbb qword [rax], 0xff                        | 48 83 18 ff                |
    | sbb qword [rcx], 0x7f                        | 48 83 19 7f                |
    | sbb qword [rdx], 0x80                        | 48 83 1a 80                |
    | sbb qword [rbx], 0xff                        | 48 83 1b ff                |
    | sbb qword [rsp], 0x00                        | 48 83 1c 24 00             |
    | sbb qword [rsi], 0x7f                        | 48 83 1e 7f                |
    | sbb qword [rdi], 0x80                        | 48 83 1f 80                |
    | sbb qword [r8], 0xff                         | 49 83 18 ff                |
    | sbb qword [r9], 0x00                         | 49 83 19 00                |
    | sbb qword [r11], 0x7f                        | 49 83 1b 7f                |
    | sbb qword [r12], 0x80                        | 49 83 1c 24 80             |
    | sbb qword [r13], 0xff                        | 49 83 5d 00 ff             |
    | sbb qword [r14], 0x00                        | 49 83 1e 00                |
    | sbb qword [rax + 1 * rcx], 0x7f              | 48 83 1c 08 7f             |
    | sbb qword [rcx + 1 * rcx], 0x80              | 48 83 1c 09 80             |
    | sbb qword [rdx + 1 * rcx], 0xff              | 48 83 1c 0a ff             |
    | sbb qword [rbx + 1 * rcx], 0x00              | 48 83 1c 0b 00             |
    | sbb qword [rbp + 1 * rcx], 0x7f              | 48 83 5c 0d 00 7f          |
    | sbb qword [rsi + 1 * rcx], 0x80              | 48 83 1c 0e 80             |
    | sbb qword [rdi + 1 * rcx], 0xff              | 48 83 1c 0f ff             |
    | sbb qword [r8 + 1 * rcx], 0x00               | 49 83 1c 08 00             |
    | sbb qword [r10 + 1 * rcx], 0x7f              | 49 83 1c 0a 7f             |
    | sbb qword [r11 + 1 * rcx], 0x80              | 49 83 1c 0b 80             |
    | sbb qword [r12 + 1 * rcx], 0xff              | 49 83 1c 0c ff             |
    | sbb qword [r13 + 1 * rcx], 0x00              | 49 83 5c 0d 00 00          |
    | sbb qword [r15 + 1 * rcx], 0x7f              | 49 83 1c 0f 7f             |
    | sbb qword [rax + 1 * rax], 0x80              | 48 83 1c 00 80             |
    | sbb qword [rax + 1 * rdx], 0xff              | 48 83 1c 10 ff             |
    | sbb qword [rax + 1 * rbx], 0x00              | 48 83 1c 18 00             |
    | sbb qword [rax + 1 * rsi], 0x7f              | 48 83 1c 30 7f             |
    | sbb qword [rax + 1 * rdi], 0x80              | 48 83 1c 38 80             |
    | sbb qword [rax + 1 * r8], 0xff               | 4a 83 1c 00 ff             |
    | sbb qword [rax + 1 * r9], 0x00               | 4a 83 1c 08 00             |
    | sbb qword [rax + 1 * r11], 0x7f              | 4a 83 1c 18 7f             |
    | sbb qword [rax + 1 * r12], 0x80              | 4a 83 1c 20 80             |
    | sbb qword [rax + 1 * r13], 0xff              | 4a 83 1c 28 ff             |
    | sbb qword [rax + 1 * r14], 0x00              | 4a 83 1c 30 00             |
    | sbb qword [rax + 2 * rcx], 0x7f              | 48 83 1c 48 7f             |
    | sbb qword [rax + 4 * rcx], 0x80              | 48 83 1c 88 80             |
    | sbb qword [rax + 8 * rcx], 0xff              | 48 83 1c c8 ff             |
    | sbb qword [r8 + 1 * r9], 0x00                | 4b 83 1c 08 00             |
    | sbb qword [r8 + 4 * r9], 0x7f                | 4b 83 1c 88 7f             |
    | sbb qword [r8 + 8 * r9], 0x80                | 4b 83 1c c8 80             |
    | sbb qword [1 * rcx], 0xff                    | 48 83 1c 0d 00 00 00 00 ff |
    | sbb qword [2 * rcx], 0x00                    | 48 83 1c 4d 00 00 00 00 00 |
    | sbb qword [8 * rcx], 0x7f                    | 48 83 1c cd 00 00 00 00 7f |
    | sbb qword [1 * r9], 0x80                     | 4a 83 1c 0d 00 00 00 00 80 |
    | sbb qword [2 * r9], 0xff                     | 4a 83 1c 4d 00 00 00 00 ff |
    | sbb qword [4 * r9], 0x00                     | 4a 83 1c 8d 00 00 00 00 00 |
    | sbb qword [r13 + 8 * r12], 0x7f              | 4b 83 5c e5 00 7f          |
    | sbb qword [rsp + 4 * r15], 0x80              | 4a 83 1c bc 80             |
    | sbb qword [rax + 1 * rcx + 0x00], 0xff       | 48 83 5c 08 00 ff          |
    | sbb qword [rax + 1 * rcx - 0x00], 0x00       | 48 83 5c 08 00 00          |
    | sbb qword [rax + 1 * rcx - 0x01], 0x7f       | 48 83 5c 08 ff 7f          |
    | sbb qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 83 9c 08 01 00 00 00 80 |
    | sbb qword [rax + 1 * rcx - 0x00000001], 0xff | 48 83 9c 08 ff ff ff ff ff |
    | sbb qword [rax + 1 * rcx + 0x7f], 0x00       | 48 83 5c 08 7f 00          |
    | sbb qword [rax + 1 * rcx + 0x80], 0x7f       | 48 83 9c 08 80 00 00 00 7f |
    | sbb qword [rax + 1 * rcx - 0x80], 0x80       | 48 83 5c 08 80 80          |
    | sbb qword [rax + 1 * rcx - 0x81], 0xff       | 48 83 9c 08 7f ff ff ff ff |
    | sbb qword [rax + 1 * rcx + 0xff], 0x00       | 48 83 9c 08 ff 00 00 00 00 |
    | sbb qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 83 9c 08 ff ff ff 7f 7f |
    | sbb qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 83 9c 08 01 00 00 80 80 |
    | sbb qword [rax + 1 * rcx - 0x80000000], 0xff | 48 83 9c 08 00 00 00 80 ff |
    | sbb qword [r10 + 0x7f], 0x00                 | 49 83 5a 7f 00             |
    | sbb qword [r10 - 0x80], 0x7f                 | 49 83 5a 80 7f             |
    | sbb qword [r10 - 0x81], 0x80                 | 49 83 9a 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sbb_addr64_imm8():
    encode(SBB_ADDR64_IMM8)


SBB_ADDR64_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | sbb qword [rax], 0x00000001                        | 48 81 18 01 00 00 00                |
    | sbb qword [rcx], 0x00000001                        | 48 81 19 01 00 00 00                |
    | sbb qword [rdx], 0x00000001                        | 48 81 1a 01 00 00 00                |
    | sbb qword [rbx], 0x00000001                        | 48 81 1b 01 00 00 00                |
    | sbb qword [rsp], 0x00000001                        | 48 81 1c 24 01 00 00 00             |
    | sbb qword [rbp], 0x00000001                        | 48 81 5d 00 01 00 00 00             |
    | sbb qword [rsi], 0x00000001                        | 48 81 1e 01 00 00 00                |
    | sbb qword [rdi], 0x00000001                        | 48 81 1f 01 00 00 00                |
    | sbb qword [r8], 0x00000001                         | 49 81 18 01 00 00 00                |
    | sbb qword [r9], 0x00000001                         | 49 81 19 01 00 00 00                |
    | sbb qword [r10], 0x00000001                        | 49 81 1a 01 00 00 00                |
    | sbb qword [r11], 0x00000001                        | 49 81 1b 01 00 00 00                |
    | sbb qword [r12], 0x00000001                        | 49 81 1c 24 01 00 00 00             |
    | sbb qword [r13], 0x00000001                        | 49 81 5d 00 01 00 00 00             |
    | sbb qword [r14], 0x00000001                        | 49 81 1e 01 00 00 00                |
    | sbb qword [r15], 0x00000001                        | 49 81 1f 01 00 00 00                |
    | sbb qword [rax + 1 * rcx], 0x00000001              | 48 81 1c 08 01 00 00 00             |
    | sbb qword [rcx + 1 * rcx], 0x00000001              | 48 81 1c 09 01 00 00 00             |
    | sbb qword [rdx + 1 * rcx], 0x00000001              | 48 81 1c 0a 01 00 00 00             |
    | sbb qword [rbx + 1 * rcx], 0x00000001              | 48 81 1c 0b 01 00 00 00             |
    | sbb qword [rsp + 1 * rcx], 0x00000001              | 48 81 1c 0c 01 00 00 00             |
    | sbb qword [rbp + 1 * rcx], 0x00000001              | 48 81 5c 0d 00 01 00 00 00          |
    | sbb qword [rsi + 1 * rcx], 0x00000001              | 48 81 1c 0e 01 00 00 00             |
    | sbb qword [rdi + 1 * rcx], 0x00000001              | 48 81 1c 0f 01 00 00 00             |
    | sbb qword [r8 + 1 * rcx], 0x00000001               | 49 81 1c 08 01 00 00 00             |
    | sbb qword [r9 + 1 * rcx], 0x00000001               | 49 81 1c 09 01 00 00 00             |
    | sbb qword [r10 + 1 * rcx], 0x00000001              | 49 81 1c 0a 01 00 00 00             |
    | sbb qword [r11 + 1 * rcx], 0x00000001              | 49 81 1c 0b 01 00 00 00             |
    | sbb qword [r12 + 1 * rcx], 0x00000001              | 49 81 1c 0c 01 00 00 00             |
    | sbb qword [r13 + 1 * rcx], 0x00000001              | 49 81 5c 0d 00 01 00 00 00          |
    | sbb qword [r14 + 1 * rcx], 0x00000001              | 49 81 1c 0e 01 00 00 00             |
    | sbb qword [r15 + 1 * rcx], 0x00000001              | 49 81 1c 0f 01 00 00 00             |
    | sbb qword [rax + 1 * rax], 0x00000001              | 48 81 1c 00 01 00 00 00             |
    | sbb qword [rax + 1 * rdx], 0x00000001              | 48 81 1c 10 01 00 00 00             |
    | sbb qword [rax + 1 * rbx], 0x00000001              | 48 81 1c 18 01 00 00 00             |
    | sbb qword [rax + 1 * rbp], 0x00000001              | 48 81 1c 28 01 00 00 00             |
    | sbb qword [rax + 1 * rsi], 0x00000001              | 48 81 1c 30 01 00 00 00             |
    | sbb qword [rax + 1 * rdi], 0x00000001              | 48 81 1c 38 01 00 00 00             |
    | sbb qword [rax + 1 * r8], 0x00000001               | 4a 81 1c 00 01 00 00 00             |
    | sbb qword [rax + 1 * r9], 0x00000001               | 4a 81 1c 08 01 00 00 00             |
    | sbb qword [rax + 1 * r10], 0x00000001              | 4a 81 1c 10 01 00 00 00             |
    | sbb qword [rax + 1 * r11], 0x00000001              | 4a 81 1c 18 01 00 00 00             |
    | sbb qword [rax + 1 * r12], 0x00000001              | 4a 81 1c 20 01 00 00 00             |
    | sbb qword [rax + 1 * r13], 0x00000001              | 4a 81 1c 28 01 00 00 00             |
    | sbb qword [rax + 1 * r14], 0x00000001              | 4a 81 1c 30 01 00 00 00             |
    | sbb qword [rax + 1 * r15], 0x00000001              | 4a 81 1c 38 01 00 00 00             |
    | sbb qword [rax + 2 * rcx], 0x00000001              | 48 81 1c 48 01 00 00 00             |
    | sbb qword [rax + 4 * rcx], 0x00000001              | 48 81 1c 88 01 00 00 00             |
    | sbb qword [rax + 8 * rcx], 0x00000001              | 48 81 1c c8 01 00 00 00             |
    | sbb qword [r8 + 1 * r9], 0x00000001                | 4b 81 1c 08 01 00 00 00             |
    | sbb qword [r8 + 2 * r9], 0x00000001                | 4b 81 1c 48 01 00 00 00             |
    | sbb qword [r8 + 4 * r9], 0x00000001                | 4b 81 1c 88 01 00 00 00             |
    | sbb qword [r8 + 8 * r9], 0x00000001                | 4b 81 1c c8 01 00 00 00             |
    | sbb qword [1 * rcx], 0x00000001                    | 48 81 1c 0d 00 00 00 00 01 00 00 00 |
    | sbb qword [2 * rcx], 0x00000001                    | 48 81 1c 4d 00 00 00 00 01 00 00 00 |
    | sbb qword [4 * rcx], 0x00000001                    | 48 81 1c 8d 00 00 00 00 01 00 00 00 |
    | sbb qword [8 * rcx], 0x00000001                    | 48 81 1c cd 00 00 00 00 01 00 00 00 |
    | sbb qword [1 * r9], 0x00000001                     | 4a 81 1c 0d 00 00 00 00 01 00 00 00 |
    | sbb qword [2 * r9], 0x00000001                     | 4a 81 1c 4d 00 00 00 00 01 00 00 00 |
    | sbb qword [4 * r9], 0x00000001                     | 4a 81 1c 8d 00 00 00 00 01 00 00 00 |
    | sbb qword [8 * r9], 0x00000001                     | 4a 81 1c cd 00 00 00 00 01 00 00 00 |
    | sbb qword [r13 + 8 * r12], 0x00000001              | 4b 81 5c e5 00 01 00 00 00          |
    | sbb qword [rsp + 4 * r15], 0x00000001              | 4a 81 1c bc 01 00 00 00             |
    | sbb qword [rax + 1 * rcx + 0x00], 0x00000001       | 48 81 5c 08 00 01 00 00 00          |
    | sbb qword [rax + 1 * rcx - 0x00], 0x00000001       | 48 81 5c 08 00 01 00 00 00          |
    | sbb qword [rax + 1 * rcx + 0x01], 0x00000001       | 48 81 5c 08 01 01 00 00 00          |
    | sbb qword [rax + 1 * rcx - 0x01], 0x00000001       | 48 81 5c 08 ff 01 00 00 00          |
    | sbb qword [rax + 1 * rcx + 0x00000001], 0x00000001 | 48 81 9c 08 01 00 00 00 01 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x00000001], 0x00000001 | 48 81 9c 08 ff ff ff ff 01 00 00 00 |
    | sbb qword [rax + 1 * rcx + 0x7f], 0x00000001       | 48 81 5c 08 7f 01 00 00 00          |
    | sbb qword [rax + 1 * rcx - 0x7f], 0x00000001       | 48 81 5c 08 81 01 00 00 00          |
    | sbb qword [rax + 1 * rcx + 0x80], 0x00000001       | 48 81 9c 08 80 00 00 00 01 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x80], 0x00000001       | 48 81 5c 08 80 01 00 00 00          |
    | sbb qword [rax + 1 * rcx - 0x81], 0x00000001       | 48 81 9c 08 7f ff ff ff 01 00 00 00 |
    | sbb qword [rax + 1 * rcx + 0xff], 0x00000001       | 48 81 9c 08 ff 00 00 00 01 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0xff], 0x00000001       | 48 81 9c 08 01 ff ff ff 01 00 00 00 |
    | sbb qword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 48 81 9c 08 ff ff ff 7f 01 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 48 81 9c 08 01 00 00 80 01 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x80000000], 0x00000001 | 48 81 9c 08 00 00 00 80 01 00 00 00 |
    | sbb qword [r10 + 0x7f], 0x00000001                 | 49 81 5a 7f 01 00 00 00             |
    | sbb qword [r10 + 0x80], 0x00000001                 | 49 81 9a 80 00 00 00 01 00 00 00    |
    | sbb qword [r10 - 0x80], 0x00000001                 | 49 81 5a 80 01 00 00 00             |
    | sbb qword [r10 - 0x81], 0x00000001                 | 49 81 9a 7f ff ff ff 01 00 00 00    |
    | sbb qword [rax], 0x00000000                        | 48 81 18 00 00 00 00                |
    | sbb qword [rax], 0x0000007f                        | 48 81 18 7f 00 00 00                |
    | sbb qword [rax], 0x00000080                        | 48 81 18 80 00 00 00                |
    | sbb qword [rax], 0x000000ff                        | 48 81 18 ff 00 00 00                |
    | sbb qword [rax], 0x00000100                        | 48 81 18 00 01 00 00                |
    | sbb qword [rax], 0x00007fff                        | 48 81 18 ff 7f 00 00                |
    | sbb qword [rax], 0x00008000                        | 48 81 18 00 80 00 00                |
    | sbb qword [rax], 0x0000ffff                        | 48 81 18 ff ff 00 00                |
    | sbb qword [rax], 0x00010000                        | 48 81 18 00 00 01 00                |
    | sbb qword [rax], 0x7fffffff                        | 48 81 18 ff ff ff 7f                |
    | sbb qword [rax], 0x80000000                        | 48 81 18 00 00 00 80                |
    | sbb qword [rax], 0xffffffff                        | 48 81 18 ff ff ff ff                |
    | sbb qword [rcx], 0x0000007f                        | 48 81 19 7f 00 00 00                |
    | sbb qword [rdx], 0x00000080                        | 48 81 1a 80 00 00 00                |
    | sbb qword [rbx], 0x000000ff                        | 48 81 1b ff 00 00 00                |
    | sbb qword [rsp], 0x00000100                        | 48 81 1c 24 00 01 00 00             |
    | sbb qword [rbp], 0x00007fff                        | 48 81 5d 00 ff 7f 00 00             |
    | sbb qword [rsi], 0x00008000                        | 48 81 1e 00 80 00 00                |
    | sbb qword [rdi], 0x0000ffff                        | 48 81 1f ff ff 00 00                |
    | sbb qword [r8], 0x00010000                         | 49 81 18 00 00 01 00                |
    | sbb qword [r9], 0x7fffffff                         | 49 81 19 ff ff ff 7f                |
    | sbb qword [r10], 0x80000000                        | 49 81 1a 00 00 00 80                |
    | sbb qword [r11], 0xffffffff                        | 49 81 1b ff ff ff ff                |
    | sbb qword [r12], 0x00000000                        | 49 81 1c 24 00 00 00 00             |
    | sbb qword [r14], 0x0000007f                        | 49 81 1e 7f 00 00 00                |
    | sbb qword [r15], 0x00000080                        | 49 81 1f 80 00 00 00                |
    | sbb qword [rax + 1 * rcx], 0x000000ff              | 48 81 1c 08 ff 00 00 00             |
    | sbb qword [rcx + 1 * rcx], 0x00000100              | 48 81 1c 09 00 01 00 00             |
    | sbb qword [rdx + 1 * rcx], 0x00007fff              | 48 81 1c 0a ff 7f 00 00             |
    | sbb qword [rbx + 1 * rcx], 0x00008000              | 48 81 1c 0b 00 80 00 00             |
    | sbb qword [rsp + 1 * rcx], 0x0000ffff              | 48 81 1c 0c ff ff 00 00             |
    | sbb qword [rbp + 1 * rcx], 0x00010000              | 48 81 5c 0d 00 00 00 01 00          |
    | sbb qword [rsi + 1 * rcx], 0x7fffffff              | 48 81 1c 0e ff ff ff 7f             |
    | sbb qword [rdi + 1 * rcx], 0x80000000              | 48 81 1c 0f 00 00 00 80             |
    | sbb qword [r8 + 1 * rcx], 0xffffffff               | 49 81 1c 08 ff ff ff ff             |
    | sbb qword [r9 + 1 * rcx], 0x00000000               | 49 81 1c 09 00 00 00 00             |
    | sbb qword [r11 + 1 * rcx], 0x0000007f              | 49 81 1c 0b 7f 00 00 00             |
    | sbb qword [r12 + 1 * rcx], 0x00000080              | 49 81 1c 0c 80 00 00 00             |
    | sbb qword [r13 + 1 * rcx], 0x000000ff              | 49 81 5c 0d 00 ff 00 00 00          |
    | sbb qword [r14 + 1 * rcx], 0x00000100              | 49 81 1c 0e 00 01 00 00             |
    | sbb qword [r15 + 1 * rcx], 0x00007fff              | 49 81 1c 0f ff 7f 00 00             |
    | sbb qword [rax + 1 * rax], 0x00008000              | 48 81 1c 00 00 80 00 00             |
    | sbb qword [rax + 1 * rdx], 0x0000ffff              | 48 81 1c 10 ff ff 00 00             |
    | sbb qword [rax + 1 * rbx], 0x00010000              | 48 81 1c 18 00 00 01 00             |
    | sbb qword [rax + 1 * rbp], 0x7fffffff              | 48 81 1c 28 ff ff ff 7f             |
    | sbb qword [rax + 1 * rsi], 0x80000000              | 48 81 1c 30 00 00 00 80             |
    | sbb qword [rax + 1 * rdi], 0xffffffff              | 48 81 1c 38 ff ff ff ff             |
    | sbb qword [rax + 1 * r8], 0x00000000               | 4a 81 1c 00 00 00 00 00             |
    | sbb qword [rax + 1 * r10], 0x0000007f              | 4a 81 1c 10 7f 00 00 00             |
    | sbb qword [rax + 1 * r11], 0x00000080              | 4a 81 1c 18 80 00 00 00             |
    | sbb qword [rax + 1 * r12], 0x000000ff              | 4a 81 1c 20 ff 00 00 00             |
    | sbb qword [rax + 1 * r13], 0x00000100              | 4a 81 1c 28 00 01 00 00             |
    | sbb qword [rax + 1 * r14], 0x00007fff              | 4a 81 1c 30 ff 7f 00 00             |
    | sbb qword [rax + 1 * r15], 0x00008000              | 4a 81 1c 38 00 80 00 00             |
    | sbb qword [rax + 2 * rcx], 0x0000ffff              | 48 81 1c 48 ff ff 00 00             |
    | sbb qword [rax + 4 * rcx], 0x00010000              | 48 81 1c 88 00 00 01 00             |
    | sbb qword [rax + 8 * rcx], 0x7fffffff              | 48 81 1c c8 ff ff ff 7f             |
    | sbb qword [r8 + 1 * r9], 0x80000000                | 4b 81 1c 08 00 00 00 80             |
    | sbb qword [r8 + 2 * r9], 0xffffffff                | 4b 81 1c 48 ff ff ff ff             |
    | sbb qword [r8 + 4 * r9], 0x00000000                | 4b 81 1c 88 00 00 00 00             |
    | sbb qword [1 * rcx], 0x0000007f                    | 48 81 1c 0d 00 00 00 00 7f 00 00 00 |
    | sbb qword [2 * rcx], 0x00000080                    | 48 81 1c 4d 00 00 00 00 80 00 00 00 |
    | sbb qword [4 * rcx], 0x000000ff                    | 48 81 1c 8d 00 00 00 00 ff 00 00 00 |
    | sbb qword [8 * rcx], 0x00000100                    | 48 81 1c cd 00 00 00 00 00 01 00 00 |
    | sbb qword [1 * r9], 0x00007fff                     | 4a 81 1c 0d 00 00 00 00 ff 7f 00 00 |
    | sbb qword [2 * r9], 0x00008000                     | 4a 81 1c 4d 00 00 00 00 00 80 00 00 |
    | sbb qword [4 * r9], 0x0000ffff                     | 4a 81 1c 8d 00 00 00 00 ff ff 00 00 |
    | sbb qword [8 * r9], 0x00010000                     | 4a 81 1c cd 00 00 00 00 00 00 01 00 |
    | sbb qword [r13 + 8 * r12], 0x7fffffff              | 4b 81 5c e5 00 ff ff ff 7f          |
    | sbb qword [rsp + 4 * r15], 0x80000000              | 4a 81 1c bc 00 00 00 80             |
    | sbb qword [rax + 1 * rcx + 0x00], 0xffffffff       | 48 81 5c 08 00 ff ff ff ff          |
    | sbb qword [rax + 1 * rcx - 0x00], 0x00000000       | 48 81 5c 08 00 00 00 00 00          |
    | sbb qword [rax + 1 * rcx - 0x01], 0x0000007f       | 48 81 5c 08 ff 7f 00 00 00          |
    | sbb qword [rax + 1 * rcx + 0x00000001], 0x00000080 | 48 81 9c 08 01 00 00 00 80 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x00000001], 0x000000ff | 48 81 9c 08 ff ff ff ff ff 00 00 00 |
    | sbb qword [rax + 1 * rcx + 0x7f], 0x00000100       | 48 81 5c 08 7f 00 01 00 00          |
    | sbb qword [rax + 1 * rcx - 0x7f], 0x00007fff       | 48 81 5c 08 81 ff 7f 00 00          |
    | sbb qword [rax + 1 * rcx + 0x80], 0x00008000       | 48 81 9c 08 80 00 00 00 00 80 00 00 |
    | sbb qword [rax + 1 * rcx - 0x80], 0x0000ffff       | 48 81 5c 08 80 ff ff 00 00          |
    | sbb qword [rax + 1 * rcx - 0x81], 0x00010000       | 48 81 9c 08 7f ff ff ff 00 00 01 00 |
    | sbb qword [rax + 1 * rcx + 0xff], 0x7fffffff       | 48 81 9c 08 ff 00 00 00 ff ff ff 7f |
    | sbb qword [rax + 1 * rcx - 0xff], 0x80000000       | 48 81 9c 08 01 ff ff ff 00 00 00 80 |
    | sbb qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 48 81 9c 08 ff ff ff 7f ff ff ff ff |
    | sbb qword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 48 81 9c 08 01 00 00 80 00 00 00 00 |
    | sbb qword [r10 + 0x7f], 0x0000007f                 | 49 81 5a 7f 7f 00 00 00             |
    | sbb qword [r10 + 0x80], 0x00000080                 | 49 81 9a 80 00 00 00 80 00 00 00    |
    | sbb qword [r10 - 0x80], 0x000000ff                 | 49 81 5a 80 ff 00 00 00             |
    | sbb qword [r10 - 0x81], 0x00000100                 | 49 81 9a 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_sbb_addr64_imm32():
    encode(SBB_ADDR64_IMM32)


SBB_ADDR64_REG64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | sbb qword [rax], rcx                        | 48 19 08                |
    | sbb qword [rcx], rcx                        | 48 19 09                |
    | sbb qword [rdx], rcx                        | 48 19 0a                |
    | sbb qword [rbx], rcx                        | 48 19 0b                |
    | sbb qword [rsp], rcx                        | 48 19 0c 24             |
    | sbb qword [rbp], rcx                        | 48 19 4d 00             |
    | sbb qword [rsi], rcx                        | 48 19 0e                |
    | sbb qword [rdi], rcx                        | 48 19 0f                |
    | sbb qword [r8], rcx                         | 49 19 08                |
    | sbb qword [r9], rcx                         | 49 19 09                |
    | sbb qword [r10], rcx                        | 49 19 0a                |
    | sbb qword [r11], rcx                        | 49 19 0b                |
    | sbb qword [r12], rcx                        | 49 19 0c 24             |
    | sbb qword [r13], rcx                        | 49 19 4d 00             |
    | sbb qword [r14], rcx                        | 49 19 0e                |
    | sbb qword [r15], rcx                        | 49 19 0f                |
    | sbb qword [rax + 1 * rcx], rcx              | 48 19 0c 08             |
    | sbb qword [rcx + 1 * rcx], rcx              | 48 19 0c 09             |
    | sbb qword [rdx + 1 * rcx], rcx              | 48 19 0c 0a             |
    | sbb qword [rbx + 1 * rcx], rcx              | 48 19 0c 0b             |
    | sbb qword [rsp + 1 * rcx], rcx              | 48 19 0c 0c             |
    | sbb qword [rbp + 1 * rcx], rcx              | 48 19 4c 0d 00          |
    | sbb qword [rsi + 1 * rcx], rcx              | 48 19 0c 0e             |
    | sbb qword [rdi + 1 * rcx], rcx              | 48 19 0c 0f             |
    | sbb qword [r8 + 1 * rcx], rcx               | 49 19 0c 08             |
    | sbb qword [r9 + 1 * rcx], rcx               | 49 19 0c 09             |
    | sbb qword [r10 + 1 * rcx], rcx              | 49 19 0c 0a             |
    | sbb qword [r11 + 1 * rcx], rcx              | 49 19 0c 0b             |
    | sbb qword [r12 + 1 * rcx], rcx              | 49 19 0c 0c             |
    | sbb qword [r13 + 1 * rcx], rcx              | 49 19 4c 0d 00          |
    | sbb qword [r14 + 1 * rcx], rcx              | 49 19 0c 0e             |
    | sbb qword [r15 + 1 * rcx], rcx              | 49 19 0c 0f             |
    | sbb qword [rax + 1 * rax], rcx              | 48 19 0c 00             |
    | sbb qword [rax + 1 * rdx], rcx              | 48 19 0c 10             |
    | sbb qword [rax + 1 * rbx], rcx              | 48 19 0c 18             |
    | sbb qword [rax + 1 * rbp], rcx              | 48 19 0c 28             |
    | sbb qword [rax + 1 * rsi], rcx              | 48 19 0c 30             |
    | sbb qword [rax + 1 * rdi], rcx              | 48 19 0c 38             |
    | sbb qword [rax + 1 * r8], rcx               | 4a 19 0c 00             |
    | sbb qword [rax + 1 * r9], rcx               | 4a 19 0c 08             |
    | sbb qword [rax + 1 * r10], rcx              | 4a 19 0c 10             |
    | sbb qword [rax + 1 * r11], rcx              | 4a 19 0c 18             |
    | sbb qword [rax + 1 * r12], rcx              | 4a 19 0c 20             |
    | sbb qword [rax + 1 * r13], rcx              | 4a 19 0c 28             |
    | sbb qword [rax + 1 * r14], rcx              | 4a 19 0c 30             |
    | sbb qword [rax + 1 * r15], rcx              | 4a 19 0c 38             |
    | sbb qword [rax + 2 * rcx], rcx              | 48 19 0c 48             |
    | sbb qword [rax + 4 * rcx], rcx              | 48 19 0c 88             |
    | sbb qword [rax + 8 * rcx], rcx              | 48 19 0c c8             |
    | sbb qword [r8 + 1 * r9], rcx                | 4b 19 0c 08             |
    | sbb qword [r8 + 2 * r9], rcx                | 4b 19 0c 48             |
    | sbb qword [r8 + 4 * r9], rcx                | 4b 19 0c 88             |
    | sbb qword [r8 + 8 * r9], rcx                | 4b 19 0c c8             |
    | sbb qword [1 * rcx], rcx                    | 48 19 0c 0d 00 00 00 00 |
    | sbb qword [2 * rcx], rcx                    | 48 19 0c 4d 00 00 00 00 |
    | sbb qword [4 * rcx], rcx                    | 48 19 0c 8d 00 00 00 00 |
    | sbb qword [8 * rcx], rcx                    | 48 19 0c cd 00 00 00 00 |
    | sbb qword [1 * r9], rcx                     | 4a 19 0c 0d 00 00 00 00 |
    | sbb qword [2 * r9], rcx                     | 4a 19 0c 4d 00 00 00 00 |
    | sbb qword [4 * r9], rcx                     | 4a 19 0c 8d 00 00 00 00 |
    | sbb qword [8 * r9], rcx                     | 4a 19 0c cd 00 00 00 00 |
    | sbb qword [r13 + 8 * r12], rcx              | 4b 19 4c e5 00          |
    | sbb qword [rsp + 4 * r15], rcx              | 4a 19 0c bc             |
    | sbb qword [rax + 1 * rcx + 0x00], rcx       | 48 19 4c 08 00          |
    | sbb qword [rax + 1 * rcx - 0x00], rcx       | 48 19 4c 08 00          |
    | sbb qword [rax + 1 * rcx + 0x01], rcx       | 48 19 4c 08 01          |
    | sbb qword [rax + 1 * rcx - 0x01], rcx       | 48 19 4c 08 ff          |
    | sbb qword [rax + 1 * rcx + 0x00000001], rcx | 48 19 8c 08 01 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x00000001], rcx | 48 19 8c 08 ff ff ff ff |
    | sbb qword [rax + 1 * rcx + 0x7f], rcx       | 48 19 4c 08 7f          |
    | sbb qword [rax + 1 * rcx - 0x7f], rcx       | 48 19 4c 08 81          |
    | sbb qword [rax + 1 * rcx + 0x80], rcx       | 48 19 8c 08 80 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x80], rcx       | 48 19 4c 08 80          |
    | sbb qword [rax + 1 * rcx - 0x81], rcx       | 48 19 8c 08 7f ff ff ff |
    | sbb qword [rax + 1 * rcx + 0xff], rcx       | 48 19 8c 08 ff 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0xff], rcx       | 48 19 8c 08 01 ff ff ff |
    | sbb qword [rax + 1 * rcx + 0x7fffffff], rcx | 48 19 8c 08 ff ff ff 7f |
    | sbb qword [rax + 1 * rcx - 0x7fffffff], rcx | 48 19 8c 08 01 00 00 80 |
    | sbb qword [rax + 1 * rcx - 0x80000000], rcx | 48 19 8c 08 00 00 00 80 |
    | sbb qword [r10 + 0x7f], rcx                 | 49 19 4a 7f             |
    | sbb qword [r10 + 0x80], rcx                 | 49 19 8a 80 00 00 00    |
    | sbb qword [r10 - 0x80], rcx                 | 49 19 4a 80             |
    | sbb qword [r10 - 0x81], rcx                 | 49 19 8a 7f ff ff ff    |
    | sbb qword [rax], rax                        | 48 19 00                |
    | sbb qword [rax], rdx                        | 48 19 10                |
    | sbb qword [rax], rbx                        | 48 19 18                |
    | sbb qword [rax], rsp                        | 48 19 20                |
    | sbb qword [rax], rbp                        | 48 19 28                |
    | sbb qword [rax], rsi                        | 48 19 30                |
    | sbb qword [rax], rdi                        | 48 19 38                |
    | sbb qword [rax], r8                         | 4c 19 00                |
    | sbb qword [rax], r9                         | 4c 19 08                |
    | sbb qword [rax], r10                        | 4c 19 10                |
    | sbb qword [rax], r11                        | 4c 19 18                |
    | sbb qword [rax], r12                        | 4c 19 20                |
    | sbb qword [rax], r13                        | 4c 19 28                |
    | sbb qword [rax], r14                        | 4c 19 30                |
    | sbb qword [rax], r15                        | 4c 19 38                |
    | sbb qword [rcx], rdx                        | 48 19 11                |
    | sbb qword [rdx], rbx                        | 48 19 1a                |
    | sbb qword [rbx], rsp                        | 48 19 23                |
    | sbb qword [rsp], rbp                        | 48 19 2c 24             |
    | sbb qword [rbp], rsi                        | 48 19 75 00             |
    | sbb qword [rsi], rdi                        | 48 19 3e                |
    | sbb qword [rdi], r8                         | 4c 19 07                |
    | sbb qword [r8], r9                          | 4d 19 08                |
    | sbb qword [r9], r10                         | 4d 19 11                |
    | sbb qword [r10], r11                        | 4d 19 1a                |
    | sbb qword [r11], r12                        | 4d 19 23                |
    | sbb qword [r12], r13                        | 4d 19 2c 24             |
    | sbb qword [r13], r14                        | 4d 19 75 00             |
    | sbb qword [r14], r15                        | 4d 19 3e                |
    | sbb qword [r15], rax                        | 49 19 07                |
    | sbb qword [rcx + 1 * rcx], rdx              | 48 19 14 09             |
    | sbb qword [rdx + 1 * rcx], rbx              | 48 19 1c 0a             |
    | sbb qword [rbx + 1 * rcx], rsp              | 48 19 24 0b             |
    | sbb qword [rsp + 1 * rcx], rbp              | 48 19 2c 0c             |
    | sbb qword [rbp + 1 * rcx], rsi              | 48 19 74 0d 00          |
    | sbb qword [rsi + 1 * rcx], rdi              | 48 19 3c 0e             |
    | sbb qword [rdi + 1 * rcx], r8               | 4c 19 04 0f             |
    | sbb qword [r8 + 1 * rcx], r9                | 4d 19 0c 08             |
    | sbb qword [r9 + 1 * rcx], r10               | 4d 19 14 09             |
    | sbb qword [r10 + 1 * rcx], r11              | 4d 19 1c 0a             |
    | sbb qword [r11 + 1 * rcx], r12              | 4d 19 24 0b             |
    | sbb qword [r12 + 1 * rcx], r13              | 4d 19 2c 0c             |
    | sbb qword [r13 + 1 * rcx], r14              | 4d 19 74 0d 00          |
    | sbb qword [r14 + 1 * rcx], r15              | 4d 19 3c 0e             |
    | sbb qword [r15 + 1 * rcx], rax              | 49 19 04 0f             |
    | sbb qword [rax + 1 * rdx], rdx              | 48 19 14 10             |
    | sbb qword [rax + 1 * rbx], rbx              | 48 19 1c 18             |
    | sbb qword [rax + 1 * rbp], rsp              | 48 19 24 28             |
    | sbb qword [rax + 1 * rsi], rbp              | 48 19 2c 30             |
    | sbb qword [rax + 1 * rdi], rsi              | 48 19 34 38             |
    | sbb qword [rax + 1 * r8], rdi               | 4a 19 3c 00             |
    | sbb qword [rax + 1 * r9], r8                | 4e 19 04 08             |
    | sbb qword [rax + 1 * r10], r9               | 4e 19 0c 10             |
    | sbb qword [rax + 1 * r11], r10              | 4e 19 14 18             |
    | sbb qword [rax + 1 * r12], r11              | 4e 19 1c 20             |
    | sbb qword [rax + 1 * r13], r12              | 4e 19 24 28             |
    | sbb qword [rax + 1 * r14], r13              | 4e 19 2c 30             |
    | sbb qword [rax + 1 * r15], r14              | 4e 19 34 38             |
    | sbb qword [rax + 2 * rcx], r15              | 4c 19 3c 48             |
    | sbb qword [rax + 4 * rcx], rax              | 48 19 04 88             |
    | sbb qword [r8 + 1 * r9], rdx                | 4b 19 14 08             |
    | sbb qword [r8 + 2 * r9], rbx                | 4b 19 1c 48             |
    | sbb qword [r8 + 4 * r9], rsp                | 4b 19 24 88             |
    | sbb qword [r8 + 8 * r9], rbp                | 4b 19 2c c8             |
    | sbb qword [1 * rcx], rsi                    | 48 19 34 0d 00 00 00 00 |
    | sbb qword [2 * rcx], rdi                    | 48 19 3c 4d 00 00 00 00 |
    | sbb qword [4 * rcx], r8                     | 4c 19 04 8d 00 00 00 00 |
    | sbb qword [8 * rcx], r9                     | 4c 19 0c cd 00 00 00 00 |
    | sbb qword [1 * r9], r10                     | 4e 19 14 0d 00 00 00 00 |
    | sbb qword [2 * r9], r11                     | 4e 19 1c 4d 00 00 00 00 |
    | sbb qword [4 * r9], r12                     | 4e 19 24 8d 00 00 00 00 |
    | sbb qword [8 * r9], r13                     | 4e 19 2c cd 00 00 00 00 |
    | sbb qword [r13 + 8 * r12], r14              | 4f 19 74 e5 00          |
    | sbb qword [rsp + 4 * r15], r15              | 4e 19 3c bc             |
    | sbb qword [rax + 1 * rcx + 0x00], rax       | 48 19 44 08 00          |
    | sbb qword [rax + 1 * rcx + 0x01], rdx       | 48 19 54 08 01          |
    | sbb qword [rax + 1 * rcx - 0x01], rbx       | 48 19 5c 08 ff          |
    | sbb qword [rax + 1 * rcx + 0x00000001], rsp | 48 19 a4 08 01 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x00000001], rbp | 48 19 ac 08 ff ff ff ff |
    | sbb qword [rax + 1 * rcx + 0x7f], rsi       | 48 19 74 08 7f          |
    | sbb qword [rax + 1 * rcx - 0x7f], rdi       | 48 19 7c 08 81          |
    | sbb qword [rax + 1 * rcx + 0x80], r8        | 4c 19 84 08 80 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0x80], r9        | 4c 19 4c 08 80          |
    | sbb qword [rax + 1 * rcx - 0x81], r10       | 4c 19 94 08 7f ff ff ff |
    | sbb qword [rax + 1 * rcx + 0xff], r11       | 4c 19 9c 08 ff 00 00 00 |
    | sbb qword [rax + 1 * rcx - 0xff], r12       | 4c 19 a4 08 01 ff ff ff |
    | sbb qword [rax + 1 * rcx + 0x7fffffff], r13 | 4c 19 ac 08 ff ff ff 7f |
    | sbb qword [rax + 1 * rcx - 0x7fffffff], r14 | 4c 19 b4 08 01 00 00 80 |
    | sbb qword [rax + 1 * rcx - 0x80000000], r15 | 4c 19 bc 08 00 00 00 80 |
    | sbb qword [r10 + 0x7f], rax                 | 49 19 42 7f             |
    | sbb qword [r10 - 0x80], rdx                 | 49 19 52 80             |
    | sbb qword [r10 - 0x81], rbx                 | 49 19 9a 7f ff ff ff    |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_sbb_addr64_reg64():
    encode(SBB_ADDR64_REG64)


SBB_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sbb dword [rax], 0x01                        | 83 18 01                   |
    | sbb dword [rcx], 0x01                        | 83 19 01                   |
    | sbb dword [rdx], 0x01                        | 83 1a 01                   |
    | sbb dword [rbx], 0x01                        | 83 1b 01                   |
    | sbb dword [rsp], 0x01                        | 83 1c 24 01                |
    | sbb dword [rbp], 0x01                        | 83 5d 00 01                |
    | sbb dword [rsi], 0x01                        | 83 1e 01                   |
    | sbb dword [rdi], 0x01                        | 83 1f 01                   |
    | sbb dword [r8], 0x01                         | 41 83 18 01                |
    | sbb dword [r9], 0x01                         | 41 83 19 01                |
    | sbb dword [r10], 0x01                        | 41 83 1a 01                |
    | sbb dword [r11], 0x01                        | 41 83 1b 01                |
    | sbb dword [r12], 0x01                        | 41 83 1c 24 01             |
    | sbb dword [r13], 0x01                        | 41 83 5d 00 01             |
    | sbb dword [r14], 0x01                        | 41 83 1e 01                |
    | sbb dword [r15], 0x01                        | 41 83 1f 01                |
    | sbb dword [rax + 1 * rcx], 0x01              | 83 1c 08 01                |
    | sbb dword [rcx + 1 * rcx], 0x01              | 83 1c 09 01                |
    | sbb dword [rdx + 1 * rcx], 0x01              | 83 1c 0a 01                |
    | sbb dword [rbx + 1 * rcx], 0x01              | 83 1c 0b 01                |
    | sbb dword [rsp + 1 * rcx], 0x01              | 83 1c 0c 01                |
    | sbb dword [rbp + 1 * rcx], 0x01              | 83 5c 0d 00 01             |
    | sbb dword [rsi + 1 * rcx], 0x01              | 83 1c 0e 01                |
    | sbb dword [rdi + 1 * rcx], 0x01              | 83 1c 0f 01                |
    | sbb dword [r8 + 1 * rcx], 0x01               | 41 83 1c 08 01             |
    | sbb dword [r9 + 1 * rcx], 0x01               | 41 83 1c 09 01             |
    | sbb dword [r10 + 1 * rcx], 0x01              | 41 83 1c 0a 01             |
    | sbb dword [r11 + 1 * rcx], 0x01              | 41 83 1c 0b 01             |
    | sbb dword [r12 + 1 * rcx], 0x01              | 41 83 1c 0c 01             |
    | sbb dword [r13 + 1 * rcx], 0x01              | 41 83 5c 0d 00 01          |
    | sbb dword [r14 + 1 * rcx], 0x01              | 41 83 1c 0e 01             |
    | sbb dword [r15 + 1 * rcx], 0x01              | 41 83 1c 0f 01             |
    | sbb dword [rax + 1 * rax], 0x01              | 83 1c 00 01                |
    | sbb dword [rax + 1 * rdx], 0x01              | 83 1c 10 01                |
    | sbb dword [rax + 1 * rbx], 0x01              | 83 1c 18 01                |
    | sbb dword [rax + 1 * rbp], 0x01              | 83 1c 28 01                |
    | sbb dword [rax + 1 * rsi], 0x01              | 83 1c 30 01                |
    | sbb dword [rax + 1 * rdi], 0x01              | 83 1c 38 01                |
    | sbb dword [rax + 1 * r8], 0x01               | 42 83 1c 00 01             |
    | sbb dword [rax + 1 * r9], 0x01               | 42 83 1c 08 01             |
    | sbb dword [rax + 1 * r10], 0x01              | 42 83 1c 10 01             |
    | sbb dword [rax + 1 * r11], 0x01              | 42 83 1c 18 01             |
    | sbb dword [rax + 1 * r12], 0x01              | 42 83 1c 20 01             |
    | sbb dword [rax + 1 * r13], 0x01              | 42 83 1c 28 01             |
    | sbb dword [rax + 1 * r14], 0x01              | 42 83 1c 30 01             |
    | sbb dword [rax + 1 * r15], 0x01              | 42 83 1c 38 01             |
    | sbb dword [rax + 2 * rcx], 0x01              | 83 1c 48 01                |
    | sbb dword [rax + 4 * rcx], 0x01              | 83 1c 88 01                |
    | sbb dword [rax + 8 * rcx], 0x01              | 83 1c c8 01                |
    | sbb dword [r8 + 1 * r9], 0x01                | 43 83 1c 08 01             |
    | sbb dword [r8 + 2 * r9], 0x01                | 43 83 1c 48 01             |
    | sbb dword [r8 + 4 * r9], 0x01                | 43 83 1c 88 01             |
    | sbb dword [r8 + 8 * r9], 0x01                | 43 83 1c c8 01             |
    | sbb dword [1 * rcx], 0x01                    | 83 1c 0d 00 00 00 00 01    |
    | sbb dword [2 * rcx], 0x01                    | 83 1c 4d 00 00 00 00 01    |
    | sbb dword [4 * rcx], 0x01                    | 83 1c 8d 00 00 00 00 01    |
    | sbb dword [8 * rcx], 0x01                    | 83 1c cd 00 00 00 00 01    |
    | sbb dword [1 * r9], 0x01                     | 42 83 1c 0d 00 00 00 00 01 |
    | sbb dword [2 * r9], 0x01                     | 42 83 1c 4d 00 00 00 00 01 |
    | sbb dword [4 * r9], 0x01                     | 42 83 1c 8d 00 00 00 00 01 |
    | sbb dword [8 * r9], 0x01                     | 42 83 1c cd 00 00 00 00 01 |
    | sbb dword [r13 + 8 * r12], 0x01              | 43 83 5c e5 00 01          |
    | sbb dword [rsp + 4 * r15], 0x01              | 42 83 1c bc 01             |
    | sbb dword [rax + 1 * rcx + 0x00], 0x01       | 83 5c 08 00 01             |
    | sbb dword [rax + 1 * rcx - 0x00], 0x01       | 83 5c 08 00 01             |
    | sbb dword [rax + 1 * rcx + 0x01], 0x01       | 83 5c 08 01 01             |
    | sbb dword [rax + 1 * rcx - 0x01], 0x01       | 83 5c 08 ff 01             |
    | sbb dword [rax + 1 * rcx + 0x00000001], 0x01 | 83 9c 08 01 00 00 00 01    |
    | sbb dword [rax + 1 * rcx - 0x00000001], 0x01 | 83 9c 08 ff ff ff ff 01    |
    | sbb dword [rax + 1 * rcx + 0x7f], 0x01       | 83 5c 08 7f 01             |
    | sbb dword [rax + 1 * rcx - 0x7f], 0x01       | 83 5c 08 81 01             |
    | sbb dword [rax + 1 * rcx + 0x80], 0x01       | 83 9c 08 80 00 00 00 01    |
    | sbb dword [rax + 1 * rcx - 0x80], 0x01       | 83 5c 08 80 01             |
    | sbb dword [rax + 1 * rcx - 0x81], 0x01       | 83 9c 08 7f ff ff ff 01    |
    | sbb dword [rax + 1 * rcx + 0xff], 0x01       | 83 9c 08 ff 00 00 00 01    |
    | sbb dword [rax + 1 * rcx - 0xff], 0x01       | 83 9c 08 01 ff ff ff 01    |
    | sbb dword [rax + 1 * rcx + 0x7fffffff], 0x01 | 83 9c 08 ff ff ff 7f 01    |
    | sbb dword [rax + 1 * rcx - 0x7fffffff], 0x01 | 83 9c 08 01 00 00 80 01    |
    | sbb dword [rax + 1 * rcx - 0x80000000], 0x01 | 83 9c 08 00 00 00 80 01    |
    | sbb dword [r10 + 0x7f], 0x01                 | 41 83 5a 7f 01             |
    | sbb dword [r10 + 0x80], 0x01                 | 41 83 9a 80 00 00 00 01    |
    | sbb dword [r10 - 0x80], 0x01                 | 41 83 5a 80 01             |
    | sbb dword [r10 - 0x81], 0x01                 | 41 83 9a 7f ff ff ff 01    |
    | sbb dword [rax], 0x00                        | 83 18 00                   |
    | sbb dword [rax], 0x7f                        | 83 18 7f                   |
    | sbb dword [rax], 0x80                        | 83 18 80                   |
    | sbb dword [rax], 0xff                        | 83 18 ff                   |
    | sbb dword [rcx], 0x7f                        | 83 19 7f                   |
    | sbb dword [rdx], 0x80                        | 83 1a 80                   |
    | sbb dword [rbx], 0xff                        | 83 1b ff                   |
    | sbb dword [rsp], 0x00                        | 83 1c 24 00                |
    | sbb dword [rsi], 0x7f                        | 83 1e 7f                   |
    | sbb dword [rdi], 0x80                        | 83 1f 80                   |
    | sbb dword [r8], 0xff                         | 41 83 18 ff                |
    | sbb dword [r9], 0x00                         | 41 83 19 00                |
    | sbb dword [r11], 0x7f                        | 41 83 1b 7f                |
    | sbb dword [r12], 0x80                        | 41 83 1c 24 80             |
    | sbb dword [r13], 0xff                        | 41 83 5d 00 ff             |
    | sbb dword [r14], 0x00                        | 41 83 1e 00                |
    | sbb dword [rax + 1 * rcx], 0x7f              | 83 1c 08 7f                |
    | sbb dword [rcx + 1 * rcx], 0x80              | 83 1c 09 80                |
    | sbb dword [rdx + 1 * rcx], 0xff              | 83 1c 0a ff                |
    | sbb dword [rbx + 1 * rcx], 0x00              | 83 1c 0b 00                |
    | sbb dword [rbp + 1 * rcx], 0x7f              | 83 5c 0d 00 7f             |
    | sbb dword [rsi + 1 * rcx], 0x80              | 83 1c 0e 80                |
    | sbb dword [rdi + 1 * rcx], 0xff              | 83 1c 0f ff                |
    | sbb dword [r8 + 1 * rcx], 0x00               | 41 83 1c 08 00             |
    | sbb dword [r10 + 1 * rcx], 0x7f              | 41 83 1c 0a 7f             |
    | sbb dword [r11 + 1 * rcx], 0x80              | 41 83 1c 0b 80             |
    | sbb dword [r12 + 1 * rcx], 0xff              | 41 83 1c 0c ff             |
    | sbb dword [r13 + 1 * rcx], 0x00              | 41 83 5c 0d 00 00          |
    | sbb dword [r15 + 1 * rcx], 0x7f              | 41 83 1c 0f 7f             |
    | sbb dword [rax + 1 * rax], 0x80              | 83 1c 00 80                |
    | sbb dword [rax + 1 * rdx], 0xff              | 83 1c 10 ff                |
    | sbb dword [rax + 1 * rbx], 0x00              | 83 1c 18 00                |
    | sbb dword [rax + 1 * rsi], 0x7f              | 83 1c 30 7f                |
    | sbb dword [rax + 1 * rdi], 0x80              | 83 1c 38 80                |
    | sbb dword [rax + 1 * r8], 0xff               | 42 83 1c 00 ff             |
    | sbb dword [rax + 1 * r9], 0x00               | 42 83 1c 08 00             |
    | sbb dword [rax + 1 * r11], 0x7f              | 42 83 1c 18 7f             |
    | sbb dword [rax + 1 * r12], 0x80              | 42 83 1c 20 80             |
    | sbb dword [rax + 1 * r13], 0xff              | 42 83 1c 28 ff             |
    | sbb dword [rax + 1 * r14], 0x00              | 42 83 1c 30 00             |
    | sbb dword [rax + 2 * rcx], 0x7f              | 83 1c 48 7f                |
    | sbb dword [rax + 4 * rcx], 0x80              | 83 1c 88 80                |
    | sbb dword [rax + 8 * rcx], 0xff              | 83 1c c8 ff                |
    | sbb dword [r8 + 1 * r9], 0x00                | 43 83 1c 08 00             |
    | sbb dword [r8 + 4 * r9], 0x7f                | 43 83 1c 88 7f             |
    | sbb dword [r8 + 8 * r9], 0x80                | 43 83 1c c8 80             |
    | sbb dword [1 * rcx], 0xff                    | 83 1c 0d 00 00 00 00 ff    |
    | sbb dword [2 * rcx], 0x00                    | 83 1c 4d 00 00 00 00 00    |
    | sbb dword [8 * rcx], 0x7f                    | 83 1c cd 00 00 00 00 7f    |
    | sbb dword [1 * r9], 0x80                     | 42 83 1c 0d 00 00 00 00 80 |
    | sbb dword [2 * r9], 0xff                     | 42 83 1c 4d 00 00 00 00 ff |
    | sbb dword [4 * r9], 0x00                     | 42 83 1c 8d 00 00 00 00 00 |
    | sbb dword [r13 + 8 * r12], 0x7f              | 43 83 5c e5 00 7f          |
    | sbb dword [rsp + 4 * r15], 0x80              | 42 83 1c bc 80             |
    | sbb dword [rax + 1 * rcx + 0x00], 0xff       | 83 5c 08 00 ff             |
    | sbb dword [rax + 1 * rcx - 0x00], 0x00       | 83 5c 08 00 00             |
    | sbb dword [rax + 1 * rcx - 0x01], 0x7f       | 83 5c 08 ff 7f             |
    | sbb dword [rax + 1 * rcx + 0x00000001], 0x80 | 83 9c 08 01 00 00 00 80    |
    | sbb dword [rax + 1 * rcx - 0x00000001], 0xff | 83 9c 08 ff ff ff ff ff    |
    | sbb dword [rax + 1 * rcx + 0x7f], 0x00       | 83 5c 08 7f 00             |
    | sbb dword [rax + 1 * rcx + 0x80], 0x7f       | 83 9c 08 80 00 00 00 7f    |
    | sbb dword [rax + 1 * rcx - 0x80], 0x80       | 83 5c 08 80 80             |
    | sbb dword [rax + 1 * rcx - 0x81], 0xff       | 83 9c 08 7f ff ff ff ff    |
    | sbb dword [rax + 1 * rcx + 0xff], 0x00       | 83 9c 08 ff 00 00 00 00    |
    | sbb dword [rax + 1 * rcx + 0x7fffffff], 0x7f | 83 9c 08 ff ff ff 7f 7f    |
    | sbb dword [rax + 1 * rcx - 0x7fffffff], 0x80 | 83 9c 08 01 00 00 80 80    |
    | sbb dword [rax + 1 * rcx - 0x80000000], 0xff | 83 9c 08 00 00 00 80 ff    |
    | sbb dword [r10 + 0x7f], 0x00                 | 41 83 5a 7f 00             |
    | sbb dword [r10 - 0x80], 0x7f                 | 41 83 5a 80 7f             |
    | sbb dword [r10 - 0x81], 0x80                 | 41 83 9a 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sbb_addr32_imm8():
    encode(SBB_ADDR32_IMM8)


SBB_ADDR32_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | sbb dword [rax], 0x00000001                        | 81 18 01 00 00 00                   |
    | sbb dword [rcx], 0x00000001                        | 81 19 01 00 00 00                   |
    | sbb dword [rdx], 0x00000001                        | 81 1a 01 00 00 00                   |
    | sbb dword [rbx], 0x00000001                        | 81 1b 01 00 00 00                   |
    | sbb dword [rsp], 0x00000001                        | 81 1c 24 01 00 00 00                |
    | sbb dword [rbp], 0x00000001                        | 81 5d 00 01 00 00 00                |
    | sbb dword [rsi], 0x00000001                        | 81 1e 01 00 00 00                   |
    | sbb dword [rdi], 0x00000001                        | 81 1f 01 00 00 00                   |
    | sbb dword [r8], 0x00000001                         | 41 81 18 01 00 00 00                |
    | sbb dword [r9], 0x00000001                         | 41 81 19 01 00 00 00                |
    | sbb dword [r10], 0x00000001                        | 41 81 1a 01 00 00 00                |
    | sbb dword [r11], 0x00000001                        | 41 81 1b 01 00 00 00                |
    | sbb dword [r12], 0x00000001                        | 41 81 1c 24 01 00 00 00             |
    | sbb dword [r13], 0x00000001                        | 41 81 5d 00 01 00 00 00             |
    | sbb dword [r14], 0x00000001                        | 41 81 1e 01 00 00 00                |
    | sbb dword [r15], 0x00000001                        | 41 81 1f 01 00 00 00                |
    | sbb dword [rax + 1 * rcx], 0x00000001              | 81 1c 08 01 00 00 00                |
    | sbb dword [rcx + 1 * rcx], 0x00000001              | 81 1c 09 01 00 00 00                |
    | sbb dword [rdx + 1 * rcx], 0x00000001              | 81 1c 0a 01 00 00 00                |
    | sbb dword [rbx + 1 * rcx], 0x00000001              | 81 1c 0b 01 00 00 00                |
    | sbb dword [rsp + 1 * rcx], 0x00000001              | 81 1c 0c 01 00 00 00                |
    | sbb dword [rbp + 1 * rcx], 0x00000001              | 81 5c 0d 00 01 00 00 00             |
    | sbb dword [rsi + 1 * rcx], 0x00000001              | 81 1c 0e 01 00 00 00                |
    | sbb dword [rdi + 1 * rcx], 0x00000001              | 81 1c 0f 01 00 00 00                |
    | sbb dword [r8 + 1 * rcx], 0x00000001               | 41 81 1c 08 01 00 00 00             |
    | sbb dword [r9 + 1 * rcx], 0x00000001               | 41 81 1c 09 01 00 00 00             |
    | sbb dword [r10 + 1 * rcx], 0x00000001              | 41 81 1c 0a 01 00 00 00             |
    | sbb dword [r11 + 1 * rcx], 0x00000001              | 41 81 1c 0b 01 00 00 00             |
    | sbb dword [r12 + 1 * rcx], 0x00000001              | 41 81 1c 0c 01 00 00 00             |
    | sbb dword [r13 + 1 * rcx], 0x00000001              | 41 81 5c 0d 00 01 00 00 00          |
    | sbb dword [r14 + 1 * rcx], 0x00000001              | 41 81 1c 0e 01 00 00 00             |
    | sbb dword [r15 + 1 * rcx], 0x00000001              | 41 81 1c 0f 01 00 00 00             |
    | sbb dword [rax + 1 * rax], 0x00000001              | 81 1c 00 01 00 00 00                |
    | sbb dword [rax + 1 * rdx], 0x00000001              | 81 1c 10 01 00 00 00                |
    | sbb dword [rax + 1 * rbx], 0x00000001              | 81 1c 18 01 00 00 00                |
    | sbb dword [rax + 1 * rbp], 0x00000001              | 81 1c 28 01 00 00 00                |
    | sbb dword [rax + 1 * rsi], 0x00000001              | 81 1c 30 01 00 00 00                |
    | sbb dword [rax + 1 * rdi], 0x00000001              | 81 1c 38 01 00 00 00                |
    | sbb dword [rax + 1 * r8], 0x00000001               | 42 81 1c 00 01 00 00 00             |
    | sbb dword [rax + 1 * r9], 0x00000001               | 42 81 1c 08 01 00 00 00             |
    | sbb dword [rax + 1 * r10], 0x00000001              | 42 81 1c 10 01 00 00 00             |
    | sbb dword [rax + 1 * r11], 0x00000001              | 42 81 1c 18 01 00 00 00             |
    | sbb dword [rax + 1 * r12], 0x00000001              | 42 81 1c 20 01 00 00 00             |
    | sbb dword [rax + 1 * r13], 0x00000001              | 42 81 1c 28 01 00 00 00             |
    | sbb dword [rax + 1 * r14], 0x00000001              | 42 81 1c 30 01 00 00 00             |
    | sbb dword [rax + 1 * r15], 0x00000001              | 42 81 1c 38 01 00 00 00             |
    | sbb dword [rax + 2 * rcx], 0x00000001              | 81 1c 48 01 00 00 00                |
    | sbb dword [rax + 4 * rcx], 0x00000001              | 81 1c 88 01 00 00 00                |
    | sbb dword [rax + 8 * rcx], 0x00000001              | 81 1c c8 01 00 00 00                |
    | sbb dword [r8 + 1 * r9], 0x00000001                | 43 81 1c 08 01 00 00 00             |
    | sbb dword [r8 + 2 * r9], 0x00000001                | 43 81 1c 48 01 00 00 00             |
    | sbb dword [r8 + 4 * r9], 0x00000001                | 43 81 1c 88 01 00 00 00             |
    | sbb dword [r8 + 8 * r9], 0x00000001                | 43 81 1c c8 01 00 00 00             |
    | sbb dword [1 * rcx], 0x00000001                    | 81 1c 0d 00 00 00 00 01 00 00 00    |
    | sbb dword [2 * rcx], 0x00000001                    | 81 1c 4d 00 00 00 00 01 00 00 00    |
    | sbb dword [4 * rcx], 0x00000001                    | 81 1c 8d 00 00 00 00 01 00 00 00    |
    | sbb dword [8 * rcx], 0x00000001                    | 81 1c cd 00 00 00 00 01 00 00 00    |
    | sbb dword [1 * r9], 0x00000001                     | 42 81 1c 0d 00 00 00 00 01 00 00 00 |
    | sbb dword [2 * r9], 0x00000001                     | 42 81 1c 4d 00 00 00 00 01 00 00 00 |
    | sbb dword [4 * r9], 0x00000001                     | 42 81 1c 8d 00 00 00 00 01 00 00 00 |
    | sbb dword [8 * r9], 0x00000001                     | 42 81 1c cd 00 00 00 00 01 00 00 00 |
    | sbb dword [r13 + 8 * r12], 0x00000001              | 43 81 5c e5 00 01 00 00 00          |
    | sbb dword [rsp + 4 * r15], 0x00000001              | 42 81 1c bc 01 00 00 00             |
    | sbb dword [rax + 1 * rcx + 0x00], 0x00000001       | 81 5c 08 00 01 00 00 00             |
    | sbb dword [rax + 1 * rcx - 0x00], 0x00000001       | 81 5c 08 00 01 00 00 00             |
    | sbb dword [rax + 1 * rcx + 0x01], 0x00000001       | 81 5c 08 01 01 00 00 00             |
    | sbb dword [rax + 1 * rcx - 0x01], 0x00000001       | 81 5c 08 ff 01 00 00 00             |
    | sbb dword [rax + 1 * rcx + 0x00000001], 0x00000001 | 81 9c 08 01 00 00 00 01 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x00000001], 0x00000001 | 81 9c 08 ff ff ff ff 01 00 00 00    |
    | sbb dword [rax + 1 * rcx + 0x7f], 0x00000001       | 81 5c 08 7f 01 00 00 00             |
    | sbb dword [rax + 1 * rcx - 0x7f], 0x00000001       | 81 5c 08 81 01 00 00 00             |
    | sbb dword [rax + 1 * rcx + 0x80], 0x00000001       | 81 9c 08 80 00 00 00 01 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x80], 0x00000001       | 81 5c 08 80 01 00 00 00             |
    | sbb dword [rax + 1 * rcx - 0x81], 0x00000001       | 81 9c 08 7f ff ff ff 01 00 00 00    |
    | sbb dword [rax + 1 * rcx + 0xff], 0x00000001       | 81 9c 08 ff 00 00 00 01 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0xff], 0x00000001       | 81 9c 08 01 ff ff ff 01 00 00 00    |
    | sbb dword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 81 9c 08 ff ff ff 7f 01 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 81 9c 08 01 00 00 80 01 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x80000000], 0x00000001 | 81 9c 08 00 00 00 80 01 00 00 00    |
    | sbb dword [r10 + 0x7f], 0x00000001                 | 41 81 5a 7f 01 00 00 00             |
    | sbb dword [r10 + 0x80], 0x00000001                 | 41 81 9a 80 00 00 00 01 00 00 00    |
    | sbb dword [r10 - 0x80], 0x00000001                 | 41 81 5a 80 01 00 00 00             |
    | sbb dword [r10 - 0x81], 0x00000001                 | 41 81 9a 7f ff ff ff 01 00 00 00    |
    | sbb dword [rax], 0x00000000                        | 81 18 00 00 00 00                   |
    | sbb dword [rax], 0x0000007f                        | 81 18 7f 00 00 00                   |
    | sbb dword [rax], 0x00000080                        | 81 18 80 00 00 00                   |
    | sbb dword [rax], 0x000000ff                        | 81 18 ff 00 00 00                   |
    | sbb dword [rax], 0x00000100                        | 81 18 00 01 00 00                   |
    | sbb dword [rax], 0x00007fff                        | 81 18 ff 7f 00 00                   |
    | sbb dword [rax], 0x00008000                        | 81 18 00 80 00 00                   |
    | sbb dword [rax], 0x0000ffff                        | 81 18 ff ff 00 00                   |
    | sbb dword [rax], 0x00010000                        | 81 18 00 00 01 00                   |
    | sbb dword [rax], 0x7fffffff                        | 81 18 ff ff ff 7f                   |
    | sbb dword [rax], 0x80000000                        | 81 18 00 00 00 80                   |
    | sbb dword [rax], 0xffffffff                        | 81 18 ff ff ff ff                   |
    | sbb dword [rcx], 0x0000007f                        | 81 19 7f 00 00 00                   |
    | sbb dword [rdx], 0x00000080                        | 81 1a 80 00 00 00                   |
    | sbb dword [rbx], 0x000000ff                        | 81 1b ff 00 00 00                   |
    | sbb dword [rsp], 0x00000100                        | 81 1c 24 00 01 00 00                |
    | sbb dword [rbp], 0x00007fff                        | 81 5d 00 ff 7f 00 00                |
    | sbb dword [rsi], 0x00008000                        | 81 1e 00 80 00 00                   |
    | sbb dword [rdi], 0x0000ffff                        | 81 1f ff ff 00 00                   |
    | sbb dword [r8], 0x00010000                         | 41 81 18 00 00 01 00                |
    | sbb dword [r9], 0x7fffffff                         | 41 81 19 ff ff ff 7f                |
    | sbb dword [r10], 0x80000000                        | 41 81 1a 00 00 00 80                |
    | sbb dword [r11], 0xffffffff                        | 41 81 1b ff ff ff ff                |
    | sbb dword [r12], 0x00000000                        | 41 81 1c 24 00 00 00 00             |
    | sbb dword [r14], 0x0000007f                        | 41 81 1e 7f 00 00 00                |
    | sbb dword [r15], 0x00000080                        | 41 81 1f 80 00 00 00                |
    | sbb dword [rax + 1 * rcx], 0x000000ff              | 81 1c 08 ff 00 00 00                |
    | sbb dword [rcx + 1 * rcx], 0x00000100              | 81 1c 09 00 01 00 00                |
    | sbb dword [rdx + 1 * rcx], 0x00007fff              | 81 1c 0a ff 7f 00 00                |
    | sbb dword [rbx + 1 * rcx], 0x00008000              | 81 1c 0b 00 80 00 00                |
    | sbb dword [rsp + 1 * rcx], 0x0000ffff              | 81 1c 0c ff ff 00 00                |
    | sbb dword [rbp + 1 * rcx], 0x00010000              | 81 5c 0d 00 00 00 01 00             |
    | sbb dword [rsi + 1 * rcx], 0x7fffffff              | 81 1c 0e ff ff ff 7f                |
    | sbb dword [rdi + 1 * rcx], 0x80000000              | 81 1c 0f 00 00 00 80                |
    | sbb dword [r8 + 1 * rcx], 0xffffffff               | 41 81 1c 08 ff ff ff ff             |
    | sbb dword [r9 + 1 * rcx], 0x00000000               | 41 81 1c 09 00 00 00 00             |
    | sbb dword [r11 + 1 * rcx], 0x0000007f              | 41 81 1c 0b 7f 00 00 00             |
    | sbb dword [r12 + 1 * rcx], 0x00000080              | 41 81 1c 0c 80 00 00 00             |
    | sbb dword [r13 + 1 * rcx], 0x000000ff              | 41 81 5c 0d 00 ff 00 00 00          |
    | sbb dword [r14 + 1 * rcx], 0x00000100              | 41 81 1c 0e 00 01 00 00             |
    | sbb dword [r15 + 1 * rcx], 0x00007fff              | 41 81 1c 0f ff 7f 00 00             |
    | sbb dword [rax + 1 * rax], 0x00008000              | 81 1c 00 00 80 00 00                |
    | sbb dword [rax + 1 * rdx], 0x0000ffff              | 81 1c 10 ff ff 00 00                |
    | sbb dword [rax + 1 * rbx], 0x00010000              | 81 1c 18 00 00 01 00                |
    | sbb dword [rax + 1 * rbp], 0x7fffffff              | 81 1c 28 ff ff ff 7f                |
    | sbb dword [rax + 1 * rsi], 0x80000000              | 81 1c 30 00 00 00 80                |
    | sbb dword [rax + 1 * rdi], 0xffffffff              | 81 1c 38 ff ff ff ff                |
    | sbb dword [rax + 1 * r8], 0x00000000               | 42 81 1c 00 00 00 00 00             |
    | sbb dword [rax + 1 * r10], 0x0000007f              | 42 81 1c 10 7f 00 00 00             |
    | sbb dword [rax + 1 * r11], 0x00000080              | 42 81 1c 18 80 00 00 00             |
    | sbb dword [rax + 1 * r12], 0x000000ff              | 42 81 1c 20 ff 00 00 00             |
    | sbb dword [rax + 1 * r13], 0x00000100              | 42 81 1c 28 00 01 00 00             |
    | sbb dword [rax + 1 * r14], 0x00007fff              | 42 81 1c 30 ff 7f 00 00             |
    | sbb dword [rax + 1 * r15], 0x00008000              | 42 81 1c 38 00 80 00 00             |
    | sbb dword [rax + 2 * rcx], 0x0000ffff              | 81 1c 48 ff ff 00 00                |
    | sbb dword [rax + 4 * rcx], 0x00010000              | 81 1c 88 00 00 01 00                |
    | sbb dword [rax + 8 * rcx], 0x7fffffff              | 81 1c c8 ff ff ff 7f                |
    | sbb dword [r8 + 1 * r9], 0x80000000                | 43 81 1c 08 00 00 00 80             |
    | sbb dword [r8 + 2 * r9], 0xffffffff                | 43 81 1c 48 ff ff ff ff             |
    | sbb dword [r8 + 4 * r9], 0x00000000                | 43 81 1c 88 00 00 00 00             |
    | sbb dword [1 * rcx], 0x0000007f                    | 81 1c 0d 00 00 00 00 7f 00 00 00    |
    | sbb dword [2 * rcx], 0x00000080                    | 81 1c 4d 00 00 00 00 80 00 00 00    |
    | sbb dword [4 * rcx], 0x000000ff                    | 81 1c 8d 00 00 00 00 ff 00 00 00    |
    | sbb dword [8 * rcx], 0x00000100                    | 81 1c cd 00 00 00 00 00 01 00 00    |
    | sbb dword [1 * r9], 0x00007fff                     | 42 81 1c 0d 00 00 00 00 ff 7f 00 00 |
    | sbb dword [2 * r9], 0x00008000                     | 42 81 1c 4d 00 00 00 00 00 80 00 00 |
    | sbb dword [4 * r9], 0x0000ffff                     | 42 81 1c 8d 00 00 00 00 ff ff 00 00 |
    | sbb dword [8 * r9], 0x00010000                     | 42 81 1c cd 00 00 00 00 00 00 01 00 |
    | sbb dword [r13 + 8 * r12], 0x7fffffff              | 43 81 5c e5 00 ff ff ff 7f          |
    | sbb dword [rsp + 4 * r15], 0x80000000              | 42 81 1c bc 00 00 00 80             |
    | sbb dword [rax + 1 * rcx + 0x00], 0xffffffff       | 81 5c 08 00 ff ff ff ff             |
    | sbb dword [rax + 1 * rcx - 0x00], 0x00000000       | 81 5c 08 00 00 00 00 00             |
    | sbb dword [rax + 1 * rcx - 0x01], 0x0000007f       | 81 5c 08 ff 7f 00 00 00             |
    | sbb dword [rax + 1 * rcx + 0x00000001], 0x00000080 | 81 9c 08 01 00 00 00 80 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x00000001], 0x000000ff | 81 9c 08 ff ff ff ff ff 00 00 00    |
    | sbb dword [rax + 1 * rcx + 0x7f], 0x00000100       | 81 5c 08 7f 00 01 00 00             |
    | sbb dword [rax + 1 * rcx - 0x7f], 0x00007fff       | 81 5c 08 81 ff 7f 00 00             |
    | sbb dword [rax + 1 * rcx + 0x80], 0x00008000       | 81 9c 08 80 00 00 00 00 80 00 00    |
    | sbb dword [rax + 1 * rcx - 0x80], 0x0000ffff       | 81 5c 08 80 ff ff 00 00             |
    | sbb dword [rax + 1 * rcx - 0x81], 0x00010000       | 81 9c 08 7f ff ff ff 00 00 01 00    |
    | sbb dword [rax + 1 * rcx + 0xff], 0x7fffffff       | 81 9c 08 ff 00 00 00 ff ff ff 7f    |
    | sbb dword [rax + 1 * rcx - 0xff], 0x80000000       | 81 9c 08 01 ff ff ff 00 00 00 80    |
    | sbb dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 81 9c 08 ff ff ff 7f ff ff ff ff    |
    | sbb dword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 81 9c 08 01 00 00 80 00 00 00 00    |
    | sbb dword [r10 + 0x7f], 0x0000007f                 | 41 81 5a 7f 7f 00 00 00             |
    | sbb dword [r10 + 0x80], 0x00000080                 | 41 81 9a 80 00 00 00 80 00 00 00    |
    | sbb dword [r10 - 0x80], 0x000000ff                 | 41 81 5a 80 ff 00 00 00             |
    | sbb dword [r10 - 0x81], 0x00000100                 | 41 81 9a 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_sbb_addr32_imm32():
    encode(SBB_ADDR32_IMM32)


SBB_ADDR32_REG32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | sbb dword [rax], ecx                         | 19 08                   |
    | sbb dword [rcx], ecx                         | 19 09                   |
    | sbb dword [rdx], ecx                         | 19 0a                   |
    | sbb dword [rbx], ecx                         | 19 0b                   |
    | sbb dword [rsp], ecx                         | 19 0c 24                |
    | sbb dword [rbp], ecx                         | 19 4d 00                |
    | sbb dword [rsi], ecx                         | 19 0e                   |
    | sbb dword [rdi], ecx                         | 19 0f                   |
    | sbb dword [r8], ecx                          | 41 19 08                |
    | sbb dword [r9], ecx                          | 41 19 09                |
    | sbb dword [r10], ecx                         | 41 19 0a                |
    | sbb dword [r11], ecx                         | 41 19 0b                |
    | sbb dword [r12], ecx                         | 41 19 0c 24             |
    | sbb dword [r13], ecx                         | 41 19 4d 00             |
    | sbb dword [r14], ecx                         | 41 19 0e                |
    | sbb dword [r15], ecx                         | 41 19 0f                |
    | sbb dword [rax + 1 * rcx], ecx               | 19 0c 08                |
    | sbb dword [rcx + 1 * rcx], ecx               | 19 0c 09                |
    | sbb dword [rdx + 1 * rcx], ecx               | 19 0c 0a                |
    | sbb dword [rbx + 1 * rcx], ecx               | 19 0c 0b                |
    | sbb dword [rsp + 1 * rcx], ecx               | 19 0c 0c                |
    | sbb dword [rbp + 1 * rcx], ecx               | 19 4c 0d 00             |
    | sbb dword [rsi + 1 * rcx], ecx               | 19 0c 0e                |
    | sbb dword [rdi + 1 * rcx], ecx               | 19 0c 0f                |
    | sbb dword [r8 + 1 * rcx], ecx                | 41 19 0c 08             |
    | sbb dword [r9 + 1 * rcx], ecx                | 41 19 0c 09             |
    | sbb dword [r10 + 1 * rcx], ecx               | 41 19 0c 0a             |
    | sbb dword [r11 + 1 * rcx], ecx               | 41 19 0c 0b             |
    | sbb dword [r12 + 1 * rcx], ecx               | 41 19 0c 0c             |
    | sbb dword [r13 + 1 * rcx], ecx               | 41 19 4c 0d 00          |
    | sbb dword [r14 + 1 * rcx], ecx               | 41 19 0c 0e             |
    | sbb dword [r15 + 1 * rcx], ecx               | 41 19 0c 0f             |
    | sbb dword [rax + 1 * rax], ecx               | 19 0c 00                |
    | sbb dword [rax + 1 * rdx], ecx               | 19 0c 10                |
    | sbb dword [rax + 1 * rbx], ecx               | 19 0c 18                |
    | sbb dword [rax + 1 * rbp], ecx               | 19 0c 28                |
    | sbb dword [rax + 1 * rsi], ecx               | 19 0c 30                |
    | sbb dword [rax + 1 * rdi], ecx               | 19 0c 38                |
    | sbb dword [rax + 1 * r8], ecx                | 42 19 0c 00             |
    | sbb dword [rax + 1 * r9], ecx                | 42 19 0c 08             |
    | sbb dword [rax + 1 * r10], ecx               | 42 19 0c 10             |
    | sbb dword [rax + 1 * r11], ecx               | 42 19 0c 18             |
    | sbb dword [rax + 1 * r12], ecx               | 42 19 0c 20             |
    | sbb dword [rax + 1 * r13], ecx               | 42 19 0c 28             |
    | sbb dword [rax + 1 * r14], ecx               | 42 19 0c 30             |
    | sbb dword [rax + 1 * r15], ecx               | 42 19 0c 38             |
    | sbb dword [rax + 2 * rcx], ecx               | 19 0c 48                |
    | sbb dword [rax + 4 * rcx], ecx               | 19 0c 88                |
    | sbb dword [rax + 8 * rcx], ecx               | 19 0c c8                |
    | sbb dword [r8 + 1 * r9], ecx                 | 43 19 0c 08             |
    | sbb dword [r8 + 2 * r9], ecx                 | 43 19 0c 48             |
    | sbb dword [r8 + 4 * r9], ecx                 | 43 19 0c 88             |
    | sbb dword [r8 + 8 * r9], ecx                 | 43 19 0c c8             |
    | sbb dword [1 * rcx], ecx                     | 19 0c 0d 00 00 00 00    |
    | sbb dword [2 * rcx], ecx                     | 19 0c 4d 00 00 00 00    |
    | sbb dword [4 * rcx], ecx                     | 19 0c 8d 00 00 00 00    |
    | sbb dword [8 * rcx], ecx                     | 19 0c cd 00 00 00 00    |
    | sbb dword [1 * r9], ecx                      | 42 19 0c 0d 00 00 00 00 |
    | sbb dword [2 * r9], ecx                      | 42 19 0c 4d 00 00 00 00 |
    | sbb dword [4 * r9], ecx                      | 42 19 0c 8d 00 00 00 00 |
    | sbb dword [8 * r9], ecx                      | 42 19 0c cd 00 00 00 00 |
    | sbb dword [r13 + 8 * r12], ecx               | 43 19 4c e5 00          |
    | sbb dword [rsp + 4 * r15], ecx               | 42 19 0c bc             |
    | sbb dword [rax + 1 * rcx + 0x00], ecx        | 19 4c 08 00             |
    | sbb dword [rax + 1 * rcx - 0x00], ecx        | 19 4c 08 00             |
    | sbb dword [rax + 1 * rcx + 0x01], ecx        | 19 4c 08 01             |
    | sbb dword [rax + 1 * rcx - 0x01], ecx        | 19 4c 08 ff             |
    | sbb dword [rax + 1 * rcx + 0x00000001], ecx  | 19 8c 08 01 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x00000001], ecx  | 19 8c 08 ff ff ff ff    |
    | sbb dword [rax + 1 * rcx + 0x7f], ecx        | 19 4c 08 7f             |
    | sbb dword [rax + 1 * rcx - 0x7f], ecx        | 19 4c 08 81             |
    | sbb dword [rax + 1 * rcx + 0x80], ecx        | 19 8c 08 80 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x80], ecx        | 19 4c 08 80             |
    | sbb dword [rax + 1 * rcx - 0x81], ecx        | 19 8c 08 7f ff ff ff    |
    | sbb dword [rax + 1 * rcx + 0xff], ecx        | 19 8c 08 ff 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0xff], ecx        | 19 8c 08 01 ff ff ff    |
    | sbb dword [rax + 1 * rcx + 0x7fffffff], ecx  | 19 8c 08 ff ff ff 7f    |
    | sbb dword [rax + 1 * rcx - 0x7fffffff], ecx  | 19 8c 08 01 00 00 80    |
    | sbb dword [rax + 1 * rcx - 0x80000000], ecx  | 19 8c 08 00 00 00 80    |
    | sbb dword [r10 + 0x7f], ecx                  | 41 19 4a 7f             |
    | sbb dword [r10 + 0x80], ecx                  | 41 19 8a 80 00 00 00    |
    | sbb dword [r10 - 0x80], ecx                  | 41 19 4a 80             |
    | sbb dword [r10 - 0x81], ecx                  | 41 19 8a 7f ff ff ff    |
    | sbb dword [rax], eax                         | 19 00                   |
    | sbb dword [rax], edx                         | 19 10                   |
    | sbb dword [rax], ebx                         | 19 18                   |
    | sbb dword [rax], esp                         | 19 20                   |
    | sbb dword [rax], ebp                         | 19 28                   |
    | sbb dword [rax], esi                         | 19 30                   |
    | sbb dword [rax], edi                         | 19 38                   |
    | sbb dword [rax], r8d                         | 44 19 00                |
    | sbb dword [rax], r9d                         | 44 19 08                |
    | sbb dword [rax], r10d                        | 44 19 10                |
    | sbb dword [rax], r11d                        | 44 19 18                |
    | sbb dword [rax], r12d                        | 44 19 20                |
    | sbb dword [rax], r13d                        | 44 19 28                |
    | sbb dword [rax], r14d                        | 44 19 30                |
    | sbb dword [rax], r15d                        | 44 19 38                |
    | sbb dword [rcx], edx                         | 19 11                   |
    | sbb dword [rdx], ebx                         | 19 1a                   |
    | sbb dword [rbx], esp                         | 19 23                   |
    | sbb dword [rsp], ebp                         | 19 2c 24                |
    | sbb dword [rbp], esi                         | 19 75 00                |
    | sbb dword [rsi], edi                         | 19 3e                   |
    | sbb dword [rdi], r8d                         | 44 19 07                |
    | sbb dword [r8], r9d                          | 45 19 08                |
    | sbb dword [r9], r10d                         | 45 19 11                |
    | sbb dword [r10], r11d                        | 45 19 1a                |
    | sbb dword [r11], r12d                        | 45 19 23                |
    | sbb dword [r12], r13d                        | 45 19 2c 24             |
    | sbb dword [r13], r14d                        | 45 19 75 00             |
    | sbb dword [r14], r15d                        | 45 19 3e                |
    | sbb dword [r15], eax                         | 41 19 07                |
    | sbb dword [rcx + 1 * rcx], edx               | 19 14 09                |
    | sbb dword [rdx + 1 * rcx], ebx               | 19 1c 0a                |
    | sbb dword [rbx + 1 * rcx], esp               | 19 24 0b                |
    | sbb dword [rsp + 1 * rcx], ebp               | 19 2c 0c                |
    | sbb dword [rbp + 1 * rcx], esi               | 19 74 0d 00             |
    | sbb dword [rsi + 1 * rcx], edi               | 19 3c 0e                |
    | sbb dword [rdi + 1 * rcx], r8d               | 44 19 04 0f             |
    | sbb dword [r8 + 1 * rcx], r9d                | 45 19 0c 08             |
    | sbb dword [r9 + 1 * rcx], r10d               | 45 19 14 09             |
    | sbb dword [r10 + 1 * rcx], r11d              | 45 19 1c 0a             |
    | sbb dword [r11 + 1 * rcx], r12d              | 45 19 24 0b             |
    | sbb dword [r12 + 1 * rcx], r13d              | 45 19 2c 0c             |
    | sbb dword [r13 + 1 * rcx], r14d              | 45 19 74 0d 00          |
    | sbb dword [r14 + 1 * rcx], r15d              | 45 19 3c 0e             |
    | sbb dword [r15 + 1 * rcx], eax               | 41 19 04 0f             |
    | sbb dword [rax + 1 * rdx], edx               | 19 14 10                |
    | sbb dword [rax + 1 * rbx], ebx               | 19 1c 18                |
    | sbb dword [rax + 1 * rbp], esp               | 19 24 28                |
    | sbb dword [rax + 1 * rsi], ebp               | 19 2c 30                |
    | sbb dword [rax + 1 * rdi], esi               | 19 34 38                |
    | sbb dword [rax + 1 * r8], edi                | 42 19 3c 00             |
    | sbb dword [rax + 1 * r9], r8d                | 46 19 04 08             |
    | sbb dword [rax + 1 * r10], r9d               | 46 19 0c 10             |
    | sbb dword [rax + 1 * r11], r10d              | 46 19 14 18             |
    | sbb dword [rax + 1 * r12], r11d              | 46 19 1c 20             |
    | sbb dword [rax + 1 * r13], r12d              | 46 19 24 28             |
    | sbb dword [rax + 1 * r14], r13d              | 46 19 2c 30             |
    | sbb dword [rax + 1 * r15], r14d              | 46 19 34 38             |
    | sbb dword [rax + 2 * rcx], r15d              | 44 19 3c 48             |
    | sbb dword [rax + 4 * rcx], eax               | 19 04 88                |
    | sbb dword [r8 + 1 * r9], edx                 | 43 19 14 08             |
    | sbb dword [r8 + 2 * r9], ebx                 | 43 19 1c 48             |
    | sbb dword [r8 + 4 * r9], esp                 | 43 19 24 88             |
    | sbb dword [r8 + 8 * r9], ebp                 | 43 19 2c c8             |
    | sbb dword [1 * rcx], esi                     | 19 34 0d 00 00 00 00    |
    | sbb dword [2 * rcx], edi                     | 19 3c 4d 00 00 00 00    |
    | sbb dword [4 * rcx], r8d                     | 44 19 04 8d 00 00 00 00 |
    | sbb dword [8 * rcx], r9d                     | 44 19 0c cd 00 00 00 00 |
    | sbb dword [1 * r9], r10d                     | 46 19 14 0d 00 00 00 00 |
    | sbb dword [2 * r9], r11d                     | 46 19 1c 4d 00 00 00 00 |
    | sbb dword [4 * r9], r12d                     | 46 19 24 8d 00 00 00 00 |
    | sbb dword [8 * r9], r13d                     | 46 19 2c cd 00 00 00 00 |
    | sbb dword [r13 + 8 * r12], r14d              | 47 19 74 e5 00          |
    | sbb dword [rsp + 4 * r15], r15d              | 46 19 3c bc             |
    | sbb dword [rax + 1 * rcx + 0x00], eax        | 19 44 08 00             |
    | sbb dword [rax + 1 * rcx + 0x01], edx        | 19 54 08 01             |
    | sbb dword [rax + 1 * rcx - 0x01], ebx        | 19 5c 08 ff             |
    | sbb dword [rax + 1 * rcx + 0x00000001], esp  | 19 a4 08 01 00 00 00    |
    | sbb dword [rax + 1 * rcx - 0x00000001], ebp  | 19 ac 08 ff ff ff ff    |
    | sbb dword [rax + 1 * rcx + 0x7f], esi        | 19 74 08 7f             |
    | sbb dword [rax + 1 * rcx - 0x7f], edi        | 19 7c 08 81             |
    | sbb dword [rax + 1 * rcx + 0x80], r8d        | 44 19 84 08 80 00 00 00 |
    | sbb dword [rax + 1 * rcx - 0x80], r9d        | 44 19 4c 08 80          |
    | sbb dword [rax + 1 * rcx - 0x81], r10d       | 44 19 94 08 7f ff ff ff |
    | sbb dword [rax + 1 * rcx + 0xff], r11d       | 44 19 9c 08 ff 00 00 00 |
    | sbb dword [rax + 1 * rcx - 0xff], r12d       | 44 19 a4 08 01 ff ff ff |
    | sbb dword [rax + 1 * rcx + 0x7fffffff], r13d | 44 19 ac 08 ff ff ff 7f |
    | sbb dword [rax + 1 * rcx - 0x7fffffff], r14d | 44 19 b4 08 01 00 00 80 |
    | sbb dword [rax + 1 * rcx - 0x80000000], r15d | 44 19 bc 08 00 00 00 80 |
    | sbb dword [r10 + 0x7f], eax                  | 41 19 42 7f             |
    | sbb dword [r10 - 0x80], edx                  | 41 19 52 80             |
    | sbb dword [r10 - 0x81], ebx                  | 41 19 9a 7f ff ff ff    |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_sbb_addr32_reg32():
    encode(SBB_ADDR32_REG32)


SBB_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | sbb word [rax], 0x01                        | 66 83 18 01                   |
    | sbb word [rcx], 0x01                        | 66 83 19 01                   |
    | sbb word [rdx], 0x01                        | 66 83 1a 01                   |
    | sbb word [rbx], 0x01                        | 66 83 1b 01                   |
    | sbb word [rsp], 0x01                        | 66 83 1c 24 01                |
    | sbb word [rbp], 0x01                        | 66 83 5d 00 01                |
    | sbb word [rsi], 0x01                        | 66 83 1e 01                   |
    | sbb word [rdi], 0x01                        | 66 83 1f 01                   |
    | sbb word [r8], 0x01                         | 66 41 83 18 01                |
    | sbb word [r9], 0x01                         | 66 41 83 19 01                |
    | sbb word [r10], 0x01                        | 66 41 83 1a 01                |
    | sbb word [r11], 0x01                        | 66 41 83 1b 01                |
    | sbb word [r12], 0x01                        | 66 41 83 1c 24 01             |
    | sbb word [r13], 0x01                        | 66 41 83 5d 00 01             |
    | sbb word [r14], 0x01                        | 66 41 83 1e 01                |
    | sbb word [r15], 0x01                        | 66 41 83 1f 01                |
    | sbb word [rax + 1 * rcx], 0x01              | 66 83 1c 08 01                |
    | sbb word [rcx + 1 * rcx], 0x01              | 66 83 1c 09 01                |
    | sbb word [rdx + 1 * rcx], 0x01              | 66 83 1c 0a 01                |
    | sbb word [rbx + 1 * rcx], 0x01              | 66 83 1c 0b 01                |
    | sbb word [rsp + 1 * rcx], 0x01              | 66 83 1c 0c 01                |
    | sbb word [rbp + 1 * rcx], 0x01              | 66 83 5c 0d 00 01             |
    | sbb word [rsi + 1 * rcx], 0x01              | 66 83 1c 0e 01                |
    | sbb word [rdi + 1 * rcx], 0x01              | 66 83 1c 0f 01                |
    | sbb word [r8 + 1 * rcx], 0x01               | 66 41 83 1c 08 01             |
    | sbb word [r9 + 1 * rcx], 0x01               | 66 41 83 1c 09 01             |
    | sbb word [r10 + 1 * rcx], 0x01              | 66 41 83 1c 0a 01             |
    | sbb word [r11 + 1 * rcx], 0x01              | 66 41 83 1c 0b 01             |
    | sbb word [r12 + 1 * rcx], 0x01              | 66 41 83 1c 0c 01             |
    | sbb word [r13 + 1 * rcx], 0x01              | 66 41 83 5c 0d 00 01          |
    | sbb word [r14 + 1 * rcx], 0x01              | 66 41 83 1c 0e 01             |
    | sbb word [r15 + 1 * rcx], 0x01              | 66 41 83 1c 0f 01             |
    | sbb word [rax + 1 * rax], 0x01              | 66 83 1c 00 01                |
    | sbb word [rax + 1 * rdx], 0x01              | 66 83 1c 10 01                |
    | sbb word [rax + 1 * rbx], 0x01              | 66 83 1c 18 01                |
    | sbb word [rax + 1 * rbp], 0x01              | 66 83 1c 28 01                |
    | sbb word [rax + 1 * rsi], 0x01              | 66 83 1c 30 01                |
    | sbb word [rax + 1 * rdi], 0x01              | 66 83 1c 38 01                |
    | sbb word [rax + 1 * r8], 0x01               | 66 42 83 1c 00 01             |
    | sbb word [rax + 1 * r9], 0x01               | 66 42 83 1c 08 01             |
    | sbb word [rax + 1 * r10], 0x01              | 66 42 83 1c 10 01             |
    | sbb word [rax + 1 * r11], 0x01              | 66 42 83 1c 18 01             |
    | sbb word [rax + 1 * r12], 0x01              | 66 42 83 1c 20 01             |
    | sbb word [rax + 1 * r13], 0x01              | 66 42 83 1c 28 01             |
    | sbb word [rax + 1 * r14], 0x01              | 66 42 83 1c 30 01             |
    | sbb word [rax + 1 * r15], 0x01              | 66 42 83 1c 38 01             |
    | sbb word [rax + 2 * rcx], 0x01              | 66 83 1c 48 01                |
    | sbb word [rax + 4 * rcx], 0x01              | 66 83 1c 88 01                |
    | sbb word [rax + 8 * rcx], 0x01              | 66 83 1c c8 01                |
    | sbb word [r8 + 1 * r9], 0x01                | 66 43 83 1c 08 01             |
    | sbb word [r8 + 2 * r9], 0x01                | 66 43 83 1c 48 01             |
    | sbb word [r8 + 4 * r9], 0x01                | 66 43 83 1c 88 01             |
    | sbb word [r8 + 8 * r9], 0x01                | 66 43 83 1c c8 01             |
    | sbb word [1 * rcx], 0x01                    | 66 83 1c 0d 00 00 00 00 01    |
    | sbb word [2 * rcx], 0x01                    | 66 83 1c 4d 00 00 00 00 01    |
    | sbb word [4 * rcx], 0x01                    | 66 83 1c 8d 00 00 00 00 01    |
    | sbb word [8 * rcx], 0x01                    | 66 83 1c cd 00 00 00 00 01    |
    | sbb word [1 * r9], 0x01                     | 66 42 83 1c 0d 00 00 00 00 01 |
    | sbb word [2 * r9], 0x01                     | 66 42 83 1c 4d 00 00 00 00 01 |
    | sbb word [4 * r9], 0x01                     | 66 42 83 1c 8d 00 00 00 00 01 |
    | sbb word [8 * r9], 0x01                     | 66 42 83 1c cd 00 00 00 00 01 |
    | sbb word [r13 + 8 * r12], 0x01              | 66 43 83 5c e5 00 01          |
    | sbb word [rsp + 4 * r15], 0x01              | 66 42 83 1c bc 01             |
    | sbb word [rax + 1 * rcx + 0x00], 0x01       | 66 83 5c 08 00 01             |
    | sbb word [rax + 1 * rcx - 0x00], 0x01       | 66 83 5c 08 00 01             |
    | sbb word [rax + 1 * rcx + 0x01], 0x01       | 66 83 5c 08 01 01             |
    | sbb word [rax + 1 * rcx - 0x01], 0x01       | 66 83 5c 08 ff 01             |
    | sbb word [rax + 1 * rcx + 0x00000001], 0x01 | 66 83 9c 08 01 00 00 00 01    |
    | sbb word [rax + 1 * rcx - 0x00000001], 0x01 | 66 83 9c 08 ff ff ff ff 01    |
    | sbb word [rax + 1 * rcx + 0x7f], 0x01       | 66 83 5c 08 7f 01             |
    | sbb word [rax + 1 * rcx - 0x7f], 0x01       | 66 83 5c 08 81 01             |
    | sbb word [rax + 1 * rcx + 0x80], 0x01       | 66 83 9c 08 80 00 00 00 01    |
    | sbb word [rax + 1 * rcx - 0x80], 0x01       | 66 83 5c 08 80 01             |
    | sbb word [rax + 1 * rcx - 0x81], 0x01       | 66 83 9c 08 7f ff ff ff 01    |
    | sbb word [rax + 1 * rcx + 0xff], 0x01       | 66 83 9c 08 ff 00 00 00 01    |
    | sbb word [rax + 1 * rcx - 0xff], 0x01       | 66 83 9c 08 01 ff ff ff 01    |
    | sbb word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 83 9c 08 ff ff ff 7f 01    |
    | sbb word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 83 9c 08 01 00 00 80 01    |
    | sbb word [rax + 1 * rcx - 0x80000000], 0x01 | 66 83 9c 08 00 00 00 80 01    |
    | sbb word [r10 + 0x7f], 0x01                 | 66 41 83 5a 7f 01             |
    | sbb word [r10 + 0x80], 0x01                 | 66 41 83 9a 80 00 00 00 01    |
    | sbb word [r10 - 0x80], 0x01                 | 66 41 83 5a 80 01             |
    | sbb word [r10 - 0x81], 0x01                 | 66 41 83 9a 7f ff ff ff 01    |
    | sbb word [rax], 0x00                        | 66 83 18 00                   |
    | sbb word [rax], 0x7f                        | 66 83 18 7f                   |
    | sbb word [rax], 0x80                        | 66 83 18 80                   |
    | sbb word [rax], 0xff                        | 66 83 18 ff                   |
    | sbb word [rcx], 0x7f                        | 66 83 19 7f                   |
    | sbb word [rdx], 0x80                        | 66 83 1a 80                   |
    | sbb word [rbx], 0xff                        | 66 83 1b ff                   |
    | sbb word [rsp], 0x00                        | 66 83 1c 24 00                |
    | sbb word [rsi], 0x7f                        | 66 83 1e 7f                   |
    | sbb word [rdi], 0x80                        | 66 83 1f 80                   |
    | sbb word [r8], 0xff                         | 66 41 83 18 ff                |
    | sbb word [r9], 0x00                         | 66 41 83 19 00                |
    | sbb word [r11], 0x7f                        | 66 41 83 1b 7f                |
    | sbb word [r12], 0x80                        | 66 41 83 1c 24 80             |
    | sbb word [r13], 0xff                        | 66 41 83 5d 00 ff             |
    | sbb word [r14], 0x00                        | 66 41 83 1e 00                |
    | sbb word [rax + 1 * rcx], 0x7f              | 66 83 1c 08 7f                |
    | sbb word [rcx + 1 * rcx], 0x80              | 66 83 1c 09 80                |
    | sbb word [rdx + 1 * rcx], 0xff              | 66 83 1c 0a ff                |
    | sbb word [rbx + 1 * rcx], 0x00              | 66 83 1c 0b 00                |
    | sbb word [rbp + 1 * rcx], 0x7f              | 66 83 5c 0d 00 7f             |
    | sbb word [rsi + 1 * rcx], 0x80              | 66 83 1c 0e 80                |
    | sbb word [rdi + 1 * rcx], 0xff              | 66 83 1c 0f ff                |
    | sbb word [r8 + 1 * rcx], 0x00               | 66 41 83 1c 08 00             |
    | sbb word [r10 + 1 * rcx], 0x7f              | 66 41 83 1c 0a 7f             |
    | sbb word [r11 + 1 * rcx], 0x80              | 66 41 83 1c 0b 80             |
    | sbb word [r12 + 1 * rcx], 0xff              | 66 41 83 1c 0c ff             |
    | sbb word [r13 + 1 * rcx], 0x00              | 66 41 83 5c 0d 00 00          |
    | sbb word [r15 + 1 * rcx], 0x7f              | 66 41 83 1c 0f 7f             |
    | sbb word [rax + 1 * rax], 0x80              | 66 83 1c 00 80                |
    | sbb word [rax + 1 * rdx], 0xff              | 66 83 1c 10 ff                |
    | sbb word [rax + 1 * rbx], 0x00              | 66 83 1c 18 00                |
    | sbb word [rax + 1 * rsi], 0x7f              | 66 83 1c 30 7f                |
    | sbb word [rax + 1 * rdi], 0x80              | 66 83 1c 38 80                |
    | sbb word [rax + 1 * r8], 0xff               | 66 42 83 1c 00 ff             |
    | sbb word [rax + 1 * r9], 0x00               | 66 42 83 1c 08 00             |
    | sbb word [rax + 1 * r11], 0x7f              | 66 42 83 1c 18 7f             |
    | sbb word [rax + 1 * r12], 0x80              | 66 42 83 1c 20 80             |
    | sbb word [rax + 1 * r13], 0xff              | 66 42 83 1c 28 ff             |
    | sbb word [rax + 1 * r14], 0x00              | 66 42 83 1c 30 00             |
    | sbb word [rax + 2 * rcx], 0x7f              | 66 83 1c 48 7f                |
    | sbb word [rax + 4 * rcx], 0x80              | 66 83 1c 88 80                |
    | sbb word [rax + 8 * rcx], 0xff              | 66 83 1c c8 ff                |
    | sbb word [r8 + 1 * r9], 0x00                | 66 43 83 1c 08 00             |
    | sbb word [r8 + 4 * r9], 0x7f                | 66 43 83 1c 88 7f             |
    | sbb word [r8 + 8 * r9], 0x80                | 66 43 83 1c c8 80             |
    | sbb word [1 * rcx], 0xff                    | 66 83 1c 0d 00 00 00 00 ff    |
    | sbb word [2 * rcx], 0x00                    | 66 83 1c 4d 00 00 00 00 00    |
    | sbb word [8 * rcx], 0x7f                    | 66 83 1c cd 00 00 00 00 7f    |
    | sbb word [1 * r9], 0x80                     | 66 42 83 1c 0d 00 00 00 00 80 |
    | sbb word [2 * r9], 0xff                     | 66 42 83 1c 4d 00 00 00 00 ff |
    | sbb word [4 * r9], 0x00                     | 66 42 83 1c 8d 00 00 00 00 00 |
    | sbb word [r13 + 8 * r12], 0x7f              | 66 43 83 5c e5 00 7f          |
    | sbb word [rsp + 4 * r15], 0x80              | 66 42 83 1c bc 80             |
    | sbb word [rax + 1 * rcx + 0x00], 0xff       | 66 83 5c 08 00 ff             |
    | sbb word [rax + 1 * rcx - 0x00], 0x00       | 66 83 5c 08 00 00             |
    | sbb word [rax + 1 * rcx - 0x01], 0x7f       | 66 83 5c 08 ff 7f             |
    | sbb word [rax + 1 * rcx + 0x00000001], 0x80 | 66 83 9c 08 01 00 00 00 80    |
    | sbb word [rax + 1 * rcx - 0x00000001], 0xff | 66 83 9c 08 ff ff ff ff ff    |
    | sbb word [rax + 1 * rcx + 0x7f], 0x00       | 66 83 5c 08 7f 00             |
    | sbb word [rax + 1 * rcx + 0x80], 0x7f       | 66 83 9c 08 80 00 00 00 7f    |
    | sbb word [rax + 1 * rcx - 0x80], 0x80       | 66 83 5c 08 80 80             |
    | sbb word [rax + 1 * rcx - 0x81], 0xff       | 66 83 9c 08 7f ff ff ff ff    |
    | sbb word [rax + 1 * rcx + 0xff], 0x00       | 66 83 9c 08 ff 00 00 00 00    |
    | sbb word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 83 9c 08 ff ff ff 7f 7f    |
    | sbb word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 83 9c 08 01 00 00 80 80    |
    | sbb word [rax + 1 * rcx - 0x80000000], 0xff | 66 83 9c 08 00 00 00 80 ff    |
    | sbb word [r10 + 0x7f], 0x00                 | 66 41 83 5a 7f 00             |
    | sbb word [r10 - 0x80], 0x7f                 | 66 41 83 5a 80 7f             |
    | sbb word [r10 - 0x81], 0x80                 | 66 41 83 9a 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_sbb_addr16_imm8():
    encode(SBB_ADDR16_IMM8)


SBB_ADDR16_IMM16 = """
    | --------------------------------------------- | -------------------------------- |
    | instruction                                   | encoding                         |
    | --------------------------------------------- | -------------------------------- |
    | sbb word [rax], 0x0001                        | 66 81 18 01 00                   |
    | sbb word [rcx], 0x0001                        | 66 81 19 01 00                   |
    | sbb word [rdx], 0x0001                        | 66 81 1a 01 00                   |
    | sbb word [rbx], 0x0001                        | 66 81 1b 01 00                   |
    | sbb word [rsp], 0x0001                        | 66 81 1c 24 01 00                |
    | sbb word [rbp], 0x0001                        | 66 81 5d 00 01 00                |
    | sbb word [rsi], 0x0001                        | 66 81 1e 01 00                   |
    | sbb word [rdi], 0x0001                        | 66 81 1f 01 00                   |
    | sbb word [r8], 0x0001                         | 66 41 81 18 01 00                |
    | sbb word [r9], 0x0001                         | 66 41 81 19 01 00                |
    | sbb word [r10], 0x0001                        | 66 41 81 1a 01 00                |
    | sbb word [r11], 0x0001                        | 66 41 81 1b 01 00                |
    | sbb word [r12], 0x0001                        | 66 41 81 1c 24 01 00             |
    | sbb word [r13], 0x0001                        | 66 41 81 5d 00 01 00             |
    | sbb word [r14], 0x0001                        | 66 41 81 1e 01 00                |
    | sbb word [r15], 0x0001                        | 66 41 81 1f 01 00                |
    | sbb word [rax + 1 * rcx], 0x0001              | 66 81 1c 08 01 00                |
    | sbb word [rcx + 1 * rcx], 0x0001              | 66 81 1c 09 01 00                |
    | sbb word [rdx + 1 * rcx], 0x0001              | 66 81 1c 0a 01 00                |
    | sbb word [rbx + 1 * rcx], 0x0001              | 66 81 1c 0b 01 00                |
    | sbb word [rsp + 1 * rcx], 0x0001              | 66 81 1c 0c 01 00                |
    | sbb word [rbp + 1 * rcx], 0x0001              | 66 81 5c 0d 00 01 00             |
    | sbb word [rsi + 1 * rcx], 0x0001              | 66 81 1c 0e 01 00                |
    | sbb word [rdi + 1 * rcx], 0x0001              | 66 81 1c 0f 01 00                |
    | sbb word [r8 + 1 * rcx], 0x0001               | 66 41 81 1c 08 01 00             |
    | sbb word [r9 + 1 * rcx], 0x0001               | 66 41 81 1c 09 01 00             |
    | sbb word [r10 + 1 * rcx], 0x0001              | 66 41 81 1c 0a 01 00             |
    | sbb word [r11 + 1 * rcx], 0x0001              | 66 41 81 1c 0b 01 00             |
    | sbb word [r12 + 1 * rcx], 0x0001              | 66 41 81 1c 0c 01 00             |
    | sbb word [r13 + 1 * rcx], 0x0001              | 66 41 81 5c 0d 00 01 00          |
    | sbb word [r14 + 1 * rcx], 0x0001              | 66 41 81 1c 0e 01 00             |
    | sbb word [r15 + 1 * rcx], 0x0001              | 66 41 81 1c 0f 01 00             |
    | sbb word [rax + 1 * rax], 0x0001              | 66 81 1c 00 01 00                |
    | sbb word [rax + 1 * rdx], 0x0001              | 66 81 1c 10 01 00                |
    | sbb word [rax + 1 * rbx], 0x0001              | 66 81 1c 18 01 00                |
    | sbb word [rax + 1 * rbp], 0x0001              | 66 81 1c 28 01 00                |
    | sbb word [rax + 1 * rsi], 0x0001              | 66 81 1c 30 01 00                |
    | sbb word [rax + 1 * rdi], 0x0001              | 66 81 1c 38 01 00                |
    | sbb word [rax + 1 * r8], 0x0001               | 66 42 81 1c 00 01 00             |
    | sbb word [rax + 1 * r9], 0x0001               | 66 42 81 1c 08 01 00             |
    | sbb word [rax + 1 * r10], 0x0001              | 66 42 81 1c 10 01 00             |
    | sbb word [rax + 1 * r11], 0x0001              | 66 42 81 1c 18 01 00             |
    | sbb word [rax + 1 * r12], 0x0001              | 66 42 81 1c 20 01 00             |
    | sbb word [rax + 1 * r13], 0x0001              | 66 42 81 1c 28 01 00             |
    | sbb word [rax + 1 * r14], 0x0001              | 66 42 81 1c 30 01 00             |
    | sbb word [rax + 1 * r15], 0x0001              | 66 42 81 1c 38 01 00             |
    | sbb word [rax + 2 * rcx], 0x0001              | 66 81 1c 48 01 00                |
    | sbb word [rax + 4 * rcx], 0x0001              | 66 81 1c 88 01 00                |
    | sbb word [rax + 8 * rcx], 0x0001              | 66 81 1c c8 01 00                |
    | sbb word [r8 + 1 * r9], 0x0001                | 66 43 81 1c 08 01 00             |
    | sbb word [r8 + 2 * r9], 0x0001                | 66 43 81 1c 48 01 00             |
    | sbb word [r8 + 4 * r9], 0x0001                | 66 43 81 1c 88 01 00             |
    | sbb word [r8 + 8 * r9], 0x0001                | 66 43 81 1c c8 01 00             |
    | sbb word [1 * rcx], 0x0001                    | 66 81 1c 0d 00 00 00 00 01 00    |
    | sbb word [2 * rcx], 0x0001                    | 66 81 1c 4d 00 00 00 00 01 00    |
    | sbb word [4 * rcx], 0x0001                    | 66 81 1c 8d 00 00 00 00 01 00    |
    | sbb word [8 * rcx], 0x0001                    | 66 81 1c cd 00 00 00 00 01 00    |
    | sbb word [1 * r9], 0x0001                     | 66 42 81 1c 0d 00 00 00 00 01 00 |
    | sbb word [2 * r9], 0x0001                     | 66 42 81 1c 4d 00 00 00 00 01 00 |
    | sbb word [4 * r9], 0x0001                     | 66 42 81 1c 8d 00 00 00 00 01 00 |
    | sbb word [8 * r9], 0x0001                     | 66 42 81 1c cd 00 00 00 00 01 00 |
    | sbb word [r13 + 8 * r12], 0x0001              | 66 43 81 5c e5 00 01 00          |
    | sbb word [rsp + 4 * r15], 0x0001              | 66 42 81 1c bc 01 00             |
    | sbb word [rax + 1 * rcx + 0x00], 0x0001       | 66 81 5c 08 00 01 00             |
    | sbb word [rax + 1 * rcx - 0x00], 0x0001       | 66 81 5c 08 00 01 00             |
    | sbb word [rax + 1 * rcx + 0x01], 0x0001       | 66 81 5c 08 01 01 00             |
    | sbb word [rax + 1 * rcx - 0x01], 0x0001       | 66 81 5c 08 ff 01 00             |
    | sbb word [rax + 1 * rcx + 0x00000001], 0x0001 | 66 81 9c 08 01 00 00 00 01 00    |
    | sbb word [rax + 1 * rcx - 0x00000001], 0x0001 | 66 81 9c 08 ff ff ff ff 01 00    |
    | sbb word [rax + 1 * rcx + 0x7f], 0x0001       | 66 81 5c 08 7f 01 00             |
    | sbb word [rax + 1 * rcx - 0x7f], 0x0001       | 66 81 5c 08 81 01 00             |
    | sbb word [rax + 1 * rcx + 0x80], 0x0001       | 66 81 9c 08 80 00 00 00 01 00    |
    | sbb word [rax + 1 * rcx - 0x80], 0x0001       | 66 81 5c 08 80 01 00             |
    | sbb word [rax + 1 * rcx - 0x81], 0x0001       | 66 81 9c 08 7f ff ff ff 01 00    |
    | sbb word [rax + 1 * rcx + 0xff], 0x0001       | 66 81 9c 08 ff 00 00 00 01 00    |
    | sbb word [rax + 1 * rcx - 0xff], 0x0001       | 66 81 9c 08 01 ff ff ff 01 00    |
    | sbb word [rax + 1 * rcx + 0x7fffffff], 0x0001 | 66 81 9c 08 ff ff ff 7f 01 00    |
    | sbb word [rax + 1 * rcx - 0x7fffffff], 0x0001 | 66 81 9c 08 01 00 00 80 01 00    |
    | sbb word [rax + 1 * rcx - 0x80000000], 0x0001 | 66 81 9c 08 00 00 00 80 01 00    |
    | sbb word [r10 + 0x7f], 0x0001                 | 66 41 81 5a 7f 01 00             |
    | sbb word [r10 + 0x80], 0x0001                 | 66 41 81 9a 80 00 00 00 01 00    |
    | sbb word [r10 - 0x80], 0x0001                 | 66 41 81 5a 80 01 00             |
    | sbb word [r10 - 0x81], 0x0001                 | 66 41 81 9a 7f ff ff ff 01 00    |
    | sbb word [rax], 0x0000                        | 66 81 18 00 00                   |
    | sbb word [rax], 0x007f                        | 66 81 18 7f 00                   |
    | sbb word [rax], 0x0080                        | 66 81 18 80 00                   |
    | sbb word [rax], 0x00ff                        | 66 81 18 ff 00                   |
    | sbb word [rax], 0x0100                        | 66 81 18 00 01                   |
    | sbb word [rax], 0x7fff                        | 66 81 18 ff 7f                   |
    | sbb word [rax], 0x8000                        | 66 81 18 00 80                   |
    | sbb word [rax], 0xffff                        | 66 81 18 ff ff                   |
    | sbb word [rcx], 0x007f                        | 66 81 19 7f 00                   |
    | sbb word [rdx], 0x0080                        | 66 81 1a 80 00                   |
    | sbb word [rbx], 0x00ff                        | 66 81 1b ff 00                   |
    | sbb word [rsp], 0x0100                        | 66 81 1c 24 00 01                |
    | sbb word [rbp], 0x7fff                        | 66 81 5d 00 ff 7f                |
    | sbb word [rsi], 0x8000                        | 66 81 1e 00 80                   |
    | sbb word [rdi], 0xffff                        | 66 81 1f ff ff                   |
    | sbb word [r8], 0x0000                         | 66 41 81 18 00 00                |
    | sbb word [r10], 0x007f                        | 66 41 81 1a 7f 00                |
    | sbb word [r11], 0x0080                        | 66 41 81 1b 80 00                |
    | sbb word [r12], 0x00ff                        | 66 41 81 1c 24 ff 00             |
    | sbb word [r13], 0x0100                        | 66 41 81 5d 00 00 01             |
    | sbb word [r14], 0x7fff                        | 66 41 81 1e ff 7f                |
    | sbb word [r15], 0x8000                        | 66 41 81 1f 00 80                |
    | sbb word [rax + 1 * rcx], 0xffff              | 66 81 1c 08 ff ff                |
    | sbb word [rcx + 1 * rcx], 0x0000              | 66 81 1c 09 00 00                |
    | sbb word [rbx + 1 * rcx], 0x007f              | 66 81 1c 0b 7f 00                |
    | sbb word [rsp + 1 * rcx], 0x0080              | 66 81 1c 0c 80 00                |
    | sbb word [rbp + 1 * rcx], 0x00ff              | 66 81 5c 0d 00 ff 00             |
    | sbb word [rsi + 1 * rcx], 0x0100              | 66 81 1c 0e 00 01                |
    | sbb word [rdi + 1 * rcx], 0x7fff              | 66 81 1c 0f ff 7f                |
    | sbb word [r8 + 1 * rcx], 0x8000               | 66 41 81 1c 08 00 80             |
    | sbb word [r9 + 1 * rcx], 0xffff               | 66 41 81 1c 09 ff ff             |
    | sbb word [r10 + 1 * rcx], 0x0000              | 66 41 81 1c 0a 00 00             |
    | sbb word [r12 + 1 * rcx], 0x007f              | 66 41 81 1c 0c 7f 00             |
    | sbb word [r13 + 1 * rcx], 0x0080              | 66 41 81 5c 0d 00 80 00          |
    | sbb word [r14 + 1 * rcx], 0x00ff              | 66 41 81 1c 0e ff 00             |
    | sbb word [r15 + 1 * rcx], 0x0100              | 66 41 81 1c 0f 00 01             |
    | sbb word [rax + 1 * rax], 0x7fff              | 66 81 1c 00 ff 7f                |
    | sbb word [rax + 1 * rdx], 0x8000              | 66 81 1c 10 00 80                |
    | sbb word [rax + 1 * rbx], 0xffff              | 66 81 1c 18 ff ff                |
    | sbb word [rax + 1 * rbp], 0x0000              | 66 81 1c 28 00 00                |
    | sbb word [rax + 1 * rdi], 0x007f              | 66 81 1c 38 7f 00                |
    | sbb word [rax + 1 * r8], 0x0080               | 66 42 81 1c 00 80 00             |
    | sbb word [rax + 1 * r9], 0x00ff               | 66 42 81 1c 08 ff 00             |
    | sbb word [rax + 1 * r10], 0x0100              | 66 42 81 1c 10 00 01             |
    | sbb word [rax + 1 * r11], 0x7fff              | 66 42 81 1c 18 ff 7f             |
    | sbb word [rax + 1 * r12], 0x8000              | 66 42 81 1c 20 00 80             |
    | sbb word [rax + 1 * r13], 0xffff              | 66 42 81 1c 28 ff ff             |
    | sbb word [rax + 1 * r14], 0x0000              | 66 42 81 1c 30 00 00             |
    | sbb word [rax + 2 * rcx], 0x007f              | 66 81 1c 48 7f 00                |
    | sbb word [rax + 4 * rcx], 0x0080              | 66 81 1c 88 80 00                |
    | sbb word [rax + 8 * rcx], 0x00ff              | 66 81 1c c8 ff 00                |
    | sbb word [r8 + 1 * r9], 0x0100                | 66 43 81 1c 08 00 01             |
    | sbb word [r8 + 2 * r9], 0x7fff                | 66 43 81 1c 48 ff 7f             |
    | sbb word [r8 + 4 * r9], 0x8000                | 66 43 81 1c 88 00 80             |
    | sbb word [r8 + 8 * r9], 0xffff                | 66 43 81 1c c8 ff ff             |
    | sbb word [1 * rcx], 0x0000                    | 66 81 1c 0d 00 00 00 00 00 00    |
    | sbb word [4 * rcx], 0x007f                    | 66 81 1c 8d 00 00 00 00 7f 00    |
    | sbb word [8 * rcx], 0x0080                    | 66 81 1c cd 00 00 00 00 80 00    |
    | sbb word [1 * r9], 0x00ff                     | 66 42 81 1c 0d 00 00 00 00 ff 00 |
    | sbb word [2 * r9], 0x0100                     | 66 42 81 1c 4d 00 00 00 00 00 01 |
    | sbb word [4 * r9], 0x7fff                     | 66 42 81 1c 8d 00 00 00 00 ff 7f |
    | sbb word [8 * r9], 0x8000                     | 66 42 81 1c cd 00 00 00 00 00 80 |
    | sbb word [r13 + 8 * r12], 0xffff              | 66 43 81 5c e5 00 ff ff          |
    | sbb word [rsp + 4 * r15], 0x0000              | 66 42 81 1c bc 00 00             |
    | sbb word [rax + 1 * rcx - 0x00], 0x007f       | 66 81 5c 08 00 7f 00             |
    | sbb word [rax + 1 * rcx + 0x01], 0x0080       | 66 81 5c 08 01 80 00             |
    | sbb word [rax + 1 * rcx - 0x01], 0x00ff       | 66 81 5c 08 ff ff 00             |
    | sbb word [rax + 1 * rcx + 0x00000001], 0x0100 | 66 81 9c 08 01 00 00 00 00 01    |
    | sbb word [rax + 1 * rcx - 0x00000001], 0x7fff | 66 81 9c 08 ff ff ff ff ff 7f    |
    | sbb word [rax + 1 * rcx + 0x7f], 0x8000       | 66 81 5c 08 7f 00 80             |
    | sbb word [rax + 1 * rcx - 0x7f], 0xffff       | 66 81 5c 08 81 ff ff             |
    | sbb word [rax + 1 * rcx + 0x80], 0x0000       | 66 81 9c 08 80 00 00 00 00 00    |
    | sbb word [rax + 1 * rcx - 0x81], 0x007f       | 66 81 9c 08 7f ff ff ff 7f 00    |
    | sbb word [rax + 1 * rcx + 0xff], 0x0080       | 66 81 9c 08 ff 00 00 00 80 00    |
    | sbb word [rax + 1 * rcx - 0xff], 0x00ff       | 66 81 9c 08 01 ff ff ff ff 00    |
    | sbb word [rax + 1 * rcx + 0x7fffffff], 0x0100 | 66 81 9c 08 ff ff ff 7f 00 01    |
    | sbb word [rax + 1 * rcx - 0x7fffffff], 0x7fff | 66 81 9c 08 01 00 00 80 ff 7f    |
    | sbb word [rax + 1 * rcx - 0x80000000], 0x8000 | 66 81 9c 08 00 00 00 80 00 80    |
    | sbb word [r10 + 0x7f], 0xffff                 | 66 41 81 5a 7f ff ff             |
    | sbb word [r10 + 0x80], 0x0000                 | 66 41 81 9a 80 00 00 00 00 00    |
    | sbb word [r10 - 0x81], 0x007f                 | 66 41 81 9a 7f ff ff ff 7f 00    |
    | --------------------------------------------- | -------------------------------- |
"""


def can_encode_sbb_addr16_imm16():
    encode(SBB_ADDR16_IMM16)


SBB_ADDR16_REG16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sbb word [rax], cx                          | 66 19 08                   |
    | sbb word [rcx], cx                          | 66 19 09                   |
    | sbb word [rdx], cx                          | 66 19 0a                   |
    | sbb word [rbx], cx                          | 66 19 0b                   |
    | sbb word [rsp], cx                          | 66 19 0c 24                |
    | sbb word [rbp], cx                          | 66 19 4d 00                |
    | sbb word [rsi], cx                          | 66 19 0e                   |
    | sbb word [rdi], cx                          | 66 19 0f                   |
    | sbb word [r8], cx                           | 66 41 19 08                |
    | sbb word [r9], cx                           | 66 41 19 09                |
    | sbb word [r10], cx                          | 66 41 19 0a                |
    | sbb word [r11], cx                          | 66 41 19 0b                |
    | sbb word [r12], cx                          | 66 41 19 0c 24             |
    | sbb word [r13], cx                          | 66 41 19 4d 00             |
    | sbb word [r14], cx                          | 66 41 19 0e                |
    | sbb word [r15], cx                          | 66 41 19 0f                |
    | sbb word [rax + 1 * rcx], cx                | 66 19 0c 08                |
    | sbb word [rcx + 1 * rcx], cx                | 66 19 0c 09                |
    | sbb word [rdx + 1 * rcx], cx                | 66 19 0c 0a                |
    | sbb word [rbx + 1 * rcx], cx                | 66 19 0c 0b                |
    | sbb word [rsp + 1 * rcx], cx                | 66 19 0c 0c                |
    | sbb word [rbp + 1 * rcx], cx                | 66 19 4c 0d 00             |
    | sbb word [rsi + 1 * rcx], cx                | 66 19 0c 0e                |
    | sbb word [rdi + 1 * rcx], cx                | 66 19 0c 0f                |
    | sbb word [r8 + 1 * rcx], cx                 | 66 41 19 0c 08             |
    | sbb word [r9 + 1 * rcx], cx                 | 66 41 19 0c 09             |
    | sbb word [r10 + 1 * rcx], cx                | 66 41 19 0c 0a             |
    | sbb word [r11 + 1 * rcx], cx                | 66 41 19 0c 0b             |
    | sbb word [r12 + 1 * rcx], cx                | 66 41 19 0c 0c             |
    | sbb word [r13 + 1 * rcx], cx                | 66 41 19 4c 0d 00          |
    | sbb word [r14 + 1 * rcx], cx                | 66 41 19 0c 0e             |
    | sbb word [r15 + 1 * rcx], cx                | 66 41 19 0c 0f             |
    | sbb word [rax + 1 * rax], cx                | 66 19 0c 00                |
    | sbb word [rax + 1 * rdx], cx                | 66 19 0c 10                |
    | sbb word [rax + 1 * rbx], cx                | 66 19 0c 18                |
    | sbb word [rax + 1 * rbp], cx                | 66 19 0c 28                |
    | sbb word [rax + 1 * rsi], cx                | 66 19 0c 30                |
    | sbb word [rax + 1 * rdi], cx                | 66 19 0c 38                |
    | sbb word [rax + 1 * r8], cx                 | 66 42 19 0c 00             |
    | sbb word [rax + 1 * r9], cx                 | 66 42 19 0c 08             |
    | sbb word [rax + 1 * r10], cx                | 66 42 19 0c 10             |
    | sbb word [rax + 1 * r11], cx                | 66 42 19 0c 18             |
    | sbb word [rax + 1 * r12], cx                | 66 42 19 0c 20             |
    | sbb word [rax + 1 * r13], cx                | 66 42 19 0c 28             |
    | sbb word [rax + 1 * r14], cx                | 66 42 19 0c 30             |
    | sbb word [rax + 1 * r15], cx                | 66 42 19 0c 38             |
    | sbb word [rax + 2 * rcx], cx                | 66 19 0c 48                |
    | sbb word [rax + 4 * rcx], cx                | 66 19 0c 88                |
    | sbb word [rax + 8 * rcx], cx                | 66 19 0c c8                |
    | sbb word [r8 + 1 * r9], cx                  | 66 43 19 0c 08             |
    | sbb word [r8 + 2 * r9], cx                  | 66 43 19 0c 48             |
    | sbb word [r8 + 4 * r9], cx                  | 66 43 19 0c 88             |
    | sbb word [r8 + 8 * r9], cx                  | 66 43 19 0c c8             |
    | sbb word [1 * rcx], cx                      | 66 19 0c 0d 00 00 00 00    |
    | sbb word [2 * rcx], cx                      | 66 19 0c 4d 00 00 00 00    |
    | sbb word [4 * rcx], cx                      | 66 19 0c 8d 00 00 00 00    |
    | sbb word [8 * rcx], cx                      | 66 19 0c cd 00 00 00 00    |
    | sbb word [1 * r9], cx                       | 66 42 19 0c 0d 00 00 00 00 |
    | sbb word [2 * r9], cx                       | 66 42 19 0c 4d 00 00 00 00 |
    | sbb word [4 * r9], cx                       | 66 42 19 0c 8d 00 00 00 00 |
    | sbb word [8 * r9], cx                       | 66 42 19 0c cd 00 00 00 00 |
    | sbb word [r13 + 8 * r12], cx                | 66 43 19 4c e5 00          |
    | sbb word [rsp + 4 * r15], cx                | 66 42 19 0c bc             |
    | sbb word [rax + 1 * rcx + 0x00], cx         | 66 19 4c 08 00             |
    | sbb word [rax + 1 * rcx - 0x00], cx         | 66 19 4c 08 00             |
    | sbb word [rax + 1 * rcx + 0x01], cx         | 66 19 4c 08 01             |
    | sbb word [rax + 1 * rcx - 0x01], cx         | 66 19 4c 08 ff             |
    | sbb word [rax + 1 * rcx + 0x00000001], cx   | 66 19 8c 08 01 00 00 00    |
    | sbb word [rax + 1 * rcx - 0x00000001], cx   | 66 19 8c 08 ff ff ff ff    |
    | sbb word [rax + 1 * rcx + 0x7f], cx         | 66 19 4c 08 7f             |
    | sbb word [rax + 1 * rcx - 0x7f], cx         | 66 19 4c 08 81             |
    | sbb word [rax + 1 * rcx + 0x80], cx         | 66 19 8c 08 80 00 00 00    |
    | sbb word [rax + 1 * rcx - 0x80], cx         | 66 19 4c 08 80             |
    | sbb word [rax + 1 * rcx - 0x81], cx         | 66 19 8c 08 7f ff ff ff    |
    | sbb word [rax + 1 * rcx + 0xff], cx         | 66 19 8c 08 ff 00 00 00    |
    | sbb word [rax + 1 * rcx - 0xff], cx         | 66 19 8c 08 01 ff ff ff    |
    | sbb word [rax + 1 * rcx + 0x7fffffff], cx   | 66 19 8c 08 ff ff ff 7f    |
    | sbb word [rax + 1 * rcx - 0x7fffffff], cx   | 66 19 8c 08 01 00 00 80    |
    | sbb word [rax + 1 * rcx - 0x80000000], cx   | 66 19 8c 08 00 00 00 80    |
    | sbb word [r10 + 0x7f], cx                   | 66 41 19 4a 7f             |
    | sbb word [r10 + 0x80], cx                   | 66 41 19 8a 80 00 00 00    |
    | sbb word [r10 - 0x80], cx                   | 66 41 19 4a 80             |
    | sbb word [r10 - 0x81], cx                   | 66 41 19 8a 7f ff ff ff    |
    | sbb word [rax], ax                          | 66 19 00                   |
    | sbb word [rax], dx                          | 66 19 10                   |
    | sbb word [rax], bx                          | 66 19 18                   |
    | sbb word [rax], sp                          | 66 19 20                   |
    | sbb word [rax], bp                          | 66 19 28                   |
    | sbb word [rax], si                          | 66 19 30                   |
    | sbb word [rax], di                          | 66 19 38                   |
    | sbb word [rax], r8w                         | 66 44 19 00                |
    | sbb word [rax], r9w                         | 66 44 19 08                |
    | sbb word [rax], r10w                        | 66 44 19 10                |
    | sbb word [rax], r11w                        | 66 44 19 18                |
    | sbb word [rax], r12w                        | 66 44 19 20                |
    | sbb word [rax], r13w                        | 66 44 19 28                |
    | sbb word [rax], r14w                        | 66 44 19 30                |
    | sbb word [rax], r15w                        | 66 44 19 38                |
    | sbb word [rcx], dx                          | 66 19 11                   |
    | sbb word [rdx], bx                          | 66 19 1a                   |
    | sbb word [rbx], sp                          | 66 19 23                   |
    | sbb word [rsp], bp                          | 66 19 2c 24                |
    | sbb word [rbp], si                          | 66 19 75 00                |
    | sbb word [rsi], di                          | 66 19 3e                   |
    | sbb word [rdi], r8w                         | 66 44 19 07                |
    | sbb word [r8], r9w                          | 66 45 19 08                |
    | sbb word [r9], r10w                         | 66 45 19 11                |
    | sbb word [r10], r11w                        | 66 45 19 1a                |
    | sbb word [r11], r12w                        | 66 45 19 23                |
    | sbb word [r12], r13w                        | 66 45 19 2c 24             |
    | sbb word [r13], r14w                        | 66 45 19 75 00             |
    | sbb word [r14], r15w                        | 66 45 19 3e                |
    | sbb word [r15], ax                          | 66 41 19 07                |
    | sbb word [rcx + 1 * rcx], dx                | 66 19 14 09                |
    | sbb word [rdx + 1 * rcx], bx                | 66 19 1c 0a                |
    | sbb word [rbx + 1 * rcx], sp                | 66 19 24 0b                |
    | sbb word [rsp + 1 * rcx], bp                | 66 19 2c 0c                |
    | sbb word [rbp + 1 * rcx], si                | 66 19 74 0d 00             |
    | sbb word [rsi + 1 * rcx], di                | 66 19 3c 0e                |
    | sbb word [rdi + 1 * rcx], r8w               | 66 44 19 04 0f             |
    | sbb word [r8 + 1 * rcx], r9w                | 66 45 19 0c 08             |
    | sbb word [r9 + 1 * rcx], r10w               | 66 45 19 14 09             |
    | sbb word [r10 + 1 * rcx], r11w              | 66 45 19 1c 0a             |
    | sbb word [r11 + 1 * rcx], r12w              | 66 45 19 24 0b             |
    | sbb word [r12 + 1 * rcx], r13w              | 66 45 19 2c 0c             |
    | sbb word [r13 + 1 * rcx], r14w              | 66 45 19 74 0d 00          |
    | sbb word [r14 + 1 * rcx], r15w              | 66 45 19 3c 0e             |
    | sbb word [r15 + 1 * rcx], ax                | 66 41 19 04 0f             |
    | sbb word [rax + 1 * rdx], dx                | 66 19 14 10                |
    | sbb word [rax + 1 * rbx], bx                | 66 19 1c 18                |
    | sbb word [rax + 1 * rbp], sp                | 66 19 24 28                |
    | sbb word [rax + 1 * rsi], bp                | 66 19 2c 30                |
    | sbb word [rax + 1 * rdi], si                | 66 19 34 38                |
    | sbb word [rax + 1 * r8], di                 | 66 42 19 3c 00             |
    | sbb word [rax + 1 * r9], r8w                | 66 46 19 04 08             |
    | sbb word [rax + 1 * r10], r9w               | 66 46 19 0c 10             |
    | sbb word [rax + 1 * r11], r10w              | 66 46 19 14 18             |
    | sbb word [rax + 1 * r12], r11w              | 66 46 19 1c 20             |
    | sbb word [rax + 1 * r13], r12w              | 66 46 19 24 28             |
    | sbb word [rax + 1 * r14], r13w              | 66 46 19 2c 30             |
    | sbb word [rax + 1 * r15], r14w              | 66 46 19 34 38             |
    | sbb word [rax + 2 * rcx], r15w              | 66 44 19 3c 48             |
    | sbb word [rax + 4 * rcx], ax                | 66 19 04 88                |
    | sbb word [r8 + 1 * r9], dx                  | 66 43 19 14 08             |
    | sbb word [r8 + 2 * r9], bx                  | 66 43 19 1c 48             |
    | sbb word [r8 + 4 * r9], sp                  | 66 43 19 24 88             |
    | sbb word [r8 + 8 * r9], bp                  | 66 43 19 2c c8             |
    | sbb word [1 * rcx], si                      | 66 19 34 0d 00 00 00 00    |
    | sbb word [2 * rcx], di                      | 66 19 3c 4d 00 00 00 00    |
    | sbb word [4 * rcx], r8w                     | 66 44 19 04 8d 00 00 00 00 |
    | sbb word [8 * rcx], r9w                     | 66 44 19 0c cd 00 00 00 00 |
    | sbb word [1 * r9], r10w                     | 66 46 19 14 0d 00 00 00 00 |
    | sbb word [2 * r9], r11w                     | 66 46 19 1c 4d 00 00 00 00 |
    | sbb word [4 * r9], r12w                     | 66 46 19 24 8d 00 00 00 00 |
    | sbb word [8 * r9], r13w                     | 66 46 19 2c cd 00 00 00 00 |
    | sbb word [r13 + 8 * r12], r14w              | 66 47 19 74 e5 00          |
    | sbb word [rsp + 4 * r15], r15w              | 66 46 19 3c bc             |
    | sbb word [rax + 1 * rcx + 0x00], ax         | 66 19 44 08 00             |
    | sbb word [rax + 1 * rcx + 0x01], dx         | 66 19 54 08 01             |
    | sbb word [rax + 1 * rcx - 0x01], bx         | 66 19 5c 08 ff             |
    | sbb word [rax + 1 * rcx + 0x00000001], sp   | 66 19 a4 08 01 00 00 00    |
    | sbb word [rax + 1 * rcx - 0x00000001], bp   | 66 19 ac 08 ff ff ff ff    |
    | sbb word [rax + 1 * rcx + 0x7f], si         | 66 19 74 08 7f             |
    | sbb word [rax + 1 * rcx - 0x7f], di         | 66 19 7c 08 81             |
    | sbb word [rax + 1 * rcx + 0x80], r8w        | 66 44 19 84 08 80 00 00 00 |
    | sbb word [rax + 1 * rcx - 0x80], r9w        | 66 44 19 4c 08 80          |
    | sbb word [rax + 1 * rcx - 0x81], r10w       | 66 44 19 94 08 7f ff ff ff |
    | sbb word [rax + 1 * rcx + 0xff], r11w       | 66 44 19 9c 08 ff 00 00 00 |
    | sbb word [rax + 1 * rcx - 0xff], r12w       | 66 44 19 a4 08 01 ff ff ff |
    | sbb word [rax + 1 * rcx + 0x7fffffff], r13w | 66 44 19 ac 08 ff ff ff 7f |
    | sbb word [rax + 1 * rcx - 0x7fffffff], r14w | 66 44 19 b4 08 01 00 00 80 |
    | sbb word [rax + 1 * rcx - 0x80000000], r15w | 66 44 19 bc 08 00 00 00 80 |
    | sbb word [r10 + 0x7f], ax                   | 66 41 19 42 7f             |
    | sbb word [r10 - 0x80], dx                   | 66 41 19 52 80             |
    | sbb word [r10 - 0x81], bx                   | 66 41 19 9a 7f ff ff ff    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sbb_addr16_reg16():
    encode(SBB_ADDR16_REG16)


SBB_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sbb byte [rax], 0x01                        | 80 18 01                   |
    | sbb byte [rcx], 0x01                        | 80 19 01                   |
    | sbb byte [rdx], 0x01                        | 80 1a 01                   |
    | sbb byte [rbx], 0x01                        | 80 1b 01                   |
    | sbb byte [rsp], 0x01                        | 80 1c 24 01                |
    | sbb byte [rbp], 0x01                        | 80 5d 00 01                |
    | sbb byte [rsi], 0x01                        | 80 1e 01                   |
    | sbb byte [rdi], 0x01                        | 80 1f 01                   |
    | sbb byte [r8], 0x01                         | 41 80 18 01                |
    | sbb byte [r9], 0x01                         | 41 80 19 01                |
    | sbb byte [r10], 0x01                        | 41 80 1a 01                |
    | sbb byte [r11], 0x01                        | 41 80 1b 01                |
    | sbb byte [r12], 0x01                        | 41 80 1c 24 01             |
    | sbb byte [r13], 0x01                        | 41 80 5d 00 01             |
    | sbb byte [r14], 0x01                        | 41 80 1e 01                |
    | sbb byte [r15], 0x01                        | 41 80 1f 01                |
    | sbb byte [rax + 1 * rcx], 0x01              | 80 1c 08 01                |
    | sbb byte [rcx + 1 * rcx], 0x01              | 80 1c 09 01                |
    | sbb byte [rdx + 1 * rcx], 0x01              | 80 1c 0a 01                |
    | sbb byte [rbx + 1 * rcx], 0x01              | 80 1c 0b 01                |
    | sbb byte [rsp + 1 * rcx], 0x01              | 80 1c 0c 01                |
    | sbb byte [rbp + 1 * rcx], 0x01              | 80 5c 0d 00 01             |
    | sbb byte [rsi + 1 * rcx], 0x01              | 80 1c 0e 01                |
    | sbb byte [rdi + 1 * rcx], 0x01              | 80 1c 0f 01                |
    | sbb byte [r8 + 1 * rcx], 0x01               | 41 80 1c 08 01             |
    | sbb byte [r9 + 1 * rcx], 0x01               | 41 80 1c 09 01             |
    | sbb byte [r10 + 1 * rcx], 0x01              | 41 80 1c 0a 01             |
    | sbb byte [r11 + 1 * rcx], 0x01              | 41 80 1c 0b 01             |
    | sbb byte [r12 + 1 * rcx], 0x01              | 41 80 1c 0c 01             |
    | sbb byte [r13 + 1 * rcx], 0x01              | 41 80 5c 0d 00 01          |
    | sbb byte [r14 + 1 * rcx], 0x01              | 41 80 1c 0e 01             |
    | sbb byte [r15 + 1 * rcx], 0x01              | 41 80 1c 0f 01             |
    | sbb byte [rax + 1 * rax], 0x01              | 80 1c 00 01                |
    | sbb byte [rax + 1 * rdx], 0x01              | 80 1c 10 01                |
    | sbb byte [rax + 1 * rbx], 0x01              | 80 1c 18 01                |
    | sbb byte [rax + 1 * rbp], 0x01              | 80 1c 28 01                |
    | sbb byte [rax + 1 * rsi], 0x01              | 80 1c 30 01                |
    | sbb byte [rax + 1 * rdi], 0x01              | 80 1c 38 01                |
    | sbb byte [rax + 1 * r8], 0x01               | 42 80 1c 00 01             |
    | sbb byte [rax + 1 * r9], 0x01               | 42 80 1c 08 01             |
    | sbb byte [rax + 1 * r10], 0x01              | 42 80 1c 10 01             |
    | sbb byte [rax + 1 * r11], 0x01              | 42 80 1c 18 01             |
    | sbb byte [rax + 1 * r12], 0x01              | 42 80 1c 20 01             |
    | sbb byte [rax + 1 * r13], 0x01              | 42 80 1c 28 01             |
    | sbb byte [rax + 1 * r14], 0x01              | 42 80 1c 30 01             |
    | sbb byte [rax + 1 * r15], 0x01              | 42 80 1c 38 01             |
    | sbb byte [rax + 2 * rcx], 0x01              | 80 1c 48 01                |
    | sbb byte [rax + 4 * rcx], 0x01              | 80 1c 88 01                |
    | sbb byte [rax + 8 * rcx], 0x01              | 80 1c c8 01                |
    | sbb byte [r8 + 1 * r9], 0x01                | 43 80 1c 08 01             |
    | sbb byte [r8 + 2 * r9], 0x01                | 43 80 1c 48 01             |
    | sbb byte [r8 + 4 * r9], 0x01                | 43 80 1c 88 01             |
    | sbb byte [r8 + 8 * r9], 0x01                | 43 80 1c c8 01             |
    | sbb byte [1 * rcx], 0x01                    | 80 1c 0d 00 00 00 00 01    |
    | sbb byte [2 * rcx], 0x01                    | 80 1c 4d 00 00 00 00 01    |
    | sbb byte [4 * rcx], 0x01                    | 80 1c 8d 00 00 00 00 01    |
    | sbb byte [8 * rcx], 0x01                    | 80 1c cd 00 00 00 00 01    |
    | sbb byte [1 * r9], 0x01                     | 42 80 1c 0d 00 00 00 00 01 |
    | sbb byte [2 * r9], 0x01                     | 42 80 1c 4d 00 00 00 00 01 |
    | sbb byte [4 * r9], 0x01                     | 42 80 1c 8d 00 00 00 00 01 |
    | sbb byte [8 * r9], 0x01                     | 42 80 1c cd 00 00 00 00 01 |
    | sbb byte [r13 + 8 * r12], 0x01              | 43 80 5c e5 00 01          |
    | sbb byte [rsp + 4 * r15], 0x01              | 42 80 1c bc 01             |
    | sbb byte [rax + 1 * rcx + 0x00], 0x01       | 80 5c 08 00 01             |
    | sbb byte [rax + 1 * rcx - 0x00], 0x01       | 80 5c 08 00 01             |
    | sbb byte [rax + 1 * rcx + 0x01], 0x01       | 80 5c 08 01 01             |
    | sbb byte [rax + 1 * rcx - 0x01], 0x01       | 80 5c 08 ff 01             |
    | sbb byte [rax + 1 * rcx + 0x00000001], 0x01 | 80 9c 08 01 00 00 00 01    |
    | sbb byte [rax + 1 * rcx - 0x00000001], 0x01 | 80 9c 08 ff ff ff ff 01    |
    | sbb byte [rax + 1 * rcx + 0x7f], 0x01       | 80 5c 08 7f 01             |
    | sbb byte [rax + 1 * rcx - 0x7f], 0x01       | 80 5c 08 81 01             |
    | sbb byte [rax + 1 * rcx + 0x80], 0x01       | 80 9c 08 80 00 00 00 01    |
    | sbb byte [rax + 1 * rcx - 0x80], 0x01       | 80 5c 08 80 01             |
    | sbb byte [rax + 1 * rcx - 0x81], 0x01       | 80 9c 08 7f ff ff ff 01    |
    | sbb byte [rax + 1 * rcx + 0xff], 0x01       | 80 9c 08 ff 00 00 00 01    |
    | sbb byte [rax + 1 * rcx - 0xff], 0x01       | 80 9c 08 01 ff ff ff 01    |
    | sbb byte [rax + 1 * rcx + 0x7fffffff], 0x01 | 80 9c 08 ff ff ff 7f 01    |
    | sbb byte [rax + 1 * rcx - 0x7fffffff], 0x01 | 80 9c 08 01 00 00 80 01    |
    | sbb byte [rax + 1 * rcx - 0x80000000], 0x01 | 80 9c 08 00 00 00 80 01    |
    | sbb byte [r10 + 0x7f], 0x01                 | 41 80 5a 7f 01             |
    | sbb byte [r10 + 0x80], 0x01                 | 41 80 9a 80 00 00 00 01    |
    | sbb byte [r10 - 0x80], 0x01                 | 41 80 5a 80 01             |
    | sbb byte [r10 - 0x81], 0x01                 | 41 80 9a 7f ff ff ff 01    |
    | sbb byte [rax], 0x00                        | 80 18 00                   |
    | sbb byte [rax], 0x7f                        | 80 18 7f                   |
    | sbb byte [rax], 0x80                        | 80 18 80                   |
    | sbb byte [rax], 0xff                        | 80 18 ff                   |
    | sbb byte [rcx], 0x7f                        | 80 19 7f                   |
    | sbb byte [rdx], 0x80                        | 80 1a 80                   |
    | sbb byte [rbx], 0xff                        | 80 1b ff                   |
    | sbb byte [rsp], 0x00                        | 80 1c 24 00                |
    | sbb byte [rsi], 0x7f                        | 80 1e 7f                   |
    | sbb byte [rdi], 0x80                        | 80 1f 80                   |
    | sbb byte [r8], 0xff                         | 41 80 18 ff                |
    | sbb byte [r9], 0x00                         | 41 80 19 00                |
    | sbb byte [r11], 0x7f                        | 41 80 1b 7f                |
    | sbb byte [r12], 0x80                        | 41 80 1c 24 80             |
    | sbb byte [r13], 0xff                        | 41 80 5d 00 ff             |
    | sbb byte [r14], 0x00                        | 41 80 1e 00                |
    | sbb byte [rax + 1 * rcx], 0x7f              | 80 1c 08 7f                |
    | sbb byte [rcx + 1 * rcx], 0x80              | 80 1c 09 80                |
    | sbb byte [rdx + 1 * rcx], 0xff              | 80 1c 0a ff                |
    | sbb byte [rbx + 1 * rcx], 0x00              | 80 1c 0b 00                |
    | sbb byte [rbp + 1 * rcx], 0x7f              | 80 5c 0d 00 7f             |
    | sbb byte [rsi + 1 * rcx], 0x80              | 80 1c 0e 80                |
    | sbb byte [rdi + 1 * rcx], 0xff              | 80 1c 0f ff                |
    | sbb byte [r8 + 1 * rcx], 0x00               | 41 80 1c 08 00             |
    | sbb byte [r10 + 1 * rcx], 0x7f              | 41 80 1c 0a 7f             |
    | sbb byte [r11 + 1 * rcx], 0x80              | 41 80 1c 0b 80             |
    | sbb byte [r12 + 1 * rcx], 0xff              | 41 80 1c 0c ff             |
    | sbb byte [r13 + 1 * rcx], 0x00              | 41 80 5c 0d 00 00          |
    | sbb byte [r15 + 1 * rcx], 0x7f              | 41 80 1c 0f 7f             |
    | sbb byte [rax + 1 * rax], 0x80              | 80 1c 00 80                |
    | sbb byte [rax + 1 * rdx], 0xff              | 80 1c 10 ff                |
    | sbb byte [rax + 1 * rbx], 0x00              | 80 1c 18 00                |
    | sbb byte [rax + 1 * rsi], 0x7f              | 80 1c 30 7f                |
    | sbb byte [rax + 1 * rdi], 0x80              | 80 1c 38 80                |
    | sbb byte [rax + 1 * r8], 0xff               | 42 80 1c 00 ff             |
    | sbb byte [rax + 1 * r9], 0x00               | 42 80 1c 08 00             |
    | sbb byte [rax + 1 * r11], 0x7f              | 42 80 1c 18 7f             |
    | sbb byte [rax + 1 * r12], 0x80              | 42 80 1c 20 80             |
    | sbb byte [rax + 1 * r13], 0xff              | 42 80 1c 28 ff             |
    | sbb byte [rax + 1 * r14], 0x00              | 42 80 1c 30 00             |
    | sbb byte [rax + 2 * rcx], 0x7f              | 80 1c 48 7f                |
    | sbb byte [rax + 4 * rcx], 0x80              | 80 1c 88 80                |
    | sbb byte [rax + 8 * rcx], 0xff              | 80 1c c8 ff                |
    | sbb byte [r8 + 1 * r9], 0x00                | 43 80 1c 08 00             |
    | sbb byte [r8 + 4 * r9], 0x7f                | 43 80 1c 88 7f             |
    | sbb byte [r8 + 8 * r9], 0x80                | 43 80 1c c8 80             |
    | sbb byte [1 * rcx], 0xff                    | 80 1c 0d 00 00 00 00 ff    |
    | sbb byte [2 * rcx], 0x00                    | 80 1c 4d 00 00 00 00 00    |
    | sbb byte [8 * rcx], 0x7f                    | 80 1c cd 00 00 00 00 7f    |
    | sbb byte [1 * r9], 0x80                     | 42 80 1c 0d 00 00 00 00 80 |
    | sbb byte [2 * r9], 0xff                     | 42 80 1c 4d 00 00 00 00 ff |
    | sbb byte [4 * r9], 0x00                     | 42 80 1c 8d 00 00 00 00 00 |
    | sbb byte [r13 + 8 * r12], 0x7f              | 43 80 5c e5 00 7f          |
    | sbb byte [rsp + 4 * r15], 0x80              | 42 80 1c bc 80             |
    | sbb byte [rax + 1 * rcx + 0x00], 0xff       | 80 5c 08 00 ff             |
    | sbb byte [rax + 1 * rcx - 0x00], 0x00       | 80 5c 08 00 00             |
    | sbb byte [rax + 1 * rcx - 0x01], 0x7f       | 80 5c 08 ff 7f             |
    | sbb byte [rax + 1 * rcx + 0x00000001], 0x80 | 80 9c 08 01 00 00 00 80    |
    | sbb byte [rax + 1 * rcx - 0x00000001], 0xff | 80 9c 08 ff ff ff ff ff    |
    | sbb byte [rax + 1 * rcx + 0x7f], 0x00       | 80 5c 08 7f 00             |
    | sbb byte [rax + 1 * rcx + 0x80], 0x7f       | 80 9c 08 80 00 00 00 7f    |
    | sbb byte [rax + 1 * rcx - 0x80], 0x80       | 80 5c 08 80 80             |
    | sbb byte [rax + 1 * rcx - 0x81], 0xff       | 80 9c 08 7f ff ff ff ff    |
    | sbb byte [rax + 1 * rcx + 0xff], 0x00       | 80 9c 08 ff 00 00 00 00    |
    | sbb byte [rax + 1 * rcx + 0x7fffffff], 0x7f | 80 9c 08 ff ff ff 7f 7f    |
    | sbb byte [rax + 1 * rcx - 0x7fffffff], 0x80 | 80 9c 08 01 00 00 80 80    |
    | sbb byte [rax + 1 * rcx - 0x80000000], 0xff | 80 9c 08 00 00 00 80 ff    |
    | sbb byte [r10 + 0x7f], 0x00                 | 41 80 5a 7f 00             |
    | sbb byte [r10 - 0x80], 0x7f                 | 41 80 5a 80 7f             |
    | sbb byte [r10 - 0x81], 0x80                 | 41 80 9a 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sbb_addr8_imm8():
    encode(SBB_ADDR8_IMM8)


SBB_ADDR8_REG8 = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | sbb byte [rax], cl                         | 18 08                   |
    | sbb byte [rcx], cl                         | 18 09                   |
    | sbb byte [rdx], cl                         | 18 0a                   |
    | sbb byte [rbx], cl                         | 18 0b                   |
    | sbb byte [rsp], cl                         | 18 0c 24                |
    | sbb byte [rbp], cl                         | 18 4d 00                |
    | sbb byte [rsi], cl                         | 18 0e                   |
    | sbb byte [rdi], cl                         | 18 0f                   |
    | sbb byte [r8], cl                          | 41 18 08                |
    | sbb byte [r9], cl                          | 41 18 09                |
    | sbb byte [r10], cl                         | 41 18 0a                |
    | sbb byte [r11], cl                         | 41 18 0b                |
    | sbb byte [r12], cl                         | 41 18 0c 24             |
    | sbb byte [r13], cl                         | 41 18 4d 00             |
    | sbb byte [r14], cl                         | 41 18 0e                |
    | sbb byte [r15], cl                         | 41 18 0f                |
    | sbb byte [rax + 1 * rcx], cl               | 18 0c 08                |
    | sbb byte [rcx + 1 * rcx], cl               | 18 0c 09                |
    | sbb byte [rdx + 1 * rcx], cl               | 18 0c 0a                |
    | sbb byte [rbx + 1 * rcx], cl               | 18 0c 0b                |
    | sbb byte [rsp + 1 * rcx], cl               | 18 0c 0c                |
    | sbb byte [rbp + 1 * rcx], cl               | 18 4c 0d 00             |
    | sbb byte [rsi + 1 * rcx], cl               | 18 0c 0e                |
    | sbb byte [rdi + 1 * rcx], cl               | 18 0c 0f                |
    | sbb byte [r8 + 1 * rcx], cl                | 41 18 0c 08             |
    | sbb byte [r9 + 1 * rcx], cl                | 41 18 0c 09             |
    | sbb byte [r10 + 1 * rcx], cl               | 41 18 0c 0a             |
    | sbb byte [r11 + 1 * rcx], cl               | 41 18 0c 0b             |
    | sbb byte [r12 + 1 * rcx], cl               | 41 18 0c 0c             |
    | sbb byte [r13 + 1 * rcx], cl               | 41 18 4c 0d 00          |
    | sbb byte [r14 + 1 * rcx], cl               | 41 18 0c 0e             |
    | sbb byte [r15 + 1 * rcx], cl               | 41 18 0c 0f             |
    | sbb byte [rax + 1 * rax], cl               | 18 0c 00                |
    | sbb byte [rax + 1 * rdx], cl               | 18 0c 10                |
    | sbb byte [rax + 1 * rbx], cl               | 18 0c 18                |
    | sbb byte [rax + 1 * rbp], cl               | 18 0c 28                |
    | sbb byte [rax + 1 * rsi], cl               | 18 0c 30                |
    | sbb byte [rax + 1 * rdi], cl               | 18 0c 38                |
    | sbb byte [rax + 1 * r8], cl                | 42 18 0c 00             |
    | sbb byte [rax + 1 * r9], cl                | 42 18 0c 08             |
    | sbb byte [rax + 1 * r10], cl               | 42 18 0c 10             |
    | sbb byte [rax + 1 * r11], cl               | 42 18 0c 18             |
    | sbb byte [rax + 1 * r12], cl               | 42 18 0c 20             |
    | sbb byte [rax + 1 * r13], cl               | 42 18 0c 28             |
    | sbb byte [rax + 1 * r14], cl               | 42 18 0c 30             |
    | sbb byte [rax + 1 * r15], cl               | 42 18 0c 38             |
    | sbb byte [rax + 2 * rcx], cl               | 18 0c 48                |
    | sbb byte [rax + 4 * rcx], cl               | 18 0c 88                |
    | sbb byte [rax + 8 * rcx], cl               | 18 0c c8                |
    | sbb byte [r8 + 1 * r9], cl                 | 43 18 0c 08             |
    | sbb byte [r8 + 2 * r9], cl                 | 43 18 0c 48             |
    | sbb byte [r8 + 4 * r9], cl                 | 43 18 0c 88             |
    | sbb byte [r8 + 8 * r9], cl                 | 43 18 0c c8             |
    | sbb byte [1 * rcx], cl                     | 18 0c 0d 00 00 00 00    |
    | sbb byte [2 * rcx], cl                     | 18 0c 4d 00 00 00 00    |
    | sbb byte [4 * rcx], cl                     | 18 0c 8d 00 00 00 00    |
    | sbb byte [8 * rcx], cl                     | 18 0c cd 00 00 00 00    |
    | sbb byte [1 * r9], cl                      | 42 18 0c 0d 00 00 00 00 |
    | sbb byte [2 * r9], cl                      | 42 18 0c 4d 00 00 00 00 |
    | sbb byte [4 * r9], cl                      | 42 18 0c 8d 00 00 00 00 |
    | sbb byte [8 * r9], cl                      | 42 18 0c cd 00 00 00 00 |
    | sbb byte [r13 + 8 * r12], cl               | 43 18 4c e5 00          |
    | sbb byte [rsp + 4 * r15], cl               | 42 18 0c bc             |
    | sbb byte [rax + 1 * rcx + 0x00], cl        | 18 4c 08 00             |
    | sbb byte [rax + 1 * rcx - 0x00], cl        | 18 4c 08 00             |
    | sbb byte [rax + 1 * rcx + 0x01], cl        | 18 4c 08 01             |
    | sbb byte [rax + 1 * rcx - 0x01], cl        | 18 4c 08 ff             |
    | sbb byte [rax + 1 * rcx + 0x00000001], cl  | 18 8c 08 01 00 00 00    |
    | sbb byte [rax + 1 * rcx - 0x00000001], cl  | 18 8c 08 ff ff ff ff    |
    | sbb byte [rax + 1 * rcx + 0x7f], cl        | 18 4c 08 7f             |
    | sbb byte [rax + 1 * rcx - 0x7f], cl        | 18 4c 08 81             |
    | sbb byte [rax + 1 * rcx + 0x80], cl        | 18 8c 08 80 00 00 00    |
    | sbb byte [rax + 1 * rcx - 0x80], cl        | 18 4c 08 80             |
    | sbb byte [rax + 1 * rcx - 0x81], cl        | 18 8c 08 7f ff ff ff    |
    | sbb byte [rax + 1 * rcx + 0xff], cl        | 18 8c 08 ff 00 00 00    |
    | sbb byte [rax + 1 * rcx - 0xff], cl        | 18 8c 08 01 ff ff ff    |
    | sbb byte [rax + 1 * rcx + 0x7fffffff], cl  | 18 8c 08 ff ff ff 7f    |
    | sbb byte [rax + 1 * rcx - 0x7fffffff], cl  | 18 8c 08 01 00 00 80    |
    | sbb byte [rax + 1 * rcx - 0x80000000], cl  | 18 8c 08 00 00 00 80    |
    | sbb byte [r10 + 0x7f], cl                  | 41 18 4a 7f             |
    | sbb byte [r10 + 0x80], cl                  | 41 18 8a 80 00 00 00    |
    | sbb byte [r10 - 0x80], cl                  | 41 18 4a 80             |
    | sbb byte [r10 - 0x81], cl                  | 41 18 8a 7f ff ff ff    |
    | sbb byte [rax], al                         | 18 00                   |
    | sbb byte [rax], dl                         | 18 10                   |
    | sbb byte [rax], bl                         | 18 18                   |
    | sbb byte [rax], spl                        | 40 18 20                |
    | sbb byte [rax], bpl                        | 40 18 28                |
    | sbb byte [rax], sil                        | 40 18 30                |
    | sbb byte [rax], dil                        | 40 18 38                |
    | sbb byte [rax], r8b                        | 44 18 00                |
    | sbb byte [rax], r9b                        | 44 18 08                |
    | sbb byte [rax], r10b                       | 44 18 10                |
    | sbb byte [rax], r11b                       | 44 18 18                |
    | sbb byte [rax], r12b                       | 44 18 20                |
    | sbb byte [rax], r13b                       | 44 18 28                |
    | sbb byte [rax], r14b                       | 44 18 30                |
    | sbb byte [rax], r15b                       | 44 18 38                |
    | sbb byte [rax], ah                         | 18 20                   |
    | sbb byte [rax], ch                         | 18 28                   |
    | sbb byte [rax], dh                         | 18 30                   |
    | sbb byte [rax], bh                         | 18 38                   |
    | sbb byte [rcx], dl                         | 18 11                   |
    | sbb byte [rdx], bl                         | 18 1a                   |
    | sbb byte [rbx], spl                        | 40 18 23                |
    | sbb byte [rsp], bpl                        | 40 18 2c 24             |
    | sbb byte [rbp], sil                        | 40 18 75 00             |
    | sbb byte [rsi], dil                        | 40 18 3e                |
    | sbb byte [rdi], r8b                        | 44 18 07                |
    | sbb byte [r8], r9b                         | 45 18 08                |
    | sbb byte [r9], r10b                        | 45 18 11                |
    | sbb byte [r10], r11b                       | 45 18 1a                |
    | sbb byte [r11], r12b                       | 45 18 23                |
    | sbb byte [r12], r13b                       | 45 18 2c 24             |
    | sbb byte [r13], r14b                       | 45 18 75 00             |
    | sbb byte [r14], r15b                       | 45 18 3e                |
    | sbb byte [r15], ah                         | !! !! !!                |
    | sbb byte [rax + 1 * rcx], ch               | 18 2c 08                |
    | sbb byte [rcx + 1 * rcx], dh               | 18 34 09                |
    | sbb byte [rdx + 1 * rcx], bh               | 18 3c 0a                |
    | sbb byte [rbx + 1 * rcx], al               | 18 04 0b                |
    | sbb byte [rbp + 1 * rcx], dl               | 18 54 0d 00             |
    | sbb byte [rsi + 1 * rcx], bl               | 18 1c 0e                |
    | sbb byte [rdi + 1 * rcx], spl              | 40 18 24 0f             |
    | sbb byte [r8 + 1 * rcx], bpl               | 41 18 2c 08             |
    | sbb byte [r9 + 1 * rcx], sil               | 41 18 34 09             |
    | sbb byte [r10 + 1 * rcx], dil              | 41 18 3c 0a             |
    | sbb byte [r11 + 1 * rcx], r8b              | 45 18 04 0b             |
    | sbb byte [r12 + 1 * rcx], r9b              | 45 18 0c 0c             |
    | sbb byte [r13 + 1 * rcx], r10b             | 45 18 54 0d 00          |
    | sbb byte [r14 + 1 * rcx], r11b             | 45 18 1c 0e             |
    | sbb byte [r15 + 1 * rcx], r12b             | 45 18 24 0f             |
    | sbb byte [rax + 1 * rax], r13b             | 44 18 2c 00             |
    | sbb byte [rax + 1 * rdx], r14b             | 44 18 34 10             |
    | sbb byte [rax + 1 * rbx], r15b             | 44 18 3c 18             |
    | sbb byte [rax + 1 * rbp], ah               | 18 24 28                |
    | sbb byte [rax + 1 * rsi], ch               | 18 2c 30                |
    | sbb byte [rax + 1 * rdi], dh               | 18 34 38                |
    | sbb byte [rax + 1 * r8], bh                | !! !! !!                |
    | sbb byte [rax + 1 * r9], al                | 42 18 04 08             |
    | sbb byte [rax + 1 * r11], dl               | 42 18 14 18             |
    | sbb byte [rax + 1 * r12], bl               | 42 18 1c 20             |
    | sbb byte [rax + 1 * r13], spl              | 42 18 24 28             |
    | sbb byte [rax + 1 * r14], bpl              | 42 18 2c 30             |
    | sbb byte [rax + 1 * r15], sil              | 42 18 34 38             |
    | sbb byte [rax + 2 * rcx], dil              | 40 18 3c 48             |
    | sbb byte [rax + 4 * rcx], r8b              | 44 18 04 88             |
    | sbb byte [rax + 8 * rcx], r9b              | 44 18 0c c8             |
    | sbb byte [r8 + 1 * r9], r10b               | 47 18 14 08             |
    | sbb byte [r8 + 2 * r9], r11b               | 47 18 1c 48             |
    | sbb byte [r8 + 4 * r9], r12b               | 47 18 24 88             |
    | sbb byte [r8 + 8 * r9], r13b               | 47 18 2c c8             |
    | sbb byte [1 * rcx], r14b                   | 44 18 34 0d 00 00 00 00 |
    | sbb byte [2 * rcx], r15b                   | 44 18 3c 4d 00 00 00 00 |
    | sbb byte [4 * rcx], ah                     | 18 24 8d 00 00 00 00    |
    | sbb byte [8 * rcx], ch                     | 18 2c cd 00 00 00 00    |
    | sbb byte [1 * r9], dh                      | !! !! !!                |
    | sbb byte [2 * r9], bh                      | !! !! !!                |
    | sbb byte [4 * r9], al                      | 42 18 04 8d 00 00 00 00 |
    | sbb byte [r13 + 8 * r12], dl               | 43 18 54 e5 00          |
    | sbb byte [rsp + 4 * r15], bl               | 42 18 1c bc             |
    | sbb byte [rax + 1 * rcx + 0x00], spl       | 40 18 64 08 00          |
    | sbb byte [rax + 1 * rcx - 0x00], bpl       | 40 18 6c 08 00          |
    | sbb byte [rax + 1 * rcx + 0x01], sil       | 40 18 74 08 01          |
    | sbb byte [rax + 1 * rcx - 0x01], dil       | 40 18 7c 08 ff          |
    | sbb byte [rax + 1 * rcx + 0x00000001], r8b | 44 18 84 08 01 00 00 00 |
    | sbb byte [rax + 1 * rcx - 0x00000001], r9b | 44 18 8c 08 ff ff ff ff |
    | sbb byte [rax + 1 * rcx + 0x7f], r10b      | 44 18 54 08 7f          |
    | sbb byte [rax + 1 * rcx - 0x7f], r11b      | 44 18 5c 08 81          |
    | sbb byte [rax + 1 * rcx + 0x80], r12b      | 44 18 a4 08 80 00 00 00 |
    | sbb byte [rax + 1 * rcx - 0x80], r13b      | 44 18 6c 08 80          |
    | sbb byte [rax + 1 * rcx - 0x81], r14b      | 44 18 b4 08 7f ff ff ff |
    | sbb byte [rax + 1 * rcx + 0xff], r15b      | 44 18 bc 08 ff 00 00 00 |
    | sbb byte [rax + 1 * rcx - 0xff], ah        | 18 a4 08 01 ff ff ff    |
    | sbb byte [rax + 1 * rcx + 0x7fffffff], ch  | 18 ac 08 ff ff ff 7f    |
    | sbb byte [rax + 1 * rcx - 0x7fffffff], dh  | 18 b4 08 01 00 00 80    |
    | sbb byte [rax + 1 * rcx - 0x80000000], bh  | 18 bc 08 00 00 00 80    |
    | sbb byte [r10 + 0x7f], al                  | 41 18 42 7f             |
    | sbb byte [r10 - 0x80], dl                  | 41 18 52 80             |
    | sbb byte [r10 - 0x81], bl                  | 41 18 9a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_sbb_addr8_reg8():
    encode(SBB_ADDR8_REG8)
