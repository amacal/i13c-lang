from tests.encoding.core import encode, exhaust


def can_exhaust_xchg():
    exhaust(
        XCHG_ADDR16_REG16,
        XCHG_ADDR32_REG32,
        XCHG_ADDR64_REG64,
        XCHG_ADDR8_REG8,
        XCHG_REG16_ADDR16,
        XCHG_REG16_REG16,
        XCHG_REG32_ADDR32,
        XCHG_REG32_REG32,
        XCHG_REG64_ADDR64,
        XCHG_REG64_REG64,
        XCHG_REG8_ADDR8,
        XCHG_REG8_REG8,
    )


XCHG_REG64_REG64 = """
    | ------------- | -------- | --- | ------------- | -------- |
    | instruction   | encoding | *** | instruction   | encoding |
    | ------------- | -------- | --- | ------------- | -------- |
    | xchg rax, rcx | 48 91    | *** | xchg rax, r8  | 49 90    |
    | xchg rcx, rcx | 48 87 c9 | *** | xchg rax, r9  | 49 91    |
    | xchg rdx, rcx | 48 87 ca | *** | xchg rax, r10 | 49 92    |
    | xchg rbx, rcx | 48 87 cb | *** | xchg rax, r11 | 49 93    |
    | xchg rsp, rcx | 48 87 cc | *** | xchg rax, r12 | 49 94    |
    | xchg rbp, rcx | 48 87 cd | *** | xchg rax, r13 | 49 95    |
    | xchg rsi, rcx | 48 87 ce | *** | xchg rax, r14 | 49 96    |
    | xchg rdi, rcx | 48 87 cf | *** | xchg rax, r15 | 49 97    |
    | xchg r8, rcx  | 49 87 c8 | *** | xchg rcx, rdx | 48 87 d1 |
    | xchg r9, rcx  | 49 87 c9 | *** | xchg rdx, rbx | 48 87 da |
    | xchg r10, rcx | 49 87 ca | *** | xchg rbx, rsp | 48 87 e3 |
    | xchg r11, rcx | 49 87 cb | *** | xchg rsp, rbp | 48 87 ec |
    | xchg r12, rcx | 49 87 cc | *** | xchg rbp, rsi | 48 87 f5 |
    | xchg r13, rcx | 49 87 cd | *** | xchg rsi, rdi | 48 87 fe |
    | xchg r14, rcx | 49 87 ce | *** | xchg rdi, r8  | 4c 87 c7 |
    | xchg r15, rcx | 49 87 cf | *** | xchg r8, r9   | 4d 87 c8 |
    | xchg rax, rax | 48 90    | *** | xchg r9, r10  | 4d 87 d1 |
    | xchg rax, rdx | 48 92    | *** | xchg r10, r11 | 4d 87 da |
    | xchg rax, rbx | 48 93    | *** | xchg r11, r12 | 4d 87 e3 |
    | xchg rax, rsp | 48 94    | *** | xchg r12, r13 | 4d 87 ec |
    | xchg rax, rbp | 48 95    | *** | xchg r13, r14 | 4d 87 f5 |
    | xchg rax, rsi | 48 96    | *** | xchg r14, r15 | 4d 87 fe |
    | xchg rax, rdi | 48 97    | *** | xchg r15, rax | 49 97    |
    | ------------- | -------- | --- | ------------- | -------- |
"""


def can_encode_xchg_reg64_reg64():
    encode(XCHG_REG64_REG64)


XCHG_REG64_ADDR64 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | xchg rax, qword [rcx]                        | 48 87 01                |
    | xchg rcx, qword [rcx]                        | 48 87 09                |
    | xchg rdx, qword [rcx]                        | 48 87 11                |
    | xchg rbx, qword [rcx]                        | 48 87 19                |
    | xchg rsp, qword [rcx]                        | 48 87 21                |
    | xchg rbp, qword [rcx]                        | 48 87 29                |
    | xchg rsi, qword [rcx]                        | 48 87 31                |
    | xchg rdi, qword [rcx]                        | 48 87 39                |
    | xchg r8, qword [rcx]                         | 4c 87 01                |
    | xchg r9, qword [rcx]                         | 4c 87 09                |
    | xchg r10, qword [rcx]                        | 4c 87 11                |
    | xchg r11, qword [rcx]                        | 4c 87 19                |
    | xchg r12, qword [rcx]                        | 4c 87 21                |
    | xchg r13, qword [rcx]                        | 4c 87 29                |
    | xchg r14, qword [rcx]                        | 4c 87 31                |
    | xchg r15, qword [rcx]                        | 4c 87 39                |
    | xchg rax, qword [rax]                        | 48 87 00                |
    | xchg rax, qword [rdx]                        | 48 87 02                |
    | xchg rax, qword [rbx]                        | 48 87 03                |
    | xchg rax, qword [rsp]                        | 48 87 04 24             |
    | xchg rax, qword [rbp]                        | 48 87 45 00             |
    | xchg rax, qword [rsi]                        | 48 87 06                |
    | xchg rax, qword [rdi]                        | 48 87 07                |
    | xchg rax, qword [r8]                         | 49 87 00                |
    | xchg rax, qword [r9]                         | 49 87 01                |
    | xchg rax, qword [r10]                        | 49 87 02                |
    | xchg rax, qword [r11]                        | 49 87 03                |
    | xchg rax, qword [r12]                        | 49 87 04 24             |
    | xchg rax, qword [r13]                        | 49 87 45 00             |
    | xchg rax, qword [r14]                        | 49 87 06                |
    | xchg rax, qword [r15]                        | 49 87 07                |
    | xchg rax, qword [rax + 1 * rcx]              | 48 87 04 08             |
    | xchg rax, qword [rcx + 1 * rcx]              | 48 87 04 09             |
    | xchg rax, qword [rdx + 1 * rcx]              | 48 87 04 0a             |
    | xchg rax, qword [rbx + 1 * rcx]              | 48 87 04 0b             |
    | xchg rax, qword [rsp + 1 * rcx]              | 48 87 04 0c             |
    | xchg rax, qword [rbp + 1 * rcx]              | 48 87 44 0d 00          |
    | xchg rax, qword [rsi + 1 * rcx]              | 48 87 04 0e             |
    | xchg rax, qword [rdi + 1 * rcx]              | 48 87 04 0f             |
    | xchg rax, qword [r8 + 1 * rcx]               | 49 87 04 08             |
    | xchg rax, qword [r9 + 1 * rcx]               | 49 87 04 09             |
    | xchg rax, qword [r10 + 1 * rcx]              | 49 87 04 0a             |
    | xchg rax, qword [r11 + 1 * rcx]              | 49 87 04 0b             |
    | xchg rax, qword [r12 + 1 * rcx]              | 49 87 04 0c             |
    | xchg rax, qword [r13 + 1 * rcx]              | 49 87 44 0d 00          |
    | xchg rax, qword [r14 + 1 * rcx]              | 49 87 04 0e             |
    | xchg rax, qword [r15 + 1 * rcx]              | 49 87 04 0f             |
    | xchg rax, qword [rax + 1 * rax]              | 48 87 04 00             |
    | xchg rax, qword [rax + 1 * rdx]              | 48 87 04 10             |
    | xchg rax, qword [rax + 1 * rbx]              | 48 87 04 18             |
    | xchg rax, qword [rax + 1 * rbp]              | 48 87 04 28             |
    | xchg rax, qword [rax + 1 * rsi]              | 48 87 04 30             |
    | xchg rax, qword [rax + 1 * rdi]              | 48 87 04 38             |
    | xchg rax, qword [rax + 1 * r8]               | 4a 87 04 00             |
    | xchg rax, qword [rax + 1 * r9]               | 4a 87 04 08             |
    | xchg rax, qword [rax + 1 * r10]              | 4a 87 04 10             |
    | xchg rax, qword [rax + 1 * r11]              | 4a 87 04 18             |
    | xchg rax, qword [rax + 1 * r12]              | 4a 87 04 20             |
    | xchg rax, qword [rax + 1 * r13]              | 4a 87 04 28             |
    | xchg rax, qword [rax + 1 * r14]              | 4a 87 04 30             |
    | xchg rax, qword [rax + 1 * r15]              | 4a 87 04 38             |
    | xchg rax, qword [rax + 2 * rcx]              | 48 87 04 48             |
    | xchg rax, qword [rax + 4 * rcx]              | 48 87 04 88             |
    | xchg rax, qword [rax + 8 * rcx]              | 48 87 04 c8             |
    | xchg rax, qword [r8 + 1 * r9]                | 4b 87 04 08             |
    | xchg rax, qword [r8 + 2 * r9]                | 4b 87 04 48             |
    | xchg rax, qword [r8 + 4 * r9]                | 4b 87 04 88             |
    | xchg rax, qword [r8 + 8 * r9]                | 4b 87 04 c8             |
    | xchg rax, qword [1 * rcx]                    | 48 87 04 0d 00 00 00 00 |
    | xchg rax, qword [2 * rcx]                    | 48 87 04 4d 00 00 00 00 |
    | xchg rax, qword [4 * rcx]                    | 48 87 04 8d 00 00 00 00 |
    | xchg rax, qword [8 * rcx]                    | 48 87 04 cd 00 00 00 00 |
    | xchg rax, qword [1 * r9]                     | 4a 87 04 0d 00 00 00 00 |
    | xchg rax, qword [2 * r9]                     | 4a 87 04 4d 00 00 00 00 |
    | xchg rax, qword [4 * r9]                     | 4a 87 04 8d 00 00 00 00 |
    | xchg rax, qword [8 * r9]                     | 4a 87 04 cd 00 00 00 00 |
    | xchg rax, qword [r13 + 8 * r12]              | 4b 87 44 e5 00          |
    | xchg rax, qword [rsp + 4 * r15]              | 4a 87 04 bc             |
    | xchg rax, qword [rax + 1 * rcx + 0x00]       | 48 87 44 08 00          |
    | xchg rax, qword [rax + 1 * rcx - 0x00]       | 48 87 44 08 00          |
    | xchg rax, qword [rax + 1 * rcx + 0x01]       | 48 87 44 08 01          |
    | xchg rax, qword [rax + 1 * rcx - 0x01]       | 48 87 44 08 ff          |
    | xchg rax, qword [rax + 1 * rcx + 0x00000001] | 48 87 84 08 01 00 00 00 |
    | xchg rax, qword [rax + 1 * rcx - 0x00000001] | 48 87 84 08 ff ff ff ff |
    | xchg rax, qword [rax + 1 * rcx + 0x7f]       | 48 87 44 08 7f          |
    | xchg rax, qword [rax + 1 * rcx - 0x7f]       | 48 87 44 08 81          |
    | xchg rax, qword [rax + 1 * rcx + 0x80]       | 48 87 84 08 80 00 00 00 |
    | xchg rax, qword [rax + 1 * rcx - 0x80]       | 48 87 44 08 80          |
    | xchg rax, qword [rax + 1 * rcx - 0x81]       | 48 87 84 08 7f ff ff ff |
    | xchg rax, qword [rax + 1 * rcx + 0xff]       | 48 87 84 08 ff 00 00 00 |
    | xchg rax, qword [rax + 1 * rcx - 0xff]       | 48 87 84 08 01 ff ff ff |
    | xchg rax, qword [rax + 1 * rcx + 0x7fffffff] | 48 87 84 08 ff ff ff 7f |
    | xchg rax, qword [rax + 1 * rcx - 0x7fffffff] | 48 87 84 08 01 00 00 80 |
    | xchg rax, qword [rax + 1 * rcx - 0x80000000] | 48 87 84 08 00 00 00 80 |
    | xchg rax, qword [r10 + 0x7f]                 | 49 87 42 7f             |
    | xchg rax, qword [r10 + 0x80]                 | 49 87 82 80 00 00 00    |
    | xchg rax, qword [r10 - 0x80]                 | 49 87 42 80             |
    | xchg rax, qword [r10 - 0x81]                 | 49 87 82 7f ff ff ff    |
    | xchg rcx, qword [rdx]                        | 48 87 0a                |
    | xchg rdx, qword [rbx]                        | 48 87 13                |
    | xchg rbx, qword [rsp]                        | 48 87 1c 24             |
    | xchg rsp, qword [rbp]                        | 48 87 65 00             |
    | xchg rbp, qword [rsi]                        | 48 87 2e                |
    | xchg rsi, qword [rdi]                        | 48 87 37                |
    | xchg rdi, qword [r8]                         | 49 87 38                |
    | xchg r8, qword [r9]                          | 4d 87 01                |
    | xchg r9, qword [r10]                         | 4d 87 0a                |
    | xchg r10, qword [r11]                        | 4d 87 13                |
    | xchg r11, qword [r12]                        | 4d 87 1c 24             |
    | xchg r12, qword [r13]                        | 4d 87 65 00             |
    | xchg r13, qword [r14]                        | 4d 87 2e                |
    | xchg r14, qword [r15]                        | 4d 87 37                |
    | xchg r15, qword [rax + 1 * rcx]              | 4c 87 3c 08             |
    | xchg rcx, qword [rdx + 1 * rcx]              | 48 87 0c 0a             |
    | xchg rdx, qword [rbx + 1 * rcx]              | 48 87 14 0b             |
    | xchg rbx, qword [rsp + 1 * rcx]              | 48 87 1c 0c             |
    | xchg rsp, qword [rbp + 1 * rcx]              | 48 87 64 0d 00          |
    | xchg rbp, qword [rsi + 1 * rcx]              | 48 87 2c 0e             |
    | xchg rsi, qword [rdi + 1 * rcx]              | 48 87 34 0f             |
    | xchg rdi, qword [r8 + 1 * rcx]               | 49 87 3c 08             |
    | xchg r8, qword [r9 + 1 * rcx]                | 4d 87 04 09             |
    | xchg r9, qword [r10 + 1 * rcx]               | 4d 87 0c 0a             |
    | xchg r10, qword [r11 + 1 * rcx]              | 4d 87 14 0b             |
    | xchg r11, qword [r12 + 1 * rcx]              | 4d 87 1c 0c             |
    | xchg r12, qword [r13 + 1 * rcx]              | 4d 87 64 0d 00          |
    | xchg r13, qword [r14 + 1 * rcx]              | 4d 87 2c 0e             |
    | xchg r14, qword [r15 + 1 * rcx]              | 4d 87 34 0f             |
    | xchg r15, qword [rax + 1 * rax]              | 4c 87 3c 00             |
    | xchg rcx, qword [rax + 1 * rbx]              | 48 87 0c 18             |
    | xchg rdx, qword [rax + 1 * rbp]              | 48 87 14 28             |
    | xchg rbx, qword [rax + 1 * rsi]              | 48 87 1c 30             |
    | xchg rsp, qword [rax + 1 * rdi]              | 48 87 24 38             |
    | xchg rbp, qword [rax + 1 * r8]               | 4a 87 2c 00             |
    | xchg rsi, qword [rax + 1 * r9]               | 4a 87 34 08             |
    | xchg rdi, qword [rax + 1 * r10]              | 4a 87 3c 10             |
    | xchg r8, qword [rax + 1 * r11]               | 4e 87 04 18             |
    | xchg r9, qword [rax + 1 * r12]               | 4e 87 0c 20             |
    | xchg r10, qword [rax + 1 * r13]              | 4e 87 14 28             |
    | xchg r11, qword [rax + 1 * r14]              | 4e 87 1c 30             |
    | xchg r12, qword [rax + 1 * r15]              | 4e 87 24 38             |
    | xchg r13, qword [rax + 2 * rcx]              | 4c 87 2c 48             |
    | xchg r14, qword [rax + 4 * rcx]              | 4c 87 34 88             |
    | xchg r15, qword [rax + 8 * rcx]              | 4c 87 3c c8             |
    | xchg rcx, qword [r8 + 2 * r9]                | 4b 87 0c 48             |
    | xchg rdx, qword [r8 + 4 * r9]                | 4b 87 14 88             |
    | xchg rbx, qword [r8 + 8 * r9]                | 4b 87 1c c8             |
    | xchg rsp, qword [1 * rcx]                    | 48 87 24 0d 00 00 00 00 |
    | xchg rbp, qword [2 * rcx]                    | 48 87 2c 4d 00 00 00 00 |
    | xchg rsi, qword [4 * rcx]                    | 48 87 34 8d 00 00 00 00 |
    | xchg rdi, qword [8 * rcx]                    | 48 87 3c cd 00 00 00 00 |
    | xchg r8, qword [1 * r9]                      | 4e 87 04 0d 00 00 00 00 |
    | xchg r9, qword [2 * r9]                      | 4e 87 0c 4d 00 00 00 00 |
    | xchg r10, qword [4 * r9]                     | 4e 87 14 8d 00 00 00 00 |
    | xchg r11, qword [8 * r9]                     | 4e 87 1c cd 00 00 00 00 |
    | xchg r12, qword [r13 + 8 * r12]              | 4f 87 64 e5 00          |
    | xchg r13, qword [rsp + 4 * r15]              | 4e 87 2c bc             |
    | xchg r14, qword [rax + 1 * rcx + 0x00]       | 4c 87 74 08 00          |
    | xchg r15, qword [rax + 1 * rcx - 0x00]       | 4c 87 7c 08 00          |
    | xchg rcx, qword [rax + 1 * rcx - 0x01]       | 48 87 4c 08 ff          |
    | xchg rdx, qword [rax + 1 * rcx + 0x00000001] | 48 87 94 08 01 00 00 00 |
    | xchg rbx, qword [rax + 1 * rcx - 0x00000001] | 48 87 9c 08 ff ff ff ff |
    | xchg rsp, qword [rax + 1 * rcx + 0x7f]       | 48 87 64 08 7f          |
    | xchg rbp, qword [rax + 1 * rcx - 0x7f]       | 48 87 6c 08 81          |
    | xchg rsi, qword [rax + 1 * rcx + 0x80]       | 48 87 b4 08 80 00 00 00 |
    | xchg rdi, qword [rax + 1 * rcx - 0x80]       | 48 87 7c 08 80          |
    | xchg r8, qword [rax + 1 * rcx - 0x81]        | 4c 87 84 08 7f ff ff ff |
    | xchg r9, qword [rax + 1 * rcx + 0xff]        | 4c 87 8c 08 ff 00 00 00 |
    | xchg r10, qword [rax + 1 * rcx - 0xff]       | 4c 87 94 08 01 ff ff ff |
    | xchg r11, qword [rax + 1 * rcx + 0x7fffffff] | 4c 87 9c 08 ff ff ff 7f |
    | xchg r12, qword [rax + 1 * rcx - 0x7fffffff] | 4c 87 a4 08 01 00 00 80 |
    | xchg r13, qword [rax + 1 * rcx - 0x80000000] | 4c 87 ac 08 00 00 00 80 |
    | xchg r14, qword [r10 + 0x7f]                 | 4d 87 72 7f             |
    | xchg r15, qword [r10 + 0x80]                 | 4d 87 ba 80 00 00 00    |
    | xchg rcx, qword [r10 - 0x81]                 | 49 87 8a 7f ff ff ff    |
    | xchg rdx, qword [rax]                        | 48 87 10                |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_xchg_reg64_addr64():
    encode(XCHG_REG64_ADDR64)


XCHG_REG32_REG32 = """
    | --------------- | -------- | --- | --------------- | -------- |
    | instruction     | encoding | *** | instruction     | encoding |
    | --------------- | -------- | --- | --------------- | -------- |
    | xchg eax, ecx   | 91       | *** | xchg eax, r8d   | 41 90    |
    | xchg ecx, ecx   | 87 c9    | *** | xchg eax, r9d   | 41 91    |
    | xchg edx, ecx   | 87 ca    | *** | xchg eax, r10d  | 41 92    |
    | xchg ebx, ecx   | 87 cb    | *** | xchg eax, r11d  | 41 93    |
    | xchg esp, ecx   | 87 cc    | *** | xchg eax, r12d  | 41 94    |
    | xchg ebp, ecx   | 87 cd    | *** | xchg eax, r13d  | 41 95    |
    | xchg esi, ecx   | 87 ce    | *** | xchg eax, r14d  | 41 96    |
    | xchg edi, ecx   | 87 cf    | *** | xchg eax, r15d  | 41 97    |
    | xchg r8d, ecx   | 41 87 c8 | *** | xchg ecx, edx   | 87 d1    |
    | xchg r9d, ecx   | 41 87 c9 | *** | xchg edx, ebx   | 87 da    |
    | xchg r10d, ecx  | 41 87 ca | *** | xchg ebx, esp   | 87 e3    |
    | xchg r11d, ecx  | 41 87 cb | *** | xchg esp, ebp   | 87 ec    |
    | xchg r12d, ecx  | 41 87 cc | *** | xchg ebp, esi   | 87 f5    |
    | xchg r13d, ecx  | 41 87 cd | *** | xchg esi, edi   | 87 fe    |
    | xchg r14d, ecx  | 41 87 ce | *** | xchg edi, r8d   | 44 87 c7 |
    | xchg r15d, ecx  | 41 87 cf | *** | xchg r8d, r9d   | 45 87 c8 |
    | xchg eax, eax   | 90       | *** | xchg r9d, r10d  | 45 87 d1 |
    | xchg eax, edx   | 92       | *** | xchg r10d, r11d | 45 87 da |
    | xchg eax, ebx   | 93       | *** | xchg r11d, r12d | 45 87 e3 |
    | xchg eax, esp   | 94       | *** | xchg r12d, r13d | 45 87 ec |
    | xchg eax, ebp   | 95       | *** | xchg r13d, r14d | 45 87 f5 |
    | xchg eax, esi   | 96       | *** | xchg r14d, r15d | 45 87 fe |
    | xchg eax, edi   | 97       | *** | xchg r15d, eax  | 41 97    |
    | --------------- | -------- | --- | --------------- | -------- |
"""


def can_encode_xchg_reg32_reg32():
    encode(XCHG_REG32_REG32)


XCHG_REG32_ADDR32 = """
    | --------------------------------------------- | ----------------------- |
    | instruction                                   | encoding                |
    | --------------------------------------------- | ----------------------- |
    | xchg eax, dword [rcx]                         | 87 01                   |
    | xchg ecx, dword [rcx]                         | 87 09                   |
    | xchg edx, dword [rcx]                         | 87 11                   |
    | xchg ebx, dword [rcx]                         | 87 19                   |
    | xchg esp, dword [rcx]                         | 87 21                   |
    | xchg ebp, dword [rcx]                         | 87 29                   |
    | xchg esi, dword [rcx]                         | 87 31                   |
    | xchg edi, dword [rcx]                         | 87 39                   |
    | xchg r8d, dword [rcx]                         | 44 87 01                |
    | xchg r9d, dword [rcx]                         | 44 87 09                |
    | xchg r10d, dword [rcx]                        | 44 87 11                |
    | xchg r11d, dword [rcx]                        | 44 87 19                |
    | xchg r12d, dword [rcx]                        | 44 87 21                |
    | xchg r13d, dword [rcx]                        | 44 87 29                |
    | xchg r14d, dword [rcx]                        | 44 87 31                |
    | xchg r15d, dword [rcx]                        | 44 87 39                |
    | xchg eax, dword [rax]                         | 87 00                   |
    | xchg eax, dword [rdx]                         | 87 02                   |
    | xchg eax, dword [rbx]                         | 87 03                   |
    | xchg eax, dword [rsp]                         | 87 04 24                |
    | xchg eax, dword [rbp]                         | 87 45 00                |
    | xchg eax, dword [rsi]                         | 87 06                   |
    | xchg eax, dword [rdi]                         | 87 07                   |
    | xchg eax, dword [r8]                          | 41 87 00                |
    | xchg eax, dword [r9]                          | 41 87 01                |
    | xchg eax, dword [r10]                         | 41 87 02                |
    | xchg eax, dword [r11]                         | 41 87 03                |
    | xchg eax, dword [r12]                         | 41 87 04 24             |
    | xchg eax, dword [r13]                         | 41 87 45 00             |
    | xchg eax, dword [r14]                         | 41 87 06                |
    | xchg eax, dword [r15]                         | 41 87 07                |
    | xchg eax, dword [rax + 1 * rcx]               | 87 04 08                |
    | xchg eax, dword [rcx + 1 * rcx]               | 87 04 09                |
    | xchg eax, dword [rdx + 1 * rcx]               | 87 04 0a                |
    | xchg eax, dword [rbx + 1 * rcx]               | 87 04 0b                |
    | xchg eax, dword [rsp + 1 * rcx]               | 87 04 0c                |
    | xchg eax, dword [rbp + 1 * rcx]               | 87 44 0d 00             |
    | xchg eax, dword [rsi + 1 * rcx]               | 87 04 0e                |
    | xchg eax, dword [rdi + 1 * rcx]               | 87 04 0f                |
    | xchg eax, dword [r8 + 1 * rcx]                | 41 87 04 08             |
    | xchg eax, dword [r9 + 1 * rcx]                | 41 87 04 09             |
    | xchg eax, dword [r10 + 1 * rcx]               | 41 87 04 0a             |
    | xchg eax, dword [r11 + 1 * rcx]               | 41 87 04 0b             |
    | xchg eax, dword [r12 + 1 * rcx]               | 41 87 04 0c             |
    | xchg eax, dword [r13 + 1 * rcx]               | 41 87 44 0d 00          |
    | xchg eax, dword [r14 + 1 * rcx]               | 41 87 04 0e             |
    | xchg eax, dword [r15 + 1 * rcx]               | 41 87 04 0f             |
    | xchg eax, dword [rax + 1 * rax]               | 87 04 00                |
    | xchg eax, dword [rax + 1 * rdx]               | 87 04 10                |
    | xchg eax, dword [rax + 1 * rbx]               | 87 04 18                |
    | xchg eax, dword [rax + 1 * rbp]               | 87 04 28                |
    | xchg eax, dword [rax + 1 * rsi]               | 87 04 30                |
    | xchg eax, dword [rax + 1 * rdi]               | 87 04 38                |
    | xchg eax, dword [rax + 1 * r8]                | 42 87 04 00             |
    | xchg eax, dword [rax + 1 * r9]                | 42 87 04 08             |
    | xchg eax, dword [rax + 1 * r10]               | 42 87 04 10             |
    | xchg eax, dword [rax + 1 * r11]               | 42 87 04 18             |
    | xchg eax, dword [rax + 1 * r12]               | 42 87 04 20             |
    | xchg eax, dword [rax + 1 * r13]               | 42 87 04 28             |
    | xchg eax, dword [rax + 1 * r14]               | 42 87 04 30             |
    | xchg eax, dword [rax + 1 * r15]               | 42 87 04 38             |
    | xchg eax, dword [rax + 2 * rcx]               | 87 04 48                |
    | xchg eax, dword [rax + 4 * rcx]               | 87 04 88                |
    | xchg eax, dword [rax + 8 * rcx]               | 87 04 c8                |
    | xchg eax, dword [r8 + 1 * r9]                 | 43 87 04 08             |
    | xchg eax, dword [r8 + 2 * r9]                 | 43 87 04 48             |
    | xchg eax, dword [r8 + 4 * r9]                 | 43 87 04 88             |
    | xchg eax, dword [r8 + 8 * r9]                 | 43 87 04 c8             |
    | xchg eax, dword [1 * rcx]                     | 87 04 0d 00 00 00 00    |
    | xchg eax, dword [2 * rcx]                     | 87 04 4d 00 00 00 00    |
    | xchg eax, dword [4 * rcx]                     | 87 04 8d 00 00 00 00    |
    | xchg eax, dword [8 * rcx]                     | 87 04 cd 00 00 00 00    |
    | xchg eax, dword [1 * r9]                      | 42 87 04 0d 00 00 00 00 |
    | xchg eax, dword [2 * r9]                      | 42 87 04 4d 00 00 00 00 |
    | xchg eax, dword [4 * r9]                      | 42 87 04 8d 00 00 00 00 |
    | xchg eax, dword [8 * r9]                      | 42 87 04 cd 00 00 00 00 |
    | xchg eax, dword [r13 + 8 * r12]               | 43 87 44 e5 00          |
    | xchg eax, dword [rsp + 4 * r15]               | 42 87 04 bc             |
    | xchg eax, dword [rax + 1 * rcx + 0x00]        | 87 44 08 00             |
    | xchg eax, dword [rax + 1 * rcx - 0x00]        | 87 44 08 00             |
    | xchg eax, dword [rax + 1 * rcx + 0x01]        | 87 44 08 01             |
    | xchg eax, dword [rax + 1 * rcx - 0x01]        | 87 44 08 ff             |
    | xchg eax, dword [rax + 1 * rcx + 0x00000001]  | 87 84 08 01 00 00 00    |
    | xchg eax, dword [rax + 1 * rcx - 0x00000001]  | 87 84 08 ff ff ff ff    |
    | xchg eax, dword [rax + 1 * rcx + 0x7f]        | 87 44 08 7f             |
    | xchg eax, dword [rax + 1 * rcx - 0x7f]        | 87 44 08 81             |
    | xchg eax, dword [rax + 1 * rcx + 0x80]        | 87 84 08 80 00 00 00    |
    | xchg eax, dword [rax + 1 * rcx - 0x80]        | 87 44 08 80             |
    | xchg eax, dword [rax + 1 * rcx - 0x81]        | 87 84 08 7f ff ff ff    |
    | xchg eax, dword [rax + 1 * rcx + 0xff]        | 87 84 08 ff 00 00 00    |
    | xchg eax, dword [rax + 1 * rcx - 0xff]        | 87 84 08 01 ff ff ff    |
    | xchg eax, dword [rax + 1 * rcx + 0x7fffffff]  | 87 84 08 ff ff ff 7f    |
    | xchg eax, dword [rax + 1 * rcx - 0x7fffffff]  | 87 84 08 01 00 00 80    |
    | xchg eax, dword [rax + 1 * rcx - 0x80000000]  | 87 84 08 00 00 00 80    |
    | xchg eax, dword [r10 + 0x7f]                  | 41 87 42 7f             |
    | xchg eax, dword [r10 + 0x80]                  | 41 87 82 80 00 00 00    |
    | xchg eax, dword [r10 - 0x80]                  | 41 87 42 80             |
    | xchg eax, dword [r10 - 0x81]                  | 41 87 82 7f ff ff ff    |
    | xchg ecx, dword [rdx]                         | 87 0a                   |
    | xchg edx, dword [rbx]                         | 87 13                   |
    | xchg ebx, dword [rsp]                         | 87 1c 24                |
    | xchg esp, dword [rbp]                         | 87 65 00                |
    | xchg ebp, dword [rsi]                         | 87 2e                   |
    | xchg esi, dword [rdi]                         | 87 37                   |
    | xchg edi, dword [r8]                          | 41 87 38                |
    | xchg r8d, dword [r9]                          | 45 87 01                |
    | xchg r9d, dword [r10]                         | 45 87 0a                |
    | xchg r10d, dword [r11]                        | 45 87 13                |
    | xchg r11d, dword [r12]                        | 45 87 1c 24             |
    | xchg r12d, dword [r13]                        | 45 87 65 00             |
    | xchg r13d, dword [r14]                        | 45 87 2e                |
    | xchg r14d, dword [r15]                        | 45 87 37                |
    | xchg r15d, dword [rax + 1 * rcx]              | 44 87 3c 08             |
    | xchg ecx, dword [rdx + 1 * rcx]               | 87 0c 0a                |
    | xchg edx, dword [rbx + 1 * rcx]               | 87 14 0b                |
    | xchg ebx, dword [rsp + 1 * rcx]               | 87 1c 0c                |
    | xchg esp, dword [rbp + 1 * rcx]               | 87 64 0d 00             |
    | xchg ebp, dword [rsi + 1 * rcx]               | 87 2c 0e                |
    | xchg esi, dword [rdi + 1 * rcx]               | 87 34 0f                |
    | xchg edi, dword [r8 + 1 * rcx]                | 41 87 3c 08             |
    | xchg r8d, dword [r9 + 1 * rcx]                | 45 87 04 09             |
    | xchg r9d, dword [r10 + 1 * rcx]               | 45 87 0c 0a             |
    | xchg r10d, dword [r11 + 1 * rcx]              | 45 87 14 0b             |
    | xchg r11d, dword [r12 + 1 * rcx]              | 45 87 1c 0c             |
    | xchg r12d, dword [r13 + 1 * rcx]              | 45 87 64 0d 00          |
    | xchg r13d, dword [r14 + 1 * rcx]              | 45 87 2c 0e             |
    | xchg r14d, dword [r15 + 1 * rcx]              | 45 87 34 0f             |
    | xchg r15d, dword [rax + 1 * rax]              | 44 87 3c 00             |
    | xchg ecx, dword [rax + 1 * rbx]               | 87 0c 18                |
    | xchg edx, dword [rax + 1 * rbp]               | 87 14 28                |
    | xchg ebx, dword [rax + 1 * rsi]               | 87 1c 30                |
    | xchg esp, dword [rax + 1 * rdi]               | 87 24 38                |
    | xchg ebp, dword [rax + 1 * r8]                | 42 87 2c 00             |
    | xchg esi, dword [rax + 1 * r9]                | 42 87 34 08             |
    | xchg edi, dword [rax + 1 * r10]               | 42 87 3c 10             |
    | xchg r8d, dword [rax + 1 * r11]               | 46 87 04 18             |
    | xchg r9d, dword [rax + 1 * r12]               | 46 87 0c 20             |
    | xchg r10d, dword [rax + 1 * r13]              | 46 87 14 28             |
    | xchg r11d, dword [rax + 1 * r14]              | 46 87 1c 30             |
    | xchg r12d, dword [rax + 1 * r15]              | 46 87 24 38             |
    | xchg r13d, dword [rax + 2 * rcx]              | 44 87 2c 48             |
    | xchg r14d, dword [rax + 4 * rcx]              | 44 87 34 88             |
    | xchg r15d, dword [rax + 8 * rcx]              | 44 87 3c c8             |
    | xchg ecx, dword [r8 + 2 * r9]                 | 43 87 0c 48             |
    | xchg edx, dword [r8 + 4 * r9]                 | 43 87 14 88             |
    | xchg ebx, dword [r8 + 8 * r9]                 | 43 87 1c c8             |
    | xchg esp, dword [1 * rcx]                     | 87 24 0d 00 00 00 00    |
    | xchg ebp, dword [2 * rcx]                     | 87 2c 4d 00 00 00 00    |
    | xchg esi, dword [4 * rcx]                     | 87 34 8d 00 00 00 00    |
    | xchg edi, dword [8 * rcx]                     | 87 3c cd 00 00 00 00    |
    | xchg r8d, dword [1 * r9]                      | 46 87 04 0d 00 00 00 00 |
    | xchg r9d, dword [2 * r9]                      | 46 87 0c 4d 00 00 00 00 |
    | xchg r10d, dword [4 * r9]                     | 46 87 14 8d 00 00 00 00 |
    | xchg r11d, dword [8 * r9]                     | 46 87 1c cd 00 00 00 00 |
    | xchg r12d, dword [r13 + 8 * r12]              | 47 87 64 e5 00          |
    | xchg r13d, dword [rsp + 4 * r15]              | 46 87 2c bc             |
    | xchg r14d, dword [rax + 1 * rcx + 0x00]       | 44 87 74 08 00          |
    | xchg r15d, dword [rax + 1 * rcx - 0x00]       | 44 87 7c 08 00          |
    | xchg ecx, dword [rax + 1 * rcx - 0x01]        | 87 4c 08 ff             |
    | xchg edx, dword [rax + 1 * rcx + 0x00000001]  | 87 94 08 01 00 00 00    |
    | xchg ebx, dword [rax + 1 * rcx - 0x00000001]  | 87 9c 08 ff ff ff ff    |
    | xchg esp, dword [rax + 1 * rcx + 0x7f]        | 87 64 08 7f             |
    | xchg ebp, dword [rax + 1 * rcx - 0x7f]        | 87 6c 08 81             |
    | xchg esi, dword [rax + 1 * rcx + 0x80]        | 87 b4 08 80 00 00 00    |
    | xchg edi, dword [rax + 1 * rcx - 0x80]        | 87 7c 08 80             |
    | xchg r8d, dword [rax + 1 * rcx - 0x81]        | 44 87 84 08 7f ff ff ff |
    | xchg r9d, dword [rax + 1 * rcx + 0xff]        | 44 87 8c 08 ff 00 00 00 |
    | xchg r10d, dword [rax + 1 * rcx - 0xff]       | 44 87 94 08 01 ff ff ff |
    | xchg r11d, dword [rax + 1 * rcx + 0x7fffffff] | 44 87 9c 08 ff ff ff 7f |
    | xchg r12d, dword [rax + 1 * rcx - 0x7fffffff] | 44 87 a4 08 01 00 00 80 |
    | xchg r13d, dword [rax + 1 * rcx - 0x80000000] | 44 87 ac 08 00 00 00 80 |
    | xchg r14d, dword [r10 + 0x7f]                 | 45 87 72 7f             |
    | xchg r15d, dword [r10 + 0x80]                 | 45 87 ba 80 00 00 00    |
    | xchg ecx, dword [r10 - 0x81]                  | 41 87 8a 7f ff ff ff    |
    | xchg edx, dword [rax]                         | 87 10                   |
    | --------------------------------------------- | ----------------------- |
"""


def can_encode_xchg_reg32_addr32():
    encode(XCHG_REG32_ADDR32)


XCHG_REG16_REG16 = """
    | --------------- | ----------- | --- | --------------- | ----------- |
    | instruction     | encoding    | *** | instruction     | encoding    |
    | --------------- | ----------- | --- | --------------- | ----------- |
    | xchg ax, cx     | 66 91       | *** | xchg ax, r8w    | 66 41 90    |
    | xchg cx, cx     | 66 87 c9    | *** | xchg ax, r9w    | 66 41 91    |
    | xchg dx, cx     | 66 87 ca    | *** | xchg ax, r10w   | 66 41 92    |
    | xchg bx, cx     | 66 87 cb    | *** | xchg ax, r11w   | 66 41 93    |
    | xchg sp, cx     | 66 87 cc    | *** | xchg ax, r12w   | 66 41 94    |
    | xchg bp, cx     | 66 87 cd    | *** | xchg ax, r13w   | 66 41 95    |
    | xchg si, cx     | 66 87 ce    | *** | xchg ax, r14w   | 66 41 96    |
    | xchg di, cx     | 66 87 cf    | *** | xchg ax, r15w   | 66 41 97    |
    | xchg r8w, cx    | 66 41 87 c8 | *** | xchg cx, dx     | 66 87 d1    |
    | xchg r9w, cx    | 66 41 87 c9 | *** | xchg dx, bx     | 66 87 da    |
    | xchg r10w, cx   | 66 41 87 ca | *** | xchg bx, sp     | 66 87 e3    |
    | xchg r11w, cx   | 66 41 87 cb | *** | xchg sp, bp     | 66 87 ec    |
    | xchg r12w, cx   | 66 41 87 cc | *** | xchg bp, si     | 66 87 f5    |
    | xchg r13w, cx   | 66 41 87 cd | *** | xchg si, di     | 66 87 fe    |
    | xchg r14w, cx   | 66 41 87 ce | *** | xchg di, r8w    | 66 44 87 c7 |
    | xchg r15w, cx   | 66 41 87 cf | *** | xchg r8w, r9w   | 66 45 87 c8 |
    | xchg ax, ax     | 66 90       | *** | xchg r9w, r10w  | 66 45 87 d1 |
    | xchg ax, dx     | 66 92       | *** | xchg r10w, r11w | 66 45 87 da |
    | xchg ax, bx     | 66 93       | *** | xchg r11w, r12w | 66 45 87 e3 |
    | xchg ax, sp     | 66 94       | *** | xchg r12w, r13w | 66 45 87 ec |
    | xchg ax, bp     | 66 95       | *** | xchg r13w, r14w | 66 45 87 f5 |
    | xchg ax, si     | 66 96       | *** | xchg r14w, r15w | 66 45 87 fe |
    | xchg ax, di     | 66 97       | *** | xchg r15w, ax   | 66 41 97    |
    | --------------- | ----------- | --- | --------------- | ----------- |
"""


def can_encode_xchg_reg16_reg16():
    encode(XCHG_REG16_REG16)


XCHG_REG16_ADDR16 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | xchg ax, word [rcx]                          | 66 87 01                   |
    | xchg cx, word [rcx]                          | 66 87 09                   |
    | xchg dx, word [rcx]                          | 66 87 11                   |
    | xchg bx, word [rcx]                          | 66 87 19                   |
    | xchg sp, word [rcx]                          | 66 87 21                   |
    | xchg bp, word [rcx]                          | 66 87 29                   |
    | xchg si, word [rcx]                          | 66 87 31                   |
    | xchg di, word [rcx]                          | 66 87 39                   |
    | xchg r8w, word [rcx]                         | 66 44 87 01                |
    | xchg r9w, word [rcx]                         | 66 44 87 09                |
    | xchg r10w, word [rcx]                        | 66 44 87 11                |
    | xchg r11w, word [rcx]                        | 66 44 87 19                |
    | xchg r12w, word [rcx]                        | 66 44 87 21                |
    | xchg r13w, word [rcx]                        | 66 44 87 29                |
    | xchg r14w, word [rcx]                        | 66 44 87 31                |
    | xchg r15w, word [rcx]                        | 66 44 87 39                |
    | xchg ax, word [rax]                          | 66 87 00                   |
    | xchg ax, word [rdx]                          | 66 87 02                   |
    | xchg ax, word [rbx]                          | 66 87 03                   |
    | xchg ax, word [rsp]                          | 66 87 04 24                |
    | xchg ax, word [rbp]                          | 66 87 45 00                |
    | xchg ax, word [rsi]                          | 66 87 06                   |
    | xchg ax, word [rdi]                          | 66 87 07                   |
    | xchg ax, word [r8]                           | 66 41 87 00                |
    | xchg ax, word [r9]                           | 66 41 87 01                |
    | xchg ax, word [r10]                          | 66 41 87 02                |
    | xchg ax, word [r11]                          | 66 41 87 03                |
    | xchg ax, word [r12]                          | 66 41 87 04 24             |
    | xchg ax, word [r13]                          | 66 41 87 45 00             |
    | xchg ax, word [r14]                          | 66 41 87 06                |
    | xchg ax, word [r15]                          | 66 41 87 07                |
    | xchg ax, word [rax + 1 * rcx]                | 66 87 04 08                |
    | xchg ax, word [rcx + 1 * rcx]                | 66 87 04 09                |
    | xchg ax, word [rdx + 1 * rcx]                | 66 87 04 0a                |
    | xchg ax, word [rbx + 1 * rcx]                | 66 87 04 0b                |
    | xchg ax, word [rsp + 1 * rcx]                | 66 87 04 0c                |
    | xchg ax, word [rbp + 1 * rcx]                | 66 87 44 0d 00             |
    | xchg ax, word [rsi + 1 * rcx]                | 66 87 04 0e                |
    | xchg ax, word [rdi + 1 * rcx]                | 66 87 04 0f                |
    | xchg ax, word [r8 + 1 * rcx]                 | 66 41 87 04 08             |
    | xchg ax, word [r9 + 1 * rcx]                 | 66 41 87 04 09             |
    | xchg ax, word [r10 + 1 * rcx]                | 66 41 87 04 0a             |
    | xchg ax, word [r11 + 1 * rcx]                | 66 41 87 04 0b             |
    | xchg ax, word [r12 + 1 * rcx]                | 66 41 87 04 0c             |
    | xchg ax, word [r13 + 1 * rcx]                | 66 41 87 44 0d 00          |
    | xchg ax, word [r14 + 1 * rcx]                | 66 41 87 04 0e             |
    | xchg ax, word [r15 + 1 * rcx]                | 66 41 87 04 0f             |
    | xchg ax, word [rax + 1 * rax]                | 66 87 04 00                |
    | xchg ax, word [rax + 1 * rdx]                | 66 87 04 10                |
    | xchg ax, word [rax + 1 * rbx]                | 66 87 04 18                |
    | xchg ax, word [rax + 1 * rbp]                | 66 87 04 28                |
    | xchg ax, word [rax + 1 * rsi]                | 66 87 04 30                |
    | xchg ax, word [rax + 1 * rdi]                | 66 87 04 38                |
    | xchg ax, word [rax + 1 * r8]                 | 66 42 87 04 00             |
    | xchg ax, word [rax + 1 * r9]                 | 66 42 87 04 08             |
    | xchg ax, word [rax + 1 * r10]                | 66 42 87 04 10             |
    | xchg ax, word [rax + 1 * r11]                | 66 42 87 04 18             |
    | xchg ax, word [rax + 1 * r12]                | 66 42 87 04 20             |
    | xchg ax, word [rax + 1 * r13]                | 66 42 87 04 28             |
    | xchg ax, word [rax + 1 * r14]                | 66 42 87 04 30             |
    | xchg ax, word [rax + 1 * r15]                | 66 42 87 04 38             |
    | xchg ax, word [rax + 2 * rcx]                | 66 87 04 48                |
    | xchg ax, word [rax + 4 * rcx]                | 66 87 04 88                |
    | xchg ax, word [rax + 8 * rcx]                | 66 87 04 c8                |
    | xchg ax, word [r8 + 1 * r9]                  | 66 43 87 04 08             |
    | xchg ax, word [r8 + 2 * r9]                  | 66 43 87 04 48             |
    | xchg ax, word [r8 + 4 * r9]                  | 66 43 87 04 88             |
    | xchg ax, word [r8 + 8 * r9]                  | 66 43 87 04 c8             |
    | xchg ax, word [1 * rcx]                      | 66 87 04 0d 00 00 00 00    |
    | xchg ax, word [2 * rcx]                      | 66 87 04 4d 00 00 00 00    |
    | xchg ax, word [4 * rcx]                      | 66 87 04 8d 00 00 00 00    |
    | xchg ax, word [8 * rcx]                      | 66 87 04 cd 00 00 00 00    |
    | xchg ax, word [1 * r9]                       | 66 42 87 04 0d 00 00 00 00 |
    | xchg ax, word [2 * r9]                       | 66 42 87 04 4d 00 00 00 00 |
    | xchg ax, word [4 * r9]                       | 66 42 87 04 8d 00 00 00 00 |
    | xchg ax, word [8 * r9]                       | 66 42 87 04 cd 00 00 00 00 |
    | xchg ax, word [r13 + 8 * r12]                | 66 43 87 44 e5 00          |
    | xchg ax, word [rsp + 4 * r15]                | 66 42 87 04 bc             |
    | xchg ax, word [rax + 1 * rcx + 0x00]         | 66 87 44 08 00             |
    | xchg ax, word [rax + 1 * rcx - 0x00]         | 66 87 44 08 00             |
    | xchg ax, word [rax + 1 * rcx + 0x01]         | 66 87 44 08 01             |
    | xchg ax, word [rax + 1 * rcx - 0x01]         | 66 87 44 08 ff             |
    | xchg ax, word [rax + 1 * rcx + 0x00000001]   | 66 87 84 08 01 00 00 00    |
    | xchg ax, word [rax + 1 * rcx - 0x00000001]   | 66 87 84 08 ff ff ff ff    |
    | xchg ax, word [rax + 1 * rcx + 0x7f]         | 66 87 44 08 7f             |
    | xchg ax, word [rax + 1 * rcx - 0x7f]         | 66 87 44 08 81             |
    | xchg ax, word [rax + 1 * rcx + 0x80]         | 66 87 84 08 80 00 00 00    |
    | xchg ax, word [rax + 1 * rcx - 0x80]         | 66 87 44 08 80             |
    | xchg ax, word [rax + 1 * rcx - 0x81]         | 66 87 84 08 7f ff ff ff    |
    | xchg ax, word [rax + 1 * rcx + 0xff]         | 66 87 84 08 ff 00 00 00    |
    | xchg ax, word [rax + 1 * rcx - 0xff]         | 66 87 84 08 01 ff ff ff    |
    | xchg ax, word [rax + 1 * rcx + 0x7fffffff]   | 66 87 84 08 ff ff ff 7f    |
    | xchg ax, word [rax + 1 * rcx - 0x7fffffff]   | 66 87 84 08 01 00 00 80    |
    | xchg ax, word [rax + 1 * rcx - 0x80000000]   | 66 87 84 08 00 00 00 80    |
    | xchg ax, word [r10 + 0x7f]                   | 66 41 87 42 7f             |
    | xchg ax, word [r10 + 0x80]                   | 66 41 87 82 80 00 00 00    |
    | xchg ax, word [r10 - 0x80]                   | 66 41 87 42 80             |
    | xchg ax, word [r10 - 0x81]                   | 66 41 87 82 7f ff ff ff    |
    | xchg cx, word [rdx]                          | 66 87 0a                   |
    | xchg dx, word [rbx]                          | 66 87 13                   |
    | xchg bx, word [rsp]                          | 66 87 1c 24                |
    | xchg sp, word [rbp]                          | 66 87 65 00                |
    | xchg bp, word [rsi]                          | 66 87 2e                   |
    | xchg si, word [rdi]                          | 66 87 37                   |
    | xchg di, word [r8]                           | 66 41 87 38                |
    | xchg r8w, word [r9]                          | 66 45 87 01                |
    | xchg r9w, word [r10]                         | 66 45 87 0a                |
    | xchg r10w, word [r11]                        | 66 45 87 13                |
    | xchg r11w, word [r12]                        | 66 45 87 1c 24             |
    | xchg r12w, word [r13]                        | 66 45 87 65 00             |
    | xchg r13w, word [r14]                        | 66 45 87 2e                |
    | xchg r14w, word [r15]                        | 66 45 87 37                |
    | xchg r15w, word [rax + 1 * rcx]              | 66 44 87 3c 08             |
    | xchg cx, word [rdx + 1 * rcx]                | 66 87 0c 0a                |
    | xchg dx, word [rbx + 1 * rcx]                | 66 87 14 0b                |
    | xchg bx, word [rsp + 1 * rcx]                | 66 87 1c 0c                |
    | xchg sp, word [rbp + 1 * rcx]                | 66 87 64 0d 00             |
    | xchg bp, word [rsi + 1 * rcx]                | 66 87 2c 0e                |
    | xchg si, word [rdi + 1 * rcx]                | 66 87 34 0f                |
    | xchg di, word [r8 + 1 * rcx]                 | 66 41 87 3c 08             |
    | xchg r8w, word [r9 + 1 * rcx]                | 66 45 87 04 09             |
    | xchg r9w, word [r10 + 1 * rcx]               | 66 45 87 0c 0a             |
    | xchg r10w, word [r11 + 1 * rcx]              | 66 45 87 14 0b             |
    | xchg r11w, word [r12 + 1 * rcx]              | 66 45 87 1c 0c             |
    | xchg r12w, word [r13 + 1 * rcx]              | 66 45 87 64 0d 00          |
    | xchg r13w, word [r14 + 1 * rcx]              | 66 45 87 2c 0e             |
    | xchg r14w, word [r15 + 1 * rcx]              | 66 45 87 34 0f             |
    | xchg r15w, word [rax + 1 * rax]              | 66 44 87 3c 00             |
    | xchg cx, word [rax + 1 * rbx]                | 66 87 0c 18                |
    | xchg dx, word [rax + 1 * rbp]                | 66 87 14 28                |
    | xchg bx, word [rax + 1 * rsi]                | 66 87 1c 30                |
    | xchg sp, word [rax + 1 * rdi]                | 66 87 24 38                |
    | xchg bp, word [rax + 1 * r8]                 | 66 42 87 2c 00             |
    | xchg si, word [rax + 1 * r9]                 | 66 42 87 34 08             |
    | xchg di, word [rax + 1 * r10]                | 66 42 87 3c 10             |
    | xchg r8w, word [rax + 1 * r11]               | 66 46 87 04 18             |
    | xchg r9w, word [rax + 1 * r12]               | 66 46 87 0c 20             |
    | xchg r10w, word [rax + 1 * r13]              | 66 46 87 14 28             |
    | xchg r11w, word [rax + 1 * r14]              | 66 46 87 1c 30             |
    | xchg r12w, word [rax + 1 * r15]              | 66 46 87 24 38             |
    | xchg r13w, word [rax + 2 * rcx]              | 66 44 87 2c 48             |
    | xchg r14w, word [rax + 4 * rcx]              | 66 44 87 34 88             |
    | xchg r15w, word [rax + 8 * rcx]              | 66 44 87 3c c8             |
    | xchg cx, word [r8 + 2 * r9]                  | 66 43 87 0c 48             |
    | xchg dx, word [r8 + 4 * r9]                  | 66 43 87 14 88             |
    | xchg bx, word [r8 + 8 * r9]                  | 66 43 87 1c c8             |
    | xchg sp, word [1 * rcx]                      | 66 87 24 0d 00 00 00 00    |
    | xchg bp, word [2 * rcx]                      | 66 87 2c 4d 00 00 00 00    |
    | xchg si, word [4 * rcx]                      | 66 87 34 8d 00 00 00 00    |
    | xchg di, word [8 * rcx]                      | 66 87 3c cd 00 00 00 00    |
    | xchg r8w, word [1 * r9]                      | 66 46 87 04 0d 00 00 00 00 |
    | xchg r9w, word [2 * r9]                      | 66 46 87 0c 4d 00 00 00 00 |
    | xchg r10w, word [4 * r9]                     | 66 46 87 14 8d 00 00 00 00 |
    | xchg r11w, word [8 * r9]                     | 66 46 87 1c cd 00 00 00 00 |
    | xchg r12w, word [r13 + 8 * r12]              | 66 47 87 64 e5 00          |
    | xchg r13w, word [rsp + 4 * r15]              | 66 46 87 2c bc             |
    | xchg r14w, word [rax + 1 * rcx + 0x00]       | 66 44 87 74 08 00          |
    | xchg r15w, word [rax + 1 * rcx - 0x00]       | 66 44 87 7c 08 00          |
    | xchg cx, word [rax + 1 * rcx - 0x01]         | 66 87 4c 08 ff             |
    | xchg dx, word [rax + 1 * rcx + 0x00000001]   | 66 87 94 08 01 00 00 00    |
    | xchg bx, word [rax + 1 * rcx - 0x00000001]   | 66 87 9c 08 ff ff ff ff    |
    | xchg sp, word [rax + 1 * rcx + 0x7f]         | 66 87 64 08 7f             |
    | xchg bp, word [rax + 1 * rcx - 0x7f]         | 66 87 6c 08 81             |
    | xchg si, word [rax + 1 * rcx + 0x80]         | 66 87 b4 08 80 00 00 00    |
    | xchg di, word [rax + 1 * rcx - 0x80]         | 66 87 7c 08 80             |
    | xchg r8w, word [rax + 1 * rcx - 0x81]        | 66 44 87 84 08 7f ff ff ff |
    | xchg r9w, word [rax + 1 * rcx + 0xff]        | 66 44 87 8c 08 ff 00 00 00 |
    | xchg r10w, word [rax + 1 * rcx - 0xff]       | 66 44 87 94 08 01 ff ff ff |
    | xchg r11w, word [rax + 1 * rcx + 0x7fffffff] | 66 44 87 9c 08 ff ff ff 7f |
    | xchg r12w, word [rax + 1 * rcx - 0x7fffffff] | 66 44 87 a4 08 01 00 00 80 |
    | xchg r13w, word [rax + 1 * rcx - 0x80000000] | 66 44 87 ac 08 00 00 00 80 |
    | xchg r14w, word [r10 + 0x7f]                 | 66 45 87 72 7f             |
    | xchg r15w, word [r10 + 0x80]                 | 66 45 87 ba 80 00 00 00    |
    | xchg cx, word [r10 - 0x81]                   | 66 41 87 8a 7f ff ff ff    |
    | xchg dx, word [rax]                          | 66 87 10                   |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_xchg_reg16_addr16():
    encode(XCHG_REG16_ADDR16)


XCHG_REG8_REG8 = """
    | --------------- | -------- | --- | --------------- | -------- |
    | instruction     | encoding | *** | instruction     | encoding |
    | --------------- | -------- | --- | --------------- | -------- |
    | xchg al, cl     | 86 c8    | *** | xchg al, r10b   | 44 86 d0 |
    | xchg cl, cl     | 86 c9    | *** | xchg al, r11b   | 44 86 d8 |
    | xchg dl, cl     | 86 ca    | *** | xchg al, r12b   | 44 86 e0 |
    | xchg bl, cl     | 86 cb    | *** | xchg al, r13b   | 44 86 e8 |
    | xchg spl, cl    | 40 86 cc | *** | xchg al, r14b   | 44 86 f0 |
    | xchg bpl, cl    | 40 86 cd | *** | xchg al, r15b   | 44 86 f8 |
    | xchg sil, cl    | 40 86 ce | *** | xchg al, ah     | 86 e0    |
    | xchg dil, cl    | 40 86 cf | *** | xchg al, ch     | 86 e8    |
    | xchg r8b, cl    | 41 86 c8 | *** | xchg al, dh     | 86 f0    |
    | xchg r9b, cl    | 41 86 c9 | *** | xchg al, bh     | 86 f8    |
    | xchg r10b, cl   | 41 86 ca | *** | xchg cl, dl     | 86 d1    |
    | xchg r11b, cl   | 41 86 cb | *** | xchg dl, bl     | 86 da    |
    | xchg r12b, cl   | 41 86 cc | *** | xchg bl, spl    | 40 86 e3 |
    | xchg r13b, cl   | 41 86 cd | *** | xchg spl, bpl   | 40 86 ec |
    | xchg r14b, cl   | 41 86 ce | *** | xchg bpl, sil   | 40 86 f5 |
    | xchg r15b, cl   | 41 86 cf | *** | xchg sil, dil   | 40 86 fe |
    | xchg ah, cl     | 86 cc    | *** | xchg dil, r8b   | 44 86 c7 |
    | xchg ch, cl     | 86 cd    | *** | xchg r8b, r9b   | 45 86 c8 |
    | xchg dh, cl     | 86 ce    | *** | xchg r9b, r10b  | 45 86 d1 |
    | xchg bh, cl     | 86 cf    | *** | xchg r10b, r11b | 45 86 da |
    | xchg al, al     | 86 c0    | *** | xchg r11b, r12b | 45 86 e3 |
    | xchg al, dl     | 86 d0    | *** | xchg r12b, r13b | 45 86 ec |
    | xchg al, bl     | 86 d8    | *** | xchg r13b, r14b | 45 86 f5 |
    | xchg al, spl    | 40 86 e0 | *** | xchg r14b, r15b | 45 86 fe |
    | xchg al, bpl    | 40 86 e8 | *** | xchg r15b, ah   | !! !! !! |
    | xchg al, sil    | 40 86 f0 | *** | xchg ah, ch     | 86 ec    |
    | xchg al, dil    | 40 86 f8 | *** | xchg ch, dh     | 86 f5    |
    | xchg al, r8b    | 44 86 c0 | *** | xchg dh, bh     | 86 fe    |
    | xchg al, r9b    | 44 86 c8 | *** | xchg bh, al     | 86 c7    |
    | --------------- | -------- | --- | --------------- | -------- |
"""


def can_encode_xchg_reg8_reg8():
    encode(XCHG_REG8_REG8)


XCHG_REG8_ADDR8 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | xchg al, byte [rcx]                          | 86 01                   |
    | xchg cl, byte [rcx]                          | 86 09                   |
    | xchg dl, byte [rcx]                          | 86 11                   |
    | xchg bl, byte [rcx]                          | 86 19                   |
    | xchg spl, byte [rcx]                         | 40 86 21                |
    | xchg bpl, byte [rcx]                         | 40 86 29                |
    | xchg sil, byte [rcx]                         | 40 86 31                |
    | xchg dil, byte [rcx]                         | 40 86 39                |
    | xchg r8b, byte [rcx]                         | 44 86 01                |
    | xchg r9b, byte [rcx]                         | 44 86 09                |
    | xchg r10b, byte [rcx]                        | 44 86 11                |
    | xchg r11b, byte [rcx]                        | 44 86 19                |
    | xchg r12b, byte [rcx]                        | 44 86 21                |
    | xchg r13b, byte [rcx]                        | 44 86 29                |
    | xchg r14b, byte [rcx]                        | 44 86 31                |
    | xchg r15b, byte [rcx]                        | 44 86 39                |
    | xchg ah, byte [rcx]                          | 86 21                   |
    | xchg ch, byte [rcx]                          | 86 29                   |
    | xchg dh, byte [rcx]                          | 86 31                   |
    | xchg bh, byte [rcx]                          | 86 39                   |
    | xchg al, byte [rax]                          | 86 00                   |
    | xchg al, byte [rdx]                          | 86 02                   |
    | xchg al, byte [rbx]                          | 86 03                   |
    | xchg al, byte [rsp]                          | 86 04 24                |
    | xchg al, byte [rbp]                          | 86 45 00                |
    | xchg al, byte [rsi]                          | 86 06                   |
    | xchg al, byte [rdi]                          | 86 07                   |
    | xchg al, byte [r8]                           | 41 86 00                |
    | xchg al, byte [r9]                           | 41 86 01                |
    | xchg al, byte [r10]                          | 41 86 02                |
    | xchg al, byte [r11]                          | 41 86 03                |
    | xchg al, byte [r12]                          | 41 86 04 24             |
    | xchg al, byte [r13]                          | 41 86 45 00             |
    | xchg al, byte [r14]                          | 41 86 06                |
    | xchg al, byte [r15]                          | 41 86 07                |
    | xchg al, byte [rax + 1 * rcx]                | 86 04 08                |
    | xchg al, byte [rcx + 1 * rcx]                | 86 04 09                |
    | xchg al, byte [rdx + 1 * rcx]                | 86 04 0a                |
    | xchg al, byte [rbx + 1 * rcx]                | 86 04 0b                |
    | xchg al, byte [rsp + 1 * rcx]                | 86 04 0c                |
    | xchg al, byte [rbp + 1 * rcx]                | 86 44 0d 00             |
    | xchg al, byte [rsi + 1 * rcx]                | 86 04 0e                |
    | xchg al, byte [rdi + 1 * rcx]                | 86 04 0f                |
    | xchg al, byte [r8 + 1 * rcx]                 | 41 86 04 08             |
    | xchg al, byte [r9 + 1 * rcx]                 | 41 86 04 09             |
    | xchg al, byte [r10 + 1 * rcx]                | 41 86 04 0a             |
    | xchg al, byte [r11 + 1 * rcx]                | 41 86 04 0b             |
    | xchg al, byte [r12 + 1 * rcx]                | 41 86 04 0c             |
    | xchg al, byte [r13 + 1 * rcx]                | 41 86 44 0d 00          |
    | xchg al, byte [r14 + 1 * rcx]                | 41 86 04 0e             |
    | xchg al, byte [r15 + 1 * rcx]                | 41 86 04 0f             |
    | xchg al, byte [rax + 1 * rax]                | 86 04 00                |
    | xchg al, byte [rax + 1 * rdx]                | 86 04 10                |
    | xchg al, byte [rax + 1 * rbx]                | 86 04 18                |
    | xchg al, byte [rax + 1 * rbp]                | 86 04 28                |
    | xchg al, byte [rax + 1 * rsi]                | 86 04 30                |
    | xchg al, byte [rax + 1 * rdi]                | 86 04 38                |
    | xchg al, byte [rax + 1 * r8]                 | 42 86 04 00             |
    | xchg al, byte [rax + 1 * r9]                 | 42 86 04 08             |
    | xchg al, byte [rax + 1 * r10]                | 42 86 04 10             |
    | xchg al, byte [rax + 1 * r11]                | 42 86 04 18             |
    | xchg al, byte [rax + 1 * r12]                | 42 86 04 20             |
    | xchg al, byte [rax + 1 * r13]                | 42 86 04 28             |
    | xchg al, byte [rax + 1 * r14]                | 42 86 04 30             |
    | xchg al, byte [rax + 1 * r15]                | 42 86 04 38             |
    | xchg al, byte [rax + 2 * rcx]                | 86 04 48                |
    | xchg al, byte [rax + 4 * rcx]                | 86 04 88                |
    | xchg al, byte [rax + 8 * rcx]                | 86 04 c8                |
    | xchg al, byte [r8 + 1 * r9]                  | 43 86 04 08             |
    | xchg al, byte [r8 + 2 * r9]                  | 43 86 04 48             |
    | xchg al, byte [r8 + 4 * r9]                  | 43 86 04 88             |
    | xchg al, byte [r8 + 8 * r9]                  | 43 86 04 c8             |
    | xchg al, byte [1 * rcx]                      | 86 04 0d 00 00 00 00    |
    | xchg al, byte [2 * rcx]                      | 86 04 4d 00 00 00 00    |
    | xchg al, byte [4 * rcx]                      | 86 04 8d 00 00 00 00    |
    | xchg al, byte [8 * rcx]                      | 86 04 cd 00 00 00 00    |
    | xchg al, byte [1 * r9]                       | 42 86 04 0d 00 00 00 00 |
    | xchg al, byte [2 * r9]                       | 42 86 04 4d 00 00 00 00 |
    | xchg al, byte [4 * r9]                       | 42 86 04 8d 00 00 00 00 |
    | xchg al, byte [8 * r9]                       | 42 86 04 cd 00 00 00 00 |
    | xchg al, byte [r13 + 8 * r12]                | 43 86 44 e5 00          |
    | xchg al, byte [rsp + 4 * r15]                | 42 86 04 bc             |
    | xchg al, byte [rax + 1 * rcx + 0x00]         | 86 44 08 00             |
    | xchg al, byte [rax + 1 * rcx - 0x00]         | 86 44 08 00             |
    | xchg al, byte [rax + 1 * rcx + 0x01]         | 86 44 08 01             |
    | xchg al, byte [rax + 1 * rcx - 0x01]         | 86 44 08 ff             |
    | xchg al, byte [rax + 1 * rcx + 0x00000001]   | 86 84 08 01 00 00 00    |
    | xchg al, byte [rax + 1 * rcx - 0x00000001]   | 86 84 08 ff ff ff ff    |
    | xchg al, byte [rax + 1 * rcx + 0x7f]         | 86 44 08 7f             |
    | xchg al, byte [rax + 1 * rcx - 0x7f]         | 86 44 08 81             |
    | xchg al, byte [rax + 1 * rcx + 0x80]         | 86 84 08 80 00 00 00    |
    | xchg al, byte [rax + 1 * rcx - 0x80]         | 86 44 08 80             |
    | xchg al, byte [rax + 1 * rcx - 0x81]         | 86 84 08 7f ff ff ff    |
    | xchg al, byte [rax + 1 * rcx + 0xff]         | 86 84 08 ff 00 00 00    |
    | xchg al, byte [rax + 1 * rcx - 0xff]         | 86 84 08 01 ff ff ff    |
    | xchg al, byte [rax + 1 * rcx + 0x7fffffff]   | 86 84 08 ff ff ff 7f    |
    | xchg al, byte [rax + 1 * rcx - 0x7fffffff]   | 86 84 08 01 00 00 80    |
    | xchg al, byte [rax + 1 * rcx - 0x80000000]   | 86 84 08 00 00 00 80    |
    | xchg al, byte [r10 + 0x7f]                   | 41 86 42 7f             |
    | xchg al, byte [r10 + 0x80]                   | 41 86 82 80 00 00 00    |
    | xchg al, byte [r10 - 0x80]                   | 41 86 42 80             |
    | xchg al, byte [r10 - 0x81]                   | 41 86 82 7f ff ff ff    |
    | xchg cl, byte [rdx]                          | 86 0a                   |
    | xchg dl, byte [rbx]                          | 86 13                   |
    | xchg bl, byte [rsp]                          | 86 1c 24                |
    | xchg spl, byte [rbp]                         | 40 86 65 00             |
    | xchg bpl, byte [rsi]                         | 40 86 2e                |
    | xchg sil, byte [rdi]                         | 40 86 37                |
    | xchg dil, byte [r8]                          | 41 86 38                |
    | xchg r8b, byte [r9]                          | 45 86 01                |
    | xchg r9b, byte [r10]                         | 45 86 0a                |
    | xchg r10b, byte [r11]                        | 45 86 13                |
    | xchg r11b, byte [r12]                        | 45 86 1c 24             |
    | xchg r12b, byte [r13]                        | 45 86 65 00             |
    | xchg r13b, byte [r14]                        | 45 86 2e                |
    | xchg r14b, byte [r15]                        | 45 86 37                |
    | xchg r15b, byte [rax + 1 * rcx]              | 44 86 3c 08             |
    | xchg ah, byte [rcx + 1 * rcx]                | 86 24 09                |
    | xchg ch, byte [rdx + 1 * rcx]                | 86 2c 0a                |
    | xchg dh, byte [rbx + 1 * rcx]                | 86 34 0b                |
    | xchg bh, byte [rsp + 1 * rcx]                | 86 3c 0c                |
    | xchg cl, byte [rsi + 1 * rcx]                | 86 0c 0e                |
    | xchg dl, byte [rdi + 1 * rcx]                | 86 14 0f                |
    | xchg bl, byte [r8 + 1 * rcx]                 | 41 86 1c 08             |
    | xchg spl, byte [r9 + 1 * rcx]                | 41 86 24 09             |
    | xchg bpl, byte [r10 + 1 * rcx]               | 41 86 2c 0a             |
    | xchg sil, byte [r11 + 1 * rcx]               | 41 86 34 0b             |
    | xchg dil, byte [r12 + 1 * rcx]               | 41 86 3c 0c             |
    | xchg r8b, byte [r13 + 1 * rcx]               | 45 86 44 0d 00          |
    | xchg r9b, byte [r14 + 1 * rcx]               | 45 86 0c 0e             |
    | xchg r10b, byte [r15 + 1 * rcx]              | 45 86 14 0f             |
    | xchg r11b, byte [rax + 1 * rax]              | 44 86 1c 00             |
    | xchg r12b, byte [rax + 1 * rdx]              | 44 86 24 10             |
    | xchg r13b, byte [rax + 1 * rbx]              | 44 86 2c 18             |
    | xchg r14b, byte [rax + 1 * rbp]              | 44 86 34 28             |
    | xchg r15b, byte [rax + 1 * rsi]              | 44 86 3c 30             |
    | xchg ah, byte [rax + 1 * rdi]                | 86 24 38                |
    | xchg ch, byte [rax + 1 * r8]                 | !! !! !!                |
    | xchg dh, byte [rax + 1 * r9]                 | !! !! !!                |
    | xchg bh, byte [rax + 1 * r10]                | !! !! !!                |
    | xchg cl, byte [rax + 1 * r12]                | 42 86 0c 20             |
    | xchg dl, byte [rax + 1 * r13]                | 42 86 14 28             |
    | xchg bl, byte [rax + 1 * r14]                | 42 86 1c 30             |
    | xchg spl, byte [rax + 1 * r15]               | 42 86 24 38             |
    | xchg bpl, byte [rax + 2 * rcx]               | 40 86 2c 48             |
    | xchg sil, byte [rax + 4 * rcx]               | 40 86 34 88             |
    | xchg dil, byte [rax + 8 * rcx]               | 40 86 3c c8             |
    | xchg r8b, byte [r8 + 1 * r9]                 | 47 86 04 08             |
    | xchg r9b, byte [r8 + 2 * r9]                 | 47 86 0c 48             |
    | xchg r10b, byte [r8 + 4 * r9]                | 47 86 14 88             |
    | xchg r11b, byte [r8 + 8 * r9]                | 47 86 1c c8             |
    | xchg r12b, byte [1 * rcx]                    | 44 86 24 0d 00 00 00 00 |
    | xchg r13b, byte [2 * rcx]                    | 44 86 2c 4d 00 00 00 00 |
    | xchg r14b, byte [4 * rcx]                    | 44 86 34 8d 00 00 00 00 |
    | xchg r15b, byte [8 * rcx]                    | 44 86 3c cd 00 00 00 00 |
    | xchg ah, byte [1 * r9]                       | !! !! !!                |
    | xchg ch, byte [2 * r9]                       | !! !! !!                |
    | xchg dh, byte [4 * r9]                       | !! !! !!                |
    | xchg bh, byte [8 * r9]                       | !! !! !!                |
    | xchg cl, byte [rsp + 4 * r15]                | 42 86 0c bc             |
    | xchg dl, byte [rax + 1 * rcx + 0x00]         | 86 54 08 00             |
    | xchg bl, byte [rax + 1 * rcx - 0x00]         | 86 5c 08 00             |
    | xchg spl, byte [rax + 1 * rcx + 0x01]        | 40 86 64 08 01          |
    | xchg bpl, byte [rax + 1 * rcx - 0x01]        | 40 86 6c 08 ff          |
    | xchg sil, byte [rax + 1 * rcx + 0x00000001]  | 40 86 b4 08 01 00 00 00 |
    | xchg dil, byte [rax + 1 * rcx - 0x00000001]  | 40 86 bc 08 ff ff ff ff |
    | xchg r8b, byte [rax + 1 * rcx + 0x7f]        | 44 86 44 08 7f          |
    | xchg r9b, byte [rax + 1 * rcx - 0x7f]        | 44 86 4c 08 81          |
    | xchg r10b, byte [rax + 1 * rcx + 0x80]       | 44 86 94 08 80 00 00 00 |
    | xchg r11b, byte [rax + 1 * rcx - 0x80]       | 44 86 5c 08 80          |
    | xchg r12b, byte [rax + 1 * rcx - 0x81]       | 44 86 a4 08 7f ff ff ff |
    | xchg r13b, byte [rax + 1 * rcx + 0xff]       | 44 86 ac 08 ff 00 00 00 |
    | xchg r14b, byte [rax + 1 * rcx - 0xff]       | 44 86 b4 08 01 ff ff ff |
    | xchg r15b, byte [rax + 1 * rcx + 0x7fffffff] | 44 86 bc 08 ff ff ff 7f |
    | xchg ah, byte [rax + 1 * rcx - 0x7fffffff]   | 86 a4 08 01 00 00 80    |
    | xchg ch, byte [rax + 1 * rcx - 0x80000000]   | 86 ac 08 00 00 00 80    |
    | xchg dh, byte [r10 + 0x7f]                   | !! !! !!                |
    | xchg bh, byte [r10 + 0x80]                   | !! !! !!                |
    | xchg cl, byte [r10 - 0x81]                   | 41 86 8a 7f ff ff ff    |
    | xchg dl, byte [rax]                          | 86 10                   |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_xchg_reg8_addr8():
    encode(XCHG_REG8_ADDR8)


XCHG_ADDR64_REG64 = """
    | -------------------------------------------- | ----------------------- |
    | instruction                                  | encoding                |
    | -------------------------------------------- | ----------------------- |
    | xchg qword [rax], rcx                        | 48 87 08                |
    | xchg qword [rcx], rcx                        | 48 87 09                |
    | xchg qword [rdx], rcx                        | 48 87 0a                |
    | xchg qword [rbx], rcx                        | 48 87 0b                |
    | xchg qword [rsp], rcx                        | 48 87 0c 24             |
    | xchg qword [rbp], rcx                        | 48 87 4d 00             |
    | xchg qword [rsi], rcx                        | 48 87 0e                |
    | xchg qword [rdi], rcx                        | 48 87 0f                |
    | xchg qword [r8], rcx                         | 49 87 08                |
    | xchg qword [r9], rcx                         | 49 87 09                |
    | xchg qword [r10], rcx                        | 49 87 0a                |
    | xchg qword [r11], rcx                        | 49 87 0b                |
    | xchg qword [r12], rcx                        | 49 87 0c 24             |
    | xchg qword [r13], rcx                        | 49 87 4d 00             |
    | xchg qword [r14], rcx                        | 49 87 0e                |
    | xchg qword [r15], rcx                        | 49 87 0f                |
    | xchg qword [rax + 1 * rcx], rcx              | 48 87 0c 08             |
    | xchg qword [rcx + 1 * rcx], rcx              | 48 87 0c 09             |
    | xchg qword [rdx + 1 * rcx], rcx              | 48 87 0c 0a             |
    | xchg qword [rbx + 1 * rcx], rcx              | 48 87 0c 0b             |
    | xchg qword [rsp + 1 * rcx], rcx              | 48 87 0c 0c             |
    | xchg qword [rbp + 1 * rcx], rcx              | 48 87 4c 0d 00          |
    | xchg qword [rsi + 1 * rcx], rcx              | 48 87 0c 0e             |
    | xchg qword [rdi + 1 * rcx], rcx              | 48 87 0c 0f             |
    | xchg qword [r8 + 1 * rcx], rcx               | 49 87 0c 08             |
    | xchg qword [r9 + 1 * rcx], rcx               | 49 87 0c 09             |
    | xchg qword [r10 + 1 * rcx], rcx              | 49 87 0c 0a             |
    | xchg qword [r11 + 1 * rcx], rcx              | 49 87 0c 0b             |
    | xchg qword [r12 + 1 * rcx], rcx              | 49 87 0c 0c             |
    | xchg qword [r13 + 1 * rcx], rcx              | 49 87 4c 0d 00          |
    | xchg qword [r14 + 1 * rcx], rcx              | 49 87 0c 0e             |
    | xchg qword [r15 + 1 * rcx], rcx              | 49 87 0c 0f             |
    | xchg qword [rax + 1 * rax], rcx              | 48 87 0c 00             |
    | xchg qword [rax + 1 * rdx], rcx              | 48 87 0c 10             |
    | xchg qword [rax + 1 * rbx], rcx              | 48 87 0c 18             |
    | xchg qword [rax + 1 * rbp], rcx              | 48 87 0c 28             |
    | xchg qword [rax + 1 * rsi], rcx              | 48 87 0c 30             |
    | xchg qword [rax + 1 * rdi], rcx              | 48 87 0c 38             |
    | xchg qword [rax + 1 * r8], rcx               | 4a 87 0c 00             |
    | xchg qword [rax + 1 * r9], rcx               | 4a 87 0c 08             |
    | xchg qword [rax + 1 * r10], rcx              | 4a 87 0c 10             |
    | xchg qword [rax + 1 * r11], rcx              | 4a 87 0c 18             |
    | xchg qword [rax + 1 * r12], rcx              | 4a 87 0c 20             |
    | xchg qword [rax + 1 * r13], rcx              | 4a 87 0c 28             |
    | xchg qword [rax + 1 * r14], rcx              | 4a 87 0c 30             |
    | xchg qword [rax + 1 * r15], rcx              | 4a 87 0c 38             |
    | xchg qword [rax + 2 * rcx], rcx              | 48 87 0c 48             |
    | xchg qword [rax + 4 * rcx], rcx              | 48 87 0c 88             |
    | xchg qword [rax + 8 * rcx], rcx              | 48 87 0c c8             |
    | xchg qword [r8 + 1 * r9], rcx                | 4b 87 0c 08             |
    | xchg qword [r8 + 2 * r9], rcx                | 4b 87 0c 48             |
    | xchg qword [r8 + 4 * r9], rcx                | 4b 87 0c 88             |
    | xchg qword [r8 + 8 * r9], rcx                | 4b 87 0c c8             |
    | xchg qword [1 * rcx], rcx                    | 48 87 0c 0d 00 00 00 00 |
    | xchg qword [2 * rcx], rcx                    | 48 87 0c 4d 00 00 00 00 |
    | xchg qword [4 * rcx], rcx                    | 48 87 0c 8d 00 00 00 00 |
    | xchg qword [8 * rcx], rcx                    | 48 87 0c cd 00 00 00 00 |
    | xchg qword [1 * r9], rcx                     | 4a 87 0c 0d 00 00 00 00 |
    | xchg qword [2 * r9], rcx                     | 4a 87 0c 4d 00 00 00 00 |
    | xchg qword [4 * r9], rcx                     | 4a 87 0c 8d 00 00 00 00 |
    | xchg qword [8 * r9], rcx                     | 4a 87 0c cd 00 00 00 00 |
    | xchg qword [r13 + 8 * r12], rcx              | 4b 87 4c e5 00          |
    | xchg qword [rsp + 4 * r15], rcx              | 4a 87 0c bc             |
    | xchg qword [rax + 1 * rcx + 0x00], rcx       | 48 87 4c 08 00          |
    | xchg qword [rax + 1 * rcx - 0x00], rcx       | 48 87 4c 08 00          |
    | xchg qword [rax + 1 * rcx + 0x01], rcx       | 48 87 4c 08 01          |
    | xchg qword [rax + 1 * rcx - 0x01], rcx       | 48 87 4c 08 ff          |
    | xchg qword [rax + 1 * rcx + 0x00000001], rcx | 48 87 8c 08 01 00 00 00 |
    | xchg qword [rax + 1 * rcx - 0x00000001], rcx | 48 87 8c 08 ff ff ff ff |
    | xchg qword [rax + 1 * rcx + 0x7f], rcx       | 48 87 4c 08 7f          |
    | xchg qword [rax + 1 * rcx - 0x7f], rcx       | 48 87 4c 08 81          |
    | xchg qword [rax + 1 * rcx + 0x80], rcx       | 48 87 8c 08 80 00 00 00 |
    | xchg qword [rax + 1 * rcx - 0x80], rcx       | 48 87 4c 08 80          |
    | xchg qword [rax + 1 * rcx - 0x81], rcx       | 48 87 8c 08 7f ff ff ff |
    | xchg qword [rax + 1 * rcx + 0xff], rcx       | 48 87 8c 08 ff 00 00 00 |
    | xchg qword [rax + 1 * rcx - 0xff], rcx       | 48 87 8c 08 01 ff ff ff |
    | xchg qword [rax + 1 * rcx + 0x7fffffff], rcx | 48 87 8c 08 ff ff ff 7f |
    | xchg qword [rax + 1 * rcx - 0x7fffffff], rcx | 48 87 8c 08 01 00 00 80 |
    | xchg qword [rax + 1 * rcx - 0x80000000], rcx | 48 87 8c 08 00 00 00 80 |
    | xchg qword [r10 + 0x7f], rcx                 | 49 87 4a 7f             |
    | xchg qword [r10 + 0x80], rcx                 | 49 87 8a 80 00 00 00    |
    | xchg qword [r10 - 0x80], rcx                 | 49 87 4a 80             |
    | xchg qword [r10 - 0x81], rcx                 | 49 87 8a 7f ff ff ff    |
    | xchg qword [rax], rax                        | 48 87 00                |
    | xchg qword [rax], rdx                        | 48 87 10                |
    | xchg qword [rax], rbx                        | 48 87 18                |
    | xchg qword [rax], rsp                        | 48 87 20                |
    | xchg qword [rax], rbp                        | 48 87 28                |
    | xchg qword [rax], rsi                        | 48 87 30                |
    | xchg qword [rax], rdi                        | 48 87 38                |
    | xchg qword [rax], r8                         | 4c 87 00                |
    | xchg qword [rax], r9                         | 4c 87 08                |
    | xchg qword [rax], r10                        | 4c 87 10                |
    | xchg qword [rax], r11                        | 4c 87 18                |
    | xchg qword [rax], r12                        | 4c 87 20                |
    | xchg qword [rax], r13                        | 4c 87 28                |
    | xchg qword [rax], r14                        | 4c 87 30                |
    | xchg qword [rax], r15                        | 4c 87 38                |
    | xchg qword [rcx], rdx                        | 48 87 11                |
    | xchg qword [rdx], rbx                        | 48 87 1a                |
    | xchg qword [rbx], rsp                        | 48 87 23                |
    | xchg qword [rsp], rbp                        | 48 87 2c 24             |
    | xchg qword [rbp], rsi                        | 48 87 75 00             |
    | xchg qword [rsi], rdi                        | 48 87 3e                |
    | xchg qword [rdi], r8                         | 4c 87 07                |
    | xchg qword [r8], r9                          | 4d 87 08                |
    | xchg qword [r9], r10                         | 4d 87 11                |
    | xchg qword [r10], r11                        | 4d 87 1a                |
    | xchg qword [r11], r12                        | 4d 87 23                |
    | xchg qword [r12], r13                        | 4d 87 2c 24             |
    | xchg qword [r13], r14                        | 4d 87 75 00             |
    | xchg qword [r14], r15                        | 4d 87 3e                |
    | xchg qword [r15], rax                        | 49 87 07                |
    | xchg qword [rcx + 1 * rcx], rdx              | 48 87 14 09             |
    | xchg qword [rdx + 1 * rcx], rbx              | 48 87 1c 0a             |
    | xchg qword [rbx + 1 * rcx], rsp              | 48 87 24 0b             |
    | xchg qword [rsp + 1 * rcx], rbp              | 48 87 2c 0c             |
    | xchg qword [rbp + 1 * rcx], rsi              | 48 87 74 0d 00          |
    | xchg qword [rsi + 1 * rcx], rdi              | 48 87 3c 0e             |
    | xchg qword [rdi + 1 * rcx], r8               | 4c 87 04 0f             |
    | xchg qword [r8 + 1 * rcx], r9                | 4d 87 0c 08             |
    | xchg qword [r9 + 1 * rcx], r10               | 4d 87 14 09             |
    | xchg qword [r10 + 1 * rcx], r11              | 4d 87 1c 0a             |
    | xchg qword [r11 + 1 * rcx], r12              | 4d 87 24 0b             |
    | xchg qword [r12 + 1 * rcx], r13              | 4d 87 2c 0c             |
    | xchg qword [r13 + 1 * rcx], r14              | 4d 87 74 0d 00          |
    | xchg qword [r14 + 1 * rcx], r15              | 4d 87 3c 0e             |
    | xchg qword [r15 + 1 * rcx], rax              | 49 87 04 0f             |
    | xchg qword [rax + 1 * rdx], rdx              | 48 87 14 10             |
    | xchg qword [rax + 1 * rbx], rbx              | 48 87 1c 18             |
    | xchg qword [rax + 1 * rbp], rsp              | 48 87 24 28             |
    | xchg qword [rax + 1 * rsi], rbp              | 48 87 2c 30             |
    | xchg qword [rax + 1 * rdi], rsi              | 48 87 34 38             |
    | xchg qword [rax + 1 * r8], rdi               | 4a 87 3c 00             |
    | xchg qword [rax + 1 * r9], r8                | 4e 87 04 08             |
    | xchg qword [rax + 1 * r10], r9               | 4e 87 0c 10             |
    | xchg qword [rax + 1 * r11], r10              | 4e 87 14 18             |
    | xchg qword [rax + 1 * r12], r11              | 4e 87 1c 20             |
    | xchg qword [rax + 1 * r13], r12              | 4e 87 24 28             |
    | xchg qword [rax + 1 * r14], r13              | 4e 87 2c 30             |
    | xchg qword [rax + 1 * r15], r14              | 4e 87 34 38             |
    | xchg qword [rax + 2 * rcx], r15              | 4c 87 3c 48             |
    | xchg qword [rax + 4 * rcx], rax              | 48 87 04 88             |
    | xchg qword [r8 + 1 * r9], rdx                | 4b 87 14 08             |
    | xchg qword [r8 + 2 * r9], rbx                | 4b 87 1c 48             |
    | xchg qword [r8 + 4 * r9], rsp                | 4b 87 24 88             |
    | xchg qword [r8 + 8 * r9], rbp                | 4b 87 2c c8             |
    | xchg qword [1 * rcx], rsi                    | 48 87 34 0d 00 00 00 00 |
    | xchg qword [2 * rcx], rdi                    | 48 87 3c 4d 00 00 00 00 |
    | xchg qword [4 * rcx], r8                     | 4c 87 04 8d 00 00 00 00 |
    | xchg qword [8 * rcx], r9                     | 4c 87 0c cd 00 00 00 00 |
    | xchg qword [1 * r9], r10                     | 4e 87 14 0d 00 00 00 00 |
    | xchg qword [2 * r9], r11                     | 4e 87 1c 4d 00 00 00 00 |
    | xchg qword [4 * r9], r12                     | 4e 87 24 8d 00 00 00 00 |
    | xchg qword [8 * r9], r13                     | 4e 87 2c cd 00 00 00 00 |
    | xchg qword [r13 + 8 * r12], r14              | 4f 87 74 e5 00          |
    | xchg qword [rsp + 4 * r15], r15              | 4e 87 3c bc             |
    | xchg qword [rax + 1 * rcx + 0x00], rax       | 48 87 44 08 00          |
    | xchg qword [rax + 1 * rcx + 0x01], rdx       | 48 87 54 08 01          |
    | xchg qword [rax + 1 * rcx - 0x01], rbx       | 48 87 5c 08 ff          |
    | xchg qword [rax + 1 * rcx + 0x00000001], rsp | 48 87 a4 08 01 00 00 00 |
    | xchg qword [rax + 1 * rcx - 0x00000001], rbp | 48 87 ac 08 ff ff ff ff |
    | xchg qword [rax + 1 * rcx + 0x7f], rsi       | 48 87 74 08 7f          |
    | xchg qword [rax + 1 * rcx - 0x7f], rdi       | 48 87 7c 08 81          |
    | xchg qword [rax + 1 * rcx + 0x80], r8        | 4c 87 84 08 80 00 00 00 |
    | xchg qword [rax + 1 * rcx - 0x80], r9        | 4c 87 4c 08 80          |
    | xchg qword [rax + 1 * rcx - 0x81], r10       | 4c 87 94 08 7f ff ff ff |
    | xchg qword [rax + 1 * rcx + 0xff], r11       | 4c 87 9c 08 ff 00 00 00 |
    | xchg qword [rax + 1 * rcx - 0xff], r12       | 4c 87 a4 08 01 ff ff ff |
    | xchg qword [rax + 1 * rcx + 0x7fffffff], r13 | 4c 87 ac 08 ff ff ff 7f |
    | xchg qword [rax + 1 * rcx - 0x7fffffff], r14 | 4c 87 b4 08 01 00 00 80 |
    | xchg qword [rax + 1 * rcx - 0x80000000], r15 | 4c 87 bc 08 00 00 00 80 |
    | xchg qword [r10 + 0x7f], rax                 | 49 87 42 7f             |
    | xchg qword [r10 - 0x80], rdx                 | 49 87 52 80             |
    | xchg qword [r10 - 0x81], rbx                 | 49 87 9a 7f ff ff ff    |
    | -------------------------------------------- | ----------------------- |
"""


def can_encode_xchg_addr64_reg64():
    encode(XCHG_ADDR64_REG64)


XCHG_ADDR32_REG32 = """
    | --------------------------------------------- | ----------------------- |
    | instruction                                   | encoding                |
    | --------------------------------------------- | ----------------------- |
    | xchg dword [rax], ecx                         | 87 08                   |
    | xchg dword [rcx], ecx                         | 87 09                   |
    | xchg dword [rdx], ecx                         | 87 0a                   |
    | xchg dword [rbx], ecx                         | 87 0b                   |
    | xchg dword [rsp], ecx                         | 87 0c 24                |
    | xchg dword [rbp], ecx                         | 87 4d 00                |
    | xchg dword [rsi], ecx                         | 87 0e                   |
    | xchg dword [rdi], ecx                         | 87 0f                   |
    | xchg dword [r8], ecx                          | 41 87 08                |
    | xchg dword [r9], ecx                          | 41 87 09                |
    | xchg dword [r10], ecx                         | 41 87 0a                |
    | xchg dword [r11], ecx                         | 41 87 0b                |
    | xchg dword [r12], ecx                         | 41 87 0c 24             |
    | xchg dword [r13], ecx                         | 41 87 4d 00             |
    | xchg dword [r14], ecx                         | 41 87 0e                |
    | xchg dword [r15], ecx                         | 41 87 0f                |
    | xchg dword [rax + 1 * rcx], ecx               | 87 0c 08                |
    | xchg dword [rcx + 1 * rcx], ecx               | 87 0c 09                |
    | xchg dword [rdx + 1 * rcx], ecx               | 87 0c 0a                |
    | xchg dword [rbx + 1 * rcx], ecx               | 87 0c 0b                |
    | xchg dword [rsp + 1 * rcx], ecx               | 87 0c 0c                |
    | xchg dword [rbp + 1 * rcx], ecx               | 87 4c 0d 00             |
    | xchg dword [rsi + 1 * rcx], ecx               | 87 0c 0e                |
    | xchg dword [rdi + 1 * rcx], ecx               | 87 0c 0f                |
    | xchg dword [r8 + 1 * rcx], ecx                | 41 87 0c 08             |
    | xchg dword [r9 + 1 * rcx], ecx                | 41 87 0c 09             |
    | xchg dword [r10 + 1 * rcx], ecx               | 41 87 0c 0a             |
    | xchg dword [r11 + 1 * rcx], ecx               | 41 87 0c 0b             |
    | xchg dword [r12 + 1 * rcx], ecx               | 41 87 0c 0c             |
    | xchg dword [r13 + 1 * rcx], ecx               | 41 87 4c 0d 00          |
    | xchg dword [r14 + 1 * rcx], ecx               | 41 87 0c 0e             |
    | xchg dword [r15 + 1 * rcx], ecx               | 41 87 0c 0f             |
    | xchg dword [rax + 1 * rax], ecx               | 87 0c 00                |
    | xchg dword [rax + 1 * rdx], ecx               | 87 0c 10                |
    | xchg dword [rax + 1 * rbx], ecx               | 87 0c 18                |
    | xchg dword [rax + 1 * rbp], ecx               | 87 0c 28                |
    | xchg dword [rax + 1 * rsi], ecx               | 87 0c 30                |
    | xchg dword [rax + 1 * rdi], ecx               | 87 0c 38                |
    | xchg dword [rax + 1 * r8], ecx                | 42 87 0c 00             |
    | xchg dword [rax + 1 * r9], ecx                | 42 87 0c 08             |
    | xchg dword [rax + 1 * r10], ecx               | 42 87 0c 10             |
    | xchg dword [rax + 1 * r11], ecx               | 42 87 0c 18             |
    | xchg dword [rax + 1 * r12], ecx               | 42 87 0c 20             |
    | xchg dword [rax + 1 * r13], ecx               | 42 87 0c 28             |
    | xchg dword [rax + 1 * r14], ecx               | 42 87 0c 30             |
    | xchg dword [rax + 1 * r15], ecx               | 42 87 0c 38             |
    | xchg dword [rax + 2 * rcx], ecx               | 87 0c 48                |
    | xchg dword [rax + 4 * rcx], ecx               | 87 0c 88                |
    | xchg dword [rax + 8 * rcx], ecx               | 87 0c c8                |
    | xchg dword [r8 + 1 * r9], ecx                 | 43 87 0c 08             |
    | xchg dword [r8 + 2 * r9], ecx                 | 43 87 0c 48             |
    | xchg dword [r8 + 4 * r9], ecx                 | 43 87 0c 88             |
    | xchg dword [r8 + 8 * r9], ecx                 | 43 87 0c c8             |
    | xchg dword [1 * rcx], ecx                     | 87 0c 0d 00 00 00 00    |
    | xchg dword [2 * rcx], ecx                     | 87 0c 4d 00 00 00 00    |
    | xchg dword [4 * rcx], ecx                     | 87 0c 8d 00 00 00 00    |
    | xchg dword [8 * rcx], ecx                     | 87 0c cd 00 00 00 00    |
    | xchg dword [1 * r9], ecx                      | 42 87 0c 0d 00 00 00 00 |
    | xchg dword [2 * r9], ecx                      | 42 87 0c 4d 00 00 00 00 |
    | xchg dword [4 * r9], ecx                      | 42 87 0c 8d 00 00 00 00 |
    | xchg dword [8 * r9], ecx                      | 42 87 0c cd 00 00 00 00 |
    | xchg dword [r13 + 8 * r12], ecx               | 43 87 4c e5 00          |
    | xchg dword [rsp + 4 * r15], ecx               | 42 87 0c bc             |
    | xchg dword [rax + 1 * rcx + 0x00], ecx        | 87 4c 08 00             |
    | xchg dword [rax + 1 * rcx - 0x00], ecx        | 87 4c 08 00             |
    | xchg dword [rax + 1 * rcx + 0x01], ecx        | 87 4c 08 01             |
    | xchg dword [rax + 1 * rcx - 0x01], ecx        | 87 4c 08 ff             |
    | xchg dword [rax + 1 * rcx + 0x00000001], ecx  | 87 8c 08 01 00 00 00    |
    | xchg dword [rax + 1 * rcx - 0x00000001], ecx  | 87 8c 08 ff ff ff ff    |
    | xchg dword [rax + 1 * rcx + 0x7f], ecx        | 87 4c 08 7f             |
    | xchg dword [rax + 1 * rcx - 0x7f], ecx        | 87 4c 08 81             |
    | xchg dword [rax + 1 * rcx + 0x80], ecx        | 87 8c 08 80 00 00 00    |
    | xchg dword [rax + 1 * rcx - 0x80], ecx        | 87 4c 08 80             |
    | xchg dword [rax + 1 * rcx - 0x81], ecx        | 87 8c 08 7f ff ff ff    |
    | xchg dword [rax + 1 * rcx + 0xff], ecx        | 87 8c 08 ff 00 00 00    |
    | xchg dword [rax + 1 * rcx - 0xff], ecx        | 87 8c 08 01 ff ff ff    |
    | xchg dword [rax + 1 * rcx + 0x7fffffff], ecx  | 87 8c 08 ff ff ff 7f    |
    | xchg dword [rax + 1 * rcx - 0x7fffffff], ecx  | 87 8c 08 01 00 00 80    |
    | xchg dword [rax + 1 * rcx - 0x80000000], ecx  | 87 8c 08 00 00 00 80    |
    | xchg dword [r10 + 0x7f], ecx                  | 41 87 4a 7f             |
    | xchg dword [r10 + 0x80], ecx                  | 41 87 8a 80 00 00 00    |
    | xchg dword [r10 - 0x80], ecx                  | 41 87 4a 80             |
    | xchg dword [r10 - 0x81], ecx                  | 41 87 8a 7f ff ff ff    |
    | xchg dword [rax], eax                         | 87 00                   |
    | xchg dword [rax], edx                         | 87 10                   |
    | xchg dword [rax], ebx                         | 87 18                   |
    | xchg dword [rax], esp                         | 87 20                   |
    | xchg dword [rax], ebp                         | 87 28                   |
    | xchg dword [rax], esi                         | 87 30                   |
    | xchg dword [rax], edi                         | 87 38                   |
    | xchg dword [rax], r8d                         | 44 87 00                |
    | xchg dword [rax], r9d                         | 44 87 08                |
    | xchg dword [rax], r10d                        | 44 87 10                |
    | xchg dword [rax], r11d                        | 44 87 18                |
    | xchg dword [rax], r12d                        | 44 87 20                |
    | xchg dword [rax], r13d                        | 44 87 28                |
    | xchg dword [rax], r14d                        | 44 87 30                |
    | xchg dword [rax], r15d                        | 44 87 38                |
    | xchg dword [rcx], edx                         | 87 11                   |
    | xchg dword [rdx], ebx                         | 87 1a                   |
    | xchg dword [rbx], esp                         | 87 23                   |
    | xchg dword [rsp], ebp                         | 87 2c 24                |
    | xchg dword [rbp], esi                         | 87 75 00                |
    | xchg dword [rsi], edi                         | 87 3e                   |
    | xchg dword [rdi], r8d                         | 44 87 07                |
    | xchg dword [r8], r9d                          | 45 87 08                |
    | xchg dword [r9], r10d                         | 45 87 11                |
    | xchg dword [r10], r11d                        | 45 87 1a                |
    | xchg dword [r11], r12d                        | 45 87 23                |
    | xchg dword [r12], r13d                        | 45 87 2c 24             |
    | xchg dword [r13], r14d                        | 45 87 75 00             |
    | xchg dword [r14], r15d                        | 45 87 3e                |
    | xchg dword [r15], eax                         | 41 87 07                |
    | xchg dword [rcx + 1 * rcx], edx               | 87 14 09                |
    | xchg dword [rdx + 1 * rcx], ebx               | 87 1c 0a                |
    | xchg dword [rbx + 1 * rcx], esp               | 87 24 0b                |
    | xchg dword [rsp + 1 * rcx], ebp               | 87 2c 0c                |
    | xchg dword [rbp + 1 * rcx], esi               | 87 74 0d 00             |
    | xchg dword [rsi + 1 * rcx], edi               | 87 3c 0e                |
    | xchg dword [rdi + 1 * rcx], r8d               | 44 87 04 0f             |
    | xchg dword [r8 + 1 * rcx], r9d                | 45 87 0c 08             |
    | xchg dword [r9 + 1 * rcx], r10d               | 45 87 14 09             |
    | xchg dword [r10 + 1 * rcx], r11d              | 45 87 1c 0a             |
    | xchg dword [r11 + 1 * rcx], r12d              | 45 87 24 0b             |
    | xchg dword [r12 + 1 * rcx], r13d              | 45 87 2c 0c             |
    | xchg dword [r13 + 1 * rcx], r14d              | 45 87 74 0d 00          |
    | xchg dword [r14 + 1 * rcx], r15d              | 45 87 3c 0e             |
    | xchg dword [r15 + 1 * rcx], eax               | 41 87 04 0f             |
    | xchg dword [rax + 1 * rdx], edx               | 87 14 10                |
    | xchg dword [rax + 1 * rbx], ebx               | 87 1c 18                |
    | xchg dword [rax + 1 * rbp], esp               | 87 24 28                |
    | xchg dword [rax + 1 * rsi], ebp               | 87 2c 30                |
    | xchg dword [rax + 1 * rdi], esi               | 87 34 38                |
    | xchg dword [rax + 1 * r8], edi                | 42 87 3c 00             |
    | xchg dword [rax + 1 * r9], r8d                | 46 87 04 08             |
    | xchg dword [rax + 1 * r10], r9d               | 46 87 0c 10             |
    | xchg dword [rax + 1 * r11], r10d              | 46 87 14 18             |
    | xchg dword [rax + 1 * r12], r11d              | 46 87 1c 20             |
    | xchg dword [rax + 1 * r13], r12d              | 46 87 24 28             |
    | xchg dword [rax + 1 * r14], r13d              | 46 87 2c 30             |
    | xchg dword [rax + 1 * r15], r14d              | 46 87 34 38             |
    | xchg dword [rax + 2 * rcx], r15d              | 44 87 3c 48             |
    | xchg dword [rax + 4 * rcx], eax               | 87 04 88                |
    | xchg dword [r8 + 1 * r9], edx                 | 43 87 14 08             |
    | xchg dword [r8 + 2 * r9], ebx                 | 43 87 1c 48             |
    | xchg dword [r8 + 4 * r9], esp                 | 43 87 24 88             |
    | xchg dword [r8 + 8 * r9], ebp                 | 43 87 2c c8             |
    | xchg dword [1 * rcx], esi                     | 87 34 0d 00 00 00 00    |
    | xchg dword [2 * rcx], edi                     | 87 3c 4d 00 00 00 00    |
    | xchg dword [4 * rcx], r8d                     | 44 87 04 8d 00 00 00 00 |
    | xchg dword [8 * rcx], r9d                     | 44 87 0c cd 00 00 00 00 |
    | xchg dword [1 * r9], r10d                     | 46 87 14 0d 00 00 00 00 |
    | xchg dword [2 * r9], r11d                     | 46 87 1c 4d 00 00 00 00 |
    | xchg dword [4 * r9], r12d                     | 46 87 24 8d 00 00 00 00 |
    | xchg dword [8 * r9], r13d                     | 46 87 2c cd 00 00 00 00 |
    | xchg dword [r13 + 8 * r12], r14d              | 47 87 74 e5 00          |
    | xchg dword [rsp + 4 * r15], r15d              | 46 87 3c bc             |
    | xchg dword [rax + 1 * rcx + 0x00], eax        | 87 44 08 00             |
    | xchg dword [rax + 1 * rcx + 0x01], edx        | 87 54 08 01             |
    | xchg dword [rax + 1 * rcx - 0x01], ebx        | 87 5c 08 ff             |
    | xchg dword [rax + 1 * rcx + 0x00000001], esp  | 87 a4 08 01 00 00 00    |
    | xchg dword [rax + 1 * rcx - 0x00000001], ebp  | 87 ac 08 ff ff ff ff    |
    | xchg dword [rax + 1 * rcx + 0x7f], esi        | 87 74 08 7f             |
    | xchg dword [rax + 1 * rcx - 0x7f], edi        | 87 7c 08 81             |
    | xchg dword [rax + 1 * rcx + 0x80], r8d        | 44 87 84 08 80 00 00 00 |
    | xchg dword [rax + 1 * rcx - 0x80], r9d        | 44 87 4c 08 80          |
    | xchg dword [rax + 1 * rcx - 0x81], r10d       | 44 87 94 08 7f ff ff ff |
    | xchg dword [rax + 1 * rcx + 0xff], r11d       | 44 87 9c 08 ff 00 00 00 |
    | xchg dword [rax + 1 * rcx - 0xff], r12d       | 44 87 a4 08 01 ff ff ff |
    | xchg dword [rax + 1 * rcx + 0x7fffffff], r13d | 44 87 ac 08 ff ff ff 7f |
    | xchg dword [rax + 1 * rcx - 0x7fffffff], r14d | 44 87 b4 08 01 00 00 80 |
    | xchg dword [rax + 1 * rcx - 0x80000000], r15d | 44 87 bc 08 00 00 00 80 |
    | xchg dword [r10 + 0x7f], eax                  | 41 87 42 7f             |
    | xchg dword [r10 - 0x80], edx                  | 41 87 52 80             |
    | xchg dword [r10 - 0x81], ebx                  | 41 87 9a 7f ff ff ff    |
    | --------------------------------------------- | ----------------------- |
"""


def can_encode_xchg_addr32_reg32():
    encode(XCHG_ADDR32_REG32)


XCHG_ADDR16_REG16 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | xchg word [rax], cx                          | 66 87 08                   |
    | xchg word [rcx], cx                          | 66 87 09                   |
    | xchg word [rdx], cx                          | 66 87 0a                   |
    | xchg word [rbx], cx                          | 66 87 0b                   |
    | xchg word [rsp], cx                          | 66 87 0c 24                |
    | xchg word [rbp], cx                          | 66 87 4d 00                |
    | xchg word [rsi], cx                          | 66 87 0e                   |
    | xchg word [rdi], cx                          | 66 87 0f                   |
    | xchg word [r8], cx                           | 66 41 87 08                |
    | xchg word [r9], cx                           | 66 41 87 09                |
    | xchg word [r10], cx                          | 66 41 87 0a                |
    | xchg word [r11], cx                          | 66 41 87 0b                |
    | xchg word [r12], cx                          | 66 41 87 0c 24             |
    | xchg word [r13], cx                          | 66 41 87 4d 00             |
    | xchg word [r14], cx                          | 66 41 87 0e                |
    | xchg word [r15], cx                          | 66 41 87 0f                |
    | xchg word [rax + 1 * rcx], cx                | 66 87 0c 08                |
    | xchg word [rcx + 1 * rcx], cx                | 66 87 0c 09                |
    | xchg word [rdx + 1 * rcx], cx                | 66 87 0c 0a                |
    | xchg word [rbx + 1 * rcx], cx                | 66 87 0c 0b                |
    | xchg word [rsp + 1 * rcx], cx                | 66 87 0c 0c                |
    | xchg word [rbp + 1 * rcx], cx                | 66 87 4c 0d 00             |
    | xchg word [rsi + 1 * rcx], cx                | 66 87 0c 0e                |
    | xchg word [rdi + 1 * rcx], cx                | 66 87 0c 0f                |
    | xchg word [r8 + 1 * rcx], cx                 | 66 41 87 0c 08             |
    | xchg word [r9 + 1 * rcx], cx                 | 66 41 87 0c 09             |
    | xchg word [r10 + 1 * rcx], cx                | 66 41 87 0c 0a             |
    | xchg word [r11 + 1 * rcx], cx                | 66 41 87 0c 0b             |
    | xchg word [r12 + 1 * rcx], cx                | 66 41 87 0c 0c             |
    | xchg word [r13 + 1 * rcx], cx                | 66 41 87 4c 0d 00          |
    | xchg word [r14 + 1 * rcx], cx                | 66 41 87 0c 0e             |
    | xchg word [r15 + 1 * rcx], cx                | 66 41 87 0c 0f             |
    | xchg word [rax + 1 * rax], cx                | 66 87 0c 00                |
    | xchg word [rax + 1 * rdx], cx                | 66 87 0c 10                |
    | xchg word [rax + 1 * rbx], cx                | 66 87 0c 18                |
    | xchg word [rax + 1 * rbp], cx                | 66 87 0c 28                |
    | xchg word [rax + 1 * rsi], cx                | 66 87 0c 30                |
    | xchg word [rax + 1 * rdi], cx                | 66 87 0c 38                |
    | xchg word [rax + 1 * r8], cx                 | 66 42 87 0c 00             |
    | xchg word [rax + 1 * r9], cx                 | 66 42 87 0c 08             |
    | xchg word [rax + 1 * r10], cx                | 66 42 87 0c 10             |
    | xchg word [rax + 1 * r11], cx                | 66 42 87 0c 18             |
    | xchg word [rax + 1 * r12], cx                | 66 42 87 0c 20             |
    | xchg word [rax + 1 * r13], cx                | 66 42 87 0c 28             |
    | xchg word [rax + 1 * r14], cx                | 66 42 87 0c 30             |
    | xchg word [rax + 1 * r15], cx                | 66 42 87 0c 38             |
    | xchg word [rax + 2 * rcx], cx                | 66 87 0c 48                |
    | xchg word [rax + 4 * rcx], cx                | 66 87 0c 88                |
    | xchg word [rax + 8 * rcx], cx                | 66 87 0c c8                |
    | xchg word [r8 + 1 * r9], cx                  | 66 43 87 0c 08             |
    | xchg word [r8 + 2 * r9], cx                  | 66 43 87 0c 48             |
    | xchg word [r8 + 4 * r9], cx                  | 66 43 87 0c 88             |
    | xchg word [r8 + 8 * r9], cx                  | 66 43 87 0c c8             |
    | xchg word [1 * rcx], cx                      | 66 87 0c 0d 00 00 00 00    |
    | xchg word [2 * rcx], cx                      | 66 87 0c 4d 00 00 00 00    |
    | xchg word [4 * rcx], cx                      | 66 87 0c 8d 00 00 00 00    |
    | xchg word [8 * rcx], cx                      | 66 87 0c cd 00 00 00 00    |
    | xchg word [1 * r9], cx                       | 66 42 87 0c 0d 00 00 00 00 |
    | xchg word [2 * r9], cx                       | 66 42 87 0c 4d 00 00 00 00 |
    | xchg word [4 * r9], cx                       | 66 42 87 0c 8d 00 00 00 00 |
    | xchg word [8 * r9], cx                       | 66 42 87 0c cd 00 00 00 00 |
    | xchg word [r13 + 8 * r12], cx                | 66 43 87 4c e5 00          |
    | xchg word [rsp + 4 * r15], cx                | 66 42 87 0c bc             |
    | xchg word [rax + 1 * rcx + 0x00], cx         | 66 87 4c 08 00             |
    | xchg word [rax + 1 * rcx - 0x00], cx         | 66 87 4c 08 00             |
    | xchg word [rax + 1 * rcx + 0x01], cx         | 66 87 4c 08 01             |
    | xchg word [rax + 1 * rcx - 0x01], cx         | 66 87 4c 08 ff             |
    | xchg word [rax + 1 * rcx + 0x00000001], cx   | 66 87 8c 08 01 00 00 00    |
    | xchg word [rax + 1 * rcx - 0x00000001], cx   | 66 87 8c 08 ff ff ff ff    |
    | xchg word [rax + 1 * rcx + 0x7f], cx         | 66 87 4c 08 7f             |
    | xchg word [rax + 1 * rcx - 0x7f], cx         | 66 87 4c 08 81             |
    | xchg word [rax + 1 * rcx + 0x80], cx         | 66 87 8c 08 80 00 00 00    |
    | xchg word [rax + 1 * rcx - 0x80], cx         | 66 87 4c 08 80             |
    | xchg word [rax + 1 * rcx - 0x81], cx         | 66 87 8c 08 7f ff ff ff    |
    | xchg word [rax + 1 * rcx + 0xff], cx         | 66 87 8c 08 ff 00 00 00    |
    | xchg word [rax + 1 * rcx - 0xff], cx         | 66 87 8c 08 01 ff ff ff    |
    | xchg word [rax + 1 * rcx + 0x7fffffff], cx   | 66 87 8c 08 ff ff ff 7f    |
    | xchg word [rax + 1 * rcx - 0x7fffffff], cx   | 66 87 8c 08 01 00 00 80    |
    | xchg word [rax + 1 * rcx - 0x80000000], cx   | 66 87 8c 08 00 00 00 80    |
    | xchg word [r10 + 0x7f], cx                   | 66 41 87 4a 7f             |
    | xchg word [r10 + 0x80], cx                   | 66 41 87 8a 80 00 00 00    |
    | xchg word [r10 - 0x80], cx                   | 66 41 87 4a 80             |
    | xchg word [r10 - 0x81], cx                   | 66 41 87 8a 7f ff ff ff    |
    | xchg word [rax], ax                          | 66 87 00                   |
    | xchg word [rax], dx                          | 66 87 10                   |
    | xchg word [rax], bx                          | 66 87 18                   |
    | xchg word [rax], sp                          | 66 87 20                   |
    | xchg word [rax], bp                          | 66 87 28                   |
    | xchg word [rax], si                          | 66 87 30                   |
    | xchg word [rax], di                          | 66 87 38                   |
    | xchg word [rax], r8w                         | 66 44 87 00                |
    | xchg word [rax], r9w                         | 66 44 87 08                |
    | xchg word [rax], r10w                        | 66 44 87 10                |
    | xchg word [rax], r11w                        | 66 44 87 18                |
    | xchg word [rax], r12w                        | 66 44 87 20                |
    | xchg word [rax], r13w                        | 66 44 87 28                |
    | xchg word [rax], r14w                        | 66 44 87 30                |
    | xchg word [rax], r15w                        | 66 44 87 38                |
    | xchg word [rcx], dx                          | 66 87 11                   |
    | xchg word [rdx], bx                          | 66 87 1a                   |
    | xchg word [rbx], sp                          | 66 87 23                   |
    | xchg word [rsp], bp                          | 66 87 2c 24                |
    | xchg word [rbp], si                          | 66 87 75 00                |
    | xchg word [rsi], di                          | 66 87 3e                   |
    | xchg word [rdi], r8w                         | 66 44 87 07                |
    | xchg word [r8], r9w                          | 66 45 87 08                |
    | xchg word [r9], r10w                         | 66 45 87 11                |
    | xchg word [r10], r11w                        | 66 45 87 1a                |
    | xchg word [r11], r12w                        | 66 45 87 23                |
    | xchg word [r12], r13w                        | 66 45 87 2c 24             |
    | xchg word [r13], r14w                        | 66 45 87 75 00             |
    | xchg word [r14], r15w                        | 66 45 87 3e                |
    | xchg word [r15], ax                          | 66 41 87 07                |
    | xchg word [rcx + 1 * rcx], dx                | 66 87 14 09                |
    | xchg word [rdx + 1 * rcx], bx                | 66 87 1c 0a                |
    | xchg word [rbx + 1 * rcx], sp                | 66 87 24 0b                |
    | xchg word [rsp + 1 * rcx], bp                | 66 87 2c 0c                |
    | xchg word [rbp + 1 * rcx], si                | 66 87 74 0d 00             |
    | xchg word [rsi + 1 * rcx], di                | 66 87 3c 0e                |
    | xchg word [rdi + 1 * rcx], r8w               | 66 44 87 04 0f             |
    | xchg word [r8 + 1 * rcx], r9w                | 66 45 87 0c 08             |
    | xchg word [r9 + 1 * rcx], r10w               | 66 45 87 14 09             |
    | xchg word [r10 + 1 * rcx], r11w              | 66 45 87 1c 0a             |
    | xchg word [r11 + 1 * rcx], r12w              | 66 45 87 24 0b             |
    | xchg word [r12 + 1 * rcx], r13w              | 66 45 87 2c 0c             |
    | xchg word [r13 + 1 * rcx], r14w              | 66 45 87 74 0d 00          |
    | xchg word [r14 + 1 * rcx], r15w              | 66 45 87 3c 0e             |
    | xchg word [r15 + 1 * rcx], ax                | 66 41 87 04 0f             |
    | xchg word [rax + 1 * rdx], dx                | 66 87 14 10                |
    | xchg word [rax + 1 * rbx], bx                | 66 87 1c 18                |
    | xchg word [rax + 1 * rbp], sp                | 66 87 24 28                |
    | xchg word [rax + 1 * rsi], bp                | 66 87 2c 30                |
    | xchg word [rax + 1 * rdi], si                | 66 87 34 38                |
    | xchg word [rax + 1 * r8], di                 | 66 42 87 3c 00             |
    | xchg word [rax + 1 * r9], r8w                | 66 46 87 04 08             |
    | xchg word [rax + 1 * r10], r9w               | 66 46 87 0c 10             |
    | xchg word [rax + 1 * r11], r10w              | 66 46 87 14 18             |
    | xchg word [rax + 1 * r12], r11w              | 66 46 87 1c 20             |
    | xchg word [rax + 1 * r13], r12w              | 66 46 87 24 28             |
    | xchg word [rax + 1 * r14], r13w              | 66 46 87 2c 30             |
    | xchg word [rax + 1 * r15], r14w              | 66 46 87 34 38             |
    | xchg word [rax + 2 * rcx], r15w              | 66 44 87 3c 48             |
    | xchg word [rax + 4 * rcx], ax                | 66 87 04 88                |
    | xchg word [r8 + 1 * r9], dx                  | 66 43 87 14 08             |
    | xchg word [r8 + 2 * r9], bx                  | 66 43 87 1c 48             |
    | xchg word [r8 + 4 * r9], sp                  | 66 43 87 24 88             |
    | xchg word [r8 + 8 * r9], bp                  | 66 43 87 2c c8             |
    | xchg word [1 * rcx], si                      | 66 87 34 0d 00 00 00 00    |
    | xchg word [2 * rcx], di                      | 66 87 3c 4d 00 00 00 00    |
    | xchg word [4 * rcx], r8w                     | 66 44 87 04 8d 00 00 00 00 |
    | xchg word [8 * rcx], r9w                     | 66 44 87 0c cd 00 00 00 00 |
    | xchg word [1 * r9], r10w                     | 66 46 87 14 0d 00 00 00 00 |
    | xchg word [2 * r9], r11w                     | 66 46 87 1c 4d 00 00 00 00 |
    | xchg word [4 * r9], r12w                     | 66 46 87 24 8d 00 00 00 00 |
    | xchg word [8 * r9], r13w                     | 66 46 87 2c cd 00 00 00 00 |
    | xchg word [r13 + 8 * r12], r14w              | 66 47 87 74 e5 00          |
    | xchg word [rsp + 4 * r15], r15w              | 66 46 87 3c bc             |
    | xchg word [rax + 1 * rcx + 0x00], ax         | 66 87 44 08 00             |
    | xchg word [rax + 1 * rcx + 0x01], dx         | 66 87 54 08 01             |
    | xchg word [rax + 1 * rcx - 0x01], bx         | 66 87 5c 08 ff             |
    | xchg word [rax + 1 * rcx + 0x00000001], sp   | 66 87 a4 08 01 00 00 00    |
    | xchg word [rax + 1 * rcx - 0x00000001], bp   | 66 87 ac 08 ff ff ff ff    |
    | xchg word [rax + 1 * rcx + 0x7f], si         | 66 87 74 08 7f             |
    | xchg word [rax + 1 * rcx - 0x7f], di         | 66 87 7c 08 81             |
    | xchg word [rax + 1 * rcx + 0x80], r8w        | 66 44 87 84 08 80 00 00 00 |
    | xchg word [rax + 1 * rcx - 0x80], r9w        | 66 44 87 4c 08 80          |
    | xchg word [rax + 1 * rcx - 0x81], r10w       | 66 44 87 94 08 7f ff ff ff |
    | xchg word [rax + 1 * rcx + 0xff], r11w       | 66 44 87 9c 08 ff 00 00 00 |
    | xchg word [rax + 1 * rcx - 0xff], r12w       | 66 44 87 a4 08 01 ff ff ff |
    | xchg word [rax + 1 * rcx + 0x7fffffff], r13w | 66 44 87 ac 08 ff ff ff 7f |
    | xchg word [rax + 1 * rcx - 0x7fffffff], r14w | 66 44 87 b4 08 01 00 00 80 |
    | xchg word [rax + 1 * rcx - 0x80000000], r15w | 66 44 87 bc 08 00 00 00 80 |
    | xchg word [r10 + 0x7f], ax                   | 66 41 87 42 7f             |
    | xchg word [r10 - 0x80], dx                   | 66 41 87 52 80             |
    | xchg word [r10 - 0x81], bx                   | 66 41 87 9a 7f ff ff ff    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_xchg_addr16_reg16():
    encode(XCHG_ADDR16_REG16)


XCHG_ADDR8_REG8 = """
    | ------------------------------------------- | ----------------------- |
    | instruction                                 | encoding                |
    | ------------------------------------------- | ----------------------- |
    | xchg byte [rax], cl                         | 86 08                   |
    | xchg byte [rcx], cl                         | 86 09                   |
    | xchg byte [rdx], cl                         | 86 0a                   |
    | xchg byte [rbx], cl                         | 86 0b                   |
    | xchg byte [rsp], cl                         | 86 0c 24                |
    | xchg byte [rbp], cl                         | 86 4d 00                |
    | xchg byte [rsi], cl                         | 86 0e                   |
    | xchg byte [rdi], cl                         | 86 0f                   |
    | xchg byte [r8], cl                          | 41 86 08                |
    | xchg byte [r9], cl                          | 41 86 09                |
    | xchg byte [r10], cl                         | 41 86 0a                |
    | xchg byte [r11], cl                         | 41 86 0b                |
    | xchg byte [r12], cl                         | 41 86 0c 24             |
    | xchg byte [r13], cl                         | 41 86 4d 00             |
    | xchg byte [r14], cl                         | 41 86 0e                |
    | xchg byte [r15], cl                         | 41 86 0f                |
    | xchg byte [rax + 1 * rcx], cl               | 86 0c 08                |
    | xchg byte [rcx + 1 * rcx], cl               | 86 0c 09                |
    | xchg byte [rdx + 1 * rcx], cl               | 86 0c 0a                |
    | xchg byte [rbx + 1 * rcx], cl               | 86 0c 0b                |
    | xchg byte [rsp + 1 * rcx], cl               | 86 0c 0c                |
    | xchg byte [rbp + 1 * rcx], cl               | 86 4c 0d 00             |
    | xchg byte [rsi + 1 * rcx], cl               | 86 0c 0e                |
    | xchg byte [rdi + 1 * rcx], cl               | 86 0c 0f                |
    | xchg byte [r8 + 1 * rcx], cl                | 41 86 0c 08             |
    | xchg byte [r9 + 1 * rcx], cl                | 41 86 0c 09             |
    | xchg byte [r10 + 1 * rcx], cl               | 41 86 0c 0a             |
    | xchg byte [r11 + 1 * rcx], cl               | 41 86 0c 0b             |
    | xchg byte [r12 + 1 * rcx], cl               | 41 86 0c 0c             |
    | xchg byte [r13 + 1 * rcx], cl               | 41 86 4c 0d 00          |
    | xchg byte [r14 + 1 * rcx], cl               | 41 86 0c 0e             |
    | xchg byte [r15 + 1 * rcx], cl               | 41 86 0c 0f             |
    | xchg byte [rax + 1 * rax], cl               | 86 0c 00                |
    | xchg byte [rax + 1 * rdx], cl               | 86 0c 10                |
    | xchg byte [rax + 1 * rbx], cl               | 86 0c 18                |
    | xchg byte [rax + 1 * rbp], cl               | 86 0c 28                |
    | xchg byte [rax + 1 * rsi], cl               | 86 0c 30                |
    | xchg byte [rax + 1 * rdi], cl               | 86 0c 38                |
    | xchg byte [rax + 1 * r8], cl                | 42 86 0c 00             |
    | xchg byte [rax + 1 * r9], cl                | 42 86 0c 08             |
    | xchg byte [rax + 1 * r10], cl               | 42 86 0c 10             |
    | xchg byte [rax + 1 * r11], cl               | 42 86 0c 18             |
    | xchg byte [rax + 1 * r12], cl               | 42 86 0c 20             |
    | xchg byte [rax + 1 * r13], cl               | 42 86 0c 28             |
    | xchg byte [rax + 1 * r14], cl               | 42 86 0c 30             |
    | xchg byte [rax + 1 * r15], cl               | 42 86 0c 38             |
    | xchg byte [rax + 2 * rcx], cl               | 86 0c 48                |
    | xchg byte [rax + 4 * rcx], cl               | 86 0c 88                |
    | xchg byte [rax + 8 * rcx], cl               | 86 0c c8                |
    | xchg byte [r8 + 1 * r9], cl                 | 43 86 0c 08             |
    | xchg byte [r8 + 2 * r9], cl                 | 43 86 0c 48             |
    | xchg byte [r8 + 4 * r9], cl                 | 43 86 0c 88             |
    | xchg byte [r8 + 8 * r9], cl                 | 43 86 0c c8             |
    | xchg byte [1 * rcx], cl                     | 86 0c 0d 00 00 00 00    |
    | xchg byte [2 * rcx], cl                     | 86 0c 4d 00 00 00 00    |
    | xchg byte [4 * rcx], cl                     | 86 0c 8d 00 00 00 00    |
    | xchg byte [8 * rcx], cl                     | 86 0c cd 00 00 00 00    |
    | xchg byte [1 * r9], cl                      | 42 86 0c 0d 00 00 00 00 |
    | xchg byte [2 * r9], cl                      | 42 86 0c 4d 00 00 00 00 |
    | xchg byte [4 * r9], cl                      | 42 86 0c 8d 00 00 00 00 |
    | xchg byte [8 * r9], cl                      | 42 86 0c cd 00 00 00 00 |
    | xchg byte [r13 + 8 * r12], cl               | 43 86 4c e5 00          |
    | xchg byte [rsp + 4 * r15], cl               | 42 86 0c bc             |
    | xchg byte [rax + 1 * rcx + 0x00], cl        | 86 4c 08 00             |
    | xchg byte [rax + 1 * rcx - 0x00], cl        | 86 4c 08 00             |
    | xchg byte [rax + 1 * rcx + 0x01], cl        | 86 4c 08 01             |
    | xchg byte [rax + 1 * rcx - 0x01], cl        | 86 4c 08 ff             |
    | xchg byte [rax + 1 * rcx + 0x00000001], cl  | 86 8c 08 01 00 00 00    |
    | xchg byte [rax + 1 * rcx - 0x00000001], cl  | 86 8c 08 ff ff ff ff    |
    | xchg byte [rax + 1 * rcx + 0x7f], cl        | 86 4c 08 7f             |
    | xchg byte [rax + 1 * rcx - 0x7f], cl        | 86 4c 08 81             |
    | xchg byte [rax + 1 * rcx + 0x80], cl        | 86 8c 08 80 00 00 00    |
    | xchg byte [rax + 1 * rcx - 0x80], cl        | 86 4c 08 80             |
    | xchg byte [rax + 1 * rcx - 0x81], cl        | 86 8c 08 7f ff ff ff    |
    | xchg byte [rax + 1 * rcx + 0xff], cl        | 86 8c 08 ff 00 00 00    |
    | xchg byte [rax + 1 * rcx - 0xff], cl        | 86 8c 08 01 ff ff ff    |
    | xchg byte [rax + 1 * rcx + 0x7fffffff], cl  | 86 8c 08 ff ff ff 7f    |
    | xchg byte [rax + 1 * rcx - 0x7fffffff], cl  | 86 8c 08 01 00 00 80    |
    | xchg byte [rax + 1 * rcx - 0x80000000], cl  | 86 8c 08 00 00 00 80    |
    | xchg byte [r10 + 0x7f], cl                  | 41 86 4a 7f             |
    | xchg byte [r10 + 0x80], cl                  | 41 86 8a 80 00 00 00    |
    | xchg byte [r10 - 0x80], cl                  | 41 86 4a 80             |
    | xchg byte [r10 - 0x81], cl                  | 41 86 8a 7f ff ff ff    |
    | xchg byte [rax], al                         | 86 00                   |
    | xchg byte [rax], dl                         | 86 10                   |
    | xchg byte [rax], bl                         | 86 18                   |
    | xchg byte [rax], spl                        | 40 86 20                |
    | xchg byte [rax], bpl                        | 40 86 28                |
    | xchg byte [rax], sil                        | 40 86 30                |
    | xchg byte [rax], dil                        | 40 86 38                |
    | xchg byte [rax], r8b                        | 44 86 00                |
    | xchg byte [rax], r9b                        | 44 86 08                |
    | xchg byte [rax], r10b                       | 44 86 10                |
    | xchg byte [rax], r11b                       | 44 86 18                |
    | xchg byte [rax], r12b                       | 44 86 20                |
    | xchg byte [rax], r13b                       | 44 86 28                |
    | xchg byte [rax], r14b                       | 44 86 30                |
    | xchg byte [rax], r15b                       | 44 86 38                |
    | xchg byte [rax], ah                         | 86 20                   |
    | xchg byte [rax], ch                         | 86 28                   |
    | xchg byte [rax], dh                         | 86 30                   |
    | xchg byte [rax], bh                         | 86 38                   |
    | xchg byte [rcx], dl                         | 86 11                   |
    | xchg byte [rdx], bl                         | 86 1a                   |
    | xchg byte [rbx], spl                        | 40 86 23                |
    | xchg byte [rsp], bpl                        | 40 86 2c 24             |
    | xchg byte [rbp], sil                        | 40 86 75 00             |
    | xchg byte [rsi], dil                        | 40 86 3e                |
    | xchg byte [rdi], r8b                        | 44 86 07                |
    | xchg byte [r8], r9b                         | 45 86 08                |
    | xchg byte [r9], r10b                        | 45 86 11                |
    | xchg byte [r10], r11b                       | 45 86 1a                |
    | xchg byte [r11], r12b                       | 45 86 23                |
    | xchg byte [r12], r13b                       | 45 86 2c 24             |
    | xchg byte [r13], r14b                       | 45 86 75 00             |
    | xchg byte [r14], r15b                       | 45 86 3e                |
    | xchg byte [r15], ah                         | !! !! !!                |
    | xchg byte [rax + 1 * rcx], ch               | 86 2c 08                |
    | xchg byte [rcx + 1 * rcx], dh               | 86 34 09                |
    | xchg byte [rdx + 1 * rcx], bh               | 86 3c 0a                |
    | xchg byte [rbx + 1 * rcx], al               | 86 04 0b                |
    | xchg byte [rbp + 1 * rcx], dl               | 86 54 0d 00             |
    | xchg byte [rsi + 1 * rcx], bl               | 86 1c 0e                |
    | xchg byte [rdi + 1 * rcx], spl              | 40 86 24 0f             |
    | xchg byte [r8 + 1 * rcx], bpl               | 41 86 2c 08             |
    | xchg byte [r9 + 1 * rcx], sil               | 41 86 34 09             |
    | xchg byte [r10 + 1 * rcx], dil              | 41 86 3c 0a             |
    | xchg byte [r11 + 1 * rcx], r8b              | 45 86 04 0b             |
    | xchg byte [r12 + 1 * rcx], r9b              | 45 86 0c 0c             |
    | xchg byte [r13 + 1 * rcx], r10b             | 45 86 54 0d 00          |
    | xchg byte [r14 + 1 * rcx], r11b             | 45 86 1c 0e             |
    | xchg byte [r15 + 1 * rcx], r12b             | 45 86 24 0f             |
    | xchg byte [rax + 1 * rax], r13b             | 44 86 2c 00             |
    | xchg byte [rax + 1 * rdx], r14b             | 44 86 34 10             |
    | xchg byte [rax + 1 * rbx], r15b             | 44 86 3c 18             |
    | xchg byte [rax + 1 * rbp], ah               | 86 24 28                |
    | xchg byte [rax + 1 * rsi], ch               | 86 2c 30                |
    | xchg byte [rax + 1 * rdi], dh               | 86 34 38                |
    | xchg byte [rax + 1 * r8], bh                | !! !! !!                |
    | xchg byte [rax + 1 * r9], al                | 42 86 04 08             |
    | xchg byte [rax + 1 * r11], dl               | 42 86 14 18             |
    | xchg byte [rax + 1 * r12], bl               | 42 86 1c 20             |
    | xchg byte [rax + 1 * r13], spl              | 42 86 24 28             |
    | xchg byte [rax + 1 * r14], bpl              | 42 86 2c 30             |
    | xchg byte [rax + 1 * r15], sil              | 42 86 34 38             |
    | xchg byte [rax + 2 * rcx], dil              | 40 86 3c 48             |
    | xchg byte [rax + 4 * rcx], r8b              | 44 86 04 88             |
    | xchg byte [rax + 8 * rcx], r9b              | 44 86 0c c8             |
    | xchg byte [r8 + 1 * r9], r10b               | 47 86 14 08             |
    | xchg byte [r8 + 2 * r9], r11b               | 47 86 1c 48             |
    | xchg byte [r8 + 4 * r9], r12b               | 47 86 24 88             |
    | xchg byte [r8 + 8 * r9], r13b               | 47 86 2c c8             |
    | xchg byte [1 * rcx], r14b                   | 44 86 34 0d 00 00 00 00 |
    | xchg byte [2 * rcx], r15b                   | 44 86 3c 4d 00 00 00 00 |
    | xchg byte [4 * rcx], ah                     | 86 24 8d 00 00 00 00    |
    | xchg byte [8 * rcx], ch                     | 86 2c cd 00 00 00 00    |
    | xchg byte [1 * r9], dh                      | !! !! !!                |
    | xchg byte [2 * r9], bh                      | !! !! !!                |
    | xchg byte [4 * r9], al                      | 42 86 04 8d 00 00 00 00 |
    | xchg byte [r13 + 8 * r12], dl               | 43 86 54 e5 00          |
    | xchg byte [rsp + 4 * r15], bl               | 42 86 1c bc             |
    | xchg byte [rax + 1 * rcx + 0x00], spl       | 40 86 64 08 00          |
    | xchg byte [rax + 1 * rcx - 0x00], bpl       | 40 86 6c 08 00          |
    | xchg byte [rax + 1 * rcx + 0x01], sil       | 40 86 74 08 01          |
    | xchg byte [rax + 1 * rcx - 0x01], dil       | 40 86 7c 08 ff          |
    | xchg byte [rax + 1 * rcx + 0x00000001], r8b | 44 86 84 08 01 00 00 00 |
    | xchg byte [rax + 1 * rcx - 0x00000001], r9b | 44 86 8c 08 ff ff ff ff |
    | xchg byte [rax + 1 * rcx + 0x7f], r10b      | 44 86 54 08 7f          |
    | xchg byte [rax + 1 * rcx - 0x7f], r11b      | 44 86 5c 08 81          |
    | xchg byte [rax + 1 * rcx + 0x80], r12b      | 44 86 a4 08 80 00 00 00 |
    | xchg byte [rax + 1 * rcx - 0x80], r13b      | 44 86 6c 08 80          |
    | xchg byte [rax + 1 * rcx - 0x81], r14b      | 44 86 b4 08 7f ff ff ff |
    | xchg byte [rax + 1 * rcx + 0xff], r15b      | 44 86 bc 08 ff 00 00 00 |
    | xchg byte [rax + 1 * rcx - 0xff], ah        | 86 a4 08 01 ff ff ff    |
    | xchg byte [rax + 1 * rcx + 0x7fffffff], ch  | 86 ac 08 ff ff ff 7f    |
    | xchg byte [rax + 1 * rcx - 0x7fffffff], dh  | 86 b4 08 01 00 00 80    |
    | xchg byte [rax + 1 * rcx - 0x80000000], bh  | 86 bc 08 00 00 00 80    |
    | xchg byte [r10 + 0x7f], al                  | 41 86 42 7f             |
    | xchg byte [r10 - 0x80], dl                  | 41 86 52 80             |
    | xchg byte [r10 - 0x81], bl                  | 41 86 9a 7f ff ff ff    |
    | ------------------------------------------- | ----------------------- |
"""


def can_encode_xchg_addr8_reg8():
    encode(XCHG_ADDR8_REG8)
