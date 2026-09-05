from tests.encoding.core import encode, exhaust


def can_exhaust_push():
    exhaust(
        PUSH_IMM8,
        PUSH_IMM16,
        PUSH_IMM32,
        PUSH_REG16,
        PUSH_REG64,
        PUSH_ADDR16,
        PUSH_ADDR64,
    )


PUSH_IMM8 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | push 0x00   | 6a 00    | *** | push 0x01   | 6a 01    |
    | push 0x7f   | 6a 7f    | *** | push 0x80   | 6a 80    |
    | push 0xff   | 6a ff    | *** | push 0xff   | 6a ff    |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_push_imm8():
    encode(PUSH_IMM8)


PUSH_IMM16 = """
    | ----------- | ----------- | --- | ----------- | ----------- |
    | instruction | encoding    | *** | instruction | encoding    |
    | ----------- | ----------- | --- | ----------- | ----------- |
    | push 0x0000 | 66 68 00 00 | *** | push 0x0001 | 66 68 01 00 |
    | push 0x007f | 66 68 7f 00 | *** | push 0x0080 | 66 68 80 00 |
    | push 0x00ff | 66 68 ff 00 | *** | push 0x0100 | 66 68 00 01 |
    | push 0x7fff | 66 68 ff 7f | *** | push 0x8000 | 66 68 00 80 |
    | push 0xffff | 66 68 ff ff | *** | push 0xffff | 66 68 ff ff |
    | ----------- | ----------- | --- | ----------- | ----------- |
"""


def can_encode_push_imm16():
    encode(PUSH_IMM16)


PUSH_IMM32 = """
    | --------------- | -------------- | --- | --------------- | -------------- |
    | instruction     | encoding       | *** | instruction     | encoding       |
    | --------------- | -------------- | --- | --------------- | -------------- |
    | push 0x00000000 | 68 00 00 00 00 | *** | push 0x00000001 | 68 01 00 00 00 |
    | push 0x0000007f | 68 7f 00 00 00 | *** | push 0x00000080 | 68 80 00 00 00 |
    | push 0x000000ff | 68 ff 00 00 00 | *** | push 0x00000100 | 68 00 01 00 00 |
    | push 0x00007fff | 68 ff 7f 00 00 | *** | push 0x00008000 | 68 00 80 00 00 |
    | push 0x0000ffff | 68 ff ff 00 00 | *** | push 0x00010000 | 68 00 00 01 00 |
    | push 0x7fffffff | 68 ff ff ff 7f | *** | push 0x80000000 | 68 00 00 00 80 |
    | push 0xffffffff | 68 ff ff ff ff | *** | push 0xffffffff | 68 ff ff ff ff |
    | --------------- | -------------- | --- | --------------- | -------------- |
"""


def can_encode_push_imm32():
    encode(PUSH_IMM32)


PUSH_REG16 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | push ax     | 66 50    | *** | push r8w    | 66 41 50 |
    | push cx     | 66 51    | *** | push r9w    | 66 41 51 |
    | push dx     | 66 52    | *** | push r10w   | 66 41 52 |
    | push bx     | 66 53    | *** | push r11w   | 66 41 53 |
    | push sp     | 66 54    | *** | push r12w   | 66 41 54 |
    | push bp     | 66 55    | *** | push r13w   | 66 41 55 |
    | push si     | 66 56    | *** | push r14w   | 66 41 56 |
    | push di     | 66 57    | *** | push r15w   | 66 41 57 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_push_reg16():
    encode(PUSH_REG16)


PUSH_REG64 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | push rax    | 50       | *** | push r8     | 41 50    |
    | push rcx    | 51       | *** | push r9     | 41 51    |
    | push rdx    | 52       | *** | push r10    | 41 52    |
    | push rbx    | 53       | *** | push r11    | 41 53    |
    | push rsp    | 54       | *** | push r12    | 41 54    |
    | push rbp    | 55       | *** | push r13    | 41 55    |
    | push rsi    | 56       | *** | push r14    | 41 56    |
    | push rdi    | 57       | *** | push r15    | 41 57    |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_push_reg64():
    encode(PUSH_REG64)


PUSH_ADDR64 = """
    | --------------------------------------- | ----------------------- |
    | instruction                             | encoding                |
    | --------------------------------------- | ----------------------- |
    | push qword [rax]                        | 48 ff 30                |
    | push qword [rcx]                        | 48 ff 31                |
    | push qword [rdx]                        | 48 ff 32                |
    | push qword [rbx]                        | 48 ff 33                |
    | push qword [rsp]                        | 48 ff 34 24             |
    | push qword [rbp]                        | 48 ff 75 00             |
    | push qword [rsi]                        | 48 ff 36                |
    | push qword [rdi]                        | 48 ff 37                |
    | push qword [r8]                         | 49 ff 30                |
    | push qword [r9]                         | 49 ff 31                |
    | push qword [r10]                        | 49 ff 32                |
    | push qword [r11]                        | 49 ff 33                |
    | push qword [r12]                        | 49 ff 34 24             |
    | push qword [r13]                        | 49 ff 75 00             |
    | push qword [r14]                        | 49 ff 36                |
    | push qword [r15]                        | 49 ff 37                |
    | push qword [rax + 1 * rcx]              | 48 ff 34 08             |
    | push qword [rcx + 1 * rcx]              | 48 ff 34 09             |
    | push qword [rdx + 1 * rcx]              | 48 ff 34 0a             |
    | push qword [rbx + 1 * rcx]              | 48 ff 34 0b             |
    | push qword [rsp + 1 * rcx]              | 48 ff 34 0c             |
    | push qword [rbp + 1 * rcx]              | 48 ff 74 0d 00          |
    | push qword [rsi + 1 * rcx]              | 48 ff 34 0e             |
    | push qword [rdi + 1 * rcx]              | 48 ff 34 0f             |
    | push qword [r8 + 1 * rcx]               | 49 ff 34 08             |
    | push qword [r9 + 1 * rcx]               | 49 ff 34 09             |
    | push qword [r10 + 1 * rcx]              | 49 ff 34 0a             |
    | push qword [r11 + 1 * rcx]              | 49 ff 34 0b             |
    | push qword [r12 + 1 * rcx]              | 49 ff 34 0c             |
    | push qword [r13 + 1 * rcx]              | 49 ff 74 0d 00          |
    | push qword [r14 + 1 * rcx]              | 49 ff 34 0e             |
    | push qword [r15 + 1 * rcx]              | 49 ff 34 0f             |
    | push qword [rax + 1 * rax]              | 48 ff 34 00             |
    | push qword [rax + 1 * rdx]              | 48 ff 34 10             |
    | push qword [rax + 1 * rbx]              | 48 ff 34 18             |
    | push qword [rax + 1 * rbp]              | 48 ff 34 28             |
    | push qword [rax + 1 * rsi]              | 48 ff 34 30             |
    | push qword [rax + 1 * rdi]              | 48 ff 34 38             |
    | push qword [rax + 1 * r8]               | 4a ff 34 00             |
    | push qword [rax + 1 * r9]               | 4a ff 34 08             |
    | push qword [rax + 1 * r10]              | 4a ff 34 10             |
    | push qword [rax + 1 * r11]              | 4a ff 34 18             |
    | push qword [rax + 1 * r12]              | 4a ff 34 20             |
    | push qword [rax + 1 * r13]              | 4a ff 34 28             |
    | push qword [rax + 1 * r14]              | 4a ff 34 30             |
    | push qword [rax + 1 * r15]              | 4a ff 34 38             |
    | push qword [rax + 2 * rcx]              | 48 ff 34 48             |
    | push qword [rax + 4 * rcx]              | 48 ff 34 88             |
    | push qword [rax + 8 * rcx]              | 48 ff 34 c8             |
    | push qword [r8 + 1 * r9]                | 4b ff 34 08             |
    | push qword [r8 + 2 * r9]                | 4b ff 34 48             |
    | push qword [r8 + 4 * r9]                | 4b ff 34 88             |
    | push qword [r8 + 8 * r9]                | 4b ff 34 c8             |
    | push qword [1 * rcx]                    | 48 ff 34 0d 00 00 00 00 |
    | push qword [2 * rcx]                    | 48 ff 34 4d 00 00 00 00 |
    | push qword [4 * rcx]                    | 48 ff 34 8d 00 00 00 00 |
    | push qword [8 * rcx]                    | 48 ff 34 cd 00 00 00 00 |
    | push qword [1 * r9]                     | 4a ff 34 0d 00 00 00 00 |
    | push qword [2 * r9]                     | 4a ff 34 4d 00 00 00 00 |
    | push qword [4 * r9]                     | 4a ff 34 8d 00 00 00 00 |
    | push qword [8 * r9]                     | 4a ff 34 cd 00 00 00 00 |
    | push qword [r13 + 8 * r12]              | 4b ff 74 e5 00          |
    | push qword [rsp + 4 * r15]              | 4a ff 34 bc             |
    | push qword [rax + 1 * rcx + 0x00]       | 48 ff 74 08 00          |
    | push qword [rax + 1 * rcx - 0x00]       | 48 ff 74 08 00          |
    | push qword [rax + 1 * rcx + 0x01]       | 48 ff 74 08 01          |
    | push qword [rax + 1 * rcx - 0x01]       | 48 ff 74 08 ff          |
    | push qword [rax + 1 * rcx + 0x00000001] | 48 ff b4 08 01 00 00 00 |
    | push qword [rax + 1 * rcx - 0x00000001] | 48 ff b4 08 ff ff ff ff |
    | push qword [rax + 1 * rcx + 0x7f]       | 48 ff 74 08 7f          |
    | push qword [rax + 1 * rcx - 0x7f]       | 48 ff 74 08 81          |
    | push qword [rax + 1 * rcx + 0x80]       | 48 ff b4 08 80 00 00 00 |
    | push qword [rax + 1 * rcx - 0x80]       | 48 ff 74 08 80          |
    | push qword [rax + 1 * rcx - 0x81]       | 48 ff b4 08 7f ff ff ff |
    | push qword [rax + 1 * rcx + 0xff]       | 48 ff b4 08 ff 00 00 00 |
    | push qword [rax + 1 * rcx - 0xff]       | 48 ff b4 08 01 ff ff ff |
    | push qword [rax + 1 * rcx + 0x7fffffff] | 48 ff b4 08 ff ff ff 7f |
    | push qword [rax + 1 * rcx - 0x7fffffff] | 48 ff b4 08 01 00 00 80 |
    | push qword [rax + 1 * rcx - 0x80000000] | 48 ff b4 08 00 00 00 80 |
    | push qword [r10 + 0x7f]                 | 49 ff 72 7f             |
    | push qword [r10 + 0x80]                 | 49 ff b2 80 00 00 00    |
    | push qword [r10 - 0x80]                 | 49 ff 72 80             |
    | push qword [r10 - 0x81]                 | 49 ff b2 7f ff ff ff    |
    | --------------------------------------- | ----------------------- |
"""


def can_encode_push_addr64():
    encode(PUSH_ADDR64)


PUSH_ADDR16 = """
    | -------------------------------------- | -------------------------- |
    | instruction                            | encoding                   |
    | -------------------------------------- | -------------------------- |
    | push word [rax]                        | 66 ff 30                   |
    | push word [rcx]                        | 66 ff 31                   |
    | push word [rdx]                        | 66 ff 32                   |
    | push word [rbx]                        | 66 ff 33                   |
    | push word [rsp]                        | 66 ff 34 24                |
    | push word [rbp]                        | 66 ff 75 00                |
    | push word [rsi]                        | 66 ff 36                   |
    | push word [rdi]                        | 66 ff 37                   |
    | push word [r8]                         | 66 41 ff 30                |
    | push word [r9]                         | 66 41 ff 31                |
    | push word [r10]                        | 66 41 ff 32                |
    | push word [r11]                        | 66 41 ff 33                |
    | push word [r12]                        | 66 41 ff 34 24             |
    | push word [r13]                        | 66 41 ff 75 00             |
    | push word [r14]                        | 66 41 ff 36                |
    | push word [r15]                        | 66 41 ff 37                |
    | push word [rax + 1 * rcx]              | 66 ff 34 08                |
    | push word [rcx + 1 * rcx]              | 66 ff 34 09                |
    | push word [rdx + 1 * rcx]              | 66 ff 34 0a                |
    | push word [rbx + 1 * rcx]              | 66 ff 34 0b                |
    | push word [rsp + 1 * rcx]              | 66 ff 34 0c                |
    | push word [rbp + 1 * rcx]              | 66 ff 74 0d 00             |
    | push word [rsi + 1 * rcx]              | 66 ff 34 0e                |
    | push word [rdi + 1 * rcx]              | 66 ff 34 0f                |
    | push word [r8 + 1 * rcx]               | 66 41 ff 34 08             |
    | push word [r9 + 1 * rcx]               | 66 41 ff 34 09             |
    | push word [r10 + 1 * rcx]              | 66 41 ff 34 0a             |
    | push word [r11 + 1 * rcx]              | 66 41 ff 34 0b             |
    | push word [r12 + 1 * rcx]              | 66 41 ff 34 0c             |
    | push word [r13 + 1 * rcx]              | 66 41 ff 74 0d 00          |
    | push word [r14 + 1 * rcx]              | 66 41 ff 34 0e             |
    | push word [r15 + 1 * rcx]              | 66 41 ff 34 0f             |
    | push word [rax + 1 * rax]              | 66 ff 34 00                |
    | push word [rax + 1 * rdx]              | 66 ff 34 10                |
    | push word [rax + 1 * rbx]              | 66 ff 34 18                |
    | push word [rax + 1 * rbp]              | 66 ff 34 28                |
    | push word [rax + 1 * rsi]              | 66 ff 34 30                |
    | push word [rax + 1 * rdi]              | 66 ff 34 38                |
    | push word [rax + 1 * r8]               | 66 42 ff 34 00             |
    | push word [rax + 1 * r9]               | 66 42 ff 34 08             |
    | push word [rax + 1 * r10]              | 66 42 ff 34 10             |
    | push word [rax + 1 * r11]              | 66 42 ff 34 18             |
    | push word [rax + 1 * r12]              | 66 42 ff 34 20             |
    | push word [rax + 1 * r13]              | 66 42 ff 34 28             |
    | push word [rax + 1 * r14]              | 66 42 ff 34 30             |
    | push word [rax + 1 * r15]              | 66 42 ff 34 38             |
    | push word [rax + 2 * rcx]              | 66 ff 34 48                |
    | push word [rax + 4 * rcx]              | 66 ff 34 88                |
    | push word [rax + 8 * rcx]              | 66 ff 34 c8                |
    | push word [r8 + 1 * r9]                | 66 43 ff 34 08             |
    | push word [r8 + 2 * r9]                | 66 43 ff 34 48             |
    | push word [r8 + 4 * r9]                | 66 43 ff 34 88             |
    | push word [r8 + 8 * r9]                | 66 43 ff 34 c8             |
    | push word [1 * rcx]                    | 66 ff 34 0d 00 00 00 00    |
    | push word [2 * rcx]                    | 66 ff 34 4d 00 00 00 00    |
    | push word [4 * rcx]                    | 66 ff 34 8d 00 00 00 00    |
    | push word [8 * rcx]                    | 66 ff 34 cd 00 00 00 00    |
    | push word [1 * r9]                     | 66 42 ff 34 0d 00 00 00 00 |
    | push word [2 * r9]                     | 66 42 ff 34 4d 00 00 00 00 |
    | push word [4 * r9]                     | 66 42 ff 34 8d 00 00 00 00 |
    | push word [8 * r9]                     | 66 42 ff 34 cd 00 00 00 00 |
    | push word [r13 + 8 * r12]              | 66 43 ff 74 e5 00          |
    | push word [rsp + 4 * r15]              | 66 42 ff 34 bc             |
    | push word [rax + 1 * rcx + 0x00]       | 66 ff 74 08 00             |
    | push word [rax + 1 * rcx - 0x00]       | 66 ff 74 08 00             |
    | push word [rax + 1 * rcx + 0x01]       | 66 ff 74 08 01             |
    | push word [rax + 1 * rcx - 0x01]       | 66 ff 74 08 ff             |
    | push word [rax + 1 * rcx + 0x00000001] | 66 ff b4 08 01 00 00 00    |
    | push word [rax + 1 * rcx - 0x00000001] | 66 ff b4 08 ff ff ff ff    |
    | push word [rax + 1 * rcx + 0x7f]       | 66 ff 74 08 7f             |
    | push word [rax + 1 * rcx - 0x7f]       | 66 ff 74 08 81             |
    | push word [rax + 1 * rcx + 0x80]       | 66 ff b4 08 80 00 00 00    |
    | push word [rax + 1 * rcx - 0x80]       | 66 ff 74 08 80             |
    | push word [rax + 1 * rcx - 0x81]       | 66 ff b4 08 7f ff ff ff    |
    | push word [rax + 1 * rcx + 0xff]       | 66 ff b4 08 ff 00 00 00    |
    | push word [rax + 1 * rcx - 0xff]       | 66 ff b4 08 01 ff ff ff    |
    | push word [rax + 1 * rcx + 0x7fffffff] | 66 ff b4 08 ff ff ff 7f    |
    | push word [rax + 1 * rcx - 0x7fffffff] | 66 ff b4 08 01 00 00 80    |
    | push word [rax + 1 * rcx - 0x80000000] | 66 ff b4 08 00 00 00 80    |
    | push word [r10 + 0x7f]                 | 66 41 ff 72 7f             |
    | push word [r10 + 0x80]                 | 66 41 ff b2 80 00 00 00    |
    | push word [r10 - 0x80]                 | 66 41 ff 72 80             |
    | push word [r10 - 0x81]                 | 66 41 ff b2 7f ff ff ff    |
    | -------------------------------------- | -------------------------- |
"""


def can_encode_push_addr16():
    encode(PUSH_ADDR16)
