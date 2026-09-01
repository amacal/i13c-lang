from tests.encoding.core import encode, exhaust


def can_exhaust_xor():
    exhaust(
        XOR_ADDR16_IMM16,
        XOR_ADDR16_IMM8,
        XOR_ADDR16_REG16,
        XOR_ADDR32_IMM32,
        XOR_ADDR32_IMM8,
        XOR_ADDR32_REG32,
        XOR_ADDR64_IMM32,
        XOR_ADDR64_IMM8,
        XOR_ADDR64_REG64,
        XOR_ADDR8_IMM8,
        XOR_ADDR8_REG8,
        XOR_REG16_ADDR16,
        XOR_REG16_IMM16,
        XOR_REG16_IMM8,
        XOR_REG16_REG16,
        XOR_REG32_ADDR32,
        XOR_REG32_IMM32,
        XOR_REG32_IMM8,
        XOR_REG32_REG32,
        XOR_REG64_ADDR64,
        XOR_REG64_IMM32,
        XOR_REG64_IMM8,
        XOR_REG64_REG64,
        XOR_REG8_ADDR8,
        XOR_REG8_IMM8,
        XOR_REG8_REG8,
    )


XOR_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | xor rax, 0x01 | 48 83 f0 01 | *** | xor rax, 0x00 | 48 83 f0 00 |
    | xor rcx, 0x01 | 48 83 f1 01 | *** | xor rax, 0x7f | 48 83 f0 7f |
    | xor rdx, 0x01 | 48 83 f2 01 | *** | xor rax, 0x80 | 48 83 f0 80 |
    | xor rbx, 0x01 | 48 83 f3 01 | *** | xor rax, 0xff | 48 83 f0 ff |
    | xor rsp, 0x01 | 48 83 f4 01 | *** | xor rcx, 0x7f | 48 83 f1 7f |
    | xor rbp, 0x01 | 48 83 f5 01 | *** | xor rdx, 0x80 | 48 83 f2 80 |
    | xor rsi, 0x01 | 48 83 f6 01 | *** | xor rbx, 0xff | 48 83 f3 ff |
    | xor rdi, 0x01 | 48 83 f7 01 | *** | xor rsp, 0x00 | 48 83 f4 00 |
    | xor r8, 0x01  | 49 83 f0 01 | *** | xor rsi, 0x7f | 48 83 f6 7f |
    | xor r9, 0x01  | 49 83 f1 01 | *** | xor rdi, 0x80 | 48 83 f7 80 |
    | xor r10, 0x01 | 49 83 f2 01 | *** | xor r8, 0xff  | 49 83 f0 ff |
    | xor r11, 0x01 | 49 83 f3 01 | *** | xor r9, 0x00  | 49 83 f1 00 |
    | xor r12, 0x01 | 49 83 f4 01 | *** | xor r11, 0x7f | 49 83 f3 7f |
    | xor r13, 0x01 | 49 83 f5 01 | *** | xor r12, 0x80 | 49 83 f4 80 |
    | xor r14, 0x01 | 49 83 f6 01 | *** | xor r13, 0xff | 49 83 f5 ff |
    | xor r15, 0x01 | 49 83 f7 01 | *** | xor r14, 0x00 | 49 83 f6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_xor_reg64_imm8():
    encode(XOR_REG64_IMM8)


XOR_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | xor rax, 0x00000001 | 48 35 01 00 00 00    | *** | xor rax, 0x00007fff | 48 35 ff 7f 00 00    |
    | xor rcx, 0x00000001 | 48 81 f1 01 00 00 00 | *** | xor rax, 0x00008000 | 48 35 00 80 00 00    |
    | xor rdx, 0x00000001 | 48 81 f2 01 00 00 00 | *** | xor rax, 0x0000ffff | 48 35 ff ff 00 00    |
    | xor rbx, 0x00000001 | 48 81 f3 01 00 00 00 | *** | xor rax, 0x00010000 | 48 35 00 00 01 00    |
    | xor rsp, 0x00000001 | 48 81 f4 01 00 00 00 | *** | xor rax, 0x7fffffff | 48 35 ff ff ff 7f    |
    | xor rbp, 0x00000001 | 48 81 f5 01 00 00 00 | *** | xor rax, 0x80000000 | 48 35 00 00 00 80    |
    | xor rsi, 0x00000001 | 48 81 f6 01 00 00 00 | *** | xor rax, 0xffffffff | 48 35 ff ff ff ff    |
    | xor rdi, 0x00000001 | 48 81 f7 01 00 00 00 | *** | xor rcx, 0x0000007f | 48 81 f1 7f 00 00 00 |
    | xor r8, 0x00000001  | 49 81 f0 01 00 00 00 | *** | xor rdx, 0x00000080 | 48 81 f2 80 00 00 00 |
    | xor r9, 0x00000001  | 49 81 f1 01 00 00 00 | *** | xor rbx, 0x000000ff | 48 81 f3 ff 00 00 00 |
    | xor r10, 0x00000001 | 49 81 f2 01 00 00 00 | *** | xor rsp, 0x00000100 | 48 81 f4 00 01 00 00 |
    | xor r11, 0x00000001 | 49 81 f3 01 00 00 00 | *** | xor rbp, 0x00007fff | 48 81 f5 ff 7f 00 00 |
    | xor r12, 0x00000001 | 49 81 f4 01 00 00 00 | *** | xor rsi, 0x00008000 | 48 81 f6 00 80 00 00 |
    | xor r13, 0x00000001 | 49 81 f5 01 00 00 00 | *** | xor rdi, 0x0000ffff | 48 81 f7 ff ff 00 00 |
    | xor r14, 0x00000001 | 49 81 f6 01 00 00 00 | *** | xor r8, 0x00010000  | 49 81 f0 00 00 01 00 |
    | xor r15, 0x00000001 | 49 81 f7 01 00 00 00 | *** | xor r9, 0x7fffffff  | 49 81 f1 ff ff ff 7f |
    | xor rax, 0x00000000 | 48 35 00 00 00 00    | *** | xor r10, 0x80000000 | 49 81 f2 00 00 00 80 |
    | xor rax, 0x0000007f | 48 35 7f 00 00 00    | *** | xor r11, 0xffffffff | 49 81 f3 ff ff ff ff |
    | xor rax, 0x00000080 | 48 35 80 00 00 00    | *** | xor r12, 0x00000000 | 49 81 f4 00 00 00 00 |
    | xor rax, 0x000000ff | 48 35 ff 00 00 00    | *** | xor r14, 0x0000007f | 49 81 f6 7f 00 00 00 |
    | xor rax, 0x00000100 | 48 35 00 01 00 00    | *** | xor r15, 0x00000080 | 49 81 f7 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_xor_reg64_imm32():
    encode(XOR_REG64_IMM32)


XOR_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | xor rax, rcx | 48 31 c8 | *** | xor rax, r8  | 4c 31 c0 |
    | xor rcx, rcx | 48 31 c9 | *** | xor rax, r9  | 4c 31 c8 |
    | xor rdx, rcx | 48 31 ca | *** | xor rax, r10 | 4c 31 d0 |
    | xor rbx, rcx | 48 31 cb | *** | xor rax, r11 | 4c 31 d8 |
    | xor rsp, rcx | 48 31 cc | *** | xor rax, r12 | 4c 31 e0 |
    | xor rbp, rcx | 48 31 cd | *** | xor rax, r13 | 4c 31 e8 |
    | xor rsi, rcx | 48 31 ce | *** | xor rax, r14 | 4c 31 f0 |
    | xor rdi, rcx | 48 31 cf | *** | xor rax, r15 | 4c 31 f8 |
    | xor r8, rcx  | 49 31 c8 | *** | xor rcx, rdx | 48 31 d1 |
    | xor r9, rcx  | 49 31 c9 | *** | xor rdx, rbx | 48 31 da |
    | xor r10, rcx | 49 31 ca | *** | xor rbx, rsp | 48 31 e3 |
    | xor r11, rcx | 49 31 cb | *** | xor rsp, rbp | 48 31 ec |
    | xor r12, rcx | 49 31 cc | *** | xor rbp, rsi | 48 31 f5 |
    | xor r13, rcx | 49 31 cd | *** | xor rsi, rdi | 48 31 fe |
    | xor r14, rcx | 49 31 ce | *** | xor rdi, r8  | 4c 31 c7 |
    | xor r15, rcx | 49 31 cf | *** | xor r8, r9   | 4d 31 c8 |
    | xor rax, rax | 48 31 c0 | *** | xor r9, r10  | 4d 31 d1 |
    | xor rax, rdx | 48 31 d0 | *** | xor r10, r11 | 4d 31 da |
    | xor rax, rbx | 48 31 d8 | *** | xor r11, r12 | 4d 31 e3 |
    | xor rax, rsp | 48 31 e0 | *** | xor r12, r13 | 4d 31 ec |
    | xor rax, rbp | 48 31 e8 | *** | xor r13, r14 | 4d 31 f5 |
    | xor rax, rsi | 48 31 f0 | *** | xor r14, r15 | 4d 31 fe |
    | xor rax, rdi | 48 31 f8 | *** | xor r15, rax | 49 31 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_xor_reg64_reg64():
    encode(XOR_REG64_REG64)


XOR_REG64_ADDR64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | xor rax, qword [rcx]                        | 48 33 01                |
    | xor rcx, qword [rcx]                        | 48 33 09                |
    | xor rdx, qword [rcx]                        | 48 33 11                |
    | xor rbx, qword [rcx]                        | 48 33 19                |
    | xor rsp, qword [rcx]                        | 48 33 21                |
    | xor rbp, qword [rcx]                        | 48 33 29                |
    | xor rsi, qword [rcx]                        | 48 33 31                |
    | xor rdi, qword [rcx]                        | 48 33 39                |
    | xor r8, qword [rcx]                         | 4c 33 01                |
    | xor r9, qword [rcx]                         | 4c 33 09                |
    | xor r10, qword [rcx]                        | 4c 33 11                |
    | xor r11, qword [rcx]                        | 4c 33 19                |
    | xor r12, qword [rcx]                        | 4c 33 21                |
    | xor r13, qword [rcx]                        | 4c 33 29                |
    | xor r14, qword [rcx]                        | 4c 33 31                |
    | xor r15, qword [rcx]                        | 4c 33 39                |
    | xor rax, qword [rax]                        | 48 33 00                |
    | xor rax, qword [rdx]                        | 48 33 02                |
    | xor rax, qword [rbx]                        | 48 33 03                |
    | xor rax, qword [rsp]                        | 48 33 04 24             |
    | xor rax, qword [rbp]                        | 48 33 45 00             |
    | xor rax, qword [rsi]                        | 48 33 06                |
    | xor rax, qword [rdi]                        | 48 33 07                |
    | xor rax, qword [r8]                         | 49 33 00                |
    | xor rax, qword [r9]                         | 49 33 01                |
    | xor rax, qword [r10]                        | 49 33 02                |
    | xor rax, qword [r11]                        | 49 33 03                |
    | xor rax, qword [r12]                        | 49 33 04 24             |
    | xor rax, qword [r13]                        | 49 33 45 00             |
    | xor rax, qword [r14]                        | 49 33 06                |
    | xor rax, qword [r15]                        | 49 33 07                |
    | xor rax, qword [rax + 1 * rcx]              | 48 33 04 08             |
    | xor rax, qword [rcx + 1 * rcx]              | 48 33 04 09             |
    | xor rax, qword [rdx + 1 * rcx]              | 48 33 04 0a             |
    | xor rax, qword [rbx + 1 * rcx]              | 48 33 04 0b             |
    | xor rax, qword [rsp + 1 * rcx]              | 48 33 04 0c             |
    | xor rax, qword [rbp + 1 * rcx]              | 48 33 44 0d 00          |
    | xor rax, qword [rsi + 1 * rcx]              | 48 33 04 0e             |
    | xor rax, qword [rdi + 1 * rcx]              | 48 33 04 0f             |
    | xor rax, qword [r8 + 1 * rcx]               | 49 33 04 08             |
    | xor rax, qword [r9 + 1 * rcx]               | 49 33 04 09             |
    | xor rax, qword [r10 + 1 * rcx]              | 49 33 04 0a             |
    | xor rax, qword [r11 + 1 * rcx]              | 49 33 04 0b             |
    | xor rax, qword [r12 + 1 * rcx]              | 49 33 04 0c             |
    | xor rax, qword [r13 + 1 * rcx]              | 49 33 44 0d 00          |
    | xor rax, qword [r14 + 1 * rcx]              | 49 33 04 0e             |
    | xor rax, qword [r15 + 1 * rcx]              | 49 33 04 0f             |
    | xor rax, qword [rax + 1 * rax]              | 48 33 04 00             |
    | xor rax, qword [rax + 1 * rdx]              | 48 33 04 10             |
    | xor rax, qword [rax + 1 * rbx]              | 48 33 04 18             |
    | xor rax, qword [rax + 1 * rbp]              | 48 33 04 28             |
    | xor rax, qword [rax + 1 * rsi]              | 48 33 04 30             |
    | xor rax, qword [rax + 1 * rdi]              | 48 33 04 38             |
    | xor rax, qword [rax + 1 * r8]               | 4a 33 04 00             |
    | xor rax, qword [rax + 1 * r9]               | 4a 33 04 08             |
    | xor rax, qword [rax + 1 * r10]              | 4a 33 04 10             |
    | xor rax, qword [rax + 1 * r11]              | 4a 33 04 18             |
    | xor rax, qword [rax + 1 * r12]              | 4a 33 04 20             |
    | xor rax, qword [rax + 1 * r13]              | 4a 33 04 28             |
    | xor rax, qword [rax + 1 * r14]              | 4a 33 04 30             |
    | xor rax, qword [rax + 1 * r15]              | 4a 33 04 38             |
    | xor rax, qword [rax + 2 * rcx]              | 48 33 04 48             |
    | xor rax, qword [rax + 4 * rcx]              | 48 33 04 88             |
    | xor rax, qword [rax + 8 * rcx]              | 48 33 04 c8             |
    | xor rax, qword [r8 + 1 * r9]                | 4b 33 04 08             |
    | xor rax, qword [r8 + 2 * r9]                | 4b 33 04 48             |
    | xor rax, qword [r8 + 4 * r9]                | 4b 33 04 88             |
    | xor rax, qword [r8 + 8 * r9]                | 4b 33 04 c8             |
    | xor rax, qword [1 * rcx]                    | 48 33 04 0d 00 00 00 00 |
    | xor rax, qword [2 * rcx]                    | 48 33 04 4d 00 00 00 00 |
    | xor rax, qword [4 * rcx]                    | 48 33 04 8d 00 00 00 00 |
    | xor rax, qword [8 * rcx]                    | 48 33 04 cd 00 00 00 00 |
    | xor rax, qword [1 * r9]                     | 4a 33 04 0d 00 00 00 00 |
    | xor rax, qword [2 * r9]                     | 4a 33 04 4d 00 00 00 00 |
    | xor rax, qword [4 * r9]                     | 4a 33 04 8d 00 00 00 00 |
    | xor rax, qword [8 * r9]                     | 4a 33 04 cd 00 00 00 00 |
    | xor rax, qword [r13 + 8 * r12]              | 4b 33 44 e5 00          |
    | xor rax, qword [rsp + 4 * r15]              | 4a 33 04 bc             |
    | xor rax, qword [rax + 1 * rcx + 0x00]       | 48 33 44 08 00          |
    | xor rax, qword [rax + 1 * rcx - 0x00]       | 48 33 44 08 00          |
    | xor rax, qword [rax + 1 * rcx + 0x01]       | 48 33 44 08 01          |
    | xor rax, qword [rax + 1 * rcx - 0x01]       | 48 33 44 08 ff          |
    | xor rax, qword [rax + 1 * rcx + 0x00000001] | 48 33 84 08 01 00 00 00 |
    | xor rax, qword [rax + 1 * rcx - 0x00000001] | 48 33 84 08 ff ff ff ff |
    | xor rax, qword [rax + 1 * rcx + 0x7f]       | 48 33 44 08 7f          |
    | xor rax, qword [rax + 1 * rcx - 0x7f]       | 48 33 44 08 81          |
    | xor rax, qword [rax + 1 * rcx + 0x80]       | 48 33 84 08 80 00 00 00 |
    | xor rax, qword [rax + 1 * rcx - 0x80]       | 48 33 44 08 80          |
    | xor rax, qword [rax + 1 * rcx - 0x81]       | 48 33 84 08 7f ff ff ff |
    | xor rax, qword [rax + 1 * rcx + 0xff]       | 48 33 84 08 ff 00 00 00 |
    | xor rax, qword [rax + 1 * rcx - 0xff]       | 48 33 84 08 01 ff ff ff |
    | xor rax, qword [rax + 1 * rcx + 0x7fffffff] | 48 33 84 08 ff ff ff 7f |
    | xor rax, qword [rax + 1 * rcx - 0x7fffffff] | 48 33 84 08 01 00 00 80 |
    | xor rax, qword [rax + 1 * rcx - 0x80000000] | 48 33 84 08 00 00 00 80 |
    | xor rax, qword [r10 + 0x7f]                 | 49 33 42 7f             |
    | xor rax, qword [r10 + 0x80]                 | 49 33 82 80 00 00 00    |
    | xor rax, qword [r10 - 0x80]                 | 49 33 42 80             |
    | xor rax, qword [r10 - 0x81]                 | 49 33 82 7f ff ff ff    |
    | xor rcx, qword [rdx]                        | 48 33 0a                |
    | xor rdx, qword [rbx]                        | 48 33 13                |
    | xor rbx, qword [rsp]                        | 48 33 1c 24             |
    | xor rsp, qword [rbp]                        | 48 33 65 00             |
    | xor rbp, qword [rsi]                        | 48 33 2e                |
    | xor rsi, qword [rdi]                        | 48 33 37                |
    | xor rdi, qword [r8]                         | 49 33 38                |
    | xor r8, qword [r9]                          | 4d 33 01                |
    | xor r9, qword [r10]                         | 4d 33 0a                |
    | xor r10, qword [r11]                        | 4d 33 13                |
    | xor r11, qword [r12]                        | 4d 33 1c 24             |
    | xor r12, qword [r13]                        | 4d 33 65 00             |
    | xor r13, qword [r14]                        | 4d 33 2e                |
    | xor r14, qword [r15]                        | 4d 33 37                |
    | xor r15, qword [rax + 1 * rcx]              | 4c 33 3c 08             |
    | xor rcx, qword [rdx + 1 * rcx]              | 48 33 0c 0a             |
    | xor rdx, qword [rbx + 1 * rcx]              | 48 33 14 0b             |
    | xor rbx, qword [rsp + 1 * rcx]              | 48 33 1c 0c             |
    | xor rsp, qword [rbp + 1 * rcx]              | 48 33 64 0d 00          |
    | xor rbp, qword [rsi + 1 * rcx]              | 48 33 2c 0e             |
    | xor rsi, qword [rdi + 1 * rcx]              | 48 33 34 0f             |
    | xor rdi, qword [r8 + 1 * rcx]               | 49 33 3c 08             |
    | xor r8, qword [r9 + 1 * rcx]                | 4d 33 04 09             |
    | xor r9, qword [r10 + 1 * rcx]               | 4d 33 0c 0a             |
    | xor r10, qword [r11 + 1 * rcx]              | 4d 33 14 0b             |
    | xor r11, qword [r12 + 1 * rcx]              | 4d 33 1c 0c             |
    | xor r12, qword [r13 + 1 * rcx]              | 4d 33 64 0d 00          |
    | xor r13, qword [r14 + 1 * rcx]              | 4d 33 2c 0e             |
    | xor r14, qword [r15 + 1 * rcx]              | 4d 33 34 0f             |
    | xor r15, qword [rax + 1 * rax]              | 4c 33 3c 00             |
    | xor rcx, qword [rax + 1 * rbx]              | 48 33 0c 18             |
    | xor rdx, qword [rax + 1 * rbp]              | 48 33 14 28             |
    | xor rbx, qword [rax + 1 * rsi]              | 48 33 1c 30             |
    | xor rsp, qword [rax + 1 * rdi]              | 48 33 24 38             |
    | xor rbp, qword [rax + 1 * r8]               | 4a 33 2c 00             |
    | xor rsi, qword [rax + 1 * r9]               | 4a 33 34 08             |
    | xor rdi, qword [rax + 1 * r10]              | 4a 33 3c 10             |
    | xor r8, qword [rax + 1 * r11]               | 4e 33 04 18             |
    | xor r9, qword [rax + 1 * r12]               | 4e 33 0c 20             |
    | xor r10, qword [rax + 1 * r13]              | 4e 33 14 28             |
    | xor r11, qword [rax + 1 * r14]              | 4e 33 1c 30             |
    | xor r12, qword [rax + 1 * r15]              | 4e 33 24 38             |
    | xor r13, qword [rax + 2 * rcx]              | 4c 33 2c 48             |
    | xor r14, qword [rax + 4 * rcx]              | 4c 33 34 88             |
    | xor r15, qword [rax + 8 * rcx]              | 4c 33 3c c8             |
    | xor rcx, qword [r8 + 2 * r9]                | 4b 33 0c 48             |
    | xor rdx, qword [r8 + 4 * r9]                | 4b 33 14 88             |
    | xor rbx, qword [r8 + 8 * r9]                | 4b 33 1c c8             |
    | xor rsp, qword [1 * rcx]                    | 48 33 24 0d 00 00 00 00 |
    | xor rbp, qword [2 * rcx]                    | 48 33 2c 4d 00 00 00 00 |
    | xor rsi, qword [4 * rcx]                    | 48 33 34 8d 00 00 00 00 |
    | xor rdi, qword [8 * rcx]                    | 48 33 3c cd 00 00 00 00 |
    | xor r8, qword [1 * r9]                      | 4e 33 04 0d 00 00 00 00 |
    | xor r9, qword [2 * r9]                      | 4e 33 0c 4d 00 00 00 00 |
    | xor r10, qword [4 * r9]                     | 4e 33 14 8d 00 00 00 00 |
    | xor r11, qword [8 * r9]                     | 4e 33 1c cd 00 00 00 00 |
    | xor r12, qword [r13 + 8 * r12]              | 4f 33 64 e5 00          |
    | xor r13, qword [rsp + 4 * r15]              | 4e 33 2c bc             |
    | xor r14, qword [rax + 1 * rcx + 0x00]       | 4c 33 74 08 00          |
    | xor r15, qword [rax + 1 * rcx - 0x00]       | 4c 33 7c 08 00          |
    | xor rcx, qword [rax + 1 * rcx - 0x01]       | 48 33 4c 08 ff          |
    | xor rdx, qword [rax + 1 * rcx + 0x00000001] | 48 33 94 08 01 00 00 00 |
    | xor rbx, qword [rax + 1 * rcx - 0x00000001] | 48 33 9c 08 ff ff ff ff |
    | xor rsp, qword [rax + 1 * rcx + 0x7f]       | 48 33 64 08 7f          |
    | xor rbp, qword [rax + 1 * rcx - 0x7f]       | 48 33 6c 08 81          |
    | xor rsi, qword [rax + 1 * rcx + 0x80]       | 48 33 b4 08 80 00 00 00 |
    | xor rdi, qword [rax + 1 * rcx - 0x80]       | 48 33 7c 08 80          |
    | xor r8, qword [rax + 1 * rcx - 0x81]        | 4c 33 84 08 7f ff ff ff |
    | xor r9, qword [rax + 1 * rcx + 0xff]        | 4c 33 8c 08 ff 00 00 00 |
    | xor r10, qword [rax + 1 * rcx - 0xff]       | 4c 33 94 08 01 ff ff ff |
    | xor r11, qword [rax + 1 * rcx + 0x7fffffff] | 4c 33 9c 08 ff ff ff 7f |
    | xor r12, qword [rax + 1 * rcx - 0x7fffffff] | 4c 33 a4 08 01 00 00 80 |
    | xor r13, qword [rax + 1 * rcx - 0x80000000] | 4c 33 ac 08 00 00 00 80 |
    | xor r14, qword [r10 + 0x7f]                 | 4d 33 72 7f             |
    | xor r15, qword [r10 + 0x80]                 | 4d 33 ba 80 00 00 00    |
    | xor rcx, qword [r10 - 0x81]                 | 49 33 8a 7f ff ff ff    |
    | xor rdx, qword [rax]                        | 48 33 10                |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_xor_reg64_addr64():
    encode(XOR_REG64_ADDR64)


XOR_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | xor eax, 0x01  | 83 f0 01    | *** | xor eax, 0x00  | 83 f0 00    |
    | xor ecx, 0x01  | 83 f1 01    | *** | xor eax, 0x7f  | 83 f0 7f    |
    | xor edx, 0x01  | 83 f2 01    | *** | xor eax, 0x80  | 83 f0 80    |
    | xor ebx, 0x01  | 83 f3 01    | *** | xor eax, 0xff  | 83 f0 ff    |
    | xor esp, 0x01  | 83 f4 01    | *** | xor ecx, 0x7f  | 83 f1 7f    |
    | xor ebp, 0x01  | 83 f5 01    | *** | xor edx, 0x80  | 83 f2 80    |
    | xor esi, 0x01  | 83 f6 01    | *** | xor ebx, 0xff  | 83 f3 ff    |
    | xor edi, 0x01  | 83 f7 01    | *** | xor esp, 0x00  | 83 f4 00    |
    | xor r8d, 0x01  | 41 83 f0 01 | *** | xor esi, 0x7f  | 83 f6 7f    |
    | xor r9d, 0x01  | 41 83 f1 01 | *** | xor edi, 0x80  | 83 f7 80    |
    | xor r10d, 0x01 | 41 83 f2 01 | *** | xor r8d, 0xff  | 41 83 f0 ff |
    | xor r11d, 0x01 | 41 83 f3 01 | *** | xor r9d, 0x00  | 41 83 f1 00 |
    | xor r12d, 0x01 | 41 83 f4 01 | *** | xor r11d, 0x7f | 41 83 f3 7f |
    | xor r13d, 0x01 | 41 83 f5 01 | *** | xor r12d, 0x80 | 41 83 f4 80 |
    | xor r14d, 0x01 | 41 83 f6 01 | *** | xor r13d, 0xff | 41 83 f5 ff |
    | xor r15d, 0x01 | 41 83 f7 01 | *** | xor r14d, 0x00 | 41 83 f6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_xor_reg32_imm8():
    encode(XOR_REG32_IMM8)


XOR_REG32_IMM32 = """
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | instruction          | encoding             | *** | instruction          | encoding             |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | xor eax, 0x00000001  | 35 01 00 00 00       | *** | xor eax, 0x00007fff  | 35 ff 7f 00 00       |
    | xor ecx, 0x00000001  | 81 f1 01 00 00 00    | *** | xor eax, 0x00008000  | 35 00 80 00 00       |
    | xor edx, 0x00000001  | 81 f2 01 00 00 00    | *** | xor eax, 0x0000ffff  | 35 ff ff 00 00       |
    | xor ebx, 0x00000001  | 81 f3 01 00 00 00    | *** | xor eax, 0x00010000  | 35 00 00 01 00       |
    | xor esp, 0x00000001  | 81 f4 01 00 00 00    | *** | xor eax, 0x7fffffff  | 35 ff ff ff 7f       |
    | xor ebp, 0x00000001  | 81 f5 01 00 00 00    | *** | xor eax, 0x80000000  | 35 00 00 00 80       |
    | xor esi, 0x00000001  | 81 f6 01 00 00 00    | *** | xor eax, 0xffffffff  | 35 ff ff ff ff       |
    | xor edi, 0x00000001  | 81 f7 01 00 00 00    | *** | xor ecx, 0x0000007f  | 81 f1 7f 00 00 00    |
    | xor r8d, 0x00000001  | 41 81 f0 01 00 00 00 | *** | xor edx, 0x00000080  | 81 f2 80 00 00 00    |
    | xor r9d, 0x00000001  | 41 81 f1 01 00 00 00 | *** | xor ebx, 0x000000ff  | 81 f3 ff 00 00 00    |
    | xor r10d, 0x00000001 | 41 81 f2 01 00 00 00 | *** | xor esp, 0x00000100  | 81 f4 00 01 00 00    |
    | xor r11d, 0x00000001 | 41 81 f3 01 00 00 00 | *** | xor ebp, 0x00007fff  | 81 f5 ff 7f 00 00    |
    | xor r12d, 0x00000001 | 41 81 f4 01 00 00 00 | *** | xor esi, 0x00008000  | 81 f6 00 80 00 00    |
    | xor r13d, 0x00000001 | 41 81 f5 01 00 00 00 | *** | xor edi, 0x0000ffff  | 81 f7 ff ff 00 00    |
    | xor r14d, 0x00000001 | 41 81 f6 01 00 00 00 | *** | xor r8d, 0x00010000  | 41 81 f0 00 00 01 00 |
    | xor r15d, 0x00000001 | 41 81 f7 01 00 00 00 | *** | xor r9d, 0x7fffffff  | 41 81 f1 ff ff ff 7f |
    | xor eax, 0x00000000  | 35 00 00 00 00       | *** | xor r10d, 0x80000000 | 41 81 f2 00 00 00 80 |
    | xor eax, 0x0000007f  | 35 7f 00 00 00       | *** | xor r11d, 0xffffffff | 41 81 f3 ff ff ff ff |
    | xor eax, 0x00000080  | 35 80 00 00 00       | *** | xor r12d, 0x00000000 | 41 81 f4 00 00 00 00 |
    | xor eax, 0x000000ff  | 35 ff 00 00 00       | *** | xor r14d, 0x0000007f | 41 81 f6 7f 00 00 00 |
    | xor eax, 0x00000100  | 35 00 01 00 00       | *** | xor r15d, 0x00000080 | 41 81 f7 80 00 00 00 |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
"""


def can_encode_xor_reg32_imm32():
    encode(XOR_REG32_IMM32)


XOR_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | xor eax, ecx   | 31 c8    | *** | xor eax, r8d   | 44 31 c0 |
    | xor ecx, ecx   | 31 c9    | *** | xor eax, r9d   | 44 31 c8 |
    | xor edx, ecx   | 31 ca    | *** | xor eax, r10d  | 44 31 d0 |
    | xor ebx, ecx   | 31 cb    | *** | xor eax, r11d  | 44 31 d8 |
    | xor esp, ecx   | 31 cc    | *** | xor eax, r12d  | 44 31 e0 |
    | xor ebp, ecx   | 31 cd    | *** | xor eax, r13d  | 44 31 e8 |
    | xor esi, ecx   | 31 ce    | *** | xor eax, r14d  | 44 31 f0 |
    | xor edi, ecx   | 31 cf    | *** | xor eax, r15d  | 44 31 f8 |
    | xor r8d, ecx   | 41 31 c8 | *** | xor ecx, edx   | 31 d1    |
    | xor r9d, ecx   | 41 31 c9 | *** | xor edx, ebx   | 31 da    |
    | xor r10d, ecx  | 41 31 ca | *** | xor ebx, esp   | 31 e3    |
    | xor r11d, ecx  | 41 31 cb | *** | xor esp, ebp   | 31 ec    |
    | xor r12d, ecx  | 41 31 cc | *** | xor ebp, esi   | 31 f5    |
    | xor r13d, ecx  | 41 31 cd | *** | xor esi, edi   | 31 fe    |
    | xor r14d, ecx  | 41 31 ce | *** | xor edi, r8d   | 44 31 c7 |
    | xor r15d, ecx  | 41 31 cf | *** | xor r8d, r9d   | 45 31 c8 |
    | xor eax, eax   | 31 c0    | *** | xor r9d, r10d  | 45 31 d1 |
    | xor eax, edx   | 31 d0    | *** | xor r10d, r11d | 45 31 da |
    | xor eax, ebx   | 31 d8    | *** | xor r11d, r12d | 45 31 e3 |
    | xor eax, esp   | 31 e0    | *** | xor r12d, r13d | 45 31 ec |
    | xor eax, ebp   | 31 e8    | *** | xor r13d, r14d | 45 31 f5 |
    | xor eax, esi   | 31 f0    | *** | xor r14d, r15d | 45 31 fe |
    | xor eax, edi   | 31 f8    | *** | xor r15d, eax  | 41 31 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_xor_reg32_reg32():
    encode(XOR_REG32_REG32)


XOR_REG32_ADDR32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | xor eax, dword [rcx]                         | 33 01                   |
    | xor ecx, dword [rcx]                         | 33 09                   |
    | xor edx, dword [rcx]                         | 33 11                   |
    | xor ebx, dword [rcx]                         | 33 19                   |
    | xor esp, dword [rcx]                         | 33 21                   |
    | xor ebp, dword [rcx]                         | 33 29                   |
    | xor esi, dword [rcx]                         | 33 31                   |
    | xor edi, dword [rcx]                         | 33 39                   |
    | xor r8d, dword [rcx]                         | 44 33 01                |
    | xor r9d, dword [rcx]                         | 44 33 09                |
    | xor r10d, dword [rcx]                        | 44 33 11                |
    | xor r11d, dword [rcx]                        | 44 33 19                |
    | xor r12d, dword [rcx]                        | 44 33 21                |
    | xor r13d, dword [rcx]                        | 44 33 29                |
    | xor r14d, dword [rcx]                        | 44 33 31                |
    | xor r15d, dword [rcx]                        | 44 33 39                |
    | xor eax, dword [rax]                         | 33 00                   |
    | xor eax, dword [rdx]                         | 33 02                   |
    | xor eax, dword [rbx]                         | 33 03                   |
    | xor eax, dword [rsp]                         | 33 04 24                |
    | xor eax, dword [rbp]                         | 33 45 00                |
    | xor eax, dword [rsi]                         | 33 06                   |
    | xor eax, dword [rdi]                         | 33 07                   |
    | xor eax, dword [r8]                          | 41 33 00                |
    | xor eax, dword [r9]                          | 41 33 01                |
    | xor eax, dword [r10]                         | 41 33 02                |
    | xor eax, dword [r11]                         | 41 33 03                |
    | xor eax, dword [r12]                         | 41 33 04 24             |
    | xor eax, dword [r13]                         | 41 33 45 00             |
    | xor eax, dword [r14]                         | 41 33 06                |
    | xor eax, dword [r15]                         | 41 33 07                |
    | xor eax, dword [rax + 1 * rcx]               | 33 04 08                |
    | xor eax, dword [rcx + 1 * rcx]               | 33 04 09                |
    | xor eax, dword [rdx + 1 * rcx]               | 33 04 0a                |
    | xor eax, dword [rbx + 1 * rcx]               | 33 04 0b                |
    | xor eax, dword [rsp + 1 * rcx]               | 33 04 0c                |
    | xor eax, dword [rbp + 1 * rcx]               | 33 44 0d 00             |
    | xor eax, dword [rsi + 1 * rcx]               | 33 04 0e                |
    | xor eax, dword [rdi + 1 * rcx]               | 33 04 0f                |
    | xor eax, dword [r8 + 1 * rcx]                | 41 33 04 08             |
    | xor eax, dword [r9 + 1 * rcx]                | 41 33 04 09             |
    | xor eax, dword [r10 + 1 * rcx]               | 41 33 04 0a             |
    | xor eax, dword [r11 + 1 * rcx]               | 41 33 04 0b             |
    | xor eax, dword [r12 + 1 * rcx]               | 41 33 04 0c             |
    | xor eax, dword [r13 + 1 * rcx]               | 41 33 44 0d 00          |
    | xor eax, dword [r14 + 1 * rcx]               | 41 33 04 0e             |
    | xor eax, dword [r15 + 1 * rcx]               | 41 33 04 0f             |
    | xor eax, dword [rax + 1 * rax]               | 33 04 00                |
    | xor eax, dword [rax + 1 * rdx]               | 33 04 10                |
    | xor eax, dword [rax + 1 * rbx]               | 33 04 18                |
    | xor eax, dword [rax + 1 * rbp]               | 33 04 28                |
    | xor eax, dword [rax + 1 * rsi]               | 33 04 30                |
    | xor eax, dword [rax + 1 * rdi]               | 33 04 38                |
    | xor eax, dword [rax + 1 * r8]                | 42 33 04 00             |
    | xor eax, dword [rax + 1 * r9]                | 42 33 04 08             |
    | xor eax, dword [rax + 1 * r10]               | 42 33 04 10             |
    | xor eax, dword [rax + 1 * r11]               | 42 33 04 18             |
    | xor eax, dword [rax + 1 * r12]               | 42 33 04 20             |
    | xor eax, dword [rax + 1 * r13]               | 42 33 04 28             |
    | xor eax, dword [rax + 1 * r14]               | 42 33 04 30             |
    | xor eax, dword [rax + 1 * r15]               | 42 33 04 38             |
    | xor eax, dword [rax + 2 * rcx]               | 33 04 48                |
    | xor eax, dword [rax + 4 * rcx]               | 33 04 88                |
    | xor eax, dword [rax + 8 * rcx]               | 33 04 c8                |
    | xor eax, dword [r8 + 1 * r9]                 | 43 33 04 08             |
    | xor eax, dword [r8 + 2 * r9]                 | 43 33 04 48             |
    | xor eax, dword [r8 + 4 * r9]                 | 43 33 04 88             |
    | xor eax, dword [r8 + 8 * r9]                 | 43 33 04 c8             |
    | xor eax, dword [1 * rcx]                     | 33 04 0d 00 00 00 00    |
    | xor eax, dword [2 * rcx]                     | 33 04 4d 00 00 00 00    |
    | xor eax, dword [4 * rcx]                     | 33 04 8d 00 00 00 00    |
    | xor eax, dword [8 * rcx]                     | 33 04 cd 00 00 00 00    |
    | xor eax, dword [1 * r9]                      | 42 33 04 0d 00 00 00 00 |
    | xor eax, dword [2 * r9]                      | 42 33 04 4d 00 00 00 00 |
    | xor eax, dword [4 * r9]                      | 42 33 04 8d 00 00 00 00 |
    | xor eax, dword [8 * r9]                      | 42 33 04 cd 00 00 00 00 |
    | xor eax, dword [r13 + 8 * r12]               | 43 33 44 e5 00          |
    | xor eax, dword [rsp + 4 * r15]               | 42 33 04 bc             |
    | xor eax, dword [rax + 1 * rcx + 0x00]        | 33 44 08 00             |
    | xor eax, dword [rax + 1 * rcx - 0x00]        | 33 44 08 00             |
    | xor eax, dword [rax + 1 * rcx + 0x01]        | 33 44 08 01             |
    | xor eax, dword [rax + 1 * rcx - 0x01]        | 33 44 08 ff             |
    | xor eax, dword [rax + 1 * rcx + 0x00000001]  | 33 84 08 01 00 00 00    |
    | xor eax, dword [rax + 1 * rcx - 0x00000001]  | 33 84 08 ff ff ff ff    |
    | xor eax, dword [rax + 1 * rcx + 0x7f]        | 33 44 08 7f             |
    | xor eax, dword [rax + 1 * rcx - 0x7f]        | 33 44 08 81             |
    | xor eax, dword [rax + 1 * rcx + 0x80]        | 33 84 08 80 00 00 00    |
    | xor eax, dword [rax + 1 * rcx - 0x80]        | 33 44 08 80             |
    | xor eax, dword [rax + 1 * rcx - 0x81]        | 33 84 08 7f ff ff ff    |
    | xor eax, dword [rax + 1 * rcx + 0xff]        | 33 84 08 ff 00 00 00    |
    | xor eax, dword [rax + 1 * rcx - 0xff]        | 33 84 08 01 ff ff ff    |
    | xor eax, dword [rax + 1 * rcx + 0x7fffffff]  | 33 84 08 ff ff ff 7f    |
    | xor eax, dword [rax + 1 * rcx - 0x7fffffff]  | 33 84 08 01 00 00 80    |
    | xor eax, dword [rax + 1 * rcx - 0x80000000]  | 33 84 08 00 00 00 80    |
    | xor eax, dword [r10 + 0x7f]                  | 41 33 42 7f             |
    | xor eax, dword [r10 + 0x80]                  | 41 33 82 80 00 00 00    |
    | xor eax, dword [r10 - 0x80]                  | 41 33 42 80             |
    | xor eax, dword [r10 - 0x81]                  | 41 33 82 7f ff ff ff    |
    | xor ecx, dword [rdx]                         | 33 0a                   |
    | xor edx, dword [rbx]                         | 33 13                   |
    | xor ebx, dword [rsp]                         | 33 1c 24                |
    | xor esp, dword [rbp]                         | 33 65 00                |
    | xor ebp, dword [rsi]                         | 33 2e                   |
    | xor esi, dword [rdi]                         | 33 37                   |
    | xor edi, dword [r8]                          | 41 33 38                |
    | xor r8d, dword [r9]                          | 45 33 01                |
    | xor r9d, dword [r10]                         | 45 33 0a                |
    | xor r10d, dword [r11]                        | 45 33 13                |
    | xor r11d, dword [r12]                        | 45 33 1c 24             |
    | xor r12d, dword [r13]                        | 45 33 65 00             |
    | xor r13d, dword [r14]                        | 45 33 2e                |
    | xor r14d, dword [r15]                        | 45 33 37                |
    | xor r15d, dword [rax + 1 * rcx]              | 44 33 3c 08             |
    | xor ecx, dword [rdx + 1 * rcx]               | 33 0c 0a                |
    | xor edx, dword [rbx + 1 * rcx]               | 33 14 0b                |
    | xor ebx, dword [rsp + 1 * rcx]               | 33 1c 0c                |
    | xor esp, dword [rbp + 1 * rcx]               | 33 64 0d 00             |
    | xor ebp, dword [rsi + 1 * rcx]               | 33 2c 0e                |
    | xor esi, dword [rdi + 1 * rcx]               | 33 34 0f                |
    | xor edi, dword [r8 + 1 * rcx]                | 41 33 3c 08             |
    | xor r8d, dword [r9 + 1 * rcx]                | 45 33 04 09             |
    | xor r9d, dword [r10 + 1 * rcx]               | 45 33 0c 0a             |
    | xor r10d, dword [r11 + 1 * rcx]              | 45 33 14 0b             |
    | xor r11d, dword [r12 + 1 * rcx]              | 45 33 1c 0c             |
    | xor r12d, dword [r13 + 1 * rcx]              | 45 33 64 0d 00          |
    | xor r13d, dword [r14 + 1 * rcx]              | 45 33 2c 0e             |
    | xor r14d, dword [r15 + 1 * rcx]              | 45 33 34 0f             |
    | xor r15d, dword [rax + 1 * rax]              | 44 33 3c 00             |
    | xor ecx, dword [rax + 1 * rbx]               | 33 0c 18                |
    | xor edx, dword [rax + 1 * rbp]               | 33 14 28                |
    | xor ebx, dword [rax + 1 * rsi]               | 33 1c 30                |
    | xor esp, dword [rax + 1 * rdi]               | 33 24 38                |
    | xor ebp, dword [rax + 1 * r8]                | 42 33 2c 00             |
    | xor esi, dword [rax + 1 * r9]                | 42 33 34 08             |
    | xor edi, dword [rax + 1 * r10]               | 42 33 3c 10             |
    | xor r8d, dword [rax + 1 * r11]               | 46 33 04 18             |
    | xor r9d, dword [rax + 1 * r12]               | 46 33 0c 20             |
    | xor r10d, dword [rax + 1 * r13]              | 46 33 14 28             |
    | xor r11d, dword [rax + 1 * r14]              | 46 33 1c 30             |
    | xor r12d, dword [rax + 1 * r15]              | 46 33 24 38             |
    | xor r13d, dword [rax + 2 * rcx]              | 44 33 2c 48             |
    | xor r14d, dword [rax + 4 * rcx]              | 44 33 34 88             |
    | xor r15d, dword [rax + 8 * rcx]              | 44 33 3c c8             |
    | xor ecx, dword [r8 + 2 * r9]                 | 43 33 0c 48             |
    | xor edx, dword [r8 + 4 * r9]                 | 43 33 14 88             |
    | xor ebx, dword [r8 + 8 * r9]                 | 43 33 1c c8             |
    | xor esp, dword [1 * rcx]                     | 33 24 0d 00 00 00 00    |
    | xor ebp, dword [2 * rcx]                     | 33 2c 4d 00 00 00 00    |
    | xor esi, dword [4 * rcx]                     | 33 34 8d 00 00 00 00    |
    | xor edi, dword [8 * rcx]                     | 33 3c cd 00 00 00 00    |
    | xor r8d, dword [1 * r9]                      | 46 33 04 0d 00 00 00 00 |
    | xor r9d, dword [2 * r9]                      | 46 33 0c 4d 00 00 00 00 |
    | xor r10d, dword [4 * r9]                     | 46 33 14 8d 00 00 00 00 |
    | xor r11d, dword [8 * r9]                     | 46 33 1c cd 00 00 00 00 |
    | xor r12d, dword [r13 + 8 * r12]              | 47 33 64 e5 00          |
    | xor r13d, dword [rsp + 4 * r15]              | 46 33 2c bc             |
    | xor r14d, dword [rax + 1 * rcx + 0x00]       | 44 33 74 08 00          |
    | xor r15d, dword [rax + 1 * rcx - 0x00]       | 44 33 7c 08 00          |
    | xor ecx, dword [rax + 1 * rcx - 0x01]        | 33 4c 08 ff             |
    | xor edx, dword [rax + 1 * rcx + 0x00000001]  | 33 94 08 01 00 00 00    |
    | xor ebx, dword [rax + 1 * rcx - 0x00000001]  | 33 9c 08 ff ff ff ff    |
    | xor esp, dword [rax + 1 * rcx + 0x7f]        | 33 64 08 7f             |
    | xor ebp, dword [rax + 1 * rcx - 0x7f]        | 33 6c 08 81             |
    | xor esi, dword [rax + 1 * rcx + 0x80]        | 33 b4 08 80 00 00 00    |
    | xor edi, dword [rax + 1 * rcx - 0x80]        | 33 7c 08 80             |
    | xor r8d, dword [rax + 1 * rcx - 0x81]        | 44 33 84 08 7f ff ff ff |
    | xor r9d, dword [rax + 1 * rcx + 0xff]        | 44 33 8c 08 ff 00 00 00 |
    | xor r10d, dword [rax + 1 * rcx - 0xff]       | 44 33 94 08 01 ff ff ff |
    | xor r11d, dword [rax + 1 * rcx + 0x7fffffff] | 44 33 9c 08 ff ff ff 7f |
    | xor r12d, dword [rax + 1 * rcx - 0x7fffffff] | 44 33 a4 08 01 00 00 80 |
    | xor r13d, dword [rax + 1 * rcx - 0x80000000] | 44 33 ac 08 00 00 00 80 |
    | xor r14d, dword [r10 + 0x7f]                 | 45 33 72 7f             |
    | xor r15d, dword [r10 + 0x80]                 | 45 33 ba 80 00 00 00    |
    | xor ecx, dword [r10 - 0x81]                  | 41 33 8a 7f ff ff ff    |
    | xor edx, dword [rax]                         | 33 10                   |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_xor_reg32_addr32():
    encode(XOR_REG32_ADDR32)


XOR_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | xor ax, 0x01   | 66 83 f0 01    | *** | xor ax, 0x00   | 66 83 f0 00    |
    | xor cx, 0x01   | 66 83 f1 01    | *** | xor ax, 0x7f   | 66 83 f0 7f    |
    | xor dx, 0x01   | 66 83 f2 01    | *** | xor ax, 0x80   | 66 83 f0 80    |
    | xor bx, 0x01   | 66 83 f3 01    | *** | xor ax, 0xff   | 66 83 f0 ff    |
    | xor sp, 0x01   | 66 83 f4 01    | *** | xor cx, 0x7f   | 66 83 f1 7f    |
    | xor bp, 0x01   | 66 83 f5 01    | *** | xor dx, 0x80   | 66 83 f2 80    |
    | xor si, 0x01   | 66 83 f6 01    | *** | xor bx, 0xff   | 66 83 f3 ff    |
    | xor di, 0x01   | 66 83 f7 01    | *** | xor sp, 0x00   | 66 83 f4 00    |
    | xor r8w, 0x01  | 66 41 83 f0 01 | *** | xor si, 0x7f   | 66 83 f6 7f    |
    | xor r9w, 0x01  | 66 41 83 f1 01 | *** | xor di, 0x80   | 66 83 f7 80    |
    | xor r10w, 0x01 | 66 41 83 f2 01 | *** | xor r8w, 0xff  | 66 41 83 f0 ff |
    | xor r11w, 0x01 | 66 41 83 f3 01 | *** | xor r9w, 0x00  | 66 41 83 f1 00 |
    | xor r12w, 0x01 | 66 41 83 f4 01 | *** | xor r11w, 0x7f | 66 41 83 f3 7f |
    | xor r13w, 0x01 | 66 41 83 f5 01 | *** | xor r12w, 0x80 | 66 41 83 f4 80 |
    | xor r14w, 0x01 | 66 41 83 f6 01 | *** | xor r13w, 0xff | 66 41 83 f5 ff |
    | xor r15w, 0x01 | 66 41 83 f7 01 | *** | xor r14w, 0x00 | 66 41 83 f6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_xor_reg16_imm8():
    encode(XOR_REG16_IMM8)


XOR_REG16_IMM16 = """
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | instruction      | encoding          | *** | instruction      | encoding          |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | xor ax, 0x0001   | 66 35 01 00       | *** | xor ax, 0x00ff   | 66 35 ff 00       |
    | xor cx, 0x0001   | 66 81 f1 01 00    | *** | xor ax, 0x0100   | 66 35 00 01       |
    | xor dx, 0x0001   | 66 81 f2 01 00    | *** | xor ax, 0x7fff   | 66 35 ff 7f       |
    | xor bx, 0x0001   | 66 81 f3 01 00    | *** | xor ax, 0x8000   | 66 35 00 80       |
    | xor sp, 0x0001   | 66 81 f4 01 00    | *** | xor ax, 0xffff   | 66 35 ff ff       |
    | xor bp, 0x0001   | 66 81 f5 01 00    | *** | xor cx, 0x007f   | 66 81 f1 7f 00    |
    | xor si, 0x0001   | 66 81 f6 01 00    | *** | xor dx, 0x0080   | 66 81 f2 80 00    |
    | xor di, 0x0001   | 66 81 f7 01 00    | *** | xor bx, 0x00ff   | 66 81 f3 ff 00    |
    | xor r8w, 0x0001  | 66 41 81 f0 01 00 | *** | xor sp, 0x0100   | 66 81 f4 00 01    |
    | xor r9w, 0x0001  | 66 41 81 f1 01 00 | *** | xor bp, 0x7fff   | 66 81 f5 ff 7f    |
    | xor r10w, 0x0001 | 66 41 81 f2 01 00 | *** | xor si, 0x8000   | 66 81 f6 00 80    |
    | xor r11w, 0x0001 | 66 41 81 f3 01 00 | *** | xor di, 0xffff   | 66 81 f7 ff ff    |
    | xor r12w, 0x0001 | 66 41 81 f4 01 00 | *** | xor r8w, 0x0000  | 66 41 81 f0 00 00 |
    | xor r13w, 0x0001 | 66 41 81 f5 01 00 | *** | xor r10w, 0x007f | 66 41 81 f2 7f 00 |
    | xor r14w, 0x0001 | 66 41 81 f6 01 00 | *** | xor r11w, 0x0080 | 66 41 81 f3 80 00 |
    | xor r15w, 0x0001 | 66 41 81 f7 01 00 | *** | xor r12w, 0x00ff | 66 41 81 f4 ff 00 |
    | xor ax, 0x0000   | 66 35 00 00       | *** | xor r13w, 0x0100 | 66 41 81 f5 00 01 |
    | xor ax, 0x007f   | 66 35 7f 00       | *** | xor r14w, 0x7fff | 66 41 81 f6 ff 7f |
    | xor ax, 0x0080   | 66 35 80 00       | *** | xor r15w, 0x8000 | 66 41 81 f7 00 80 |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
"""


def can_encode_xor_reg16_imm16():
    encode(XOR_REG16_IMM16)


XOR_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | xor ax, cx     | 66 31 c8    | *** | xor ax, r8w    | 66 44 31 c0 |
    | xor cx, cx     | 66 31 c9    | *** | xor ax, r9w    | 66 44 31 c8 |
    | xor dx, cx     | 66 31 ca    | *** | xor ax, r10w   | 66 44 31 d0 |
    | xor bx, cx     | 66 31 cb    | *** | xor ax, r11w   | 66 44 31 d8 |
    | xor sp, cx     | 66 31 cc    | *** | xor ax, r12w   | 66 44 31 e0 |
    | xor bp, cx     | 66 31 cd    | *** | xor ax, r13w   | 66 44 31 e8 |
    | xor si, cx     | 66 31 ce    | *** | xor ax, r14w   | 66 44 31 f0 |
    | xor di, cx     | 66 31 cf    | *** | xor ax, r15w   | 66 44 31 f8 |
    | xor r8w, cx    | 66 41 31 c8 | *** | xor cx, dx     | 66 31 d1    |
    | xor r9w, cx    | 66 41 31 c9 | *** | xor dx, bx     | 66 31 da    |
    | xor r10w, cx   | 66 41 31 ca | *** | xor bx, sp     | 66 31 e3    |
    | xor r11w, cx   | 66 41 31 cb | *** | xor sp, bp     | 66 31 ec    |
    | xor r12w, cx   | 66 41 31 cc | *** | xor bp, si     | 66 31 f5    |
    | xor r13w, cx   | 66 41 31 cd | *** | xor si, di     | 66 31 fe    |
    | xor r14w, cx   | 66 41 31 ce | *** | xor di, r8w    | 66 44 31 c7 |
    | xor r15w, cx   | 66 41 31 cf | *** | xor r8w, r9w   | 66 45 31 c8 |
    | xor ax, ax     | 66 31 c0    | *** | xor r9w, r10w  | 66 45 31 d1 |
    | xor ax, dx     | 66 31 d0    | *** | xor r10w, r11w | 66 45 31 da |
    | xor ax, bx     | 66 31 d8    | *** | xor r11w, r12w | 66 45 31 e3 |
    | xor ax, sp     | 66 31 e0    | *** | xor r12w, r13w | 66 45 31 ec |
    | xor ax, bp     | 66 31 e8    | *** | xor r13w, r14w | 66 45 31 f5 |
    | xor ax, si     | 66 31 f0    | *** | xor r14w, r15w | 66 45 31 fe |
    | xor ax, di     | 66 31 f8    | *** | xor r15w, ax   | 66 41 31 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_xor_reg16_reg16():
    encode(XOR_REG16_REG16)


XOR_REG16_ADDR16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | xor ax, word [rcx]                          | 66 33 01                   |
    | xor cx, word [rcx]                          | 66 33 09                   |
    | xor dx, word [rcx]                          | 66 33 11                   |
    | xor bx, word [rcx]                          | 66 33 19                   |
    | xor sp, word [rcx]                          | 66 33 21                   |
    | xor bp, word [rcx]                          | 66 33 29                   |
    | xor si, word [rcx]                          | 66 33 31                   |
    | xor di, word [rcx]                          | 66 33 39                   |
    | xor r8w, word [rcx]                         | 66 44 33 01                |
    | xor r9w, word [rcx]                         | 66 44 33 09                |
    | xor r10w, word [rcx]                        | 66 44 33 11                |
    | xor r11w, word [rcx]                        | 66 44 33 19                |
    | xor r12w, word [rcx]                        | 66 44 33 21                |
    | xor r13w, word [rcx]                        | 66 44 33 29                |
    | xor r14w, word [rcx]                        | 66 44 33 31                |
    | xor r15w, word [rcx]                        | 66 44 33 39                |
    | xor ax, word [rax]                          | 66 33 00                   |
    | xor ax, word [rdx]                          | 66 33 02                   |
    | xor ax, word [rbx]                          | 66 33 03                   |
    | xor ax, word [rsp]                          | 66 33 04 24                |
    | xor ax, word [rbp]                          | 66 33 45 00                |
    | xor ax, word [rsi]                          | 66 33 06                   |
    | xor ax, word [rdi]                          | 66 33 07                   |
    | xor ax, word [r8]                           | 66 41 33 00                |
    | xor ax, word [r9]                           | 66 41 33 01                |
    | xor ax, word [r10]                          | 66 41 33 02                |
    | xor ax, word [r11]                          | 66 41 33 03                |
    | xor ax, word [r12]                          | 66 41 33 04 24             |
    | xor ax, word [r13]                          | 66 41 33 45 00             |
    | xor ax, word [r14]                          | 66 41 33 06                |
    | xor ax, word [r15]                          | 66 41 33 07                |
    | xor ax, word [rax + 1 * rcx]                | 66 33 04 08                |
    | xor ax, word [rcx + 1 * rcx]                | 66 33 04 09                |
    | xor ax, word [rdx + 1 * rcx]                | 66 33 04 0a                |
    | xor ax, word [rbx + 1 * rcx]                | 66 33 04 0b                |
    | xor ax, word [rsp + 1 * rcx]                | 66 33 04 0c                |
    | xor ax, word [rbp + 1 * rcx]                | 66 33 44 0d 00             |
    | xor ax, word [rsi + 1 * rcx]                | 66 33 04 0e                |
    | xor ax, word [rdi + 1 * rcx]                | 66 33 04 0f                |
    | xor ax, word [r8 + 1 * rcx]                 | 66 41 33 04 08             |
    | xor ax, word [r9 + 1 * rcx]                 | 66 41 33 04 09             |
    | xor ax, word [r10 + 1 * rcx]                | 66 41 33 04 0a             |
    | xor ax, word [r11 + 1 * rcx]                | 66 41 33 04 0b             |
    | xor ax, word [r12 + 1 * rcx]                | 66 41 33 04 0c             |
    | xor ax, word [r13 + 1 * rcx]                | 66 41 33 44 0d 00          |
    | xor ax, word [r14 + 1 * rcx]                | 66 41 33 04 0e             |
    | xor ax, word [r15 + 1 * rcx]                | 66 41 33 04 0f             |
    | xor ax, word [rax + 1 * rax]                | 66 33 04 00                |
    | xor ax, word [rax + 1 * rdx]                | 66 33 04 10                |
    | xor ax, word [rax + 1 * rbx]                | 66 33 04 18                |
    | xor ax, word [rax + 1 * rbp]                | 66 33 04 28                |
    | xor ax, word [rax + 1 * rsi]                | 66 33 04 30                |
    | xor ax, word [rax + 1 * rdi]                | 66 33 04 38                |
    | xor ax, word [rax + 1 * r8]                 | 66 42 33 04 00             |
    | xor ax, word [rax + 1 * r9]                 | 66 42 33 04 08             |
    | xor ax, word [rax + 1 * r10]                | 66 42 33 04 10             |
    | xor ax, word [rax + 1 * r11]                | 66 42 33 04 18             |
    | xor ax, word [rax + 1 * r12]                | 66 42 33 04 20             |
    | xor ax, word [rax + 1 * r13]                | 66 42 33 04 28             |
    | xor ax, word [rax + 1 * r14]                | 66 42 33 04 30             |
    | xor ax, word [rax + 1 * r15]                | 66 42 33 04 38             |
    | xor ax, word [rax + 2 * rcx]                | 66 33 04 48                |
    | xor ax, word [rax + 4 * rcx]                | 66 33 04 88                |
    | xor ax, word [rax + 8 * rcx]                | 66 33 04 c8                |
    | xor ax, word [r8 + 1 * r9]                  | 66 43 33 04 08             |
    | xor ax, word [r8 + 2 * r9]                  | 66 43 33 04 48             |
    | xor ax, word [r8 + 4 * r9]                  | 66 43 33 04 88             |
    | xor ax, word [r8 + 8 * r9]                  | 66 43 33 04 c8             |
    | xor ax, word [1 * rcx]                      | 66 33 04 0d 00 00 00 00    |
    | xor ax, word [2 * rcx]                      | 66 33 04 4d 00 00 00 00    |
    | xor ax, word [4 * rcx]                      | 66 33 04 8d 00 00 00 00    |
    | xor ax, word [8 * rcx]                      | 66 33 04 cd 00 00 00 00    |
    | xor ax, word [1 * r9]                       | 66 42 33 04 0d 00 00 00 00 |
    | xor ax, word [2 * r9]                       | 66 42 33 04 4d 00 00 00 00 |
    | xor ax, word [4 * r9]                       | 66 42 33 04 8d 00 00 00 00 |
    | xor ax, word [8 * r9]                       | 66 42 33 04 cd 00 00 00 00 |
    | xor ax, word [r13 + 8 * r12]                | 66 43 33 44 e5 00          |
    | xor ax, word [rsp + 4 * r15]                | 66 42 33 04 bc             |
    | xor ax, word [rax + 1 * rcx + 0x00]         | 66 33 44 08 00             |
    | xor ax, word [rax + 1 * rcx - 0x00]         | 66 33 44 08 00             |
    | xor ax, word [rax + 1 * rcx + 0x01]         | 66 33 44 08 01             |
    | xor ax, word [rax + 1 * rcx - 0x01]         | 66 33 44 08 ff             |
    | xor ax, word [rax + 1 * rcx + 0x00000001]   | 66 33 84 08 01 00 00 00    |
    | xor ax, word [rax + 1 * rcx - 0x00000001]   | 66 33 84 08 ff ff ff ff    |
    | xor ax, word [rax + 1 * rcx + 0x7f]         | 66 33 44 08 7f             |
    | xor ax, word [rax + 1 * rcx - 0x7f]         | 66 33 44 08 81             |
    | xor ax, word [rax + 1 * rcx + 0x80]         | 66 33 84 08 80 00 00 00    |
    | xor ax, word [rax + 1 * rcx - 0x80]         | 66 33 44 08 80             |
    | xor ax, word [rax + 1 * rcx - 0x81]         | 66 33 84 08 7f ff ff ff    |
    | xor ax, word [rax + 1 * rcx + 0xff]         | 66 33 84 08 ff 00 00 00    |
    | xor ax, word [rax + 1 * rcx - 0xff]         | 66 33 84 08 01 ff ff ff    |
    | xor ax, word [rax + 1 * rcx + 0x7fffffff]   | 66 33 84 08 ff ff ff 7f    |
    | xor ax, word [rax + 1 * rcx - 0x7fffffff]   | 66 33 84 08 01 00 00 80    |
    | xor ax, word [rax + 1 * rcx - 0x80000000]   | 66 33 84 08 00 00 00 80    |
    | xor ax, word [r10 + 0x7f]                   | 66 41 33 42 7f             |
    | xor ax, word [r10 + 0x80]                   | 66 41 33 82 80 00 00 00    |
    | xor ax, word [r10 - 0x80]                   | 66 41 33 42 80             |
    | xor ax, word [r10 - 0x81]                   | 66 41 33 82 7f ff ff ff    |
    | xor cx, word [rdx]                          | 66 33 0a                   |
    | xor dx, word [rbx]                          | 66 33 13                   |
    | xor bx, word [rsp]                          | 66 33 1c 24                |
    | xor sp, word [rbp]                          | 66 33 65 00                |
    | xor bp, word [rsi]                          | 66 33 2e                   |
    | xor si, word [rdi]                          | 66 33 37                   |
    | xor di, word [r8]                           | 66 41 33 38                |
    | xor r8w, word [r9]                          | 66 45 33 01                |
    | xor r9w, word [r10]                         | 66 45 33 0a                |
    | xor r10w, word [r11]                        | 66 45 33 13                |
    | xor r11w, word [r12]                        | 66 45 33 1c 24             |
    | xor r12w, word [r13]                        | 66 45 33 65 00             |
    | xor r13w, word [r14]                        | 66 45 33 2e                |
    | xor r14w, word [r15]                        | 66 45 33 37                |
    | xor r15w, word [rax + 1 * rcx]              | 66 44 33 3c 08             |
    | xor cx, word [rdx + 1 * rcx]                | 66 33 0c 0a                |
    | xor dx, word [rbx + 1 * rcx]                | 66 33 14 0b                |
    | xor bx, word [rsp + 1 * rcx]                | 66 33 1c 0c                |
    | xor sp, word [rbp + 1 * rcx]                | 66 33 64 0d 00             |
    | xor bp, word [rsi + 1 * rcx]                | 66 33 2c 0e                |
    | xor si, word [rdi + 1 * rcx]                | 66 33 34 0f                |
    | xor di, word [r8 + 1 * rcx]                 | 66 41 33 3c 08             |
    | xor r8w, word [r9 + 1 * rcx]                | 66 45 33 04 09             |
    | xor r9w, word [r10 + 1 * rcx]               | 66 45 33 0c 0a             |
    | xor r10w, word [r11 + 1 * rcx]              | 66 45 33 14 0b             |
    | xor r11w, word [r12 + 1 * rcx]              | 66 45 33 1c 0c             |
    | xor r12w, word [r13 + 1 * rcx]              | 66 45 33 64 0d 00          |
    | xor r13w, word [r14 + 1 * rcx]              | 66 45 33 2c 0e             |
    | xor r14w, word [r15 + 1 * rcx]              | 66 45 33 34 0f             |
    | xor r15w, word [rax + 1 * rax]              | 66 44 33 3c 00             |
    | xor cx, word [rax + 1 * rbx]                | 66 33 0c 18                |
    | xor dx, word [rax + 1 * rbp]                | 66 33 14 28                |
    | xor bx, word [rax + 1 * rsi]                | 66 33 1c 30                |
    | xor sp, word [rax + 1 * rdi]                | 66 33 24 38                |
    | xor bp, word [rax + 1 * r8]                 | 66 42 33 2c 00             |
    | xor si, word [rax + 1 * r9]                 | 66 42 33 34 08             |
    | xor di, word [rax + 1 * r10]                | 66 42 33 3c 10             |
    | xor r8w, word [rax + 1 * r11]               | 66 46 33 04 18             |
    | xor r9w, word [rax + 1 * r12]               | 66 46 33 0c 20             |
    | xor r10w, word [rax + 1 * r13]              | 66 46 33 14 28             |
    | xor r11w, word [rax + 1 * r14]              | 66 46 33 1c 30             |
    | xor r12w, word [rax + 1 * r15]              | 66 46 33 24 38             |
    | xor r13w, word [rax + 2 * rcx]              | 66 44 33 2c 48             |
    | xor r14w, word [rax + 4 * rcx]              | 66 44 33 34 88             |
    | xor r15w, word [rax + 8 * rcx]              | 66 44 33 3c c8             |
    | xor cx, word [r8 + 2 * r9]                  | 66 43 33 0c 48             |
    | xor dx, word [r8 + 4 * r9]                  | 66 43 33 14 88             |
    | xor bx, word [r8 + 8 * r9]                  | 66 43 33 1c c8             |
    | xor sp, word [1 * rcx]                      | 66 33 24 0d 00 00 00 00    |
    | xor bp, word [2 * rcx]                      | 66 33 2c 4d 00 00 00 00    |
    | xor si, word [4 * rcx]                      | 66 33 34 8d 00 00 00 00    |
    | xor di, word [8 * rcx]                      | 66 33 3c cd 00 00 00 00    |
    | xor r8w, word [1 * r9]                      | 66 46 33 04 0d 00 00 00 00 |
    | xor r9w, word [2 * r9]                      | 66 46 33 0c 4d 00 00 00 00 |
    | xor r10w, word [4 * r9]                     | 66 46 33 14 8d 00 00 00 00 |
    | xor r11w, word [8 * r9]                     | 66 46 33 1c cd 00 00 00 00 |
    | xor r12w, word [r13 + 8 * r12]              | 66 47 33 64 e5 00          |
    | xor r13w, word [rsp + 4 * r15]              | 66 46 33 2c bc             |
    | xor r14w, word [rax + 1 * rcx + 0x00]       | 66 44 33 74 08 00          |
    | xor r15w, word [rax + 1 * rcx - 0x00]       | 66 44 33 7c 08 00          |
    | xor cx, word [rax + 1 * rcx - 0x01]         | 66 33 4c 08 ff             |
    | xor dx, word [rax + 1 * rcx + 0x00000001]   | 66 33 94 08 01 00 00 00    |
    | xor bx, word [rax + 1 * rcx - 0x00000001]   | 66 33 9c 08 ff ff ff ff    |
    | xor sp, word [rax + 1 * rcx + 0x7f]         | 66 33 64 08 7f             |
    | xor bp, word [rax + 1 * rcx - 0x7f]         | 66 33 6c 08 81             |
    | xor si, word [rax + 1 * rcx + 0x80]         | 66 33 b4 08 80 00 00 00    |
    | xor di, word [rax + 1 * rcx - 0x80]         | 66 33 7c 08 80             |
    | xor r8w, word [rax + 1 * rcx - 0x81]        | 66 44 33 84 08 7f ff ff ff |
    | xor r9w, word [rax + 1 * rcx + 0xff]        | 66 44 33 8c 08 ff 00 00 00 |
    | xor r10w, word [rax + 1 * rcx - 0xff]       | 66 44 33 94 08 01 ff ff ff |
    | xor r11w, word [rax + 1 * rcx + 0x7fffffff] | 66 44 33 9c 08 ff ff ff 7f |
    | xor r12w, word [rax + 1 * rcx - 0x7fffffff] | 66 44 33 a4 08 01 00 00 80 |
    | xor r13w, word [rax + 1 * rcx - 0x80000000] | 66 44 33 ac 08 00 00 00 80 |
    | xor r14w, word [r10 + 0x7f]                 | 66 45 33 72 7f             |
    | xor r15w, word [r10 + 0x80]                 | 66 45 33 ba 80 00 00 00    |
    | xor cx, word [r10 - 0x81]                   | 66 41 33 8a 7f ff ff ff    |
    | xor dx, word [rax]                          | 66 33 10                   |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_xor_reg16_addr16():
    encode(XOR_REG16_ADDR16)


XOR_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | xor al, 0x01   | 34 01       | *** | xor al, 0x00   | 34 00       |
    | xor cl, 0x01   | 80 f1 01    | *** | xor al, 0x7f   | 34 7f       |
    | xor dl, 0x01   | 80 f2 01    | *** | xor al, 0x80   | 34 80       |
    | xor bl, 0x01   | 80 f3 01    | *** | xor al, 0xff   | 34 ff       |
    | xor spl, 0x01  | 40 80 f4 01 | *** | xor cl, 0x7f   | 80 f1 7f    |
    | xor bpl, 0x01  | 40 80 f5 01 | *** | xor dl, 0x80   | 80 f2 80    |
    | xor sil, 0x01  | 40 80 f6 01 | *** | xor bl, 0xff   | 80 f3 ff    |
    | xor dil, 0x01  | 40 80 f7 01 | *** | xor spl, 0x00  | 40 80 f4 00 |
    | xor r8b, 0x01  | 41 80 f0 01 | *** | xor sil, 0x7f  | 40 80 f6 7f |
    | xor r9b, 0x01  | 41 80 f1 01 | *** | xor dil, 0x80  | 40 80 f7 80 |
    | xor r10b, 0x01 | 41 80 f2 01 | *** | xor r8b, 0xff  | 41 80 f0 ff |
    | xor r11b, 0x01 | 41 80 f3 01 | *** | xor r9b, 0x00  | 41 80 f1 00 |
    | xor r12b, 0x01 | 41 80 f4 01 | *** | xor r11b, 0x7f | 41 80 f3 7f |
    | xor r13b, 0x01 | 41 80 f5 01 | *** | xor r12b, 0x80 | 41 80 f4 80 |
    | xor r14b, 0x01 | 41 80 f6 01 | *** | xor r13b, 0xff | 41 80 f5 ff |
    | xor r15b, 0x01 | 41 80 f7 01 | *** | xor r14b, 0x00 | 41 80 f6 00 |
    | xor ah, 0x01   | 80 f4 01    | *** | xor ah, 0x7f   | 80 f4 7f    |
    | xor ch, 0x01   | 80 f5 01    | *** | xor ch, 0x80   | 80 f5 80    |
    | xor dh, 0x01   | 80 f6 01    | *** | xor dh, 0xff   | 80 f6 ff    |
    | xor bh, 0x01   | 80 f7 01    | *** | xor bh, 0x00   | 80 f7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_xor_reg8_imm8():
    encode(XOR_REG8_IMM8)


XOR_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | xor al, cl     | 30 c8    | *** | xor al, r10b   | 44 30 d0 |
    | xor cl, cl     | 30 c9    | *** | xor al, r11b   | 44 30 d8 |
    | xor dl, cl     | 30 ca    | *** | xor al, r12b   | 44 30 e0 |
    | xor bl, cl     | 30 cb    | *** | xor al, r13b   | 44 30 e8 |
    | xor spl, cl    | 40 30 cc | *** | xor al, r14b   | 44 30 f0 |
    | xor bpl, cl    | 40 30 cd | *** | xor al, r15b   | 44 30 f8 |
    | xor sil, cl    | 40 30 ce | *** | xor al, ah     | 30 e0    |
    | xor dil, cl    | 40 30 cf | *** | xor al, ch     | 30 e8    |
    | xor r8b, cl    | 41 30 c8 | *** | xor al, dh     | 30 f0    |
    | xor r9b, cl    | 41 30 c9 | *** | xor al, bh     | 30 f8    |
    | xor r10b, cl   | 41 30 ca | *** | xor cl, dl     | 30 d1    |
    | xor r11b, cl   | 41 30 cb | *** | xor dl, bl     | 30 da    |
    | xor r12b, cl   | 41 30 cc | *** | xor bl, spl    | 40 30 e3 |
    | xor r13b, cl   | 41 30 cd | *** | xor spl, bpl   | 40 30 ec |
    | xor r14b, cl   | 41 30 ce | *** | xor bpl, sil   | 40 30 f5 |
    | xor r15b, cl   | 41 30 cf | *** | xor sil, dil   | 40 30 fe |
    | xor ah, cl     | 30 cc    | *** | xor dil, r8b   | 44 30 c7 |
    | xor ch, cl     | 30 cd    | *** | xor r8b, r9b   | 45 30 c8 |
    | xor dh, cl     | 30 ce    | *** | xor r9b, r10b  | 45 30 d1 |
    | xor bh, cl     | 30 cf    | *** | xor r10b, r11b | 45 30 da |
    | xor al, al     | 30 c0    | *** | xor r11b, r12b | 45 30 e3 |
    | xor al, dl     | 30 d0    | *** | xor r12b, r13b | 45 30 ec |
    | xor al, bl     | 30 d8    | *** | xor r13b, r14b | 45 30 f5 |
    | xor al, spl    | 40 30 e0 | *** | xor r14b, r15b | 45 30 fe |
    | xor al, bpl    | 40 30 e8 | *** | xor r15b, ah   | !! !! !! |
    | xor al, sil    | 40 30 f0 | *** | xor ah, ch     | 30 ec    |
    | xor al, dil    | 40 30 f8 | *** | xor ch, dh     | 30 f5    |
    | xor al, r8b    | 44 30 c0 | *** | xor dh, bh     | 30 fe    |
    | xor al, r9b    | 44 30 c8 | *** | xor bh, al     | 30 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_xor_reg8_reg8():
    encode(XOR_REG8_REG8)


XOR_REG8_ADDR8 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | xor al, byte [rcx]                          | 32 01                   |
    | xor cl, byte [rcx]                          | 32 09                   |
    | xor dl, byte [rcx]                          | 32 11                   |
    | xor bl, byte [rcx]                          | 32 19                   |
    | xor spl, byte [rcx]                         | 40 32 21                |
    | xor bpl, byte [rcx]                         | 40 32 29                |
    | xor sil, byte [rcx]                         | 40 32 31                |
    | xor dil, byte [rcx]                         | 40 32 39                |
    | xor r8b, byte [rcx]                         | 44 32 01                |
    | xor r9b, byte [rcx]                         | 44 32 09                |
    | xor r10b, byte [rcx]                        | 44 32 11                |
    | xor r11b, byte [rcx]                        | 44 32 19                |
    | xor r12b, byte [rcx]                        | 44 32 21                |
    | xor r13b, byte [rcx]                        | 44 32 29                |
    | xor r14b, byte [rcx]                        | 44 32 31                |
    | xor r15b, byte [rcx]                        | 44 32 39                |
    | xor ah, byte [rcx]                          | 32 21                   |
    | xor ch, byte [rcx]                          | 32 29                   |
    | xor dh, byte [rcx]                          | 32 31                   |
    | xor bh, byte [rcx]                          | 32 39                   |
    | xor al, byte [rax]                          | 32 00                   |
    | xor al, byte [rdx]                          | 32 02                   |
    | xor al, byte [rbx]                          | 32 03                   |
    | xor al, byte [rsp]                          | 32 04 24                |
    | xor al, byte [rbp]                          | 32 45 00                |
    | xor al, byte [rsi]                          | 32 06                   |
    | xor al, byte [rdi]                          | 32 07                   |
    | xor al, byte [r8]                           | 41 32 00                |
    | xor al, byte [r9]                           | 41 32 01                |
    | xor al, byte [r10]                          | 41 32 02                |
    | xor al, byte [r11]                          | 41 32 03                |
    | xor al, byte [r12]                          | 41 32 04 24             |
    | xor al, byte [r13]                          | 41 32 45 00             |
    | xor al, byte [r14]                          | 41 32 06                |
    | xor al, byte [r15]                          | 41 32 07                |
    | xor al, byte [rax + 1 * rcx]                | 32 04 08                |
    | xor al, byte [rcx + 1 * rcx]                | 32 04 09                |
    | xor al, byte [rdx + 1 * rcx]                | 32 04 0a                |
    | xor al, byte [rbx + 1 * rcx]                | 32 04 0b                |
    | xor al, byte [rsp + 1 * rcx]                | 32 04 0c                |
    | xor al, byte [rbp + 1 * rcx]                | 32 44 0d 00             |
    | xor al, byte [rsi + 1 * rcx]                | 32 04 0e                |
    | xor al, byte [rdi + 1 * rcx]                | 32 04 0f                |
    | xor al, byte [r8 + 1 * rcx]                 | 41 32 04 08             |
    | xor al, byte [r9 + 1 * rcx]                 | 41 32 04 09             |
    | xor al, byte [r10 + 1 * rcx]                | 41 32 04 0a             |
    | xor al, byte [r11 + 1 * rcx]                | 41 32 04 0b             |
    | xor al, byte [r12 + 1 * rcx]                | 41 32 04 0c             |
    | xor al, byte [r13 + 1 * rcx]                | 41 32 44 0d 00          |
    | xor al, byte [r14 + 1 * rcx]                | 41 32 04 0e             |
    | xor al, byte [r15 + 1 * rcx]                | 41 32 04 0f             |
    | xor al, byte [rax + 1 * rax]                | 32 04 00                |
    | xor al, byte [rax + 1 * rdx]                | 32 04 10                |
    | xor al, byte [rax + 1 * rbx]                | 32 04 18                |
    | xor al, byte [rax + 1 * rbp]                | 32 04 28                |
    | xor al, byte [rax + 1 * rsi]                | 32 04 30                |
    | xor al, byte [rax + 1 * rdi]                | 32 04 38                |
    | xor al, byte [rax + 1 * r8]                 | 42 32 04 00             |
    | xor al, byte [rax + 1 * r9]                 | 42 32 04 08             |
    | xor al, byte [rax + 1 * r10]                | 42 32 04 10             |
    | xor al, byte [rax + 1 * r11]                | 42 32 04 18             |
    | xor al, byte [rax + 1 * r12]                | 42 32 04 20             |
    | xor al, byte [rax + 1 * r13]                | 42 32 04 28             |
    | xor al, byte [rax + 1 * r14]                | 42 32 04 30             |
    | xor al, byte [rax + 1 * r15]                | 42 32 04 38             |
    | xor al, byte [rax + 2 * rcx]                | 32 04 48                |
    | xor al, byte [rax + 4 * rcx]                | 32 04 88                |
    | xor al, byte [rax + 8 * rcx]                | 32 04 c8                |
    | xor al, byte [r8 + 1 * r9]                  | 43 32 04 08             |
    | xor al, byte [r8 + 2 * r9]                  | 43 32 04 48             |
    | xor al, byte [r8 + 4 * r9]                  | 43 32 04 88             |
    | xor al, byte [r8 + 8 * r9]                  | 43 32 04 c8             |
    | xor al, byte [1 * rcx]                      | 32 04 0d 00 00 00 00    |
    | xor al, byte [2 * rcx]                      | 32 04 4d 00 00 00 00    |
    | xor al, byte [4 * rcx]                      | 32 04 8d 00 00 00 00    |
    | xor al, byte [8 * rcx]                      | 32 04 cd 00 00 00 00    |
    | xor al, byte [1 * r9]                       | 42 32 04 0d 00 00 00 00 |
    | xor al, byte [2 * r9]                       | 42 32 04 4d 00 00 00 00 |
    | xor al, byte [4 * r9]                       | 42 32 04 8d 00 00 00 00 |
    | xor al, byte [8 * r9]                       | 42 32 04 cd 00 00 00 00 |
    | xor al, byte [r13 + 8 * r12]                | 43 32 44 e5 00          |
    | xor al, byte [rsp + 4 * r15]                | 42 32 04 bc             |
    | xor al, byte [rax + 1 * rcx + 0x00]         | 32 44 08 00             |
    | xor al, byte [rax + 1 * rcx - 0x00]         | 32 44 08 00             |
    | xor al, byte [rax + 1 * rcx + 0x01]         | 32 44 08 01             |
    | xor al, byte [rax + 1 * rcx - 0x01]         | 32 44 08 ff             |
    | xor al, byte [rax + 1 * rcx + 0x00000001]   | 32 84 08 01 00 00 00    |
    | xor al, byte [rax + 1 * rcx - 0x00000001]   | 32 84 08 ff ff ff ff    |
    | xor al, byte [rax + 1 * rcx + 0x7f]         | 32 44 08 7f             |
    | xor al, byte [rax + 1 * rcx - 0x7f]         | 32 44 08 81             |
    | xor al, byte [rax + 1 * rcx + 0x80]         | 32 84 08 80 00 00 00    |
    | xor al, byte [rax + 1 * rcx - 0x80]         | 32 44 08 80             |
    | xor al, byte [rax + 1 * rcx - 0x81]         | 32 84 08 7f ff ff ff    |
    | xor al, byte [rax + 1 * rcx + 0xff]         | 32 84 08 ff 00 00 00    |
    | xor al, byte [rax + 1 * rcx - 0xff]         | 32 84 08 01 ff ff ff    |
    | xor al, byte [rax + 1 * rcx + 0x7fffffff]   | 32 84 08 ff ff ff 7f    |
    | xor al, byte [rax + 1 * rcx - 0x7fffffff]   | 32 84 08 01 00 00 80    |
    | xor al, byte [rax + 1 * rcx - 0x80000000]   | 32 84 08 00 00 00 80    |
    | xor al, byte [r10 + 0x7f]                   | 41 32 42 7f             |
    | xor al, byte [r10 + 0x80]                   | 41 32 82 80 00 00 00    |
    | xor al, byte [r10 - 0x80]                   | 41 32 42 80             |
    | xor al, byte [r10 - 0x81]                   | 41 32 82 7f ff ff ff    |
    | xor cl, byte [rdx]                          | 32 0a                   |
    | xor dl, byte [rbx]                          | 32 13                   |
    | xor bl, byte [rsp]                          | 32 1c 24                |
    | xor spl, byte [rbp]                         | 40 32 65 00             |
    | xor bpl, byte [rsi]                         | 40 32 2e                |
    | xor sil, byte [rdi]                         | 40 32 37                |
    | xor dil, byte [r8]                          | 41 32 38                |
    | xor r8b, byte [r9]                          | 45 32 01                |
    | xor r9b, byte [r10]                         | 45 32 0a                |
    | xor r10b, byte [r11]                        | 45 32 13                |
    | xor r11b, byte [r12]                        | 45 32 1c 24             |
    | xor r12b, byte [r13]                        | 45 32 65 00             |
    | xor r13b, byte [r14]                        | 45 32 2e                |
    | xor r14b, byte [r15]                        | 45 32 37                |
    | xor r15b, byte [rax + 1 * rcx]              | 44 32 3c 08             |
    | xor ah, byte [rcx + 1 * rcx]                | 32 24 09                |
    | xor ch, byte [rdx + 1 * rcx]                | 32 2c 0a                |
    | xor dh, byte [rbx + 1 * rcx]                | 32 34 0b                |
    | xor bh, byte [rsp + 1 * rcx]                | 32 3c 0c                |
    | xor cl, byte [rsi + 1 * rcx]                | 32 0c 0e                |
    | xor dl, byte [rdi + 1 * rcx]                | 32 14 0f                |
    | xor bl, byte [r8 + 1 * rcx]                 | 41 32 1c 08             |
    | xor spl, byte [r9 + 1 * rcx]                | 41 32 24 09             |
    | xor bpl, byte [r10 + 1 * rcx]               | 41 32 2c 0a             |
    | xor sil, byte [r11 + 1 * rcx]               | 41 32 34 0b             |
    | xor dil, byte [r12 + 1 * rcx]               | 41 32 3c 0c             |
    | xor r8b, byte [r13 + 1 * rcx]               | 45 32 44 0d 00          |
    | xor r9b, byte [r14 + 1 * rcx]               | 45 32 0c 0e             |
    | xor r10b, byte [r15 + 1 * rcx]              | 45 32 14 0f             |
    | xor r11b, byte [rax + 1 * rax]              | 44 32 1c 00             |
    | xor r12b, byte [rax + 1 * rdx]              | 44 32 24 10             |
    | xor r13b, byte [rax + 1 * rbx]              | 44 32 2c 18             |
    | xor r14b, byte [rax + 1 * rbp]              | 44 32 34 28             |
    | xor r15b, byte [rax + 1 * rsi]              | 44 32 3c 30             |
    | xor ah, byte [rax + 1 * rdi]                | 32 24 38                |
    | xor ch, byte [rax + 1 * r8]                 | !! !! !!                |
    | xor dh, byte [rax + 1 * r9]                 | !! !! !!                |
    | xor bh, byte [rax + 1 * r10]                | !! !! !!                |
    | xor cl, byte [rax + 1 * r12]                | 42 32 0c 20             |
    | xor dl, byte [rax + 1 * r13]                | 42 32 14 28             |
    | xor bl, byte [rax + 1 * r14]                | 42 32 1c 30             |
    | xor spl, byte [rax + 1 * r15]               | 42 32 24 38             |
    | xor bpl, byte [rax + 2 * rcx]               | 40 32 2c 48             |
    | xor sil, byte [rax + 4 * rcx]               | 40 32 34 88             |
    | xor dil, byte [rax + 8 * rcx]               | 40 32 3c c8             |
    | xor r8b, byte [r8 + 1 * r9]                 | 47 32 04 08             |
    | xor r9b, byte [r8 + 2 * r9]                 | 47 32 0c 48             |
    | xor r10b, byte [r8 + 4 * r9]                | 47 32 14 88             |
    | xor r11b, byte [r8 + 8 * r9]                | 47 32 1c c8             |
    | xor r12b, byte [1 * rcx]                    | 44 32 24 0d 00 00 00 00 |
    | xor r13b, byte [2 * rcx]                    | 44 32 2c 4d 00 00 00 00 |
    | xor r14b, byte [4 * rcx]                    | 44 32 34 8d 00 00 00 00 |
    | xor r15b, byte [8 * rcx]                    | 44 32 3c cd 00 00 00 00 |
    | xor ah, byte [1 * r9]                       | !! !! !!                |
    | xor ch, byte [2 * r9]                       | !! !! !!                |
    | xor dh, byte [4 * r9]                       | !! !! !!                |
    | xor bh, byte [8 * r9]                       | !! !! !!                |
    | xor cl, byte [rsp + 4 * r15]                | 42 32 0c bc             |
    | xor dl, byte [rax + 1 * rcx + 0x00]         | 32 54 08 00             |
    | xor bl, byte [rax + 1 * rcx - 0x00]         | 32 5c 08 00             |
    | xor spl, byte [rax + 1 * rcx + 0x01]        | 40 32 64 08 01          |
    | xor bpl, byte [rax + 1 * rcx - 0x01]        | 40 32 6c 08 ff          |
    | xor sil, byte [rax + 1 * rcx + 0x00000001]  | 40 32 b4 08 01 00 00 00 |
    | xor dil, byte [rax + 1 * rcx - 0x00000001]  | 40 32 bc 08 ff ff ff ff |
    | xor r8b, byte [rax + 1 * rcx + 0x7f]        | 44 32 44 08 7f          |
    | xor r9b, byte [rax + 1 * rcx - 0x7f]        | 44 32 4c 08 81          |
    | xor r10b, byte [rax + 1 * rcx + 0x80]       | 44 32 94 08 80 00 00 00 |
    | xor r11b, byte [rax + 1 * rcx - 0x80]       | 44 32 5c 08 80          |
    | xor r12b, byte [rax + 1 * rcx - 0x81]       | 44 32 a4 08 7f ff ff ff |
    | xor r13b, byte [rax + 1 * rcx + 0xff]       | 44 32 ac 08 ff 00 00 00 |
    | xor r14b, byte [rax + 1 * rcx - 0xff]       | 44 32 b4 08 01 ff ff ff |
    | xor r15b, byte [rax + 1 * rcx + 0x7fffffff] | 44 32 bc 08 ff ff ff 7f |
    | xor ah, byte [rax + 1 * rcx - 0x7fffffff]   | 32 a4 08 01 00 00 80    |
    | xor ch, byte [rax + 1 * rcx - 0x80000000]   | 32 ac 08 00 00 00 80    |
    | xor dh, byte [r10 + 0x7f]                   | !! !! !!                |
    | xor bh, byte [r10 + 0x80]                   | !! !! !!                |
    | xor cl, byte [r10 - 0x81]                   | 41 32 8a 7f ff ff ff    |
    | xor dl, byte [rax]                          | 32 10                   |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_xor_reg8_addr8():
    encode(XOR_REG8_ADDR8)


XOR_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | xor qword [rax], 0x01                        | 48 83 30 01                |
    | xor qword [rcx], 0x01                        | 48 83 31 01                |
    | xor qword [rdx], 0x01                        | 48 83 32 01                |
    | xor qword [rbx], 0x01                        | 48 83 33 01                |
    | xor qword [rsp], 0x01                        | 48 83 34 24 01             |
    | xor qword [rbp], 0x01                        | 48 83 75 00 01             |
    | xor qword [rsi], 0x01                        | 48 83 36 01                |
    | xor qword [rdi], 0x01                        | 48 83 37 01                |
    | xor qword [r8], 0x01                         | 49 83 30 01                |
    | xor qword [r9], 0x01                         | 49 83 31 01                |
    | xor qword [r10], 0x01                        | 49 83 32 01                |
    | xor qword [r11], 0x01                        | 49 83 33 01                |
    | xor qword [r12], 0x01                        | 49 83 34 24 01             |
    | xor qword [r13], 0x01                        | 49 83 75 00 01             |
    | xor qword [r14], 0x01                        | 49 83 36 01                |
    | xor qword [r15], 0x01                        | 49 83 37 01                |
    | xor qword [rax + 1 * rcx], 0x01              | 48 83 34 08 01             |
    | xor qword [rcx + 1 * rcx], 0x01              | 48 83 34 09 01             |
    | xor qword [rdx + 1 * rcx], 0x01              | 48 83 34 0a 01             |
    | xor qword [rbx + 1 * rcx], 0x01              | 48 83 34 0b 01             |
    | xor qword [rsp + 1 * rcx], 0x01              | 48 83 34 0c 01             |
    | xor qword [rbp + 1 * rcx], 0x01              | 48 83 74 0d 00 01          |
    | xor qword [rsi + 1 * rcx], 0x01              | 48 83 34 0e 01             |
    | xor qword [rdi + 1 * rcx], 0x01              | 48 83 34 0f 01             |
    | xor qword [r8 + 1 * rcx], 0x01               | 49 83 34 08 01             |
    | xor qword [r9 + 1 * rcx], 0x01               | 49 83 34 09 01             |
    | xor qword [r10 + 1 * rcx], 0x01              | 49 83 34 0a 01             |
    | xor qword [r11 + 1 * rcx], 0x01              | 49 83 34 0b 01             |
    | xor qword [r12 + 1 * rcx], 0x01              | 49 83 34 0c 01             |
    | xor qword [r13 + 1 * rcx], 0x01              | 49 83 74 0d 00 01          |
    | xor qword [r14 + 1 * rcx], 0x01              | 49 83 34 0e 01             |
    | xor qword [r15 + 1 * rcx], 0x01              | 49 83 34 0f 01             |
    | xor qword [rax + 1 * rax], 0x01              | 48 83 34 00 01             |
    | xor qword [rax + 1 * rdx], 0x01              | 48 83 34 10 01             |
    | xor qword [rax + 1 * rbx], 0x01              | 48 83 34 18 01             |
    | xor qword [rax + 1 * rbp], 0x01              | 48 83 34 28 01             |
    | xor qword [rax + 1 * rsi], 0x01              | 48 83 34 30 01             |
    | xor qword [rax + 1 * rdi], 0x01              | 48 83 34 38 01             |
    | xor qword [rax + 1 * r8], 0x01               | 4a 83 34 00 01             |
    | xor qword [rax + 1 * r9], 0x01               | 4a 83 34 08 01             |
    | xor qword [rax + 1 * r10], 0x01              | 4a 83 34 10 01             |
    | xor qword [rax + 1 * r11], 0x01              | 4a 83 34 18 01             |
    | xor qword [rax + 1 * r12], 0x01              | 4a 83 34 20 01             |
    | xor qword [rax + 1 * r13], 0x01              | 4a 83 34 28 01             |
    | xor qword [rax + 1 * r14], 0x01              | 4a 83 34 30 01             |
    | xor qword [rax + 1 * r15], 0x01              | 4a 83 34 38 01             |
    | xor qword [rax + 2 * rcx], 0x01              | 48 83 34 48 01             |
    | xor qword [rax + 4 * rcx], 0x01              | 48 83 34 88 01             |
    | xor qword [rax + 8 * rcx], 0x01              | 48 83 34 c8 01             |
    | xor qword [r8 + 1 * r9], 0x01                | 4b 83 34 08 01             |
    | xor qword [r8 + 2 * r9], 0x01                | 4b 83 34 48 01             |
    | xor qword [r8 + 4 * r9], 0x01                | 4b 83 34 88 01             |
    | xor qword [r8 + 8 * r9], 0x01                | 4b 83 34 c8 01             |
    | xor qword [1 * rcx], 0x01                    | 48 83 34 0d 00 00 00 00 01 |
    | xor qword [2 * rcx], 0x01                    | 48 83 34 4d 00 00 00 00 01 |
    | xor qword [4 * rcx], 0x01                    | 48 83 34 8d 00 00 00 00 01 |
    | xor qword [8 * rcx], 0x01                    | 48 83 34 cd 00 00 00 00 01 |
    | xor qword [1 * r9], 0x01                     | 4a 83 34 0d 00 00 00 00 01 |
    | xor qword [2 * r9], 0x01                     | 4a 83 34 4d 00 00 00 00 01 |
    | xor qword [4 * r9], 0x01                     | 4a 83 34 8d 00 00 00 00 01 |
    | xor qword [8 * r9], 0x01                     | 4a 83 34 cd 00 00 00 00 01 |
    | xor qword [r13 + 8 * r12], 0x01              | 4b 83 74 e5 00 01          |
    | xor qword [rsp + 4 * r15], 0x01              | 4a 83 34 bc 01             |
    | xor qword [rax + 1 * rcx + 0x00], 0x01       | 48 83 74 08 00 01          |
    | xor qword [rax + 1 * rcx - 0x00], 0x01       | 48 83 74 08 00 01          |
    | xor qword [rax + 1 * rcx + 0x01], 0x01       | 48 83 74 08 01 01          |
    | xor qword [rax + 1 * rcx - 0x01], 0x01       | 48 83 74 08 ff 01          |
    | xor qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 83 b4 08 01 00 00 00 01 |
    | xor qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 83 b4 08 ff ff ff ff 01 |
    | xor qword [rax + 1 * rcx + 0x7f], 0x01       | 48 83 74 08 7f 01          |
    | xor qword [rax + 1 * rcx - 0x7f], 0x01       | 48 83 74 08 81 01          |
    | xor qword [rax + 1 * rcx + 0x80], 0x01       | 48 83 b4 08 80 00 00 00 01 |
    | xor qword [rax + 1 * rcx - 0x80], 0x01       | 48 83 74 08 80 01          |
    | xor qword [rax + 1 * rcx - 0x81], 0x01       | 48 83 b4 08 7f ff ff ff 01 |
    | xor qword [rax + 1 * rcx + 0xff], 0x01       | 48 83 b4 08 ff 00 00 00 01 |
    | xor qword [rax + 1 * rcx - 0xff], 0x01       | 48 83 b4 08 01 ff ff ff 01 |
    | xor qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 83 b4 08 ff ff ff 7f 01 |
    | xor qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 83 b4 08 01 00 00 80 01 |
    | xor qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 83 b4 08 00 00 00 80 01 |
    | xor qword [r10 + 0x7f], 0x01                 | 49 83 72 7f 01             |
    | xor qword [r10 + 0x80], 0x01                 | 49 83 b2 80 00 00 00 01    |
    | xor qword [r10 - 0x80], 0x01                 | 49 83 72 80 01             |
    | xor qword [r10 - 0x81], 0x01                 | 49 83 b2 7f ff ff ff 01    |
    | xor qword [rax], 0x00                        | 48 83 30 00                |
    | xor qword [rax], 0x7f                        | 48 83 30 7f                |
    | xor qword [rax], 0x80                        | 48 83 30 80                |
    | xor qword [rax], 0xff                        | 48 83 30 ff                |
    | xor qword [rcx], 0x7f                        | 48 83 31 7f                |
    | xor qword [rdx], 0x80                        | 48 83 32 80                |
    | xor qword [rbx], 0xff                        | 48 83 33 ff                |
    | xor qword [rsp], 0x00                        | 48 83 34 24 00             |
    | xor qword [rsi], 0x7f                        | 48 83 36 7f                |
    | xor qword [rdi], 0x80                        | 48 83 37 80                |
    | xor qword [r8], 0xff                         | 49 83 30 ff                |
    | xor qword [r9], 0x00                         | 49 83 31 00                |
    | xor qword [r11], 0x7f                        | 49 83 33 7f                |
    | xor qword [r12], 0x80                        | 49 83 34 24 80             |
    | xor qword [r13], 0xff                        | 49 83 75 00 ff             |
    | xor qword [r14], 0x00                        | 49 83 36 00                |
    | xor qword [rax + 1 * rcx], 0x7f              | 48 83 34 08 7f             |
    | xor qword [rcx + 1 * rcx], 0x80              | 48 83 34 09 80             |
    | xor qword [rdx + 1 * rcx], 0xff              | 48 83 34 0a ff             |
    | xor qword [rbx + 1 * rcx], 0x00              | 48 83 34 0b 00             |
    | xor qword [rbp + 1 * rcx], 0x7f              | 48 83 74 0d 00 7f          |
    | xor qword [rsi + 1 * rcx], 0x80              | 48 83 34 0e 80             |
    | xor qword [rdi + 1 * rcx], 0xff              | 48 83 34 0f ff             |
    | xor qword [r8 + 1 * rcx], 0x00               | 49 83 34 08 00             |
    | xor qword [r10 + 1 * rcx], 0x7f              | 49 83 34 0a 7f             |
    | xor qword [r11 + 1 * rcx], 0x80              | 49 83 34 0b 80             |
    | xor qword [r12 + 1 * rcx], 0xff              | 49 83 34 0c ff             |
    | xor qword [r13 + 1 * rcx], 0x00              | 49 83 74 0d 00 00          |
    | xor qword [r15 + 1 * rcx], 0x7f              | 49 83 34 0f 7f             |
    | xor qword [rax + 1 * rax], 0x80              | 48 83 34 00 80             |
    | xor qword [rax + 1 * rdx], 0xff              | 48 83 34 10 ff             |
    | xor qword [rax + 1 * rbx], 0x00              | 48 83 34 18 00             |
    | xor qword [rax + 1 * rsi], 0x7f              | 48 83 34 30 7f             |
    | xor qword [rax + 1 * rdi], 0x80              | 48 83 34 38 80             |
    | xor qword [rax + 1 * r8], 0xff               | 4a 83 34 00 ff             |
    | xor qword [rax + 1 * r9], 0x00               | 4a 83 34 08 00             |
    | xor qword [rax + 1 * r11], 0x7f              | 4a 83 34 18 7f             |
    | xor qword [rax + 1 * r12], 0x80              | 4a 83 34 20 80             |
    | xor qword [rax + 1 * r13], 0xff              | 4a 83 34 28 ff             |
    | xor qword [rax + 1 * r14], 0x00              | 4a 83 34 30 00             |
    | xor qword [rax + 2 * rcx], 0x7f              | 48 83 34 48 7f             |
    | xor qword [rax + 4 * rcx], 0x80              | 48 83 34 88 80             |
    | xor qword [rax + 8 * rcx], 0xff              | 48 83 34 c8 ff             |
    | xor qword [r8 + 1 * r9], 0x00                | 4b 83 34 08 00             |
    | xor qword [r8 + 4 * r9], 0x7f                | 4b 83 34 88 7f             |
    | xor qword [r8 + 8 * r9], 0x80                | 4b 83 34 c8 80             |
    | xor qword [1 * rcx], 0xff                    | 48 83 34 0d 00 00 00 00 ff |
    | xor qword [2 * rcx], 0x00                    | 48 83 34 4d 00 00 00 00 00 |
    | xor qword [8 * rcx], 0x7f                    | 48 83 34 cd 00 00 00 00 7f |
    | xor qword [1 * r9], 0x80                     | 4a 83 34 0d 00 00 00 00 80 |
    | xor qword [2 * r9], 0xff                     | 4a 83 34 4d 00 00 00 00 ff |
    | xor qword [4 * r9], 0x00                     | 4a 83 34 8d 00 00 00 00 00 |
    | xor qword [r13 + 8 * r12], 0x7f              | 4b 83 74 e5 00 7f          |
    | xor qword [rsp + 4 * r15], 0x80              | 4a 83 34 bc 80             |
    | xor qword [rax + 1 * rcx + 0x00], 0xff       | 48 83 74 08 00 ff          |
    | xor qword [rax + 1 * rcx - 0x00], 0x00       | 48 83 74 08 00 00          |
    | xor qword [rax + 1 * rcx - 0x01], 0x7f       | 48 83 74 08 ff 7f          |
    | xor qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 83 b4 08 01 00 00 00 80 |
    | xor qword [rax + 1 * rcx - 0x00000001], 0xff | 48 83 b4 08 ff ff ff ff ff |
    | xor qword [rax + 1 * rcx + 0x7f], 0x00       | 48 83 74 08 7f 00          |
    | xor qword [rax + 1 * rcx + 0x80], 0x7f       | 48 83 b4 08 80 00 00 00 7f |
    | xor qword [rax + 1 * rcx - 0x80], 0x80       | 48 83 74 08 80 80          |
    | xor qword [rax + 1 * rcx - 0x81], 0xff       | 48 83 b4 08 7f ff ff ff ff |
    | xor qword [rax + 1 * rcx + 0xff], 0x00       | 48 83 b4 08 ff 00 00 00 00 |
    | xor qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 83 b4 08 ff ff ff 7f 7f |
    | xor qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 83 b4 08 01 00 00 80 80 |
    | xor qword [rax + 1 * rcx - 0x80000000], 0xff | 48 83 b4 08 00 00 00 80 ff |
    | xor qword [r10 + 0x7f], 0x00                 | 49 83 72 7f 00             |
    | xor qword [r10 - 0x80], 0x7f                 | 49 83 72 80 7f             |
    | xor qword [r10 - 0x81], 0x80                 | 49 83 b2 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_xor_addr64_imm8():
    encode(XOR_ADDR64_IMM8)


XOR_ADDR64_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | xor qword [rax], 0x00000001                        | 48 81 30 01 00 00 00                |
    | xor qword [rcx], 0x00000001                        | 48 81 31 01 00 00 00                |
    | xor qword [rdx], 0x00000001                        | 48 81 32 01 00 00 00                |
    | xor qword [rbx], 0x00000001                        | 48 81 33 01 00 00 00                |
    | xor qword [rsp], 0x00000001                        | 48 81 34 24 01 00 00 00             |
    | xor qword [rbp], 0x00000001                        | 48 81 75 00 01 00 00 00             |
    | xor qword [rsi], 0x00000001                        | 48 81 36 01 00 00 00                |
    | xor qword [rdi], 0x00000001                        | 48 81 37 01 00 00 00                |
    | xor qword [r8], 0x00000001                         | 49 81 30 01 00 00 00                |
    | xor qword [r9], 0x00000001                         | 49 81 31 01 00 00 00                |
    | xor qword [r10], 0x00000001                        | 49 81 32 01 00 00 00                |
    | xor qword [r11], 0x00000001                        | 49 81 33 01 00 00 00                |
    | xor qword [r12], 0x00000001                        | 49 81 34 24 01 00 00 00             |
    | xor qword [r13], 0x00000001                        | 49 81 75 00 01 00 00 00             |
    | xor qword [r14], 0x00000001                        | 49 81 36 01 00 00 00                |
    | xor qword [r15], 0x00000001                        | 49 81 37 01 00 00 00                |
    | xor qword [rax + 1 * rcx], 0x00000001              | 48 81 34 08 01 00 00 00             |
    | xor qword [rcx + 1 * rcx], 0x00000001              | 48 81 34 09 01 00 00 00             |
    | xor qword [rdx + 1 * rcx], 0x00000001              | 48 81 34 0a 01 00 00 00             |
    | xor qword [rbx + 1 * rcx], 0x00000001              | 48 81 34 0b 01 00 00 00             |
    | xor qword [rsp + 1 * rcx], 0x00000001              | 48 81 34 0c 01 00 00 00             |
    | xor qword [rbp + 1 * rcx], 0x00000001              | 48 81 74 0d 00 01 00 00 00          |
    | xor qword [rsi + 1 * rcx], 0x00000001              | 48 81 34 0e 01 00 00 00             |
    | xor qword [rdi + 1 * rcx], 0x00000001              | 48 81 34 0f 01 00 00 00             |
    | xor qword [r8 + 1 * rcx], 0x00000001               | 49 81 34 08 01 00 00 00             |
    | xor qword [r9 + 1 * rcx], 0x00000001               | 49 81 34 09 01 00 00 00             |
    | xor qword [r10 + 1 * rcx], 0x00000001              | 49 81 34 0a 01 00 00 00             |
    | xor qword [r11 + 1 * rcx], 0x00000001              | 49 81 34 0b 01 00 00 00             |
    | xor qword [r12 + 1 * rcx], 0x00000001              | 49 81 34 0c 01 00 00 00             |
    | xor qword [r13 + 1 * rcx], 0x00000001              | 49 81 74 0d 00 01 00 00 00          |
    | xor qword [r14 + 1 * rcx], 0x00000001              | 49 81 34 0e 01 00 00 00             |
    | xor qword [r15 + 1 * rcx], 0x00000001              | 49 81 34 0f 01 00 00 00             |
    | xor qword [rax + 1 * rax], 0x00000001              | 48 81 34 00 01 00 00 00             |
    | xor qword [rax + 1 * rdx], 0x00000001              | 48 81 34 10 01 00 00 00             |
    | xor qword [rax + 1 * rbx], 0x00000001              | 48 81 34 18 01 00 00 00             |
    | xor qword [rax + 1 * rbp], 0x00000001              | 48 81 34 28 01 00 00 00             |
    | xor qword [rax + 1 * rsi], 0x00000001              | 48 81 34 30 01 00 00 00             |
    | xor qword [rax + 1 * rdi], 0x00000001              | 48 81 34 38 01 00 00 00             |
    | xor qword [rax + 1 * r8], 0x00000001               | 4a 81 34 00 01 00 00 00             |
    | xor qword [rax + 1 * r9], 0x00000001               | 4a 81 34 08 01 00 00 00             |
    | xor qword [rax + 1 * r10], 0x00000001              | 4a 81 34 10 01 00 00 00             |
    | xor qword [rax + 1 * r11], 0x00000001              | 4a 81 34 18 01 00 00 00             |
    | xor qword [rax + 1 * r12], 0x00000001              | 4a 81 34 20 01 00 00 00             |
    | xor qword [rax + 1 * r13], 0x00000001              | 4a 81 34 28 01 00 00 00             |
    | xor qword [rax + 1 * r14], 0x00000001              | 4a 81 34 30 01 00 00 00             |
    | xor qword [rax + 1 * r15], 0x00000001              | 4a 81 34 38 01 00 00 00             |
    | xor qword [rax + 2 * rcx], 0x00000001              | 48 81 34 48 01 00 00 00             |
    | xor qword [rax + 4 * rcx], 0x00000001              | 48 81 34 88 01 00 00 00             |
    | xor qword [rax + 8 * rcx], 0x00000001              | 48 81 34 c8 01 00 00 00             |
    | xor qword [r8 + 1 * r9], 0x00000001                | 4b 81 34 08 01 00 00 00             |
    | xor qword [r8 + 2 * r9], 0x00000001                | 4b 81 34 48 01 00 00 00             |
    | xor qword [r8 + 4 * r9], 0x00000001                | 4b 81 34 88 01 00 00 00             |
    | xor qword [r8 + 8 * r9], 0x00000001                | 4b 81 34 c8 01 00 00 00             |
    | xor qword [1 * rcx], 0x00000001                    | 48 81 34 0d 00 00 00 00 01 00 00 00 |
    | xor qword [2 * rcx], 0x00000001                    | 48 81 34 4d 00 00 00 00 01 00 00 00 |
    | xor qword [4 * rcx], 0x00000001                    | 48 81 34 8d 00 00 00 00 01 00 00 00 |
    | xor qword [8 * rcx], 0x00000001                    | 48 81 34 cd 00 00 00 00 01 00 00 00 |
    | xor qword [1 * r9], 0x00000001                     | 4a 81 34 0d 00 00 00 00 01 00 00 00 |
    | xor qword [2 * r9], 0x00000001                     | 4a 81 34 4d 00 00 00 00 01 00 00 00 |
    | xor qword [4 * r9], 0x00000001                     | 4a 81 34 8d 00 00 00 00 01 00 00 00 |
    | xor qword [8 * r9], 0x00000001                     | 4a 81 34 cd 00 00 00 00 01 00 00 00 |
    | xor qword [r13 + 8 * r12], 0x00000001              | 4b 81 74 e5 00 01 00 00 00          |
    | xor qword [rsp + 4 * r15], 0x00000001              | 4a 81 34 bc 01 00 00 00             |
    | xor qword [rax + 1 * rcx + 0x00], 0x00000001       | 48 81 74 08 00 01 00 00 00          |
    | xor qword [rax + 1 * rcx - 0x00], 0x00000001       | 48 81 74 08 00 01 00 00 00          |
    | xor qword [rax + 1 * rcx + 0x01], 0x00000001       | 48 81 74 08 01 01 00 00 00          |
    | xor qword [rax + 1 * rcx - 0x01], 0x00000001       | 48 81 74 08 ff 01 00 00 00          |
    | xor qword [rax + 1 * rcx + 0x00000001], 0x00000001 | 48 81 b4 08 01 00 00 00 01 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x00000001], 0x00000001 | 48 81 b4 08 ff ff ff ff 01 00 00 00 |
    | xor qword [rax + 1 * rcx + 0x7f], 0x00000001       | 48 81 74 08 7f 01 00 00 00          |
    | xor qword [rax + 1 * rcx - 0x7f], 0x00000001       | 48 81 74 08 81 01 00 00 00          |
    | xor qword [rax + 1 * rcx + 0x80], 0x00000001       | 48 81 b4 08 80 00 00 00 01 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x80], 0x00000001       | 48 81 74 08 80 01 00 00 00          |
    | xor qword [rax + 1 * rcx - 0x81], 0x00000001       | 48 81 b4 08 7f ff ff ff 01 00 00 00 |
    | xor qword [rax + 1 * rcx + 0xff], 0x00000001       | 48 81 b4 08 ff 00 00 00 01 00 00 00 |
    | xor qword [rax + 1 * rcx - 0xff], 0x00000001       | 48 81 b4 08 01 ff ff ff 01 00 00 00 |
    | xor qword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 48 81 b4 08 ff ff ff 7f 01 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 48 81 b4 08 01 00 00 80 01 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x80000000], 0x00000001 | 48 81 b4 08 00 00 00 80 01 00 00 00 |
    | xor qword [r10 + 0x7f], 0x00000001                 | 49 81 72 7f 01 00 00 00             |
    | xor qword [r10 + 0x80], 0x00000001                 | 49 81 b2 80 00 00 00 01 00 00 00    |
    | xor qword [r10 - 0x80], 0x00000001                 | 49 81 72 80 01 00 00 00             |
    | xor qword [r10 - 0x81], 0x00000001                 | 49 81 b2 7f ff ff ff 01 00 00 00    |
    | xor qword [rax], 0x00000000                        | 48 81 30 00 00 00 00                |
    | xor qword [rax], 0x0000007f                        | 48 81 30 7f 00 00 00                |
    | xor qword [rax], 0x00000080                        | 48 81 30 80 00 00 00                |
    | xor qword [rax], 0x000000ff                        | 48 81 30 ff 00 00 00                |
    | xor qword [rax], 0x00000100                        | 48 81 30 00 01 00 00                |
    | xor qword [rax], 0x00007fff                        | 48 81 30 ff 7f 00 00                |
    | xor qword [rax], 0x00008000                        | 48 81 30 00 80 00 00                |
    | xor qword [rax], 0x0000ffff                        | 48 81 30 ff ff 00 00                |
    | xor qword [rax], 0x00010000                        | 48 81 30 00 00 01 00                |
    | xor qword [rax], 0x7fffffff                        | 48 81 30 ff ff ff 7f                |
    | xor qword [rax], 0x80000000                        | 48 81 30 00 00 00 80                |
    | xor qword [rax], 0xffffffff                        | 48 81 30 ff ff ff ff                |
    | xor qword [rcx], 0x0000007f                        | 48 81 31 7f 00 00 00                |
    | xor qword [rdx], 0x00000080                        | 48 81 32 80 00 00 00                |
    | xor qword [rbx], 0x000000ff                        | 48 81 33 ff 00 00 00                |
    | xor qword [rsp], 0x00000100                        | 48 81 34 24 00 01 00 00             |
    | xor qword [rbp], 0x00007fff                        | 48 81 75 00 ff 7f 00 00             |
    | xor qword [rsi], 0x00008000                        | 48 81 36 00 80 00 00                |
    | xor qword [rdi], 0x0000ffff                        | 48 81 37 ff ff 00 00                |
    | xor qword [r8], 0x00010000                         | 49 81 30 00 00 01 00                |
    | xor qword [r9], 0x7fffffff                         | 49 81 31 ff ff ff 7f                |
    | xor qword [r10], 0x80000000                        | 49 81 32 00 00 00 80                |
    | xor qword [r11], 0xffffffff                        | 49 81 33 ff ff ff ff                |
    | xor qword [r12], 0x00000000                        | 49 81 34 24 00 00 00 00             |
    | xor qword [r14], 0x0000007f                        | 49 81 36 7f 00 00 00                |
    | xor qword [r15], 0x00000080                        | 49 81 37 80 00 00 00                |
    | xor qword [rax + 1 * rcx], 0x000000ff              | 48 81 34 08 ff 00 00 00             |
    | xor qword [rcx + 1 * rcx], 0x00000100              | 48 81 34 09 00 01 00 00             |
    | xor qword [rdx + 1 * rcx], 0x00007fff              | 48 81 34 0a ff 7f 00 00             |
    | xor qword [rbx + 1 * rcx], 0x00008000              | 48 81 34 0b 00 80 00 00             |
    | xor qword [rsp + 1 * rcx], 0x0000ffff              | 48 81 34 0c ff ff 00 00             |
    | xor qword [rbp + 1 * rcx], 0x00010000              | 48 81 74 0d 00 00 00 01 00          |
    | xor qword [rsi + 1 * rcx], 0x7fffffff              | 48 81 34 0e ff ff ff 7f             |
    | xor qword [rdi + 1 * rcx], 0x80000000              | 48 81 34 0f 00 00 00 80             |
    | xor qword [r8 + 1 * rcx], 0xffffffff               | 49 81 34 08 ff ff ff ff             |
    | xor qword [r9 + 1 * rcx], 0x00000000               | 49 81 34 09 00 00 00 00             |
    | xor qword [r11 + 1 * rcx], 0x0000007f              | 49 81 34 0b 7f 00 00 00             |
    | xor qword [r12 + 1 * rcx], 0x00000080              | 49 81 34 0c 80 00 00 00             |
    | xor qword [r13 + 1 * rcx], 0x000000ff              | 49 81 74 0d 00 ff 00 00 00          |
    | xor qword [r14 + 1 * rcx], 0x00000100              | 49 81 34 0e 00 01 00 00             |
    | xor qword [r15 + 1 * rcx], 0x00007fff              | 49 81 34 0f ff 7f 00 00             |
    | xor qword [rax + 1 * rax], 0x00008000              | 48 81 34 00 00 80 00 00             |
    | xor qword [rax + 1 * rdx], 0x0000ffff              | 48 81 34 10 ff ff 00 00             |
    | xor qword [rax + 1 * rbx], 0x00010000              | 48 81 34 18 00 00 01 00             |
    | xor qword [rax + 1 * rbp], 0x7fffffff              | 48 81 34 28 ff ff ff 7f             |
    | xor qword [rax + 1 * rsi], 0x80000000              | 48 81 34 30 00 00 00 80             |
    | xor qword [rax + 1 * rdi], 0xffffffff              | 48 81 34 38 ff ff ff ff             |
    | xor qword [rax + 1 * r8], 0x00000000               | 4a 81 34 00 00 00 00 00             |
    | xor qword [rax + 1 * r10], 0x0000007f              | 4a 81 34 10 7f 00 00 00             |
    | xor qword [rax + 1 * r11], 0x00000080              | 4a 81 34 18 80 00 00 00             |
    | xor qword [rax + 1 * r12], 0x000000ff              | 4a 81 34 20 ff 00 00 00             |
    | xor qword [rax + 1 * r13], 0x00000100              | 4a 81 34 28 00 01 00 00             |
    | xor qword [rax + 1 * r14], 0x00007fff              | 4a 81 34 30 ff 7f 00 00             |
    | xor qword [rax + 1 * r15], 0x00008000              | 4a 81 34 38 00 80 00 00             |
    | xor qword [rax + 2 * rcx], 0x0000ffff              | 48 81 34 48 ff ff 00 00             |
    | xor qword [rax + 4 * rcx], 0x00010000              | 48 81 34 88 00 00 01 00             |
    | xor qword [rax + 8 * rcx], 0x7fffffff              | 48 81 34 c8 ff ff ff 7f             |
    | xor qword [r8 + 1 * r9], 0x80000000                | 4b 81 34 08 00 00 00 80             |
    | xor qword [r8 + 2 * r9], 0xffffffff                | 4b 81 34 48 ff ff ff ff             |
    | xor qword [r8 + 4 * r9], 0x00000000                | 4b 81 34 88 00 00 00 00             |
    | xor qword [1 * rcx], 0x0000007f                    | 48 81 34 0d 00 00 00 00 7f 00 00 00 |
    | xor qword [2 * rcx], 0x00000080                    | 48 81 34 4d 00 00 00 00 80 00 00 00 |
    | xor qword [4 * rcx], 0x000000ff                    | 48 81 34 8d 00 00 00 00 ff 00 00 00 |
    | xor qword [8 * rcx], 0x00000100                    | 48 81 34 cd 00 00 00 00 00 01 00 00 |
    | xor qword [1 * r9], 0x00007fff                     | 4a 81 34 0d 00 00 00 00 ff 7f 00 00 |
    | xor qword [2 * r9], 0x00008000                     | 4a 81 34 4d 00 00 00 00 00 80 00 00 |
    | xor qword [4 * r9], 0x0000ffff                     | 4a 81 34 8d 00 00 00 00 ff ff 00 00 |
    | xor qword [8 * r9], 0x00010000                     | 4a 81 34 cd 00 00 00 00 00 00 01 00 |
    | xor qword [r13 + 8 * r12], 0x7fffffff              | 4b 81 74 e5 00 ff ff ff 7f          |
    | xor qword [rsp + 4 * r15], 0x80000000              | 4a 81 34 bc 00 00 00 80             |
    | xor qword [rax + 1 * rcx + 0x00], 0xffffffff       | 48 81 74 08 00 ff ff ff ff          |
    | xor qword [rax + 1 * rcx - 0x00], 0x00000000       | 48 81 74 08 00 00 00 00 00          |
    | xor qword [rax + 1 * rcx - 0x01], 0x0000007f       | 48 81 74 08 ff 7f 00 00 00          |
    | xor qword [rax + 1 * rcx + 0x00000001], 0x00000080 | 48 81 b4 08 01 00 00 00 80 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x00000001], 0x000000ff | 48 81 b4 08 ff ff ff ff ff 00 00 00 |
    | xor qword [rax + 1 * rcx + 0x7f], 0x00000100       | 48 81 74 08 7f 00 01 00 00          |
    | xor qword [rax + 1 * rcx - 0x7f], 0x00007fff       | 48 81 74 08 81 ff 7f 00 00          |
    | xor qword [rax + 1 * rcx + 0x80], 0x00008000       | 48 81 b4 08 80 00 00 00 00 80 00 00 |
    | xor qword [rax + 1 * rcx - 0x80], 0x0000ffff       | 48 81 74 08 80 ff ff 00 00          |
    | xor qword [rax + 1 * rcx - 0x81], 0x00010000       | 48 81 b4 08 7f ff ff ff 00 00 01 00 |
    | xor qword [rax + 1 * rcx + 0xff], 0x7fffffff       | 48 81 b4 08 ff 00 00 00 ff ff ff 7f |
    | xor qword [rax + 1 * rcx - 0xff], 0x80000000       | 48 81 b4 08 01 ff ff ff 00 00 00 80 |
    | xor qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 48 81 b4 08 ff ff ff 7f ff ff ff ff |
    | xor qword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 48 81 b4 08 01 00 00 80 00 00 00 00 |
    | xor qword [r10 + 0x7f], 0x0000007f                 | 49 81 72 7f 7f 00 00 00             |
    | xor qword [r10 + 0x80], 0x00000080                 | 49 81 b2 80 00 00 00 80 00 00 00    |
    | xor qword [r10 - 0x80], 0x000000ff                 | 49 81 72 80 ff 00 00 00             |
    | xor qword [r10 - 0x81], 0x00000100                 | 49 81 b2 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_xor_addr64_imm32():
    encode(XOR_ADDR64_IMM32)


XOR_ADDR64_REG64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | xor qword [rax], rcx                        | 48 31 08                |
    | xor qword [rcx], rcx                        | 48 31 09                |
    | xor qword [rdx], rcx                        | 48 31 0a                |
    | xor qword [rbx], rcx                        | 48 31 0b                |
    | xor qword [rsp], rcx                        | 48 31 0c 24             |
    | xor qword [rbp], rcx                        | 48 31 4d 00             |
    | xor qword [rsi], rcx                        | 48 31 0e                |
    | xor qword [rdi], rcx                        | 48 31 0f                |
    | xor qword [r8], rcx                         | 49 31 08                |
    | xor qword [r9], rcx                         | 49 31 09                |
    | xor qword [r10], rcx                        | 49 31 0a                |
    | xor qword [r11], rcx                        | 49 31 0b                |
    | xor qword [r12], rcx                        | 49 31 0c 24             |
    | xor qword [r13], rcx                        | 49 31 4d 00             |
    | xor qword [r14], rcx                        | 49 31 0e                |
    | xor qword [r15], rcx                        | 49 31 0f                |
    | xor qword [rax + 1 * rcx], rcx              | 48 31 0c 08             |
    | xor qword [rcx + 1 * rcx], rcx              | 48 31 0c 09             |
    | xor qword [rdx + 1 * rcx], rcx              | 48 31 0c 0a             |
    | xor qword [rbx + 1 * rcx], rcx              | 48 31 0c 0b             |
    | xor qword [rsp + 1 * rcx], rcx              | 48 31 0c 0c             |
    | xor qword [rbp + 1 * rcx], rcx              | 48 31 4c 0d 00          |
    | xor qword [rsi + 1 * rcx], rcx              | 48 31 0c 0e             |
    | xor qword [rdi + 1 * rcx], rcx              | 48 31 0c 0f             |
    | xor qword [r8 + 1 * rcx], rcx               | 49 31 0c 08             |
    | xor qword [r9 + 1 * rcx], rcx               | 49 31 0c 09             |
    | xor qword [r10 + 1 * rcx], rcx              | 49 31 0c 0a             |
    | xor qword [r11 + 1 * rcx], rcx              | 49 31 0c 0b             |
    | xor qword [r12 + 1 * rcx], rcx              | 49 31 0c 0c             |
    | xor qword [r13 + 1 * rcx], rcx              | 49 31 4c 0d 00          |
    | xor qword [r14 + 1 * rcx], rcx              | 49 31 0c 0e             |
    | xor qword [r15 + 1 * rcx], rcx              | 49 31 0c 0f             |
    | xor qword [rax + 1 * rax], rcx              | 48 31 0c 00             |
    | xor qword [rax + 1 * rdx], rcx              | 48 31 0c 10             |
    | xor qword [rax + 1 * rbx], rcx              | 48 31 0c 18             |
    | xor qword [rax + 1 * rbp], rcx              | 48 31 0c 28             |
    | xor qword [rax + 1 * rsi], rcx              | 48 31 0c 30             |
    | xor qword [rax + 1 * rdi], rcx              | 48 31 0c 38             |
    | xor qword [rax + 1 * r8], rcx               | 4a 31 0c 00             |
    | xor qword [rax + 1 * r9], rcx               | 4a 31 0c 08             |
    | xor qword [rax + 1 * r10], rcx              | 4a 31 0c 10             |
    | xor qword [rax + 1 * r11], rcx              | 4a 31 0c 18             |
    | xor qword [rax + 1 * r12], rcx              | 4a 31 0c 20             |
    | xor qword [rax + 1 * r13], rcx              | 4a 31 0c 28             |
    | xor qword [rax + 1 * r14], rcx              | 4a 31 0c 30             |
    | xor qword [rax + 1 * r15], rcx              | 4a 31 0c 38             |
    | xor qword [rax + 2 * rcx], rcx              | 48 31 0c 48             |
    | xor qword [rax + 4 * rcx], rcx              | 48 31 0c 88             |
    | xor qword [rax + 8 * rcx], rcx              | 48 31 0c c8             |
    | xor qword [r8 + 1 * r9], rcx                | 4b 31 0c 08             |
    | xor qword [r8 + 2 * r9], rcx                | 4b 31 0c 48             |
    | xor qword [r8 + 4 * r9], rcx                | 4b 31 0c 88             |
    | xor qword [r8 + 8 * r9], rcx                | 4b 31 0c c8             |
    | xor qword [1 * rcx], rcx                    | 48 31 0c 0d 00 00 00 00 |
    | xor qword [2 * rcx], rcx                    | 48 31 0c 4d 00 00 00 00 |
    | xor qword [4 * rcx], rcx                    | 48 31 0c 8d 00 00 00 00 |
    | xor qword [8 * rcx], rcx                    | 48 31 0c cd 00 00 00 00 |
    | xor qword [1 * r9], rcx                     | 4a 31 0c 0d 00 00 00 00 |
    | xor qword [2 * r9], rcx                     | 4a 31 0c 4d 00 00 00 00 |
    | xor qword [4 * r9], rcx                     | 4a 31 0c 8d 00 00 00 00 |
    | xor qword [8 * r9], rcx                     | 4a 31 0c cd 00 00 00 00 |
    | xor qword [r13 + 8 * r12], rcx              | 4b 31 4c e5 00          |
    | xor qword [rsp + 4 * r15], rcx              | 4a 31 0c bc             |
    | xor qword [rax + 1 * rcx + 0x00], rcx       | 48 31 4c 08 00          |
    | xor qword [rax + 1 * rcx - 0x00], rcx       | 48 31 4c 08 00          |
    | xor qword [rax + 1 * rcx + 0x01], rcx       | 48 31 4c 08 01          |
    | xor qword [rax + 1 * rcx - 0x01], rcx       | 48 31 4c 08 ff          |
    | xor qword [rax + 1 * rcx + 0x00000001], rcx | 48 31 8c 08 01 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x00000001], rcx | 48 31 8c 08 ff ff ff ff |
    | xor qword [rax + 1 * rcx + 0x7f], rcx       | 48 31 4c 08 7f          |
    | xor qword [rax + 1 * rcx - 0x7f], rcx       | 48 31 4c 08 81          |
    | xor qword [rax + 1 * rcx + 0x80], rcx       | 48 31 8c 08 80 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x80], rcx       | 48 31 4c 08 80          |
    | xor qword [rax + 1 * rcx - 0x81], rcx       | 48 31 8c 08 7f ff ff ff |
    | xor qword [rax + 1 * rcx + 0xff], rcx       | 48 31 8c 08 ff 00 00 00 |
    | xor qword [rax + 1 * rcx - 0xff], rcx       | 48 31 8c 08 01 ff ff ff |
    | xor qword [rax + 1 * rcx + 0x7fffffff], rcx | 48 31 8c 08 ff ff ff 7f |
    | xor qword [rax + 1 * rcx - 0x7fffffff], rcx | 48 31 8c 08 01 00 00 80 |
    | xor qword [rax + 1 * rcx - 0x80000000], rcx | 48 31 8c 08 00 00 00 80 |
    | xor qword [r10 + 0x7f], rcx                 | 49 31 4a 7f             |
    | xor qword [r10 + 0x80], rcx                 | 49 31 8a 80 00 00 00    |
    | xor qword [r10 - 0x80], rcx                 | 49 31 4a 80             |
    | xor qword [r10 - 0x81], rcx                 | 49 31 8a 7f ff ff ff    |
    | xor qword [rax], rax                        | 48 31 00                |
    | xor qword [rax], rdx                        | 48 31 10                |
    | xor qword [rax], rbx                        | 48 31 18                |
    | xor qword [rax], rsp                        | 48 31 20                |
    | xor qword [rax], rbp                        | 48 31 28                |
    | xor qword [rax], rsi                        | 48 31 30                |
    | xor qword [rax], rdi                        | 48 31 38                |
    | xor qword [rax], r8                         | 4c 31 00                |
    | xor qword [rax], r9                         | 4c 31 08                |
    | xor qword [rax], r10                        | 4c 31 10                |
    | xor qword [rax], r11                        | 4c 31 18                |
    | xor qword [rax], r12                        | 4c 31 20                |
    | xor qword [rax], r13                        | 4c 31 28                |
    | xor qword [rax], r14                        | 4c 31 30                |
    | xor qword [rax], r15                        | 4c 31 38                |
    | xor qword [rcx], rdx                        | 48 31 11                |
    | xor qword [rdx], rbx                        | 48 31 1a                |
    | xor qword [rbx], rsp                        | 48 31 23                |
    | xor qword [rsp], rbp                        | 48 31 2c 24             |
    | xor qword [rbp], rsi                        | 48 31 75 00             |
    | xor qword [rsi], rdi                        | 48 31 3e                |
    | xor qword [rdi], r8                         | 4c 31 07                |
    | xor qword [r8], r9                          | 4d 31 08                |
    | xor qword [r9], r10                         | 4d 31 11                |
    | xor qword [r10], r11                        | 4d 31 1a                |
    | xor qword [r11], r12                        | 4d 31 23                |
    | xor qword [r12], r13                        | 4d 31 2c 24             |
    | xor qword [r13], r14                        | 4d 31 75 00             |
    | xor qword [r14], r15                        | 4d 31 3e                |
    | xor qword [r15], rax                        | 49 31 07                |
    | xor qword [rcx + 1 * rcx], rdx              | 48 31 14 09             |
    | xor qword [rdx + 1 * rcx], rbx              | 48 31 1c 0a             |
    | xor qword [rbx + 1 * rcx], rsp              | 48 31 24 0b             |
    | xor qword [rsp + 1 * rcx], rbp              | 48 31 2c 0c             |
    | xor qword [rbp + 1 * rcx], rsi              | 48 31 74 0d 00          |
    | xor qword [rsi + 1 * rcx], rdi              | 48 31 3c 0e             |
    | xor qword [rdi + 1 * rcx], r8               | 4c 31 04 0f             |
    | xor qword [r8 + 1 * rcx], r9                | 4d 31 0c 08             |
    | xor qword [r9 + 1 * rcx], r10               | 4d 31 14 09             |
    | xor qword [r10 + 1 * rcx], r11              | 4d 31 1c 0a             |
    | xor qword [r11 + 1 * rcx], r12              | 4d 31 24 0b             |
    | xor qword [r12 + 1 * rcx], r13              | 4d 31 2c 0c             |
    | xor qword [r13 + 1 * rcx], r14              | 4d 31 74 0d 00          |
    | xor qword [r14 + 1 * rcx], r15              | 4d 31 3c 0e             |
    | xor qword [r15 + 1 * rcx], rax              | 49 31 04 0f             |
    | xor qword [rax + 1 * rdx], rdx              | 48 31 14 10             |
    | xor qword [rax + 1 * rbx], rbx              | 48 31 1c 18             |
    | xor qword [rax + 1 * rbp], rsp              | 48 31 24 28             |
    | xor qword [rax + 1 * rsi], rbp              | 48 31 2c 30             |
    | xor qword [rax + 1 * rdi], rsi              | 48 31 34 38             |
    | xor qword [rax + 1 * r8], rdi               | 4a 31 3c 00             |
    | xor qword [rax + 1 * r9], r8                | 4e 31 04 08             |
    | xor qword [rax + 1 * r10], r9               | 4e 31 0c 10             |
    | xor qword [rax + 1 * r11], r10              | 4e 31 14 18             |
    | xor qword [rax + 1 * r12], r11              | 4e 31 1c 20             |
    | xor qword [rax + 1 * r13], r12              | 4e 31 24 28             |
    | xor qword [rax + 1 * r14], r13              | 4e 31 2c 30             |
    | xor qword [rax + 1 * r15], r14              | 4e 31 34 38             |
    | xor qword [rax + 2 * rcx], r15              | 4c 31 3c 48             |
    | xor qword [rax + 4 * rcx], rax              | 48 31 04 88             |
    | xor qword [r8 + 1 * r9], rdx                | 4b 31 14 08             |
    | xor qword [r8 + 2 * r9], rbx                | 4b 31 1c 48             |
    | xor qword [r8 + 4 * r9], rsp                | 4b 31 24 88             |
    | xor qword [r8 + 8 * r9], rbp                | 4b 31 2c c8             |
    | xor qword [1 * rcx], rsi                    | 48 31 34 0d 00 00 00 00 |
    | xor qword [2 * rcx], rdi                    | 48 31 3c 4d 00 00 00 00 |
    | xor qword [4 * rcx], r8                     | 4c 31 04 8d 00 00 00 00 |
    | xor qword [8 * rcx], r9                     | 4c 31 0c cd 00 00 00 00 |
    | xor qword [1 * r9], r10                     | 4e 31 14 0d 00 00 00 00 |
    | xor qword [2 * r9], r11                     | 4e 31 1c 4d 00 00 00 00 |
    | xor qword [4 * r9], r12                     | 4e 31 24 8d 00 00 00 00 |
    | xor qword [8 * r9], r13                     | 4e 31 2c cd 00 00 00 00 |
    | xor qword [r13 + 8 * r12], r14              | 4f 31 74 e5 00          |
    | xor qword [rsp + 4 * r15], r15              | 4e 31 3c bc             |
    | xor qword [rax + 1 * rcx + 0x00], rax       | 48 31 44 08 00          |
    | xor qword [rax + 1 * rcx + 0x01], rdx       | 48 31 54 08 01          |
    | xor qword [rax + 1 * rcx - 0x01], rbx       | 48 31 5c 08 ff          |
    | xor qword [rax + 1 * rcx + 0x00000001], rsp | 48 31 a4 08 01 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x00000001], rbp | 48 31 ac 08 ff ff ff ff |
    | xor qword [rax + 1 * rcx + 0x7f], rsi       | 48 31 74 08 7f          |
    | xor qword [rax + 1 * rcx - 0x7f], rdi       | 48 31 7c 08 81          |
    | xor qword [rax + 1 * rcx + 0x80], r8        | 4c 31 84 08 80 00 00 00 |
    | xor qword [rax + 1 * rcx - 0x80], r9        | 4c 31 4c 08 80          |
    | xor qword [rax + 1 * rcx - 0x81], r10       | 4c 31 94 08 7f ff ff ff |
    | xor qword [rax + 1 * rcx + 0xff], r11       | 4c 31 9c 08 ff 00 00 00 |
    | xor qword [rax + 1 * rcx - 0xff], r12       | 4c 31 a4 08 01 ff ff ff |
    | xor qword [rax + 1 * rcx + 0x7fffffff], r13 | 4c 31 ac 08 ff ff ff 7f |
    | xor qword [rax + 1 * rcx - 0x7fffffff], r14 | 4c 31 b4 08 01 00 00 80 |
    | xor qword [rax + 1 * rcx - 0x80000000], r15 | 4c 31 bc 08 00 00 00 80 |
    | xor qword [r10 + 0x7f], rax                 | 49 31 42 7f             |
    | xor qword [r10 - 0x80], rdx                 | 49 31 52 80             |
    | xor qword [r10 - 0x81], rbx                 | 49 31 9a 7f ff ff ff    |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_xor_addr64_reg64():
    encode(XOR_ADDR64_REG64)


XOR_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | xor dword [rax], 0x01                        | 83 30 01                   |
    | xor dword [rcx], 0x01                        | 83 31 01                   |
    | xor dword [rdx], 0x01                        | 83 32 01                   |
    | xor dword [rbx], 0x01                        | 83 33 01                   |
    | xor dword [rsp], 0x01                        | 83 34 24 01                |
    | xor dword [rbp], 0x01                        | 83 75 00 01                |
    | xor dword [rsi], 0x01                        | 83 36 01                   |
    | xor dword [rdi], 0x01                        | 83 37 01                   |
    | xor dword [r8], 0x01                         | 41 83 30 01                |
    | xor dword [r9], 0x01                         | 41 83 31 01                |
    | xor dword [r10], 0x01                        | 41 83 32 01                |
    | xor dword [r11], 0x01                        | 41 83 33 01                |
    | xor dword [r12], 0x01                        | 41 83 34 24 01             |
    | xor dword [r13], 0x01                        | 41 83 75 00 01             |
    | xor dword [r14], 0x01                        | 41 83 36 01                |
    | xor dword [r15], 0x01                        | 41 83 37 01                |
    | xor dword [rax + 1 * rcx], 0x01              | 83 34 08 01                |
    | xor dword [rcx + 1 * rcx], 0x01              | 83 34 09 01                |
    | xor dword [rdx + 1 * rcx], 0x01              | 83 34 0a 01                |
    | xor dword [rbx + 1 * rcx], 0x01              | 83 34 0b 01                |
    | xor dword [rsp + 1 * rcx], 0x01              | 83 34 0c 01                |
    | xor dword [rbp + 1 * rcx], 0x01              | 83 74 0d 00 01             |
    | xor dword [rsi + 1 * rcx], 0x01              | 83 34 0e 01                |
    | xor dword [rdi + 1 * rcx], 0x01              | 83 34 0f 01                |
    | xor dword [r8 + 1 * rcx], 0x01               | 41 83 34 08 01             |
    | xor dword [r9 + 1 * rcx], 0x01               | 41 83 34 09 01             |
    | xor dword [r10 + 1 * rcx], 0x01              | 41 83 34 0a 01             |
    | xor dword [r11 + 1 * rcx], 0x01              | 41 83 34 0b 01             |
    | xor dword [r12 + 1 * rcx], 0x01              | 41 83 34 0c 01             |
    | xor dword [r13 + 1 * rcx], 0x01              | 41 83 74 0d 00 01          |
    | xor dword [r14 + 1 * rcx], 0x01              | 41 83 34 0e 01             |
    | xor dword [r15 + 1 * rcx], 0x01              | 41 83 34 0f 01             |
    | xor dword [rax + 1 * rax], 0x01              | 83 34 00 01                |
    | xor dword [rax + 1 * rdx], 0x01              | 83 34 10 01                |
    | xor dword [rax + 1 * rbx], 0x01              | 83 34 18 01                |
    | xor dword [rax + 1 * rbp], 0x01              | 83 34 28 01                |
    | xor dword [rax + 1 * rsi], 0x01              | 83 34 30 01                |
    | xor dword [rax + 1 * rdi], 0x01              | 83 34 38 01                |
    | xor dword [rax + 1 * r8], 0x01               | 42 83 34 00 01             |
    | xor dword [rax + 1 * r9], 0x01               | 42 83 34 08 01             |
    | xor dword [rax + 1 * r10], 0x01              | 42 83 34 10 01             |
    | xor dword [rax + 1 * r11], 0x01              | 42 83 34 18 01             |
    | xor dword [rax + 1 * r12], 0x01              | 42 83 34 20 01             |
    | xor dword [rax + 1 * r13], 0x01              | 42 83 34 28 01             |
    | xor dword [rax + 1 * r14], 0x01              | 42 83 34 30 01             |
    | xor dword [rax + 1 * r15], 0x01              | 42 83 34 38 01             |
    | xor dword [rax + 2 * rcx], 0x01              | 83 34 48 01                |
    | xor dword [rax + 4 * rcx], 0x01              | 83 34 88 01                |
    | xor dword [rax + 8 * rcx], 0x01              | 83 34 c8 01                |
    | xor dword [r8 + 1 * r9], 0x01                | 43 83 34 08 01             |
    | xor dword [r8 + 2 * r9], 0x01                | 43 83 34 48 01             |
    | xor dword [r8 + 4 * r9], 0x01                | 43 83 34 88 01             |
    | xor dword [r8 + 8 * r9], 0x01                | 43 83 34 c8 01             |
    | xor dword [1 * rcx], 0x01                    | 83 34 0d 00 00 00 00 01    |
    | xor dword [2 * rcx], 0x01                    | 83 34 4d 00 00 00 00 01    |
    | xor dword [4 * rcx], 0x01                    | 83 34 8d 00 00 00 00 01    |
    | xor dword [8 * rcx], 0x01                    | 83 34 cd 00 00 00 00 01    |
    | xor dword [1 * r9], 0x01                     | 42 83 34 0d 00 00 00 00 01 |
    | xor dword [2 * r9], 0x01                     | 42 83 34 4d 00 00 00 00 01 |
    | xor dword [4 * r9], 0x01                     | 42 83 34 8d 00 00 00 00 01 |
    | xor dword [8 * r9], 0x01                     | 42 83 34 cd 00 00 00 00 01 |
    | xor dword [r13 + 8 * r12], 0x01              | 43 83 74 e5 00 01          |
    | xor dword [rsp + 4 * r15], 0x01              | 42 83 34 bc 01             |
    | xor dword [rax + 1 * rcx + 0x00], 0x01       | 83 74 08 00 01             |
    | xor dword [rax + 1 * rcx - 0x00], 0x01       | 83 74 08 00 01             |
    | xor dword [rax + 1 * rcx + 0x01], 0x01       | 83 74 08 01 01             |
    | xor dword [rax + 1 * rcx - 0x01], 0x01       | 83 74 08 ff 01             |
    | xor dword [rax + 1 * rcx + 0x00000001], 0x01 | 83 b4 08 01 00 00 00 01    |
    | xor dword [rax + 1 * rcx - 0x00000001], 0x01 | 83 b4 08 ff ff ff ff 01    |
    | xor dword [rax + 1 * rcx + 0x7f], 0x01       | 83 74 08 7f 01             |
    | xor dword [rax + 1 * rcx - 0x7f], 0x01       | 83 74 08 81 01             |
    | xor dword [rax + 1 * rcx + 0x80], 0x01       | 83 b4 08 80 00 00 00 01    |
    | xor dword [rax + 1 * rcx - 0x80], 0x01       | 83 74 08 80 01             |
    | xor dword [rax + 1 * rcx - 0x81], 0x01       | 83 b4 08 7f ff ff ff 01    |
    | xor dword [rax + 1 * rcx + 0xff], 0x01       | 83 b4 08 ff 00 00 00 01    |
    | xor dword [rax + 1 * rcx - 0xff], 0x01       | 83 b4 08 01 ff ff ff 01    |
    | xor dword [rax + 1 * rcx + 0x7fffffff], 0x01 | 83 b4 08 ff ff ff 7f 01    |
    | xor dword [rax + 1 * rcx - 0x7fffffff], 0x01 | 83 b4 08 01 00 00 80 01    |
    | xor dword [rax + 1 * rcx - 0x80000000], 0x01 | 83 b4 08 00 00 00 80 01    |
    | xor dword [r10 + 0x7f], 0x01                 | 41 83 72 7f 01             |
    | xor dword [r10 + 0x80], 0x01                 | 41 83 b2 80 00 00 00 01    |
    | xor dword [r10 - 0x80], 0x01                 | 41 83 72 80 01             |
    | xor dword [r10 - 0x81], 0x01                 | 41 83 b2 7f ff ff ff 01    |
    | xor dword [rax], 0x00                        | 83 30 00                   |
    | xor dword [rax], 0x7f                        | 83 30 7f                   |
    | xor dword [rax], 0x80                        | 83 30 80                   |
    | xor dword [rax], 0xff                        | 83 30 ff                   |
    | xor dword [rcx], 0x7f                        | 83 31 7f                   |
    | xor dword [rdx], 0x80                        | 83 32 80                   |
    | xor dword [rbx], 0xff                        | 83 33 ff                   |
    | xor dword [rsp], 0x00                        | 83 34 24 00                |
    | xor dword [rsi], 0x7f                        | 83 36 7f                   |
    | xor dword [rdi], 0x80                        | 83 37 80                   |
    | xor dword [r8], 0xff                         | 41 83 30 ff                |
    | xor dword [r9], 0x00                         | 41 83 31 00                |
    | xor dword [r11], 0x7f                        | 41 83 33 7f                |
    | xor dword [r12], 0x80                        | 41 83 34 24 80             |
    | xor dword [r13], 0xff                        | 41 83 75 00 ff             |
    | xor dword [r14], 0x00                        | 41 83 36 00                |
    | xor dword [rax + 1 * rcx], 0x7f              | 83 34 08 7f                |
    | xor dword [rcx + 1 * rcx], 0x80              | 83 34 09 80                |
    | xor dword [rdx + 1 * rcx], 0xff              | 83 34 0a ff                |
    | xor dword [rbx + 1 * rcx], 0x00              | 83 34 0b 00                |
    | xor dword [rbp + 1 * rcx], 0x7f              | 83 74 0d 00 7f             |
    | xor dword [rsi + 1 * rcx], 0x80              | 83 34 0e 80                |
    | xor dword [rdi + 1 * rcx], 0xff              | 83 34 0f ff                |
    | xor dword [r8 + 1 * rcx], 0x00               | 41 83 34 08 00             |
    | xor dword [r10 + 1 * rcx], 0x7f              | 41 83 34 0a 7f             |
    | xor dword [r11 + 1 * rcx], 0x80              | 41 83 34 0b 80             |
    | xor dword [r12 + 1 * rcx], 0xff              | 41 83 34 0c ff             |
    | xor dword [r13 + 1 * rcx], 0x00              | 41 83 74 0d 00 00          |
    | xor dword [r15 + 1 * rcx], 0x7f              | 41 83 34 0f 7f             |
    | xor dword [rax + 1 * rax], 0x80              | 83 34 00 80                |
    | xor dword [rax + 1 * rdx], 0xff              | 83 34 10 ff                |
    | xor dword [rax + 1 * rbx], 0x00              | 83 34 18 00                |
    | xor dword [rax + 1 * rsi], 0x7f              | 83 34 30 7f                |
    | xor dword [rax + 1 * rdi], 0x80              | 83 34 38 80                |
    | xor dword [rax + 1 * r8], 0xff               | 42 83 34 00 ff             |
    | xor dword [rax + 1 * r9], 0x00               | 42 83 34 08 00             |
    | xor dword [rax + 1 * r11], 0x7f              | 42 83 34 18 7f             |
    | xor dword [rax + 1 * r12], 0x80              | 42 83 34 20 80             |
    | xor dword [rax + 1 * r13], 0xff              | 42 83 34 28 ff             |
    | xor dword [rax + 1 * r14], 0x00              | 42 83 34 30 00             |
    | xor dword [rax + 2 * rcx], 0x7f              | 83 34 48 7f                |
    | xor dword [rax + 4 * rcx], 0x80              | 83 34 88 80                |
    | xor dword [rax + 8 * rcx], 0xff              | 83 34 c8 ff                |
    | xor dword [r8 + 1 * r9], 0x00                | 43 83 34 08 00             |
    | xor dword [r8 + 4 * r9], 0x7f                | 43 83 34 88 7f             |
    | xor dword [r8 + 8 * r9], 0x80                | 43 83 34 c8 80             |
    | xor dword [1 * rcx], 0xff                    | 83 34 0d 00 00 00 00 ff    |
    | xor dword [2 * rcx], 0x00                    | 83 34 4d 00 00 00 00 00    |
    | xor dword [8 * rcx], 0x7f                    | 83 34 cd 00 00 00 00 7f    |
    | xor dword [1 * r9], 0x80                     | 42 83 34 0d 00 00 00 00 80 |
    | xor dword [2 * r9], 0xff                     | 42 83 34 4d 00 00 00 00 ff |
    | xor dword [4 * r9], 0x00                     | 42 83 34 8d 00 00 00 00 00 |
    | xor dword [r13 + 8 * r12], 0x7f              | 43 83 74 e5 00 7f          |
    | xor dword [rsp + 4 * r15], 0x80              | 42 83 34 bc 80             |
    | xor dword [rax + 1 * rcx + 0x00], 0xff       | 83 74 08 00 ff             |
    | xor dword [rax + 1 * rcx - 0x00], 0x00       | 83 74 08 00 00             |
    | xor dword [rax + 1 * rcx - 0x01], 0x7f       | 83 74 08 ff 7f             |
    | xor dword [rax + 1 * rcx + 0x00000001], 0x80 | 83 b4 08 01 00 00 00 80    |
    | xor dword [rax + 1 * rcx - 0x00000001], 0xff | 83 b4 08 ff ff ff ff ff    |
    | xor dword [rax + 1 * rcx + 0x7f], 0x00       | 83 74 08 7f 00             |
    | xor dword [rax + 1 * rcx + 0x80], 0x7f       | 83 b4 08 80 00 00 00 7f    |
    | xor dword [rax + 1 * rcx - 0x80], 0x80       | 83 74 08 80 80             |
    | xor dword [rax + 1 * rcx - 0x81], 0xff       | 83 b4 08 7f ff ff ff ff    |
    | xor dword [rax + 1 * rcx + 0xff], 0x00       | 83 b4 08 ff 00 00 00 00    |
    | xor dword [rax + 1 * rcx + 0x7fffffff], 0x7f | 83 b4 08 ff ff ff 7f 7f    |
    | xor dword [rax + 1 * rcx - 0x7fffffff], 0x80 | 83 b4 08 01 00 00 80 80    |
    | xor dword [rax + 1 * rcx - 0x80000000], 0xff | 83 b4 08 00 00 00 80 ff    |
    | xor dword [r10 + 0x7f], 0x00                 | 41 83 72 7f 00             |
    | xor dword [r10 - 0x80], 0x7f                 | 41 83 72 80 7f             |
    | xor dword [r10 - 0x81], 0x80                 | 41 83 b2 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_xor_addr32_imm8():
    encode(XOR_ADDR32_IMM8)


XOR_ADDR32_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | xor dword [rax], 0x00000001                        | 81 30 01 00 00 00                   |
    | xor dword [rcx], 0x00000001                        | 81 31 01 00 00 00                   |
    | xor dword [rdx], 0x00000001                        | 81 32 01 00 00 00                   |
    | xor dword [rbx], 0x00000001                        | 81 33 01 00 00 00                   |
    | xor dword [rsp], 0x00000001                        | 81 34 24 01 00 00 00                |
    | xor dword [rbp], 0x00000001                        | 81 75 00 01 00 00 00                |
    | xor dword [rsi], 0x00000001                        | 81 36 01 00 00 00                   |
    | xor dword [rdi], 0x00000001                        | 81 37 01 00 00 00                   |
    | xor dword [r8], 0x00000001                         | 41 81 30 01 00 00 00                |
    | xor dword [r9], 0x00000001                         | 41 81 31 01 00 00 00                |
    | xor dword [r10], 0x00000001                        | 41 81 32 01 00 00 00                |
    | xor dword [r11], 0x00000001                        | 41 81 33 01 00 00 00                |
    | xor dword [r12], 0x00000001                        | 41 81 34 24 01 00 00 00             |
    | xor dword [r13], 0x00000001                        | 41 81 75 00 01 00 00 00             |
    | xor dword [r14], 0x00000001                        | 41 81 36 01 00 00 00                |
    | xor dword [r15], 0x00000001                        | 41 81 37 01 00 00 00                |
    | xor dword [rax + 1 * rcx], 0x00000001              | 81 34 08 01 00 00 00                |
    | xor dword [rcx + 1 * rcx], 0x00000001              | 81 34 09 01 00 00 00                |
    | xor dword [rdx + 1 * rcx], 0x00000001              | 81 34 0a 01 00 00 00                |
    | xor dword [rbx + 1 * rcx], 0x00000001              | 81 34 0b 01 00 00 00                |
    | xor dword [rsp + 1 * rcx], 0x00000001              | 81 34 0c 01 00 00 00                |
    | xor dword [rbp + 1 * rcx], 0x00000001              | 81 74 0d 00 01 00 00 00             |
    | xor dword [rsi + 1 * rcx], 0x00000001              | 81 34 0e 01 00 00 00                |
    | xor dword [rdi + 1 * rcx], 0x00000001              | 81 34 0f 01 00 00 00                |
    | xor dword [r8 + 1 * rcx], 0x00000001               | 41 81 34 08 01 00 00 00             |
    | xor dword [r9 + 1 * rcx], 0x00000001               | 41 81 34 09 01 00 00 00             |
    | xor dword [r10 + 1 * rcx], 0x00000001              | 41 81 34 0a 01 00 00 00             |
    | xor dword [r11 + 1 * rcx], 0x00000001              | 41 81 34 0b 01 00 00 00             |
    | xor dword [r12 + 1 * rcx], 0x00000001              | 41 81 34 0c 01 00 00 00             |
    | xor dword [r13 + 1 * rcx], 0x00000001              | 41 81 74 0d 00 01 00 00 00          |
    | xor dword [r14 + 1 * rcx], 0x00000001              | 41 81 34 0e 01 00 00 00             |
    | xor dword [r15 + 1 * rcx], 0x00000001              | 41 81 34 0f 01 00 00 00             |
    | xor dword [rax + 1 * rax], 0x00000001              | 81 34 00 01 00 00 00                |
    | xor dword [rax + 1 * rdx], 0x00000001              | 81 34 10 01 00 00 00                |
    | xor dword [rax + 1 * rbx], 0x00000001              | 81 34 18 01 00 00 00                |
    | xor dword [rax + 1 * rbp], 0x00000001              | 81 34 28 01 00 00 00                |
    | xor dword [rax + 1 * rsi], 0x00000001              | 81 34 30 01 00 00 00                |
    | xor dword [rax + 1 * rdi], 0x00000001              | 81 34 38 01 00 00 00                |
    | xor dword [rax + 1 * r8], 0x00000001               | 42 81 34 00 01 00 00 00             |
    | xor dword [rax + 1 * r9], 0x00000001               | 42 81 34 08 01 00 00 00             |
    | xor dword [rax + 1 * r10], 0x00000001              | 42 81 34 10 01 00 00 00             |
    | xor dword [rax + 1 * r11], 0x00000001              | 42 81 34 18 01 00 00 00             |
    | xor dword [rax + 1 * r12], 0x00000001              | 42 81 34 20 01 00 00 00             |
    | xor dword [rax + 1 * r13], 0x00000001              | 42 81 34 28 01 00 00 00             |
    | xor dword [rax + 1 * r14], 0x00000001              | 42 81 34 30 01 00 00 00             |
    | xor dword [rax + 1 * r15], 0x00000001              | 42 81 34 38 01 00 00 00             |
    | xor dword [rax + 2 * rcx], 0x00000001              | 81 34 48 01 00 00 00                |
    | xor dword [rax + 4 * rcx], 0x00000001              | 81 34 88 01 00 00 00                |
    | xor dword [rax + 8 * rcx], 0x00000001              | 81 34 c8 01 00 00 00                |
    | xor dword [r8 + 1 * r9], 0x00000001                | 43 81 34 08 01 00 00 00             |
    | xor dword [r8 + 2 * r9], 0x00000001                | 43 81 34 48 01 00 00 00             |
    | xor dword [r8 + 4 * r9], 0x00000001                | 43 81 34 88 01 00 00 00             |
    | xor dword [r8 + 8 * r9], 0x00000001                | 43 81 34 c8 01 00 00 00             |
    | xor dword [1 * rcx], 0x00000001                    | 81 34 0d 00 00 00 00 01 00 00 00    |
    | xor dword [2 * rcx], 0x00000001                    | 81 34 4d 00 00 00 00 01 00 00 00    |
    | xor dword [4 * rcx], 0x00000001                    | 81 34 8d 00 00 00 00 01 00 00 00    |
    | xor dword [8 * rcx], 0x00000001                    | 81 34 cd 00 00 00 00 01 00 00 00    |
    | xor dword [1 * r9], 0x00000001                     | 42 81 34 0d 00 00 00 00 01 00 00 00 |
    | xor dword [2 * r9], 0x00000001                     | 42 81 34 4d 00 00 00 00 01 00 00 00 |
    | xor dword [4 * r9], 0x00000001                     | 42 81 34 8d 00 00 00 00 01 00 00 00 |
    | xor dword [8 * r9], 0x00000001                     | 42 81 34 cd 00 00 00 00 01 00 00 00 |
    | xor dword [r13 + 8 * r12], 0x00000001              | 43 81 74 e5 00 01 00 00 00          |
    | xor dword [rsp + 4 * r15], 0x00000001              | 42 81 34 bc 01 00 00 00             |
    | xor dword [rax + 1 * rcx + 0x00], 0x00000001       | 81 74 08 00 01 00 00 00             |
    | xor dword [rax + 1 * rcx - 0x00], 0x00000001       | 81 74 08 00 01 00 00 00             |
    | xor dword [rax + 1 * rcx + 0x01], 0x00000001       | 81 74 08 01 01 00 00 00             |
    | xor dword [rax + 1 * rcx - 0x01], 0x00000001       | 81 74 08 ff 01 00 00 00             |
    | xor dword [rax + 1 * rcx + 0x00000001], 0x00000001 | 81 b4 08 01 00 00 00 01 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x00000001], 0x00000001 | 81 b4 08 ff ff ff ff 01 00 00 00    |
    | xor dword [rax + 1 * rcx + 0x7f], 0x00000001       | 81 74 08 7f 01 00 00 00             |
    | xor dword [rax + 1 * rcx - 0x7f], 0x00000001       | 81 74 08 81 01 00 00 00             |
    | xor dword [rax + 1 * rcx + 0x80], 0x00000001       | 81 b4 08 80 00 00 00 01 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x80], 0x00000001       | 81 74 08 80 01 00 00 00             |
    | xor dword [rax + 1 * rcx - 0x81], 0x00000001       | 81 b4 08 7f ff ff ff 01 00 00 00    |
    | xor dword [rax + 1 * rcx + 0xff], 0x00000001       | 81 b4 08 ff 00 00 00 01 00 00 00    |
    | xor dword [rax + 1 * rcx - 0xff], 0x00000001       | 81 b4 08 01 ff ff ff 01 00 00 00    |
    | xor dword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 81 b4 08 ff ff ff 7f 01 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 81 b4 08 01 00 00 80 01 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x80000000], 0x00000001 | 81 b4 08 00 00 00 80 01 00 00 00    |
    | xor dword [r10 + 0x7f], 0x00000001                 | 41 81 72 7f 01 00 00 00             |
    | xor dword [r10 + 0x80], 0x00000001                 | 41 81 b2 80 00 00 00 01 00 00 00    |
    | xor dword [r10 - 0x80], 0x00000001                 | 41 81 72 80 01 00 00 00             |
    | xor dword [r10 - 0x81], 0x00000001                 | 41 81 b2 7f ff ff ff 01 00 00 00    |
    | xor dword [rax], 0x00000000                        | 81 30 00 00 00 00                   |
    | xor dword [rax], 0x0000007f                        | 81 30 7f 00 00 00                   |
    | xor dword [rax], 0x00000080                        | 81 30 80 00 00 00                   |
    | xor dword [rax], 0x000000ff                        | 81 30 ff 00 00 00                   |
    | xor dword [rax], 0x00000100                        | 81 30 00 01 00 00                   |
    | xor dword [rax], 0x00007fff                        | 81 30 ff 7f 00 00                   |
    | xor dword [rax], 0x00008000                        | 81 30 00 80 00 00                   |
    | xor dword [rax], 0x0000ffff                        | 81 30 ff ff 00 00                   |
    | xor dword [rax], 0x00010000                        | 81 30 00 00 01 00                   |
    | xor dword [rax], 0x7fffffff                        | 81 30 ff ff ff 7f                   |
    | xor dword [rax], 0x80000000                        | 81 30 00 00 00 80                   |
    | xor dword [rax], 0xffffffff                        | 81 30 ff ff ff ff                   |
    | xor dword [rcx], 0x0000007f                        | 81 31 7f 00 00 00                   |
    | xor dword [rdx], 0x00000080                        | 81 32 80 00 00 00                   |
    | xor dword [rbx], 0x000000ff                        | 81 33 ff 00 00 00                   |
    | xor dword [rsp], 0x00000100                        | 81 34 24 00 01 00 00                |
    | xor dword [rbp], 0x00007fff                        | 81 75 00 ff 7f 00 00                |
    | xor dword [rsi], 0x00008000                        | 81 36 00 80 00 00                   |
    | xor dword [rdi], 0x0000ffff                        | 81 37 ff ff 00 00                   |
    | xor dword [r8], 0x00010000                         | 41 81 30 00 00 01 00                |
    | xor dword [r9], 0x7fffffff                         | 41 81 31 ff ff ff 7f                |
    | xor dword [r10], 0x80000000                        | 41 81 32 00 00 00 80                |
    | xor dword [r11], 0xffffffff                        | 41 81 33 ff ff ff ff                |
    | xor dword [r12], 0x00000000                        | 41 81 34 24 00 00 00 00             |
    | xor dword [r14], 0x0000007f                        | 41 81 36 7f 00 00 00                |
    | xor dword [r15], 0x00000080                        | 41 81 37 80 00 00 00                |
    | xor dword [rax + 1 * rcx], 0x000000ff              | 81 34 08 ff 00 00 00                |
    | xor dword [rcx + 1 * rcx], 0x00000100              | 81 34 09 00 01 00 00                |
    | xor dword [rdx + 1 * rcx], 0x00007fff              | 81 34 0a ff 7f 00 00                |
    | xor dword [rbx + 1 * rcx], 0x00008000              | 81 34 0b 00 80 00 00                |
    | xor dword [rsp + 1 * rcx], 0x0000ffff              | 81 34 0c ff ff 00 00                |
    | xor dword [rbp + 1 * rcx], 0x00010000              | 81 74 0d 00 00 00 01 00             |
    | xor dword [rsi + 1 * rcx], 0x7fffffff              | 81 34 0e ff ff ff 7f                |
    | xor dword [rdi + 1 * rcx], 0x80000000              | 81 34 0f 00 00 00 80                |
    | xor dword [r8 + 1 * rcx], 0xffffffff               | 41 81 34 08 ff ff ff ff             |
    | xor dword [r9 + 1 * rcx], 0x00000000               | 41 81 34 09 00 00 00 00             |
    | xor dword [r11 + 1 * rcx], 0x0000007f              | 41 81 34 0b 7f 00 00 00             |
    | xor dword [r12 + 1 * rcx], 0x00000080              | 41 81 34 0c 80 00 00 00             |
    | xor dword [r13 + 1 * rcx], 0x000000ff              | 41 81 74 0d 00 ff 00 00 00          |
    | xor dword [r14 + 1 * rcx], 0x00000100              | 41 81 34 0e 00 01 00 00             |
    | xor dword [r15 + 1 * rcx], 0x00007fff              | 41 81 34 0f ff 7f 00 00             |
    | xor dword [rax + 1 * rax], 0x00008000              | 81 34 00 00 80 00 00                |
    | xor dword [rax + 1 * rdx], 0x0000ffff              | 81 34 10 ff ff 00 00                |
    | xor dword [rax + 1 * rbx], 0x00010000              | 81 34 18 00 00 01 00                |
    | xor dword [rax + 1 * rbp], 0x7fffffff              | 81 34 28 ff ff ff 7f                |
    | xor dword [rax + 1 * rsi], 0x80000000              | 81 34 30 00 00 00 80                |
    | xor dword [rax + 1 * rdi], 0xffffffff              | 81 34 38 ff ff ff ff                |
    | xor dword [rax + 1 * r8], 0x00000000               | 42 81 34 00 00 00 00 00             |
    | xor dword [rax + 1 * r10], 0x0000007f              | 42 81 34 10 7f 00 00 00             |
    | xor dword [rax + 1 * r11], 0x00000080              | 42 81 34 18 80 00 00 00             |
    | xor dword [rax + 1 * r12], 0x000000ff              | 42 81 34 20 ff 00 00 00             |
    | xor dword [rax + 1 * r13], 0x00000100              | 42 81 34 28 00 01 00 00             |
    | xor dword [rax + 1 * r14], 0x00007fff              | 42 81 34 30 ff 7f 00 00             |
    | xor dword [rax + 1 * r15], 0x00008000              | 42 81 34 38 00 80 00 00             |
    | xor dword [rax + 2 * rcx], 0x0000ffff              | 81 34 48 ff ff 00 00                |
    | xor dword [rax + 4 * rcx], 0x00010000              | 81 34 88 00 00 01 00                |
    | xor dword [rax + 8 * rcx], 0x7fffffff              | 81 34 c8 ff ff ff 7f                |
    | xor dword [r8 + 1 * r9], 0x80000000                | 43 81 34 08 00 00 00 80             |
    | xor dword [r8 + 2 * r9], 0xffffffff                | 43 81 34 48 ff ff ff ff             |
    | xor dword [r8 + 4 * r9], 0x00000000                | 43 81 34 88 00 00 00 00             |
    | xor dword [1 * rcx], 0x0000007f                    | 81 34 0d 00 00 00 00 7f 00 00 00    |
    | xor dword [2 * rcx], 0x00000080                    | 81 34 4d 00 00 00 00 80 00 00 00    |
    | xor dword [4 * rcx], 0x000000ff                    | 81 34 8d 00 00 00 00 ff 00 00 00    |
    | xor dword [8 * rcx], 0x00000100                    | 81 34 cd 00 00 00 00 00 01 00 00    |
    | xor dword [1 * r9], 0x00007fff                     | 42 81 34 0d 00 00 00 00 ff 7f 00 00 |
    | xor dword [2 * r9], 0x00008000                     | 42 81 34 4d 00 00 00 00 00 80 00 00 |
    | xor dword [4 * r9], 0x0000ffff                     | 42 81 34 8d 00 00 00 00 ff ff 00 00 |
    | xor dword [8 * r9], 0x00010000                     | 42 81 34 cd 00 00 00 00 00 00 01 00 |
    | xor dword [r13 + 8 * r12], 0x7fffffff              | 43 81 74 e5 00 ff ff ff 7f          |
    | xor dword [rsp + 4 * r15], 0x80000000              | 42 81 34 bc 00 00 00 80             |
    | xor dword [rax + 1 * rcx + 0x00], 0xffffffff       | 81 74 08 00 ff ff ff ff             |
    | xor dword [rax + 1 * rcx - 0x00], 0x00000000       | 81 74 08 00 00 00 00 00             |
    | xor dword [rax + 1 * rcx - 0x01], 0x0000007f       | 81 74 08 ff 7f 00 00 00             |
    | xor dword [rax + 1 * rcx + 0x00000001], 0x00000080 | 81 b4 08 01 00 00 00 80 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x00000001], 0x000000ff | 81 b4 08 ff ff ff ff ff 00 00 00    |
    | xor dword [rax + 1 * rcx + 0x7f], 0x00000100       | 81 74 08 7f 00 01 00 00             |
    | xor dword [rax + 1 * rcx - 0x7f], 0x00007fff       | 81 74 08 81 ff 7f 00 00             |
    | xor dword [rax + 1 * rcx + 0x80], 0x00008000       | 81 b4 08 80 00 00 00 00 80 00 00    |
    | xor dword [rax + 1 * rcx - 0x80], 0x0000ffff       | 81 74 08 80 ff ff 00 00             |
    | xor dword [rax + 1 * rcx - 0x81], 0x00010000       | 81 b4 08 7f ff ff ff 00 00 01 00    |
    | xor dword [rax + 1 * rcx + 0xff], 0x7fffffff       | 81 b4 08 ff 00 00 00 ff ff ff 7f    |
    | xor dword [rax + 1 * rcx - 0xff], 0x80000000       | 81 b4 08 01 ff ff ff 00 00 00 80    |
    | xor dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 81 b4 08 ff ff ff 7f ff ff ff ff    |
    | xor dword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 81 b4 08 01 00 00 80 00 00 00 00    |
    | xor dword [r10 + 0x7f], 0x0000007f                 | 41 81 72 7f 7f 00 00 00             |
    | xor dword [r10 + 0x80], 0x00000080                 | 41 81 b2 80 00 00 00 80 00 00 00    |
    | xor dword [r10 - 0x80], 0x000000ff                 | 41 81 72 80 ff 00 00 00             |
    | xor dword [r10 - 0x81], 0x00000100                 | 41 81 b2 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_xor_addr32_imm32():
    encode(XOR_ADDR32_IMM32)


XOR_ADDR32_REG32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | xor dword [rax], ecx                         | 31 08                   |
    | xor dword [rcx], ecx                         | 31 09                   |
    | xor dword [rdx], ecx                         | 31 0a                   |
    | xor dword [rbx], ecx                         | 31 0b                   |
    | xor dword [rsp], ecx                         | 31 0c 24                |
    | xor dword [rbp], ecx                         | 31 4d 00                |
    | xor dword [rsi], ecx                         | 31 0e                   |
    | xor dword [rdi], ecx                         | 31 0f                   |
    | xor dword [r8], ecx                          | 41 31 08                |
    | xor dword [r9], ecx                          | 41 31 09                |
    | xor dword [r10], ecx                         | 41 31 0a                |
    | xor dword [r11], ecx                         | 41 31 0b                |
    | xor dword [r12], ecx                         | 41 31 0c 24             |
    | xor dword [r13], ecx                         | 41 31 4d 00             |
    | xor dword [r14], ecx                         | 41 31 0e                |
    | xor dword [r15], ecx                         | 41 31 0f                |
    | xor dword [rax + 1 * rcx], ecx               | 31 0c 08                |
    | xor dword [rcx + 1 * rcx], ecx               | 31 0c 09                |
    | xor dword [rdx + 1 * rcx], ecx               | 31 0c 0a                |
    | xor dword [rbx + 1 * rcx], ecx               | 31 0c 0b                |
    | xor dword [rsp + 1 * rcx], ecx               | 31 0c 0c                |
    | xor dword [rbp + 1 * rcx], ecx               | 31 4c 0d 00             |
    | xor dword [rsi + 1 * rcx], ecx               | 31 0c 0e                |
    | xor dword [rdi + 1 * rcx], ecx               | 31 0c 0f                |
    | xor dword [r8 + 1 * rcx], ecx                | 41 31 0c 08             |
    | xor dword [r9 + 1 * rcx], ecx                | 41 31 0c 09             |
    | xor dword [r10 + 1 * rcx], ecx               | 41 31 0c 0a             |
    | xor dword [r11 + 1 * rcx], ecx               | 41 31 0c 0b             |
    | xor dword [r12 + 1 * rcx], ecx               | 41 31 0c 0c             |
    | xor dword [r13 + 1 * rcx], ecx               | 41 31 4c 0d 00          |
    | xor dword [r14 + 1 * rcx], ecx               | 41 31 0c 0e             |
    | xor dword [r15 + 1 * rcx], ecx               | 41 31 0c 0f             |
    | xor dword [rax + 1 * rax], ecx               | 31 0c 00                |
    | xor dword [rax + 1 * rdx], ecx               | 31 0c 10                |
    | xor dword [rax + 1 * rbx], ecx               | 31 0c 18                |
    | xor dword [rax + 1 * rbp], ecx               | 31 0c 28                |
    | xor dword [rax + 1 * rsi], ecx               | 31 0c 30                |
    | xor dword [rax + 1 * rdi], ecx               | 31 0c 38                |
    | xor dword [rax + 1 * r8], ecx                | 42 31 0c 00             |
    | xor dword [rax + 1 * r9], ecx                | 42 31 0c 08             |
    | xor dword [rax + 1 * r10], ecx               | 42 31 0c 10             |
    | xor dword [rax + 1 * r11], ecx               | 42 31 0c 18             |
    | xor dword [rax + 1 * r12], ecx               | 42 31 0c 20             |
    | xor dword [rax + 1 * r13], ecx               | 42 31 0c 28             |
    | xor dword [rax + 1 * r14], ecx               | 42 31 0c 30             |
    | xor dword [rax + 1 * r15], ecx               | 42 31 0c 38             |
    | xor dword [rax + 2 * rcx], ecx               | 31 0c 48                |
    | xor dword [rax + 4 * rcx], ecx               | 31 0c 88                |
    | xor dword [rax + 8 * rcx], ecx               | 31 0c c8                |
    | xor dword [r8 + 1 * r9], ecx                 | 43 31 0c 08             |
    | xor dword [r8 + 2 * r9], ecx                 | 43 31 0c 48             |
    | xor dword [r8 + 4 * r9], ecx                 | 43 31 0c 88             |
    | xor dword [r8 + 8 * r9], ecx                 | 43 31 0c c8             |
    | xor dword [1 * rcx], ecx                     | 31 0c 0d 00 00 00 00    |
    | xor dword [2 * rcx], ecx                     | 31 0c 4d 00 00 00 00    |
    | xor dword [4 * rcx], ecx                     | 31 0c 8d 00 00 00 00    |
    | xor dword [8 * rcx], ecx                     | 31 0c cd 00 00 00 00    |
    | xor dword [1 * r9], ecx                      | 42 31 0c 0d 00 00 00 00 |
    | xor dword [2 * r9], ecx                      | 42 31 0c 4d 00 00 00 00 |
    | xor dword [4 * r9], ecx                      | 42 31 0c 8d 00 00 00 00 |
    | xor dword [8 * r9], ecx                      | 42 31 0c cd 00 00 00 00 |
    | xor dword [r13 + 8 * r12], ecx               | 43 31 4c e5 00          |
    | xor dword [rsp + 4 * r15], ecx               | 42 31 0c bc             |
    | xor dword [rax + 1 * rcx + 0x00], ecx        | 31 4c 08 00             |
    | xor dword [rax + 1 * rcx - 0x00], ecx        | 31 4c 08 00             |
    | xor dword [rax + 1 * rcx + 0x01], ecx        | 31 4c 08 01             |
    | xor dword [rax + 1 * rcx - 0x01], ecx        | 31 4c 08 ff             |
    | xor dword [rax + 1 * rcx + 0x00000001], ecx  | 31 8c 08 01 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x00000001], ecx  | 31 8c 08 ff ff ff ff    |
    | xor dword [rax + 1 * rcx + 0x7f], ecx        | 31 4c 08 7f             |
    | xor dword [rax + 1 * rcx - 0x7f], ecx        | 31 4c 08 81             |
    | xor dword [rax + 1 * rcx + 0x80], ecx        | 31 8c 08 80 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x80], ecx        | 31 4c 08 80             |
    | xor dword [rax + 1 * rcx - 0x81], ecx        | 31 8c 08 7f ff ff ff    |
    | xor dword [rax + 1 * rcx + 0xff], ecx        | 31 8c 08 ff 00 00 00    |
    | xor dword [rax + 1 * rcx - 0xff], ecx        | 31 8c 08 01 ff ff ff    |
    | xor dword [rax + 1 * rcx + 0x7fffffff], ecx  | 31 8c 08 ff ff ff 7f    |
    | xor dword [rax + 1 * rcx - 0x7fffffff], ecx  | 31 8c 08 01 00 00 80    |
    | xor dword [rax + 1 * rcx - 0x80000000], ecx  | 31 8c 08 00 00 00 80    |
    | xor dword [r10 + 0x7f], ecx                  | 41 31 4a 7f             |
    | xor dword [r10 + 0x80], ecx                  | 41 31 8a 80 00 00 00    |
    | xor dword [r10 - 0x80], ecx                  | 41 31 4a 80             |
    | xor dword [r10 - 0x81], ecx                  | 41 31 8a 7f ff ff ff    |
    | xor dword [rax], eax                         | 31 00                   |
    | xor dword [rax], edx                         | 31 10                   |
    | xor dword [rax], ebx                         | 31 18                   |
    | xor dword [rax], esp                         | 31 20                   |
    | xor dword [rax], ebp                         | 31 28                   |
    | xor dword [rax], esi                         | 31 30                   |
    | xor dword [rax], edi                         | 31 38                   |
    | xor dword [rax], r8d                         | 44 31 00                |
    | xor dword [rax], r9d                         | 44 31 08                |
    | xor dword [rax], r10d                        | 44 31 10                |
    | xor dword [rax], r11d                        | 44 31 18                |
    | xor dword [rax], r12d                        | 44 31 20                |
    | xor dword [rax], r13d                        | 44 31 28                |
    | xor dword [rax], r14d                        | 44 31 30                |
    | xor dword [rax], r15d                        | 44 31 38                |
    | xor dword [rcx], edx                         | 31 11                   |
    | xor dword [rdx], ebx                         | 31 1a                   |
    | xor dword [rbx], esp                         | 31 23                   |
    | xor dword [rsp], ebp                         | 31 2c 24                |
    | xor dword [rbp], esi                         | 31 75 00                |
    | xor dword [rsi], edi                         | 31 3e                   |
    | xor dword [rdi], r8d                         | 44 31 07                |
    | xor dword [r8], r9d                          | 45 31 08                |
    | xor dword [r9], r10d                         | 45 31 11                |
    | xor dword [r10], r11d                        | 45 31 1a                |
    | xor dword [r11], r12d                        | 45 31 23                |
    | xor dword [r12], r13d                        | 45 31 2c 24             |
    | xor dword [r13], r14d                        | 45 31 75 00             |
    | xor dword [r14], r15d                        | 45 31 3e                |
    | xor dword [r15], eax                         | 41 31 07                |
    | xor dword [rcx + 1 * rcx], edx               | 31 14 09                |
    | xor dword [rdx + 1 * rcx], ebx               | 31 1c 0a                |
    | xor dword [rbx + 1 * rcx], esp               | 31 24 0b                |
    | xor dword [rsp + 1 * rcx], ebp               | 31 2c 0c                |
    | xor dword [rbp + 1 * rcx], esi               | 31 74 0d 00             |
    | xor dword [rsi + 1 * rcx], edi               | 31 3c 0e                |
    | xor dword [rdi + 1 * rcx], r8d               | 44 31 04 0f             |
    | xor dword [r8 + 1 * rcx], r9d                | 45 31 0c 08             |
    | xor dword [r9 + 1 * rcx], r10d               | 45 31 14 09             |
    | xor dword [r10 + 1 * rcx], r11d              | 45 31 1c 0a             |
    | xor dword [r11 + 1 * rcx], r12d              | 45 31 24 0b             |
    | xor dword [r12 + 1 * rcx], r13d              | 45 31 2c 0c             |
    | xor dword [r13 + 1 * rcx], r14d              | 45 31 74 0d 00          |
    | xor dword [r14 + 1 * rcx], r15d              | 45 31 3c 0e             |
    | xor dword [r15 + 1 * rcx], eax               | 41 31 04 0f             |
    | xor dword [rax + 1 * rdx], edx               | 31 14 10                |
    | xor dword [rax + 1 * rbx], ebx               | 31 1c 18                |
    | xor dword [rax + 1 * rbp], esp               | 31 24 28                |
    | xor dword [rax + 1 * rsi], ebp               | 31 2c 30                |
    | xor dword [rax + 1 * rdi], esi               | 31 34 38                |
    | xor dword [rax + 1 * r8], edi                | 42 31 3c 00             |
    | xor dword [rax + 1 * r9], r8d                | 46 31 04 08             |
    | xor dword [rax + 1 * r10], r9d               | 46 31 0c 10             |
    | xor dword [rax + 1 * r11], r10d              | 46 31 14 18             |
    | xor dword [rax + 1 * r12], r11d              | 46 31 1c 20             |
    | xor dword [rax + 1 * r13], r12d              | 46 31 24 28             |
    | xor dword [rax + 1 * r14], r13d              | 46 31 2c 30             |
    | xor dword [rax + 1 * r15], r14d              | 46 31 34 38             |
    | xor dword [rax + 2 * rcx], r15d              | 44 31 3c 48             |
    | xor dword [rax + 4 * rcx], eax               | 31 04 88                |
    | xor dword [r8 + 1 * r9], edx                 | 43 31 14 08             |
    | xor dword [r8 + 2 * r9], ebx                 | 43 31 1c 48             |
    | xor dword [r8 + 4 * r9], esp                 | 43 31 24 88             |
    | xor dword [r8 + 8 * r9], ebp                 | 43 31 2c c8             |
    | xor dword [1 * rcx], esi                     | 31 34 0d 00 00 00 00    |
    | xor dword [2 * rcx], edi                     | 31 3c 4d 00 00 00 00    |
    | xor dword [4 * rcx], r8d                     | 44 31 04 8d 00 00 00 00 |
    | xor dword [8 * rcx], r9d                     | 44 31 0c cd 00 00 00 00 |
    | xor dword [1 * r9], r10d                     | 46 31 14 0d 00 00 00 00 |
    | xor dword [2 * r9], r11d                     | 46 31 1c 4d 00 00 00 00 |
    | xor dword [4 * r9], r12d                     | 46 31 24 8d 00 00 00 00 |
    | xor dword [8 * r9], r13d                     | 46 31 2c cd 00 00 00 00 |
    | xor dword [r13 + 8 * r12], r14d              | 47 31 74 e5 00          |
    | xor dword [rsp + 4 * r15], r15d              | 46 31 3c bc             |
    | xor dword [rax + 1 * rcx + 0x00], eax        | 31 44 08 00             |
    | xor dword [rax + 1 * rcx + 0x01], edx        | 31 54 08 01             |
    | xor dword [rax + 1 * rcx - 0x01], ebx        | 31 5c 08 ff             |
    | xor dword [rax + 1 * rcx + 0x00000001], esp  | 31 a4 08 01 00 00 00    |
    | xor dword [rax + 1 * rcx - 0x00000001], ebp  | 31 ac 08 ff ff ff ff    |
    | xor dword [rax + 1 * rcx + 0x7f], esi        | 31 74 08 7f             |
    | xor dword [rax + 1 * rcx - 0x7f], edi        | 31 7c 08 81             |
    | xor dword [rax + 1 * rcx + 0x80], r8d        | 44 31 84 08 80 00 00 00 |
    | xor dword [rax + 1 * rcx - 0x80], r9d        | 44 31 4c 08 80          |
    | xor dword [rax + 1 * rcx - 0x81], r10d       | 44 31 94 08 7f ff ff ff |
    | xor dword [rax + 1 * rcx + 0xff], r11d       | 44 31 9c 08 ff 00 00 00 |
    | xor dword [rax + 1 * rcx - 0xff], r12d       | 44 31 a4 08 01 ff ff ff |
    | xor dword [rax + 1 * rcx + 0x7fffffff], r13d | 44 31 ac 08 ff ff ff 7f |
    | xor dword [rax + 1 * rcx - 0x7fffffff], r14d | 44 31 b4 08 01 00 00 80 |
    | xor dword [rax + 1 * rcx - 0x80000000], r15d | 44 31 bc 08 00 00 00 80 |
    | xor dword [r10 + 0x7f], eax                  | 41 31 42 7f             |
    | xor dword [r10 - 0x80], edx                  | 41 31 52 80             |
    | xor dword [r10 - 0x81], ebx                  | 41 31 9a 7f ff ff ff    |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_xor_addr32_reg32():
    encode(XOR_ADDR32_REG32)


XOR_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | xor word [rax], 0x01                        | 66 83 30 01                   |
    | xor word [rcx], 0x01                        | 66 83 31 01                   |
    | xor word [rdx], 0x01                        | 66 83 32 01                   |
    | xor word [rbx], 0x01                        | 66 83 33 01                   |
    | xor word [rsp], 0x01                        | 66 83 34 24 01                |
    | xor word [rbp], 0x01                        | 66 83 75 00 01                |
    | xor word [rsi], 0x01                        | 66 83 36 01                   |
    | xor word [rdi], 0x01                        | 66 83 37 01                   |
    | xor word [r8], 0x01                         | 66 41 83 30 01                |
    | xor word [r9], 0x01                         | 66 41 83 31 01                |
    | xor word [r10], 0x01                        | 66 41 83 32 01                |
    | xor word [r11], 0x01                        | 66 41 83 33 01                |
    | xor word [r12], 0x01                        | 66 41 83 34 24 01             |
    | xor word [r13], 0x01                        | 66 41 83 75 00 01             |
    | xor word [r14], 0x01                        | 66 41 83 36 01                |
    | xor word [r15], 0x01                        | 66 41 83 37 01                |
    | xor word [rax + 1 * rcx], 0x01              | 66 83 34 08 01                |
    | xor word [rcx + 1 * rcx], 0x01              | 66 83 34 09 01                |
    | xor word [rdx + 1 * rcx], 0x01              | 66 83 34 0a 01                |
    | xor word [rbx + 1 * rcx], 0x01              | 66 83 34 0b 01                |
    | xor word [rsp + 1 * rcx], 0x01              | 66 83 34 0c 01                |
    | xor word [rbp + 1 * rcx], 0x01              | 66 83 74 0d 00 01             |
    | xor word [rsi + 1 * rcx], 0x01              | 66 83 34 0e 01                |
    | xor word [rdi + 1 * rcx], 0x01              | 66 83 34 0f 01                |
    | xor word [r8 + 1 * rcx], 0x01               | 66 41 83 34 08 01             |
    | xor word [r9 + 1 * rcx], 0x01               | 66 41 83 34 09 01             |
    | xor word [r10 + 1 * rcx], 0x01              | 66 41 83 34 0a 01             |
    | xor word [r11 + 1 * rcx], 0x01              | 66 41 83 34 0b 01             |
    | xor word [r12 + 1 * rcx], 0x01              | 66 41 83 34 0c 01             |
    | xor word [r13 + 1 * rcx], 0x01              | 66 41 83 74 0d 00 01          |
    | xor word [r14 + 1 * rcx], 0x01              | 66 41 83 34 0e 01             |
    | xor word [r15 + 1 * rcx], 0x01              | 66 41 83 34 0f 01             |
    | xor word [rax + 1 * rax], 0x01              | 66 83 34 00 01                |
    | xor word [rax + 1 * rdx], 0x01              | 66 83 34 10 01                |
    | xor word [rax + 1 * rbx], 0x01              | 66 83 34 18 01                |
    | xor word [rax + 1 * rbp], 0x01              | 66 83 34 28 01                |
    | xor word [rax + 1 * rsi], 0x01              | 66 83 34 30 01                |
    | xor word [rax + 1 * rdi], 0x01              | 66 83 34 38 01                |
    | xor word [rax + 1 * r8], 0x01               | 66 42 83 34 00 01             |
    | xor word [rax + 1 * r9], 0x01               | 66 42 83 34 08 01             |
    | xor word [rax + 1 * r10], 0x01              | 66 42 83 34 10 01             |
    | xor word [rax + 1 * r11], 0x01              | 66 42 83 34 18 01             |
    | xor word [rax + 1 * r12], 0x01              | 66 42 83 34 20 01             |
    | xor word [rax + 1 * r13], 0x01              | 66 42 83 34 28 01             |
    | xor word [rax + 1 * r14], 0x01              | 66 42 83 34 30 01             |
    | xor word [rax + 1 * r15], 0x01              | 66 42 83 34 38 01             |
    | xor word [rax + 2 * rcx], 0x01              | 66 83 34 48 01                |
    | xor word [rax + 4 * rcx], 0x01              | 66 83 34 88 01                |
    | xor word [rax + 8 * rcx], 0x01              | 66 83 34 c8 01                |
    | xor word [r8 + 1 * r9], 0x01                | 66 43 83 34 08 01             |
    | xor word [r8 + 2 * r9], 0x01                | 66 43 83 34 48 01             |
    | xor word [r8 + 4 * r9], 0x01                | 66 43 83 34 88 01             |
    | xor word [r8 + 8 * r9], 0x01                | 66 43 83 34 c8 01             |
    | xor word [1 * rcx], 0x01                    | 66 83 34 0d 00 00 00 00 01    |
    | xor word [2 * rcx], 0x01                    | 66 83 34 4d 00 00 00 00 01    |
    | xor word [4 * rcx], 0x01                    | 66 83 34 8d 00 00 00 00 01    |
    | xor word [8 * rcx], 0x01                    | 66 83 34 cd 00 00 00 00 01    |
    | xor word [1 * r9], 0x01                     | 66 42 83 34 0d 00 00 00 00 01 |
    | xor word [2 * r9], 0x01                     | 66 42 83 34 4d 00 00 00 00 01 |
    | xor word [4 * r9], 0x01                     | 66 42 83 34 8d 00 00 00 00 01 |
    | xor word [8 * r9], 0x01                     | 66 42 83 34 cd 00 00 00 00 01 |
    | xor word [r13 + 8 * r12], 0x01              | 66 43 83 74 e5 00 01          |
    | xor word [rsp + 4 * r15], 0x01              | 66 42 83 34 bc 01             |
    | xor word [rax + 1 * rcx + 0x00], 0x01       | 66 83 74 08 00 01             |
    | xor word [rax + 1 * rcx - 0x00], 0x01       | 66 83 74 08 00 01             |
    | xor word [rax + 1 * rcx + 0x01], 0x01       | 66 83 74 08 01 01             |
    | xor word [rax + 1 * rcx - 0x01], 0x01       | 66 83 74 08 ff 01             |
    | xor word [rax + 1 * rcx + 0x00000001], 0x01 | 66 83 b4 08 01 00 00 00 01    |
    | xor word [rax + 1 * rcx - 0x00000001], 0x01 | 66 83 b4 08 ff ff ff ff 01    |
    | xor word [rax + 1 * rcx + 0x7f], 0x01       | 66 83 74 08 7f 01             |
    | xor word [rax + 1 * rcx - 0x7f], 0x01       | 66 83 74 08 81 01             |
    | xor word [rax + 1 * rcx + 0x80], 0x01       | 66 83 b4 08 80 00 00 00 01    |
    | xor word [rax + 1 * rcx - 0x80], 0x01       | 66 83 74 08 80 01             |
    | xor word [rax + 1 * rcx - 0x81], 0x01       | 66 83 b4 08 7f ff ff ff 01    |
    | xor word [rax + 1 * rcx + 0xff], 0x01       | 66 83 b4 08 ff 00 00 00 01    |
    | xor word [rax + 1 * rcx - 0xff], 0x01       | 66 83 b4 08 01 ff ff ff 01    |
    | xor word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 83 b4 08 ff ff ff 7f 01    |
    | xor word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 83 b4 08 01 00 00 80 01    |
    | xor word [rax + 1 * rcx - 0x80000000], 0x01 | 66 83 b4 08 00 00 00 80 01    |
    | xor word [r10 + 0x7f], 0x01                 | 66 41 83 72 7f 01             |
    | xor word [r10 + 0x80], 0x01                 | 66 41 83 b2 80 00 00 00 01    |
    | xor word [r10 - 0x80], 0x01                 | 66 41 83 72 80 01             |
    | xor word [r10 - 0x81], 0x01                 | 66 41 83 b2 7f ff ff ff 01    |
    | xor word [rax], 0x00                        | 66 83 30 00                   |
    | xor word [rax], 0x7f                        | 66 83 30 7f                   |
    | xor word [rax], 0x80                        | 66 83 30 80                   |
    | xor word [rax], 0xff                        | 66 83 30 ff                   |
    | xor word [rcx], 0x7f                        | 66 83 31 7f                   |
    | xor word [rdx], 0x80                        | 66 83 32 80                   |
    | xor word [rbx], 0xff                        | 66 83 33 ff                   |
    | xor word [rsp], 0x00                        | 66 83 34 24 00                |
    | xor word [rsi], 0x7f                        | 66 83 36 7f                   |
    | xor word [rdi], 0x80                        | 66 83 37 80                   |
    | xor word [r8], 0xff                         | 66 41 83 30 ff                |
    | xor word [r9], 0x00                         | 66 41 83 31 00                |
    | xor word [r11], 0x7f                        | 66 41 83 33 7f                |
    | xor word [r12], 0x80                        | 66 41 83 34 24 80             |
    | xor word [r13], 0xff                        | 66 41 83 75 00 ff             |
    | xor word [r14], 0x00                        | 66 41 83 36 00                |
    | xor word [rax + 1 * rcx], 0x7f              | 66 83 34 08 7f                |
    | xor word [rcx + 1 * rcx], 0x80              | 66 83 34 09 80                |
    | xor word [rdx + 1 * rcx], 0xff              | 66 83 34 0a ff                |
    | xor word [rbx + 1 * rcx], 0x00              | 66 83 34 0b 00                |
    | xor word [rbp + 1 * rcx], 0x7f              | 66 83 74 0d 00 7f             |
    | xor word [rsi + 1 * rcx], 0x80              | 66 83 34 0e 80                |
    | xor word [rdi + 1 * rcx], 0xff              | 66 83 34 0f ff                |
    | xor word [r8 + 1 * rcx], 0x00               | 66 41 83 34 08 00             |
    | xor word [r10 + 1 * rcx], 0x7f              | 66 41 83 34 0a 7f             |
    | xor word [r11 + 1 * rcx], 0x80              | 66 41 83 34 0b 80             |
    | xor word [r12 + 1 * rcx], 0xff              | 66 41 83 34 0c ff             |
    | xor word [r13 + 1 * rcx], 0x00              | 66 41 83 74 0d 00 00          |
    | xor word [r15 + 1 * rcx], 0x7f              | 66 41 83 34 0f 7f             |
    | xor word [rax + 1 * rax], 0x80              | 66 83 34 00 80                |
    | xor word [rax + 1 * rdx], 0xff              | 66 83 34 10 ff                |
    | xor word [rax + 1 * rbx], 0x00              | 66 83 34 18 00                |
    | xor word [rax + 1 * rsi], 0x7f              | 66 83 34 30 7f                |
    | xor word [rax + 1 * rdi], 0x80              | 66 83 34 38 80                |
    | xor word [rax + 1 * r8], 0xff               | 66 42 83 34 00 ff             |
    | xor word [rax + 1 * r9], 0x00               | 66 42 83 34 08 00             |
    | xor word [rax + 1 * r11], 0x7f              | 66 42 83 34 18 7f             |
    | xor word [rax + 1 * r12], 0x80              | 66 42 83 34 20 80             |
    | xor word [rax + 1 * r13], 0xff              | 66 42 83 34 28 ff             |
    | xor word [rax + 1 * r14], 0x00              | 66 42 83 34 30 00             |
    | xor word [rax + 2 * rcx], 0x7f              | 66 83 34 48 7f                |
    | xor word [rax + 4 * rcx], 0x80              | 66 83 34 88 80                |
    | xor word [rax + 8 * rcx], 0xff              | 66 83 34 c8 ff                |
    | xor word [r8 + 1 * r9], 0x00                | 66 43 83 34 08 00             |
    | xor word [r8 + 4 * r9], 0x7f                | 66 43 83 34 88 7f             |
    | xor word [r8 + 8 * r9], 0x80                | 66 43 83 34 c8 80             |
    | xor word [1 * rcx], 0xff                    | 66 83 34 0d 00 00 00 00 ff    |
    | xor word [2 * rcx], 0x00                    | 66 83 34 4d 00 00 00 00 00    |
    | xor word [8 * rcx], 0x7f                    | 66 83 34 cd 00 00 00 00 7f    |
    | xor word [1 * r9], 0x80                     | 66 42 83 34 0d 00 00 00 00 80 |
    | xor word [2 * r9], 0xff                     | 66 42 83 34 4d 00 00 00 00 ff |
    | xor word [4 * r9], 0x00                     | 66 42 83 34 8d 00 00 00 00 00 |
    | xor word [r13 + 8 * r12], 0x7f              | 66 43 83 74 e5 00 7f          |
    | xor word [rsp + 4 * r15], 0x80              | 66 42 83 34 bc 80             |
    | xor word [rax + 1 * rcx + 0x00], 0xff       | 66 83 74 08 00 ff             |
    | xor word [rax + 1 * rcx - 0x00], 0x00       | 66 83 74 08 00 00             |
    | xor word [rax + 1 * rcx - 0x01], 0x7f       | 66 83 74 08 ff 7f             |
    | xor word [rax + 1 * rcx + 0x00000001], 0x80 | 66 83 b4 08 01 00 00 00 80    |
    | xor word [rax + 1 * rcx - 0x00000001], 0xff | 66 83 b4 08 ff ff ff ff ff    |
    | xor word [rax + 1 * rcx + 0x7f], 0x00       | 66 83 74 08 7f 00             |
    | xor word [rax + 1 * rcx + 0x80], 0x7f       | 66 83 b4 08 80 00 00 00 7f    |
    | xor word [rax + 1 * rcx - 0x80], 0x80       | 66 83 74 08 80 80             |
    | xor word [rax + 1 * rcx - 0x81], 0xff       | 66 83 b4 08 7f ff ff ff ff    |
    | xor word [rax + 1 * rcx + 0xff], 0x00       | 66 83 b4 08 ff 00 00 00 00    |
    | xor word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 83 b4 08 ff ff ff 7f 7f    |
    | xor word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 83 b4 08 01 00 00 80 80    |
    | xor word [rax + 1 * rcx - 0x80000000], 0xff | 66 83 b4 08 00 00 00 80 ff    |
    | xor word [r10 + 0x7f], 0x00                 | 66 41 83 72 7f 00             |
    | xor word [r10 - 0x80], 0x7f                 | 66 41 83 72 80 7f             |
    | xor word [r10 - 0x81], 0x80                 | 66 41 83 b2 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_xor_addr16_imm8():
    encode(XOR_ADDR16_IMM8)


XOR_ADDR16_IMM16 = """
    | --------------------------------------------- | -------------------------------- |
    | instruction                                   | encoding                         |
    | --------------------------------------------- | -------------------------------- |
    | xor word [rax], 0x0001                        | 66 81 30 01 00                   |
    | xor word [rcx], 0x0001                        | 66 81 31 01 00                   |
    | xor word [rdx], 0x0001                        | 66 81 32 01 00                   |
    | xor word [rbx], 0x0001                        | 66 81 33 01 00                   |
    | xor word [rsp], 0x0001                        | 66 81 34 24 01 00                |
    | xor word [rbp], 0x0001                        | 66 81 75 00 01 00                |
    | xor word [rsi], 0x0001                        | 66 81 36 01 00                   |
    | xor word [rdi], 0x0001                        | 66 81 37 01 00                   |
    | xor word [r8], 0x0001                         | 66 41 81 30 01 00                |
    | xor word [r9], 0x0001                         | 66 41 81 31 01 00                |
    | xor word [r10], 0x0001                        | 66 41 81 32 01 00                |
    | xor word [r11], 0x0001                        | 66 41 81 33 01 00                |
    | xor word [r12], 0x0001                        | 66 41 81 34 24 01 00             |
    | xor word [r13], 0x0001                        | 66 41 81 75 00 01 00             |
    | xor word [r14], 0x0001                        | 66 41 81 36 01 00                |
    | xor word [r15], 0x0001                        | 66 41 81 37 01 00                |
    | xor word [rax + 1 * rcx], 0x0001              | 66 81 34 08 01 00                |
    | xor word [rcx + 1 * rcx], 0x0001              | 66 81 34 09 01 00                |
    | xor word [rdx + 1 * rcx], 0x0001              | 66 81 34 0a 01 00                |
    | xor word [rbx + 1 * rcx], 0x0001              | 66 81 34 0b 01 00                |
    | xor word [rsp + 1 * rcx], 0x0001              | 66 81 34 0c 01 00                |
    | xor word [rbp + 1 * rcx], 0x0001              | 66 81 74 0d 00 01 00             |
    | xor word [rsi + 1 * rcx], 0x0001              | 66 81 34 0e 01 00                |
    | xor word [rdi + 1 * rcx], 0x0001              | 66 81 34 0f 01 00                |
    | xor word [r8 + 1 * rcx], 0x0001               | 66 41 81 34 08 01 00             |
    | xor word [r9 + 1 * rcx], 0x0001               | 66 41 81 34 09 01 00             |
    | xor word [r10 + 1 * rcx], 0x0001              | 66 41 81 34 0a 01 00             |
    | xor word [r11 + 1 * rcx], 0x0001              | 66 41 81 34 0b 01 00             |
    | xor word [r12 + 1 * rcx], 0x0001              | 66 41 81 34 0c 01 00             |
    | xor word [r13 + 1 * rcx], 0x0001              | 66 41 81 74 0d 00 01 00          |
    | xor word [r14 + 1 * rcx], 0x0001              | 66 41 81 34 0e 01 00             |
    | xor word [r15 + 1 * rcx], 0x0001              | 66 41 81 34 0f 01 00             |
    | xor word [rax + 1 * rax], 0x0001              | 66 81 34 00 01 00                |
    | xor word [rax + 1 * rdx], 0x0001              | 66 81 34 10 01 00                |
    | xor word [rax + 1 * rbx], 0x0001              | 66 81 34 18 01 00                |
    | xor word [rax + 1 * rbp], 0x0001              | 66 81 34 28 01 00                |
    | xor word [rax + 1 * rsi], 0x0001              | 66 81 34 30 01 00                |
    | xor word [rax + 1 * rdi], 0x0001              | 66 81 34 38 01 00                |
    | xor word [rax + 1 * r8], 0x0001               | 66 42 81 34 00 01 00             |
    | xor word [rax + 1 * r9], 0x0001               | 66 42 81 34 08 01 00             |
    | xor word [rax + 1 * r10], 0x0001              | 66 42 81 34 10 01 00             |
    | xor word [rax + 1 * r11], 0x0001              | 66 42 81 34 18 01 00             |
    | xor word [rax + 1 * r12], 0x0001              | 66 42 81 34 20 01 00             |
    | xor word [rax + 1 * r13], 0x0001              | 66 42 81 34 28 01 00             |
    | xor word [rax + 1 * r14], 0x0001              | 66 42 81 34 30 01 00             |
    | xor word [rax + 1 * r15], 0x0001              | 66 42 81 34 38 01 00             |
    | xor word [rax + 2 * rcx], 0x0001              | 66 81 34 48 01 00                |
    | xor word [rax + 4 * rcx], 0x0001              | 66 81 34 88 01 00                |
    | xor word [rax + 8 * rcx], 0x0001              | 66 81 34 c8 01 00                |
    | xor word [r8 + 1 * r9], 0x0001                | 66 43 81 34 08 01 00             |
    | xor word [r8 + 2 * r9], 0x0001                | 66 43 81 34 48 01 00             |
    | xor word [r8 + 4 * r9], 0x0001                | 66 43 81 34 88 01 00             |
    | xor word [r8 + 8 * r9], 0x0001                | 66 43 81 34 c8 01 00             |
    | xor word [1 * rcx], 0x0001                    | 66 81 34 0d 00 00 00 00 01 00    |
    | xor word [2 * rcx], 0x0001                    | 66 81 34 4d 00 00 00 00 01 00    |
    | xor word [4 * rcx], 0x0001                    | 66 81 34 8d 00 00 00 00 01 00    |
    | xor word [8 * rcx], 0x0001                    | 66 81 34 cd 00 00 00 00 01 00    |
    | xor word [1 * r9], 0x0001                     | 66 42 81 34 0d 00 00 00 00 01 00 |
    | xor word [2 * r9], 0x0001                     | 66 42 81 34 4d 00 00 00 00 01 00 |
    | xor word [4 * r9], 0x0001                     | 66 42 81 34 8d 00 00 00 00 01 00 |
    | xor word [8 * r9], 0x0001                     | 66 42 81 34 cd 00 00 00 00 01 00 |
    | xor word [r13 + 8 * r12], 0x0001              | 66 43 81 74 e5 00 01 00          |
    | xor word [rsp + 4 * r15], 0x0001              | 66 42 81 34 bc 01 00             |
    | xor word [rax + 1 * rcx + 0x00], 0x0001       | 66 81 74 08 00 01 00             |
    | xor word [rax + 1 * rcx - 0x00], 0x0001       | 66 81 74 08 00 01 00             |
    | xor word [rax + 1 * rcx + 0x01], 0x0001       | 66 81 74 08 01 01 00             |
    | xor word [rax + 1 * rcx - 0x01], 0x0001       | 66 81 74 08 ff 01 00             |
    | xor word [rax + 1 * rcx + 0x00000001], 0x0001 | 66 81 b4 08 01 00 00 00 01 00    |
    | xor word [rax + 1 * rcx - 0x00000001], 0x0001 | 66 81 b4 08 ff ff ff ff 01 00    |
    | xor word [rax + 1 * rcx + 0x7f], 0x0001       | 66 81 74 08 7f 01 00             |
    | xor word [rax + 1 * rcx - 0x7f], 0x0001       | 66 81 74 08 81 01 00             |
    | xor word [rax + 1 * rcx + 0x80], 0x0001       | 66 81 b4 08 80 00 00 00 01 00    |
    | xor word [rax + 1 * rcx - 0x80], 0x0001       | 66 81 74 08 80 01 00             |
    | xor word [rax + 1 * rcx - 0x81], 0x0001       | 66 81 b4 08 7f ff ff ff 01 00    |
    | xor word [rax + 1 * rcx + 0xff], 0x0001       | 66 81 b4 08 ff 00 00 00 01 00    |
    | xor word [rax + 1 * rcx - 0xff], 0x0001       | 66 81 b4 08 01 ff ff ff 01 00    |
    | xor word [rax + 1 * rcx + 0x7fffffff], 0x0001 | 66 81 b4 08 ff ff ff 7f 01 00    |
    | xor word [rax + 1 * rcx - 0x7fffffff], 0x0001 | 66 81 b4 08 01 00 00 80 01 00    |
    | xor word [rax + 1 * rcx - 0x80000000], 0x0001 | 66 81 b4 08 00 00 00 80 01 00    |
    | xor word [r10 + 0x7f], 0x0001                 | 66 41 81 72 7f 01 00             |
    | xor word [r10 + 0x80], 0x0001                 | 66 41 81 b2 80 00 00 00 01 00    |
    | xor word [r10 - 0x80], 0x0001                 | 66 41 81 72 80 01 00             |
    | xor word [r10 - 0x81], 0x0001                 | 66 41 81 b2 7f ff ff ff 01 00    |
    | xor word [rax], 0x0000                        | 66 81 30 00 00                   |
    | xor word [rax], 0x007f                        | 66 81 30 7f 00                   |
    | xor word [rax], 0x0080                        | 66 81 30 80 00                   |
    | xor word [rax], 0x00ff                        | 66 81 30 ff 00                   |
    | xor word [rax], 0x0100                        | 66 81 30 00 01                   |
    | xor word [rax], 0x7fff                        | 66 81 30 ff 7f                   |
    | xor word [rax], 0x8000                        | 66 81 30 00 80                   |
    | xor word [rax], 0xffff                        | 66 81 30 ff ff                   |
    | xor word [rcx], 0x007f                        | 66 81 31 7f 00                   |
    | xor word [rdx], 0x0080                        | 66 81 32 80 00                   |
    | xor word [rbx], 0x00ff                        | 66 81 33 ff 00                   |
    | xor word [rsp], 0x0100                        | 66 81 34 24 00 01                |
    | xor word [rbp], 0x7fff                        | 66 81 75 00 ff 7f                |
    | xor word [rsi], 0x8000                        | 66 81 36 00 80                   |
    | xor word [rdi], 0xffff                        | 66 81 37 ff ff                   |
    | xor word [r8], 0x0000                         | 66 41 81 30 00 00                |
    | xor word [r10], 0x007f                        | 66 41 81 32 7f 00                |
    | xor word [r11], 0x0080                        | 66 41 81 33 80 00                |
    | xor word [r12], 0x00ff                        | 66 41 81 34 24 ff 00             |
    | xor word [r13], 0x0100                        | 66 41 81 75 00 00 01             |
    | xor word [r14], 0x7fff                        | 66 41 81 36 ff 7f                |
    | xor word [r15], 0x8000                        | 66 41 81 37 00 80                |
    | xor word [rax + 1 * rcx], 0xffff              | 66 81 34 08 ff ff                |
    | xor word [rcx + 1 * rcx], 0x0000              | 66 81 34 09 00 00                |
    | xor word [rbx + 1 * rcx], 0x007f              | 66 81 34 0b 7f 00                |
    | xor word [rsp + 1 * rcx], 0x0080              | 66 81 34 0c 80 00                |
    | xor word [rbp + 1 * rcx], 0x00ff              | 66 81 74 0d 00 ff 00             |
    | xor word [rsi + 1 * rcx], 0x0100              | 66 81 34 0e 00 01                |
    | xor word [rdi + 1 * rcx], 0x7fff              | 66 81 34 0f ff 7f                |
    | xor word [r8 + 1 * rcx], 0x8000               | 66 41 81 34 08 00 80             |
    | xor word [r9 + 1 * rcx], 0xffff               | 66 41 81 34 09 ff ff             |
    | xor word [r10 + 1 * rcx], 0x0000              | 66 41 81 34 0a 00 00             |
    | xor word [r12 + 1 * rcx], 0x007f              | 66 41 81 34 0c 7f 00             |
    | xor word [r13 + 1 * rcx], 0x0080              | 66 41 81 74 0d 00 80 00          |
    | xor word [r14 + 1 * rcx], 0x00ff              | 66 41 81 34 0e ff 00             |
    | xor word [r15 + 1 * rcx], 0x0100              | 66 41 81 34 0f 00 01             |
    | xor word [rax + 1 * rax], 0x7fff              | 66 81 34 00 ff 7f                |
    | xor word [rax + 1 * rdx], 0x8000              | 66 81 34 10 00 80                |
    | xor word [rax + 1 * rbx], 0xffff              | 66 81 34 18 ff ff                |
    | xor word [rax + 1 * rbp], 0x0000              | 66 81 34 28 00 00                |
    | xor word [rax + 1 * rdi], 0x007f              | 66 81 34 38 7f 00                |
    | xor word [rax + 1 * r8], 0x0080               | 66 42 81 34 00 80 00             |
    | xor word [rax + 1 * r9], 0x00ff               | 66 42 81 34 08 ff 00             |
    | xor word [rax + 1 * r10], 0x0100              | 66 42 81 34 10 00 01             |
    | xor word [rax + 1 * r11], 0x7fff              | 66 42 81 34 18 ff 7f             |
    | xor word [rax + 1 * r12], 0x8000              | 66 42 81 34 20 00 80             |
    | xor word [rax + 1 * r13], 0xffff              | 66 42 81 34 28 ff ff             |
    | xor word [rax + 1 * r14], 0x0000              | 66 42 81 34 30 00 00             |
    | xor word [rax + 2 * rcx], 0x007f              | 66 81 34 48 7f 00                |
    | xor word [rax + 4 * rcx], 0x0080              | 66 81 34 88 80 00                |
    | xor word [rax + 8 * rcx], 0x00ff              | 66 81 34 c8 ff 00                |
    | xor word [r8 + 1 * r9], 0x0100                | 66 43 81 34 08 00 01             |
    | xor word [r8 + 2 * r9], 0x7fff                | 66 43 81 34 48 ff 7f             |
    | xor word [r8 + 4 * r9], 0x8000                | 66 43 81 34 88 00 80             |
    | xor word [r8 + 8 * r9], 0xffff                | 66 43 81 34 c8 ff ff             |
    | xor word [1 * rcx], 0x0000                    | 66 81 34 0d 00 00 00 00 00 00    |
    | xor word [4 * rcx], 0x007f                    | 66 81 34 8d 00 00 00 00 7f 00    |
    | xor word [8 * rcx], 0x0080                    | 66 81 34 cd 00 00 00 00 80 00    |
    | xor word [1 * r9], 0x00ff                     | 66 42 81 34 0d 00 00 00 00 ff 00 |
    | xor word [2 * r9], 0x0100                     | 66 42 81 34 4d 00 00 00 00 00 01 |
    | xor word [4 * r9], 0x7fff                     | 66 42 81 34 8d 00 00 00 00 ff 7f |
    | xor word [8 * r9], 0x8000                     | 66 42 81 34 cd 00 00 00 00 00 80 |
    | xor word [r13 + 8 * r12], 0xffff              | 66 43 81 74 e5 00 ff ff          |
    | xor word [rsp + 4 * r15], 0x0000              | 66 42 81 34 bc 00 00             |
    | xor word [rax + 1 * rcx - 0x00], 0x007f       | 66 81 74 08 00 7f 00             |
    | xor word [rax + 1 * rcx + 0x01], 0x0080       | 66 81 74 08 01 80 00             |
    | xor word [rax + 1 * rcx - 0x01], 0x00ff       | 66 81 74 08 ff ff 00             |
    | xor word [rax + 1 * rcx + 0x00000001], 0x0100 | 66 81 b4 08 01 00 00 00 00 01    |
    | xor word [rax + 1 * rcx - 0x00000001], 0x7fff | 66 81 b4 08 ff ff ff ff ff 7f    |
    | xor word [rax + 1 * rcx + 0x7f], 0x8000       | 66 81 74 08 7f 00 80             |
    | xor word [rax + 1 * rcx - 0x7f], 0xffff       | 66 81 74 08 81 ff ff             |
    | xor word [rax + 1 * rcx + 0x80], 0x0000       | 66 81 b4 08 80 00 00 00 00 00    |
    | xor word [rax + 1 * rcx - 0x81], 0x007f       | 66 81 b4 08 7f ff ff ff 7f 00    |
    | xor word [rax + 1 * rcx + 0xff], 0x0080       | 66 81 b4 08 ff 00 00 00 80 00    |
    | xor word [rax + 1 * rcx - 0xff], 0x00ff       | 66 81 b4 08 01 ff ff ff ff 00    |
    | xor word [rax + 1 * rcx + 0x7fffffff], 0x0100 | 66 81 b4 08 ff ff ff 7f 00 01    |
    | xor word [rax + 1 * rcx - 0x7fffffff], 0x7fff | 66 81 b4 08 01 00 00 80 ff 7f    |
    | xor word [rax + 1 * rcx - 0x80000000], 0x8000 | 66 81 b4 08 00 00 00 80 00 80    |
    | xor word [r10 + 0x7f], 0xffff                 | 66 41 81 72 7f ff ff             |
    | xor word [r10 + 0x80], 0x0000                 | 66 41 81 b2 80 00 00 00 00 00    |
    | xor word [r10 - 0x81], 0x007f                 | 66 41 81 b2 7f ff ff ff 7f 00    |
    | --------------------------------------------- | -------------------------------- |
"""


def can_encode_xor_addr16_imm16():
    encode(XOR_ADDR16_IMM16)


XOR_ADDR16_REG16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | xor word [rax], cx                          | 66 31 08                   |
    | xor word [rcx], cx                          | 66 31 09                   |
    | xor word [rdx], cx                          | 66 31 0a                   |
    | xor word [rbx], cx                          | 66 31 0b                   |
    | xor word [rsp], cx                          | 66 31 0c 24                |
    | xor word [rbp], cx                          | 66 31 4d 00                |
    | xor word [rsi], cx                          | 66 31 0e                   |
    | xor word [rdi], cx                          | 66 31 0f                   |
    | xor word [r8], cx                           | 66 41 31 08                |
    | xor word [r9], cx                           | 66 41 31 09                |
    | xor word [r10], cx                          | 66 41 31 0a                |
    | xor word [r11], cx                          | 66 41 31 0b                |
    | xor word [r12], cx                          | 66 41 31 0c 24             |
    | xor word [r13], cx                          | 66 41 31 4d 00             |
    | xor word [r14], cx                          | 66 41 31 0e                |
    | xor word [r15], cx                          | 66 41 31 0f                |
    | xor word [rax + 1 * rcx], cx                | 66 31 0c 08                |
    | xor word [rcx + 1 * rcx], cx                | 66 31 0c 09                |
    | xor word [rdx + 1 * rcx], cx                | 66 31 0c 0a                |
    | xor word [rbx + 1 * rcx], cx                | 66 31 0c 0b                |
    | xor word [rsp + 1 * rcx], cx                | 66 31 0c 0c                |
    | xor word [rbp + 1 * rcx], cx                | 66 31 4c 0d 00             |
    | xor word [rsi + 1 * rcx], cx                | 66 31 0c 0e                |
    | xor word [rdi + 1 * rcx], cx                | 66 31 0c 0f                |
    | xor word [r8 + 1 * rcx], cx                 | 66 41 31 0c 08             |
    | xor word [r9 + 1 * rcx], cx                 | 66 41 31 0c 09             |
    | xor word [r10 + 1 * rcx], cx                | 66 41 31 0c 0a             |
    | xor word [r11 + 1 * rcx], cx                | 66 41 31 0c 0b             |
    | xor word [r12 + 1 * rcx], cx                | 66 41 31 0c 0c             |
    | xor word [r13 + 1 * rcx], cx                | 66 41 31 4c 0d 00          |
    | xor word [r14 + 1 * rcx], cx                | 66 41 31 0c 0e             |
    | xor word [r15 + 1 * rcx], cx                | 66 41 31 0c 0f             |
    | xor word [rax + 1 * rax], cx                | 66 31 0c 00                |
    | xor word [rax + 1 * rdx], cx                | 66 31 0c 10                |
    | xor word [rax + 1 * rbx], cx                | 66 31 0c 18                |
    | xor word [rax + 1 * rbp], cx                | 66 31 0c 28                |
    | xor word [rax + 1 * rsi], cx                | 66 31 0c 30                |
    | xor word [rax + 1 * rdi], cx                | 66 31 0c 38                |
    | xor word [rax + 1 * r8], cx                 | 66 42 31 0c 00             |
    | xor word [rax + 1 * r9], cx                 | 66 42 31 0c 08             |
    | xor word [rax + 1 * r10], cx                | 66 42 31 0c 10             |
    | xor word [rax + 1 * r11], cx                | 66 42 31 0c 18             |
    | xor word [rax + 1 * r12], cx                | 66 42 31 0c 20             |
    | xor word [rax + 1 * r13], cx                | 66 42 31 0c 28             |
    | xor word [rax + 1 * r14], cx                | 66 42 31 0c 30             |
    | xor word [rax + 1 * r15], cx                | 66 42 31 0c 38             |
    | xor word [rax + 2 * rcx], cx                | 66 31 0c 48                |
    | xor word [rax + 4 * rcx], cx                | 66 31 0c 88                |
    | xor word [rax + 8 * rcx], cx                | 66 31 0c c8                |
    | xor word [r8 + 1 * r9], cx                  | 66 43 31 0c 08             |
    | xor word [r8 + 2 * r9], cx                  | 66 43 31 0c 48             |
    | xor word [r8 + 4 * r9], cx                  | 66 43 31 0c 88             |
    | xor word [r8 + 8 * r9], cx                  | 66 43 31 0c c8             |
    | xor word [1 * rcx], cx                      | 66 31 0c 0d 00 00 00 00    |
    | xor word [2 * rcx], cx                      | 66 31 0c 4d 00 00 00 00    |
    | xor word [4 * rcx], cx                      | 66 31 0c 8d 00 00 00 00    |
    | xor word [8 * rcx], cx                      | 66 31 0c cd 00 00 00 00    |
    | xor word [1 * r9], cx                       | 66 42 31 0c 0d 00 00 00 00 |
    | xor word [2 * r9], cx                       | 66 42 31 0c 4d 00 00 00 00 |
    | xor word [4 * r9], cx                       | 66 42 31 0c 8d 00 00 00 00 |
    | xor word [8 * r9], cx                       | 66 42 31 0c cd 00 00 00 00 |
    | xor word [r13 + 8 * r12], cx                | 66 43 31 4c e5 00          |
    | xor word [rsp + 4 * r15], cx                | 66 42 31 0c bc             |
    | xor word [rax + 1 * rcx + 0x00], cx         | 66 31 4c 08 00             |
    | xor word [rax + 1 * rcx - 0x00], cx         | 66 31 4c 08 00             |
    | xor word [rax + 1 * rcx + 0x01], cx         | 66 31 4c 08 01             |
    | xor word [rax + 1 * rcx - 0x01], cx         | 66 31 4c 08 ff             |
    | xor word [rax + 1 * rcx + 0x00000001], cx   | 66 31 8c 08 01 00 00 00    |
    | xor word [rax + 1 * rcx - 0x00000001], cx   | 66 31 8c 08 ff ff ff ff    |
    | xor word [rax + 1 * rcx + 0x7f], cx         | 66 31 4c 08 7f             |
    | xor word [rax + 1 * rcx - 0x7f], cx         | 66 31 4c 08 81             |
    | xor word [rax + 1 * rcx + 0x80], cx         | 66 31 8c 08 80 00 00 00    |
    | xor word [rax + 1 * rcx - 0x80], cx         | 66 31 4c 08 80             |
    | xor word [rax + 1 * rcx - 0x81], cx         | 66 31 8c 08 7f ff ff ff    |
    | xor word [rax + 1 * rcx + 0xff], cx         | 66 31 8c 08 ff 00 00 00    |
    | xor word [rax + 1 * rcx - 0xff], cx         | 66 31 8c 08 01 ff ff ff    |
    | xor word [rax + 1 * rcx + 0x7fffffff], cx   | 66 31 8c 08 ff ff ff 7f    |
    | xor word [rax + 1 * rcx - 0x7fffffff], cx   | 66 31 8c 08 01 00 00 80    |
    | xor word [rax + 1 * rcx - 0x80000000], cx   | 66 31 8c 08 00 00 00 80    |
    | xor word [r10 + 0x7f], cx                   | 66 41 31 4a 7f             |
    | xor word [r10 + 0x80], cx                   | 66 41 31 8a 80 00 00 00    |
    | xor word [r10 - 0x80], cx                   | 66 41 31 4a 80             |
    | xor word [r10 - 0x81], cx                   | 66 41 31 8a 7f ff ff ff    |
    | xor word [rax], ax                          | 66 31 00                   |
    | xor word [rax], dx                          | 66 31 10                   |
    | xor word [rax], bx                          | 66 31 18                   |
    | xor word [rax], sp                          | 66 31 20                   |
    | xor word [rax], bp                          | 66 31 28                   |
    | xor word [rax], si                          | 66 31 30                   |
    | xor word [rax], di                          | 66 31 38                   |
    | xor word [rax], r8w                         | 66 44 31 00                |
    | xor word [rax], r9w                         | 66 44 31 08                |
    | xor word [rax], r10w                        | 66 44 31 10                |
    | xor word [rax], r11w                        | 66 44 31 18                |
    | xor word [rax], r12w                        | 66 44 31 20                |
    | xor word [rax], r13w                        | 66 44 31 28                |
    | xor word [rax], r14w                        | 66 44 31 30                |
    | xor word [rax], r15w                        | 66 44 31 38                |
    | xor word [rcx], dx                          | 66 31 11                   |
    | xor word [rdx], bx                          | 66 31 1a                   |
    | xor word [rbx], sp                          | 66 31 23                   |
    | xor word [rsp], bp                          | 66 31 2c 24                |
    | xor word [rbp], si                          | 66 31 75 00                |
    | xor word [rsi], di                          | 66 31 3e                   |
    | xor word [rdi], r8w                         | 66 44 31 07                |
    | xor word [r8], r9w                          | 66 45 31 08                |
    | xor word [r9], r10w                         | 66 45 31 11                |
    | xor word [r10], r11w                        | 66 45 31 1a                |
    | xor word [r11], r12w                        | 66 45 31 23                |
    | xor word [r12], r13w                        | 66 45 31 2c 24             |
    | xor word [r13], r14w                        | 66 45 31 75 00             |
    | xor word [r14], r15w                        | 66 45 31 3e                |
    | xor word [r15], ax                          | 66 41 31 07                |
    | xor word [rcx + 1 * rcx], dx                | 66 31 14 09                |
    | xor word [rdx + 1 * rcx], bx                | 66 31 1c 0a                |
    | xor word [rbx + 1 * rcx], sp                | 66 31 24 0b                |
    | xor word [rsp + 1 * rcx], bp                | 66 31 2c 0c                |
    | xor word [rbp + 1 * rcx], si                | 66 31 74 0d 00             |
    | xor word [rsi + 1 * rcx], di                | 66 31 3c 0e                |
    | xor word [rdi + 1 * rcx], r8w               | 66 44 31 04 0f             |
    | xor word [r8 + 1 * rcx], r9w                | 66 45 31 0c 08             |
    | xor word [r9 + 1 * rcx], r10w               | 66 45 31 14 09             |
    | xor word [r10 + 1 * rcx], r11w              | 66 45 31 1c 0a             |
    | xor word [r11 + 1 * rcx], r12w              | 66 45 31 24 0b             |
    | xor word [r12 + 1 * rcx], r13w              | 66 45 31 2c 0c             |
    | xor word [r13 + 1 * rcx], r14w              | 66 45 31 74 0d 00          |
    | xor word [r14 + 1 * rcx], r15w              | 66 45 31 3c 0e             |
    | xor word [r15 + 1 * rcx], ax                | 66 41 31 04 0f             |
    | xor word [rax + 1 * rdx], dx                | 66 31 14 10                |
    | xor word [rax + 1 * rbx], bx                | 66 31 1c 18                |
    | xor word [rax + 1 * rbp], sp                | 66 31 24 28                |
    | xor word [rax + 1 * rsi], bp                | 66 31 2c 30                |
    | xor word [rax + 1 * rdi], si                | 66 31 34 38                |
    | xor word [rax + 1 * r8], di                 | 66 42 31 3c 00             |
    | xor word [rax + 1 * r9], r8w                | 66 46 31 04 08             |
    | xor word [rax + 1 * r10], r9w               | 66 46 31 0c 10             |
    | xor word [rax + 1 * r11], r10w              | 66 46 31 14 18             |
    | xor word [rax + 1 * r12], r11w              | 66 46 31 1c 20             |
    | xor word [rax + 1 * r13], r12w              | 66 46 31 24 28             |
    | xor word [rax + 1 * r14], r13w              | 66 46 31 2c 30             |
    | xor word [rax + 1 * r15], r14w              | 66 46 31 34 38             |
    | xor word [rax + 2 * rcx], r15w              | 66 44 31 3c 48             |
    | xor word [rax + 4 * rcx], ax                | 66 31 04 88                |
    | xor word [r8 + 1 * r9], dx                  | 66 43 31 14 08             |
    | xor word [r8 + 2 * r9], bx                  | 66 43 31 1c 48             |
    | xor word [r8 + 4 * r9], sp                  | 66 43 31 24 88             |
    | xor word [r8 + 8 * r9], bp                  | 66 43 31 2c c8             |
    | xor word [1 * rcx], si                      | 66 31 34 0d 00 00 00 00    |
    | xor word [2 * rcx], di                      | 66 31 3c 4d 00 00 00 00    |
    | xor word [4 * rcx], r8w                     | 66 44 31 04 8d 00 00 00 00 |
    | xor word [8 * rcx], r9w                     | 66 44 31 0c cd 00 00 00 00 |
    | xor word [1 * r9], r10w                     | 66 46 31 14 0d 00 00 00 00 |
    | xor word [2 * r9], r11w                     | 66 46 31 1c 4d 00 00 00 00 |
    | xor word [4 * r9], r12w                     | 66 46 31 24 8d 00 00 00 00 |
    | xor word [8 * r9], r13w                     | 66 46 31 2c cd 00 00 00 00 |
    | xor word [r13 + 8 * r12], r14w              | 66 47 31 74 e5 00          |
    | xor word [rsp + 4 * r15], r15w              | 66 46 31 3c bc             |
    | xor word [rax + 1 * rcx + 0x00], ax         | 66 31 44 08 00             |
    | xor word [rax + 1 * rcx + 0x01], dx         | 66 31 54 08 01             |
    | xor word [rax + 1 * rcx - 0x01], bx         | 66 31 5c 08 ff             |
    | xor word [rax + 1 * rcx + 0x00000001], sp   | 66 31 a4 08 01 00 00 00    |
    | xor word [rax + 1 * rcx - 0x00000001], bp   | 66 31 ac 08 ff ff ff ff    |
    | xor word [rax + 1 * rcx + 0x7f], si         | 66 31 74 08 7f             |
    | xor word [rax + 1 * rcx - 0x7f], di         | 66 31 7c 08 81             |
    | xor word [rax + 1 * rcx + 0x80], r8w        | 66 44 31 84 08 80 00 00 00 |
    | xor word [rax + 1 * rcx - 0x80], r9w        | 66 44 31 4c 08 80          |
    | xor word [rax + 1 * rcx - 0x81], r10w       | 66 44 31 94 08 7f ff ff ff |
    | xor word [rax + 1 * rcx + 0xff], r11w       | 66 44 31 9c 08 ff 00 00 00 |
    | xor word [rax + 1 * rcx - 0xff], r12w       | 66 44 31 a4 08 01 ff ff ff |
    | xor word [rax + 1 * rcx + 0x7fffffff], r13w | 66 44 31 ac 08 ff ff ff 7f |
    | xor word [rax + 1 * rcx - 0x7fffffff], r14w | 66 44 31 b4 08 01 00 00 80 |
    | xor word [rax + 1 * rcx - 0x80000000], r15w | 66 44 31 bc 08 00 00 00 80 |
    | xor word [r10 + 0x7f], ax                   | 66 41 31 42 7f             |
    | xor word [r10 - 0x80], dx                   | 66 41 31 52 80             |
    | xor word [r10 - 0x81], bx                   | 66 41 31 9a 7f ff ff ff    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_xor_addr16_reg16():
    encode(XOR_ADDR16_REG16)


XOR_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | xor byte [rax], 0x01                        | 80 30 01                   |
    | xor byte [rcx], 0x01                        | 80 31 01                   |
    | xor byte [rdx], 0x01                        | 80 32 01                   |
    | xor byte [rbx], 0x01                        | 80 33 01                   |
    | xor byte [rsp], 0x01                        | 80 34 24 01                |
    | xor byte [rbp], 0x01                        | 80 75 00 01                |
    | xor byte [rsi], 0x01                        | 80 36 01                   |
    | xor byte [rdi], 0x01                        | 80 37 01                   |
    | xor byte [r8], 0x01                         | 41 80 30 01                |
    | xor byte [r9], 0x01                         | 41 80 31 01                |
    | xor byte [r10], 0x01                        | 41 80 32 01                |
    | xor byte [r11], 0x01                        | 41 80 33 01                |
    | xor byte [r12], 0x01                        | 41 80 34 24 01             |
    | xor byte [r13], 0x01                        | 41 80 75 00 01             |
    | xor byte [r14], 0x01                        | 41 80 36 01                |
    | xor byte [r15], 0x01                        | 41 80 37 01                |
    | xor byte [rax + 1 * rcx], 0x01              | 80 34 08 01                |
    | xor byte [rcx + 1 * rcx], 0x01              | 80 34 09 01                |
    | xor byte [rdx + 1 * rcx], 0x01              | 80 34 0a 01                |
    | xor byte [rbx + 1 * rcx], 0x01              | 80 34 0b 01                |
    | xor byte [rsp + 1 * rcx], 0x01              | 80 34 0c 01                |
    | xor byte [rbp + 1 * rcx], 0x01              | 80 74 0d 00 01             |
    | xor byte [rsi + 1 * rcx], 0x01              | 80 34 0e 01                |
    | xor byte [rdi + 1 * rcx], 0x01              | 80 34 0f 01                |
    | xor byte [r8 + 1 * rcx], 0x01               | 41 80 34 08 01             |
    | xor byte [r9 + 1 * rcx], 0x01               | 41 80 34 09 01             |
    | xor byte [r10 + 1 * rcx], 0x01              | 41 80 34 0a 01             |
    | xor byte [r11 + 1 * rcx], 0x01              | 41 80 34 0b 01             |
    | xor byte [r12 + 1 * rcx], 0x01              | 41 80 34 0c 01             |
    | xor byte [r13 + 1 * rcx], 0x01              | 41 80 74 0d 00 01          |
    | xor byte [r14 + 1 * rcx], 0x01              | 41 80 34 0e 01             |
    | xor byte [r15 + 1 * rcx], 0x01              | 41 80 34 0f 01             |
    | xor byte [rax + 1 * rax], 0x01              | 80 34 00 01                |
    | xor byte [rax + 1 * rdx], 0x01              | 80 34 10 01                |
    | xor byte [rax + 1 * rbx], 0x01              | 80 34 18 01                |
    | xor byte [rax + 1 * rbp], 0x01              | 80 34 28 01                |
    | xor byte [rax + 1 * rsi], 0x01              | 80 34 30 01                |
    | xor byte [rax + 1 * rdi], 0x01              | 80 34 38 01                |
    | xor byte [rax + 1 * r8], 0x01               | 42 80 34 00 01             |
    | xor byte [rax + 1 * r9], 0x01               | 42 80 34 08 01             |
    | xor byte [rax + 1 * r10], 0x01              | 42 80 34 10 01             |
    | xor byte [rax + 1 * r11], 0x01              | 42 80 34 18 01             |
    | xor byte [rax + 1 * r12], 0x01              | 42 80 34 20 01             |
    | xor byte [rax + 1 * r13], 0x01              | 42 80 34 28 01             |
    | xor byte [rax + 1 * r14], 0x01              | 42 80 34 30 01             |
    | xor byte [rax + 1 * r15], 0x01              | 42 80 34 38 01             |
    | xor byte [rax + 2 * rcx], 0x01              | 80 34 48 01                |
    | xor byte [rax + 4 * rcx], 0x01              | 80 34 88 01                |
    | xor byte [rax + 8 * rcx], 0x01              | 80 34 c8 01                |
    | xor byte [r8 + 1 * r9], 0x01                | 43 80 34 08 01             |
    | xor byte [r8 + 2 * r9], 0x01                | 43 80 34 48 01             |
    | xor byte [r8 + 4 * r9], 0x01                | 43 80 34 88 01             |
    | xor byte [r8 + 8 * r9], 0x01                | 43 80 34 c8 01             |
    | xor byte [1 * rcx], 0x01                    | 80 34 0d 00 00 00 00 01    |
    | xor byte [2 * rcx], 0x01                    | 80 34 4d 00 00 00 00 01    |
    | xor byte [4 * rcx], 0x01                    | 80 34 8d 00 00 00 00 01    |
    | xor byte [8 * rcx], 0x01                    | 80 34 cd 00 00 00 00 01    |
    | xor byte [1 * r9], 0x01                     | 42 80 34 0d 00 00 00 00 01 |
    | xor byte [2 * r9], 0x01                     | 42 80 34 4d 00 00 00 00 01 |
    | xor byte [4 * r9], 0x01                     | 42 80 34 8d 00 00 00 00 01 |
    | xor byte [8 * r9], 0x01                     | 42 80 34 cd 00 00 00 00 01 |
    | xor byte [r13 + 8 * r12], 0x01              | 43 80 74 e5 00 01          |
    | xor byte [rsp + 4 * r15], 0x01              | 42 80 34 bc 01             |
    | xor byte [rax + 1 * rcx + 0x00], 0x01       | 80 74 08 00 01             |
    | xor byte [rax + 1 * rcx - 0x00], 0x01       | 80 74 08 00 01             |
    | xor byte [rax + 1 * rcx + 0x01], 0x01       | 80 74 08 01 01             |
    | xor byte [rax + 1 * rcx - 0x01], 0x01       | 80 74 08 ff 01             |
    | xor byte [rax + 1 * rcx + 0x00000001], 0x01 | 80 b4 08 01 00 00 00 01    |
    | xor byte [rax + 1 * rcx - 0x00000001], 0x01 | 80 b4 08 ff ff ff ff 01    |
    | xor byte [rax + 1 * rcx + 0x7f], 0x01       | 80 74 08 7f 01             |
    | xor byte [rax + 1 * rcx - 0x7f], 0x01       | 80 74 08 81 01             |
    | xor byte [rax + 1 * rcx + 0x80], 0x01       | 80 b4 08 80 00 00 00 01    |
    | xor byte [rax + 1 * rcx - 0x80], 0x01       | 80 74 08 80 01             |
    | xor byte [rax + 1 * rcx - 0x81], 0x01       | 80 b4 08 7f ff ff ff 01    |
    | xor byte [rax + 1 * rcx + 0xff], 0x01       | 80 b4 08 ff 00 00 00 01    |
    | xor byte [rax + 1 * rcx - 0xff], 0x01       | 80 b4 08 01 ff ff ff 01    |
    | xor byte [rax + 1 * rcx + 0x7fffffff], 0x01 | 80 b4 08 ff ff ff 7f 01    |
    | xor byte [rax + 1 * rcx - 0x7fffffff], 0x01 | 80 b4 08 01 00 00 80 01    |
    | xor byte [rax + 1 * rcx - 0x80000000], 0x01 | 80 b4 08 00 00 00 80 01    |
    | xor byte [r10 + 0x7f], 0x01                 | 41 80 72 7f 01             |
    | xor byte [r10 + 0x80], 0x01                 | 41 80 b2 80 00 00 00 01    |
    | xor byte [r10 - 0x80], 0x01                 | 41 80 72 80 01             |
    | xor byte [r10 - 0x81], 0x01                 | 41 80 b2 7f ff ff ff 01    |
    | xor byte [rax], 0x00                        | 80 30 00                   |
    | xor byte [rax], 0x7f                        | 80 30 7f                   |
    | xor byte [rax], 0x80                        | 80 30 80                   |
    | xor byte [rax], 0xff                        | 80 30 ff                   |
    | xor byte [rcx], 0x7f                        | 80 31 7f                   |
    | xor byte [rdx], 0x80                        | 80 32 80                   |
    | xor byte [rbx], 0xff                        | 80 33 ff                   |
    | xor byte [rsp], 0x00                        | 80 34 24 00                |
    | xor byte [rsi], 0x7f                        | 80 36 7f                   |
    | xor byte [rdi], 0x80                        | 80 37 80                   |
    | xor byte [r8], 0xff                         | 41 80 30 ff                |
    | xor byte [r9], 0x00                         | 41 80 31 00                |
    | xor byte [r11], 0x7f                        | 41 80 33 7f                |
    | xor byte [r12], 0x80                        | 41 80 34 24 80             |
    | xor byte [r13], 0xff                        | 41 80 75 00 ff             |
    | xor byte [r14], 0x00                        | 41 80 36 00                |
    | xor byte [rax + 1 * rcx], 0x7f              | 80 34 08 7f                |
    | xor byte [rcx + 1 * rcx], 0x80              | 80 34 09 80                |
    | xor byte [rdx + 1 * rcx], 0xff              | 80 34 0a ff                |
    | xor byte [rbx + 1 * rcx], 0x00              | 80 34 0b 00                |
    | xor byte [rbp + 1 * rcx], 0x7f              | 80 74 0d 00 7f             |
    | xor byte [rsi + 1 * rcx], 0x80              | 80 34 0e 80                |
    | xor byte [rdi + 1 * rcx], 0xff              | 80 34 0f ff                |
    | xor byte [r8 + 1 * rcx], 0x00               | 41 80 34 08 00             |
    | xor byte [r10 + 1 * rcx], 0x7f              | 41 80 34 0a 7f             |
    | xor byte [r11 + 1 * rcx], 0x80              | 41 80 34 0b 80             |
    | xor byte [r12 + 1 * rcx], 0xff              | 41 80 34 0c ff             |
    | xor byte [r13 + 1 * rcx], 0x00              | 41 80 74 0d 00 00          |
    | xor byte [r15 + 1 * rcx], 0x7f              | 41 80 34 0f 7f             |
    | xor byte [rax + 1 * rax], 0x80              | 80 34 00 80                |
    | xor byte [rax + 1 * rdx], 0xff              | 80 34 10 ff                |
    | xor byte [rax + 1 * rbx], 0x00              | 80 34 18 00                |
    | xor byte [rax + 1 * rsi], 0x7f              | 80 34 30 7f                |
    | xor byte [rax + 1 * rdi], 0x80              | 80 34 38 80                |
    | xor byte [rax + 1 * r8], 0xff               | 42 80 34 00 ff             |
    | xor byte [rax + 1 * r9], 0x00               | 42 80 34 08 00             |
    | xor byte [rax + 1 * r11], 0x7f              | 42 80 34 18 7f             |
    | xor byte [rax + 1 * r12], 0x80              | 42 80 34 20 80             |
    | xor byte [rax + 1 * r13], 0xff              | 42 80 34 28 ff             |
    | xor byte [rax + 1 * r14], 0x00              | 42 80 34 30 00             |
    | xor byte [rax + 2 * rcx], 0x7f              | 80 34 48 7f                |
    | xor byte [rax + 4 * rcx], 0x80              | 80 34 88 80                |
    | xor byte [rax + 8 * rcx], 0xff              | 80 34 c8 ff                |
    | xor byte [r8 + 1 * r9], 0x00                | 43 80 34 08 00             |
    | xor byte [r8 + 4 * r9], 0x7f                | 43 80 34 88 7f             |
    | xor byte [r8 + 8 * r9], 0x80                | 43 80 34 c8 80             |
    | xor byte [1 * rcx], 0xff                    | 80 34 0d 00 00 00 00 ff    |
    | xor byte [2 * rcx], 0x00                    | 80 34 4d 00 00 00 00 00    |
    | xor byte [8 * rcx], 0x7f                    | 80 34 cd 00 00 00 00 7f    |
    | xor byte [1 * r9], 0x80                     | 42 80 34 0d 00 00 00 00 80 |
    | xor byte [2 * r9], 0xff                     | 42 80 34 4d 00 00 00 00 ff |
    | xor byte [4 * r9], 0x00                     | 42 80 34 8d 00 00 00 00 00 |
    | xor byte [r13 + 8 * r12], 0x7f              | 43 80 74 e5 00 7f          |
    | xor byte [rsp + 4 * r15], 0x80              | 42 80 34 bc 80             |
    | xor byte [rax + 1 * rcx + 0x00], 0xff       | 80 74 08 00 ff             |
    | xor byte [rax + 1 * rcx - 0x00], 0x00       | 80 74 08 00 00             |
    | xor byte [rax + 1 * rcx - 0x01], 0x7f       | 80 74 08 ff 7f             |
    | xor byte [rax + 1 * rcx + 0x00000001], 0x80 | 80 b4 08 01 00 00 00 80    |
    | xor byte [rax + 1 * rcx - 0x00000001], 0xff | 80 b4 08 ff ff ff ff ff    |
    | xor byte [rax + 1 * rcx + 0x7f], 0x00       | 80 74 08 7f 00             |
    | xor byte [rax + 1 * rcx + 0x80], 0x7f       | 80 b4 08 80 00 00 00 7f    |
    | xor byte [rax + 1 * rcx - 0x80], 0x80       | 80 74 08 80 80             |
    | xor byte [rax + 1 * rcx - 0x81], 0xff       | 80 b4 08 7f ff ff ff ff    |
    | xor byte [rax + 1 * rcx + 0xff], 0x00       | 80 b4 08 ff 00 00 00 00    |
    | xor byte [rax + 1 * rcx + 0x7fffffff], 0x7f | 80 b4 08 ff ff ff 7f 7f    |
    | xor byte [rax + 1 * rcx - 0x7fffffff], 0x80 | 80 b4 08 01 00 00 80 80    |
    | xor byte [rax + 1 * rcx - 0x80000000], 0xff | 80 b4 08 00 00 00 80 ff    |
    | xor byte [r10 + 0x7f], 0x00                 | 41 80 72 7f 00             |
    | xor byte [r10 - 0x80], 0x7f                 | 41 80 72 80 7f             |
    | xor byte [r10 - 0x81], 0x80                 | 41 80 b2 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_xor_addr8_imm8():
    encode(XOR_ADDR8_IMM8)


XOR_ADDR8_REG8 = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | xor byte [rax], cl                         | 30 08                   |
    | xor byte [rcx], cl                         | 30 09                   |
    | xor byte [rdx], cl                         | 30 0a                   |
    | xor byte [rbx], cl                         | 30 0b                   |
    | xor byte [rsp], cl                         | 30 0c 24                |
    | xor byte [rbp], cl                         | 30 4d 00                |
    | xor byte [rsi], cl                         | 30 0e                   |
    | xor byte [rdi], cl                         | 30 0f                   |
    | xor byte [r8], cl                          | 41 30 08                |
    | xor byte [r9], cl                          | 41 30 09                |
    | xor byte [r10], cl                         | 41 30 0a                |
    | xor byte [r11], cl                         | 41 30 0b                |
    | xor byte [r12], cl                         | 41 30 0c 24             |
    | xor byte [r13], cl                         | 41 30 4d 00             |
    | xor byte [r14], cl                         | 41 30 0e                |
    | xor byte [r15], cl                         | 41 30 0f                |
    | xor byte [rax + 1 * rcx], cl               | 30 0c 08                |
    | xor byte [rcx + 1 * rcx], cl               | 30 0c 09                |
    | xor byte [rdx + 1 * rcx], cl               | 30 0c 0a                |
    | xor byte [rbx + 1 * rcx], cl               | 30 0c 0b                |
    | xor byte [rsp + 1 * rcx], cl               | 30 0c 0c                |
    | xor byte [rbp + 1 * rcx], cl               | 30 4c 0d 00             |
    | xor byte [rsi + 1 * rcx], cl               | 30 0c 0e                |
    | xor byte [rdi + 1 * rcx], cl               | 30 0c 0f                |
    | xor byte [r8 + 1 * rcx], cl                | 41 30 0c 08             |
    | xor byte [r9 + 1 * rcx], cl                | 41 30 0c 09             |
    | xor byte [r10 + 1 * rcx], cl               | 41 30 0c 0a             |
    | xor byte [r11 + 1 * rcx], cl               | 41 30 0c 0b             |
    | xor byte [r12 + 1 * rcx], cl               | 41 30 0c 0c             |
    | xor byte [r13 + 1 * rcx], cl               | 41 30 4c 0d 00          |
    | xor byte [r14 + 1 * rcx], cl               | 41 30 0c 0e             |
    | xor byte [r15 + 1 * rcx], cl               | 41 30 0c 0f             |
    | xor byte [rax + 1 * rax], cl               | 30 0c 00                |
    | xor byte [rax + 1 * rdx], cl               | 30 0c 10                |
    | xor byte [rax + 1 * rbx], cl               | 30 0c 18                |
    | xor byte [rax + 1 * rbp], cl               | 30 0c 28                |
    | xor byte [rax + 1 * rsi], cl               | 30 0c 30                |
    | xor byte [rax + 1 * rdi], cl               | 30 0c 38                |
    | xor byte [rax + 1 * r8], cl                | 42 30 0c 00             |
    | xor byte [rax + 1 * r9], cl                | 42 30 0c 08             |
    | xor byte [rax + 1 * r10], cl               | 42 30 0c 10             |
    | xor byte [rax + 1 * r11], cl               | 42 30 0c 18             |
    | xor byte [rax + 1 * r12], cl               | 42 30 0c 20             |
    | xor byte [rax + 1 * r13], cl               | 42 30 0c 28             |
    | xor byte [rax + 1 * r14], cl               | 42 30 0c 30             |
    | xor byte [rax + 1 * r15], cl               | 42 30 0c 38             |
    | xor byte [rax + 2 * rcx], cl               | 30 0c 48                |
    | xor byte [rax + 4 * rcx], cl               | 30 0c 88                |
    | xor byte [rax + 8 * rcx], cl               | 30 0c c8                |
    | xor byte [r8 + 1 * r9], cl                 | 43 30 0c 08             |
    | xor byte [r8 + 2 * r9], cl                 | 43 30 0c 48             |
    | xor byte [r8 + 4 * r9], cl                 | 43 30 0c 88             |
    | xor byte [r8 + 8 * r9], cl                 | 43 30 0c c8             |
    | xor byte [1 * rcx], cl                     | 30 0c 0d 00 00 00 00    |
    | xor byte [2 * rcx], cl                     | 30 0c 4d 00 00 00 00    |
    | xor byte [4 * rcx], cl                     | 30 0c 8d 00 00 00 00    |
    | xor byte [8 * rcx], cl                     | 30 0c cd 00 00 00 00    |
    | xor byte [1 * r9], cl                      | 42 30 0c 0d 00 00 00 00 |
    | xor byte [2 * r9], cl                      | 42 30 0c 4d 00 00 00 00 |
    | xor byte [4 * r9], cl                      | 42 30 0c 8d 00 00 00 00 |
    | xor byte [8 * r9], cl                      | 42 30 0c cd 00 00 00 00 |
    | xor byte [r13 + 8 * r12], cl               | 43 30 4c e5 00          |
    | xor byte [rsp + 4 * r15], cl               | 42 30 0c bc             |
    | xor byte [rax + 1 * rcx + 0x00], cl        | 30 4c 08 00             |
    | xor byte [rax + 1 * rcx - 0x00], cl        | 30 4c 08 00             |
    | xor byte [rax + 1 * rcx + 0x01], cl        | 30 4c 08 01             |
    | xor byte [rax + 1 * rcx - 0x01], cl        | 30 4c 08 ff             |
    | xor byte [rax + 1 * rcx + 0x00000001], cl  | 30 8c 08 01 00 00 00    |
    | xor byte [rax + 1 * rcx - 0x00000001], cl  | 30 8c 08 ff ff ff ff    |
    | xor byte [rax + 1 * rcx + 0x7f], cl        | 30 4c 08 7f             |
    | xor byte [rax + 1 * rcx - 0x7f], cl        | 30 4c 08 81             |
    | xor byte [rax + 1 * rcx + 0x80], cl        | 30 8c 08 80 00 00 00    |
    | xor byte [rax + 1 * rcx - 0x80], cl        | 30 4c 08 80             |
    | xor byte [rax + 1 * rcx - 0x81], cl        | 30 8c 08 7f ff ff ff    |
    | xor byte [rax + 1 * rcx + 0xff], cl        | 30 8c 08 ff 00 00 00    |
    | xor byte [rax + 1 * rcx - 0xff], cl        | 30 8c 08 01 ff ff ff    |
    | xor byte [rax + 1 * rcx + 0x7fffffff], cl  | 30 8c 08 ff ff ff 7f    |
    | xor byte [rax + 1 * rcx - 0x7fffffff], cl  | 30 8c 08 01 00 00 80    |
    | xor byte [rax + 1 * rcx - 0x80000000], cl  | 30 8c 08 00 00 00 80    |
    | xor byte [r10 + 0x7f], cl                  | 41 30 4a 7f             |
    | xor byte [r10 + 0x80], cl                  | 41 30 8a 80 00 00 00    |
    | xor byte [r10 - 0x80], cl                  | 41 30 4a 80             |
    | xor byte [r10 - 0x81], cl                  | 41 30 8a 7f ff ff ff    |
    | xor byte [rax], al                         | 30 00                   |
    | xor byte [rax], dl                         | 30 10                   |
    | xor byte [rax], bl                         | 30 18                   |
    | xor byte [rax], spl                        | 40 30 20                |
    | xor byte [rax], bpl                        | 40 30 28                |
    | xor byte [rax], sil                        | 40 30 30                |
    | xor byte [rax], dil                        | 40 30 38                |
    | xor byte [rax], r8b                        | 44 30 00                |
    | xor byte [rax], r9b                        | 44 30 08                |
    | xor byte [rax], r10b                       | 44 30 10                |
    | xor byte [rax], r11b                       | 44 30 18                |
    | xor byte [rax], r12b                       | 44 30 20                |
    | xor byte [rax], r13b                       | 44 30 28                |
    | xor byte [rax], r14b                       | 44 30 30                |
    | xor byte [rax], r15b                       | 44 30 38                |
    | xor byte [rax], ah                         | 30 20                   |
    | xor byte [rax], ch                         | 30 28                   |
    | xor byte [rax], dh                         | 30 30                   |
    | xor byte [rax], bh                         | 30 38                   |
    | xor byte [rcx], dl                         | 30 11                   |
    | xor byte [rdx], bl                         | 30 1a                   |
    | xor byte [rbx], spl                        | 40 30 23                |
    | xor byte [rsp], bpl                        | 40 30 2c 24             |
    | xor byte [rbp], sil                        | 40 30 75 00             |
    | xor byte [rsi], dil                        | 40 30 3e                |
    | xor byte [rdi], r8b                        | 44 30 07                |
    | xor byte [r8], r9b                         | 45 30 08                |
    | xor byte [r9], r10b                        | 45 30 11                |
    | xor byte [r10], r11b                       | 45 30 1a                |
    | xor byte [r11], r12b                       | 45 30 23                |
    | xor byte [r12], r13b                       | 45 30 2c 24             |
    | xor byte [r13], r14b                       | 45 30 75 00             |
    | xor byte [r14], r15b                       | 45 30 3e                |
    | xor byte [r15], ah                         | !! !! !!                |
    | xor byte [rax + 1 * rcx], ch               | 30 2c 08                |
    | xor byte [rcx + 1 * rcx], dh               | 30 34 09                |
    | xor byte [rdx + 1 * rcx], bh               | 30 3c 0a                |
    | xor byte [rbx + 1 * rcx], al               | 30 04 0b                |
    | xor byte [rbp + 1 * rcx], dl               | 30 54 0d 00             |
    | xor byte [rsi + 1 * rcx], bl               | 30 1c 0e                |
    | xor byte [rdi + 1 * rcx], spl              | 40 30 24 0f             |
    | xor byte [r8 + 1 * rcx], bpl               | 41 30 2c 08             |
    | xor byte [r9 + 1 * rcx], sil               | 41 30 34 09             |
    | xor byte [r10 + 1 * rcx], dil              | 41 30 3c 0a             |
    | xor byte [r11 + 1 * rcx], r8b              | 45 30 04 0b             |
    | xor byte [r12 + 1 * rcx], r9b              | 45 30 0c 0c             |
    | xor byte [r13 + 1 * rcx], r10b             | 45 30 54 0d 00          |
    | xor byte [r14 + 1 * rcx], r11b             | 45 30 1c 0e             |
    | xor byte [r15 + 1 * rcx], r12b             | 45 30 24 0f             |
    | xor byte [rax + 1 * rax], r13b             | 44 30 2c 00             |
    | xor byte [rax + 1 * rdx], r14b             | 44 30 34 10             |
    | xor byte [rax + 1 * rbx], r15b             | 44 30 3c 18             |
    | xor byte [rax + 1 * rbp], ah               | 30 24 28                |
    | xor byte [rax + 1 * rsi], ch               | 30 2c 30                |
    | xor byte [rax + 1 * rdi], dh               | 30 34 38                |
    | xor byte [rax + 1 * r8], bh                | !! !! !!                |
    | xor byte [rax + 1 * r9], al                | 42 30 04 08             |
    | xor byte [rax + 1 * r11], dl               | 42 30 14 18             |
    | xor byte [rax + 1 * r12], bl               | 42 30 1c 20             |
    | xor byte [rax + 1 * r13], spl              | 42 30 24 28             |
    | xor byte [rax + 1 * r14], bpl              | 42 30 2c 30             |
    | xor byte [rax + 1 * r15], sil              | 42 30 34 38             |
    | xor byte [rax + 2 * rcx], dil              | 40 30 3c 48             |
    | xor byte [rax + 4 * rcx], r8b              | 44 30 04 88             |
    | xor byte [rax + 8 * rcx], r9b              | 44 30 0c c8             |
    | xor byte [r8 + 1 * r9], r10b               | 47 30 14 08             |
    | xor byte [r8 + 2 * r9], r11b               | 47 30 1c 48             |
    | xor byte [r8 + 4 * r9], r12b               | 47 30 24 88             |
    | xor byte [r8 + 8 * r9], r13b               | 47 30 2c c8             |
    | xor byte [1 * rcx], r14b                   | 44 30 34 0d 00 00 00 00 |
    | xor byte [2 * rcx], r15b                   | 44 30 3c 4d 00 00 00 00 |
    | xor byte [4 * rcx], ah                     | 30 24 8d 00 00 00 00    |
    | xor byte [8 * rcx], ch                     | 30 2c cd 00 00 00 00    |
    | xor byte [1 * r9], dh                      | !! !! !!                |
    | xor byte [2 * r9], bh                      | !! !! !!                |
    | xor byte [4 * r9], al                      | 42 30 04 8d 00 00 00 00 |
    | xor byte [r13 + 8 * r12], dl               | 43 30 54 e5 00          |
    | xor byte [rsp + 4 * r15], bl               | 42 30 1c bc             |
    | xor byte [rax + 1 * rcx + 0x00], spl       | 40 30 64 08 00          |
    | xor byte [rax + 1 * rcx - 0x00], bpl       | 40 30 6c 08 00          |
    | xor byte [rax + 1 * rcx + 0x01], sil       | 40 30 74 08 01          |
    | xor byte [rax + 1 * rcx - 0x01], dil       | 40 30 7c 08 ff          |
    | xor byte [rax + 1 * rcx + 0x00000001], r8b | 44 30 84 08 01 00 00 00 |
    | xor byte [rax + 1 * rcx - 0x00000001], r9b | 44 30 8c 08 ff ff ff ff |
    | xor byte [rax + 1 * rcx + 0x7f], r10b      | 44 30 54 08 7f          |
    | xor byte [rax + 1 * rcx - 0x7f], r11b      | 44 30 5c 08 81          |
    | xor byte [rax + 1 * rcx + 0x80], r12b      | 44 30 a4 08 80 00 00 00 |
    | xor byte [rax + 1 * rcx - 0x80], r13b      | 44 30 6c 08 80          |
    | xor byte [rax + 1 * rcx - 0x81], r14b      | 44 30 b4 08 7f ff ff ff |
    | xor byte [rax + 1 * rcx + 0xff], r15b      | 44 30 bc 08 ff 00 00 00 |
    | xor byte [rax + 1 * rcx - 0xff], ah        | 30 a4 08 01 ff ff ff    |
    | xor byte [rax + 1 * rcx + 0x7fffffff], ch  | 30 ac 08 ff ff ff 7f    |
    | xor byte [rax + 1 * rcx - 0x7fffffff], dh  | 30 b4 08 01 00 00 80    |
    | xor byte [rax + 1 * rcx - 0x80000000], bh  | 30 bc 08 00 00 00 80    |
    | xor byte [r10 + 0x7f], al                  | 41 30 42 7f             |
    | xor byte [r10 - 0x80], dl                  | 41 30 52 80             |
    | xor byte [r10 - 0x81], bl                  | 41 30 9a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_xor_addr8_reg8():
    encode(XOR_ADDR8_REG8)
