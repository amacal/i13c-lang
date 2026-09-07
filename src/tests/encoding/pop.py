from tests.encoding.core import encode, exhaust


def can_exhaust_pop():
    exhaust(
        POP_REG16,
        POP_REG64,
        POP_ADDR16,
        POP_ADDR64,
    )


POP_REG16 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | pop ax      | 66 58    | *** | pop r8w     | 66 41 58 |
    | pop cx      | 66 59    | *** | pop r9w     | 66 41 59 |
    | pop dx      | 66 5a    | *** | pop r10w    | 66 41 5a |
    | pop bx      | 66 5b    | *** | pop r11w    | 66 41 5b |
    | pop sp      | 66 5c    | *** | pop r12w    | 66 41 5c |
    | pop bp      | 66 5d    | *** | pop r13w    | 66 41 5d |
    | pop si      | 66 5e    | *** | pop r14w    | 66 41 5e |
    | pop di      | 66 5f    | *** | pop r15w    | 66 41 5f |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_pop_reg16():
    encode(POP_REG16)


POP_REG64 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | pop rax     | 58       | *** | pop r8      | 41 58    |
    | pop rcx     | 59       | *** | pop r9      | 41 59    |
    | pop rdx     | 5a       | *** | pop r10     | 41 5a    |
    | pop rbx     | 5b       | *** | pop r11     | 41 5b    |
    | pop rsp     | 5c       | *** | pop r12     | 41 5c    |
    | pop rbp     | 5d       | *** | pop r13     | 41 5d    |
    | pop rsi     | 5e       | *** | pop r14     | 41 5e    |
    | pop rdi     | 5f       | *** | pop r15     | 41 5f    |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_pop_reg64():
    encode(POP_REG64)


POP_ADDR64 = """
    | ------------------------------------------------------------ | -------------------------------------- |
    | instruction                                                  | encoding                               |
    | ------------------------------------------------------------ | -------------------------------------- |
    | pop qword [rax]                                              | 48 8f 00                               |
    | pop qword [rcx]                                              | 48 8f 01                               |
    | pop qword [rdx]                                              | 48 8f 02                               |
    | pop qword [rbx]                                              | 48 8f 03                               |
    | pop qword [rsp]                                              | 48 8f 04 24                            |
    | pop qword [rbp]                                              | 48 8f 45 00                            |
    | pop qword [rsi]                                              | 48 8f 06                               |
    | pop qword [rdi]                                              | 48 8f 07                               |
    | pop qword [r8]                                               | 49 8f 00                               |
    | pop qword [r9]                                               | 49 8f 01                               |
    | pop qword [r10]                                              | 49 8f 02                               |
    | pop qword [r11]                                              | 49 8f 03                               |
    | pop qword [r12]                                              | 49 8f 04 24                            |
    | pop qword [r13]                                              | 49 8f 45 00                            |
    | pop qword [r14]                                              | 49 8f 06                               |
    | pop qword [r15]                                              | 49 8f 07                               |
    | pop qword [rax + 1 * rcx]                                    | 48 8f 04 08                            |
    | pop qword [rcx + 1 * rcx]                                    | 48 8f 04 09                            |
    | pop qword [rdx + 1 * rcx]                                    | 48 8f 04 0a                            |
    | pop qword [rbx + 1 * rcx]                                    | 48 8f 04 0b                            |
    | pop qword [rsp + 1 * rcx]                                    | 48 8f 04 0c                            |
    | pop qword [rbp + 1 * rcx]                                    | 48 8f 44 0d 00                         |
    | pop qword [rsi + 1 * rcx]                                    | 48 8f 04 0e                            |
    | pop qword [rdi + 1 * rcx]                                    | 48 8f 04 0f                            |
    | pop qword [r8 + 1 * rcx]                                     | 49 8f 04 08                            |
    | pop qword [r9 + 1 * rcx]                                     | 49 8f 04 09                            |
    | pop qword [r10 + 1 * rcx]                                    | 49 8f 04 0a                            |
    | pop qword [r11 + 1 * rcx]                                    | 49 8f 04 0b                            |
    | pop qword [r12 + 1 * rcx]                                    | 49 8f 04 0c                            |
    | pop qword [r13 + 1 * rcx]                                    | 49 8f 44 0d 00                         |
    | pop qword [r14 + 1 * rcx]                                    | 49 8f 04 0e                            |
    | pop qword [r15 + 1 * rcx]                                    | 49 8f 04 0f                            |
    | pop qword [rax + 1 * rax]                                    | 48 8f 04 00                            |
    | pop qword [rax + 1 * rdx]                                    | 48 8f 04 10                            |
    | pop qword [rax + 1 * rbx]                                    | 48 8f 04 18                            |
    | pop qword [rax + 1 * rbp]                                    | 48 8f 04 28                            |
    | pop qword [rax + 1 * rsi]                                    | 48 8f 04 30                            |
    | pop qword [rax + 1 * rdi]                                    | 48 8f 04 38                            |
    | pop qword [rax + 1 * r8]                                     | 4a 8f 04 00                            |
    | pop qword [rax + 1 * r9]                                     | 4a 8f 04 08                            |
    | pop qword [rax + 1 * r10]                                    | 4a 8f 04 10                            |
    | pop qword [rax + 1 * r11]                                    | 4a 8f 04 18                            |
    | pop qword [rax + 1 * r12]                                    | 4a 8f 04 20                            |
    | pop qword [rax + 1 * r13]                                    | 4a 8f 04 28                            |
    | pop qword [rax + 1 * r14]                                    | 4a 8f 04 30                            |
    | pop qword [rax + 1 * r15]                                    | 4a 8f 04 38                            |
    | pop qword [rax + 2 * rcx]                                    | 48 8f 04 48                            |
    | pop qword [rax + 4 * rcx]                                    | 48 8f 04 88                            |
    | pop qword [rax + 8 * rcx]                                    | 48 8f 04 c8                            |
    | pop qword [r8 + 1 * r9]                                      | 4b 8f 04 08                            |
    | pop qword [r8 + 2 * r9]                                      | 4b 8f 04 48                            |
    | pop qword [r8 + 4 * r9]                                      | 4b 8f 04 88                            |
    | pop qword [r8 + 8 * r9]                                      | 4b 8f 04 c8                            |
    | pop qword [1 * rcx]                                          | 48 8f 04 0d 00 00 00 00                |
    | pop qword [2 * rcx]                                          | 48 8f 04 4d 00 00 00 00                |
    | pop qword [4 * rcx]                                          | 48 8f 04 8d 00 00 00 00                |
    | pop qword [8 * rcx]                                          | 48 8f 04 cd 00 00 00 00                |
    | pop qword [1 * r9]                                           | 4a 8f 04 0d 00 00 00 00                |
    | pop qword [2 * r9]                                           | 4a 8f 04 4d 00 00 00 00                |
    | pop qword [4 * r9]                                           | 4a 8f 04 8d 00 00 00 00                |
    | pop qword [8 * r9]                                           | 4a 8f 04 cd 00 00 00 00                |
    | pop qword [r13 + 8 * r12]                                    | 4b 8f 44 e5 00                         |
    | pop qword [rsp + 4 * r15]                                    | 4a 8f 04 bc                            |
    | pop qword [rax + 1 * rcx + 0x00]                             | 48 8f 44 08 00                         |
    | pop qword [rax + 1 * rcx - 0x00]                             | 48 8f 44 08 00                         |
    | pop qword [rax + 1 * rcx + 0x01]                             | 48 8f 44 08 01                         |
    | pop qword [rax + 1 * rcx - 0x01]                             | 48 8f 44 08 ff                         |
    | pop qword [rax + 1 * rcx + 0x00000001]                       | 48 8f 84 08 01 00 00 00                |
    | pop qword [rax + 1 * rcx - 0x00000001]                       | 48 8f 84 08 ff ff ff ff                |
    | pop qword [rax + 1 * rcx + 0x7f]                             | 48 8f 44 08 7f                         |
    | pop qword [rax + 1 * rcx - 0x7f]                             | 48 8f 44 08 81                         |
    | pop qword [rax + 1 * rcx + 0x80]                             | 48 8f 84 08 80 00 00 00                |
    | pop qword [rax + 1 * rcx - 0x80]                             | 48 8f 44 08 80                         |
    | pop qword [rax + 1 * rcx - 0x81]                             | 48 8f 84 08 7f ff ff ff                |
    | pop qword [rax + 1 * rcx + 0xff]                             | 48 8f 84 08 ff 00 00 00                |
    | pop qword [rax + 1 * rcx - 0xff]                             | 48 8f 84 08 01 ff ff ff                |
    | pop qword [rax + 1 * rcx + 0x7fffffff]                       | 48 8f 84 08 ff ff ff 7f                |
    | pop qword [rax + 1 * rcx - 0x7fffffff]                       | 48 8f 84 08 01 00 00 80                |
    | pop qword [rax + 1 * rcx - 0x80000000]                       | 48 8f 84 08 00 00 00 80                |
    | pop qword [r10 + 0x7f]                                       | 49 8f 42 7f                            |
    | pop qword [r10 + 0x80]                                       | 49 8f 82 80 00 00 00                   |
    | pop qword [r10 - 0x80]                                       | 49 8f 42 80                            |
    | pop qword [r10 - 0x81]                                       | 49 8f 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; pop qword [rel @prev5]      | 90 90 90 90 90 48 8f 05 f4 ff ff ff    |
    | .prev1: nop; pop qword [rel @prev1]                          | 90 48 8f 05 f8 ff ff ff                |
    | pop qword [rel @next1]; nop; .next1: nop                     | 48 8f 05 01 00 00 00 90 90             |
    | pop qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 8f 05 05 00 00 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------ | -------------------------------------- |
"""


def can_encode_pop_addr64():
    encode(POP_ADDR64)


POP_ADDR16 = """
    | ----------------------------------------------------------- | -------------------------------------- |
    | instruction                                                 | encoding                               |
    | ----------------------------------------------------------- | -------------------------------------- |
    | pop word [rax]                                              | 66 8f 00                               |
    | pop word [rcx]                                              | 66 8f 01                               |
    | pop word [rdx]                                              | 66 8f 02                               |
    | pop word [rbx]                                              | 66 8f 03                               |
    | pop word [rsp]                                              | 66 8f 04 24                            |
    | pop word [rbp]                                              | 66 8f 45 00                            |
    | pop word [rsi]                                              | 66 8f 06                               |
    | pop word [rdi]                                              | 66 8f 07                               |
    | pop word [r8]                                               | 66 41 8f 00                            |
    | pop word [r9]                                               | 66 41 8f 01                            |
    | pop word [r10]                                              | 66 41 8f 02                            |
    | pop word [r11]                                              | 66 41 8f 03                            |
    | pop word [r12]                                              | 66 41 8f 04 24                         |
    | pop word [r13]                                              | 66 41 8f 45 00                         |
    | pop word [r14]                                              | 66 41 8f 06                            |
    | pop word [r15]                                              | 66 41 8f 07                            |
    | pop word [rax + 1 * rcx]                                    | 66 8f 04 08                            |
    | pop word [rcx + 1 * rcx]                                    | 66 8f 04 09                            |
    | pop word [rdx + 1 * rcx]                                    | 66 8f 04 0a                            |
    | pop word [rbx + 1 * rcx]                                    | 66 8f 04 0b                            |
    | pop word [rsp + 1 * rcx]                                    | 66 8f 04 0c                            |
    | pop word [rbp + 1 * rcx]                                    | 66 8f 44 0d 00                         |
    | pop word [rsi + 1 * rcx]                                    | 66 8f 04 0e                            |
    | pop word [rdi + 1 * rcx]                                    | 66 8f 04 0f                            |
    | pop word [r8 + 1 * rcx]                                     | 66 41 8f 04 08                         |
    | pop word [r9 + 1 * rcx]                                     | 66 41 8f 04 09                         |
    | pop word [r10 + 1 * rcx]                                    | 66 41 8f 04 0a                         |
    | pop word [r11 + 1 * rcx]                                    | 66 41 8f 04 0b                         |
    | pop word [r12 + 1 * rcx]                                    | 66 41 8f 04 0c                         |
    | pop word [r13 + 1 * rcx]                                    | 66 41 8f 44 0d 00                      |
    | pop word [r14 + 1 * rcx]                                    | 66 41 8f 04 0e                         |
    | pop word [r15 + 1 * rcx]                                    | 66 41 8f 04 0f                         |
    | pop word [rax + 1 * rax]                                    | 66 8f 04 00                            |
    | pop word [rax + 1 * rdx]                                    | 66 8f 04 10                            |
    | pop word [rax + 1 * rbx]                                    | 66 8f 04 18                            |
    | pop word [rax + 1 * rbp]                                    | 66 8f 04 28                            |
    | pop word [rax + 1 * rsi]                                    | 66 8f 04 30                            |
    | pop word [rax + 1 * rdi]                                    | 66 8f 04 38                            |
    | pop word [rax + 1 * r8]                                     | 66 42 8f 04 00                         |
    | pop word [rax + 1 * r9]                                     | 66 42 8f 04 08                         |
    | pop word [rax + 1 * r10]                                    | 66 42 8f 04 10                         |
    | pop word [rax + 1 * r11]                                    | 66 42 8f 04 18                         |
    | pop word [rax + 1 * r12]                                    | 66 42 8f 04 20                         |
    | pop word [rax + 1 * r13]                                    | 66 42 8f 04 28                         |
    | pop word [rax + 1 * r14]                                    | 66 42 8f 04 30                         |
    | pop word [rax + 1 * r15]                                    | 66 42 8f 04 38                         |
    | pop word [rax + 2 * rcx]                                    | 66 8f 04 48                            |
    | pop word [rax + 4 * rcx]                                    | 66 8f 04 88                            |
    | pop word [rax + 8 * rcx]                                    | 66 8f 04 c8                            |
    | pop word [r8 + 1 * r9]                                      | 66 43 8f 04 08                         |
    | pop word [r8 + 2 * r9]                                      | 66 43 8f 04 48                         |
    | pop word [r8 + 4 * r9]                                      | 66 43 8f 04 88                         |
    | pop word [r8 + 8 * r9]                                      | 66 43 8f 04 c8                         |
    | pop word [1 * rcx]                                          | 66 8f 04 0d 00 00 00 00                |
    | pop word [2 * rcx]                                          | 66 8f 04 4d 00 00 00 00                |
    | pop word [4 * rcx]                                          | 66 8f 04 8d 00 00 00 00                |
    | pop word [8 * rcx]                                          | 66 8f 04 cd 00 00 00 00                |
    | pop word [1 * r9]                                           | 66 42 8f 04 0d 00 00 00 00             |
    | pop word [2 * r9]                                           | 66 42 8f 04 4d 00 00 00 00             |
    | pop word [4 * r9]                                           | 66 42 8f 04 8d 00 00 00 00             |
    | pop word [8 * r9]                                           | 66 42 8f 04 cd 00 00 00 00             |
    | pop word [r13 + 8 * r12]                                    | 66 43 8f 44 e5 00                      |
    | pop word [rsp + 4 * r15]                                    | 66 42 8f 04 bc                         |
    | pop word [rax + 1 * rcx + 0x00]                             | 66 8f 44 08 00                         |
    | pop word [rax + 1 * rcx - 0x00]                             | 66 8f 44 08 00                         |
    | pop word [rax + 1 * rcx + 0x01]                             | 66 8f 44 08 01                         |
    | pop word [rax + 1 * rcx - 0x01]                             | 66 8f 44 08 ff                         |
    | pop word [rax + 1 * rcx + 0x00000001]                       | 66 8f 84 08 01 00 00 00                |
    | pop word [rax + 1 * rcx - 0x00000001]                       | 66 8f 84 08 ff ff ff ff                |
    | pop word [rax + 1 * rcx + 0x7f]                             | 66 8f 44 08 7f                         |
    | pop word [rax + 1 * rcx - 0x7f]                             | 66 8f 44 08 81                         |
    | pop word [rax + 1 * rcx + 0x80]                             | 66 8f 84 08 80 00 00 00                |
    | pop word [rax + 1 * rcx - 0x80]                             | 66 8f 44 08 80                         |
    | pop word [rax + 1 * rcx - 0x81]                             | 66 8f 84 08 7f ff ff ff                |
    | pop word [rax + 1 * rcx + 0xff]                             | 66 8f 84 08 ff 00 00 00                |
    | pop word [rax + 1 * rcx - 0xff]                             | 66 8f 84 08 01 ff ff ff                |
    | pop word [rax + 1 * rcx + 0x7fffffff]                       | 66 8f 84 08 ff ff ff 7f                |
    | pop word [rax + 1 * rcx - 0x7fffffff]                       | 66 8f 84 08 01 00 00 80                |
    | pop word [rax + 1 * rcx - 0x80000000]                       | 66 8f 84 08 00 00 00 80                |
    | pop word [r10 + 0x7f]                                       | 66 41 8f 42 7f                         |
    | pop word [r10 + 0x80]                                       | 66 41 8f 82 80 00 00 00                |
    | pop word [r10 - 0x80]                                       | 66 41 8f 42 80                         |
    | pop word [r10 - 0x81]                                       | 66 41 8f 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; pop word [rel @prev5]      | 90 90 90 90 90 66 8f 05 f4 ff ff ff    |
    | .prev1: nop; pop word [rel @prev1]                          | 90 66 8f 05 f8 ff ff ff                |
    | pop word [rel @next1]; nop; .next1: nop                     | 66 8f 05 01 00 00 00 90 90             |
    | pop word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 8f 05 05 00 00 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_pop_addr16():
    encode(POP_ADDR16)
