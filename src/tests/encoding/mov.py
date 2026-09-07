from tests.encoding.core import encode, exhaust


def can_exhaust_mov():
    exhaust(
        MOV_ADDR16_IMM16,
        MOV_ADDR16_REG16,
        MOV_ADDR32_IMM32,
        MOV_ADDR32_REG32,
        MOV_ADDR64_IMM32,
        MOV_ADDR64_REG64,
        MOV_ADDR8_IMM8,
        MOV_ADDR8_REG8,
        MOV_REG16_ADDR16,
        MOV_REG16_IMM16,
        MOV_REG16_REG16,
        MOV_REG32_ADDR32,
        MOV_REG32_IMM32,
        MOV_REG32_REG32,
        MOV_REG64_ADDR64,
        MOV_REG64_IMM32,
        MOV_REG64_IMM64,
        MOV_REG64_REG64,
        MOV_REG8_ADDR8,
        MOV_REG8_IMM8,
        MOV_REG8_REG8,
    )


MOV_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | mov rax, 0x00000001 | 48 c7 c0 01 00 00 00 | *** | mov rax, 0x00007fff | 48 c7 c0 ff 7f 00 00 |
    | mov rcx, 0x00000001 | 48 c7 c1 01 00 00 00 | *** | mov rax, 0x00008000 | 48 c7 c0 00 80 00 00 |
    | mov rdx, 0x00000001 | 48 c7 c2 01 00 00 00 | *** | mov rax, 0x0000ffff | 48 c7 c0 ff ff 00 00 |
    | mov rbx, 0x00000001 | 48 c7 c3 01 00 00 00 | *** | mov rax, 0x00010000 | 48 c7 c0 00 00 01 00 |
    | mov rsp, 0x00000001 | 48 c7 c4 01 00 00 00 | *** | mov rax, 0x7fffffff | 48 c7 c0 ff ff ff 7f |
    | mov rbp, 0x00000001 | 48 c7 c5 01 00 00 00 | *** | mov rax, 0x80000000 | 48 c7 c0 00 00 00 80 |
    | mov rsi, 0x00000001 | 48 c7 c6 01 00 00 00 | *** | mov rax, 0xffffffff | 48 c7 c0 ff ff ff ff |
    | mov rdi, 0x00000001 | 48 c7 c7 01 00 00 00 | *** | mov rcx, 0x0000007f | 48 c7 c1 7f 00 00 00 |
    | mov r8, 0x00000001  | 49 c7 c0 01 00 00 00 | *** | mov rdx, 0x00000080 | 48 c7 c2 80 00 00 00 |
    | mov r9, 0x00000001  | 49 c7 c1 01 00 00 00 | *** | mov rbx, 0x000000ff | 48 c7 c3 ff 00 00 00 |
    | mov r10, 0x00000001 | 49 c7 c2 01 00 00 00 | *** | mov rsp, 0x00000100 | 48 c7 c4 00 01 00 00 |
    | mov r11, 0x00000001 | 49 c7 c3 01 00 00 00 | *** | mov rbp, 0x00007fff | 48 c7 c5 ff 7f 00 00 |
    | mov r12, 0x00000001 | 49 c7 c4 01 00 00 00 | *** | mov rsi, 0x00008000 | 48 c7 c6 00 80 00 00 |
    | mov r13, 0x00000001 | 49 c7 c5 01 00 00 00 | *** | mov rdi, 0x0000ffff | 48 c7 c7 ff ff 00 00 |
    | mov r14, 0x00000001 | 49 c7 c6 01 00 00 00 | *** | mov r8, 0x00010000  | 49 c7 c0 00 00 01 00 |
    | mov r15, 0x00000001 | 49 c7 c7 01 00 00 00 | *** | mov r9, 0x7fffffff  | 49 c7 c1 ff ff ff 7f |
    | mov rax, 0x00000000 | 48 c7 c0 00 00 00 00 | *** | mov r10, 0x80000000 | 49 c7 c2 00 00 00 80 |
    | mov rax, 0x0000007f | 48 c7 c0 7f 00 00 00 | *** | mov r11, 0xffffffff | 49 c7 c3 ff ff ff ff |
    | mov rax, 0x00000080 | 48 c7 c0 80 00 00 00 | *** | mov r12, 0x00000000 | 49 c7 c4 00 00 00 00 |
    | mov rax, 0x000000ff | 48 c7 c0 ff 00 00 00 | *** | mov r14, 0x0000007f | 49 c7 c6 7f 00 00 00 |
    | mov rax, 0x00000100 | 48 c7 c0 00 01 00 00 | *** | mov r15, 0x00000080 | 49 c7 c7 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_mov_reg64_imm32():
    encode(MOV_REG64_IMM32)


MOV_REG64_IMM64 = """
    | --------------------------- | ----------------------------- | --- | --------------------------- | ----------------------------- |
    | instruction                 | encoding                      | *** | instruction                 | encoding                      |
    | --------------------------- | ----------------------------- | --- | --------------------------- | ----------------------------- |
    | mov rax, 0x0000000000000001 | 48 b8 01 00 00 00 00 00 00 00 | *** | mov rax, 0x0000000000010000 | 48 b8 00 00 01 00 00 00 00 00 |
    | mov rcx, 0x0000000000000001 | 48 b9 01 00 00 00 00 00 00 00 | *** | mov rax, 0x000000007fffffff | 48 b8 ff ff ff 7f 00 00 00 00 |
    | mov rdx, 0x0000000000000001 | 48 ba 01 00 00 00 00 00 00 00 | *** | mov rax, 0x0000000080000000 | 48 b8 00 00 00 80 00 00 00 00 |
    | mov rbx, 0x0000000000000001 | 48 bb 01 00 00 00 00 00 00 00 | *** | mov rax, 0x00000000ffffffff | 48 b8 ff ff ff ff 00 00 00 00 |
    | mov rsp, 0x0000000000000001 | 48 bc 01 00 00 00 00 00 00 00 | *** | mov rax, 0x0000000100000000 | 48 b8 00 00 00 00 01 00 00 00 |
    | mov rbp, 0x0000000000000001 | 48 bd 01 00 00 00 00 00 00 00 | *** | mov rax, 0x7fffffffffffffff | 48 b8 ff ff ff ff ff ff ff 7f |
    | mov rsi, 0x0000000000000001 | 48 be 01 00 00 00 00 00 00 00 | *** | mov rax, 0x8000000000000000 | 48 b8 00 00 00 00 00 00 00 80 |
    | mov rdi, 0x0000000000000001 | 48 bf 01 00 00 00 00 00 00 00 | *** | mov rax, 0xffffffffffffffff | 48 b8 ff ff ff ff ff ff ff ff |
    | mov r8, 0x0000000000000001  | 49 b8 01 00 00 00 00 00 00 00 | *** | mov rcx, 0x000000000000007f | 48 b9 7f 00 00 00 00 00 00 00 |
    | mov r9, 0x0000000000000001  | 49 b9 01 00 00 00 00 00 00 00 | *** | mov rdx, 0x0000000000000080 | 48 ba 80 00 00 00 00 00 00 00 |
    | mov r10, 0x0000000000000001 | 49 ba 01 00 00 00 00 00 00 00 | *** | mov rbx, 0x00000000000000ff | 48 bb ff 00 00 00 00 00 00 00 |
    | mov r11, 0x0000000000000001 | 49 bb 01 00 00 00 00 00 00 00 | *** | mov rsp, 0x0000000000000100 | 48 bc 00 01 00 00 00 00 00 00 |
    | mov r12, 0x0000000000000001 | 49 bc 01 00 00 00 00 00 00 00 | *** | mov rbp, 0x0000000000007fff | 48 bd ff 7f 00 00 00 00 00 00 |
    | mov r13, 0x0000000000000001 | 49 bd 01 00 00 00 00 00 00 00 | *** | mov rsi, 0x0000000000008000 | 48 be 00 80 00 00 00 00 00 00 |
    | mov r14, 0x0000000000000001 | 49 be 01 00 00 00 00 00 00 00 | *** | mov rdi, 0x000000000000ffff | 48 bf ff ff 00 00 00 00 00 00 |
    | mov r15, 0x0000000000000001 | 49 bf 01 00 00 00 00 00 00 00 | *** | mov r8, 0x0000000000010000  | 49 b8 00 00 01 00 00 00 00 00 |
    | mov rax, 0x0000000000000000 | 48 b8 00 00 00 00 00 00 00 00 | *** | mov r9, 0x000000007fffffff  | 49 b9 ff ff ff 7f 00 00 00 00 |
    | mov rax, 0x000000000000007f | 48 b8 7f 00 00 00 00 00 00 00 | *** | mov r10, 0x0000000080000000 | 49 ba 00 00 00 80 00 00 00 00 |
    | mov rax, 0x0000000000000080 | 48 b8 80 00 00 00 00 00 00 00 | *** | mov r11, 0x00000000ffffffff | 49 bb ff ff ff ff 00 00 00 00 |
    | mov rax, 0x00000000000000ff | 48 b8 ff 00 00 00 00 00 00 00 | *** | mov r12, 0x0000000100000000 | 49 bc 00 00 00 00 01 00 00 00 |
    | mov rax, 0x0000000000000100 | 48 b8 00 01 00 00 00 00 00 00 | *** | mov r13, 0x7fffffffffffffff | 49 bd ff ff ff ff ff ff ff 7f |
    | mov rax, 0x0000000000007fff | 48 b8 ff 7f 00 00 00 00 00 00 | *** | mov r14, 0x8000000000000000 | 49 be 00 00 00 00 00 00 00 80 |
    | mov rax, 0x0000000000008000 | 48 b8 00 80 00 00 00 00 00 00 | *** | mov r15, 0xffffffffffffffff | 49 bf ff ff ff ff ff ff ff ff |
    | mov rax, 0x000000000000ffff | 48 b8 ff ff 00 00 00 00 00 00 | *** | mov r15, 0xffffffffffffffff | 49 bf ff ff ff ff ff ff ff ff |
    | --------------------------- | ----------------------------- | --- | --------------------------- | ----------------------------- |
"""


def can_encode_mov_reg64_imm64():
    encode(MOV_REG64_IMM64)


MOV_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | mov rax, rcx | 48 89 c8 | *** | mov rax, r8  | 4c 89 c0 |
    | mov rcx, rcx | 48 89 c9 | *** | mov rax, r9  | 4c 89 c8 |
    | mov rdx, rcx | 48 89 ca | *** | mov rax, r10 | 4c 89 d0 |
    | mov rbx, rcx | 48 89 cb | *** | mov rax, r11 | 4c 89 d8 |
    | mov rsp, rcx | 48 89 cc | *** | mov rax, r12 | 4c 89 e0 |
    | mov rbp, rcx | 48 89 cd | *** | mov rax, r13 | 4c 89 e8 |
    | mov rsi, rcx | 48 89 ce | *** | mov rax, r14 | 4c 89 f0 |
    | mov rdi, rcx | 48 89 cf | *** | mov rax, r15 | 4c 89 f8 |
    | mov r8, rcx  | 49 89 c8 | *** | mov rcx, rdx | 48 89 d1 |
    | mov r9, rcx  | 49 89 c9 | *** | mov rdx, rbx | 48 89 da |
    | mov r10, rcx | 49 89 ca | *** | mov rbx, rsp | 48 89 e3 |
    | mov r11, rcx | 49 89 cb | *** | mov rsp, rbp | 48 89 ec |
    | mov r12, rcx | 49 89 cc | *** | mov rbp, rsi | 48 89 f5 |
    | mov r13, rcx | 49 89 cd | *** | mov rsi, rdi | 48 89 fe |
    | mov r14, rcx | 49 89 ce | *** | mov rdi, r8  | 4c 89 c7 |
    | mov r15, rcx | 49 89 cf | *** | mov r8, r9   | 4d 89 c8 |
    | mov rax, rax | 48 89 c0 | *** | mov r9, r10  | 4d 89 d1 |
    | mov rax, rdx | 48 89 d0 | *** | mov r10, r11 | 4d 89 da |
    | mov rax, rbx | 48 89 d8 | *** | mov r11, r12 | 4d 89 e3 |
    | mov rax, rsp | 48 89 e0 | *** | mov r12, r13 | 4d 89 ec |
    | mov rax, rbp | 48 89 e8 | *** | mov r13, r14 | 4d 89 f5 |
    | mov rax, rsi | 48 89 f0 | *** | mov r14, r15 | 4d 89 fe |
    | mov rax, rdi | 48 89 f8 | *** | mov r15, rax | 49 89 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_mov_reg64_reg64():
    encode(MOV_REG64_REG64)


MOV_REG64_ADDR64 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | mov rax, qword [rcx]                                              | 48 8b 01                               |
    | mov rcx, qword [rcx]                                              | 48 8b 09                               |
    | mov rdx, qword [rcx]                                              | 48 8b 11                               |
    | mov rbx, qword [rcx]                                              | 48 8b 19                               |
    | mov rsp, qword [rcx]                                              | 48 8b 21                               |
    | mov rbp, qword [rcx]                                              | 48 8b 29                               |
    | mov rsi, qword [rcx]                                              | 48 8b 31                               |
    | mov rdi, qword [rcx]                                              | 48 8b 39                               |
    | mov r8, qword [rcx]                                               | 4c 8b 01                               |
    | mov r9, qword [rcx]                                               | 4c 8b 09                               |
    | mov r10, qword [rcx]                                              | 4c 8b 11                               |
    | mov r11, qword [rcx]                                              | 4c 8b 19                               |
    | mov r12, qword [rcx]                                              | 4c 8b 21                               |
    | mov r13, qword [rcx]                                              | 4c 8b 29                               |
    | mov r14, qword [rcx]                                              | 4c 8b 31                               |
    | mov r15, qword [rcx]                                              | 4c 8b 39                               |
    | mov rax, qword [rax]                                              | 48 8b 00                               |
    | mov rax, qword [rdx]                                              | 48 8b 02                               |
    | mov rax, qword [rbx]                                              | 48 8b 03                               |
    | mov rax, qword [rsp]                                              | 48 8b 04 24                            |
    | mov rax, qword [rbp]                                              | 48 8b 45 00                            |
    | mov rax, qword [rsi]                                              | 48 8b 06                               |
    | mov rax, qword [rdi]                                              | 48 8b 07                               |
    | mov rax, qword [r8]                                               | 49 8b 00                               |
    | mov rax, qword [r9]                                               | 49 8b 01                               |
    | mov rax, qword [r10]                                              | 49 8b 02                               |
    | mov rax, qword [r11]                                              | 49 8b 03                               |
    | mov rax, qword [r12]                                              | 49 8b 04 24                            |
    | mov rax, qword [r13]                                              | 49 8b 45 00                            |
    | mov rax, qword [r14]                                              | 49 8b 06                               |
    | mov rax, qword [r15]                                              | 49 8b 07                               |
    | mov rax, qword [rax + 1 * rcx]                                    | 48 8b 04 08                            |
    | mov rax, qword [rcx + 1 * rcx]                                    | 48 8b 04 09                            |
    | mov rax, qword [rdx + 1 * rcx]                                    | 48 8b 04 0a                            |
    | mov rax, qword [rbx + 1 * rcx]                                    | 48 8b 04 0b                            |
    | mov rax, qword [rsp + 1 * rcx]                                    | 48 8b 04 0c                            |
    | mov rax, qword [rbp + 1 * rcx]                                    | 48 8b 44 0d 00                         |
    | mov rax, qword [rsi + 1 * rcx]                                    | 48 8b 04 0e                            |
    | mov rax, qword [rdi + 1 * rcx]                                    | 48 8b 04 0f                            |
    | mov rax, qword [r8 + 1 * rcx]                                     | 49 8b 04 08                            |
    | mov rax, qword [r9 + 1 * rcx]                                     | 49 8b 04 09                            |
    | mov rax, qword [r10 + 1 * rcx]                                    | 49 8b 04 0a                            |
    | mov rax, qword [r11 + 1 * rcx]                                    | 49 8b 04 0b                            |
    | mov rax, qword [r12 + 1 * rcx]                                    | 49 8b 04 0c                            |
    | mov rax, qword [r13 + 1 * rcx]                                    | 49 8b 44 0d 00                         |
    | mov rax, qword [r14 + 1 * rcx]                                    | 49 8b 04 0e                            |
    | mov rax, qword [r15 + 1 * rcx]                                    | 49 8b 04 0f                            |
    | mov rax, qword [rax + 1 * rax]                                    | 48 8b 04 00                            |
    | mov rax, qword [rax + 1 * rdx]                                    | 48 8b 04 10                            |
    | mov rax, qword [rax + 1 * rbx]                                    | 48 8b 04 18                            |
    | mov rax, qword [rax + 1 * rbp]                                    | 48 8b 04 28                            |
    | mov rax, qword [rax + 1 * rsi]                                    | 48 8b 04 30                            |
    | mov rax, qword [rax + 1 * rdi]                                    | 48 8b 04 38                            |
    | mov rax, qword [rax + 1 * r8]                                     | 4a 8b 04 00                            |
    | mov rax, qword [rax + 1 * r9]                                     | 4a 8b 04 08                            |
    | mov rax, qword [rax + 1 * r10]                                    | 4a 8b 04 10                            |
    | mov rax, qword [rax + 1 * r11]                                    | 4a 8b 04 18                            |
    | mov rax, qword [rax + 1 * r12]                                    | 4a 8b 04 20                            |
    | mov rax, qword [rax + 1 * r13]                                    | 4a 8b 04 28                            |
    | mov rax, qword [rax + 1 * r14]                                    | 4a 8b 04 30                            |
    | mov rax, qword [rax + 1 * r15]                                    | 4a 8b 04 38                            |
    | mov rax, qword [rax + 2 * rcx]                                    | 48 8b 04 48                            |
    | mov rax, qword [rax + 4 * rcx]                                    | 48 8b 04 88                            |
    | mov rax, qword [rax + 8 * rcx]                                    | 48 8b 04 c8                            |
    | mov rax, qword [r8 + 1 * r9]                                      | 4b 8b 04 08                            |
    | mov rax, qword [r8 + 2 * r9]                                      | 4b 8b 04 48                            |
    | mov rax, qword [r8 + 4 * r9]                                      | 4b 8b 04 88                            |
    | mov rax, qword [r8 + 8 * r9]                                      | 4b 8b 04 c8                            |
    | mov rax, qword [1 * rcx]                                          | 48 8b 04 0d 00 00 00 00                |
    | mov rax, qword [2 * rcx]                                          | 48 8b 04 4d 00 00 00 00                |
    | mov rax, qword [4 * rcx]                                          | 48 8b 04 8d 00 00 00 00                |
    | mov rax, qword [8 * rcx]                                          | 48 8b 04 cd 00 00 00 00                |
    | mov rax, qword [1 * r9]                                           | 4a 8b 04 0d 00 00 00 00                |
    | mov rax, qword [2 * r9]                                           | 4a 8b 04 4d 00 00 00 00                |
    | mov rax, qword [4 * r9]                                           | 4a 8b 04 8d 00 00 00 00                |
    | mov rax, qword [8 * r9]                                           | 4a 8b 04 cd 00 00 00 00                |
    | mov rax, qword [r13 + 8 * r12]                                    | 4b 8b 44 e5 00                         |
    | mov rax, qword [rsp + 4 * r15]                                    | 4a 8b 04 bc                            |
    | mov rax, qword [rax + 1 * rcx + 0x00]                             | 48 8b 44 08 00                         |
    | mov rax, qword [rax + 1 * rcx - 0x00]                             | 48 8b 44 08 00                         |
    | mov rax, qword [rax + 1 * rcx + 0x01]                             | 48 8b 44 08 01                         |
    | mov rax, qword [rax + 1 * rcx - 0x01]                             | 48 8b 44 08 ff                         |
    | mov rax, qword [rax + 1 * rcx + 0x00000001]                       | 48 8b 84 08 01 00 00 00                |
    | mov rax, qword [rax + 1 * rcx - 0x00000001]                       | 48 8b 84 08 ff ff ff ff                |
    | mov rax, qword [rax + 1 * rcx + 0x7f]                             | 48 8b 44 08 7f                         |
    | mov rax, qword [rax + 1 * rcx - 0x7f]                             | 48 8b 44 08 81                         |
    | mov rax, qword [rax + 1 * rcx + 0x80]                             | 48 8b 84 08 80 00 00 00                |
    | mov rax, qword [rax + 1 * rcx - 0x80]                             | 48 8b 44 08 80                         |
    | mov rax, qword [rax + 1 * rcx - 0x81]                             | 48 8b 84 08 7f ff ff ff                |
    | mov rax, qword [rax + 1 * rcx + 0xff]                             | 48 8b 84 08 ff 00 00 00                |
    | mov rax, qword [rax + 1 * rcx - 0xff]                             | 48 8b 84 08 01 ff ff ff                |
    | mov rax, qword [rax + 1 * rcx + 0x7fffffff]                       | 48 8b 84 08 ff ff ff 7f                |
    | mov rax, qword [rax + 1 * rcx - 0x7fffffff]                       | 48 8b 84 08 01 00 00 80                |
    | mov rax, qword [rax + 1 * rcx - 0x80000000]                       | 48 8b 84 08 00 00 00 80                |
    | mov rax, qword [r10 + 0x7f]                                       | 49 8b 42 7f                            |
    | mov rax, qword [r10 + 0x80]                                       | 49 8b 82 80 00 00 00                   |
    | mov rax, qword [r10 - 0x80]                                       | 49 8b 42 80                            |
    | mov rax, qword [r10 - 0x81]                                       | 49 8b 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov rax, qword [rel @prev5]      | 90 90 90 90 90 48 8b 05 f4 ff ff ff    |
    | .prev1: nop; mov rax, qword [rel @prev1]                          | 90 48 8b 05 f8 ff ff ff                |
    | mov rax, qword [rel @next1]; nop; .next1: nop                     | 48 8b 05 01 00 00 00 90 90             |
    | mov rax, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 8b 05 05 00 00 00 90 90 90 90 90 90 |
    | mov rcx, qword [rdx]                                              | 48 8b 0a                               |
    | mov rdx, qword [rbx]                                              | 48 8b 13                               |
    | mov rbx, qword [rsp]                                              | 48 8b 1c 24                            |
    | mov rsp, qword [rbp]                                              | 48 8b 65 00                            |
    | mov rbp, qword [rsi]                                              | 48 8b 2e                               |
    | mov rsi, qword [rdi]                                              | 48 8b 37                               |
    | mov rdi, qword [r8]                                               | 49 8b 38                               |
    | mov r8, qword [r9]                                                | 4d 8b 01                               |
    | mov r9, qword [r10]                                               | 4d 8b 0a                               |
    | mov r10, qword [r11]                                              | 4d 8b 13                               |
    | mov r11, qword [r12]                                              | 4d 8b 1c 24                            |
    | mov r12, qword [r13]                                              | 4d 8b 65 00                            |
    | mov r13, qword [r14]                                              | 4d 8b 2e                               |
    | mov r14, qword [r15]                                              | 4d 8b 37                               |
    | mov r15, qword [rax + 1 * rcx]                                    | 4c 8b 3c 08                            |
    | mov rcx, qword [rdx + 1 * rcx]                                    | 48 8b 0c 0a                            |
    | mov rdx, qword [rbx + 1 * rcx]                                    | 48 8b 14 0b                            |
    | mov rbx, qword [rsp + 1 * rcx]                                    | 48 8b 1c 0c                            |
    | mov rsp, qword [rbp + 1 * rcx]                                    | 48 8b 64 0d 00                         |
    | mov rbp, qword [rsi + 1 * rcx]                                    | 48 8b 2c 0e                            |
    | mov rsi, qword [rdi + 1 * rcx]                                    | 48 8b 34 0f                            |
    | mov rdi, qword [r8 + 1 * rcx]                                     | 49 8b 3c 08                            |
    | mov r8, qword [r9 + 1 * rcx]                                      | 4d 8b 04 09                            |
    | mov r9, qword [r10 + 1 * rcx]                                     | 4d 8b 0c 0a                            |
    | mov r10, qword [r11 + 1 * rcx]                                    | 4d 8b 14 0b                            |
    | mov r11, qword [r12 + 1 * rcx]                                    | 4d 8b 1c 0c                            |
    | mov r12, qword [r13 + 1 * rcx]                                    | 4d 8b 64 0d 00                         |
    | mov r13, qword [r14 + 1 * rcx]                                    | 4d 8b 2c 0e                            |
    | mov r14, qword [r15 + 1 * rcx]                                    | 4d 8b 34 0f                            |
    | mov r15, qword [rax + 1 * rax]                                    | 4c 8b 3c 00                            |
    | mov rcx, qword [rax + 1 * rbx]                                    | 48 8b 0c 18                            |
    | mov rdx, qword [rax + 1 * rbp]                                    | 48 8b 14 28                            |
    | mov rbx, qword [rax + 1 * rsi]                                    | 48 8b 1c 30                            |
    | mov rsp, qword [rax + 1 * rdi]                                    | 48 8b 24 38                            |
    | mov rbp, qword [rax + 1 * r8]                                     | 4a 8b 2c 00                            |
    | mov rsi, qword [rax + 1 * r9]                                     | 4a 8b 34 08                            |
    | mov rdi, qword [rax + 1 * r10]                                    | 4a 8b 3c 10                            |
    | mov r8, qword [rax + 1 * r11]                                     | 4e 8b 04 18                            |
    | mov r9, qword [rax + 1 * r12]                                     | 4e 8b 0c 20                            |
    | mov r10, qword [rax + 1 * r13]                                    | 4e 8b 14 28                            |
    | mov r11, qword [rax + 1 * r14]                                    | 4e 8b 1c 30                            |
    | mov r12, qword [rax + 1 * r15]                                    | 4e 8b 24 38                            |
    | mov r13, qword [rax + 2 * rcx]                                    | 4c 8b 2c 48                            |
    | mov r14, qword [rax + 4 * rcx]                                    | 4c 8b 34 88                            |
    | mov r15, qword [rax + 8 * rcx]                                    | 4c 8b 3c c8                            |
    | mov rcx, qword [r8 + 2 * r9]                                      | 4b 8b 0c 48                            |
    | mov rdx, qword [r8 + 4 * r9]                                      | 4b 8b 14 88                            |
    | mov rbx, qword [r8 + 8 * r9]                                      | 4b 8b 1c c8                            |
    | mov rsp, qword [1 * rcx]                                          | 48 8b 24 0d 00 00 00 00                |
    | mov rbp, qword [2 * rcx]                                          | 48 8b 2c 4d 00 00 00 00                |
    | mov rsi, qword [4 * rcx]                                          | 48 8b 34 8d 00 00 00 00                |
    | mov rdi, qword [8 * rcx]                                          | 48 8b 3c cd 00 00 00 00                |
    | mov r8, qword [1 * r9]                                            | 4e 8b 04 0d 00 00 00 00                |
    | mov r9, qword [2 * r9]                                            | 4e 8b 0c 4d 00 00 00 00                |
    | mov r10, qword [4 * r9]                                           | 4e 8b 14 8d 00 00 00 00                |
    | mov r11, qword [8 * r9]                                           | 4e 8b 1c cd 00 00 00 00                |
    | mov r12, qword [r13 + 8 * r12]                                    | 4f 8b 64 e5 00                         |
    | mov r13, qword [rsp + 4 * r15]                                    | 4e 8b 2c bc                            |
    | mov r14, qword [rax + 1 * rcx + 0x00]                             | 4c 8b 74 08 00                         |
    | mov r15, qword [rax + 1 * rcx - 0x00]                             | 4c 8b 7c 08 00                         |
    | mov rcx, qword [rax + 1 * rcx - 0x01]                             | 48 8b 4c 08 ff                         |
    | mov rdx, qword [rax + 1 * rcx + 0x00000001]                       | 48 8b 94 08 01 00 00 00                |
    | mov rbx, qword [rax + 1 * rcx - 0x00000001]                       | 48 8b 9c 08 ff ff ff ff                |
    | mov rsp, qword [rax + 1 * rcx + 0x7f]                             | 48 8b 64 08 7f                         |
    | mov rbp, qword [rax + 1 * rcx - 0x7f]                             | 48 8b 6c 08 81                         |
    | mov rsi, qword [rax + 1 * rcx + 0x80]                             | 48 8b b4 08 80 00 00 00                |
    | mov rdi, qword [rax + 1 * rcx - 0x80]                             | 48 8b 7c 08 80                         |
    | mov r8, qword [rax + 1 * rcx - 0x81]                              | 4c 8b 84 08 7f ff ff ff                |
    | mov r9, qword [rax + 1 * rcx + 0xff]                              | 4c 8b 8c 08 ff 00 00 00                |
    | mov r10, qword [rax + 1 * rcx - 0xff]                             | 4c 8b 94 08 01 ff ff ff                |
    | mov r11, qword [rax + 1 * rcx + 0x7fffffff]                       | 4c 8b 9c 08 ff ff ff 7f                |
    | mov r12, qword [rax + 1 * rcx - 0x7fffffff]                       | 4c 8b a4 08 01 00 00 80                |
    | mov r13, qword [rax + 1 * rcx - 0x80000000]                       | 4c 8b ac 08 00 00 00 80                |
    | mov r14, qword [r10 + 0x7f]                                       | 4d 8b 72 7f                            |
    | mov r15, qword [r10 + 0x80]                                       | 4d 8b ba 80 00 00 00                   |
    | mov rcx, qword [r10 - 0x81]                                       | 49 8b 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov rdx, qword [rel @prev5]      | 90 90 90 90 90 48 8b 15 f4 ff ff ff    |
    | .prev1: nop; mov rbx, qword [rel @prev1]                          | 90 48 8b 1d f8 ff ff ff                |
    | mov rsp, qword [rel @next1]; nop; .next1: nop                     | 48 8b 25 01 00 00 00 90 90             |
    | mov rbp, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 8b 2d 05 00 00 00 90 90 90 90 90 90 |
    | mov rsi, qword [rax]                                              | 48 8b 30                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_mov_reg64_addr64():
    encode(MOV_REG64_ADDR64)


MOV_REG32_IMM32 = """
    | -------------------- | ----------------- | --- | -------------------- | ----------------- |
    | instruction          | encoding          | *** | instruction          | encoding          |
    | -------------------- | ----------------- | --- | -------------------- | ----------------- |
    | mov eax, 0x00000001  | b8 01 00 00 00    | *** | mov eax, 0x00007fff  | b8 ff 7f 00 00    |
    | mov ecx, 0x00000001  | b9 01 00 00 00    | *** | mov eax, 0x00008000  | b8 00 80 00 00    |
    | mov edx, 0x00000001  | ba 01 00 00 00    | *** | mov eax, 0x0000ffff  | b8 ff ff 00 00    |
    | mov ebx, 0x00000001  | bb 01 00 00 00    | *** | mov eax, 0x00010000  | b8 00 00 01 00    |
    | mov esp, 0x00000001  | bc 01 00 00 00    | *** | mov eax, 0x7fffffff  | b8 ff ff ff 7f    |
    | mov ebp, 0x00000001  | bd 01 00 00 00    | *** | mov eax, 0x80000000  | b8 00 00 00 80    |
    | mov esi, 0x00000001  | be 01 00 00 00    | *** | mov eax, 0xffffffff  | b8 ff ff ff ff    |
    | mov edi, 0x00000001  | bf 01 00 00 00    | *** | mov ecx, 0x0000007f  | b9 7f 00 00 00    |
    | mov r8d, 0x00000001  | 41 b8 01 00 00 00 | *** | mov edx, 0x00000080  | ba 80 00 00 00    |
    | mov r9d, 0x00000001  | 41 b9 01 00 00 00 | *** | mov ebx, 0x000000ff  | bb ff 00 00 00    |
    | mov r10d, 0x00000001 | 41 ba 01 00 00 00 | *** | mov esp, 0x00000100  | bc 00 01 00 00    |
    | mov r11d, 0x00000001 | 41 bb 01 00 00 00 | *** | mov ebp, 0x00007fff  | bd ff 7f 00 00    |
    | mov r12d, 0x00000001 | 41 bc 01 00 00 00 | *** | mov esi, 0x00008000  | be 00 80 00 00    |
    | mov r13d, 0x00000001 | 41 bd 01 00 00 00 | *** | mov edi, 0x0000ffff  | bf ff ff 00 00    |
    | mov r14d, 0x00000001 | 41 be 01 00 00 00 | *** | mov r8d, 0x00010000  | 41 b8 00 00 01 00 |
    | mov r15d, 0x00000001 | 41 bf 01 00 00 00 | *** | mov r9d, 0x7fffffff  | 41 b9 ff ff ff 7f |
    | mov eax, 0x00000000  | b8 00 00 00 00    | *** | mov r10d, 0x80000000 | 41 ba 00 00 00 80 |
    | mov eax, 0x0000007f  | b8 7f 00 00 00    | *** | mov r11d, 0xffffffff | 41 bb ff ff ff ff |
    | mov eax, 0x00000080  | b8 80 00 00 00    | *** | mov r12d, 0x00000000 | 41 bc 00 00 00 00 |
    | mov eax, 0x000000ff  | b8 ff 00 00 00    | *** | mov r14d, 0x0000007f | 41 be 7f 00 00 00 |
    | mov eax, 0x00000100  | b8 00 01 00 00    | *** | mov r15d, 0x00000080 | 41 bf 80 00 00 00 |
    | -------------------- | ----------------- | --- | -------------------- | ----------------- |
"""


def can_encode_mov_reg32_imm32():
    encode(MOV_REG32_IMM32)


MOV_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | mov eax, ecx   | 89 c8    | *** | mov eax, r8d   | 44 89 c0 |
    | mov ecx, ecx   | 89 c9    | *** | mov eax, r9d   | 44 89 c8 |
    | mov edx, ecx   | 89 ca    | *** | mov eax, r10d  | 44 89 d0 |
    | mov ebx, ecx   | 89 cb    | *** | mov eax, r11d  | 44 89 d8 |
    | mov esp, ecx   | 89 cc    | *** | mov eax, r12d  | 44 89 e0 |
    | mov ebp, ecx   | 89 cd    | *** | mov eax, r13d  | 44 89 e8 |
    | mov esi, ecx   | 89 ce    | *** | mov eax, r14d  | 44 89 f0 |
    | mov edi, ecx   | 89 cf    | *** | mov eax, r15d  | 44 89 f8 |
    | mov r8d, ecx   | 41 89 c8 | *** | mov ecx, edx   | 89 d1    |
    | mov r9d, ecx   | 41 89 c9 | *** | mov edx, ebx   | 89 da    |
    | mov r10d, ecx  | 41 89 ca | *** | mov ebx, esp   | 89 e3    |
    | mov r11d, ecx  | 41 89 cb | *** | mov esp, ebp   | 89 ec    |
    | mov r12d, ecx  | 41 89 cc | *** | mov ebp, esi   | 89 f5    |
    | mov r13d, ecx  | 41 89 cd | *** | mov esi, edi   | 89 fe    |
    | mov r14d, ecx  | 41 89 ce | *** | mov edi, r8d   | 44 89 c7 |
    | mov r15d, ecx  | 41 89 cf | *** | mov r8d, r9d   | 45 89 c8 |
    | mov eax, eax   | 89 c0    | *** | mov r9d, r10d  | 45 89 d1 |
    | mov eax, edx   | 89 d0    | *** | mov r10d, r11d | 45 89 da |
    | mov eax, ebx   | 89 d8    | *** | mov r11d, r12d | 45 89 e3 |
    | mov eax, esp   | 89 e0    | *** | mov r12d, r13d | 45 89 ec |
    | mov eax, ebp   | 89 e8    | *** | mov r13d, r14d | 45 89 f5 |
    | mov eax, esi   | 89 f0    | *** | mov r14d, r15d | 45 89 fe |
    | mov eax, edi   | 89 f8    | *** | mov r15d, eax  | 41 89 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_mov_reg32_reg32():
    encode(MOV_REG32_REG32)


MOV_REG32_ADDR32 = """
    | ----------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                       | encoding                            |
    | ----------------------------------------------------------------- | ----------------------------------- |
    | mov eax, dword [rcx]                                              | 8b 01                               |
    | mov ecx, dword [rcx]                                              | 8b 09                               |
    | mov edx, dword [rcx]                                              | 8b 11                               |
    | mov ebx, dword [rcx]                                              | 8b 19                               |
    | mov esp, dword [rcx]                                              | 8b 21                               |
    | mov ebp, dword [rcx]                                              | 8b 29                               |
    | mov esi, dword [rcx]                                              | 8b 31                               |
    | mov edi, dword [rcx]                                              | 8b 39                               |
    | mov r8d, dword [rcx]                                              | 44 8b 01                            |
    | mov r9d, dword [rcx]                                              | 44 8b 09                            |
    | mov r10d, dword [rcx]                                             | 44 8b 11                            |
    | mov r11d, dword [rcx]                                             | 44 8b 19                            |
    | mov r12d, dword [rcx]                                             | 44 8b 21                            |
    | mov r13d, dword [rcx]                                             | 44 8b 29                            |
    | mov r14d, dword [rcx]                                             | 44 8b 31                            |
    | mov r15d, dword [rcx]                                             | 44 8b 39                            |
    | mov eax, dword [rax]                                              | 8b 00                               |
    | mov eax, dword [rdx]                                              | 8b 02                               |
    | mov eax, dword [rbx]                                              | 8b 03                               |
    | mov eax, dword [rsp]                                              | 8b 04 24                            |
    | mov eax, dword [rbp]                                              | 8b 45 00                            |
    | mov eax, dword [rsi]                                              | 8b 06                               |
    | mov eax, dword [rdi]                                              | 8b 07                               |
    | mov eax, dword [r8]                                               | 41 8b 00                            |
    | mov eax, dword [r9]                                               | 41 8b 01                            |
    | mov eax, dword [r10]                                              | 41 8b 02                            |
    | mov eax, dword [r11]                                              | 41 8b 03                            |
    | mov eax, dword [r12]                                              | 41 8b 04 24                         |
    | mov eax, dword [r13]                                              | 41 8b 45 00                         |
    | mov eax, dword [r14]                                              | 41 8b 06                            |
    | mov eax, dword [r15]                                              | 41 8b 07                            |
    | mov eax, dword [rax + 1 * rcx]                                    | 8b 04 08                            |
    | mov eax, dword [rcx + 1 * rcx]                                    | 8b 04 09                            |
    | mov eax, dword [rdx + 1 * rcx]                                    | 8b 04 0a                            |
    | mov eax, dword [rbx + 1 * rcx]                                    | 8b 04 0b                            |
    | mov eax, dword [rsp + 1 * rcx]                                    | 8b 04 0c                            |
    | mov eax, dword [rbp + 1 * rcx]                                    | 8b 44 0d 00                         |
    | mov eax, dword [rsi + 1 * rcx]                                    | 8b 04 0e                            |
    | mov eax, dword [rdi + 1 * rcx]                                    | 8b 04 0f                            |
    | mov eax, dword [r8 + 1 * rcx]                                     | 41 8b 04 08                         |
    | mov eax, dword [r9 + 1 * rcx]                                     | 41 8b 04 09                         |
    | mov eax, dword [r10 + 1 * rcx]                                    | 41 8b 04 0a                         |
    | mov eax, dword [r11 + 1 * rcx]                                    | 41 8b 04 0b                         |
    | mov eax, dword [r12 + 1 * rcx]                                    | 41 8b 04 0c                         |
    | mov eax, dword [r13 + 1 * rcx]                                    | 41 8b 44 0d 00                      |
    | mov eax, dword [r14 + 1 * rcx]                                    | 41 8b 04 0e                         |
    | mov eax, dword [r15 + 1 * rcx]                                    | 41 8b 04 0f                         |
    | mov eax, dword [rax + 1 * rax]                                    | 8b 04 00                            |
    | mov eax, dword [rax + 1 * rdx]                                    | 8b 04 10                            |
    | mov eax, dword [rax + 1 * rbx]                                    | 8b 04 18                            |
    | mov eax, dword [rax + 1 * rbp]                                    | 8b 04 28                            |
    | mov eax, dword [rax + 1 * rsi]                                    | 8b 04 30                            |
    | mov eax, dword [rax + 1 * rdi]                                    | 8b 04 38                            |
    | mov eax, dword [rax + 1 * r8]                                     | 42 8b 04 00                         |
    | mov eax, dword [rax + 1 * r9]                                     | 42 8b 04 08                         |
    | mov eax, dword [rax + 1 * r10]                                    | 42 8b 04 10                         |
    | mov eax, dword [rax + 1 * r11]                                    | 42 8b 04 18                         |
    | mov eax, dword [rax + 1 * r12]                                    | 42 8b 04 20                         |
    | mov eax, dword [rax + 1 * r13]                                    | 42 8b 04 28                         |
    | mov eax, dword [rax + 1 * r14]                                    | 42 8b 04 30                         |
    | mov eax, dword [rax + 1 * r15]                                    | 42 8b 04 38                         |
    | mov eax, dword [rax + 2 * rcx]                                    | 8b 04 48                            |
    | mov eax, dword [rax + 4 * rcx]                                    | 8b 04 88                            |
    | mov eax, dword [rax + 8 * rcx]                                    | 8b 04 c8                            |
    | mov eax, dword [r8 + 1 * r9]                                      | 43 8b 04 08                         |
    | mov eax, dword [r8 + 2 * r9]                                      | 43 8b 04 48                         |
    | mov eax, dword [r8 + 4 * r9]                                      | 43 8b 04 88                         |
    | mov eax, dword [r8 + 8 * r9]                                      | 43 8b 04 c8                         |
    | mov eax, dword [1 * rcx]                                          | 8b 04 0d 00 00 00 00                |
    | mov eax, dword [2 * rcx]                                          | 8b 04 4d 00 00 00 00                |
    | mov eax, dword [4 * rcx]                                          | 8b 04 8d 00 00 00 00                |
    | mov eax, dword [8 * rcx]                                          | 8b 04 cd 00 00 00 00                |
    | mov eax, dword [1 * r9]                                           | 42 8b 04 0d 00 00 00 00             |
    | mov eax, dword [2 * r9]                                           | 42 8b 04 4d 00 00 00 00             |
    | mov eax, dword [4 * r9]                                           | 42 8b 04 8d 00 00 00 00             |
    | mov eax, dword [8 * r9]                                           | 42 8b 04 cd 00 00 00 00             |
    | mov eax, dword [r13 + 8 * r12]                                    | 43 8b 44 e5 00                      |
    | mov eax, dword [rsp + 4 * r15]                                    | 42 8b 04 bc                         |
    | mov eax, dword [rax + 1 * rcx + 0x00]                             | 8b 44 08 00                         |
    | mov eax, dword [rax + 1 * rcx - 0x00]                             | 8b 44 08 00                         |
    | mov eax, dword [rax + 1 * rcx + 0x01]                             | 8b 44 08 01                         |
    | mov eax, dword [rax + 1 * rcx - 0x01]                             | 8b 44 08 ff                         |
    | mov eax, dword [rax + 1 * rcx + 0x00000001]                       | 8b 84 08 01 00 00 00                |
    | mov eax, dword [rax + 1 * rcx - 0x00000001]                       | 8b 84 08 ff ff ff ff                |
    | mov eax, dword [rax + 1 * rcx + 0x7f]                             | 8b 44 08 7f                         |
    | mov eax, dword [rax + 1 * rcx - 0x7f]                             | 8b 44 08 81                         |
    | mov eax, dword [rax + 1 * rcx + 0x80]                             | 8b 84 08 80 00 00 00                |
    | mov eax, dword [rax + 1 * rcx - 0x80]                             | 8b 44 08 80                         |
    | mov eax, dword [rax + 1 * rcx - 0x81]                             | 8b 84 08 7f ff ff ff                |
    | mov eax, dword [rax + 1 * rcx + 0xff]                             | 8b 84 08 ff 00 00 00                |
    | mov eax, dword [rax + 1 * rcx - 0xff]                             | 8b 84 08 01 ff ff ff                |
    | mov eax, dword [rax + 1 * rcx + 0x7fffffff]                       | 8b 84 08 ff ff ff 7f                |
    | mov eax, dword [rax + 1 * rcx - 0x7fffffff]                       | 8b 84 08 01 00 00 80                |
    | mov eax, dword [rax + 1 * rcx - 0x80000000]                       | 8b 84 08 00 00 00 80                |
    | mov eax, dword [r10 + 0x7f]                                       | 41 8b 42 7f                         |
    | mov eax, dword [r10 + 0x80]                                       | 41 8b 82 80 00 00 00                |
    | mov eax, dword [r10 - 0x80]                                       | 41 8b 42 80                         |
    | mov eax, dword [r10 - 0x81]                                       | 41 8b 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov eax, dword [rel @prev5]      | 90 90 90 90 90 8b 05 f5 ff ff ff    |
    | .prev1: nop; mov eax, dword [rel @prev1]                          | 90 8b 05 f9 ff ff ff                |
    | mov eax, dword [rel @next1]; nop; .next1: nop                     | 8b 05 01 00 00 00 90 90             |
    | mov eax, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 8b 05 05 00 00 00 90 90 90 90 90 90 |
    | mov ecx, dword [rdx]                                              | 8b 0a                               |
    | mov edx, dword [rbx]                                              | 8b 13                               |
    | mov ebx, dword [rsp]                                              | 8b 1c 24                            |
    | mov esp, dword [rbp]                                              | 8b 65 00                            |
    | mov ebp, dword [rsi]                                              | 8b 2e                               |
    | mov esi, dword [rdi]                                              | 8b 37                               |
    | mov edi, dword [r8]                                               | 41 8b 38                            |
    | mov r8d, dword [r9]                                               | 45 8b 01                            |
    | mov r9d, dword [r10]                                              | 45 8b 0a                            |
    | mov r10d, dword [r11]                                             | 45 8b 13                            |
    | mov r11d, dword [r12]                                             | 45 8b 1c 24                         |
    | mov r12d, dword [r13]                                             | 45 8b 65 00                         |
    | mov r13d, dword [r14]                                             | 45 8b 2e                            |
    | mov r14d, dword [r15]                                             | 45 8b 37                            |
    | mov r15d, dword [rax + 1 * rcx]                                   | 44 8b 3c 08                         |
    | mov ecx, dword [rdx + 1 * rcx]                                    | 8b 0c 0a                            |
    | mov edx, dword [rbx + 1 * rcx]                                    | 8b 14 0b                            |
    | mov ebx, dword [rsp + 1 * rcx]                                    | 8b 1c 0c                            |
    | mov esp, dword [rbp + 1 * rcx]                                    | 8b 64 0d 00                         |
    | mov ebp, dword [rsi + 1 * rcx]                                    | 8b 2c 0e                            |
    | mov esi, dword [rdi + 1 * rcx]                                    | 8b 34 0f                            |
    | mov edi, dword [r8 + 1 * rcx]                                     | 41 8b 3c 08                         |
    | mov r8d, dword [r9 + 1 * rcx]                                     | 45 8b 04 09                         |
    | mov r9d, dword [r10 + 1 * rcx]                                    | 45 8b 0c 0a                         |
    | mov r10d, dword [r11 + 1 * rcx]                                   | 45 8b 14 0b                         |
    | mov r11d, dword [r12 + 1 * rcx]                                   | 45 8b 1c 0c                         |
    | mov r12d, dword [r13 + 1 * rcx]                                   | 45 8b 64 0d 00                      |
    | mov r13d, dword [r14 + 1 * rcx]                                   | 45 8b 2c 0e                         |
    | mov r14d, dword [r15 + 1 * rcx]                                   | 45 8b 34 0f                         |
    | mov r15d, dword [rax + 1 * rax]                                   | 44 8b 3c 00                         |
    | mov ecx, dword [rax + 1 * rbx]                                    | 8b 0c 18                            |
    | mov edx, dword [rax + 1 * rbp]                                    | 8b 14 28                            |
    | mov ebx, dword [rax + 1 * rsi]                                    | 8b 1c 30                            |
    | mov esp, dword [rax + 1 * rdi]                                    | 8b 24 38                            |
    | mov ebp, dword [rax + 1 * r8]                                     | 42 8b 2c 00                         |
    | mov esi, dword [rax + 1 * r9]                                     | 42 8b 34 08                         |
    | mov edi, dword [rax + 1 * r10]                                    | 42 8b 3c 10                         |
    | mov r8d, dword [rax + 1 * r11]                                    | 46 8b 04 18                         |
    | mov r9d, dword [rax + 1 * r12]                                    | 46 8b 0c 20                         |
    | mov r10d, dword [rax + 1 * r13]                                   | 46 8b 14 28                         |
    | mov r11d, dword [rax + 1 * r14]                                   | 46 8b 1c 30                         |
    | mov r12d, dword [rax + 1 * r15]                                   | 46 8b 24 38                         |
    | mov r13d, dword [rax + 2 * rcx]                                   | 44 8b 2c 48                         |
    | mov r14d, dword [rax + 4 * rcx]                                   | 44 8b 34 88                         |
    | mov r15d, dword [rax + 8 * rcx]                                   | 44 8b 3c c8                         |
    | mov ecx, dword [r8 + 2 * r9]                                      | 43 8b 0c 48                         |
    | mov edx, dword [r8 + 4 * r9]                                      | 43 8b 14 88                         |
    | mov ebx, dword [r8 + 8 * r9]                                      | 43 8b 1c c8                         |
    | mov esp, dword [1 * rcx]                                          | 8b 24 0d 00 00 00 00                |
    | mov ebp, dword [2 * rcx]                                          | 8b 2c 4d 00 00 00 00                |
    | mov esi, dword [4 * rcx]                                          | 8b 34 8d 00 00 00 00                |
    | mov edi, dword [8 * rcx]                                          | 8b 3c cd 00 00 00 00                |
    | mov r8d, dword [1 * r9]                                           | 46 8b 04 0d 00 00 00 00             |
    | mov r9d, dword [2 * r9]                                           | 46 8b 0c 4d 00 00 00 00             |
    | mov r10d, dword [4 * r9]                                          | 46 8b 14 8d 00 00 00 00             |
    | mov r11d, dword [8 * r9]                                          | 46 8b 1c cd 00 00 00 00             |
    | mov r12d, dword [r13 + 8 * r12]                                   | 47 8b 64 e5 00                      |
    | mov r13d, dword [rsp + 4 * r15]                                   | 46 8b 2c bc                         |
    | mov r14d, dword [rax + 1 * rcx + 0x00]                            | 44 8b 74 08 00                      |
    | mov r15d, dword [rax + 1 * rcx - 0x00]                            | 44 8b 7c 08 00                      |
    | mov ecx, dword [rax + 1 * rcx - 0x01]                             | 8b 4c 08 ff                         |
    | mov edx, dword [rax + 1 * rcx + 0x00000001]                       | 8b 94 08 01 00 00 00                |
    | mov ebx, dword [rax + 1 * rcx - 0x00000001]                       | 8b 9c 08 ff ff ff ff                |
    | mov esp, dword [rax + 1 * rcx + 0x7f]                             | 8b 64 08 7f                         |
    | mov ebp, dword [rax + 1 * rcx - 0x7f]                             | 8b 6c 08 81                         |
    | mov esi, dword [rax + 1 * rcx + 0x80]                             | 8b b4 08 80 00 00 00                |
    | mov edi, dword [rax + 1 * rcx - 0x80]                             | 8b 7c 08 80                         |
    | mov r8d, dword [rax + 1 * rcx - 0x81]                             | 44 8b 84 08 7f ff ff ff             |
    | mov r9d, dword [rax + 1 * rcx + 0xff]                             | 44 8b 8c 08 ff 00 00 00             |
    | mov r10d, dword [rax + 1 * rcx - 0xff]                            | 44 8b 94 08 01 ff ff ff             |
    | mov r11d, dword [rax + 1 * rcx + 0x7fffffff]                      | 44 8b 9c 08 ff ff ff 7f             |
    | mov r12d, dword [rax + 1 * rcx - 0x7fffffff]                      | 44 8b a4 08 01 00 00 80             |
    | mov r13d, dword [rax + 1 * rcx - 0x80000000]                      | 44 8b ac 08 00 00 00 80             |
    | mov r14d, dword [r10 + 0x7f]                                      | 45 8b 72 7f                         |
    | mov r15d, dword [r10 + 0x80]                                      | 45 8b ba 80 00 00 00                |
    | mov ecx, dword [r10 - 0x81]                                       | 41 8b 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov edx, dword [rel @prev5]      | 90 90 90 90 90 8b 15 f5 ff ff ff    |
    | .prev1: nop; mov ebx, dword [rel @prev1]                          | 90 8b 1d f9 ff ff ff                |
    | mov esp, dword [rel @next1]; nop; .next1: nop                     | 8b 25 01 00 00 00 90 90             |
    | mov ebp, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 8b 2d 05 00 00 00 90 90 90 90 90 90 |
    | mov esi, dword [rax]                                              | 8b 30                               |
    | ----------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_mov_reg32_addr32():
    encode(MOV_REG32_ADDR32)


MOV_REG16_IMM16 = """
    | ---------------- | -------------- | --- | ---------------- | -------------- |
    | instruction      | encoding       | *** | instruction      | encoding       |
    | ---------------- | -------------- | --- | ---------------- | -------------- |
    | mov ax, 0x0001   | 66 b8 01 00    | *** | mov ax, 0x00ff   | 66 b8 ff 00    |
    | mov cx, 0x0001   | 66 b9 01 00    | *** | mov ax, 0x0100   | 66 b8 00 01    |
    | mov dx, 0x0001   | 66 ba 01 00    | *** | mov ax, 0x7fff   | 66 b8 ff 7f    |
    | mov bx, 0x0001   | 66 bb 01 00    | *** | mov ax, 0x8000   | 66 b8 00 80    |
    | mov sp, 0x0001   | 66 bc 01 00    | *** | mov ax, 0xffff   | 66 b8 ff ff    |
    | mov bp, 0x0001   | 66 bd 01 00    | *** | mov cx, 0x007f   | 66 b9 7f 00    |
    | mov si, 0x0001   | 66 be 01 00    | *** | mov dx, 0x0080   | 66 ba 80 00    |
    | mov di, 0x0001   | 66 bf 01 00    | *** | mov bx, 0x00ff   | 66 bb ff 00    |
    | mov r8w, 0x0001  | 66 41 b8 01 00 | *** | mov sp, 0x0100   | 66 bc 00 01    |
    | mov r9w, 0x0001  | 66 41 b9 01 00 | *** | mov bp, 0x7fff   | 66 bd ff 7f    |
    | mov r10w, 0x0001 | 66 41 ba 01 00 | *** | mov si, 0x8000   | 66 be 00 80    |
    | mov r11w, 0x0001 | 66 41 bb 01 00 | *** | mov di, 0xffff   | 66 bf ff ff    |
    | mov r12w, 0x0001 | 66 41 bc 01 00 | *** | mov r8w, 0x0000  | 66 41 b8 00 00 |
    | mov r13w, 0x0001 | 66 41 bd 01 00 | *** | mov r10w, 0x007f | 66 41 ba 7f 00 |
    | mov r14w, 0x0001 | 66 41 be 01 00 | *** | mov r11w, 0x0080 | 66 41 bb 80 00 |
    | mov r15w, 0x0001 | 66 41 bf 01 00 | *** | mov r12w, 0x00ff | 66 41 bc ff 00 |
    | mov ax, 0x0000   | 66 b8 00 00    | *** | mov r13w, 0x0100 | 66 41 bd 00 01 |
    | mov ax, 0x007f   | 66 b8 7f 00    | *** | mov r14w, 0x7fff | 66 41 be ff 7f |
    | mov ax, 0x0080   | 66 b8 80 00    | *** | mov r15w, 0x8000 | 66 41 bf 00 80 |
    | ---------------- | -------------- | --- | ---------------- | -------------- |
"""


def can_encode_mov_reg16_imm16():
    encode(MOV_REG16_IMM16)


MOV_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | mov ax, cx     | 66 89 c8    | *** | mov ax, r8w    | 66 44 89 c0 |
    | mov cx, cx     | 66 89 c9    | *** | mov ax, r9w    | 66 44 89 c8 |
    | mov dx, cx     | 66 89 ca    | *** | mov ax, r10w   | 66 44 89 d0 |
    | mov bx, cx     | 66 89 cb    | *** | mov ax, r11w   | 66 44 89 d8 |
    | mov sp, cx     | 66 89 cc    | *** | mov ax, r12w   | 66 44 89 e0 |
    | mov bp, cx     | 66 89 cd    | *** | mov ax, r13w   | 66 44 89 e8 |
    | mov si, cx     | 66 89 ce    | *** | mov ax, r14w   | 66 44 89 f0 |
    | mov di, cx     | 66 89 cf    | *** | mov ax, r15w   | 66 44 89 f8 |
    | mov r8w, cx    | 66 41 89 c8 | *** | mov cx, dx     | 66 89 d1    |
    | mov r9w, cx    | 66 41 89 c9 | *** | mov dx, bx     | 66 89 da    |
    | mov r10w, cx   | 66 41 89 ca | *** | mov bx, sp     | 66 89 e3    |
    | mov r11w, cx   | 66 41 89 cb | *** | mov sp, bp     | 66 89 ec    |
    | mov r12w, cx   | 66 41 89 cc | *** | mov bp, si     | 66 89 f5    |
    | mov r13w, cx   | 66 41 89 cd | *** | mov si, di     | 66 89 fe    |
    | mov r14w, cx   | 66 41 89 ce | *** | mov di, r8w    | 66 44 89 c7 |
    | mov r15w, cx   | 66 41 89 cf | *** | mov r8w, r9w   | 66 45 89 c8 |
    | mov ax, ax     | 66 89 c0    | *** | mov r9w, r10w  | 66 45 89 d1 |
    | mov ax, dx     | 66 89 d0    | *** | mov r10w, r11w | 66 45 89 da |
    | mov ax, bx     | 66 89 d8    | *** | mov r11w, r12w | 66 45 89 e3 |
    | mov ax, sp     | 66 89 e0    | *** | mov r12w, r13w | 66 45 89 ec |
    | mov ax, bp     | 66 89 e8    | *** | mov r13w, r14w | 66 45 89 f5 |
    | mov ax, si     | 66 89 f0    | *** | mov r14w, r15w | 66 45 89 fe |
    | mov ax, di     | 66 89 f8    | *** | mov r15w, ax   | 66 41 89 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_mov_reg16_reg16():
    encode(MOV_REG16_REG16)


MOV_REG16_ADDR16 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | mov ax, word [rcx]                                              | 66 8b 01                               |
    | mov cx, word [rcx]                                              | 66 8b 09                               |
    | mov dx, word [rcx]                                              | 66 8b 11                               |
    | mov bx, word [rcx]                                              | 66 8b 19                               |
    | mov sp, word [rcx]                                              | 66 8b 21                               |
    | mov bp, word [rcx]                                              | 66 8b 29                               |
    | mov si, word [rcx]                                              | 66 8b 31                               |
    | mov di, word [rcx]                                              | 66 8b 39                               |
    | mov r8w, word [rcx]                                             | 66 44 8b 01                            |
    | mov r9w, word [rcx]                                             | 66 44 8b 09                            |
    | mov r10w, word [rcx]                                            | 66 44 8b 11                            |
    | mov r11w, word [rcx]                                            | 66 44 8b 19                            |
    | mov r12w, word [rcx]                                            | 66 44 8b 21                            |
    | mov r13w, word [rcx]                                            | 66 44 8b 29                            |
    | mov r14w, word [rcx]                                            | 66 44 8b 31                            |
    | mov r15w, word [rcx]                                            | 66 44 8b 39                            |
    | mov ax, word [rax]                                              | 66 8b 00                               |
    | mov ax, word [rdx]                                              | 66 8b 02                               |
    | mov ax, word [rbx]                                              | 66 8b 03                               |
    | mov ax, word [rsp]                                              | 66 8b 04 24                            |
    | mov ax, word [rbp]                                              | 66 8b 45 00                            |
    | mov ax, word [rsi]                                              | 66 8b 06                               |
    | mov ax, word [rdi]                                              | 66 8b 07                               |
    | mov ax, word [r8]                                               | 66 41 8b 00                            |
    | mov ax, word [r9]                                               | 66 41 8b 01                            |
    | mov ax, word [r10]                                              | 66 41 8b 02                            |
    | mov ax, word [r11]                                              | 66 41 8b 03                            |
    | mov ax, word [r12]                                              | 66 41 8b 04 24                         |
    | mov ax, word [r13]                                              | 66 41 8b 45 00                         |
    | mov ax, word [r14]                                              | 66 41 8b 06                            |
    | mov ax, word [r15]                                              | 66 41 8b 07                            |
    | mov ax, word [rax + 1 * rcx]                                    | 66 8b 04 08                            |
    | mov ax, word [rcx + 1 * rcx]                                    | 66 8b 04 09                            |
    | mov ax, word [rdx + 1 * rcx]                                    | 66 8b 04 0a                            |
    | mov ax, word [rbx + 1 * rcx]                                    | 66 8b 04 0b                            |
    | mov ax, word [rsp + 1 * rcx]                                    | 66 8b 04 0c                            |
    | mov ax, word [rbp + 1 * rcx]                                    | 66 8b 44 0d 00                         |
    | mov ax, word [rsi + 1 * rcx]                                    | 66 8b 04 0e                            |
    | mov ax, word [rdi + 1 * rcx]                                    | 66 8b 04 0f                            |
    | mov ax, word [r8 + 1 * rcx]                                     | 66 41 8b 04 08                         |
    | mov ax, word [r9 + 1 * rcx]                                     | 66 41 8b 04 09                         |
    | mov ax, word [r10 + 1 * rcx]                                    | 66 41 8b 04 0a                         |
    | mov ax, word [r11 + 1 * rcx]                                    | 66 41 8b 04 0b                         |
    | mov ax, word [r12 + 1 * rcx]                                    | 66 41 8b 04 0c                         |
    | mov ax, word [r13 + 1 * rcx]                                    | 66 41 8b 44 0d 00                      |
    | mov ax, word [r14 + 1 * rcx]                                    | 66 41 8b 04 0e                         |
    | mov ax, word [r15 + 1 * rcx]                                    | 66 41 8b 04 0f                         |
    | mov ax, word [rax + 1 * rax]                                    | 66 8b 04 00                            |
    | mov ax, word [rax + 1 * rdx]                                    | 66 8b 04 10                            |
    | mov ax, word [rax + 1 * rbx]                                    | 66 8b 04 18                            |
    | mov ax, word [rax + 1 * rbp]                                    | 66 8b 04 28                            |
    | mov ax, word [rax + 1 * rsi]                                    | 66 8b 04 30                            |
    | mov ax, word [rax + 1 * rdi]                                    | 66 8b 04 38                            |
    | mov ax, word [rax + 1 * r8]                                     | 66 42 8b 04 00                         |
    | mov ax, word [rax + 1 * r9]                                     | 66 42 8b 04 08                         |
    | mov ax, word [rax + 1 * r10]                                    | 66 42 8b 04 10                         |
    | mov ax, word [rax + 1 * r11]                                    | 66 42 8b 04 18                         |
    | mov ax, word [rax + 1 * r12]                                    | 66 42 8b 04 20                         |
    | mov ax, word [rax + 1 * r13]                                    | 66 42 8b 04 28                         |
    | mov ax, word [rax + 1 * r14]                                    | 66 42 8b 04 30                         |
    | mov ax, word [rax + 1 * r15]                                    | 66 42 8b 04 38                         |
    | mov ax, word [rax + 2 * rcx]                                    | 66 8b 04 48                            |
    | mov ax, word [rax + 4 * rcx]                                    | 66 8b 04 88                            |
    | mov ax, word [rax + 8 * rcx]                                    | 66 8b 04 c8                            |
    | mov ax, word [r8 + 1 * r9]                                      | 66 43 8b 04 08                         |
    | mov ax, word [r8 + 2 * r9]                                      | 66 43 8b 04 48                         |
    | mov ax, word [r8 + 4 * r9]                                      | 66 43 8b 04 88                         |
    | mov ax, word [r8 + 8 * r9]                                      | 66 43 8b 04 c8                         |
    | mov ax, word [1 * rcx]                                          | 66 8b 04 0d 00 00 00 00                |
    | mov ax, word [2 * rcx]                                          | 66 8b 04 4d 00 00 00 00                |
    | mov ax, word [4 * rcx]                                          | 66 8b 04 8d 00 00 00 00                |
    | mov ax, word [8 * rcx]                                          | 66 8b 04 cd 00 00 00 00                |
    | mov ax, word [1 * r9]                                           | 66 42 8b 04 0d 00 00 00 00             |
    | mov ax, word [2 * r9]                                           | 66 42 8b 04 4d 00 00 00 00             |
    | mov ax, word [4 * r9]                                           | 66 42 8b 04 8d 00 00 00 00             |
    | mov ax, word [8 * r9]                                           | 66 42 8b 04 cd 00 00 00 00             |
    | mov ax, word [r13 + 8 * r12]                                    | 66 43 8b 44 e5 00                      |
    | mov ax, word [rsp + 4 * r15]                                    | 66 42 8b 04 bc                         |
    | mov ax, word [rax + 1 * rcx + 0x00]                             | 66 8b 44 08 00                         |
    | mov ax, word [rax + 1 * rcx - 0x00]                             | 66 8b 44 08 00                         |
    | mov ax, word [rax + 1 * rcx + 0x01]                             | 66 8b 44 08 01                         |
    | mov ax, word [rax + 1 * rcx - 0x01]                             | 66 8b 44 08 ff                         |
    | mov ax, word [rax + 1 * rcx + 0x00000001]                       | 66 8b 84 08 01 00 00 00                |
    | mov ax, word [rax + 1 * rcx - 0x00000001]                       | 66 8b 84 08 ff ff ff ff                |
    | mov ax, word [rax + 1 * rcx + 0x7f]                             | 66 8b 44 08 7f                         |
    | mov ax, word [rax + 1 * rcx - 0x7f]                             | 66 8b 44 08 81                         |
    | mov ax, word [rax + 1 * rcx + 0x80]                             | 66 8b 84 08 80 00 00 00                |
    | mov ax, word [rax + 1 * rcx - 0x80]                             | 66 8b 44 08 80                         |
    | mov ax, word [rax + 1 * rcx - 0x81]                             | 66 8b 84 08 7f ff ff ff                |
    | mov ax, word [rax + 1 * rcx + 0xff]                             | 66 8b 84 08 ff 00 00 00                |
    | mov ax, word [rax + 1 * rcx - 0xff]                             | 66 8b 84 08 01 ff ff ff                |
    | mov ax, word [rax + 1 * rcx + 0x7fffffff]                       | 66 8b 84 08 ff ff ff 7f                |
    | mov ax, word [rax + 1 * rcx - 0x7fffffff]                       | 66 8b 84 08 01 00 00 80                |
    | mov ax, word [rax + 1 * rcx - 0x80000000]                       | 66 8b 84 08 00 00 00 80                |
    | mov ax, word [r10 + 0x7f]                                       | 66 41 8b 42 7f                         |
    | mov ax, word [r10 + 0x80]                                       | 66 41 8b 82 80 00 00 00                |
    | mov ax, word [r10 - 0x80]                                       | 66 41 8b 42 80                         |
    | mov ax, word [r10 - 0x81]                                       | 66 41 8b 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov ax, word [rel @prev5]      | 90 90 90 90 90 66 8b 05 f4 ff ff ff    |
    | .prev1: nop; mov ax, word [rel @prev1]                          | 90 66 8b 05 f8 ff ff ff                |
    | mov ax, word [rel @next1]; nop; .next1: nop                     | 66 8b 05 01 00 00 00 90 90             |
    | mov ax, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 8b 05 05 00 00 00 90 90 90 90 90 90 |
    | mov cx, word [rdx]                                              | 66 8b 0a                               |
    | mov dx, word [rbx]                                              | 66 8b 13                               |
    | mov bx, word [rsp]                                              | 66 8b 1c 24                            |
    | mov sp, word [rbp]                                              | 66 8b 65 00                            |
    | mov bp, word [rsi]                                              | 66 8b 2e                               |
    | mov si, word [rdi]                                              | 66 8b 37                               |
    | mov di, word [r8]                                               | 66 41 8b 38                            |
    | mov r8w, word [r9]                                              | 66 45 8b 01                            |
    | mov r9w, word [r10]                                             | 66 45 8b 0a                            |
    | mov r10w, word [r11]                                            | 66 45 8b 13                            |
    | mov r11w, word [r12]                                            | 66 45 8b 1c 24                         |
    | mov r12w, word [r13]                                            | 66 45 8b 65 00                         |
    | mov r13w, word [r14]                                            | 66 45 8b 2e                            |
    | mov r14w, word [r15]                                            | 66 45 8b 37                            |
    | mov r15w, word [rax + 1 * rcx]                                  | 66 44 8b 3c 08                         |
    | mov cx, word [rdx + 1 * rcx]                                    | 66 8b 0c 0a                            |
    | mov dx, word [rbx + 1 * rcx]                                    | 66 8b 14 0b                            |
    | mov bx, word [rsp + 1 * rcx]                                    | 66 8b 1c 0c                            |
    | mov sp, word [rbp + 1 * rcx]                                    | 66 8b 64 0d 00                         |
    | mov bp, word [rsi + 1 * rcx]                                    | 66 8b 2c 0e                            |
    | mov si, word [rdi + 1 * rcx]                                    | 66 8b 34 0f                            |
    | mov di, word [r8 + 1 * rcx]                                     | 66 41 8b 3c 08                         |
    | mov r8w, word [r9 + 1 * rcx]                                    | 66 45 8b 04 09                         |
    | mov r9w, word [r10 + 1 * rcx]                                   | 66 45 8b 0c 0a                         |
    | mov r10w, word [r11 + 1 * rcx]                                  | 66 45 8b 14 0b                         |
    | mov r11w, word [r12 + 1 * rcx]                                  | 66 45 8b 1c 0c                         |
    | mov r12w, word [r13 + 1 * rcx]                                  | 66 45 8b 64 0d 00                      |
    | mov r13w, word [r14 + 1 * rcx]                                  | 66 45 8b 2c 0e                         |
    | mov r14w, word [r15 + 1 * rcx]                                  | 66 45 8b 34 0f                         |
    | mov r15w, word [rax + 1 * rax]                                  | 66 44 8b 3c 00                         |
    | mov cx, word [rax + 1 * rbx]                                    | 66 8b 0c 18                            |
    | mov dx, word [rax + 1 * rbp]                                    | 66 8b 14 28                            |
    | mov bx, word [rax + 1 * rsi]                                    | 66 8b 1c 30                            |
    | mov sp, word [rax + 1 * rdi]                                    | 66 8b 24 38                            |
    | mov bp, word [rax + 1 * r8]                                     | 66 42 8b 2c 00                         |
    | mov si, word [rax + 1 * r9]                                     | 66 42 8b 34 08                         |
    | mov di, word [rax + 1 * r10]                                    | 66 42 8b 3c 10                         |
    | mov r8w, word [rax + 1 * r11]                                   | 66 46 8b 04 18                         |
    | mov r9w, word [rax + 1 * r12]                                   | 66 46 8b 0c 20                         |
    | mov r10w, word [rax + 1 * r13]                                  | 66 46 8b 14 28                         |
    | mov r11w, word [rax + 1 * r14]                                  | 66 46 8b 1c 30                         |
    | mov r12w, word [rax + 1 * r15]                                  | 66 46 8b 24 38                         |
    | mov r13w, word [rax + 2 * rcx]                                  | 66 44 8b 2c 48                         |
    | mov r14w, word [rax + 4 * rcx]                                  | 66 44 8b 34 88                         |
    | mov r15w, word [rax + 8 * rcx]                                  | 66 44 8b 3c c8                         |
    | mov cx, word [r8 + 2 * r9]                                      | 66 43 8b 0c 48                         |
    | mov dx, word [r8 + 4 * r9]                                      | 66 43 8b 14 88                         |
    | mov bx, word [r8 + 8 * r9]                                      | 66 43 8b 1c c8                         |
    | mov sp, word [1 * rcx]                                          | 66 8b 24 0d 00 00 00 00                |
    | mov bp, word [2 * rcx]                                          | 66 8b 2c 4d 00 00 00 00                |
    | mov si, word [4 * rcx]                                          | 66 8b 34 8d 00 00 00 00                |
    | mov di, word [8 * rcx]                                          | 66 8b 3c cd 00 00 00 00                |
    | mov r8w, word [1 * r9]                                          | 66 46 8b 04 0d 00 00 00 00             |
    | mov r9w, word [2 * r9]                                          | 66 46 8b 0c 4d 00 00 00 00             |
    | mov r10w, word [4 * r9]                                         | 66 46 8b 14 8d 00 00 00 00             |
    | mov r11w, word [8 * r9]                                         | 66 46 8b 1c cd 00 00 00 00             |
    | mov r12w, word [r13 + 8 * r12]                                  | 66 47 8b 64 e5 00                      |
    | mov r13w, word [rsp + 4 * r15]                                  | 66 46 8b 2c bc                         |
    | mov r14w, word [rax + 1 * rcx + 0x00]                           | 66 44 8b 74 08 00                      |
    | mov r15w, word [rax + 1 * rcx - 0x00]                           | 66 44 8b 7c 08 00                      |
    | mov cx, word [rax + 1 * rcx - 0x01]                             | 66 8b 4c 08 ff                         |
    | mov dx, word [rax + 1 * rcx + 0x00000001]                       | 66 8b 94 08 01 00 00 00                |
    | mov bx, word [rax + 1 * rcx - 0x00000001]                       | 66 8b 9c 08 ff ff ff ff                |
    | mov sp, word [rax + 1 * rcx + 0x7f]                             | 66 8b 64 08 7f                         |
    | mov bp, word [rax + 1 * rcx - 0x7f]                             | 66 8b 6c 08 81                         |
    | mov si, word [rax + 1 * rcx + 0x80]                             | 66 8b b4 08 80 00 00 00                |
    | mov di, word [rax + 1 * rcx - 0x80]                             | 66 8b 7c 08 80                         |
    | mov r8w, word [rax + 1 * rcx - 0x81]                            | 66 44 8b 84 08 7f ff ff ff             |
    | mov r9w, word [rax + 1 * rcx + 0xff]                            | 66 44 8b 8c 08 ff 00 00 00             |
    | mov r10w, word [rax + 1 * rcx - 0xff]                           | 66 44 8b 94 08 01 ff ff ff             |
    | mov r11w, word [rax + 1 * rcx + 0x7fffffff]                     | 66 44 8b 9c 08 ff ff ff 7f             |
    | mov r12w, word [rax + 1 * rcx - 0x7fffffff]                     | 66 44 8b a4 08 01 00 00 80             |
    | mov r13w, word [rax + 1 * rcx - 0x80000000]                     | 66 44 8b ac 08 00 00 00 80             |
    | mov r14w, word [r10 + 0x7f]                                     | 66 45 8b 72 7f                         |
    | mov r15w, word [r10 + 0x80]                                     | 66 45 8b ba 80 00 00 00                |
    | mov cx, word [r10 - 0x81]                                       | 66 41 8b 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov dx, word [rel @prev5]      | 90 90 90 90 90 66 8b 15 f4 ff ff ff    |
    | .prev1: nop; mov bx, word [rel @prev1]                          | 90 66 8b 1d f8 ff ff ff                |
    | mov sp, word [rel @next1]; nop; .next1: nop                     | 66 8b 25 01 00 00 00 90 90             |
    | mov bp, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 8b 2d 05 00 00 00 90 90 90 90 90 90 |
    | mov si, word [rax]                                              | 66 8b 30                               |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_mov_reg16_addr16():
    encode(MOV_REG16_ADDR16)


MOV_REG8_IMM8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | mov al, 0x01   | b0 01    | *** | mov al, 0x00   | b0 00    |
    | mov cl, 0x01   | b1 01    | *** | mov al, 0x7f   | b0 7f    |
    | mov dl, 0x01   | b2 01    | *** | mov al, 0x80   | b0 80    |
    | mov bl, 0x01   | b3 01    | *** | mov al, 0xff   | b0 ff    |
    | mov spl, 0x01  | 40 b4 01 | *** | mov cl, 0x7f   | b1 7f    |
    | mov bpl, 0x01  | 40 b5 01 | *** | mov dl, 0x80   | b2 80    |
    | mov sil, 0x01  | 40 b6 01 | *** | mov bl, 0xff   | b3 ff    |
    | mov dil, 0x01  | 40 b7 01 | *** | mov spl, 0x00  | 40 b4 00 |
    | mov r8b, 0x01  | 41 b0 01 | *** | mov sil, 0x7f  | 40 b6 7f |
    | mov r9b, 0x01  | 41 b1 01 | *** | mov dil, 0x80  | 40 b7 80 |
    | mov r10b, 0x01 | 41 b2 01 | *** | mov r8b, 0xff  | 41 b0 ff |
    | mov r11b, 0x01 | 41 b3 01 | *** | mov r9b, 0x00  | 41 b1 00 |
    | mov r12b, 0x01 | 41 b4 01 | *** | mov r11b, 0x7f | 41 b3 7f |
    | mov r13b, 0x01 | 41 b5 01 | *** | mov r12b, 0x80 | 41 b4 80 |
    | mov r14b, 0x01 | 41 b6 01 | *** | mov r13b, 0xff | 41 b5 ff |
    | mov r15b, 0x01 | 41 b7 01 | *** | mov r14b, 0x00 | 41 b6 00 |
    | mov ah, 0x01   | b4 01    | *** | mov ah, 0x7f   | b4 7f    |
    | mov ch, 0x01   | b5 01    | *** | mov ch, 0x80   | b5 80    |
    | mov dh, 0x01   | b6 01    | *** | mov dh, 0xff   | b6 ff    |
    | mov bh, 0x01   | b7 01    | *** | mov bh, 0x00   | b7 00    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_mov_reg8_imm8():
    encode(MOV_REG8_IMM8)


MOV_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | mov al, cl     | 88 c8    | *** | mov al, r10b   | 44 88 d0 |
    | mov cl, cl     | 88 c9    | *** | mov al, r11b   | 44 88 d8 |
    | mov dl, cl     | 88 ca    | *** | mov al, r12b   | 44 88 e0 |
    | mov bl, cl     | 88 cb    | *** | mov al, r13b   | 44 88 e8 |
    | mov spl, cl    | 40 88 cc | *** | mov al, r14b   | 44 88 f0 |
    | mov bpl, cl    | 40 88 cd | *** | mov al, r15b   | 44 88 f8 |
    | mov sil, cl    | 40 88 ce | *** | mov al, ah     | 88 e0    |
    | mov dil, cl    | 40 88 cf | *** | mov al, ch     | 88 e8    |
    | mov r8b, cl    | 41 88 c8 | *** | mov al, dh     | 88 f0    |
    | mov r9b, cl    | 41 88 c9 | *** | mov al, bh     | 88 f8    |
    | mov r10b, cl   | 41 88 ca | *** | mov cl, dl     | 88 d1    |
    | mov r11b, cl   | 41 88 cb | *** | mov dl, bl     | 88 da    |
    | mov r12b, cl   | 41 88 cc | *** | mov bl, spl    | 40 88 e3 |
    | mov r13b, cl   | 41 88 cd | *** | mov spl, bpl   | 40 88 ec |
    | mov r14b, cl   | 41 88 ce | *** | mov bpl, sil   | 40 88 f5 |
    | mov r15b, cl   | 41 88 cf | *** | mov sil, dil   | 40 88 fe |
    | mov ah, cl     | 88 cc    | *** | mov dil, r8b   | 44 88 c7 |
    | mov ch, cl     | 88 cd    | *** | mov r8b, r9b   | 45 88 c8 |
    | mov dh, cl     | 88 ce    | *** | mov r9b, r10b  | 45 88 d1 |
    | mov bh, cl     | 88 cf    | *** | mov r10b, r11b | 45 88 da |
    | mov al, al     | 88 c0    | *** | mov r11b, r12b | 45 88 e3 |
    | mov al, dl     | 88 d0    | *** | mov r12b, r13b | 45 88 ec |
    | mov al, bl     | 88 d8    | *** | mov r13b, r14b | 45 88 f5 |
    | mov al, spl    | 40 88 e0 | *** | mov r14b, r15b | 45 88 fe |
    | mov al, bpl    | 40 88 e8 | *** | mov r15b, ah   | !! !! !! |
    | mov al, sil    | 40 88 f0 | *** | mov ah, ch     | 88 ec    |
    | mov al, dil    | 40 88 f8 | *** | mov ch, dh     | 88 f5    |
    | mov al, r8b    | 44 88 c0 | *** | mov dh, bh     | 88 fe    |
    | mov al, r9b    | 44 88 c8 | *** | mov bh, al     | 88 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_mov_reg8_reg8():
    encode(MOV_REG8_REG8)


MOV_REG8_ADDR8 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | mov al, byte [rcx]                                               | 8a 01                                  |
    | mov cl, byte [rcx]                                               | 8a 09                                  |
    | mov dl, byte [rcx]                                               | 8a 11                                  |
    | mov bl, byte [rcx]                                               | 8a 19                                  |
    | mov spl, byte [rcx]                                              | 40 8a 21                               |
    | mov bpl, byte [rcx]                                              | 40 8a 29                               |
    | mov sil, byte [rcx]                                              | 40 8a 31                               |
    | mov dil, byte [rcx]                                              | 40 8a 39                               |
    | mov r8b, byte [rcx]                                              | 44 8a 01                               |
    | mov r9b, byte [rcx]                                              | 44 8a 09                               |
    | mov r10b, byte [rcx]                                             | 44 8a 11                               |
    | mov r11b, byte [rcx]                                             | 44 8a 19                               |
    | mov r12b, byte [rcx]                                             | 44 8a 21                               |
    | mov r13b, byte [rcx]                                             | 44 8a 29                               |
    | mov r14b, byte [rcx]                                             | 44 8a 31                               |
    | mov r15b, byte [rcx]                                             | 44 8a 39                               |
    | mov ah, byte [rcx]                                               | 8a 21                                  |
    | mov ch, byte [rcx]                                               | 8a 29                                  |
    | mov dh, byte [rcx]                                               | 8a 31                                  |
    | mov bh, byte [rcx]                                               | 8a 39                                  |
    | mov al, byte [rax]                                               | 8a 00                                  |
    | mov al, byte [rdx]                                               | 8a 02                                  |
    | mov al, byte [rbx]                                               | 8a 03                                  |
    | mov al, byte [rsp]                                               | 8a 04 24                               |
    | mov al, byte [rbp]                                               | 8a 45 00                               |
    | mov al, byte [rsi]                                               | 8a 06                                  |
    | mov al, byte [rdi]                                               | 8a 07                                  |
    | mov al, byte [r8]                                                | 41 8a 00                               |
    | mov al, byte [r9]                                                | 41 8a 01                               |
    | mov al, byte [r10]                                               | 41 8a 02                               |
    | mov al, byte [r11]                                               | 41 8a 03                               |
    | mov al, byte [r12]                                               | 41 8a 04 24                            |
    | mov al, byte [r13]                                               | 41 8a 45 00                            |
    | mov al, byte [r14]                                               | 41 8a 06                               |
    | mov al, byte [r15]                                               | 41 8a 07                               |
    | mov al, byte [rax + 1 * rcx]                                     | 8a 04 08                               |
    | mov al, byte [rcx + 1 * rcx]                                     | 8a 04 09                               |
    | mov al, byte [rdx + 1 * rcx]                                     | 8a 04 0a                               |
    | mov al, byte [rbx + 1 * rcx]                                     | 8a 04 0b                               |
    | mov al, byte [rsp + 1 * rcx]                                     | 8a 04 0c                               |
    | mov al, byte [rbp + 1 * rcx]                                     | 8a 44 0d 00                            |
    | mov al, byte [rsi + 1 * rcx]                                     | 8a 04 0e                               |
    | mov al, byte [rdi + 1 * rcx]                                     | 8a 04 0f                               |
    | mov al, byte [r8 + 1 * rcx]                                      | 41 8a 04 08                            |
    | mov al, byte [r9 + 1 * rcx]                                      | 41 8a 04 09                            |
    | mov al, byte [r10 + 1 * rcx]                                     | 41 8a 04 0a                            |
    | mov al, byte [r11 + 1 * rcx]                                     | 41 8a 04 0b                            |
    | mov al, byte [r12 + 1 * rcx]                                     | 41 8a 04 0c                            |
    | mov al, byte [r13 + 1 * rcx]                                     | 41 8a 44 0d 00                         |
    | mov al, byte [r14 + 1 * rcx]                                     | 41 8a 04 0e                            |
    | mov al, byte [r15 + 1 * rcx]                                     | 41 8a 04 0f                            |
    | mov al, byte [rax + 1 * rax]                                     | 8a 04 00                               |
    | mov al, byte [rax + 1 * rdx]                                     | 8a 04 10                               |
    | mov al, byte [rax + 1 * rbx]                                     | 8a 04 18                               |
    | mov al, byte [rax + 1 * rbp]                                     | 8a 04 28                               |
    | mov al, byte [rax + 1 * rsi]                                     | 8a 04 30                               |
    | mov al, byte [rax + 1 * rdi]                                     | 8a 04 38                               |
    | mov al, byte [rax + 1 * r8]                                      | 42 8a 04 00                            |
    | mov al, byte [rax + 1 * r9]                                      | 42 8a 04 08                            |
    | mov al, byte [rax + 1 * r10]                                     | 42 8a 04 10                            |
    | mov al, byte [rax + 1 * r11]                                     | 42 8a 04 18                            |
    | mov al, byte [rax + 1 * r12]                                     | 42 8a 04 20                            |
    | mov al, byte [rax + 1 * r13]                                     | 42 8a 04 28                            |
    | mov al, byte [rax + 1 * r14]                                     | 42 8a 04 30                            |
    | mov al, byte [rax + 1 * r15]                                     | 42 8a 04 38                            |
    | mov al, byte [rax + 2 * rcx]                                     | 8a 04 48                               |
    | mov al, byte [rax + 4 * rcx]                                     | 8a 04 88                               |
    | mov al, byte [rax + 8 * rcx]                                     | 8a 04 c8                               |
    | mov al, byte [r8 + 1 * r9]                                       | 43 8a 04 08                            |
    | mov al, byte [r8 + 2 * r9]                                       | 43 8a 04 48                            |
    | mov al, byte [r8 + 4 * r9]                                       | 43 8a 04 88                            |
    | mov al, byte [r8 + 8 * r9]                                       | 43 8a 04 c8                            |
    | mov al, byte [1 * rcx]                                           | 8a 04 0d 00 00 00 00                   |
    | mov al, byte [2 * rcx]                                           | 8a 04 4d 00 00 00 00                   |
    | mov al, byte [4 * rcx]                                           | 8a 04 8d 00 00 00 00                   |
    | mov al, byte [8 * rcx]                                           | 8a 04 cd 00 00 00 00                   |
    | mov al, byte [1 * r9]                                            | 42 8a 04 0d 00 00 00 00                |
    | mov al, byte [2 * r9]                                            | 42 8a 04 4d 00 00 00 00                |
    | mov al, byte [4 * r9]                                            | 42 8a 04 8d 00 00 00 00                |
    | mov al, byte [8 * r9]                                            | 42 8a 04 cd 00 00 00 00                |
    | mov al, byte [r13 + 8 * r12]                                     | 43 8a 44 e5 00                         |
    | mov al, byte [rsp + 4 * r15]                                     | 42 8a 04 bc                            |
    | mov al, byte [rax + 1 * rcx + 0x00]                              | 8a 44 08 00                            |
    | mov al, byte [rax + 1 * rcx - 0x00]                              | 8a 44 08 00                            |
    | mov al, byte [rax + 1 * rcx + 0x01]                              | 8a 44 08 01                            |
    | mov al, byte [rax + 1 * rcx - 0x01]                              | 8a 44 08 ff                            |
    | mov al, byte [rax + 1 * rcx + 0x00000001]                        | 8a 84 08 01 00 00 00                   |
    | mov al, byte [rax + 1 * rcx - 0x00000001]                        | 8a 84 08 ff ff ff ff                   |
    | mov al, byte [rax + 1 * rcx + 0x7f]                              | 8a 44 08 7f                            |
    | mov al, byte [rax + 1 * rcx - 0x7f]                              | 8a 44 08 81                            |
    | mov al, byte [rax + 1 * rcx + 0x80]                              | 8a 84 08 80 00 00 00                   |
    | mov al, byte [rax + 1 * rcx - 0x80]                              | 8a 44 08 80                            |
    | mov al, byte [rax + 1 * rcx - 0x81]                              | 8a 84 08 7f ff ff ff                   |
    | mov al, byte [rax + 1 * rcx + 0xff]                              | 8a 84 08 ff 00 00 00                   |
    | mov al, byte [rax + 1 * rcx - 0xff]                              | 8a 84 08 01 ff ff ff                   |
    | mov al, byte [rax + 1 * rcx + 0x7fffffff]                        | 8a 84 08 ff ff ff 7f                   |
    | mov al, byte [rax + 1 * rcx - 0x7fffffff]                        | 8a 84 08 01 00 00 80                   |
    | mov al, byte [rax + 1 * rcx - 0x80000000]                        | 8a 84 08 00 00 00 80                   |
    | mov al, byte [r10 + 0x7f]                                        | 41 8a 42 7f                            |
    | mov al, byte [r10 + 0x80]                                        | 41 8a 82 80 00 00 00                   |
    | mov al, byte [r10 - 0x80]                                        | 41 8a 42 80                            |
    | mov al, byte [r10 - 0x81]                                        | 41 8a 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov al, byte [rel @prev5]       | 90 90 90 90 90 8a 05 f5 ff ff ff       |
    | .prev1: nop; mov al, byte [rel @prev1]                           | 90 8a 05 f9 ff ff ff                   |
    | mov al, byte [rel @next1]; nop; .next1: nop                      | 8a 05 01 00 00 00 90 90                |
    | mov al, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop  | 8a 05 05 00 00 00 90 90 90 90 90 90    |
    | mov cl, byte [rdx]                                               | 8a 0a                                  |
    | mov dl, byte [rbx]                                               | 8a 13                                  |
    | mov bl, byte [rsp]                                               | 8a 1c 24                               |
    | mov spl, byte [rbp]                                              | 40 8a 65 00                            |
    | mov bpl, byte [rsi]                                              | 40 8a 2e                               |
    | mov sil, byte [rdi]                                              | 40 8a 37                               |
    | mov dil, byte [r8]                                               | 41 8a 38                               |
    | mov r8b, byte [r9]                                               | 45 8a 01                               |
    | mov r9b, byte [r10]                                              | 45 8a 0a                               |
    | mov r10b, byte [r11]                                             | 45 8a 13                               |
    | mov r11b, byte [r12]                                             | 45 8a 1c 24                            |
    | mov r12b, byte [r13]                                             | 45 8a 65 00                            |
    | mov r13b, byte [r14]                                             | 45 8a 2e                               |
    | mov r14b, byte [r15]                                             | 45 8a 37                               |
    | mov r15b, byte [rax + 1 * rcx]                                   | 44 8a 3c 08                            |
    | mov ah, byte [rcx + 1 * rcx]                                     | 8a 24 09                               |
    | mov ch, byte [rdx + 1 * rcx]                                     | 8a 2c 0a                               |
    | mov dh, byte [rbx + 1 * rcx]                                     | 8a 34 0b                               |
    | mov bh, byte [rsp + 1 * rcx]                                     | 8a 3c 0c                               |
    | mov cl, byte [rsi + 1 * rcx]                                     | 8a 0c 0e                               |
    | mov dl, byte [rdi + 1 * rcx]                                     | 8a 14 0f                               |
    | mov bl, byte [r8 + 1 * rcx]                                      | 41 8a 1c 08                            |
    | mov spl, byte [r9 + 1 * rcx]                                     | 41 8a 24 09                            |
    | mov bpl, byte [r10 + 1 * rcx]                                    | 41 8a 2c 0a                            |
    | mov sil, byte [r11 + 1 * rcx]                                    | 41 8a 34 0b                            |
    | mov dil, byte [r12 + 1 * rcx]                                    | 41 8a 3c 0c                            |
    | mov r8b, byte [r13 + 1 * rcx]                                    | 45 8a 44 0d 00                         |
    | mov r9b, byte [r14 + 1 * rcx]                                    | 45 8a 0c 0e                            |
    | mov r10b, byte [r15 + 1 * rcx]                                   | 45 8a 14 0f                            |
    | mov r11b, byte [rax + 1 * rax]                                   | 44 8a 1c 00                            |
    | mov r12b, byte [rax + 1 * rdx]                                   | 44 8a 24 10                            |
    | mov r13b, byte [rax + 1 * rbx]                                   | 44 8a 2c 18                            |
    | mov r14b, byte [rax + 1 * rbp]                                   | 44 8a 34 28                            |
    | mov r15b, byte [rax + 1 * rsi]                                   | 44 8a 3c 30                            |
    | mov ah, byte [rax + 1 * rdi]                                     | 8a 24 38                               |
    | mov ch, byte [rax + 1 * r8]                                      | !! !! !!                               |
    | mov dh, byte [rax + 1 * r9]                                      | !! !! !!                               |
    | mov bh, byte [rax + 1 * r10]                                     | !! !! !!                               |
    | mov cl, byte [rax + 1 * r12]                                     | 42 8a 0c 20                            |
    | mov dl, byte [rax + 1 * r13]                                     | 42 8a 14 28                            |
    | mov bl, byte [rax + 1 * r14]                                     | 42 8a 1c 30                            |
    | mov spl, byte [rax + 1 * r15]                                    | 42 8a 24 38                            |
    | mov bpl, byte [rax + 2 * rcx]                                    | 40 8a 2c 48                            |
    | mov sil, byte [rax + 4 * rcx]                                    | 40 8a 34 88                            |
    | mov dil, byte [rax + 8 * rcx]                                    | 40 8a 3c c8                            |
    | mov r8b, byte [r8 + 1 * r9]                                      | 47 8a 04 08                            |
    | mov r9b, byte [r8 + 2 * r9]                                      | 47 8a 0c 48                            |
    | mov r10b, byte [r8 + 4 * r9]                                     | 47 8a 14 88                            |
    | mov r11b, byte [r8 + 8 * r9]                                     | 47 8a 1c c8                            |
    | mov r12b, byte [1 * rcx]                                         | 44 8a 24 0d 00 00 00 00                |
    | mov r13b, byte [2 * rcx]                                         | 44 8a 2c 4d 00 00 00 00                |
    | mov r14b, byte [4 * rcx]                                         | 44 8a 34 8d 00 00 00 00                |
    | mov r15b, byte [8 * rcx]                                         | 44 8a 3c cd 00 00 00 00                |
    | mov ah, byte [1 * r9]                                            | !! !! !!                               |
    | mov ch, byte [2 * r9]                                            | !! !! !!                               |
    | mov dh, byte [4 * r9]                                            | !! !! !!                               |
    | mov bh, byte [8 * r9]                                            | !! !! !!                               |
    | mov cl, byte [rsp + 4 * r15]                                     | 42 8a 0c bc                            |
    | mov dl, byte [rax + 1 * rcx + 0x00]                              | 8a 54 08 00                            |
    | mov bl, byte [rax + 1 * rcx - 0x00]                              | 8a 5c 08 00                            |
    | mov spl, byte [rax + 1 * rcx + 0x01]                             | 40 8a 64 08 01                         |
    | mov bpl, byte [rax + 1 * rcx - 0x01]                             | 40 8a 6c 08 ff                         |
    | mov sil, byte [rax + 1 * rcx + 0x00000001]                       | 40 8a b4 08 01 00 00 00                |
    | mov dil, byte [rax + 1 * rcx - 0x00000001]                       | 40 8a bc 08 ff ff ff ff                |
    | mov r8b, byte [rax + 1 * rcx + 0x7f]                             | 44 8a 44 08 7f                         |
    | mov r9b, byte [rax + 1 * rcx - 0x7f]                             | 44 8a 4c 08 81                         |
    | mov r10b, byte [rax + 1 * rcx + 0x80]                            | 44 8a 94 08 80 00 00 00                |
    | mov r11b, byte [rax + 1 * rcx - 0x80]                            | 44 8a 5c 08 80                         |
    | mov r12b, byte [rax + 1 * rcx - 0x81]                            | 44 8a a4 08 7f ff ff ff                |
    | mov r13b, byte [rax + 1 * rcx + 0xff]                            | 44 8a ac 08 ff 00 00 00                |
    | mov r14b, byte [rax + 1 * rcx - 0xff]                            | 44 8a b4 08 01 ff ff ff                |
    | mov r15b, byte [rax + 1 * rcx + 0x7fffffff]                      | 44 8a bc 08 ff ff ff 7f                |
    | mov ah, byte [rax + 1 * rcx - 0x7fffffff]                        | 8a a4 08 01 00 00 80                   |
    | mov ch, byte [rax + 1 * rcx - 0x80000000]                        | 8a ac 08 00 00 00 80                   |
    | mov dh, byte [r10 + 0x7f]                                        | !! !! !!                               |
    | mov bh, byte [r10 + 0x80]                                        | !! !! !!                               |
    | mov cl, byte [r10 - 0x81]                                        | 41 8a 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov dl, byte [rel @prev5]       | 90 90 90 90 90 8a 15 f5 ff ff ff       |
    | .prev1: nop; mov bl, byte [rel @prev1]                           | 90 8a 1d f9 ff ff ff                   |
    | mov spl, byte [rel @next1]; nop; .next1: nop                     | 40 8a 25 01 00 00 00 90 90             |
    | mov bpl, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 40 8a 2d 05 00 00 00 90 90 90 90 90 90 |
    | mov sil, byte [rax]                                              | 40 8a 30                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_mov_reg8_addr8():
    encode(MOV_REG8_ADDR8)


MOV_ADDR64_IMM32 = """
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
    | instruction                                                              | encoding                                           |
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
    | mov qword [rax], 0x00000001                                              | 48 c7 00 01 00 00 00                               |
    | mov qword [rcx], 0x00000001                                              | 48 c7 01 01 00 00 00                               |
    | mov qword [rdx], 0x00000001                                              | 48 c7 02 01 00 00 00                               |
    | mov qword [rbx], 0x00000001                                              | 48 c7 03 01 00 00 00                               |
    | mov qword [rsp], 0x00000001                                              | 48 c7 04 24 01 00 00 00                            |
    | mov qword [rbp], 0x00000001                                              | 48 c7 45 00 01 00 00 00                            |
    | mov qword [rsi], 0x00000001                                              | 48 c7 06 01 00 00 00                               |
    | mov qword [rdi], 0x00000001                                              | 48 c7 07 01 00 00 00                               |
    | mov qword [r8], 0x00000001                                               | 49 c7 00 01 00 00 00                               |
    | mov qword [r9], 0x00000001                                               | 49 c7 01 01 00 00 00                               |
    | mov qword [r10], 0x00000001                                              | 49 c7 02 01 00 00 00                               |
    | mov qword [r11], 0x00000001                                              | 49 c7 03 01 00 00 00                               |
    | mov qword [r12], 0x00000001                                              | 49 c7 04 24 01 00 00 00                            |
    | mov qword [r13], 0x00000001                                              | 49 c7 45 00 01 00 00 00                            |
    | mov qword [r14], 0x00000001                                              | 49 c7 06 01 00 00 00                               |
    | mov qword [r15], 0x00000001                                              | 49 c7 07 01 00 00 00                               |
    | mov qword [rax + 1 * rcx], 0x00000001                                    | 48 c7 04 08 01 00 00 00                            |
    | mov qword [rcx + 1 * rcx], 0x00000001                                    | 48 c7 04 09 01 00 00 00                            |
    | mov qword [rdx + 1 * rcx], 0x00000001                                    | 48 c7 04 0a 01 00 00 00                            |
    | mov qword [rbx + 1 * rcx], 0x00000001                                    | 48 c7 04 0b 01 00 00 00                            |
    | mov qword [rsp + 1 * rcx], 0x00000001                                    | 48 c7 04 0c 01 00 00 00                            |
    | mov qword [rbp + 1 * rcx], 0x00000001                                    | 48 c7 44 0d 00 01 00 00 00                         |
    | mov qword [rsi + 1 * rcx], 0x00000001                                    | 48 c7 04 0e 01 00 00 00                            |
    | mov qword [rdi + 1 * rcx], 0x00000001                                    | 48 c7 04 0f 01 00 00 00                            |
    | mov qword [r8 + 1 * rcx], 0x00000001                                     | 49 c7 04 08 01 00 00 00                            |
    | mov qword [r9 + 1 * rcx], 0x00000001                                     | 49 c7 04 09 01 00 00 00                            |
    | mov qword [r10 + 1 * rcx], 0x00000001                                    | 49 c7 04 0a 01 00 00 00                            |
    | mov qword [r11 + 1 * rcx], 0x00000001                                    | 49 c7 04 0b 01 00 00 00                            |
    | mov qword [r12 + 1 * rcx], 0x00000001                                    | 49 c7 04 0c 01 00 00 00                            |
    | mov qword [r13 + 1 * rcx], 0x00000001                                    | 49 c7 44 0d 00 01 00 00 00                         |
    | mov qword [r14 + 1 * rcx], 0x00000001                                    | 49 c7 04 0e 01 00 00 00                            |
    | mov qword [r15 + 1 * rcx], 0x00000001                                    | 49 c7 04 0f 01 00 00 00                            |
    | mov qword [rax + 1 * rax], 0x00000001                                    | 48 c7 04 00 01 00 00 00                            |
    | mov qword [rax + 1 * rdx], 0x00000001                                    | 48 c7 04 10 01 00 00 00                            |
    | mov qword [rax + 1 * rbx], 0x00000001                                    | 48 c7 04 18 01 00 00 00                            |
    | mov qword [rax + 1 * rbp], 0x00000001                                    | 48 c7 04 28 01 00 00 00                            |
    | mov qword [rax + 1 * rsi], 0x00000001                                    | 48 c7 04 30 01 00 00 00                            |
    | mov qword [rax + 1 * rdi], 0x00000001                                    | 48 c7 04 38 01 00 00 00                            |
    | mov qword [rax + 1 * r8], 0x00000001                                     | 4a c7 04 00 01 00 00 00                            |
    | mov qword [rax + 1 * r9], 0x00000001                                     | 4a c7 04 08 01 00 00 00                            |
    | mov qword [rax + 1 * r10], 0x00000001                                    | 4a c7 04 10 01 00 00 00                            |
    | mov qword [rax + 1 * r11], 0x00000001                                    | 4a c7 04 18 01 00 00 00                            |
    | mov qword [rax + 1 * r12], 0x00000001                                    | 4a c7 04 20 01 00 00 00                            |
    | mov qword [rax + 1 * r13], 0x00000001                                    | 4a c7 04 28 01 00 00 00                            |
    | mov qword [rax + 1 * r14], 0x00000001                                    | 4a c7 04 30 01 00 00 00                            |
    | mov qword [rax + 1 * r15], 0x00000001                                    | 4a c7 04 38 01 00 00 00                            |
    | mov qword [rax + 2 * rcx], 0x00000001                                    | 48 c7 04 48 01 00 00 00                            |
    | mov qword [rax + 4 * rcx], 0x00000001                                    | 48 c7 04 88 01 00 00 00                            |
    | mov qword [rax + 8 * rcx], 0x00000001                                    | 48 c7 04 c8 01 00 00 00                            |
    | mov qword [r8 + 1 * r9], 0x00000001                                      | 4b c7 04 08 01 00 00 00                            |
    | mov qword [r8 + 2 * r9], 0x00000001                                      | 4b c7 04 48 01 00 00 00                            |
    | mov qword [r8 + 4 * r9], 0x00000001                                      | 4b c7 04 88 01 00 00 00                            |
    | mov qword [r8 + 8 * r9], 0x00000001                                      | 4b c7 04 c8 01 00 00 00                            |
    | mov qword [1 * rcx], 0x00000001                                          | 48 c7 04 0d 00 00 00 00 01 00 00 00                |
    | mov qword [2 * rcx], 0x00000001                                          | 48 c7 04 4d 00 00 00 00 01 00 00 00                |
    | mov qword [4 * rcx], 0x00000001                                          | 48 c7 04 8d 00 00 00 00 01 00 00 00                |
    | mov qword [8 * rcx], 0x00000001                                          | 48 c7 04 cd 00 00 00 00 01 00 00 00                |
    | mov qword [1 * r9], 0x00000001                                           | 4a c7 04 0d 00 00 00 00 01 00 00 00                |
    | mov qword [2 * r9], 0x00000001                                           | 4a c7 04 4d 00 00 00 00 01 00 00 00                |
    | mov qword [4 * r9], 0x00000001                                           | 4a c7 04 8d 00 00 00 00 01 00 00 00                |
    | mov qword [8 * r9], 0x00000001                                           | 4a c7 04 cd 00 00 00 00 01 00 00 00                |
    | mov qword [r13 + 8 * r12], 0x00000001                                    | 4b c7 44 e5 00 01 00 00 00                         |
    | mov qword [rsp + 4 * r15], 0x00000001                                    | 4a c7 04 bc 01 00 00 00                            |
    | mov qword [rax + 1 * rcx + 0x00], 0x00000001                             | 48 c7 44 08 00 01 00 00 00                         |
    | mov qword [rax + 1 * rcx - 0x00], 0x00000001                             | 48 c7 44 08 00 01 00 00 00                         |
    | mov qword [rax + 1 * rcx + 0x01], 0x00000001                             | 48 c7 44 08 01 01 00 00 00                         |
    | mov qword [rax + 1 * rcx - 0x01], 0x00000001                             | 48 c7 44 08 ff 01 00 00 00                         |
    | mov qword [rax + 1 * rcx + 0x00000001], 0x00000001                       | 48 c7 84 08 01 00 00 00 01 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x00000001], 0x00000001                       | 48 c7 84 08 ff ff ff ff 01 00 00 00                |
    | mov qword [rax + 1 * rcx + 0x7f], 0x00000001                             | 48 c7 44 08 7f 01 00 00 00                         |
    | mov qword [rax + 1 * rcx - 0x7f], 0x00000001                             | 48 c7 44 08 81 01 00 00 00                         |
    | mov qword [rax + 1 * rcx + 0x80], 0x00000001                             | 48 c7 84 08 80 00 00 00 01 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x80], 0x00000001                             | 48 c7 44 08 80 01 00 00 00                         |
    | mov qword [rax + 1 * rcx - 0x81], 0x00000001                             | 48 c7 84 08 7f ff ff ff 01 00 00 00                |
    | mov qword [rax + 1 * rcx + 0xff], 0x00000001                             | 48 c7 84 08 ff 00 00 00 01 00 00 00                |
    | mov qword [rax + 1 * rcx - 0xff], 0x00000001                             | 48 c7 84 08 01 ff ff ff 01 00 00 00                |
    | mov qword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | 48 c7 84 08 ff ff ff 7f 01 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | 48 c7 84 08 01 00 00 80 01 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x80000000], 0x00000001                       | 48 c7 84 08 00 00 00 80 01 00 00 00                |
    | mov qword [r10 + 0x7f], 0x00000001                                       | 49 c7 42 7f 01 00 00 00                            |
    | mov qword [r10 + 0x80], 0x00000001                                       | 49 c7 82 80 00 00 00 01 00 00 00                   |
    | mov qword [r10 - 0x80], 0x00000001                                       | 49 c7 42 80 01 00 00 00                            |
    | mov qword [r10 - 0x81], 0x00000001                                       | 49 c7 82 7f ff ff ff 01 00 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; mov qword [rel @prev5], 0x00000001      | 90 90 90 90 90 48 c7 05 f0 ff ff ff 01 00 00 00    |
    | .prev1: nop; mov qword [rel @prev1], 0x00000001                          | 90 48 c7 05 f4 ff ff ff 01 00 00 00                |
    | mov qword [rel @next1], 0x00000001; nop; .next1: nop                     | 48 c7 05 01 00 00 00 01 00 00 00 90 90             |
    | mov qword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | 48 c7 05 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | mov qword [rax], 0x00000000                                              | 48 c7 00 00 00 00 00                               |
    | mov qword [rax], 0x0000007f                                              | 48 c7 00 7f 00 00 00                               |
    | mov qword [rax], 0x00000080                                              | 48 c7 00 80 00 00 00                               |
    | mov qword [rax], 0x000000ff                                              | 48 c7 00 ff 00 00 00                               |
    | mov qword [rax], 0x00000100                                              | 48 c7 00 00 01 00 00                               |
    | mov qword [rax], 0x00007fff                                              | 48 c7 00 ff 7f 00 00                               |
    | mov qword [rax], 0x00008000                                              | 48 c7 00 00 80 00 00                               |
    | mov qword [rax], 0x0000ffff                                              | 48 c7 00 ff ff 00 00                               |
    | mov qword [rax], 0x00010000                                              | 48 c7 00 00 00 01 00                               |
    | mov qword [rax], 0x7fffffff                                              | 48 c7 00 ff ff ff 7f                               |
    | mov qword [rax], 0x80000000                                              | 48 c7 00 00 00 00 80                               |
    | mov qword [rax], 0xffffffff                                              | 48 c7 00 ff ff ff ff                               |
    | mov qword [rcx], 0x0000007f                                              | 48 c7 01 7f 00 00 00                               |
    | mov qword [rdx], 0x00000080                                              | 48 c7 02 80 00 00 00                               |
    | mov qword [rbx], 0x000000ff                                              | 48 c7 03 ff 00 00 00                               |
    | mov qword [rsp], 0x00000100                                              | 48 c7 04 24 00 01 00 00                            |
    | mov qword [rbp], 0x00007fff                                              | 48 c7 45 00 ff 7f 00 00                            |
    | mov qword [rsi], 0x00008000                                              | 48 c7 06 00 80 00 00                               |
    | mov qword [rdi], 0x0000ffff                                              | 48 c7 07 ff ff 00 00                               |
    | mov qword [r8], 0x00010000                                               | 49 c7 00 00 00 01 00                               |
    | mov qword [r9], 0x7fffffff                                               | 49 c7 01 ff ff ff 7f                               |
    | mov qword [r10], 0x80000000                                              | 49 c7 02 00 00 00 80                               |
    | mov qword [r11], 0xffffffff                                              | 49 c7 03 ff ff ff ff                               |
    | mov qword [r12], 0x00000000                                              | 49 c7 04 24 00 00 00 00                            |
    | mov qword [r14], 0x0000007f                                              | 49 c7 06 7f 00 00 00                               |
    | mov qword [r15], 0x00000080                                              | 49 c7 07 80 00 00 00                               |
    | mov qword [rax + 1 * rcx], 0x000000ff                                    | 48 c7 04 08 ff 00 00 00                            |
    | mov qword [rcx + 1 * rcx], 0x00000100                                    | 48 c7 04 09 00 01 00 00                            |
    | mov qword [rdx + 1 * rcx], 0x00007fff                                    | 48 c7 04 0a ff 7f 00 00                            |
    | mov qword [rbx + 1 * rcx], 0x00008000                                    | 48 c7 04 0b 00 80 00 00                            |
    | mov qword [rsp + 1 * rcx], 0x0000ffff                                    | 48 c7 04 0c ff ff 00 00                            |
    | mov qword [rbp + 1 * rcx], 0x00010000                                    | 48 c7 44 0d 00 00 00 01 00                         |
    | mov qword [rsi + 1 * rcx], 0x7fffffff                                    | 48 c7 04 0e ff ff ff 7f                            |
    | mov qword [rdi + 1 * rcx], 0x80000000                                    | 48 c7 04 0f 00 00 00 80                            |
    | mov qword [r8 + 1 * rcx], 0xffffffff                                     | 49 c7 04 08 ff ff ff ff                            |
    | mov qword [r9 + 1 * rcx], 0x00000000                                     | 49 c7 04 09 00 00 00 00                            |
    | mov qword [r11 + 1 * rcx], 0x0000007f                                    | 49 c7 04 0b 7f 00 00 00                            |
    | mov qword [r12 + 1 * rcx], 0x00000080                                    | 49 c7 04 0c 80 00 00 00                            |
    | mov qword [r13 + 1 * rcx], 0x000000ff                                    | 49 c7 44 0d 00 ff 00 00 00                         |
    | mov qword [r14 + 1 * rcx], 0x00000100                                    | 49 c7 04 0e 00 01 00 00                            |
    | mov qword [r15 + 1 * rcx], 0x00007fff                                    | 49 c7 04 0f ff 7f 00 00                            |
    | mov qword [rax + 1 * rax], 0x00008000                                    | 48 c7 04 00 00 80 00 00                            |
    | mov qword [rax + 1 * rdx], 0x0000ffff                                    | 48 c7 04 10 ff ff 00 00                            |
    | mov qword [rax + 1 * rbx], 0x00010000                                    | 48 c7 04 18 00 00 01 00                            |
    | mov qword [rax + 1 * rbp], 0x7fffffff                                    | 48 c7 04 28 ff ff ff 7f                            |
    | mov qword [rax + 1 * rsi], 0x80000000                                    | 48 c7 04 30 00 00 00 80                            |
    | mov qword [rax + 1 * rdi], 0xffffffff                                    | 48 c7 04 38 ff ff ff ff                            |
    | mov qword [rax + 1 * r8], 0x00000000                                     | 4a c7 04 00 00 00 00 00                            |
    | mov qword [rax + 1 * r10], 0x0000007f                                    | 4a c7 04 10 7f 00 00 00                            |
    | mov qword [rax + 1 * r11], 0x00000080                                    | 4a c7 04 18 80 00 00 00                            |
    | mov qword [rax + 1 * r12], 0x000000ff                                    | 4a c7 04 20 ff 00 00 00                            |
    | mov qword [rax + 1 * r13], 0x00000100                                    | 4a c7 04 28 00 01 00 00                            |
    | mov qword [rax + 1 * r14], 0x00007fff                                    | 4a c7 04 30 ff 7f 00 00                            |
    | mov qword [rax + 1 * r15], 0x00008000                                    | 4a c7 04 38 00 80 00 00                            |
    | mov qword [rax + 2 * rcx], 0x0000ffff                                    | 48 c7 04 48 ff ff 00 00                            |
    | mov qword [rax + 4 * rcx], 0x00010000                                    | 48 c7 04 88 00 00 01 00                            |
    | mov qword [rax + 8 * rcx], 0x7fffffff                                    | 48 c7 04 c8 ff ff ff 7f                            |
    | mov qword [r8 + 1 * r9], 0x80000000                                      | 4b c7 04 08 00 00 00 80                            |
    | mov qword [r8 + 2 * r9], 0xffffffff                                      | 4b c7 04 48 ff ff ff ff                            |
    | mov qword [r8 + 4 * r9], 0x00000000                                      | 4b c7 04 88 00 00 00 00                            |
    | mov qword [1 * rcx], 0x0000007f                                          | 48 c7 04 0d 00 00 00 00 7f 00 00 00                |
    | mov qword [2 * rcx], 0x00000080                                          | 48 c7 04 4d 00 00 00 00 80 00 00 00                |
    | mov qword [4 * rcx], 0x000000ff                                          | 48 c7 04 8d 00 00 00 00 ff 00 00 00                |
    | mov qword [8 * rcx], 0x00000100                                          | 48 c7 04 cd 00 00 00 00 00 01 00 00                |
    | mov qword [1 * r9], 0x00007fff                                           | 4a c7 04 0d 00 00 00 00 ff 7f 00 00                |
    | mov qword [2 * r9], 0x00008000                                           | 4a c7 04 4d 00 00 00 00 00 80 00 00                |
    | mov qword [4 * r9], 0x0000ffff                                           | 4a c7 04 8d 00 00 00 00 ff ff 00 00                |
    | mov qword [8 * r9], 0x00010000                                           | 4a c7 04 cd 00 00 00 00 00 00 01 00                |
    | mov qword [r13 + 8 * r12], 0x7fffffff                                    | 4b c7 44 e5 00 ff ff ff 7f                         |
    | mov qword [rsp + 4 * r15], 0x80000000                                    | 4a c7 04 bc 00 00 00 80                            |
    | mov qword [rax + 1 * rcx + 0x00], 0xffffffff                             | 48 c7 44 08 00 ff ff ff ff                         |
    | mov qword [rax + 1 * rcx - 0x00], 0x00000000                             | 48 c7 44 08 00 00 00 00 00                         |
    | mov qword [rax + 1 * rcx - 0x01], 0x0000007f                             | 48 c7 44 08 ff 7f 00 00 00                         |
    | mov qword [rax + 1 * rcx + 0x00000001], 0x00000080                       | 48 c7 84 08 01 00 00 00 80 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | 48 c7 84 08 ff ff ff ff ff 00 00 00                |
    | mov qword [rax + 1 * rcx + 0x7f], 0x00000100                             | 48 c7 44 08 7f 00 01 00 00                         |
    | mov qword [rax + 1 * rcx - 0x7f], 0x00007fff                             | 48 c7 44 08 81 ff 7f 00 00                         |
    | mov qword [rax + 1 * rcx + 0x80], 0x00008000                             | 48 c7 84 08 80 00 00 00 00 80 00 00                |
    | mov qword [rax + 1 * rcx - 0x80], 0x0000ffff                             | 48 c7 44 08 80 ff ff 00 00                         |
    | mov qword [rax + 1 * rcx - 0x81], 0x00010000                             | 48 c7 84 08 7f ff ff ff 00 00 01 00                |
    | mov qword [rax + 1 * rcx + 0xff], 0x7fffffff                             | 48 c7 84 08 ff 00 00 00 ff ff ff 7f                |
    | mov qword [rax + 1 * rcx - 0xff], 0x80000000                             | 48 c7 84 08 01 ff ff ff 00 00 00 80                |
    | mov qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | 48 c7 84 08 ff ff ff 7f ff ff ff ff                |
    | mov qword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | 48 c7 84 08 01 00 00 80 00 00 00 00                |
    | mov qword [r10 + 0x7f], 0x0000007f                                       | 49 c7 42 7f 7f 00 00 00                            |
    | mov qword [r10 + 0x80], 0x00000080                                       | 49 c7 82 80 00 00 00 80 00 00 00                   |
    | mov qword [r10 - 0x80], 0x000000ff                                       | 49 c7 42 80 ff 00 00 00                            |
    | mov qword [r10 - 0x81], 0x00000100                                       | 49 c7 82 7f ff ff ff 00 01 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; mov qword [rel @prev5], 0x00007fff      | 90 90 90 90 90 48 c7 05 f0 ff ff ff ff 7f 00 00    |
    | .prev1: nop; mov qword [rel @prev1], 0x00008000                          | 90 48 c7 05 f4 ff ff ff 00 80 00 00                |
    | mov qword [rel @next1], 0x0000ffff; nop; .next1: nop                     | 48 c7 05 01 00 00 00 ff ff 00 00 90 90             |
    | mov qword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | 48 c7 05 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
"""


def can_encode_mov_addr64_imm32():
    encode(MOV_ADDR64_IMM32)


MOV_ADDR64_REG64 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | mov qword [rax], rcx                                              | 48 89 08                               |
    | mov qword [rcx], rcx                                              | 48 89 09                               |
    | mov qword [rdx], rcx                                              | 48 89 0a                               |
    | mov qword [rbx], rcx                                              | 48 89 0b                               |
    | mov qword [rsp], rcx                                              | 48 89 0c 24                            |
    | mov qword [rbp], rcx                                              | 48 89 4d 00                            |
    | mov qword [rsi], rcx                                              | 48 89 0e                               |
    | mov qword [rdi], rcx                                              | 48 89 0f                               |
    | mov qword [r8], rcx                                               | 49 89 08                               |
    | mov qword [r9], rcx                                               | 49 89 09                               |
    | mov qword [r10], rcx                                              | 49 89 0a                               |
    | mov qword [r11], rcx                                              | 49 89 0b                               |
    | mov qword [r12], rcx                                              | 49 89 0c 24                            |
    | mov qword [r13], rcx                                              | 49 89 4d 00                            |
    | mov qword [r14], rcx                                              | 49 89 0e                               |
    | mov qword [r15], rcx                                              | 49 89 0f                               |
    | mov qword [rax + 1 * rcx], rcx                                    | 48 89 0c 08                            |
    | mov qword [rcx + 1 * rcx], rcx                                    | 48 89 0c 09                            |
    | mov qword [rdx + 1 * rcx], rcx                                    | 48 89 0c 0a                            |
    | mov qword [rbx + 1 * rcx], rcx                                    | 48 89 0c 0b                            |
    | mov qword [rsp + 1 * rcx], rcx                                    | 48 89 0c 0c                            |
    | mov qword [rbp + 1 * rcx], rcx                                    | 48 89 4c 0d 00                         |
    | mov qword [rsi + 1 * rcx], rcx                                    | 48 89 0c 0e                            |
    | mov qword [rdi + 1 * rcx], rcx                                    | 48 89 0c 0f                            |
    | mov qword [r8 + 1 * rcx], rcx                                     | 49 89 0c 08                            |
    | mov qword [r9 + 1 * rcx], rcx                                     | 49 89 0c 09                            |
    | mov qword [r10 + 1 * rcx], rcx                                    | 49 89 0c 0a                            |
    | mov qword [r11 + 1 * rcx], rcx                                    | 49 89 0c 0b                            |
    | mov qword [r12 + 1 * rcx], rcx                                    | 49 89 0c 0c                            |
    | mov qword [r13 + 1 * rcx], rcx                                    | 49 89 4c 0d 00                         |
    | mov qword [r14 + 1 * rcx], rcx                                    | 49 89 0c 0e                            |
    | mov qword [r15 + 1 * rcx], rcx                                    | 49 89 0c 0f                            |
    | mov qword [rax + 1 * rax], rcx                                    | 48 89 0c 00                            |
    | mov qword [rax + 1 * rdx], rcx                                    | 48 89 0c 10                            |
    | mov qword [rax + 1 * rbx], rcx                                    | 48 89 0c 18                            |
    | mov qword [rax + 1 * rbp], rcx                                    | 48 89 0c 28                            |
    | mov qword [rax + 1 * rsi], rcx                                    | 48 89 0c 30                            |
    | mov qword [rax + 1 * rdi], rcx                                    | 48 89 0c 38                            |
    | mov qword [rax + 1 * r8], rcx                                     | 4a 89 0c 00                            |
    | mov qword [rax + 1 * r9], rcx                                     | 4a 89 0c 08                            |
    | mov qword [rax + 1 * r10], rcx                                    | 4a 89 0c 10                            |
    | mov qword [rax + 1 * r11], rcx                                    | 4a 89 0c 18                            |
    | mov qword [rax + 1 * r12], rcx                                    | 4a 89 0c 20                            |
    | mov qword [rax + 1 * r13], rcx                                    | 4a 89 0c 28                            |
    | mov qword [rax + 1 * r14], rcx                                    | 4a 89 0c 30                            |
    | mov qword [rax + 1 * r15], rcx                                    | 4a 89 0c 38                            |
    | mov qword [rax + 2 * rcx], rcx                                    | 48 89 0c 48                            |
    | mov qword [rax + 4 * rcx], rcx                                    | 48 89 0c 88                            |
    | mov qword [rax + 8 * rcx], rcx                                    | 48 89 0c c8                            |
    | mov qword [r8 + 1 * r9], rcx                                      | 4b 89 0c 08                            |
    | mov qword [r8 + 2 * r9], rcx                                      | 4b 89 0c 48                            |
    | mov qword [r8 + 4 * r9], rcx                                      | 4b 89 0c 88                            |
    | mov qword [r8 + 8 * r9], rcx                                      | 4b 89 0c c8                            |
    | mov qword [1 * rcx], rcx                                          | 48 89 0c 0d 00 00 00 00                |
    | mov qword [2 * rcx], rcx                                          | 48 89 0c 4d 00 00 00 00                |
    | mov qword [4 * rcx], rcx                                          | 48 89 0c 8d 00 00 00 00                |
    | mov qword [8 * rcx], rcx                                          | 48 89 0c cd 00 00 00 00                |
    | mov qword [1 * r9], rcx                                           | 4a 89 0c 0d 00 00 00 00                |
    | mov qword [2 * r9], rcx                                           | 4a 89 0c 4d 00 00 00 00                |
    | mov qword [4 * r9], rcx                                           | 4a 89 0c 8d 00 00 00 00                |
    | mov qword [8 * r9], rcx                                           | 4a 89 0c cd 00 00 00 00                |
    | mov qword [r13 + 8 * r12], rcx                                    | 4b 89 4c e5 00                         |
    | mov qword [rsp + 4 * r15], rcx                                    | 4a 89 0c bc                            |
    | mov qword [rax + 1 * rcx + 0x00], rcx                             | 48 89 4c 08 00                         |
    | mov qword [rax + 1 * rcx - 0x00], rcx                             | 48 89 4c 08 00                         |
    | mov qword [rax + 1 * rcx + 0x01], rcx                             | 48 89 4c 08 01                         |
    | mov qword [rax + 1 * rcx - 0x01], rcx                             | 48 89 4c 08 ff                         |
    | mov qword [rax + 1 * rcx + 0x00000001], rcx                       | 48 89 8c 08 01 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x00000001], rcx                       | 48 89 8c 08 ff ff ff ff                |
    | mov qword [rax + 1 * rcx + 0x7f], rcx                             | 48 89 4c 08 7f                         |
    | mov qword [rax + 1 * rcx - 0x7f], rcx                             | 48 89 4c 08 81                         |
    | mov qword [rax + 1 * rcx + 0x80], rcx                             | 48 89 8c 08 80 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x80], rcx                             | 48 89 4c 08 80                         |
    | mov qword [rax + 1 * rcx - 0x81], rcx                             | 48 89 8c 08 7f ff ff ff                |
    | mov qword [rax + 1 * rcx + 0xff], rcx                             | 48 89 8c 08 ff 00 00 00                |
    | mov qword [rax + 1 * rcx - 0xff], rcx                             | 48 89 8c 08 01 ff ff ff                |
    | mov qword [rax + 1 * rcx + 0x7fffffff], rcx                       | 48 89 8c 08 ff ff ff 7f                |
    | mov qword [rax + 1 * rcx - 0x7fffffff], rcx                       | 48 89 8c 08 01 00 00 80                |
    | mov qword [rax + 1 * rcx - 0x80000000], rcx                       | 48 89 8c 08 00 00 00 80                |
    | mov qword [r10 + 0x7f], rcx                                       | 49 89 4a 7f                            |
    | mov qword [r10 + 0x80], rcx                                       | 49 89 8a 80 00 00 00                   |
    | mov qword [r10 - 0x80], rcx                                       | 49 89 4a 80                            |
    | mov qword [r10 - 0x81], rcx                                       | 49 89 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov qword [rel @prev5], rcx      | 90 90 90 90 90 48 89 0d f4 ff ff ff    |
    | .prev1: nop; mov qword [rel @prev1], rcx                          | 90 48 89 0d f8 ff ff ff                |
    | mov qword [rel @next1], rcx; nop; .next1: nop                     | 48 89 0d 01 00 00 00 90 90             |
    | mov qword [rel @next5], rcx; nop; nop; nop; nop; nop; .next5: nop | 48 89 0d 05 00 00 00 90 90 90 90 90 90 |
    | mov qword [rax], rax                                              | 48 89 00                               |
    | mov qword [rax], rdx                                              | 48 89 10                               |
    | mov qword [rax], rbx                                              | 48 89 18                               |
    | mov qword [rax], rsp                                              | 48 89 20                               |
    | mov qword [rax], rbp                                              | 48 89 28                               |
    | mov qword [rax], rsi                                              | 48 89 30                               |
    | mov qword [rax], rdi                                              | 48 89 38                               |
    | mov qword [rax], r8                                               | 4c 89 00                               |
    | mov qword [rax], r9                                               | 4c 89 08                               |
    | mov qword [rax], r10                                              | 4c 89 10                               |
    | mov qword [rax], r11                                              | 4c 89 18                               |
    | mov qword [rax], r12                                              | 4c 89 20                               |
    | mov qword [rax], r13                                              | 4c 89 28                               |
    | mov qword [rax], r14                                              | 4c 89 30                               |
    | mov qword [rax], r15                                              | 4c 89 38                               |
    | mov qword [rcx], rdx                                              | 48 89 11                               |
    | mov qword [rdx], rbx                                              | 48 89 1a                               |
    | mov qword [rbx], rsp                                              | 48 89 23                               |
    | mov qword [rsp], rbp                                              | 48 89 2c 24                            |
    | mov qword [rbp], rsi                                              | 48 89 75 00                            |
    | mov qword [rsi], rdi                                              | 48 89 3e                               |
    | mov qword [rdi], r8                                               | 4c 89 07                               |
    | mov qword [r8], r9                                                | 4d 89 08                               |
    | mov qword [r9], r10                                               | 4d 89 11                               |
    | mov qword [r10], r11                                              | 4d 89 1a                               |
    | mov qword [r11], r12                                              | 4d 89 23                               |
    | mov qword [r12], r13                                              | 4d 89 2c 24                            |
    | mov qword [r13], r14                                              | 4d 89 75 00                            |
    | mov qword [r14], r15                                              | 4d 89 3e                               |
    | mov qword [r15], rax                                              | 49 89 07                               |
    | mov qword [rcx + 1 * rcx], rdx                                    | 48 89 14 09                            |
    | mov qword [rdx + 1 * rcx], rbx                                    | 48 89 1c 0a                            |
    | mov qword [rbx + 1 * rcx], rsp                                    | 48 89 24 0b                            |
    | mov qword [rsp + 1 * rcx], rbp                                    | 48 89 2c 0c                            |
    | mov qword [rbp + 1 * rcx], rsi                                    | 48 89 74 0d 00                         |
    | mov qword [rsi + 1 * rcx], rdi                                    | 48 89 3c 0e                            |
    | mov qword [rdi + 1 * rcx], r8                                     | 4c 89 04 0f                            |
    | mov qword [r8 + 1 * rcx], r9                                      | 4d 89 0c 08                            |
    | mov qword [r9 + 1 * rcx], r10                                     | 4d 89 14 09                            |
    | mov qword [r10 + 1 * rcx], r11                                    | 4d 89 1c 0a                            |
    | mov qword [r11 + 1 * rcx], r12                                    | 4d 89 24 0b                            |
    | mov qword [r12 + 1 * rcx], r13                                    | 4d 89 2c 0c                            |
    | mov qword [r13 + 1 * rcx], r14                                    | 4d 89 74 0d 00                         |
    | mov qword [r14 + 1 * rcx], r15                                    | 4d 89 3c 0e                            |
    | mov qword [r15 + 1 * rcx], rax                                    | 49 89 04 0f                            |
    | mov qword [rax + 1 * rdx], rdx                                    | 48 89 14 10                            |
    | mov qword [rax + 1 * rbx], rbx                                    | 48 89 1c 18                            |
    | mov qword [rax + 1 * rbp], rsp                                    | 48 89 24 28                            |
    | mov qword [rax + 1 * rsi], rbp                                    | 48 89 2c 30                            |
    | mov qword [rax + 1 * rdi], rsi                                    | 48 89 34 38                            |
    | mov qword [rax + 1 * r8], rdi                                     | 4a 89 3c 00                            |
    | mov qword [rax + 1 * r9], r8                                      | 4e 89 04 08                            |
    | mov qword [rax + 1 * r10], r9                                     | 4e 89 0c 10                            |
    | mov qword [rax + 1 * r11], r10                                    | 4e 89 14 18                            |
    | mov qword [rax + 1 * r12], r11                                    | 4e 89 1c 20                            |
    | mov qword [rax + 1 * r13], r12                                    | 4e 89 24 28                            |
    | mov qword [rax + 1 * r14], r13                                    | 4e 89 2c 30                            |
    | mov qword [rax + 1 * r15], r14                                    | 4e 89 34 38                            |
    | mov qword [rax + 2 * rcx], r15                                    | 4c 89 3c 48                            |
    | mov qword [rax + 4 * rcx], rax                                    | 48 89 04 88                            |
    | mov qword [r8 + 1 * r9], rdx                                      | 4b 89 14 08                            |
    | mov qword [r8 + 2 * r9], rbx                                      | 4b 89 1c 48                            |
    | mov qword [r8 + 4 * r9], rsp                                      | 4b 89 24 88                            |
    | mov qword [r8 + 8 * r9], rbp                                      | 4b 89 2c c8                            |
    | mov qword [1 * rcx], rsi                                          | 48 89 34 0d 00 00 00 00                |
    | mov qword [2 * rcx], rdi                                          | 48 89 3c 4d 00 00 00 00                |
    | mov qword [4 * rcx], r8                                           | 4c 89 04 8d 00 00 00 00                |
    | mov qword [8 * rcx], r9                                           | 4c 89 0c cd 00 00 00 00                |
    | mov qword [1 * r9], r10                                           | 4e 89 14 0d 00 00 00 00                |
    | mov qword [2 * r9], r11                                           | 4e 89 1c 4d 00 00 00 00                |
    | mov qword [4 * r9], r12                                           | 4e 89 24 8d 00 00 00 00                |
    | mov qword [8 * r9], r13                                           | 4e 89 2c cd 00 00 00 00                |
    | mov qword [r13 + 8 * r12], r14                                    | 4f 89 74 e5 00                         |
    | mov qword [rsp + 4 * r15], r15                                    | 4e 89 3c bc                            |
    | mov qword [rax + 1 * rcx + 0x00], rax                             | 48 89 44 08 00                         |
    | mov qword [rax + 1 * rcx + 0x01], rdx                             | 48 89 54 08 01                         |
    | mov qword [rax + 1 * rcx - 0x01], rbx                             | 48 89 5c 08 ff                         |
    | mov qword [rax + 1 * rcx + 0x00000001], rsp                       | 48 89 a4 08 01 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x00000001], rbp                       | 48 89 ac 08 ff ff ff ff                |
    | mov qword [rax + 1 * rcx + 0x7f], rsi                             | 48 89 74 08 7f                         |
    | mov qword [rax + 1 * rcx - 0x7f], rdi                             | 48 89 7c 08 81                         |
    | mov qword [rax + 1 * rcx + 0x80], r8                              | 4c 89 84 08 80 00 00 00                |
    | mov qword [rax + 1 * rcx - 0x80], r9                              | 4c 89 4c 08 80                         |
    | mov qword [rax + 1 * rcx - 0x81], r10                             | 4c 89 94 08 7f ff ff ff                |
    | mov qword [rax + 1 * rcx + 0xff], r11                             | 4c 89 9c 08 ff 00 00 00                |
    | mov qword [rax + 1 * rcx - 0xff], r12                             | 4c 89 a4 08 01 ff ff ff                |
    | mov qword [rax + 1 * rcx + 0x7fffffff], r13                       | 4c 89 ac 08 ff ff ff 7f                |
    | mov qword [rax + 1 * rcx - 0x7fffffff], r14                       | 4c 89 b4 08 01 00 00 80                |
    | mov qword [rax + 1 * rcx - 0x80000000], r15                       | 4c 89 bc 08 00 00 00 80                |
    | mov qword [r10 + 0x7f], rax                                       | 49 89 42 7f                            |
    | mov qword [r10 - 0x80], rdx                                       | 49 89 52 80                            |
    | mov qword [r10 - 0x81], rbx                                       | 49 89 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov qword [rel @prev5], rsp      | 90 90 90 90 90 48 89 25 f4 ff ff ff    |
    | .prev1: nop; mov qword [rel @prev1], rbp                          | 90 48 89 2d f8 ff ff ff                |
    | mov qword [rel @next1], rsi; nop; .next1: nop                     | 48 89 35 01 00 00 00 90 90             |
    | mov qword [rel @next5], rdi; nop; nop; nop; nop; nop; .next5: nop | 48 89 3d 05 00 00 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_mov_addr64_reg64():
    encode(MOV_ADDR64_REG64)


MOV_ADDR32_IMM32 = """
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
    | instruction                                                              | encoding                                        |
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
    | mov dword [rax], 0x00000001                                              | c7 00 01 00 00 00                               |
    | mov dword [rcx], 0x00000001                                              | c7 01 01 00 00 00                               |
    | mov dword [rdx], 0x00000001                                              | c7 02 01 00 00 00                               |
    | mov dword [rbx], 0x00000001                                              | c7 03 01 00 00 00                               |
    | mov dword [rsp], 0x00000001                                              | c7 04 24 01 00 00 00                            |
    | mov dword [rbp], 0x00000001                                              | c7 45 00 01 00 00 00                            |
    | mov dword [rsi], 0x00000001                                              | c7 06 01 00 00 00                               |
    | mov dword [rdi], 0x00000001                                              | c7 07 01 00 00 00                               |
    | mov dword [r8], 0x00000001                                               | 41 c7 00 01 00 00 00                            |
    | mov dword [r9], 0x00000001                                               | 41 c7 01 01 00 00 00                            |
    | mov dword [r10], 0x00000001                                              | 41 c7 02 01 00 00 00                            |
    | mov dword [r11], 0x00000001                                              | 41 c7 03 01 00 00 00                            |
    | mov dword [r12], 0x00000001                                              | 41 c7 04 24 01 00 00 00                         |
    | mov dword [r13], 0x00000001                                              | 41 c7 45 00 01 00 00 00                         |
    | mov dword [r14], 0x00000001                                              | 41 c7 06 01 00 00 00                            |
    | mov dword [r15], 0x00000001                                              | 41 c7 07 01 00 00 00                            |
    | mov dword [rax + 1 * rcx], 0x00000001                                    | c7 04 08 01 00 00 00                            |
    | mov dword [rcx + 1 * rcx], 0x00000001                                    | c7 04 09 01 00 00 00                            |
    | mov dword [rdx + 1 * rcx], 0x00000001                                    | c7 04 0a 01 00 00 00                            |
    | mov dword [rbx + 1 * rcx], 0x00000001                                    | c7 04 0b 01 00 00 00                            |
    | mov dword [rsp + 1 * rcx], 0x00000001                                    | c7 04 0c 01 00 00 00                            |
    | mov dword [rbp + 1 * rcx], 0x00000001                                    | c7 44 0d 00 01 00 00 00                         |
    | mov dword [rsi + 1 * rcx], 0x00000001                                    | c7 04 0e 01 00 00 00                            |
    | mov dword [rdi + 1 * rcx], 0x00000001                                    | c7 04 0f 01 00 00 00                            |
    | mov dword [r8 + 1 * rcx], 0x00000001                                     | 41 c7 04 08 01 00 00 00                         |
    | mov dword [r9 + 1 * rcx], 0x00000001                                     | 41 c7 04 09 01 00 00 00                         |
    | mov dword [r10 + 1 * rcx], 0x00000001                                    | 41 c7 04 0a 01 00 00 00                         |
    | mov dword [r11 + 1 * rcx], 0x00000001                                    | 41 c7 04 0b 01 00 00 00                         |
    | mov dword [r12 + 1 * rcx], 0x00000001                                    | 41 c7 04 0c 01 00 00 00                         |
    | mov dword [r13 + 1 * rcx], 0x00000001                                    | 41 c7 44 0d 00 01 00 00 00                      |
    | mov dword [r14 + 1 * rcx], 0x00000001                                    | 41 c7 04 0e 01 00 00 00                         |
    | mov dword [r15 + 1 * rcx], 0x00000001                                    | 41 c7 04 0f 01 00 00 00                         |
    | mov dword [rax + 1 * rax], 0x00000001                                    | c7 04 00 01 00 00 00                            |
    | mov dword [rax + 1 * rdx], 0x00000001                                    | c7 04 10 01 00 00 00                            |
    | mov dword [rax + 1 * rbx], 0x00000001                                    | c7 04 18 01 00 00 00                            |
    | mov dword [rax + 1 * rbp], 0x00000001                                    | c7 04 28 01 00 00 00                            |
    | mov dword [rax + 1 * rsi], 0x00000001                                    | c7 04 30 01 00 00 00                            |
    | mov dword [rax + 1 * rdi], 0x00000001                                    | c7 04 38 01 00 00 00                            |
    | mov dword [rax + 1 * r8], 0x00000001                                     | 42 c7 04 00 01 00 00 00                         |
    | mov dword [rax + 1 * r9], 0x00000001                                     | 42 c7 04 08 01 00 00 00                         |
    | mov dword [rax + 1 * r10], 0x00000001                                    | 42 c7 04 10 01 00 00 00                         |
    | mov dword [rax + 1 * r11], 0x00000001                                    | 42 c7 04 18 01 00 00 00                         |
    | mov dword [rax + 1 * r12], 0x00000001                                    | 42 c7 04 20 01 00 00 00                         |
    | mov dword [rax + 1 * r13], 0x00000001                                    | 42 c7 04 28 01 00 00 00                         |
    | mov dword [rax + 1 * r14], 0x00000001                                    | 42 c7 04 30 01 00 00 00                         |
    | mov dword [rax + 1 * r15], 0x00000001                                    | 42 c7 04 38 01 00 00 00                         |
    | mov dword [rax + 2 * rcx], 0x00000001                                    | c7 04 48 01 00 00 00                            |
    | mov dword [rax + 4 * rcx], 0x00000001                                    | c7 04 88 01 00 00 00                            |
    | mov dword [rax + 8 * rcx], 0x00000001                                    | c7 04 c8 01 00 00 00                            |
    | mov dword [r8 + 1 * r9], 0x00000001                                      | 43 c7 04 08 01 00 00 00                         |
    | mov dword [r8 + 2 * r9], 0x00000001                                      | 43 c7 04 48 01 00 00 00                         |
    | mov dword [r8 + 4 * r9], 0x00000001                                      | 43 c7 04 88 01 00 00 00                         |
    | mov dword [r8 + 8 * r9], 0x00000001                                      | 43 c7 04 c8 01 00 00 00                         |
    | mov dword [1 * rcx], 0x00000001                                          | c7 04 0d 00 00 00 00 01 00 00 00                |
    | mov dword [2 * rcx], 0x00000001                                          | c7 04 4d 00 00 00 00 01 00 00 00                |
    | mov dword [4 * rcx], 0x00000001                                          | c7 04 8d 00 00 00 00 01 00 00 00                |
    | mov dword [8 * rcx], 0x00000001                                          | c7 04 cd 00 00 00 00 01 00 00 00                |
    | mov dword [1 * r9], 0x00000001                                           | 42 c7 04 0d 00 00 00 00 01 00 00 00             |
    | mov dword [2 * r9], 0x00000001                                           | 42 c7 04 4d 00 00 00 00 01 00 00 00             |
    | mov dword [4 * r9], 0x00000001                                           | 42 c7 04 8d 00 00 00 00 01 00 00 00             |
    | mov dword [8 * r9], 0x00000001                                           | 42 c7 04 cd 00 00 00 00 01 00 00 00             |
    | mov dword [r13 + 8 * r12], 0x00000001                                    | 43 c7 44 e5 00 01 00 00 00                      |
    | mov dword [rsp + 4 * r15], 0x00000001                                    | 42 c7 04 bc 01 00 00 00                         |
    | mov dword [rax + 1 * rcx + 0x00], 0x00000001                             | c7 44 08 00 01 00 00 00                         |
    | mov dword [rax + 1 * rcx - 0x00], 0x00000001                             | c7 44 08 00 01 00 00 00                         |
    | mov dword [rax + 1 * rcx + 0x01], 0x00000001                             | c7 44 08 01 01 00 00 00                         |
    | mov dword [rax + 1 * rcx - 0x01], 0x00000001                             | c7 44 08 ff 01 00 00 00                         |
    | mov dword [rax + 1 * rcx + 0x00000001], 0x00000001                       | c7 84 08 01 00 00 00 01 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x00000001], 0x00000001                       | c7 84 08 ff ff ff ff 01 00 00 00                |
    | mov dword [rax + 1 * rcx + 0x7f], 0x00000001                             | c7 44 08 7f 01 00 00 00                         |
    | mov dword [rax + 1 * rcx - 0x7f], 0x00000001                             | c7 44 08 81 01 00 00 00                         |
    | mov dword [rax + 1 * rcx + 0x80], 0x00000001                             | c7 84 08 80 00 00 00 01 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x80], 0x00000001                             | c7 44 08 80 01 00 00 00                         |
    | mov dword [rax + 1 * rcx - 0x81], 0x00000001                             | c7 84 08 7f ff ff ff 01 00 00 00                |
    | mov dword [rax + 1 * rcx + 0xff], 0x00000001                             | c7 84 08 ff 00 00 00 01 00 00 00                |
    | mov dword [rax + 1 * rcx - 0xff], 0x00000001                             | c7 84 08 01 ff ff ff 01 00 00 00                |
    | mov dword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | c7 84 08 ff ff ff 7f 01 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | c7 84 08 01 00 00 80 01 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x80000000], 0x00000001                       | c7 84 08 00 00 00 80 01 00 00 00                |
    | mov dword [r10 + 0x7f], 0x00000001                                       | 41 c7 42 7f 01 00 00 00                         |
    | mov dword [r10 + 0x80], 0x00000001                                       | 41 c7 82 80 00 00 00 01 00 00 00                |
    | mov dword [r10 - 0x80], 0x00000001                                       | 41 c7 42 80 01 00 00 00                         |
    | mov dword [r10 - 0x81], 0x00000001                                       | 41 c7 82 7f ff ff ff 01 00 00 00                |
    | .prev5: nop; nop; nop; nop; nop; mov dword [rel @prev5], 0x00000001      | 90 90 90 90 90 c7 05 f1 ff ff ff 01 00 00 00    |
    | .prev1: nop; mov dword [rel @prev1], 0x00000001                          | 90 c7 05 f5 ff ff ff 01 00 00 00                |
    | mov dword [rel @next1], 0x00000001; nop; .next1: nop                     | c7 05 01 00 00 00 01 00 00 00 90 90             |
    | mov dword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | c7 05 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | mov dword [rax], 0x00000000                                              | c7 00 00 00 00 00                               |
    | mov dword [rax], 0x0000007f                                              | c7 00 7f 00 00 00                               |
    | mov dword [rax], 0x00000080                                              | c7 00 80 00 00 00                               |
    | mov dword [rax], 0x000000ff                                              | c7 00 ff 00 00 00                               |
    | mov dword [rax], 0x00000100                                              | c7 00 00 01 00 00                               |
    | mov dword [rax], 0x00007fff                                              | c7 00 ff 7f 00 00                               |
    | mov dword [rax], 0x00008000                                              | c7 00 00 80 00 00                               |
    | mov dword [rax], 0x0000ffff                                              | c7 00 ff ff 00 00                               |
    | mov dword [rax], 0x00010000                                              | c7 00 00 00 01 00                               |
    | mov dword [rax], 0x7fffffff                                              | c7 00 ff ff ff 7f                               |
    | mov dword [rax], 0x80000000                                              | c7 00 00 00 00 80                               |
    | mov dword [rax], 0xffffffff                                              | c7 00 ff ff ff ff                               |
    | mov dword [rcx], 0x0000007f                                              | c7 01 7f 00 00 00                               |
    | mov dword [rdx], 0x00000080                                              | c7 02 80 00 00 00                               |
    | mov dword [rbx], 0x000000ff                                              | c7 03 ff 00 00 00                               |
    | mov dword [rsp], 0x00000100                                              | c7 04 24 00 01 00 00                            |
    | mov dword [rbp], 0x00007fff                                              | c7 45 00 ff 7f 00 00                            |
    | mov dword [rsi], 0x00008000                                              | c7 06 00 80 00 00                               |
    | mov dword [rdi], 0x0000ffff                                              | c7 07 ff ff 00 00                               |
    | mov dword [r8], 0x00010000                                               | 41 c7 00 00 00 01 00                            |
    | mov dword [r9], 0x7fffffff                                               | 41 c7 01 ff ff ff 7f                            |
    | mov dword [r10], 0x80000000                                              | 41 c7 02 00 00 00 80                            |
    | mov dword [r11], 0xffffffff                                              | 41 c7 03 ff ff ff ff                            |
    | mov dword [r12], 0x00000000                                              | 41 c7 04 24 00 00 00 00                         |
    | mov dword [r14], 0x0000007f                                              | 41 c7 06 7f 00 00 00                            |
    | mov dword [r15], 0x00000080                                              | 41 c7 07 80 00 00 00                            |
    | mov dword [rax + 1 * rcx], 0x000000ff                                    | c7 04 08 ff 00 00 00                            |
    | mov dword [rcx + 1 * rcx], 0x00000100                                    | c7 04 09 00 01 00 00                            |
    | mov dword [rdx + 1 * rcx], 0x00007fff                                    | c7 04 0a ff 7f 00 00                            |
    | mov dword [rbx + 1 * rcx], 0x00008000                                    | c7 04 0b 00 80 00 00                            |
    | mov dword [rsp + 1 * rcx], 0x0000ffff                                    | c7 04 0c ff ff 00 00                            |
    | mov dword [rbp + 1 * rcx], 0x00010000                                    | c7 44 0d 00 00 00 01 00                         |
    | mov dword [rsi + 1 * rcx], 0x7fffffff                                    | c7 04 0e ff ff ff 7f                            |
    | mov dword [rdi + 1 * rcx], 0x80000000                                    | c7 04 0f 00 00 00 80                            |
    | mov dword [r8 + 1 * rcx], 0xffffffff                                     | 41 c7 04 08 ff ff ff ff                         |
    | mov dword [r9 + 1 * rcx], 0x00000000                                     | 41 c7 04 09 00 00 00 00                         |
    | mov dword [r11 + 1 * rcx], 0x0000007f                                    | 41 c7 04 0b 7f 00 00 00                         |
    | mov dword [r12 + 1 * rcx], 0x00000080                                    | 41 c7 04 0c 80 00 00 00                         |
    | mov dword [r13 + 1 * rcx], 0x000000ff                                    | 41 c7 44 0d 00 ff 00 00 00                      |
    | mov dword [r14 + 1 * rcx], 0x00000100                                    | 41 c7 04 0e 00 01 00 00                         |
    | mov dword [r15 + 1 * rcx], 0x00007fff                                    | 41 c7 04 0f ff 7f 00 00                         |
    | mov dword [rax + 1 * rax], 0x00008000                                    | c7 04 00 00 80 00 00                            |
    | mov dword [rax + 1 * rdx], 0x0000ffff                                    | c7 04 10 ff ff 00 00                            |
    | mov dword [rax + 1 * rbx], 0x00010000                                    | c7 04 18 00 00 01 00                            |
    | mov dword [rax + 1 * rbp], 0x7fffffff                                    | c7 04 28 ff ff ff 7f                            |
    | mov dword [rax + 1 * rsi], 0x80000000                                    | c7 04 30 00 00 00 80                            |
    | mov dword [rax + 1 * rdi], 0xffffffff                                    | c7 04 38 ff ff ff ff                            |
    | mov dword [rax + 1 * r8], 0x00000000                                     | 42 c7 04 00 00 00 00 00                         |
    | mov dword [rax + 1 * r10], 0x0000007f                                    | 42 c7 04 10 7f 00 00 00                         |
    | mov dword [rax + 1 * r11], 0x00000080                                    | 42 c7 04 18 80 00 00 00                         |
    | mov dword [rax + 1 * r12], 0x000000ff                                    | 42 c7 04 20 ff 00 00 00                         |
    | mov dword [rax + 1 * r13], 0x00000100                                    | 42 c7 04 28 00 01 00 00                         |
    | mov dword [rax + 1 * r14], 0x00007fff                                    | 42 c7 04 30 ff 7f 00 00                         |
    | mov dword [rax + 1 * r15], 0x00008000                                    | 42 c7 04 38 00 80 00 00                         |
    | mov dword [rax + 2 * rcx], 0x0000ffff                                    | c7 04 48 ff ff 00 00                            |
    | mov dword [rax + 4 * rcx], 0x00010000                                    | c7 04 88 00 00 01 00                            |
    | mov dword [rax + 8 * rcx], 0x7fffffff                                    | c7 04 c8 ff ff ff 7f                            |
    | mov dword [r8 + 1 * r9], 0x80000000                                      | 43 c7 04 08 00 00 00 80                         |
    | mov dword [r8 + 2 * r9], 0xffffffff                                      | 43 c7 04 48 ff ff ff ff                         |
    | mov dword [r8 + 4 * r9], 0x00000000                                      | 43 c7 04 88 00 00 00 00                         |
    | mov dword [1 * rcx], 0x0000007f                                          | c7 04 0d 00 00 00 00 7f 00 00 00                |
    | mov dword [2 * rcx], 0x00000080                                          | c7 04 4d 00 00 00 00 80 00 00 00                |
    | mov dword [4 * rcx], 0x000000ff                                          | c7 04 8d 00 00 00 00 ff 00 00 00                |
    | mov dword [8 * rcx], 0x00000100                                          | c7 04 cd 00 00 00 00 00 01 00 00                |
    | mov dword [1 * r9], 0x00007fff                                           | 42 c7 04 0d 00 00 00 00 ff 7f 00 00             |
    | mov dword [2 * r9], 0x00008000                                           | 42 c7 04 4d 00 00 00 00 00 80 00 00             |
    | mov dword [4 * r9], 0x0000ffff                                           | 42 c7 04 8d 00 00 00 00 ff ff 00 00             |
    | mov dword [8 * r9], 0x00010000                                           | 42 c7 04 cd 00 00 00 00 00 00 01 00             |
    | mov dword [r13 + 8 * r12], 0x7fffffff                                    | 43 c7 44 e5 00 ff ff ff 7f                      |
    | mov dword [rsp + 4 * r15], 0x80000000                                    | 42 c7 04 bc 00 00 00 80                         |
    | mov dword [rax + 1 * rcx + 0x00], 0xffffffff                             | c7 44 08 00 ff ff ff ff                         |
    | mov dword [rax + 1 * rcx - 0x00], 0x00000000                             | c7 44 08 00 00 00 00 00                         |
    | mov dword [rax + 1 * rcx - 0x01], 0x0000007f                             | c7 44 08 ff 7f 00 00 00                         |
    | mov dword [rax + 1 * rcx + 0x00000001], 0x00000080                       | c7 84 08 01 00 00 00 80 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | c7 84 08 ff ff ff ff ff 00 00 00                |
    | mov dword [rax + 1 * rcx + 0x7f], 0x00000100                             | c7 44 08 7f 00 01 00 00                         |
    | mov dword [rax + 1 * rcx - 0x7f], 0x00007fff                             | c7 44 08 81 ff 7f 00 00                         |
    | mov dword [rax + 1 * rcx + 0x80], 0x00008000                             | c7 84 08 80 00 00 00 00 80 00 00                |
    | mov dword [rax + 1 * rcx - 0x80], 0x0000ffff                             | c7 44 08 80 ff ff 00 00                         |
    | mov dword [rax + 1 * rcx - 0x81], 0x00010000                             | c7 84 08 7f ff ff ff 00 00 01 00                |
    | mov dword [rax + 1 * rcx + 0xff], 0x7fffffff                             | c7 84 08 ff 00 00 00 ff ff ff 7f                |
    | mov dword [rax + 1 * rcx - 0xff], 0x80000000                             | c7 84 08 01 ff ff ff 00 00 00 80                |
    | mov dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | c7 84 08 ff ff ff 7f ff ff ff ff                |
    | mov dword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | c7 84 08 01 00 00 80 00 00 00 00                |
    | mov dword [r10 + 0x7f], 0x0000007f                                       | 41 c7 42 7f 7f 00 00 00                         |
    | mov dword [r10 + 0x80], 0x00000080                                       | 41 c7 82 80 00 00 00 80 00 00 00                |
    | mov dword [r10 - 0x80], 0x000000ff                                       | 41 c7 42 80 ff 00 00 00                         |
    | mov dword [r10 - 0x81], 0x00000100                                       | 41 c7 82 7f ff ff ff 00 01 00 00                |
    | .prev5: nop; nop; nop; nop; nop; mov dword [rel @prev5], 0x00007fff      | 90 90 90 90 90 c7 05 f1 ff ff ff ff 7f 00 00    |
    | .prev1: nop; mov dword [rel @prev1], 0x00008000                          | 90 c7 05 f5 ff ff ff 00 80 00 00                |
    | mov dword [rel @next1], 0x0000ffff; nop; .next1: nop                     | c7 05 01 00 00 00 ff ff 00 00 90 90             |
    | mov dword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | c7 05 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
"""


def can_encode_mov_addr32_imm32():
    encode(MOV_ADDR32_IMM32)


MOV_ADDR32_REG32 = """
    | ----------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                       | encoding                            |
    | ----------------------------------------------------------------- | ----------------------------------- |
    | mov dword [rax], ecx                                              | 89 08                               |
    | mov dword [rcx], ecx                                              | 89 09                               |
    | mov dword [rdx], ecx                                              | 89 0a                               |
    | mov dword [rbx], ecx                                              | 89 0b                               |
    | mov dword [rsp], ecx                                              | 89 0c 24                            |
    | mov dword [rbp], ecx                                              | 89 4d 00                            |
    | mov dword [rsi], ecx                                              | 89 0e                               |
    | mov dword [rdi], ecx                                              | 89 0f                               |
    | mov dword [r8], ecx                                               | 41 89 08                            |
    | mov dword [r9], ecx                                               | 41 89 09                            |
    | mov dword [r10], ecx                                              | 41 89 0a                            |
    | mov dword [r11], ecx                                              | 41 89 0b                            |
    | mov dword [r12], ecx                                              | 41 89 0c 24                         |
    | mov dword [r13], ecx                                              | 41 89 4d 00                         |
    | mov dword [r14], ecx                                              | 41 89 0e                            |
    | mov dword [r15], ecx                                              | 41 89 0f                            |
    | mov dword [rax + 1 * rcx], ecx                                    | 89 0c 08                            |
    | mov dword [rcx + 1 * rcx], ecx                                    | 89 0c 09                            |
    | mov dword [rdx + 1 * rcx], ecx                                    | 89 0c 0a                            |
    | mov dword [rbx + 1 * rcx], ecx                                    | 89 0c 0b                            |
    | mov dword [rsp + 1 * rcx], ecx                                    | 89 0c 0c                            |
    | mov dword [rbp + 1 * rcx], ecx                                    | 89 4c 0d 00                         |
    | mov dword [rsi + 1 * rcx], ecx                                    | 89 0c 0e                            |
    | mov dword [rdi + 1 * rcx], ecx                                    | 89 0c 0f                            |
    | mov dword [r8 + 1 * rcx], ecx                                     | 41 89 0c 08                         |
    | mov dword [r9 + 1 * rcx], ecx                                     | 41 89 0c 09                         |
    | mov dword [r10 + 1 * rcx], ecx                                    | 41 89 0c 0a                         |
    | mov dword [r11 + 1 * rcx], ecx                                    | 41 89 0c 0b                         |
    | mov dword [r12 + 1 * rcx], ecx                                    | 41 89 0c 0c                         |
    | mov dword [r13 + 1 * rcx], ecx                                    | 41 89 4c 0d 00                      |
    | mov dword [r14 + 1 * rcx], ecx                                    | 41 89 0c 0e                         |
    | mov dword [r15 + 1 * rcx], ecx                                    | 41 89 0c 0f                         |
    | mov dword [rax + 1 * rax], ecx                                    | 89 0c 00                            |
    | mov dword [rax + 1 * rdx], ecx                                    | 89 0c 10                            |
    | mov dword [rax + 1 * rbx], ecx                                    | 89 0c 18                            |
    | mov dword [rax + 1 * rbp], ecx                                    | 89 0c 28                            |
    | mov dword [rax + 1 * rsi], ecx                                    | 89 0c 30                            |
    | mov dword [rax + 1 * rdi], ecx                                    | 89 0c 38                            |
    | mov dword [rax + 1 * r8], ecx                                     | 42 89 0c 00                         |
    | mov dword [rax + 1 * r9], ecx                                     | 42 89 0c 08                         |
    | mov dword [rax + 1 * r10], ecx                                    | 42 89 0c 10                         |
    | mov dword [rax + 1 * r11], ecx                                    | 42 89 0c 18                         |
    | mov dword [rax + 1 * r12], ecx                                    | 42 89 0c 20                         |
    | mov dword [rax + 1 * r13], ecx                                    | 42 89 0c 28                         |
    | mov dword [rax + 1 * r14], ecx                                    | 42 89 0c 30                         |
    | mov dword [rax + 1 * r15], ecx                                    | 42 89 0c 38                         |
    | mov dword [rax + 2 * rcx], ecx                                    | 89 0c 48                            |
    | mov dword [rax + 4 * rcx], ecx                                    | 89 0c 88                            |
    | mov dword [rax + 8 * rcx], ecx                                    | 89 0c c8                            |
    | mov dword [r8 + 1 * r9], ecx                                      | 43 89 0c 08                         |
    | mov dword [r8 + 2 * r9], ecx                                      | 43 89 0c 48                         |
    | mov dword [r8 + 4 * r9], ecx                                      | 43 89 0c 88                         |
    | mov dword [r8 + 8 * r9], ecx                                      | 43 89 0c c8                         |
    | mov dword [1 * rcx], ecx                                          | 89 0c 0d 00 00 00 00                |
    | mov dword [2 * rcx], ecx                                          | 89 0c 4d 00 00 00 00                |
    | mov dword [4 * rcx], ecx                                          | 89 0c 8d 00 00 00 00                |
    | mov dword [8 * rcx], ecx                                          | 89 0c cd 00 00 00 00                |
    | mov dword [1 * r9], ecx                                           | 42 89 0c 0d 00 00 00 00             |
    | mov dword [2 * r9], ecx                                           | 42 89 0c 4d 00 00 00 00             |
    | mov dword [4 * r9], ecx                                           | 42 89 0c 8d 00 00 00 00             |
    | mov dword [8 * r9], ecx                                           | 42 89 0c cd 00 00 00 00             |
    | mov dword [r13 + 8 * r12], ecx                                    | 43 89 4c e5 00                      |
    | mov dword [rsp + 4 * r15], ecx                                    | 42 89 0c bc                         |
    | mov dword [rax + 1 * rcx + 0x00], ecx                             | 89 4c 08 00                         |
    | mov dword [rax + 1 * rcx - 0x00], ecx                             | 89 4c 08 00                         |
    | mov dword [rax + 1 * rcx + 0x01], ecx                             | 89 4c 08 01                         |
    | mov dword [rax + 1 * rcx - 0x01], ecx                             | 89 4c 08 ff                         |
    | mov dword [rax + 1 * rcx + 0x00000001], ecx                       | 89 8c 08 01 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x00000001], ecx                       | 89 8c 08 ff ff ff ff                |
    | mov dword [rax + 1 * rcx + 0x7f], ecx                             | 89 4c 08 7f                         |
    | mov dword [rax + 1 * rcx - 0x7f], ecx                             | 89 4c 08 81                         |
    | mov dword [rax + 1 * rcx + 0x80], ecx                             | 89 8c 08 80 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x80], ecx                             | 89 4c 08 80                         |
    | mov dword [rax + 1 * rcx - 0x81], ecx                             | 89 8c 08 7f ff ff ff                |
    | mov dword [rax + 1 * rcx + 0xff], ecx                             | 89 8c 08 ff 00 00 00                |
    | mov dword [rax + 1 * rcx - 0xff], ecx                             | 89 8c 08 01 ff ff ff                |
    | mov dword [rax + 1 * rcx + 0x7fffffff], ecx                       | 89 8c 08 ff ff ff 7f                |
    | mov dword [rax + 1 * rcx - 0x7fffffff], ecx                       | 89 8c 08 01 00 00 80                |
    | mov dword [rax + 1 * rcx - 0x80000000], ecx                       | 89 8c 08 00 00 00 80                |
    | mov dword [r10 + 0x7f], ecx                                       | 41 89 4a 7f                         |
    | mov dword [r10 + 0x80], ecx                                       | 41 89 8a 80 00 00 00                |
    | mov dword [r10 - 0x80], ecx                                       | 41 89 4a 80                         |
    | mov dword [r10 - 0x81], ecx                                       | 41 89 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov dword [rel @prev5], ecx      | 90 90 90 90 90 89 0d f5 ff ff ff    |
    | .prev1: nop; mov dword [rel @prev1], ecx                          | 90 89 0d f9 ff ff ff                |
    | mov dword [rel @next1], ecx; nop; .next1: nop                     | 89 0d 01 00 00 00 90 90             |
    | mov dword [rel @next5], ecx; nop; nop; nop; nop; nop; .next5: nop | 89 0d 05 00 00 00 90 90 90 90 90 90 |
    | mov dword [rax], eax                                              | 89 00                               |
    | mov dword [rax], edx                                              | 89 10                               |
    | mov dword [rax], ebx                                              | 89 18                               |
    | mov dword [rax], esp                                              | 89 20                               |
    | mov dword [rax], ebp                                              | 89 28                               |
    | mov dword [rax], esi                                              | 89 30                               |
    | mov dword [rax], edi                                              | 89 38                               |
    | mov dword [rax], r8d                                              | 44 89 00                            |
    | mov dword [rax], r9d                                              | 44 89 08                            |
    | mov dword [rax], r10d                                             | 44 89 10                            |
    | mov dword [rax], r11d                                             | 44 89 18                            |
    | mov dword [rax], r12d                                             | 44 89 20                            |
    | mov dword [rax], r13d                                             | 44 89 28                            |
    | mov dword [rax], r14d                                             | 44 89 30                            |
    | mov dword [rax], r15d                                             | 44 89 38                            |
    | mov dword [rcx], edx                                              | 89 11                               |
    | mov dword [rdx], ebx                                              | 89 1a                               |
    | mov dword [rbx], esp                                              | 89 23                               |
    | mov dword [rsp], ebp                                              | 89 2c 24                            |
    | mov dword [rbp], esi                                              | 89 75 00                            |
    | mov dword [rsi], edi                                              | 89 3e                               |
    | mov dword [rdi], r8d                                              | 44 89 07                            |
    | mov dword [r8], r9d                                               | 45 89 08                            |
    | mov dword [r9], r10d                                              | 45 89 11                            |
    | mov dword [r10], r11d                                             | 45 89 1a                            |
    | mov dword [r11], r12d                                             | 45 89 23                            |
    | mov dword [r12], r13d                                             | 45 89 2c 24                         |
    | mov dword [r13], r14d                                             | 45 89 75 00                         |
    | mov dword [r14], r15d                                             | 45 89 3e                            |
    | mov dword [r15], eax                                              | 41 89 07                            |
    | mov dword [rcx + 1 * rcx], edx                                    | 89 14 09                            |
    | mov dword [rdx + 1 * rcx], ebx                                    | 89 1c 0a                            |
    | mov dword [rbx + 1 * rcx], esp                                    | 89 24 0b                            |
    | mov dword [rsp + 1 * rcx], ebp                                    | 89 2c 0c                            |
    | mov dword [rbp + 1 * rcx], esi                                    | 89 74 0d 00                         |
    | mov dword [rsi + 1 * rcx], edi                                    | 89 3c 0e                            |
    | mov dword [rdi + 1 * rcx], r8d                                    | 44 89 04 0f                         |
    | mov dword [r8 + 1 * rcx], r9d                                     | 45 89 0c 08                         |
    | mov dword [r9 + 1 * rcx], r10d                                    | 45 89 14 09                         |
    | mov dword [r10 + 1 * rcx], r11d                                   | 45 89 1c 0a                         |
    | mov dword [r11 + 1 * rcx], r12d                                   | 45 89 24 0b                         |
    | mov dword [r12 + 1 * rcx], r13d                                   | 45 89 2c 0c                         |
    | mov dword [r13 + 1 * rcx], r14d                                   | 45 89 74 0d 00                      |
    | mov dword [r14 + 1 * rcx], r15d                                   | 45 89 3c 0e                         |
    | mov dword [r15 + 1 * rcx], eax                                    | 41 89 04 0f                         |
    | mov dword [rax + 1 * rdx], edx                                    | 89 14 10                            |
    | mov dword [rax + 1 * rbx], ebx                                    | 89 1c 18                            |
    | mov dword [rax + 1 * rbp], esp                                    | 89 24 28                            |
    | mov dword [rax + 1 * rsi], ebp                                    | 89 2c 30                            |
    | mov dword [rax + 1 * rdi], esi                                    | 89 34 38                            |
    | mov dword [rax + 1 * r8], edi                                     | 42 89 3c 00                         |
    | mov dword [rax + 1 * r9], r8d                                     | 46 89 04 08                         |
    | mov dword [rax + 1 * r10], r9d                                    | 46 89 0c 10                         |
    | mov dword [rax + 1 * r11], r10d                                   | 46 89 14 18                         |
    | mov dword [rax + 1 * r12], r11d                                   | 46 89 1c 20                         |
    | mov dword [rax + 1 * r13], r12d                                   | 46 89 24 28                         |
    | mov dword [rax + 1 * r14], r13d                                   | 46 89 2c 30                         |
    | mov dword [rax + 1 * r15], r14d                                   | 46 89 34 38                         |
    | mov dword [rax + 2 * rcx], r15d                                   | 44 89 3c 48                         |
    | mov dword [rax + 4 * rcx], eax                                    | 89 04 88                            |
    | mov dword [r8 + 1 * r9], edx                                      | 43 89 14 08                         |
    | mov dword [r8 + 2 * r9], ebx                                      | 43 89 1c 48                         |
    | mov dword [r8 + 4 * r9], esp                                      | 43 89 24 88                         |
    | mov dword [r8 + 8 * r9], ebp                                      | 43 89 2c c8                         |
    | mov dword [1 * rcx], esi                                          | 89 34 0d 00 00 00 00                |
    | mov dword [2 * rcx], edi                                          | 89 3c 4d 00 00 00 00                |
    | mov dword [4 * rcx], r8d                                          | 44 89 04 8d 00 00 00 00             |
    | mov dword [8 * rcx], r9d                                          | 44 89 0c cd 00 00 00 00             |
    | mov dword [1 * r9], r10d                                          | 46 89 14 0d 00 00 00 00             |
    | mov dword [2 * r9], r11d                                          | 46 89 1c 4d 00 00 00 00             |
    | mov dword [4 * r9], r12d                                          | 46 89 24 8d 00 00 00 00             |
    | mov dword [8 * r9], r13d                                          | 46 89 2c cd 00 00 00 00             |
    | mov dword [r13 + 8 * r12], r14d                                   | 47 89 74 e5 00                      |
    | mov dword [rsp + 4 * r15], r15d                                   | 46 89 3c bc                         |
    | mov dword [rax + 1 * rcx + 0x00], eax                             | 89 44 08 00                         |
    | mov dword [rax + 1 * rcx + 0x01], edx                             | 89 54 08 01                         |
    | mov dword [rax + 1 * rcx - 0x01], ebx                             | 89 5c 08 ff                         |
    | mov dword [rax + 1 * rcx + 0x00000001], esp                       | 89 a4 08 01 00 00 00                |
    | mov dword [rax + 1 * rcx - 0x00000001], ebp                       | 89 ac 08 ff ff ff ff                |
    | mov dword [rax + 1 * rcx + 0x7f], esi                             | 89 74 08 7f                         |
    | mov dword [rax + 1 * rcx - 0x7f], edi                             | 89 7c 08 81                         |
    | mov dword [rax + 1 * rcx + 0x80], r8d                             | 44 89 84 08 80 00 00 00             |
    | mov dword [rax + 1 * rcx - 0x80], r9d                             | 44 89 4c 08 80                      |
    | mov dword [rax + 1 * rcx - 0x81], r10d                            | 44 89 94 08 7f ff ff ff             |
    | mov dword [rax + 1 * rcx + 0xff], r11d                            | 44 89 9c 08 ff 00 00 00             |
    | mov dword [rax + 1 * rcx - 0xff], r12d                            | 44 89 a4 08 01 ff ff ff             |
    | mov dword [rax + 1 * rcx + 0x7fffffff], r13d                      | 44 89 ac 08 ff ff ff 7f             |
    | mov dword [rax + 1 * rcx - 0x7fffffff], r14d                      | 44 89 b4 08 01 00 00 80             |
    | mov dword [rax + 1 * rcx - 0x80000000], r15d                      | 44 89 bc 08 00 00 00 80             |
    | mov dword [r10 + 0x7f], eax                                       | 41 89 42 7f                         |
    | mov dword [r10 - 0x80], edx                                       | 41 89 52 80                         |
    | mov dword [r10 - 0x81], ebx                                       | 41 89 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov dword [rel @prev5], esp      | 90 90 90 90 90 89 25 f5 ff ff ff    |
    | .prev1: nop; mov dword [rel @prev1], ebp                          | 90 89 2d f9 ff ff ff                |
    | mov dword [rel @next1], esi; nop; .next1: nop                     | 89 35 01 00 00 00 90 90             |
    | mov dword [rel @next5], edi; nop; nop; nop; nop; nop; .next5: nop | 89 3d 05 00 00 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_mov_addr32_reg32():
    encode(MOV_ADDR32_REG32)


MOV_ADDR16_IMM16 = """
    | ------------------------------------------------------------------- | -------------------------------------------- |
    | instruction                                                         | encoding                                     |
    | ------------------------------------------------------------------- | -------------------------------------------- |
    | mov word [rax], 0x0001                                              | 66 c7 00 01 00                               |
    | mov word [rcx], 0x0001                                              | 66 c7 01 01 00                               |
    | mov word [rdx], 0x0001                                              | 66 c7 02 01 00                               |
    | mov word [rbx], 0x0001                                              | 66 c7 03 01 00                               |
    | mov word [rsp], 0x0001                                              | 66 c7 04 24 01 00                            |
    | mov word [rbp], 0x0001                                              | 66 c7 45 00 01 00                            |
    | mov word [rsi], 0x0001                                              | 66 c7 06 01 00                               |
    | mov word [rdi], 0x0001                                              | 66 c7 07 01 00                               |
    | mov word [r8], 0x0001                                               | 66 41 c7 00 01 00                            |
    | mov word [r9], 0x0001                                               | 66 41 c7 01 01 00                            |
    | mov word [r10], 0x0001                                              | 66 41 c7 02 01 00                            |
    | mov word [r11], 0x0001                                              | 66 41 c7 03 01 00                            |
    | mov word [r12], 0x0001                                              | 66 41 c7 04 24 01 00                         |
    | mov word [r13], 0x0001                                              | 66 41 c7 45 00 01 00                         |
    | mov word [r14], 0x0001                                              | 66 41 c7 06 01 00                            |
    | mov word [r15], 0x0001                                              | 66 41 c7 07 01 00                            |
    | mov word [rax + 1 * rcx], 0x0001                                    | 66 c7 04 08 01 00                            |
    | mov word [rcx + 1 * rcx], 0x0001                                    | 66 c7 04 09 01 00                            |
    | mov word [rdx + 1 * rcx], 0x0001                                    | 66 c7 04 0a 01 00                            |
    | mov word [rbx + 1 * rcx], 0x0001                                    | 66 c7 04 0b 01 00                            |
    | mov word [rsp + 1 * rcx], 0x0001                                    | 66 c7 04 0c 01 00                            |
    | mov word [rbp + 1 * rcx], 0x0001                                    | 66 c7 44 0d 00 01 00                         |
    | mov word [rsi + 1 * rcx], 0x0001                                    | 66 c7 04 0e 01 00                            |
    | mov word [rdi + 1 * rcx], 0x0001                                    | 66 c7 04 0f 01 00                            |
    | mov word [r8 + 1 * rcx], 0x0001                                     | 66 41 c7 04 08 01 00                         |
    | mov word [r9 + 1 * rcx], 0x0001                                     | 66 41 c7 04 09 01 00                         |
    | mov word [r10 + 1 * rcx], 0x0001                                    | 66 41 c7 04 0a 01 00                         |
    | mov word [r11 + 1 * rcx], 0x0001                                    | 66 41 c7 04 0b 01 00                         |
    | mov word [r12 + 1 * rcx], 0x0001                                    | 66 41 c7 04 0c 01 00                         |
    | mov word [r13 + 1 * rcx], 0x0001                                    | 66 41 c7 44 0d 00 01 00                      |
    | mov word [r14 + 1 * rcx], 0x0001                                    | 66 41 c7 04 0e 01 00                         |
    | mov word [r15 + 1 * rcx], 0x0001                                    | 66 41 c7 04 0f 01 00                         |
    | mov word [rax + 1 * rax], 0x0001                                    | 66 c7 04 00 01 00                            |
    | mov word [rax + 1 * rdx], 0x0001                                    | 66 c7 04 10 01 00                            |
    | mov word [rax + 1 * rbx], 0x0001                                    | 66 c7 04 18 01 00                            |
    | mov word [rax + 1 * rbp], 0x0001                                    | 66 c7 04 28 01 00                            |
    | mov word [rax + 1 * rsi], 0x0001                                    | 66 c7 04 30 01 00                            |
    | mov word [rax + 1 * rdi], 0x0001                                    | 66 c7 04 38 01 00                            |
    | mov word [rax + 1 * r8], 0x0001                                     | 66 42 c7 04 00 01 00                         |
    | mov word [rax + 1 * r9], 0x0001                                     | 66 42 c7 04 08 01 00                         |
    | mov word [rax + 1 * r10], 0x0001                                    | 66 42 c7 04 10 01 00                         |
    | mov word [rax + 1 * r11], 0x0001                                    | 66 42 c7 04 18 01 00                         |
    | mov word [rax + 1 * r12], 0x0001                                    | 66 42 c7 04 20 01 00                         |
    | mov word [rax + 1 * r13], 0x0001                                    | 66 42 c7 04 28 01 00                         |
    | mov word [rax + 1 * r14], 0x0001                                    | 66 42 c7 04 30 01 00                         |
    | mov word [rax + 1 * r15], 0x0001                                    | 66 42 c7 04 38 01 00                         |
    | mov word [rax + 2 * rcx], 0x0001                                    | 66 c7 04 48 01 00                            |
    | mov word [rax + 4 * rcx], 0x0001                                    | 66 c7 04 88 01 00                            |
    | mov word [rax + 8 * rcx], 0x0001                                    | 66 c7 04 c8 01 00                            |
    | mov word [r8 + 1 * r9], 0x0001                                      | 66 43 c7 04 08 01 00                         |
    | mov word [r8 + 2 * r9], 0x0001                                      | 66 43 c7 04 48 01 00                         |
    | mov word [r8 + 4 * r9], 0x0001                                      | 66 43 c7 04 88 01 00                         |
    | mov word [r8 + 8 * r9], 0x0001                                      | 66 43 c7 04 c8 01 00                         |
    | mov word [1 * rcx], 0x0001                                          | 66 c7 04 0d 00 00 00 00 01 00                |
    | mov word [2 * rcx], 0x0001                                          | 66 c7 04 4d 00 00 00 00 01 00                |
    | mov word [4 * rcx], 0x0001                                          | 66 c7 04 8d 00 00 00 00 01 00                |
    | mov word [8 * rcx], 0x0001                                          | 66 c7 04 cd 00 00 00 00 01 00                |
    | mov word [1 * r9], 0x0001                                           | 66 42 c7 04 0d 00 00 00 00 01 00             |
    | mov word [2 * r9], 0x0001                                           | 66 42 c7 04 4d 00 00 00 00 01 00             |
    | mov word [4 * r9], 0x0001                                           | 66 42 c7 04 8d 00 00 00 00 01 00             |
    | mov word [8 * r9], 0x0001                                           | 66 42 c7 04 cd 00 00 00 00 01 00             |
    | mov word [r13 + 8 * r12], 0x0001                                    | 66 43 c7 44 e5 00 01 00                      |
    | mov word [rsp + 4 * r15], 0x0001                                    | 66 42 c7 04 bc 01 00                         |
    | mov word [rax + 1 * rcx + 0x00], 0x0001                             | 66 c7 44 08 00 01 00                         |
    | mov word [rax + 1 * rcx - 0x00], 0x0001                             | 66 c7 44 08 00 01 00                         |
    | mov word [rax + 1 * rcx + 0x01], 0x0001                             | 66 c7 44 08 01 01 00                         |
    | mov word [rax + 1 * rcx - 0x01], 0x0001                             | 66 c7 44 08 ff 01 00                         |
    | mov word [rax + 1 * rcx + 0x00000001], 0x0001                       | 66 c7 84 08 01 00 00 00 01 00                |
    | mov word [rax + 1 * rcx - 0x00000001], 0x0001                       | 66 c7 84 08 ff ff ff ff 01 00                |
    | mov word [rax + 1 * rcx + 0x7f], 0x0001                             | 66 c7 44 08 7f 01 00                         |
    | mov word [rax + 1 * rcx - 0x7f], 0x0001                             | 66 c7 44 08 81 01 00                         |
    | mov word [rax + 1 * rcx + 0x80], 0x0001                             | 66 c7 84 08 80 00 00 00 01 00                |
    | mov word [rax + 1 * rcx - 0x80], 0x0001                             | 66 c7 44 08 80 01 00                         |
    | mov word [rax + 1 * rcx - 0x81], 0x0001                             | 66 c7 84 08 7f ff ff ff 01 00                |
    | mov word [rax + 1 * rcx + 0xff], 0x0001                             | 66 c7 84 08 ff 00 00 00 01 00                |
    | mov word [rax + 1 * rcx - 0xff], 0x0001                             | 66 c7 84 08 01 ff ff ff 01 00                |
    | mov word [rax + 1 * rcx + 0x7fffffff], 0x0001                       | 66 c7 84 08 ff ff ff 7f 01 00                |
    | mov word [rax + 1 * rcx - 0x7fffffff], 0x0001                       | 66 c7 84 08 01 00 00 80 01 00                |
    | mov word [rax + 1 * rcx - 0x80000000], 0x0001                       | 66 c7 84 08 00 00 00 80 01 00                |
    | mov word [r10 + 0x7f], 0x0001                                       | 66 41 c7 42 7f 01 00                         |
    | mov word [r10 + 0x80], 0x0001                                       | 66 41 c7 82 80 00 00 00 01 00                |
    | mov word [r10 - 0x80], 0x0001                                       | 66 41 c7 42 80 01 00                         |
    | mov word [r10 - 0x81], 0x0001                                       | 66 41 c7 82 7f ff ff ff 01 00                |
    | .prev5: nop; nop; nop; nop; nop; mov word [rel @prev5], 0x0001      | 90 90 90 90 90 66 c7 05 f2 ff ff ff 01 00    |
    | .prev1: nop; mov word [rel @prev1], 0x0001                          | 90 66 c7 05 f6 ff ff ff 01 00                |
    | mov word [rel @next1], 0x0001; nop; .next1: nop                     | 66 c7 05 01 00 00 00 01 00 90 90             |
    | mov word [rel @next5], 0x0001; nop; nop; nop; nop; nop; .next5: nop | 66 c7 05 05 00 00 00 01 00 90 90 90 90 90 90 |
    | mov word [rax], 0x0000                                              | 66 c7 00 00 00                               |
    | mov word [rax], 0x007f                                              | 66 c7 00 7f 00                               |
    | mov word [rax], 0x0080                                              | 66 c7 00 80 00                               |
    | mov word [rax], 0x00ff                                              | 66 c7 00 ff 00                               |
    | mov word [rax], 0x0100                                              | 66 c7 00 00 01                               |
    | mov word [rax], 0x7fff                                              | 66 c7 00 ff 7f                               |
    | mov word [rax], 0x8000                                              | 66 c7 00 00 80                               |
    | mov word [rax], 0xffff                                              | 66 c7 00 ff ff                               |
    | mov word [rcx], 0x007f                                              | 66 c7 01 7f 00                               |
    | mov word [rdx], 0x0080                                              | 66 c7 02 80 00                               |
    | mov word [rbx], 0x00ff                                              | 66 c7 03 ff 00                               |
    | mov word [rsp], 0x0100                                              | 66 c7 04 24 00 01                            |
    | mov word [rbp], 0x7fff                                              | 66 c7 45 00 ff 7f                            |
    | mov word [rsi], 0x8000                                              | 66 c7 06 00 80                               |
    | mov word [rdi], 0xffff                                              | 66 c7 07 ff ff                               |
    | mov word [r8], 0x0000                                               | 66 41 c7 00 00 00                            |
    | mov word [r10], 0x007f                                              | 66 41 c7 02 7f 00                            |
    | mov word [r11], 0x0080                                              | 66 41 c7 03 80 00                            |
    | mov word [r12], 0x00ff                                              | 66 41 c7 04 24 ff 00                         |
    | mov word [r13], 0x0100                                              | 66 41 c7 45 00 00 01                         |
    | mov word [r14], 0x7fff                                              | 66 41 c7 06 ff 7f                            |
    | mov word [r15], 0x8000                                              | 66 41 c7 07 00 80                            |
    | mov word [rax + 1 * rcx], 0xffff                                    | 66 c7 04 08 ff ff                            |
    | mov word [rcx + 1 * rcx], 0x0000                                    | 66 c7 04 09 00 00                            |
    | mov word [rbx + 1 * rcx], 0x007f                                    | 66 c7 04 0b 7f 00                            |
    | mov word [rsp + 1 * rcx], 0x0080                                    | 66 c7 04 0c 80 00                            |
    | mov word [rbp + 1 * rcx], 0x00ff                                    | 66 c7 44 0d 00 ff 00                         |
    | mov word [rsi + 1 * rcx], 0x0100                                    | 66 c7 04 0e 00 01                            |
    | mov word [rdi + 1 * rcx], 0x7fff                                    | 66 c7 04 0f ff 7f                            |
    | mov word [r8 + 1 * rcx], 0x8000                                     | 66 41 c7 04 08 00 80                         |
    | mov word [r9 + 1 * rcx], 0xffff                                     | 66 41 c7 04 09 ff ff                         |
    | mov word [r10 + 1 * rcx], 0x0000                                    | 66 41 c7 04 0a 00 00                         |
    | mov word [r12 + 1 * rcx], 0x007f                                    | 66 41 c7 04 0c 7f 00                         |
    | mov word [r13 + 1 * rcx], 0x0080                                    | 66 41 c7 44 0d 00 80 00                      |
    | mov word [r14 + 1 * rcx], 0x00ff                                    | 66 41 c7 04 0e ff 00                         |
    | mov word [r15 + 1 * rcx], 0x0100                                    | 66 41 c7 04 0f 00 01                         |
    | mov word [rax + 1 * rax], 0x7fff                                    | 66 c7 04 00 ff 7f                            |
    | mov word [rax + 1 * rdx], 0x8000                                    | 66 c7 04 10 00 80                            |
    | mov word [rax + 1 * rbx], 0xffff                                    | 66 c7 04 18 ff ff                            |
    | mov word [rax + 1 * rbp], 0x0000                                    | 66 c7 04 28 00 00                            |
    | mov word [rax + 1 * rdi], 0x007f                                    | 66 c7 04 38 7f 00                            |
    | mov word [rax + 1 * r8], 0x0080                                     | 66 42 c7 04 00 80 00                         |
    | mov word [rax + 1 * r9], 0x00ff                                     | 66 42 c7 04 08 ff 00                         |
    | mov word [rax + 1 * r10], 0x0100                                    | 66 42 c7 04 10 00 01                         |
    | mov word [rax + 1 * r11], 0x7fff                                    | 66 42 c7 04 18 ff 7f                         |
    | mov word [rax + 1 * r12], 0x8000                                    | 66 42 c7 04 20 00 80                         |
    | mov word [rax + 1 * r13], 0xffff                                    | 66 42 c7 04 28 ff ff                         |
    | mov word [rax + 1 * r14], 0x0000                                    | 66 42 c7 04 30 00 00                         |
    | mov word [rax + 2 * rcx], 0x007f                                    | 66 c7 04 48 7f 00                            |
    | mov word [rax + 4 * rcx], 0x0080                                    | 66 c7 04 88 80 00                            |
    | mov word [rax + 8 * rcx], 0x00ff                                    | 66 c7 04 c8 ff 00                            |
    | mov word [r8 + 1 * r9], 0x0100                                      | 66 43 c7 04 08 00 01                         |
    | mov word [r8 + 2 * r9], 0x7fff                                      | 66 43 c7 04 48 ff 7f                         |
    | mov word [r8 + 4 * r9], 0x8000                                      | 66 43 c7 04 88 00 80                         |
    | mov word [r8 + 8 * r9], 0xffff                                      | 66 43 c7 04 c8 ff ff                         |
    | mov word [1 * rcx], 0x0000                                          | 66 c7 04 0d 00 00 00 00 00 00                |
    | mov word [4 * rcx], 0x007f                                          | 66 c7 04 8d 00 00 00 00 7f 00                |
    | mov word [8 * rcx], 0x0080                                          | 66 c7 04 cd 00 00 00 00 80 00                |
    | mov word [1 * r9], 0x00ff                                           | 66 42 c7 04 0d 00 00 00 00 ff 00             |
    | mov word [2 * r9], 0x0100                                           | 66 42 c7 04 4d 00 00 00 00 00 01             |
    | mov word [4 * r9], 0x7fff                                           | 66 42 c7 04 8d 00 00 00 00 ff 7f             |
    | mov word [8 * r9], 0x8000                                           | 66 42 c7 04 cd 00 00 00 00 00 80             |
    | mov word [r13 + 8 * r12], 0xffff                                    | 66 43 c7 44 e5 00 ff ff                      |
    | mov word [rsp + 4 * r15], 0x0000                                    | 66 42 c7 04 bc 00 00                         |
    | mov word [rax + 1 * rcx - 0x00], 0x007f                             | 66 c7 44 08 00 7f 00                         |
    | mov word [rax + 1 * rcx + 0x01], 0x0080                             | 66 c7 44 08 01 80 00                         |
    | mov word [rax + 1 * rcx - 0x01], 0x00ff                             | 66 c7 44 08 ff ff 00                         |
    | mov word [rax + 1 * rcx + 0x00000001], 0x0100                       | 66 c7 84 08 01 00 00 00 00 01                |
    | mov word [rax + 1 * rcx - 0x00000001], 0x7fff                       | 66 c7 84 08 ff ff ff ff ff 7f                |
    | mov word [rax + 1 * rcx + 0x7f], 0x8000                             | 66 c7 44 08 7f 00 80                         |
    | mov word [rax + 1 * rcx - 0x7f], 0xffff                             | 66 c7 44 08 81 ff ff                         |
    | mov word [rax + 1 * rcx + 0x80], 0x0000                             | 66 c7 84 08 80 00 00 00 00 00                |
    | mov word [rax + 1 * rcx - 0x81], 0x007f                             | 66 c7 84 08 7f ff ff ff 7f 00                |
    | mov word [rax + 1 * rcx + 0xff], 0x0080                             | 66 c7 84 08 ff 00 00 00 80 00                |
    | mov word [rax + 1 * rcx - 0xff], 0x00ff                             | 66 c7 84 08 01 ff ff ff ff 00                |
    | mov word [rax + 1 * rcx + 0x7fffffff], 0x0100                       | 66 c7 84 08 ff ff ff 7f 00 01                |
    | mov word [rax + 1 * rcx - 0x7fffffff], 0x7fff                       | 66 c7 84 08 01 00 00 80 ff 7f                |
    | mov word [rax + 1 * rcx - 0x80000000], 0x8000                       | 66 c7 84 08 00 00 00 80 00 80                |
    | mov word [r10 + 0x7f], 0xffff                                       | 66 41 c7 42 7f ff ff                         |
    | mov word [r10 + 0x80], 0x0000                                       | 66 41 c7 82 80 00 00 00 00 00                |
    | mov word [r10 - 0x81], 0x007f                                       | 66 41 c7 82 7f ff ff ff 7f 00                |
    | .prev5: nop; nop; nop; nop; nop; mov word [rel @prev5], 0x0080      | 90 90 90 90 90 66 c7 05 f2 ff ff ff 80 00    |
    | .prev1: nop; mov word [rel @prev1], 0x00ff                          | 90 66 c7 05 f6 ff ff ff ff 00                |
    | mov word [rel @next1], 0x0100; nop; .next1: nop                     | 66 c7 05 01 00 00 00 00 01 90 90             |
    | mov word [rel @next5], 0x7fff; nop; nop; nop; nop; nop; .next5: nop | 66 c7 05 05 00 00 00 ff 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------- | -------------------------------------------- |
"""


def can_encode_mov_addr16_imm16():
    encode(MOV_ADDR16_IMM16)


MOV_ADDR16_REG16 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | mov word [rax], cx                                              | 66 89 08                               |
    | mov word [rcx], cx                                              | 66 89 09                               |
    | mov word [rdx], cx                                              | 66 89 0a                               |
    | mov word [rbx], cx                                              | 66 89 0b                               |
    | mov word [rsp], cx                                              | 66 89 0c 24                            |
    | mov word [rbp], cx                                              | 66 89 4d 00                            |
    | mov word [rsi], cx                                              | 66 89 0e                               |
    | mov word [rdi], cx                                              | 66 89 0f                               |
    | mov word [r8], cx                                               | 66 41 89 08                            |
    | mov word [r9], cx                                               | 66 41 89 09                            |
    | mov word [r10], cx                                              | 66 41 89 0a                            |
    | mov word [r11], cx                                              | 66 41 89 0b                            |
    | mov word [r12], cx                                              | 66 41 89 0c 24                         |
    | mov word [r13], cx                                              | 66 41 89 4d 00                         |
    | mov word [r14], cx                                              | 66 41 89 0e                            |
    | mov word [r15], cx                                              | 66 41 89 0f                            |
    | mov word [rax + 1 * rcx], cx                                    | 66 89 0c 08                            |
    | mov word [rcx + 1 * rcx], cx                                    | 66 89 0c 09                            |
    | mov word [rdx + 1 * rcx], cx                                    | 66 89 0c 0a                            |
    | mov word [rbx + 1 * rcx], cx                                    | 66 89 0c 0b                            |
    | mov word [rsp + 1 * rcx], cx                                    | 66 89 0c 0c                            |
    | mov word [rbp + 1 * rcx], cx                                    | 66 89 4c 0d 00                         |
    | mov word [rsi + 1 * rcx], cx                                    | 66 89 0c 0e                            |
    | mov word [rdi + 1 * rcx], cx                                    | 66 89 0c 0f                            |
    | mov word [r8 + 1 * rcx], cx                                     | 66 41 89 0c 08                         |
    | mov word [r9 + 1 * rcx], cx                                     | 66 41 89 0c 09                         |
    | mov word [r10 + 1 * rcx], cx                                    | 66 41 89 0c 0a                         |
    | mov word [r11 + 1 * rcx], cx                                    | 66 41 89 0c 0b                         |
    | mov word [r12 + 1 * rcx], cx                                    | 66 41 89 0c 0c                         |
    | mov word [r13 + 1 * rcx], cx                                    | 66 41 89 4c 0d 00                      |
    | mov word [r14 + 1 * rcx], cx                                    | 66 41 89 0c 0e                         |
    | mov word [r15 + 1 * rcx], cx                                    | 66 41 89 0c 0f                         |
    | mov word [rax + 1 * rax], cx                                    | 66 89 0c 00                            |
    | mov word [rax + 1 * rdx], cx                                    | 66 89 0c 10                            |
    | mov word [rax + 1 * rbx], cx                                    | 66 89 0c 18                            |
    | mov word [rax + 1 * rbp], cx                                    | 66 89 0c 28                            |
    | mov word [rax + 1 * rsi], cx                                    | 66 89 0c 30                            |
    | mov word [rax + 1 * rdi], cx                                    | 66 89 0c 38                            |
    | mov word [rax + 1 * r8], cx                                     | 66 42 89 0c 00                         |
    | mov word [rax + 1 * r9], cx                                     | 66 42 89 0c 08                         |
    | mov word [rax + 1 * r10], cx                                    | 66 42 89 0c 10                         |
    | mov word [rax + 1 * r11], cx                                    | 66 42 89 0c 18                         |
    | mov word [rax + 1 * r12], cx                                    | 66 42 89 0c 20                         |
    | mov word [rax + 1 * r13], cx                                    | 66 42 89 0c 28                         |
    | mov word [rax + 1 * r14], cx                                    | 66 42 89 0c 30                         |
    | mov word [rax + 1 * r15], cx                                    | 66 42 89 0c 38                         |
    | mov word [rax + 2 * rcx], cx                                    | 66 89 0c 48                            |
    | mov word [rax + 4 * rcx], cx                                    | 66 89 0c 88                            |
    | mov word [rax + 8 * rcx], cx                                    | 66 89 0c c8                            |
    | mov word [r8 + 1 * r9], cx                                      | 66 43 89 0c 08                         |
    | mov word [r8 + 2 * r9], cx                                      | 66 43 89 0c 48                         |
    | mov word [r8 + 4 * r9], cx                                      | 66 43 89 0c 88                         |
    | mov word [r8 + 8 * r9], cx                                      | 66 43 89 0c c8                         |
    | mov word [1 * rcx], cx                                          | 66 89 0c 0d 00 00 00 00                |
    | mov word [2 * rcx], cx                                          | 66 89 0c 4d 00 00 00 00                |
    | mov word [4 * rcx], cx                                          | 66 89 0c 8d 00 00 00 00                |
    | mov word [8 * rcx], cx                                          | 66 89 0c cd 00 00 00 00                |
    | mov word [1 * r9], cx                                           | 66 42 89 0c 0d 00 00 00 00             |
    | mov word [2 * r9], cx                                           | 66 42 89 0c 4d 00 00 00 00             |
    | mov word [4 * r9], cx                                           | 66 42 89 0c 8d 00 00 00 00             |
    | mov word [8 * r9], cx                                           | 66 42 89 0c cd 00 00 00 00             |
    | mov word [r13 + 8 * r12], cx                                    | 66 43 89 4c e5 00                      |
    | mov word [rsp + 4 * r15], cx                                    | 66 42 89 0c bc                         |
    | mov word [rax + 1 * rcx + 0x00], cx                             | 66 89 4c 08 00                         |
    | mov word [rax + 1 * rcx - 0x00], cx                             | 66 89 4c 08 00                         |
    | mov word [rax + 1 * rcx + 0x01], cx                             | 66 89 4c 08 01                         |
    | mov word [rax + 1 * rcx - 0x01], cx                             | 66 89 4c 08 ff                         |
    | mov word [rax + 1 * rcx + 0x00000001], cx                       | 66 89 8c 08 01 00 00 00                |
    | mov word [rax + 1 * rcx - 0x00000001], cx                       | 66 89 8c 08 ff ff ff ff                |
    | mov word [rax + 1 * rcx + 0x7f], cx                             | 66 89 4c 08 7f                         |
    | mov word [rax + 1 * rcx - 0x7f], cx                             | 66 89 4c 08 81                         |
    | mov word [rax + 1 * rcx + 0x80], cx                             | 66 89 8c 08 80 00 00 00                |
    | mov word [rax + 1 * rcx - 0x80], cx                             | 66 89 4c 08 80                         |
    | mov word [rax + 1 * rcx - 0x81], cx                             | 66 89 8c 08 7f ff ff ff                |
    | mov word [rax + 1 * rcx + 0xff], cx                             | 66 89 8c 08 ff 00 00 00                |
    | mov word [rax + 1 * rcx - 0xff], cx                             | 66 89 8c 08 01 ff ff ff                |
    | mov word [rax + 1 * rcx + 0x7fffffff], cx                       | 66 89 8c 08 ff ff ff 7f                |
    | mov word [rax + 1 * rcx - 0x7fffffff], cx                       | 66 89 8c 08 01 00 00 80                |
    | mov word [rax + 1 * rcx - 0x80000000], cx                       | 66 89 8c 08 00 00 00 80                |
    | mov word [r10 + 0x7f], cx                                       | 66 41 89 4a 7f                         |
    | mov word [r10 + 0x80], cx                                       | 66 41 89 8a 80 00 00 00                |
    | mov word [r10 - 0x80], cx                                       | 66 41 89 4a 80                         |
    | mov word [r10 - 0x81], cx                                       | 66 41 89 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov word [rel @prev5], cx      | 90 90 90 90 90 66 89 0d f4 ff ff ff    |
    | .prev1: nop; mov word [rel @prev1], cx                          | 90 66 89 0d f8 ff ff ff                |
    | mov word [rel @next1], cx; nop; .next1: nop                     | 66 89 0d 01 00 00 00 90 90             |
    | mov word [rel @next5], cx; nop; nop; nop; nop; nop; .next5: nop | 66 89 0d 05 00 00 00 90 90 90 90 90 90 |
    | mov word [rax], ax                                              | 66 89 00                               |
    | mov word [rax], dx                                              | 66 89 10                               |
    | mov word [rax], bx                                              | 66 89 18                               |
    | mov word [rax], sp                                              | 66 89 20                               |
    | mov word [rax], bp                                              | 66 89 28                               |
    | mov word [rax], si                                              | 66 89 30                               |
    | mov word [rax], di                                              | 66 89 38                               |
    | mov word [rax], r8w                                             | 66 44 89 00                            |
    | mov word [rax], r9w                                             | 66 44 89 08                            |
    | mov word [rax], r10w                                            | 66 44 89 10                            |
    | mov word [rax], r11w                                            | 66 44 89 18                            |
    | mov word [rax], r12w                                            | 66 44 89 20                            |
    | mov word [rax], r13w                                            | 66 44 89 28                            |
    | mov word [rax], r14w                                            | 66 44 89 30                            |
    | mov word [rax], r15w                                            | 66 44 89 38                            |
    | mov word [rcx], dx                                              | 66 89 11                               |
    | mov word [rdx], bx                                              | 66 89 1a                               |
    | mov word [rbx], sp                                              | 66 89 23                               |
    | mov word [rsp], bp                                              | 66 89 2c 24                            |
    | mov word [rbp], si                                              | 66 89 75 00                            |
    | mov word [rsi], di                                              | 66 89 3e                               |
    | mov word [rdi], r8w                                             | 66 44 89 07                            |
    | mov word [r8], r9w                                              | 66 45 89 08                            |
    | mov word [r9], r10w                                             | 66 45 89 11                            |
    | mov word [r10], r11w                                            | 66 45 89 1a                            |
    | mov word [r11], r12w                                            | 66 45 89 23                            |
    | mov word [r12], r13w                                            | 66 45 89 2c 24                         |
    | mov word [r13], r14w                                            | 66 45 89 75 00                         |
    | mov word [r14], r15w                                            | 66 45 89 3e                            |
    | mov word [r15], ax                                              | 66 41 89 07                            |
    | mov word [rcx + 1 * rcx], dx                                    | 66 89 14 09                            |
    | mov word [rdx + 1 * rcx], bx                                    | 66 89 1c 0a                            |
    | mov word [rbx + 1 * rcx], sp                                    | 66 89 24 0b                            |
    | mov word [rsp + 1 * rcx], bp                                    | 66 89 2c 0c                            |
    | mov word [rbp + 1 * rcx], si                                    | 66 89 74 0d 00                         |
    | mov word [rsi + 1 * rcx], di                                    | 66 89 3c 0e                            |
    | mov word [rdi + 1 * rcx], r8w                                   | 66 44 89 04 0f                         |
    | mov word [r8 + 1 * rcx], r9w                                    | 66 45 89 0c 08                         |
    | mov word [r9 + 1 * rcx], r10w                                   | 66 45 89 14 09                         |
    | mov word [r10 + 1 * rcx], r11w                                  | 66 45 89 1c 0a                         |
    | mov word [r11 + 1 * rcx], r12w                                  | 66 45 89 24 0b                         |
    | mov word [r12 + 1 * rcx], r13w                                  | 66 45 89 2c 0c                         |
    | mov word [r13 + 1 * rcx], r14w                                  | 66 45 89 74 0d 00                      |
    | mov word [r14 + 1 * rcx], r15w                                  | 66 45 89 3c 0e                         |
    | mov word [r15 + 1 * rcx], ax                                    | 66 41 89 04 0f                         |
    | mov word [rax + 1 * rdx], dx                                    | 66 89 14 10                            |
    | mov word [rax + 1 * rbx], bx                                    | 66 89 1c 18                            |
    | mov word [rax + 1 * rbp], sp                                    | 66 89 24 28                            |
    | mov word [rax + 1 * rsi], bp                                    | 66 89 2c 30                            |
    | mov word [rax + 1 * rdi], si                                    | 66 89 34 38                            |
    | mov word [rax + 1 * r8], di                                     | 66 42 89 3c 00                         |
    | mov word [rax + 1 * r9], r8w                                    | 66 46 89 04 08                         |
    | mov word [rax + 1 * r10], r9w                                   | 66 46 89 0c 10                         |
    | mov word [rax + 1 * r11], r10w                                  | 66 46 89 14 18                         |
    | mov word [rax + 1 * r12], r11w                                  | 66 46 89 1c 20                         |
    | mov word [rax + 1 * r13], r12w                                  | 66 46 89 24 28                         |
    | mov word [rax + 1 * r14], r13w                                  | 66 46 89 2c 30                         |
    | mov word [rax + 1 * r15], r14w                                  | 66 46 89 34 38                         |
    | mov word [rax + 2 * rcx], r15w                                  | 66 44 89 3c 48                         |
    | mov word [rax + 4 * rcx], ax                                    | 66 89 04 88                            |
    | mov word [r8 + 1 * r9], dx                                      | 66 43 89 14 08                         |
    | mov word [r8 + 2 * r9], bx                                      | 66 43 89 1c 48                         |
    | mov word [r8 + 4 * r9], sp                                      | 66 43 89 24 88                         |
    | mov word [r8 + 8 * r9], bp                                      | 66 43 89 2c c8                         |
    | mov word [1 * rcx], si                                          | 66 89 34 0d 00 00 00 00                |
    | mov word [2 * rcx], di                                          | 66 89 3c 4d 00 00 00 00                |
    | mov word [4 * rcx], r8w                                         | 66 44 89 04 8d 00 00 00 00             |
    | mov word [8 * rcx], r9w                                         | 66 44 89 0c cd 00 00 00 00             |
    | mov word [1 * r9], r10w                                         | 66 46 89 14 0d 00 00 00 00             |
    | mov word [2 * r9], r11w                                         | 66 46 89 1c 4d 00 00 00 00             |
    | mov word [4 * r9], r12w                                         | 66 46 89 24 8d 00 00 00 00             |
    | mov word [8 * r9], r13w                                         | 66 46 89 2c cd 00 00 00 00             |
    | mov word [r13 + 8 * r12], r14w                                  | 66 47 89 74 e5 00                      |
    | mov word [rsp + 4 * r15], r15w                                  | 66 46 89 3c bc                         |
    | mov word [rax + 1 * rcx + 0x00], ax                             | 66 89 44 08 00                         |
    | mov word [rax + 1 * rcx + 0x01], dx                             | 66 89 54 08 01                         |
    | mov word [rax + 1 * rcx - 0x01], bx                             | 66 89 5c 08 ff                         |
    | mov word [rax + 1 * rcx + 0x00000001], sp                       | 66 89 a4 08 01 00 00 00                |
    | mov word [rax + 1 * rcx - 0x00000001], bp                       | 66 89 ac 08 ff ff ff ff                |
    | mov word [rax + 1 * rcx + 0x7f], si                             | 66 89 74 08 7f                         |
    | mov word [rax + 1 * rcx - 0x7f], di                             | 66 89 7c 08 81                         |
    | mov word [rax + 1 * rcx + 0x80], r8w                            | 66 44 89 84 08 80 00 00 00             |
    | mov word [rax + 1 * rcx - 0x80], r9w                            | 66 44 89 4c 08 80                      |
    | mov word [rax + 1 * rcx - 0x81], r10w                           | 66 44 89 94 08 7f ff ff ff             |
    | mov word [rax + 1 * rcx + 0xff], r11w                           | 66 44 89 9c 08 ff 00 00 00             |
    | mov word [rax + 1 * rcx - 0xff], r12w                           | 66 44 89 a4 08 01 ff ff ff             |
    | mov word [rax + 1 * rcx + 0x7fffffff], r13w                     | 66 44 89 ac 08 ff ff ff 7f             |
    | mov word [rax + 1 * rcx - 0x7fffffff], r14w                     | 66 44 89 b4 08 01 00 00 80             |
    | mov word [rax + 1 * rcx - 0x80000000], r15w                     | 66 44 89 bc 08 00 00 00 80             |
    | mov word [r10 + 0x7f], ax                                       | 66 41 89 42 7f                         |
    | mov word [r10 - 0x80], dx                                       | 66 41 89 52 80                         |
    | mov word [r10 - 0x81], bx                                       | 66 41 89 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; mov word [rel @prev5], sp      | 90 90 90 90 90 66 89 25 f4 ff ff ff    |
    | .prev1: nop; mov word [rel @prev1], bp                          | 90 66 89 2d f8 ff ff ff                |
    | mov word [rel @next1], si; nop; .next1: nop                     | 66 89 35 01 00 00 00 90 90             |
    | mov word [rel @next5], di; nop; nop; nop; nop; nop; .next5: nop | 66 89 3d 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_mov_addr16_reg16():
    encode(MOV_ADDR16_REG16)


MOV_ADDR8_IMM8 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | mov byte [rax], 0x01                                              | c6 00 01                               |
    | mov byte [rcx], 0x01                                              | c6 01 01                               |
    | mov byte [rdx], 0x01                                              | c6 02 01                               |
    | mov byte [rbx], 0x01                                              | c6 03 01                               |
    | mov byte [rsp], 0x01                                              | c6 04 24 01                            |
    | mov byte [rbp], 0x01                                              | c6 45 00 01                            |
    | mov byte [rsi], 0x01                                              | c6 06 01                               |
    | mov byte [rdi], 0x01                                              | c6 07 01                               |
    | mov byte [r8], 0x01                                               | 41 c6 00 01                            |
    | mov byte [r9], 0x01                                               | 41 c6 01 01                            |
    | mov byte [r10], 0x01                                              | 41 c6 02 01                            |
    | mov byte [r11], 0x01                                              | 41 c6 03 01                            |
    | mov byte [r12], 0x01                                              | 41 c6 04 24 01                         |
    | mov byte [r13], 0x01                                              | 41 c6 45 00 01                         |
    | mov byte [r14], 0x01                                              | 41 c6 06 01                            |
    | mov byte [r15], 0x01                                              | 41 c6 07 01                            |
    | mov byte [rax + 1 * rcx], 0x01                                    | c6 04 08 01                            |
    | mov byte [rcx + 1 * rcx], 0x01                                    | c6 04 09 01                            |
    | mov byte [rdx + 1 * rcx], 0x01                                    | c6 04 0a 01                            |
    | mov byte [rbx + 1 * rcx], 0x01                                    | c6 04 0b 01                            |
    | mov byte [rsp + 1 * rcx], 0x01                                    | c6 04 0c 01                            |
    | mov byte [rbp + 1 * rcx], 0x01                                    | c6 44 0d 00 01                         |
    | mov byte [rsi + 1 * rcx], 0x01                                    | c6 04 0e 01                            |
    | mov byte [rdi + 1 * rcx], 0x01                                    | c6 04 0f 01                            |
    | mov byte [r8 + 1 * rcx], 0x01                                     | 41 c6 04 08 01                         |
    | mov byte [r9 + 1 * rcx], 0x01                                     | 41 c6 04 09 01                         |
    | mov byte [r10 + 1 * rcx], 0x01                                    | 41 c6 04 0a 01                         |
    | mov byte [r11 + 1 * rcx], 0x01                                    | 41 c6 04 0b 01                         |
    | mov byte [r12 + 1 * rcx], 0x01                                    | 41 c6 04 0c 01                         |
    | mov byte [r13 + 1 * rcx], 0x01                                    | 41 c6 44 0d 00 01                      |
    | mov byte [r14 + 1 * rcx], 0x01                                    | 41 c6 04 0e 01                         |
    | mov byte [r15 + 1 * rcx], 0x01                                    | 41 c6 04 0f 01                         |
    | mov byte [rax + 1 * rax], 0x01                                    | c6 04 00 01                            |
    | mov byte [rax + 1 * rdx], 0x01                                    | c6 04 10 01                            |
    | mov byte [rax + 1 * rbx], 0x01                                    | c6 04 18 01                            |
    | mov byte [rax + 1 * rbp], 0x01                                    | c6 04 28 01                            |
    | mov byte [rax + 1 * rsi], 0x01                                    | c6 04 30 01                            |
    | mov byte [rax + 1 * rdi], 0x01                                    | c6 04 38 01                            |
    | mov byte [rax + 1 * r8], 0x01                                     | 42 c6 04 00 01                         |
    | mov byte [rax + 1 * r9], 0x01                                     | 42 c6 04 08 01                         |
    | mov byte [rax + 1 * r10], 0x01                                    | 42 c6 04 10 01                         |
    | mov byte [rax + 1 * r11], 0x01                                    | 42 c6 04 18 01                         |
    | mov byte [rax + 1 * r12], 0x01                                    | 42 c6 04 20 01                         |
    | mov byte [rax + 1 * r13], 0x01                                    | 42 c6 04 28 01                         |
    | mov byte [rax + 1 * r14], 0x01                                    | 42 c6 04 30 01                         |
    | mov byte [rax + 1 * r15], 0x01                                    | 42 c6 04 38 01                         |
    | mov byte [rax + 2 * rcx], 0x01                                    | c6 04 48 01                            |
    | mov byte [rax + 4 * rcx], 0x01                                    | c6 04 88 01                            |
    | mov byte [rax + 8 * rcx], 0x01                                    | c6 04 c8 01                            |
    | mov byte [r8 + 1 * r9], 0x01                                      | 43 c6 04 08 01                         |
    | mov byte [r8 + 2 * r9], 0x01                                      | 43 c6 04 48 01                         |
    | mov byte [r8 + 4 * r9], 0x01                                      | 43 c6 04 88 01                         |
    | mov byte [r8 + 8 * r9], 0x01                                      | 43 c6 04 c8 01                         |
    | mov byte [1 * rcx], 0x01                                          | c6 04 0d 00 00 00 00 01                |
    | mov byte [2 * rcx], 0x01                                          | c6 04 4d 00 00 00 00 01                |
    | mov byte [4 * rcx], 0x01                                          | c6 04 8d 00 00 00 00 01                |
    | mov byte [8 * rcx], 0x01                                          | c6 04 cd 00 00 00 00 01                |
    | mov byte [1 * r9], 0x01                                           | 42 c6 04 0d 00 00 00 00 01             |
    | mov byte [2 * r9], 0x01                                           | 42 c6 04 4d 00 00 00 00 01             |
    | mov byte [4 * r9], 0x01                                           | 42 c6 04 8d 00 00 00 00 01             |
    | mov byte [8 * r9], 0x01                                           | 42 c6 04 cd 00 00 00 00 01             |
    | mov byte [r13 + 8 * r12], 0x01                                    | 43 c6 44 e5 00 01                      |
    | mov byte [rsp + 4 * r15], 0x01                                    | 42 c6 04 bc 01                         |
    | mov byte [rax + 1 * rcx + 0x00], 0x01                             | c6 44 08 00 01                         |
    | mov byte [rax + 1 * rcx - 0x00], 0x01                             | c6 44 08 00 01                         |
    | mov byte [rax + 1 * rcx + 0x01], 0x01                             | c6 44 08 01 01                         |
    | mov byte [rax + 1 * rcx - 0x01], 0x01                             | c6 44 08 ff 01                         |
    | mov byte [rax + 1 * rcx + 0x00000001], 0x01                       | c6 84 08 01 00 00 00 01                |
    | mov byte [rax + 1 * rcx - 0x00000001], 0x01                       | c6 84 08 ff ff ff ff 01                |
    | mov byte [rax + 1 * rcx + 0x7f], 0x01                             | c6 44 08 7f 01                         |
    | mov byte [rax + 1 * rcx - 0x7f], 0x01                             | c6 44 08 81 01                         |
    | mov byte [rax + 1 * rcx + 0x80], 0x01                             | c6 84 08 80 00 00 00 01                |
    | mov byte [rax + 1 * rcx - 0x80], 0x01                             | c6 44 08 80 01                         |
    | mov byte [rax + 1 * rcx - 0x81], 0x01                             | c6 84 08 7f ff ff ff 01                |
    | mov byte [rax + 1 * rcx + 0xff], 0x01                             | c6 84 08 ff 00 00 00 01                |
    | mov byte [rax + 1 * rcx - 0xff], 0x01                             | c6 84 08 01 ff ff ff 01                |
    | mov byte [rax + 1 * rcx + 0x7fffffff], 0x01                       | c6 84 08 ff ff ff 7f 01                |
    | mov byte [rax + 1 * rcx - 0x7fffffff], 0x01                       | c6 84 08 01 00 00 80 01                |
    | mov byte [rax + 1 * rcx - 0x80000000], 0x01                       | c6 84 08 00 00 00 80 01                |
    | mov byte [r10 + 0x7f], 0x01                                       | 41 c6 42 7f 01                         |
    | mov byte [r10 + 0x80], 0x01                                       | 41 c6 82 80 00 00 00 01                |
    | mov byte [r10 - 0x80], 0x01                                       | 41 c6 42 80 01                         |
    | mov byte [r10 - 0x81], 0x01                                       | 41 c6 82 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; mov byte [rel @prev5], 0x01      | 90 90 90 90 90 c6 05 f4 ff ff ff 01    |
    | .prev1: nop; mov byte [rel @prev1], 0x01                          | 90 c6 05 f8 ff ff ff 01                |
    | mov byte [rel @next1], 0x01; nop; .next1: nop                     | c6 05 01 00 00 00 01 90 90             |
    | mov byte [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | c6 05 05 00 00 00 01 90 90 90 90 90 90 |
    | mov byte [rax], 0x00                                              | c6 00 00                               |
    | mov byte [rax], 0x7f                                              | c6 00 7f                               |
    | mov byte [rax], 0x80                                              | c6 00 80                               |
    | mov byte [rax], 0xff                                              | c6 00 ff                               |
    | mov byte [rcx], 0x7f                                              | c6 01 7f                               |
    | mov byte [rdx], 0x80                                              | c6 02 80                               |
    | mov byte [rbx], 0xff                                              | c6 03 ff                               |
    | mov byte [rsp], 0x00                                              | c6 04 24 00                            |
    | mov byte [rsi], 0x7f                                              | c6 06 7f                               |
    | mov byte [rdi], 0x80                                              | c6 07 80                               |
    | mov byte [r8], 0xff                                               | 41 c6 00 ff                            |
    | mov byte [r9], 0x00                                               | 41 c6 01 00                            |
    | mov byte [r11], 0x7f                                              | 41 c6 03 7f                            |
    | mov byte [r12], 0x80                                              | 41 c6 04 24 80                         |
    | mov byte [r13], 0xff                                              | 41 c6 45 00 ff                         |
    | mov byte [r14], 0x00                                              | 41 c6 06 00                            |
    | mov byte [rax + 1 * rcx], 0x7f                                    | c6 04 08 7f                            |
    | mov byte [rcx + 1 * rcx], 0x80                                    | c6 04 09 80                            |
    | mov byte [rdx + 1 * rcx], 0xff                                    | c6 04 0a ff                            |
    | mov byte [rbx + 1 * rcx], 0x00                                    | c6 04 0b 00                            |
    | mov byte [rbp + 1 * rcx], 0x7f                                    | c6 44 0d 00 7f                         |
    | mov byte [rsi + 1 * rcx], 0x80                                    | c6 04 0e 80                            |
    | mov byte [rdi + 1 * rcx], 0xff                                    | c6 04 0f ff                            |
    | mov byte [r8 + 1 * rcx], 0x00                                     | 41 c6 04 08 00                         |
    | mov byte [r10 + 1 * rcx], 0x7f                                    | 41 c6 04 0a 7f                         |
    | mov byte [r11 + 1 * rcx], 0x80                                    | 41 c6 04 0b 80                         |
    | mov byte [r12 + 1 * rcx], 0xff                                    | 41 c6 04 0c ff                         |
    | mov byte [r13 + 1 * rcx], 0x00                                    | 41 c6 44 0d 00 00                      |
    | mov byte [r15 + 1 * rcx], 0x7f                                    | 41 c6 04 0f 7f                         |
    | mov byte [rax + 1 * rax], 0x80                                    | c6 04 00 80                            |
    | mov byte [rax + 1 * rdx], 0xff                                    | c6 04 10 ff                            |
    | mov byte [rax + 1 * rbx], 0x00                                    | c6 04 18 00                            |
    | mov byte [rax + 1 * rsi], 0x7f                                    | c6 04 30 7f                            |
    | mov byte [rax + 1 * rdi], 0x80                                    | c6 04 38 80                            |
    | mov byte [rax + 1 * r8], 0xff                                     | 42 c6 04 00 ff                         |
    | mov byte [rax + 1 * r9], 0x00                                     | 42 c6 04 08 00                         |
    | mov byte [rax + 1 * r11], 0x7f                                    | 42 c6 04 18 7f                         |
    | mov byte [rax + 1 * r12], 0x80                                    | 42 c6 04 20 80                         |
    | mov byte [rax + 1 * r13], 0xff                                    | 42 c6 04 28 ff                         |
    | mov byte [rax + 1 * r14], 0x00                                    | 42 c6 04 30 00                         |
    | mov byte [rax + 2 * rcx], 0x7f                                    | c6 04 48 7f                            |
    | mov byte [rax + 4 * rcx], 0x80                                    | c6 04 88 80                            |
    | mov byte [rax + 8 * rcx], 0xff                                    | c6 04 c8 ff                            |
    | mov byte [r8 + 1 * r9], 0x00                                      | 43 c6 04 08 00                         |
    | mov byte [r8 + 4 * r9], 0x7f                                      | 43 c6 04 88 7f                         |
    | mov byte [r8 + 8 * r9], 0x80                                      | 43 c6 04 c8 80                         |
    | mov byte [1 * rcx], 0xff                                          | c6 04 0d 00 00 00 00 ff                |
    | mov byte [2 * rcx], 0x00                                          | c6 04 4d 00 00 00 00 00                |
    | mov byte [8 * rcx], 0x7f                                          | c6 04 cd 00 00 00 00 7f                |
    | mov byte [1 * r9], 0x80                                           | 42 c6 04 0d 00 00 00 00 80             |
    | mov byte [2 * r9], 0xff                                           | 42 c6 04 4d 00 00 00 00 ff             |
    | mov byte [4 * r9], 0x00                                           | 42 c6 04 8d 00 00 00 00 00             |
    | mov byte [r13 + 8 * r12], 0x7f                                    | 43 c6 44 e5 00 7f                      |
    | mov byte [rsp + 4 * r15], 0x80                                    | 42 c6 04 bc 80                         |
    | mov byte [rax + 1 * rcx + 0x00], 0xff                             | c6 44 08 00 ff                         |
    | mov byte [rax + 1 * rcx - 0x00], 0x00                             | c6 44 08 00 00                         |
    | mov byte [rax + 1 * rcx - 0x01], 0x7f                             | c6 44 08 ff 7f                         |
    | mov byte [rax + 1 * rcx + 0x00000001], 0x80                       | c6 84 08 01 00 00 00 80                |
    | mov byte [rax + 1 * rcx - 0x00000001], 0xff                       | c6 84 08 ff ff ff ff ff                |
    | mov byte [rax + 1 * rcx + 0x7f], 0x00                             | c6 44 08 7f 00                         |
    | mov byte [rax + 1 * rcx + 0x80], 0x7f                             | c6 84 08 80 00 00 00 7f                |
    | mov byte [rax + 1 * rcx - 0x80], 0x80                             | c6 44 08 80 80                         |
    | mov byte [rax + 1 * rcx - 0x81], 0xff                             | c6 84 08 7f ff ff ff ff                |
    | mov byte [rax + 1 * rcx + 0xff], 0x00                             | c6 84 08 ff 00 00 00 00                |
    | mov byte [rax + 1 * rcx + 0x7fffffff], 0x7f                       | c6 84 08 ff ff ff 7f 7f                |
    | mov byte [rax + 1 * rcx - 0x7fffffff], 0x80                       | c6 84 08 01 00 00 80 80                |
    | mov byte [rax + 1 * rcx - 0x80000000], 0xff                       | c6 84 08 00 00 00 80 ff                |
    | mov byte [r10 + 0x7f], 0x00                                       | 41 c6 42 7f 00                         |
    | mov byte [r10 - 0x80], 0x7f                                       | 41 c6 42 80 7f                         |
    | mov byte [r10 - 0x81], 0x80                                       | 41 c6 82 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; mov byte [rel @prev5], 0xff      | 90 90 90 90 90 c6 05 f4 ff ff ff ff    |
    | .prev1: nop; mov byte [rel @prev1], 0x00                          | 90 c6 05 f8 ff ff ff 00                |
    | mov byte [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | c6 05 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_mov_addr8_imm8():
    encode(MOV_ADDR8_IMM8)


MOV_ADDR8_REG8 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | mov byte [rax], cl                                               | 88 08                                  |
    | mov byte [rcx], cl                                               | 88 09                                  |
    | mov byte [rdx], cl                                               | 88 0a                                  |
    | mov byte [rbx], cl                                               | 88 0b                                  |
    | mov byte [rsp], cl                                               | 88 0c 24                               |
    | mov byte [rbp], cl                                               | 88 4d 00                               |
    | mov byte [rsi], cl                                               | 88 0e                                  |
    | mov byte [rdi], cl                                               | 88 0f                                  |
    | mov byte [r8], cl                                                | 41 88 08                               |
    | mov byte [r9], cl                                                | 41 88 09                               |
    | mov byte [r10], cl                                               | 41 88 0a                               |
    | mov byte [r11], cl                                               | 41 88 0b                               |
    | mov byte [r12], cl                                               | 41 88 0c 24                            |
    | mov byte [r13], cl                                               | 41 88 4d 00                            |
    | mov byte [r14], cl                                               | 41 88 0e                               |
    | mov byte [r15], cl                                               | 41 88 0f                               |
    | mov byte [rax + 1 * rcx], cl                                     | 88 0c 08                               |
    | mov byte [rcx + 1 * rcx], cl                                     | 88 0c 09                               |
    | mov byte [rdx + 1 * rcx], cl                                     | 88 0c 0a                               |
    | mov byte [rbx + 1 * rcx], cl                                     | 88 0c 0b                               |
    | mov byte [rsp + 1 * rcx], cl                                     | 88 0c 0c                               |
    | mov byte [rbp + 1 * rcx], cl                                     | 88 4c 0d 00                            |
    | mov byte [rsi + 1 * rcx], cl                                     | 88 0c 0e                               |
    | mov byte [rdi + 1 * rcx], cl                                     | 88 0c 0f                               |
    | mov byte [r8 + 1 * rcx], cl                                      | 41 88 0c 08                            |
    | mov byte [r9 + 1 * rcx], cl                                      | 41 88 0c 09                            |
    | mov byte [r10 + 1 * rcx], cl                                     | 41 88 0c 0a                            |
    | mov byte [r11 + 1 * rcx], cl                                     | 41 88 0c 0b                            |
    | mov byte [r12 + 1 * rcx], cl                                     | 41 88 0c 0c                            |
    | mov byte [r13 + 1 * rcx], cl                                     | 41 88 4c 0d 00                         |
    | mov byte [r14 + 1 * rcx], cl                                     | 41 88 0c 0e                            |
    | mov byte [r15 + 1 * rcx], cl                                     | 41 88 0c 0f                            |
    | mov byte [rax + 1 * rax], cl                                     | 88 0c 00                               |
    | mov byte [rax + 1 * rdx], cl                                     | 88 0c 10                               |
    | mov byte [rax + 1 * rbx], cl                                     | 88 0c 18                               |
    | mov byte [rax + 1 * rbp], cl                                     | 88 0c 28                               |
    | mov byte [rax + 1 * rsi], cl                                     | 88 0c 30                               |
    | mov byte [rax + 1 * rdi], cl                                     | 88 0c 38                               |
    | mov byte [rax + 1 * r8], cl                                      | 42 88 0c 00                            |
    | mov byte [rax + 1 * r9], cl                                      | 42 88 0c 08                            |
    | mov byte [rax + 1 * r10], cl                                     | 42 88 0c 10                            |
    | mov byte [rax + 1 * r11], cl                                     | 42 88 0c 18                            |
    | mov byte [rax + 1 * r12], cl                                     | 42 88 0c 20                            |
    | mov byte [rax + 1 * r13], cl                                     | 42 88 0c 28                            |
    | mov byte [rax + 1 * r14], cl                                     | 42 88 0c 30                            |
    | mov byte [rax + 1 * r15], cl                                     | 42 88 0c 38                            |
    | mov byte [rax + 2 * rcx], cl                                     | 88 0c 48                               |
    | mov byte [rax + 4 * rcx], cl                                     | 88 0c 88                               |
    | mov byte [rax + 8 * rcx], cl                                     | 88 0c c8                               |
    | mov byte [r8 + 1 * r9], cl                                       | 43 88 0c 08                            |
    | mov byte [r8 + 2 * r9], cl                                       | 43 88 0c 48                            |
    | mov byte [r8 + 4 * r9], cl                                       | 43 88 0c 88                            |
    | mov byte [r8 + 8 * r9], cl                                       | 43 88 0c c8                            |
    | mov byte [1 * rcx], cl                                           | 88 0c 0d 00 00 00 00                   |
    | mov byte [2 * rcx], cl                                           | 88 0c 4d 00 00 00 00                   |
    | mov byte [4 * rcx], cl                                           | 88 0c 8d 00 00 00 00                   |
    | mov byte [8 * rcx], cl                                           | 88 0c cd 00 00 00 00                   |
    | mov byte [1 * r9], cl                                            | 42 88 0c 0d 00 00 00 00                |
    | mov byte [2 * r9], cl                                            | 42 88 0c 4d 00 00 00 00                |
    | mov byte [4 * r9], cl                                            | 42 88 0c 8d 00 00 00 00                |
    | mov byte [8 * r9], cl                                            | 42 88 0c cd 00 00 00 00                |
    | mov byte [r13 + 8 * r12], cl                                     | 43 88 4c e5 00                         |
    | mov byte [rsp + 4 * r15], cl                                     | 42 88 0c bc                            |
    | mov byte [rax + 1 * rcx + 0x00], cl                              | 88 4c 08 00                            |
    | mov byte [rax + 1 * rcx - 0x00], cl                              | 88 4c 08 00                            |
    | mov byte [rax + 1 * rcx + 0x01], cl                              | 88 4c 08 01                            |
    | mov byte [rax + 1 * rcx - 0x01], cl                              | 88 4c 08 ff                            |
    | mov byte [rax + 1 * rcx + 0x00000001], cl                        | 88 8c 08 01 00 00 00                   |
    | mov byte [rax + 1 * rcx - 0x00000001], cl                        | 88 8c 08 ff ff ff ff                   |
    | mov byte [rax + 1 * rcx + 0x7f], cl                              | 88 4c 08 7f                            |
    | mov byte [rax + 1 * rcx - 0x7f], cl                              | 88 4c 08 81                            |
    | mov byte [rax + 1 * rcx + 0x80], cl                              | 88 8c 08 80 00 00 00                   |
    | mov byte [rax + 1 * rcx - 0x80], cl                              | 88 4c 08 80                            |
    | mov byte [rax + 1 * rcx - 0x81], cl                              | 88 8c 08 7f ff ff ff                   |
    | mov byte [rax + 1 * rcx + 0xff], cl                              | 88 8c 08 ff 00 00 00                   |
    | mov byte [rax + 1 * rcx - 0xff], cl                              | 88 8c 08 01 ff ff ff                   |
    | mov byte [rax + 1 * rcx + 0x7fffffff], cl                        | 88 8c 08 ff ff ff 7f                   |
    | mov byte [rax + 1 * rcx - 0x7fffffff], cl                        | 88 8c 08 01 00 00 80                   |
    | mov byte [rax + 1 * rcx - 0x80000000], cl                        | 88 8c 08 00 00 00 80                   |
    | mov byte [r10 + 0x7f], cl                                        | 41 88 4a 7f                            |
    | mov byte [r10 + 0x80], cl                                        | 41 88 8a 80 00 00 00                   |
    | mov byte [r10 - 0x80], cl                                        | 41 88 4a 80                            |
    | mov byte [r10 - 0x81], cl                                        | 41 88 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov byte [rel @prev5], cl       | 90 90 90 90 90 88 0d f5 ff ff ff       |
    | .prev1: nop; mov byte [rel @prev1], cl                           | 90 88 0d f9 ff ff ff                   |
    | mov byte [rel @next1], cl; nop; .next1: nop                      | 88 0d 01 00 00 00 90 90                |
    | mov byte [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop  | 88 0d 05 00 00 00 90 90 90 90 90 90    |
    | mov byte [rax], al                                               | 88 00                                  |
    | mov byte [rax], dl                                               | 88 10                                  |
    | mov byte [rax], bl                                               | 88 18                                  |
    | mov byte [rax], spl                                              | 40 88 20                               |
    | mov byte [rax], bpl                                              | 40 88 28                               |
    | mov byte [rax], sil                                              | 40 88 30                               |
    | mov byte [rax], dil                                              | 40 88 38                               |
    | mov byte [rax], r8b                                              | 44 88 00                               |
    | mov byte [rax], r9b                                              | 44 88 08                               |
    | mov byte [rax], r10b                                             | 44 88 10                               |
    | mov byte [rax], r11b                                             | 44 88 18                               |
    | mov byte [rax], r12b                                             | 44 88 20                               |
    | mov byte [rax], r13b                                             | 44 88 28                               |
    | mov byte [rax], r14b                                             | 44 88 30                               |
    | mov byte [rax], r15b                                             | 44 88 38                               |
    | mov byte [rax], ah                                               | 88 20                                  |
    | mov byte [rax], ch                                               | 88 28                                  |
    | mov byte [rax], dh                                               | 88 30                                  |
    | mov byte [rax], bh                                               | 88 38                                  |
    | mov byte [rcx], dl                                               | 88 11                                  |
    | mov byte [rdx], bl                                               | 88 1a                                  |
    | mov byte [rbx], spl                                              | 40 88 23                               |
    | mov byte [rsp], bpl                                              | 40 88 2c 24                            |
    | mov byte [rbp], sil                                              | 40 88 75 00                            |
    | mov byte [rsi], dil                                              | 40 88 3e                               |
    | mov byte [rdi], r8b                                              | 44 88 07                               |
    | mov byte [r8], r9b                                               | 45 88 08                               |
    | mov byte [r9], r10b                                              | 45 88 11                               |
    | mov byte [r10], r11b                                             | 45 88 1a                               |
    | mov byte [r11], r12b                                             | 45 88 23                               |
    | mov byte [r12], r13b                                             | 45 88 2c 24                            |
    | mov byte [r13], r14b                                             | 45 88 75 00                            |
    | mov byte [r14], r15b                                             | 45 88 3e                               |
    | mov byte [r15], ah                                               | !! !! !!                               |
    | mov byte [rax + 1 * rcx], ch                                     | 88 2c 08                               |
    | mov byte [rcx + 1 * rcx], dh                                     | 88 34 09                               |
    | mov byte [rdx + 1 * rcx], bh                                     | 88 3c 0a                               |
    | mov byte [rbx + 1 * rcx], al                                     | 88 04 0b                               |
    | mov byte [rbp + 1 * rcx], dl                                     | 88 54 0d 00                            |
    | mov byte [rsi + 1 * rcx], bl                                     | 88 1c 0e                               |
    | mov byte [rdi + 1 * rcx], spl                                    | 40 88 24 0f                            |
    | mov byte [r8 + 1 * rcx], bpl                                     | 41 88 2c 08                            |
    | mov byte [r9 + 1 * rcx], sil                                     | 41 88 34 09                            |
    | mov byte [r10 + 1 * rcx], dil                                    | 41 88 3c 0a                            |
    | mov byte [r11 + 1 * rcx], r8b                                    | 45 88 04 0b                            |
    | mov byte [r12 + 1 * rcx], r9b                                    | 45 88 0c 0c                            |
    | mov byte [r13 + 1 * rcx], r10b                                   | 45 88 54 0d 00                         |
    | mov byte [r14 + 1 * rcx], r11b                                   | 45 88 1c 0e                            |
    | mov byte [r15 + 1 * rcx], r12b                                   | 45 88 24 0f                            |
    | mov byte [rax + 1 * rax], r13b                                   | 44 88 2c 00                            |
    | mov byte [rax + 1 * rdx], r14b                                   | 44 88 34 10                            |
    | mov byte [rax + 1 * rbx], r15b                                   | 44 88 3c 18                            |
    | mov byte [rax + 1 * rbp], ah                                     | 88 24 28                               |
    | mov byte [rax + 1 * rsi], ch                                     | 88 2c 30                               |
    | mov byte [rax + 1 * rdi], dh                                     | 88 34 38                               |
    | mov byte [rax + 1 * r8], bh                                      | !! !! !!                               |
    | mov byte [rax + 1 * r9], al                                      | 42 88 04 08                            |
    | mov byte [rax + 1 * r11], dl                                     | 42 88 14 18                            |
    | mov byte [rax + 1 * r12], bl                                     | 42 88 1c 20                            |
    | mov byte [rax + 1 * r13], spl                                    | 42 88 24 28                            |
    | mov byte [rax + 1 * r14], bpl                                    | 42 88 2c 30                            |
    | mov byte [rax + 1 * r15], sil                                    | 42 88 34 38                            |
    | mov byte [rax + 2 * rcx], dil                                    | 40 88 3c 48                            |
    | mov byte [rax + 4 * rcx], r8b                                    | 44 88 04 88                            |
    | mov byte [rax + 8 * rcx], r9b                                    | 44 88 0c c8                            |
    | mov byte [r8 + 1 * r9], r10b                                     | 47 88 14 08                            |
    | mov byte [r8 + 2 * r9], r11b                                     | 47 88 1c 48                            |
    | mov byte [r8 + 4 * r9], r12b                                     | 47 88 24 88                            |
    | mov byte [r8 + 8 * r9], r13b                                     | 47 88 2c c8                            |
    | mov byte [1 * rcx], r14b                                         | 44 88 34 0d 00 00 00 00                |
    | mov byte [2 * rcx], r15b                                         | 44 88 3c 4d 00 00 00 00                |
    | mov byte [4 * rcx], ah                                           | 88 24 8d 00 00 00 00                   |
    | mov byte [8 * rcx], ch                                           | 88 2c cd 00 00 00 00                   |
    | mov byte [1 * r9], dh                                            | !! !! !!                               |
    | mov byte [2 * r9], bh                                            | !! !! !!                               |
    | mov byte [4 * r9], al                                            | 42 88 04 8d 00 00 00 00                |
    | mov byte [r13 + 8 * r12], dl                                     | 43 88 54 e5 00                         |
    | mov byte [rsp + 4 * r15], bl                                     | 42 88 1c bc                            |
    | mov byte [rax + 1 * rcx + 0x00], spl                             | 40 88 64 08 00                         |
    | mov byte [rax + 1 * rcx - 0x00], bpl                             | 40 88 6c 08 00                         |
    | mov byte [rax + 1 * rcx + 0x01], sil                             | 40 88 74 08 01                         |
    | mov byte [rax + 1 * rcx - 0x01], dil                             | 40 88 7c 08 ff                         |
    | mov byte [rax + 1 * rcx + 0x00000001], r8b                       | 44 88 84 08 01 00 00 00                |
    | mov byte [rax + 1 * rcx - 0x00000001], r9b                       | 44 88 8c 08 ff ff ff ff                |
    | mov byte [rax + 1 * rcx + 0x7f], r10b                            | 44 88 54 08 7f                         |
    | mov byte [rax + 1 * rcx - 0x7f], r11b                            | 44 88 5c 08 81                         |
    | mov byte [rax + 1 * rcx + 0x80], r12b                            | 44 88 a4 08 80 00 00 00                |
    | mov byte [rax + 1 * rcx - 0x80], r13b                            | 44 88 6c 08 80                         |
    | mov byte [rax + 1 * rcx - 0x81], r14b                            | 44 88 b4 08 7f ff ff ff                |
    | mov byte [rax + 1 * rcx + 0xff], r15b                            | 44 88 bc 08 ff 00 00 00                |
    | mov byte [rax + 1 * rcx - 0xff], ah                              | 88 a4 08 01 ff ff ff                   |
    | mov byte [rax + 1 * rcx + 0x7fffffff], ch                        | 88 ac 08 ff ff ff 7f                   |
    | mov byte [rax + 1 * rcx - 0x7fffffff], dh                        | 88 b4 08 01 00 00 80                   |
    | mov byte [rax + 1 * rcx - 0x80000000], bh                        | 88 bc 08 00 00 00 80                   |
    | mov byte [r10 + 0x7f], al                                        | 41 88 42 7f                            |
    | mov byte [r10 - 0x80], dl                                        | 41 88 52 80                            |
    | mov byte [r10 - 0x81], bl                                        | 41 88 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; mov byte [rel @prev5], spl      | 90 90 90 90 90 40 88 25 f4 ff ff ff    |
    | .prev1: nop; mov byte [rel @prev1], bpl                          | 90 40 88 2d f8 ff ff ff                |
    | mov byte [rel @next1], sil; nop; .next1: nop                     | 40 88 35 01 00 00 00 90 90             |
    | mov byte [rel @next5], dil; nop; nop; nop; nop; nop; .next5: nop | 40 88 3d 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_mov_addr8_reg8():
    encode(MOV_ADDR8_REG8)
