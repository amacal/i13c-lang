from tests.encoding.core import encode, exhaust


def can_exhaust_call():
    exhaust(CALL_REG64, CALL_ADDR64, CALL_REL)


CALL_REG64 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | call rax    | ff d0    | *** | call r8     | 41 ff d0 |
    | call rcx    | ff d1    | *** | call r9     | 41 ff d1 |
    | call rdx    | ff d2    | *** | call r10    | 41 ff d2 |
    | call rbx    | ff d3    | *** | call r11    | 41 ff d3 |
    | call rsp    | ff d4    | *** | call r12    | 41 ff d4 |
    | call rbp    | ff d5    | *** | call r13    | 41 ff d5 |
    | call rsi    | ff d6    | *** | call r14    | 41 ff d6 |
    | call rdi    | ff d7    | *** | call r15    | 41 ff d7 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_call_reg64():
    encode(CALL_REG64)


CALL_ADDR64 = """
    | ------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                   | encoding                            |
    | ------------------------------------------------------------- | ----------------------------------- |
    | call qword [rax]                                              | ff 10                               |
    | call qword [rcx]                                              | ff 11                               |
    | call qword [rdx]                                              | ff 12                               |
    | call qword [rbx]                                              | ff 13                               |
    | call qword [rsp]                                              | ff 14 24                            |
    | call qword [rbp]                                              | ff 55 00                            |
    | call qword [rsi]                                              | ff 16                               |
    | call qword [rdi]                                              | ff 17                               |
    | call qword [r8]                                               | 41 ff 10                            |
    | call qword [r9]                                               | 41 ff 11                            |
    | call qword [r10]                                              | 41 ff 12                            |
    | call qword [r11]                                              | 41 ff 13                            |
    | call qword [r12]                                              | 41 ff 14 24                         |
    | call qword [r13]                                              | 41 ff 55 00                         |
    | call qword [r14]                                              | 41 ff 16                            |
    | call qword [r15]                                              | 41 ff 17                            |
    | call qword [rax + 1 * rcx]                                    | ff 14 08                            |
    | call qword [rcx + 1 * rcx]                                    | ff 14 09                            |
    | call qword [rdx + 1 * rcx]                                    | ff 14 0a                            |
    | call qword [rbx + 1 * rcx]                                    | ff 14 0b                            |
    | call qword [rsp + 1 * rcx]                                    | ff 14 0c                            |
    | call qword [rbp + 1 * rcx]                                    | ff 54 0d 00                         |
    | call qword [rsi + 1 * rcx]                                    | ff 14 0e                            |
    | call qword [rdi + 1 * rcx]                                    | ff 14 0f                            |
    | call qword [r8 + 1 * rcx]                                     | 41 ff 14 08                         |
    | call qword [r9 + 1 * rcx]                                     | 41 ff 14 09                         |
    | call qword [r10 + 1 * rcx]                                    | 41 ff 14 0a                         |
    | call qword [r11 + 1 * rcx]                                    | 41 ff 14 0b                         |
    | call qword [r12 + 1 * rcx]                                    | 41 ff 14 0c                         |
    | call qword [r13 + 1 * rcx]                                    | 41 ff 54 0d 00                      |
    | call qword [r14 + 1 * rcx]                                    | 41 ff 14 0e                         |
    | call qword [r15 + 1 * rcx]                                    | 41 ff 14 0f                         |
    | call qword [rax + 1 * rax]                                    | ff 14 00                            |
    | call qword [rax + 1 * rdx]                                    | ff 14 10                            |
    | call qword [rax + 1 * rbx]                                    | ff 14 18                            |
    | call qword [rax + 1 * rbp]                                    | ff 14 28                            |
    | call qword [rax + 1 * rsi]                                    | ff 14 30                            |
    | call qword [rax + 1 * rdi]                                    | ff 14 38                            |
    | call qword [rax + 1 * r8]                                     | 42 ff 14 00                         |
    | call qword [rax + 1 * r9]                                     | 42 ff 14 08                         |
    | call qword [rax + 1 * r10]                                    | 42 ff 14 10                         |
    | call qword [rax + 1 * r11]                                    | 42 ff 14 18                         |
    | call qword [rax + 1 * r12]                                    | 42 ff 14 20                         |
    | call qword [rax + 1 * r13]                                    | 42 ff 14 28                         |
    | call qword [rax + 1 * r14]                                    | 42 ff 14 30                         |
    | call qword [rax + 1 * r15]                                    | 42 ff 14 38                         |
    | call qword [rax + 2 * rcx]                                    | ff 14 48                            |
    | call qword [rax + 4 * rcx]                                    | ff 14 88                            |
    | call qword [rax + 8 * rcx]                                    | ff 14 c8                            |
    | call qword [r8 + 1 * r9]                                      | 43 ff 14 08                         |
    | call qword [r8 + 2 * r9]                                      | 43 ff 14 48                         |
    | call qword [r8 + 4 * r9]                                      | 43 ff 14 88                         |
    | call qword [r8 + 8 * r9]                                      | 43 ff 14 c8                         |
    | call qword [1 * rcx]                                          | ff 14 0d 00 00 00 00                |
    | call qword [2 * rcx]                                          | ff 14 4d 00 00 00 00                |
    | call qword [4 * rcx]                                          | ff 14 8d 00 00 00 00                |
    | call qword [8 * rcx]                                          | ff 14 cd 00 00 00 00                |
    | call qword [1 * r9]                                           | 42 ff 14 0d 00 00 00 00             |
    | call qword [2 * r9]                                           | 42 ff 14 4d 00 00 00 00             |
    | call qword [4 * r9]                                           | 42 ff 14 8d 00 00 00 00             |
    | call qword [8 * r9]                                           | 42 ff 14 cd 00 00 00 00             |
    | call qword [r13 + 8 * r12]                                    | 43 ff 54 e5 00                      |
    | call qword [rsp + 4 * r15]                                    | 42 ff 14 bc                         |
    | call qword [rax + 1 * rcx + 0x00]                             | ff 54 08 00                         |
    | call qword [rax + 1 * rcx - 0x00]                             | ff 54 08 00                         |
    | call qword [rax + 1 * rcx + 0x01]                             | ff 54 08 01                         |
    | call qword [rax + 1 * rcx - 0x01]                             | ff 54 08 ff                         |
    | call qword [rax + 1 * rcx + 0x00000001]                       | ff 94 08 01 00 00 00                |
    | call qword [rax + 1 * rcx - 0x00000001]                       | ff 94 08 ff ff ff ff                |
    | call qword [rax + 1 * rcx + 0x7f]                             | ff 54 08 7f                         |
    | call qword [rax + 1 * rcx - 0x7f]                             | ff 54 08 81                         |
    | call qword [rax + 1 * rcx + 0x80]                             | ff 94 08 80 00 00 00                |
    | call qword [rax + 1 * rcx - 0x80]                             | ff 54 08 80                         |
    | call qword [rax + 1 * rcx - 0x81]                             | ff 94 08 7f ff ff ff                |
    | call qword [rax + 1 * rcx + 0xff]                             | ff 94 08 ff 00 00 00                |
    | call qword [rax + 1 * rcx - 0xff]                             | ff 94 08 01 ff ff ff                |
    | call qword [rax + 1 * rcx + 0x7fffffff]                       | ff 94 08 ff ff ff 7f                |
    | call qword [rax + 1 * rcx - 0x7fffffff]                       | ff 94 08 01 00 00 80                |
    | call qword [rax + 1 * rcx - 0x80000000]                       | ff 94 08 00 00 00 80                |
    | call qword [r10 + 0x7f]                                       | 41 ff 52 7f                         |
    | call qword [r10 + 0x80]                                       | 41 ff 92 80 00 00 00                |
    | call qword [r10 - 0x80]                                       | 41 ff 52 80                         |
    | call qword [r10 - 0x81]                                       | 41 ff 92 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; call qword [rel @prev5]      | 90 90 90 90 90 ff 15 f5 ff ff ff    |
    | .prev1: nop; call qword [rel @prev1]                          | 90 ff 15 f9 ff ff ff                |
    | call qword [rel @next1]; nop; .next1: nop                     | ff 15 01 00 00 00 90 90             |
    | call qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | ff 15 05 00 00 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_call_addr64():
    encode(CALL_ADDR64)


CALL_REL = """
    | -------------------------------------------------- | -------------------------------- |
    | instruction                                        | encoding                         |
    | -------------------------------------------------- | -------------------------------- |
    | .prev5: nop; nop; nop; nop; nop; call @prev5       | 90 90 90 90 90 e8 f6 ff ff ff    |
    | .prev1: nop; call @prev1                           | 90 e8 fa ff ff ff                |
    | call @next1; nop; .next1: nop                      | e8 01 00 00 00 90 90             |
    | call @next5; nop; nop; nop; nop; nop; .next5: nop  | e8 05 00 00 00 90 90 90 90 90 90 |
    | -------------------------------------------------- | -------------------------------- |
"""


def can_encode_call_rel():
    encode(CALL_REL)
