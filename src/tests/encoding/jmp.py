from tests.encoding.core import encode, exhaust


def can_exhaust_jmp():
    exhaust(JMP_REG64, JMP_ADDR64, JMP_REL)


JMP_REG64 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | jmp rax     | ff e0    | *** | jmp r8      | 41 ff e0 |
    | jmp rcx     | ff e1    | *** | jmp r9      | 41 ff e1 |
    | jmp rdx     | ff e2    | *** | jmp r10     | 41 ff e2 |
    | jmp rbx     | ff e3    | *** | jmp r11     | 41 ff e3 |
    | jmp rsp     | ff e4    | *** | jmp r12     | 41 ff e4 |
    | jmp rbp     | ff e5    | *** | jmp r13     | 41 ff e5 |
    | jmp rsi     | ff e6    | *** | jmp r14     | 41 ff e6 |
    | jmp rdi     | ff e7    | *** | jmp r15     | 41 ff e7 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_jmp_reg64():
    encode(JMP_REG64)


JMP_ADDR64 = """
    | ------------------------------------------------------------ | ----------------------------------- |
    | instruction                                                  | encoding                            |
    | ------------------------------------------------------------ | ----------------------------------- |
    | jmp qword [rax]                                              | ff 20                               |
    | jmp qword [rcx]                                              | ff 21                               |
    | jmp qword [rdx]                                              | ff 22                               |
    | jmp qword [rbx]                                              | ff 23                               |
    | jmp qword [rsp]                                              | ff 24 24                            |
    | jmp qword [rbp]                                              | ff 65 00                            |
    | jmp qword [rsi]                                              | ff 26                               |
    | jmp qword [rdi]                                              | ff 27                               |
    | jmp qword [r8]                                               | 41 ff 20                            |
    | jmp qword [r9]                                               | 41 ff 21                            |
    | jmp qword [r10]                                              | 41 ff 22                            |
    | jmp qword [r11]                                              | 41 ff 23                            |
    | jmp qword [r12]                                              | 41 ff 24 24                         |
    | jmp qword [r13]                                              | 41 ff 65 00                         |
    | jmp qword [r14]                                              | 41 ff 26                            |
    | jmp qword [r15]                                              | 41 ff 27                            |
    | jmp qword [rax + 1 * rcx]                                    | ff 24 08                            |
    | jmp qword [rcx + 1 * rcx]                                    | ff 24 09                            |
    | jmp qword [rdx + 1 * rcx]                                    | ff 24 0a                            |
    | jmp qword [rbx + 1 * rcx]                                    | ff 24 0b                            |
    | jmp qword [rsp + 1 * rcx]                                    | ff 24 0c                            |
    | jmp qword [rbp + 1 * rcx]                                    | ff 64 0d 00                         |
    | jmp qword [rsi + 1 * rcx]                                    | ff 24 0e                            |
    | jmp qword [rdi + 1 * rcx]                                    | ff 24 0f                            |
    | jmp qword [r8 + 1 * rcx]                                     | 41 ff 24 08                         |
    | jmp qword [r9 + 1 * rcx]                                     | 41 ff 24 09                         |
    | jmp qword [r10 + 1 * rcx]                                    | 41 ff 24 0a                         |
    | jmp qword [r11 + 1 * rcx]                                    | 41 ff 24 0b                         |
    | jmp qword [r12 + 1 * rcx]                                    | 41 ff 24 0c                         |
    | jmp qword [r13 + 1 * rcx]                                    | 41 ff 64 0d 00                      |
    | jmp qword [r14 + 1 * rcx]                                    | 41 ff 24 0e                         |
    | jmp qword [r15 + 1 * rcx]                                    | 41 ff 24 0f                         |
    | jmp qword [rax + 1 * rax]                                    | ff 24 00                            |
    | jmp qword [rax + 1 * rdx]                                    | ff 24 10                            |
    | jmp qword [rax + 1 * rbx]                                    | ff 24 18                            |
    | jmp qword [rax + 1 * rbp]                                    | ff 24 28                            |
    | jmp qword [rax + 1 * rsi]                                    | ff 24 30                            |
    | jmp qword [rax + 1 * rdi]                                    | ff 24 38                            |
    | jmp qword [rax + 1 * r8]                                     | 42 ff 24 00                         |
    | jmp qword [rax + 1 * r9]                                     | 42 ff 24 08                         |
    | jmp qword [rax + 1 * r10]                                    | 42 ff 24 10                         |
    | jmp qword [rax + 1 * r11]                                    | 42 ff 24 18                         |
    | jmp qword [rax + 1 * r12]                                    | 42 ff 24 20                         |
    | jmp qword [rax + 1 * r13]                                    | 42 ff 24 28                         |
    | jmp qword [rax + 1 * r14]                                    | 42 ff 24 30                         |
    | jmp qword [rax + 1 * r15]                                    | 42 ff 24 38                         |
    | jmp qword [rax + 2 * rcx]                                    | ff 24 48                            |
    | jmp qword [rax + 4 * rcx]                                    | ff 24 88                            |
    | jmp qword [rax + 8 * rcx]                                    | ff 24 c8                            |
    | jmp qword [r8 + 1 * r9]                                      | 43 ff 24 08                         |
    | jmp qword [r8 + 2 * r9]                                      | 43 ff 24 48                         |
    | jmp qword [r8 + 4 * r9]                                      | 43 ff 24 88                         |
    | jmp qword [r8 + 8 * r9]                                      | 43 ff 24 c8                         |
    | jmp qword [1 * rcx]                                          | ff 24 0d 00 00 00 00                |
    | jmp qword [2 * rcx]                                          | ff 24 4d 00 00 00 00                |
    | jmp qword [4 * rcx]                                          | ff 24 8d 00 00 00 00                |
    | jmp qword [8 * rcx]                                          | ff 24 cd 00 00 00 00                |
    | jmp qword [1 * r9]                                           | 42 ff 24 0d 00 00 00 00             |
    | jmp qword [2 * r9]                                           | 42 ff 24 4d 00 00 00 00             |
    | jmp qword [4 * r9]                                           | 42 ff 24 8d 00 00 00 00             |
    | jmp qword [8 * r9]                                           | 42 ff 24 cd 00 00 00 00             |
    | jmp qword [r13 + 8 * r12]                                    | 43 ff 64 e5 00                      |
    | jmp qword [rsp + 4 * r15]                                    | 42 ff 24 bc                         |
    | jmp qword [rax + 1 * rcx + 0x00]                             | ff 64 08 00                         |
    | jmp qword [rax + 1 * rcx - 0x00]                             | ff 64 08 00                         |
    | jmp qword [rax + 1 * rcx + 0x01]                             | ff 64 08 01                         |
    | jmp qword [rax + 1 * rcx - 0x01]                             | ff 64 08 ff                         |
    | jmp qword [rax + 1 * rcx + 0x00000001]                       | ff a4 08 01 00 00 00                |
    | jmp qword [rax + 1 * rcx - 0x00000001]                       | ff a4 08 ff ff ff ff                |
    | jmp qword [rax + 1 * rcx + 0x7f]                             | ff 64 08 7f                         |
    | jmp qword [rax + 1 * rcx - 0x7f]                             | ff 64 08 81                         |
    | jmp qword [rax + 1 * rcx + 0x80]                             | ff a4 08 80 00 00 00                |
    | jmp qword [rax + 1 * rcx - 0x80]                             | ff 64 08 80                         |
    | jmp qword [rax + 1 * rcx - 0x81]                             | ff a4 08 7f ff ff ff                |
    | jmp qword [rax + 1 * rcx + 0xff]                             | ff a4 08 ff 00 00 00                |
    | jmp qword [rax + 1 * rcx - 0xff]                             | ff a4 08 01 ff ff ff                |
    | jmp qword [rax + 1 * rcx + 0x7fffffff]                       | ff a4 08 ff ff ff 7f                |
    | jmp qword [rax + 1 * rcx - 0x7fffffff]                       | ff a4 08 01 00 00 80                |
    | jmp qword [rax + 1 * rcx - 0x80000000]                       | ff a4 08 00 00 00 80                |
    | jmp qword [r10 + 0x7f]                                       | 41 ff 62 7f                         |
    | jmp qword [r10 + 0x80]                                       | 41 ff a2 80 00 00 00                |
    | jmp qword [r10 - 0x80]                                       | 41 ff 62 80                         |
    | jmp qword [r10 - 0x81]                                       | 41 ff a2 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; jmp qword [rel @prev5]      | 90 90 90 90 90 ff 25 f5 ff ff ff    |
    | .prev1: nop; jmp qword [rel @prev1]                          | 90 ff 25 f9 ff ff ff                |
    | jmp qword [rel @next1]; nop; .next1: nop                     | ff 25 01 00 00 00 90 90             |
    | jmp qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | ff 25 05 00 00 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------ | ----------------------------------- |
"""


def can_encode_jmp_addr64():
    encode(JMP_ADDR64)


JMP_REL = """
    | -------------------------------------------------- | ------------------------------ |
    | instruction                                        | encoding                        |
    | -------------------------------------------------- | ------------------------------ |
    | .prev5: nop; nop; nop; nop; nop; jmp @prev5        | 90 90 90 90 90 e9 f6 ff ff ff   |
    | .prev1: nop; jmp @prev1                            | 90 e9 fa ff ff ff               |
    | jmp @next1; nop; .next1: nop                       | e9 01 00 00 00 90 90            |
    | jmp @next5; nop; nop; nop; nop; nop; .next5: nop   | e9 05 00 00 00 90 90 90 90 90 90 |
    | -------------------------------------------------- | ------------------------------ |
"""


def can_encode_jmp_rel():
    encode(JMP_REL)
