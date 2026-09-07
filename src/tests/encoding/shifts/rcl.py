from tests.encoding.core import encode, exhaust


def can_exhaust_rcl():
    exhaust(
        RCL_ADDR16_CL,
        RCL_ADDR16_IMM8,
        RCL_ADDR32_CL,
        RCL_ADDR32_IMM8,
        RCL_ADDR64_CL,
        RCL_ADDR64_IMM8,
        RCL_ADDR8_CL,
        RCL_ADDR8_IMM8,
        RCL_REG16_CL,
        RCL_REG16_IMM8,
        RCL_REG32_CL,
        RCL_REG32_IMM8,
        RCL_REG64_CL,
        RCL_REG64_IMM8,
        RCL_REG8_CL,
        RCL_REG8_IMM8,
    )


RCL_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | rcl rax, 0x01 | 48 d1 d0    | *** | rcl rax, 0x00 | 48 c1 d0 00 |
    | rcl rcx, 0x01 | 48 d1 d1    | *** | rcl rax, 0x7f | 48 c1 d0 7f |
    | rcl rdx, 0x01 | 48 d1 d2    | *** | rcl rax, 0x80 | 48 c1 d0 80 |
    | rcl rbx, 0x01 | 48 d1 d3    | *** | rcl rax, 0xff | 48 c1 d0 ff |
    | rcl rsp, 0x01 | 48 d1 d4    | *** | rcl rcx, 0x7f | 48 c1 d1 7f |
    | rcl rbp, 0x01 | 48 d1 d5    | *** | rcl rdx, 0x80 | 48 c1 d2 80 |
    | rcl rsi, 0x01 | 48 d1 d6    | *** | rcl rbx, 0xff | 48 c1 d3 ff |
    | rcl rdi, 0x01 | 48 d1 d7    | *** | rcl rsp, 0x00 | 48 c1 d4 00 |
    | rcl r8, 0x01  | 49 d1 d0    | *** | rcl rsi, 0x7f | 48 c1 d6 7f |
    | rcl r9, 0x01  | 49 d1 d1    | *** | rcl rdi, 0x80 | 48 c1 d7 80 |
    | rcl r10, 0x01 | 49 d1 d2    | *** | rcl r8, 0xff  | 49 c1 d0 ff |
    | rcl r11, 0x01 | 49 d1 d3    | *** | rcl r9, 0x00  | 49 c1 d1 00 |
    | rcl r12, 0x01 | 49 d1 d4    | *** | rcl r11, 0x7f | 49 c1 d3 7f |
    | rcl r13, 0x01 | 49 d1 d5    | *** | rcl r12, 0x80 | 49 c1 d4 80 |
    | rcl r14, 0x01 | 49 d1 d6    | *** | rcl r13, 0xff | 49 c1 d5 ff |
    | rcl r15, 0x01 | 49 d1 d7    | *** | rcl r14, 0x00 | 49 c1 d6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_rcl_reg64_imm8():
    encode(RCL_REG64_IMM8)


RCL_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | rcl rax, cl | 48 d3 d0 | *** | rcl r8, cl  | 49 d3 d0 |
    | rcl rcx, cl | 48 d3 d1 | *** | rcl r9, cl  | 49 d3 d1 |
    | rcl rdx, cl | 48 d3 d2 | *** | rcl r10, cl | 49 d3 d2 |
    | rcl rbx, cl | 48 d3 d3 | *** | rcl r11, cl | 49 d3 d3 |
    | rcl rsp, cl | 48 d3 d4 | *** | rcl r12, cl | 49 d3 d4 |
    | rcl rbp, cl | 48 d3 d5 | *** | rcl r13, cl | 49 d3 d5 |
    | rcl rsi, cl | 48 d3 d6 | *** | rcl r14, cl | 49 d3 d6 |
    | rcl rdi, cl | 48 d3 d7 | *** | rcl r15, cl | 49 d3 d7 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_rcl_reg64_cl():
    encode(RCL_REG64_CL)


RCL_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | rcl eax, 0x01  | d1 d0       | *** | rcl eax, 0x00  | c1 d0 00    |
    | rcl ecx, 0x01  | d1 d1       | *** | rcl eax, 0x7f  | c1 d0 7f    |
    | rcl edx, 0x01  | d1 d2       | *** | rcl eax, 0x80  | c1 d0 80    |
    | rcl ebx, 0x01  | d1 d3       | *** | rcl eax, 0xff  | c1 d0 ff    |
    | rcl esp, 0x01  | d1 d4       | *** | rcl ecx, 0x7f  | c1 d1 7f    |
    | rcl ebp, 0x01  | d1 d5       | *** | rcl edx, 0x80  | c1 d2 80    |
    | rcl esi, 0x01  | d1 d6       | *** | rcl ebx, 0xff  | c1 d3 ff    |
    | rcl edi, 0x01  | d1 d7       | *** | rcl esp, 0x00  | c1 d4 00    |
    | rcl r8d, 0x01  | 41 d1 d0    | *** | rcl esi, 0x7f  | c1 d6 7f    |
    | rcl r9d, 0x01  | 41 d1 d1    | *** | rcl edi, 0x80  | c1 d7 80    |
    | rcl r10d, 0x01 | 41 d1 d2    | *** | rcl r8d, 0xff  | 41 c1 d0 ff |
    | rcl r11d, 0x01 | 41 d1 d3    | *** | rcl r9d, 0x00  | 41 c1 d1 00 |
    | rcl r12d, 0x01 | 41 d1 d4    | *** | rcl r11d, 0x7f | 41 c1 d3 7f |
    | rcl r13d, 0x01 | 41 d1 d5    | *** | rcl r12d, 0x80 | 41 c1 d4 80 |
    | rcl r14d, 0x01 | 41 d1 d6    | *** | rcl r13d, 0xff | 41 c1 d5 ff |
    | rcl r15d, 0x01 | 41 d1 d7    | *** | rcl r14d, 0x00 | 41 c1 d6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_rcl_reg32_imm8():
    encode(RCL_REG32_IMM8)


RCL_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | rcl eax, cl  | d3 d0    | *** | rcl r8d, cl  | 41 d3 d0 |
    | rcl ecx, cl  | d3 d1    | *** | rcl r9d, cl  | 41 d3 d1 |
    | rcl edx, cl  | d3 d2    | *** | rcl r10d, cl | 41 d3 d2 |
    | rcl ebx, cl  | d3 d3    | *** | rcl r11d, cl | 41 d3 d3 |
    | rcl esp, cl  | d3 d4    | *** | rcl r12d, cl | 41 d3 d4 |
    | rcl ebp, cl  | d3 d5    | *** | rcl r13d, cl | 41 d3 d5 |
    | rcl esi, cl  | d3 d6    | *** | rcl r14d, cl | 41 d3 d6 |
    | rcl edi, cl  | d3 d7    | *** | rcl r15d, cl | 41 d3 d7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_rcl_reg32_cl():
    encode(RCL_REG32_CL)


RCL_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | rcl ax, 0x01   | 66 d1 d0       | *** | rcl ax, 0x00   | 66 c1 d0 00    |
    | rcl cx, 0x01   | 66 d1 d1       | *** | rcl ax, 0x7f   | 66 c1 d0 7f    |
    | rcl dx, 0x01   | 66 d1 d2       | *** | rcl ax, 0x80   | 66 c1 d0 80    |
    | rcl bx, 0x01   | 66 d1 d3       | *** | rcl ax, 0xff   | 66 c1 d0 ff    |
    | rcl sp, 0x01   | 66 d1 d4       | *** | rcl cx, 0x7f   | 66 c1 d1 7f    |
    | rcl bp, 0x01   | 66 d1 d5       | *** | rcl dx, 0x80   | 66 c1 d2 80    |
    | rcl si, 0x01   | 66 d1 d6       | *** | rcl bx, 0xff   | 66 c1 d3 ff    |
    | rcl di, 0x01   | 66 d1 d7       | *** | rcl sp, 0x00   | 66 c1 d4 00    |
    | rcl r8w, 0x01  | 66 41 d1 d0    | *** | rcl si, 0x7f   | 66 c1 d6 7f    |
    | rcl r9w, 0x01  | 66 41 d1 d1    | *** | rcl di, 0x80   | 66 c1 d7 80    |
    | rcl r10w, 0x01 | 66 41 d1 d2    | *** | rcl r8w, 0xff  | 66 41 c1 d0 ff |
    | rcl r11w, 0x01 | 66 41 d1 d3    | *** | rcl r9w, 0x00  | 66 41 c1 d1 00 |
    | rcl r12w, 0x01 | 66 41 d1 d4    | *** | rcl r11w, 0x7f | 66 41 c1 d3 7f |
    | rcl r13w, 0x01 | 66 41 d1 d5    | *** | rcl r12w, 0x80 | 66 41 c1 d4 80 |
    | rcl r14w, 0x01 | 66 41 d1 d6    | *** | rcl r13w, 0xff | 66 41 c1 d5 ff |
    | rcl r15w, 0x01 | 66 41 d1 d7    | *** | rcl r14w, 0x00 | 66 41 c1 d6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_rcl_reg16_imm8():
    encode(RCL_REG16_IMM8)


RCL_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | rcl ax, cl   | 66 d3 d0    | *** | rcl r8w, cl  | 66 41 d3 d0 |
    | rcl cx, cl   | 66 d3 d1    | *** | rcl r9w, cl  | 66 41 d3 d1 |
    | rcl dx, cl   | 66 d3 d2    | *** | rcl r10w, cl | 66 41 d3 d2 |
    | rcl bx, cl   | 66 d3 d3    | *** | rcl r11w, cl | 66 41 d3 d3 |
    | rcl sp, cl   | 66 d3 d4    | *** | rcl r12w, cl | 66 41 d3 d4 |
    | rcl bp, cl   | 66 d3 d5    | *** | rcl r13w, cl | 66 41 d3 d5 |
    | rcl si, cl   | 66 d3 d6    | *** | rcl r14w, cl | 66 41 d3 d6 |
    | rcl di, cl   | 66 d3 d7    | *** | rcl r15w, cl | 66 41 d3 d7 |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_rcl_reg16_cl():
    encode(RCL_REG16_CL)


RCL_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | rcl al, 0x01   | d0 d0       | *** | rcl al, 0x00   | c0 d0 00    |
    | rcl cl, 0x01   | d0 d1       | *** | rcl al, 0x7f   | c0 d0 7f    |
    | rcl dl, 0x01   | d0 d2       | *** | rcl al, 0x80   | c0 d0 80    |
    | rcl bl, 0x01   | d0 d3       | *** | rcl al, 0xff   | c0 d0 ff    |
    | rcl spl, 0x01  | 40 d0 d4    | *** | rcl cl, 0x7f   | c0 d1 7f    |
    | rcl bpl, 0x01  | 40 d0 d5    | *** | rcl dl, 0x80   | c0 d2 80    |
    | rcl sil, 0x01  | 40 d0 d6    | *** | rcl bl, 0xff   | c0 d3 ff    |
    | rcl dil, 0x01  | 40 d0 d7    | *** | rcl spl, 0x00  | 40 c0 d4 00 |
    | rcl r8b, 0x01  | 41 d0 d0    | *** | rcl sil, 0x7f  | 40 c0 d6 7f |
    | rcl r9b, 0x01  | 41 d0 d1    | *** | rcl dil, 0x80  | 40 c0 d7 80 |
    | rcl r10b, 0x01 | 41 d0 d2    | *** | rcl r8b, 0xff  | 41 c0 d0 ff |
    | rcl r11b, 0x01 | 41 d0 d3    | *** | rcl r9b, 0x00  | 41 c0 d1 00 |
    | rcl r12b, 0x01 | 41 d0 d4    | *** | rcl r11b, 0x7f | 41 c0 d3 7f |
    | rcl r13b, 0x01 | 41 d0 d5    | *** | rcl r12b, 0x80 | 41 c0 d4 80 |
    | rcl r14b, 0x01 | 41 d0 d6    | *** | rcl r13b, 0xff | 41 c0 d5 ff |
    | rcl r15b, 0x01 | 41 d0 d7    | *** | rcl r14b, 0x00 | 41 c0 d6 00 |
    | rcl ah, 0x01   | d0 d4       | *** | rcl ah, 0x7f   | c0 d4 7f    |
    | rcl ch, 0x01   | d0 d5       | *** | rcl ch, 0x80   | c0 d5 80    |
    | rcl dh, 0x01   | d0 d6       | *** | rcl dh, 0xff   | c0 d6 ff    |
    | rcl bh, 0x01   | d0 d7       | *** | rcl bh, 0x00   | c0 d7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_rcl_reg8_imm8():
    encode(RCL_REG8_IMM8)


RCL_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | rcl al, cl   | d2 d0    | *** | rcl r10b, cl | 41 d2 d2 |
    | rcl cl, cl   | d2 d1    | *** | rcl r11b, cl | 41 d2 d3 |
    | rcl dl, cl   | d2 d2    | *** | rcl r12b, cl | 41 d2 d4 |
    | rcl bl, cl   | d2 d3    | *** | rcl r13b, cl | 41 d2 d5 |
    | rcl spl, cl  | 40 d2 d4 | *** | rcl r14b, cl | 41 d2 d6 |
    | rcl bpl, cl  | 40 d2 d5 | *** | rcl r15b, cl | 41 d2 d7 |
    | rcl sil, cl  | 40 d2 d6 | *** | rcl ah, cl   | d2 d4    |
    | rcl dil, cl  | 40 d2 d7 | *** | rcl ch, cl   | d2 d5    |
    | rcl r8b, cl  | 41 d2 d0 | *** | rcl dh, cl   | d2 d6    |
    | rcl r9b, cl  | 41 d2 d1 | *** | rcl bh, cl   | d2 d7    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_rcl_reg8_cl():
    encode(RCL_REG8_CL)


RCL_ADDR64_IMM8 = """
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | instruction                                                        | encoding                                  |
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | rcl qword [rax], 0x01                                              | 48 d1 10                                  |
    | rcl qword [rcx], 0x01                                              | 48 d1 11                                  |
    | rcl qword [rdx], 0x01                                              | 48 d1 12                                  |
    | rcl qword [rbx], 0x01                                              | 48 d1 13                                  |
    | rcl qword [rsp], 0x01                                              | 48 d1 14 24                               |
    | rcl qword [rbp], 0x01                                              | 48 d1 55 00                               |
    | rcl qword [rsi], 0x01                                              | 48 d1 16                                  |
    | rcl qword [rdi], 0x01                                              | 48 d1 17                                  |
    | rcl qword [r8], 0x01                                               | 49 d1 10                                  |
    | rcl qword [r9], 0x01                                               | 49 d1 11                                  |
    | rcl qword [r10], 0x01                                              | 49 d1 12                                  |
    | rcl qword [r11], 0x01                                              | 49 d1 13                                  |
    | rcl qword [r12], 0x01                                              | 49 d1 14 24                               |
    | rcl qword [r13], 0x01                                              | 49 d1 55 00                               |
    | rcl qword [r14], 0x01                                              | 49 d1 16                                  |
    | rcl qword [r15], 0x01                                              | 49 d1 17                                  |
    | rcl qword [rax + 1 * rcx], 0x01                                    | 48 d1 14 08                               |
    | rcl qword [rcx + 1 * rcx], 0x01                                    | 48 d1 14 09                               |
    | rcl qword [rdx + 1 * rcx], 0x01                                    | 48 d1 14 0a                               |
    | rcl qword [rbx + 1 * rcx], 0x01                                    | 48 d1 14 0b                               |
    | rcl qword [rsp + 1 * rcx], 0x01                                    | 48 d1 14 0c                               |
    | rcl qword [rbp + 1 * rcx], 0x01                                    | 48 d1 54 0d 00                            |
    | rcl qword [rsi + 1 * rcx], 0x01                                    | 48 d1 14 0e                               |
    | rcl qword [rdi + 1 * rcx], 0x01                                    | 48 d1 14 0f                               |
    | rcl qword [r8 + 1 * rcx], 0x01                                     | 49 d1 14 08                               |
    | rcl qword [r9 + 1 * rcx], 0x01                                     | 49 d1 14 09                               |
    | rcl qword [r10 + 1 * rcx], 0x01                                    | 49 d1 14 0a                               |
    | rcl qword [r11 + 1 * rcx], 0x01                                    | 49 d1 14 0b                               |
    | rcl qword [r12 + 1 * rcx], 0x01                                    | 49 d1 14 0c                               |
    | rcl qword [r13 + 1 * rcx], 0x01                                    | 49 d1 54 0d 00                            |
    | rcl qword [r14 + 1 * rcx], 0x01                                    | 49 d1 14 0e                               |
    | rcl qword [r15 + 1 * rcx], 0x01                                    | 49 d1 14 0f                               |
    | rcl qword [rax + 1 * rax], 0x01                                    | 48 d1 14 00                               |
    | rcl qword [rax + 1 * rdx], 0x01                                    | 48 d1 14 10                               |
    | rcl qword [rax + 1 * rbx], 0x01                                    | 48 d1 14 18                               |
    | rcl qword [rax + 1 * rbp], 0x01                                    | 48 d1 14 28                               |
    | rcl qword [rax + 1 * rsi], 0x01                                    | 48 d1 14 30                               |
    | rcl qword [rax + 1 * rdi], 0x01                                    | 48 d1 14 38                               |
    | rcl qword [rax + 1 * r8], 0x01                                     | 4a d1 14 00                               |
    | rcl qword [rax + 1 * r9], 0x01                                     | 4a d1 14 08                               |
    | rcl qword [rax + 1 * r10], 0x01                                    | 4a d1 14 10                               |
    | rcl qword [rax + 1 * r11], 0x01                                    | 4a d1 14 18                               |
    | rcl qword [rax + 1 * r12], 0x01                                    | 4a d1 14 20                               |
    | rcl qword [rax + 1 * r13], 0x01                                    | 4a d1 14 28                               |
    | rcl qword [rax + 1 * r14], 0x01                                    | 4a d1 14 30                               |
    | rcl qword [rax + 1 * r15], 0x01                                    | 4a d1 14 38                               |
    | rcl qword [rax + 2 * rcx], 0x01                                    | 48 d1 14 48                               |
    | rcl qword [rax + 4 * rcx], 0x01                                    | 48 d1 14 88                               |
    | rcl qword [rax + 8 * rcx], 0x01                                    | 48 d1 14 c8                               |
    | rcl qword [r8 + 1 * r9], 0x01                                      | 4b d1 14 08                               |
    | rcl qword [r8 + 2 * r9], 0x01                                      | 4b d1 14 48                               |
    | rcl qword [r8 + 4 * r9], 0x01                                      | 4b d1 14 88                               |
    | rcl qword [r8 + 8 * r9], 0x01                                      | 4b d1 14 c8                               |
    | rcl qword [1 * rcx], 0x01                                          | 48 d1 14 0d 00 00 00 00                   |
    | rcl qword [2 * rcx], 0x01                                          | 48 d1 14 4d 00 00 00 00                   |
    | rcl qword [4 * rcx], 0x01                                          | 48 d1 14 8d 00 00 00 00                   |
    | rcl qword [8 * rcx], 0x01                                          | 48 d1 14 cd 00 00 00 00                   |
    | rcl qword [1 * r9], 0x01                                           | 4a d1 14 0d 00 00 00 00                   |
    | rcl qword [2 * r9], 0x01                                           | 4a d1 14 4d 00 00 00 00                   |
    | rcl qword [4 * r9], 0x01                                           | 4a d1 14 8d 00 00 00 00                   |
    | rcl qword [8 * r9], 0x01                                           | 4a d1 14 cd 00 00 00 00                   |
    | rcl qword [r13 + 8 * r12], 0x01                                    | 4b d1 54 e5 00                            |
    | rcl qword [rsp + 4 * r15], 0x01                                    | 4a d1 14 bc                               |
    | rcl qword [rax + 1 * rcx + 0x00], 0x01                             | 48 d1 54 08 00                            |
    | rcl qword [rax + 1 * rcx - 0x00], 0x01                             | 48 d1 54 08 00                            |
    | rcl qword [rax + 1 * rcx + 0x01], 0x01                             | 48 d1 54 08 01                            |
    | rcl qword [rax + 1 * rcx - 0x01], 0x01                             | 48 d1 54 08 ff                            |
    | rcl qword [rax + 1 * rcx + 0x00000001], 0x01                       | 48 d1 94 08 01 00 00 00                   |
    | rcl qword [rax + 1 * rcx - 0x00000001], 0x01                       | 48 d1 94 08 ff ff ff ff                   |
    | rcl qword [rax + 1 * rcx + 0x7f], 0x01                             | 48 d1 54 08 7f                            |
    | rcl qword [rax + 1 * rcx - 0x7f], 0x01                             | 48 d1 54 08 81                            |
    | rcl qword [rax + 1 * rcx + 0x80], 0x01                             | 48 d1 94 08 80 00 00 00                   |
    | rcl qword [rax + 1 * rcx - 0x80], 0x01                             | 48 d1 54 08 80                            |
    | rcl qword [rax + 1 * rcx - 0x81], 0x01                             | 48 d1 94 08 7f ff ff ff                   |
    | rcl qword [rax + 1 * rcx + 0xff], 0x01                             | 48 d1 94 08 ff 00 00 00                   |
    | rcl qword [rax + 1 * rcx - 0xff], 0x01                             | 48 d1 94 08 01 ff ff ff                   |
    | rcl qword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 48 d1 94 08 ff ff ff 7f                   |
    | rcl qword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 48 d1 94 08 01 00 00 80                   |
    | rcl qword [rax + 1 * rcx - 0x80000000], 0x01                       | 48 d1 94 08 00 00 00 80                   |
    | rcl qword [r10 + 0x7f], 0x01                                       | 49 d1 52 7f                               |
    | rcl qword [r10 + 0x80], 0x01                                       | 49 d1 92 80 00 00 00                      |
    | rcl qword [r10 - 0x80], 0x01                                       | 49 d1 52 80                               |
    | rcl qword [r10 - 0x81], 0x01                                       | 49 d1 92 7f ff ff ff                      |
    | .prev5: nop; nop; nop; nop; nop; rcl qword [rel @prev5], 0x01      | 90 90 90 90 90 48 d1 15 f4 ff ff ff       |
    | .prev1: nop; rcl qword [rel @prev1], 0x01                          | 90 48 d1 15 f8 ff ff ff                   |
    | rcl qword [rel @next1], 0x01; nop; .next1: nop                     | 48 d1 15 01 00 00 00 90 90                |
    | rcl qword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 48 d1 15 05 00 00 00 90 90 90 90 90 90    |
    | rcl qword [rax], 0x00                                              | 48 c1 10 00                               |
    | rcl qword [rax], 0x7f                                              | 48 c1 10 7f                               |
    | rcl qword [rax], 0x80                                              | 48 c1 10 80                               |
    | rcl qword [rax], 0xff                                              | 48 c1 10 ff                               |
    | rcl qword [rcx], 0x7f                                              | 48 c1 11 7f                               |
    | rcl qword [rdx], 0x80                                              | 48 c1 12 80                               |
    | rcl qword [rbx], 0xff                                              | 48 c1 13 ff                               |
    | rcl qword [rsp], 0x00                                              | 48 c1 14 24 00                            |
    | rcl qword [rsi], 0x7f                                              | 48 c1 16 7f                               |
    | rcl qword [rdi], 0x80                                              | 48 c1 17 80                               |
    | rcl qword [r8], 0xff                                               | 49 c1 10 ff                               |
    | rcl qword [r9], 0x00                                               | 49 c1 11 00                               |
    | rcl qword [r11], 0x7f                                              | 49 c1 13 7f                               |
    | rcl qword [r12], 0x80                                              | 49 c1 14 24 80                            |
    | rcl qword [r13], 0xff                                              | 49 c1 55 00 ff                            |
    | rcl qword [r14], 0x00                                              | 49 c1 16 00                               |
    | rcl qword [rax + 1 * rcx], 0x7f                                    | 48 c1 14 08 7f                            |
    | rcl qword [rcx + 1 * rcx], 0x80                                    | 48 c1 14 09 80                            |
    | rcl qword [rdx + 1 * rcx], 0xff                                    | 48 c1 14 0a ff                            |
    | rcl qword [rbx + 1 * rcx], 0x00                                    | 48 c1 14 0b 00                            |
    | rcl qword [rbp + 1 * rcx], 0x7f                                    | 48 c1 54 0d 00 7f                         |
    | rcl qword [rsi + 1 * rcx], 0x80                                    | 48 c1 14 0e 80                            |
    | rcl qword [rdi + 1 * rcx], 0xff                                    | 48 c1 14 0f ff                            |
    | rcl qword [r8 + 1 * rcx], 0x00                                     | 49 c1 14 08 00                            |
    | rcl qword [r10 + 1 * rcx], 0x7f                                    | 49 c1 14 0a 7f                            |
    | rcl qword [r11 + 1 * rcx], 0x80                                    | 49 c1 14 0b 80                            |
    | rcl qword [r12 + 1 * rcx], 0xff                                    | 49 c1 14 0c ff                            |
    | rcl qword [r13 + 1 * rcx], 0x00                                    | 49 c1 54 0d 00 00                         |
    | rcl qword [r15 + 1 * rcx], 0x7f                                    | 49 c1 14 0f 7f                            |
    | rcl qword [rax + 1 * rax], 0x80                                    | 48 c1 14 00 80                            |
    | rcl qword [rax + 1 * rdx], 0xff                                    | 48 c1 14 10 ff                            |
    | rcl qword [rax + 1 * rbx], 0x00                                    | 48 c1 14 18 00                            |
    | rcl qword [rax + 1 * rsi], 0x7f                                    | 48 c1 14 30 7f                            |
    | rcl qword [rax + 1 * rdi], 0x80                                    | 48 c1 14 38 80                            |
    | rcl qword [rax + 1 * r8], 0xff                                     | 4a c1 14 00 ff                            |
    | rcl qword [rax + 1 * r9], 0x00                                     | 4a c1 14 08 00                            |
    | rcl qword [rax + 1 * r11], 0x7f                                    | 4a c1 14 18 7f                            |
    | rcl qword [rax + 1 * r12], 0x80                                    | 4a c1 14 20 80                            |
    | rcl qword [rax + 1 * r13], 0xff                                    | 4a c1 14 28 ff                            |
    | rcl qword [rax + 1 * r14], 0x00                                    | 4a c1 14 30 00                            |
    | rcl qword [rax + 2 * rcx], 0x7f                                    | 48 c1 14 48 7f                            |
    | rcl qword [rax + 4 * rcx], 0x80                                    | 48 c1 14 88 80                            |
    | rcl qword [rax + 8 * rcx], 0xff                                    | 48 c1 14 c8 ff                            |
    | rcl qword [r8 + 1 * r9], 0x00                                      | 4b c1 14 08 00                            |
    | rcl qword [r8 + 4 * r9], 0x7f                                      | 4b c1 14 88 7f                            |
    | rcl qword [r8 + 8 * r9], 0x80                                      | 4b c1 14 c8 80                            |
    | rcl qword [1 * rcx], 0xff                                          | 48 c1 14 0d 00 00 00 00 ff                |
    | rcl qword [2 * rcx], 0x00                                          | 48 c1 14 4d 00 00 00 00 00                |
    | rcl qword [8 * rcx], 0x7f                                          | 48 c1 14 cd 00 00 00 00 7f                |
    | rcl qword [1 * r9], 0x80                                           | 4a c1 14 0d 00 00 00 00 80                |
    | rcl qword [2 * r9], 0xff                                           | 4a c1 14 4d 00 00 00 00 ff                |
    | rcl qword [4 * r9], 0x00                                           | 4a c1 14 8d 00 00 00 00 00                |
    | rcl qword [r13 + 8 * r12], 0x7f                                    | 4b c1 54 e5 00 7f                         |
    | rcl qword [rsp + 4 * r15], 0x80                                    | 4a c1 14 bc 80                            |
    | rcl qword [rax + 1 * rcx + 0x00], 0xff                             | 48 c1 54 08 00 ff                         |
    | rcl qword [rax + 1 * rcx - 0x00], 0x00                             | 48 c1 54 08 00 00                         |
    | rcl qword [rax + 1 * rcx - 0x01], 0x7f                             | 48 c1 54 08 ff 7f                         |
    | rcl qword [rax + 1 * rcx + 0x00000001], 0x80                       | 48 c1 94 08 01 00 00 00 80                |
    | rcl qword [rax + 1 * rcx - 0x00000001], 0xff                       | 48 c1 94 08 ff ff ff ff ff                |
    | rcl qword [rax + 1 * rcx + 0x7f], 0x00                             | 48 c1 54 08 7f 00                         |
    | rcl qword [rax + 1 * rcx + 0x80], 0x7f                             | 48 c1 94 08 80 00 00 00 7f                |
    | rcl qword [rax + 1 * rcx - 0x80], 0x80                             | 48 c1 54 08 80 80                         |
    | rcl qword [rax + 1 * rcx - 0x81], 0xff                             | 48 c1 94 08 7f ff ff ff ff                |
    | rcl qword [rax + 1 * rcx + 0xff], 0x00                             | 48 c1 94 08 ff 00 00 00 00                |
    | rcl qword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 48 c1 94 08 ff ff ff 7f 7f                |
    | rcl qword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 48 c1 94 08 01 00 00 80 80                |
    | rcl qword [rax + 1 * rcx - 0x80000000], 0xff                       | 48 c1 94 08 00 00 00 80 ff                |
    | rcl qword [r10 + 0x7f], 0x00                                       | 49 c1 52 7f 00                            |
    | rcl qword [r10 - 0x80], 0x7f                                       | 49 c1 52 80 7f                            |
    | rcl qword [r10 - 0x81], 0x80                                       | 49 c1 92 7f ff ff ff 80                   |
    | .prev5: nop; nop; nop; nop; nop; rcl qword [rel @prev5], 0xff      | 90 90 90 90 90 48 c1 15 f3 ff ff ff ff    |
    | .prev1: nop; rcl qword [rel @prev1], 0x00                          | 90 48 c1 15 f7 ff ff ff 00                |
    | rcl qword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 48 c1 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | ----------------------------------------- |
"""


def can_encode_rcl_addr64_imm8():
    encode(RCL_ADDR64_IMM8)


RCL_ADDR64_CL = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | rcl qword [rax], cl                                              | 48 d3 10                               |
    | rcl qword [rcx], cl                                              | 48 d3 11                               |
    | rcl qword [rdx], cl                                              | 48 d3 12                               |
    | rcl qword [rbx], cl                                              | 48 d3 13                               |
    | rcl qword [rsp], cl                                              | 48 d3 14 24                            |
    | rcl qword [rbp], cl                                              | 48 d3 55 00                            |
    | rcl qword [rsi], cl                                              | 48 d3 16                               |
    | rcl qword [rdi], cl                                              | 48 d3 17                               |
    | rcl qword [r8], cl                                               | 49 d3 10                               |
    | rcl qword [r9], cl                                               | 49 d3 11                               |
    | rcl qword [r10], cl                                              | 49 d3 12                               |
    | rcl qword [r11], cl                                              | 49 d3 13                               |
    | rcl qword [r12], cl                                              | 49 d3 14 24                            |
    | rcl qword [r13], cl                                              | 49 d3 55 00                            |
    | rcl qword [r14], cl                                              | 49 d3 16                               |
    | rcl qword [r15], cl                                              | 49 d3 17                               |
    | rcl qword [rax + 1 * rcx], cl                                    | 48 d3 14 08                            |
    | rcl qword [rcx + 1 * rcx], cl                                    | 48 d3 14 09                            |
    | rcl qword [rdx + 1 * rcx], cl                                    | 48 d3 14 0a                            |
    | rcl qword [rbx + 1 * rcx], cl                                    | 48 d3 14 0b                            |
    | rcl qword [rsp + 1 * rcx], cl                                    | 48 d3 14 0c                            |
    | rcl qword [rbp + 1 * rcx], cl                                    | 48 d3 54 0d 00                         |
    | rcl qword [rsi + 1 * rcx], cl                                    | 48 d3 14 0e                            |
    | rcl qword [rdi + 1 * rcx], cl                                    | 48 d3 14 0f                            |
    | rcl qword [r8 + 1 * rcx], cl                                     | 49 d3 14 08                            |
    | rcl qword [r9 + 1 * rcx], cl                                     | 49 d3 14 09                            |
    | rcl qword [r10 + 1 * rcx], cl                                    | 49 d3 14 0a                            |
    | rcl qword [r11 + 1 * rcx], cl                                    | 49 d3 14 0b                            |
    | rcl qword [r12 + 1 * rcx], cl                                    | 49 d3 14 0c                            |
    | rcl qword [r13 + 1 * rcx], cl                                    | 49 d3 54 0d 00                         |
    | rcl qword [r14 + 1 * rcx], cl                                    | 49 d3 14 0e                            |
    | rcl qword [r15 + 1 * rcx], cl                                    | 49 d3 14 0f                            |
    | rcl qword [rax + 1 * rax], cl                                    | 48 d3 14 00                            |
    | rcl qword [rax + 1 * rdx], cl                                    | 48 d3 14 10                            |
    | rcl qword [rax + 1 * rbx], cl                                    | 48 d3 14 18                            |
    | rcl qword [rax + 1 * rbp], cl                                    | 48 d3 14 28                            |
    | rcl qword [rax + 1 * rsi], cl                                    | 48 d3 14 30                            |
    | rcl qword [rax + 1 * rdi], cl                                    | 48 d3 14 38                            |
    | rcl qword [rax + 1 * r8], cl                                     | 4a d3 14 00                            |
    | rcl qword [rax + 1 * r9], cl                                     | 4a d3 14 08                            |
    | rcl qword [rax + 1 * r10], cl                                    | 4a d3 14 10                            |
    | rcl qword [rax + 1 * r11], cl                                    | 4a d3 14 18                            |
    | rcl qword [rax + 1 * r12], cl                                    | 4a d3 14 20                            |
    | rcl qword [rax + 1 * r13], cl                                    | 4a d3 14 28                            |
    | rcl qword [rax + 1 * r14], cl                                    | 4a d3 14 30                            |
    | rcl qword [rax + 1 * r15], cl                                    | 4a d3 14 38                            |
    | rcl qword [rax + 2 * rcx], cl                                    | 48 d3 14 48                            |
    | rcl qword [rax + 4 * rcx], cl                                    | 48 d3 14 88                            |
    | rcl qword [rax + 8 * rcx], cl                                    | 48 d3 14 c8                            |
    | rcl qword [r8 + 1 * r9], cl                                      | 4b d3 14 08                            |
    | rcl qword [r8 + 2 * r9], cl                                      | 4b d3 14 48                            |
    | rcl qword [r8 + 4 * r9], cl                                      | 4b d3 14 88                            |
    | rcl qword [r8 + 8 * r9], cl                                      | 4b d3 14 c8                            |
    | rcl qword [1 * rcx], cl                                          | 48 d3 14 0d 00 00 00 00                |
    | rcl qword [2 * rcx], cl                                          | 48 d3 14 4d 00 00 00 00                |
    | rcl qword [4 * rcx], cl                                          | 48 d3 14 8d 00 00 00 00                |
    | rcl qword [8 * rcx], cl                                          | 48 d3 14 cd 00 00 00 00                |
    | rcl qword [1 * r9], cl                                           | 4a d3 14 0d 00 00 00 00                |
    | rcl qword [2 * r9], cl                                           | 4a d3 14 4d 00 00 00 00                |
    | rcl qword [4 * r9], cl                                           | 4a d3 14 8d 00 00 00 00                |
    | rcl qword [8 * r9], cl                                           | 4a d3 14 cd 00 00 00 00                |
    | rcl qword [r13 + 8 * r12], cl                                    | 4b d3 54 e5 00                         |
    | rcl qword [rsp + 4 * r15], cl                                    | 4a d3 14 bc                            |
    | rcl qword [rax + 1 * rcx + 0x00], cl                             | 48 d3 54 08 00                         |
    | rcl qword [rax + 1 * rcx - 0x00], cl                             | 48 d3 54 08 00                         |
    | rcl qword [rax + 1 * rcx + 0x01], cl                             | 48 d3 54 08 01                         |
    | rcl qword [rax + 1 * rcx - 0x01], cl                             | 48 d3 54 08 ff                         |
    | rcl qword [rax + 1 * rcx + 0x00000001], cl                       | 48 d3 94 08 01 00 00 00                |
    | rcl qword [rax + 1 * rcx - 0x00000001], cl                       | 48 d3 94 08 ff ff ff ff                |
    | rcl qword [rax + 1 * rcx + 0x7f], cl                             | 48 d3 54 08 7f                         |
    | rcl qword [rax + 1 * rcx - 0x7f], cl                             | 48 d3 54 08 81                         |
    | rcl qword [rax + 1 * rcx + 0x80], cl                             | 48 d3 94 08 80 00 00 00                |
    | rcl qword [rax + 1 * rcx - 0x80], cl                             | 48 d3 54 08 80                         |
    | rcl qword [rax + 1 * rcx - 0x81], cl                             | 48 d3 94 08 7f ff ff ff                |
    | rcl qword [rax + 1 * rcx + 0xff], cl                             | 48 d3 94 08 ff 00 00 00                |
    | rcl qword [rax + 1 * rcx - 0xff], cl                             | 48 d3 94 08 01 ff ff ff                |
    | rcl qword [rax + 1 * rcx + 0x7fffffff], cl                       | 48 d3 94 08 ff ff ff 7f                |
    | rcl qword [rax + 1 * rcx - 0x7fffffff], cl                       | 48 d3 94 08 01 00 00 80                |
    | rcl qword [rax + 1 * rcx - 0x80000000], cl                       | 48 d3 94 08 00 00 00 80                |
    | rcl qword [r10 + 0x7f], cl                                       | 49 d3 52 7f                            |
    | rcl qword [r10 + 0x80], cl                                       | 49 d3 92 80 00 00 00                   |
    | rcl qword [r10 - 0x80], cl                                       | 49 d3 52 80                            |
    | rcl qword [r10 - 0x81], cl                                       | 49 d3 92 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; rcl qword [rel @prev5], cl      | 90 90 90 90 90 48 d3 15 f4 ff ff ff    |
    | .prev1: nop; rcl qword [rel @prev1], cl                          | 90 48 d3 15 f8 ff ff ff                |
    | rcl qword [rel @next1], cl; nop; .next1: nop                     | 48 d3 15 01 00 00 00 90 90             |
    | rcl qword [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | 48 d3 15 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_rcl_addr64_cl():
    encode(RCL_ADDR64_CL)


RCL_ADDR32_IMM8 = """
    | ------------------------------------------------------------------ | -------------------------------------- |
    | instruction                                                        | encoding                               |
    | ------------------------------------------------------------------ | -------------------------------------- |
    | rcl dword [rax], 0x01                                              | d1 10                                  |
    | rcl dword [rcx], 0x01                                              | d1 11                                  |
    | rcl dword [rdx], 0x01                                              | d1 12                                  |
    | rcl dword [rbx], 0x01                                              | d1 13                                  |
    | rcl dword [rsp], 0x01                                              | d1 14 24                               |
    | rcl dword [rbp], 0x01                                              | d1 55 00                               |
    | rcl dword [rsi], 0x01                                              | d1 16                                  |
    | rcl dword [rdi], 0x01                                              | d1 17                                  |
    | rcl dword [r8], 0x01                                               | 41 d1 10                               |
    | rcl dword [r9], 0x01                                               | 41 d1 11                               |
    | rcl dword [r10], 0x01                                              | 41 d1 12                               |
    | rcl dword [r11], 0x01                                              | 41 d1 13                               |
    | rcl dword [r12], 0x01                                              | 41 d1 14 24                            |
    | rcl dword [r13], 0x01                                              | 41 d1 55 00                            |
    | rcl dword [r14], 0x01                                              | 41 d1 16                               |
    | rcl dword [r15], 0x01                                              | 41 d1 17                               |
    | rcl dword [rax + 1 * rcx], 0x01                                    | d1 14 08                               |
    | rcl dword [rcx + 1 * rcx], 0x01                                    | d1 14 09                               |
    | rcl dword [rdx + 1 * rcx], 0x01                                    | d1 14 0a                               |
    | rcl dword [rbx + 1 * rcx], 0x01                                    | d1 14 0b                               |
    | rcl dword [rsp + 1 * rcx], 0x01                                    | d1 14 0c                               |
    | rcl dword [rbp + 1 * rcx], 0x01                                    | d1 54 0d 00                            |
    | rcl dword [rsi + 1 * rcx], 0x01                                    | d1 14 0e                               |
    | rcl dword [rdi + 1 * rcx], 0x01                                    | d1 14 0f                               |
    | rcl dword [r8 + 1 * rcx], 0x01                                     | 41 d1 14 08                            |
    | rcl dword [r9 + 1 * rcx], 0x01                                     | 41 d1 14 09                            |
    | rcl dword [r10 + 1 * rcx], 0x01                                    | 41 d1 14 0a                            |
    | rcl dword [r11 + 1 * rcx], 0x01                                    | 41 d1 14 0b                            |
    | rcl dword [r12 + 1 * rcx], 0x01                                    | 41 d1 14 0c                            |
    | rcl dword [r13 + 1 * rcx], 0x01                                    | 41 d1 54 0d 00                         |
    | rcl dword [r14 + 1 * rcx], 0x01                                    | 41 d1 14 0e                            |
    | rcl dword [r15 + 1 * rcx], 0x01                                    | 41 d1 14 0f                            |
    | rcl dword [rax + 1 * rax], 0x01                                    | d1 14 00                               |
    | rcl dword [rax + 1 * rdx], 0x01                                    | d1 14 10                               |
    | rcl dword [rax + 1 * rbx], 0x01                                    | d1 14 18                               |
    | rcl dword [rax + 1 * rbp], 0x01                                    | d1 14 28                               |
    | rcl dword [rax + 1 * rsi], 0x01                                    | d1 14 30                               |
    | rcl dword [rax + 1 * rdi], 0x01                                    | d1 14 38                               |
    | rcl dword [rax + 1 * r8], 0x01                                     | 42 d1 14 00                            |
    | rcl dword [rax + 1 * r9], 0x01                                     | 42 d1 14 08                            |
    | rcl dword [rax + 1 * r10], 0x01                                    | 42 d1 14 10                            |
    | rcl dword [rax + 1 * r11], 0x01                                    | 42 d1 14 18                            |
    | rcl dword [rax + 1 * r12], 0x01                                    | 42 d1 14 20                            |
    | rcl dword [rax + 1 * r13], 0x01                                    | 42 d1 14 28                            |
    | rcl dword [rax + 1 * r14], 0x01                                    | 42 d1 14 30                            |
    | rcl dword [rax + 1 * r15], 0x01                                    | 42 d1 14 38                            |
    | rcl dword [rax + 2 * rcx], 0x01                                    | d1 14 48                               |
    | rcl dword [rax + 4 * rcx], 0x01                                    | d1 14 88                               |
    | rcl dword [rax + 8 * rcx], 0x01                                    | d1 14 c8                               |
    | rcl dword [r8 + 1 * r9], 0x01                                      | 43 d1 14 08                            |
    | rcl dword [r8 + 2 * r9], 0x01                                      | 43 d1 14 48                            |
    | rcl dword [r8 + 4 * r9], 0x01                                      | 43 d1 14 88                            |
    | rcl dword [r8 + 8 * r9], 0x01                                      | 43 d1 14 c8                            |
    | rcl dword [1 * rcx], 0x01                                          | d1 14 0d 00 00 00 00                   |
    | rcl dword [2 * rcx], 0x01                                          | d1 14 4d 00 00 00 00                   |
    | rcl dword [4 * rcx], 0x01                                          | d1 14 8d 00 00 00 00                   |
    | rcl dword [8 * rcx], 0x01                                          | d1 14 cd 00 00 00 00                   |
    | rcl dword [1 * r9], 0x01                                           | 42 d1 14 0d 00 00 00 00                |
    | rcl dword [2 * r9], 0x01                                           | 42 d1 14 4d 00 00 00 00                |
    | rcl dword [4 * r9], 0x01                                           | 42 d1 14 8d 00 00 00 00                |
    | rcl dword [8 * r9], 0x01                                           | 42 d1 14 cd 00 00 00 00                |
    | rcl dword [r13 + 8 * r12], 0x01                                    | 43 d1 54 e5 00                         |
    | rcl dword [rsp + 4 * r15], 0x01                                    | 42 d1 14 bc                            |
    | rcl dword [rax + 1 * rcx + 0x00], 0x01                             | d1 54 08 00                            |
    | rcl dword [rax + 1 * rcx - 0x00], 0x01                             | d1 54 08 00                            |
    | rcl dword [rax + 1 * rcx + 0x01], 0x01                             | d1 54 08 01                            |
    | rcl dword [rax + 1 * rcx - 0x01], 0x01                             | d1 54 08 ff                            |
    | rcl dword [rax + 1 * rcx + 0x00000001], 0x01                       | d1 94 08 01 00 00 00                   |
    | rcl dword [rax + 1 * rcx - 0x00000001], 0x01                       | d1 94 08 ff ff ff ff                   |
    | rcl dword [rax + 1 * rcx + 0x7f], 0x01                             | d1 54 08 7f                            |
    | rcl dword [rax + 1 * rcx - 0x7f], 0x01                             | d1 54 08 81                            |
    | rcl dword [rax + 1 * rcx + 0x80], 0x01                             | d1 94 08 80 00 00 00                   |
    | rcl dword [rax + 1 * rcx - 0x80], 0x01                             | d1 54 08 80                            |
    | rcl dword [rax + 1 * rcx - 0x81], 0x01                             | d1 94 08 7f ff ff ff                   |
    | rcl dword [rax + 1 * rcx + 0xff], 0x01                             | d1 94 08 ff 00 00 00                   |
    | rcl dword [rax + 1 * rcx - 0xff], 0x01                             | d1 94 08 01 ff ff ff                   |
    | rcl dword [rax + 1 * rcx + 0x7fffffff], 0x01                       | d1 94 08 ff ff ff 7f                   |
    | rcl dword [rax + 1 * rcx - 0x7fffffff], 0x01                       | d1 94 08 01 00 00 80                   |
    | rcl dword [rax + 1 * rcx - 0x80000000], 0x01                       | d1 94 08 00 00 00 80                   |
    | rcl dword [r10 + 0x7f], 0x01                                       | 41 d1 52 7f                            |
    | rcl dword [r10 + 0x80], 0x01                                       | 41 d1 92 80 00 00 00                   |
    | rcl dword [r10 - 0x80], 0x01                                       | 41 d1 52 80                            |
    | rcl dword [r10 - 0x81], 0x01                                       | 41 d1 92 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; rcl dword [rel @prev5], 0x01      | 90 90 90 90 90 d1 15 f5 ff ff ff       |
    | .prev1: nop; rcl dword [rel @prev1], 0x01                          | 90 d1 15 f9 ff ff ff                   |
    | rcl dword [rel @next1], 0x01; nop; .next1: nop                     | d1 15 01 00 00 00 90 90                |
    | rcl dword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | d1 15 05 00 00 00 90 90 90 90 90 90    |
    | rcl dword [rax], 0x00                                              | c1 10 00                               |
    | rcl dword [rax], 0x7f                                              | c1 10 7f                               |
    | rcl dword [rax], 0x80                                              | c1 10 80                               |
    | rcl dword [rax], 0xff                                              | c1 10 ff                               |
    | rcl dword [rcx], 0x7f                                              | c1 11 7f                               |
    | rcl dword [rdx], 0x80                                              | c1 12 80                               |
    | rcl dword [rbx], 0xff                                              | c1 13 ff                               |
    | rcl dword [rsp], 0x00                                              | c1 14 24 00                            |
    | rcl dword [rsi], 0x7f                                              | c1 16 7f                               |
    | rcl dword [rdi], 0x80                                              | c1 17 80                               |
    | rcl dword [r8], 0xff                                               | 41 c1 10 ff                            |
    | rcl dword [r9], 0x00                                               | 41 c1 11 00                            |
    | rcl dword [r11], 0x7f                                              | 41 c1 13 7f                            |
    | rcl dword [r12], 0x80                                              | 41 c1 14 24 80                         |
    | rcl dword [r13], 0xff                                              | 41 c1 55 00 ff                         |
    | rcl dword [r14], 0x00                                              | 41 c1 16 00                            |
    | rcl dword [rax + 1 * rcx], 0x7f                                    | c1 14 08 7f                            |
    | rcl dword [rcx + 1 * rcx], 0x80                                    | c1 14 09 80                            |
    | rcl dword [rdx + 1 * rcx], 0xff                                    | c1 14 0a ff                            |
    | rcl dword [rbx + 1 * rcx], 0x00                                    | c1 14 0b 00                            |
    | rcl dword [rbp + 1 * rcx], 0x7f                                    | c1 54 0d 00 7f                         |
    | rcl dword [rsi + 1 * rcx], 0x80                                    | c1 14 0e 80                            |
    | rcl dword [rdi + 1 * rcx], 0xff                                    | c1 14 0f ff                            |
    | rcl dword [r8 + 1 * rcx], 0x00                                     | 41 c1 14 08 00                         |
    | rcl dword [r10 + 1 * rcx], 0x7f                                    | 41 c1 14 0a 7f                         |
    | rcl dword [r11 + 1 * rcx], 0x80                                    | 41 c1 14 0b 80                         |
    | rcl dword [r12 + 1 * rcx], 0xff                                    | 41 c1 14 0c ff                         |
    | rcl dword [r13 + 1 * rcx], 0x00                                    | 41 c1 54 0d 00 00                      |
    | rcl dword [r15 + 1 * rcx], 0x7f                                    | 41 c1 14 0f 7f                         |
    | rcl dword [rax + 1 * rax], 0x80                                    | c1 14 00 80                            |
    | rcl dword [rax + 1 * rdx], 0xff                                    | c1 14 10 ff                            |
    | rcl dword [rax + 1 * rbx], 0x00                                    | c1 14 18 00                            |
    | rcl dword [rax + 1 * rsi], 0x7f                                    | c1 14 30 7f                            |
    | rcl dword [rax + 1 * rdi], 0x80                                    | c1 14 38 80                            |
    | rcl dword [rax + 1 * r8], 0xff                                     | 42 c1 14 00 ff                         |
    | rcl dword [rax + 1 * r9], 0x00                                     | 42 c1 14 08 00                         |
    | rcl dword [rax + 1 * r11], 0x7f                                    | 42 c1 14 18 7f                         |
    | rcl dword [rax + 1 * r12], 0x80                                    | 42 c1 14 20 80                         |
    | rcl dword [rax + 1 * r13], 0xff                                    | 42 c1 14 28 ff                         |
    | rcl dword [rax + 1 * r14], 0x00                                    | 42 c1 14 30 00                         |
    | rcl dword [rax + 2 * rcx], 0x7f                                    | c1 14 48 7f                            |
    | rcl dword [rax + 4 * rcx], 0x80                                    | c1 14 88 80                            |
    | rcl dword [rax + 8 * rcx], 0xff                                    | c1 14 c8 ff                            |
    | rcl dword [r8 + 1 * r9], 0x00                                      | 43 c1 14 08 00                         |
    | rcl dword [r8 + 4 * r9], 0x7f                                      | 43 c1 14 88 7f                         |
    | rcl dword [r8 + 8 * r9], 0x80                                      | 43 c1 14 c8 80                         |
    | rcl dword [1 * rcx], 0xff                                          | c1 14 0d 00 00 00 00 ff                |
    | rcl dword [2 * rcx], 0x00                                          | c1 14 4d 00 00 00 00 00                |
    | rcl dword [8 * rcx], 0x7f                                          | c1 14 cd 00 00 00 00 7f                |
    | rcl dword [1 * r9], 0x80                                           | 42 c1 14 0d 00 00 00 00 80             |
    | rcl dword [2 * r9], 0xff                                           | 42 c1 14 4d 00 00 00 00 ff             |
    | rcl dword [4 * r9], 0x00                                           | 42 c1 14 8d 00 00 00 00 00             |
    | rcl dword [r13 + 8 * r12], 0x7f                                    | 43 c1 54 e5 00 7f                      |
    | rcl dword [rsp + 4 * r15], 0x80                                    | 42 c1 14 bc 80                         |
    | rcl dword [rax + 1 * rcx + 0x00], 0xff                             | c1 54 08 00 ff                         |
    | rcl dword [rax + 1 * rcx - 0x00], 0x00                             | c1 54 08 00 00                         |
    | rcl dword [rax + 1 * rcx - 0x01], 0x7f                             | c1 54 08 ff 7f                         |
    | rcl dword [rax + 1 * rcx + 0x00000001], 0x80                       | c1 94 08 01 00 00 00 80                |
    | rcl dword [rax + 1 * rcx - 0x00000001], 0xff                       | c1 94 08 ff ff ff ff ff                |
    | rcl dword [rax + 1 * rcx + 0x7f], 0x00                             | c1 54 08 7f 00                         |
    | rcl dword [rax + 1 * rcx + 0x80], 0x7f                             | c1 94 08 80 00 00 00 7f                |
    | rcl dword [rax + 1 * rcx - 0x80], 0x80                             | c1 54 08 80 80                         |
    | rcl dword [rax + 1 * rcx - 0x81], 0xff                             | c1 94 08 7f ff ff ff ff                |
    | rcl dword [rax + 1 * rcx + 0xff], 0x00                             | c1 94 08 ff 00 00 00 00                |
    | rcl dword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | c1 94 08 ff ff ff 7f 7f                |
    | rcl dword [rax + 1 * rcx - 0x7fffffff], 0x80                       | c1 94 08 01 00 00 80 80                |
    | rcl dword [rax + 1 * rcx - 0x80000000], 0xff                       | c1 94 08 00 00 00 80 ff                |
    | rcl dword [r10 + 0x7f], 0x00                                       | 41 c1 52 7f 00                         |
    | rcl dword [r10 - 0x80], 0x7f                                       | 41 c1 52 80 7f                         |
    | rcl dword [r10 - 0x81], 0x80                                       | 41 c1 92 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; rcl dword [rel @prev5], 0xff      | 90 90 90 90 90 c1 15 f4 ff ff ff ff    |
    | .prev1: nop; rcl dword [rel @prev1], 0x00                          | 90 c1 15 f8 ff ff ff 00                |
    | rcl dword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | c1 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | -------------------------------------- |
"""


def can_encode_rcl_addr32_imm8():
    encode(RCL_ADDR32_IMM8)


RCL_ADDR32_CL = """
    | ---------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                      | encoding                            |
    | ---------------------------------------------------------------- | ----------------------------------- |
    | rcl dword [rax], cl                                              | d3 10                               |
    | rcl dword [rcx], cl                                              | d3 11                               |
    | rcl dword [rdx], cl                                              | d3 12                               |
    | rcl dword [rbx], cl                                              | d3 13                               |
    | rcl dword [rsp], cl                                              | d3 14 24                            |
    | rcl dword [rbp], cl                                              | d3 55 00                            |
    | rcl dword [rsi], cl                                              | d3 16                               |
    | rcl dword [rdi], cl                                              | d3 17                               |
    | rcl dword [r8], cl                                               | 41 d3 10                            |
    | rcl dword [r9], cl                                               | 41 d3 11                            |
    | rcl dword [r10], cl                                              | 41 d3 12                            |
    | rcl dword [r11], cl                                              | 41 d3 13                            |
    | rcl dword [r12], cl                                              | 41 d3 14 24                         |
    | rcl dword [r13], cl                                              | 41 d3 55 00                         |
    | rcl dword [r14], cl                                              | 41 d3 16                            |
    | rcl dword [r15], cl                                              | 41 d3 17                            |
    | rcl dword [rax + 1 * rcx], cl                                    | d3 14 08                            |
    | rcl dword [rcx + 1 * rcx], cl                                    | d3 14 09                            |
    | rcl dword [rdx + 1 * rcx], cl                                    | d3 14 0a                            |
    | rcl dword [rbx + 1 * rcx], cl                                    | d3 14 0b                            |
    | rcl dword [rsp + 1 * rcx], cl                                    | d3 14 0c                            |
    | rcl dword [rbp + 1 * rcx], cl                                    | d3 54 0d 00                         |
    | rcl dword [rsi + 1 * rcx], cl                                    | d3 14 0e                            |
    | rcl dword [rdi + 1 * rcx], cl                                    | d3 14 0f                            |
    | rcl dword [r8 + 1 * rcx], cl                                     | 41 d3 14 08                         |
    | rcl dword [r9 + 1 * rcx], cl                                     | 41 d3 14 09                         |
    | rcl dword [r10 + 1 * rcx], cl                                    | 41 d3 14 0a                         |
    | rcl dword [r11 + 1 * rcx], cl                                    | 41 d3 14 0b                         |
    | rcl dword [r12 + 1 * rcx], cl                                    | 41 d3 14 0c                         |
    | rcl dword [r13 + 1 * rcx], cl                                    | 41 d3 54 0d 00                      |
    | rcl dword [r14 + 1 * rcx], cl                                    | 41 d3 14 0e                         |
    | rcl dword [r15 + 1 * rcx], cl                                    | 41 d3 14 0f                         |
    | rcl dword [rax + 1 * rax], cl                                    | d3 14 00                            |
    | rcl dword [rax + 1 * rdx], cl                                    | d3 14 10                            |
    | rcl dword [rax + 1 * rbx], cl                                    | d3 14 18                            |
    | rcl dword [rax + 1 * rbp], cl                                    | d3 14 28                            |
    | rcl dword [rax + 1 * rsi], cl                                    | d3 14 30                            |
    | rcl dword [rax + 1 * rdi], cl                                    | d3 14 38                            |
    | rcl dword [rax + 1 * r8], cl                                     | 42 d3 14 00                         |
    | rcl dword [rax + 1 * r9], cl                                     | 42 d3 14 08                         |
    | rcl dword [rax + 1 * r10], cl                                    | 42 d3 14 10                         |
    | rcl dword [rax + 1 * r11], cl                                    | 42 d3 14 18                         |
    | rcl dword [rax + 1 * r12], cl                                    | 42 d3 14 20                         |
    | rcl dword [rax + 1 * r13], cl                                    | 42 d3 14 28                         |
    | rcl dword [rax + 1 * r14], cl                                    | 42 d3 14 30                         |
    | rcl dword [rax + 1 * r15], cl                                    | 42 d3 14 38                         |
    | rcl dword [rax + 2 * rcx], cl                                    | d3 14 48                            |
    | rcl dword [rax + 4 * rcx], cl                                    | d3 14 88                            |
    | rcl dword [rax + 8 * rcx], cl                                    | d3 14 c8                            |
    | rcl dword [r8 + 1 * r9], cl                                      | 43 d3 14 08                         |
    | rcl dword [r8 + 2 * r9], cl                                      | 43 d3 14 48                         |
    | rcl dword [r8 + 4 * r9], cl                                      | 43 d3 14 88                         |
    | rcl dword [r8 + 8 * r9], cl                                      | 43 d3 14 c8                         |
    | rcl dword [1 * rcx], cl                                          | d3 14 0d 00 00 00 00                |
    | rcl dword [2 * rcx], cl                                          | d3 14 4d 00 00 00 00                |
    | rcl dword [4 * rcx], cl                                          | d3 14 8d 00 00 00 00                |
    | rcl dword [8 * rcx], cl                                          | d3 14 cd 00 00 00 00                |
    | rcl dword [1 * r9], cl                                           | 42 d3 14 0d 00 00 00 00             |
    | rcl dword [2 * r9], cl                                           | 42 d3 14 4d 00 00 00 00             |
    | rcl dword [4 * r9], cl                                           | 42 d3 14 8d 00 00 00 00             |
    | rcl dword [8 * r9], cl                                           | 42 d3 14 cd 00 00 00 00             |
    | rcl dword [r13 + 8 * r12], cl                                    | 43 d3 54 e5 00                      |
    | rcl dword [rsp + 4 * r15], cl                                    | 42 d3 14 bc                         |
    | rcl dword [rax + 1 * rcx + 0x00], cl                             | d3 54 08 00                         |
    | rcl dword [rax + 1 * rcx - 0x00], cl                             | d3 54 08 00                         |
    | rcl dword [rax + 1 * rcx + 0x01], cl                             | d3 54 08 01                         |
    | rcl dword [rax + 1 * rcx - 0x01], cl                             | d3 54 08 ff                         |
    | rcl dword [rax + 1 * rcx + 0x00000001], cl                       | d3 94 08 01 00 00 00                |
    | rcl dword [rax + 1 * rcx - 0x00000001], cl                       | d3 94 08 ff ff ff ff                |
    | rcl dword [rax + 1 * rcx + 0x7f], cl                             | d3 54 08 7f                         |
    | rcl dword [rax + 1 * rcx - 0x7f], cl                             | d3 54 08 81                         |
    | rcl dword [rax + 1 * rcx + 0x80], cl                             | d3 94 08 80 00 00 00                |
    | rcl dword [rax + 1 * rcx - 0x80], cl                             | d3 54 08 80                         |
    | rcl dword [rax + 1 * rcx - 0x81], cl                             | d3 94 08 7f ff ff ff                |
    | rcl dword [rax + 1 * rcx + 0xff], cl                             | d3 94 08 ff 00 00 00                |
    | rcl dword [rax + 1 * rcx - 0xff], cl                             | d3 94 08 01 ff ff ff                |
    | rcl dword [rax + 1 * rcx + 0x7fffffff], cl                       | d3 94 08 ff ff ff 7f                |
    | rcl dword [rax + 1 * rcx - 0x7fffffff], cl                       | d3 94 08 01 00 00 80                |
    | rcl dword [rax + 1 * rcx - 0x80000000], cl                       | d3 94 08 00 00 00 80                |
    | rcl dword [r10 + 0x7f], cl                                       | 41 d3 52 7f                         |
    | rcl dword [r10 + 0x80], cl                                       | 41 d3 92 80 00 00 00                |
    | rcl dword [r10 - 0x80], cl                                       | 41 d3 52 80                         |
    | rcl dword [r10 - 0x81], cl                                       | 41 d3 92 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; rcl dword [rel @prev5], cl      | 90 90 90 90 90 d3 15 f5 ff ff ff    |
    | .prev1: nop; rcl dword [rel @prev1], cl                          | 90 d3 15 f9 ff ff ff                |
    | rcl dword [rel @next1], cl; nop; .next1: nop                     | d3 15 01 00 00 00 90 90             |
    | rcl dword [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | d3 15 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_rcl_addr32_cl():
    encode(RCL_ADDR32_CL)


RCL_ADDR16_IMM8 = """
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | instruction                                                       | encoding                                  |
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | rcl word [rax], 0x01                                              | 66 d1 10                                  |
    | rcl word [rcx], 0x01                                              | 66 d1 11                                  |
    | rcl word [rdx], 0x01                                              | 66 d1 12                                  |
    | rcl word [rbx], 0x01                                              | 66 d1 13                                  |
    | rcl word [rsp], 0x01                                              | 66 d1 14 24                               |
    | rcl word [rbp], 0x01                                              | 66 d1 55 00                               |
    | rcl word [rsi], 0x01                                              | 66 d1 16                                  |
    | rcl word [rdi], 0x01                                              | 66 d1 17                                  |
    | rcl word [r8], 0x01                                               | 66 41 d1 10                               |
    | rcl word [r9], 0x01                                               | 66 41 d1 11                               |
    | rcl word [r10], 0x01                                              | 66 41 d1 12                               |
    | rcl word [r11], 0x01                                              | 66 41 d1 13                               |
    | rcl word [r12], 0x01                                              | 66 41 d1 14 24                            |
    | rcl word [r13], 0x01                                              | 66 41 d1 55 00                            |
    | rcl word [r14], 0x01                                              | 66 41 d1 16                               |
    | rcl word [r15], 0x01                                              | 66 41 d1 17                               |
    | rcl word [rax + 1 * rcx], 0x01                                    | 66 d1 14 08                               |
    | rcl word [rcx + 1 * rcx], 0x01                                    | 66 d1 14 09                               |
    | rcl word [rdx + 1 * rcx], 0x01                                    | 66 d1 14 0a                               |
    | rcl word [rbx + 1 * rcx], 0x01                                    | 66 d1 14 0b                               |
    | rcl word [rsp + 1 * rcx], 0x01                                    | 66 d1 14 0c                               |
    | rcl word [rbp + 1 * rcx], 0x01                                    | 66 d1 54 0d 00                            |
    | rcl word [rsi + 1 * rcx], 0x01                                    | 66 d1 14 0e                               |
    | rcl word [rdi + 1 * rcx], 0x01                                    | 66 d1 14 0f                               |
    | rcl word [r8 + 1 * rcx], 0x01                                     | 66 41 d1 14 08                            |
    | rcl word [r9 + 1 * rcx], 0x01                                     | 66 41 d1 14 09                            |
    | rcl word [r10 + 1 * rcx], 0x01                                    | 66 41 d1 14 0a                            |
    | rcl word [r11 + 1 * rcx], 0x01                                    | 66 41 d1 14 0b                            |
    | rcl word [r12 + 1 * rcx], 0x01                                    | 66 41 d1 14 0c                            |
    | rcl word [r13 + 1 * rcx], 0x01                                    | 66 41 d1 54 0d 00                         |
    | rcl word [r14 + 1 * rcx], 0x01                                    | 66 41 d1 14 0e                            |
    | rcl word [r15 + 1 * rcx], 0x01                                    | 66 41 d1 14 0f                            |
    | rcl word [rax + 1 * rax], 0x01                                    | 66 d1 14 00                               |
    | rcl word [rax + 1 * rdx], 0x01                                    | 66 d1 14 10                               |
    | rcl word [rax + 1 * rbx], 0x01                                    | 66 d1 14 18                               |
    | rcl word [rax + 1 * rbp], 0x01                                    | 66 d1 14 28                               |
    | rcl word [rax + 1 * rsi], 0x01                                    | 66 d1 14 30                               |
    | rcl word [rax + 1 * rdi], 0x01                                    | 66 d1 14 38                               |
    | rcl word [rax + 1 * r8], 0x01                                     | 66 42 d1 14 00                            |
    | rcl word [rax + 1 * r9], 0x01                                     | 66 42 d1 14 08                            |
    | rcl word [rax + 1 * r10], 0x01                                    | 66 42 d1 14 10                            |
    | rcl word [rax + 1 * r11], 0x01                                    | 66 42 d1 14 18                            |
    | rcl word [rax + 1 * r12], 0x01                                    | 66 42 d1 14 20                            |
    | rcl word [rax + 1 * r13], 0x01                                    | 66 42 d1 14 28                            |
    | rcl word [rax + 1 * r14], 0x01                                    | 66 42 d1 14 30                            |
    | rcl word [rax + 1 * r15], 0x01                                    | 66 42 d1 14 38                            |
    | rcl word [rax + 2 * rcx], 0x01                                    | 66 d1 14 48                               |
    | rcl word [rax + 4 * rcx], 0x01                                    | 66 d1 14 88                               |
    | rcl word [rax + 8 * rcx], 0x01                                    | 66 d1 14 c8                               |
    | rcl word [r8 + 1 * r9], 0x01                                      | 66 43 d1 14 08                            |
    | rcl word [r8 + 2 * r9], 0x01                                      | 66 43 d1 14 48                            |
    | rcl word [r8 + 4 * r9], 0x01                                      | 66 43 d1 14 88                            |
    | rcl word [r8 + 8 * r9], 0x01                                      | 66 43 d1 14 c8                            |
    | rcl word [1 * rcx], 0x01                                          | 66 d1 14 0d 00 00 00 00                   |
    | rcl word [2 * rcx], 0x01                                          | 66 d1 14 4d 00 00 00 00                   |
    | rcl word [4 * rcx], 0x01                                          | 66 d1 14 8d 00 00 00 00                   |
    | rcl word [8 * rcx], 0x01                                          | 66 d1 14 cd 00 00 00 00                   |
    | rcl word [1 * r9], 0x01                                           | 66 42 d1 14 0d 00 00 00 00                |
    | rcl word [2 * r9], 0x01                                           | 66 42 d1 14 4d 00 00 00 00                |
    | rcl word [4 * r9], 0x01                                           | 66 42 d1 14 8d 00 00 00 00                |
    | rcl word [8 * r9], 0x01                                           | 66 42 d1 14 cd 00 00 00 00                |
    | rcl word [r13 + 8 * r12], 0x01                                    | 66 43 d1 54 e5 00                         |
    | rcl word [rsp + 4 * r15], 0x01                                    | 66 42 d1 14 bc                            |
    | rcl word [rax + 1 * rcx + 0x00], 0x01                             | 66 d1 54 08 00                            |
    | rcl word [rax + 1 * rcx - 0x00], 0x01                             | 66 d1 54 08 00                            |
    | rcl word [rax + 1 * rcx + 0x01], 0x01                             | 66 d1 54 08 01                            |
    | rcl word [rax + 1 * rcx - 0x01], 0x01                             | 66 d1 54 08 ff                            |
    | rcl word [rax + 1 * rcx + 0x00000001], 0x01                       | 66 d1 94 08 01 00 00 00                   |
    | rcl word [rax + 1 * rcx - 0x00000001], 0x01                       | 66 d1 94 08 ff ff ff ff                   |
    | rcl word [rax + 1 * rcx + 0x7f], 0x01                             | 66 d1 54 08 7f                            |
    | rcl word [rax + 1 * rcx - 0x7f], 0x01                             | 66 d1 54 08 81                            |
    | rcl word [rax + 1 * rcx + 0x80], 0x01                             | 66 d1 94 08 80 00 00 00                   |
    | rcl word [rax + 1 * rcx - 0x80], 0x01                             | 66 d1 54 08 80                            |
    | rcl word [rax + 1 * rcx - 0x81], 0x01                             | 66 d1 94 08 7f ff ff ff                   |
    | rcl word [rax + 1 * rcx + 0xff], 0x01                             | 66 d1 94 08 ff 00 00 00                   |
    | rcl word [rax + 1 * rcx - 0xff], 0x01                             | 66 d1 94 08 01 ff ff ff                   |
    | rcl word [rax + 1 * rcx + 0x7fffffff], 0x01                       | 66 d1 94 08 ff ff ff 7f                   |
    | rcl word [rax + 1 * rcx - 0x7fffffff], 0x01                       | 66 d1 94 08 01 00 00 80                   |
    | rcl word [rax + 1 * rcx - 0x80000000], 0x01                       | 66 d1 94 08 00 00 00 80                   |
    | rcl word [r10 + 0x7f], 0x01                                       | 66 41 d1 52 7f                            |
    | rcl word [r10 + 0x80], 0x01                                       | 66 41 d1 92 80 00 00 00                   |
    | rcl word [r10 - 0x80], 0x01                                       | 66 41 d1 52 80                            |
    | rcl word [r10 - 0x81], 0x01                                       | 66 41 d1 92 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; rcl word [rel @prev5], 0x01      | 90 90 90 90 90 66 d1 15 f4 ff ff ff       |
    | .prev1: nop; rcl word [rel @prev1], 0x01                          | 90 66 d1 15 f8 ff ff ff                   |
    | rcl word [rel @next1], 0x01; nop; .next1: nop                     | 66 d1 15 01 00 00 00 90 90                |
    | rcl word [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 66 d1 15 05 00 00 00 90 90 90 90 90 90    |
    | rcl word [rax], 0x00                                              | 66 c1 10 00                               |
    | rcl word [rax], 0x7f                                              | 66 c1 10 7f                               |
    | rcl word [rax], 0x80                                              | 66 c1 10 80                               |
    | rcl word [rax], 0xff                                              | 66 c1 10 ff                               |
    | rcl word [rcx], 0x7f                                              | 66 c1 11 7f                               |
    | rcl word [rdx], 0x80                                              | 66 c1 12 80                               |
    | rcl word [rbx], 0xff                                              | 66 c1 13 ff                               |
    | rcl word [rsp], 0x00                                              | 66 c1 14 24 00                            |
    | rcl word [rsi], 0x7f                                              | 66 c1 16 7f                               |
    | rcl word [rdi], 0x80                                              | 66 c1 17 80                               |
    | rcl word [r8], 0xff                                               | 66 41 c1 10 ff                            |
    | rcl word [r9], 0x00                                               | 66 41 c1 11 00                            |
    | rcl word [r11], 0x7f                                              | 66 41 c1 13 7f                            |
    | rcl word [r12], 0x80                                              | 66 41 c1 14 24 80                         |
    | rcl word [r13], 0xff                                              | 66 41 c1 55 00 ff                         |
    | rcl word [r14], 0x00                                              | 66 41 c1 16 00                            |
    | rcl word [rax + 1 * rcx], 0x7f                                    | 66 c1 14 08 7f                            |
    | rcl word [rcx + 1 * rcx], 0x80                                    | 66 c1 14 09 80                            |
    | rcl word [rdx + 1 * rcx], 0xff                                    | 66 c1 14 0a ff                            |
    | rcl word [rbx + 1 * rcx], 0x00                                    | 66 c1 14 0b 00                            |
    | rcl word [rbp + 1 * rcx], 0x7f                                    | 66 c1 54 0d 00 7f                         |
    | rcl word [rsi + 1 * rcx], 0x80                                    | 66 c1 14 0e 80                            |
    | rcl word [rdi + 1 * rcx], 0xff                                    | 66 c1 14 0f ff                            |
    | rcl word [r8 + 1 * rcx], 0x00                                     | 66 41 c1 14 08 00                         |
    | rcl word [r10 + 1 * rcx], 0x7f                                    | 66 41 c1 14 0a 7f                         |
    | rcl word [r11 + 1 * rcx], 0x80                                    | 66 41 c1 14 0b 80                         |
    | rcl word [r12 + 1 * rcx], 0xff                                    | 66 41 c1 14 0c ff                         |
    | rcl word [r13 + 1 * rcx], 0x00                                    | 66 41 c1 54 0d 00 00                      |
    | rcl word [r15 + 1 * rcx], 0x7f                                    | 66 41 c1 14 0f 7f                         |
    | rcl word [rax + 1 * rax], 0x80                                    | 66 c1 14 00 80                            |
    | rcl word [rax + 1 * rdx], 0xff                                    | 66 c1 14 10 ff                            |
    | rcl word [rax + 1 * rbx], 0x00                                    | 66 c1 14 18 00                            |
    | rcl word [rax + 1 * rsi], 0x7f                                    | 66 c1 14 30 7f                            |
    | rcl word [rax + 1 * rdi], 0x80                                    | 66 c1 14 38 80                            |
    | rcl word [rax + 1 * r8], 0xff                                     | 66 42 c1 14 00 ff                         |
    | rcl word [rax + 1 * r9], 0x00                                     | 66 42 c1 14 08 00                         |
    | rcl word [rax + 1 * r11], 0x7f                                    | 66 42 c1 14 18 7f                         |
    | rcl word [rax + 1 * r12], 0x80                                    | 66 42 c1 14 20 80                         |
    | rcl word [rax + 1 * r13], 0xff                                    | 66 42 c1 14 28 ff                         |
    | rcl word [rax + 1 * r14], 0x00                                    | 66 42 c1 14 30 00                         |
    | rcl word [rax + 2 * rcx], 0x7f                                    | 66 c1 14 48 7f                            |
    | rcl word [rax + 4 * rcx], 0x80                                    | 66 c1 14 88 80                            |
    | rcl word [rax + 8 * rcx], 0xff                                    | 66 c1 14 c8 ff                            |
    | rcl word [r8 + 1 * r9], 0x00                                      | 66 43 c1 14 08 00                         |
    | rcl word [r8 + 4 * r9], 0x7f                                      | 66 43 c1 14 88 7f                         |
    | rcl word [r8 + 8 * r9], 0x80                                      | 66 43 c1 14 c8 80                         |
    | rcl word [1 * rcx], 0xff                                          | 66 c1 14 0d 00 00 00 00 ff                |
    | rcl word [2 * rcx], 0x00                                          | 66 c1 14 4d 00 00 00 00 00                |
    | rcl word [8 * rcx], 0x7f                                          | 66 c1 14 cd 00 00 00 00 7f                |
    | rcl word [1 * r9], 0x80                                           | 66 42 c1 14 0d 00 00 00 00 80             |
    | rcl word [2 * r9], 0xff                                           | 66 42 c1 14 4d 00 00 00 00 ff             |
    | rcl word [4 * r9], 0x00                                           | 66 42 c1 14 8d 00 00 00 00 00             |
    | rcl word [r13 + 8 * r12], 0x7f                                    | 66 43 c1 54 e5 00 7f                      |
    | rcl word [rsp + 4 * r15], 0x80                                    | 66 42 c1 14 bc 80                         |
    | rcl word [rax + 1 * rcx + 0x00], 0xff                             | 66 c1 54 08 00 ff                         |
    | rcl word [rax + 1 * rcx - 0x00], 0x00                             | 66 c1 54 08 00 00                         |
    | rcl word [rax + 1 * rcx - 0x01], 0x7f                             | 66 c1 54 08 ff 7f                         |
    | rcl word [rax + 1 * rcx + 0x00000001], 0x80                       | 66 c1 94 08 01 00 00 00 80                |
    | rcl word [rax + 1 * rcx - 0x00000001], 0xff                       | 66 c1 94 08 ff ff ff ff ff                |
    | rcl word [rax + 1 * rcx + 0x7f], 0x00                             | 66 c1 54 08 7f 00                         |
    | rcl word [rax + 1 * rcx + 0x80], 0x7f                             | 66 c1 94 08 80 00 00 00 7f                |
    | rcl word [rax + 1 * rcx - 0x80], 0x80                             | 66 c1 54 08 80 80                         |
    | rcl word [rax + 1 * rcx - 0x81], 0xff                             | 66 c1 94 08 7f ff ff ff ff                |
    | rcl word [rax + 1 * rcx + 0xff], 0x00                             | 66 c1 94 08 ff 00 00 00 00                |
    | rcl word [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 66 c1 94 08 ff ff ff 7f 7f                |
    | rcl word [rax + 1 * rcx - 0x7fffffff], 0x80                       | 66 c1 94 08 01 00 00 80 80                |
    | rcl word [rax + 1 * rcx - 0x80000000], 0xff                       | 66 c1 94 08 00 00 00 80 ff                |
    | rcl word [r10 + 0x7f], 0x00                                       | 66 41 c1 52 7f 00                         |
    | rcl word [r10 - 0x80], 0x7f                                       | 66 41 c1 52 80 7f                         |
    | rcl word [r10 - 0x81], 0x80                                       | 66 41 c1 92 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; rcl word [rel @prev5], 0xff      | 90 90 90 90 90 66 c1 15 f3 ff ff ff ff    |
    | .prev1: nop; rcl word [rel @prev1], 0x00                          | 90 66 c1 15 f7 ff ff ff 00                |
    | rcl word [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 66 c1 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------------- |
"""


def can_encode_rcl_addr16_imm8():
    encode(RCL_ADDR16_IMM8)


RCL_ADDR16_CL = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | rcl word [rax], cl                                              | 66 d3 10                               |
    | rcl word [rcx], cl                                              | 66 d3 11                               |
    | rcl word [rdx], cl                                              | 66 d3 12                               |
    | rcl word [rbx], cl                                              | 66 d3 13                               |
    | rcl word [rsp], cl                                              | 66 d3 14 24                            |
    | rcl word [rbp], cl                                              | 66 d3 55 00                            |
    | rcl word [rsi], cl                                              | 66 d3 16                               |
    | rcl word [rdi], cl                                              | 66 d3 17                               |
    | rcl word [r8], cl                                               | 66 41 d3 10                            |
    | rcl word [r9], cl                                               | 66 41 d3 11                            |
    | rcl word [r10], cl                                              | 66 41 d3 12                            |
    | rcl word [r11], cl                                              | 66 41 d3 13                            |
    | rcl word [r12], cl                                              | 66 41 d3 14 24                         |
    | rcl word [r13], cl                                              | 66 41 d3 55 00                         |
    | rcl word [r14], cl                                              | 66 41 d3 16                            |
    | rcl word [r15], cl                                              | 66 41 d3 17                            |
    | rcl word [rax + 1 * rcx], cl                                    | 66 d3 14 08                            |
    | rcl word [rcx + 1 * rcx], cl                                    | 66 d3 14 09                            |
    | rcl word [rdx + 1 * rcx], cl                                    | 66 d3 14 0a                            |
    | rcl word [rbx + 1 * rcx], cl                                    | 66 d3 14 0b                            |
    | rcl word [rsp + 1 * rcx], cl                                    | 66 d3 14 0c                            |
    | rcl word [rbp + 1 * rcx], cl                                    | 66 d3 54 0d 00                         |
    | rcl word [rsi + 1 * rcx], cl                                    | 66 d3 14 0e                            |
    | rcl word [rdi + 1 * rcx], cl                                    | 66 d3 14 0f                            |
    | rcl word [r8 + 1 * rcx], cl                                     | 66 41 d3 14 08                         |
    | rcl word [r9 + 1 * rcx], cl                                     | 66 41 d3 14 09                         |
    | rcl word [r10 + 1 * rcx], cl                                    | 66 41 d3 14 0a                         |
    | rcl word [r11 + 1 * rcx], cl                                    | 66 41 d3 14 0b                         |
    | rcl word [r12 + 1 * rcx], cl                                    | 66 41 d3 14 0c                         |
    | rcl word [r13 + 1 * rcx], cl                                    | 66 41 d3 54 0d 00                      |
    | rcl word [r14 + 1 * rcx], cl                                    | 66 41 d3 14 0e                         |
    | rcl word [r15 + 1 * rcx], cl                                    | 66 41 d3 14 0f                         |
    | rcl word [rax + 1 * rax], cl                                    | 66 d3 14 00                            |
    | rcl word [rax + 1 * rdx], cl                                    | 66 d3 14 10                            |
    | rcl word [rax + 1 * rbx], cl                                    | 66 d3 14 18                            |
    | rcl word [rax + 1 * rbp], cl                                    | 66 d3 14 28                            |
    | rcl word [rax + 1 * rsi], cl                                    | 66 d3 14 30                            |
    | rcl word [rax + 1 * rdi], cl                                    | 66 d3 14 38                            |
    | rcl word [rax + 1 * r8], cl                                     | 66 42 d3 14 00                         |
    | rcl word [rax + 1 * r9], cl                                     | 66 42 d3 14 08                         |
    | rcl word [rax + 1 * r10], cl                                    | 66 42 d3 14 10                         |
    | rcl word [rax + 1 * r11], cl                                    | 66 42 d3 14 18                         |
    | rcl word [rax + 1 * r12], cl                                    | 66 42 d3 14 20                         |
    | rcl word [rax + 1 * r13], cl                                    | 66 42 d3 14 28                         |
    | rcl word [rax + 1 * r14], cl                                    | 66 42 d3 14 30                         |
    | rcl word [rax + 1 * r15], cl                                    | 66 42 d3 14 38                         |
    | rcl word [rax + 2 * rcx], cl                                    | 66 d3 14 48                            |
    | rcl word [rax + 4 * rcx], cl                                    | 66 d3 14 88                            |
    | rcl word [rax + 8 * rcx], cl                                    | 66 d3 14 c8                            |
    | rcl word [r8 + 1 * r9], cl                                      | 66 43 d3 14 08                         |
    | rcl word [r8 + 2 * r9], cl                                      | 66 43 d3 14 48                         |
    | rcl word [r8 + 4 * r9], cl                                      | 66 43 d3 14 88                         |
    | rcl word [r8 + 8 * r9], cl                                      | 66 43 d3 14 c8                         |
    | rcl word [1 * rcx], cl                                          | 66 d3 14 0d 00 00 00 00                |
    | rcl word [2 * rcx], cl                                          | 66 d3 14 4d 00 00 00 00                |
    | rcl word [4 * rcx], cl                                          | 66 d3 14 8d 00 00 00 00                |
    | rcl word [8 * rcx], cl                                          | 66 d3 14 cd 00 00 00 00                |
    | rcl word [1 * r9], cl                                           | 66 42 d3 14 0d 00 00 00 00             |
    | rcl word [2 * r9], cl                                           | 66 42 d3 14 4d 00 00 00 00             |
    | rcl word [4 * r9], cl                                           | 66 42 d3 14 8d 00 00 00 00             |
    | rcl word [8 * r9], cl                                           | 66 42 d3 14 cd 00 00 00 00             |
    | rcl word [r13 + 8 * r12], cl                                    | 66 43 d3 54 e5 00                      |
    | rcl word [rsp + 4 * r15], cl                                    | 66 42 d3 14 bc                         |
    | rcl word [rax + 1 * rcx + 0x00], cl                             | 66 d3 54 08 00                         |
    | rcl word [rax + 1 * rcx - 0x00], cl                             | 66 d3 54 08 00                         |
    | rcl word [rax + 1 * rcx + 0x01], cl                             | 66 d3 54 08 01                         |
    | rcl word [rax + 1 * rcx - 0x01], cl                             | 66 d3 54 08 ff                         |
    | rcl word [rax + 1 * rcx + 0x00000001], cl                       | 66 d3 94 08 01 00 00 00                |
    | rcl word [rax + 1 * rcx - 0x00000001], cl                       | 66 d3 94 08 ff ff ff ff                |
    | rcl word [rax + 1 * rcx + 0x7f], cl                             | 66 d3 54 08 7f                         |
    | rcl word [rax + 1 * rcx - 0x7f], cl                             | 66 d3 54 08 81                         |
    | rcl word [rax + 1 * rcx + 0x80], cl                             | 66 d3 94 08 80 00 00 00                |
    | rcl word [rax + 1 * rcx - 0x80], cl                             | 66 d3 54 08 80                         |
    | rcl word [rax + 1 * rcx - 0x81], cl                             | 66 d3 94 08 7f ff ff ff                |
    | rcl word [rax + 1 * rcx + 0xff], cl                             | 66 d3 94 08 ff 00 00 00                |
    | rcl word [rax + 1 * rcx - 0xff], cl                             | 66 d3 94 08 01 ff ff ff                |
    | rcl word [rax + 1 * rcx + 0x7fffffff], cl                       | 66 d3 94 08 ff ff ff 7f                |
    | rcl word [rax + 1 * rcx - 0x7fffffff], cl                       | 66 d3 94 08 01 00 00 80                |
    | rcl word [rax + 1 * rcx - 0x80000000], cl                       | 66 d3 94 08 00 00 00 80                |
    | rcl word [r10 + 0x7f], cl                                       | 66 41 d3 52 7f                         |
    | rcl word [r10 + 0x80], cl                                       | 66 41 d3 92 80 00 00 00                |
    | rcl word [r10 - 0x80], cl                                       | 66 41 d3 52 80                         |
    | rcl word [r10 - 0x81], cl                                       | 66 41 d3 92 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; rcl word [rel @prev5], cl      | 90 90 90 90 90 66 d3 15 f4 ff ff ff    |
    | .prev1: nop; rcl word [rel @prev1], cl                          | 90 66 d3 15 f8 ff ff ff                |
    | rcl word [rel @next1], cl; nop; .next1: nop                     | 66 d3 15 01 00 00 00 90 90             |
    | rcl word [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | 66 d3 15 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_rcl_addr16_cl():
    encode(RCL_ADDR16_CL)


RCL_ADDR8_IMM8 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | rcl byte [rax], 0x01                                              | d0 10                                  |
    | rcl byte [rcx], 0x01                                              | d0 11                                  |
    | rcl byte [rdx], 0x01                                              | d0 12                                  |
    | rcl byte [rbx], 0x01                                              | d0 13                                  |
    | rcl byte [rsp], 0x01                                              | d0 14 24                               |
    | rcl byte [rbp], 0x01                                              | d0 55 00                               |
    | rcl byte [rsi], 0x01                                              | d0 16                                  |
    | rcl byte [rdi], 0x01                                              | d0 17                                  |
    | rcl byte [r8], 0x01                                               | 41 d0 10                               |
    | rcl byte [r9], 0x01                                               | 41 d0 11                               |
    | rcl byte [r10], 0x01                                              | 41 d0 12                               |
    | rcl byte [r11], 0x01                                              | 41 d0 13                               |
    | rcl byte [r12], 0x01                                              | 41 d0 14 24                            |
    | rcl byte [r13], 0x01                                              | 41 d0 55 00                            |
    | rcl byte [r14], 0x01                                              | 41 d0 16                               |
    | rcl byte [r15], 0x01                                              | 41 d0 17                               |
    | rcl byte [rax + 1 * rcx], 0x01                                    | d0 14 08                               |
    | rcl byte [rcx + 1 * rcx], 0x01                                    | d0 14 09                               |
    | rcl byte [rdx + 1 * rcx], 0x01                                    | d0 14 0a                               |
    | rcl byte [rbx + 1 * rcx], 0x01                                    | d0 14 0b                               |
    | rcl byte [rsp + 1 * rcx], 0x01                                    | d0 14 0c                               |
    | rcl byte [rbp + 1 * rcx], 0x01                                    | d0 54 0d 00                            |
    | rcl byte [rsi + 1 * rcx], 0x01                                    | d0 14 0e                               |
    | rcl byte [rdi + 1 * rcx], 0x01                                    | d0 14 0f                               |
    | rcl byte [r8 + 1 * rcx], 0x01                                     | 41 d0 14 08                            |
    | rcl byte [r9 + 1 * rcx], 0x01                                     | 41 d0 14 09                            |
    | rcl byte [r10 + 1 * rcx], 0x01                                    | 41 d0 14 0a                            |
    | rcl byte [r11 + 1 * rcx], 0x01                                    | 41 d0 14 0b                            |
    | rcl byte [r12 + 1 * rcx], 0x01                                    | 41 d0 14 0c                            |
    | rcl byte [r13 + 1 * rcx], 0x01                                    | 41 d0 54 0d 00                         |
    | rcl byte [r14 + 1 * rcx], 0x01                                    | 41 d0 14 0e                            |
    | rcl byte [r15 + 1 * rcx], 0x01                                    | 41 d0 14 0f                            |
    | rcl byte [rax + 1 * rax], 0x01                                    | d0 14 00                               |
    | rcl byte [rax + 1 * rdx], 0x01                                    | d0 14 10                               |
    | rcl byte [rax + 1 * rbx], 0x01                                    | d0 14 18                               |
    | rcl byte [rax + 1 * rbp], 0x01                                    | d0 14 28                               |
    | rcl byte [rax + 1 * rsi], 0x01                                    | d0 14 30                               |
    | rcl byte [rax + 1 * rdi], 0x01                                    | d0 14 38                               |
    | rcl byte [rax + 1 * r8], 0x01                                     | 42 d0 14 00                            |
    | rcl byte [rax + 1 * r9], 0x01                                     | 42 d0 14 08                            |
    | rcl byte [rax + 1 * r10], 0x01                                    | 42 d0 14 10                            |
    | rcl byte [rax + 1 * r11], 0x01                                    | 42 d0 14 18                            |
    | rcl byte [rax + 1 * r12], 0x01                                    | 42 d0 14 20                            |
    | rcl byte [rax + 1 * r13], 0x01                                    | 42 d0 14 28                            |
    | rcl byte [rax + 1 * r14], 0x01                                    | 42 d0 14 30                            |
    | rcl byte [rax + 1 * r15], 0x01                                    | 42 d0 14 38                            |
    | rcl byte [rax + 2 * rcx], 0x01                                    | d0 14 48                               |
    | rcl byte [rax + 4 * rcx], 0x01                                    | d0 14 88                               |
    | rcl byte [rax + 8 * rcx], 0x01                                    | d0 14 c8                               |
    | rcl byte [r8 + 1 * r9], 0x01                                      | 43 d0 14 08                            |
    | rcl byte [r8 + 2 * r9], 0x01                                      | 43 d0 14 48                            |
    | rcl byte [r8 + 4 * r9], 0x01                                      | 43 d0 14 88                            |
    | rcl byte [r8 + 8 * r9], 0x01                                      | 43 d0 14 c8                            |
    | rcl byte [1 * rcx], 0x01                                          | d0 14 0d 00 00 00 00                   |
    | rcl byte [2 * rcx], 0x01                                          | d0 14 4d 00 00 00 00                   |
    | rcl byte [4 * rcx], 0x01                                          | d0 14 8d 00 00 00 00                   |
    | rcl byte [8 * rcx], 0x01                                          | d0 14 cd 00 00 00 00                   |
    | rcl byte [1 * r9], 0x01                                           | 42 d0 14 0d 00 00 00 00                |
    | rcl byte [2 * r9], 0x01                                           | 42 d0 14 4d 00 00 00 00                |
    | rcl byte [4 * r9], 0x01                                           | 42 d0 14 8d 00 00 00 00                |
    | rcl byte [8 * r9], 0x01                                           | 42 d0 14 cd 00 00 00 00                |
    | rcl byte [r13 + 8 * r12], 0x01                                    | 43 d0 54 e5 00                         |
    | rcl byte [rsp + 4 * r15], 0x01                                    | 42 d0 14 bc                            |
    | rcl byte [rax + 1 * rcx + 0x00], 0x01                             | d0 54 08 00                            |
    | rcl byte [rax + 1 * rcx - 0x00], 0x01                             | d0 54 08 00                            |
    | rcl byte [rax + 1 * rcx + 0x01], 0x01                             | d0 54 08 01                            |
    | rcl byte [rax + 1 * rcx - 0x01], 0x01                             | d0 54 08 ff                            |
    | rcl byte [rax + 1 * rcx + 0x00000001], 0x01                       | d0 94 08 01 00 00 00                   |
    | rcl byte [rax + 1 * rcx - 0x00000001], 0x01                       | d0 94 08 ff ff ff ff                   |
    | rcl byte [rax + 1 * rcx + 0x7f], 0x01                             | d0 54 08 7f                            |
    | rcl byte [rax + 1 * rcx - 0x7f], 0x01                             | d0 54 08 81                            |
    | rcl byte [rax + 1 * rcx + 0x80], 0x01                             | d0 94 08 80 00 00 00                   |
    | rcl byte [rax + 1 * rcx - 0x80], 0x01                             | d0 54 08 80                            |
    | rcl byte [rax + 1 * rcx - 0x81], 0x01                             | d0 94 08 7f ff ff ff                   |
    | rcl byte [rax + 1 * rcx + 0xff], 0x01                             | d0 94 08 ff 00 00 00                   |
    | rcl byte [rax + 1 * rcx - 0xff], 0x01                             | d0 94 08 01 ff ff ff                   |
    | rcl byte [rax + 1 * rcx + 0x7fffffff], 0x01                       | d0 94 08 ff ff ff 7f                   |
    | rcl byte [rax + 1 * rcx - 0x7fffffff], 0x01                       | d0 94 08 01 00 00 80                   |
    | rcl byte [rax + 1 * rcx - 0x80000000], 0x01                       | d0 94 08 00 00 00 80                   |
    | rcl byte [r10 + 0x7f], 0x01                                       | 41 d0 52 7f                            |
    | rcl byte [r10 + 0x80], 0x01                                       | 41 d0 92 80 00 00 00                   |
    | rcl byte [r10 - 0x80], 0x01                                       | 41 d0 52 80                            |
    | rcl byte [r10 - 0x81], 0x01                                       | 41 d0 92 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; rcl byte [rel @prev5], 0x01      | 90 90 90 90 90 d0 15 f5 ff ff ff       |
    | .prev1: nop; rcl byte [rel @prev1], 0x01                          | 90 d0 15 f9 ff ff ff                   |
    | rcl byte [rel @next1], 0x01; nop; .next1: nop                     | d0 15 01 00 00 00 90 90                |
    | rcl byte [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | d0 15 05 00 00 00 90 90 90 90 90 90    |
    | rcl byte [rax], 0x00                                              | c0 10 00                               |
    | rcl byte [rax], 0x7f                                              | c0 10 7f                               |
    | rcl byte [rax], 0x80                                              | c0 10 80                               |
    | rcl byte [rax], 0xff                                              | c0 10 ff                               |
    | rcl byte [rcx], 0x7f                                              | c0 11 7f                               |
    | rcl byte [rdx], 0x80                                              | c0 12 80                               |
    | rcl byte [rbx], 0xff                                              | c0 13 ff                               |
    | rcl byte [rsp], 0x00                                              | c0 14 24 00                            |
    | rcl byte [rsi], 0x7f                                              | c0 16 7f                               |
    | rcl byte [rdi], 0x80                                              | c0 17 80                               |
    | rcl byte [r8], 0xff                                               | 41 c0 10 ff                            |
    | rcl byte [r9], 0x00                                               | 41 c0 11 00                            |
    | rcl byte [r11], 0x7f                                              | 41 c0 13 7f                            |
    | rcl byte [r12], 0x80                                              | 41 c0 14 24 80                         |
    | rcl byte [r13], 0xff                                              | 41 c0 55 00 ff                         |
    | rcl byte [r14], 0x00                                              | 41 c0 16 00                            |
    | rcl byte [rax + 1 * rcx], 0x7f                                    | c0 14 08 7f                            |
    | rcl byte [rcx + 1 * rcx], 0x80                                    | c0 14 09 80                            |
    | rcl byte [rdx + 1 * rcx], 0xff                                    | c0 14 0a ff                            |
    | rcl byte [rbx + 1 * rcx], 0x00                                    | c0 14 0b 00                            |
    | rcl byte [rbp + 1 * rcx], 0x7f                                    | c0 54 0d 00 7f                         |
    | rcl byte [rsi + 1 * rcx], 0x80                                    | c0 14 0e 80                            |
    | rcl byte [rdi + 1 * rcx], 0xff                                    | c0 14 0f ff                            |
    | rcl byte [r8 + 1 * rcx], 0x00                                     | 41 c0 14 08 00                         |
    | rcl byte [r10 + 1 * rcx], 0x7f                                    | 41 c0 14 0a 7f                         |
    | rcl byte [r11 + 1 * rcx], 0x80                                    | 41 c0 14 0b 80                         |
    | rcl byte [r12 + 1 * rcx], 0xff                                    | 41 c0 14 0c ff                         |
    | rcl byte [r13 + 1 * rcx], 0x00                                    | 41 c0 54 0d 00 00                      |
    | rcl byte [r15 + 1 * rcx], 0x7f                                    | 41 c0 14 0f 7f                         |
    | rcl byte [rax + 1 * rax], 0x80                                    | c0 14 00 80                            |
    | rcl byte [rax + 1 * rdx], 0xff                                    | c0 14 10 ff                            |
    | rcl byte [rax + 1 * rbx], 0x00                                    | c0 14 18 00                            |
    | rcl byte [rax + 1 * rsi], 0x7f                                    | c0 14 30 7f                            |
    | rcl byte [rax + 1 * rdi], 0x80                                    | c0 14 38 80                            |
    | rcl byte [rax + 1 * r8], 0xff                                     | 42 c0 14 00 ff                         |
    | rcl byte [rax + 1 * r9], 0x00                                     | 42 c0 14 08 00                         |
    | rcl byte [rax + 1 * r11], 0x7f                                    | 42 c0 14 18 7f                         |
    | rcl byte [rax + 1 * r12], 0x80                                    | 42 c0 14 20 80                         |
    | rcl byte [rax + 1 * r13], 0xff                                    | 42 c0 14 28 ff                         |
    | rcl byte [rax + 1 * r14], 0x00                                    | 42 c0 14 30 00                         |
    | rcl byte [rax + 2 * rcx], 0x7f                                    | c0 14 48 7f                            |
    | rcl byte [rax + 4 * rcx], 0x80                                    | c0 14 88 80                            |
    | rcl byte [rax + 8 * rcx], 0xff                                    | c0 14 c8 ff                            |
    | rcl byte [r8 + 1 * r9], 0x00                                      | 43 c0 14 08 00                         |
    | rcl byte [r8 + 4 * r9], 0x7f                                      | 43 c0 14 88 7f                         |
    | rcl byte [r8 + 8 * r9], 0x80                                      | 43 c0 14 c8 80                         |
    | rcl byte [1 * rcx], 0xff                                          | c0 14 0d 00 00 00 00 ff                |
    | rcl byte [2 * rcx], 0x00                                          | c0 14 4d 00 00 00 00 00                |
    | rcl byte [8 * rcx], 0x7f                                          | c0 14 cd 00 00 00 00 7f                |
    | rcl byte [1 * r9], 0x80                                           | 42 c0 14 0d 00 00 00 00 80             |
    | rcl byte [2 * r9], 0xff                                           | 42 c0 14 4d 00 00 00 00 ff             |
    | rcl byte [4 * r9], 0x00                                           | 42 c0 14 8d 00 00 00 00 00             |
    | rcl byte [r13 + 8 * r12], 0x7f                                    | 43 c0 54 e5 00 7f                      |
    | rcl byte [rsp + 4 * r15], 0x80                                    | 42 c0 14 bc 80                         |
    | rcl byte [rax + 1 * rcx + 0x00], 0xff                             | c0 54 08 00 ff                         |
    | rcl byte [rax + 1 * rcx - 0x00], 0x00                             | c0 54 08 00 00                         |
    | rcl byte [rax + 1 * rcx - 0x01], 0x7f                             | c0 54 08 ff 7f                         |
    | rcl byte [rax + 1 * rcx + 0x00000001], 0x80                       | c0 94 08 01 00 00 00 80                |
    | rcl byte [rax + 1 * rcx - 0x00000001], 0xff                       | c0 94 08 ff ff ff ff ff                |
    | rcl byte [rax + 1 * rcx + 0x7f], 0x00                             | c0 54 08 7f 00                         |
    | rcl byte [rax + 1 * rcx + 0x80], 0x7f                             | c0 94 08 80 00 00 00 7f                |
    | rcl byte [rax + 1 * rcx - 0x80], 0x80                             | c0 54 08 80 80                         |
    | rcl byte [rax + 1 * rcx - 0x81], 0xff                             | c0 94 08 7f ff ff ff ff                |
    | rcl byte [rax + 1 * rcx + 0xff], 0x00                             | c0 94 08 ff 00 00 00 00                |
    | rcl byte [rax + 1 * rcx + 0x7fffffff], 0x7f                       | c0 94 08 ff ff ff 7f 7f                |
    | rcl byte [rax + 1 * rcx - 0x7fffffff], 0x80                       | c0 94 08 01 00 00 80 80                |
    | rcl byte [rax + 1 * rcx - 0x80000000], 0xff                       | c0 94 08 00 00 00 80 ff                |
    | rcl byte [r10 + 0x7f], 0x00                                       | 41 c0 52 7f 00                         |
    | rcl byte [r10 - 0x80], 0x7f                                       | 41 c0 52 80 7f                         |
    | rcl byte [r10 - 0x81], 0x80                                       | 41 c0 92 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; rcl byte [rel @prev5], 0xff      | 90 90 90 90 90 c0 15 f4 ff ff ff ff    |
    | .prev1: nop; rcl byte [rel @prev1], 0x00                          | 90 c0 15 f8 ff ff ff 00                |
    | rcl byte [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | c0 15 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_rcl_addr8_imm8():
    encode(RCL_ADDR8_IMM8)


RCL_ADDR8_CL = """
    | --------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                     | encoding                            |
    | --------------------------------------------------------------- | ----------------------------------- |
    | rcl byte [rax], cl                                              | d2 10                               |
    | rcl byte [rcx], cl                                              | d2 11                               |
    | rcl byte [rdx], cl                                              | d2 12                               |
    | rcl byte [rbx], cl                                              | d2 13                               |
    | rcl byte [rsp], cl                                              | d2 14 24                            |
    | rcl byte [rbp], cl                                              | d2 55 00                            |
    | rcl byte [rsi], cl                                              | d2 16                               |
    | rcl byte [rdi], cl                                              | d2 17                               |
    | rcl byte [r8], cl                                               | 41 d2 10                            |
    | rcl byte [r9], cl                                               | 41 d2 11                            |
    | rcl byte [r10], cl                                              | 41 d2 12                            |
    | rcl byte [r11], cl                                              | 41 d2 13                            |
    | rcl byte [r12], cl                                              | 41 d2 14 24                         |
    | rcl byte [r13], cl                                              | 41 d2 55 00                         |
    | rcl byte [r14], cl                                              | 41 d2 16                            |
    | rcl byte [r15], cl                                              | 41 d2 17                            |
    | rcl byte [rax + 1 * rcx], cl                                    | d2 14 08                            |
    | rcl byte [rcx + 1 * rcx], cl                                    | d2 14 09                            |
    | rcl byte [rdx + 1 * rcx], cl                                    | d2 14 0a                            |
    | rcl byte [rbx + 1 * rcx], cl                                    | d2 14 0b                            |
    | rcl byte [rsp + 1 * rcx], cl                                    | d2 14 0c                            |
    | rcl byte [rbp + 1 * rcx], cl                                    | d2 54 0d 00                         |
    | rcl byte [rsi + 1 * rcx], cl                                    | d2 14 0e                            |
    | rcl byte [rdi + 1 * rcx], cl                                    | d2 14 0f                            |
    | rcl byte [r8 + 1 * rcx], cl                                     | 41 d2 14 08                         |
    | rcl byte [r9 + 1 * rcx], cl                                     | 41 d2 14 09                         |
    | rcl byte [r10 + 1 * rcx], cl                                    | 41 d2 14 0a                         |
    | rcl byte [r11 + 1 * rcx], cl                                    | 41 d2 14 0b                         |
    | rcl byte [r12 + 1 * rcx], cl                                    | 41 d2 14 0c                         |
    | rcl byte [r13 + 1 * rcx], cl                                    | 41 d2 54 0d 00                      |
    | rcl byte [r14 + 1 * rcx], cl                                    | 41 d2 14 0e                         |
    | rcl byte [r15 + 1 * rcx], cl                                    | 41 d2 14 0f                         |
    | rcl byte [rax + 1 * rax], cl                                    | d2 14 00                            |
    | rcl byte [rax + 1 * rdx], cl                                    | d2 14 10                            |
    | rcl byte [rax + 1 * rbx], cl                                    | d2 14 18                            |
    | rcl byte [rax + 1 * rbp], cl                                    | d2 14 28                            |
    | rcl byte [rax + 1 * rsi], cl                                    | d2 14 30                            |
    | rcl byte [rax + 1 * rdi], cl                                    | d2 14 38                            |
    | rcl byte [rax + 1 * r8], cl                                     | 42 d2 14 00                         |
    | rcl byte [rax + 1 * r9], cl                                     | 42 d2 14 08                         |
    | rcl byte [rax + 1 * r10], cl                                    | 42 d2 14 10                         |
    | rcl byte [rax + 1 * r11], cl                                    | 42 d2 14 18                         |
    | rcl byte [rax + 1 * r12], cl                                    | 42 d2 14 20                         |
    | rcl byte [rax + 1 * r13], cl                                    | 42 d2 14 28                         |
    | rcl byte [rax + 1 * r14], cl                                    | 42 d2 14 30                         |
    | rcl byte [rax + 1 * r15], cl                                    | 42 d2 14 38                         |
    | rcl byte [rax + 2 * rcx], cl                                    | d2 14 48                            |
    | rcl byte [rax + 4 * rcx], cl                                    | d2 14 88                            |
    | rcl byte [rax + 8 * rcx], cl                                    | d2 14 c8                            |
    | rcl byte [r8 + 1 * r9], cl                                      | 43 d2 14 08                         |
    | rcl byte [r8 + 2 * r9], cl                                      | 43 d2 14 48                         |
    | rcl byte [r8 + 4 * r9], cl                                      | 43 d2 14 88                         |
    | rcl byte [r8 + 8 * r9], cl                                      | 43 d2 14 c8                         |
    | rcl byte [1 * rcx], cl                                          | d2 14 0d 00 00 00 00                |
    | rcl byte [2 * rcx], cl                                          | d2 14 4d 00 00 00 00                |
    | rcl byte [4 * rcx], cl                                          | d2 14 8d 00 00 00 00                |
    | rcl byte [8 * rcx], cl                                          | d2 14 cd 00 00 00 00                |
    | rcl byte [1 * r9], cl                                           | 42 d2 14 0d 00 00 00 00             |
    | rcl byte [2 * r9], cl                                           | 42 d2 14 4d 00 00 00 00             |
    | rcl byte [4 * r9], cl                                           | 42 d2 14 8d 00 00 00 00             |
    | rcl byte [8 * r9], cl                                           | 42 d2 14 cd 00 00 00 00             |
    | rcl byte [r13 + 8 * r12], cl                                    | 43 d2 54 e5 00                      |
    | rcl byte [rsp + 4 * r15], cl                                    | 42 d2 14 bc                         |
    | rcl byte [rax + 1 * rcx + 0x00], cl                             | d2 54 08 00                         |
    | rcl byte [rax + 1 * rcx - 0x00], cl                             | d2 54 08 00                         |
    | rcl byte [rax + 1 * rcx + 0x01], cl                             | d2 54 08 01                         |
    | rcl byte [rax + 1 * rcx - 0x01], cl                             | d2 54 08 ff                         |
    | rcl byte [rax + 1 * rcx + 0x00000001], cl                       | d2 94 08 01 00 00 00                |
    | rcl byte [rax + 1 * rcx - 0x00000001], cl                       | d2 94 08 ff ff ff ff                |
    | rcl byte [rax + 1 * rcx + 0x7f], cl                             | d2 54 08 7f                         |
    | rcl byte [rax + 1 * rcx - 0x7f], cl                             | d2 54 08 81                         |
    | rcl byte [rax + 1 * rcx + 0x80], cl                             | d2 94 08 80 00 00 00                |
    | rcl byte [rax + 1 * rcx - 0x80], cl                             | d2 54 08 80                         |
    | rcl byte [rax + 1 * rcx - 0x81], cl                             | d2 94 08 7f ff ff ff                |
    | rcl byte [rax + 1 * rcx + 0xff], cl                             | d2 94 08 ff 00 00 00                |
    | rcl byte [rax + 1 * rcx - 0xff], cl                             | d2 94 08 01 ff ff ff                |
    | rcl byte [rax + 1 * rcx + 0x7fffffff], cl                       | d2 94 08 ff ff ff 7f                |
    | rcl byte [rax + 1 * rcx - 0x7fffffff], cl                       | d2 94 08 01 00 00 80                |
    | rcl byte [rax + 1 * rcx - 0x80000000], cl                       | d2 94 08 00 00 00 80                |
    | rcl byte [r10 + 0x7f], cl                                       | 41 d2 52 7f                         |
    | rcl byte [r10 + 0x80], cl                                       | 41 d2 92 80 00 00 00                |
    | rcl byte [r10 - 0x80], cl                                       | 41 d2 52 80                         |
    | rcl byte [r10 - 0x81], cl                                       | 41 d2 92 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; rcl byte [rel @prev5], cl      | 90 90 90 90 90 d2 15 f5 ff ff ff    |
    | .prev1: nop; rcl byte [rel @prev1], cl                          | 90 d2 15 f9 ff ff ff                |
    | rcl byte [rel @next1], cl; nop; .next1: nop                     | d2 15 01 00 00 00 90 90             |
    | rcl byte [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | d2 15 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_rcl_addr8_cl():
    encode(RCL_ADDR8_CL)
