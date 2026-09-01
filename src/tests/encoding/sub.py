from tests.encoding.core import encode, exhaust


def can_exhaust_sub():
    exhaust(
        SUB_ADDR16_IMM16,
        SUB_ADDR16_IMM8,
        SUB_ADDR16_REG16,
        SUB_ADDR32_IMM32,
        SUB_ADDR32_IMM8,
        SUB_ADDR32_REG32,
        SUB_ADDR64_IMM32,
        SUB_ADDR64_IMM8,
        SUB_ADDR64_REG64,
        SUB_ADDR8_IMM8,
        SUB_ADDR8_REG8,
        SUB_REG16_ADDR16,
        SUB_REG16_IMM16,
        SUB_REG16_IMM8,
        SUB_REG16_REG16,
        SUB_REG32_ADDR32,
        SUB_REG32_IMM32,
        SUB_REG32_IMM8,
        SUB_REG32_REG32,
        SUB_REG64_ADDR64,
        SUB_REG64_IMM32,
        SUB_REG64_IMM8,
        SUB_REG64_REG64,
        SUB_REG8_ADDR8,
        SUB_REG8_IMM8,
        SUB_REG8_REG8,
    )


SUB_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | sub rax, 0x01 | 48 83 e8 01 | *** | sub rax, 0x00 | 48 83 e8 00 |
    | sub rcx, 0x01 | 48 83 e9 01 | *** | sub rax, 0x7f | 48 83 e8 7f |
    | sub rdx, 0x01 | 48 83 ea 01 | *** | sub rax, 0x80 | 48 83 e8 80 |
    | sub rbx, 0x01 | 48 83 eb 01 | *** | sub rax, 0xff | 48 83 e8 ff |
    | sub rsp, 0x01 | 48 83 ec 01 | *** | sub rcx, 0x7f | 48 83 e9 7f |
    | sub rbp, 0x01 | 48 83 ed 01 | *** | sub rdx, 0x80 | 48 83 ea 80 |
    | sub rsi, 0x01 | 48 83 ee 01 | *** | sub rbx, 0xff | 48 83 eb ff |
    | sub rdi, 0x01 | 48 83 ef 01 | *** | sub rsp, 0x00 | 48 83 ec 00 |
    | sub r8, 0x01  | 49 83 e8 01 | *** | sub rsi, 0x7f | 48 83 ee 7f |
    | sub r9, 0x01  | 49 83 e9 01 | *** | sub rdi, 0x80 | 48 83 ef 80 |
    | sub r10, 0x01 | 49 83 ea 01 | *** | sub r8, 0xff  | 49 83 e8 ff |
    | sub r11, 0x01 | 49 83 eb 01 | *** | sub r9, 0x00  | 49 83 e9 00 |
    | sub r12, 0x01 | 49 83 ec 01 | *** | sub r11, 0x7f | 49 83 eb 7f |
    | sub r13, 0x01 | 49 83 ed 01 | *** | sub r12, 0x80 | 49 83 ec 80 |
    | sub r14, 0x01 | 49 83 ee 01 | *** | sub r13, 0xff | 49 83 ed ff |
    | sub r15, 0x01 | 49 83 ef 01 | *** | sub r14, 0x00 | 49 83 ee 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_sub_reg64_imm8():
    encode(SUB_REG64_IMM8)


SUB_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | sub rax, 0x00000001 | 48 2d 01 00 00 00    | *** | sub rax, 0x00007fff | 48 2d ff 7f 00 00    |
    | sub rcx, 0x00000001 | 48 81 e9 01 00 00 00 | *** | sub rax, 0x00008000 | 48 2d 00 80 00 00    |
    | sub rdx, 0x00000001 | 48 81 ea 01 00 00 00 | *** | sub rax, 0x0000ffff | 48 2d ff ff 00 00    |
    | sub rbx, 0x00000001 | 48 81 eb 01 00 00 00 | *** | sub rax, 0x00010000 | 48 2d 00 00 01 00    |
    | sub rsp, 0x00000001 | 48 81 ec 01 00 00 00 | *** | sub rax, 0x7fffffff | 48 2d ff ff ff 7f    |
    | sub rbp, 0x00000001 | 48 81 ed 01 00 00 00 | *** | sub rax, 0x80000000 | 48 2d 00 00 00 80    |
    | sub rsi, 0x00000001 | 48 81 ee 01 00 00 00 | *** | sub rax, 0xffffffff | 48 2d ff ff ff ff    |
    | sub rdi, 0x00000001 | 48 81 ef 01 00 00 00 | *** | sub rcx, 0x0000007f | 48 81 e9 7f 00 00 00 |
    | sub r8, 0x00000001  | 49 81 e8 01 00 00 00 | *** | sub rdx, 0x00000080 | 48 81 ea 80 00 00 00 |
    | sub r9, 0x00000001  | 49 81 e9 01 00 00 00 | *** | sub rbx, 0x000000ff | 48 81 eb ff 00 00 00 |
    | sub r10, 0x00000001 | 49 81 ea 01 00 00 00 | *** | sub rsp, 0x00000100 | 48 81 ec 00 01 00 00 |
    | sub r11, 0x00000001 | 49 81 eb 01 00 00 00 | *** | sub rbp, 0x00007fff | 48 81 ed ff 7f 00 00 |
    | sub r12, 0x00000001 | 49 81 ec 01 00 00 00 | *** | sub rsi, 0x00008000 | 48 81 ee 00 80 00 00 |
    | sub r13, 0x00000001 | 49 81 ed 01 00 00 00 | *** | sub rdi, 0x0000ffff | 48 81 ef ff ff 00 00 |
    | sub r14, 0x00000001 | 49 81 ee 01 00 00 00 | *** | sub r8, 0x00010000  | 49 81 e8 00 00 01 00 |
    | sub r15, 0x00000001 | 49 81 ef 01 00 00 00 | *** | sub r9, 0x7fffffff  | 49 81 e9 ff ff ff 7f |
    | sub rax, 0x00000000 | 48 2d 00 00 00 00    | *** | sub r10, 0x80000000 | 49 81 ea 00 00 00 80 |
    | sub rax, 0x0000007f | 48 2d 7f 00 00 00    | *** | sub r11, 0xffffffff | 49 81 eb ff ff ff ff |
    | sub rax, 0x00000080 | 48 2d 80 00 00 00    | *** | sub r12, 0x00000000 | 49 81 ec 00 00 00 00 |
    | sub rax, 0x000000ff | 48 2d ff 00 00 00    | *** | sub r14, 0x0000007f | 49 81 ee 7f 00 00 00 |
    | sub rax, 0x00000100 | 48 2d 00 01 00 00    | *** | sub r15, 0x00000080 | 49 81 ef 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_sub_reg64_imm32():
    encode(SUB_REG64_IMM32)


SUB_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | sub rax, rcx | 48 29 c8 | *** | sub rax, r8  | 4c 29 c0 |
    | sub rcx, rcx | 48 29 c9 | *** | sub rax, r9  | 4c 29 c8 |
    | sub rdx, rcx | 48 29 ca | *** | sub rax, r10 | 4c 29 d0 |
    | sub rbx, rcx | 48 29 cb | *** | sub rax, r11 | 4c 29 d8 |
    | sub rsp, rcx | 48 29 cc | *** | sub rax, r12 | 4c 29 e0 |
    | sub rbp, rcx | 48 29 cd | *** | sub rax, r13 | 4c 29 e8 |
    | sub rsi, rcx | 48 29 ce | *** | sub rax, r14 | 4c 29 f0 |
    | sub rdi, rcx | 48 29 cf | *** | sub rax, r15 | 4c 29 f8 |
    | sub r8, rcx  | 49 29 c8 | *** | sub rcx, rdx | 48 29 d1 |
    | sub r9, rcx  | 49 29 c9 | *** | sub rdx, rbx | 48 29 da |
    | sub r10, rcx | 49 29 ca | *** | sub rbx, rsp | 48 29 e3 |
    | sub r11, rcx | 49 29 cb | *** | sub rsp, rbp | 48 29 ec |
    | sub r12, rcx | 49 29 cc | *** | sub rbp, rsi | 48 29 f5 |
    | sub r13, rcx | 49 29 cd | *** | sub rsi, rdi | 48 29 fe |
    | sub r14, rcx | 49 29 ce | *** | sub rdi, r8  | 4c 29 c7 |
    | sub r15, rcx | 49 29 cf | *** | sub r8, r9   | 4d 29 c8 |
    | sub rax, rax | 48 29 c0 | *** | sub r9, r10  | 4d 29 d1 |
    | sub rax, rdx | 48 29 d0 | *** | sub r10, r11 | 4d 29 da |
    | sub rax, rbx | 48 29 d8 | *** | sub r11, r12 | 4d 29 e3 |
    | sub rax, rsp | 48 29 e0 | *** | sub r12, r13 | 4d 29 ec |
    | sub rax, rbp | 48 29 e8 | *** | sub r13, r14 | 4d 29 f5 |
    | sub rax, rsi | 48 29 f0 | *** | sub r14, r15 | 4d 29 fe |
    | sub rax, rdi | 48 29 f8 | *** | sub r15, rax | 49 29 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_sub_reg64_reg64():
    encode(SUB_REG64_REG64)


SUB_REG64_ADDR64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | sub rax, qword [rcx]                        | 48 2b 01                |
    | sub rcx, qword [rcx]                        | 48 2b 09                |
    | sub rdx, qword [rcx]                        | 48 2b 11                |
    | sub rbx, qword [rcx]                        | 48 2b 19                |
    | sub rsp, qword [rcx]                        | 48 2b 21                |
    | sub rbp, qword [rcx]                        | 48 2b 29                |
    | sub rsi, qword [rcx]                        | 48 2b 31                |
    | sub rdi, qword [rcx]                        | 48 2b 39                |
    | sub r8, qword [rcx]                         | 4c 2b 01                |
    | sub r9, qword [rcx]                         | 4c 2b 09                |
    | sub r10, qword [rcx]                        | 4c 2b 11                |
    | sub r11, qword [rcx]                        | 4c 2b 19                |
    | sub r12, qword [rcx]                        | 4c 2b 21                |
    | sub r13, qword [rcx]                        | 4c 2b 29                |
    | sub r14, qword [rcx]                        | 4c 2b 31                |
    | sub r15, qword [rcx]                        | 4c 2b 39                |
    | sub rax, qword [rax]                        | 48 2b 00                |
    | sub rax, qword [rdx]                        | 48 2b 02                |
    | sub rax, qword [rbx]                        | 48 2b 03                |
    | sub rax, qword [rsp]                        | 48 2b 04 24             |
    | sub rax, qword [rbp]                        | 48 2b 45 00             |
    | sub rax, qword [rsi]                        | 48 2b 06                |
    | sub rax, qword [rdi]                        | 48 2b 07                |
    | sub rax, qword [r8]                         | 49 2b 00                |
    | sub rax, qword [r9]                         | 49 2b 01                |
    | sub rax, qword [r10]                        | 49 2b 02                |
    | sub rax, qword [r11]                        | 49 2b 03                |
    | sub rax, qword [r12]                        | 49 2b 04 24             |
    | sub rax, qword [r13]                        | 49 2b 45 00             |
    | sub rax, qword [r14]                        | 49 2b 06                |
    | sub rax, qword [r15]                        | 49 2b 07                |
    | sub rax, qword [rax + 1 * rcx]              | 48 2b 04 08             |
    | sub rax, qword [rcx + 1 * rcx]              | 48 2b 04 09             |
    | sub rax, qword [rdx + 1 * rcx]              | 48 2b 04 0a             |
    | sub rax, qword [rbx + 1 * rcx]              | 48 2b 04 0b             |
    | sub rax, qword [rsp + 1 * rcx]              | 48 2b 04 0c             |
    | sub rax, qword [rbp + 1 * rcx]              | 48 2b 44 0d 00          |
    | sub rax, qword [rsi + 1 * rcx]              | 48 2b 04 0e             |
    | sub rax, qword [rdi + 1 * rcx]              | 48 2b 04 0f             |
    | sub rax, qword [r8 + 1 * rcx]               | 49 2b 04 08             |
    | sub rax, qword [r9 + 1 * rcx]               | 49 2b 04 09             |
    | sub rax, qword [r10 + 1 * rcx]              | 49 2b 04 0a             |
    | sub rax, qword [r11 + 1 * rcx]              | 49 2b 04 0b             |
    | sub rax, qword [r12 + 1 * rcx]              | 49 2b 04 0c             |
    | sub rax, qword [r13 + 1 * rcx]              | 49 2b 44 0d 00          |
    | sub rax, qword [r14 + 1 * rcx]              | 49 2b 04 0e             |
    | sub rax, qword [r15 + 1 * rcx]              | 49 2b 04 0f             |
    | sub rax, qword [rax + 1 * rax]              | 48 2b 04 00             |
    | sub rax, qword [rax + 1 * rdx]              | 48 2b 04 10             |
    | sub rax, qword [rax + 1 * rbx]              | 48 2b 04 18             |
    | sub rax, qword [rax + 1 * rbp]              | 48 2b 04 28             |
    | sub rax, qword [rax + 1 * rsi]              | 48 2b 04 30             |
    | sub rax, qword [rax + 1 * rdi]              | 48 2b 04 38             |
    | sub rax, qword [rax + 1 * r8]               | 4a 2b 04 00             |
    | sub rax, qword [rax + 1 * r9]               | 4a 2b 04 08             |
    | sub rax, qword [rax + 1 * r10]              | 4a 2b 04 10             |
    | sub rax, qword [rax + 1 * r11]              | 4a 2b 04 18             |
    | sub rax, qword [rax + 1 * r12]              | 4a 2b 04 20             |
    | sub rax, qword [rax + 1 * r13]              | 4a 2b 04 28             |
    | sub rax, qword [rax + 1 * r14]              | 4a 2b 04 30             |
    | sub rax, qword [rax + 1 * r15]              | 4a 2b 04 38             |
    | sub rax, qword [rax + 2 * rcx]              | 48 2b 04 48             |
    | sub rax, qword [rax + 4 * rcx]              | 48 2b 04 88             |
    | sub rax, qword [rax + 8 * rcx]              | 48 2b 04 c8             |
    | sub rax, qword [r8 + 1 * r9]                | 4b 2b 04 08             |
    | sub rax, qword [r8 + 2 * r9]                | 4b 2b 04 48             |
    | sub rax, qword [r8 + 4 * r9]                | 4b 2b 04 88             |
    | sub rax, qword [r8 + 8 * r9]                | 4b 2b 04 c8             |
    | sub rax, qword [1 * rcx]                    | 48 2b 04 0d 00 00 00 00 |
    | sub rax, qword [2 * rcx]                    | 48 2b 04 4d 00 00 00 00 |
    | sub rax, qword [4 * rcx]                    | 48 2b 04 8d 00 00 00 00 |
    | sub rax, qword [8 * rcx]                    | 48 2b 04 cd 00 00 00 00 |
    | sub rax, qword [1 * r9]                     | 4a 2b 04 0d 00 00 00 00 |
    | sub rax, qword [2 * r9]                     | 4a 2b 04 4d 00 00 00 00 |
    | sub rax, qword [4 * r9]                     | 4a 2b 04 8d 00 00 00 00 |
    | sub rax, qword [8 * r9]                     | 4a 2b 04 cd 00 00 00 00 |
    | sub rax, qword [r13 + 8 * r12]              | 4b 2b 44 e5 00          |
    | sub rax, qword [rsp + 4 * r15]              | 4a 2b 04 bc             |
    | sub rax, qword [rax + 1 * rcx + 0x00]       | 48 2b 44 08 00          |
    | sub rax, qword [rax + 1 * rcx - 0x00]       | 48 2b 44 08 00          |
    | sub rax, qword [rax + 1 * rcx + 0x01]       | 48 2b 44 08 01          |
    | sub rax, qword [rax + 1 * rcx - 0x01]       | 48 2b 44 08 ff          |
    | sub rax, qword [rax + 1 * rcx + 0x00000001] | 48 2b 84 08 01 00 00 00 |
    | sub rax, qword [rax + 1 * rcx - 0x00000001] | 48 2b 84 08 ff ff ff ff |
    | sub rax, qword [rax + 1 * rcx + 0x7f]       | 48 2b 44 08 7f          |
    | sub rax, qword [rax + 1 * rcx - 0x7f]       | 48 2b 44 08 81          |
    | sub rax, qword [rax + 1 * rcx + 0x80]       | 48 2b 84 08 80 00 00 00 |
    | sub rax, qword [rax + 1 * rcx - 0x80]       | 48 2b 44 08 80          |
    | sub rax, qword [rax + 1 * rcx - 0x81]       | 48 2b 84 08 7f ff ff ff |
    | sub rax, qword [rax + 1 * rcx + 0xff]       | 48 2b 84 08 ff 00 00 00 |
    | sub rax, qword [rax + 1 * rcx - 0xff]       | 48 2b 84 08 01 ff ff ff |
    | sub rax, qword [rax + 1 * rcx + 0x7fffffff] | 48 2b 84 08 ff ff ff 7f |
    | sub rax, qword [rax + 1 * rcx - 0x7fffffff] | 48 2b 84 08 01 00 00 80 |
    | sub rax, qword [rax + 1 * rcx - 0x80000000] | 48 2b 84 08 00 00 00 80 |
    | sub rax, qword [r10 + 0x7f]                 | 49 2b 42 7f             |
    | sub rax, qword [r10 + 0x80]                 | 49 2b 82 80 00 00 00    |
    | sub rax, qword [r10 - 0x80]                 | 49 2b 42 80             |
    | sub rax, qword [r10 - 0x81]                 | 49 2b 82 7f ff ff ff    |
    | sub rcx, qword [rdx]                        | 48 2b 0a                |
    | sub rdx, qword [rbx]                        | 48 2b 13                |
    | sub rbx, qword [rsp]                        | 48 2b 1c 24             |
    | sub rsp, qword [rbp]                        | 48 2b 65 00             |
    | sub rbp, qword [rsi]                        | 48 2b 2e                |
    | sub rsi, qword [rdi]                        | 48 2b 37                |
    | sub rdi, qword [r8]                         | 49 2b 38                |
    | sub r8, qword [r9]                          | 4d 2b 01                |
    | sub r9, qword [r10]                         | 4d 2b 0a                |
    | sub r10, qword [r11]                        | 4d 2b 13                |
    | sub r11, qword [r12]                        | 4d 2b 1c 24             |
    | sub r12, qword [r13]                        | 4d 2b 65 00             |
    | sub r13, qword [r14]                        | 4d 2b 2e                |
    | sub r14, qword [r15]                        | 4d 2b 37                |
    | sub r15, qword [rax + 1 * rcx]              | 4c 2b 3c 08             |
    | sub rcx, qword [rdx + 1 * rcx]              | 48 2b 0c 0a             |
    | sub rdx, qword [rbx + 1 * rcx]              | 48 2b 14 0b             |
    | sub rbx, qword [rsp + 1 * rcx]              | 48 2b 1c 0c             |
    | sub rsp, qword [rbp + 1 * rcx]              | 48 2b 64 0d 00          |
    | sub rbp, qword [rsi + 1 * rcx]              | 48 2b 2c 0e             |
    | sub rsi, qword [rdi + 1 * rcx]              | 48 2b 34 0f             |
    | sub rdi, qword [r8 + 1 * rcx]               | 49 2b 3c 08             |
    | sub r8, qword [r9 + 1 * rcx]                | 4d 2b 04 09             |
    | sub r9, qword [r10 + 1 * rcx]               | 4d 2b 0c 0a             |
    | sub r10, qword [r11 + 1 * rcx]              | 4d 2b 14 0b             |
    | sub r11, qword [r12 + 1 * rcx]              | 4d 2b 1c 0c             |
    | sub r12, qword [r13 + 1 * rcx]              | 4d 2b 64 0d 00          |
    | sub r13, qword [r14 + 1 * rcx]              | 4d 2b 2c 0e             |
    | sub r14, qword [r15 + 1 * rcx]              | 4d 2b 34 0f             |
    | sub r15, qword [rax + 1 * rax]              | 4c 2b 3c 00             |
    | sub rcx, qword [rax + 1 * rbx]              | 48 2b 0c 18             |
    | sub rdx, qword [rax + 1 * rbp]              | 48 2b 14 28             |
    | sub rbx, qword [rax + 1 * rsi]              | 48 2b 1c 30             |
    | sub rsp, qword [rax + 1 * rdi]              | 48 2b 24 38             |
    | sub rbp, qword [rax + 1 * r8]               | 4a 2b 2c 00             |
    | sub rsi, qword [rax + 1 * r9]               | 4a 2b 34 08             |
    | sub rdi, qword [rax + 1 * r10]              | 4a 2b 3c 10             |
    | sub r8, qword [rax + 1 * r11]               | 4e 2b 04 18             |
    | sub r9, qword [rax + 1 * r12]               | 4e 2b 0c 20             |
    | sub r10, qword [rax + 1 * r13]              | 4e 2b 14 28             |
    | sub r11, qword [rax + 1 * r14]              | 4e 2b 1c 30             |
    | sub r12, qword [rax + 1 * r15]              | 4e 2b 24 38             |
    | sub r13, qword [rax + 2 * rcx]              | 4c 2b 2c 48             |
    | sub r14, qword [rax + 4 * rcx]              | 4c 2b 34 88             |
    | sub r15, qword [rax + 8 * rcx]              | 4c 2b 3c c8             |
    | sub rcx, qword [r8 + 2 * r9]                | 4b 2b 0c 48             |
    | sub rdx, qword [r8 + 4 * r9]                | 4b 2b 14 88             |
    | sub rbx, qword [r8 + 8 * r9]                | 4b 2b 1c c8             |
    | sub rsp, qword [1 * rcx]                    | 48 2b 24 0d 00 00 00 00 |
    | sub rbp, qword [2 * rcx]                    | 48 2b 2c 4d 00 00 00 00 |
    | sub rsi, qword [4 * rcx]                    | 48 2b 34 8d 00 00 00 00 |
    | sub rdi, qword [8 * rcx]                    | 48 2b 3c cd 00 00 00 00 |
    | sub r8, qword [1 * r9]                      | 4e 2b 04 0d 00 00 00 00 |
    | sub r9, qword [2 * r9]                      | 4e 2b 0c 4d 00 00 00 00 |
    | sub r10, qword [4 * r9]                     | 4e 2b 14 8d 00 00 00 00 |
    | sub r11, qword [8 * r9]                     | 4e 2b 1c cd 00 00 00 00 |
    | sub r12, qword [r13 + 8 * r12]              | 4f 2b 64 e5 00          |
    | sub r13, qword [rsp + 4 * r15]              | 4e 2b 2c bc             |
    | sub r14, qword [rax + 1 * rcx + 0x00]       | 4c 2b 74 08 00          |
    | sub r15, qword [rax + 1 * rcx - 0x00]       | 4c 2b 7c 08 00          |
    | sub rcx, qword [rax + 1 * rcx - 0x01]       | 48 2b 4c 08 ff          |
    | sub rdx, qword [rax + 1 * rcx + 0x00000001] | 48 2b 94 08 01 00 00 00 |
    | sub rbx, qword [rax + 1 * rcx - 0x00000001] | 48 2b 9c 08 ff ff ff ff |
    | sub rsp, qword [rax + 1 * rcx + 0x7f]       | 48 2b 64 08 7f          |
    | sub rbp, qword [rax + 1 * rcx - 0x7f]       | 48 2b 6c 08 81          |
    | sub rsi, qword [rax + 1 * rcx + 0x80]       | 48 2b b4 08 80 00 00 00 |
    | sub rdi, qword [rax + 1 * rcx - 0x80]       | 48 2b 7c 08 80          |
    | sub r8, qword [rax + 1 * rcx - 0x81]        | 4c 2b 84 08 7f ff ff ff |
    | sub r9, qword [rax + 1 * rcx + 0xff]        | 4c 2b 8c 08 ff 00 00 00 |
    | sub r10, qword [rax + 1 * rcx - 0xff]       | 4c 2b 94 08 01 ff ff ff |
    | sub r11, qword [rax + 1 * rcx + 0x7fffffff] | 4c 2b 9c 08 ff ff ff 7f |
    | sub r12, qword [rax + 1 * rcx - 0x7fffffff] | 4c 2b a4 08 01 00 00 80 |
    | sub r13, qword [rax + 1 * rcx - 0x80000000] | 4c 2b ac 08 00 00 00 80 |
    | sub r14, qword [r10 + 0x7f]                 | 4d 2b 72 7f             |
    | sub r15, qword [r10 + 0x80]                 | 4d 2b ba 80 00 00 00    |
    | sub rcx, qword [r10 - 0x81]                 | 49 2b 8a 7f ff ff ff    |
    | sub rdx, qword [rax]                        | 48 2b 10                |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_sub_reg64_addr64():
    encode(SUB_REG64_ADDR64)


SUB_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sub eax, 0x01  | 83 e8 01    | *** | sub eax, 0x00  | 83 e8 00    |
    | sub ecx, 0x01  | 83 e9 01    | *** | sub eax, 0x7f  | 83 e8 7f    |
    | sub edx, 0x01  | 83 ea 01    | *** | sub eax, 0x80  | 83 e8 80    |
    | sub ebx, 0x01  | 83 eb 01    | *** | sub eax, 0xff  | 83 e8 ff    |
    | sub esp, 0x01  | 83 ec 01    | *** | sub ecx, 0x7f  | 83 e9 7f    |
    | sub ebp, 0x01  | 83 ed 01    | *** | sub edx, 0x80  | 83 ea 80    |
    | sub esi, 0x01  | 83 ee 01    | *** | sub ebx, 0xff  | 83 eb ff    |
    | sub edi, 0x01  | 83 ef 01    | *** | sub esp, 0x00  | 83 ec 00    |
    | sub r8d, 0x01  | 41 83 e8 01 | *** | sub esi, 0x7f  | 83 ee 7f    |
    | sub r9d, 0x01  | 41 83 e9 01 | *** | sub edi, 0x80  | 83 ef 80    |
    | sub r10d, 0x01 | 41 83 ea 01 | *** | sub r8d, 0xff  | 41 83 e8 ff |
    | sub r11d, 0x01 | 41 83 eb 01 | *** | sub r9d, 0x00  | 41 83 e9 00 |
    | sub r12d, 0x01 | 41 83 ec 01 | *** | sub r11d, 0x7f | 41 83 eb 7f |
    | sub r13d, 0x01 | 41 83 ed 01 | *** | sub r12d, 0x80 | 41 83 ec 80 |
    | sub r14d, 0x01 | 41 83 ee 01 | *** | sub r13d, 0xff | 41 83 ed ff |
    | sub r15d, 0x01 | 41 83 ef 01 | *** | sub r14d, 0x00 | 41 83 ee 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sub_reg32_imm8():
    encode(SUB_REG32_IMM8)


SUB_REG32_IMM32 = """
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | instruction          | encoding             | *** | instruction          | encoding             |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | sub eax, 0x00000001  | 2d 01 00 00 00       | *** | sub eax, 0x00007fff  | 2d ff 7f 00 00       |
    | sub ecx, 0x00000001  | 81 e9 01 00 00 00    | *** | sub eax, 0x00008000  | 2d 00 80 00 00       |
    | sub edx, 0x00000001  | 81 ea 01 00 00 00    | *** | sub eax, 0x0000ffff  | 2d ff ff 00 00       |
    | sub ebx, 0x00000001  | 81 eb 01 00 00 00    | *** | sub eax, 0x00010000  | 2d 00 00 01 00       |
    | sub esp, 0x00000001  | 81 ec 01 00 00 00    | *** | sub eax, 0x7fffffff  | 2d ff ff ff 7f       |
    | sub ebp, 0x00000001  | 81 ed 01 00 00 00    | *** | sub eax, 0x80000000  | 2d 00 00 00 80       |
    | sub esi, 0x00000001  | 81 ee 01 00 00 00    | *** | sub eax, 0xffffffff  | 2d ff ff ff ff       |
    | sub edi, 0x00000001  | 81 ef 01 00 00 00    | *** | sub ecx, 0x0000007f  | 81 e9 7f 00 00 00    |
    | sub r8d, 0x00000001  | 41 81 e8 01 00 00 00 | *** | sub edx, 0x00000080  | 81 ea 80 00 00 00    |
    | sub r9d, 0x00000001  | 41 81 e9 01 00 00 00 | *** | sub ebx, 0x000000ff  | 81 eb ff 00 00 00    |
    | sub r10d, 0x00000001 | 41 81 ea 01 00 00 00 | *** | sub esp, 0x00000100  | 81 ec 00 01 00 00    |
    | sub r11d, 0x00000001 | 41 81 eb 01 00 00 00 | *** | sub ebp, 0x00007fff  | 81 ed ff 7f 00 00    |
    | sub r12d, 0x00000001 | 41 81 ec 01 00 00 00 | *** | sub esi, 0x00008000  | 81 ee 00 80 00 00    |
    | sub r13d, 0x00000001 | 41 81 ed 01 00 00 00 | *** | sub edi, 0x0000ffff  | 81 ef ff ff 00 00    |
    | sub r14d, 0x00000001 | 41 81 ee 01 00 00 00 | *** | sub r8d, 0x00010000  | 41 81 e8 00 00 01 00 |
    | sub r15d, 0x00000001 | 41 81 ef 01 00 00 00 | *** | sub r9d, 0x7fffffff  | 41 81 e9 ff ff ff 7f |
    | sub eax, 0x00000000  | 2d 00 00 00 00       | *** | sub r10d, 0x80000000 | 41 81 ea 00 00 00 80 |
    | sub eax, 0x0000007f  | 2d 7f 00 00 00       | *** | sub r11d, 0xffffffff | 41 81 eb ff ff ff ff |
    | sub eax, 0x00000080  | 2d 80 00 00 00       | *** | sub r12d, 0x00000000 | 41 81 ec 00 00 00 00 |
    | sub eax, 0x000000ff  | 2d ff 00 00 00       | *** | sub r14d, 0x0000007f | 41 81 ee 7f 00 00 00 |
    | sub eax, 0x00000100  | 2d 00 01 00 00       | *** | sub r15d, 0x00000080 | 41 81 ef 80 00 00 00 |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
"""


def can_encode_sub_reg32_imm32():
    encode(SUB_REG32_IMM32)


SUB_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | sub eax, ecx   | 29 c8    | *** | sub eax, r8d   | 44 29 c0 |
    | sub ecx, ecx   | 29 c9    | *** | sub eax, r9d   | 44 29 c8 |
    | sub edx, ecx   | 29 ca    | *** | sub eax, r10d  | 44 29 d0 |
    | sub ebx, ecx   | 29 cb    | *** | sub eax, r11d  | 44 29 d8 |
    | sub esp, ecx   | 29 cc    | *** | sub eax, r12d  | 44 29 e0 |
    | sub ebp, ecx   | 29 cd    | *** | sub eax, r13d  | 44 29 e8 |
    | sub esi, ecx   | 29 ce    | *** | sub eax, r14d  | 44 29 f0 |
    | sub edi, ecx   | 29 cf    | *** | sub eax, r15d  | 44 29 f8 |
    | sub r8d, ecx   | 41 29 c8 | *** | sub ecx, edx   | 29 d1    |
    | sub r9d, ecx   | 41 29 c9 | *** | sub edx, ebx   | 29 da    |
    | sub r10d, ecx  | 41 29 ca | *** | sub ebx, esp   | 29 e3    |
    | sub r11d, ecx  | 41 29 cb | *** | sub esp, ebp   | 29 ec    |
    | sub r12d, ecx  | 41 29 cc | *** | sub ebp, esi   | 29 f5    |
    | sub r13d, ecx  | 41 29 cd | *** | sub esi, edi   | 29 fe    |
    | sub r14d, ecx  | 41 29 ce | *** | sub edi, r8d   | 44 29 c7 |
    | sub r15d, ecx  | 41 29 cf | *** | sub r8d, r9d   | 45 29 c8 |
    | sub eax, eax   | 29 c0    | *** | sub r9d, r10d  | 45 29 d1 |
    | sub eax, edx   | 29 d0    | *** | sub r10d, r11d | 45 29 da |
    | sub eax, ebx   | 29 d8    | *** | sub r11d, r12d | 45 29 e3 |
    | sub eax, esp   | 29 e0    | *** | sub r12d, r13d | 45 29 ec |
    | sub eax, ebp   | 29 e8    | *** | sub r13d, r14d | 45 29 f5 |
    | sub eax, esi   | 29 f0    | *** | sub r14d, r15d | 45 29 fe |
    | sub eax, edi   | 29 f8    | *** | sub r15d, eax  | 41 29 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_sub_reg32_reg32():
    encode(SUB_REG32_REG32)


SUB_REG32_ADDR32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | sub eax, dword [rcx]                         | 2b 01                   |
    | sub ecx, dword [rcx]                         | 2b 09                   |
    | sub edx, dword [rcx]                         | 2b 11                   |
    | sub ebx, dword [rcx]                         | 2b 19                   |
    | sub esp, dword [rcx]                         | 2b 21                   |
    | sub ebp, dword [rcx]                         | 2b 29                   |
    | sub esi, dword [rcx]                         | 2b 31                   |
    | sub edi, dword [rcx]                         | 2b 39                   |
    | sub r8d, dword [rcx]                         | 44 2b 01                |
    | sub r9d, dword [rcx]                         | 44 2b 09                |
    | sub r10d, dword [rcx]                        | 44 2b 11                |
    | sub r11d, dword [rcx]                        | 44 2b 19                |
    | sub r12d, dword [rcx]                        | 44 2b 21                |
    | sub r13d, dword [rcx]                        | 44 2b 29                |
    | sub r14d, dword [rcx]                        | 44 2b 31                |
    | sub r15d, dword [rcx]                        | 44 2b 39                |
    | sub eax, dword [rax]                         | 2b 00                   |
    | sub eax, dword [rdx]                         | 2b 02                   |
    | sub eax, dword [rbx]                         | 2b 03                   |
    | sub eax, dword [rsp]                         | 2b 04 24                |
    | sub eax, dword [rbp]                         | 2b 45 00                |
    | sub eax, dword [rsi]                         | 2b 06                   |
    | sub eax, dword [rdi]                         | 2b 07                   |
    | sub eax, dword [r8]                          | 41 2b 00                |
    | sub eax, dword [r9]                          | 41 2b 01                |
    | sub eax, dword [r10]                         | 41 2b 02                |
    | sub eax, dword [r11]                         | 41 2b 03                |
    | sub eax, dword [r12]                         | 41 2b 04 24             |
    | sub eax, dword [r13]                         | 41 2b 45 00             |
    | sub eax, dword [r14]                         | 41 2b 06                |
    | sub eax, dword [r15]                         | 41 2b 07                |
    | sub eax, dword [rax + 1 * rcx]               | 2b 04 08                |
    | sub eax, dword [rcx + 1 * rcx]               | 2b 04 09                |
    | sub eax, dword [rdx + 1 * rcx]               | 2b 04 0a                |
    | sub eax, dword [rbx + 1 * rcx]               | 2b 04 0b                |
    | sub eax, dword [rsp + 1 * rcx]               | 2b 04 0c                |
    | sub eax, dword [rbp + 1 * rcx]               | 2b 44 0d 00             |
    | sub eax, dword [rsi + 1 * rcx]               | 2b 04 0e                |
    | sub eax, dword [rdi + 1 * rcx]               | 2b 04 0f                |
    | sub eax, dword [r8 + 1 * rcx]                | 41 2b 04 08             |
    | sub eax, dword [r9 + 1 * rcx]                | 41 2b 04 09             |
    | sub eax, dword [r10 + 1 * rcx]               | 41 2b 04 0a             |
    | sub eax, dword [r11 + 1 * rcx]               | 41 2b 04 0b             |
    | sub eax, dword [r12 + 1 * rcx]               | 41 2b 04 0c             |
    | sub eax, dword [r13 + 1 * rcx]               | 41 2b 44 0d 00          |
    | sub eax, dword [r14 + 1 * rcx]               | 41 2b 04 0e             |
    | sub eax, dword [r15 + 1 * rcx]               | 41 2b 04 0f             |
    | sub eax, dword [rax + 1 * rax]               | 2b 04 00                |
    | sub eax, dword [rax + 1 * rdx]               | 2b 04 10                |
    | sub eax, dword [rax + 1 * rbx]               | 2b 04 18                |
    | sub eax, dword [rax + 1 * rbp]               | 2b 04 28                |
    | sub eax, dword [rax + 1 * rsi]               | 2b 04 30                |
    | sub eax, dword [rax + 1 * rdi]               | 2b 04 38                |
    | sub eax, dword [rax + 1 * r8]                | 42 2b 04 00             |
    | sub eax, dword [rax + 1 * r9]                | 42 2b 04 08             |
    | sub eax, dword [rax + 1 * r10]               | 42 2b 04 10             |
    | sub eax, dword [rax + 1 * r11]               | 42 2b 04 18             |
    | sub eax, dword [rax + 1 * r12]               | 42 2b 04 20             |
    | sub eax, dword [rax + 1 * r13]               | 42 2b 04 28             |
    | sub eax, dword [rax + 1 * r14]               | 42 2b 04 30             |
    | sub eax, dword [rax + 1 * r15]               | 42 2b 04 38             |
    | sub eax, dword [rax + 2 * rcx]               | 2b 04 48                |
    | sub eax, dword [rax + 4 * rcx]               | 2b 04 88                |
    | sub eax, dword [rax + 8 * rcx]               | 2b 04 c8                |
    | sub eax, dword [r8 + 1 * r9]                 | 43 2b 04 08             |
    | sub eax, dword [r8 + 2 * r9]                 | 43 2b 04 48             |
    | sub eax, dword [r8 + 4 * r9]                 | 43 2b 04 88             |
    | sub eax, dword [r8 + 8 * r9]                 | 43 2b 04 c8             |
    | sub eax, dword [1 * rcx]                     | 2b 04 0d 00 00 00 00    |
    | sub eax, dword [2 * rcx]                     | 2b 04 4d 00 00 00 00    |
    | sub eax, dword [4 * rcx]                     | 2b 04 8d 00 00 00 00    |
    | sub eax, dword [8 * rcx]                     | 2b 04 cd 00 00 00 00    |
    | sub eax, dword [1 * r9]                      | 42 2b 04 0d 00 00 00 00 |
    | sub eax, dword [2 * r9]                      | 42 2b 04 4d 00 00 00 00 |
    | sub eax, dword [4 * r9]                      | 42 2b 04 8d 00 00 00 00 |
    | sub eax, dword [8 * r9]                      | 42 2b 04 cd 00 00 00 00 |
    | sub eax, dword [r13 + 8 * r12]               | 43 2b 44 e5 00          |
    | sub eax, dword [rsp + 4 * r15]               | 42 2b 04 bc             |
    | sub eax, dword [rax + 1 * rcx + 0x00]        | 2b 44 08 00             |
    | sub eax, dword [rax + 1 * rcx - 0x00]        | 2b 44 08 00             |
    | sub eax, dword [rax + 1 * rcx + 0x01]        | 2b 44 08 01             |
    | sub eax, dword [rax + 1 * rcx - 0x01]        | 2b 44 08 ff             |
    | sub eax, dword [rax + 1 * rcx + 0x00000001]  | 2b 84 08 01 00 00 00    |
    | sub eax, dword [rax + 1 * rcx - 0x00000001]  | 2b 84 08 ff ff ff ff    |
    | sub eax, dword [rax + 1 * rcx + 0x7f]        | 2b 44 08 7f             |
    | sub eax, dword [rax + 1 * rcx - 0x7f]        | 2b 44 08 81             |
    | sub eax, dword [rax + 1 * rcx + 0x80]        | 2b 84 08 80 00 00 00    |
    | sub eax, dword [rax + 1 * rcx - 0x80]        | 2b 44 08 80             |
    | sub eax, dword [rax + 1 * rcx - 0x81]        | 2b 84 08 7f ff ff ff    |
    | sub eax, dword [rax + 1 * rcx + 0xff]        | 2b 84 08 ff 00 00 00    |
    | sub eax, dword [rax + 1 * rcx - 0xff]        | 2b 84 08 01 ff ff ff    |
    | sub eax, dword [rax + 1 * rcx + 0x7fffffff]  | 2b 84 08 ff ff ff 7f    |
    | sub eax, dword [rax + 1 * rcx - 0x7fffffff]  | 2b 84 08 01 00 00 80    |
    | sub eax, dword [rax + 1 * rcx - 0x80000000]  | 2b 84 08 00 00 00 80    |
    | sub eax, dword [r10 + 0x7f]                  | 41 2b 42 7f             |
    | sub eax, dword [r10 + 0x80]                  | 41 2b 82 80 00 00 00    |
    | sub eax, dword [r10 - 0x80]                  | 41 2b 42 80             |
    | sub eax, dword [r10 - 0x81]                  | 41 2b 82 7f ff ff ff    |
    | sub ecx, dword [rdx]                         | 2b 0a                   |
    | sub edx, dword [rbx]                         | 2b 13                   |
    | sub ebx, dword [rsp]                         | 2b 1c 24                |
    | sub esp, dword [rbp]                         | 2b 65 00                |
    | sub ebp, dword [rsi]                         | 2b 2e                   |
    | sub esi, dword [rdi]                         | 2b 37                   |
    | sub edi, dword [r8]                          | 41 2b 38                |
    | sub r8d, dword [r9]                          | 45 2b 01                |
    | sub r9d, dword [r10]                         | 45 2b 0a                |
    | sub r10d, dword [r11]                        | 45 2b 13                |
    | sub r11d, dword [r12]                        | 45 2b 1c 24             |
    | sub r12d, dword [r13]                        | 45 2b 65 00             |
    | sub r13d, dword [r14]                        | 45 2b 2e                |
    | sub r14d, dword [r15]                        | 45 2b 37                |
    | sub r15d, dword [rax + 1 * rcx]              | 44 2b 3c 08             |
    | sub ecx, dword [rdx + 1 * rcx]               | 2b 0c 0a                |
    | sub edx, dword [rbx + 1 * rcx]               | 2b 14 0b                |
    | sub ebx, dword [rsp + 1 * rcx]               | 2b 1c 0c                |
    | sub esp, dword [rbp + 1 * rcx]               | 2b 64 0d 00             |
    | sub ebp, dword [rsi + 1 * rcx]               | 2b 2c 0e                |
    | sub esi, dword [rdi + 1 * rcx]               | 2b 34 0f                |
    | sub edi, dword [r8 + 1 * rcx]                | 41 2b 3c 08             |
    | sub r8d, dword [r9 + 1 * rcx]                | 45 2b 04 09             |
    | sub r9d, dword [r10 + 1 * rcx]               | 45 2b 0c 0a             |
    | sub r10d, dword [r11 + 1 * rcx]              | 45 2b 14 0b             |
    | sub r11d, dword [r12 + 1 * rcx]              | 45 2b 1c 0c             |
    | sub r12d, dword [r13 + 1 * rcx]              | 45 2b 64 0d 00          |
    | sub r13d, dword [r14 + 1 * rcx]              | 45 2b 2c 0e             |
    | sub r14d, dword [r15 + 1 * rcx]              | 45 2b 34 0f             |
    | sub r15d, dword [rax + 1 * rax]              | 44 2b 3c 00             |
    | sub ecx, dword [rax + 1 * rbx]               | 2b 0c 18                |
    | sub edx, dword [rax + 1 * rbp]               | 2b 14 28                |
    | sub ebx, dword [rax + 1 * rsi]               | 2b 1c 30                |
    | sub esp, dword [rax + 1 * rdi]               | 2b 24 38                |
    | sub ebp, dword [rax + 1 * r8]                | 42 2b 2c 00             |
    | sub esi, dword [rax + 1 * r9]                | 42 2b 34 08             |
    | sub edi, dword [rax + 1 * r10]               | 42 2b 3c 10             |
    | sub r8d, dword [rax + 1 * r11]               | 46 2b 04 18             |
    | sub r9d, dword [rax + 1 * r12]               | 46 2b 0c 20             |
    | sub r10d, dword [rax + 1 * r13]              | 46 2b 14 28             |
    | sub r11d, dword [rax + 1 * r14]              | 46 2b 1c 30             |
    | sub r12d, dword [rax + 1 * r15]              | 46 2b 24 38             |
    | sub r13d, dword [rax + 2 * rcx]              | 44 2b 2c 48             |
    | sub r14d, dword [rax + 4 * rcx]              | 44 2b 34 88             |
    | sub r15d, dword [rax + 8 * rcx]              | 44 2b 3c c8             |
    | sub ecx, dword [r8 + 2 * r9]                 | 43 2b 0c 48             |
    | sub edx, dword [r8 + 4 * r9]                 | 43 2b 14 88             |
    | sub ebx, dword [r8 + 8 * r9]                 | 43 2b 1c c8             |
    | sub esp, dword [1 * rcx]                     | 2b 24 0d 00 00 00 00    |
    | sub ebp, dword [2 * rcx]                     | 2b 2c 4d 00 00 00 00    |
    | sub esi, dword [4 * rcx]                     | 2b 34 8d 00 00 00 00    |
    | sub edi, dword [8 * rcx]                     | 2b 3c cd 00 00 00 00    |
    | sub r8d, dword [1 * r9]                      | 46 2b 04 0d 00 00 00 00 |
    | sub r9d, dword [2 * r9]                      | 46 2b 0c 4d 00 00 00 00 |
    | sub r10d, dword [4 * r9]                     | 46 2b 14 8d 00 00 00 00 |
    | sub r11d, dword [8 * r9]                     | 46 2b 1c cd 00 00 00 00 |
    | sub r12d, dword [r13 + 8 * r12]              | 47 2b 64 e5 00          |
    | sub r13d, dword [rsp + 4 * r15]              | 46 2b 2c bc             |
    | sub r14d, dword [rax + 1 * rcx + 0x00]       | 44 2b 74 08 00          |
    | sub r15d, dword [rax + 1 * rcx - 0x00]       | 44 2b 7c 08 00          |
    | sub ecx, dword [rax + 1 * rcx - 0x01]        | 2b 4c 08 ff             |
    | sub edx, dword [rax + 1 * rcx + 0x00000001]  | 2b 94 08 01 00 00 00    |
    | sub ebx, dword [rax + 1 * rcx - 0x00000001]  | 2b 9c 08 ff ff ff ff    |
    | sub esp, dword [rax + 1 * rcx + 0x7f]        | 2b 64 08 7f             |
    | sub ebp, dword [rax + 1 * rcx - 0x7f]        | 2b 6c 08 81             |
    | sub esi, dword [rax + 1 * rcx + 0x80]        | 2b b4 08 80 00 00 00    |
    | sub edi, dword [rax + 1 * rcx - 0x80]        | 2b 7c 08 80             |
    | sub r8d, dword [rax + 1 * rcx - 0x81]        | 44 2b 84 08 7f ff ff ff |
    | sub r9d, dword [rax + 1 * rcx + 0xff]        | 44 2b 8c 08 ff 00 00 00 |
    | sub r10d, dword [rax + 1 * rcx - 0xff]       | 44 2b 94 08 01 ff ff ff |
    | sub r11d, dword [rax + 1 * rcx + 0x7fffffff] | 44 2b 9c 08 ff ff ff 7f |
    | sub r12d, dword [rax + 1 * rcx - 0x7fffffff] | 44 2b a4 08 01 00 00 80 |
    | sub r13d, dword [rax + 1 * rcx - 0x80000000] | 44 2b ac 08 00 00 00 80 |
    | sub r14d, dword [r10 + 0x7f]                 | 45 2b 72 7f             |
    | sub r15d, dword [r10 + 0x80]                 | 45 2b ba 80 00 00 00    |
    | sub ecx, dword [r10 - 0x81]                  | 41 2b 8a 7f ff ff ff    |
    | sub edx, dword [rax]                         | 2b 10                   |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_sub_reg32_addr32():
    encode(SUB_REG32_ADDR32)


SUB_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | sub ax, 0x01   | 66 83 e8 01    | *** | sub ax, 0x00   | 66 83 e8 00    |
    | sub cx, 0x01   | 66 83 e9 01    | *** | sub ax, 0x7f   | 66 83 e8 7f    |
    | sub dx, 0x01   | 66 83 ea 01    | *** | sub ax, 0x80   | 66 83 e8 80    |
    | sub bx, 0x01   | 66 83 eb 01    | *** | sub ax, 0xff   | 66 83 e8 ff    |
    | sub sp, 0x01   | 66 83 ec 01    | *** | sub cx, 0x7f   | 66 83 e9 7f    |
    | sub bp, 0x01   | 66 83 ed 01    | *** | sub dx, 0x80   | 66 83 ea 80    |
    | sub si, 0x01   | 66 83 ee 01    | *** | sub bx, 0xff   | 66 83 eb ff    |
    | sub di, 0x01   | 66 83 ef 01    | *** | sub sp, 0x00   | 66 83 ec 00    |
    | sub r8w, 0x01  | 66 41 83 e8 01 | *** | sub si, 0x7f   | 66 83 ee 7f    |
    | sub r9w, 0x01  | 66 41 83 e9 01 | *** | sub di, 0x80   | 66 83 ef 80    |
    | sub r10w, 0x01 | 66 41 83 ea 01 | *** | sub r8w, 0xff  | 66 41 83 e8 ff |
    | sub r11w, 0x01 | 66 41 83 eb 01 | *** | sub r9w, 0x00  | 66 41 83 e9 00 |
    | sub r12w, 0x01 | 66 41 83 ec 01 | *** | sub r11w, 0x7f | 66 41 83 eb 7f |
    | sub r13w, 0x01 | 66 41 83 ed 01 | *** | sub r12w, 0x80 | 66 41 83 ec 80 |
    | sub r14w, 0x01 | 66 41 83 ee 01 | *** | sub r13w, 0xff | 66 41 83 ed ff |
    | sub r15w, 0x01 | 66 41 83 ef 01 | *** | sub r14w, 0x00 | 66 41 83 ee 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_sub_reg16_imm8():
    encode(SUB_REG16_IMM8)


SUB_REG16_IMM16 = """
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | instruction      | encoding          | *** | instruction      | encoding          |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | sub ax, 0x0001   | 66 2d 01 00       | *** | sub ax, 0x00ff   | 66 2d ff 00       |
    | sub cx, 0x0001   | 66 81 e9 01 00    | *** | sub ax, 0x0100   | 66 2d 00 01       |
    | sub dx, 0x0001   | 66 81 ea 01 00    | *** | sub ax, 0x7fff   | 66 2d ff 7f       |
    | sub bx, 0x0001   | 66 81 eb 01 00    | *** | sub ax, 0x8000   | 66 2d 00 80       |
    | sub sp, 0x0001   | 66 81 ec 01 00    | *** | sub ax, 0xffff   | 66 2d ff ff       |
    | sub bp, 0x0001   | 66 81 ed 01 00    | *** | sub cx, 0x007f   | 66 81 e9 7f 00    |
    | sub si, 0x0001   | 66 81 ee 01 00    | *** | sub dx, 0x0080   | 66 81 ea 80 00    |
    | sub di, 0x0001   | 66 81 ef 01 00    | *** | sub bx, 0x00ff   | 66 81 eb ff 00    |
    | sub r8w, 0x0001  | 66 41 81 e8 01 00 | *** | sub sp, 0x0100   | 66 81 ec 00 01    |
    | sub r9w, 0x0001  | 66 41 81 e9 01 00 | *** | sub bp, 0x7fff   | 66 81 ed ff 7f    |
    | sub r10w, 0x0001 | 66 41 81 ea 01 00 | *** | sub si, 0x8000   | 66 81 ee 00 80    |
    | sub r11w, 0x0001 | 66 41 81 eb 01 00 | *** | sub di, 0xffff   | 66 81 ef ff ff    |
    | sub r12w, 0x0001 | 66 41 81 ec 01 00 | *** | sub r8w, 0x0000  | 66 41 81 e8 00 00 |
    | sub r13w, 0x0001 | 66 41 81 ed 01 00 | *** | sub r10w, 0x007f | 66 41 81 ea 7f 00 |
    | sub r14w, 0x0001 | 66 41 81 ee 01 00 | *** | sub r11w, 0x0080 | 66 41 81 eb 80 00 |
    | sub r15w, 0x0001 | 66 41 81 ef 01 00 | *** | sub r12w, 0x00ff | 66 41 81 ec ff 00 |
    | sub ax, 0x0000   | 66 2d 00 00       | *** | sub r13w, 0x0100 | 66 41 81 ed 00 01 |
    | sub ax, 0x007f   | 66 2d 7f 00       | *** | sub r14w, 0x7fff | 66 41 81 ee ff 7f |
    | sub ax, 0x0080   | 66 2d 80 00       | *** | sub r15w, 0x8000 | 66 41 81 ef 00 80 |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
"""


def can_encode_sub_reg16_imm16():
    encode(SUB_REG16_IMM16)


SUB_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sub ax, cx     | 66 29 c8    | *** | sub ax, r8w    | 66 44 29 c0 |
    | sub cx, cx     | 66 29 c9    | *** | sub ax, r9w    | 66 44 29 c8 |
    | sub dx, cx     | 66 29 ca    | *** | sub ax, r10w   | 66 44 29 d0 |
    | sub bx, cx     | 66 29 cb    | *** | sub ax, r11w   | 66 44 29 d8 |
    | sub sp, cx     | 66 29 cc    | *** | sub ax, r12w   | 66 44 29 e0 |
    | sub bp, cx     | 66 29 cd    | *** | sub ax, r13w   | 66 44 29 e8 |
    | sub si, cx     | 66 29 ce    | *** | sub ax, r14w   | 66 44 29 f0 |
    | sub di, cx     | 66 29 cf    | *** | sub ax, r15w   | 66 44 29 f8 |
    | sub r8w, cx    | 66 41 29 c8 | *** | sub cx, dx     | 66 29 d1    |
    | sub r9w, cx    | 66 41 29 c9 | *** | sub dx, bx     | 66 29 da    |
    | sub r10w, cx   | 66 41 29 ca | *** | sub bx, sp     | 66 29 e3    |
    | sub r11w, cx   | 66 41 29 cb | *** | sub sp, bp     | 66 29 ec    |
    | sub r12w, cx   | 66 41 29 cc | *** | sub bp, si     | 66 29 f5    |
    | sub r13w, cx   | 66 41 29 cd | *** | sub si, di     | 66 29 fe    |
    | sub r14w, cx   | 66 41 29 ce | *** | sub di, r8w    | 66 44 29 c7 |
    | sub r15w, cx   | 66 41 29 cf | *** | sub r8w, r9w   | 66 45 29 c8 |
    | sub ax, ax     | 66 29 c0    | *** | sub r9w, r10w  | 66 45 29 d1 |
    | sub ax, dx     | 66 29 d0    | *** | sub r10w, r11w | 66 45 29 da |
    | sub ax, bx     | 66 29 d8    | *** | sub r11w, r12w | 66 45 29 e3 |
    | sub ax, sp     | 66 29 e0    | *** | sub r12w, r13w | 66 45 29 ec |
    | sub ax, bp     | 66 29 e8    | *** | sub r13w, r14w | 66 45 29 f5 |
    | sub ax, si     | 66 29 f0    | *** | sub r14w, r15w | 66 45 29 fe |
    | sub ax, di     | 66 29 f8    | *** | sub r15w, ax   | 66 41 29 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sub_reg16_reg16():
    encode(SUB_REG16_REG16)


SUB_REG16_ADDR16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sub ax, word [rcx]                          | 66 2b 01                   |
    | sub cx, word [rcx]                          | 66 2b 09                   |
    | sub dx, word [rcx]                          | 66 2b 11                   |
    | sub bx, word [rcx]                          | 66 2b 19                   |
    | sub sp, word [rcx]                          | 66 2b 21                   |
    | sub bp, word [rcx]                          | 66 2b 29                   |
    | sub si, word [rcx]                          | 66 2b 31                   |
    | sub di, word [rcx]                          | 66 2b 39                   |
    | sub r8w, word [rcx]                         | 66 44 2b 01                |
    | sub r9w, word [rcx]                         | 66 44 2b 09                |
    | sub r10w, word [rcx]                        | 66 44 2b 11                |
    | sub r11w, word [rcx]                        | 66 44 2b 19                |
    | sub r12w, word [rcx]                        | 66 44 2b 21                |
    | sub r13w, word [rcx]                        | 66 44 2b 29                |
    | sub r14w, word [rcx]                        | 66 44 2b 31                |
    | sub r15w, word [rcx]                        | 66 44 2b 39                |
    | sub ax, word [rax]                          | 66 2b 00                   |
    | sub ax, word [rdx]                          | 66 2b 02                   |
    | sub ax, word [rbx]                          | 66 2b 03                   |
    | sub ax, word [rsp]                          | 66 2b 04 24                |
    | sub ax, word [rbp]                          | 66 2b 45 00                |
    | sub ax, word [rsi]                          | 66 2b 06                   |
    | sub ax, word [rdi]                          | 66 2b 07                   |
    | sub ax, word [r8]                           | 66 41 2b 00                |
    | sub ax, word [r9]                           | 66 41 2b 01                |
    | sub ax, word [r10]                          | 66 41 2b 02                |
    | sub ax, word [r11]                          | 66 41 2b 03                |
    | sub ax, word [r12]                          | 66 41 2b 04 24             |
    | sub ax, word [r13]                          | 66 41 2b 45 00             |
    | sub ax, word [r14]                          | 66 41 2b 06                |
    | sub ax, word [r15]                          | 66 41 2b 07                |
    | sub ax, word [rax + 1 * rcx]                | 66 2b 04 08                |
    | sub ax, word [rcx + 1 * rcx]                | 66 2b 04 09                |
    | sub ax, word [rdx + 1 * rcx]                | 66 2b 04 0a                |
    | sub ax, word [rbx + 1 * rcx]                | 66 2b 04 0b                |
    | sub ax, word [rsp + 1 * rcx]                | 66 2b 04 0c                |
    | sub ax, word [rbp + 1 * rcx]                | 66 2b 44 0d 00             |
    | sub ax, word [rsi + 1 * rcx]                | 66 2b 04 0e                |
    | sub ax, word [rdi + 1 * rcx]                | 66 2b 04 0f                |
    | sub ax, word [r8 + 1 * rcx]                 | 66 41 2b 04 08             |
    | sub ax, word [r9 + 1 * rcx]                 | 66 41 2b 04 09             |
    | sub ax, word [r10 + 1 * rcx]                | 66 41 2b 04 0a             |
    | sub ax, word [r11 + 1 * rcx]                | 66 41 2b 04 0b             |
    | sub ax, word [r12 + 1 * rcx]                | 66 41 2b 04 0c             |
    | sub ax, word [r13 + 1 * rcx]                | 66 41 2b 44 0d 00          |
    | sub ax, word [r14 + 1 * rcx]                | 66 41 2b 04 0e             |
    | sub ax, word [r15 + 1 * rcx]                | 66 41 2b 04 0f             |
    | sub ax, word [rax + 1 * rax]                | 66 2b 04 00                |
    | sub ax, word [rax + 1 * rdx]                | 66 2b 04 10                |
    | sub ax, word [rax + 1 * rbx]                | 66 2b 04 18                |
    | sub ax, word [rax + 1 * rbp]                | 66 2b 04 28                |
    | sub ax, word [rax + 1 * rsi]                | 66 2b 04 30                |
    | sub ax, word [rax + 1 * rdi]                | 66 2b 04 38                |
    | sub ax, word [rax + 1 * r8]                 | 66 42 2b 04 00             |
    | sub ax, word [rax + 1 * r9]                 | 66 42 2b 04 08             |
    | sub ax, word [rax + 1 * r10]                | 66 42 2b 04 10             |
    | sub ax, word [rax + 1 * r11]                | 66 42 2b 04 18             |
    | sub ax, word [rax + 1 * r12]                | 66 42 2b 04 20             |
    | sub ax, word [rax + 1 * r13]                | 66 42 2b 04 28             |
    | sub ax, word [rax + 1 * r14]                | 66 42 2b 04 30             |
    | sub ax, word [rax + 1 * r15]                | 66 42 2b 04 38             |
    | sub ax, word [rax + 2 * rcx]                | 66 2b 04 48                |
    | sub ax, word [rax + 4 * rcx]                | 66 2b 04 88                |
    | sub ax, word [rax + 8 * rcx]                | 66 2b 04 c8                |
    | sub ax, word [r8 + 1 * r9]                  | 66 43 2b 04 08             |
    | sub ax, word [r8 + 2 * r9]                  | 66 43 2b 04 48             |
    | sub ax, word [r8 + 4 * r9]                  | 66 43 2b 04 88             |
    | sub ax, word [r8 + 8 * r9]                  | 66 43 2b 04 c8             |
    | sub ax, word [1 * rcx]                      | 66 2b 04 0d 00 00 00 00    |
    | sub ax, word [2 * rcx]                      | 66 2b 04 4d 00 00 00 00    |
    | sub ax, word [4 * rcx]                      | 66 2b 04 8d 00 00 00 00    |
    | sub ax, word [8 * rcx]                      | 66 2b 04 cd 00 00 00 00    |
    | sub ax, word [1 * r9]                       | 66 42 2b 04 0d 00 00 00 00 |
    | sub ax, word [2 * r9]                       | 66 42 2b 04 4d 00 00 00 00 |
    | sub ax, word [4 * r9]                       | 66 42 2b 04 8d 00 00 00 00 |
    | sub ax, word [8 * r9]                       | 66 42 2b 04 cd 00 00 00 00 |
    | sub ax, word [r13 + 8 * r12]                | 66 43 2b 44 e5 00          |
    | sub ax, word [rsp + 4 * r15]                | 66 42 2b 04 bc             |
    | sub ax, word [rax + 1 * rcx + 0x00]         | 66 2b 44 08 00             |
    | sub ax, word [rax + 1 * rcx - 0x00]         | 66 2b 44 08 00             |
    | sub ax, word [rax + 1 * rcx + 0x01]         | 66 2b 44 08 01             |
    | sub ax, word [rax + 1 * rcx - 0x01]         | 66 2b 44 08 ff             |
    | sub ax, word [rax + 1 * rcx + 0x00000001]   | 66 2b 84 08 01 00 00 00    |
    | sub ax, word [rax + 1 * rcx - 0x00000001]   | 66 2b 84 08 ff ff ff ff    |
    | sub ax, word [rax + 1 * rcx + 0x7f]         | 66 2b 44 08 7f             |
    | sub ax, word [rax + 1 * rcx - 0x7f]         | 66 2b 44 08 81             |
    | sub ax, word [rax + 1 * rcx + 0x80]         | 66 2b 84 08 80 00 00 00    |
    | sub ax, word [rax + 1 * rcx - 0x80]         | 66 2b 44 08 80             |
    | sub ax, word [rax + 1 * rcx - 0x81]         | 66 2b 84 08 7f ff ff ff    |
    | sub ax, word [rax + 1 * rcx + 0xff]         | 66 2b 84 08 ff 00 00 00    |
    | sub ax, word [rax + 1 * rcx - 0xff]         | 66 2b 84 08 01 ff ff ff    |
    | sub ax, word [rax + 1 * rcx + 0x7fffffff]   | 66 2b 84 08 ff ff ff 7f    |
    | sub ax, word [rax + 1 * rcx - 0x7fffffff]   | 66 2b 84 08 01 00 00 80    |
    | sub ax, word [rax + 1 * rcx - 0x80000000]   | 66 2b 84 08 00 00 00 80    |
    | sub ax, word [r10 + 0x7f]                   | 66 41 2b 42 7f             |
    | sub ax, word [r10 + 0x80]                   | 66 41 2b 82 80 00 00 00    |
    | sub ax, word [r10 - 0x80]                   | 66 41 2b 42 80             |
    | sub ax, word [r10 - 0x81]                   | 66 41 2b 82 7f ff ff ff    |
    | sub cx, word [rdx]                          | 66 2b 0a                   |
    | sub dx, word [rbx]                          | 66 2b 13                   |
    | sub bx, word [rsp]                          | 66 2b 1c 24                |
    | sub sp, word [rbp]                          | 66 2b 65 00                |
    | sub bp, word [rsi]                          | 66 2b 2e                   |
    | sub si, word [rdi]                          | 66 2b 37                   |
    | sub di, word [r8]                           | 66 41 2b 38                |
    | sub r8w, word [r9]                          | 66 45 2b 01                |
    | sub r9w, word [r10]                         | 66 45 2b 0a                |
    | sub r10w, word [r11]                        | 66 45 2b 13                |
    | sub r11w, word [r12]                        | 66 45 2b 1c 24             |
    | sub r12w, word [r13]                        | 66 45 2b 65 00             |
    | sub r13w, word [r14]                        | 66 45 2b 2e                |
    | sub r14w, word [r15]                        | 66 45 2b 37                |
    | sub r15w, word [rax + 1 * rcx]              | 66 44 2b 3c 08             |
    | sub cx, word [rdx + 1 * rcx]                | 66 2b 0c 0a                |
    | sub dx, word [rbx + 1 * rcx]                | 66 2b 14 0b                |
    | sub bx, word [rsp + 1 * rcx]                | 66 2b 1c 0c                |
    | sub sp, word [rbp + 1 * rcx]                | 66 2b 64 0d 00             |
    | sub bp, word [rsi + 1 * rcx]                | 66 2b 2c 0e                |
    | sub si, word [rdi + 1 * rcx]                | 66 2b 34 0f                |
    | sub di, word [r8 + 1 * rcx]                 | 66 41 2b 3c 08             |
    | sub r8w, word [r9 + 1 * rcx]                | 66 45 2b 04 09             |
    | sub r9w, word [r10 + 1 * rcx]               | 66 45 2b 0c 0a             |
    | sub r10w, word [r11 + 1 * rcx]              | 66 45 2b 14 0b             |
    | sub r11w, word [r12 + 1 * rcx]              | 66 45 2b 1c 0c             |
    | sub r12w, word [r13 + 1 * rcx]              | 66 45 2b 64 0d 00          |
    | sub r13w, word [r14 + 1 * rcx]              | 66 45 2b 2c 0e             |
    | sub r14w, word [r15 + 1 * rcx]              | 66 45 2b 34 0f             |
    | sub r15w, word [rax + 1 * rax]              | 66 44 2b 3c 00             |
    | sub cx, word [rax + 1 * rbx]                | 66 2b 0c 18                |
    | sub dx, word [rax + 1 * rbp]                | 66 2b 14 28                |
    | sub bx, word [rax + 1 * rsi]                | 66 2b 1c 30                |
    | sub sp, word [rax + 1 * rdi]                | 66 2b 24 38                |
    | sub bp, word [rax + 1 * r8]                 | 66 42 2b 2c 00             |
    | sub si, word [rax + 1 * r9]                 | 66 42 2b 34 08             |
    | sub di, word [rax + 1 * r10]                | 66 42 2b 3c 10             |
    | sub r8w, word [rax + 1 * r11]               | 66 46 2b 04 18             |
    | sub r9w, word [rax + 1 * r12]               | 66 46 2b 0c 20             |
    | sub r10w, word [rax + 1 * r13]              | 66 46 2b 14 28             |
    | sub r11w, word [rax + 1 * r14]              | 66 46 2b 1c 30             |
    | sub r12w, word [rax + 1 * r15]              | 66 46 2b 24 38             |
    | sub r13w, word [rax + 2 * rcx]              | 66 44 2b 2c 48             |
    | sub r14w, word [rax + 4 * rcx]              | 66 44 2b 34 88             |
    | sub r15w, word [rax + 8 * rcx]              | 66 44 2b 3c c8             |
    | sub cx, word [r8 + 2 * r9]                  | 66 43 2b 0c 48             |
    | sub dx, word [r8 + 4 * r9]                  | 66 43 2b 14 88             |
    | sub bx, word [r8 + 8 * r9]                  | 66 43 2b 1c c8             |
    | sub sp, word [1 * rcx]                      | 66 2b 24 0d 00 00 00 00    |
    | sub bp, word [2 * rcx]                      | 66 2b 2c 4d 00 00 00 00    |
    | sub si, word [4 * rcx]                      | 66 2b 34 8d 00 00 00 00    |
    | sub di, word [8 * rcx]                      | 66 2b 3c cd 00 00 00 00    |
    | sub r8w, word [1 * r9]                      | 66 46 2b 04 0d 00 00 00 00 |
    | sub r9w, word [2 * r9]                      | 66 46 2b 0c 4d 00 00 00 00 |
    | sub r10w, word [4 * r9]                     | 66 46 2b 14 8d 00 00 00 00 |
    | sub r11w, word [8 * r9]                     | 66 46 2b 1c cd 00 00 00 00 |
    | sub r12w, word [r13 + 8 * r12]              | 66 47 2b 64 e5 00          |
    | sub r13w, word [rsp + 4 * r15]              | 66 46 2b 2c bc             |
    | sub r14w, word [rax + 1 * rcx + 0x00]       | 66 44 2b 74 08 00          |
    | sub r15w, word [rax + 1 * rcx - 0x00]       | 66 44 2b 7c 08 00          |
    | sub cx, word [rax + 1 * rcx - 0x01]         | 66 2b 4c 08 ff             |
    | sub dx, word [rax + 1 * rcx + 0x00000001]   | 66 2b 94 08 01 00 00 00    |
    | sub bx, word [rax + 1 * rcx - 0x00000001]   | 66 2b 9c 08 ff ff ff ff    |
    | sub sp, word [rax + 1 * rcx + 0x7f]         | 66 2b 64 08 7f             |
    | sub bp, word [rax + 1 * rcx - 0x7f]         | 66 2b 6c 08 81             |
    | sub si, word [rax + 1 * rcx + 0x80]         | 66 2b b4 08 80 00 00 00    |
    | sub di, word [rax + 1 * rcx - 0x80]         | 66 2b 7c 08 80             |
    | sub r8w, word [rax + 1 * rcx - 0x81]        | 66 44 2b 84 08 7f ff ff ff |
    | sub r9w, word [rax + 1 * rcx + 0xff]        | 66 44 2b 8c 08 ff 00 00 00 |
    | sub r10w, word [rax + 1 * rcx - 0xff]       | 66 44 2b 94 08 01 ff ff ff |
    | sub r11w, word [rax + 1 * rcx + 0x7fffffff] | 66 44 2b 9c 08 ff ff ff 7f |
    | sub r12w, word [rax + 1 * rcx - 0x7fffffff] | 66 44 2b a4 08 01 00 00 80 |
    | sub r13w, word [rax + 1 * rcx - 0x80000000] | 66 44 2b ac 08 00 00 00 80 |
    | sub r14w, word [r10 + 0x7f]                 | 66 45 2b 72 7f             |
    | sub r15w, word [r10 + 0x80]                 | 66 45 2b ba 80 00 00 00    |
    | sub cx, word [r10 - 0x81]                   | 66 41 2b 8a 7f ff ff ff    |
    | sub dx, word [rax]                          | 66 2b 10                   |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sub_reg16_addr16():
    encode(SUB_REG16_ADDR16)


SUB_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sub al, 0x01   | 2c 01       | *** | sub al, 0x00   | 2c 00       |
    | sub cl, 0x01   | 80 e9 01    | *** | sub al, 0x7f   | 2c 7f       |
    | sub dl, 0x01   | 80 ea 01    | *** | sub al, 0x80   | 2c 80       |
    | sub bl, 0x01   | 80 eb 01    | *** | sub al, 0xff   | 2c ff       |
    | sub spl, 0x01  | 40 80 ec 01 | *** | sub cl, 0x7f   | 80 e9 7f    |
    | sub bpl, 0x01  | 40 80 ed 01 | *** | sub dl, 0x80   | 80 ea 80    |
    | sub sil, 0x01  | 40 80 ee 01 | *** | sub bl, 0xff   | 80 eb ff    |
    | sub dil, 0x01  | 40 80 ef 01 | *** | sub spl, 0x00  | 40 80 ec 00 |
    | sub r8b, 0x01  | 41 80 e8 01 | *** | sub sil, 0x7f  | 40 80 ee 7f |
    | sub r9b, 0x01  | 41 80 e9 01 | *** | sub dil, 0x80  | 40 80 ef 80 |
    | sub r10b, 0x01 | 41 80 ea 01 | *** | sub r8b, 0xff  | 41 80 e8 ff |
    | sub r11b, 0x01 | 41 80 eb 01 | *** | sub r9b, 0x00  | 41 80 e9 00 |
    | sub r12b, 0x01 | 41 80 ec 01 | *** | sub r11b, 0x7f | 41 80 eb 7f |
    | sub r13b, 0x01 | 41 80 ed 01 | *** | sub r12b, 0x80 | 41 80 ec 80 |
    | sub r14b, 0x01 | 41 80 ee 01 | *** | sub r13b, 0xff | 41 80 ed ff |
    | sub r15b, 0x01 | 41 80 ef 01 | *** | sub r14b, 0x00 | 41 80 ee 00 |
    | sub ah, 0x01   | 80 ec 01    | *** | sub ah, 0x7f   | 80 ec 7f    |
    | sub ch, 0x01   | 80 ed 01    | *** | sub ch, 0x80   | 80 ed 80    |
    | sub dh, 0x01   | 80 ee 01    | *** | sub dh, 0xff   | 80 ee ff    |
    | sub bh, 0x01   | 80 ef 01    | *** | sub bh, 0x00   | 80 ef 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sub_reg8_imm8():
    encode(SUB_REG8_IMM8)


SUB_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | sub al, cl     | 28 c8    | *** | sub al, r10b   | 44 28 d0 |
    | sub cl, cl     | 28 c9    | *** | sub al, r11b   | 44 28 d8 |
    | sub dl, cl     | 28 ca    | *** | sub al, r12b   | 44 28 e0 |
    | sub bl, cl     | 28 cb    | *** | sub al, r13b   | 44 28 e8 |
    | sub spl, cl    | 40 28 cc | *** | sub al, r14b   | 44 28 f0 |
    | sub bpl, cl    | 40 28 cd | *** | sub al, r15b   | 44 28 f8 |
    | sub sil, cl    | 40 28 ce | *** | sub al, ah     | 28 e0    |
    | sub dil, cl    | 40 28 cf | *** | sub al, ch     | 28 e8    |
    | sub r8b, cl    | 41 28 c8 | *** | sub al, dh     | 28 f0    |
    | sub r9b, cl    | 41 28 c9 | *** | sub al, bh     | 28 f8    |
    | sub r10b, cl   | 41 28 ca | *** | sub cl, dl     | 28 d1    |
    | sub r11b, cl   | 41 28 cb | *** | sub dl, bl     | 28 da    |
    | sub r12b, cl   | 41 28 cc | *** | sub bl, spl    | 40 28 e3 |
    | sub r13b, cl   | 41 28 cd | *** | sub spl, bpl   | 40 28 ec |
    | sub r14b, cl   | 41 28 ce | *** | sub bpl, sil   | 40 28 f5 |
    | sub r15b, cl   | 41 28 cf | *** | sub sil, dil   | 40 28 fe |
    | sub ah, cl     | 28 cc    | *** | sub dil, r8b   | 44 28 c7 |
    | sub ch, cl     | 28 cd    | *** | sub r8b, r9b   | 45 28 c8 |
    | sub dh, cl     | 28 ce    | *** | sub r9b, r10b  | 45 28 d1 |
    | sub bh, cl     | 28 cf    | *** | sub r10b, r11b | 45 28 da |
    | sub al, al     | 28 c0    | *** | sub r11b, r12b | 45 28 e3 |
    | sub al, dl     | 28 d0    | *** | sub r12b, r13b | 45 28 ec |
    | sub al, bl     | 28 d8    | *** | sub r13b, r14b | 45 28 f5 |
    | sub al, spl    | 40 28 e0 | *** | sub r14b, r15b | 45 28 fe |
    | sub al, bpl    | 40 28 e8 | *** | sub r15b, ah   | !! !! !! |
    | sub al, sil    | 40 28 f0 | *** | sub ah, ch     | 28 ec    |
    | sub al, dil    | 40 28 f8 | *** | sub ch, dh     | 28 f5    |
    | sub al, r8b    | 44 28 c0 | *** | sub dh, bh     | 28 fe    |
    | sub al, r9b    | 44 28 c8 | *** | sub bh, al     | 28 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_sub_reg8_reg8():
    encode(SUB_REG8_REG8)


SUB_REG8_ADDR8 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | sub al, byte [rcx]                          | 2a 01                   |
    | sub cl, byte [rcx]                          | 2a 09                   |
    | sub dl, byte [rcx]                          | 2a 11                   |
    | sub bl, byte [rcx]                          | 2a 19                   |
    | sub spl, byte [rcx]                         | 40 2a 21                |
    | sub bpl, byte [rcx]                         | 40 2a 29                |
    | sub sil, byte [rcx]                         | 40 2a 31                |
    | sub dil, byte [rcx]                         | 40 2a 39                |
    | sub r8b, byte [rcx]                         | 44 2a 01                |
    | sub r9b, byte [rcx]                         | 44 2a 09                |
    | sub r10b, byte [rcx]                        | 44 2a 11                |
    | sub r11b, byte [rcx]                        | 44 2a 19                |
    | sub r12b, byte [rcx]                        | 44 2a 21                |
    | sub r13b, byte [rcx]                        | 44 2a 29                |
    | sub r14b, byte [rcx]                        | 44 2a 31                |
    | sub r15b, byte [rcx]                        | 44 2a 39                |
    | sub ah, byte [rcx]                          | 2a 21                   |
    | sub ch, byte [rcx]                          | 2a 29                   |
    | sub dh, byte [rcx]                          | 2a 31                   |
    | sub bh, byte [rcx]                          | 2a 39                   |
    | sub al, byte [rax]                          | 2a 00                   |
    | sub al, byte [rdx]                          | 2a 02                   |
    | sub al, byte [rbx]                          | 2a 03                   |
    | sub al, byte [rsp]                          | 2a 04 24                |
    | sub al, byte [rbp]                          | 2a 45 00                |
    | sub al, byte [rsi]                          | 2a 06                   |
    | sub al, byte [rdi]                          | 2a 07                   |
    | sub al, byte [r8]                           | 41 2a 00                |
    | sub al, byte [r9]                           | 41 2a 01                |
    | sub al, byte [r10]                          | 41 2a 02                |
    | sub al, byte [r11]                          | 41 2a 03                |
    | sub al, byte [r12]                          | 41 2a 04 24             |
    | sub al, byte [r13]                          | 41 2a 45 00             |
    | sub al, byte [r14]                          | 41 2a 06                |
    | sub al, byte [r15]                          | 41 2a 07                |
    | sub al, byte [rax + 1 * rcx]                | 2a 04 08                |
    | sub al, byte [rcx + 1 * rcx]                | 2a 04 09                |
    | sub al, byte [rdx + 1 * rcx]                | 2a 04 0a                |
    | sub al, byte [rbx + 1 * rcx]                | 2a 04 0b                |
    | sub al, byte [rsp + 1 * rcx]                | 2a 04 0c                |
    | sub al, byte [rbp + 1 * rcx]                | 2a 44 0d 00             |
    | sub al, byte [rsi + 1 * rcx]                | 2a 04 0e                |
    | sub al, byte [rdi + 1 * rcx]                | 2a 04 0f                |
    | sub al, byte [r8 + 1 * rcx]                 | 41 2a 04 08             |
    | sub al, byte [r9 + 1 * rcx]                 | 41 2a 04 09             |
    | sub al, byte [r10 + 1 * rcx]                | 41 2a 04 0a             |
    | sub al, byte [r11 + 1 * rcx]                | 41 2a 04 0b             |
    | sub al, byte [r12 + 1 * rcx]                | 41 2a 04 0c             |
    | sub al, byte [r13 + 1 * rcx]                | 41 2a 44 0d 00          |
    | sub al, byte [r14 + 1 * rcx]                | 41 2a 04 0e             |
    | sub al, byte [r15 + 1 * rcx]                | 41 2a 04 0f             |
    | sub al, byte [rax + 1 * rax]                | 2a 04 00                |
    | sub al, byte [rax + 1 * rdx]                | 2a 04 10                |
    | sub al, byte [rax + 1 * rbx]                | 2a 04 18                |
    | sub al, byte [rax + 1 * rbp]                | 2a 04 28                |
    | sub al, byte [rax + 1 * rsi]                | 2a 04 30                |
    | sub al, byte [rax + 1 * rdi]                | 2a 04 38                |
    | sub al, byte [rax + 1 * r8]                 | 42 2a 04 00             |
    | sub al, byte [rax + 1 * r9]                 | 42 2a 04 08             |
    | sub al, byte [rax + 1 * r10]                | 42 2a 04 10             |
    | sub al, byte [rax + 1 * r11]                | 42 2a 04 18             |
    | sub al, byte [rax + 1 * r12]                | 42 2a 04 20             |
    | sub al, byte [rax + 1 * r13]                | 42 2a 04 28             |
    | sub al, byte [rax + 1 * r14]                | 42 2a 04 30             |
    | sub al, byte [rax + 1 * r15]                | 42 2a 04 38             |
    | sub al, byte [rax + 2 * rcx]                | 2a 04 48                |
    | sub al, byte [rax + 4 * rcx]                | 2a 04 88                |
    | sub al, byte [rax + 8 * rcx]                | 2a 04 c8                |
    | sub al, byte [r8 + 1 * r9]                  | 43 2a 04 08             |
    | sub al, byte [r8 + 2 * r9]                  | 43 2a 04 48             |
    | sub al, byte [r8 + 4 * r9]                  | 43 2a 04 88             |
    | sub al, byte [r8 + 8 * r9]                  | 43 2a 04 c8             |
    | sub al, byte [1 * rcx]                      | 2a 04 0d 00 00 00 00    |
    | sub al, byte [2 * rcx]                      | 2a 04 4d 00 00 00 00    |
    | sub al, byte [4 * rcx]                      | 2a 04 8d 00 00 00 00    |
    | sub al, byte [8 * rcx]                      | 2a 04 cd 00 00 00 00    |
    | sub al, byte [1 * r9]                       | 42 2a 04 0d 00 00 00 00 |
    | sub al, byte [2 * r9]                       | 42 2a 04 4d 00 00 00 00 |
    | sub al, byte [4 * r9]                       | 42 2a 04 8d 00 00 00 00 |
    | sub al, byte [8 * r9]                       | 42 2a 04 cd 00 00 00 00 |
    | sub al, byte [r13 + 8 * r12]                | 43 2a 44 e5 00          |
    | sub al, byte [rsp + 4 * r15]                | 42 2a 04 bc             |
    | sub al, byte [rax + 1 * rcx + 0x00]         | 2a 44 08 00             |
    | sub al, byte [rax + 1 * rcx - 0x00]         | 2a 44 08 00             |
    | sub al, byte [rax + 1 * rcx + 0x01]         | 2a 44 08 01             |
    | sub al, byte [rax + 1 * rcx - 0x01]         | 2a 44 08 ff             |
    | sub al, byte [rax + 1 * rcx + 0x00000001]   | 2a 84 08 01 00 00 00    |
    | sub al, byte [rax + 1 * rcx - 0x00000001]   | 2a 84 08 ff ff ff ff    |
    | sub al, byte [rax + 1 * rcx + 0x7f]         | 2a 44 08 7f             |
    | sub al, byte [rax + 1 * rcx - 0x7f]         | 2a 44 08 81             |
    | sub al, byte [rax + 1 * rcx + 0x80]         | 2a 84 08 80 00 00 00    |
    | sub al, byte [rax + 1 * rcx - 0x80]         | 2a 44 08 80             |
    | sub al, byte [rax + 1 * rcx - 0x81]         | 2a 84 08 7f ff ff ff    |
    | sub al, byte [rax + 1 * rcx + 0xff]         | 2a 84 08 ff 00 00 00    |
    | sub al, byte [rax + 1 * rcx - 0xff]         | 2a 84 08 01 ff ff ff    |
    | sub al, byte [rax + 1 * rcx + 0x7fffffff]   | 2a 84 08 ff ff ff 7f    |
    | sub al, byte [rax + 1 * rcx - 0x7fffffff]   | 2a 84 08 01 00 00 80    |
    | sub al, byte [rax + 1 * rcx - 0x80000000]   | 2a 84 08 00 00 00 80    |
    | sub al, byte [r10 + 0x7f]                   | 41 2a 42 7f             |
    | sub al, byte [r10 + 0x80]                   | 41 2a 82 80 00 00 00    |
    | sub al, byte [r10 - 0x80]                   | 41 2a 42 80             |
    | sub al, byte [r10 - 0x81]                   | 41 2a 82 7f ff ff ff    |
    | sub cl, byte [rdx]                          | 2a 0a                   |
    | sub dl, byte [rbx]                          | 2a 13                   |
    | sub bl, byte [rsp]                          | 2a 1c 24                |
    | sub spl, byte [rbp]                         | 40 2a 65 00             |
    | sub bpl, byte [rsi]                         | 40 2a 2e                |
    | sub sil, byte [rdi]                         | 40 2a 37                |
    | sub dil, byte [r8]                          | 41 2a 38                |
    | sub r8b, byte [r9]                          | 45 2a 01                |
    | sub r9b, byte [r10]                         | 45 2a 0a                |
    | sub r10b, byte [r11]                        | 45 2a 13                |
    | sub r11b, byte [r12]                        | 45 2a 1c 24             |
    | sub r12b, byte [r13]                        | 45 2a 65 00             |
    | sub r13b, byte [r14]                        | 45 2a 2e                |
    | sub r14b, byte [r15]                        | 45 2a 37                |
    | sub r15b, byte [rax + 1 * rcx]              | 44 2a 3c 08             |
    | sub ah, byte [rcx + 1 * rcx]                | 2a 24 09                |
    | sub ch, byte [rdx + 1 * rcx]                | 2a 2c 0a                |
    | sub dh, byte [rbx + 1 * rcx]                | 2a 34 0b                |
    | sub bh, byte [rsp + 1 * rcx]                | 2a 3c 0c                |
    | sub cl, byte [rsi + 1 * rcx]                | 2a 0c 0e                |
    | sub dl, byte [rdi + 1 * rcx]                | 2a 14 0f                |
    | sub bl, byte [r8 + 1 * rcx]                 | 41 2a 1c 08             |
    | sub spl, byte [r9 + 1 * rcx]                | 41 2a 24 09             |
    | sub bpl, byte [r10 + 1 * rcx]               | 41 2a 2c 0a             |
    | sub sil, byte [r11 + 1 * rcx]               | 41 2a 34 0b             |
    | sub dil, byte [r12 + 1 * rcx]               | 41 2a 3c 0c             |
    | sub r8b, byte [r13 + 1 * rcx]               | 45 2a 44 0d 00          |
    | sub r9b, byte [r14 + 1 * rcx]               | 45 2a 0c 0e             |
    | sub r10b, byte [r15 + 1 * rcx]              | 45 2a 14 0f             |
    | sub r11b, byte [rax + 1 * rax]              | 44 2a 1c 00             |
    | sub r12b, byte [rax + 1 * rdx]              | 44 2a 24 10             |
    | sub r13b, byte [rax + 1 * rbx]              | 44 2a 2c 18             |
    | sub r14b, byte [rax + 1 * rbp]              | 44 2a 34 28             |
    | sub r15b, byte [rax + 1 * rsi]              | 44 2a 3c 30             |
    | sub ah, byte [rax + 1 * rdi]                | 2a 24 38                |
    | sub ch, byte [rax + 1 * r8]                 | !! !! !!                |
    | sub dh, byte [rax + 1 * r9]                 | !! !! !!                |
    | sub bh, byte [rax + 1 * r10]                | !! !! !!                |
    | sub cl, byte [rax + 1 * r12]                | 42 2a 0c 20             |
    | sub dl, byte [rax + 1 * r13]                | 42 2a 14 28             |
    | sub bl, byte [rax + 1 * r14]                | 42 2a 1c 30             |
    | sub spl, byte [rax + 1 * r15]               | 42 2a 24 38             |
    | sub bpl, byte [rax + 2 * rcx]               | 40 2a 2c 48             |
    | sub sil, byte [rax + 4 * rcx]               | 40 2a 34 88             |
    | sub dil, byte [rax + 8 * rcx]               | 40 2a 3c c8             |
    | sub r8b, byte [r8 + 1 * r9]                 | 47 2a 04 08             |
    | sub r9b, byte [r8 + 2 * r9]                 | 47 2a 0c 48             |
    | sub r10b, byte [r8 + 4 * r9]                | 47 2a 14 88             |
    | sub r11b, byte [r8 + 8 * r9]                | 47 2a 1c c8             |
    | sub r12b, byte [1 * rcx]                    | 44 2a 24 0d 00 00 00 00 |
    | sub r13b, byte [2 * rcx]                    | 44 2a 2c 4d 00 00 00 00 |
    | sub r14b, byte [4 * rcx]                    | 44 2a 34 8d 00 00 00 00 |
    | sub r15b, byte [8 * rcx]                    | 44 2a 3c cd 00 00 00 00 |
    | sub ah, byte [1 * r9]                       | !! !! !!                |
    | sub ch, byte [2 * r9]                       | !! !! !!                |
    | sub dh, byte [4 * r9]                       | !! !! !!                |
    | sub bh, byte [8 * r9]                       | !! !! !!                |
    | sub cl, byte [rsp + 4 * r15]                | 42 2a 0c bc             |
    | sub dl, byte [rax + 1 * rcx + 0x00]         | 2a 54 08 00             |
    | sub bl, byte [rax + 1 * rcx - 0x00]         | 2a 5c 08 00             |
    | sub spl, byte [rax + 1 * rcx + 0x01]        | 40 2a 64 08 01          |
    | sub bpl, byte [rax + 1 * rcx - 0x01]        | 40 2a 6c 08 ff          |
    | sub sil, byte [rax + 1 * rcx + 0x00000001]  | 40 2a b4 08 01 00 00 00 |
    | sub dil, byte [rax + 1 * rcx - 0x00000001]  | 40 2a bc 08 ff ff ff ff |
    | sub r8b, byte [rax + 1 * rcx + 0x7f]        | 44 2a 44 08 7f          |
    | sub r9b, byte [rax + 1 * rcx - 0x7f]        | 44 2a 4c 08 81          |
    | sub r10b, byte [rax + 1 * rcx + 0x80]       | 44 2a 94 08 80 00 00 00 |
    | sub r11b, byte [rax + 1 * rcx - 0x80]       | 44 2a 5c 08 80          |
    | sub r12b, byte [rax + 1 * rcx - 0x81]       | 44 2a a4 08 7f ff ff ff |
    | sub r13b, byte [rax + 1 * rcx + 0xff]       | 44 2a ac 08 ff 00 00 00 |
    | sub r14b, byte [rax + 1 * rcx - 0xff]       | 44 2a b4 08 01 ff ff ff |
    | sub r15b, byte [rax + 1 * rcx + 0x7fffffff] | 44 2a bc 08 ff ff ff 7f |
    | sub ah, byte [rax + 1 * rcx - 0x7fffffff]   | 2a a4 08 01 00 00 80    |
    | sub ch, byte [rax + 1 * rcx - 0x80000000]   | 2a ac 08 00 00 00 80    |
    | sub dh, byte [r10 + 0x7f]                   | !! !! !!                |
    | sub bh, byte [r10 + 0x80]                   | !! !! !!                |
    | sub cl, byte [r10 - 0x81]                   | 41 2a 8a 7f ff ff ff    |
    | sub dl, byte [rax]                          | 2a 10                   |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_sub_reg8_addr8():
    encode(SUB_REG8_ADDR8)


SUB_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sub qword [rax], 0x01                        | 48 83 28 01                |
    | sub qword [rcx], 0x01                        | 48 83 29 01                |
    | sub qword [rdx], 0x01                        | 48 83 2a 01                |
    | sub qword [rbx], 0x01                        | 48 83 2b 01                |
    | sub qword [rsp], 0x01                        | 48 83 2c 24 01             |
    | sub qword [rbp], 0x01                        | 48 83 6d 00 01             |
    | sub qword [rsi], 0x01                        | 48 83 2e 01                |
    | sub qword [rdi], 0x01                        | 48 83 2f 01                |
    | sub qword [r8], 0x01                         | 49 83 28 01                |
    | sub qword [r9], 0x01                         | 49 83 29 01                |
    | sub qword [r10], 0x01                        | 49 83 2a 01                |
    | sub qword [r11], 0x01                        | 49 83 2b 01                |
    | sub qword [r12], 0x01                        | 49 83 2c 24 01             |
    | sub qword [r13], 0x01                        | 49 83 6d 00 01             |
    | sub qword [r14], 0x01                        | 49 83 2e 01                |
    | sub qword [r15], 0x01                        | 49 83 2f 01                |
    | sub qword [rax + 1 * rcx], 0x01              | 48 83 2c 08 01             |
    | sub qword [rcx + 1 * rcx], 0x01              | 48 83 2c 09 01             |
    | sub qword [rdx + 1 * rcx], 0x01              | 48 83 2c 0a 01             |
    | sub qword [rbx + 1 * rcx], 0x01              | 48 83 2c 0b 01             |
    | sub qword [rsp + 1 * rcx], 0x01              | 48 83 2c 0c 01             |
    | sub qword [rbp + 1 * rcx], 0x01              | 48 83 6c 0d 00 01          |
    | sub qword [rsi + 1 * rcx], 0x01              | 48 83 2c 0e 01             |
    | sub qword [rdi + 1 * rcx], 0x01              | 48 83 2c 0f 01             |
    | sub qword [r8 + 1 * rcx], 0x01               | 49 83 2c 08 01             |
    | sub qword [r9 + 1 * rcx], 0x01               | 49 83 2c 09 01             |
    | sub qword [r10 + 1 * rcx], 0x01              | 49 83 2c 0a 01             |
    | sub qword [r11 + 1 * rcx], 0x01              | 49 83 2c 0b 01             |
    | sub qword [r12 + 1 * rcx], 0x01              | 49 83 2c 0c 01             |
    | sub qword [r13 + 1 * rcx], 0x01              | 49 83 6c 0d 00 01          |
    | sub qword [r14 + 1 * rcx], 0x01              | 49 83 2c 0e 01             |
    | sub qword [r15 + 1 * rcx], 0x01              | 49 83 2c 0f 01             |
    | sub qword [rax + 1 * rax], 0x01              | 48 83 2c 00 01             |
    | sub qword [rax + 1 * rdx], 0x01              | 48 83 2c 10 01             |
    | sub qword [rax + 1 * rbx], 0x01              | 48 83 2c 18 01             |
    | sub qword [rax + 1 * rbp], 0x01              | 48 83 2c 28 01             |
    | sub qword [rax + 1 * rsi], 0x01              | 48 83 2c 30 01             |
    | sub qword [rax + 1 * rdi], 0x01              | 48 83 2c 38 01             |
    | sub qword [rax + 1 * r8], 0x01               | 4a 83 2c 00 01             |
    | sub qword [rax + 1 * r9], 0x01               | 4a 83 2c 08 01             |
    | sub qword [rax + 1 * r10], 0x01              | 4a 83 2c 10 01             |
    | sub qword [rax + 1 * r11], 0x01              | 4a 83 2c 18 01             |
    | sub qword [rax + 1 * r12], 0x01              | 4a 83 2c 20 01             |
    | sub qword [rax + 1 * r13], 0x01              | 4a 83 2c 28 01             |
    | sub qword [rax + 1 * r14], 0x01              | 4a 83 2c 30 01             |
    | sub qword [rax + 1 * r15], 0x01              | 4a 83 2c 38 01             |
    | sub qword [rax + 2 * rcx], 0x01              | 48 83 2c 48 01             |
    | sub qword [rax + 4 * rcx], 0x01              | 48 83 2c 88 01             |
    | sub qword [rax + 8 * rcx], 0x01              | 48 83 2c c8 01             |
    | sub qword [r8 + 1 * r9], 0x01                | 4b 83 2c 08 01             |
    | sub qword [r8 + 2 * r9], 0x01                | 4b 83 2c 48 01             |
    | sub qword [r8 + 4 * r9], 0x01                | 4b 83 2c 88 01             |
    | sub qword [r8 + 8 * r9], 0x01                | 4b 83 2c c8 01             |
    | sub qword [1 * rcx], 0x01                    | 48 83 2c 0d 00 00 00 00 01 |
    | sub qword [2 * rcx], 0x01                    | 48 83 2c 4d 00 00 00 00 01 |
    | sub qword [4 * rcx], 0x01                    | 48 83 2c 8d 00 00 00 00 01 |
    | sub qword [8 * rcx], 0x01                    | 48 83 2c cd 00 00 00 00 01 |
    | sub qword [1 * r9], 0x01                     | 4a 83 2c 0d 00 00 00 00 01 |
    | sub qword [2 * r9], 0x01                     | 4a 83 2c 4d 00 00 00 00 01 |
    | sub qword [4 * r9], 0x01                     | 4a 83 2c 8d 00 00 00 00 01 |
    | sub qword [8 * r9], 0x01                     | 4a 83 2c cd 00 00 00 00 01 |
    | sub qword [r13 + 8 * r12], 0x01              | 4b 83 6c e5 00 01          |
    | sub qword [rsp + 4 * r15], 0x01              | 4a 83 2c bc 01             |
    | sub qword [rax + 1 * rcx + 0x00], 0x01       | 48 83 6c 08 00 01          |
    | sub qword [rax + 1 * rcx - 0x00], 0x01       | 48 83 6c 08 00 01          |
    | sub qword [rax + 1 * rcx + 0x01], 0x01       | 48 83 6c 08 01 01          |
    | sub qword [rax + 1 * rcx - 0x01], 0x01       | 48 83 6c 08 ff 01          |
    | sub qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 83 ac 08 01 00 00 00 01 |
    | sub qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 83 ac 08 ff ff ff ff 01 |
    | sub qword [rax + 1 * rcx + 0x7f], 0x01       | 48 83 6c 08 7f 01          |
    | sub qword [rax + 1 * rcx - 0x7f], 0x01       | 48 83 6c 08 81 01          |
    | sub qword [rax + 1 * rcx + 0x80], 0x01       | 48 83 ac 08 80 00 00 00 01 |
    | sub qword [rax + 1 * rcx - 0x80], 0x01       | 48 83 6c 08 80 01          |
    | sub qword [rax + 1 * rcx - 0x81], 0x01       | 48 83 ac 08 7f ff ff ff 01 |
    | sub qword [rax + 1 * rcx + 0xff], 0x01       | 48 83 ac 08 ff 00 00 00 01 |
    | sub qword [rax + 1 * rcx - 0xff], 0x01       | 48 83 ac 08 01 ff ff ff 01 |
    | sub qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 83 ac 08 ff ff ff 7f 01 |
    | sub qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 83 ac 08 01 00 00 80 01 |
    | sub qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 83 ac 08 00 00 00 80 01 |
    | sub qword [r10 + 0x7f], 0x01                 | 49 83 6a 7f 01             |
    | sub qword [r10 + 0x80], 0x01                 | 49 83 aa 80 00 00 00 01    |
    | sub qword [r10 - 0x80], 0x01                 | 49 83 6a 80 01             |
    | sub qword [r10 - 0x81], 0x01                 | 49 83 aa 7f ff ff ff 01    |
    | sub qword [rax], 0x00                        | 48 83 28 00                |
    | sub qword [rax], 0x7f                        | 48 83 28 7f                |
    | sub qword [rax], 0x80                        | 48 83 28 80                |
    | sub qword [rax], 0xff                        | 48 83 28 ff                |
    | sub qword [rcx], 0x7f                        | 48 83 29 7f                |
    | sub qword [rdx], 0x80                        | 48 83 2a 80                |
    | sub qword [rbx], 0xff                        | 48 83 2b ff                |
    | sub qword [rsp], 0x00                        | 48 83 2c 24 00             |
    | sub qword [rsi], 0x7f                        | 48 83 2e 7f                |
    | sub qword [rdi], 0x80                        | 48 83 2f 80                |
    | sub qword [r8], 0xff                         | 49 83 28 ff                |
    | sub qword [r9], 0x00                         | 49 83 29 00                |
    | sub qword [r11], 0x7f                        | 49 83 2b 7f                |
    | sub qword [r12], 0x80                        | 49 83 2c 24 80             |
    | sub qword [r13], 0xff                        | 49 83 6d 00 ff             |
    | sub qword [r14], 0x00                        | 49 83 2e 00                |
    | sub qword [rax + 1 * rcx], 0x7f              | 48 83 2c 08 7f             |
    | sub qword [rcx + 1 * rcx], 0x80              | 48 83 2c 09 80             |
    | sub qword [rdx + 1 * rcx], 0xff              | 48 83 2c 0a ff             |
    | sub qword [rbx + 1 * rcx], 0x00              | 48 83 2c 0b 00             |
    | sub qword [rbp + 1 * rcx], 0x7f              | 48 83 6c 0d 00 7f          |
    | sub qword [rsi + 1 * rcx], 0x80              | 48 83 2c 0e 80             |
    | sub qword [rdi + 1 * rcx], 0xff              | 48 83 2c 0f ff             |
    | sub qword [r8 + 1 * rcx], 0x00               | 49 83 2c 08 00             |
    | sub qword [r10 + 1 * rcx], 0x7f              | 49 83 2c 0a 7f             |
    | sub qword [r11 + 1 * rcx], 0x80              | 49 83 2c 0b 80             |
    | sub qword [r12 + 1 * rcx], 0xff              | 49 83 2c 0c ff             |
    | sub qword [r13 + 1 * rcx], 0x00              | 49 83 6c 0d 00 00          |
    | sub qword [r15 + 1 * rcx], 0x7f              | 49 83 2c 0f 7f             |
    | sub qword [rax + 1 * rax], 0x80              | 48 83 2c 00 80             |
    | sub qword [rax + 1 * rdx], 0xff              | 48 83 2c 10 ff             |
    | sub qword [rax + 1 * rbx], 0x00              | 48 83 2c 18 00             |
    | sub qword [rax + 1 * rsi], 0x7f              | 48 83 2c 30 7f             |
    | sub qword [rax + 1 * rdi], 0x80              | 48 83 2c 38 80             |
    | sub qword [rax + 1 * r8], 0xff               | 4a 83 2c 00 ff             |
    | sub qword [rax + 1 * r9], 0x00               | 4a 83 2c 08 00             |
    | sub qword [rax + 1 * r11], 0x7f              | 4a 83 2c 18 7f             |
    | sub qword [rax + 1 * r12], 0x80              | 4a 83 2c 20 80             |
    | sub qword [rax + 1 * r13], 0xff              | 4a 83 2c 28 ff             |
    | sub qword [rax + 1 * r14], 0x00              | 4a 83 2c 30 00             |
    | sub qword [rax + 2 * rcx], 0x7f              | 48 83 2c 48 7f             |
    | sub qword [rax + 4 * rcx], 0x80              | 48 83 2c 88 80             |
    | sub qword [rax + 8 * rcx], 0xff              | 48 83 2c c8 ff             |
    | sub qword [r8 + 1 * r9], 0x00                | 4b 83 2c 08 00             |
    | sub qword [r8 + 4 * r9], 0x7f                | 4b 83 2c 88 7f             |
    | sub qword [r8 + 8 * r9], 0x80                | 4b 83 2c c8 80             |
    | sub qword [1 * rcx], 0xff                    | 48 83 2c 0d 00 00 00 00 ff |
    | sub qword [2 * rcx], 0x00                    | 48 83 2c 4d 00 00 00 00 00 |
    | sub qword [8 * rcx], 0x7f                    | 48 83 2c cd 00 00 00 00 7f |
    | sub qword [1 * r9], 0x80                     | 4a 83 2c 0d 00 00 00 00 80 |
    | sub qword [2 * r9], 0xff                     | 4a 83 2c 4d 00 00 00 00 ff |
    | sub qword [4 * r9], 0x00                     | 4a 83 2c 8d 00 00 00 00 00 |
    | sub qword [r13 + 8 * r12], 0x7f              | 4b 83 6c e5 00 7f          |
    | sub qword [rsp + 4 * r15], 0x80              | 4a 83 2c bc 80             |
    | sub qword [rax + 1 * rcx + 0x00], 0xff       | 48 83 6c 08 00 ff          |
    | sub qword [rax + 1 * rcx - 0x00], 0x00       | 48 83 6c 08 00 00          |
    | sub qword [rax + 1 * rcx - 0x01], 0x7f       | 48 83 6c 08 ff 7f          |
    | sub qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 83 ac 08 01 00 00 00 80 |
    | sub qword [rax + 1 * rcx - 0x00000001], 0xff | 48 83 ac 08 ff ff ff ff ff |
    | sub qword [rax + 1 * rcx + 0x7f], 0x00       | 48 83 6c 08 7f 00          |
    | sub qword [rax + 1 * rcx + 0x80], 0x7f       | 48 83 ac 08 80 00 00 00 7f |
    | sub qword [rax + 1 * rcx - 0x80], 0x80       | 48 83 6c 08 80 80          |
    | sub qword [rax + 1 * rcx - 0x81], 0xff       | 48 83 ac 08 7f ff ff ff ff |
    | sub qword [rax + 1 * rcx + 0xff], 0x00       | 48 83 ac 08 ff 00 00 00 00 |
    | sub qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 83 ac 08 ff ff ff 7f 7f |
    | sub qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 83 ac 08 01 00 00 80 80 |
    | sub qword [rax + 1 * rcx - 0x80000000], 0xff | 48 83 ac 08 00 00 00 80 ff |
    | sub qword [r10 + 0x7f], 0x00                 | 49 83 6a 7f 00             |
    | sub qword [r10 - 0x80], 0x7f                 | 49 83 6a 80 7f             |
    | sub qword [r10 - 0x81], 0x80                 | 49 83 aa 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sub_addr64_imm8():
    encode(SUB_ADDR64_IMM8)


SUB_ADDR64_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | sub qword [rax], 0x00000001                        | 48 81 28 01 00 00 00                |
    | sub qword [rcx], 0x00000001                        | 48 81 29 01 00 00 00                |
    | sub qword [rdx], 0x00000001                        | 48 81 2a 01 00 00 00                |
    | sub qword [rbx], 0x00000001                        | 48 81 2b 01 00 00 00                |
    | sub qword [rsp], 0x00000001                        | 48 81 2c 24 01 00 00 00             |
    | sub qword [rbp], 0x00000001                        | 48 81 6d 00 01 00 00 00             |
    | sub qword [rsi], 0x00000001                        | 48 81 2e 01 00 00 00                |
    | sub qword [rdi], 0x00000001                        | 48 81 2f 01 00 00 00                |
    | sub qword [r8], 0x00000001                         | 49 81 28 01 00 00 00                |
    | sub qword [r9], 0x00000001                         | 49 81 29 01 00 00 00                |
    | sub qword [r10], 0x00000001                        | 49 81 2a 01 00 00 00                |
    | sub qword [r11], 0x00000001                        | 49 81 2b 01 00 00 00                |
    | sub qword [r12], 0x00000001                        | 49 81 2c 24 01 00 00 00             |
    | sub qword [r13], 0x00000001                        | 49 81 6d 00 01 00 00 00             |
    | sub qword [r14], 0x00000001                        | 49 81 2e 01 00 00 00                |
    | sub qword [r15], 0x00000001                        | 49 81 2f 01 00 00 00                |
    | sub qword [rax + 1 * rcx], 0x00000001              | 48 81 2c 08 01 00 00 00             |
    | sub qword [rcx + 1 * rcx], 0x00000001              | 48 81 2c 09 01 00 00 00             |
    | sub qword [rdx + 1 * rcx], 0x00000001              | 48 81 2c 0a 01 00 00 00             |
    | sub qword [rbx + 1 * rcx], 0x00000001              | 48 81 2c 0b 01 00 00 00             |
    | sub qword [rsp + 1 * rcx], 0x00000001              | 48 81 2c 0c 01 00 00 00             |
    | sub qword [rbp + 1 * rcx], 0x00000001              | 48 81 6c 0d 00 01 00 00 00          |
    | sub qword [rsi + 1 * rcx], 0x00000001              | 48 81 2c 0e 01 00 00 00             |
    | sub qword [rdi + 1 * rcx], 0x00000001              | 48 81 2c 0f 01 00 00 00             |
    | sub qword [r8 + 1 * rcx], 0x00000001               | 49 81 2c 08 01 00 00 00             |
    | sub qword [r9 + 1 * rcx], 0x00000001               | 49 81 2c 09 01 00 00 00             |
    | sub qword [r10 + 1 * rcx], 0x00000001              | 49 81 2c 0a 01 00 00 00             |
    | sub qword [r11 + 1 * rcx], 0x00000001              | 49 81 2c 0b 01 00 00 00             |
    | sub qword [r12 + 1 * rcx], 0x00000001              | 49 81 2c 0c 01 00 00 00             |
    | sub qword [r13 + 1 * rcx], 0x00000001              | 49 81 6c 0d 00 01 00 00 00          |
    | sub qword [r14 + 1 * rcx], 0x00000001              | 49 81 2c 0e 01 00 00 00             |
    | sub qword [r15 + 1 * rcx], 0x00000001              | 49 81 2c 0f 01 00 00 00             |
    | sub qword [rax + 1 * rax], 0x00000001              | 48 81 2c 00 01 00 00 00             |
    | sub qword [rax + 1 * rdx], 0x00000001              | 48 81 2c 10 01 00 00 00             |
    | sub qword [rax + 1 * rbx], 0x00000001              | 48 81 2c 18 01 00 00 00             |
    | sub qword [rax + 1 * rbp], 0x00000001              | 48 81 2c 28 01 00 00 00             |
    | sub qword [rax + 1 * rsi], 0x00000001              | 48 81 2c 30 01 00 00 00             |
    | sub qword [rax + 1 * rdi], 0x00000001              | 48 81 2c 38 01 00 00 00             |
    | sub qword [rax + 1 * r8], 0x00000001               | 4a 81 2c 00 01 00 00 00             |
    | sub qword [rax + 1 * r9], 0x00000001               | 4a 81 2c 08 01 00 00 00             |
    | sub qword [rax + 1 * r10], 0x00000001              | 4a 81 2c 10 01 00 00 00             |
    | sub qword [rax + 1 * r11], 0x00000001              | 4a 81 2c 18 01 00 00 00             |
    | sub qword [rax + 1 * r12], 0x00000001              | 4a 81 2c 20 01 00 00 00             |
    | sub qword [rax + 1 * r13], 0x00000001              | 4a 81 2c 28 01 00 00 00             |
    | sub qword [rax + 1 * r14], 0x00000001              | 4a 81 2c 30 01 00 00 00             |
    | sub qword [rax + 1 * r15], 0x00000001              | 4a 81 2c 38 01 00 00 00             |
    | sub qword [rax + 2 * rcx], 0x00000001              | 48 81 2c 48 01 00 00 00             |
    | sub qword [rax + 4 * rcx], 0x00000001              | 48 81 2c 88 01 00 00 00             |
    | sub qword [rax + 8 * rcx], 0x00000001              | 48 81 2c c8 01 00 00 00             |
    | sub qword [r8 + 1 * r9], 0x00000001                | 4b 81 2c 08 01 00 00 00             |
    | sub qword [r8 + 2 * r9], 0x00000001                | 4b 81 2c 48 01 00 00 00             |
    | sub qword [r8 + 4 * r9], 0x00000001                | 4b 81 2c 88 01 00 00 00             |
    | sub qword [r8 + 8 * r9], 0x00000001                | 4b 81 2c c8 01 00 00 00             |
    | sub qword [1 * rcx], 0x00000001                    | 48 81 2c 0d 00 00 00 00 01 00 00 00 |
    | sub qword [2 * rcx], 0x00000001                    | 48 81 2c 4d 00 00 00 00 01 00 00 00 |
    | sub qword [4 * rcx], 0x00000001                    | 48 81 2c 8d 00 00 00 00 01 00 00 00 |
    | sub qword [8 * rcx], 0x00000001                    | 48 81 2c cd 00 00 00 00 01 00 00 00 |
    | sub qword [1 * r9], 0x00000001                     | 4a 81 2c 0d 00 00 00 00 01 00 00 00 |
    | sub qword [2 * r9], 0x00000001                     | 4a 81 2c 4d 00 00 00 00 01 00 00 00 |
    | sub qword [4 * r9], 0x00000001                     | 4a 81 2c 8d 00 00 00 00 01 00 00 00 |
    | sub qword [8 * r9], 0x00000001                     | 4a 81 2c cd 00 00 00 00 01 00 00 00 |
    | sub qword [r13 + 8 * r12], 0x00000001              | 4b 81 6c e5 00 01 00 00 00          |
    | sub qword [rsp + 4 * r15], 0x00000001              | 4a 81 2c bc 01 00 00 00             |
    | sub qword [rax + 1 * rcx + 0x00], 0x00000001       | 48 81 6c 08 00 01 00 00 00          |
    | sub qword [rax + 1 * rcx - 0x00], 0x00000001       | 48 81 6c 08 00 01 00 00 00          |
    | sub qword [rax + 1 * rcx + 0x01], 0x00000001       | 48 81 6c 08 01 01 00 00 00          |
    | sub qword [rax + 1 * rcx - 0x01], 0x00000001       | 48 81 6c 08 ff 01 00 00 00          |
    | sub qword [rax + 1 * rcx + 0x00000001], 0x00000001 | 48 81 ac 08 01 00 00 00 01 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x00000001], 0x00000001 | 48 81 ac 08 ff ff ff ff 01 00 00 00 |
    | sub qword [rax + 1 * rcx + 0x7f], 0x00000001       | 48 81 6c 08 7f 01 00 00 00          |
    | sub qword [rax + 1 * rcx - 0x7f], 0x00000001       | 48 81 6c 08 81 01 00 00 00          |
    | sub qword [rax + 1 * rcx + 0x80], 0x00000001       | 48 81 ac 08 80 00 00 00 01 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x80], 0x00000001       | 48 81 6c 08 80 01 00 00 00          |
    | sub qword [rax + 1 * rcx - 0x81], 0x00000001       | 48 81 ac 08 7f ff ff ff 01 00 00 00 |
    | sub qword [rax + 1 * rcx + 0xff], 0x00000001       | 48 81 ac 08 ff 00 00 00 01 00 00 00 |
    | sub qword [rax + 1 * rcx - 0xff], 0x00000001       | 48 81 ac 08 01 ff ff ff 01 00 00 00 |
    | sub qword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 48 81 ac 08 ff ff ff 7f 01 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 48 81 ac 08 01 00 00 80 01 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x80000000], 0x00000001 | 48 81 ac 08 00 00 00 80 01 00 00 00 |
    | sub qword [r10 + 0x7f], 0x00000001                 | 49 81 6a 7f 01 00 00 00             |
    | sub qword [r10 + 0x80], 0x00000001                 | 49 81 aa 80 00 00 00 01 00 00 00    |
    | sub qword [r10 - 0x80], 0x00000001                 | 49 81 6a 80 01 00 00 00             |
    | sub qword [r10 - 0x81], 0x00000001                 | 49 81 aa 7f ff ff ff 01 00 00 00    |
    | sub qword [rax], 0x00000000                        | 48 81 28 00 00 00 00                |
    | sub qword [rax], 0x0000007f                        | 48 81 28 7f 00 00 00                |
    | sub qword [rax], 0x00000080                        | 48 81 28 80 00 00 00                |
    | sub qword [rax], 0x000000ff                        | 48 81 28 ff 00 00 00                |
    | sub qword [rax], 0x00000100                        | 48 81 28 00 01 00 00                |
    | sub qword [rax], 0x00007fff                        | 48 81 28 ff 7f 00 00                |
    | sub qword [rax], 0x00008000                        | 48 81 28 00 80 00 00                |
    | sub qword [rax], 0x0000ffff                        | 48 81 28 ff ff 00 00                |
    | sub qword [rax], 0x00010000                        | 48 81 28 00 00 01 00                |
    | sub qword [rax], 0x7fffffff                        | 48 81 28 ff ff ff 7f                |
    | sub qword [rax], 0x80000000                        | 48 81 28 00 00 00 80                |
    | sub qword [rax], 0xffffffff                        | 48 81 28 ff ff ff ff                |
    | sub qword [rcx], 0x0000007f                        | 48 81 29 7f 00 00 00                |
    | sub qword [rdx], 0x00000080                        | 48 81 2a 80 00 00 00                |
    | sub qword [rbx], 0x000000ff                        | 48 81 2b ff 00 00 00                |
    | sub qword [rsp], 0x00000100                        | 48 81 2c 24 00 01 00 00             |
    | sub qword [rbp], 0x00007fff                        | 48 81 6d 00 ff 7f 00 00             |
    | sub qword [rsi], 0x00008000                        | 48 81 2e 00 80 00 00                |
    | sub qword [rdi], 0x0000ffff                        | 48 81 2f ff ff 00 00                |
    | sub qword [r8], 0x00010000                         | 49 81 28 00 00 01 00                |
    | sub qword [r9], 0x7fffffff                         | 49 81 29 ff ff ff 7f                |
    | sub qword [r10], 0x80000000                        | 49 81 2a 00 00 00 80                |
    | sub qword [r11], 0xffffffff                        | 49 81 2b ff ff ff ff                |
    | sub qword [r12], 0x00000000                        | 49 81 2c 24 00 00 00 00             |
    | sub qword [r14], 0x0000007f                        | 49 81 2e 7f 00 00 00                |
    | sub qword [r15], 0x00000080                        | 49 81 2f 80 00 00 00                |
    | sub qword [rax + 1 * rcx], 0x000000ff              | 48 81 2c 08 ff 00 00 00             |
    | sub qword [rcx + 1 * rcx], 0x00000100              | 48 81 2c 09 00 01 00 00             |
    | sub qword [rdx + 1 * rcx], 0x00007fff              | 48 81 2c 0a ff 7f 00 00             |
    | sub qword [rbx + 1 * rcx], 0x00008000              | 48 81 2c 0b 00 80 00 00             |
    | sub qword [rsp + 1 * rcx], 0x0000ffff              | 48 81 2c 0c ff ff 00 00             |
    | sub qword [rbp + 1 * rcx], 0x00010000              | 48 81 6c 0d 00 00 00 01 00          |
    | sub qword [rsi + 1 * rcx], 0x7fffffff              | 48 81 2c 0e ff ff ff 7f             |
    | sub qword [rdi + 1 * rcx], 0x80000000              | 48 81 2c 0f 00 00 00 80             |
    | sub qword [r8 + 1 * rcx], 0xffffffff               | 49 81 2c 08 ff ff ff ff             |
    | sub qword [r9 + 1 * rcx], 0x00000000               | 49 81 2c 09 00 00 00 00             |
    | sub qword [r11 + 1 * rcx], 0x0000007f              | 49 81 2c 0b 7f 00 00 00             |
    | sub qword [r12 + 1 * rcx], 0x00000080              | 49 81 2c 0c 80 00 00 00             |
    | sub qword [r13 + 1 * rcx], 0x000000ff              | 49 81 6c 0d 00 ff 00 00 00          |
    | sub qword [r14 + 1 * rcx], 0x00000100              | 49 81 2c 0e 00 01 00 00             |
    | sub qword [r15 + 1 * rcx], 0x00007fff              | 49 81 2c 0f ff 7f 00 00             |
    | sub qword [rax + 1 * rax], 0x00008000              | 48 81 2c 00 00 80 00 00             |
    | sub qword [rax + 1 * rdx], 0x0000ffff              | 48 81 2c 10 ff ff 00 00             |
    | sub qword [rax + 1 * rbx], 0x00010000              | 48 81 2c 18 00 00 01 00             |
    | sub qword [rax + 1 * rbp], 0x7fffffff              | 48 81 2c 28 ff ff ff 7f             |
    | sub qword [rax + 1 * rsi], 0x80000000              | 48 81 2c 30 00 00 00 80             |
    | sub qword [rax + 1 * rdi], 0xffffffff              | 48 81 2c 38 ff ff ff ff             |
    | sub qword [rax + 1 * r8], 0x00000000               | 4a 81 2c 00 00 00 00 00             |
    | sub qword [rax + 1 * r10], 0x0000007f              | 4a 81 2c 10 7f 00 00 00             |
    | sub qword [rax + 1 * r11], 0x00000080              | 4a 81 2c 18 80 00 00 00             |
    | sub qword [rax + 1 * r12], 0x000000ff              | 4a 81 2c 20 ff 00 00 00             |
    | sub qword [rax + 1 * r13], 0x00000100              | 4a 81 2c 28 00 01 00 00             |
    | sub qword [rax + 1 * r14], 0x00007fff              | 4a 81 2c 30 ff 7f 00 00             |
    | sub qword [rax + 1 * r15], 0x00008000              | 4a 81 2c 38 00 80 00 00             |
    | sub qword [rax + 2 * rcx], 0x0000ffff              | 48 81 2c 48 ff ff 00 00             |
    | sub qword [rax + 4 * rcx], 0x00010000              | 48 81 2c 88 00 00 01 00             |
    | sub qword [rax + 8 * rcx], 0x7fffffff              | 48 81 2c c8 ff ff ff 7f             |
    | sub qword [r8 + 1 * r9], 0x80000000                | 4b 81 2c 08 00 00 00 80             |
    | sub qword [r8 + 2 * r9], 0xffffffff                | 4b 81 2c 48 ff ff ff ff             |
    | sub qword [r8 + 4 * r9], 0x00000000                | 4b 81 2c 88 00 00 00 00             |
    | sub qword [1 * rcx], 0x0000007f                    | 48 81 2c 0d 00 00 00 00 7f 00 00 00 |
    | sub qword [2 * rcx], 0x00000080                    | 48 81 2c 4d 00 00 00 00 80 00 00 00 |
    | sub qword [4 * rcx], 0x000000ff                    | 48 81 2c 8d 00 00 00 00 ff 00 00 00 |
    | sub qword [8 * rcx], 0x00000100                    | 48 81 2c cd 00 00 00 00 00 01 00 00 |
    | sub qword [1 * r9], 0x00007fff                     | 4a 81 2c 0d 00 00 00 00 ff 7f 00 00 |
    | sub qword [2 * r9], 0x00008000                     | 4a 81 2c 4d 00 00 00 00 00 80 00 00 |
    | sub qword [4 * r9], 0x0000ffff                     | 4a 81 2c 8d 00 00 00 00 ff ff 00 00 |
    | sub qword [8 * r9], 0x00010000                     | 4a 81 2c cd 00 00 00 00 00 00 01 00 |
    | sub qword [r13 + 8 * r12], 0x7fffffff              | 4b 81 6c e5 00 ff ff ff 7f          |
    | sub qword [rsp + 4 * r15], 0x80000000              | 4a 81 2c bc 00 00 00 80             |
    | sub qword [rax + 1 * rcx + 0x00], 0xffffffff       | 48 81 6c 08 00 ff ff ff ff          |
    | sub qword [rax + 1 * rcx - 0x00], 0x00000000       | 48 81 6c 08 00 00 00 00 00          |
    | sub qword [rax + 1 * rcx - 0x01], 0x0000007f       | 48 81 6c 08 ff 7f 00 00 00          |
    | sub qword [rax + 1 * rcx + 0x00000001], 0x00000080 | 48 81 ac 08 01 00 00 00 80 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x00000001], 0x000000ff | 48 81 ac 08 ff ff ff ff ff 00 00 00 |
    | sub qword [rax + 1 * rcx + 0x7f], 0x00000100       | 48 81 6c 08 7f 00 01 00 00          |
    | sub qword [rax + 1 * rcx - 0x7f], 0x00007fff       | 48 81 6c 08 81 ff 7f 00 00          |
    | sub qword [rax + 1 * rcx + 0x80], 0x00008000       | 48 81 ac 08 80 00 00 00 00 80 00 00 |
    | sub qword [rax + 1 * rcx - 0x80], 0x0000ffff       | 48 81 6c 08 80 ff ff 00 00          |
    | sub qword [rax + 1 * rcx - 0x81], 0x00010000       | 48 81 ac 08 7f ff ff ff 00 00 01 00 |
    | sub qword [rax + 1 * rcx + 0xff], 0x7fffffff       | 48 81 ac 08 ff 00 00 00 ff ff ff 7f |
    | sub qword [rax + 1 * rcx - 0xff], 0x80000000       | 48 81 ac 08 01 ff ff ff 00 00 00 80 |
    | sub qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 48 81 ac 08 ff ff ff 7f ff ff ff ff |
    | sub qword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 48 81 ac 08 01 00 00 80 00 00 00 00 |
    | sub qword [r10 + 0x7f], 0x0000007f                 | 49 81 6a 7f 7f 00 00 00             |
    | sub qword [r10 + 0x80], 0x00000080                 | 49 81 aa 80 00 00 00 80 00 00 00    |
    | sub qword [r10 - 0x80], 0x000000ff                 | 49 81 6a 80 ff 00 00 00             |
    | sub qword [r10 - 0x81], 0x00000100                 | 49 81 aa 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_sub_addr64_imm32():
    encode(SUB_ADDR64_IMM32)


SUB_ADDR64_REG64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | sub qword [rax], rcx                        | 48 29 08                |
    | sub qword [rcx], rcx                        | 48 29 09                |
    | sub qword [rdx], rcx                        | 48 29 0a                |
    | sub qword [rbx], rcx                        | 48 29 0b                |
    | sub qword [rsp], rcx                        | 48 29 0c 24             |
    | sub qword [rbp], rcx                        | 48 29 4d 00             |
    | sub qword [rsi], rcx                        | 48 29 0e                |
    | sub qword [rdi], rcx                        | 48 29 0f                |
    | sub qword [r8], rcx                         | 49 29 08                |
    | sub qword [r9], rcx                         | 49 29 09                |
    | sub qword [r10], rcx                        | 49 29 0a                |
    | sub qword [r11], rcx                        | 49 29 0b                |
    | sub qword [r12], rcx                        | 49 29 0c 24             |
    | sub qword [r13], rcx                        | 49 29 4d 00             |
    | sub qword [r14], rcx                        | 49 29 0e                |
    | sub qword [r15], rcx                        | 49 29 0f                |
    | sub qword [rax + 1 * rcx], rcx              | 48 29 0c 08             |
    | sub qword [rcx + 1 * rcx], rcx              | 48 29 0c 09             |
    | sub qword [rdx + 1 * rcx], rcx              | 48 29 0c 0a             |
    | sub qword [rbx + 1 * rcx], rcx              | 48 29 0c 0b             |
    | sub qword [rsp + 1 * rcx], rcx              | 48 29 0c 0c             |
    | sub qword [rbp + 1 * rcx], rcx              | 48 29 4c 0d 00          |
    | sub qword [rsi + 1 * rcx], rcx              | 48 29 0c 0e             |
    | sub qword [rdi + 1 * rcx], rcx              | 48 29 0c 0f             |
    | sub qword [r8 + 1 * rcx], rcx               | 49 29 0c 08             |
    | sub qword [r9 + 1 * rcx], rcx               | 49 29 0c 09             |
    | sub qword [r10 + 1 * rcx], rcx              | 49 29 0c 0a             |
    | sub qword [r11 + 1 * rcx], rcx              | 49 29 0c 0b             |
    | sub qword [r12 + 1 * rcx], rcx              | 49 29 0c 0c             |
    | sub qword [r13 + 1 * rcx], rcx              | 49 29 4c 0d 00          |
    | sub qword [r14 + 1 * rcx], rcx              | 49 29 0c 0e             |
    | sub qword [r15 + 1 * rcx], rcx              | 49 29 0c 0f             |
    | sub qword [rax + 1 * rax], rcx              | 48 29 0c 00             |
    | sub qword [rax + 1 * rdx], rcx              | 48 29 0c 10             |
    | sub qword [rax + 1 * rbx], rcx              | 48 29 0c 18             |
    | sub qword [rax + 1 * rbp], rcx              | 48 29 0c 28             |
    | sub qword [rax + 1 * rsi], rcx              | 48 29 0c 30             |
    | sub qword [rax + 1 * rdi], rcx              | 48 29 0c 38             |
    | sub qword [rax + 1 * r8], rcx               | 4a 29 0c 00             |
    | sub qword [rax + 1 * r9], rcx               | 4a 29 0c 08             |
    | sub qword [rax + 1 * r10], rcx              | 4a 29 0c 10             |
    | sub qword [rax + 1 * r11], rcx              | 4a 29 0c 18             |
    | sub qword [rax + 1 * r12], rcx              | 4a 29 0c 20             |
    | sub qword [rax + 1 * r13], rcx              | 4a 29 0c 28             |
    | sub qword [rax + 1 * r14], rcx              | 4a 29 0c 30             |
    | sub qword [rax + 1 * r15], rcx              | 4a 29 0c 38             |
    | sub qword [rax + 2 * rcx], rcx              | 48 29 0c 48             |
    | sub qword [rax + 4 * rcx], rcx              | 48 29 0c 88             |
    | sub qword [rax + 8 * rcx], rcx              | 48 29 0c c8             |
    | sub qword [r8 + 1 * r9], rcx                | 4b 29 0c 08             |
    | sub qword [r8 + 2 * r9], rcx                | 4b 29 0c 48             |
    | sub qword [r8 + 4 * r9], rcx                | 4b 29 0c 88             |
    | sub qword [r8 + 8 * r9], rcx                | 4b 29 0c c8             |
    | sub qword [1 * rcx], rcx                    | 48 29 0c 0d 00 00 00 00 |
    | sub qword [2 * rcx], rcx                    | 48 29 0c 4d 00 00 00 00 |
    | sub qword [4 * rcx], rcx                    | 48 29 0c 8d 00 00 00 00 |
    | sub qword [8 * rcx], rcx                    | 48 29 0c cd 00 00 00 00 |
    | sub qword [1 * r9], rcx                     | 4a 29 0c 0d 00 00 00 00 |
    | sub qword [2 * r9], rcx                     | 4a 29 0c 4d 00 00 00 00 |
    | sub qword [4 * r9], rcx                     | 4a 29 0c 8d 00 00 00 00 |
    | sub qword [8 * r9], rcx                     | 4a 29 0c cd 00 00 00 00 |
    | sub qword [r13 + 8 * r12], rcx              | 4b 29 4c e5 00          |
    | sub qword [rsp + 4 * r15], rcx              | 4a 29 0c bc             |
    | sub qword [rax + 1 * rcx + 0x00], rcx       | 48 29 4c 08 00          |
    | sub qword [rax + 1 * rcx - 0x00], rcx       | 48 29 4c 08 00          |
    | sub qword [rax + 1 * rcx + 0x01], rcx       | 48 29 4c 08 01          |
    | sub qword [rax + 1 * rcx - 0x01], rcx       | 48 29 4c 08 ff          |
    | sub qword [rax + 1 * rcx + 0x00000001], rcx | 48 29 8c 08 01 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x00000001], rcx | 48 29 8c 08 ff ff ff ff |
    | sub qword [rax + 1 * rcx + 0x7f], rcx       | 48 29 4c 08 7f          |
    | sub qword [rax + 1 * rcx - 0x7f], rcx       | 48 29 4c 08 81          |
    | sub qword [rax + 1 * rcx + 0x80], rcx       | 48 29 8c 08 80 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x80], rcx       | 48 29 4c 08 80          |
    | sub qword [rax + 1 * rcx - 0x81], rcx       | 48 29 8c 08 7f ff ff ff |
    | sub qword [rax + 1 * rcx + 0xff], rcx       | 48 29 8c 08 ff 00 00 00 |
    | sub qword [rax + 1 * rcx - 0xff], rcx       | 48 29 8c 08 01 ff ff ff |
    | sub qword [rax + 1 * rcx + 0x7fffffff], rcx | 48 29 8c 08 ff ff ff 7f |
    | sub qword [rax + 1 * rcx - 0x7fffffff], rcx | 48 29 8c 08 01 00 00 80 |
    | sub qword [rax + 1 * rcx - 0x80000000], rcx | 48 29 8c 08 00 00 00 80 |
    | sub qword [r10 + 0x7f], rcx                 | 49 29 4a 7f             |
    | sub qword [r10 + 0x80], rcx                 | 49 29 8a 80 00 00 00    |
    | sub qword [r10 - 0x80], rcx                 | 49 29 4a 80             |
    | sub qword [r10 - 0x81], rcx                 | 49 29 8a 7f ff ff ff    |
    | sub qword [rax], rax                        | 48 29 00                |
    | sub qword [rax], rdx                        | 48 29 10                |
    | sub qword [rax], rbx                        | 48 29 18                |
    | sub qword [rax], rsp                        | 48 29 20                |
    | sub qword [rax], rbp                        | 48 29 28                |
    | sub qword [rax], rsi                        | 48 29 30                |
    | sub qword [rax], rdi                        | 48 29 38                |
    | sub qword [rax], r8                         | 4c 29 00                |
    | sub qword [rax], r9                         | 4c 29 08                |
    | sub qword [rax], r10                        | 4c 29 10                |
    | sub qword [rax], r11                        | 4c 29 18                |
    | sub qword [rax], r12                        | 4c 29 20                |
    | sub qword [rax], r13                        | 4c 29 28                |
    | sub qword [rax], r14                        | 4c 29 30                |
    | sub qword [rax], r15                        | 4c 29 38                |
    | sub qword [rcx], rdx                        | 48 29 11                |
    | sub qword [rdx], rbx                        | 48 29 1a                |
    | sub qword [rbx], rsp                        | 48 29 23                |
    | sub qword [rsp], rbp                        | 48 29 2c 24             |
    | sub qword [rbp], rsi                        | 48 29 75 00             |
    | sub qword [rsi], rdi                        | 48 29 3e                |
    | sub qword [rdi], r8                         | 4c 29 07                |
    | sub qword [r8], r9                          | 4d 29 08                |
    | sub qword [r9], r10                         | 4d 29 11                |
    | sub qword [r10], r11                        | 4d 29 1a                |
    | sub qword [r11], r12                        | 4d 29 23                |
    | sub qword [r12], r13                        | 4d 29 2c 24             |
    | sub qword [r13], r14                        | 4d 29 75 00             |
    | sub qword [r14], r15                        | 4d 29 3e                |
    | sub qword [r15], rax                        | 49 29 07                |
    | sub qword [rcx + 1 * rcx], rdx              | 48 29 14 09             |
    | sub qword [rdx + 1 * rcx], rbx              | 48 29 1c 0a             |
    | sub qword [rbx + 1 * rcx], rsp              | 48 29 24 0b             |
    | sub qword [rsp + 1 * rcx], rbp              | 48 29 2c 0c             |
    | sub qword [rbp + 1 * rcx], rsi              | 48 29 74 0d 00          |
    | sub qword [rsi + 1 * rcx], rdi              | 48 29 3c 0e             |
    | sub qword [rdi + 1 * rcx], r8               | 4c 29 04 0f             |
    | sub qword [r8 + 1 * rcx], r9                | 4d 29 0c 08             |
    | sub qword [r9 + 1 * rcx], r10               | 4d 29 14 09             |
    | sub qword [r10 + 1 * rcx], r11              | 4d 29 1c 0a             |
    | sub qword [r11 + 1 * rcx], r12              | 4d 29 24 0b             |
    | sub qword [r12 + 1 * rcx], r13              | 4d 29 2c 0c             |
    | sub qword [r13 + 1 * rcx], r14              | 4d 29 74 0d 00          |
    | sub qword [r14 + 1 * rcx], r15              | 4d 29 3c 0e             |
    | sub qword [r15 + 1 * rcx], rax              | 49 29 04 0f             |
    | sub qword [rax + 1 * rdx], rdx              | 48 29 14 10             |
    | sub qword [rax + 1 * rbx], rbx              | 48 29 1c 18             |
    | sub qword [rax + 1 * rbp], rsp              | 48 29 24 28             |
    | sub qword [rax + 1 * rsi], rbp              | 48 29 2c 30             |
    | sub qword [rax + 1 * rdi], rsi              | 48 29 34 38             |
    | sub qword [rax + 1 * r8], rdi               | 4a 29 3c 00             |
    | sub qword [rax + 1 * r9], r8                | 4e 29 04 08             |
    | sub qword [rax + 1 * r10], r9               | 4e 29 0c 10             |
    | sub qword [rax + 1 * r11], r10              | 4e 29 14 18             |
    | sub qword [rax + 1 * r12], r11              | 4e 29 1c 20             |
    | sub qword [rax + 1 * r13], r12              | 4e 29 24 28             |
    | sub qword [rax + 1 * r14], r13              | 4e 29 2c 30             |
    | sub qword [rax + 1 * r15], r14              | 4e 29 34 38             |
    | sub qword [rax + 2 * rcx], r15              | 4c 29 3c 48             |
    | sub qword [rax + 4 * rcx], rax              | 48 29 04 88             |
    | sub qword [r8 + 1 * r9], rdx                | 4b 29 14 08             |
    | sub qword [r8 + 2 * r9], rbx                | 4b 29 1c 48             |
    | sub qword [r8 + 4 * r9], rsp                | 4b 29 24 88             |
    | sub qword [r8 + 8 * r9], rbp                | 4b 29 2c c8             |
    | sub qword [1 * rcx], rsi                    | 48 29 34 0d 00 00 00 00 |
    | sub qword [2 * rcx], rdi                    | 48 29 3c 4d 00 00 00 00 |
    | sub qword [4 * rcx], r8                     | 4c 29 04 8d 00 00 00 00 |
    | sub qword [8 * rcx], r9                     | 4c 29 0c cd 00 00 00 00 |
    | sub qword [1 * r9], r10                     | 4e 29 14 0d 00 00 00 00 |
    | sub qword [2 * r9], r11                     | 4e 29 1c 4d 00 00 00 00 |
    | sub qword [4 * r9], r12                     | 4e 29 24 8d 00 00 00 00 |
    | sub qword [8 * r9], r13                     | 4e 29 2c cd 00 00 00 00 |
    | sub qword [r13 + 8 * r12], r14              | 4f 29 74 e5 00          |
    | sub qword [rsp + 4 * r15], r15              | 4e 29 3c bc             |
    | sub qword [rax + 1 * rcx + 0x00], rax       | 48 29 44 08 00          |
    | sub qword [rax + 1 * rcx + 0x01], rdx       | 48 29 54 08 01          |
    | sub qword [rax + 1 * rcx - 0x01], rbx       | 48 29 5c 08 ff          |
    | sub qword [rax + 1 * rcx + 0x00000001], rsp | 48 29 a4 08 01 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x00000001], rbp | 48 29 ac 08 ff ff ff ff |
    | sub qword [rax + 1 * rcx + 0x7f], rsi       | 48 29 74 08 7f          |
    | sub qword [rax + 1 * rcx - 0x7f], rdi       | 48 29 7c 08 81          |
    | sub qword [rax + 1 * rcx + 0x80], r8        | 4c 29 84 08 80 00 00 00 |
    | sub qword [rax + 1 * rcx - 0x80], r9        | 4c 29 4c 08 80          |
    | sub qword [rax + 1 * rcx - 0x81], r10       | 4c 29 94 08 7f ff ff ff |
    | sub qword [rax + 1 * rcx + 0xff], r11       | 4c 29 9c 08 ff 00 00 00 |
    | sub qword [rax + 1 * rcx - 0xff], r12       | 4c 29 a4 08 01 ff ff ff |
    | sub qword [rax + 1 * rcx + 0x7fffffff], r13 | 4c 29 ac 08 ff ff ff 7f |
    | sub qword [rax + 1 * rcx - 0x7fffffff], r14 | 4c 29 b4 08 01 00 00 80 |
    | sub qword [rax + 1 * rcx - 0x80000000], r15 | 4c 29 bc 08 00 00 00 80 |
    | sub qword [r10 + 0x7f], rax                 | 49 29 42 7f             |
    | sub qword [r10 - 0x80], rdx                 | 49 29 52 80             |
    | sub qword [r10 - 0x81], rbx                 | 49 29 9a 7f ff ff ff    |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_sub_addr64_reg64():
    encode(SUB_ADDR64_REG64)


SUB_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sub dword [rax], 0x01                        | 83 28 01                   |
    | sub dword [rcx], 0x01                        | 83 29 01                   |
    | sub dword [rdx], 0x01                        | 83 2a 01                   |
    | sub dword [rbx], 0x01                        | 83 2b 01                   |
    | sub dword [rsp], 0x01                        | 83 2c 24 01                |
    | sub dword [rbp], 0x01                        | 83 6d 00 01                |
    | sub dword [rsi], 0x01                        | 83 2e 01                   |
    | sub dword [rdi], 0x01                        | 83 2f 01                   |
    | sub dword [r8], 0x01                         | 41 83 28 01                |
    | sub dword [r9], 0x01                         | 41 83 29 01                |
    | sub dword [r10], 0x01                        | 41 83 2a 01                |
    | sub dword [r11], 0x01                        | 41 83 2b 01                |
    | sub dword [r12], 0x01                        | 41 83 2c 24 01             |
    | sub dword [r13], 0x01                        | 41 83 6d 00 01             |
    | sub dword [r14], 0x01                        | 41 83 2e 01                |
    | sub dword [r15], 0x01                        | 41 83 2f 01                |
    | sub dword [rax + 1 * rcx], 0x01              | 83 2c 08 01                |
    | sub dword [rcx + 1 * rcx], 0x01              | 83 2c 09 01                |
    | sub dword [rdx + 1 * rcx], 0x01              | 83 2c 0a 01                |
    | sub dword [rbx + 1 * rcx], 0x01              | 83 2c 0b 01                |
    | sub dword [rsp + 1 * rcx], 0x01              | 83 2c 0c 01                |
    | sub dword [rbp + 1 * rcx], 0x01              | 83 6c 0d 00 01             |
    | sub dword [rsi + 1 * rcx], 0x01              | 83 2c 0e 01                |
    | sub dword [rdi + 1 * rcx], 0x01              | 83 2c 0f 01                |
    | sub dword [r8 + 1 * rcx], 0x01               | 41 83 2c 08 01             |
    | sub dword [r9 + 1 * rcx], 0x01               | 41 83 2c 09 01             |
    | sub dword [r10 + 1 * rcx], 0x01              | 41 83 2c 0a 01             |
    | sub dword [r11 + 1 * rcx], 0x01              | 41 83 2c 0b 01             |
    | sub dword [r12 + 1 * rcx], 0x01              | 41 83 2c 0c 01             |
    | sub dword [r13 + 1 * rcx], 0x01              | 41 83 6c 0d 00 01          |
    | sub dword [r14 + 1 * rcx], 0x01              | 41 83 2c 0e 01             |
    | sub dword [r15 + 1 * rcx], 0x01              | 41 83 2c 0f 01             |
    | sub dword [rax + 1 * rax], 0x01              | 83 2c 00 01                |
    | sub dword [rax + 1 * rdx], 0x01              | 83 2c 10 01                |
    | sub dword [rax + 1 * rbx], 0x01              | 83 2c 18 01                |
    | sub dword [rax + 1 * rbp], 0x01              | 83 2c 28 01                |
    | sub dword [rax + 1 * rsi], 0x01              | 83 2c 30 01                |
    | sub dword [rax + 1 * rdi], 0x01              | 83 2c 38 01                |
    | sub dword [rax + 1 * r8], 0x01               | 42 83 2c 00 01             |
    | sub dword [rax + 1 * r9], 0x01               | 42 83 2c 08 01             |
    | sub dword [rax + 1 * r10], 0x01              | 42 83 2c 10 01             |
    | sub dword [rax + 1 * r11], 0x01              | 42 83 2c 18 01             |
    | sub dword [rax + 1 * r12], 0x01              | 42 83 2c 20 01             |
    | sub dword [rax + 1 * r13], 0x01              | 42 83 2c 28 01             |
    | sub dword [rax + 1 * r14], 0x01              | 42 83 2c 30 01             |
    | sub dword [rax + 1 * r15], 0x01              | 42 83 2c 38 01             |
    | sub dword [rax + 2 * rcx], 0x01              | 83 2c 48 01                |
    | sub dword [rax + 4 * rcx], 0x01              | 83 2c 88 01                |
    | sub dword [rax + 8 * rcx], 0x01              | 83 2c c8 01                |
    | sub dword [r8 + 1 * r9], 0x01                | 43 83 2c 08 01             |
    | sub dword [r8 + 2 * r9], 0x01                | 43 83 2c 48 01             |
    | sub dword [r8 + 4 * r9], 0x01                | 43 83 2c 88 01             |
    | sub dword [r8 + 8 * r9], 0x01                | 43 83 2c c8 01             |
    | sub dword [1 * rcx], 0x01                    | 83 2c 0d 00 00 00 00 01    |
    | sub dword [2 * rcx], 0x01                    | 83 2c 4d 00 00 00 00 01    |
    | sub dword [4 * rcx], 0x01                    | 83 2c 8d 00 00 00 00 01    |
    | sub dword [8 * rcx], 0x01                    | 83 2c cd 00 00 00 00 01    |
    | sub dword [1 * r9], 0x01                     | 42 83 2c 0d 00 00 00 00 01 |
    | sub dword [2 * r9], 0x01                     | 42 83 2c 4d 00 00 00 00 01 |
    | sub dword [4 * r9], 0x01                     | 42 83 2c 8d 00 00 00 00 01 |
    | sub dword [8 * r9], 0x01                     | 42 83 2c cd 00 00 00 00 01 |
    | sub dword [r13 + 8 * r12], 0x01              | 43 83 6c e5 00 01          |
    | sub dword [rsp + 4 * r15], 0x01              | 42 83 2c bc 01             |
    | sub dword [rax + 1 * rcx + 0x00], 0x01       | 83 6c 08 00 01             |
    | sub dword [rax + 1 * rcx - 0x00], 0x01       | 83 6c 08 00 01             |
    | sub dword [rax + 1 * rcx + 0x01], 0x01       | 83 6c 08 01 01             |
    | sub dword [rax + 1 * rcx - 0x01], 0x01       | 83 6c 08 ff 01             |
    | sub dword [rax + 1 * rcx + 0x00000001], 0x01 | 83 ac 08 01 00 00 00 01    |
    | sub dword [rax + 1 * rcx - 0x00000001], 0x01 | 83 ac 08 ff ff ff ff 01    |
    | sub dword [rax + 1 * rcx + 0x7f], 0x01       | 83 6c 08 7f 01             |
    | sub dword [rax + 1 * rcx - 0x7f], 0x01       | 83 6c 08 81 01             |
    | sub dword [rax + 1 * rcx + 0x80], 0x01       | 83 ac 08 80 00 00 00 01    |
    | sub dword [rax + 1 * rcx - 0x80], 0x01       | 83 6c 08 80 01             |
    | sub dword [rax + 1 * rcx - 0x81], 0x01       | 83 ac 08 7f ff ff ff 01    |
    | sub dword [rax + 1 * rcx + 0xff], 0x01       | 83 ac 08 ff 00 00 00 01    |
    | sub dword [rax + 1 * rcx - 0xff], 0x01       | 83 ac 08 01 ff ff ff 01    |
    | sub dword [rax + 1 * rcx + 0x7fffffff], 0x01 | 83 ac 08 ff ff ff 7f 01    |
    | sub dword [rax + 1 * rcx - 0x7fffffff], 0x01 | 83 ac 08 01 00 00 80 01    |
    | sub dword [rax + 1 * rcx - 0x80000000], 0x01 | 83 ac 08 00 00 00 80 01    |
    | sub dword [r10 + 0x7f], 0x01                 | 41 83 6a 7f 01             |
    | sub dword [r10 + 0x80], 0x01                 | 41 83 aa 80 00 00 00 01    |
    | sub dword [r10 - 0x80], 0x01                 | 41 83 6a 80 01             |
    | sub dword [r10 - 0x81], 0x01                 | 41 83 aa 7f ff ff ff 01    |
    | sub dword [rax], 0x00                        | 83 28 00                   |
    | sub dword [rax], 0x7f                        | 83 28 7f                   |
    | sub dword [rax], 0x80                        | 83 28 80                   |
    | sub dword [rax], 0xff                        | 83 28 ff                   |
    | sub dword [rcx], 0x7f                        | 83 29 7f                   |
    | sub dword [rdx], 0x80                        | 83 2a 80                   |
    | sub dword [rbx], 0xff                        | 83 2b ff                   |
    | sub dword [rsp], 0x00                        | 83 2c 24 00                |
    | sub dword [rsi], 0x7f                        | 83 2e 7f                   |
    | sub dword [rdi], 0x80                        | 83 2f 80                   |
    | sub dword [r8], 0xff                         | 41 83 28 ff                |
    | sub dword [r9], 0x00                         | 41 83 29 00                |
    | sub dword [r11], 0x7f                        | 41 83 2b 7f                |
    | sub dword [r12], 0x80                        | 41 83 2c 24 80             |
    | sub dword [r13], 0xff                        | 41 83 6d 00 ff             |
    | sub dword [r14], 0x00                        | 41 83 2e 00                |
    | sub dword [rax + 1 * rcx], 0x7f              | 83 2c 08 7f                |
    | sub dword [rcx + 1 * rcx], 0x80              | 83 2c 09 80                |
    | sub dword [rdx + 1 * rcx], 0xff              | 83 2c 0a ff                |
    | sub dword [rbx + 1 * rcx], 0x00              | 83 2c 0b 00                |
    | sub dword [rbp + 1 * rcx], 0x7f              | 83 6c 0d 00 7f             |
    | sub dword [rsi + 1 * rcx], 0x80              | 83 2c 0e 80                |
    | sub dword [rdi + 1 * rcx], 0xff              | 83 2c 0f ff                |
    | sub dword [r8 + 1 * rcx], 0x00               | 41 83 2c 08 00             |
    | sub dword [r10 + 1 * rcx], 0x7f              | 41 83 2c 0a 7f             |
    | sub dword [r11 + 1 * rcx], 0x80              | 41 83 2c 0b 80             |
    | sub dword [r12 + 1 * rcx], 0xff              | 41 83 2c 0c ff             |
    | sub dword [r13 + 1 * rcx], 0x00              | 41 83 6c 0d 00 00          |
    | sub dword [r15 + 1 * rcx], 0x7f              | 41 83 2c 0f 7f             |
    | sub dword [rax + 1 * rax], 0x80              | 83 2c 00 80                |
    | sub dword [rax + 1 * rdx], 0xff              | 83 2c 10 ff                |
    | sub dword [rax + 1 * rbx], 0x00              | 83 2c 18 00                |
    | sub dword [rax + 1 * rsi], 0x7f              | 83 2c 30 7f                |
    | sub dword [rax + 1 * rdi], 0x80              | 83 2c 38 80                |
    | sub dword [rax + 1 * r8], 0xff               | 42 83 2c 00 ff             |
    | sub dword [rax + 1 * r9], 0x00               | 42 83 2c 08 00             |
    | sub dword [rax + 1 * r11], 0x7f              | 42 83 2c 18 7f             |
    | sub dword [rax + 1 * r12], 0x80              | 42 83 2c 20 80             |
    | sub dword [rax + 1 * r13], 0xff              | 42 83 2c 28 ff             |
    | sub dword [rax + 1 * r14], 0x00              | 42 83 2c 30 00             |
    | sub dword [rax + 2 * rcx], 0x7f              | 83 2c 48 7f                |
    | sub dword [rax + 4 * rcx], 0x80              | 83 2c 88 80                |
    | sub dword [rax + 8 * rcx], 0xff              | 83 2c c8 ff                |
    | sub dword [r8 + 1 * r9], 0x00                | 43 83 2c 08 00             |
    | sub dword [r8 + 4 * r9], 0x7f                | 43 83 2c 88 7f             |
    | sub dword [r8 + 8 * r9], 0x80                | 43 83 2c c8 80             |
    | sub dword [1 * rcx], 0xff                    | 83 2c 0d 00 00 00 00 ff    |
    | sub dword [2 * rcx], 0x00                    | 83 2c 4d 00 00 00 00 00    |
    | sub dword [8 * rcx], 0x7f                    | 83 2c cd 00 00 00 00 7f    |
    | sub dword [1 * r9], 0x80                     | 42 83 2c 0d 00 00 00 00 80 |
    | sub dword [2 * r9], 0xff                     | 42 83 2c 4d 00 00 00 00 ff |
    | sub dword [4 * r9], 0x00                     | 42 83 2c 8d 00 00 00 00 00 |
    | sub dword [r13 + 8 * r12], 0x7f              | 43 83 6c e5 00 7f          |
    | sub dword [rsp + 4 * r15], 0x80              | 42 83 2c bc 80             |
    | sub dword [rax + 1 * rcx + 0x00], 0xff       | 83 6c 08 00 ff             |
    | sub dword [rax + 1 * rcx - 0x00], 0x00       | 83 6c 08 00 00             |
    | sub dword [rax + 1 * rcx - 0x01], 0x7f       | 83 6c 08 ff 7f             |
    | sub dword [rax + 1 * rcx + 0x00000001], 0x80 | 83 ac 08 01 00 00 00 80    |
    | sub dword [rax + 1 * rcx - 0x00000001], 0xff | 83 ac 08 ff ff ff ff ff    |
    | sub dword [rax + 1 * rcx + 0x7f], 0x00       | 83 6c 08 7f 00             |
    | sub dword [rax + 1 * rcx + 0x80], 0x7f       | 83 ac 08 80 00 00 00 7f    |
    | sub dword [rax + 1 * rcx - 0x80], 0x80       | 83 6c 08 80 80             |
    | sub dword [rax + 1 * rcx - 0x81], 0xff       | 83 ac 08 7f ff ff ff ff    |
    | sub dword [rax + 1 * rcx + 0xff], 0x00       | 83 ac 08 ff 00 00 00 00    |
    | sub dword [rax + 1 * rcx + 0x7fffffff], 0x7f | 83 ac 08 ff ff ff 7f 7f    |
    | sub dword [rax + 1 * rcx - 0x7fffffff], 0x80 | 83 ac 08 01 00 00 80 80    |
    | sub dword [rax + 1 * rcx - 0x80000000], 0xff | 83 ac 08 00 00 00 80 ff    |
    | sub dword [r10 + 0x7f], 0x00                 | 41 83 6a 7f 00             |
    | sub dword [r10 - 0x80], 0x7f                 | 41 83 6a 80 7f             |
    | sub dword [r10 - 0x81], 0x80                 | 41 83 aa 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sub_addr32_imm8():
    encode(SUB_ADDR32_IMM8)


SUB_ADDR32_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | sub dword [rax], 0x00000001                        | 81 28 01 00 00 00                   |
    | sub dword [rcx], 0x00000001                        | 81 29 01 00 00 00                   |
    | sub dword [rdx], 0x00000001                        | 81 2a 01 00 00 00                   |
    | sub dword [rbx], 0x00000001                        | 81 2b 01 00 00 00                   |
    | sub dword [rsp], 0x00000001                        | 81 2c 24 01 00 00 00                |
    | sub dword [rbp], 0x00000001                        | 81 6d 00 01 00 00 00                |
    | sub dword [rsi], 0x00000001                        | 81 2e 01 00 00 00                   |
    | sub dword [rdi], 0x00000001                        | 81 2f 01 00 00 00                   |
    | sub dword [r8], 0x00000001                         | 41 81 28 01 00 00 00                |
    | sub dword [r9], 0x00000001                         | 41 81 29 01 00 00 00                |
    | sub dword [r10], 0x00000001                        | 41 81 2a 01 00 00 00                |
    | sub dword [r11], 0x00000001                        | 41 81 2b 01 00 00 00                |
    | sub dword [r12], 0x00000001                        | 41 81 2c 24 01 00 00 00             |
    | sub dword [r13], 0x00000001                        | 41 81 6d 00 01 00 00 00             |
    | sub dword [r14], 0x00000001                        | 41 81 2e 01 00 00 00                |
    | sub dword [r15], 0x00000001                        | 41 81 2f 01 00 00 00                |
    | sub dword [rax + 1 * rcx], 0x00000001              | 81 2c 08 01 00 00 00                |
    | sub dword [rcx + 1 * rcx], 0x00000001              | 81 2c 09 01 00 00 00                |
    | sub dword [rdx + 1 * rcx], 0x00000001              | 81 2c 0a 01 00 00 00                |
    | sub dword [rbx + 1 * rcx], 0x00000001              | 81 2c 0b 01 00 00 00                |
    | sub dword [rsp + 1 * rcx], 0x00000001              | 81 2c 0c 01 00 00 00                |
    | sub dword [rbp + 1 * rcx], 0x00000001              | 81 6c 0d 00 01 00 00 00             |
    | sub dword [rsi + 1 * rcx], 0x00000001              | 81 2c 0e 01 00 00 00                |
    | sub dword [rdi + 1 * rcx], 0x00000001              | 81 2c 0f 01 00 00 00                |
    | sub dword [r8 + 1 * rcx], 0x00000001               | 41 81 2c 08 01 00 00 00             |
    | sub dword [r9 + 1 * rcx], 0x00000001               | 41 81 2c 09 01 00 00 00             |
    | sub dword [r10 + 1 * rcx], 0x00000001              | 41 81 2c 0a 01 00 00 00             |
    | sub dword [r11 + 1 * rcx], 0x00000001              | 41 81 2c 0b 01 00 00 00             |
    | sub dword [r12 + 1 * rcx], 0x00000001              | 41 81 2c 0c 01 00 00 00             |
    | sub dword [r13 + 1 * rcx], 0x00000001              | 41 81 6c 0d 00 01 00 00 00          |
    | sub dword [r14 + 1 * rcx], 0x00000001              | 41 81 2c 0e 01 00 00 00             |
    | sub dword [r15 + 1 * rcx], 0x00000001              | 41 81 2c 0f 01 00 00 00             |
    | sub dword [rax + 1 * rax], 0x00000001              | 81 2c 00 01 00 00 00                |
    | sub dword [rax + 1 * rdx], 0x00000001              | 81 2c 10 01 00 00 00                |
    | sub dword [rax + 1 * rbx], 0x00000001              | 81 2c 18 01 00 00 00                |
    | sub dword [rax + 1 * rbp], 0x00000001              | 81 2c 28 01 00 00 00                |
    | sub dword [rax + 1 * rsi], 0x00000001              | 81 2c 30 01 00 00 00                |
    | sub dword [rax + 1 * rdi], 0x00000001              | 81 2c 38 01 00 00 00                |
    | sub dword [rax + 1 * r8], 0x00000001               | 42 81 2c 00 01 00 00 00             |
    | sub dword [rax + 1 * r9], 0x00000001               | 42 81 2c 08 01 00 00 00             |
    | sub dword [rax + 1 * r10], 0x00000001              | 42 81 2c 10 01 00 00 00             |
    | sub dword [rax + 1 * r11], 0x00000001              | 42 81 2c 18 01 00 00 00             |
    | sub dword [rax + 1 * r12], 0x00000001              | 42 81 2c 20 01 00 00 00             |
    | sub dword [rax + 1 * r13], 0x00000001              | 42 81 2c 28 01 00 00 00             |
    | sub dword [rax + 1 * r14], 0x00000001              | 42 81 2c 30 01 00 00 00             |
    | sub dword [rax + 1 * r15], 0x00000001              | 42 81 2c 38 01 00 00 00             |
    | sub dword [rax + 2 * rcx], 0x00000001              | 81 2c 48 01 00 00 00                |
    | sub dword [rax + 4 * rcx], 0x00000001              | 81 2c 88 01 00 00 00                |
    | sub dword [rax + 8 * rcx], 0x00000001              | 81 2c c8 01 00 00 00                |
    | sub dword [r8 + 1 * r9], 0x00000001                | 43 81 2c 08 01 00 00 00             |
    | sub dword [r8 + 2 * r9], 0x00000001                | 43 81 2c 48 01 00 00 00             |
    | sub dword [r8 + 4 * r9], 0x00000001                | 43 81 2c 88 01 00 00 00             |
    | sub dword [r8 + 8 * r9], 0x00000001                | 43 81 2c c8 01 00 00 00             |
    | sub dword [1 * rcx], 0x00000001                    | 81 2c 0d 00 00 00 00 01 00 00 00    |
    | sub dword [2 * rcx], 0x00000001                    | 81 2c 4d 00 00 00 00 01 00 00 00    |
    | sub dword [4 * rcx], 0x00000001                    | 81 2c 8d 00 00 00 00 01 00 00 00    |
    | sub dword [8 * rcx], 0x00000001                    | 81 2c cd 00 00 00 00 01 00 00 00    |
    | sub dword [1 * r9], 0x00000001                     | 42 81 2c 0d 00 00 00 00 01 00 00 00 |
    | sub dword [2 * r9], 0x00000001                     | 42 81 2c 4d 00 00 00 00 01 00 00 00 |
    | sub dword [4 * r9], 0x00000001                     | 42 81 2c 8d 00 00 00 00 01 00 00 00 |
    | sub dword [8 * r9], 0x00000001                     | 42 81 2c cd 00 00 00 00 01 00 00 00 |
    | sub dword [r13 + 8 * r12], 0x00000001              | 43 81 6c e5 00 01 00 00 00          |
    | sub dword [rsp + 4 * r15], 0x00000001              | 42 81 2c bc 01 00 00 00             |
    | sub dword [rax + 1 * rcx + 0x00], 0x00000001       | 81 6c 08 00 01 00 00 00             |
    | sub dword [rax + 1 * rcx - 0x00], 0x00000001       | 81 6c 08 00 01 00 00 00             |
    | sub dword [rax + 1 * rcx + 0x01], 0x00000001       | 81 6c 08 01 01 00 00 00             |
    | sub dword [rax + 1 * rcx - 0x01], 0x00000001       | 81 6c 08 ff 01 00 00 00             |
    | sub dword [rax + 1 * rcx + 0x00000001], 0x00000001 | 81 ac 08 01 00 00 00 01 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x00000001], 0x00000001 | 81 ac 08 ff ff ff ff 01 00 00 00    |
    | sub dword [rax + 1 * rcx + 0x7f], 0x00000001       | 81 6c 08 7f 01 00 00 00             |
    | sub dword [rax + 1 * rcx - 0x7f], 0x00000001       | 81 6c 08 81 01 00 00 00             |
    | sub dword [rax + 1 * rcx + 0x80], 0x00000001       | 81 ac 08 80 00 00 00 01 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x80], 0x00000001       | 81 6c 08 80 01 00 00 00             |
    | sub dword [rax + 1 * rcx - 0x81], 0x00000001       | 81 ac 08 7f ff ff ff 01 00 00 00    |
    | sub dword [rax + 1 * rcx + 0xff], 0x00000001       | 81 ac 08 ff 00 00 00 01 00 00 00    |
    | sub dword [rax + 1 * rcx - 0xff], 0x00000001       | 81 ac 08 01 ff ff ff 01 00 00 00    |
    | sub dword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 81 ac 08 ff ff ff 7f 01 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 81 ac 08 01 00 00 80 01 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x80000000], 0x00000001 | 81 ac 08 00 00 00 80 01 00 00 00    |
    | sub dword [r10 + 0x7f], 0x00000001                 | 41 81 6a 7f 01 00 00 00             |
    | sub dword [r10 + 0x80], 0x00000001                 | 41 81 aa 80 00 00 00 01 00 00 00    |
    | sub dword [r10 - 0x80], 0x00000001                 | 41 81 6a 80 01 00 00 00             |
    | sub dword [r10 - 0x81], 0x00000001                 | 41 81 aa 7f ff ff ff 01 00 00 00    |
    | sub dword [rax], 0x00000000                        | 81 28 00 00 00 00                   |
    | sub dword [rax], 0x0000007f                        | 81 28 7f 00 00 00                   |
    | sub dword [rax], 0x00000080                        | 81 28 80 00 00 00                   |
    | sub dword [rax], 0x000000ff                        | 81 28 ff 00 00 00                   |
    | sub dword [rax], 0x00000100                        | 81 28 00 01 00 00                   |
    | sub dword [rax], 0x00007fff                        | 81 28 ff 7f 00 00                   |
    | sub dword [rax], 0x00008000                        | 81 28 00 80 00 00                   |
    | sub dword [rax], 0x0000ffff                        | 81 28 ff ff 00 00                   |
    | sub dword [rax], 0x00010000                        | 81 28 00 00 01 00                   |
    | sub dword [rax], 0x7fffffff                        | 81 28 ff ff ff 7f                   |
    | sub dword [rax], 0x80000000                        | 81 28 00 00 00 80                   |
    | sub dword [rax], 0xffffffff                        | 81 28 ff ff ff ff                   |
    | sub dword [rcx], 0x0000007f                        | 81 29 7f 00 00 00                   |
    | sub dword [rdx], 0x00000080                        | 81 2a 80 00 00 00                   |
    | sub dword [rbx], 0x000000ff                        | 81 2b ff 00 00 00                   |
    | sub dword [rsp], 0x00000100                        | 81 2c 24 00 01 00 00                |
    | sub dword [rbp], 0x00007fff                        | 81 6d 00 ff 7f 00 00                |
    | sub dword [rsi], 0x00008000                        | 81 2e 00 80 00 00                   |
    | sub dword [rdi], 0x0000ffff                        | 81 2f ff ff 00 00                   |
    | sub dword [r8], 0x00010000                         | 41 81 28 00 00 01 00                |
    | sub dword [r9], 0x7fffffff                         | 41 81 29 ff ff ff 7f                |
    | sub dword [r10], 0x80000000                        | 41 81 2a 00 00 00 80                |
    | sub dword [r11], 0xffffffff                        | 41 81 2b ff ff ff ff                |
    | sub dword [r12], 0x00000000                        | 41 81 2c 24 00 00 00 00             |
    | sub dword [r14], 0x0000007f                        | 41 81 2e 7f 00 00 00                |
    | sub dword [r15], 0x00000080                        | 41 81 2f 80 00 00 00                |
    | sub dword [rax + 1 * rcx], 0x000000ff              | 81 2c 08 ff 00 00 00                |
    | sub dword [rcx + 1 * rcx], 0x00000100              | 81 2c 09 00 01 00 00                |
    | sub dword [rdx + 1 * rcx], 0x00007fff              | 81 2c 0a ff 7f 00 00                |
    | sub dword [rbx + 1 * rcx], 0x00008000              | 81 2c 0b 00 80 00 00                |
    | sub dword [rsp + 1 * rcx], 0x0000ffff              | 81 2c 0c ff ff 00 00                |
    | sub dword [rbp + 1 * rcx], 0x00010000              | 81 6c 0d 00 00 00 01 00             |
    | sub dword [rsi + 1 * rcx], 0x7fffffff              | 81 2c 0e ff ff ff 7f                |
    | sub dword [rdi + 1 * rcx], 0x80000000              | 81 2c 0f 00 00 00 80                |
    | sub dword [r8 + 1 * rcx], 0xffffffff               | 41 81 2c 08 ff ff ff ff             |
    | sub dword [r9 + 1 * rcx], 0x00000000               | 41 81 2c 09 00 00 00 00             |
    | sub dword [r11 + 1 * rcx], 0x0000007f              | 41 81 2c 0b 7f 00 00 00             |
    | sub dword [r12 + 1 * rcx], 0x00000080              | 41 81 2c 0c 80 00 00 00             |
    | sub dword [r13 + 1 * rcx], 0x000000ff              | 41 81 6c 0d 00 ff 00 00 00          |
    | sub dword [r14 + 1 * rcx], 0x00000100              | 41 81 2c 0e 00 01 00 00             |
    | sub dword [r15 + 1 * rcx], 0x00007fff              | 41 81 2c 0f ff 7f 00 00             |
    | sub dword [rax + 1 * rax], 0x00008000              | 81 2c 00 00 80 00 00                |
    | sub dword [rax + 1 * rdx], 0x0000ffff              | 81 2c 10 ff ff 00 00                |
    | sub dword [rax + 1 * rbx], 0x00010000              | 81 2c 18 00 00 01 00                |
    | sub dword [rax + 1 * rbp], 0x7fffffff              | 81 2c 28 ff ff ff 7f                |
    | sub dword [rax + 1 * rsi], 0x80000000              | 81 2c 30 00 00 00 80                |
    | sub dword [rax + 1 * rdi], 0xffffffff              | 81 2c 38 ff ff ff ff                |
    | sub dword [rax + 1 * r8], 0x00000000               | 42 81 2c 00 00 00 00 00             |
    | sub dword [rax + 1 * r10], 0x0000007f              | 42 81 2c 10 7f 00 00 00             |
    | sub dword [rax + 1 * r11], 0x00000080              | 42 81 2c 18 80 00 00 00             |
    | sub dword [rax + 1 * r12], 0x000000ff              | 42 81 2c 20 ff 00 00 00             |
    | sub dword [rax + 1 * r13], 0x00000100              | 42 81 2c 28 00 01 00 00             |
    | sub dword [rax + 1 * r14], 0x00007fff              | 42 81 2c 30 ff 7f 00 00             |
    | sub dword [rax + 1 * r15], 0x00008000              | 42 81 2c 38 00 80 00 00             |
    | sub dword [rax + 2 * rcx], 0x0000ffff              | 81 2c 48 ff ff 00 00                |
    | sub dword [rax + 4 * rcx], 0x00010000              | 81 2c 88 00 00 01 00                |
    | sub dword [rax + 8 * rcx], 0x7fffffff              | 81 2c c8 ff ff ff 7f                |
    | sub dword [r8 + 1 * r9], 0x80000000                | 43 81 2c 08 00 00 00 80             |
    | sub dword [r8 + 2 * r9], 0xffffffff                | 43 81 2c 48 ff ff ff ff             |
    | sub dword [r8 + 4 * r9], 0x00000000                | 43 81 2c 88 00 00 00 00             |
    | sub dword [1 * rcx], 0x0000007f                    | 81 2c 0d 00 00 00 00 7f 00 00 00    |
    | sub dword [2 * rcx], 0x00000080                    | 81 2c 4d 00 00 00 00 80 00 00 00    |
    | sub dword [4 * rcx], 0x000000ff                    | 81 2c 8d 00 00 00 00 ff 00 00 00    |
    | sub dword [8 * rcx], 0x00000100                    | 81 2c cd 00 00 00 00 00 01 00 00    |
    | sub dword [1 * r9], 0x00007fff                     | 42 81 2c 0d 00 00 00 00 ff 7f 00 00 |
    | sub dword [2 * r9], 0x00008000                     | 42 81 2c 4d 00 00 00 00 00 80 00 00 |
    | sub dword [4 * r9], 0x0000ffff                     | 42 81 2c 8d 00 00 00 00 ff ff 00 00 |
    | sub dword [8 * r9], 0x00010000                     | 42 81 2c cd 00 00 00 00 00 00 01 00 |
    | sub dword [r13 + 8 * r12], 0x7fffffff              | 43 81 6c e5 00 ff ff ff 7f          |
    | sub dword [rsp + 4 * r15], 0x80000000              | 42 81 2c bc 00 00 00 80             |
    | sub dword [rax + 1 * rcx + 0x00], 0xffffffff       | 81 6c 08 00 ff ff ff ff             |
    | sub dword [rax + 1 * rcx - 0x00], 0x00000000       | 81 6c 08 00 00 00 00 00             |
    | sub dword [rax + 1 * rcx - 0x01], 0x0000007f       | 81 6c 08 ff 7f 00 00 00             |
    | sub dword [rax + 1 * rcx + 0x00000001], 0x00000080 | 81 ac 08 01 00 00 00 80 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x00000001], 0x000000ff | 81 ac 08 ff ff ff ff ff 00 00 00    |
    | sub dword [rax + 1 * rcx + 0x7f], 0x00000100       | 81 6c 08 7f 00 01 00 00             |
    | sub dword [rax + 1 * rcx - 0x7f], 0x00007fff       | 81 6c 08 81 ff 7f 00 00             |
    | sub dword [rax + 1 * rcx + 0x80], 0x00008000       | 81 ac 08 80 00 00 00 00 80 00 00    |
    | sub dword [rax + 1 * rcx - 0x80], 0x0000ffff       | 81 6c 08 80 ff ff 00 00             |
    | sub dword [rax + 1 * rcx - 0x81], 0x00010000       | 81 ac 08 7f ff ff ff 00 00 01 00    |
    | sub dword [rax + 1 * rcx + 0xff], 0x7fffffff       | 81 ac 08 ff 00 00 00 ff ff ff 7f    |
    | sub dword [rax + 1 * rcx - 0xff], 0x80000000       | 81 ac 08 01 ff ff ff 00 00 00 80    |
    | sub dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 81 ac 08 ff ff ff 7f ff ff ff ff    |
    | sub dword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 81 ac 08 01 00 00 80 00 00 00 00    |
    | sub dword [r10 + 0x7f], 0x0000007f                 | 41 81 6a 7f 7f 00 00 00             |
    | sub dword [r10 + 0x80], 0x00000080                 | 41 81 aa 80 00 00 00 80 00 00 00    |
    | sub dword [r10 - 0x80], 0x000000ff                 | 41 81 6a 80 ff 00 00 00             |
    | sub dword [r10 - 0x81], 0x00000100                 | 41 81 aa 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_sub_addr32_imm32():
    encode(SUB_ADDR32_IMM32)


SUB_ADDR32_REG32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | sub dword [rax], ecx                         | 29 08                   |
    | sub dword [rcx], ecx                         | 29 09                   |
    | sub dword [rdx], ecx                         | 29 0a                   |
    | sub dword [rbx], ecx                         | 29 0b                   |
    | sub dword [rsp], ecx                         | 29 0c 24                |
    | sub dword [rbp], ecx                         | 29 4d 00                |
    | sub dword [rsi], ecx                         | 29 0e                   |
    | sub dword [rdi], ecx                         | 29 0f                   |
    | sub dword [r8], ecx                          | 41 29 08                |
    | sub dword [r9], ecx                          | 41 29 09                |
    | sub dword [r10], ecx                         | 41 29 0a                |
    | sub dword [r11], ecx                         | 41 29 0b                |
    | sub dword [r12], ecx                         | 41 29 0c 24             |
    | sub dword [r13], ecx                         | 41 29 4d 00             |
    | sub dword [r14], ecx                         | 41 29 0e                |
    | sub dword [r15], ecx                         | 41 29 0f                |
    | sub dword [rax + 1 * rcx], ecx               | 29 0c 08                |
    | sub dword [rcx + 1 * rcx], ecx               | 29 0c 09                |
    | sub dword [rdx + 1 * rcx], ecx               | 29 0c 0a                |
    | sub dword [rbx + 1 * rcx], ecx               | 29 0c 0b                |
    | sub dword [rsp + 1 * rcx], ecx               | 29 0c 0c                |
    | sub dword [rbp + 1 * rcx], ecx               | 29 4c 0d 00             |
    | sub dword [rsi + 1 * rcx], ecx               | 29 0c 0e                |
    | sub dword [rdi + 1 * rcx], ecx               | 29 0c 0f                |
    | sub dword [r8 + 1 * rcx], ecx                | 41 29 0c 08             |
    | sub dword [r9 + 1 * rcx], ecx                | 41 29 0c 09             |
    | sub dword [r10 + 1 * rcx], ecx               | 41 29 0c 0a             |
    | sub dword [r11 + 1 * rcx], ecx               | 41 29 0c 0b             |
    | sub dword [r12 + 1 * rcx], ecx               | 41 29 0c 0c             |
    | sub dword [r13 + 1 * rcx], ecx               | 41 29 4c 0d 00          |
    | sub dword [r14 + 1 * rcx], ecx               | 41 29 0c 0e             |
    | sub dword [r15 + 1 * rcx], ecx               | 41 29 0c 0f             |
    | sub dword [rax + 1 * rax], ecx               | 29 0c 00                |
    | sub dword [rax + 1 * rdx], ecx               | 29 0c 10                |
    | sub dword [rax + 1 * rbx], ecx               | 29 0c 18                |
    | sub dword [rax + 1 * rbp], ecx               | 29 0c 28                |
    | sub dword [rax + 1 * rsi], ecx               | 29 0c 30                |
    | sub dword [rax + 1 * rdi], ecx               | 29 0c 38                |
    | sub dword [rax + 1 * r8], ecx                | 42 29 0c 00             |
    | sub dword [rax + 1 * r9], ecx                | 42 29 0c 08             |
    | sub dword [rax + 1 * r10], ecx               | 42 29 0c 10             |
    | sub dword [rax + 1 * r11], ecx               | 42 29 0c 18             |
    | sub dword [rax + 1 * r12], ecx               | 42 29 0c 20             |
    | sub dword [rax + 1 * r13], ecx               | 42 29 0c 28             |
    | sub dword [rax + 1 * r14], ecx               | 42 29 0c 30             |
    | sub dword [rax + 1 * r15], ecx               | 42 29 0c 38             |
    | sub dword [rax + 2 * rcx], ecx               | 29 0c 48                |
    | sub dword [rax + 4 * rcx], ecx               | 29 0c 88                |
    | sub dword [rax + 8 * rcx], ecx               | 29 0c c8                |
    | sub dword [r8 + 1 * r9], ecx                 | 43 29 0c 08             |
    | sub dword [r8 + 2 * r9], ecx                 | 43 29 0c 48             |
    | sub dword [r8 + 4 * r9], ecx                 | 43 29 0c 88             |
    | sub dword [r8 + 8 * r9], ecx                 | 43 29 0c c8             |
    | sub dword [1 * rcx], ecx                     | 29 0c 0d 00 00 00 00    |
    | sub dword [2 * rcx], ecx                     | 29 0c 4d 00 00 00 00    |
    | sub dword [4 * rcx], ecx                     | 29 0c 8d 00 00 00 00    |
    | sub dword [8 * rcx], ecx                     | 29 0c cd 00 00 00 00    |
    | sub dword [1 * r9], ecx                      | 42 29 0c 0d 00 00 00 00 |
    | sub dword [2 * r9], ecx                      | 42 29 0c 4d 00 00 00 00 |
    | sub dword [4 * r9], ecx                      | 42 29 0c 8d 00 00 00 00 |
    | sub dword [8 * r9], ecx                      | 42 29 0c cd 00 00 00 00 |
    | sub dword [r13 + 8 * r12], ecx               | 43 29 4c e5 00          |
    | sub dword [rsp + 4 * r15], ecx               | 42 29 0c bc             |
    | sub dword [rax + 1 * rcx + 0x00], ecx        | 29 4c 08 00             |
    | sub dword [rax + 1 * rcx - 0x00], ecx        | 29 4c 08 00             |
    | sub dword [rax + 1 * rcx + 0x01], ecx        | 29 4c 08 01             |
    | sub dword [rax + 1 * rcx - 0x01], ecx        | 29 4c 08 ff             |
    | sub dword [rax + 1 * rcx + 0x00000001], ecx  | 29 8c 08 01 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x00000001], ecx  | 29 8c 08 ff ff ff ff    |
    | sub dword [rax + 1 * rcx + 0x7f], ecx        | 29 4c 08 7f             |
    | sub dword [rax + 1 * rcx - 0x7f], ecx        | 29 4c 08 81             |
    | sub dword [rax + 1 * rcx + 0x80], ecx        | 29 8c 08 80 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x80], ecx        | 29 4c 08 80             |
    | sub dword [rax + 1 * rcx - 0x81], ecx        | 29 8c 08 7f ff ff ff    |
    | sub dword [rax + 1 * rcx + 0xff], ecx        | 29 8c 08 ff 00 00 00    |
    | sub dword [rax + 1 * rcx - 0xff], ecx        | 29 8c 08 01 ff ff ff    |
    | sub dword [rax + 1 * rcx + 0x7fffffff], ecx  | 29 8c 08 ff ff ff 7f    |
    | sub dword [rax + 1 * rcx - 0x7fffffff], ecx  | 29 8c 08 01 00 00 80    |
    | sub dword [rax + 1 * rcx - 0x80000000], ecx  | 29 8c 08 00 00 00 80    |
    | sub dword [r10 + 0x7f], ecx                  | 41 29 4a 7f             |
    | sub dword [r10 + 0x80], ecx                  | 41 29 8a 80 00 00 00    |
    | sub dword [r10 - 0x80], ecx                  | 41 29 4a 80             |
    | sub dword [r10 - 0x81], ecx                  | 41 29 8a 7f ff ff ff    |
    | sub dword [rax], eax                         | 29 00                   |
    | sub dword [rax], edx                         | 29 10                   |
    | sub dword [rax], ebx                         | 29 18                   |
    | sub dword [rax], esp                         | 29 20                   |
    | sub dword [rax], ebp                         | 29 28                   |
    | sub dword [rax], esi                         | 29 30                   |
    | sub dword [rax], edi                         | 29 38                   |
    | sub dword [rax], r8d                         | 44 29 00                |
    | sub dword [rax], r9d                         | 44 29 08                |
    | sub dword [rax], r10d                        | 44 29 10                |
    | sub dword [rax], r11d                        | 44 29 18                |
    | sub dword [rax], r12d                        | 44 29 20                |
    | sub dword [rax], r13d                        | 44 29 28                |
    | sub dword [rax], r14d                        | 44 29 30                |
    | sub dword [rax], r15d                        | 44 29 38                |
    | sub dword [rcx], edx                         | 29 11                   |
    | sub dword [rdx], ebx                         | 29 1a                   |
    | sub dword [rbx], esp                         | 29 23                   |
    | sub dword [rsp], ebp                         | 29 2c 24                |
    | sub dword [rbp], esi                         | 29 75 00                |
    | sub dword [rsi], edi                         | 29 3e                   |
    | sub dword [rdi], r8d                         | 44 29 07                |
    | sub dword [r8], r9d                          | 45 29 08                |
    | sub dword [r9], r10d                         | 45 29 11                |
    | sub dword [r10], r11d                        | 45 29 1a                |
    | sub dword [r11], r12d                        | 45 29 23                |
    | sub dword [r12], r13d                        | 45 29 2c 24             |
    | sub dword [r13], r14d                        | 45 29 75 00             |
    | sub dword [r14], r15d                        | 45 29 3e                |
    | sub dword [r15], eax                         | 41 29 07                |
    | sub dword [rcx + 1 * rcx], edx               | 29 14 09                |
    | sub dword [rdx + 1 * rcx], ebx               | 29 1c 0a                |
    | sub dword [rbx + 1 * rcx], esp               | 29 24 0b                |
    | sub dword [rsp + 1 * rcx], ebp               | 29 2c 0c                |
    | sub dword [rbp + 1 * rcx], esi               | 29 74 0d 00             |
    | sub dword [rsi + 1 * rcx], edi               | 29 3c 0e                |
    | sub dword [rdi + 1 * rcx], r8d               | 44 29 04 0f             |
    | sub dword [r8 + 1 * rcx], r9d                | 45 29 0c 08             |
    | sub dword [r9 + 1 * rcx], r10d               | 45 29 14 09             |
    | sub dword [r10 + 1 * rcx], r11d              | 45 29 1c 0a             |
    | sub dword [r11 + 1 * rcx], r12d              | 45 29 24 0b             |
    | sub dword [r12 + 1 * rcx], r13d              | 45 29 2c 0c             |
    | sub dword [r13 + 1 * rcx], r14d              | 45 29 74 0d 00          |
    | sub dword [r14 + 1 * rcx], r15d              | 45 29 3c 0e             |
    | sub dword [r15 + 1 * rcx], eax               | 41 29 04 0f             |
    | sub dword [rax + 1 * rdx], edx               | 29 14 10                |
    | sub dword [rax + 1 * rbx], ebx               | 29 1c 18                |
    | sub dword [rax + 1 * rbp], esp               | 29 24 28                |
    | sub dword [rax + 1 * rsi], ebp               | 29 2c 30                |
    | sub dword [rax + 1 * rdi], esi               | 29 34 38                |
    | sub dword [rax + 1 * r8], edi                | 42 29 3c 00             |
    | sub dword [rax + 1 * r9], r8d                | 46 29 04 08             |
    | sub dword [rax + 1 * r10], r9d               | 46 29 0c 10             |
    | sub dword [rax + 1 * r11], r10d              | 46 29 14 18             |
    | sub dword [rax + 1 * r12], r11d              | 46 29 1c 20             |
    | sub dword [rax + 1 * r13], r12d              | 46 29 24 28             |
    | sub dword [rax + 1 * r14], r13d              | 46 29 2c 30             |
    | sub dword [rax + 1 * r15], r14d              | 46 29 34 38             |
    | sub dword [rax + 2 * rcx], r15d              | 44 29 3c 48             |
    | sub dword [rax + 4 * rcx], eax               | 29 04 88                |
    | sub dword [r8 + 1 * r9], edx                 | 43 29 14 08             |
    | sub dword [r8 + 2 * r9], ebx                 | 43 29 1c 48             |
    | sub dword [r8 + 4 * r9], esp                 | 43 29 24 88             |
    | sub dword [r8 + 8 * r9], ebp                 | 43 29 2c c8             |
    | sub dword [1 * rcx], esi                     | 29 34 0d 00 00 00 00    |
    | sub dword [2 * rcx], edi                     | 29 3c 4d 00 00 00 00    |
    | sub dword [4 * rcx], r8d                     | 44 29 04 8d 00 00 00 00 |
    | sub dword [8 * rcx], r9d                     | 44 29 0c cd 00 00 00 00 |
    | sub dword [1 * r9], r10d                     | 46 29 14 0d 00 00 00 00 |
    | sub dword [2 * r9], r11d                     | 46 29 1c 4d 00 00 00 00 |
    | sub dword [4 * r9], r12d                     | 46 29 24 8d 00 00 00 00 |
    | sub dword [8 * r9], r13d                     | 46 29 2c cd 00 00 00 00 |
    | sub dword [r13 + 8 * r12], r14d              | 47 29 74 e5 00          |
    | sub dword [rsp + 4 * r15], r15d              | 46 29 3c bc             |
    | sub dword [rax + 1 * rcx + 0x00], eax        | 29 44 08 00             |
    | sub dword [rax + 1 * rcx + 0x01], edx        | 29 54 08 01             |
    | sub dword [rax + 1 * rcx - 0x01], ebx        | 29 5c 08 ff             |
    | sub dword [rax + 1 * rcx + 0x00000001], esp  | 29 a4 08 01 00 00 00    |
    | sub dword [rax + 1 * rcx - 0x00000001], ebp  | 29 ac 08 ff ff ff ff    |
    | sub dword [rax + 1 * rcx + 0x7f], esi        | 29 74 08 7f             |
    | sub dword [rax + 1 * rcx - 0x7f], edi        | 29 7c 08 81             |
    | sub dword [rax + 1 * rcx + 0x80], r8d        | 44 29 84 08 80 00 00 00 |
    | sub dword [rax + 1 * rcx - 0x80], r9d        | 44 29 4c 08 80          |
    | sub dword [rax + 1 * rcx - 0x81], r10d       | 44 29 94 08 7f ff ff ff |
    | sub dword [rax + 1 * rcx + 0xff], r11d       | 44 29 9c 08 ff 00 00 00 |
    | sub dword [rax + 1 * rcx - 0xff], r12d       | 44 29 a4 08 01 ff ff ff |
    | sub dword [rax + 1 * rcx + 0x7fffffff], r13d | 44 29 ac 08 ff ff ff 7f |
    | sub dword [rax + 1 * rcx - 0x7fffffff], r14d | 44 29 b4 08 01 00 00 80 |
    | sub dword [rax + 1 * rcx - 0x80000000], r15d | 44 29 bc 08 00 00 00 80 |
    | sub dword [r10 + 0x7f], eax                  | 41 29 42 7f             |
    | sub dword [r10 - 0x80], edx                  | 41 29 52 80             |
    | sub dword [r10 - 0x81], ebx                  | 41 29 9a 7f ff ff ff    |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_sub_addr32_reg32():
    encode(SUB_ADDR32_REG32)


SUB_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | sub word [rax], 0x01                        | 66 83 28 01                   |
    | sub word [rcx], 0x01                        | 66 83 29 01                   |
    | sub word [rdx], 0x01                        | 66 83 2a 01                   |
    | sub word [rbx], 0x01                        | 66 83 2b 01                   |
    | sub word [rsp], 0x01                        | 66 83 2c 24 01                |
    | sub word [rbp], 0x01                        | 66 83 6d 00 01                |
    | sub word [rsi], 0x01                        | 66 83 2e 01                   |
    | sub word [rdi], 0x01                        | 66 83 2f 01                   |
    | sub word [r8], 0x01                         | 66 41 83 28 01                |
    | sub word [r9], 0x01                         | 66 41 83 29 01                |
    | sub word [r10], 0x01                        | 66 41 83 2a 01                |
    | sub word [r11], 0x01                        | 66 41 83 2b 01                |
    | sub word [r12], 0x01                        | 66 41 83 2c 24 01             |
    | sub word [r13], 0x01                        | 66 41 83 6d 00 01             |
    | sub word [r14], 0x01                        | 66 41 83 2e 01                |
    | sub word [r15], 0x01                        | 66 41 83 2f 01                |
    | sub word [rax + 1 * rcx], 0x01              | 66 83 2c 08 01                |
    | sub word [rcx + 1 * rcx], 0x01              | 66 83 2c 09 01                |
    | sub word [rdx + 1 * rcx], 0x01              | 66 83 2c 0a 01                |
    | sub word [rbx + 1 * rcx], 0x01              | 66 83 2c 0b 01                |
    | sub word [rsp + 1 * rcx], 0x01              | 66 83 2c 0c 01                |
    | sub word [rbp + 1 * rcx], 0x01              | 66 83 6c 0d 00 01             |
    | sub word [rsi + 1 * rcx], 0x01              | 66 83 2c 0e 01                |
    | sub word [rdi + 1 * rcx], 0x01              | 66 83 2c 0f 01                |
    | sub word [r8 + 1 * rcx], 0x01               | 66 41 83 2c 08 01             |
    | sub word [r9 + 1 * rcx], 0x01               | 66 41 83 2c 09 01             |
    | sub word [r10 + 1 * rcx], 0x01              | 66 41 83 2c 0a 01             |
    | sub word [r11 + 1 * rcx], 0x01              | 66 41 83 2c 0b 01             |
    | sub word [r12 + 1 * rcx], 0x01              | 66 41 83 2c 0c 01             |
    | sub word [r13 + 1 * rcx], 0x01              | 66 41 83 6c 0d 00 01          |
    | sub word [r14 + 1 * rcx], 0x01              | 66 41 83 2c 0e 01             |
    | sub word [r15 + 1 * rcx], 0x01              | 66 41 83 2c 0f 01             |
    | sub word [rax + 1 * rax], 0x01              | 66 83 2c 00 01                |
    | sub word [rax + 1 * rdx], 0x01              | 66 83 2c 10 01                |
    | sub word [rax + 1 * rbx], 0x01              | 66 83 2c 18 01                |
    | sub word [rax + 1 * rbp], 0x01              | 66 83 2c 28 01                |
    | sub word [rax + 1 * rsi], 0x01              | 66 83 2c 30 01                |
    | sub word [rax + 1 * rdi], 0x01              | 66 83 2c 38 01                |
    | sub word [rax + 1 * r8], 0x01               | 66 42 83 2c 00 01             |
    | sub word [rax + 1 * r9], 0x01               | 66 42 83 2c 08 01             |
    | sub word [rax + 1 * r10], 0x01              | 66 42 83 2c 10 01             |
    | sub word [rax + 1 * r11], 0x01              | 66 42 83 2c 18 01             |
    | sub word [rax + 1 * r12], 0x01              | 66 42 83 2c 20 01             |
    | sub word [rax + 1 * r13], 0x01              | 66 42 83 2c 28 01             |
    | sub word [rax + 1 * r14], 0x01              | 66 42 83 2c 30 01             |
    | sub word [rax + 1 * r15], 0x01              | 66 42 83 2c 38 01             |
    | sub word [rax + 2 * rcx], 0x01              | 66 83 2c 48 01                |
    | sub word [rax + 4 * rcx], 0x01              | 66 83 2c 88 01                |
    | sub word [rax + 8 * rcx], 0x01              | 66 83 2c c8 01                |
    | sub word [r8 + 1 * r9], 0x01                | 66 43 83 2c 08 01             |
    | sub word [r8 + 2 * r9], 0x01                | 66 43 83 2c 48 01             |
    | sub word [r8 + 4 * r9], 0x01                | 66 43 83 2c 88 01             |
    | sub word [r8 + 8 * r9], 0x01                | 66 43 83 2c c8 01             |
    | sub word [1 * rcx], 0x01                    | 66 83 2c 0d 00 00 00 00 01    |
    | sub word [2 * rcx], 0x01                    | 66 83 2c 4d 00 00 00 00 01    |
    | sub word [4 * rcx], 0x01                    | 66 83 2c 8d 00 00 00 00 01    |
    | sub word [8 * rcx], 0x01                    | 66 83 2c cd 00 00 00 00 01    |
    | sub word [1 * r9], 0x01                     | 66 42 83 2c 0d 00 00 00 00 01 |
    | sub word [2 * r9], 0x01                     | 66 42 83 2c 4d 00 00 00 00 01 |
    | sub word [4 * r9], 0x01                     | 66 42 83 2c 8d 00 00 00 00 01 |
    | sub word [8 * r9], 0x01                     | 66 42 83 2c cd 00 00 00 00 01 |
    | sub word [r13 + 8 * r12], 0x01              | 66 43 83 6c e5 00 01          |
    | sub word [rsp + 4 * r15], 0x01              | 66 42 83 2c bc 01             |
    | sub word [rax + 1 * rcx + 0x00], 0x01       | 66 83 6c 08 00 01             |
    | sub word [rax + 1 * rcx - 0x00], 0x01       | 66 83 6c 08 00 01             |
    | sub word [rax + 1 * rcx + 0x01], 0x01       | 66 83 6c 08 01 01             |
    | sub word [rax + 1 * rcx - 0x01], 0x01       | 66 83 6c 08 ff 01             |
    | sub word [rax + 1 * rcx + 0x00000001], 0x01 | 66 83 ac 08 01 00 00 00 01    |
    | sub word [rax + 1 * rcx - 0x00000001], 0x01 | 66 83 ac 08 ff ff ff ff 01    |
    | sub word [rax + 1 * rcx + 0x7f], 0x01       | 66 83 6c 08 7f 01             |
    | sub word [rax + 1 * rcx - 0x7f], 0x01       | 66 83 6c 08 81 01             |
    | sub word [rax + 1 * rcx + 0x80], 0x01       | 66 83 ac 08 80 00 00 00 01    |
    | sub word [rax + 1 * rcx - 0x80], 0x01       | 66 83 6c 08 80 01             |
    | sub word [rax + 1 * rcx - 0x81], 0x01       | 66 83 ac 08 7f ff ff ff 01    |
    | sub word [rax + 1 * rcx + 0xff], 0x01       | 66 83 ac 08 ff 00 00 00 01    |
    | sub word [rax + 1 * rcx - 0xff], 0x01       | 66 83 ac 08 01 ff ff ff 01    |
    | sub word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 83 ac 08 ff ff ff 7f 01    |
    | sub word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 83 ac 08 01 00 00 80 01    |
    | sub word [rax + 1 * rcx - 0x80000000], 0x01 | 66 83 ac 08 00 00 00 80 01    |
    | sub word [r10 + 0x7f], 0x01                 | 66 41 83 6a 7f 01             |
    | sub word [r10 + 0x80], 0x01                 | 66 41 83 aa 80 00 00 00 01    |
    | sub word [r10 - 0x80], 0x01                 | 66 41 83 6a 80 01             |
    | sub word [r10 - 0x81], 0x01                 | 66 41 83 aa 7f ff ff ff 01    |
    | sub word [rax], 0x00                        | 66 83 28 00                   |
    | sub word [rax], 0x7f                        | 66 83 28 7f                   |
    | sub word [rax], 0x80                        | 66 83 28 80                   |
    | sub word [rax], 0xff                        | 66 83 28 ff                   |
    | sub word [rcx], 0x7f                        | 66 83 29 7f                   |
    | sub word [rdx], 0x80                        | 66 83 2a 80                   |
    | sub word [rbx], 0xff                        | 66 83 2b ff                   |
    | sub word [rsp], 0x00                        | 66 83 2c 24 00                |
    | sub word [rsi], 0x7f                        | 66 83 2e 7f                   |
    | sub word [rdi], 0x80                        | 66 83 2f 80                   |
    | sub word [r8], 0xff                         | 66 41 83 28 ff                |
    | sub word [r9], 0x00                         | 66 41 83 29 00                |
    | sub word [r11], 0x7f                        | 66 41 83 2b 7f                |
    | sub word [r12], 0x80                        | 66 41 83 2c 24 80             |
    | sub word [r13], 0xff                        | 66 41 83 6d 00 ff             |
    | sub word [r14], 0x00                        | 66 41 83 2e 00                |
    | sub word [rax + 1 * rcx], 0x7f              | 66 83 2c 08 7f                |
    | sub word [rcx + 1 * rcx], 0x80              | 66 83 2c 09 80                |
    | sub word [rdx + 1 * rcx], 0xff              | 66 83 2c 0a ff                |
    | sub word [rbx + 1 * rcx], 0x00              | 66 83 2c 0b 00                |
    | sub word [rbp + 1 * rcx], 0x7f              | 66 83 6c 0d 00 7f             |
    | sub word [rsi + 1 * rcx], 0x80              | 66 83 2c 0e 80                |
    | sub word [rdi + 1 * rcx], 0xff              | 66 83 2c 0f ff                |
    | sub word [r8 + 1 * rcx], 0x00               | 66 41 83 2c 08 00             |
    | sub word [r10 + 1 * rcx], 0x7f              | 66 41 83 2c 0a 7f             |
    | sub word [r11 + 1 * rcx], 0x80              | 66 41 83 2c 0b 80             |
    | sub word [r12 + 1 * rcx], 0xff              | 66 41 83 2c 0c ff             |
    | sub word [r13 + 1 * rcx], 0x00              | 66 41 83 6c 0d 00 00          |
    | sub word [r15 + 1 * rcx], 0x7f              | 66 41 83 2c 0f 7f             |
    | sub word [rax + 1 * rax], 0x80              | 66 83 2c 00 80                |
    | sub word [rax + 1 * rdx], 0xff              | 66 83 2c 10 ff                |
    | sub word [rax + 1 * rbx], 0x00              | 66 83 2c 18 00                |
    | sub word [rax + 1 * rsi], 0x7f              | 66 83 2c 30 7f                |
    | sub word [rax + 1 * rdi], 0x80              | 66 83 2c 38 80                |
    | sub word [rax + 1 * r8], 0xff               | 66 42 83 2c 00 ff             |
    | sub word [rax + 1 * r9], 0x00               | 66 42 83 2c 08 00             |
    | sub word [rax + 1 * r11], 0x7f              | 66 42 83 2c 18 7f             |
    | sub word [rax + 1 * r12], 0x80              | 66 42 83 2c 20 80             |
    | sub word [rax + 1 * r13], 0xff              | 66 42 83 2c 28 ff             |
    | sub word [rax + 1 * r14], 0x00              | 66 42 83 2c 30 00             |
    | sub word [rax + 2 * rcx], 0x7f              | 66 83 2c 48 7f                |
    | sub word [rax + 4 * rcx], 0x80              | 66 83 2c 88 80                |
    | sub word [rax + 8 * rcx], 0xff              | 66 83 2c c8 ff                |
    | sub word [r8 + 1 * r9], 0x00                | 66 43 83 2c 08 00             |
    | sub word [r8 + 4 * r9], 0x7f                | 66 43 83 2c 88 7f             |
    | sub word [r8 + 8 * r9], 0x80                | 66 43 83 2c c8 80             |
    | sub word [1 * rcx], 0xff                    | 66 83 2c 0d 00 00 00 00 ff    |
    | sub word [2 * rcx], 0x00                    | 66 83 2c 4d 00 00 00 00 00    |
    | sub word [8 * rcx], 0x7f                    | 66 83 2c cd 00 00 00 00 7f    |
    | sub word [1 * r9], 0x80                     | 66 42 83 2c 0d 00 00 00 00 80 |
    | sub word [2 * r9], 0xff                     | 66 42 83 2c 4d 00 00 00 00 ff |
    | sub word [4 * r9], 0x00                     | 66 42 83 2c 8d 00 00 00 00 00 |
    | sub word [r13 + 8 * r12], 0x7f              | 66 43 83 6c e5 00 7f          |
    | sub word [rsp + 4 * r15], 0x80              | 66 42 83 2c bc 80             |
    | sub word [rax + 1 * rcx + 0x00], 0xff       | 66 83 6c 08 00 ff             |
    | sub word [rax + 1 * rcx - 0x00], 0x00       | 66 83 6c 08 00 00             |
    | sub word [rax + 1 * rcx - 0x01], 0x7f       | 66 83 6c 08 ff 7f             |
    | sub word [rax + 1 * rcx + 0x00000001], 0x80 | 66 83 ac 08 01 00 00 00 80    |
    | sub word [rax + 1 * rcx - 0x00000001], 0xff | 66 83 ac 08 ff ff ff ff ff    |
    | sub word [rax + 1 * rcx + 0x7f], 0x00       | 66 83 6c 08 7f 00             |
    | sub word [rax + 1 * rcx + 0x80], 0x7f       | 66 83 ac 08 80 00 00 00 7f    |
    | sub word [rax + 1 * rcx - 0x80], 0x80       | 66 83 6c 08 80 80             |
    | sub word [rax + 1 * rcx - 0x81], 0xff       | 66 83 ac 08 7f ff ff ff ff    |
    | sub word [rax + 1 * rcx + 0xff], 0x00       | 66 83 ac 08 ff 00 00 00 00    |
    | sub word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 83 ac 08 ff ff ff 7f 7f    |
    | sub word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 83 ac 08 01 00 00 80 80    |
    | sub word [rax + 1 * rcx - 0x80000000], 0xff | 66 83 ac 08 00 00 00 80 ff    |
    | sub word [r10 + 0x7f], 0x00                 | 66 41 83 6a 7f 00             |
    | sub word [r10 - 0x80], 0x7f                 | 66 41 83 6a 80 7f             |
    | sub word [r10 - 0x81], 0x80                 | 66 41 83 aa 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_sub_addr16_imm8():
    encode(SUB_ADDR16_IMM8)


SUB_ADDR16_IMM16 = """
    | --------------------------------------------- | -------------------------------- |
    | instruction                                   | encoding                         |
    | --------------------------------------------- | -------------------------------- |
    | sub word [rax], 0x0001                        | 66 81 28 01 00                   |
    | sub word [rcx], 0x0001                        | 66 81 29 01 00                   |
    | sub word [rdx], 0x0001                        | 66 81 2a 01 00                   |
    | sub word [rbx], 0x0001                        | 66 81 2b 01 00                   |
    | sub word [rsp], 0x0001                        | 66 81 2c 24 01 00                |
    | sub word [rbp], 0x0001                        | 66 81 6d 00 01 00                |
    | sub word [rsi], 0x0001                        | 66 81 2e 01 00                   |
    | sub word [rdi], 0x0001                        | 66 81 2f 01 00                   |
    | sub word [r8], 0x0001                         | 66 41 81 28 01 00                |
    | sub word [r9], 0x0001                         | 66 41 81 29 01 00                |
    | sub word [r10], 0x0001                        | 66 41 81 2a 01 00                |
    | sub word [r11], 0x0001                        | 66 41 81 2b 01 00                |
    | sub word [r12], 0x0001                        | 66 41 81 2c 24 01 00             |
    | sub word [r13], 0x0001                        | 66 41 81 6d 00 01 00             |
    | sub word [r14], 0x0001                        | 66 41 81 2e 01 00                |
    | sub word [r15], 0x0001                        | 66 41 81 2f 01 00                |
    | sub word [rax + 1 * rcx], 0x0001              | 66 81 2c 08 01 00                |
    | sub word [rcx + 1 * rcx], 0x0001              | 66 81 2c 09 01 00                |
    | sub word [rdx + 1 * rcx], 0x0001              | 66 81 2c 0a 01 00                |
    | sub word [rbx + 1 * rcx], 0x0001              | 66 81 2c 0b 01 00                |
    | sub word [rsp + 1 * rcx], 0x0001              | 66 81 2c 0c 01 00                |
    | sub word [rbp + 1 * rcx], 0x0001              | 66 81 6c 0d 00 01 00             |
    | sub word [rsi + 1 * rcx], 0x0001              | 66 81 2c 0e 01 00                |
    | sub word [rdi + 1 * rcx], 0x0001              | 66 81 2c 0f 01 00                |
    | sub word [r8 + 1 * rcx], 0x0001               | 66 41 81 2c 08 01 00             |
    | sub word [r9 + 1 * rcx], 0x0001               | 66 41 81 2c 09 01 00             |
    | sub word [r10 + 1 * rcx], 0x0001              | 66 41 81 2c 0a 01 00             |
    | sub word [r11 + 1 * rcx], 0x0001              | 66 41 81 2c 0b 01 00             |
    | sub word [r12 + 1 * rcx], 0x0001              | 66 41 81 2c 0c 01 00             |
    | sub word [r13 + 1 * rcx], 0x0001              | 66 41 81 6c 0d 00 01 00          |
    | sub word [r14 + 1 * rcx], 0x0001              | 66 41 81 2c 0e 01 00             |
    | sub word [r15 + 1 * rcx], 0x0001              | 66 41 81 2c 0f 01 00             |
    | sub word [rax + 1 * rax], 0x0001              | 66 81 2c 00 01 00                |
    | sub word [rax + 1 * rdx], 0x0001              | 66 81 2c 10 01 00                |
    | sub word [rax + 1 * rbx], 0x0001              | 66 81 2c 18 01 00                |
    | sub word [rax + 1 * rbp], 0x0001              | 66 81 2c 28 01 00                |
    | sub word [rax + 1 * rsi], 0x0001              | 66 81 2c 30 01 00                |
    | sub word [rax + 1 * rdi], 0x0001              | 66 81 2c 38 01 00                |
    | sub word [rax + 1 * r8], 0x0001               | 66 42 81 2c 00 01 00             |
    | sub word [rax + 1 * r9], 0x0001               | 66 42 81 2c 08 01 00             |
    | sub word [rax + 1 * r10], 0x0001              | 66 42 81 2c 10 01 00             |
    | sub word [rax + 1 * r11], 0x0001              | 66 42 81 2c 18 01 00             |
    | sub word [rax + 1 * r12], 0x0001              | 66 42 81 2c 20 01 00             |
    | sub word [rax + 1 * r13], 0x0001              | 66 42 81 2c 28 01 00             |
    | sub word [rax + 1 * r14], 0x0001              | 66 42 81 2c 30 01 00             |
    | sub word [rax + 1 * r15], 0x0001              | 66 42 81 2c 38 01 00             |
    | sub word [rax + 2 * rcx], 0x0001              | 66 81 2c 48 01 00                |
    | sub word [rax + 4 * rcx], 0x0001              | 66 81 2c 88 01 00                |
    | sub word [rax + 8 * rcx], 0x0001              | 66 81 2c c8 01 00                |
    | sub word [r8 + 1 * r9], 0x0001                | 66 43 81 2c 08 01 00             |
    | sub word [r8 + 2 * r9], 0x0001                | 66 43 81 2c 48 01 00             |
    | sub word [r8 + 4 * r9], 0x0001                | 66 43 81 2c 88 01 00             |
    | sub word [r8 + 8 * r9], 0x0001                | 66 43 81 2c c8 01 00             |
    | sub word [1 * rcx], 0x0001                    | 66 81 2c 0d 00 00 00 00 01 00    |
    | sub word [2 * rcx], 0x0001                    | 66 81 2c 4d 00 00 00 00 01 00    |
    | sub word [4 * rcx], 0x0001                    | 66 81 2c 8d 00 00 00 00 01 00    |
    | sub word [8 * rcx], 0x0001                    | 66 81 2c cd 00 00 00 00 01 00    |
    | sub word [1 * r9], 0x0001                     | 66 42 81 2c 0d 00 00 00 00 01 00 |
    | sub word [2 * r9], 0x0001                     | 66 42 81 2c 4d 00 00 00 00 01 00 |
    | sub word [4 * r9], 0x0001                     | 66 42 81 2c 8d 00 00 00 00 01 00 |
    | sub word [8 * r9], 0x0001                     | 66 42 81 2c cd 00 00 00 00 01 00 |
    | sub word [r13 + 8 * r12], 0x0001              | 66 43 81 6c e5 00 01 00          |
    | sub word [rsp + 4 * r15], 0x0001              | 66 42 81 2c bc 01 00             |
    | sub word [rax + 1 * rcx + 0x00], 0x0001       | 66 81 6c 08 00 01 00             |
    | sub word [rax + 1 * rcx - 0x00], 0x0001       | 66 81 6c 08 00 01 00             |
    | sub word [rax + 1 * rcx + 0x01], 0x0001       | 66 81 6c 08 01 01 00             |
    | sub word [rax + 1 * rcx - 0x01], 0x0001       | 66 81 6c 08 ff 01 00             |
    | sub word [rax + 1 * rcx + 0x00000001], 0x0001 | 66 81 ac 08 01 00 00 00 01 00    |
    | sub word [rax + 1 * rcx - 0x00000001], 0x0001 | 66 81 ac 08 ff ff ff ff 01 00    |
    | sub word [rax + 1 * rcx + 0x7f], 0x0001       | 66 81 6c 08 7f 01 00             |
    | sub word [rax + 1 * rcx - 0x7f], 0x0001       | 66 81 6c 08 81 01 00             |
    | sub word [rax + 1 * rcx + 0x80], 0x0001       | 66 81 ac 08 80 00 00 00 01 00    |
    | sub word [rax + 1 * rcx - 0x80], 0x0001       | 66 81 6c 08 80 01 00             |
    | sub word [rax + 1 * rcx - 0x81], 0x0001       | 66 81 ac 08 7f ff ff ff 01 00    |
    | sub word [rax + 1 * rcx + 0xff], 0x0001       | 66 81 ac 08 ff 00 00 00 01 00    |
    | sub word [rax + 1 * rcx - 0xff], 0x0001       | 66 81 ac 08 01 ff ff ff 01 00    |
    | sub word [rax + 1 * rcx + 0x7fffffff], 0x0001 | 66 81 ac 08 ff ff ff 7f 01 00    |
    | sub word [rax + 1 * rcx - 0x7fffffff], 0x0001 | 66 81 ac 08 01 00 00 80 01 00    |
    | sub word [rax + 1 * rcx - 0x80000000], 0x0001 | 66 81 ac 08 00 00 00 80 01 00    |
    | sub word [r10 + 0x7f], 0x0001                 | 66 41 81 6a 7f 01 00             |
    | sub word [r10 + 0x80], 0x0001                 | 66 41 81 aa 80 00 00 00 01 00    |
    | sub word [r10 - 0x80], 0x0001                 | 66 41 81 6a 80 01 00             |
    | sub word [r10 - 0x81], 0x0001                 | 66 41 81 aa 7f ff ff ff 01 00    |
    | sub word [rax], 0x0000                        | 66 81 28 00 00                   |
    | sub word [rax], 0x007f                        | 66 81 28 7f 00                   |
    | sub word [rax], 0x0080                        | 66 81 28 80 00                   |
    | sub word [rax], 0x00ff                        | 66 81 28 ff 00                   |
    | sub word [rax], 0x0100                        | 66 81 28 00 01                   |
    | sub word [rax], 0x7fff                        | 66 81 28 ff 7f                   |
    | sub word [rax], 0x8000                        | 66 81 28 00 80                   |
    | sub word [rax], 0xffff                        | 66 81 28 ff ff                   |
    | sub word [rcx], 0x007f                        | 66 81 29 7f 00                   |
    | sub word [rdx], 0x0080                        | 66 81 2a 80 00                   |
    | sub word [rbx], 0x00ff                        | 66 81 2b ff 00                   |
    | sub word [rsp], 0x0100                        | 66 81 2c 24 00 01                |
    | sub word [rbp], 0x7fff                        | 66 81 6d 00 ff 7f                |
    | sub word [rsi], 0x8000                        | 66 81 2e 00 80                   |
    | sub word [rdi], 0xffff                        | 66 81 2f ff ff                   |
    | sub word [r8], 0x0000                         | 66 41 81 28 00 00                |
    | sub word [r10], 0x007f                        | 66 41 81 2a 7f 00                |
    | sub word [r11], 0x0080                        | 66 41 81 2b 80 00                |
    | sub word [r12], 0x00ff                        | 66 41 81 2c 24 ff 00             |
    | sub word [r13], 0x0100                        | 66 41 81 6d 00 00 01             |
    | sub word [r14], 0x7fff                        | 66 41 81 2e ff 7f                |
    | sub word [r15], 0x8000                        | 66 41 81 2f 00 80                |
    | sub word [rax + 1 * rcx], 0xffff              | 66 81 2c 08 ff ff                |
    | sub word [rcx + 1 * rcx], 0x0000              | 66 81 2c 09 00 00                |
    | sub word [rbx + 1 * rcx], 0x007f              | 66 81 2c 0b 7f 00                |
    | sub word [rsp + 1 * rcx], 0x0080              | 66 81 2c 0c 80 00                |
    | sub word [rbp + 1 * rcx], 0x00ff              | 66 81 6c 0d 00 ff 00             |
    | sub word [rsi + 1 * rcx], 0x0100              | 66 81 2c 0e 00 01                |
    | sub word [rdi + 1 * rcx], 0x7fff              | 66 81 2c 0f ff 7f                |
    | sub word [r8 + 1 * rcx], 0x8000               | 66 41 81 2c 08 00 80             |
    | sub word [r9 + 1 * rcx], 0xffff               | 66 41 81 2c 09 ff ff             |
    | sub word [r10 + 1 * rcx], 0x0000              | 66 41 81 2c 0a 00 00             |
    | sub word [r12 + 1 * rcx], 0x007f              | 66 41 81 2c 0c 7f 00             |
    | sub word [r13 + 1 * rcx], 0x0080              | 66 41 81 6c 0d 00 80 00          |
    | sub word [r14 + 1 * rcx], 0x00ff              | 66 41 81 2c 0e ff 00             |
    | sub word [r15 + 1 * rcx], 0x0100              | 66 41 81 2c 0f 00 01             |
    | sub word [rax + 1 * rax], 0x7fff              | 66 81 2c 00 ff 7f                |
    | sub word [rax + 1 * rdx], 0x8000              | 66 81 2c 10 00 80                |
    | sub word [rax + 1 * rbx], 0xffff              | 66 81 2c 18 ff ff                |
    | sub word [rax + 1 * rbp], 0x0000              | 66 81 2c 28 00 00                |
    | sub word [rax + 1 * rdi], 0x007f              | 66 81 2c 38 7f 00                |
    | sub word [rax + 1 * r8], 0x0080               | 66 42 81 2c 00 80 00             |
    | sub word [rax + 1 * r9], 0x00ff               | 66 42 81 2c 08 ff 00             |
    | sub word [rax + 1 * r10], 0x0100              | 66 42 81 2c 10 00 01             |
    | sub word [rax + 1 * r11], 0x7fff              | 66 42 81 2c 18 ff 7f             |
    | sub word [rax + 1 * r12], 0x8000              | 66 42 81 2c 20 00 80             |
    | sub word [rax + 1 * r13], 0xffff              | 66 42 81 2c 28 ff ff             |
    | sub word [rax + 1 * r14], 0x0000              | 66 42 81 2c 30 00 00             |
    | sub word [rax + 2 * rcx], 0x007f              | 66 81 2c 48 7f 00                |
    | sub word [rax + 4 * rcx], 0x0080              | 66 81 2c 88 80 00                |
    | sub word [rax + 8 * rcx], 0x00ff              | 66 81 2c c8 ff 00                |
    | sub word [r8 + 1 * r9], 0x0100                | 66 43 81 2c 08 00 01             |
    | sub word [r8 + 2 * r9], 0x7fff                | 66 43 81 2c 48 ff 7f             |
    | sub word [r8 + 4 * r9], 0x8000                | 66 43 81 2c 88 00 80             |
    | sub word [r8 + 8 * r9], 0xffff                | 66 43 81 2c c8 ff ff             |
    | sub word [1 * rcx], 0x0000                    | 66 81 2c 0d 00 00 00 00 00 00    |
    | sub word [4 * rcx], 0x007f                    | 66 81 2c 8d 00 00 00 00 7f 00    |
    | sub word [8 * rcx], 0x0080                    | 66 81 2c cd 00 00 00 00 80 00    |
    | sub word [1 * r9], 0x00ff                     | 66 42 81 2c 0d 00 00 00 00 ff 00 |
    | sub word [2 * r9], 0x0100                     | 66 42 81 2c 4d 00 00 00 00 00 01 |
    | sub word [4 * r9], 0x7fff                     | 66 42 81 2c 8d 00 00 00 00 ff 7f |
    | sub word [8 * r9], 0x8000                     | 66 42 81 2c cd 00 00 00 00 00 80 |
    | sub word [r13 + 8 * r12], 0xffff              | 66 43 81 6c e5 00 ff ff          |
    | sub word [rsp + 4 * r15], 0x0000              | 66 42 81 2c bc 00 00             |
    | sub word [rax + 1 * rcx - 0x00], 0x007f       | 66 81 6c 08 00 7f 00             |
    | sub word [rax + 1 * rcx + 0x01], 0x0080       | 66 81 6c 08 01 80 00             |
    | sub word [rax + 1 * rcx - 0x01], 0x00ff       | 66 81 6c 08 ff ff 00             |
    | sub word [rax + 1 * rcx + 0x00000001], 0x0100 | 66 81 ac 08 01 00 00 00 00 01    |
    | sub word [rax + 1 * rcx - 0x00000001], 0x7fff | 66 81 ac 08 ff ff ff ff ff 7f    |
    | sub word [rax + 1 * rcx + 0x7f], 0x8000       | 66 81 6c 08 7f 00 80             |
    | sub word [rax + 1 * rcx - 0x7f], 0xffff       | 66 81 6c 08 81 ff ff             |
    | sub word [rax + 1 * rcx + 0x80], 0x0000       | 66 81 ac 08 80 00 00 00 00 00    |
    | sub word [rax + 1 * rcx - 0x81], 0x007f       | 66 81 ac 08 7f ff ff ff 7f 00    |
    | sub word [rax + 1 * rcx + 0xff], 0x0080       | 66 81 ac 08 ff 00 00 00 80 00    |
    | sub word [rax + 1 * rcx - 0xff], 0x00ff       | 66 81 ac 08 01 ff ff ff ff 00    |
    | sub word [rax + 1 * rcx + 0x7fffffff], 0x0100 | 66 81 ac 08 ff ff ff 7f 00 01    |
    | sub word [rax + 1 * rcx - 0x7fffffff], 0x7fff | 66 81 ac 08 01 00 00 80 ff 7f    |
    | sub word [rax + 1 * rcx - 0x80000000], 0x8000 | 66 81 ac 08 00 00 00 80 00 80    |
    | sub word [r10 + 0x7f], 0xffff                 | 66 41 81 6a 7f ff ff             |
    | sub word [r10 + 0x80], 0x0000                 | 66 41 81 aa 80 00 00 00 00 00    |
    | sub word [r10 - 0x81], 0x007f                 | 66 41 81 aa 7f ff ff ff 7f 00    |
    | --------------------------------------------- | -------------------------------- |
"""


def can_encode_sub_addr16_imm16():
    encode(SUB_ADDR16_IMM16)


SUB_ADDR16_REG16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sub word [rax], cx                          | 66 29 08                   |
    | sub word [rcx], cx                          | 66 29 09                   |
    | sub word [rdx], cx                          | 66 29 0a                   |
    | sub word [rbx], cx                          | 66 29 0b                   |
    | sub word [rsp], cx                          | 66 29 0c 24                |
    | sub word [rbp], cx                          | 66 29 4d 00                |
    | sub word [rsi], cx                          | 66 29 0e                   |
    | sub word [rdi], cx                          | 66 29 0f                   |
    | sub word [r8], cx                           | 66 41 29 08                |
    | sub word [r9], cx                           | 66 41 29 09                |
    | sub word [r10], cx                          | 66 41 29 0a                |
    | sub word [r11], cx                          | 66 41 29 0b                |
    | sub word [r12], cx                          | 66 41 29 0c 24             |
    | sub word [r13], cx                          | 66 41 29 4d 00             |
    | sub word [r14], cx                          | 66 41 29 0e                |
    | sub word [r15], cx                          | 66 41 29 0f                |
    | sub word [rax + 1 * rcx], cx                | 66 29 0c 08                |
    | sub word [rcx + 1 * rcx], cx                | 66 29 0c 09                |
    | sub word [rdx + 1 * rcx], cx                | 66 29 0c 0a                |
    | sub word [rbx + 1 * rcx], cx                | 66 29 0c 0b                |
    | sub word [rsp + 1 * rcx], cx                | 66 29 0c 0c                |
    | sub word [rbp + 1 * rcx], cx                | 66 29 4c 0d 00             |
    | sub word [rsi + 1 * rcx], cx                | 66 29 0c 0e                |
    | sub word [rdi + 1 * rcx], cx                | 66 29 0c 0f                |
    | sub word [r8 + 1 * rcx], cx                 | 66 41 29 0c 08             |
    | sub word [r9 + 1 * rcx], cx                 | 66 41 29 0c 09             |
    | sub word [r10 + 1 * rcx], cx                | 66 41 29 0c 0a             |
    | sub word [r11 + 1 * rcx], cx                | 66 41 29 0c 0b             |
    | sub word [r12 + 1 * rcx], cx                | 66 41 29 0c 0c             |
    | sub word [r13 + 1 * rcx], cx                | 66 41 29 4c 0d 00          |
    | sub word [r14 + 1 * rcx], cx                | 66 41 29 0c 0e             |
    | sub word [r15 + 1 * rcx], cx                | 66 41 29 0c 0f             |
    | sub word [rax + 1 * rax], cx                | 66 29 0c 00                |
    | sub word [rax + 1 * rdx], cx                | 66 29 0c 10                |
    | sub word [rax + 1 * rbx], cx                | 66 29 0c 18                |
    | sub word [rax + 1 * rbp], cx                | 66 29 0c 28                |
    | sub word [rax + 1 * rsi], cx                | 66 29 0c 30                |
    | sub word [rax + 1 * rdi], cx                | 66 29 0c 38                |
    | sub word [rax + 1 * r8], cx                 | 66 42 29 0c 00             |
    | sub word [rax + 1 * r9], cx                 | 66 42 29 0c 08             |
    | sub word [rax + 1 * r10], cx                | 66 42 29 0c 10             |
    | sub word [rax + 1 * r11], cx                | 66 42 29 0c 18             |
    | sub word [rax + 1 * r12], cx                | 66 42 29 0c 20             |
    | sub word [rax + 1 * r13], cx                | 66 42 29 0c 28             |
    | sub word [rax + 1 * r14], cx                | 66 42 29 0c 30             |
    | sub word [rax + 1 * r15], cx                | 66 42 29 0c 38             |
    | sub word [rax + 2 * rcx], cx                | 66 29 0c 48                |
    | sub word [rax + 4 * rcx], cx                | 66 29 0c 88                |
    | sub word [rax + 8 * rcx], cx                | 66 29 0c c8                |
    | sub word [r8 + 1 * r9], cx                  | 66 43 29 0c 08             |
    | sub word [r8 + 2 * r9], cx                  | 66 43 29 0c 48             |
    | sub word [r8 + 4 * r9], cx                  | 66 43 29 0c 88             |
    | sub word [r8 + 8 * r9], cx                  | 66 43 29 0c c8             |
    | sub word [1 * rcx], cx                      | 66 29 0c 0d 00 00 00 00    |
    | sub word [2 * rcx], cx                      | 66 29 0c 4d 00 00 00 00    |
    | sub word [4 * rcx], cx                      | 66 29 0c 8d 00 00 00 00    |
    | sub word [8 * rcx], cx                      | 66 29 0c cd 00 00 00 00    |
    | sub word [1 * r9], cx                       | 66 42 29 0c 0d 00 00 00 00 |
    | sub word [2 * r9], cx                       | 66 42 29 0c 4d 00 00 00 00 |
    | sub word [4 * r9], cx                       | 66 42 29 0c 8d 00 00 00 00 |
    | sub word [8 * r9], cx                       | 66 42 29 0c cd 00 00 00 00 |
    | sub word [r13 + 8 * r12], cx                | 66 43 29 4c e5 00          |
    | sub word [rsp + 4 * r15], cx                | 66 42 29 0c bc             |
    | sub word [rax + 1 * rcx + 0x00], cx         | 66 29 4c 08 00             |
    | sub word [rax + 1 * rcx - 0x00], cx         | 66 29 4c 08 00             |
    | sub word [rax + 1 * rcx + 0x01], cx         | 66 29 4c 08 01             |
    | sub word [rax + 1 * rcx - 0x01], cx         | 66 29 4c 08 ff             |
    | sub word [rax + 1 * rcx + 0x00000001], cx   | 66 29 8c 08 01 00 00 00    |
    | sub word [rax + 1 * rcx - 0x00000001], cx   | 66 29 8c 08 ff ff ff ff    |
    | sub word [rax + 1 * rcx + 0x7f], cx         | 66 29 4c 08 7f             |
    | sub word [rax + 1 * rcx - 0x7f], cx         | 66 29 4c 08 81             |
    | sub word [rax + 1 * rcx + 0x80], cx         | 66 29 8c 08 80 00 00 00    |
    | sub word [rax + 1 * rcx - 0x80], cx         | 66 29 4c 08 80             |
    | sub word [rax + 1 * rcx - 0x81], cx         | 66 29 8c 08 7f ff ff ff    |
    | sub word [rax + 1 * rcx + 0xff], cx         | 66 29 8c 08 ff 00 00 00    |
    | sub word [rax + 1 * rcx - 0xff], cx         | 66 29 8c 08 01 ff ff ff    |
    | sub word [rax + 1 * rcx + 0x7fffffff], cx   | 66 29 8c 08 ff ff ff 7f    |
    | sub word [rax + 1 * rcx - 0x7fffffff], cx   | 66 29 8c 08 01 00 00 80    |
    | sub word [rax + 1 * rcx - 0x80000000], cx   | 66 29 8c 08 00 00 00 80    |
    | sub word [r10 + 0x7f], cx                   | 66 41 29 4a 7f             |
    | sub word [r10 + 0x80], cx                   | 66 41 29 8a 80 00 00 00    |
    | sub word [r10 - 0x80], cx                   | 66 41 29 4a 80             |
    | sub word [r10 - 0x81], cx                   | 66 41 29 8a 7f ff ff ff    |
    | sub word [rax], ax                          | 66 29 00                   |
    | sub word [rax], dx                          | 66 29 10                   |
    | sub word [rax], bx                          | 66 29 18                   |
    | sub word [rax], sp                          | 66 29 20                   |
    | sub word [rax], bp                          | 66 29 28                   |
    | sub word [rax], si                          | 66 29 30                   |
    | sub word [rax], di                          | 66 29 38                   |
    | sub word [rax], r8w                         | 66 44 29 00                |
    | sub word [rax], r9w                         | 66 44 29 08                |
    | sub word [rax], r10w                        | 66 44 29 10                |
    | sub word [rax], r11w                        | 66 44 29 18                |
    | sub word [rax], r12w                        | 66 44 29 20                |
    | sub word [rax], r13w                        | 66 44 29 28                |
    | sub word [rax], r14w                        | 66 44 29 30                |
    | sub word [rax], r15w                        | 66 44 29 38                |
    | sub word [rcx], dx                          | 66 29 11                   |
    | sub word [rdx], bx                          | 66 29 1a                   |
    | sub word [rbx], sp                          | 66 29 23                   |
    | sub word [rsp], bp                          | 66 29 2c 24                |
    | sub word [rbp], si                          | 66 29 75 00                |
    | sub word [rsi], di                          | 66 29 3e                   |
    | sub word [rdi], r8w                         | 66 44 29 07                |
    | sub word [r8], r9w                          | 66 45 29 08                |
    | sub word [r9], r10w                         | 66 45 29 11                |
    | sub word [r10], r11w                        | 66 45 29 1a                |
    | sub word [r11], r12w                        | 66 45 29 23                |
    | sub word [r12], r13w                        | 66 45 29 2c 24             |
    | sub word [r13], r14w                        | 66 45 29 75 00             |
    | sub word [r14], r15w                        | 66 45 29 3e                |
    | sub word [r15], ax                          | 66 41 29 07                |
    | sub word [rcx + 1 * rcx], dx                | 66 29 14 09                |
    | sub word [rdx + 1 * rcx], bx                | 66 29 1c 0a                |
    | sub word [rbx + 1 * rcx], sp                | 66 29 24 0b                |
    | sub word [rsp + 1 * rcx], bp                | 66 29 2c 0c                |
    | sub word [rbp + 1 * rcx], si                | 66 29 74 0d 00             |
    | sub word [rsi + 1 * rcx], di                | 66 29 3c 0e                |
    | sub word [rdi + 1 * rcx], r8w               | 66 44 29 04 0f             |
    | sub word [r8 + 1 * rcx], r9w                | 66 45 29 0c 08             |
    | sub word [r9 + 1 * rcx], r10w               | 66 45 29 14 09             |
    | sub word [r10 + 1 * rcx], r11w              | 66 45 29 1c 0a             |
    | sub word [r11 + 1 * rcx], r12w              | 66 45 29 24 0b             |
    | sub word [r12 + 1 * rcx], r13w              | 66 45 29 2c 0c             |
    | sub word [r13 + 1 * rcx], r14w              | 66 45 29 74 0d 00          |
    | sub word [r14 + 1 * rcx], r15w              | 66 45 29 3c 0e             |
    | sub word [r15 + 1 * rcx], ax                | 66 41 29 04 0f             |
    | sub word [rax + 1 * rdx], dx                | 66 29 14 10                |
    | sub word [rax + 1 * rbx], bx                | 66 29 1c 18                |
    | sub word [rax + 1 * rbp], sp                | 66 29 24 28                |
    | sub word [rax + 1 * rsi], bp                | 66 29 2c 30                |
    | sub word [rax + 1 * rdi], si                | 66 29 34 38                |
    | sub word [rax + 1 * r8], di                 | 66 42 29 3c 00             |
    | sub word [rax + 1 * r9], r8w                | 66 46 29 04 08             |
    | sub word [rax + 1 * r10], r9w               | 66 46 29 0c 10             |
    | sub word [rax + 1 * r11], r10w              | 66 46 29 14 18             |
    | sub word [rax + 1 * r12], r11w              | 66 46 29 1c 20             |
    | sub word [rax + 1 * r13], r12w              | 66 46 29 24 28             |
    | sub word [rax + 1 * r14], r13w              | 66 46 29 2c 30             |
    | sub word [rax + 1 * r15], r14w              | 66 46 29 34 38             |
    | sub word [rax + 2 * rcx], r15w              | 66 44 29 3c 48             |
    | sub word [rax + 4 * rcx], ax                | 66 29 04 88                |
    | sub word [r8 + 1 * r9], dx                  | 66 43 29 14 08             |
    | sub word [r8 + 2 * r9], bx                  | 66 43 29 1c 48             |
    | sub word [r8 + 4 * r9], sp                  | 66 43 29 24 88             |
    | sub word [r8 + 8 * r9], bp                  | 66 43 29 2c c8             |
    | sub word [1 * rcx], si                      | 66 29 34 0d 00 00 00 00    |
    | sub word [2 * rcx], di                      | 66 29 3c 4d 00 00 00 00    |
    | sub word [4 * rcx], r8w                     | 66 44 29 04 8d 00 00 00 00 |
    | sub word [8 * rcx], r9w                     | 66 44 29 0c cd 00 00 00 00 |
    | sub word [1 * r9], r10w                     | 66 46 29 14 0d 00 00 00 00 |
    | sub word [2 * r9], r11w                     | 66 46 29 1c 4d 00 00 00 00 |
    | sub word [4 * r9], r12w                     | 66 46 29 24 8d 00 00 00 00 |
    | sub word [8 * r9], r13w                     | 66 46 29 2c cd 00 00 00 00 |
    | sub word [r13 + 8 * r12], r14w              | 66 47 29 74 e5 00          |
    | sub word [rsp + 4 * r15], r15w              | 66 46 29 3c bc             |
    | sub word [rax + 1 * rcx + 0x00], ax         | 66 29 44 08 00             |
    | sub word [rax + 1 * rcx + 0x01], dx         | 66 29 54 08 01             |
    | sub word [rax + 1 * rcx - 0x01], bx         | 66 29 5c 08 ff             |
    | sub word [rax + 1 * rcx + 0x00000001], sp   | 66 29 a4 08 01 00 00 00    |
    | sub word [rax + 1 * rcx - 0x00000001], bp   | 66 29 ac 08 ff ff ff ff    |
    | sub word [rax + 1 * rcx + 0x7f], si         | 66 29 74 08 7f             |
    | sub word [rax + 1 * rcx - 0x7f], di         | 66 29 7c 08 81             |
    | sub word [rax + 1 * rcx + 0x80], r8w        | 66 44 29 84 08 80 00 00 00 |
    | sub word [rax + 1 * rcx - 0x80], r9w        | 66 44 29 4c 08 80          |
    | sub word [rax + 1 * rcx - 0x81], r10w       | 66 44 29 94 08 7f ff ff ff |
    | sub word [rax + 1 * rcx + 0xff], r11w       | 66 44 29 9c 08 ff 00 00 00 |
    | sub word [rax + 1 * rcx - 0xff], r12w       | 66 44 29 a4 08 01 ff ff ff |
    | sub word [rax + 1 * rcx + 0x7fffffff], r13w | 66 44 29 ac 08 ff ff ff 7f |
    | sub word [rax + 1 * rcx - 0x7fffffff], r14w | 66 44 29 b4 08 01 00 00 80 |
    | sub word [rax + 1 * rcx - 0x80000000], r15w | 66 44 29 bc 08 00 00 00 80 |
    | sub word [r10 + 0x7f], ax                   | 66 41 29 42 7f             |
    | sub word [r10 - 0x80], dx                   | 66 41 29 52 80             |
    | sub word [r10 - 0x81], bx                   | 66 41 29 9a 7f ff ff ff    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sub_addr16_reg16():
    encode(SUB_ADDR16_REG16)


SUB_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sub byte [rax], 0x01                        | 80 28 01                   |
    | sub byte [rcx], 0x01                        | 80 29 01                   |
    | sub byte [rdx], 0x01                        | 80 2a 01                   |
    | sub byte [rbx], 0x01                        | 80 2b 01                   |
    | sub byte [rsp], 0x01                        | 80 2c 24 01                |
    | sub byte [rbp], 0x01                        | 80 6d 00 01                |
    | sub byte [rsi], 0x01                        | 80 2e 01                   |
    | sub byte [rdi], 0x01                        | 80 2f 01                   |
    | sub byte [r8], 0x01                         | 41 80 28 01                |
    | sub byte [r9], 0x01                         | 41 80 29 01                |
    | sub byte [r10], 0x01                        | 41 80 2a 01                |
    | sub byte [r11], 0x01                        | 41 80 2b 01                |
    | sub byte [r12], 0x01                        | 41 80 2c 24 01             |
    | sub byte [r13], 0x01                        | 41 80 6d 00 01             |
    | sub byte [r14], 0x01                        | 41 80 2e 01                |
    | sub byte [r15], 0x01                        | 41 80 2f 01                |
    | sub byte [rax + 1 * rcx], 0x01              | 80 2c 08 01                |
    | sub byte [rcx + 1 * rcx], 0x01              | 80 2c 09 01                |
    | sub byte [rdx + 1 * rcx], 0x01              | 80 2c 0a 01                |
    | sub byte [rbx + 1 * rcx], 0x01              | 80 2c 0b 01                |
    | sub byte [rsp + 1 * rcx], 0x01              | 80 2c 0c 01                |
    | sub byte [rbp + 1 * rcx], 0x01              | 80 6c 0d 00 01             |
    | sub byte [rsi + 1 * rcx], 0x01              | 80 2c 0e 01                |
    | sub byte [rdi + 1 * rcx], 0x01              | 80 2c 0f 01                |
    | sub byte [r8 + 1 * rcx], 0x01               | 41 80 2c 08 01             |
    | sub byte [r9 + 1 * rcx], 0x01               | 41 80 2c 09 01             |
    | sub byte [r10 + 1 * rcx], 0x01              | 41 80 2c 0a 01             |
    | sub byte [r11 + 1 * rcx], 0x01              | 41 80 2c 0b 01             |
    | sub byte [r12 + 1 * rcx], 0x01              | 41 80 2c 0c 01             |
    | sub byte [r13 + 1 * rcx], 0x01              | 41 80 6c 0d 00 01          |
    | sub byte [r14 + 1 * rcx], 0x01              | 41 80 2c 0e 01             |
    | sub byte [r15 + 1 * rcx], 0x01              | 41 80 2c 0f 01             |
    | sub byte [rax + 1 * rax], 0x01              | 80 2c 00 01                |
    | sub byte [rax + 1 * rdx], 0x01              | 80 2c 10 01                |
    | sub byte [rax + 1 * rbx], 0x01              | 80 2c 18 01                |
    | sub byte [rax + 1 * rbp], 0x01              | 80 2c 28 01                |
    | sub byte [rax + 1 * rsi], 0x01              | 80 2c 30 01                |
    | sub byte [rax + 1 * rdi], 0x01              | 80 2c 38 01                |
    | sub byte [rax + 1 * r8], 0x01               | 42 80 2c 00 01             |
    | sub byte [rax + 1 * r9], 0x01               | 42 80 2c 08 01             |
    | sub byte [rax + 1 * r10], 0x01              | 42 80 2c 10 01             |
    | sub byte [rax + 1 * r11], 0x01              | 42 80 2c 18 01             |
    | sub byte [rax + 1 * r12], 0x01              | 42 80 2c 20 01             |
    | sub byte [rax + 1 * r13], 0x01              | 42 80 2c 28 01             |
    | sub byte [rax + 1 * r14], 0x01              | 42 80 2c 30 01             |
    | sub byte [rax + 1 * r15], 0x01              | 42 80 2c 38 01             |
    | sub byte [rax + 2 * rcx], 0x01              | 80 2c 48 01                |
    | sub byte [rax + 4 * rcx], 0x01              | 80 2c 88 01                |
    | sub byte [rax + 8 * rcx], 0x01              | 80 2c c8 01                |
    | sub byte [r8 + 1 * r9], 0x01                | 43 80 2c 08 01             |
    | sub byte [r8 + 2 * r9], 0x01                | 43 80 2c 48 01             |
    | sub byte [r8 + 4 * r9], 0x01                | 43 80 2c 88 01             |
    | sub byte [r8 + 8 * r9], 0x01                | 43 80 2c c8 01             |
    | sub byte [1 * rcx], 0x01                    | 80 2c 0d 00 00 00 00 01    |
    | sub byte [2 * rcx], 0x01                    | 80 2c 4d 00 00 00 00 01    |
    | sub byte [4 * rcx], 0x01                    | 80 2c 8d 00 00 00 00 01    |
    | sub byte [8 * rcx], 0x01                    | 80 2c cd 00 00 00 00 01    |
    | sub byte [1 * r9], 0x01                     | 42 80 2c 0d 00 00 00 00 01 |
    | sub byte [2 * r9], 0x01                     | 42 80 2c 4d 00 00 00 00 01 |
    | sub byte [4 * r9], 0x01                     | 42 80 2c 8d 00 00 00 00 01 |
    | sub byte [8 * r9], 0x01                     | 42 80 2c cd 00 00 00 00 01 |
    | sub byte [r13 + 8 * r12], 0x01              | 43 80 6c e5 00 01          |
    | sub byte [rsp + 4 * r15], 0x01              | 42 80 2c bc 01             |
    | sub byte [rax + 1 * rcx + 0x00], 0x01       | 80 6c 08 00 01             |
    | sub byte [rax + 1 * rcx - 0x00], 0x01       | 80 6c 08 00 01             |
    | sub byte [rax + 1 * rcx + 0x01], 0x01       | 80 6c 08 01 01             |
    | sub byte [rax + 1 * rcx - 0x01], 0x01       | 80 6c 08 ff 01             |
    | sub byte [rax + 1 * rcx + 0x00000001], 0x01 | 80 ac 08 01 00 00 00 01    |
    | sub byte [rax + 1 * rcx - 0x00000001], 0x01 | 80 ac 08 ff ff ff ff 01    |
    | sub byte [rax + 1 * rcx + 0x7f], 0x01       | 80 6c 08 7f 01             |
    | sub byte [rax + 1 * rcx - 0x7f], 0x01       | 80 6c 08 81 01             |
    | sub byte [rax + 1 * rcx + 0x80], 0x01       | 80 ac 08 80 00 00 00 01    |
    | sub byte [rax + 1 * rcx - 0x80], 0x01       | 80 6c 08 80 01             |
    | sub byte [rax + 1 * rcx - 0x81], 0x01       | 80 ac 08 7f ff ff ff 01    |
    | sub byte [rax + 1 * rcx + 0xff], 0x01       | 80 ac 08 ff 00 00 00 01    |
    | sub byte [rax + 1 * rcx - 0xff], 0x01       | 80 ac 08 01 ff ff ff 01    |
    | sub byte [rax + 1 * rcx + 0x7fffffff], 0x01 | 80 ac 08 ff ff ff 7f 01    |
    | sub byte [rax + 1 * rcx - 0x7fffffff], 0x01 | 80 ac 08 01 00 00 80 01    |
    | sub byte [rax + 1 * rcx - 0x80000000], 0x01 | 80 ac 08 00 00 00 80 01    |
    | sub byte [r10 + 0x7f], 0x01                 | 41 80 6a 7f 01             |
    | sub byte [r10 + 0x80], 0x01                 | 41 80 aa 80 00 00 00 01    |
    | sub byte [r10 - 0x80], 0x01                 | 41 80 6a 80 01             |
    | sub byte [r10 - 0x81], 0x01                 | 41 80 aa 7f ff ff ff 01    |
    | sub byte [rax], 0x00                        | 80 28 00                   |
    | sub byte [rax], 0x7f                        | 80 28 7f                   |
    | sub byte [rax], 0x80                        | 80 28 80                   |
    | sub byte [rax], 0xff                        | 80 28 ff                   |
    | sub byte [rcx], 0x7f                        | 80 29 7f                   |
    | sub byte [rdx], 0x80                        | 80 2a 80                   |
    | sub byte [rbx], 0xff                        | 80 2b ff                   |
    | sub byte [rsp], 0x00                        | 80 2c 24 00                |
    | sub byte [rsi], 0x7f                        | 80 2e 7f                   |
    | sub byte [rdi], 0x80                        | 80 2f 80                   |
    | sub byte [r8], 0xff                         | 41 80 28 ff                |
    | sub byte [r9], 0x00                         | 41 80 29 00                |
    | sub byte [r11], 0x7f                        | 41 80 2b 7f                |
    | sub byte [r12], 0x80                        | 41 80 2c 24 80             |
    | sub byte [r13], 0xff                        | 41 80 6d 00 ff             |
    | sub byte [r14], 0x00                        | 41 80 2e 00                |
    | sub byte [rax + 1 * rcx], 0x7f              | 80 2c 08 7f                |
    | sub byte [rcx + 1 * rcx], 0x80              | 80 2c 09 80                |
    | sub byte [rdx + 1 * rcx], 0xff              | 80 2c 0a ff                |
    | sub byte [rbx + 1 * rcx], 0x00              | 80 2c 0b 00                |
    | sub byte [rbp + 1 * rcx], 0x7f              | 80 6c 0d 00 7f             |
    | sub byte [rsi + 1 * rcx], 0x80              | 80 2c 0e 80                |
    | sub byte [rdi + 1 * rcx], 0xff              | 80 2c 0f ff                |
    | sub byte [r8 + 1 * rcx], 0x00               | 41 80 2c 08 00             |
    | sub byte [r10 + 1 * rcx], 0x7f              | 41 80 2c 0a 7f             |
    | sub byte [r11 + 1 * rcx], 0x80              | 41 80 2c 0b 80             |
    | sub byte [r12 + 1 * rcx], 0xff              | 41 80 2c 0c ff             |
    | sub byte [r13 + 1 * rcx], 0x00              | 41 80 6c 0d 00 00          |
    | sub byte [r15 + 1 * rcx], 0x7f              | 41 80 2c 0f 7f             |
    | sub byte [rax + 1 * rax], 0x80              | 80 2c 00 80                |
    | sub byte [rax + 1 * rdx], 0xff              | 80 2c 10 ff                |
    | sub byte [rax + 1 * rbx], 0x00              | 80 2c 18 00                |
    | sub byte [rax + 1 * rsi], 0x7f              | 80 2c 30 7f                |
    | sub byte [rax + 1 * rdi], 0x80              | 80 2c 38 80                |
    | sub byte [rax + 1 * r8], 0xff               | 42 80 2c 00 ff             |
    | sub byte [rax + 1 * r9], 0x00               | 42 80 2c 08 00             |
    | sub byte [rax + 1 * r11], 0x7f              | 42 80 2c 18 7f             |
    | sub byte [rax + 1 * r12], 0x80              | 42 80 2c 20 80             |
    | sub byte [rax + 1 * r13], 0xff              | 42 80 2c 28 ff             |
    | sub byte [rax + 1 * r14], 0x00              | 42 80 2c 30 00             |
    | sub byte [rax + 2 * rcx], 0x7f              | 80 2c 48 7f                |
    | sub byte [rax + 4 * rcx], 0x80              | 80 2c 88 80                |
    | sub byte [rax + 8 * rcx], 0xff              | 80 2c c8 ff                |
    | sub byte [r8 + 1 * r9], 0x00                | 43 80 2c 08 00             |
    | sub byte [r8 + 4 * r9], 0x7f                | 43 80 2c 88 7f             |
    | sub byte [r8 + 8 * r9], 0x80                | 43 80 2c c8 80             |
    | sub byte [1 * rcx], 0xff                    | 80 2c 0d 00 00 00 00 ff    |
    | sub byte [2 * rcx], 0x00                    | 80 2c 4d 00 00 00 00 00    |
    | sub byte [8 * rcx], 0x7f                    | 80 2c cd 00 00 00 00 7f    |
    | sub byte [1 * r9], 0x80                     | 42 80 2c 0d 00 00 00 00 80 |
    | sub byte [2 * r9], 0xff                     | 42 80 2c 4d 00 00 00 00 ff |
    | sub byte [4 * r9], 0x00                     | 42 80 2c 8d 00 00 00 00 00 |
    | sub byte [r13 + 8 * r12], 0x7f              | 43 80 6c e5 00 7f          |
    | sub byte [rsp + 4 * r15], 0x80              | 42 80 2c bc 80             |
    | sub byte [rax + 1 * rcx + 0x00], 0xff       | 80 6c 08 00 ff             |
    | sub byte [rax + 1 * rcx - 0x00], 0x00       | 80 6c 08 00 00             |
    | sub byte [rax + 1 * rcx - 0x01], 0x7f       | 80 6c 08 ff 7f             |
    | sub byte [rax + 1 * rcx + 0x00000001], 0x80 | 80 ac 08 01 00 00 00 80    |
    | sub byte [rax + 1 * rcx - 0x00000001], 0xff | 80 ac 08 ff ff ff ff ff    |
    | sub byte [rax + 1 * rcx + 0x7f], 0x00       | 80 6c 08 7f 00             |
    | sub byte [rax + 1 * rcx + 0x80], 0x7f       | 80 ac 08 80 00 00 00 7f    |
    | sub byte [rax + 1 * rcx - 0x80], 0x80       | 80 6c 08 80 80             |
    | sub byte [rax + 1 * rcx - 0x81], 0xff       | 80 ac 08 7f ff ff ff ff    |
    | sub byte [rax + 1 * rcx + 0xff], 0x00       | 80 ac 08 ff 00 00 00 00    |
    | sub byte [rax + 1 * rcx + 0x7fffffff], 0x7f | 80 ac 08 ff ff ff 7f 7f    |
    | sub byte [rax + 1 * rcx - 0x7fffffff], 0x80 | 80 ac 08 01 00 00 80 80    |
    | sub byte [rax + 1 * rcx - 0x80000000], 0xff | 80 ac 08 00 00 00 80 ff    |
    | sub byte [r10 + 0x7f], 0x00                 | 41 80 6a 7f 00             |
    | sub byte [r10 - 0x80], 0x7f                 | 41 80 6a 80 7f             |
    | sub byte [r10 - 0x81], 0x80                 | 41 80 aa 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sub_addr8_imm8():
    encode(SUB_ADDR8_IMM8)


SUB_ADDR8_REG8 = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | sub byte [rax], cl                         | 28 08                   |
    | sub byte [rcx], cl                         | 28 09                   |
    | sub byte [rdx], cl                         | 28 0a                   |
    | sub byte [rbx], cl                         | 28 0b                   |
    | sub byte [rsp], cl                         | 28 0c 24                |
    | sub byte [rbp], cl                         | 28 4d 00                |
    | sub byte [rsi], cl                         | 28 0e                   |
    | sub byte [rdi], cl                         | 28 0f                   |
    | sub byte [r8], cl                          | 41 28 08                |
    | sub byte [r9], cl                          | 41 28 09                |
    | sub byte [r10], cl                         | 41 28 0a                |
    | sub byte [r11], cl                         | 41 28 0b                |
    | sub byte [r12], cl                         | 41 28 0c 24             |
    | sub byte [r13], cl                         | 41 28 4d 00             |
    | sub byte [r14], cl                         | 41 28 0e                |
    | sub byte [r15], cl                         | 41 28 0f                |
    | sub byte [rax + 1 * rcx], cl               | 28 0c 08                |
    | sub byte [rcx + 1 * rcx], cl               | 28 0c 09                |
    | sub byte [rdx + 1 * rcx], cl               | 28 0c 0a                |
    | sub byte [rbx + 1 * rcx], cl               | 28 0c 0b                |
    | sub byte [rsp + 1 * rcx], cl               | 28 0c 0c                |
    | sub byte [rbp + 1 * rcx], cl               | 28 4c 0d 00             |
    | sub byte [rsi + 1 * rcx], cl               | 28 0c 0e                |
    | sub byte [rdi + 1 * rcx], cl               | 28 0c 0f                |
    | sub byte [r8 + 1 * rcx], cl                | 41 28 0c 08             |
    | sub byte [r9 + 1 * rcx], cl                | 41 28 0c 09             |
    | sub byte [r10 + 1 * rcx], cl               | 41 28 0c 0a             |
    | sub byte [r11 + 1 * rcx], cl               | 41 28 0c 0b             |
    | sub byte [r12 + 1 * rcx], cl               | 41 28 0c 0c             |
    | sub byte [r13 + 1 * rcx], cl               | 41 28 4c 0d 00          |
    | sub byte [r14 + 1 * rcx], cl               | 41 28 0c 0e             |
    | sub byte [r15 + 1 * rcx], cl               | 41 28 0c 0f             |
    | sub byte [rax + 1 * rax], cl               | 28 0c 00                |
    | sub byte [rax + 1 * rdx], cl               | 28 0c 10                |
    | sub byte [rax + 1 * rbx], cl               | 28 0c 18                |
    | sub byte [rax + 1 * rbp], cl               | 28 0c 28                |
    | sub byte [rax + 1 * rsi], cl               | 28 0c 30                |
    | sub byte [rax + 1 * rdi], cl               | 28 0c 38                |
    | sub byte [rax + 1 * r8], cl                | 42 28 0c 00             |
    | sub byte [rax + 1 * r9], cl                | 42 28 0c 08             |
    | sub byte [rax + 1 * r10], cl               | 42 28 0c 10             |
    | sub byte [rax + 1 * r11], cl               | 42 28 0c 18             |
    | sub byte [rax + 1 * r12], cl               | 42 28 0c 20             |
    | sub byte [rax + 1 * r13], cl               | 42 28 0c 28             |
    | sub byte [rax + 1 * r14], cl               | 42 28 0c 30             |
    | sub byte [rax + 1 * r15], cl               | 42 28 0c 38             |
    | sub byte [rax + 2 * rcx], cl               | 28 0c 48                |
    | sub byte [rax + 4 * rcx], cl               | 28 0c 88                |
    | sub byte [rax + 8 * rcx], cl               | 28 0c c8                |
    | sub byte [r8 + 1 * r9], cl                 | 43 28 0c 08             |
    | sub byte [r8 + 2 * r9], cl                 | 43 28 0c 48             |
    | sub byte [r8 + 4 * r9], cl                 | 43 28 0c 88             |
    | sub byte [r8 + 8 * r9], cl                 | 43 28 0c c8             |
    | sub byte [1 * rcx], cl                     | 28 0c 0d 00 00 00 00    |
    | sub byte [2 * rcx], cl                     | 28 0c 4d 00 00 00 00    |
    | sub byte [4 * rcx], cl                     | 28 0c 8d 00 00 00 00    |
    | sub byte [8 * rcx], cl                     | 28 0c cd 00 00 00 00    |
    | sub byte [1 * r9], cl                      | 42 28 0c 0d 00 00 00 00 |
    | sub byte [2 * r9], cl                      | 42 28 0c 4d 00 00 00 00 |
    | sub byte [4 * r9], cl                      | 42 28 0c 8d 00 00 00 00 |
    | sub byte [8 * r9], cl                      | 42 28 0c cd 00 00 00 00 |
    | sub byte [r13 + 8 * r12], cl               | 43 28 4c e5 00          |
    | sub byte [rsp + 4 * r15], cl               | 42 28 0c bc             |
    | sub byte [rax + 1 * rcx + 0x00], cl        | 28 4c 08 00             |
    | sub byte [rax + 1 * rcx - 0x00], cl        | 28 4c 08 00             |
    | sub byte [rax + 1 * rcx + 0x01], cl        | 28 4c 08 01             |
    | sub byte [rax + 1 * rcx - 0x01], cl        | 28 4c 08 ff             |
    | sub byte [rax + 1 * rcx + 0x00000001], cl  | 28 8c 08 01 00 00 00    |
    | sub byte [rax + 1 * rcx - 0x00000001], cl  | 28 8c 08 ff ff ff ff    |
    | sub byte [rax + 1 * rcx + 0x7f], cl        | 28 4c 08 7f             |
    | sub byte [rax + 1 * rcx - 0x7f], cl        | 28 4c 08 81             |
    | sub byte [rax + 1 * rcx + 0x80], cl        | 28 8c 08 80 00 00 00    |
    | sub byte [rax + 1 * rcx - 0x80], cl        | 28 4c 08 80             |
    | sub byte [rax + 1 * rcx - 0x81], cl        | 28 8c 08 7f ff ff ff    |
    | sub byte [rax + 1 * rcx + 0xff], cl        | 28 8c 08 ff 00 00 00    |
    | sub byte [rax + 1 * rcx - 0xff], cl        | 28 8c 08 01 ff ff ff    |
    | sub byte [rax + 1 * rcx + 0x7fffffff], cl  | 28 8c 08 ff ff ff 7f    |
    | sub byte [rax + 1 * rcx - 0x7fffffff], cl  | 28 8c 08 01 00 00 80    |
    | sub byte [rax + 1 * rcx - 0x80000000], cl  | 28 8c 08 00 00 00 80    |
    | sub byte [r10 + 0x7f], cl                  | 41 28 4a 7f             |
    | sub byte [r10 + 0x80], cl                  | 41 28 8a 80 00 00 00    |
    | sub byte [r10 - 0x80], cl                  | 41 28 4a 80             |
    | sub byte [r10 - 0x81], cl                  | 41 28 8a 7f ff ff ff    |
    | sub byte [rax], al                         | 28 00                   |
    | sub byte [rax], dl                         | 28 10                   |
    | sub byte [rax], bl                         | 28 18                   |
    | sub byte [rax], spl                        | 40 28 20                |
    | sub byte [rax], bpl                        | 40 28 28                |
    | sub byte [rax], sil                        | 40 28 30                |
    | sub byte [rax], dil                        | 40 28 38                |
    | sub byte [rax], r8b                        | 44 28 00                |
    | sub byte [rax], r9b                        | 44 28 08                |
    | sub byte [rax], r10b                       | 44 28 10                |
    | sub byte [rax], r11b                       | 44 28 18                |
    | sub byte [rax], r12b                       | 44 28 20                |
    | sub byte [rax], r13b                       | 44 28 28                |
    | sub byte [rax], r14b                       | 44 28 30                |
    | sub byte [rax], r15b                       | 44 28 38                |
    | sub byte [rax], ah                         | 28 20                   |
    | sub byte [rax], ch                         | 28 28                   |
    | sub byte [rax], dh                         | 28 30                   |
    | sub byte [rax], bh                         | 28 38                   |
    | sub byte [rcx], dl                         | 28 11                   |
    | sub byte [rdx], bl                         | 28 1a                   |
    | sub byte [rbx], spl                        | 40 28 23                |
    | sub byte [rsp], bpl                        | 40 28 2c 24             |
    | sub byte [rbp], sil                        | 40 28 75 00             |
    | sub byte [rsi], dil                        | 40 28 3e                |
    | sub byte [rdi], r8b                        | 44 28 07                |
    | sub byte [r8], r9b                         | 45 28 08                |
    | sub byte [r9], r10b                        | 45 28 11                |
    | sub byte [r10], r11b                       | 45 28 1a                |
    | sub byte [r11], r12b                       | 45 28 23                |
    | sub byte [r12], r13b                       | 45 28 2c 24             |
    | sub byte [r13], r14b                       | 45 28 75 00             |
    | sub byte [r14], r15b                       | 45 28 3e                |
    | sub byte [r15], ah                         | !! !! !!                |
    | sub byte [rax + 1 * rcx], ch               | 28 2c 08                |
    | sub byte [rcx + 1 * rcx], dh               | 28 34 09                |
    | sub byte [rdx + 1 * rcx], bh               | 28 3c 0a                |
    | sub byte [rbx + 1 * rcx], al               | 28 04 0b                |
    | sub byte [rbp + 1 * rcx], dl               | 28 54 0d 00             |
    | sub byte [rsi + 1 * rcx], bl               | 28 1c 0e                |
    | sub byte [rdi + 1 * rcx], spl              | 40 28 24 0f             |
    | sub byte [r8 + 1 * rcx], bpl               | 41 28 2c 08             |
    | sub byte [r9 + 1 * rcx], sil               | 41 28 34 09             |
    | sub byte [r10 + 1 * rcx], dil              | 41 28 3c 0a             |
    | sub byte [r11 + 1 * rcx], r8b              | 45 28 04 0b             |
    | sub byte [r12 + 1 * rcx], r9b              | 45 28 0c 0c             |
    | sub byte [r13 + 1 * rcx], r10b             | 45 28 54 0d 00          |
    | sub byte [r14 + 1 * rcx], r11b             | 45 28 1c 0e             |
    | sub byte [r15 + 1 * rcx], r12b             | 45 28 24 0f             |
    | sub byte [rax + 1 * rax], r13b             | 44 28 2c 00             |
    | sub byte [rax + 1 * rdx], r14b             | 44 28 34 10             |
    | sub byte [rax + 1 * rbx], r15b             | 44 28 3c 18             |
    | sub byte [rax + 1 * rbp], ah               | 28 24 28                |
    | sub byte [rax + 1 * rsi], ch               | 28 2c 30                |
    | sub byte [rax + 1 * rdi], dh               | 28 34 38                |
    | sub byte [rax + 1 * r8], bh                | !! !! !!                |
    | sub byte [rax + 1 * r9], al                | 42 28 04 08             |
    | sub byte [rax + 1 * r11], dl               | 42 28 14 18             |
    | sub byte [rax + 1 * r12], bl               | 42 28 1c 20             |
    | sub byte [rax + 1 * r13], spl              | 42 28 24 28             |
    | sub byte [rax + 1 * r14], bpl              | 42 28 2c 30             |
    | sub byte [rax + 1 * r15], sil              | 42 28 34 38             |
    | sub byte [rax + 2 * rcx], dil              | 40 28 3c 48             |
    | sub byte [rax + 4 * rcx], r8b              | 44 28 04 88             |
    | sub byte [rax + 8 * rcx], r9b              | 44 28 0c c8             |
    | sub byte [r8 + 1 * r9], r10b               | 47 28 14 08             |
    | sub byte [r8 + 2 * r9], r11b               | 47 28 1c 48             |
    | sub byte [r8 + 4 * r9], r12b               | 47 28 24 88             |
    | sub byte [r8 + 8 * r9], r13b               | 47 28 2c c8             |
    | sub byte [1 * rcx], r14b                   | 44 28 34 0d 00 00 00 00 |
    | sub byte [2 * rcx], r15b                   | 44 28 3c 4d 00 00 00 00 |
    | sub byte [4 * rcx], ah                     | 28 24 8d 00 00 00 00    |
    | sub byte [8 * rcx], ch                     | 28 2c cd 00 00 00 00    |
    | sub byte [1 * r9], dh                      | !! !! !!                |
    | sub byte [2 * r9], bh                      | !! !! !!                |
    | sub byte [4 * r9], al                      | 42 28 04 8d 00 00 00 00 |
    | sub byte [r13 + 8 * r12], dl               | 43 28 54 e5 00          |
    | sub byte [rsp + 4 * r15], bl               | 42 28 1c bc             |
    | sub byte [rax + 1 * rcx + 0x00], spl       | 40 28 64 08 00          |
    | sub byte [rax + 1 * rcx - 0x00], bpl       | 40 28 6c 08 00          |
    | sub byte [rax + 1 * rcx + 0x01], sil       | 40 28 74 08 01          |
    | sub byte [rax + 1 * rcx - 0x01], dil       | 40 28 7c 08 ff          |
    | sub byte [rax + 1 * rcx + 0x00000001], r8b | 44 28 84 08 01 00 00 00 |
    | sub byte [rax + 1 * rcx - 0x00000001], r9b | 44 28 8c 08 ff ff ff ff |
    | sub byte [rax + 1 * rcx + 0x7f], r10b      | 44 28 54 08 7f          |
    | sub byte [rax + 1 * rcx - 0x7f], r11b      | 44 28 5c 08 81          |
    | sub byte [rax + 1 * rcx + 0x80], r12b      | 44 28 a4 08 80 00 00 00 |
    | sub byte [rax + 1 * rcx - 0x80], r13b      | 44 28 6c 08 80          |
    | sub byte [rax + 1 * rcx - 0x81], r14b      | 44 28 b4 08 7f ff ff ff |
    | sub byte [rax + 1 * rcx + 0xff], r15b      | 44 28 bc 08 ff 00 00 00 |
    | sub byte [rax + 1 * rcx - 0xff], ah        | 28 a4 08 01 ff ff ff    |
    | sub byte [rax + 1 * rcx + 0x7fffffff], ch  | 28 ac 08 ff ff ff 7f    |
    | sub byte [rax + 1 * rcx - 0x7fffffff], dh  | 28 b4 08 01 00 00 80    |
    | sub byte [rax + 1 * rcx - 0x80000000], bh  | 28 bc 08 00 00 00 80    |
    | sub byte [r10 + 0x7f], al                  | 41 28 42 7f             |
    | sub byte [r10 - 0x80], dl                  | 41 28 52 80             |
    | sub byte [r10 - 0x81], bl                  | 41 28 9a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_sub_addr8_reg8():
    encode(SUB_ADDR8_REG8)
