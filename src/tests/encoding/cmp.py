from tests.encoding.core import encode, exhaust


def can_exhaust_cmp():
    exhaust(
        CMP_ADDR16_IMM16,
        CMP_ADDR16_IMM8,
        CMP_ADDR16_REG16,
        CMP_ADDR32_IMM32,
        CMP_ADDR32_IMM8,
        CMP_ADDR32_REG32,
        CMP_ADDR64_IMM32,
        CMP_ADDR64_IMM8,
        CMP_ADDR64_REG64,
        CMP_ADDR8_IMM8,
        CMP_ADDR8_REG8,
        CMP_REG16_ADDR16,
        CMP_REG16_IMM16,
        CMP_REG16_IMM8,
        CMP_REG16_REG16,
        CMP_REG32_ADDR32,
        CMP_REG32_IMM32,
        CMP_REG32_IMM8,
        CMP_REG32_REG32,
        CMP_REG64_ADDR64,
        CMP_REG64_IMM32,
        CMP_REG64_IMM8,
        CMP_REG64_REG64,
        CMP_REG8_ADDR8,
        CMP_REG8_IMM8,
        CMP_REG8_REG8,
    )


CMP_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | cmp rax, 0x01 | 48 83 f8 01 | *** | cmp rax, 0x00 | 48 83 f8 00 |
    | cmp rcx, 0x01 | 48 83 f9 01 | *** | cmp rax, 0x7f | 48 83 f8 7f |
    | cmp rdx, 0x01 | 48 83 fa 01 | *** | cmp rax, 0x80 | 48 83 f8 80 |
    | cmp rbx, 0x01 | 48 83 fb 01 | *** | cmp rax, 0xff | 48 83 f8 ff |
    | cmp rsp, 0x01 | 48 83 fc 01 | *** | cmp rcx, 0x7f | 48 83 f9 7f |
    | cmp rbp, 0x01 | 48 83 fd 01 | *** | cmp rdx, 0x80 | 48 83 fa 80 |
    | cmp rsi, 0x01 | 48 83 fe 01 | *** | cmp rbx, 0xff | 48 83 fb ff |
    | cmp rdi, 0x01 | 48 83 ff 01 | *** | cmp rsp, 0x00 | 48 83 fc 00 |
    | cmp r8, 0x01  | 49 83 f8 01 | *** | cmp rsi, 0x7f | 48 83 fe 7f |
    | cmp r9, 0x01  | 49 83 f9 01 | *** | cmp rdi, 0x80 | 48 83 ff 80 |
    | cmp r10, 0x01 | 49 83 fa 01 | *** | cmp r8, 0xff  | 49 83 f8 ff |
    | cmp r11, 0x01 | 49 83 fb 01 | *** | cmp r9, 0x00  | 49 83 f9 00 |
    | cmp r12, 0x01 | 49 83 fc 01 | *** | cmp r11, 0x7f | 49 83 fb 7f |
    | cmp r13, 0x01 | 49 83 fd 01 | *** | cmp r12, 0x80 | 49 83 fc 80 |
    | cmp r14, 0x01 | 49 83 fe 01 | *** | cmp r13, 0xff | 49 83 fd ff |
    | cmp r15, 0x01 | 49 83 ff 01 | *** | cmp r14, 0x00 | 49 83 fe 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_cmp_reg64_imm8():
    encode(CMP_REG64_IMM8)


CMP_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | cmp rax, 0x00000001 | 48 3d 01 00 00 00    | *** | cmp rax, 0x00007fff | 48 3d ff 7f 00 00    |
    | cmp rcx, 0x00000001 | 48 81 f9 01 00 00 00 | *** | cmp rax, 0x00008000 | 48 3d 00 80 00 00    |
    | cmp rdx, 0x00000001 | 48 81 fa 01 00 00 00 | *** | cmp rax, 0x0000ffff | 48 3d ff ff 00 00    |
    | cmp rbx, 0x00000001 | 48 81 fb 01 00 00 00 | *** | cmp rax, 0x00010000 | 48 3d 00 00 01 00    |
    | cmp rsp, 0x00000001 | 48 81 fc 01 00 00 00 | *** | cmp rax, 0x7fffffff | 48 3d ff ff ff 7f    |
    | cmp rbp, 0x00000001 | 48 81 fd 01 00 00 00 | *** | cmp rax, 0x80000000 | 48 3d 00 00 00 80    |
    | cmp rsi, 0x00000001 | 48 81 fe 01 00 00 00 | *** | cmp rax, 0xffffffff | 48 3d ff ff ff ff    |
    | cmp rdi, 0x00000001 | 48 81 ff 01 00 00 00 | *** | cmp rcx, 0x0000007f | 48 81 f9 7f 00 00 00 |
    | cmp r8, 0x00000001  | 49 81 f8 01 00 00 00 | *** | cmp rdx, 0x00000080 | 48 81 fa 80 00 00 00 |
    | cmp r9, 0x00000001  | 49 81 f9 01 00 00 00 | *** | cmp rbx, 0x000000ff | 48 81 fb ff 00 00 00 |
    | cmp r10, 0x00000001 | 49 81 fa 01 00 00 00 | *** | cmp rsp, 0x00000100 | 48 81 fc 00 01 00 00 |
    | cmp r11, 0x00000001 | 49 81 fb 01 00 00 00 | *** | cmp rbp, 0x00007fff | 48 81 fd ff 7f 00 00 |
    | cmp r12, 0x00000001 | 49 81 fc 01 00 00 00 | *** | cmp rsi, 0x00008000 | 48 81 fe 00 80 00 00 |
    | cmp r13, 0x00000001 | 49 81 fd 01 00 00 00 | *** | cmp rdi, 0x0000ffff | 48 81 ff ff ff 00 00 |
    | cmp r14, 0x00000001 | 49 81 fe 01 00 00 00 | *** | cmp r8, 0x00010000  | 49 81 f8 00 00 01 00 |
    | cmp r15, 0x00000001 | 49 81 ff 01 00 00 00 | *** | cmp r9, 0x7fffffff  | 49 81 f9 ff ff ff 7f |
    | cmp rax, 0x00000000 | 48 3d 00 00 00 00    | *** | cmp r10, 0x80000000 | 49 81 fa 00 00 00 80 |
    | cmp rax, 0x0000007f | 48 3d 7f 00 00 00    | *** | cmp r11, 0xffffffff | 49 81 fb ff ff ff ff |
    | cmp rax, 0x00000080 | 48 3d 80 00 00 00    | *** | cmp r12, 0x00000000 | 49 81 fc 00 00 00 00 |
    | cmp rax, 0x000000ff | 48 3d ff 00 00 00    | *** | cmp r14, 0x0000007f | 49 81 fe 7f 00 00 00 |
    | cmp rax, 0x00000100 | 48 3d 00 01 00 00    | *** | cmp r15, 0x00000080 | 49 81 ff 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_cmp_reg64_imm32():
    encode(CMP_REG64_IMM32)


CMP_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | cmp rax, rcx | 48 39 c8 | *** | cmp rax, r8  | 4c 39 c0 |
    | cmp rcx, rcx | 48 39 c9 | *** | cmp rax, r9  | 4c 39 c8 |
    | cmp rdx, rcx | 48 39 ca | *** | cmp rax, r10 | 4c 39 d0 |
    | cmp rbx, rcx | 48 39 cb | *** | cmp rax, r11 | 4c 39 d8 |
    | cmp rsp, rcx | 48 39 cc | *** | cmp rax, r12 | 4c 39 e0 |
    | cmp rbp, rcx | 48 39 cd | *** | cmp rax, r13 | 4c 39 e8 |
    | cmp rsi, rcx | 48 39 ce | *** | cmp rax, r14 | 4c 39 f0 |
    | cmp rdi, rcx | 48 39 cf | *** | cmp rax, r15 | 4c 39 f8 |
    | cmp r8, rcx  | 49 39 c8 | *** | cmp rcx, rdx | 48 39 d1 |
    | cmp r9, rcx  | 49 39 c9 | *** | cmp rdx, rbx | 48 39 da |
    | cmp r10, rcx | 49 39 ca | *** | cmp rbx, rsp | 48 39 e3 |
    | cmp r11, rcx | 49 39 cb | *** | cmp rsp, rbp | 48 39 ec |
    | cmp r12, rcx | 49 39 cc | *** | cmp rbp, rsi | 48 39 f5 |
    | cmp r13, rcx | 49 39 cd | *** | cmp rsi, rdi | 48 39 fe |
    | cmp r14, rcx | 49 39 ce | *** | cmp rdi, r8  | 4c 39 c7 |
    | cmp r15, rcx | 49 39 cf | *** | cmp r8, r9   | 4d 39 c8 |
    | cmp rax, rax | 48 39 c0 | *** | cmp r9, r10  | 4d 39 d1 |
    | cmp rax, rdx | 48 39 d0 | *** | cmp r10, r11 | 4d 39 da |
    | cmp rax, rbx | 48 39 d8 | *** | cmp r11, r12 | 4d 39 e3 |
    | cmp rax, rsp | 48 39 e0 | *** | cmp r12, r13 | 4d 39 ec |
    | cmp rax, rbp | 48 39 e8 | *** | cmp r13, r14 | 4d 39 f5 |
    | cmp rax, rsi | 48 39 f0 | *** | cmp r14, r15 | 4d 39 fe |
    | cmp rax, rdi | 48 39 f8 | *** | cmp r15, rax | 49 39 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_cmp_reg64_reg64():
    encode(CMP_REG64_REG64)


CMP_REG64_ADDR64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | cmp rax, qword [rcx]                        | 48 3b 01                |
    | cmp rcx, qword [rcx]                        | 48 3b 09                |
    | cmp rdx, qword [rcx]                        | 48 3b 11                |
    | cmp rbx, qword [rcx]                        | 48 3b 19                |
    | cmp rsp, qword [rcx]                        | 48 3b 21                |
    | cmp rbp, qword [rcx]                        | 48 3b 29                |
    | cmp rsi, qword [rcx]                        | 48 3b 31                |
    | cmp rdi, qword [rcx]                        | 48 3b 39                |
    | cmp r8, qword [rcx]                         | 4c 3b 01                |
    | cmp r9, qword [rcx]                         | 4c 3b 09                |
    | cmp r10, qword [rcx]                        | 4c 3b 11                |
    | cmp r11, qword [rcx]                        | 4c 3b 19                |
    | cmp r12, qword [rcx]                        | 4c 3b 21                |
    | cmp r13, qword [rcx]                        | 4c 3b 29                |
    | cmp r14, qword [rcx]                        | 4c 3b 31                |
    | cmp r15, qword [rcx]                        | 4c 3b 39                |
    | cmp rax, qword [rax]                        | 48 3b 00                |
    | cmp rax, qword [rdx]                        | 48 3b 02                |
    | cmp rax, qword [rbx]                        | 48 3b 03                |
    | cmp rax, qword [rsp]                        | 48 3b 04 24             |
    | cmp rax, qword [rbp]                        | 48 3b 45 00             |
    | cmp rax, qword [rsi]                        | 48 3b 06                |
    | cmp rax, qword [rdi]                        | 48 3b 07                |
    | cmp rax, qword [r8]                         | 49 3b 00                |
    | cmp rax, qword [r9]                         | 49 3b 01                |
    | cmp rax, qword [r10]                        | 49 3b 02                |
    | cmp rax, qword [r11]                        | 49 3b 03                |
    | cmp rax, qword [r12]                        | 49 3b 04 24             |
    | cmp rax, qword [r13]                        | 49 3b 45 00             |
    | cmp rax, qword [r14]                        | 49 3b 06                |
    | cmp rax, qword [r15]                        | 49 3b 07                |
    | cmp rax, qword [rax + 1 * rcx]              | 48 3b 04 08             |
    | cmp rax, qword [rcx + 1 * rcx]              | 48 3b 04 09             |
    | cmp rax, qword [rdx + 1 * rcx]              | 48 3b 04 0a             |
    | cmp rax, qword [rbx + 1 * rcx]              | 48 3b 04 0b             |
    | cmp rax, qword [rsp + 1 * rcx]              | 48 3b 04 0c             |
    | cmp rax, qword [rbp + 1 * rcx]              | 48 3b 44 0d 00          |
    | cmp rax, qword [rsi + 1 * rcx]              | 48 3b 04 0e             |
    | cmp rax, qword [rdi + 1 * rcx]              | 48 3b 04 0f             |
    | cmp rax, qword [r8 + 1 * rcx]               | 49 3b 04 08             |
    | cmp rax, qword [r9 + 1 * rcx]               | 49 3b 04 09             |
    | cmp rax, qword [r10 + 1 * rcx]              | 49 3b 04 0a             |
    | cmp rax, qword [r11 + 1 * rcx]              | 49 3b 04 0b             |
    | cmp rax, qword [r12 + 1 * rcx]              | 49 3b 04 0c             |
    | cmp rax, qword [r13 + 1 * rcx]              | 49 3b 44 0d 00          |
    | cmp rax, qword [r14 + 1 * rcx]              | 49 3b 04 0e             |
    | cmp rax, qword [r15 + 1 * rcx]              | 49 3b 04 0f             |
    | cmp rax, qword [rax + 1 * rax]              | 48 3b 04 00             |
    | cmp rax, qword [rax + 1 * rdx]              | 48 3b 04 10             |
    | cmp rax, qword [rax + 1 * rbx]              | 48 3b 04 18             |
    | cmp rax, qword [rax + 1 * rbp]              | 48 3b 04 28             |
    | cmp rax, qword [rax + 1 * rsi]              | 48 3b 04 30             |
    | cmp rax, qword [rax + 1 * rdi]              | 48 3b 04 38             |
    | cmp rax, qword [rax + 1 * r8]               | 4a 3b 04 00             |
    | cmp rax, qword [rax + 1 * r9]               | 4a 3b 04 08             |
    | cmp rax, qword [rax + 1 * r10]              | 4a 3b 04 10             |
    | cmp rax, qword [rax + 1 * r11]              | 4a 3b 04 18             |
    | cmp rax, qword [rax + 1 * r12]              | 4a 3b 04 20             |
    | cmp rax, qword [rax + 1 * r13]              | 4a 3b 04 28             |
    | cmp rax, qword [rax + 1 * r14]              | 4a 3b 04 30             |
    | cmp rax, qword [rax + 1 * r15]              | 4a 3b 04 38             |
    | cmp rax, qword [rax + 2 * rcx]              | 48 3b 04 48             |
    | cmp rax, qword [rax + 4 * rcx]              | 48 3b 04 88             |
    | cmp rax, qword [rax + 8 * rcx]              | 48 3b 04 c8             |
    | cmp rax, qword [r8 + 1 * r9]                | 4b 3b 04 08             |
    | cmp rax, qword [r8 + 2 * r9]                | 4b 3b 04 48             |
    | cmp rax, qword [r8 + 4 * r9]                | 4b 3b 04 88             |
    | cmp rax, qword [r8 + 8 * r9]                | 4b 3b 04 c8             |
    | cmp rax, qword [1 * rcx]                    | 48 3b 04 0d 00 00 00 00 |
    | cmp rax, qword [2 * rcx]                    | 48 3b 04 4d 00 00 00 00 |
    | cmp rax, qword [4 * rcx]                    | 48 3b 04 8d 00 00 00 00 |
    | cmp rax, qword [8 * rcx]                    | 48 3b 04 cd 00 00 00 00 |
    | cmp rax, qword [1 * r9]                     | 4a 3b 04 0d 00 00 00 00 |
    | cmp rax, qword [2 * r9]                     | 4a 3b 04 4d 00 00 00 00 |
    | cmp rax, qword [4 * r9]                     | 4a 3b 04 8d 00 00 00 00 |
    | cmp rax, qword [8 * r9]                     | 4a 3b 04 cd 00 00 00 00 |
    | cmp rax, qword [r13 + 8 * r12]              | 4b 3b 44 e5 00          |
    | cmp rax, qword [rsp + 4 * r15]              | 4a 3b 04 bc             |
    | cmp rax, qword [rax + 1 * rcx + 0x00]       | 48 3b 44 08 00          |
    | cmp rax, qword [rax + 1 * rcx - 0x00]       | 48 3b 44 08 00          |
    | cmp rax, qword [rax + 1 * rcx + 0x01]       | 48 3b 44 08 01          |
    | cmp rax, qword [rax + 1 * rcx - 0x01]       | 48 3b 44 08 ff          |
    | cmp rax, qword [rax + 1 * rcx + 0x00000001] | 48 3b 84 08 01 00 00 00 |
    | cmp rax, qword [rax + 1 * rcx - 0x00000001] | 48 3b 84 08 ff ff ff ff |
    | cmp rax, qword [rax + 1 * rcx + 0x7f]       | 48 3b 44 08 7f          |
    | cmp rax, qword [rax + 1 * rcx - 0x7f]       | 48 3b 44 08 81          |
    | cmp rax, qword [rax + 1 * rcx + 0x80]       | 48 3b 84 08 80 00 00 00 |
    | cmp rax, qword [rax + 1 * rcx - 0x80]       | 48 3b 44 08 80          |
    | cmp rax, qword [rax + 1 * rcx - 0x81]       | 48 3b 84 08 7f ff ff ff |
    | cmp rax, qword [rax + 1 * rcx + 0xff]       | 48 3b 84 08 ff 00 00 00 |
    | cmp rax, qword [rax + 1 * rcx - 0xff]       | 48 3b 84 08 01 ff ff ff |
    | cmp rax, qword [rax + 1 * rcx + 0x7fffffff] | 48 3b 84 08 ff ff ff 7f |
    | cmp rax, qword [rax + 1 * rcx - 0x7fffffff] | 48 3b 84 08 01 00 00 80 |
    | cmp rax, qword [rax + 1 * rcx - 0x80000000] | 48 3b 84 08 00 00 00 80 |
    | cmp rax, qword [r10 + 0x7f]                 | 49 3b 42 7f             |
    | cmp rax, qword [r10 + 0x80]                 | 49 3b 82 80 00 00 00    |
    | cmp rax, qword [r10 - 0x80]                 | 49 3b 42 80             |
    | cmp rax, qword [r10 - 0x81]                 | 49 3b 82 7f ff ff ff    |
    | cmp rcx, qword [rdx]                        | 48 3b 0a                |
    | cmp rdx, qword [rbx]                        | 48 3b 13                |
    | cmp rbx, qword [rsp]                        | 48 3b 1c 24             |
    | cmp rsp, qword [rbp]                        | 48 3b 65 00             |
    | cmp rbp, qword [rsi]                        | 48 3b 2e                |
    | cmp rsi, qword [rdi]                        | 48 3b 37                |
    | cmp rdi, qword [r8]                         | 49 3b 38                |
    | cmp r8, qword [r9]                          | 4d 3b 01                |
    | cmp r9, qword [r10]                         | 4d 3b 0a                |
    | cmp r10, qword [r11]                        | 4d 3b 13                |
    | cmp r11, qword [r12]                        | 4d 3b 1c 24             |
    | cmp r12, qword [r13]                        | 4d 3b 65 00             |
    | cmp r13, qword [r14]                        | 4d 3b 2e                |
    | cmp r14, qword [r15]                        | 4d 3b 37                |
    | cmp r15, qword [rax + 1 * rcx]              | 4c 3b 3c 08             |
    | cmp rcx, qword [rdx + 1 * rcx]              | 48 3b 0c 0a             |
    | cmp rdx, qword [rbx + 1 * rcx]              | 48 3b 14 0b             |
    | cmp rbx, qword [rsp + 1 * rcx]              | 48 3b 1c 0c             |
    | cmp rsp, qword [rbp + 1 * rcx]              | 48 3b 64 0d 00          |
    | cmp rbp, qword [rsi + 1 * rcx]              | 48 3b 2c 0e             |
    | cmp rsi, qword [rdi + 1 * rcx]              | 48 3b 34 0f             |
    | cmp rdi, qword [r8 + 1 * rcx]               | 49 3b 3c 08             |
    | cmp r8, qword [r9 + 1 * rcx]                | 4d 3b 04 09             |
    | cmp r9, qword [r10 + 1 * rcx]               | 4d 3b 0c 0a             |
    | cmp r10, qword [r11 + 1 * rcx]              | 4d 3b 14 0b             |
    | cmp r11, qword [r12 + 1 * rcx]              | 4d 3b 1c 0c             |
    | cmp r12, qword [r13 + 1 * rcx]              | 4d 3b 64 0d 00          |
    | cmp r13, qword [r14 + 1 * rcx]              | 4d 3b 2c 0e             |
    | cmp r14, qword [r15 + 1 * rcx]              | 4d 3b 34 0f             |
    | cmp r15, qword [rax + 1 * rax]              | 4c 3b 3c 00             |
    | cmp rcx, qword [rax + 1 * rbx]              | 48 3b 0c 18             |
    | cmp rdx, qword [rax + 1 * rbp]              | 48 3b 14 28             |
    | cmp rbx, qword [rax + 1 * rsi]              | 48 3b 1c 30             |
    | cmp rsp, qword [rax + 1 * rdi]              | 48 3b 24 38             |
    | cmp rbp, qword [rax + 1 * r8]               | 4a 3b 2c 00             |
    | cmp rsi, qword [rax + 1 * r9]               | 4a 3b 34 08             |
    | cmp rdi, qword [rax + 1 * r10]              | 4a 3b 3c 10             |
    | cmp r8, qword [rax + 1 * r11]               | 4e 3b 04 18             |
    | cmp r9, qword [rax + 1 * r12]               | 4e 3b 0c 20             |
    | cmp r10, qword [rax + 1 * r13]              | 4e 3b 14 28             |
    | cmp r11, qword [rax + 1 * r14]              | 4e 3b 1c 30             |
    | cmp r12, qword [rax + 1 * r15]              | 4e 3b 24 38             |
    | cmp r13, qword [rax + 2 * rcx]              | 4c 3b 2c 48             |
    | cmp r14, qword [rax + 4 * rcx]              | 4c 3b 34 88             |
    | cmp r15, qword [rax + 8 * rcx]              | 4c 3b 3c c8             |
    | cmp rcx, qword [r8 + 2 * r9]                | 4b 3b 0c 48             |
    | cmp rdx, qword [r8 + 4 * r9]                | 4b 3b 14 88             |
    | cmp rbx, qword [r8 + 8 * r9]                | 4b 3b 1c c8             |
    | cmp rsp, qword [1 * rcx]                    | 48 3b 24 0d 00 00 00 00 |
    | cmp rbp, qword [2 * rcx]                    | 48 3b 2c 4d 00 00 00 00 |
    | cmp rsi, qword [4 * rcx]                    | 48 3b 34 8d 00 00 00 00 |
    | cmp rdi, qword [8 * rcx]                    | 48 3b 3c cd 00 00 00 00 |
    | cmp r8, qword [1 * r9]                      | 4e 3b 04 0d 00 00 00 00 |
    | cmp r9, qword [2 * r9]                      | 4e 3b 0c 4d 00 00 00 00 |
    | cmp r10, qword [4 * r9]                     | 4e 3b 14 8d 00 00 00 00 |
    | cmp r11, qword [8 * r9]                     | 4e 3b 1c cd 00 00 00 00 |
    | cmp r12, qword [r13 + 8 * r12]              | 4f 3b 64 e5 00          |
    | cmp r13, qword [rsp + 4 * r15]              | 4e 3b 2c bc             |
    | cmp r14, qword [rax + 1 * rcx + 0x00]       | 4c 3b 74 08 00          |
    | cmp r15, qword [rax + 1 * rcx - 0x00]       | 4c 3b 7c 08 00          |
    | cmp rcx, qword [rax + 1 * rcx - 0x01]       | 48 3b 4c 08 ff          |
    | cmp rdx, qword [rax + 1 * rcx + 0x00000001] | 48 3b 94 08 01 00 00 00 |
    | cmp rbx, qword [rax + 1 * rcx - 0x00000001] | 48 3b 9c 08 ff ff ff ff |
    | cmp rsp, qword [rax + 1 * rcx + 0x7f]       | 48 3b 64 08 7f          |
    | cmp rbp, qword [rax + 1 * rcx - 0x7f]       | 48 3b 6c 08 81          |
    | cmp rsi, qword [rax + 1 * rcx + 0x80]       | 48 3b b4 08 80 00 00 00 |
    | cmp rdi, qword [rax + 1 * rcx - 0x80]       | 48 3b 7c 08 80          |
    | cmp r8, qword [rax + 1 * rcx - 0x81]        | 4c 3b 84 08 7f ff ff ff |
    | cmp r9, qword [rax + 1 * rcx + 0xff]        | 4c 3b 8c 08 ff 00 00 00 |
    | cmp r10, qword [rax + 1 * rcx - 0xff]       | 4c 3b 94 08 01 ff ff ff |
    | cmp r11, qword [rax + 1 * rcx + 0x7fffffff] | 4c 3b 9c 08 ff ff ff 7f |
    | cmp r12, qword [rax + 1 * rcx - 0x7fffffff] | 4c 3b a4 08 01 00 00 80 |
    | cmp r13, qword [rax + 1 * rcx - 0x80000000] | 4c 3b ac 08 00 00 00 80 |
    | cmp r14, qword [r10 + 0x7f]                 | 4d 3b 72 7f             |
    | cmp r15, qword [r10 + 0x80]                 | 4d 3b ba 80 00 00 00    |
    | cmp rcx, qword [r10 - 0x81]                 | 49 3b 8a 7f ff ff ff    |
    | cmp rdx, qword [rax]                        | 48 3b 10                |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_cmp_reg64_addr64():
    encode(CMP_REG64_ADDR64)


CMP_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | cmp eax, 0x01  | 83 f8 01    | *** | cmp eax, 0x00  | 83 f8 00    |
    | cmp ecx, 0x01  | 83 f9 01    | *** | cmp eax, 0x7f  | 83 f8 7f    |
    | cmp edx, 0x01  | 83 fa 01    | *** | cmp eax, 0x80  | 83 f8 80    |
    | cmp ebx, 0x01  | 83 fb 01    | *** | cmp eax, 0xff  | 83 f8 ff    |
    | cmp esp, 0x01  | 83 fc 01    | *** | cmp ecx, 0x7f  | 83 f9 7f    |
    | cmp ebp, 0x01  | 83 fd 01    | *** | cmp edx, 0x80  | 83 fa 80    |
    | cmp esi, 0x01  | 83 fe 01    | *** | cmp ebx, 0xff  | 83 fb ff    |
    | cmp edi, 0x01  | 83 ff 01    | *** | cmp esp, 0x00  | 83 fc 00    |
    | cmp r8d, 0x01  | 41 83 f8 01 | *** | cmp esi, 0x7f  | 83 fe 7f    |
    | cmp r9d, 0x01  | 41 83 f9 01 | *** | cmp edi, 0x80  | 83 ff 80    |
    | cmp r10d, 0x01 | 41 83 fa 01 | *** | cmp r8d, 0xff  | 41 83 f8 ff |
    | cmp r11d, 0x01 | 41 83 fb 01 | *** | cmp r9d, 0x00  | 41 83 f9 00 |
    | cmp r12d, 0x01 | 41 83 fc 01 | *** | cmp r11d, 0x7f | 41 83 fb 7f |
    | cmp r13d, 0x01 | 41 83 fd 01 | *** | cmp r12d, 0x80 | 41 83 fc 80 |
    | cmp r14d, 0x01 | 41 83 fe 01 | *** | cmp r13d, 0xff | 41 83 fd ff |
    | cmp r15d, 0x01 | 41 83 ff 01 | *** | cmp r14d, 0x00 | 41 83 fe 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_cmp_reg32_imm8():
    encode(CMP_REG32_IMM8)


CMP_REG32_IMM32 = """
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | instruction          | encoding             | *** | instruction          | encoding             |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | cmp eax, 0x00000001  | 3d 01 00 00 00       | *** | cmp eax, 0x00007fff  | 3d ff 7f 00 00       |
    | cmp ecx, 0x00000001  | 81 f9 01 00 00 00    | *** | cmp eax, 0x00008000  | 3d 00 80 00 00       |
    | cmp edx, 0x00000001  | 81 fa 01 00 00 00    | *** | cmp eax, 0x0000ffff  | 3d ff ff 00 00       |
    | cmp ebx, 0x00000001  | 81 fb 01 00 00 00    | *** | cmp eax, 0x00010000  | 3d 00 00 01 00       |
    | cmp esp, 0x00000001  | 81 fc 01 00 00 00    | *** | cmp eax, 0x7fffffff  | 3d ff ff ff 7f       |
    | cmp ebp, 0x00000001  | 81 fd 01 00 00 00    | *** | cmp eax, 0x80000000  | 3d 00 00 00 80       |
    | cmp esi, 0x00000001  | 81 fe 01 00 00 00    | *** | cmp eax, 0xffffffff  | 3d ff ff ff ff       |
    | cmp edi, 0x00000001  | 81 ff 01 00 00 00    | *** | cmp ecx, 0x0000007f  | 81 f9 7f 00 00 00    |
    | cmp r8d, 0x00000001  | 41 81 f8 01 00 00 00 | *** | cmp edx, 0x00000080  | 81 fa 80 00 00 00    |
    | cmp r9d, 0x00000001  | 41 81 f9 01 00 00 00 | *** | cmp ebx, 0x000000ff  | 81 fb ff 00 00 00    |
    | cmp r10d, 0x00000001 | 41 81 fa 01 00 00 00 | *** | cmp esp, 0x00000100  | 81 fc 00 01 00 00    |
    | cmp r11d, 0x00000001 | 41 81 fb 01 00 00 00 | *** | cmp ebp, 0x00007fff  | 81 fd ff 7f 00 00    |
    | cmp r12d, 0x00000001 | 41 81 fc 01 00 00 00 | *** | cmp esi, 0x00008000  | 81 fe 00 80 00 00    |
    | cmp r13d, 0x00000001 | 41 81 fd 01 00 00 00 | *** | cmp edi, 0x0000ffff  | 81 ff ff ff 00 00    |
    | cmp r14d, 0x00000001 | 41 81 fe 01 00 00 00 | *** | cmp r8d, 0x00010000  | 41 81 f8 00 00 01 00 |
    | cmp r15d, 0x00000001 | 41 81 ff 01 00 00 00 | *** | cmp r9d, 0x7fffffff  | 41 81 f9 ff ff ff 7f |
    | cmp eax, 0x00000000  | 3d 00 00 00 00       | *** | cmp r10d, 0x80000000 | 41 81 fa 00 00 00 80 |
    | cmp eax, 0x0000007f  | 3d 7f 00 00 00       | *** | cmp r11d, 0xffffffff | 41 81 fb ff ff ff ff |
    | cmp eax, 0x00000080  | 3d 80 00 00 00       | *** | cmp r12d, 0x00000000 | 41 81 fc 00 00 00 00 |
    | cmp eax, 0x000000ff  | 3d ff 00 00 00       | *** | cmp r14d, 0x0000007f | 41 81 fe 7f 00 00 00 |
    | cmp eax, 0x00000100  | 3d 00 01 00 00       | *** | cmp r15d, 0x00000080 | 41 81 ff 80 00 00 00 |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
"""


def can_encode_cmp_reg32_imm32():
    encode(CMP_REG32_IMM32)


CMP_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | cmp eax, ecx   | 39 c8    | *** | cmp eax, r8d   | 44 39 c0 |
    | cmp ecx, ecx   | 39 c9    | *** | cmp eax, r9d   | 44 39 c8 |
    | cmp edx, ecx   | 39 ca    | *** | cmp eax, r10d  | 44 39 d0 |
    | cmp ebx, ecx   | 39 cb    | *** | cmp eax, r11d  | 44 39 d8 |
    | cmp esp, ecx   | 39 cc    | *** | cmp eax, r12d  | 44 39 e0 |
    | cmp ebp, ecx   | 39 cd    | *** | cmp eax, r13d  | 44 39 e8 |
    | cmp esi, ecx   | 39 ce    | *** | cmp eax, r14d  | 44 39 f0 |
    | cmp edi, ecx   | 39 cf    | *** | cmp eax, r15d  | 44 39 f8 |
    | cmp r8d, ecx   | 41 39 c8 | *** | cmp ecx, edx   | 39 d1    |
    | cmp r9d, ecx   | 41 39 c9 | *** | cmp edx, ebx   | 39 da    |
    | cmp r10d, ecx  | 41 39 ca | *** | cmp ebx, esp   | 39 e3    |
    | cmp r11d, ecx  | 41 39 cb | *** | cmp esp, ebp   | 39 ec    |
    | cmp r12d, ecx  | 41 39 cc | *** | cmp ebp, esi   | 39 f5    |
    | cmp r13d, ecx  | 41 39 cd | *** | cmp esi, edi   | 39 fe    |
    | cmp r14d, ecx  | 41 39 ce | *** | cmp edi, r8d   | 44 39 c7 |
    | cmp r15d, ecx  | 41 39 cf | *** | cmp r8d, r9d   | 45 39 c8 |
    | cmp eax, eax   | 39 c0    | *** | cmp r9d, r10d  | 45 39 d1 |
    | cmp eax, edx   | 39 d0    | *** | cmp r10d, r11d | 45 39 da |
    | cmp eax, ebx   | 39 d8    | *** | cmp r11d, r12d | 45 39 e3 |
    | cmp eax, esp   | 39 e0    | *** | cmp r12d, r13d | 45 39 ec |
    | cmp eax, ebp   | 39 e8    | *** | cmp r13d, r14d | 45 39 f5 |
    | cmp eax, esi   | 39 f0    | *** | cmp r14d, r15d | 45 39 fe |
    | cmp eax, edi   | 39 f8    | *** | cmp r15d, eax  | 41 39 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_cmp_reg32_reg32():
    encode(CMP_REG32_REG32)


CMP_REG32_ADDR32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | cmp eax, dword [rcx]                         | 3b 01                   |
    | cmp ecx, dword [rcx]                         | 3b 09                   |
    | cmp edx, dword [rcx]                         | 3b 11                   |
    | cmp ebx, dword [rcx]                         | 3b 19                   |
    | cmp esp, dword [rcx]                         | 3b 21                   |
    | cmp ebp, dword [rcx]                         | 3b 29                   |
    | cmp esi, dword [rcx]                         | 3b 31                   |
    | cmp edi, dword [rcx]                         | 3b 39                   |
    | cmp r8d, dword [rcx]                         | 44 3b 01                |
    | cmp r9d, dword [rcx]                         | 44 3b 09                |
    | cmp r10d, dword [rcx]                        | 44 3b 11                |
    | cmp r11d, dword [rcx]                        | 44 3b 19                |
    | cmp r12d, dword [rcx]                        | 44 3b 21                |
    | cmp r13d, dword [rcx]                        | 44 3b 29                |
    | cmp r14d, dword [rcx]                        | 44 3b 31                |
    | cmp r15d, dword [rcx]                        | 44 3b 39                |
    | cmp eax, dword [rax]                         | 3b 00                   |
    | cmp eax, dword [rdx]                         | 3b 02                   |
    | cmp eax, dword [rbx]                         | 3b 03                   |
    | cmp eax, dword [rsp]                         | 3b 04 24                |
    | cmp eax, dword [rbp]                         | 3b 45 00                |
    | cmp eax, dword [rsi]                         | 3b 06                   |
    | cmp eax, dword [rdi]                         | 3b 07                   |
    | cmp eax, dword [r8]                          | 41 3b 00                |
    | cmp eax, dword [r9]                          | 41 3b 01                |
    | cmp eax, dword [r10]                         | 41 3b 02                |
    | cmp eax, dword [r11]                         | 41 3b 03                |
    | cmp eax, dword [r12]                         | 41 3b 04 24             |
    | cmp eax, dword [r13]                         | 41 3b 45 00             |
    | cmp eax, dword [r14]                         | 41 3b 06                |
    | cmp eax, dword [r15]                         | 41 3b 07                |
    | cmp eax, dword [rax + 1 * rcx]               | 3b 04 08                |
    | cmp eax, dword [rcx + 1 * rcx]               | 3b 04 09                |
    | cmp eax, dword [rdx + 1 * rcx]               | 3b 04 0a                |
    | cmp eax, dword [rbx + 1 * rcx]               | 3b 04 0b                |
    | cmp eax, dword [rsp + 1 * rcx]               | 3b 04 0c                |
    | cmp eax, dword [rbp + 1 * rcx]               | 3b 44 0d 00             |
    | cmp eax, dword [rsi + 1 * rcx]               | 3b 04 0e                |
    | cmp eax, dword [rdi + 1 * rcx]               | 3b 04 0f                |
    | cmp eax, dword [r8 + 1 * rcx]                | 41 3b 04 08             |
    | cmp eax, dword [r9 + 1 * rcx]                | 41 3b 04 09             |
    | cmp eax, dword [r10 + 1 * rcx]               | 41 3b 04 0a             |
    | cmp eax, dword [r11 + 1 * rcx]               | 41 3b 04 0b             |
    | cmp eax, dword [r12 + 1 * rcx]               | 41 3b 04 0c             |
    | cmp eax, dword [r13 + 1 * rcx]               | 41 3b 44 0d 00          |
    | cmp eax, dword [r14 + 1 * rcx]               | 41 3b 04 0e             |
    | cmp eax, dword [r15 + 1 * rcx]               | 41 3b 04 0f             |
    | cmp eax, dword [rax + 1 * rax]               | 3b 04 00                |
    | cmp eax, dword [rax + 1 * rdx]               | 3b 04 10                |
    | cmp eax, dword [rax + 1 * rbx]               | 3b 04 18                |
    | cmp eax, dword [rax + 1 * rbp]               | 3b 04 28                |
    | cmp eax, dword [rax + 1 * rsi]               | 3b 04 30                |
    | cmp eax, dword [rax + 1 * rdi]               | 3b 04 38                |
    | cmp eax, dword [rax + 1 * r8]                | 42 3b 04 00             |
    | cmp eax, dword [rax + 1 * r9]                | 42 3b 04 08             |
    | cmp eax, dword [rax + 1 * r10]               | 42 3b 04 10             |
    | cmp eax, dword [rax + 1 * r11]               | 42 3b 04 18             |
    | cmp eax, dword [rax + 1 * r12]               | 42 3b 04 20             |
    | cmp eax, dword [rax + 1 * r13]               | 42 3b 04 28             |
    | cmp eax, dword [rax + 1 * r14]               | 42 3b 04 30             |
    | cmp eax, dword [rax + 1 * r15]               | 42 3b 04 38             |
    | cmp eax, dword [rax + 2 * rcx]               | 3b 04 48                |
    | cmp eax, dword [rax + 4 * rcx]               | 3b 04 88                |
    | cmp eax, dword [rax + 8 * rcx]               | 3b 04 c8                |
    | cmp eax, dword [r8 + 1 * r9]                 | 43 3b 04 08             |
    | cmp eax, dword [r8 + 2 * r9]                 | 43 3b 04 48             |
    | cmp eax, dword [r8 + 4 * r9]                 | 43 3b 04 88             |
    | cmp eax, dword [r8 + 8 * r9]                 | 43 3b 04 c8             |
    | cmp eax, dword [1 * rcx]                     | 3b 04 0d 00 00 00 00    |
    | cmp eax, dword [2 * rcx]                     | 3b 04 4d 00 00 00 00    |
    | cmp eax, dword [4 * rcx]                     | 3b 04 8d 00 00 00 00    |
    | cmp eax, dword [8 * rcx]                     | 3b 04 cd 00 00 00 00    |
    | cmp eax, dword [1 * r9]                      | 42 3b 04 0d 00 00 00 00 |
    | cmp eax, dword [2 * r9]                      | 42 3b 04 4d 00 00 00 00 |
    | cmp eax, dword [4 * r9]                      | 42 3b 04 8d 00 00 00 00 |
    | cmp eax, dword [8 * r9]                      | 42 3b 04 cd 00 00 00 00 |
    | cmp eax, dword [r13 + 8 * r12]               | 43 3b 44 e5 00          |
    | cmp eax, dword [rsp + 4 * r15]               | 42 3b 04 bc             |
    | cmp eax, dword [rax + 1 * rcx + 0x00]        | 3b 44 08 00             |
    | cmp eax, dword [rax + 1 * rcx - 0x00]        | 3b 44 08 00             |
    | cmp eax, dword [rax + 1 * rcx + 0x01]        | 3b 44 08 01             |
    | cmp eax, dword [rax + 1 * rcx - 0x01]        | 3b 44 08 ff             |
    | cmp eax, dword [rax + 1 * rcx + 0x00000001]  | 3b 84 08 01 00 00 00    |
    | cmp eax, dword [rax + 1 * rcx - 0x00000001]  | 3b 84 08 ff ff ff ff    |
    | cmp eax, dword [rax + 1 * rcx + 0x7f]        | 3b 44 08 7f             |
    | cmp eax, dword [rax + 1 * rcx - 0x7f]        | 3b 44 08 81             |
    | cmp eax, dword [rax + 1 * rcx + 0x80]        | 3b 84 08 80 00 00 00    |
    | cmp eax, dword [rax + 1 * rcx - 0x80]        | 3b 44 08 80             |
    | cmp eax, dword [rax + 1 * rcx - 0x81]        | 3b 84 08 7f ff ff ff    |
    | cmp eax, dword [rax + 1 * rcx + 0xff]        | 3b 84 08 ff 00 00 00    |
    | cmp eax, dword [rax + 1 * rcx - 0xff]        | 3b 84 08 01 ff ff ff    |
    | cmp eax, dword [rax + 1 * rcx + 0x7fffffff]  | 3b 84 08 ff ff ff 7f    |
    | cmp eax, dword [rax + 1 * rcx - 0x7fffffff]  | 3b 84 08 01 00 00 80    |
    | cmp eax, dword [rax + 1 * rcx - 0x80000000]  | 3b 84 08 00 00 00 80    |
    | cmp eax, dword [r10 + 0x7f]                  | 41 3b 42 7f             |
    | cmp eax, dword [r10 + 0x80]                  | 41 3b 82 80 00 00 00    |
    | cmp eax, dword [r10 - 0x80]                  | 41 3b 42 80             |
    | cmp eax, dword [r10 - 0x81]                  | 41 3b 82 7f ff ff ff    |
    | cmp ecx, dword [rdx]                         | 3b 0a                   |
    | cmp edx, dword [rbx]                         | 3b 13                   |
    | cmp ebx, dword [rsp]                         | 3b 1c 24                |
    | cmp esp, dword [rbp]                         | 3b 65 00                |
    | cmp ebp, dword [rsi]                         | 3b 2e                   |
    | cmp esi, dword [rdi]                         | 3b 37                   |
    | cmp edi, dword [r8]                          | 41 3b 38                |
    | cmp r8d, dword [r9]                          | 45 3b 01                |
    | cmp r9d, dword [r10]                         | 45 3b 0a                |
    | cmp r10d, dword [r11]                        | 45 3b 13                |
    | cmp r11d, dword [r12]                        | 45 3b 1c 24             |
    | cmp r12d, dword [r13]                        | 45 3b 65 00             |
    | cmp r13d, dword [r14]                        | 45 3b 2e                |
    | cmp r14d, dword [r15]                        | 45 3b 37                |
    | cmp r15d, dword [rax + 1 * rcx]              | 44 3b 3c 08             |
    | cmp ecx, dword [rdx + 1 * rcx]               | 3b 0c 0a                |
    | cmp edx, dword [rbx + 1 * rcx]               | 3b 14 0b                |
    | cmp ebx, dword [rsp + 1 * rcx]               | 3b 1c 0c                |
    | cmp esp, dword [rbp + 1 * rcx]               | 3b 64 0d 00             |
    | cmp ebp, dword [rsi + 1 * rcx]               | 3b 2c 0e                |
    | cmp esi, dword [rdi + 1 * rcx]               | 3b 34 0f                |
    | cmp edi, dword [r8 + 1 * rcx]                | 41 3b 3c 08             |
    | cmp r8d, dword [r9 + 1 * rcx]                | 45 3b 04 09             |
    | cmp r9d, dword [r10 + 1 * rcx]               | 45 3b 0c 0a             |
    | cmp r10d, dword [r11 + 1 * rcx]              | 45 3b 14 0b             |
    | cmp r11d, dword [r12 + 1 * rcx]              | 45 3b 1c 0c             |
    | cmp r12d, dword [r13 + 1 * rcx]              | 45 3b 64 0d 00          |
    | cmp r13d, dword [r14 + 1 * rcx]              | 45 3b 2c 0e             |
    | cmp r14d, dword [r15 + 1 * rcx]              | 45 3b 34 0f             |
    | cmp r15d, dword [rax + 1 * rax]              | 44 3b 3c 00             |
    | cmp ecx, dword [rax + 1 * rbx]               | 3b 0c 18                |
    | cmp edx, dword [rax + 1 * rbp]               | 3b 14 28                |
    | cmp ebx, dword [rax + 1 * rsi]               | 3b 1c 30                |
    | cmp esp, dword [rax + 1 * rdi]               | 3b 24 38                |
    | cmp ebp, dword [rax + 1 * r8]                | 42 3b 2c 00             |
    | cmp esi, dword [rax + 1 * r9]                | 42 3b 34 08             |
    | cmp edi, dword [rax + 1 * r10]               | 42 3b 3c 10             |
    | cmp r8d, dword [rax + 1 * r11]               | 46 3b 04 18             |
    | cmp r9d, dword [rax + 1 * r12]               | 46 3b 0c 20             |
    | cmp r10d, dword [rax + 1 * r13]              | 46 3b 14 28             |
    | cmp r11d, dword [rax + 1 * r14]              | 46 3b 1c 30             |
    | cmp r12d, dword [rax + 1 * r15]              | 46 3b 24 38             |
    | cmp r13d, dword [rax + 2 * rcx]              | 44 3b 2c 48             |
    | cmp r14d, dword [rax + 4 * rcx]              | 44 3b 34 88             |
    | cmp r15d, dword [rax + 8 * rcx]              | 44 3b 3c c8             |
    | cmp ecx, dword [r8 + 2 * r9]                 | 43 3b 0c 48             |
    | cmp edx, dword [r8 + 4 * r9]                 | 43 3b 14 88             |
    | cmp ebx, dword [r8 + 8 * r9]                 | 43 3b 1c c8             |
    | cmp esp, dword [1 * rcx]                     | 3b 24 0d 00 00 00 00    |
    | cmp ebp, dword [2 * rcx]                     | 3b 2c 4d 00 00 00 00    |
    | cmp esi, dword [4 * rcx]                     | 3b 34 8d 00 00 00 00    |
    | cmp edi, dword [8 * rcx]                     | 3b 3c cd 00 00 00 00    |
    | cmp r8d, dword [1 * r9]                      | 46 3b 04 0d 00 00 00 00 |
    | cmp r9d, dword [2 * r9]                      | 46 3b 0c 4d 00 00 00 00 |
    | cmp r10d, dword [4 * r9]                     | 46 3b 14 8d 00 00 00 00 |
    | cmp r11d, dword [8 * r9]                     | 46 3b 1c cd 00 00 00 00 |
    | cmp r12d, dword [r13 + 8 * r12]              | 47 3b 64 e5 00          |
    | cmp r13d, dword [rsp + 4 * r15]              | 46 3b 2c bc             |
    | cmp r14d, dword [rax + 1 * rcx + 0x00]       | 44 3b 74 08 00          |
    | cmp r15d, dword [rax + 1 * rcx - 0x00]       | 44 3b 7c 08 00          |
    | cmp ecx, dword [rax + 1 * rcx - 0x01]        | 3b 4c 08 ff             |
    | cmp edx, dword [rax + 1 * rcx + 0x00000001]  | 3b 94 08 01 00 00 00    |
    | cmp ebx, dword [rax + 1 * rcx - 0x00000001]  | 3b 9c 08 ff ff ff ff    |
    | cmp esp, dword [rax + 1 * rcx + 0x7f]        | 3b 64 08 7f             |
    | cmp ebp, dword [rax + 1 * rcx - 0x7f]        | 3b 6c 08 81             |
    | cmp esi, dword [rax + 1 * rcx + 0x80]        | 3b b4 08 80 00 00 00    |
    | cmp edi, dword [rax + 1 * rcx - 0x80]        | 3b 7c 08 80             |
    | cmp r8d, dword [rax + 1 * rcx - 0x81]        | 44 3b 84 08 7f ff ff ff |
    | cmp r9d, dword [rax + 1 * rcx + 0xff]        | 44 3b 8c 08 ff 00 00 00 |
    | cmp r10d, dword [rax + 1 * rcx - 0xff]       | 44 3b 94 08 01 ff ff ff |
    | cmp r11d, dword [rax + 1 * rcx + 0x7fffffff] | 44 3b 9c 08 ff ff ff 7f |
    | cmp r12d, dword [rax + 1 * rcx - 0x7fffffff] | 44 3b a4 08 01 00 00 80 |
    | cmp r13d, dword [rax + 1 * rcx - 0x80000000] | 44 3b ac 08 00 00 00 80 |
    | cmp r14d, dword [r10 + 0x7f]                 | 45 3b 72 7f             |
    | cmp r15d, dword [r10 + 0x80]                 | 45 3b ba 80 00 00 00    |
    | cmp ecx, dword [r10 - 0x81]                  | 41 3b 8a 7f ff ff ff    |
    | cmp edx, dword [rax]                         | 3b 10                   |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_cmp_reg32_addr32():
    encode(CMP_REG32_ADDR32)


CMP_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | cmp ax, 0x01   | 66 83 f8 01    | *** | cmp ax, 0x00   | 66 83 f8 00    |
    | cmp cx, 0x01   | 66 83 f9 01    | *** | cmp ax, 0x7f   | 66 83 f8 7f    |
    | cmp dx, 0x01   | 66 83 fa 01    | *** | cmp ax, 0x80   | 66 83 f8 80    |
    | cmp bx, 0x01   | 66 83 fb 01    | *** | cmp ax, 0xff   | 66 83 f8 ff    |
    | cmp sp, 0x01   | 66 83 fc 01    | *** | cmp cx, 0x7f   | 66 83 f9 7f    |
    | cmp bp, 0x01   | 66 83 fd 01    | *** | cmp dx, 0x80   | 66 83 fa 80    |
    | cmp si, 0x01   | 66 83 fe 01    | *** | cmp bx, 0xff   | 66 83 fb ff    |
    | cmp di, 0x01   | 66 83 ff 01    | *** | cmp sp, 0x00   | 66 83 fc 00    |
    | cmp r8w, 0x01  | 66 41 83 f8 01 | *** | cmp si, 0x7f   | 66 83 fe 7f    |
    | cmp r9w, 0x01  | 66 41 83 f9 01 | *** | cmp di, 0x80   | 66 83 ff 80    |
    | cmp r10w, 0x01 | 66 41 83 fa 01 | *** | cmp r8w, 0xff  | 66 41 83 f8 ff |
    | cmp r11w, 0x01 | 66 41 83 fb 01 | *** | cmp r9w, 0x00  | 66 41 83 f9 00 |
    | cmp r12w, 0x01 | 66 41 83 fc 01 | *** | cmp r11w, 0x7f | 66 41 83 fb 7f |
    | cmp r13w, 0x01 | 66 41 83 fd 01 | *** | cmp r12w, 0x80 | 66 41 83 fc 80 |
    | cmp r14w, 0x01 | 66 41 83 fe 01 | *** | cmp r13w, 0xff | 66 41 83 fd ff |
    | cmp r15w, 0x01 | 66 41 83 ff 01 | *** | cmp r14w, 0x00 | 66 41 83 fe 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_cmp_reg16_imm8():
    encode(CMP_REG16_IMM8)


CMP_REG16_IMM16 = """
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | instruction      | encoding          | *** | instruction      | encoding          |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | cmp ax, 0x0001   | 66 3d 01 00       | *** | cmp ax, 0x00ff   | 66 3d ff 00       |
    | cmp cx, 0x0001   | 66 81 f9 01 00    | *** | cmp ax, 0x0100   | 66 3d 00 01       |
    | cmp dx, 0x0001   | 66 81 fa 01 00    | *** | cmp ax, 0x7fff   | 66 3d ff 7f       |
    | cmp bx, 0x0001   | 66 81 fb 01 00    | *** | cmp ax, 0x8000   | 66 3d 00 80       |
    | cmp sp, 0x0001   | 66 81 fc 01 00    | *** | cmp ax, 0xffff   | 66 3d ff ff       |
    | cmp bp, 0x0001   | 66 81 fd 01 00    | *** | cmp cx, 0x007f   | 66 81 f9 7f 00    |
    | cmp si, 0x0001   | 66 81 fe 01 00    | *** | cmp dx, 0x0080   | 66 81 fa 80 00    |
    | cmp di, 0x0001   | 66 81 ff 01 00    | *** | cmp bx, 0x00ff   | 66 81 fb ff 00    |
    | cmp r8w, 0x0001  | 66 41 81 f8 01 00 | *** | cmp sp, 0x0100   | 66 81 fc 00 01    |
    | cmp r9w, 0x0001  | 66 41 81 f9 01 00 | *** | cmp bp, 0x7fff   | 66 81 fd ff 7f    |
    | cmp r10w, 0x0001 | 66 41 81 fa 01 00 | *** | cmp si, 0x8000   | 66 81 fe 00 80    |
    | cmp r11w, 0x0001 | 66 41 81 fb 01 00 | *** | cmp di, 0xffff   | 66 81 ff ff ff    |
    | cmp r12w, 0x0001 | 66 41 81 fc 01 00 | *** | cmp r8w, 0x0000  | 66 41 81 f8 00 00 |
    | cmp r13w, 0x0001 | 66 41 81 fd 01 00 | *** | cmp r10w, 0x007f | 66 41 81 fa 7f 00 |
    | cmp r14w, 0x0001 | 66 41 81 fe 01 00 | *** | cmp r11w, 0x0080 | 66 41 81 fb 80 00 |
    | cmp r15w, 0x0001 | 66 41 81 ff 01 00 | *** | cmp r12w, 0x00ff | 66 41 81 fc ff 00 |
    | cmp ax, 0x0000   | 66 3d 00 00       | *** | cmp r13w, 0x0100 | 66 41 81 fd 00 01 |
    | cmp ax, 0x007f   | 66 3d 7f 00       | *** | cmp r14w, 0x7fff | 66 41 81 fe ff 7f |
    | cmp ax, 0x0080   | 66 3d 80 00       | *** | cmp r15w, 0x8000 | 66 41 81 ff 00 80 |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
"""


def can_encode_cmp_reg16_imm16():
    encode(CMP_REG16_IMM16)


CMP_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | cmp ax, cx     | 66 39 c8    | *** | cmp ax, r8w    | 66 44 39 c0 |
    | cmp cx, cx     | 66 39 c9    | *** | cmp ax, r9w    | 66 44 39 c8 |
    | cmp dx, cx     | 66 39 ca    | *** | cmp ax, r10w   | 66 44 39 d0 |
    | cmp bx, cx     | 66 39 cb    | *** | cmp ax, r11w   | 66 44 39 d8 |
    | cmp sp, cx     | 66 39 cc    | *** | cmp ax, r12w   | 66 44 39 e0 |
    | cmp bp, cx     | 66 39 cd    | *** | cmp ax, r13w   | 66 44 39 e8 |
    | cmp si, cx     | 66 39 ce    | *** | cmp ax, r14w   | 66 44 39 f0 |
    | cmp di, cx     | 66 39 cf    | *** | cmp ax, r15w   | 66 44 39 f8 |
    | cmp r8w, cx    | 66 41 39 c8 | *** | cmp cx, dx     | 66 39 d1    |
    | cmp r9w, cx    | 66 41 39 c9 | *** | cmp dx, bx     | 66 39 da    |
    | cmp r10w, cx   | 66 41 39 ca | *** | cmp bx, sp     | 66 39 e3    |
    | cmp r11w, cx   | 66 41 39 cb | *** | cmp sp, bp     | 66 39 ec    |
    | cmp r12w, cx   | 66 41 39 cc | *** | cmp bp, si     | 66 39 f5    |
    | cmp r13w, cx   | 66 41 39 cd | *** | cmp si, di     | 66 39 fe    |
    | cmp r14w, cx   | 66 41 39 ce | *** | cmp di, r8w    | 66 44 39 c7 |
    | cmp r15w, cx   | 66 41 39 cf | *** | cmp r8w, r9w   | 66 45 39 c8 |
    | cmp ax, ax     | 66 39 c0    | *** | cmp r9w, r10w  | 66 45 39 d1 |
    | cmp ax, dx     | 66 39 d0    | *** | cmp r10w, r11w | 66 45 39 da |
    | cmp ax, bx     | 66 39 d8    | *** | cmp r11w, r12w | 66 45 39 e3 |
    | cmp ax, sp     | 66 39 e0    | *** | cmp r12w, r13w | 66 45 39 ec |
    | cmp ax, bp     | 66 39 e8    | *** | cmp r13w, r14w | 66 45 39 f5 |
    | cmp ax, si     | 66 39 f0    | *** | cmp r14w, r15w | 66 45 39 fe |
    | cmp ax, di     | 66 39 f8    | *** | cmp r15w, ax   | 66 41 39 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_cmp_reg16_reg16():
    encode(CMP_REG16_REG16)


CMP_REG16_ADDR16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | cmp ax, word [rcx]                          | 66 3b 01                   |
    | cmp cx, word [rcx]                          | 66 3b 09                   |
    | cmp dx, word [rcx]                          | 66 3b 11                   |
    | cmp bx, word [rcx]                          | 66 3b 19                   |
    | cmp sp, word [rcx]                          | 66 3b 21                   |
    | cmp bp, word [rcx]                          | 66 3b 29                   |
    | cmp si, word [rcx]                          | 66 3b 31                   |
    | cmp di, word [rcx]                          | 66 3b 39                   |
    | cmp r8w, word [rcx]                         | 66 44 3b 01                |
    | cmp r9w, word [rcx]                         | 66 44 3b 09                |
    | cmp r10w, word [rcx]                        | 66 44 3b 11                |
    | cmp r11w, word [rcx]                        | 66 44 3b 19                |
    | cmp r12w, word [rcx]                        | 66 44 3b 21                |
    | cmp r13w, word [rcx]                        | 66 44 3b 29                |
    | cmp r14w, word [rcx]                        | 66 44 3b 31                |
    | cmp r15w, word [rcx]                        | 66 44 3b 39                |
    | cmp ax, word [rax]                          | 66 3b 00                   |
    | cmp ax, word [rdx]                          | 66 3b 02                   |
    | cmp ax, word [rbx]                          | 66 3b 03                   |
    | cmp ax, word [rsp]                          | 66 3b 04 24                |
    | cmp ax, word [rbp]                          | 66 3b 45 00                |
    | cmp ax, word [rsi]                          | 66 3b 06                   |
    | cmp ax, word [rdi]                          | 66 3b 07                   |
    | cmp ax, word [r8]                           | 66 41 3b 00                |
    | cmp ax, word [r9]                           | 66 41 3b 01                |
    | cmp ax, word [r10]                          | 66 41 3b 02                |
    | cmp ax, word [r11]                          | 66 41 3b 03                |
    | cmp ax, word [r12]                          | 66 41 3b 04 24             |
    | cmp ax, word [r13]                          | 66 41 3b 45 00             |
    | cmp ax, word [r14]                          | 66 41 3b 06                |
    | cmp ax, word [r15]                          | 66 41 3b 07                |
    | cmp ax, word [rax + 1 * rcx]                | 66 3b 04 08                |
    | cmp ax, word [rcx + 1 * rcx]                | 66 3b 04 09                |
    | cmp ax, word [rdx + 1 * rcx]                | 66 3b 04 0a                |
    | cmp ax, word [rbx + 1 * rcx]                | 66 3b 04 0b                |
    | cmp ax, word [rsp + 1 * rcx]                | 66 3b 04 0c                |
    | cmp ax, word [rbp + 1 * rcx]                | 66 3b 44 0d 00             |
    | cmp ax, word [rsi + 1 * rcx]                | 66 3b 04 0e                |
    | cmp ax, word [rdi + 1 * rcx]                | 66 3b 04 0f                |
    | cmp ax, word [r8 + 1 * rcx]                 | 66 41 3b 04 08             |
    | cmp ax, word [r9 + 1 * rcx]                 | 66 41 3b 04 09             |
    | cmp ax, word [r10 + 1 * rcx]                | 66 41 3b 04 0a             |
    | cmp ax, word [r11 + 1 * rcx]                | 66 41 3b 04 0b             |
    | cmp ax, word [r12 + 1 * rcx]                | 66 41 3b 04 0c             |
    | cmp ax, word [r13 + 1 * rcx]                | 66 41 3b 44 0d 00          |
    | cmp ax, word [r14 + 1 * rcx]                | 66 41 3b 04 0e             |
    | cmp ax, word [r15 + 1 * rcx]                | 66 41 3b 04 0f             |
    | cmp ax, word [rax + 1 * rax]                | 66 3b 04 00                |
    | cmp ax, word [rax + 1 * rdx]                | 66 3b 04 10                |
    | cmp ax, word [rax + 1 * rbx]                | 66 3b 04 18                |
    | cmp ax, word [rax + 1 * rbp]                | 66 3b 04 28                |
    | cmp ax, word [rax + 1 * rsi]                | 66 3b 04 30                |
    | cmp ax, word [rax + 1 * rdi]                | 66 3b 04 38                |
    | cmp ax, word [rax + 1 * r8]                 | 66 42 3b 04 00             |
    | cmp ax, word [rax + 1 * r9]                 | 66 42 3b 04 08             |
    | cmp ax, word [rax + 1 * r10]                | 66 42 3b 04 10             |
    | cmp ax, word [rax + 1 * r11]                | 66 42 3b 04 18             |
    | cmp ax, word [rax + 1 * r12]                | 66 42 3b 04 20             |
    | cmp ax, word [rax + 1 * r13]                | 66 42 3b 04 28             |
    | cmp ax, word [rax + 1 * r14]                | 66 42 3b 04 30             |
    | cmp ax, word [rax + 1 * r15]                | 66 42 3b 04 38             |
    | cmp ax, word [rax + 2 * rcx]                | 66 3b 04 48                |
    | cmp ax, word [rax + 4 * rcx]                | 66 3b 04 88                |
    | cmp ax, word [rax + 8 * rcx]                | 66 3b 04 c8                |
    | cmp ax, word [r8 + 1 * r9]                  | 66 43 3b 04 08             |
    | cmp ax, word [r8 + 2 * r9]                  | 66 43 3b 04 48             |
    | cmp ax, word [r8 + 4 * r9]                  | 66 43 3b 04 88             |
    | cmp ax, word [r8 + 8 * r9]                  | 66 43 3b 04 c8             |
    | cmp ax, word [1 * rcx]                      | 66 3b 04 0d 00 00 00 00    |
    | cmp ax, word [2 * rcx]                      | 66 3b 04 4d 00 00 00 00    |
    | cmp ax, word [4 * rcx]                      | 66 3b 04 8d 00 00 00 00    |
    | cmp ax, word [8 * rcx]                      | 66 3b 04 cd 00 00 00 00    |
    | cmp ax, word [1 * r9]                       | 66 42 3b 04 0d 00 00 00 00 |
    | cmp ax, word [2 * r9]                       | 66 42 3b 04 4d 00 00 00 00 |
    | cmp ax, word [4 * r9]                       | 66 42 3b 04 8d 00 00 00 00 |
    | cmp ax, word [8 * r9]                       | 66 42 3b 04 cd 00 00 00 00 |
    | cmp ax, word [r13 + 8 * r12]                | 66 43 3b 44 e5 00          |
    | cmp ax, word [rsp + 4 * r15]                | 66 42 3b 04 bc             |
    | cmp ax, word [rax + 1 * rcx + 0x00]         | 66 3b 44 08 00             |
    | cmp ax, word [rax + 1 * rcx - 0x00]         | 66 3b 44 08 00             |
    | cmp ax, word [rax + 1 * rcx + 0x01]         | 66 3b 44 08 01             |
    | cmp ax, word [rax + 1 * rcx - 0x01]         | 66 3b 44 08 ff             |
    | cmp ax, word [rax + 1 * rcx + 0x00000001]   | 66 3b 84 08 01 00 00 00    |
    | cmp ax, word [rax + 1 * rcx - 0x00000001]   | 66 3b 84 08 ff ff ff ff    |
    | cmp ax, word [rax + 1 * rcx + 0x7f]         | 66 3b 44 08 7f             |
    | cmp ax, word [rax + 1 * rcx - 0x7f]         | 66 3b 44 08 81             |
    | cmp ax, word [rax + 1 * rcx + 0x80]         | 66 3b 84 08 80 00 00 00    |
    | cmp ax, word [rax + 1 * rcx - 0x80]         | 66 3b 44 08 80             |
    | cmp ax, word [rax + 1 * rcx - 0x81]         | 66 3b 84 08 7f ff ff ff    |
    | cmp ax, word [rax + 1 * rcx + 0xff]         | 66 3b 84 08 ff 00 00 00    |
    | cmp ax, word [rax + 1 * rcx - 0xff]         | 66 3b 84 08 01 ff ff ff    |
    | cmp ax, word [rax + 1 * rcx + 0x7fffffff]   | 66 3b 84 08 ff ff ff 7f    |
    | cmp ax, word [rax + 1 * rcx - 0x7fffffff]   | 66 3b 84 08 01 00 00 80    |
    | cmp ax, word [rax + 1 * rcx - 0x80000000]   | 66 3b 84 08 00 00 00 80    |
    | cmp ax, word [r10 + 0x7f]                   | 66 41 3b 42 7f             |
    | cmp ax, word [r10 + 0x80]                   | 66 41 3b 82 80 00 00 00    |
    | cmp ax, word [r10 - 0x80]                   | 66 41 3b 42 80             |
    | cmp ax, word [r10 - 0x81]                   | 66 41 3b 82 7f ff ff ff    |
    | cmp cx, word [rdx]                          | 66 3b 0a                   |
    | cmp dx, word [rbx]                          | 66 3b 13                   |
    | cmp bx, word [rsp]                          | 66 3b 1c 24                |
    | cmp sp, word [rbp]                          | 66 3b 65 00                |
    | cmp bp, word [rsi]                          | 66 3b 2e                   |
    | cmp si, word [rdi]                          | 66 3b 37                   |
    | cmp di, word [r8]                           | 66 41 3b 38                |
    | cmp r8w, word [r9]                          | 66 45 3b 01                |
    | cmp r9w, word [r10]                         | 66 45 3b 0a                |
    | cmp r10w, word [r11]                        | 66 45 3b 13                |
    | cmp r11w, word [r12]                        | 66 45 3b 1c 24             |
    | cmp r12w, word [r13]                        | 66 45 3b 65 00             |
    | cmp r13w, word [r14]                        | 66 45 3b 2e                |
    | cmp r14w, word [r15]                        | 66 45 3b 37                |
    | cmp r15w, word [rax + 1 * rcx]              | 66 44 3b 3c 08             |
    | cmp cx, word [rdx + 1 * rcx]                | 66 3b 0c 0a                |
    | cmp dx, word [rbx + 1 * rcx]                | 66 3b 14 0b                |
    | cmp bx, word [rsp + 1 * rcx]                | 66 3b 1c 0c                |
    | cmp sp, word [rbp + 1 * rcx]                | 66 3b 64 0d 00             |
    | cmp bp, word [rsi + 1 * rcx]                | 66 3b 2c 0e                |
    | cmp si, word [rdi + 1 * rcx]                | 66 3b 34 0f                |
    | cmp di, word [r8 + 1 * rcx]                 | 66 41 3b 3c 08             |
    | cmp r8w, word [r9 + 1 * rcx]                | 66 45 3b 04 09             |
    | cmp r9w, word [r10 + 1 * rcx]               | 66 45 3b 0c 0a             |
    | cmp r10w, word [r11 + 1 * rcx]              | 66 45 3b 14 0b             |
    | cmp r11w, word [r12 + 1 * rcx]              | 66 45 3b 1c 0c             |
    | cmp r12w, word [r13 + 1 * rcx]              | 66 45 3b 64 0d 00          |
    | cmp r13w, word [r14 + 1 * rcx]              | 66 45 3b 2c 0e             |
    | cmp r14w, word [r15 + 1 * rcx]              | 66 45 3b 34 0f             |
    | cmp r15w, word [rax + 1 * rax]              | 66 44 3b 3c 00             |
    | cmp cx, word [rax + 1 * rbx]                | 66 3b 0c 18                |
    | cmp dx, word [rax + 1 * rbp]                | 66 3b 14 28                |
    | cmp bx, word [rax + 1 * rsi]                | 66 3b 1c 30                |
    | cmp sp, word [rax + 1 * rdi]                | 66 3b 24 38                |
    | cmp bp, word [rax + 1 * r8]                 | 66 42 3b 2c 00             |
    | cmp si, word [rax + 1 * r9]                 | 66 42 3b 34 08             |
    | cmp di, word [rax + 1 * r10]                | 66 42 3b 3c 10             |
    | cmp r8w, word [rax + 1 * r11]               | 66 46 3b 04 18             |
    | cmp r9w, word [rax + 1 * r12]               | 66 46 3b 0c 20             |
    | cmp r10w, word [rax + 1 * r13]              | 66 46 3b 14 28             |
    | cmp r11w, word [rax + 1 * r14]              | 66 46 3b 1c 30             |
    | cmp r12w, word [rax + 1 * r15]              | 66 46 3b 24 38             |
    | cmp r13w, word [rax + 2 * rcx]              | 66 44 3b 2c 48             |
    | cmp r14w, word [rax + 4 * rcx]              | 66 44 3b 34 88             |
    | cmp r15w, word [rax + 8 * rcx]              | 66 44 3b 3c c8             |
    | cmp cx, word [r8 + 2 * r9]                  | 66 43 3b 0c 48             |
    | cmp dx, word [r8 + 4 * r9]                  | 66 43 3b 14 88             |
    | cmp bx, word [r8 + 8 * r9]                  | 66 43 3b 1c c8             |
    | cmp sp, word [1 * rcx]                      | 66 3b 24 0d 00 00 00 00    |
    | cmp bp, word [2 * rcx]                      | 66 3b 2c 4d 00 00 00 00    |
    | cmp si, word [4 * rcx]                      | 66 3b 34 8d 00 00 00 00    |
    | cmp di, word [8 * rcx]                      | 66 3b 3c cd 00 00 00 00    |
    | cmp r8w, word [1 * r9]                      | 66 46 3b 04 0d 00 00 00 00 |
    | cmp r9w, word [2 * r9]                      | 66 46 3b 0c 4d 00 00 00 00 |
    | cmp r10w, word [4 * r9]                     | 66 46 3b 14 8d 00 00 00 00 |
    | cmp r11w, word [8 * r9]                     | 66 46 3b 1c cd 00 00 00 00 |
    | cmp r12w, word [r13 + 8 * r12]              | 66 47 3b 64 e5 00          |
    | cmp r13w, word [rsp + 4 * r15]              | 66 46 3b 2c bc             |
    | cmp r14w, word [rax + 1 * rcx + 0x00]       | 66 44 3b 74 08 00          |
    | cmp r15w, word [rax + 1 * rcx - 0x00]       | 66 44 3b 7c 08 00          |
    | cmp cx, word [rax + 1 * rcx - 0x01]         | 66 3b 4c 08 ff             |
    | cmp dx, word [rax + 1 * rcx + 0x00000001]   | 66 3b 94 08 01 00 00 00    |
    | cmp bx, word [rax + 1 * rcx - 0x00000001]   | 66 3b 9c 08 ff ff ff ff    |
    | cmp sp, word [rax + 1 * rcx + 0x7f]         | 66 3b 64 08 7f             |
    | cmp bp, word [rax + 1 * rcx - 0x7f]         | 66 3b 6c 08 81             |
    | cmp si, word [rax + 1 * rcx + 0x80]         | 66 3b b4 08 80 00 00 00    |
    | cmp di, word [rax + 1 * rcx - 0x80]         | 66 3b 7c 08 80             |
    | cmp r8w, word [rax + 1 * rcx - 0x81]        | 66 44 3b 84 08 7f ff ff ff |
    | cmp r9w, word [rax + 1 * rcx + 0xff]        | 66 44 3b 8c 08 ff 00 00 00 |
    | cmp r10w, word [rax + 1 * rcx - 0xff]       | 66 44 3b 94 08 01 ff ff ff |
    | cmp r11w, word [rax + 1 * rcx + 0x7fffffff] | 66 44 3b 9c 08 ff ff ff 7f |
    | cmp r12w, word [rax + 1 * rcx - 0x7fffffff] | 66 44 3b a4 08 01 00 00 80 |
    | cmp r13w, word [rax + 1 * rcx - 0x80000000] | 66 44 3b ac 08 00 00 00 80 |
    | cmp r14w, word [r10 + 0x7f]                 | 66 45 3b 72 7f             |
    | cmp r15w, word [r10 + 0x80]                 | 66 45 3b ba 80 00 00 00    |
    | cmp cx, word [r10 - 0x81]                   | 66 41 3b 8a 7f ff ff ff    |
    | cmp dx, word [rax]                          | 66 3b 10                   |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_cmp_reg16_addr16():
    encode(CMP_REG16_ADDR16)


CMP_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | cmp al, 0x01   | 3c 01       | *** | cmp al, 0x00   | 3c 00       |
    | cmp cl, 0x01   | 80 f9 01    | *** | cmp al, 0x7f   | 3c 7f       |
    | cmp dl, 0x01   | 80 fa 01    | *** | cmp al, 0x80   | 3c 80       |
    | cmp bl, 0x01   | 80 fb 01    | *** | cmp al, 0xff   | 3c ff       |
    | cmp spl, 0x01  | 40 80 fc 01 | *** | cmp cl, 0x7f   | 80 f9 7f    |
    | cmp bpl, 0x01  | 40 80 fd 01 | *** | cmp dl, 0x80   | 80 fa 80    |
    | cmp sil, 0x01  | 40 80 fe 01 | *** | cmp bl, 0xff   | 80 fb ff    |
    | cmp dil, 0x01  | 40 80 ff 01 | *** | cmp spl, 0x00  | 40 80 fc 00 |
    | cmp r8b, 0x01  | 41 80 f8 01 | *** | cmp sil, 0x7f  | 40 80 fe 7f |
    | cmp r9b, 0x01  | 41 80 f9 01 | *** | cmp dil, 0x80  | 40 80 ff 80 |
    | cmp r10b, 0x01 | 41 80 fa 01 | *** | cmp r8b, 0xff  | 41 80 f8 ff |
    | cmp r11b, 0x01 | 41 80 fb 01 | *** | cmp r9b, 0x00  | 41 80 f9 00 |
    | cmp r12b, 0x01 | 41 80 fc 01 | *** | cmp r11b, 0x7f | 41 80 fb 7f |
    | cmp r13b, 0x01 | 41 80 fd 01 | *** | cmp r12b, 0x80 | 41 80 fc 80 |
    | cmp r14b, 0x01 | 41 80 fe 01 | *** | cmp r13b, 0xff | 41 80 fd ff |
    | cmp r15b, 0x01 | 41 80 ff 01 | *** | cmp r14b, 0x00 | 41 80 fe 00 |
    | cmp ah, 0x01   | 80 fc 01    | *** | cmp ah, 0x7f   | 80 fc 7f    |
    | cmp ch, 0x01   | 80 fd 01    | *** | cmp ch, 0x80   | 80 fd 80    |
    | cmp dh, 0x01   | 80 fe 01    | *** | cmp dh, 0xff   | 80 fe ff    |
    | cmp bh, 0x01   | 80 ff 01    | *** | cmp bh, 0x00   | 80 ff 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_cmp_reg8_imm8():
    encode(CMP_REG8_IMM8)


CMP_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | cmp al, cl     | 38 c8    | *** | cmp al, r10b   | 44 38 d0 |
    | cmp cl, cl     | 38 c9    | *** | cmp al, r11b   | 44 38 d8 |
    | cmp dl, cl     | 38 ca    | *** | cmp al, r12b   | 44 38 e0 |
    | cmp bl, cl     | 38 cb    | *** | cmp al, r13b   | 44 38 e8 |
    | cmp spl, cl    | 40 38 cc | *** | cmp al, r14b   | 44 38 f0 |
    | cmp bpl, cl    | 40 38 cd | *** | cmp al, r15b   | 44 38 f8 |
    | cmp sil, cl    | 40 38 ce | *** | cmp al, ah     | 38 e0    |
    | cmp dil, cl    | 40 38 cf | *** | cmp al, ch     | 38 e8    |
    | cmp r8b, cl    | 41 38 c8 | *** | cmp al, dh     | 38 f0    |
    | cmp r9b, cl    | 41 38 c9 | *** | cmp al, bh     | 38 f8    |
    | cmp r10b, cl   | 41 38 ca | *** | cmp cl, dl     | 38 d1    |
    | cmp r11b, cl   | 41 38 cb | *** | cmp dl, bl     | 38 da    |
    | cmp r12b, cl   | 41 38 cc | *** | cmp bl, spl    | 40 38 e3 |
    | cmp r13b, cl   | 41 38 cd | *** | cmp spl, bpl   | 40 38 ec |
    | cmp r14b, cl   | 41 38 ce | *** | cmp bpl, sil   | 40 38 f5 |
    | cmp r15b, cl   | 41 38 cf | *** | cmp sil, dil   | 40 38 fe |
    | cmp ah, cl     | 38 cc    | *** | cmp dil, r8b   | 44 38 c7 |
    | cmp ch, cl     | 38 cd    | *** | cmp r8b, r9b   | 45 38 c8 |
    | cmp dh, cl     | 38 ce    | *** | cmp r9b, r10b  | 45 38 d1 |
    | cmp bh, cl     | 38 cf    | *** | cmp r10b, r11b | 45 38 da |
    | cmp al, al     | 38 c0    | *** | cmp r11b, r12b | 45 38 e3 |
    | cmp al, dl     | 38 d0    | *** | cmp r12b, r13b | 45 38 ec |
    | cmp al, bl     | 38 d8    | *** | cmp r13b, r14b | 45 38 f5 |
    | cmp al, spl    | 40 38 e0 | *** | cmp r14b, r15b | 45 38 fe |
    | cmp al, bpl    | 40 38 e8 | *** | cmp r15b, ah   | !! !! !! |
    | cmp al, sil    | 40 38 f0 | *** | cmp ah, ch     | 38 ec    |
    | cmp al, dil    | 40 38 f8 | *** | cmp ch, dh     | 38 f5    |
    | cmp al, r8b    | 44 38 c0 | *** | cmp dh, bh     | 38 fe    |
    | cmp al, r9b    | 44 38 c8 | *** | cmp bh, al     | 38 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_cmp_reg8_reg8():
    encode(CMP_REG8_REG8)


CMP_REG8_ADDR8 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | cmp al, byte [rcx]                          | 3a 01                   |
    | cmp cl, byte [rcx]                          | 3a 09                   |
    | cmp dl, byte [rcx]                          | 3a 11                   |
    | cmp bl, byte [rcx]                          | 3a 19                   |
    | cmp spl, byte [rcx]                         | 40 3a 21                |
    | cmp bpl, byte [rcx]                         | 40 3a 29                |
    | cmp sil, byte [rcx]                         | 40 3a 31                |
    | cmp dil, byte [rcx]                         | 40 3a 39                |
    | cmp r8b, byte [rcx]                         | 44 3a 01                |
    | cmp r9b, byte [rcx]                         | 44 3a 09                |
    | cmp r10b, byte [rcx]                        | 44 3a 11                |
    | cmp r11b, byte [rcx]                        | 44 3a 19                |
    | cmp r12b, byte [rcx]                        | 44 3a 21                |
    | cmp r13b, byte [rcx]                        | 44 3a 29                |
    | cmp r14b, byte [rcx]                        | 44 3a 31                |
    | cmp r15b, byte [rcx]                        | 44 3a 39                |
    | cmp ah, byte [rcx]                          | 3a 21                   |
    | cmp ch, byte [rcx]                          | 3a 29                   |
    | cmp dh, byte [rcx]                          | 3a 31                   |
    | cmp bh, byte [rcx]                          | 3a 39                   |
    | cmp al, byte [rax]                          | 3a 00                   |
    | cmp al, byte [rdx]                          | 3a 02                   |
    | cmp al, byte [rbx]                          | 3a 03                   |
    | cmp al, byte [rsp]                          | 3a 04 24                |
    | cmp al, byte [rbp]                          | 3a 45 00                |
    | cmp al, byte [rsi]                          | 3a 06                   |
    | cmp al, byte [rdi]                          | 3a 07                   |
    | cmp al, byte [r8]                           | 41 3a 00                |
    | cmp al, byte [r9]                           | 41 3a 01                |
    | cmp al, byte [r10]                          | 41 3a 02                |
    | cmp al, byte [r11]                          | 41 3a 03                |
    | cmp al, byte [r12]                          | 41 3a 04 24             |
    | cmp al, byte [r13]                          | 41 3a 45 00             |
    | cmp al, byte [r14]                          | 41 3a 06                |
    | cmp al, byte [r15]                          | 41 3a 07                |
    | cmp al, byte [rax + 1 * rcx]                | 3a 04 08                |
    | cmp al, byte [rcx + 1 * rcx]                | 3a 04 09                |
    | cmp al, byte [rdx + 1 * rcx]                | 3a 04 0a                |
    | cmp al, byte [rbx + 1 * rcx]                | 3a 04 0b                |
    | cmp al, byte [rsp + 1 * rcx]                | 3a 04 0c                |
    | cmp al, byte [rbp + 1 * rcx]                | 3a 44 0d 00             |
    | cmp al, byte [rsi + 1 * rcx]                | 3a 04 0e                |
    | cmp al, byte [rdi + 1 * rcx]                | 3a 04 0f                |
    | cmp al, byte [r8 + 1 * rcx]                 | 41 3a 04 08             |
    | cmp al, byte [r9 + 1 * rcx]                 | 41 3a 04 09             |
    | cmp al, byte [r10 + 1 * rcx]                | 41 3a 04 0a             |
    | cmp al, byte [r11 + 1 * rcx]                | 41 3a 04 0b             |
    | cmp al, byte [r12 + 1 * rcx]                | 41 3a 04 0c             |
    | cmp al, byte [r13 + 1 * rcx]                | 41 3a 44 0d 00          |
    | cmp al, byte [r14 + 1 * rcx]                | 41 3a 04 0e             |
    | cmp al, byte [r15 + 1 * rcx]                | 41 3a 04 0f             |
    | cmp al, byte [rax + 1 * rax]                | 3a 04 00                |
    | cmp al, byte [rax + 1 * rdx]                | 3a 04 10                |
    | cmp al, byte [rax + 1 * rbx]                | 3a 04 18                |
    | cmp al, byte [rax + 1 * rbp]                | 3a 04 28                |
    | cmp al, byte [rax + 1 * rsi]                | 3a 04 30                |
    | cmp al, byte [rax + 1 * rdi]                | 3a 04 38                |
    | cmp al, byte [rax + 1 * r8]                 | 42 3a 04 00             |
    | cmp al, byte [rax + 1 * r9]                 | 42 3a 04 08             |
    | cmp al, byte [rax + 1 * r10]                | 42 3a 04 10             |
    | cmp al, byte [rax + 1 * r11]                | 42 3a 04 18             |
    | cmp al, byte [rax + 1 * r12]                | 42 3a 04 20             |
    | cmp al, byte [rax + 1 * r13]                | 42 3a 04 28             |
    | cmp al, byte [rax + 1 * r14]                | 42 3a 04 30             |
    | cmp al, byte [rax + 1 * r15]                | 42 3a 04 38             |
    | cmp al, byte [rax + 2 * rcx]                | 3a 04 48                |
    | cmp al, byte [rax + 4 * rcx]                | 3a 04 88                |
    | cmp al, byte [rax + 8 * rcx]                | 3a 04 c8                |
    | cmp al, byte [r8 + 1 * r9]                  | 43 3a 04 08             |
    | cmp al, byte [r8 + 2 * r9]                  | 43 3a 04 48             |
    | cmp al, byte [r8 + 4 * r9]                  | 43 3a 04 88             |
    | cmp al, byte [r8 + 8 * r9]                  | 43 3a 04 c8             |
    | cmp al, byte [1 * rcx]                      | 3a 04 0d 00 00 00 00    |
    | cmp al, byte [2 * rcx]                      | 3a 04 4d 00 00 00 00    |
    | cmp al, byte [4 * rcx]                      | 3a 04 8d 00 00 00 00    |
    | cmp al, byte [8 * rcx]                      | 3a 04 cd 00 00 00 00    |
    | cmp al, byte [1 * r9]                       | 42 3a 04 0d 00 00 00 00 |
    | cmp al, byte [2 * r9]                       | 42 3a 04 4d 00 00 00 00 |
    | cmp al, byte [4 * r9]                       | 42 3a 04 8d 00 00 00 00 |
    | cmp al, byte [8 * r9]                       | 42 3a 04 cd 00 00 00 00 |
    | cmp al, byte [r13 + 8 * r12]                | 43 3a 44 e5 00          |
    | cmp al, byte [rsp + 4 * r15]                | 42 3a 04 bc             |
    | cmp al, byte [rax + 1 * rcx + 0x00]         | 3a 44 08 00             |
    | cmp al, byte [rax + 1 * rcx - 0x00]         | 3a 44 08 00             |
    | cmp al, byte [rax + 1 * rcx + 0x01]         | 3a 44 08 01             |
    | cmp al, byte [rax + 1 * rcx - 0x01]         | 3a 44 08 ff             |
    | cmp al, byte [rax + 1 * rcx + 0x00000001]   | 3a 84 08 01 00 00 00    |
    | cmp al, byte [rax + 1 * rcx - 0x00000001]   | 3a 84 08 ff ff ff ff    |
    | cmp al, byte [rax + 1 * rcx + 0x7f]         | 3a 44 08 7f             |
    | cmp al, byte [rax + 1 * rcx - 0x7f]         | 3a 44 08 81             |
    | cmp al, byte [rax + 1 * rcx + 0x80]         | 3a 84 08 80 00 00 00    |
    | cmp al, byte [rax + 1 * rcx - 0x80]         | 3a 44 08 80             |
    | cmp al, byte [rax + 1 * rcx - 0x81]         | 3a 84 08 7f ff ff ff    |
    | cmp al, byte [rax + 1 * rcx + 0xff]         | 3a 84 08 ff 00 00 00    |
    | cmp al, byte [rax + 1 * rcx - 0xff]         | 3a 84 08 01 ff ff ff    |
    | cmp al, byte [rax + 1 * rcx + 0x7fffffff]   | 3a 84 08 ff ff ff 7f    |
    | cmp al, byte [rax + 1 * rcx - 0x7fffffff]   | 3a 84 08 01 00 00 80    |
    | cmp al, byte [rax + 1 * rcx - 0x80000000]   | 3a 84 08 00 00 00 80    |
    | cmp al, byte [r10 + 0x7f]                   | 41 3a 42 7f             |
    | cmp al, byte [r10 + 0x80]                   | 41 3a 82 80 00 00 00    |
    | cmp al, byte [r10 - 0x80]                   | 41 3a 42 80             |
    | cmp al, byte [r10 - 0x81]                   | 41 3a 82 7f ff ff ff    |
    | cmp cl, byte [rdx]                          | 3a 0a                   |
    | cmp dl, byte [rbx]                          | 3a 13                   |
    | cmp bl, byte [rsp]                          | 3a 1c 24                |
    | cmp spl, byte [rbp]                         | 40 3a 65 00             |
    | cmp bpl, byte [rsi]                         | 40 3a 2e                |
    | cmp sil, byte [rdi]                         | 40 3a 37                |
    | cmp dil, byte [r8]                          | 41 3a 38                |
    | cmp r8b, byte [r9]                          | 45 3a 01                |
    | cmp r9b, byte [r10]                         | 45 3a 0a                |
    | cmp r10b, byte [r11]                        | 45 3a 13                |
    | cmp r11b, byte [r12]                        | 45 3a 1c 24             |
    | cmp r12b, byte [r13]                        | 45 3a 65 00             |
    | cmp r13b, byte [r14]                        | 45 3a 2e                |
    | cmp r14b, byte [r15]                        | 45 3a 37                |
    | cmp r15b, byte [rax + 1 * rcx]              | 44 3a 3c 08             |
    | cmp ah, byte [rcx + 1 * rcx]                | 3a 24 09                |
    | cmp ch, byte [rdx + 1 * rcx]                | 3a 2c 0a                |
    | cmp dh, byte [rbx + 1 * rcx]                | 3a 34 0b                |
    | cmp bh, byte [rsp + 1 * rcx]                | 3a 3c 0c                |
    | cmp cl, byte [rsi + 1 * rcx]                | 3a 0c 0e                |
    | cmp dl, byte [rdi + 1 * rcx]                | 3a 14 0f                |
    | cmp bl, byte [r8 + 1 * rcx]                 | 41 3a 1c 08             |
    | cmp spl, byte [r9 + 1 * rcx]                | 41 3a 24 09             |
    | cmp bpl, byte [r10 + 1 * rcx]               | 41 3a 2c 0a             |
    | cmp sil, byte [r11 + 1 * rcx]               | 41 3a 34 0b             |
    | cmp dil, byte [r12 + 1 * rcx]               | 41 3a 3c 0c             |
    | cmp r8b, byte [r13 + 1 * rcx]               | 45 3a 44 0d 00          |
    | cmp r9b, byte [r14 + 1 * rcx]               | 45 3a 0c 0e             |
    | cmp r10b, byte [r15 + 1 * rcx]              | 45 3a 14 0f             |
    | cmp r11b, byte [rax + 1 * rax]              | 44 3a 1c 00             |
    | cmp r12b, byte [rax + 1 * rdx]              | 44 3a 24 10             |
    | cmp r13b, byte [rax + 1 * rbx]              | 44 3a 2c 18             |
    | cmp r14b, byte [rax + 1 * rbp]              | 44 3a 34 28             |
    | cmp r15b, byte [rax + 1 * rsi]              | 44 3a 3c 30             |
    | cmp ah, byte [rax + 1 * rdi]                | 3a 24 38                |
    | cmp ch, byte [rax + 1 * r8]                 | !! !! !!                |
    | cmp dh, byte [rax + 1 * r9]                 | !! !! !!                |
    | cmp bh, byte [rax + 1 * r10]                | !! !! !!                |
    | cmp cl, byte [rax + 1 * r12]                | 42 3a 0c 20             |
    | cmp dl, byte [rax + 1 * r13]                | 42 3a 14 28             |
    | cmp bl, byte [rax + 1 * r14]                | 42 3a 1c 30             |
    | cmp spl, byte [rax + 1 * r15]               | 42 3a 24 38             |
    | cmp bpl, byte [rax + 2 * rcx]               | 40 3a 2c 48             |
    | cmp sil, byte [rax + 4 * rcx]               | 40 3a 34 88             |
    | cmp dil, byte [rax + 8 * rcx]               | 40 3a 3c c8             |
    | cmp r8b, byte [r8 + 1 * r9]                 | 47 3a 04 08             |
    | cmp r9b, byte [r8 + 2 * r9]                 | 47 3a 0c 48             |
    | cmp r10b, byte [r8 + 4 * r9]                | 47 3a 14 88             |
    | cmp r11b, byte [r8 + 8 * r9]                | 47 3a 1c c8             |
    | cmp r12b, byte [1 * rcx]                    | 44 3a 24 0d 00 00 00 00 |
    | cmp r13b, byte [2 * rcx]                    | 44 3a 2c 4d 00 00 00 00 |
    | cmp r14b, byte [4 * rcx]                    | 44 3a 34 8d 00 00 00 00 |
    | cmp r15b, byte [8 * rcx]                    | 44 3a 3c cd 00 00 00 00 |
    | cmp ah, byte [1 * r9]                       | !! !! !!                |
    | cmp ch, byte [2 * r9]                       | !! !! !!                |
    | cmp dh, byte [4 * r9]                       | !! !! !!                |
    | cmp bh, byte [8 * r9]                       | !! !! !!                |
    | cmp cl, byte [rsp + 4 * r15]                | 42 3a 0c bc             |
    | cmp dl, byte [rax + 1 * rcx + 0x00]         | 3a 54 08 00             |
    | cmp bl, byte [rax + 1 * rcx - 0x00]         | 3a 5c 08 00             |
    | cmp spl, byte [rax + 1 * rcx + 0x01]        | 40 3a 64 08 01          |
    | cmp bpl, byte [rax + 1 * rcx - 0x01]        | 40 3a 6c 08 ff          |
    | cmp sil, byte [rax + 1 * rcx + 0x00000001]  | 40 3a b4 08 01 00 00 00 |
    | cmp dil, byte [rax + 1 * rcx - 0x00000001]  | 40 3a bc 08 ff ff ff ff |
    | cmp r8b, byte [rax + 1 * rcx + 0x7f]        | 44 3a 44 08 7f          |
    | cmp r9b, byte [rax + 1 * rcx - 0x7f]        | 44 3a 4c 08 81          |
    | cmp r10b, byte [rax + 1 * rcx + 0x80]       | 44 3a 94 08 80 00 00 00 |
    | cmp r11b, byte [rax + 1 * rcx - 0x80]       | 44 3a 5c 08 80          |
    | cmp r12b, byte [rax + 1 * rcx - 0x81]       | 44 3a a4 08 7f ff ff ff |
    | cmp r13b, byte [rax + 1 * rcx + 0xff]       | 44 3a ac 08 ff 00 00 00 |
    | cmp r14b, byte [rax + 1 * rcx - 0xff]       | 44 3a b4 08 01 ff ff ff |
    | cmp r15b, byte [rax + 1 * rcx + 0x7fffffff] | 44 3a bc 08 ff ff ff 7f |
    | cmp ah, byte [rax + 1 * rcx - 0x7fffffff]   | 3a a4 08 01 00 00 80    |
    | cmp ch, byte [rax + 1 * rcx - 0x80000000]   | 3a ac 08 00 00 00 80    |
    | cmp dh, byte [r10 + 0x7f]                   | !! !! !!                |
    | cmp bh, byte [r10 + 0x80]                   | !! !! !!                |
    | cmp cl, byte [r10 - 0x81]                   | 41 3a 8a 7f ff ff ff    |
    | cmp dl, byte [rax]                          | 3a 10                   |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_cmp_reg8_addr8():
    encode(CMP_REG8_ADDR8)


CMP_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | cmp qword [rax], 0x01                        | 48 83 38 01                |
    | cmp qword [rcx], 0x01                        | 48 83 39 01                |
    | cmp qword [rdx], 0x01                        | 48 83 3a 01                |
    | cmp qword [rbx], 0x01                        | 48 83 3b 01                |
    | cmp qword [rsp], 0x01                        | 48 83 3c 24 01             |
    | cmp qword [rbp], 0x01                        | 48 83 7d 00 01             |
    | cmp qword [rsi], 0x01                        | 48 83 3e 01                |
    | cmp qword [rdi], 0x01                        | 48 83 3f 01                |
    | cmp qword [r8], 0x01                         | 49 83 38 01                |
    | cmp qword [r9], 0x01                         | 49 83 39 01                |
    | cmp qword [r10], 0x01                        | 49 83 3a 01                |
    | cmp qword [r11], 0x01                        | 49 83 3b 01                |
    | cmp qword [r12], 0x01                        | 49 83 3c 24 01             |
    | cmp qword [r13], 0x01                        | 49 83 7d 00 01             |
    | cmp qword [r14], 0x01                        | 49 83 3e 01                |
    | cmp qword [r15], 0x01                        | 49 83 3f 01                |
    | cmp qword [rax + 1 * rcx], 0x01              | 48 83 3c 08 01             |
    | cmp qword [rcx + 1 * rcx], 0x01              | 48 83 3c 09 01             |
    | cmp qword [rdx + 1 * rcx], 0x01              | 48 83 3c 0a 01             |
    | cmp qword [rbx + 1 * rcx], 0x01              | 48 83 3c 0b 01             |
    | cmp qword [rsp + 1 * rcx], 0x01              | 48 83 3c 0c 01             |
    | cmp qword [rbp + 1 * rcx], 0x01              | 48 83 7c 0d 00 01          |
    | cmp qword [rsi + 1 * rcx], 0x01              | 48 83 3c 0e 01             |
    | cmp qword [rdi + 1 * rcx], 0x01              | 48 83 3c 0f 01             |
    | cmp qword [r8 + 1 * rcx], 0x01               | 49 83 3c 08 01             |
    | cmp qword [r9 + 1 * rcx], 0x01               | 49 83 3c 09 01             |
    | cmp qword [r10 + 1 * rcx], 0x01              | 49 83 3c 0a 01             |
    | cmp qword [r11 + 1 * rcx], 0x01              | 49 83 3c 0b 01             |
    | cmp qword [r12 + 1 * rcx], 0x01              | 49 83 3c 0c 01             |
    | cmp qword [r13 + 1 * rcx], 0x01              | 49 83 7c 0d 00 01          |
    | cmp qword [r14 + 1 * rcx], 0x01              | 49 83 3c 0e 01             |
    | cmp qword [r15 + 1 * rcx], 0x01              | 49 83 3c 0f 01             |
    | cmp qword [rax + 1 * rax], 0x01              | 48 83 3c 00 01             |
    | cmp qword [rax + 1 * rdx], 0x01              | 48 83 3c 10 01             |
    | cmp qword [rax + 1 * rbx], 0x01              | 48 83 3c 18 01             |
    | cmp qword [rax + 1 * rbp], 0x01              | 48 83 3c 28 01             |
    | cmp qword [rax + 1 * rsi], 0x01              | 48 83 3c 30 01             |
    | cmp qword [rax + 1 * rdi], 0x01              | 48 83 3c 38 01             |
    | cmp qword [rax + 1 * r8], 0x01               | 4a 83 3c 00 01             |
    | cmp qword [rax + 1 * r9], 0x01               | 4a 83 3c 08 01             |
    | cmp qword [rax + 1 * r10], 0x01              | 4a 83 3c 10 01             |
    | cmp qword [rax + 1 * r11], 0x01              | 4a 83 3c 18 01             |
    | cmp qword [rax + 1 * r12], 0x01              | 4a 83 3c 20 01             |
    | cmp qword [rax + 1 * r13], 0x01              | 4a 83 3c 28 01             |
    | cmp qword [rax + 1 * r14], 0x01              | 4a 83 3c 30 01             |
    | cmp qword [rax + 1 * r15], 0x01              | 4a 83 3c 38 01             |
    | cmp qword [rax + 2 * rcx], 0x01              | 48 83 3c 48 01             |
    | cmp qword [rax + 4 * rcx], 0x01              | 48 83 3c 88 01             |
    | cmp qword [rax + 8 * rcx], 0x01              | 48 83 3c c8 01             |
    | cmp qword [r8 + 1 * r9], 0x01                | 4b 83 3c 08 01             |
    | cmp qword [r8 + 2 * r9], 0x01                | 4b 83 3c 48 01             |
    | cmp qword [r8 + 4 * r9], 0x01                | 4b 83 3c 88 01             |
    | cmp qword [r8 + 8 * r9], 0x01                | 4b 83 3c c8 01             |
    | cmp qword [1 * rcx], 0x01                    | 48 83 3c 0d 00 00 00 00 01 |
    | cmp qword [2 * rcx], 0x01                    | 48 83 3c 4d 00 00 00 00 01 |
    | cmp qword [4 * rcx], 0x01                    | 48 83 3c 8d 00 00 00 00 01 |
    | cmp qword [8 * rcx], 0x01                    | 48 83 3c cd 00 00 00 00 01 |
    | cmp qword [1 * r9], 0x01                     | 4a 83 3c 0d 00 00 00 00 01 |
    | cmp qword [2 * r9], 0x01                     | 4a 83 3c 4d 00 00 00 00 01 |
    | cmp qword [4 * r9], 0x01                     | 4a 83 3c 8d 00 00 00 00 01 |
    | cmp qword [8 * r9], 0x01                     | 4a 83 3c cd 00 00 00 00 01 |
    | cmp qword [r13 + 8 * r12], 0x01              | 4b 83 7c e5 00 01          |
    | cmp qword [rsp + 4 * r15], 0x01              | 4a 83 3c bc 01             |
    | cmp qword [rax + 1 * rcx + 0x00], 0x01       | 48 83 7c 08 00 01          |
    | cmp qword [rax + 1 * rcx - 0x00], 0x01       | 48 83 7c 08 00 01          |
    | cmp qword [rax + 1 * rcx + 0x01], 0x01       | 48 83 7c 08 01 01          |
    | cmp qword [rax + 1 * rcx - 0x01], 0x01       | 48 83 7c 08 ff 01          |
    | cmp qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 83 bc 08 01 00 00 00 01 |
    | cmp qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 83 bc 08 ff ff ff ff 01 |
    | cmp qword [rax + 1 * rcx + 0x7f], 0x01       | 48 83 7c 08 7f 01          |
    | cmp qword [rax + 1 * rcx - 0x7f], 0x01       | 48 83 7c 08 81 01          |
    | cmp qword [rax + 1 * rcx + 0x80], 0x01       | 48 83 bc 08 80 00 00 00 01 |
    | cmp qword [rax + 1 * rcx - 0x80], 0x01       | 48 83 7c 08 80 01          |
    | cmp qword [rax + 1 * rcx - 0x81], 0x01       | 48 83 bc 08 7f ff ff ff 01 |
    | cmp qword [rax + 1 * rcx + 0xff], 0x01       | 48 83 bc 08 ff 00 00 00 01 |
    | cmp qword [rax + 1 * rcx - 0xff], 0x01       | 48 83 bc 08 01 ff ff ff 01 |
    | cmp qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 83 bc 08 ff ff ff 7f 01 |
    | cmp qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 83 bc 08 01 00 00 80 01 |
    | cmp qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 83 bc 08 00 00 00 80 01 |
    | cmp qword [r10 + 0x7f], 0x01                 | 49 83 7a 7f 01             |
    | cmp qword [r10 + 0x80], 0x01                 | 49 83 ba 80 00 00 00 01    |
    | cmp qword [r10 - 0x80], 0x01                 | 49 83 7a 80 01             |
    | cmp qword [r10 - 0x81], 0x01                 | 49 83 ba 7f ff ff ff 01    |
    | cmp qword [rax], 0x00                        | 48 83 38 00                |
    | cmp qword [rax], 0x7f                        | 48 83 38 7f                |
    | cmp qword [rax], 0x80                        | 48 83 38 80                |
    | cmp qword [rax], 0xff                        | 48 83 38 ff                |
    | cmp qword [rcx], 0x7f                        | 48 83 39 7f                |
    | cmp qword [rdx], 0x80                        | 48 83 3a 80                |
    | cmp qword [rbx], 0xff                        | 48 83 3b ff                |
    | cmp qword [rsp], 0x00                        | 48 83 3c 24 00             |
    | cmp qword [rsi], 0x7f                        | 48 83 3e 7f                |
    | cmp qword [rdi], 0x80                        | 48 83 3f 80                |
    | cmp qword [r8], 0xff                         | 49 83 38 ff                |
    | cmp qword [r9], 0x00                         | 49 83 39 00                |
    | cmp qword [r11], 0x7f                        | 49 83 3b 7f                |
    | cmp qword [r12], 0x80                        | 49 83 3c 24 80             |
    | cmp qword [r13], 0xff                        | 49 83 7d 00 ff             |
    | cmp qword [r14], 0x00                        | 49 83 3e 00                |
    | cmp qword [rax + 1 * rcx], 0x7f              | 48 83 3c 08 7f             |
    | cmp qword [rcx + 1 * rcx], 0x80              | 48 83 3c 09 80             |
    | cmp qword [rdx + 1 * rcx], 0xff              | 48 83 3c 0a ff             |
    | cmp qword [rbx + 1 * rcx], 0x00              | 48 83 3c 0b 00             |
    | cmp qword [rbp + 1 * rcx], 0x7f              | 48 83 7c 0d 00 7f          |
    | cmp qword [rsi + 1 * rcx], 0x80              | 48 83 3c 0e 80             |
    | cmp qword [rdi + 1 * rcx], 0xff              | 48 83 3c 0f ff             |
    | cmp qword [r8 + 1 * rcx], 0x00               | 49 83 3c 08 00             |
    | cmp qword [r10 + 1 * rcx], 0x7f              | 49 83 3c 0a 7f             |
    | cmp qword [r11 + 1 * rcx], 0x80              | 49 83 3c 0b 80             |
    | cmp qword [r12 + 1 * rcx], 0xff              | 49 83 3c 0c ff             |
    | cmp qword [r13 + 1 * rcx], 0x00              | 49 83 7c 0d 00 00          |
    | cmp qword [r15 + 1 * rcx], 0x7f              | 49 83 3c 0f 7f             |
    | cmp qword [rax + 1 * rax], 0x80              | 48 83 3c 00 80             |
    | cmp qword [rax + 1 * rdx], 0xff              | 48 83 3c 10 ff             |
    | cmp qword [rax + 1 * rbx], 0x00              | 48 83 3c 18 00             |
    | cmp qword [rax + 1 * rsi], 0x7f              | 48 83 3c 30 7f             |
    | cmp qword [rax + 1 * rdi], 0x80              | 48 83 3c 38 80             |
    | cmp qword [rax + 1 * r8], 0xff               | 4a 83 3c 00 ff             |
    | cmp qword [rax + 1 * r9], 0x00               | 4a 83 3c 08 00             |
    | cmp qword [rax + 1 * r11], 0x7f              | 4a 83 3c 18 7f             |
    | cmp qword [rax + 1 * r12], 0x80              | 4a 83 3c 20 80             |
    | cmp qword [rax + 1 * r13], 0xff              | 4a 83 3c 28 ff             |
    | cmp qword [rax + 1 * r14], 0x00              | 4a 83 3c 30 00             |
    | cmp qword [rax + 2 * rcx], 0x7f              | 48 83 3c 48 7f             |
    | cmp qword [rax + 4 * rcx], 0x80              | 48 83 3c 88 80             |
    | cmp qword [rax + 8 * rcx], 0xff              | 48 83 3c c8 ff             |
    | cmp qword [r8 + 1 * r9], 0x00                | 4b 83 3c 08 00             |
    | cmp qword [r8 + 4 * r9], 0x7f                | 4b 83 3c 88 7f             |
    | cmp qword [r8 + 8 * r9], 0x80                | 4b 83 3c c8 80             |
    | cmp qword [1 * rcx], 0xff                    | 48 83 3c 0d 00 00 00 00 ff |
    | cmp qword [2 * rcx], 0x00                    | 48 83 3c 4d 00 00 00 00 00 |
    | cmp qword [8 * rcx], 0x7f                    | 48 83 3c cd 00 00 00 00 7f |
    | cmp qword [1 * r9], 0x80                     | 4a 83 3c 0d 00 00 00 00 80 |
    | cmp qword [2 * r9], 0xff                     | 4a 83 3c 4d 00 00 00 00 ff |
    | cmp qword [4 * r9], 0x00                     | 4a 83 3c 8d 00 00 00 00 00 |
    | cmp qword [r13 + 8 * r12], 0x7f              | 4b 83 7c e5 00 7f          |
    | cmp qword [rsp + 4 * r15], 0x80              | 4a 83 3c bc 80             |
    | cmp qword [rax + 1 * rcx + 0x00], 0xff       | 48 83 7c 08 00 ff          |
    | cmp qword [rax + 1 * rcx - 0x00], 0x00       | 48 83 7c 08 00 00          |
    | cmp qword [rax + 1 * rcx - 0x01], 0x7f       | 48 83 7c 08 ff 7f          |
    | cmp qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 83 bc 08 01 00 00 00 80 |
    | cmp qword [rax + 1 * rcx - 0x00000001], 0xff | 48 83 bc 08 ff ff ff ff ff |
    | cmp qword [rax + 1 * rcx + 0x7f], 0x00       | 48 83 7c 08 7f 00          |
    | cmp qword [rax + 1 * rcx + 0x80], 0x7f       | 48 83 bc 08 80 00 00 00 7f |
    | cmp qword [rax + 1 * rcx - 0x80], 0x80       | 48 83 7c 08 80 80          |
    | cmp qword [rax + 1 * rcx - 0x81], 0xff       | 48 83 bc 08 7f ff ff ff ff |
    | cmp qword [rax + 1 * rcx + 0xff], 0x00       | 48 83 bc 08 ff 00 00 00 00 |
    | cmp qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 83 bc 08 ff ff ff 7f 7f |
    | cmp qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 83 bc 08 01 00 00 80 80 |
    | cmp qword [rax + 1 * rcx - 0x80000000], 0xff | 48 83 bc 08 00 00 00 80 ff |
    | cmp qword [r10 + 0x7f], 0x00                 | 49 83 7a 7f 00             |
    | cmp qword [r10 - 0x80], 0x7f                 | 49 83 7a 80 7f             |
    | cmp qword [r10 - 0x81], 0x80                 | 49 83 ba 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_cmp_addr64_imm8():
    encode(CMP_ADDR64_IMM8)


CMP_ADDR64_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | cmp qword [rax], 0x00000001                        | 48 81 38 01 00 00 00                |
    | cmp qword [rcx], 0x00000001                        | 48 81 39 01 00 00 00                |
    | cmp qword [rdx], 0x00000001                        | 48 81 3a 01 00 00 00                |
    | cmp qword [rbx], 0x00000001                        | 48 81 3b 01 00 00 00                |
    | cmp qword [rsp], 0x00000001                        | 48 81 3c 24 01 00 00 00             |
    | cmp qword [rbp], 0x00000001                        | 48 81 7d 00 01 00 00 00             |
    | cmp qword [rsi], 0x00000001                        | 48 81 3e 01 00 00 00                |
    | cmp qword [rdi], 0x00000001                        | 48 81 3f 01 00 00 00                |
    | cmp qword [r8], 0x00000001                         | 49 81 38 01 00 00 00                |
    | cmp qword [r9], 0x00000001                         | 49 81 39 01 00 00 00                |
    | cmp qword [r10], 0x00000001                        | 49 81 3a 01 00 00 00                |
    | cmp qword [r11], 0x00000001                        | 49 81 3b 01 00 00 00                |
    | cmp qword [r12], 0x00000001                        | 49 81 3c 24 01 00 00 00             |
    | cmp qword [r13], 0x00000001                        | 49 81 7d 00 01 00 00 00             |
    | cmp qword [r14], 0x00000001                        | 49 81 3e 01 00 00 00                |
    | cmp qword [r15], 0x00000001                        | 49 81 3f 01 00 00 00                |
    | cmp qword [rax + 1 * rcx], 0x00000001              | 48 81 3c 08 01 00 00 00             |
    | cmp qword [rcx + 1 * rcx], 0x00000001              | 48 81 3c 09 01 00 00 00             |
    | cmp qword [rdx + 1 * rcx], 0x00000001              | 48 81 3c 0a 01 00 00 00             |
    | cmp qword [rbx + 1 * rcx], 0x00000001              | 48 81 3c 0b 01 00 00 00             |
    | cmp qword [rsp + 1 * rcx], 0x00000001              | 48 81 3c 0c 01 00 00 00             |
    | cmp qword [rbp + 1 * rcx], 0x00000001              | 48 81 7c 0d 00 01 00 00 00          |
    | cmp qword [rsi + 1 * rcx], 0x00000001              | 48 81 3c 0e 01 00 00 00             |
    | cmp qword [rdi + 1 * rcx], 0x00000001              | 48 81 3c 0f 01 00 00 00             |
    | cmp qword [r8 + 1 * rcx], 0x00000001               | 49 81 3c 08 01 00 00 00             |
    | cmp qword [r9 + 1 * rcx], 0x00000001               | 49 81 3c 09 01 00 00 00             |
    | cmp qword [r10 + 1 * rcx], 0x00000001              | 49 81 3c 0a 01 00 00 00             |
    | cmp qword [r11 + 1 * rcx], 0x00000001              | 49 81 3c 0b 01 00 00 00             |
    | cmp qword [r12 + 1 * rcx], 0x00000001              | 49 81 3c 0c 01 00 00 00             |
    | cmp qword [r13 + 1 * rcx], 0x00000001              | 49 81 7c 0d 00 01 00 00 00          |
    | cmp qword [r14 + 1 * rcx], 0x00000001              | 49 81 3c 0e 01 00 00 00             |
    | cmp qword [r15 + 1 * rcx], 0x00000001              | 49 81 3c 0f 01 00 00 00             |
    | cmp qword [rax + 1 * rax], 0x00000001              | 48 81 3c 00 01 00 00 00             |
    | cmp qword [rax + 1 * rdx], 0x00000001              | 48 81 3c 10 01 00 00 00             |
    | cmp qword [rax + 1 * rbx], 0x00000001              | 48 81 3c 18 01 00 00 00             |
    | cmp qword [rax + 1 * rbp], 0x00000001              | 48 81 3c 28 01 00 00 00             |
    | cmp qword [rax + 1 * rsi], 0x00000001              | 48 81 3c 30 01 00 00 00             |
    | cmp qword [rax + 1 * rdi], 0x00000001              | 48 81 3c 38 01 00 00 00             |
    | cmp qword [rax + 1 * r8], 0x00000001               | 4a 81 3c 00 01 00 00 00             |
    | cmp qword [rax + 1 * r9], 0x00000001               | 4a 81 3c 08 01 00 00 00             |
    | cmp qword [rax + 1 * r10], 0x00000001              | 4a 81 3c 10 01 00 00 00             |
    | cmp qword [rax + 1 * r11], 0x00000001              | 4a 81 3c 18 01 00 00 00             |
    | cmp qword [rax + 1 * r12], 0x00000001              | 4a 81 3c 20 01 00 00 00             |
    | cmp qword [rax + 1 * r13], 0x00000001              | 4a 81 3c 28 01 00 00 00             |
    | cmp qword [rax + 1 * r14], 0x00000001              | 4a 81 3c 30 01 00 00 00             |
    | cmp qword [rax + 1 * r15], 0x00000001              | 4a 81 3c 38 01 00 00 00             |
    | cmp qword [rax + 2 * rcx], 0x00000001              | 48 81 3c 48 01 00 00 00             |
    | cmp qword [rax + 4 * rcx], 0x00000001              | 48 81 3c 88 01 00 00 00             |
    | cmp qword [rax + 8 * rcx], 0x00000001              | 48 81 3c c8 01 00 00 00             |
    | cmp qword [r8 + 1 * r9], 0x00000001                | 4b 81 3c 08 01 00 00 00             |
    | cmp qword [r8 + 2 * r9], 0x00000001                | 4b 81 3c 48 01 00 00 00             |
    | cmp qword [r8 + 4 * r9], 0x00000001                | 4b 81 3c 88 01 00 00 00             |
    | cmp qword [r8 + 8 * r9], 0x00000001                | 4b 81 3c c8 01 00 00 00             |
    | cmp qword [1 * rcx], 0x00000001                    | 48 81 3c 0d 00 00 00 00 01 00 00 00 |
    | cmp qword [2 * rcx], 0x00000001                    | 48 81 3c 4d 00 00 00 00 01 00 00 00 |
    | cmp qword [4 * rcx], 0x00000001                    | 48 81 3c 8d 00 00 00 00 01 00 00 00 |
    | cmp qword [8 * rcx], 0x00000001                    | 48 81 3c cd 00 00 00 00 01 00 00 00 |
    | cmp qword [1 * r9], 0x00000001                     | 4a 81 3c 0d 00 00 00 00 01 00 00 00 |
    | cmp qword [2 * r9], 0x00000001                     | 4a 81 3c 4d 00 00 00 00 01 00 00 00 |
    | cmp qword [4 * r9], 0x00000001                     | 4a 81 3c 8d 00 00 00 00 01 00 00 00 |
    | cmp qword [8 * r9], 0x00000001                     | 4a 81 3c cd 00 00 00 00 01 00 00 00 |
    | cmp qword [r13 + 8 * r12], 0x00000001              | 4b 81 7c e5 00 01 00 00 00          |
    | cmp qword [rsp + 4 * r15], 0x00000001              | 4a 81 3c bc 01 00 00 00             |
    | cmp qword [rax + 1 * rcx + 0x00], 0x00000001       | 48 81 7c 08 00 01 00 00 00          |
    | cmp qword [rax + 1 * rcx - 0x00], 0x00000001       | 48 81 7c 08 00 01 00 00 00          |
    | cmp qword [rax + 1 * rcx + 0x01], 0x00000001       | 48 81 7c 08 01 01 00 00 00          |
    | cmp qword [rax + 1 * rcx - 0x01], 0x00000001       | 48 81 7c 08 ff 01 00 00 00          |
    | cmp qword [rax + 1 * rcx + 0x00000001], 0x00000001 | 48 81 bc 08 01 00 00 00 01 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x00000001], 0x00000001 | 48 81 bc 08 ff ff ff ff 01 00 00 00 |
    | cmp qword [rax + 1 * rcx + 0x7f], 0x00000001       | 48 81 7c 08 7f 01 00 00 00          |
    | cmp qword [rax + 1 * rcx - 0x7f], 0x00000001       | 48 81 7c 08 81 01 00 00 00          |
    | cmp qword [rax + 1 * rcx + 0x80], 0x00000001       | 48 81 bc 08 80 00 00 00 01 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x80], 0x00000001       | 48 81 7c 08 80 01 00 00 00          |
    | cmp qword [rax + 1 * rcx - 0x81], 0x00000001       | 48 81 bc 08 7f ff ff ff 01 00 00 00 |
    | cmp qword [rax + 1 * rcx + 0xff], 0x00000001       | 48 81 bc 08 ff 00 00 00 01 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0xff], 0x00000001       | 48 81 bc 08 01 ff ff ff 01 00 00 00 |
    | cmp qword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 48 81 bc 08 ff ff ff 7f 01 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 48 81 bc 08 01 00 00 80 01 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x80000000], 0x00000001 | 48 81 bc 08 00 00 00 80 01 00 00 00 |
    | cmp qword [r10 + 0x7f], 0x00000001                 | 49 81 7a 7f 01 00 00 00             |
    | cmp qword [r10 + 0x80], 0x00000001                 | 49 81 ba 80 00 00 00 01 00 00 00    |
    | cmp qword [r10 - 0x80], 0x00000001                 | 49 81 7a 80 01 00 00 00             |
    | cmp qword [r10 - 0x81], 0x00000001                 | 49 81 ba 7f ff ff ff 01 00 00 00    |
    | cmp qword [rax], 0x00000000                        | 48 81 38 00 00 00 00                |
    | cmp qword [rax], 0x0000007f                        | 48 81 38 7f 00 00 00                |
    | cmp qword [rax], 0x00000080                        | 48 81 38 80 00 00 00                |
    | cmp qword [rax], 0x000000ff                        | 48 81 38 ff 00 00 00                |
    | cmp qword [rax], 0x00000100                        | 48 81 38 00 01 00 00                |
    | cmp qword [rax], 0x00007fff                        | 48 81 38 ff 7f 00 00                |
    | cmp qword [rax], 0x00008000                        | 48 81 38 00 80 00 00                |
    | cmp qword [rax], 0x0000ffff                        | 48 81 38 ff ff 00 00                |
    | cmp qword [rax], 0x00010000                        | 48 81 38 00 00 01 00                |
    | cmp qword [rax], 0x7fffffff                        | 48 81 38 ff ff ff 7f                |
    | cmp qword [rax], 0x80000000                        | 48 81 38 00 00 00 80                |
    | cmp qword [rax], 0xffffffff                        | 48 81 38 ff ff ff ff                |
    | cmp qword [rcx], 0x0000007f                        | 48 81 39 7f 00 00 00                |
    | cmp qword [rdx], 0x00000080                        | 48 81 3a 80 00 00 00                |
    | cmp qword [rbx], 0x000000ff                        | 48 81 3b ff 00 00 00                |
    | cmp qword [rsp], 0x00000100                        | 48 81 3c 24 00 01 00 00             |
    | cmp qword [rbp], 0x00007fff                        | 48 81 7d 00 ff 7f 00 00             |
    | cmp qword [rsi], 0x00008000                        | 48 81 3e 00 80 00 00                |
    | cmp qword [rdi], 0x0000ffff                        | 48 81 3f ff ff 00 00                |
    | cmp qword [r8], 0x00010000                         | 49 81 38 00 00 01 00                |
    | cmp qword [r9], 0x7fffffff                         | 49 81 39 ff ff ff 7f                |
    | cmp qword [r10], 0x80000000                        | 49 81 3a 00 00 00 80                |
    | cmp qword [r11], 0xffffffff                        | 49 81 3b ff ff ff ff                |
    | cmp qword [r12], 0x00000000                        | 49 81 3c 24 00 00 00 00             |
    | cmp qword [r14], 0x0000007f                        | 49 81 3e 7f 00 00 00                |
    | cmp qword [r15], 0x00000080                        | 49 81 3f 80 00 00 00                |
    | cmp qword [rax + 1 * rcx], 0x000000ff              | 48 81 3c 08 ff 00 00 00             |
    | cmp qword [rcx + 1 * rcx], 0x00000100              | 48 81 3c 09 00 01 00 00             |
    | cmp qword [rdx + 1 * rcx], 0x00007fff              | 48 81 3c 0a ff 7f 00 00             |
    | cmp qword [rbx + 1 * rcx], 0x00008000              | 48 81 3c 0b 00 80 00 00             |
    | cmp qword [rsp + 1 * rcx], 0x0000ffff              | 48 81 3c 0c ff ff 00 00             |
    | cmp qword [rbp + 1 * rcx], 0x00010000              | 48 81 7c 0d 00 00 00 01 00          |
    | cmp qword [rsi + 1 * rcx], 0x7fffffff              | 48 81 3c 0e ff ff ff 7f             |
    | cmp qword [rdi + 1 * rcx], 0x80000000              | 48 81 3c 0f 00 00 00 80             |
    | cmp qword [r8 + 1 * rcx], 0xffffffff               | 49 81 3c 08 ff ff ff ff             |
    | cmp qword [r9 + 1 * rcx], 0x00000000               | 49 81 3c 09 00 00 00 00             |
    | cmp qword [r11 + 1 * rcx], 0x0000007f              | 49 81 3c 0b 7f 00 00 00             |
    | cmp qword [r12 + 1 * rcx], 0x00000080              | 49 81 3c 0c 80 00 00 00             |
    | cmp qword [r13 + 1 * rcx], 0x000000ff              | 49 81 7c 0d 00 ff 00 00 00          |
    | cmp qword [r14 + 1 * rcx], 0x00000100              | 49 81 3c 0e 00 01 00 00             |
    | cmp qword [r15 + 1 * rcx], 0x00007fff              | 49 81 3c 0f ff 7f 00 00             |
    | cmp qword [rax + 1 * rax], 0x00008000              | 48 81 3c 00 00 80 00 00             |
    | cmp qword [rax + 1 * rdx], 0x0000ffff              | 48 81 3c 10 ff ff 00 00             |
    | cmp qword [rax + 1 * rbx], 0x00010000              | 48 81 3c 18 00 00 01 00             |
    | cmp qword [rax + 1 * rbp], 0x7fffffff              | 48 81 3c 28 ff ff ff 7f             |
    | cmp qword [rax + 1 * rsi], 0x80000000              | 48 81 3c 30 00 00 00 80             |
    | cmp qword [rax + 1 * rdi], 0xffffffff              | 48 81 3c 38 ff ff ff ff             |
    | cmp qword [rax + 1 * r8], 0x00000000               | 4a 81 3c 00 00 00 00 00             |
    | cmp qword [rax + 1 * r10], 0x0000007f              | 4a 81 3c 10 7f 00 00 00             |
    | cmp qword [rax + 1 * r11], 0x00000080              | 4a 81 3c 18 80 00 00 00             |
    | cmp qword [rax + 1 * r12], 0x000000ff              | 4a 81 3c 20 ff 00 00 00             |
    | cmp qword [rax + 1 * r13], 0x00000100              | 4a 81 3c 28 00 01 00 00             |
    | cmp qword [rax + 1 * r14], 0x00007fff              | 4a 81 3c 30 ff 7f 00 00             |
    | cmp qword [rax + 1 * r15], 0x00008000              | 4a 81 3c 38 00 80 00 00             |
    | cmp qword [rax + 2 * rcx], 0x0000ffff              | 48 81 3c 48 ff ff 00 00             |
    | cmp qword [rax + 4 * rcx], 0x00010000              | 48 81 3c 88 00 00 01 00             |
    | cmp qword [rax + 8 * rcx], 0x7fffffff              | 48 81 3c c8 ff ff ff 7f             |
    | cmp qword [r8 + 1 * r9], 0x80000000                | 4b 81 3c 08 00 00 00 80             |
    | cmp qword [r8 + 2 * r9], 0xffffffff                | 4b 81 3c 48 ff ff ff ff             |
    | cmp qword [r8 + 4 * r9], 0x00000000                | 4b 81 3c 88 00 00 00 00             |
    | cmp qword [1 * rcx], 0x0000007f                    | 48 81 3c 0d 00 00 00 00 7f 00 00 00 |
    | cmp qword [2 * rcx], 0x00000080                    | 48 81 3c 4d 00 00 00 00 80 00 00 00 |
    | cmp qword [4 * rcx], 0x000000ff                    | 48 81 3c 8d 00 00 00 00 ff 00 00 00 |
    | cmp qword [8 * rcx], 0x00000100                    | 48 81 3c cd 00 00 00 00 00 01 00 00 |
    | cmp qword [1 * r9], 0x00007fff                     | 4a 81 3c 0d 00 00 00 00 ff 7f 00 00 |
    | cmp qword [2 * r9], 0x00008000                     | 4a 81 3c 4d 00 00 00 00 00 80 00 00 |
    | cmp qword [4 * r9], 0x0000ffff                     | 4a 81 3c 8d 00 00 00 00 ff ff 00 00 |
    | cmp qword [8 * r9], 0x00010000                     | 4a 81 3c cd 00 00 00 00 00 00 01 00 |
    | cmp qword [r13 + 8 * r12], 0x7fffffff              | 4b 81 7c e5 00 ff ff ff 7f          |
    | cmp qword [rsp + 4 * r15], 0x80000000              | 4a 81 3c bc 00 00 00 80             |
    | cmp qword [rax + 1 * rcx + 0x00], 0xffffffff       | 48 81 7c 08 00 ff ff ff ff          |
    | cmp qword [rax + 1 * rcx - 0x00], 0x00000000       | 48 81 7c 08 00 00 00 00 00          |
    | cmp qword [rax + 1 * rcx - 0x01], 0x0000007f       | 48 81 7c 08 ff 7f 00 00 00          |
    | cmp qword [rax + 1 * rcx + 0x00000001], 0x00000080 | 48 81 bc 08 01 00 00 00 80 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x00000001], 0x000000ff | 48 81 bc 08 ff ff ff ff ff 00 00 00 |
    | cmp qword [rax + 1 * rcx + 0x7f], 0x00000100       | 48 81 7c 08 7f 00 01 00 00          |
    | cmp qword [rax + 1 * rcx - 0x7f], 0x00007fff       | 48 81 7c 08 81 ff 7f 00 00          |
    | cmp qword [rax + 1 * rcx + 0x80], 0x00008000       | 48 81 bc 08 80 00 00 00 00 80 00 00 |
    | cmp qword [rax + 1 * rcx - 0x80], 0x0000ffff       | 48 81 7c 08 80 ff ff 00 00          |
    | cmp qword [rax + 1 * rcx - 0x81], 0x00010000       | 48 81 bc 08 7f ff ff ff 00 00 01 00 |
    | cmp qword [rax + 1 * rcx + 0xff], 0x7fffffff       | 48 81 bc 08 ff 00 00 00 ff ff ff 7f |
    | cmp qword [rax + 1 * rcx - 0xff], 0x80000000       | 48 81 bc 08 01 ff ff ff 00 00 00 80 |
    | cmp qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 48 81 bc 08 ff ff ff 7f ff ff ff ff |
    | cmp qword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 48 81 bc 08 01 00 00 80 00 00 00 00 |
    | cmp qword [r10 + 0x7f], 0x0000007f                 | 49 81 7a 7f 7f 00 00 00             |
    | cmp qword [r10 + 0x80], 0x00000080                 | 49 81 ba 80 00 00 00 80 00 00 00    |
    | cmp qword [r10 - 0x80], 0x000000ff                 | 49 81 7a 80 ff 00 00 00             |
    | cmp qword [r10 - 0x81], 0x00000100                 | 49 81 ba 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_cmp_addr64_imm32():
    encode(CMP_ADDR64_IMM32)


CMP_ADDR64_REG64 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | cmp qword [rax], rcx                        | 48 39 08                |
    | cmp qword [rcx], rcx                        | 48 39 09                |
    | cmp qword [rdx], rcx                        | 48 39 0a                |
    | cmp qword [rbx], rcx                        | 48 39 0b                |
    | cmp qword [rsp], rcx                        | 48 39 0c 24             |
    | cmp qword [rbp], rcx                        | 48 39 4d 00             |
    | cmp qword [rsi], rcx                        | 48 39 0e                |
    | cmp qword [rdi], rcx                        | 48 39 0f                |
    | cmp qword [r8], rcx                         | 49 39 08                |
    | cmp qword [r9], rcx                         | 49 39 09                |
    | cmp qword [r10], rcx                        | 49 39 0a                |
    | cmp qword [r11], rcx                        | 49 39 0b                |
    | cmp qword [r12], rcx                        | 49 39 0c 24             |
    | cmp qword [r13], rcx                        | 49 39 4d 00             |
    | cmp qword [r14], rcx                        | 49 39 0e                |
    | cmp qword [r15], rcx                        | 49 39 0f                |
    | cmp qword [rax + 1 * rcx], rcx              | 48 39 0c 08             |
    | cmp qword [rcx + 1 * rcx], rcx              | 48 39 0c 09             |
    | cmp qword [rdx + 1 * rcx], rcx              | 48 39 0c 0a             |
    | cmp qword [rbx + 1 * rcx], rcx              | 48 39 0c 0b             |
    | cmp qword [rsp + 1 * rcx], rcx              | 48 39 0c 0c             |
    | cmp qword [rbp + 1 * rcx], rcx              | 48 39 4c 0d 00          |
    | cmp qword [rsi + 1 * rcx], rcx              | 48 39 0c 0e             |
    | cmp qword [rdi + 1 * rcx], rcx              | 48 39 0c 0f             |
    | cmp qword [r8 + 1 * rcx], rcx               | 49 39 0c 08             |
    | cmp qword [r9 + 1 * rcx], rcx               | 49 39 0c 09             |
    | cmp qword [r10 + 1 * rcx], rcx              | 49 39 0c 0a             |
    | cmp qword [r11 + 1 * rcx], rcx              | 49 39 0c 0b             |
    | cmp qword [r12 + 1 * rcx], rcx              | 49 39 0c 0c             |
    | cmp qword [r13 + 1 * rcx], rcx              | 49 39 4c 0d 00          |
    | cmp qword [r14 + 1 * rcx], rcx              | 49 39 0c 0e             |
    | cmp qword [r15 + 1 * rcx], rcx              | 49 39 0c 0f             |
    | cmp qword [rax + 1 * rax], rcx              | 48 39 0c 00             |
    | cmp qword [rax + 1 * rdx], rcx              | 48 39 0c 10             |
    | cmp qword [rax + 1 * rbx], rcx              | 48 39 0c 18             |
    | cmp qword [rax + 1 * rbp], rcx              | 48 39 0c 28             |
    | cmp qword [rax + 1 * rsi], rcx              | 48 39 0c 30             |
    | cmp qword [rax + 1 * rdi], rcx              | 48 39 0c 38             |
    | cmp qword [rax + 1 * r8], rcx               | 4a 39 0c 00             |
    | cmp qword [rax + 1 * r9], rcx               | 4a 39 0c 08             |
    | cmp qword [rax + 1 * r10], rcx              | 4a 39 0c 10             |
    | cmp qword [rax + 1 * r11], rcx              | 4a 39 0c 18             |
    | cmp qword [rax + 1 * r12], rcx              | 4a 39 0c 20             |
    | cmp qword [rax + 1 * r13], rcx              | 4a 39 0c 28             |
    | cmp qword [rax + 1 * r14], rcx              | 4a 39 0c 30             |
    | cmp qword [rax + 1 * r15], rcx              | 4a 39 0c 38             |
    | cmp qword [rax + 2 * rcx], rcx              | 48 39 0c 48             |
    | cmp qword [rax + 4 * rcx], rcx              | 48 39 0c 88             |
    | cmp qword [rax + 8 * rcx], rcx              | 48 39 0c c8             |
    | cmp qword [r8 + 1 * r9], rcx                | 4b 39 0c 08             |
    | cmp qword [r8 + 2 * r9], rcx                | 4b 39 0c 48             |
    | cmp qword [r8 + 4 * r9], rcx                | 4b 39 0c 88             |
    | cmp qword [r8 + 8 * r9], rcx                | 4b 39 0c c8             |
    | cmp qword [1 * rcx], rcx                    | 48 39 0c 0d 00 00 00 00 |
    | cmp qword [2 * rcx], rcx                    | 48 39 0c 4d 00 00 00 00 |
    | cmp qword [4 * rcx], rcx                    | 48 39 0c 8d 00 00 00 00 |
    | cmp qword [8 * rcx], rcx                    | 48 39 0c cd 00 00 00 00 |
    | cmp qword [1 * r9], rcx                     | 4a 39 0c 0d 00 00 00 00 |
    | cmp qword [2 * r9], rcx                     | 4a 39 0c 4d 00 00 00 00 |
    | cmp qword [4 * r9], rcx                     | 4a 39 0c 8d 00 00 00 00 |
    | cmp qword [8 * r9], rcx                     | 4a 39 0c cd 00 00 00 00 |
    | cmp qword [r13 + 8 * r12], rcx              | 4b 39 4c e5 00          |
    | cmp qword [rsp + 4 * r15], rcx              | 4a 39 0c bc             |
    | cmp qword [rax + 1 * rcx + 0x00], rcx       | 48 39 4c 08 00          |
    | cmp qword [rax + 1 * rcx - 0x00], rcx       | 48 39 4c 08 00          |
    | cmp qword [rax + 1 * rcx + 0x01], rcx       | 48 39 4c 08 01          |
    | cmp qword [rax + 1 * rcx - 0x01], rcx       | 48 39 4c 08 ff          |
    | cmp qword [rax + 1 * rcx + 0x00000001], rcx | 48 39 8c 08 01 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x00000001], rcx | 48 39 8c 08 ff ff ff ff |
    | cmp qword [rax + 1 * rcx + 0x7f], rcx       | 48 39 4c 08 7f          |
    | cmp qword [rax + 1 * rcx - 0x7f], rcx       | 48 39 4c 08 81          |
    | cmp qword [rax + 1 * rcx + 0x80], rcx       | 48 39 8c 08 80 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x80], rcx       | 48 39 4c 08 80          |
    | cmp qword [rax + 1 * rcx - 0x81], rcx       | 48 39 8c 08 7f ff ff ff |
    | cmp qword [rax + 1 * rcx + 0xff], rcx       | 48 39 8c 08 ff 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0xff], rcx       | 48 39 8c 08 01 ff ff ff |
    | cmp qword [rax + 1 * rcx + 0x7fffffff], rcx | 48 39 8c 08 ff ff ff 7f |
    | cmp qword [rax + 1 * rcx - 0x7fffffff], rcx | 48 39 8c 08 01 00 00 80 |
    | cmp qword [rax + 1 * rcx - 0x80000000], rcx | 48 39 8c 08 00 00 00 80 |
    | cmp qword [r10 + 0x7f], rcx                 | 49 39 4a 7f             |
    | cmp qword [r10 + 0x80], rcx                 | 49 39 8a 80 00 00 00    |
    | cmp qword [r10 - 0x80], rcx                 | 49 39 4a 80             |
    | cmp qword [r10 - 0x81], rcx                 | 49 39 8a 7f ff ff ff    |
    | cmp qword [rax], rax                        | 48 39 00                |
    | cmp qword [rax], rdx                        | 48 39 10                |
    | cmp qword [rax], rbx                        | 48 39 18                |
    | cmp qword [rax], rsp                        | 48 39 20                |
    | cmp qword [rax], rbp                        | 48 39 28                |
    | cmp qword [rax], rsi                        | 48 39 30                |
    | cmp qword [rax], rdi                        | 48 39 38                |
    | cmp qword [rax], r8                         | 4c 39 00                |
    | cmp qword [rax], r9                         | 4c 39 08                |
    | cmp qword [rax], r10                        | 4c 39 10                |
    | cmp qword [rax], r11                        | 4c 39 18                |
    | cmp qword [rax], r12                        | 4c 39 20                |
    | cmp qword [rax], r13                        | 4c 39 28                |
    | cmp qword [rax], r14                        | 4c 39 30                |
    | cmp qword [rax], r15                        | 4c 39 38                |
    | cmp qword [rcx], rdx                        | 48 39 11                |
    | cmp qword [rdx], rbx                        | 48 39 1a                |
    | cmp qword [rbx], rsp                        | 48 39 23                |
    | cmp qword [rsp], rbp                        | 48 39 2c 24             |
    | cmp qword [rbp], rsi                        | 48 39 75 00             |
    | cmp qword [rsi], rdi                        | 48 39 3e                |
    | cmp qword [rdi], r8                         | 4c 39 07                |
    | cmp qword [r8], r9                          | 4d 39 08                |
    | cmp qword [r9], r10                         | 4d 39 11                |
    | cmp qword [r10], r11                        | 4d 39 1a                |
    | cmp qword [r11], r12                        | 4d 39 23                |
    | cmp qword [r12], r13                        | 4d 39 2c 24             |
    | cmp qword [r13], r14                        | 4d 39 75 00             |
    | cmp qword [r14], r15                        | 4d 39 3e                |
    | cmp qword [r15], rax                        | 49 39 07                |
    | cmp qword [rcx + 1 * rcx], rdx              | 48 39 14 09             |
    | cmp qword [rdx + 1 * rcx], rbx              | 48 39 1c 0a             |
    | cmp qword [rbx + 1 * rcx], rsp              | 48 39 24 0b             |
    | cmp qword [rsp + 1 * rcx], rbp              | 48 39 2c 0c             |
    | cmp qword [rbp + 1 * rcx], rsi              | 48 39 74 0d 00          |
    | cmp qword [rsi + 1 * rcx], rdi              | 48 39 3c 0e             |
    | cmp qword [rdi + 1 * rcx], r8               | 4c 39 04 0f             |
    | cmp qword [r8 + 1 * rcx], r9                | 4d 39 0c 08             |
    | cmp qword [r9 + 1 * rcx], r10               | 4d 39 14 09             |
    | cmp qword [r10 + 1 * rcx], r11              | 4d 39 1c 0a             |
    | cmp qword [r11 + 1 * rcx], r12              | 4d 39 24 0b             |
    | cmp qword [r12 + 1 * rcx], r13              | 4d 39 2c 0c             |
    | cmp qword [r13 + 1 * rcx], r14              | 4d 39 74 0d 00          |
    | cmp qword [r14 + 1 * rcx], r15              | 4d 39 3c 0e             |
    | cmp qword [r15 + 1 * rcx], rax              | 49 39 04 0f             |
    | cmp qword [rax + 1 * rdx], rdx              | 48 39 14 10             |
    | cmp qword [rax + 1 * rbx], rbx              | 48 39 1c 18             |
    | cmp qword [rax + 1 * rbp], rsp              | 48 39 24 28             |
    | cmp qword [rax + 1 * rsi], rbp              | 48 39 2c 30             |
    | cmp qword [rax + 1 * rdi], rsi              | 48 39 34 38             |
    | cmp qword [rax + 1 * r8], rdi               | 4a 39 3c 00             |
    | cmp qword [rax + 1 * r9], r8                | 4e 39 04 08             |
    | cmp qword [rax + 1 * r10], r9               | 4e 39 0c 10             |
    | cmp qword [rax + 1 * r11], r10              | 4e 39 14 18             |
    | cmp qword [rax + 1 * r12], r11              | 4e 39 1c 20             |
    | cmp qword [rax + 1 * r13], r12              | 4e 39 24 28             |
    | cmp qword [rax + 1 * r14], r13              | 4e 39 2c 30             |
    | cmp qword [rax + 1 * r15], r14              | 4e 39 34 38             |
    | cmp qword [rax + 2 * rcx], r15              | 4c 39 3c 48             |
    | cmp qword [rax + 4 * rcx], rax              | 48 39 04 88             |
    | cmp qword [r8 + 1 * r9], rdx                | 4b 39 14 08             |
    | cmp qword [r8 + 2 * r9], rbx                | 4b 39 1c 48             |
    | cmp qword [r8 + 4 * r9], rsp                | 4b 39 24 88             |
    | cmp qword [r8 + 8 * r9], rbp                | 4b 39 2c c8             |
    | cmp qword [1 * rcx], rsi                    | 48 39 34 0d 00 00 00 00 |
    | cmp qword [2 * rcx], rdi                    | 48 39 3c 4d 00 00 00 00 |
    | cmp qword [4 * rcx], r8                     | 4c 39 04 8d 00 00 00 00 |
    | cmp qword [8 * rcx], r9                     | 4c 39 0c cd 00 00 00 00 |
    | cmp qword [1 * r9], r10                     | 4e 39 14 0d 00 00 00 00 |
    | cmp qword [2 * r9], r11                     | 4e 39 1c 4d 00 00 00 00 |
    | cmp qword [4 * r9], r12                     | 4e 39 24 8d 00 00 00 00 |
    | cmp qword [8 * r9], r13                     | 4e 39 2c cd 00 00 00 00 |
    | cmp qword [r13 + 8 * r12], r14              | 4f 39 74 e5 00          |
    | cmp qword [rsp + 4 * r15], r15              | 4e 39 3c bc             |
    | cmp qword [rax + 1 * rcx + 0x00], rax       | 48 39 44 08 00          |
    | cmp qword [rax + 1 * rcx + 0x01], rdx       | 48 39 54 08 01          |
    | cmp qword [rax + 1 * rcx - 0x01], rbx       | 48 39 5c 08 ff          |
    | cmp qword [rax + 1 * rcx + 0x00000001], rsp | 48 39 a4 08 01 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x00000001], rbp | 48 39 ac 08 ff ff ff ff |
    | cmp qword [rax + 1 * rcx + 0x7f], rsi       | 48 39 74 08 7f          |
    | cmp qword [rax + 1 * rcx - 0x7f], rdi       | 48 39 7c 08 81          |
    | cmp qword [rax + 1 * rcx + 0x80], r8        | 4c 39 84 08 80 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0x80], r9        | 4c 39 4c 08 80          |
    | cmp qword [rax + 1 * rcx - 0x81], r10       | 4c 39 94 08 7f ff ff ff |
    | cmp qword [rax + 1 * rcx + 0xff], r11       | 4c 39 9c 08 ff 00 00 00 |
    | cmp qword [rax + 1 * rcx - 0xff], r12       | 4c 39 a4 08 01 ff ff ff |
    | cmp qword [rax + 1 * rcx + 0x7fffffff], r13 | 4c 39 ac 08 ff ff ff 7f |
    | cmp qword [rax + 1 * rcx - 0x7fffffff], r14 | 4c 39 b4 08 01 00 00 80 |
    | cmp qword [rax + 1 * rcx - 0x80000000], r15 | 4c 39 bc 08 00 00 00 80 |
    | cmp qword [r10 + 0x7f], rax                 | 49 39 42 7f             |
    | cmp qword [r10 - 0x80], rdx                 | 49 39 52 80             |
    | cmp qword [r10 - 0x81], rbx                 | 49 39 9a 7f ff ff ff    |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_cmp_addr64_reg64():
    encode(CMP_ADDR64_REG64)


CMP_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | cmp dword [rax], 0x01                        | 83 38 01                   |
    | cmp dword [rcx], 0x01                        | 83 39 01                   |
    | cmp dword [rdx], 0x01                        | 83 3a 01                   |
    | cmp dword [rbx], 0x01                        | 83 3b 01                   |
    | cmp dword [rsp], 0x01                        | 83 3c 24 01                |
    | cmp dword [rbp], 0x01                        | 83 7d 00 01                |
    | cmp dword [rsi], 0x01                        | 83 3e 01                   |
    | cmp dword [rdi], 0x01                        | 83 3f 01                   |
    | cmp dword [r8], 0x01                         | 41 83 38 01                |
    | cmp dword [r9], 0x01                         | 41 83 39 01                |
    | cmp dword [r10], 0x01                        | 41 83 3a 01                |
    | cmp dword [r11], 0x01                        | 41 83 3b 01                |
    | cmp dword [r12], 0x01                        | 41 83 3c 24 01             |
    | cmp dword [r13], 0x01                        | 41 83 7d 00 01             |
    | cmp dword [r14], 0x01                        | 41 83 3e 01                |
    | cmp dword [r15], 0x01                        | 41 83 3f 01                |
    | cmp dword [rax + 1 * rcx], 0x01              | 83 3c 08 01                |
    | cmp dword [rcx + 1 * rcx], 0x01              | 83 3c 09 01                |
    | cmp dword [rdx + 1 * rcx], 0x01              | 83 3c 0a 01                |
    | cmp dword [rbx + 1 * rcx], 0x01              | 83 3c 0b 01                |
    | cmp dword [rsp + 1 * rcx], 0x01              | 83 3c 0c 01                |
    | cmp dword [rbp + 1 * rcx], 0x01              | 83 7c 0d 00 01             |
    | cmp dword [rsi + 1 * rcx], 0x01              | 83 3c 0e 01                |
    | cmp dword [rdi + 1 * rcx], 0x01              | 83 3c 0f 01                |
    | cmp dword [r8 + 1 * rcx], 0x01               | 41 83 3c 08 01             |
    | cmp dword [r9 + 1 * rcx], 0x01               | 41 83 3c 09 01             |
    | cmp dword [r10 + 1 * rcx], 0x01              | 41 83 3c 0a 01             |
    | cmp dword [r11 + 1 * rcx], 0x01              | 41 83 3c 0b 01             |
    | cmp dword [r12 + 1 * rcx], 0x01              | 41 83 3c 0c 01             |
    | cmp dword [r13 + 1 * rcx], 0x01              | 41 83 7c 0d 00 01          |
    | cmp dword [r14 + 1 * rcx], 0x01              | 41 83 3c 0e 01             |
    | cmp dword [r15 + 1 * rcx], 0x01              | 41 83 3c 0f 01             |
    | cmp dword [rax + 1 * rax], 0x01              | 83 3c 00 01                |
    | cmp dword [rax + 1 * rdx], 0x01              | 83 3c 10 01                |
    | cmp dword [rax + 1 * rbx], 0x01              | 83 3c 18 01                |
    | cmp dword [rax + 1 * rbp], 0x01              | 83 3c 28 01                |
    | cmp dword [rax + 1 * rsi], 0x01              | 83 3c 30 01                |
    | cmp dword [rax + 1 * rdi], 0x01              | 83 3c 38 01                |
    | cmp dword [rax + 1 * r8], 0x01               | 42 83 3c 00 01             |
    | cmp dword [rax + 1 * r9], 0x01               | 42 83 3c 08 01             |
    | cmp dword [rax + 1 * r10], 0x01              | 42 83 3c 10 01             |
    | cmp dword [rax + 1 * r11], 0x01              | 42 83 3c 18 01             |
    | cmp dword [rax + 1 * r12], 0x01              | 42 83 3c 20 01             |
    | cmp dword [rax + 1 * r13], 0x01              | 42 83 3c 28 01             |
    | cmp dword [rax + 1 * r14], 0x01              | 42 83 3c 30 01             |
    | cmp dword [rax + 1 * r15], 0x01              | 42 83 3c 38 01             |
    | cmp dword [rax + 2 * rcx], 0x01              | 83 3c 48 01                |
    | cmp dword [rax + 4 * rcx], 0x01              | 83 3c 88 01                |
    | cmp dword [rax + 8 * rcx], 0x01              | 83 3c c8 01                |
    | cmp dword [r8 + 1 * r9], 0x01                | 43 83 3c 08 01             |
    | cmp dword [r8 + 2 * r9], 0x01                | 43 83 3c 48 01             |
    | cmp dword [r8 + 4 * r9], 0x01                | 43 83 3c 88 01             |
    | cmp dword [r8 + 8 * r9], 0x01                | 43 83 3c c8 01             |
    | cmp dword [1 * rcx], 0x01                    | 83 3c 0d 00 00 00 00 01    |
    | cmp dword [2 * rcx], 0x01                    | 83 3c 4d 00 00 00 00 01    |
    | cmp dword [4 * rcx], 0x01                    | 83 3c 8d 00 00 00 00 01    |
    | cmp dword [8 * rcx], 0x01                    | 83 3c cd 00 00 00 00 01    |
    | cmp dword [1 * r9], 0x01                     | 42 83 3c 0d 00 00 00 00 01 |
    | cmp dword [2 * r9], 0x01                     | 42 83 3c 4d 00 00 00 00 01 |
    | cmp dword [4 * r9], 0x01                     | 42 83 3c 8d 00 00 00 00 01 |
    | cmp dword [8 * r9], 0x01                     | 42 83 3c cd 00 00 00 00 01 |
    | cmp dword [r13 + 8 * r12], 0x01              | 43 83 7c e5 00 01          |
    | cmp dword [rsp + 4 * r15], 0x01              | 42 83 3c bc 01             |
    | cmp dword [rax + 1 * rcx + 0x00], 0x01       | 83 7c 08 00 01             |
    | cmp dword [rax + 1 * rcx - 0x00], 0x01       | 83 7c 08 00 01             |
    | cmp dword [rax + 1 * rcx + 0x01], 0x01       | 83 7c 08 01 01             |
    | cmp dword [rax + 1 * rcx - 0x01], 0x01       | 83 7c 08 ff 01             |
    | cmp dword [rax + 1 * rcx + 0x00000001], 0x01 | 83 bc 08 01 00 00 00 01    |
    | cmp dword [rax + 1 * rcx - 0x00000001], 0x01 | 83 bc 08 ff ff ff ff 01    |
    | cmp dword [rax + 1 * rcx + 0x7f], 0x01       | 83 7c 08 7f 01             |
    | cmp dword [rax + 1 * rcx - 0x7f], 0x01       | 83 7c 08 81 01             |
    | cmp dword [rax + 1 * rcx + 0x80], 0x01       | 83 bc 08 80 00 00 00 01    |
    | cmp dword [rax + 1 * rcx - 0x80], 0x01       | 83 7c 08 80 01             |
    | cmp dword [rax + 1 * rcx - 0x81], 0x01       | 83 bc 08 7f ff ff ff 01    |
    | cmp dword [rax + 1 * rcx + 0xff], 0x01       | 83 bc 08 ff 00 00 00 01    |
    | cmp dword [rax + 1 * rcx - 0xff], 0x01       | 83 bc 08 01 ff ff ff 01    |
    | cmp dword [rax + 1 * rcx + 0x7fffffff], 0x01 | 83 bc 08 ff ff ff 7f 01    |
    | cmp dword [rax + 1 * rcx - 0x7fffffff], 0x01 | 83 bc 08 01 00 00 80 01    |
    | cmp dword [rax + 1 * rcx - 0x80000000], 0x01 | 83 bc 08 00 00 00 80 01    |
    | cmp dword [r10 + 0x7f], 0x01                 | 41 83 7a 7f 01             |
    | cmp dword [r10 + 0x80], 0x01                 | 41 83 ba 80 00 00 00 01    |
    | cmp dword [r10 - 0x80], 0x01                 | 41 83 7a 80 01             |
    | cmp dword [r10 - 0x81], 0x01                 | 41 83 ba 7f ff ff ff 01    |
    | cmp dword [rax], 0x00                        | 83 38 00                   |
    | cmp dword [rax], 0x7f                        | 83 38 7f                   |
    | cmp dword [rax], 0x80                        | 83 38 80                   |
    | cmp dword [rax], 0xff                        | 83 38 ff                   |
    | cmp dword [rcx], 0x7f                        | 83 39 7f                   |
    | cmp dword [rdx], 0x80                        | 83 3a 80                   |
    | cmp dword [rbx], 0xff                        | 83 3b ff                   |
    | cmp dword [rsp], 0x00                        | 83 3c 24 00                |
    | cmp dword [rsi], 0x7f                        | 83 3e 7f                   |
    | cmp dword [rdi], 0x80                        | 83 3f 80                   |
    | cmp dword [r8], 0xff                         | 41 83 38 ff                |
    | cmp dword [r9], 0x00                         | 41 83 39 00                |
    | cmp dword [r11], 0x7f                        | 41 83 3b 7f                |
    | cmp dword [r12], 0x80                        | 41 83 3c 24 80             |
    | cmp dword [r13], 0xff                        | 41 83 7d 00 ff             |
    | cmp dword [r14], 0x00                        | 41 83 3e 00                |
    | cmp dword [rax + 1 * rcx], 0x7f              | 83 3c 08 7f                |
    | cmp dword [rcx + 1 * rcx], 0x80              | 83 3c 09 80                |
    | cmp dword [rdx + 1 * rcx], 0xff              | 83 3c 0a ff                |
    | cmp dword [rbx + 1 * rcx], 0x00              | 83 3c 0b 00                |
    | cmp dword [rbp + 1 * rcx], 0x7f              | 83 7c 0d 00 7f             |
    | cmp dword [rsi + 1 * rcx], 0x80              | 83 3c 0e 80                |
    | cmp dword [rdi + 1 * rcx], 0xff              | 83 3c 0f ff                |
    | cmp dword [r8 + 1 * rcx], 0x00               | 41 83 3c 08 00             |
    | cmp dword [r10 + 1 * rcx], 0x7f              | 41 83 3c 0a 7f             |
    | cmp dword [r11 + 1 * rcx], 0x80              | 41 83 3c 0b 80             |
    | cmp dword [r12 + 1 * rcx], 0xff              | 41 83 3c 0c ff             |
    | cmp dword [r13 + 1 * rcx], 0x00              | 41 83 7c 0d 00 00          |
    | cmp dword [r15 + 1 * rcx], 0x7f              | 41 83 3c 0f 7f             |
    | cmp dword [rax + 1 * rax], 0x80              | 83 3c 00 80                |
    | cmp dword [rax + 1 * rdx], 0xff              | 83 3c 10 ff                |
    | cmp dword [rax + 1 * rbx], 0x00              | 83 3c 18 00                |
    | cmp dword [rax + 1 * rsi], 0x7f              | 83 3c 30 7f                |
    | cmp dword [rax + 1 * rdi], 0x80              | 83 3c 38 80                |
    | cmp dword [rax + 1 * r8], 0xff               | 42 83 3c 00 ff             |
    | cmp dword [rax + 1 * r9], 0x00               | 42 83 3c 08 00             |
    | cmp dword [rax + 1 * r11], 0x7f              | 42 83 3c 18 7f             |
    | cmp dword [rax + 1 * r12], 0x80              | 42 83 3c 20 80             |
    | cmp dword [rax + 1 * r13], 0xff              | 42 83 3c 28 ff             |
    | cmp dword [rax + 1 * r14], 0x00              | 42 83 3c 30 00             |
    | cmp dword [rax + 2 * rcx], 0x7f              | 83 3c 48 7f                |
    | cmp dword [rax + 4 * rcx], 0x80              | 83 3c 88 80                |
    | cmp dword [rax + 8 * rcx], 0xff              | 83 3c c8 ff                |
    | cmp dword [r8 + 1 * r9], 0x00                | 43 83 3c 08 00             |
    | cmp dword [r8 + 4 * r9], 0x7f                | 43 83 3c 88 7f             |
    | cmp dword [r8 + 8 * r9], 0x80                | 43 83 3c c8 80             |
    | cmp dword [1 * rcx], 0xff                    | 83 3c 0d 00 00 00 00 ff    |
    | cmp dword [2 * rcx], 0x00                    | 83 3c 4d 00 00 00 00 00    |
    | cmp dword [8 * rcx], 0x7f                    | 83 3c cd 00 00 00 00 7f    |
    | cmp dword [1 * r9], 0x80                     | 42 83 3c 0d 00 00 00 00 80 |
    | cmp dword [2 * r9], 0xff                     | 42 83 3c 4d 00 00 00 00 ff |
    | cmp dword [4 * r9], 0x00                     | 42 83 3c 8d 00 00 00 00 00 |
    | cmp dword [r13 + 8 * r12], 0x7f              | 43 83 7c e5 00 7f          |
    | cmp dword [rsp + 4 * r15], 0x80              | 42 83 3c bc 80             |
    | cmp dword [rax + 1 * rcx + 0x00], 0xff       | 83 7c 08 00 ff             |
    | cmp dword [rax + 1 * rcx - 0x00], 0x00       | 83 7c 08 00 00             |
    | cmp dword [rax + 1 * rcx - 0x01], 0x7f       | 83 7c 08 ff 7f             |
    | cmp dword [rax + 1 * rcx + 0x00000001], 0x80 | 83 bc 08 01 00 00 00 80    |
    | cmp dword [rax + 1 * rcx - 0x00000001], 0xff | 83 bc 08 ff ff ff ff ff    |
    | cmp dword [rax + 1 * rcx + 0x7f], 0x00       | 83 7c 08 7f 00             |
    | cmp dword [rax + 1 * rcx + 0x80], 0x7f       | 83 bc 08 80 00 00 00 7f    |
    | cmp dword [rax + 1 * rcx - 0x80], 0x80       | 83 7c 08 80 80             |
    | cmp dword [rax + 1 * rcx - 0x81], 0xff       | 83 bc 08 7f ff ff ff ff    |
    | cmp dword [rax + 1 * rcx + 0xff], 0x00       | 83 bc 08 ff 00 00 00 00    |
    | cmp dword [rax + 1 * rcx + 0x7fffffff], 0x7f | 83 bc 08 ff ff ff 7f 7f    |
    | cmp dword [rax + 1 * rcx - 0x7fffffff], 0x80 | 83 bc 08 01 00 00 80 80    |
    | cmp dword [rax + 1 * rcx - 0x80000000], 0xff | 83 bc 08 00 00 00 80 ff    |
    | cmp dword [r10 + 0x7f], 0x00                 | 41 83 7a 7f 00             |
    | cmp dword [r10 - 0x80], 0x7f                 | 41 83 7a 80 7f             |
    | cmp dword [r10 - 0x81], 0x80                 | 41 83 ba 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_cmp_addr32_imm8():
    encode(CMP_ADDR32_IMM8)


CMP_ADDR32_IMM32 = """
    | -------------------------------------------------- | ----------------------------------- |
    | instruction                                        | encoding                            |
    | -------------------------------------------------- | ----------------------------------- |
    | cmp dword [rax], 0x00000001                        | 81 38 01 00 00 00                   |
    | cmp dword [rcx], 0x00000001                        | 81 39 01 00 00 00                   |
    | cmp dword [rdx], 0x00000001                        | 81 3a 01 00 00 00                   |
    | cmp dword [rbx], 0x00000001                        | 81 3b 01 00 00 00                   |
    | cmp dword [rsp], 0x00000001                        | 81 3c 24 01 00 00 00                |
    | cmp dword [rbp], 0x00000001                        | 81 7d 00 01 00 00 00                |
    | cmp dword [rsi], 0x00000001                        | 81 3e 01 00 00 00                   |
    | cmp dword [rdi], 0x00000001                        | 81 3f 01 00 00 00                   |
    | cmp dword [r8], 0x00000001                         | 41 81 38 01 00 00 00                |
    | cmp dword [r9], 0x00000001                         | 41 81 39 01 00 00 00                |
    | cmp dword [r10], 0x00000001                        | 41 81 3a 01 00 00 00                |
    | cmp dword [r11], 0x00000001                        | 41 81 3b 01 00 00 00                |
    | cmp dword [r12], 0x00000001                        | 41 81 3c 24 01 00 00 00             |
    | cmp dword [r13], 0x00000001                        | 41 81 7d 00 01 00 00 00             |
    | cmp dword [r14], 0x00000001                        | 41 81 3e 01 00 00 00                |
    | cmp dword [r15], 0x00000001                        | 41 81 3f 01 00 00 00                |
    | cmp dword [rax + 1 * rcx], 0x00000001              | 81 3c 08 01 00 00 00                |
    | cmp dword [rcx + 1 * rcx], 0x00000001              | 81 3c 09 01 00 00 00                |
    | cmp dword [rdx + 1 * rcx], 0x00000001              | 81 3c 0a 01 00 00 00                |
    | cmp dword [rbx + 1 * rcx], 0x00000001              | 81 3c 0b 01 00 00 00                |
    | cmp dword [rsp + 1 * rcx], 0x00000001              | 81 3c 0c 01 00 00 00                |
    | cmp dword [rbp + 1 * rcx], 0x00000001              | 81 7c 0d 00 01 00 00 00             |
    | cmp dword [rsi + 1 * rcx], 0x00000001              | 81 3c 0e 01 00 00 00                |
    | cmp dword [rdi + 1 * rcx], 0x00000001              | 81 3c 0f 01 00 00 00                |
    | cmp dword [r8 + 1 * rcx], 0x00000001               | 41 81 3c 08 01 00 00 00             |
    | cmp dword [r9 + 1 * rcx], 0x00000001               | 41 81 3c 09 01 00 00 00             |
    | cmp dword [r10 + 1 * rcx], 0x00000001              | 41 81 3c 0a 01 00 00 00             |
    | cmp dword [r11 + 1 * rcx], 0x00000001              | 41 81 3c 0b 01 00 00 00             |
    | cmp dword [r12 + 1 * rcx], 0x00000001              | 41 81 3c 0c 01 00 00 00             |
    | cmp dword [r13 + 1 * rcx], 0x00000001              | 41 81 7c 0d 00 01 00 00 00          |
    | cmp dword [r14 + 1 * rcx], 0x00000001              | 41 81 3c 0e 01 00 00 00             |
    | cmp dword [r15 + 1 * rcx], 0x00000001              | 41 81 3c 0f 01 00 00 00             |
    | cmp dword [rax + 1 * rax], 0x00000001              | 81 3c 00 01 00 00 00                |
    | cmp dword [rax + 1 * rdx], 0x00000001              | 81 3c 10 01 00 00 00                |
    | cmp dword [rax + 1 * rbx], 0x00000001              | 81 3c 18 01 00 00 00                |
    | cmp dword [rax + 1 * rbp], 0x00000001              | 81 3c 28 01 00 00 00                |
    | cmp dword [rax + 1 * rsi], 0x00000001              | 81 3c 30 01 00 00 00                |
    | cmp dword [rax + 1 * rdi], 0x00000001              | 81 3c 38 01 00 00 00                |
    | cmp dword [rax + 1 * r8], 0x00000001               | 42 81 3c 00 01 00 00 00             |
    | cmp dword [rax + 1 * r9], 0x00000001               | 42 81 3c 08 01 00 00 00             |
    | cmp dword [rax + 1 * r10], 0x00000001              | 42 81 3c 10 01 00 00 00             |
    | cmp dword [rax + 1 * r11], 0x00000001              | 42 81 3c 18 01 00 00 00             |
    | cmp dword [rax + 1 * r12], 0x00000001              | 42 81 3c 20 01 00 00 00             |
    | cmp dword [rax + 1 * r13], 0x00000001              | 42 81 3c 28 01 00 00 00             |
    | cmp dword [rax + 1 * r14], 0x00000001              | 42 81 3c 30 01 00 00 00             |
    | cmp dword [rax + 1 * r15], 0x00000001              | 42 81 3c 38 01 00 00 00             |
    | cmp dword [rax + 2 * rcx], 0x00000001              | 81 3c 48 01 00 00 00                |
    | cmp dword [rax + 4 * rcx], 0x00000001              | 81 3c 88 01 00 00 00                |
    | cmp dword [rax + 8 * rcx], 0x00000001              | 81 3c c8 01 00 00 00                |
    | cmp dword [r8 + 1 * r9], 0x00000001                | 43 81 3c 08 01 00 00 00             |
    | cmp dword [r8 + 2 * r9], 0x00000001                | 43 81 3c 48 01 00 00 00             |
    | cmp dword [r8 + 4 * r9], 0x00000001                | 43 81 3c 88 01 00 00 00             |
    | cmp dword [r8 + 8 * r9], 0x00000001                | 43 81 3c c8 01 00 00 00             |
    | cmp dword [1 * rcx], 0x00000001                    | 81 3c 0d 00 00 00 00 01 00 00 00    |
    | cmp dword [2 * rcx], 0x00000001                    | 81 3c 4d 00 00 00 00 01 00 00 00    |
    | cmp dword [4 * rcx], 0x00000001                    | 81 3c 8d 00 00 00 00 01 00 00 00    |
    | cmp dword [8 * rcx], 0x00000001                    | 81 3c cd 00 00 00 00 01 00 00 00    |
    | cmp dword [1 * r9], 0x00000001                     | 42 81 3c 0d 00 00 00 00 01 00 00 00 |
    | cmp dword [2 * r9], 0x00000001                     | 42 81 3c 4d 00 00 00 00 01 00 00 00 |
    | cmp dword [4 * r9], 0x00000001                     | 42 81 3c 8d 00 00 00 00 01 00 00 00 |
    | cmp dword [8 * r9], 0x00000001                     | 42 81 3c cd 00 00 00 00 01 00 00 00 |
    | cmp dword [r13 + 8 * r12], 0x00000001              | 43 81 7c e5 00 01 00 00 00          |
    | cmp dword [rsp + 4 * r15], 0x00000001              | 42 81 3c bc 01 00 00 00             |
    | cmp dword [rax + 1 * rcx + 0x00], 0x00000001       | 81 7c 08 00 01 00 00 00             |
    | cmp dword [rax + 1 * rcx - 0x00], 0x00000001       | 81 7c 08 00 01 00 00 00             |
    | cmp dword [rax + 1 * rcx + 0x01], 0x00000001       | 81 7c 08 01 01 00 00 00             |
    | cmp dword [rax + 1 * rcx - 0x01], 0x00000001       | 81 7c 08 ff 01 00 00 00             |
    | cmp dword [rax + 1 * rcx + 0x00000001], 0x00000001 | 81 bc 08 01 00 00 00 01 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x00000001], 0x00000001 | 81 bc 08 ff ff ff ff 01 00 00 00    |
    | cmp dword [rax + 1 * rcx + 0x7f], 0x00000001       | 81 7c 08 7f 01 00 00 00             |
    | cmp dword [rax + 1 * rcx - 0x7f], 0x00000001       | 81 7c 08 81 01 00 00 00             |
    | cmp dword [rax + 1 * rcx + 0x80], 0x00000001       | 81 bc 08 80 00 00 00 01 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x80], 0x00000001       | 81 7c 08 80 01 00 00 00             |
    | cmp dword [rax + 1 * rcx - 0x81], 0x00000001       | 81 bc 08 7f ff ff ff 01 00 00 00    |
    | cmp dword [rax + 1 * rcx + 0xff], 0x00000001       | 81 bc 08 ff 00 00 00 01 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0xff], 0x00000001       | 81 bc 08 01 ff ff ff 01 00 00 00    |
    | cmp dword [rax + 1 * rcx + 0x7fffffff], 0x00000001 | 81 bc 08 ff ff ff 7f 01 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x7fffffff], 0x00000001 | 81 bc 08 01 00 00 80 01 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x80000000], 0x00000001 | 81 bc 08 00 00 00 80 01 00 00 00    |
    | cmp dword [r10 + 0x7f], 0x00000001                 | 41 81 7a 7f 01 00 00 00             |
    | cmp dword [r10 + 0x80], 0x00000001                 | 41 81 ba 80 00 00 00 01 00 00 00    |
    | cmp dword [r10 - 0x80], 0x00000001                 | 41 81 7a 80 01 00 00 00             |
    | cmp dword [r10 - 0x81], 0x00000001                 | 41 81 ba 7f ff ff ff 01 00 00 00    |
    | cmp dword [rax], 0x00000000                        | 81 38 00 00 00 00                   |
    | cmp dword [rax], 0x0000007f                        | 81 38 7f 00 00 00                   |
    | cmp dword [rax], 0x00000080                        | 81 38 80 00 00 00                   |
    | cmp dword [rax], 0x000000ff                        | 81 38 ff 00 00 00                   |
    | cmp dword [rax], 0x00000100                        | 81 38 00 01 00 00                   |
    | cmp dword [rax], 0x00007fff                        | 81 38 ff 7f 00 00                   |
    | cmp dword [rax], 0x00008000                        | 81 38 00 80 00 00                   |
    | cmp dword [rax], 0x0000ffff                        | 81 38 ff ff 00 00                   |
    | cmp dword [rax], 0x00010000                        | 81 38 00 00 01 00                   |
    | cmp dword [rax], 0x7fffffff                        | 81 38 ff ff ff 7f                   |
    | cmp dword [rax], 0x80000000                        | 81 38 00 00 00 80                   |
    | cmp dword [rax], 0xffffffff                        | 81 38 ff ff ff ff                   |
    | cmp dword [rcx], 0x0000007f                        | 81 39 7f 00 00 00                   |
    | cmp dword [rdx], 0x00000080                        | 81 3a 80 00 00 00                   |
    | cmp dword [rbx], 0x000000ff                        | 81 3b ff 00 00 00                   |
    | cmp dword [rsp], 0x00000100                        | 81 3c 24 00 01 00 00                |
    | cmp dword [rbp], 0x00007fff                        | 81 7d 00 ff 7f 00 00                |
    | cmp dword [rsi], 0x00008000                        | 81 3e 00 80 00 00                   |
    | cmp dword [rdi], 0x0000ffff                        | 81 3f ff ff 00 00                   |
    | cmp dword [r8], 0x00010000                         | 41 81 38 00 00 01 00                |
    | cmp dword [r9], 0x7fffffff                         | 41 81 39 ff ff ff 7f                |
    | cmp dword [r10], 0x80000000                        | 41 81 3a 00 00 00 80                |
    | cmp dword [r11], 0xffffffff                        | 41 81 3b ff ff ff ff                |
    | cmp dword [r12], 0x00000000                        | 41 81 3c 24 00 00 00 00             |
    | cmp dword [r14], 0x0000007f                        | 41 81 3e 7f 00 00 00                |
    | cmp dword [r15], 0x00000080                        | 41 81 3f 80 00 00 00                |
    | cmp dword [rax + 1 * rcx], 0x000000ff              | 81 3c 08 ff 00 00 00                |
    | cmp dword [rcx + 1 * rcx], 0x00000100              | 81 3c 09 00 01 00 00                |
    | cmp dword [rdx + 1 * rcx], 0x00007fff              | 81 3c 0a ff 7f 00 00                |
    | cmp dword [rbx + 1 * rcx], 0x00008000              | 81 3c 0b 00 80 00 00                |
    | cmp dword [rsp + 1 * rcx], 0x0000ffff              | 81 3c 0c ff ff 00 00                |
    | cmp dword [rbp + 1 * rcx], 0x00010000              | 81 7c 0d 00 00 00 01 00             |
    | cmp dword [rsi + 1 * rcx], 0x7fffffff              | 81 3c 0e ff ff ff 7f                |
    | cmp dword [rdi + 1 * rcx], 0x80000000              | 81 3c 0f 00 00 00 80                |
    | cmp dword [r8 + 1 * rcx], 0xffffffff               | 41 81 3c 08 ff ff ff ff             |
    | cmp dword [r9 + 1 * rcx], 0x00000000               | 41 81 3c 09 00 00 00 00             |
    | cmp dword [r11 + 1 * rcx], 0x0000007f              | 41 81 3c 0b 7f 00 00 00             |
    | cmp dword [r12 + 1 * rcx], 0x00000080              | 41 81 3c 0c 80 00 00 00             |
    | cmp dword [r13 + 1 * rcx], 0x000000ff              | 41 81 7c 0d 00 ff 00 00 00          |
    | cmp dword [r14 + 1 * rcx], 0x00000100              | 41 81 3c 0e 00 01 00 00             |
    | cmp dword [r15 + 1 * rcx], 0x00007fff              | 41 81 3c 0f ff 7f 00 00             |
    | cmp dword [rax + 1 * rax], 0x00008000              | 81 3c 00 00 80 00 00                |
    | cmp dword [rax + 1 * rdx], 0x0000ffff              | 81 3c 10 ff ff 00 00                |
    | cmp dword [rax + 1 * rbx], 0x00010000              | 81 3c 18 00 00 01 00                |
    | cmp dword [rax + 1 * rbp], 0x7fffffff              | 81 3c 28 ff ff ff 7f                |
    | cmp dword [rax + 1 * rsi], 0x80000000              | 81 3c 30 00 00 00 80                |
    | cmp dword [rax + 1 * rdi], 0xffffffff              | 81 3c 38 ff ff ff ff                |
    | cmp dword [rax + 1 * r8], 0x00000000               | 42 81 3c 00 00 00 00 00             |
    | cmp dword [rax + 1 * r10], 0x0000007f              | 42 81 3c 10 7f 00 00 00             |
    | cmp dword [rax + 1 * r11], 0x00000080              | 42 81 3c 18 80 00 00 00             |
    | cmp dword [rax + 1 * r12], 0x000000ff              | 42 81 3c 20 ff 00 00 00             |
    | cmp dword [rax + 1 * r13], 0x00000100              | 42 81 3c 28 00 01 00 00             |
    | cmp dword [rax + 1 * r14], 0x00007fff              | 42 81 3c 30 ff 7f 00 00             |
    | cmp dword [rax + 1 * r15], 0x00008000              | 42 81 3c 38 00 80 00 00             |
    | cmp dword [rax + 2 * rcx], 0x0000ffff              | 81 3c 48 ff ff 00 00                |
    | cmp dword [rax + 4 * rcx], 0x00010000              | 81 3c 88 00 00 01 00                |
    | cmp dword [rax + 8 * rcx], 0x7fffffff              | 81 3c c8 ff ff ff 7f                |
    | cmp dword [r8 + 1 * r9], 0x80000000                | 43 81 3c 08 00 00 00 80             |
    | cmp dword [r8 + 2 * r9], 0xffffffff                | 43 81 3c 48 ff ff ff ff             |
    | cmp dword [r8 + 4 * r9], 0x00000000                | 43 81 3c 88 00 00 00 00             |
    | cmp dword [1 * rcx], 0x0000007f                    | 81 3c 0d 00 00 00 00 7f 00 00 00    |
    | cmp dword [2 * rcx], 0x00000080                    | 81 3c 4d 00 00 00 00 80 00 00 00    |
    | cmp dword [4 * rcx], 0x000000ff                    | 81 3c 8d 00 00 00 00 ff 00 00 00    |
    | cmp dword [8 * rcx], 0x00000100                    | 81 3c cd 00 00 00 00 00 01 00 00    |
    | cmp dword [1 * r9], 0x00007fff                     | 42 81 3c 0d 00 00 00 00 ff 7f 00 00 |
    | cmp dword [2 * r9], 0x00008000                     | 42 81 3c 4d 00 00 00 00 00 80 00 00 |
    | cmp dword [4 * r9], 0x0000ffff                     | 42 81 3c 8d 00 00 00 00 ff ff 00 00 |
    | cmp dword [8 * r9], 0x00010000                     | 42 81 3c cd 00 00 00 00 00 00 01 00 |
    | cmp dword [r13 + 8 * r12], 0x7fffffff              | 43 81 7c e5 00 ff ff ff 7f          |
    | cmp dword [rsp + 4 * r15], 0x80000000              | 42 81 3c bc 00 00 00 80             |
    | cmp dword [rax + 1 * rcx + 0x00], 0xffffffff       | 81 7c 08 00 ff ff ff ff             |
    | cmp dword [rax + 1 * rcx - 0x00], 0x00000000       | 81 7c 08 00 00 00 00 00             |
    | cmp dword [rax + 1 * rcx - 0x01], 0x0000007f       | 81 7c 08 ff 7f 00 00 00             |
    | cmp dword [rax + 1 * rcx + 0x00000001], 0x00000080 | 81 bc 08 01 00 00 00 80 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x00000001], 0x000000ff | 81 bc 08 ff ff ff ff ff 00 00 00    |
    | cmp dword [rax + 1 * rcx + 0x7f], 0x00000100       | 81 7c 08 7f 00 01 00 00             |
    | cmp dword [rax + 1 * rcx - 0x7f], 0x00007fff       | 81 7c 08 81 ff 7f 00 00             |
    | cmp dword [rax + 1 * rcx + 0x80], 0x00008000       | 81 bc 08 80 00 00 00 00 80 00 00    |
    | cmp dword [rax + 1 * rcx - 0x80], 0x0000ffff       | 81 7c 08 80 ff ff 00 00             |
    | cmp dword [rax + 1 * rcx - 0x81], 0x00010000       | 81 bc 08 7f ff ff ff 00 00 01 00    |
    | cmp dword [rax + 1 * rcx + 0xff], 0x7fffffff       | 81 bc 08 ff 00 00 00 ff ff ff 7f    |
    | cmp dword [rax + 1 * rcx - 0xff], 0x80000000       | 81 bc 08 01 ff ff ff 00 00 00 80    |
    | cmp dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff | 81 bc 08 ff ff ff 7f ff ff ff ff    |
    | cmp dword [rax + 1 * rcx - 0x7fffffff], 0x00000000 | 81 bc 08 01 00 00 80 00 00 00 00    |
    | cmp dword [r10 + 0x7f], 0x0000007f                 | 41 81 7a 7f 7f 00 00 00             |
    | cmp dword [r10 + 0x80], 0x00000080                 | 41 81 ba 80 00 00 00 80 00 00 00    |
    | cmp dword [r10 - 0x80], 0x000000ff                 | 41 81 7a 80 ff 00 00 00             |
    | cmp dword [r10 - 0x81], 0x00000100                 | 41 81 ba 7f ff ff ff 00 01 00 00    |
    | -------------------------------------------------- | ----------------------------------- |
"""


def can_encode_cmp_addr32_imm32():
    encode(CMP_ADDR32_IMM32)


CMP_ADDR32_REG32 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | cmp dword [rax], ecx                         | 39 08                   |
    | cmp dword [rcx], ecx                         | 39 09                   |
    | cmp dword [rdx], ecx                         | 39 0a                   |
    | cmp dword [rbx], ecx                         | 39 0b                   |
    | cmp dword [rsp], ecx                         | 39 0c 24                |
    | cmp dword [rbp], ecx                         | 39 4d 00                |
    | cmp dword [rsi], ecx                         | 39 0e                   |
    | cmp dword [rdi], ecx                         | 39 0f                   |
    | cmp dword [r8], ecx                          | 41 39 08                |
    | cmp dword [r9], ecx                          | 41 39 09                |
    | cmp dword [r10], ecx                         | 41 39 0a                |
    | cmp dword [r11], ecx                         | 41 39 0b                |
    | cmp dword [r12], ecx                         | 41 39 0c 24             |
    | cmp dword [r13], ecx                         | 41 39 4d 00             |
    | cmp dword [r14], ecx                         | 41 39 0e                |
    | cmp dword [r15], ecx                         | 41 39 0f                |
    | cmp dword [rax + 1 * rcx], ecx               | 39 0c 08                |
    | cmp dword [rcx + 1 * rcx], ecx               | 39 0c 09                |
    | cmp dword [rdx + 1 * rcx], ecx               | 39 0c 0a                |
    | cmp dword [rbx + 1 * rcx], ecx               | 39 0c 0b                |
    | cmp dword [rsp + 1 * rcx], ecx               | 39 0c 0c                |
    | cmp dword [rbp + 1 * rcx], ecx               | 39 4c 0d 00             |
    | cmp dword [rsi + 1 * rcx], ecx               | 39 0c 0e                |
    | cmp dword [rdi + 1 * rcx], ecx               | 39 0c 0f                |
    | cmp dword [r8 + 1 * rcx], ecx                | 41 39 0c 08             |
    | cmp dword [r9 + 1 * rcx], ecx                | 41 39 0c 09             |
    | cmp dword [r10 + 1 * rcx], ecx               | 41 39 0c 0a             |
    | cmp dword [r11 + 1 * rcx], ecx               | 41 39 0c 0b             |
    | cmp dword [r12 + 1 * rcx], ecx               | 41 39 0c 0c             |
    | cmp dword [r13 + 1 * rcx], ecx               | 41 39 4c 0d 00          |
    | cmp dword [r14 + 1 * rcx], ecx               | 41 39 0c 0e             |
    | cmp dword [r15 + 1 * rcx], ecx               | 41 39 0c 0f             |
    | cmp dword [rax + 1 * rax], ecx               | 39 0c 00                |
    | cmp dword [rax + 1 * rdx], ecx               | 39 0c 10                |
    | cmp dword [rax + 1 * rbx], ecx               | 39 0c 18                |
    | cmp dword [rax + 1 * rbp], ecx               | 39 0c 28                |
    | cmp dword [rax + 1 * rsi], ecx               | 39 0c 30                |
    | cmp dword [rax + 1 * rdi], ecx               | 39 0c 38                |
    | cmp dword [rax + 1 * r8], ecx                | 42 39 0c 00             |
    | cmp dword [rax + 1 * r9], ecx                | 42 39 0c 08             |
    | cmp dword [rax + 1 * r10], ecx               | 42 39 0c 10             |
    | cmp dword [rax + 1 * r11], ecx               | 42 39 0c 18             |
    | cmp dword [rax + 1 * r12], ecx               | 42 39 0c 20             |
    | cmp dword [rax + 1 * r13], ecx               | 42 39 0c 28             |
    | cmp dword [rax + 1 * r14], ecx               | 42 39 0c 30             |
    | cmp dword [rax + 1 * r15], ecx               | 42 39 0c 38             |
    | cmp dword [rax + 2 * rcx], ecx               | 39 0c 48                |
    | cmp dword [rax + 4 * rcx], ecx               | 39 0c 88                |
    | cmp dword [rax + 8 * rcx], ecx               | 39 0c c8                |
    | cmp dword [r8 + 1 * r9], ecx                 | 43 39 0c 08             |
    | cmp dword [r8 + 2 * r9], ecx                 | 43 39 0c 48             |
    | cmp dword [r8 + 4 * r9], ecx                 | 43 39 0c 88             |
    | cmp dword [r8 + 8 * r9], ecx                 | 43 39 0c c8             |
    | cmp dword [1 * rcx], ecx                     | 39 0c 0d 00 00 00 00    |
    | cmp dword [2 * rcx], ecx                     | 39 0c 4d 00 00 00 00    |
    | cmp dword [4 * rcx], ecx                     | 39 0c 8d 00 00 00 00    |
    | cmp dword [8 * rcx], ecx                     | 39 0c cd 00 00 00 00    |
    | cmp dword [1 * r9], ecx                      | 42 39 0c 0d 00 00 00 00 |
    | cmp dword [2 * r9], ecx                      | 42 39 0c 4d 00 00 00 00 |
    | cmp dword [4 * r9], ecx                      | 42 39 0c 8d 00 00 00 00 |
    | cmp dword [8 * r9], ecx                      | 42 39 0c cd 00 00 00 00 |
    | cmp dword [r13 + 8 * r12], ecx               | 43 39 4c e5 00          |
    | cmp dword [rsp + 4 * r15], ecx               | 42 39 0c bc             |
    | cmp dword [rax + 1 * rcx + 0x00], ecx        | 39 4c 08 00             |
    | cmp dword [rax + 1 * rcx - 0x00], ecx        | 39 4c 08 00             |
    | cmp dword [rax + 1 * rcx + 0x01], ecx        | 39 4c 08 01             |
    | cmp dword [rax + 1 * rcx - 0x01], ecx        | 39 4c 08 ff             |
    | cmp dword [rax + 1 * rcx + 0x00000001], ecx  | 39 8c 08 01 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x00000001], ecx  | 39 8c 08 ff ff ff ff    |
    | cmp dword [rax + 1 * rcx + 0x7f], ecx        | 39 4c 08 7f             |
    | cmp dword [rax + 1 * rcx - 0x7f], ecx        | 39 4c 08 81             |
    | cmp dword [rax + 1 * rcx + 0x80], ecx        | 39 8c 08 80 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x80], ecx        | 39 4c 08 80             |
    | cmp dword [rax + 1 * rcx - 0x81], ecx        | 39 8c 08 7f ff ff ff    |
    | cmp dword [rax + 1 * rcx + 0xff], ecx        | 39 8c 08 ff 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0xff], ecx        | 39 8c 08 01 ff ff ff    |
    | cmp dword [rax + 1 * rcx + 0x7fffffff], ecx  | 39 8c 08 ff ff ff 7f    |
    | cmp dword [rax + 1 * rcx - 0x7fffffff], ecx  | 39 8c 08 01 00 00 80    |
    | cmp dword [rax + 1 * rcx - 0x80000000], ecx  | 39 8c 08 00 00 00 80    |
    | cmp dword [r10 + 0x7f], ecx                  | 41 39 4a 7f             |
    | cmp dword [r10 + 0x80], ecx                  | 41 39 8a 80 00 00 00    |
    | cmp dword [r10 - 0x80], ecx                  | 41 39 4a 80             |
    | cmp dword [r10 - 0x81], ecx                  | 41 39 8a 7f ff ff ff    |
    | cmp dword [rax], eax                         | 39 00                   |
    | cmp dword [rax], edx                         | 39 10                   |
    | cmp dword [rax], ebx                         | 39 18                   |
    | cmp dword [rax], esp                         | 39 20                   |
    | cmp dword [rax], ebp                         | 39 28                   |
    | cmp dword [rax], esi                         | 39 30                   |
    | cmp dword [rax], edi                         | 39 38                   |
    | cmp dword [rax], r8d                         | 44 39 00                |
    | cmp dword [rax], r9d                         | 44 39 08                |
    | cmp dword [rax], r10d                        | 44 39 10                |
    | cmp dword [rax], r11d                        | 44 39 18                |
    | cmp dword [rax], r12d                        | 44 39 20                |
    | cmp dword [rax], r13d                        | 44 39 28                |
    | cmp dword [rax], r14d                        | 44 39 30                |
    | cmp dword [rax], r15d                        | 44 39 38                |
    | cmp dword [rcx], edx                         | 39 11                   |
    | cmp dword [rdx], ebx                         | 39 1a                   |
    | cmp dword [rbx], esp                         | 39 23                   |
    | cmp dword [rsp], ebp                         | 39 2c 24                |
    | cmp dword [rbp], esi                         | 39 75 00                |
    | cmp dword [rsi], edi                         | 39 3e                   |
    | cmp dword [rdi], r8d                         | 44 39 07                |
    | cmp dword [r8], r9d                          | 45 39 08                |
    | cmp dword [r9], r10d                         | 45 39 11                |
    | cmp dword [r10], r11d                        | 45 39 1a                |
    | cmp dword [r11], r12d                        | 45 39 23                |
    | cmp dword [r12], r13d                        | 45 39 2c 24             |
    | cmp dword [r13], r14d                        | 45 39 75 00             |
    | cmp dword [r14], r15d                        | 45 39 3e                |
    | cmp dword [r15], eax                         | 41 39 07                |
    | cmp dword [rcx + 1 * rcx], edx               | 39 14 09                |
    | cmp dword [rdx + 1 * rcx], ebx               | 39 1c 0a                |
    | cmp dword [rbx + 1 * rcx], esp               | 39 24 0b                |
    | cmp dword [rsp + 1 * rcx], ebp               | 39 2c 0c                |
    | cmp dword [rbp + 1 * rcx], esi               | 39 74 0d 00             |
    | cmp dword [rsi + 1 * rcx], edi               | 39 3c 0e                |
    | cmp dword [rdi + 1 * rcx], r8d               | 44 39 04 0f             |
    | cmp dword [r8 + 1 * rcx], r9d                | 45 39 0c 08             |
    | cmp dword [r9 + 1 * rcx], r10d               | 45 39 14 09             |
    | cmp dword [r10 + 1 * rcx], r11d              | 45 39 1c 0a             |
    | cmp dword [r11 + 1 * rcx], r12d              | 45 39 24 0b             |
    | cmp dword [r12 + 1 * rcx], r13d              | 45 39 2c 0c             |
    | cmp dword [r13 + 1 * rcx], r14d              | 45 39 74 0d 00          |
    | cmp dword [r14 + 1 * rcx], r15d              | 45 39 3c 0e             |
    | cmp dword [r15 + 1 * rcx], eax               | 41 39 04 0f             |
    | cmp dword [rax + 1 * rdx], edx               | 39 14 10                |
    | cmp dword [rax + 1 * rbx], ebx               | 39 1c 18                |
    | cmp dword [rax + 1 * rbp], esp               | 39 24 28                |
    | cmp dword [rax + 1 * rsi], ebp               | 39 2c 30                |
    | cmp dword [rax + 1 * rdi], esi               | 39 34 38                |
    | cmp dword [rax + 1 * r8], edi                | 42 39 3c 00             |
    | cmp dword [rax + 1 * r9], r8d                | 46 39 04 08             |
    | cmp dword [rax + 1 * r10], r9d               | 46 39 0c 10             |
    | cmp dword [rax + 1 * r11], r10d              | 46 39 14 18             |
    | cmp dword [rax + 1 * r12], r11d              | 46 39 1c 20             |
    | cmp dword [rax + 1 * r13], r12d              | 46 39 24 28             |
    | cmp dword [rax + 1 * r14], r13d              | 46 39 2c 30             |
    | cmp dword [rax + 1 * r15], r14d              | 46 39 34 38             |
    | cmp dword [rax + 2 * rcx], r15d              | 44 39 3c 48             |
    | cmp dword [rax + 4 * rcx], eax               | 39 04 88                |
    | cmp dword [r8 + 1 * r9], edx                 | 43 39 14 08             |
    | cmp dword [r8 + 2 * r9], ebx                 | 43 39 1c 48             |
    | cmp dword [r8 + 4 * r9], esp                 | 43 39 24 88             |
    | cmp dword [r8 + 8 * r9], ebp                 | 43 39 2c c8             |
    | cmp dword [1 * rcx], esi                     | 39 34 0d 00 00 00 00    |
    | cmp dword [2 * rcx], edi                     | 39 3c 4d 00 00 00 00    |
    | cmp dword [4 * rcx], r8d                     | 44 39 04 8d 00 00 00 00 |
    | cmp dword [8 * rcx], r9d                     | 44 39 0c cd 00 00 00 00 |
    | cmp dword [1 * r9], r10d                     | 46 39 14 0d 00 00 00 00 |
    | cmp dword [2 * r9], r11d                     | 46 39 1c 4d 00 00 00 00 |
    | cmp dword [4 * r9], r12d                     | 46 39 24 8d 00 00 00 00 |
    | cmp dword [8 * r9], r13d                     | 46 39 2c cd 00 00 00 00 |
    | cmp dword [r13 + 8 * r12], r14d              | 47 39 74 e5 00          |
    | cmp dword [rsp + 4 * r15], r15d              | 46 39 3c bc             |
    | cmp dword [rax + 1 * rcx + 0x00], eax        | 39 44 08 00             |
    | cmp dword [rax + 1 * rcx + 0x01], edx        | 39 54 08 01             |
    | cmp dword [rax + 1 * rcx - 0x01], ebx        | 39 5c 08 ff             |
    | cmp dword [rax + 1 * rcx + 0x00000001], esp  | 39 a4 08 01 00 00 00    |
    | cmp dword [rax + 1 * rcx - 0x00000001], ebp  | 39 ac 08 ff ff ff ff    |
    | cmp dword [rax + 1 * rcx + 0x7f], esi        | 39 74 08 7f             |
    | cmp dword [rax + 1 * rcx - 0x7f], edi        | 39 7c 08 81             |
    | cmp dword [rax + 1 * rcx + 0x80], r8d        | 44 39 84 08 80 00 00 00 |
    | cmp dword [rax + 1 * rcx - 0x80], r9d        | 44 39 4c 08 80          |
    | cmp dword [rax + 1 * rcx - 0x81], r10d       | 44 39 94 08 7f ff ff ff |
    | cmp dword [rax + 1 * rcx + 0xff], r11d       | 44 39 9c 08 ff 00 00 00 |
    | cmp dword [rax + 1 * rcx - 0xff], r12d       | 44 39 a4 08 01 ff ff ff |
    | cmp dword [rax + 1 * rcx + 0x7fffffff], r13d | 44 39 ac 08 ff ff ff 7f |
    | cmp dword [rax + 1 * rcx - 0x7fffffff], r14d | 44 39 b4 08 01 00 00 80 |
    | cmp dword [rax + 1 * rcx - 0x80000000], r15d | 44 39 bc 08 00 00 00 80 |
    | cmp dword [r10 + 0x7f], eax                  | 41 39 42 7f             |
    | cmp dword [r10 - 0x80], edx                  | 41 39 52 80             |
    | cmp dword [r10 - 0x81], ebx                  | 41 39 9a 7f ff ff ff    |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_cmp_addr32_reg32():
    encode(CMP_ADDR32_REG32)


CMP_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | cmp word [rax], 0x01                        | 66 83 38 01                   |
    | cmp word [rcx], 0x01                        | 66 83 39 01                   |
    | cmp word [rdx], 0x01                        | 66 83 3a 01                   |
    | cmp word [rbx], 0x01                        | 66 83 3b 01                   |
    | cmp word [rsp], 0x01                        | 66 83 3c 24 01                |
    | cmp word [rbp], 0x01                        | 66 83 7d 00 01                |
    | cmp word [rsi], 0x01                        | 66 83 3e 01                   |
    | cmp word [rdi], 0x01                        | 66 83 3f 01                   |
    | cmp word [r8], 0x01                         | 66 41 83 38 01                |
    | cmp word [r9], 0x01                         | 66 41 83 39 01                |
    | cmp word [r10], 0x01                        | 66 41 83 3a 01                |
    | cmp word [r11], 0x01                        | 66 41 83 3b 01                |
    | cmp word [r12], 0x01                        | 66 41 83 3c 24 01             |
    | cmp word [r13], 0x01                        | 66 41 83 7d 00 01             |
    | cmp word [r14], 0x01                        | 66 41 83 3e 01                |
    | cmp word [r15], 0x01                        | 66 41 83 3f 01                |
    | cmp word [rax + 1 * rcx], 0x01              | 66 83 3c 08 01                |
    | cmp word [rcx + 1 * rcx], 0x01              | 66 83 3c 09 01                |
    | cmp word [rdx + 1 * rcx], 0x01              | 66 83 3c 0a 01                |
    | cmp word [rbx + 1 * rcx], 0x01              | 66 83 3c 0b 01                |
    | cmp word [rsp + 1 * rcx], 0x01              | 66 83 3c 0c 01                |
    | cmp word [rbp + 1 * rcx], 0x01              | 66 83 7c 0d 00 01             |
    | cmp word [rsi + 1 * rcx], 0x01              | 66 83 3c 0e 01                |
    | cmp word [rdi + 1 * rcx], 0x01              | 66 83 3c 0f 01                |
    | cmp word [r8 + 1 * rcx], 0x01               | 66 41 83 3c 08 01             |
    | cmp word [r9 + 1 * rcx], 0x01               | 66 41 83 3c 09 01             |
    | cmp word [r10 + 1 * rcx], 0x01              | 66 41 83 3c 0a 01             |
    | cmp word [r11 + 1 * rcx], 0x01              | 66 41 83 3c 0b 01             |
    | cmp word [r12 + 1 * rcx], 0x01              | 66 41 83 3c 0c 01             |
    | cmp word [r13 + 1 * rcx], 0x01              | 66 41 83 7c 0d 00 01          |
    | cmp word [r14 + 1 * rcx], 0x01              | 66 41 83 3c 0e 01             |
    | cmp word [r15 + 1 * rcx], 0x01              | 66 41 83 3c 0f 01             |
    | cmp word [rax + 1 * rax], 0x01              | 66 83 3c 00 01                |
    | cmp word [rax + 1 * rdx], 0x01              | 66 83 3c 10 01                |
    | cmp word [rax + 1 * rbx], 0x01              | 66 83 3c 18 01                |
    | cmp word [rax + 1 * rbp], 0x01              | 66 83 3c 28 01                |
    | cmp word [rax + 1 * rsi], 0x01              | 66 83 3c 30 01                |
    | cmp word [rax + 1 * rdi], 0x01              | 66 83 3c 38 01                |
    | cmp word [rax + 1 * r8], 0x01               | 66 42 83 3c 00 01             |
    | cmp word [rax + 1 * r9], 0x01               | 66 42 83 3c 08 01             |
    | cmp word [rax + 1 * r10], 0x01              | 66 42 83 3c 10 01             |
    | cmp word [rax + 1 * r11], 0x01              | 66 42 83 3c 18 01             |
    | cmp word [rax + 1 * r12], 0x01              | 66 42 83 3c 20 01             |
    | cmp word [rax + 1 * r13], 0x01              | 66 42 83 3c 28 01             |
    | cmp word [rax + 1 * r14], 0x01              | 66 42 83 3c 30 01             |
    | cmp word [rax + 1 * r15], 0x01              | 66 42 83 3c 38 01             |
    | cmp word [rax + 2 * rcx], 0x01              | 66 83 3c 48 01                |
    | cmp word [rax + 4 * rcx], 0x01              | 66 83 3c 88 01                |
    | cmp word [rax + 8 * rcx], 0x01              | 66 83 3c c8 01                |
    | cmp word [r8 + 1 * r9], 0x01                | 66 43 83 3c 08 01             |
    | cmp word [r8 + 2 * r9], 0x01                | 66 43 83 3c 48 01             |
    | cmp word [r8 + 4 * r9], 0x01                | 66 43 83 3c 88 01             |
    | cmp word [r8 + 8 * r9], 0x01                | 66 43 83 3c c8 01             |
    | cmp word [1 * rcx], 0x01                    | 66 83 3c 0d 00 00 00 00 01    |
    | cmp word [2 * rcx], 0x01                    | 66 83 3c 4d 00 00 00 00 01    |
    | cmp word [4 * rcx], 0x01                    | 66 83 3c 8d 00 00 00 00 01    |
    | cmp word [8 * rcx], 0x01                    | 66 83 3c cd 00 00 00 00 01    |
    | cmp word [1 * r9], 0x01                     | 66 42 83 3c 0d 00 00 00 00 01 |
    | cmp word [2 * r9], 0x01                     | 66 42 83 3c 4d 00 00 00 00 01 |
    | cmp word [4 * r9], 0x01                     | 66 42 83 3c 8d 00 00 00 00 01 |
    | cmp word [8 * r9], 0x01                     | 66 42 83 3c cd 00 00 00 00 01 |
    | cmp word [r13 + 8 * r12], 0x01              | 66 43 83 7c e5 00 01          |
    | cmp word [rsp + 4 * r15], 0x01              | 66 42 83 3c bc 01             |
    | cmp word [rax + 1 * rcx + 0x00], 0x01       | 66 83 7c 08 00 01             |
    | cmp word [rax + 1 * rcx - 0x00], 0x01       | 66 83 7c 08 00 01             |
    | cmp word [rax + 1 * rcx + 0x01], 0x01       | 66 83 7c 08 01 01             |
    | cmp word [rax + 1 * rcx - 0x01], 0x01       | 66 83 7c 08 ff 01             |
    | cmp word [rax + 1 * rcx + 0x00000001], 0x01 | 66 83 bc 08 01 00 00 00 01    |
    | cmp word [rax + 1 * rcx - 0x00000001], 0x01 | 66 83 bc 08 ff ff ff ff 01    |
    | cmp word [rax + 1 * rcx + 0x7f], 0x01       | 66 83 7c 08 7f 01             |
    | cmp word [rax + 1 * rcx - 0x7f], 0x01       | 66 83 7c 08 81 01             |
    | cmp word [rax + 1 * rcx + 0x80], 0x01       | 66 83 bc 08 80 00 00 00 01    |
    | cmp word [rax + 1 * rcx - 0x80], 0x01       | 66 83 7c 08 80 01             |
    | cmp word [rax + 1 * rcx - 0x81], 0x01       | 66 83 bc 08 7f ff ff ff 01    |
    | cmp word [rax + 1 * rcx + 0xff], 0x01       | 66 83 bc 08 ff 00 00 00 01    |
    | cmp word [rax + 1 * rcx - 0xff], 0x01       | 66 83 bc 08 01 ff ff ff 01    |
    | cmp word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 83 bc 08 ff ff ff 7f 01    |
    | cmp word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 83 bc 08 01 00 00 80 01    |
    | cmp word [rax + 1 * rcx - 0x80000000], 0x01 | 66 83 bc 08 00 00 00 80 01    |
    | cmp word [r10 + 0x7f], 0x01                 | 66 41 83 7a 7f 01             |
    | cmp word [r10 + 0x80], 0x01                 | 66 41 83 ba 80 00 00 00 01    |
    | cmp word [r10 - 0x80], 0x01                 | 66 41 83 7a 80 01             |
    | cmp word [r10 - 0x81], 0x01                 | 66 41 83 ba 7f ff ff ff 01    |
    | cmp word [rax], 0x00                        | 66 83 38 00                   |
    | cmp word [rax], 0x7f                        | 66 83 38 7f                   |
    | cmp word [rax], 0x80                        | 66 83 38 80                   |
    | cmp word [rax], 0xff                        | 66 83 38 ff                   |
    | cmp word [rcx], 0x7f                        | 66 83 39 7f                   |
    | cmp word [rdx], 0x80                        | 66 83 3a 80                   |
    | cmp word [rbx], 0xff                        | 66 83 3b ff                   |
    | cmp word [rsp], 0x00                        | 66 83 3c 24 00                |
    | cmp word [rsi], 0x7f                        | 66 83 3e 7f                   |
    | cmp word [rdi], 0x80                        | 66 83 3f 80                   |
    | cmp word [r8], 0xff                         | 66 41 83 38 ff                |
    | cmp word [r9], 0x00                         | 66 41 83 39 00                |
    | cmp word [r11], 0x7f                        | 66 41 83 3b 7f                |
    | cmp word [r12], 0x80                        | 66 41 83 3c 24 80             |
    | cmp word [r13], 0xff                        | 66 41 83 7d 00 ff             |
    | cmp word [r14], 0x00                        | 66 41 83 3e 00                |
    | cmp word [rax + 1 * rcx], 0x7f              | 66 83 3c 08 7f                |
    | cmp word [rcx + 1 * rcx], 0x80              | 66 83 3c 09 80                |
    | cmp word [rdx + 1 * rcx], 0xff              | 66 83 3c 0a ff                |
    | cmp word [rbx + 1 * rcx], 0x00              | 66 83 3c 0b 00                |
    | cmp word [rbp + 1 * rcx], 0x7f              | 66 83 7c 0d 00 7f             |
    | cmp word [rsi + 1 * rcx], 0x80              | 66 83 3c 0e 80                |
    | cmp word [rdi + 1 * rcx], 0xff              | 66 83 3c 0f ff                |
    | cmp word [r8 + 1 * rcx], 0x00               | 66 41 83 3c 08 00             |
    | cmp word [r10 + 1 * rcx], 0x7f              | 66 41 83 3c 0a 7f             |
    | cmp word [r11 + 1 * rcx], 0x80              | 66 41 83 3c 0b 80             |
    | cmp word [r12 + 1 * rcx], 0xff              | 66 41 83 3c 0c ff             |
    | cmp word [r13 + 1 * rcx], 0x00              | 66 41 83 7c 0d 00 00          |
    | cmp word [r15 + 1 * rcx], 0x7f              | 66 41 83 3c 0f 7f             |
    | cmp word [rax + 1 * rax], 0x80              | 66 83 3c 00 80                |
    | cmp word [rax + 1 * rdx], 0xff              | 66 83 3c 10 ff                |
    | cmp word [rax + 1 * rbx], 0x00              | 66 83 3c 18 00                |
    | cmp word [rax + 1 * rsi], 0x7f              | 66 83 3c 30 7f                |
    | cmp word [rax + 1 * rdi], 0x80              | 66 83 3c 38 80                |
    | cmp word [rax + 1 * r8], 0xff               | 66 42 83 3c 00 ff             |
    | cmp word [rax + 1 * r9], 0x00               | 66 42 83 3c 08 00             |
    | cmp word [rax + 1 * r11], 0x7f              | 66 42 83 3c 18 7f             |
    | cmp word [rax + 1 * r12], 0x80              | 66 42 83 3c 20 80             |
    | cmp word [rax + 1 * r13], 0xff              | 66 42 83 3c 28 ff             |
    | cmp word [rax + 1 * r14], 0x00              | 66 42 83 3c 30 00             |
    | cmp word [rax + 2 * rcx], 0x7f              | 66 83 3c 48 7f                |
    | cmp word [rax + 4 * rcx], 0x80              | 66 83 3c 88 80                |
    | cmp word [rax + 8 * rcx], 0xff              | 66 83 3c c8 ff                |
    | cmp word [r8 + 1 * r9], 0x00                | 66 43 83 3c 08 00             |
    | cmp word [r8 + 4 * r9], 0x7f                | 66 43 83 3c 88 7f             |
    | cmp word [r8 + 8 * r9], 0x80                | 66 43 83 3c c8 80             |
    | cmp word [1 * rcx], 0xff                    | 66 83 3c 0d 00 00 00 00 ff    |
    | cmp word [2 * rcx], 0x00                    | 66 83 3c 4d 00 00 00 00 00    |
    | cmp word [8 * rcx], 0x7f                    | 66 83 3c cd 00 00 00 00 7f    |
    | cmp word [1 * r9], 0x80                     | 66 42 83 3c 0d 00 00 00 00 80 |
    | cmp word [2 * r9], 0xff                     | 66 42 83 3c 4d 00 00 00 00 ff |
    | cmp word [4 * r9], 0x00                     | 66 42 83 3c 8d 00 00 00 00 00 |
    | cmp word [r13 + 8 * r12], 0x7f              | 66 43 83 7c e5 00 7f          |
    | cmp word [rsp + 4 * r15], 0x80              | 66 42 83 3c bc 80             |
    | cmp word [rax + 1 * rcx + 0x00], 0xff       | 66 83 7c 08 00 ff             |
    | cmp word [rax + 1 * rcx - 0x00], 0x00       | 66 83 7c 08 00 00             |
    | cmp word [rax + 1 * rcx - 0x01], 0x7f       | 66 83 7c 08 ff 7f             |
    | cmp word [rax + 1 * rcx + 0x00000001], 0x80 | 66 83 bc 08 01 00 00 00 80    |
    | cmp word [rax + 1 * rcx - 0x00000001], 0xff | 66 83 bc 08 ff ff ff ff ff    |
    | cmp word [rax + 1 * rcx + 0x7f], 0x00       | 66 83 7c 08 7f 00             |
    | cmp word [rax + 1 * rcx + 0x80], 0x7f       | 66 83 bc 08 80 00 00 00 7f    |
    | cmp word [rax + 1 * rcx - 0x80], 0x80       | 66 83 7c 08 80 80             |
    | cmp word [rax + 1 * rcx - 0x81], 0xff       | 66 83 bc 08 7f ff ff ff ff    |
    | cmp word [rax + 1 * rcx + 0xff], 0x00       | 66 83 bc 08 ff 00 00 00 00    |
    | cmp word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 83 bc 08 ff ff ff 7f 7f    |
    | cmp word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 83 bc 08 01 00 00 80 80    |
    | cmp word [rax + 1 * rcx - 0x80000000], 0xff | 66 83 bc 08 00 00 00 80 ff    |
    | cmp word [r10 + 0x7f], 0x00                 | 66 41 83 7a 7f 00             |
    | cmp word [r10 - 0x80], 0x7f                 | 66 41 83 7a 80 7f             |
    | cmp word [r10 - 0x81], 0x80                 | 66 41 83 ba 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_cmp_addr16_imm8():
    encode(CMP_ADDR16_IMM8)


CMP_ADDR16_IMM16 = """
    | --------------------------------------------- | -------------------------------- |
    | instruction                                   | encoding                         |
    | --------------------------------------------- | -------------------------------- |
    | cmp word [rax], 0x0001                        | 66 81 38 01 00                   |
    | cmp word [rcx], 0x0001                        | 66 81 39 01 00                   |
    | cmp word [rdx], 0x0001                        | 66 81 3a 01 00                   |
    | cmp word [rbx], 0x0001                        | 66 81 3b 01 00                   |
    | cmp word [rsp], 0x0001                        | 66 81 3c 24 01 00                |
    | cmp word [rbp], 0x0001                        | 66 81 7d 00 01 00                |
    | cmp word [rsi], 0x0001                        | 66 81 3e 01 00                   |
    | cmp word [rdi], 0x0001                        | 66 81 3f 01 00                   |
    | cmp word [r8], 0x0001                         | 66 41 81 38 01 00                |
    | cmp word [r9], 0x0001                         | 66 41 81 39 01 00                |
    | cmp word [r10], 0x0001                        | 66 41 81 3a 01 00                |
    | cmp word [r11], 0x0001                        | 66 41 81 3b 01 00                |
    | cmp word [r12], 0x0001                        | 66 41 81 3c 24 01 00             |
    | cmp word [r13], 0x0001                        | 66 41 81 7d 00 01 00             |
    | cmp word [r14], 0x0001                        | 66 41 81 3e 01 00                |
    | cmp word [r15], 0x0001                        | 66 41 81 3f 01 00                |
    | cmp word [rax + 1 * rcx], 0x0001              | 66 81 3c 08 01 00                |
    | cmp word [rcx + 1 * rcx], 0x0001              | 66 81 3c 09 01 00                |
    | cmp word [rdx + 1 * rcx], 0x0001              | 66 81 3c 0a 01 00                |
    | cmp word [rbx + 1 * rcx], 0x0001              | 66 81 3c 0b 01 00                |
    | cmp word [rsp + 1 * rcx], 0x0001              | 66 81 3c 0c 01 00                |
    | cmp word [rbp + 1 * rcx], 0x0001              | 66 81 7c 0d 00 01 00             |
    | cmp word [rsi + 1 * rcx], 0x0001              | 66 81 3c 0e 01 00                |
    | cmp word [rdi + 1 * rcx], 0x0001              | 66 81 3c 0f 01 00                |
    | cmp word [r8 + 1 * rcx], 0x0001               | 66 41 81 3c 08 01 00             |
    | cmp word [r9 + 1 * rcx], 0x0001               | 66 41 81 3c 09 01 00             |
    | cmp word [r10 + 1 * rcx], 0x0001              | 66 41 81 3c 0a 01 00             |
    | cmp word [r11 + 1 * rcx], 0x0001              | 66 41 81 3c 0b 01 00             |
    | cmp word [r12 + 1 * rcx], 0x0001              | 66 41 81 3c 0c 01 00             |
    | cmp word [r13 + 1 * rcx], 0x0001              | 66 41 81 7c 0d 00 01 00          |
    | cmp word [r14 + 1 * rcx], 0x0001              | 66 41 81 3c 0e 01 00             |
    | cmp word [r15 + 1 * rcx], 0x0001              | 66 41 81 3c 0f 01 00             |
    | cmp word [rax + 1 * rax], 0x0001              | 66 81 3c 00 01 00                |
    | cmp word [rax + 1 * rdx], 0x0001              | 66 81 3c 10 01 00                |
    | cmp word [rax + 1 * rbx], 0x0001              | 66 81 3c 18 01 00                |
    | cmp word [rax + 1 * rbp], 0x0001              | 66 81 3c 28 01 00                |
    | cmp word [rax + 1 * rsi], 0x0001              | 66 81 3c 30 01 00                |
    | cmp word [rax + 1 * rdi], 0x0001              | 66 81 3c 38 01 00                |
    | cmp word [rax + 1 * r8], 0x0001               | 66 42 81 3c 00 01 00             |
    | cmp word [rax + 1 * r9], 0x0001               | 66 42 81 3c 08 01 00             |
    | cmp word [rax + 1 * r10], 0x0001              | 66 42 81 3c 10 01 00             |
    | cmp word [rax + 1 * r11], 0x0001              | 66 42 81 3c 18 01 00             |
    | cmp word [rax + 1 * r12], 0x0001              | 66 42 81 3c 20 01 00             |
    | cmp word [rax + 1 * r13], 0x0001              | 66 42 81 3c 28 01 00             |
    | cmp word [rax + 1 * r14], 0x0001              | 66 42 81 3c 30 01 00             |
    | cmp word [rax + 1 * r15], 0x0001              | 66 42 81 3c 38 01 00             |
    | cmp word [rax + 2 * rcx], 0x0001              | 66 81 3c 48 01 00                |
    | cmp word [rax + 4 * rcx], 0x0001              | 66 81 3c 88 01 00                |
    | cmp word [rax + 8 * rcx], 0x0001              | 66 81 3c c8 01 00                |
    | cmp word [r8 + 1 * r9], 0x0001                | 66 43 81 3c 08 01 00             |
    | cmp word [r8 + 2 * r9], 0x0001                | 66 43 81 3c 48 01 00             |
    | cmp word [r8 + 4 * r9], 0x0001                | 66 43 81 3c 88 01 00             |
    | cmp word [r8 + 8 * r9], 0x0001                | 66 43 81 3c c8 01 00             |
    | cmp word [1 * rcx], 0x0001                    | 66 81 3c 0d 00 00 00 00 01 00    |
    | cmp word [2 * rcx], 0x0001                    | 66 81 3c 4d 00 00 00 00 01 00    |
    | cmp word [4 * rcx], 0x0001                    | 66 81 3c 8d 00 00 00 00 01 00    |
    | cmp word [8 * rcx], 0x0001                    | 66 81 3c cd 00 00 00 00 01 00    |
    | cmp word [1 * r9], 0x0001                     | 66 42 81 3c 0d 00 00 00 00 01 00 |
    | cmp word [2 * r9], 0x0001                     | 66 42 81 3c 4d 00 00 00 00 01 00 |
    | cmp word [4 * r9], 0x0001                     | 66 42 81 3c 8d 00 00 00 00 01 00 |
    | cmp word [8 * r9], 0x0001                     | 66 42 81 3c cd 00 00 00 00 01 00 |
    | cmp word [r13 + 8 * r12], 0x0001              | 66 43 81 7c e5 00 01 00          |
    | cmp word [rsp + 4 * r15], 0x0001              | 66 42 81 3c bc 01 00             |
    | cmp word [rax + 1 * rcx + 0x00], 0x0001       | 66 81 7c 08 00 01 00             |
    | cmp word [rax + 1 * rcx - 0x00], 0x0001       | 66 81 7c 08 00 01 00             |
    | cmp word [rax + 1 * rcx + 0x01], 0x0001       | 66 81 7c 08 01 01 00             |
    | cmp word [rax + 1 * rcx - 0x01], 0x0001       | 66 81 7c 08 ff 01 00             |
    | cmp word [rax + 1 * rcx + 0x00000001], 0x0001 | 66 81 bc 08 01 00 00 00 01 00    |
    | cmp word [rax + 1 * rcx - 0x00000001], 0x0001 | 66 81 bc 08 ff ff ff ff 01 00    |
    | cmp word [rax + 1 * rcx + 0x7f], 0x0001       | 66 81 7c 08 7f 01 00             |
    | cmp word [rax + 1 * rcx - 0x7f], 0x0001       | 66 81 7c 08 81 01 00             |
    | cmp word [rax + 1 * rcx + 0x80], 0x0001       | 66 81 bc 08 80 00 00 00 01 00    |
    | cmp word [rax + 1 * rcx - 0x80], 0x0001       | 66 81 7c 08 80 01 00             |
    | cmp word [rax + 1 * rcx - 0x81], 0x0001       | 66 81 bc 08 7f ff ff ff 01 00    |
    | cmp word [rax + 1 * rcx + 0xff], 0x0001       | 66 81 bc 08 ff 00 00 00 01 00    |
    | cmp word [rax + 1 * rcx - 0xff], 0x0001       | 66 81 bc 08 01 ff ff ff 01 00    |
    | cmp word [rax + 1 * rcx + 0x7fffffff], 0x0001 | 66 81 bc 08 ff ff ff 7f 01 00    |
    | cmp word [rax + 1 * rcx - 0x7fffffff], 0x0001 | 66 81 bc 08 01 00 00 80 01 00    |
    | cmp word [rax + 1 * rcx - 0x80000000], 0x0001 | 66 81 bc 08 00 00 00 80 01 00    |
    | cmp word [r10 + 0x7f], 0x0001                 | 66 41 81 7a 7f 01 00             |
    | cmp word [r10 + 0x80], 0x0001                 | 66 41 81 ba 80 00 00 00 01 00    |
    | cmp word [r10 - 0x80], 0x0001                 | 66 41 81 7a 80 01 00             |
    | cmp word [r10 - 0x81], 0x0001                 | 66 41 81 ba 7f ff ff ff 01 00    |
    | cmp word [rax], 0x0000                        | 66 81 38 00 00                   |
    | cmp word [rax], 0x007f                        | 66 81 38 7f 00                   |
    | cmp word [rax], 0x0080                        | 66 81 38 80 00                   |
    | cmp word [rax], 0x00ff                        | 66 81 38 ff 00                   |
    | cmp word [rax], 0x0100                        | 66 81 38 00 01                   |
    | cmp word [rax], 0x7fff                        | 66 81 38 ff 7f                   |
    | cmp word [rax], 0x8000                        | 66 81 38 00 80                   |
    | cmp word [rax], 0xffff                        | 66 81 38 ff ff                   |
    | cmp word [rcx], 0x007f                        | 66 81 39 7f 00                   |
    | cmp word [rdx], 0x0080                        | 66 81 3a 80 00                   |
    | cmp word [rbx], 0x00ff                        | 66 81 3b ff 00                   |
    | cmp word [rsp], 0x0100                        | 66 81 3c 24 00 01                |
    | cmp word [rbp], 0x7fff                        | 66 81 7d 00 ff 7f                |
    | cmp word [rsi], 0x8000                        | 66 81 3e 00 80                   |
    | cmp word [rdi], 0xffff                        | 66 81 3f ff ff                   |
    | cmp word [r8], 0x0000                         | 66 41 81 38 00 00                |
    | cmp word [r10], 0x007f                        | 66 41 81 3a 7f 00                |
    | cmp word [r11], 0x0080                        | 66 41 81 3b 80 00                |
    | cmp word [r12], 0x00ff                        | 66 41 81 3c 24 ff 00             |
    | cmp word [r13], 0x0100                        | 66 41 81 7d 00 00 01             |
    | cmp word [r14], 0x7fff                        | 66 41 81 3e ff 7f                |
    | cmp word [r15], 0x8000                        | 66 41 81 3f 00 80                |
    | cmp word [rax + 1 * rcx], 0xffff              | 66 81 3c 08 ff ff                |
    | cmp word [rcx + 1 * rcx], 0x0000              | 66 81 3c 09 00 00                |
    | cmp word [rbx + 1 * rcx], 0x007f              | 66 81 3c 0b 7f 00                |
    | cmp word [rsp + 1 * rcx], 0x0080              | 66 81 3c 0c 80 00                |
    | cmp word [rbp + 1 * rcx], 0x00ff              | 66 81 7c 0d 00 ff 00             |
    | cmp word [rsi + 1 * rcx], 0x0100              | 66 81 3c 0e 00 01                |
    | cmp word [rdi + 1 * rcx], 0x7fff              | 66 81 3c 0f ff 7f                |
    | cmp word [r8 + 1 * rcx], 0x8000               | 66 41 81 3c 08 00 80             |
    | cmp word [r9 + 1 * rcx], 0xffff               | 66 41 81 3c 09 ff ff             |
    | cmp word [r10 + 1 * rcx], 0x0000              | 66 41 81 3c 0a 00 00             |
    | cmp word [r12 + 1 * rcx], 0x007f              | 66 41 81 3c 0c 7f 00             |
    | cmp word [r13 + 1 * rcx], 0x0080              | 66 41 81 7c 0d 00 80 00          |
    | cmp word [r14 + 1 * rcx], 0x00ff              | 66 41 81 3c 0e ff 00             |
    | cmp word [r15 + 1 * rcx], 0x0100              | 66 41 81 3c 0f 00 01             |
    | cmp word [rax + 1 * rax], 0x7fff              | 66 81 3c 00 ff 7f                |
    | cmp word [rax + 1 * rdx], 0x8000              | 66 81 3c 10 00 80                |
    | cmp word [rax + 1 * rbx], 0xffff              | 66 81 3c 18 ff ff                |
    | cmp word [rax + 1 * rbp], 0x0000              | 66 81 3c 28 00 00                |
    | cmp word [rax + 1 * rdi], 0x007f              | 66 81 3c 38 7f 00                |
    | cmp word [rax + 1 * r8], 0x0080               | 66 42 81 3c 00 80 00             |
    | cmp word [rax + 1 * r9], 0x00ff               | 66 42 81 3c 08 ff 00             |
    | cmp word [rax + 1 * r10], 0x0100              | 66 42 81 3c 10 00 01             |
    | cmp word [rax + 1 * r11], 0x7fff              | 66 42 81 3c 18 ff 7f             |
    | cmp word [rax + 1 * r12], 0x8000              | 66 42 81 3c 20 00 80             |
    | cmp word [rax + 1 * r13], 0xffff              | 66 42 81 3c 28 ff ff             |
    | cmp word [rax + 1 * r14], 0x0000              | 66 42 81 3c 30 00 00             |
    | cmp word [rax + 2 * rcx], 0x007f              | 66 81 3c 48 7f 00                |
    | cmp word [rax + 4 * rcx], 0x0080              | 66 81 3c 88 80 00                |
    | cmp word [rax + 8 * rcx], 0x00ff              | 66 81 3c c8 ff 00                |
    | cmp word [r8 + 1 * r9], 0x0100                | 66 43 81 3c 08 00 01             |
    | cmp word [r8 + 2 * r9], 0x7fff                | 66 43 81 3c 48 ff 7f             |
    | cmp word [r8 + 4 * r9], 0x8000                | 66 43 81 3c 88 00 80             |
    | cmp word [r8 + 8 * r9], 0xffff                | 66 43 81 3c c8 ff ff             |
    | cmp word [1 * rcx], 0x0000                    | 66 81 3c 0d 00 00 00 00 00 00    |
    | cmp word [4 * rcx], 0x007f                    | 66 81 3c 8d 00 00 00 00 7f 00    |
    | cmp word [8 * rcx], 0x0080                    | 66 81 3c cd 00 00 00 00 80 00    |
    | cmp word [1 * r9], 0x00ff                     | 66 42 81 3c 0d 00 00 00 00 ff 00 |
    | cmp word [2 * r9], 0x0100                     | 66 42 81 3c 4d 00 00 00 00 00 01 |
    | cmp word [4 * r9], 0x7fff                     | 66 42 81 3c 8d 00 00 00 00 ff 7f |
    | cmp word [8 * r9], 0x8000                     | 66 42 81 3c cd 00 00 00 00 00 80 |
    | cmp word [r13 + 8 * r12], 0xffff              | 66 43 81 7c e5 00 ff ff          |
    | cmp word [rsp + 4 * r15], 0x0000              | 66 42 81 3c bc 00 00             |
    | cmp word [rax + 1 * rcx - 0x00], 0x007f       | 66 81 7c 08 00 7f 00             |
    | cmp word [rax + 1 * rcx + 0x01], 0x0080       | 66 81 7c 08 01 80 00             |
    | cmp word [rax + 1 * rcx - 0x01], 0x00ff       | 66 81 7c 08 ff ff 00             |
    | cmp word [rax + 1 * rcx + 0x00000001], 0x0100 | 66 81 bc 08 01 00 00 00 00 01    |
    | cmp word [rax + 1 * rcx - 0x00000001], 0x7fff | 66 81 bc 08 ff ff ff ff ff 7f    |
    | cmp word [rax + 1 * rcx + 0x7f], 0x8000       | 66 81 7c 08 7f 00 80             |
    | cmp word [rax + 1 * rcx - 0x7f], 0xffff       | 66 81 7c 08 81 ff ff             |
    | cmp word [rax + 1 * rcx + 0x80], 0x0000       | 66 81 bc 08 80 00 00 00 00 00    |
    | cmp word [rax + 1 * rcx - 0x81], 0x007f       | 66 81 bc 08 7f ff ff ff 7f 00    |
    | cmp word [rax + 1 * rcx + 0xff], 0x0080       | 66 81 bc 08 ff 00 00 00 80 00    |
    | cmp word [rax + 1 * rcx - 0xff], 0x00ff       | 66 81 bc 08 01 ff ff ff ff 00    |
    | cmp word [rax + 1 * rcx + 0x7fffffff], 0x0100 | 66 81 bc 08 ff ff ff 7f 00 01    |
    | cmp word [rax + 1 * rcx - 0x7fffffff], 0x7fff | 66 81 bc 08 01 00 00 80 ff 7f    |
    | cmp word [rax + 1 * rcx - 0x80000000], 0x8000 | 66 81 bc 08 00 00 00 80 00 80    |
    | cmp word [r10 + 0x7f], 0xffff                 | 66 41 81 7a 7f ff ff             |
    | cmp word [r10 + 0x80], 0x0000                 | 66 41 81 ba 80 00 00 00 00 00    |
    | cmp word [r10 - 0x81], 0x007f                 | 66 41 81 ba 7f ff ff ff 7f 00    |
    | --------------------------------------------- | -------------------------------- |
"""


def can_encode_cmp_addr16_imm16():
    encode(CMP_ADDR16_IMM16)


CMP_ADDR16_REG16 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | cmp word [rax], cx                          | 66 39 08                   |
    | cmp word [rcx], cx                          | 66 39 09                   |
    | cmp word [rdx], cx                          | 66 39 0a                   |
    | cmp word [rbx], cx                          | 66 39 0b                   |
    | cmp word [rsp], cx                          | 66 39 0c 24                |
    | cmp word [rbp], cx                          | 66 39 4d 00                |
    | cmp word [rsi], cx                          | 66 39 0e                   |
    | cmp word [rdi], cx                          | 66 39 0f                   |
    | cmp word [r8], cx                           | 66 41 39 08                |
    | cmp word [r9], cx                           | 66 41 39 09                |
    | cmp word [r10], cx                          | 66 41 39 0a                |
    | cmp word [r11], cx                          | 66 41 39 0b                |
    | cmp word [r12], cx                          | 66 41 39 0c 24             |
    | cmp word [r13], cx                          | 66 41 39 4d 00             |
    | cmp word [r14], cx                          | 66 41 39 0e                |
    | cmp word [r15], cx                          | 66 41 39 0f                |
    | cmp word [rax + 1 * rcx], cx                | 66 39 0c 08                |
    | cmp word [rcx + 1 * rcx], cx                | 66 39 0c 09                |
    | cmp word [rdx + 1 * rcx], cx                | 66 39 0c 0a                |
    | cmp word [rbx + 1 * rcx], cx                | 66 39 0c 0b                |
    | cmp word [rsp + 1 * rcx], cx                | 66 39 0c 0c                |
    | cmp word [rbp + 1 * rcx], cx                | 66 39 4c 0d 00             |
    | cmp word [rsi + 1 * rcx], cx                | 66 39 0c 0e                |
    | cmp word [rdi + 1 * rcx], cx                | 66 39 0c 0f                |
    | cmp word [r8 + 1 * rcx], cx                 | 66 41 39 0c 08             |
    | cmp word [r9 + 1 * rcx], cx                 | 66 41 39 0c 09             |
    | cmp word [r10 + 1 * rcx], cx                | 66 41 39 0c 0a             |
    | cmp word [r11 + 1 * rcx], cx                | 66 41 39 0c 0b             |
    | cmp word [r12 + 1 * rcx], cx                | 66 41 39 0c 0c             |
    | cmp word [r13 + 1 * rcx], cx                | 66 41 39 4c 0d 00          |
    | cmp word [r14 + 1 * rcx], cx                | 66 41 39 0c 0e             |
    | cmp word [r15 + 1 * rcx], cx                | 66 41 39 0c 0f             |
    | cmp word [rax + 1 * rax], cx                | 66 39 0c 00                |
    | cmp word [rax + 1 * rdx], cx                | 66 39 0c 10                |
    | cmp word [rax + 1 * rbx], cx                | 66 39 0c 18                |
    | cmp word [rax + 1 * rbp], cx                | 66 39 0c 28                |
    | cmp word [rax + 1 * rsi], cx                | 66 39 0c 30                |
    | cmp word [rax + 1 * rdi], cx                | 66 39 0c 38                |
    | cmp word [rax + 1 * r8], cx                 | 66 42 39 0c 00             |
    | cmp word [rax + 1 * r9], cx                 | 66 42 39 0c 08             |
    | cmp word [rax + 1 * r10], cx                | 66 42 39 0c 10             |
    | cmp word [rax + 1 * r11], cx                | 66 42 39 0c 18             |
    | cmp word [rax + 1 * r12], cx                | 66 42 39 0c 20             |
    | cmp word [rax + 1 * r13], cx                | 66 42 39 0c 28             |
    | cmp word [rax + 1 * r14], cx                | 66 42 39 0c 30             |
    | cmp word [rax + 1 * r15], cx                | 66 42 39 0c 38             |
    | cmp word [rax + 2 * rcx], cx                | 66 39 0c 48                |
    | cmp word [rax + 4 * rcx], cx                | 66 39 0c 88                |
    | cmp word [rax + 8 * rcx], cx                | 66 39 0c c8                |
    | cmp word [r8 + 1 * r9], cx                  | 66 43 39 0c 08             |
    | cmp word [r8 + 2 * r9], cx                  | 66 43 39 0c 48             |
    | cmp word [r8 + 4 * r9], cx                  | 66 43 39 0c 88             |
    | cmp word [r8 + 8 * r9], cx                  | 66 43 39 0c c8             |
    | cmp word [1 * rcx], cx                      | 66 39 0c 0d 00 00 00 00    |
    | cmp word [2 * rcx], cx                      | 66 39 0c 4d 00 00 00 00    |
    | cmp word [4 * rcx], cx                      | 66 39 0c 8d 00 00 00 00    |
    | cmp word [8 * rcx], cx                      | 66 39 0c cd 00 00 00 00    |
    | cmp word [1 * r9], cx                       | 66 42 39 0c 0d 00 00 00 00 |
    | cmp word [2 * r9], cx                       | 66 42 39 0c 4d 00 00 00 00 |
    | cmp word [4 * r9], cx                       | 66 42 39 0c 8d 00 00 00 00 |
    | cmp word [8 * r9], cx                       | 66 42 39 0c cd 00 00 00 00 |
    | cmp word [r13 + 8 * r12], cx                | 66 43 39 4c e5 00          |
    | cmp word [rsp + 4 * r15], cx                | 66 42 39 0c bc             |
    | cmp word [rax + 1 * rcx + 0x00], cx         | 66 39 4c 08 00             |
    | cmp word [rax + 1 * rcx - 0x00], cx         | 66 39 4c 08 00             |
    | cmp word [rax + 1 * rcx + 0x01], cx         | 66 39 4c 08 01             |
    | cmp word [rax + 1 * rcx - 0x01], cx         | 66 39 4c 08 ff             |
    | cmp word [rax + 1 * rcx + 0x00000001], cx   | 66 39 8c 08 01 00 00 00    |
    | cmp word [rax + 1 * rcx - 0x00000001], cx   | 66 39 8c 08 ff ff ff ff    |
    | cmp word [rax + 1 * rcx + 0x7f], cx         | 66 39 4c 08 7f             |
    | cmp word [rax + 1 * rcx - 0x7f], cx         | 66 39 4c 08 81             |
    | cmp word [rax + 1 * rcx + 0x80], cx         | 66 39 8c 08 80 00 00 00    |
    | cmp word [rax + 1 * rcx - 0x80], cx         | 66 39 4c 08 80             |
    | cmp word [rax + 1 * rcx - 0x81], cx         | 66 39 8c 08 7f ff ff ff    |
    | cmp word [rax + 1 * rcx + 0xff], cx         | 66 39 8c 08 ff 00 00 00    |
    | cmp word [rax + 1 * rcx - 0xff], cx         | 66 39 8c 08 01 ff ff ff    |
    | cmp word [rax + 1 * rcx + 0x7fffffff], cx   | 66 39 8c 08 ff ff ff 7f    |
    | cmp word [rax + 1 * rcx - 0x7fffffff], cx   | 66 39 8c 08 01 00 00 80    |
    | cmp word [rax + 1 * rcx - 0x80000000], cx   | 66 39 8c 08 00 00 00 80    |
    | cmp word [r10 + 0x7f], cx                   | 66 41 39 4a 7f             |
    | cmp word [r10 + 0x80], cx                   | 66 41 39 8a 80 00 00 00    |
    | cmp word [r10 - 0x80], cx                   | 66 41 39 4a 80             |
    | cmp word [r10 - 0x81], cx                   | 66 41 39 8a 7f ff ff ff    |
    | cmp word [rax], ax                          | 66 39 00                   |
    | cmp word [rax], dx                          | 66 39 10                   |
    | cmp word [rax], bx                          | 66 39 18                   |
    | cmp word [rax], sp                          | 66 39 20                   |
    | cmp word [rax], bp                          | 66 39 28                   |
    | cmp word [rax], si                          | 66 39 30                   |
    | cmp word [rax], di                          | 66 39 38                   |
    | cmp word [rax], r8w                         | 66 44 39 00                |
    | cmp word [rax], r9w                         | 66 44 39 08                |
    | cmp word [rax], r10w                        | 66 44 39 10                |
    | cmp word [rax], r11w                        | 66 44 39 18                |
    | cmp word [rax], r12w                        | 66 44 39 20                |
    | cmp word [rax], r13w                        | 66 44 39 28                |
    | cmp word [rax], r14w                        | 66 44 39 30                |
    | cmp word [rax], r15w                        | 66 44 39 38                |
    | cmp word [rcx], dx                          | 66 39 11                   |
    | cmp word [rdx], bx                          | 66 39 1a                   |
    | cmp word [rbx], sp                          | 66 39 23                   |
    | cmp word [rsp], bp                          | 66 39 2c 24                |
    | cmp word [rbp], si                          | 66 39 75 00                |
    | cmp word [rsi], di                          | 66 39 3e                   |
    | cmp word [rdi], r8w                         | 66 44 39 07                |
    | cmp word [r8], r9w                          | 66 45 39 08                |
    | cmp word [r9], r10w                         | 66 45 39 11                |
    | cmp word [r10], r11w                        | 66 45 39 1a                |
    | cmp word [r11], r12w                        | 66 45 39 23                |
    | cmp word [r12], r13w                        | 66 45 39 2c 24             |
    | cmp word [r13], r14w                        | 66 45 39 75 00             |
    | cmp word [r14], r15w                        | 66 45 39 3e                |
    | cmp word [r15], ax                          | 66 41 39 07                |
    | cmp word [rcx + 1 * rcx], dx                | 66 39 14 09                |
    | cmp word [rdx + 1 * rcx], bx                | 66 39 1c 0a                |
    | cmp word [rbx + 1 * rcx], sp                | 66 39 24 0b                |
    | cmp word [rsp + 1 * rcx], bp                | 66 39 2c 0c                |
    | cmp word [rbp + 1 * rcx], si                | 66 39 74 0d 00             |
    | cmp word [rsi + 1 * rcx], di                | 66 39 3c 0e                |
    | cmp word [rdi + 1 * rcx], r8w               | 66 44 39 04 0f             |
    | cmp word [r8 + 1 * rcx], r9w                | 66 45 39 0c 08             |
    | cmp word [r9 + 1 * rcx], r10w               | 66 45 39 14 09             |
    | cmp word [r10 + 1 * rcx], r11w              | 66 45 39 1c 0a             |
    | cmp word [r11 + 1 * rcx], r12w              | 66 45 39 24 0b             |
    | cmp word [r12 + 1 * rcx], r13w              | 66 45 39 2c 0c             |
    | cmp word [r13 + 1 * rcx], r14w              | 66 45 39 74 0d 00          |
    | cmp word [r14 + 1 * rcx], r15w              | 66 45 39 3c 0e             |
    | cmp word [r15 + 1 * rcx], ax                | 66 41 39 04 0f             |
    | cmp word [rax + 1 * rdx], dx                | 66 39 14 10                |
    | cmp word [rax + 1 * rbx], bx                | 66 39 1c 18                |
    | cmp word [rax + 1 * rbp], sp                | 66 39 24 28                |
    | cmp word [rax + 1 * rsi], bp                | 66 39 2c 30                |
    | cmp word [rax + 1 * rdi], si                | 66 39 34 38                |
    | cmp word [rax + 1 * r8], di                 | 66 42 39 3c 00             |
    | cmp word [rax + 1 * r9], r8w                | 66 46 39 04 08             |
    | cmp word [rax + 1 * r10], r9w               | 66 46 39 0c 10             |
    | cmp word [rax + 1 * r11], r10w              | 66 46 39 14 18             |
    | cmp word [rax + 1 * r12], r11w              | 66 46 39 1c 20             |
    | cmp word [rax + 1 * r13], r12w              | 66 46 39 24 28             |
    | cmp word [rax + 1 * r14], r13w              | 66 46 39 2c 30             |
    | cmp word [rax + 1 * r15], r14w              | 66 46 39 34 38             |
    | cmp word [rax + 2 * rcx], r15w              | 66 44 39 3c 48             |
    | cmp word [rax + 4 * rcx], ax                | 66 39 04 88                |
    | cmp word [r8 + 1 * r9], dx                  | 66 43 39 14 08             |
    | cmp word [r8 + 2 * r9], bx                  | 66 43 39 1c 48             |
    | cmp word [r8 + 4 * r9], sp                  | 66 43 39 24 88             |
    | cmp word [r8 + 8 * r9], bp                  | 66 43 39 2c c8             |
    | cmp word [1 * rcx], si                      | 66 39 34 0d 00 00 00 00    |
    | cmp word [2 * rcx], di                      | 66 39 3c 4d 00 00 00 00    |
    | cmp word [4 * rcx], r8w                     | 66 44 39 04 8d 00 00 00 00 |
    | cmp word [8 * rcx], r9w                     | 66 44 39 0c cd 00 00 00 00 |
    | cmp word [1 * r9], r10w                     | 66 46 39 14 0d 00 00 00 00 |
    | cmp word [2 * r9], r11w                     | 66 46 39 1c 4d 00 00 00 00 |
    | cmp word [4 * r9], r12w                     | 66 46 39 24 8d 00 00 00 00 |
    | cmp word [8 * r9], r13w                     | 66 46 39 2c cd 00 00 00 00 |
    | cmp word [r13 + 8 * r12], r14w              | 66 47 39 74 e5 00          |
    | cmp word [rsp + 4 * r15], r15w              | 66 46 39 3c bc             |
    | cmp word [rax + 1 * rcx + 0x00], ax         | 66 39 44 08 00             |
    | cmp word [rax + 1 * rcx + 0x01], dx         | 66 39 54 08 01             |
    | cmp word [rax + 1 * rcx - 0x01], bx         | 66 39 5c 08 ff             |
    | cmp word [rax + 1 * rcx + 0x00000001], sp   | 66 39 a4 08 01 00 00 00    |
    | cmp word [rax + 1 * rcx - 0x00000001], bp   | 66 39 ac 08 ff ff ff ff    |
    | cmp word [rax + 1 * rcx + 0x7f], si         | 66 39 74 08 7f             |
    | cmp word [rax + 1 * rcx - 0x7f], di         | 66 39 7c 08 81             |
    | cmp word [rax + 1 * rcx + 0x80], r8w        | 66 44 39 84 08 80 00 00 00 |
    | cmp word [rax + 1 * rcx - 0x80], r9w        | 66 44 39 4c 08 80          |
    | cmp word [rax + 1 * rcx - 0x81], r10w       | 66 44 39 94 08 7f ff ff ff |
    | cmp word [rax + 1 * rcx + 0xff], r11w       | 66 44 39 9c 08 ff 00 00 00 |
    | cmp word [rax + 1 * rcx - 0xff], r12w       | 66 44 39 a4 08 01 ff ff ff |
    | cmp word [rax + 1 * rcx + 0x7fffffff], r13w | 66 44 39 ac 08 ff ff ff 7f |
    | cmp word [rax + 1 * rcx - 0x7fffffff], r14w | 66 44 39 b4 08 01 00 00 80 |
    | cmp word [rax + 1 * rcx - 0x80000000], r15w | 66 44 39 bc 08 00 00 00 80 |
    | cmp word [r10 + 0x7f], ax                   | 66 41 39 42 7f             |
    | cmp word [r10 - 0x80], dx                   | 66 41 39 52 80             |
    | cmp word [r10 - 0x81], bx                   | 66 41 39 9a 7f ff ff ff    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_cmp_addr16_reg16():
    encode(CMP_ADDR16_REG16)


CMP_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | cmp byte [rax], 0x01                        | 80 38 01                   |
    | cmp byte [rcx], 0x01                        | 80 39 01                   |
    | cmp byte [rdx], 0x01                        | 80 3a 01                   |
    | cmp byte [rbx], 0x01                        | 80 3b 01                   |
    | cmp byte [rsp], 0x01                        | 80 3c 24 01                |
    | cmp byte [rbp], 0x01                        | 80 7d 00 01                |
    | cmp byte [rsi], 0x01                        | 80 3e 01                   |
    | cmp byte [rdi], 0x01                        | 80 3f 01                   |
    | cmp byte [r8], 0x01                         | 41 80 38 01                |
    | cmp byte [r9], 0x01                         | 41 80 39 01                |
    | cmp byte [r10], 0x01                        | 41 80 3a 01                |
    | cmp byte [r11], 0x01                        | 41 80 3b 01                |
    | cmp byte [r12], 0x01                        | 41 80 3c 24 01             |
    | cmp byte [r13], 0x01                        | 41 80 7d 00 01             |
    | cmp byte [r14], 0x01                        | 41 80 3e 01                |
    | cmp byte [r15], 0x01                        | 41 80 3f 01                |
    | cmp byte [rax + 1 * rcx], 0x01              | 80 3c 08 01                |
    | cmp byte [rcx + 1 * rcx], 0x01              | 80 3c 09 01                |
    | cmp byte [rdx + 1 * rcx], 0x01              | 80 3c 0a 01                |
    | cmp byte [rbx + 1 * rcx], 0x01              | 80 3c 0b 01                |
    | cmp byte [rsp + 1 * rcx], 0x01              | 80 3c 0c 01                |
    | cmp byte [rbp + 1 * rcx], 0x01              | 80 7c 0d 00 01             |
    | cmp byte [rsi + 1 * rcx], 0x01              | 80 3c 0e 01                |
    | cmp byte [rdi + 1 * rcx], 0x01              | 80 3c 0f 01                |
    | cmp byte [r8 + 1 * rcx], 0x01               | 41 80 3c 08 01             |
    | cmp byte [r9 + 1 * rcx], 0x01               | 41 80 3c 09 01             |
    | cmp byte [r10 + 1 * rcx], 0x01              | 41 80 3c 0a 01             |
    | cmp byte [r11 + 1 * rcx], 0x01              | 41 80 3c 0b 01             |
    | cmp byte [r12 + 1 * rcx], 0x01              | 41 80 3c 0c 01             |
    | cmp byte [r13 + 1 * rcx], 0x01              | 41 80 7c 0d 00 01          |
    | cmp byte [r14 + 1 * rcx], 0x01              | 41 80 3c 0e 01             |
    | cmp byte [r15 + 1 * rcx], 0x01              | 41 80 3c 0f 01             |
    | cmp byte [rax + 1 * rax], 0x01              | 80 3c 00 01                |
    | cmp byte [rax + 1 * rdx], 0x01              | 80 3c 10 01                |
    | cmp byte [rax + 1 * rbx], 0x01              | 80 3c 18 01                |
    | cmp byte [rax + 1 * rbp], 0x01              | 80 3c 28 01                |
    | cmp byte [rax + 1 * rsi], 0x01              | 80 3c 30 01                |
    | cmp byte [rax + 1 * rdi], 0x01              | 80 3c 38 01                |
    | cmp byte [rax + 1 * r8], 0x01               | 42 80 3c 00 01             |
    | cmp byte [rax + 1 * r9], 0x01               | 42 80 3c 08 01             |
    | cmp byte [rax + 1 * r10], 0x01              | 42 80 3c 10 01             |
    | cmp byte [rax + 1 * r11], 0x01              | 42 80 3c 18 01             |
    | cmp byte [rax + 1 * r12], 0x01              | 42 80 3c 20 01             |
    | cmp byte [rax + 1 * r13], 0x01              | 42 80 3c 28 01             |
    | cmp byte [rax + 1 * r14], 0x01              | 42 80 3c 30 01             |
    | cmp byte [rax + 1 * r15], 0x01              | 42 80 3c 38 01             |
    | cmp byte [rax + 2 * rcx], 0x01              | 80 3c 48 01                |
    | cmp byte [rax + 4 * rcx], 0x01              | 80 3c 88 01                |
    | cmp byte [rax + 8 * rcx], 0x01              | 80 3c c8 01                |
    | cmp byte [r8 + 1 * r9], 0x01                | 43 80 3c 08 01             |
    | cmp byte [r8 + 2 * r9], 0x01                | 43 80 3c 48 01             |
    | cmp byte [r8 + 4 * r9], 0x01                | 43 80 3c 88 01             |
    | cmp byte [r8 + 8 * r9], 0x01                | 43 80 3c c8 01             |
    | cmp byte [1 * rcx], 0x01                    | 80 3c 0d 00 00 00 00 01    |
    | cmp byte [2 * rcx], 0x01                    | 80 3c 4d 00 00 00 00 01    |
    | cmp byte [4 * rcx], 0x01                    | 80 3c 8d 00 00 00 00 01    |
    | cmp byte [8 * rcx], 0x01                    | 80 3c cd 00 00 00 00 01    |
    | cmp byte [1 * r9], 0x01                     | 42 80 3c 0d 00 00 00 00 01 |
    | cmp byte [2 * r9], 0x01                     | 42 80 3c 4d 00 00 00 00 01 |
    | cmp byte [4 * r9], 0x01                     | 42 80 3c 8d 00 00 00 00 01 |
    | cmp byte [8 * r9], 0x01                     | 42 80 3c cd 00 00 00 00 01 |
    | cmp byte [r13 + 8 * r12], 0x01              | 43 80 7c e5 00 01          |
    | cmp byte [rsp + 4 * r15], 0x01              | 42 80 3c bc 01             |
    | cmp byte [rax + 1 * rcx + 0x00], 0x01       | 80 7c 08 00 01             |
    | cmp byte [rax + 1 * rcx - 0x00], 0x01       | 80 7c 08 00 01             |
    | cmp byte [rax + 1 * rcx + 0x01], 0x01       | 80 7c 08 01 01             |
    | cmp byte [rax + 1 * rcx - 0x01], 0x01       | 80 7c 08 ff 01             |
    | cmp byte [rax + 1 * rcx + 0x00000001], 0x01 | 80 bc 08 01 00 00 00 01    |
    | cmp byte [rax + 1 * rcx - 0x00000001], 0x01 | 80 bc 08 ff ff ff ff 01    |
    | cmp byte [rax + 1 * rcx + 0x7f], 0x01       | 80 7c 08 7f 01             |
    | cmp byte [rax + 1 * rcx - 0x7f], 0x01       | 80 7c 08 81 01             |
    | cmp byte [rax + 1 * rcx + 0x80], 0x01       | 80 bc 08 80 00 00 00 01    |
    | cmp byte [rax + 1 * rcx - 0x80], 0x01       | 80 7c 08 80 01             |
    | cmp byte [rax + 1 * rcx - 0x81], 0x01       | 80 bc 08 7f ff ff ff 01    |
    | cmp byte [rax + 1 * rcx + 0xff], 0x01       | 80 bc 08 ff 00 00 00 01    |
    | cmp byte [rax + 1 * rcx - 0xff], 0x01       | 80 bc 08 01 ff ff ff 01    |
    | cmp byte [rax + 1 * rcx + 0x7fffffff], 0x01 | 80 bc 08 ff ff ff 7f 01    |
    | cmp byte [rax + 1 * rcx - 0x7fffffff], 0x01 | 80 bc 08 01 00 00 80 01    |
    | cmp byte [rax + 1 * rcx - 0x80000000], 0x01 | 80 bc 08 00 00 00 80 01    |
    | cmp byte [r10 + 0x7f], 0x01                 | 41 80 7a 7f 01             |
    | cmp byte [r10 + 0x80], 0x01                 | 41 80 ba 80 00 00 00 01    |
    | cmp byte [r10 - 0x80], 0x01                 | 41 80 7a 80 01             |
    | cmp byte [r10 - 0x81], 0x01                 | 41 80 ba 7f ff ff ff 01    |
    | cmp byte [rax], 0x00                        | 80 38 00                   |
    | cmp byte [rax], 0x7f                        | 80 38 7f                   |
    | cmp byte [rax], 0x80                        | 80 38 80                   |
    | cmp byte [rax], 0xff                        | 80 38 ff                   |
    | cmp byte [rcx], 0x7f                        | 80 39 7f                   |
    | cmp byte [rdx], 0x80                        | 80 3a 80                   |
    | cmp byte [rbx], 0xff                        | 80 3b ff                   |
    | cmp byte [rsp], 0x00                        | 80 3c 24 00                |
    | cmp byte [rsi], 0x7f                        | 80 3e 7f                   |
    | cmp byte [rdi], 0x80                        | 80 3f 80                   |
    | cmp byte [r8], 0xff                         | 41 80 38 ff                |
    | cmp byte [r9], 0x00                         | 41 80 39 00                |
    | cmp byte [r11], 0x7f                        | 41 80 3b 7f                |
    | cmp byte [r12], 0x80                        | 41 80 3c 24 80             |
    | cmp byte [r13], 0xff                        | 41 80 7d 00 ff             |
    | cmp byte [r14], 0x00                        | 41 80 3e 00                |
    | cmp byte [rax + 1 * rcx], 0x7f              | 80 3c 08 7f                |
    | cmp byte [rcx + 1 * rcx], 0x80              | 80 3c 09 80                |
    | cmp byte [rdx + 1 * rcx], 0xff              | 80 3c 0a ff                |
    | cmp byte [rbx + 1 * rcx], 0x00              | 80 3c 0b 00                |
    | cmp byte [rbp + 1 * rcx], 0x7f              | 80 7c 0d 00 7f             |
    | cmp byte [rsi + 1 * rcx], 0x80              | 80 3c 0e 80                |
    | cmp byte [rdi + 1 * rcx], 0xff              | 80 3c 0f ff                |
    | cmp byte [r8 + 1 * rcx], 0x00               | 41 80 3c 08 00             |
    | cmp byte [r10 + 1 * rcx], 0x7f              | 41 80 3c 0a 7f             |
    | cmp byte [r11 + 1 * rcx], 0x80              | 41 80 3c 0b 80             |
    | cmp byte [r12 + 1 * rcx], 0xff              | 41 80 3c 0c ff             |
    | cmp byte [r13 + 1 * rcx], 0x00              | 41 80 7c 0d 00 00          |
    | cmp byte [r15 + 1 * rcx], 0x7f              | 41 80 3c 0f 7f             |
    | cmp byte [rax + 1 * rax], 0x80              | 80 3c 00 80                |
    | cmp byte [rax + 1 * rdx], 0xff              | 80 3c 10 ff                |
    | cmp byte [rax + 1 * rbx], 0x00              | 80 3c 18 00                |
    | cmp byte [rax + 1 * rsi], 0x7f              | 80 3c 30 7f                |
    | cmp byte [rax + 1 * rdi], 0x80              | 80 3c 38 80                |
    | cmp byte [rax + 1 * r8], 0xff               | 42 80 3c 00 ff             |
    | cmp byte [rax + 1 * r9], 0x00               | 42 80 3c 08 00             |
    | cmp byte [rax + 1 * r11], 0x7f              | 42 80 3c 18 7f             |
    | cmp byte [rax + 1 * r12], 0x80              | 42 80 3c 20 80             |
    | cmp byte [rax + 1 * r13], 0xff              | 42 80 3c 28 ff             |
    | cmp byte [rax + 1 * r14], 0x00              | 42 80 3c 30 00             |
    | cmp byte [rax + 2 * rcx], 0x7f              | 80 3c 48 7f                |
    | cmp byte [rax + 4 * rcx], 0x80              | 80 3c 88 80                |
    | cmp byte [rax + 8 * rcx], 0xff              | 80 3c c8 ff                |
    | cmp byte [r8 + 1 * r9], 0x00                | 43 80 3c 08 00             |
    | cmp byte [r8 + 4 * r9], 0x7f                | 43 80 3c 88 7f             |
    | cmp byte [r8 + 8 * r9], 0x80                | 43 80 3c c8 80             |
    | cmp byte [1 * rcx], 0xff                    | 80 3c 0d 00 00 00 00 ff    |
    | cmp byte [2 * rcx], 0x00                    | 80 3c 4d 00 00 00 00 00    |
    | cmp byte [8 * rcx], 0x7f                    | 80 3c cd 00 00 00 00 7f    |
    | cmp byte [1 * r9], 0x80                     | 42 80 3c 0d 00 00 00 00 80 |
    | cmp byte [2 * r9], 0xff                     | 42 80 3c 4d 00 00 00 00 ff |
    | cmp byte [4 * r9], 0x00                     | 42 80 3c 8d 00 00 00 00 00 |
    | cmp byte [r13 + 8 * r12], 0x7f              | 43 80 7c e5 00 7f          |
    | cmp byte [rsp + 4 * r15], 0x80              | 42 80 3c bc 80             |
    | cmp byte [rax + 1 * rcx + 0x00], 0xff       | 80 7c 08 00 ff             |
    | cmp byte [rax + 1 * rcx - 0x00], 0x00       | 80 7c 08 00 00             |
    | cmp byte [rax + 1 * rcx - 0x01], 0x7f       | 80 7c 08 ff 7f             |
    | cmp byte [rax + 1 * rcx + 0x00000001], 0x80 | 80 bc 08 01 00 00 00 80    |
    | cmp byte [rax + 1 * rcx - 0x00000001], 0xff | 80 bc 08 ff ff ff ff ff    |
    | cmp byte [rax + 1 * rcx + 0x7f], 0x00       | 80 7c 08 7f 00             |
    | cmp byte [rax + 1 * rcx + 0x80], 0x7f       | 80 bc 08 80 00 00 00 7f    |
    | cmp byte [rax + 1 * rcx - 0x80], 0x80       | 80 7c 08 80 80             |
    | cmp byte [rax + 1 * rcx - 0x81], 0xff       | 80 bc 08 7f ff ff ff ff    |
    | cmp byte [rax + 1 * rcx + 0xff], 0x00       | 80 bc 08 ff 00 00 00 00    |
    | cmp byte [rax + 1 * rcx + 0x7fffffff], 0x7f | 80 bc 08 ff ff ff 7f 7f    |
    | cmp byte [rax + 1 * rcx - 0x7fffffff], 0x80 | 80 bc 08 01 00 00 80 80    |
    | cmp byte [rax + 1 * rcx - 0x80000000], 0xff | 80 bc 08 00 00 00 80 ff    |
    | cmp byte [r10 + 0x7f], 0x00                 | 41 80 7a 7f 00             |
    | cmp byte [r10 - 0x80], 0x7f                 | 41 80 7a 80 7f             |
    | cmp byte [r10 - 0x81], 0x80                 | 41 80 ba 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_cmp_addr8_imm8():
    encode(CMP_ADDR8_IMM8)


CMP_ADDR8_REG8 = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | cmp byte [rax], cl                         | 38 08                   |
    | cmp byte [rcx], cl                         | 38 09                   |
    | cmp byte [rdx], cl                         | 38 0a                   |
    | cmp byte [rbx], cl                         | 38 0b                   |
    | cmp byte [rsp], cl                         | 38 0c 24                |
    | cmp byte [rbp], cl                         | 38 4d 00                |
    | cmp byte [rsi], cl                         | 38 0e                   |
    | cmp byte [rdi], cl                         | 38 0f                   |
    | cmp byte [r8], cl                          | 41 38 08                |
    | cmp byte [r9], cl                          | 41 38 09                |
    | cmp byte [r10], cl                         | 41 38 0a                |
    | cmp byte [r11], cl                         | 41 38 0b                |
    | cmp byte [r12], cl                         | 41 38 0c 24             |
    | cmp byte [r13], cl                         | 41 38 4d 00             |
    | cmp byte [r14], cl                         | 41 38 0e                |
    | cmp byte [r15], cl                         | 41 38 0f                |
    | cmp byte [rax + 1 * rcx], cl               | 38 0c 08                |
    | cmp byte [rcx + 1 * rcx], cl               | 38 0c 09                |
    | cmp byte [rdx + 1 * rcx], cl               | 38 0c 0a                |
    | cmp byte [rbx + 1 * rcx], cl               | 38 0c 0b                |
    | cmp byte [rsp + 1 * rcx], cl               | 38 0c 0c                |
    | cmp byte [rbp + 1 * rcx], cl               | 38 4c 0d 00             |
    | cmp byte [rsi + 1 * rcx], cl               | 38 0c 0e                |
    | cmp byte [rdi + 1 * rcx], cl               | 38 0c 0f                |
    | cmp byte [r8 + 1 * rcx], cl                | 41 38 0c 08             |
    | cmp byte [r9 + 1 * rcx], cl                | 41 38 0c 09             |
    | cmp byte [r10 + 1 * rcx], cl               | 41 38 0c 0a             |
    | cmp byte [r11 + 1 * rcx], cl               | 41 38 0c 0b             |
    | cmp byte [r12 + 1 * rcx], cl               | 41 38 0c 0c             |
    | cmp byte [r13 + 1 * rcx], cl               | 41 38 4c 0d 00          |
    | cmp byte [r14 + 1 * rcx], cl               | 41 38 0c 0e             |
    | cmp byte [r15 + 1 * rcx], cl               | 41 38 0c 0f             |
    | cmp byte [rax + 1 * rax], cl               | 38 0c 00                |
    | cmp byte [rax + 1 * rdx], cl               | 38 0c 10                |
    | cmp byte [rax + 1 * rbx], cl               | 38 0c 18                |
    | cmp byte [rax + 1 * rbp], cl               | 38 0c 28                |
    | cmp byte [rax + 1 * rsi], cl               | 38 0c 30                |
    | cmp byte [rax + 1 * rdi], cl               | 38 0c 38                |
    | cmp byte [rax + 1 * r8], cl                | 42 38 0c 00             |
    | cmp byte [rax + 1 * r9], cl                | 42 38 0c 08             |
    | cmp byte [rax + 1 * r10], cl               | 42 38 0c 10             |
    | cmp byte [rax + 1 * r11], cl               | 42 38 0c 18             |
    | cmp byte [rax + 1 * r12], cl               | 42 38 0c 20             |
    | cmp byte [rax + 1 * r13], cl               | 42 38 0c 28             |
    | cmp byte [rax + 1 * r14], cl               | 42 38 0c 30             |
    | cmp byte [rax + 1 * r15], cl               | 42 38 0c 38             |
    | cmp byte [rax + 2 * rcx], cl               | 38 0c 48                |
    | cmp byte [rax + 4 * rcx], cl               | 38 0c 88                |
    | cmp byte [rax + 8 * rcx], cl               | 38 0c c8                |
    | cmp byte [r8 + 1 * r9], cl                 | 43 38 0c 08             |
    | cmp byte [r8 + 2 * r9], cl                 | 43 38 0c 48             |
    | cmp byte [r8 + 4 * r9], cl                 | 43 38 0c 88             |
    | cmp byte [r8 + 8 * r9], cl                 | 43 38 0c c8             |
    | cmp byte [1 * rcx], cl                     | 38 0c 0d 00 00 00 00    |
    | cmp byte [2 * rcx], cl                     | 38 0c 4d 00 00 00 00    |
    | cmp byte [4 * rcx], cl                     | 38 0c 8d 00 00 00 00    |
    | cmp byte [8 * rcx], cl                     | 38 0c cd 00 00 00 00    |
    | cmp byte [1 * r9], cl                      | 42 38 0c 0d 00 00 00 00 |
    | cmp byte [2 * r9], cl                      | 42 38 0c 4d 00 00 00 00 |
    | cmp byte [4 * r9], cl                      | 42 38 0c 8d 00 00 00 00 |
    | cmp byte [8 * r9], cl                      | 42 38 0c cd 00 00 00 00 |
    | cmp byte [r13 + 8 * r12], cl               | 43 38 4c e5 00          |
    | cmp byte [rsp + 4 * r15], cl               | 42 38 0c bc             |
    | cmp byte [rax + 1 * rcx + 0x00], cl        | 38 4c 08 00             |
    | cmp byte [rax + 1 * rcx - 0x00], cl        | 38 4c 08 00             |
    | cmp byte [rax + 1 * rcx + 0x01], cl        | 38 4c 08 01             |
    | cmp byte [rax + 1 * rcx - 0x01], cl        | 38 4c 08 ff             |
    | cmp byte [rax + 1 * rcx + 0x00000001], cl  | 38 8c 08 01 00 00 00    |
    | cmp byte [rax + 1 * rcx - 0x00000001], cl  | 38 8c 08 ff ff ff ff    |
    | cmp byte [rax + 1 * rcx + 0x7f], cl        | 38 4c 08 7f             |
    | cmp byte [rax + 1 * rcx - 0x7f], cl        | 38 4c 08 81             |
    | cmp byte [rax + 1 * rcx + 0x80], cl        | 38 8c 08 80 00 00 00    |
    | cmp byte [rax + 1 * rcx - 0x80], cl        | 38 4c 08 80             |
    | cmp byte [rax + 1 * rcx - 0x81], cl        | 38 8c 08 7f ff ff ff    |
    | cmp byte [rax + 1 * rcx + 0xff], cl        | 38 8c 08 ff 00 00 00    |
    | cmp byte [rax + 1 * rcx - 0xff], cl        | 38 8c 08 01 ff ff ff    |
    | cmp byte [rax + 1 * rcx + 0x7fffffff], cl  | 38 8c 08 ff ff ff 7f    |
    | cmp byte [rax + 1 * rcx - 0x7fffffff], cl  | 38 8c 08 01 00 00 80    |
    | cmp byte [rax + 1 * rcx - 0x80000000], cl  | 38 8c 08 00 00 00 80    |
    | cmp byte [r10 + 0x7f], cl                  | 41 38 4a 7f             |
    | cmp byte [r10 + 0x80], cl                  | 41 38 8a 80 00 00 00    |
    | cmp byte [r10 - 0x80], cl                  | 41 38 4a 80             |
    | cmp byte [r10 - 0x81], cl                  | 41 38 8a 7f ff ff ff    |
    | cmp byte [rax], al                         | 38 00                   |
    | cmp byte [rax], dl                         | 38 10                   |
    | cmp byte [rax], bl                         | 38 18                   |
    | cmp byte [rax], spl                        | 40 38 20                |
    | cmp byte [rax], bpl                        | 40 38 28                |
    | cmp byte [rax], sil                        | 40 38 30                |
    | cmp byte [rax], dil                        | 40 38 38                |
    | cmp byte [rax], r8b                        | 44 38 00                |
    | cmp byte [rax], r9b                        | 44 38 08                |
    | cmp byte [rax], r10b                       | 44 38 10                |
    | cmp byte [rax], r11b                       | 44 38 18                |
    | cmp byte [rax], r12b                       | 44 38 20                |
    | cmp byte [rax], r13b                       | 44 38 28                |
    | cmp byte [rax], r14b                       | 44 38 30                |
    | cmp byte [rax], r15b                       | 44 38 38                |
    | cmp byte [rax], ah                         | 38 20                   |
    | cmp byte [rax], ch                         | 38 28                   |
    | cmp byte [rax], dh                         | 38 30                   |
    | cmp byte [rax], bh                         | 38 38                   |
    | cmp byte [rcx], dl                         | 38 11                   |
    | cmp byte [rdx], bl                         | 38 1a                   |
    | cmp byte [rbx], spl                        | 40 38 23                |
    | cmp byte [rsp], bpl                        | 40 38 2c 24             |
    | cmp byte [rbp], sil                        | 40 38 75 00             |
    | cmp byte [rsi], dil                        | 40 38 3e                |
    | cmp byte [rdi], r8b                        | 44 38 07                |
    | cmp byte [r8], r9b                         | 45 38 08                |
    | cmp byte [r9], r10b                        | 45 38 11                |
    | cmp byte [r10], r11b                       | 45 38 1a                |
    | cmp byte [r11], r12b                       | 45 38 23                |
    | cmp byte [r12], r13b                       | 45 38 2c 24             |
    | cmp byte [r13], r14b                       | 45 38 75 00             |
    | cmp byte [r14], r15b                       | 45 38 3e                |
    | cmp byte [r15], ah                         | !! !! !!                |
    | cmp byte [rax + 1 * rcx], ch               | 38 2c 08                |
    | cmp byte [rcx + 1 * rcx], dh               | 38 34 09                |
    | cmp byte [rdx + 1 * rcx], bh               | 38 3c 0a                |
    | cmp byte [rbx + 1 * rcx], al               | 38 04 0b                |
    | cmp byte [rbp + 1 * rcx], dl               | 38 54 0d 00             |
    | cmp byte [rsi + 1 * rcx], bl               | 38 1c 0e                |
    | cmp byte [rdi + 1 * rcx], spl              | 40 38 24 0f             |
    | cmp byte [r8 + 1 * rcx], bpl               | 41 38 2c 08             |
    | cmp byte [r9 + 1 * rcx], sil               | 41 38 34 09             |
    | cmp byte [r10 + 1 * rcx], dil              | 41 38 3c 0a             |
    | cmp byte [r11 + 1 * rcx], r8b              | 45 38 04 0b             |
    | cmp byte [r12 + 1 * rcx], r9b              | 45 38 0c 0c             |
    | cmp byte [r13 + 1 * rcx], r10b             | 45 38 54 0d 00          |
    | cmp byte [r14 + 1 * rcx], r11b             | 45 38 1c 0e             |
    | cmp byte [r15 + 1 * rcx], r12b             | 45 38 24 0f             |
    | cmp byte [rax + 1 * rax], r13b             | 44 38 2c 00             |
    | cmp byte [rax + 1 * rdx], r14b             | 44 38 34 10             |
    | cmp byte [rax + 1 * rbx], r15b             | 44 38 3c 18             |
    | cmp byte [rax + 1 * rbp], ah               | 38 24 28                |
    | cmp byte [rax + 1 * rsi], ch               | 38 2c 30                |
    | cmp byte [rax + 1 * rdi], dh               | 38 34 38                |
    | cmp byte [rax + 1 * r8], bh                | !! !! !!                |
    | cmp byte [rax + 1 * r9], al                | 42 38 04 08             |
    | cmp byte [rax + 1 * r11], dl               | 42 38 14 18             |
    | cmp byte [rax + 1 * r12], bl               | 42 38 1c 20             |
    | cmp byte [rax + 1 * r13], spl              | 42 38 24 28             |
    | cmp byte [rax + 1 * r14], bpl              | 42 38 2c 30             |
    | cmp byte [rax + 1 * r15], sil              | 42 38 34 38             |
    | cmp byte [rax + 2 * rcx], dil              | 40 38 3c 48             |
    | cmp byte [rax + 4 * rcx], r8b              | 44 38 04 88             |
    | cmp byte [rax + 8 * rcx], r9b              | 44 38 0c c8             |
    | cmp byte [r8 + 1 * r9], r10b               | 47 38 14 08             |
    | cmp byte [r8 + 2 * r9], r11b               | 47 38 1c 48             |
    | cmp byte [r8 + 4 * r9], r12b               | 47 38 24 88             |
    | cmp byte [r8 + 8 * r9], r13b               | 47 38 2c c8             |
    | cmp byte [1 * rcx], r14b                   | 44 38 34 0d 00 00 00 00 |
    | cmp byte [2 * rcx], r15b                   | 44 38 3c 4d 00 00 00 00 |
    | cmp byte [4 * rcx], ah                     | 38 24 8d 00 00 00 00    |
    | cmp byte [8 * rcx], ch                     | 38 2c cd 00 00 00 00    |
    | cmp byte [1 * r9], dh                      | !! !! !!                |
    | cmp byte [2 * r9], bh                      | !! !! !!                |
    | cmp byte [4 * r9], al                      | 42 38 04 8d 00 00 00 00 |
    | cmp byte [r13 + 8 * r12], dl               | 43 38 54 e5 00          |
    | cmp byte [rsp + 4 * r15], bl               | 42 38 1c bc             |
    | cmp byte [rax + 1 * rcx + 0x00], spl       | 40 38 64 08 00          |
    | cmp byte [rax + 1 * rcx - 0x00], bpl       | 40 38 6c 08 00          |
    | cmp byte [rax + 1 * rcx + 0x01], sil       | 40 38 74 08 01          |
    | cmp byte [rax + 1 * rcx - 0x01], dil       | 40 38 7c 08 ff          |
    | cmp byte [rax + 1 * rcx + 0x00000001], r8b | 44 38 84 08 01 00 00 00 |
    | cmp byte [rax + 1 * rcx - 0x00000001], r9b | 44 38 8c 08 ff ff ff ff |
    | cmp byte [rax + 1 * rcx + 0x7f], r10b      | 44 38 54 08 7f          |
    | cmp byte [rax + 1 * rcx - 0x7f], r11b      | 44 38 5c 08 81          |
    | cmp byte [rax + 1 * rcx + 0x80], r12b      | 44 38 a4 08 80 00 00 00 |
    | cmp byte [rax + 1 * rcx - 0x80], r13b      | 44 38 6c 08 80          |
    | cmp byte [rax + 1 * rcx - 0x81], r14b      | 44 38 b4 08 7f ff ff ff |
    | cmp byte [rax + 1 * rcx + 0xff], r15b      | 44 38 bc 08 ff 00 00 00 |
    | cmp byte [rax + 1 * rcx - 0xff], ah        | 38 a4 08 01 ff ff ff    |
    | cmp byte [rax + 1 * rcx + 0x7fffffff], ch  | 38 ac 08 ff ff ff 7f    |
    | cmp byte [rax + 1 * rcx - 0x7fffffff], dh  | 38 b4 08 01 00 00 80    |
    | cmp byte [rax + 1 * rcx - 0x80000000], bh  | 38 bc 08 00 00 00 80    |
    | cmp byte [r10 + 0x7f], al                  | 41 38 42 7f             |
    | cmp byte [r10 - 0x80], dl                  | 41 38 52 80             |
    | cmp byte [r10 - 0x81], bl                  | 41 38 9a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_cmp_addr8_reg8():
    encode(CMP_ADDR8_REG8)
