from tests.encoding.core import encode, exhaust


def can_exhaust_push():
    exhaust(
        PUSH_IMM8,
        PUSH_IMM16,
        PUSH_IMM32,
        PUSH_REG16,
        PUSH_REG64,
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
    | --------------------------------- | ----------------------- |
    | instruction                       | encoding                |
    | --------------------------------- | ----------------------- |
    | push [rax]                        | 48 ff 30                |
    | push [rcx]                        | 48 ff 31                |
    | push [rdx]                        | 48 ff 32                |
    | push [rbx]                        | 48 ff 33                |
    | push [rsp]                        | 48 ff 34 24             |
    | push [rbp]                        | 48 ff 75 00             |
    | push [rsi]                        | 48 ff 36                |
    | push [rdi]                        | 48 ff 37                |
    | push [r8]                         | 49 ff 30                |
    | push [r9]                         | 49 ff 31                |
    | push [r10]                        | 49 ff 32                |
    | push [r11]                        | 49 ff 33                |
    | push [r12]                        | 49 ff 34 24             |
    | push [r13]                        | 49 ff 75 00             |
    | push [r14]                        | 49 ff 36                |
    | push [r15]                        | 49 ff 37                |
    | push [rax + 1 * rcx]              | 48 ff 34 08             |
    | push [rcx + 1 * rcx]              | 48 ff 34 09             |
    | push [rdx + 1 * rcx]              | 48 ff 34 0a             |
    | push [rbx + 1 * rcx]              | 48 ff 34 0b             |
    | push [rsp + 1 * rcx]              | 48 ff 34 0c             |
    | push [rbp + 1 * rcx]              | 48 ff 74 0d 00          |
    | push [rsi + 1 * rcx]              | 48 ff 34 0e             |
    | push [rdi + 1 * rcx]              | 48 ff 34 0f             |
    | push [r8 + 1 * rcx]               | 49 ff 34 08             |
    | push [r9 + 1 * rcx]               | 49 ff 34 09             |
    | push [r10 + 1 * rcx]              | 49 ff 34 0a             |
    | push [r11 + 1 * rcx]              | 49 ff 34 0b             |
    | push [r12 + 1 * rcx]              | 49 ff 34 0c             |
    | push [r13 + 1 * rcx]              | 49 ff 74 0d 00          |
    | push [r14 + 1 * rcx]              | 49 ff 34 0e             |
    | push [r15 + 1 * rcx]              | 49 ff 34 0f             |
    | push [rax + 1 * rax]              | 48 ff 34 00             |
    | push [rax + 1 * rdx]              | 48 ff 34 10             |
    | push [rax + 1 * rbx]              | 48 ff 34 18             |
    | push [rax + 1 * rbp]              | 48 ff 34 28             |
    | push [rax + 1 * rsi]              | 48 ff 34 30             |
    | push [rax + 1 * rdi]              | 48 ff 34 38             |
    | push [rax + 1 * r8]               | 4a ff 34 00             |
    | push [rax + 1 * r9]               | 4a ff 34 08             |
    | push [rax + 1 * r10]              | 4a ff 34 10             |
    | push [rax + 1 * r11]              | 4a ff 34 18             |
    | push [rax + 1 * r12]              | 4a ff 34 20             |
    | push [rax + 1 * r13]              | 4a ff 34 28             |
    | push [rax + 1 * r14]              | 4a ff 34 30             |
    | push [rax + 1 * r15]              | 4a ff 34 38             |
    | push [rax + 2 * rcx]              | 48 ff 34 48             |
    | push [rax + 4 * rcx]              | 48 ff 34 88             |
    | push [rax + 8 * rcx]              | 48 ff 34 c8             |
    | push [r8 + 1 * r9]                | 4b ff 34 08             |
    | push [r8 + 2 * r9]                | 4b ff 34 48             |
    | push [r8 + 4 * r9]                | 4b ff 34 88             |
    | push [r8 + 8 * r9]                | 4b ff 34 c8             |
    | push [1 * rcx]                    | 48 ff 34 0d 00 00 00 00 |
    | push [2 * rcx]                    | 48 ff 34 4d 00 00 00 00 |
    | push [4 * rcx]                    | 48 ff 34 8d 00 00 00 00 |
    | push [8 * rcx]                    | 48 ff 34 cd 00 00 00 00 |
    | push [1 * r9]                     | 4a ff 34 0d 00 00 00 00 |
    | push [2 * r9]                     | 4a ff 34 4d 00 00 00 00 |
    | push [4 * r9]                     | 4a ff 34 8d 00 00 00 00 |
    | push [8 * r9]                     | 4a ff 34 cd 00 00 00 00 |
    | push [r13 + 8 * r12]              | 4b ff 74 e5 00          |
    | push [rsp + 4 * r15]              | 4a ff 34 bc             |
    | push [rax + 1 * rcx + 0x00]       | 48 ff 74 08 00          |
    | push [rax + 1 * rcx - 0x00]       | 48 ff 74 08 00          |
    | push [rax + 1 * rcx + 0x0000]     | 48 ff b4 08 00 00 00 00 |
    | push [rax + 1 * rcx - 0x0000]     | 48 ff b4 08 00 00 00 00 |
    | push [rax + 1 * rcx + 0x01]       | 48 ff 74 08 01          |
    | push [rax + 1 * rcx - 0x01]       | 48 ff 74 08 ff          |
    | push [rax + 1 * rcx + 0x0001]     | 48 ff b4 08 01 00 00 00 |
    | push [rax + 1 * rcx - 0x0001]     | 48 ff b4 08 ff ff ff ff |
    | push [rax + 1 * rcx + 0x00000001] | 48 ff b4 08 01 00 00 00 |
    | push [rax + 1 * rcx - 0x00000001] | 48 ff b4 08 ff ff ff ff |
    | push [rax + 1 * rcx + 0x7f]       | 48 ff 74 08 7f          |
    | push [rax + 1 * rcx - 0x7f]       | 48 ff 74 08 81          |
    | push [rax + 1 * rcx + 0x80]       | 48 ff b4 08 80 00 00 00 |
    | push [rax + 1 * rcx - 0x80]       | 48 ff 74 08 80          |
    | push [rax + 1 * rcx - 0x81]       | 48 ff b4 08 7f ff ff ff |
    | push [rax + 1 * rcx + 0xff]       | 48 ff b4 08 ff 00 00 00 |
    | push [rax + 1 * rcx - 0xff]       | 48 ff b4 08 01 ff ff ff |
    | push [rax + 1 * rcx + 0x7fff]     | 48 ff b4 08 ff 7f 00 00 |
    | push [rax + 1 * rcx - 0x7fff]     | 48 ff b4 08 01 80 ff ff |
    | push [rax + 1 * rcx + 0x8000]     | 48 ff b4 08 00 80 00 00 |
    | push [rax + 1 * rcx - 0x8000]     | 48 ff b4 08 00 80 ff ff |
    | push [rax + 1 * rcx + 0xffff]     | 48 ff b4 08 ff ff 00 00 |
    | push [rax + 1 * rcx - 0xffff]     | 48 ff b4 08 01 00 ff ff |
    | push [rax + 1 * rcx + 0x7fffffff] | 48 ff b4 08 ff ff ff 7f |
    | push [rax + 1 * rcx - 0x7fffffff] | 48 ff b4 08 01 00 00 80 |
    | push [rax + 1 * rcx - 0x80000000] | 48 ff b4 08 00 00 00 80 |
    | push [r10 + 0x7f]                 | 49 ff 72 7f             |
    | push [r10 + 0x80]                 | 49 ff b2 80 00 00 00    |
    | push [r10 - 0x80]                 | 49 ff 72 80             |
    | push [r10 - 0x81]                 | 49 ff b2 7f ff ff ff    |
    | --------------------------------- | ----------------------- |
"""


def can_encode_push_addr64():
    encode(PUSH_ADDR64)
