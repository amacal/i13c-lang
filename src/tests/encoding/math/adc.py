from tests.encoding.core import encode, exhaust


def can_exhaust_adc():
    exhaust(
        ADC_ADDR16_IMM16,
        ADC_ADDR16_IMM8,
        ADC_ADDR16_REG16,
        ADC_ADDR32_IMM32,
        ADC_ADDR32_IMM8,
        ADC_ADDR32_REG32,
        ADC_ADDR64_IMM32,
        ADC_ADDR64_IMM8,
        ADC_ADDR64_REG64,
        ADC_ADDR8_IMM8,
        ADC_ADDR8_REG8,
        ADC_REG16_ADDR16,
        ADC_REG16_IMM16,
        ADC_REG16_IMM8,
        ADC_REG16_REG16,
        ADC_REG32_ADDR32,
        ADC_REG32_IMM32,
        ADC_REG32_IMM8,
        ADC_REG32_REG32,
        ADC_REG64_ADDR64,
        ADC_REG64_IMM32,
        ADC_REG64_IMM8,
        ADC_REG64_REG64,
        ADC_REG8_ADDR8,
        ADC_REG8_IMM8,
        ADC_REG8_REG8,
    )


ADC_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | adc rax, 0x01 | 48 83 d0 01 | *** | adc rax, 0x00 | 48 83 d0 00 |
    | adc rcx, 0x01 | 48 83 d1 01 | *** | adc rax, 0x7f | 48 83 d0 7f |
    | adc rdx, 0x01 | 48 83 d2 01 | *** | adc rax, 0x80 | 48 83 d0 80 |
    | adc rbx, 0x01 | 48 83 d3 01 | *** | adc rax, 0xff | 48 83 d0 ff |
    | adc rsp, 0x01 | 48 83 d4 01 | *** | adc rcx, 0x7f | 48 83 d1 7f |
    | adc rbp, 0x01 | 48 83 d5 01 | *** | adc rdx, 0x80 | 48 83 d2 80 |
    | adc rsi, 0x01 | 48 83 d6 01 | *** | adc rbx, 0xff | 48 83 d3 ff |
    | adc rdi, 0x01 | 48 83 d7 01 | *** | adc rsp, 0x00 | 48 83 d4 00 |
    | adc r8, 0x01  | 49 83 d0 01 | *** | adc rsi, 0x7f | 48 83 d6 7f |
    | adc r9, 0x01  | 49 83 d1 01 | *** | adc rdi, 0x80 | 48 83 d7 80 |
    | adc r10, 0x01 | 49 83 d2 01 | *** | adc r8, 0xff  | 49 83 d0 ff |
    | adc r11, 0x01 | 49 83 d3 01 | *** | adc r9, 0x00  | 49 83 d1 00 |
    | adc r12, 0x01 | 49 83 d4 01 | *** | adc r11, 0x7f | 49 83 d3 7f |
    | adc r13, 0x01 | 49 83 d5 01 | *** | adc r12, 0x80 | 49 83 d4 80 |
    | adc r14, 0x01 | 49 83 d6 01 | *** | adc r13, 0xff | 49 83 d5 ff |
    | adc r15, 0x01 | 49 83 d7 01 | *** | adc r14, 0x00 | 49 83 d6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_adc_reg64_imm8():
    encode(ADC_REG64_IMM8)


ADC_REG64_IMM32 = """
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | instruction         | encoding             | *** | instruction         | encoding             |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
    | adc rax, 0x00000001 | 48 15 01 00 00 00    | *** | adc rax, 0x00007fff | 48 15 ff 7f 00 00    |
    | adc rcx, 0x00000001 | 48 81 d1 01 00 00 00 | *** | adc rax, 0x00008000 | 48 15 00 80 00 00    |
    | adc rdx, 0x00000001 | 48 81 d2 01 00 00 00 | *** | adc rax, 0x0000ffff | 48 15 ff ff 00 00    |
    | adc rbx, 0x00000001 | 48 81 d3 01 00 00 00 | *** | adc rax, 0x00010000 | 48 15 00 00 01 00    |
    | adc rsp, 0x00000001 | 48 81 d4 01 00 00 00 | *** | adc rax, 0x7fffffff | 48 15 ff ff ff 7f    |
    | adc rbp, 0x00000001 | 48 81 d5 01 00 00 00 | *** | adc rax, 0x80000000 | 48 15 00 00 00 80    |
    | adc rsi, 0x00000001 | 48 81 d6 01 00 00 00 | *** | adc rax, 0xffffffff | 48 15 ff ff ff ff    |
    | adc rdi, 0x00000001 | 48 81 d7 01 00 00 00 | *** | adc rcx, 0x0000007f | 48 81 d1 7f 00 00 00 |
    | adc r8, 0x00000001  | 49 81 d0 01 00 00 00 | *** | adc rdx, 0x00000080 | 48 81 d2 80 00 00 00 |
    | adc r9, 0x00000001  | 49 81 d1 01 00 00 00 | *** | adc rbx, 0x000000ff | 48 81 d3 ff 00 00 00 |
    | adc r10, 0x00000001 | 49 81 d2 01 00 00 00 | *** | adc rsp, 0x00000100 | 48 81 d4 00 01 00 00 |
    | adc r11, 0x00000001 | 49 81 d3 01 00 00 00 | *** | adc rbp, 0x00007fff | 48 81 d5 ff 7f 00 00 |
    | adc r12, 0x00000001 | 49 81 d4 01 00 00 00 | *** | adc rsi, 0x00008000 | 48 81 d6 00 80 00 00 |
    | adc r13, 0x00000001 | 49 81 d5 01 00 00 00 | *** | adc rdi, 0x0000ffff | 48 81 d7 ff ff 00 00 |
    | adc r14, 0x00000001 | 49 81 d6 01 00 00 00 | *** | adc r8, 0x00010000  | 49 81 d0 00 00 01 00 |
    | adc r15, 0x00000001 | 49 81 d7 01 00 00 00 | *** | adc r9, 0x7fffffff  | 49 81 d1 ff ff ff 7f |
    | adc rax, 0x00000000 | 48 15 00 00 00 00    | *** | adc r10, 0x80000000 | 49 81 d2 00 00 00 80 |
    | adc rax, 0x0000007f | 48 15 7f 00 00 00    | *** | adc r11, 0xffffffff | 49 81 d3 ff ff ff ff |
    | adc rax, 0x00000080 | 48 15 80 00 00 00    | *** | adc r12, 0x00000000 | 49 81 d4 00 00 00 00 |
    | adc rax, 0x000000ff | 48 15 ff 00 00 00    | *** | adc r14, 0x0000007f | 49 81 d6 7f 00 00 00 |
    | adc rax, 0x00000100 | 48 15 00 01 00 00    | *** | adc r15, 0x00000080 | 49 81 d7 80 00 00 00 |
    | ------------------- | -------------------- | --- | ------------------- | -------------------- |
"""


def can_encode_adc_reg64_imm32():
    encode(ADC_REG64_IMM32)


ADC_REG64_REG64 = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | adc rax, rcx | 48 11 c8 | *** | adc rax, r8  | 4c 11 c0 |
    | adc rcx, rcx | 48 11 c9 | *** | adc rax, r9  | 4c 11 c8 |
    | adc rdx, rcx | 48 11 ca | *** | adc rax, r10 | 4c 11 d0 |
    | adc rbx, rcx | 48 11 cb | *** | adc rax, r11 | 4c 11 d8 |
    | adc rsp, rcx | 48 11 cc | *** | adc rax, r12 | 4c 11 e0 |
    | adc rbp, rcx | 48 11 cd | *** | adc rax, r13 | 4c 11 e8 |
    | adc rsi, rcx | 48 11 ce | *** | adc rax, r14 | 4c 11 f0 |
    | adc rdi, rcx | 48 11 cf | *** | adc rax, r15 | 4c 11 f8 |
    | adc r8, rcx  | 49 11 c8 | *** | adc rcx, rdx | 48 11 d1 |
    | adc r9, rcx  | 49 11 c9 | *** | adc rdx, rbx | 48 11 da |
    | adc r10, rcx | 49 11 ca | *** | adc rbx, rsp | 48 11 e3 |
    | adc r11, rcx | 49 11 cb | *** | adc rsp, rbp | 48 11 ec |
    | adc r12, rcx | 49 11 cc | *** | adc rbp, rsi | 48 11 f5 |
    | adc r13, rcx | 49 11 cd | *** | adc rsi, rdi | 48 11 fe |
    | adc r14, rcx | 49 11 ce | *** | adc rdi, r8  | 4c 11 c7 |
    | adc r15, rcx | 49 11 cf | *** | adc r8, r9   | 4d 11 c8 |
    | adc rax, rax | 48 11 c0 | *** | adc r9, r10  | 4d 11 d1 |
    | adc rax, rdx | 48 11 d0 | *** | adc r10, r11 | 4d 11 da |
    | adc rax, rbx | 48 11 d8 | *** | adc r11, r12 | 4d 11 e3 |
    | adc rax, rsp | 48 11 e0 | *** | adc r12, r13 | 4d 11 ec |
    | adc rax, rbp | 48 11 e8 | *** | adc r13, r14 | 4d 11 f5 |
    | adc rax, rsi | 48 11 f0 | *** | adc r14, r15 | 4d 11 fe |
    | adc rax, rdi | 48 11 f8 | *** | adc r15, rax | 49 11 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_adc_reg64_reg64():
    encode(ADC_REG64_REG64)


ADC_REG64_ADDR64 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | adc rax, qword [rcx]                                              | 48 13 01                               |
    | adc rcx, qword [rcx]                                              | 48 13 09                               |
    | adc rdx, qword [rcx]                                              | 48 13 11                               |
    | adc rbx, qword [rcx]                                              | 48 13 19                               |
    | adc rsp, qword [rcx]                                              | 48 13 21                               |
    | adc rbp, qword [rcx]                                              | 48 13 29                               |
    | adc rsi, qword [rcx]                                              | 48 13 31                               |
    | adc rdi, qword [rcx]                                              | 48 13 39                               |
    | adc r8, qword [rcx]                                               | 4c 13 01                               |
    | adc r9, qword [rcx]                                               | 4c 13 09                               |
    | adc r10, qword [rcx]                                              | 4c 13 11                               |
    | adc r11, qword [rcx]                                              | 4c 13 19                               |
    | adc r12, qword [rcx]                                              | 4c 13 21                               |
    | adc r13, qword [rcx]                                              | 4c 13 29                               |
    | adc r14, qword [rcx]                                              | 4c 13 31                               |
    | adc r15, qword [rcx]                                              | 4c 13 39                               |
    | adc rax, qword [rax]                                              | 48 13 00                               |
    | adc rax, qword [rdx]                                              | 48 13 02                               |
    | adc rax, qword [rbx]                                              | 48 13 03                               |
    | adc rax, qword [rsp]                                              | 48 13 04 24                            |
    | adc rax, qword [rbp]                                              | 48 13 45 00                            |
    | adc rax, qword [rsi]                                              | 48 13 06                               |
    | adc rax, qword [rdi]                                              | 48 13 07                               |
    | adc rax, qword [r8]                                               | 49 13 00                               |
    | adc rax, qword [r9]                                               | 49 13 01                               |
    | adc rax, qword [r10]                                              | 49 13 02                               |
    | adc rax, qword [r11]                                              | 49 13 03                               |
    | adc rax, qword [r12]                                              | 49 13 04 24                            |
    | adc rax, qword [r13]                                              | 49 13 45 00                            |
    | adc rax, qword [r14]                                              | 49 13 06                               |
    | adc rax, qword [r15]                                              | 49 13 07                               |
    | adc rax, qword [rax + 1 * rcx]                                    | 48 13 04 08                            |
    | adc rax, qword [rcx + 1 * rcx]                                    | 48 13 04 09                            |
    | adc rax, qword [rdx + 1 * rcx]                                    | 48 13 04 0a                            |
    | adc rax, qword [rbx + 1 * rcx]                                    | 48 13 04 0b                            |
    | adc rax, qword [rsp + 1 * rcx]                                    | 48 13 04 0c                            |
    | adc rax, qword [rbp + 1 * rcx]                                    | 48 13 44 0d 00                         |
    | adc rax, qword [rsi + 1 * rcx]                                    | 48 13 04 0e                            |
    | adc rax, qword [rdi + 1 * rcx]                                    | 48 13 04 0f                            |
    | adc rax, qword [r8 + 1 * rcx]                                     | 49 13 04 08                            |
    | adc rax, qword [r9 + 1 * rcx]                                     | 49 13 04 09                            |
    | adc rax, qword [r10 + 1 * rcx]                                    | 49 13 04 0a                            |
    | adc rax, qword [r11 + 1 * rcx]                                    | 49 13 04 0b                            |
    | adc rax, qword [r12 + 1 * rcx]                                    | 49 13 04 0c                            |
    | adc rax, qword [r13 + 1 * rcx]                                    | 49 13 44 0d 00                         |
    | adc rax, qword [r14 + 1 * rcx]                                    | 49 13 04 0e                            |
    | adc rax, qword [r15 + 1 * rcx]                                    | 49 13 04 0f                            |
    | adc rax, qword [rax + 1 * rax]                                    | 48 13 04 00                            |
    | adc rax, qword [rax + 1 * rdx]                                    | 48 13 04 10                            |
    | adc rax, qword [rax + 1 * rbx]                                    | 48 13 04 18                            |
    | adc rax, qword [rax + 1 * rbp]                                    | 48 13 04 28                            |
    | adc rax, qword [rax + 1 * rsi]                                    | 48 13 04 30                            |
    | adc rax, qword [rax + 1 * rdi]                                    | 48 13 04 38                            |
    | adc rax, qword [rax + 1 * r8]                                     | 4a 13 04 00                            |
    | adc rax, qword [rax + 1 * r9]                                     | 4a 13 04 08                            |
    | adc rax, qword [rax + 1 * r10]                                    | 4a 13 04 10                            |
    | adc rax, qword [rax + 1 * r11]                                    | 4a 13 04 18                            |
    | adc rax, qword [rax + 1 * r12]                                    | 4a 13 04 20                            |
    | adc rax, qword [rax + 1 * r13]                                    | 4a 13 04 28                            |
    | adc rax, qword [rax + 1 * r14]                                    | 4a 13 04 30                            |
    | adc rax, qword [rax + 1 * r15]                                    | 4a 13 04 38                            |
    | adc rax, qword [rax + 2 * rcx]                                    | 48 13 04 48                            |
    | adc rax, qword [rax + 4 * rcx]                                    | 48 13 04 88                            |
    | adc rax, qword [rax + 8 * rcx]                                    | 48 13 04 c8                            |
    | adc rax, qword [r8 + 1 * r9]                                      | 4b 13 04 08                            |
    | adc rax, qword [r8 + 2 * r9]                                      | 4b 13 04 48                            |
    | adc rax, qword [r8 + 4 * r9]                                      | 4b 13 04 88                            |
    | adc rax, qword [r8 + 8 * r9]                                      | 4b 13 04 c8                            |
    | adc rax, qword [1 * rcx]                                          | 48 13 04 0d 00 00 00 00                |
    | adc rax, qword [2 * rcx]                                          | 48 13 04 4d 00 00 00 00                |
    | adc rax, qword [4 * rcx]                                          | 48 13 04 8d 00 00 00 00                |
    | adc rax, qword [8 * rcx]                                          | 48 13 04 cd 00 00 00 00                |
    | adc rax, qword [1 * r9]                                           | 4a 13 04 0d 00 00 00 00                |
    | adc rax, qword [2 * r9]                                           | 4a 13 04 4d 00 00 00 00                |
    | adc rax, qword [4 * r9]                                           | 4a 13 04 8d 00 00 00 00                |
    | adc rax, qword [8 * r9]                                           | 4a 13 04 cd 00 00 00 00                |
    | adc rax, qword [r13 + 8 * r12]                                    | 4b 13 44 e5 00                         |
    | adc rax, qword [rsp + 4 * r15]                                    | 4a 13 04 bc                            |
    | adc rax, qword [rax + 1 * rcx + 0x00]                             | 48 13 44 08 00                         |
    | adc rax, qword [rax + 1 * rcx - 0x00]                             | 48 13 44 08 00                         |
    | adc rax, qword [rax + 1 * rcx + 0x01]                             | 48 13 44 08 01                         |
    | adc rax, qword [rax + 1 * rcx - 0x01]                             | 48 13 44 08 ff                         |
    | adc rax, qword [rax + 1 * rcx + 0x00000001]                       | 48 13 84 08 01 00 00 00                |
    | adc rax, qword [rax + 1 * rcx - 0x00000001]                       | 48 13 84 08 ff ff ff ff                |
    | adc rax, qword [rax + 1 * rcx + 0x7f]                             | 48 13 44 08 7f                         |
    | adc rax, qword [rax + 1 * rcx - 0x7f]                             | 48 13 44 08 81                         |
    | adc rax, qword [rax + 1 * rcx + 0x80]                             | 48 13 84 08 80 00 00 00                |
    | adc rax, qword [rax + 1 * rcx - 0x80]                             | 48 13 44 08 80                         |
    | adc rax, qword [rax + 1 * rcx - 0x81]                             | 48 13 84 08 7f ff ff ff                |
    | adc rax, qword [rax + 1 * rcx + 0xff]                             | 48 13 84 08 ff 00 00 00                |
    | adc rax, qword [rax + 1 * rcx - 0xff]                             | 48 13 84 08 01 ff ff ff                |
    | adc rax, qword [rax + 1 * rcx + 0x7fffffff]                       | 48 13 84 08 ff ff ff 7f                |
    | adc rax, qword [rax + 1 * rcx - 0x7fffffff]                       | 48 13 84 08 01 00 00 80                |
    | adc rax, qword [rax + 1 * rcx - 0x80000000]                       | 48 13 84 08 00 00 00 80                |
    | adc rax, qword [r10 + 0x7f]                                       | 49 13 42 7f                            |
    | adc rax, qword [r10 + 0x80]                                       | 49 13 82 80 00 00 00                   |
    | adc rax, qword [r10 - 0x80]                                       | 49 13 42 80                            |
    | adc rax, qword [r10 - 0x81]                                       | 49 13 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc rax, qword [rel @prev5]      | 90 90 90 90 90 48 13 05 f4 ff ff ff    |
    | .prev1: nop; adc rax, qword [rel @prev1]                          | 90 48 13 05 f8 ff ff ff                |
    | adc rax, qword [rel @next1]; nop; .next1: nop                     | 48 13 05 01 00 00 00 90 90             |
    | adc rax, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 13 05 05 00 00 00 90 90 90 90 90 90 |
    | adc rcx, qword [rdx]                                              | 48 13 0a                               |
    | adc rdx, qword [rbx]                                              | 48 13 13                               |
    | adc rbx, qword [rsp]                                              | 48 13 1c 24                            |
    | adc rsp, qword [rbp]                                              | 48 13 65 00                            |
    | adc rbp, qword [rsi]                                              | 48 13 2e                               |
    | adc rsi, qword [rdi]                                              | 48 13 37                               |
    | adc rdi, qword [r8]                                               | 49 13 38                               |
    | adc r8, qword [r9]                                                | 4d 13 01                               |
    | adc r9, qword [r10]                                               | 4d 13 0a                               |
    | adc r10, qword [r11]                                              | 4d 13 13                               |
    | adc r11, qword [r12]                                              | 4d 13 1c 24                            |
    | adc r12, qword [r13]                                              | 4d 13 65 00                            |
    | adc r13, qword [r14]                                              | 4d 13 2e                               |
    | adc r14, qword [r15]                                              | 4d 13 37                               |
    | adc r15, qword [rax + 1 * rcx]                                    | 4c 13 3c 08                            |
    | adc rcx, qword [rdx + 1 * rcx]                                    | 48 13 0c 0a                            |
    | adc rdx, qword [rbx + 1 * rcx]                                    | 48 13 14 0b                            |
    | adc rbx, qword [rsp + 1 * rcx]                                    | 48 13 1c 0c                            |
    | adc rsp, qword [rbp + 1 * rcx]                                    | 48 13 64 0d 00                         |
    | adc rbp, qword [rsi + 1 * rcx]                                    | 48 13 2c 0e                            |
    | adc rsi, qword [rdi + 1 * rcx]                                    | 48 13 34 0f                            |
    | adc rdi, qword [r8 + 1 * rcx]                                     | 49 13 3c 08                            |
    | adc r8, qword [r9 + 1 * rcx]                                      | 4d 13 04 09                            |
    | adc r9, qword [r10 + 1 * rcx]                                     | 4d 13 0c 0a                            |
    | adc r10, qword [r11 + 1 * rcx]                                    | 4d 13 14 0b                            |
    | adc r11, qword [r12 + 1 * rcx]                                    | 4d 13 1c 0c                            |
    | adc r12, qword [r13 + 1 * rcx]                                    | 4d 13 64 0d 00                         |
    | adc r13, qword [r14 + 1 * rcx]                                    | 4d 13 2c 0e                            |
    | adc r14, qword [r15 + 1 * rcx]                                    | 4d 13 34 0f                            |
    | adc r15, qword [rax + 1 * rax]                                    | 4c 13 3c 00                            |
    | adc rcx, qword [rax + 1 * rbx]                                    | 48 13 0c 18                            |
    | adc rdx, qword [rax + 1 * rbp]                                    | 48 13 14 28                            |
    | adc rbx, qword [rax + 1 * rsi]                                    | 48 13 1c 30                            |
    | adc rsp, qword [rax + 1 * rdi]                                    | 48 13 24 38                            |
    | adc rbp, qword [rax + 1 * r8]                                     | 4a 13 2c 00                            |
    | adc rsi, qword [rax + 1 * r9]                                     | 4a 13 34 08                            |
    | adc rdi, qword [rax + 1 * r10]                                    | 4a 13 3c 10                            |
    | adc r8, qword [rax + 1 * r11]                                     | 4e 13 04 18                            |
    | adc r9, qword [rax + 1 * r12]                                     | 4e 13 0c 20                            |
    | adc r10, qword [rax + 1 * r13]                                    | 4e 13 14 28                            |
    | adc r11, qword [rax + 1 * r14]                                    | 4e 13 1c 30                            |
    | adc r12, qword [rax + 1 * r15]                                    | 4e 13 24 38                            |
    | adc r13, qword [rax + 2 * rcx]                                    | 4c 13 2c 48                            |
    | adc r14, qword [rax + 4 * rcx]                                    | 4c 13 34 88                            |
    | adc r15, qword [rax + 8 * rcx]                                    | 4c 13 3c c8                            |
    | adc rcx, qword [r8 + 2 * r9]                                      | 4b 13 0c 48                            |
    | adc rdx, qword [r8 + 4 * r9]                                      | 4b 13 14 88                            |
    | adc rbx, qword [r8 + 8 * r9]                                      | 4b 13 1c c8                            |
    | adc rsp, qword [1 * rcx]                                          | 48 13 24 0d 00 00 00 00                |
    | adc rbp, qword [2 * rcx]                                          | 48 13 2c 4d 00 00 00 00                |
    | adc rsi, qword [4 * rcx]                                          | 48 13 34 8d 00 00 00 00                |
    | adc rdi, qword [8 * rcx]                                          | 48 13 3c cd 00 00 00 00                |
    | adc r8, qword [1 * r9]                                            | 4e 13 04 0d 00 00 00 00                |
    | adc r9, qword [2 * r9]                                            | 4e 13 0c 4d 00 00 00 00                |
    | adc r10, qword [4 * r9]                                           | 4e 13 14 8d 00 00 00 00                |
    | adc r11, qword [8 * r9]                                           | 4e 13 1c cd 00 00 00 00                |
    | adc r12, qword [r13 + 8 * r12]                                    | 4f 13 64 e5 00                         |
    | adc r13, qword [rsp + 4 * r15]                                    | 4e 13 2c bc                            |
    | adc r14, qword [rax + 1 * rcx + 0x00]                             | 4c 13 74 08 00                         |
    | adc r15, qword [rax + 1 * rcx - 0x00]                             | 4c 13 7c 08 00                         |
    | adc rcx, qword [rax + 1 * rcx - 0x01]                             | 48 13 4c 08 ff                         |
    | adc rdx, qword [rax + 1 * rcx + 0x00000001]                       | 48 13 94 08 01 00 00 00                |
    | adc rbx, qword [rax + 1 * rcx - 0x00000001]                       | 48 13 9c 08 ff ff ff ff                |
    | adc rsp, qword [rax + 1 * rcx + 0x7f]                             | 48 13 64 08 7f                         |
    | adc rbp, qword [rax + 1 * rcx - 0x7f]                             | 48 13 6c 08 81                         |
    | adc rsi, qword [rax + 1 * rcx + 0x80]                             | 48 13 b4 08 80 00 00 00                |
    | adc rdi, qword [rax + 1 * rcx - 0x80]                             | 48 13 7c 08 80                         |
    | adc r8, qword [rax + 1 * rcx - 0x81]                              | 4c 13 84 08 7f ff ff ff                |
    | adc r9, qword [rax + 1 * rcx + 0xff]                              | 4c 13 8c 08 ff 00 00 00                |
    | adc r10, qword [rax + 1 * rcx - 0xff]                             | 4c 13 94 08 01 ff ff ff                |
    | adc r11, qword [rax + 1 * rcx + 0x7fffffff]                       | 4c 13 9c 08 ff ff ff 7f                |
    | adc r12, qword [rax + 1 * rcx - 0x7fffffff]                       | 4c 13 a4 08 01 00 00 80                |
    | adc r13, qword [rax + 1 * rcx - 0x80000000]                       | 4c 13 ac 08 00 00 00 80                |
    | adc r14, qword [r10 + 0x7f]                                       | 4d 13 72 7f                            |
    | adc r15, qword [r10 + 0x80]                                       | 4d 13 ba 80 00 00 00                   |
    | adc rcx, qword [r10 - 0x81]                                       | 49 13 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc rdx, qword [rel @prev5]      | 90 90 90 90 90 48 13 15 f4 ff ff ff    |
    | .prev1: nop; adc rbx, qword [rel @prev1]                          | 90 48 13 1d f8 ff ff ff                |
    | adc rsp, qword [rel @next1]; nop; .next1: nop                     | 48 13 25 01 00 00 00 90 90             |
    | adc rbp, qword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 48 13 2d 05 00 00 00 90 90 90 90 90 90 |
    | adc rsi, qword [rax]                                              | 48 13 30                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_adc_reg64_addr64():
    encode(ADC_REG64_ADDR64)


ADC_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | adc eax, 0x01  | 83 d0 01    | *** | adc eax, 0x00  | 83 d0 00    |
    | adc ecx, 0x01  | 83 d1 01    | *** | adc eax, 0x7f  | 83 d0 7f    |
    | adc edx, 0x01  | 83 d2 01    | *** | adc eax, 0x80  | 83 d0 80    |
    | adc ebx, 0x01  | 83 d3 01    | *** | adc eax, 0xff  | 83 d0 ff    |
    | adc esp, 0x01  | 83 d4 01    | *** | adc ecx, 0x7f  | 83 d1 7f    |
    | adc ebp, 0x01  | 83 d5 01    | *** | adc edx, 0x80  | 83 d2 80    |
    | adc esi, 0x01  | 83 d6 01    | *** | adc ebx, 0xff  | 83 d3 ff    |
    | adc edi, 0x01  | 83 d7 01    | *** | adc esp, 0x00  | 83 d4 00    |
    | adc r8d, 0x01  | 41 83 d0 01 | *** | adc esi, 0x7f  | 83 d6 7f    |
    | adc r9d, 0x01  | 41 83 d1 01 | *** | adc edi, 0x80  | 83 d7 80    |
    | adc r10d, 0x01 | 41 83 d2 01 | *** | adc r8d, 0xff  | 41 83 d0 ff |
    | adc r11d, 0x01 | 41 83 d3 01 | *** | adc r9d, 0x00  | 41 83 d1 00 |
    | adc r12d, 0x01 | 41 83 d4 01 | *** | adc r11d, 0x7f | 41 83 d3 7f |
    | adc r13d, 0x01 | 41 83 d5 01 | *** | adc r12d, 0x80 | 41 83 d4 80 |
    | adc r14d, 0x01 | 41 83 d6 01 | *** | adc r13d, 0xff | 41 83 d5 ff |
    | adc r15d, 0x01 | 41 83 d7 01 | *** | adc r14d, 0x00 | 41 83 d6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_adc_reg32_imm8():
    encode(ADC_REG32_IMM8)


ADC_REG32_IMM32 = """
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | instruction          | encoding             | *** | instruction          | encoding             |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
    | adc eax, 0x00000001  | 15 01 00 00 00       | *** | adc eax, 0x00007fff  | 15 ff 7f 00 00       |
    | adc ecx, 0x00000001  | 81 d1 01 00 00 00    | *** | adc eax, 0x00008000  | 15 00 80 00 00       |
    | adc edx, 0x00000001  | 81 d2 01 00 00 00    | *** | adc eax, 0x0000ffff  | 15 ff ff 00 00       |
    | adc ebx, 0x00000001  | 81 d3 01 00 00 00    | *** | adc eax, 0x00010000  | 15 00 00 01 00       |
    | adc esp, 0x00000001  | 81 d4 01 00 00 00    | *** | adc eax, 0x7fffffff  | 15 ff ff ff 7f       |
    | adc ebp, 0x00000001  | 81 d5 01 00 00 00    | *** | adc eax, 0x80000000  | 15 00 00 00 80       |
    | adc esi, 0x00000001  | 81 d6 01 00 00 00    | *** | adc eax, 0xffffffff  | 15 ff ff ff ff       |
    | adc edi, 0x00000001  | 81 d7 01 00 00 00    | *** | adc ecx, 0x0000007f  | 81 d1 7f 00 00 00    |
    | adc r8d, 0x00000001  | 41 81 d0 01 00 00 00 | *** | adc edx, 0x00000080  | 81 d2 80 00 00 00    |
    | adc r9d, 0x00000001  | 41 81 d1 01 00 00 00 | *** | adc ebx, 0x000000ff  | 81 d3 ff 00 00 00    |
    | adc r10d, 0x00000001 | 41 81 d2 01 00 00 00 | *** | adc esp, 0x00000100  | 81 d4 00 01 00 00    |
    | adc r11d, 0x00000001 | 41 81 d3 01 00 00 00 | *** | adc ebp, 0x00007fff  | 81 d5 ff 7f 00 00    |
    | adc r12d, 0x00000001 | 41 81 d4 01 00 00 00 | *** | adc esi, 0x00008000  | 81 d6 00 80 00 00    |
    | adc r13d, 0x00000001 | 41 81 d5 01 00 00 00 | *** | adc edi, 0x0000ffff  | 81 d7 ff ff 00 00    |
    | adc r14d, 0x00000001 | 41 81 d6 01 00 00 00 | *** | adc r8d, 0x00010000  | 41 81 d0 00 00 01 00 |
    | adc r15d, 0x00000001 | 41 81 d7 01 00 00 00 | *** | adc r9d, 0x7fffffff  | 41 81 d1 ff ff ff 7f |
    | adc eax, 0x00000000  | 15 00 00 00 00       | *** | adc r10d, 0x80000000 | 41 81 d2 00 00 00 80 |
    | adc eax, 0x0000007f  | 15 7f 00 00 00       | *** | adc r11d, 0xffffffff | 41 81 d3 ff ff ff ff |
    | adc eax, 0x00000080  | 15 80 00 00 00       | *** | adc r12d, 0x00000000 | 41 81 d4 00 00 00 00 |
    | adc eax, 0x000000ff  | 15 ff 00 00 00       | *** | adc r14d, 0x0000007f | 41 81 d6 7f 00 00 00 |
    | adc eax, 0x00000100  | 15 00 01 00 00       | *** | adc r15d, 0x00000080 | 41 81 d7 80 00 00 00 |
    | -------------------- | -------------------- | --- | -------------------- | -------------------- |
"""


def can_encode_adc_reg32_imm32():
    encode(ADC_REG32_IMM32)


ADC_REG32_REG32 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | adc eax, ecx   | 11 c8    | *** | adc eax, r8d   | 44 11 c0 |
    | adc ecx, ecx   | 11 c9    | *** | adc eax, r9d   | 44 11 c8 |
    | adc edx, ecx   | 11 ca    | *** | adc eax, r10d  | 44 11 d0 |
    | adc ebx, ecx   | 11 cb    | *** | adc eax, r11d  | 44 11 d8 |
    | adc esp, ecx   | 11 cc    | *** | adc eax, r12d  | 44 11 e0 |
    | adc ebp, ecx   | 11 cd    | *** | adc eax, r13d  | 44 11 e8 |
    | adc esi, ecx   | 11 ce    | *** | adc eax, r14d  | 44 11 f0 |
    | adc edi, ecx   | 11 cf    | *** | adc eax, r15d  | 44 11 f8 |
    | adc r8d, ecx   | 41 11 c8 | *** | adc ecx, edx   | 11 d1    |
    | adc r9d, ecx   | 41 11 c9 | *** | adc edx, ebx   | 11 da    |
    | adc r10d, ecx  | 41 11 ca | *** | adc ebx, esp   | 11 e3    |
    | adc r11d, ecx  | 41 11 cb | *** | adc esp, ebp   | 11 ec    |
    | adc r12d, ecx  | 41 11 cc | *** | adc ebp, esi   | 11 f5    |
    | adc r13d, ecx  | 41 11 cd | *** | adc esi, edi   | 11 fe    |
    | adc r14d, ecx  | 41 11 ce | *** | adc edi, r8d   | 44 11 c7 |
    | adc r15d, ecx  | 41 11 cf | *** | adc r8d, r9d   | 45 11 c8 |
    | adc eax, eax   | 11 c0    | *** | adc r9d, r10d  | 45 11 d1 |
    | adc eax, edx   | 11 d0    | *** | adc r10d, r11d | 45 11 da |
    | adc eax, ebx   | 11 d8    | *** | adc r11d, r12d | 45 11 e3 |
    | adc eax, esp   | 11 e0    | *** | adc r12d, r13d | 45 11 ec |
    | adc eax, ebp   | 11 e8    | *** | adc r13d, r14d | 45 11 f5 |
    | adc eax, esi   | 11 f0    | *** | adc r14d, r15d | 45 11 fe |
    | adc eax, edi   | 11 f8    | *** | adc r15d, eax  | 41 11 c7 |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_adc_reg32_reg32():
    encode(ADC_REG32_REG32)


ADC_REG32_ADDR32 = """
    | ----------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                       | encoding                            |
    | ----------------------------------------------------------------- | ----------------------------------- |
    | adc eax, dword [rcx]                                              | 13 01                               |
    | adc ecx, dword [rcx]                                              | 13 09                               |
    | adc edx, dword [rcx]                                              | 13 11                               |
    | adc ebx, dword [rcx]                                              | 13 19                               |
    | adc esp, dword [rcx]                                              | 13 21                               |
    | adc ebp, dword [rcx]                                              | 13 29                               |
    | adc esi, dword [rcx]                                              | 13 31                               |
    | adc edi, dword [rcx]                                              | 13 39                               |
    | adc r8d, dword [rcx]                                              | 44 13 01                            |
    | adc r9d, dword [rcx]                                              | 44 13 09                            |
    | adc r10d, dword [rcx]                                             | 44 13 11                            |
    | adc r11d, dword [rcx]                                             | 44 13 19                            |
    | adc r12d, dword [rcx]                                             | 44 13 21                            |
    | adc r13d, dword [rcx]                                             | 44 13 29                            |
    | adc r14d, dword [rcx]                                             | 44 13 31                            |
    | adc r15d, dword [rcx]                                             | 44 13 39                            |
    | adc eax, dword [rax]                                              | 13 00                               |
    | adc eax, dword [rdx]                                              | 13 02                               |
    | adc eax, dword [rbx]                                              | 13 03                               |
    | adc eax, dword [rsp]                                              | 13 04 24                            |
    | adc eax, dword [rbp]                                              | 13 45 00                            |
    | adc eax, dword [rsi]                                              | 13 06                               |
    | adc eax, dword [rdi]                                              | 13 07                               |
    | adc eax, dword [r8]                                               | 41 13 00                            |
    | adc eax, dword [r9]                                               | 41 13 01                            |
    | adc eax, dword [r10]                                              | 41 13 02                            |
    | adc eax, dword [r11]                                              | 41 13 03                            |
    | adc eax, dword [r12]                                              | 41 13 04 24                         |
    | adc eax, dword [r13]                                              | 41 13 45 00                         |
    | adc eax, dword [r14]                                              | 41 13 06                            |
    | adc eax, dword [r15]                                              | 41 13 07                            |
    | adc eax, dword [rax + 1 * rcx]                                    | 13 04 08                            |
    | adc eax, dword [rcx + 1 * rcx]                                    | 13 04 09                            |
    | adc eax, dword [rdx + 1 * rcx]                                    | 13 04 0a                            |
    | adc eax, dword [rbx + 1 * rcx]                                    | 13 04 0b                            |
    | adc eax, dword [rsp + 1 * rcx]                                    | 13 04 0c                            |
    | adc eax, dword [rbp + 1 * rcx]                                    | 13 44 0d 00                         |
    | adc eax, dword [rsi + 1 * rcx]                                    | 13 04 0e                            |
    | adc eax, dword [rdi + 1 * rcx]                                    | 13 04 0f                            |
    | adc eax, dword [r8 + 1 * rcx]                                     | 41 13 04 08                         |
    | adc eax, dword [r9 + 1 * rcx]                                     | 41 13 04 09                         |
    | adc eax, dword [r10 + 1 * rcx]                                    | 41 13 04 0a                         |
    | adc eax, dword [r11 + 1 * rcx]                                    | 41 13 04 0b                         |
    | adc eax, dword [r12 + 1 * rcx]                                    | 41 13 04 0c                         |
    | adc eax, dword [r13 + 1 * rcx]                                    | 41 13 44 0d 00                      |
    | adc eax, dword [r14 + 1 * rcx]                                    | 41 13 04 0e                         |
    | adc eax, dword [r15 + 1 * rcx]                                    | 41 13 04 0f                         |
    | adc eax, dword [rax + 1 * rax]                                    | 13 04 00                            |
    | adc eax, dword [rax + 1 * rdx]                                    | 13 04 10                            |
    | adc eax, dword [rax + 1 * rbx]                                    | 13 04 18                            |
    | adc eax, dword [rax + 1 * rbp]                                    | 13 04 28                            |
    | adc eax, dword [rax + 1 * rsi]                                    | 13 04 30                            |
    | adc eax, dword [rax + 1 * rdi]                                    | 13 04 38                            |
    | adc eax, dword [rax + 1 * r8]                                     | 42 13 04 00                         |
    | adc eax, dword [rax + 1 * r9]                                     | 42 13 04 08                         |
    | adc eax, dword [rax + 1 * r10]                                    | 42 13 04 10                         |
    | adc eax, dword [rax + 1 * r11]                                    | 42 13 04 18                         |
    | adc eax, dword [rax + 1 * r12]                                    | 42 13 04 20                         |
    | adc eax, dword [rax + 1 * r13]                                    | 42 13 04 28                         |
    | adc eax, dword [rax + 1 * r14]                                    | 42 13 04 30                         |
    | adc eax, dword [rax + 1 * r15]                                    | 42 13 04 38                         |
    | adc eax, dword [rax + 2 * rcx]                                    | 13 04 48                            |
    | adc eax, dword [rax + 4 * rcx]                                    | 13 04 88                            |
    | adc eax, dword [rax + 8 * rcx]                                    | 13 04 c8                            |
    | adc eax, dword [r8 + 1 * r9]                                      | 43 13 04 08                         |
    | adc eax, dword [r8 + 2 * r9]                                      | 43 13 04 48                         |
    | adc eax, dword [r8 + 4 * r9]                                      | 43 13 04 88                         |
    | adc eax, dword [r8 + 8 * r9]                                      | 43 13 04 c8                         |
    | adc eax, dword [1 * rcx]                                          | 13 04 0d 00 00 00 00                |
    | adc eax, dword [2 * rcx]                                          | 13 04 4d 00 00 00 00                |
    | adc eax, dword [4 * rcx]                                          | 13 04 8d 00 00 00 00                |
    | adc eax, dword [8 * rcx]                                          | 13 04 cd 00 00 00 00                |
    | adc eax, dword [1 * r9]                                           | 42 13 04 0d 00 00 00 00             |
    | adc eax, dword [2 * r9]                                           | 42 13 04 4d 00 00 00 00             |
    | adc eax, dword [4 * r9]                                           | 42 13 04 8d 00 00 00 00             |
    | adc eax, dword [8 * r9]                                           | 42 13 04 cd 00 00 00 00             |
    | adc eax, dword [r13 + 8 * r12]                                    | 43 13 44 e5 00                      |
    | adc eax, dword [rsp + 4 * r15]                                    | 42 13 04 bc                         |
    | adc eax, dword [rax + 1 * rcx + 0x00]                             | 13 44 08 00                         |
    | adc eax, dword [rax + 1 * rcx - 0x00]                             | 13 44 08 00                         |
    | adc eax, dword [rax + 1 * rcx + 0x01]                             | 13 44 08 01                         |
    | adc eax, dword [rax + 1 * rcx - 0x01]                             | 13 44 08 ff                         |
    | adc eax, dword [rax + 1 * rcx + 0x00000001]                       | 13 84 08 01 00 00 00                |
    | adc eax, dword [rax + 1 * rcx - 0x00000001]                       | 13 84 08 ff ff ff ff                |
    | adc eax, dword [rax + 1 * rcx + 0x7f]                             | 13 44 08 7f                         |
    | adc eax, dword [rax + 1 * rcx - 0x7f]                             | 13 44 08 81                         |
    | adc eax, dword [rax + 1 * rcx + 0x80]                             | 13 84 08 80 00 00 00                |
    | adc eax, dword [rax + 1 * rcx - 0x80]                             | 13 44 08 80                         |
    | adc eax, dword [rax + 1 * rcx - 0x81]                             | 13 84 08 7f ff ff ff                |
    | adc eax, dword [rax + 1 * rcx + 0xff]                             | 13 84 08 ff 00 00 00                |
    | adc eax, dword [rax + 1 * rcx - 0xff]                             | 13 84 08 01 ff ff ff                |
    | adc eax, dword [rax + 1 * rcx + 0x7fffffff]                       | 13 84 08 ff ff ff 7f                |
    | adc eax, dword [rax + 1 * rcx - 0x7fffffff]                       | 13 84 08 01 00 00 80                |
    | adc eax, dword [rax + 1 * rcx - 0x80000000]                       | 13 84 08 00 00 00 80                |
    | adc eax, dword [r10 + 0x7f]                                       | 41 13 42 7f                         |
    | adc eax, dword [r10 + 0x80]                                       | 41 13 82 80 00 00 00                |
    | adc eax, dword [r10 - 0x80]                                       | 41 13 42 80                         |
    | adc eax, dword [r10 - 0x81]                                       | 41 13 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc eax, dword [rel @prev5]      | 90 90 90 90 90 13 05 f5 ff ff ff    |
    | .prev1: nop; adc eax, dword [rel @prev1]                          | 90 13 05 f9 ff ff ff                |
    | adc eax, dword [rel @next1]; nop; .next1: nop                     | 13 05 01 00 00 00 90 90             |
    | adc eax, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 13 05 05 00 00 00 90 90 90 90 90 90 |
    | adc ecx, dword [rdx]                                              | 13 0a                               |
    | adc edx, dword [rbx]                                              | 13 13                               |
    | adc ebx, dword [rsp]                                              | 13 1c 24                            |
    | adc esp, dword [rbp]                                              | 13 65 00                            |
    | adc ebp, dword [rsi]                                              | 13 2e                               |
    | adc esi, dword [rdi]                                              | 13 37                               |
    | adc edi, dword [r8]                                               | 41 13 38                            |
    | adc r8d, dword [r9]                                               | 45 13 01                            |
    | adc r9d, dword [r10]                                              | 45 13 0a                            |
    | adc r10d, dword [r11]                                             | 45 13 13                            |
    | adc r11d, dword [r12]                                             | 45 13 1c 24                         |
    | adc r12d, dword [r13]                                             | 45 13 65 00                         |
    | adc r13d, dword [r14]                                             | 45 13 2e                            |
    | adc r14d, dword [r15]                                             | 45 13 37                            |
    | adc r15d, dword [rax + 1 * rcx]                                   | 44 13 3c 08                         |
    | adc ecx, dword [rdx + 1 * rcx]                                    | 13 0c 0a                            |
    | adc edx, dword [rbx + 1 * rcx]                                    | 13 14 0b                            |
    | adc ebx, dword [rsp + 1 * rcx]                                    | 13 1c 0c                            |
    | adc esp, dword [rbp + 1 * rcx]                                    | 13 64 0d 00                         |
    | adc ebp, dword [rsi + 1 * rcx]                                    | 13 2c 0e                            |
    | adc esi, dword [rdi + 1 * rcx]                                    | 13 34 0f                            |
    | adc edi, dword [r8 + 1 * rcx]                                     | 41 13 3c 08                         |
    | adc r8d, dword [r9 + 1 * rcx]                                     | 45 13 04 09                         |
    | adc r9d, dword [r10 + 1 * rcx]                                    | 45 13 0c 0a                         |
    | adc r10d, dword [r11 + 1 * rcx]                                   | 45 13 14 0b                         |
    | adc r11d, dword [r12 + 1 * rcx]                                   | 45 13 1c 0c                         |
    | adc r12d, dword [r13 + 1 * rcx]                                   | 45 13 64 0d 00                      |
    | adc r13d, dword [r14 + 1 * rcx]                                   | 45 13 2c 0e                         |
    | adc r14d, dword [r15 + 1 * rcx]                                   | 45 13 34 0f                         |
    | adc r15d, dword [rax + 1 * rax]                                   | 44 13 3c 00                         |
    | adc ecx, dword [rax + 1 * rbx]                                    | 13 0c 18                            |
    | adc edx, dword [rax + 1 * rbp]                                    | 13 14 28                            |
    | adc ebx, dword [rax + 1 * rsi]                                    | 13 1c 30                            |
    | adc esp, dword [rax + 1 * rdi]                                    | 13 24 38                            |
    | adc ebp, dword [rax + 1 * r8]                                     | 42 13 2c 00                         |
    | adc esi, dword [rax + 1 * r9]                                     | 42 13 34 08                         |
    | adc edi, dword [rax + 1 * r10]                                    | 42 13 3c 10                         |
    | adc r8d, dword [rax + 1 * r11]                                    | 46 13 04 18                         |
    | adc r9d, dword [rax + 1 * r12]                                    | 46 13 0c 20                         |
    | adc r10d, dword [rax + 1 * r13]                                   | 46 13 14 28                         |
    | adc r11d, dword [rax + 1 * r14]                                   | 46 13 1c 30                         |
    | adc r12d, dword [rax + 1 * r15]                                   | 46 13 24 38                         |
    | adc r13d, dword [rax + 2 * rcx]                                   | 44 13 2c 48                         |
    | adc r14d, dword [rax + 4 * rcx]                                   | 44 13 34 88                         |
    | adc r15d, dword [rax + 8 * rcx]                                   | 44 13 3c c8                         |
    | adc ecx, dword [r8 + 2 * r9]                                      | 43 13 0c 48                         |
    | adc edx, dword [r8 + 4 * r9]                                      | 43 13 14 88                         |
    | adc ebx, dword [r8 + 8 * r9]                                      | 43 13 1c c8                         |
    | adc esp, dword [1 * rcx]                                          | 13 24 0d 00 00 00 00                |
    | adc ebp, dword [2 * rcx]                                          | 13 2c 4d 00 00 00 00                |
    | adc esi, dword [4 * rcx]                                          | 13 34 8d 00 00 00 00                |
    | adc edi, dword [8 * rcx]                                          | 13 3c cd 00 00 00 00                |
    | adc r8d, dword [1 * r9]                                           | 46 13 04 0d 00 00 00 00             |
    | adc r9d, dword [2 * r9]                                           | 46 13 0c 4d 00 00 00 00             |
    | adc r10d, dword [4 * r9]                                          | 46 13 14 8d 00 00 00 00             |
    | adc r11d, dword [8 * r9]                                          | 46 13 1c cd 00 00 00 00             |
    | adc r12d, dword [r13 + 8 * r12]                                   | 47 13 64 e5 00                      |
    | adc r13d, dword [rsp + 4 * r15]                                   | 46 13 2c bc                         |
    | adc r14d, dword [rax + 1 * rcx + 0x00]                            | 44 13 74 08 00                      |
    | adc r15d, dword [rax + 1 * rcx - 0x00]                            | 44 13 7c 08 00                      |
    | adc ecx, dword [rax + 1 * rcx - 0x01]                             | 13 4c 08 ff                         |
    | adc edx, dword [rax + 1 * rcx + 0x00000001]                       | 13 94 08 01 00 00 00                |
    | adc ebx, dword [rax + 1 * rcx - 0x00000001]                       | 13 9c 08 ff ff ff ff                |
    | adc esp, dword [rax + 1 * rcx + 0x7f]                             | 13 64 08 7f                         |
    | adc ebp, dword [rax + 1 * rcx - 0x7f]                             | 13 6c 08 81                         |
    | adc esi, dword [rax + 1 * rcx + 0x80]                             | 13 b4 08 80 00 00 00                |
    | adc edi, dword [rax + 1 * rcx - 0x80]                             | 13 7c 08 80                         |
    | adc r8d, dword [rax + 1 * rcx - 0x81]                             | 44 13 84 08 7f ff ff ff             |
    | adc r9d, dword [rax + 1 * rcx + 0xff]                             | 44 13 8c 08 ff 00 00 00             |
    | adc r10d, dword [rax + 1 * rcx - 0xff]                            | 44 13 94 08 01 ff ff ff             |
    | adc r11d, dword [rax + 1 * rcx + 0x7fffffff]                      | 44 13 9c 08 ff ff ff 7f             |
    | adc r12d, dword [rax + 1 * rcx - 0x7fffffff]                      | 44 13 a4 08 01 00 00 80             |
    | adc r13d, dword [rax + 1 * rcx - 0x80000000]                      | 44 13 ac 08 00 00 00 80             |
    | adc r14d, dword [r10 + 0x7f]                                      | 45 13 72 7f                         |
    | adc r15d, dword [r10 + 0x80]                                      | 45 13 ba 80 00 00 00                |
    | adc ecx, dword [r10 - 0x81]                                       | 41 13 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc edx, dword [rel @prev5]      | 90 90 90 90 90 13 15 f5 ff ff ff    |
    | .prev1: nop; adc ebx, dword [rel @prev1]                          | 90 13 1d f9 ff ff ff                |
    | adc esp, dword [rel @next1]; nop; .next1: nop                     | 13 25 01 00 00 00 90 90             |
    | adc ebp, dword [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 13 2d 05 00 00 00 90 90 90 90 90 90 |
    | adc esi, dword [rax]                                              | 13 30                               |
    | ----------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_adc_reg32_addr32():
    encode(ADC_REG32_ADDR32)


ADC_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | adc ax, 0x01   | 66 83 d0 01    | *** | adc ax, 0x00   | 66 83 d0 00    |
    | adc cx, 0x01   | 66 83 d1 01    | *** | adc ax, 0x7f   | 66 83 d0 7f    |
    | adc dx, 0x01   | 66 83 d2 01    | *** | adc ax, 0x80   | 66 83 d0 80    |
    | adc bx, 0x01   | 66 83 d3 01    | *** | adc ax, 0xff   | 66 83 d0 ff    |
    | adc sp, 0x01   | 66 83 d4 01    | *** | adc cx, 0x7f   | 66 83 d1 7f    |
    | adc bp, 0x01   | 66 83 d5 01    | *** | adc dx, 0x80   | 66 83 d2 80    |
    | adc si, 0x01   | 66 83 d6 01    | *** | adc bx, 0xff   | 66 83 d3 ff    |
    | adc di, 0x01   | 66 83 d7 01    | *** | adc sp, 0x00   | 66 83 d4 00    |
    | adc r8w, 0x01  | 66 41 83 d0 01 | *** | adc si, 0x7f   | 66 83 d6 7f    |
    | adc r9w, 0x01  | 66 41 83 d1 01 | *** | adc di, 0x80   | 66 83 d7 80    |
    | adc r10w, 0x01 | 66 41 83 d2 01 | *** | adc r8w, 0xff  | 66 41 83 d0 ff |
    | adc r11w, 0x01 | 66 41 83 d3 01 | *** | adc r9w, 0x00  | 66 41 83 d1 00 |
    | adc r12w, 0x01 | 66 41 83 d4 01 | *** | adc r11w, 0x7f | 66 41 83 d3 7f |
    | adc r13w, 0x01 | 66 41 83 d5 01 | *** | adc r12w, 0x80 | 66 41 83 d4 80 |
    | adc r14w, 0x01 | 66 41 83 d6 01 | *** | adc r13w, 0xff | 66 41 83 d5 ff |
    | adc r15w, 0x01 | 66 41 83 d7 01 | *** | adc r14w, 0x00 | 66 41 83 d6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_adc_reg16_imm8():
    encode(ADC_REG16_IMM8)


ADC_REG16_IMM16 = """
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | instruction      | encoding          | *** | instruction      | encoding          |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
    | adc ax, 0x0001   | 66 15 01 00       | *** | adc ax, 0x00ff   | 66 15 ff 00       |
    | adc cx, 0x0001   | 66 81 d1 01 00    | *** | adc ax, 0x0100   | 66 15 00 01       |
    | adc dx, 0x0001   | 66 81 d2 01 00    | *** | adc ax, 0x7fff   | 66 15 ff 7f       |
    | adc bx, 0x0001   | 66 81 d3 01 00    | *** | adc ax, 0x8000   | 66 15 00 80       |
    | adc sp, 0x0001   | 66 81 d4 01 00    | *** | adc ax, 0xffff   | 66 15 ff ff       |
    | adc bp, 0x0001   | 66 81 d5 01 00    | *** | adc cx, 0x007f   | 66 81 d1 7f 00    |
    | adc si, 0x0001   | 66 81 d6 01 00    | *** | adc dx, 0x0080   | 66 81 d2 80 00    |
    | adc di, 0x0001   | 66 81 d7 01 00    | *** | adc bx, 0x00ff   | 66 81 d3 ff 00    |
    | adc r8w, 0x0001  | 66 41 81 d0 01 00 | *** | adc sp, 0x0100   | 66 81 d4 00 01    |
    | adc r9w, 0x0001  | 66 41 81 d1 01 00 | *** | adc bp, 0x7fff   | 66 81 d5 ff 7f    |
    | adc r10w, 0x0001 | 66 41 81 d2 01 00 | *** | adc si, 0x8000   | 66 81 d6 00 80    |
    | adc r11w, 0x0001 | 66 41 81 d3 01 00 | *** | adc di, 0xffff   | 66 81 d7 ff ff    |
    | adc r12w, 0x0001 | 66 41 81 d4 01 00 | *** | adc r8w, 0x0000  | 66 41 81 d0 00 00 |
    | adc r13w, 0x0001 | 66 41 81 d5 01 00 | *** | adc r10w, 0x007f | 66 41 81 d2 7f 00 |
    | adc r14w, 0x0001 | 66 41 81 d6 01 00 | *** | adc r11w, 0x0080 | 66 41 81 d3 80 00 |
    | adc r15w, 0x0001 | 66 41 81 d7 01 00 | *** | adc r12w, 0x00ff | 66 41 81 d4 ff 00 |
    | adc ax, 0x0000   | 66 15 00 00       | *** | adc r13w, 0x0100 | 66 41 81 d5 00 01 |
    | adc ax, 0x007f   | 66 15 7f 00       | *** | adc r14w, 0x7fff | 66 41 81 d6 ff 7f |
    | adc ax, 0x0080   | 66 15 80 00       | *** | adc r15w, 0x8000 | 66 41 81 d7 00 80 |
    | ---------------- | ----------------- | --- | ---------------- | ----------------- |
"""


def can_encode_adc_reg16_imm16():
    encode(ADC_REG16_IMM16)


ADC_REG16_REG16 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | adc ax, cx     | 66 11 c8    | *** | adc ax, r8w    | 66 44 11 c0 |
    | adc cx, cx     | 66 11 c9    | *** | adc ax, r9w    | 66 44 11 c8 |
    | adc dx, cx     | 66 11 ca    | *** | adc ax, r10w   | 66 44 11 d0 |
    | adc bx, cx     | 66 11 cb    | *** | adc ax, r11w   | 66 44 11 d8 |
    | adc sp, cx     | 66 11 cc    | *** | adc ax, r12w   | 66 44 11 e0 |
    | adc bp, cx     | 66 11 cd    | *** | adc ax, r13w   | 66 44 11 e8 |
    | adc si, cx     | 66 11 ce    | *** | adc ax, r14w   | 66 44 11 f0 |
    | adc di, cx     | 66 11 cf    | *** | adc ax, r15w   | 66 44 11 f8 |
    | adc r8w, cx    | 66 41 11 c8 | *** | adc cx, dx     | 66 11 d1    |
    | adc r9w, cx    | 66 41 11 c9 | *** | adc dx, bx     | 66 11 da    |
    | adc r10w, cx   | 66 41 11 ca | *** | adc bx, sp     | 66 11 e3    |
    | adc r11w, cx   | 66 41 11 cb | *** | adc sp, bp     | 66 11 ec    |
    | adc r12w, cx   | 66 41 11 cc | *** | adc bp, si     | 66 11 f5    |
    | adc r13w, cx   | 66 41 11 cd | *** | adc si, di     | 66 11 fe    |
    | adc r14w, cx   | 66 41 11 ce | *** | adc di, r8w    | 66 44 11 c7 |
    | adc r15w, cx   | 66 41 11 cf | *** | adc r8w, r9w   | 66 45 11 c8 |
    | adc ax, ax     | 66 11 c0    | *** | adc r9w, r10w  | 66 45 11 d1 |
    | adc ax, dx     | 66 11 d0    | *** | adc r10w, r11w | 66 45 11 da |
    | adc ax, bx     | 66 11 d8    | *** | adc r11w, r12w | 66 45 11 e3 |
    | adc ax, sp     | 66 11 e0    | *** | adc r12w, r13w | 66 45 11 ec |
    | adc ax, bp     | 66 11 e8    | *** | adc r13w, r14w | 66 45 11 f5 |
    | adc ax, si     | 66 11 f0    | *** | adc r14w, r15w | 66 45 11 fe |
    | adc ax, di     | 66 11 f8    | *** | adc r15w, ax   | 66 41 11 c7 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_adc_reg16_reg16():
    encode(ADC_REG16_REG16)


ADC_REG16_ADDR16 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | adc ax, word [rcx]                                              | 66 13 01                               |
    | adc cx, word [rcx]                                              | 66 13 09                               |
    | adc dx, word [rcx]                                              | 66 13 11                               |
    | adc bx, word [rcx]                                              | 66 13 19                               |
    | adc sp, word [rcx]                                              | 66 13 21                               |
    | adc bp, word [rcx]                                              | 66 13 29                               |
    | adc si, word [rcx]                                              | 66 13 31                               |
    | adc di, word [rcx]                                              | 66 13 39                               |
    | adc r8w, word [rcx]                                             | 66 44 13 01                            |
    | adc r9w, word [rcx]                                             | 66 44 13 09                            |
    | adc r10w, word [rcx]                                            | 66 44 13 11                            |
    | adc r11w, word [rcx]                                            | 66 44 13 19                            |
    | adc r12w, word [rcx]                                            | 66 44 13 21                            |
    | adc r13w, word [rcx]                                            | 66 44 13 29                            |
    | adc r14w, word [rcx]                                            | 66 44 13 31                            |
    | adc r15w, word [rcx]                                            | 66 44 13 39                            |
    | adc ax, word [rax]                                              | 66 13 00                               |
    | adc ax, word [rdx]                                              | 66 13 02                               |
    | adc ax, word [rbx]                                              | 66 13 03                               |
    | adc ax, word [rsp]                                              | 66 13 04 24                            |
    | adc ax, word [rbp]                                              | 66 13 45 00                            |
    | adc ax, word [rsi]                                              | 66 13 06                               |
    | adc ax, word [rdi]                                              | 66 13 07                               |
    | adc ax, word [r8]                                               | 66 41 13 00                            |
    | adc ax, word [r9]                                               | 66 41 13 01                            |
    | adc ax, word [r10]                                              | 66 41 13 02                            |
    | adc ax, word [r11]                                              | 66 41 13 03                            |
    | adc ax, word [r12]                                              | 66 41 13 04 24                         |
    | adc ax, word [r13]                                              | 66 41 13 45 00                         |
    | adc ax, word [r14]                                              | 66 41 13 06                            |
    | adc ax, word [r15]                                              | 66 41 13 07                            |
    | adc ax, word [rax + 1 * rcx]                                    | 66 13 04 08                            |
    | adc ax, word [rcx + 1 * rcx]                                    | 66 13 04 09                            |
    | adc ax, word [rdx + 1 * rcx]                                    | 66 13 04 0a                            |
    | adc ax, word [rbx + 1 * rcx]                                    | 66 13 04 0b                            |
    | adc ax, word [rsp + 1 * rcx]                                    | 66 13 04 0c                            |
    | adc ax, word [rbp + 1 * rcx]                                    | 66 13 44 0d 00                         |
    | adc ax, word [rsi + 1 * rcx]                                    | 66 13 04 0e                            |
    | adc ax, word [rdi + 1 * rcx]                                    | 66 13 04 0f                            |
    | adc ax, word [r8 + 1 * rcx]                                     | 66 41 13 04 08                         |
    | adc ax, word [r9 + 1 * rcx]                                     | 66 41 13 04 09                         |
    | adc ax, word [r10 + 1 * rcx]                                    | 66 41 13 04 0a                         |
    | adc ax, word [r11 + 1 * rcx]                                    | 66 41 13 04 0b                         |
    | adc ax, word [r12 + 1 * rcx]                                    | 66 41 13 04 0c                         |
    | adc ax, word [r13 + 1 * rcx]                                    | 66 41 13 44 0d 00                      |
    | adc ax, word [r14 + 1 * rcx]                                    | 66 41 13 04 0e                         |
    | adc ax, word [r15 + 1 * rcx]                                    | 66 41 13 04 0f                         |
    | adc ax, word [rax + 1 * rax]                                    | 66 13 04 00                            |
    | adc ax, word [rax + 1 * rdx]                                    | 66 13 04 10                            |
    | adc ax, word [rax + 1 * rbx]                                    | 66 13 04 18                            |
    | adc ax, word [rax + 1 * rbp]                                    | 66 13 04 28                            |
    | adc ax, word [rax + 1 * rsi]                                    | 66 13 04 30                            |
    | adc ax, word [rax + 1 * rdi]                                    | 66 13 04 38                            |
    | adc ax, word [rax + 1 * r8]                                     | 66 42 13 04 00                         |
    | adc ax, word [rax + 1 * r9]                                     | 66 42 13 04 08                         |
    | adc ax, word [rax + 1 * r10]                                    | 66 42 13 04 10                         |
    | adc ax, word [rax + 1 * r11]                                    | 66 42 13 04 18                         |
    | adc ax, word [rax + 1 * r12]                                    | 66 42 13 04 20                         |
    | adc ax, word [rax + 1 * r13]                                    | 66 42 13 04 28                         |
    | adc ax, word [rax + 1 * r14]                                    | 66 42 13 04 30                         |
    | adc ax, word [rax + 1 * r15]                                    | 66 42 13 04 38                         |
    | adc ax, word [rax + 2 * rcx]                                    | 66 13 04 48                            |
    | adc ax, word [rax + 4 * rcx]                                    | 66 13 04 88                            |
    | adc ax, word [rax + 8 * rcx]                                    | 66 13 04 c8                            |
    | adc ax, word [r8 + 1 * r9]                                      | 66 43 13 04 08                         |
    | adc ax, word [r8 + 2 * r9]                                      | 66 43 13 04 48                         |
    | adc ax, word [r8 + 4 * r9]                                      | 66 43 13 04 88                         |
    | adc ax, word [r8 + 8 * r9]                                      | 66 43 13 04 c8                         |
    | adc ax, word [1 * rcx]                                          | 66 13 04 0d 00 00 00 00                |
    | adc ax, word [2 * rcx]                                          | 66 13 04 4d 00 00 00 00                |
    | adc ax, word [4 * rcx]                                          | 66 13 04 8d 00 00 00 00                |
    | adc ax, word [8 * rcx]                                          | 66 13 04 cd 00 00 00 00                |
    | adc ax, word [1 * r9]                                           | 66 42 13 04 0d 00 00 00 00             |
    | adc ax, word [2 * r9]                                           | 66 42 13 04 4d 00 00 00 00             |
    | adc ax, word [4 * r9]                                           | 66 42 13 04 8d 00 00 00 00             |
    | adc ax, word [8 * r9]                                           | 66 42 13 04 cd 00 00 00 00             |
    | adc ax, word [r13 + 8 * r12]                                    | 66 43 13 44 e5 00                      |
    | adc ax, word [rsp + 4 * r15]                                    | 66 42 13 04 bc                         |
    | adc ax, word [rax + 1 * rcx + 0x00]                             | 66 13 44 08 00                         |
    | adc ax, word [rax + 1 * rcx - 0x00]                             | 66 13 44 08 00                         |
    | adc ax, word [rax + 1 * rcx + 0x01]                             | 66 13 44 08 01                         |
    | adc ax, word [rax + 1 * rcx - 0x01]                             | 66 13 44 08 ff                         |
    | adc ax, word [rax + 1 * rcx + 0x00000001]                       | 66 13 84 08 01 00 00 00                |
    | adc ax, word [rax + 1 * rcx - 0x00000001]                       | 66 13 84 08 ff ff ff ff                |
    | adc ax, word [rax + 1 * rcx + 0x7f]                             | 66 13 44 08 7f                         |
    | adc ax, word [rax + 1 * rcx - 0x7f]                             | 66 13 44 08 81                         |
    | adc ax, word [rax + 1 * rcx + 0x80]                             | 66 13 84 08 80 00 00 00                |
    | adc ax, word [rax + 1 * rcx - 0x80]                             | 66 13 44 08 80                         |
    | adc ax, word [rax + 1 * rcx - 0x81]                             | 66 13 84 08 7f ff ff ff                |
    | adc ax, word [rax + 1 * rcx + 0xff]                             | 66 13 84 08 ff 00 00 00                |
    | adc ax, word [rax + 1 * rcx - 0xff]                             | 66 13 84 08 01 ff ff ff                |
    | adc ax, word [rax + 1 * rcx + 0x7fffffff]                       | 66 13 84 08 ff ff ff 7f                |
    | adc ax, word [rax + 1 * rcx - 0x7fffffff]                       | 66 13 84 08 01 00 00 80                |
    | adc ax, word [rax + 1 * rcx - 0x80000000]                       | 66 13 84 08 00 00 00 80                |
    | adc ax, word [r10 + 0x7f]                                       | 66 41 13 42 7f                         |
    | adc ax, word [r10 + 0x80]                                       | 66 41 13 82 80 00 00 00                |
    | adc ax, word [r10 - 0x80]                                       | 66 41 13 42 80                         |
    | adc ax, word [r10 - 0x81]                                       | 66 41 13 82 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc ax, word [rel @prev5]      | 90 90 90 90 90 66 13 05 f4 ff ff ff    |
    | .prev1: nop; adc ax, word [rel @prev1]                          | 90 66 13 05 f8 ff ff ff                |
    | adc ax, word [rel @next1]; nop; .next1: nop                     | 66 13 05 01 00 00 00 90 90             |
    | adc ax, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 13 05 05 00 00 00 90 90 90 90 90 90 |
    | adc cx, word [rdx]                                              | 66 13 0a                               |
    | adc dx, word [rbx]                                              | 66 13 13                               |
    | adc bx, word [rsp]                                              | 66 13 1c 24                            |
    | adc sp, word [rbp]                                              | 66 13 65 00                            |
    | adc bp, word [rsi]                                              | 66 13 2e                               |
    | adc si, word [rdi]                                              | 66 13 37                               |
    | adc di, word [r8]                                               | 66 41 13 38                            |
    | adc r8w, word [r9]                                              | 66 45 13 01                            |
    | adc r9w, word [r10]                                             | 66 45 13 0a                            |
    | adc r10w, word [r11]                                            | 66 45 13 13                            |
    | adc r11w, word [r12]                                            | 66 45 13 1c 24                         |
    | adc r12w, word [r13]                                            | 66 45 13 65 00                         |
    | adc r13w, word [r14]                                            | 66 45 13 2e                            |
    | adc r14w, word [r15]                                            | 66 45 13 37                            |
    | adc r15w, word [rax + 1 * rcx]                                  | 66 44 13 3c 08                         |
    | adc cx, word [rdx + 1 * rcx]                                    | 66 13 0c 0a                            |
    | adc dx, word [rbx + 1 * rcx]                                    | 66 13 14 0b                            |
    | adc bx, word [rsp + 1 * rcx]                                    | 66 13 1c 0c                            |
    | adc sp, word [rbp + 1 * rcx]                                    | 66 13 64 0d 00                         |
    | adc bp, word [rsi + 1 * rcx]                                    | 66 13 2c 0e                            |
    | adc si, word [rdi + 1 * rcx]                                    | 66 13 34 0f                            |
    | adc di, word [r8 + 1 * rcx]                                     | 66 41 13 3c 08                         |
    | adc r8w, word [r9 + 1 * rcx]                                    | 66 45 13 04 09                         |
    | adc r9w, word [r10 + 1 * rcx]                                   | 66 45 13 0c 0a                         |
    | adc r10w, word [r11 + 1 * rcx]                                  | 66 45 13 14 0b                         |
    | adc r11w, word [r12 + 1 * rcx]                                  | 66 45 13 1c 0c                         |
    | adc r12w, word [r13 + 1 * rcx]                                  | 66 45 13 64 0d 00                      |
    | adc r13w, word [r14 + 1 * rcx]                                  | 66 45 13 2c 0e                         |
    | adc r14w, word [r15 + 1 * rcx]                                  | 66 45 13 34 0f                         |
    | adc r15w, word [rax + 1 * rax]                                  | 66 44 13 3c 00                         |
    | adc cx, word [rax + 1 * rbx]                                    | 66 13 0c 18                            |
    | adc dx, word [rax + 1 * rbp]                                    | 66 13 14 28                            |
    | adc bx, word [rax + 1 * rsi]                                    | 66 13 1c 30                            |
    | adc sp, word [rax + 1 * rdi]                                    | 66 13 24 38                            |
    | adc bp, word [rax + 1 * r8]                                     | 66 42 13 2c 00                         |
    | adc si, word [rax + 1 * r9]                                     | 66 42 13 34 08                         |
    | adc di, word [rax + 1 * r10]                                    | 66 42 13 3c 10                         |
    | adc r8w, word [rax + 1 * r11]                                   | 66 46 13 04 18                         |
    | adc r9w, word [rax + 1 * r12]                                   | 66 46 13 0c 20                         |
    | adc r10w, word [rax + 1 * r13]                                  | 66 46 13 14 28                         |
    | adc r11w, word [rax + 1 * r14]                                  | 66 46 13 1c 30                         |
    | adc r12w, word [rax + 1 * r15]                                  | 66 46 13 24 38                         |
    | adc r13w, word [rax + 2 * rcx]                                  | 66 44 13 2c 48                         |
    | adc r14w, word [rax + 4 * rcx]                                  | 66 44 13 34 88                         |
    | adc r15w, word [rax + 8 * rcx]                                  | 66 44 13 3c c8                         |
    | adc cx, word [r8 + 2 * r9]                                      | 66 43 13 0c 48                         |
    | adc dx, word [r8 + 4 * r9]                                      | 66 43 13 14 88                         |
    | adc bx, word [r8 + 8 * r9]                                      | 66 43 13 1c c8                         |
    | adc sp, word [1 * rcx]                                          | 66 13 24 0d 00 00 00 00                |
    | adc bp, word [2 * rcx]                                          | 66 13 2c 4d 00 00 00 00                |
    | adc si, word [4 * rcx]                                          | 66 13 34 8d 00 00 00 00                |
    | adc di, word [8 * rcx]                                          | 66 13 3c cd 00 00 00 00                |
    | adc r8w, word [1 * r9]                                          | 66 46 13 04 0d 00 00 00 00             |
    | adc r9w, word [2 * r9]                                          | 66 46 13 0c 4d 00 00 00 00             |
    | adc r10w, word [4 * r9]                                         | 66 46 13 14 8d 00 00 00 00             |
    | adc r11w, word [8 * r9]                                         | 66 46 13 1c cd 00 00 00 00             |
    | adc r12w, word [r13 + 8 * r12]                                  | 66 47 13 64 e5 00                      |
    | adc r13w, word [rsp + 4 * r15]                                  | 66 46 13 2c bc                         |
    | adc r14w, word [rax + 1 * rcx + 0x00]                           | 66 44 13 74 08 00                      |
    | adc r15w, word [rax + 1 * rcx - 0x00]                           | 66 44 13 7c 08 00                      |
    | adc cx, word [rax + 1 * rcx - 0x01]                             | 66 13 4c 08 ff                         |
    | adc dx, word [rax + 1 * rcx + 0x00000001]                       | 66 13 94 08 01 00 00 00                |
    | adc bx, word [rax + 1 * rcx - 0x00000001]                       | 66 13 9c 08 ff ff ff ff                |
    | adc sp, word [rax + 1 * rcx + 0x7f]                             | 66 13 64 08 7f                         |
    | adc bp, word [rax + 1 * rcx - 0x7f]                             | 66 13 6c 08 81                         |
    | adc si, word [rax + 1 * rcx + 0x80]                             | 66 13 b4 08 80 00 00 00                |
    | adc di, word [rax + 1 * rcx - 0x80]                             | 66 13 7c 08 80                         |
    | adc r8w, word [rax + 1 * rcx - 0x81]                            | 66 44 13 84 08 7f ff ff ff             |
    | adc r9w, word [rax + 1 * rcx + 0xff]                            | 66 44 13 8c 08 ff 00 00 00             |
    | adc r10w, word [rax + 1 * rcx - 0xff]                           | 66 44 13 94 08 01 ff ff ff             |
    | adc r11w, word [rax + 1 * rcx + 0x7fffffff]                     | 66 44 13 9c 08 ff ff ff 7f             |
    | adc r12w, word [rax + 1 * rcx - 0x7fffffff]                     | 66 44 13 a4 08 01 00 00 80             |
    | adc r13w, word [rax + 1 * rcx - 0x80000000]                     | 66 44 13 ac 08 00 00 00 80             |
    | adc r14w, word [r10 + 0x7f]                                     | 66 45 13 72 7f                         |
    | adc r15w, word [r10 + 0x80]                                     | 66 45 13 ba 80 00 00 00                |
    | adc cx, word [r10 - 0x81]                                       | 66 41 13 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc dx, word [rel @prev5]      | 90 90 90 90 90 66 13 15 f4 ff ff ff    |
    | .prev1: nop; adc bx, word [rel @prev1]                          | 90 66 13 1d f8 ff ff ff                |
    | adc sp, word [rel @next1]; nop; .next1: nop                     | 66 13 25 01 00 00 00 90 90             |
    | adc bp, word [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 66 13 2d 05 00 00 00 90 90 90 90 90 90 |
    | adc si, word [rax]                                              | 66 13 30                               |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_adc_reg16_addr16():
    encode(ADC_REG16_ADDR16)


ADC_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | adc al, 0x01   | 14 01       | *** | adc al, 0x00   | 14 00       |
    | adc cl, 0x01   | 80 d1 01    | *** | adc al, 0x7f   | 14 7f       |
    | adc dl, 0x01   | 80 d2 01    | *** | adc al, 0x80   | 14 80       |
    | adc bl, 0x01   | 80 d3 01    | *** | adc al, 0xff   | 14 ff       |
    | adc spl, 0x01  | 40 80 d4 01 | *** | adc cl, 0x7f   | 80 d1 7f    |
    | adc bpl, 0x01  | 40 80 d5 01 | *** | adc dl, 0x80   | 80 d2 80    |
    | adc sil, 0x01  | 40 80 d6 01 | *** | adc bl, 0xff   | 80 d3 ff    |
    | adc dil, 0x01  | 40 80 d7 01 | *** | adc spl, 0x00  | 40 80 d4 00 |
    | adc r8b, 0x01  | 41 80 d0 01 | *** | adc sil, 0x7f  | 40 80 d6 7f |
    | adc r9b, 0x01  | 41 80 d1 01 | *** | adc dil, 0x80  | 40 80 d7 80 |
    | adc r10b, 0x01 | 41 80 d2 01 | *** | adc r8b, 0xff  | 41 80 d0 ff |
    | adc r11b, 0x01 | 41 80 d3 01 | *** | adc r9b, 0x00  | 41 80 d1 00 |
    | adc r12b, 0x01 | 41 80 d4 01 | *** | adc r11b, 0x7f | 41 80 d3 7f |
    | adc r13b, 0x01 | 41 80 d5 01 | *** | adc r12b, 0x80 | 41 80 d4 80 |
    | adc r14b, 0x01 | 41 80 d6 01 | *** | adc r13b, 0xff | 41 80 d5 ff |
    | adc r15b, 0x01 | 41 80 d7 01 | *** | adc r14b, 0x00 | 41 80 d6 00 |
    | adc ah, 0x01   | 80 d4 01    | *** | adc ah, 0x7f   | 80 d4 7f    |
    | adc ch, 0x01   | 80 d5 01    | *** | adc ch, 0x80   | 80 d5 80    |
    | adc dh, 0x01   | 80 d6 01    | *** | adc dh, 0xff   | 80 d6 ff    |
    | adc bh, 0x01   | 80 d7 01    | *** | adc bh, 0x00   | 80 d7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_adc_reg8_imm8():
    encode(ADC_REG8_IMM8)


ADC_REG8_REG8 = """
    | -------------- | -------- | --- | -------------- | -------- |
    | instruction    | encoding | *** | instruction    | encoding |
    | -------------- | -------- | --- | -------------- | -------- |
    | adc al, cl     | 10 c8    | *** | adc al, r10b   | 44 10 d0 |
    | adc cl, cl     | 10 c9    | *** | adc al, r11b   | 44 10 d8 |
    | adc dl, cl     | 10 ca    | *** | adc al, r12b   | 44 10 e0 |
    | adc bl, cl     | 10 cb    | *** | adc al, r13b   | 44 10 e8 |
    | adc spl, cl    | 40 10 cc | *** | adc al, r14b   | 44 10 f0 |
    | adc bpl, cl    | 40 10 cd | *** | adc al, r15b   | 44 10 f8 |
    | adc sil, cl    | 40 10 ce | *** | adc al, ah     | 10 e0    |
    | adc dil, cl    | 40 10 cf | *** | adc al, ch     | 10 e8    |
    | adc r8b, cl    | 41 10 c8 | *** | adc al, dh     | 10 f0    |
    | adc r9b, cl    | 41 10 c9 | *** | adc al, bh     | 10 f8    |
    | adc r10b, cl   | 41 10 ca | *** | adc cl, dl     | 10 d1    |
    | adc r11b, cl   | 41 10 cb | *** | adc dl, bl     | 10 da    |
    | adc r12b, cl   | 41 10 cc | *** | adc bl, spl    | 40 10 e3 |
    | adc r13b, cl   | 41 10 cd | *** | adc spl, bpl   | 40 10 ec |
    | adc r14b, cl   | 41 10 ce | *** | adc bpl, sil   | 40 10 f5 |
    | adc r15b, cl   | 41 10 cf | *** | adc sil, dil   | 40 10 fe |
    | adc ah, cl     | 10 cc    | *** | adc dil, r8b   | 44 10 c7 |
    | adc ch, cl     | 10 cd    | *** | adc r8b, r9b   | 45 10 c8 |
    | adc dh, cl     | 10 ce    | *** | adc r9b, r10b  | 45 10 d1 |
    | adc bh, cl     | 10 cf    | *** | adc r10b, r11b | 45 10 da |
    | adc al, al     | 10 c0    | *** | adc r11b, r12b | 45 10 e3 |
    | adc al, dl     | 10 d0    | *** | adc r12b, r13b | 45 10 ec |
    | adc al, bl     | 10 d8    | *** | adc r13b, r14b | 45 10 f5 |
    | adc al, spl    | 40 10 e0 | *** | adc r14b, r15b | 45 10 fe |
    | adc al, bpl    | 40 10 e8 | *** | adc r15b, ah   | !! !! !! |
    | adc al, sil    | 40 10 f0 | *** | adc ah, ch     | 10 ec    |
    | adc al, dil    | 40 10 f8 | *** | adc ch, dh     | 10 f5    |
    | adc al, r8b    | 44 10 c0 | *** | adc dh, bh     | 10 fe    |
    | adc al, r9b    | 44 10 c8 | *** | adc bh, al     | 10 c7    |
    | -------------- | -------- | --- | -------------- | -------- |
"""


def can_encode_adc_reg8_reg8():
    encode(ADC_REG8_REG8)


ADC_REG8_ADDR8 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | adc al, byte [rcx]                                               | 12 01                                  |
    | adc cl, byte [rcx]                                               | 12 09                                  |
    | adc dl, byte [rcx]                                               | 12 11                                  |
    | adc bl, byte [rcx]                                               | 12 19                                  |
    | adc spl, byte [rcx]                                              | 40 12 21                               |
    | adc bpl, byte [rcx]                                              | 40 12 29                               |
    | adc sil, byte [rcx]                                              | 40 12 31                               |
    | adc dil, byte [rcx]                                              | 40 12 39                               |
    | adc r8b, byte [rcx]                                              | 44 12 01                               |
    | adc r9b, byte [rcx]                                              | 44 12 09                               |
    | adc r10b, byte [rcx]                                             | 44 12 11                               |
    | adc r11b, byte [rcx]                                             | 44 12 19                               |
    | adc r12b, byte [rcx]                                             | 44 12 21                               |
    | adc r13b, byte [rcx]                                             | 44 12 29                               |
    | adc r14b, byte [rcx]                                             | 44 12 31                               |
    | adc r15b, byte [rcx]                                             | 44 12 39                               |
    | adc ah, byte [rcx]                                               | 12 21                                  |
    | adc ch, byte [rcx]                                               | 12 29                                  |
    | adc dh, byte [rcx]                                               | 12 31                                  |
    | adc bh, byte [rcx]                                               | 12 39                                  |
    | adc al, byte [rax]                                               | 12 00                                  |
    | adc al, byte [rdx]                                               | 12 02                                  |
    | adc al, byte [rbx]                                               | 12 03                                  |
    | adc al, byte [rsp]                                               | 12 04 24                               |
    | adc al, byte [rbp]                                               | 12 45 00                               |
    | adc al, byte [rsi]                                               | 12 06                                  |
    | adc al, byte [rdi]                                               | 12 07                                  |
    | adc al, byte [r8]                                                | 41 12 00                               |
    | adc al, byte [r9]                                                | 41 12 01                               |
    | adc al, byte [r10]                                               | 41 12 02                               |
    | adc al, byte [r11]                                               | 41 12 03                               |
    | adc al, byte [r12]                                               | 41 12 04 24                            |
    | adc al, byte [r13]                                               | 41 12 45 00                            |
    | adc al, byte [r14]                                               | 41 12 06                               |
    | adc al, byte [r15]                                               | 41 12 07                               |
    | adc al, byte [rax + 1 * rcx]                                     | 12 04 08                               |
    | adc al, byte [rcx + 1 * rcx]                                     | 12 04 09                               |
    | adc al, byte [rdx + 1 * rcx]                                     | 12 04 0a                               |
    | adc al, byte [rbx + 1 * rcx]                                     | 12 04 0b                               |
    | adc al, byte [rsp + 1 * rcx]                                     | 12 04 0c                               |
    | adc al, byte [rbp + 1 * rcx]                                     | 12 44 0d 00                            |
    | adc al, byte [rsi + 1 * rcx]                                     | 12 04 0e                               |
    | adc al, byte [rdi + 1 * rcx]                                     | 12 04 0f                               |
    | adc al, byte [r8 + 1 * rcx]                                      | 41 12 04 08                            |
    | adc al, byte [r9 + 1 * rcx]                                      | 41 12 04 09                            |
    | adc al, byte [r10 + 1 * rcx]                                     | 41 12 04 0a                            |
    | adc al, byte [r11 + 1 * rcx]                                     | 41 12 04 0b                            |
    | adc al, byte [r12 + 1 * rcx]                                     | 41 12 04 0c                            |
    | adc al, byte [r13 + 1 * rcx]                                     | 41 12 44 0d 00                         |
    | adc al, byte [r14 + 1 * rcx]                                     | 41 12 04 0e                            |
    | adc al, byte [r15 + 1 * rcx]                                     | 41 12 04 0f                            |
    | adc al, byte [rax + 1 * rax]                                     | 12 04 00                               |
    | adc al, byte [rax + 1 * rdx]                                     | 12 04 10                               |
    | adc al, byte [rax + 1 * rbx]                                     | 12 04 18                               |
    | adc al, byte [rax + 1 * rbp]                                     | 12 04 28                               |
    | adc al, byte [rax + 1 * rsi]                                     | 12 04 30                               |
    | adc al, byte [rax + 1 * rdi]                                     | 12 04 38                               |
    | adc al, byte [rax + 1 * r8]                                      | 42 12 04 00                            |
    | adc al, byte [rax + 1 * r9]                                      | 42 12 04 08                            |
    | adc al, byte [rax + 1 * r10]                                     | 42 12 04 10                            |
    | adc al, byte [rax + 1 * r11]                                     | 42 12 04 18                            |
    | adc al, byte [rax + 1 * r12]                                     | 42 12 04 20                            |
    | adc al, byte [rax + 1 * r13]                                     | 42 12 04 28                            |
    | adc al, byte [rax + 1 * r14]                                     | 42 12 04 30                            |
    | adc al, byte [rax + 1 * r15]                                     | 42 12 04 38                            |
    | adc al, byte [rax + 2 * rcx]                                     | 12 04 48                               |
    | adc al, byte [rax + 4 * rcx]                                     | 12 04 88                               |
    | adc al, byte [rax + 8 * rcx]                                     | 12 04 c8                               |
    | adc al, byte [r8 + 1 * r9]                                       | 43 12 04 08                            |
    | adc al, byte [r8 + 2 * r9]                                       | 43 12 04 48                            |
    | adc al, byte [r8 + 4 * r9]                                       | 43 12 04 88                            |
    | adc al, byte [r8 + 8 * r9]                                       | 43 12 04 c8                            |
    | adc al, byte [1 * rcx]                                           | 12 04 0d 00 00 00 00                   |
    | adc al, byte [2 * rcx]                                           | 12 04 4d 00 00 00 00                   |
    | adc al, byte [4 * rcx]                                           | 12 04 8d 00 00 00 00                   |
    | adc al, byte [8 * rcx]                                           | 12 04 cd 00 00 00 00                   |
    | adc al, byte [1 * r9]                                            | 42 12 04 0d 00 00 00 00                |
    | adc al, byte [2 * r9]                                            | 42 12 04 4d 00 00 00 00                |
    | adc al, byte [4 * r9]                                            | 42 12 04 8d 00 00 00 00                |
    | adc al, byte [8 * r9]                                            | 42 12 04 cd 00 00 00 00                |
    | adc al, byte [r13 + 8 * r12]                                     | 43 12 44 e5 00                         |
    | adc al, byte [rsp + 4 * r15]                                     | 42 12 04 bc                            |
    | adc al, byte [rax + 1 * rcx + 0x00]                              | 12 44 08 00                            |
    | adc al, byte [rax + 1 * rcx - 0x00]                              | 12 44 08 00                            |
    | adc al, byte [rax + 1 * rcx + 0x01]                              | 12 44 08 01                            |
    | adc al, byte [rax + 1 * rcx - 0x01]                              | 12 44 08 ff                            |
    | adc al, byte [rax + 1 * rcx + 0x00000001]                        | 12 84 08 01 00 00 00                   |
    | adc al, byte [rax + 1 * rcx - 0x00000001]                        | 12 84 08 ff ff ff ff                   |
    | adc al, byte [rax + 1 * rcx + 0x7f]                              | 12 44 08 7f                            |
    | adc al, byte [rax + 1 * rcx - 0x7f]                              | 12 44 08 81                            |
    | adc al, byte [rax + 1 * rcx + 0x80]                              | 12 84 08 80 00 00 00                   |
    | adc al, byte [rax + 1 * rcx - 0x80]                              | 12 44 08 80                            |
    | adc al, byte [rax + 1 * rcx - 0x81]                              | 12 84 08 7f ff ff ff                   |
    | adc al, byte [rax + 1 * rcx + 0xff]                              | 12 84 08 ff 00 00 00                   |
    | adc al, byte [rax + 1 * rcx - 0xff]                              | 12 84 08 01 ff ff ff                   |
    | adc al, byte [rax + 1 * rcx + 0x7fffffff]                        | 12 84 08 ff ff ff 7f                   |
    | adc al, byte [rax + 1 * rcx - 0x7fffffff]                        | 12 84 08 01 00 00 80                   |
    | adc al, byte [rax + 1 * rcx - 0x80000000]                        | 12 84 08 00 00 00 80                   |
    | adc al, byte [r10 + 0x7f]                                        | 41 12 42 7f                            |
    | adc al, byte [r10 + 0x80]                                        | 41 12 82 80 00 00 00                   |
    | adc al, byte [r10 - 0x80]                                        | 41 12 42 80                            |
    | adc al, byte [r10 - 0x81]                                        | 41 12 82 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc al, byte [rel @prev5]       | 90 90 90 90 90 12 05 f5 ff ff ff       |
    | .prev1: nop; adc al, byte [rel @prev1]                           | 90 12 05 f9 ff ff ff                   |
    | adc al, byte [rel @next1]; nop; .next1: nop                      | 12 05 01 00 00 00 90 90                |
    | adc al, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop  | 12 05 05 00 00 00 90 90 90 90 90 90    |
    | adc cl, byte [rdx]                                               | 12 0a                                  |
    | adc dl, byte [rbx]                                               | 12 13                                  |
    | adc bl, byte [rsp]                                               | 12 1c 24                               |
    | adc spl, byte [rbp]                                              | 40 12 65 00                            |
    | adc bpl, byte [rsi]                                              | 40 12 2e                               |
    | adc sil, byte [rdi]                                              | 40 12 37                               |
    | adc dil, byte [r8]                                               | 41 12 38                               |
    | adc r8b, byte [r9]                                               | 45 12 01                               |
    | adc r9b, byte [r10]                                              | 45 12 0a                               |
    | adc r10b, byte [r11]                                             | 45 12 13                               |
    | adc r11b, byte [r12]                                             | 45 12 1c 24                            |
    | adc r12b, byte [r13]                                             | 45 12 65 00                            |
    | adc r13b, byte [r14]                                             | 45 12 2e                               |
    | adc r14b, byte [r15]                                             | 45 12 37                               |
    | adc r15b, byte [rax + 1 * rcx]                                   | 44 12 3c 08                            |
    | adc ah, byte [rcx + 1 * rcx]                                     | 12 24 09                               |
    | adc ch, byte [rdx + 1 * rcx]                                     | 12 2c 0a                               |
    | adc dh, byte [rbx + 1 * rcx]                                     | 12 34 0b                               |
    | adc bh, byte [rsp + 1 * rcx]                                     | 12 3c 0c                               |
    | adc cl, byte [rsi + 1 * rcx]                                     | 12 0c 0e                               |
    | adc dl, byte [rdi + 1 * rcx]                                     | 12 14 0f                               |
    | adc bl, byte [r8 + 1 * rcx]                                      | 41 12 1c 08                            |
    | adc spl, byte [r9 + 1 * rcx]                                     | 41 12 24 09                            |
    | adc bpl, byte [r10 + 1 * rcx]                                    | 41 12 2c 0a                            |
    | adc sil, byte [r11 + 1 * rcx]                                    | 41 12 34 0b                            |
    | adc dil, byte [r12 + 1 * rcx]                                    | 41 12 3c 0c                            |
    | adc r8b, byte [r13 + 1 * rcx]                                    | 45 12 44 0d 00                         |
    | adc r9b, byte [r14 + 1 * rcx]                                    | 45 12 0c 0e                            |
    | adc r10b, byte [r15 + 1 * rcx]                                   | 45 12 14 0f                            |
    | adc r11b, byte [rax + 1 * rax]                                   | 44 12 1c 00                            |
    | adc r12b, byte [rax + 1 * rdx]                                   | 44 12 24 10                            |
    | adc r13b, byte [rax + 1 * rbx]                                   | 44 12 2c 18                            |
    | adc r14b, byte [rax + 1 * rbp]                                   | 44 12 34 28                            |
    | adc r15b, byte [rax + 1 * rsi]                                   | 44 12 3c 30                            |
    | adc ah, byte [rax + 1 * rdi]                                     | 12 24 38                               |
    | adc ch, byte [rax + 1 * r8]                                      | !! !! !!                               |
    | adc dh, byte [rax + 1 * r9]                                      | !! !! !!                               |
    | adc bh, byte [rax + 1 * r10]                                     | !! !! !!                               |
    | adc cl, byte [rax + 1 * r12]                                     | 42 12 0c 20                            |
    | adc dl, byte [rax + 1 * r13]                                     | 42 12 14 28                            |
    | adc bl, byte [rax + 1 * r14]                                     | 42 12 1c 30                            |
    | adc spl, byte [rax + 1 * r15]                                    | 42 12 24 38                            |
    | adc bpl, byte [rax + 2 * rcx]                                    | 40 12 2c 48                            |
    | adc sil, byte [rax + 4 * rcx]                                    | 40 12 34 88                            |
    | adc dil, byte [rax + 8 * rcx]                                    | 40 12 3c c8                            |
    | adc r8b, byte [r8 + 1 * r9]                                      | 47 12 04 08                            |
    | adc r9b, byte [r8 + 2 * r9]                                      | 47 12 0c 48                            |
    | adc r10b, byte [r8 + 4 * r9]                                     | 47 12 14 88                            |
    | adc r11b, byte [r8 + 8 * r9]                                     | 47 12 1c c8                            |
    | adc r12b, byte [1 * rcx]                                         | 44 12 24 0d 00 00 00 00                |
    | adc r13b, byte [2 * rcx]                                         | 44 12 2c 4d 00 00 00 00                |
    | adc r14b, byte [4 * rcx]                                         | 44 12 34 8d 00 00 00 00                |
    | adc r15b, byte [8 * rcx]                                         | 44 12 3c cd 00 00 00 00                |
    | adc ah, byte [1 * r9]                                            | !! !! !!                               |
    | adc ch, byte [2 * r9]                                            | !! !! !!                               |
    | adc dh, byte [4 * r9]                                            | !! !! !!                               |
    | adc bh, byte [8 * r9]                                            | !! !! !!                               |
    | adc cl, byte [rsp + 4 * r15]                                     | 42 12 0c bc                            |
    | adc dl, byte [rax + 1 * rcx + 0x00]                              | 12 54 08 00                            |
    | adc bl, byte [rax + 1 * rcx - 0x00]                              | 12 5c 08 00                            |
    | adc spl, byte [rax + 1 * rcx + 0x01]                             | 40 12 64 08 01                         |
    | adc bpl, byte [rax + 1 * rcx - 0x01]                             | 40 12 6c 08 ff                         |
    | adc sil, byte [rax + 1 * rcx + 0x00000001]                       | 40 12 b4 08 01 00 00 00                |
    | adc dil, byte [rax + 1 * rcx - 0x00000001]                       | 40 12 bc 08 ff ff ff ff                |
    | adc r8b, byte [rax + 1 * rcx + 0x7f]                             | 44 12 44 08 7f                         |
    | adc r9b, byte [rax + 1 * rcx - 0x7f]                             | 44 12 4c 08 81                         |
    | adc r10b, byte [rax + 1 * rcx + 0x80]                            | 44 12 94 08 80 00 00 00                |
    | adc r11b, byte [rax + 1 * rcx - 0x80]                            | 44 12 5c 08 80                         |
    | adc r12b, byte [rax + 1 * rcx - 0x81]                            | 44 12 a4 08 7f ff ff ff                |
    | adc r13b, byte [rax + 1 * rcx + 0xff]                            | 44 12 ac 08 ff 00 00 00                |
    | adc r14b, byte [rax + 1 * rcx - 0xff]                            | 44 12 b4 08 01 ff ff ff                |
    | adc r15b, byte [rax + 1 * rcx + 0x7fffffff]                      | 44 12 bc 08 ff ff ff 7f                |
    | adc ah, byte [rax + 1 * rcx - 0x7fffffff]                        | 12 a4 08 01 00 00 80                   |
    | adc ch, byte [rax + 1 * rcx - 0x80000000]                        | 12 ac 08 00 00 00 80                   |
    | adc dh, byte [r10 + 0x7f]                                        | !! !! !!                               |
    | adc bh, byte [r10 + 0x80]                                        | !! !! !!                               |
    | adc cl, byte [r10 - 0x81]                                        | 41 12 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc dl, byte [rel @prev5]       | 90 90 90 90 90 12 15 f5 ff ff ff       |
    | .prev1: nop; adc bl, byte [rel @prev1]                           | 90 12 1d f9 ff ff ff                   |
    | adc spl, byte [rel @next1]; nop; .next1: nop                     | 40 12 25 01 00 00 00 90 90             |
    | adc bpl, byte [rel @next5]; nop; nop; nop; nop; nop; .next5: nop | 40 12 2d 05 00 00 00 90 90 90 90 90 90 |
    | adc sil, byte [rax]                                              | 40 12 30                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_adc_reg8_addr8():
    encode(ADC_REG8_ADDR8)


ADC_ADDR64_IMM8 = """
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | instruction                                                        | encoding                                  |
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | adc qword [rax], 0x01                                              | 48 83 10 01                               |
    | adc qword [rcx], 0x01                                              | 48 83 11 01                               |
    | adc qword [rdx], 0x01                                              | 48 83 12 01                               |
    | adc qword [rbx], 0x01                                              | 48 83 13 01                               |
    | adc qword [rsp], 0x01                                              | 48 83 14 24 01                            |
    | adc qword [rbp], 0x01                                              | 48 83 55 00 01                            |
    | adc qword [rsi], 0x01                                              | 48 83 16 01                               |
    | adc qword [rdi], 0x01                                              | 48 83 17 01                               |
    | adc qword [r8], 0x01                                               | 49 83 10 01                               |
    | adc qword [r9], 0x01                                               | 49 83 11 01                               |
    | adc qword [r10], 0x01                                              | 49 83 12 01                               |
    | adc qword [r11], 0x01                                              | 49 83 13 01                               |
    | adc qword [r12], 0x01                                              | 49 83 14 24 01                            |
    | adc qword [r13], 0x01                                              | 49 83 55 00 01                            |
    | adc qword [r14], 0x01                                              | 49 83 16 01                               |
    | adc qword [r15], 0x01                                              | 49 83 17 01                               |
    | adc qword [rax + 1 * rcx], 0x01                                    | 48 83 14 08 01                            |
    | adc qword [rcx + 1 * rcx], 0x01                                    | 48 83 14 09 01                            |
    | adc qword [rdx + 1 * rcx], 0x01                                    | 48 83 14 0a 01                            |
    | adc qword [rbx + 1 * rcx], 0x01                                    | 48 83 14 0b 01                            |
    | adc qword [rsp + 1 * rcx], 0x01                                    | 48 83 14 0c 01                            |
    | adc qword [rbp + 1 * rcx], 0x01                                    | 48 83 54 0d 00 01                         |
    | adc qword [rsi + 1 * rcx], 0x01                                    | 48 83 14 0e 01                            |
    | adc qword [rdi + 1 * rcx], 0x01                                    | 48 83 14 0f 01                            |
    | adc qword [r8 + 1 * rcx], 0x01                                     | 49 83 14 08 01                            |
    | adc qword [r9 + 1 * rcx], 0x01                                     | 49 83 14 09 01                            |
    | adc qword [r10 + 1 * rcx], 0x01                                    | 49 83 14 0a 01                            |
    | adc qword [r11 + 1 * rcx], 0x01                                    | 49 83 14 0b 01                            |
    | adc qword [r12 + 1 * rcx], 0x01                                    | 49 83 14 0c 01                            |
    | adc qword [r13 + 1 * rcx], 0x01                                    | 49 83 54 0d 00 01                         |
    | adc qword [r14 + 1 * rcx], 0x01                                    | 49 83 14 0e 01                            |
    | adc qword [r15 + 1 * rcx], 0x01                                    | 49 83 14 0f 01                            |
    | adc qword [rax + 1 * rax], 0x01                                    | 48 83 14 00 01                            |
    | adc qword [rax + 1 * rdx], 0x01                                    | 48 83 14 10 01                            |
    | adc qword [rax + 1 * rbx], 0x01                                    | 48 83 14 18 01                            |
    | adc qword [rax + 1 * rbp], 0x01                                    | 48 83 14 28 01                            |
    | adc qword [rax + 1 * rsi], 0x01                                    | 48 83 14 30 01                            |
    | adc qword [rax + 1 * rdi], 0x01                                    | 48 83 14 38 01                            |
    | adc qword [rax + 1 * r8], 0x01                                     | 4a 83 14 00 01                            |
    | adc qword [rax + 1 * r9], 0x01                                     | 4a 83 14 08 01                            |
    | adc qword [rax + 1 * r10], 0x01                                    | 4a 83 14 10 01                            |
    | adc qword [rax + 1 * r11], 0x01                                    | 4a 83 14 18 01                            |
    | adc qword [rax + 1 * r12], 0x01                                    | 4a 83 14 20 01                            |
    | adc qword [rax + 1 * r13], 0x01                                    | 4a 83 14 28 01                            |
    | adc qword [rax + 1 * r14], 0x01                                    | 4a 83 14 30 01                            |
    | adc qword [rax + 1 * r15], 0x01                                    | 4a 83 14 38 01                            |
    | adc qword [rax + 2 * rcx], 0x01                                    | 48 83 14 48 01                            |
    | adc qword [rax + 4 * rcx], 0x01                                    | 48 83 14 88 01                            |
    | adc qword [rax + 8 * rcx], 0x01                                    | 48 83 14 c8 01                            |
    | adc qword [r8 + 1 * r9], 0x01                                      | 4b 83 14 08 01                            |
    | adc qword [r8 + 2 * r9], 0x01                                      | 4b 83 14 48 01                            |
    | adc qword [r8 + 4 * r9], 0x01                                      | 4b 83 14 88 01                            |
    | adc qword [r8 + 8 * r9], 0x01                                      | 4b 83 14 c8 01                            |
    | adc qword [1 * rcx], 0x01                                          | 48 83 14 0d 00 00 00 00 01                |
    | adc qword [2 * rcx], 0x01                                          | 48 83 14 4d 00 00 00 00 01                |
    | adc qword [4 * rcx], 0x01                                          | 48 83 14 8d 00 00 00 00 01                |
    | adc qword [8 * rcx], 0x01                                          | 48 83 14 cd 00 00 00 00 01                |
    | adc qword [1 * r9], 0x01                                           | 4a 83 14 0d 00 00 00 00 01                |
    | adc qword [2 * r9], 0x01                                           | 4a 83 14 4d 00 00 00 00 01                |
    | adc qword [4 * r9], 0x01                                           | 4a 83 14 8d 00 00 00 00 01                |
    | adc qword [8 * r9], 0x01                                           | 4a 83 14 cd 00 00 00 00 01                |
    | adc qword [r13 + 8 * r12], 0x01                                    | 4b 83 54 e5 00 01                         |
    | adc qword [rsp + 4 * r15], 0x01                                    | 4a 83 14 bc 01                            |
    | adc qword [rax + 1 * rcx + 0x00], 0x01                             | 48 83 54 08 00 01                         |
    | adc qword [rax + 1 * rcx - 0x00], 0x01                             | 48 83 54 08 00 01                         |
    | adc qword [rax + 1 * rcx + 0x01], 0x01                             | 48 83 54 08 01 01                         |
    | adc qword [rax + 1 * rcx - 0x01], 0x01                             | 48 83 54 08 ff 01                         |
    | adc qword [rax + 1 * rcx + 0x00000001], 0x01                       | 48 83 94 08 01 00 00 00 01                |
    | adc qword [rax + 1 * rcx - 0x00000001], 0x01                       | 48 83 94 08 ff ff ff ff 01                |
    | adc qword [rax + 1 * rcx + 0x7f], 0x01                             | 48 83 54 08 7f 01                         |
    | adc qword [rax + 1 * rcx - 0x7f], 0x01                             | 48 83 54 08 81 01                         |
    | adc qword [rax + 1 * rcx + 0x80], 0x01                             | 48 83 94 08 80 00 00 00 01                |
    | adc qword [rax + 1 * rcx - 0x80], 0x01                             | 48 83 54 08 80 01                         |
    | adc qword [rax + 1 * rcx - 0x81], 0x01                             | 48 83 94 08 7f ff ff ff 01                |
    | adc qword [rax + 1 * rcx + 0xff], 0x01                             | 48 83 94 08 ff 00 00 00 01                |
    | adc qword [rax + 1 * rcx - 0xff], 0x01                             | 48 83 94 08 01 ff ff ff 01                |
    | adc qword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 48 83 94 08 ff ff ff 7f 01                |
    | adc qword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 48 83 94 08 01 00 00 80 01                |
    | adc qword [rax + 1 * rcx - 0x80000000], 0x01                       | 48 83 94 08 00 00 00 80 01                |
    | adc qword [r10 + 0x7f], 0x01                                       | 49 83 52 7f 01                            |
    | adc qword [r10 + 0x80], 0x01                                       | 49 83 92 80 00 00 00 01                   |
    | adc qword [r10 - 0x80], 0x01                                       | 49 83 52 80 01                            |
    | adc qword [r10 - 0x81], 0x01                                       | 49 83 92 7f ff ff ff 01                   |
    | .prev5: nop; nop; nop; nop; nop; adc qword [rel @prev5], 0x01      | 90 90 90 90 90 48 83 15 f3 ff ff ff 01    |
    | .prev1: nop; adc qword [rel @prev1], 0x01                          | 90 48 83 15 f7 ff ff ff 01                |
    | adc qword [rel @next1], 0x01; nop; .next1: nop                     | 48 83 15 01 00 00 00 01 90 90             |
    | adc qword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 48 83 15 05 00 00 00 01 90 90 90 90 90 90 |
    | adc qword [rax], 0x00                                              | 48 83 10 00                               |
    | adc qword [rax], 0x7f                                              | 48 83 10 7f                               |
    | adc qword [rax], 0x80                                              | 48 83 10 80                               |
    | adc qword [rax], 0xff                                              | 48 83 10 ff                               |
    | adc qword [rcx], 0x7f                                              | 48 83 11 7f                               |
    | adc qword [rdx], 0x80                                              | 48 83 12 80                               |
    | adc qword [rbx], 0xff                                              | 48 83 13 ff                               |
    | adc qword [rsp], 0x00                                              | 48 83 14 24 00                            |
    | adc qword [rsi], 0x7f                                              | 48 83 16 7f                               |
    | adc qword [rdi], 0x80                                              | 48 83 17 80                               |
    | adc qword [r8], 0xff                                               | 49 83 10 ff                               |
    | adc qword [r9], 0x00                                               | 49 83 11 00                               |
    | adc qword [r11], 0x7f                                              | 49 83 13 7f                               |
    | adc qword [r12], 0x80                                              | 49 83 14 24 80                            |
    | adc qword [r13], 0xff                                              | 49 83 55 00 ff                            |
    | adc qword [r14], 0x00                                              | 49 83 16 00                               |
    | adc qword [rax + 1 * rcx], 0x7f                                    | 48 83 14 08 7f                            |
    | adc qword [rcx + 1 * rcx], 0x80                                    | 48 83 14 09 80                            |
    | adc qword [rdx + 1 * rcx], 0xff                                    | 48 83 14 0a ff                            |
    | adc qword [rbx + 1 * rcx], 0x00                                    | 48 83 14 0b 00                            |
    | adc qword [rbp + 1 * rcx], 0x7f                                    | 48 83 54 0d 00 7f                         |
    | adc qword [rsi + 1 * rcx], 0x80                                    | 48 83 14 0e 80                            |
    | adc qword [rdi + 1 * rcx], 0xff                                    | 48 83 14 0f ff                            |
    | adc qword [r8 + 1 * rcx], 0x00                                     | 49 83 14 08 00                            |
    | adc qword [r10 + 1 * rcx], 0x7f                                    | 49 83 14 0a 7f                            |
    | adc qword [r11 + 1 * rcx], 0x80                                    | 49 83 14 0b 80                            |
    | adc qword [r12 + 1 * rcx], 0xff                                    | 49 83 14 0c ff                            |
    | adc qword [r13 + 1 * rcx], 0x00                                    | 49 83 54 0d 00 00                         |
    | adc qword [r15 + 1 * rcx], 0x7f                                    | 49 83 14 0f 7f                            |
    | adc qword [rax + 1 * rax], 0x80                                    | 48 83 14 00 80                            |
    | adc qword [rax + 1 * rdx], 0xff                                    | 48 83 14 10 ff                            |
    | adc qword [rax + 1 * rbx], 0x00                                    | 48 83 14 18 00                            |
    | adc qword [rax + 1 * rsi], 0x7f                                    | 48 83 14 30 7f                            |
    | adc qword [rax + 1 * rdi], 0x80                                    | 48 83 14 38 80                            |
    | adc qword [rax + 1 * r8], 0xff                                     | 4a 83 14 00 ff                            |
    | adc qword [rax + 1 * r9], 0x00                                     | 4a 83 14 08 00                            |
    | adc qword [rax + 1 * r11], 0x7f                                    | 4a 83 14 18 7f                            |
    | adc qword [rax + 1 * r12], 0x80                                    | 4a 83 14 20 80                            |
    | adc qword [rax + 1 * r13], 0xff                                    | 4a 83 14 28 ff                            |
    | adc qword [rax + 1 * r14], 0x00                                    | 4a 83 14 30 00                            |
    | adc qword [rax + 2 * rcx], 0x7f                                    | 48 83 14 48 7f                            |
    | adc qword [rax + 4 * rcx], 0x80                                    | 48 83 14 88 80                            |
    | adc qword [rax + 8 * rcx], 0xff                                    | 48 83 14 c8 ff                            |
    | adc qword [r8 + 1 * r9], 0x00                                      | 4b 83 14 08 00                            |
    | adc qword [r8 + 4 * r9], 0x7f                                      | 4b 83 14 88 7f                            |
    | adc qword [r8 + 8 * r9], 0x80                                      | 4b 83 14 c8 80                            |
    | adc qword [1 * rcx], 0xff                                          | 48 83 14 0d 00 00 00 00 ff                |
    | adc qword [2 * rcx], 0x00                                          | 48 83 14 4d 00 00 00 00 00                |
    | adc qword [8 * rcx], 0x7f                                          | 48 83 14 cd 00 00 00 00 7f                |
    | adc qword [1 * r9], 0x80                                           | 4a 83 14 0d 00 00 00 00 80                |
    | adc qword [2 * r9], 0xff                                           | 4a 83 14 4d 00 00 00 00 ff                |
    | adc qword [4 * r9], 0x00                                           | 4a 83 14 8d 00 00 00 00 00                |
    | adc qword [r13 + 8 * r12], 0x7f                                    | 4b 83 54 e5 00 7f                         |
    | adc qword [rsp + 4 * r15], 0x80                                    | 4a 83 14 bc 80                            |
    | adc qword [rax + 1 * rcx + 0x00], 0xff                             | 48 83 54 08 00 ff                         |
    | adc qword [rax + 1 * rcx - 0x00], 0x00                             | 48 83 54 08 00 00                         |
    | adc qword [rax + 1 * rcx - 0x01], 0x7f                             | 48 83 54 08 ff 7f                         |
    | adc qword [rax + 1 * rcx + 0x00000001], 0x80                       | 48 83 94 08 01 00 00 00 80                |
    | adc qword [rax + 1 * rcx - 0x00000001], 0xff                       | 48 83 94 08 ff ff ff ff ff                |
    | adc qword [rax + 1 * rcx + 0x7f], 0x00                             | 48 83 54 08 7f 00                         |
    | adc qword [rax + 1 * rcx + 0x80], 0x7f                             | 48 83 94 08 80 00 00 00 7f                |
    | adc qword [rax + 1 * rcx - 0x80], 0x80                             | 48 83 54 08 80 80                         |
    | adc qword [rax + 1 * rcx - 0x81], 0xff                             | 48 83 94 08 7f ff ff ff ff                |
    | adc qword [rax + 1 * rcx + 0xff], 0x00                             | 48 83 94 08 ff 00 00 00 00                |
    | adc qword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 48 83 94 08 ff ff ff 7f 7f                |
    | adc qword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 48 83 94 08 01 00 00 80 80                |
    | adc qword [rax + 1 * rcx - 0x80000000], 0xff                       | 48 83 94 08 00 00 00 80 ff                |
    | adc qword [r10 + 0x7f], 0x00                                       | 49 83 52 7f 00                            |
    | adc qword [r10 - 0x80], 0x7f                                       | 49 83 52 80 7f                            |
    | adc qword [r10 - 0x81], 0x80                                       | 49 83 92 7f ff ff ff 80                   |
    | .prev5: nop; nop; nop; nop; nop; adc qword [rel @prev5], 0xff      | 90 90 90 90 90 48 83 15 f3 ff ff ff ff    |
    | .prev1: nop; adc qword [rel @prev1], 0x00                          | 90 48 83 15 f7 ff ff ff 00                |
    | adc qword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 48 83 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | ----------------------------------------- |
"""


def can_encode_adc_addr64_imm8():
    encode(ADC_ADDR64_IMM8)


ADC_ADDR64_IMM32 = """
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
    | instruction                                                              | encoding                                           |
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
    | adc qword [rax], 0x00000001                                              | 48 81 10 01 00 00 00                               |
    | adc qword [rcx], 0x00000001                                              | 48 81 11 01 00 00 00                               |
    | adc qword [rdx], 0x00000001                                              | 48 81 12 01 00 00 00                               |
    | adc qword [rbx], 0x00000001                                              | 48 81 13 01 00 00 00                               |
    | adc qword [rsp], 0x00000001                                              | 48 81 14 24 01 00 00 00                            |
    | adc qword [rbp], 0x00000001                                              | 48 81 55 00 01 00 00 00                            |
    | adc qword [rsi], 0x00000001                                              | 48 81 16 01 00 00 00                               |
    | adc qword [rdi], 0x00000001                                              | 48 81 17 01 00 00 00                               |
    | adc qword [r8], 0x00000001                                               | 49 81 10 01 00 00 00                               |
    | adc qword [r9], 0x00000001                                               | 49 81 11 01 00 00 00                               |
    | adc qword [r10], 0x00000001                                              | 49 81 12 01 00 00 00                               |
    | adc qword [r11], 0x00000001                                              | 49 81 13 01 00 00 00                               |
    | adc qword [r12], 0x00000001                                              | 49 81 14 24 01 00 00 00                            |
    | adc qword [r13], 0x00000001                                              | 49 81 55 00 01 00 00 00                            |
    | adc qword [r14], 0x00000001                                              | 49 81 16 01 00 00 00                               |
    | adc qword [r15], 0x00000001                                              | 49 81 17 01 00 00 00                               |
    | adc qword [rax + 1 * rcx], 0x00000001                                    | 48 81 14 08 01 00 00 00                            |
    | adc qword [rcx + 1 * rcx], 0x00000001                                    | 48 81 14 09 01 00 00 00                            |
    | adc qword [rdx + 1 * rcx], 0x00000001                                    | 48 81 14 0a 01 00 00 00                            |
    | adc qword [rbx + 1 * rcx], 0x00000001                                    | 48 81 14 0b 01 00 00 00                            |
    | adc qword [rsp + 1 * rcx], 0x00000001                                    | 48 81 14 0c 01 00 00 00                            |
    | adc qword [rbp + 1 * rcx], 0x00000001                                    | 48 81 54 0d 00 01 00 00 00                         |
    | adc qword [rsi + 1 * rcx], 0x00000001                                    | 48 81 14 0e 01 00 00 00                            |
    | adc qword [rdi + 1 * rcx], 0x00000001                                    | 48 81 14 0f 01 00 00 00                            |
    | adc qword [r8 + 1 * rcx], 0x00000001                                     | 49 81 14 08 01 00 00 00                            |
    | adc qword [r9 + 1 * rcx], 0x00000001                                     | 49 81 14 09 01 00 00 00                            |
    | adc qword [r10 + 1 * rcx], 0x00000001                                    | 49 81 14 0a 01 00 00 00                            |
    | adc qword [r11 + 1 * rcx], 0x00000001                                    | 49 81 14 0b 01 00 00 00                            |
    | adc qword [r12 + 1 * rcx], 0x00000001                                    | 49 81 14 0c 01 00 00 00                            |
    | adc qword [r13 + 1 * rcx], 0x00000001                                    | 49 81 54 0d 00 01 00 00 00                         |
    | adc qword [r14 + 1 * rcx], 0x00000001                                    | 49 81 14 0e 01 00 00 00                            |
    | adc qword [r15 + 1 * rcx], 0x00000001                                    | 49 81 14 0f 01 00 00 00                            |
    | adc qword [rax + 1 * rax], 0x00000001                                    | 48 81 14 00 01 00 00 00                            |
    | adc qword [rax + 1 * rdx], 0x00000001                                    | 48 81 14 10 01 00 00 00                            |
    | adc qword [rax + 1 * rbx], 0x00000001                                    | 48 81 14 18 01 00 00 00                            |
    | adc qword [rax + 1 * rbp], 0x00000001                                    | 48 81 14 28 01 00 00 00                            |
    | adc qword [rax + 1 * rsi], 0x00000001                                    | 48 81 14 30 01 00 00 00                            |
    | adc qword [rax + 1 * rdi], 0x00000001                                    | 48 81 14 38 01 00 00 00                            |
    | adc qword [rax + 1 * r8], 0x00000001                                     | 4a 81 14 00 01 00 00 00                            |
    | adc qword [rax + 1 * r9], 0x00000001                                     | 4a 81 14 08 01 00 00 00                            |
    | adc qword [rax + 1 * r10], 0x00000001                                    | 4a 81 14 10 01 00 00 00                            |
    | adc qword [rax + 1 * r11], 0x00000001                                    | 4a 81 14 18 01 00 00 00                            |
    | adc qword [rax + 1 * r12], 0x00000001                                    | 4a 81 14 20 01 00 00 00                            |
    | adc qword [rax + 1 * r13], 0x00000001                                    | 4a 81 14 28 01 00 00 00                            |
    | adc qword [rax + 1 * r14], 0x00000001                                    | 4a 81 14 30 01 00 00 00                            |
    | adc qword [rax + 1 * r15], 0x00000001                                    | 4a 81 14 38 01 00 00 00                            |
    | adc qword [rax + 2 * rcx], 0x00000001                                    | 48 81 14 48 01 00 00 00                            |
    | adc qword [rax + 4 * rcx], 0x00000001                                    | 48 81 14 88 01 00 00 00                            |
    | adc qword [rax + 8 * rcx], 0x00000001                                    | 48 81 14 c8 01 00 00 00                            |
    | adc qword [r8 + 1 * r9], 0x00000001                                      | 4b 81 14 08 01 00 00 00                            |
    | adc qword [r8 + 2 * r9], 0x00000001                                      | 4b 81 14 48 01 00 00 00                            |
    | adc qword [r8 + 4 * r9], 0x00000001                                      | 4b 81 14 88 01 00 00 00                            |
    | adc qword [r8 + 8 * r9], 0x00000001                                      | 4b 81 14 c8 01 00 00 00                            |
    | adc qword [1 * rcx], 0x00000001                                          | 48 81 14 0d 00 00 00 00 01 00 00 00                |
    | adc qword [2 * rcx], 0x00000001                                          | 48 81 14 4d 00 00 00 00 01 00 00 00                |
    | adc qword [4 * rcx], 0x00000001                                          | 48 81 14 8d 00 00 00 00 01 00 00 00                |
    | adc qword [8 * rcx], 0x00000001                                          | 48 81 14 cd 00 00 00 00 01 00 00 00                |
    | adc qword [1 * r9], 0x00000001                                           | 4a 81 14 0d 00 00 00 00 01 00 00 00                |
    | adc qword [2 * r9], 0x00000001                                           | 4a 81 14 4d 00 00 00 00 01 00 00 00                |
    | adc qword [4 * r9], 0x00000001                                           | 4a 81 14 8d 00 00 00 00 01 00 00 00                |
    | adc qword [8 * r9], 0x00000001                                           | 4a 81 14 cd 00 00 00 00 01 00 00 00                |
    | adc qword [r13 + 8 * r12], 0x00000001                                    | 4b 81 54 e5 00 01 00 00 00                         |
    | adc qword [rsp + 4 * r15], 0x00000001                                    | 4a 81 14 bc 01 00 00 00                            |
    | adc qword [rax + 1 * rcx + 0x00], 0x00000001                             | 48 81 54 08 00 01 00 00 00                         |
    | adc qword [rax + 1 * rcx - 0x00], 0x00000001                             | 48 81 54 08 00 01 00 00 00                         |
    | adc qword [rax + 1 * rcx + 0x01], 0x00000001                             | 48 81 54 08 01 01 00 00 00                         |
    | adc qword [rax + 1 * rcx - 0x01], 0x00000001                             | 48 81 54 08 ff 01 00 00 00                         |
    | adc qword [rax + 1 * rcx + 0x00000001], 0x00000001                       | 48 81 94 08 01 00 00 00 01 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x00000001], 0x00000001                       | 48 81 94 08 ff ff ff ff 01 00 00 00                |
    | adc qword [rax + 1 * rcx + 0x7f], 0x00000001                             | 48 81 54 08 7f 01 00 00 00                         |
    | adc qword [rax + 1 * rcx - 0x7f], 0x00000001                             | 48 81 54 08 81 01 00 00 00                         |
    | adc qword [rax + 1 * rcx + 0x80], 0x00000001                             | 48 81 94 08 80 00 00 00 01 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x80], 0x00000001                             | 48 81 54 08 80 01 00 00 00                         |
    | adc qword [rax + 1 * rcx - 0x81], 0x00000001                             | 48 81 94 08 7f ff ff ff 01 00 00 00                |
    | adc qword [rax + 1 * rcx + 0xff], 0x00000001                             | 48 81 94 08 ff 00 00 00 01 00 00 00                |
    | adc qword [rax + 1 * rcx - 0xff], 0x00000001                             | 48 81 94 08 01 ff ff ff 01 00 00 00                |
    | adc qword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | 48 81 94 08 ff ff ff 7f 01 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | 48 81 94 08 01 00 00 80 01 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x80000000], 0x00000001                       | 48 81 94 08 00 00 00 80 01 00 00 00                |
    | adc qword [r10 + 0x7f], 0x00000001                                       | 49 81 52 7f 01 00 00 00                            |
    | adc qword [r10 + 0x80], 0x00000001                                       | 49 81 92 80 00 00 00 01 00 00 00                   |
    | adc qword [r10 - 0x80], 0x00000001                                       | 49 81 52 80 01 00 00 00                            |
    | adc qword [r10 - 0x81], 0x00000001                                       | 49 81 92 7f ff ff ff 01 00 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; adc qword [rel @prev5], 0x00000001      | 90 90 90 90 90 48 81 15 f0 ff ff ff 01 00 00 00    |
    | .prev1: nop; adc qword [rel @prev1], 0x00000001                          | 90 48 81 15 f4 ff ff ff 01 00 00 00                |
    | adc qword [rel @next1], 0x00000001; nop; .next1: nop                     | 48 81 15 01 00 00 00 01 00 00 00 90 90             |
    | adc qword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | 48 81 15 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | adc qword [rax], 0x00000000                                              | 48 81 10 00 00 00 00                               |
    | adc qword [rax], 0x0000007f                                              | 48 81 10 7f 00 00 00                               |
    | adc qword [rax], 0x00000080                                              | 48 81 10 80 00 00 00                               |
    | adc qword [rax], 0x000000ff                                              | 48 81 10 ff 00 00 00                               |
    | adc qword [rax], 0x00000100                                              | 48 81 10 00 01 00 00                               |
    | adc qword [rax], 0x00007fff                                              | 48 81 10 ff 7f 00 00                               |
    | adc qword [rax], 0x00008000                                              | 48 81 10 00 80 00 00                               |
    | adc qword [rax], 0x0000ffff                                              | 48 81 10 ff ff 00 00                               |
    | adc qword [rax], 0x00010000                                              | 48 81 10 00 00 01 00                               |
    | adc qword [rax], 0x7fffffff                                              | 48 81 10 ff ff ff 7f                               |
    | adc qword [rax], 0x80000000                                              | 48 81 10 00 00 00 80                               |
    | adc qword [rax], 0xffffffff                                              | 48 81 10 ff ff ff ff                               |
    | adc qword [rcx], 0x0000007f                                              | 48 81 11 7f 00 00 00                               |
    | adc qword [rdx], 0x00000080                                              | 48 81 12 80 00 00 00                               |
    | adc qword [rbx], 0x000000ff                                              | 48 81 13 ff 00 00 00                               |
    | adc qword [rsp], 0x00000100                                              | 48 81 14 24 00 01 00 00                            |
    | adc qword [rbp], 0x00007fff                                              | 48 81 55 00 ff 7f 00 00                            |
    | adc qword [rsi], 0x00008000                                              | 48 81 16 00 80 00 00                               |
    | adc qword [rdi], 0x0000ffff                                              | 48 81 17 ff ff 00 00                               |
    | adc qword [r8], 0x00010000                                               | 49 81 10 00 00 01 00                               |
    | adc qword [r9], 0x7fffffff                                               | 49 81 11 ff ff ff 7f                               |
    | adc qword [r10], 0x80000000                                              | 49 81 12 00 00 00 80                               |
    | adc qword [r11], 0xffffffff                                              | 49 81 13 ff ff ff ff                               |
    | adc qword [r12], 0x00000000                                              | 49 81 14 24 00 00 00 00                            |
    | adc qword [r14], 0x0000007f                                              | 49 81 16 7f 00 00 00                               |
    | adc qword [r15], 0x00000080                                              | 49 81 17 80 00 00 00                               |
    | adc qword [rax + 1 * rcx], 0x000000ff                                    | 48 81 14 08 ff 00 00 00                            |
    | adc qword [rcx + 1 * rcx], 0x00000100                                    | 48 81 14 09 00 01 00 00                            |
    | adc qword [rdx + 1 * rcx], 0x00007fff                                    | 48 81 14 0a ff 7f 00 00                            |
    | adc qword [rbx + 1 * rcx], 0x00008000                                    | 48 81 14 0b 00 80 00 00                            |
    | adc qword [rsp + 1 * rcx], 0x0000ffff                                    | 48 81 14 0c ff ff 00 00                            |
    | adc qword [rbp + 1 * rcx], 0x00010000                                    | 48 81 54 0d 00 00 00 01 00                         |
    | adc qword [rsi + 1 * rcx], 0x7fffffff                                    | 48 81 14 0e ff ff ff 7f                            |
    | adc qword [rdi + 1 * rcx], 0x80000000                                    | 48 81 14 0f 00 00 00 80                            |
    | adc qword [r8 + 1 * rcx], 0xffffffff                                     | 49 81 14 08 ff ff ff ff                            |
    | adc qword [r9 + 1 * rcx], 0x00000000                                     | 49 81 14 09 00 00 00 00                            |
    | adc qword [r11 + 1 * rcx], 0x0000007f                                    | 49 81 14 0b 7f 00 00 00                            |
    | adc qword [r12 + 1 * rcx], 0x00000080                                    | 49 81 14 0c 80 00 00 00                            |
    | adc qword [r13 + 1 * rcx], 0x000000ff                                    | 49 81 54 0d 00 ff 00 00 00                         |
    | adc qword [r14 + 1 * rcx], 0x00000100                                    | 49 81 14 0e 00 01 00 00                            |
    | adc qword [r15 + 1 * rcx], 0x00007fff                                    | 49 81 14 0f ff 7f 00 00                            |
    | adc qword [rax + 1 * rax], 0x00008000                                    | 48 81 14 00 00 80 00 00                            |
    | adc qword [rax + 1 * rdx], 0x0000ffff                                    | 48 81 14 10 ff ff 00 00                            |
    | adc qword [rax + 1 * rbx], 0x00010000                                    | 48 81 14 18 00 00 01 00                            |
    | adc qword [rax + 1 * rbp], 0x7fffffff                                    | 48 81 14 28 ff ff ff 7f                            |
    | adc qword [rax + 1 * rsi], 0x80000000                                    | 48 81 14 30 00 00 00 80                            |
    | adc qword [rax + 1 * rdi], 0xffffffff                                    | 48 81 14 38 ff ff ff ff                            |
    | adc qword [rax + 1 * r8], 0x00000000                                     | 4a 81 14 00 00 00 00 00                            |
    | adc qword [rax + 1 * r10], 0x0000007f                                    | 4a 81 14 10 7f 00 00 00                            |
    | adc qword [rax + 1 * r11], 0x00000080                                    | 4a 81 14 18 80 00 00 00                            |
    | adc qword [rax + 1 * r12], 0x000000ff                                    | 4a 81 14 20 ff 00 00 00                            |
    | adc qword [rax + 1 * r13], 0x00000100                                    | 4a 81 14 28 00 01 00 00                            |
    | adc qword [rax + 1 * r14], 0x00007fff                                    | 4a 81 14 30 ff 7f 00 00                            |
    | adc qword [rax + 1 * r15], 0x00008000                                    | 4a 81 14 38 00 80 00 00                            |
    | adc qword [rax + 2 * rcx], 0x0000ffff                                    | 48 81 14 48 ff ff 00 00                            |
    | adc qword [rax + 4 * rcx], 0x00010000                                    | 48 81 14 88 00 00 01 00                            |
    | adc qword [rax + 8 * rcx], 0x7fffffff                                    | 48 81 14 c8 ff ff ff 7f                            |
    | adc qword [r8 + 1 * r9], 0x80000000                                      | 4b 81 14 08 00 00 00 80                            |
    | adc qword [r8 + 2 * r9], 0xffffffff                                      | 4b 81 14 48 ff ff ff ff                            |
    | adc qword [r8 + 4 * r9], 0x00000000                                      | 4b 81 14 88 00 00 00 00                            |
    | adc qword [1 * rcx], 0x0000007f                                          | 48 81 14 0d 00 00 00 00 7f 00 00 00                |
    | adc qword [2 * rcx], 0x00000080                                          | 48 81 14 4d 00 00 00 00 80 00 00 00                |
    | adc qword [4 * rcx], 0x000000ff                                          | 48 81 14 8d 00 00 00 00 ff 00 00 00                |
    | adc qword [8 * rcx], 0x00000100                                          | 48 81 14 cd 00 00 00 00 00 01 00 00                |
    | adc qword [1 * r9], 0x00007fff                                           | 4a 81 14 0d 00 00 00 00 ff 7f 00 00                |
    | adc qword [2 * r9], 0x00008000                                           | 4a 81 14 4d 00 00 00 00 00 80 00 00                |
    | adc qword [4 * r9], 0x0000ffff                                           | 4a 81 14 8d 00 00 00 00 ff ff 00 00                |
    | adc qword [8 * r9], 0x00010000                                           | 4a 81 14 cd 00 00 00 00 00 00 01 00                |
    | adc qword [r13 + 8 * r12], 0x7fffffff                                    | 4b 81 54 e5 00 ff ff ff 7f                         |
    | adc qword [rsp + 4 * r15], 0x80000000                                    | 4a 81 14 bc 00 00 00 80                            |
    | adc qword [rax + 1 * rcx + 0x00], 0xffffffff                             | 48 81 54 08 00 ff ff ff ff                         |
    | adc qword [rax + 1 * rcx - 0x00], 0x00000000                             | 48 81 54 08 00 00 00 00 00                         |
    | adc qword [rax + 1 * rcx - 0x01], 0x0000007f                             | 48 81 54 08 ff 7f 00 00 00                         |
    | adc qword [rax + 1 * rcx + 0x00000001], 0x00000080                       | 48 81 94 08 01 00 00 00 80 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | 48 81 94 08 ff ff ff ff ff 00 00 00                |
    | adc qword [rax + 1 * rcx + 0x7f], 0x00000100                             | 48 81 54 08 7f 00 01 00 00                         |
    | adc qword [rax + 1 * rcx - 0x7f], 0x00007fff                             | 48 81 54 08 81 ff 7f 00 00                         |
    | adc qword [rax + 1 * rcx + 0x80], 0x00008000                             | 48 81 94 08 80 00 00 00 00 80 00 00                |
    | adc qword [rax + 1 * rcx - 0x80], 0x0000ffff                             | 48 81 54 08 80 ff ff 00 00                         |
    | adc qword [rax + 1 * rcx - 0x81], 0x00010000                             | 48 81 94 08 7f ff ff ff 00 00 01 00                |
    | adc qword [rax + 1 * rcx + 0xff], 0x7fffffff                             | 48 81 94 08 ff 00 00 00 ff ff ff 7f                |
    | adc qword [rax + 1 * rcx - 0xff], 0x80000000                             | 48 81 94 08 01 ff ff ff 00 00 00 80                |
    | adc qword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | 48 81 94 08 ff ff ff 7f ff ff ff ff                |
    | adc qword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | 48 81 94 08 01 00 00 80 00 00 00 00                |
    | adc qword [r10 + 0x7f], 0x0000007f                                       | 49 81 52 7f 7f 00 00 00                            |
    | adc qword [r10 + 0x80], 0x00000080                                       | 49 81 92 80 00 00 00 80 00 00 00                   |
    | adc qword [r10 - 0x80], 0x000000ff                                       | 49 81 52 80 ff 00 00 00                            |
    | adc qword [r10 - 0x81], 0x00000100                                       | 49 81 92 7f ff ff ff 00 01 00 00                   |
    | .prev5: nop; nop; nop; nop; nop; adc qword [rel @prev5], 0x00007fff      | 90 90 90 90 90 48 81 15 f0 ff ff ff ff 7f 00 00    |
    | .prev1: nop; adc qword [rel @prev1], 0x00008000                          | 90 48 81 15 f4 ff ff ff 00 80 00 00                |
    | adc qword [rel @next1], 0x0000ffff; nop; .next1: nop                     | 48 81 15 01 00 00 00 ff ff 00 00 90 90             |
    | adc qword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | 48 81 15 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------------------ | -------------------------------------------------- |
"""


def can_encode_adc_addr64_imm32():
    encode(ADC_ADDR64_IMM32)


ADC_ADDR64_REG64 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | adc qword [rax], rcx                                              | 48 11 08                               |
    | adc qword [rcx], rcx                                              | 48 11 09                               |
    | adc qword [rdx], rcx                                              | 48 11 0a                               |
    | adc qword [rbx], rcx                                              | 48 11 0b                               |
    | adc qword [rsp], rcx                                              | 48 11 0c 24                            |
    | adc qword [rbp], rcx                                              | 48 11 4d 00                            |
    | adc qword [rsi], rcx                                              | 48 11 0e                               |
    | adc qword [rdi], rcx                                              | 48 11 0f                               |
    | adc qword [r8], rcx                                               | 49 11 08                               |
    | adc qword [r9], rcx                                               | 49 11 09                               |
    | adc qword [r10], rcx                                              | 49 11 0a                               |
    | adc qword [r11], rcx                                              | 49 11 0b                               |
    | adc qword [r12], rcx                                              | 49 11 0c 24                            |
    | adc qword [r13], rcx                                              | 49 11 4d 00                            |
    | adc qword [r14], rcx                                              | 49 11 0e                               |
    | adc qword [r15], rcx                                              | 49 11 0f                               |
    | adc qword [rax + 1 * rcx], rcx                                    | 48 11 0c 08                            |
    | adc qword [rcx + 1 * rcx], rcx                                    | 48 11 0c 09                            |
    | adc qword [rdx + 1 * rcx], rcx                                    | 48 11 0c 0a                            |
    | adc qword [rbx + 1 * rcx], rcx                                    | 48 11 0c 0b                            |
    | adc qword [rsp + 1 * rcx], rcx                                    | 48 11 0c 0c                            |
    | adc qword [rbp + 1 * rcx], rcx                                    | 48 11 4c 0d 00                         |
    | adc qword [rsi + 1 * rcx], rcx                                    | 48 11 0c 0e                            |
    | adc qword [rdi + 1 * rcx], rcx                                    | 48 11 0c 0f                            |
    | adc qword [r8 + 1 * rcx], rcx                                     | 49 11 0c 08                            |
    | adc qword [r9 + 1 * rcx], rcx                                     | 49 11 0c 09                            |
    | adc qword [r10 + 1 * rcx], rcx                                    | 49 11 0c 0a                            |
    | adc qword [r11 + 1 * rcx], rcx                                    | 49 11 0c 0b                            |
    | adc qword [r12 + 1 * rcx], rcx                                    | 49 11 0c 0c                            |
    | adc qword [r13 + 1 * rcx], rcx                                    | 49 11 4c 0d 00                         |
    | adc qword [r14 + 1 * rcx], rcx                                    | 49 11 0c 0e                            |
    | adc qword [r15 + 1 * rcx], rcx                                    | 49 11 0c 0f                            |
    | adc qword [rax + 1 * rax], rcx                                    | 48 11 0c 00                            |
    | adc qword [rax + 1 * rdx], rcx                                    | 48 11 0c 10                            |
    | adc qword [rax + 1 * rbx], rcx                                    | 48 11 0c 18                            |
    | adc qword [rax + 1 * rbp], rcx                                    | 48 11 0c 28                            |
    | adc qword [rax + 1 * rsi], rcx                                    | 48 11 0c 30                            |
    | adc qword [rax + 1 * rdi], rcx                                    | 48 11 0c 38                            |
    | adc qword [rax + 1 * r8], rcx                                     | 4a 11 0c 00                            |
    | adc qword [rax + 1 * r9], rcx                                     | 4a 11 0c 08                            |
    | adc qword [rax + 1 * r10], rcx                                    | 4a 11 0c 10                            |
    | adc qword [rax + 1 * r11], rcx                                    | 4a 11 0c 18                            |
    | adc qword [rax + 1 * r12], rcx                                    | 4a 11 0c 20                            |
    | adc qword [rax + 1 * r13], rcx                                    | 4a 11 0c 28                            |
    | adc qword [rax + 1 * r14], rcx                                    | 4a 11 0c 30                            |
    | adc qword [rax + 1 * r15], rcx                                    | 4a 11 0c 38                            |
    | adc qword [rax + 2 * rcx], rcx                                    | 48 11 0c 48                            |
    | adc qword [rax + 4 * rcx], rcx                                    | 48 11 0c 88                            |
    | adc qword [rax + 8 * rcx], rcx                                    | 48 11 0c c8                            |
    | adc qword [r8 + 1 * r9], rcx                                      | 4b 11 0c 08                            |
    | adc qword [r8 + 2 * r9], rcx                                      | 4b 11 0c 48                            |
    | adc qword [r8 + 4 * r9], rcx                                      | 4b 11 0c 88                            |
    | adc qword [r8 + 8 * r9], rcx                                      | 4b 11 0c c8                            |
    | adc qword [1 * rcx], rcx                                          | 48 11 0c 0d 00 00 00 00                |
    | adc qword [2 * rcx], rcx                                          | 48 11 0c 4d 00 00 00 00                |
    | adc qword [4 * rcx], rcx                                          | 48 11 0c 8d 00 00 00 00                |
    | adc qword [8 * rcx], rcx                                          | 48 11 0c cd 00 00 00 00                |
    | adc qword [1 * r9], rcx                                           | 4a 11 0c 0d 00 00 00 00                |
    | adc qword [2 * r9], rcx                                           | 4a 11 0c 4d 00 00 00 00                |
    | adc qword [4 * r9], rcx                                           | 4a 11 0c 8d 00 00 00 00                |
    | adc qword [8 * r9], rcx                                           | 4a 11 0c cd 00 00 00 00                |
    | adc qword [r13 + 8 * r12], rcx                                    | 4b 11 4c e5 00                         |
    | adc qword [rsp + 4 * r15], rcx                                    | 4a 11 0c bc                            |
    | adc qword [rax + 1 * rcx + 0x00], rcx                             | 48 11 4c 08 00                         |
    | adc qword [rax + 1 * rcx - 0x00], rcx                             | 48 11 4c 08 00                         |
    | adc qword [rax + 1 * rcx + 0x01], rcx                             | 48 11 4c 08 01                         |
    | adc qword [rax + 1 * rcx - 0x01], rcx                             | 48 11 4c 08 ff                         |
    | adc qword [rax + 1 * rcx + 0x00000001], rcx                       | 48 11 8c 08 01 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x00000001], rcx                       | 48 11 8c 08 ff ff ff ff                |
    | adc qword [rax + 1 * rcx + 0x7f], rcx                             | 48 11 4c 08 7f                         |
    | adc qword [rax + 1 * rcx - 0x7f], rcx                             | 48 11 4c 08 81                         |
    | adc qword [rax + 1 * rcx + 0x80], rcx                             | 48 11 8c 08 80 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x80], rcx                             | 48 11 4c 08 80                         |
    | adc qword [rax + 1 * rcx - 0x81], rcx                             | 48 11 8c 08 7f ff ff ff                |
    | adc qword [rax + 1 * rcx + 0xff], rcx                             | 48 11 8c 08 ff 00 00 00                |
    | adc qword [rax + 1 * rcx - 0xff], rcx                             | 48 11 8c 08 01 ff ff ff                |
    | adc qword [rax + 1 * rcx + 0x7fffffff], rcx                       | 48 11 8c 08 ff ff ff 7f                |
    | adc qword [rax + 1 * rcx - 0x7fffffff], rcx                       | 48 11 8c 08 01 00 00 80                |
    | adc qword [rax + 1 * rcx - 0x80000000], rcx                       | 48 11 8c 08 00 00 00 80                |
    | adc qword [r10 + 0x7f], rcx                                       | 49 11 4a 7f                            |
    | adc qword [r10 + 0x80], rcx                                       | 49 11 8a 80 00 00 00                   |
    | adc qword [r10 - 0x80], rcx                                       | 49 11 4a 80                            |
    | adc qword [r10 - 0x81], rcx                                       | 49 11 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc qword [rel @prev5], rcx      | 90 90 90 90 90 48 11 0d f4 ff ff ff    |
    | .prev1: nop; adc qword [rel @prev1], rcx                          | 90 48 11 0d f8 ff ff ff                |
    | adc qword [rel @next1], rcx; nop; .next1: nop                     | 48 11 0d 01 00 00 00 90 90             |
    | adc qword [rel @next5], rcx; nop; nop; nop; nop; nop; .next5: nop | 48 11 0d 05 00 00 00 90 90 90 90 90 90 |
    | adc qword [rax], rax                                              | 48 11 00                               |
    | adc qword [rax], rdx                                              | 48 11 10                               |
    | adc qword [rax], rbx                                              | 48 11 18                               |
    | adc qword [rax], rsp                                              | 48 11 20                               |
    | adc qword [rax], rbp                                              | 48 11 28                               |
    | adc qword [rax], rsi                                              | 48 11 30                               |
    | adc qword [rax], rdi                                              | 48 11 38                               |
    | adc qword [rax], r8                                               | 4c 11 00                               |
    | adc qword [rax], r9                                               | 4c 11 08                               |
    | adc qword [rax], r10                                              | 4c 11 10                               |
    | adc qword [rax], r11                                              | 4c 11 18                               |
    | adc qword [rax], r12                                              | 4c 11 20                               |
    | adc qword [rax], r13                                              | 4c 11 28                               |
    | adc qword [rax], r14                                              | 4c 11 30                               |
    | adc qword [rax], r15                                              | 4c 11 38                               |
    | adc qword [rcx], rdx                                              | 48 11 11                               |
    | adc qword [rdx], rbx                                              | 48 11 1a                               |
    | adc qword [rbx], rsp                                              | 48 11 23                               |
    | adc qword [rsp], rbp                                              | 48 11 2c 24                            |
    | adc qword [rbp], rsi                                              | 48 11 75 00                            |
    | adc qword [rsi], rdi                                              | 48 11 3e                               |
    | adc qword [rdi], r8                                               | 4c 11 07                               |
    | adc qword [r8], r9                                                | 4d 11 08                               |
    | adc qword [r9], r10                                               | 4d 11 11                               |
    | adc qword [r10], r11                                              | 4d 11 1a                               |
    | adc qword [r11], r12                                              | 4d 11 23                               |
    | adc qword [r12], r13                                              | 4d 11 2c 24                            |
    | adc qword [r13], r14                                              | 4d 11 75 00                            |
    | adc qword [r14], r15                                              | 4d 11 3e                               |
    | adc qword [r15], rax                                              | 49 11 07                               |
    | adc qword [rcx + 1 * rcx], rdx                                    | 48 11 14 09                            |
    | adc qword [rdx + 1 * rcx], rbx                                    | 48 11 1c 0a                            |
    | adc qword [rbx + 1 * rcx], rsp                                    | 48 11 24 0b                            |
    | adc qword [rsp + 1 * rcx], rbp                                    | 48 11 2c 0c                            |
    | adc qword [rbp + 1 * rcx], rsi                                    | 48 11 74 0d 00                         |
    | adc qword [rsi + 1 * rcx], rdi                                    | 48 11 3c 0e                            |
    | adc qword [rdi + 1 * rcx], r8                                     | 4c 11 04 0f                            |
    | adc qword [r8 + 1 * rcx], r9                                      | 4d 11 0c 08                            |
    | adc qword [r9 + 1 * rcx], r10                                     | 4d 11 14 09                            |
    | adc qword [r10 + 1 * rcx], r11                                    | 4d 11 1c 0a                            |
    | adc qword [r11 + 1 * rcx], r12                                    | 4d 11 24 0b                            |
    | adc qword [r12 + 1 * rcx], r13                                    | 4d 11 2c 0c                            |
    | adc qword [r13 + 1 * rcx], r14                                    | 4d 11 74 0d 00                         |
    | adc qword [r14 + 1 * rcx], r15                                    | 4d 11 3c 0e                            |
    | adc qword [r15 + 1 * rcx], rax                                    | 49 11 04 0f                            |
    | adc qword [rax + 1 * rdx], rdx                                    | 48 11 14 10                            |
    | adc qword [rax + 1 * rbx], rbx                                    | 48 11 1c 18                            |
    | adc qword [rax + 1 * rbp], rsp                                    | 48 11 24 28                            |
    | adc qword [rax + 1 * rsi], rbp                                    | 48 11 2c 30                            |
    | adc qword [rax + 1 * rdi], rsi                                    | 48 11 34 38                            |
    | adc qword [rax + 1 * r8], rdi                                     | 4a 11 3c 00                            |
    | adc qword [rax + 1 * r9], r8                                      | 4e 11 04 08                            |
    | adc qword [rax + 1 * r10], r9                                     | 4e 11 0c 10                            |
    | adc qword [rax + 1 * r11], r10                                    | 4e 11 14 18                            |
    | adc qword [rax + 1 * r12], r11                                    | 4e 11 1c 20                            |
    | adc qword [rax + 1 * r13], r12                                    | 4e 11 24 28                            |
    | adc qword [rax + 1 * r14], r13                                    | 4e 11 2c 30                            |
    | adc qword [rax + 1 * r15], r14                                    | 4e 11 34 38                            |
    | adc qword [rax + 2 * rcx], r15                                    | 4c 11 3c 48                            |
    | adc qword [rax + 4 * rcx], rax                                    | 48 11 04 88                            |
    | adc qword [r8 + 1 * r9], rdx                                      | 4b 11 14 08                            |
    | adc qword [r8 + 2 * r9], rbx                                      | 4b 11 1c 48                            |
    | adc qword [r8 + 4 * r9], rsp                                      | 4b 11 24 88                            |
    | adc qword [r8 + 8 * r9], rbp                                      | 4b 11 2c c8                            |
    | adc qword [1 * rcx], rsi                                          | 48 11 34 0d 00 00 00 00                |
    | adc qword [2 * rcx], rdi                                          | 48 11 3c 4d 00 00 00 00                |
    | adc qword [4 * rcx], r8                                           | 4c 11 04 8d 00 00 00 00                |
    | adc qword [8 * rcx], r9                                           | 4c 11 0c cd 00 00 00 00                |
    | adc qword [1 * r9], r10                                           | 4e 11 14 0d 00 00 00 00                |
    | adc qword [2 * r9], r11                                           | 4e 11 1c 4d 00 00 00 00                |
    | adc qword [4 * r9], r12                                           | 4e 11 24 8d 00 00 00 00                |
    | adc qword [8 * r9], r13                                           | 4e 11 2c cd 00 00 00 00                |
    | adc qword [r13 + 8 * r12], r14                                    | 4f 11 74 e5 00                         |
    | adc qword [rsp + 4 * r15], r15                                    | 4e 11 3c bc                            |
    | adc qword [rax + 1 * rcx + 0x00], rax                             | 48 11 44 08 00                         |
    | adc qword [rax + 1 * rcx + 0x01], rdx                             | 48 11 54 08 01                         |
    | adc qword [rax + 1 * rcx - 0x01], rbx                             | 48 11 5c 08 ff                         |
    | adc qword [rax + 1 * rcx + 0x00000001], rsp                       | 48 11 a4 08 01 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x00000001], rbp                       | 48 11 ac 08 ff ff ff ff                |
    | adc qword [rax + 1 * rcx + 0x7f], rsi                             | 48 11 74 08 7f                         |
    | adc qword [rax + 1 * rcx - 0x7f], rdi                             | 48 11 7c 08 81                         |
    | adc qword [rax + 1 * rcx + 0x80], r8                              | 4c 11 84 08 80 00 00 00                |
    | adc qword [rax + 1 * rcx - 0x80], r9                              | 4c 11 4c 08 80                         |
    | adc qword [rax + 1 * rcx - 0x81], r10                             | 4c 11 94 08 7f ff ff ff                |
    | adc qword [rax + 1 * rcx + 0xff], r11                             | 4c 11 9c 08 ff 00 00 00                |
    | adc qword [rax + 1 * rcx - 0xff], r12                             | 4c 11 a4 08 01 ff ff ff                |
    | adc qword [rax + 1 * rcx + 0x7fffffff], r13                       | 4c 11 ac 08 ff ff ff 7f                |
    | adc qword [rax + 1 * rcx - 0x7fffffff], r14                       | 4c 11 b4 08 01 00 00 80                |
    | adc qword [rax + 1 * rcx - 0x80000000], r15                       | 4c 11 bc 08 00 00 00 80                |
    | adc qword [r10 + 0x7f], rax                                       | 49 11 42 7f                            |
    | adc qword [r10 - 0x80], rdx                                       | 49 11 52 80                            |
    | adc qword [r10 - 0x81], rbx                                       | 49 11 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc qword [rel @prev5], rsp      | 90 90 90 90 90 48 11 25 f4 ff ff ff    |
    | .prev1: nop; adc qword [rel @prev1], rbp                          | 90 48 11 2d f8 ff ff ff                |
    | adc qword [rel @next1], rsi; nop; .next1: nop                     | 48 11 35 01 00 00 00 90 90             |
    | adc qword [rel @next5], rdi; nop; nop; nop; nop; nop; .next5: nop | 48 11 3d 05 00 00 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_adc_addr64_reg64():
    encode(ADC_ADDR64_REG64)


ADC_ADDR32_IMM8 = """
    | ------------------------------------------------------------------ | -------------------------------------- |
    | instruction                                                        | encoding                               |
    | ------------------------------------------------------------------ | -------------------------------------- |
    | adc dword [rax], 0x01                                              | 83 10 01                               |
    | adc dword [rcx], 0x01                                              | 83 11 01                               |
    | adc dword [rdx], 0x01                                              | 83 12 01                               |
    | adc dword [rbx], 0x01                                              | 83 13 01                               |
    | adc dword [rsp], 0x01                                              | 83 14 24 01                            |
    | adc dword [rbp], 0x01                                              | 83 55 00 01                            |
    | adc dword [rsi], 0x01                                              | 83 16 01                               |
    | adc dword [rdi], 0x01                                              | 83 17 01                               |
    | adc dword [r8], 0x01                                               | 41 83 10 01                            |
    | adc dword [r9], 0x01                                               | 41 83 11 01                            |
    | adc dword [r10], 0x01                                              | 41 83 12 01                            |
    | adc dword [r11], 0x01                                              | 41 83 13 01                            |
    | adc dword [r12], 0x01                                              | 41 83 14 24 01                         |
    | adc dword [r13], 0x01                                              | 41 83 55 00 01                         |
    | adc dword [r14], 0x01                                              | 41 83 16 01                            |
    | adc dword [r15], 0x01                                              | 41 83 17 01                            |
    | adc dword [rax + 1 * rcx], 0x01                                    | 83 14 08 01                            |
    | adc dword [rcx + 1 * rcx], 0x01                                    | 83 14 09 01                            |
    | adc dword [rdx + 1 * rcx], 0x01                                    | 83 14 0a 01                            |
    | adc dword [rbx + 1 * rcx], 0x01                                    | 83 14 0b 01                            |
    | adc dword [rsp + 1 * rcx], 0x01                                    | 83 14 0c 01                            |
    | adc dword [rbp + 1 * rcx], 0x01                                    | 83 54 0d 00 01                         |
    | adc dword [rsi + 1 * rcx], 0x01                                    | 83 14 0e 01                            |
    | adc dword [rdi + 1 * rcx], 0x01                                    | 83 14 0f 01                            |
    | adc dword [r8 + 1 * rcx], 0x01                                     | 41 83 14 08 01                         |
    | adc dword [r9 + 1 * rcx], 0x01                                     | 41 83 14 09 01                         |
    | adc dword [r10 + 1 * rcx], 0x01                                    | 41 83 14 0a 01                         |
    | adc dword [r11 + 1 * rcx], 0x01                                    | 41 83 14 0b 01                         |
    | adc dword [r12 + 1 * rcx], 0x01                                    | 41 83 14 0c 01                         |
    | adc dword [r13 + 1 * rcx], 0x01                                    | 41 83 54 0d 00 01                      |
    | adc dword [r14 + 1 * rcx], 0x01                                    | 41 83 14 0e 01                         |
    | adc dword [r15 + 1 * rcx], 0x01                                    | 41 83 14 0f 01                         |
    | adc dword [rax + 1 * rax], 0x01                                    | 83 14 00 01                            |
    | adc dword [rax + 1 * rdx], 0x01                                    | 83 14 10 01                            |
    | adc dword [rax + 1 * rbx], 0x01                                    | 83 14 18 01                            |
    | adc dword [rax + 1 * rbp], 0x01                                    | 83 14 28 01                            |
    | adc dword [rax + 1 * rsi], 0x01                                    | 83 14 30 01                            |
    | adc dword [rax + 1 * rdi], 0x01                                    | 83 14 38 01                            |
    | adc dword [rax + 1 * r8], 0x01                                     | 42 83 14 00 01                         |
    | adc dword [rax + 1 * r9], 0x01                                     | 42 83 14 08 01                         |
    | adc dword [rax + 1 * r10], 0x01                                    | 42 83 14 10 01                         |
    | adc dword [rax + 1 * r11], 0x01                                    | 42 83 14 18 01                         |
    | adc dword [rax + 1 * r12], 0x01                                    | 42 83 14 20 01                         |
    | adc dword [rax + 1 * r13], 0x01                                    | 42 83 14 28 01                         |
    | adc dword [rax + 1 * r14], 0x01                                    | 42 83 14 30 01                         |
    | adc dword [rax + 1 * r15], 0x01                                    | 42 83 14 38 01                         |
    | adc dword [rax + 2 * rcx], 0x01                                    | 83 14 48 01                            |
    | adc dword [rax + 4 * rcx], 0x01                                    | 83 14 88 01                            |
    | adc dword [rax + 8 * rcx], 0x01                                    | 83 14 c8 01                            |
    | adc dword [r8 + 1 * r9], 0x01                                      | 43 83 14 08 01                         |
    | adc dword [r8 + 2 * r9], 0x01                                      | 43 83 14 48 01                         |
    | adc dword [r8 + 4 * r9], 0x01                                      | 43 83 14 88 01                         |
    | adc dword [r8 + 8 * r9], 0x01                                      | 43 83 14 c8 01                         |
    | adc dword [1 * rcx], 0x01                                          | 83 14 0d 00 00 00 00 01                |
    | adc dword [2 * rcx], 0x01                                          | 83 14 4d 00 00 00 00 01                |
    | adc dword [4 * rcx], 0x01                                          | 83 14 8d 00 00 00 00 01                |
    | adc dword [8 * rcx], 0x01                                          | 83 14 cd 00 00 00 00 01                |
    | adc dword [1 * r9], 0x01                                           | 42 83 14 0d 00 00 00 00 01             |
    | adc dword [2 * r9], 0x01                                           | 42 83 14 4d 00 00 00 00 01             |
    | adc dword [4 * r9], 0x01                                           | 42 83 14 8d 00 00 00 00 01             |
    | adc dword [8 * r9], 0x01                                           | 42 83 14 cd 00 00 00 00 01             |
    | adc dword [r13 + 8 * r12], 0x01                                    | 43 83 54 e5 00 01                      |
    | adc dword [rsp + 4 * r15], 0x01                                    | 42 83 14 bc 01                         |
    | adc dword [rax + 1 * rcx + 0x00], 0x01                             | 83 54 08 00 01                         |
    | adc dword [rax + 1 * rcx - 0x00], 0x01                             | 83 54 08 00 01                         |
    | adc dword [rax + 1 * rcx + 0x01], 0x01                             | 83 54 08 01 01                         |
    | adc dword [rax + 1 * rcx - 0x01], 0x01                             | 83 54 08 ff 01                         |
    | adc dword [rax + 1 * rcx + 0x00000001], 0x01                       | 83 94 08 01 00 00 00 01                |
    | adc dword [rax + 1 * rcx - 0x00000001], 0x01                       | 83 94 08 ff ff ff ff 01                |
    | adc dword [rax + 1 * rcx + 0x7f], 0x01                             | 83 54 08 7f 01                         |
    | adc dword [rax + 1 * rcx - 0x7f], 0x01                             | 83 54 08 81 01                         |
    | adc dword [rax + 1 * rcx + 0x80], 0x01                             | 83 94 08 80 00 00 00 01                |
    | adc dword [rax + 1 * rcx - 0x80], 0x01                             | 83 54 08 80 01                         |
    | adc dword [rax + 1 * rcx - 0x81], 0x01                             | 83 94 08 7f ff ff ff 01                |
    | adc dword [rax + 1 * rcx + 0xff], 0x01                             | 83 94 08 ff 00 00 00 01                |
    | adc dword [rax + 1 * rcx - 0xff], 0x01                             | 83 94 08 01 ff ff ff 01                |
    | adc dword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 83 94 08 ff ff ff 7f 01                |
    | adc dword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 83 94 08 01 00 00 80 01                |
    | adc dword [rax + 1 * rcx - 0x80000000], 0x01                       | 83 94 08 00 00 00 80 01                |
    | adc dword [r10 + 0x7f], 0x01                                       | 41 83 52 7f 01                         |
    | adc dword [r10 + 0x80], 0x01                                       | 41 83 92 80 00 00 00 01                |
    | adc dword [r10 - 0x80], 0x01                                       | 41 83 52 80 01                         |
    | adc dword [r10 - 0x81], 0x01                                       | 41 83 92 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; adc dword [rel @prev5], 0x01      | 90 90 90 90 90 83 15 f4 ff ff ff 01    |
    | .prev1: nop; adc dword [rel @prev1], 0x01                          | 90 83 15 f8 ff ff ff 01                |
    | adc dword [rel @next1], 0x01; nop; .next1: nop                     | 83 15 01 00 00 00 01 90 90             |
    | adc dword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 83 15 05 00 00 00 01 90 90 90 90 90 90 |
    | adc dword [rax], 0x00                                              | 83 10 00                               |
    | adc dword [rax], 0x7f                                              | 83 10 7f                               |
    | adc dword [rax], 0x80                                              | 83 10 80                               |
    | adc dword [rax], 0xff                                              | 83 10 ff                               |
    | adc dword [rcx], 0x7f                                              | 83 11 7f                               |
    | adc dword [rdx], 0x80                                              | 83 12 80                               |
    | adc dword [rbx], 0xff                                              | 83 13 ff                               |
    | adc dword [rsp], 0x00                                              | 83 14 24 00                            |
    | adc dword [rsi], 0x7f                                              | 83 16 7f                               |
    | adc dword [rdi], 0x80                                              | 83 17 80                               |
    | adc dword [r8], 0xff                                               | 41 83 10 ff                            |
    | adc dword [r9], 0x00                                               | 41 83 11 00                            |
    | adc dword [r11], 0x7f                                              | 41 83 13 7f                            |
    | adc dword [r12], 0x80                                              | 41 83 14 24 80                         |
    | adc dword [r13], 0xff                                              | 41 83 55 00 ff                         |
    | adc dword [r14], 0x00                                              | 41 83 16 00                            |
    | adc dword [rax + 1 * rcx], 0x7f                                    | 83 14 08 7f                            |
    | adc dword [rcx + 1 * rcx], 0x80                                    | 83 14 09 80                            |
    | adc dword [rdx + 1 * rcx], 0xff                                    | 83 14 0a ff                            |
    | adc dword [rbx + 1 * rcx], 0x00                                    | 83 14 0b 00                            |
    | adc dword [rbp + 1 * rcx], 0x7f                                    | 83 54 0d 00 7f                         |
    | adc dword [rsi + 1 * rcx], 0x80                                    | 83 14 0e 80                            |
    | adc dword [rdi + 1 * rcx], 0xff                                    | 83 14 0f ff                            |
    | adc dword [r8 + 1 * rcx], 0x00                                     | 41 83 14 08 00                         |
    | adc dword [r10 + 1 * rcx], 0x7f                                    | 41 83 14 0a 7f                         |
    | adc dword [r11 + 1 * rcx], 0x80                                    | 41 83 14 0b 80                         |
    | adc dword [r12 + 1 * rcx], 0xff                                    | 41 83 14 0c ff                         |
    | adc dword [r13 + 1 * rcx], 0x00                                    | 41 83 54 0d 00 00                      |
    | adc dword [r15 + 1 * rcx], 0x7f                                    | 41 83 14 0f 7f                         |
    | adc dword [rax + 1 * rax], 0x80                                    | 83 14 00 80                            |
    | adc dword [rax + 1 * rdx], 0xff                                    | 83 14 10 ff                            |
    | adc dword [rax + 1 * rbx], 0x00                                    | 83 14 18 00                            |
    | adc dword [rax + 1 * rsi], 0x7f                                    | 83 14 30 7f                            |
    | adc dword [rax + 1 * rdi], 0x80                                    | 83 14 38 80                            |
    | adc dword [rax + 1 * r8], 0xff                                     | 42 83 14 00 ff                         |
    | adc dword [rax + 1 * r9], 0x00                                     | 42 83 14 08 00                         |
    | adc dword [rax + 1 * r11], 0x7f                                    | 42 83 14 18 7f                         |
    | adc dword [rax + 1 * r12], 0x80                                    | 42 83 14 20 80                         |
    | adc dword [rax + 1 * r13], 0xff                                    | 42 83 14 28 ff                         |
    | adc dword [rax + 1 * r14], 0x00                                    | 42 83 14 30 00                         |
    | adc dword [rax + 2 * rcx], 0x7f                                    | 83 14 48 7f                            |
    | adc dword [rax + 4 * rcx], 0x80                                    | 83 14 88 80                            |
    | adc dword [rax + 8 * rcx], 0xff                                    | 83 14 c8 ff                            |
    | adc dword [r8 + 1 * r9], 0x00                                      | 43 83 14 08 00                         |
    | adc dword [r8 + 4 * r9], 0x7f                                      | 43 83 14 88 7f                         |
    | adc dword [r8 + 8 * r9], 0x80                                      | 43 83 14 c8 80                         |
    | adc dword [1 * rcx], 0xff                                          | 83 14 0d 00 00 00 00 ff                |
    | adc dword [2 * rcx], 0x00                                          | 83 14 4d 00 00 00 00 00                |
    | adc dword [8 * rcx], 0x7f                                          | 83 14 cd 00 00 00 00 7f                |
    | adc dword [1 * r9], 0x80                                           | 42 83 14 0d 00 00 00 00 80             |
    | adc dword [2 * r9], 0xff                                           | 42 83 14 4d 00 00 00 00 ff             |
    | adc dword [4 * r9], 0x00                                           | 42 83 14 8d 00 00 00 00 00             |
    | adc dword [r13 + 8 * r12], 0x7f                                    | 43 83 54 e5 00 7f                      |
    | adc dword [rsp + 4 * r15], 0x80                                    | 42 83 14 bc 80                         |
    | adc dword [rax + 1 * rcx + 0x00], 0xff                             | 83 54 08 00 ff                         |
    | adc dword [rax + 1 * rcx - 0x00], 0x00                             | 83 54 08 00 00                         |
    | adc dword [rax + 1 * rcx - 0x01], 0x7f                             | 83 54 08 ff 7f                         |
    | adc dword [rax + 1 * rcx + 0x00000001], 0x80                       | 83 94 08 01 00 00 00 80                |
    | adc dword [rax + 1 * rcx - 0x00000001], 0xff                       | 83 94 08 ff ff ff ff ff                |
    | adc dword [rax + 1 * rcx + 0x7f], 0x00                             | 83 54 08 7f 00                         |
    | adc dword [rax + 1 * rcx + 0x80], 0x7f                             | 83 94 08 80 00 00 00 7f                |
    | adc dword [rax + 1 * rcx - 0x80], 0x80                             | 83 54 08 80 80                         |
    | adc dword [rax + 1 * rcx - 0x81], 0xff                             | 83 94 08 7f ff ff ff ff                |
    | adc dword [rax + 1 * rcx + 0xff], 0x00                             | 83 94 08 ff 00 00 00 00                |
    | adc dword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 83 94 08 ff ff ff 7f 7f                |
    | adc dword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 83 94 08 01 00 00 80 80                |
    | adc dword [rax + 1 * rcx - 0x80000000], 0xff                       | 83 94 08 00 00 00 80 ff                |
    | adc dword [r10 + 0x7f], 0x00                                       | 41 83 52 7f 00                         |
    | adc dword [r10 - 0x80], 0x7f                                       | 41 83 52 80 7f                         |
    | adc dword [r10 - 0x81], 0x80                                       | 41 83 92 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; adc dword [rel @prev5], 0xff      | 90 90 90 90 90 83 15 f4 ff ff ff ff    |
    | .prev1: nop; adc dword [rel @prev1], 0x00                          | 90 83 15 f8 ff ff ff 00                |
    | adc dword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 83 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | -------------------------------------- |
"""


def can_encode_adc_addr32_imm8():
    encode(ADC_ADDR32_IMM8)


ADC_ADDR32_IMM32 = """
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
    | instruction                                                              | encoding                                        |
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
    | adc dword [rax], 0x00000001                                              | 81 10 01 00 00 00                               |
    | adc dword [rcx], 0x00000001                                              | 81 11 01 00 00 00                               |
    | adc dword [rdx], 0x00000001                                              | 81 12 01 00 00 00                               |
    | adc dword [rbx], 0x00000001                                              | 81 13 01 00 00 00                               |
    | adc dword [rsp], 0x00000001                                              | 81 14 24 01 00 00 00                            |
    | adc dword [rbp], 0x00000001                                              | 81 55 00 01 00 00 00                            |
    | adc dword [rsi], 0x00000001                                              | 81 16 01 00 00 00                               |
    | adc dword [rdi], 0x00000001                                              | 81 17 01 00 00 00                               |
    | adc dword [r8], 0x00000001                                               | 41 81 10 01 00 00 00                            |
    | adc dword [r9], 0x00000001                                               | 41 81 11 01 00 00 00                            |
    | adc dword [r10], 0x00000001                                              | 41 81 12 01 00 00 00                            |
    | adc dword [r11], 0x00000001                                              | 41 81 13 01 00 00 00                            |
    | adc dword [r12], 0x00000001                                              | 41 81 14 24 01 00 00 00                         |
    | adc dword [r13], 0x00000001                                              | 41 81 55 00 01 00 00 00                         |
    | adc dword [r14], 0x00000001                                              | 41 81 16 01 00 00 00                            |
    | adc dword [r15], 0x00000001                                              | 41 81 17 01 00 00 00                            |
    | adc dword [rax + 1 * rcx], 0x00000001                                    | 81 14 08 01 00 00 00                            |
    | adc dword [rcx + 1 * rcx], 0x00000001                                    | 81 14 09 01 00 00 00                            |
    | adc dword [rdx + 1 * rcx], 0x00000001                                    | 81 14 0a 01 00 00 00                            |
    | adc dword [rbx + 1 * rcx], 0x00000001                                    | 81 14 0b 01 00 00 00                            |
    | adc dword [rsp + 1 * rcx], 0x00000001                                    | 81 14 0c 01 00 00 00                            |
    | adc dword [rbp + 1 * rcx], 0x00000001                                    | 81 54 0d 00 01 00 00 00                         |
    | adc dword [rsi + 1 * rcx], 0x00000001                                    | 81 14 0e 01 00 00 00                            |
    | adc dword [rdi + 1 * rcx], 0x00000001                                    | 81 14 0f 01 00 00 00                            |
    | adc dword [r8 + 1 * rcx], 0x00000001                                     | 41 81 14 08 01 00 00 00                         |
    | adc dword [r9 + 1 * rcx], 0x00000001                                     | 41 81 14 09 01 00 00 00                         |
    | adc dword [r10 + 1 * rcx], 0x00000001                                    | 41 81 14 0a 01 00 00 00                         |
    | adc dword [r11 + 1 * rcx], 0x00000001                                    | 41 81 14 0b 01 00 00 00                         |
    | adc dword [r12 + 1 * rcx], 0x00000001                                    | 41 81 14 0c 01 00 00 00                         |
    | adc dword [r13 + 1 * rcx], 0x00000001                                    | 41 81 54 0d 00 01 00 00 00                      |
    | adc dword [r14 + 1 * rcx], 0x00000001                                    | 41 81 14 0e 01 00 00 00                         |
    | adc dword [r15 + 1 * rcx], 0x00000001                                    | 41 81 14 0f 01 00 00 00                         |
    | adc dword [rax + 1 * rax], 0x00000001                                    | 81 14 00 01 00 00 00                            |
    | adc dword [rax + 1 * rdx], 0x00000001                                    | 81 14 10 01 00 00 00                            |
    | adc dword [rax + 1 * rbx], 0x00000001                                    | 81 14 18 01 00 00 00                            |
    | adc dword [rax + 1 * rbp], 0x00000001                                    | 81 14 28 01 00 00 00                            |
    | adc dword [rax + 1 * rsi], 0x00000001                                    | 81 14 30 01 00 00 00                            |
    | adc dword [rax + 1 * rdi], 0x00000001                                    | 81 14 38 01 00 00 00                            |
    | adc dword [rax + 1 * r8], 0x00000001                                     | 42 81 14 00 01 00 00 00                         |
    | adc dword [rax + 1 * r9], 0x00000001                                     | 42 81 14 08 01 00 00 00                         |
    | adc dword [rax + 1 * r10], 0x00000001                                    | 42 81 14 10 01 00 00 00                         |
    | adc dword [rax + 1 * r11], 0x00000001                                    | 42 81 14 18 01 00 00 00                         |
    | adc dword [rax + 1 * r12], 0x00000001                                    | 42 81 14 20 01 00 00 00                         |
    | adc dword [rax + 1 * r13], 0x00000001                                    | 42 81 14 28 01 00 00 00                         |
    | adc dword [rax + 1 * r14], 0x00000001                                    | 42 81 14 30 01 00 00 00                         |
    | adc dword [rax + 1 * r15], 0x00000001                                    | 42 81 14 38 01 00 00 00                         |
    | adc dword [rax + 2 * rcx], 0x00000001                                    | 81 14 48 01 00 00 00                            |
    | adc dword [rax + 4 * rcx], 0x00000001                                    | 81 14 88 01 00 00 00                            |
    | adc dword [rax + 8 * rcx], 0x00000001                                    | 81 14 c8 01 00 00 00                            |
    | adc dword [r8 + 1 * r9], 0x00000001                                      | 43 81 14 08 01 00 00 00                         |
    | adc dword [r8 + 2 * r9], 0x00000001                                      | 43 81 14 48 01 00 00 00                         |
    | adc dword [r8 + 4 * r9], 0x00000001                                      | 43 81 14 88 01 00 00 00                         |
    | adc dword [r8 + 8 * r9], 0x00000001                                      | 43 81 14 c8 01 00 00 00                         |
    | adc dword [1 * rcx], 0x00000001                                          | 81 14 0d 00 00 00 00 01 00 00 00                |
    | adc dword [2 * rcx], 0x00000001                                          | 81 14 4d 00 00 00 00 01 00 00 00                |
    | adc dword [4 * rcx], 0x00000001                                          | 81 14 8d 00 00 00 00 01 00 00 00                |
    | adc dword [8 * rcx], 0x00000001                                          | 81 14 cd 00 00 00 00 01 00 00 00                |
    | adc dword [1 * r9], 0x00000001                                           | 42 81 14 0d 00 00 00 00 01 00 00 00             |
    | adc dword [2 * r9], 0x00000001                                           | 42 81 14 4d 00 00 00 00 01 00 00 00             |
    | adc dword [4 * r9], 0x00000001                                           | 42 81 14 8d 00 00 00 00 01 00 00 00             |
    | adc dword [8 * r9], 0x00000001                                           | 42 81 14 cd 00 00 00 00 01 00 00 00             |
    | adc dword [r13 + 8 * r12], 0x00000001                                    | 43 81 54 e5 00 01 00 00 00                      |
    | adc dword [rsp + 4 * r15], 0x00000001                                    | 42 81 14 bc 01 00 00 00                         |
    | adc dword [rax + 1 * rcx + 0x00], 0x00000001                             | 81 54 08 00 01 00 00 00                         |
    | adc dword [rax + 1 * rcx - 0x00], 0x00000001                             | 81 54 08 00 01 00 00 00                         |
    | adc dword [rax + 1 * rcx + 0x01], 0x00000001                             | 81 54 08 01 01 00 00 00                         |
    | adc dword [rax + 1 * rcx - 0x01], 0x00000001                             | 81 54 08 ff 01 00 00 00                         |
    | adc dword [rax + 1 * rcx + 0x00000001], 0x00000001                       | 81 94 08 01 00 00 00 01 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x00000001], 0x00000001                       | 81 94 08 ff ff ff ff 01 00 00 00                |
    | adc dword [rax + 1 * rcx + 0x7f], 0x00000001                             | 81 54 08 7f 01 00 00 00                         |
    | adc dword [rax + 1 * rcx - 0x7f], 0x00000001                             | 81 54 08 81 01 00 00 00                         |
    | adc dword [rax + 1 * rcx + 0x80], 0x00000001                             | 81 94 08 80 00 00 00 01 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x80], 0x00000001                             | 81 54 08 80 01 00 00 00                         |
    | adc dword [rax + 1 * rcx - 0x81], 0x00000001                             | 81 94 08 7f ff ff ff 01 00 00 00                |
    | adc dword [rax + 1 * rcx + 0xff], 0x00000001                             | 81 94 08 ff 00 00 00 01 00 00 00                |
    | adc dword [rax + 1 * rcx - 0xff], 0x00000001                             | 81 94 08 01 ff ff ff 01 00 00 00                |
    | adc dword [rax + 1 * rcx + 0x7fffffff], 0x00000001                       | 81 94 08 ff ff ff 7f 01 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x7fffffff], 0x00000001                       | 81 94 08 01 00 00 80 01 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x80000000], 0x00000001                       | 81 94 08 00 00 00 80 01 00 00 00                |
    | adc dword [r10 + 0x7f], 0x00000001                                       | 41 81 52 7f 01 00 00 00                         |
    | adc dword [r10 + 0x80], 0x00000001                                       | 41 81 92 80 00 00 00 01 00 00 00                |
    | adc dword [r10 - 0x80], 0x00000001                                       | 41 81 52 80 01 00 00 00                         |
    | adc dword [r10 - 0x81], 0x00000001                                       | 41 81 92 7f ff ff ff 01 00 00 00                |
    | .prev5: nop; nop; nop; nop; nop; adc dword [rel @prev5], 0x00000001      | 90 90 90 90 90 81 15 f1 ff ff ff 01 00 00 00    |
    | .prev1: nop; adc dword [rel @prev1], 0x00000001                          | 90 81 15 f5 ff ff ff 01 00 00 00                |
    | adc dword [rel @next1], 0x00000001; nop; .next1: nop                     | 81 15 01 00 00 00 01 00 00 00 90 90             |
    | adc dword [rel @next5], 0x00000001; nop; nop; nop; nop; nop; .next5: nop | 81 15 05 00 00 00 01 00 00 00 90 90 90 90 90 90 |
    | adc dword [rax], 0x00000000                                              | 81 10 00 00 00 00                               |
    | adc dword [rax], 0x0000007f                                              | 81 10 7f 00 00 00                               |
    | adc dword [rax], 0x00000080                                              | 81 10 80 00 00 00                               |
    | adc dword [rax], 0x000000ff                                              | 81 10 ff 00 00 00                               |
    | adc dword [rax], 0x00000100                                              | 81 10 00 01 00 00                               |
    | adc dword [rax], 0x00007fff                                              | 81 10 ff 7f 00 00                               |
    | adc dword [rax], 0x00008000                                              | 81 10 00 80 00 00                               |
    | adc dword [rax], 0x0000ffff                                              | 81 10 ff ff 00 00                               |
    | adc dword [rax], 0x00010000                                              | 81 10 00 00 01 00                               |
    | adc dword [rax], 0x7fffffff                                              | 81 10 ff ff ff 7f                               |
    | adc dword [rax], 0x80000000                                              | 81 10 00 00 00 80                               |
    | adc dword [rax], 0xffffffff                                              | 81 10 ff ff ff ff                               |
    | adc dword [rcx], 0x0000007f                                              | 81 11 7f 00 00 00                               |
    | adc dword [rdx], 0x00000080                                              | 81 12 80 00 00 00                               |
    | adc dword [rbx], 0x000000ff                                              | 81 13 ff 00 00 00                               |
    | adc dword [rsp], 0x00000100                                              | 81 14 24 00 01 00 00                            |
    | adc dword [rbp], 0x00007fff                                              | 81 55 00 ff 7f 00 00                            |
    | adc dword [rsi], 0x00008000                                              | 81 16 00 80 00 00                               |
    | adc dword [rdi], 0x0000ffff                                              | 81 17 ff ff 00 00                               |
    | adc dword [r8], 0x00010000                                               | 41 81 10 00 00 01 00                            |
    | adc dword [r9], 0x7fffffff                                               | 41 81 11 ff ff ff 7f                            |
    | adc dword [r10], 0x80000000                                              | 41 81 12 00 00 00 80                            |
    | adc dword [r11], 0xffffffff                                              | 41 81 13 ff ff ff ff                            |
    | adc dword [r12], 0x00000000                                              | 41 81 14 24 00 00 00 00                         |
    | adc dword [r14], 0x0000007f                                              | 41 81 16 7f 00 00 00                            |
    | adc dword [r15], 0x00000080                                              | 41 81 17 80 00 00 00                            |
    | adc dword [rax + 1 * rcx], 0x000000ff                                    | 81 14 08 ff 00 00 00                            |
    | adc dword [rcx + 1 * rcx], 0x00000100                                    | 81 14 09 00 01 00 00                            |
    | adc dword [rdx + 1 * rcx], 0x00007fff                                    | 81 14 0a ff 7f 00 00                            |
    | adc dword [rbx + 1 * rcx], 0x00008000                                    | 81 14 0b 00 80 00 00                            |
    | adc dword [rsp + 1 * rcx], 0x0000ffff                                    | 81 14 0c ff ff 00 00                            |
    | adc dword [rbp + 1 * rcx], 0x00010000                                    | 81 54 0d 00 00 00 01 00                         |
    | adc dword [rsi + 1 * rcx], 0x7fffffff                                    | 81 14 0e ff ff ff 7f                            |
    | adc dword [rdi + 1 * rcx], 0x80000000                                    | 81 14 0f 00 00 00 80                            |
    | adc dword [r8 + 1 * rcx], 0xffffffff                                     | 41 81 14 08 ff ff ff ff                         |
    | adc dword [r9 + 1 * rcx], 0x00000000                                     | 41 81 14 09 00 00 00 00                         |
    | adc dword [r11 + 1 * rcx], 0x0000007f                                    | 41 81 14 0b 7f 00 00 00                         |
    | adc dword [r12 + 1 * rcx], 0x00000080                                    | 41 81 14 0c 80 00 00 00                         |
    | adc dword [r13 + 1 * rcx], 0x000000ff                                    | 41 81 54 0d 00 ff 00 00 00                      |
    | adc dword [r14 + 1 * rcx], 0x00000100                                    | 41 81 14 0e 00 01 00 00                         |
    | adc dword [r15 + 1 * rcx], 0x00007fff                                    | 41 81 14 0f ff 7f 00 00                         |
    | adc dword [rax + 1 * rax], 0x00008000                                    | 81 14 00 00 80 00 00                            |
    | adc dword [rax + 1 * rdx], 0x0000ffff                                    | 81 14 10 ff ff 00 00                            |
    | adc dword [rax + 1 * rbx], 0x00010000                                    | 81 14 18 00 00 01 00                            |
    | adc dword [rax + 1 * rbp], 0x7fffffff                                    | 81 14 28 ff ff ff 7f                            |
    | adc dword [rax + 1 * rsi], 0x80000000                                    | 81 14 30 00 00 00 80                            |
    | adc dword [rax + 1 * rdi], 0xffffffff                                    | 81 14 38 ff ff ff ff                            |
    | adc dword [rax + 1 * r8], 0x00000000                                     | 42 81 14 00 00 00 00 00                         |
    | adc dword [rax + 1 * r10], 0x0000007f                                    | 42 81 14 10 7f 00 00 00                         |
    | adc dword [rax + 1 * r11], 0x00000080                                    | 42 81 14 18 80 00 00 00                         |
    | adc dword [rax + 1 * r12], 0x000000ff                                    | 42 81 14 20 ff 00 00 00                         |
    | adc dword [rax + 1 * r13], 0x00000100                                    | 42 81 14 28 00 01 00 00                         |
    | adc dword [rax + 1 * r14], 0x00007fff                                    | 42 81 14 30 ff 7f 00 00                         |
    | adc dword [rax + 1 * r15], 0x00008000                                    | 42 81 14 38 00 80 00 00                         |
    | adc dword [rax + 2 * rcx], 0x0000ffff                                    | 81 14 48 ff ff 00 00                            |
    | adc dword [rax + 4 * rcx], 0x00010000                                    | 81 14 88 00 00 01 00                            |
    | adc dword [rax + 8 * rcx], 0x7fffffff                                    | 81 14 c8 ff ff ff 7f                            |
    | adc dword [r8 + 1 * r9], 0x80000000                                      | 43 81 14 08 00 00 00 80                         |
    | adc dword [r8 + 2 * r9], 0xffffffff                                      | 43 81 14 48 ff ff ff ff                         |
    | adc dword [r8 + 4 * r9], 0x00000000                                      | 43 81 14 88 00 00 00 00                         |
    | adc dword [1 * rcx], 0x0000007f                                          | 81 14 0d 00 00 00 00 7f 00 00 00                |
    | adc dword [2 * rcx], 0x00000080                                          | 81 14 4d 00 00 00 00 80 00 00 00                |
    | adc dword [4 * rcx], 0x000000ff                                          | 81 14 8d 00 00 00 00 ff 00 00 00                |
    | adc dword [8 * rcx], 0x00000100                                          | 81 14 cd 00 00 00 00 00 01 00 00                |
    | adc dword [1 * r9], 0x00007fff                                           | 42 81 14 0d 00 00 00 00 ff 7f 00 00             |
    | adc dword [2 * r9], 0x00008000                                           | 42 81 14 4d 00 00 00 00 00 80 00 00             |
    | adc dword [4 * r9], 0x0000ffff                                           | 42 81 14 8d 00 00 00 00 ff ff 00 00             |
    | adc dword [8 * r9], 0x00010000                                           | 42 81 14 cd 00 00 00 00 00 00 01 00             |
    | adc dword [r13 + 8 * r12], 0x7fffffff                                    | 43 81 54 e5 00 ff ff ff 7f                      |
    | adc dword [rsp + 4 * r15], 0x80000000                                    | 42 81 14 bc 00 00 00 80                         |
    | adc dword [rax + 1 * rcx + 0x00], 0xffffffff                             | 81 54 08 00 ff ff ff ff                         |
    | adc dword [rax + 1 * rcx - 0x00], 0x00000000                             | 81 54 08 00 00 00 00 00                         |
    | adc dword [rax + 1 * rcx - 0x01], 0x0000007f                             | 81 54 08 ff 7f 00 00 00                         |
    | adc dword [rax + 1 * rcx + 0x00000001], 0x00000080                       | 81 94 08 01 00 00 00 80 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x00000001], 0x000000ff                       | 81 94 08 ff ff ff ff ff 00 00 00                |
    | adc dword [rax + 1 * rcx + 0x7f], 0x00000100                             | 81 54 08 7f 00 01 00 00                         |
    | adc dword [rax + 1 * rcx - 0x7f], 0x00007fff                             | 81 54 08 81 ff 7f 00 00                         |
    | adc dword [rax + 1 * rcx + 0x80], 0x00008000                             | 81 94 08 80 00 00 00 00 80 00 00                |
    | adc dword [rax + 1 * rcx - 0x80], 0x0000ffff                             | 81 54 08 80 ff ff 00 00                         |
    | adc dword [rax + 1 * rcx - 0x81], 0x00010000                             | 81 94 08 7f ff ff ff 00 00 01 00                |
    | adc dword [rax + 1 * rcx + 0xff], 0x7fffffff                             | 81 94 08 ff 00 00 00 ff ff ff 7f                |
    | adc dword [rax + 1 * rcx - 0xff], 0x80000000                             | 81 94 08 01 ff ff ff 00 00 00 80                |
    | adc dword [rax + 1 * rcx + 0x7fffffff], 0xffffffff                       | 81 94 08 ff ff ff 7f ff ff ff ff                |
    | adc dword [rax + 1 * rcx - 0x7fffffff], 0x00000000                       | 81 94 08 01 00 00 80 00 00 00 00                |
    | adc dword [r10 + 0x7f], 0x0000007f                                       | 41 81 52 7f 7f 00 00 00                         |
    | adc dword [r10 + 0x80], 0x00000080                                       | 41 81 92 80 00 00 00 80 00 00 00                |
    | adc dword [r10 - 0x80], 0x000000ff                                       | 41 81 52 80 ff 00 00 00                         |
    | adc dword [r10 - 0x81], 0x00000100                                       | 41 81 92 7f ff ff ff 00 01 00 00                |
    | .prev5: nop; nop; nop; nop; nop; adc dword [rel @prev5], 0x00007fff      | 90 90 90 90 90 81 15 f1 ff ff ff ff 7f 00 00    |
    | .prev1: nop; adc dword [rel @prev1], 0x00008000                          | 90 81 15 f5 ff ff ff 00 80 00 00                |
    | adc dword [rel @next1], 0x0000ffff; nop; .next1: nop                     | 81 15 01 00 00 00 ff ff 00 00 90 90             |
    | adc dword [rel @next5], 0x00010000; nop; nop; nop; nop; nop; .next5: nop | 81 15 05 00 00 00 00 00 01 00 90 90 90 90 90 90 |
    | ------------------------------------------------------------------------ | ----------------------------------------------- |
"""


def can_encode_adc_addr32_imm32():
    encode(ADC_ADDR32_IMM32)


ADC_ADDR32_REG32 = """
    | ----------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                       | encoding                            |
    | ----------------------------------------------------------------- | ----------------------------------- |
    | adc dword [rax], ecx                                              | 11 08                               |
    | adc dword [rcx], ecx                                              | 11 09                               |
    | adc dword [rdx], ecx                                              | 11 0a                               |
    | adc dword [rbx], ecx                                              | 11 0b                               |
    | adc dword [rsp], ecx                                              | 11 0c 24                            |
    | adc dword [rbp], ecx                                              | 11 4d 00                            |
    | adc dword [rsi], ecx                                              | 11 0e                               |
    | adc dword [rdi], ecx                                              | 11 0f                               |
    | adc dword [r8], ecx                                               | 41 11 08                            |
    | adc dword [r9], ecx                                               | 41 11 09                            |
    | adc dword [r10], ecx                                              | 41 11 0a                            |
    | adc dword [r11], ecx                                              | 41 11 0b                            |
    | adc dword [r12], ecx                                              | 41 11 0c 24                         |
    | adc dword [r13], ecx                                              | 41 11 4d 00                         |
    | adc dword [r14], ecx                                              | 41 11 0e                            |
    | adc dword [r15], ecx                                              | 41 11 0f                            |
    | adc dword [rax + 1 * rcx], ecx                                    | 11 0c 08                            |
    | adc dword [rcx + 1 * rcx], ecx                                    | 11 0c 09                            |
    | adc dword [rdx + 1 * rcx], ecx                                    | 11 0c 0a                            |
    | adc dword [rbx + 1 * rcx], ecx                                    | 11 0c 0b                            |
    | adc dword [rsp + 1 * rcx], ecx                                    | 11 0c 0c                            |
    | adc dword [rbp + 1 * rcx], ecx                                    | 11 4c 0d 00                         |
    | adc dword [rsi + 1 * rcx], ecx                                    | 11 0c 0e                            |
    | adc dword [rdi + 1 * rcx], ecx                                    | 11 0c 0f                            |
    | adc dword [r8 + 1 * rcx], ecx                                     | 41 11 0c 08                         |
    | adc dword [r9 + 1 * rcx], ecx                                     | 41 11 0c 09                         |
    | adc dword [r10 + 1 * rcx], ecx                                    | 41 11 0c 0a                         |
    | adc dword [r11 + 1 * rcx], ecx                                    | 41 11 0c 0b                         |
    | adc dword [r12 + 1 * rcx], ecx                                    | 41 11 0c 0c                         |
    | adc dword [r13 + 1 * rcx], ecx                                    | 41 11 4c 0d 00                      |
    | adc dword [r14 + 1 * rcx], ecx                                    | 41 11 0c 0e                         |
    | adc dword [r15 + 1 * rcx], ecx                                    | 41 11 0c 0f                         |
    | adc dword [rax + 1 * rax], ecx                                    | 11 0c 00                            |
    | adc dword [rax + 1 * rdx], ecx                                    | 11 0c 10                            |
    | adc dword [rax + 1 * rbx], ecx                                    | 11 0c 18                            |
    | adc dword [rax + 1 * rbp], ecx                                    | 11 0c 28                            |
    | adc dword [rax + 1 * rsi], ecx                                    | 11 0c 30                            |
    | adc dword [rax + 1 * rdi], ecx                                    | 11 0c 38                            |
    | adc dword [rax + 1 * r8], ecx                                     | 42 11 0c 00                         |
    | adc dword [rax + 1 * r9], ecx                                     | 42 11 0c 08                         |
    | adc dword [rax + 1 * r10], ecx                                    | 42 11 0c 10                         |
    | adc dword [rax + 1 * r11], ecx                                    | 42 11 0c 18                         |
    | adc dword [rax + 1 * r12], ecx                                    | 42 11 0c 20                         |
    | adc dword [rax + 1 * r13], ecx                                    | 42 11 0c 28                         |
    | adc dword [rax + 1 * r14], ecx                                    | 42 11 0c 30                         |
    | adc dword [rax + 1 * r15], ecx                                    | 42 11 0c 38                         |
    | adc dword [rax + 2 * rcx], ecx                                    | 11 0c 48                            |
    | adc dword [rax + 4 * rcx], ecx                                    | 11 0c 88                            |
    | adc dword [rax + 8 * rcx], ecx                                    | 11 0c c8                            |
    | adc dword [r8 + 1 * r9], ecx                                      | 43 11 0c 08                         |
    | adc dword [r8 + 2 * r9], ecx                                      | 43 11 0c 48                         |
    | adc dword [r8 + 4 * r9], ecx                                      | 43 11 0c 88                         |
    | adc dword [r8 + 8 * r9], ecx                                      | 43 11 0c c8                         |
    | adc dword [1 * rcx], ecx                                          | 11 0c 0d 00 00 00 00                |
    | adc dword [2 * rcx], ecx                                          | 11 0c 4d 00 00 00 00                |
    | adc dword [4 * rcx], ecx                                          | 11 0c 8d 00 00 00 00                |
    | adc dword [8 * rcx], ecx                                          | 11 0c cd 00 00 00 00                |
    | adc dword [1 * r9], ecx                                           | 42 11 0c 0d 00 00 00 00             |
    | adc dword [2 * r9], ecx                                           | 42 11 0c 4d 00 00 00 00             |
    | adc dword [4 * r9], ecx                                           | 42 11 0c 8d 00 00 00 00             |
    | adc dword [8 * r9], ecx                                           | 42 11 0c cd 00 00 00 00             |
    | adc dword [r13 + 8 * r12], ecx                                    | 43 11 4c e5 00                      |
    | adc dword [rsp + 4 * r15], ecx                                    | 42 11 0c bc                         |
    | adc dword [rax + 1 * rcx + 0x00], ecx                             | 11 4c 08 00                         |
    | adc dword [rax + 1 * rcx - 0x00], ecx                             | 11 4c 08 00                         |
    | adc dword [rax + 1 * rcx + 0x01], ecx                             | 11 4c 08 01                         |
    | adc dword [rax + 1 * rcx - 0x01], ecx                             | 11 4c 08 ff                         |
    | adc dword [rax + 1 * rcx + 0x00000001], ecx                       | 11 8c 08 01 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x00000001], ecx                       | 11 8c 08 ff ff ff ff                |
    | adc dword [rax + 1 * rcx + 0x7f], ecx                             | 11 4c 08 7f                         |
    | adc dword [rax + 1 * rcx - 0x7f], ecx                             | 11 4c 08 81                         |
    | adc dword [rax + 1 * rcx + 0x80], ecx                             | 11 8c 08 80 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x80], ecx                             | 11 4c 08 80                         |
    | adc dword [rax + 1 * rcx - 0x81], ecx                             | 11 8c 08 7f ff ff ff                |
    | adc dword [rax + 1 * rcx + 0xff], ecx                             | 11 8c 08 ff 00 00 00                |
    | adc dword [rax + 1 * rcx - 0xff], ecx                             | 11 8c 08 01 ff ff ff                |
    | adc dword [rax + 1 * rcx + 0x7fffffff], ecx                       | 11 8c 08 ff ff ff 7f                |
    | adc dword [rax + 1 * rcx - 0x7fffffff], ecx                       | 11 8c 08 01 00 00 80                |
    | adc dword [rax + 1 * rcx - 0x80000000], ecx                       | 11 8c 08 00 00 00 80                |
    | adc dword [r10 + 0x7f], ecx                                       | 41 11 4a 7f                         |
    | adc dword [r10 + 0x80], ecx                                       | 41 11 8a 80 00 00 00                |
    | adc dword [r10 - 0x80], ecx                                       | 41 11 4a 80                         |
    | adc dword [r10 - 0x81], ecx                                       | 41 11 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc dword [rel @prev5], ecx      | 90 90 90 90 90 11 0d f5 ff ff ff    |
    | .prev1: nop; adc dword [rel @prev1], ecx                          | 90 11 0d f9 ff ff ff                |
    | adc dword [rel @next1], ecx; nop; .next1: nop                     | 11 0d 01 00 00 00 90 90             |
    | adc dword [rel @next5], ecx; nop; nop; nop; nop; nop; .next5: nop | 11 0d 05 00 00 00 90 90 90 90 90 90 |
    | adc dword [rax], eax                                              | 11 00                               |
    | adc dword [rax], edx                                              | 11 10                               |
    | adc dword [rax], ebx                                              | 11 18                               |
    | adc dword [rax], esp                                              | 11 20                               |
    | adc dword [rax], ebp                                              | 11 28                               |
    | adc dword [rax], esi                                              | 11 30                               |
    | adc dword [rax], edi                                              | 11 38                               |
    | adc dword [rax], r8d                                              | 44 11 00                            |
    | adc dword [rax], r9d                                              | 44 11 08                            |
    | adc dword [rax], r10d                                             | 44 11 10                            |
    | adc dword [rax], r11d                                             | 44 11 18                            |
    | adc dword [rax], r12d                                             | 44 11 20                            |
    | adc dword [rax], r13d                                             | 44 11 28                            |
    | adc dword [rax], r14d                                             | 44 11 30                            |
    | adc dword [rax], r15d                                             | 44 11 38                            |
    | adc dword [rcx], edx                                              | 11 11                               |
    | adc dword [rdx], ebx                                              | 11 1a                               |
    | adc dword [rbx], esp                                              | 11 23                               |
    | adc dword [rsp], ebp                                              | 11 2c 24                            |
    | adc dword [rbp], esi                                              | 11 75 00                            |
    | adc dword [rsi], edi                                              | 11 3e                               |
    | adc dword [rdi], r8d                                              | 44 11 07                            |
    | adc dword [r8], r9d                                               | 45 11 08                            |
    | adc dword [r9], r10d                                              | 45 11 11                            |
    | adc dword [r10], r11d                                             | 45 11 1a                            |
    | adc dword [r11], r12d                                             | 45 11 23                            |
    | adc dword [r12], r13d                                             | 45 11 2c 24                         |
    | adc dword [r13], r14d                                             | 45 11 75 00                         |
    | adc dword [r14], r15d                                             | 45 11 3e                            |
    | adc dword [r15], eax                                              | 41 11 07                            |
    | adc dword [rcx + 1 * rcx], edx                                    | 11 14 09                            |
    | adc dword [rdx + 1 * rcx], ebx                                    | 11 1c 0a                            |
    | adc dword [rbx + 1 * rcx], esp                                    | 11 24 0b                            |
    | adc dword [rsp + 1 * rcx], ebp                                    | 11 2c 0c                            |
    | adc dword [rbp + 1 * rcx], esi                                    | 11 74 0d 00                         |
    | adc dword [rsi + 1 * rcx], edi                                    | 11 3c 0e                            |
    | adc dword [rdi + 1 * rcx], r8d                                    | 44 11 04 0f                         |
    | adc dword [r8 + 1 * rcx], r9d                                     | 45 11 0c 08                         |
    | adc dword [r9 + 1 * rcx], r10d                                    | 45 11 14 09                         |
    | adc dword [r10 + 1 * rcx], r11d                                   | 45 11 1c 0a                         |
    | adc dword [r11 + 1 * rcx], r12d                                   | 45 11 24 0b                         |
    | adc dword [r12 + 1 * rcx], r13d                                   | 45 11 2c 0c                         |
    | adc dword [r13 + 1 * rcx], r14d                                   | 45 11 74 0d 00                      |
    | adc dword [r14 + 1 * rcx], r15d                                   | 45 11 3c 0e                         |
    | adc dword [r15 + 1 * rcx], eax                                    | 41 11 04 0f                         |
    | adc dword [rax + 1 * rdx], edx                                    | 11 14 10                            |
    | adc dword [rax + 1 * rbx], ebx                                    | 11 1c 18                            |
    | adc dword [rax + 1 * rbp], esp                                    | 11 24 28                            |
    | adc dword [rax + 1 * rsi], ebp                                    | 11 2c 30                            |
    | adc dword [rax + 1 * rdi], esi                                    | 11 34 38                            |
    | adc dword [rax + 1 * r8], edi                                     | 42 11 3c 00                         |
    | adc dword [rax + 1 * r9], r8d                                     | 46 11 04 08                         |
    | adc dword [rax + 1 * r10], r9d                                    | 46 11 0c 10                         |
    | adc dword [rax + 1 * r11], r10d                                   | 46 11 14 18                         |
    | adc dword [rax + 1 * r12], r11d                                   | 46 11 1c 20                         |
    | adc dword [rax + 1 * r13], r12d                                   | 46 11 24 28                         |
    | adc dword [rax + 1 * r14], r13d                                   | 46 11 2c 30                         |
    | adc dword [rax + 1 * r15], r14d                                   | 46 11 34 38                         |
    | adc dword [rax + 2 * rcx], r15d                                   | 44 11 3c 48                         |
    | adc dword [rax + 4 * rcx], eax                                    | 11 04 88                            |
    | adc dword [r8 + 1 * r9], edx                                      | 43 11 14 08                         |
    | adc dword [r8 + 2 * r9], ebx                                      | 43 11 1c 48                         |
    | adc dword [r8 + 4 * r9], esp                                      | 43 11 24 88                         |
    | adc dword [r8 + 8 * r9], ebp                                      | 43 11 2c c8                         |
    | adc dword [1 * rcx], esi                                          | 11 34 0d 00 00 00 00                |
    | adc dword [2 * rcx], edi                                          | 11 3c 4d 00 00 00 00                |
    | adc dword [4 * rcx], r8d                                          | 44 11 04 8d 00 00 00 00             |
    | adc dword [8 * rcx], r9d                                          | 44 11 0c cd 00 00 00 00             |
    | adc dword [1 * r9], r10d                                          | 46 11 14 0d 00 00 00 00             |
    | adc dword [2 * r9], r11d                                          | 46 11 1c 4d 00 00 00 00             |
    | adc dword [4 * r9], r12d                                          | 46 11 24 8d 00 00 00 00             |
    | adc dword [8 * r9], r13d                                          | 46 11 2c cd 00 00 00 00             |
    | adc dword [r13 + 8 * r12], r14d                                   | 47 11 74 e5 00                      |
    | adc dword [rsp + 4 * r15], r15d                                   | 46 11 3c bc                         |
    | adc dword [rax + 1 * rcx + 0x00], eax                             | 11 44 08 00                         |
    | adc dword [rax + 1 * rcx + 0x01], edx                             | 11 54 08 01                         |
    | adc dword [rax + 1 * rcx - 0x01], ebx                             | 11 5c 08 ff                         |
    | adc dword [rax + 1 * rcx + 0x00000001], esp                       | 11 a4 08 01 00 00 00                |
    | adc dword [rax + 1 * rcx - 0x00000001], ebp                       | 11 ac 08 ff ff ff ff                |
    | adc dword [rax + 1 * rcx + 0x7f], esi                             | 11 74 08 7f                         |
    | adc dword [rax + 1 * rcx - 0x7f], edi                             | 11 7c 08 81                         |
    | adc dword [rax + 1 * rcx + 0x80], r8d                             | 44 11 84 08 80 00 00 00             |
    | adc dword [rax + 1 * rcx - 0x80], r9d                             | 44 11 4c 08 80                      |
    | adc dword [rax + 1 * rcx - 0x81], r10d                            | 44 11 94 08 7f ff ff ff             |
    | adc dword [rax + 1 * rcx + 0xff], r11d                            | 44 11 9c 08 ff 00 00 00             |
    | adc dword [rax + 1 * rcx - 0xff], r12d                            | 44 11 a4 08 01 ff ff ff             |
    | adc dword [rax + 1 * rcx + 0x7fffffff], r13d                      | 44 11 ac 08 ff ff ff 7f             |
    | adc dword [rax + 1 * rcx - 0x7fffffff], r14d                      | 44 11 b4 08 01 00 00 80             |
    | adc dword [rax + 1 * rcx - 0x80000000], r15d                      | 44 11 bc 08 00 00 00 80             |
    | adc dword [r10 + 0x7f], eax                                       | 41 11 42 7f                         |
    | adc dword [r10 - 0x80], edx                                       | 41 11 52 80                         |
    | adc dword [r10 - 0x81], ebx                                       | 41 11 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc dword [rel @prev5], esp      | 90 90 90 90 90 11 25 f5 ff ff ff    |
    | .prev1: nop; adc dword [rel @prev1], ebp                          | 90 11 2d f9 ff ff ff                |
    | adc dword [rel @next1], esi; nop; .next1: nop                     | 11 35 01 00 00 00 90 90             |
    | adc dword [rel @next5], edi; nop; nop; nop; nop; nop; .next5: nop | 11 3d 05 00 00 00 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_adc_addr32_reg32():
    encode(ADC_ADDR32_REG32)


ADC_ADDR16_IMM8 = """
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | instruction                                                       | encoding                                  |
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | adc word [rax], 0x01                                              | 66 83 10 01                               |
    | adc word [rcx], 0x01                                              | 66 83 11 01                               |
    | adc word [rdx], 0x01                                              | 66 83 12 01                               |
    | adc word [rbx], 0x01                                              | 66 83 13 01                               |
    | adc word [rsp], 0x01                                              | 66 83 14 24 01                            |
    | adc word [rbp], 0x01                                              | 66 83 55 00 01                            |
    | adc word [rsi], 0x01                                              | 66 83 16 01                               |
    | adc word [rdi], 0x01                                              | 66 83 17 01                               |
    | adc word [r8], 0x01                                               | 66 41 83 10 01                            |
    | adc word [r9], 0x01                                               | 66 41 83 11 01                            |
    | adc word [r10], 0x01                                              | 66 41 83 12 01                            |
    | adc word [r11], 0x01                                              | 66 41 83 13 01                            |
    | adc word [r12], 0x01                                              | 66 41 83 14 24 01                         |
    | adc word [r13], 0x01                                              | 66 41 83 55 00 01                         |
    | adc word [r14], 0x01                                              | 66 41 83 16 01                            |
    | adc word [r15], 0x01                                              | 66 41 83 17 01                            |
    | adc word [rax + 1 * rcx], 0x01                                    | 66 83 14 08 01                            |
    | adc word [rcx + 1 * rcx], 0x01                                    | 66 83 14 09 01                            |
    | adc word [rdx + 1 * rcx], 0x01                                    | 66 83 14 0a 01                            |
    | adc word [rbx + 1 * rcx], 0x01                                    | 66 83 14 0b 01                            |
    | adc word [rsp + 1 * rcx], 0x01                                    | 66 83 14 0c 01                            |
    | adc word [rbp + 1 * rcx], 0x01                                    | 66 83 54 0d 00 01                         |
    | adc word [rsi + 1 * rcx], 0x01                                    | 66 83 14 0e 01                            |
    | adc word [rdi + 1 * rcx], 0x01                                    | 66 83 14 0f 01                            |
    | adc word [r8 + 1 * rcx], 0x01                                     | 66 41 83 14 08 01                         |
    | adc word [r9 + 1 * rcx], 0x01                                     | 66 41 83 14 09 01                         |
    | adc word [r10 + 1 * rcx], 0x01                                    | 66 41 83 14 0a 01                         |
    | adc word [r11 + 1 * rcx], 0x01                                    | 66 41 83 14 0b 01                         |
    | adc word [r12 + 1 * rcx], 0x01                                    | 66 41 83 14 0c 01                         |
    | adc word [r13 + 1 * rcx], 0x01                                    | 66 41 83 54 0d 00 01                      |
    | adc word [r14 + 1 * rcx], 0x01                                    | 66 41 83 14 0e 01                         |
    | adc word [r15 + 1 * rcx], 0x01                                    | 66 41 83 14 0f 01                         |
    | adc word [rax + 1 * rax], 0x01                                    | 66 83 14 00 01                            |
    | adc word [rax + 1 * rdx], 0x01                                    | 66 83 14 10 01                            |
    | adc word [rax + 1 * rbx], 0x01                                    | 66 83 14 18 01                            |
    | adc word [rax + 1 * rbp], 0x01                                    | 66 83 14 28 01                            |
    | adc word [rax + 1 * rsi], 0x01                                    | 66 83 14 30 01                            |
    | adc word [rax + 1 * rdi], 0x01                                    | 66 83 14 38 01                            |
    | adc word [rax + 1 * r8], 0x01                                     | 66 42 83 14 00 01                         |
    | adc word [rax + 1 * r9], 0x01                                     | 66 42 83 14 08 01                         |
    | adc word [rax + 1 * r10], 0x01                                    | 66 42 83 14 10 01                         |
    | adc word [rax + 1 * r11], 0x01                                    | 66 42 83 14 18 01                         |
    | adc word [rax + 1 * r12], 0x01                                    | 66 42 83 14 20 01                         |
    | adc word [rax + 1 * r13], 0x01                                    | 66 42 83 14 28 01                         |
    | adc word [rax + 1 * r14], 0x01                                    | 66 42 83 14 30 01                         |
    | adc word [rax + 1 * r15], 0x01                                    | 66 42 83 14 38 01                         |
    | adc word [rax + 2 * rcx], 0x01                                    | 66 83 14 48 01                            |
    | adc word [rax + 4 * rcx], 0x01                                    | 66 83 14 88 01                            |
    | adc word [rax + 8 * rcx], 0x01                                    | 66 83 14 c8 01                            |
    | adc word [r8 + 1 * r9], 0x01                                      | 66 43 83 14 08 01                         |
    | adc word [r8 + 2 * r9], 0x01                                      | 66 43 83 14 48 01                         |
    | adc word [r8 + 4 * r9], 0x01                                      | 66 43 83 14 88 01                         |
    | adc word [r8 + 8 * r9], 0x01                                      | 66 43 83 14 c8 01                         |
    | adc word [1 * rcx], 0x01                                          | 66 83 14 0d 00 00 00 00 01                |
    | adc word [2 * rcx], 0x01                                          | 66 83 14 4d 00 00 00 00 01                |
    | adc word [4 * rcx], 0x01                                          | 66 83 14 8d 00 00 00 00 01                |
    | adc word [8 * rcx], 0x01                                          | 66 83 14 cd 00 00 00 00 01                |
    | adc word [1 * r9], 0x01                                           | 66 42 83 14 0d 00 00 00 00 01             |
    | adc word [2 * r9], 0x01                                           | 66 42 83 14 4d 00 00 00 00 01             |
    | adc word [4 * r9], 0x01                                           | 66 42 83 14 8d 00 00 00 00 01             |
    | adc word [8 * r9], 0x01                                           | 66 42 83 14 cd 00 00 00 00 01             |
    | adc word [r13 + 8 * r12], 0x01                                    | 66 43 83 54 e5 00 01                      |
    | adc word [rsp + 4 * r15], 0x01                                    | 66 42 83 14 bc 01                         |
    | adc word [rax + 1 * rcx + 0x00], 0x01                             | 66 83 54 08 00 01                         |
    | adc word [rax + 1 * rcx - 0x00], 0x01                             | 66 83 54 08 00 01                         |
    | adc word [rax + 1 * rcx + 0x01], 0x01                             | 66 83 54 08 01 01                         |
    | adc word [rax + 1 * rcx - 0x01], 0x01                             | 66 83 54 08 ff 01                         |
    | adc word [rax + 1 * rcx + 0x00000001], 0x01                       | 66 83 94 08 01 00 00 00 01                |
    | adc word [rax + 1 * rcx - 0x00000001], 0x01                       | 66 83 94 08 ff ff ff ff 01                |
    | adc word [rax + 1 * rcx + 0x7f], 0x01                             | 66 83 54 08 7f 01                         |
    | adc word [rax + 1 * rcx - 0x7f], 0x01                             | 66 83 54 08 81 01                         |
    | adc word [rax + 1 * rcx + 0x80], 0x01                             | 66 83 94 08 80 00 00 00 01                |
    | adc word [rax + 1 * rcx - 0x80], 0x01                             | 66 83 54 08 80 01                         |
    | adc word [rax + 1 * rcx - 0x81], 0x01                             | 66 83 94 08 7f ff ff ff 01                |
    | adc word [rax + 1 * rcx + 0xff], 0x01                             | 66 83 94 08 ff 00 00 00 01                |
    | adc word [rax + 1 * rcx - 0xff], 0x01                             | 66 83 94 08 01 ff ff ff 01                |
    | adc word [rax + 1 * rcx + 0x7fffffff], 0x01                       | 66 83 94 08 ff ff ff 7f 01                |
    | adc word [rax + 1 * rcx - 0x7fffffff], 0x01                       | 66 83 94 08 01 00 00 80 01                |
    | adc word [rax + 1 * rcx - 0x80000000], 0x01                       | 66 83 94 08 00 00 00 80 01                |
    | adc word [r10 + 0x7f], 0x01                                       | 66 41 83 52 7f 01                         |
    | adc word [r10 + 0x80], 0x01                                       | 66 41 83 92 80 00 00 00 01                |
    | adc word [r10 - 0x80], 0x01                                       | 66 41 83 52 80 01                         |
    | adc word [r10 - 0x81], 0x01                                       | 66 41 83 92 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; adc word [rel @prev5], 0x01      | 90 90 90 90 90 66 83 15 f3 ff ff ff 01    |
    | .prev1: nop; adc word [rel @prev1], 0x01                          | 90 66 83 15 f7 ff ff ff 01                |
    | adc word [rel @next1], 0x01; nop; .next1: nop                     | 66 83 15 01 00 00 00 01 90 90             |
    | adc word [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 66 83 15 05 00 00 00 01 90 90 90 90 90 90 |
    | adc word [rax], 0x00                                              | 66 83 10 00                               |
    | adc word [rax], 0x7f                                              | 66 83 10 7f                               |
    | adc word [rax], 0x80                                              | 66 83 10 80                               |
    | adc word [rax], 0xff                                              | 66 83 10 ff                               |
    | adc word [rcx], 0x7f                                              | 66 83 11 7f                               |
    | adc word [rdx], 0x80                                              | 66 83 12 80                               |
    | adc word [rbx], 0xff                                              | 66 83 13 ff                               |
    | adc word [rsp], 0x00                                              | 66 83 14 24 00                            |
    | adc word [rsi], 0x7f                                              | 66 83 16 7f                               |
    | adc word [rdi], 0x80                                              | 66 83 17 80                               |
    | adc word [r8], 0xff                                               | 66 41 83 10 ff                            |
    | adc word [r9], 0x00                                               | 66 41 83 11 00                            |
    | adc word [r11], 0x7f                                              | 66 41 83 13 7f                            |
    | adc word [r12], 0x80                                              | 66 41 83 14 24 80                         |
    | adc word [r13], 0xff                                              | 66 41 83 55 00 ff                         |
    | adc word [r14], 0x00                                              | 66 41 83 16 00                            |
    | adc word [rax + 1 * rcx], 0x7f                                    | 66 83 14 08 7f                            |
    | adc word [rcx + 1 * rcx], 0x80                                    | 66 83 14 09 80                            |
    | adc word [rdx + 1 * rcx], 0xff                                    | 66 83 14 0a ff                            |
    | adc word [rbx + 1 * rcx], 0x00                                    | 66 83 14 0b 00                            |
    | adc word [rbp + 1 * rcx], 0x7f                                    | 66 83 54 0d 00 7f                         |
    | adc word [rsi + 1 * rcx], 0x80                                    | 66 83 14 0e 80                            |
    | adc word [rdi + 1 * rcx], 0xff                                    | 66 83 14 0f ff                            |
    | adc word [r8 + 1 * rcx], 0x00                                     | 66 41 83 14 08 00                         |
    | adc word [r10 + 1 * rcx], 0x7f                                    | 66 41 83 14 0a 7f                         |
    | adc word [r11 + 1 * rcx], 0x80                                    | 66 41 83 14 0b 80                         |
    | adc word [r12 + 1 * rcx], 0xff                                    | 66 41 83 14 0c ff                         |
    | adc word [r13 + 1 * rcx], 0x00                                    | 66 41 83 54 0d 00 00                      |
    | adc word [r15 + 1 * rcx], 0x7f                                    | 66 41 83 14 0f 7f                         |
    | adc word [rax + 1 * rax], 0x80                                    | 66 83 14 00 80                            |
    | adc word [rax + 1 * rdx], 0xff                                    | 66 83 14 10 ff                            |
    | adc word [rax + 1 * rbx], 0x00                                    | 66 83 14 18 00                            |
    | adc word [rax + 1 * rsi], 0x7f                                    | 66 83 14 30 7f                            |
    | adc word [rax + 1 * rdi], 0x80                                    | 66 83 14 38 80                            |
    | adc word [rax + 1 * r8], 0xff                                     | 66 42 83 14 00 ff                         |
    | adc word [rax + 1 * r9], 0x00                                     | 66 42 83 14 08 00                         |
    | adc word [rax + 1 * r11], 0x7f                                    | 66 42 83 14 18 7f                         |
    | adc word [rax + 1 * r12], 0x80                                    | 66 42 83 14 20 80                         |
    | adc word [rax + 1 * r13], 0xff                                    | 66 42 83 14 28 ff                         |
    | adc word [rax + 1 * r14], 0x00                                    | 66 42 83 14 30 00                         |
    | adc word [rax + 2 * rcx], 0x7f                                    | 66 83 14 48 7f                            |
    | adc word [rax + 4 * rcx], 0x80                                    | 66 83 14 88 80                            |
    | adc word [rax + 8 * rcx], 0xff                                    | 66 83 14 c8 ff                            |
    | adc word [r8 + 1 * r9], 0x00                                      | 66 43 83 14 08 00                         |
    | adc word [r8 + 4 * r9], 0x7f                                      | 66 43 83 14 88 7f                         |
    | adc word [r8 + 8 * r9], 0x80                                      | 66 43 83 14 c8 80                         |
    | adc word [1 * rcx], 0xff                                          | 66 83 14 0d 00 00 00 00 ff                |
    | adc word [2 * rcx], 0x00                                          | 66 83 14 4d 00 00 00 00 00                |
    | adc word [8 * rcx], 0x7f                                          | 66 83 14 cd 00 00 00 00 7f                |
    | adc word [1 * r9], 0x80                                           | 66 42 83 14 0d 00 00 00 00 80             |
    | adc word [2 * r9], 0xff                                           | 66 42 83 14 4d 00 00 00 00 ff             |
    | adc word [4 * r9], 0x00                                           | 66 42 83 14 8d 00 00 00 00 00             |
    | adc word [r13 + 8 * r12], 0x7f                                    | 66 43 83 54 e5 00 7f                      |
    | adc word [rsp + 4 * r15], 0x80                                    | 66 42 83 14 bc 80                         |
    | adc word [rax + 1 * rcx + 0x00], 0xff                             | 66 83 54 08 00 ff                         |
    | adc word [rax + 1 * rcx - 0x00], 0x00                             | 66 83 54 08 00 00                         |
    | adc word [rax + 1 * rcx - 0x01], 0x7f                             | 66 83 54 08 ff 7f                         |
    | adc word [rax + 1 * rcx + 0x00000001], 0x80                       | 66 83 94 08 01 00 00 00 80                |
    | adc word [rax + 1 * rcx - 0x00000001], 0xff                       | 66 83 94 08 ff ff ff ff ff                |
    | adc word [rax + 1 * rcx + 0x7f], 0x00                             | 66 83 54 08 7f 00                         |
    | adc word [rax + 1 * rcx + 0x80], 0x7f                             | 66 83 94 08 80 00 00 00 7f                |
    | adc word [rax + 1 * rcx - 0x80], 0x80                             | 66 83 54 08 80 80                         |
    | adc word [rax + 1 * rcx - 0x81], 0xff                             | 66 83 94 08 7f ff ff ff ff                |
    | adc word [rax + 1 * rcx + 0xff], 0x00                             | 66 83 94 08 ff 00 00 00 00                |
    | adc word [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 66 83 94 08 ff ff ff 7f 7f                |
    | adc word [rax + 1 * rcx - 0x7fffffff], 0x80                       | 66 83 94 08 01 00 00 80 80                |
    | adc word [rax + 1 * rcx - 0x80000000], 0xff                       | 66 83 94 08 00 00 00 80 ff                |
    | adc word [r10 + 0x7f], 0x00                                       | 66 41 83 52 7f 00                         |
    | adc word [r10 - 0x80], 0x7f                                       | 66 41 83 52 80 7f                         |
    | adc word [r10 - 0x81], 0x80                                       | 66 41 83 92 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; adc word [rel @prev5], 0xff      | 90 90 90 90 90 66 83 15 f3 ff ff ff ff    |
    | .prev1: nop; adc word [rel @prev1], 0x00                          | 90 66 83 15 f7 ff ff ff 00                |
    | adc word [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 66 83 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------------- |
"""


def can_encode_adc_addr16_imm8():
    encode(ADC_ADDR16_IMM8)


ADC_ADDR16_IMM16 = """
    | ------------------------------------------------------------------- | -------------------------------------------- |
    | instruction                                                         | encoding                                     |
    | ------------------------------------------------------------------- | -------------------------------------------- |
    | adc word [rax], 0x0001                                              | 66 81 10 01 00                               |
    | adc word [rcx], 0x0001                                              | 66 81 11 01 00                               |
    | adc word [rdx], 0x0001                                              | 66 81 12 01 00                               |
    | adc word [rbx], 0x0001                                              | 66 81 13 01 00                               |
    | adc word [rsp], 0x0001                                              | 66 81 14 24 01 00                            |
    | adc word [rbp], 0x0001                                              | 66 81 55 00 01 00                            |
    | adc word [rsi], 0x0001                                              | 66 81 16 01 00                               |
    | adc word [rdi], 0x0001                                              | 66 81 17 01 00                               |
    | adc word [r8], 0x0001                                               | 66 41 81 10 01 00                            |
    | adc word [r9], 0x0001                                               | 66 41 81 11 01 00                            |
    | adc word [r10], 0x0001                                              | 66 41 81 12 01 00                            |
    | adc word [r11], 0x0001                                              | 66 41 81 13 01 00                            |
    | adc word [r12], 0x0001                                              | 66 41 81 14 24 01 00                         |
    | adc word [r13], 0x0001                                              | 66 41 81 55 00 01 00                         |
    | adc word [r14], 0x0001                                              | 66 41 81 16 01 00                            |
    | adc word [r15], 0x0001                                              | 66 41 81 17 01 00                            |
    | adc word [rax + 1 * rcx], 0x0001                                    | 66 81 14 08 01 00                            |
    | adc word [rcx + 1 * rcx], 0x0001                                    | 66 81 14 09 01 00                            |
    | adc word [rdx + 1 * rcx], 0x0001                                    | 66 81 14 0a 01 00                            |
    | adc word [rbx + 1 * rcx], 0x0001                                    | 66 81 14 0b 01 00                            |
    | adc word [rsp + 1 * rcx], 0x0001                                    | 66 81 14 0c 01 00                            |
    | adc word [rbp + 1 * rcx], 0x0001                                    | 66 81 54 0d 00 01 00                         |
    | adc word [rsi + 1 * rcx], 0x0001                                    | 66 81 14 0e 01 00                            |
    | adc word [rdi + 1 * rcx], 0x0001                                    | 66 81 14 0f 01 00                            |
    | adc word [r8 + 1 * rcx], 0x0001                                     | 66 41 81 14 08 01 00                         |
    | adc word [r9 + 1 * rcx], 0x0001                                     | 66 41 81 14 09 01 00                         |
    | adc word [r10 + 1 * rcx], 0x0001                                    | 66 41 81 14 0a 01 00                         |
    | adc word [r11 + 1 * rcx], 0x0001                                    | 66 41 81 14 0b 01 00                         |
    | adc word [r12 + 1 * rcx], 0x0001                                    | 66 41 81 14 0c 01 00                         |
    | adc word [r13 + 1 * rcx], 0x0001                                    | 66 41 81 54 0d 00 01 00                      |
    | adc word [r14 + 1 * rcx], 0x0001                                    | 66 41 81 14 0e 01 00                         |
    | adc word [r15 + 1 * rcx], 0x0001                                    | 66 41 81 14 0f 01 00                         |
    | adc word [rax + 1 * rax], 0x0001                                    | 66 81 14 00 01 00                            |
    | adc word [rax + 1 * rdx], 0x0001                                    | 66 81 14 10 01 00                            |
    | adc word [rax + 1 * rbx], 0x0001                                    | 66 81 14 18 01 00                            |
    | adc word [rax + 1 * rbp], 0x0001                                    | 66 81 14 28 01 00                            |
    | adc word [rax + 1 * rsi], 0x0001                                    | 66 81 14 30 01 00                            |
    | adc word [rax + 1 * rdi], 0x0001                                    | 66 81 14 38 01 00                            |
    | adc word [rax + 1 * r8], 0x0001                                     | 66 42 81 14 00 01 00                         |
    | adc word [rax + 1 * r9], 0x0001                                     | 66 42 81 14 08 01 00                         |
    | adc word [rax + 1 * r10], 0x0001                                    | 66 42 81 14 10 01 00                         |
    | adc word [rax + 1 * r11], 0x0001                                    | 66 42 81 14 18 01 00                         |
    | adc word [rax + 1 * r12], 0x0001                                    | 66 42 81 14 20 01 00                         |
    | adc word [rax + 1 * r13], 0x0001                                    | 66 42 81 14 28 01 00                         |
    | adc word [rax + 1 * r14], 0x0001                                    | 66 42 81 14 30 01 00                         |
    | adc word [rax + 1 * r15], 0x0001                                    | 66 42 81 14 38 01 00                         |
    | adc word [rax + 2 * rcx], 0x0001                                    | 66 81 14 48 01 00                            |
    | adc word [rax + 4 * rcx], 0x0001                                    | 66 81 14 88 01 00                            |
    | adc word [rax + 8 * rcx], 0x0001                                    | 66 81 14 c8 01 00                            |
    | adc word [r8 + 1 * r9], 0x0001                                      | 66 43 81 14 08 01 00                         |
    | adc word [r8 + 2 * r9], 0x0001                                      | 66 43 81 14 48 01 00                         |
    | adc word [r8 + 4 * r9], 0x0001                                      | 66 43 81 14 88 01 00                         |
    | adc word [r8 + 8 * r9], 0x0001                                      | 66 43 81 14 c8 01 00                         |
    | adc word [1 * rcx], 0x0001                                          | 66 81 14 0d 00 00 00 00 01 00                |
    | adc word [2 * rcx], 0x0001                                          | 66 81 14 4d 00 00 00 00 01 00                |
    | adc word [4 * rcx], 0x0001                                          | 66 81 14 8d 00 00 00 00 01 00                |
    | adc word [8 * rcx], 0x0001                                          | 66 81 14 cd 00 00 00 00 01 00                |
    | adc word [1 * r9], 0x0001                                           | 66 42 81 14 0d 00 00 00 00 01 00             |
    | adc word [2 * r9], 0x0001                                           | 66 42 81 14 4d 00 00 00 00 01 00             |
    | adc word [4 * r9], 0x0001                                           | 66 42 81 14 8d 00 00 00 00 01 00             |
    | adc word [8 * r9], 0x0001                                           | 66 42 81 14 cd 00 00 00 00 01 00             |
    | adc word [r13 + 8 * r12], 0x0001                                    | 66 43 81 54 e5 00 01 00                      |
    | adc word [rsp + 4 * r15], 0x0001                                    | 66 42 81 14 bc 01 00                         |
    | adc word [rax + 1 * rcx + 0x00], 0x0001                             | 66 81 54 08 00 01 00                         |
    | adc word [rax + 1 * rcx - 0x00], 0x0001                             | 66 81 54 08 00 01 00                         |
    | adc word [rax + 1 * rcx + 0x01], 0x0001                             | 66 81 54 08 01 01 00                         |
    | adc word [rax + 1 * rcx - 0x01], 0x0001                             | 66 81 54 08 ff 01 00                         |
    | adc word [rax + 1 * rcx + 0x00000001], 0x0001                       | 66 81 94 08 01 00 00 00 01 00                |
    | adc word [rax + 1 * rcx - 0x00000001], 0x0001                       | 66 81 94 08 ff ff ff ff 01 00                |
    | adc word [rax + 1 * rcx + 0x7f], 0x0001                             | 66 81 54 08 7f 01 00                         |
    | adc word [rax + 1 * rcx - 0x7f], 0x0001                             | 66 81 54 08 81 01 00                         |
    | adc word [rax + 1 * rcx + 0x80], 0x0001                             | 66 81 94 08 80 00 00 00 01 00                |
    | adc word [rax + 1 * rcx - 0x80], 0x0001                             | 66 81 54 08 80 01 00                         |
    | adc word [rax + 1 * rcx - 0x81], 0x0001                             | 66 81 94 08 7f ff ff ff 01 00                |
    | adc word [rax + 1 * rcx + 0xff], 0x0001                             | 66 81 94 08 ff 00 00 00 01 00                |
    | adc word [rax + 1 * rcx - 0xff], 0x0001                             | 66 81 94 08 01 ff ff ff 01 00                |
    | adc word [rax + 1 * rcx + 0x7fffffff], 0x0001                       | 66 81 94 08 ff ff ff 7f 01 00                |
    | adc word [rax + 1 * rcx - 0x7fffffff], 0x0001                       | 66 81 94 08 01 00 00 80 01 00                |
    | adc word [rax + 1 * rcx - 0x80000000], 0x0001                       | 66 81 94 08 00 00 00 80 01 00                |
    | adc word [r10 + 0x7f], 0x0001                                       | 66 41 81 52 7f 01 00                         |
    | adc word [r10 + 0x80], 0x0001                                       | 66 41 81 92 80 00 00 00 01 00                |
    | adc word [r10 - 0x80], 0x0001                                       | 66 41 81 52 80 01 00                         |
    | adc word [r10 - 0x81], 0x0001                                       | 66 41 81 92 7f ff ff ff 01 00                |
    | .prev5: nop; nop; nop; nop; nop; adc word [rel @prev5], 0x0001      | 90 90 90 90 90 66 81 15 f2 ff ff ff 01 00    |
    | .prev1: nop; adc word [rel @prev1], 0x0001                          | 90 66 81 15 f6 ff ff ff 01 00                |
    | adc word [rel @next1], 0x0001; nop; .next1: nop                     | 66 81 15 01 00 00 00 01 00 90 90             |
    | adc word [rel @next5], 0x0001; nop; nop; nop; nop; nop; .next5: nop | 66 81 15 05 00 00 00 01 00 90 90 90 90 90 90 |
    | adc word [rax], 0x0000                                              | 66 81 10 00 00                               |
    | adc word [rax], 0x007f                                              | 66 81 10 7f 00                               |
    | adc word [rax], 0x0080                                              | 66 81 10 80 00                               |
    | adc word [rax], 0x00ff                                              | 66 81 10 ff 00                               |
    | adc word [rax], 0x0100                                              | 66 81 10 00 01                               |
    | adc word [rax], 0x7fff                                              | 66 81 10 ff 7f                               |
    | adc word [rax], 0x8000                                              | 66 81 10 00 80                               |
    | adc word [rax], 0xffff                                              | 66 81 10 ff ff                               |
    | adc word [rcx], 0x007f                                              | 66 81 11 7f 00                               |
    | adc word [rdx], 0x0080                                              | 66 81 12 80 00                               |
    | adc word [rbx], 0x00ff                                              | 66 81 13 ff 00                               |
    | adc word [rsp], 0x0100                                              | 66 81 14 24 00 01                            |
    | adc word [rbp], 0x7fff                                              | 66 81 55 00 ff 7f                            |
    | adc word [rsi], 0x8000                                              | 66 81 16 00 80                               |
    | adc word [rdi], 0xffff                                              | 66 81 17 ff ff                               |
    | adc word [r8], 0x0000                                               | 66 41 81 10 00 00                            |
    | adc word [r10], 0x007f                                              | 66 41 81 12 7f 00                            |
    | adc word [r11], 0x0080                                              | 66 41 81 13 80 00                            |
    | adc word [r12], 0x00ff                                              | 66 41 81 14 24 ff 00                         |
    | adc word [r13], 0x0100                                              | 66 41 81 55 00 00 01                         |
    | adc word [r14], 0x7fff                                              | 66 41 81 16 ff 7f                            |
    | adc word [r15], 0x8000                                              | 66 41 81 17 00 80                            |
    | adc word [rax + 1 * rcx], 0xffff                                    | 66 81 14 08 ff ff                            |
    | adc word [rcx + 1 * rcx], 0x0000                                    | 66 81 14 09 00 00                            |
    | adc word [rbx + 1 * rcx], 0x007f                                    | 66 81 14 0b 7f 00                            |
    | adc word [rsp + 1 * rcx], 0x0080                                    | 66 81 14 0c 80 00                            |
    | adc word [rbp + 1 * rcx], 0x00ff                                    | 66 81 54 0d 00 ff 00                         |
    | adc word [rsi + 1 * rcx], 0x0100                                    | 66 81 14 0e 00 01                            |
    | adc word [rdi + 1 * rcx], 0x7fff                                    | 66 81 14 0f ff 7f                            |
    | adc word [r8 + 1 * rcx], 0x8000                                     | 66 41 81 14 08 00 80                         |
    | adc word [r9 + 1 * rcx], 0xffff                                     | 66 41 81 14 09 ff ff                         |
    | adc word [r10 + 1 * rcx], 0x0000                                    | 66 41 81 14 0a 00 00                         |
    | adc word [r12 + 1 * rcx], 0x007f                                    | 66 41 81 14 0c 7f 00                         |
    | adc word [r13 + 1 * rcx], 0x0080                                    | 66 41 81 54 0d 00 80 00                      |
    | adc word [r14 + 1 * rcx], 0x00ff                                    | 66 41 81 14 0e ff 00                         |
    | adc word [r15 + 1 * rcx], 0x0100                                    | 66 41 81 14 0f 00 01                         |
    | adc word [rax + 1 * rax], 0x7fff                                    | 66 81 14 00 ff 7f                            |
    | adc word [rax + 1 * rdx], 0x8000                                    | 66 81 14 10 00 80                            |
    | adc word [rax + 1 * rbx], 0xffff                                    | 66 81 14 18 ff ff                            |
    | adc word [rax + 1 * rbp], 0x0000                                    | 66 81 14 28 00 00                            |
    | adc word [rax + 1 * rdi], 0x007f                                    | 66 81 14 38 7f 00                            |
    | adc word [rax + 1 * r8], 0x0080                                     | 66 42 81 14 00 80 00                         |
    | adc word [rax + 1 * r9], 0x00ff                                     | 66 42 81 14 08 ff 00                         |
    | adc word [rax + 1 * r10], 0x0100                                    | 66 42 81 14 10 00 01                         |
    | adc word [rax + 1 * r11], 0x7fff                                    | 66 42 81 14 18 ff 7f                         |
    | adc word [rax + 1 * r12], 0x8000                                    | 66 42 81 14 20 00 80                         |
    | adc word [rax + 1 * r13], 0xffff                                    | 66 42 81 14 28 ff ff                         |
    | adc word [rax + 1 * r14], 0x0000                                    | 66 42 81 14 30 00 00                         |
    | adc word [rax + 2 * rcx], 0x007f                                    | 66 81 14 48 7f 00                            |
    | adc word [rax + 4 * rcx], 0x0080                                    | 66 81 14 88 80 00                            |
    | adc word [rax + 8 * rcx], 0x00ff                                    | 66 81 14 c8 ff 00                            |
    | adc word [r8 + 1 * r9], 0x0100                                      | 66 43 81 14 08 00 01                         |
    | adc word [r8 + 2 * r9], 0x7fff                                      | 66 43 81 14 48 ff 7f                         |
    | adc word [r8 + 4 * r9], 0x8000                                      | 66 43 81 14 88 00 80                         |
    | adc word [r8 + 8 * r9], 0xffff                                      | 66 43 81 14 c8 ff ff                         |
    | adc word [1 * rcx], 0x0000                                          | 66 81 14 0d 00 00 00 00 00 00                |
    | adc word [4 * rcx], 0x007f                                          | 66 81 14 8d 00 00 00 00 7f 00                |
    | adc word [8 * rcx], 0x0080                                          | 66 81 14 cd 00 00 00 00 80 00                |
    | adc word [1 * r9], 0x00ff                                           | 66 42 81 14 0d 00 00 00 00 ff 00             |
    | adc word [2 * r9], 0x0100                                           | 66 42 81 14 4d 00 00 00 00 00 01             |
    | adc word [4 * r9], 0x7fff                                           | 66 42 81 14 8d 00 00 00 00 ff 7f             |
    | adc word [8 * r9], 0x8000                                           | 66 42 81 14 cd 00 00 00 00 00 80             |
    | adc word [r13 + 8 * r12], 0xffff                                    | 66 43 81 54 e5 00 ff ff                      |
    | adc word [rsp + 4 * r15], 0x0000                                    | 66 42 81 14 bc 00 00                         |
    | adc word [rax + 1 * rcx - 0x00], 0x007f                             | 66 81 54 08 00 7f 00                         |
    | adc word [rax + 1 * rcx + 0x01], 0x0080                             | 66 81 54 08 01 80 00                         |
    | adc word [rax + 1 * rcx - 0x01], 0x00ff                             | 66 81 54 08 ff ff 00                         |
    | adc word [rax + 1 * rcx + 0x00000001], 0x0100                       | 66 81 94 08 01 00 00 00 00 01                |
    | adc word [rax + 1 * rcx - 0x00000001], 0x7fff                       | 66 81 94 08 ff ff ff ff ff 7f                |
    | adc word [rax + 1 * rcx + 0x7f], 0x8000                             | 66 81 54 08 7f 00 80                         |
    | adc word [rax + 1 * rcx - 0x7f], 0xffff                             | 66 81 54 08 81 ff ff                         |
    | adc word [rax + 1 * rcx + 0x80], 0x0000                             | 66 81 94 08 80 00 00 00 00 00                |
    | adc word [rax + 1 * rcx - 0x81], 0x007f                             | 66 81 94 08 7f ff ff ff 7f 00                |
    | adc word [rax + 1 * rcx + 0xff], 0x0080                             | 66 81 94 08 ff 00 00 00 80 00                |
    | adc word [rax + 1 * rcx - 0xff], 0x00ff                             | 66 81 94 08 01 ff ff ff ff 00                |
    | adc word [rax + 1 * rcx + 0x7fffffff], 0x0100                       | 66 81 94 08 ff ff ff 7f 00 01                |
    | adc word [rax + 1 * rcx - 0x7fffffff], 0x7fff                       | 66 81 94 08 01 00 00 80 ff 7f                |
    | adc word [rax + 1 * rcx - 0x80000000], 0x8000                       | 66 81 94 08 00 00 00 80 00 80                |
    | adc word [r10 + 0x7f], 0xffff                                       | 66 41 81 52 7f ff ff                         |
    | adc word [r10 + 0x80], 0x0000                                       | 66 41 81 92 80 00 00 00 00 00                |
    | adc word [r10 - 0x81], 0x007f                                       | 66 41 81 92 7f ff ff ff 7f 00                |
    | .prev5: nop; nop; nop; nop; nop; adc word [rel @prev5], 0x0080      | 90 90 90 90 90 66 81 15 f2 ff ff ff 80 00    |
    | .prev1: nop; adc word [rel @prev1], 0x00ff                          | 90 66 81 15 f6 ff ff ff ff 00                |
    | adc word [rel @next1], 0x0100; nop; .next1: nop                     | 66 81 15 01 00 00 00 00 01 90 90             |
    | adc word [rel @next5], 0x7fff; nop; nop; nop; nop; nop; .next5: nop | 66 81 15 05 00 00 00 ff 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------- | -------------------------------------------- |
"""


def can_encode_adc_addr16_imm16():
    encode(ADC_ADDR16_IMM16)


ADC_ADDR16_REG16 = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | adc word [rax], cx                                              | 66 11 08                               |
    | adc word [rcx], cx                                              | 66 11 09                               |
    | adc word [rdx], cx                                              | 66 11 0a                               |
    | adc word [rbx], cx                                              | 66 11 0b                               |
    | adc word [rsp], cx                                              | 66 11 0c 24                            |
    | adc word [rbp], cx                                              | 66 11 4d 00                            |
    | adc word [rsi], cx                                              | 66 11 0e                               |
    | adc word [rdi], cx                                              | 66 11 0f                               |
    | adc word [r8], cx                                               | 66 41 11 08                            |
    | adc word [r9], cx                                               | 66 41 11 09                            |
    | adc word [r10], cx                                              | 66 41 11 0a                            |
    | adc word [r11], cx                                              | 66 41 11 0b                            |
    | adc word [r12], cx                                              | 66 41 11 0c 24                         |
    | adc word [r13], cx                                              | 66 41 11 4d 00                         |
    | adc word [r14], cx                                              | 66 41 11 0e                            |
    | adc word [r15], cx                                              | 66 41 11 0f                            |
    | adc word [rax + 1 * rcx], cx                                    | 66 11 0c 08                            |
    | adc word [rcx + 1 * rcx], cx                                    | 66 11 0c 09                            |
    | adc word [rdx + 1 * rcx], cx                                    | 66 11 0c 0a                            |
    | adc word [rbx + 1 * rcx], cx                                    | 66 11 0c 0b                            |
    | adc word [rsp + 1 * rcx], cx                                    | 66 11 0c 0c                            |
    | adc word [rbp + 1 * rcx], cx                                    | 66 11 4c 0d 00                         |
    | adc word [rsi + 1 * rcx], cx                                    | 66 11 0c 0e                            |
    | adc word [rdi + 1 * rcx], cx                                    | 66 11 0c 0f                            |
    | adc word [r8 + 1 * rcx], cx                                     | 66 41 11 0c 08                         |
    | adc word [r9 + 1 * rcx], cx                                     | 66 41 11 0c 09                         |
    | adc word [r10 + 1 * rcx], cx                                    | 66 41 11 0c 0a                         |
    | adc word [r11 + 1 * rcx], cx                                    | 66 41 11 0c 0b                         |
    | adc word [r12 + 1 * rcx], cx                                    | 66 41 11 0c 0c                         |
    | adc word [r13 + 1 * rcx], cx                                    | 66 41 11 4c 0d 00                      |
    | adc word [r14 + 1 * rcx], cx                                    | 66 41 11 0c 0e                         |
    | adc word [r15 + 1 * rcx], cx                                    | 66 41 11 0c 0f                         |
    | adc word [rax + 1 * rax], cx                                    | 66 11 0c 00                            |
    | adc word [rax + 1 * rdx], cx                                    | 66 11 0c 10                            |
    | adc word [rax + 1 * rbx], cx                                    | 66 11 0c 18                            |
    | adc word [rax + 1 * rbp], cx                                    | 66 11 0c 28                            |
    | adc word [rax + 1 * rsi], cx                                    | 66 11 0c 30                            |
    | adc word [rax + 1 * rdi], cx                                    | 66 11 0c 38                            |
    | adc word [rax + 1 * r8], cx                                     | 66 42 11 0c 00                         |
    | adc word [rax + 1 * r9], cx                                     | 66 42 11 0c 08                         |
    | adc word [rax + 1 * r10], cx                                    | 66 42 11 0c 10                         |
    | adc word [rax + 1 * r11], cx                                    | 66 42 11 0c 18                         |
    | adc word [rax + 1 * r12], cx                                    | 66 42 11 0c 20                         |
    | adc word [rax + 1 * r13], cx                                    | 66 42 11 0c 28                         |
    | adc word [rax + 1 * r14], cx                                    | 66 42 11 0c 30                         |
    | adc word [rax + 1 * r15], cx                                    | 66 42 11 0c 38                         |
    | adc word [rax + 2 * rcx], cx                                    | 66 11 0c 48                            |
    | adc word [rax + 4 * rcx], cx                                    | 66 11 0c 88                            |
    | adc word [rax + 8 * rcx], cx                                    | 66 11 0c c8                            |
    | adc word [r8 + 1 * r9], cx                                      | 66 43 11 0c 08                         |
    | adc word [r8 + 2 * r9], cx                                      | 66 43 11 0c 48                         |
    | adc word [r8 + 4 * r9], cx                                      | 66 43 11 0c 88                         |
    | adc word [r8 + 8 * r9], cx                                      | 66 43 11 0c c8                         |
    | adc word [1 * rcx], cx                                          | 66 11 0c 0d 00 00 00 00                |
    | adc word [2 * rcx], cx                                          | 66 11 0c 4d 00 00 00 00                |
    | adc word [4 * rcx], cx                                          | 66 11 0c 8d 00 00 00 00                |
    | adc word [8 * rcx], cx                                          | 66 11 0c cd 00 00 00 00                |
    | adc word [1 * r9], cx                                           | 66 42 11 0c 0d 00 00 00 00             |
    | adc word [2 * r9], cx                                           | 66 42 11 0c 4d 00 00 00 00             |
    | adc word [4 * r9], cx                                           | 66 42 11 0c 8d 00 00 00 00             |
    | adc word [8 * r9], cx                                           | 66 42 11 0c cd 00 00 00 00             |
    | adc word [r13 + 8 * r12], cx                                    | 66 43 11 4c e5 00                      |
    | adc word [rsp + 4 * r15], cx                                    | 66 42 11 0c bc                         |
    | adc word [rax + 1 * rcx + 0x00], cx                             | 66 11 4c 08 00                         |
    | adc word [rax + 1 * rcx - 0x00], cx                             | 66 11 4c 08 00                         |
    | adc word [rax + 1 * rcx + 0x01], cx                             | 66 11 4c 08 01                         |
    | adc word [rax + 1 * rcx - 0x01], cx                             | 66 11 4c 08 ff                         |
    | adc word [rax + 1 * rcx + 0x00000001], cx                       | 66 11 8c 08 01 00 00 00                |
    | adc word [rax + 1 * rcx - 0x00000001], cx                       | 66 11 8c 08 ff ff ff ff                |
    | adc word [rax + 1 * rcx + 0x7f], cx                             | 66 11 4c 08 7f                         |
    | adc word [rax + 1 * rcx - 0x7f], cx                             | 66 11 4c 08 81                         |
    | adc word [rax + 1 * rcx + 0x80], cx                             | 66 11 8c 08 80 00 00 00                |
    | adc word [rax + 1 * rcx - 0x80], cx                             | 66 11 4c 08 80                         |
    | adc word [rax + 1 * rcx - 0x81], cx                             | 66 11 8c 08 7f ff ff ff                |
    | adc word [rax + 1 * rcx + 0xff], cx                             | 66 11 8c 08 ff 00 00 00                |
    | adc word [rax + 1 * rcx - 0xff], cx                             | 66 11 8c 08 01 ff ff ff                |
    | adc word [rax + 1 * rcx + 0x7fffffff], cx                       | 66 11 8c 08 ff ff ff 7f                |
    | adc word [rax + 1 * rcx - 0x7fffffff], cx                       | 66 11 8c 08 01 00 00 80                |
    | adc word [rax + 1 * rcx - 0x80000000], cx                       | 66 11 8c 08 00 00 00 80                |
    | adc word [r10 + 0x7f], cx                                       | 66 41 11 4a 7f                         |
    | adc word [r10 + 0x80], cx                                       | 66 41 11 8a 80 00 00 00                |
    | adc word [r10 - 0x80], cx                                       | 66 41 11 4a 80                         |
    | adc word [r10 - 0x81], cx                                       | 66 41 11 8a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc word [rel @prev5], cx      | 90 90 90 90 90 66 11 0d f4 ff ff ff    |
    | .prev1: nop; adc word [rel @prev1], cx                          | 90 66 11 0d f8 ff ff ff                |
    | adc word [rel @next1], cx; nop; .next1: nop                     | 66 11 0d 01 00 00 00 90 90             |
    | adc word [rel @next5], cx; nop; nop; nop; nop; nop; .next5: nop | 66 11 0d 05 00 00 00 90 90 90 90 90 90 |
    | adc word [rax], ax                                              | 66 11 00                               |
    | adc word [rax], dx                                              | 66 11 10                               |
    | adc word [rax], bx                                              | 66 11 18                               |
    | adc word [rax], sp                                              | 66 11 20                               |
    | adc word [rax], bp                                              | 66 11 28                               |
    | adc word [rax], si                                              | 66 11 30                               |
    | adc word [rax], di                                              | 66 11 38                               |
    | adc word [rax], r8w                                             | 66 44 11 00                            |
    | adc word [rax], r9w                                             | 66 44 11 08                            |
    | adc word [rax], r10w                                            | 66 44 11 10                            |
    | adc word [rax], r11w                                            | 66 44 11 18                            |
    | adc word [rax], r12w                                            | 66 44 11 20                            |
    | adc word [rax], r13w                                            | 66 44 11 28                            |
    | adc word [rax], r14w                                            | 66 44 11 30                            |
    | adc word [rax], r15w                                            | 66 44 11 38                            |
    | adc word [rcx], dx                                              | 66 11 11                               |
    | adc word [rdx], bx                                              | 66 11 1a                               |
    | adc word [rbx], sp                                              | 66 11 23                               |
    | adc word [rsp], bp                                              | 66 11 2c 24                            |
    | adc word [rbp], si                                              | 66 11 75 00                            |
    | adc word [rsi], di                                              | 66 11 3e                               |
    | adc word [rdi], r8w                                             | 66 44 11 07                            |
    | adc word [r8], r9w                                              | 66 45 11 08                            |
    | adc word [r9], r10w                                             | 66 45 11 11                            |
    | adc word [r10], r11w                                            | 66 45 11 1a                            |
    | adc word [r11], r12w                                            | 66 45 11 23                            |
    | adc word [r12], r13w                                            | 66 45 11 2c 24                         |
    | adc word [r13], r14w                                            | 66 45 11 75 00                         |
    | adc word [r14], r15w                                            | 66 45 11 3e                            |
    | adc word [r15], ax                                              | 66 41 11 07                            |
    | adc word [rcx + 1 * rcx], dx                                    | 66 11 14 09                            |
    | adc word [rdx + 1 * rcx], bx                                    | 66 11 1c 0a                            |
    | adc word [rbx + 1 * rcx], sp                                    | 66 11 24 0b                            |
    | adc word [rsp + 1 * rcx], bp                                    | 66 11 2c 0c                            |
    | adc word [rbp + 1 * rcx], si                                    | 66 11 74 0d 00                         |
    | adc word [rsi + 1 * rcx], di                                    | 66 11 3c 0e                            |
    | adc word [rdi + 1 * rcx], r8w                                   | 66 44 11 04 0f                         |
    | adc word [r8 + 1 * rcx], r9w                                    | 66 45 11 0c 08                         |
    | adc word [r9 + 1 * rcx], r10w                                   | 66 45 11 14 09                         |
    | adc word [r10 + 1 * rcx], r11w                                  | 66 45 11 1c 0a                         |
    | adc word [r11 + 1 * rcx], r12w                                  | 66 45 11 24 0b                         |
    | adc word [r12 + 1 * rcx], r13w                                  | 66 45 11 2c 0c                         |
    | adc word [r13 + 1 * rcx], r14w                                  | 66 45 11 74 0d 00                      |
    | adc word [r14 + 1 * rcx], r15w                                  | 66 45 11 3c 0e                         |
    | adc word [r15 + 1 * rcx], ax                                    | 66 41 11 04 0f                         |
    | adc word [rax + 1 * rdx], dx                                    | 66 11 14 10                            |
    | adc word [rax + 1 * rbx], bx                                    | 66 11 1c 18                            |
    | adc word [rax + 1 * rbp], sp                                    | 66 11 24 28                            |
    | adc word [rax + 1 * rsi], bp                                    | 66 11 2c 30                            |
    | adc word [rax + 1 * rdi], si                                    | 66 11 34 38                            |
    | adc word [rax + 1 * r8], di                                     | 66 42 11 3c 00                         |
    | adc word [rax + 1 * r9], r8w                                    | 66 46 11 04 08                         |
    | adc word [rax + 1 * r10], r9w                                   | 66 46 11 0c 10                         |
    | adc word [rax + 1 * r11], r10w                                  | 66 46 11 14 18                         |
    | adc word [rax + 1 * r12], r11w                                  | 66 46 11 1c 20                         |
    | adc word [rax + 1 * r13], r12w                                  | 66 46 11 24 28                         |
    | adc word [rax + 1 * r14], r13w                                  | 66 46 11 2c 30                         |
    | adc word [rax + 1 * r15], r14w                                  | 66 46 11 34 38                         |
    | adc word [rax + 2 * rcx], r15w                                  | 66 44 11 3c 48                         |
    | adc word [rax + 4 * rcx], ax                                    | 66 11 04 88                            |
    | adc word [r8 + 1 * r9], dx                                      | 66 43 11 14 08                         |
    | adc word [r8 + 2 * r9], bx                                      | 66 43 11 1c 48                         |
    | adc word [r8 + 4 * r9], sp                                      | 66 43 11 24 88                         |
    | adc word [r8 + 8 * r9], bp                                      | 66 43 11 2c c8                         |
    | adc word [1 * rcx], si                                          | 66 11 34 0d 00 00 00 00                |
    | adc word [2 * rcx], di                                          | 66 11 3c 4d 00 00 00 00                |
    | adc word [4 * rcx], r8w                                         | 66 44 11 04 8d 00 00 00 00             |
    | adc word [8 * rcx], r9w                                         | 66 44 11 0c cd 00 00 00 00             |
    | adc word [1 * r9], r10w                                         | 66 46 11 14 0d 00 00 00 00             |
    | adc word [2 * r9], r11w                                         | 66 46 11 1c 4d 00 00 00 00             |
    | adc word [4 * r9], r12w                                         | 66 46 11 24 8d 00 00 00 00             |
    | adc word [8 * r9], r13w                                         | 66 46 11 2c cd 00 00 00 00             |
    | adc word [r13 + 8 * r12], r14w                                  | 66 47 11 74 e5 00                      |
    | adc word [rsp + 4 * r15], r15w                                  | 66 46 11 3c bc                         |
    | adc word [rax + 1 * rcx + 0x00], ax                             | 66 11 44 08 00                         |
    | adc word [rax + 1 * rcx + 0x01], dx                             | 66 11 54 08 01                         |
    | adc word [rax + 1 * rcx - 0x01], bx                             | 66 11 5c 08 ff                         |
    | adc word [rax + 1 * rcx + 0x00000001], sp                       | 66 11 a4 08 01 00 00 00                |
    | adc word [rax + 1 * rcx - 0x00000001], bp                       | 66 11 ac 08 ff ff ff ff                |
    | adc word [rax + 1 * rcx + 0x7f], si                             | 66 11 74 08 7f                         |
    | adc word [rax + 1 * rcx - 0x7f], di                             | 66 11 7c 08 81                         |
    | adc word [rax + 1 * rcx + 0x80], r8w                            | 66 44 11 84 08 80 00 00 00             |
    | adc word [rax + 1 * rcx - 0x80], r9w                            | 66 44 11 4c 08 80                      |
    | adc word [rax + 1 * rcx - 0x81], r10w                           | 66 44 11 94 08 7f ff ff ff             |
    | adc word [rax + 1 * rcx + 0xff], r11w                           | 66 44 11 9c 08 ff 00 00 00             |
    | adc word [rax + 1 * rcx - 0xff], r12w                           | 66 44 11 a4 08 01 ff ff ff             |
    | adc word [rax + 1 * rcx + 0x7fffffff], r13w                     | 66 44 11 ac 08 ff ff ff 7f             |
    | adc word [rax + 1 * rcx - 0x7fffffff], r14w                     | 66 44 11 b4 08 01 00 00 80             |
    | adc word [rax + 1 * rcx - 0x80000000], r15w                     | 66 44 11 bc 08 00 00 00 80             |
    | adc word [r10 + 0x7f], ax                                       | 66 41 11 42 7f                         |
    | adc word [r10 - 0x80], dx                                       | 66 41 11 52 80                         |
    | adc word [r10 - 0x81], bx                                       | 66 41 11 9a 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; adc word [rel @prev5], sp      | 90 90 90 90 90 66 11 25 f4 ff ff ff    |
    | .prev1: nop; adc word [rel @prev1], bp                          | 90 66 11 2d f8 ff ff ff                |
    | adc word [rel @next1], si; nop; .next1: nop                     | 66 11 35 01 00 00 00 90 90             |
    | adc word [rel @next5], di; nop; nop; nop; nop; nop; .next5: nop | 66 11 3d 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_adc_addr16_reg16():
    encode(ADC_ADDR16_REG16)


ADC_ADDR8_IMM8 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | adc byte [rax], 0x01                                              | 80 10 01                               |
    | adc byte [rcx], 0x01                                              | 80 11 01                               |
    | adc byte [rdx], 0x01                                              | 80 12 01                               |
    | adc byte [rbx], 0x01                                              | 80 13 01                               |
    | adc byte [rsp], 0x01                                              | 80 14 24 01                            |
    | adc byte [rbp], 0x01                                              | 80 55 00 01                            |
    | adc byte [rsi], 0x01                                              | 80 16 01                               |
    | adc byte [rdi], 0x01                                              | 80 17 01                               |
    | adc byte [r8], 0x01                                               | 41 80 10 01                            |
    | adc byte [r9], 0x01                                               | 41 80 11 01                            |
    | adc byte [r10], 0x01                                              | 41 80 12 01                            |
    | adc byte [r11], 0x01                                              | 41 80 13 01                            |
    | adc byte [r12], 0x01                                              | 41 80 14 24 01                         |
    | adc byte [r13], 0x01                                              | 41 80 55 00 01                         |
    | adc byte [r14], 0x01                                              | 41 80 16 01                            |
    | adc byte [r15], 0x01                                              | 41 80 17 01                            |
    | adc byte [rax + 1 * rcx], 0x01                                    | 80 14 08 01                            |
    | adc byte [rcx + 1 * rcx], 0x01                                    | 80 14 09 01                            |
    | adc byte [rdx + 1 * rcx], 0x01                                    | 80 14 0a 01                            |
    | adc byte [rbx + 1 * rcx], 0x01                                    | 80 14 0b 01                            |
    | adc byte [rsp + 1 * rcx], 0x01                                    | 80 14 0c 01                            |
    | adc byte [rbp + 1 * rcx], 0x01                                    | 80 54 0d 00 01                         |
    | adc byte [rsi + 1 * rcx], 0x01                                    | 80 14 0e 01                            |
    | adc byte [rdi + 1 * rcx], 0x01                                    | 80 14 0f 01                            |
    | adc byte [r8 + 1 * rcx], 0x01                                     | 41 80 14 08 01                         |
    | adc byte [r9 + 1 * rcx], 0x01                                     | 41 80 14 09 01                         |
    | adc byte [r10 + 1 * rcx], 0x01                                    | 41 80 14 0a 01                         |
    | adc byte [r11 + 1 * rcx], 0x01                                    | 41 80 14 0b 01                         |
    | adc byte [r12 + 1 * rcx], 0x01                                    | 41 80 14 0c 01                         |
    | adc byte [r13 + 1 * rcx], 0x01                                    | 41 80 54 0d 00 01                      |
    | adc byte [r14 + 1 * rcx], 0x01                                    | 41 80 14 0e 01                         |
    | adc byte [r15 + 1 * rcx], 0x01                                    | 41 80 14 0f 01                         |
    | adc byte [rax + 1 * rax], 0x01                                    | 80 14 00 01                            |
    | adc byte [rax + 1 * rdx], 0x01                                    | 80 14 10 01                            |
    | adc byte [rax + 1 * rbx], 0x01                                    | 80 14 18 01                            |
    | adc byte [rax + 1 * rbp], 0x01                                    | 80 14 28 01                            |
    | adc byte [rax + 1 * rsi], 0x01                                    | 80 14 30 01                            |
    | adc byte [rax + 1 * rdi], 0x01                                    | 80 14 38 01                            |
    | adc byte [rax + 1 * r8], 0x01                                     | 42 80 14 00 01                         |
    | adc byte [rax + 1 * r9], 0x01                                     | 42 80 14 08 01                         |
    | adc byte [rax + 1 * r10], 0x01                                    | 42 80 14 10 01                         |
    | adc byte [rax + 1 * r11], 0x01                                    | 42 80 14 18 01                         |
    | adc byte [rax + 1 * r12], 0x01                                    | 42 80 14 20 01                         |
    | adc byte [rax + 1 * r13], 0x01                                    | 42 80 14 28 01                         |
    | adc byte [rax + 1 * r14], 0x01                                    | 42 80 14 30 01                         |
    | adc byte [rax + 1 * r15], 0x01                                    | 42 80 14 38 01                         |
    | adc byte [rax + 2 * rcx], 0x01                                    | 80 14 48 01                            |
    | adc byte [rax + 4 * rcx], 0x01                                    | 80 14 88 01                            |
    | adc byte [rax + 8 * rcx], 0x01                                    | 80 14 c8 01                            |
    | adc byte [r8 + 1 * r9], 0x01                                      | 43 80 14 08 01                         |
    | adc byte [r8 + 2 * r9], 0x01                                      | 43 80 14 48 01                         |
    | adc byte [r8 + 4 * r9], 0x01                                      | 43 80 14 88 01                         |
    | adc byte [r8 + 8 * r9], 0x01                                      | 43 80 14 c8 01                         |
    | adc byte [1 * rcx], 0x01                                          | 80 14 0d 00 00 00 00 01                |
    | adc byte [2 * rcx], 0x01                                          | 80 14 4d 00 00 00 00 01                |
    | adc byte [4 * rcx], 0x01                                          | 80 14 8d 00 00 00 00 01                |
    | adc byte [8 * rcx], 0x01                                          | 80 14 cd 00 00 00 00 01                |
    | adc byte [1 * r9], 0x01                                           | 42 80 14 0d 00 00 00 00 01             |
    | adc byte [2 * r9], 0x01                                           | 42 80 14 4d 00 00 00 00 01             |
    | adc byte [4 * r9], 0x01                                           | 42 80 14 8d 00 00 00 00 01             |
    | adc byte [8 * r9], 0x01                                           | 42 80 14 cd 00 00 00 00 01             |
    | adc byte [r13 + 8 * r12], 0x01                                    | 43 80 54 e5 00 01                      |
    | adc byte [rsp + 4 * r15], 0x01                                    | 42 80 14 bc 01                         |
    | adc byte [rax + 1 * rcx + 0x00], 0x01                             | 80 54 08 00 01                         |
    | adc byte [rax + 1 * rcx - 0x00], 0x01                             | 80 54 08 00 01                         |
    | adc byte [rax + 1 * rcx + 0x01], 0x01                             | 80 54 08 01 01                         |
    | adc byte [rax + 1 * rcx - 0x01], 0x01                             | 80 54 08 ff 01                         |
    | adc byte [rax + 1 * rcx + 0x00000001], 0x01                       | 80 94 08 01 00 00 00 01                |
    | adc byte [rax + 1 * rcx - 0x00000001], 0x01                       | 80 94 08 ff ff ff ff 01                |
    | adc byte [rax + 1 * rcx + 0x7f], 0x01                             | 80 54 08 7f 01                         |
    | adc byte [rax + 1 * rcx - 0x7f], 0x01                             | 80 54 08 81 01                         |
    | adc byte [rax + 1 * rcx + 0x80], 0x01                             | 80 94 08 80 00 00 00 01                |
    | adc byte [rax + 1 * rcx - 0x80], 0x01                             | 80 54 08 80 01                         |
    | adc byte [rax + 1 * rcx - 0x81], 0x01                             | 80 94 08 7f ff ff ff 01                |
    | adc byte [rax + 1 * rcx + 0xff], 0x01                             | 80 94 08 ff 00 00 00 01                |
    | adc byte [rax + 1 * rcx - 0xff], 0x01                             | 80 94 08 01 ff ff ff 01                |
    | adc byte [rax + 1 * rcx + 0x7fffffff], 0x01                       | 80 94 08 ff ff ff 7f 01                |
    | adc byte [rax + 1 * rcx - 0x7fffffff], 0x01                       | 80 94 08 01 00 00 80 01                |
    | adc byte [rax + 1 * rcx - 0x80000000], 0x01                       | 80 94 08 00 00 00 80 01                |
    | adc byte [r10 + 0x7f], 0x01                                       | 41 80 52 7f 01                         |
    | adc byte [r10 + 0x80], 0x01                                       | 41 80 92 80 00 00 00 01                |
    | adc byte [r10 - 0x80], 0x01                                       | 41 80 52 80 01                         |
    | adc byte [r10 - 0x81], 0x01                                       | 41 80 92 7f ff ff ff 01                |
    | .prev5: nop; nop; nop; nop; nop; adc byte [rel @prev5], 0x01      | 90 90 90 90 90 80 15 f4 ff ff ff 01    |
    | .prev1: nop; adc byte [rel @prev1], 0x01                          | 90 80 15 f8 ff ff ff 01                |
    | adc byte [rel @next1], 0x01; nop; .next1: nop                     | 80 15 01 00 00 00 01 90 90             |
    | adc byte [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 80 15 05 00 00 00 01 90 90 90 90 90 90 |
    | adc byte [rax], 0x00                                              | 80 10 00                               |
    | adc byte [rax], 0x7f                                              | 80 10 7f                               |
    | adc byte [rax], 0x80                                              | 80 10 80                               |
    | adc byte [rax], 0xff                                              | 80 10 ff                               |
    | adc byte [rcx], 0x7f                                              | 80 11 7f                               |
    | adc byte [rdx], 0x80                                              | 80 12 80                               |
    | adc byte [rbx], 0xff                                              | 80 13 ff                               |
    | adc byte [rsp], 0x00                                              | 80 14 24 00                            |
    | adc byte [rsi], 0x7f                                              | 80 16 7f                               |
    | adc byte [rdi], 0x80                                              | 80 17 80                               |
    | adc byte [r8], 0xff                                               | 41 80 10 ff                            |
    | adc byte [r9], 0x00                                               | 41 80 11 00                            |
    | adc byte [r11], 0x7f                                              | 41 80 13 7f                            |
    | adc byte [r12], 0x80                                              | 41 80 14 24 80                         |
    | adc byte [r13], 0xff                                              | 41 80 55 00 ff                         |
    | adc byte [r14], 0x00                                              | 41 80 16 00                            |
    | adc byte [rax + 1 * rcx], 0x7f                                    | 80 14 08 7f                            |
    | adc byte [rcx + 1 * rcx], 0x80                                    | 80 14 09 80                            |
    | adc byte [rdx + 1 * rcx], 0xff                                    | 80 14 0a ff                            |
    | adc byte [rbx + 1 * rcx], 0x00                                    | 80 14 0b 00                            |
    | adc byte [rbp + 1 * rcx], 0x7f                                    | 80 54 0d 00 7f                         |
    | adc byte [rsi + 1 * rcx], 0x80                                    | 80 14 0e 80                            |
    | adc byte [rdi + 1 * rcx], 0xff                                    | 80 14 0f ff                            |
    | adc byte [r8 + 1 * rcx], 0x00                                     | 41 80 14 08 00                         |
    | adc byte [r10 + 1 * rcx], 0x7f                                    | 41 80 14 0a 7f                         |
    | adc byte [r11 + 1 * rcx], 0x80                                    | 41 80 14 0b 80                         |
    | adc byte [r12 + 1 * rcx], 0xff                                    | 41 80 14 0c ff                         |
    | adc byte [r13 + 1 * rcx], 0x00                                    | 41 80 54 0d 00 00                      |
    | adc byte [r15 + 1 * rcx], 0x7f                                    | 41 80 14 0f 7f                         |
    | adc byte [rax + 1 * rax], 0x80                                    | 80 14 00 80                            |
    | adc byte [rax + 1 * rdx], 0xff                                    | 80 14 10 ff                            |
    | adc byte [rax + 1 * rbx], 0x00                                    | 80 14 18 00                            |
    | adc byte [rax + 1 * rsi], 0x7f                                    | 80 14 30 7f                            |
    | adc byte [rax + 1 * rdi], 0x80                                    | 80 14 38 80                            |
    | adc byte [rax + 1 * r8], 0xff                                     | 42 80 14 00 ff                         |
    | adc byte [rax + 1 * r9], 0x00                                     | 42 80 14 08 00                         |
    | adc byte [rax + 1 * r11], 0x7f                                    | 42 80 14 18 7f                         |
    | adc byte [rax + 1 * r12], 0x80                                    | 42 80 14 20 80                         |
    | adc byte [rax + 1 * r13], 0xff                                    | 42 80 14 28 ff                         |
    | adc byte [rax + 1 * r14], 0x00                                    | 42 80 14 30 00                         |
    | adc byte [rax + 2 * rcx], 0x7f                                    | 80 14 48 7f                            |
    | adc byte [rax + 4 * rcx], 0x80                                    | 80 14 88 80                            |
    | adc byte [rax + 8 * rcx], 0xff                                    | 80 14 c8 ff                            |
    | adc byte [r8 + 1 * r9], 0x00                                      | 43 80 14 08 00                         |
    | adc byte [r8 + 4 * r9], 0x7f                                      | 43 80 14 88 7f                         |
    | adc byte [r8 + 8 * r9], 0x80                                      | 43 80 14 c8 80                         |
    | adc byte [1 * rcx], 0xff                                          | 80 14 0d 00 00 00 00 ff                |
    | adc byte [2 * rcx], 0x00                                          | 80 14 4d 00 00 00 00 00                |
    | adc byte [8 * rcx], 0x7f                                          | 80 14 cd 00 00 00 00 7f                |
    | adc byte [1 * r9], 0x80                                           | 42 80 14 0d 00 00 00 00 80             |
    | adc byte [2 * r9], 0xff                                           | 42 80 14 4d 00 00 00 00 ff             |
    | adc byte [4 * r9], 0x00                                           | 42 80 14 8d 00 00 00 00 00             |
    | adc byte [r13 + 8 * r12], 0x7f                                    | 43 80 54 e5 00 7f                      |
    | adc byte [rsp + 4 * r15], 0x80                                    | 42 80 14 bc 80                         |
    | adc byte [rax + 1 * rcx + 0x00], 0xff                             | 80 54 08 00 ff                         |
    | adc byte [rax + 1 * rcx - 0x00], 0x00                             | 80 54 08 00 00                         |
    | adc byte [rax + 1 * rcx - 0x01], 0x7f                             | 80 54 08 ff 7f                         |
    | adc byte [rax + 1 * rcx + 0x00000001], 0x80                       | 80 94 08 01 00 00 00 80                |
    | adc byte [rax + 1 * rcx - 0x00000001], 0xff                       | 80 94 08 ff ff ff ff ff                |
    | adc byte [rax + 1 * rcx + 0x7f], 0x00                             | 80 54 08 7f 00                         |
    | adc byte [rax + 1 * rcx + 0x80], 0x7f                             | 80 94 08 80 00 00 00 7f                |
    | adc byte [rax + 1 * rcx - 0x80], 0x80                             | 80 54 08 80 80                         |
    | adc byte [rax + 1 * rcx - 0x81], 0xff                             | 80 94 08 7f ff ff ff ff                |
    | adc byte [rax + 1 * rcx + 0xff], 0x00                             | 80 94 08 ff 00 00 00 00                |
    | adc byte [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 80 94 08 ff ff ff 7f 7f                |
    | adc byte [rax + 1 * rcx - 0x7fffffff], 0x80                       | 80 94 08 01 00 00 80 80                |
    | adc byte [rax + 1 * rcx - 0x80000000], 0xff                       | 80 94 08 00 00 00 80 ff                |
    | adc byte [r10 + 0x7f], 0x00                                       | 41 80 52 7f 00                         |
    | adc byte [r10 - 0x80], 0x7f                                       | 41 80 52 80 7f                         |
    | adc byte [r10 - 0x81], 0x80                                       | 41 80 92 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; adc byte [rel @prev5], 0xff      | 90 90 90 90 90 80 15 f4 ff ff ff ff    |
    | .prev1: nop; adc byte [rel @prev1], 0x00                          | 90 80 15 f8 ff ff ff 00                |
    | adc byte [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 80 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_adc_addr8_imm8():
    encode(ADC_ADDR8_IMM8)


ADC_ADDR8_REG8 = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | adc byte [rax], cl                                               | 10 08                                  |
    | adc byte [rcx], cl                                               | 10 09                                  |
    | adc byte [rdx], cl                                               | 10 0a                                  |
    | adc byte [rbx], cl                                               | 10 0b                                  |
    | adc byte [rsp], cl                                               | 10 0c 24                               |
    | adc byte [rbp], cl                                               | 10 4d 00                               |
    | adc byte [rsi], cl                                               | 10 0e                                  |
    | adc byte [rdi], cl                                               | 10 0f                                  |
    | adc byte [r8], cl                                                | 41 10 08                               |
    | adc byte [r9], cl                                                | 41 10 09                               |
    | adc byte [r10], cl                                               | 41 10 0a                               |
    | adc byte [r11], cl                                               | 41 10 0b                               |
    | adc byte [r12], cl                                               | 41 10 0c 24                            |
    | adc byte [r13], cl                                               | 41 10 4d 00                            |
    | adc byte [r14], cl                                               | 41 10 0e                               |
    | adc byte [r15], cl                                               | 41 10 0f                               |
    | adc byte [rax + 1 * rcx], cl                                     | 10 0c 08                               |
    | adc byte [rcx + 1 * rcx], cl                                     | 10 0c 09                               |
    | adc byte [rdx + 1 * rcx], cl                                     | 10 0c 0a                               |
    | adc byte [rbx + 1 * rcx], cl                                     | 10 0c 0b                               |
    | adc byte [rsp + 1 * rcx], cl                                     | 10 0c 0c                               |
    | adc byte [rbp + 1 * rcx], cl                                     | 10 4c 0d 00                            |
    | adc byte [rsi + 1 * rcx], cl                                     | 10 0c 0e                               |
    | adc byte [rdi + 1 * rcx], cl                                     | 10 0c 0f                               |
    | adc byte [r8 + 1 * rcx], cl                                      | 41 10 0c 08                            |
    | adc byte [r9 + 1 * rcx], cl                                      | 41 10 0c 09                            |
    | adc byte [r10 + 1 * rcx], cl                                     | 41 10 0c 0a                            |
    | adc byte [r11 + 1 * rcx], cl                                     | 41 10 0c 0b                            |
    | adc byte [r12 + 1 * rcx], cl                                     | 41 10 0c 0c                            |
    | adc byte [r13 + 1 * rcx], cl                                     | 41 10 4c 0d 00                         |
    | adc byte [r14 + 1 * rcx], cl                                     | 41 10 0c 0e                            |
    | adc byte [r15 + 1 * rcx], cl                                     | 41 10 0c 0f                            |
    | adc byte [rax + 1 * rax], cl                                     | 10 0c 00                               |
    | adc byte [rax + 1 * rdx], cl                                     | 10 0c 10                               |
    | adc byte [rax + 1 * rbx], cl                                     | 10 0c 18                               |
    | adc byte [rax + 1 * rbp], cl                                     | 10 0c 28                               |
    | adc byte [rax + 1 * rsi], cl                                     | 10 0c 30                               |
    | adc byte [rax + 1 * rdi], cl                                     | 10 0c 38                               |
    | adc byte [rax + 1 * r8], cl                                      | 42 10 0c 00                            |
    | adc byte [rax + 1 * r9], cl                                      | 42 10 0c 08                            |
    | adc byte [rax + 1 * r10], cl                                     | 42 10 0c 10                            |
    | adc byte [rax + 1 * r11], cl                                     | 42 10 0c 18                            |
    | adc byte [rax + 1 * r12], cl                                     | 42 10 0c 20                            |
    | adc byte [rax + 1 * r13], cl                                     | 42 10 0c 28                            |
    | adc byte [rax + 1 * r14], cl                                     | 42 10 0c 30                            |
    | adc byte [rax + 1 * r15], cl                                     | 42 10 0c 38                            |
    | adc byte [rax + 2 * rcx], cl                                     | 10 0c 48                               |
    | adc byte [rax + 4 * rcx], cl                                     | 10 0c 88                               |
    | adc byte [rax + 8 * rcx], cl                                     | 10 0c c8                               |
    | adc byte [r8 + 1 * r9], cl                                       | 43 10 0c 08                            |
    | adc byte [r8 + 2 * r9], cl                                       | 43 10 0c 48                            |
    | adc byte [r8 + 4 * r9], cl                                       | 43 10 0c 88                            |
    | adc byte [r8 + 8 * r9], cl                                       | 43 10 0c c8                            |
    | adc byte [1 * rcx], cl                                           | 10 0c 0d 00 00 00 00                   |
    | adc byte [2 * rcx], cl                                           | 10 0c 4d 00 00 00 00                   |
    | adc byte [4 * rcx], cl                                           | 10 0c 8d 00 00 00 00                   |
    | adc byte [8 * rcx], cl                                           | 10 0c cd 00 00 00 00                   |
    | adc byte [1 * r9], cl                                            | 42 10 0c 0d 00 00 00 00                |
    | adc byte [2 * r9], cl                                            | 42 10 0c 4d 00 00 00 00                |
    | adc byte [4 * r9], cl                                            | 42 10 0c 8d 00 00 00 00                |
    | adc byte [8 * r9], cl                                            | 42 10 0c cd 00 00 00 00                |
    | adc byte [r13 + 8 * r12], cl                                     | 43 10 4c e5 00                         |
    | adc byte [rsp + 4 * r15], cl                                     | 42 10 0c bc                            |
    | adc byte [rax + 1 * rcx + 0x00], cl                              | 10 4c 08 00                            |
    | adc byte [rax + 1 * rcx - 0x00], cl                              | 10 4c 08 00                            |
    | adc byte [rax + 1 * rcx + 0x01], cl                              | 10 4c 08 01                            |
    | adc byte [rax + 1 * rcx - 0x01], cl                              | 10 4c 08 ff                            |
    | adc byte [rax + 1 * rcx + 0x00000001], cl                        | 10 8c 08 01 00 00 00                   |
    | adc byte [rax + 1 * rcx - 0x00000001], cl                        | 10 8c 08 ff ff ff ff                   |
    | adc byte [rax + 1 * rcx + 0x7f], cl                              | 10 4c 08 7f                            |
    | adc byte [rax + 1 * rcx - 0x7f], cl                              | 10 4c 08 81                            |
    | adc byte [rax + 1 * rcx + 0x80], cl                              | 10 8c 08 80 00 00 00                   |
    | adc byte [rax + 1 * rcx - 0x80], cl                              | 10 4c 08 80                            |
    | adc byte [rax + 1 * rcx - 0x81], cl                              | 10 8c 08 7f ff ff ff                   |
    | adc byte [rax + 1 * rcx + 0xff], cl                              | 10 8c 08 ff 00 00 00                   |
    | adc byte [rax + 1 * rcx - 0xff], cl                              | 10 8c 08 01 ff ff ff                   |
    | adc byte [rax + 1 * rcx + 0x7fffffff], cl                        | 10 8c 08 ff ff ff 7f                   |
    | adc byte [rax + 1 * rcx - 0x7fffffff], cl                        | 10 8c 08 01 00 00 80                   |
    | adc byte [rax + 1 * rcx - 0x80000000], cl                        | 10 8c 08 00 00 00 80                   |
    | adc byte [r10 + 0x7f], cl                                        | 41 10 4a 7f                            |
    | adc byte [r10 + 0x80], cl                                        | 41 10 8a 80 00 00 00                   |
    | adc byte [r10 - 0x80], cl                                        | 41 10 4a 80                            |
    | adc byte [r10 - 0x81], cl                                        | 41 10 8a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc byte [rel @prev5], cl       | 90 90 90 90 90 10 0d f5 ff ff ff       |
    | .prev1: nop; adc byte [rel @prev1], cl                           | 90 10 0d f9 ff ff ff                   |
    | adc byte [rel @next1], cl; nop; .next1: nop                      | 10 0d 01 00 00 00 90 90                |
    | adc byte [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop  | 10 0d 05 00 00 00 90 90 90 90 90 90    |
    | adc byte [rax], al                                               | 10 00                                  |
    | adc byte [rax], dl                                               | 10 10                                  |
    | adc byte [rax], bl                                               | 10 18                                  |
    | adc byte [rax], spl                                              | 40 10 20                               |
    | adc byte [rax], bpl                                              | 40 10 28                               |
    | adc byte [rax], sil                                              | 40 10 30                               |
    | adc byte [rax], dil                                              | 40 10 38                               |
    | adc byte [rax], r8b                                              | 44 10 00                               |
    | adc byte [rax], r9b                                              | 44 10 08                               |
    | adc byte [rax], r10b                                             | 44 10 10                               |
    | adc byte [rax], r11b                                             | 44 10 18                               |
    | adc byte [rax], r12b                                             | 44 10 20                               |
    | adc byte [rax], r13b                                             | 44 10 28                               |
    | adc byte [rax], r14b                                             | 44 10 30                               |
    | adc byte [rax], r15b                                             | 44 10 38                               |
    | adc byte [rax], ah                                               | 10 20                                  |
    | adc byte [rax], ch                                               | 10 28                                  |
    | adc byte [rax], dh                                               | 10 30                                  |
    | adc byte [rax], bh                                               | 10 38                                  |
    | adc byte [rcx], dl                                               | 10 11                                  |
    | adc byte [rdx], bl                                               | 10 1a                                  |
    | adc byte [rbx], spl                                              | 40 10 23                               |
    | adc byte [rsp], bpl                                              | 40 10 2c 24                            |
    | adc byte [rbp], sil                                              | 40 10 75 00                            |
    | adc byte [rsi], dil                                              | 40 10 3e                               |
    | adc byte [rdi], r8b                                              | 44 10 07                               |
    | adc byte [r8], r9b                                               | 45 10 08                               |
    | adc byte [r9], r10b                                              | 45 10 11                               |
    | adc byte [r10], r11b                                             | 45 10 1a                               |
    | adc byte [r11], r12b                                             | 45 10 23                               |
    | adc byte [r12], r13b                                             | 45 10 2c 24                            |
    | adc byte [r13], r14b                                             | 45 10 75 00                            |
    | adc byte [r14], r15b                                             | 45 10 3e                               |
    | adc byte [r15], ah                                               | !! !! !!                               |
    | adc byte [rax + 1 * rcx], ch                                     | 10 2c 08                               |
    | adc byte [rcx + 1 * rcx], dh                                     | 10 34 09                               |
    | adc byte [rdx + 1 * rcx], bh                                     | 10 3c 0a                               |
    | adc byte [rbx + 1 * rcx], al                                     | 10 04 0b                               |
    | adc byte [rbp + 1 * rcx], dl                                     | 10 54 0d 00                            |
    | adc byte [rsi + 1 * rcx], bl                                     | 10 1c 0e                               |
    | adc byte [rdi + 1 * rcx], spl                                    | 40 10 24 0f                            |
    | adc byte [r8 + 1 * rcx], bpl                                     | 41 10 2c 08                            |
    | adc byte [r9 + 1 * rcx], sil                                     | 41 10 34 09                            |
    | adc byte [r10 + 1 * rcx], dil                                    | 41 10 3c 0a                            |
    | adc byte [r11 + 1 * rcx], r8b                                    | 45 10 04 0b                            |
    | adc byte [r12 + 1 * rcx], r9b                                    | 45 10 0c 0c                            |
    | adc byte [r13 + 1 * rcx], r10b                                   | 45 10 54 0d 00                         |
    | adc byte [r14 + 1 * rcx], r11b                                   | 45 10 1c 0e                            |
    | adc byte [r15 + 1 * rcx], r12b                                   | 45 10 24 0f                            |
    | adc byte [rax + 1 * rax], r13b                                   | 44 10 2c 00                            |
    | adc byte [rax + 1 * rdx], r14b                                   | 44 10 34 10                            |
    | adc byte [rax + 1 * rbx], r15b                                   | 44 10 3c 18                            |
    | adc byte [rax + 1 * rbp], ah                                     | 10 24 28                               |
    | adc byte [rax + 1 * rsi], ch                                     | 10 2c 30                               |
    | adc byte [rax + 1 * rdi], dh                                     | 10 34 38                               |
    | adc byte [rax + 1 * r8], bh                                      | !! !! !!                               |
    | adc byte [rax + 1 * r9], al                                      | 42 10 04 08                            |
    | adc byte [rax + 1 * r11], dl                                     | 42 10 14 18                            |
    | adc byte [rax + 1 * r12], bl                                     | 42 10 1c 20                            |
    | adc byte [rax + 1 * r13], spl                                    | 42 10 24 28                            |
    | adc byte [rax + 1 * r14], bpl                                    | 42 10 2c 30                            |
    | adc byte [rax + 1 * r15], sil                                    | 42 10 34 38                            |
    | adc byte [rax + 2 * rcx], dil                                    | 40 10 3c 48                            |
    | adc byte [rax + 4 * rcx], r8b                                    | 44 10 04 88                            |
    | adc byte [rax + 8 * rcx], r9b                                    | 44 10 0c c8                            |
    | adc byte [r8 + 1 * r9], r10b                                     | 47 10 14 08                            |
    | adc byte [r8 + 2 * r9], r11b                                     | 47 10 1c 48                            |
    | adc byte [r8 + 4 * r9], r12b                                     | 47 10 24 88                            |
    | adc byte [r8 + 8 * r9], r13b                                     | 47 10 2c c8                            |
    | adc byte [1 * rcx], r14b                                         | 44 10 34 0d 00 00 00 00                |
    | adc byte [2 * rcx], r15b                                         | 44 10 3c 4d 00 00 00 00                |
    | adc byte [4 * rcx], ah                                           | 10 24 8d 00 00 00 00                   |
    | adc byte [8 * rcx], ch                                           | 10 2c cd 00 00 00 00                   |
    | adc byte [1 * r9], dh                                            | !! !! !!                               |
    | adc byte [2 * r9], bh                                            | !! !! !!                               |
    | adc byte [4 * r9], al                                            | 42 10 04 8d 00 00 00 00                |
    | adc byte [r13 + 8 * r12], dl                                     | 43 10 54 e5 00                         |
    | adc byte [rsp + 4 * r15], bl                                     | 42 10 1c bc                            |
    | adc byte [rax + 1 * rcx + 0x00], spl                             | 40 10 64 08 00                         |
    | adc byte [rax + 1 * rcx - 0x00], bpl                             | 40 10 6c 08 00                         |
    | adc byte [rax + 1 * rcx + 0x01], sil                             | 40 10 74 08 01                         |
    | adc byte [rax + 1 * rcx - 0x01], dil                             | 40 10 7c 08 ff                         |
    | adc byte [rax + 1 * rcx + 0x00000001], r8b                       | 44 10 84 08 01 00 00 00                |
    | adc byte [rax + 1 * rcx - 0x00000001], r9b                       | 44 10 8c 08 ff ff ff ff                |
    | adc byte [rax + 1 * rcx + 0x7f], r10b                            | 44 10 54 08 7f                         |
    | adc byte [rax + 1 * rcx - 0x7f], r11b                            | 44 10 5c 08 81                         |
    | adc byte [rax + 1 * rcx + 0x80], r12b                            | 44 10 a4 08 80 00 00 00                |
    | adc byte [rax + 1 * rcx - 0x80], r13b                            | 44 10 6c 08 80                         |
    | adc byte [rax + 1 * rcx - 0x81], r14b                            | 44 10 b4 08 7f ff ff ff                |
    | adc byte [rax + 1 * rcx + 0xff], r15b                            | 44 10 bc 08 ff 00 00 00                |
    | adc byte [rax + 1 * rcx - 0xff], ah                              | 10 a4 08 01 ff ff ff                   |
    | adc byte [rax + 1 * rcx + 0x7fffffff], ch                        | 10 ac 08 ff ff ff 7f                   |
    | adc byte [rax + 1 * rcx - 0x7fffffff], dh                        | 10 b4 08 01 00 00 80                   |
    | adc byte [rax + 1 * rcx - 0x80000000], bh                        | 10 bc 08 00 00 00 80                   |
    | adc byte [r10 + 0x7f], al                                        | 41 10 42 7f                            |
    | adc byte [r10 - 0x80], dl                                        | 41 10 52 80                            |
    | adc byte [r10 - 0x81], bl                                        | 41 10 9a 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; adc byte [rel @prev5], spl      | 90 90 90 90 90 40 10 25 f4 ff ff ff    |
    | .prev1: nop; adc byte [rel @prev1], bpl                          | 90 40 10 2d f8 ff ff ff                |
    | adc byte [rel @next1], sil; nop; .next1: nop                     | 40 10 35 01 00 00 00 90 90             |
    | adc byte [rel @next5], dil; nop; nop; nop; nop; nop; .next5: nop | 40 10 3d 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_adc_addr8_reg8():
    encode(ADC_ADDR8_REG8)
