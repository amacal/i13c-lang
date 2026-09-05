from tests.encoding.core import encode, exhaust


def can_exhaust_sal():
    exhaust(
        SAL_ADDR16_CL,
        SAL_ADDR16_IMM8,
        SAL_ADDR32_CL,
        SAL_ADDR32_IMM8,
        SAL_ADDR64_CL,
        SAL_ADDR64_IMM8,
        SAL_ADDR8_CL,
        SAL_ADDR8_IMM8,
        SAL_REG16_CL,
        SAL_REG16_IMM8,
        SAL_REG32_CL,
        SAL_REG32_IMM8,
        SAL_REG64_CL,
        SAL_REG64_IMM8,
        SAL_REG8_CL,
        SAL_REG8_IMM8,
    )


SAL_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | sal rax, 0x01 | 48 d1 e0    | *** | sal rax, 0x00 | 48 c1 e0 00 |
    | sal rcx, 0x01 | 48 d1 e1    | *** | sal rax, 0x7f | 48 c1 e0 7f |
    | sal rdx, 0x01 | 48 d1 e2    | *** | sal rax, 0x80 | 48 c1 e0 80 |
    | sal rbx, 0x01 | 48 d1 e3    | *** | sal rax, 0xff | 48 c1 e0 ff |
    | sal rsp, 0x01 | 48 d1 e4    | *** | sal rcx, 0x7f | 48 c1 e1 7f |
    | sal rbp, 0x01 | 48 d1 e5    | *** | sal rdx, 0x80 | 48 c1 e2 80 |
    | sal rsi, 0x01 | 48 d1 e6    | *** | sal rbx, 0xff | 48 c1 e3 ff |
    | sal rdi, 0x01 | 48 d1 e7    | *** | sal rsp, 0x00 | 48 c1 e4 00 |
    | sal r8, 0x01  | 49 d1 e0    | *** | sal rsi, 0x7f | 48 c1 e6 7f |
    | sal r9, 0x01  | 49 d1 e1    | *** | sal rdi, 0x80 | 48 c1 e7 80 |
    | sal r10, 0x01 | 49 d1 e2    | *** | sal r8, 0xff  | 49 c1 e0 ff |
    | sal r11, 0x01 | 49 d1 e3    | *** | sal r9, 0x00  | 49 c1 e1 00 |
    | sal r12, 0x01 | 49 d1 e4    | *** | sal r11, 0x7f | 49 c1 e3 7f |
    | sal r13, 0x01 | 49 d1 e5    | *** | sal r12, 0x80 | 49 c1 e4 80 |
    | sal r14, 0x01 | 49 d1 e6    | *** | sal r13, 0xff | 49 c1 e5 ff |
    | sal r15, 0x01 | 49 d1 e7    | *** | sal r14, 0x00 | 49 c1 e6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_sal_reg64_imm8():
    encode(SAL_REG64_IMM8)


SAL_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | sal rax, cl | 48 d3 e0 | *** | sal r8, cl  | 49 d3 e0 |
    | sal rcx, cl | 48 d3 e1 | *** | sal r9, cl  | 49 d3 e1 |
    | sal rdx, cl | 48 d3 e2 | *** | sal r10, cl | 49 d3 e2 |
    | sal rbx, cl | 48 d3 e3 | *** | sal r11, cl | 49 d3 e3 |
    | sal rsp, cl | 48 d3 e4 | *** | sal r12, cl | 49 d3 e4 |
    | sal rbp, cl | 48 d3 e5 | *** | sal r13, cl | 49 d3 e5 |
    | sal rsi, cl | 48 d3 e6 | *** | sal r14, cl | 49 d3 e6 |
    | sal rdi, cl | 48 d3 e7 | *** | sal r15, cl | 49 d3 e7 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_sal_reg64_cl():
    encode(SAL_REG64_CL)


SAL_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sal eax, 0x01  | d1 e0       | *** | sal eax, 0x00  | c1 e0 00    |
    | sal ecx, 0x01  | d1 e1       | *** | sal eax, 0x7f  | c1 e0 7f    |
    | sal edx, 0x01  | d1 e2       | *** | sal eax, 0x80  | c1 e0 80    |
    | sal ebx, 0x01  | d1 e3       | *** | sal eax, 0xff  | c1 e0 ff    |
    | sal esp, 0x01  | d1 e4       | *** | sal ecx, 0x7f  | c1 e1 7f    |
    | sal ebp, 0x01  | d1 e5       | *** | sal edx, 0x80  | c1 e2 80    |
    | sal esi, 0x01  | d1 e6       | *** | sal ebx, 0xff  | c1 e3 ff    |
    | sal edi, 0x01  | d1 e7       | *** | sal esp, 0x00  | c1 e4 00    |
    | sal r8d, 0x01  | 41 d1 e0    | *** | sal esi, 0x7f  | c1 e6 7f    |
    | sal r9d, 0x01  | 41 d1 e1    | *** | sal edi, 0x80  | c1 e7 80    |
    | sal r10d, 0x01 | 41 d1 e2    | *** | sal r8d, 0xff  | 41 c1 e0 ff |
    | sal r11d, 0x01 | 41 d1 e3    | *** | sal r9d, 0x00  | 41 c1 e1 00 |
    | sal r12d, 0x01 | 41 d1 e4    | *** | sal r11d, 0x7f | 41 c1 e3 7f |
    | sal r13d, 0x01 | 41 d1 e5    | *** | sal r12d, 0x80 | 41 c1 e4 80 |
    | sal r14d, 0x01 | 41 d1 e6    | *** | sal r13d, 0xff | 41 c1 e5 ff |
    | sal r15d, 0x01 | 41 d1 e7    | *** | sal r14d, 0x00 | 41 c1 e6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sal_reg32_imm8():
    encode(SAL_REG32_IMM8)


SAL_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | sal eax, cl  | d3 e0    | *** | sal r8d, cl  | 41 d3 e0 |
    | sal ecx, cl  | d3 e1    | *** | sal r9d, cl  | 41 d3 e1 |
    | sal edx, cl  | d3 e2    | *** | sal r10d, cl | 41 d3 e2 |
    | sal ebx, cl  | d3 e3    | *** | sal r11d, cl | 41 d3 e3 |
    | sal esp, cl  | d3 e4    | *** | sal r12d, cl | 41 d3 e4 |
    | sal ebp, cl  | d3 e5    | *** | sal r13d, cl | 41 d3 e5 |
    | sal esi, cl  | d3 e6    | *** | sal r14d, cl | 41 d3 e6 |
    | sal edi, cl  | d3 e7    | *** | sal r15d, cl | 41 d3 e7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_sal_reg32_cl():
    encode(SAL_REG32_CL)


SAL_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | sal ax, 0x01   | 66 d1 e0       | *** | sal ax, 0x00   | 66 c1 e0 00    |
    | sal cx, 0x01   | 66 d1 e1       | *** | sal ax, 0x7f   | 66 c1 e0 7f    |
    | sal dx, 0x01   | 66 d1 e2       | *** | sal ax, 0x80   | 66 c1 e0 80    |
    | sal bx, 0x01   | 66 d1 e3       | *** | sal ax, 0xff   | 66 c1 e0 ff    |
    | sal sp, 0x01   | 66 d1 e4       | *** | sal cx, 0x7f   | 66 c1 e1 7f    |
    | sal bp, 0x01   | 66 d1 e5       | *** | sal dx, 0x80   | 66 c1 e2 80    |
    | sal si, 0x01   | 66 d1 e6       | *** | sal bx, 0xff   | 66 c1 e3 ff    |
    | sal di, 0x01   | 66 d1 e7       | *** | sal sp, 0x00   | 66 c1 e4 00    |
    | sal r8w, 0x01  | 66 41 d1 e0    | *** | sal si, 0x7f   | 66 c1 e6 7f    |
    | sal r9w, 0x01  | 66 41 d1 e1    | *** | sal di, 0x80   | 66 c1 e7 80    |
    | sal r10w, 0x01 | 66 41 d1 e2    | *** | sal r8w, 0xff  | 66 41 c1 e0 ff |
    | sal r11w, 0x01 | 66 41 d1 e3    | *** | sal r9w, 0x00  | 66 41 c1 e1 00 |
    | sal r12w, 0x01 | 66 41 d1 e4    | *** | sal r11w, 0x7f | 66 41 c1 e3 7f |
    | sal r13w, 0x01 | 66 41 d1 e5    | *** | sal r12w, 0x80 | 66 41 c1 e4 80 |
    | sal r14w, 0x01 | 66 41 d1 e6    | *** | sal r13w, 0xff | 66 41 c1 e5 ff |
    | sal r15w, 0x01 | 66 41 d1 e7    | *** | sal r14w, 0x00 | 66 41 c1 e6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_sal_reg16_imm8():
    encode(SAL_REG16_IMM8)


SAL_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | sal ax, cl   | 66 d3 e0    | *** | sal r8w, cl  | 66 41 d3 e0 |
    | sal cx, cl   | 66 d3 e1    | *** | sal r9w, cl  | 66 41 d3 e1 |
    | sal dx, cl   | 66 d3 e2    | *** | sal r10w, cl | 66 41 d3 e2 |
    | sal bx, cl   | 66 d3 e3    | *** | sal r11w, cl | 66 41 d3 e3 |
    | sal sp, cl   | 66 d3 e4    | *** | sal r12w, cl | 66 41 d3 e4 |
    | sal bp, cl   | 66 d3 e5    | *** | sal r13w, cl | 66 41 d3 e5 |
    | sal si, cl   | 66 d3 e6    | *** | sal r14w, cl | 66 41 d3 e6 |
    | sal di, cl   | 66 d3 e7    | *** | sal r15w, cl | 66 41 d3 e7 |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_sal_reg16_cl():
    encode(SAL_REG16_CL)


SAL_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sal al, 0x01   | d0 e0       | *** | sal al, 0x00   | c0 e0 00    |
    | sal cl, 0x01   | d0 e1       | *** | sal al, 0x7f   | c0 e0 7f    |
    | sal dl, 0x01   | d0 e2       | *** | sal al, 0x80   | c0 e0 80    |
    | sal bl, 0x01   | d0 e3       | *** | sal al, 0xff   | c0 e0 ff    |
    | sal spl, 0x01  | 40 d0 e4    | *** | sal cl, 0x7f   | c0 e1 7f    |
    | sal bpl, 0x01  | 40 d0 e5    | *** | sal dl, 0x80   | c0 e2 80    |
    | sal sil, 0x01  | 40 d0 e6    | *** | sal bl, 0xff   | c0 e3 ff    |
    | sal dil, 0x01  | 40 d0 e7    | *** | sal spl, 0x00  | 40 c0 e4 00 |
    | sal r8b, 0x01  | 41 d0 e0    | *** | sal sil, 0x7f  | 40 c0 e6 7f |
    | sal r9b, 0x01  | 41 d0 e1    | *** | sal dil, 0x80  | 40 c0 e7 80 |
    | sal r10b, 0x01 | 41 d0 e2    | *** | sal r8b, 0xff  | 41 c0 e0 ff |
    | sal r11b, 0x01 | 41 d0 e3    | *** | sal r9b, 0x00  | 41 c0 e1 00 |
    | sal r12b, 0x01 | 41 d0 e4    | *** | sal r11b, 0x7f | 41 c0 e3 7f |
    | sal r13b, 0x01 | 41 d0 e5    | *** | sal r12b, 0x80 | 41 c0 e4 80 |
    | sal r14b, 0x01 | 41 d0 e6    | *** | sal r13b, 0xff | 41 c0 e5 ff |
    | sal r15b, 0x01 | 41 d0 e7    | *** | sal r14b, 0x00 | 41 c0 e6 00 |
    | sal ah, 0x01   | d0 e4       | *** | sal ah, 0x7f   | c0 e4 7f    |
    | sal ch, 0x01   | d0 e5       | *** | sal ch, 0x80   | c0 e5 80    |
    | sal dh, 0x01   | d0 e6       | *** | sal dh, 0xff   | c0 e6 ff    |
    | sal bh, 0x01   | d0 e7       | *** | sal bh, 0x00   | c0 e7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sal_reg8_imm8():
    encode(SAL_REG8_IMM8)


SAL_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | sal al, cl   | d2 e0    | *** | sal r10b, cl | 41 d2 e2 |
    | sal cl, cl   | d2 e1    | *** | sal r11b, cl | 41 d2 e3 |
    | sal dl, cl   | d2 e2    | *** | sal r12b, cl | 41 d2 e4 |
    | sal bl, cl   | d2 e3    | *** | sal r13b, cl | 41 d2 e5 |
    | sal spl, cl  | 40 d2 e4 | *** | sal r14b, cl | 41 d2 e6 |
    | sal bpl, cl  | 40 d2 e5 | *** | sal r15b, cl | 41 d2 e7 |
    | sal sil, cl  | 40 d2 e6 | *** | sal ah, cl   | d2 e4    |
    | sal dil, cl  | 40 d2 e7 | *** | sal ch, cl   | d2 e5    |
    | sal r8b, cl  | 41 d2 e0 | *** | sal dh, cl   | d2 e6    |
    | sal r9b, cl  | 41 d2 e1 | *** | sal bh, cl   | d2 e7    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_sal_reg8_cl():
    encode(SAL_REG8_CL)


SAL_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sal qword [rax], 0x01                        | 48 d1 20                   |
    | sal qword [rcx], 0x01                        | 48 d1 21                   |
    | sal qword [rdx], 0x01                        | 48 d1 22                   |
    | sal qword [rbx], 0x01                        | 48 d1 23                   |
    | sal qword [rsp], 0x01                        | 48 d1 24 24                |
    | sal qword [rbp], 0x01                        | 48 d1 65 00                |
    | sal qword [rsi], 0x01                        | 48 d1 26                   |
    | sal qword [rdi], 0x01                        | 48 d1 27                   |
    | sal qword [r8], 0x01                         | 49 d1 20                   |
    | sal qword [r9], 0x01                         | 49 d1 21                   |
    | sal qword [r10], 0x01                        | 49 d1 22                   |
    | sal qword [r11], 0x01                        | 49 d1 23                   |
    | sal qword [r12], 0x01                        | 49 d1 24 24                |
    | sal qword [r13], 0x01                        | 49 d1 65 00                |
    | sal qword [r14], 0x01                        | 49 d1 26                   |
    | sal qword [r15], 0x01                        | 49 d1 27                   |
    | sal qword [rax + 1 * rcx], 0x01              | 48 d1 24 08                |
    | sal qword [rcx + 1 * rcx], 0x01              | 48 d1 24 09                |
    | sal qword [rdx + 1 * rcx], 0x01              | 48 d1 24 0a                |
    | sal qword [rbx + 1 * rcx], 0x01              | 48 d1 24 0b                |
    | sal qword [rsp + 1 * rcx], 0x01              | 48 d1 24 0c                |
    | sal qword [rbp + 1 * rcx], 0x01              | 48 d1 64 0d 00             |
    | sal qword [rsi + 1 * rcx], 0x01              | 48 d1 24 0e                |
    | sal qword [rdi + 1 * rcx], 0x01              | 48 d1 24 0f                |
    | sal qword [r8 + 1 * rcx], 0x01               | 49 d1 24 08                |
    | sal qword [r9 + 1 * rcx], 0x01               | 49 d1 24 09                |
    | sal qword [r10 + 1 * rcx], 0x01              | 49 d1 24 0a                |
    | sal qword [r11 + 1 * rcx], 0x01              | 49 d1 24 0b                |
    | sal qword [r12 + 1 * rcx], 0x01              | 49 d1 24 0c                |
    | sal qword [r13 + 1 * rcx], 0x01              | 49 d1 64 0d 00             |
    | sal qword [r14 + 1 * rcx], 0x01              | 49 d1 24 0e                |
    | sal qword [r15 + 1 * rcx], 0x01              | 49 d1 24 0f                |
    | sal qword [rax + 1 * rax], 0x01              | 48 d1 24 00                |
    | sal qword [rax + 1 * rdx], 0x01              | 48 d1 24 10                |
    | sal qword [rax + 1 * rbx], 0x01              | 48 d1 24 18                |
    | sal qword [rax + 1 * rbp], 0x01              | 48 d1 24 28                |
    | sal qword [rax + 1 * rsi], 0x01              | 48 d1 24 30                |
    | sal qword [rax + 1 * rdi], 0x01              | 48 d1 24 38                |
    | sal qword [rax + 1 * r8], 0x01               | 4a d1 24 00                |
    | sal qword [rax + 1 * r9], 0x01               | 4a d1 24 08                |
    | sal qword [rax + 1 * r10], 0x01              | 4a d1 24 10                |
    | sal qword [rax + 1 * r11], 0x01              | 4a d1 24 18                |
    | sal qword [rax + 1 * r12], 0x01              | 4a d1 24 20                |
    | sal qword [rax + 1 * r13], 0x01              | 4a d1 24 28                |
    | sal qword [rax + 1 * r14], 0x01              | 4a d1 24 30                |
    | sal qword [rax + 1 * r15], 0x01              | 4a d1 24 38                |
    | sal qword [rax + 2 * rcx], 0x01              | 48 d1 24 48                |
    | sal qword [rax + 4 * rcx], 0x01              | 48 d1 24 88                |
    | sal qword [rax + 8 * rcx], 0x01              | 48 d1 24 c8                |
    | sal qword [r8 + 1 * r9], 0x01                | 4b d1 24 08                |
    | sal qword [r8 + 2 * r9], 0x01                | 4b d1 24 48                |
    | sal qword [r8 + 4 * r9], 0x01                | 4b d1 24 88                |
    | sal qword [r8 + 8 * r9], 0x01                | 4b d1 24 c8                |
    | sal qword [1 * rcx], 0x01                    | 48 d1 24 0d 00 00 00 00    |
    | sal qword [2 * rcx], 0x01                    | 48 d1 24 4d 00 00 00 00    |
    | sal qword [4 * rcx], 0x01                    | 48 d1 24 8d 00 00 00 00    |
    | sal qword [8 * rcx], 0x01                    | 48 d1 24 cd 00 00 00 00    |
    | sal qword [1 * r9], 0x01                     | 4a d1 24 0d 00 00 00 00    |
    | sal qword [2 * r9], 0x01                     | 4a d1 24 4d 00 00 00 00    |
    | sal qword [4 * r9], 0x01                     | 4a d1 24 8d 00 00 00 00    |
    | sal qword [8 * r9], 0x01                     | 4a d1 24 cd 00 00 00 00    |
    | sal qword [r13 + 8 * r12], 0x01              | 4b d1 64 e5 00             |
    | sal qword [rsp + 4 * r15], 0x01              | 4a d1 24 bc                |
    | sal qword [rax + 1 * rcx + 0x00], 0x01       | 48 d1 64 08 00             |
    | sal qword [rax + 1 * rcx - 0x00], 0x01       | 48 d1 64 08 00             |
    | sal qword [rax + 1 * rcx + 0x01], 0x01       | 48 d1 64 08 01             |
    | sal qword [rax + 1 * rcx - 0x01], 0x01       | 48 d1 64 08 ff             |
    | sal qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 d1 a4 08 01 00 00 00    |
    | sal qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 d1 a4 08 ff ff ff ff    |
    | sal qword [rax + 1 * rcx + 0x7f], 0x01       | 48 d1 64 08 7f             |
    | sal qword [rax + 1 * rcx - 0x7f], 0x01       | 48 d1 64 08 81             |
    | sal qword [rax + 1 * rcx + 0x80], 0x01       | 48 d1 a4 08 80 00 00 00    |
    | sal qword [rax + 1 * rcx - 0x80], 0x01       | 48 d1 64 08 80             |
    | sal qword [rax + 1 * rcx - 0x81], 0x01       | 48 d1 a4 08 7f ff ff ff    |
    | sal qword [rax + 1 * rcx + 0xff], 0x01       | 48 d1 a4 08 ff 00 00 00    |
    | sal qword [rax + 1 * rcx - 0xff], 0x01       | 48 d1 a4 08 01 ff ff ff    |
    | sal qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 d1 a4 08 ff ff ff 7f    |
    | sal qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 d1 a4 08 01 00 00 80    |
    | sal qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 d1 a4 08 00 00 00 80    |
    | sal qword [r10 + 0x7f], 0x01                 | 49 d1 62 7f                |
    | sal qword [r10 + 0x80], 0x01                 | 49 d1 a2 80 00 00 00       |
    | sal qword [r10 - 0x80], 0x01                 | 49 d1 62 80                |
    | sal qword [r10 - 0x81], 0x01                 | 49 d1 a2 7f ff ff ff       |
    | sal qword [rax], 0x00                        | 48 c1 20 00                |
    | sal qword [rax], 0x7f                        | 48 c1 20 7f                |
    | sal qword [rax], 0x80                        | 48 c1 20 80                |
    | sal qword [rax], 0xff                        | 48 c1 20 ff                |
    | sal qword [rcx], 0x7f                        | 48 c1 21 7f                |
    | sal qword [rdx], 0x80                        | 48 c1 22 80                |
    | sal qword [rbx], 0xff                        | 48 c1 23 ff                |
    | sal qword [rsp], 0x00                        | 48 c1 24 24 00             |
    | sal qword [rsi], 0x7f                        | 48 c1 26 7f                |
    | sal qword [rdi], 0x80                        | 48 c1 27 80                |
    | sal qword [r8], 0xff                         | 49 c1 20 ff                |
    | sal qword [r9], 0x00                         | 49 c1 21 00                |
    | sal qword [r11], 0x7f                        | 49 c1 23 7f                |
    | sal qword [r12], 0x80                        | 49 c1 24 24 80             |
    | sal qword [r13], 0xff                        | 49 c1 65 00 ff             |
    | sal qword [r14], 0x00                        | 49 c1 26 00                |
    | sal qword [rax + 1 * rcx], 0x7f              | 48 c1 24 08 7f             |
    | sal qword [rcx + 1 * rcx], 0x80              | 48 c1 24 09 80             |
    | sal qword [rdx + 1 * rcx], 0xff              | 48 c1 24 0a ff             |
    | sal qword [rbx + 1 * rcx], 0x00              | 48 c1 24 0b 00             |
    | sal qword [rbp + 1 * rcx], 0x7f              | 48 c1 64 0d 00 7f          |
    | sal qword [rsi + 1 * rcx], 0x80              | 48 c1 24 0e 80             |
    | sal qword [rdi + 1 * rcx], 0xff              | 48 c1 24 0f ff             |
    | sal qword [r8 + 1 * rcx], 0x00               | 49 c1 24 08 00             |
    | sal qword [r10 + 1 * rcx], 0x7f              | 49 c1 24 0a 7f             |
    | sal qword [r11 + 1 * rcx], 0x80              | 49 c1 24 0b 80             |
    | sal qword [r12 + 1 * rcx], 0xff              | 49 c1 24 0c ff             |
    | sal qword [r13 + 1 * rcx], 0x00              | 49 c1 64 0d 00 00          |
    | sal qword [r15 + 1 * rcx], 0x7f              | 49 c1 24 0f 7f             |
    | sal qword [rax + 1 * rax], 0x80              | 48 c1 24 00 80             |
    | sal qword [rax + 1 * rdx], 0xff              | 48 c1 24 10 ff             |
    | sal qword [rax + 1 * rbx], 0x00              | 48 c1 24 18 00             |
    | sal qword [rax + 1 * rsi], 0x7f              | 48 c1 24 30 7f             |
    | sal qword [rax + 1 * rdi], 0x80              | 48 c1 24 38 80             |
    | sal qword [rax + 1 * r8], 0xff               | 4a c1 24 00 ff             |
    | sal qword [rax + 1 * r9], 0x00               | 4a c1 24 08 00             |
    | sal qword [rax + 1 * r11], 0x7f              | 4a c1 24 18 7f             |
    | sal qword [rax + 1 * r12], 0x80              | 4a c1 24 20 80             |
    | sal qword [rax + 1 * r13], 0xff              | 4a c1 24 28 ff             |
    | sal qword [rax + 1 * r14], 0x00              | 4a c1 24 30 00             |
    | sal qword [rax + 2 * rcx], 0x7f              | 48 c1 24 48 7f             |
    | sal qword [rax + 4 * rcx], 0x80              | 48 c1 24 88 80             |
    | sal qword [rax + 8 * rcx], 0xff              | 48 c1 24 c8 ff             |
    | sal qword [r8 + 1 * r9], 0x00                | 4b c1 24 08 00             |
    | sal qword [r8 + 4 * r9], 0x7f                | 4b c1 24 88 7f             |
    | sal qword [r8 + 8 * r9], 0x80                | 4b c1 24 c8 80             |
    | sal qword [1 * rcx], 0xff                    | 48 c1 24 0d 00 00 00 00 ff |
    | sal qword [2 * rcx], 0x00                    | 48 c1 24 4d 00 00 00 00 00 |
    | sal qword [8 * rcx], 0x7f                    | 48 c1 24 cd 00 00 00 00 7f |
    | sal qword [1 * r9], 0x80                     | 4a c1 24 0d 00 00 00 00 80 |
    | sal qword [2 * r9], 0xff                     | 4a c1 24 4d 00 00 00 00 ff |
    | sal qword [4 * r9], 0x00                     | 4a c1 24 8d 00 00 00 00 00 |
    | sal qword [r13 + 8 * r12], 0x7f              | 4b c1 64 e5 00 7f          |
    | sal qword [rsp + 4 * r15], 0x80              | 4a c1 24 bc 80             |
    | sal qword [rax + 1 * rcx + 0x00], 0xff       | 48 c1 64 08 00 ff          |
    | sal qword [rax + 1 * rcx - 0x00], 0x00       | 48 c1 64 08 00 00          |
    | sal qword [rax + 1 * rcx - 0x01], 0x7f       | 48 c1 64 08 ff 7f          |
    | sal qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 c1 a4 08 01 00 00 00 80 |
    | sal qword [rax + 1 * rcx - 0x00000001], 0xff | 48 c1 a4 08 ff ff ff ff ff |
    | sal qword [rax + 1 * rcx + 0x7f], 0x00       | 48 c1 64 08 7f 00          |
    | sal qword [rax + 1 * rcx + 0x80], 0x7f       | 48 c1 a4 08 80 00 00 00 7f |
    | sal qword [rax + 1 * rcx - 0x80], 0x80       | 48 c1 64 08 80 80          |
    | sal qword [rax + 1 * rcx - 0x81], 0xff       | 48 c1 a4 08 7f ff ff ff ff |
    | sal qword [rax + 1 * rcx + 0xff], 0x00       | 48 c1 a4 08 ff 00 00 00 00 |
    | sal qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 c1 a4 08 ff ff ff 7f 7f |
    | sal qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 c1 a4 08 01 00 00 80 80 |
    | sal qword [rax + 1 * rcx - 0x80000000], 0xff | 48 c1 a4 08 00 00 00 80 ff |
    | sal qword [r10 + 0x7f], 0x00                 | 49 c1 62 7f 00             |
    | sal qword [r10 - 0x80], 0x7f                 | 49 c1 62 80 7f             |
    | sal qword [r10 - 0x81], 0x80                 | 49 c1 a2 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sal_addr64_imm8():
    encode(SAL_ADDR64_IMM8)


SAL_ADDR64_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | sal qword [rax], cl                        | 48 d3 20                |
    | sal qword [rcx], cl                        | 48 d3 21                |
    | sal qword [rdx], cl                        | 48 d3 22                |
    | sal qword [rbx], cl                        | 48 d3 23                |
    | sal qword [rsp], cl                        | 48 d3 24 24             |
    | sal qword [rbp], cl                        | 48 d3 65 00             |
    | sal qword [rsi], cl                        | 48 d3 26                |
    | sal qword [rdi], cl                        | 48 d3 27                |
    | sal qword [r8], cl                         | 49 d3 20                |
    | sal qword [r9], cl                         | 49 d3 21                |
    | sal qword [r10], cl                        | 49 d3 22                |
    | sal qword [r11], cl                        | 49 d3 23                |
    | sal qword [r12], cl                        | 49 d3 24 24             |
    | sal qword [r13], cl                        | 49 d3 65 00             |
    | sal qword [r14], cl                        | 49 d3 26                |
    | sal qword [r15], cl                        | 49 d3 27                |
    | sal qword [rax + 1 * rcx], cl              | 48 d3 24 08             |
    | sal qword [rcx + 1 * rcx], cl              | 48 d3 24 09             |
    | sal qword [rdx + 1 * rcx], cl              | 48 d3 24 0a             |
    | sal qword [rbx + 1 * rcx], cl              | 48 d3 24 0b             |
    | sal qword [rsp + 1 * rcx], cl              | 48 d3 24 0c             |
    | sal qword [rbp + 1 * rcx], cl              | 48 d3 64 0d 00          |
    | sal qword [rsi + 1 * rcx], cl              | 48 d3 24 0e             |
    | sal qword [rdi + 1 * rcx], cl              | 48 d3 24 0f             |
    | sal qword [r8 + 1 * rcx], cl               | 49 d3 24 08             |
    | sal qword [r9 + 1 * rcx], cl               | 49 d3 24 09             |
    | sal qword [r10 + 1 * rcx], cl              | 49 d3 24 0a             |
    | sal qword [r11 + 1 * rcx], cl              | 49 d3 24 0b             |
    | sal qword [r12 + 1 * rcx], cl              | 49 d3 24 0c             |
    | sal qword [r13 + 1 * rcx], cl              | 49 d3 64 0d 00          |
    | sal qword [r14 + 1 * rcx], cl              | 49 d3 24 0e             |
    | sal qword [r15 + 1 * rcx], cl              | 49 d3 24 0f             |
    | sal qword [rax + 1 * rax], cl              | 48 d3 24 00             |
    | sal qword [rax + 1 * rdx], cl              | 48 d3 24 10             |
    | sal qword [rax + 1 * rbx], cl              | 48 d3 24 18             |
    | sal qword [rax + 1 * rbp], cl              | 48 d3 24 28             |
    | sal qword [rax + 1 * rsi], cl              | 48 d3 24 30             |
    | sal qword [rax + 1 * rdi], cl              | 48 d3 24 38             |
    | sal qword [rax + 1 * r8], cl               | 4a d3 24 00             |
    | sal qword [rax + 1 * r9], cl               | 4a d3 24 08             |
    | sal qword [rax + 1 * r10], cl              | 4a d3 24 10             |
    | sal qword [rax + 1 * r11], cl              | 4a d3 24 18             |
    | sal qword [rax + 1 * r12], cl              | 4a d3 24 20             |
    | sal qword [rax + 1 * r13], cl              | 4a d3 24 28             |
    | sal qword [rax + 1 * r14], cl              | 4a d3 24 30             |
    | sal qword [rax + 1 * r15], cl              | 4a d3 24 38             |
    | sal qword [rax + 2 * rcx], cl              | 48 d3 24 48             |
    | sal qword [rax + 4 * rcx], cl              | 48 d3 24 88             |
    | sal qword [rax + 8 * rcx], cl              | 48 d3 24 c8             |
    | sal qword [r8 + 1 * r9], cl                | 4b d3 24 08             |
    | sal qword [r8 + 2 * r9], cl                | 4b d3 24 48             |
    | sal qword [r8 + 4 * r9], cl                | 4b d3 24 88             |
    | sal qword [r8 + 8 * r9], cl                | 4b d3 24 c8             |
    | sal qword [1 * rcx], cl                    | 48 d3 24 0d 00 00 00 00 |
    | sal qword [2 * rcx], cl                    | 48 d3 24 4d 00 00 00 00 |
    | sal qword [4 * rcx], cl                    | 48 d3 24 8d 00 00 00 00 |
    | sal qword [8 * rcx], cl                    | 48 d3 24 cd 00 00 00 00 |
    | sal qword [1 * r9], cl                     | 4a d3 24 0d 00 00 00 00 |
    | sal qword [2 * r9], cl                     | 4a d3 24 4d 00 00 00 00 |
    | sal qword [4 * r9], cl                     | 4a d3 24 8d 00 00 00 00 |
    | sal qword [8 * r9], cl                     | 4a d3 24 cd 00 00 00 00 |
    | sal qword [r13 + 8 * r12], cl              | 4b d3 64 e5 00          |
    | sal qword [rsp + 4 * r15], cl              | 4a d3 24 bc             |
    | sal qword [rax + 1 * rcx + 0x00], cl       | 48 d3 64 08 00          |
    | sal qword [rax + 1 * rcx - 0x00], cl       | 48 d3 64 08 00          |
    | sal qword [rax + 1 * rcx + 0x01], cl       | 48 d3 64 08 01          |
    | sal qword [rax + 1 * rcx - 0x01], cl       | 48 d3 64 08 ff          |
    | sal qword [rax + 1 * rcx + 0x00000001], cl | 48 d3 a4 08 01 00 00 00 |
    | sal qword [rax + 1 * rcx - 0x00000001], cl | 48 d3 a4 08 ff ff ff ff |
    | sal qword [rax + 1 * rcx + 0x7f], cl       | 48 d3 64 08 7f          |
    | sal qword [rax + 1 * rcx - 0x7f], cl       | 48 d3 64 08 81          |
    | sal qword [rax + 1 * rcx + 0x80], cl       | 48 d3 a4 08 80 00 00 00 |
    | sal qword [rax + 1 * rcx - 0x80], cl       | 48 d3 64 08 80          |
    | sal qword [rax + 1 * rcx - 0x81], cl       | 48 d3 a4 08 7f ff ff ff |
    | sal qword [rax + 1 * rcx + 0xff], cl       | 48 d3 a4 08 ff 00 00 00 |
    | sal qword [rax + 1 * rcx - 0xff], cl       | 48 d3 a4 08 01 ff ff ff |
    | sal qword [rax + 1 * rcx + 0x7fffffff], cl | 48 d3 a4 08 ff ff ff 7f |
    | sal qword [rax + 1 * rcx - 0x7fffffff], cl | 48 d3 a4 08 01 00 00 80 |
    | sal qword [rax + 1 * rcx - 0x80000000], cl | 48 d3 a4 08 00 00 00 80 |
    | sal qword [r10 + 0x7f], cl                 | 49 d3 62 7f             |
    | sal qword [r10 + 0x80], cl                 | 49 d3 a2 80 00 00 00    |
    | sal qword [r10 - 0x80], cl                 | 49 d3 62 80             |
    | sal qword [r10 - 0x81], cl                 | 49 d3 a2 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_sal_addr64_cl():
    encode(SAL_ADDR64_CL)


SAL_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sal dword [rax], 0x01                        | d1 20                      |
    | sal dword [rcx], 0x01                        | d1 21                      |
    | sal dword [rdx], 0x01                        | d1 22                      |
    | sal dword [rbx], 0x01                        | d1 23                      |
    | sal dword [rsp], 0x01                        | d1 24 24                   |
    | sal dword [rbp], 0x01                        | d1 65 00                   |
    | sal dword [rsi], 0x01                        | d1 26                      |
    | sal dword [rdi], 0x01                        | d1 27                      |
    | sal dword [r8], 0x01                         | 41 d1 20                   |
    | sal dword [r9], 0x01                         | 41 d1 21                   |
    | sal dword [r10], 0x01                        | 41 d1 22                   |
    | sal dword [r11], 0x01                        | 41 d1 23                   |
    | sal dword [r12], 0x01                        | 41 d1 24 24                |
    | sal dword [r13], 0x01                        | 41 d1 65 00                |
    | sal dword [r14], 0x01                        | 41 d1 26                   |
    | sal dword [r15], 0x01                        | 41 d1 27                   |
    | sal dword [rax + 1 * rcx], 0x01              | d1 24 08                   |
    | sal dword [rcx + 1 * rcx], 0x01              | d1 24 09                   |
    | sal dword [rdx + 1 * rcx], 0x01              | d1 24 0a                   |
    | sal dword [rbx + 1 * rcx], 0x01              | d1 24 0b                   |
    | sal dword [rsp + 1 * rcx], 0x01              | d1 24 0c                   |
    | sal dword [rbp + 1 * rcx], 0x01              | d1 64 0d 00                |
    | sal dword [rsi + 1 * rcx], 0x01              | d1 24 0e                   |
    | sal dword [rdi + 1 * rcx], 0x01              | d1 24 0f                   |
    | sal dword [r8 + 1 * rcx], 0x01               | 41 d1 24 08                |
    | sal dword [r9 + 1 * rcx], 0x01               | 41 d1 24 09                |
    | sal dword [r10 + 1 * rcx], 0x01              | 41 d1 24 0a                |
    | sal dword [r11 + 1 * rcx], 0x01              | 41 d1 24 0b                |
    | sal dword [r12 + 1 * rcx], 0x01              | 41 d1 24 0c                |
    | sal dword [r13 + 1 * rcx], 0x01              | 41 d1 64 0d 00             |
    | sal dword [r14 + 1 * rcx], 0x01              | 41 d1 24 0e                |
    | sal dword [r15 + 1 * rcx], 0x01              | 41 d1 24 0f                |
    | sal dword [rax + 1 * rax], 0x01              | d1 24 00                   |
    | sal dword [rax + 1 * rdx], 0x01              | d1 24 10                   |
    | sal dword [rax + 1 * rbx], 0x01              | d1 24 18                   |
    | sal dword [rax + 1 * rbp], 0x01              | d1 24 28                   |
    | sal dword [rax + 1 * rsi], 0x01              | d1 24 30                   |
    | sal dword [rax + 1 * rdi], 0x01              | d1 24 38                   |
    | sal dword [rax + 1 * r8], 0x01               | 42 d1 24 00                |
    | sal dword [rax + 1 * r9], 0x01               | 42 d1 24 08                |
    | sal dword [rax + 1 * r10], 0x01              | 42 d1 24 10                |
    | sal dword [rax + 1 * r11], 0x01              | 42 d1 24 18                |
    | sal dword [rax + 1 * r12], 0x01              | 42 d1 24 20                |
    | sal dword [rax + 1 * r13], 0x01              | 42 d1 24 28                |
    | sal dword [rax + 1 * r14], 0x01              | 42 d1 24 30                |
    | sal dword [rax + 1 * r15], 0x01              | 42 d1 24 38                |
    | sal dword [rax + 2 * rcx], 0x01              | d1 24 48                   |
    | sal dword [rax + 4 * rcx], 0x01              | d1 24 88                   |
    | sal dword [rax + 8 * rcx], 0x01              | d1 24 c8                   |
    | sal dword [r8 + 1 * r9], 0x01                | 43 d1 24 08                |
    | sal dword [r8 + 2 * r9], 0x01                | 43 d1 24 48                |
    | sal dword [r8 + 4 * r9], 0x01                | 43 d1 24 88                |
    | sal dword [r8 + 8 * r9], 0x01                | 43 d1 24 c8                |
    | sal dword [1 * rcx], 0x01                    | d1 24 0d 00 00 00 00       |
    | sal dword [2 * rcx], 0x01                    | d1 24 4d 00 00 00 00       |
    | sal dword [4 * rcx], 0x01                    | d1 24 8d 00 00 00 00       |
    | sal dword [8 * rcx], 0x01                    | d1 24 cd 00 00 00 00       |
    | sal dword [1 * r9], 0x01                     | 42 d1 24 0d 00 00 00 00    |
    | sal dword [2 * r9], 0x01                     | 42 d1 24 4d 00 00 00 00    |
    | sal dword [4 * r9], 0x01                     | 42 d1 24 8d 00 00 00 00    |
    | sal dword [8 * r9], 0x01                     | 42 d1 24 cd 00 00 00 00    |
    | sal dword [r13 + 8 * r12], 0x01              | 43 d1 64 e5 00             |
    | sal dword [rsp + 4 * r15], 0x01              | 42 d1 24 bc                |
    | sal dword [rax + 1 * rcx + 0x00], 0x01       | d1 64 08 00                |
    | sal dword [rax + 1 * rcx - 0x00], 0x01       | d1 64 08 00                |
    | sal dword [rax + 1 * rcx + 0x01], 0x01       | d1 64 08 01                |
    | sal dword [rax + 1 * rcx - 0x01], 0x01       | d1 64 08 ff                |
    | sal dword [rax + 1 * rcx + 0x00000001], 0x01 | d1 a4 08 01 00 00 00       |
    | sal dword [rax + 1 * rcx - 0x00000001], 0x01 | d1 a4 08 ff ff ff ff       |
    | sal dword [rax + 1 * rcx + 0x7f], 0x01       | d1 64 08 7f                |
    | sal dword [rax + 1 * rcx - 0x7f], 0x01       | d1 64 08 81                |
    | sal dword [rax + 1 * rcx + 0x80], 0x01       | d1 a4 08 80 00 00 00       |
    | sal dword [rax + 1 * rcx - 0x80], 0x01       | d1 64 08 80                |
    | sal dword [rax + 1 * rcx - 0x81], 0x01       | d1 a4 08 7f ff ff ff       |
    | sal dword [rax + 1 * rcx + 0xff], 0x01       | d1 a4 08 ff 00 00 00       |
    | sal dword [rax + 1 * rcx - 0xff], 0x01       | d1 a4 08 01 ff ff ff       |
    | sal dword [rax + 1 * rcx + 0x7fffffff], 0x01 | d1 a4 08 ff ff ff 7f       |
    | sal dword [rax + 1 * rcx - 0x7fffffff], 0x01 | d1 a4 08 01 00 00 80       |
    | sal dword [rax + 1 * rcx - 0x80000000], 0x01 | d1 a4 08 00 00 00 80       |
    | sal dword [r10 + 0x7f], 0x01                 | 41 d1 62 7f                |
    | sal dword [r10 + 0x80], 0x01                 | 41 d1 a2 80 00 00 00       |
    | sal dword [r10 - 0x80], 0x01                 | 41 d1 62 80                |
    | sal dword [r10 - 0x81], 0x01                 | 41 d1 a2 7f ff ff ff       |
    | sal dword [rax], 0x00                        | c1 20 00                   |
    | sal dword [rax], 0x7f                        | c1 20 7f                   |
    | sal dword [rax], 0x80                        | c1 20 80                   |
    | sal dword [rax], 0xff                        | c1 20 ff                   |
    | sal dword [rcx], 0x7f                        | c1 21 7f                   |
    | sal dword [rdx], 0x80                        | c1 22 80                   |
    | sal dword [rbx], 0xff                        | c1 23 ff                   |
    | sal dword [rsp], 0x00                        | c1 24 24 00                |
    | sal dword [rsi], 0x7f                        | c1 26 7f                   |
    | sal dword [rdi], 0x80                        | c1 27 80                   |
    | sal dword [r8], 0xff                         | 41 c1 20 ff                |
    | sal dword [r9], 0x00                         | 41 c1 21 00                |
    | sal dword [r11], 0x7f                        | 41 c1 23 7f                |
    | sal dword [r12], 0x80                        | 41 c1 24 24 80             |
    | sal dword [r13], 0xff                        | 41 c1 65 00 ff             |
    | sal dword [r14], 0x00                        | 41 c1 26 00                |
    | sal dword [rax + 1 * rcx], 0x7f              | c1 24 08 7f                |
    | sal dword [rcx + 1 * rcx], 0x80              | c1 24 09 80                |
    | sal dword [rdx + 1 * rcx], 0xff              | c1 24 0a ff                |
    | sal dword [rbx + 1 * rcx], 0x00              | c1 24 0b 00                |
    | sal dword [rbp + 1 * rcx], 0x7f              | c1 64 0d 00 7f             |
    | sal dword [rsi + 1 * rcx], 0x80              | c1 24 0e 80                |
    | sal dword [rdi + 1 * rcx], 0xff              | c1 24 0f ff                |
    | sal dword [r8 + 1 * rcx], 0x00               | 41 c1 24 08 00             |
    | sal dword [r10 + 1 * rcx], 0x7f              | 41 c1 24 0a 7f             |
    | sal dword [r11 + 1 * rcx], 0x80              | 41 c1 24 0b 80             |
    | sal dword [r12 + 1 * rcx], 0xff              | 41 c1 24 0c ff             |
    | sal dword [r13 + 1 * rcx], 0x00              | 41 c1 64 0d 00 00          |
    | sal dword [r15 + 1 * rcx], 0x7f              | 41 c1 24 0f 7f             |
    | sal dword [rax + 1 * rax], 0x80              | c1 24 00 80                |
    | sal dword [rax + 1 * rdx], 0xff              | c1 24 10 ff                |
    | sal dword [rax + 1 * rbx], 0x00              | c1 24 18 00                |
    | sal dword [rax + 1 * rsi], 0x7f              | c1 24 30 7f                |
    | sal dword [rax + 1 * rdi], 0x80              | c1 24 38 80                |
    | sal dword [rax + 1 * r8], 0xff               | 42 c1 24 00 ff             |
    | sal dword [rax + 1 * r9], 0x00               | 42 c1 24 08 00             |
    | sal dword [rax + 1 * r11], 0x7f              | 42 c1 24 18 7f             |
    | sal dword [rax + 1 * r12], 0x80              | 42 c1 24 20 80             |
    | sal dword [rax + 1 * r13], 0xff              | 42 c1 24 28 ff             |
    | sal dword [rax + 1 * r14], 0x00              | 42 c1 24 30 00             |
    | sal dword [rax + 2 * rcx], 0x7f              | c1 24 48 7f                |
    | sal dword [rax + 4 * rcx], 0x80              | c1 24 88 80                |
    | sal dword [rax + 8 * rcx], 0xff              | c1 24 c8 ff                |
    | sal dword [r8 + 1 * r9], 0x00                | 43 c1 24 08 00             |
    | sal dword [r8 + 4 * r9], 0x7f                | 43 c1 24 88 7f             |
    | sal dword [r8 + 8 * r9], 0x80                | 43 c1 24 c8 80             |
    | sal dword [1 * rcx], 0xff                    | c1 24 0d 00 00 00 00 ff    |
    | sal dword [2 * rcx], 0x00                    | c1 24 4d 00 00 00 00 00    |
    | sal dword [8 * rcx], 0x7f                    | c1 24 cd 00 00 00 00 7f    |
    | sal dword [1 * r9], 0x80                     | 42 c1 24 0d 00 00 00 00 80 |
    | sal dword [2 * r9], 0xff                     | 42 c1 24 4d 00 00 00 00 ff |
    | sal dword [4 * r9], 0x00                     | 42 c1 24 8d 00 00 00 00 00 |
    | sal dword [r13 + 8 * r12], 0x7f              | 43 c1 64 e5 00 7f          |
    | sal dword [rsp + 4 * r15], 0x80              | 42 c1 24 bc 80             |
    | sal dword [rax + 1 * rcx + 0x00], 0xff       | c1 64 08 00 ff             |
    | sal dword [rax + 1 * rcx - 0x00], 0x00       | c1 64 08 00 00             |
    | sal dword [rax + 1 * rcx - 0x01], 0x7f       | c1 64 08 ff 7f             |
    | sal dword [rax + 1 * rcx + 0x00000001], 0x80 | c1 a4 08 01 00 00 00 80    |
    | sal dword [rax + 1 * rcx - 0x00000001], 0xff | c1 a4 08 ff ff ff ff ff    |
    | sal dword [rax + 1 * rcx + 0x7f], 0x00       | c1 64 08 7f 00             |
    | sal dword [rax + 1 * rcx + 0x80], 0x7f       | c1 a4 08 80 00 00 00 7f    |
    | sal dword [rax + 1 * rcx - 0x80], 0x80       | c1 64 08 80 80             |
    | sal dword [rax + 1 * rcx - 0x81], 0xff       | c1 a4 08 7f ff ff ff ff    |
    | sal dword [rax + 1 * rcx + 0xff], 0x00       | c1 a4 08 ff 00 00 00 00    |
    | sal dword [rax + 1 * rcx + 0x7fffffff], 0x7f | c1 a4 08 ff ff ff 7f 7f    |
    | sal dword [rax + 1 * rcx - 0x7fffffff], 0x80 | c1 a4 08 01 00 00 80 80    |
    | sal dword [rax + 1 * rcx - 0x80000000], 0xff | c1 a4 08 00 00 00 80 ff    |
    | sal dword [r10 + 0x7f], 0x00                 | 41 c1 62 7f 00             |
    | sal dword [r10 - 0x80], 0x7f                 | 41 c1 62 80 7f             |
    | sal dword [r10 - 0x81], 0x80                 | 41 c1 a2 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sal_addr32_imm8():
    encode(SAL_ADDR32_IMM8)


SAL_ADDR32_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | sal dword [rax], cl                        | d3 20                   |
    | sal dword [rcx], cl                        | d3 21                   |
    | sal dword [rdx], cl                        | d3 22                   |
    | sal dword [rbx], cl                        | d3 23                   |
    | sal dword [rsp], cl                        | d3 24 24                |
    | sal dword [rbp], cl                        | d3 65 00                |
    | sal dword [rsi], cl                        | d3 26                   |
    | sal dword [rdi], cl                        | d3 27                   |
    | sal dword [r8], cl                         | 41 d3 20                |
    | sal dword [r9], cl                         | 41 d3 21                |
    | sal dword [r10], cl                        | 41 d3 22                |
    | sal dword [r11], cl                        | 41 d3 23                |
    | sal dword [r12], cl                        | 41 d3 24 24             |
    | sal dword [r13], cl                        | 41 d3 65 00             |
    | sal dword [r14], cl                        | 41 d3 26                |
    | sal dword [r15], cl                        | 41 d3 27                |
    | sal dword [rax + 1 * rcx], cl              | d3 24 08                |
    | sal dword [rcx + 1 * rcx], cl              | d3 24 09                |
    | sal dword [rdx + 1 * rcx], cl              | d3 24 0a                |
    | sal dword [rbx + 1 * rcx], cl              | d3 24 0b                |
    | sal dword [rsp + 1 * rcx], cl              | d3 24 0c                |
    | sal dword [rbp + 1 * rcx], cl              | d3 64 0d 00             |
    | sal dword [rsi + 1 * rcx], cl              | d3 24 0e                |
    | sal dword [rdi + 1 * rcx], cl              | d3 24 0f                |
    | sal dword [r8 + 1 * rcx], cl               | 41 d3 24 08             |
    | sal dword [r9 + 1 * rcx], cl               | 41 d3 24 09             |
    | sal dword [r10 + 1 * rcx], cl              | 41 d3 24 0a             |
    | sal dword [r11 + 1 * rcx], cl              | 41 d3 24 0b             |
    | sal dword [r12 + 1 * rcx], cl              | 41 d3 24 0c             |
    | sal dword [r13 + 1 * rcx], cl              | 41 d3 64 0d 00          |
    | sal dword [r14 + 1 * rcx], cl              | 41 d3 24 0e             |
    | sal dword [r15 + 1 * rcx], cl              | 41 d3 24 0f             |
    | sal dword [rax + 1 * rax], cl              | d3 24 00                |
    | sal dword [rax + 1 * rdx], cl              | d3 24 10                |
    | sal dword [rax + 1 * rbx], cl              | d3 24 18                |
    | sal dword [rax + 1 * rbp], cl              | d3 24 28                |
    | sal dword [rax + 1 * rsi], cl              | d3 24 30                |
    | sal dword [rax + 1 * rdi], cl              | d3 24 38                |
    | sal dword [rax + 1 * r8], cl               | 42 d3 24 00             |
    | sal dword [rax + 1 * r9], cl               | 42 d3 24 08             |
    | sal dword [rax + 1 * r10], cl              | 42 d3 24 10             |
    | sal dword [rax + 1 * r11], cl              | 42 d3 24 18             |
    | sal dword [rax + 1 * r12], cl              | 42 d3 24 20             |
    | sal dword [rax + 1 * r13], cl              | 42 d3 24 28             |
    | sal dword [rax + 1 * r14], cl              | 42 d3 24 30             |
    | sal dword [rax + 1 * r15], cl              | 42 d3 24 38             |
    | sal dword [rax + 2 * rcx], cl              | d3 24 48                |
    | sal dword [rax + 4 * rcx], cl              | d3 24 88                |
    | sal dword [rax + 8 * rcx], cl              | d3 24 c8                |
    | sal dword [r8 + 1 * r9], cl                | 43 d3 24 08             |
    | sal dword [r8 + 2 * r9], cl                | 43 d3 24 48             |
    | sal dword [r8 + 4 * r9], cl                | 43 d3 24 88             |
    | sal dword [r8 + 8 * r9], cl                | 43 d3 24 c8             |
    | sal dword [1 * rcx], cl                    | d3 24 0d 00 00 00 00    |
    | sal dword [2 * rcx], cl                    | d3 24 4d 00 00 00 00    |
    | sal dword [4 * rcx], cl                    | d3 24 8d 00 00 00 00    |
    | sal dword [8 * rcx], cl                    | d3 24 cd 00 00 00 00    |
    | sal dword [1 * r9], cl                     | 42 d3 24 0d 00 00 00 00 |
    | sal dword [2 * r9], cl                     | 42 d3 24 4d 00 00 00 00 |
    | sal dword [4 * r9], cl                     | 42 d3 24 8d 00 00 00 00 |
    | sal dword [8 * r9], cl                     | 42 d3 24 cd 00 00 00 00 |
    | sal dword [r13 + 8 * r12], cl              | 43 d3 64 e5 00          |
    | sal dword [rsp + 4 * r15], cl              | 42 d3 24 bc             |
    | sal dword [rax + 1 * rcx + 0x00], cl       | d3 64 08 00             |
    | sal dword [rax + 1 * rcx - 0x00], cl       | d3 64 08 00             |
    | sal dword [rax + 1 * rcx + 0x01], cl       | d3 64 08 01             |
    | sal dword [rax + 1 * rcx - 0x01], cl       | d3 64 08 ff             |
    | sal dword [rax + 1 * rcx + 0x00000001], cl | d3 a4 08 01 00 00 00    |
    | sal dword [rax + 1 * rcx - 0x00000001], cl | d3 a4 08 ff ff ff ff    |
    | sal dword [rax + 1 * rcx + 0x7f], cl       | d3 64 08 7f             |
    | sal dword [rax + 1 * rcx - 0x7f], cl       | d3 64 08 81             |
    | sal dword [rax + 1 * rcx + 0x80], cl       | d3 a4 08 80 00 00 00    |
    | sal dword [rax + 1 * rcx - 0x80], cl       | d3 64 08 80             |
    | sal dword [rax + 1 * rcx - 0x81], cl       | d3 a4 08 7f ff ff ff    |
    | sal dword [rax + 1 * rcx + 0xff], cl       | d3 a4 08 ff 00 00 00    |
    | sal dword [rax + 1 * rcx - 0xff], cl       | d3 a4 08 01 ff ff ff    |
    | sal dword [rax + 1 * rcx + 0x7fffffff], cl | d3 a4 08 ff ff ff 7f    |
    | sal dword [rax + 1 * rcx - 0x7fffffff], cl | d3 a4 08 01 00 00 80    |
    | sal dword [rax + 1 * rcx - 0x80000000], cl | d3 a4 08 00 00 00 80    |
    | sal dword [r10 + 0x7f], cl                 | 41 d3 62 7f             |
    | sal dword [r10 + 0x80], cl                 | 41 d3 a2 80 00 00 00    |
    | sal dword [r10 - 0x80], cl                 | 41 d3 62 80             |
    | sal dword [r10 - 0x81], cl                 | 41 d3 a2 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_sal_addr32_cl():
    encode(SAL_ADDR32_CL)


SAL_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | sal word [rax], 0x01                        | 66 d1 20                      |
    | sal word [rcx], 0x01                        | 66 d1 21                      |
    | sal word [rdx], 0x01                        | 66 d1 22                      |
    | sal word [rbx], 0x01                        | 66 d1 23                      |
    | sal word [rsp], 0x01                        | 66 d1 24 24                   |
    | sal word [rbp], 0x01                        | 66 d1 65 00                   |
    | sal word [rsi], 0x01                        | 66 d1 26                      |
    | sal word [rdi], 0x01                        | 66 d1 27                      |
    | sal word [r8], 0x01                         | 66 41 d1 20                   |
    | sal word [r9], 0x01                         | 66 41 d1 21                   |
    | sal word [r10], 0x01                        | 66 41 d1 22                   |
    | sal word [r11], 0x01                        | 66 41 d1 23                   |
    | sal word [r12], 0x01                        | 66 41 d1 24 24                |
    | sal word [r13], 0x01                        | 66 41 d1 65 00                |
    | sal word [r14], 0x01                        | 66 41 d1 26                   |
    | sal word [r15], 0x01                        | 66 41 d1 27                   |
    | sal word [rax + 1 * rcx], 0x01              | 66 d1 24 08                   |
    | sal word [rcx + 1 * rcx], 0x01              | 66 d1 24 09                   |
    | sal word [rdx + 1 * rcx], 0x01              | 66 d1 24 0a                   |
    | sal word [rbx + 1 * rcx], 0x01              | 66 d1 24 0b                   |
    | sal word [rsp + 1 * rcx], 0x01              | 66 d1 24 0c                   |
    | sal word [rbp + 1 * rcx], 0x01              | 66 d1 64 0d 00                |
    | sal word [rsi + 1 * rcx], 0x01              | 66 d1 24 0e                   |
    | sal word [rdi + 1 * rcx], 0x01              | 66 d1 24 0f                   |
    | sal word [r8 + 1 * rcx], 0x01               | 66 41 d1 24 08                |
    | sal word [r9 + 1 * rcx], 0x01               | 66 41 d1 24 09                |
    | sal word [r10 + 1 * rcx], 0x01              | 66 41 d1 24 0a                |
    | sal word [r11 + 1 * rcx], 0x01              | 66 41 d1 24 0b                |
    | sal word [r12 + 1 * rcx], 0x01              | 66 41 d1 24 0c                |
    | sal word [r13 + 1 * rcx], 0x01              | 66 41 d1 64 0d 00             |
    | sal word [r14 + 1 * rcx], 0x01              | 66 41 d1 24 0e                |
    | sal word [r15 + 1 * rcx], 0x01              | 66 41 d1 24 0f                |
    | sal word [rax + 1 * rax], 0x01              | 66 d1 24 00                   |
    | sal word [rax + 1 * rdx], 0x01              | 66 d1 24 10                   |
    | sal word [rax + 1 * rbx], 0x01              | 66 d1 24 18                   |
    | sal word [rax + 1 * rbp], 0x01              | 66 d1 24 28                   |
    | sal word [rax + 1 * rsi], 0x01              | 66 d1 24 30                   |
    | sal word [rax + 1 * rdi], 0x01              | 66 d1 24 38                   |
    | sal word [rax + 1 * r8], 0x01               | 66 42 d1 24 00                |
    | sal word [rax + 1 * r9], 0x01               | 66 42 d1 24 08                |
    | sal word [rax + 1 * r10], 0x01              | 66 42 d1 24 10                |
    | sal word [rax + 1 * r11], 0x01              | 66 42 d1 24 18                |
    | sal word [rax + 1 * r12], 0x01              | 66 42 d1 24 20                |
    | sal word [rax + 1 * r13], 0x01              | 66 42 d1 24 28                |
    | sal word [rax + 1 * r14], 0x01              | 66 42 d1 24 30                |
    | sal word [rax + 1 * r15], 0x01              | 66 42 d1 24 38                |
    | sal word [rax + 2 * rcx], 0x01              | 66 d1 24 48                   |
    | sal word [rax + 4 * rcx], 0x01              | 66 d1 24 88                   |
    | sal word [rax + 8 * rcx], 0x01              | 66 d1 24 c8                   |
    | sal word [r8 + 1 * r9], 0x01                | 66 43 d1 24 08                |
    | sal word [r8 + 2 * r9], 0x01                | 66 43 d1 24 48                |
    | sal word [r8 + 4 * r9], 0x01                | 66 43 d1 24 88                |
    | sal word [r8 + 8 * r9], 0x01                | 66 43 d1 24 c8                |
    | sal word [1 * rcx], 0x01                    | 66 d1 24 0d 00 00 00 00       |
    | sal word [2 * rcx], 0x01                    | 66 d1 24 4d 00 00 00 00       |
    | sal word [4 * rcx], 0x01                    | 66 d1 24 8d 00 00 00 00       |
    | sal word [8 * rcx], 0x01                    | 66 d1 24 cd 00 00 00 00       |
    | sal word [1 * r9], 0x01                     | 66 42 d1 24 0d 00 00 00 00    |
    | sal word [2 * r9], 0x01                     | 66 42 d1 24 4d 00 00 00 00    |
    | sal word [4 * r9], 0x01                     | 66 42 d1 24 8d 00 00 00 00    |
    | sal word [8 * r9], 0x01                     | 66 42 d1 24 cd 00 00 00 00    |
    | sal word [r13 + 8 * r12], 0x01              | 66 43 d1 64 e5 00             |
    | sal word [rsp + 4 * r15], 0x01              | 66 42 d1 24 bc                |
    | sal word [rax + 1 * rcx + 0x00], 0x01       | 66 d1 64 08 00                |
    | sal word [rax + 1 * rcx - 0x00], 0x01       | 66 d1 64 08 00                |
    | sal word [rax + 1 * rcx + 0x01], 0x01       | 66 d1 64 08 01                |
    | sal word [rax + 1 * rcx - 0x01], 0x01       | 66 d1 64 08 ff                |
    | sal word [rax + 1 * rcx + 0x00000001], 0x01 | 66 d1 a4 08 01 00 00 00       |
    | sal word [rax + 1 * rcx - 0x00000001], 0x01 | 66 d1 a4 08 ff ff ff ff       |
    | sal word [rax + 1 * rcx + 0x7f], 0x01       | 66 d1 64 08 7f                |
    | sal word [rax + 1 * rcx - 0x7f], 0x01       | 66 d1 64 08 81                |
    | sal word [rax + 1 * rcx + 0x80], 0x01       | 66 d1 a4 08 80 00 00 00       |
    | sal word [rax + 1 * rcx - 0x80], 0x01       | 66 d1 64 08 80                |
    | sal word [rax + 1 * rcx - 0x81], 0x01       | 66 d1 a4 08 7f ff ff ff       |
    | sal word [rax + 1 * rcx + 0xff], 0x01       | 66 d1 a4 08 ff 00 00 00       |
    | sal word [rax + 1 * rcx - 0xff], 0x01       | 66 d1 a4 08 01 ff ff ff       |
    | sal word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 d1 a4 08 ff ff ff 7f       |
    | sal word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 d1 a4 08 01 00 00 80       |
    | sal word [rax + 1 * rcx - 0x80000000], 0x01 | 66 d1 a4 08 00 00 00 80       |
    | sal word [r10 + 0x7f], 0x01                 | 66 41 d1 62 7f                |
    | sal word [r10 + 0x80], 0x01                 | 66 41 d1 a2 80 00 00 00       |
    | sal word [r10 - 0x80], 0x01                 | 66 41 d1 62 80                |
    | sal word [r10 - 0x81], 0x01                 | 66 41 d1 a2 7f ff ff ff       |
    | sal word [rax], 0x00                        | 66 c1 20 00                   |
    | sal word [rax], 0x7f                        | 66 c1 20 7f                   |
    | sal word [rax], 0x80                        | 66 c1 20 80                   |
    | sal word [rax], 0xff                        | 66 c1 20 ff                   |
    | sal word [rcx], 0x7f                        | 66 c1 21 7f                   |
    | sal word [rdx], 0x80                        | 66 c1 22 80                   |
    | sal word [rbx], 0xff                        | 66 c1 23 ff                   |
    | sal word [rsp], 0x00                        | 66 c1 24 24 00                |
    | sal word [rsi], 0x7f                        | 66 c1 26 7f                   |
    | sal word [rdi], 0x80                        | 66 c1 27 80                   |
    | sal word [r8], 0xff                         | 66 41 c1 20 ff                |
    | sal word [r9], 0x00                         | 66 41 c1 21 00                |
    | sal word [r11], 0x7f                        | 66 41 c1 23 7f                |
    | sal word [r12], 0x80                        | 66 41 c1 24 24 80             |
    | sal word [r13], 0xff                        | 66 41 c1 65 00 ff             |
    | sal word [r14], 0x00                        | 66 41 c1 26 00                |
    | sal word [rax + 1 * rcx], 0x7f              | 66 c1 24 08 7f                |
    | sal word [rcx + 1 * rcx], 0x80              | 66 c1 24 09 80                |
    | sal word [rdx + 1 * rcx], 0xff              | 66 c1 24 0a ff                |
    | sal word [rbx + 1 * rcx], 0x00              | 66 c1 24 0b 00                |
    | sal word [rbp + 1 * rcx], 0x7f              | 66 c1 64 0d 00 7f             |
    | sal word [rsi + 1 * rcx], 0x80              | 66 c1 24 0e 80                |
    | sal word [rdi + 1 * rcx], 0xff              | 66 c1 24 0f ff                |
    | sal word [r8 + 1 * rcx], 0x00               | 66 41 c1 24 08 00             |
    | sal word [r10 + 1 * rcx], 0x7f              | 66 41 c1 24 0a 7f             |
    | sal word [r11 + 1 * rcx], 0x80              | 66 41 c1 24 0b 80             |
    | sal word [r12 + 1 * rcx], 0xff              | 66 41 c1 24 0c ff             |
    | sal word [r13 + 1 * rcx], 0x00              | 66 41 c1 64 0d 00 00          |
    | sal word [r15 + 1 * rcx], 0x7f              | 66 41 c1 24 0f 7f             |
    | sal word [rax + 1 * rax], 0x80              | 66 c1 24 00 80                |
    | sal word [rax + 1 * rdx], 0xff              | 66 c1 24 10 ff                |
    | sal word [rax + 1 * rbx], 0x00              | 66 c1 24 18 00                |
    | sal word [rax + 1 * rsi], 0x7f              | 66 c1 24 30 7f                |
    | sal word [rax + 1 * rdi], 0x80              | 66 c1 24 38 80                |
    | sal word [rax + 1 * r8], 0xff               | 66 42 c1 24 00 ff             |
    | sal word [rax + 1 * r9], 0x00               | 66 42 c1 24 08 00             |
    | sal word [rax + 1 * r11], 0x7f              | 66 42 c1 24 18 7f             |
    | sal word [rax + 1 * r12], 0x80              | 66 42 c1 24 20 80             |
    | sal word [rax + 1 * r13], 0xff              | 66 42 c1 24 28 ff             |
    | sal word [rax + 1 * r14], 0x00              | 66 42 c1 24 30 00             |
    | sal word [rax + 2 * rcx], 0x7f              | 66 c1 24 48 7f                |
    | sal word [rax + 4 * rcx], 0x80              | 66 c1 24 88 80                |
    | sal word [rax + 8 * rcx], 0xff              | 66 c1 24 c8 ff                |
    | sal word [r8 + 1 * r9], 0x00                | 66 43 c1 24 08 00             |
    | sal word [r8 + 4 * r9], 0x7f                | 66 43 c1 24 88 7f             |
    | sal word [r8 + 8 * r9], 0x80                | 66 43 c1 24 c8 80             |
    | sal word [1 * rcx], 0xff                    | 66 c1 24 0d 00 00 00 00 ff    |
    | sal word [2 * rcx], 0x00                    | 66 c1 24 4d 00 00 00 00 00    |
    | sal word [8 * rcx], 0x7f                    | 66 c1 24 cd 00 00 00 00 7f    |
    | sal word [1 * r9], 0x80                     | 66 42 c1 24 0d 00 00 00 00 80 |
    | sal word [2 * r9], 0xff                     | 66 42 c1 24 4d 00 00 00 00 ff |
    | sal word [4 * r9], 0x00                     | 66 42 c1 24 8d 00 00 00 00 00 |
    | sal word [r13 + 8 * r12], 0x7f              | 66 43 c1 64 e5 00 7f          |
    | sal word [rsp + 4 * r15], 0x80              | 66 42 c1 24 bc 80             |
    | sal word [rax + 1 * rcx + 0x00], 0xff       | 66 c1 64 08 00 ff             |
    | sal word [rax + 1 * rcx - 0x00], 0x00       | 66 c1 64 08 00 00             |
    | sal word [rax + 1 * rcx - 0x01], 0x7f       | 66 c1 64 08 ff 7f             |
    | sal word [rax + 1 * rcx + 0x00000001], 0x80 | 66 c1 a4 08 01 00 00 00 80    |
    | sal word [rax + 1 * rcx - 0x00000001], 0xff | 66 c1 a4 08 ff ff ff ff ff    |
    | sal word [rax + 1 * rcx + 0x7f], 0x00       | 66 c1 64 08 7f 00             |
    | sal word [rax + 1 * rcx + 0x80], 0x7f       | 66 c1 a4 08 80 00 00 00 7f    |
    | sal word [rax + 1 * rcx - 0x80], 0x80       | 66 c1 64 08 80 80             |
    | sal word [rax + 1 * rcx - 0x81], 0xff       | 66 c1 a4 08 7f ff ff ff ff    |
    | sal word [rax + 1 * rcx + 0xff], 0x00       | 66 c1 a4 08 ff 00 00 00 00    |
    | sal word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 c1 a4 08 ff ff ff 7f 7f    |
    | sal word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 c1 a4 08 01 00 00 80 80    |
    | sal word [rax + 1 * rcx - 0x80000000], 0xff | 66 c1 a4 08 00 00 00 80 ff    |
    | sal word [r10 + 0x7f], 0x00                 | 66 41 c1 62 7f 00             |
    | sal word [r10 - 0x80], 0x7f                 | 66 41 c1 62 80 7f             |
    | sal word [r10 - 0x81], 0x80                 | 66 41 c1 a2 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_sal_addr16_imm8():
    encode(SAL_ADDR16_IMM8)


SAL_ADDR16_CL = """
    | ----------------------------------------- | -------------------------- |
    | instruction                               | encoding                   |
    | ----------------------------------------- | -------------------------- |
    | sal word [rax], cl                        | 66 d3 20                   |
    | sal word [rcx], cl                        | 66 d3 21                   |
    | sal word [rdx], cl                        | 66 d3 22                   |
    | sal word [rbx], cl                        | 66 d3 23                   |
    | sal word [rsp], cl                        | 66 d3 24 24                |
    | sal word [rbp], cl                        | 66 d3 65 00                |
    | sal word [rsi], cl                        | 66 d3 26                   |
    | sal word [rdi], cl                        | 66 d3 27                   |
    | sal word [r8], cl                         | 66 41 d3 20                |
    | sal word [r9], cl                         | 66 41 d3 21                |
    | sal word [r10], cl                        | 66 41 d3 22                |
    | sal word [r11], cl                        | 66 41 d3 23                |
    | sal word [r12], cl                        | 66 41 d3 24 24             |
    | sal word [r13], cl                        | 66 41 d3 65 00             |
    | sal word [r14], cl                        | 66 41 d3 26                |
    | sal word [r15], cl                        | 66 41 d3 27                |
    | sal word [rax + 1 * rcx], cl              | 66 d3 24 08                |
    | sal word [rcx + 1 * rcx], cl              | 66 d3 24 09                |
    | sal word [rdx + 1 * rcx], cl              | 66 d3 24 0a                |
    | sal word [rbx + 1 * rcx], cl              | 66 d3 24 0b                |
    | sal word [rsp + 1 * rcx], cl              | 66 d3 24 0c                |
    | sal word [rbp + 1 * rcx], cl              | 66 d3 64 0d 00             |
    | sal word [rsi + 1 * rcx], cl              | 66 d3 24 0e                |
    | sal word [rdi + 1 * rcx], cl              | 66 d3 24 0f                |
    | sal word [r8 + 1 * rcx], cl               | 66 41 d3 24 08             |
    | sal word [r9 + 1 * rcx], cl               | 66 41 d3 24 09             |
    | sal word [r10 + 1 * rcx], cl              | 66 41 d3 24 0a             |
    | sal word [r11 + 1 * rcx], cl              | 66 41 d3 24 0b             |
    | sal word [r12 + 1 * rcx], cl              | 66 41 d3 24 0c             |
    | sal word [r13 + 1 * rcx], cl              | 66 41 d3 64 0d 00          |
    | sal word [r14 + 1 * rcx], cl              | 66 41 d3 24 0e             |
    | sal word [r15 + 1 * rcx], cl              | 66 41 d3 24 0f             |
    | sal word [rax + 1 * rax], cl              | 66 d3 24 00                |
    | sal word [rax + 1 * rdx], cl              | 66 d3 24 10                |
    | sal word [rax + 1 * rbx], cl              | 66 d3 24 18                |
    | sal word [rax + 1 * rbp], cl              | 66 d3 24 28                |
    | sal word [rax + 1 * rsi], cl              | 66 d3 24 30                |
    | sal word [rax + 1 * rdi], cl              | 66 d3 24 38                |
    | sal word [rax + 1 * r8], cl               | 66 42 d3 24 00             |
    | sal word [rax + 1 * r9], cl               | 66 42 d3 24 08             |
    | sal word [rax + 1 * r10], cl              | 66 42 d3 24 10             |
    | sal word [rax + 1 * r11], cl              | 66 42 d3 24 18             |
    | sal word [rax + 1 * r12], cl              | 66 42 d3 24 20             |
    | sal word [rax + 1 * r13], cl              | 66 42 d3 24 28             |
    | sal word [rax + 1 * r14], cl              | 66 42 d3 24 30             |
    | sal word [rax + 1 * r15], cl              | 66 42 d3 24 38             |
    | sal word [rax + 2 * rcx], cl              | 66 d3 24 48                |
    | sal word [rax + 4 * rcx], cl              | 66 d3 24 88                |
    | sal word [rax + 8 * rcx], cl              | 66 d3 24 c8                |
    | sal word [r8 + 1 * r9], cl                | 66 43 d3 24 08             |
    | sal word [r8 + 2 * r9], cl                | 66 43 d3 24 48             |
    | sal word [r8 + 4 * r9], cl                | 66 43 d3 24 88             |
    | sal word [r8 + 8 * r9], cl                | 66 43 d3 24 c8             |
    | sal word [1 * rcx], cl                    | 66 d3 24 0d 00 00 00 00    |
    | sal word [2 * rcx], cl                    | 66 d3 24 4d 00 00 00 00    |
    | sal word [4 * rcx], cl                    | 66 d3 24 8d 00 00 00 00    |
    | sal word [8 * rcx], cl                    | 66 d3 24 cd 00 00 00 00    |
    | sal word [1 * r9], cl                     | 66 42 d3 24 0d 00 00 00 00 |
    | sal word [2 * r9], cl                     | 66 42 d3 24 4d 00 00 00 00 |
    | sal word [4 * r9], cl                     | 66 42 d3 24 8d 00 00 00 00 |
    | sal word [8 * r9], cl                     | 66 42 d3 24 cd 00 00 00 00 |
    | sal word [r13 + 8 * r12], cl              | 66 43 d3 64 e5 00          |
    | sal word [rsp + 4 * r15], cl              | 66 42 d3 24 bc             |
    | sal word [rax + 1 * rcx + 0x00], cl       | 66 d3 64 08 00             |
    | sal word [rax + 1 * rcx - 0x00], cl       | 66 d3 64 08 00             |
    | sal word [rax + 1 * rcx + 0x01], cl       | 66 d3 64 08 01             |
    | sal word [rax + 1 * rcx - 0x01], cl       | 66 d3 64 08 ff             |
    | sal word [rax + 1 * rcx + 0x00000001], cl | 66 d3 a4 08 01 00 00 00    |
    | sal word [rax + 1 * rcx - 0x00000001], cl | 66 d3 a4 08 ff ff ff ff    |
    | sal word [rax + 1 * rcx + 0x7f], cl       | 66 d3 64 08 7f             |
    | sal word [rax + 1 * rcx - 0x7f], cl       | 66 d3 64 08 81             |
    | sal word [rax + 1 * rcx + 0x80], cl       | 66 d3 a4 08 80 00 00 00    |
    | sal word [rax + 1 * rcx - 0x80], cl       | 66 d3 64 08 80             |
    | sal word [rax + 1 * rcx - 0x81], cl       | 66 d3 a4 08 7f ff ff ff    |
    | sal word [rax + 1 * rcx + 0xff], cl       | 66 d3 a4 08 ff 00 00 00    |
    | sal word [rax + 1 * rcx - 0xff], cl       | 66 d3 a4 08 01 ff ff ff    |
    | sal word [rax + 1 * rcx + 0x7fffffff], cl | 66 d3 a4 08 ff ff ff 7f    |
    | sal word [rax + 1 * rcx - 0x7fffffff], cl | 66 d3 a4 08 01 00 00 80    |
    | sal word [rax + 1 * rcx - 0x80000000], cl | 66 d3 a4 08 00 00 00 80    |
    | sal word [r10 + 0x7f], cl                 | 66 41 d3 62 7f             |
    | sal word [r10 + 0x80], cl                 | 66 41 d3 a2 80 00 00 00    |
    | sal word [r10 - 0x80], cl                 | 66 41 d3 62 80             |
    | sal word [r10 - 0x81], cl                 | 66 41 d3 a2 7f ff ff ff    |
    | ----------------------------------------- | -------------------------- |
"""


def can_encode_sal_addr16_cl():
    encode(SAL_ADDR16_CL)


SAL_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sal byte [rax], 0x01                        | d0 20                      |
    | sal byte [rcx], 0x01                        | d0 21                      |
    | sal byte [rdx], 0x01                        | d0 22                      |
    | sal byte [rbx], 0x01                        | d0 23                      |
    | sal byte [rsp], 0x01                        | d0 24 24                   |
    | sal byte [rbp], 0x01                        | d0 65 00                   |
    | sal byte [rsi], 0x01                        | d0 26                      |
    | sal byte [rdi], 0x01                        | d0 27                      |
    | sal byte [r8], 0x01                         | 41 d0 20                   |
    | sal byte [r9], 0x01                         | 41 d0 21                   |
    | sal byte [r10], 0x01                        | 41 d0 22                   |
    | sal byte [r11], 0x01                        | 41 d0 23                   |
    | sal byte [r12], 0x01                        | 41 d0 24 24                |
    | sal byte [r13], 0x01                        | 41 d0 65 00                |
    | sal byte [r14], 0x01                        | 41 d0 26                   |
    | sal byte [r15], 0x01                        | 41 d0 27                   |
    | sal byte [rax + 1 * rcx], 0x01              | d0 24 08                   |
    | sal byte [rcx + 1 * rcx], 0x01              | d0 24 09                   |
    | sal byte [rdx + 1 * rcx], 0x01              | d0 24 0a                   |
    | sal byte [rbx + 1 * rcx], 0x01              | d0 24 0b                   |
    | sal byte [rsp + 1 * rcx], 0x01              | d0 24 0c                   |
    | sal byte [rbp + 1 * rcx], 0x01              | d0 64 0d 00                |
    | sal byte [rsi + 1 * rcx], 0x01              | d0 24 0e                   |
    | sal byte [rdi + 1 * rcx], 0x01              | d0 24 0f                   |
    | sal byte [r8 + 1 * rcx], 0x01               | 41 d0 24 08                |
    | sal byte [r9 + 1 * rcx], 0x01               | 41 d0 24 09                |
    | sal byte [r10 + 1 * rcx], 0x01              | 41 d0 24 0a                |
    | sal byte [r11 + 1 * rcx], 0x01              | 41 d0 24 0b                |
    | sal byte [r12 + 1 * rcx], 0x01              | 41 d0 24 0c                |
    | sal byte [r13 + 1 * rcx], 0x01              | 41 d0 64 0d 00             |
    | sal byte [r14 + 1 * rcx], 0x01              | 41 d0 24 0e                |
    | sal byte [r15 + 1 * rcx], 0x01              | 41 d0 24 0f                |
    | sal byte [rax + 1 * rax], 0x01              | d0 24 00                   |
    | sal byte [rax + 1 * rdx], 0x01              | d0 24 10                   |
    | sal byte [rax + 1 * rbx], 0x01              | d0 24 18                   |
    | sal byte [rax + 1 * rbp], 0x01              | d0 24 28                   |
    | sal byte [rax + 1 * rsi], 0x01              | d0 24 30                   |
    | sal byte [rax + 1 * rdi], 0x01              | d0 24 38                   |
    | sal byte [rax + 1 * r8], 0x01               | 42 d0 24 00                |
    | sal byte [rax + 1 * r9], 0x01               | 42 d0 24 08                |
    | sal byte [rax + 1 * r10], 0x01              | 42 d0 24 10                |
    | sal byte [rax + 1 * r11], 0x01              | 42 d0 24 18                |
    | sal byte [rax + 1 * r12], 0x01              | 42 d0 24 20                |
    | sal byte [rax + 1 * r13], 0x01              | 42 d0 24 28                |
    | sal byte [rax + 1 * r14], 0x01              | 42 d0 24 30                |
    | sal byte [rax + 1 * r15], 0x01              | 42 d0 24 38                |
    | sal byte [rax + 2 * rcx], 0x01              | d0 24 48                   |
    | sal byte [rax + 4 * rcx], 0x01              | d0 24 88                   |
    | sal byte [rax + 8 * rcx], 0x01              | d0 24 c8                   |
    | sal byte [r8 + 1 * r9], 0x01                | 43 d0 24 08                |
    | sal byte [r8 + 2 * r9], 0x01                | 43 d0 24 48                |
    | sal byte [r8 + 4 * r9], 0x01                | 43 d0 24 88                |
    | sal byte [r8 + 8 * r9], 0x01                | 43 d0 24 c8                |
    | sal byte [1 * rcx], 0x01                    | d0 24 0d 00 00 00 00       |
    | sal byte [2 * rcx], 0x01                    | d0 24 4d 00 00 00 00       |
    | sal byte [4 * rcx], 0x01                    | d0 24 8d 00 00 00 00       |
    | sal byte [8 * rcx], 0x01                    | d0 24 cd 00 00 00 00       |
    | sal byte [1 * r9], 0x01                     | 42 d0 24 0d 00 00 00 00    |
    | sal byte [2 * r9], 0x01                     | 42 d0 24 4d 00 00 00 00    |
    | sal byte [4 * r9], 0x01                     | 42 d0 24 8d 00 00 00 00    |
    | sal byte [8 * r9], 0x01                     | 42 d0 24 cd 00 00 00 00    |
    | sal byte [r13 + 8 * r12], 0x01              | 43 d0 64 e5 00             |
    | sal byte [rsp + 4 * r15], 0x01              | 42 d0 24 bc                |
    | sal byte [rax + 1 * rcx + 0x00], 0x01       | d0 64 08 00                |
    | sal byte [rax + 1 * rcx - 0x00], 0x01       | d0 64 08 00                |
    | sal byte [rax + 1 * rcx + 0x01], 0x01       | d0 64 08 01                |
    | sal byte [rax + 1 * rcx - 0x01], 0x01       | d0 64 08 ff                |
    | sal byte [rax + 1 * rcx + 0x00000001], 0x01 | d0 a4 08 01 00 00 00       |
    | sal byte [rax + 1 * rcx - 0x00000001], 0x01 | d0 a4 08 ff ff ff ff       |
    | sal byte [rax + 1 * rcx + 0x7f], 0x01       | d0 64 08 7f                |
    | sal byte [rax + 1 * rcx - 0x7f], 0x01       | d0 64 08 81                |
    | sal byte [rax + 1 * rcx + 0x80], 0x01       | d0 a4 08 80 00 00 00       |
    | sal byte [rax + 1 * rcx - 0x80], 0x01       | d0 64 08 80                |
    | sal byte [rax + 1 * rcx - 0x81], 0x01       | d0 a4 08 7f ff ff ff       |
    | sal byte [rax + 1 * rcx + 0xff], 0x01       | d0 a4 08 ff 00 00 00       |
    | sal byte [rax + 1 * rcx - 0xff], 0x01       | d0 a4 08 01 ff ff ff       |
    | sal byte [rax + 1 * rcx + 0x7fffffff], 0x01 | d0 a4 08 ff ff ff 7f       |
    | sal byte [rax + 1 * rcx - 0x7fffffff], 0x01 | d0 a4 08 01 00 00 80       |
    | sal byte [rax + 1 * rcx - 0x80000000], 0x01 | d0 a4 08 00 00 00 80       |
    | sal byte [r10 + 0x7f], 0x01                 | 41 d0 62 7f                |
    | sal byte [r10 + 0x80], 0x01                 | 41 d0 a2 80 00 00 00       |
    | sal byte [r10 - 0x80], 0x01                 | 41 d0 62 80                |
    | sal byte [r10 - 0x81], 0x01                 | 41 d0 a2 7f ff ff ff       |
    | sal byte [rax], 0x00                        | c0 20 00                   |
    | sal byte [rax], 0x7f                        | c0 20 7f                   |
    | sal byte [rax], 0x80                        | c0 20 80                   |
    | sal byte [rax], 0xff                        | c0 20 ff                   |
    | sal byte [rcx], 0x7f                        | c0 21 7f                   |
    | sal byte [rdx], 0x80                        | c0 22 80                   |
    | sal byte [rbx], 0xff                        | c0 23 ff                   |
    | sal byte [rsp], 0x00                        | c0 24 24 00                |
    | sal byte [rsi], 0x7f                        | c0 26 7f                   |
    | sal byte [rdi], 0x80                        | c0 27 80                   |
    | sal byte [r8], 0xff                         | 41 c0 20 ff                |
    | sal byte [r9], 0x00                         | 41 c0 21 00                |
    | sal byte [r11], 0x7f                        | 41 c0 23 7f                |
    | sal byte [r12], 0x80                        | 41 c0 24 24 80             |
    | sal byte [r13], 0xff                        | 41 c0 65 00 ff             |
    | sal byte [r14], 0x00                        | 41 c0 26 00                |
    | sal byte [rax + 1 * rcx], 0x7f              | c0 24 08 7f                |
    | sal byte [rcx + 1 * rcx], 0x80              | c0 24 09 80                |
    | sal byte [rdx + 1 * rcx], 0xff              | c0 24 0a ff                |
    | sal byte [rbx + 1 * rcx], 0x00              | c0 24 0b 00                |
    | sal byte [rbp + 1 * rcx], 0x7f              | c0 64 0d 00 7f             |
    | sal byte [rsi + 1 * rcx], 0x80              | c0 24 0e 80                |
    | sal byte [rdi + 1 * rcx], 0xff              | c0 24 0f ff                |
    | sal byte [r8 + 1 * rcx], 0x00               | 41 c0 24 08 00             |
    | sal byte [r10 + 1 * rcx], 0x7f              | 41 c0 24 0a 7f             |
    | sal byte [r11 + 1 * rcx], 0x80              | 41 c0 24 0b 80             |
    | sal byte [r12 + 1 * rcx], 0xff              | 41 c0 24 0c ff             |
    | sal byte [r13 + 1 * rcx], 0x00              | 41 c0 64 0d 00 00          |
    | sal byte [r15 + 1 * rcx], 0x7f              | 41 c0 24 0f 7f             |
    | sal byte [rax + 1 * rax], 0x80              | c0 24 00 80                |
    | sal byte [rax + 1 * rdx], 0xff              | c0 24 10 ff                |
    | sal byte [rax + 1 * rbx], 0x00              | c0 24 18 00                |
    | sal byte [rax + 1 * rsi], 0x7f              | c0 24 30 7f                |
    | sal byte [rax + 1 * rdi], 0x80              | c0 24 38 80                |
    | sal byte [rax + 1 * r8], 0xff               | 42 c0 24 00 ff             |
    | sal byte [rax + 1 * r9], 0x00               | 42 c0 24 08 00             |
    | sal byte [rax + 1 * r11], 0x7f              | 42 c0 24 18 7f             |
    | sal byte [rax + 1 * r12], 0x80              | 42 c0 24 20 80             |
    | sal byte [rax + 1 * r13], 0xff              | 42 c0 24 28 ff             |
    | sal byte [rax + 1 * r14], 0x00              | 42 c0 24 30 00             |
    | sal byte [rax + 2 * rcx], 0x7f              | c0 24 48 7f                |
    | sal byte [rax + 4 * rcx], 0x80              | c0 24 88 80                |
    | sal byte [rax + 8 * rcx], 0xff              | c0 24 c8 ff                |
    | sal byte [r8 + 1 * r9], 0x00                | 43 c0 24 08 00             |
    | sal byte [r8 + 4 * r9], 0x7f                | 43 c0 24 88 7f             |
    | sal byte [r8 + 8 * r9], 0x80                | 43 c0 24 c8 80             |
    | sal byte [1 * rcx], 0xff                    | c0 24 0d 00 00 00 00 ff    |
    | sal byte [2 * rcx], 0x00                    | c0 24 4d 00 00 00 00 00    |
    | sal byte [8 * rcx], 0x7f                    | c0 24 cd 00 00 00 00 7f    |
    | sal byte [1 * r9], 0x80                     | 42 c0 24 0d 00 00 00 00 80 |
    | sal byte [2 * r9], 0xff                     | 42 c0 24 4d 00 00 00 00 ff |
    | sal byte [4 * r9], 0x00                     | 42 c0 24 8d 00 00 00 00 00 |
    | sal byte [r13 + 8 * r12], 0x7f              | 43 c0 64 e5 00 7f          |
    | sal byte [rsp + 4 * r15], 0x80              | 42 c0 24 bc 80             |
    | sal byte [rax + 1 * rcx + 0x00], 0xff       | c0 64 08 00 ff             |
    | sal byte [rax + 1 * rcx - 0x00], 0x00       | c0 64 08 00 00             |
    | sal byte [rax + 1 * rcx - 0x01], 0x7f       | c0 64 08 ff 7f             |
    | sal byte [rax + 1 * rcx + 0x00000001], 0x80 | c0 a4 08 01 00 00 00 80    |
    | sal byte [rax + 1 * rcx - 0x00000001], 0xff | c0 a4 08 ff ff ff ff ff    |
    | sal byte [rax + 1 * rcx + 0x7f], 0x00       | c0 64 08 7f 00             |
    | sal byte [rax + 1 * rcx + 0x80], 0x7f       | c0 a4 08 80 00 00 00 7f    |
    | sal byte [rax + 1 * rcx - 0x80], 0x80       | c0 64 08 80 80             |
    | sal byte [rax + 1 * rcx - 0x81], 0xff       | c0 a4 08 7f ff ff ff ff    |
    | sal byte [rax + 1 * rcx + 0xff], 0x00       | c0 a4 08 ff 00 00 00 00    |
    | sal byte [rax + 1 * rcx + 0x7fffffff], 0x7f | c0 a4 08 ff ff ff 7f 7f    |
    | sal byte [rax + 1 * rcx - 0x7fffffff], 0x80 | c0 a4 08 01 00 00 80 80    |
    | sal byte [rax + 1 * rcx - 0x80000000], 0xff | c0 a4 08 00 00 00 80 ff    |
    | sal byte [r10 + 0x7f], 0x00                 | 41 c0 62 7f 00             |
    | sal byte [r10 - 0x80], 0x7f                 | 41 c0 62 80 7f             |
    | sal byte [r10 - 0x81], 0x80                 | 41 c0 a2 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sal_addr8_imm8():
    encode(SAL_ADDR8_IMM8)


SAL_ADDR8_CL = """
    | ----------------------------------------- | ----------------------- |
    | instruction                               | encoding                |
    | ----------------------------------------- | ----------------------- |
    | sal byte [rax], cl                        | d2 20                   |
    | sal byte [rcx], cl                        | d2 21                   |
    | sal byte [rdx], cl                        | d2 22                   |
    | sal byte [rbx], cl                        | d2 23                   |
    | sal byte [rsp], cl                        | d2 24 24                |
    | sal byte [rbp], cl                        | d2 65 00                |
    | sal byte [rsi], cl                        | d2 26                   |
    | sal byte [rdi], cl                        | d2 27                   |
    | sal byte [r8], cl                         | 41 d2 20                |
    | sal byte [r9], cl                         | 41 d2 21                |
    | sal byte [r10], cl                        | 41 d2 22                |
    | sal byte [r11], cl                        | 41 d2 23                |
    | sal byte [r12], cl                        | 41 d2 24 24             |
    | sal byte [r13], cl                        | 41 d2 65 00             |
    | sal byte [r14], cl                        | 41 d2 26                |
    | sal byte [r15], cl                        | 41 d2 27                |
    | sal byte [rax + 1 * rcx], cl              | d2 24 08                |
    | sal byte [rcx + 1 * rcx], cl              | d2 24 09                |
    | sal byte [rdx + 1 * rcx], cl              | d2 24 0a                |
    | sal byte [rbx + 1 * rcx], cl              | d2 24 0b                |
    | sal byte [rsp + 1 * rcx], cl              | d2 24 0c                |
    | sal byte [rbp + 1 * rcx], cl              | d2 64 0d 00             |
    | sal byte [rsi + 1 * rcx], cl              | d2 24 0e                |
    | sal byte [rdi + 1 * rcx], cl              | d2 24 0f                |
    | sal byte [r8 + 1 * rcx], cl               | 41 d2 24 08             |
    | sal byte [r9 + 1 * rcx], cl               | 41 d2 24 09             |
    | sal byte [r10 + 1 * rcx], cl              | 41 d2 24 0a             |
    | sal byte [r11 + 1 * rcx], cl              | 41 d2 24 0b             |
    | sal byte [r12 + 1 * rcx], cl              | 41 d2 24 0c             |
    | sal byte [r13 + 1 * rcx], cl              | 41 d2 64 0d 00          |
    | sal byte [r14 + 1 * rcx], cl              | 41 d2 24 0e             |
    | sal byte [r15 + 1 * rcx], cl              | 41 d2 24 0f             |
    | sal byte [rax + 1 * rax], cl              | d2 24 00                |
    | sal byte [rax + 1 * rdx], cl              | d2 24 10                |
    | sal byte [rax + 1 * rbx], cl              | d2 24 18                |
    | sal byte [rax + 1 * rbp], cl              | d2 24 28                |
    | sal byte [rax + 1 * rsi], cl              | d2 24 30                |
    | sal byte [rax + 1 * rdi], cl              | d2 24 38                |
    | sal byte [rax + 1 * r8], cl               | 42 d2 24 00             |
    | sal byte [rax + 1 * r9], cl               | 42 d2 24 08             |
    | sal byte [rax + 1 * r10], cl              | 42 d2 24 10             |
    | sal byte [rax + 1 * r11], cl              | 42 d2 24 18             |
    | sal byte [rax + 1 * r12], cl              | 42 d2 24 20             |
    | sal byte [rax + 1 * r13], cl              | 42 d2 24 28             |
    | sal byte [rax + 1 * r14], cl              | 42 d2 24 30             |
    | sal byte [rax + 1 * r15], cl              | 42 d2 24 38             |
    | sal byte [rax + 2 * rcx], cl              | d2 24 48                |
    | sal byte [rax + 4 * rcx], cl              | d2 24 88                |
    | sal byte [rax + 8 * rcx], cl              | d2 24 c8                |
    | sal byte [r8 + 1 * r9], cl                | 43 d2 24 08             |
    | sal byte [r8 + 2 * r9], cl                | 43 d2 24 48             |
    | sal byte [r8 + 4 * r9], cl                | 43 d2 24 88             |
    | sal byte [r8 + 8 * r9], cl                | 43 d2 24 c8             |
    | sal byte [1 * rcx], cl                    | d2 24 0d 00 00 00 00    |
    | sal byte [2 * rcx], cl                    | d2 24 4d 00 00 00 00    |
    | sal byte [4 * rcx], cl                    | d2 24 8d 00 00 00 00    |
    | sal byte [8 * rcx], cl                    | d2 24 cd 00 00 00 00    |
    | sal byte [1 * r9], cl                     | 42 d2 24 0d 00 00 00 00 |
    | sal byte [2 * r9], cl                     | 42 d2 24 4d 00 00 00 00 |
    | sal byte [4 * r9], cl                     | 42 d2 24 8d 00 00 00 00 |
    | sal byte [8 * r9], cl                     | 42 d2 24 cd 00 00 00 00 |
    | sal byte [r13 + 8 * r12], cl              | 43 d2 64 e5 00          |
    | sal byte [rsp + 4 * r15], cl              | 42 d2 24 bc             |
    | sal byte [rax + 1 * rcx + 0x00], cl       | d2 64 08 00             |
    | sal byte [rax + 1 * rcx - 0x00], cl       | d2 64 08 00             |
    | sal byte [rax + 1 * rcx + 0x01], cl       | d2 64 08 01             |
    | sal byte [rax + 1 * rcx - 0x01], cl       | d2 64 08 ff             |
    | sal byte [rax + 1 * rcx + 0x00000001], cl | d2 a4 08 01 00 00 00    |
    | sal byte [rax + 1 * rcx - 0x00000001], cl | d2 a4 08 ff ff ff ff    |
    | sal byte [rax + 1 * rcx + 0x7f], cl       | d2 64 08 7f             |
    | sal byte [rax + 1 * rcx - 0x7f], cl       | d2 64 08 81             |
    | sal byte [rax + 1 * rcx + 0x80], cl       | d2 a4 08 80 00 00 00    |
    | sal byte [rax + 1 * rcx - 0x80], cl       | d2 64 08 80             |
    | sal byte [rax + 1 * rcx - 0x81], cl       | d2 a4 08 7f ff ff ff    |
    | sal byte [rax + 1 * rcx + 0xff], cl       | d2 a4 08 ff 00 00 00    |
    | sal byte [rax + 1 * rcx - 0xff], cl       | d2 a4 08 01 ff ff ff    |
    | sal byte [rax + 1 * rcx + 0x7fffffff], cl | d2 a4 08 ff ff ff 7f    |
    | sal byte [rax + 1 * rcx - 0x7fffffff], cl | d2 a4 08 01 00 00 80    |
    | sal byte [rax + 1 * rcx - 0x80000000], cl | d2 a4 08 00 00 00 80    |
    | sal byte [r10 + 0x7f], cl                 | 41 d2 62 7f             |
    | sal byte [r10 + 0x80], cl                 | 41 d2 a2 80 00 00 00    |
    | sal byte [r10 - 0x80], cl                 | 41 d2 62 80             |
    | sal byte [r10 - 0x81], cl                 | 41 d2 a2 7f ff ff ff    |
    | ----------------------------------------- | ----------------------- |
"""


def can_encode_sal_addr8_cl():
    encode(SAL_ADDR8_CL)
