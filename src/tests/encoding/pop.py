from tests.encoding.core import encode, exhaust


def can_exhaust_pop():
    exhaust(
        POP_REG16,
        POP_REG64,
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
    | -------------------------------- | ----------------------- |
    | instruction                      | encoding                |
    | -------------------------------- | ----------------------- |
    | pop [rax]                        | 48 8f 00                |
    | pop [rcx]                        | 48 8f 01                |
    | pop [rdx]                        | 48 8f 02                |
    | pop [rbx]                        | 48 8f 03                |
    | pop [rsp]                        | 48 8f 04 24             |
    | pop [rbp]                        | 48 8f 45 00             |
    | pop [rsi]                        | 48 8f 06                |
    | pop [rdi]                        | 48 8f 07                |
    | pop [r8]                         | 49 8f 00                |
    | pop [r9]                         | 49 8f 01                |
    | pop [r10]                        | 49 8f 02                |
    | pop [r11]                        | 49 8f 03                |
    | pop [r12]                        | 49 8f 04 24             |
    | pop [r13]                        | 49 8f 45 00             |
    | pop [r14]                        | 49 8f 06                |
    | pop [r15]                        | 49 8f 07                |
    | pop [rax + 1 * rcx]              | 48 8f 04 08             |
    | pop [rcx + 1 * rcx]              | 48 8f 04 09             |
    | pop [rdx + 1 * rcx]              | 48 8f 04 0a             |
    | pop [rbx + 1 * rcx]              | 48 8f 04 0b             |
    | pop [rsp + 1 * rcx]              | 48 8f 04 0c             |
    | pop [rbp + 1 * rcx]              | 48 8f 44 0d 00          |
    | pop [rsi + 1 * rcx]              | 48 8f 04 0e             |
    | pop [rdi + 1 * rcx]              | 48 8f 04 0f             |
    | pop [r8 + 1 * rcx]               | 49 8f 04 08             |
    | pop [r9 + 1 * rcx]               | 49 8f 04 09             |
    | pop [r10 + 1 * rcx]              | 49 8f 04 0a             |
    | pop [r11 + 1 * rcx]              | 49 8f 04 0b             |
    | pop [r12 + 1 * rcx]              | 49 8f 04 0c             |
    | pop [r13 + 1 * rcx]              | 49 8f 44 0d 00          |
    | pop [r14 + 1 * rcx]              | 49 8f 04 0e             |
    | pop [r15 + 1 * rcx]              | 49 8f 04 0f             |
    | pop [rax + 1 * rax]              | 48 8f 04 00             |
    | pop [rax + 1 * rdx]              | 48 8f 04 10             |
    | pop [rax + 1 * rbx]              | 48 8f 04 18             |
    | pop [rax + 1 * rbp]              | 48 8f 04 28             |
    | pop [rax + 1 * rsi]              | 48 8f 04 30             |
    | pop [rax + 1 * rdi]              | 48 8f 04 38             |
    | pop [rax + 1 * r8]               | 4a 8f 04 00             |
    | pop [rax + 1 * r9]               | 4a 8f 04 08             |
    | pop [rax + 1 * r10]              | 4a 8f 04 10             |
    | pop [rax + 1 * r11]              | 4a 8f 04 18             |
    | pop [rax + 1 * r12]              | 4a 8f 04 20             |
    | pop [rax + 1 * r13]              | 4a 8f 04 28             |
    | pop [rax + 1 * r14]              | 4a 8f 04 30             |
    | pop [rax + 1 * r15]              | 4a 8f 04 38             |
    | pop [rax + 2 * rcx]              | 48 8f 04 48             |
    | pop [rax + 4 * rcx]              | 48 8f 04 88             |
    | pop [rax + 8 * rcx]              | 48 8f 04 c8             |
    | pop [r8 + 1 * r9]                | 4b 8f 04 08             |
    | pop [r8 + 2 * r9]                | 4b 8f 04 48             |
    | pop [r8 + 4 * r9]                | 4b 8f 04 88             |
    | pop [r8 + 8 * r9]                | 4b 8f 04 c8             |
    | pop [1 * rcx]                    | 48 8f 04 0d 00 00 00 00 |
    | pop [2 * rcx]                    | 48 8f 04 4d 00 00 00 00 |
    | pop [4 * rcx]                    | 48 8f 04 8d 00 00 00 00 |
    | pop [8 * rcx]                    | 48 8f 04 cd 00 00 00 00 |
    | pop [1 * r9]                     | 4a 8f 04 0d 00 00 00 00 |
    | pop [2 * r9]                     | 4a 8f 04 4d 00 00 00 00 |
    | pop [4 * r9]                     | 4a 8f 04 8d 00 00 00 00 |
    | pop [8 * r9]                     | 4a 8f 04 cd 00 00 00 00 |
    | pop [r13 + 8 * r12]              | 4b 8f 44 e5 00          |
    | pop [rsp + 4 * r15]              | 4a 8f 04 bc             |
    | pop [rax + 1 * rcx + 0x00]       | 48 8f 44 08 00          |
    | pop [rax + 1 * rcx - 0x00]       | 48 8f 44 08 00          |
    | pop [rax + 1 * rcx + 0x0000]     | 48 8f 84 08 00 00 00 00 |
    | pop [rax + 1 * rcx - 0x0000]     | 48 8f 84 08 00 00 00 00 |
    | pop [rax + 1 * rcx + 0x01]       | 48 8f 44 08 01          |
    | pop [rax + 1 * rcx - 0x01]       | 48 8f 44 08 ff          |
    | pop [rax + 1 * rcx + 0x0001]     | 48 8f 84 08 01 00 00 00 |
    | pop [rax + 1 * rcx - 0x0001]     | 48 8f 84 08 ff ff ff ff |
    | pop [rax + 1 * rcx + 0x00000001] | 48 8f 84 08 01 00 00 00 |
    | pop [rax + 1 * rcx - 0x00000001] | 48 8f 84 08 ff ff ff ff |
    | pop [rax + 1 * rcx + 0x7f]       | 48 8f 44 08 7f          |
    | pop [rax + 1 * rcx - 0x7f]       | 48 8f 44 08 81          |
    | pop [rax + 1 * rcx + 0x80]       | 48 8f 84 08 80 00 00 00 |
    | pop [rax + 1 * rcx - 0x80]       | 48 8f 44 08 80          |
    | pop [rax + 1 * rcx - 0x81]       | 48 8f 84 08 7f ff ff ff |
    | pop [rax + 1 * rcx + 0xff]       | 48 8f 84 08 ff 00 00 00 |
    | pop [rax + 1 * rcx - 0xff]       | 48 8f 84 08 01 ff ff ff |
    | pop [rax + 1 * rcx + 0x7fff]     | 48 8f 84 08 ff 7f 00 00 |
    | pop [rax + 1 * rcx - 0x7fff]     | 48 8f 84 08 01 80 ff ff |
    | pop [rax + 1 * rcx + 0x8000]     | 48 8f 84 08 00 80 00 00 |
    | pop [rax + 1 * rcx - 0x8000]     | 48 8f 84 08 00 80 ff ff |
    | pop [rax + 1 * rcx + 0xffff]     | 48 8f 84 08 ff ff 00 00 |
    | pop [rax + 1 * rcx - 0xffff]     | 48 8f 84 08 01 00 ff ff |
    | pop [rax + 1 * rcx + 0x7fffffff] | 48 8f 84 08 ff ff ff 7f |
    | pop [rax + 1 * rcx - 0x7fffffff] | 48 8f 84 08 01 00 00 80 |
    | pop [rax + 1 * rcx - 0x80000000] | 48 8f 84 08 00 00 00 80 |
    | pop [r10 + 0x7f]                 | 49 8f 42 7f             |
    | pop [r10 + 0x80]                 | 49 8f 82 80 00 00 00    |
    | pop [r10 - 0x80]                 | 49 8f 42 80             |
    | pop [r10 - 0x81]                 | 49 8f 82 7f ff ff ff    |
    | -------------------------------- | ----------------------- |
"""


def can_encode_pop_addr64():
    encode(POP_ADDR64)
