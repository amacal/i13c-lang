from tests.encoding.core import encode, exhaust


def can_exhaust_or():
    exhaust(
        OR_ADDR16_IMM16,
        OR_ADDR16_IMM8,
        OR_ADDR16_REG16,
        OR_ADDR32_IMM32,
        OR_ADDR32_IMM8,
        OR_ADDR32_REG32,
        OR_ADDR64_IMM32,
        OR_ADDR64_IMM8,
        OR_ADDR64_REG64,
        OR_ADDR8_IMM8,
        OR_ADDR8_REG8,
        OR_REG16_ADDR16,
        OR_REG16_IMM16,
        OR_REG16_IMM8,
        OR_REG16_REG16,
        OR_REG32_ADDR32,
        OR_REG32_IMM32,
        OR_REG32_IMM8,
        OR_REG32_REG32,
        OR_REG64_ADDR64,
        OR_REG64_IMM32,
        OR_REG64_IMM8,
        OR_REG64_REG64,
        OR_REG8_ADDR8,
        OR_REG8_IMM8,
        OR_REG8_REG8,
    )


OR_REG64_IMM8 = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | or rax, 0x01 | 48 83 c8 01 | *** | or rax, 0x00 | 48 83 c8 00 |
    | or rcx, 0x01 | 48 83 c9 01 | *** | or rax, 0x7f | 48 83 c8 7f |
    | or rdx, 0x01 | 48 83 ca 01 | *** | or rax, 0x80 | 48 83 c8 80 |
    | or rbx, 0x01 | 48 83 cb 01 | *** | or rax, 0xff | 48 83 c8 ff |
    | or rsp, 0x01 | 48 83 cc 01 | *** | or rcx, 0x7f | 48 83 c9 7f |
    | or rbp, 0x01 | 48 83 cd 01 | *** | or rdx, 0x80 | 48 83 ca 80 |
    | or rsi, 0x01 | 48 83 ce 01 | *** | or rbx, 0xff | 48 83 cb ff |
    | or rdi, 0x01 | 48 83 cf 01 | *** | or rsp, 0x00 | 48 83 cc 00 |
    | or r8, 0x01  | 49 83 c8 01 | *** | or rsi, 0x7f | 48 83 ce 7f |
    | or r9, 0x01  | 49 83 c9 01 | *** | or rdi, 0x80 | 48 83 cf 80 |
    | or r10, 0x01 | 49 83 ca 01 | *** | or r8, 0xff  | 49 83 c8 ff |
    | or r11, 0x01 | 49 83 cb 01 | *** | or r9, 0x00  | 49 83 c9 00 |
    | or r12, 0x01 | 49 83 cc 01 | *** | or r11, 0x7f | 49 83 cb 7f |
    | or r13, 0x01 | 49 83 cd 01 | *** | or r12, 0x80 | 49 83 cc 80 |
    | or r14, 0x01 | 49 83 ce 01 | *** | or r13, 0xff | 49 83 cd ff |
    | or r15, 0x01 | 49 83 cf 01 | *** | or r14, 0x00 | 49 83 ce 00 |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_or_reg64_imm8():
    encode(OR_REG64_IMM8)


OR_REG64_IMM32 = """
    | ------------------ | -------------------- | --- | ------------------ | -------------------- |
    | instruction        | encoding             | *** | instruction        | encoding             |
    | ------------------ | -------------------- | --- | ------------------ | -------------------- |
    | or rax, 0x00000001 | 48 0d 01 00 00 00    | *** | or rax, 0x00007fff | 48 0d ff 7f 00 00    |
    | or rcx, 0x00000001 | 48 81 c9 01 00 00 00 | *** | or rax, 0x00008000 | 48 0d 00 80 00 00    |
    | or rdx, 0x00000001 | 48 81 ca 01 00 00 00 | *** | or rax, 0x0000ffff | 48 0d ff ff 00 00    |
    | or rbx, 0x00000001 | 48 81 cb 01 00 00 00 | *** | or rax, 0x00010000 | 48 0d 00 00 01 00    |
    | or rsp, 0x00000001 | 48 81 cc 01 00 00 00 | *** | or rax, 0x7fffffff | 48 0d ff ff ff 7f    |
    | or rbp, 0x00000001 | 48 81 cd 01 00 00 00 | *** | or rax, 0x80000000 | 48 0d 00 00 00 80    |
    | or rsi, 0x00000001 | 48 81 ce 01 00 00 00 | *** | or rax, 0xffffffff | 48 0d ff ff ff ff    |
    | or rdi, 0x00000001 | 48 81 cf 01 00 00 00 | *** | or rcx, 0x0000007f | 48 81 c9 7f 00 00 00 |
    | or r8, 0x00000001  | 49 81 c8 01 00 00 00 | *** | or rdx, 0x00000080 | 48 81 ca 80 00 00 00 |
    | or r9, 0x00000001  | 49 81 c9 01 00 00 00 | *** | or rbx, 0x000000ff | 48 81 cb ff 00 00 00 |
    | or r10, 0x00000001 | 49 81 ca 01 00 00 00 | *** | or rsp, 0x00000100 | 48 81 cc 00 01 00 00 |
    | or r11, 0x00000001 | 49 81 cb 01 00 00 00 | *** | or rbp, 0x00007fff | 48 81 cd ff 7f 00 00 |
    | or r12, 0x00000001 | 49 81 cc 01 00 00 00 | *** | or rsi, 0x00008000 | 48 81 ce 00 80 00 00 |
    | or r13, 0x00000001 | 49 81 cd 01 00 00 00 | *** | or rdi, 0x0000ffff | 48 81 cf ff ff 00 00 |
    | or r14, 0x00000001 | 49 81 ce 01 00 00 00 | *** | or r8, 0x00010000  | 49 81 c8 00 00 01 00 |
    | or r15, 0x00000001 | 49 81 cf 01 00 00 00 | *** | or r9, 0x7fffffff  | 49 81 c9 ff ff ff 7f |
    | or rax, 0x00000000 | 48 0d 00 00 00 00    | *** | or r10, 0x80000000 | 49 81 ca 00 00 00 80 |
    | or rax, 0x0000007f | 48 0d 7f 00 00 00    | *** | or r11, 0xffffffff | 49 81 cb ff ff ff ff |
    | or rax, 0x00000080 | 48 0d 80 00 00 00    | *** | or r12, 0x00000000 | 49 81 cc 00 00 00 00 |
    | or rax, 0x000000ff | 48 0d ff 00 00 00    | *** | or r14, 0x0000007f | 49 81 ce 7f 00 00 00 |
    | or rax, 0x00000100 | 48 0d 00 01 00 00    | *** | or r15, 0x00000080 | 49 81 cf 80 00 00 00 |
    | ------------------ | -------------------- | --- | ------------------ | -------------------- |
"""


def can_encode_or_reg64_imm32():
    encode(OR_REG64_IMM32)


OR_REG64_REG64 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | or rax, rcx | 48 09 c8 | *** | or rax, r8  | 4c 09 c0 |
    | or rcx, rcx | 48 09 c9 | *** | or rax, r9  | 4c 09 c8 |
    | or rdx, rcx | 48 09 ca | *** | or rax, r10 | 4c 09 d0 |
    | or rbx, rcx | 48 09 cb | *** | or rax, r11 | 4c 09 d8 |
    | or rsp, rcx | 48 09 cc | *** | or rax, r12 | 4c 09 e0 |
    | or rbp, rcx | 48 09 cd | *** | or rax, r13 | 4c 09 e8 |
    | or rsi, rcx | 48 09 ce | *** | or rax, r14 | 4c 09 f0 |
    | or rdi, rcx | 48 09 cf | *** | or rax, r15 | 4c 09 f8 |
    | or r8, rcx  | 49 09 c8 | *** | or rcx, rdx | 48 09 d1 |
    | or r9, rcx  | 49 09 c9 | *** | or rdx, rbx | 48 09 da |
    | or r10, rcx | 49 09 ca | *** | or rbx, rsp | 48 09 e3 |
    | or r11, rcx | 49 09 cb | *** | or rsp, rbp | 48 09 ec |
    | or r12, rcx | 49 09 cc | *** | or rbp, rsi | 48 09 f5 |
    | or r13, rcx | 49 09 cd | *** | or rsi, rdi | 48 09 fe |
    | or r14, rcx | 49 09 ce | *** | or rdi, r8  | 4c 09 c7 |
    | or r15, rcx | 49 09 cf | *** | or r8, r9   | 4d 09 c8 |
    | or rax, rax | 48 09 c0 | *** | or r9, r10  | 4d 09 d1 |
    | or rax, rdx | 48 09 d0 | *** | or r10, r11 | 4d 09 da |
    | or rax, rbx | 48 09 d8 | *** | or r11, r12 | 4d 09 e3 |
    | or rax, rsp | 48 09 e0 | *** | or r12, r13 | 4d 09 ec |
    | or rax, rbp | 48 09 e8 | *** | or r13, r14 | 4d 09 f5 |
    | or rax, rsi | 48 09 f0 | *** | or r14, r15 | 4d 09 fe |
    | or rax, rdi | 48 09 f8 | *** | or r15, rax | 49 09 c7 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_or_reg64_reg64():
    encode(OR_REG64_REG64)


OR_REG64_ADDR64 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | or rax, qword [rcx]                                              | 48 0b 01                               |
    | or rcx, qword [rcx]                                              | 48 0b 09                               |
    | or rdx, qword [rcx]                                              | 48 0b 11                               |
    | or rbx, qword [rcx]                                              | 48 0b 19                               |
    | or rsp, qword [rcx]                                              | 48 0b 21                               |
    | or rbp, qword [rcx]                                              | 48 0b 29                               |
    | or rsi, qword [rcx]                                              | 48 0b 31                               |
    | or rdi, qword [rcx]                                              | 48 0b 39                               |
    | or r8, qword [rcx]                                               | 4c 0b 01                               |
    | or r9, qword [rcx]                                               | 4c 0b 09                               |
    | or r10, qword [rcx]                                              | 4c 0b 11                               |
    | or r11, qword [rcx]                                              | 4c 0b 19                               |
    | or r12, qword [rcx]                                              | 4c 0b 21                               |
    | or r13, qword [rcx]                                              | 4c 0b 29                               |
    | or r14, qword [rcx]                                              | 4c 0b 31                               |
    | or r15, qword [rcx]                                              | 4c 0b 39                               |
    | or rax, qword [rax]                                              | 48 0b 00                               |
    | or rax, qword [rdx]                                              | 48 0b 02                               |
    | or rax, qword [rbx]                                              | 48 0b 03                               |
    | or rax, qword [rsp]                                              | 48 0b 04 24                            |
    | or rax, qword [rbp]                                              | 48 0b 45 00                            |
    | or rax, qword [rsi]                                              | 48 0b 06                               |
    | or rax, qword [rdi]                                              | 48 0b 07                               |
    | or rax, qword [r8]                                               | 49 0b 00                               |
    | or rax, qword [r9]                                               | 49 0b 01                               |
    | or rax, qword [r10]                                              | 49 0b 02                               |
    | or rax, qword [r11]                                              | 49 0b 03                               |
    | or rax, qword [r12]                                              | 49 0b 04 24                            |
    | or rax, qword [r13]                                              | 49 0b 45 00                            |
    | or rax, qword [r14]                                              | 49 0b 06                               |
    | or rax, qword [r15]                                              | 49 0b 07                               |
    | or rax, qword [rax + 1 * rcx]                                    | 48 0b 04 08                            |
    | or rax, qword [rcx + 1 * rcx]                                    | 48 0b 04 09                            |
    | or rax, qword [rdx + 1 * rcx]                                    | 48 0b 04 0a                            |
    | or rax, qword [rbx + 1 * rcx]                                    | 48 0b 04 0b                            |
    | or rax, qword [rsp + 1 * rcx]                                    | 48 0b 04 0c                            |
    | or rax, qword [rbp + 1 * rcx]                                    | 48 0b 44 0d 00                         |
    | or rax, qword [rsi + 1 * rcx]                                    | 48 0b 04 0e                            |
    | or rax, qword [rdi + 1 * rcx]                                    | 48 0b 04 0f                            |
    | or rax, qword [r8 + 1 * rcx]                                     | 49 0b 04 08                            |
    | or rax, qword [r9 + 1 * rcx]                                     | 49 0b 04 09                            |
    | or rax, qword [r10 + 1 * rcx]                                    | 49 0b 04 0a                            |
    | or rax, qword [r11 + 1 * rcx]                                    | 49 0b 04 0b                            |
    | or rax, qword [r12 + 1 * rcx]                                    | 49 0b 04 0c                            |
    | or rax, qword [r13 + 1 * rcx]                                    | 49 0b 44 0d 00                         |
    | or rax, qword [r14 + 1 * rcx]                                    | 49 0b 04 0e                            |
    | or rax, qword [r15 + 1 * rcx]                                    | 49 0b 04 0f                            |
    | or rax, qword [rax + 1 * rax]                                    | 48 0b 04 00                            |
    | or rax, qword [rax + 1 * rdx]                                    | 48 0b 04 10                            |
    | or rax, qword [rax + 1 * rbx]                                    | 48 0b 04 18                            |
    | or rax, qword [rax + 1 * rbp]                                    | 48 0b 04 28                            |
    | or rax, qword [rax + 1 * rsi]                                    | 48 0b 04 30                            |
    | or rax, qword [rax + 1 * rdi]                                    | 48 0b 04 38                            |
    | or rax, qword [rax + 1 * r8]                                     | 4a 0b 04 00                            |
    | or rax, qword [rax + 1 * r9]                                     | 4a 0b 04 08                            |
    | or rax, qword [rax + 1 * r10]                                    | 4a 0b 04 10                            |
    | or rax, qword [rax + 1 * r11]                                    | 4a 0b 04 18                            |
    | or rax, qword [rax + 1 * r12]                                    | 4a 0b 04 20                            |
    | or rax, qword [rax + 1 * r13]                                    | 4a 0b 04 28                            |
    | or rax, qword [rax + 1 * r14]                                    | 4a 0b 04 30                            |
    | or rax, qword [rax + 1 * r15]                                    | 4a 0b 04 38                            |
    | or rax, qword [rax + 2 * rcx]                                    | 48 0b 04 48                            |
    | or rax, qword [rax + 4 * rcx]                                    | 48 0b 04 88                            |
    | or rax, qword [rax + 8 * rcx]                                    | 48 0b 04 c8                            |
    | or rax, qword [r8 + 1 * r9]                                      | 4b 0b 04 08                            |
    | or rax, qword [r8 + 2 * r9]                                      | 4b 0b 04 48                            |
    | or rax, qword [r8 + 4 * r9]                                      | 4b 0b 04 88                            |
    | or rax, qword [r8 + 8 * r9]                                      | 4b 0b 04 c8                            |
    | or rax, qword [1 * rcx]                                          | 48 0b 04 0d 00 00 00 00                |
    | or rax, qword [2 * rcx]                                          | 48 0b 04 4d 00 00 00 00                |
    | or rax, qword [4 * rcx]                                          | 48 0b 04 8d 00 00 00 00                |
    | or rax, qword [8 * rcx]                                          | 48 0b 04 cd 00 00 00 00                |
    | or rax, qword [1 * r9]                                           | 4a 0b 04 0d 00 00 00 00                |
    | or rax, qword [2 * r9]                                           | 4a 0b 04 4d 00 00 00 00                |
    | or rax, qword [4 * r9]                                           | 4a 0b 04 8d 00 00 00 00                |
    | or rax, qword [8 * r9]                                           | 4a 0b 04 cd 00 00 00 00                |
    | or rax, qword [r13 + 8 * r12]                                    | 4b 0b 44 e5 00                         |
    | or rax, qword [rsp + 4 * r15]                                    | 4a 0b 04 bc                            |
    | or rax, qword [rax + 1 * rcx + 0x00]                             | 48 0b 44 08 00                         |
    | or rax, qword [rax + 1 * rcx - 0x00]                             | 48 0b 44 08 00                         |
    | or rax, qword [rax + 1 * rcx + 0x01]                             | 48 0b 44 08 01                         |
    | or rax, qword [rax + 1 * rcx - 0x01]                             | 48 0b 44 08 ff                         |
    | or rax, qword [rax + 1 * rcx + 0x00000001]                       | 48 0b 84 08 01 00 00 00                |
    | or rax, qword [rax + 1 * rcx - 0x00000001]                       | 48 0b 84 08 ff ff ff ff                |
    | or rax, qword [rax + 1 * rcx + 0x7f]                             | 48 0b 44 08 7f                         |
    | or rax, qword [rax + 1 * rcx - 0x7f]                             | 48 0b 44 08 81                         |
    | or rax, qword [rax + 1 * rcx + 0x80]                             | 48 0b 84 08 80 00 00 00                |
    | or rax, qword [rax + 1 * rcx - 0x80]                             | 48 0b 44 08 80                         |
    | or rax, qword [rax + 1 * rcx - 0x81]                             | 48 0b 84 08 7f ff ff ff                |
    | or rax, qword [rax + 1 * rcx + 0xff]                             | 48 0b 84 08 ff 00 00 00                |
    | or rax, qword [rax + 1 * rcx - 0xff]                             | 48 0b 84 08 01 ff ff ff                |
    | or rax, qword [rax + 1 * rcx + 0x7fffffff]                       | 48 0b 84 08 ff ff ff 7f                |
    | or rax, qword [rax + 1 * rcx - 0x7fffffff]                       | 48 0b 84 08 01 00 00 80                |
    | or rax, qword [rax + 1 * rcx - 0x80000000]                       | 48 0b 84 08 00 00 00 80                |
    | or rax, qword [r10 + 0x7f]                                       | 49 0b 42 7f                            |
    | or rax, qword [r10 + 0x80]                                       | 49 0b 82 80 00 00 00                   |
    | or rax, qword [r10 - 0x80]                                       | 49 0b 42 80                            |
    | or rax, qword [r10 - 0x81]                                       | 49 0b 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or rax, qword [rel @prev5]      | 90 90 90 90 90 48 0b 05 f4 ff ff ff    |
    | .prev1: nop; or rax, qword [rel @prev1]                          | 90 48 0b 05 f8 ff ff ff                |
    | or rax, qword [rel @next1]; nop; .next1: nop                     | 48 0b 05 01 00 00 00 90 90             |
    | or rax, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 0b 05 05 00 00 00 90 90 90 90 90 90 |
    | or rcx, qword [rdx]                                              | 48 0b 0a                               |
    | or rdx, qword [rbx]                                              | 48 0b 13                               |
    | or rbx, qword [rsp]                                              | 48 0b 1c 24                            |
    | or rsp, qword [rbp]                                              | 48 0b 65 00                            |
    | or rbp, qword [rsi]                                              | 48 0b 2e                               |
    | or rsi, qword [rdi]                                              | 48 0b 37                               |
    | or rdi, qword [r8]                                               | 49 0b 38                               |
    | or r8, qword [r9]                                                | 4d 0b 01                               |
    | or r9, qword [r10]                                               | 4d 0b 0a                               |
    | or r10, qword [r11]                                              | 4d 0b 13                               |
    | or r11, qword [r12]                                              | 4d 0b 1c 24                            |
    | or r12, qword [r13]                                              | 4d 0b 65 00                            |
    | or r13, qword [r14]                                              | 4d 0b 2e                               |
    | or r14, qword [r15]                                              | 4d 0b 37                               |
    | or r15, qword [rax + 1 * rcx]                                    | 4c 0b 3c 08                            |
    | or rcx, qword [rdx + 1 * rcx]                                    | 48 0b 0c 0a                            |
    | or rdx, qword [rbx + 1 * rcx]                                    | 48 0b 14 0b                            |
    | or rbx, qword [rsp + 1 * rcx]                                    | 48 0b 1c 0c                            |
    | or rsp, qword [rbp + 1 * rcx]                                    | 48 0b 64 0d 00                         |
    | or rbp, qword [rsi + 1 * rcx]                                    | 48 0b 2c 0e                            |
    | or rsi, qword [rdi + 1 * rcx]                                    | 48 0b 34 0f                            |
    | or rdi, qword [r8 + 1 * rcx]                                     | 49 0b 3c 08                            |
    | or r8, qword [r9 + 1 * rcx]                                      | 4d 0b 04 09                            |
    | or r9, qword [r10 + 1 * rcx]                                     | 4d 0b 0c 0a                            |
    | or r10, qword [r11 + 1 * rcx]                                    | 4d 0b 14 0b                            |
    | or r11, qword [r12 + 1 * rcx]                                    | 4d 0b 1c 0c                            |
    | or r12, qword [r13 + 1 * rcx]                                    | 4d 0b 64 0d 00                         |
    | or r13, qword [r14 + 1 * rcx]                                    | 4d 0b 2c 0e                            |
    | or r14, qword [r15 + 1 * rcx]                                    | 4d 0b 34 0f                            |
    | or r15, qword [rax + 1 * rax]                                    | 4c 0b 3c 00                            |
    | or rcx, qword [rax + 1 * rbx]                                    | 48 0b 0c 18                            |
    | or rdx, qword [rax + 1 * rbp]                                    | 48 0b 14 28                            |
    | or rbx, qword [rax + 1 * rsi]                                    | 48 0b 1c 30                            |
    | or rsp, qword [rax + 1 * rdi]                                    | 48 0b 24 38                            |
    | or rbp, qword [rax + 1 * r8]                                     | 4a 0b 2c 00                            |
    | or rsi, qword [rax + 1 * r9]                                     | 4a 0b 34 08                            |
    | or rdi, qword [rax + 1 * r10]                                    | 4a 0b 3c 10                            |
    | or r8, qword [rax + 1 * r11]                                     | 4e 0b 04 18                            |
    | or r9, qword [rax + 1 * r12]                                     | 4e 0b 0c 20                            |
    | or r10, qword [rax + 1 * r13]                                    | 4e 0b 14 28                            |
    | or r11, qword [rax + 1 * r14]                                    | 4e 0b 1c 30                            |
    | or r12, qword [rax + 1 * r15]                                    | 4e 0b 24 38                            |
    | or r13, qword [rax + 2 * rcx]                                    | 4c 0b 2c 48                            |
    | or r14, qword [rax + 4 * rcx]                                    | 4c 0b 34 88                            |
    | or r15, qword [rax + 8 * rcx]                                    | 4c 0b 3c c8                            |
    | or rcx, qword [r8 + 2 * r9]                                      | 4b 0b 0c 48                            |
    | or rdx, qword [r8 + 4 * r9]                                      | 4b 0b 14 88                            |
    | or rbx, qword [r8 + 8 * r9]                                      | 4b 0b 1c c8                            |
    | or rsp, qword [1 * rcx]                                          | 48 0b 24 0d 00 00 00 00                |
    | or rbp, qword [2 * rcx]                                          | 48 0b 2c 4d 00 00 00 00                |
    | or rsi, qword [4 * rcx]                                          | 48 0b 34 8d 00 00 00 00                |
    | or rdi, qword [8 * rcx]                                          | 48 0b 3c cd 00 00 00 00                |
    | or r8, qword [1 * r9]                                            | 4e 0b 04 0d 00 00 00 00                |
    | or r9, qword [2 * r9]                                            | 4e 0b 0c 4d 00 00 00 00                |
    | or r10, qword [4 * r9]                                           | 4e 0b 14 8d 00 00 00 00                |
    | or r11, qword [8 * r9]                                           | 4e 0b 1c cd 00 00 00 00                |
    | or r12, qword [r13 + 8 * r12]                                    | 4f 0b 64 e5 00                         |
    | or r13, qword [rsp + 4 * r15]                                    | 4e 0b 2c bc                            |
    | or r14, qword [rax + 1 * rcx + 0x00]                             | 4c 0b 74 08 00                         |
    | or r15, qword [rax + 1 * rcx - 0x00]                             | 4c 0b 7c 08 00                         |
    | or rcx, qword [rax + 1 * rcx - 0x01]                             | 48 0b 4c 08 ff                         |
    | or rdx, qword [rax + 1 * rcx + 0x00000001]                       | 48 0b 94 08 01 00 00 00                |
    | or rbx, qword [rax + 1 * rcx - 0x00000001]                       | 48 0b 9c 08 ff ff ff ff                |
    | or rsp, qword [rax + 1 * rcx + 0x7f]                             | 48 0b 64 08 7f                         |
    | or rbp, qword [rax + 1 * rcx - 0x7f]                             | 48 0b 6c 08 81                         |
    | or rsi, qword [rax + 1 * rcx + 0x80]                             | 48 0b b4 08 80 00 00 00                |
    | or rdi, qword [rax + 1 * rcx - 0x80]                             | 48 0b 7c 08 80                         |
    | or r8, qword [rax + 1 * rcx - 0x81]                              | 4c 0b 84 08 7f ff ff ff                |
    | or r9, qword [rax + 1 * rcx + 0xff]                              | 4c 0b 8c 08 ff 00 00 00                |
    | or r10, qword [rax + 1 * rcx - 0xff]                             | 4c 0b 94 08 01 ff ff ff                |
    | or r11, qword [rax + 1 * rcx + 0x7fffffff]                       | 4c 0b 9c 08 ff ff ff 7f                |
    | or r12, qword [rax + 1 * rcx - 0x7fffffff]                       | 4c 0b a4 08 01 00 00 80                |
    | or r13, qword [rax + 1 * rcx - 0x80000000]                       | 4c 0b ac 08 00 00 00 80                |
    | or r14, qword [r10 + 0x7f]                                       | 4d 0b 72 7f                            |
    | or r15, qword [r10 + 0x80]                                       | 4d 0b ba 80 00 00 00                   |
    | or rcx, qword [r10 - 0x81]                                       | 49 0b 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or rdx, qword [rel @prev5]      | 90 90 90 90 90 48 0b 15 f4 ff ff ff    |
    | .prev1: nop; or rbx, qword [rel @prev1]                          | 90 48 0b 1d f8 ff ff ff                |
    | or rsp, qword [rel @next1]; nop; .next1: nop                     | 48 0b 25 01 00 00 00 90 90             |
    | or rbp, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 0b 2d 05 00 00 00 90 90 90 90 90 90 |
    | or rsi, qword [rax]                                              | 48 0b 30                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_reg64_addr64():
    encode(OR_REG64_ADDR64)


OR_REG32_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | or eax, 0x01  | 83 c8 01    | *** | or eax, 0x00  | 83 c8 00    |
    | or ecx, 0x01  | 83 c9 01    | *** | or eax, 0x7f  | 83 c8 7f    |
    | or edx, 0x01  | 83 ca 01    | *** | or eax, 0x80  | 83 c8 80    |
    | or ebx, 0x01  | 83 cb 01    | *** | or eax, 0xff  | 83 c8 ff    |
    | or esp, 0x01  | 83 cc 01    | *** | or ecx, 0x7f  | 83 c9 7f    |
    | or ebp, 0x01  | 83 cd 01    | *** | or edx, 0x80  | 83 ca 80    |
    | or esi, 0x01  | 83 ce 01    | *** | or ebx, 0xff  | 83 cb ff    |
    | or edi, 0x01  | 83 cf 01    | *** | or esp, 0x00  | 83 cc 00    |
    | or r8d, 0x01  | 41 83 c8 01 | *** | or esi, 0x7f  | 83 ce 7f    |
    | or r9d, 0x01  | 41 83 c9 01 | *** | or edi, 0x80  | 83 cf 80    |
    | or r10d, 0x01 | 41 83 ca 01 | *** | or r8d, 0xff  | 41 83 c8 ff |
    | or r11d, 0x01 | 41 83 cb 01 | *** | or r9d, 0x00  | 41 83 c9 00 |
    | or r12d, 0x01 | 41 83 cc 01 | *** | or r11d, 0x7f | 41 83 cb 7f |
    | or r13d, 0x01 | 41 83 cd 01 | *** | or r12d, 0x80 | 41 83 cc 80 |
    | or r14d, 0x01 | 41 83 ce 01 | *** | or r13d, 0xff | 41 83 cd ff |
    | or r15d, 0x01 | 41 83 cf 01 | *** | or r14d, 0x00 | 41 83 ce 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_or_reg32_imm8():
    encode(OR_REG32_IMM8)


OR_REG32_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | or eax, 0x00000001  | 0d 01 00 00 00       | *** | or eax, 0x00007fff  | 0d ff 7f 00 00       |
    | or ecx, 0x00000001  | 81 c9 01 00 00 00    | *** | or eax, 0x00008000  | 0d 00 80 00 00       |
    | or edx, 0x00000001  | 81 ca 01 00 00 00    | *** | or eax, 0x0000ffff  | 0d ff ff 00 00       |
    | or ebx, 0x00000001  | 81 cb 01 00 00 00    | *** | or eax, 0x00010000  | 0d 00 00 01 00       |
    | or esp, 0x00000001  | 81 cc 01 00 00 00    | *** | or eax, 0x7fffffff  | 0d ff ff ff 7f       |
    | or ebp, 0x00000001  | 81 cd 01 00 00 00    | *** | or eax, 0x80000000  | 0d 00 00 00 80       |
    | or esi, 0x00000001  | 81 ce 01 00 00 00    | *** | or eax, 0xffffffff  | 0d ff ff ff ff       |
    | or edi, 0x00000001  | 81 cf 01 00 00 00    | *** | or ecx, 0x0000007f  | 81 c9 7f 00 00 00    |
    | or r8d, 0x00000001  | 41 81 c8 01 00 00 00 | *** | or edx, 0x00000080  | 81 ca 80 00 00 00    |
    | or r9d, 0x00000001  | 41 81 c9 01 00 00 00 | *** | or ebx, 0x000000ff  | 81 cb ff 00 00 00    |
    | or r10d, 0x00000001 | 41 81 ca 01 00 00 00 | *** | or esp, 0x00000100  | 81 cc 00 01 00 00    |
    | or r11d, 0x00000001 | 41 81 cb 01 00 00 00 | *** | or ebp, 0x00007fff  | 81 cd ff 7f 00 00    |
    | or r12d, 0x00000001 | 41 81 cc 01 00 00 00 | *** | or esi, 0x00008000  | 81 ce 00 80 00 00    |
    | or r13d, 0x00000001 | 41 81 cd 01 00 00 00 | *** | or edi, 0x0000ffff  | 81 cf ff ff 00 00    |
    | or r14d, 0x00000001 | 41 81 ce 01 00 00 00 | *** | or r8d, 0x00010000  | 41 81 c8 00 00 01 00 |
    | or r15d, 0x00000001 | 41 81 cf 01 00 00 00 | *** | or r9d, 0x7fffffff  | 41 81 c9 ff ff ff 7f |
    | or eax, 0x00000000  | 0d 00 00 00 00       | *** | or r10d, 0x80000000 | 41 81 ca 00 00 00 80 |
    | or eax, 0x0000007f  | 0d 7f 00 00 00       | *** | or r11d, 0xffffffff | 41 81 cb ff ff ff ff |
    | or eax, 0x00000080  | 0d 80 00 00 00       | *** | or r12d, 0x00000000 | 41 81 cc 00 00 00 00 |
    | or eax, 0x000000ff  | 0d ff 00 00 00       | *** | or r14d, 0x0000007f | 41 81 ce 7f 00 00 00 |
    | or eax, 0x00000100  | 0d 00 01 00 00       | *** | or r15d, 0x00000080 | 41 81 cf 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_or_reg32_imm32():
    encode(OR_REG32_IMM32)


OR_REG32_REG32 = """
    | ------------- | -------- | --- | ------------- | -------- |
    | instruction   | encoding | *** | instruction   | encoding |
    | ------------- | -------- | --- | ------------- | -------- |
    | or eax, ecx   | 09 c8    | *** | or eax, r8d   | 44 09 c0 |
    | or ecx, ecx   | 09 c9    | *** | or eax, r9d   | 44 09 c8 |
    | or edx, ecx   | 09 ca    | *** | or eax, r10d  | 44 09 d0 |
    | or ebx, ecx   | 09 cb    | *** | or eax, r11d  | 44 09 d8 |
    | or esp, ecx   | 09 cc    | *** | or eax, r12d  | 44 09 e0 |
    | or ebp, ecx   | 09 cd    | *** | or eax, r13d  | 44 09 e8 |
    | or esi, ecx   | 09 ce    | *** | or eax, r14d  | 44 09 f0 |
    | or edi, ecx   | 09 cf    | *** | or eax, r15d  | 44 09 f8 |
    | or r8d, ecx   | 41 09 c8 | *** | or ecx, edx   | 09 d1    |
    | or r9d, ecx   | 41 09 c9 | *** | or edx, ebx   | 09 da    |
    | or r10d, ecx  | 41 09 ca | *** | or ebx, esp   | 09 e3    |
    | or r11d, ecx  | 41 09 cb | *** | or esp, ebp   | 09 ec    |
    | or r12d, ecx  | 41 09 cc | *** | or ebp, esi   | 09 f5    |
    | or r13d, ecx  | 41 09 cd | *** | or esi, edi   | 09 fe    |
    | or r14d, ecx  | 41 09 ce | *** | or edi, r8d   | 44 09 c7 |
    | or r15d, ecx  | 41 09 cf | *** | or r8d, r9d   | 45 09 c8 |
    | or eax, eax   | 09 c0    | *** | or r9d, r10d  | 45 09 d1 |
    | or eax, edx   | 09 d0    | *** | or r10d, r11d | 45 09 da |
    | or eax, ebx   | 09 d8    | *** | or r11d, r12d | 45 09 e3 |
    | or eax, esp   | 09 e0    | *** | or r12d, r13d | 45 09 ec |
    | or eax, ebp   | 09 e8    | *** | or r13d, r14d | 45 09 f5 |
    | or eax, esi   | 09 f0    | *** | or r14d, r15d | 45 09 fe |
    | or eax, edi   | 09 f8    | *** | or r15d, eax  | 41 09 c7 |
    | ------------- | -------- | --- | ------------- | -------- |
"""


def can_encode_or_reg32_reg32():
    encode(OR_REG32_REG32)


OR_REG32_ADDR32 = """
    | ---------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                      | encoding                            |
    | ---------------------------------------------------------------- | ----------------------------------- |
    | or eax, dword [rcx]                                              | 0b 01                               |
    | or ecx, dword [rcx]                                              | 0b 09                               |
    | or edx, dword [rcx]                                              | 0b 11                               |
    | or ebx, dword [rcx]                                              | 0b 19                               |
    | or esp, dword [rcx]                                              | 0b 21                               |
    | or ebp, dword [rcx]                                              | 0b 29                               |
    | or esi, dword [rcx]                                              | 0b 31                               |
    | or edi, dword [rcx]                                              | 0b 39                               |
    | or r8d, dword [rcx]                                              | 44 0b 01                            |
    | or r9d, dword [rcx]                                              | 44 0b 09                            |
    | or r10d, dword [rcx]                                             | 44 0b 11                            |
    | or r11d, dword [rcx]                                             | 44 0b 19                            |
    | or r12d, dword [rcx]                                             | 44 0b 21                            |
    | or r13d, dword [rcx]                                             | 44 0b 29                            |
    | or r14d, dword [rcx]                                             | 44 0b 31                            |
    | or r15d, dword [rcx]                                             | 44 0b 39                            |
    | or eax, dword [rax]                                              | 0b 00                               |
    | or eax, dword [rdx]                                              | 0b 02                               |
    | or eax, dword [rbx]                                              | 0b 03                               |
    | or eax, dword [rsp]                                              | 0b 04 24                            |
    | or eax, dword [rbp]                                              | 0b 45 00                            |
    | or eax, dword [rsi]                                              | 0b 06                               |
    | or eax, dword [rdi]                                              | 0b 07                               |
    | or eax, dword [r8]                                               | 41 0b 00                            |
    | or eax, dword [r9]                                               | 41 0b 01                            |
    | or eax, dword [r10]                                              | 41 0b 02                            |
    | or eax, dword [r11]                                              | 41 0b 03                            |
    | or eax, dword [r12]                                              | 41 0b 04 24                         |
    | or eax, dword [r13]                                              | 41 0b 45 00                         |
    | or eax, dword [r14]                                              | 41 0b 06                            |
    | or eax, dword [r15]                                              | 41 0b 07                            |
    | or eax, dword [rax + 1 * rcx]                                    | 0b 04 08                            |
    | or eax, dword [rcx + 1 * rcx]                                    | 0b 04 09                            |
    | or eax, dword [rdx + 1 * rcx]                                    | 0b 04 0a                            |
    | or eax, dword [rbx + 1 * rcx]                                    | 0b 04 0b                            |
    | or eax, dword [rsp + 1 * rcx]                                    | 0b 04 0c                            |
    | or eax, dword [rbp + 1 * rcx]                                    | 0b 44 0d 00                         |
    | or eax, dword [rsi + 1 * rcx]                                    | 0b 04 0e                            |
    | or eax, dword [rdi + 1 * rcx]                                    | 0b 04 0f                            |
    | or eax, dword [r8 + 1 * rcx]                                     | 41 0b 04 08                         |
    | or eax, dword [r9 + 1 * rcx]                                     | 41 0b 04 09                         |
    | or eax, dword [r10 + 1 * rcx]                                    | 41 0b 04 0a                         |
    | or eax, dword [r11 + 1 * rcx]                                    | 41 0b 04 0b                         |
    | or eax, dword [r12 + 1 * rcx]                                    | 41 0b 04 0c                         |
    | or eax, dword [r13 + 1 * rcx]                                    | 41 0b 44 0d 00                      |
    | or eax, dword [r14 + 1 * rcx]                                    | 41 0b 04 0e                         |
    | or eax, dword [r15 + 1 * rcx]                                    | 41 0b 04 0f                         |
    | or eax, dword [rax + 1 * rax]                                    | 0b 04 00                            |
    | or eax, dword [rax + 1 * rdx]                                    | 0b 04 10                            |
    | or eax, dword [rax + 1 * rbx]                                    | 0b 04 18                            |
    | or eax, dword [rax + 1 * rbp]                                    | 0b 04 28                            |
    | or eax, dword [rax + 1 * rsi]                                    | 0b 04 30                            |
    | or eax, dword [rax + 1 * rdi]                                    | 0b 04 38                            |
    | or eax, dword [rax + 1 * r8]                                     | 42 0b 04 00                         |
    | or eax, dword [rax + 1 * r9]                                     | 42 0b 04 08                         |
    | or eax, dword [rax + 1 * r10]                                    | 42 0b 04 10                         |
    | or eax, dword [rax + 1 * r11]                                    | 42 0b 04 18                         |
    | or eax, dword [rax + 1 * r12]                                    | 42 0b 04 20                         |
    | or eax, dword [rax + 1 * r13]                                    | 42 0b 04 28                         |
    | or eax, dword [rax + 1 * r14]                                    | 42 0b 04 30                         |
    | or eax, dword [rax + 1 * r15]                                    | 42 0b 04 38                         |
    | or eax, dword [rax + 2 * rcx]                                    | 0b 04 48                            |
    | or eax, dword [rax + 4 * rcx]                                    | 0b 04 88                            |
    | or eax, dword [rax + 8 * rcx]                                    | 0b 04 c8                            |
    | or eax, dword [r8 + 1 * r9]                                      | 43 0b 04 08                         |
    | or eax, dword [r8 + 2 * r9]                                      | 43 0b 04 48                         |
    | or eax, dword [r8 + 4 * r9]                                      | 43 0b 04 88                         |
    | or eax, dword [r8 + 8 * r9]                                      | 43 0b 04 c8                         |
    | or eax, dword [1 * rcx]                                          | 0b 04 0d 00 00 00 00                |
    | or eax, dword [2 * rcx]                                          | 0b 04 4d 00 00 00 00                |
    | or eax, dword [4 * rcx]                                          | 0b 04 8d 00 00 00 00                |
    | or eax, dword [8 * rcx]                                          | 0b 04 cd 00 00 00 00                |
    | or eax, dword [1 * r9]                                           | 42 0b 04 0d 00 00 00 00             |
    | or eax, dword [2 * r9]                                           | 42 0b 04 4d 00 00 00 00             |
    | or eax, dword [4 * r9]                                           | 42 0b 04 8d 00 00 00 00             |
    | or eax, dword [8 * r9]                                           | 42 0b 04 cd 00 00 00 00             |
    | or eax, dword [r13 + 8 * r12]                                    | 43 0b 44 e5 00                      |
    | or eax, dword [rsp + 4 * r15]                                    | 42 0b 04 bc                         |
    | or eax, dword [rax + 1 * rcx + 0x00]                             | 0b 44 08 00                         |
    | or eax, dword [rax + 1 * rcx - 0x00]                             | 0b 44 08 00                         |
    | or eax, dword [rax + 1 * rcx + 0x01]                             | 0b 44 08 01                         |
    | or eax, dword [rax + 1 * rcx - 0x01]                             | 0b 44 08 ff                         |
    | or eax, dword [rax + 1 * rcx + 0x00000001]                       | 0b 84 08 01 00 00 00                |
    | or eax, dword [rax + 1 * rcx - 0x00000001]                       | 0b 84 08 ff ff ff ff                |
    | or eax, dword [rax + 1 * rcx + 0x7f]                             | 0b 44 08 7f                         |
    | or eax, dword [rax + 1 * rcx - 0x7f]                             | 0b 44 08 81                         |
    | or eax, dword [rax + 1 * rcx + 0x80]                             | 0b 84 08 80 00 00 00                |
    | or eax, dword [rax + 1 * rcx - 0x80]                             | 0b 44 08 80                         |
    | or eax, dword [rax + 1 * rcx - 0x81]                             | 0b 84 08 7f ff ff ff                |
    | or eax, dword [rax + 1 * rcx + 0xff]                             | 0b 84 08 ff 00 00 00                |
    | or eax, dword [rax + 1 * rcx - 0xff]                             | 0b 84 08 01 ff ff ff                |
    | or eax, dword [rax + 1 * rcx + 0x7fffffff]                       | 0b 84 08 ff ff ff 7f                |
    | or eax, dword [rax + 1 * rcx - 0x7fffffff]                       | 0b 84 08 01 00 00 80                |
    | or eax, dword [rax + 1 * rcx - 0x80000000]                       | 0b 84 08 00 00 00 80                |
    | or eax, dword [r10 + 0x7f]                                       | 41 0b 42 7f                         |
    | or eax, dword [r10 + 0x80]                                       | 41 0b 82 80 00 00 00                |
    | or eax, dword [r10 - 0x80]                                       | 41 0b 42 80                         |
    | or eax, dword [r10 - 0x81]                                       | 41 0b 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or eax, dword [rel @prev5]      | 90 90 90 90 90 0b 05 f5 ff ff ff    |
    | .prev1: nop; or eax, dword [rel @prev1]                          | 90 0b 05 f9 ff ff ff                |
    | or eax, dword [rel @next1]; nop; .next1: nop                     | 0b 05 01 00 00 00 90 90             |
    | or eax, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 0b 05 05 00 00 00 90 90 90 90 90 90 |
    | or ecx, dword [rdx]                                              | 0b 0a                               |
    | or edx, dword [rbx]                                              | 0b 13                               |
    | or ebx, dword [rsp]                                              | 0b 1c 24                            |
    | or esp, dword [rbp]                                              | 0b 65 00                            |
    | or ebp, dword [rsi]                                              | 0b 2e                               |
    | or esi, dword [rdi]                                              | 0b 37                               |
    | or edi, dword [r8]                                               | 41 0b 38                            |
    | or r8d, dword [r9]                                               | 45 0b 01                            |
    | or r9d, dword [r10]                                              | 45 0b 0a                            |
    | or r10d, dword [r11]                                             | 45 0b 13                            |
    | or r11d, dword [r12]                                             | 45 0b 1c 24                         |
    | or r12d, dword [r13]                                             | 45 0b 65 00                         |
    | or r13d, dword [r14]                                             | 45 0b 2e                            |
    | or r14d, dword [r15]                                             | 45 0b 37                            |
    | or r15d, dword [rax + 1 * rcx]                                   | 44 0b 3c 08                         |
    | or ecx, dword [rdx + 1 * rcx]                                    | 0b 0c 0a                            |
    | or edx, dword [rbx + 1 * rcx]                                    | 0b 14 0b                            |
    | or ebx, dword [rsp + 1 * rcx]                                    | 0b 1c 0c                            |
    | or esp, dword [rbp + 1 * rcx]                                    | 0b 64 0d 00                         |
    | or ebp, dword [rsi + 1 * rcx]                                    | 0b 2c 0e                            |
    | or esi, dword [rdi + 1 * rcx]                                    | 0b 34 0f                            |
    | or edi, dword [r8 + 1 * rcx]                                     | 41 0b 3c 08                         |
    | or r8d, dword [r9 + 1 * rcx]                                     | 45 0b 04 09                         |
    | or r9d, dword [r10 + 1 * rcx]                                    | 45 0b 0c 0a                         |
    | or r10d, dword [r11 + 1 * rcx]                                   | 45 0b 14 0b                         |
    | or r11d, dword [r12 + 1 * rcx]                                   | 45 0b 1c 0c                         |
    | or r12d, dword [r13 + 1 * rcx]                                   | 45 0b 64 0d 00                      |
    | or r13d, dword [r14 + 1 * rcx]                                   | 45 0b 2c 0e                         |
    | or r14d, dword [r15 + 1 * rcx]                                   | 45 0b 34 0f                         |
    | or r15d, dword [rax + 1 * rax]                                   | 44 0b 3c 00                         |
    | or ecx, dword [rax + 1 * rbx]                                    | 0b 0c 18                            |
    | or edx, dword [rax + 1 * rbp]                                    | 0b 14 28                            |
    | or ebx, dword [rax + 1 * rsi]                                    | 0b 1c 30                            |
    | or esp, dword [rax + 1 * rdi]                                    | 0b 24 38                            |
    | or ebp, dword [rax + 1 * r8]                                     | 42 0b 2c 00                         |
    | or esi, dword [rax + 1 * r9]                                     | 42 0b 34 08                         |
    | or edi, dword [rax + 1 * r10]                                    | 42 0b 3c 10                         |
    | or r8d, dword [rax + 1 * r11]                                    | 46 0b 04 18                         |
    | or r9d, dword [rax + 1 * r12]                                    | 46 0b 0c 20                         |
    | or r10d, dword [rax + 1 * r13]                                   | 46 0b 14 28                         |
    | or r11d, dword [rax + 1 * r14]                                   | 46 0b 1c 30                         |
    | or r12d, dword [rax + 1 * r15]                                   | 46 0b 24 38                         |
    | or r13d, dword [rax + 2 * rcx]                                   | 44 0b 2c 48                         |
    | or r14d, dword [rax + 4 * rcx]                                   | 44 0b 34 88                         |
    | or r15d, dword [rax + 8 * rcx]                                   | 44 0b 3c c8                         |
    | or ecx, dword [r8 + 2 * r9]                                      | 43 0b 0c 48                         |
    | or edx, dword [r8 + 4 * r9]                                      | 43 0b 14 88                         |
    | or ebx, dword [r8 + 8 * r9]                                      | 43 0b 1c c8                         |
    | or esp, dword [1 * rcx]                                          | 0b 24 0d 00 00 00 00                |
    | or ebp, dword [2 * rcx]                                          | 0b 2c 4d 00 00 00 00                |
    | or esi, dword [4 * rcx]                                          | 0b 34 8d 00 00 00 00                |
    | or edi, dword [8 * rcx]                                          | 0b 3c cd 00 00 00 00                |
    | or r8d, dword [1 * r9]                                           | 46 0b 04 0d 00 00 00 00             |
    | or r9d, dword [2 * r9]                                           | 46 0b 0c 4d 00 00 00 00             |
    | or r10d, dword [4 * r9]                                          | 46 0b 14 8d 00 00 00 00             |
    | or r11d, dword [8 * r9]                                          | 46 0b 1c cd 00 00 00 00             |
    | or r12d, dword [r13 + 8 * r12]                                   | 47 0b 64 e5 00                      |
    | or r13d, dword [rsp + 4 * r15]                                   | 46 0b 2c bc                         |
    | or r14d, dword [rax + 1 * rcx + 0x00]                            | 44 0b 74 08 00                      |
    | or r15d, dword [rax + 1 * rcx - 0x00]                            | 44 0b 7c 08 00                      |
    | or ecx, dword [rax + 1 * rcx - 0x01]                             | 0b 4c 08 ff                         |
    | or edx, dword [rax + 1 * rcx + 0x00000001]                       | 0b 94 08 01 00 00 00                |
    | or ebx, dword [rax + 1 * rcx - 0x00000001]                       | 0b 9c 08 ff ff ff ff                |
    | or esp, dword [rax + 1 * rcx + 0x7f]                             | 0b 64 08 7f                         |
    | or ebp, dword [rax + 1 * rcx - 0x7f]                             | 0b 6c 08 81                         |
    | or esi, dword [rax + 1 * rcx + 0x80]                             | 0b b4 08 80 00 00 00                |
    | or edi, dword [rax + 1 * rcx - 0x80]                             | 0b 7c 08 80                         |
    | or r8d, dword [rax + 1 * rcx - 0x81]                             | 44 0b 84 08 7f ff ff ff             |
    | or r9d, dword [rax + 1 * rcx + 0xff]                             | 44 0b 8c 08 ff 00 00 00             |
    | or r10d, dword [rax + 1 * rcx - 0xff]                            | 44 0b 94 08 01 ff ff ff             |
    | or r11d, dword [rax + 1 * rcx + 0x7fffffff]                      | 44 0b 9c 08 ff ff ff 7f             |
    | or r12d, dword [rax + 1 * rcx - 0x7fffffff]                      | 44 0b a4 08 01 00 00 80             |
    | or r13d, dword [rax + 1 * rcx - 0x80000000]                      | 44 0b ac 08 00 00 00 80             |
    | or r14d, dword [r10 + 0x7f]                                      | 45 0b 72 7f                         |
    | or r15d, dword [r10 + 0x80]                                      | 45 0b ba 80 00 00 00                |
    | or ecx, dword [r10 - 0x81]                                       | 41 0b 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or edx, dword [rel @prev5]      | 90 90 90 90 90 0b 15 f5 ff ff ff    |
    | .prev1: nop; or ebx, dword [rel @prev1]                          | 90 0b 1d f9 ff ff ff                |
    | or esp, dword [rel @next1]; nop; .next1: nop                     | 0b 25 01 00 00 00 90 90             |
    | or ebp, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 0b 2d 05 00 00 00 90 90 90 90 90 90 |
    | or esi, dword [rax]                                              | 0b 30                               |
    | ---------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_or_reg32_addr32():
    encode(OR_REG32_ADDR32)


OR_REG16_IMM8 = """
    | ------------- | -------------- | --- | ------------- | -------------- |
    | instruction   | encoding       | *** | instruction   | encoding       |
    | ------------- | -------------- | --- | ------------- | -------------- |
    | or ax, 0x01   | 66 83 c8 01    | *** | or ax, 0x00   | 66 83 c8 00    |
    | or cx, 0x01   | 66 83 c9 01    | *** | or ax, 0x7f   | 66 83 c8 7f    |
    | or dx, 0x01   | 66 83 ca 01    | *** | or ax, 0x80   | 66 83 c8 80    |
    | or bx, 0x01   | 66 83 cb 01    | *** | or ax, 0xff   | 66 83 c8 ff    |
    | or sp, 0x01   | 66 83 cc 01    | *** | or cx, 0x7f   | 66 83 c9 7f    |
    | or bp, 0x01   | 66 83 cd 01    | *** | or dx, 0x80   | 66 83 ca 80    |
    | or si, 0x01   | 66 83 ce 01    | *** | or bx, 0xff   | 66 83 cb ff    |
    | or di, 0x01   | 66 83 cf 01    | *** | or sp, 0x00   | 66 83 cc 00    |
    | or r8w, 0x01  | 66 41 83 c8 01 | *** | or si, 0x7f   | 66 83 ce 7f    |
    | or r9w, 0x01  | 66 41 83 c9 01 | *** | or di, 0x80   | 66 83 cf 80    |
    | or r10w, 0x01 | 66 41 83 ca 01 | *** | or r8w, 0xff  | 66 41 83 c8 ff |
    | or r11w, 0x01 | 66 41 83 cb 01 | *** | or r9w, 0x00  | 66 41 83 c9 00 |
    | or r12w, 0x01 | 66 41 83 cc 01 | *** | or r11w, 0x7f | 66 41 83 cb 7f |
    | or r13w, 0x01 | 66 41 83 cd 01 | *** | or r12w, 0x80 | 66 41 83 cc 80 |
    | or r14w, 0x01 | 66 41 83 ce 01 | *** | or r13w, 0xff | 66 41 83 cd ff |
    | or r15w, 0x01 | 66 41 83 cf 01 | *** | or r14w, 0x00 | 66 41 83 ce 00 |
    | ------------- | -------------- | --- | ------------- | -------------- |
"""


def can_encode_or_reg16_imm8():
    encode(OR_REG16_IMM8)


OR_REG16_IMM16 = """
    | --------------- | ----------------- | --- | --------------- | ----------------- |
    | instruction     | encoding          | *** | instruction     | encoding          |
    | --------------- | ----------------- | --- | --------------- | ----------------- |
    | or ax, 0x0001   | 66 0d 01 00       | *** | or ax, 0x00ff   | 66 0d ff 00       |
    | or cx, 0x0001   | 66 81 c9 01 00    | *** | or ax, 0x0100   | 66 0d 00 01       |
    | or dx, 0x0001   | 66 81 ca 01 00    | *** | or ax, 0x7fff   | 66 0d ff 7f       |
    | or bx, 0x0001   | 66 81 cb 01 00    | *** | or ax, 0x8000   | 66 0d 00 80       |
    | or sp, 0x0001   | 66 81 cc 01 00    | *** | or ax, 0xffff   | 66 0d ff ff       |
    | or bp, 0x0001   | 66 81 cd 01 00    | *** | or cx, 0x007f   | 66 81 c9 7f 00    |
    | or si, 0x0001   | 66 81 ce 01 00    | *** | or dx, 0x0080   | 66 81 ca 80 00    |
    | or di, 0x0001   | 66 81 cf 01 00    | *** | or bx, 0x00ff   | 66 81 cb ff 00    |
    | or r8w, 0x0001  | 66 41 81 c8 01 00 | *** | or sp, 0x0100   | 66 81 cc 00 01    |
    | or r9w, 0x0001  | 66 41 81 c9 01 00 | *** | or bp, 0x7fff   | 66 81 cd ff 7f    |
    | or r10w, 0x0001 | 66 41 81 ca 01 00 | *** | or si, 0x8000   | 66 81 ce 00 80    |
    | or r11w, 0x0001 | 66 41 81 cb 01 00 | *** | or di, 0xffff   | 66 81 cf ff ff    |
    | or r12w, 0x0001 | 66 41 81 cc 01 00 | *** | or r8w, 0x0000  | 66 41 81 c8 00 00 |
    | or r13w, 0x0001 | 66 41 81 cd 01 00 | *** | or r10w, 0x007f | 66 41 81 ca 7f 00 |
    | or r14w, 0x0001 | 66 41 81 ce 01 00 | *** | or r11w, 0x0080 | 66 41 81 cb 80 00 |
    | or r15w, 0x0001 | 66 41 81 cf 01 00 | *** | or r12w, 0x00ff | 66 41 81 cc ff 00 |
    | or ax, 0x0000   | 66 0d 00 00       | *** | or r13w, 0x0100 | 66 41 81 cd 00 01 |
    | or ax, 0x007f   | 66 0d 7f 00       | *** | or r14w, 0x7fff | 66 41 81 ce ff 7f |
    | or ax, 0x0080   | 66 0d 80 00       | *** | or r15w, 0x8000 | 66 41 81 cf 00 80 |
    | --------------- | ----------------- | --- | --------------- | ----------------- |
"""


def can_encode_or_reg16_imm16():
    encode(OR_REG16_IMM16)


OR_REG16_REG16 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | or ax, cx     | 66 09 c8    | *** | or ax, r8w    | 66 44 09 c0 |
    | or cx, cx     | 66 09 c9    | *** | or ax, r9w    | 66 44 09 c8 |
    | or dx, cx     | 66 09 ca    | *** | or ax, r10w   | 66 44 09 d0 |
    | or bx, cx     | 66 09 cb    | *** | or ax, r11w   | 66 44 09 d8 |
    | or sp, cx     | 66 09 cc    | *** | or ax, r12w   | 66 44 09 e0 |
    | or bp, cx     | 66 09 cd    | *** | or ax, r13w   | 66 44 09 e8 |
    | or si, cx     | 66 09 ce    | *** | or ax, r14w   | 66 44 09 f0 |
    | or di, cx     | 66 09 cf    | *** | or ax, r15w   | 66 44 09 f8 |
    | or r8w, cx    | 66 41 09 c8 | *** | or cx, dx     | 66 09 d1    |
    | or r9w, cx    | 66 41 09 c9 | *** | or dx, bx     | 66 09 da    |
    | or r10w, cx   | 66 41 09 ca | *** | or bx, sp     | 66 09 e3    |
    | or r11w, cx   | 66 41 09 cb | *** | or sp, bp     | 66 09 ec    |
    | or r12w, cx   | 66 41 09 cc | *** | or bp, si     | 66 09 f5    |
    | or r13w, cx   | 66 41 09 cd | *** | or si, di     | 66 09 fe    |
    | or r14w, cx   | 66 41 09 ce | *** | or di, r8w    | 66 44 09 c7 |
    | or r15w, cx   | 66 41 09 cf | *** | or r8w, r9w   | 66 45 09 c8 |
    | or ax, ax     | 66 09 c0    | *** | or r9w, r10w  | 66 45 09 d1 |
    | or ax, dx     | 66 09 d0    | *** | or r10w, r11w | 66 45 09 da |
    | or ax, bx     | 66 09 d8    | *** | or r11w, r12w | 66 45 09 e3 |
    | or ax, sp     | 66 09 e0    | *** | or r12w, r13w | 66 45 09 ec |
    | or ax, bp     | 66 09 e8    | *** | or r13w, r14w | 66 45 09 f5 |
    | or ax, si     | 66 09 f0    | *** | or r14w, r15w | 66 45 09 fe |
    | or ax, di     | 66 09 f8    | *** | or r15w, ax   | 66 41 09 c7 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_or_reg16_reg16():
    encode(OR_REG16_REG16)


OR_REG16_ADDR16 = """
    | -------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                    | encoding                               |
    | -------------------------------------------------------------- | -------------------------------------- |
    | or ax, word [rcx]                                              | 66 0b 01                               |
    | or cx, word [rcx]                                              | 66 0b 09                               |
    | or dx, word [rcx]                                              | 66 0b 11                               |
    | or bx, word [rcx]                                              | 66 0b 19                               |
    | or sp, word [rcx]                                              | 66 0b 21                               |
    | or bp, word [rcx]                                              | 66 0b 29                               |
    | or si, word [rcx]                                              | 66 0b 31                               |
    | or di, word [rcx]                                              | 66 0b 39                               |
    | or r8w, word [rcx]                                             | 66 44 0b 01                            |
    | or r9w, word [rcx]                                             | 66 44 0b 09                            |
    | or r10w, word [rcx]                                            | 66 44 0b 11                            |
    | or r11w, word [rcx]                                            | 66 44 0b 19                            |
    | or r12w, word [rcx]                                            | 66 44 0b 21                            |
    | or r13w, word [rcx]                                            | 66 44 0b 29                            |
    | or r14w, word [rcx]                                            | 66 44 0b 31                            |
    | or r15w, word [rcx]                                            | 66 44 0b 39                            |
    | or ax, word [rax]                                              | 66 0b 00                               |
    | or ax, word [rdx]                                              | 66 0b 02                               |
    | or ax, word [rbx]                                              | 66 0b 03                               |
    | or ax, word [rsp]                                              | 66 0b 04 24                            |
    | or ax, word [rbp]                                              | 66 0b 45 00                            |
    | or ax, word [rsi]                                              | 66 0b 06                               |
    | or ax, word [rdi]                                              | 66 0b 07                               |
    | or ax, word [r8]                                               | 66 41 0b 00                            |
    | or ax, word [r9]                                               | 66 41 0b 01                            |
    | or ax, word [r10]                                              | 66 41 0b 02                            |
    | or ax, word [r11]                                              | 66 41 0b 03                            |
    | or ax, word [r12]                                              | 66 41 0b 04 24                         |
    | or ax, word [r13]                                              | 66 41 0b 45 00                         |
    | or ax, word [r14]                                              | 66 41 0b 06                            |
    | or ax, word [r15]                                              | 66 41 0b 07                            |
    | or ax, word [rax + 1 * rcx]                                    | 66 0b 04 08                            |
    | or ax, word [rcx + 1 * rcx]                                    | 66 0b 04 09                            |
    | or ax, word [rdx + 1 * rcx]                                    | 66 0b 04 0a                            |
    | or ax, word [rbx + 1 * rcx]                                    | 66 0b 04 0b                            |
    | or ax, word [rsp + 1 * rcx]                                    | 66 0b 04 0c                            |
    | or ax, word [rbp + 1 * rcx]                                    | 66 0b 44 0d 00                         |
    | or ax, word [rsi + 1 * rcx]                                    | 66 0b 04 0e                            |
    | or ax, word [rdi + 1 * rcx]                                    | 66 0b 04 0f                            |
    | or ax, word [r8 + 1 * rcx]                                     | 66 41 0b 04 08                         |
    | or ax, word [r9 + 1 * rcx]                                     | 66 41 0b 04 09                         |
    | or ax, word [r10 + 1 * rcx]                                    | 66 41 0b 04 0a                         |
    | or ax, word [r11 + 1 * rcx]                                    | 66 41 0b 04 0b                         |
    | or ax, word [r12 + 1 * rcx]                                    | 66 41 0b 04 0c                         |
    | or ax, word [r13 + 1 * rcx]                                    | 66 41 0b 44 0d 00                      |
    | or ax, word [r14 + 1 * rcx]                                    | 66 41 0b 04 0e                         |
    | or ax, word [r15 + 1 * rcx]                                    | 66 41 0b 04 0f                         |
    | or ax, word [rax + 1 * rax]                                    | 66 0b 04 00                            |
    | or ax, word [rax + 1 * rdx]                                    | 66 0b 04 10                            |
    | or ax, word [rax + 1 * rbx]                                    | 66 0b 04 18                            |
    | or ax, word [rax + 1 * rbp]                                    | 66 0b 04 28                            |
    | or ax, word [rax + 1 * rsi]                                    | 66 0b 04 30                            |
    | or ax, word [rax + 1 * rdi]                                    | 66 0b 04 38                            |
    | or ax, word [rax + 1 * r8]                                     | 66 42 0b 04 00                         |
    | or ax, word [rax + 1 * r9]                                     | 66 42 0b 04 08                         |
    | or ax, word [rax + 1 * r10]                                    | 66 42 0b 04 10                         |
    | or ax, word [rax + 1 * r11]                                    | 66 42 0b 04 18                         |
    | or ax, word [rax + 1 * r12]                                    | 66 42 0b 04 20                         |
    | or ax, word [rax + 1 * r13]                                    | 66 42 0b 04 28                         |
    | or ax, word [rax + 1 * r14]                                    | 66 42 0b 04 30                         |
    | or ax, word [rax + 1 * r15]                                    | 66 42 0b 04 38                         |
    | or ax, word [rax + 2 * rcx]                                    | 66 0b 04 48                            |
    | or ax, word [rax + 4 * rcx]                                    | 66 0b 04 88                            |
    | or ax, word [rax + 8 * rcx]                                    | 66 0b 04 c8                            |
    | or ax, word [r8 + 1 * r9]                                      | 66 43 0b 04 08                         |
    | or ax, word [r8 + 2 * r9]                                      | 66 43 0b 04 48                         |
    | or ax, word [r8 + 4 * r9]                                      | 66 43 0b 04 88                         |
    | or ax, word [r8 + 8 * r9]                                      | 66 43 0b 04 c8                         |
    | or ax, word [1 * rcx]                                          | 66 0b 04 0d 00 00 00 00                |
    | or ax, word [2 * rcx]                                          | 66 0b 04 4d 00 00 00 00                |
    | or ax, word [4 * rcx]                                          | 66 0b 04 8d 00 00 00 00                |
    | or ax, word [8 * rcx]                                          | 66 0b 04 cd 00 00 00 00                |
    | or ax, word [1 * r9]                                           | 66 42 0b 04 0d 00 00 00 00             |
    | or ax, word [2 * r9]                                           | 66 42 0b 04 4d 00 00 00 00             |
    | or ax, word [4 * r9]                                           | 66 42 0b 04 8d 00 00 00 00             |
    | or ax, word [8 * r9]                                           | 66 42 0b 04 cd 00 00 00 00             |
    | or ax, word [r13 + 8 * r12]                                    | 66 43 0b 44 e5 00                      |
    | or ax, word [rsp + 4 * r15]                                    | 66 42 0b 04 bc                         |
    | or ax, word [rax + 1 * rcx + 0x00]                             | 66 0b 44 08 00                         |
    | or ax, word [rax + 1 * rcx - 0x00]                             | 66 0b 44 08 00                         |
    | or ax, word [rax + 1 * rcx + 0x01]                             | 66 0b 44 08 01                         |
    | or ax, word [rax + 1 * rcx - 0x01]                             | 66 0b 44 08 ff                         |
    | or ax, word [rax + 1 * rcx + 0x00000001]                       | 66 0b 84 08 01 00 00 00                |
    | or ax, word [rax + 1 * rcx - 0x00000001]                       | 66 0b 84 08 ff ff ff ff                |
    | or ax, word [rax + 1 * rcx + 0x7f]                             | 66 0b 44 08 7f                         |
    | or ax, word [rax + 1 * rcx - 0x7f]                             | 66 0b 44 08 81                         |
    | or ax, word [rax + 1 * rcx + 0x80]                             | 66 0b 84 08 80 00 00 00                |
    | or ax, word [rax + 1 * rcx - 0x80]                             | 66 0b 44 08 80                         |
    | or ax, word [rax + 1 * rcx - 0x81]                             | 66 0b 84 08 7f ff ff ff                |
    | or ax, word [rax + 1 * rcx + 0xff]                             | 66 0b 84 08 ff 00 00 00                |
    | or ax, word [rax + 1 * rcx - 0xff]                             | 66 0b 84 08 01 ff ff ff                |
    | or ax, word [rax + 1 * rcx + 0x7fffffff]                       | 66 0b 84 08 ff ff ff 7f                |
    | or ax, word [rax + 1 * rcx - 0x7fffffff]                       | 66 0b 84 08 01 00 00 80                |
    | or ax, word [rax + 1 * rcx - 0x80000000]                       | 66 0b 84 08 00 00 00 80                |
    | or ax, word [r10 + 0x7f]                                       | 66 41 0b 42 7f                         |
    | or ax, word [r10 + 0x80]                                       | 66 41 0b 82 80 00 00 00                |
    | or ax, word [r10 - 0x80]                                       | 66 41 0b 42 80                         |
    | or ax, word [r10 - 0x81]                                       | 66 41 0b 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or ax, word [rel @prev5]      | 90 90 90 90 90 66 0b 05 f4 ff ff ff    |
    | .prev1: nop; or ax, word [rel @prev1]                          | 90 66 0b 05 f8 ff ff ff                |
    | or ax, word [rel @next1]; nop; .next1: nop                     | 66 0b 05 01 00 00 00 90 90             |
    | or ax, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 0b 05 05 00 00 00 90 90 90 90 90 90 |
    | or cx, word [rdx]                                              | 66 0b 0a                               |
    | or dx, word [rbx]                                              | 66 0b 13                               |
    | or bx, word [rsp]                                              | 66 0b 1c 24                            |
    | or sp, word [rbp]                                              | 66 0b 65 00                            |
    | or bp, word [rsi]                                              | 66 0b 2e                               |
    | or si, word [rdi]                                              | 66 0b 37                               |
    | or di, word [r8]                                               | 66 41 0b 38                            |
    | or r8w, word [r9]                                              | 66 45 0b 01                            |
    | or r9w, word [r10]                                             | 66 45 0b 0a                            |
    | or r10w, word [r11]                                            | 66 45 0b 13                            |
    | or r11w, word [r12]                                            | 66 45 0b 1c 24                         |
    | or r12w, word [r13]                                            | 66 45 0b 65 00                         |
    | or r13w, word [r14]                                            | 66 45 0b 2e                            |
    | or r14w, word [r15]                                            | 66 45 0b 37                            |
    | or r15w, word [rax + 1 * rcx]                                  | 66 44 0b 3c 08                         |
    | or cx, word [rdx + 1 * rcx]                                    | 66 0b 0c 0a                            |
    | or dx, word [rbx + 1 * rcx]                                    | 66 0b 14 0b                            |
    | or bx, word [rsp + 1 * rcx]                                    | 66 0b 1c 0c                            |
    | or sp, word [rbp + 1 * rcx]                                    | 66 0b 64 0d 00                         |
    | or bp, word [rsi + 1 * rcx]                                    | 66 0b 2c 0e                            |
    | or si, word [rdi + 1 * rcx]                                    | 66 0b 34 0f                            |
    | or di, word [r8 + 1 * rcx]                                     | 66 41 0b 3c 08                         |
    | or r8w, word [r9 + 1 * rcx]                                    | 66 45 0b 04 09                         |
    | or r9w, word [r10 + 1 * rcx]                                   | 66 45 0b 0c 0a                         |
    | or r10w, word [r11 + 1 * rcx]                                  | 66 45 0b 14 0b                         |
    | or r11w, word [r12 + 1 * rcx]                                  | 66 45 0b 1c 0c                         |
    | or r12w, word [r13 + 1 * rcx]                                  | 66 45 0b 64 0d 00                      |
    | or r13w, word [r14 + 1 * rcx]                                  | 66 45 0b 2c 0e                         |
    | or r14w, word [r15 + 1 * rcx]                                  | 66 45 0b 34 0f                         |
    | or r15w, word [rax + 1 * rax]                                  | 66 44 0b 3c 00                         |
    | or cx, word [rax + 1 * rbx]                                    | 66 0b 0c 18                            |
    | or dx, word [rax + 1 * rbp]                                    | 66 0b 14 28                            |
    | or bx, word [rax + 1 * rsi]                                    | 66 0b 1c 30                            |
    | or sp, word [rax + 1 * rdi]                                    | 66 0b 24 38                            |
    | or bp, word [rax + 1 * r8]                                     | 66 42 0b 2c 00                         |
    | or si, word [rax + 1 * r9]                                     | 66 42 0b 34 08                         |
    | or di, word [rax + 1 * r10]                                    | 66 42 0b 3c 10                         |
    | or r8w, word [rax + 1 * r11]                                   | 66 46 0b 04 18                         |
    | or r9w, word [rax + 1 * r12]                                   | 66 46 0b 0c 20                         |
    | or r10w, word [rax + 1 * r13]                                  | 66 46 0b 14 28                         |
    | or r11w, word [rax + 1 * r14]                                  | 66 46 0b 1c 30                         |
    | or r12w, word [rax + 1 * r15]                                  | 66 46 0b 24 38                         |
    | or r13w, word [rax + 2 * rcx]                                  | 66 44 0b 2c 48                         |
    | or r14w, word [rax + 4 * rcx]                                  | 66 44 0b 34 88                         |
    | or r15w, word [rax + 8 * rcx]                                  | 66 44 0b 3c c8                         |
    | or cx, word [r8 + 2 * r9]                                      | 66 43 0b 0c 48                         |
    | or dx, word [r8 + 4 * r9]                                      | 66 43 0b 14 88                         |
    | or bx, word [r8 + 8 * r9]                                      | 66 43 0b 1c c8                         |
    | or sp, word [1 * rcx]                                          | 66 0b 24 0d 00 00 00 00                |
    | or bp, word [2 * rcx]                                          | 66 0b 2c 4d 00 00 00 00                |
    | or si, word [4 * rcx]                                          | 66 0b 34 8d 00 00 00 00                |
    | or di, word [8 * rcx]                                          | 66 0b 3c cd 00 00 00 00                |
    | or r8w, word [1 * r9]                                          | 66 46 0b 04 0d 00 00 00 00             |
    | or r9w, word [2 * r9]                                          | 66 46 0b 0c 4d 00 00 00 00             |
    | or r10w, word [4 * r9]                                         | 66 46 0b 14 8d 00 00 00 00             |
    | or r11w, word [8 * r9]                                         | 66 46 0b 1c cd 00 00 00 00             |
    | or r12w, word [r13 + 8 * r12]                                  | 66 47 0b 64 e5 00                      |
    | or r13w, word [rsp + 4 * r15]                                  | 66 46 0b 2c bc                         |
    | or r14w, word [rax + 1 * rcx + 0x00]                           | 66 44 0b 74 08 00                      |
    | or r15w, word [rax + 1 * rcx - 0x00]                           | 66 44 0b 7c 08 00                      |
    | or cx, word [rax + 1 * rcx - 0x01]                             | 66 0b 4c 08 ff                         |
    | or dx, word [rax + 1 * rcx + 0x00000001]                       | 66 0b 94 08 01 00 00 00                |
    | or bx, word [rax + 1 * rcx - 0x00000001]                       | 66 0b 9c 08 ff ff ff ff                |
    | or sp, word [rax + 1 * rcx + 0x7f]                             | 66 0b 64 08 7f                         |
    | or bp, word [rax + 1 * rcx - 0x7f]                             | 66 0b 6c 08 81                         |
    | or si, word [rax + 1 * rcx + 0x80]                             | 66 0b b4 08 80 00 00 00                |
    | or di, word [rax + 1 * rcx - 0x80]                             | 66 0b 7c 08 80                         |
    | or r8w, word [rax + 1 * rcx - 0x81]                            | 66 44 0b 84 08 7f ff ff ff             |
    | or r9w, word [rax + 1 * rcx + 0xff]                            | 66 44 0b 8c 08 ff 00 00 00             |
    | or r10w, word [rax + 1 * rcx - 0xff]                           | 66 44 0b 94 08 01 ff ff ff             |
    | or r11w, word [rax + 1 * rcx + 0x7fffffff]                     | 66 44 0b 9c 08 ff ff ff 7f             |
    | or r12w, word [rax + 1 * rcx - 0x7fffffff]                     | 66 44 0b a4 08 01 00 00 80             |
    | or r13w, word [rax + 1 * rcx - 0x80000000]                     | 66 44 0b ac 08 00 00 00 80             |
    | or r14w, word [r10 + 0x7f]                                     | 66 45 0b 72 7f                         |
    | or r15w, word [r10 + 0x80]                                     | 66 45 0b ba 80 00 00 00                |
    | or cx, word [r10 - 0x81]                                       | 66 41 0b 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or dx, word [rel @prev5]      | 90 90 90 90 90 66 0b 15 f4 ff ff ff    |
    | .prev1: nop; or bx, word [rel @prev1]                          | 90 66 0b 1d f8 ff ff ff                |
    | or sp, word [rel @next1]; nop; .next1: nop                     | 66 0b 25 01 00 00 00 90 90             |
    | or bp, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 0b 2d 05 00 00 00 90 90 90 90 90 90 |
    | or si, word [rax]                                              | 66 0b 30                               |
    | -------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_reg16_addr16():
    encode(OR_REG16_ADDR16)


OR_REG8_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | or al, 0x01   | 0c 01       | *** | or al, 0x00   | 0c 00       |
    | or cl, 0x01   | 80 c9 01    | *** | or al, 0x7f   | 0c 7f       |
    | or dl, 0x01   | 80 ca 01    | *** | or al, 0x80   | 0c 80       |
    | or bl, 0x01   | 80 cb 01    | *** | or al, 0xff   | 0c ff       |
    | or spl, 0x01  | 40 80 cc 01 | *** | or cl, 0x7f   | 80 c9 7f    |
    | or bpl, 0x01  | 40 80 cd 01 | *** | or dl, 0x80   | 80 ca 80    |
    | or sil, 0x01  | 40 80 ce 01 | *** | or bl, 0xff   | 80 cb ff    |
    | or dil, 0x01  | 40 80 cf 01 | *** | or spl, 0x00  | 40 80 cc 00 |
    | or r8b, 0x01  | 41 80 c8 01 | *** | or sil, 0x7f  | 40 80 ce 7f |
    | or r9b, 0x01  | 41 80 c9 01 | *** | or dil, 0x80  | 40 80 cf 80 |
    | or r10b, 0x01 | 41 80 ca 01 | *** | or r8b, 0xff  | 41 80 c8 ff |
    | or r11b, 0x01 | 41 80 cb 01 | *** | or r9b, 0x00  | 41 80 c9 00 |
    | or r12b, 0x01 | 41 80 cc 01 | *** | or r11b, 0x7f | 41 80 cb 7f |
    | or r13b, 0x01 | 41 80 cd 01 | *** | or r12b, 0x80 | 41 80 cc 80 |
    | or r14b, 0x01 | 41 80 ce 01 | *** | or r13b, 0xff | 41 80 cd ff |
    | or r15b, 0x01 | 41 80 cf 01 | *** | or r14b, 0x00 | 41 80 ce 00 |
    | or ah, 0x01   | 80 cc 01    | *** | or ah, 0x7f   | 80 cc 7f    |
    | or ch, 0x01   | 80 cd 01    | *** | or ch, 0x80   | 80 cd 80    |
    | or dh, 0x01   | 80 ce 01    | *** | or dh, 0xff   | 80 ce ff    |
    | or bh, 0x01   | 80 cf 01    | *** | or bh, 0x00   | 80 cf 00    |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_or_reg8_imm8():
    encode(OR_REG8_IMM8)


OR_REG8_REG8 = """
    | ------------- | -------- | --- | ------------- | -------- |
    | instruction   | encoding | *** | instruction   | encoding |
    | ------------- | -------- | --- | ------------- | -------- |
    | or al, cl     | 08 c8    | *** | or al, r10b   | 44 08 d0 |
    | or cl, cl     | 08 c9    | *** | or al, r11b   | 44 08 d8 |
    | or dl, cl     | 08 ca    | *** | or al, r12b   | 44 08 e0 |
    | or bl, cl     | 08 cb    | *** | or al, r13b   | 44 08 e8 |
    | or spl, cl    | 40 08 cc | *** | or al, r14b   | 44 08 f0 |
    | or bpl, cl    | 40 08 cd | *** | or al, r15b   | 44 08 f8 |
    | or sil, cl    | 40 08 ce | *** | or al, ah     | 08 e0    |
    | or dil, cl    | 40 08 cf | *** | or al, ch     | 08 e8    |
    | or r8b, cl    | 41 08 c8 | *** | or al, dh     | 08 f0    |
    | or r9b, cl    | 41 08 c9 | *** | or al, bh     | 08 f8    |
    | or r10b, cl   | 41 08 ca | *** | or cl, dl     | 08 d1    |
    | or r11b, cl   | 41 08 cb | *** | or dl, bl     | 08 da    |
    | or r12b, cl   | 41 08 cc | *** | or bl, spl    | 40 08 e3 |
    | or r13b, cl   | 41 08 cd | *** | or spl, bpl   | 40 08 ec |
    | or r14b, cl   | 41 08 ce | *** | or bpl, sil   | 40 08 f5 |
    | or r15b, cl   | 41 08 cf | *** | or sil, dil   | 40 08 fe |
    | or ah, cl     | 08 cc    | *** | or dil, r8b   | 44 08 c7 |
    | or ch, cl     | 08 cd    | *** | or r8b, r9b   | 45 08 c8 |
    | or dh, cl     | 08 ce    | *** | or r9b, r10b  | 45 08 d1 |
    | or bh, cl     | 08 cf    | *** | or r10b, r11b | 45 08 da |
    | or al, al     | 08 c0    | *** | or r11b, r12b | 45 08 e3 |
    | or al, dl     | 08 d0    | *** | or r12b, r13b | 45 08 ec |
    | or al, bl     | 08 d8    | *** | or r13b, r14b | 45 08 f5 |
    | or al, spl    | 40 08 e0 | *** | or r14b, r15b | 45 08 fe |
    | or al, bpl    | 40 08 e8 | *** | or r15b, ah   | !! !! !! |
    | or al, sil    | 40 08 f0 | *** | or ah, ch     | 08 ec    |
    | or al, dil    | 40 08 f8 | *** | or ch, dh     | 08 f5    |
    | or al, r8b    | 44 08 c0 | *** | or dh, bh     | 08 fe    |
    | or al, r9b    | 44 08 c8 | *** | or bh, al     | 08 c7    |
    | ------------- | -------- | --- | ------------- | -------- |
"""


def can_encode_or_reg8_reg8():
    encode(OR_REG8_REG8)


OR_REG8_ADDR8 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | or al, byte [rcx]                                               | 0a 01                                  |
    | or cl, byte [rcx]                                               | 0a 09                                  |
    | or dl, byte [rcx]                                               | 0a 11                                  |
    | or bl, byte [rcx]                                               | 0a 19                                  |
    | or spl, byte [rcx]                                              | 40 0a 21                               |
    | or bpl, byte [rcx]                                              | 40 0a 29                               |
    | or sil, byte [rcx]                                              | 40 0a 31                               |
    | or dil, byte [rcx]                                              | 40 0a 39                               |
    | or r8b, byte [rcx]                                              | 44 0a 01                               |
    | or r9b, byte [rcx]                                              | 44 0a 09                               |
    | or r10b, byte [rcx]                                             | 44 0a 11                               |
    | or r11b, byte [rcx]                                             | 44 0a 19                               |
    | or r12b, byte [rcx]                                             | 44 0a 21                               |
    | or r13b, byte [rcx]                                             | 44 0a 29                               |
    | or r14b, byte [rcx]                                             | 44 0a 31                               |
    | or r15b, byte [rcx]                                             | 44 0a 39                               |
    | or ah, byte [rcx]                                               | 0a 21                                  |
    | or ch, byte [rcx]                                               | 0a 29                                  |
    | or dh, byte [rcx]                                               | 0a 31                                  |
    | or bh, byte [rcx]                                               | 0a 39                                  |
    | or al, byte [rax]                                               | 0a 00                                  |
    | or al, byte [rdx]                                               | 0a 02                                  |
    | or al, byte [rbx]                                               | 0a 03                                  |
    | or al, byte [rsp]                                               | 0a 04 24                               |
    | or al, byte [rbp]                                               | 0a 45 00                               |
    | or al, byte [rsi]                                               | 0a 06                                  |
    | or al, byte [rdi]                                               | 0a 07                                  |
    | or al, byte [r8]                                                | 41 0a 00                               |
    | or al, byte [r9]                                                | 41 0a 01                               |
    | or al, byte [r10]                                               | 41 0a 02                               |
    | or al, byte [r11]                                               | 41 0a 03                               |
    | or al, byte [r12]                                               | 41 0a 04 24                            |
    | or al, byte [r13]                                               | 41 0a 45 00                            |
    | or al, byte [r14]                                               | 41 0a 06                               |
    | or al, byte [r15]                                               | 41 0a 07                               |
    | or al, byte [rax + 1 * rcx]                                     | 0a 04 08                               |
    | or al, byte [rcx + 1 * rcx]                                     | 0a 04 09                               |
    | or al, byte [rdx + 1 * rcx]                                     | 0a 04 0a                               |
    | or al, byte [rbx + 1 * rcx]                                     | 0a 04 0b                               |
    | or al, byte [rsp + 1 * rcx]                                     | 0a 04 0c                               |
    | or al, byte [rbp + 1 * rcx]                                     | 0a 44 0d 00                            |
    | or al, byte [rsi + 1 * rcx]                                     | 0a 04 0e                               |
    | or al, byte [rdi + 1 * rcx]                                     | 0a 04 0f                               |
    | or al, byte [r8 + 1 * rcx]                                      | 41 0a 04 08                            |
    | or al, byte [r9 + 1 * rcx]                                      | 41 0a 04 09                            |
    | or al, byte [r10 + 1 * rcx]                                     | 41 0a 04 0a                            |
    | or al, byte [r11 + 1 * rcx]                                     | 41 0a 04 0b                            |
    | or al, byte [r12 + 1 * rcx]                                     | 41 0a 04 0c                            |
    | or al, byte [r13 + 1 * rcx]                                     | 41 0a 44 0d 00                         |
    | or al, byte [r14 + 1 * rcx]                                     | 41 0a 04 0e                            |
    | or al, byte [r15 + 1 * rcx]                                     | 41 0a 04 0f                            |
    | or al, byte [rax + 1 * rax]                                     | 0a 04 00                               |
    | or al, byte [rax + 1 * rdx]                                     | 0a 04 10                               |
    | or al, byte [rax + 1 * rbx]                                     | 0a 04 18                               |
    | or al, byte [rax + 1 * rbp]                                     | 0a 04 28                               |
    | or al, byte [rax + 1 * rsi]                                     | 0a 04 30                               |
    | or al, byte [rax + 1 * rdi]                                     | 0a 04 38                               |
    | or al, byte [rax + 1 * r8]                                      | 42 0a 04 00                            |
    | or al, byte [rax + 1 * r9]                                      | 42 0a 04 08                            |
    | or al, byte [rax + 1 * r10]                                     | 42 0a 04 10                            |
    | or al, byte [rax + 1 * r11]                                     | 42 0a 04 18                            |
    | or al, byte [rax + 1 * r12]                                     | 42 0a 04 20                            |
    | or al, byte [rax + 1 * r13]                                     | 42 0a 04 28                            |
    | or al, byte [rax + 1 * r14]                                     | 42 0a 04 30                            |
    | or al, byte [rax + 1 * r15]                                     | 42 0a 04 38                            |
    | or al, byte [rax + 2 * rcx]                                     | 0a 04 48                               |
    | or al, byte [rax + 4 * rcx]                                     | 0a 04 88                               |
    | or al, byte [rax + 8 * rcx]                                     | 0a 04 c8                               |
    | or al, byte [r8 + 1 * r9]                                       | 43 0a 04 08                            |
    | or al, byte [r8 + 2 * r9]                                       | 43 0a 04 48                            |
    | or al, byte [r8 + 4 * r9]                                       | 43 0a 04 88                            |
    | or al, byte [r8 + 8 * r9]                                       | 43 0a 04 c8                            |
    | or al, byte [1 * rcx]                                           | 0a 04 0d 00 00 00 00                   |
    | or al, byte [2 * rcx]                                           | 0a 04 4d 00 00 00 00                   |
    | or al, byte [4 * rcx]                                           | 0a 04 8d 00 00 00 00                   |
    | or al, byte [8 * rcx]                                           | 0a 04 cd 00 00 00 00                   |
    | or al, byte [1 * r9]                                            | 42 0a 04 0d 00 00 00 00                |
    | or al, byte [2 * r9]                                            | 42 0a 04 4d 00 00 00 00                |
    | or al, byte [4 * r9]                                            | 42 0a 04 8d 00 00 00 00                |
    | or al, byte [8 * r9]                                            | 42 0a 04 cd 00 00 00 00                |
    | or al, byte [r13 + 8 * r12]                                     | 43 0a 44 e5 00                         |
    | or al, byte [rsp + 4 * r15]                                     | 42 0a 04 bc                            |
    | or al, byte [rax + 1 * rcx + 0x00]                              | 0a 44 08 00                            |
    | or al, byte [rax + 1 * rcx - 0x00]                              | 0a 44 08 00                            |
    | or al, byte [rax + 1 * rcx + 0x01]                              | 0a 44 08 01                            |
    | or al, byte [rax + 1 * rcx - 0x01]                              | 0a 44 08 ff                            |
    | or al, byte [rax + 1 * rcx + 0x00000001]                        | 0a 84 08 01 00 00 00                   |
    | or al, byte [rax + 1 * rcx - 0x00000001]                        | 0a 84 08 ff ff ff ff                   |
    | or al, byte [rax + 1 * rcx + 0x7f]                              | 0a 44 08 7f                            |
    | or al, byte [rax + 1 * rcx - 0x7f]                              | 0a 44 08 81                            |
    | or al, byte [rax + 1 * rcx + 0x80]                              | 0a 84 08 80 00 00 00                   |
    | or al, byte [rax + 1 * rcx - 0x80]                              | 0a 44 08 80                            |
    | or al, byte [rax + 1 * rcx - 0x81]                              | 0a 84 08 7f ff ff ff                   |
    | or al, byte [rax + 1 * rcx + 0xff]                              | 0a 84 08 ff 00 00 00                   |
    | or al, byte [rax + 1 * rcx - 0xff]                              | 0a 84 08 01 ff ff ff                   |
    | or al, byte [rax + 1 * rcx + 0x7fffffff]                        | 0a 84 08 ff ff ff 7f                   |
    | or al, byte [rax + 1 * rcx - 0x7fffffff]                        | 0a 84 08 01 00 00 80                   |
    | or al, byte [rax + 1 * rcx - 0x80000000]                        | 0a 84 08 00 00 00 80                   |
    | or al, byte [r10 + 0x7f]                                        | 41 0a 42 7f                            |
    | or al, byte [r10 + 0x80]                                        | 41 0a 82 80 00 00 00                   |
    | or al, byte [r10 - 0x80]                                        | 41 0a 42 80                            |
    | or al, byte [r10 - 0x81]                                        | 41 0a 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or al, byte [rel @prev5]       | 90 90 90 90 90 0a 05 f5 ff ff ff       |
    | .prev1: nop; or al, byte [rel @prev1]                           | 90 0a 05 f9 ff ff ff                   |
    | or al, byte [rel @next1]; nop; .next1: nop                      | 0a 05 01 00 00 00 90 90                |
    | or al, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop  | 0a 05 05 00 00 00 90 90 90 90 90 90    |
    | or cl, byte [rdx]                                               | 0a 0a                                  |
    | or dl, byte [rbx]                                               | 0a 13                                  |
    | or bl, byte [rsp]                                               | 0a 1c 24                               |
    | or spl, byte [rbp]                                              | 40 0a 65 00                            |
    | or bpl, byte [rsi]                                              | 40 0a 2e                               |
    | or sil, byte [rdi]                                              | 40 0a 37                               |
    | or dil, byte [r8]                                               | 41 0a 38                               |
    | or r8b, byte [r9]                                               | 45 0a 01                               |
    | or r9b, byte [r10]                                              | 45 0a 0a                               |
    | or r10b, byte [r11]                                             | 45 0a 13                               |
    | or r11b, byte [r12]                                             | 45 0a 1c 24                            |
    | or r12b, byte [r13]                                             | 45 0a 65 00                            |
    | or r13b, byte [r14]                                             | 45 0a 2e                               |
    | or r14b, byte [r15]                                             | 45 0a 37                               |
    | or r15b, byte [rax + 1 * rcx]                                   | 44 0a 3c 08                            |
    | or ah, byte [rcx + 1 * rcx]                                     | 0a 24 09                               |
    | or ch, byte [rdx + 1 * rcx]                                     | 0a 2c 0a                               |
    | or dh, byte [rbx + 1 * rcx]                                     | 0a 34 0b                               |
    | or bh, byte [rsp + 1 * rcx]                                     | 0a 3c 0c                               |
    | or cl, byte [rsi + 1 * rcx]                                     | 0a 0c 0e                               |
    | or dl, byte [rdi + 1 * rcx]                                     | 0a 14 0f                               |
    | or bl, byte [r8 + 1 * rcx]                                      | 41 0a 1c 08                            |
    | or spl, byte [r9 + 1 * rcx]                                     | 41 0a 24 09                            |
    | or bpl, byte [r10 + 1 * rcx]                                    | 41 0a 2c 0a                            |
    | or sil, byte [r11 + 1 * rcx]                                    | 41 0a 34 0b                            |
    | or dil, byte [r12 + 1 * rcx]                                    | 41 0a 3c 0c                            |
    | or r8b, byte [r13 + 1 * rcx]                                    | 45 0a 44 0d 00                         |
    | or r9b, byte [r14 + 1 * rcx]                                    | 45 0a 0c 0e                            |
    | or r10b, byte [r15 + 1 * rcx]                                   | 45 0a 14 0f                            |
    | or r11b, byte [rax + 1 * rax]                                   | 44 0a 1c 00                            |
    | or r12b, byte [rax + 1 * rdx]                                   | 44 0a 24 10                            |
    | or r13b, byte [rax + 1 * rbx]                                   | 44 0a 2c 18                            |
    | or r14b, byte [rax + 1 * rbp]                                   | 44 0a 34 28                            |
    | or r15b, byte [rax + 1 * rsi]                                   | 44 0a 3c 30                            |
    | or ah, byte [rax + 1 * rdi]                                     | 0a 24 38                               |
    | or ch, byte [rax + 1 * r8]                                      | !! !! !!                               |
    | or dh, byte [rax + 1 * r9]                                      | !! !! !!                               |
    | or bh, byte [rax + 1 * r10]                                     | !! !! !!                               |
    | or cl, byte [rax + 1 * r12]                                     | 42 0a 0c 20                            |
    | or dl, byte [rax + 1 * r13]                                     | 42 0a 14 28                            |
    | or bl, byte [rax + 1 * r14]                                     | 42 0a 1c 30                            |
    | or spl, byte [rax + 1 * r15]                                    | 42 0a 24 38                            |
    | or bpl, byte [rax + 2 * rcx]                                    | 40 0a 2c 48                            |
    | or sil, byte [rax + 4 * rcx]                                    | 40 0a 34 88                            |
    | or dil, byte [rax + 8 * rcx]                                    | 40 0a 3c c8                            |
    | or r8b, byte [r8 + 1 * r9]                                      | 47 0a 04 08                            |
    | or r9b, byte [r8 + 2 * r9]                                      | 47 0a 0c 48                            |
    | or r10b, byte [r8 + 4 * r9]                                     | 47 0a 14 88                            |
    | or r11b, byte [r8 + 8 * r9]                                     | 47 0a 1c c8                            |
    | or r12b, byte [1 * rcx]                                         | 44 0a 24 0d 00 00 00 00                |
    | or r13b, byte [2 * rcx]                                         | 44 0a 2c 4d 00 00 00 00                |
    | or r14b, byte [4 * rcx]                                         | 44 0a 34 8d 00 00 00 00                |
    | or r15b, byte [8 * rcx]                                         | 44 0a 3c cd 00 00 00 00                |
    | or ah, byte [1 * r9]                                            | !! !! !!                               |
    | or ch, byte [2 * r9]                                            | !! !! !!                               |
    | or dh, byte [4 * r9]                                            | !! !! !!                               |
    | or bh, byte [8 * r9]                                            | !! !! !!                               |
    | or cl, byte [rsp + 4 * r15]                                     | 42 0a 0c bc                            |
    | or dl, byte [rax + 1 * rcx + 0x00]                              | 0a 54 08 00                            |
    | or bl, byte [rax + 1 * rcx - 0x00]                              | 0a 5c 08 00                            |
    | or spl, byte [rax + 1 * rcx + 0x01]                             | 40 0a 64 08 01                         |
    | or bpl, byte [rax + 1 * rcx - 0x01]                             | 40 0a 6c 08 ff                         |
    | or sil, byte [rax + 1 * rcx + 0x00000001]                       | 40 0a b4 08 01 00 00 00                |
    | or dil, byte [rax + 1 * rcx - 0x00000001]                       | 40 0a bc 08 ff ff ff ff                |
    | or r8b, byte [rax + 1 * rcx + 0x7f]                             | 44 0a 44 08 7f                         |
    | or r9b, byte [rax + 1 * rcx - 0x7f]                             | 44 0a 4c 08 81                         |
    | or r10b, byte [rax + 1 * rcx + 0x80]                            | 44 0a 94 08 80 00 00 00                |
    | or r11b, byte [rax + 1 * rcx - 0x80]                            | 44 0a 5c 08 80                         |
    | or r12b, byte [rax + 1 * rcx - 0x81]                            | 44 0a a4 08 7f ff ff ff                |
    | or r13b, byte [rax + 1 * rcx + 0xff]                            | 44 0a ac 08 ff 00 00 00                |
    | or r14b, byte [rax + 1 * rcx - 0xff]                            | 44 0a b4 08 01 ff ff ff                |
    | or r15b, byte [rax + 1 * rcx + 0x7fffffff]                      | 44 0a bc 08 ff ff ff 7f                |
    | or ah, byte [rax + 1 * rcx - 0x7fffffff]                        | 0a a4 08 01 00 00 80                   |
    | or ch, byte [rax + 1 * rcx - 0x80000000]                        | 0a ac 08 00 00 00 80                   |
    | or dh, byte [r10 + 0x7f]                                        | !! !! !!                               |
    | or bh, byte [r10 + 0x80]                                        | !! !! !!                               |
    | or cl, byte [r10 - 0x81]                                        | 41 0a 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or dl, byte [rel @prev5]       | 90 90 90 90 90 0a 15 f5 ff ff ff       |
    | .prev1: nop; or bl, byte [rel @prev1]                           | 90 0a 1d f9 ff ff ff                   |
    | or spl, byte [rel @next1]; nop; .next1: nop                     | 40 0a 25 01 00 00 00 90 90             |
    | or bpl, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 40 0a 2d 05 00 00 00 90 90 90 90 90 90 |
    | or sil, byte [rax]                                              | 40 0a 30                               |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_reg8_addr8():
    encode(OR_REG8_ADDR8)


OR_ADDR64_IMM8 = """
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | instruction                                                       | encoding                                  |
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | or qword [rax], 0x01                                              | 48 83 08 01                               |
    | or qword [rcx], 0x01                                              | 48 83 09 01                               |
    | or qword [rdx], 0x01                                              | 48 83 0a 01                               |
    | or qword [rbx], 0x01                                              | 48 83 0b 01                               |
    | or qword [rsp], 0x01                                              | 48 83 0c 24 01                            |
    | or qword [rbp], 0x01                                              | 48 83 4d 00 01                            |
    | or qword [rsi], 0x01                                              | 48 83 0e 01                               |
    | or qword [rdi], 0x01                                              | 48 83 0f 01                               |
    | or qword [r8], 0x01                                               | 49 83 08 01                               |
    | or qword [r9], 0x01                                               | 49 83 09 01                               |
    | or qword [r10], 0x01                                              | 49 83 0a 01                               |
    | or qword [r11], 0x01                                              | 49 83 0b 01                               |
    | or qword [r12], 0x01                                              | 49 83 0c 24 01                            |
    | or qword [r13], 0x01                                              | 49 83 4d 00 01                            |
    | or qword [r14], 0x01                                              | 49 83 0e 01                               |
    | or qword [r15], 0x01                                              | 49 83 0f 01                               |
    | or qword [rax + 1 * rcx], 0x01                                    | 48 83 0c 08 01                            |
    | or qword [rcx + 1 * rcx], 0x01                                    | 48 83 0c 09 01                            |
    | or qword [rdx + 1 * rcx], 0x01                                    | 48 83 0c 0a 01                            |
    | or qword [rbx + 1 * rcx], 0x01                                    | 48 83 0c 0b 01                            |
    | or qword [rsp + 1 * rcx], 0x01                                    | 48 83 0c 0c 01                            |
    | or qword [rbp + 1 * rcx], 0x01                                    | 48 83 4c 0d 00 01                         |
    | or qword [rsi + 1 * rcx], 0x01                                    | 48 83 0c 0e 01                            |
    | or qword [rdi + 1 * rcx], 0x01                                    | 48 83 0c 0f 01                            |
    | or qword [r8 + 1 * rcx], 0x01                                     | 49 83 0c 08 01                            |
    | or qword [r9 + 1 * rcx], 0x01                                     | 49 83 0c 09 01                            |
    | or qword [r10 + 1 * rcx], 0x01                                    | 49 83 0c 0a 01                            |
    | or qword [r11 + 1 * rcx], 0x01                                    | 49 83 0c 0b 01                            |
    | or qword [r12 + 1 * rcx], 0x01                                    | 49 83 0c 0c 01                            |
    | or qword [r13 + 1 * rcx], 0x01                                    | 49 83 4c 0d 00 01                         |
    | or qword [r14 + 1 * rcx], 0x01                                    | 49 83 0c 0e 01                            |
    | or qword [r15 + 1 * rcx], 0x01                                    | 49 83 0c 0f 01                            |
    | or qword [rax + 1 * rax], 0x01                                    | 48 83 0c 00 01                            |
    | or qword [rax + 1 * rdx], 0x01                                    | 48 83 0c 10 01                            |
    | or qword [rax + 1 * rbx], 0x01                                    | 48 83 0c 18 01                            |
    | or qword [rax + 1 * rbp], 0x01                                    | 48 83 0c 28 01                            |
    | or qword [rax + 1 * rsi], 0x01                                    | 48 83 0c 30 01                            |
    | or qword [rax + 1 * rdi], 0x01                                    | 48 83 0c 38 01                            |
    | or qword [rax + 1 * r8], 0x01                                     | 4a 83 0c 00 01                            |
    | or qword [rax + 1 * r9], 0x01                                     | 4a 83 0c 08 01                            |
    | or qword [rax + 1 * r10], 0x01                                    | 4a 83 0c 10 01                            |
    | or qword [rax + 1 * r11], 0x01                                    | 4a 83 0c 18 01                            |
    | or qword [rax + 1 * r12], 0x01                                    | 4a 83 0c 20 01                            |
    | or qword [rax + 1 * r13], 0x01                                    | 4a 83 0c 28 01                            |
    | or qword [rax + 1 * r14], 0x01                                    | 4a 83 0c 30 01                            |
    | or qword [rax + 1 * r15], 0x01                                    | 4a 83 0c 38 01                            |
    | or qword [rax + 2 * rcx], 0x01                                    | 48 83 0c 48 01                            |
    | or qword [rax + 4 * rcx], 0x01                                    | 48 83 0c 88 01                            |
    | or qword [rax + 8 * rcx], 0x01                                    | 48 83 0c c8 01                            |
    | or qword [r8 + 1 * r9], 0x01                                      | 4b 83 0c 08 01                            |
    | or qword [r8 + 2 * r9], 0x01                                      | 4b 83 0c 48 01                            |
    | or qword [r8 + 4 * r9], 0x01                                      | 4b 83 0c 88 01                            |
    | or qword [r8 + 8 * r9], 0x01                                      | 4b 83 0c c8 01                            |
    | or qword [1 * rcx], 0x01                                          | 48 83 0c 0d 00 00 00 00 01                |
    | or qword [2 * rcx], 0x01                                          | 48 83 0c 4d 00 00 00 00 01                |
    | or qword [4 * rcx], 0x01                                          | 48 83 0c 8d 00 00 00 00 01                |
    | or qword [8 * rcx], 0x01                                          | 48 83 0c cd 00 00 00 00 01                |
    | or qword [1 * r9], 0x01                                           | 4a 83 0c 0d 00 00 00 00 01                |
    | or qword [2 * r9], 0x01                                           | 4a 83 0c 4d 00 00 00 00 01                |
    | or qword [4 * r9], 0x01                                           | 4a 83 0c 8d 00 00 00 00 01                |
    | or qword [8 * r9], 0x01                                           | 4a 83 0c cd 00 00 00 00 01                |
    | or qword [r13 + 8 * r12], 0x01                                    | 4b 83 4c e5 00 01                         |
    | or qword [rsp + 4 * r15], 0x01                                    | 4a 83 0c bc 01                            |
    | or qword [rax + 1 * rcx + 0x00], 0x01                             | 48 83 4c 08 00 01                         |
    | or qword [rax + 1 * rcx - 0x00], 0x01                             | 48 83 4c 08 00 01                         |
    | or qword [rax + 1 * rcx + 0x01], 0x01                             | 48 83 4c 08 01 01                         |
    | or qword [rax + 1 * rcx - 0x01], 0x01                             | 48 83 4c 08 ff 01                         |
    | or qword [rax + 1 * rcx + 0x00000001], 0x01                       | 48 83 8c 08 01 00 00 00 01                |
    | or qword [rax + 1 * rcx - 0x00000001], 0x01                       | 48 83 8c 08 ff ff ff ff 01                |
    | or qword [rax + 1 * rcx + 0x7f], 0x01                             | 48 83 4c 08 7f 01                         |
    | or qword [rax + 1 * rcx - 0x7f], 0x01                             | 48 83 4c 08 81 01                         |
    | or qword [rax + 1 * rcx + 0x80], 0x01                             | 48 83 8c 08 80 00 00 00 01                |
    | or qword [rax + 1 * rcx - 0x80], 0x01                             | 48 83 4c 08 80 01                         |
    | or qword [rax + 1 * rcx - 0x81], 0x01                             | 48 83 8c 08 7f ff ff ff 01                |
    | or qword [rax + 1 * rcx + 0xff], 0x01                             | 48 83 8c 08 ff 00 00 00 01                |
    | or qword [rax + 1 * rcx - 0xff], 0x01                             | 48 83 8c 08 01 ff ff ff 01                |
    | or qword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 48 83 8c 08 ff ff ff 7f 01                |
    | or qword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 48 83 8c 08 01 00 00 80 01                |
    | or qword [rax + 1 * rcx - 0x80000000], 0x01                       | 48 83 8c 08 00 00 00 80 01                |
    | or qword [r10 + 0x7f], 0x01                                       | 49 83 4a 7f 01                            |
    | or qword [r10 + 0x80], 0x01                                       | 49 83 8a 80 00 00 00 01                   |
    | or qword [r10 - 0x80], 0x01                                       | 49 83 4a 80 01                            |
    | or qword [r10 - 0x81], 0x01                                       | 49 83 8a 7f ff ff ff 01                   |
    | .prev5: nop; nop; nop; nop; nop; or qword [rel @prev5], 0x01      | 90 90 90 90 90 48 83 0d f3 ff ff ff 01    |
    | .prev1: nop; or qword [rel @prev1], 0x01                          | 90 48 83 0d f7 ff ff ff 01                |
    | or qword [rel @next1], 0x01; nop; .next1: nop                     | 48 83 0d 01 00 00 00 01 90 90             |
    | or qword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 48 83 0d 05 00 00 00 01 90 90 90 90 90 90 |
    | or qword [rax], 0x00                                              | 48 83 08 00                               |
    | or qword [rax], 0x7f                                              | 48 83 08 7f                               |
    | or qword [rax], 0x80                                              | 48 83 08 80                               |
    | or qword [rax], 0xff                                              | 48 83 08 ff                               |
    | or qword [rcx], 0x7f                                              | 48 83 09 7f                               |
    | or qword [rdx], 0x80                                              | 48 83 0a 80                               |
    | or qword [rbx], 0xff                                              | 48 83 0b ff                               |
    | or qword [rsp], 0x00                                              | 48 83 0c 24 00                            |
    | or qword [rsi], 0x7f                                              | 48 83 0e 7f                               |
    | or qword [rdi], 0x80                                              | 48 83 0f 80                               |
    | or qword [r8], 0xff                                               | 49 83 08 ff                               |
    | or qword [r9], 0x00                                               | 49 83 09 00                               |
    | or qword [r11], 0x7f                                              | 49 83 0b 7f                               |
    | or qword [r12], 0x80                                              | 49 83 0c 24 80                            |
    | or qword [r13], 0xff                                              | 49 83 4d 00 ff                            |
    | or qword [r14], 0x00                                              | 49 83 0e 00                               |
    | or qword [rax + 1 * rcx], 0x7f                                    | 48 83 0c 08 7f                            |
    | or qword [rcx + 1 * rcx], 0x80                                    | 48 83 0c 09 80                            |
    | or qword [rdx + 1 * rcx], 0xff                                    | 48 83 0c 0a ff                            |
    | or qword [rbx + 1 * rcx], 0x00                                    | 48 83 0c 0b 00                            |
    | or qword [rbp + 1 * rcx], 0x7f                                    | 48 83 4c 0d 00 7f                         |
    | or qword [rsi + 1 * rcx], 0x80                                    | 48 83 0c 0e 80                            |
    | or qword [rdi + 1 * rcx], 0xff                                    | 48 83 0c 0f ff                            |
    | or qword [r8 + 1 * rcx], 0x00                                     | 49 83 0c 08 00                            |
    | or qword [r10 + 1 * rcx], 0x7f                                    | 49 83 0c 0a 7f                            |
    | or qword [r11 + 1 * rcx], 0x80                                    | 49 83 0c 0b 80                            |
    | or qword [r12 + 1 * rcx], 0xff                                    | 49 83 0c 0c ff                            |
    | or qword [r13 + 1 * rcx], 0x00                                    | 49 83 4c 0d 00 00                         |
    | or qword [r15 + 1 * rcx], 0x7f                                    | 49 83 0c 0f 7f                            |
    | or qword [rax + 1 * rax], 0x80                                    | 48 83 0c 00 80                            |
    | or qword [rax + 1 * rdx], 0xff                                    | 48 83 0c 10 ff                            |
    | or qword [rax + 1 * rbx], 0x00                                    | 48 83 0c 18 00                            |
    | or qword [rax + 1 * rsi], 0x7f                                    | 48 83 0c 30 7f                            |
    | or qword [rax + 1 * rdi], 0x80                                    | 48 83 0c 38 80                            |
    | or qword [rax + 1 * r8], 0xff                                     | 4a 83 0c 00 ff                            |
    | or qword [rax + 1 * r9], 0x00                                     | 4a 83 0c 08 00                            |
    | or qword [rax + 1 * r11], 0x7f                                    | 4a 83 0c 18 7f                            |
    | or qword [rax + 1 * r12], 0x80                                    | 4a 83 0c 20 80                            |
    | or qword [rax + 1 * r13], 0xff                                    | 4a 83 0c 28 ff                            |
    | or qword [rax + 1 * r14], 0x00                                    | 4a 83 0c 30 00                            |
    | or qword [rax + 2 * rcx], 0x7f                                    | 48 83 0c 48 7f                            |
    | or qword [rax + 4 * rcx], 0x80                                    | 48 83 0c 88 80                            |
    | or qword [rax + 8 * rcx], 0xff                                    | 48 83 0c c8 ff                            |
    | or qword [r8 + 1 * r9], 0x00                                      | 4b 83 0c 08 00                            |
    | or qword [r8 + 4 * r9], 0x7f                                      | 4b 83 0c 88 7f                            |
    | or qword [r8 + 8 * r9], 0x80                                      | 4b 83 0c c8 80                            |
    | or qword [1 * rcx], 0xff                                          | 48 83 0c 0d 00 00 00 00 ff                |
    | or qword [2 * rcx], 0x00                                          | 48 83 0c 4d 00 00 00 00 00                |
    | or qword [8 * rcx], 0x7f                                          | 48 83 0c cd 00 00 00 00 7f                |
    | or qword [1 * r9], 0x80                                           | 4a 83 0c 0d 00 00 00 00 80                |
    | or qword [2 * r9], 0xff                                           | 4a 83 0c 4d 00 00 00 00 ff                |
    | or qword [4 * r9], 0x00                                           | 4a 83 0c 8d 00 00 00 00 00                |
    | or qword [r13 + 8 * r12], 0x7f                                    | 4b 83 4c e5 00 7f                         |
    | or qword [rsp + 4 * r15], 0x80                                    | 4a 83 0c bc 80                            |
    | or qword [rax + 1 * rcx + 0x00], 0xff                             | 48 83 4c 08 00 ff                         |
    | or qword [rax + 1 * rcx - 0x00], 0x00                             | 48 83 4c 08 00 00                         |
    | or qword [rax + 1 * rcx - 0x01], 0x7f                             | 48 83 4c 08 ff 7f                         |
    | or qword [rax + 1 * rcx + 0x00000001], 0x80                       | 48 83 8c 08 01 00 00 00 80                |
    | or qword [rax + 1 * rcx - 0x00000001], 0xff                       | 48 83 8c 08 ff ff ff ff ff                |
    | or qword [rax + 1 * rcx + 0x7f], 0x00                             | 48 83 4c 08 7f 00                         |
    | or qword [rax + 1 * rcx + 0x80], 0x7f                             | 48 83 8c 08 80 00 00 00 7f                |
    | or qword [rax + 1 * rcx - 0x80], 0x80                             | 48 83 4c 08 80 80                         |
    | or qword [rax + 1 * rcx - 0x81], 0xff                             | 48 83 8c 08 7f ff ff ff ff                |
    | or qword [rax + 1 * rcx + 0xff], 0x00                             | 48 83 8c 08 ff 00 00 00 00                |
    | or qword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 48 83 8c 08 ff ff ff 7f 7f                |
    | or qword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 48 83 8c 08 01 00 00 80 80                |
    | or qword [rax + 1 * rcx - 0x80000000], 0xff                       | 48 83 8c 08 00 00 00 80 ff                |
    | or qword [r10 + 0x7f], 0x00                                       | 49 83 4a 7f 00                            |
    | or qword [r10 - 0x80], 0x7f                                       | 49 83 4a 80 7f                            |
    | or qword [r10 - 0x81], 0x80                                       | 49 83 8a 7f ff ff ff 80                   |
    | .prev5: nop; nop; nop; nop; nop; or qword [rel @prev5], 0xff      | 90 90 90 90 90 48 83 0d f3 ff ff ff ff    |
    | .prev1: nop; or qword [rel @prev1], 0x00                          | 90 48 83 0d f7 ff ff ff 00                |
    | or qword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 48 83 0d 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------------- |
"""


def can_encode_or_addr64_imm8():
    encode(OR_ADDR64_IMM8)


OR_ADDR64_IMM32 = """
    | ----------------------------------------------------------------------- | -------------------------------------------------- |
    | instruction                                                             | encoding                                           |
    | ----------------------------------------------------------------------- | -------------------------------------------------- |
    | or qword [rax], 0x00000001                                              | 48 81 08 01 00 00 00                               |
    | or qword [rcx], 0x00000001                                              | 48 81 09 01 00 00 00                               |
    | or qword [rdx], 0x00000001                                              | 48 81 0a 01 00 00 00                               |
    | or qword [rbx], 0x00000001                                              | 48 81 0b 01 00 00 00                               |
    | or qword [rsp], 0x00000001                                              | 48 81 0c 24 01 00 00 00                            |
    | or qword [rbp], 0x00000001                                              | 48 81 4d 00 01 00 00 00                            |
    | or qword [rsi], 0x00000001                                              | 48 81 0e 01 00 00 00                               |
    | or qword [rdi], 0x00000001                                              | 48 81 0f 01 00 00 00                               |
    | or qword [r8], 0x00000001                                               | 49 81 08 01 00 00 00                               |
    | or qword [r9], 0x00000001                                               | 49 81 09 01 00 00 00                               |
    | or qword [r10], 0x00000001                                              | 49 81 0a 01 00 00 00                               |
    | or qword [r11], 0x00000001                                              | 49 81 0b 01 00 00 00                               |
    | or qword [r12], 0x00000001                                              | 49 81 0c 24 01 00 00 00                            |
    | or qword [r13], 0x00000001                                              | 49 81 4d 00 01 00 00 00                            |
    | or qword [r14], 0x00000001                                              | 49 81 0e 01 00 00 00                               |
    | or qword [r15], 0x00000001                                              | 49 81 0f 01 00 00 00                               |
    | or qword [rax + 1 * rcx], 0x00000001                                    | 48 81 0c 08 01 00 00 00                            |
    | or qword [rcx + 1 * rcx], 0x00000001                                    | 48 81 0c 09 01 00 00 00                            |
    | or qword [rdx + 1 * rcx], 0x00000001                                    | 48 81 0c 0a 01 00 00 00                            |
    | or qword [rbx + 1 * rcx], 0x00000001                                    | 48 81 0c 0b 01 00 00 00                            |
    | or qword [rsp + 1 * rcx], 0x00000001                                    | 48 81 0c 0c 01 00 00 00                            |
    | or qword [rbp + 1 * rcx], 0x00000001                                    | 48 81 4c 0d 00 01 00 00 00                         |
    | or qword [rsi + 1 * rcx], 0x00000001                                    | 48 81 0c 0e 01 00 00 00                            |
    | or qword [rdi + 1 * rcx], 0x00000001                                    | 48 81 0c 0f 01 00 00 00                            |
    | or qword [r8 + 1 * rcx], 0x00000001                                     | 49 81 0c 08 01 00 00 00                            |
    | or qword [r9 + 1 * rcx], 0x00000001                                     | 49 81 0c 09 01 00 00 00                            |
    | or qword [r10 + 1 * rcx], 0x00000001                                    | 49 81 0c 0a 01 00 00 00                            |
    | or qword [r11 + 1 * rcx], 0x00000001                                    | 49 81 0c 0b 01 00 00 00                            |
    | or qword [r12 + 1 * rcx], 0x00000001                                    | 49 81 0c 0c 01 00 00 00                            |
    | or qword [r13 + 1 * rcx], 0x00000001                                    | 49 81 4c 0d 00 01 00 00 00                         |
    | or qword [r14 + 1 * rcx], 0x00000001                                    | 49 81 0c 0e 01 00 00 00                            |
    | or qword [r15 + 1 * rcx], 0x00000001                                    | 49 81 0c 0f 01 00 00 00                            |
    | or qword [rax + 1 * rax], 0x00000001                                    | 48 81 0c 00 01 00 00 00                            |
    | or qword [rax + 1 * rdx], 0x00000001                                    | 48 81 0c 10 01 00 00 00                            |
    | or qword [rax + 1 * rbx], 0x00000001                                    | 48 81 0c 18 01 00 00 00                            |
    | or qword [rax + 1 * rbp], 0x00000001                                    | 48 81 0c 28 01 00 00 00                            |
    | or qword [rax + 1 * rsi], 0x00000001                                    | 48 81 0c 30 01 00 00 00                            |
    | or qword [rax + 1 * rdi], 0x00000001                                    | 48 81 0c 38 01 00 00 00                            |
    | or qword [rax + 1 * r8], 0x00000001                                     | 4a 81 0c 00 01 00 00 00                            |
    | or qword [rax + 1 * r9], 0x00000001                                     | 4a 81 0c 08 01 00 00 00                            |
    | or qword [rax + 1 * r10], 0x00000001                                    | 4a 81 0c 10 01 00 00 00                            |
    | or qword [rax + 1 * r11], 0x00000001                                    | 4a 81 0c 18 01 00 00 00                            |
    | or qword [rax + 1 * r12], 0x00000001                                    | 4a 81 0c 20 01 00 00 00                            |
    | or qword [rax + 1 * r13], 0x00000001                                    | 4a 81 0c 28 01 00 00 00                            |
    | or qword [rax + 1 * r14], 0x00000001                                    | 4a 81 0c 30 01 00 00 00                            |
    | or qword [rax + 1 * r15], 0x00000001                                    | 4a 81 0c 38 01 00 00 00                            |
    | or qword [rax + 2 * rcx], 0x00000001                                    | 48 81 0c 48 01 00 00 00                            |
    | or qword [rax + 4 * rcx], 0x00000001                                    | 48 81 0c 88 01 00 00 00                            |
    | or qword [rax + 8 * rcx], 0x00000001                                    | 48 81 0c c8 01 00 00 00                            |
    | or qword [r8 + 1 * r9], 0x00000001                                      | 4b 81 0c 08 01 00 00 00                            |
    | or qword [r8 + 2 * r9], 0x00000001                                      | 4b 81 0c 48 01 00 00 00                            |
    | or qword [r8 + 4 * r9], 0x00000001                                      | 4b 81 0c 88 01 00 00 00                            |
    | or qword [r8 + 8 * r9], 0x00000001                                      | 4b 81 0c c8 01 00 00 00                            |
    | or qword [1 * rcx], 0x00000001                                          | 48 81 0c 0d 00 00 00 00 01 00 00 00                |
    | or qword [2 * rcx], 0x00000001                                          | 48 81 0c 4d 00 00 00 00 01 00 00 00                |
    | or qword [4 * rcx], 0x00000001                                          | 48 81 0c 8d 00 00 00 00 01 00 00 00                |
    | or qword [8 * rcx], 0x00000001                                          | 48 81 0c cd 00 00 00 00 01 00 00 00                |
    | or qword [1 * r9], 0x00000001                                           | 4a 81 0c 0d 00 00 00 00 01 00 00 00                |
    | or qword [2 * r9], 0x00000001                                           | 4a 81 0c 4d 00 00 00 00 01 00 00 00                |
    | or qword [4 * r9], 0x00000001                                           | 4a 81 0c 8d 00 00 00 00 01 00 00 00                |
    | or qword [8 * r9], 0x00000001                                           | 4a 81 0c cd 00 00 00 00 01 00 00 00                |
    | or qword [r13 + 8 * r12], 0x00000001                                    | 4b 81 4c e5 00 01 00 00 00                         |
    | or qword [rsp + 4 * r15], 0x00000001                                    | 4a 81 0c bc 01 00 00 00                            |
    | or qword [rax + 1 * rcx + 0x00], 0x00000001                             | 48 81 4c 08 00 01 00 00 00                         |
    | or qword [rax + 1 * rcx - 0x00], 0x00000001                             | 48 81 4c 08 00 01 00 00 00                         |
    | or qword [rax + 1 * rcx + 0x01], 0x00000001                             | 48 81 4c 08 01 01 00 00 00                         |
    | or qword [rax + 1 * rcx - 0x01], 0x00000001                             | 48 81 4c 08 ff 01 00 00 00                         |
    | or qword [rax + 1 * rcx + 0x00000001], 0x00000001                       | 48 81 8c 08 01 00 00 00 01 00 00 00                |
    | or qword [rax + 1 * rcx - 0x00000001], 0x00000001                       | 48 81 8c 08 ff ff ff ff 01 00 00 00                |
    | or qword [rax + 1 * rcx + 0x7f], 0x00000001                             | 48 81 4c 08 7f 01 00 00 00                         |
    | or qword [rax + 1 * rcx - 0x7f], 0x00000001                             | 48 81 4c 08 81 01 00 00 00                         |
    | or qword [rax + 1 * rcx + 0x80], 0x00000001                             | 48 81 8c 08 80 00 00 00 01 00 00 00                |
    | or qword [rax + 1 * rcx - 0x80], 0x00000001                             | 48 81 4c 08 80 01 00 00 00                         |
    | or qword [rax + 1 * rcx - 0x81], 0x00000001                             | 48 81 8c 08 7f ff ff ff 01 00 00 00                |
    | or qword [rax + 1 * rcx + 0xff], 0x00000001                             | 48 81 8c 08 ff 00 00 00 01 00 00 00                |
    | or qword [rax + 1 * rcx - 0xff], 0x00000001                             | 48 81 8c 08 01 ff ff ff 01 00 00 00                |
    | or qword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | 48 81 8c 08 ff ff ff 7f 01 00 00 00                |
    | or qword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | 48 81 8c 08 01 00 00 80 01 00 00 00                |
    | or qword [rax + 1 * rcx - 0x80000000], 0x00000001                       | 48 81 8c 08 00 00 00 80 01 00 00 00                |
    | or qword [r10 + 0x7f], 0x00000001                                       | 49 81 4a 7f 01 00 00 00                            |
    | or qword [r10 + 0x80], 0x00000001                                       | 49 81 8a 80 00 00 00 01 00 00 00                   |
    | or qword [r10 - 0x80], 0x00000001                                       | 49 81 4a 80 01 00 00 00                            |
    | or qword [r10 - 0x81], 0x00000001                                       | 49 81 8a 7f ff ff ff 01 00 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; or qword [rel @prev5], 0x00000001      | 90 90 90 90 90 48 81 0d f0 ff ff ff 01 00 00 00    |
    | .prev1: nop; or qword [rel @prev1], 0x00000001                          | 90 48 81 0d f4 ff ff ff 01 00 00 00                |
    | or qword [rel @next1], 0x00000001; nop; .next1: nop                     | 48 81 0d 01 00 00 00 01 00 00 00 90 90             |
    | or qword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | 48 81 0d 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | or qword [rax], 0x00000000                                              | 48 81 08 00 00 00 00                               |
    | or qword [rax], 0x0000007f                                              | 48 81 08 7f 00 00 00                               |
    | or qword [rax], 0x00000080                                              | 48 81 08 80 00 00 00                               |
    | or qword [rax], 0x000000ff                                              | 48 81 08 ff 00 00 00                               |
    | or qword [rax], 0x00000100                                              | 48 81 08 00 01 00 00                               |
    | or qword [rax], 0x00007fff                                              | 48 81 08 ff 7f 00 00                               |
    | or qword [rax], 0x00008000                                              | 48 81 08 00 80 00 00                               |
    | or qword [rax], 0x0000ffff                                              | 48 81 08 ff ff 00 00                               |
    | or qword [rax], 0x00010000                                              | 48 81 08 00 00 01 00                               |
    | or qword [rax], 0x7fffffff                                              | 48 81 08 ff ff ff 7f                               |
    | or qword [rax], 0x80000000                                              | 48 81 08 00 00 00 80                               |
    | or qword [rax], 0xffffffff                                              | 48 81 08 ff ff ff ff                               |
    | or qword [rcx], 0x0000007f                                              | 48 81 09 7f 00 00 00                               |
    | or qword [rdx], 0x00000080                                              | 48 81 0a 80 00 00 00                               |
    | or qword [rbx], 0x000000ff                                              | 48 81 0b ff 00 00 00                               |
    | or qword [rsp], 0x00000100                                              | 48 81 0c 24 00 01 00 00                            |
    | or qword [rbp], 0x00007fff                                              | 48 81 4d 00 ff 7f 00 00                            |
    | or qword [rsi], 0x00008000                                              | 48 81 0e 00 80 00 00                               |
    | or qword [rdi], 0x0000ffff                                              | 48 81 0f ff ff 00 00                               |
    | or qword [r8], 0x00010000                                               | 49 81 08 00 00 01 00                               |
    | or qword [r9], 0x7fffffff                                               | 49 81 09 ff ff ff 7f                               |
    | or qword [r10], 0x80000000                                              | 49 81 0a 00 00 00 80                               |
    | or qword [r11], 0xffffffff                                              | 49 81 0b ff ff ff ff                               |
    | or qword [r12], 0x00000000                                              | 49 81 0c 24 00 00 00 00                            |
    | or qword [r14], 0x0000007f                                              | 49 81 0e 7f 00 00 00                               |
    | or qword [r15], 0x00000080                                              | 49 81 0f 80 00 00 00                               |
    | or qword [rax + 1 * rcx], 0x000000ff                                    | 48 81 0c 08 ff 00 00 00                            |
    | or qword [rcx + 1 * rcx], 0x00000100                                    | 48 81 0c 09 00 01 00 00                            |
    | or qword [rdx + 1 * rcx], 0x00007fff                                    | 48 81 0c 0a ff 7f 00 00                            |
    | or qword [rbx + 1 * rcx], 0x00008000                                    | 48 81 0c 0b 00 80 00 00                            |
    | or qword [rsp + 1 * rcx], 0x0000ffff                                    | 48 81 0c 0c ff ff 00 00                            |
    | or qword [rbp + 1 * rcx], 0x00010000                                    | 48 81 4c 0d 00 00 00 01 00                         |
    | or qword [rsi + 1 * rcx], 0x7fffffff                                    | 48 81 0c 0e ff ff ff 7f                            |
    | or qword [rdi + 1 * rcx], 0x80000000                                    | 48 81 0c 0f 00 00 00 80                            |
    | or qword [r8 + 1 * rcx], 0xffffffff                                     | 49 81 0c 08 ff ff ff ff                            |
    | or qword [r9 + 1 * rcx], 0x00000000                                     | 49 81 0c 09 00 00 00 00                            |
    | or qword [r11 + 1 * rcx], 0x0000007f                                    | 49 81 0c 0b 7f 00 00 00                            |
    | or qword [r12 + 1 * rcx], 0x00000080                                    | 49 81 0c 0c 80 00 00 00                            |
    | or qword [r13 + 1 * rcx], 0x000000ff                                    | 49 81 4c 0d 00 ff 00 00 00                         |
    | or qword [r14 + 1 * rcx], 0x00000100                                    | 49 81 0c 0e 00 01 00 00                            |
    | or qword [r15 + 1 * rcx], 0x00007fff                                    | 49 81 0c 0f ff 7f 00 00                            |
    | or qword [rax + 1 * rax], 0x00008000                                    | 48 81 0c 00 00 80 00 00                            |
    | or qword [rax + 1 * rdx], 0x0000ffff                                    | 48 81 0c 10 ff ff 00 00                            |
    | or qword [rax + 1 * rbx], 0x00010000                                    | 48 81 0c 18 00 00 01 00                            |
    | or qword [rax + 1 * rbp], 0x7fffffff                                    | 48 81 0c 28 ff ff ff 7f                            |
    | or qword [rax + 1 * rsi], 0x80000000                                    | 48 81 0c 30 00 00 00 80                            |
    | or qword [rax + 1 * rdi], 0xffffffff                                    | 48 81 0c 38 ff ff ff ff                            |
    | or qword [rax + 1 * r8], 0x00000000                                     | 4a 81 0c 00 00 00 00 00                            |
    | or qword [rax + 1 * r10], 0x0000007f                                    | 4a 81 0c 10 7f 00 00 00                            |
    | or qword [rax + 1 * r11], 0x00000080                                    | 4a 81 0c 18 80 00 00 00                            |
    | or qword [rax + 1 * r12], 0x000000ff                                    | 4a 81 0c 20 ff 00 00 00                            |
    | or qword [rax + 1 * r13], 0x00000100                                    | 4a 81 0c 28 00 01 00 00                            |
    | or qword [rax + 1 * r14], 0x00007fff                                    | 4a 81 0c 30 ff 7f 00 00                            |
    | or qword [rax + 1 * r15], 0x00008000                                    | 4a 81 0c 38 00 80 00 00                            |
    | or qword [rax + 2 * rcx], 0x0000ffff                                    | 48 81 0c 48 ff ff 00 00                            |
    | or qword [rax + 4 * rcx], 0x00010000                                    | 48 81 0c 88 00 00 01 00                            |
    | or qword [rax + 8 * rcx], 0x7fffffff                                    | 48 81 0c c8 ff ff ff 7f                            |
    | or qword [r8 + 1 * r9], 0x80000000                                      | 4b 81 0c 08 00 00 00 80                            |
    | or qword [r8 + 2 * r9], 0xffffffff                                      | 4b 81 0c 48 ff ff ff ff                            |
    | or qword [r8 + 4 * r9], 0x00000000                                      | 4b 81 0c 88 00 00 00 00                            |
    | or qword [1 * rcx], 0x0000007f                                          | 48 81 0c 0d 00 00 00 00 7f 00 00 00                |
    | or qword [2 * rcx], 0x00000080                                          | 48 81 0c 4d 00 00 00 00 80 00 00 00                |
    | or qword [4 * rcx], 0x000000ff                                          | 48 81 0c 8d 00 00 00 00 ff 00 00 00                |
    | or qword [8 * rcx], 0x00000100                                          | 48 81 0c cd 00 00 00 00 00 01 00 00                |
    | or qword [1 * r9], 0x00007fff                                           | 4a 81 0c 0d 00 00 00 00 ff 7f 00 00                |
    | or qword [2 * r9], 0x00008000                                           | 4a 81 0c 4d 00 00 00 00 00 80 00 00                |
    | or qword [4 * r9], 0x0000ffff                                           | 4a 81 0c 8d 00 00 00 00 ff ff 00 00                |
    | or qword [8 * r9], 0x00010000                                           | 4a 81 0c cd 00 00 00 00 00 00 01 00                |
    | or qword [r13 + 8 * r12], 0x7fffffff                                    | 4b 81 4c e5 00 ff ff ff 7f                         |
    | or qword [rsp + 4 * r15], 0x80000000                                    | 4a 81 0c bc 00 00 00 80                            |
    | or qword [rax + 1 * rcx + 0x00], 0xffffffff                             | 48 81 4c 08 00 ff ff ff ff                         |
    | or qword [rax + 1 * rcx - 0x00], 0x00000000                             | 48 81 4c 08 00 00 00 00 00                         |
    | or qword [rax + 1 * rcx - 0x01], 0x0000007f                             | 48 81 4c 08 ff 7f 00 00 00                         |
    | or qword [rax + 1 * rcx + 0x00000001], 0x00000080                       | 48 81 8c 08 01 00 00 00 80 00 00 00                |
    | or qword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | 48 81 8c 08 ff ff ff ff ff 00 00 00                |
    | or qword [rax + 1 * rcx + 0x7f], 0x00000100                             | 48 81 4c 08 7f 00 01 00 00                         |
    | or qword [rax + 1 * rcx - 0x7f], 0x00007fff                             | 48 81 4c 08 81 ff 7f 00 00                         |
    | or qword [rax + 1 * rcx + 0x80], 0x00008000                             | 48 81 8c 08 80 00 00 00 00 80 00 00                |
    | or qword [rax + 1 * rcx - 0x80], 0x0000ffff                             | 48 81 4c 08 80 ff ff 00 00                         |
    | or qword [rax + 1 * rcx - 0x81], 0x00010000                             | 48 81 8c 08 7f ff ff ff 00 00 01 00                |
    | or qword [rax + 1 * rcx + 0xff], 0x7fffffff                             | 48 81 8c 08 ff 00 00 00 ff ff ff 7f                |
    | or qword [rax + 1 * rcx - 0xff], 0x80000000                             | 48 81 8c 08 01 ff ff ff 00 00 00 80                |
    | or qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | 48 81 8c 08 ff ff ff 7f ff ff ff ff                |
    | or qword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | 48 81 8c 08 01 00 00 80 00 00 00 00                |
    | or qword [r10 + 0x7f], 0x0000007f                                       | 49 81 4a 7f 7f 00 00 00                            |
    | or qword [r10 + 0x80], 0x00000080                                       | 49 81 8a 80 00 00 00 80 00 00 00                   |
    | or qword [r10 - 0x80], 0x000000ff                                       | 49 81 4a 80 ff 00 00 00                            |
    | or qword [r10 - 0x81], 0x00000100                                       | 49 81 8a 7f ff ff ff 00 01 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; or qword [rel @prev5], 0x00007fff      | 90 90 90 90 90 48 81 0d f0 ff ff ff ff 7f 00 00    |
    | .prev1: nop; or qword [rel @prev1], 0x00008000                          | 90 48 81 0d f4 ff ff ff 00 80 00 00                |
    | or qword [rel @next1], 0x0000ffff; nop; .next1: nop                     | 48 81 0d 01 00 00 00 ff ff 00 00 90 90             |
    | or qword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | 48 81 0d 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------------- | -------------------------------------------------- |
"""


def can_encode_or_addr64_imm32():
    encode(OR_ADDR64_IMM32)


OR_ADDR64_REG64 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | or qword [rax], rcx                                              | 48 09 08                               |
    | or qword [rcx], rcx                                              | 48 09 09                               |
    | or qword [rdx], rcx                                              | 48 09 0a                               |
    | or qword [rbx], rcx                                              | 48 09 0b                               |
    | or qword [rsp], rcx                                              | 48 09 0c 24                            |
    | or qword [rbp], rcx                                              | 48 09 4d 00                            |
    | or qword [rsi], rcx                                              | 48 09 0e                               |
    | or qword [rdi], rcx                                              | 48 09 0f                               |
    | or qword [r8], rcx                                               | 49 09 08                               |
    | or qword [r9], rcx                                               | 49 09 09                               |
    | or qword [r10], rcx                                              | 49 09 0a                               |
    | or qword [r11], rcx                                              | 49 09 0b                               |
    | or qword [r12], rcx                                              | 49 09 0c 24                            |
    | or qword [r13], rcx                                              | 49 09 4d 00                            |
    | or qword [r14], rcx                                              | 49 09 0e                               |
    | or qword [r15], rcx                                              | 49 09 0f                               |
    | or qword [rax + 1 * rcx], rcx                                    | 48 09 0c 08                            |
    | or qword [rcx + 1 * rcx], rcx                                    | 48 09 0c 09                            |
    | or qword [rdx + 1 * rcx], rcx                                    | 48 09 0c 0a                            |
    | or qword [rbx + 1 * rcx], rcx                                    | 48 09 0c 0b                            |
    | or qword [rsp + 1 * rcx], rcx                                    | 48 09 0c 0c                            |
    | or qword [rbp + 1 * rcx], rcx                                    | 48 09 4c 0d 00                         |
    | or qword [rsi + 1 * rcx], rcx                                    | 48 09 0c 0e                            |
    | or qword [rdi + 1 * rcx], rcx                                    | 48 09 0c 0f                            |
    | or qword [r8 + 1 * rcx], rcx                                     | 49 09 0c 08                            |
    | or qword [r9 + 1 * rcx], rcx                                     | 49 09 0c 09                            |
    | or qword [r10 + 1 * rcx], rcx                                    | 49 09 0c 0a                            |
    | or qword [r11 + 1 * rcx], rcx                                    | 49 09 0c 0b                            |
    | or qword [r12 + 1 * rcx], rcx                                    | 49 09 0c 0c                            |
    | or qword [r13 + 1 * rcx], rcx                                    | 49 09 4c 0d 00                         |
    | or qword [r14 + 1 * rcx], rcx                                    | 49 09 0c 0e                            |
    | or qword [r15 + 1 * rcx], rcx                                    | 49 09 0c 0f                            |
    | or qword [rax + 1 * rax], rcx                                    | 48 09 0c 00                            |
    | or qword [rax + 1 * rdx], rcx                                    | 48 09 0c 10                            |
    | or qword [rax + 1 * rbx], rcx                                    | 48 09 0c 18                            |
    | or qword [rax + 1 * rbp], rcx                                    | 48 09 0c 28                            |
    | or qword [rax + 1 * rsi], rcx                                    | 48 09 0c 30                            |
    | or qword [rax + 1 * rdi], rcx                                    | 48 09 0c 38                            |
    | or qword [rax + 1 * r8], rcx                                     | 4a 09 0c 00                            |
    | or qword [rax + 1 * r9], rcx                                     | 4a 09 0c 08                            |
    | or qword [rax + 1 * r10], rcx                                    | 4a 09 0c 10                            |
    | or qword [rax + 1 * r11], rcx                                    | 4a 09 0c 18                            |
    | or qword [rax + 1 * r12], rcx                                    | 4a 09 0c 20                            |
    | or qword [rax + 1 * r13], rcx                                    | 4a 09 0c 28                            |
    | or qword [rax + 1 * r14], rcx                                    | 4a 09 0c 30                            |
    | or qword [rax + 1 * r15], rcx                                    | 4a 09 0c 38                            |
    | or qword [rax + 2 * rcx], rcx                                    | 48 09 0c 48                            |
    | or qword [rax + 4 * rcx], rcx                                    | 48 09 0c 88                            |
    | or qword [rax + 8 * rcx], rcx                                    | 48 09 0c c8                            |
    | or qword [r8 + 1 * r9], rcx                                      | 4b 09 0c 08                            |
    | or qword [r8 + 2 * r9], rcx                                      | 4b 09 0c 48                            |
    | or qword [r8 + 4 * r9], rcx                                      | 4b 09 0c 88                            |
    | or qword [r8 + 8 * r9], rcx                                      | 4b 09 0c c8                            |
    | or qword [1 * rcx], rcx                                          | 48 09 0c 0d 00 00 00 00                |
    | or qword [2 * rcx], rcx                                          | 48 09 0c 4d 00 00 00 00                |
    | or qword [4 * rcx], rcx                                          | 48 09 0c 8d 00 00 00 00                |
    | or qword [8 * rcx], rcx                                          | 48 09 0c cd 00 00 00 00                |
    | or qword [1 * r9], rcx                                           | 4a 09 0c 0d 00 00 00 00                |
    | or qword [2 * r9], rcx                                           | 4a 09 0c 4d 00 00 00 00                |
    | or qword [4 * r9], rcx                                           | 4a 09 0c 8d 00 00 00 00                |
    | or qword [8 * r9], rcx                                           | 4a 09 0c cd 00 00 00 00                |
    | or qword [r13 + 8 * r12], rcx                                    | 4b 09 4c e5 00                         |
    | or qword [rsp + 4 * r15], rcx                                    | 4a 09 0c bc                            |
    | or qword [rax + 1 * rcx + 0x00], rcx                             | 48 09 4c 08 00                         |
    | or qword [rax + 1 * rcx - 0x00], rcx                             | 48 09 4c 08 00                         |
    | or qword [rax + 1 * rcx + 0x01], rcx                             | 48 09 4c 08 01                         |
    | or qword [rax + 1 * rcx - 0x01], rcx                             | 48 09 4c 08 ff                         |
    | or qword [rax + 1 * rcx + 0x00000001], rcx                       | 48 09 8c 08 01 00 00 00                |
    | or qword [rax + 1 * rcx - 0x00000001], rcx                       | 48 09 8c 08 ff ff ff ff                |
    | or qword [rax + 1 * rcx + 0x7f], rcx                             | 48 09 4c 08 7f                         |
    | or qword [rax + 1 * rcx - 0x7f], rcx                             | 48 09 4c 08 81                         |
    | or qword [rax + 1 * rcx + 0x80], rcx                             | 48 09 8c 08 80 00 00 00                |
    | or qword [rax + 1 * rcx - 0x80], rcx                             | 48 09 4c 08 80                         |
    | or qword [rax + 1 * rcx - 0x81], rcx                             | 48 09 8c 08 7f ff ff ff                |
    | or qword [rax + 1 * rcx + 0xff], rcx                             | 48 09 8c 08 ff 00 00 00                |
    | or qword [rax + 1 * rcx - 0xff], rcx                             | 48 09 8c 08 01 ff ff ff                |
    | or qword [rax + 1 * rcx + 0x7fffffff], rcx                       | 48 09 8c 08 ff ff ff 7f                |
    | or qword [rax + 1 * rcx - 0x7fffffff], rcx                       | 48 09 8c 08 01 00 00 80                |
    | or qword [rax + 1 * rcx - 0x80000000], rcx                       | 48 09 8c 08 00 00 00 80                |
    | or qword [r10 + 0x7f], rcx                                       | 49 09 4a 7f                            |
    | or qword [r10 + 0x80], rcx                                       | 49 09 8a 80 00 00 00                   |
    | or qword [r10 - 0x80], rcx                                       | 49 09 4a 80                            |
    | or qword [r10 - 0x81], rcx                                       | 49 09 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or qword [rel @prev5], rcx      | 90 90 90 90 90 48 09 0d f4 ff ff ff    |
    | .prev1: nop; or qword [rel @prev1], rcx                          | 90 48 09 0d f8 ff ff ff                |
    | or qword [rel @next1], rcx; nop; .next1: nop                     | 48 09 0d 01 00 00 00 90 90             |
    | or qword [rel @next5], rcx; nop; nop; nop; nop; nop; .next5: nop | 48 09 0d 05 00 00 00 90 90 90 90 90 90 |
    | or qword [rax], rax                                              | 48 09 00                               |
    | or qword [rax], rdx                                              | 48 09 10                               |
    | or qword [rax], rbx                                              | 48 09 18                               |
    | or qword [rax], rsp                                              | 48 09 20                               |
    | or qword [rax], rbp                                              | 48 09 28                               |
    | or qword [rax], rsi                                              | 48 09 30                               |
    | or qword [rax], rdi                                              | 48 09 38                               |
    | or qword [rax], r8                                               | 4c 09 00                               |
    | or qword [rax], r9                                               | 4c 09 08                               |
    | or qword [rax], r10                                              | 4c 09 10                               |
    | or qword [rax], r11                                              | 4c 09 18                               |
    | or qword [rax], r12                                              | 4c 09 20                               |
    | or qword [rax], r13                                              | 4c 09 28                               |
    | or qword [rax], r14                                              | 4c 09 30                               |
    | or qword [rax], r15                                              | 4c 09 38                               |
    | or qword [rcx], rdx                                              | 48 09 11                               |
    | or qword [rdx], rbx                                              | 48 09 1a                               |
    | or qword [rbx], rsp                                              | 48 09 23                               |
    | or qword [rsp], rbp                                              | 48 09 2c 24                            |
    | or qword [rbp], rsi                                              | 48 09 75 00                            |
    | or qword [rsi], rdi                                              | 48 09 3e                               |
    | or qword [rdi], r8                                               | 4c 09 07                               |
    | or qword [r8], r9                                                | 4d 09 08                               |
    | or qword [r9], r10                                               | 4d 09 11                               |
    | or qword [r10], r11                                              | 4d 09 1a                               |
    | or qword [r11], r12                                              | 4d 09 23                               |
    | or qword [r12], r13                                              | 4d 09 2c 24                            |
    | or qword [r13], r14                                              | 4d 09 75 00                            |
    | or qword [r14], r15                                              | 4d 09 3e                               |
    | or qword [r15], rax                                              | 49 09 07                               |
    | or qword [rcx + 1 * rcx], rdx                                    | 48 09 14 09                            |
    | or qword [rdx + 1 * rcx], rbx                                    | 48 09 1c 0a                            |
    | or qword [rbx + 1 * rcx], rsp                                    | 48 09 24 0b                            |
    | or qword [rsp + 1 * rcx], rbp                                    | 48 09 2c 0c                            |
    | or qword [rbp + 1 * rcx], rsi                                    | 48 09 74 0d 00                         |
    | or qword [rsi + 1 * rcx], rdi                                    | 48 09 3c 0e                            |
    | or qword [rdi + 1 * rcx], r8                                     | 4c 09 04 0f                            |
    | or qword [r8 + 1 * rcx], r9                                      | 4d 09 0c 08                            |
    | or qword [r9 + 1 * rcx], r10                                     | 4d 09 14 09                            |
    | or qword [r10 + 1 * rcx], r11                                    | 4d 09 1c 0a                            |
    | or qword [r11 + 1 * rcx], r12                                    | 4d 09 24 0b                            |
    | or qword [r12 + 1 * rcx], r13                                    | 4d 09 2c 0c                            |
    | or qword [r13 + 1 * rcx], r14                                    | 4d 09 74 0d 00                         |
    | or qword [r14 + 1 * rcx], r15                                    | 4d 09 3c 0e                            |
    | or qword [r15 + 1 * rcx], rax                                    | 49 09 04 0f                            |
    | or qword [rax + 1 * rdx], rdx                                    | 48 09 14 10                            |
    | or qword [rax + 1 * rbx], rbx                                    | 48 09 1c 18                            |
    | or qword [rax + 1 * rbp], rsp                                    | 48 09 24 28                            |
    | or qword [rax + 1 * rsi], rbp                                    | 48 09 2c 30                            |
    | or qword [rax + 1 * rdi], rsi                                    | 48 09 34 38                            |
    | or qword [rax + 1 * r8], rdi                                     | 4a 09 3c 00                            |
    | or qword [rax + 1 * r9], r8                                      | 4e 09 04 08                            |
    | or qword [rax + 1 * r10], r9                                     | 4e 09 0c 10                            |
    | or qword [rax + 1 * r11], r10                                    | 4e 09 14 18                            |
    | or qword [rax + 1 * r12], r11                                    | 4e 09 1c 20                            |
    | or qword [rax + 1 * r13], r12                                    | 4e 09 24 28                            |
    | or qword [rax + 1 * r14], r13                                    | 4e 09 2c 30                            |
    | or qword [rax + 1 * r15], r14                                    | 4e 09 34 38                            |
    | or qword [rax + 2 * rcx], r15                                    | 4c 09 3c 48                            |
    | or qword [rax + 4 * rcx], rax                                    | 48 09 04 88                            |
    | or qword [r8 + 1 * r9], rdx                                      | 4b 09 14 08                            |
    | or qword [r8 + 2 * r9], rbx                                      | 4b 09 1c 48                            |
    | or qword [r8 + 4 * r9], rsp                                      | 4b 09 24 88                            |
    | or qword [r8 + 8 * r9], rbp                                      | 4b 09 2c c8                            |
    | or qword [1 * rcx], rsi                                          | 48 09 34 0d 00 00 00 00                |
    | or qword [2 * rcx], rdi                                          | 48 09 3c 4d 00 00 00 00                |
    | or qword [4 * rcx], r8                                           | 4c 09 04 8d 00 00 00 00                |
    | or qword [8 * rcx], r9                                           | 4c 09 0c cd 00 00 00 00                |
    | or qword [1 * r9], r10                                           | 4e 09 14 0d 00 00 00 00                |
    | or qword [2 * r9], r11                                           | 4e 09 1c 4d 00 00 00 00                |
    | or qword [4 * r9], r12                                           | 4e 09 24 8d 00 00 00 00                |
    | or qword [8 * r9], r13                                           | 4e 09 2c cd 00 00 00 00                |
    | or qword [r13 + 8 * r12], r14                                    | 4f 09 74 e5 00                         |
    | or qword [rsp + 4 * r15], r15                                    | 4e 09 3c bc                            |
    | or qword [rax + 1 * rcx + 0x00], rax                             | 48 09 44 08 00                         |
    | or qword [rax + 1 * rcx + 0x01], rdx                             | 48 09 54 08 01                         |
    | or qword [rax + 1 * rcx - 0x01], rbx                             | 48 09 5c 08 ff                         |
    | or qword [rax + 1 * rcx + 0x00000001], rsp                       | 48 09 a4 08 01 00 00 00                |
    | or qword [rax + 1 * rcx - 0x00000001], rbp                       | 48 09 ac 08 ff ff ff ff                |
    | or qword [rax + 1 * rcx + 0x7f], rsi                             | 48 09 74 08 7f                         |
    | or qword [rax + 1 * rcx - 0x7f], rdi                             | 48 09 7c 08 81                         |
    | or qword [rax + 1 * rcx + 0x80], r8                              | 4c 09 84 08 80 00 00 00                |
    | or qword [rax + 1 * rcx - 0x80], r9                              | 4c 09 4c 08 80                         |
    | or qword [rax + 1 * rcx - 0x81], r10                             | 4c 09 94 08 7f ff ff ff                |
    | or qword [rax + 1 * rcx + 0xff], r11                             | 4c 09 9c 08 ff 00 00 00                |
    | or qword [rax + 1 * rcx - 0xff], r12                             | 4c 09 a4 08 01 ff ff ff                |
    | or qword [rax + 1 * rcx + 0x7fffffff], r13                       | 4c 09 ac 08 ff ff ff 7f                |
    | or qword [rax + 1 * rcx - 0x7fffffff], r14                       | 4c 09 b4 08 01 00 00 80                |
    | or qword [rax + 1 * rcx - 0x80000000], r15                       | 4c 09 bc 08 00 00 00 80                |
    | or qword [r10 + 0x7f], rax                                       | 49 09 42 7f                            |
    | or qword [r10 - 0x80], rdx                                       | 49 09 52 80                            |
    | or qword [r10 - 0x81], rbx                                       | 49 09 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or qword [rel @prev5], rsp      | 90 90 90 90 90 48 09 25 f4 ff ff ff    |
    | .prev1: nop; or qword [rel @prev1], rbp                          | 90 48 09 2d f8 ff ff ff                |
    | or qword [rel @next1], rsi; nop; .next1: nop                     | 48 09 35 01 00 00 00 90 90             |
    | or qword [rel @next5], rdi; nop; nop; nop; nop; nop; .next5: nop | 48 09 3d 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_addr64_reg64():
    encode(OR_ADDR64_REG64)


OR_ADDR32_IMM8 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | or dword [rax], 0x01                                              | 83 08 01                               |
    | or dword [rcx], 0x01                                              | 83 09 01                               |
    | or dword [rdx], 0x01                                              | 83 0a 01                               |
    | or dword [rbx], 0x01                                              | 83 0b 01                               |
    | or dword [rsp], 0x01                                              | 83 0c 24 01                            |
    | or dword [rbp], 0x01                                              | 83 4d 00 01                            |
    | or dword [rsi], 0x01                                              | 83 0e 01                               |
    | or dword [rdi], 0x01                                              | 83 0f 01                               |
    | or dword [r8], 0x01                                               | 41 83 08 01                            |
    | or dword [r9], 0x01                                               | 41 83 09 01                            |
    | or dword [r10], 0x01                                              | 41 83 0a 01                            |
    | or dword [r11], 0x01                                              | 41 83 0b 01                            |
    | or dword [r12], 0x01                                              | 41 83 0c 24 01                         |
    | or dword [r13], 0x01                                              | 41 83 4d 00 01                         |
    | or dword [r14], 0x01                                              | 41 83 0e 01                            |
    | or dword [r15], 0x01                                              | 41 83 0f 01                            |
    | or dword [rax + 1 * rcx], 0x01                                    | 83 0c 08 01                            |
    | or dword [rcx + 1 * rcx], 0x01                                    | 83 0c 09 01                            |
    | or dword [rdx + 1 * rcx], 0x01                                    | 83 0c 0a 01                            |
    | or dword [rbx + 1 * rcx], 0x01                                    | 83 0c 0b 01                            |
    | or dword [rsp + 1 * rcx], 0x01                                    | 83 0c 0c 01                            |
    | or dword [rbp + 1 * rcx], 0x01                                    | 83 4c 0d 00 01                         |
    | or dword [rsi + 1 * rcx], 0x01                                    | 83 0c 0e 01                            |
    | or dword [rdi + 1 * rcx], 0x01                                    | 83 0c 0f 01                            |
    | or dword [r8 + 1 * rcx], 0x01                                     | 41 83 0c 08 01                         |
    | or dword [r9 + 1 * rcx], 0x01                                     | 41 83 0c 09 01                         |
    | or dword [r10 + 1 * rcx], 0x01                                    | 41 83 0c 0a 01                         |
    | or dword [r11 + 1 * rcx], 0x01                                    | 41 83 0c 0b 01                         |
    | or dword [r12 + 1 * rcx], 0x01                                    | 41 83 0c 0c 01                         |
    | or dword [r13 + 1 * rcx], 0x01                                    | 41 83 4c 0d 00 01                      |
    | or dword [r14 + 1 * rcx], 0x01                                    | 41 83 0c 0e 01                         |
    | or dword [r15 + 1 * rcx], 0x01                                    | 41 83 0c 0f 01                         |
    | or dword [rax + 1 * rax], 0x01                                    | 83 0c 00 01                            |
    | or dword [rax + 1 * rdx], 0x01                                    | 83 0c 10 01                            |
    | or dword [rax + 1 * rbx], 0x01                                    | 83 0c 18 01                            |
    | or dword [rax + 1 * rbp], 0x01                                    | 83 0c 28 01                            |
    | or dword [rax + 1 * rsi], 0x01                                    | 83 0c 30 01                            |
    | or dword [rax + 1 * rdi], 0x01                                    | 83 0c 38 01                            |
    | or dword [rax + 1 * r8], 0x01                                     | 42 83 0c 00 01                         |
    | or dword [rax + 1 * r9], 0x01                                     | 42 83 0c 08 01                         |
    | or dword [rax + 1 * r10], 0x01                                    | 42 83 0c 10 01                         |
    | or dword [rax + 1 * r11], 0x01                                    | 42 83 0c 18 01                         |
    | or dword [rax + 1 * r12], 0x01                                    | 42 83 0c 20 01                         |
    | or dword [rax + 1 * r13], 0x01                                    | 42 83 0c 28 01                         |
    | or dword [rax + 1 * r14], 0x01                                    | 42 83 0c 30 01                         |
    | or dword [rax + 1 * r15], 0x01                                    | 42 83 0c 38 01                         |
    | or dword [rax + 2 * rcx], 0x01                                    | 83 0c 48 01                            |
    | or dword [rax + 4 * rcx], 0x01                                    | 83 0c 88 01                            |
    | or dword [rax + 8 * rcx], 0x01                                    | 83 0c c8 01                            |
    | or dword [r8 + 1 * r9], 0x01                                      | 43 83 0c 08 01                         |
    | or dword [r8 + 2 * r9], 0x01                                      | 43 83 0c 48 01                         |
    | or dword [r8 + 4 * r9], 0x01                                      | 43 83 0c 88 01                         |
    | or dword [r8 + 8 * r9], 0x01                                      | 43 83 0c c8 01                         |
    | or dword [1 * rcx], 0x01                                          | 83 0c 0d 00 00 00 00 01                |
    | or dword [2 * rcx], 0x01                                          | 83 0c 4d 00 00 00 00 01                |
    | or dword [4 * rcx], 0x01                                          | 83 0c 8d 00 00 00 00 01                |
    | or dword [8 * rcx], 0x01                                          | 83 0c cd 00 00 00 00 01                |
    | or dword [1 * r9], 0x01                                           | 42 83 0c 0d 00 00 00 00 01             |
    | or dword [2 * r9], 0x01                                           | 42 83 0c 4d 00 00 00 00 01             |
    | or dword [4 * r9], 0x01                                           | 42 83 0c 8d 00 00 00 00 01             |
    | or dword [8 * r9], 0x01                                           | 42 83 0c cd 00 00 00 00 01             |
    | or dword [r13 + 8 * r12], 0x01                                    | 43 83 4c e5 00 01                      |
    | or dword [rsp + 4 * r15], 0x01                                    | 42 83 0c bc 01                         |
    | or dword [rax + 1 * rcx + 0x00], 0x01                             | 83 4c 08 00 01                         |
    | or dword [rax + 1 * rcx - 0x00], 0x01                             | 83 4c 08 00 01                         |
    | or dword [rax + 1 * rcx + 0x01], 0x01                             | 83 4c 08 01 01                         |
    | or dword [rax + 1 * rcx - 0x01], 0x01                             | 83 4c 08 ff 01                         |
    | or dword [rax + 1 * rcx + 0x00000001], 0x01                       | 83 8c 08 01 00 00 00 01                |
    | or dword [rax + 1 * rcx - 0x00000001], 0x01                       | 83 8c 08 ff ff ff ff 01                |
    | or dword [rax + 1 * rcx + 0x7f], 0x01                             | 83 4c 08 7f 01                         |
    | or dword [rax + 1 * rcx - 0x7f], 0x01                             | 83 4c 08 81 01                         |
    | or dword [rax + 1 * rcx + 0x80], 0x01                             | 83 8c 08 80 00 00 00 01                |
    | or dword [rax + 1 * rcx - 0x80], 0x01                             | 83 4c 08 80 01                         |
    | or dword [rax + 1 * rcx - 0x81], 0x01                             | 83 8c 08 7f ff ff ff 01                |
    | or dword [rax + 1 * rcx + 0xff], 0x01                             | 83 8c 08 ff 00 00 00 01                |
    | or dword [rax + 1 * rcx - 0xff], 0x01                             | 83 8c 08 01 ff ff ff 01                |
    | or dword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 83 8c 08 ff ff ff 7f 01                |
    | or dword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 83 8c 08 01 00 00 80 01                |
    | or dword [rax + 1 * rcx - 0x80000000], 0x01                       | 83 8c 08 00 00 00 80 01                |
    | or dword [r10 + 0x7f], 0x01                                       | 41 83 4a 7f 01                         |
    | or dword [r10 + 0x80], 0x01                                       | 41 83 8a 80 00 00 00 01                |
    | or dword [r10 - 0x80], 0x01                                       | 41 83 4a 80 01                         |
    | or dword [r10 - 0x81], 0x01                                       | 41 83 8a 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; or dword [rel @prev5], 0x01      | 90 90 90 90 90 83 0d f4 ff ff ff 01    |
    | .prev1: nop; or dword [rel @prev1], 0x01                          | 90 83 0d f8 ff ff ff 01                |
    | or dword [rel @next1], 0x01; nop; .next1: nop                     | 83 0d 01 00 00 00 01 90 90             |
    | or dword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 83 0d 05 00 00 00 01 90 90 90 90 90 90 |
    | or dword [rax], 0x00                                              | 83 08 00                               |
    | or dword [rax], 0x7f                                              | 83 08 7f                               |
    | or dword [rax], 0x80                                              | 83 08 80                               |
    | or dword [rax], 0xff                                              | 83 08 ff                               |
    | or dword [rcx], 0x7f                                              | 83 09 7f                               |
    | or dword [rdx], 0x80                                              | 83 0a 80                               |
    | or dword [rbx], 0xff                                              | 83 0b ff                               |
    | or dword [rsp], 0x00                                              | 83 0c 24 00                            |
    | or dword [rsi], 0x7f                                              | 83 0e 7f                               |
    | or dword [rdi], 0x80                                              | 83 0f 80                               |
    | or dword [r8], 0xff                                               | 41 83 08 ff                            |
    | or dword [r9], 0x00                                               | 41 83 09 00                            |
    | or dword [r11], 0x7f                                              | 41 83 0b 7f                            |
    | or dword [r12], 0x80                                              | 41 83 0c 24 80                         |
    | or dword [r13], 0xff                                              | 41 83 4d 00 ff                         |
    | or dword [r14], 0x00                                              | 41 83 0e 00                            |
    | or dword [rax + 1 * rcx], 0x7f                                    | 83 0c 08 7f                            |
    | or dword [rcx + 1 * rcx], 0x80                                    | 83 0c 09 80                            |
    | or dword [rdx + 1 * rcx], 0xff                                    | 83 0c 0a ff                            |
    | or dword [rbx + 1 * rcx], 0x00                                    | 83 0c 0b 00                            |
    | or dword [rbp + 1 * rcx], 0x7f                                    | 83 4c 0d 00 7f                         |
    | or dword [rsi + 1 * rcx], 0x80                                    | 83 0c 0e 80                            |
    | or dword [rdi + 1 * rcx], 0xff                                    | 83 0c 0f ff                            |
    | or dword [r8 + 1 * rcx], 0x00                                     | 41 83 0c 08 00                         |
    | or dword [r10 + 1 * rcx], 0x7f                                    | 41 83 0c 0a 7f                         |
    | or dword [r11 + 1 * rcx], 0x80                                    | 41 83 0c 0b 80                         |
    | or dword [r12 + 1 * rcx], 0xff                                    | 41 83 0c 0c ff                         |
    | or dword [r13 + 1 * rcx], 0x00                                    | 41 83 4c 0d 00 00                      |
    | or dword [r15 + 1 * rcx], 0x7f                                    | 41 83 0c 0f 7f                         |
    | or dword [rax + 1 * rax], 0x80                                    | 83 0c 00 80                            |
    | or dword [rax + 1 * rdx], 0xff                                    | 83 0c 10 ff                            |
    | or dword [rax + 1 * rbx], 0x00                                    | 83 0c 18 00                            |
    | or dword [rax + 1 * rsi], 0x7f                                    | 83 0c 30 7f                            |
    | or dword [rax + 1 * rdi], 0x80                                    | 83 0c 38 80                            |
    | or dword [rax + 1 * r8], 0xff                                     | 42 83 0c 00 ff                         |
    | or dword [rax + 1 * r9], 0x00                                     | 42 83 0c 08 00                         |
    | or dword [rax + 1 * r11], 0x7f                                    | 42 83 0c 18 7f                         |
    | or dword [rax + 1 * r12], 0x80                                    | 42 83 0c 20 80                         |
    | or dword [rax + 1 * r13], 0xff                                    | 42 83 0c 28 ff                         |
    | or dword [rax + 1 * r14], 0x00                                    | 42 83 0c 30 00                         |
    | or dword [rax + 2 * rcx], 0x7f                                    | 83 0c 48 7f                            |
    | or dword [rax + 4 * rcx], 0x80                                    | 83 0c 88 80                            |
    | or dword [rax + 8 * rcx], 0xff                                    | 83 0c c8 ff                            |
    | or dword [r8 + 1 * r9], 0x00                                      | 43 83 0c 08 00                         |
    | or dword [r8 + 4 * r9], 0x7f                                      | 43 83 0c 88 7f                         |
    | or dword [r8 + 8 * r9], 0x80                                      | 43 83 0c c8 80                         |
    | or dword [1 * rcx], 0xff                                          | 83 0c 0d 00 00 00 00 ff                |
    | or dword [2 * rcx], 0x00                                          | 83 0c 4d 00 00 00 00 00                |
    | or dword [8 * rcx], 0x7f                                          | 83 0c cd 00 00 00 00 7f                |
    | or dword [1 * r9], 0x80                                           | 42 83 0c 0d 00 00 00 00 80             |
    | or dword [2 * r9], 0xff                                           | 42 83 0c 4d 00 00 00 00 ff             |
    | or dword [4 * r9], 0x00                                           | 42 83 0c 8d 00 00 00 00 00             |
    | or dword [r13 + 8 * r12], 0x7f                                    | 43 83 4c e5 00 7f                      |
    | or dword [rsp + 4 * r15], 0x80                                    | 42 83 0c bc 80                         |
    | or dword [rax + 1 * rcx + 0x00], 0xff                             | 83 4c 08 00 ff                         |
    | or dword [rax + 1 * rcx - 0x00], 0x00                             | 83 4c 08 00 00                         |
    | or dword [rax + 1 * rcx - 0x01], 0x7f                             | 83 4c 08 ff 7f                         |
    | or dword [rax + 1 * rcx + 0x00000001], 0x80                       | 83 8c 08 01 00 00 00 80                |
    | or dword [rax + 1 * rcx - 0x00000001], 0xff                       | 83 8c 08 ff ff ff ff ff                |
    | or dword [rax + 1 * rcx + 0x7f], 0x00                             | 83 4c 08 7f 00                         |
    | or dword [rax + 1 * rcx + 0x80], 0x7f                             | 83 8c 08 80 00 00 00 7f                |
    | or dword [rax + 1 * rcx - 0x80], 0x80                             | 83 4c 08 80 80                         |
    | or dword [rax + 1 * rcx - 0x81], 0xff                             | 83 8c 08 7f ff ff ff ff                |
    | or dword [rax + 1 * rcx + 0xff], 0x00                             | 83 8c 08 ff 00 00 00 00                |
    | or dword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 83 8c 08 ff ff ff 7f 7f                |
    | or dword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 83 8c 08 01 00 00 80 80                |
    | or dword [rax + 1 * rcx - 0x80000000], 0xff                       | 83 8c 08 00 00 00 80 ff                |
    | or dword [r10 + 0x7f], 0x00                                       | 41 83 4a 7f 00                         |
    | or dword [r10 - 0x80], 0x7f                                       | 41 83 4a 80 7f                         |
    | or dword [r10 - 0x81], 0x80                                       | 41 83 8a 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; or dword [rel @prev5], 0xff      | 90 90 90 90 90 83 0d f4 ff ff ff ff    |
    | .prev1: nop; or dword [rel @prev1], 0x00                          | 90 83 0d f8 ff ff ff 00                |
    | or dword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 83 0d 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_addr32_imm8():
    encode(OR_ADDR32_IMM8)


OR_ADDR32_IMM32 = """
    | ----------------------------------------------------------------------- | ----------------------------------------------- |
    | instruction                                                             | encoding                                        |
    | ----------------------------------------------------------------------- | ----------------------------------------------- |
    | or dword [rax], 0x00000001                                              | 81 08 01 00 00 00                               |
    | or dword [rcx], 0x00000001                                              | 81 09 01 00 00 00                               |
    | or dword [rdx], 0x00000001                                              | 81 0a 01 00 00 00                               |
    | or dword [rbx], 0x00000001                                              | 81 0b 01 00 00 00                               |
    | or dword [rsp], 0x00000001                                              | 81 0c 24 01 00 00 00                            |
    | or dword [rbp], 0x00000001                                              | 81 4d 00 01 00 00 00                            |
    | or dword [rsi], 0x00000001                                              | 81 0e 01 00 00 00                               |
    | or dword [rdi], 0x00000001                                              | 81 0f 01 00 00 00                               |
    | or dword [r8], 0x00000001                                               | 41 81 08 01 00 00 00                            |
    | or dword [r9], 0x00000001                                               | 41 81 09 01 00 00 00                            |
    | or dword [r10], 0x00000001                                              | 41 81 0a 01 00 00 00                            |
    | or dword [r11], 0x00000001                                              | 41 81 0b 01 00 00 00                            |
    | or dword [r12], 0x00000001                                              | 41 81 0c 24 01 00 00 00                         |
    | or dword [r13], 0x00000001                                              | 41 81 4d 00 01 00 00 00                         |
    | or dword [r14], 0x00000001                                              | 41 81 0e 01 00 00 00                            |
    | or dword [r15], 0x00000001                                              | 41 81 0f 01 00 00 00                            |
    | or dword [rax + 1 * rcx], 0x00000001                                    | 81 0c 08 01 00 00 00                            |
    | or dword [rcx + 1 * rcx], 0x00000001                                    | 81 0c 09 01 00 00 00                            |
    | or dword [rdx + 1 * rcx], 0x00000001                                    | 81 0c 0a 01 00 00 00                            |
    | or dword [rbx + 1 * rcx], 0x00000001                                    | 81 0c 0b 01 00 00 00                            |
    | or dword [rsp + 1 * rcx], 0x00000001                                    | 81 0c 0c 01 00 00 00                            |
    | or dword [rbp + 1 * rcx], 0x00000001                                    | 81 4c 0d 00 01 00 00 00                         |
    | or dword [rsi + 1 * rcx], 0x00000001                                    | 81 0c 0e 01 00 00 00                            |
    | or dword [rdi + 1 * rcx], 0x00000001                                    | 81 0c 0f 01 00 00 00                            |
    | or dword [r8 + 1 * rcx], 0x00000001                                     | 41 81 0c 08 01 00 00 00                         |
    | or dword [r9 + 1 * rcx], 0x00000001                                     | 41 81 0c 09 01 00 00 00                         |
    | or dword [r10 + 1 * rcx], 0x00000001                                    | 41 81 0c 0a 01 00 00 00                         |
    | or dword [r11 + 1 * rcx], 0x00000001                                    | 41 81 0c 0b 01 00 00 00                         |
    | or dword [r12 + 1 * rcx], 0x00000001                                    | 41 81 0c 0c 01 00 00 00                         |
    | or dword [r13 + 1 * rcx], 0x00000001                                    | 41 81 4c 0d 00 01 00 00 00                      |
    | or dword [r14 + 1 * rcx], 0x00000001                                    | 41 81 0c 0e 01 00 00 00                         |
    | or dword [r15 + 1 * rcx], 0x00000001                                    | 41 81 0c 0f 01 00 00 00                         |
    | or dword [rax + 1 * rax], 0x00000001                                    | 81 0c 00 01 00 00 00                            |
    | or dword [rax + 1 * rdx], 0x00000001                                    | 81 0c 10 01 00 00 00                            |
    | or dword [rax + 1 * rbx], 0x00000001                                    | 81 0c 18 01 00 00 00                            |
    | or dword [rax + 1 * rbp], 0x00000001                                    | 81 0c 28 01 00 00 00                            |
    | or dword [rax + 1 * rsi], 0x00000001                                    | 81 0c 30 01 00 00 00                            |
    | or dword [rax + 1 * rdi], 0x00000001                                    | 81 0c 38 01 00 00 00                            |
    | or dword [rax + 1 * r8], 0x00000001                                     | 42 81 0c 00 01 00 00 00                         |
    | or dword [rax + 1 * r9], 0x00000001                                     | 42 81 0c 08 01 00 00 00                         |
    | or dword [rax + 1 * r10], 0x00000001                                    | 42 81 0c 10 01 00 00 00                         |
    | or dword [rax + 1 * r11], 0x00000001                                    | 42 81 0c 18 01 00 00 00                         |
    | or dword [rax + 1 * r12], 0x00000001                                    | 42 81 0c 20 01 00 00 00                         |
    | or dword [rax + 1 * r13], 0x00000001                                    | 42 81 0c 28 01 00 00 00                         |
    | or dword [rax + 1 * r14], 0x00000001                                    | 42 81 0c 30 01 00 00 00                         |
    | or dword [rax + 1 * r15], 0x00000001                                    | 42 81 0c 38 01 00 00 00                         |
    | or dword [rax + 2 * rcx], 0x00000001                                    | 81 0c 48 01 00 00 00                            |
    | or dword [rax + 4 * rcx], 0x00000001                                    | 81 0c 88 01 00 00 00                            |
    | or dword [rax + 8 * rcx], 0x00000001                                    | 81 0c c8 01 00 00 00                            |
    | or dword [r8 + 1 * r9], 0x00000001                                      | 43 81 0c 08 01 00 00 00                         |
    | or dword [r8 + 2 * r9], 0x00000001                                      | 43 81 0c 48 01 00 00 00                         |
    | or dword [r8 + 4 * r9], 0x00000001                                      | 43 81 0c 88 01 00 00 00                         |
    | or dword [r8 + 8 * r9], 0x00000001                                      | 43 81 0c c8 01 00 00 00                         |
    | or dword [1 * rcx], 0x00000001                                          | 81 0c 0d 00 00 00 00 01 00 00 00                |
    | or dword [2 * rcx], 0x00000001                                          | 81 0c 4d 00 00 00 00 01 00 00 00                |
    | or dword [4 * rcx], 0x00000001                                          | 81 0c 8d 00 00 00 00 01 00 00 00                |
    | or dword [8 * rcx], 0x00000001                                          | 81 0c cd 00 00 00 00 01 00 00 00                |
    | or dword [1 * r9], 0x00000001                                           | 42 81 0c 0d 00 00 00 00 01 00 00 00             |
    | or dword [2 * r9], 0x00000001                                           | 42 81 0c 4d 00 00 00 00 01 00 00 00             |
    | or dword [4 * r9], 0x00000001                                           | 42 81 0c 8d 00 00 00 00 01 00 00 00             |
    | or dword [8 * r9], 0x00000001                                           | 42 81 0c cd 00 00 00 00 01 00 00 00             |
    | or dword [r13 + 8 * r12], 0x00000001                                    | 43 81 4c e5 00 01 00 00 00                      |
    | or dword [rsp + 4 * r15], 0x00000001                                    | 42 81 0c bc 01 00 00 00                         |
    | or dword [rax + 1 * rcx + 0x00], 0x00000001                             | 81 4c 08 00 01 00 00 00                         |
    | or dword [rax + 1 * rcx - 0x00], 0x00000001                             | 81 4c 08 00 01 00 00 00                         |
    | or dword [rax + 1 * rcx + 0x01], 0x00000001                             | 81 4c 08 01 01 00 00 00                         |
    | or dword [rax + 1 * rcx - 0x01], 0x00000001                             | 81 4c 08 ff 01 00 00 00                         |
    | or dword [rax + 1 * rcx + 0x00000001], 0x00000001                       | 81 8c 08 01 00 00 00 01 00 00 00                |
    | or dword [rax + 1 * rcx - 0x00000001], 0x00000001                       | 81 8c 08 ff ff ff ff 01 00 00 00                |
    | or dword [rax + 1 * rcx + 0x7f], 0x00000001                             | 81 4c 08 7f 01 00 00 00                         |
    | or dword [rax + 1 * rcx - 0x7f], 0x00000001                             | 81 4c 08 81 01 00 00 00                         |
    | or dword [rax + 1 * rcx + 0x80], 0x00000001                             | 81 8c 08 80 00 00 00 01 00 00 00                |
    | or dword [rax + 1 * rcx - 0x80], 0x00000001                             | 81 4c 08 80 01 00 00 00                         |
    | or dword [rax + 1 * rcx - 0x81], 0x00000001                             | 81 8c 08 7f ff ff ff 01 00 00 00                |
    | or dword [rax + 1 * rcx + 0xff], 0x00000001                             | 81 8c 08 ff 00 00 00 01 00 00 00                |
    | or dword [rax + 1 * rcx - 0xff], 0x00000001                             | 81 8c 08 01 ff ff ff 01 00 00 00                |
    | or dword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | 81 8c 08 ff ff ff 7f 01 00 00 00                |
    | or dword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | 81 8c 08 01 00 00 80 01 00 00 00                |
    | or dword [rax + 1 * rcx - 0x80000000], 0x00000001                       | 81 8c 08 00 00 00 80 01 00 00 00                |
    | or dword [r10 + 0x7f], 0x00000001                                       | 41 81 4a 7f 01 00 00 00                         |
    | or dword [r10 + 0x80], 0x00000001                                       | 41 81 8a 80 00 00 00 01 00 00 00                |
    | or dword [r10 - 0x80], 0x00000001                                       | 41 81 4a 80 01 00 00 00                         |
    | or dword [r10 - 0x81], 0x00000001                                       | 41 81 8a 7f ff ff ff 01 00 00 00                |
    | .prev5: nop; nop; nop; nop; nop; or dword [rel @prev5], 0x00000001      | 90 90 90 90 90 81 0d f1 ff ff ff 01 00 00 00    |
    | .prev1: nop; or dword [rel @prev1], 0x00000001                          | 90 81 0d f5 ff ff ff 01 00 00 00                |
    | or dword [rel @next1], 0x00000001; nop; .next1: nop                     | 81 0d 01 00 00 00 01 00 00 00 90 90             |
    | or dword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | 81 0d 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | or dword [rax], 0x00000000                                              | 81 08 00 00 00 00                               |
    | or dword [rax], 0x0000007f                                              | 81 08 7f 00 00 00                               |
    | or dword [rax], 0x00000080                                              | 81 08 80 00 00 00                               |
    | or dword [rax], 0x000000ff                                              | 81 08 ff 00 00 00                               |
    | or dword [rax], 0x00000100                                              | 81 08 00 01 00 00                               |
    | or dword [rax], 0x00007fff                                              | 81 08 ff 7f 00 00                               |
    | or dword [rax], 0x00008000                                              | 81 08 00 80 00 00                               |
    | or dword [rax], 0x0000ffff                                              | 81 08 ff ff 00 00                               |
    | or dword [rax], 0x00010000                                              | 81 08 00 00 01 00                               |
    | or dword [rax], 0x7fffffff                                              | 81 08 ff ff ff 7f                               |
    | or dword [rax], 0x80000000                                              | 81 08 00 00 00 80                               |
    | or dword [rax], 0xffffffff                                              | 81 08 ff ff ff ff                               |
    | or dword [rcx], 0x0000007f                                              | 81 09 7f 00 00 00                               |
    | or dword [rdx], 0x00000080                                              | 81 0a 80 00 00 00                               |
    | or dword [rbx], 0x000000ff                                              | 81 0b ff 00 00 00                               |
    | or dword [rsp], 0x00000100                                              | 81 0c 24 00 01 00 00                            |
    | or dword [rbp], 0x00007fff                                              | 81 4d 00 ff 7f 00 00                            |
    | or dword [rsi], 0x00008000                                              | 81 0e 00 80 00 00                               |
    | or dword [rdi], 0x0000ffff                                              | 81 0f ff ff 00 00                               |
    | or dword [r8], 0x00010000                                               | 41 81 08 00 00 01 00                            |
    | or dword [r9], 0x7fffffff                                               | 41 81 09 ff ff ff 7f                            |
    | or dword [r10], 0x80000000                                              | 41 81 0a 00 00 00 80                            |
    | or dword [r11], 0xffffffff                                              | 41 81 0b ff ff ff ff                            |
    | or dword [r12], 0x00000000                                              | 41 81 0c 24 00 00 00 00                         |
    | or dword [r14], 0x0000007f                                              | 41 81 0e 7f 00 00 00                            |
    | or dword [r15], 0x00000080                                              | 41 81 0f 80 00 00 00                            |
    | or dword [rax + 1 * rcx], 0x000000ff                                    | 81 0c 08 ff 00 00 00                            |
    | or dword [rcx + 1 * rcx], 0x00000100                                    | 81 0c 09 00 01 00 00                            |
    | or dword [rdx + 1 * rcx], 0x00007fff                                    | 81 0c 0a ff 7f 00 00                            |
    | or dword [rbx + 1 * rcx], 0x00008000                                    | 81 0c 0b 00 80 00 00                            |
    | or dword [rsp + 1 * rcx], 0x0000ffff                                    | 81 0c 0c ff ff 00 00                            |
    | or dword [rbp + 1 * rcx], 0x00010000                                    | 81 4c 0d 00 00 00 01 00                         |
    | or dword [rsi + 1 * rcx], 0x7fffffff                                    | 81 0c 0e ff ff ff 7f                            |
    | or dword [rdi + 1 * rcx], 0x80000000                                    | 81 0c 0f 00 00 00 80                            |
    | or dword [r8 + 1 * rcx], 0xffffffff                                     | 41 81 0c 08 ff ff ff ff                         |
    | or dword [r9 + 1 * rcx], 0x00000000                                     | 41 81 0c 09 00 00 00 00                         |
    | or dword [r11 + 1 * rcx], 0x0000007f                                    | 41 81 0c 0b 7f 00 00 00                         |
    | or dword [r12 + 1 * rcx], 0x00000080                                    | 41 81 0c 0c 80 00 00 00                         |
    | or dword [r13 + 1 * rcx], 0x000000ff                                    | 41 81 4c 0d 00 ff 00 00 00                      |
    | or dword [r14 + 1 * rcx], 0x00000100                                    | 41 81 0c 0e 00 01 00 00                         |
    | or dword [r15 + 1 * rcx], 0x00007fff                                    | 41 81 0c 0f ff 7f 00 00                         |
    | or dword [rax + 1 * rax], 0x00008000                                    | 81 0c 00 00 80 00 00                            |
    | or dword [rax + 1 * rdx], 0x0000ffff                                    | 81 0c 10 ff ff 00 00                            |
    | or dword [rax + 1 * rbx], 0x00010000                                    | 81 0c 18 00 00 01 00                            |
    | or dword [rax + 1 * rbp], 0x7fffffff                                    | 81 0c 28 ff ff ff 7f                            |
    | or dword [rax + 1 * rsi], 0x80000000                                    | 81 0c 30 00 00 00 80                            |
    | or dword [rax + 1 * rdi], 0xffffffff                                    | 81 0c 38 ff ff ff ff                            |
    | or dword [rax + 1 * r8], 0x00000000                                     | 42 81 0c 00 00 00 00 00                         |
    | or dword [rax + 1 * r10], 0x0000007f                                    | 42 81 0c 10 7f 00 00 00                         |
    | or dword [rax + 1 * r11], 0x00000080                                    | 42 81 0c 18 80 00 00 00                         |
    | or dword [rax + 1 * r12], 0x000000ff                                    | 42 81 0c 20 ff 00 00 00                         |
    | or dword [rax + 1 * r13], 0x00000100                                    | 42 81 0c 28 00 01 00 00                         |
    | or dword [rax + 1 * r14], 0x00007fff                                    | 42 81 0c 30 ff 7f 00 00                         |
    | or dword [rax + 1 * r15], 0x00008000                                    | 42 81 0c 38 00 80 00 00                         |
    | or dword [rax + 2 * rcx], 0x0000ffff                                    | 81 0c 48 ff ff 00 00                            |
    | or dword [rax + 4 * rcx], 0x00010000                                    | 81 0c 88 00 00 01 00                            |
    | or dword [rax + 8 * rcx], 0x7fffffff                                    | 81 0c c8 ff ff ff 7f                            |
    | or dword [r8 + 1 * r9], 0x80000000                                      | 43 81 0c 08 00 00 00 80                         |
    | or dword [r8 + 2 * r9], 0xffffffff                                      | 43 81 0c 48 ff ff ff ff                         |
    | or dword [r8 + 4 * r9], 0x00000000                                      | 43 81 0c 88 00 00 00 00                         |
    | or dword [1 * rcx], 0x0000007f                                          | 81 0c 0d 00 00 00 00 7f 00 00 00                |
    | or dword [2 * rcx], 0x00000080                                          | 81 0c 4d 00 00 00 00 80 00 00 00                |
    | or dword [4 * rcx], 0x000000ff                                          | 81 0c 8d 00 00 00 00 ff 00 00 00                |
    | or dword [8 * rcx], 0x00000100                                          | 81 0c cd 00 00 00 00 00 01 00 00                |
    | or dword [1 * r9], 0x00007fff                                           | 42 81 0c 0d 00 00 00 00 ff 7f 00 00             |
    | or dword [2 * r9], 0x00008000                                           | 42 81 0c 4d 00 00 00 00 00 80 00 00             |
    | or dword [4 * r9], 0x0000ffff                                           | 42 81 0c 8d 00 00 00 00 ff ff 00 00             |
    | or dword [8 * r9], 0x00010000                                           | 42 81 0c cd 00 00 00 00 00 00 01 00             |
    | or dword [r13 + 8 * r12], 0x7fffffff                                    | 43 81 4c e5 00 ff ff ff 7f                      |
    | or dword [rsp + 4 * r15], 0x80000000                                    | 42 81 0c bc 00 00 00 80                         |
    | or dword [rax + 1 * rcx + 0x00], 0xffffffff                             | 81 4c 08 00 ff ff ff ff                         |
    | or dword [rax + 1 * rcx - 0x00], 0x00000000                             | 81 4c 08 00 00 00 00 00                         |
    | or dword [rax + 1 * rcx - 0x01], 0x0000007f                             | 81 4c 08 ff 7f 00 00 00                         |
    | or dword [rax + 1 * rcx + 0x00000001], 0x00000080                       | 81 8c 08 01 00 00 00 80 00 00 00                |
    | or dword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | 81 8c 08 ff ff ff ff ff 00 00 00                |
    | or dword [rax + 1 * rcx + 0x7f], 0x00000100                             | 81 4c 08 7f 00 01 00 00                         |
    | or dword [rax + 1 * rcx - 0x7f], 0x00007fff                             | 81 4c 08 81 ff 7f 00 00                         |
    | or dword [rax + 1 * rcx + 0x80], 0x00008000                             | 81 8c 08 80 00 00 00 00 80 00 00                |
    | or dword [rax + 1 * rcx - 0x80], 0x0000ffff                             | 81 4c 08 80 ff ff 00 00                         |
    | or dword [rax + 1 * rcx - 0x81], 0x00010000                             | 81 8c 08 7f ff ff ff 00 00 01 00                |
    | or dword [rax + 1 * rcx + 0xff], 0x7fffffff                             | 81 8c 08 ff 00 00 00 ff ff ff 7f                |
    | or dword [rax + 1 * rcx - 0xff], 0x80000000                             | 81 8c 08 01 ff ff ff 00 00 00 80                |
    | or dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | 81 8c 08 ff ff ff 7f ff ff ff ff                |
    | or dword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | 81 8c 08 01 00 00 80 00 00 00 00                |
    | or dword [r10 + 0x7f], 0x0000007f                                       | 41 81 4a 7f 7f 00 00 00                         |
    | or dword [r10 + 0x80], 0x00000080                                       | 41 81 8a 80 00 00 00 80 00 00 00                |
    | or dword [r10 - 0x80], 0x000000ff                                       | 41 81 4a 80 ff 00 00 00                         |
    | or dword [r10 - 0x81], 0x00000100                                       | 41 81 8a 7f ff ff ff 00 01 00 00                |
    | .prev5: nop; nop; nop; nop; nop; or dword [rel @prev5], 0x00007fff      | 90 90 90 90 90 81 0d f1 ff ff ff ff 7f 00 00    |
    | .prev1: nop; or dword [rel @prev1], 0x00008000                          | 90 81 0d f5 ff ff ff 00 80 00 00                |
    | or dword [rel @next1], 0x0000ffff; nop; .next1: nop                     | 81 0d 01 00 00 00 ff ff 00 00 90 90             |
    | or dword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | 81 0d 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------------- | ----------------------------------------------- |
"""


def can_encode_or_addr32_imm32():
    encode(OR_ADDR32_IMM32)


OR_ADDR32_REG32 = """
    | ---------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                      | encoding                            |
    | ---------------------------------------------------------------- | ----------------------------------- |
    | or dword [rax], ecx                                              | 09 08                               |
    | or dword [rcx], ecx                                              | 09 09                               |
    | or dword [rdx], ecx                                              | 09 0a                               |
    | or dword [rbx], ecx                                              | 09 0b                               |
    | or dword [rsp], ecx                                              | 09 0c 24                            |
    | or dword [rbp], ecx                                              | 09 4d 00                            |
    | or dword [rsi], ecx                                              | 09 0e                               |
    | or dword [rdi], ecx                                              | 09 0f                               |
    | or dword [r8], ecx                                               | 41 09 08                            |
    | or dword [r9], ecx                                               | 41 09 09                            |
    | or dword [r10], ecx                                              | 41 09 0a                            |
    | or dword [r11], ecx                                              | 41 09 0b                            |
    | or dword [r12], ecx                                              | 41 09 0c 24                         |
    | or dword [r13], ecx                                              | 41 09 4d 00                         |
    | or dword [r14], ecx                                              | 41 09 0e                            |
    | or dword [r15], ecx                                              | 41 09 0f                            |
    | or dword [rax + 1 * rcx], ecx                                    | 09 0c 08                            |
    | or dword [rcx + 1 * rcx], ecx                                    | 09 0c 09                            |
    | or dword [rdx + 1 * rcx], ecx                                    | 09 0c 0a                            |
    | or dword [rbx + 1 * rcx], ecx                                    | 09 0c 0b                            |
    | or dword [rsp + 1 * rcx], ecx                                    | 09 0c 0c                            |
    | or dword [rbp + 1 * rcx], ecx                                    | 09 4c 0d 00                         |
    | or dword [rsi + 1 * rcx], ecx                                    | 09 0c 0e                            |
    | or dword [rdi + 1 * rcx], ecx                                    | 09 0c 0f                            |
    | or dword [r8 + 1 * rcx], ecx                                     | 41 09 0c 08                         |
    | or dword [r9 + 1 * rcx], ecx                                     | 41 09 0c 09                         |
    | or dword [r10 + 1 * rcx], ecx                                    | 41 09 0c 0a                         |
    | or dword [r11 + 1 * rcx], ecx                                    | 41 09 0c 0b                         |
    | or dword [r12 + 1 * rcx], ecx                                    | 41 09 0c 0c                         |
    | or dword [r13 + 1 * rcx], ecx                                    | 41 09 4c 0d 00                      |
    | or dword [r14 + 1 * rcx], ecx                                    | 41 09 0c 0e                         |
    | or dword [r15 + 1 * rcx], ecx                                    | 41 09 0c 0f                         |
    | or dword [rax + 1 * rax], ecx                                    | 09 0c 00                            |
    | or dword [rax + 1 * rdx], ecx                                    | 09 0c 10                            |
    | or dword [rax + 1 * rbx], ecx                                    | 09 0c 18                            |
    | or dword [rax + 1 * rbp], ecx                                    | 09 0c 28                            |
    | or dword [rax + 1 * rsi], ecx                                    | 09 0c 30                            |
    | or dword [rax + 1 * rdi], ecx                                    | 09 0c 38                            |
    | or dword [rax + 1 * r8], ecx                                     | 42 09 0c 00                         |
    | or dword [rax + 1 * r9], ecx                                     | 42 09 0c 08                         |
    | or dword [rax + 1 * r10], ecx                                    | 42 09 0c 10                         |
    | or dword [rax + 1 * r11], ecx                                    | 42 09 0c 18                         |
    | or dword [rax + 1 * r12], ecx                                    | 42 09 0c 20                         |
    | or dword [rax + 1 * r13], ecx                                    | 42 09 0c 28                         |
    | or dword [rax + 1 * r14], ecx                                    | 42 09 0c 30                         |
    | or dword [rax + 1 * r15], ecx                                    | 42 09 0c 38                         |
    | or dword [rax + 2 * rcx], ecx                                    | 09 0c 48                            |
    | or dword [rax + 4 * rcx], ecx                                    | 09 0c 88                            |
    | or dword [rax + 8 * rcx], ecx                                    | 09 0c c8                            |
    | or dword [r8 + 1 * r9], ecx                                      | 43 09 0c 08                         |
    | or dword [r8 + 2 * r9], ecx                                      | 43 09 0c 48                         |
    | or dword [r8 + 4 * r9], ecx                                      | 43 09 0c 88                         |
    | or dword [r8 + 8 * r9], ecx                                      | 43 09 0c c8                         |
    | or dword [1 * rcx], ecx                                          | 09 0c 0d 00 00 00 00                |
    | or dword [2 * rcx], ecx                                          | 09 0c 4d 00 00 00 00                |
    | or dword [4 * rcx], ecx                                          | 09 0c 8d 00 00 00 00                |
    | or dword [8 * rcx], ecx                                          | 09 0c cd 00 00 00 00                |
    | or dword [1 * r9], ecx                                           | 42 09 0c 0d 00 00 00 00             |
    | or dword [2 * r9], ecx                                           | 42 09 0c 4d 00 00 00 00             |
    | or dword [4 * r9], ecx                                           | 42 09 0c 8d 00 00 00 00             |
    | or dword [8 * r9], ecx                                           | 42 09 0c cd 00 00 00 00             |
    | or dword [r13 + 8 * r12], ecx                                    | 43 09 4c e5 00                      |
    | or dword [rsp + 4 * r15], ecx                                    | 42 09 0c bc                         |
    | or dword [rax + 1 * rcx + 0x00], ecx                             | 09 4c 08 00                         |
    | or dword [rax + 1 * rcx - 0x00], ecx                             | 09 4c 08 00                         |
    | or dword [rax + 1 * rcx + 0x01], ecx                             | 09 4c 08 01                         |
    | or dword [rax + 1 * rcx - 0x01], ecx                             | 09 4c 08 ff                         |
    | or dword [rax + 1 * rcx + 0x00000001], ecx                       | 09 8c 08 01 00 00 00                |
    | or dword [rax + 1 * rcx - 0x00000001], ecx                       | 09 8c 08 ff ff ff ff                |
    | or dword [rax + 1 * rcx + 0x7f], ecx                             | 09 4c 08 7f                         |
    | or dword [rax + 1 * rcx - 0x7f], ecx                             | 09 4c 08 81                         |
    | or dword [rax + 1 * rcx + 0x80], ecx                             | 09 8c 08 80 00 00 00                |
    | or dword [rax + 1 * rcx - 0x80], ecx                             | 09 4c 08 80                         |
    | or dword [rax + 1 * rcx - 0x81], ecx                             | 09 8c 08 7f ff ff ff                |
    | or dword [rax + 1 * rcx + 0xff], ecx                             | 09 8c 08 ff 00 00 00                |
    | or dword [rax + 1 * rcx - 0xff], ecx                             | 09 8c 08 01 ff ff ff                |
    | or dword [rax + 1 * rcx + 0x7fffffff], ecx                       | 09 8c 08 ff ff ff 7f                |
    | or dword [rax + 1 * rcx - 0x7fffffff], ecx                       | 09 8c 08 01 00 00 80                |
    | or dword [rax + 1 * rcx - 0x80000000], ecx                       | 09 8c 08 00 00 00 80                |
    | or dword [r10 + 0x7f], ecx                                       | 41 09 4a 7f                         |
    | or dword [r10 + 0x80], ecx                                       | 41 09 8a 80 00 00 00                |
    | or dword [r10 - 0x80], ecx                                       | 41 09 4a 80                         |
    | or dword [r10 - 0x81], ecx                                       | 41 09 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or dword [rel @prev5], ecx      | 90 90 90 90 90 09 0d f5 ff ff ff    |
    | .prev1: nop; or dword [rel @prev1], ecx                          | 90 09 0d f9 ff ff ff                |
    | or dword [rel @next1], ecx; nop; .next1: nop                     | 09 0d 01 00 00 00 90 90             |
    | or dword [rel @next5], ecx; nop; nop; nop; nop; nop; .next5: nop | 09 0d 05 00 00 00 90 90 90 90 90 90 |
    | or dword [rax], eax                                              | 09 00                               |
    | or dword [rax], edx                                              | 09 10                               |
    | or dword [rax], ebx                                              | 09 18                               |
    | or dword [rax], esp                                              | 09 20                               |
    | or dword [rax], ebp                                              | 09 28                               |
    | or dword [rax], esi                                              | 09 30                               |
    | or dword [rax], edi                                              | 09 38                               |
    | or dword [rax], r8d                                              | 44 09 00                            |
    | or dword [rax], r9d                                              | 44 09 08                            |
    | or dword [rax], r10d                                             | 44 09 10                            |
    | or dword [rax], r11d                                             | 44 09 18                            |
    | or dword [rax], r12d                                             | 44 09 20                            |
    | or dword [rax], r13d                                             | 44 09 28                            |
    | or dword [rax], r14d                                             | 44 09 30                            |
    | or dword [rax], r15d                                             | 44 09 38                            |
    | or dword [rcx], edx                                              | 09 11                               |
    | or dword [rdx], ebx                                              | 09 1a                               |
    | or dword [rbx], esp                                              | 09 23                               |
    | or dword [rsp], ebp                                              | 09 2c 24                            |
    | or dword [rbp], esi                                              | 09 75 00                            |
    | or dword [rsi], edi                                              | 09 3e                               |
    | or dword [rdi], r8d                                              | 44 09 07                            |
    | or dword [r8], r9d                                               | 45 09 08                            |
    | or dword [r9], r10d                                              | 45 09 11                            |
    | or dword [r10], r11d                                             | 45 09 1a                            |
    | or dword [r11], r12d                                             | 45 09 23                            |
    | or dword [r12], r13d                                             | 45 09 2c 24                         |
    | or dword [r13], r14d                                             | 45 09 75 00                         |
    | or dword [r14], r15d                                             | 45 09 3e                            |
    | or dword [r15], eax                                              | 41 09 07                            |
    | or dword [rcx + 1 * rcx], edx                                    | 09 14 09                            |
    | or dword [rdx + 1 * rcx], ebx                                    | 09 1c 0a                            |
    | or dword [rbx + 1 * rcx], esp                                    | 09 24 0b                            |
    | or dword [rsp + 1 * rcx], ebp                                    | 09 2c 0c                            |
    | or dword [rbp + 1 * rcx], esi                                    | 09 74 0d 00                         |
    | or dword [rsi + 1 * rcx], edi                                    | 09 3c 0e                            |
    | or dword [rdi + 1 * rcx], r8d                                    | 44 09 04 0f                         |
    | or dword [r8 + 1 * rcx], r9d                                     | 45 09 0c 08                         |
    | or dword [r9 + 1 * rcx], r10d                                    | 45 09 14 09                         |
    | or dword [r10 + 1 * rcx], r11d                                   | 45 09 1c 0a                         |
    | or dword [r11 + 1 * rcx], r12d                                   | 45 09 24 0b                         |
    | or dword [r12 + 1 * rcx], r13d                                   | 45 09 2c 0c                         |
    | or dword [r13 + 1 * rcx], r14d                                   | 45 09 74 0d 00                      |
    | or dword [r14 + 1 * rcx], r15d                                   | 45 09 3c 0e                         |
    | or dword [r15 + 1 * rcx], eax                                    | 41 09 04 0f                         |
    | or dword [rax + 1 * rdx], edx                                    | 09 14 10                            |
    | or dword [rax + 1 * rbx], ebx                                    | 09 1c 18                            |
    | or dword [rax + 1 * rbp], esp                                    | 09 24 28                            |
    | or dword [rax + 1 * rsi], ebp                                    | 09 2c 30                            |
    | or dword [rax + 1 * rdi], esi                                    | 09 34 38                            |
    | or dword [rax + 1 * r8], edi                                     | 42 09 3c 00                         |
    | or dword [rax + 1 * r9], r8d                                     | 46 09 04 08                         |
    | or dword [rax + 1 * r10], r9d                                    | 46 09 0c 10                         |
    | or dword [rax + 1 * r11], r10d                                   | 46 09 14 18                         |
    | or dword [rax + 1 * r12], r11d                                   | 46 09 1c 20                         |
    | or dword [rax + 1 * r13], r12d                                   | 46 09 24 28                         |
    | or dword [rax + 1 * r14], r13d                                   | 46 09 2c 30                         |
    | or dword [rax + 1 * r15], r14d                                   | 46 09 34 38                         |
    | or dword [rax + 2 * rcx], r15d                                   | 44 09 3c 48                         |
    | or dword [rax + 4 * rcx], eax                                    | 09 04 88                            |
    | or dword [r8 + 1 * r9], edx                                      | 43 09 14 08                         |
    | or dword [r8 + 2 * r9], ebx                                      | 43 09 1c 48                         |
    | or dword [r8 + 4 * r9], esp                                      | 43 09 24 88                         |
    | or dword [r8 + 8 * r9], ebp                                      | 43 09 2c c8                         |
    | or dword [1 * rcx], esi                                          | 09 34 0d 00 00 00 00                |
    | or dword [2 * rcx], edi                                          | 09 3c 4d 00 00 00 00                |
    | or dword [4 * rcx], r8d                                          | 44 09 04 8d 00 00 00 00             |
    | or dword [8 * rcx], r9d                                          | 44 09 0c cd 00 00 00 00             |
    | or dword [1 * r9], r10d                                          | 46 09 14 0d 00 00 00 00             |
    | or dword [2 * r9], r11d                                          | 46 09 1c 4d 00 00 00 00             |
    | or dword [4 * r9], r12d                                          | 46 09 24 8d 00 00 00 00             |
    | or dword [8 * r9], r13d                                          | 46 09 2c cd 00 00 00 00             |
    | or dword [r13 + 8 * r12], r14d                                   | 47 09 74 e5 00                      |
    | or dword [rsp + 4 * r15], r15d                                   | 46 09 3c bc                         |
    | or dword [rax + 1 * rcx + 0x00], eax                             | 09 44 08 00                         |
    | or dword [rax + 1 * rcx + 0x01], edx                             | 09 54 08 01                         |
    | or dword [rax + 1 * rcx - 0x01], ebx                             | 09 5c 08 ff                         |
    | or dword [rax + 1 * rcx + 0x00000001], esp                       | 09 a4 08 01 00 00 00                |
    | or dword [rax + 1 * rcx - 0x00000001], ebp                       | 09 ac 08 ff ff ff ff                |
    | or dword [rax + 1 * rcx + 0x7f], esi                             | 09 74 08 7f                         |
    | or dword [rax + 1 * rcx - 0x7f], edi                             | 09 7c 08 81                         |
    | or dword [rax + 1 * rcx + 0x80], r8d                             | 44 09 84 08 80 00 00 00             |
    | or dword [rax + 1 * rcx - 0x80], r9d                             | 44 09 4c 08 80                      |
    | or dword [rax + 1 * rcx - 0x81], r10d                            | 44 09 94 08 7f ff ff ff             |
    | or dword [rax + 1 * rcx + 0xff], r11d                            | 44 09 9c 08 ff 00 00 00             |
    | or dword [rax + 1 * rcx - 0xff], r12d                            | 44 09 a4 08 01 ff ff ff             |
    | or dword [rax + 1 * rcx + 0x7fffffff], r13d                      | 44 09 ac 08 ff ff ff 7f             |
    | or dword [rax + 1 * rcx - 0x7fffffff], r14d                      | 44 09 b4 08 01 00 00 80             |
    | or dword [rax + 1 * rcx - 0x80000000], r15d                      | 44 09 bc 08 00 00 00 80             |
    | or dword [r10 + 0x7f], eax                                       | 41 09 42 7f                         |
    | or dword [r10 - 0x80], edx                                       | 41 09 52 80                         |
    | or dword [r10 - 0x81], ebx                                       | 41 09 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or dword [rel @prev5], esp      | 90 90 90 90 90 09 25 f5 ff ff ff    |
    | .prev1: nop; or dword [rel @prev1], ebp                          | 90 09 2d f9 ff ff ff                |
    | or dword [rel @next1], esi; nop; .next1: nop                     | 09 35 01 00 00 00 90 90             |
    | or dword [rel @next5], edi; nop; nop; nop; nop; nop; .next5: nop | 09 3d 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_or_addr32_reg32():
    encode(OR_ADDR32_REG32)


OR_ADDR16_IMM8 = """
    | ---------------------------------------------------------------- | ----------------------------------------- |
    | instruction                                                      | encoding                                  |
    | ---------------------------------------------------------------- | ----------------------------------------- |
    | or word [rax], 0x01                                              | 66 83 08 01                               |
    | or word [rcx], 0x01                                              | 66 83 09 01                               |
    | or word [rdx], 0x01                                              | 66 83 0a 01                               |
    | or word [rbx], 0x01                                              | 66 83 0b 01                               |
    | or word [rsp], 0x01                                              | 66 83 0c 24 01                            |
    | or word [rbp], 0x01                                              | 66 83 4d 00 01                            |
    | or word [rsi], 0x01                                              | 66 83 0e 01                               |
    | or word [rdi], 0x01                                              | 66 83 0f 01                               |
    | or word [r8], 0x01                                               | 66 41 83 08 01                            |
    | or word [r9], 0x01                                               | 66 41 83 09 01                            |
    | or word [r10], 0x01                                              | 66 41 83 0a 01                            |
    | or word [r11], 0x01                                              | 66 41 83 0b 01                            |
    | or word [r12], 0x01                                              | 66 41 83 0c 24 01                         |
    | or word [r13], 0x01                                              | 66 41 83 4d 00 01                         |
    | or word [r14], 0x01                                              | 66 41 83 0e 01                            |
    | or word [r15], 0x01                                              | 66 41 83 0f 01                            |
    | or word [rax + 1 * rcx], 0x01                                    | 66 83 0c 08 01                            |
    | or word [rcx + 1 * rcx], 0x01                                    | 66 83 0c 09 01                            |
    | or word [rdx + 1 * rcx], 0x01                                    | 66 83 0c 0a 01                            |
    | or word [rbx + 1 * rcx], 0x01                                    | 66 83 0c 0b 01                            |
    | or word [rsp + 1 * rcx], 0x01                                    | 66 83 0c 0c 01                            |
    | or word [rbp + 1 * rcx], 0x01                                    | 66 83 4c 0d 00 01                         |
    | or word [rsi + 1 * rcx], 0x01                                    | 66 83 0c 0e 01                            |
    | or word [rdi + 1 * rcx], 0x01                                    | 66 83 0c 0f 01                            |
    | or word [r8 + 1 * rcx], 0x01                                     | 66 41 83 0c 08 01                         |
    | or word [r9 + 1 * rcx], 0x01                                     | 66 41 83 0c 09 01                         |
    | or word [r10 + 1 * rcx], 0x01                                    | 66 41 83 0c 0a 01                         |
    | or word [r11 + 1 * rcx], 0x01                                    | 66 41 83 0c 0b 01                         |
    | or word [r12 + 1 * rcx], 0x01                                    | 66 41 83 0c 0c 01                         |
    | or word [r13 + 1 * rcx], 0x01                                    | 66 41 83 4c 0d 00 01                      |
    | or word [r14 + 1 * rcx], 0x01                                    | 66 41 83 0c 0e 01                         |
    | or word [r15 + 1 * rcx], 0x01                                    | 66 41 83 0c 0f 01                         |
    | or word [rax + 1 * rax], 0x01                                    | 66 83 0c 00 01                            |
    | or word [rax + 1 * rdx], 0x01                                    | 66 83 0c 10 01                            |
    | or word [rax + 1 * rbx], 0x01                                    | 66 83 0c 18 01                            |
    | or word [rax + 1 * rbp], 0x01                                    | 66 83 0c 28 01                            |
    | or word [rax + 1 * rsi], 0x01                                    | 66 83 0c 30 01                            |
    | or word [rax + 1 * rdi], 0x01                                    | 66 83 0c 38 01                            |
    | or word [rax + 1 * r8], 0x01                                     | 66 42 83 0c 00 01                         |
    | or word [rax + 1 * r9], 0x01                                     | 66 42 83 0c 08 01                         |
    | or word [rax + 1 * r10], 0x01                                    | 66 42 83 0c 10 01                         |
    | or word [rax + 1 * r11], 0x01                                    | 66 42 83 0c 18 01                         |
    | or word [rax + 1 * r12], 0x01                                    | 66 42 83 0c 20 01                         |
    | or word [rax + 1 * r13], 0x01                                    | 66 42 83 0c 28 01                         |
    | or word [rax + 1 * r14], 0x01                                    | 66 42 83 0c 30 01                         |
    | or word [rax + 1 * r15], 0x01                                    | 66 42 83 0c 38 01                         |
    | or word [rax + 2 * rcx], 0x01                                    | 66 83 0c 48 01                            |
    | or word [rax + 4 * rcx], 0x01                                    | 66 83 0c 88 01                            |
    | or word [rax + 8 * rcx], 0x01                                    | 66 83 0c c8 01                            |
    | or word [r8 + 1 * r9], 0x01                                      | 66 43 83 0c 08 01                         |
    | or word [r8 + 2 * r9], 0x01                                      | 66 43 83 0c 48 01                         |
    | or word [r8 + 4 * r9], 0x01                                      | 66 43 83 0c 88 01                         |
    | or word [r8 + 8 * r9], 0x01                                      | 66 43 83 0c c8 01                         |
    | or word [1 * rcx], 0x01                                          | 66 83 0c 0d 00 00 00 00 01                |
    | or word [2 * rcx], 0x01                                          | 66 83 0c 4d 00 00 00 00 01                |
    | or word [4 * rcx], 0x01                                          | 66 83 0c 8d 00 00 00 00 01                |
    | or word [8 * rcx], 0x01                                          | 66 83 0c cd 00 00 00 00 01                |
    | or word [1 * r9], 0x01                                           | 66 42 83 0c 0d 00 00 00 00 01             |
    | or word [2 * r9], 0x01                                           | 66 42 83 0c 4d 00 00 00 00 01             |
    | or word [4 * r9], 0x01                                           | 66 42 83 0c 8d 00 00 00 00 01             |
    | or word [8 * r9], 0x01                                           | 66 42 83 0c cd 00 00 00 00 01             |
    | or word [r13 + 8 * r12], 0x01                                    | 66 43 83 4c e5 00 01                      |
    | or word [rsp + 4 * r15], 0x01                                    | 66 42 83 0c bc 01                         |
    | or word [rax + 1 * rcx + 0x00], 0x01                             | 66 83 4c 08 00 01                         |
    | or word [rax + 1 * rcx - 0x00], 0x01                             | 66 83 4c 08 00 01                         |
    | or word [rax + 1 * rcx + 0x01], 0x01                             | 66 83 4c 08 01 01                         |
    | or word [rax + 1 * rcx - 0x01], 0x01                             | 66 83 4c 08 ff 01                         |
    | or word [rax + 1 * rcx + 0x00000001], 0x01                       | 66 83 8c 08 01 00 00 00 01                |
    | or word [rax + 1 * rcx - 0x00000001], 0x01                       | 66 83 8c 08 ff ff ff ff 01                |
    | or word [rax + 1 * rcx + 0x7f], 0x01                             | 66 83 4c 08 7f 01                         |
    | or word [rax + 1 * rcx - 0x7f], 0x01                             | 66 83 4c 08 81 01                         |
    | or word [rax + 1 * rcx + 0x80], 0x01                             | 66 83 8c 08 80 00 00 00 01                |
    | or word [rax + 1 * rcx - 0x80], 0x01                             | 66 83 4c 08 80 01                         |
    | or word [rax + 1 * rcx - 0x81], 0x01                             | 66 83 8c 08 7f ff ff ff 01                |
    | or word [rax + 1 * rcx + 0xff], 0x01                             | 66 83 8c 08 ff 00 00 00 01                |
    | or word [rax + 1 * rcx - 0xff], 0x01                             | 66 83 8c 08 01 ff ff ff 01                |
    | or word [rax + 1 * rcx + 0x7fffffff], 0x01                       | 66 83 8c 08 ff ff ff 7f 01                |
    | or word [rax + 1 * rcx - 0x7fffffff], 0x01                       | 66 83 8c 08 01 00 00 80 01                |
    | or word [rax + 1 * rcx - 0x80000000], 0x01                       | 66 83 8c 08 00 00 00 80 01                |
    | or word [r10 + 0x7f], 0x01                                       | 66 41 83 4a 7f 01                         |
    | or word [r10 + 0x80], 0x01                                       | 66 41 83 8a 80 00 00 00 01                |
    | or word [r10 - 0x80], 0x01                                       | 66 41 83 4a 80 01                         |
    | or word [r10 - 0x81], 0x01                                       | 66 41 83 8a 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; or word [rel @prev5], 0x01      | 90 90 90 90 90 66 83 0d f3 ff ff ff 01    |
    | .prev1: nop; or word [rel @prev1], 0x01                          | 90 66 83 0d f7 ff ff ff 01                |
    | or word [rel @next1], 0x01; nop; .next1: nop                     | 66 83 0d 01 00 00 00 01 90 90             |
    | or word [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 66 83 0d 05 00 00 00 01 90 90 90 90 90 90 |
    | or word [rax], 0x00                                              | 66 83 08 00                               |
    | or word [rax], 0x7f                                              | 66 83 08 7f                               |
    | or word [rax], 0x80                                              | 66 83 08 80                               |
    | or word [rax], 0xff                                              | 66 83 08 ff                               |
    | or word [rcx], 0x7f                                              | 66 83 09 7f                               |
    | or word [rdx], 0x80                                              | 66 83 0a 80                               |
    | or word [rbx], 0xff                                              | 66 83 0b ff                               |
    | or word [rsp], 0x00                                              | 66 83 0c 24 00                            |
    | or word [rsi], 0x7f                                              | 66 83 0e 7f                               |
    | or word [rdi], 0x80                                              | 66 83 0f 80                               |
    | or word [r8], 0xff                                               | 66 41 83 08 ff                            |
    | or word [r9], 0x00                                               | 66 41 83 09 00                            |
    | or word [r11], 0x7f                                              | 66 41 83 0b 7f                            |
    | or word [r12], 0x80                                              | 66 41 83 0c 24 80                         |
    | or word [r13], 0xff                                              | 66 41 83 4d 00 ff                         |
    | or word [r14], 0x00                                              | 66 41 83 0e 00                            |
    | or word [rax + 1 * rcx], 0x7f                                    | 66 83 0c 08 7f                            |
    | or word [rcx + 1 * rcx], 0x80                                    | 66 83 0c 09 80                            |
    | or word [rdx + 1 * rcx], 0xff                                    | 66 83 0c 0a ff                            |
    | or word [rbx + 1 * rcx], 0x00                                    | 66 83 0c 0b 00                            |
    | or word [rbp + 1 * rcx], 0x7f                                    | 66 83 4c 0d 00 7f                         |
    | or word [rsi + 1 * rcx], 0x80                                    | 66 83 0c 0e 80                            |
    | or word [rdi + 1 * rcx], 0xff                                    | 66 83 0c 0f ff                            |
    | or word [r8 + 1 * rcx], 0x00                                     | 66 41 83 0c 08 00                         |
    | or word [r10 + 1 * rcx], 0x7f                                    | 66 41 83 0c 0a 7f                         |
    | or word [r11 + 1 * rcx], 0x80                                    | 66 41 83 0c 0b 80                         |
    | or word [r12 + 1 * rcx], 0xff                                    | 66 41 83 0c 0c ff                         |
    | or word [r13 + 1 * rcx], 0x00                                    | 66 41 83 4c 0d 00 00                      |
    | or word [r15 + 1 * rcx], 0x7f                                    | 66 41 83 0c 0f 7f                         |
    | or word [rax + 1 * rax], 0x80                                    | 66 83 0c 00 80                            |
    | or word [rax + 1 * rdx], 0xff                                    | 66 83 0c 10 ff                            |
    | or word [rax + 1 * rbx], 0x00                                    | 66 83 0c 18 00                            |
    | or word [rax + 1 * rsi], 0x7f                                    | 66 83 0c 30 7f                            |
    | or word [rax + 1 * rdi], 0x80                                    | 66 83 0c 38 80                            |
    | or word [rax + 1 * r8], 0xff                                     | 66 42 83 0c 00 ff                         |
    | or word [rax + 1 * r9], 0x00                                     | 66 42 83 0c 08 00                         |
    | or word [rax + 1 * r11], 0x7f                                    | 66 42 83 0c 18 7f                         |
    | or word [rax + 1 * r12], 0x80                                    | 66 42 83 0c 20 80                         |
    | or word [rax + 1 * r13], 0xff                                    | 66 42 83 0c 28 ff                         |
    | or word [rax + 1 * r14], 0x00                                    | 66 42 83 0c 30 00                         |
    | or word [rax + 2 * rcx], 0x7f                                    | 66 83 0c 48 7f                            |
    | or word [rax + 4 * rcx], 0x80                                    | 66 83 0c 88 80                            |
    | or word [rax + 8 * rcx], 0xff                                    | 66 83 0c c8 ff                            |
    | or word [r8 + 1 * r9], 0x00                                      | 66 43 83 0c 08 00                         |
    | or word [r8 + 4 * r9], 0x7f                                      | 66 43 83 0c 88 7f                         |
    | or word [r8 + 8 * r9], 0x80                                      | 66 43 83 0c c8 80                         |
    | or word [1 * rcx], 0xff                                          | 66 83 0c 0d 00 00 00 00 ff                |
    | or word [2 * rcx], 0x00                                          | 66 83 0c 4d 00 00 00 00 00                |
    | or word [8 * rcx], 0x7f                                          | 66 83 0c cd 00 00 00 00 7f                |
    | or word [1 * r9], 0x80                                           | 66 42 83 0c 0d 00 00 00 00 80             |
    | or word [2 * r9], 0xff                                           | 66 42 83 0c 4d 00 00 00 00 ff             |
    | or word [4 * r9], 0x00                                           | 66 42 83 0c 8d 00 00 00 00 00             |
    | or word [r13 + 8 * r12], 0x7f                                    | 66 43 83 4c e5 00 7f                      |
    | or word [rsp + 4 * r15], 0x80                                    | 66 42 83 0c bc 80                         |
    | or word [rax + 1 * rcx + 0x00], 0xff                             | 66 83 4c 08 00 ff                         |
    | or word [rax + 1 * rcx - 0x00], 0x00                             | 66 83 4c 08 00 00                         |
    | or word [rax + 1 * rcx - 0x01], 0x7f                             | 66 83 4c 08 ff 7f                         |
    | or word [rax + 1 * rcx + 0x00000001], 0x80                       | 66 83 8c 08 01 00 00 00 80                |
    | or word [rax + 1 * rcx - 0x00000001], 0xff                       | 66 83 8c 08 ff ff ff ff ff                |
    | or word [rax + 1 * rcx + 0x7f], 0x00                             | 66 83 4c 08 7f 00                         |
    | or word [rax + 1 * rcx + 0x80], 0x7f                             | 66 83 8c 08 80 00 00 00 7f                |
    | or word [rax + 1 * rcx - 0x80], 0x80                             | 66 83 4c 08 80 80                         |
    | or word [rax + 1 * rcx - 0x81], 0xff                             | 66 83 8c 08 7f ff ff ff ff                |
    | or word [rax + 1 * rcx + 0xff], 0x00                             | 66 83 8c 08 ff 00 00 00 00                |
    | or word [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 66 83 8c 08 ff ff ff 7f 7f                |
    | or word [rax + 1 * rcx - 0x7fffffff], 0x80                       | 66 83 8c 08 01 00 00 80 80                |
    | or word [rax + 1 * rcx - 0x80000000], 0xff                       | 66 83 8c 08 00 00 00 80 ff                |
    | or word [r10 + 0x7f], 0x00                                       | 66 41 83 4a 7f 00                         |
    | or word [r10 - 0x80], 0x7f                                       | 66 41 83 4a 80 7f                         |
    | or word [r10 - 0x81], 0x80                                       | 66 41 83 8a 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; or word [rel @prev5], 0xff      | 90 90 90 90 90 66 83 0d f3 ff ff ff ff    |
    | .prev1: nop; or word [rel @prev1], 0x00                          | 90 66 83 0d f7 ff ff ff 00                |
    | or word [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 66 83 0d 05 00 00 00 7f 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | ----------------------------------------- |
"""


def can_encode_or_addr16_imm8():
    encode(OR_ADDR16_IMM8)


OR_ADDR16_IMM16 = """
    | ------------------------------------------------------------------ | -------------------------------------------- |
    | instruction                                                        | encoding                                     |
    | ------------------------------------------------------------------ | -------------------------------------------- |
    | or word [rax], 0x0001                                              | 66 81 08 01 00                               |
    | or word [rcx], 0x0001                                              | 66 81 09 01 00                               |
    | or word [rdx], 0x0001                                              | 66 81 0a 01 00                               |
    | or word [rbx], 0x0001                                              | 66 81 0b 01 00                               |
    | or word [rsp], 0x0001                                              | 66 81 0c 24 01 00                            |
    | or word [rbp], 0x0001                                              | 66 81 4d 00 01 00                            |
    | or word [rsi], 0x0001                                              | 66 81 0e 01 00                               |
    | or word [rdi], 0x0001                                              | 66 81 0f 01 00                               |
    | or word [r8], 0x0001                                               | 66 41 81 08 01 00                            |
    | or word [r9], 0x0001                                               | 66 41 81 09 01 00                            |
    | or word [r10], 0x0001                                              | 66 41 81 0a 01 00                            |
    | or word [r11], 0x0001                                              | 66 41 81 0b 01 00                            |
    | or word [r12], 0x0001                                              | 66 41 81 0c 24 01 00                         |
    | or word [r13], 0x0001                                              | 66 41 81 4d 00 01 00                         |
    | or word [r14], 0x0001                                              | 66 41 81 0e 01 00                            |
    | or word [r15], 0x0001                                              | 66 41 81 0f 01 00                            |
    | or word [rax + 1 * rcx], 0x0001                                    | 66 81 0c 08 01 00                            |
    | or word [rcx + 1 * rcx], 0x0001                                    | 66 81 0c 09 01 00                            |
    | or word [rdx + 1 * rcx], 0x0001                                    | 66 81 0c 0a 01 00                            |
    | or word [rbx + 1 * rcx], 0x0001                                    | 66 81 0c 0b 01 00                            |
    | or word [rsp + 1 * rcx], 0x0001                                    | 66 81 0c 0c 01 00                            |
    | or word [rbp + 1 * rcx], 0x0001                                    | 66 81 4c 0d 00 01 00                         |
    | or word [rsi + 1 * rcx], 0x0001                                    | 66 81 0c 0e 01 00                            |
    | or word [rdi + 1 * rcx], 0x0001                                    | 66 81 0c 0f 01 00                            |
    | or word [r8 + 1 * rcx], 0x0001                                     | 66 41 81 0c 08 01 00                         |
    | or word [r9 + 1 * rcx], 0x0001                                     | 66 41 81 0c 09 01 00                         |
    | or word [r10 + 1 * rcx], 0x0001                                    | 66 41 81 0c 0a 01 00                         |
    | or word [r11 + 1 * rcx], 0x0001                                    | 66 41 81 0c 0b 01 00                         |
    | or word [r12 + 1 * rcx], 0x0001                                    | 66 41 81 0c 0c 01 00                         |
    | or word [r13 + 1 * rcx], 0x0001                                    | 66 41 81 4c 0d 00 01 00                      |
    | or word [r14 + 1 * rcx], 0x0001                                    | 66 41 81 0c 0e 01 00                         |
    | or word [r15 + 1 * rcx], 0x0001                                    | 66 41 81 0c 0f 01 00                         |
    | or word [rax + 1 * rax], 0x0001                                    | 66 81 0c 00 01 00                            |
    | or word [rax + 1 * rdx], 0x0001                                    | 66 81 0c 10 01 00                            |
    | or word [rax + 1 * rbx], 0x0001                                    | 66 81 0c 18 01 00                            |
    | or word [rax + 1 * rbp], 0x0001                                    | 66 81 0c 28 01 00                            |
    | or word [rax + 1 * rsi], 0x0001                                    | 66 81 0c 30 01 00                            |
    | or word [rax + 1 * rdi], 0x0001                                    | 66 81 0c 38 01 00                            |
    | or word [rax + 1 * r8], 0x0001                                     | 66 42 81 0c 00 01 00                         |
    | or word [rax + 1 * r9], 0x0001                                     | 66 42 81 0c 08 01 00                         |
    | or word [rax + 1 * r10], 0x0001                                    | 66 42 81 0c 10 01 00                         |
    | or word [rax + 1 * r11], 0x0001                                    | 66 42 81 0c 18 01 00                         |
    | or word [rax + 1 * r12], 0x0001                                    | 66 42 81 0c 20 01 00                         |
    | or word [rax + 1 * r13], 0x0001                                    | 66 42 81 0c 28 01 00                         |
    | or word [rax + 1 * r14], 0x0001                                    | 66 42 81 0c 30 01 00                         |
    | or word [rax + 1 * r15], 0x0001                                    | 66 42 81 0c 38 01 00                         |
    | or word [rax + 2 * rcx], 0x0001                                    | 66 81 0c 48 01 00                            |
    | or word [rax + 4 * rcx], 0x0001                                    | 66 81 0c 88 01 00                            |
    | or word [rax + 8 * rcx], 0x0001                                    | 66 81 0c c8 01 00                            |
    | or word [r8 + 1 * r9], 0x0001                                      | 66 43 81 0c 08 01 00                         |
    | or word [r8 + 2 * r9], 0x0001                                      | 66 43 81 0c 48 01 00                         |
    | or word [r8 + 4 * r9], 0x0001                                      | 66 43 81 0c 88 01 00                         |
    | or word [r8 + 8 * r9], 0x0001                                      | 66 43 81 0c c8 01 00                         |
    | or word [1 * rcx], 0x0001                                          | 66 81 0c 0d 00 00 00 00 01 00                |
    | or word [2 * rcx], 0x0001                                          | 66 81 0c 4d 00 00 00 00 01 00                |
    | or word [4 * rcx], 0x0001                                          | 66 81 0c 8d 00 00 00 00 01 00                |
    | or word [8 * rcx], 0x0001                                          | 66 81 0c cd 00 00 00 00 01 00                |
    | or word [1 * r9], 0x0001                                           | 66 42 81 0c 0d 00 00 00 00 01 00             |
    | or word [2 * r9], 0x0001                                           | 66 42 81 0c 4d 00 00 00 00 01 00             |
    | or word [4 * r9], 0x0001                                           | 66 42 81 0c 8d 00 00 00 00 01 00             |
    | or word [8 * r9], 0x0001                                           | 66 42 81 0c cd 00 00 00 00 01 00             |
    | or word [r13 + 8 * r12], 0x0001                                    | 66 43 81 4c e5 00 01 00                      |
    | or word [rsp + 4 * r15], 0x0001                                    | 66 42 81 0c bc 01 00                         |
    | or word [rax + 1 * rcx + 0x00], 0x0001                             | 66 81 4c 08 00 01 00                         |
    | or word [rax + 1 * rcx - 0x00], 0x0001                             | 66 81 4c 08 00 01 00                         |
    | or word [rax + 1 * rcx + 0x01], 0x0001                             | 66 81 4c 08 01 01 00                         |
    | or word [rax + 1 * rcx - 0x01], 0x0001                             | 66 81 4c 08 ff 01 00                         |
    | or word [rax + 1 * rcx + 0x00000001], 0x0001                       | 66 81 8c 08 01 00 00 00 01 00                |
    | or word [rax + 1 * rcx - 0x00000001], 0x0001                       | 66 81 8c 08 ff ff ff ff 01 00                |
    | or word [rax + 1 * rcx + 0x7f], 0x0001                             | 66 81 4c 08 7f 01 00                         |
    | or word [rax + 1 * rcx - 0x7f], 0x0001                             | 66 81 4c 08 81 01 00                         |
    | or word [rax + 1 * rcx + 0x80], 0x0001                             | 66 81 8c 08 80 00 00 00 01 00                |
    | or word [rax + 1 * rcx - 0x80], 0x0001                             | 66 81 4c 08 80 01 00                         |
    | or word [rax + 1 * rcx - 0x81], 0x0001                             | 66 81 8c 08 7f ff ff ff 01 00                |
    | or word [rax + 1 * rcx + 0xff], 0x0001                             | 66 81 8c 08 ff 00 00 00 01 00                |
    | or word [rax + 1 * rcx - 0xff], 0x0001                             | 66 81 8c 08 01 ff ff ff 01 00                |
    | or word [rax + 1 * rcx + 0x7fffffff], 0x0001                       | 66 81 8c 08 ff ff ff 7f 01 00                |
    | or word [rax + 1 * rcx - 0x7fffffff], 0x0001                       | 66 81 8c 08 01 00 00 80 01 00                |
    | or word [rax + 1 * rcx - 0x80000000], 0x0001                       | 66 81 8c 08 00 00 00 80 01 00                |
    | or word [r10 + 0x7f], 0x0001                                       | 66 41 81 4a 7f 01 00                         |
    | or word [r10 + 0x80], 0x0001                                       | 66 41 81 8a 80 00 00 00 01 00                |
    | or word [r10 - 0x80], 0x0001                                       | 66 41 81 4a 80 01 00                         |
    | or word [r10 - 0x81], 0x0001                                       | 66 41 81 8a 7f ff ff ff 01 00                |
    | .prev5: nop; nop; nop; nop; nop; or word [rel @prev5], 0x0001      | 90 90 90 90 90 66 81 0d f2 ff ff ff 01 00    |
    | .prev1: nop; or word [rel @prev1], 0x0001                          | 90 66 81 0d f6 ff ff ff 01 00                |
    | or word [rel @next1], 0x0001; nop; .next1: nop                     | 66 81 0d 01 00 00 00 01 00 90 90             |
    | or word [rel @next5], 0x0001; nop; nop; nop; nop; nop; .next5: nop | 66 81 0d 05 00 00 00 01 00 90 90 90 90 90 90 |
    | or word [rax], 0x0000                                              | 66 81 08 00 00                               |
    | or word [rax], 0x007f                                              | 66 81 08 7f 00                               |
    | or word [rax], 0x0080                                              | 66 81 08 80 00                               |
    | or word [rax], 0x00ff                                              | 66 81 08 ff 00                               |
    | or word [rax], 0x0100                                              | 66 81 08 00 01                               |
    | or word [rax], 0x7fff                                              | 66 81 08 ff 7f                               |
    | or word [rax], 0x8000                                              | 66 81 08 00 80                               |
    | or word [rax], 0xffff                                              | 66 81 08 ff ff                               |
    | or word [rcx], 0x007f                                              | 66 81 09 7f 00                               |
    | or word [rdx], 0x0080                                              | 66 81 0a 80 00                               |
    | or word [rbx], 0x00ff                                              | 66 81 0b ff 00                               |
    | or word [rsp], 0x0100                                              | 66 81 0c 24 00 01                            |
    | or word [rbp], 0x7fff                                              | 66 81 4d 00 ff 7f                            |
    | or word [rsi], 0x8000                                              | 66 81 0e 00 80                               |
    | or word [rdi], 0xffff                                              | 66 81 0f ff ff                               |
    | or word [r8], 0x0000                                               | 66 41 81 08 00 00                            |
    | or word [r10], 0x007f                                              | 66 41 81 0a 7f 00                            |
    | or word [r11], 0x0080                                              | 66 41 81 0b 80 00                            |
    | or word [r12], 0x00ff                                              | 66 41 81 0c 24 ff 00                         |
    | or word [r13], 0x0100                                              | 66 41 81 4d 00 00 01                         |
    | or word [r14], 0x7fff                                              | 66 41 81 0e ff 7f                            |
    | or word [r15], 0x8000                                              | 66 41 81 0f 00 80                            |
    | or word [rax + 1 * rcx], 0xffff                                    | 66 81 0c 08 ff ff                            |
    | or word [rcx + 1 * rcx], 0x0000                                    | 66 81 0c 09 00 00                            |
    | or word [rbx + 1 * rcx], 0x007f                                    | 66 81 0c 0b 7f 00                            |
    | or word [rsp + 1 * rcx], 0x0080                                    | 66 81 0c 0c 80 00                            |
    | or word [rbp + 1 * rcx], 0x00ff                                    | 66 81 4c 0d 00 ff 00                         |
    | or word [rsi + 1 * rcx], 0x0100                                    | 66 81 0c 0e 00 01                            |
    | or word [rdi + 1 * rcx], 0x7fff                                    | 66 81 0c 0f ff 7f                            |
    | or word [r8 + 1 * rcx], 0x8000                                     | 66 41 81 0c 08 00 80                         |
    | or word [r9 + 1 * rcx], 0xffff                                     | 66 41 81 0c 09 ff ff                         |
    | or word [r10 + 1 * rcx], 0x0000                                    | 66 41 81 0c 0a 00 00                         |
    | or word [r12 + 1 * rcx], 0x007f                                    | 66 41 81 0c 0c 7f 00                         |
    | or word [r13 + 1 * rcx], 0x0080                                    | 66 41 81 4c 0d 00 80 00                      |
    | or word [r14 + 1 * rcx], 0x00ff                                    | 66 41 81 0c 0e ff 00                         |
    | or word [r15 + 1 * rcx], 0x0100                                    | 66 41 81 0c 0f 00 01                         |
    | or word [rax + 1 * rax], 0x7fff                                    | 66 81 0c 00 ff 7f                            |
    | or word [rax + 1 * rdx], 0x8000                                    | 66 81 0c 10 00 80                            |
    | or word [rax + 1 * rbx], 0xffff                                    | 66 81 0c 18 ff ff                            |
    | or word [rax + 1 * rbp], 0x0000                                    | 66 81 0c 28 00 00                            |
    | or word [rax + 1 * rdi], 0x007f                                    | 66 81 0c 38 7f 00                            |
    | or word [rax + 1 * r8], 0x0080                                     | 66 42 81 0c 00 80 00                         |
    | or word [rax + 1 * r9], 0x00ff                                     | 66 42 81 0c 08 ff 00                         |
    | or word [rax + 1 * r10], 0x0100                                    | 66 42 81 0c 10 00 01                         |
    | or word [rax + 1 * r11], 0x7fff                                    | 66 42 81 0c 18 ff 7f                         |
    | or word [rax + 1 * r12], 0x8000                                    | 66 42 81 0c 20 00 80                         |
    | or word [rax + 1 * r13], 0xffff                                    | 66 42 81 0c 28 ff ff                         |
    | or word [rax + 1 * r14], 0x0000                                    | 66 42 81 0c 30 00 00                         |
    | or word [rax + 2 * rcx], 0x007f                                    | 66 81 0c 48 7f 00                            |
    | or word [rax + 4 * rcx], 0x0080                                    | 66 81 0c 88 80 00                            |
    | or word [rax + 8 * rcx], 0x00ff                                    | 66 81 0c c8 ff 00                            |
    | or word [r8 + 1 * r9], 0x0100                                      | 66 43 81 0c 08 00 01                         |
    | or word [r8 + 2 * r9], 0x7fff                                      | 66 43 81 0c 48 ff 7f                         |
    | or word [r8 + 4 * r9], 0x8000                                      | 66 43 81 0c 88 00 80                         |
    | or word [r8 + 8 * r9], 0xffff                                      | 66 43 81 0c c8 ff ff                         |
    | or word [1 * rcx], 0x0000                                          | 66 81 0c 0d 00 00 00 00 00 00                |
    | or word [4 * rcx], 0x007f                                          | 66 81 0c 8d 00 00 00 00 7f 00                |
    | or word [8 * rcx], 0x0080                                          | 66 81 0c cd 00 00 00 00 80 00                |
    | or word [1 * r9], 0x00ff                                           | 66 42 81 0c 0d 00 00 00 00 ff 00             |
    | or word [2 * r9], 0x0100                                           | 66 42 81 0c 4d 00 00 00 00 00 01             |
    | or word [4 * r9], 0x7fff                                           | 66 42 81 0c 8d 00 00 00 00 ff 7f             |
    | or word [8 * r9], 0x8000                                           | 66 42 81 0c cd 00 00 00 00 00 80             |
    | or word [r13 + 8 * r12], 0xffff                                    | 66 43 81 4c e5 00 ff ff                      |
    | or word [rsp + 4 * r15], 0x0000                                    | 66 42 81 0c bc 00 00                         |
    | or word [rax + 1 * rcx - 0x00], 0x007f                             | 66 81 4c 08 00 7f 00                         |
    | or word [rax + 1 * rcx + 0x01], 0x0080                             | 66 81 4c 08 01 80 00                         |
    | or word [rax + 1 * rcx - 0x01], 0x00ff                             | 66 81 4c 08 ff ff 00                         |
    | or word [rax + 1 * rcx + 0x00000001], 0x0100                       | 66 81 8c 08 01 00 00 00 00 01                |
    | or word [rax + 1 * rcx - 0x00000001], 0x7fff                       | 66 81 8c 08 ff ff ff ff ff 7f                |
    | or word [rax + 1 * rcx + 0x7f], 0x8000                             | 66 81 4c 08 7f 00 80                         |
    | or word [rax + 1 * rcx - 0x7f], 0xffff                             | 66 81 4c 08 81 ff ff                         |
    | or word [rax + 1 * rcx + 0x80], 0x0000                             | 66 81 8c 08 80 00 00 00 00 00                |
    | or word [rax + 1 * rcx - 0x81], 0x007f                             | 66 81 8c 08 7f ff ff ff 7f 00                |
    | or word [rax + 1 * rcx + 0xff], 0x0080                             | 66 81 8c 08 ff 00 00 00 80 00                |
    | or word [rax + 1 * rcx - 0xff], 0x00ff                             | 66 81 8c 08 01 ff ff ff ff 00                |
    | or word [rax + 1 * rcx + 0x7fffffff], 0x0100                       | 66 81 8c 08 ff ff ff 7f 00 01                |
    | or word [rax + 1 * rcx - 0x7fffffff], 0x7fff                       | 66 81 8c 08 01 00 00 80 ff 7f                |
    | or word [rax + 1 * rcx - 0x80000000], 0x8000                       | 66 81 8c 08 00 00 00 80 00 80                |
    | or word [r10 + 0x7f], 0xffff                                       | 66 41 81 4a 7f ff ff                         |
    | or word [r10 + 0x80], 0x0000                                       | 66 41 81 8a 80 00 00 00 00 00                |
    | or word [r10 - 0x81], 0x007f                                       | 66 41 81 8a 7f ff ff ff 7f 00                |
    | .prev5: nop; nop; nop; nop; nop; or word [rel @prev5], 0x0080      | 90 90 90 90 90 66 81 0d f2 ff ff ff 80 00    |
    | .prev1: nop; or word [rel @prev1], 0x00ff                          | 90 66 81 0d f6 ff ff ff ff 00                |
    | or word [rel @next1], 0x0100; nop; .next1: nop                     | 66 81 0d 01 00 00 00 00 01 90 90             |
    | or word [rel @next5], 0x7fff; nop; nop; nop; nop; nop; .next5: nop | 66 81 0d 05 00 00 00 ff 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | -------------------------------------------- |
"""


def can_encode_or_addr16_imm16():
    encode(OR_ADDR16_IMM16)


OR_ADDR16_REG16 = """
    | -------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                    | encoding                               |
    | -------------------------------------------------------------- | -------------------------------------- |
    | or word [rax], cx                                              | 66 09 08                               |
    | or word [rcx], cx                                              | 66 09 09                               |
    | or word [rdx], cx                                              | 66 09 0a                               |
    | or word [rbx], cx                                              | 66 09 0b                               |
    | or word [rsp], cx                                              | 66 09 0c 24                            |
    | or word [rbp], cx                                              | 66 09 4d 00                            |
    | or word [rsi], cx                                              | 66 09 0e                               |
    | or word [rdi], cx                                              | 66 09 0f                               |
    | or word [r8], cx                                               | 66 41 09 08                            |
    | or word [r9], cx                                               | 66 41 09 09                            |
    | or word [r10], cx                                              | 66 41 09 0a                            |
    | or word [r11], cx                                              | 66 41 09 0b                            |
    | or word [r12], cx                                              | 66 41 09 0c 24                         |
    | or word [r13], cx                                              | 66 41 09 4d 00                         |
    | or word [r14], cx                                              | 66 41 09 0e                            |
    | or word [r15], cx                                              | 66 41 09 0f                            |
    | or word [rax + 1 * rcx], cx                                    | 66 09 0c 08                            |
    | or word [rcx + 1 * rcx], cx                                    | 66 09 0c 09                            |
    | or word [rdx + 1 * rcx], cx                                    | 66 09 0c 0a                            |
    | or word [rbx + 1 * rcx], cx                                    | 66 09 0c 0b                            |
    | or word [rsp + 1 * rcx], cx                                    | 66 09 0c 0c                            |
    | or word [rbp + 1 * rcx], cx                                    | 66 09 4c 0d 00                         |
    | or word [rsi + 1 * rcx], cx                                    | 66 09 0c 0e                            |
    | or word [rdi + 1 * rcx], cx                                    | 66 09 0c 0f                            |
    | or word [r8 + 1 * rcx], cx                                     | 66 41 09 0c 08                         |
    | or word [r9 + 1 * rcx], cx                                     | 66 41 09 0c 09                         |
    | or word [r10 + 1 * rcx], cx                                    | 66 41 09 0c 0a                         |
    | or word [r11 + 1 * rcx], cx                                    | 66 41 09 0c 0b                         |
    | or word [r12 + 1 * rcx], cx                                    | 66 41 09 0c 0c                         |
    | or word [r13 + 1 * rcx], cx                                    | 66 41 09 4c 0d 00                      |
    | or word [r14 + 1 * rcx], cx                                    | 66 41 09 0c 0e                         |
    | or word [r15 + 1 * rcx], cx                                    | 66 41 09 0c 0f                         |
    | or word [rax + 1 * rax], cx                                    | 66 09 0c 00                            |
    | or word [rax + 1 * rdx], cx                                    | 66 09 0c 10                            |
    | or word [rax + 1 * rbx], cx                                    | 66 09 0c 18                            |
    | or word [rax + 1 * rbp], cx                                    | 66 09 0c 28                            |
    | or word [rax + 1 * rsi], cx                                    | 66 09 0c 30                            |
    | or word [rax + 1 * rdi], cx                                    | 66 09 0c 38                            |
    | or word [rax + 1 * r8], cx                                     | 66 42 09 0c 00                         |
    | or word [rax + 1 * r9], cx                                     | 66 42 09 0c 08                         |
    | or word [rax + 1 * r10], cx                                    | 66 42 09 0c 10                         |
    | or word [rax + 1 * r11], cx                                    | 66 42 09 0c 18                         |
    | or word [rax + 1 * r12], cx                                    | 66 42 09 0c 20                         |
    | or word [rax + 1 * r13], cx                                    | 66 42 09 0c 28                         |
    | or word [rax + 1 * r14], cx                                    | 66 42 09 0c 30                         |
    | or word [rax + 1 * r15], cx                                    | 66 42 09 0c 38                         |
    | or word [rax + 2 * rcx], cx                                    | 66 09 0c 48                            |
    | or word [rax + 4 * rcx], cx                                    | 66 09 0c 88                            |
    | or word [rax + 8 * rcx], cx                                    | 66 09 0c c8                            |
    | or word [r8 + 1 * r9], cx                                      | 66 43 09 0c 08                         |
    | or word [r8 + 2 * r9], cx                                      | 66 43 09 0c 48                         |
    | or word [r8 + 4 * r9], cx                                      | 66 43 09 0c 88                         |
    | or word [r8 + 8 * r9], cx                                      | 66 43 09 0c c8                         |
    | or word [1 * rcx], cx                                          | 66 09 0c 0d 00 00 00 00                |
    | or word [2 * rcx], cx                                          | 66 09 0c 4d 00 00 00 00                |
    | or word [4 * rcx], cx                                          | 66 09 0c 8d 00 00 00 00                |
    | or word [8 * rcx], cx                                          | 66 09 0c cd 00 00 00 00                |
    | or word [1 * r9], cx                                           | 66 42 09 0c 0d 00 00 00 00             |
    | or word [2 * r9], cx                                           | 66 42 09 0c 4d 00 00 00 00             |
    | or word [4 * r9], cx                                           | 66 42 09 0c 8d 00 00 00 00             |
    | or word [8 * r9], cx                                           | 66 42 09 0c cd 00 00 00 00             |
    | or word [r13 + 8 * r12], cx                                    | 66 43 09 4c e5 00                      |
    | or word [rsp + 4 * r15], cx                                    | 66 42 09 0c bc                         |
    | or word [rax + 1 * rcx + 0x00], cx                             | 66 09 4c 08 00                         |
    | or word [rax + 1 * rcx - 0x00], cx                             | 66 09 4c 08 00                         |
    | or word [rax + 1 * rcx + 0x01], cx                             | 66 09 4c 08 01                         |
    | or word [rax + 1 * rcx - 0x01], cx                             | 66 09 4c 08 ff                         |
    | or word [rax + 1 * rcx + 0x00000001], cx                       | 66 09 8c 08 01 00 00 00                |
    | or word [rax + 1 * rcx - 0x00000001], cx                       | 66 09 8c 08 ff ff ff ff                |
    | or word [rax + 1 * rcx + 0x7f], cx                             | 66 09 4c 08 7f                         |
    | or word [rax + 1 * rcx - 0x7f], cx                             | 66 09 4c 08 81                         |
    | or word [rax + 1 * rcx + 0x80], cx                             | 66 09 8c 08 80 00 00 00                |
    | or word [rax + 1 * rcx - 0x80], cx                             | 66 09 4c 08 80                         |
    | or word [rax + 1 * rcx - 0x81], cx                             | 66 09 8c 08 7f ff ff ff                |
    | or word [rax + 1 * rcx + 0xff], cx                             | 66 09 8c 08 ff 00 00 00                |
    | or word [rax + 1 * rcx - 0xff], cx                             | 66 09 8c 08 01 ff ff ff                |
    | or word [rax + 1 * rcx + 0x7fffffff], cx                       | 66 09 8c 08 ff ff ff 7f                |
    | or word [rax + 1 * rcx - 0x7fffffff], cx                       | 66 09 8c 08 01 00 00 80                |
    | or word [rax + 1 * rcx - 0x80000000], cx                       | 66 09 8c 08 00 00 00 80                |
    | or word [r10 + 0x7f], cx                                       | 66 41 09 4a 7f                         |
    | or word [r10 + 0x80], cx                                       | 66 41 09 8a 80 00 00 00                |
    | or word [r10 - 0x80], cx                                       | 66 41 09 4a 80                         |
    | or word [r10 - 0x81], cx                                       | 66 41 09 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or word [rel @prev5], cx      | 90 90 90 90 90 66 09 0d f4 ff ff ff    |
    | .prev1: nop; or word [rel @prev1], cx                          | 90 66 09 0d f8 ff ff ff                |
    | or word [rel @next1], cx; nop; .next1: nop                     | 66 09 0d 01 00 00 00 90 90             |
    | or word [rel @next5], cx; nop; nop; nop; nop; nop; .next5: nop | 66 09 0d 05 00 00 00 90 90 90 90 90 90 |
    | or word [rax], ax                                              | 66 09 00                               |
    | or word [rax], dx                                              | 66 09 10                               |
    | or word [rax], bx                                              | 66 09 18                               |
    | or word [rax], sp                                              | 66 09 20                               |
    | or word [rax], bp                                              | 66 09 28                               |
    | or word [rax], si                                              | 66 09 30                               |
    | or word [rax], di                                              | 66 09 38                               |
    | or word [rax], r8w                                             | 66 44 09 00                            |
    | or word [rax], r9w                                             | 66 44 09 08                            |
    | or word [rax], r10w                                            | 66 44 09 10                            |
    | or word [rax], r11w                                            | 66 44 09 18                            |
    | or word [rax], r12w                                            | 66 44 09 20                            |
    | or word [rax], r13w                                            | 66 44 09 28                            |
    | or word [rax], r14w                                            | 66 44 09 30                            |
    | or word [rax], r15w                                            | 66 44 09 38                            |
    | or word [rcx], dx                                              | 66 09 11                               |
    | or word [rdx], bx                                              | 66 09 1a                               |
    | or word [rbx], sp                                              | 66 09 23                               |
    | or word [rsp], bp                                              | 66 09 2c 24                            |
    | or word [rbp], si                                              | 66 09 75 00                            |
    | or word [rsi], di                                              | 66 09 3e                               |
    | or word [rdi], r8w                                             | 66 44 09 07                            |
    | or word [r8], r9w                                              | 66 45 09 08                            |
    | or word [r9], r10w                                             | 66 45 09 11                            |
    | or word [r10], r11w                                            | 66 45 09 1a                            |
    | or word [r11], r12w                                            | 66 45 09 23                            |
    | or word [r12], r13w                                            | 66 45 09 2c 24                         |
    | or word [r13], r14w                                            | 66 45 09 75 00                         |
    | or word [r14], r15w                                            | 66 45 09 3e                            |
    | or word [r15], ax                                              | 66 41 09 07                            |
    | or word [rcx + 1 * rcx], dx                                    | 66 09 14 09                            |
    | or word [rdx + 1 * rcx], bx                                    | 66 09 1c 0a                            |
    | or word [rbx + 1 * rcx], sp                                    | 66 09 24 0b                            |
    | or word [rsp + 1 * rcx], bp                                    | 66 09 2c 0c                            |
    | or word [rbp + 1 * rcx], si                                    | 66 09 74 0d 00                         |
    | or word [rsi + 1 * rcx], di                                    | 66 09 3c 0e                            |
    | or word [rdi + 1 * rcx], r8w                                   | 66 44 09 04 0f                         |
    | or word [r8 + 1 * rcx], r9w                                    | 66 45 09 0c 08                         |
    | or word [r9 + 1 * rcx], r10w                                   | 66 45 09 14 09                         |
    | or word [r10 + 1 * rcx], r11w                                  | 66 45 09 1c 0a                         |
    | or word [r11 + 1 * rcx], r12w                                  | 66 45 09 24 0b                         |
    | or word [r12 + 1 * rcx], r13w                                  | 66 45 09 2c 0c                         |
    | or word [r13 + 1 * rcx], r14w                                  | 66 45 09 74 0d 00                      |
    | or word [r14 + 1 * rcx], r15w                                  | 66 45 09 3c 0e                         |
    | or word [r15 + 1 * rcx], ax                                    | 66 41 09 04 0f                         |
    | or word [rax + 1 * rdx], dx                                    | 66 09 14 10                            |
    | or word [rax + 1 * rbx], bx                                    | 66 09 1c 18                            |
    | or word [rax + 1 * rbp], sp                                    | 66 09 24 28                            |
    | or word [rax + 1 * rsi], bp                                    | 66 09 2c 30                            |
    | or word [rax + 1 * rdi], si                                    | 66 09 34 38                            |
    | or word [rax + 1 * r8], di                                     | 66 42 09 3c 00                         |
    | or word [rax + 1 * r9], r8w                                    | 66 46 09 04 08                         |
    | or word [rax + 1 * r10], r9w                                   | 66 46 09 0c 10                         |
    | or word [rax + 1 * r11], r10w                                  | 66 46 09 14 18                         |
    | or word [rax + 1 * r12], r11w                                  | 66 46 09 1c 20                         |
    | or word [rax + 1 * r13], r12w                                  | 66 46 09 24 28                         |
    | or word [rax + 1 * r14], r13w                                  | 66 46 09 2c 30                         |
    | or word [rax + 1 * r15], r14w                                  | 66 46 09 34 38                         |
    | or word [rax + 2 * rcx], r15w                                  | 66 44 09 3c 48                         |
    | or word [rax + 4 * rcx], ax                                    | 66 09 04 88                            |
    | or word [r8 + 1 * r9], dx                                      | 66 43 09 14 08                         |
    | or word [r8 + 2 * r9], bx                                      | 66 43 09 1c 48                         |
    | or word [r8 + 4 * r9], sp                                      | 66 43 09 24 88                         |
    | or word [r8 + 8 * r9], bp                                      | 66 43 09 2c c8                         |
    | or word [1 * rcx], si                                          | 66 09 34 0d 00 00 00 00                |
    | or word [2 * rcx], di                                          | 66 09 3c 4d 00 00 00 00                |
    | or word [4 * rcx], r8w                                         | 66 44 09 04 8d 00 00 00 00             |
    | or word [8 * rcx], r9w                                         | 66 44 09 0c cd 00 00 00 00             |
    | or word [1 * r9], r10w                                         | 66 46 09 14 0d 00 00 00 00             |
    | or word [2 * r9], r11w                                         | 66 46 09 1c 4d 00 00 00 00             |
    | or word [4 * r9], r12w                                         | 66 46 09 24 8d 00 00 00 00             |
    | or word [8 * r9], r13w                                         | 66 46 09 2c cd 00 00 00 00             |
    | or word [r13 + 8 * r12], r14w                                  | 66 47 09 74 e5 00                      |
    | or word [rsp + 4 * r15], r15w                                  | 66 46 09 3c bc                         |
    | or word [rax + 1 * rcx + 0x00], ax                             | 66 09 44 08 00                         |
    | or word [rax + 1 * rcx + 0x01], dx                             | 66 09 54 08 01                         |
    | or word [rax + 1 * rcx - 0x01], bx                             | 66 09 5c 08 ff                         |
    | or word [rax + 1 * rcx + 0x00000001], sp                       | 66 09 a4 08 01 00 00 00                |
    | or word [rax + 1 * rcx - 0x00000001], bp                       | 66 09 ac 08 ff ff ff ff                |
    | or word [rax + 1 * rcx + 0x7f], si                             | 66 09 74 08 7f                         |
    | or word [rax + 1 * rcx - 0x7f], di                             | 66 09 7c 08 81                         |
    | or word [rax + 1 * rcx + 0x80], r8w                            | 66 44 09 84 08 80 00 00 00             |
    | or word [rax + 1 * rcx - 0x80], r9w                            | 66 44 09 4c 08 80                      |
    | or word [rax + 1 * rcx - 0x81], r10w                           | 66 44 09 94 08 7f ff ff ff             |
    | or word [rax + 1 * rcx + 0xff], r11w                           | 66 44 09 9c 08 ff 00 00 00             |
    | or word [rax + 1 * rcx - 0xff], r12w                           | 66 44 09 a4 08 01 ff ff ff             |
    | or word [rax + 1 * rcx + 0x7fffffff], r13w                     | 66 44 09 ac 08 ff ff ff 7f             |
    | or word [rax + 1 * rcx - 0x7fffffff], r14w                     | 66 44 09 b4 08 01 00 00 80             |
    | or word [rax + 1 * rcx - 0x80000000], r15w                     | 66 44 09 bc 08 00 00 00 80             |
    | or word [r10 + 0x7f], ax                                       | 66 41 09 42 7f                         |
    | or word [r10 - 0x80], dx                                       | 66 41 09 52 80                         |
    | or word [r10 - 0x81], bx                                       | 66 41 09 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; or word [rel @prev5], sp      | 90 90 90 90 90 66 09 25 f4 ff ff ff    |
    | .prev1: nop; or word [rel @prev1], bp                          | 90 66 09 2d f8 ff ff ff                |
    | or word [rel @next1], si; nop; .next1: nop                     | 66 09 35 01 00 00 00 90 90             |
    | or word [rel @next5], di; nop; nop; nop; nop; nop; .next5: nop | 66 09 3d 05 00 00 00 90 90 90 90 90 90 |
    | -------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_addr16_reg16():
    encode(OR_ADDR16_REG16)


OR_ADDR8_IMM8 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | or byte [rax], 0x01                                              | 80 08 01                               |
    | or byte [rcx], 0x01                                              | 80 09 01                               |
    | or byte [rdx], 0x01                                              | 80 0a 01                               |
    | or byte [rbx], 0x01                                              | 80 0b 01                               |
    | or byte [rsp], 0x01                                              | 80 0c 24 01                            |
    | or byte [rbp], 0x01                                              | 80 4d 00 01                            |
    | or byte [rsi], 0x01                                              | 80 0e 01                               |
    | or byte [rdi], 0x01                                              | 80 0f 01                               |
    | or byte [r8], 0x01                                               | 41 80 08 01                            |
    | or byte [r9], 0x01                                               | 41 80 09 01                            |
    | or byte [r10], 0x01                                              | 41 80 0a 01                            |
    | or byte [r11], 0x01                                              | 41 80 0b 01                            |
    | or byte [r12], 0x01                                              | 41 80 0c 24 01                         |
    | or byte [r13], 0x01                                              | 41 80 4d 00 01                         |
    | or byte [r14], 0x01                                              | 41 80 0e 01                            |
    | or byte [r15], 0x01                                              | 41 80 0f 01                            |
    | or byte [rax + 1 * rcx], 0x01                                    | 80 0c 08 01                            |
    | or byte [rcx + 1 * rcx], 0x01                                    | 80 0c 09 01                            |
    | or byte [rdx + 1 * rcx], 0x01                                    | 80 0c 0a 01                            |
    | or byte [rbx + 1 * rcx], 0x01                                    | 80 0c 0b 01                            |
    | or byte [rsp + 1 * rcx], 0x01                                    | 80 0c 0c 01                            |
    | or byte [rbp + 1 * rcx], 0x01                                    | 80 4c 0d 00 01                         |
    | or byte [rsi + 1 * rcx], 0x01                                    | 80 0c 0e 01                            |
    | or byte [rdi + 1 * rcx], 0x01                                    | 80 0c 0f 01                            |
    | or byte [r8 + 1 * rcx], 0x01                                     | 41 80 0c 08 01                         |
    | or byte [r9 + 1 * rcx], 0x01                                     | 41 80 0c 09 01                         |
    | or byte [r10 + 1 * rcx], 0x01                                    | 41 80 0c 0a 01                         |
    | or byte [r11 + 1 * rcx], 0x01                                    | 41 80 0c 0b 01                         |
    | or byte [r12 + 1 * rcx], 0x01                                    | 41 80 0c 0c 01                         |
    | or byte [r13 + 1 * rcx], 0x01                                    | 41 80 4c 0d 00 01                      |
    | or byte [r14 + 1 * rcx], 0x01                                    | 41 80 0c 0e 01                         |
    | or byte [r15 + 1 * rcx], 0x01                                    | 41 80 0c 0f 01                         |
    | or byte [rax + 1 * rax], 0x01                                    | 80 0c 00 01                            |
    | or byte [rax + 1 * rdx], 0x01                                    | 80 0c 10 01                            |
    | or byte [rax + 1 * rbx], 0x01                                    | 80 0c 18 01                            |
    | or byte [rax + 1 * rbp], 0x01                                    | 80 0c 28 01                            |
    | or byte [rax + 1 * rsi], 0x01                                    | 80 0c 30 01                            |
    | or byte [rax + 1 * rdi], 0x01                                    | 80 0c 38 01                            |
    | or byte [rax + 1 * r8], 0x01                                     | 42 80 0c 00 01                         |
    | or byte [rax + 1 * r9], 0x01                                     | 42 80 0c 08 01                         |
    | or byte [rax + 1 * r10], 0x01                                    | 42 80 0c 10 01                         |
    | or byte [rax + 1 * r11], 0x01                                    | 42 80 0c 18 01                         |
    | or byte [rax + 1 * r12], 0x01                                    | 42 80 0c 20 01                         |
    | or byte [rax + 1 * r13], 0x01                                    | 42 80 0c 28 01                         |
    | or byte [rax + 1 * r14], 0x01                                    | 42 80 0c 30 01                         |
    | or byte [rax + 1 * r15], 0x01                                    | 42 80 0c 38 01                         |
    | or byte [rax + 2 * rcx], 0x01                                    | 80 0c 48 01                            |
    | or byte [rax + 4 * rcx], 0x01                                    | 80 0c 88 01                            |
    | or byte [rax + 8 * rcx], 0x01                                    | 80 0c c8 01                            |
    | or byte [r8 + 1 * r9], 0x01                                      | 43 80 0c 08 01                         |
    | or byte [r8 + 2 * r9], 0x01                                      | 43 80 0c 48 01                         |
    | or byte [r8 + 4 * r9], 0x01                                      | 43 80 0c 88 01                         |
    | or byte [r8 + 8 * r9], 0x01                                      | 43 80 0c c8 01                         |
    | or byte [1 * rcx], 0x01                                          | 80 0c 0d 00 00 00 00 01                |
    | or byte [2 * rcx], 0x01                                          | 80 0c 4d 00 00 00 00 01                |
    | or byte [4 * rcx], 0x01                                          | 80 0c 8d 00 00 00 00 01                |
    | or byte [8 * rcx], 0x01                                          | 80 0c cd 00 00 00 00 01                |
    | or byte [1 * r9], 0x01                                           | 42 80 0c 0d 00 00 00 00 01             |
    | or byte [2 * r9], 0x01                                           | 42 80 0c 4d 00 00 00 00 01             |
    | or byte [4 * r9], 0x01                                           | 42 80 0c 8d 00 00 00 00 01             |
    | or byte [8 * r9], 0x01                                           | 42 80 0c cd 00 00 00 00 01             |
    | or byte [r13 + 8 * r12], 0x01                                    | 43 80 4c e5 00 01                      |
    | or byte [rsp + 4 * r15], 0x01                                    | 42 80 0c bc 01                         |
    | or byte [rax + 1 * rcx + 0x00], 0x01                             | 80 4c 08 00 01                         |
    | or byte [rax + 1 * rcx - 0x00], 0x01                             | 80 4c 08 00 01                         |
    | or byte [rax + 1 * rcx + 0x01], 0x01                             | 80 4c 08 01 01                         |
    | or byte [rax + 1 * rcx - 0x01], 0x01                             | 80 4c 08 ff 01                         |
    | or byte [rax + 1 * rcx + 0x00000001], 0x01                       | 80 8c 08 01 00 00 00 01                |
    | or byte [rax + 1 * rcx - 0x00000001], 0x01                       | 80 8c 08 ff ff ff ff 01                |
    | or byte [rax + 1 * rcx + 0x7f], 0x01                             | 80 4c 08 7f 01                         |
    | or byte [rax + 1 * rcx - 0x7f], 0x01                             | 80 4c 08 81 01                         |
    | or byte [rax + 1 * rcx + 0x80], 0x01                             | 80 8c 08 80 00 00 00 01                |
    | or byte [rax + 1 * rcx - 0x80], 0x01                             | 80 4c 08 80 01                         |
    | or byte [rax + 1 * rcx - 0x81], 0x01                             | 80 8c 08 7f ff ff ff 01                |
    | or byte [rax + 1 * rcx + 0xff], 0x01                             | 80 8c 08 ff 00 00 00 01                |
    | or byte [rax + 1 * rcx - 0xff], 0x01                             | 80 8c 08 01 ff ff ff 01                |
    | or byte [rax + 1 * rcx + 0x7fffffff], 0x01                       | 80 8c 08 ff ff ff 7f 01                |
    | or byte [rax + 1 * rcx - 0x7fffffff], 0x01                       | 80 8c 08 01 00 00 80 01                |
    | or byte [rax + 1 * rcx - 0x80000000], 0x01                       | 80 8c 08 00 00 00 80 01                |
    | or byte [r10 + 0x7f], 0x01                                       | 41 80 4a 7f 01                         |
    | or byte [r10 + 0x80], 0x01                                       | 41 80 8a 80 00 00 00 01                |
    | or byte [r10 - 0x80], 0x01                                       | 41 80 4a 80 01                         |
    | or byte [r10 - 0x81], 0x01                                       | 41 80 8a 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; or byte [rel @prev5], 0x01      | 90 90 90 90 90 80 0d f4 ff ff ff 01    |
    | .prev1: nop; or byte [rel @prev1], 0x01                          | 90 80 0d f8 ff ff ff 01                |
    | or byte [rel @next1], 0x01; nop; .next1: nop                     | 80 0d 01 00 00 00 01 90 90             |
    | or byte [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 80 0d 05 00 00 00 01 90 90 90 90 90 90 |
    | or byte [rax], 0x00                                              | 80 08 00                               |
    | or byte [rax], 0x7f                                              | 80 08 7f                               |
    | or byte [rax], 0x80                                              | 80 08 80                               |
    | or byte [rax], 0xff                                              | 80 08 ff                               |
    | or byte [rcx], 0x7f                                              | 80 09 7f                               |
    | or byte [rdx], 0x80                                              | 80 0a 80                               |
    | or byte [rbx], 0xff                                              | 80 0b ff                               |
    | or byte [rsp], 0x00                                              | 80 0c 24 00                            |
    | or byte [rsi], 0x7f                                              | 80 0e 7f                               |
    | or byte [rdi], 0x80                                              | 80 0f 80                               |
    | or byte [r8], 0xff                                               | 41 80 08 ff                            |
    | or byte [r9], 0x00                                               | 41 80 09 00                            |
    | or byte [r11], 0x7f                                              | 41 80 0b 7f                            |
    | or byte [r12], 0x80                                              | 41 80 0c 24 80                         |
    | or byte [r13], 0xff                                              | 41 80 4d 00 ff                         |
    | or byte [r14], 0x00                                              | 41 80 0e 00                            |
    | or byte [rax + 1 * rcx], 0x7f                                    | 80 0c 08 7f                            |
    | or byte [rcx + 1 * rcx], 0x80                                    | 80 0c 09 80                            |
    | or byte [rdx + 1 * rcx], 0xff                                    | 80 0c 0a ff                            |
    | or byte [rbx + 1 * rcx], 0x00                                    | 80 0c 0b 00                            |
    | or byte [rbp + 1 * rcx], 0x7f                                    | 80 4c 0d 00 7f                         |
    | or byte [rsi + 1 * rcx], 0x80                                    | 80 0c 0e 80                            |
    | or byte [rdi + 1 * rcx], 0xff                                    | 80 0c 0f ff                            |
    | or byte [r8 + 1 * rcx], 0x00                                     | 41 80 0c 08 00                         |
    | or byte [r10 + 1 * rcx], 0x7f                                    | 41 80 0c 0a 7f                         |
    | or byte [r11 + 1 * rcx], 0x80                                    | 41 80 0c 0b 80                         |
    | or byte [r12 + 1 * rcx], 0xff                                    | 41 80 0c 0c ff                         |
    | or byte [r13 + 1 * rcx], 0x00                                    | 41 80 4c 0d 00 00                      |
    | or byte [r15 + 1 * rcx], 0x7f                                    | 41 80 0c 0f 7f                         |
    | or byte [rax + 1 * rax], 0x80                                    | 80 0c 00 80                            |
    | or byte [rax + 1 * rdx], 0xff                                    | 80 0c 10 ff                            |
    | or byte [rax + 1 * rbx], 0x00                                    | 80 0c 18 00                            |
    | or byte [rax + 1 * rsi], 0x7f                                    | 80 0c 30 7f                            |
    | or byte [rax + 1 * rdi], 0x80                                    | 80 0c 38 80                            |
    | or byte [rax + 1 * r8], 0xff                                     | 42 80 0c 00 ff                         |
    | or byte [rax + 1 * r9], 0x00                                     | 42 80 0c 08 00                         |
    | or byte [rax + 1 * r11], 0x7f                                    | 42 80 0c 18 7f                         |
    | or byte [rax + 1 * r12], 0x80                                    | 42 80 0c 20 80                         |
    | or byte [rax + 1 * r13], 0xff                                    | 42 80 0c 28 ff                         |
    | or byte [rax + 1 * r14], 0x00                                    | 42 80 0c 30 00                         |
    | or byte [rax + 2 * rcx], 0x7f                                    | 80 0c 48 7f                            |
    | or byte [rax + 4 * rcx], 0x80                                    | 80 0c 88 80                            |
    | or byte [rax + 8 * rcx], 0xff                                    | 80 0c c8 ff                            |
    | or byte [r8 + 1 * r9], 0x00                                      | 43 80 0c 08 00                         |
    | or byte [r8 + 4 * r9], 0x7f                                      | 43 80 0c 88 7f                         |
    | or byte [r8 + 8 * r9], 0x80                                      | 43 80 0c c8 80                         |
    | or byte [1 * rcx], 0xff                                          | 80 0c 0d 00 00 00 00 ff                |
    | or byte [2 * rcx], 0x00                                          | 80 0c 4d 00 00 00 00 00                |
    | or byte [8 * rcx], 0x7f                                          | 80 0c cd 00 00 00 00 7f                |
    | or byte [1 * r9], 0x80                                           | 42 80 0c 0d 00 00 00 00 80             |
    | or byte [2 * r9], 0xff                                           | 42 80 0c 4d 00 00 00 00 ff             |
    | or byte [4 * r9], 0x00                                           | 42 80 0c 8d 00 00 00 00 00             |
    | or byte [r13 + 8 * r12], 0x7f                                    | 43 80 4c e5 00 7f                      |
    | or byte [rsp + 4 * r15], 0x80                                    | 42 80 0c bc 80                         |
    | or byte [rax + 1 * rcx + 0x00], 0xff                             | 80 4c 08 00 ff                         |
    | or byte [rax + 1 * rcx - 0x00], 0x00                             | 80 4c 08 00 00                         |
    | or byte [rax + 1 * rcx - 0x01], 0x7f                             | 80 4c 08 ff 7f                         |
    | or byte [rax + 1 * rcx + 0x00000001], 0x80                       | 80 8c 08 01 00 00 00 80                |
    | or byte [rax + 1 * rcx - 0x00000001], 0xff                       | 80 8c 08 ff ff ff ff ff                |
    | or byte [rax + 1 * rcx + 0x7f], 0x00                             | 80 4c 08 7f 00                         |
    | or byte [rax + 1 * rcx + 0x80], 0x7f                             | 80 8c 08 80 00 00 00 7f                |
    | or byte [rax + 1 * rcx - 0x80], 0x80                             | 80 4c 08 80 80                         |
    | or byte [rax + 1 * rcx - 0x81], 0xff                             | 80 8c 08 7f ff ff ff ff                |
    | or byte [rax + 1 * rcx + 0xff], 0x00                             | 80 8c 08 ff 00 00 00 00                |
    | or byte [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 80 8c 08 ff ff ff 7f 7f                |
    | or byte [rax + 1 * rcx - 0x7fffffff], 0x80                       | 80 8c 08 01 00 00 80 80                |
    | or byte [rax + 1 * rcx - 0x80000000], 0xff                       | 80 8c 08 00 00 00 80 ff                |
    | or byte [r10 + 0x7f], 0x00                                       | 41 80 4a 7f 00                         |
    | or byte [r10 - 0x80], 0x7f                                       | 41 80 4a 80 7f                         |
    | or byte [r10 - 0x81], 0x80                                       | 41 80 8a 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; or byte [rel @prev5], 0xff      | 90 90 90 90 90 80 0d f4 ff ff ff ff    |
    | .prev1: nop; or byte [rel @prev1], 0x00                          | 90 80 0d f8 ff ff ff 00                |
    | or byte [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 80 0d 05 00 00 00 7f 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_addr8_imm8():
    encode(OR_ADDR8_IMM8)


OR_ADDR8_REG8 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | or byte [rax], cl                                               | 08 08                                  |
    | or byte [rcx], cl                                               | 08 09                                  |
    | or byte [rdx], cl                                               | 08 0a                                  |
    | or byte [rbx], cl                                               | 08 0b                                  |
    | or byte [rsp], cl                                               | 08 0c 24                               |
    | or byte [rbp], cl                                               | 08 4d 00                               |
    | or byte [rsi], cl                                               | 08 0e                                  |
    | or byte [rdi], cl                                               | 08 0f                                  |
    | or byte [r8], cl                                                | 41 08 08                               |
    | or byte [r9], cl                                                | 41 08 09                               |
    | or byte [r10], cl                                               | 41 08 0a                               |
    | or byte [r11], cl                                               | 41 08 0b                               |
    | or byte [r12], cl                                               | 41 08 0c 24                            |
    | or byte [r13], cl                                               | 41 08 4d 00                            |
    | or byte [r14], cl                                               | 41 08 0e                               |
    | or byte [r15], cl                                               | 41 08 0f                               |
    | or byte [rax + 1 * rcx], cl                                     | 08 0c 08                               |
    | or byte [rcx + 1 * rcx], cl                                     | 08 0c 09                               |
    | or byte [rdx + 1 * rcx], cl                                     | 08 0c 0a                               |
    | or byte [rbx + 1 * rcx], cl                                     | 08 0c 0b                               |
    | or byte [rsp + 1 * rcx], cl                                     | 08 0c 0c                               |
    | or byte [rbp + 1 * rcx], cl                                     | 08 4c 0d 00                            |
    | or byte [rsi + 1 * rcx], cl                                     | 08 0c 0e                               |
    | or byte [rdi + 1 * rcx], cl                                     | 08 0c 0f                               |
    | or byte [r8 + 1 * rcx], cl                                      | 41 08 0c 08                            |
    | or byte [r9 + 1 * rcx], cl                                      | 41 08 0c 09                            |
    | or byte [r10 + 1 * rcx], cl                                     | 41 08 0c 0a                            |
    | or byte [r11 + 1 * rcx], cl                                     | 41 08 0c 0b                            |
    | or byte [r12 + 1 * rcx], cl                                     | 41 08 0c 0c                            |
    | or byte [r13 + 1 * rcx], cl                                     | 41 08 4c 0d 00                         |
    | or byte [r14 + 1 * rcx], cl                                     | 41 08 0c 0e                            |
    | or byte [r15 + 1 * rcx], cl                                     | 41 08 0c 0f                            |
    | or byte [rax + 1 * rax], cl                                     | 08 0c 00                               |
    | or byte [rax + 1 * rdx], cl                                     | 08 0c 10                               |
    | or byte [rax + 1 * rbx], cl                                     | 08 0c 18                               |
    | or byte [rax + 1 * rbp], cl                                     | 08 0c 28                               |
    | or byte [rax + 1 * rsi], cl                                     | 08 0c 30                               |
    | or byte [rax + 1 * rdi], cl                                     | 08 0c 38                               |
    | or byte [rax + 1 * r8], cl                                      | 42 08 0c 00                            |
    | or byte [rax + 1 * r9], cl                                      | 42 08 0c 08                            |
    | or byte [rax + 1 * r10], cl                                     | 42 08 0c 10                            |
    | or byte [rax + 1 * r11], cl                                     | 42 08 0c 18                            |
    | or byte [rax + 1 * r12], cl                                     | 42 08 0c 20                            |
    | or byte [rax + 1 * r13], cl                                     | 42 08 0c 28                            |
    | or byte [rax + 1 * r14], cl                                     | 42 08 0c 30                            |
    | or byte [rax + 1 * r15], cl                                     | 42 08 0c 38                            |
    | or byte [rax + 2 * rcx], cl                                     | 08 0c 48                               |
    | or byte [rax + 4 * rcx], cl                                     | 08 0c 88                               |
    | or byte [rax + 8 * rcx], cl                                     | 08 0c c8                               |
    | or byte [r8 + 1 * r9], cl                                       | 43 08 0c 08                            |
    | or byte [r8 + 2 * r9], cl                                       | 43 08 0c 48                            |
    | or byte [r8 + 4 * r9], cl                                       | 43 08 0c 88                            |
    | or byte [r8 + 8 * r9], cl                                       | 43 08 0c c8                            |
    | or byte [1 * rcx], cl                                           | 08 0c 0d 00 00 00 00                   |
    | or byte [2 * rcx], cl                                           | 08 0c 4d 00 00 00 00                   |
    | or byte [4 * rcx], cl                                           | 08 0c 8d 00 00 00 00                   |
    | or byte [8 * rcx], cl                                           | 08 0c cd 00 00 00 00                   |
    | or byte [1 * r9], cl                                            | 42 08 0c 0d 00 00 00 00                |
    | or byte [2 * r9], cl                                            | 42 08 0c 4d 00 00 00 00                |
    | or byte [4 * r9], cl                                            | 42 08 0c 8d 00 00 00 00                |
    | or byte [8 * r9], cl                                            | 42 08 0c cd 00 00 00 00                |
    | or byte [r13 + 8 * r12], cl                                     | 43 08 4c e5 00                         |
    | or byte [rsp + 4 * r15], cl                                     | 42 08 0c bc                            |
    | or byte [rax + 1 * rcx + 0x00], cl                              | 08 4c 08 00                            |
    | or byte [rax + 1 * rcx - 0x00], cl                              | 08 4c 08 00                            |
    | or byte [rax + 1 * rcx + 0x01], cl                              | 08 4c 08 01                            |
    | or byte [rax + 1 * rcx - 0x01], cl                              | 08 4c 08 ff                            |
    | or byte [rax + 1 * rcx + 0x00000001], cl                        | 08 8c 08 01 00 00 00                   |
    | or byte [rax + 1 * rcx - 0x00000001], cl                        | 08 8c 08 ff ff ff ff                   |
    | or byte [rax + 1 * rcx + 0x7f], cl                              | 08 4c 08 7f                            |
    | or byte [rax + 1 * rcx - 0x7f], cl                              | 08 4c 08 81                            |
    | or byte [rax + 1 * rcx + 0x80], cl                              | 08 8c 08 80 00 00 00                   |
    | or byte [rax + 1 * rcx - 0x80], cl                              | 08 4c 08 80                            |
    | or byte [rax + 1 * rcx - 0x81], cl                              | 08 8c 08 7f ff ff ff                   |
    | or byte [rax + 1 * rcx + 0xff], cl                              | 08 8c 08 ff 00 00 00                   |
    | or byte [rax + 1 * rcx - 0xff], cl                              | 08 8c 08 01 ff ff ff                   |
    | or byte [rax + 1 * rcx + 0x7fffffff], cl                        | 08 8c 08 ff ff ff 7f                   |
    | or byte [rax + 1 * rcx - 0x7fffffff], cl                        | 08 8c 08 01 00 00 80                   |
    | or byte [rax + 1 * rcx - 0x80000000], cl                        | 08 8c 08 00 00 00 80                   |
    | or byte [r10 + 0x7f], cl                                        | 41 08 4a 7f                            |
    | or byte [r10 + 0x80], cl                                        | 41 08 8a 80 00 00 00                   |
    | or byte [r10 - 0x80], cl                                        | 41 08 4a 80                            |
    | or byte [r10 - 0x81], cl                                        | 41 08 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or byte [rel @prev5], cl       | 90 90 90 90 90 08 0d f5 ff ff ff       |
    | .prev1: nop; or byte [rel @prev1], cl                           | 90 08 0d f9 ff ff ff                   |
    | or byte [rel @next1], cl; nop; .next1: nop                      | 08 0d 01 00 00 00 90 90                |
    | or byte [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop  | 08 0d 05 00 00 00 90 90 90 90 90 90    |
    | or byte [rax], al                                               | 08 00                                  |
    | or byte [rax], dl                                               | 08 10                                  |
    | or byte [rax], bl                                               | 08 18                                  |
    | or byte [rax], spl                                              | 40 08 20                               |
    | or byte [rax], bpl                                              | 40 08 28                               |
    | or byte [rax], sil                                              | 40 08 30                               |
    | or byte [rax], dil                                              | 40 08 38                               |
    | or byte [rax], r8b                                              | 44 08 00                               |
    | or byte [rax], r9b                                              | 44 08 08                               |
    | or byte [rax], r10b                                             | 44 08 10                               |
    | or byte [rax], r11b                                             | 44 08 18                               |
    | or byte [rax], r12b                                             | 44 08 20                               |
    | or byte [rax], r13b                                             | 44 08 28                               |
    | or byte [rax], r14b                                             | 44 08 30                               |
    | or byte [rax], r15b                                             | 44 08 38                               |
    | or byte [rax], ah                                               | 08 20                                  |
    | or byte [rax], ch                                               | 08 28                                  |
    | or byte [rax], dh                                               | 08 30                                  |
    | or byte [rax], bh                                               | 08 38                                  |
    | or byte [rcx], dl                                               | 08 11                                  |
    | or byte [rdx], bl                                               | 08 1a                                  |
    | or byte [rbx], spl                                              | 40 08 23                               |
    | or byte [rsp], bpl                                              | 40 08 2c 24                            |
    | or byte [rbp], sil                                              | 40 08 75 00                            |
    | or byte [rsi], dil                                              | 40 08 3e                               |
    | or byte [rdi], r8b                                              | 44 08 07                               |
    | or byte [r8], r9b                                               | 45 08 08                               |
    | or byte [r9], r10b                                              | 45 08 11                               |
    | or byte [r10], r11b                                             | 45 08 1a                               |
    | or byte [r11], r12b                                             | 45 08 23                               |
    | or byte [r12], r13b                                             | 45 08 2c 24                            |
    | or byte [r13], r14b                                             | 45 08 75 00                            |
    | or byte [r14], r15b                                             | 45 08 3e                               |
    | or byte [r15], ah                                               | !! !! !!                               |
    | or byte [rax + 1 * rcx], ch                                     | 08 2c 08                               |
    | or byte [rcx + 1 * rcx], dh                                     | 08 34 09                               |
    | or byte [rdx + 1 * rcx], bh                                     | 08 3c 0a                               |
    | or byte [rbx + 1 * rcx], al                                     | 08 04 0b                               |
    | or byte [rbp + 1 * rcx], dl                                     | 08 54 0d 00                            |
    | or byte [rsi + 1 * rcx], bl                                     | 08 1c 0e                               |
    | or byte [rdi + 1 * rcx], spl                                    | 40 08 24 0f                            |
    | or byte [r8 + 1 * rcx], bpl                                     | 41 08 2c 08                            |
    | or byte [r9 + 1 * rcx], sil                                     | 41 08 34 09                            |
    | or byte [r10 + 1 * rcx], dil                                    | 41 08 3c 0a                            |
    | or byte [r11 + 1 * rcx], r8b                                    | 45 08 04 0b                            |
    | or byte [r12 + 1 * rcx], r9b                                    | 45 08 0c 0c                            |
    | or byte [r13 + 1 * rcx], r10b                                   | 45 08 54 0d 00                         |
    | or byte [r14 + 1 * rcx], r11b                                   | 45 08 1c 0e                            |
    | or byte [r15 + 1 * rcx], r12b                                   | 45 08 24 0f                            |
    | or byte [rax + 1 * rax], r13b                                   | 44 08 2c 00                            |
    | or byte [rax + 1 * rdx], r14b                                   | 44 08 34 10                            |
    | or byte [rax + 1 * rbx], r15b                                   | 44 08 3c 18                            |
    | or byte [rax + 1 * rbp], ah                                     | 08 24 28                               |
    | or byte [rax + 1 * rsi], ch                                     | 08 2c 30                               |
    | or byte [rax + 1 * rdi], dh                                     | 08 34 38                               |
    | or byte [rax + 1 * r8], bh                                      | !! !! !!                               |
    | or byte [rax + 1 * r9], al                                      | 42 08 04 08                            |
    | or byte [rax + 1 * r11], dl                                     | 42 08 14 18                            |
    | or byte [rax + 1 * r12], bl                                     | 42 08 1c 20                            |
    | or byte [rax + 1 * r13], spl                                    | 42 08 24 28                            |
    | or byte [rax + 1 * r14], bpl                                    | 42 08 2c 30                            |
    | or byte [rax + 1 * r15], sil                                    | 42 08 34 38                            |
    | or byte [rax + 2 * rcx], dil                                    | 40 08 3c 48                            |
    | or byte [rax + 4 * rcx], r8b                                    | 44 08 04 88                            |
    | or byte [rax + 8 * rcx], r9b                                    | 44 08 0c c8                            |
    | or byte [r8 + 1 * r9], r10b                                     | 47 08 14 08                            |
    | or byte [r8 + 2 * r9], r11b                                     | 47 08 1c 48                            |
    | or byte [r8 + 4 * r9], r12b                                     | 47 08 24 88                            |
    | or byte [r8 + 8 * r9], r13b                                     | 47 08 2c c8                            |
    | or byte [1 * rcx], r14b                                         | 44 08 34 0d 00 00 00 00                |
    | or byte [2 * rcx], r15b                                         | 44 08 3c 4d 00 00 00 00                |
    | or byte [4 * rcx], ah                                           | 08 24 8d 00 00 00 00                   |
    | or byte [8 * rcx], ch                                           | 08 2c cd 00 00 00 00                   |
    | or byte [1 * r9], dh                                            | !! !! !!                               |
    | or byte [2 * r9], bh                                            | !! !! !!                               |
    | or byte [4 * r9], al                                            | 42 08 04 8d 00 00 00 00                |
    | or byte [r13 + 8 * r12], dl                                     | 43 08 54 e5 00                         |
    | or byte [rsp + 4 * r15], bl                                     | 42 08 1c bc                            |
    | or byte [rax + 1 * rcx + 0x00], spl                             | 40 08 64 08 00                         |
    | or byte [rax + 1 * rcx - 0x00], bpl                             | 40 08 6c 08 00                         |
    | or byte [rax + 1 * rcx + 0x01], sil                             | 40 08 74 08 01                         |
    | or byte [rax + 1 * rcx - 0x01], dil                             | 40 08 7c 08 ff                         |
    | or byte [rax + 1 * rcx + 0x00000001], r8b                       | 44 08 84 08 01 00 00 00                |
    | or byte [rax + 1 * rcx - 0x00000001], r9b                       | 44 08 8c 08 ff ff ff ff                |
    | or byte [rax + 1 * rcx + 0x7f], r10b                            | 44 08 54 08 7f                         |
    | or byte [rax + 1 * rcx - 0x7f], r11b                            | 44 08 5c 08 81                         |
    | or byte [rax + 1 * rcx + 0x80], r12b                            | 44 08 a4 08 80 00 00 00                |
    | or byte [rax + 1 * rcx - 0x80], r13b                            | 44 08 6c 08 80                         |
    | or byte [rax + 1 * rcx - 0x81], r14b                            | 44 08 b4 08 7f ff ff ff                |
    | or byte [rax + 1 * rcx + 0xff], r15b                            | 44 08 bc 08 ff 00 00 00                |
    | or byte [rax + 1 * rcx - 0xff], ah                              | 08 a4 08 01 ff ff ff                   |
    | or byte [rax + 1 * rcx + 0x7fffffff], ch                        | 08 ac 08 ff ff ff 7f                   |
    | or byte [rax + 1 * rcx - 0x7fffffff], dh                        | 08 b4 08 01 00 00 80                   |
    | or byte [rax + 1 * rcx - 0x80000000], bh                        | 08 bc 08 00 00 00 80                   |
    | or byte [r10 + 0x7f], al                                        | 41 08 42 7f                            |
    | or byte [r10 - 0x80], dl                                        | 41 08 52 80                            |
    | or byte [r10 - 0x81], bl                                        | 41 08 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; or byte [rel @prev5], spl      | 90 90 90 90 90 40 08 25 f4 ff ff ff    |
    | .prev1: nop; or byte [rel @prev1], bpl                          | 90 40 08 2d f8 ff ff ff                |
    | or byte [rel @next1], sil; nop; .next1: nop                     | 40 08 35 01 00 00 00 90 90             |
    | or byte [rel @next5], dil; nop; nop; nop; nop; nop; .next5: nop | 40 08 3d 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_or_addr8_reg8():
    encode(OR_ADDR8_REG8)
