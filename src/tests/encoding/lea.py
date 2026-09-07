from tests.encoding.core import encode, exhaust


def can_exhaust_lea():
    exhaust(
        LEA_REG16_ADDR64,
        LEA_REG32_ADDR64,
        LEA_REG64_ADDR64,
    )


LEA_REG64_ADDR64 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | lea rax, qword [rcx]                                              | 48 8d 01                               |
    | lea rcx, qword [rcx]                                              | 48 8d 09                               |
    | lea rdx, qword [rcx]                                              | 48 8d 11                               |
    | lea rbx, qword [rcx]                                              | 48 8d 19                               |
    | lea rsp, qword [rcx]                                              | 48 8d 21                               |
    | lea rbp, qword [rcx]                                              | 48 8d 29                               |
    | lea rsi, qword [rcx]                                              | 48 8d 31                               |
    | lea rdi, qword [rcx]                                              | 48 8d 39                               |
    | lea r8, qword [rcx]                                               | 4c 8d 01                               |
    | lea r9, qword [rcx]                                               | 4c 8d 09                               |
    | lea r10, qword [rcx]                                              | 4c 8d 11                               |
    | lea r11, qword [rcx]                                              | 4c 8d 19                               |
    | lea r12, qword [rcx]                                              | 4c 8d 21                               |
    | lea r13, qword [rcx]                                              | 4c 8d 29                               |
    | lea r14, qword [rcx]                                              | 4c 8d 31                               |
    | lea r15, qword [rcx]                                              | 4c 8d 39                               |
    | lea rax, qword [rax]                                              | 48 8d 00                               |
    | lea rax, qword [rdx]                                              | 48 8d 02                               |
    | lea rax, qword [rbx]                                              | 48 8d 03                               |
    | lea rax, qword [rsp]                                              | 48 8d 04 24                            |
    | lea rax, qword [rbp]                                              | 48 8d 45 00                            |
    | lea rax, qword [rsi]                                              | 48 8d 06                               |
    | lea rax, qword [rdi]                                              | 48 8d 07                               |
    | lea rax, qword [r8]                                               | 49 8d 00                               |
    | lea rax, qword [r9]                                               | 49 8d 01                               |
    | lea rax, qword [r10]                                              | 49 8d 02                               |
    | lea rax, qword [r11]                                              | 49 8d 03                               |
    | lea rax, qword [r12]                                              | 49 8d 04 24                            |
    | lea rax, qword [r13]                                              | 49 8d 45 00                            |
    | lea rax, qword [r14]                                              | 49 8d 06                               |
    | lea rax, qword [r15]                                              | 49 8d 07                               |
    | lea rax, qword [rax + 1 * rcx]                                    | 48 8d 04 08                            |
    | lea rax, qword [rcx + 1 * rcx]                                    | 48 8d 04 09                            |
    | lea rax, qword [rdx + 1 * rcx]                                    | 48 8d 04 0a                            |
    | lea rax, qword [rbx + 1 * rcx]                                    | 48 8d 04 0b                            |
    | lea rax, qword [rsp + 1 * rcx]                                    | 48 8d 04 0c                            |
    | lea rax, qword [rbp + 1 * rcx]                                    | 48 8d 44 0d 00                         |
    | lea rax, qword [rsi + 1 * rcx]                                    | 48 8d 04 0e                            |
    | lea rax, qword [rdi + 1 * rcx]                                    | 48 8d 04 0f                            |
    | lea rax, qword [r8 + 1 * rcx]                                     | 49 8d 04 08                            |
    | lea rax, qword [r9 + 1 * rcx]                                     | 49 8d 04 09                            |
    | lea rax, qword [r10 + 1 * rcx]                                    | 49 8d 04 0a                            |
    | lea rax, qword [r11 + 1 * rcx]                                    | 49 8d 04 0b                            |
    | lea rax, qword [r12 + 1 * rcx]                                    | 49 8d 04 0c                            |
    | lea rax, qword [r13 + 1 * rcx]                                    | 49 8d 44 0d 00                         |
    | lea rax, qword [r14 + 1 * rcx]                                    | 49 8d 04 0e                            |
    | lea rax, qword [r15 + 1 * rcx]                                    | 49 8d 04 0f                            |
    | lea rax, qword [rax + 1 * rax]                                    | 48 8d 04 00                            |
    | lea rax, qword [rax + 1 * rdx]                                    | 48 8d 04 10                            |
    | lea rax, qword [rax + 1 * rbx]                                    | 48 8d 04 18                            |
    | lea rax, qword [rax + 1 * rbp]                                    | 48 8d 04 28                            |
    | lea rax, qword [rax + 1 * rsi]                                    | 48 8d 04 30                            |
    | lea rax, qword [rax + 1 * rdi]                                    | 48 8d 04 38                            |
    | lea rax, qword [rax + 1 * r8]                                     | 4a 8d 04 00                            |
    | lea rax, qword [rax + 1 * r9]                                     | 4a 8d 04 08                            |
    | lea rax, qword [rax + 1 * r10]                                    | 4a 8d 04 10                            |
    | lea rax, qword [rax + 1 * r11]                                    | 4a 8d 04 18                            |
    | lea rax, qword [rax + 1 * r12]                                    | 4a 8d 04 20                            |
    | lea rax, qword [rax + 1 * r13]                                    | 4a 8d 04 28                            |
    | lea rax, qword [rax + 1 * r14]                                    | 4a 8d 04 30                            |
    | lea rax, qword [rax + 1 * r15]                                    | 4a 8d 04 38                            |
    | lea rax, qword [rax + 2 * rcx]                                    | 48 8d 04 48                            |
    | lea rax, qword [rax + 4 * rcx]                                    | 48 8d 04 88                            |
    | lea rax, qword [rax + 8 * rcx]                                    | 48 8d 04 c8                            |
    | lea rax, qword [r8 + 1 * r9]                                      | 4b 8d 04 08                            |
    | lea rax, qword [r8 + 2 * r9]                                      | 4b 8d 04 48                            |
    | lea rax, qword [r8 + 4 * r9]                                      | 4b 8d 04 88                            |
    | lea rax, qword [r8 + 8 * r9]                                      | 4b 8d 04 c8                            |
    | lea rax, qword [1 * rcx]                                          | 48 8d 04 0d 00 00 00 00                |
    | lea rax, qword [2 * rcx]                                          | 48 8d 04 4d 00 00 00 00                |
    | lea rax, qword [4 * rcx]                                          | 48 8d 04 8d 00 00 00 00                |
    | lea rax, qword [8 * rcx]                                          | 48 8d 04 cd 00 00 00 00                |
    | lea rax, qword [1 * r9]                                           | 4a 8d 04 0d 00 00 00 00                |
    | lea rax, qword [2 * r9]                                           | 4a 8d 04 4d 00 00 00 00                |
    | lea rax, qword [4 * r9]                                           | 4a 8d 04 8d 00 00 00 00                |
    | lea rax, qword [8 * r9]                                           | 4a 8d 04 cd 00 00 00 00                |
    | lea rax, qword [r13 + 8 * r12]                                    | 4b 8d 44 e5 00                         |
    | lea rax, qword [rsp + 4 * r15]                                    | 4a 8d 04 bc                            |
    | lea rax, qword [rax + 1 * rcx + 0x00]                             | 48 8d 44 08 00                         |
    | lea rax, qword [rax + 1 * rcx - 0x00]                             | 48 8d 44 08 00                         |
    | lea rax, qword [rax + 1 * rcx + 0x01]                             | 48 8d 44 08 01                         |
    | lea rax, qword [rax + 1 * rcx - 0x01]                             | 48 8d 44 08 ff                         |
    | lea rax, qword [rax + 1 * rcx + 0x00000001]                       | 48 8d 84 08 01 00 00 00                |
    | lea rax, qword [rax + 1 * rcx - 0x00000001]                       | 48 8d 84 08 ff ff ff ff                |
    | lea rax, qword [rax + 1 * rcx + 0x7f]                             | 48 8d 44 08 7f                         |
    | lea rax, qword [rax + 1 * rcx - 0x7f]                             | 48 8d 44 08 81                         |
    | lea rax, qword [rax + 1 * rcx + 0x80]                             | 48 8d 84 08 80 00 00 00                |
    | lea rax, qword [rax + 1 * rcx - 0x80]                             | 48 8d 44 08 80                         |
    | lea rax, qword [rax + 1 * rcx - 0x81]                             | 48 8d 84 08 7f ff ff ff                |
    | lea rax, qword [rax + 1 * rcx + 0xff]                             | 48 8d 84 08 ff 00 00 00                |
    | lea rax, qword [rax + 1 * rcx - 0xff]                             | 48 8d 84 08 01 ff ff ff                |
    | lea rax, qword [rax + 1 * rcx + 0x7fffffff]                       | 48 8d 84 08 ff ff ff 7f                |
    | lea rax, qword [rax + 1 * rcx - 0x7fffffff]                       | 48 8d 84 08 01 00 00 80                |
    | lea rax, qword [rax + 1 * rcx - 0x80000000]                       | 48 8d 84 08 00 00 00 80                |
    | lea rax, qword [r10 + 0x7f]                                       | 49 8d 42 7f                            |
    | lea rax, qword [r10 + 0x80]                                       | 49 8d 82 80 00 00 00                   |
    | lea rax, qword [r10 - 0x80]                                       | 49 8d 42 80                            |
    | lea rax, qword [r10 - 0x81]                                       | 49 8d 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; lea rax, qword [rel @prev5]      | 90 90 90 90 90 48 8d 05 f4 ff ff ff    |
    | .prev1: nop; lea rax, qword [rel @prev1]                          | 90 48 8d 05 f8 ff ff ff                |
    | lea rax, qword [rel @next1]; nop; .next1: nop                     | 48 8d 05 01 00 00 00 90 90             |
    | lea rax, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 8d 05 05 00 00 00 90 90 90 90 90 90 |
    | lea rcx, qword [rdx]                                              | 48 8d 0a                               |
    | lea rdx, qword [rbx]                                              | 48 8d 13                               |
    | lea rbx, qword [rsp]                                              | 48 8d 1c 24                            |
    | lea rsp, qword [rbp]                                              | 48 8d 65 00                            |
    | lea rbp, qword [rsi]                                              | 48 8d 2e                               |
    | lea rsi, qword [rdi]                                              | 48 8d 37                               |
    | lea rdi, qword [r8]                                               | 49 8d 38                               |
    | lea r8, qword [r9]                                                | 4d 8d 01                               |
    | lea r9, qword [r10]                                               | 4d 8d 0a                               |
    | lea r10, qword [r11]                                              | 4d 8d 13                               |
    | lea r11, qword [r12]                                              | 4d 8d 1c 24                            |
    | lea r12, qword [r13]                                              | 4d 8d 65 00                            |
    | lea r13, qword [r14]                                              | 4d 8d 2e                               |
    | lea r14, qword [r15]                                              | 4d 8d 37                               |
    | lea r15, qword [rax + 1 * rcx]                                    | 4c 8d 3c 08                            |
    | lea rcx, qword [rdx + 1 * rcx]                                    | 48 8d 0c 0a                            |
    | lea rdx, qword [rbx + 1 * rcx]                                    | 48 8d 14 0b                            |
    | lea rbx, qword [rsp + 1 * rcx]                                    | 48 8d 1c 0c                            |
    | lea rsp, qword [rbp + 1 * rcx]                                    | 48 8d 64 0d 00                         |
    | lea rbp, qword [rsi + 1 * rcx]                                    | 48 8d 2c 0e                            |
    | lea rsi, qword [rdi + 1 * rcx]                                    | 48 8d 34 0f                            |
    | lea rdi, qword [r8 + 1 * rcx]                                     | 49 8d 3c 08                            |
    | lea r8, qword [r9 + 1 * rcx]                                      | 4d 8d 04 09                            |
    | lea r9, qword [r10 + 1 * rcx]                                     | 4d 8d 0c 0a                            |
    | lea r10, qword [r11 + 1 * rcx]                                    | 4d 8d 14 0b                            |
    | lea r11, qword [r12 + 1 * rcx]                                    | 4d 8d 1c 0c                            |
    | lea r12, qword [r13 + 1 * rcx]                                    | 4d 8d 64 0d 00                         |
    | lea r13, qword [r14 + 1 * rcx]                                    | 4d 8d 2c 0e                            |
    | lea r14, qword [r15 + 1 * rcx]                                    | 4d 8d 34 0f                            |
    | lea r15, qword [rax + 1 * rax]                                    | 4c 8d 3c 00                            |
    | lea rcx, qword [rax + 1 * rbx]                                    | 48 8d 0c 18                            |
    | lea rdx, qword [rax + 1 * rbp]                                    | 48 8d 14 28                            |
    | lea rbx, qword [rax + 1 * rsi]                                    | 48 8d 1c 30                            |
    | lea rsp, qword [rax + 1 * rdi]                                    | 48 8d 24 38                            |
    | lea rbp, qword [rax + 1 * r8]                                     | 4a 8d 2c 00                            |
    | lea rsi, qword [rax + 1 * r9]                                     | 4a 8d 34 08                            |
    | lea rdi, qword [rax + 1 * r10]                                    | 4a 8d 3c 10                            |
    | lea r8, qword [rax + 1 * r11]                                     | 4e 8d 04 18                            |
    | lea r9, qword [rax + 1 * r12]                                     | 4e 8d 0c 20                            |
    | lea r10, qword [rax + 1 * r13]                                    | 4e 8d 14 28                            |
    | lea r11, qword [rax + 1 * r14]                                    | 4e 8d 1c 30                            |
    | lea r12, qword [rax + 1 * r15]                                    | 4e 8d 24 38                            |
    | lea r13, qword [rax + 2 * rcx]                                    | 4c 8d 2c 48                            |
    | lea r14, qword [rax + 4 * rcx]                                    | 4c 8d 34 88                            |
    | lea r15, qword [rax + 8 * rcx]                                    | 4c 8d 3c c8                            |
    | lea rcx, qword [r8 + 2 * r9]                                      | 4b 8d 0c 48                            |
    | lea rdx, qword [r8 + 4 * r9]                                      | 4b 8d 14 88                            |
    | lea rbx, qword [r8 + 8 * r9]                                      | 4b 8d 1c c8                            |
    | lea rsp, qword [1 * rcx]                                          | 48 8d 24 0d 00 00 00 00                |
    | lea rbp, qword [2 * rcx]                                          | 48 8d 2c 4d 00 00 00 00                |
    | lea rsi, qword [4 * rcx]                                          | 48 8d 34 8d 00 00 00 00                |
    | lea rdi, qword [8 * rcx]                                          | 48 8d 3c cd 00 00 00 00                |
    | lea r8, qword [1 * r9]                                            | 4e 8d 04 0d 00 00 00 00                |
    | lea r9, qword [2 * r9]                                            | 4e 8d 0c 4d 00 00 00 00                |
    | lea r10, qword [4 * r9]                                           | 4e 8d 14 8d 00 00 00 00                |
    | lea r11, qword [8 * r9]                                           | 4e 8d 1c cd 00 00 00 00                |
    | lea r12, qword [r13 + 8 * r12]                                    | 4f 8d 64 e5 00                         |
    | lea r13, qword [rsp + 4 * r15]                                    | 4e 8d 2c bc                            |
    | lea r14, qword [rax + 1 * rcx + 0x00]                             | 4c 8d 74 08 00                         |
    | lea r15, qword [rax + 1 * rcx - 0x00]                             | 4c 8d 7c 08 00                         |
    | lea rcx, qword [rax + 1 * rcx - 0x01]                             | 48 8d 4c 08 ff                         |
    | lea rdx, qword [rax + 1 * rcx + 0x00000001]                       | 48 8d 94 08 01 00 00 00                |
    | lea rbx, qword [rax + 1 * rcx - 0x00000001]                       | 48 8d 9c 08 ff ff ff ff                |
    | lea rsp, qword [rax + 1 * rcx + 0x7f]                             | 48 8d 64 08 7f                         |
    | lea rbp, qword [rax + 1 * rcx - 0x7f]                             | 48 8d 6c 08 81                         |
    | lea rsi, qword [rax + 1 * rcx + 0x80]                             | 48 8d b4 08 80 00 00 00                |
    | lea rdi, qword [rax + 1 * rcx - 0x80]                             | 48 8d 7c 08 80                         |
    | lea r8, qword [rax + 1 * rcx - 0x81]                              | 4c 8d 84 08 7f ff ff ff                |
    | lea r9, qword [rax + 1 * rcx + 0xff]                              | 4c 8d 8c 08 ff 00 00 00                |
    | lea r10, qword [rax + 1 * rcx - 0xff]                             | 4c 8d 94 08 01 ff ff ff                |
    | lea r11, qword [rax + 1 * rcx + 0x7fffffff]                       | 4c 8d 9c 08 ff ff ff 7f                |
    | lea r12, qword [rax + 1 * rcx - 0x7fffffff]                       | 4c 8d a4 08 01 00 00 80                |
    | lea r13, qword [rax + 1 * rcx - 0x80000000]                       | 4c 8d ac 08 00 00 00 80                |
    | lea r14, qword [r10 + 0x7f]                                       | 4d 8d 72 7f                            |
    | lea r15, qword [r10 + 0x80]                                       | 4d 8d ba 80 00 00 00                   |
    | lea rcx, qword [r10 - 0x81]                                       | 49 8d 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; lea rdx, qword [rel @prev5]      | 90 90 90 90 90 48 8d 15 f4 ff ff ff    |
    | .prev1: nop; lea rbx, qword [rel @prev1]                          | 90 48 8d 1d f8 ff ff ff                |
    | lea rsp, qword [rel @next1]; nop; .next1: nop                     | 48 8d 25 01 00 00 00 90 90             |
    | lea rbp, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 8d 2d 05 00 00 00 90 90 90 90 90 90 |
    | lea rsi, qword [rax]                                              | 48 8d 30                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_lea_reg64_addr64():
    encode(LEA_REG64_ADDR64)


LEA_REG32_ADDR64 = """
    | ----------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                       | encoding                            |
    | ----------------------------------------------------------------- | ----------------------------------- |
    | lea eax, qword [rcx]                                              | 8d 01                               |
    | lea ecx, qword [rcx]                                              | 8d 09                               |
    | lea edx, qword [rcx]                                              | 8d 11                               |
    | lea ebx, qword [rcx]                                              | 8d 19                               |
    | lea esp, qword [rcx]                                              | 8d 21                               |
    | lea ebp, qword [rcx]                                              | 8d 29                               |
    | lea esi, qword [rcx]                                              | 8d 31                               |
    | lea edi, qword [rcx]                                              | 8d 39                               |
    | lea r8d, qword [rcx]                                              | 44 8d 01                            |
    | lea r9d, qword [rcx]                                              | 44 8d 09                            |
    | lea r10d, qword [rcx]                                             | 44 8d 11                            |
    | lea r11d, qword [rcx]                                             | 44 8d 19                            |
    | lea r12d, qword [rcx]                                             | 44 8d 21                            |
    | lea r13d, qword [rcx]                                             | 44 8d 29                            |
    | lea r14d, qword [rcx]                                             | 44 8d 31                            |
    | lea r15d, qword [rcx]                                             | 44 8d 39                            |
    | lea eax, qword [rax]                                              | 8d 00                               |
    | lea eax, qword [rdx]                                              | 8d 02                               |
    | lea eax, qword [rbx]                                              | 8d 03                               |
    | lea eax, qword [rsp]                                              | 8d 04 24                            |
    | lea eax, qword [rbp]                                              | 8d 45 00                            |
    | lea eax, qword [rsi]                                              | 8d 06                               |
    | lea eax, qword [rdi]                                              | 8d 07                               |
    | lea eax, qword [r8]                                               | 41 8d 00                            |
    | lea eax, qword [r9]                                               | 41 8d 01                            |
    | lea eax, qword [r10]                                              | 41 8d 02                            |
    | lea eax, qword [r11]                                              | 41 8d 03                            |
    | lea eax, qword [r12]                                              | 41 8d 04 24                         |
    | lea eax, qword [r13]                                              | 41 8d 45 00                         |
    | lea eax, qword [r14]                                              | 41 8d 06                            |
    | lea eax, qword [r15]                                              | 41 8d 07                            |
    | lea eax, qword [rax + 1 * rcx]                                    | 8d 04 08                            |
    | lea eax, qword [rcx + 1 * rcx]                                    | 8d 04 09                            |
    | lea eax, qword [rdx + 1 * rcx]                                    | 8d 04 0a                            |
    | lea eax, qword [rbx + 1 * rcx]                                    | 8d 04 0b                            |
    | lea eax, qword [rsp + 1 * rcx]                                    | 8d 04 0c                            |
    | lea eax, qword [rbp + 1 * rcx]                                    | 8d 44 0d 00                         |
    | lea eax, qword [rsi + 1 * rcx]                                    | 8d 04 0e                            |
    | lea eax, qword [rdi + 1 * rcx]                                    | 8d 04 0f                            |
    | lea eax, qword [r8 + 1 * rcx]                                     | 41 8d 04 08                         |
    | lea eax, qword [r9 + 1 * rcx]                                     | 41 8d 04 09                         |
    | lea eax, qword [r10 + 1 * rcx]                                    | 41 8d 04 0a                         |
    | lea eax, qword [r11 + 1 * rcx]                                    | 41 8d 04 0b                         |
    | lea eax, qword [r12 + 1 * rcx]                                    | 41 8d 04 0c                         |
    | lea eax, qword [r13 + 1 * rcx]                                    | 41 8d 44 0d 00                      |
    | lea eax, qword [r14 + 1 * rcx]                                    | 41 8d 04 0e                         |
    | lea eax, qword [r15 + 1 * rcx]                                    | 41 8d 04 0f                         |
    | lea eax, qword [rax + 1 * rax]                                    | 8d 04 00                            |
    | lea eax, qword [rax + 1 * rdx]                                    | 8d 04 10                            |
    | lea eax, qword [rax + 1 * rbx]                                    | 8d 04 18                            |
    | lea eax, qword [rax + 1 * rbp]                                    | 8d 04 28                            |
    | lea eax, qword [rax + 1 * rsi]                                    | 8d 04 30                            |
    | lea eax, qword [rax + 1 * rdi]                                    | 8d 04 38                            |
    | lea eax, qword [rax + 1 * r8]                                     | 42 8d 04 00                         |
    | lea eax, qword [rax + 1 * r9]                                     | 42 8d 04 08                         |
    | lea eax, qword [rax + 1 * r10]                                    | 42 8d 04 10                         |
    | lea eax, qword [rax + 1 * r11]                                    | 42 8d 04 18                         |
    | lea eax, qword [rax + 1 * r12]                                    | 42 8d 04 20                         |
    | lea eax, qword [rax + 1 * r13]                                    | 42 8d 04 28                         |
    | lea eax, qword [rax + 1 * r14]                                    | 42 8d 04 30                         |
    | lea eax, qword [rax + 1 * r15]                                    | 42 8d 04 38                         |
    | lea eax, qword [rax + 2 * rcx]                                    | 8d 04 48                            |
    | lea eax, qword [rax + 4 * rcx]                                    | 8d 04 88                            |
    | lea eax, qword [rax + 8 * rcx]                                    | 8d 04 c8                            |
    | lea eax, qword [r8 + 1 * r9]                                      | 43 8d 04 08                         |
    | lea eax, qword [r8 + 2 * r9]                                      | 43 8d 04 48                         |
    | lea eax, qword [r8 + 4 * r9]                                      | 43 8d 04 88                         |
    | lea eax, qword [r8 + 8 * r9]                                      | 43 8d 04 c8                         |
    | lea eax, qword [1 * rcx]                                          | 8d 04 0d 00 00 00 00                |
    | lea eax, qword [2 * rcx]                                          | 8d 04 4d 00 00 00 00                |
    | lea eax, qword [4 * rcx]                                          | 8d 04 8d 00 00 00 00                |
    | lea eax, qword [8 * rcx]                                          | 8d 04 cd 00 00 00 00                |
    | lea eax, qword [1 * r9]                                           | 42 8d 04 0d 00 00 00 00             |
    | lea eax, qword [2 * r9]                                           | 42 8d 04 4d 00 00 00 00             |
    | lea eax, qword [4 * r9]                                           | 42 8d 04 8d 00 00 00 00             |
    | lea eax, qword [8 * r9]                                           | 42 8d 04 cd 00 00 00 00             |
    | lea eax, qword [r13 + 8 * r12]                                    | 43 8d 44 e5 00                      |
    | lea eax, qword [rsp + 4 * r15]                                    | 42 8d 04 bc                         |
    | lea eax, qword [rax + 1 * rcx + 0x00]                             | 8d 44 08 00                         |
    | lea eax, qword [rax + 1 * rcx - 0x00]                             | 8d 44 08 00                         |
    | lea eax, qword [rax + 1 * rcx + 0x01]                             | 8d 44 08 01                         |
    | lea eax, qword [rax + 1 * rcx - 0x01]                             | 8d 44 08 ff                         |
    | lea eax, qword [rax + 1 * rcx + 0x00000001]                       | 8d 84 08 01 00 00 00                |
    | lea eax, qword [rax + 1 * rcx - 0x00000001]                       | 8d 84 08 ff ff ff ff                |
    | lea eax, qword [rax + 1 * rcx + 0x7f]                             | 8d 44 08 7f                         |
    | lea eax, qword [rax + 1 * rcx - 0x7f]                             | 8d 44 08 81                         |
    | lea eax, qword [rax + 1 * rcx + 0x80]                             | 8d 84 08 80 00 00 00                |
    | lea eax, qword [rax + 1 * rcx - 0x80]                             | 8d 44 08 80                         |
    | lea eax, qword [rax + 1 * rcx - 0x81]                             | 8d 84 08 7f ff ff ff                |
    | lea eax, qword [rax + 1 * rcx + 0xff]                             | 8d 84 08 ff 00 00 00                |
    | lea eax, qword [rax + 1 * rcx - 0xff]                             | 8d 84 08 01 ff ff ff                |
    | lea eax, qword [rax + 1 * rcx + 0x7fffffff]                       | 8d 84 08 ff ff ff 7f                |
    | lea eax, qword [rax + 1 * rcx - 0x7fffffff]                       | 8d 84 08 01 00 00 80                |
    | lea eax, qword [rax + 1 * rcx - 0x80000000]                       | 8d 84 08 00 00 00 80                |
    | lea eax, qword [r10 + 0x7f]                                       | 41 8d 42 7f                         |
    | lea eax, qword [r10 + 0x80]                                       | 41 8d 82 80 00 00 00                |
    | lea eax, qword [r10 - 0x80]                                       | 41 8d 42 80                         |
    | lea eax, qword [r10 - 0x81]                                       | 41 8d 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; lea eax, qword [rel @prev5]      | 90 90 90 90 90 8d 05 f5 ff ff ff    |
    | .prev1: nop; lea eax, qword [rel @prev1]                          | 90 8d 05 f9 ff ff ff                |
    | lea eax, qword [rel @next1]; nop; .next1: nop                     | 8d 05 01 00 00 00 90 90             |
    | lea eax, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 8d 05 05 00 00 00 90 90 90 90 90 90 |
    | lea ecx, qword [rdx]                                              | 8d 0a                               |
    | lea edx, qword [rbx]                                              | 8d 13                               |
    | lea ebx, qword [rsp]                                              | 8d 1c 24                            |
    | lea esp, qword [rbp]                                              | 8d 65 00                            |
    | lea ebp, qword [rsi]                                              | 8d 2e                               |
    | lea esi, qword [rdi]                                              | 8d 37                               |
    | lea edi, qword [r8]                                               | 41 8d 38                            |
    | lea r8d, qword [r9]                                               | 45 8d 01                            |
    | lea r9d, qword [r10]                                              | 45 8d 0a                            |
    | lea r10d, qword [r11]                                             | 45 8d 13                            |
    | lea r11d, qword [r12]                                             | 45 8d 1c 24                         |
    | lea r12d, qword [r13]                                             | 45 8d 65 00                         |
    | lea r13d, qword [r14]                                             | 45 8d 2e                            |
    | lea r14d, qword [r15]                                             | 45 8d 37                            |
    | lea r15d, qword [rax + 1 * rcx]                                   | 44 8d 3c 08                         |
    | lea ecx, qword [rdx + 1 * rcx]                                    | 8d 0c 0a                            |
    | lea edx, qword [rbx + 1 * rcx]                                    | 8d 14 0b                            |
    | lea ebx, qword [rsp + 1 * rcx]                                    | 8d 1c 0c                            |
    | lea esp, qword [rbp + 1 * rcx]                                    | 8d 64 0d 00                         |
    | lea ebp, qword [rsi + 1 * rcx]                                    | 8d 2c 0e                            |
    | lea esi, qword [rdi + 1 * rcx]                                    | 8d 34 0f                            |
    | lea edi, qword [r8 + 1 * rcx]                                     | 41 8d 3c 08                         |
    | lea r8d, qword [r9 + 1 * rcx]                                     | 45 8d 04 09                         |
    | lea r9d, qword [r10 + 1 * rcx]                                    | 45 8d 0c 0a                         |
    | lea r10d, qword [r11 + 1 * rcx]                                   | 45 8d 14 0b                         |
    | lea r11d, qword [r12 + 1 * rcx]                                   | 45 8d 1c 0c                         |
    | lea r12d, qword [r13 + 1 * rcx]                                   | 45 8d 64 0d 00                      |
    | lea r13d, qword [r14 + 1 * rcx]                                   | 45 8d 2c 0e                         |
    | lea r14d, qword [r15 + 1 * rcx]                                   | 45 8d 34 0f                         |
    | lea r15d, qword [rax + 1 * rax]                                   | 44 8d 3c 00                         |
    | lea ecx, qword [rax + 1 * rbx]                                    | 8d 0c 18                            |
    | lea edx, qword [rax + 1 * rbp]                                    | 8d 14 28                            |
    | lea ebx, qword [rax + 1 * rsi]                                    | 8d 1c 30                            |
    | lea esp, qword [rax + 1 * rdi]                                    | 8d 24 38                            |
    | lea ebp, qword [rax + 1 * r8]                                     | 42 8d 2c 00                         |
    | lea esi, qword [rax + 1 * r9]                                     | 42 8d 34 08                         |
    | lea edi, qword [rax + 1 * r10]                                    | 42 8d 3c 10                         |
    | lea r8d, qword [rax + 1 * r11]                                    | 46 8d 04 18                         |
    | lea r9d, qword [rax + 1 * r12]                                    | 46 8d 0c 20                         |
    | lea r10d, qword [rax + 1 * r13]                                   | 46 8d 14 28                         |
    | lea r11d, qword [rax + 1 * r14]                                   | 46 8d 1c 30                         |
    | lea r12d, qword [rax + 1 * r15]                                   | 46 8d 24 38                         |
    | lea r13d, qword [rax + 2 * rcx]                                   | 44 8d 2c 48                         |
    | lea r14d, qword [rax + 4 * rcx]                                   | 44 8d 34 88                         |
    | lea r15d, qword [rax + 8 * rcx]                                   | 44 8d 3c c8                         |
    | lea ecx, qword [r8 + 2 * r9]                                      | 43 8d 0c 48                         |
    | lea edx, qword [r8 + 4 * r9]                                      | 43 8d 14 88                         |
    | lea ebx, qword [r8 + 8 * r9]                                      | 43 8d 1c c8                         |
    | lea esp, qword [1 * rcx]                                          | 8d 24 0d 00 00 00 00                |
    | lea ebp, qword [2 * rcx]                                          | 8d 2c 4d 00 00 00 00                |
    | lea esi, qword [4 * rcx]                                          | 8d 34 8d 00 00 00 00                |
    | lea edi, qword [8 * rcx]                                          | 8d 3c cd 00 00 00 00                |
    | lea r8d, qword [1 * r9]                                           | 46 8d 04 0d 00 00 00 00             |
    | lea r9d, qword [2 * r9]                                           | 46 8d 0c 4d 00 00 00 00             |
    | lea r10d, qword [4 * r9]                                          | 46 8d 14 8d 00 00 00 00             |
    | lea r11d, qword [8 * r9]                                          | 46 8d 1c cd 00 00 00 00             |
    | lea r12d, qword [r13 + 8 * r12]                                   | 47 8d 64 e5 00                      |
    | lea r13d, qword [rsp + 4 * r15]                                   | 46 8d 2c bc                         |
    | lea r14d, qword [rax + 1 * rcx + 0x00]                            | 44 8d 74 08 00                      |
    | lea r15d, qword [rax + 1 * rcx - 0x00]                            | 44 8d 7c 08 00                      |
    | lea ecx, qword [rax + 1 * rcx - 0x01]                             | 8d 4c 08 ff                         |
    | lea edx, qword [rax + 1 * rcx + 0x00000001]                       | 8d 94 08 01 00 00 00                |
    | lea ebx, qword [rax + 1 * rcx - 0x00000001]                       | 8d 9c 08 ff ff ff ff                |
    | lea esp, qword [rax + 1 * rcx + 0x7f]                             | 8d 64 08 7f                         |
    | lea ebp, qword [rax + 1 * rcx - 0x7f]                             | 8d 6c 08 81                         |
    | lea esi, qword [rax + 1 * rcx + 0x80]                             | 8d b4 08 80 00 00 00                |
    | lea edi, qword [rax + 1 * rcx - 0x80]                             | 8d 7c 08 80                         |
    | lea r8d, qword [rax + 1 * rcx - 0x81]                             | 44 8d 84 08 7f ff ff ff             |
    | lea r9d, qword [rax + 1 * rcx + 0xff]                             | 44 8d 8c 08 ff 00 00 00             |
    | lea r10d, qword [rax + 1 * rcx - 0xff]                            | 44 8d 94 08 01 ff ff ff             |
    | lea r11d, qword [rax + 1 * rcx + 0x7fffffff]                      | 44 8d 9c 08 ff ff ff 7f             |
    | lea r12d, qword [rax + 1 * rcx - 0x7fffffff]                      | 44 8d a4 08 01 00 00 80             |
    | lea r13d, qword [rax + 1 * rcx - 0x80000000]                      | 44 8d ac 08 00 00 00 80             |
    | lea r14d, qword [r10 + 0x7f]                                      | 45 8d 72 7f                         |
    | lea r15d, qword [r10 + 0x80]                                      | 45 8d ba 80 00 00 00                |
    | lea ecx, qword [r10 - 0x81]                                       | 41 8d 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; lea edx, qword [rel @prev5]      | 90 90 90 90 90 8d 15 f5 ff ff ff    |
    | .prev1: nop; lea ebx, qword [rel @prev1]                          | 90 8d 1d f9 ff ff ff                |
    | lea esp, qword [rel @next1]; nop; .next1: nop                     | 8d 25 01 00 00 00 90 90             |
    | lea ebp, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 8d 2d 05 00 00 00 90 90 90 90 90 90 |
    | lea esi, qword [rax]                                              | 8d 30                               |
    | ----------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_lea_reg32_addr64():
    encode(LEA_REG32_ADDR64)


LEA_REG16_ADDR64 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | lea ax, qword [rcx]                                              | 66 8d 01                               |
    | lea cx, qword [rcx]                                              | 66 8d 09                               |
    | lea dx, qword [rcx]                                              | 66 8d 11                               |
    | lea bx, qword [rcx]                                              | 66 8d 19                               |
    | lea sp, qword [rcx]                                              | 66 8d 21                               |
    | lea bp, qword [rcx]                                              | 66 8d 29                               |
    | lea si, qword [rcx]                                              | 66 8d 31                               |
    | lea di, qword [rcx]                                              | 66 8d 39                               |
    | lea r8w, qword [rcx]                                             | 66 44 8d 01                            |
    | lea r9w, qword [rcx]                                             | 66 44 8d 09                            |
    | lea r10w, qword [rcx]                                            | 66 44 8d 11                            |
    | lea r11w, qword [rcx]                                            | 66 44 8d 19                            |
    | lea r12w, qword [rcx]                                            | 66 44 8d 21                            |
    | lea r13w, qword [rcx]                                            | 66 44 8d 29                            |
    | lea r14w, qword [rcx]                                            | 66 44 8d 31                            |
    | lea r15w, qword [rcx]                                            | 66 44 8d 39                            |
    | lea ax, qword [rax]                                              | 66 8d 00                               |
    | lea ax, qword [rdx]                                              | 66 8d 02                               |
    | lea ax, qword [rbx]                                              | 66 8d 03                               |
    | lea ax, qword [rsp]                                              | 66 8d 04 24                            |
    | lea ax, qword [rbp]                                              | 66 8d 45 00                            |
    | lea ax, qword [rsi]                                              | 66 8d 06                               |
    | lea ax, qword [rdi]                                              | 66 8d 07                               |
    | lea ax, qword [r8]                                               | 66 41 8d 00                            |
    | lea ax, qword [r9]                                               | 66 41 8d 01                            |
    | lea ax, qword [r10]                                              | 66 41 8d 02                            |
    | lea ax, qword [r11]                                              | 66 41 8d 03                            |
    | lea ax, qword [r12]                                              | 66 41 8d 04 24                         |
    | lea ax, qword [r13]                                              | 66 41 8d 45 00                         |
    | lea ax, qword [r14]                                              | 66 41 8d 06                            |
    | lea ax, qword [r15]                                              | 66 41 8d 07                            |
    | lea ax, qword [rax + 1 * rcx]                                    | 66 8d 04 08                            |
    | lea ax, qword [rcx + 1 * rcx]                                    | 66 8d 04 09                            |
    | lea ax, qword [rdx + 1 * rcx]                                    | 66 8d 04 0a                            |
    | lea ax, qword [rbx + 1 * rcx]                                    | 66 8d 04 0b                            |
    | lea ax, qword [rsp + 1 * rcx]                                    | 66 8d 04 0c                            |
    | lea ax, qword [rbp + 1 * rcx]                                    | 66 8d 44 0d 00                         |
    | lea ax, qword [rsi + 1 * rcx]                                    | 66 8d 04 0e                            |
    | lea ax, qword [rdi + 1 * rcx]                                    | 66 8d 04 0f                            |
    | lea ax, qword [r8 + 1 * rcx]                                     | 66 41 8d 04 08                         |
    | lea ax, qword [r9 + 1 * rcx]                                     | 66 41 8d 04 09                         |
    | lea ax, qword [r10 + 1 * rcx]                                    | 66 41 8d 04 0a                         |
    | lea ax, qword [r11 + 1 * rcx]                                    | 66 41 8d 04 0b                         |
    | lea ax, qword [r12 + 1 * rcx]                                    | 66 41 8d 04 0c                         |
    | lea ax, qword [r13 + 1 * rcx]                                    | 66 41 8d 44 0d 00                      |
    | lea ax, qword [r14 + 1 * rcx]                                    | 66 41 8d 04 0e                         |
    | lea ax, qword [r15 + 1 * rcx]                                    | 66 41 8d 04 0f                         |
    | lea ax, qword [rax + 1 * rax]                                    | 66 8d 04 00                            |
    | lea ax, qword [rax + 1 * rdx]                                    | 66 8d 04 10                            |
    | lea ax, qword [rax + 1 * rbx]                                    | 66 8d 04 18                            |
    | lea ax, qword [rax + 1 * rbp]                                    | 66 8d 04 28                            |
    | lea ax, qword [rax + 1 * rsi]                                    | 66 8d 04 30                            |
    | lea ax, qword [rax + 1 * rdi]                                    | 66 8d 04 38                            |
    | lea ax, qword [rax + 1 * r8]                                     | 66 42 8d 04 00                         |
    | lea ax, qword [rax + 1 * r9]                                     | 66 42 8d 04 08                         |
    | lea ax, qword [rax + 1 * r10]                                    | 66 42 8d 04 10                         |
    | lea ax, qword [rax + 1 * r11]                                    | 66 42 8d 04 18                         |
    | lea ax, qword [rax + 1 * r12]                                    | 66 42 8d 04 20                         |
    | lea ax, qword [rax + 1 * r13]                                    | 66 42 8d 04 28                         |
    | lea ax, qword [rax + 1 * r14]                                    | 66 42 8d 04 30                         |
    | lea ax, qword [rax + 1 * r15]                                    | 66 42 8d 04 38                         |
    | lea ax, qword [rax + 2 * rcx]                                    | 66 8d 04 48                            |
    | lea ax, qword [rax + 4 * rcx]                                    | 66 8d 04 88                            |
    | lea ax, qword [rax + 8 * rcx]                                    | 66 8d 04 c8                            |
    | lea ax, qword [r8 + 1 * r9]                                      | 66 43 8d 04 08                         |
    | lea ax, qword [r8 + 2 * r9]                                      | 66 43 8d 04 48                         |
    | lea ax, qword [r8 + 4 * r9]                                      | 66 43 8d 04 88                         |
    | lea ax, qword [r8 + 8 * r9]                                      | 66 43 8d 04 c8                         |
    | lea ax, qword [1 * rcx]                                          | 66 8d 04 0d 00 00 00 00                |
    | lea ax, qword [2 * rcx]                                          | 66 8d 04 4d 00 00 00 00                |
    | lea ax, qword [4 * rcx]                                          | 66 8d 04 8d 00 00 00 00                |
    | lea ax, qword [8 * rcx]                                          | 66 8d 04 cd 00 00 00 00                |
    | lea ax, qword [1 * r9]                                           | 66 42 8d 04 0d 00 00 00 00             |
    | lea ax, qword [2 * r9]                                           | 66 42 8d 04 4d 00 00 00 00             |
    | lea ax, qword [4 * r9]                                           | 66 42 8d 04 8d 00 00 00 00             |
    | lea ax, qword [8 * r9]                                           | 66 42 8d 04 cd 00 00 00 00             |
    | lea ax, qword [r13 + 8 * r12]                                    | 66 43 8d 44 e5 00                      |
    | lea ax, qword [rsp + 4 * r15]                                    | 66 42 8d 04 bc                         |
    | lea ax, qword [rax + 1 * rcx + 0x00]                             | 66 8d 44 08 00                         |
    | lea ax, qword [rax + 1 * rcx - 0x00]                             | 66 8d 44 08 00                         |
    | lea ax, qword [rax + 1 * rcx + 0x01]                             | 66 8d 44 08 01                         |
    | lea ax, qword [rax + 1 * rcx - 0x01]                             | 66 8d 44 08 ff                         |
    | lea ax, qword [rax + 1 * rcx + 0x00000001]                       | 66 8d 84 08 01 00 00 00                |
    | lea ax, qword [rax + 1 * rcx - 0x00000001]                       | 66 8d 84 08 ff ff ff ff                |
    | lea ax, qword [rax + 1 * rcx + 0x7f]                             | 66 8d 44 08 7f                         |
    | lea ax, qword [rax + 1 * rcx - 0x7f]                             | 66 8d 44 08 81                         |
    | lea ax, qword [rax + 1 * rcx + 0x80]                             | 66 8d 84 08 80 00 00 00                |
    | lea ax, qword [rax + 1 * rcx - 0x80]                             | 66 8d 44 08 80                         |
    | lea ax, qword [rax + 1 * rcx - 0x81]                             | 66 8d 84 08 7f ff ff ff                |
    | lea ax, qword [rax + 1 * rcx + 0xff]                             | 66 8d 84 08 ff 00 00 00                |
    | lea ax, qword [rax + 1 * rcx - 0xff]                             | 66 8d 84 08 01 ff ff ff                |
    | lea ax, qword [rax + 1 * rcx + 0x7fffffff]                       | 66 8d 84 08 ff ff ff 7f                |
    | lea ax, qword [rax + 1 * rcx - 0x7fffffff]                       | 66 8d 84 08 01 00 00 80                |
    | lea ax, qword [rax + 1 * rcx - 0x80000000]                       | 66 8d 84 08 00 00 00 80                |
    | lea ax, qword [r10 + 0x7f]                                       | 66 41 8d 42 7f                         |
    | lea ax, qword [r10 + 0x80]                                       | 66 41 8d 82 80 00 00 00                |
    | lea ax, qword [r10 - 0x80]                                       | 66 41 8d 42 80                         |
    | lea ax, qword [r10 - 0x81]                                       | 66 41 8d 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; lea ax, qword [rel @prev5]      | 90 90 90 90 90 66 8d 05 f4 ff ff ff    |
    | .prev1: nop; lea ax, qword [rel @prev1]                          | 90 66 8d 05 f8 ff ff ff                |
    | lea ax, qword [rel @next1]; nop; .next1: nop                     | 66 8d 05 01 00 00 00 90 90             |
    | lea ax, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 8d 05 05 00 00 00 90 90 90 90 90 90 |
    | lea cx, qword [rdx]                                              | 66 8d 0a                               |
    | lea dx, qword [rbx]                                              | 66 8d 13                               |
    | lea bx, qword [rsp]                                              | 66 8d 1c 24                            |
    | lea sp, qword [rbp]                                              | 66 8d 65 00                            |
    | lea bp, qword [rsi]                                              | 66 8d 2e                               |
    | lea si, qword [rdi]                                              | 66 8d 37                               |
    | lea di, qword [r8]                                               | 66 41 8d 38                            |
    | lea r8w, qword [r9]                                              | 66 45 8d 01                            |
    | lea r9w, qword [r10]                                             | 66 45 8d 0a                            |
    | lea r10w, qword [r11]                                            | 66 45 8d 13                            |
    | lea r11w, qword [r12]                                            | 66 45 8d 1c 24                         |
    | lea r12w, qword [r13]                                            | 66 45 8d 65 00                         |
    | lea r13w, qword [r14]                                            | 66 45 8d 2e                            |
    | lea r14w, qword [r15]                                            | 66 45 8d 37                            |
    | lea r15w, qword [rax + 1 * rcx]                                  | 66 44 8d 3c 08                         |
    | lea cx, qword [rdx + 1 * rcx]                                    | 66 8d 0c 0a                            |
    | lea dx, qword [rbx + 1 * rcx]                                    | 66 8d 14 0b                            |
    | lea bx, qword [rsp + 1 * rcx]                                    | 66 8d 1c 0c                            |
    | lea sp, qword [rbp + 1 * rcx]                                    | 66 8d 64 0d 00                         |
    | lea bp, qword [rsi + 1 * rcx]                                    | 66 8d 2c 0e                            |
    | lea si, qword [rdi + 1 * rcx]                                    | 66 8d 34 0f                            |
    | lea di, qword [r8 + 1 * rcx]                                     | 66 41 8d 3c 08                         |
    | lea r8w, qword [r9 + 1 * rcx]                                    | 66 45 8d 04 09                         |
    | lea r9w, qword [r10 + 1 * rcx]                                   | 66 45 8d 0c 0a                         |
    | lea r10w, qword [r11 + 1 * rcx]                                  | 66 45 8d 14 0b                         |
    | lea r11w, qword [r12 + 1 * rcx]                                  | 66 45 8d 1c 0c                         |
    | lea r12w, qword [r13 + 1 * rcx]                                  | 66 45 8d 64 0d 00                      |
    | lea r13w, qword [r14 + 1 * rcx]                                  | 66 45 8d 2c 0e                         |
    | lea r14w, qword [r15 + 1 * rcx]                                  | 66 45 8d 34 0f                         |
    | lea r15w, qword [rax + 1 * rax]                                  | 66 44 8d 3c 00                         |
    | lea cx, qword [rax + 1 * rbx]                                    | 66 8d 0c 18                            |
    | lea dx, qword [rax + 1 * rbp]                                    | 66 8d 14 28                            |
    | lea bx, qword [rax + 1 * rsi]                                    | 66 8d 1c 30                            |
    | lea sp, qword [rax + 1 * rdi]                                    | 66 8d 24 38                            |
    | lea bp, qword [rax + 1 * r8]                                     | 66 42 8d 2c 00                         |
    | lea si, qword [rax + 1 * r9]                                     | 66 42 8d 34 08                         |
    | lea di, qword [rax + 1 * r10]                                    | 66 42 8d 3c 10                         |
    | lea r8w, qword [rax + 1 * r11]                                   | 66 46 8d 04 18                         |
    | lea r9w, qword [rax + 1 * r12]                                   | 66 46 8d 0c 20                         |
    | lea r10w, qword [rax + 1 * r13]                                  | 66 46 8d 14 28                         |
    | lea r11w, qword [rax + 1 * r14]                                  | 66 46 8d 1c 30                         |
    | lea r12w, qword [rax + 1 * r15]                                  | 66 46 8d 24 38                         |
    | lea r13w, qword [rax + 2 * rcx]                                  | 66 44 8d 2c 48                         |
    | lea r14w, qword [rax + 4 * rcx]                                  | 66 44 8d 34 88                         |
    | lea r15w, qword [rax + 8 * rcx]                                  | 66 44 8d 3c c8                         |
    | lea cx, qword [r8 + 2 * r9]                                      | 66 43 8d 0c 48                         |
    | lea dx, qword [r8 + 4 * r9]                                      | 66 43 8d 14 88                         |
    | lea bx, qword [r8 + 8 * r9]                                      | 66 43 8d 1c c8                         |
    | lea sp, qword [1 * rcx]                                          | 66 8d 24 0d 00 00 00 00                |
    | lea bp, qword [2 * rcx]                                          | 66 8d 2c 4d 00 00 00 00                |
    | lea si, qword [4 * rcx]                                          | 66 8d 34 8d 00 00 00 00                |
    | lea di, qword [8 * rcx]                                          | 66 8d 3c cd 00 00 00 00                |
    | lea r8w, qword [1 * r9]                                          | 66 46 8d 04 0d 00 00 00 00             |
    | lea r9w, qword [2 * r9]                                          | 66 46 8d 0c 4d 00 00 00 00             |
    | lea r10w, qword [4 * r9]                                         | 66 46 8d 14 8d 00 00 00 00             |
    | lea r11w, qword [8 * r9]                                         | 66 46 8d 1c cd 00 00 00 00             |
    | lea r12w, qword [r13 + 8 * r12]                                  | 66 47 8d 64 e5 00                      |
    | lea r13w, qword [rsp + 4 * r15]                                  | 66 46 8d 2c bc                         |
    | lea r14w, qword [rax + 1 * rcx + 0x00]                           | 66 44 8d 74 08 00                      |
    | lea r15w, qword [rax + 1 * rcx - 0x00]                           | 66 44 8d 7c 08 00                      |
    | lea cx, qword [rax + 1 * rcx - 0x01]                             | 66 8d 4c 08 ff                         |
    | lea dx, qword [rax + 1 * rcx + 0x00000001]                       | 66 8d 94 08 01 00 00 00                |
    | lea bx, qword [rax + 1 * rcx - 0x00000001]                       | 66 8d 9c 08 ff ff ff ff                |
    | lea sp, qword [rax + 1 * rcx + 0x7f]                             | 66 8d 64 08 7f                         |
    | lea bp, qword [rax + 1 * rcx - 0x7f]                             | 66 8d 6c 08 81                         |
    | lea si, qword [rax + 1 * rcx + 0x80]                             | 66 8d b4 08 80 00 00 00                |
    | lea di, qword [rax + 1 * rcx - 0x80]                             | 66 8d 7c 08 80                         |
    | lea r8w, qword [rax + 1 * rcx - 0x81]                            | 66 44 8d 84 08 7f ff ff ff             |
    | lea r9w, qword [rax + 1 * rcx + 0xff]                            | 66 44 8d 8c 08 ff 00 00 00             |
    | lea r10w, qword [rax + 1 * rcx - 0xff]                           | 66 44 8d 94 08 01 ff ff ff             |
    | lea r11w, qword [rax + 1 * rcx + 0x7fffffff]                     | 66 44 8d 9c 08 ff ff ff 7f             |
    | lea r12w, qword [rax + 1 * rcx - 0x7fffffff]                     | 66 44 8d a4 08 01 00 00 80             |
    | lea r13w, qword [rax + 1 * rcx - 0x80000000]                     | 66 44 8d ac 08 00 00 00 80             |
    | lea r14w, qword [r10 + 0x7f]                                     | 66 45 8d 72 7f                         |
    | lea r15w, qword [r10 + 0x80]                                     | 66 45 8d ba 80 00 00 00                |
    | lea cx, qword [r10 - 0x81]                                       | 66 41 8d 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; lea dx, qword [rel @prev5]      | 90 90 90 90 90 66 8d 15 f4 ff ff ff    |
    | .prev1: nop; lea bx, qword [rel @prev1]                          | 90 66 8d 1d f8 ff ff ff                |
    | lea sp, qword [rel @next1]; nop; .next1: nop                     | 66 8d 25 01 00 00 00 90 90             |
    | lea bp, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 8d 2d 05 00 00 00 90 90 90 90 90 90 |
    | lea si, qword [rax]                                              | 66 8d 30                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_lea_reg16_addr64():
    encode(LEA_REG16_ADDR64)
