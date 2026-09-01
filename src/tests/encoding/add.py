from tests.encoding.core import encode, exhaust


def can_exhaust_add():
    exhaust(
        ADD_ADDR16_IMM16,
        ADD_ADDR16_IMM8,
        ADD_ADDR16_REG16,
        ADD_ADDR32_IMM32,
        ADD_ADDR32_IMM8,
        ADD_ADDR32_REG32,
        ADD_ADDR64_IMM32,
        ADD_ADDR64_IMM8,
        ADD_ADDR64_REG64,
        ADD_ADDR8_IMM8,
        ADD_ADDR8_REG8,
        ADD_REG16_ADDR16,
        ADD_REG16_IMM16,
        ADD_REG16_IMM8,
        ADD_REG16_REG16,
        ADD_REG32_ADDR32,
        ADD_REG32_IMM32,
        ADD_REG32_IMM8,
        ADD_REG32_REG32,
        ADD_REG64_ADDR64,
        ADD_REG64_IMM32,
        ADD_REG64_IMM8,
        ADD_REG64_REG64,
        ADD_REG8_ADDR8,
        ADD_REG8_IMM8,
        ADD_REG8_REG8,
    )


ADD_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | add rax, 0x01 | 48 83 c0 01 | *** | add rax, 0x00 | 48 83 c0 00 |
    | add rcx, 0x01 | 48 83 c1 01 | *** | add rax, 0x7f | 48 83 c0 7f |
    | add rdx, 0x01 | 48 83 c2 01 | *** | add rax, 0x80 | 48 83 c0 80 |
    | add rbx, 0x01 | 48 83 c3 01 | *** | add rax, 0xff | 48 83 c0 ff |
    | add rsp, 0x01 | 48 83 c4 01 | *** | add rcx, 0x7f | 48 83 c1 7f |
    | add rbp, 0x01 | 48 83 c5 01 | *** | add rdx, 0x80 | 48 83 c2 80 |
    | add rsi, 0x01 | 48 83 c6 01 | *** | add rbx, 0xff | 48 83 c3 ff |
    | add rdi, 0x01 | 48 83 c7 01 | *** | add rsp, 0x00 | 48 83 c4 00 |
    | add r8, 0x01  | 49 83 c0 01 | *** | add rsi, 0x7f | 48 83 c6 7f |
    | add r9, 0x01  | 49 83 c1 01 | *** | add rdi, 0x80 | 48 83 c7 80 |
    | add r10, 0x01 | 49 83 c2 01 | *** | add r8, 0xff  | 49 83 c0 ff |
    | add r11, 0x01 | 49 83 c3 01 | *** | add r9, 0x00  | 49 83 c1 00 |
    | add r12, 0x01 | 49 83 c4 01 | *** | add r11, 0x7f | 49 83 c3 7f |
    | add r13, 0x01 | 49 83 c5 01 | *** | add r12, 0x80 | 49 83 c4 80 |
    | add r14, 0x01 | 49 83 c6 01 | *** | add r13, 0xff | 49 83 c5 ff |
    | add r15, 0x01 | 49 83 c7 01 | *** | add r14, 0x00 | 49 83 c6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_add_reg64_imm8():
    encode(ADD_REG64_IMM8)


ADD_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | add rax, 0x00000001 | 48 05 01 00 00 00    | *** | add rax, 0x00007fff | 48 05 ff 7f 00 00    |
    | add rcx, 0x00000001 | 48 81 c1 01 00 00 00 | *** | add rax, 0x00008000 | 48 05 00 80 00 00    |
    | add rdx, 0x00000001 | 48 81 c2 01 00 00 00 | *** | add rax, 0x0000ffff | 48 05 ff ff 00 00    |
    | add rbx, 0x00000001 | 48 81 c3 01 00 00 00 | *** | add rax, 0x00010000 | 48 05 00 00 01 00    |
    | add rsp, 0x00000001 | 48 81 c4 01 00 00 00 | *** | add rax, 0x7fffffff | 48 05 ff ff ff 7f    |
    | add rbp, 0x00000001 | 48 81 c5 01 00 00 00 | *** | add rax, 0x80000000 | 48 05 00 00 00 80    |
    | add rsi, 0x00000001 | 48 81 c6 01 00 00 00 | *** | add rax, 0xffffffff | 48 05 ff ff ff ff    |
    | add rdi, 0x00000001 | 48 81 c7 01 00 00 00 | *** | add rcx, 0x0000007f | 48 81 c1 7f 00 00 00 |
    | add r8, 0x00000001  | 49 81 c0 01 00 00 00 | *** | add rdx, 0x00000080 | 48 81 c2 80 00 00 00 |
    | add r9, 0x00000001  | 49 81 c1 01 00 00 00 | *** | add rbx, 0x000000ff | 48 81 c3 ff 00 00 00 |
    | add r10, 0x00000001 | 49 81 c2 01 00 00 00 | *** | add rsp, 0x00000100 | 48 81 c4 00 01 00 00 |
    | add r11, 0x00000001 | 49 81 c3 01 00 00 00 | *** | add rbp, 0x00007fff | 48 81 c5 ff 7f 00 00 |
    | add r12, 0x00000001 | 49 81 c4 01 00 00 00 | *** | add rsi, 0x00008000 | 48 81 c6 00 80 00 00 |
    | add r13, 0x00000001 | 49 81 c5 01 00 00 00 | *** | add rdi, 0x0000ffff | 48 81 c7 ff ff 00 00 |
    | add r14, 0x00000001 | 49 81 c6 01 00 00 00 | *** | add r8, 0x00010000  | 49 81 c0 00 00 01 00 |
    | add r15, 0x00000001 | 49 81 c7 01 00 00 00 | *** | add r9, 0x7fffffff  | 49 81 c1 ff ff ff 7f |
    | add rax, 0x00000000 | 48 05 00 00 00 00    | *** | add r10, 0x80000000 | 49 81 c2 00 00 00 80 |
    | add rax, 0x0000007f | 48 05 7f 00 00 00    | *** | add r11, 0xffffffff | 49 81 c3 ff ff ff ff |
    | add rax, 0x00000080 | 48 05 80 00 00 00    | *** | add r12, 0x00000000 | 49 81 c4 00 00 00 00 |
    | add rax, 0x000000ff | 48 05 ff 00 00 00    | *** | add r14, 0x0000007f | 49 81 c6 7f 00 00 00 |
    | add rax, 0x00000100 | 48 05 00 01 00 00    | *** | add r15, 0x00000080 | 49 81 c7 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_add_reg64_imm32():
    encode(ADD_REG64_IMM32)


ADD_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | add rax, rcx | 48 01 c8 | *** | add rax, r8  | 4c 01 c0 |
    | add rcx, rcx | 48 01 c9 | *** | add rax, r9  | 4c 01 c8 |
    | add rdx, rcx | 48 01 ca | *** | add rax, r10 | 4c 01 d0 |
    | add rbx, rcx | 48 01 cb | *** | add rax, r11 | 4c 01 d8 |
    | add rsp, rcx | 48 01 cc | *** | add rax, r12 | 4c 01 e0 |
    | add rbp, rcx | 48 01 cd | *** | add rax, r13 | 4c 01 e8 |
    | add rsi, rcx | 48 01 ce | *** | add rax, r14 | 4c 01 f0 |
    | add rdi, rcx | 48 01 cf | *** | add rax, r15 | 4c 01 f8 |
    | add r8, rcx  | 49 01 c8 | *** | add rcx, rdx | 48 01 d1 |
    | add r9, rcx  | 49 01 c9 | *** | add rdx, rbx | 48 01 da |
    | add r10, rcx | 49 01 ca | *** | add rbx, rsp | 48 01 e3 |
    | add r11, rcx | 49 01 cb | *** | add rsp, rbp | 48 01 ec |
    | add r12, rcx | 49 01 cc | *** | add rbp, rsi | 48 01 f5 |
    | add r13, rcx | 49 01 cd | *** | add rsi, rdi | 48 01 fe |
    | add r14, rcx | 49 01 ce | *** | add rdi, r8  | 4c 01 c7 |
    | add r15, rcx | 49 01 cf | *** | add r8, r9   | 4d 01 c8 |
    | add rax, rax | 48 01 c0 | *** | add r9, r10  | 4d 01 d1 |
    | add rax, rdx | 48 01 d0 | *** | add r10, r11 | 4d 01 da |
    | add rax, rbx | 48 01 d8 | *** | add r11, r12 | 4d 01 e3 |
    | add rax, rsp | 48 01 e0 | *** | add r12, r13 | 4d 01 ec |
    | add rax, rbp | 48 01 e8 | *** | add r13, r14 | 4d 01 f5 |
    | add rax, rsi | 48 01 f0 | *** | add r14, r15 | 4d 01 fe |
    | add rax, rdi | 48 01 f8 | *** | add r15, rax | 49 01 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_add_reg64_reg64():
    encode(ADD_REG64_REG64)


ADD_REG64_ADDR64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | add rax, qword [rcx]                        | 48 03 01                |
    | add rcx, qword [rcx]                        | 48 03 09                |
    | add rdx, qword [rcx]                        | 48 03 11                |
    | add rbx, qword [rcx]                        | 48 03 19                |
    | add rsp, qword [rcx]                        | 48 03 21                |
    | add rbp, qword [rcx]                        | 48 03 29                |
    | add rsi, qword [rcx]                        | 48 03 31                |
    | add rdi, qword [rcx]                        | 48 03 39                |
    | add r8, qword [rcx]                         | 4c 03 01                |
    | add r9, qword [rcx]                         | 4c 03 09                |
    | add r10, qword [rcx]                        | 4c 03 11                |
    | add r11, qword [rcx]                        | 4c 03 19                |
    | add r12, qword [rcx]                        | 4c 03 21                |
    | add r13, qword [rcx]                        | 4c 03 29                |
    | add r14, qword [rcx]                        | 4c 03 31                |
    | add r15, qword [rcx]                        | 4c 03 39                |
    | add rax, qword [rax]                        | 48 03 00                |
    | add rax, qword [rdx]                        | 48 03 02                |
    | add rax, qword [rbx]                        | 48 03 03                |
    | add rax, qword [rsp]                        | 48 03 04 24             |
    | add rax, qword [rbp]                        | 48 03 45 00             |
    | add rax, qword [rsi]                        | 48 03 06                |
    | add rax, qword [rdi]                        | 48 03 07                |
    | add rax, qword [r8]                         | 49 03 00                |
    | add rax, qword [r9]                         | 49 03 01                |
    | add rax, qword [r10]                        | 49 03 02                |
    | add rax, qword [r11]                        | 49 03 03                |
    | add rax, qword [r12]                        | 49 03 04 24             |
    | add rax, qword [r13]                        | 49 03 45 00             |
    | add rax, qword [r14]                        | 49 03 06                |
    | add rax, qword [r15]                        | 49 03 07                |
    | add rax, qword [rax + 1 * rcx]              | 48 03 04 08             |
    | add rax, qword [rcx + 1 * rcx]              | 48 03 04 09             |
    | add rax, qword [rdx + 1 * rcx]              | 48 03 04 0a             |
    | add rax, qword [rbx + 1 * rcx]              | 48 03 04 0b             |
    | add rax, qword [rsp + 1 * rcx]              | 48 03 04 0c             |
    | add rax, qword [rbp + 1 * rcx]              | 48 03 44 0d 00          |
    | add rax, qword [rsi + 1 * rcx]              | 48 03 04 0e             |
    | add rax, qword [rdi + 1 * rcx]              | 48 03 04 0f             |
    | add rax, qword [r8 + 1 * rcx]               | 49 03 04 08             |
    | add rax, qword [r9 + 1 * rcx]               | 49 03 04 09             |
    | add rax, qword [r10 + 1 * rcx]              | 49 03 04 0a             |
    | add rax, qword [r11 + 1 * rcx]              | 49 03 04 0b             |
    | add rax, qword [r12 + 1 * rcx]              | 49 03 04 0c             |
    | add rax, qword [r13 + 1 * rcx]              | 49 03 44 0d 00          |
    | add rax, qword [r14 + 1 * rcx]              | 49 03 04 0e             |
    | add rax, qword [r15 + 1 * rcx]              | 49 03 04 0f             |
    | add rax, qword [rax + 1 * rax]              | 48 03 04 00             |
    | add rax, qword [rax + 1 * rdx]              | 48 03 04 10             |
    | add rax, qword [rax + 1 * rbx]              | 48 03 04 18             |
    | add rax, qword [rax + 1 * rbp]              | 48 03 04 28             |
    | add rax, qword [rax + 1 * rsi]              | 48 03 04 30             |
    | add rax, qword [rax + 1 * rdi]              | 48 03 04 38             |
    | add rax, qword [rax + 1 * r8]               | 4a 03 04 00             |
    | add rax, qword [rax + 1 * r9]               | 4a 03 04 08             |
    | add rax, qword [rax + 1 * r10]              | 4a 03 04 10             |
    | add rax, qword [rax + 1 * r11]              | 4a 03 04 18             |
    | add rax, qword [rax + 1 * r12]              | 4a 03 04 20             |
    | add rax, qword [rax + 1 * r13]              | 4a 03 04 28             |
    | add rax, qword [rax + 1 * r14]              | 4a 03 04 30             |
    | add rax, qword [rax + 1 * r15]              | 4a 03 04 38             |
    | add rax, qword [rax + 2 * rcx]              | 48 03 04 48             |
    | add rax, qword [rax + 4 * rcx]              | 48 03 04 88             |
    | add rax, qword [rax + 8 * rcx]              | 48 03 04 c8             |
    | add rax, qword [r8 + 1 * r9]                | 4b 03 04 08             |
    | add rax, qword [r8 + 2 * r9]                | 4b 03 04 48             |
    | add rax, qword [r8 + 4 * r9]                | 4b 03 04 88             |
    | add rax, qword [r8 + 8 * r9]                | 4b 03 04 c8             |
    | add rax, qword [1 * rcx]                    | 48 03 04 0d 00 00 00 00 |
    | add rax, qword [2 * rcx]                    | 48 03 04 4d 00 00 00 00 |
    | add rax, qword [4 * rcx]                    | 48 03 04 8d 00 00 00 00 |
    | add rax, qword [8 * rcx]                    | 48 03 04 cd 00 00 00 00 |
    | add rax, qword [1 * r9]                     | 4a 03 04 0d 00 00 00 00 |
    | add rax, qword [2 * r9]                     | 4a 03 04 4d 00 00 00 00 |
    | add rax, qword [4 * r9]                     | 4a 03 04 8d 00 00 00 00 |
    | add rax, qword [8 * r9]                     | 4a 03 04 cd 00 00 00 00 |
    | add rax, qword [r13 + 8 * r12]              | 4b 03 44 e5 00          |
    | add rax, qword [rsp + 4 * r15]              | 4a 03 04 bc             |
    | add rax, qword [rax + 1 * rcx + 0x00]       | 48 03 44 08 00          |
    | add rax, qword [rax + 1 * rcx - 0x00]       | 48 03 44 08 00          |
    | add rax, qword [rax + 1 * rcx + 0x01]       | 48 03 44 08 01          |
    | add rax, qword [rax + 1 * rcx - 0x01]       | 48 03 44 08 ff          |
    | add rax, qword [rax + 1 * rcx + 0x00000001] | 48 03 84 08 01 00 00 00 |
    | add rax, qword [rax + 1 * rcx - 0x00000001] | 48 03 84 08 ff ff ff ff |
    | add rax, qword [rax + 1 * rcx + 0x7f]       | 48 03 44 08 7f          |
    | add rax, qword [rax + 1 * rcx - 0x7f]       | 48 03 44 08 81          |
    | add rax, qword [rax + 1 * rcx + 0x80]       | 48 03 84 08 80 00 00 00 |
    | add rax, qword [rax + 1 * rcx - 0x80]       | 48 03 44 08 80          |
    | add rax, qword [rax + 1 * rcx - 0x81]       | 48 03 84 08 7f ff ff ff |
    | add rax, qword [rax + 1 * rcx + 0xff]       | 48 03 84 08 ff 00 00 00 |
    | add rax, qword [rax + 1 * rcx - 0xff]       | 48 03 84 08 01 ff ff ff |
    | add rax, qword [rax + 1 * rcx + 0x7fffffff] | 48 03 84 08 ff ff ff 7f |
    | add rax, qword [rax + 1 * rcx - 0x7fffffff] | 48 03 84 08 01 00 00 80 |
    | add rax, qword [rax + 1 * rcx - 0x80000000] | 48 03 84 08 00 00 00 80 |
    | add rax, qword [r10 + 0x7f]                 | 49 03 42 7f             |
    | add rax, qword [r10 + 0x80]                 | 49 03 82 80 00 00 00    |
    | add rax, qword [r10 - 0x80]                 | 49 03 42 80             |
    | add rax, qword [r10 - 0x81]                 | 49 03 82 7f ff ff ff    |
    | add rcx, qword [rdx]                        | 48 03 0a                |
    | add rdx, qword [rbx]                        | 48 03 13                |
    | add rbx, qword [rsp]                        | 48 03 1c 24             |
    | add rsp, qword [rbp]                        | 48 03 65 00             |
    | add rbp, qword [rsi]                        | 48 03 2e                |
    | add rsi, qword [rdi]                        | 48 03 37                |
    | add rdi, qword [r8]                         | 49 03 38                |
    | add r8, qword [r9]                          | 4d 03 01                |
    | add r9, qword [r10]                         | 4d 03 0a                |
    | add r10, qword [r11]                        | 4d 03 13                |
    | add r11, qword [r12]                        | 4d 03 1c 24             |
    | add r12, qword [r13]                        | 4d 03 65 00             |
    | add r13, qword [r14]                        | 4d 03 2e                |
    | add r14, qword [r15]                        | 4d 03 37                |
    | add r15, qword [rax + 1 * rcx]              | 4c 03 3c 08             |
    | add rcx, qword [rdx + 1 * rcx]              | 48 03 0c 0a             |
    | add rdx, qword [rbx + 1 * rcx]              | 48 03 14 0b             |
    | add rbx, qword [rsp + 1 * rcx]              | 48 03 1c 0c             |
    | add rsp, qword [rbp + 1 * rcx]              | 48 03 64 0d 00          |
    | add rbp, qword [rsi + 1 * rcx]              | 48 03 2c 0e             |
    | add rsi, qword [rdi + 1 * rcx]              | 48 03 34 0f             |
    | add rdi, qword [r8 + 1 * rcx]               | 49 03 3c 08             |
    | add r8, qword [r9 + 1 * rcx]                | 4d 03 04 09             |
    | add r9, qword [r10 + 1 * rcx]               | 4d 03 0c 0a             |
    | add r10, qword [r11 + 1 * rcx]              | 4d 03 14 0b             |
    | add r11, qword [r12 + 1 * rcx]              | 4d 03 1c 0c             |
    | add r12, qword [r13 + 1 * rcx]              | 4d 03 64 0d 00          |
    | add r13, qword [r14 + 1 * rcx]              | 4d 03 2c 0e             |
    | add r14, qword [r15 + 1 * rcx]              | 4d 03 34 0f             |
    | add r15, qword [rax + 1 * rax]              | 4c 03 3c 00             |
    | add rcx, qword [rax + 1 * rbx]              | 48 03 0c 18             |
    | add rdx, qword [rax + 1 * rbp]              | 48 03 14 28             |
    | add rbx, qword [rax + 1 * rsi]              | 48 03 1c 30             |
    | add rsp, qword [rax + 1 * rdi]              | 48 03 24 38             |
    | add rbp, qword [rax + 1 * r8]               | 4a 03 2c 00             |
    | add rsi, qword [rax + 1 * r9]               | 4a 03 34 08             |
    | add rdi, qword [rax + 1 * r10]              | 4a 03 3c 10             |
    | add r8, qword [rax + 1 * r11]               | 4e 03 04 18             |
    | add r9, qword [rax + 1 * r12]               | 4e 03 0c 20             |
    | add r10, qword [rax + 1 * r13]              | 4e 03 14 28             |
    | add r11, qword [rax + 1 * r14]              | 4e 03 1c 30             |
    | add r12, qword [rax + 1 * r15]              | 4e 03 24 38             |
    | add r13, qword [rax + 2 * rcx]              | 4c 03 2c 48             |
    | add r14, qword [rax + 4 * rcx]              | 4c 03 34 88             |
    | add r15, qword [rax + 8 * rcx]              | 4c 03 3c c8             |
    | add rcx, qword [r8 + 2 * r9]                | 4b 03 0c 48             |
    | add rdx, qword [r8 + 4 * r9]                | 4b 03 14 88             |
    | add rbx, qword [r8 + 8 * r9]                | 4b 03 1c c8             |
    | add rsp, qword [1 * rcx]                    | 48 03 24 0d 00 00 00 00 |
    | add rbp, qword [2 * rcx]                    | 48 03 2c 4d 00 00 00 00 |
    | add rsi, qword [4 * rcx]                    | 48 03 34 8d 00 00 00 00 |
    | add rdi, qword [8 * rcx]                    | 48 03 3c cd 00 00 00 00 |
    | add r8, qword [1 * r9]                      | 4e 03 04 0d 00 00 00 00 |
    | add r9, qword [2 * r9]                      | 4e 03 0c 4d 00 00 00 00 |
    | add r10, qword [4 * r9]                     | 4e 03 14 8d 00 00 00 00 |
    | add r11, qword [8 * r9]                     | 4e 03 1c cd 00 00 00 00 |
    | add r12, qword [r13 + 8 * r12]              | 4f 03 64 e5 00          |
    | add r13, qword [rsp + 4 * r15]              | 4e 03 2c bc             |
    | add r14, qword [rax + 1 * rcx + 0x00]       | 4c 03 74 08 00          |
    | add r15, qword [rax + 1 * rcx - 0x00]       | 4c 03 7c 08 00          |
    | add rcx, qword [rax + 1 * rcx - 0x01]       | 48 03 4c 08 ff          |
    | add rdx, qword [rax + 1 * rcx + 0x00000001] | 48 03 94 08 01 00 00 00 |
    | add rbx, qword [rax + 1 * rcx - 0x00000001] | 48 03 9c 08 ff ff ff ff |
    | add rsp, qword [rax + 1 * rcx + 0x7f]       | 48 03 64 08 7f          |
    | add rbp, qword [rax + 1 * rcx - 0x7f]       | 48 03 6c 08 81          |
    | add rsi, qword [rax + 1 * rcx + 0x80]       | 48 03 b4 08 80 00 00 00 |
    | add rdi, qword [rax + 1 * rcx - 0x80]       | 48 03 7c 08 80          |
    | add r8, qword [rax + 1 * rcx - 0x81]        | 4c 03 84 08 7f ff ff ff |
    | add r9, qword [rax + 1 * rcx + 0xff]        | 4c 03 8c 08 ff 00 00 00 |
    | add r10, qword [rax + 1 * rcx - 0xff]       | 4c 03 94 08 01 ff ff ff |
    | add r11, qword [rax + 1 * rcx + 0x7fffffff] | 4c 03 9c 08 ff ff ff 7f |
    | add r12, qword [rax + 1 * rcx - 0x7fffffff] | 4c 03 a4 08 01 00 00 80 |
    | add r13, qword [rax + 1 * rcx - 0x80000000] | 4c 03 ac 08 00 00 00 80 |
    | add r14, qword [r10 + 0x7f]                 | 4d 03 72 7f             |
    | add r15, qword [r10 + 0x80]                 | 4d 03 ba 80 00 00 00    |
    | add rcx, qword [r10 - 0x81]                 | 49 03 8a 7f ff ff ff    |
    | add rdx, qword [rax]                        | 48 03 10                |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_add_reg64_addr64():
    encode(ADD_REG64_ADDR64)


ADD_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | add eax, 0x01  | 83 c0 01    | *** | add eax, 0x00  | 83 c0 00    |
    | add ecx, 0x01  | 83 c1 01    | *** | add eax, 0x7f  | 83 c0 7f    |
    | add edx, 0x01  | 83 c2 01    | *** | add eax, 0x80  | 83 c0 80    |
    | add ebx, 0x01  | 83 c3 01    | *** | add eax, 0xff  | 83 c0 ff    |
    | add esp, 0x01  | 83 c4 01    | *** | add ecx, 0x7f  | 83 c1 7f    |
    | add ebp, 0x01  | 83 c5 01    | *** | add edx, 0x80  | 83 c2 80    |
    | add esi, 0x01  | 83 c6 01    | *** | add ebx, 0xff  | 83 c3 ff    |
    | add edi, 0x01  | 83 c7 01    | *** | add esp, 0x00  | 83 c4 00    |
    | add r8d, 0x01  | 41 83 c0 01 | *** | add esi, 0x7f  | 83 c6 7f    |
    | add r9d, 0x01  | 41 83 c1 01 | *** | add edi, 0x80  | 83 c7 80    |
    | add r10d, 0x01 | 41 83 c2 01 | *** | add r8d, 0xff  | 41 83 c0 ff |
    | add r11d, 0x01 | 41 83 c3 01 | *** | add r9d, 0x00  | 41 83 c1 00 |
    | add r12d, 0x01 | 41 83 c4 01 | *** | add r11d, 0x7f | 41 83 c3 7f |
    | add r13d, 0x01 | 41 83 c5 01 | *** | add r12d, 0x80 | 41 83 c4 80 |
    | add r14d, 0x01 | 41 83 c6 01 | *** | add r13d, 0xff | 41 83 c5 ff |
    | add r15d, 0x01 | 41 83 c7 01 | *** | add r14d, 0x00 | 41 83 c6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_add_reg32_imm8():
    encode(ADD_REG32_IMM8)


ADD_REG32_IMM32 = """
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | instruction          | encoding             | *** | instruction          | encoding             |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | add eax, 0x00000001  | 05 01 00 00 00       | *** | add eax, 0x00007fff  | 05 ff 7f 00 00       |
    | add ecx, 0x00000001  | 81 c1 01 00 00 00    | *** | add eax, 0x00008000  | 05 00 80 00 00       |
    | add edx, 0x00000001  | 81 c2 01 00 00 00    | *** | add eax, 0x0000ffff  | 05 ff ff 00 00       |
    | add ebx, 0x00000001  | 81 c3 01 00 00 00    | *** | add eax, 0x00010000  | 05 00 00 01 00       |
    | add esp, 0x00000001  | 81 c4 01 00 00 00    | *** | add eax, 0x7fffffff  | 05 ff ff ff 7f       |
    | add ebp, 0x00000001  | 81 c5 01 00 00 00    | *** | add eax, 0x80000000  | 05 00 00 00 80       |
    | add esi, 0x00000001  | 81 c6 01 00 00 00    | *** | add eax, 0xffffffff  | 05 ff ff ff ff       |
    | add edi, 0x00000001  | 81 c7 01 00 00 00    | *** | add ecx, 0x0000007f  | 81 c1 7f 00 00 00    |
    | add r8d, 0x00000001  | 41 81 c0 01 00 00 00 | *** | add edx, 0x00000080  | 81 c2 80 00 00 00    |
    | add r9d, 0x00000001  | 41 81 c1 01 00 00 00 | *** | add ebx, 0x000000ff  | 81 c3 ff 00 00 00    |
    | add r10d, 0x00000001 | 41 81 c2 01 00 00 00 | *** | add esp, 0x00000100  | 81 c4 00 01 00 00    |
    | add r11d, 0x00000001 | 41 81 c3 01 00 00 00 | *** | add ebp, 0x00007fff  | 81 c5 ff 7f 00 00    |
    | add r12d, 0x00000001 | 41 81 c4 01 00 00 00 | *** | add esi, 0x00008000  | 81 c6 00 80 00 00    |
    | add r13d, 0x00000001 | 41 81 c5 01 00 00 00 | *** | add edi, 0x0000ffff  | 81 c7 ff ff 00 00    |
    | add r14d, 0x00000001 | 41 81 c6 01 00 00 00 | *** | add r8d, 0x00010000  | 41 81 c0 00 00 01 00 |
    | add r15d, 0x00000001 | 41 81 c7 01 00 00 00 | *** | add r9d, 0x7fffffff  | 41 81 c1 ff ff ff 7f |
    | add eax, 0x00000000  | 05 00 00 00 00       | *** | add r10d, 0x80000000 | 41 81 c2 00 00 00 80 |
    | add eax, 0x0000007f  | 05 7f 00 00 00       | *** | add r11d, 0xffffffff | 41 81 c3 ff ff ff ff |
    | add eax, 0x00000080  | 05 80 00 00 00       | *** | add r12d, 0x00000000 | 41 81 c4 00 00 00 00 |
    | add eax, 0x000000ff  | 05 ff 00 00 00       | *** | add r14d, 0x0000007f | 41 81 c6 7f 00 00 00 |
    | add eax, 0x00000100  | 05 00 01 00 00       | *** | add r15d, 0x00000080 | 41 81 c7 80 00 00 00 |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
"""


def can_encode_add_reg32_imm32():
    encode(ADD_REG32_IMM32)


ADD_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | add eax, ecx   | 01 c8    | *** | add eax, r8d   | 44 01 c0 |
    | add ecx, ecx   | 01 c9    | *** | add eax, r9d   | 44 01 c8 |
    | add edx, ecx   | 01 ca    | *** | add eax, r10d  | 44 01 d0 |
    | add ebx, ecx   | 01 cb    | *** | add eax, r11d  | 44 01 d8 |
    | add esp, ecx   | 01 cc    | *** | add eax, r12d  | 44 01 e0 |
    | add ebp, ecx   | 01 cd    | *** | add eax, r13d  | 44 01 e8 |
    | add esi, ecx   | 01 ce    | *** | add eax, r14d  | 44 01 f0 |
    | add edi, ecx   | 01 cf    | *** | add eax, r15d  | 44 01 f8 |
    | add r8d, ecx   | 41 01 c8 | *** | add ecx, edx   | 01 d1    |
    | add r9d, ecx   | 41 01 c9 | *** | add edx, ebx   | 01 da    |
    | add r10d, ecx  | 41 01 ca | *** | add ebx, esp   | 01 e3    |
    | add r11d, ecx  | 41 01 cb | *** | add esp, ebp   | 01 ec    |
    | add r12d, ecx  | 41 01 cc | *** | add ebp, esi   | 01 f5    |
    | add r13d, ecx  | 41 01 cd | *** | add esi, edi   | 01 fe    |
    | add r14d, ecx  | 41 01 ce | *** | add edi, r8d   | 44 01 c7 |
    | add r15d, ecx  | 41 01 cf | *** | add r8d, r9d   | 45 01 c8 |
    | add eax, eax   | 01 c0    | *** | add r9d, r10d  | 45 01 d1 |
    | add eax, edx   | 01 d0    | *** | add r10d, r11d | 45 01 da |
    | add eax, ebx   | 01 d8    | *** | add r11d, r12d | 45 01 e3 |
    | add eax, esp   | 01 e0    | *** | add r12d, r13d | 45 01 ec |
    | add eax, ebp   | 01 e8    | *** | add r13d, r14d | 45 01 f5 |
    | add eax, esi   | 01 f0    | *** | add r14d, r15d | 45 01 fe |
    | add eax, edi   | 01 f8    | *** | add r15d, eax  | 41 01 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_add_reg32_reg32():
    encode(ADD_REG32_REG32)


ADD_REG32_ADDR32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | add eax, dword [rcx]                         | 03 01                   |
    | add ecx, dword [rcx]                         | 03 09                   |
    | add edx, dword [rcx]                         | 03 11                   |
    | add ebx, dword [rcx]                         | 03 19                   |
    | add esp, dword [rcx]                         | 03 21                   |
    | add ebp, dword [rcx]                         | 03 29                   |
    | add esi, dword [rcx]                         | 03 31                   |
    | add edi, dword [rcx]                         | 03 39                   |
    | add r8d, dword [rcx]                         | 44 03 01                |
    | add r9d, dword [rcx]                         | 44 03 09                |
    | add r10d, dword [rcx]                        | 44 03 11                |
    | add r11d, dword [rcx]                        | 44 03 19                |
    | add r12d, dword [rcx]                        | 44 03 21                |
    | add r13d, dword [rcx]                        | 44 03 29                |
    | add r14d, dword [rcx]                        | 44 03 31                |
    | add r15d, dword [rcx]                        | 44 03 39                |
    | add eax, dword [rax]                         | 03 00                   |
    | add eax, dword [rdx]                         | 03 02                   |
    | add eax, dword [rbx]                         | 03 03                   |
    | add eax, dword [rsp]                         | 03 04 24                |
    | add eax, dword [rbp]                         | 03 45 00                |
    | add eax, dword [rsi]                         | 03 06                   |
    | add eax, dword [rdi]                         | 03 07                   |
    | add eax, dword [r8]                          | 41 03 00                |
    | add eax, dword [r9]                          | 41 03 01                |
    | add eax, dword [r10]                         | 41 03 02                |
    | add eax, dword [r11]                         | 41 03 03                |
    | add eax, dword [r12]                         | 41 03 04 24             |
    | add eax, dword [r13]                         | 41 03 45 00             |
    | add eax, dword [r14]                         | 41 03 06                |
    | add eax, dword [r15]                         | 41 03 07                |
    | add eax, dword [rax + 1 * rcx]               | 03 04 08                |
    | add eax, dword [rcx + 1 * rcx]               | 03 04 09                |
    | add eax, dword [rdx + 1 * rcx]               | 03 04 0a                |
    | add eax, dword [rbx + 1 * rcx]               | 03 04 0b                |
    | add eax, dword [rsp + 1 * rcx]               | 03 04 0c                |
    | add eax, dword [rbp + 1 * rcx]               | 03 44 0d 00             |
    | add eax, dword [rsi + 1 * rcx]               | 03 04 0e                |
    | add eax, dword [rdi + 1 * rcx]               | 03 04 0f                |
    | add eax, dword [r8 + 1 * rcx]                | 41 03 04 08             |
    | add eax, dword [r9 + 1 * rcx]                | 41 03 04 09             |
    | add eax, dword [r10 + 1 * rcx]               | 41 03 04 0a             |
    | add eax, dword [r11 + 1 * rcx]               | 41 03 04 0b             |
    | add eax, dword [r12 + 1 * rcx]               | 41 03 04 0c             |
    | add eax, dword [r13 + 1 * rcx]               | 41 03 44 0d 00          |
    | add eax, dword [r14 + 1 * rcx]               | 41 03 04 0e             |
    | add eax, dword [r15 + 1 * rcx]               | 41 03 04 0f             |
    | add eax, dword [rax + 1 * rax]               | 03 04 00                |
    | add eax, dword [rax + 1 * rdx]               | 03 04 10                |
    | add eax, dword [rax + 1 * rbx]               | 03 04 18                |
    | add eax, dword [rax + 1 * rbp]               | 03 04 28                |
    | add eax, dword [rax + 1 * rsi]               | 03 04 30                |
    | add eax, dword [rax + 1 * rdi]               | 03 04 38                |
    | add eax, dword [rax + 1 * r8]                | 42 03 04 00             |
    | add eax, dword [rax + 1 * r9]                | 42 03 04 08             |
    | add eax, dword [rax + 1 * r10]               | 42 03 04 10             |
    | add eax, dword [rax + 1 * r11]               | 42 03 04 18             |
    | add eax, dword [rax + 1 * r12]               | 42 03 04 20             |
    | add eax, dword [rax + 1 * r13]               | 42 03 04 28             |
    | add eax, dword [rax + 1 * r14]               | 42 03 04 30             |
    | add eax, dword [rax + 1 * r15]               | 42 03 04 38             |
    | add eax, dword [rax + 2 * rcx]               | 03 04 48                |
    | add eax, dword [rax + 4 * rcx]               | 03 04 88                |
    | add eax, dword [rax + 8 * rcx]               | 03 04 c8                |
    | add eax, dword [r8 + 1 * r9]                 | 43 03 04 08             |
    | add eax, dword [r8 + 2 * r9]                 | 43 03 04 48             |
    | add eax, dword [r8 + 4 * r9]                 | 43 03 04 88             |
    | add eax, dword [r8 + 8 * r9]                 | 43 03 04 c8             |
    | add eax, dword [1 * rcx]                     | 03 04 0d 00 00 00 00    |
    | add eax, dword [2 * rcx]                     | 03 04 4d 00 00 00 00    |
    | add eax, dword [4 * rcx]                     | 03 04 8d 00 00 00 00    |
    | add eax, dword [8 * rcx]                     | 03 04 cd 00 00 00 00    |
    | add eax, dword [1 * r9]                      | 42 03 04 0d 00 00 00 00 |
    | add eax, dword [2 * r9]                      | 42 03 04 4d 00 00 00 00 |
    | add eax, dword [4 * r9]                      | 42 03 04 8d 00 00 00 00 |
    | add eax, dword [8 * r9]                      | 42 03 04 cd 00 00 00 00 |
    | add eax, dword [r13 + 8 * r12]               | 43 03 44 e5 00          |
    | add eax, dword [rsp + 4 * r15]               | 42 03 04 bc             |
    | add eax, dword [rax + 1 * rcx + 0x00]        | 03 44 08 00             |
    | add eax, dword [rax + 1 * rcx - 0x00]        | 03 44 08 00             |
    | add eax, dword [rax + 1 * rcx + 0x01]        | 03 44 08 01             |
    | add eax, dword [rax + 1 * rcx - 0x01]        | 03 44 08 ff             |
    | add eax, dword [rax + 1 * rcx + 0x00000001]  | 03 84 08 01 00 00 00    |
    | add eax, dword [rax + 1 * rcx - 0x00000001]  | 03 84 08 ff ff ff ff    |
    | add eax, dword [rax + 1 * rcx + 0x7f]        | 03 44 08 7f             |
    | add eax, dword [rax + 1 * rcx - 0x7f]        | 03 44 08 81             |
    | add eax, dword [rax + 1 * rcx + 0x80]        | 03 84 08 80 00 00 00    |
    | add eax, dword [rax + 1 * rcx - 0x80]        | 03 44 08 80             |
    | add eax, dword [rax + 1 * rcx - 0x81]        | 03 84 08 7f ff ff ff    |
    | add eax, dword [rax + 1 * rcx + 0xff]        | 03 84 08 ff 00 00 00    |
    | add eax, dword [rax + 1 * rcx - 0xff]        | 03 84 08 01 ff ff ff    |
    | add eax, dword [rax + 1 * rcx + 0x7fffffff]  | 03 84 08 ff ff ff 7f    |
    | add eax, dword [rax + 1 * rcx - 0x7fffffff]  | 03 84 08 01 00 00 80    |
    | add eax, dword [rax + 1 * rcx - 0x80000000]  | 03 84 08 00 00 00 80    |
    | add eax, dword [r10 + 0x7f]                  | 41 03 42 7f             |
    | add eax, dword [r10 + 0x80]                  | 41 03 82 80 00 00 00    |
    | add eax, dword [r10 - 0x80]                  | 41 03 42 80             |
    | add eax, dword [r10 - 0x81]                  | 41 03 82 7f ff ff ff    |
    | add ecx, dword [rdx]                         | 03 0a                   |
    | add edx, dword [rbx]                         | 03 13                   |
    | add ebx, dword [rsp]                         | 03 1c 24                |
    | add esp, dword [rbp]                         | 03 65 00                |
    | add ebp, dword [rsi]                         | 03 2e                   |
    | add esi, dword [rdi]                         | 03 37                   |
    | add edi, dword [r8]                          | 41 03 38                |
    | add r8d, dword [r9]                          | 45 03 01                |
    | add r9d, dword [r10]                         | 45 03 0a                |
    | add r10d, dword [r11]                        | 45 03 13                |
    | add r11d, dword [r12]                        | 45 03 1c 24             |
    | add r12d, dword [r13]                        | 45 03 65 00             |
    | add r13d, dword [r14]                        | 45 03 2e                |
    | add r14d, dword [r15]                        | 45 03 37                |
    | add r15d, dword [rax + 1 * rcx]              | 44 03 3c 08             |
    | add ecx, dword [rdx + 1 * rcx]               | 03 0c 0a                |
    | add edx, dword [rbx + 1 * rcx]               | 03 14 0b                |
    | add ebx, dword [rsp + 1 * rcx]               | 03 1c 0c                |
    | add esp, dword [rbp + 1 * rcx]               | 03 64 0d 00             |
    | add ebp, dword [rsi + 1 * rcx]               | 03 2c 0e                |
    | add esi, dword [rdi + 1 * rcx]               | 03 34 0f                |
    | add edi, dword [r8 + 1 * rcx]                | 41 03 3c 08             |
    | add r8d, dword [r9 + 1 * rcx]                | 45 03 04 09             |
    | add r9d, dword [r10 + 1 * rcx]               | 45 03 0c 0a             |
    | add r10d, dword [r11 + 1 * rcx]              | 45 03 14 0b             |
    | add r11d, dword [r12 + 1 * rcx]              | 45 03 1c 0c             |
    | add r12d, dword [r13 + 1 * rcx]              | 45 03 64 0d 00          |
    | add r13d, dword [r14 + 1 * rcx]              | 45 03 2c 0e             |
    | add r14d, dword [r15 + 1 * rcx]              | 45 03 34 0f             |
    | add r15d, dword [rax + 1 * rax]              | 44 03 3c 00             |
    | add ecx, dword [rax + 1 * rbx]               | 03 0c 18                |
    | add edx, dword [rax + 1 * rbp]               | 03 14 28                |
    | add ebx, dword [rax + 1 * rsi]               | 03 1c 30                |
    | add esp, dword [rax + 1 * rdi]               | 03 24 38                |
    | add ebp, dword [rax + 1 * r8]                | 42 03 2c 00             |
    | add esi, dword [rax + 1 * r9]                | 42 03 34 08             |
    | add edi, dword [rax + 1 * r10]               | 42 03 3c 10             |
    | add r8d, dword [rax + 1 * r11]               | 46 03 04 18             |
    | add r9d, dword [rax + 1 * r12]               | 46 03 0c 20             |
    | add r10d, dword [rax + 1 * r13]              | 46 03 14 28             |
    | add r11d, dword [rax + 1 * r14]              | 46 03 1c 30             |
    | add r12d, dword [rax + 1 * r15]              | 46 03 24 38             |
    | add r13d, dword [rax + 2 * rcx]              | 44 03 2c 48             |
    | add r14d, dword [rax + 4 * rcx]              | 44 03 34 88             |
    | add r15d, dword [rax + 8 * rcx]              | 44 03 3c c8             |
    | add ecx, dword [r8 + 2 * r9]                 | 43 03 0c 48             |
    | add edx, dword [r8 + 4 * r9]                 | 43 03 14 88             |
    | add ebx, dword [r8 + 8 * r9]                 | 43 03 1c c8             |
    | add esp, dword [1 * rcx]                     | 03 24 0d 00 00 00 00    |
    | add ebp, dword [2 * rcx]                     | 03 2c 4d 00 00 00 00    |
    | add esi, dword [4 * rcx]                     | 03 34 8d 00 00 00 00    |
    | add edi, dword [8 * rcx]                     | 03 3c cd 00 00 00 00    |
    | add r8d, dword [1 * r9]                      | 46 03 04 0d 00 00 00 00 |
    | add r9d, dword [2 * r9]                      | 46 03 0c 4d 00 00 00 00 |
    | add r10d, dword [4 * r9]                     | 46 03 14 8d 00 00 00 00 |
    | add r11d, dword [8 * r9]                     | 46 03 1c cd 00 00 00 00 |
    | add r12d, dword [r13 + 8 * r12]              | 47 03 64 e5 00          |
    | add r13d, dword [rsp + 4 * r15]              | 46 03 2c bc             |
    | add r14d, dword [rax + 1 * rcx + 0x00]       | 44 03 74 08 00          |
    | add r15d, dword [rax + 1 * rcx - 0x00]       | 44 03 7c 08 00          |
    | add ecx, dword [rax + 1 * rcx - 0x01]        | 03 4c 08 ff             |
    | add edx, dword [rax + 1 * rcx + 0x00000001]  | 03 94 08 01 00 00 00    |
    | add ebx, dword [rax + 1 * rcx - 0x00000001]  | 03 9c 08 ff ff ff ff    |
    | add esp, dword [rax + 1 * rcx + 0x7f]        | 03 64 08 7f             |
    | add ebp, dword [rax + 1 * rcx - 0x7f]        | 03 6c 08 81             |
    | add esi, dword [rax + 1 * rcx + 0x80]        | 03 b4 08 80 00 00 00    |
    | add edi, dword [rax + 1 * rcx - 0x80]        | 03 7c 08 80             |
    | add r8d, dword [rax + 1 * rcx - 0x81]        | 44 03 84 08 7f ff ff ff |
    | add r9d, dword [rax + 1 * rcx + 0xff]        | 44 03 8c 08 ff 00 00 00 |
    | add r10d, dword [rax + 1 * rcx - 0xff]       | 44 03 94 08 01 ff ff ff |
    | add r11d, dword [rax + 1 * rcx + 0x7fffffff] | 44 03 9c 08 ff ff ff 7f |
    | add r12d, dword [rax + 1 * rcx - 0x7fffffff] | 44 03 a4 08 01 00 00 80 |
    | add r13d, dword [rax + 1 * rcx - 0x80000000] | 44 03 ac 08 00 00 00 80 |
    | add r14d, dword [r10 + 0x7f]                 | 45 03 72 7f             |
    | add r15d, dword [r10 + 0x80]                 | 45 03 ba 80 00 00 00    |
    | add ecx, dword [r10 - 0x81]                  | 41 03 8a 7f ff ff ff    |
    | add edx, dword [rax]                         | 03 10                   |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_add_reg32_addr32():
    encode(ADD_REG32_ADDR32)


ADD_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | add ax, 0x01   | 66 83 c0 01    | *** | add ax, 0x00   | 66 83 c0 00    |
    | add cx, 0x01   | 66 83 c1 01    | *** | add ax, 0x7f   | 66 83 c0 7f    |
    | add dx, 0x01   | 66 83 c2 01    | *** | add ax, 0x80   | 66 83 c0 80    |
    | add bx, 0x01   | 66 83 c3 01    | *** | add ax, 0xff   | 66 83 c0 ff    |
    | add sp, 0x01   | 66 83 c4 01    | *** | add cx, 0x7f   | 66 83 c1 7f    |
    | add bp, 0x01   | 66 83 c5 01    | *** | add dx, 0x80   | 66 83 c2 80    |
    | add si, 0x01   | 66 83 c6 01    | *** | add bx, 0xff   | 66 83 c3 ff    |
    | add di, 0x01   | 66 83 c7 01    | *** | add sp, 0x00   | 66 83 c4 00    |
    | add r8w, 0x01  | 66 41 83 c0 01 | *** | add si, 0x7f   | 66 83 c6 7f    |
    | add r9w, 0x01  | 66 41 83 c1 01 | *** | add di, 0x80   | 66 83 c7 80    |
    | add r10w, 0x01 | 66 41 83 c2 01 | *** | add r8w, 0xff  | 66 41 83 c0 ff |
    | add r11w, 0x01 | 66 41 83 c3 01 | *** | add r9w, 0x00  | 66 41 83 c1 00 |
    | add r12w, 0x01 | 66 41 83 c4 01 | *** | add r11w, 0x7f | 66 41 83 c3 7f |
    | add r13w, 0x01 | 66 41 83 c5 01 | *** | add r12w, 0x80 | 66 41 83 c4 80 |
    | add r14w, 0x01 | 66 41 83 c6 01 | *** | add r13w, 0xff | 66 41 83 c5 ff |
    | add r15w, 0x01 | 66 41 83 c7 01 | *** | add r14w, 0x00 | 66 41 83 c6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_add_reg16_imm8():
    encode(ADD_REG16_IMM8)


ADD_REG16_IMM16 = """
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | instruction      | encoding          | *** | instruction      | encoding          |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | add ax, 0x0001   | 66 05 01 00       | *** | add ax, 0x00ff   | 66 05 ff 00       |
    | add cx, 0x0001   | 66 81 c1 01 00    | *** | add ax, 0x0100   | 66 05 00 01       |
    | add dx, 0x0001   | 66 81 c2 01 00    | *** | add ax, 0x7fff   | 66 05 ff 7f       |
    | add bx, 0x0001   | 66 81 c3 01 00    | *** | add ax, 0x8000   | 66 05 00 80       |
    | add sp, 0x0001   | 66 81 c4 01 00    | *** | add ax, 0xffff   | 66 05 ff ff       |
    | add bp, 0x0001   | 66 81 c5 01 00    | *** | add cx, 0x007f   | 66 81 c1 7f 00    |
    | add si, 0x0001   | 66 81 c6 01 00    | *** | add dx, 0x0080   | 66 81 c2 80 00    |
    | add di, 0x0001   | 66 81 c7 01 00    | *** | add bx, 0x00ff   | 66 81 c3 ff 00    |
    | add r8w, 0x0001  | 66 41 81 c0 01 00 | *** | add sp, 0x0100   | 66 81 c4 00 01    |
    | add r9w, 0x0001  | 66 41 81 c1 01 00 | *** | add bp, 0x7fff   | 66 81 c5 ff 7f    |
    | add r10w, 0x0001 | 66 41 81 c2 01 00 | *** | add si, 0x8000   | 66 81 c6 00 80    |
    | add r11w, 0x0001 | 66 41 81 c3 01 00 | *** | add di, 0xffff   | 66 81 c7 ff ff    |
    | add r12w, 0x0001 | 66 41 81 c4 01 00 | *** | add r8w, 0x0000  | 66 41 81 c0 00 00 |
    | add r13w, 0x0001 | 66 41 81 c5 01 00 | *** | add r10w, 0x007f | 66 41 81 c2 7f 00 |
    | add r14w, 0x0001 | 66 41 81 c6 01 00 | *** | add r11w, 0x0080 | 66 41 81 c3 80 00 |
    | add r15w, 0x0001 | 66 41 81 c7 01 00 | *** | add r12w, 0x00ff | 66 41 81 c4 ff 00 |
    | add ax, 0x0000   | 66 05 00 00       | *** | add r13w, 0x0100 | 66 41 81 c5 00 01 |
    | add ax, 0x007f   | 66 05 7f 00       | *** | add r14w, 0x7fff | 66 41 81 c6 ff 7f |
    | add ax, 0x0080   | 66 05 80 00       | *** | add r15w, 0x8000 | 66 41 81 c7 00 80 |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
"""


def can_encode_add_reg16_imm16():
    encode(ADD_REG16_IMM16)


ADD_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | add ax, cx     | 66 01 c8    | *** | add ax, r8w    | 66 44 01 c0 |
    | add cx, cx     | 66 01 c9    | *** | add ax, r9w    | 66 44 01 c8 |
    | add dx, cx     | 66 01 ca    | *** | add ax, r10w   | 66 44 01 d0 |
    | add bx, cx     | 66 01 cb    | *** | add ax, r11w   | 66 44 01 d8 |
    | add sp, cx     | 66 01 cc    | *** | add ax, r12w   | 66 44 01 e0 |
    | add bp, cx     | 66 01 cd    | *** | add ax, r13w   | 66 44 01 e8 |
    | add si, cx     | 66 01 ce    | *** | add ax, r14w   | 66 44 01 f0 |
    | add di, cx     | 66 01 cf    | *** | add ax, r15w   | 66 44 01 f8 |
    | add r8w, cx    | 66 41 01 c8 | *** | add cx, dx     | 66 01 d1    |
    | add r9w, cx    | 66 41 01 c9 | *** | add dx, bx     | 66 01 da    |
    | add r10w, cx   | 66 41 01 ca | *** | add bx, sp     | 66 01 e3    |
    | add r11w, cx   | 66 41 01 cb | *** | add sp, bp     | 66 01 ec    |
    | add r12w, cx   | 66 41 01 cc | *** | add bp, si     | 66 01 f5    |
    | add r13w, cx   | 66 41 01 cd | *** | add si, di     | 66 01 fe    |
    | add r14w, cx   | 66 41 01 ce | *** | add di, r8w    | 66 44 01 c7 |
    | add r15w, cx   | 66 41 01 cf | *** | add r8w, r9w   | 66 45 01 c8 |
    | add ax, ax     | 66 01 c0    | *** | add r9w, r10w  | 66 45 01 d1 |
    | add ax, dx     | 66 01 d0    | *** | add r10w, r11w | 66 45 01 da |
    | add ax, bx     | 66 01 d8    | *** | add r11w, r12w | 66 45 01 e3 |
    | add ax, sp     | 66 01 e0    | *** | add r12w, r13w | 66 45 01 ec |
    | add ax, bp     | 66 01 e8    | *** | add r13w, r14w | 66 45 01 f5 |
    | add ax, si     | 66 01 f0    | *** | add r14w, r15w | 66 45 01 fe |
    | add ax, di     | 66 01 f8    | *** | add r15w, ax   | 66 41 01 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_add_reg16_reg16():
    encode(ADD_REG16_REG16)


ADD_REG16_ADDR16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | add ax, word [rcx]                          | 66 03 01                   |
    | add cx, word [rcx]                          | 66 03 09                   |
    | add dx, word [rcx]                          | 66 03 11                   |
    | add bx, word [rcx]                          | 66 03 19                   |
    | add sp, word [rcx]                          | 66 03 21                   |
    | add bp, word [rcx]                          | 66 03 29                   |
    | add si, word [rcx]                          | 66 03 31                   |
    | add di, word [rcx]                          | 66 03 39                   |
    | add r8w, word [rcx]                         | 66 44 03 01                |
    | add r9w, word [rcx]                         | 66 44 03 09                |
    | add r10w, word [rcx]                        | 66 44 03 11                |
    | add r11w, word [rcx]                        | 66 44 03 19                |
    | add r12w, word [rcx]                        | 66 44 03 21                |
    | add r13w, word [rcx]                        | 66 44 03 29                |
    | add r14w, word [rcx]                        | 66 44 03 31                |
    | add r15w, word [rcx]                        | 66 44 03 39                |
    | add ax, word [rax]                          | 66 03 00                   |
    | add ax, word [rdx]                          | 66 03 02                   |
    | add ax, word [rbx]                          | 66 03 03                   |
    | add ax, word [rsp]                          | 66 03 04 24                |
    | add ax, word [rbp]                          | 66 03 45 00                |
    | add ax, word [rsi]                          | 66 03 06                   |
    | add ax, word [rdi]                          | 66 03 07                   |
    | add ax, word [r8]                           | 66 41 03 00                |
    | add ax, word [r9]                           | 66 41 03 01                |
    | add ax, word [r10]                          | 66 41 03 02                |
    | add ax, word [r11]                          | 66 41 03 03                |
    | add ax, word [r12]                          | 66 41 03 04 24             |
    | add ax, word [r13]                          | 66 41 03 45 00             |
    | add ax, word [r14]                          | 66 41 03 06                |
    | add ax, word [r15]                          | 66 41 03 07                |
    | add ax, word [rax + 1 * rcx]                | 66 03 04 08                |
    | add ax, word [rcx + 1 * rcx]                | 66 03 04 09                |
    | add ax, word [rdx + 1 * rcx]                | 66 03 04 0a                |
    | add ax, word [rbx + 1 * rcx]                | 66 03 04 0b                |
    | add ax, word [rsp + 1 * rcx]                | 66 03 04 0c                |
    | add ax, word [rbp + 1 * rcx]                | 66 03 44 0d 00             |
    | add ax, word [rsi + 1 * rcx]                | 66 03 04 0e                |
    | add ax, word [rdi + 1 * rcx]                | 66 03 04 0f                |
    | add ax, word [r8 + 1 * rcx]                 | 66 41 03 04 08             |
    | add ax, word [r9 + 1 * rcx]                 | 66 41 03 04 09             |
    | add ax, word [r10 + 1 * rcx]                | 66 41 03 04 0a             |
    | add ax, word [r11 + 1 * rcx]                | 66 41 03 04 0b             |
    | add ax, word [r12 + 1 * rcx]                | 66 41 03 04 0c             |
    | add ax, word [r13 + 1 * rcx]                | 66 41 03 44 0d 00          |
    | add ax, word [r14 + 1 * rcx]                | 66 41 03 04 0e             |
    | add ax, word [r15 + 1 * rcx]                | 66 41 03 04 0f             |
    | add ax, word [rax + 1 * rax]                | 66 03 04 00                |
    | add ax, word [rax + 1 * rdx]                | 66 03 04 10                |
    | add ax, word [rax + 1 * rbx]                | 66 03 04 18                |
    | add ax, word [rax + 1 * rbp]                | 66 03 04 28                |
    | add ax, word [rax + 1 * rsi]                | 66 03 04 30                |
    | add ax, word [rax + 1 * rdi]                | 66 03 04 38                |
    | add ax, word [rax + 1 * r8]                 | 66 42 03 04 00             |
    | add ax, word [rax + 1 * r9]                 | 66 42 03 04 08             |
    | add ax, word [rax + 1 * r10]                | 66 42 03 04 10             |
    | add ax, word [rax + 1 * r11]                | 66 42 03 04 18             |
    | add ax, word [rax + 1 * r12]                | 66 42 03 04 20             |
    | add ax, word [rax + 1 * r13]                | 66 42 03 04 28             |
    | add ax, word [rax + 1 * r14]                | 66 42 03 04 30             |
    | add ax, word [rax + 1 * r15]                | 66 42 03 04 38             |
    | add ax, word [rax + 2 * rcx]                | 66 03 04 48                |
    | add ax, word [rax + 4 * rcx]                | 66 03 04 88                |
    | add ax, word [rax + 8 * rcx]                | 66 03 04 c8                |
    | add ax, word [r8 + 1 * r9]                  | 66 43 03 04 08             |
    | add ax, word [r8 + 2 * r9]                  | 66 43 03 04 48             |
    | add ax, word [r8 + 4 * r9]                  | 66 43 03 04 88             |
    | add ax, word [r8 + 8 * r9]                  | 66 43 03 04 c8             |
    | add ax, word [1 * rcx]                      | 66 03 04 0d 00 00 00 00    |
    | add ax, word [2 * rcx]                      | 66 03 04 4d 00 00 00 00    |
    | add ax, word [4 * rcx]                      | 66 03 04 8d 00 00 00 00    |
    | add ax, word [8 * rcx]                      | 66 03 04 cd 00 00 00 00    |
    | add ax, word [1 * r9]                       | 66 42 03 04 0d 00 00 00 00 |
    | add ax, word [2 * r9]                       | 66 42 03 04 4d 00 00 00 00 |
    | add ax, word [4 * r9]                       | 66 42 03 04 8d 00 00 00 00 |
    | add ax, word [8 * r9]                       | 66 42 03 04 cd 00 00 00 00 |
    | add ax, word [r13 + 8 * r12]                | 66 43 03 44 e5 00          |
    | add ax, word [rsp + 4 * r15]                | 66 42 03 04 bc             |
    | add ax, word [rax + 1 * rcx + 0x00]         | 66 03 44 08 00             |
    | add ax, word [rax + 1 * rcx - 0x00]         | 66 03 44 08 00             |
    | add ax, word [rax + 1 * rcx + 0x01]         | 66 03 44 08 01             |
    | add ax, word [rax + 1 * rcx - 0x01]         | 66 03 44 08 ff             |
    | add ax, word [rax + 1 * rcx + 0x00000001]   | 66 03 84 08 01 00 00 00    |
    | add ax, word [rax + 1 * rcx - 0x00000001]   | 66 03 84 08 ff ff ff ff    |
    | add ax, word [rax + 1 * rcx + 0x7f]         | 66 03 44 08 7f             |
    | add ax, word [rax + 1 * rcx - 0x7f]         | 66 03 44 08 81             |
    | add ax, word [rax + 1 * rcx + 0x80]         | 66 03 84 08 80 00 00 00    |
    | add ax, word [rax + 1 * rcx - 0x80]         | 66 03 44 08 80             |
    | add ax, word [rax + 1 * rcx - 0x81]         | 66 03 84 08 7f ff ff ff    |
    | add ax, word [rax + 1 * rcx + 0xff]         | 66 03 84 08 ff 00 00 00    |
    | add ax, word [rax + 1 * rcx - 0xff]         | 66 03 84 08 01 ff ff ff    |
    | add ax, word [rax + 1 * rcx + 0x7fffffff]   | 66 03 84 08 ff ff ff 7f    |
    | add ax, word [rax + 1 * rcx - 0x7fffffff]   | 66 03 84 08 01 00 00 80    |
    | add ax, word [rax + 1 * rcx - 0x80000000]   | 66 03 84 08 00 00 00 80    |
    | add ax, word [r10 + 0x7f]                   | 66 41 03 42 7f             |
    | add ax, word [r10 + 0x80]                   | 66 41 03 82 80 00 00 00    |
    | add ax, word [r10 - 0x80]                   | 66 41 03 42 80             |
    | add ax, word [r10 - 0x81]                   | 66 41 03 82 7f ff ff ff    |
    | add cx, word [rdx]                          | 66 03 0a                   |
    | add dx, word [rbx]                          | 66 03 13                   |
    | add bx, word [rsp]                          | 66 03 1c 24                |
    | add sp, word [rbp]                          | 66 03 65 00                |
    | add bp, word [rsi]                          | 66 03 2e                   |
    | add si, word [rdi]                          | 66 03 37                   |
    | add di, word [r8]                           | 66 41 03 38                |
    | add r8w, word [r9]                          | 66 45 03 01                |
    | add r9w, word [r10]                         | 66 45 03 0a                |
    | add r10w, word [r11]                        | 66 45 03 13                |
    | add r11w, word [r12]                        | 66 45 03 1c 24             |
    | add r12w, word [r13]                        | 66 45 03 65 00             |
    | add r13w, word [r14]                        | 66 45 03 2e                |
    | add r14w, word [r15]                        | 66 45 03 37                |
    | add r15w, word [rax + 1 * rcx]              | 66 44 03 3c 08             |
    | add cx, word [rdx + 1 * rcx]                | 66 03 0c 0a                |
    | add dx, word [rbx + 1 * rcx]                | 66 03 14 0b                |
    | add bx, word [rsp + 1 * rcx]                | 66 03 1c 0c                |
    | add sp, word [rbp + 1 * rcx]                | 66 03 64 0d 00             |
    | add bp, word [rsi + 1 * rcx]                | 66 03 2c 0e                |
    | add si, word [rdi + 1 * rcx]                | 66 03 34 0f                |
    | add di, word [r8 + 1 * rcx]                 | 66 41 03 3c 08             |
    | add r8w, word [r9 + 1 * rcx]                | 66 45 03 04 09             |
    | add r9w, word [r10 + 1 * rcx]               | 66 45 03 0c 0a             |
    | add r10w, word [r11 + 1 * rcx]              | 66 45 03 14 0b             |
    | add r11w, word [r12 + 1 * rcx]              | 66 45 03 1c 0c             |
    | add r12w, word [r13 + 1 * rcx]              | 66 45 03 64 0d 00          |
    | add r13w, word [r14 + 1 * rcx]              | 66 45 03 2c 0e             |
    | add r14w, word [r15 + 1 * rcx]              | 66 45 03 34 0f             |
    | add r15w, word [rax + 1 * rax]              | 66 44 03 3c 00             |
    | add cx, word [rax + 1 * rbx]                | 66 03 0c 18                |
    | add dx, word [rax + 1 * rbp]                | 66 03 14 28                |
    | add bx, word [rax + 1 * rsi]                | 66 03 1c 30                |
    | add sp, word [rax + 1 * rdi]                | 66 03 24 38                |
    | add bp, word [rax + 1 * r8]                 | 66 42 03 2c 00             |
    | add si, word [rax + 1 * r9]                 | 66 42 03 34 08             |
    | add di, word [rax + 1 * r10]                | 66 42 03 3c 10             |
    | add r8w, word [rax + 1 * r11]               | 66 46 03 04 18             |
    | add r9w, word [rax + 1 * r12]               | 66 46 03 0c 20             |
    | add r10w, word [rax + 1 * r13]              | 66 46 03 14 28             |
    | add r11w, word [rax + 1 * r14]              | 66 46 03 1c 30             |
    | add r12w, word [rax + 1 * r15]              | 66 46 03 24 38             |
    | add r13w, word [rax + 2 * rcx]              | 66 44 03 2c 48             |
    | add r14w, word [rax + 4 * rcx]              | 66 44 03 34 88             |
    | add r15w, word [rax + 8 * rcx]              | 66 44 03 3c c8             |
    | add cx, word [r8 + 2 * r9]                  | 66 43 03 0c 48             |
    | add dx, word [r8 + 4 * r9]                  | 66 43 03 14 88             |
    | add bx, word [r8 + 8 * r9]                  | 66 43 03 1c c8             |
    | add sp, word [1 * rcx]                      | 66 03 24 0d 00 00 00 00    |
    | add bp, word [2 * rcx]                      | 66 03 2c 4d 00 00 00 00    |
    | add si, word [4 * rcx]                      | 66 03 34 8d 00 00 00 00    |
    | add di, word [8 * rcx]                      | 66 03 3c cd 00 00 00 00    |
    | add r8w, word [1 * r9]                      | 66 46 03 04 0d 00 00 00 00 |
    | add r9w, word [2 * r9]                      | 66 46 03 0c 4d 00 00 00 00 |
    | add r10w, word [4 * r9]                     | 66 46 03 14 8d 00 00 00 00 |
    | add r11w, word [8 * r9]                     | 66 46 03 1c cd 00 00 00 00 |
    | add r12w, word [r13 + 8 * r12]              | 66 47 03 64 e5 00          |
    | add r13w, word [rsp + 4 * r15]              | 66 46 03 2c bc             |
    | add r14w, word [rax + 1 * rcx + 0x00]       | 66 44 03 74 08 00          |
    | add r15w, word [rax + 1 * rcx - 0x00]       | 66 44 03 7c 08 00          |
    | add cx, word [rax + 1 * rcx - 0x01]         | 66 03 4c 08 ff             |
    | add dx, word [rax + 1 * rcx + 0x00000001]   | 66 03 94 08 01 00 00 00    |
    | add bx, word [rax + 1 * rcx - 0x00000001]   | 66 03 9c 08 ff ff ff ff    |
    | add sp, word [rax + 1 * rcx + 0x7f]         | 66 03 64 08 7f             |
    | add bp, word [rax + 1 * rcx - 0x7f]         | 66 03 6c 08 81             |
    | add si, word [rax + 1 * rcx + 0x80]         | 66 03 b4 08 80 00 00 00    |
    | add di, word [rax + 1 * rcx - 0x80]         | 66 03 7c 08 80             |
    | add r8w, word [rax + 1 * rcx - 0x81]        | 66 44 03 84 08 7f ff ff ff |
    | add r9w, word [rax + 1 * rcx + 0xff]        | 66 44 03 8c 08 ff 00 00 00 |
    | add r10w, word [rax + 1 * rcx - 0xff]       | 66 44 03 94 08 01 ff ff ff |
    | add r11w, word [rax + 1 * rcx + 0x7fffffff] | 66 44 03 9c 08 ff ff ff 7f |
    | add r12w, word [rax + 1 * rcx - 0x7fffffff] | 66 44 03 a4 08 01 00 00 80 |
    | add r13w, word [rax + 1 * rcx - 0x80000000] | 66 44 03 ac 08 00 00 00 80 |
    | add r14w, word [r10 + 0x7f]                 | 66 45 03 72 7f             |
    | add r15w, word [r10 + 0x80]                 | 66 45 03 ba 80 00 00 00    |
    | add cx, word [r10 - 0x81]                   | 66 41 03 8a 7f ff ff ff    |
    | add dx, word [rax]                          | 66 03 10                   |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_add_reg16_addr16():
    encode(ADD_REG16_ADDR16)


ADD_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | add al, 0x01   | 04 01       | *** | add al, 0x00   | 04 00       |
    | add cl, 0x01   | 80 c1 01    | *** | add al, 0x7f   | 04 7f       |
    | add dl, 0x01   | 80 c2 01    | *** | add al, 0x80   | 04 80       |
    | add bl, 0x01   | 80 c3 01    | *** | add al, 0xff   | 04 ff       |
    | add spl, 0x01  | 40 80 c4 01 | *** | add cl, 0x7f   | 80 c1 7f    |
    | add bpl, 0x01  | 40 80 c5 01 | *** | add dl, 0x80   | 80 c2 80    |
    | add sil, 0x01  | 40 80 c6 01 | *** | add bl, 0xff   | 80 c3 ff    |
    | add dil, 0x01  | 40 80 c7 01 | *** | add spl, 0x00  | 40 80 c4 00 |
    | add r8b, 0x01  | 41 80 c0 01 | *** | add sil, 0x7f  | 40 80 c6 7f |
    | add r9b, 0x01  | 41 80 c1 01 | *** | add dil, 0x80  | 40 80 c7 80 |
    | add r10b, 0x01 | 41 80 c2 01 | *** | add r8b, 0xff  | 41 80 c0 ff |
    | add r11b, 0x01 | 41 80 c3 01 | *** | add r9b, 0x00  | 41 80 c1 00 |
    | add r12b, 0x01 | 41 80 c4 01 | *** | add r11b, 0x7f | 41 80 c3 7f |
    | add r13b, 0x01 | 41 80 c5 01 | *** | add r12b, 0x80 | 41 80 c4 80 |
    | add r14b, 0x01 | 41 80 c6 01 | *** | add r13b, 0xff | 41 80 c5 ff |
    | add r15b, 0x01 | 41 80 c7 01 | *** | add r14b, 0x00 | 41 80 c6 00 |
    | add ah, 0x01   | 80 c4 01    | *** | add ah, 0x7f   | 80 c4 7f    |
    | add ch, 0x01   | 80 c5 01    | *** | add ch, 0x80   | 80 c5 80    |
    | add dh, 0x01   | 80 c6 01    | *** | add dh, 0xff   | 80 c6 ff    |
    | add bh, 0x01   | 80 c7 01    | *** | add bh, 0x00   | 80 c7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_add_reg8_imm8():
    encode(ADD_REG8_IMM8)


ADD_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | add al, cl     | 00 c8    | *** | add al, r10b   | 44 00 d0 |
    | add cl, cl     | 00 c9    | *** | add al, r11b   | 44 00 d8 |
    | add dl, cl     | 00 ca    | *** | add al, r12b   | 44 00 e0 |
    | add bl, cl     | 00 cb    | *** | add al, r13b   | 44 00 e8 |
    | add spl, cl    | 40 00 cc | *** | add al, r14b   | 44 00 f0 |
    | add bpl, cl    | 40 00 cd | *** | add al, r15b   | 44 00 f8 |
    | add sil, cl    | 40 00 ce | *** | add al, ah     | 00 e0    |
    | add dil, cl    | 40 00 cf | *** | add al, ch     | 00 e8    |
    | add r8b, cl    | 41 00 c8 | *** | add al, dh     | 00 f0    |
    | add r9b, cl    | 41 00 c9 | *** | add al, bh     | 00 f8    |
    | add r10b, cl   | 41 00 ca | *** | add cl, dl     | 00 d1    |
    | add r11b, cl   | 41 00 cb | *** | add dl, bl     | 00 da    |
    | add r12b, cl   | 41 00 cc | *** | add bl, spl    | 40 00 e3 |
    | add r13b, cl   | 41 00 cd | *** | add spl, bpl   | 40 00 ec |
    | add r14b, cl   | 41 00 ce | *** | add bpl, sil   | 40 00 f5 |
    | add r15b, cl   | 41 00 cf | *** | add sil, dil   | 40 00 fe |
    | add ah, cl     | 00 cc    | *** | add dil, r8b   | 44 00 c7 |
    | add ch, cl     | 00 cd    | *** | add r8b, r9b   | 45 00 c8 |
    | add dh, cl     | 00 ce    | *** | add r9b, r10b  | 45 00 d1 |
    | add bh, cl     | 00 cf    | *** | add r10b, r11b | 45 00 da |
    | add al, al     | 00 c0    | *** | add r11b, r12b | 45 00 e3 |
    | add al, dl     | 00 d0    | *** | add r12b, r13b | 45 00 ec |
    | add al, bl     | 00 d8    | *** | add r13b, r14b | 45 00 f5 |
    | add al, spl    | 40 00 e0 | *** | add r14b, r15b | 45 00 fe |
    | add al, bpl    | 40 00 e8 | *** | add r15b, ah   | !! !! !! |
    | add al, sil    | 40 00 f0 | *** | add ah, ch     | 00 ec    |
    | add al, dil    | 40 00 f8 | *** | add ch, dh     | 00 f5    |
    | add al, r8b    | 44 00 c0 | *** | add dh, bh     | 00 fe    |
    | add al, r9b    | 44 00 c8 | *** | add bh, al     | 00 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_add_reg8_reg8():
    encode(ADD_REG8_REG8)


ADD_REG8_ADDR8 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | add al, byte [rcx]                          | 02 01                   |
    | add cl, byte [rcx]                          | 02 09                   |
    | add dl, byte [rcx]                          | 02 11                   |
    | add bl, byte [rcx]                          | 02 19                   |
    | add spl, byte [rcx]                         | 40 02 21                |
    | add bpl, byte [rcx]                         | 40 02 29                |
    | add sil, byte [rcx]                         | 40 02 31                |
    | add dil, byte [rcx]                         | 40 02 39                |
    | add r8b, byte [rcx]                         | 44 02 01                |
    | add r9b, byte [rcx]                         | 44 02 09                |
    | add r10b, byte [rcx]                        | 44 02 11                |
    | add r11b, byte [rcx]                        | 44 02 19                |
    | add r12b, byte [rcx]                        | 44 02 21                |
    | add r13b, byte [rcx]                        | 44 02 29                |
    | add r14b, byte [rcx]                        | 44 02 31                |
    | add r15b, byte [rcx]                        | 44 02 39                |
    | add ah, byte [rcx]                          | 02 21                   |
    | add ch, byte [rcx]                          | 02 29                   |
    | add dh, byte [rcx]                          | 02 31                   |
    | add bh, byte [rcx]                          | 02 39                   |
    | add al, byte [rax]                          | 02 00                   |
    | add al, byte [rdx]                          | 02 02                   |
    | add al, byte [rbx]                          | 02 03                   |
    | add al, byte [rsp]                          | 02 04 24                |
    | add al, byte [rbp]                          | 02 45 00                |
    | add al, byte [rsi]                          | 02 06                   |
    | add al, byte [rdi]                          | 02 07                   |
    | add al, byte [r8]                           | 41 02 00                |
    | add al, byte [r9]                           | 41 02 01                |
    | add al, byte [r10]                          | 41 02 02                |
    | add al, byte [r11]                          | 41 02 03                |
    | add al, byte [r12]                          | 41 02 04 24             |
    | add al, byte [r13]                          | 41 02 45 00             |
    | add al, byte [r14]                          | 41 02 06                |
    | add al, byte [r15]                          | 41 02 07                |
    | add al, byte [rax + 1 * rcx]                | 02 04 08                |
    | add al, byte [rcx + 1 * rcx]                | 02 04 09                |
    | add al, byte [rdx + 1 * rcx]                | 02 04 0a                |
    | add al, byte [rbx + 1 * rcx]                | 02 04 0b                |
    | add al, byte [rsp + 1 * rcx]                | 02 04 0c                |
    | add al, byte [rbp + 1 * rcx]                | 02 44 0d 00             |
    | add al, byte [rsi + 1 * rcx]                | 02 04 0e                |
    | add al, byte [rdi + 1 * rcx]                | 02 04 0f                |
    | add al, byte [r8 + 1 * rcx]                 | 41 02 04 08             |
    | add al, byte [r9 + 1 * rcx]                 | 41 02 04 09             |
    | add al, byte [r10 + 1 * rcx]                | 41 02 04 0a             |
    | add al, byte [r11 + 1 * rcx]                | 41 02 04 0b             |
    | add al, byte [r12 + 1 * rcx]                | 41 02 04 0c             |
    | add al, byte [r13 + 1 * rcx]                | 41 02 44 0d 00          |
    | add al, byte [r14 + 1 * rcx]                | 41 02 04 0e             |
    | add al, byte [r15 + 1 * rcx]                | 41 02 04 0f             |
    | add al, byte [rax + 1 * rax]                | 02 04 00                |
    | add al, byte [rax + 1 * rdx]                | 02 04 10                |
    | add al, byte [rax + 1 * rbx]                | 02 04 18                |
    | add al, byte [rax + 1 * rbp]                | 02 04 28                |
    | add al, byte [rax + 1 * rsi]                | 02 04 30                |
    | add al, byte [rax + 1 * rdi]                | 02 04 38                |
    | add al, byte [rax + 1 * r8]                 | 42 02 04 00             |
    | add al, byte [rax + 1 * r9]                 | 42 02 04 08             |
    | add al, byte [rax + 1 * r10]                | 42 02 04 10             |
    | add al, byte [rax + 1 * r11]                | 42 02 04 18             |
    | add al, byte [rax + 1 * r12]                | 42 02 04 20             |
    | add al, byte [rax + 1 * r13]                | 42 02 04 28             |
    | add al, byte [rax + 1 * r14]                | 42 02 04 30             |
    | add al, byte [rax + 1 * r15]                | 42 02 04 38             |
    | add al, byte [rax + 2 * rcx]                | 02 04 48                |
    | add al, byte [rax + 4 * rcx]                | 02 04 88                |
    | add al, byte [rax + 8 * rcx]                | 02 04 c8                |
    | add al, byte [r8 + 1 * r9]                  | 43 02 04 08             |
    | add al, byte [r8 + 2 * r9]                  | 43 02 04 48             |
    | add al, byte [r8 + 4 * r9]                  | 43 02 04 88             |
    | add al, byte [r8 + 8 * r9]                  | 43 02 04 c8             |
    | add al, byte [1 * rcx]                      | 02 04 0d 00 00 00 00    |
    | add al, byte [2 * rcx]                      | 02 04 4d 00 00 00 00    |
    | add al, byte [4 * rcx]                      | 02 04 8d 00 00 00 00    |
    | add al, byte [8 * rcx]                      | 02 04 cd 00 00 00 00    |
    | add al, byte [1 * r9]                       | 42 02 04 0d 00 00 00 00 |
    | add al, byte [2 * r9]                       | 42 02 04 4d 00 00 00 00 |
    | add al, byte [4 * r9]                       | 42 02 04 8d 00 00 00 00 |
    | add al, byte [8 * r9]                       | 42 02 04 cd 00 00 00 00 |
    | add al, byte [r13 + 8 * r12]                | 43 02 44 e5 00          |
    | add al, byte [rsp + 4 * r15]                | 42 02 04 bc             |
    | add al, byte [rax + 1 * rcx + 0x00]         | 02 44 08 00             |
    | add al, byte [rax + 1 * rcx - 0x00]         | 02 44 08 00             |
    | add al, byte [rax + 1 * rcx + 0x01]         | 02 44 08 01             |
    | add al, byte [rax + 1 * rcx - 0x01]         | 02 44 08 ff             |
    | add al, byte [rax + 1 * rcx + 0x00000001]   | 02 84 08 01 00 00 00    |
    | add al, byte [rax + 1 * rcx - 0x00000001]   | 02 84 08 ff ff ff ff    |
    | add al, byte [rax + 1 * rcx + 0x7f]         | 02 44 08 7f             |
    | add al, byte [rax + 1 * rcx - 0x7f]         | 02 44 08 81             |
    | add al, byte [rax + 1 * rcx + 0x80]         | 02 84 08 80 00 00 00    |
    | add al, byte [rax + 1 * rcx - 0x80]         | 02 44 08 80             |
    | add al, byte [rax + 1 * rcx - 0x81]         | 02 84 08 7f ff ff ff    |
    | add al, byte [rax + 1 * rcx + 0xff]         | 02 84 08 ff 00 00 00    |
    | add al, byte [rax + 1 * rcx - 0xff]         | 02 84 08 01 ff ff ff    |
    | add al, byte [rax + 1 * rcx + 0x7fffffff]   | 02 84 08 ff ff ff 7f    |
    | add al, byte [rax + 1 * rcx - 0x7fffffff]   | 02 84 08 01 00 00 80    |
    | add al, byte [rax + 1 * rcx - 0x80000000]   | 02 84 08 00 00 00 80    |
    | add al, byte [r10 + 0x7f]                   | 41 02 42 7f             |
    | add al, byte [r10 + 0x80]                   | 41 02 82 80 00 00 00    |
    | add al, byte [r10 - 0x80]                   | 41 02 42 80             |
    | add al, byte [r10 - 0x81]                   | 41 02 82 7f ff ff ff    |
    | add cl, byte [rdx]                          | 02 0a                   |
    | add dl, byte [rbx]                          | 02 13                   |
    | add bl, byte [rsp]                          | 02 1c 24                |
    | add spl, byte [rbp]                         | 40 02 65 00             |
    | add bpl, byte [rsi]                         | 40 02 2e                |
    | add sil, byte [rdi]                         | 40 02 37                |
    | add dil, byte [r8]                          | 41 02 38                |
    | add r8b, byte [r9]                          | 45 02 01                |
    | add r9b, byte [r10]                         | 45 02 0a                |
    | add r10b, byte [r11]                        | 45 02 13                |
    | add r11b, byte [r12]                        | 45 02 1c 24             |
    | add r12b, byte [r13]                        | 45 02 65 00             |
    | add r13b, byte [r14]                        | 45 02 2e                |
    | add r14b, byte [r15]                        | 45 02 37                |
    | add r15b, byte [rax + 1 * rcx]              | 44 02 3c 08             |
    | add ah, byte [rcx + 1 * rcx]                | 02 24 09                |
    | add ch, byte [rdx + 1 * rcx]                | 02 2c 0a                |
    | add dh, byte [rbx + 1 * rcx]                | 02 34 0b                |
    | add bh, byte [rsp + 1 * rcx]                | 02 3c 0c                |
    | add cl, byte [rsi + 1 * rcx]                | 02 0c 0e                |
    | add dl, byte [rdi + 1 * rcx]                | 02 14 0f                |
    | add bl, byte [r8 + 1 * rcx]                 | 41 02 1c 08             |
    | add spl, byte [r9 + 1 * rcx]                | 41 02 24 09             |
    | add bpl, byte [r10 + 1 * rcx]               | 41 02 2c 0a             |
    | add sil, byte [r11 + 1 * rcx]               | 41 02 34 0b             |
    | add dil, byte [r12 + 1 * rcx]               | 41 02 3c 0c             |
    | add r8b, byte [r13 + 1 * rcx]               | 45 02 44 0d 00          |
    | add r9b, byte [r14 + 1 * rcx]               | 45 02 0c 0e             |
    | add r10b, byte [r15 + 1 * rcx]              | 45 02 14 0f             |
    | add r11b, byte [rax + 1 * rax]              | 44 02 1c 00             |
    | add r12b, byte [rax + 1 * rdx]              | 44 02 24 10             |
    | add r13b, byte [rax + 1 * rbx]              | 44 02 2c 18             |
    | add r14b, byte [rax + 1 * rbp]              | 44 02 34 28             |
    | add r15b, byte [rax + 1 * rsi]              | 44 02 3c 30             |
    | add ah, byte [rax + 1 * rdi]                | 02 24 38                |
    | add ch, byte [rax + 1 * r8]                 | !! !! !!                |
    | add dh, byte [rax + 1 * r9]                 | !! !! !!                |
    | add bh, byte [rax + 1 * r10]                | !! !! !!                |
    | add cl, byte [rax + 1 * r12]                | 42 02 0c 20             |
    | add dl, byte [rax + 1 * r13]                | 42 02 14 28             |
    | add bl, byte [rax + 1 * r14]                | 42 02 1c 30             |
    | add spl, byte [rax + 1 * r15]               | 42 02 24 38             |
    | add bpl, byte [rax + 2 * rcx]               | 40 02 2c 48             |
    | add sil, byte [rax + 4 * rcx]               | 40 02 34 88             |
    | add dil, byte [rax + 8 * rcx]               | 40 02 3c c8             |
    | add r8b, byte [r8 + 1 * r9]                 | 47 02 04 08             |
    | add r9b, byte [r8 + 2 * r9]                 | 47 02 0c 48             |
    | add r10b, byte [r8 + 4 * r9]                | 47 02 14 88             |
    | add r11b, byte [r8 + 8 * r9]                | 47 02 1c c8             |
    | add r12b, byte [1 * rcx]                    | 44 02 24 0d 00 00 00 00 |
    | add r13b, byte [2 * rcx]                    | 44 02 2c 4d 00 00 00 00 |
    | add r14b, byte [4 * rcx]                    | 44 02 34 8d 00 00 00 00 |
    | add r15b, byte [8 * rcx]                    | 44 02 3c cd 00 00 00 00 |
    | add ah, byte [1 * r9]                       | !! !! !!                |
    | add ch, byte [2 * r9]                       | !! !! !!                |
    | add dh, byte [4 * r9]                       | !! !! !!                |
    | add bh, byte [8 * r9]                       | !! !! !!                |
    | add cl, byte [rsp + 4 * r15]                | 42 02 0c bc             |
    | add dl, byte [rax + 1 * rcx + 0x00]         | 02 54 08 00             |
    | add bl, byte [rax + 1 * rcx - 0x00]         | 02 5c 08 00             |
    | add spl, byte [rax + 1 * rcx + 0x01]        | 40 02 64 08 01          |
    | add bpl, byte [rax + 1 * rcx - 0x01]        | 40 02 6c 08 ff          |
    | add sil, byte [rax + 1 * rcx + 0x00000001]  | 40 02 b4 08 01 00 00 00 |
    | add dil, byte [rax + 1 * rcx - 0x00000001]  | 40 02 bc 08 ff ff ff ff |
    | add r8b, byte [rax + 1 * rcx + 0x7f]        | 44 02 44 08 7f          |
    | add r9b, byte [rax + 1 * rcx - 0x7f]        | 44 02 4c 08 81          |
    | add r10b, byte [rax + 1 * rcx + 0x80]       | 44 02 94 08 80 00 00 00 |
    | add r11b, byte [rax + 1 * rcx - 0x80]       | 44 02 5c 08 80          |
    | add r12b, byte [rax + 1 * rcx - 0x81]       | 44 02 a4 08 7f ff ff ff |
    | add r13b, byte [rax + 1 * rcx + 0xff]       | 44 02 ac 08 ff 00 00 00 |
    | add r14b, byte [rax + 1 * rcx - 0xff]       | 44 02 b4 08 01 ff ff ff |
    | add r15b, byte [rax + 1 * rcx + 0x7fffffff] | 44 02 bc 08 ff ff ff 7f |
    | add ah, byte [rax + 1 * rcx - 0x7fffffff]   | 02 a4 08 01 00 00 80    |
    | add ch, byte [rax + 1 * rcx - 0x80000000]   | 02 ac 08 00 00 00 80    |
    | add dh, byte [r10 + 0x7f]                   | !! !! !!                |
    | add bh, byte [r10 + 0x80]                   | !! !! !!                |
    | add cl, byte [r10 - 0x81]                   | 41 02 8a 7f ff ff ff    |
    | add dl, byte [rax]                          | 02 10                   |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_add_reg8_addr8():
    encode(ADD_REG8_ADDR8)


ADD_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | add qword [rax], 0x01                        | 48 83 00 01                |
    | add qword [rcx], 0x01                        | 48 83 01 01                |
    | add qword [rdx], 0x01                        | 48 83 02 01                |
    | add qword [rbx], 0x01                        | 48 83 03 01                |
    | add qword [rsp], 0x01                        | 48 83 04 24 01             |
    | add qword [rbp], 0x01                        | 48 83 45 00 01             |
    | add qword [rsi], 0x01                        | 48 83 06 01                |
    | add qword [rdi], 0x01                        | 48 83 07 01                |
    | add qword [r8], 0x01                         | 49 83 00 01                |
    | add qword [r9], 0x01                         | 49 83 01 01                |
    | add qword [r10], 0x01                        | 49 83 02 01                |
    | add qword [r11], 0x01                        | 49 83 03 01                |
    | add qword [r12], 0x01                        | 49 83 04 24 01             |
    | add qword [r13], 0x01                        | 49 83 45 00 01             |
    | add qword [r14], 0x01                        | 49 83 06 01                |
    | add qword [r15], 0x01                        | 49 83 07 01                |
    | add qword [rax + 1 * rcx], 0x01              | 48 83 04 08 01             |
    | add qword [rcx + 1 * rcx], 0x01              | 48 83 04 09 01             |
    | add qword [rdx + 1 * rcx], 0x01              | 48 83 04 0a 01             |
    | add qword [rbx + 1 * rcx], 0x01              | 48 83 04 0b 01             |
    | add qword [rsp + 1 * rcx], 0x01              | 48 83 04 0c 01             |
    | add qword [rbp + 1 * rcx], 0x01              | 48 83 44 0d 00 01          |
    | add qword [rsi + 1 * rcx], 0x01              | 48 83 04 0e 01             |
    | add qword [rdi + 1 * rcx], 0x01              | 48 83 04 0f 01             |
    | add qword [r8 + 1 * rcx], 0x01               | 49 83 04 08 01             |
    | add qword [r9 + 1 * rcx], 0x01               | 49 83 04 09 01             |
    | add qword [r10 + 1 * rcx], 0x01              | 49 83 04 0a 01             |
    | add qword [r11 + 1 * rcx], 0x01              | 49 83 04 0b 01             |
    | add qword [r12 + 1 * rcx], 0x01              | 49 83 04 0c 01             |
    | add qword [r13 + 1 * rcx], 0x01              | 49 83 44 0d 00 01          |
    | add qword [r14 + 1 * rcx], 0x01              | 49 83 04 0e 01             |
    | add qword [r15 + 1 * rcx], 0x01              | 49 83 04 0f 01             |
    | add qword [rax + 1 * rax], 0x01              | 48 83 04 00 01             |
    | add qword [rax + 1 * rdx], 0x01              | 48 83 04 10 01             |
    | add qword [rax + 1 * rbx], 0x01              | 48 83 04 18 01             |
    | add qword [rax + 1 * rbp], 0x01              | 48 83 04 28 01             |
    | add qword [rax + 1 * rsi], 0x01              | 48 83 04 30 01             |
    | add qword [rax + 1 * rdi], 0x01              | 48 83 04 38 01             |
    | add qword [rax + 1 * r8], 0x01               | 4a 83 04 00 01             |
    | add qword [rax + 1 * r9], 0x01               | 4a 83 04 08 01             |
    | add qword [rax + 1 * r10], 0x01              | 4a 83 04 10 01             |
    | add qword [rax + 1 * r11], 0x01              | 4a 83 04 18 01             |
    | add qword [rax + 1 * r12], 0x01              | 4a 83 04 20 01             |
    | add qword [rax + 1 * r13], 0x01              | 4a 83 04 28 01             |
    | add qword [rax + 1 * r14], 0x01              | 4a 83 04 30 01             |
    | add qword [rax + 1 * r15], 0x01              | 4a 83 04 38 01             |
    | add qword [rax + 2 * rcx], 0x01              | 48 83 04 48 01             |
    | add qword [rax + 4 * rcx], 0x01              | 48 83 04 88 01             |
    | add qword [rax + 8 * rcx], 0x01              | 48 83 04 c8 01             |
    | add qword [r8 + 1 * r9], 0x01                | 4b 83 04 08 01             |
    | add qword [r8 + 2 * r9], 0x01                | 4b 83 04 48 01             |
    | add qword [r8 + 4 * r9], 0x01                | 4b 83 04 88 01             |
    | add qword [r8 + 8 * r9], 0x01                | 4b 83 04 c8 01             |
    | add qword [1 * rcx], 0x01                    | 48 83 04 0d 00 00 00 00 01 |
    | add qword [2 * rcx], 0x01                    | 48 83 04 4d 00 00 00 00 01 |
    | add qword [4 * rcx], 0x01                    | 48 83 04 8d 00 00 00 00 01 |
    | add qword [8 * rcx], 0x01                    | 48 83 04 cd 00 00 00 00 01 |
    | add qword [1 * r9], 0x01                     | 4a 83 04 0d 00 00 00 00 01 |
    | add qword [2 * r9], 0x01                     | 4a 83 04 4d 00 00 00 00 01 |
    | add qword [4 * r9], 0x01                     | 4a 83 04 8d 00 00 00 00 01 |
    | add qword [8 * r9], 0x01                     | 4a 83 04 cd 00 00 00 00 01 |
    | add qword [r13 + 8 * r12], 0x01              | 4b 83 44 e5 00 01          |
    | add qword [rsp + 4 * r15], 0x01              | 4a 83 04 bc 01             |
    | add qword [rax + 1 * rcx + 0x00], 0x01       | 48 83 44 08 00 01          |
    | add qword [rax + 1 * rcx - 0x00], 0x01       | 48 83 44 08 00 01          |
    | add qword [rax + 1 * rcx + 0x01], 0x01       | 48 83 44 08 01 01          |
    | add qword [rax + 1 * rcx - 0x01], 0x01       | 48 83 44 08 ff 01          |
    | add qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 83 84 08 01 00 00 00 01 |
    | add qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 83 84 08 ff ff ff ff 01 |
    | add qword [rax + 1 * rcx + 0x7f], 0x01       | 48 83 44 08 7f 01          |
    | add qword [rax + 1 * rcx - 0x7f], 0x01       | 48 83 44 08 81 01          |
    | add qword [rax + 1 * rcx + 0x80], 0x01       | 48 83 84 08 80 00 00 00 01 |
    | add qword [rax + 1 * rcx - 0x80], 0x01       | 48 83 44 08 80 01          |
    | add qword [rax + 1 * rcx - 0x81], 0x01       | 48 83 84 08 7f ff ff ff 01 |
    | add qword [rax + 1 * rcx + 0xff], 0x01       | 48 83 84 08 ff 00 00 00 01 |
    | add qword [rax + 1 * rcx - 0xff], 0x01       | 48 83 84 08 01 ff ff ff 01 |
    | add qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 83 84 08 ff ff ff 7f 01 |
    | add qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 83 84 08 01 00 00 80 01 |
    | add qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 83 84 08 00 00 00 80 01 |
    | add qword [r10 + 0x7f], 0x01                 | 49 83 42 7f 01             |
    | add qword [r10 + 0x80], 0x01                 | 49 83 82 80 00 00 00 01    |
    | add qword [r10 - 0x80], 0x01                 | 49 83 42 80 01             |
    | add qword [r10 - 0x81], 0x01                 | 49 83 82 7f ff ff ff 01    |
    | add qword [rax], 0x00                        | 48 83 00 00                |
    | add qword [rax], 0x7f                        | 48 83 00 7f                |
    | add qword [rax], 0x80                        | 48 83 00 80                |
    | add qword [rax], 0xff                        | 48 83 00 ff                |
    | add qword [rcx], 0x7f                        | 48 83 01 7f                |
    | add qword [rdx], 0x80                        | 48 83 02 80                |
    | add qword [rbx], 0xff                        | 48 83 03 ff                |
    | add qword [rsp], 0x00                        | 48 83 04 24 00             |
    | add qword [rsi], 0x7f                        | 48 83 06 7f                |
    | add qword [rdi], 0x80                        | 48 83 07 80                |
    | add qword [r8], 0xff                         | 49 83 00 ff                |
    | add qword [r9], 0x00                         | 49 83 01 00                |
    | add qword [r11], 0x7f                        | 49 83 03 7f                |
    | add qword [r12], 0x80                        | 49 83 04 24 80             |
    | add qword [r13], 0xff                        | 49 83 45 00 ff             |
    | add qword [r14], 0x00                        | 49 83 06 00                |
    | add qword [rax + 1 * rcx], 0x7f              | 48 83 04 08 7f             |
    | add qword [rcx + 1 * rcx], 0x80              | 48 83 04 09 80             |
    | add qword [rdx + 1 * rcx], 0xff              | 48 83 04 0a ff             |
    | add qword [rbx + 1 * rcx], 0x00              | 48 83 04 0b 00             |
    | add qword [rbp + 1 * rcx], 0x7f              | 48 83 44 0d 00 7f          |
    | add qword [rsi + 1 * rcx], 0x80              | 48 83 04 0e 80             |
    | add qword [rdi + 1 * rcx], 0xff              | 48 83 04 0f ff             |
    | add qword [r8 + 1 * rcx], 0x00               | 49 83 04 08 00             |
    | add qword [r10 + 1 * rcx], 0x7f              | 49 83 04 0a 7f             |
    | add qword [r11 + 1 * rcx], 0x80              | 49 83 04 0b 80             |
    | add qword [r12 + 1 * rcx], 0xff              | 49 83 04 0c ff             |
    | add qword [r13 + 1 * rcx], 0x00              | 49 83 44 0d 00 00          |
    | add qword [r15 + 1 * rcx], 0x7f              | 49 83 04 0f 7f             |
    | add qword [rax + 1 * rax], 0x80              | 48 83 04 00 80             |
    | add qword [rax + 1 * rdx], 0xff              | 48 83 04 10 ff             |
    | add qword [rax + 1 * rbx], 0x00              | 48 83 04 18 00             |
    | add qword [rax + 1 * rsi], 0x7f              | 48 83 04 30 7f             |
    | add qword [rax + 1 * rdi], 0x80              | 48 83 04 38 80             |
    | add qword [rax + 1 * r8], 0xff               | 4a 83 04 00 ff             |
    | add qword [rax + 1 * r9], 0x00               | 4a 83 04 08 00             |
    | add qword [rax + 1 * r11], 0x7f              | 4a 83 04 18 7f             |
    | add qword [rax + 1 * r12], 0x80              | 4a 83 04 20 80             |
    | add qword [rax + 1 * r13], 0xff              | 4a 83 04 28 ff             |
    | add qword [rax + 1 * r14], 0x00              | 4a 83 04 30 00             |
    | add qword [rax + 2 * rcx], 0x7f              | 48 83 04 48 7f             |
    | add qword [rax + 4 * rcx], 0x80              | 48 83 04 88 80             |
    | add qword [rax + 8 * rcx], 0xff              | 48 83 04 c8 ff             |
    | add qword [r8 + 1 * r9], 0x00                | 4b 83 04 08 00             |
    | add qword [r8 + 4 * r9], 0x7f                | 4b 83 04 88 7f             |
    | add qword [r8 + 8 * r9], 0x80                | 4b 83 04 c8 80             |
    | add qword [1 * rcx], 0xff                    | 48 83 04 0d 00 00 00 00 ff |
    | add qword [2 * rcx], 0x00                    | 48 83 04 4d 00 00 00 00 00 |
    | add qword [8 * rcx], 0x7f                    | 48 83 04 cd 00 00 00 00 7f |
    | add qword [1 * r9], 0x80                     | 4a 83 04 0d 00 00 00 00 80 |
    | add qword [2 * r9], 0xff                     | 4a 83 04 4d 00 00 00 00 ff |
    | add qword [4 * r9], 0x00                     | 4a 83 04 8d 00 00 00 00 00 |
    | add qword [r13 + 8 * r12], 0x7f              | 4b 83 44 e5 00 7f          |
    | add qword [rsp + 4 * r15], 0x80              | 4a 83 04 bc 80             |
    | add qword [rax + 1 * rcx + 0x00], 0xff       | 48 83 44 08 00 ff          |
    | add qword [rax + 1 * rcx - 0x00], 0x00       | 48 83 44 08 00 00          |
    | add qword [rax + 1 * rcx - 0x01], 0x7f       | 48 83 44 08 ff 7f          |
    | add qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 83 84 08 01 00 00 00 80 |
    | add qword [rax + 1 * rcx - 0x00000001], 0xff | 48 83 84 08 ff ff ff ff ff |
    | add qword [rax + 1 * rcx + 0x7f], 0x00       | 48 83 44 08 7f 00          |
    | add qword [rax + 1 * rcx + 0x80], 0x7f       | 48 83 84 08 80 00 00 00 7f |
    | add qword [rax + 1 * rcx - 0x80], 0x80       | 48 83 44 08 80 80          |
    | add qword [rax + 1 * rcx - 0x81], 0xff       | 48 83 84 08 7f ff ff ff ff |
    | add qword [rax + 1 * rcx + 0xff], 0x00       | 48 83 84 08 ff 00 00 00 00 |
    | add qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 83 84 08 ff ff ff 7f 7f |
    | add qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 83 84 08 01 00 00 80 80 |
    | add qword [rax + 1 * rcx - 0x80000000], 0xff | 48 83 84 08 00 00 00 80 ff |
    | add qword [r10 + 0x7f], 0x00                 | 49 83 42 7f 00             |
    | add qword [r10 - 0x80], 0x7f                 | 49 83 42 80 7f             |
    | add qword [r10 - 0x81], 0x80                 | 49 83 82 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_add_addr64_imm8():
    encode(ADD_ADDR64_IMM8)


ADD_ADDR64_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | add qword [rax], 0x00000001                        | 48 81 00 01 00 00 00                |
    | add qword [rcx], 0x00000001                        | 48 81 01 01 00 00 00                |
    | add qword [rdx], 0x00000001                        | 48 81 02 01 00 00 00                |
    | add qword [rbx], 0x00000001                        | 48 81 03 01 00 00 00                |
    | add qword [rsp], 0x00000001                        | 48 81 04 24 01 00 00 00             |
    | add qword [rbp], 0x00000001                        | 48 81 45 00 01 00 00 00             |
    | add qword [rsi], 0x00000001                        | 48 81 06 01 00 00 00                |
    | add qword [rdi], 0x00000001                        | 48 81 07 01 00 00 00                |
    | add qword [r8], 0x00000001                         | 49 81 00 01 00 00 00                |
    | add qword [r9], 0x00000001                         | 49 81 01 01 00 00 00                |
    | add qword [r10], 0x00000001                        | 49 81 02 01 00 00 00                |
    | add qword [r11], 0x00000001                        | 49 81 03 01 00 00 00                |
    | add qword [r12], 0x00000001                        | 49 81 04 24 01 00 00 00             |
    | add qword [r13], 0x00000001                        | 49 81 45 00 01 00 00 00             |
    | add qword [r14], 0x00000001                        | 49 81 06 01 00 00 00                |
    | add qword [r15], 0x00000001                        | 49 81 07 01 00 00 00                |
    | add qword [rax + 1 * rcx], 0x00000001              | 48 81 04 08 01 00 00 00             |
    | add qword [rcx + 1 * rcx], 0x00000001              | 48 81 04 09 01 00 00 00             |
    | add qword [rdx + 1 * rcx], 0x00000001              | 48 81 04 0a 01 00 00 00             |
    | add qword [rbx + 1 * rcx], 0x00000001              | 48 81 04 0b 01 00 00 00             |
    | add qword [rsp + 1 * rcx], 0x00000001              | 48 81 04 0c 01 00 00 00             |
    | add qword [rbp + 1 * rcx], 0x00000001              | 48 81 44 0d 00 01 00 00 00          |
    | add qword [rsi + 1 * rcx], 0x00000001              | 48 81 04 0e 01 00 00 00             |
    | add qword [rdi + 1 * rcx], 0x00000001              | 48 81 04 0f 01 00 00 00             |
    | add qword [r8 + 1 * rcx], 0x00000001               | 49 81 04 08 01 00 00 00             |
    | add qword [r9 + 1 * rcx], 0x00000001               | 49 81 04 09 01 00 00 00             |
    | add qword [r10 + 1 * rcx], 0x00000001              | 49 81 04 0a 01 00 00 00             |
    | add qword [r11 + 1 * rcx], 0x00000001              | 49 81 04 0b 01 00 00 00             |
    | add qword [r12 + 1 * rcx], 0x00000001              | 49 81 04 0c 01 00 00 00             |
    | add qword [r13 + 1 * rcx], 0x00000001              | 49 81 44 0d 00 01 00 00 00          |
    | add qword [r14 + 1 * rcx], 0x00000001              | 49 81 04 0e 01 00 00 00             |
    | add qword [r15 + 1 * rcx], 0x00000001              | 49 81 04 0f 01 00 00 00             |
    | add qword [rax + 1 * rax], 0x00000001              | 48 81 04 00 01 00 00 00             |
    | add qword [rax + 1 * rdx], 0x00000001              | 48 81 04 10 01 00 00 00             |
    | add qword [rax + 1 * rbx], 0x00000001              | 48 81 04 18 01 00 00 00             |
    | add qword [rax + 1 * rbp], 0x00000001              | 48 81 04 28 01 00 00 00             |
    | add qword [rax + 1 * rsi], 0x00000001              | 48 81 04 30 01 00 00 00             |
    | add qword [rax + 1 * rdi], 0x00000001              | 48 81 04 38 01 00 00 00             |
    | add qword [rax + 1 * r8], 0x00000001               | 4a 81 04 00 01 00 00 00             |
    | add qword [rax + 1 * r9], 0x00000001               | 4a 81 04 08 01 00 00 00             |
    | add qword [rax + 1 * r10], 0x00000001              | 4a 81 04 10 01 00 00 00             |
    | add qword [rax + 1 * r11], 0x00000001              | 4a 81 04 18 01 00 00 00             |
    | add qword [rax + 1 * r12], 0x00000001              | 4a 81 04 20 01 00 00 00             |
    | add qword [rax + 1 * r13], 0x00000001              | 4a 81 04 28 01 00 00 00             |
    | add qword [rax + 1 * r14], 0x00000001              | 4a 81 04 30 01 00 00 00             |
    | add qword [rax + 1 * r15], 0x00000001              | 4a 81 04 38 01 00 00 00             |
    | add qword [rax + 2 * rcx], 0x00000001              | 48 81 04 48 01 00 00 00             |
    | add qword [rax + 4 * rcx], 0x00000001              | 48 81 04 88 01 00 00 00             |
    | add qword [rax + 8 * rcx], 0x00000001              | 48 81 04 c8 01 00 00 00             |
    | add qword [r8 + 1 * r9], 0x00000001                | 4b 81 04 08 01 00 00 00             |
    | add qword [r8 + 2 * r9], 0x00000001                | 4b 81 04 48 01 00 00 00             |
    | add qword [r8 + 4 * r9], 0x00000001                | 4b 81 04 88 01 00 00 00             |
    | add qword [r8 + 8 * r9], 0x00000001                | 4b 81 04 c8 01 00 00 00             |
    | add qword [1 * rcx], 0x00000001                    | 48 81 04 0d 00 00 00 00 01 00 00 00 |
    | add qword [2 * rcx], 0x00000001                    | 48 81 04 4d 00 00 00 00 01 00 00 00 |
    | add qword [4 * rcx], 0x00000001                    | 48 81 04 8d 00 00 00 00 01 00 00 00 |
    | add qword [8 * rcx], 0x00000001                    | 48 81 04 cd 00 00 00 00 01 00 00 00 |
    | add qword [1 * r9], 0x00000001                     | 4a 81 04 0d 00 00 00 00 01 00 00 00 |
    | add qword [2 * r9], 0x00000001                     | 4a 81 04 4d 00 00 00 00 01 00 00 00 |
    | add qword [4 * r9], 0x00000001                     | 4a 81 04 8d 00 00 00 00 01 00 00 00 |
    | add qword [8 * r9], 0x00000001                     | 4a 81 04 cd 00 00 00 00 01 00 00 00 |
    | add qword [r13 + 8 * r12], 0x00000001              | 4b 81 44 e5 00 01 00 00 00          |
    | add qword [rsp + 4 * r15], 0x00000001              | 4a 81 04 bc 01 00 00 00             |
    | add qword [rax + 1 * rcx + 0x00], 0x00000001       | 48 81 44 08 00 01 00 00 00          |
    | add qword [rax + 1 * rcx - 0x00], 0x00000001       | 48 81 44 08 00 01 00 00 00          |
    | add qword [rax + 1 * rcx + 0x01], 0x00000001       | 48 81 44 08 01 01 00 00 00          |
    | add qword [rax + 1 * rcx - 0x01], 0x00000001       | 48 81 44 08 ff 01 00 00 00          |
    | add qword [rax + 1 * rcx + 0x00000001], 0x00000001 | 48 81 84 08 01 00 00 00 01 00 00 00 |
    | add qword [rax + 1 * rcx - 0x00000001], 0x00000001 | 48 81 84 08 ff ff ff ff 01 00 00 00 |
    | add qword [rax + 1 * rcx + 0x7f], 0x00000001       | 48 81 44 08 7f 01 00 00 00          |
    | add qword [rax + 1 * rcx - 0x7f], 0x00000001       | 48 81 44 08 81 01 00 00 00          |
    | add qword [rax + 1 * rcx + 0x80], 0x00000001       | 48 81 84 08 80 00 00 00 01 00 00 00 |
    | add qword [rax + 1 * rcx - 0x80], 0x00000001       | 48 81 44 08 80 01 00 00 00          |
    | add qword [rax + 1 * rcx - 0x81], 0x00000001       | 48 81 84 08 7f ff ff ff 01 00 00 00 |
    | add qword [rax + 1 * rcx + 0xff], 0x00000001       | 48 81 84 08 ff 00 00 00 01 00 00 00 |
    | add qword [rax + 1 * rcx - 0xff], 0x00000001       | 48 81 84 08 01 ff ff ff 01 00 00 00 |
    | add qword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 48 81 84 08 ff ff ff 7f 01 00 00 00 |
    | add qword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 48 81 84 08 01 00 00 80 01 00 00 00 |
    | add qword [rax + 1 * rcx - 0x80000000], 0x00000001 | 48 81 84 08 00 00 00 80 01 00 00 00 |
    | add qword [r10 + 0x7f], 0x00000001                 | 49 81 42 7f 01 00 00 00             |
    | add qword [r10 + 0x80], 0x00000001                 | 49 81 82 80 00 00 00 01 00 00 00    |
    | add qword [r10 - 0x80], 0x00000001                 | 49 81 42 80 01 00 00 00             |
    | add qword [r10 - 0x81], 0x00000001                 | 49 81 82 7f ff ff ff 01 00 00 00    |
    | add qword [rax], 0x00000000                        | 48 81 00 00 00 00 00                |
    | add qword [rax], 0x0000007f                        | 48 81 00 7f 00 00 00                |
    | add qword [rax], 0x00000080                        | 48 81 00 80 00 00 00                |
    | add qword [rax], 0x000000ff                        | 48 81 00 ff 00 00 00                |
    | add qword [rax], 0x00000100                        | 48 81 00 00 01 00 00                |
    | add qword [rax], 0x00007fff                        | 48 81 00 ff 7f 00 00                |
    | add qword [rax], 0x00008000                        | 48 81 00 00 80 00 00                |
    | add qword [rax], 0x0000ffff                        | 48 81 00 ff ff 00 00                |
    | add qword [rax], 0x00010000                        | 48 81 00 00 00 01 00                |
    | add qword [rax], 0x7fffffff                        | 48 81 00 ff ff ff 7f                |
    | add qword [rax], 0x80000000                        | 48 81 00 00 00 00 80                |
    | add qword [rax], 0xffffffff                        | 48 81 00 ff ff ff ff                |
    | add qword [rcx], 0x0000007f                        | 48 81 01 7f 00 00 00                |
    | add qword [rdx], 0x00000080                        | 48 81 02 80 00 00 00                |
    | add qword [rbx], 0x000000ff                        | 48 81 03 ff 00 00 00                |
    | add qword [rsp], 0x00000100                        | 48 81 04 24 00 01 00 00             |
    | add qword [rbp], 0x00007fff                        | 48 81 45 00 ff 7f 00 00             |
    | add qword [rsi], 0x00008000                        | 48 81 06 00 80 00 00                |
    | add qword [rdi], 0x0000ffff                        | 48 81 07 ff ff 00 00                |
    | add qword [r8], 0x00010000                         | 49 81 00 00 00 01 00                |
    | add qword [r9], 0x7fffffff                         | 49 81 01 ff ff ff 7f                |
    | add qword [r10], 0x80000000                        | 49 81 02 00 00 00 80                |
    | add qword [r11], 0xffffffff                        | 49 81 03 ff ff ff ff                |
    | add qword [r12], 0x00000000                        | 49 81 04 24 00 00 00 00             |
    | add qword [r14], 0x0000007f                        | 49 81 06 7f 00 00 00                |
    | add qword [r15], 0x00000080                        | 49 81 07 80 00 00 00                |
    | add qword [rax + 1 * rcx], 0x000000ff              | 48 81 04 08 ff 00 00 00             |
    | add qword [rcx + 1 * rcx], 0x00000100              | 48 81 04 09 00 01 00 00             |
    | add qword [rdx + 1 * rcx], 0x00007fff              | 48 81 04 0a ff 7f 00 00             |
    | add qword [rbx + 1 * rcx], 0x00008000              | 48 81 04 0b 00 80 00 00             |
    | add qword [rsp + 1 * rcx], 0x0000ffff              | 48 81 04 0c ff ff 00 00             |
    | add qword [rbp + 1 * rcx], 0x00010000              | 48 81 44 0d 00 00 00 01 00          |
    | add qword [rsi + 1 * rcx], 0x7fffffff              | 48 81 04 0e ff ff ff 7f             |
    | add qword [rdi + 1 * rcx], 0x80000000              | 48 81 04 0f 00 00 00 80             |
    | add qword [r8 + 1 * rcx], 0xffffffff               | 49 81 04 08 ff ff ff ff             |
    | add qword [r9 + 1 * rcx], 0x00000000               | 49 81 04 09 00 00 00 00             |
    | add qword [r11 + 1 * rcx], 0x0000007f              | 49 81 04 0b 7f 00 00 00             |
    | add qword [r12 + 1 * rcx], 0x00000080              | 49 81 04 0c 80 00 00 00             |
    | add qword [r13 + 1 * rcx], 0x000000ff              | 49 81 44 0d 00 ff 00 00 00          |
    | add qword [r14 + 1 * rcx], 0x00000100              | 49 81 04 0e 00 01 00 00             |
    | add qword [r15 + 1 * rcx], 0x00007fff              | 49 81 04 0f ff 7f 00 00             |
    | add qword [rax + 1 * rax], 0x00008000              | 48 81 04 00 00 80 00 00             |
    | add qword [rax + 1 * rdx], 0x0000ffff              | 48 81 04 10 ff ff 00 00             |
    | add qword [rax + 1 * rbx], 0x00010000              | 48 81 04 18 00 00 01 00             |
    | add qword [rax + 1 * rbp], 0x7fffffff              | 48 81 04 28 ff ff ff 7f             |
    | add qword [rax + 1 * rsi], 0x80000000              | 48 81 04 30 00 00 00 80             |
    | add qword [rax + 1 * rdi], 0xffffffff              | 48 81 04 38 ff ff ff ff             |
    | add qword [rax + 1 * r8], 0x00000000               | 4a 81 04 00 00 00 00 00             |
    | add qword [rax + 1 * r10], 0x0000007f              | 4a 81 04 10 7f 00 00 00             |
    | add qword [rax + 1 * r11], 0x00000080              | 4a 81 04 18 80 00 00 00             |
    | add qword [rax + 1 * r12], 0x000000ff              | 4a 81 04 20 ff 00 00 00             |
    | add qword [rax + 1 * r13], 0x00000100              | 4a 81 04 28 00 01 00 00             |
    | add qword [rax + 1 * r14], 0x00007fff              | 4a 81 04 30 ff 7f 00 00             |
    | add qword [rax + 1 * r15], 0x00008000              | 4a 81 04 38 00 80 00 00             |
    | add qword [rax + 2 * rcx], 0x0000ffff              | 48 81 04 48 ff ff 00 00             |
    | add qword [rax + 4 * rcx], 0x00010000              | 48 81 04 88 00 00 01 00             |
    | add qword [rax + 8 * rcx], 0x7fffffff              | 48 81 04 c8 ff ff ff 7f             |
    | add qword [r8 + 1 * r9], 0x80000000                | 4b 81 04 08 00 00 00 80             |
    | add qword [r8 + 2 * r9], 0xffffffff                | 4b 81 04 48 ff ff ff ff             |
    | add qword [r8 + 4 * r9], 0x00000000                | 4b 81 04 88 00 00 00 00             |
    | add qword [1 * rcx], 0x0000007f                    | 48 81 04 0d 00 00 00 00 7f 00 00 00 |
    | add qword [2 * rcx], 0x00000080                    | 48 81 04 4d 00 00 00 00 80 00 00 00 |
    | add qword [4 * rcx], 0x000000ff                    | 48 81 04 8d 00 00 00 00 ff 00 00 00 |
    | add qword [8 * rcx], 0x00000100                    | 48 81 04 cd 00 00 00 00 00 01 00 00 |
    | add qword [1 * r9], 0x00007fff                     | 4a 81 04 0d 00 00 00 00 ff 7f 00 00 |
    | add qword [2 * r9], 0x00008000                     | 4a 81 04 4d 00 00 00 00 00 80 00 00 |
    | add qword [4 * r9], 0x0000ffff                     | 4a 81 04 8d 00 00 00 00 ff ff 00 00 |
    | add qword [8 * r9], 0x00010000                     | 4a 81 04 cd 00 00 00 00 00 00 01 00 |
    | add qword [r13 + 8 * r12], 0x7fffffff              | 4b 81 44 e5 00 ff ff ff 7f          |
    | add qword [rsp + 4 * r15], 0x80000000              | 4a 81 04 bc 00 00 00 80             |
    | add qword [rax + 1 * rcx + 0x00], 0xffffffff       | 48 81 44 08 00 ff ff ff ff          |
    | add qword [rax + 1 * rcx - 0x00], 0x00000000       | 48 81 44 08 00 00 00 00 00          |
    | add qword [rax + 1 * rcx - 0x01], 0x0000007f       | 48 81 44 08 ff 7f 00 00 00          |
    | add qword [rax + 1 * rcx + 0x00000001], 0x00000080 | 48 81 84 08 01 00 00 00 80 00 00 00 |
    | add qword [rax + 1 * rcx - 0x00000001], 0x000000ff | 48 81 84 08 ff ff ff ff ff 00 00 00 |
    | add qword [rax + 1 * rcx + 0x7f], 0x00000100       | 48 81 44 08 7f 00 01 00 00          |
    | add qword [rax + 1 * rcx - 0x7f], 0x00007fff       | 48 81 44 08 81 ff 7f 00 00          |
    | add qword [rax + 1 * rcx + 0x80], 0x00008000       | 48 81 84 08 80 00 00 00 00 80 00 00 |
    | add qword [rax + 1 * rcx - 0x80], 0x0000ffff       | 48 81 44 08 80 ff ff 00 00          |
    | add qword [rax + 1 * rcx - 0x81], 0x00010000       | 48 81 84 08 7f ff ff ff 00 00 01 00 |
    | add qword [rax + 1 * rcx + 0xff], 0x7fffffff       | 48 81 84 08 ff 00 00 00 ff ff ff 7f |
    | add qword [rax + 1 * rcx - 0xff], 0x80000000       | 48 81 84 08 01 ff ff ff 00 00 00 80 |
    | add qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 48 81 84 08 ff ff ff 7f ff ff ff ff |
    | add qword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 48 81 84 08 01 00 00 80 00 00 00 00 |
    | add qword [r10 + 0x7f], 0x0000007f                 | 49 81 42 7f 7f 00 00 00             |
    | add qword [r10 + 0x80], 0x00000080                 | 49 81 82 80 00 00 00 80 00 00 00    |
    | add qword [r10 - 0x80], 0x000000ff                 | 49 81 42 80 ff 00 00 00             |
    | add qword [r10 - 0x81], 0x00000100                 | 49 81 82 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_add_addr64_imm32():
    encode(ADD_ADDR64_IMM32)


ADD_ADDR64_REG64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | add qword [rax], rcx                        | 48 01 08                |
    | add qword [rcx], rcx                        | 48 01 09                |
    | add qword [rdx], rcx                        | 48 01 0a                |
    | add qword [rbx], rcx                        | 48 01 0b                |
    | add qword [rsp], rcx                        | 48 01 0c 24             |
    | add qword [rbp], rcx                        | 48 01 4d 00             |
    | add qword [rsi], rcx                        | 48 01 0e                |
    | add qword [rdi], rcx                        | 48 01 0f                |
    | add qword [r8], rcx                         | 49 01 08                |
    | add qword [r9], rcx                         | 49 01 09                |
    | add qword [r10], rcx                        | 49 01 0a                |
    | add qword [r11], rcx                        | 49 01 0b                |
    | add qword [r12], rcx                        | 49 01 0c 24             |
    | add qword [r13], rcx                        | 49 01 4d 00             |
    | add qword [r14], rcx                        | 49 01 0e                |
    | add qword [r15], rcx                        | 49 01 0f                |
    | add qword [rax + 1 * rcx], rcx              | 48 01 0c 08             |
    | add qword [rcx + 1 * rcx], rcx              | 48 01 0c 09             |
    | add qword [rdx + 1 * rcx], rcx              | 48 01 0c 0a             |
    | add qword [rbx + 1 * rcx], rcx              | 48 01 0c 0b             |
    | add qword [rsp + 1 * rcx], rcx              | 48 01 0c 0c             |
    | add qword [rbp + 1 * rcx], rcx              | 48 01 4c 0d 00          |
    | add qword [rsi + 1 * rcx], rcx              | 48 01 0c 0e             |
    | add qword [rdi + 1 * rcx], rcx              | 48 01 0c 0f             |
    | add qword [r8 + 1 * rcx], rcx               | 49 01 0c 08             |
    | add qword [r9 + 1 * rcx], rcx               | 49 01 0c 09             |
    | add qword [r10 + 1 * rcx], rcx              | 49 01 0c 0a             |
    | add qword [r11 + 1 * rcx], rcx              | 49 01 0c 0b             |
    | add qword [r12 + 1 * rcx], rcx              | 49 01 0c 0c             |
    | add qword [r13 + 1 * rcx], rcx              | 49 01 4c 0d 00          |
    | add qword [r14 + 1 * rcx], rcx              | 49 01 0c 0e             |
    | add qword [r15 + 1 * rcx], rcx              | 49 01 0c 0f             |
    | add qword [rax + 1 * rax], rcx              | 48 01 0c 00             |
    | add qword [rax + 1 * rdx], rcx              | 48 01 0c 10             |
    | add qword [rax + 1 * rbx], rcx              | 48 01 0c 18             |
    | add qword [rax + 1 * rbp], rcx              | 48 01 0c 28             |
    | add qword [rax + 1 * rsi], rcx              | 48 01 0c 30             |
    | add qword [rax + 1 * rdi], rcx              | 48 01 0c 38             |
    | add qword [rax + 1 * r8], rcx               | 4a 01 0c 00             |
    | add qword [rax + 1 * r9], rcx               | 4a 01 0c 08             |
    | add qword [rax + 1 * r10], rcx              | 4a 01 0c 10             |
    | add qword [rax + 1 * r11], rcx              | 4a 01 0c 18             |
    | add qword [rax + 1 * r12], rcx              | 4a 01 0c 20             |
    | add qword [rax + 1 * r13], rcx              | 4a 01 0c 28             |
    | add qword [rax + 1 * r14], rcx              | 4a 01 0c 30             |
    | add qword [rax + 1 * r15], rcx              | 4a 01 0c 38             |
    | add qword [rax + 2 * rcx], rcx              | 48 01 0c 48             |
    | add qword [rax + 4 * rcx], rcx              | 48 01 0c 88             |
    | add qword [rax + 8 * rcx], rcx              | 48 01 0c c8             |
    | add qword [r8 + 1 * r9], rcx                | 4b 01 0c 08             |
    | add qword [r8 + 2 * r9], rcx                | 4b 01 0c 48             |
    | add qword [r8 + 4 * r9], rcx                | 4b 01 0c 88             |
    | add qword [r8 + 8 * r9], rcx                | 4b 01 0c c8             |
    | add qword [1 * rcx], rcx                    | 48 01 0c 0d 00 00 00 00 |
    | add qword [2 * rcx], rcx                    | 48 01 0c 4d 00 00 00 00 |
    | add qword [4 * rcx], rcx                    | 48 01 0c 8d 00 00 00 00 |
    | add qword [8 * rcx], rcx                    | 48 01 0c cd 00 00 00 00 |
    | add qword [1 * r9], rcx                     | 4a 01 0c 0d 00 00 00 00 |
    | add qword [2 * r9], rcx                     | 4a 01 0c 4d 00 00 00 00 |
    | add qword [4 * r9], rcx                     | 4a 01 0c 8d 00 00 00 00 |
    | add qword [8 * r9], rcx                     | 4a 01 0c cd 00 00 00 00 |
    | add qword [r13 + 8 * r12], rcx              | 4b 01 4c e5 00          |
    | add qword [rsp + 4 * r15], rcx              | 4a 01 0c bc             |
    | add qword [rax + 1 * rcx + 0x00], rcx       | 48 01 4c 08 00          |
    | add qword [rax + 1 * rcx - 0x00], rcx       | 48 01 4c 08 00          |
    | add qword [rax + 1 * rcx + 0x01], rcx       | 48 01 4c 08 01          |
    | add qword [rax + 1 * rcx - 0x01], rcx       | 48 01 4c 08 ff          |
    | add qword [rax + 1 * rcx + 0x00000001], rcx | 48 01 8c 08 01 00 00 00 |
    | add qword [rax + 1 * rcx - 0x00000001], rcx | 48 01 8c 08 ff ff ff ff |
    | add qword [rax + 1 * rcx + 0x7f], rcx       | 48 01 4c 08 7f          |
    | add qword [rax + 1 * rcx - 0x7f], rcx       | 48 01 4c 08 81          |
    | add qword [rax + 1 * rcx + 0x80], rcx       | 48 01 8c 08 80 00 00 00 |
    | add qword [rax + 1 * rcx - 0x80], rcx       | 48 01 4c 08 80          |
    | add qword [rax + 1 * rcx - 0x81], rcx       | 48 01 8c 08 7f ff ff ff |
    | add qword [rax + 1 * rcx + 0xff], rcx       | 48 01 8c 08 ff 00 00 00 |
    | add qword [rax + 1 * rcx - 0xff], rcx       | 48 01 8c 08 01 ff ff ff |
    | add qword [rax + 1 * rcx + 0x7fffffff], rcx | 48 01 8c 08 ff ff ff 7f |
    | add qword [rax + 1 * rcx - 0x7fffffff], rcx | 48 01 8c 08 01 00 00 80 |
    | add qword [rax + 1 * rcx - 0x80000000], rcx | 48 01 8c 08 00 00 00 80 |
    | add qword [r10 + 0x7f], rcx                 | 49 01 4a 7f             |
    | add qword [r10 + 0x80], rcx                 | 49 01 8a 80 00 00 00    |
    | add qword [r10 - 0x80], rcx                 | 49 01 4a 80             |
    | add qword [r10 - 0x81], rcx                 | 49 01 8a 7f ff ff ff    |
    | add qword [rax], rax                        | 48 01 00                |
    | add qword [rax], rdx                        | 48 01 10                |
    | add qword [rax], rbx                        | 48 01 18                |
    | add qword [rax], rsp                        | 48 01 20                |
    | add qword [rax], rbp                        | 48 01 28                |
    | add qword [rax], rsi                        | 48 01 30                |
    | add qword [rax], rdi                        | 48 01 38                |
    | add qword [rax], r8                         | 4c 01 00                |
    | add qword [rax], r9                         | 4c 01 08                |
    | add qword [rax], r10                        | 4c 01 10                |
    | add qword [rax], r11                        | 4c 01 18                |
    | add qword [rax], r12                        | 4c 01 20                |
    | add qword [rax], r13                        | 4c 01 28                |
    | add qword [rax], r14                        | 4c 01 30                |
    | add qword [rax], r15                        | 4c 01 38                |
    | add qword [rcx], rdx                        | 48 01 11                |
    | add qword [rdx], rbx                        | 48 01 1a                |
    | add qword [rbx], rsp                        | 48 01 23                |
    | add qword [rsp], rbp                        | 48 01 2c 24             |
    | add qword [rbp], rsi                        | 48 01 75 00             |
    | add qword [rsi], rdi                        | 48 01 3e                |
    | add qword [rdi], r8                         | 4c 01 07                |
    | add qword [r8], r9                          | 4d 01 08                |
    | add qword [r9], r10                         | 4d 01 11                |
    | add qword [r10], r11                        | 4d 01 1a                |
    | add qword [r11], r12                        | 4d 01 23                |
    | add qword [r12], r13                        | 4d 01 2c 24             |
    | add qword [r13], r14                        | 4d 01 75 00             |
    | add qword [r14], r15                        | 4d 01 3e                |
    | add qword [r15], rax                        | 49 01 07                |
    | add qword [rcx + 1 * rcx], rdx              | 48 01 14 09             |
    | add qword [rdx + 1 * rcx], rbx              | 48 01 1c 0a             |
    | add qword [rbx + 1 * rcx], rsp              | 48 01 24 0b             |
    | add qword [rsp + 1 * rcx], rbp              | 48 01 2c 0c             |
    | add qword [rbp + 1 * rcx], rsi              | 48 01 74 0d 00          |
    | add qword [rsi + 1 * rcx], rdi              | 48 01 3c 0e             |
    | add qword [rdi + 1 * rcx], r8               | 4c 01 04 0f             |
    | add qword [r8 + 1 * rcx], r9                | 4d 01 0c 08             |
    | add qword [r9 + 1 * rcx], r10               | 4d 01 14 09             |
    | add qword [r10 + 1 * rcx], r11              | 4d 01 1c 0a             |
    | add qword [r11 + 1 * rcx], r12              | 4d 01 24 0b             |
    | add qword [r12 + 1 * rcx], r13              | 4d 01 2c 0c             |
    | add qword [r13 + 1 * rcx], r14              | 4d 01 74 0d 00          |
    | add qword [r14 + 1 * rcx], r15              | 4d 01 3c 0e             |
    | add qword [r15 + 1 * rcx], rax              | 49 01 04 0f             |
    | add qword [rax + 1 * rdx], rdx              | 48 01 14 10             |
    | add qword [rax + 1 * rbx], rbx              | 48 01 1c 18             |
    | add qword [rax + 1 * rbp], rsp              | 48 01 24 28             |
    | add qword [rax + 1 * rsi], rbp              | 48 01 2c 30             |
    | add qword [rax + 1 * rdi], rsi              | 48 01 34 38             |
    | add qword [rax + 1 * r8], rdi               | 4a 01 3c 00             |
    | add qword [rax + 1 * r9], r8                | 4e 01 04 08             |
    | add qword [rax + 1 * r10], r9               | 4e 01 0c 10             |
    | add qword [rax + 1 * r11], r10              | 4e 01 14 18             |
    | add qword [rax + 1 * r12], r11              | 4e 01 1c 20             |
    | add qword [rax + 1 * r13], r12              | 4e 01 24 28             |
    | add qword [rax + 1 * r14], r13              | 4e 01 2c 30             |
    | add qword [rax + 1 * r15], r14              | 4e 01 34 38             |
    | add qword [rax + 2 * rcx], r15              | 4c 01 3c 48             |
    | add qword [rax + 4 * rcx], rax              | 48 01 04 88             |
    | add qword [r8 + 1 * r9], rdx                | 4b 01 14 08             |
    | add qword [r8 + 2 * r9], rbx                | 4b 01 1c 48             |
    | add qword [r8 + 4 * r9], rsp                | 4b 01 24 88             |
    | add qword [r8 + 8 * r9], rbp                | 4b 01 2c c8             |
    | add qword [1 * rcx], rsi                    | 48 01 34 0d 00 00 00 00 |
    | add qword [2 * rcx], rdi                    | 48 01 3c 4d 00 00 00 00 |
    | add qword [4 * rcx], r8                     | 4c 01 04 8d 00 00 00 00 |
    | add qword [8 * rcx], r9                     | 4c 01 0c cd 00 00 00 00 |
    | add qword [1 * r9], r10                     | 4e 01 14 0d 00 00 00 00 |
    | add qword [2 * r9], r11                     | 4e 01 1c 4d 00 00 00 00 |
    | add qword [4 * r9], r12                     | 4e 01 24 8d 00 00 00 00 |
    | add qword [8 * r9], r13                     | 4e 01 2c cd 00 00 00 00 |
    | add qword [r13 + 8 * r12], r14              | 4f 01 74 e5 00          |
    | add qword [rsp + 4 * r15], r15              | 4e 01 3c bc             |
    | add qword [rax + 1 * rcx + 0x00], rax       | 48 01 44 08 00          |
    | add qword [rax + 1 * rcx + 0x01], rdx       | 48 01 54 08 01          |
    | add qword [rax + 1 * rcx - 0x01], rbx       | 48 01 5c 08 ff          |
    | add qword [rax + 1 * rcx + 0x00000001], rsp | 48 01 a4 08 01 00 00 00 |
    | add qword [rax + 1 * rcx - 0x00000001], rbp | 48 01 ac 08 ff ff ff ff |
    | add qword [rax + 1 * rcx + 0x7f], rsi       | 48 01 74 08 7f          |
    | add qword [rax + 1 * rcx - 0x7f], rdi       | 48 01 7c 08 81          |
    | add qword [rax + 1 * rcx + 0x80], r8        | 4c 01 84 08 80 00 00 00 |
    | add qword [rax + 1 * rcx - 0x80], r9        | 4c 01 4c 08 80          |
    | add qword [rax + 1 * rcx - 0x81], r10       | 4c 01 94 08 7f ff ff ff |
    | add qword [rax + 1 * rcx + 0xff], r11       | 4c 01 9c 08 ff 00 00 00 |
    | add qword [rax + 1 * rcx - 0xff], r12       | 4c 01 a4 08 01 ff ff ff |
    | add qword [rax + 1 * rcx + 0x7fffffff], r13 | 4c 01 ac 08 ff ff ff 7f |
    | add qword [rax + 1 * rcx - 0x7fffffff], r14 | 4c 01 b4 08 01 00 00 80 |
    | add qword [rax + 1 * rcx - 0x80000000], r15 | 4c 01 bc 08 00 00 00 80 |
    | add qword [r10 + 0x7f], rax                 | 49 01 42 7f             |
    | add qword [r10 - 0x80], rdx                 | 49 01 52 80             |
    | add qword [r10 - 0x81], rbx                 | 49 01 9a 7f ff ff ff    |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_add_addr64_reg64():
    encode(ADD_ADDR64_REG64)


ADD_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | add dword [rax], 0x01                        | 83 00 01                   |
    | add dword [rcx], 0x01                        | 83 01 01                   |
    | add dword [rdx], 0x01                        | 83 02 01                   |
    | add dword [rbx], 0x01                        | 83 03 01                   |
    | add dword [rsp], 0x01                        | 83 04 24 01                |
    | add dword [rbp], 0x01                        | 83 45 00 01                |
    | add dword [rsi], 0x01                        | 83 06 01                   |
    | add dword [rdi], 0x01                        | 83 07 01                   |
    | add dword [r8], 0x01                         | 41 83 00 01                |
    | add dword [r9], 0x01                         | 41 83 01 01                |
    | add dword [r10], 0x01                        | 41 83 02 01                |
    | add dword [r11], 0x01                        | 41 83 03 01                |
    | add dword [r12], 0x01                        | 41 83 04 24 01             |
    | add dword [r13], 0x01                        | 41 83 45 00 01             |
    | add dword [r14], 0x01                        | 41 83 06 01                |
    | add dword [r15], 0x01                        | 41 83 07 01                |
    | add dword [rax + 1 * rcx], 0x01              | 83 04 08 01                |
    | add dword [rcx + 1 * rcx], 0x01              | 83 04 09 01                |
    | add dword [rdx + 1 * rcx], 0x01              | 83 04 0a 01                |
    | add dword [rbx + 1 * rcx], 0x01              | 83 04 0b 01                |
    | add dword [rsp + 1 * rcx], 0x01              | 83 04 0c 01                |
    | add dword [rbp + 1 * rcx], 0x01              | 83 44 0d 00 01             |
    | add dword [rsi + 1 * rcx], 0x01              | 83 04 0e 01                |
    | add dword [rdi + 1 * rcx], 0x01              | 83 04 0f 01                |
    | add dword [r8 + 1 * rcx], 0x01               | 41 83 04 08 01             |
    | add dword [r9 + 1 * rcx], 0x01               | 41 83 04 09 01             |
    | add dword [r10 + 1 * rcx], 0x01              | 41 83 04 0a 01             |
    | add dword [r11 + 1 * rcx], 0x01              | 41 83 04 0b 01             |
    | add dword [r12 + 1 * rcx], 0x01              | 41 83 04 0c 01             |
    | add dword [r13 + 1 * rcx], 0x01              | 41 83 44 0d 00 01          |
    | add dword [r14 + 1 * rcx], 0x01              | 41 83 04 0e 01             |
    | add dword [r15 + 1 * rcx], 0x01              | 41 83 04 0f 01             |
    | add dword [rax + 1 * rax], 0x01              | 83 04 00 01                |
    | add dword [rax + 1 * rdx], 0x01              | 83 04 10 01                |
    | add dword [rax + 1 * rbx], 0x01              | 83 04 18 01                |
    | add dword [rax + 1 * rbp], 0x01              | 83 04 28 01                |
    | add dword [rax + 1 * rsi], 0x01              | 83 04 30 01                |
    | add dword [rax + 1 * rdi], 0x01              | 83 04 38 01                |
    | add dword [rax + 1 * r8], 0x01               | 42 83 04 00 01             |
    | add dword [rax + 1 * r9], 0x01               | 42 83 04 08 01             |
    | add dword [rax + 1 * r10], 0x01              | 42 83 04 10 01             |
    | add dword [rax + 1 * r11], 0x01              | 42 83 04 18 01             |
    | add dword [rax + 1 * r12], 0x01              | 42 83 04 20 01             |
    | add dword [rax + 1 * r13], 0x01              | 42 83 04 28 01             |
    | add dword [rax + 1 * r14], 0x01              | 42 83 04 30 01             |
    | add dword [rax + 1 * r15], 0x01              | 42 83 04 38 01             |
    | add dword [rax + 2 * rcx], 0x01              | 83 04 48 01                |
    | add dword [rax + 4 * rcx], 0x01              | 83 04 88 01                |
    | add dword [rax + 8 * rcx], 0x01              | 83 04 c8 01                |
    | add dword [r8 + 1 * r9], 0x01                | 43 83 04 08 01             |
    | add dword [r8 + 2 * r9], 0x01                | 43 83 04 48 01             |
    | add dword [r8 + 4 * r9], 0x01                | 43 83 04 88 01             |
    | add dword [r8 + 8 * r9], 0x01                | 43 83 04 c8 01             |
    | add dword [1 * rcx], 0x01                    | 83 04 0d 00 00 00 00 01    |
    | add dword [2 * rcx], 0x01                    | 83 04 4d 00 00 00 00 01    |
    | add dword [4 * rcx], 0x01                    | 83 04 8d 00 00 00 00 01    |
    | add dword [8 * rcx], 0x01                    | 83 04 cd 00 00 00 00 01    |
    | add dword [1 * r9], 0x01                     | 42 83 04 0d 00 00 00 00 01 |
    | add dword [2 * r9], 0x01                     | 42 83 04 4d 00 00 00 00 01 |
    | add dword [4 * r9], 0x01                     | 42 83 04 8d 00 00 00 00 01 |
    | add dword [8 * r9], 0x01                     | 42 83 04 cd 00 00 00 00 01 |
    | add dword [r13 + 8 * r12], 0x01              | 43 83 44 e5 00 01          |
    | add dword [rsp + 4 * r15], 0x01              | 42 83 04 bc 01             |
    | add dword [rax + 1 * rcx + 0x00], 0x01       | 83 44 08 00 01             |
    | add dword [rax + 1 * rcx - 0x00], 0x01       | 83 44 08 00 01             |
    | add dword [rax + 1 * rcx + 0x01], 0x01       | 83 44 08 01 01             |
    | add dword [rax + 1 * rcx - 0x01], 0x01       | 83 44 08 ff 01             |
    | add dword [rax + 1 * rcx + 0x00000001], 0x01 | 83 84 08 01 00 00 00 01    |
    | add dword [rax + 1 * rcx - 0x00000001], 0x01 | 83 84 08 ff ff ff ff 01    |
    | add dword [rax + 1 * rcx + 0x7f], 0x01       | 83 44 08 7f 01             |
    | add dword [rax + 1 * rcx - 0x7f], 0x01       | 83 44 08 81 01             |
    | add dword [rax + 1 * rcx + 0x80], 0x01       | 83 84 08 80 00 00 00 01    |
    | add dword [rax + 1 * rcx - 0x80], 0x01       | 83 44 08 80 01             |
    | add dword [rax + 1 * rcx - 0x81], 0x01       | 83 84 08 7f ff ff ff 01    |
    | add dword [rax + 1 * rcx + 0xff], 0x01       | 83 84 08 ff 00 00 00 01    |
    | add dword [rax + 1 * rcx - 0xff], 0x01       | 83 84 08 01 ff ff ff 01    |
    | add dword [rax + 1 * rcx + 0x7fffffff], 0x01 | 83 84 08 ff ff ff 7f 01    |
    | add dword [rax + 1 * rcx - 0x7fffffff], 0x01 | 83 84 08 01 00 00 80 01    |
    | add dword [rax + 1 * rcx - 0x80000000], 0x01 | 83 84 08 00 00 00 80 01    |
    | add dword [r10 + 0x7f], 0x01                 | 41 83 42 7f 01             |
    | add dword [r10 + 0x80], 0x01                 | 41 83 82 80 00 00 00 01    |
    | add dword [r10 - 0x80], 0x01                 | 41 83 42 80 01             |
    | add dword [r10 - 0x81], 0x01                 | 41 83 82 7f ff ff ff 01    |
    | add dword [rax], 0x00                        | 83 00 00                   |
    | add dword [rax], 0x7f                        | 83 00 7f                   |
    | add dword [rax], 0x80                        | 83 00 80                   |
    | add dword [rax], 0xff                        | 83 00 ff                   |
    | add dword [rcx], 0x7f                        | 83 01 7f                   |
    | add dword [rdx], 0x80                        | 83 02 80                   |
    | add dword [rbx], 0xff                        | 83 03 ff                   |
    | add dword [rsp], 0x00                        | 83 04 24 00                |
    | add dword [rsi], 0x7f                        | 83 06 7f                   |
    | add dword [rdi], 0x80                        | 83 07 80                   |
    | add dword [r8], 0xff                         | 41 83 00 ff                |
    | add dword [r9], 0x00                         | 41 83 01 00                |
    | add dword [r11], 0x7f                        | 41 83 03 7f                |
    | add dword [r12], 0x80                        | 41 83 04 24 80             |
    | add dword [r13], 0xff                        | 41 83 45 00 ff             |
    | add dword [r14], 0x00                        | 41 83 06 00                |
    | add dword [rax + 1 * rcx], 0x7f              | 83 04 08 7f                |
    | add dword [rcx + 1 * rcx], 0x80              | 83 04 09 80                |
    | add dword [rdx + 1 * rcx], 0xff              | 83 04 0a ff                |
    | add dword [rbx + 1 * rcx], 0x00              | 83 04 0b 00                |
    | add dword [rbp + 1 * rcx], 0x7f              | 83 44 0d 00 7f             |
    | add dword [rsi + 1 * rcx], 0x80              | 83 04 0e 80                |
    | add dword [rdi + 1 * rcx], 0xff              | 83 04 0f ff                |
    | add dword [r8 + 1 * rcx], 0x00               | 41 83 04 08 00             |
    | add dword [r10 + 1 * rcx], 0x7f              | 41 83 04 0a 7f             |
    | add dword [r11 + 1 * rcx], 0x80              | 41 83 04 0b 80             |
    | add dword [r12 + 1 * rcx], 0xff              | 41 83 04 0c ff             |
    | add dword [r13 + 1 * rcx], 0x00              | 41 83 44 0d 00 00          |
    | add dword [r15 + 1 * rcx], 0x7f              | 41 83 04 0f 7f             |
    | add dword [rax + 1 * rax], 0x80              | 83 04 00 80                |
    | add dword [rax + 1 * rdx], 0xff              | 83 04 10 ff                |
    | add dword [rax + 1 * rbx], 0x00              | 83 04 18 00                |
    | add dword [rax + 1 * rsi], 0x7f              | 83 04 30 7f                |
    | add dword [rax + 1 * rdi], 0x80              | 83 04 38 80                |
    | add dword [rax + 1 * r8], 0xff               | 42 83 04 00 ff             |
    | add dword [rax + 1 * r9], 0x00               | 42 83 04 08 00             |
    | add dword [rax + 1 * r11], 0x7f              | 42 83 04 18 7f             |
    | add dword [rax + 1 * r12], 0x80              | 42 83 04 20 80             |
    | add dword [rax + 1 * r13], 0xff              | 42 83 04 28 ff             |
    | add dword [rax + 1 * r14], 0x00              | 42 83 04 30 00             |
    | add dword [rax + 2 * rcx], 0x7f              | 83 04 48 7f                |
    | add dword [rax + 4 * rcx], 0x80              | 83 04 88 80                |
    | add dword [rax + 8 * rcx], 0xff              | 83 04 c8 ff                |
    | add dword [r8 + 1 * r9], 0x00                | 43 83 04 08 00             |
    | add dword [r8 + 4 * r9], 0x7f                | 43 83 04 88 7f             |
    | add dword [r8 + 8 * r9], 0x80                | 43 83 04 c8 80             |
    | add dword [1 * rcx], 0xff                    | 83 04 0d 00 00 00 00 ff    |
    | add dword [2 * rcx], 0x00                    | 83 04 4d 00 00 00 00 00    |
    | add dword [8 * rcx], 0x7f                    | 83 04 cd 00 00 00 00 7f    |
    | add dword [1 * r9], 0x80                     | 42 83 04 0d 00 00 00 00 80 |
    | add dword [2 * r9], 0xff                     | 42 83 04 4d 00 00 00 00 ff |
    | add dword [4 * r9], 0x00                     | 42 83 04 8d 00 00 00 00 00 |
    | add dword [r13 + 8 * r12], 0x7f              | 43 83 44 e5 00 7f          |
    | add dword [rsp + 4 * r15], 0x80              | 42 83 04 bc 80             |
    | add dword [rax + 1 * rcx + 0x00], 0xff       | 83 44 08 00 ff             |
    | add dword [rax + 1 * rcx - 0x00], 0x00       | 83 44 08 00 00             |
    | add dword [rax + 1 * rcx - 0x01], 0x7f       | 83 44 08 ff 7f             |
    | add dword [rax + 1 * rcx + 0x00000001], 0x80 | 83 84 08 01 00 00 00 80    |
    | add dword [rax + 1 * rcx - 0x00000001], 0xff | 83 84 08 ff ff ff ff ff    |
    | add dword [rax + 1 * rcx + 0x7f], 0x00       | 83 44 08 7f 00             |
    | add dword [rax + 1 * rcx + 0x80], 0x7f       | 83 84 08 80 00 00 00 7f    |
    | add dword [rax + 1 * rcx - 0x80], 0x80       | 83 44 08 80 80             |
    | add dword [rax + 1 * rcx - 0x81], 0xff       | 83 84 08 7f ff ff ff ff    |
    | add dword [rax + 1 * rcx + 0xff], 0x00       | 83 84 08 ff 00 00 00 00    |
    | add dword [rax + 1 * rcx + 0x7fffffff], 0x7f | 83 84 08 ff ff ff 7f 7f    |
    | add dword [rax + 1 * rcx - 0x7fffffff], 0x80 | 83 84 08 01 00 00 80 80    |
    | add dword [rax + 1 * rcx - 0x80000000], 0xff | 83 84 08 00 00 00 80 ff    |
    | add dword [r10 + 0x7f], 0x00                 | 41 83 42 7f 00             |
    | add dword [r10 - 0x80], 0x7f                 | 41 83 42 80 7f             |
    | add dword [r10 - 0x81], 0x80                 | 41 83 82 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_add_addr32_imm8():
    encode(ADD_ADDR32_IMM8)


ADD_ADDR32_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | add dword [rax], 0x00000001                        | 81 00 01 00 00 00                   |
    | add dword [rcx], 0x00000001                        | 81 01 01 00 00 00                   |
    | add dword [rdx], 0x00000001                        | 81 02 01 00 00 00                   |
    | add dword [rbx], 0x00000001                        | 81 03 01 00 00 00                   |
    | add dword [rsp], 0x00000001                        | 81 04 24 01 00 00 00                |
    | add dword [rbp], 0x00000001                        | 81 45 00 01 00 00 00                |
    | add dword [rsi], 0x00000001                        | 81 06 01 00 00 00                   |
    | add dword [rdi], 0x00000001                        | 81 07 01 00 00 00                   |
    | add dword [r8], 0x00000001                         | 41 81 00 01 00 00 00                |
    | add dword [r9], 0x00000001                         | 41 81 01 01 00 00 00                |
    | add dword [r10], 0x00000001                        | 41 81 02 01 00 00 00                |
    | add dword [r11], 0x00000001                        | 41 81 03 01 00 00 00                |
    | add dword [r12], 0x00000001                        | 41 81 04 24 01 00 00 00             |
    | add dword [r13], 0x00000001                        | 41 81 45 00 01 00 00 00             |
    | add dword [r14], 0x00000001                        | 41 81 06 01 00 00 00                |
    | add dword [r15], 0x00000001                        | 41 81 07 01 00 00 00                |
    | add dword [rax + 1 * rcx], 0x00000001              | 81 04 08 01 00 00 00                |
    | add dword [rcx + 1 * rcx], 0x00000001              | 81 04 09 01 00 00 00                |
    | add dword [rdx + 1 * rcx], 0x00000001              | 81 04 0a 01 00 00 00                |
    | add dword [rbx + 1 * rcx], 0x00000001              | 81 04 0b 01 00 00 00                |
    | add dword [rsp + 1 * rcx], 0x00000001              | 81 04 0c 01 00 00 00                |
    | add dword [rbp + 1 * rcx], 0x00000001              | 81 44 0d 00 01 00 00 00             |
    | add dword [rsi + 1 * rcx], 0x00000001              | 81 04 0e 01 00 00 00                |
    | add dword [rdi + 1 * rcx], 0x00000001              | 81 04 0f 01 00 00 00                |
    | add dword [r8 + 1 * rcx], 0x00000001               | 41 81 04 08 01 00 00 00             |
    | add dword [r9 + 1 * rcx], 0x00000001               | 41 81 04 09 01 00 00 00             |
    | add dword [r10 + 1 * rcx], 0x00000001              | 41 81 04 0a 01 00 00 00             |
    | add dword [r11 + 1 * rcx], 0x00000001              | 41 81 04 0b 01 00 00 00             |
    | add dword [r12 + 1 * rcx], 0x00000001              | 41 81 04 0c 01 00 00 00             |
    | add dword [r13 + 1 * rcx], 0x00000001              | 41 81 44 0d 00 01 00 00 00          |
    | add dword [r14 + 1 * rcx], 0x00000001              | 41 81 04 0e 01 00 00 00             |
    | add dword [r15 + 1 * rcx], 0x00000001              | 41 81 04 0f 01 00 00 00             |
    | add dword [rax + 1 * rax], 0x00000001              | 81 04 00 01 00 00 00                |
    | add dword [rax + 1 * rdx], 0x00000001              | 81 04 10 01 00 00 00                |
    | add dword [rax + 1 * rbx], 0x00000001              | 81 04 18 01 00 00 00                |
    | add dword [rax + 1 * rbp], 0x00000001              | 81 04 28 01 00 00 00                |
    | add dword [rax + 1 * rsi], 0x00000001              | 81 04 30 01 00 00 00                |
    | add dword [rax + 1 * rdi], 0x00000001              | 81 04 38 01 00 00 00                |
    | add dword [rax + 1 * r8], 0x00000001               | 42 81 04 00 01 00 00 00             |
    | add dword [rax + 1 * r9], 0x00000001               | 42 81 04 08 01 00 00 00             |
    | add dword [rax + 1 * r10], 0x00000001              | 42 81 04 10 01 00 00 00             |
    | add dword [rax + 1 * r11], 0x00000001              | 42 81 04 18 01 00 00 00             |
    | add dword [rax + 1 * r12], 0x00000001              | 42 81 04 20 01 00 00 00             |
    | add dword [rax + 1 * r13], 0x00000001              | 42 81 04 28 01 00 00 00             |
    | add dword [rax + 1 * r14], 0x00000001              | 42 81 04 30 01 00 00 00             |
    | add dword [rax + 1 * r15], 0x00000001              | 42 81 04 38 01 00 00 00             |
    | add dword [rax + 2 * rcx], 0x00000001              | 81 04 48 01 00 00 00                |
    | add dword [rax + 4 * rcx], 0x00000001              | 81 04 88 01 00 00 00                |
    | add dword [rax + 8 * rcx], 0x00000001              | 81 04 c8 01 00 00 00                |
    | add dword [r8 + 1 * r9], 0x00000001                | 43 81 04 08 01 00 00 00             |
    | add dword [r8 + 2 * r9], 0x00000001                | 43 81 04 48 01 00 00 00             |
    | add dword [r8 + 4 * r9], 0x00000001                | 43 81 04 88 01 00 00 00             |
    | add dword [r8 + 8 * r9], 0x00000001                | 43 81 04 c8 01 00 00 00             |
    | add dword [1 * rcx], 0x00000001                    | 81 04 0d 00 00 00 00 01 00 00 00    |
    | add dword [2 * rcx], 0x00000001                    | 81 04 4d 00 00 00 00 01 00 00 00    |
    | add dword [4 * rcx], 0x00000001                    | 81 04 8d 00 00 00 00 01 00 00 00    |
    | add dword [8 * rcx], 0x00000001                    | 81 04 cd 00 00 00 00 01 00 00 00    |
    | add dword [1 * r9], 0x00000001                     | 42 81 04 0d 00 00 00 00 01 00 00 00 |
    | add dword [2 * r9], 0x00000001                     | 42 81 04 4d 00 00 00 00 01 00 00 00 |
    | add dword [4 * r9], 0x00000001                     | 42 81 04 8d 00 00 00 00 01 00 00 00 |
    | add dword [8 * r9], 0x00000001                     | 42 81 04 cd 00 00 00 00 01 00 00 00 |
    | add dword [r13 + 8 * r12], 0x00000001              | 43 81 44 e5 00 01 00 00 00          |
    | add dword [rsp + 4 * r15], 0x00000001              | 42 81 04 bc 01 00 00 00             |
    | add dword [rax + 1 * rcx + 0x00], 0x00000001       | 81 44 08 00 01 00 00 00             |
    | add dword [rax + 1 * rcx - 0x00], 0x00000001       | 81 44 08 00 01 00 00 00             |
    | add dword [rax + 1 * rcx + 0x01], 0x00000001       | 81 44 08 01 01 00 00 00             |
    | add dword [rax + 1 * rcx - 0x01], 0x00000001       | 81 44 08 ff 01 00 00 00             |
    | add dword [rax + 1 * rcx + 0x00000001], 0x00000001 | 81 84 08 01 00 00 00 01 00 00 00    |
    | add dword [rax + 1 * rcx - 0x00000001], 0x00000001 | 81 84 08 ff ff ff ff 01 00 00 00    |
    | add dword [rax + 1 * rcx + 0x7f], 0x00000001       | 81 44 08 7f 01 00 00 00             |
    | add dword [rax + 1 * rcx - 0x7f], 0x00000001       | 81 44 08 81 01 00 00 00             |
    | add dword [rax + 1 * rcx + 0x80], 0x00000001       | 81 84 08 80 00 00 00 01 00 00 00    |
    | add dword [rax + 1 * rcx - 0x80], 0x00000001       | 81 44 08 80 01 00 00 00             |
    | add dword [rax + 1 * rcx - 0x81], 0x00000001       | 81 84 08 7f ff ff ff 01 00 00 00    |
    | add dword [rax + 1 * rcx + 0xff], 0x00000001       | 81 84 08 ff 00 00 00 01 00 00 00    |
    | add dword [rax + 1 * rcx - 0xff], 0x00000001       | 81 84 08 01 ff ff ff 01 00 00 00    |
    | add dword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 81 84 08 ff ff ff 7f 01 00 00 00    |
    | add dword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 81 84 08 01 00 00 80 01 00 00 00    |
    | add dword [rax + 1 * rcx - 0x80000000], 0x00000001 | 81 84 08 00 00 00 80 01 00 00 00    |
    | add dword [r10 + 0x7f], 0x00000001                 | 41 81 42 7f 01 00 00 00             |
    | add dword [r10 + 0x80], 0x00000001                 | 41 81 82 80 00 00 00 01 00 00 00    |
    | add dword [r10 - 0x80], 0x00000001                 | 41 81 42 80 01 00 00 00             |
    | add dword [r10 - 0x81], 0x00000001                 | 41 81 82 7f ff ff ff 01 00 00 00    |
    | add dword [rax], 0x00000000                        | 81 00 00 00 00 00                   |
    | add dword [rax], 0x0000007f                        | 81 00 7f 00 00 00                   |
    | add dword [rax], 0x00000080                        | 81 00 80 00 00 00                   |
    | add dword [rax], 0x000000ff                        | 81 00 ff 00 00 00                   |
    | add dword [rax], 0x00000100                        | 81 00 00 01 00 00                   |
    | add dword [rax], 0x00007fff                        | 81 00 ff 7f 00 00                   |
    | add dword [rax], 0x00008000                        | 81 00 00 80 00 00                   |
    | add dword [rax], 0x0000ffff                        | 81 00 ff ff 00 00                   |
    | add dword [rax], 0x00010000                        | 81 00 00 00 01 00                   |
    | add dword [rax], 0x7fffffff                        | 81 00 ff ff ff 7f                   |
    | add dword [rax], 0x80000000                        | 81 00 00 00 00 80                   |
    | add dword [rax], 0xffffffff                        | 81 00 ff ff ff ff                   |
    | add dword [rcx], 0x0000007f                        | 81 01 7f 00 00 00                   |
    | add dword [rdx], 0x00000080                        | 81 02 80 00 00 00                   |
    | add dword [rbx], 0x000000ff                        | 81 03 ff 00 00 00                   |
    | add dword [rsp], 0x00000100                        | 81 04 24 00 01 00 00                |
    | add dword [rbp], 0x00007fff                        | 81 45 00 ff 7f 00 00                |
    | add dword [rsi], 0x00008000                        | 81 06 00 80 00 00                   |
    | add dword [rdi], 0x0000ffff                        | 81 07 ff ff 00 00                   |
    | add dword [r8], 0x00010000                         | 41 81 00 00 00 01 00                |
    | add dword [r9], 0x7fffffff                         | 41 81 01 ff ff ff 7f                |
    | add dword [r10], 0x80000000                        | 41 81 02 00 00 00 80                |
    | add dword [r11], 0xffffffff                        | 41 81 03 ff ff ff ff                |
    | add dword [r12], 0x00000000                        | 41 81 04 24 00 00 00 00             |
    | add dword [r14], 0x0000007f                        | 41 81 06 7f 00 00 00                |
    | add dword [r15], 0x00000080                        | 41 81 07 80 00 00 00                |
    | add dword [rax + 1 * rcx], 0x000000ff              | 81 04 08 ff 00 00 00                |
    | add dword [rcx + 1 * rcx], 0x00000100              | 81 04 09 00 01 00 00                |
    | add dword [rdx + 1 * rcx], 0x00007fff              | 81 04 0a ff 7f 00 00                |
    | add dword [rbx + 1 * rcx], 0x00008000              | 81 04 0b 00 80 00 00                |
    | add dword [rsp + 1 * rcx], 0x0000ffff              | 81 04 0c ff ff 00 00                |
    | add dword [rbp + 1 * rcx], 0x00010000              | 81 44 0d 00 00 00 01 00             |
    | add dword [rsi + 1 * rcx], 0x7fffffff              | 81 04 0e ff ff ff 7f                |
    | add dword [rdi + 1 * rcx], 0x80000000              | 81 04 0f 00 00 00 80                |
    | add dword [r8 + 1 * rcx], 0xffffffff               | 41 81 04 08 ff ff ff ff             |
    | add dword [r9 + 1 * rcx], 0x00000000               | 41 81 04 09 00 00 00 00             |
    | add dword [r11 + 1 * rcx], 0x0000007f              | 41 81 04 0b 7f 00 00 00             |
    | add dword [r12 + 1 * rcx], 0x00000080              | 41 81 04 0c 80 00 00 00             |
    | add dword [r13 + 1 * rcx], 0x000000ff              | 41 81 44 0d 00 ff 00 00 00          |
    | add dword [r14 + 1 * rcx], 0x00000100              | 41 81 04 0e 00 01 00 00             |
    | add dword [r15 + 1 * rcx], 0x00007fff              | 41 81 04 0f ff 7f 00 00             |
    | add dword [rax + 1 * rax], 0x00008000              | 81 04 00 00 80 00 00                |
    | add dword [rax + 1 * rdx], 0x0000ffff              | 81 04 10 ff ff 00 00                |
    | add dword [rax + 1 * rbx], 0x00010000              | 81 04 18 00 00 01 00                |
    | add dword [rax + 1 * rbp], 0x7fffffff              | 81 04 28 ff ff ff 7f                |
    | add dword [rax + 1 * rsi], 0x80000000              | 81 04 30 00 00 00 80                |
    | add dword [rax + 1 * rdi], 0xffffffff              | 81 04 38 ff ff ff ff                |
    | add dword [rax + 1 * r8], 0x00000000               | 42 81 04 00 00 00 00 00             |
    | add dword [rax + 1 * r10], 0x0000007f              | 42 81 04 10 7f 00 00 00             |
    | add dword [rax + 1 * r11], 0x00000080              | 42 81 04 18 80 00 00 00             |
    | add dword [rax + 1 * r12], 0x000000ff              | 42 81 04 20 ff 00 00 00             |
    | add dword [rax + 1 * r13], 0x00000100              | 42 81 04 28 00 01 00 00             |
    | add dword [rax + 1 * r14], 0x00007fff              | 42 81 04 30 ff 7f 00 00             |
    | add dword [rax + 1 * r15], 0x00008000              | 42 81 04 38 00 80 00 00             |
    | add dword [rax + 2 * rcx], 0x0000ffff              | 81 04 48 ff ff 00 00                |
    | add dword [rax + 4 * rcx], 0x00010000              | 81 04 88 00 00 01 00                |
    | add dword [rax + 8 * rcx], 0x7fffffff              | 81 04 c8 ff ff ff 7f                |
    | add dword [r8 + 1 * r9], 0x80000000                | 43 81 04 08 00 00 00 80             |
    | add dword [r8 + 2 * r9], 0xffffffff                | 43 81 04 48 ff ff ff ff             |
    | add dword [r8 + 4 * r9], 0x00000000                | 43 81 04 88 00 00 00 00             |
    | add dword [1 * rcx], 0x0000007f                    | 81 04 0d 00 00 00 00 7f 00 00 00    |
    | add dword [2 * rcx], 0x00000080                    | 81 04 4d 00 00 00 00 80 00 00 00    |
    | add dword [4 * rcx], 0x000000ff                    | 81 04 8d 00 00 00 00 ff 00 00 00    |
    | add dword [8 * rcx], 0x00000100                    | 81 04 cd 00 00 00 00 00 01 00 00    |
    | add dword [1 * r9], 0x00007fff                     | 42 81 04 0d 00 00 00 00 ff 7f 00 00 |
    | add dword [2 * r9], 0x00008000                     | 42 81 04 4d 00 00 00 00 00 80 00 00 |
    | add dword [4 * r9], 0x0000ffff                     | 42 81 04 8d 00 00 00 00 ff ff 00 00 |
    | add dword [8 * r9], 0x00010000                     | 42 81 04 cd 00 00 00 00 00 00 01 00 |
    | add dword [r13 + 8 * r12], 0x7fffffff              | 43 81 44 e5 00 ff ff ff 7f          |
    | add dword [rsp + 4 * r15], 0x80000000              | 42 81 04 bc 00 00 00 80             |
    | add dword [rax + 1 * rcx + 0x00], 0xffffffff       | 81 44 08 00 ff ff ff ff             |
    | add dword [rax + 1 * rcx - 0x00], 0x00000000       | 81 44 08 00 00 00 00 00             |
    | add dword [rax + 1 * rcx - 0x01], 0x0000007f       | 81 44 08 ff 7f 00 00 00             |
    | add dword [rax + 1 * rcx + 0x00000001], 0x00000080 | 81 84 08 01 00 00 00 80 00 00 00    |
    | add dword [rax + 1 * rcx - 0x00000001], 0x000000ff | 81 84 08 ff ff ff ff ff 00 00 00    |
    | add dword [rax + 1 * rcx + 0x7f], 0x00000100       | 81 44 08 7f 00 01 00 00             |
    | add dword [rax + 1 * rcx - 0x7f], 0x00007fff       | 81 44 08 81 ff 7f 00 00             |
    | add dword [rax + 1 * rcx + 0x80], 0x00008000       | 81 84 08 80 00 00 00 00 80 00 00    |
    | add dword [rax + 1 * rcx - 0x80], 0x0000ffff       | 81 44 08 80 ff ff 00 00             |
    | add dword [rax + 1 * rcx - 0x81], 0x00010000       | 81 84 08 7f ff ff ff 00 00 01 00    |
    | add dword [rax + 1 * rcx + 0xff], 0x7fffffff       | 81 84 08 ff 00 00 00 ff ff ff 7f    |
    | add dword [rax + 1 * rcx - 0xff], 0x80000000       | 81 84 08 01 ff ff ff 00 00 00 80    |
    | add dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 81 84 08 ff ff ff 7f ff ff ff ff    |
    | add dword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 81 84 08 01 00 00 80 00 00 00 00    |
    | add dword [r10 + 0x7f], 0x0000007f                 | 41 81 42 7f 7f 00 00 00             |
    | add dword [r10 + 0x80], 0x00000080                 | 41 81 82 80 00 00 00 80 00 00 00    |
    | add dword [r10 - 0x80], 0x000000ff                 | 41 81 42 80 ff 00 00 00             |
    | add dword [r10 - 0x81], 0x00000100                 | 41 81 82 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_add_addr32_imm32():
    encode(ADD_ADDR32_IMM32)


ADD_ADDR32_REG32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | add dword [rax], ecx                         | 01 08                   |
    | add dword [rcx], ecx                         | 01 09                   |
    | add dword [rdx], ecx                         | 01 0a                   |
    | add dword [rbx], ecx                         | 01 0b                   |
    | add dword [rsp], ecx                         | 01 0c 24                |
    | add dword [rbp], ecx                         | 01 4d 00                |
    | add dword [rsi], ecx                         | 01 0e                   |
    | add dword [rdi], ecx                         | 01 0f                   |
    | add dword [r8], ecx                          | 41 01 08                |
    | add dword [r9], ecx                          | 41 01 09                |
    | add dword [r10], ecx                         | 41 01 0a                |
    | add dword [r11], ecx                         | 41 01 0b                |
    | add dword [r12], ecx                         | 41 01 0c 24             |
    | add dword [r13], ecx                         | 41 01 4d 00             |
    | add dword [r14], ecx                         | 41 01 0e                |
    | add dword [r15], ecx                         | 41 01 0f                |
    | add dword [rax + 1 * rcx], ecx               | 01 0c 08                |
    | add dword [rcx + 1 * rcx], ecx               | 01 0c 09                |
    | add dword [rdx + 1 * rcx], ecx               | 01 0c 0a                |
    | add dword [rbx + 1 * rcx], ecx               | 01 0c 0b                |
    | add dword [rsp + 1 * rcx], ecx               | 01 0c 0c                |
    | add dword [rbp + 1 * rcx], ecx               | 01 4c 0d 00             |
    | add dword [rsi + 1 * rcx], ecx               | 01 0c 0e                |
    | add dword [rdi + 1 * rcx], ecx               | 01 0c 0f                |
    | add dword [r8 + 1 * rcx], ecx                | 41 01 0c 08             |
    | add dword [r9 + 1 * rcx], ecx                | 41 01 0c 09             |
    | add dword [r10 + 1 * rcx], ecx               | 41 01 0c 0a             |
    | add dword [r11 + 1 * rcx], ecx               | 41 01 0c 0b             |
    | add dword [r12 + 1 * rcx], ecx               | 41 01 0c 0c             |
    | add dword [r13 + 1 * rcx], ecx               | 41 01 4c 0d 00          |
    | add dword [r14 + 1 * rcx], ecx               | 41 01 0c 0e             |
    | add dword [r15 + 1 * rcx], ecx               | 41 01 0c 0f             |
    | add dword [rax + 1 * rax], ecx               | 01 0c 00                |
    | add dword [rax + 1 * rdx], ecx               | 01 0c 10                |
    | add dword [rax + 1 * rbx], ecx               | 01 0c 18                |
    | add dword [rax + 1 * rbp], ecx               | 01 0c 28                |
    | add dword [rax + 1 * rsi], ecx               | 01 0c 30                |
    | add dword [rax + 1 * rdi], ecx               | 01 0c 38                |
    | add dword [rax + 1 * r8], ecx                | 42 01 0c 00             |
    | add dword [rax + 1 * r9], ecx                | 42 01 0c 08             |
    | add dword [rax + 1 * r10], ecx               | 42 01 0c 10             |
    | add dword [rax + 1 * r11], ecx               | 42 01 0c 18             |
    | add dword [rax + 1 * r12], ecx               | 42 01 0c 20             |
    | add dword [rax + 1 * r13], ecx               | 42 01 0c 28             |
    | add dword [rax + 1 * r14], ecx               | 42 01 0c 30             |
    | add dword [rax + 1 * r15], ecx               | 42 01 0c 38             |
    | add dword [rax + 2 * rcx], ecx               | 01 0c 48                |
    | add dword [rax + 4 * rcx], ecx               | 01 0c 88                |
    | add dword [rax + 8 * rcx], ecx               | 01 0c c8                |
    | add dword [r8 + 1 * r9], ecx                 | 43 01 0c 08             |
    | add dword [r8 + 2 * r9], ecx                 | 43 01 0c 48             |
    | add dword [r8 + 4 * r9], ecx                 | 43 01 0c 88             |
    | add dword [r8 + 8 * r9], ecx                 | 43 01 0c c8             |
    | add dword [1 * rcx], ecx                     | 01 0c 0d 00 00 00 00    |
    | add dword [2 * rcx], ecx                     | 01 0c 4d 00 00 00 00    |
    | add dword [4 * rcx], ecx                     | 01 0c 8d 00 00 00 00    |
    | add dword [8 * rcx], ecx                     | 01 0c cd 00 00 00 00    |
    | add dword [1 * r9], ecx                      | 42 01 0c 0d 00 00 00 00 |
    | add dword [2 * r9], ecx                      | 42 01 0c 4d 00 00 00 00 |
    | add dword [4 * r9], ecx                      | 42 01 0c 8d 00 00 00 00 |
    | add dword [8 * r9], ecx                      | 42 01 0c cd 00 00 00 00 |
    | add dword [r13 + 8 * r12], ecx               | 43 01 4c e5 00          |
    | add dword [rsp + 4 * r15], ecx               | 42 01 0c bc             |
    | add dword [rax + 1 * rcx + 0x00], ecx        | 01 4c 08 00             |
    | add dword [rax + 1 * rcx - 0x00], ecx        | 01 4c 08 00             |
    | add dword [rax + 1 * rcx + 0x01], ecx        | 01 4c 08 01             |
    | add dword [rax + 1 * rcx - 0x01], ecx        | 01 4c 08 ff             |
    | add dword [rax + 1 * rcx + 0x00000001], ecx  | 01 8c 08 01 00 00 00    |
    | add dword [rax + 1 * rcx - 0x00000001], ecx  | 01 8c 08 ff ff ff ff    |
    | add dword [rax + 1 * rcx + 0x7f], ecx        | 01 4c 08 7f             |
    | add dword [rax + 1 * rcx - 0x7f], ecx        | 01 4c 08 81             |
    | add dword [rax + 1 * rcx + 0x80], ecx        | 01 8c 08 80 00 00 00    |
    | add dword [rax + 1 * rcx - 0x80], ecx        | 01 4c 08 80             |
    | add dword [rax + 1 * rcx - 0x81], ecx        | 01 8c 08 7f ff ff ff    |
    | add dword [rax + 1 * rcx + 0xff], ecx        | 01 8c 08 ff 00 00 00    |
    | add dword [rax + 1 * rcx - 0xff], ecx        | 01 8c 08 01 ff ff ff    |
    | add dword [rax + 1 * rcx + 0x7fffffff], ecx  | 01 8c 08 ff ff ff 7f    |
    | add dword [rax + 1 * rcx - 0x7fffffff], ecx  | 01 8c 08 01 00 00 80    |
    | add dword [rax + 1 * rcx - 0x80000000], ecx  | 01 8c 08 00 00 00 80    |
    | add dword [r10 + 0x7f], ecx                  | 41 01 4a 7f             |
    | add dword [r10 + 0x80], ecx                  | 41 01 8a 80 00 00 00    |
    | add dword [r10 - 0x80], ecx                  | 41 01 4a 80             |
    | add dword [r10 - 0x81], ecx                  | 41 01 8a 7f ff ff ff    |
    | add dword [rax], eax                         | 01 00                   |
    | add dword [rax], edx                         | 01 10                   |
    | add dword [rax], ebx                         | 01 18                   |
    | add dword [rax], esp                         | 01 20                   |
    | add dword [rax], ebp                         | 01 28                   |
    | add dword [rax], esi                         | 01 30                   |
    | add dword [rax], edi                         | 01 38                   |
    | add dword [rax], r8d                         | 44 01 00                |
    | add dword [rax], r9d                         | 44 01 08                |
    | add dword [rax], r10d                        | 44 01 10                |
    | add dword [rax], r11d                        | 44 01 18                |
    | add dword [rax], r12d                        | 44 01 20                |
    | add dword [rax], r13d                        | 44 01 28                |
    | add dword [rax], r14d                        | 44 01 30                |
    | add dword [rax], r15d                        | 44 01 38                |
    | add dword [rcx], edx                         | 01 11                   |
    | add dword [rdx], ebx                         | 01 1a                   |
    | add dword [rbx], esp                         | 01 23                   |
    | add dword [rsp], ebp                         | 01 2c 24                |
    | add dword [rbp], esi                         | 01 75 00                |
    | add dword [rsi], edi                         | 01 3e                   |
    | add dword [rdi], r8d                         | 44 01 07                |
    | add dword [r8], r9d                          | 45 01 08                |
    | add dword [r9], r10d                         | 45 01 11                |
    | add dword [r10], r11d                        | 45 01 1a                |
    | add dword [r11], r12d                        | 45 01 23                |
    | add dword [r12], r13d                        | 45 01 2c 24             |
    | add dword [r13], r14d                        | 45 01 75 00             |
    | add dword [r14], r15d                        | 45 01 3e                |
    | add dword [r15], eax                         | 41 01 07                |
    | add dword [rcx + 1 * rcx], edx               | 01 14 09                |
    | add dword [rdx + 1 * rcx], ebx               | 01 1c 0a                |
    | add dword [rbx + 1 * rcx], esp               | 01 24 0b                |
    | add dword [rsp + 1 * rcx], ebp               | 01 2c 0c                |
    | add dword [rbp + 1 * rcx], esi               | 01 74 0d 00             |
    | add dword [rsi + 1 * rcx], edi               | 01 3c 0e                |
    | add dword [rdi + 1 * rcx], r8d               | 44 01 04 0f             |
    | add dword [r8 + 1 * rcx], r9d                | 45 01 0c 08             |
    | add dword [r9 + 1 * rcx], r10d               | 45 01 14 09             |
    | add dword [r10 + 1 * rcx], r11d              | 45 01 1c 0a             |
    | add dword [r11 + 1 * rcx], r12d              | 45 01 24 0b             |
    | add dword [r12 + 1 * rcx], r13d              | 45 01 2c 0c             |
    | add dword [r13 + 1 * rcx], r14d              | 45 01 74 0d 00          |
    | add dword [r14 + 1 * rcx], r15d              | 45 01 3c 0e             |
    | add dword [r15 + 1 * rcx], eax               | 41 01 04 0f             |
    | add dword [rax + 1 * rdx], edx               | 01 14 10                |
    | add dword [rax + 1 * rbx], ebx               | 01 1c 18                |
    | add dword [rax + 1 * rbp], esp               | 01 24 28                |
    | add dword [rax + 1 * rsi], ebp               | 01 2c 30                |
    | add dword [rax + 1 * rdi], esi               | 01 34 38                |
    | add dword [rax + 1 * r8], edi                | 42 01 3c 00             |
    | add dword [rax + 1 * r9], r8d                | 46 01 04 08             |
    | add dword [rax + 1 * r10], r9d               | 46 01 0c 10             |
    | add dword [rax + 1 * r11], r10d              | 46 01 14 18             |
    | add dword [rax + 1 * r12], r11d              | 46 01 1c 20             |
    | add dword [rax + 1 * r13], r12d              | 46 01 24 28             |
    | add dword [rax + 1 * r14], r13d              | 46 01 2c 30             |
    | add dword [rax + 1 * r15], r14d              | 46 01 34 38             |
    | add dword [rax + 2 * rcx], r15d              | 44 01 3c 48             |
    | add dword [rax + 4 * rcx], eax               | 01 04 88                |
    | add dword [r8 + 1 * r9], edx                 | 43 01 14 08             |
    | add dword [r8 + 2 * r9], ebx                 | 43 01 1c 48             |
    | add dword [r8 + 4 * r9], esp                 | 43 01 24 88             |
    | add dword [r8 + 8 * r9], ebp                 | 43 01 2c c8             |
    | add dword [1 * rcx], esi                     | 01 34 0d 00 00 00 00    |
    | add dword [2 * rcx], edi                     | 01 3c 4d 00 00 00 00    |
    | add dword [4 * rcx], r8d                     | 44 01 04 8d 00 00 00 00 |
    | add dword [8 * rcx], r9d                     | 44 01 0c cd 00 00 00 00 |
    | add dword [1 * r9], r10d                     | 46 01 14 0d 00 00 00 00 |
    | add dword [2 * r9], r11d                     | 46 01 1c 4d 00 00 00 00 |
    | add dword [4 * r9], r12d                     | 46 01 24 8d 00 00 00 00 |
    | add dword [8 * r9], r13d                     | 46 01 2c cd 00 00 00 00 |
    | add dword [r13 + 8 * r12], r14d              | 47 01 74 e5 00          |
    | add dword [rsp + 4 * r15], r15d              | 46 01 3c bc             |
    | add dword [rax + 1 * rcx + 0x00], eax        | 01 44 08 00             |
    | add dword [rax + 1 * rcx + 0x01], edx        | 01 54 08 01             |
    | add dword [rax + 1 * rcx - 0x01], ebx        | 01 5c 08 ff             |
    | add dword [rax + 1 * rcx + 0x00000001], esp  | 01 a4 08 01 00 00 00    |
    | add dword [rax + 1 * rcx - 0x00000001], ebp  | 01 ac 08 ff ff ff ff    |
    | add dword [rax + 1 * rcx + 0x7f], esi        | 01 74 08 7f             |
    | add dword [rax + 1 * rcx - 0x7f], edi        | 01 7c 08 81             |
    | add dword [rax + 1 * rcx + 0x80], r8d        | 44 01 84 08 80 00 00 00 |
    | add dword [rax + 1 * rcx - 0x80], r9d        | 44 01 4c 08 80          |
    | add dword [rax + 1 * rcx - 0x81], r10d       | 44 01 94 08 7f ff ff ff |
    | add dword [rax + 1 * rcx + 0xff], r11d       | 44 01 9c 08 ff 00 00 00 |
    | add dword [rax + 1 * rcx - 0xff], r12d       | 44 01 a4 08 01 ff ff ff |
    | add dword [rax + 1 * rcx + 0x7fffffff], r13d | 44 01 ac 08 ff ff ff 7f |
    | add dword [rax + 1 * rcx - 0x7fffffff], r14d | 44 01 b4 08 01 00 00 80 |
    | add dword [rax + 1 * rcx - 0x80000000], r15d | 44 01 bc 08 00 00 00 80 |
    | add dword [r10 + 0x7f], eax                  | 41 01 42 7f             |
    | add dword [r10 - 0x80], edx                  | 41 01 52 80             |
    | add dword [r10 - 0x81], ebx                  | 41 01 9a 7f ff ff ff    |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_add_addr32_reg32():
    encode(ADD_ADDR32_REG32)


ADD_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | add word [rax], 0x01                        | 66 83 00 01                   |
    | add word [rcx], 0x01                        | 66 83 01 01                   |
    | add word [rdx], 0x01                        | 66 83 02 01                   |
    | add word [rbx], 0x01                        | 66 83 03 01                   |
    | add word [rsp], 0x01                        | 66 83 04 24 01                |
    | add word [rbp], 0x01                        | 66 83 45 00 01                |
    | add word [rsi], 0x01                        | 66 83 06 01                   |
    | add word [rdi], 0x01                        | 66 83 07 01                   |
    | add word [r8], 0x01                         | 66 41 83 00 01                |
    | add word [r9], 0x01                         | 66 41 83 01 01                |
    | add word [r10], 0x01                        | 66 41 83 02 01                |
    | add word [r11], 0x01                        | 66 41 83 03 01                |
    | add word [r12], 0x01                        | 66 41 83 04 24 01             |
    | add word [r13], 0x01                        | 66 41 83 45 00 01             |
    | add word [r14], 0x01                        | 66 41 83 06 01                |
    | add word [r15], 0x01                        | 66 41 83 07 01                |
    | add word [rax + 1 * rcx], 0x01              | 66 83 04 08 01                |
    | add word [rcx + 1 * rcx], 0x01              | 66 83 04 09 01                |
    | add word [rdx + 1 * rcx], 0x01              | 66 83 04 0a 01                |
    | add word [rbx + 1 * rcx], 0x01              | 66 83 04 0b 01                |
    | add word [rsp + 1 * rcx], 0x01              | 66 83 04 0c 01                |
    | add word [rbp + 1 * rcx], 0x01              | 66 83 44 0d 00 01             |
    | add word [rsi + 1 * rcx], 0x01              | 66 83 04 0e 01                |
    | add word [rdi + 1 * rcx], 0x01              | 66 83 04 0f 01                |
    | add word [r8 + 1 * rcx], 0x01               | 66 41 83 04 08 01             |
    | add word [r9 + 1 * rcx], 0x01               | 66 41 83 04 09 01             |
    | add word [r10 + 1 * rcx], 0x01              | 66 41 83 04 0a 01             |
    | add word [r11 + 1 * rcx], 0x01              | 66 41 83 04 0b 01             |
    | add word [r12 + 1 * rcx], 0x01              | 66 41 83 04 0c 01             |
    | add word [r13 + 1 * rcx], 0x01              | 66 41 83 44 0d 00 01          |
    | add word [r14 + 1 * rcx], 0x01              | 66 41 83 04 0e 01             |
    | add word [r15 + 1 * rcx], 0x01              | 66 41 83 04 0f 01             |
    | add word [rax + 1 * rax], 0x01              | 66 83 04 00 01                |
    | add word [rax + 1 * rdx], 0x01              | 66 83 04 10 01                |
    | add word [rax + 1 * rbx], 0x01              | 66 83 04 18 01                |
    | add word [rax + 1 * rbp], 0x01              | 66 83 04 28 01                |
    | add word [rax + 1 * rsi], 0x01              | 66 83 04 30 01                |
    | add word [rax + 1 * rdi], 0x01              | 66 83 04 38 01                |
    | add word [rax + 1 * r8], 0x01               | 66 42 83 04 00 01             |
    | add word [rax + 1 * r9], 0x01               | 66 42 83 04 08 01             |
    | add word [rax + 1 * r10], 0x01              | 66 42 83 04 10 01             |
    | add word [rax + 1 * r11], 0x01              | 66 42 83 04 18 01             |
    | add word [rax + 1 * r12], 0x01              | 66 42 83 04 20 01             |
    | add word [rax + 1 * r13], 0x01              | 66 42 83 04 28 01             |
    | add word [rax + 1 * r14], 0x01              | 66 42 83 04 30 01             |
    | add word [rax + 1 * r15], 0x01              | 66 42 83 04 38 01             |
    | add word [rax + 2 * rcx], 0x01              | 66 83 04 48 01                |
    | add word [rax + 4 * rcx], 0x01              | 66 83 04 88 01                |
    | add word [rax + 8 * rcx], 0x01              | 66 83 04 c8 01                |
    | add word [r8 + 1 * r9], 0x01                | 66 43 83 04 08 01             |
    | add word [r8 + 2 * r9], 0x01                | 66 43 83 04 48 01             |
    | add word [r8 + 4 * r9], 0x01                | 66 43 83 04 88 01             |
    | add word [r8 + 8 * r9], 0x01                | 66 43 83 04 c8 01             |
    | add word [1 * rcx], 0x01                    | 66 83 04 0d 00 00 00 00 01    |
    | add word [2 * rcx], 0x01                    | 66 83 04 4d 00 00 00 00 01    |
    | add word [4 * rcx], 0x01                    | 66 83 04 8d 00 00 00 00 01    |
    | add word [8 * rcx], 0x01                    | 66 83 04 cd 00 00 00 00 01    |
    | add word [1 * r9], 0x01                     | 66 42 83 04 0d 00 00 00 00 01 |
    | add word [2 * r9], 0x01                     | 66 42 83 04 4d 00 00 00 00 01 |
    | add word [4 * r9], 0x01                     | 66 42 83 04 8d 00 00 00 00 01 |
    | add word [8 * r9], 0x01                     | 66 42 83 04 cd 00 00 00 00 01 |
    | add word [r13 + 8 * r12], 0x01              | 66 43 83 44 e5 00 01          |
    | add word [rsp + 4 * r15], 0x01              | 66 42 83 04 bc 01             |
    | add word [rax + 1 * rcx + 0x00], 0x01       | 66 83 44 08 00 01             |
    | add word [rax + 1 * rcx - 0x00], 0x01       | 66 83 44 08 00 01             |
    | add word [rax + 1 * rcx + 0x01], 0x01       | 66 83 44 08 01 01             |
    | add word [rax + 1 * rcx - 0x01], 0x01       | 66 83 44 08 ff 01             |
    | add word [rax + 1 * rcx + 0x00000001], 0x01 | 66 83 84 08 01 00 00 00 01    |
    | add word [rax + 1 * rcx - 0x00000001], 0x01 | 66 83 84 08 ff ff ff ff 01    |
    | add word [rax + 1 * rcx + 0x7f], 0x01       | 66 83 44 08 7f 01             |
    | add word [rax + 1 * rcx - 0x7f], 0x01       | 66 83 44 08 81 01             |
    | add word [rax + 1 * rcx + 0x80], 0x01       | 66 83 84 08 80 00 00 00 01    |
    | add word [rax + 1 * rcx - 0x80], 0x01       | 66 83 44 08 80 01             |
    | add word [rax + 1 * rcx - 0x81], 0x01       | 66 83 84 08 7f ff ff ff 01    |
    | add word [rax + 1 * rcx + 0xff], 0x01       | 66 83 84 08 ff 00 00 00 01    |
    | add word [rax + 1 * rcx - 0xff], 0x01       | 66 83 84 08 01 ff ff ff 01    |
    | add word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 83 84 08 ff ff ff 7f 01    |
    | add word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 83 84 08 01 00 00 80 01    |
    | add word [rax + 1 * rcx - 0x80000000], 0x01 | 66 83 84 08 00 00 00 80 01    |
    | add word [r10 + 0x7f], 0x01                 | 66 41 83 42 7f 01             |
    | add word [r10 + 0x80], 0x01                 | 66 41 83 82 80 00 00 00 01    |
    | add word [r10 - 0x80], 0x01                 | 66 41 83 42 80 01             |
    | add word [r10 - 0x81], 0x01                 | 66 41 83 82 7f ff ff ff 01    |
    | add word [rax], 0x00                        | 66 83 00 00                   |
    | add word [rax], 0x7f                        | 66 83 00 7f                   |
    | add word [rax], 0x80                        | 66 83 00 80                   |
    | add word [rax], 0xff                        | 66 83 00 ff                   |
    | add word [rcx], 0x7f                        | 66 83 01 7f                   |
    | add word [rdx], 0x80                        | 66 83 02 80                   |
    | add word [rbx], 0xff                        | 66 83 03 ff                   |
    | add word [rsp], 0x00                        | 66 83 04 24 00                |
    | add word [rsi], 0x7f                        | 66 83 06 7f                   |
    | add word [rdi], 0x80                        | 66 83 07 80                   |
    | add word [r8], 0xff                         | 66 41 83 00 ff                |
    | add word [r9], 0x00                         | 66 41 83 01 00                |
    | add word [r11], 0x7f                        | 66 41 83 03 7f                |
    | add word [r12], 0x80                        | 66 41 83 04 24 80             |
    | add word [r13], 0xff                        | 66 41 83 45 00 ff             |
    | add word [r14], 0x00                        | 66 41 83 06 00                |
    | add word [rax + 1 * rcx], 0x7f              | 66 83 04 08 7f                |
    | add word [rcx + 1 * rcx], 0x80              | 66 83 04 09 80                |
    | add word [rdx + 1 * rcx], 0xff              | 66 83 04 0a ff                |
    | add word [rbx + 1 * rcx], 0x00              | 66 83 04 0b 00                |
    | add word [rbp + 1 * rcx], 0x7f              | 66 83 44 0d 00 7f             |
    | add word [rsi + 1 * rcx], 0x80              | 66 83 04 0e 80                |
    | add word [rdi + 1 * rcx], 0xff              | 66 83 04 0f ff                |
    | add word [r8 + 1 * rcx], 0x00               | 66 41 83 04 08 00             |
    | add word [r10 + 1 * rcx], 0x7f              | 66 41 83 04 0a 7f             |
    | add word [r11 + 1 * rcx], 0x80              | 66 41 83 04 0b 80             |
    | add word [r12 + 1 * rcx], 0xff              | 66 41 83 04 0c ff             |
    | add word [r13 + 1 * rcx], 0x00              | 66 41 83 44 0d 00 00          |
    | add word [r15 + 1 * rcx], 0x7f              | 66 41 83 04 0f 7f             |
    | add word [rax + 1 * rax], 0x80              | 66 83 04 00 80                |
    | add word [rax + 1 * rdx], 0xff              | 66 83 04 10 ff                |
    | add word [rax + 1 * rbx], 0x00              | 66 83 04 18 00                |
    | add word [rax + 1 * rsi], 0x7f              | 66 83 04 30 7f                |
    | add word [rax + 1 * rdi], 0x80              | 66 83 04 38 80                |
    | add word [rax + 1 * r8], 0xff               | 66 42 83 04 00 ff             |
    | add word [rax + 1 * r9], 0x00               | 66 42 83 04 08 00             |
    | add word [rax + 1 * r11], 0x7f              | 66 42 83 04 18 7f             |
    | add word [rax + 1 * r12], 0x80              | 66 42 83 04 20 80             |
    | add word [rax + 1 * r13], 0xff              | 66 42 83 04 28 ff             |
    | add word [rax + 1 * r14], 0x00              | 66 42 83 04 30 00             |
    | add word [rax + 2 * rcx], 0x7f              | 66 83 04 48 7f                |
    | add word [rax + 4 * rcx], 0x80              | 66 83 04 88 80                |
    | add word [rax + 8 * rcx], 0xff              | 66 83 04 c8 ff                |
    | add word [r8 + 1 * r9], 0x00                | 66 43 83 04 08 00             |
    | add word [r8 + 4 * r9], 0x7f                | 66 43 83 04 88 7f             |
    | add word [r8 + 8 * r9], 0x80                | 66 43 83 04 c8 80             |
    | add word [1 * rcx], 0xff                    | 66 83 04 0d 00 00 00 00 ff    |
    | add word [2 * rcx], 0x00                    | 66 83 04 4d 00 00 00 00 00    |
    | add word [8 * rcx], 0x7f                    | 66 83 04 cd 00 00 00 00 7f    |
    | add word [1 * r9], 0x80                     | 66 42 83 04 0d 00 00 00 00 80 |
    | add word [2 * r9], 0xff                     | 66 42 83 04 4d 00 00 00 00 ff |
    | add word [4 * r9], 0x00                     | 66 42 83 04 8d 00 00 00 00 00 |
    | add word [r13 + 8 * r12], 0x7f              | 66 43 83 44 e5 00 7f          |
    | add word [rsp + 4 * r15], 0x80              | 66 42 83 04 bc 80             |
    | add word [rax + 1 * rcx + 0x00], 0xff       | 66 83 44 08 00 ff             |
    | add word [rax + 1 * rcx - 0x00], 0x00       | 66 83 44 08 00 00             |
    | add word [rax + 1 * rcx - 0x01], 0x7f       | 66 83 44 08 ff 7f             |
    | add word [rax + 1 * rcx + 0x00000001], 0x80 | 66 83 84 08 01 00 00 00 80    |
    | add word [rax + 1 * rcx - 0x00000001], 0xff | 66 83 84 08 ff ff ff ff ff    |
    | add word [rax + 1 * rcx + 0x7f], 0x00       | 66 83 44 08 7f 00             |
    | add word [rax + 1 * rcx + 0x80], 0x7f       | 66 83 84 08 80 00 00 00 7f    |
    | add word [rax + 1 * rcx - 0x80], 0x80       | 66 83 44 08 80 80             |
    | add word [rax + 1 * rcx - 0x81], 0xff       | 66 83 84 08 7f ff ff ff ff    |
    | add word [rax + 1 * rcx + 0xff], 0x00       | 66 83 84 08 ff 00 00 00 00    |
    | add word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 83 84 08 ff ff ff 7f 7f    |
    | add word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 83 84 08 01 00 00 80 80    |
    | add word [rax + 1 * rcx - 0x80000000], 0xff | 66 83 84 08 00 00 00 80 ff    |
    | add word [r10 + 0x7f], 0x00                 | 66 41 83 42 7f 00             |
    | add word [r10 - 0x80], 0x7f                 | 66 41 83 42 80 7f             |
    | add word [r10 - 0x81], 0x80                 | 66 41 83 82 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_add_addr16_imm8():
    encode(ADD_ADDR16_IMM8)


ADD_ADDR16_IMM16 = """
    | --------------------------------------------- | -------------------------------- |
    | instruction                                   | encoding                         |
    | --------------------------------------------- | -------------------------------- |
    | add word [rax], 0x0001                        | 66 81 00 01 00                   |
    | add word [rcx], 0x0001                        | 66 81 01 01 00                   |
    | add word [rdx], 0x0001                        | 66 81 02 01 00                   |
    | add word [rbx], 0x0001                        | 66 81 03 01 00                   |
    | add word [rsp], 0x0001                        | 66 81 04 24 01 00                |
    | add word [rbp], 0x0001                        | 66 81 45 00 01 00                |
    | add word [rsi], 0x0001                        | 66 81 06 01 00                   |
    | add word [rdi], 0x0001                        | 66 81 07 01 00                   |
    | add word [r8], 0x0001                         | 66 41 81 00 01 00                |
    | add word [r9], 0x0001                         | 66 41 81 01 01 00                |
    | add word [r10], 0x0001                        | 66 41 81 02 01 00                |
    | add word [r11], 0x0001                        | 66 41 81 03 01 00                |
    | add word [r12], 0x0001                        | 66 41 81 04 24 01 00             |
    | add word [r13], 0x0001                        | 66 41 81 45 00 01 00             |
    | add word [r14], 0x0001                        | 66 41 81 06 01 00                |
    | add word [r15], 0x0001                        | 66 41 81 07 01 00                |
    | add word [rax + 1 * rcx], 0x0001              | 66 81 04 08 01 00                |
    | add word [rcx + 1 * rcx], 0x0001              | 66 81 04 09 01 00                |
    | add word [rdx + 1 * rcx], 0x0001              | 66 81 04 0a 01 00                |
    | add word [rbx + 1 * rcx], 0x0001              | 66 81 04 0b 01 00                |
    | add word [rsp + 1 * rcx], 0x0001              | 66 81 04 0c 01 00                |
    | add word [rbp + 1 * rcx], 0x0001              | 66 81 44 0d 00 01 00             |
    | add word [rsi + 1 * rcx], 0x0001              | 66 81 04 0e 01 00                |
    | add word [rdi + 1 * rcx], 0x0001              | 66 81 04 0f 01 00                |
    | add word [r8 + 1 * rcx], 0x0001               | 66 41 81 04 08 01 00             |
    | add word [r9 + 1 * rcx], 0x0001               | 66 41 81 04 09 01 00             |
    | add word [r10 + 1 * rcx], 0x0001              | 66 41 81 04 0a 01 00             |
    | add word [r11 + 1 * rcx], 0x0001              | 66 41 81 04 0b 01 00             |
    | add word [r12 + 1 * rcx], 0x0001              | 66 41 81 04 0c 01 00             |
    | add word [r13 + 1 * rcx], 0x0001              | 66 41 81 44 0d 00 01 00          |
    | add word [r14 + 1 * rcx], 0x0001              | 66 41 81 04 0e 01 00             |
    | add word [r15 + 1 * rcx], 0x0001              | 66 41 81 04 0f 01 00             |
    | add word [rax + 1 * rax], 0x0001              | 66 81 04 00 01 00                |
    | add word [rax + 1 * rdx], 0x0001              | 66 81 04 10 01 00                |
    | add word [rax + 1 * rbx], 0x0001              | 66 81 04 18 01 00                |
    | add word [rax + 1 * rbp], 0x0001              | 66 81 04 28 01 00                |
    | add word [rax + 1 * rsi], 0x0001              | 66 81 04 30 01 00                |
    | add word [rax + 1 * rdi], 0x0001              | 66 81 04 38 01 00                |
    | add word [rax + 1 * r8], 0x0001               | 66 42 81 04 00 01 00             |
    | add word [rax + 1 * r9], 0x0001               | 66 42 81 04 08 01 00             |
    | add word [rax + 1 * r10], 0x0001              | 66 42 81 04 10 01 00             |
    | add word [rax + 1 * r11], 0x0001              | 66 42 81 04 18 01 00             |
    | add word [rax + 1 * r12], 0x0001              | 66 42 81 04 20 01 00             |
    | add word [rax + 1 * r13], 0x0001              | 66 42 81 04 28 01 00             |
    | add word [rax + 1 * r14], 0x0001              | 66 42 81 04 30 01 00             |
    | add word [rax + 1 * r15], 0x0001              | 66 42 81 04 38 01 00             |
    | add word [rax + 2 * rcx], 0x0001              | 66 81 04 48 01 00                |
    | add word [rax + 4 * rcx], 0x0001              | 66 81 04 88 01 00                |
    | add word [rax + 8 * rcx], 0x0001              | 66 81 04 c8 01 00                |
    | add word [r8 + 1 * r9], 0x0001                | 66 43 81 04 08 01 00             |
    | add word [r8 + 2 * r9], 0x0001                | 66 43 81 04 48 01 00             |
    | add word [r8 + 4 * r9], 0x0001                | 66 43 81 04 88 01 00             |
    | add word [r8 + 8 * r9], 0x0001                | 66 43 81 04 c8 01 00             |
    | add word [1 * rcx], 0x0001                    | 66 81 04 0d 00 00 00 00 01 00    |
    | add word [2 * rcx], 0x0001                    | 66 81 04 4d 00 00 00 00 01 00    |
    | add word [4 * rcx], 0x0001                    | 66 81 04 8d 00 00 00 00 01 00    |
    | add word [8 * rcx], 0x0001                    | 66 81 04 cd 00 00 00 00 01 00    |
    | add word [1 * r9], 0x0001                     | 66 42 81 04 0d 00 00 00 00 01 00 |
    | add word [2 * r9], 0x0001                     | 66 42 81 04 4d 00 00 00 00 01 00 |
    | add word [4 * r9], 0x0001                     | 66 42 81 04 8d 00 00 00 00 01 00 |
    | add word [8 * r9], 0x0001                     | 66 42 81 04 cd 00 00 00 00 01 00 |
    | add word [r13 + 8 * r12], 0x0001              | 66 43 81 44 e5 00 01 00          |
    | add word [rsp + 4 * r15], 0x0001              | 66 42 81 04 bc 01 00             |
    | add word [rax + 1 * rcx + 0x00], 0x0001       | 66 81 44 08 00 01 00             |
    | add word [rax + 1 * rcx - 0x00], 0x0001       | 66 81 44 08 00 01 00             |
    | add word [rax + 1 * rcx + 0x01], 0x0001       | 66 81 44 08 01 01 00             |
    | add word [rax + 1 * rcx - 0x01], 0x0001       | 66 81 44 08 ff 01 00             |
    | add word [rax + 1 * rcx + 0x00000001], 0x0001 | 66 81 84 08 01 00 00 00 01 00    |
    | add word [rax + 1 * rcx - 0x00000001], 0x0001 | 66 81 84 08 ff ff ff ff 01 00    |
    | add word [rax + 1 * rcx + 0x7f], 0x0001       | 66 81 44 08 7f 01 00             |
    | add word [rax + 1 * rcx - 0x7f], 0x0001       | 66 81 44 08 81 01 00             |
    | add word [rax + 1 * rcx + 0x80], 0x0001       | 66 81 84 08 80 00 00 00 01 00    |
    | add word [rax + 1 * rcx - 0x80], 0x0001       | 66 81 44 08 80 01 00             |
    | add word [rax + 1 * rcx - 0x81], 0x0001       | 66 81 84 08 7f ff ff ff 01 00    |
    | add word [rax + 1 * rcx + 0xff], 0x0001       | 66 81 84 08 ff 00 00 00 01 00    |
    | add word [rax + 1 * rcx - 0xff], 0x0001       | 66 81 84 08 01 ff ff ff 01 00    |
    | add word [rax + 1 * rcx + 0x7fffffff], 0x0001 | 66 81 84 08 ff ff ff 7f 01 00    |
    | add word [rax + 1 * rcx - 0x7fffffff], 0x0001 | 66 81 84 08 01 00 00 80 01 00    |
    | add word [rax + 1 * rcx - 0x80000000], 0x0001 | 66 81 84 08 00 00 00 80 01 00    |
    | add word [r10 + 0x7f], 0x0001                 | 66 41 81 42 7f 01 00             |
    | add word [r10 + 0x80], 0x0001                 | 66 41 81 82 80 00 00 00 01 00    |
    | add word [r10 - 0x80], 0x0001                 | 66 41 81 42 80 01 00             |
    | add word [r10 - 0x81], 0x0001                 | 66 41 81 82 7f ff ff ff 01 00    |
    | add word [rax], 0x0000                        | 66 81 00 00 00                   |
    | add word [rax], 0x007f                        | 66 81 00 7f 00                   |
    | add word [rax], 0x0080                        | 66 81 00 80 00                   |
    | add word [rax], 0x00ff                        | 66 81 00 ff 00                   |
    | add word [rax], 0x0100                        | 66 81 00 00 01                   |
    | add word [rax], 0x7fff                        | 66 81 00 ff 7f                   |
    | add word [rax], 0x8000                        | 66 81 00 00 80                   |
    | add word [rax], 0xffff                        | 66 81 00 ff ff                   |
    | add word [rcx], 0x007f                        | 66 81 01 7f 00                   |
    | add word [rdx], 0x0080                        | 66 81 02 80 00                   |
    | add word [rbx], 0x00ff                        | 66 81 03 ff 00                   |
    | add word [rsp], 0x0100                        | 66 81 04 24 00 01                |
    | add word [rbp], 0x7fff                        | 66 81 45 00 ff 7f                |
    | add word [rsi], 0x8000                        | 66 81 06 00 80                   |
    | add word [rdi], 0xffff                        | 66 81 07 ff ff                   |
    | add word [r8], 0x0000                         | 66 41 81 00 00 00                |
    | add word [r10], 0x007f                        | 66 41 81 02 7f 00                |
    | add word [r11], 0x0080                        | 66 41 81 03 80 00                |
    | add word [r12], 0x00ff                        | 66 41 81 04 24 ff 00             |
    | add word [r13], 0x0100                        | 66 41 81 45 00 00 01             |
    | add word [r14], 0x7fff                        | 66 41 81 06 ff 7f                |
    | add word [r15], 0x8000                        | 66 41 81 07 00 80                |
    | add word [rax + 1 * rcx], 0xffff              | 66 81 04 08 ff ff                |
    | add word [rcx + 1 * rcx], 0x0000              | 66 81 04 09 00 00                |
    | add word [rbx + 1 * rcx], 0x007f              | 66 81 04 0b 7f 00                |
    | add word [rsp + 1 * rcx], 0x0080              | 66 81 04 0c 80 00                |
    | add word [rbp + 1 * rcx], 0x00ff              | 66 81 44 0d 00 ff 00             |
    | add word [rsi + 1 * rcx], 0x0100              | 66 81 04 0e 00 01                |
    | add word [rdi + 1 * rcx], 0x7fff              | 66 81 04 0f ff 7f                |
    | add word [r8 + 1 * rcx], 0x8000               | 66 41 81 04 08 00 80             |
    | add word [r9 + 1 * rcx], 0xffff               | 66 41 81 04 09 ff ff             |
    | add word [r10 + 1 * rcx], 0x0000              | 66 41 81 04 0a 00 00             |
    | add word [r12 + 1 * rcx], 0x007f              | 66 41 81 04 0c 7f 00             |
    | add word [r13 + 1 * rcx], 0x0080              | 66 41 81 44 0d 00 80 00          |
    | add word [r14 + 1 * rcx], 0x00ff              | 66 41 81 04 0e ff 00             |
    | add word [r15 + 1 * rcx], 0x0100              | 66 41 81 04 0f 00 01             |
    | add word [rax + 1 * rax], 0x7fff              | 66 81 04 00 ff 7f                |
    | add word [rax + 1 * rdx], 0x8000              | 66 81 04 10 00 80                |
    | add word [rax + 1 * rbx], 0xffff              | 66 81 04 18 ff ff                |
    | add word [rax + 1 * rbp], 0x0000              | 66 81 04 28 00 00                |
    | add word [rax + 1 * rdi], 0x007f              | 66 81 04 38 7f 00                |
    | add word [rax + 1 * r8], 0x0080               | 66 42 81 04 00 80 00             |
    | add word [rax + 1 * r9], 0x00ff               | 66 42 81 04 08 ff 00             |
    | add word [rax + 1 * r10], 0x0100              | 66 42 81 04 10 00 01             |
    | add word [rax + 1 * r11], 0x7fff              | 66 42 81 04 18 ff 7f             |
    | add word [rax + 1 * r12], 0x8000              | 66 42 81 04 20 00 80             |
    | add word [rax + 1 * r13], 0xffff              | 66 42 81 04 28 ff ff             |
    | add word [rax + 1 * r14], 0x0000              | 66 42 81 04 30 00 00             |
    | add word [rax + 2 * rcx], 0x007f              | 66 81 04 48 7f 00                |
    | add word [rax + 4 * rcx], 0x0080              | 66 81 04 88 80 00                |
    | add word [rax + 8 * rcx], 0x00ff              | 66 81 04 c8 ff 00                |
    | add word [r8 + 1 * r9], 0x0100                | 66 43 81 04 08 00 01             |
    | add word [r8 + 2 * r9], 0x7fff                | 66 43 81 04 48 ff 7f             |
    | add word [r8 + 4 * r9], 0x8000                | 66 43 81 04 88 00 80             |
    | add word [r8 + 8 * r9], 0xffff                | 66 43 81 04 c8 ff ff             |
    | add word [1 * rcx], 0x0000                    | 66 81 04 0d 00 00 00 00 00 00    |
    | add word [4 * rcx], 0x007f                    | 66 81 04 8d 00 00 00 00 7f 00    |
    | add word [8 * rcx], 0x0080                    | 66 81 04 cd 00 00 00 00 80 00    |
    | add word [1 * r9], 0x00ff                     | 66 42 81 04 0d 00 00 00 00 ff 00 |
    | add word [2 * r9], 0x0100                     | 66 42 81 04 4d 00 00 00 00 00 01 |
    | add word [4 * r9], 0x7fff                     | 66 42 81 04 8d 00 00 00 00 ff 7f |
    | add word [8 * r9], 0x8000                     | 66 42 81 04 cd 00 00 00 00 00 80 |
    | add word [r13 + 8 * r12], 0xffff              | 66 43 81 44 e5 00 ff ff          |
    | add word [rsp + 4 * r15], 0x0000              | 66 42 81 04 bc 00 00             |
    | add word [rax + 1 * rcx - 0x00], 0x007f       | 66 81 44 08 00 7f 00             |
    | add word [rax + 1 * rcx + 0x01], 0x0080       | 66 81 44 08 01 80 00             |
    | add word [rax + 1 * rcx - 0x01], 0x00ff       | 66 81 44 08 ff ff 00             |
    | add word [rax + 1 * rcx + 0x00000001], 0x0100 | 66 81 84 08 01 00 00 00 00 01    |
    | add word [rax + 1 * rcx - 0x00000001], 0x7fff | 66 81 84 08 ff ff ff ff ff 7f    |
    | add word [rax + 1 * rcx + 0x7f], 0x8000       | 66 81 44 08 7f 00 80             |
    | add word [rax + 1 * rcx - 0x7f], 0xffff       | 66 81 44 08 81 ff ff             |
    | add word [rax + 1 * rcx + 0x80], 0x0000       | 66 81 84 08 80 00 00 00 00 00    |
    | add word [rax + 1 * rcx - 0x81], 0x007f       | 66 81 84 08 7f ff ff ff 7f 00    |
    | add word [rax + 1 * rcx + 0xff], 0x0080       | 66 81 84 08 ff 00 00 00 80 00    |
    | add word [rax + 1 * rcx - 0xff], 0x00ff       | 66 81 84 08 01 ff ff ff ff 00    |
    | add word [rax + 1 * rcx + 0x7fffffff], 0x0100 | 66 81 84 08 ff ff ff 7f 00 01    |
    | add word [rax + 1 * rcx - 0x7fffffff], 0x7fff | 66 81 84 08 01 00 00 80 ff 7f    |
    | add word [rax + 1 * rcx - 0x80000000], 0x8000 | 66 81 84 08 00 00 00 80 00 80    |
    | add word [r10 + 0x7f], 0xffff                 | 66 41 81 42 7f ff ff             |
    | add word [r10 + 0x80], 0x0000                 | 66 41 81 82 80 00 00 00 00 00    |
    | add word [r10 - 0x81], 0x007f                 | 66 41 81 82 7f ff ff ff 7f 00    |
    | --------------------------------------------- | -------------------------------- |
"""


def can_encode_add_addr16_imm16():
    encode(ADD_ADDR16_IMM16)


ADD_ADDR16_REG16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | add word [rax], cx                          | 66 01 08                   |
    | add word [rcx], cx                          | 66 01 09                   |
    | add word [rdx], cx                          | 66 01 0a                   |
    | add word [rbx], cx                          | 66 01 0b                   |
    | add word [rsp], cx                          | 66 01 0c 24                |
    | add word [rbp], cx                          | 66 01 4d 00                |
    | add word [rsi], cx                          | 66 01 0e                   |
    | add word [rdi], cx                          | 66 01 0f                   |
    | add word [r8], cx                           | 66 41 01 08                |
    | add word [r9], cx                           | 66 41 01 09                |
    | add word [r10], cx                          | 66 41 01 0a                |
    | add word [r11], cx                          | 66 41 01 0b                |
    | add word [r12], cx                          | 66 41 01 0c 24             |
    | add word [r13], cx                          | 66 41 01 4d 00             |
    | add word [r14], cx                          | 66 41 01 0e                |
    | add word [r15], cx                          | 66 41 01 0f                |
    | add word [rax + 1 * rcx], cx                | 66 01 0c 08                |
    | add word [rcx + 1 * rcx], cx                | 66 01 0c 09                |
    | add word [rdx + 1 * rcx], cx                | 66 01 0c 0a                |
    | add word [rbx + 1 * rcx], cx                | 66 01 0c 0b                |
    | add word [rsp + 1 * rcx], cx                | 66 01 0c 0c                |
    | add word [rbp + 1 * rcx], cx                | 66 01 4c 0d 00             |
    | add word [rsi + 1 * rcx], cx                | 66 01 0c 0e                |
    | add word [rdi + 1 * rcx], cx                | 66 01 0c 0f                |
    | add word [r8 + 1 * rcx], cx                 | 66 41 01 0c 08             |
    | add word [r9 + 1 * rcx], cx                 | 66 41 01 0c 09             |
    | add word [r10 + 1 * rcx], cx                | 66 41 01 0c 0a             |
    | add word [r11 + 1 * rcx], cx                | 66 41 01 0c 0b             |
    | add word [r12 + 1 * rcx], cx                | 66 41 01 0c 0c             |
    | add word [r13 + 1 * rcx], cx                | 66 41 01 4c 0d 00          |
    | add word [r14 + 1 * rcx], cx                | 66 41 01 0c 0e             |
    | add word [r15 + 1 * rcx], cx                | 66 41 01 0c 0f             |
    | add word [rax + 1 * rax], cx                | 66 01 0c 00                |
    | add word [rax + 1 * rdx], cx                | 66 01 0c 10                |
    | add word [rax + 1 * rbx], cx                | 66 01 0c 18                |
    | add word [rax + 1 * rbp], cx                | 66 01 0c 28                |
    | add word [rax + 1 * rsi], cx                | 66 01 0c 30                |
    | add word [rax + 1 * rdi], cx                | 66 01 0c 38                |
    | add word [rax + 1 * r8], cx                 | 66 42 01 0c 00             |
    | add word [rax + 1 * r9], cx                 | 66 42 01 0c 08             |
    | add word [rax + 1 * r10], cx                | 66 42 01 0c 10             |
    | add word [rax + 1 * r11], cx                | 66 42 01 0c 18             |
    | add word [rax + 1 * r12], cx                | 66 42 01 0c 20             |
    | add word [rax + 1 * r13], cx                | 66 42 01 0c 28             |
    | add word [rax + 1 * r14], cx                | 66 42 01 0c 30             |
    | add word [rax + 1 * r15], cx                | 66 42 01 0c 38             |
    | add word [rax + 2 * rcx], cx                | 66 01 0c 48                |
    | add word [rax + 4 * rcx], cx                | 66 01 0c 88                |
    | add word [rax + 8 * rcx], cx                | 66 01 0c c8                |
    | add word [r8 + 1 * r9], cx                  | 66 43 01 0c 08             |
    | add word [r8 + 2 * r9], cx                  | 66 43 01 0c 48             |
    | add word [r8 + 4 * r9], cx                  | 66 43 01 0c 88             |
    | add word [r8 + 8 * r9], cx                  | 66 43 01 0c c8             |
    | add word [1 * rcx], cx                      | 66 01 0c 0d 00 00 00 00    |
    | add word [2 * rcx], cx                      | 66 01 0c 4d 00 00 00 00    |
    | add word [4 * rcx], cx                      | 66 01 0c 8d 00 00 00 00    |
    | add word [8 * rcx], cx                      | 66 01 0c cd 00 00 00 00    |
    | add word [1 * r9], cx                       | 66 42 01 0c 0d 00 00 00 00 |
    | add word [2 * r9], cx                       | 66 42 01 0c 4d 00 00 00 00 |
    | add word [4 * r9], cx                       | 66 42 01 0c 8d 00 00 00 00 |
    | add word [8 * r9], cx                       | 66 42 01 0c cd 00 00 00 00 |
    | add word [r13 + 8 * r12], cx                | 66 43 01 4c e5 00          |
    | add word [rsp + 4 * r15], cx                | 66 42 01 0c bc             |
    | add word [rax + 1 * rcx + 0x00], cx         | 66 01 4c 08 00             |
    | add word [rax + 1 * rcx - 0x00], cx         | 66 01 4c 08 00             |
    | add word [rax + 1 * rcx + 0x01], cx         | 66 01 4c 08 01             |
    | add word [rax + 1 * rcx - 0x01], cx         | 66 01 4c 08 ff             |
    | add word [rax + 1 * rcx + 0x00000001], cx   | 66 01 8c 08 01 00 00 00    |
    | add word [rax + 1 * rcx - 0x00000001], cx   | 66 01 8c 08 ff ff ff ff    |
    | add word [rax + 1 * rcx + 0x7f], cx         | 66 01 4c 08 7f             |
    | add word [rax + 1 * rcx - 0x7f], cx         | 66 01 4c 08 81             |
    | add word [rax + 1 * rcx + 0x80], cx         | 66 01 8c 08 80 00 00 00    |
    | add word [rax + 1 * rcx - 0x80], cx         | 66 01 4c 08 80             |
    | add word [rax + 1 * rcx - 0x81], cx         | 66 01 8c 08 7f ff ff ff    |
    | add word [rax + 1 * rcx + 0xff], cx         | 66 01 8c 08 ff 00 00 00    |
    | add word [rax + 1 * rcx - 0xff], cx         | 66 01 8c 08 01 ff ff ff    |
    | add word [rax + 1 * rcx + 0x7fffffff], cx   | 66 01 8c 08 ff ff ff 7f    |
    | add word [rax + 1 * rcx - 0x7fffffff], cx   | 66 01 8c 08 01 00 00 80    |
    | add word [rax + 1 * rcx - 0x80000000], cx   | 66 01 8c 08 00 00 00 80    |
    | add word [r10 + 0x7f], cx                   | 66 41 01 4a 7f             |
    | add word [r10 + 0x80], cx                   | 66 41 01 8a 80 00 00 00    |
    | add word [r10 - 0x80], cx                   | 66 41 01 4a 80             |
    | add word [r10 - 0x81], cx                   | 66 41 01 8a 7f ff ff ff    |
    | add word [rax], ax                          | 66 01 00                   |
    | add word [rax], dx                          | 66 01 10                   |
    | add word [rax], bx                          | 66 01 18                   |
    | add word [rax], sp                          | 66 01 20                   |
    | add word [rax], bp                          | 66 01 28                   |
    | add word [rax], si                          | 66 01 30                   |
    | add word [rax], di                          | 66 01 38                   |
    | add word [rax], r8w                         | 66 44 01 00                |
    | add word [rax], r9w                         | 66 44 01 08                |
    | add word [rax], r10w                        | 66 44 01 10                |
    | add word [rax], r11w                        | 66 44 01 18                |
    | add word [rax], r12w                        | 66 44 01 20                |
    | add word [rax], r13w                        | 66 44 01 28                |
    | add word [rax], r14w                        | 66 44 01 30                |
    | add word [rax], r15w                        | 66 44 01 38                |
    | add word [rcx], dx                          | 66 01 11                   |
    | add word [rdx], bx                          | 66 01 1a                   |
    | add word [rbx], sp                          | 66 01 23                   |
    | add word [rsp], bp                          | 66 01 2c 24                |
    | add word [rbp], si                          | 66 01 75 00                |
    | add word [rsi], di                          | 66 01 3e                   |
    | add word [rdi], r8w                         | 66 44 01 07                |
    | add word [r8], r9w                          | 66 45 01 08                |
    | add word [r9], r10w                         | 66 45 01 11                |
    | add word [r10], r11w                        | 66 45 01 1a                |
    | add word [r11], r12w                        | 66 45 01 23                |
    | add word [r12], r13w                        | 66 45 01 2c 24             |
    | add word [r13], r14w                        | 66 45 01 75 00             |
    | add word [r14], r15w                        | 66 45 01 3e                |
    | add word [r15], ax                          | 66 41 01 07                |
    | add word [rcx + 1 * rcx], dx                | 66 01 14 09                |
    | add word [rdx + 1 * rcx], bx                | 66 01 1c 0a                |
    | add word [rbx + 1 * rcx], sp                | 66 01 24 0b                |
    | add word [rsp + 1 * rcx], bp                | 66 01 2c 0c                |
    | add word [rbp + 1 * rcx], si                | 66 01 74 0d 00             |
    | add word [rsi + 1 * rcx], di                | 66 01 3c 0e                |
    | add word [rdi + 1 * rcx], r8w               | 66 44 01 04 0f             |
    | add word [r8 + 1 * rcx], r9w                | 66 45 01 0c 08             |
    | add word [r9 + 1 * rcx], r10w               | 66 45 01 14 09             |
    | add word [r10 + 1 * rcx], r11w              | 66 45 01 1c 0a             |
    | add word [r11 + 1 * rcx], r12w              | 66 45 01 24 0b             |
    | add word [r12 + 1 * rcx], r13w              | 66 45 01 2c 0c             |
    | add word [r13 + 1 * rcx], r14w              | 66 45 01 74 0d 00          |
    | add word [r14 + 1 * rcx], r15w              | 66 45 01 3c 0e             |
    | add word [r15 + 1 * rcx], ax                | 66 41 01 04 0f             |
    | add word [rax + 1 * rdx], dx                | 66 01 14 10                |
    | add word [rax + 1 * rbx], bx                | 66 01 1c 18                |
    | add word [rax + 1 * rbp], sp                | 66 01 24 28                |
    | add word [rax + 1 * rsi], bp                | 66 01 2c 30                |
    | add word [rax + 1 * rdi], si                | 66 01 34 38                |
    | add word [rax + 1 * r8], di                 | 66 42 01 3c 00             |
    | add word [rax + 1 * r9], r8w                | 66 46 01 04 08             |
    | add word [rax + 1 * r10], r9w               | 66 46 01 0c 10             |
    | add word [rax + 1 * r11], r10w              | 66 46 01 14 18             |
    | add word [rax + 1 * r12], r11w              | 66 46 01 1c 20             |
    | add word [rax + 1 * r13], r12w              | 66 46 01 24 28             |
    | add word [rax + 1 * r14], r13w              | 66 46 01 2c 30             |
    | add word [rax + 1 * r15], r14w              | 66 46 01 34 38             |
    | add word [rax + 2 * rcx], r15w              | 66 44 01 3c 48             |
    | add word [rax + 4 * rcx], ax                | 66 01 04 88                |
    | add word [r8 + 1 * r9], dx                  | 66 43 01 14 08             |
    | add word [r8 + 2 * r9], bx                  | 66 43 01 1c 48             |
    | add word [r8 + 4 * r9], sp                  | 66 43 01 24 88             |
    | add word [r8 + 8 * r9], bp                  | 66 43 01 2c c8             |
    | add word [1 * rcx], si                      | 66 01 34 0d 00 00 00 00    |
    | add word [2 * rcx], di                      | 66 01 3c 4d 00 00 00 00    |
    | add word [4 * rcx], r8w                     | 66 44 01 04 8d 00 00 00 00 |
    | add word [8 * rcx], r9w                     | 66 44 01 0c cd 00 00 00 00 |
    | add word [1 * r9], r10w                     | 66 46 01 14 0d 00 00 00 00 |
    | add word [2 * r9], r11w                     | 66 46 01 1c 4d 00 00 00 00 |
    | add word [4 * r9], r12w                     | 66 46 01 24 8d 00 00 00 00 |
    | add word [8 * r9], r13w                     | 66 46 01 2c cd 00 00 00 00 |
    | add word [r13 + 8 * r12], r14w              | 66 47 01 74 e5 00          |
    | add word [rsp + 4 * r15], r15w              | 66 46 01 3c bc             |
    | add word [rax + 1 * rcx + 0x00], ax         | 66 01 44 08 00             |
    | add word [rax + 1 * rcx + 0x01], dx         | 66 01 54 08 01             |
    | add word [rax + 1 * rcx - 0x01], bx         | 66 01 5c 08 ff             |
    | add word [rax + 1 * rcx + 0x00000001], sp   | 66 01 a4 08 01 00 00 00    |
    | add word [rax + 1 * rcx - 0x00000001], bp   | 66 01 ac 08 ff ff ff ff    |
    | add word [rax + 1 * rcx + 0x7f], si         | 66 01 74 08 7f             |
    | add word [rax + 1 * rcx - 0x7f], di         | 66 01 7c 08 81             |
    | add word [rax + 1 * rcx + 0x80], r8w        | 66 44 01 84 08 80 00 00 00 |
    | add word [rax + 1 * rcx - 0x80], r9w        | 66 44 01 4c 08 80          |
    | add word [rax + 1 * rcx - 0x81], r10w       | 66 44 01 94 08 7f ff ff ff |
    | add word [rax + 1 * rcx + 0xff], r11w       | 66 44 01 9c 08 ff 00 00 00 |
    | add word [rax + 1 * rcx - 0xff], r12w       | 66 44 01 a4 08 01 ff ff ff |
    | add word [rax + 1 * rcx + 0x7fffffff], r13w | 66 44 01 ac 08 ff ff ff 7f |
    | add word [rax + 1 * rcx - 0x7fffffff], r14w | 66 44 01 b4 08 01 00 00 80 |
    | add word [rax + 1 * rcx - 0x80000000], r15w | 66 44 01 bc 08 00 00 00 80 |
    | add word [r10 + 0x7f], ax                   | 66 41 01 42 7f             |
    | add word [r10 - 0x80], dx                   | 66 41 01 52 80             |
    | add word [r10 - 0x81], bx                   | 66 41 01 9a 7f ff ff ff    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_add_addr16_reg16():
    encode(ADD_ADDR16_REG16)


ADD_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | add byte [rax], 0x01                        | 80 00 01                   |
    | add byte [rcx], 0x01                        | 80 01 01                   |
    | add byte [rdx], 0x01                        | 80 02 01                   |
    | add byte [rbx], 0x01                        | 80 03 01                   |
    | add byte [rsp], 0x01                        | 80 04 24 01                |
    | add byte [rbp], 0x01                        | 80 45 00 01                |
    | add byte [rsi], 0x01                        | 80 06 01                   |
    | add byte [rdi], 0x01                        | 80 07 01                   |
    | add byte [r8], 0x01                         | 41 80 00 01                |
    | add byte [r9], 0x01                         | 41 80 01 01                |
    | add byte [r10], 0x01                        | 41 80 02 01                |
    | add byte [r11], 0x01                        | 41 80 03 01                |
    | add byte [r12], 0x01                        | 41 80 04 24 01             |
    | add byte [r13], 0x01                        | 41 80 45 00 01             |
    | add byte [r14], 0x01                        | 41 80 06 01                |
    | add byte [r15], 0x01                        | 41 80 07 01                |
    | add byte [rax + 1 * rcx], 0x01              | 80 04 08 01                |
    | add byte [rcx + 1 * rcx], 0x01              | 80 04 09 01                |
    | add byte [rdx + 1 * rcx], 0x01              | 80 04 0a 01                |
    | add byte [rbx + 1 * rcx], 0x01              | 80 04 0b 01                |
    | add byte [rsp + 1 * rcx], 0x01              | 80 04 0c 01                |
    | add byte [rbp + 1 * rcx], 0x01              | 80 44 0d 00 01             |
    | add byte [rsi + 1 * rcx], 0x01              | 80 04 0e 01                |
    | add byte [rdi + 1 * rcx], 0x01              | 80 04 0f 01                |
    | add byte [r8 + 1 * rcx], 0x01               | 41 80 04 08 01             |
    | add byte [r9 + 1 * rcx], 0x01               | 41 80 04 09 01             |
    | add byte [r10 + 1 * rcx], 0x01              | 41 80 04 0a 01             |
    | add byte [r11 + 1 * rcx], 0x01              | 41 80 04 0b 01             |
    | add byte [r12 + 1 * rcx], 0x01              | 41 80 04 0c 01             |
    | add byte [r13 + 1 * rcx], 0x01              | 41 80 44 0d 00 01          |
    | add byte [r14 + 1 * rcx], 0x01              | 41 80 04 0e 01             |
    | add byte [r15 + 1 * rcx], 0x01              | 41 80 04 0f 01             |
    | add byte [rax + 1 * rax], 0x01              | 80 04 00 01                |
    | add byte [rax + 1 * rdx], 0x01              | 80 04 10 01                |
    | add byte [rax + 1 * rbx], 0x01              | 80 04 18 01                |
    | add byte [rax + 1 * rbp], 0x01              | 80 04 28 01                |
    | add byte [rax + 1 * rsi], 0x01              | 80 04 30 01                |
    | add byte [rax + 1 * rdi], 0x01              | 80 04 38 01                |
    | add byte [rax + 1 * r8], 0x01               | 42 80 04 00 01             |
    | add byte [rax + 1 * r9], 0x01               | 42 80 04 08 01             |
    | add byte [rax + 1 * r10], 0x01              | 42 80 04 10 01             |
    | add byte [rax + 1 * r11], 0x01              | 42 80 04 18 01             |
    | add byte [rax + 1 * r12], 0x01              | 42 80 04 20 01             |
    | add byte [rax + 1 * r13], 0x01              | 42 80 04 28 01             |
    | add byte [rax + 1 * r14], 0x01              | 42 80 04 30 01             |
    | add byte [rax + 1 * r15], 0x01              | 42 80 04 38 01             |
    | add byte [rax + 2 * rcx], 0x01              | 80 04 48 01                |
    | add byte [rax + 4 * rcx], 0x01              | 80 04 88 01                |
    | add byte [rax + 8 * rcx], 0x01              | 80 04 c8 01                |
    | add byte [r8 + 1 * r9], 0x01                | 43 80 04 08 01             |
    | add byte [r8 + 2 * r9], 0x01                | 43 80 04 48 01             |
    | add byte [r8 + 4 * r9], 0x01                | 43 80 04 88 01             |
    | add byte [r8 + 8 * r9], 0x01                | 43 80 04 c8 01             |
    | add byte [1 * rcx], 0x01                    | 80 04 0d 00 00 00 00 01    |
    | add byte [2 * rcx], 0x01                    | 80 04 4d 00 00 00 00 01    |
    | add byte [4 * rcx], 0x01                    | 80 04 8d 00 00 00 00 01    |
    | add byte [8 * rcx], 0x01                    | 80 04 cd 00 00 00 00 01    |
    | add byte [1 * r9], 0x01                     | 42 80 04 0d 00 00 00 00 01 |
    | add byte [2 * r9], 0x01                     | 42 80 04 4d 00 00 00 00 01 |
    | add byte [4 * r9], 0x01                     | 42 80 04 8d 00 00 00 00 01 |
    | add byte [8 * r9], 0x01                     | 42 80 04 cd 00 00 00 00 01 |
    | add byte [r13 + 8 * r12], 0x01              | 43 80 44 e5 00 01          |
    | add byte [rsp + 4 * r15], 0x01              | 42 80 04 bc 01             |
    | add byte [rax + 1 * rcx + 0x00], 0x01       | 80 44 08 00 01             |
    | add byte [rax + 1 * rcx - 0x00], 0x01       | 80 44 08 00 01             |
    | add byte [rax + 1 * rcx + 0x01], 0x01       | 80 44 08 01 01             |
    | add byte [rax + 1 * rcx - 0x01], 0x01       | 80 44 08 ff 01             |
    | add byte [rax + 1 * rcx + 0x00000001], 0x01 | 80 84 08 01 00 00 00 01    |
    | add byte [rax + 1 * rcx - 0x00000001], 0x01 | 80 84 08 ff ff ff ff 01    |
    | add byte [rax + 1 * rcx + 0x7f], 0x01       | 80 44 08 7f 01             |
    | add byte [rax + 1 * rcx - 0x7f], 0x01       | 80 44 08 81 01             |
    | add byte [rax + 1 * rcx + 0x80], 0x01       | 80 84 08 80 00 00 00 01    |
    | add byte [rax + 1 * rcx - 0x80], 0x01       | 80 44 08 80 01             |
    | add byte [rax + 1 * rcx - 0x81], 0x01       | 80 84 08 7f ff ff ff 01    |
    | add byte [rax + 1 * rcx + 0xff], 0x01       | 80 84 08 ff 00 00 00 01    |
    | add byte [rax + 1 * rcx - 0xff], 0x01       | 80 84 08 01 ff ff ff 01    |
    | add byte [rax + 1 * rcx + 0x7fffffff], 0x01 | 80 84 08 ff ff ff 7f 01    |
    | add byte [rax + 1 * rcx - 0x7fffffff], 0x01 | 80 84 08 01 00 00 80 01    |
    | add byte [rax + 1 * rcx - 0x80000000], 0x01 | 80 84 08 00 00 00 80 01    |
    | add byte [r10 + 0x7f], 0x01                 | 41 80 42 7f 01             |
    | add byte [r10 + 0x80], 0x01                 | 41 80 82 80 00 00 00 01    |
    | add byte [r10 - 0x80], 0x01                 | 41 80 42 80 01             |
    | add byte [r10 - 0x81], 0x01                 | 41 80 82 7f ff ff ff 01    |
    | add byte [rax], 0x00                        | 80 00 00                   |
    | add byte [rax], 0x7f                        | 80 00 7f                   |
    | add byte [rax], 0x80                        | 80 00 80                   |
    | add byte [rax], 0xff                        | 80 00 ff                   |
    | add byte [rcx], 0x7f                        | 80 01 7f                   |
    | add byte [rdx], 0x80                        | 80 02 80                   |
    | add byte [rbx], 0xff                        | 80 03 ff                   |
    | add byte [rsp], 0x00                        | 80 04 24 00                |
    | add byte [rsi], 0x7f                        | 80 06 7f                   |
    | add byte [rdi], 0x80                        | 80 07 80                   |
    | add byte [r8], 0xff                         | 41 80 00 ff                |
    | add byte [r9], 0x00                         | 41 80 01 00                |
    | add byte [r11], 0x7f                        | 41 80 03 7f                |
    | add byte [r12], 0x80                        | 41 80 04 24 80             |
    | add byte [r13], 0xff                        | 41 80 45 00 ff             |
    | add byte [r14], 0x00                        | 41 80 06 00                |
    | add byte [rax + 1 * rcx], 0x7f              | 80 04 08 7f                |
    | add byte [rcx + 1 * rcx], 0x80              | 80 04 09 80                |
    | add byte [rdx + 1 * rcx], 0xff              | 80 04 0a ff                |
    | add byte [rbx + 1 * rcx], 0x00              | 80 04 0b 00                |
    | add byte [rbp + 1 * rcx], 0x7f              | 80 44 0d 00 7f             |
    | add byte [rsi + 1 * rcx], 0x80              | 80 04 0e 80                |
    | add byte [rdi + 1 * rcx], 0xff              | 80 04 0f ff                |
    | add byte [r8 + 1 * rcx], 0x00               | 41 80 04 08 00             |
    | add byte [r10 + 1 * rcx], 0x7f              | 41 80 04 0a 7f             |
    | add byte [r11 + 1 * rcx], 0x80              | 41 80 04 0b 80             |
    | add byte [r12 + 1 * rcx], 0xff              | 41 80 04 0c ff             |
    | add byte [r13 + 1 * rcx], 0x00              | 41 80 44 0d 00 00          |
    | add byte [r15 + 1 * rcx], 0x7f              | 41 80 04 0f 7f             |
    | add byte [rax + 1 * rax], 0x80              | 80 04 00 80                |
    | add byte [rax + 1 * rdx], 0xff              | 80 04 10 ff                |
    | add byte [rax + 1 * rbx], 0x00              | 80 04 18 00                |
    | add byte [rax + 1 * rsi], 0x7f              | 80 04 30 7f                |
    | add byte [rax + 1 * rdi], 0x80              | 80 04 38 80                |
    | add byte [rax + 1 * r8], 0xff               | 42 80 04 00 ff             |
    | add byte [rax + 1 * r9], 0x00               | 42 80 04 08 00             |
    | add byte [rax + 1 * r11], 0x7f              | 42 80 04 18 7f             |
    | add byte [rax + 1 * r12], 0x80              | 42 80 04 20 80             |
    | add byte [rax + 1 * r13], 0xff              | 42 80 04 28 ff             |
    | add byte [rax + 1 * r14], 0x00              | 42 80 04 30 00             |
    | add byte [rax + 2 * rcx], 0x7f              | 80 04 48 7f                |
    | add byte [rax + 4 * rcx], 0x80              | 80 04 88 80                |
    | add byte [rax + 8 * rcx], 0xff              | 80 04 c8 ff                |
    | add byte [r8 + 1 * r9], 0x00                | 43 80 04 08 00             |
    | add byte [r8 + 4 * r9], 0x7f                | 43 80 04 88 7f             |
    | add byte [r8 + 8 * r9], 0x80                | 43 80 04 c8 80             |
    | add byte [1 * rcx], 0xff                    | 80 04 0d 00 00 00 00 ff    |
    | add byte [2 * rcx], 0x00                    | 80 04 4d 00 00 00 00 00    |
    | add byte [8 * rcx], 0x7f                    | 80 04 cd 00 00 00 00 7f    |
    | add byte [1 * r9], 0x80                     | 42 80 04 0d 00 00 00 00 80 |
    | add byte [2 * r9], 0xff                     | 42 80 04 4d 00 00 00 00 ff |
    | add byte [4 * r9], 0x00                     | 42 80 04 8d 00 00 00 00 00 |
    | add byte [r13 + 8 * r12], 0x7f              | 43 80 44 e5 00 7f          |
    | add byte [rsp + 4 * r15], 0x80              | 42 80 04 bc 80             |
    | add byte [rax + 1 * rcx + 0x00], 0xff       | 80 44 08 00 ff             |
    | add byte [rax + 1 * rcx - 0x00], 0x00       | 80 44 08 00 00             |
    | add byte [rax + 1 * rcx - 0x01], 0x7f       | 80 44 08 ff 7f             |
    | add byte [rax + 1 * rcx + 0x00000001], 0x80 | 80 84 08 01 00 00 00 80    |
    | add byte [rax + 1 * rcx - 0x00000001], 0xff | 80 84 08 ff ff ff ff ff    |
    | add byte [rax + 1 * rcx + 0x7f], 0x00       | 80 44 08 7f 00             |
    | add byte [rax + 1 * rcx + 0x80], 0x7f       | 80 84 08 80 00 00 00 7f    |
    | add byte [rax + 1 * rcx - 0x80], 0x80       | 80 44 08 80 80             |
    | add byte [rax + 1 * rcx - 0x81], 0xff       | 80 84 08 7f ff ff ff ff    |
    | add byte [rax + 1 * rcx + 0xff], 0x00       | 80 84 08 ff 00 00 00 00    |
    | add byte [rax + 1 * rcx + 0x7fffffff], 0x7f | 80 84 08 ff ff ff 7f 7f    |
    | add byte [rax + 1 * rcx - 0x7fffffff], 0x80 | 80 84 08 01 00 00 80 80    |
    | add byte [rax + 1 * rcx - 0x80000000], 0xff | 80 84 08 00 00 00 80 ff    |
    | add byte [r10 + 0x7f], 0x00                 | 41 80 42 7f 00             |
    | add byte [r10 - 0x80], 0x7f                 | 41 80 42 80 7f             |
    | add byte [r10 - 0x81], 0x80                 | 41 80 82 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_add_addr8_imm8():
    encode(ADD_ADDR8_IMM8)


ADD_ADDR8_REG8 = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | add byte [rax], cl                         | 00 08                   |
    | add byte [rcx], cl                         | 00 09                   |
    | add byte [rdx], cl                         | 00 0a                   |
    | add byte [rbx], cl                         | 00 0b                   |
    | add byte [rsp], cl                         | 00 0c 24                |
    | add byte [rbp], cl                         | 00 4d 00                |
    | add byte [rsi], cl                         | 00 0e                   |
    | add byte [rdi], cl                         | 00 0f                   |
    | add byte [r8], cl                          | 41 00 08                |
    | add byte [r9], cl                          | 41 00 09                |
    | add byte [r10], cl                         | 41 00 0a                |
    | add byte [r11], cl                         | 41 00 0b                |
    | add byte [r12], cl                         | 41 00 0c 24             |
    | add byte [r13], cl                         | 41 00 4d 00             |
    | add byte [r14], cl                         | 41 00 0e                |
    | add byte [r15], cl                         | 41 00 0f                |
    | add byte [rax + 1 * rcx], cl               | 00 0c 08                |
    | add byte [rcx + 1 * rcx], cl               | 00 0c 09                |
    | add byte [rdx + 1 * rcx], cl               | 00 0c 0a                |
    | add byte [rbx + 1 * rcx], cl               | 00 0c 0b                |
    | add byte [rsp + 1 * rcx], cl               | 00 0c 0c                |
    | add byte [rbp + 1 * rcx], cl               | 00 4c 0d 00             |
    | add byte [rsi + 1 * rcx], cl               | 00 0c 0e                |
    | add byte [rdi + 1 * rcx], cl               | 00 0c 0f                |
    | add byte [r8 + 1 * rcx], cl                | 41 00 0c 08             |
    | add byte [r9 + 1 * rcx], cl                | 41 00 0c 09             |
    | add byte [r10 + 1 * rcx], cl               | 41 00 0c 0a             |
    | add byte [r11 + 1 * rcx], cl               | 41 00 0c 0b             |
    | add byte [r12 + 1 * rcx], cl               | 41 00 0c 0c             |
    | add byte [r13 + 1 * rcx], cl               | 41 00 4c 0d 00          |
    | add byte [r14 + 1 * rcx], cl               | 41 00 0c 0e             |
    | add byte [r15 + 1 * rcx], cl               | 41 00 0c 0f             |
    | add byte [rax + 1 * rax], cl               | 00 0c 00                |
    | add byte [rax + 1 * rdx], cl               | 00 0c 10                |
    | add byte [rax + 1 * rbx], cl               | 00 0c 18                |
    | add byte [rax + 1 * rbp], cl               | 00 0c 28                |
    | add byte [rax + 1 * rsi], cl               | 00 0c 30                |
    | add byte [rax + 1 * rdi], cl               | 00 0c 38                |
    | add byte [rax + 1 * r8], cl                | 42 00 0c 00             |
    | add byte [rax + 1 * r9], cl                | 42 00 0c 08             |
    | add byte [rax + 1 * r10], cl               | 42 00 0c 10             |
    | add byte [rax + 1 * r11], cl               | 42 00 0c 18             |
    | add byte [rax + 1 * r12], cl               | 42 00 0c 20             |
    | add byte [rax + 1 * r13], cl               | 42 00 0c 28             |
    | add byte [rax + 1 * r14], cl               | 42 00 0c 30             |
    | add byte [rax + 1 * r15], cl               | 42 00 0c 38             |
    | add byte [rax + 2 * rcx], cl               | 00 0c 48                |
    | add byte [rax + 4 * rcx], cl               | 00 0c 88                |
    | add byte [rax + 8 * rcx], cl               | 00 0c c8                |
    | add byte [r8 + 1 * r9], cl                 | 43 00 0c 08             |
    | add byte [r8 + 2 * r9], cl                 | 43 00 0c 48             |
    | add byte [r8 + 4 * r9], cl                 | 43 00 0c 88             |
    | add byte [r8 + 8 * r9], cl                 | 43 00 0c c8             |
    | add byte [1 * rcx], cl                     | 00 0c 0d 00 00 00 00    |
    | add byte [2 * rcx], cl                     | 00 0c 4d 00 00 00 00    |
    | add byte [4 * rcx], cl                     | 00 0c 8d 00 00 00 00    |
    | add byte [8 * rcx], cl                     | 00 0c cd 00 00 00 00    |
    | add byte [1 * r9], cl                      | 42 00 0c 0d 00 00 00 00 |
    | add byte [2 * r9], cl                      | 42 00 0c 4d 00 00 00 00 |
    | add byte [4 * r9], cl                      | 42 00 0c 8d 00 00 00 00 |
    | add byte [8 * r9], cl                      | 42 00 0c cd 00 00 00 00 |
    | add byte [r13 + 8 * r12], cl               | 43 00 4c e5 00          |
    | add byte [rsp + 4 * r15], cl               | 42 00 0c bc             |
    | add byte [rax + 1 * rcx + 0x00], cl        | 00 4c 08 00             |
    | add byte [rax + 1 * rcx - 0x00], cl        | 00 4c 08 00             |
    | add byte [rax + 1 * rcx + 0x01], cl        | 00 4c 08 01             |
    | add byte [rax + 1 * rcx - 0x01], cl        | 00 4c 08 ff             |
    | add byte [rax + 1 * rcx + 0x00000001], cl  | 00 8c 08 01 00 00 00    |
    | add byte [rax + 1 * rcx - 0x00000001], cl  | 00 8c 08 ff ff ff ff    |
    | add byte [rax + 1 * rcx + 0x7f], cl        | 00 4c 08 7f             |
    | add byte [rax + 1 * rcx - 0x7f], cl        | 00 4c 08 81             |
    | add byte [rax + 1 * rcx + 0x80], cl        | 00 8c 08 80 00 00 00    |
    | add byte [rax + 1 * rcx - 0x80], cl        | 00 4c 08 80             |
    | add byte [rax + 1 * rcx - 0x81], cl        | 00 8c 08 7f ff ff ff    |
    | add byte [rax + 1 * rcx + 0xff], cl        | 00 8c 08 ff 00 00 00    |
    | add byte [rax + 1 * rcx - 0xff], cl        | 00 8c 08 01 ff ff ff    |
    | add byte [rax + 1 * rcx + 0x7fffffff], cl  | 00 8c 08 ff ff ff 7f    |
    | add byte [rax + 1 * rcx - 0x7fffffff], cl  | 00 8c 08 01 00 00 80    |
    | add byte [rax + 1 * rcx - 0x80000000], cl  | 00 8c 08 00 00 00 80    |
    | add byte [r10 + 0x7f], cl                  | 41 00 4a 7f             |
    | add byte [r10 + 0x80], cl                  | 41 00 8a 80 00 00 00    |
    | add byte [r10 - 0x80], cl                  | 41 00 4a 80             |
    | add byte [r10 - 0x81], cl                  | 41 00 8a 7f ff ff ff    |
    | add byte [rax], al                         | 00 00                   |
    | add byte [rax], dl                         | 00 10                   |
    | add byte [rax], bl                         | 00 18                   |
    | add byte [rax], spl                        | 40 00 20                |
    | add byte [rax], bpl                        | 40 00 28                |
    | add byte [rax], sil                        | 40 00 30                |
    | add byte [rax], dil                        | 40 00 38                |
    | add byte [rax], r8b                        | 44 00 00                |
    | add byte [rax], r9b                        | 44 00 08                |
    | add byte [rax], r10b                       | 44 00 10                |
    | add byte [rax], r11b                       | 44 00 18                |
    | add byte [rax], r12b                       | 44 00 20                |
    | add byte [rax], r13b                       | 44 00 28                |
    | add byte [rax], r14b                       | 44 00 30                |
    | add byte [rax], r15b                       | 44 00 38                |
    | add byte [rax], ah                         | 00 20                   |
    | add byte [rax], ch                         | 00 28                   |
    | add byte [rax], dh                         | 00 30                   |
    | add byte [rax], bh                         | 00 38                   |
    | add byte [rcx], dl                         | 00 11                   |
    | add byte [rdx], bl                         | 00 1a                   |
    | add byte [rbx], spl                        | 40 00 23                |
    | add byte [rsp], bpl                        | 40 00 2c 24             |
    | add byte [rbp], sil                        | 40 00 75 00             |
    | add byte [rsi], dil                        | 40 00 3e                |
    | add byte [rdi], r8b                        | 44 00 07                |
    | add byte [r8], r9b                         | 45 00 08                |
    | add byte [r9], r10b                        | 45 00 11                |
    | add byte [r10], r11b                       | 45 00 1a                |
    | add byte [r11], r12b                       | 45 00 23                |
    | add byte [r12], r13b                       | 45 00 2c 24             |
    | add byte [r13], r14b                       | 45 00 75 00             |
    | add byte [r14], r15b                       | 45 00 3e                |
    | add byte [r15], ah                         | !! !! !!                |
    | add byte [rax + 1 * rcx], ch               | 00 2c 08                |
    | add byte [rcx + 1 * rcx], dh               | 00 34 09                |
    | add byte [rdx + 1 * rcx], bh               | 00 3c 0a                |
    | add byte [rbx + 1 * rcx], al               | 00 04 0b                |
    | add byte [rbp + 1 * rcx], dl               | 00 54 0d 00             |
    | add byte [rsi + 1 * rcx], bl               | 00 1c 0e                |
    | add byte [rdi + 1 * rcx], spl              | 40 00 24 0f             |
    | add byte [r8 + 1 * rcx], bpl               | 41 00 2c 08             |
    | add byte [r9 + 1 * rcx], sil               | 41 00 34 09             |
    | add byte [r10 + 1 * rcx], dil              | 41 00 3c 0a             |
    | add byte [r11 + 1 * rcx], r8b              | 45 00 04 0b             |
    | add byte [r12 + 1 * rcx], r9b              | 45 00 0c 0c             |
    | add byte [r13 + 1 * rcx], r10b             | 45 00 54 0d 00          |
    | add byte [r14 + 1 * rcx], r11b             | 45 00 1c 0e             |
    | add byte [r15 + 1 * rcx], r12b             | 45 00 24 0f             |
    | add byte [rax + 1 * rax], r13b             | 44 00 2c 00             |
    | add byte [rax + 1 * rdx], r14b             | 44 00 34 10             |
    | add byte [rax + 1 * rbx], r15b             | 44 00 3c 18             |
    | add byte [rax + 1 * rbp], ah               | 00 24 28                |
    | add byte [rax + 1 * rsi], ch               | 00 2c 30                |
    | add byte [rax + 1 * rdi], dh               | 00 34 38                |
    | add byte [rax + 1 * r8], bh                | !! !! !!                |
    | add byte [rax + 1 * r9], al                | 42 00 04 08             |
    | add byte [rax + 1 * r11], dl               | 42 00 14 18             |
    | add byte [rax + 1 * r12], bl               | 42 00 1c 20             |
    | add byte [rax + 1 * r13], spl              | 42 00 24 28             |
    | add byte [rax + 1 * r14], bpl              | 42 00 2c 30             |
    | add byte [rax + 1 * r15], sil              | 42 00 34 38             |
    | add byte [rax + 2 * rcx], dil              | 40 00 3c 48             |
    | add byte [rax + 4 * rcx], r8b              | 44 00 04 88             |
    | add byte [rax + 8 * rcx], r9b              | 44 00 0c c8             |
    | add byte [r8 + 1 * r9], r10b               | 47 00 14 08             |
    | add byte [r8 + 2 * r9], r11b               | 47 00 1c 48             |
    | add byte [r8 + 4 * r9], r12b               | 47 00 24 88             |
    | add byte [r8 + 8 * r9], r13b               | 47 00 2c c8             |
    | add byte [1 * rcx], r14b                   | 44 00 34 0d 00 00 00 00 |
    | add byte [2 * rcx], r15b                   | 44 00 3c 4d 00 00 00 00 |
    | add byte [4 * rcx], ah                     | 00 24 8d 00 00 00 00    |
    | add byte [8 * rcx], ch                     | 00 2c cd 00 00 00 00    |
    | add byte [1 * r9], dh                      | !! !! !!                |
    | add byte [2 * r9], bh                      | !! !! !!                |
    | add byte [4 * r9], al                      | 42 00 04 8d 00 00 00 00 |
    | add byte [r13 + 8 * r12], dl               | 43 00 54 e5 00          |
    | add byte [rsp + 4 * r15], bl               | 42 00 1c bc             |
    | add byte [rax + 1 * rcx + 0x00], spl       | 40 00 64 08 00          |
    | add byte [rax + 1 * rcx - 0x00], bpl       | 40 00 6c 08 00          |
    | add byte [rax + 1 * rcx + 0x01], sil       | 40 00 74 08 01          |
    | add byte [rax + 1 * rcx - 0x01], dil       | 40 00 7c 08 ff          |
    | add byte [rax + 1 * rcx + 0x00000001], r8b | 44 00 84 08 01 00 00 00 |
    | add byte [rax + 1 * rcx - 0x00000001], r9b | 44 00 8c 08 ff ff ff ff |
    | add byte [rax + 1 * rcx + 0x7f], r10b      | 44 00 54 08 7f          |
    | add byte [rax + 1 * rcx - 0x7f], r11b      | 44 00 5c 08 81          |
    | add byte [rax + 1 * rcx + 0x80], r12b      | 44 00 a4 08 80 00 00 00 |
    | add byte [rax + 1 * rcx - 0x80], r13b      | 44 00 6c 08 80          |
    | add byte [rax + 1 * rcx - 0x81], r14b      | 44 00 b4 08 7f ff ff ff |
    | add byte [rax + 1 * rcx + 0xff], r15b      | 44 00 bc 08 ff 00 00 00 |
    | add byte [rax + 1 * rcx - 0xff], ah        | 00 a4 08 01 ff ff ff    |
    | add byte [rax + 1 * rcx + 0x7fffffff], ch  | 00 ac 08 ff ff ff 7f    |
    | add byte [rax + 1 * rcx - 0x7fffffff], dh  | 00 b4 08 01 00 00 80    |
    | add byte [rax + 1 * rcx - 0x80000000], bh  | 00 bc 08 00 00 00 80    |
    | add byte [r10 + 0x7f], al                  | 41 00 42 7f             |
    | add byte [r10 - 0x80], dl                  | 41 00 52 80             |
    | add byte [r10 - 0x81], bl                  | 41 00 9a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_add_addr8_reg8():
    encode(ADD_ADDR8_REG8)
