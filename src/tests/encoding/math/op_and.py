from tests.encoding.core import encode, exhaust


def can_exhaust_and():
    exhaust(
        AND_ADDR16_IMM16,
        AND_ADDR16_IMM8,
        AND_ADDR16_REG16,
        AND_ADDR32_IMM32,
        AND_ADDR32_IMM8,
        AND_ADDR32_REG32,
        AND_ADDR64_IMM32,
        AND_ADDR64_IMM8,
        AND_ADDR64_REG64,
        AND_ADDR8_IMM8,
        AND_ADDR8_REG8,
        AND_REG16_ADDR16,
        AND_REG16_IMM16,
        AND_REG16_IMM8,
        AND_REG16_REG16,
        AND_REG32_ADDR32,
        AND_REG32_IMM32,
        AND_REG32_IMM8,
        AND_REG32_REG32,
        AND_REG64_ADDR64,
        AND_REG64_IMM32,
        AND_REG64_IMM8,
        AND_REG64_REG64,
        AND_REG8_ADDR8,
        AND_REG8_IMM8,
        AND_REG8_REG8,
    )


AND_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | and rax, 0x01 | 48 83 e0 01 | *** | and rax, 0x00 | 48 83 e0 00 |
    | and rcx, 0x01 | 48 83 e1 01 | *** | and rax, 0x7f | 48 83 e0 7f |
    | and rdx, 0x01 | 48 83 e2 01 | *** | and rax, 0x80 | 48 83 e0 80 |
    | and rbx, 0x01 | 48 83 e3 01 | *** | and rax, 0xff | 48 83 e0 ff |
    | and rsp, 0x01 | 48 83 e4 01 | *** | and rcx, 0x7f | 48 83 e1 7f |
    | and rbp, 0x01 | 48 83 e5 01 | *** | and rdx, 0x80 | 48 83 e2 80 |
    | and rsi, 0x01 | 48 83 e6 01 | *** | and rbx, 0xff | 48 83 e3 ff |
    | and rdi, 0x01 | 48 83 e7 01 | *** | and rsp, 0x00 | 48 83 e4 00 |
    | and r8, 0x01  | 49 83 e0 01 | *** | and rsi, 0x7f | 48 83 e6 7f |
    | and r9, 0x01  | 49 83 e1 01 | *** | and rdi, 0x80 | 48 83 e7 80 |
    | and r10, 0x01 | 49 83 e2 01 | *** | and r8, 0xff  | 49 83 e0 ff |
    | and r11, 0x01 | 49 83 e3 01 | *** | and r9, 0x00  | 49 83 e1 00 |
    | and r12, 0x01 | 49 83 e4 01 | *** | and r11, 0x7f | 49 83 e3 7f |
    | and r13, 0x01 | 49 83 e5 01 | *** | and r12, 0x80 | 49 83 e4 80 |
    | and r14, 0x01 | 49 83 e6 01 | *** | and r13, 0xff | 49 83 e5 ff |
    | and r15, 0x01 | 49 83 e7 01 | *** | and r14, 0x00 | 49 83 e6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_and_reg64_imm8():
    encode(AND_REG64_IMM8)


AND_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | and rax, 0x00000001 | 48 25 01 00 00 00    | *** | and rax, 0x00007fff | 48 25 ff 7f 00 00    |
    | and rcx, 0x00000001 | 48 81 e1 01 00 00 00 | *** | and rax, 0x00008000 | 48 25 00 80 00 00    |
    | and rdx, 0x00000001 | 48 81 e2 01 00 00 00 | *** | and rax, 0x0000ffff | 48 25 ff ff 00 00    |
    | and rbx, 0x00000001 | 48 81 e3 01 00 00 00 | *** | and rax, 0x00010000 | 48 25 00 00 01 00    |
    | and rsp, 0x00000001 | 48 81 e4 01 00 00 00 | *** | and rax, 0x7fffffff | 48 25 ff ff ff 7f    |
    | and rbp, 0x00000001 | 48 81 e5 01 00 00 00 | *** | and rax, 0x80000000 | 48 25 00 00 00 80    |
    | and rsi, 0x00000001 | 48 81 e6 01 00 00 00 | *** | and rax, 0xffffffff | 48 25 ff ff ff ff    |
    | and rdi, 0x00000001 | 48 81 e7 01 00 00 00 | *** | and rcx, 0x0000007f | 48 81 e1 7f 00 00 00 |
    | and r8, 0x00000001  | 49 81 e0 01 00 00 00 | *** | and rdx, 0x00000080 | 48 81 e2 80 00 00 00 |
    | and r9, 0x00000001  | 49 81 e1 01 00 00 00 | *** | and rbx, 0x000000ff | 48 81 e3 ff 00 00 00 |
    | and r10, 0x00000001 | 49 81 e2 01 00 00 00 | *** | and rsp, 0x00000100 | 48 81 e4 00 01 00 00 |
    | and r11, 0x00000001 | 49 81 e3 01 00 00 00 | *** | and rbp, 0x00007fff | 48 81 e5 ff 7f 00 00 |
    | and r12, 0x00000001 | 49 81 e4 01 00 00 00 | *** | and rsi, 0x00008000 | 48 81 e6 00 80 00 00 |
    | and r13, 0x00000001 | 49 81 e5 01 00 00 00 | *** | and rdi, 0x0000ffff | 48 81 e7 ff ff 00 00 |
    | and r14, 0x00000001 | 49 81 e6 01 00 00 00 | *** | and r8, 0x00010000  | 49 81 e0 00 00 01 00 |
    | and r15, 0x00000001 | 49 81 e7 01 00 00 00 | *** | and r9, 0x7fffffff  | 49 81 e1 ff ff ff 7f |
    | and rax, 0x00000000 | 48 25 00 00 00 00    | *** | and r10, 0x80000000 | 49 81 e2 00 00 00 80 |
    | and rax, 0x0000007f | 48 25 7f 00 00 00    | *** | and r11, 0xffffffff | 49 81 e3 ff ff ff ff |
    | and rax, 0x00000080 | 48 25 80 00 00 00    | *** | and r12, 0x00000000 | 49 81 e4 00 00 00 00 |
    | and rax, 0x000000ff | 48 25 ff 00 00 00    | *** | and r14, 0x0000007f | 49 81 e6 7f 00 00 00 |
    | and rax, 0x00000100 | 48 25 00 01 00 00    | *** | and r15, 0x00000080 | 49 81 e7 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_and_reg64_imm32():
    encode(AND_REG64_IMM32)


AND_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | and rax, rcx | 48 21 c8 | *** | and rax, r8  | 4c 21 c0 |
    | and rcx, rcx | 48 21 c9 | *** | and rax, r9  | 4c 21 c8 |
    | and rdx, rcx | 48 21 ca | *** | and rax, r10 | 4c 21 d0 |
    | and rbx, rcx | 48 21 cb | *** | and rax, r11 | 4c 21 d8 |
    | and rsp, rcx | 48 21 cc | *** | and rax, r12 | 4c 21 e0 |
    | and rbp, rcx | 48 21 cd | *** | and rax, r13 | 4c 21 e8 |
    | and rsi, rcx | 48 21 ce | *** | and rax, r14 | 4c 21 f0 |
    | and rdi, rcx | 48 21 cf | *** | and rax, r15 | 4c 21 f8 |
    | and r8, rcx  | 49 21 c8 | *** | and rcx, rdx | 48 21 d1 |
    | and r9, rcx  | 49 21 c9 | *** | and rdx, rbx | 48 21 da |
    | and r10, rcx | 49 21 ca | *** | and rbx, rsp | 48 21 e3 |
    | and r11, rcx | 49 21 cb | *** | and rsp, rbp | 48 21 ec |
    | and r12, rcx | 49 21 cc | *** | and rbp, rsi | 48 21 f5 |
    | and r13, rcx | 49 21 cd | *** | and rsi, rdi | 48 21 fe |
    | and r14, rcx | 49 21 ce | *** | and rdi, r8  | 4c 21 c7 |
    | and r15, rcx | 49 21 cf | *** | and r8, r9   | 4d 21 c8 |
    | and rax, rax | 48 21 c0 | *** | and r9, r10  | 4d 21 d1 |
    | and rax, rdx | 48 21 d0 | *** | and r10, r11 | 4d 21 da |
    | and rax, rbx | 48 21 d8 | *** | and r11, r12 | 4d 21 e3 |
    | and rax, rsp | 48 21 e0 | *** | and r12, r13 | 4d 21 ec |
    | and rax, rbp | 48 21 e8 | *** | and r13, r14 | 4d 21 f5 |
    | and rax, rsi | 48 21 f0 | *** | and r14, r15 | 4d 21 fe |
    | and rax, rdi | 48 21 f8 | *** | and r15, rax | 49 21 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_and_reg64_reg64():
    encode(AND_REG64_REG64)


AND_REG64_ADDR64 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | and rax, qword [rcx]                                              | 48 23 01                               |
    | and rcx, qword [rcx]                                              | 48 23 09                               |
    | and rdx, qword [rcx]                                              | 48 23 11                               |
    | and rbx, qword [rcx]                                              | 48 23 19                               |
    | and rsp, qword [rcx]                                              | 48 23 21                               |
    | and rbp, qword [rcx]                                              | 48 23 29                               |
    | and rsi, qword [rcx]                                              | 48 23 31                               |
    | and rdi, qword [rcx]                                              | 48 23 39                               |
    | and r8, qword [rcx]                                               | 4c 23 01                               |
    | and r9, qword [rcx]                                               | 4c 23 09                               |
    | and r10, qword [rcx]                                              | 4c 23 11                               |
    | and r11, qword [rcx]                                              | 4c 23 19                               |
    | and r12, qword [rcx]                                              | 4c 23 21                               |
    | and r13, qword [rcx]                                              | 4c 23 29                               |
    | and r14, qword [rcx]                                              | 4c 23 31                               |
    | and r15, qword [rcx]                                              | 4c 23 39                               |
    | and rax, qword [rax]                                              | 48 23 00                               |
    | and rax, qword [rdx]                                              | 48 23 02                               |
    | and rax, qword [rbx]                                              | 48 23 03                               |
    | and rax, qword [rsp]                                              | 48 23 04 24                            |
    | and rax, qword [rbp]                                              | 48 23 45 00                            |
    | and rax, qword [rsi]                                              | 48 23 06                               |
    | and rax, qword [rdi]                                              | 48 23 07                               |
    | and rax, qword [r8]                                               | 49 23 00                               |
    | and rax, qword [r9]                                               | 49 23 01                               |
    | and rax, qword [r10]                                              | 49 23 02                               |
    | and rax, qword [r11]                                              | 49 23 03                               |
    | and rax, qword [r12]                                              | 49 23 04 24                            |
    | and rax, qword [r13]                                              | 49 23 45 00                            |
    | and rax, qword [r14]                                              | 49 23 06                               |
    | and rax, qword [r15]                                              | 49 23 07                               |
    | and rax, qword [rax + 1 * rcx]                                    | 48 23 04 08                            |
    | and rax, qword [rcx + 1 * rcx]                                    | 48 23 04 09                            |
    | and rax, qword [rdx + 1 * rcx]                                    | 48 23 04 0a                            |
    | and rax, qword [rbx + 1 * rcx]                                    | 48 23 04 0b                            |
    | and rax, qword [rsp + 1 * rcx]                                    | 48 23 04 0c                            |
    | and rax, qword [rbp + 1 * rcx]                                    | 48 23 44 0d 00                         |
    | and rax, qword [rsi + 1 * rcx]                                    | 48 23 04 0e                            |
    | and rax, qword [rdi + 1 * rcx]                                    | 48 23 04 0f                            |
    | and rax, qword [r8 + 1 * rcx]                                     | 49 23 04 08                            |
    | and rax, qword [r9 + 1 * rcx]                                     | 49 23 04 09                            |
    | and rax, qword [r10 + 1 * rcx]                                    | 49 23 04 0a                            |
    | and rax, qword [r11 + 1 * rcx]                                    | 49 23 04 0b                            |
    | and rax, qword [r12 + 1 * rcx]                                    | 49 23 04 0c                            |
    | and rax, qword [r13 + 1 * rcx]                                    | 49 23 44 0d 00                         |
    | and rax, qword [r14 + 1 * rcx]                                    | 49 23 04 0e                            |
    | and rax, qword [r15 + 1 * rcx]                                    | 49 23 04 0f                            |
    | and rax, qword [rax + 1 * rax]                                    | 48 23 04 00                            |
    | and rax, qword [rax + 1 * rdx]                                    | 48 23 04 10                            |
    | and rax, qword [rax + 1 * rbx]                                    | 48 23 04 18                            |
    | and rax, qword [rax + 1 * rbp]                                    | 48 23 04 28                            |
    | and rax, qword [rax + 1 * rsi]                                    | 48 23 04 30                            |
    | and rax, qword [rax + 1 * rdi]                                    | 48 23 04 38                            |
    | and rax, qword [rax + 1 * r8]                                     | 4a 23 04 00                            |
    | and rax, qword [rax + 1 * r9]                                     | 4a 23 04 08                            |
    | and rax, qword [rax + 1 * r10]                                    | 4a 23 04 10                            |
    | and rax, qword [rax + 1 * r11]                                    | 4a 23 04 18                            |
    | and rax, qword [rax + 1 * r12]                                    | 4a 23 04 20                            |
    | and rax, qword [rax + 1 * r13]                                    | 4a 23 04 28                            |
    | and rax, qword [rax + 1 * r14]                                    | 4a 23 04 30                            |
    | and rax, qword [rax + 1 * r15]                                    | 4a 23 04 38                            |
    | and rax, qword [rax + 2 * rcx]                                    | 48 23 04 48                            |
    | and rax, qword [rax + 4 * rcx]                                    | 48 23 04 88                            |
    | and rax, qword [rax + 8 * rcx]                                    | 48 23 04 c8                            |
    | and rax, qword [r8 + 1 * r9]                                      | 4b 23 04 08                            |
    | and rax, qword [r8 + 2 * r9]                                      | 4b 23 04 48                            |
    | and rax, qword [r8 + 4 * r9]                                      | 4b 23 04 88                            |
    | and rax, qword [r8 + 8 * r9]                                      | 4b 23 04 c8                            |
    | and rax, qword [1 * rcx]                                          | 48 23 04 0d 00 00 00 00                |
    | and rax, qword [2 * rcx]                                          | 48 23 04 4d 00 00 00 00                |
    | and rax, qword [4 * rcx]                                          | 48 23 04 8d 00 00 00 00                |
    | and rax, qword [8 * rcx]                                          | 48 23 04 cd 00 00 00 00                |
    | and rax, qword [1 * r9]                                           | 4a 23 04 0d 00 00 00 00                |
    | and rax, qword [2 * r9]                                           | 4a 23 04 4d 00 00 00 00                |
    | and rax, qword [4 * r9]                                           | 4a 23 04 8d 00 00 00 00                |
    | and rax, qword [8 * r9]                                           | 4a 23 04 cd 00 00 00 00                |
    | and rax, qword [r13 + 8 * r12]                                    | 4b 23 44 e5 00                         |
    | and rax, qword [rsp + 4 * r15]                                    | 4a 23 04 bc                            |
    | and rax, qword [rax + 1 * rcx + 0x00]                             | 48 23 44 08 00                         |
    | and rax, qword [rax + 1 * rcx - 0x00]                             | 48 23 44 08 00                         |
    | and rax, qword [rax + 1 * rcx + 0x01]                             | 48 23 44 08 01                         |
    | and rax, qword [rax + 1 * rcx - 0x01]                             | 48 23 44 08 ff                         |
    | and rax, qword [rax + 1 * rcx + 0x00000001]                       | 48 23 84 08 01 00 00 00                |
    | and rax, qword [rax + 1 * rcx - 0x00000001]                       | 48 23 84 08 ff ff ff ff                |
    | and rax, qword [rax + 1 * rcx + 0x7f]                             | 48 23 44 08 7f                         |
    | and rax, qword [rax + 1 * rcx - 0x7f]                             | 48 23 44 08 81                         |
    | and rax, qword [rax + 1 * rcx + 0x80]                             | 48 23 84 08 80 00 00 00                |
    | and rax, qword [rax + 1 * rcx - 0x80]                             | 48 23 44 08 80                         |
    | and rax, qword [rax + 1 * rcx - 0x81]                             | 48 23 84 08 7f ff ff ff                |
    | and rax, qword [rax + 1 * rcx + 0xff]                             | 48 23 84 08 ff 00 00 00                |
    | and rax, qword [rax + 1 * rcx - 0xff]                             | 48 23 84 08 01 ff ff ff                |
    | and rax, qword [rax + 1 * rcx + 0x7fffffff]                       | 48 23 84 08 ff ff ff 7f                |
    | and rax, qword [rax + 1 * rcx - 0x7fffffff]                       | 48 23 84 08 01 00 00 80                |
    | and rax, qword [rax + 1 * rcx - 0x80000000]                       | 48 23 84 08 00 00 00 80                |
    | and rax, qword [r10 + 0x7f]                                       | 49 23 42 7f                            |
    | and rax, qword [r10 + 0x80]                                       | 49 23 82 80 00 00 00                   |
    | and rax, qword [r10 - 0x80]                                       | 49 23 42 80                            |
    | and rax, qword [r10 - 0x81]                                       | 49 23 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and rax, qword [rel @prev5]      | 90 90 90 90 90 48 23 05 f4 ff ff ff    |
    | .prev1: nop; and rax, qword [rel @prev1]                          | 90 48 23 05 f8 ff ff ff                |
    | and rax, qword [rel @next1]; nop; .next1: nop                     | 48 23 05 01 00 00 00 90 90             |
    | and rax, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 23 05 05 00 00 00 90 90 90 90 90 90 |
    | and rcx, qword [rdx]                                              | 48 23 0a                               |
    | and rdx, qword [rbx]                                              | 48 23 13                               |
    | and rbx, qword [rsp]                                              | 48 23 1c 24                            |
    | and rsp, qword [rbp]                                              | 48 23 65 00                            |
    | and rbp, qword [rsi]                                              | 48 23 2e                               |
    | and rsi, qword [rdi]                                              | 48 23 37                               |
    | and rdi, qword [r8]                                               | 49 23 38                               |
    | and r8, qword [r9]                                                | 4d 23 01                               |
    | and r9, qword [r10]                                               | 4d 23 0a                               |
    | and r10, qword [r11]                                              | 4d 23 13                               |
    | and r11, qword [r12]                                              | 4d 23 1c 24                            |
    | and r12, qword [r13]                                              | 4d 23 65 00                            |
    | and r13, qword [r14]                                              | 4d 23 2e                               |
    | and r14, qword [r15]                                              | 4d 23 37                               |
    | and r15, qword [rax + 1 * rcx]                                    | 4c 23 3c 08                            |
    | and rcx, qword [rdx + 1 * rcx]                                    | 48 23 0c 0a                            |
    | and rdx, qword [rbx + 1 * rcx]                                    | 48 23 14 0b                            |
    | and rbx, qword [rsp + 1 * rcx]                                    | 48 23 1c 0c                            |
    | and rsp, qword [rbp + 1 * rcx]                                    | 48 23 64 0d 00                         |
    | and rbp, qword [rsi + 1 * rcx]                                    | 48 23 2c 0e                            |
    | and rsi, qword [rdi + 1 * rcx]                                    | 48 23 34 0f                            |
    | and rdi, qword [r8 + 1 * rcx]                                     | 49 23 3c 08                            |
    | and r8, qword [r9 + 1 * rcx]                                      | 4d 23 04 09                            |
    | and r9, qword [r10 + 1 * rcx]                                     | 4d 23 0c 0a                            |
    | and r10, qword [r11 + 1 * rcx]                                    | 4d 23 14 0b                            |
    | and r11, qword [r12 + 1 * rcx]                                    | 4d 23 1c 0c                            |
    | and r12, qword [r13 + 1 * rcx]                                    | 4d 23 64 0d 00                         |
    | and r13, qword [r14 + 1 * rcx]                                    | 4d 23 2c 0e                            |
    | and r14, qword [r15 + 1 * rcx]                                    | 4d 23 34 0f                            |
    | and r15, qword [rax + 1 * rax]                                    | 4c 23 3c 00                            |
    | and rcx, qword [rax + 1 * rbx]                                    | 48 23 0c 18                            |
    | and rdx, qword [rax + 1 * rbp]                                    | 48 23 14 28                            |
    | and rbx, qword [rax + 1 * rsi]                                    | 48 23 1c 30                            |
    | and rsp, qword [rax + 1 * rdi]                                    | 48 23 24 38                            |
    | and rbp, qword [rax + 1 * r8]                                     | 4a 23 2c 00                            |
    | and rsi, qword [rax + 1 * r9]                                     | 4a 23 34 08                            |
    | and rdi, qword [rax + 1 * r10]                                    | 4a 23 3c 10                            |
    | and r8, qword [rax + 1 * r11]                                     | 4e 23 04 18                            |
    | and r9, qword [rax + 1 * r12]                                     | 4e 23 0c 20                            |
    | and r10, qword [rax + 1 * r13]                                    | 4e 23 14 28                            |
    | and r11, qword [rax + 1 * r14]                                    | 4e 23 1c 30                            |
    | and r12, qword [rax + 1 * r15]                                    | 4e 23 24 38                            |
    | and r13, qword [rax + 2 * rcx]                                    | 4c 23 2c 48                            |
    | and r14, qword [rax + 4 * rcx]                                    | 4c 23 34 88                            |
    | and r15, qword [rax + 8 * rcx]                                    | 4c 23 3c c8                            |
    | and rcx, qword [r8 + 2 * r9]                                      | 4b 23 0c 48                            |
    | and rdx, qword [r8 + 4 * r9]                                      | 4b 23 14 88                            |
    | and rbx, qword [r8 + 8 * r9]                                      | 4b 23 1c c8                            |
    | and rsp, qword [1 * rcx]                                          | 48 23 24 0d 00 00 00 00                |
    | and rbp, qword [2 * rcx]                                          | 48 23 2c 4d 00 00 00 00                |
    | and rsi, qword [4 * rcx]                                          | 48 23 34 8d 00 00 00 00                |
    | and rdi, qword [8 * rcx]                                          | 48 23 3c cd 00 00 00 00                |
    | and r8, qword [1 * r9]                                            | 4e 23 04 0d 00 00 00 00                |
    | and r9, qword [2 * r9]                                            | 4e 23 0c 4d 00 00 00 00                |
    | and r10, qword [4 * r9]                                           | 4e 23 14 8d 00 00 00 00                |
    | and r11, qword [8 * r9]                                           | 4e 23 1c cd 00 00 00 00                |
    | and r12, qword [r13 + 8 * r12]                                    | 4f 23 64 e5 00                         |
    | and r13, qword [rsp + 4 * r15]                                    | 4e 23 2c bc                            |
    | and r14, qword [rax + 1 * rcx + 0x00]                             | 4c 23 74 08 00                         |
    | and r15, qword [rax + 1 * rcx - 0x00]                             | 4c 23 7c 08 00                         |
    | and rcx, qword [rax + 1 * rcx - 0x01]                             | 48 23 4c 08 ff                         |
    | and rdx, qword [rax + 1 * rcx + 0x00000001]                       | 48 23 94 08 01 00 00 00                |
    | and rbx, qword [rax + 1 * rcx - 0x00000001]                       | 48 23 9c 08 ff ff ff ff                |
    | and rsp, qword [rax + 1 * rcx + 0x7f]                             | 48 23 64 08 7f                         |
    | and rbp, qword [rax + 1 * rcx - 0x7f]                             | 48 23 6c 08 81                         |
    | and rsi, qword [rax + 1 * rcx + 0x80]                             | 48 23 b4 08 80 00 00 00                |
    | and rdi, qword [rax + 1 * rcx - 0x80]                             | 48 23 7c 08 80                         |
    | and r8, qword [rax + 1 * rcx - 0x81]                              | 4c 23 84 08 7f ff ff ff                |
    | and r9, qword [rax + 1 * rcx + 0xff]                              | 4c 23 8c 08 ff 00 00 00                |
    | and r10, qword [rax + 1 * rcx - 0xff]                             | 4c 23 94 08 01 ff ff ff                |
    | and r11, qword [rax + 1 * rcx + 0x7fffffff]                       | 4c 23 9c 08 ff ff ff 7f                |
    | and r12, qword [rax + 1 * rcx - 0x7fffffff]                       | 4c 23 a4 08 01 00 00 80                |
    | and r13, qword [rax + 1 * rcx - 0x80000000]                       | 4c 23 ac 08 00 00 00 80                |
    | and r14, qword [r10 + 0x7f]                                       | 4d 23 72 7f                            |
    | and r15, qword [r10 + 0x80]                                       | 4d 23 ba 80 00 00 00                   |
    | and rcx, qword [r10 - 0x81]                                       | 49 23 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and rdx, qword [rel @prev5]      | 90 90 90 90 90 48 23 15 f4 ff ff ff    |
    | .prev1: nop; and rbx, qword [rel @prev1]                          | 90 48 23 1d f8 ff ff ff                |
    | and rsp, qword [rel @next1]; nop; .next1: nop                     | 48 23 25 01 00 00 00 90 90             |
    | and rbp, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 23 2d 05 00 00 00 90 90 90 90 90 90 |
    | and rsi, qword [rax]                                              | 48 23 30                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_and_reg64_addr64():
    encode(AND_REG64_ADDR64)


AND_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | and eax, 0x01  | 83 e0 01    | *** | and eax, 0x00  | 83 e0 00    |
    | and ecx, 0x01  | 83 e1 01    | *** | and eax, 0x7f  | 83 e0 7f    |
    | and edx, 0x01  | 83 e2 01    | *** | and eax, 0x80  | 83 e0 80    |
    | and ebx, 0x01  | 83 e3 01    | *** | and eax, 0xff  | 83 e0 ff    |
    | and esp, 0x01  | 83 e4 01    | *** | and ecx, 0x7f  | 83 e1 7f    |
    | and ebp, 0x01  | 83 e5 01    | *** | and edx, 0x80  | 83 e2 80    |
    | and esi, 0x01  | 83 e6 01    | *** | and ebx, 0xff  | 83 e3 ff    |
    | and edi, 0x01  | 83 e7 01    | *** | and esp, 0x00  | 83 e4 00    |
    | and r8d, 0x01  | 41 83 e0 01 | *** | and esi, 0x7f  | 83 e6 7f    |
    | and r9d, 0x01  | 41 83 e1 01 | *** | and edi, 0x80  | 83 e7 80    |
    | and r10d, 0x01 | 41 83 e2 01 | *** | and r8d, 0xff  | 41 83 e0 ff |
    | and r11d, 0x01 | 41 83 e3 01 | *** | and r9d, 0x00  | 41 83 e1 00 |
    | and r12d, 0x01 | 41 83 e4 01 | *** | and r11d, 0x7f | 41 83 e3 7f |
    | and r13d, 0x01 | 41 83 e5 01 | *** | and r12d, 0x80 | 41 83 e4 80 |
    | and r14d, 0x01 | 41 83 e6 01 | *** | and r13d, 0xff | 41 83 e5 ff |
    | and r15d, 0x01 | 41 83 e7 01 | *** | and r14d, 0x00 | 41 83 e6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_and_reg32_imm8():
    encode(AND_REG32_IMM8)


AND_REG32_IMM32 = """
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | instruction          | encoding             | *** | instruction          | encoding             |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | and eax, 0x00000001  | 25 01 00 00 00       | *** | and eax, 0x00007fff  | 25 ff 7f 00 00       |
    | and ecx, 0x00000001  | 81 e1 01 00 00 00    | *** | and eax, 0x00008000  | 25 00 80 00 00       |
    | and edx, 0x00000001  | 81 e2 01 00 00 00    | *** | and eax, 0x0000ffff  | 25 ff ff 00 00       |
    | and ebx, 0x00000001  | 81 e3 01 00 00 00    | *** | and eax, 0x00010000  | 25 00 00 01 00       |
    | and esp, 0x00000001  | 81 e4 01 00 00 00    | *** | and eax, 0x7fffffff  | 25 ff ff ff 7f       |
    | and ebp, 0x00000001  | 81 e5 01 00 00 00    | *** | and eax, 0x80000000  | 25 00 00 00 80       |
    | and esi, 0x00000001  | 81 e6 01 00 00 00    | *** | and eax, 0xffffffff  | 25 ff ff ff ff       |
    | and edi, 0x00000001  | 81 e7 01 00 00 00    | *** | and ecx, 0x0000007f  | 81 e1 7f 00 00 00    |
    | and r8d, 0x00000001  | 41 81 e0 01 00 00 00 | *** | and edx, 0x00000080  | 81 e2 80 00 00 00    |
    | and r9d, 0x00000001  | 41 81 e1 01 00 00 00 | *** | and ebx, 0x000000ff  | 81 e3 ff 00 00 00    |
    | and r10d, 0x00000001 | 41 81 e2 01 00 00 00 | *** | and esp, 0x00000100  | 81 e4 00 01 00 00    |
    | and r11d, 0x00000001 | 41 81 e3 01 00 00 00 | *** | and ebp, 0x00007fff  | 81 e5 ff 7f 00 00    |
    | and r12d, 0x00000001 | 41 81 e4 01 00 00 00 | *** | and esi, 0x00008000  | 81 e6 00 80 00 00    |
    | and r13d, 0x00000001 | 41 81 e5 01 00 00 00 | *** | and edi, 0x0000ffff  | 81 e7 ff ff 00 00    |
    | and r14d, 0x00000001 | 41 81 e6 01 00 00 00 | *** | and r8d, 0x00010000  | 41 81 e0 00 00 01 00 |
    | and r15d, 0x00000001 | 41 81 e7 01 00 00 00 | *** | and r9d, 0x7fffffff  | 41 81 e1 ff ff ff 7f |
    | and eax, 0x00000000  | 25 00 00 00 00       | *** | and r10d, 0x80000000 | 41 81 e2 00 00 00 80 |
    | and eax, 0x0000007f  | 25 7f 00 00 00       | *** | and r11d, 0xffffffff | 41 81 e3 ff ff ff ff |
    | and eax, 0x00000080  | 25 80 00 00 00       | *** | and r12d, 0x00000000 | 41 81 e4 00 00 00 00 |
    | and eax, 0x000000ff  | 25 ff 00 00 00       | *** | and r14d, 0x0000007f | 41 81 e6 7f 00 00 00 |
    | and eax, 0x00000100  | 25 00 01 00 00       | *** | and r15d, 0x00000080 | 41 81 e7 80 00 00 00 |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
"""


def can_encode_and_reg32_imm32():
    encode(AND_REG32_IMM32)


AND_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | and eax, ecx   | 21 c8    | *** | and eax, r8d   | 44 21 c0 |
    | and ecx, ecx   | 21 c9    | *** | and eax, r9d   | 44 21 c8 |
    | and edx, ecx   | 21 ca    | *** | and eax, r10d  | 44 21 d0 |
    | and ebx, ecx   | 21 cb    | *** | and eax, r11d  | 44 21 d8 |
    | and esp, ecx   | 21 cc    | *** | and eax, r12d  | 44 21 e0 |
    | and ebp, ecx   | 21 cd    | *** | and eax, r13d  | 44 21 e8 |
    | and esi, ecx   | 21 ce    | *** | and eax, r14d  | 44 21 f0 |
    | and edi, ecx   | 21 cf    | *** | and eax, r15d  | 44 21 f8 |
    | and r8d, ecx   | 41 21 c8 | *** | and ecx, edx   | 21 d1    |
    | and r9d, ecx   | 41 21 c9 | *** | and edx, ebx   | 21 da    |
    | and r10d, ecx  | 41 21 ca | *** | and ebx, esp   | 21 e3    |
    | and r11d, ecx  | 41 21 cb | *** | and esp, ebp   | 21 ec    |
    | and r12d, ecx  | 41 21 cc | *** | and ebp, esi   | 21 f5    |
    | and r13d, ecx  | 41 21 cd | *** | and esi, edi   | 21 fe    |
    | and r14d, ecx  | 41 21 ce | *** | and edi, r8d   | 44 21 c7 |
    | and r15d, ecx  | 41 21 cf | *** | and r8d, r9d   | 45 21 c8 |
    | and eax, eax   | 21 c0    | *** | and r9d, r10d  | 45 21 d1 |
    | and eax, edx   | 21 d0    | *** | and r10d, r11d | 45 21 da |
    | and eax, ebx   | 21 d8    | *** | and r11d, r12d | 45 21 e3 |
    | and eax, esp   | 21 e0    | *** | and r12d, r13d | 45 21 ec |
    | and eax, ebp   | 21 e8    | *** | and r13d, r14d | 45 21 f5 |
    | and eax, esi   | 21 f0    | *** | and r14d, r15d | 45 21 fe |
    | and eax, edi   | 21 f8    | *** | and r15d, eax  | 41 21 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_and_reg32_reg32():
    encode(AND_REG32_REG32)


AND_REG32_ADDR32 = """
    | ----------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                       | encoding                            |
    | ----------------------------------------------------------------- | ----------------------------------- |
    | and eax, dword [rcx]                                              | 23 01                               |
    | and ecx, dword [rcx]                                              | 23 09                               |
    | and edx, dword [rcx]                                              | 23 11                               |
    | and ebx, dword [rcx]                                              | 23 19                               |
    | and esp, dword [rcx]                                              | 23 21                               |
    | and ebp, dword [rcx]                                              | 23 29                               |
    | and esi, dword [rcx]                                              | 23 31                               |
    | and edi, dword [rcx]                                              | 23 39                               |
    | and r8d, dword [rcx]                                              | 44 23 01                            |
    | and r9d, dword [rcx]                                              | 44 23 09                            |
    | and r10d, dword [rcx]                                             | 44 23 11                            |
    | and r11d, dword [rcx]                                             | 44 23 19                            |
    | and r12d, dword [rcx]                                             | 44 23 21                            |
    | and r13d, dword [rcx]                                             | 44 23 29                            |
    | and r14d, dword [rcx]                                             | 44 23 31                            |
    | and r15d, dword [rcx]                                             | 44 23 39                            |
    | and eax, dword [rax]                                              | 23 00                               |
    | and eax, dword [rdx]                                              | 23 02                               |
    | and eax, dword [rbx]                                              | 23 03                               |
    | and eax, dword [rsp]                                              | 23 04 24                            |
    | and eax, dword [rbp]                                              | 23 45 00                            |
    | and eax, dword [rsi]                                              | 23 06                               |
    | and eax, dword [rdi]                                              | 23 07                               |
    | and eax, dword [r8]                                               | 41 23 00                            |
    | and eax, dword [r9]                                               | 41 23 01                            |
    | and eax, dword [r10]                                              | 41 23 02                            |
    | and eax, dword [r11]                                              | 41 23 03                            |
    | and eax, dword [r12]                                              | 41 23 04 24                         |
    | and eax, dword [r13]                                              | 41 23 45 00                         |
    | and eax, dword [r14]                                              | 41 23 06                            |
    | and eax, dword [r15]                                              | 41 23 07                            |
    | and eax, dword [rax + 1 * rcx]                                    | 23 04 08                            |
    | and eax, dword [rcx + 1 * rcx]                                    | 23 04 09                            |
    | and eax, dword [rdx + 1 * rcx]                                    | 23 04 0a                            |
    | and eax, dword [rbx + 1 * rcx]                                    | 23 04 0b                            |
    | and eax, dword [rsp + 1 * rcx]                                    | 23 04 0c                            |
    | and eax, dword [rbp + 1 * rcx]                                    | 23 44 0d 00                         |
    | and eax, dword [rsi + 1 * rcx]                                    | 23 04 0e                            |
    | and eax, dword [rdi + 1 * rcx]                                    | 23 04 0f                            |
    | and eax, dword [r8 + 1 * rcx]                                     | 41 23 04 08                         |
    | and eax, dword [r9 + 1 * rcx]                                     | 41 23 04 09                         |
    | and eax, dword [r10 + 1 * rcx]                                    | 41 23 04 0a                         |
    | and eax, dword [r11 + 1 * rcx]                                    | 41 23 04 0b                         |
    | and eax, dword [r12 + 1 * rcx]                                    | 41 23 04 0c                         |
    | and eax, dword [r13 + 1 * rcx]                                    | 41 23 44 0d 00                      |
    | and eax, dword [r14 + 1 * rcx]                                    | 41 23 04 0e                         |
    | and eax, dword [r15 + 1 * rcx]                                    | 41 23 04 0f                         |
    | and eax, dword [rax + 1 * rax]                                    | 23 04 00                            |
    | and eax, dword [rax + 1 * rdx]                                    | 23 04 10                            |
    | and eax, dword [rax + 1 * rbx]                                    | 23 04 18                            |
    | and eax, dword [rax + 1 * rbp]                                    | 23 04 28                            |
    | and eax, dword [rax + 1 * rsi]                                    | 23 04 30                            |
    | and eax, dword [rax + 1 * rdi]                                    | 23 04 38                            |
    | and eax, dword [rax + 1 * r8]                                     | 42 23 04 00                         |
    | and eax, dword [rax + 1 * r9]                                     | 42 23 04 08                         |
    | and eax, dword [rax + 1 * r10]                                    | 42 23 04 10                         |
    | and eax, dword [rax + 1 * r11]                                    | 42 23 04 18                         |
    | and eax, dword [rax + 1 * r12]                                    | 42 23 04 20                         |
    | and eax, dword [rax + 1 * r13]                                    | 42 23 04 28                         |
    | and eax, dword [rax + 1 * r14]                                    | 42 23 04 30                         |
    | and eax, dword [rax + 1 * r15]                                    | 42 23 04 38                         |
    | and eax, dword [rax + 2 * rcx]                                    | 23 04 48                            |
    | and eax, dword [rax + 4 * rcx]                                    | 23 04 88                            |
    | and eax, dword [rax + 8 * rcx]                                    | 23 04 c8                            |
    | and eax, dword [r8 + 1 * r9]                                      | 43 23 04 08                         |
    | and eax, dword [r8 + 2 * r9]                                      | 43 23 04 48                         |
    | and eax, dword [r8 + 4 * r9]                                      | 43 23 04 88                         |
    | and eax, dword [r8 + 8 * r9]                                      | 43 23 04 c8                         |
    | and eax, dword [1 * rcx]                                          | 23 04 0d 00 00 00 00                |
    | and eax, dword [2 * rcx]                                          | 23 04 4d 00 00 00 00                |
    | and eax, dword [4 * rcx]                                          | 23 04 8d 00 00 00 00                |
    | and eax, dword [8 * rcx]                                          | 23 04 cd 00 00 00 00                |
    | and eax, dword [1 * r9]                                           | 42 23 04 0d 00 00 00 00             |
    | and eax, dword [2 * r9]                                           | 42 23 04 4d 00 00 00 00             |
    | and eax, dword [4 * r9]                                           | 42 23 04 8d 00 00 00 00             |
    | and eax, dword [8 * r9]                                           | 42 23 04 cd 00 00 00 00             |
    | and eax, dword [r13 + 8 * r12]                                    | 43 23 44 e5 00                      |
    | and eax, dword [rsp + 4 * r15]                                    | 42 23 04 bc                         |
    | and eax, dword [rax + 1 * rcx + 0x00]                             | 23 44 08 00                         |
    | and eax, dword [rax + 1 * rcx - 0x00]                             | 23 44 08 00                         |
    | and eax, dword [rax + 1 * rcx + 0x01]                             | 23 44 08 01                         |
    | and eax, dword [rax + 1 * rcx - 0x01]                             | 23 44 08 ff                         |
    | and eax, dword [rax + 1 * rcx + 0x00000001]                       | 23 84 08 01 00 00 00                |
    | and eax, dword [rax + 1 * rcx - 0x00000001]                       | 23 84 08 ff ff ff ff                |
    | and eax, dword [rax + 1 * rcx + 0x7f]                             | 23 44 08 7f                         |
    | and eax, dword [rax + 1 * rcx - 0x7f]                             | 23 44 08 81                         |
    | and eax, dword [rax + 1 * rcx + 0x80]                             | 23 84 08 80 00 00 00                |
    | and eax, dword [rax + 1 * rcx - 0x80]                             | 23 44 08 80                         |
    | and eax, dword [rax + 1 * rcx - 0x81]                             | 23 84 08 7f ff ff ff                |
    | and eax, dword [rax + 1 * rcx + 0xff]                             | 23 84 08 ff 00 00 00                |
    | and eax, dword [rax + 1 * rcx - 0xff]                             | 23 84 08 01 ff ff ff                |
    | and eax, dword [rax + 1 * rcx + 0x7fffffff]                       | 23 84 08 ff ff ff 7f                |
    | and eax, dword [rax + 1 * rcx - 0x7fffffff]                       | 23 84 08 01 00 00 80                |
    | and eax, dword [rax + 1 * rcx - 0x80000000]                       | 23 84 08 00 00 00 80                |
    | and eax, dword [r10 + 0x7f]                                       | 41 23 42 7f                         |
    | and eax, dword [r10 + 0x80]                                       | 41 23 82 80 00 00 00                |
    | and eax, dword [r10 - 0x80]                                       | 41 23 42 80                         |
    | and eax, dword [r10 - 0x81]                                       | 41 23 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and eax, dword [rel @prev5]      | 90 90 90 90 90 23 05 f5 ff ff ff    |
    | .prev1: nop; and eax, dword [rel @prev1]                          | 90 23 05 f9 ff ff ff                |
    | and eax, dword [rel @next1]; nop; .next1: nop                     | 23 05 01 00 00 00 90 90             |
    | and eax, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 23 05 05 00 00 00 90 90 90 90 90 90 |
    | and ecx, dword [rdx]                                              | 23 0a                               |
    | and edx, dword [rbx]                                              | 23 13                               |
    | and ebx, dword [rsp]                                              | 23 1c 24                            |
    | and esp, dword [rbp]                                              | 23 65 00                            |
    | and ebp, dword [rsi]                                              | 23 2e                               |
    | and esi, dword [rdi]                                              | 23 37                               |
    | and edi, dword [r8]                                               | 41 23 38                            |
    | and r8d, dword [r9]                                               | 45 23 01                            |
    | and r9d, dword [r10]                                              | 45 23 0a                            |
    | and r10d, dword [r11]                                             | 45 23 13                            |
    | and r11d, dword [r12]                                             | 45 23 1c 24                         |
    | and r12d, dword [r13]                                             | 45 23 65 00                         |
    | and r13d, dword [r14]                                             | 45 23 2e                            |
    | and r14d, dword [r15]                                             | 45 23 37                            |
    | and r15d, dword [rax + 1 * rcx]                                   | 44 23 3c 08                         |
    | and ecx, dword [rdx + 1 * rcx]                                    | 23 0c 0a                            |
    | and edx, dword [rbx + 1 * rcx]                                    | 23 14 0b                            |
    | and ebx, dword [rsp + 1 * rcx]                                    | 23 1c 0c                            |
    | and esp, dword [rbp + 1 * rcx]                                    | 23 64 0d 00                         |
    | and ebp, dword [rsi + 1 * rcx]                                    | 23 2c 0e                            |
    | and esi, dword [rdi + 1 * rcx]                                    | 23 34 0f                            |
    | and edi, dword [r8 + 1 * rcx]                                     | 41 23 3c 08                         |
    | and r8d, dword [r9 + 1 * rcx]                                     | 45 23 04 09                         |
    | and r9d, dword [r10 + 1 * rcx]                                    | 45 23 0c 0a                         |
    | and r10d, dword [r11 + 1 * rcx]                                   | 45 23 14 0b                         |
    | and r11d, dword [r12 + 1 * rcx]                                   | 45 23 1c 0c                         |
    | and r12d, dword [r13 + 1 * rcx]                                   | 45 23 64 0d 00                      |
    | and r13d, dword [r14 + 1 * rcx]                                   | 45 23 2c 0e                         |
    | and r14d, dword [r15 + 1 * rcx]                                   | 45 23 34 0f                         |
    | and r15d, dword [rax + 1 * rax]                                   | 44 23 3c 00                         |
    | and ecx, dword [rax + 1 * rbx]                                    | 23 0c 18                            |
    | and edx, dword [rax + 1 * rbp]                                    | 23 14 28                            |
    | and ebx, dword [rax + 1 * rsi]                                    | 23 1c 30                            |
    | and esp, dword [rax + 1 * rdi]                                    | 23 24 38                            |
    | and ebp, dword [rax + 1 * r8]                                     | 42 23 2c 00                         |
    | and esi, dword [rax + 1 * r9]                                     | 42 23 34 08                         |
    | and edi, dword [rax + 1 * r10]                                    | 42 23 3c 10                         |
    | and r8d, dword [rax + 1 * r11]                                    | 46 23 04 18                         |
    | and r9d, dword [rax + 1 * r12]                                    | 46 23 0c 20                         |
    | and r10d, dword [rax + 1 * r13]                                   | 46 23 14 28                         |
    | and r11d, dword [rax + 1 * r14]                                   | 46 23 1c 30                         |
    | and r12d, dword [rax + 1 * r15]                                   | 46 23 24 38                         |
    | and r13d, dword [rax + 2 * rcx]                                   | 44 23 2c 48                         |
    | and r14d, dword [rax + 4 * rcx]                                   | 44 23 34 88                         |
    | and r15d, dword [rax + 8 * rcx]                                   | 44 23 3c c8                         |
    | and ecx, dword [r8 + 2 * r9]                                      | 43 23 0c 48                         |
    | and edx, dword [r8 + 4 * r9]                                      | 43 23 14 88                         |
    | and ebx, dword [r8 + 8 * r9]                                      | 43 23 1c c8                         |
    | and esp, dword [1 * rcx]                                          | 23 24 0d 00 00 00 00                |
    | and ebp, dword [2 * rcx]                                          | 23 2c 4d 00 00 00 00                |
    | and esi, dword [4 * rcx]                                          | 23 34 8d 00 00 00 00                |
    | and edi, dword [8 * rcx]                                          | 23 3c cd 00 00 00 00                |
    | and r8d, dword [1 * r9]                                           | 46 23 04 0d 00 00 00 00             |
    | and r9d, dword [2 * r9]                                           | 46 23 0c 4d 00 00 00 00             |
    | and r10d, dword [4 * r9]                                          | 46 23 14 8d 00 00 00 00             |
    | and r11d, dword [8 * r9]                                          | 46 23 1c cd 00 00 00 00             |
    | and r12d, dword [r13 + 8 * r12]                                   | 47 23 64 e5 00                      |
    | and r13d, dword [rsp + 4 * r15]                                   | 46 23 2c bc                         |
    | and r14d, dword [rax + 1 * rcx + 0x00]                            | 44 23 74 08 00                      |
    | and r15d, dword [rax + 1 * rcx - 0x00]                            | 44 23 7c 08 00                      |
    | and ecx, dword [rax + 1 * rcx - 0x01]                             | 23 4c 08 ff                         |
    | and edx, dword [rax + 1 * rcx + 0x00000001]                       | 23 94 08 01 00 00 00                |
    | and ebx, dword [rax + 1 * rcx - 0x00000001]                       | 23 9c 08 ff ff ff ff                |
    | and esp, dword [rax + 1 * rcx + 0x7f]                             | 23 64 08 7f                         |
    | and ebp, dword [rax + 1 * rcx - 0x7f]                             | 23 6c 08 81                         |
    | and esi, dword [rax + 1 * rcx + 0x80]                             | 23 b4 08 80 00 00 00                |
    | and edi, dword [rax + 1 * rcx - 0x80]                             | 23 7c 08 80                         |
    | and r8d, dword [rax + 1 * rcx - 0x81]                             | 44 23 84 08 7f ff ff ff             |
    | and r9d, dword [rax + 1 * rcx + 0xff]                             | 44 23 8c 08 ff 00 00 00             |
    | and r10d, dword [rax + 1 * rcx - 0xff]                            | 44 23 94 08 01 ff ff ff             |
    | and r11d, dword [rax + 1 * rcx + 0x7fffffff]                      | 44 23 9c 08 ff ff ff 7f             |
    | and r12d, dword [rax + 1 * rcx - 0x7fffffff]                      | 44 23 a4 08 01 00 00 80             |
    | and r13d, dword [rax + 1 * rcx - 0x80000000]                      | 44 23 ac 08 00 00 00 80             |
    | and r14d, dword [r10 + 0x7f]                                      | 45 23 72 7f                         |
    | and r15d, dword [r10 + 0x80]                                      | 45 23 ba 80 00 00 00                |
    | and ecx, dword [r10 - 0x81]                                       | 41 23 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and edx, dword [rel @prev5]      | 90 90 90 90 90 23 15 f5 ff ff ff    |
    | .prev1: nop; and ebx, dword [rel @prev1]                          | 90 23 1d f9 ff ff ff                |
    | and esp, dword [rel @next1]; nop; .next1: nop                     | 23 25 01 00 00 00 90 90             |
    | and ebp, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 23 2d 05 00 00 00 90 90 90 90 90 90 |
    | and esi, dword [rax]                                              | 23 30                               |
    | ----------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_and_reg32_addr32():
    encode(AND_REG32_ADDR32)


AND_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | and ax, 0x01   | 66 83 e0 01    | *** | and ax, 0x00   | 66 83 e0 00    |
    | and cx, 0x01   | 66 83 e1 01    | *** | and ax, 0x7f   | 66 83 e0 7f    |
    | and dx, 0x01   | 66 83 e2 01    | *** | and ax, 0x80   | 66 83 e0 80    |
    | and bx, 0x01   | 66 83 e3 01    | *** | and ax, 0xff   | 66 83 e0 ff    |
    | and sp, 0x01   | 66 83 e4 01    | *** | and cx, 0x7f   | 66 83 e1 7f    |
    | and bp, 0x01   | 66 83 e5 01    | *** | and dx, 0x80   | 66 83 e2 80    |
    | and si, 0x01   | 66 83 e6 01    | *** | and bx, 0xff   | 66 83 e3 ff    |
    | and di, 0x01   | 66 83 e7 01    | *** | and sp, 0x00   | 66 83 e4 00    |
    | and r8w, 0x01  | 66 41 83 e0 01 | *** | and si, 0x7f   | 66 83 e6 7f    |
    | and r9w, 0x01  | 66 41 83 e1 01 | *** | and di, 0x80   | 66 83 e7 80    |
    | and r10w, 0x01 | 66 41 83 e2 01 | *** | and r8w, 0xff  | 66 41 83 e0 ff |
    | and r11w, 0x01 | 66 41 83 e3 01 | *** | and r9w, 0x00  | 66 41 83 e1 00 |
    | and r12w, 0x01 | 66 41 83 e4 01 | *** | and r11w, 0x7f | 66 41 83 e3 7f |
    | and r13w, 0x01 | 66 41 83 e5 01 | *** | and r12w, 0x80 | 66 41 83 e4 80 |
    | and r14w, 0x01 | 66 41 83 e6 01 | *** | and r13w, 0xff | 66 41 83 e5 ff |
    | and r15w, 0x01 | 66 41 83 e7 01 | *** | and r14w, 0x00 | 66 41 83 e6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_and_reg16_imm8():
    encode(AND_REG16_IMM8)


AND_REG16_IMM16 = """
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | instruction      | encoding          | *** | instruction      | encoding          |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | and ax, 0x0001   | 66 25 01 00       | *** | and ax, 0x00ff   | 66 25 ff 00       |
    | and cx, 0x0001   | 66 81 e1 01 00    | *** | and ax, 0x0100   | 66 25 00 01       |
    | and dx, 0x0001   | 66 81 e2 01 00    | *** | and ax, 0x7fff   | 66 25 ff 7f       |
    | and bx, 0x0001   | 66 81 e3 01 00    | *** | and ax, 0x8000   | 66 25 00 80       |
    | and sp, 0x0001   | 66 81 e4 01 00    | *** | and ax, 0xffff   | 66 25 ff ff       |
    | and bp, 0x0001   | 66 81 e5 01 00    | *** | and cx, 0x007f   | 66 81 e1 7f 00    |
    | and si, 0x0001   | 66 81 e6 01 00    | *** | and dx, 0x0080   | 66 81 e2 80 00    |
    | and di, 0x0001   | 66 81 e7 01 00    | *** | and bx, 0x00ff   | 66 81 e3 ff 00    |
    | and r8w, 0x0001  | 66 41 81 e0 01 00 | *** | and sp, 0x0100   | 66 81 e4 00 01    |
    | and r9w, 0x0001  | 66 41 81 e1 01 00 | *** | and bp, 0x7fff   | 66 81 e5 ff 7f    |
    | and r10w, 0x0001 | 66 41 81 e2 01 00 | *** | and si, 0x8000   | 66 81 e6 00 80    |
    | and r11w, 0x0001 | 66 41 81 e3 01 00 | *** | and di, 0xffff   | 66 81 e7 ff ff    |
    | and r12w, 0x0001 | 66 41 81 e4 01 00 | *** | and r8w, 0x0000  | 66 41 81 e0 00 00 |
    | and r13w, 0x0001 | 66 41 81 e5 01 00 | *** | and r10w, 0x007f | 66 41 81 e2 7f 00 |
    | and r14w, 0x0001 | 66 41 81 e6 01 00 | *** | and r11w, 0x0080 | 66 41 81 e3 80 00 |
    | and r15w, 0x0001 | 66 41 81 e7 01 00 | *** | and r12w, 0x00ff | 66 41 81 e4 ff 00 |
    | and ax, 0x0000   | 66 25 00 00       | *** | and r13w, 0x0100 | 66 41 81 e5 00 01 |
    | and ax, 0x007f   | 66 25 7f 00       | *** | and r14w, 0x7fff | 66 41 81 e6 ff 7f |
    | and ax, 0x0080   | 66 25 80 00       | *** | and r15w, 0x8000 | 66 41 81 e7 00 80 |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
"""


def can_encode_and_reg16_imm16():
    encode(AND_REG16_IMM16)


AND_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | and ax, cx     | 66 21 c8    | *** | and ax, r8w    | 66 44 21 c0 |
    | and cx, cx     | 66 21 c9    | *** | and ax, r9w    | 66 44 21 c8 |
    | and dx, cx     | 66 21 ca    | *** | and ax, r10w   | 66 44 21 d0 |
    | and bx, cx     | 66 21 cb    | *** | and ax, r11w   | 66 44 21 d8 |
    | and sp, cx     | 66 21 cc    | *** | and ax, r12w   | 66 44 21 e0 |
    | and bp, cx     | 66 21 cd    | *** | and ax, r13w   | 66 44 21 e8 |
    | and si, cx     | 66 21 ce    | *** | and ax, r14w   | 66 44 21 f0 |
    | and di, cx     | 66 21 cf    | *** | and ax, r15w   | 66 44 21 f8 |
    | and r8w, cx    | 66 41 21 c8 | *** | and cx, dx     | 66 21 d1    |
    | and r9w, cx    | 66 41 21 c9 | *** | and dx, bx     | 66 21 da    |
    | and r10w, cx   | 66 41 21 ca | *** | and bx, sp     | 66 21 e3    |
    | and r11w, cx   | 66 41 21 cb | *** | and sp, bp     | 66 21 ec    |
    | and r12w, cx   | 66 41 21 cc | *** | and bp, si     | 66 21 f5    |
    | and r13w, cx   | 66 41 21 cd | *** | and si, di     | 66 21 fe    |
    | and r14w, cx   | 66 41 21 ce | *** | and di, r8w    | 66 44 21 c7 |
    | and r15w, cx   | 66 41 21 cf | *** | and r8w, r9w   | 66 45 21 c8 |
    | and ax, ax     | 66 21 c0    | *** | and r9w, r10w  | 66 45 21 d1 |
    | and ax, dx     | 66 21 d0    | *** | and r10w, r11w | 66 45 21 da |
    | and ax, bx     | 66 21 d8    | *** | and r11w, r12w | 66 45 21 e3 |
    | and ax, sp     | 66 21 e0    | *** | and r12w, r13w | 66 45 21 ec |
    | and ax, bp     | 66 21 e8    | *** | and r13w, r14w | 66 45 21 f5 |
    | and ax, si     | 66 21 f0    | *** | and r14w, r15w | 66 45 21 fe |
    | and ax, di     | 66 21 f8    | *** | and r15w, ax   | 66 41 21 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_and_reg16_reg16():
    encode(AND_REG16_REG16)


AND_REG16_ADDR16 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | and ax, word [rcx]                                              | 66 23 01                               |
    | and cx, word [rcx]                                              | 66 23 09                               |
    | and dx, word [rcx]                                              | 66 23 11                               |
    | and bx, word [rcx]                                              | 66 23 19                               |
    | and sp, word [rcx]                                              | 66 23 21                               |
    | and bp, word [rcx]                                              | 66 23 29                               |
    | and si, word [rcx]                                              | 66 23 31                               |
    | and di, word [rcx]                                              | 66 23 39                               |
    | and r8w, word [rcx]                                             | 66 44 23 01                            |
    | and r9w, word [rcx]                                             | 66 44 23 09                            |
    | and r10w, word [rcx]                                            | 66 44 23 11                            |
    | and r11w, word [rcx]                                            | 66 44 23 19                            |
    | and r12w, word [rcx]                                            | 66 44 23 21                            |
    | and r13w, word [rcx]                                            | 66 44 23 29                            |
    | and r14w, word [rcx]                                            | 66 44 23 31                            |
    | and r15w, word [rcx]                                            | 66 44 23 39                            |
    | and ax, word [rax]                                              | 66 23 00                               |
    | and ax, word [rdx]                                              | 66 23 02                               |
    | and ax, word [rbx]                                              | 66 23 03                               |
    | and ax, word [rsp]                                              | 66 23 04 24                            |
    | and ax, word [rbp]                                              | 66 23 45 00                            |
    | and ax, word [rsi]                                              | 66 23 06                               |
    | and ax, word [rdi]                                              | 66 23 07                               |
    | and ax, word [r8]                                               | 66 41 23 00                            |
    | and ax, word [r9]                                               | 66 41 23 01                            |
    | and ax, word [r10]                                              | 66 41 23 02                            |
    | and ax, word [r11]                                              | 66 41 23 03                            |
    | and ax, word [r12]                                              | 66 41 23 04 24                         |
    | and ax, word [r13]                                              | 66 41 23 45 00                         |
    | and ax, word [r14]                                              | 66 41 23 06                            |
    | and ax, word [r15]                                              | 66 41 23 07                            |
    | and ax, word [rax + 1 * rcx]                                    | 66 23 04 08                            |
    | and ax, word [rcx + 1 * rcx]                                    | 66 23 04 09                            |
    | and ax, word [rdx + 1 * rcx]                                    | 66 23 04 0a                            |
    | and ax, word [rbx + 1 * rcx]                                    | 66 23 04 0b                            |
    | and ax, word [rsp + 1 * rcx]                                    | 66 23 04 0c                            |
    | and ax, word [rbp + 1 * rcx]                                    | 66 23 44 0d 00                         |
    | and ax, word [rsi + 1 * rcx]                                    | 66 23 04 0e                            |
    | and ax, word [rdi + 1 * rcx]                                    | 66 23 04 0f                            |
    | and ax, word [r8 + 1 * rcx]                                     | 66 41 23 04 08                         |
    | and ax, word [r9 + 1 * rcx]                                     | 66 41 23 04 09                         |
    | and ax, word [r10 + 1 * rcx]                                    | 66 41 23 04 0a                         |
    | and ax, word [r11 + 1 * rcx]                                    | 66 41 23 04 0b                         |
    | and ax, word [r12 + 1 * rcx]                                    | 66 41 23 04 0c                         |
    | and ax, word [r13 + 1 * rcx]                                    | 66 41 23 44 0d 00                      |
    | and ax, word [r14 + 1 * rcx]                                    | 66 41 23 04 0e                         |
    | and ax, word [r15 + 1 * rcx]                                    | 66 41 23 04 0f                         |
    | and ax, word [rax + 1 * rax]                                    | 66 23 04 00                            |
    | and ax, word [rax + 1 * rdx]                                    | 66 23 04 10                            |
    | and ax, word [rax + 1 * rbx]                                    | 66 23 04 18                            |
    | and ax, word [rax + 1 * rbp]                                    | 66 23 04 28                            |
    | and ax, word [rax + 1 * rsi]                                    | 66 23 04 30                            |
    | and ax, word [rax + 1 * rdi]                                    | 66 23 04 38                            |
    | and ax, word [rax + 1 * r8]                                     | 66 42 23 04 00                         |
    | and ax, word [rax + 1 * r9]                                     | 66 42 23 04 08                         |
    | and ax, word [rax + 1 * r10]                                    | 66 42 23 04 10                         |
    | and ax, word [rax + 1 * r11]                                    | 66 42 23 04 18                         |
    | and ax, word [rax + 1 * r12]                                    | 66 42 23 04 20                         |
    | and ax, word [rax + 1 * r13]                                    | 66 42 23 04 28                         |
    | and ax, word [rax + 1 * r14]                                    | 66 42 23 04 30                         |
    | and ax, word [rax + 1 * r15]                                    | 66 42 23 04 38                         |
    | and ax, word [rax + 2 * rcx]                                    | 66 23 04 48                            |
    | and ax, word [rax + 4 * rcx]                                    | 66 23 04 88                            |
    | and ax, word [rax + 8 * rcx]                                    | 66 23 04 c8                            |
    | and ax, word [r8 + 1 * r9]                                      | 66 43 23 04 08                         |
    | and ax, word [r8 + 2 * r9]                                      | 66 43 23 04 48                         |
    | and ax, word [r8 + 4 * r9]                                      | 66 43 23 04 88                         |
    | and ax, word [r8 + 8 * r9]                                      | 66 43 23 04 c8                         |
    | and ax, word [1 * rcx]                                          | 66 23 04 0d 00 00 00 00                |
    | and ax, word [2 * rcx]                                          | 66 23 04 4d 00 00 00 00                |
    | and ax, word [4 * rcx]                                          | 66 23 04 8d 00 00 00 00                |
    | and ax, word [8 * rcx]                                          | 66 23 04 cd 00 00 00 00                |
    | and ax, word [1 * r9]                                           | 66 42 23 04 0d 00 00 00 00             |
    | and ax, word [2 * r9]                                           | 66 42 23 04 4d 00 00 00 00             |
    | and ax, word [4 * r9]                                           | 66 42 23 04 8d 00 00 00 00             |
    | and ax, word [8 * r9]                                           | 66 42 23 04 cd 00 00 00 00             |
    | and ax, word [r13 + 8 * r12]                                    | 66 43 23 44 e5 00                      |
    | and ax, word [rsp + 4 * r15]                                    | 66 42 23 04 bc                         |
    | and ax, word [rax + 1 * rcx + 0x00]                             | 66 23 44 08 00                         |
    | and ax, word [rax + 1 * rcx - 0x00]                             | 66 23 44 08 00                         |
    | and ax, word [rax + 1 * rcx + 0x01]                             | 66 23 44 08 01                         |
    | and ax, word [rax + 1 * rcx - 0x01]                             | 66 23 44 08 ff                         |
    | and ax, word [rax + 1 * rcx + 0x00000001]                       | 66 23 84 08 01 00 00 00                |
    | and ax, word [rax + 1 * rcx - 0x00000001]                       | 66 23 84 08 ff ff ff ff                |
    | and ax, word [rax + 1 * rcx + 0x7f]                             | 66 23 44 08 7f                         |
    | and ax, word [rax + 1 * rcx - 0x7f]                             | 66 23 44 08 81                         |
    | and ax, word [rax + 1 * rcx + 0x80]                             | 66 23 84 08 80 00 00 00                |
    | and ax, word [rax + 1 * rcx - 0x80]                             | 66 23 44 08 80                         |
    | and ax, word [rax + 1 * rcx - 0x81]                             | 66 23 84 08 7f ff ff ff                |
    | and ax, word [rax + 1 * rcx + 0xff]                             | 66 23 84 08 ff 00 00 00                |
    | and ax, word [rax + 1 * rcx - 0xff]                             | 66 23 84 08 01 ff ff ff                |
    | and ax, word [rax + 1 * rcx + 0x7fffffff]                       | 66 23 84 08 ff ff ff 7f                |
    | and ax, word [rax + 1 * rcx - 0x7fffffff]                       | 66 23 84 08 01 00 00 80                |
    | and ax, word [rax + 1 * rcx - 0x80000000]                       | 66 23 84 08 00 00 00 80                |
    | and ax, word [r10 + 0x7f]                                       | 66 41 23 42 7f                         |
    | and ax, word [r10 + 0x80]                                       | 66 41 23 82 80 00 00 00                |
    | and ax, word [r10 - 0x80]                                       | 66 41 23 42 80                         |
    | and ax, word [r10 - 0x81]                                       | 66 41 23 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and ax, word [rel @prev5]      | 90 90 90 90 90 66 23 05 f4 ff ff ff    |
    | .prev1: nop; and ax, word [rel @prev1]                          | 90 66 23 05 f8 ff ff ff                |
    | and ax, word [rel @next1]; nop; .next1: nop                     | 66 23 05 01 00 00 00 90 90             |
    | and ax, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 23 05 05 00 00 00 90 90 90 90 90 90 |
    | and cx, word [rdx]                                              | 66 23 0a                               |
    | and dx, word [rbx]                                              | 66 23 13                               |
    | and bx, word [rsp]                                              | 66 23 1c 24                            |
    | and sp, word [rbp]                                              | 66 23 65 00                            |
    | and bp, word [rsi]                                              | 66 23 2e                               |
    | and si, word [rdi]                                              | 66 23 37                               |
    | and di, word [r8]                                               | 66 41 23 38                            |
    | and r8w, word [r9]                                              | 66 45 23 01                            |
    | and r9w, word [r10]                                             | 66 45 23 0a                            |
    | and r10w, word [r11]                                            | 66 45 23 13                            |
    | and r11w, word [r12]                                            | 66 45 23 1c 24                         |
    | and r12w, word [r13]                                            | 66 45 23 65 00                         |
    | and r13w, word [r14]                                            | 66 45 23 2e                            |
    | and r14w, word [r15]                                            | 66 45 23 37                            |
    | and r15w, word [rax + 1 * rcx]                                  | 66 44 23 3c 08                         |
    | and cx, word [rdx + 1 * rcx]                                    | 66 23 0c 0a                            |
    | and dx, word [rbx + 1 * rcx]                                    | 66 23 14 0b                            |
    | and bx, word [rsp + 1 * rcx]                                    | 66 23 1c 0c                            |
    | and sp, word [rbp + 1 * rcx]                                    | 66 23 64 0d 00                         |
    | and bp, word [rsi + 1 * rcx]                                    | 66 23 2c 0e                            |
    | and si, word [rdi + 1 * rcx]                                    | 66 23 34 0f                            |
    | and di, word [r8 + 1 * rcx]                                     | 66 41 23 3c 08                         |
    | and r8w, word [r9 + 1 * rcx]                                    | 66 45 23 04 09                         |
    | and r9w, word [r10 + 1 * rcx]                                   | 66 45 23 0c 0a                         |
    | and r10w, word [r11 + 1 * rcx]                                  | 66 45 23 14 0b                         |
    | and r11w, word [r12 + 1 * rcx]                                  | 66 45 23 1c 0c                         |
    | and r12w, word [r13 + 1 * rcx]                                  | 66 45 23 64 0d 00                      |
    | and r13w, word [r14 + 1 * rcx]                                  | 66 45 23 2c 0e                         |
    | and r14w, word [r15 + 1 * rcx]                                  | 66 45 23 34 0f                         |
    | and r15w, word [rax + 1 * rax]                                  | 66 44 23 3c 00                         |
    | and cx, word [rax + 1 * rbx]                                    | 66 23 0c 18                            |
    | and dx, word [rax + 1 * rbp]                                    | 66 23 14 28                            |
    | and bx, word [rax + 1 * rsi]                                    | 66 23 1c 30                            |
    | and sp, word [rax + 1 * rdi]                                    | 66 23 24 38                            |
    | and bp, word [rax + 1 * r8]                                     | 66 42 23 2c 00                         |
    | and si, word [rax + 1 * r9]                                     | 66 42 23 34 08                         |
    | and di, word [rax + 1 * r10]                                    | 66 42 23 3c 10                         |
    | and r8w, word [rax + 1 * r11]                                   | 66 46 23 04 18                         |
    | and r9w, word [rax + 1 * r12]                                   | 66 46 23 0c 20                         |
    | and r10w, word [rax + 1 * r13]                                  | 66 46 23 14 28                         |
    | and r11w, word [rax + 1 * r14]                                  | 66 46 23 1c 30                         |
    | and r12w, word [rax + 1 * r15]                                  | 66 46 23 24 38                         |
    | and r13w, word [rax + 2 * rcx]                                  | 66 44 23 2c 48                         |
    | and r14w, word [rax + 4 * rcx]                                  | 66 44 23 34 88                         |
    | and r15w, word [rax + 8 * rcx]                                  | 66 44 23 3c c8                         |
    | and cx, word [r8 + 2 * r9]                                      | 66 43 23 0c 48                         |
    | and dx, word [r8 + 4 * r9]                                      | 66 43 23 14 88                         |
    | and bx, word [r8 + 8 * r9]                                      | 66 43 23 1c c8                         |
    | and sp, word [1 * rcx]                                          | 66 23 24 0d 00 00 00 00                |
    | and bp, word [2 * rcx]                                          | 66 23 2c 4d 00 00 00 00                |
    | and si, word [4 * rcx]                                          | 66 23 34 8d 00 00 00 00                |
    | and di, word [8 * rcx]                                          | 66 23 3c cd 00 00 00 00                |
    | and r8w, word [1 * r9]                                          | 66 46 23 04 0d 00 00 00 00             |
    | and r9w, word [2 * r9]                                          | 66 46 23 0c 4d 00 00 00 00             |
    | and r10w, word [4 * r9]                                         | 66 46 23 14 8d 00 00 00 00             |
    | and r11w, word [8 * r9]                                         | 66 46 23 1c cd 00 00 00 00             |
    | and r12w, word [r13 + 8 * r12]                                  | 66 47 23 64 e5 00                      |
    | and r13w, word [rsp + 4 * r15]                                  | 66 46 23 2c bc                         |
    | and r14w, word [rax + 1 * rcx + 0x00]                           | 66 44 23 74 08 00                      |
    | and r15w, word [rax + 1 * rcx - 0x00]                           | 66 44 23 7c 08 00                      |
    | and cx, word [rax + 1 * rcx - 0x01]                             | 66 23 4c 08 ff                         |
    | and dx, word [rax + 1 * rcx + 0x00000001]                       | 66 23 94 08 01 00 00 00                |
    | and bx, word [rax + 1 * rcx - 0x00000001]                       | 66 23 9c 08 ff ff ff ff                |
    | and sp, word [rax + 1 * rcx + 0x7f]                             | 66 23 64 08 7f                         |
    | and bp, word [rax + 1 * rcx - 0x7f]                             | 66 23 6c 08 81                         |
    | and si, word [rax + 1 * rcx + 0x80]                             | 66 23 b4 08 80 00 00 00                |
    | and di, word [rax + 1 * rcx - 0x80]                             | 66 23 7c 08 80                         |
    | and r8w, word [rax + 1 * rcx - 0x81]                            | 66 44 23 84 08 7f ff ff ff             |
    | and r9w, word [rax + 1 * rcx + 0xff]                            | 66 44 23 8c 08 ff 00 00 00             |
    | and r10w, word [rax + 1 * rcx - 0xff]                           | 66 44 23 94 08 01 ff ff ff             |
    | and r11w, word [rax + 1 * rcx + 0x7fffffff]                     | 66 44 23 9c 08 ff ff ff 7f             |
    | and r12w, word [rax + 1 * rcx - 0x7fffffff]                     | 66 44 23 a4 08 01 00 00 80             |
    | and r13w, word [rax + 1 * rcx - 0x80000000]                     | 66 44 23 ac 08 00 00 00 80             |
    | and r14w, word [r10 + 0x7f]                                     | 66 45 23 72 7f                         |
    | and r15w, word [r10 + 0x80]                                     | 66 45 23 ba 80 00 00 00                |
    | and cx, word [r10 - 0x81]                                       | 66 41 23 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and dx, word [rel @prev5]      | 90 90 90 90 90 66 23 15 f4 ff ff ff    |
    | .prev1: nop; and bx, word [rel @prev1]                          | 90 66 23 1d f8 ff ff ff                |
    | and sp, word [rel @next1]; nop; .next1: nop                     | 66 23 25 01 00 00 00 90 90             |
    | and bp, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 23 2d 05 00 00 00 90 90 90 90 90 90 |
    | and si, word [rax]                                              | 66 23 30                               |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_and_reg16_addr16():
    encode(AND_REG16_ADDR16)


AND_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | and al, 0x01   | 24 01       | *** | and al, 0x00   | 24 00       |
    | and cl, 0x01   | 80 e1 01    | *** | and al, 0x7f   | 24 7f       |
    | and dl, 0x01   | 80 e2 01    | *** | and al, 0x80   | 24 80       |
    | and bl, 0x01   | 80 e3 01    | *** | and al, 0xff   | 24 ff       |
    | and spl, 0x01  | 40 80 e4 01 | *** | and cl, 0x7f   | 80 e1 7f    |
    | and bpl, 0x01  | 40 80 e5 01 | *** | and dl, 0x80   | 80 e2 80    |
    | and sil, 0x01  | 40 80 e6 01 | *** | and bl, 0xff   | 80 e3 ff    |
    | and dil, 0x01  | 40 80 e7 01 | *** | and spl, 0x00  | 40 80 e4 00 |
    | and r8b, 0x01  | 41 80 e0 01 | *** | and sil, 0x7f  | 40 80 e6 7f |
    | and r9b, 0x01  | 41 80 e1 01 | *** | and dil, 0x80  | 40 80 e7 80 |
    | and r10b, 0x01 | 41 80 e2 01 | *** | and r8b, 0xff  | 41 80 e0 ff |
    | and r11b, 0x01 | 41 80 e3 01 | *** | and r9b, 0x00  | 41 80 e1 00 |
    | and r12b, 0x01 | 41 80 e4 01 | *** | and r11b, 0x7f | 41 80 e3 7f |
    | and r13b, 0x01 | 41 80 e5 01 | *** | and r12b, 0x80 | 41 80 e4 80 |
    | and r14b, 0x01 | 41 80 e6 01 | *** | and r13b, 0xff | 41 80 e5 ff |
    | and r15b, 0x01 | 41 80 e7 01 | *** | and r14b, 0x00 | 41 80 e6 00 |
    | and ah, 0x01   | 80 e4 01    | *** | and ah, 0x7f   | 80 e4 7f    |
    | and ch, 0x01   | 80 e5 01    | *** | and ch, 0x80   | 80 e5 80    |
    | and dh, 0x01   | 80 e6 01    | *** | and dh, 0xff   | 80 e6 ff    |
    | and bh, 0x01   | 80 e7 01    | *** | and bh, 0x00   | 80 e7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_and_reg8_imm8():
    encode(AND_REG8_IMM8)


AND_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | and al, cl     | 20 c8    | *** | and al, r10b   | 44 20 d0 |
    | and cl, cl     | 20 c9    | *** | and al, r11b   | 44 20 d8 |
    | and dl, cl     | 20 ca    | *** | and al, r12b   | 44 20 e0 |
    | and bl, cl     | 20 cb    | *** | and al, r13b   | 44 20 e8 |
    | and spl, cl    | 40 20 cc | *** | and al, r14b   | 44 20 f0 |
    | and bpl, cl    | 40 20 cd | *** | and al, r15b   | 44 20 f8 |
    | and sil, cl    | 40 20 ce | *** | and al, ah     | 20 e0    |
    | and dil, cl    | 40 20 cf | *** | and al, ch     | 20 e8    |
    | and r8b, cl    | 41 20 c8 | *** | and al, dh     | 20 f0    |
    | and r9b, cl    | 41 20 c9 | *** | and al, bh     | 20 f8    |
    | and r10b, cl   | 41 20 ca | *** | and cl, dl     | 20 d1    |
    | and r11b, cl   | 41 20 cb | *** | and dl, bl     | 20 da    |
    | and r12b, cl   | 41 20 cc | *** | and bl, spl    | 40 20 e3 |
    | and r13b, cl   | 41 20 cd | *** | and spl, bpl   | 40 20 ec |
    | and r14b, cl   | 41 20 ce | *** | and bpl, sil   | 40 20 f5 |
    | and r15b, cl   | 41 20 cf | *** | and sil, dil   | 40 20 fe |
    | and ah, cl     | 20 cc    | *** | and dil, r8b   | 44 20 c7 |
    | and ch, cl     | 20 cd    | *** | and r8b, r9b   | 45 20 c8 |
    | and dh, cl     | 20 ce    | *** | and r9b, r10b  | 45 20 d1 |
    | and bh, cl     | 20 cf    | *** | and r10b, r11b | 45 20 da |
    | and al, al     | 20 c0    | *** | and r11b, r12b | 45 20 e3 |
    | and al, dl     | 20 d0    | *** | and r12b, r13b | 45 20 ec |
    | and al, bl     | 20 d8    | *** | and r13b, r14b | 45 20 f5 |
    | and al, spl    | 40 20 e0 | *** | and r14b, r15b | 45 20 fe |
    | and al, bpl    | 40 20 e8 | *** | and r15b, ah   | !! !! !! |
    | and al, sil    | 40 20 f0 | *** | and ah, ch     | 20 ec    |
    | and al, dil    | 40 20 f8 | *** | and ch, dh     | 20 f5    |
    | and al, r8b    | 44 20 c0 | *** | and dh, bh     | 20 fe    |
    | and al, r9b    | 44 20 c8 | *** | and bh, al     | 20 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_and_reg8_reg8():
    encode(AND_REG8_REG8)


AND_REG8_ADDR8 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | and al, byte [rcx]                                               | 22 01                                  |
    | and cl, byte [rcx]                                               | 22 09                                  |
    | and dl, byte [rcx]                                               | 22 11                                  |
    | and bl, byte [rcx]                                               | 22 19                                  |
    | and spl, byte [rcx]                                              | 40 22 21                               |
    | and bpl, byte [rcx]                                              | 40 22 29                               |
    | and sil, byte [rcx]                                              | 40 22 31                               |
    | and dil, byte [rcx]                                              | 40 22 39                               |
    | and r8b, byte [rcx]                                              | 44 22 01                               |
    | and r9b, byte [rcx]                                              | 44 22 09                               |
    | and r10b, byte [rcx]                                             | 44 22 11                               |
    | and r11b, byte [rcx]                                             | 44 22 19                               |
    | and r12b, byte [rcx]                                             | 44 22 21                               |
    | and r13b, byte [rcx]                                             | 44 22 29                               |
    | and r14b, byte [rcx]                                             | 44 22 31                               |
    | and r15b, byte [rcx]                                             | 44 22 39                               |
    | and ah, byte [rcx]                                               | 22 21                                  |
    | and ch, byte [rcx]                                               | 22 29                                  |
    | and dh, byte [rcx]                                               | 22 31                                  |
    | and bh, byte [rcx]                                               | 22 39                                  |
    | and al, byte [rax]                                               | 22 00                                  |
    | and al, byte [rdx]                                               | 22 02                                  |
    | and al, byte [rbx]                                               | 22 03                                  |
    | and al, byte [rsp]                                               | 22 04 24                               |
    | and al, byte [rbp]                                               | 22 45 00                               |
    | and al, byte [rsi]                                               | 22 06                                  |
    | and al, byte [rdi]                                               | 22 07                                  |
    | and al, byte [r8]                                                | 41 22 00                               |
    | and al, byte [r9]                                                | 41 22 01                               |
    | and al, byte [r10]                                               | 41 22 02                               |
    | and al, byte [r11]                                               | 41 22 03                               |
    | and al, byte [r12]                                               | 41 22 04 24                            |
    | and al, byte [r13]                                               | 41 22 45 00                            |
    | and al, byte [r14]                                               | 41 22 06                               |
    | and al, byte [r15]                                               | 41 22 07                               |
    | and al, byte [rax + 1 * rcx]                                     | 22 04 08                               |
    | and al, byte [rcx + 1 * rcx]                                     | 22 04 09                               |
    | and al, byte [rdx + 1 * rcx]                                     | 22 04 0a                               |
    | and al, byte [rbx + 1 * rcx]                                     | 22 04 0b                               |
    | and al, byte [rsp + 1 * rcx]                                     | 22 04 0c                               |
    | and al, byte [rbp + 1 * rcx]                                     | 22 44 0d 00                            |
    | and al, byte [rsi + 1 * rcx]                                     | 22 04 0e                               |
    | and al, byte [rdi + 1 * rcx]                                     | 22 04 0f                               |
    | and al, byte [r8 + 1 * rcx]                                      | 41 22 04 08                            |
    | and al, byte [r9 + 1 * rcx]                                      | 41 22 04 09                            |
    | and al, byte [r10 + 1 * rcx]                                     | 41 22 04 0a                            |
    | and al, byte [r11 + 1 * rcx]                                     | 41 22 04 0b                            |
    | and al, byte [r12 + 1 * rcx]                                     | 41 22 04 0c                            |
    | and al, byte [r13 + 1 * rcx]                                     | 41 22 44 0d 00                         |
    | and al, byte [r14 + 1 * rcx]                                     | 41 22 04 0e                            |
    | and al, byte [r15 + 1 * rcx]                                     | 41 22 04 0f                            |
    | and al, byte [rax + 1 * rax]                                     | 22 04 00                               |
    | and al, byte [rax + 1 * rdx]                                     | 22 04 10                               |
    | and al, byte [rax + 1 * rbx]                                     | 22 04 18                               |
    | and al, byte [rax + 1 * rbp]                                     | 22 04 28                               |
    | and al, byte [rax + 1 * rsi]                                     | 22 04 30                               |
    | and al, byte [rax + 1 * rdi]                                     | 22 04 38                               |
    | and al, byte [rax + 1 * r8]                                      | 42 22 04 00                            |
    | and al, byte [rax + 1 * r9]                                      | 42 22 04 08                            |
    | and al, byte [rax + 1 * r10]                                     | 42 22 04 10                            |
    | and al, byte [rax + 1 * r11]                                     | 42 22 04 18                            |
    | and al, byte [rax + 1 * r12]                                     | 42 22 04 20                            |
    | and al, byte [rax + 1 * r13]                                     | 42 22 04 28                            |
    | and al, byte [rax + 1 * r14]                                     | 42 22 04 30                            |
    | and al, byte [rax + 1 * r15]                                     | 42 22 04 38                            |
    | and al, byte [rax + 2 * rcx]                                     | 22 04 48                               |
    | and al, byte [rax + 4 * rcx]                                     | 22 04 88                               |
    | and al, byte [rax + 8 * rcx]                                     | 22 04 c8                               |
    | and al, byte [r8 + 1 * r9]                                       | 43 22 04 08                            |
    | and al, byte [r8 + 2 * r9]                                       | 43 22 04 48                            |
    | and al, byte [r8 + 4 * r9]                                       | 43 22 04 88                            |
    | and al, byte [r8 + 8 * r9]                                       | 43 22 04 c8                            |
    | and al, byte [1 * rcx]                                           | 22 04 0d 00 00 00 00                   |
    | and al, byte [2 * rcx]                                           | 22 04 4d 00 00 00 00                   |
    | and al, byte [4 * rcx]                                           | 22 04 8d 00 00 00 00                   |
    | and al, byte [8 * rcx]                                           | 22 04 cd 00 00 00 00                   |
    | and al, byte [1 * r9]                                            | 42 22 04 0d 00 00 00 00                |
    | and al, byte [2 * r9]                                            | 42 22 04 4d 00 00 00 00                |
    | and al, byte [4 * r9]                                            | 42 22 04 8d 00 00 00 00                |
    | and al, byte [8 * r9]                                            | 42 22 04 cd 00 00 00 00                |
    | and al, byte [r13 + 8 * r12]                                     | 43 22 44 e5 00                         |
    | and al, byte [rsp + 4 * r15]                                     | 42 22 04 bc                            |
    | and al, byte [rax + 1 * rcx + 0x00]                              | 22 44 08 00                            |
    | and al, byte [rax + 1 * rcx - 0x00]                              | 22 44 08 00                            |
    | and al, byte [rax + 1 * rcx + 0x01]                              | 22 44 08 01                            |
    | and al, byte [rax + 1 * rcx - 0x01]                              | 22 44 08 ff                            |
    | and al, byte [rax + 1 * rcx + 0x00000001]                        | 22 84 08 01 00 00 00                   |
    | and al, byte [rax + 1 * rcx - 0x00000001]                        | 22 84 08 ff ff ff ff                   |
    | and al, byte [rax + 1 * rcx + 0x7f]                              | 22 44 08 7f                            |
    | and al, byte [rax + 1 * rcx - 0x7f]                              | 22 44 08 81                            |
    | and al, byte [rax + 1 * rcx + 0x80]                              | 22 84 08 80 00 00 00                   |
    | and al, byte [rax + 1 * rcx - 0x80]                              | 22 44 08 80                            |
    | and al, byte [rax + 1 * rcx - 0x81]                              | 22 84 08 7f ff ff ff                   |
    | and al, byte [rax + 1 * rcx + 0xff]                              | 22 84 08 ff 00 00 00                   |
    | and al, byte [rax + 1 * rcx - 0xff]                              | 22 84 08 01 ff ff ff                   |
    | and al, byte [rax + 1 * rcx + 0x7fffffff]                        | 22 84 08 ff ff ff 7f                   |
    | and al, byte [rax + 1 * rcx - 0x7fffffff]                        | 22 84 08 01 00 00 80                   |
    | and al, byte [rax + 1 * rcx - 0x80000000]                        | 22 84 08 00 00 00 80                   |
    | and al, byte [r10 + 0x7f]                                        | 41 22 42 7f                            |
    | and al, byte [r10 + 0x80]                                        | 41 22 82 80 00 00 00                   |
    | and al, byte [r10 - 0x80]                                        | 41 22 42 80                            |
    | and al, byte [r10 - 0x81]                                        | 41 22 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and al, byte [rel @prev5]       | 90 90 90 90 90 22 05 f5 ff ff ff       |
    | .prev1: nop; and al, byte [rel @prev1]                           | 90 22 05 f9 ff ff ff                   |
    | and al, byte [rel @next1]; nop; .next1: nop                      | 22 05 01 00 00 00 90 90                |
    | and al, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop  | 22 05 05 00 00 00 90 90 90 90 90 90    |
    | and cl, byte [rdx]                                               | 22 0a                                  |
    | and dl, byte [rbx]                                               | 22 13                                  |
    | and bl, byte [rsp]                                               | 22 1c 24                               |
    | and spl, byte [rbp]                                              | 40 22 65 00                            |
    | and bpl, byte [rsi]                                              | 40 22 2e                               |
    | and sil, byte [rdi]                                              | 40 22 37                               |
    | and dil, byte [r8]                                               | 41 22 38                               |
    | and r8b, byte [r9]                                               | 45 22 01                               |
    | and r9b, byte [r10]                                              | 45 22 0a                               |
    | and r10b, byte [r11]                                             | 45 22 13                               |
    | and r11b, byte [r12]                                             | 45 22 1c 24                            |
    | and r12b, byte [r13]                                             | 45 22 65 00                            |
    | and r13b, byte [r14]                                             | 45 22 2e                               |
    | and r14b, byte [r15]                                             | 45 22 37                               |
    | and r15b, byte [rax + 1 * rcx]                                   | 44 22 3c 08                            |
    | and ah, byte [rcx + 1 * rcx]                                     | 22 24 09                               |
    | and ch, byte [rdx + 1 * rcx]                                     | 22 2c 0a                               |
    | and dh, byte [rbx + 1 * rcx]                                     | 22 34 0b                               |
    | and bh, byte [rsp + 1 * rcx]                                     | 22 3c 0c                               |
    | and cl, byte [rsi + 1 * rcx]                                     | 22 0c 0e                               |
    | and dl, byte [rdi + 1 * rcx]                                     | 22 14 0f                               |
    | and bl, byte [r8 + 1 * rcx]                                      | 41 22 1c 08                            |
    | and spl, byte [r9 + 1 * rcx]                                     | 41 22 24 09                            |
    | and bpl, byte [r10 + 1 * rcx]                                    | 41 22 2c 0a                            |
    | and sil, byte [r11 + 1 * rcx]                                    | 41 22 34 0b                            |
    | and dil, byte [r12 + 1 * rcx]                                    | 41 22 3c 0c                            |
    | and r8b, byte [r13 + 1 * rcx]                                    | 45 22 44 0d 00                         |
    | and r9b, byte [r14 + 1 * rcx]                                    | 45 22 0c 0e                            |
    | and r10b, byte [r15 + 1 * rcx]                                   | 45 22 14 0f                            |
    | and r11b, byte [rax + 1 * rax]                                   | 44 22 1c 00                            |
    | and r12b, byte [rax + 1 * rdx]                                   | 44 22 24 10                            |
    | and r13b, byte [rax + 1 * rbx]                                   | 44 22 2c 18                            |
    | and r14b, byte [rax + 1 * rbp]                                   | 44 22 34 28                            |
    | and r15b, byte [rax + 1 * rsi]                                   | 44 22 3c 30                            |
    | and ah, byte [rax + 1 * rdi]                                     | 22 24 38                               |
    | and ch, byte [rax + 1 * r8]                                      | !! !! !!                               |
    | and dh, byte [rax + 1 * r9]                                      | !! !! !!                               |
    | and bh, byte [rax + 1 * r10]                                     | !! !! !!                               |
    | and cl, byte [rax + 1 * r12]                                     | 42 22 0c 20                            |
    | and dl, byte [rax + 1 * r13]                                     | 42 22 14 28                            |
    | and bl, byte [rax + 1 * r14]                                     | 42 22 1c 30                            |
    | and spl, byte [rax + 1 * r15]                                    | 42 22 24 38                            |
    | and bpl, byte [rax + 2 * rcx]                                    | 40 22 2c 48                            |
    | and sil, byte [rax + 4 * rcx]                                    | 40 22 34 88                            |
    | and dil, byte [rax + 8 * rcx]                                    | 40 22 3c c8                            |
    | and r8b, byte [r8 + 1 * r9]                                      | 47 22 04 08                            |
    | and r9b, byte [r8 + 2 * r9]                                      | 47 22 0c 48                            |
    | and r10b, byte [r8 + 4 * r9]                                     | 47 22 14 88                            |
    | and r11b, byte [r8 + 8 * r9]                                     | 47 22 1c c8                            |
    | and r12b, byte [1 * rcx]                                         | 44 22 24 0d 00 00 00 00                |
    | and r13b, byte [2 * rcx]                                         | 44 22 2c 4d 00 00 00 00                |
    | and r14b, byte [4 * rcx]                                         | 44 22 34 8d 00 00 00 00                |
    | and r15b, byte [8 * rcx]                                         | 44 22 3c cd 00 00 00 00                |
    | and ah, byte [1 * r9]                                            | !! !! !!                               |
    | and ch, byte [2 * r9]                                            | !! !! !!                               |
    | and dh, byte [4 * r9]                                            | !! !! !!                               |
    | and bh, byte [8 * r9]                                            | !! !! !!                               |
    | and cl, byte [rsp + 4 * r15]                                     | 42 22 0c bc                            |
    | and dl, byte [rax + 1 * rcx + 0x00]                              | 22 54 08 00                            |
    | and bl, byte [rax + 1 * rcx - 0x00]                              | 22 5c 08 00                            |
    | and spl, byte [rax + 1 * rcx + 0x01]                             | 40 22 64 08 01                         |
    | and bpl, byte [rax + 1 * rcx - 0x01]                             | 40 22 6c 08 ff                         |
    | and sil, byte [rax + 1 * rcx + 0x00000001]                       | 40 22 b4 08 01 00 00 00                |
    | and dil, byte [rax + 1 * rcx - 0x00000001]                       | 40 22 bc 08 ff ff ff ff                |
    | and r8b, byte [rax + 1 * rcx + 0x7f]                             | 44 22 44 08 7f                         |
    | and r9b, byte [rax + 1 * rcx - 0x7f]                             | 44 22 4c 08 81                         |
    | and r10b, byte [rax + 1 * rcx + 0x80]                            | 44 22 94 08 80 00 00 00                |
    | and r11b, byte [rax + 1 * rcx - 0x80]                            | 44 22 5c 08 80                         |
    | and r12b, byte [rax + 1 * rcx - 0x81]                            | 44 22 a4 08 7f ff ff ff                |
    | and r13b, byte [rax + 1 * rcx + 0xff]                            | 44 22 ac 08 ff 00 00 00                |
    | and r14b, byte [rax + 1 * rcx - 0xff]                            | 44 22 b4 08 01 ff ff ff                |
    | and r15b, byte [rax + 1 * rcx + 0x7fffffff]                      | 44 22 bc 08 ff ff ff 7f                |
    | and ah, byte [rax + 1 * rcx - 0x7fffffff]                        | 22 a4 08 01 00 00 80                   |
    | and ch, byte [rax + 1 * rcx - 0x80000000]                        | 22 ac 08 00 00 00 80                   |
    | and dh, byte [r10 + 0x7f]                                        | !! !! !!                               |
    | and bh, byte [r10 + 0x80]                                        | !! !! !!                               |
    | and cl, byte [r10 - 0x81]                                        | 41 22 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and dl, byte [rel @prev5]       | 90 90 90 90 90 22 15 f5 ff ff ff       |
    | .prev1: nop; and bl, byte [rel @prev1]                           | 90 22 1d f9 ff ff ff                   |
    | and spl, byte [rel @next1]; nop; .next1: nop                     | 40 22 25 01 00 00 00 90 90             |
    | and bpl, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 40 22 2d 05 00 00 00 90 90 90 90 90 90 |
    | and sil, byte [rax]                                              | 40 22 30                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_and_reg8_addr8():
    encode(AND_REG8_ADDR8)


AND_ADDR64_IMM8 = """
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | instruction                                                        | encoding                                  |
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | and qword [rax], 0x01                                              | 48 83 20 01                               |
    | and qword [rcx], 0x01                                              | 48 83 21 01                               |
    | and qword [rdx], 0x01                                              | 48 83 22 01                               |
    | and qword [rbx], 0x01                                              | 48 83 23 01                               |
    | and qword [rsp], 0x01                                              | 48 83 24 24 01                            |
    | and qword [rbp], 0x01                                              | 48 83 65 00 01                            |
    | and qword [rsi], 0x01                                              | 48 83 26 01                               |
    | and qword [rdi], 0x01                                              | 48 83 27 01                               |
    | and qword [r8], 0x01                                               | 49 83 20 01                               |
    | and qword [r9], 0x01                                               | 49 83 21 01                               |
    | and qword [r10], 0x01                                              | 49 83 22 01                               |
    | and qword [r11], 0x01                                              | 49 83 23 01                               |
    | and qword [r12], 0x01                                              | 49 83 24 24 01                            |
    | and qword [r13], 0x01                                              | 49 83 65 00 01                            |
    | and qword [r14], 0x01                                              | 49 83 26 01                               |
    | and qword [r15], 0x01                                              | 49 83 27 01                               |
    | and qword [rax + 1 * rcx], 0x01                                    | 48 83 24 08 01                            |
    | and qword [rcx + 1 * rcx], 0x01                                    | 48 83 24 09 01                            |
    | and qword [rdx + 1 * rcx], 0x01                                    | 48 83 24 0a 01                            |
    | and qword [rbx + 1 * rcx], 0x01                                    | 48 83 24 0b 01                            |
    | and qword [rsp + 1 * rcx], 0x01                                    | 48 83 24 0c 01                            |
    | and qword [rbp + 1 * rcx], 0x01                                    | 48 83 64 0d 00 01                         |
    | and qword [rsi + 1 * rcx], 0x01                                    | 48 83 24 0e 01                            |
    | and qword [rdi + 1 * rcx], 0x01                                    | 48 83 24 0f 01                            |
    | and qword [r8 + 1 * rcx], 0x01                                     | 49 83 24 08 01                            |
    | and qword [r9 + 1 * rcx], 0x01                                     | 49 83 24 09 01                            |
    | and qword [r10 + 1 * rcx], 0x01                                    | 49 83 24 0a 01                            |
    | and qword [r11 + 1 * rcx], 0x01                                    | 49 83 24 0b 01                            |
    | and qword [r12 + 1 * rcx], 0x01                                    | 49 83 24 0c 01                            |
    | and qword [r13 + 1 * rcx], 0x01                                    | 49 83 64 0d 00 01                         |
    | and qword [r14 + 1 * rcx], 0x01                                    | 49 83 24 0e 01                            |
    | and qword [r15 + 1 * rcx], 0x01                                    | 49 83 24 0f 01                            |
    | and qword [rax + 1 * rax], 0x01                                    | 48 83 24 00 01                            |
    | and qword [rax + 1 * rdx], 0x01                                    | 48 83 24 10 01                            |
    | and qword [rax + 1 * rbx], 0x01                                    | 48 83 24 18 01                            |
    | and qword [rax + 1 * rbp], 0x01                                    | 48 83 24 28 01                            |
    | and qword [rax + 1 * rsi], 0x01                                    | 48 83 24 30 01                            |
    | and qword [rax + 1 * rdi], 0x01                                    | 48 83 24 38 01                            |
    | and qword [rax + 1 * r8], 0x01                                     | 4a 83 24 00 01                            |
    | and qword [rax + 1 * r9], 0x01                                     | 4a 83 24 08 01                            |
    | and qword [rax + 1 * r10], 0x01                                    | 4a 83 24 10 01                            |
    | and qword [rax + 1 * r11], 0x01                                    | 4a 83 24 18 01                            |
    | and qword [rax + 1 * r12], 0x01                                    | 4a 83 24 20 01                            |
    | and qword [rax + 1 * r13], 0x01                                    | 4a 83 24 28 01                            |
    | and qword [rax + 1 * r14], 0x01                                    | 4a 83 24 30 01                            |
    | and qword [rax + 1 * r15], 0x01                                    | 4a 83 24 38 01                            |
    | and qword [rax + 2 * rcx], 0x01                                    | 48 83 24 48 01                            |
    | and qword [rax + 4 * rcx], 0x01                                    | 48 83 24 88 01                            |
    | and qword [rax + 8 * rcx], 0x01                                    | 48 83 24 c8 01                            |
    | and qword [r8 + 1 * r9], 0x01                                      | 4b 83 24 08 01                            |
    | and qword [r8 + 2 * r9], 0x01                                      | 4b 83 24 48 01                            |
    | and qword [r8 + 4 * r9], 0x01                                      | 4b 83 24 88 01                            |
    | and qword [r8 + 8 * r9], 0x01                                      | 4b 83 24 c8 01                            |
    | and qword [1 * rcx], 0x01                                          | 48 83 24 0d 00 00 00 00 01                |
    | and qword [2 * rcx], 0x01                                          | 48 83 24 4d 00 00 00 00 01                |
    | and qword [4 * rcx], 0x01                                          | 48 83 24 8d 00 00 00 00 01                |
    | and qword [8 * rcx], 0x01                                          | 48 83 24 cd 00 00 00 00 01                |
    | and qword [1 * r9], 0x01                                           | 4a 83 24 0d 00 00 00 00 01                |
    | and qword [2 * r9], 0x01                                           | 4a 83 24 4d 00 00 00 00 01                |
    | and qword [4 * r9], 0x01                                           | 4a 83 24 8d 00 00 00 00 01                |
    | and qword [8 * r9], 0x01                                           | 4a 83 24 cd 00 00 00 00 01                |
    | and qword [r13 + 8 * r12], 0x01                                    | 4b 83 64 e5 00 01                         |
    | and qword [rsp + 4 * r15], 0x01                                    | 4a 83 24 bc 01                            |
    | and qword [rax + 1 * rcx + 0x00], 0x01                             | 48 83 64 08 00 01                         |
    | and qword [rax + 1 * rcx - 0x00], 0x01                             | 48 83 64 08 00 01                         |
    | and qword [rax + 1 * rcx + 0x01], 0x01                             | 48 83 64 08 01 01                         |
    | and qword [rax + 1 * rcx - 0x01], 0x01                             | 48 83 64 08 ff 01                         |
    | and qword [rax + 1 * rcx + 0x00000001], 0x01                       | 48 83 a4 08 01 00 00 00 01                |
    | and qword [rax + 1 * rcx - 0x00000001], 0x01                       | 48 83 a4 08 ff ff ff ff 01                |
    | and qword [rax + 1 * rcx + 0x7f], 0x01                             | 48 83 64 08 7f 01                         |
    | and qword [rax + 1 * rcx - 0x7f], 0x01                             | 48 83 64 08 81 01                         |
    | and qword [rax + 1 * rcx + 0x80], 0x01                             | 48 83 a4 08 80 00 00 00 01                |
    | and qword [rax + 1 * rcx - 0x80], 0x01                             | 48 83 64 08 80 01                         |
    | and qword [rax + 1 * rcx - 0x81], 0x01                             | 48 83 a4 08 7f ff ff ff 01                |
    | and qword [rax + 1 * rcx + 0xff], 0x01                             | 48 83 a4 08 ff 00 00 00 01                |
    | and qword [rax + 1 * rcx - 0xff], 0x01                             | 48 83 a4 08 01 ff ff ff 01                |
    | and qword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 48 83 a4 08 ff ff ff 7f 01                |
    | and qword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 48 83 a4 08 01 00 00 80 01                |
    | and qword [rax + 1 * rcx - 0x80000000], 0x01                       | 48 83 a4 08 00 00 00 80 01                |
    | and qword [r10 + 0x7f], 0x01                                       | 49 83 62 7f 01                            |
    | and qword [r10 + 0x80], 0x01                                       | 49 83 a2 80 00 00 00 01                   |
    | and qword [r10 - 0x80], 0x01                                       | 49 83 62 80 01                            |
    | and qword [r10 - 0x81], 0x01                                       | 49 83 a2 7f ff ff ff 01                   |
    | .prev5: nop; nop; nop; nop; nop; and qword [rel @prev5], 0x01      | 90 90 90 90 90 48 83 25 f3 ff ff ff 01    |
    | .prev1: nop; and qword [rel @prev1], 0x01                          | 90 48 83 25 f7 ff ff ff 01                |
    | and qword [rel @next1], 0x01; nop; .next1: nop                     | 48 83 25 01 00 00 00 01 90 90             |
    | and qword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 48 83 25 05 00 00 00 01 90 90 90 90 90 90 |
    | and qword [rax], 0x00                                              | 48 83 20 00                               |
    | and qword [rax], 0x7f                                              | 48 83 20 7f                               |
    | and qword [rax], 0x80                                              | 48 83 20 80                               |
    | and qword [rax], 0xff                                              | 48 83 20 ff                               |
    | and qword [rcx], 0x7f                                              | 48 83 21 7f                               |
    | and qword [rdx], 0x80                                              | 48 83 22 80                               |
    | and qword [rbx], 0xff                                              | 48 83 23 ff                               |
    | and qword [rsp], 0x00                                              | 48 83 24 24 00                            |
    | and qword [rsi], 0x7f                                              | 48 83 26 7f                               |
    | and qword [rdi], 0x80                                              | 48 83 27 80                               |
    | and qword [r8], 0xff                                               | 49 83 20 ff                               |
    | and qword [r9], 0x00                                               | 49 83 21 00                               |
    | and qword [r11], 0x7f                                              | 49 83 23 7f                               |
    | and qword [r12], 0x80                                              | 49 83 24 24 80                            |
    | and qword [r13], 0xff                                              | 49 83 65 00 ff                            |
    | and qword [r14], 0x00                                              | 49 83 26 00                               |
    | and qword [rax + 1 * rcx], 0x7f                                    | 48 83 24 08 7f                            |
    | and qword [rcx + 1 * rcx], 0x80                                    | 48 83 24 09 80                            |
    | and qword [rdx + 1 * rcx], 0xff                                    | 48 83 24 0a ff                            |
    | and qword [rbx + 1 * rcx], 0x00                                    | 48 83 24 0b 00                            |
    | and qword [rbp + 1 * rcx], 0x7f                                    | 48 83 64 0d 00 7f                         |
    | and qword [rsi + 1 * rcx], 0x80                                    | 48 83 24 0e 80                            |
    | and qword [rdi + 1 * rcx], 0xff                                    | 48 83 24 0f ff                            |
    | and qword [r8 + 1 * rcx], 0x00                                     | 49 83 24 08 00                            |
    | and qword [r10 + 1 * rcx], 0x7f                                    | 49 83 24 0a 7f                            |
    | and qword [r11 + 1 * rcx], 0x80                                    | 49 83 24 0b 80                            |
    | and qword [r12 + 1 * rcx], 0xff                                    | 49 83 24 0c ff                            |
    | and qword [r13 + 1 * rcx], 0x00                                    | 49 83 64 0d 00 00                         |
    | and qword [r15 + 1 * rcx], 0x7f                                    | 49 83 24 0f 7f                            |
    | and qword [rax + 1 * rax], 0x80                                    | 48 83 24 00 80                            |
    | and qword [rax + 1 * rdx], 0xff                                    | 48 83 24 10 ff                            |
    | and qword [rax + 1 * rbx], 0x00                                    | 48 83 24 18 00                            |
    | and qword [rax + 1 * rsi], 0x7f                                    | 48 83 24 30 7f                            |
    | and qword [rax + 1 * rdi], 0x80                                    | 48 83 24 38 80                            |
    | and qword [rax + 1 * r8], 0xff                                     | 4a 83 24 00 ff                            |
    | and qword [rax + 1 * r9], 0x00                                     | 4a 83 24 08 00                            |
    | and qword [rax + 1 * r11], 0x7f                                    | 4a 83 24 18 7f                            |
    | and qword [rax + 1 * r12], 0x80                                    | 4a 83 24 20 80                            |
    | and qword [rax + 1 * r13], 0xff                                    | 4a 83 24 28 ff                            |
    | and qword [rax + 1 * r14], 0x00                                    | 4a 83 24 30 00                            |
    | and qword [rax + 2 * rcx], 0x7f                                    | 48 83 24 48 7f                            |
    | and qword [rax + 4 * rcx], 0x80                                    | 48 83 24 88 80                            |
    | and qword [rax + 8 * rcx], 0xff                                    | 48 83 24 c8 ff                            |
    | and qword [r8 + 1 * r9], 0x00                                      | 4b 83 24 08 00                            |
    | and qword [r8 + 4 * r9], 0x7f                                      | 4b 83 24 88 7f                            |
    | and qword [r8 + 8 * r9], 0x80                                      | 4b 83 24 c8 80                            |
    | and qword [1 * rcx], 0xff                                          | 48 83 24 0d 00 00 00 00 ff                |
    | and qword [2 * rcx], 0x00                                          | 48 83 24 4d 00 00 00 00 00                |
    | and qword [8 * rcx], 0x7f                                          | 48 83 24 cd 00 00 00 00 7f                |
    | and qword [1 * r9], 0x80                                           | 4a 83 24 0d 00 00 00 00 80                |
    | and qword [2 * r9], 0xff                                           | 4a 83 24 4d 00 00 00 00 ff                |
    | and qword [4 * r9], 0x00                                           | 4a 83 24 8d 00 00 00 00 00                |
    | and qword [r13 + 8 * r12], 0x7f                                    | 4b 83 64 e5 00 7f                         |
    | and qword [rsp + 4 * r15], 0x80                                    | 4a 83 24 bc 80                            |
    | and qword [rax + 1 * rcx + 0x00], 0xff                             | 48 83 64 08 00 ff                         |
    | and qword [rax + 1 * rcx - 0x00], 0x00                             | 48 83 64 08 00 00                         |
    | and qword [rax + 1 * rcx - 0x01], 0x7f                             | 48 83 64 08 ff 7f                         |
    | and qword [rax + 1 * rcx + 0x00000001], 0x80                       | 48 83 a4 08 01 00 00 00 80                |
    | and qword [rax + 1 * rcx - 0x00000001], 0xff                       | 48 83 a4 08 ff ff ff ff ff                |
    | and qword [rax + 1 * rcx + 0x7f], 0x00                             | 48 83 64 08 7f 00                         |
    | and qword [rax + 1 * rcx + 0x80], 0x7f                             | 48 83 a4 08 80 00 00 00 7f                |
    | and qword [rax + 1 * rcx - 0x80], 0x80                             | 48 83 64 08 80 80                         |
    | and qword [rax + 1 * rcx - 0x81], 0xff                             | 48 83 a4 08 7f ff ff ff ff                |
    | and qword [rax + 1 * rcx + 0xff], 0x00                             | 48 83 a4 08 ff 00 00 00 00                |
    | and qword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 48 83 a4 08 ff ff ff 7f 7f                |
    | and qword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 48 83 a4 08 01 00 00 80 80                |
    | and qword [rax + 1 * rcx - 0x80000000], 0xff                       | 48 83 a4 08 00 00 00 80 ff                |
    | and qword [r10 + 0x7f], 0x00                                       | 49 83 62 7f 00                            |
    | and qword [r10 - 0x80], 0x7f                                       | 49 83 62 80 7f                            |
    | and qword [r10 - 0x81], 0x80                                       | 49 83 a2 7f ff ff ff 80                   |
    | .prev5: nop; nop; nop; nop; nop; and qword [rel @prev5], 0xff      | 90 90 90 90 90 48 83 25 f3 ff ff ff ff    |
    | .prev1: nop; and qword [rel @prev1], 0x00                          | 90 48 83 25 f7 ff ff ff 00                |
    | and qword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 48 83 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | ----------------------------------------- |
"""


def can_encode_and_addr64_imm8():
    encode(AND_ADDR64_IMM8)


AND_ADDR64_IMM32 = """
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
    | instruction                                                              | encoding                                           |
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
    | and qword [rax], 0x00000001                                              | 48 81 20 01 00 00 00                               |
    | and qword [rcx], 0x00000001                                              | 48 81 21 01 00 00 00                               |
    | and qword [rdx], 0x00000001                                              | 48 81 22 01 00 00 00                               |
    | and qword [rbx], 0x00000001                                              | 48 81 23 01 00 00 00                               |
    | and qword [rsp], 0x00000001                                              | 48 81 24 24 01 00 00 00                            |
    | and qword [rbp], 0x00000001                                              | 48 81 65 00 01 00 00 00                            |
    | and qword [rsi], 0x00000001                                              | 48 81 26 01 00 00 00                               |
    | and qword [rdi], 0x00000001                                              | 48 81 27 01 00 00 00                               |
    | and qword [r8], 0x00000001                                               | 49 81 20 01 00 00 00                               |
    | and qword [r9], 0x00000001                                               | 49 81 21 01 00 00 00                               |
    | and qword [r10], 0x00000001                                              | 49 81 22 01 00 00 00                               |
    | and qword [r11], 0x00000001                                              | 49 81 23 01 00 00 00                               |
    | and qword [r12], 0x00000001                                              | 49 81 24 24 01 00 00 00                            |
    | and qword [r13], 0x00000001                                              | 49 81 65 00 01 00 00 00                            |
    | and qword [r14], 0x00000001                                              | 49 81 26 01 00 00 00                               |
    | and qword [r15], 0x00000001                                              | 49 81 27 01 00 00 00                               |
    | and qword [rax + 1 * rcx], 0x00000001                                    | 48 81 24 08 01 00 00 00                            |
    | and qword [rcx + 1 * rcx], 0x00000001                                    | 48 81 24 09 01 00 00 00                            |
    | and qword [rdx + 1 * rcx], 0x00000001                                    | 48 81 24 0a 01 00 00 00                            |
    | and qword [rbx + 1 * rcx], 0x00000001                                    | 48 81 24 0b 01 00 00 00                            |
    | and qword [rsp + 1 * rcx], 0x00000001                                    | 48 81 24 0c 01 00 00 00                            |
    | and qword [rbp + 1 * rcx], 0x00000001                                    | 48 81 64 0d 00 01 00 00 00                         |
    | and qword [rsi + 1 * rcx], 0x00000001                                    | 48 81 24 0e 01 00 00 00                            |
    | and qword [rdi + 1 * rcx], 0x00000001                                    | 48 81 24 0f 01 00 00 00                            |
    | and qword [r8 + 1 * rcx], 0x00000001                                     | 49 81 24 08 01 00 00 00                            |
    | and qword [r9 + 1 * rcx], 0x00000001                                     | 49 81 24 09 01 00 00 00                            |
    | and qword [r10 + 1 * rcx], 0x00000001                                    | 49 81 24 0a 01 00 00 00                            |
    | and qword [r11 + 1 * rcx], 0x00000001                                    | 49 81 24 0b 01 00 00 00                            |
    | and qword [r12 + 1 * rcx], 0x00000001                                    | 49 81 24 0c 01 00 00 00                            |
    | and qword [r13 + 1 * rcx], 0x00000001                                    | 49 81 64 0d 00 01 00 00 00                         |
    | and qword [r14 + 1 * rcx], 0x00000001                                    | 49 81 24 0e 01 00 00 00                            |
    | and qword [r15 + 1 * rcx], 0x00000001                                    | 49 81 24 0f 01 00 00 00                            |
    | and qword [rax + 1 * rax], 0x00000001                                    | 48 81 24 00 01 00 00 00                            |
    | and qword [rax + 1 * rdx], 0x00000001                                    | 48 81 24 10 01 00 00 00                            |
    | and qword [rax + 1 * rbx], 0x00000001                                    | 48 81 24 18 01 00 00 00                            |
    | and qword [rax + 1 * rbp], 0x00000001                                    | 48 81 24 28 01 00 00 00                            |
    | and qword [rax + 1 * rsi], 0x00000001                                    | 48 81 24 30 01 00 00 00                            |
    | and qword [rax + 1 * rdi], 0x00000001                                    | 48 81 24 38 01 00 00 00                            |
    | and qword [rax + 1 * r8], 0x00000001                                     | 4a 81 24 00 01 00 00 00                            |
    | and qword [rax + 1 * r9], 0x00000001                                     | 4a 81 24 08 01 00 00 00                            |
    | and qword [rax + 1 * r10], 0x00000001                                    | 4a 81 24 10 01 00 00 00                            |
    | and qword [rax + 1 * r11], 0x00000001                                    | 4a 81 24 18 01 00 00 00                            |
    | and qword [rax + 1 * r12], 0x00000001                                    | 4a 81 24 20 01 00 00 00                            |
    | and qword [rax + 1 * r13], 0x00000001                                    | 4a 81 24 28 01 00 00 00                            |
    | and qword [rax + 1 * r14], 0x00000001                                    | 4a 81 24 30 01 00 00 00                            |
    | and qword [rax + 1 * r15], 0x00000001                                    | 4a 81 24 38 01 00 00 00                            |
    | and qword [rax + 2 * rcx], 0x00000001                                    | 48 81 24 48 01 00 00 00                            |
    | and qword [rax + 4 * rcx], 0x00000001                                    | 48 81 24 88 01 00 00 00                            |
    | and qword [rax + 8 * rcx], 0x00000001                                    | 48 81 24 c8 01 00 00 00                            |
    | and qword [r8 + 1 * r9], 0x00000001                                      | 4b 81 24 08 01 00 00 00                            |
    | and qword [r8 + 2 * r9], 0x00000001                                      | 4b 81 24 48 01 00 00 00                            |
    | and qword [r8 + 4 * r9], 0x00000001                                      | 4b 81 24 88 01 00 00 00                            |
    | and qword [r8 + 8 * r9], 0x00000001                                      | 4b 81 24 c8 01 00 00 00                            |
    | and qword [1 * rcx], 0x00000001                                          | 48 81 24 0d 00 00 00 00 01 00 00 00                |
    | and qword [2 * rcx], 0x00000001                                          | 48 81 24 4d 00 00 00 00 01 00 00 00                |
    | and qword [4 * rcx], 0x00000001                                          | 48 81 24 8d 00 00 00 00 01 00 00 00                |
    | and qword [8 * rcx], 0x00000001                                          | 48 81 24 cd 00 00 00 00 01 00 00 00                |
    | and qword [1 * r9], 0x00000001                                           | 4a 81 24 0d 00 00 00 00 01 00 00 00                |
    | and qword [2 * r9], 0x00000001                                           | 4a 81 24 4d 00 00 00 00 01 00 00 00                |
    | and qword [4 * r9], 0x00000001                                           | 4a 81 24 8d 00 00 00 00 01 00 00 00                |
    | and qword [8 * r9], 0x00000001                                           | 4a 81 24 cd 00 00 00 00 01 00 00 00                |
    | and qword [r13 + 8 * r12], 0x00000001                                    | 4b 81 64 e5 00 01 00 00 00                         |
    | and qword [rsp + 4 * r15], 0x00000001                                    | 4a 81 24 bc 01 00 00 00                            |
    | and qword [rax + 1 * rcx + 0x00], 0x00000001                             | 48 81 64 08 00 01 00 00 00                         |
    | and qword [rax + 1 * rcx - 0x00], 0x00000001                             | 48 81 64 08 00 01 00 00 00                         |
    | and qword [rax + 1 * rcx + 0x01], 0x00000001                             | 48 81 64 08 01 01 00 00 00                         |
    | and qword [rax + 1 * rcx - 0x01], 0x00000001                             | 48 81 64 08 ff 01 00 00 00                         |
    | and qword [rax + 1 * rcx + 0x00000001], 0x00000001                       | 48 81 a4 08 01 00 00 00 01 00 00 00                |
    | and qword [rax + 1 * rcx - 0x00000001], 0x00000001                       | 48 81 a4 08 ff ff ff ff 01 00 00 00                |
    | and qword [rax + 1 * rcx + 0x7f], 0x00000001                             | 48 81 64 08 7f 01 00 00 00                         |
    | and qword [rax + 1 * rcx - 0x7f], 0x00000001                             | 48 81 64 08 81 01 00 00 00                         |
    | and qword [rax + 1 * rcx + 0x80], 0x00000001                             | 48 81 a4 08 80 00 00 00 01 00 00 00                |
    | and qword [rax + 1 * rcx - 0x80], 0x00000001                             | 48 81 64 08 80 01 00 00 00                         |
    | and qword [rax + 1 * rcx - 0x81], 0x00000001                             | 48 81 a4 08 7f ff ff ff 01 00 00 00                |
    | and qword [rax + 1 * rcx + 0xff], 0x00000001                             | 48 81 a4 08 ff 00 00 00 01 00 00 00                |
    | and qword [rax + 1 * rcx - 0xff], 0x00000001                             | 48 81 a4 08 01 ff ff ff 01 00 00 00                |
    | and qword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | 48 81 a4 08 ff ff ff 7f 01 00 00 00                |
    | and qword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | 48 81 a4 08 01 00 00 80 01 00 00 00                |
    | and qword [rax + 1 * rcx - 0x80000000], 0x00000001                       | 48 81 a4 08 00 00 00 80 01 00 00 00                |
    | and qword [r10 + 0x7f], 0x00000001                                       | 49 81 62 7f 01 00 00 00                            |
    | and qword [r10 + 0x80], 0x00000001                                       | 49 81 a2 80 00 00 00 01 00 00 00                   |
    | and qword [r10 - 0x80], 0x00000001                                       | 49 81 62 80 01 00 00 00                            |
    | and qword [r10 - 0x81], 0x00000001                                       | 49 81 a2 7f ff ff ff 01 00 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; and qword [rel @prev5], 0x00000001      | 90 90 90 90 90 48 81 25 f0 ff ff ff 01 00 00 00    |
    | .prev1: nop; and qword [rel @prev1], 0x00000001                          | 90 48 81 25 f4 ff ff ff 01 00 00 00                |
    | and qword [rel @next1], 0x00000001; nop; .next1: nop                     | 48 81 25 01 00 00 00 01 00 00 00 90 90             |
    | and qword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | 48 81 25 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | and qword [rax], 0x00000000                                              | 48 81 20 00 00 00 00                               |
    | and qword [rax], 0x0000007f                                              | 48 81 20 7f 00 00 00                               |
    | and qword [rax], 0x00000080                                              | 48 81 20 80 00 00 00                               |
    | and qword [rax], 0x000000ff                                              | 48 81 20 ff 00 00 00                               |
    | and qword [rax], 0x00000100                                              | 48 81 20 00 01 00 00                               |
    | and qword [rax], 0x00007fff                                              | 48 81 20 ff 7f 00 00                               |
    | and qword [rax], 0x00008000                                              | 48 81 20 00 80 00 00                               |
    | and qword [rax], 0x0000ffff                                              | 48 81 20 ff ff 00 00                               |
    | and qword [rax], 0x00010000                                              | 48 81 20 00 00 01 00                               |
    | and qword [rax], 0x7fffffff                                              | 48 81 20 ff ff ff 7f                               |
    | and qword [rax], 0x80000000                                              | 48 81 20 00 00 00 80                               |
    | and qword [rax], 0xffffffff                                              | 48 81 20 ff ff ff ff                               |
    | and qword [rcx], 0x0000007f                                              | 48 81 21 7f 00 00 00                               |
    | and qword [rdx], 0x00000080                                              | 48 81 22 80 00 00 00                               |
    | and qword [rbx], 0x000000ff                                              | 48 81 23 ff 00 00 00                               |
    | and qword [rsp], 0x00000100                                              | 48 81 24 24 00 01 00 00                            |
    | and qword [rbp], 0x00007fff                                              | 48 81 65 00 ff 7f 00 00                            |
    | and qword [rsi], 0x00008000                                              | 48 81 26 00 80 00 00                               |
    | and qword [rdi], 0x0000ffff                                              | 48 81 27 ff ff 00 00                               |
    | and qword [r8], 0x00010000                                               | 49 81 20 00 00 01 00                               |
    | and qword [r9], 0x7fffffff                                               | 49 81 21 ff ff ff 7f                               |
    | and qword [r10], 0x80000000                                              | 49 81 22 00 00 00 80                               |
    | and qword [r11], 0xffffffff                                              | 49 81 23 ff ff ff ff                               |
    | and qword [r12], 0x00000000                                              | 49 81 24 24 00 00 00 00                            |
    | and qword [r14], 0x0000007f                                              | 49 81 26 7f 00 00 00                               |
    | and qword [r15], 0x00000080                                              | 49 81 27 80 00 00 00                               |
    | and qword [rax + 1 * rcx], 0x000000ff                                    | 48 81 24 08 ff 00 00 00                            |
    | and qword [rcx + 1 * rcx], 0x00000100                                    | 48 81 24 09 00 01 00 00                            |
    | and qword [rdx + 1 * rcx], 0x00007fff                                    | 48 81 24 0a ff 7f 00 00                            |
    | and qword [rbx + 1 * rcx], 0x00008000                                    | 48 81 24 0b 00 80 00 00                            |
    | and qword [rsp + 1 * rcx], 0x0000ffff                                    | 48 81 24 0c ff ff 00 00                            |
    | and qword [rbp + 1 * rcx], 0x00010000                                    | 48 81 64 0d 00 00 00 01 00                         |
    | and qword [rsi + 1 * rcx], 0x7fffffff                                    | 48 81 24 0e ff ff ff 7f                            |
    | and qword [rdi + 1 * rcx], 0x80000000                                    | 48 81 24 0f 00 00 00 80                            |
    | and qword [r8 + 1 * rcx], 0xffffffff                                     | 49 81 24 08 ff ff ff ff                            |
    | and qword [r9 + 1 * rcx], 0x00000000                                     | 49 81 24 09 00 00 00 00                            |
    | and qword [r11 + 1 * rcx], 0x0000007f                                    | 49 81 24 0b 7f 00 00 00                            |
    | and qword [r12 + 1 * rcx], 0x00000080                                    | 49 81 24 0c 80 00 00 00                            |
    | and qword [r13 + 1 * rcx], 0x000000ff                                    | 49 81 64 0d 00 ff 00 00 00                         |
    | and qword [r14 + 1 * rcx], 0x00000100                                    | 49 81 24 0e 00 01 00 00                            |
    | and qword [r15 + 1 * rcx], 0x00007fff                                    | 49 81 24 0f ff 7f 00 00                            |
    | and qword [rax + 1 * rax], 0x00008000                                    | 48 81 24 00 00 80 00 00                            |
    | and qword [rax + 1 * rdx], 0x0000ffff                                    | 48 81 24 10 ff ff 00 00                            |
    | and qword [rax + 1 * rbx], 0x00010000                                    | 48 81 24 18 00 00 01 00                            |
    | and qword [rax + 1 * rbp], 0x7fffffff                                    | 48 81 24 28 ff ff ff 7f                            |
    | and qword [rax + 1 * rsi], 0x80000000                                    | 48 81 24 30 00 00 00 80                            |
    | and qword [rax + 1 * rdi], 0xffffffff                                    | 48 81 24 38 ff ff ff ff                            |
    | and qword [rax + 1 * r8], 0x00000000                                     | 4a 81 24 00 00 00 00 00                            |
    | and qword [rax + 1 * r10], 0x0000007f                                    | 4a 81 24 10 7f 00 00 00                            |
    | and qword [rax + 1 * r11], 0x00000080                                    | 4a 81 24 18 80 00 00 00                            |
    | and qword [rax + 1 * r12], 0x000000ff                                    | 4a 81 24 20 ff 00 00 00                            |
    | and qword [rax + 1 * r13], 0x00000100                                    | 4a 81 24 28 00 01 00 00                            |
    | and qword [rax + 1 * r14], 0x00007fff                                    | 4a 81 24 30 ff 7f 00 00                            |
    | and qword [rax + 1 * r15], 0x00008000                                    | 4a 81 24 38 00 80 00 00                            |
    | and qword [rax + 2 * rcx], 0x0000ffff                                    | 48 81 24 48 ff ff 00 00                            |
    | and qword [rax + 4 * rcx], 0x00010000                                    | 48 81 24 88 00 00 01 00                            |
    | and qword [rax + 8 * rcx], 0x7fffffff                                    | 48 81 24 c8 ff ff ff 7f                            |
    | and qword [r8 + 1 * r9], 0x80000000                                      | 4b 81 24 08 00 00 00 80                            |
    | and qword [r8 + 2 * r9], 0xffffffff                                      | 4b 81 24 48 ff ff ff ff                            |
    | and qword [r8 + 4 * r9], 0x00000000                                      | 4b 81 24 88 00 00 00 00                            |
    | and qword [1 * rcx], 0x0000007f                                          | 48 81 24 0d 00 00 00 00 7f 00 00 00                |
    | and qword [2 * rcx], 0x00000080                                          | 48 81 24 4d 00 00 00 00 80 00 00 00                |
    | and qword [4 * rcx], 0x000000ff                                          | 48 81 24 8d 00 00 00 00 ff 00 00 00                |
    | and qword [8 * rcx], 0x00000100                                          | 48 81 24 cd 00 00 00 00 00 01 00 00                |
    | and qword [1 * r9], 0x00007fff                                           | 4a 81 24 0d 00 00 00 00 ff 7f 00 00                |
    | and qword [2 * r9], 0x00008000                                           | 4a 81 24 4d 00 00 00 00 00 80 00 00                |
    | and qword [4 * r9], 0x0000ffff                                           | 4a 81 24 8d 00 00 00 00 ff ff 00 00                |
    | and qword [8 * r9], 0x00010000                                           | 4a 81 24 cd 00 00 00 00 00 00 01 00                |
    | and qword [r13 + 8 * r12], 0x7fffffff                                    | 4b 81 64 e5 00 ff ff ff 7f                         |
    | and qword [rsp + 4 * r15], 0x80000000                                    | 4a 81 24 bc 00 00 00 80                            |
    | and qword [rax + 1 * rcx + 0x00], 0xffffffff                             | 48 81 64 08 00 ff ff ff ff                         |
    | and qword [rax + 1 * rcx - 0x00], 0x00000000                             | 48 81 64 08 00 00 00 00 00                         |
    | and qword [rax + 1 * rcx - 0x01], 0x0000007f                             | 48 81 64 08 ff 7f 00 00 00                         |
    | and qword [rax + 1 * rcx + 0x00000001], 0x00000080                       | 48 81 a4 08 01 00 00 00 80 00 00 00                |
    | and qword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | 48 81 a4 08 ff ff ff ff ff 00 00 00                |
    | and qword [rax + 1 * rcx + 0x7f], 0x00000100                             | 48 81 64 08 7f 00 01 00 00                         |
    | and qword [rax + 1 * rcx - 0x7f], 0x00007fff                             | 48 81 64 08 81 ff 7f 00 00                         |
    | and qword [rax + 1 * rcx + 0x80], 0x00008000                             | 48 81 a4 08 80 00 00 00 00 80 00 00                |
    | and qword [rax + 1 * rcx - 0x80], 0x0000ffff                             | 48 81 64 08 80 ff ff 00 00                         |
    | and qword [rax + 1 * rcx - 0x81], 0x00010000                             | 48 81 a4 08 7f ff ff ff 00 00 01 00                |
    | and qword [rax + 1 * rcx + 0xff], 0x7fffffff                             | 48 81 a4 08 ff 00 00 00 ff ff ff 7f                |
    | and qword [rax + 1 * rcx - 0xff], 0x80000000                             | 48 81 a4 08 01 ff ff ff 00 00 00 80                |
    | and qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | 48 81 a4 08 ff ff ff 7f ff ff ff ff                |
    | and qword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | 48 81 a4 08 01 00 00 80 00 00 00 00                |
    | and qword [r10 + 0x7f], 0x0000007f                                       | 49 81 62 7f 7f 00 00 00                            |
    | and qword [r10 + 0x80], 0x00000080                                       | 49 81 a2 80 00 00 00 80 00 00 00                   |
    | and qword [r10 - 0x80], 0x000000ff                                       | 49 81 62 80 ff 00 00 00                            |
    | and qword [r10 - 0x81], 0x00000100                                       | 49 81 a2 7f ff ff ff 00 01 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; and qword [rel @prev5], 0x00007fff      | 90 90 90 90 90 48 81 25 f0 ff ff ff ff 7f 00 00    |
    | .prev1: nop; and qword [rel @prev1], 0x00008000                          | 90 48 81 25 f4 ff ff ff 00 80 00 00                |
    | and qword [rel @next1], 0x0000ffff; nop; .next1: nop                     | 48 81 25 01 00 00 00 ff ff 00 00 90 90             |
    | and qword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | 48 81 25 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
"""


def can_encode_and_addr64_imm32():
    encode(AND_ADDR64_IMM32)


AND_ADDR64_REG64 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | and qword [rax], rcx                                              | 48 21 08                               |
    | and qword [rcx], rcx                                              | 48 21 09                               |
    | and qword [rdx], rcx                                              | 48 21 0a                               |
    | and qword [rbx], rcx                                              | 48 21 0b                               |
    | and qword [rsp], rcx                                              | 48 21 0c 24                            |
    | and qword [rbp], rcx                                              | 48 21 4d 00                            |
    | and qword [rsi], rcx                                              | 48 21 0e                               |
    | and qword [rdi], rcx                                              | 48 21 0f                               |
    | and qword [r8], rcx                                               | 49 21 08                               |
    | and qword [r9], rcx                                               | 49 21 09                               |
    | and qword [r10], rcx                                              | 49 21 0a                               |
    | and qword [r11], rcx                                              | 49 21 0b                               |
    | and qword [r12], rcx                                              | 49 21 0c 24                            |
    | and qword [r13], rcx                                              | 49 21 4d 00                            |
    | and qword [r14], rcx                                              | 49 21 0e                               |
    | and qword [r15], rcx                                              | 49 21 0f                               |
    | and qword [rax + 1 * rcx], rcx                                    | 48 21 0c 08                            |
    | and qword [rcx + 1 * rcx], rcx                                    | 48 21 0c 09                            |
    | and qword [rdx + 1 * rcx], rcx                                    | 48 21 0c 0a                            |
    | and qword [rbx + 1 * rcx], rcx                                    | 48 21 0c 0b                            |
    | and qword [rsp + 1 * rcx], rcx                                    | 48 21 0c 0c                            |
    | and qword [rbp + 1 * rcx], rcx                                    | 48 21 4c 0d 00                         |
    | and qword [rsi + 1 * rcx], rcx                                    | 48 21 0c 0e                            |
    | and qword [rdi + 1 * rcx], rcx                                    | 48 21 0c 0f                            |
    | and qword [r8 + 1 * rcx], rcx                                     | 49 21 0c 08                            |
    | and qword [r9 + 1 * rcx], rcx                                     | 49 21 0c 09                            |
    | and qword [r10 + 1 * rcx], rcx                                    | 49 21 0c 0a                            |
    | and qword [r11 + 1 * rcx], rcx                                    | 49 21 0c 0b                            |
    | and qword [r12 + 1 * rcx], rcx                                    | 49 21 0c 0c                            |
    | and qword [r13 + 1 * rcx], rcx                                    | 49 21 4c 0d 00                         |
    | and qword [r14 + 1 * rcx], rcx                                    | 49 21 0c 0e                            |
    | and qword [r15 + 1 * rcx], rcx                                    | 49 21 0c 0f                            |
    | and qword [rax + 1 * rax], rcx                                    | 48 21 0c 00                            |
    | and qword [rax + 1 * rdx], rcx                                    | 48 21 0c 10                            |
    | and qword [rax + 1 * rbx], rcx                                    | 48 21 0c 18                            |
    | and qword [rax + 1 * rbp], rcx                                    | 48 21 0c 28                            |
    | and qword [rax + 1 * rsi], rcx                                    | 48 21 0c 30                            |
    | and qword [rax + 1 * rdi], rcx                                    | 48 21 0c 38                            |
    | and qword [rax + 1 * r8], rcx                                     | 4a 21 0c 00                            |
    | and qword [rax + 1 * r9], rcx                                     | 4a 21 0c 08                            |
    | and qword [rax + 1 * r10], rcx                                    | 4a 21 0c 10                            |
    | and qword [rax + 1 * r11], rcx                                    | 4a 21 0c 18                            |
    | and qword [rax + 1 * r12], rcx                                    | 4a 21 0c 20                            |
    | and qword [rax + 1 * r13], rcx                                    | 4a 21 0c 28                            |
    | and qword [rax + 1 * r14], rcx                                    | 4a 21 0c 30                            |
    | and qword [rax + 1 * r15], rcx                                    | 4a 21 0c 38                            |
    | and qword [rax + 2 * rcx], rcx                                    | 48 21 0c 48                            |
    | and qword [rax + 4 * rcx], rcx                                    | 48 21 0c 88                            |
    | and qword [rax + 8 * rcx], rcx                                    | 48 21 0c c8                            |
    | and qword [r8 + 1 * r9], rcx                                      | 4b 21 0c 08                            |
    | and qword [r8 + 2 * r9], rcx                                      | 4b 21 0c 48                            |
    | and qword [r8 + 4 * r9], rcx                                      | 4b 21 0c 88                            |
    | and qword [r8 + 8 * r9], rcx                                      | 4b 21 0c c8                            |
    | and qword [1 * rcx], rcx                                          | 48 21 0c 0d 00 00 00 00                |
    | and qword [2 * rcx], rcx                                          | 48 21 0c 4d 00 00 00 00                |
    | and qword [4 * rcx], rcx                                          | 48 21 0c 8d 00 00 00 00                |
    | and qword [8 * rcx], rcx                                          | 48 21 0c cd 00 00 00 00                |
    | and qword [1 * r9], rcx                                           | 4a 21 0c 0d 00 00 00 00                |
    | and qword [2 * r9], rcx                                           | 4a 21 0c 4d 00 00 00 00                |
    | and qword [4 * r9], rcx                                           | 4a 21 0c 8d 00 00 00 00                |
    | and qword [8 * r9], rcx                                           | 4a 21 0c cd 00 00 00 00                |
    | and qword [r13 + 8 * r12], rcx                                    | 4b 21 4c e5 00                         |
    | and qword [rsp + 4 * r15], rcx                                    | 4a 21 0c bc                            |
    | and qword [rax + 1 * rcx + 0x00], rcx                             | 48 21 4c 08 00                         |
    | and qword [rax + 1 * rcx - 0x00], rcx                             | 48 21 4c 08 00                         |
    | and qword [rax + 1 * rcx + 0x01], rcx                             | 48 21 4c 08 01                         |
    | and qword [rax + 1 * rcx - 0x01], rcx                             | 48 21 4c 08 ff                         |
    | and qword [rax + 1 * rcx + 0x00000001], rcx                       | 48 21 8c 08 01 00 00 00                |
    | and qword [rax + 1 * rcx - 0x00000001], rcx                       | 48 21 8c 08 ff ff ff ff                |
    | and qword [rax + 1 * rcx + 0x7f], rcx                             | 48 21 4c 08 7f                         |
    | and qword [rax + 1 * rcx - 0x7f], rcx                             | 48 21 4c 08 81                         |
    | and qword [rax + 1 * rcx + 0x80], rcx                             | 48 21 8c 08 80 00 00 00                |
    | and qword [rax + 1 * rcx - 0x80], rcx                             | 48 21 4c 08 80                         |
    | and qword [rax + 1 * rcx - 0x81], rcx                             | 48 21 8c 08 7f ff ff ff                |
    | and qword [rax + 1 * rcx + 0xff], rcx                             | 48 21 8c 08 ff 00 00 00                |
    | and qword [rax + 1 * rcx - 0xff], rcx                             | 48 21 8c 08 01 ff ff ff                |
    | and qword [rax + 1 * rcx + 0x7fffffff], rcx                       | 48 21 8c 08 ff ff ff 7f                |
    | and qword [rax + 1 * rcx - 0x7fffffff], rcx                       | 48 21 8c 08 01 00 00 80                |
    | and qword [rax + 1 * rcx - 0x80000000], rcx                       | 48 21 8c 08 00 00 00 80                |
    | and qword [r10 + 0x7f], rcx                                       | 49 21 4a 7f                            |
    | and qword [r10 + 0x80], rcx                                       | 49 21 8a 80 00 00 00                   |
    | and qword [r10 - 0x80], rcx                                       | 49 21 4a 80                            |
    | and qword [r10 - 0x81], rcx                                       | 49 21 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and qword [rel @prev5], rcx      | 90 90 90 90 90 48 21 0d f4 ff ff ff    |
    | .prev1: nop; and qword [rel @prev1], rcx                          | 90 48 21 0d f8 ff ff ff                |
    | and qword [rel @next1], rcx; nop; .next1: nop                     | 48 21 0d 01 00 00 00 90 90             |
    | and qword [rel @next5], rcx; nop; nop; nop; nop; nop; .next5: nop | 48 21 0d 05 00 00 00 90 90 90 90 90 90 |
    | and qword [rax], rax                                              | 48 21 00                               |
    | and qword [rax], rdx                                              | 48 21 10                               |
    | and qword [rax], rbx                                              | 48 21 18                               |
    | and qword [rax], rsp                                              | 48 21 20                               |
    | and qword [rax], rbp                                              | 48 21 28                               |
    | and qword [rax], rsi                                              | 48 21 30                               |
    | and qword [rax], rdi                                              | 48 21 38                               |
    | and qword [rax], r8                                               | 4c 21 00                               |
    | and qword [rax], r9                                               | 4c 21 08                               |
    | and qword [rax], r10                                              | 4c 21 10                               |
    | and qword [rax], r11                                              | 4c 21 18                               |
    | and qword [rax], r12                                              | 4c 21 20                               |
    | and qword [rax], r13                                              | 4c 21 28                               |
    | and qword [rax], r14                                              | 4c 21 30                               |
    | and qword [rax], r15                                              | 4c 21 38                               |
    | and qword [rcx], rdx                                              | 48 21 11                               |
    | and qword [rdx], rbx                                              | 48 21 1a                               |
    | and qword [rbx], rsp                                              | 48 21 23                               |
    | and qword [rsp], rbp                                              | 48 21 2c 24                            |
    | and qword [rbp], rsi                                              | 48 21 75 00                            |
    | and qword [rsi], rdi                                              | 48 21 3e                               |
    | and qword [rdi], r8                                               | 4c 21 07                               |
    | and qword [r8], r9                                                | 4d 21 08                               |
    | and qword [r9], r10                                               | 4d 21 11                               |
    | and qword [r10], r11                                              | 4d 21 1a                               |
    | and qword [r11], r12                                              | 4d 21 23                               |
    | and qword [r12], r13                                              | 4d 21 2c 24                            |
    | and qword [r13], r14                                              | 4d 21 75 00                            |
    | and qword [r14], r15                                              | 4d 21 3e                               |
    | and qword [r15], rax                                              | 49 21 07                               |
    | and qword [rcx + 1 * rcx], rdx                                    | 48 21 14 09                            |
    | and qword [rdx + 1 * rcx], rbx                                    | 48 21 1c 0a                            |
    | and qword [rbx + 1 * rcx], rsp                                    | 48 21 24 0b                            |
    | and qword [rsp + 1 * rcx], rbp                                    | 48 21 2c 0c                            |
    | and qword [rbp + 1 * rcx], rsi                                    | 48 21 74 0d 00                         |
    | and qword [rsi + 1 * rcx], rdi                                    | 48 21 3c 0e                            |
    | and qword [rdi + 1 * rcx], r8                                     | 4c 21 04 0f                            |
    | and qword [r8 + 1 * rcx], r9                                      | 4d 21 0c 08                            |
    | and qword [r9 + 1 * rcx], r10                                     | 4d 21 14 09                            |
    | and qword [r10 + 1 * rcx], r11                                    | 4d 21 1c 0a                            |
    | and qword [r11 + 1 * rcx], r12                                    | 4d 21 24 0b                            |
    | and qword [r12 + 1 * rcx], r13                                    | 4d 21 2c 0c                            |
    | and qword [r13 + 1 * rcx], r14                                    | 4d 21 74 0d 00                         |
    | and qword [r14 + 1 * rcx], r15                                    | 4d 21 3c 0e                            |
    | and qword [r15 + 1 * rcx], rax                                    | 49 21 04 0f                            |
    | and qword [rax + 1 * rdx], rdx                                    | 48 21 14 10                            |
    | and qword [rax + 1 * rbx], rbx                                    | 48 21 1c 18                            |
    | and qword [rax + 1 * rbp], rsp                                    | 48 21 24 28                            |
    | and qword [rax + 1 * rsi], rbp                                    | 48 21 2c 30                            |
    | and qword [rax + 1 * rdi], rsi                                    | 48 21 34 38                            |
    | and qword [rax + 1 * r8], rdi                                     | 4a 21 3c 00                            |
    | and qword [rax + 1 * r9], r8                                      | 4e 21 04 08                            |
    | and qword [rax + 1 * r10], r9                                     | 4e 21 0c 10                            |
    | and qword [rax + 1 * r11], r10                                    | 4e 21 14 18                            |
    | and qword [rax + 1 * r12], r11                                    | 4e 21 1c 20                            |
    | and qword [rax + 1 * r13], r12                                    | 4e 21 24 28                            |
    | and qword [rax + 1 * r14], r13                                    | 4e 21 2c 30                            |
    | and qword [rax + 1 * r15], r14                                    | 4e 21 34 38                            |
    | and qword [rax + 2 * rcx], r15                                    | 4c 21 3c 48                            |
    | and qword [rax + 4 * rcx], rax                                    | 48 21 04 88                            |
    | and qword [r8 + 1 * r9], rdx                                      | 4b 21 14 08                            |
    | and qword [r8 + 2 * r9], rbx                                      | 4b 21 1c 48                            |
    | and qword [r8 + 4 * r9], rsp                                      | 4b 21 24 88                            |
    | and qword [r8 + 8 * r9], rbp                                      | 4b 21 2c c8                            |
    | and qword [1 * rcx], rsi                                          | 48 21 34 0d 00 00 00 00                |
    | and qword [2 * rcx], rdi                                          | 48 21 3c 4d 00 00 00 00                |
    | and qword [4 * rcx], r8                                           | 4c 21 04 8d 00 00 00 00                |
    | and qword [8 * rcx], r9                                           | 4c 21 0c cd 00 00 00 00                |
    | and qword [1 * r9], r10                                           | 4e 21 14 0d 00 00 00 00                |
    | and qword [2 * r9], r11                                           | 4e 21 1c 4d 00 00 00 00                |
    | and qword [4 * r9], r12                                           | 4e 21 24 8d 00 00 00 00                |
    | and qword [8 * r9], r13                                           | 4e 21 2c cd 00 00 00 00                |
    | and qword [r13 + 8 * r12], r14                                    | 4f 21 74 e5 00                         |
    | and qword [rsp + 4 * r15], r15                                    | 4e 21 3c bc                            |
    | and qword [rax + 1 * rcx + 0x00], rax                             | 48 21 44 08 00                         |
    | and qword [rax + 1 * rcx + 0x01], rdx                             | 48 21 54 08 01                         |
    | and qword [rax + 1 * rcx - 0x01], rbx                             | 48 21 5c 08 ff                         |
    | and qword [rax + 1 * rcx + 0x00000001], rsp                       | 48 21 a4 08 01 00 00 00                |
    | and qword [rax + 1 * rcx - 0x00000001], rbp                       | 48 21 ac 08 ff ff ff ff                |
    | and qword [rax + 1 * rcx + 0x7f], rsi                             | 48 21 74 08 7f                         |
    | and qword [rax + 1 * rcx - 0x7f], rdi                             | 48 21 7c 08 81                         |
    | and qword [rax + 1 * rcx + 0x80], r8                              | 4c 21 84 08 80 00 00 00                |
    | and qword [rax + 1 * rcx - 0x80], r9                              | 4c 21 4c 08 80                         |
    | and qword [rax + 1 * rcx - 0x81], r10                             | 4c 21 94 08 7f ff ff ff                |
    | and qword [rax + 1 * rcx + 0xff], r11                             | 4c 21 9c 08 ff 00 00 00                |
    | and qword [rax + 1 * rcx - 0xff], r12                             | 4c 21 a4 08 01 ff ff ff                |
    | and qword [rax + 1 * rcx + 0x7fffffff], r13                       | 4c 21 ac 08 ff ff ff 7f                |
    | and qword [rax + 1 * rcx - 0x7fffffff], r14                       | 4c 21 b4 08 01 00 00 80                |
    | and qword [rax + 1 * rcx - 0x80000000], r15                       | 4c 21 bc 08 00 00 00 80                |
    | and qword [r10 + 0x7f], rax                                       | 49 21 42 7f                            |
    | and qword [r10 - 0x80], rdx                                       | 49 21 52 80                            |
    | and qword [r10 - 0x81], rbx                                       | 49 21 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and qword [rel @prev5], rsp      | 90 90 90 90 90 48 21 25 f4 ff ff ff    |
    | .prev1: nop; and qword [rel @prev1], rbp                          | 90 48 21 2d f8 ff ff ff                |
    | and qword [rel @next1], rsi; nop; .next1: nop                     | 48 21 35 01 00 00 00 90 90             |
    | and qword [rel @next5], rdi; nop; nop; nop; nop; nop; .next5: nop | 48 21 3d 05 00 00 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_and_addr64_reg64():
    encode(AND_ADDR64_REG64)


AND_ADDR32_IMM8 = """
    | ------------------------------------------------------------------ | -------------------------------------- |
    | instruction                                                        | encoding                               |
    | ------------------------------------------------------------------ | -------------------------------------- |
    | and dword [rax], 0x01                                              | 83 20 01                               |
    | and dword [rcx], 0x01                                              | 83 21 01                               |
    | and dword [rdx], 0x01                                              | 83 22 01                               |
    | and dword [rbx], 0x01                                              | 83 23 01                               |
    | and dword [rsp], 0x01                                              | 83 24 24 01                            |
    | and dword [rbp], 0x01                                              | 83 65 00 01                            |
    | and dword [rsi], 0x01                                              | 83 26 01                               |
    | and dword [rdi], 0x01                                              | 83 27 01                               |
    | and dword [r8], 0x01                                               | 41 83 20 01                            |
    | and dword [r9], 0x01                                               | 41 83 21 01                            |
    | and dword [r10], 0x01                                              | 41 83 22 01                            |
    | and dword [r11], 0x01                                              | 41 83 23 01                            |
    | and dword [r12], 0x01                                              | 41 83 24 24 01                         |
    | and dword [r13], 0x01                                              | 41 83 65 00 01                         |
    | and dword [r14], 0x01                                              | 41 83 26 01                            |
    | and dword [r15], 0x01                                              | 41 83 27 01                            |
    | and dword [rax + 1 * rcx], 0x01                                    | 83 24 08 01                            |
    | and dword [rcx + 1 * rcx], 0x01                                    | 83 24 09 01                            |
    | and dword [rdx + 1 * rcx], 0x01                                    | 83 24 0a 01                            |
    | and dword [rbx + 1 * rcx], 0x01                                    | 83 24 0b 01                            |
    | and dword [rsp + 1 * rcx], 0x01                                    | 83 24 0c 01                            |
    | and dword [rbp + 1 * rcx], 0x01                                    | 83 64 0d 00 01                         |
    | and dword [rsi + 1 * rcx], 0x01                                    | 83 24 0e 01                            |
    | and dword [rdi + 1 * rcx], 0x01                                    | 83 24 0f 01                            |
    | and dword [r8 + 1 * rcx], 0x01                                     | 41 83 24 08 01                         |
    | and dword [r9 + 1 * rcx], 0x01                                     | 41 83 24 09 01                         |
    | and dword [r10 + 1 * rcx], 0x01                                    | 41 83 24 0a 01                         |
    | and dword [r11 + 1 * rcx], 0x01                                    | 41 83 24 0b 01                         |
    | and dword [r12 + 1 * rcx], 0x01                                    | 41 83 24 0c 01                         |
    | and dword [r13 + 1 * rcx], 0x01                                    | 41 83 64 0d 00 01                      |
    | and dword [r14 + 1 * rcx], 0x01                                    | 41 83 24 0e 01                         |
    | and dword [r15 + 1 * rcx], 0x01                                    | 41 83 24 0f 01                         |
    | and dword [rax + 1 * rax], 0x01                                    | 83 24 00 01                            |
    | and dword [rax + 1 * rdx], 0x01                                    | 83 24 10 01                            |
    | and dword [rax + 1 * rbx], 0x01                                    | 83 24 18 01                            |
    | and dword [rax + 1 * rbp], 0x01                                    | 83 24 28 01                            |
    | and dword [rax + 1 * rsi], 0x01                                    | 83 24 30 01                            |
    | and dword [rax + 1 * rdi], 0x01                                    | 83 24 38 01                            |
    | and dword [rax + 1 * r8], 0x01                                     | 42 83 24 00 01                         |
    | and dword [rax + 1 * r9], 0x01                                     | 42 83 24 08 01                         |
    | and dword [rax + 1 * r10], 0x01                                    | 42 83 24 10 01                         |
    | and dword [rax + 1 * r11], 0x01                                    | 42 83 24 18 01                         |
    | and dword [rax + 1 * r12], 0x01                                    | 42 83 24 20 01                         |
    | and dword [rax + 1 * r13], 0x01                                    | 42 83 24 28 01                         |
    | and dword [rax + 1 * r14], 0x01                                    | 42 83 24 30 01                         |
    | and dword [rax + 1 * r15], 0x01                                    | 42 83 24 38 01                         |
    | and dword [rax + 2 * rcx], 0x01                                    | 83 24 48 01                            |
    | and dword [rax + 4 * rcx], 0x01                                    | 83 24 88 01                            |
    | and dword [rax + 8 * rcx], 0x01                                    | 83 24 c8 01                            |
    | and dword [r8 + 1 * r9], 0x01                                      | 43 83 24 08 01                         |
    | and dword [r8 + 2 * r9], 0x01                                      | 43 83 24 48 01                         |
    | and dword [r8 + 4 * r9], 0x01                                      | 43 83 24 88 01                         |
    | and dword [r8 + 8 * r9], 0x01                                      | 43 83 24 c8 01                         |
    | and dword [1 * rcx], 0x01                                          | 83 24 0d 00 00 00 00 01                |
    | and dword [2 * rcx], 0x01                                          | 83 24 4d 00 00 00 00 01                |
    | and dword [4 * rcx], 0x01                                          | 83 24 8d 00 00 00 00 01                |
    | and dword [8 * rcx], 0x01                                          | 83 24 cd 00 00 00 00 01                |
    | and dword [1 * r9], 0x01                                           | 42 83 24 0d 00 00 00 00 01             |
    | and dword [2 * r9], 0x01                                           | 42 83 24 4d 00 00 00 00 01             |
    | and dword [4 * r9], 0x01                                           | 42 83 24 8d 00 00 00 00 01             |
    | and dword [8 * r9], 0x01                                           | 42 83 24 cd 00 00 00 00 01             |
    | and dword [r13 + 8 * r12], 0x01                                    | 43 83 64 e5 00 01                      |
    | and dword [rsp + 4 * r15], 0x01                                    | 42 83 24 bc 01                         |
    | and dword [rax + 1 * rcx + 0x00], 0x01                             | 83 64 08 00 01                         |
    | and dword [rax + 1 * rcx - 0x00], 0x01                             | 83 64 08 00 01                         |
    | and dword [rax + 1 * rcx + 0x01], 0x01                             | 83 64 08 01 01                         |
    | and dword [rax + 1 * rcx - 0x01], 0x01                             | 83 64 08 ff 01                         |
    | and dword [rax + 1 * rcx + 0x00000001], 0x01                       | 83 a4 08 01 00 00 00 01                |
    | and dword [rax + 1 * rcx - 0x00000001], 0x01                       | 83 a4 08 ff ff ff ff 01                |
    | and dword [rax + 1 * rcx + 0x7f], 0x01                             | 83 64 08 7f 01                         |
    | and dword [rax + 1 * rcx - 0x7f], 0x01                             | 83 64 08 81 01                         |
    | and dword [rax + 1 * rcx + 0x80], 0x01                             | 83 a4 08 80 00 00 00 01                |
    | and dword [rax + 1 * rcx - 0x80], 0x01                             | 83 64 08 80 01                         |
    | and dword [rax + 1 * rcx - 0x81], 0x01                             | 83 a4 08 7f ff ff ff 01                |
    | and dword [rax + 1 * rcx + 0xff], 0x01                             | 83 a4 08 ff 00 00 00 01                |
    | and dword [rax + 1 * rcx - 0xff], 0x01                             | 83 a4 08 01 ff ff ff 01                |
    | and dword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 83 a4 08 ff ff ff 7f 01                |
    | and dword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 83 a4 08 01 00 00 80 01                |
    | and dword [rax + 1 * rcx - 0x80000000], 0x01                       | 83 a4 08 00 00 00 80 01                |
    | and dword [r10 + 0x7f], 0x01                                       | 41 83 62 7f 01                         |
    | and dword [r10 + 0x80], 0x01                                       | 41 83 a2 80 00 00 00 01                |
    | and dword [r10 - 0x80], 0x01                                       | 41 83 62 80 01                         |
    | and dword [r10 - 0x81], 0x01                                       | 41 83 a2 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; and dword [rel @prev5], 0x01      | 90 90 90 90 90 83 25 f4 ff ff ff 01    |
    | .prev1: nop; and dword [rel @prev1], 0x01                          | 90 83 25 f8 ff ff ff 01                |
    | and dword [rel @next1], 0x01; nop; .next1: nop                     | 83 25 01 00 00 00 01 90 90             |
    | and dword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 83 25 05 00 00 00 01 90 90 90 90 90 90 |
    | and dword [rax], 0x00                                              | 83 20 00                               |
    | and dword [rax], 0x7f                                              | 83 20 7f                               |
    | and dword [rax], 0x80                                              | 83 20 80                               |
    | and dword [rax], 0xff                                              | 83 20 ff                               |
    | and dword [rcx], 0x7f                                              | 83 21 7f                               |
    | and dword [rdx], 0x80                                              | 83 22 80                               |
    | and dword [rbx], 0xff                                              | 83 23 ff                               |
    | and dword [rsp], 0x00                                              | 83 24 24 00                            |
    | and dword [rsi], 0x7f                                              | 83 26 7f                               |
    | and dword [rdi], 0x80                                              | 83 27 80                               |
    | and dword [r8], 0xff                                               | 41 83 20 ff                            |
    | and dword [r9], 0x00                                               | 41 83 21 00                            |
    | and dword [r11], 0x7f                                              | 41 83 23 7f                            |
    | and dword [r12], 0x80                                              | 41 83 24 24 80                         |
    | and dword [r13], 0xff                                              | 41 83 65 00 ff                         |
    | and dword [r14], 0x00                                              | 41 83 26 00                            |
    | and dword [rax + 1 * rcx], 0x7f                                    | 83 24 08 7f                            |
    | and dword [rcx + 1 * rcx], 0x80                                    | 83 24 09 80                            |
    | and dword [rdx + 1 * rcx], 0xff                                    | 83 24 0a ff                            |
    | and dword [rbx + 1 * rcx], 0x00                                    | 83 24 0b 00                            |
    | and dword [rbp + 1 * rcx], 0x7f                                    | 83 64 0d 00 7f                         |
    | and dword [rsi + 1 * rcx], 0x80                                    | 83 24 0e 80                            |
    | and dword [rdi + 1 * rcx], 0xff                                    | 83 24 0f ff                            |
    | and dword [r8 + 1 * rcx], 0x00                                     | 41 83 24 08 00                         |
    | and dword [r10 + 1 * rcx], 0x7f                                    | 41 83 24 0a 7f                         |
    | and dword [r11 + 1 * rcx], 0x80                                    | 41 83 24 0b 80                         |
    | and dword [r12 + 1 * rcx], 0xff                                    | 41 83 24 0c ff                         |
    | and dword [r13 + 1 * rcx], 0x00                                    | 41 83 64 0d 00 00                      |
    | and dword [r15 + 1 * rcx], 0x7f                                    | 41 83 24 0f 7f                         |
    | and dword [rax + 1 * rax], 0x80                                    | 83 24 00 80                            |
    | and dword [rax + 1 * rdx], 0xff                                    | 83 24 10 ff                            |
    | and dword [rax + 1 * rbx], 0x00                                    | 83 24 18 00                            |
    | and dword [rax + 1 * rsi], 0x7f                                    | 83 24 30 7f                            |
    | and dword [rax + 1 * rdi], 0x80                                    | 83 24 38 80                            |
    | and dword [rax + 1 * r8], 0xff                                     | 42 83 24 00 ff                         |
    | and dword [rax + 1 * r9], 0x00                                     | 42 83 24 08 00                         |
    | and dword [rax + 1 * r11], 0x7f                                    | 42 83 24 18 7f                         |
    | and dword [rax + 1 * r12], 0x80                                    | 42 83 24 20 80                         |
    | and dword [rax + 1 * r13], 0xff                                    | 42 83 24 28 ff                         |
    | and dword [rax + 1 * r14], 0x00                                    | 42 83 24 30 00                         |
    | and dword [rax + 2 * rcx], 0x7f                                    | 83 24 48 7f                            |
    | and dword [rax + 4 * rcx], 0x80                                    | 83 24 88 80                            |
    | and dword [rax + 8 * rcx], 0xff                                    | 83 24 c8 ff                            |
    | and dword [r8 + 1 * r9], 0x00                                      | 43 83 24 08 00                         |
    | and dword [r8 + 4 * r9], 0x7f                                      | 43 83 24 88 7f                         |
    | and dword [r8 + 8 * r9], 0x80                                      | 43 83 24 c8 80                         |
    | and dword [1 * rcx], 0xff                                          | 83 24 0d 00 00 00 00 ff                |
    | and dword [2 * rcx], 0x00                                          | 83 24 4d 00 00 00 00 00                |
    | and dword [8 * rcx], 0x7f                                          | 83 24 cd 00 00 00 00 7f                |
    | and dword [1 * r9], 0x80                                           | 42 83 24 0d 00 00 00 00 80             |
    | and dword [2 * r9], 0xff                                           | 42 83 24 4d 00 00 00 00 ff             |
    | and dword [4 * r9], 0x00                                           | 42 83 24 8d 00 00 00 00 00             |
    | and dword [r13 + 8 * r12], 0x7f                                    | 43 83 64 e5 00 7f                      |
    | and dword [rsp + 4 * r15], 0x80                                    | 42 83 24 bc 80                         |
    | and dword [rax + 1 * rcx + 0x00], 0xff                             | 83 64 08 00 ff                         |
    | and dword [rax + 1 * rcx - 0x00], 0x00                             | 83 64 08 00 00                         |
    | and dword [rax + 1 * rcx - 0x01], 0x7f                             | 83 64 08 ff 7f                         |
    | and dword [rax + 1 * rcx + 0x00000001], 0x80                       | 83 a4 08 01 00 00 00 80                |
    | and dword [rax + 1 * rcx - 0x00000001], 0xff                       | 83 a4 08 ff ff ff ff ff                |
    | and dword [rax + 1 * rcx + 0x7f], 0x00                             | 83 64 08 7f 00                         |
    | and dword [rax + 1 * rcx + 0x80], 0x7f                             | 83 a4 08 80 00 00 00 7f                |
    | and dword [rax + 1 * rcx - 0x80], 0x80                             | 83 64 08 80 80                         |
    | and dword [rax + 1 * rcx - 0x81], 0xff                             | 83 a4 08 7f ff ff ff ff                |
    | and dword [rax + 1 * rcx + 0xff], 0x00                             | 83 a4 08 ff 00 00 00 00                |
    | and dword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 83 a4 08 ff ff ff 7f 7f                |
    | and dword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 83 a4 08 01 00 00 80 80                |
    | and dword [rax + 1 * rcx - 0x80000000], 0xff                       | 83 a4 08 00 00 00 80 ff                |
    | and dword [r10 + 0x7f], 0x00                                       | 41 83 62 7f 00                         |
    | and dword [r10 - 0x80], 0x7f                                       | 41 83 62 80 7f                         |
    | and dword [r10 - 0x81], 0x80                                       | 41 83 a2 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; and dword [rel @prev5], 0xff      | 90 90 90 90 90 83 25 f4 ff ff ff ff    |
    | .prev1: nop; and dword [rel @prev1], 0x00                          | 90 83 25 f8 ff ff ff 00                |
    | and dword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 83 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | -------------------------------------- |
"""


def can_encode_and_addr32_imm8():
    encode(AND_ADDR32_IMM8)


AND_ADDR32_IMM32 = """
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
    | instruction                                                              | encoding                                        |
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
    | and dword [rax], 0x00000001                                              | 81 20 01 00 00 00                               |
    | and dword [rcx], 0x00000001                                              | 81 21 01 00 00 00                               |
    | and dword [rdx], 0x00000001                                              | 81 22 01 00 00 00                               |
    | and dword [rbx], 0x00000001                                              | 81 23 01 00 00 00                               |
    | and dword [rsp], 0x00000001                                              | 81 24 24 01 00 00 00                            |
    | and dword [rbp], 0x00000001                                              | 81 65 00 01 00 00 00                            |
    | and dword [rsi], 0x00000001                                              | 81 26 01 00 00 00                               |
    | and dword [rdi], 0x00000001                                              | 81 27 01 00 00 00                               |
    | and dword [r8], 0x00000001                                               | 41 81 20 01 00 00 00                            |
    | and dword [r9], 0x00000001                                               | 41 81 21 01 00 00 00                            |
    | and dword [r10], 0x00000001                                              | 41 81 22 01 00 00 00                            |
    | and dword [r11], 0x00000001                                              | 41 81 23 01 00 00 00                            |
    | and dword [r12], 0x00000001                                              | 41 81 24 24 01 00 00 00                         |
    | and dword [r13], 0x00000001                                              | 41 81 65 00 01 00 00 00                         |
    | and dword [r14], 0x00000001                                              | 41 81 26 01 00 00 00                            |
    | and dword [r15], 0x00000001                                              | 41 81 27 01 00 00 00                            |
    | and dword [rax + 1 * rcx], 0x00000001                                    | 81 24 08 01 00 00 00                            |
    | and dword [rcx + 1 * rcx], 0x00000001                                    | 81 24 09 01 00 00 00                            |
    | and dword [rdx + 1 * rcx], 0x00000001                                    | 81 24 0a 01 00 00 00                            |
    | and dword [rbx + 1 * rcx], 0x00000001                                    | 81 24 0b 01 00 00 00                            |
    | and dword [rsp + 1 * rcx], 0x00000001                                    | 81 24 0c 01 00 00 00                            |
    | and dword [rbp + 1 * rcx], 0x00000001                                    | 81 64 0d 00 01 00 00 00                         |
    | and dword [rsi + 1 * rcx], 0x00000001                                    | 81 24 0e 01 00 00 00                            |
    | and dword [rdi + 1 * rcx], 0x00000001                                    | 81 24 0f 01 00 00 00                            |
    | and dword [r8 + 1 * rcx], 0x00000001                                     | 41 81 24 08 01 00 00 00                         |
    | and dword [r9 + 1 * rcx], 0x00000001                                     | 41 81 24 09 01 00 00 00                         |
    | and dword [r10 + 1 * rcx], 0x00000001                                    | 41 81 24 0a 01 00 00 00                         |
    | and dword [r11 + 1 * rcx], 0x00000001                                    | 41 81 24 0b 01 00 00 00                         |
    | and dword [r12 + 1 * rcx], 0x00000001                                    | 41 81 24 0c 01 00 00 00                         |
    | and dword [r13 + 1 * rcx], 0x00000001                                    | 41 81 64 0d 00 01 00 00 00                      |
    | and dword [r14 + 1 * rcx], 0x00000001                                    | 41 81 24 0e 01 00 00 00                         |
    | and dword [r15 + 1 * rcx], 0x00000001                                    | 41 81 24 0f 01 00 00 00                         |
    | and dword [rax + 1 * rax], 0x00000001                                    | 81 24 00 01 00 00 00                            |
    | and dword [rax + 1 * rdx], 0x00000001                                    | 81 24 10 01 00 00 00                            |
    | and dword [rax + 1 * rbx], 0x00000001                                    | 81 24 18 01 00 00 00                            |
    | and dword [rax + 1 * rbp], 0x00000001                                    | 81 24 28 01 00 00 00                            |
    | and dword [rax + 1 * rsi], 0x00000001                                    | 81 24 30 01 00 00 00                            |
    | and dword [rax + 1 * rdi], 0x00000001                                    | 81 24 38 01 00 00 00                            |
    | and dword [rax + 1 * r8], 0x00000001                                     | 42 81 24 00 01 00 00 00                         |
    | and dword [rax + 1 * r9], 0x00000001                                     | 42 81 24 08 01 00 00 00                         |
    | and dword [rax + 1 * r10], 0x00000001                                    | 42 81 24 10 01 00 00 00                         |
    | and dword [rax + 1 * r11], 0x00000001                                    | 42 81 24 18 01 00 00 00                         |
    | and dword [rax + 1 * r12], 0x00000001                                    | 42 81 24 20 01 00 00 00                         |
    | and dword [rax + 1 * r13], 0x00000001                                    | 42 81 24 28 01 00 00 00                         |
    | and dword [rax + 1 * r14], 0x00000001                                    | 42 81 24 30 01 00 00 00                         |
    | and dword [rax + 1 * r15], 0x00000001                                    | 42 81 24 38 01 00 00 00                         |
    | and dword [rax + 2 * rcx], 0x00000001                                    | 81 24 48 01 00 00 00                            |
    | and dword [rax + 4 * rcx], 0x00000001                                    | 81 24 88 01 00 00 00                            |
    | and dword [rax + 8 * rcx], 0x00000001                                    | 81 24 c8 01 00 00 00                            |
    | and dword [r8 + 1 * r9], 0x00000001                                      | 43 81 24 08 01 00 00 00                         |
    | and dword [r8 + 2 * r9], 0x00000001                                      | 43 81 24 48 01 00 00 00                         |
    | and dword [r8 + 4 * r9], 0x00000001                                      | 43 81 24 88 01 00 00 00                         |
    | and dword [r8 + 8 * r9], 0x00000001                                      | 43 81 24 c8 01 00 00 00                         |
    | and dword [1 * rcx], 0x00000001                                          | 81 24 0d 00 00 00 00 01 00 00 00                |
    | and dword [2 * rcx], 0x00000001                                          | 81 24 4d 00 00 00 00 01 00 00 00                |
    | and dword [4 * rcx], 0x00000001                                          | 81 24 8d 00 00 00 00 01 00 00 00                |
    | and dword [8 * rcx], 0x00000001                                          | 81 24 cd 00 00 00 00 01 00 00 00                |
    | and dword [1 * r9], 0x00000001                                           | 42 81 24 0d 00 00 00 00 01 00 00 00             |
    | and dword [2 * r9], 0x00000001                                           | 42 81 24 4d 00 00 00 00 01 00 00 00             |
    | and dword [4 * r9], 0x00000001                                           | 42 81 24 8d 00 00 00 00 01 00 00 00             |
    | and dword [8 * r9], 0x00000001                                           | 42 81 24 cd 00 00 00 00 01 00 00 00             |
    | and dword [r13 + 8 * r12], 0x00000001                                    | 43 81 64 e5 00 01 00 00 00                      |
    | and dword [rsp + 4 * r15], 0x00000001                                    | 42 81 24 bc 01 00 00 00                         |
    | and dword [rax + 1 * rcx + 0x00], 0x00000001                             | 81 64 08 00 01 00 00 00                         |
    | and dword [rax + 1 * rcx - 0x00], 0x00000001                             | 81 64 08 00 01 00 00 00                         |
    | and dword [rax + 1 * rcx + 0x01], 0x00000001                             | 81 64 08 01 01 00 00 00                         |
    | and dword [rax + 1 * rcx - 0x01], 0x00000001                             | 81 64 08 ff 01 00 00 00                         |
    | and dword [rax + 1 * rcx + 0x00000001], 0x00000001                       | 81 a4 08 01 00 00 00 01 00 00 00                |
    | and dword [rax + 1 * rcx - 0x00000001], 0x00000001                       | 81 a4 08 ff ff ff ff 01 00 00 00                |
    | and dword [rax + 1 * rcx + 0x7f], 0x00000001                             | 81 64 08 7f 01 00 00 00                         |
    | and dword [rax + 1 * rcx - 0x7f], 0x00000001                             | 81 64 08 81 01 00 00 00                         |
    | and dword [rax + 1 * rcx + 0x80], 0x00000001                             | 81 a4 08 80 00 00 00 01 00 00 00                |
    | and dword [rax + 1 * rcx - 0x80], 0x00000001                             | 81 64 08 80 01 00 00 00                         |
    | and dword [rax + 1 * rcx - 0x81], 0x00000001                             | 81 a4 08 7f ff ff ff 01 00 00 00                |
    | and dword [rax + 1 * rcx + 0xff], 0x00000001                             | 81 a4 08 ff 00 00 00 01 00 00 00                |
    | and dword [rax + 1 * rcx - 0xff], 0x00000001                             | 81 a4 08 01 ff ff ff 01 00 00 00                |
    | and dword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | 81 a4 08 ff ff ff 7f 01 00 00 00                |
    | and dword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | 81 a4 08 01 00 00 80 01 00 00 00                |
    | and dword [rax + 1 * rcx - 0x80000000], 0x00000001                       | 81 a4 08 00 00 00 80 01 00 00 00                |
    | and dword [r10 + 0x7f], 0x00000001                                       | 41 81 62 7f 01 00 00 00                         |
    | and dword [r10 + 0x80], 0x00000001                                       | 41 81 a2 80 00 00 00 01 00 00 00                |
    | and dword [r10 - 0x80], 0x00000001                                       | 41 81 62 80 01 00 00 00                         |
    | and dword [r10 - 0x81], 0x00000001                                       | 41 81 a2 7f ff ff ff 01 00 00 00                |
    | .prev5: nop; nop; nop; nop; nop; and dword [rel @prev5], 0x00000001      | 90 90 90 90 90 81 25 f1 ff ff ff 01 00 00 00    |
    | .prev1: nop; and dword [rel @prev1], 0x00000001                          | 90 81 25 f5 ff ff ff 01 00 00 00                |
    | and dword [rel @next1], 0x00000001; nop; .next1: nop                     | 81 25 01 00 00 00 01 00 00 00 90 90             |
    | and dword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | 81 25 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | and dword [rax], 0x00000000                                              | 81 20 00 00 00 00                               |
    | and dword [rax], 0x0000007f                                              | 81 20 7f 00 00 00                               |
    | and dword [rax], 0x00000080                                              | 81 20 80 00 00 00                               |
    | and dword [rax], 0x000000ff                                              | 81 20 ff 00 00 00                               |
    | and dword [rax], 0x00000100                                              | 81 20 00 01 00 00                               |
    | and dword [rax], 0x00007fff                                              | 81 20 ff 7f 00 00                               |
    | and dword [rax], 0x00008000                                              | 81 20 00 80 00 00                               |
    | and dword [rax], 0x0000ffff                                              | 81 20 ff ff 00 00                               |
    | and dword [rax], 0x00010000                                              | 81 20 00 00 01 00                               |
    | and dword [rax], 0x7fffffff                                              | 81 20 ff ff ff 7f                               |
    | and dword [rax], 0x80000000                                              | 81 20 00 00 00 80                               |
    | and dword [rax], 0xffffffff                                              | 81 20 ff ff ff ff                               |
    | and dword [rcx], 0x0000007f                                              | 81 21 7f 00 00 00                               |
    | and dword [rdx], 0x00000080                                              | 81 22 80 00 00 00                               |
    | and dword [rbx], 0x000000ff                                              | 81 23 ff 00 00 00                               |
    | and dword [rsp], 0x00000100                                              | 81 24 24 00 01 00 00                            |
    | and dword [rbp], 0x00007fff                                              | 81 65 00 ff 7f 00 00                            |
    | and dword [rsi], 0x00008000                                              | 81 26 00 80 00 00                               |
    | and dword [rdi], 0x0000ffff                                              | 81 27 ff ff 00 00                               |
    | and dword [r8], 0x00010000                                               | 41 81 20 00 00 01 00                            |
    | and dword [r9], 0x7fffffff                                               | 41 81 21 ff ff ff 7f                            |
    | and dword [r10], 0x80000000                                              | 41 81 22 00 00 00 80                            |
    | and dword [r11], 0xffffffff                                              | 41 81 23 ff ff ff ff                            |
    | and dword [r12], 0x00000000                                              | 41 81 24 24 00 00 00 00                         |
    | and dword [r14], 0x0000007f                                              | 41 81 26 7f 00 00 00                            |
    | and dword [r15], 0x00000080                                              | 41 81 27 80 00 00 00                            |
    | and dword [rax + 1 * rcx], 0x000000ff                                    | 81 24 08 ff 00 00 00                            |
    | and dword [rcx + 1 * rcx], 0x00000100                                    | 81 24 09 00 01 00 00                            |
    | and dword [rdx + 1 * rcx], 0x00007fff                                    | 81 24 0a ff 7f 00 00                            |
    | and dword [rbx + 1 * rcx], 0x00008000                                    | 81 24 0b 00 80 00 00                            |
    | and dword [rsp + 1 * rcx], 0x0000ffff                                    | 81 24 0c ff ff 00 00                            |
    | and dword [rbp + 1 * rcx], 0x00010000                                    | 81 64 0d 00 00 00 01 00                         |
    | and dword [rsi + 1 * rcx], 0x7fffffff                                    | 81 24 0e ff ff ff 7f                            |
    | and dword [rdi + 1 * rcx], 0x80000000                                    | 81 24 0f 00 00 00 80                            |
    | and dword [r8 + 1 * rcx], 0xffffffff                                     | 41 81 24 08 ff ff ff ff                         |
    | and dword [r9 + 1 * rcx], 0x00000000                                     | 41 81 24 09 00 00 00 00                         |
    | and dword [r11 + 1 * rcx], 0x0000007f                                    | 41 81 24 0b 7f 00 00 00                         |
    | and dword [r12 + 1 * rcx], 0x00000080                                    | 41 81 24 0c 80 00 00 00                         |
    | and dword [r13 + 1 * rcx], 0x000000ff                                    | 41 81 64 0d 00 ff 00 00 00                      |
    | and dword [r14 + 1 * rcx], 0x00000100                                    | 41 81 24 0e 00 01 00 00                         |
    | and dword [r15 + 1 * rcx], 0x00007fff                                    | 41 81 24 0f ff 7f 00 00                         |
    | and dword [rax + 1 * rax], 0x00008000                                    | 81 24 00 00 80 00 00                            |
    | and dword [rax + 1 * rdx], 0x0000ffff                                    | 81 24 10 ff ff 00 00                            |
    | and dword [rax + 1 * rbx], 0x00010000                                    | 81 24 18 00 00 01 00                            |
    | and dword [rax + 1 * rbp], 0x7fffffff                                    | 81 24 28 ff ff ff 7f                            |
    | and dword [rax + 1 * rsi], 0x80000000                                    | 81 24 30 00 00 00 80                            |
    | and dword [rax + 1 * rdi], 0xffffffff                                    | 81 24 38 ff ff ff ff                            |
    | and dword [rax + 1 * r8], 0x00000000                                     | 42 81 24 00 00 00 00 00                         |
    | and dword [rax + 1 * r10], 0x0000007f                                    | 42 81 24 10 7f 00 00 00                         |
    | and dword [rax + 1 * r11], 0x00000080                                    | 42 81 24 18 80 00 00 00                         |
    | and dword [rax + 1 * r12], 0x000000ff                                    | 42 81 24 20 ff 00 00 00                         |
    | and dword [rax + 1 * r13], 0x00000100                                    | 42 81 24 28 00 01 00 00                         |
    | and dword [rax + 1 * r14], 0x00007fff                                    | 42 81 24 30 ff 7f 00 00                         |
    | and dword [rax + 1 * r15], 0x00008000                                    | 42 81 24 38 00 80 00 00                         |
    | and dword [rax + 2 * rcx], 0x0000ffff                                    | 81 24 48 ff ff 00 00                            |
    | and dword [rax + 4 * rcx], 0x00010000                                    | 81 24 88 00 00 01 00                            |
    | and dword [rax + 8 * rcx], 0x7fffffff                                    | 81 24 c8 ff ff ff 7f                            |
    | and dword [r8 + 1 * r9], 0x80000000                                      | 43 81 24 08 00 00 00 80                         |
    | and dword [r8 + 2 * r9], 0xffffffff                                      | 43 81 24 48 ff ff ff ff                         |
    | and dword [r8 + 4 * r9], 0x00000000                                      | 43 81 24 88 00 00 00 00                         |
    | and dword [1 * rcx], 0x0000007f                                          | 81 24 0d 00 00 00 00 7f 00 00 00                |
    | and dword [2 * rcx], 0x00000080                                          | 81 24 4d 00 00 00 00 80 00 00 00                |
    | and dword [4 * rcx], 0x000000ff                                          | 81 24 8d 00 00 00 00 ff 00 00 00                |
    | and dword [8 * rcx], 0x00000100                                          | 81 24 cd 00 00 00 00 00 01 00 00                |
    | and dword [1 * r9], 0x00007fff                                           | 42 81 24 0d 00 00 00 00 ff 7f 00 00             |
    | and dword [2 * r9], 0x00008000                                           | 42 81 24 4d 00 00 00 00 00 80 00 00             |
    | and dword [4 * r9], 0x0000ffff                                           | 42 81 24 8d 00 00 00 00 ff ff 00 00             |
    | and dword [8 * r9], 0x00010000                                           | 42 81 24 cd 00 00 00 00 00 00 01 00             |
    | and dword [r13 + 8 * r12], 0x7fffffff                                    | 43 81 64 e5 00 ff ff ff 7f                      |
    | and dword [rsp + 4 * r15], 0x80000000                                    | 42 81 24 bc 00 00 00 80                         |
    | and dword [rax + 1 * rcx + 0x00], 0xffffffff                             | 81 64 08 00 ff ff ff ff                         |
    | and dword [rax + 1 * rcx - 0x00], 0x00000000                             | 81 64 08 00 00 00 00 00                         |
    | and dword [rax + 1 * rcx - 0x01], 0x0000007f                             | 81 64 08 ff 7f 00 00 00                         |
    | and dword [rax + 1 * rcx + 0x00000001], 0x00000080                       | 81 a4 08 01 00 00 00 80 00 00 00                |
    | and dword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | 81 a4 08 ff ff ff ff ff 00 00 00                |
    | and dword [rax + 1 * rcx + 0x7f], 0x00000100                             | 81 64 08 7f 00 01 00 00                         |
    | and dword [rax + 1 * rcx - 0x7f], 0x00007fff                             | 81 64 08 81 ff 7f 00 00                         |
    | and dword [rax + 1 * rcx + 0x80], 0x00008000                             | 81 a4 08 80 00 00 00 00 80 00 00                |
    | and dword [rax + 1 * rcx - 0x80], 0x0000ffff                             | 81 64 08 80 ff ff 00 00                         |
    | and dword [rax + 1 * rcx - 0x81], 0x00010000                             | 81 a4 08 7f ff ff ff 00 00 01 00                |
    | and dword [rax + 1 * rcx + 0xff], 0x7fffffff                             | 81 a4 08 ff 00 00 00 ff ff ff 7f                |
    | and dword [rax + 1 * rcx - 0xff], 0x80000000                             | 81 a4 08 01 ff ff ff 00 00 00 80                |
    | and dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | 81 a4 08 ff ff ff 7f ff ff ff ff                |
    | and dword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | 81 a4 08 01 00 00 80 00 00 00 00                |
    | and dword [r10 + 0x7f], 0x0000007f                                       | 41 81 62 7f 7f 00 00 00                         |
    | and dword [r10 + 0x80], 0x00000080                                       | 41 81 a2 80 00 00 00 80 00 00 00                |
    | and dword [r10 - 0x80], 0x000000ff                                       | 41 81 62 80 ff 00 00 00                         |
    | and dword [r10 - 0x81], 0x00000100                                       | 41 81 a2 7f ff ff ff 00 01 00 00                |
    | .prev5: nop; nop; nop; nop; nop; and dword [rel @prev5], 0x00007fff      | 90 90 90 90 90 81 25 f1 ff ff ff ff 7f 00 00    |
    | .prev1: nop; and dword [rel @prev1], 0x00008000                          | 90 81 25 f5 ff ff ff 00 80 00 00                |
    | and dword [rel @next1], 0x0000ffff; nop; .next1: nop                     | 81 25 01 00 00 00 ff ff 00 00 90 90             |
    | and dword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | 81 25 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
"""


def can_encode_and_addr32_imm32():
    encode(AND_ADDR32_IMM32)


AND_ADDR32_REG32 = """
    | ----------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                       | encoding                            |
    | ----------------------------------------------------------------- | ----------------------------------- |
    | and dword [rax], ecx                                              | 21 08                               |
    | and dword [rcx], ecx                                              | 21 09                               |
    | and dword [rdx], ecx                                              | 21 0a                               |
    | and dword [rbx], ecx                                              | 21 0b                               |
    | and dword [rsp], ecx                                              | 21 0c 24                            |
    | and dword [rbp], ecx                                              | 21 4d 00                            |
    | and dword [rsi], ecx                                              | 21 0e                               |
    | and dword [rdi], ecx                                              | 21 0f                               |
    | and dword [r8], ecx                                               | 41 21 08                            |
    | and dword [r9], ecx                                               | 41 21 09                            |
    | and dword [r10], ecx                                              | 41 21 0a                            |
    | and dword [r11], ecx                                              | 41 21 0b                            |
    | and dword [r12], ecx                                              | 41 21 0c 24                         |
    | and dword [r13], ecx                                              | 41 21 4d 00                         |
    | and dword [r14], ecx                                              | 41 21 0e                            |
    | and dword [r15], ecx                                              | 41 21 0f                            |
    | and dword [rax + 1 * rcx], ecx                                    | 21 0c 08                            |
    | and dword [rcx + 1 * rcx], ecx                                    | 21 0c 09                            |
    | and dword [rdx + 1 * rcx], ecx                                    | 21 0c 0a                            |
    | and dword [rbx + 1 * rcx], ecx                                    | 21 0c 0b                            |
    | and dword [rsp + 1 * rcx], ecx                                    | 21 0c 0c                            |
    | and dword [rbp + 1 * rcx], ecx                                    | 21 4c 0d 00                         |
    | and dword [rsi + 1 * rcx], ecx                                    | 21 0c 0e                            |
    | and dword [rdi + 1 * rcx], ecx                                    | 21 0c 0f                            |
    | and dword [r8 + 1 * rcx], ecx                                     | 41 21 0c 08                         |
    | and dword [r9 + 1 * rcx], ecx                                     | 41 21 0c 09                         |
    | and dword [r10 + 1 * rcx], ecx                                    | 41 21 0c 0a                         |
    | and dword [r11 + 1 * rcx], ecx                                    | 41 21 0c 0b                         |
    | and dword [r12 + 1 * rcx], ecx                                    | 41 21 0c 0c                         |
    | and dword [r13 + 1 * rcx], ecx                                    | 41 21 4c 0d 00                      |
    | and dword [r14 + 1 * rcx], ecx                                    | 41 21 0c 0e                         |
    | and dword [r15 + 1 * rcx], ecx                                    | 41 21 0c 0f                         |
    | and dword [rax + 1 * rax], ecx                                    | 21 0c 00                            |
    | and dword [rax + 1 * rdx], ecx                                    | 21 0c 10                            |
    | and dword [rax + 1 * rbx], ecx                                    | 21 0c 18                            |
    | and dword [rax + 1 * rbp], ecx                                    | 21 0c 28                            |
    | and dword [rax + 1 * rsi], ecx                                    | 21 0c 30                            |
    | and dword [rax + 1 * rdi], ecx                                    | 21 0c 38                            |
    | and dword [rax + 1 * r8], ecx                                     | 42 21 0c 00                         |
    | and dword [rax + 1 * r9], ecx                                     | 42 21 0c 08                         |
    | and dword [rax + 1 * r10], ecx                                    | 42 21 0c 10                         |
    | and dword [rax + 1 * r11], ecx                                    | 42 21 0c 18                         |
    | and dword [rax + 1 * r12], ecx                                    | 42 21 0c 20                         |
    | and dword [rax + 1 * r13], ecx                                    | 42 21 0c 28                         |
    | and dword [rax + 1 * r14], ecx                                    | 42 21 0c 30                         |
    | and dword [rax + 1 * r15], ecx                                    | 42 21 0c 38                         |
    | and dword [rax + 2 * rcx], ecx                                    | 21 0c 48                            |
    | and dword [rax + 4 * rcx], ecx                                    | 21 0c 88                            |
    | and dword [rax + 8 * rcx], ecx                                    | 21 0c c8                            |
    | and dword [r8 + 1 * r9], ecx                                      | 43 21 0c 08                         |
    | and dword [r8 + 2 * r9], ecx                                      | 43 21 0c 48                         |
    | and dword [r8 + 4 * r9], ecx                                      | 43 21 0c 88                         |
    | and dword [r8 + 8 * r9], ecx                                      | 43 21 0c c8                         |
    | and dword [1 * rcx], ecx                                          | 21 0c 0d 00 00 00 00                |
    | and dword [2 * rcx], ecx                                          | 21 0c 4d 00 00 00 00                |
    | and dword [4 * rcx], ecx                                          | 21 0c 8d 00 00 00 00                |
    | and dword [8 * rcx], ecx                                          | 21 0c cd 00 00 00 00                |
    | and dword [1 * r9], ecx                                           | 42 21 0c 0d 00 00 00 00             |
    | and dword [2 * r9], ecx                                           | 42 21 0c 4d 00 00 00 00             |
    | and dword [4 * r9], ecx                                           | 42 21 0c 8d 00 00 00 00             |
    | and dword [8 * r9], ecx                                           | 42 21 0c cd 00 00 00 00             |
    | and dword [r13 + 8 * r12], ecx                                    | 43 21 4c e5 00                      |
    | and dword [rsp + 4 * r15], ecx                                    | 42 21 0c bc                         |
    | and dword [rax + 1 * rcx + 0x00], ecx                             | 21 4c 08 00                         |
    | and dword [rax + 1 * rcx - 0x00], ecx                             | 21 4c 08 00                         |
    | and dword [rax + 1 * rcx + 0x01], ecx                             | 21 4c 08 01                         |
    | and dword [rax + 1 * rcx - 0x01], ecx                             | 21 4c 08 ff                         |
    | and dword [rax + 1 * rcx + 0x00000001], ecx                       | 21 8c 08 01 00 00 00                |
    | and dword [rax + 1 * rcx - 0x00000001], ecx                       | 21 8c 08 ff ff ff ff                |
    | and dword [rax + 1 * rcx + 0x7f], ecx                             | 21 4c 08 7f                         |
    | and dword [rax + 1 * rcx - 0x7f], ecx                             | 21 4c 08 81                         |
    | and dword [rax + 1 * rcx + 0x80], ecx                             | 21 8c 08 80 00 00 00                |
    | and dword [rax + 1 * rcx - 0x80], ecx                             | 21 4c 08 80                         |
    | and dword [rax + 1 * rcx - 0x81], ecx                             | 21 8c 08 7f ff ff ff                |
    | and dword [rax + 1 * rcx + 0xff], ecx                             | 21 8c 08 ff 00 00 00                |
    | and dword [rax + 1 * rcx - 0xff], ecx                             | 21 8c 08 01 ff ff ff                |
    | and dword [rax + 1 * rcx + 0x7fffffff], ecx                       | 21 8c 08 ff ff ff 7f                |
    | and dword [rax + 1 * rcx - 0x7fffffff], ecx                       | 21 8c 08 01 00 00 80                |
    | and dword [rax + 1 * rcx - 0x80000000], ecx                       | 21 8c 08 00 00 00 80                |
    | and dword [r10 + 0x7f], ecx                                       | 41 21 4a 7f                         |
    | and dword [r10 + 0x80], ecx                                       | 41 21 8a 80 00 00 00                |
    | and dword [r10 - 0x80], ecx                                       | 41 21 4a 80                         |
    | and dword [r10 - 0x81], ecx                                       | 41 21 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and dword [rel @prev5], ecx      | 90 90 90 90 90 21 0d f5 ff ff ff    |
    | .prev1: nop; and dword [rel @prev1], ecx                          | 90 21 0d f9 ff ff ff                |
    | and dword [rel @next1], ecx; nop; .next1: nop                     | 21 0d 01 00 00 00 90 90             |
    | and dword [rel @next5], ecx; nop; nop; nop; nop; nop; .next5: nop | 21 0d 05 00 00 00 90 90 90 90 90 90 |
    | and dword [rax], eax                                              | 21 00                               |
    | and dword [rax], edx                                              | 21 10                               |
    | and dword [rax], ebx                                              | 21 18                               |
    | and dword [rax], esp                                              | 21 20                               |
    | and dword [rax], ebp                                              | 21 28                               |
    | and dword [rax], esi                                              | 21 30                               |
    | and dword [rax], edi                                              | 21 38                               |
    | and dword [rax], r8d                                              | 44 21 00                            |
    | and dword [rax], r9d                                              | 44 21 08                            |
    | and dword [rax], r10d                                             | 44 21 10                            |
    | and dword [rax], r11d                                             | 44 21 18                            |
    | and dword [rax], r12d                                             | 44 21 20                            |
    | and dword [rax], r13d                                             | 44 21 28                            |
    | and dword [rax], r14d                                             | 44 21 30                            |
    | and dword [rax], r15d                                             | 44 21 38                            |
    | and dword [rcx], edx                                              | 21 11                               |
    | and dword [rdx], ebx                                              | 21 1a                               |
    | and dword [rbx], esp                                              | 21 23                               |
    | and dword [rsp], ebp                                              | 21 2c 24                            |
    | and dword [rbp], esi                                              | 21 75 00                            |
    | and dword [rsi], edi                                              | 21 3e                               |
    | and dword [rdi], r8d                                              | 44 21 07                            |
    | and dword [r8], r9d                                               | 45 21 08                            |
    | and dword [r9], r10d                                              | 45 21 11                            |
    | and dword [r10], r11d                                             | 45 21 1a                            |
    | and dword [r11], r12d                                             | 45 21 23                            |
    | and dword [r12], r13d                                             | 45 21 2c 24                         |
    | and dword [r13], r14d                                             | 45 21 75 00                         |
    | and dword [r14], r15d                                             | 45 21 3e                            |
    | and dword [r15], eax                                              | 41 21 07                            |
    | and dword [rcx + 1 * rcx], edx                                    | 21 14 09                            |
    | and dword [rdx + 1 * rcx], ebx                                    | 21 1c 0a                            |
    | and dword [rbx + 1 * rcx], esp                                    | 21 24 0b                            |
    | and dword [rsp + 1 * rcx], ebp                                    | 21 2c 0c                            |
    | and dword [rbp + 1 * rcx], esi                                    | 21 74 0d 00                         |
    | and dword [rsi + 1 * rcx], edi                                    | 21 3c 0e                            |
    | and dword [rdi + 1 * rcx], r8d                                    | 44 21 04 0f                         |
    | and dword [r8 + 1 * rcx], r9d                                     | 45 21 0c 08                         |
    | and dword [r9 + 1 * rcx], r10d                                    | 45 21 14 09                         |
    | and dword [r10 + 1 * rcx], r11d                                   | 45 21 1c 0a                         |
    | and dword [r11 + 1 * rcx], r12d                                   | 45 21 24 0b                         |
    | and dword [r12 + 1 * rcx], r13d                                   | 45 21 2c 0c                         |
    | and dword [r13 + 1 * rcx], r14d                                   | 45 21 74 0d 00                      |
    | and dword [r14 + 1 * rcx], r15d                                   | 45 21 3c 0e                         |
    | and dword [r15 + 1 * rcx], eax                                    | 41 21 04 0f                         |
    | and dword [rax + 1 * rdx], edx                                    | 21 14 10                            |
    | and dword [rax + 1 * rbx], ebx                                    | 21 1c 18                            |
    | and dword [rax + 1 * rbp], esp                                    | 21 24 28                            |
    | and dword [rax + 1 * rsi], ebp                                    | 21 2c 30                            |
    | and dword [rax + 1 * rdi], esi                                    | 21 34 38                            |
    | and dword [rax + 1 * r8], edi                                     | 42 21 3c 00                         |
    | and dword [rax + 1 * r9], r8d                                     | 46 21 04 08                         |
    | and dword [rax + 1 * r10], r9d                                    | 46 21 0c 10                         |
    | and dword [rax + 1 * r11], r10d                                   | 46 21 14 18                         |
    | and dword [rax + 1 * r12], r11d                                   | 46 21 1c 20                         |
    | and dword [rax + 1 * r13], r12d                                   | 46 21 24 28                         |
    | and dword [rax + 1 * r14], r13d                                   | 46 21 2c 30                         |
    | and dword [rax + 1 * r15], r14d                                   | 46 21 34 38                         |
    | and dword [rax + 2 * rcx], r15d                                   | 44 21 3c 48                         |
    | and dword [rax + 4 * rcx], eax                                    | 21 04 88                            |
    | and dword [r8 + 1 * r9], edx                                      | 43 21 14 08                         |
    | and dword [r8 + 2 * r9], ebx                                      | 43 21 1c 48                         |
    | and dword [r8 + 4 * r9], esp                                      | 43 21 24 88                         |
    | and dword [r8 + 8 * r9], ebp                                      | 43 21 2c c8                         |
    | and dword [1 * rcx], esi                                          | 21 34 0d 00 00 00 00                |
    | and dword [2 * rcx], edi                                          | 21 3c 4d 00 00 00 00                |
    | and dword [4 * rcx], r8d                                          | 44 21 04 8d 00 00 00 00             |
    | and dword [8 * rcx], r9d                                          | 44 21 0c cd 00 00 00 00             |
    | and dword [1 * r9], r10d                                          | 46 21 14 0d 00 00 00 00             |
    | and dword [2 * r9], r11d                                          | 46 21 1c 4d 00 00 00 00             |
    | and dword [4 * r9], r12d                                          | 46 21 24 8d 00 00 00 00             |
    | and dword [8 * r9], r13d                                          | 46 21 2c cd 00 00 00 00             |
    | and dword [r13 + 8 * r12], r14d                                   | 47 21 74 e5 00                      |
    | and dword [rsp + 4 * r15], r15d                                   | 46 21 3c bc                         |
    | and dword [rax + 1 * rcx + 0x00], eax                             | 21 44 08 00                         |
    | and dword [rax + 1 * rcx + 0x01], edx                             | 21 54 08 01                         |
    | and dword [rax + 1 * rcx - 0x01], ebx                             | 21 5c 08 ff                         |
    | and dword [rax + 1 * rcx + 0x00000001], esp                       | 21 a4 08 01 00 00 00                |
    | and dword [rax + 1 * rcx - 0x00000001], ebp                       | 21 ac 08 ff ff ff ff                |
    | and dword [rax + 1 * rcx + 0x7f], esi                             | 21 74 08 7f                         |
    | and dword [rax + 1 * rcx - 0x7f], edi                             | 21 7c 08 81                         |
    | and dword [rax + 1 * rcx + 0x80], r8d                             | 44 21 84 08 80 00 00 00             |
    | and dword [rax + 1 * rcx - 0x80], r9d                             | 44 21 4c 08 80                      |
    | and dword [rax + 1 * rcx - 0x81], r10d                            | 44 21 94 08 7f ff ff ff             |
    | and dword [rax + 1 * rcx + 0xff], r11d                            | 44 21 9c 08 ff 00 00 00             |
    | and dword [rax + 1 * rcx - 0xff], r12d                            | 44 21 a4 08 01 ff ff ff             |
    | and dword [rax + 1 * rcx + 0x7fffffff], r13d                      | 44 21 ac 08 ff ff ff 7f             |
    | and dword [rax + 1 * rcx - 0x7fffffff], r14d                      | 44 21 b4 08 01 00 00 80             |
    | and dword [rax + 1 * rcx - 0x80000000], r15d                      | 44 21 bc 08 00 00 00 80             |
    | and dword [r10 + 0x7f], eax                                       | 41 21 42 7f                         |
    | and dword [r10 - 0x80], edx                                       | 41 21 52 80                         |
    | and dword [r10 - 0x81], ebx                                       | 41 21 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and dword [rel @prev5], esp      | 90 90 90 90 90 21 25 f5 ff ff ff    |
    | .prev1: nop; and dword [rel @prev1], ebp                          | 90 21 2d f9 ff ff ff                |
    | and dword [rel @next1], esi; nop; .next1: nop                     | 21 35 01 00 00 00 90 90             |
    | and dword [rel @next5], edi; nop; nop; nop; nop; nop; .next5: nop | 21 3d 05 00 00 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_and_addr32_reg32():
    encode(AND_ADDR32_REG32)


AND_ADDR16_IMM8 = """
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | instruction                                                       | encoding                                  |
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | and word [rax], 0x01                                              | 66 83 20 01                               |
    | and word [rcx], 0x01                                              | 66 83 21 01                               |
    | and word [rdx], 0x01                                              | 66 83 22 01                               |
    | and word [rbx], 0x01                                              | 66 83 23 01                               |
    | and word [rsp], 0x01                                              | 66 83 24 24 01                            |
    | and word [rbp], 0x01                                              | 66 83 65 00 01                            |
    | and word [rsi], 0x01                                              | 66 83 26 01                               |
    | and word [rdi], 0x01                                              | 66 83 27 01                               |
    | and word [r8], 0x01                                               | 66 41 83 20 01                            |
    | and word [r9], 0x01                                               | 66 41 83 21 01                            |
    | and word [r10], 0x01                                              | 66 41 83 22 01                            |
    | and word [r11], 0x01                                              | 66 41 83 23 01                            |
    | and word [r12], 0x01                                              | 66 41 83 24 24 01                         |
    | and word [r13], 0x01                                              | 66 41 83 65 00 01                         |
    | and word [r14], 0x01                                              | 66 41 83 26 01                            |
    | and word [r15], 0x01                                              | 66 41 83 27 01                            |
    | and word [rax + 1 * rcx], 0x01                                    | 66 83 24 08 01                            |
    | and word [rcx + 1 * rcx], 0x01                                    | 66 83 24 09 01                            |
    | and word [rdx + 1 * rcx], 0x01                                    | 66 83 24 0a 01                            |
    | and word [rbx + 1 * rcx], 0x01                                    | 66 83 24 0b 01                            |
    | and word [rsp + 1 * rcx], 0x01                                    | 66 83 24 0c 01                            |
    | and word [rbp + 1 * rcx], 0x01                                    | 66 83 64 0d 00 01                         |
    | and word [rsi + 1 * rcx], 0x01                                    | 66 83 24 0e 01                            |
    | and word [rdi + 1 * rcx], 0x01                                    | 66 83 24 0f 01                            |
    | and word [r8 + 1 * rcx], 0x01                                     | 66 41 83 24 08 01                         |
    | and word [r9 + 1 * rcx], 0x01                                     | 66 41 83 24 09 01                         |
    | and word [r10 + 1 * rcx], 0x01                                    | 66 41 83 24 0a 01                         |
    | and word [r11 + 1 * rcx], 0x01                                    | 66 41 83 24 0b 01                         |
    | and word [r12 + 1 * rcx], 0x01                                    | 66 41 83 24 0c 01                         |
    | and word [r13 + 1 * rcx], 0x01                                    | 66 41 83 64 0d 00 01                      |
    | and word [r14 + 1 * rcx], 0x01                                    | 66 41 83 24 0e 01                         |
    | and word [r15 + 1 * rcx], 0x01                                    | 66 41 83 24 0f 01                         |
    | and word [rax + 1 * rax], 0x01                                    | 66 83 24 00 01                            |
    | and word [rax + 1 * rdx], 0x01                                    | 66 83 24 10 01                            |
    | and word [rax + 1 * rbx], 0x01                                    | 66 83 24 18 01                            |
    | and word [rax + 1 * rbp], 0x01                                    | 66 83 24 28 01                            |
    | and word [rax + 1 * rsi], 0x01                                    | 66 83 24 30 01                            |
    | and word [rax + 1 * rdi], 0x01                                    | 66 83 24 38 01                            |
    | and word [rax + 1 * r8], 0x01                                     | 66 42 83 24 00 01                         |
    | and word [rax + 1 * r9], 0x01                                     | 66 42 83 24 08 01                         |
    | and word [rax + 1 * r10], 0x01                                    | 66 42 83 24 10 01                         |
    | and word [rax + 1 * r11], 0x01                                    | 66 42 83 24 18 01                         |
    | and word [rax + 1 * r12], 0x01                                    | 66 42 83 24 20 01                         |
    | and word [rax + 1 * r13], 0x01                                    | 66 42 83 24 28 01                         |
    | and word [rax + 1 * r14], 0x01                                    | 66 42 83 24 30 01                         |
    | and word [rax + 1 * r15], 0x01                                    | 66 42 83 24 38 01                         |
    | and word [rax + 2 * rcx], 0x01                                    | 66 83 24 48 01                            |
    | and word [rax + 4 * rcx], 0x01                                    | 66 83 24 88 01                            |
    | and word [rax + 8 * rcx], 0x01                                    | 66 83 24 c8 01                            |
    | and word [r8 + 1 * r9], 0x01                                      | 66 43 83 24 08 01                         |
    | and word [r8 + 2 * r9], 0x01                                      | 66 43 83 24 48 01                         |
    | and word [r8 + 4 * r9], 0x01                                      | 66 43 83 24 88 01                         |
    | and word [r8 + 8 * r9], 0x01                                      | 66 43 83 24 c8 01                         |
    | and word [1 * rcx], 0x01                                          | 66 83 24 0d 00 00 00 00 01                |
    | and word [2 * rcx], 0x01                                          | 66 83 24 4d 00 00 00 00 01                |
    | and word [4 * rcx], 0x01                                          | 66 83 24 8d 00 00 00 00 01                |
    | and word [8 * rcx], 0x01                                          | 66 83 24 cd 00 00 00 00 01                |
    | and word [1 * r9], 0x01                                           | 66 42 83 24 0d 00 00 00 00 01             |
    | and word [2 * r9], 0x01                                           | 66 42 83 24 4d 00 00 00 00 01             |
    | and word [4 * r9], 0x01                                           | 66 42 83 24 8d 00 00 00 00 01             |
    | and word [8 * r9], 0x01                                           | 66 42 83 24 cd 00 00 00 00 01             |
    | and word [r13 + 8 * r12], 0x01                                    | 66 43 83 64 e5 00 01                      |
    | and word [rsp + 4 * r15], 0x01                                    | 66 42 83 24 bc 01                         |
    | and word [rax + 1 * rcx + 0x00], 0x01                             | 66 83 64 08 00 01                         |
    | and word [rax + 1 * rcx - 0x00], 0x01                             | 66 83 64 08 00 01                         |
    | and word [rax + 1 * rcx + 0x01], 0x01                             | 66 83 64 08 01 01                         |
    | and word [rax + 1 * rcx - 0x01], 0x01                             | 66 83 64 08 ff 01                         |
    | and word [rax + 1 * rcx + 0x00000001], 0x01                       | 66 83 a4 08 01 00 00 00 01                |
    | and word [rax + 1 * rcx - 0x00000001], 0x01                       | 66 83 a4 08 ff ff ff ff 01                |
    | and word [rax + 1 * rcx + 0x7f], 0x01                             | 66 83 64 08 7f 01                         |
    | and word [rax + 1 * rcx - 0x7f], 0x01                             | 66 83 64 08 81 01                         |
    | and word [rax + 1 * rcx + 0x80], 0x01                             | 66 83 a4 08 80 00 00 00 01                |
    | and word [rax + 1 * rcx - 0x80], 0x01                             | 66 83 64 08 80 01                         |
    | and word [rax + 1 * rcx - 0x81], 0x01                             | 66 83 a4 08 7f ff ff ff 01                |
    | and word [rax + 1 * rcx + 0xff], 0x01                             | 66 83 a4 08 ff 00 00 00 01                |
    | and word [rax + 1 * rcx - 0xff], 0x01                             | 66 83 a4 08 01 ff ff ff 01                |
    | and word [rax + 1 * rcx + 0x7fffffff], 0x01                       | 66 83 a4 08 ff ff ff 7f 01                |
    | and word [rax + 1 * rcx - 0x7fffffff], 0x01                       | 66 83 a4 08 01 00 00 80 01                |
    | and word [rax + 1 * rcx - 0x80000000], 0x01                       | 66 83 a4 08 00 00 00 80 01                |
    | and word [r10 + 0x7f], 0x01                                       | 66 41 83 62 7f 01                         |
    | and word [r10 + 0x80], 0x01                                       | 66 41 83 a2 80 00 00 00 01                |
    | and word [r10 - 0x80], 0x01                                       | 66 41 83 62 80 01                         |
    | and word [r10 - 0x81], 0x01                                       | 66 41 83 a2 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; and word [rel @prev5], 0x01      | 90 90 90 90 90 66 83 25 f3 ff ff ff 01    |
    | .prev1: nop; and word [rel @prev1], 0x01                          | 90 66 83 25 f7 ff ff ff 01                |
    | and word [rel @next1], 0x01; nop; .next1: nop                     | 66 83 25 01 00 00 00 01 90 90             |
    | and word [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 66 83 25 05 00 00 00 01 90 90 90 90 90 90 |
    | and word [rax], 0x00                                              | 66 83 20 00                               |
    | and word [rax], 0x7f                                              | 66 83 20 7f                               |
    | and word [rax], 0x80                                              | 66 83 20 80                               |
    | and word [rax], 0xff                                              | 66 83 20 ff                               |
    | and word [rcx], 0x7f                                              | 66 83 21 7f                               |
    | and word [rdx], 0x80                                              | 66 83 22 80                               |
    | and word [rbx], 0xff                                              | 66 83 23 ff                               |
    | and word [rsp], 0x00                                              | 66 83 24 24 00                            |
    | and word [rsi], 0x7f                                              | 66 83 26 7f                               |
    | and word [rdi], 0x80                                              | 66 83 27 80                               |
    | and word [r8], 0xff                                               | 66 41 83 20 ff                            |
    | and word [r9], 0x00                                               | 66 41 83 21 00                            |
    | and word [r11], 0x7f                                              | 66 41 83 23 7f                            |
    | and word [r12], 0x80                                              | 66 41 83 24 24 80                         |
    | and word [r13], 0xff                                              | 66 41 83 65 00 ff                         |
    | and word [r14], 0x00                                              | 66 41 83 26 00                            |
    | and word [rax + 1 * rcx], 0x7f                                    | 66 83 24 08 7f                            |
    | and word [rcx + 1 * rcx], 0x80                                    | 66 83 24 09 80                            |
    | and word [rdx + 1 * rcx], 0xff                                    | 66 83 24 0a ff                            |
    | and word [rbx + 1 * rcx], 0x00                                    | 66 83 24 0b 00                            |
    | and word [rbp + 1 * rcx], 0x7f                                    | 66 83 64 0d 00 7f                         |
    | and word [rsi + 1 * rcx], 0x80                                    | 66 83 24 0e 80                            |
    | and word [rdi + 1 * rcx], 0xff                                    | 66 83 24 0f ff                            |
    | and word [r8 + 1 * rcx], 0x00                                     | 66 41 83 24 08 00                         |
    | and word [r10 + 1 * rcx], 0x7f                                    | 66 41 83 24 0a 7f                         |
    | and word [r11 + 1 * rcx], 0x80                                    | 66 41 83 24 0b 80                         |
    | and word [r12 + 1 * rcx], 0xff                                    | 66 41 83 24 0c ff                         |
    | and word [r13 + 1 * rcx], 0x00                                    | 66 41 83 64 0d 00 00                      |
    | and word [r15 + 1 * rcx], 0x7f                                    | 66 41 83 24 0f 7f                         |
    | and word [rax + 1 * rax], 0x80                                    | 66 83 24 00 80                            |
    | and word [rax + 1 * rdx], 0xff                                    | 66 83 24 10 ff                            |
    | and word [rax + 1 * rbx], 0x00                                    | 66 83 24 18 00                            |
    | and word [rax + 1 * rsi], 0x7f                                    | 66 83 24 30 7f                            |
    | and word [rax + 1 * rdi], 0x80                                    | 66 83 24 38 80                            |
    | and word [rax + 1 * r8], 0xff                                     | 66 42 83 24 00 ff                         |
    | and word [rax + 1 * r9], 0x00                                     | 66 42 83 24 08 00                         |
    | and word [rax + 1 * r11], 0x7f                                    | 66 42 83 24 18 7f                         |
    | and word [rax + 1 * r12], 0x80                                    | 66 42 83 24 20 80                         |
    | and word [rax + 1 * r13], 0xff                                    | 66 42 83 24 28 ff                         |
    | and word [rax + 1 * r14], 0x00                                    | 66 42 83 24 30 00                         |
    | and word [rax + 2 * rcx], 0x7f                                    | 66 83 24 48 7f                            |
    | and word [rax + 4 * rcx], 0x80                                    | 66 83 24 88 80                            |
    | and word [rax + 8 * rcx], 0xff                                    | 66 83 24 c8 ff                            |
    | and word [r8 + 1 * r9], 0x00                                      | 66 43 83 24 08 00                         |
    | and word [r8 + 4 * r9], 0x7f                                      | 66 43 83 24 88 7f                         |
    | and word [r8 + 8 * r9], 0x80                                      | 66 43 83 24 c8 80                         |
    | and word [1 * rcx], 0xff                                          | 66 83 24 0d 00 00 00 00 ff                |
    | and word [2 * rcx], 0x00                                          | 66 83 24 4d 00 00 00 00 00                |
    | and word [8 * rcx], 0x7f                                          | 66 83 24 cd 00 00 00 00 7f                |
    | and word [1 * r9], 0x80                                           | 66 42 83 24 0d 00 00 00 00 80             |
    | and word [2 * r9], 0xff                                           | 66 42 83 24 4d 00 00 00 00 ff             |
    | and word [4 * r9], 0x00                                           | 66 42 83 24 8d 00 00 00 00 00             |
    | and word [r13 + 8 * r12], 0x7f                                    | 66 43 83 64 e5 00 7f                      |
    | and word [rsp + 4 * r15], 0x80                                    | 66 42 83 24 bc 80                         |
    | and word [rax + 1 * rcx + 0x00], 0xff                             | 66 83 64 08 00 ff                         |
    | and word [rax + 1 * rcx - 0x00], 0x00                             | 66 83 64 08 00 00                         |
    | and word [rax + 1 * rcx - 0x01], 0x7f                             | 66 83 64 08 ff 7f                         |
    | and word [rax + 1 * rcx + 0x00000001], 0x80                       | 66 83 a4 08 01 00 00 00 80                |
    | and word [rax + 1 * rcx - 0x00000001], 0xff                       | 66 83 a4 08 ff ff ff ff ff                |
    | and word [rax + 1 * rcx + 0x7f], 0x00                             | 66 83 64 08 7f 00                         |
    | and word [rax + 1 * rcx + 0x80], 0x7f                             | 66 83 a4 08 80 00 00 00 7f                |
    | and word [rax + 1 * rcx - 0x80], 0x80                             | 66 83 64 08 80 80                         |
    | and word [rax + 1 * rcx - 0x81], 0xff                             | 66 83 a4 08 7f ff ff ff ff                |
    | and word [rax + 1 * rcx + 0xff], 0x00                             | 66 83 a4 08 ff 00 00 00 00                |
    | and word [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 66 83 a4 08 ff ff ff 7f 7f                |
    | and word [rax + 1 * rcx - 0x7fffffff], 0x80                       | 66 83 a4 08 01 00 00 80 80                |
    | and word [rax + 1 * rcx - 0x80000000], 0xff                       | 66 83 a4 08 00 00 00 80 ff                |
    | and word [r10 + 0x7f], 0x00                                       | 66 41 83 62 7f 00                         |
    | and word [r10 - 0x80], 0x7f                                       | 66 41 83 62 80 7f                         |
    | and word [r10 - 0x81], 0x80                                       | 66 41 83 a2 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; and word [rel @prev5], 0xff      | 90 90 90 90 90 66 83 25 f3 ff ff ff ff    |
    | .prev1: nop; and word [rel @prev1], 0x00                          | 90 66 83 25 f7 ff ff ff 00                |
    | and word [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 66 83 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------------- |
"""


def can_encode_and_addr16_imm8():
    encode(AND_ADDR16_IMM8)


AND_ADDR16_IMM16 = """
    | ------------------------------------------------------------------- | -------------------------------------------- |
    | instruction                                                         | encoding                                     |
    | ------------------------------------------------------------------- | -------------------------------------------- |
    | and word [rax], 0x0001                                              | 66 81 20 01 00                               |
    | and word [rcx], 0x0001                                              | 66 81 21 01 00                               |
    | and word [rdx], 0x0001                                              | 66 81 22 01 00                               |
    | and word [rbx], 0x0001                                              | 66 81 23 01 00                               |
    | and word [rsp], 0x0001                                              | 66 81 24 24 01 00                            |
    | and word [rbp], 0x0001                                              | 66 81 65 00 01 00                            |
    | and word [rsi], 0x0001                                              | 66 81 26 01 00                               |
    | and word [rdi], 0x0001                                              | 66 81 27 01 00                               |
    | and word [r8], 0x0001                                               | 66 41 81 20 01 00                            |
    | and word [r9], 0x0001                                               | 66 41 81 21 01 00                            |
    | and word [r10], 0x0001                                              | 66 41 81 22 01 00                            |
    | and word [r11], 0x0001                                              | 66 41 81 23 01 00                            |
    | and word [r12], 0x0001                                              | 66 41 81 24 24 01 00                         |
    | and word [r13], 0x0001                                              | 66 41 81 65 00 01 00                         |
    | and word [r14], 0x0001                                              | 66 41 81 26 01 00                            |
    | and word [r15], 0x0001                                              | 66 41 81 27 01 00                            |
    | and word [rax + 1 * rcx], 0x0001                                    | 66 81 24 08 01 00                            |
    | and word [rcx + 1 * rcx], 0x0001                                    | 66 81 24 09 01 00                            |
    | and word [rdx + 1 * rcx], 0x0001                                    | 66 81 24 0a 01 00                            |
    | and word [rbx + 1 * rcx], 0x0001                                    | 66 81 24 0b 01 00                            |
    | and word [rsp + 1 * rcx], 0x0001                                    | 66 81 24 0c 01 00                            |
    | and word [rbp + 1 * rcx], 0x0001                                    | 66 81 64 0d 00 01 00                         |
    | and word [rsi + 1 * rcx], 0x0001                                    | 66 81 24 0e 01 00                            |
    | and word [rdi + 1 * rcx], 0x0001                                    | 66 81 24 0f 01 00                            |
    | and word [r8 + 1 * rcx], 0x0001                                     | 66 41 81 24 08 01 00                         |
    | and word [r9 + 1 * rcx], 0x0001                                     | 66 41 81 24 09 01 00                         |
    | and word [r10 + 1 * rcx], 0x0001                                    | 66 41 81 24 0a 01 00                         |
    | and word [r11 + 1 * rcx], 0x0001                                    | 66 41 81 24 0b 01 00                         |
    | and word [r12 + 1 * rcx], 0x0001                                    | 66 41 81 24 0c 01 00                         |
    | and word [r13 + 1 * rcx], 0x0001                                    | 66 41 81 64 0d 00 01 00                      |
    | and word [r14 + 1 * rcx], 0x0001                                    | 66 41 81 24 0e 01 00                         |
    | and word [r15 + 1 * rcx], 0x0001                                    | 66 41 81 24 0f 01 00                         |
    | and word [rax + 1 * rax], 0x0001                                    | 66 81 24 00 01 00                            |
    | and word [rax + 1 * rdx], 0x0001                                    | 66 81 24 10 01 00                            |
    | and word [rax + 1 * rbx], 0x0001                                    | 66 81 24 18 01 00                            |
    | and word [rax + 1 * rbp], 0x0001                                    | 66 81 24 28 01 00                            |
    | and word [rax + 1 * rsi], 0x0001                                    | 66 81 24 30 01 00                            |
    | and word [rax + 1 * rdi], 0x0001                                    | 66 81 24 38 01 00                            |
    | and word [rax + 1 * r8], 0x0001                                     | 66 42 81 24 00 01 00                         |
    | and word [rax + 1 * r9], 0x0001                                     | 66 42 81 24 08 01 00                         |
    | and word [rax + 1 * r10], 0x0001                                    | 66 42 81 24 10 01 00                         |
    | and word [rax + 1 * r11], 0x0001                                    | 66 42 81 24 18 01 00                         |
    | and word [rax + 1 * r12], 0x0001                                    | 66 42 81 24 20 01 00                         |
    | and word [rax + 1 * r13], 0x0001                                    | 66 42 81 24 28 01 00                         |
    | and word [rax + 1 * r14], 0x0001                                    | 66 42 81 24 30 01 00                         |
    | and word [rax + 1 * r15], 0x0001                                    | 66 42 81 24 38 01 00                         |
    | and word [rax + 2 * rcx], 0x0001                                    | 66 81 24 48 01 00                            |
    | and word [rax + 4 * rcx], 0x0001                                    | 66 81 24 88 01 00                            |
    | and word [rax + 8 * rcx], 0x0001                                    | 66 81 24 c8 01 00                            |
    | and word [r8 + 1 * r9], 0x0001                                      | 66 43 81 24 08 01 00                         |
    | and word [r8 + 2 * r9], 0x0001                                      | 66 43 81 24 48 01 00                         |
    | and word [r8 + 4 * r9], 0x0001                                      | 66 43 81 24 88 01 00                         |
    | and word [r8 + 8 * r9], 0x0001                                      | 66 43 81 24 c8 01 00                         |
    | and word [1 * rcx], 0x0001                                          | 66 81 24 0d 00 00 00 00 01 00                |
    | and word [2 * rcx], 0x0001                                          | 66 81 24 4d 00 00 00 00 01 00                |
    | and word [4 * rcx], 0x0001                                          | 66 81 24 8d 00 00 00 00 01 00                |
    | and word [8 * rcx], 0x0001                                          | 66 81 24 cd 00 00 00 00 01 00                |
    | and word [1 * r9], 0x0001                                           | 66 42 81 24 0d 00 00 00 00 01 00             |
    | and word [2 * r9], 0x0001                                           | 66 42 81 24 4d 00 00 00 00 01 00             |
    | and word [4 * r9], 0x0001                                           | 66 42 81 24 8d 00 00 00 00 01 00             |
    | and word [8 * r9], 0x0001                                           | 66 42 81 24 cd 00 00 00 00 01 00             |
    | and word [r13 + 8 * r12], 0x0001                                    | 66 43 81 64 e5 00 01 00                      |
    | and word [rsp + 4 * r15], 0x0001                                    | 66 42 81 24 bc 01 00                         |
    | and word [rax + 1 * rcx + 0x00], 0x0001                             | 66 81 64 08 00 01 00                         |
    | and word [rax + 1 * rcx - 0x00], 0x0001                             | 66 81 64 08 00 01 00                         |
    | and word [rax + 1 * rcx + 0x01], 0x0001                             | 66 81 64 08 01 01 00                         |
    | and word [rax + 1 * rcx - 0x01], 0x0001                             | 66 81 64 08 ff 01 00                         |
    | and word [rax + 1 * rcx + 0x00000001], 0x0001                       | 66 81 a4 08 01 00 00 00 01 00                |
    | and word [rax + 1 * rcx - 0x00000001], 0x0001                       | 66 81 a4 08 ff ff ff ff 01 00                |
    | and word [rax + 1 * rcx + 0x7f], 0x0001                             | 66 81 64 08 7f 01 00                         |
    | and word [rax + 1 * rcx - 0x7f], 0x0001                             | 66 81 64 08 81 01 00                         |
    | and word [rax + 1 * rcx + 0x80], 0x0001                             | 66 81 a4 08 80 00 00 00 01 00                |
    | and word [rax + 1 * rcx - 0x80], 0x0001                             | 66 81 64 08 80 01 00                         |
    | and word [rax + 1 * rcx - 0x81], 0x0001                             | 66 81 a4 08 7f ff ff ff 01 00                |
    | and word [rax + 1 * rcx + 0xff], 0x0001                             | 66 81 a4 08 ff 00 00 00 01 00                |
    | and word [rax + 1 * rcx - 0xff], 0x0001                             | 66 81 a4 08 01 ff ff ff 01 00                |
    | and word [rax + 1 * rcx + 0x7fffffff], 0x0001                       | 66 81 a4 08 ff ff ff 7f 01 00                |
    | and word [rax + 1 * rcx - 0x7fffffff], 0x0001                       | 66 81 a4 08 01 00 00 80 01 00                |
    | and word [rax + 1 * rcx - 0x80000000], 0x0001                       | 66 81 a4 08 00 00 00 80 01 00                |
    | and word [r10 + 0x7f], 0x0001                                       | 66 41 81 62 7f 01 00                         |
    | and word [r10 + 0x80], 0x0001                                       | 66 41 81 a2 80 00 00 00 01 00                |
    | and word [r10 - 0x80], 0x0001                                       | 66 41 81 62 80 01 00                         |
    | and word [r10 - 0x81], 0x0001                                       | 66 41 81 a2 7f ff ff ff 01 00                |
    | .prev5: nop; nop; nop; nop; nop; and word [rel @prev5], 0x0001      | 90 90 90 90 90 66 81 25 f2 ff ff ff 01 00    |
    | .prev1: nop; and word [rel @prev1], 0x0001                          | 90 66 81 25 f6 ff ff ff 01 00                |
    | and word [rel @next1], 0x0001; nop; .next1: nop                     | 66 81 25 01 00 00 00 01 00 90 90             |
    | and word [rel @next5], 0x0001; nop; nop; nop; nop; nop; .next5: nop | 66 81 25 05 00 00 00 01 00 90 90 90 90 90 90 |
    | and word [rax], 0x0000                                              | 66 81 20 00 00                               |
    | and word [rax], 0x007f                                              | 66 81 20 7f 00                               |
    | and word [rax], 0x0080                                              | 66 81 20 80 00                               |
    | and word [rax], 0x00ff                                              | 66 81 20 ff 00                               |
    | and word [rax], 0x0100                                              | 66 81 20 00 01                               |
    | and word [rax], 0x7fff                                              | 66 81 20 ff 7f                               |
    | and word [rax], 0x8000                                              | 66 81 20 00 80                               |
    | and word [rax], 0xffff                                              | 66 81 20 ff ff                               |
    | and word [rcx], 0x007f                                              | 66 81 21 7f 00                               |
    | and word [rdx], 0x0080                                              | 66 81 22 80 00                               |
    | and word [rbx], 0x00ff                                              | 66 81 23 ff 00                               |
    | and word [rsp], 0x0100                                              | 66 81 24 24 00 01                            |
    | and word [rbp], 0x7fff                                              | 66 81 65 00 ff 7f                            |
    | and word [rsi], 0x8000                                              | 66 81 26 00 80                               |
    | and word [rdi], 0xffff                                              | 66 81 27 ff ff                               |
    | and word [r8], 0x0000                                               | 66 41 81 20 00 00                            |
    | and word [r10], 0x007f                                              | 66 41 81 22 7f 00                            |
    | and word [r11], 0x0080                                              | 66 41 81 23 80 00                            |
    | and word [r12], 0x00ff                                              | 66 41 81 24 24 ff 00                         |
    | and word [r13], 0x0100                                              | 66 41 81 65 00 00 01                         |
    | and word [r14], 0x7fff                                              | 66 41 81 26 ff 7f                            |
    | and word [r15], 0x8000                                              | 66 41 81 27 00 80                            |
    | and word [rax + 1 * rcx], 0xffff                                    | 66 81 24 08 ff ff                            |
    | and word [rcx + 1 * rcx], 0x0000                                    | 66 81 24 09 00 00                            |
    | and word [rbx + 1 * rcx], 0x007f                                    | 66 81 24 0b 7f 00                            |
    | and word [rsp + 1 * rcx], 0x0080                                    | 66 81 24 0c 80 00                            |
    | and word [rbp + 1 * rcx], 0x00ff                                    | 66 81 64 0d 00 ff 00                         |
    | and word [rsi + 1 * rcx], 0x0100                                    | 66 81 24 0e 00 01                            |
    | and word [rdi + 1 * rcx], 0x7fff                                    | 66 81 24 0f ff 7f                            |
    | and word [r8 + 1 * rcx], 0x8000                                     | 66 41 81 24 08 00 80                         |
    | and word [r9 + 1 * rcx], 0xffff                                     | 66 41 81 24 09 ff ff                         |
    | and word [r10 + 1 * rcx], 0x0000                                    | 66 41 81 24 0a 00 00                         |
    | and word [r12 + 1 * rcx], 0x007f                                    | 66 41 81 24 0c 7f 00                         |
    | and word [r13 + 1 * rcx], 0x0080                                    | 66 41 81 64 0d 00 80 00                      |
    | and word [r14 + 1 * rcx], 0x00ff                                    | 66 41 81 24 0e ff 00                         |
    | and word [r15 + 1 * rcx], 0x0100                                    | 66 41 81 24 0f 00 01                         |
    | and word [rax + 1 * rax], 0x7fff                                    | 66 81 24 00 ff 7f                            |
    | and word [rax + 1 * rdx], 0x8000                                    | 66 81 24 10 00 80                            |
    | and word [rax + 1 * rbx], 0xffff                                    | 66 81 24 18 ff ff                            |
    | and word [rax + 1 * rbp], 0x0000                                    | 66 81 24 28 00 00                            |
    | and word [rax + 1 * rdi], 0x007f                                    | 66 81 24 38 7f 00                            |
    | and word [rax + 1 * r8], 0x0080                                     | 66 42 81 24 00 80 00                         |
    | and word [rax + 1 * r9], 0x00ff                                     | 66 42 81 24 08 ff 00                         |
    | and word [rax + 1 * r10], 0x0100                                    | 66 42 81 24 10 00 01                         |
    | and word [rax + 1 * r11], 0x7fff                                    | 66 42 81 24 18 ff 7f                         |
    | and word [rax + 1 * r12], 0x8000                                    | 66 42 81 24 20 00 80                         |
    | and word [rax + 1 * r13], 0xffff                                    | 66 42 81 24 28 ff ff                         |
    | and word [rax + 1 * r14], 0x0000                                    | 66 42 81 24 30 00 00                         |
    | and word [rax + 2 * rcx], 0x007f                                    | 66 81 24 48 7f 00                            |
    | and word [rax + 4 * rcx], 0x0080                                    | 66 81 24 88 80 00                            |
    | and word [rax + 8 * rcx], 0x00ff                                    | 66 81 24 c8 ff 00                            |
    | and word [r8 + 1 * r9], 0x0100                                      | 66 43 81 24 08 00 01                         |
    | and word [r8 + 2 * r9], 0x7fff                                      | 66 43 81 24 48 ff 7f                         |
    | and word [r8 + 4 * r9], 0x8000                                      | 66 43 81 24 88 00 80                         |
    | and word [r8 + 8 * r9], 0xffff                                      | 66 43 81 24 c8 ff ff                         |
    | and word [1 * rcx], 0x0000                                          | 66 81 24 0d 00 00 00 00 00 00                |
    | and word [4 * rcx], 0x007f                                          | 66 81 24 8d 00 00 00 00 7f 00                |
    | and word [8 * rcx], 0x0080                                          | 66 81 24 cd 00 00 00 00 80 00                |
    | and word [1 * r9], 0x00ff                                           | 66 42 81 24 0d 00 00 00 00 ff 00             |
    | and word [2 * r9], 0x0100                                           | 66 42 81 24 4d 00 00 00 00 00 01             |
    | and word [4 * r9], 0x7fff                                           | 66 42 81 24 8d 00 00 00 00 ff 7f             |
    | and word [8 * r9], 0x8000                                           | 66 42 81 24 cd 00 00 00 00 00 80             |
    | and word [r13 + 8 * r12], 0xffff                                    | 66 43 81 64 e5 00 ff ff                      |
    | and word [rsp + 4 * r15], 0x0000                                    | 66 42 81 24 bc 00 00                         |
    | and word [rax + 1 * rcx - 0x00], 0x007f                             | 66 81 64 08 00 7f 00                         |
    | and word [rax + 1 * rcx + 0x01], 0x0080                             | 66 81 64 08 01 80 00                         |
    | and word [rax + 1 * rcx - 0x01], 0x00ff                             | 66 81 64 08 ff ff 00                         |
    | and word [rax + 1 * rcx + 0x00000001], 0x0100                       | 66 81 a4 08 01 00 00 00 00 01                |
    | and word [rax + 1 * rcx - 0x00000001], 0x7fff                       | 66 81 a4 08 ff ff ff ff ff 7f                |
    | and word [rax + 1 * rcx + 0x7f], 0x8000                             | 66 81 64 08 7f 00 80                         |
    | and word [rax + 1 * rcx - 0x7f], 0xffff                             | 66 81 64 08 81 ff ff                         |
    | and word [rax + 1 * rcx + 0x80], 0x0000                             | 66 81 a4 08 80 00 00 00 00 00                |
    | and word [rax + 1 * rcx - 0x81], 0x007f                             | 66 81 a4 08 7f ff ff ff 7f 00                |
    | and word [rax + 1 * rcx + 0xff], 0x0080                             | 66 81 a4 08 ff 00 00 00 80 00                |
    | and word [rax + 1 * rcx - 0xff], 0x00ff                             | 66 81 a4 08 01 ff ff ff ff 00                |
    | and word [rax + 1 * rcx + 0x7fffffff], 0x0100                       | 66 81 a4 08 ff ff ff 7f 00 01                |
    | and word [rax + 1 * rcx - 0x7fffffff], 0x7fff                       | 66 81 a4 08 01 00 00 80 ff 7f                |
    | and word [rax + 1 * rcx - 0x80000000], 0x8000                       | 66 81 a4 08 00 00 00 80 00 80                |
    | and word [r10 + 0x7f], 0xffff                                       | 66 41 81 62 7f ff ff                         |
    | and word [r10 + 0x80], 0x0000                                       | 66 41 81 a2 80 00 00 00 00 00                |
    | and word [r10 - 0x81], 0x007f                                       | 66 41 81 a2 7f ff ff ff 7f 00                |
    | .prev5: nop; nop; nop; nop; nop; and word [rel @prev5], 0x0080      | 90 90 90 90 90 66 81 25 f2 ff ff ff 80 00    |
    | .prev1: nop; and word [rel @prev1], 0x00ff                          | 90 66 81 25 f6 ff ff ff ff 00                |
    | and word [rel @next1], 0x0100; nop; .next1: nop                     | 66 81 25 01 00 00 00 00 01 90 90             |
    | and word [rel @next5], 0x7fff; nop; nop; nop; nop; nop; .next5: nop | 66 81 25 05 00 00 00 ff 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------- | -------------------------------------------- |
"""


def can_encode_and_addr16_imm16():
    encode(AND_ADDR16_IMM16)


AND_ADDR16_REG16 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | and word [rax], cx                                              | 66 21 08                               |
    | and word [rcx], cx                                              | 66 21 09                               |
    | and word [rdx], cx                                              | 66 21 0a                               |
    | and word [rbx], cx                                              | 66 21 0b                               |
    | and word [rsp], cx                                              | 66 21 0c 24                            |
    | and word [rbp], cx                                              | 66 21 4d 00                            |
    | and word [rsi], cx                                              | 66 21 0e                               |
    | and word [rdi], cx                                              | 66 21 0f                               |
    | and word [r8], cx                                               | 66 41 21 08                            |
    | and word [r9], cx                                               | 66 41 21 09                            |
    | and word [r10], cx                                              | 66 41 21 0a                            |
    | and word [r11], cx                                              | 66 41 21 0b                            |
    | and word [r12], cx                                              | 66 41 21 0c 24                         |
    | and word [r13], cx                                              | 66 41 21 4d 00                         |
    | and word [r14], cx                                              | 66 41 21 0e                            |
    | and word [r15], cx                                              | 66 41 21 0f                            |
    | and word [rax + 1 * rcx], cx                                    | 66 21 0c 08                            |
    | and word [rcx + 1 * rcx], cx                                    | 66 21 0c 09                            |
    | and word [rdx + 1 * rcx], cx                                    | 66 21 0c 0a                            |
    | and word [rbx + 1 * rcx], cx                                    | 66 21 0c 0b                            |
    | and word [rsp + 1 * rcx], cx                                    | 66 21 0c 0c                            |
    | and word [rbp + 1 * rcx], cx                                    | 66 21 4c 0d 00                         |
    | and word [rsi + 1 * rcx], cx                                    | 66 21 0c 0e                            |
    | and word [rdi + 1 * rcx], cx                                    | 66 21 0c 0f                            |
    | and word [r8 + 1 * rcx], cx                                     | 66 41 21 0c 08                         |
    | and word [r9 + 1 * rcx], cx                                     | 66 41 21 0c 09                         |
    | and word [r10 + 1 * rcx], cx                                    | 66 41 21 0c 0a                         |
    | and word [r11 + 1 * rcx], cx                                    | 66 41 21 0c 0b                         |
    | and word [r12 + 1 * rcx], cx                                    | 66 41 21 0c 0c                         |
    | and word [r13 + 1 * rcx], cx                                    | 66 41 21 4c 0d 00                      |
    | and word [r14 + 1 * rcx], cx                                    | 66 41 21 0c 0e                         |
    | and word [r15 + 1 * rcx], cx                                    | 66 41 21 0c 0f                         |
    | and word [rax + 1 * rax], cx                                    | 66 21 0c 00                            |
    | and word [rax + 1 * rdx], cx                                    | 66 21 0c 10                            |
    | and word [rax + 1 * rbx], cx                                    | 66 21 0c 18                            |
    | and word [rax + 1 * rbp], cx                                    | 66 21 0c 28                            |
    | and word [rax + 1 * rsi], cx                                    | 66 21 0c 30                            |
    | and word [rax + 1 * rdi], cx                                    | 66 21 0c 38                            |
    | and word [rax + 1 * r8], cx                                     | 66 42 21 0c 00                         |
    | and word [rax + 1 * r9], cx                                     | 66 42 21 0c 08                         |
    | and word [rax + 1 * r10], cx                                    | 66 42 21 0c 10                         |
    | and word [rax + 1 * r11], cx                                    | 66 42 21 0c 18                         |
    | and word [rax + 1 * r12], cx                                    | 66 42 21 0c 20                         |
    | and word [rax + 1 * r13], cx                                    | 66 42 21 0c 28                         |
    | and word [rax + 1 * r14], cx                                    | 66 42 21 0c 30                         |
    | and word [rax + 1 * r15], cx                                    | 66 42 21 0c 38                         |
    | and word [rax + 2 * rcx], cx                                    | 66 21 0c 48                            |
    | and word [rax + 4 * rcx], cx                                    | 66 21 0c 88                            |
    | and word [rax + 8 * rcx], cx                                    | 66 21 0c c8                            |
    | and word [r8 + 1 * r9], cx                                      | 66 43 21 0c 08                         |
    | and word [r8 + 2 * r9], cx                                      | 66 43 21 0c 48                         |
    | and word [r8 + 4 * r9], cx                                      | 66 43 21 0c 88                         |
    | and word [r8 + 8 * r9], cx                                      | 66 43 21 0c c8                         |
    | and word [1 * rcx], cx                                          | 66 21 0c 0d 00 00 00 00                |
    | and word [2 * rcx], cx                                          | 66 21 0c 4d 00 00 00 00                |
    | and word [4 * rcx], cx                                          | 66 21 0c 8d 00 00 00 00                |
    | and word [8 * rcx], cx                                          | 66 21 0c cd 00 00 00 00                |
    | and word [1 * r9], cx                                           | 66 42 21 0c 0d 00 00 00 00             |
    | and word [2 * r9], cx                                           | 66 42 21 0c 4d 00 00 00 00             |
    | and word [4 * r9], cx                                           | 66 42 21 0c 8d 00 00 00 00             |
    | and word [8 * r9], cx                                           | 66 42 21 0c cd 00 00 00 00             |
    | and word [r13 + 8 * r12], cx                                    | 66 43 21 4c e5 00                      |
    | and word [rsp + 4 * r15], cx                                    | 66 42 21 0c bc                         |
    | and word [rax + 1 * rcx + 0x00], cx                             | 66 21 4c 08 00                         |
    | and word [rax + 1 * rcx - 0x00], cx                             | 66 21 4c 08 00                         |
    | and word [rax + 1 * rcx + 0x01], cx                             | 66 21 4c 08 01                         |
    | and word [rax + 1 * rcx - 0x01], cx                             | 66 21 4c 08 ff                         |
    | and word [rax + 1 * rcx + 0x00000001], cx                       | 66 21 8c 08 01 00 00 00                |
    | and word [rax + 1 * rcx - 0x00000001], cx                       | 66 21 8c 08 ff ff ff ff                |
    | and word [rax + 1 * rcx + 0x7f], cx                             | 66 21 4c 08 7f                         |
    | and word [rax + 1 * rcx - 0x7f], cx                             | 66 21 4c 08 81                         |
    | and word [rax + 1 * rcx + 0x80], cx                             | 66 21 8c 08 80 00 00 00                |
    | and word [rax + 1 * rcx - 0x80], cx                             | 66 21 4c 08 80                         |
    | and word [rax + 1 * rcx - 0x81], cx                             | 66 21 8c 08 7f ff ff ff                |
    | and word [rax + 1 * rcx + 0xff], cx                             | 66 21 8c 08 ff 00 00 00                |
    | and word [rax + 1 * rcx - 0xff], cx                             | 66 21 8c 08 01 ff ff ff                |
    | and word [rax + 1 * rcx + 0x7fffffff], cx                       | 66 21 8c 08 ff ff ff 7f                |
    | and word [rax + 1 * rcx - 0x7fffffff], cx                       | 66 21 8c 08 01 00 00 80                |
    | and word [rax + 1 * rcx - 0x80000000], cx                       | 66 21 8c 08 00 00 00 80                |
    | and word [r10 + 0x7f], cx                                       | 66 41 21 4a 7f                         |
    | and word [r10 + 0x80], cx                                       | 66 41 21 8a 80 00 00 00                |
    | and word [r10 - 0x80], cx                                       | 66 41 21 4a 80                         |
    | and word [r10 - 0x81], cx                                       | 66 41 21 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and word [rel @prev5], cx      | 90 90 90 90 90 66 21 0d f4 ff ff ff    |
    | .prev1: nop; and word [rel @prev1], cx                          | 90 66 21 0d f8 ff ff ff                |
    | and word [rel @next1], cx; nop; .next1: nop                     | 66 21 0d 01 00 00 00 90 90             |
    | and word [rel @next5], cx; nop; nop; nop; nop; nop; .next5: nop | 66 21 0d 05 00 00 00 90 90 90 90 90 90 |
    | and word [rax], ax                                              | 66 21 00                               |
    | and word [rax], dx                                              | 66 21 10                               |
    | and word [rax], bx                                              | 66 21 18                               |
    | and word [rax], sp                                              | 66 21 20                               |
    | and word [rax], bp                                              | 66 21 28                               |
    | and word [rax], si                                              | 66 21 30                               |
    | and word [rax], di                                              | 66 21 38                               |
    | and word [rax], r8w                                             | 66 44 21 00                            |
    | and word [rax], r9w                                             | 66 44 21 08                            |
    | and word [rax], r10w                                            | 66 44 21 10                            |
    | and word [rax], r11w                                            | 66 44 21 18                            |
    | and word [rax], r12w                                            | 66 44 21 20                            |
    | and word [rax], r13w                                            | 66 44 21 28                            |
    | and word [rax], r14w                                            | 66 44 21 30                            |
    | and word [rax], r15w                                            | 66 44 21 38                            |
    | and word [rcx], dx                                              | 66 21 11                               |
    | and word [rdx], bx                                              | 66 21 1a                               |
    | and word [rbx], sp                                              | 66 21 23                               |
    | and word [rsp], bp                                              | 66 21 2c 24                            |
    | and word [rbp], si                                              | 66 21 75 00                            |
    | and word [rsi], di                                              | 66 21 3e                               |
    | and word [rdi], r8w                                             | 66 44 21 07                            |
    | and word [r8], r9w                                              | 66 45 21 08                            |
    | and word [r9], r10w                                             | 66 45 21 11                            |
    | and word [r10], r11w                                            | 66 45 21 1a                            |
    | and word [r11], r12w                                            | 66 45 21 23                            |
    | and word [r12], r13w                                            | 66 45 21 2c 24                         |
    | and word [r13], r14w                                            | 66 45 21 75 00                         |
    | and word [r14], r15w                                            | 66 45 21 3e                            |
    | and word [r15], ax                                              | 66 41 21 07                            |
    | and word [rcx + 1 * rcx], dx                                    | 66 21 14 09                            |
    | and word [rdx + 1 * rcx], bx                                    | 66 21 1c 0a                            |
    | and word [rbx + 1 * rcx], sp                                    | 66 21 24 0b                            |
    | and word [rsp + 1 * rcx], bp                                    | 66 21 2c 0c                            |
    | and word [rbp + 1 * rcx], si                                    | 66 21 74 0d 00                         |
    | and word [rsi + 1 * rcx], di                                    | 66 21 3c 0e                            |
    | and word [rdi + 1 * rcx], r8w                                   | 66 44 21 04 0f                         |
    | and word [r8 + 1 * rcx], r9w                                    | 66 45 21 0c 08                         |
    | and word [r9 + 1 * rcx], r10w                                   | 66 45 21 14 09                         |
    | and word [r10 + 1 * rcx], r11w                                  | 66 45 21 1c 0a                         |
    | and word [r11 + 1 * rcx], r12w                                  | 66 45 21 24 0b                         |
    | and word [r12 + 1 * rcx], r13w                                  | 66 45 21 2c 0c                         |
    | and word [r13 + 1 * rcx], r14w                                  | 66 45 21 74 0d 00                      |
    | and word [r14 + 1 * rcx], r15w                                  | 66 45 21 3c 0e                         |
    | and word [r15 + 1 * rcx], ax                                    | 66 41 21 04 0f                         |
    | and word [rax + 1 * rdx], dx                                    | 66 21 14 10                            |
    | and word [rax + 1 * rbx], bx                                    | 66 21 1c 18                            |
    | and word [rax + 1 * rbp], sp                                    | 66 21 24 28                            |
    | and word [rax + 1 * rsi], bp                                    | 66 21 2c 30                            |
    | and word [rax + 1 * rdi], si                                    | 66 21 34 38                            |
    | and word [rax + 1 * r8], di                                     | 66 42 21 3c 00                         |
    | and word [rax + 1 * r9], r8w                                    | 66 46 21 04 08                         |
    | and word [rax + 1 * r10], r9w                                   | 66 46 21 0c 10                         |
    | and word [rax + 1 * r11], r10w                                  | 66 46 21 14 18                         |
    | and word [rax + 1 * r12], r11w                                  | 66 46 21 1c 20                         |
    | and word [rax + 1 * r13], r12w                                  | 66 46 21 24 28                         |
    | and word [rax + 1 * r14], r13w                                  | 66 46 21 2c 30                         |
    | and word [rax + 1 * r15], r14w                                  | 66 46 21 34 38                         |
    | and word [rax + 2 * rcx], r15w                                  | 66 44 21 3c 48                         |
    | and word [rax + 4 * rcx], ax                                    | 66 21 04 88                            |
    | and word [r8 + 1 * r9], dx                                      | 66 43 21 14 08                         |
    | and word [r8 + 2 * r9], bx                                      | 66 43 21 1c 48                         |
    | and word [r8 + 4 * r9], sp                                      | 66 43 21 24 88                         |
    | and word [r8 + 8 * r9], bp                                      | 66 43 21 2c c8                         |
    | and word [1 * rcx], si                                          | 66 21 34 0d 00 00 00 00                |
    | and word [2 * rcx], di                                          | 66 21 3c 4d 00 00 00 00                |
    | and word [4 * rcx], r8w                                         | 66 44 21 04 8d 00 00 00 00             |
    | and word [8 * rcx], r9w                                         | 66 44 21 0c cd 00 00 00 00             |
    | and word [1 * r9], r10w                                         | 66 46 21 14 0d 00 00 00 00             |
    | and word [2 * r9], r11w                                         | 66 46 21 1c 4d 00 00 00 00             |
    | and word [4 * r9], r12w                                         | 66 46 21 24 8d 00 00 00 00             |
    | and word [8 * r9], r13w                                         | 66 46 21 2c cd 00 00 00 00             |
    | and word [r13 + 8 * r12], r14w                                  | 66 47 21 74 e5 00                      |
    | and word [rsp + 4 * r15], r15w                                  | 66 46 21 3c bc                         |
    | and word [rax + 1 * rcx + 0x00], ax                             | 66 21 44 08 00                         |
    | and word [rax + 1 * rcx + 0x01], dx                             | 66 21 54 08 01                         |
    | and word [rax + 1 * rcx - 0x01], bx                             | 66 21 5c 08 ff                         |
    | and word [rax + 1 * rcx + 0x00000001], sp                       | 66 21 a4 08 01 00 00 00                |
    | and word [rax + 1 * rcx - 0x00000001], bp                       | 66 21 ac 08 ff ff ff ff                |
    | and word [rax + 1 * rcx + 0x7f], si                             | 66 21 74 08 7f                         |
    | and word [rax + 1 * rcx - 0x7f], di                             | 66 21 7c 08 81                         |
    | and word [rax + 1 * rcx + 0x80], r8w                            | 66 44 21 84 08 80 00 00 00             |
    | and word [rax + 1 * rcx - 0x80], r9w                            | 66 44 21 4c 08 80                      |
    | and word [rax + 1 * rcx - 0x81], r10w                           | 66 44 21 94 08 7f ff ff ff             |
    | and word [rax + 1 * rcx + 0xff], r11w                           | 66 44 21 9c 08 ff 00 00 00             |
    | and word [rax + 1 * rcx - 0xff], r12w                           | 66 44 21 a4 08 01 ff ff ff             |
    | and word [rax + 1 * rcx + 0x7fffffff], r13w                     | 66 44 21 ac 08 ff ff ff 7f             |
    | and word [rax + 1 * rcx - 0x7fffffff], r14w                     | 66 44 21 b4 08 01 00 00 80             |
    | and word [rax + 1 * rcx - 0x80000000], r15w                     | 66 44 21 bc 08 00 00 00 80             |
    | and word [r10 + 0x7f], ax                                       | 66 41 21 42 7f                         |
    | and word [r10 - 0x80], dx                                       | 66 41 21 52 80                         |
    | and word [r10 - 0x81], bx                                       | 66 41 21 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; and word [rel @prev5], sp      | 90 90 90 90 90 66 21 25 f4 ff ff ff    |
    | .prev1: nop; and word [rel @prev1], bp                          | 90 66 21 2d f8 ff ff ff                |
    | and word [rel @next1], si; nop; .next1: nop                     | 66 21 35 01 00 00 00 90 90             |
    | and word [rel @next5], di; nop; nop; nop; nop; nop; .next5: nop | 66 21 3d 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_and_addr16_reg16():
    encode(AND_ADDR16_REG16)


AND_ADDR8_IMM8 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | and byte [rax], 0x01                                              | 80 20 01                               |
    | and byte [rcx], 0x01                                              | 80 21 01                               |
    | and byte [rdx], 0x01                                              | 80 22 01                               |
    | and byte [rbx], 0x01                                              | 80 23 01                               |
    | and byte [rsp], 0x01                                              | 80 24 24 01                            |
    | and byte [rbp], 0x01                                              | 80 65 00 01                            |
    | and byte [rsi], 0x01                                              | 80 26 01                               |
    | and byte [rdi], 0x01                                              | 80 27 01                               |
    | and byte [r8], 0x01                                               | 41 80 20 01                            |
    | and byte [r9], 0x01                                               | 41 80 21 01                            |
    | and byte [r10], 0x01                                              | 41 80 22 01                            |
    | and byte [r11], 0x01                                              | 41 80 23 01                            |
    | and byte [r12], 0x01                                              | 41 80 24 24 01                         |
    | and byte [r13], 0x01                                              | 41 80 65 00 01                         |
    | and byte [r14], 0x01                                              | 41 80 26 01                            |
    | and byte [r15], 0x01                                              | 41 80 27 01                            |
    | and byte [rax + 1 * rcx], 0x01                                    | 80 24 08 01                            |
    | and byte [rcx + 1 * rcx], 0x01                                    | 80 24 09 01                            |
    | and byte [rdx + 1 * rcx], 0x01                                    | 80 24 0a 01                            |
    | and byte [rbx + 1 * rcx], 0x01                                    | 80 24 0b 01                            |
    | and byte [rsp + 1 * rcx], 0x01                                    | 80 24 0c 01                            |
    | and byte [rbp + 1 * rcx], 0x01                                    | 80 64 0d 00 01                         |
    | and byte [rsi + 1 * rcx], 0x01                                    | 80 24 0e 01                            |
    | and byte [rdi + 1 * rcx], 0x01                                    | 80 24 0f 01                            |
    | and byte [r8 + 1 * rcx], 0x01                                     | 41 80 24 08 01                         |
    | and byte [r9 + 1 * rcx], 0x01                                     | 41 80 24 09 01                         |
    | and byte [r10 + 1 * rcx], 0x01                                    | 41 80 24 0a 01                         |
    | and byte [r11 + 1 * rcx], 0x01                                    | 41 80 24 0b 01                         |
    | and byte [r12 + 1 * rcx], 0x01                                    | 41 80 24 0c 01                         |
    | and byte [r13 + 1 * rcx], 0x01                                    | 41 80 64 0d 00 01                      |
    | and byte [r14 + 1 * rcx], 0x01                                    | 41 80 24 0e 01                         |
    | and byte [r15 + 1 * rcx], 0x01                                    | 41 80 24 0f 01                         |
    | and byte [rax + 1 * rax], 0x01                                    | 80 24 00 01                            |
    | and byte [rax + 1 * rdx], 0x01                                    | 80 24 10 01                            |
    | and byte [rax + 1 * rbx], 0x01                                    | 80 24 18 01                            |
    | and byte [rax + 1 * rbp], 0x01                                    | 80 24 28 01                            |
    | and byte [rax + 1 * rsi], 0x01                                    | 80 24 30 01                            |
    | and byte [rax + 1 * rdi], 0x01                                    | 80 24 38 01                            |
    | and byte [rax + 1 * r8], 0x01                                     | 42 80 24 00 01                         |
    | and byte [rax + 1 * r9], 0x01                                     | 42 80 24 08 01                         |
    | and byte [rax + 1 * r10], 0x01                                    | 42 80 24 10 01                         |
    | and byte [rax + 1 * r11], 0x01                                    | 42 80 24 18 01                         |
    | and byte [rax + 1 * r12], 0x01                                    | 42 80 24 20 01                         |
    | and byte [rax + 1 * r13], 0x01                                    | 42 80 24 28 01                         |
    | and byte [rax + 1 * r14], 0x01                                    | 42 80 24 30 01                         |
    | and byte [rax + 1 * r15], 0x01                                    | 42 80 24 38 01                         |
    | and byte [rax + 2 * rcx], 0x01                                    | 80 24 48 01                            |
    | and byte [rax + 4 * rcx], 0x01                                    | 80 24 88 01                            |
    | and byte [rax + 8 * rcx], 0x01                                    | 80 24 c8 01                            |
    | and byte [r8 + 1 * r9], 0x01                                      | 43 80 24 08 01                         |
    | and byte [r8 + 2 * r9], 0x01                                      | 43 80 24 48 01                         |
    | and byte [r8 + 4 * r9], 0x01                                      | 43 80 24 88 01                         |
    | and byte [r8 + 8 * r9], 0x01                                      | 43 80 24 c8 01                         |
    | and byte [1 * rcx], 0x01                                          | 80 24 0d 00 00 00 00 01                |
    | and byte [2 * rcx], 0x01                                          | 80 24 4d 00 00 00 00 01                |
    | and byte [4 * rcx], 0x01                                          | 80 24 8d 00 00 00 00 01                |
    | and byte [8 * rcx], 0x01                                          | 80 24 cd 00 00 00 00 01                |
    | and byte [1 * r9], 0x01                                           | 42 80 24 0d 00 00 00 00 01             |
    | and byte [2 * r9], 0x01                                           | 42 80 24 4d 00 00 00 00 01             |
    | and byte [4 * r9], 0x01                                           | 42 80 24 8d 00 00 00 00 01             |
    | and byte [8 * r9], 0x01                                           | 42 80 24 cd 00 00 00 00 01             |
    | and byte [r13 + 8 * r12], 0x01                                    | 43 80 64 e5 00 01                      |
    | and byte [rsp + 4 * r15], 0x01                                    | 42 80 24 bc 01                         |
    | and byte [rax + 1 * rcx + 0x00], 0x01                             | 80 64 08 00 01                         |
    | and byte [rax + 1 * rcx - 0x00], 0x01                             | 80 64 08 00 01                         |
    | and byte [rax + 1 * rcx + 0x01], 0x01                             | 80 64 08 01 01                         |
    | and byte [rax + 1 * rcx - 0x01], 0x01                             | 80 64 08 ff 01                         |
    | and byte [rax + 1 * rcx + 0x00000001], 0x01                       | 80 a4 08 01 00 00 00 01                |
    | and byte [rax + 1 * rcx - 0x00000001], 0x01                       | 80 a4 08 ff ff ff ff 01                |
    | and byte [rax + 1 * rcx + 0x7f], 0x01                             | 80 64 08 7f 01                         |
    | and byte [rax + 1 * rcx - 0x7f], 0x01                             | 80 64 08 81 01                         |
    | and byte [rax + 1 * rcx + 0x80], 0x01                             | 80 a4 08 80 00 00 00 01                |
    | and byte [rax + 1 * rcx - 0x80], 0x01                             | 80 64 08 80 01                         |
    | and byte [rax + 1 * rcx - 0x81], 0x01                             | 80 a4 08 7f ff ff ff 01                |
    | and byte [rax + 1 * rcx + 0xff], 0x01                             | 80 a4 08 ff 00 00 00 01                |
    | and byte [rax + 1 * rcx - 0xff], 0x01                             | 80 a4 08 01 ff ff ff 01                |
    | and byte [rax + 1 * rcx + 0x7fffffff], 0x01                       | 80 a4 08 ff ff ff 7f 01                |
    | and byte [rax + 1 * rcx - 0x7fffffff], 0x01                       | 80 a4 08 01 00 00 80 01                |
    | and byte [rax + 1 * rcx - 0x80000000], 0x01                       | 80 a4 08 00 00 00 80 01                |
    | and byte [r10 + 0x7f], 0x01                                       | 41 80 62 7f 01                         |
    | and byte [r10 + 0x80], 0x01                                       | 41 80 a2 80 00 00 00 01                |
    | and byte [r10 - 0x80], 0x01                                       | 41 80 62 80 01                         |
    | and byte [r10 - 0x81], 0x01                                       | 41 80 a2 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; and byte [rel @prev5], 0x01      | 90 90 90 90 90 80 25 f4 ff ff ff 01    |
    | .prev1: nop; and byte [rel @prev1], 0x01                          | 90 80 25 f8 ff ff ff 01                |
    | and byte [rel @next1], 0x01; nop; .next1: nop                     | 80 25 01 00 00 00 01 90 90             |
    | and byte [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 80 25 05 00 00 00 01 90 90 90 90 90 90 |
    | and byte [rax], 0x00                                              | 80 20 00                               |
    | and byte [rax], 0x7f                                              | 80 20 7f                               |
    | and byte [rax], 0x80                                              | 80 20 80                               |
    | and byte [rax], 0xff                                              | 80 20 ff                               |
    | and byte [rcx], 0x7f                                              | 80 21 7f                               |
    | and byte [rdx], 0x80                                              | 80 22 80                               |
    | and byte [rbx], 0xff                                              | 80 23 ff                               |
    | and byte [rsp], 0x00                                              | 80 24 24 00                            |
    | and byte [rsi], 0x7f                                              | 80 26 7f                               |
    | and byte [rdi], 0x80                                              | 80 27 80                               |
    | and byte [r8], 0xff                                               | 41 80 20 ff                            |
    | and byte [r9], 0x00                                               | 41 80 21 00                            |
    | and byte [r11], 0x7f                                              | 41 80 23 7f                            |
    | and byte [r12], 0x80                                              | 41 80 24 24 80                         |
    | and byte [r13], 0xff                                              | 41 80 65 00 ff                         |
    | and byte [r14], 0x00                                              | 41 80 26 00                            |
    | and byte [rax + 1 * rcx], 0x7f                                    | 80 24 08 7f                            |
    | and byte [rcx + 1 * rcx], 0x80                                    | 80 24 09 80                            |
    | and byte [rdx + 1 * rcx], 0xff                                    | 80 24 0a ff                            |
    | and byte [rbx + 1 * rcx], 0x00                                    | 80 24 0b 00                            |
    | and byte [rbp + 1 * rcx], 0x7f                                    | 80 64 0d 00 7f                         |
    | and byte [rsi + 1 * rcx], 0x80                                    | 80 24 0e 80                            |
    | and byte [rdi + 1 * rcx], 0xff                                    | 80 24 0f ff                            |
    | and byte [r8 + 1 * rcx], 0x00                                     | 41 80 24 08 00                         |
    | and byte [r10 + 1 * rcx], 0x7f                                    | 41 80 24 0a 7f                         |
    | and byte [r11 + 1 * rcx], 0x80                                    | 41 80 24 0b 80                         |
    | and byte [r12 + 1 * rcx], 0xff                                    | 41 80 24 0c ff                         |
    | and byte [r13 + 1 * rcx], 0x00                                    | 41 80 64 0d 00 00                      |
    | and byte [r15 + 1 * rcx], 0x7f                                    | 41 80 24 0f 7f                         |
    | and byte [rax + 1 * rax], 0x80                                    | 80 24 00 80                            |
    | and byte [rax + 1 * rdx], 0xff                                    | 80 24 10 ff                            |
    | and byte [rax + 1 * rbx], 0x00                                    | 80 24 18 00                            |
    | and byte [rax + 1 * rsi], 0x7f                                    | 80 24 30 7f                            |
    | and byte [rax + 1 * rdi], 0x80                                    | 80 24 38 80                            |
    | and byte [rax + 1 * r8], 0xff                                     | 42 80 24 00 ff                         |
    | and byte [rax + 1 * r9], 0x00                                     | 42 80 24 08 00                         |
    | and byte [rax + 1 * r11], 0x7f                                    | 42 80 24 18 7f                         |
    | and byte [rax + 1 * r12], 0x80                                    | 42 80 24 20 80                         |
    | and byte [rax + 1 * r13], 0xff                                    | 42 80 24 28 ff                         |
    | and byte [rax + 1 * r14], 0x00                                    | 42 80 24 30 00                         |
    | and byte [rax + 2 * rcx], 0x7f                                    | 80 24 48 7f                            |
    | and byte [rax + 4 * rcx], 0x80                                    | 80 24 88 80                            |
    | and byte [rax + 8 * rcx], 0xff                                    | 80 24 c8 ff                            |
    | and byte [r8 + 1 * r9], 0x00                                      | 43 80 24 08 00                         |
    | and byte [r8 + 4 * r9], 0x7f                                      | 43 80 24 88 7f                         |
    | and byte [r8 + 8 * r9], 0x80                                      | 43 80 24 c8 80                         |
    | and byte [1 * rcx], 0xff                                          | 80 24 0d 00 00 00 00 ff                |
    | and byte [2 * rcx], 0x00                                          | 80 24 4d 00 00 00 00 00                |
    | and byte [8 * rcx], 0x7f                                          | 80 24 cd 00 00 00 00 7f                |
    | and byte [1 * r9], 0x80                                           | 42 80 24 0d 00 00 00 00 80             |
    | and byte [2 * r9], 0xff                                           | 42 80 24 4d 00 00 00 00 ff             |
    | and byte [4 * r9], 0x00                                           | 42 80 24 8d 00 00 00 00 00             |
    | and byte [r13 + 8 * r12], 0x7f                                    | 43 80 64 e5 00 7f                      |
    | and byte [rsp + 4 * r15], 0x80                                    | 42 80 24 bc 80                         |
    | and byte [rax + 1 * rcx + 0x00], 0xff                             | 80 64 08 00 ff                         |
    | and byte [rax + 1 * rcx - 0x00], 0x00                             | 80 64 08 00 00                         |
    | and byte [rax + 1 * rcx - 0x01], 0x7f                             | 80 64 08 ff 7f                         |
    | and byte [rax + 1 * rcx + 0x00000001], 0x80                       | 80 a4 08 01 00 00 00 80                |
    | and byte [rax + 1 * rcx - 0x00000001], 0xff                       | 80 a4 08 ff ff ff ff ff                |
    | and byte [rax + 1 * rcx + 0x7f], 0x00                             | 80 64 08 7f 00                         |
    | and byte [rax + 1 * rcx + 0x80], 0x7f                             | 80 a4 08 80 00 00 00 7f                |
    | and byte [rax + 1 * rcx - 0x80], 0x80                             | 80 64 08 80 80                         |
    | and byte [rax + 1 * rcx - 0x81], 0xff                             | 80 a4 08 7f ff ff ff ff                |
    | and byte [rax + 1 * rcx + 0xff], 0x00                             | 80 a4 08 ff 00 00 00 00                |
    | and byte [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 80 a4 08 ff ff ff 7f 7f                |
    | and byte [rax + 1 * rcx - 0x7fffffff], 0x80                       | 80 a4 08 01 00 00 80 80                |
    | and byte [rax + 1 * rcx - 0x80000000], 0xff                       | 80 a4 08 00 00 00 80 ff                |
    | and byte [r10 + 0x7f], 0x00                                       | 41 80 62 7f 00                         |
    | and byte [r10 - 0x80], 0x7f                                       | 41 80 62 80 7f                         |
    | and byte [r10 - 0x81], 0x80                                       | 41 80 a2 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; and byte [rel @prev5], 0xff      | 90 90 90 90 90 80 25 f4 ff ff ff ff    |
    | .prev1: nop; and byte [rel @prev1], 0x00                          | 90 80 25 f8 ff ff ff 00                |
    | and byte [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 80 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_and_addr8_imm8():
    encode(AND_ADDR8_IMM8)


AND_ADDR8_REG8 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | and byte [rax], cl                                               | 20 08                                  |
    | and byte [rcx], cl                                               | 20 09                                  |
    | and byte [rdx], cl                                               | 20 0a                                  |
    | and byte [rbx], cl                                               | 20 0b                                  |
    | and byte [rsp], cl                                               | 20 0c 24                               |
    | and byte [rbp], cl                                               | 20 4d 00                               |
    | and byte [rsi], cl                                               | 20 0e                                  |
    | and byte [rdi], cl                                               | 20 0f                                  |
    | and byte [r8], cl                                                | 41 20 08                               |
    | and byte [r9], cl                                                | 41 20 09                               |
    | and byte [r10], cl                                               | 41 20 0a                               |
    | and byte [r11], cl                                               | 41 20 0b                               |
    | and byte [r12], cl                                               | 41 20 0c 24                            |
    | and byte [r13], cl                                               | 41 20 4d 00                            |
    | and byte [r14], cl                                               | 41 20 0e                               |
    | and byte [r15], cl                                               | 41 20 0f                               |
    | and byte [rax + 1 * rcx], cl                                     | 20 0c 08                               |
    | and byte [rcx + 1 * rcx], cl                                     | 20 0c 09                               |
    | and byte [rdx + 1 * rcx], cl                                     | 20 0c 0a                               |
    | and byte [rbx + 1 * rcx], cl                                     | 20 0c 0b                               |
    | and byte [rsp + 1 * rcx], cl                                     | 20 0c 0c                               |
    | and byte [rbp + 1 * rcx], cl                                     | 20 4c 0d 00                            |
    | and byte [rsi + 1 * rcx], cl                                     | 20 0c 0e                               |
    | and byte [rdi + 1 * rcx], cl                                     | 20 0c 0f                               |
    | and byte [r8 + 1 * rcx], cl                                      | 41 20 0c 08                            |
    | and byte [r9 + 1 * rcx], cl                                      | 41 20 0c 09                            |
    | and byte [r10 + 1 * rcx], cl                                     | 41 20 0c 0a                            |
    | and byte [r11 + 1 * rcx], cl                                     | 41 20 0c 0b                            |
    | and byte [r12 + 1 * rcx], cl                                     | 41 20 0c 0c                            |
    | and byte [r13 + 1 * rcx], cl                                     | 41 20 4c 0d 00                         |
    | and byte [r14 + 1 * rcx], cl                                     | 41 20 0c 0e                            |
    | and byte [r15 + 1 * rcx], cl                                     | 41 20 0c 0f                            |
    | and byte [rax + 1 * rax], cl                                     | 20 0c 00                               |
    | and byte [rax + 1 * rdx], cl                                     | 20 0c 10                               |
    | and byte [rax + 1 * rbx], cl                                     | 20 0c 18                               |
    | and byte [rax + 1 * rbp], cl                                     | 20 0c 28                               |
    | and byte [rax + 1 * rsi], cl                                     | 20 0c 30                               |
    | and byte [rax + 1 * rdi], cl                                     | 20 0c 38                               |
    | and byte [rax + 1 * r8], cl                                      | 42 20 0c 00                            |
    | and byte [rax + 1 * r9], cl                                      | 42 20 0c 08                            |
    | and byte [rax + 1 * r10], cl                                     | 42 20 0c 10                            |
    | and byte [rax + 1 * r11], cl                                     | 42 20 0c 18                            |
    | and byte [rax + 1 * r12], cl                                     | 42 20 0c 20                            |
    | and byte [rax + 1 * r13], cl                                     | 42 20 0c 28                            |
    | and byte [rax + 1 * r14], cl                                     | 42 20 0c 30                            |
    | and byte [rax + 1 * r15], cl                                     | 42 20 0c 38                            |
    | and byte [rax + 2 * rcx], cl                                     | 20 0c 48                               |
    | and byte [rax + 4 * rcx], cl                                     | 20 0c 88                               |
    | and byte [rax + 8 * rcx], cl                                     | 20 0c c8                               |
    | and byte [r8 + 1 * r9], cl                                       | 43 20 0c 08                            |
    | and byte [r8 + 2 * r9], cl                                       | 43 20 0c 48                            |
    | and byte [r8 + 4 * r9], cl                                       | 43 20 0c 88                            |
    | and byte [r8 + 8 * r9], cl                                       | 43 20 0c c8                            |
    | and byte [1 * rcx], cl                                           | 20 0c 0d 00 00 00 00                   |
    | and byte [2 * rcx], cl                                           | 20 0c 4d 00 00 00 00                   |
    | and byte [4 * rcx], cl                                           | 20 0c 8d 00 00 00 00                   |
    | and byte [8 * rcx], cl                                           | 20 0c cd 00 00 00 00                   |
    | and byte [1 * r9], cl                                            | 42 20 0c 0d 00 00 00 00                |
    | and byte [2 * r9], cl                                            | 42 20 0c 4d 00 00 00 00                |
    | and byte [4 * r9], cl                                            | 42 20 0c 8d 00 00 00 00                |
    | and byte [8 * r9], cl                                            | 42 20 0c cd 00 00 00 00                |
    | and byte [r13 + 8 * r12], cl                                     | 43 20 4c e5 00                         |
    | and byte [rsp + 4 * r15], cl                                     | 42 20 0c bc                            |
    | and byte [rax + 1 * rcx + 0x00], cl                              | 20 4c 08 00                            |
    | and byte [rax + 1 * rcx - 0x00], cl                              | 20 4c 08 00                            |
    | and byte [rax + 1 * rcx + 0x01], cl                              | 20 4c 08 01                            |
    | and byte [rax + 1 * rcx - 0x01], cl                              | 20 4c 08 ff                            |
    | and byte [rax + 1 * rcx + 0x00000001], cl                        | 20 8c 08 01 00 00 00                   |
    | and byte [rax + 1 * rcx - 0x00000001], cl                        | 20 8c 08 ff ff ff ff                   |
    | and byte [rax + 1 * rcx + 0x7f], cl                              | 20 4c 08 7f                            |
    | and byte [rax + 1 * rcx - 0x7f], cl                              | 20 4c 08 81                            |
    | and byte [rax + 1 * rcx + 0x80], cl                              | 20 8c 08 80 00 00 00                   |
    | and byte [rax + 1 * rcx - 0x80], cl                              | 20 4c 08 80                            |
    | and byte [rax + 1 * rcx - 0x81], cl                              | 20 8c 08 7f ff ff ff                   |
    | and byte [rax + 1 * rcx + 0xff], cl                              | 20 8c 08 ff 00 00 00                   |
    | and byte [rax + 1 * rcx - 0xff], cl                              | 20 8c 08 01 ff ff ff                   |
    | and byte [rax + 1 * rcx + 0x7fffffff], cl                        | 20 8c 08 ff ff ff 7f                   |
    | and byte [rax + 1 * rcx - 0x7fffffff], cl                        | 20 8c 08 01 00 00 80                   |
    | and byte [rax + 1 * rcx - 0x80000000], cl                        | 20 8c 08 00 00 00 80                   |
    | and byte [r10 + 0x7f], cl                                        | 41 20 4a 7f                            |
    | and byte [r10 + 0x80], cl                                        | 41 20 8a 80 00 00 00                   |
    | and byte [r10 - 0x80], cl                                        | 41 20 4a 80                            |
    | and byte [r10 - 0x81], cl                                        | 41 20 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and byte [rel @prev5], cl       | 90 90 90 90 90 20 0d f5 ff ff ff       |
    | .prev1: nop; and byte [rel @prev1], cl                           | 90 20 0d f9 ff ff ff                   |
    | and byte [rel @next1], cl; nop; .next1: nop                      | 20 0d 01 00 00 00 90 90                |
    | and byte [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop  | 20 0d 05 00 00 00 90 90 90 90 90 90    |
    | and byte [rax], al                                               | 20 00                                  |
    | and byte [rax], dl                                               | 20 10                                  |
    | and byte [rax], bl                                               | 20 18                                  |
    | and byte [rax], spl                                              | 40 20 20                               |
    | and byte [rax], bpl                                              | 40 20 28                               |
    | and byte [rax], sil                                              | 40 20 30                               |
    | and byte [rax], dil                                              | 40 20 38                               |
    | and byte [rax], r8b                                              | 44 20 00                               |
    | and byte [rax], r9b                                              | 44 20 08                               |
    | and byte [rax], r10b                                             | 44 20 10                               |
    | and byte [rax], r11b                                             | 44 20 18                               |
    | and byte [rax], r12b                                             | 44 20 20                               |
    | and byte [rax], r13b                                             | 44 20 28                               |
    | and byte [rax], r14b                                             | 44 20 30                               |
    | and byte [rax], r15b                                             | 44 20 38                               |
    | and byte [rax], ah                                               | 20 20                                  |
    | and byte [rax], ch                                               | 20 28                                  |
    | and byte [rax], dh                                               | 20 30                                  |
    | and byte [rax], bh                                               | 20 38                                  |
    | and byte [rcx], dl                                               | 20 11                                  |
    | and byte [rdx], bl                                               | 20 1a                                  |
    | and byte [rbx], spl                                              | 40 20 23                               |
    | and byte [rsp], bpl                                              | 40 20 2c 24                            |
    | and byte [rbp], sil                                              | 40 20 75 00                            |
    | and byte [rsi], dil                                              | 40 20 3e                               |
    | and byte [rdi], r8b                                              | 44 20 07                               |
    | and byte [r8], r9b                                               | 45 20 08                               |
    | and byte [r9], r10b                                              | 45 20 11                               |
    | and byte [r10], r11b                                             | 45 20 1a                               |
    | and byte [r11], r12b                                             | 45 20 23                               |
    | and byte [r12], r13b                                             | 45 20 2c 24                            |
    | and byte [r13], r14b                                             | 45 20 75 00                            |
    | and byte [r14], r15b                                             | 45 20 3e                               |
    | and byte [r15], ah                                               | !! !! !!                               |
    | and byte [rax + 1 * rcx], ch                                     | 20 2c 08                               |
    | and byte [rcx + 1 * rcx], dh                                     | 20 34 09                               |
    | and byte [rdx + 1 * rcx], bh                                     | 20 3c 0a                               |
    | and byte [rbx + 1 * rcx], al                                     | 20 04 0b                               |
    | and byte [rbp + 1 * rcx], dl                                     | 20 54 0d 00                            |
    | and byte [rsi + 1 * rcx], bl                                     | 20 1c 0e                               |
    | and byte [rdi + 1 * rcx], spl                                    | 40 20 24 0f                            |
    | and byte [r8 + 1 * rcx], bpl                                     | 41 20 2c 08                            |
    | and byte [r9 + 1 * rcx], sil                                     | 41 20 34 09                            |
    | and byte [r10 + 1 * rcx], dil                                    | 41 20 3c 0a                            |
    | and byte [r11 + 1 * rcx], r8b                                    | 45 20 04 0b                            |
    | and byte [r12 + 1 * rcx], r9b                                    | 45 20 0c 0c                            |
    | and byte [r13 + 1 * rcx], r10b                                   | 45 20 54 0d 00                         |
    | and byte [r14 + 1 * rcx], r11b                                   | 45 20 1c 0e                            |
    | and byte [r15 + 1 * rcx], r12b                                   | 45 20 24 0f                            |
    | and byte [rax + 1 * rax], r13b                                   | 44 20 2c 00                            |
    | and byte [rax + 1 * rdx], r14b                                   | 44 20 34 10                            |
    | and byte [rax + 1 * rbx], r15b                                   | 44 20 3c 18                            |
    | and byte [rax + 1 * rbp], ah                                     | 20 24 28                               |
    | and byte [rax + 1 * rsi], ch                                     | 20 2c 30                               |
    | and byte [rax + 1 * rdi], dh                                     | 20 34 38                               |
    | and byte [rax + 1 * r8], bh                                      | !! !! !!                               |
    | and byte [rax + 1 * r9], al                                      | 42 20 04 08                            |
    | and byte [rax + 1 * r11], dl                                     | 42 20 14 18                            |
    | and byte [rax + 1 * r12], bl                                     | 42 20 1c 20                            |
    | and byte [rax + 1 * r13], spl                                    | 42 20 24 28                            |
    | and byte [rax + 1 * r14], bpl                                    | 42 20 2c 30                            |
    | and byte [rax + 1 * r15], sil                                    | 42 20 34 38                            |
    | and byte [rax + 2 * rcx], dil                                    | 40 20 3c 48                            |
    | and byte [rax + 4 * rcx], r8b                                    | 44 20 04 88                            |
    | and byte [rax + 8 * rcx], r9b                                    | 44 20 0c c8                            |
    | and byte [r8 + 1 * r9], r10b                                     | 47 20 14 08                            |
    | and byte [r8 + 2 * r9], r11b                                     | 47 20 1c 48                            |
    | and byte [r8 + 4 * r9], r12b                                     | 47 20 24 88                            |
    | and byte [r8 + 8 * r9], r13b                                     | 47 20 2c c8                            |
    | and byte [1 * rcx], r14b                                         | 44 20 34 0d 00 00 00 00                |
    | and byte [2 * rcx], r15b                                         | 44 20 3c 4d 00 00 00 00                |
    | and byte [4 * rcx], ah                                           | 20 24 8d 00 00 00 00                   |
    | and byte [8 * rcx], ch                                           | 20 2c cd 00 00 00 00                   |
    | and byte [1 * r9], dh                                            | !! !! !!                               |
    | and byte [2 * r9], bh                                            | !! !! !!                               |
    | and byte [4 * r9], al                                            | 42 20 04 8d 00 00 00 00                |
    | and byte [r13 + 8 * r12], dl                                     | 43 20 54 e5 00                         |
    | and byte [rsp + 4 * r15], bl                                     | 42 20 1c bc                            |
    | and byte [rax + 1 * rcx + 0x00], spl                             | 40 20 64 08 00                         |
    | and byte [rax + 1 * rcx - 0x00], bpl                             | 40 20 6c 08 00                         |
    | and byte [rax + 1 * rcx + 0x01], sil                             | 40 20 74 08 01                         |
    | and byte [rax + 1 * rcx - 0x01], dil                             | 40 20 7c 08 ff                         |
    | and byte [rax + 1 * rcx + 0x00000001], r8b                       | 44 20 84 08 01 00 00 00                |
    | and byte [rax + 1 * rcx - 0x00000001], r9b                       | 44 20 8c 08 ff ff ff ff                |
    | and byte [rax + 1 * rcx + 0x7f], r10b                            | 44 20 54 08 7f                         |
    | and byte [rax + 1 * rcx - 0x7f], r11b                            | 44 20 5c 08 81                         |
    | and byte [rax + 1 * rcx + 0x80], r12b                            | 44 20 a4 08 80 00 00 00                |
    | and byte [rax + 1 * rcx - 0x80], r13b                            | 44 20 6c 08 80                         |
    | and byte [rax + 1 * rcx - 0x81], r14b                            | 44 20 b4 08 7f ff ff ff                |
    | and byte [rax + 1 * rcx + 0xff], r15b                            | 44 20 bc 08 ff 00 00 00                |
    | and byte [rax + 1 * rcx - 0xff], ah                              | 20 a4 08 01 ff ff ff                   |
    | and byte [rax + 1 * rcx + 0x7fffffff], ch                        | 20 ac 08 ff ff ff 7f                   |
    | and byte [rax + 1 * rcx - 0x7fffffff], dh                        | 20 b4 08 01 00 00 80                   |
    | and byte [rax + 1 * rcx - 0x80000000], bh                        | 20 bc 08 00 00 00 80                   |
    | and byte [r10 + 0x7f], al                                        | 41 20 42 7f                            |
    | and byte [r10 - 0x80], dl                                        | 41 20 52 80                            |
    | and byte [r10 - 0x81], bl                                        | 41 20 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; and byte [rel @prev5], spl      | 90 90 90 90 90 40 20 25 f4 ff ff ff    |
    | .prev1: nop; and byte [rel @prev1], bpl                          | 90 40 20 2d f8 ff ff ff                |
    | and byte [rel @next1], sil; nop; .next1: nop                     | 40 20 35 01 00 00 00 90 90             |
    | and byte [rel @next5], dil; nop; nop; nop; nop; nop; .next5: nop | 40 20 3d 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_and_addr8_reg8():
    encode(AND_ADDR8_REG8)
