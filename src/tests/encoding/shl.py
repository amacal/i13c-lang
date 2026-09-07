from tests.encoding.core import encode, exhaust


def can_exhaust_shl():
    exhaust(
        SHL_ADDR16_CL,
        SHL_ADDR16_IMM8,
        SHL_ADDR32_CL,
        SHL_ADDR32_IMM8,
        SHL_ADDR64_CL,
        SHL_ADDR64_IMM8,
        SHL_ADDR8_CL,
        SHL_ADDR8_IMM8,
        SHL_REG16_CL,
        SHL_REG16_IMM8,
        SHL_REG32_CL,
        SHL_REG32_IMM8,
        SHL_REG64_CL,
        SHL_REG64_IMM8,
        SHL_REG8_CL,
        SHL_REG8_IMM8,
    )


SHL_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | shl rax, 0x01 | 48 d1 e0    | *** | shl rax, 0x00 | 48 c1 e0 00 |
    | shl rcx, 0x01 | 48 d1 e1    | *** | shl rax, 0x7f | 48 c1 e0 7f |
    | shl rdx, 0x01 | 48 d1 e2    | *** | shl rax, 0x80 | 48 c1 e0 80 |
    | shl rbx, 0x01 | 48 d1 e3    | *** | shl rax, 0xff | 48 c1 e0 ff |
    | shl rsp, 0x01 | 48 d1 e4    | *** | shl rcx, 0x7f | 48 c1 e1 7f |
    | shl rbp, 0x01 | 48 d1 e5    | *** | shl rdx, 0x80 | 48 c1 e2 80 |
    | shl rsi, 0x01 | 48 d1 e6    | *** | shl rbx, 0xff | 48 c1 e3 ff |
    | shl rdi, 0x01 | 48 d1 e7    | *** | shl rsp, 0x00 | 48 c1 e4 00 |
    | shl r8, 0x01  | 49 d1 e0    | *** | shl rsi, 0x7f | 48 c1 e6 7f |
    | shl r9, 0x01  | 49 d1 e1    | *** | shl rdi, 0x80 | 48 c1 e7 80 |
    | shl r10, 0x01 | 49 d1 e2    | *** | shl r8, 0xff  | 49 c1 e0 ff |
    | shl r11, 0x01 | 49 d1 e3    | *** | shl r9, 0x00  | 49 c1 e1 00 |
    | shl r12, 0x01 | 49 d1 e4    | *** | shl r11, 0x7f | 49 c1 e3 7f |
    | shl r13, 0x01 | 49 d1 e5    | *** | shl r12, 0x80 | 49 c1 e4 80 |
    | shl r14, 0x01 | 49 d1 e6    | *** | shl r13, 0xff | 49 c1 e5 ff |
    | shl r15, 0x01 | 49 d1 e7    | *** | shl r14, 0x00 | 49 c1 e6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_shl_reg64_imm8():
    encode(SHL_REG64_IMM8)


SHL_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | shl rax, cl | 48 d3 e0 | *** | shl r8, cl  | 49 d3 e0 |
    | shl rcx, cl | 48 d3 e1 | *** | shl r9, cl  | 49 d3 e1 |
    | shl rdx, cl | 48 d3 e2 | *** | shl r10, cl | 49 d3 e2 |
    | shl rbx, cl | 48 d3 e3 | *** | shl r11, cl | 49 d3 e3 |
    | shl rsp, cl | 48 d3 e4 | *** | shl r12, cl | 49 d3 e4 |
    | shl rbp, cl | 48 d3 e5 | *** | shl r13, cl | 49 d3 e5 |
    | shl rsi, cl | 48 d3 e6 | *** | shl r14, cl | 49 d3 e6 |
    | shl rdi, cl | 48 d3 e7 | *** | shl r15, cl | 49 d3 e7 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_shl_reg64_cl():
    encode(SHL_REG64_CL)


SHL_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | shl eax, 0x01  | d1 e0       | *** | shl eax, 0x00  | c1 e0 00    |
    | shl ecx, 0x01  | d1 e1       | *** | shl eax, 0x7f  | c1 e0 7f    |
    | shl edx, 0x01  | d1 e2       | *** | shl eax, 0x80  | c1 e0 80    |
    | shl ebx, 0x01  | d1 e3       | *** | shl eax, 0xff  | c1 e0 ff    |
    | shl esp, 0x01  | d1 e4       | *** | shl ecx, 0x7f  | c1 e1 7f    |
    | shl ebp, 0x01  | d1 e5       | *** | shl edx, 0x80  | c1 e2 80    |
    | shl esi, 0x01  | d1 e6       | *** | shl ebx, 0xff  | c1 e3 ff    |
    | shl edi, 0x01  | d1 e7       | *** | shl esp, 0x00  | c1 e4 00    |
    | shl r8d, 0x01  | 41 d1 e0    | *** | shl esi, 0x7f  | c1 e6 7f    |
    | shl r9d, 0x01  | 41 d1 e1    | *** | shl edi, 0x80  | c1 e7 80    |
    | shl r10d, 0x01 | 41 d1 e2    | *** | shl r8d, 0xff  | 41 c1 e0 ff |
    | shl r11d, 0x01 | 41 d1 e3    | *** | shl r9d, 0x00  | 41 c1 e1 00 |
    | shl r12d, 0x01 | 41 d1 e4    | *** | shl r11d, 0x7f | 41 c1 e3 7f |
    | shl r13d, 0x01 | 41 d1 e5    | *** | shl r12d, 0x80 | 41 c1 e4 80 |
    | shl r14d, 0x01 | 41 d1 e6    | *** | shl r13d, 0xff | 41 c1 e5 ff |
    | shl r15d, 0x01 | 41 d1 e7    | *** | shl r14d, 0x00 | 41 c1 e6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_shl_reg32_imm8():
    encode(SHL_REG32_IMM8)


SHL_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | shl eax, cl  | d3 e0    | *** | shl r8d, cl  | 41 d3 e0 |
    | shl ecx, cl  | d3 e1    | *** | shl r9d, cl  | 41 d3 e1 |
    | shl edx, cl  | d3 e2    | *** | shl r10d, cl | 41 d3 e2 |
    | shl ebx, cl  | d3 e3    | *** | shl r11d, cl | 41 d3 e3 |
    | shl esp, cl  | d3 e4    | *** | shl r12d, cl | 41 d3 e4 |
    | shl ebp, cl  | d3 e5    | *** | shl r13d, cl | 41 d3 e5 |
    | shl esi, cl  | d3 e6    | *** | shl r14d, cl | 41 d3 e6 |
    | shl edi, cl  | d3 e7    | *** | shl r15d, cl | 41 d3 e7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_shl_reg32_cl():
    encode(SHL_REG32_CL)


SHL_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | shl ax, 0x01   | 66 d1 e0       | *** | shl ax, 0x00   | 66 c1 e0 00    |
    | shl cx, 0x01   | 66 d1 e1       | *** | shl ax, 0x7f   | 66 c1 e0 7f    |
    | shl dx, 0x01   | 66 d1 e2       | *** | shl ax, 0x80   | 66 c1 e0 80    |
    | shl bx, 0x01   | 66 d1 e3       | *** | shl ax, 0xff   | 66 c1 e0 ff    |
    | shl sp, 0x01   | 66 d1 e4       | *** | shl cx, 0x7f   | 66 c1 e1 7f    |
    | shl bp, 0x01   | 66 d1 e5       | *** | shl dx, 0x80   | 66 c1 e2 80    |
    | shl si, 0x01   | 66 d1 e6       | *** | shl bx, 0xff   | 66 c1 e3 ff    |
    | shl di, 0x01   | 66 d1 e7       | *** | shl sp, 0x00   | 66 c1 e4 00    |
    | shl r8w, 0x01  | 66 41 d1 e0    | *** | shl si, 0x7f   | 66 c1 e6 7f    |
    | shl r9w, 0x01  | 66 41 d1 e1    | *** | shl di, 0x80   | 66 c1 e7 80    |
    | shl r10w, 0x01 | 66 41 d1 e2    | *** | shl r8w, 0xff  | 66 41 c1 e0 ff |
    | shl r11w, 0x01 | 66 41 d1 e3    | *** | shl r9w, 0x00  | 66 41 c1 e1 00 |
    | shl r12w, 0x01 | 66 41 d1 e4    | *** | shl r11w, 0x7f | 66 41 c1 e3 7f |
    | shl r13w, 0x01 | 66 41 d1 e5    | *** | shl r12w, 0x80 | 66 41 c1 e4 80 |
    | shl r14w, 0x01 | 66 41 d1 e6    | *** | shl r13w, 0xff | 66 41 c1 e5 ff |
    | shl r15w, 0x01 | 66 41 d1 e7    | *** | shl r14w, 0x00 | 66 41 c1 e6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_shl_reg16_imm8():
    encode(SHL_REG16_IMM8)


SHL_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | shl ax, cl   | 66 d3 e0    | *** | shl r8w, cl  | 66 41 d3 e0 |
    | shl cx, cl   | 66 d3 e1    | *** | shl r9w, cl  | 66 41 d3 e1 |
    | shl dx, cl   | 66 d3 e2    | *** | shl r10w, cl | 66 41 d3 e2 |
    | shl bx, cl   | 66 d3 e3    | *** | shl r11w, cl | 66 41 d3 e3 |
    | shl sp, cl   | 66 d3 e4    | *** | shl r12w, cl | 66 41 d3 e4 |
    | shl bp, cl   | 66 d3 e5    | *** | shl r13w, cl | 66 41 d3 e5 |
    | shl si, cl   | 66 d3 e6    | *** | shl r14w, cl | 66 41 d3 e6 |
    | shl di, cl   | 66 d3 e7    | *** | shl r15w, cl | 66 41 d3 e7 |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_shl_reg16_cl():
    encode(SHL_REG16_CL)


SHL_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | shl al, 0x01   | d0 e0       | *** | shl al, 0x00   | c0 e0 00    |
    | shl cl, 0x01   | d0 e1       | *** | shl al, 0x7f   | c0 e0 7f    |
    | shl dl, 0x01   | d0 e2       | *** | shl al, 0x80   | c0 e0 80    |
    | shl bl, 0x01   | d0 e3       | *** | shl al, 0xff   | c0 e0 ff    |
    | shl spl, 0x01  | 40 d0 e4    | *** | shl cl, 0x7f   | c0 e1 7f    |
    | shl bpl, 0x01  | 40 d0 e5    | *** | shl dl, 0x80   | c0 e2 80    |
    | shl sil, 0x01  | 40 d0 e6    | *** | shl bl, 0xff   | c0 e3 ff    |
    | shl dil, 0x01  | 40 d0 e7    | *** | shl spl, 0x00  | 40 c0 e4 00 |
    | shl r8b, 0x01  | 41 d0 e0    | *** | shl sil, 0x7f  | 40 c0 e6 7f |
    | shl r9b, 0x01  | 41 d0 e1    | *** | shl dil, 0x80  | 40 c0 e7 80 |
    | shl r10b, 0x01 | 41 d0 e2    | *** | shl r8b, 0xff  | 41 c0 e0 ff |
    | shl r11b, 0x01 | 41 d0 e3    | *** | shl r9b, 0x00  | 41 c0 e1 00 |
    | shl r12b, 0x01 | 41 d0 e4    | *** | shl r11b, 0x7f | 41 c0 e3 7f |
    | shl r13b, 0x01 | 41 d0 e5    | *** | shl r12b, 0x80 | 41 c0 e4 80 |
    | shl r14b, 0x01 | 41 d0 e6    | *** | shl r13b, 0xff | 41 c0 e5 ff |
    | shl r15b, 0x01 | 41 d0 e7    | *** | shl r14b, 0x00 | 41 c0 e6 00 |
    | shl ah, 0x01   | d0 e4       | *** | shl ah, 0x7f   | c0 e4 7f    |
    | shl ch, 0x01   | d0 e5       | *** | shl ch, 0x80   | c0 e5 80    |
    | shl dh, 0x01   | d0 e6       | *** | shl dh, 0xff   | c0 e6 ff    |
    | shl bh, 0x01   | d0 e7       | *** | shl bh, 0x00   | c0 e7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_shl_reg8_imm8():
    encode(SHL_REG8_IMM8)


SHL_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | shl al, cl   | d2 e0    | *** | shl r10b, cl | 41 d2 e2 |
    | shl cl, cl   | d2 e1    | *** | shl r11b, cl | 41 d2 e3 |
    | shl dl, cl   | d2 e2    | *** | shl r12b, cl | 41 d2 e4 |
    | shl bl, cl   | d2 e3    | *** | shl r13b, cl | 41 d2 e5 |
    | shl spl, cl  | 40 d2 e4 | *** | shl r14b, cl | 41 d2 e6 |
    | shl bpl, cl  | 40 d2 e5 | *** | shl r15b, cl | 41 d2 e7 |
    | shl sil, cl  | 40 d2 e6 | *** | shl ah, cl   | d2 e4    |
    | shl dil, cl  | 40 d2 e7 | *** | shl ch, cl   | d2 e5    |
    | shl r8b, cl  | 41 d2 e0 | *** | shl dh, cl   | d2 e6    |
    | shl r9b, cl  | 41 d2 e1 | *** | shl bh, cl   | d2 e7    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_shl_reg8_cl():
    encode(SHL_REG8_CL)


SHL_ADDR64_IMM8 = """
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | instruction                                                        | encoding                                  |
    | ------------------------------------------------------------------ | ----------------------------------------- |
    | shl qword [rax], 0x01                                              | 48 d1 20                                  |
    | shl qword [rcx], 0x01                                              | 48 d1 21                                  |
    | shl qword [rdx], 0x01                                              | 48 d1 22                                  |
    | shl qword [rbx], 0x01                                              | 48 d1 23                                  |
    | shl qword [rsp], 0x01                                              | 48 d1 24 24                               |
    | shl qword [rbp], 0x01                                              | 48 d1 65 00                               |
    | shl qword [rsi], 0x01                                              | 48 d1 26                                  |
    | shl qword [rdi], 0x01                                              | 48 d1 27                                  |
    | shl qword [r8], 0x01                                               | 49 d1 20                                  |
    | shl qword [r9], 0x01                                               | 49 d1 21                                  |
    | shl qword [r10], 0x01                                              | 49 d1 22                                  |
    | shl qword [r11], 0x01                                              | 49 d1 23                                  |
    | shl qword [r12], 0x01                                              | 49 d1 24 24                               |
    | shl qword [r13], 0x01                                              | 49 d1 65 00                               |
    | shl qword [r14], 0x01                                              | 49 d1 26                                  |
    | shl qword [r15], 0x01                                              | 49 d1 27                                  |
    | shl qword [rax + 1 * rcx], 0x01                                    | 48 d1 24 08                               |
    | shl qword [rcx + 1 * rcx], 0x01                                    | 48 d1 24 09                               |
    | shl qword [rdx + 1 * rcx], 0x01                                    | 48 d1 24 0a                               |
    | shl qword [rbx + 1 * rcx], 0x01                                    | 48 d1 24 0b                               |
    | shl qword [rsp + 1 * rcx], 0x01                                    | 48 d1 24 0c                               |
    | shl qword [rbp + 1 * rcx], 0x01                                    | 48 d1 64 0d 00                            |
    | shl qword [rsi + 1 * rcx], 0x01                                    | 48 d1 24 0e                               |
    | shl qword [rdi + 1 * rcx], 0x01                                    | 48 d1 24 0f                               |
    | shl qword [r8 + 1 * rcx], 0x01                                     | 49 d1 24 08                               |
    | shl qword [r9 + 1 * rcx], 0x01                                     | 49 d1 24 09                               |
    | shl qword [r10 + 1 * rcx], 0x01                                    | 49 d1 24 0a                               |
    | shl qword [r11 + 1 * rcx], 0x01                                    | 49 d1 24 0b                               |
    | shl qword [r12 + 1 * rcx], 0x01                                    | 49 d1 24 0c                               |
    | shl qword [r13 + 1 * rcx], 0x01                                    | 49 d1 64 0d 00                            |
    | shl qword [r14 + 1 * rcx], 0x01                                    | 49 d1 24 0e                               |
    | shl qword [r15 + 1 * rcx], 0x01                                    | 49 d1 24 0f                               |
    | shl qword [rax + 1 * rax], 0x01                                    | 48 d1 24 00                               |
    | shl qword [rax + 1 * rdx], 0x01                                    | 48 d1 24 10                               |
    | shl qword [rax + 1 * rbx], 0x01                                    | 48 d1 24 18                               |
    | shl qword [rax + 1 * rbp], 0x01                                    | 48 d1 24 28                               |
    | shl qword [rax + 1 * rsi], 0x01                                    | 48 d1 24 30                               |
    | shl qword [rax + 1 * rdi], 0x01                                    | 48 d1 24 38                               |
    | shl qword [rax + 1 * r8], 0x01                                     | 4a d1 24 00                               |
    | shl qword [rax + 1 * r9], 0x01                                     | 4a d1 24 08                               |
    | shl qword [rax + 1 * r10], 0x01                                    | 4a d1 24 10                               |
    | shl qword [rax + 1 * r11], 0x01                                    | 4a d1 24 18                               |
    | shl qword [rax + 1 * r12], 0x01                                    | 4a d1 24 20                               |
    | shl qword [rax + 1 * r13], 0x01                                    | 4a d1 24 28                               |
    | shl qword [rax + 1 * r14], 0x01                                    | 4a d1 24 30                               |
    | shl qword [rax + 1 * r15], 0x01                                    | 4a d1 24 38                               |
    | shl qword [rax + 2 * rcx], 0x01                                    | 48 d1 24 48                               |
    | shl qword [rax + 4 * rcx], 0x01                                    | 48 d1 24 88                               |
    | shl qword [rax + 8 * rcx], 0x01                                    | 48 d1 24 c8                               |
    | shl qword [r8 + 1 * r9], 0x01                                      | 4b d1 24 08                               |
    | shl qword [r8 + 2 * r9], 0x01                                      | 4b d1 24 48                               |
    | shl qword [r8 + 4 * r9], 0x01                                      | 4b d1 24 88                               |
    | shl qword [r8 + 8 * r9], 0x01                                      | 4b d1 24 c8                               |
    | shl qword [1 * rcx], 0x01                                          | 48 d1 24 0d 00 00 00 00                   |
    | shl qword [2 * rcx], 0x01                                          | 48 d1 24 4d 00 00 00 00                   |
    | shl qword [4 * rcx], 0x01                                          | 48 d1 24 8d 00 00 00 00                   |
    | shl qword [8 * rcx], 0x01                                          | 48 d1 24 cd 00 00 00 00                   |
    | shl qword [1 * r9], 0x01                                           | 4a d1 24 0d 00 00 00 00                   |
    | shl qword [2 * r9], 0x01                                           | 4a d1 24 4d 00 00 00 00                   |
    | shl qword [4 * r9], 0x01                                           | 4a d1 24 8d 00 00 00 00                   |
    | shl qword [8 * r9], 0x01                                           | 4a d1 24 cd 00 00 00 00                   |
    | shl qword [r13 + 8 * r12], 0x01                                    | 4b d1 64 e5 00                            |
    | shl qword [rsp + 4 * r15], 0x01                                    | 4a d1 24 bc                               |
    | shl qword [rax + 1 * rcx + 0x00], 0x01                             | 48 d1 64 08 00                            |
    | shl qword [rax + 1 * rcx - 0x00], 0x01                             | 48 d1 64 08 00                            |
    | shl qword [rax + 1 * rcx + 0x01], 0x01                             | 48 d1 64 08 01                            |
    | shl qword [rax + 1 * rcx - 0x01], 0x01                             | 48 d1 64 08 ff                            |
    | shl qword [rax + 1 * rcx + 0x00000001], 0x01                       | 48 d1 a4 08 01 00 00 00                   |
    | shl qword [rax + 1 * rcx - 0x00000001], 0x01                       | 48 d1 a4 08 ff ff ff ff                   |
    | shl qword [rax + 1 * rcx + 0x7f], 0x01                             | 48 d1 64 08 7f                            |
    | shl qword [rax + 1 * rcx - 0x7f], 0x01                             | 48 d1 64 08 81                            |
    | shl qword [rax + 1 * rcx + 0x80], 0x01                             | 48 d1 a4 08 80 00 00 00                   |
    | shl qword [rax + 1 * rcx - 0x80], 0x01                             | 48 d1 64 08 80                            |
    | shl qword [rax + 1 * rcx - 0x81], 0x01                             | 48 d1 a4 08 7f ff ff ff                   |
    | shl qword [rax + 1 * rcx + 0xff], 0x01                             | 48 d1 a4 08 ff 00 00 00                   |
    | shl qword [rax + 1 * rcx - 0xff], 0x01                             | 48 d1 a4 08 01 ff ff ff                   |
    | shl qword [rax + 1 * rcx + 0x7fffffff], 0x01                       | 48 d1 a4 08 ff ff ff 7f                   |
    | shl qword [rax + 1 * rcx - 0x7fffffff], 0x01                       | 48 d1 a4 08 01 00 00 80                   |
    | shl qword [rax + 1 * rcx - 0x80000000], 0x01                       | 48 d1 a4 08 00 00 00 80                   |
    | shl qword [r10 + 0x7f], 0x01                                       | 49 d1 62 7f                               |
    | shl qword [r10 + 0x80], 0x01                                       | 49 d1 a2 80 00 00 00                      |
    | shl qword [r10 - 0x80], 0x01                                       | 49 d1 62 80                               |
    | shl qword [r10 - 0x81], 0x01                                       | 49 d1 a2 7f ff ff ff                      |
    | .prev5: nop; nop; nop; nop; nop; shl qword [rel @prev5], 0x01      | 90 90 90 90 90 48 d1 25 f4 ff ff ff       |
    | .prev1: nop; shl qword [rel @prev1], 0x01                          | 90 48 d1 25 f8 ff ff ff                   |
    | shl qword [rel @next1], 0x01; nop; .next1: nop                     | 48 d1 25 01 00 00 00 90 90                |
    | shl qword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 48 d1 25 05 00 00 00 90 90 90 90 90 90    |
    | shl qword [rax], 0x00                                              | 48 c1 20 00                               |
    | shl qword [rax], 0x7f                                              | 48 c1 20 7f                               |
    | shl qword [rax], 0x80                                              | 48 c1 20 80                               |
    | shl qword [rax], 0xff                                              | 48 c1 20 ff                               |
    | shl qword [rcx], 0x7f                                              | 48 c1 21 7f                               |
    | shl qword [rdx], 0x80                                              | 48 c1 22 80                               |
    | shl qword [rbx], 0xff                                              | 48 c1 23 ff                               |
    | shl qword [rsp], 0x00                                              | 48 c1 24 24 00                            |
    | shl qword [rsi], 0x7f                                              | 48 c1 26 7f                               |
    | shl qword [rdi], 0x80                                              | 48 c1 27 80                               |
    | shl qword [r8], 0xff                                               | 49 c1 20 ff                               |
    | shl qword [r9], 0x00                                               | 49 c1 21 00                               |
    | shl qword [r11], 0x7f                                              | 49 c1 23 7f                               |
    | shl qword [r12], 0x80                                              | 49 c1 24 24 80                            |
    | shl qword [r13], 0xff                                              | 49 c1 65 00 ff                            |
    | shl qword [r14], 0x00                                              | 49 c1 26 00                               |
    | shl qword [rax + 1 * rcx], 0x7f                                    | 48 c1 24 08 7f                            |
    | shl qword [rcx + 1 * rcx], 0x80                                    | 48 c1 24 09 80                            |
    | shl qword [rdx + 1 * rcx], 0xff                                    | 48 c1 24 0a ff                            |
    | shl qword [rbx + 1 * rcx], 0x00                                    | 48 c1 24 0b 00                            |
    | shl qword [rbp + 1 * rcx], 0x7f                                    | 48 c1 64 0d 00 7f                         |
    | shl qword [rsi + 1 * rcx], 0x80                                    | 48 c1 24 0e 80                            |
    | shl qword [rdi + 1 * rcx], 0xff                                    | 48 c1 24 0f ff                            |
    | shl qword [r8 + 1 * rcx], 0x00                                     | 49 c1 24 08 00                            |
    | shl qword [r10 + 1 * rcx], 0x7f                                    | 49 c1 24 0a 7f                            |
    | shl qword [r11 + 1 * rcx], 0x80                                    | 49 c1 24 0b 80                            |
    | shl qword [r12 + 1 * rcx], 0xff                                    | 49 c1 24 0c ff                            |
    | shl qword [r13 + 1 * rcx], 0x00                                    | 49 c1 64 0d 00 00                         |
    | shl qword [r15 + 1 * rcx], 0x7f                                    | 49 c1 24 0f 7f                            |
    | shl qword [rax + 1 * rax], 0x80                                    | 48 c1 24 00 80                            |
    | shl qword [rax + 1 * rdx], 0xff                                    | 48 c1 24 10 ff                            |
    | shl qword [rax + 1 * rbx], 0x00                                    | 48 c1 24 18 00                            |
    | shl qword [rax + 1 * rsi], 0x7f                                    | 48 c1 24 30 7f                            |
    | shl qword [rax + 1 * rdi], 0x80                                    | 48 c1 24 38 80                            |
    | shl qword [rax + 1 * r8], 0xff                                     | 4a c1 24 00 ff                            |
    | shl qword [rax + 1 * r9], 0x00                                     | 4a c1 24 08 00                            |
    | shl qword [rax + 1 * r11], 0x7f                                    | 4a c1 24 18 7f                            |
    | shl qword [rax + 1 * r12], 0x80                                    | 4a c1 24 20 80                            |
    | shl qword [rax + 1 * r13], 0xff                                    | 4a c1 24 28 ff                            |
    | shl qword [rax + 1 * r14], 0x00                                    | 4a c1 24 30 00                            |
    | shl qword [rax + 2 * rcx], 0x7f                                    | 48 c1 24 48 7f                            |
    | shl qword [rax + 4 * rcx], 0x80                                    | 48 c1 24 88 80                            |
    | shl qword [rax + 8 * rcx], 0xff                                    | 48 c1 24 c8 ff                            |
    | shl qword [r8 + 1 * r9], 0x00                                      | 4b c1 24 08 00                            |
    | shl qword [r8 + 4 * r9], 0x7f                                      | 4b c1 24 88 7f                            |
    | shl qword [r8 + 8 * r9], 0x80                                      | 4b c1 24 c8 80                            |
    | shl qword [1 * rcx], 0xff                                          | 48 c1 24 0d 00 00 00 00 ff                |
    | shl qword [2 * rcx], 0x00                                          | 48 c1 24 4d 00 00 00 00 00                |
    | shl qword [8 * rcx], 0x7f                                          | 48 c1 24 cd 00 00 00 00 7f                |
    | shl qword [1 * r9], 0x80                                           | 4a c1 24 0d 00 00 00 00 80                |
    | shl qword [2 * r9], 0xff                                           | 4a c1 24 4d 00 00 00 00 ff                |
    | shl qword [4 * r9], 0x00                                           | 4a c1 24 8d 00 00 00 00 00                |
    | shl qword [r13 + 8 * r12], 0x7f                                    | 4b c1 64 e5 00 7f                         |
    | shl qword [rsp + 4 * r15], 0x80                                    | 4a c1 24 bc 80                            |
    | shl qword [rax + 1 * rcx + 0x00], 0xff                             | 48 c1 64 08 00 ff                         |
    | shl qword [rax + 1 * rcx - 0x00], 0x00                             | 48 c1 64 08 00 00                         |
    | shl qword [rax + 1 * rcx - 0x01], 0x7f                             | 48 c1 64 08 ff 7f                         |
    | shl qword [rax + 1 * rcx + 0x00000001], 0x80                       | 48 c1 a4 08 01 00 00 00 80                |
    | shl qword [rax + 1 * rcx - 0x00000001], 0xff                       | 48 c1 a4 08 ff ff ff ff ff                |
    | shl qword [rax + 1 * rcx + 0x7f], 0x00                             | 48 c1 64 08 7f 00                         |
    | shl qword [rax + 1 * rcx + 0x80], 0x7f                             | 48 c1 a4 08 80 00 00 00 7f                |
    | shl qword [rax + 1 * rcx - 0x80], 0x80                             | 48 c1 64 08 80 80                         |
    | shl qword [rax + 1 * rcx - 0x81], 0xff                             | 48 c1 a4 08 7f ff ff ff ff                |
    | shl qword [rax + 1 * rcx + 0xff], 0x00                             | 48 c1 a4 08 ff 00 00 00 00                |
    | shl qword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 48 c1 a4 08 ff ff ff 7f 7f                |
    | shl qword [rax + 1 * rcx - 0x7fffffff], 0x80                       | 48 c1 a4 08 01 00 00 80 80                |
    | shl qword [rax + 1 * rcx - 0x80000000], 0xff                       | 48 c1 a4 08 00 00 00 80 ff                |
    | shl qword [r10 + 0x7f], 0x00                                       | 49 c1 62 7f 00                            |
    | shl qword [r10 - 0x80], 0x7f                                       | 49 c1 62 80 7f                            |
    | shl qword [r10 - 0x81], 0x80                                       | 49 c1 a2 7f ff ff ff 80                   |
    | .prev5: nop; nop; nop; nop; nop; shl qword [rel @prev5], 0xff      | 90 90 90 90 90 48 c1 25 f3 ff ff ff ff    |
    | .prev1: nop; shl qword [rel @prev1], 0x00                          | 90 48 c1 25 f7 ff ff ff 00                |
    | shl qword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 48 c1 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | ----------------------------------------- |
"""


def can_encode_shl_addr64_imm8():
    encode(SHL_ADDR64_IMM8)


SHL_ADDR64_CL = """
    | ---------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                      | encoding                               |
    | ---------------------------------------------------------------- | -------------------------------------- |
    | shl qword [rax], cl                                              | 48 d3 20                               |
    | shl qword [rcx], cl                                              | 48 d3 21                               |
    | shl qword [rdx], cl                                              | 48 d3 22                               |
    | shl qword [rbx], cl                                              | 48 d3 23                               |
    | shl qword [rsp], cl                                              | 48 d3 24 24                            |
    | shl qword [rbp], cl                                              | 48 d3 65 00                            |
    | shl qword [rsi], cl                                              | 48 d3 26                               |
    | shl qword [rdi], cl                                              | 48 d3 27                               |
    | shl qword [r8], cl                                               | 49 d3 20                               |
    | shl qword [r9], cl                                               | 49 d3 21                               |
    | shl qword [r10], cl                                              | 49 d3 22                               |
    | shl qword [r11], cl                                              | 49 d3 23                               |
    | shl qword [r12], cl                                              | 49 d3 24 24                            |
    | shl qword [r13], cl                                              | 49 d3 65 00                            |
    | shl qword [r14], cl                                              | 49 d3 26                               |
    | shl qword [r15], cl                                              | 49 d3 27                               |
    | shl qword [rax + 1 * rcx], cl                                    | 48 d3 24 08                            |
    | shl qword [rcx + 1 * rcx], cl                                    | 48 d3 24 09                            |
    | shl qword [rdx + 1 * rcx], cl                                    | 48 d3 24 0a                            |
    | shl qword [rbx + 1 * rcx], cl                                    | 48 d3 24 0b                            |
    | shl qword [rsp + 1 * rcx], cl                                    | 48 d3 24 0c                            |
    | shl qword [rbp + 1 * rcx], cl                                    | 48 d3 64 0d 00                         |
    | shl qword [rsi + 1 * rcx], cl                                    | 48 d3 24 0e                            |
    | shl qword [rdi + 1 * rcx], cl                                    | 48 d3 24 0f                            |
    | shl qword [r8 + 1 * rcx], cl                                     | 49 d3 24 08                            |
    | shl qword [r9 + 1 * rcx], cl                                     | 49 d3 24 09                            |
    | shl qword [r10 + 1 * rcx], cl                                    | 49 d3 24 0a                            |
    | shl qword [r11 + 1 * rcx], cl                                    | 49 d3 24 0b                            |
    | shl qword [r12 + 1 * rcx], cl                                    | 49 d3 24 0c                            |
    | shl qword [r13 + 1 * rcx], cl                                    | 49 d3 64 0d 00                         |
    | shl qword [r14 + 1 * rcx], cl                                    | 49 d3 24 0e                            |
    | shl qword [r15 + 1 * rcx], cl                                    | 49 d3 24 0f                            |
    | shl qword [rax + 1 * rax], cl                                    | 48 d3 24 00                            |
    | shl qword [rax + 1 * rdx], cl                                    | 48 d3 24 10                            |
    | shl qword [rax + 1 * rbx], cl                                    | 48 d3 24 18                            |
    | shl qword [rax + 1 * rbp], cl                                    | 48 d3 24 28                            |
    | shl qword [rax + 1 * rsi], cl                                    | 48 d3 24 30                            |
    | shl qword [rax + 1 * rdi], cl                                    | 48 d3 24 38                            |
    | shl qword [rax + 1 * r8], cl                                     | 4a d3 24 00                            |
    | shl qword [rax + 1 * r9], cl                                     | 4a d3 24 08                            |
    | shl qword [rax + 1 * r10], cl                                    | 4a d3 24 10                            |
    | shl qword [rax + 1 * r11], cl                                    | 4a d3 24 18                            |
    | shl qword [rax + 1 * r12], cl                                    | 4a d3 24 20                            |
    | shl qword [rax + 1 * r13], cl                                    | 4a d3 24 28                            |
    | shl qword [rax + 1 * r14], cl                                    | 4a d3 24 30                            |
    | shl qword [rax + 1 * r15], cl                                    | 4a d3 24 38                            |
    | shl qword [rax + 2 * rcx], cl                                    | 48 d3 24 48                            |
    | shl qword [rax + 4 * rcx], cl                                    | 48 d3 24 88                            |
    | shl qword [rax + 8 * rcx], cl                                    | 48 d3 24 c8                            |
    | shl qword [r8 + 1 * r9], cl                                      | 4b d3 24 08                            |
    | shl qword [r8 + 2 * r9], cl                                      | 4b d3 24 48                            |
    | shl qword [r8 + 4 * r9], cl                                      | 4b d3 24 88                            |
    | shl qword [r8 + 8 * r9], cl                                      | 4b d3 24 c8                            |
    | shl qword [1 * rcx], cl                                          | 48 d3 24 0d 00 00 00 00                |
    | shl qword [2 * rcx], cl                                          | 48 d3 24 4d 00 00 00 00                |
    | shl qword [4 * rcx], cl                                          | 48 d3 24 8d 00 00 00 00                |
    | shl qword [8 * rcx], cl                                          | 48 d3 24 cd 00 00 00 00                |
    | shl qword [1 * r9], cl                                           | 4a d3 24 0d 00 00 00 00                |
    | shl qword [2 * r9], cl                                           | 4a d3 24 4d 00 00 00 00                |
    | shl qword [4 * r9], cl                                           | 4a d3 24 8d 00 00 00 00                |
    | shl qword [8 * r9], cl                                           | 4a d3 24 cd 00 00 00 00                |
    | shl qword [r13 + 8 * r12], cl                                    | 4b d3 64 e5 00                         |
    | shl qword [rsp + 4 * r15], cl                                    | 4a d3 24 bc                            |
    | shl qword [rax + 1 * rcx + 0x00], cl                             | 48 d3 64 08 00                         |
    | shl qword [rax + 1 * rcx - 0x00], cl                             | 48 d3 64 08 00                         |
    | shl qword [rax + 1 * rcx + 0x01], cl                             | 48 d3 64 08 01                         |
    | shl qword [rax + 1 * rcx - 0x01], cl                             | 48 d3 64 08 ff                         |
    | shl qword [rax + 1 * rcx + 0x00000001], cl                       | 48 d3 a4 08 01 00 00 00                |
    | shl qword [rax + 1 * rcx - 0x00000001], cl                       | 48 d3 a4 08 ff ff ff ff                |
    | shl qword [rax + 1 * rcx + 0x7f], cl                             | 48 d3 64 08 7f                         |
    | shl qword [rax + 1 * rcx - 0x7f], cl                             | 48 d3 64 08 81                         |
    | shl qword [rax + 1 * rcx + 0x80], cl                             | 48 d3 a4 08 80 00 00 00                |
    | shl qword [rax + 1 * rcx - 0x80], cl                             | 48 d3 64 08 80                         |
    | shl qword [rax + 1 * rcx - 0x81], cl                             | 48 d3 a4 08 7f ff ff ff                |
    | shl qword [rax + 1 * rcx + 0xff], cl                             | 48 d3 a4 08 ff 00 00 00                |
    | shl qword [rax + 1 * rcx - 0xff], cl                             | 48 d3 a4 08 01 ff ff ff                |
    | shl qword [rax + 1 * rcx + 0x7fffffff], cl                       | 48 d3 a4 08 ff ff ff 7f                |
    | shl qword [rax + 1 * rcx - 0x7fffffff], cl                       | 48 d3 a4 08 01 00 00 80                |
    | shl qword [rax + 1 * rcx - 0x80000000], cl                       | 48 d3 a4 08 00 00 00 80                |
    | shl qword [r10 + 0x7f], cl                                       | 49 d3 62 7f                            |
    | shl qword [r10 + 0x80], cl                                       | 49 d3 a2 80 00 00 00                   |
    | shl qword [r10 - 0x80], cl                                       | 49 d3 62 80                            |
    | shl qword [r10 - 0x81], cl                                       | 49 d3 a2 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; shl qword [rel @prev5], cl      | 90 90 90 90 90 48 d3 25 f4 ff ff ff    |
    | .prev1: nop; shl qword [rel @prev1], cl                          | 90 48 d3 25 f8 ff ff ff                |
    | shl qword [rel @next1], cl; nop; .next1: nop                     | 48 d3 25 01 00 00 00 90 90             |
    | shl qword [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | 48 d3 25 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_shl_addr64_cl():
    encode(SHL_ADDR64_CL)


SHL_ADDR32_IMM8 = """
    | ------------------------------------------------------------------ | -------------------------------------- |
    | instruction                                                        | encoding                               |
    | ------------------------------------------------------------------ | -------------------------------------- |
    | shl dword [rax], 0x01                                              | d1 20                                  |
    | shl dword [rcx], 0x01                                              | d1 21                                  |
    | shl dword [rdx], 0x01                                              | d1 22                                  |
    | shl dword [rbx], 0x01                                              | d1 23                                  |
    | shl dword [rsp], 0x01                                              | d1 24 24                               |
    | shl dword [rbp], 0x01                                              | d1 65 00                               |
    | shl dword [rsi], 0x01                                              | d1 26                                  |
    | shl dword [rdi], 0x01                                              | d1 27                                  |
    | shl dword [r8], 0x01                                               | 41 d1 20                               |
    | shl dword [r9], 0x01                                               | 41 d1 21                               |
    | shl dword [r10], 0x01                                              | 41 d1 22                               |
    | shl dword [r11], 0x01                                              | 41 d1 23                               |
    | shl dword [r12], 0x01                                              | 41 d1 24 24                            |
    | shl dword [r13], 0x01                                              | 41 d1 65 00                            |
    | shl dword [r14], 0x01                                              | 41 d1 26                               |
    | shl dword [r15], 0x01                                              | 41 d1 27                               |
    | shl dword [rax + 1 * rcx], 0x01                                    | d1 24 08                               |
    | shl dword [rcx + 1 * rcx], 0x01                                    | d1 24 09                               |
    | shl dword [rdx + 1 * rcx], 0x01                                    | d1 24 0a                               |
    | shl dword [rbx + 1 * rcx], 0x01                                    | d1 24 0b                               |
    | shl dword [rsp + 1 * rcx], 0x01                                    | d1 24 0c                               |
    | shl dword [rbp + 1 * rcx], 0x01                                    | d1 64 0d 00                            |
    | shl dword [rsi + 1 * rcx], 0x01                                    | d1 24 0e                               |
    | shl dword [rdi + 1 * rcx], 0x01                                    | d1 24 0f                               |
    | shl dword [r8 + 1 * rcx], 0x01                                     | 41 d1 24 08                            |
    | shl dword [r9 + 1 * rcx], 0x01                                     | 41 d1 24 09                            |
    | shl dword [r10 + 1 * rcx], 0x01                                    | 41 d1 24 0a                            |
    | shl dword [r11 + 1 * rcx], 0x01                                    | 41 d1 24 0b                            |
    | shl dword [r12 + 1 * rcx], 0x01                                    | 41 d1 24 0c                            |
    | shl dword [r13 + 1 * rcx], 0x01                                    | 41 d1 64 0d 00                         |
    | shl dword [r14 + 1 * rcx], 0x01                                    | 41 d1 24 0e                            |
    | shl dword [r15 + 1 * rcx], 0x01                                    | 41 d1 24 0f                            |
    | shl dword [rax + 1 * rax], 0x01                                    | d1 24 00                               |
    | shl dword [rax + 1 * rdx], 0x01                                    | d1 24 10                               |
    | shl dword [rax + 1 * rbx], 0x01                                    | d1 24 18                               |
    | shl dword [rax + 1 * rbp], 0x01                                    | d1 24 28                               |
    | shl dword [rax + 1 * rsi], 0x01                                    | d1 24 30                               |
    | shl dword [rax + 1 * rdi], 0x01                                    | d1 24 38                               |
    | shl dword [rax + 1 * r8], 0x01                                     | 42 d1 24 00                            |
    | shl dword [rax + 1 * r9], 0x01                                     | 42 d1 24 08                            |
    | shl dword [rax + 1 * r10], 0x01                                    | 42 d1 24 10                            |
    | shl dword [rax + 1 * r11], 0x01                                    | 42 d1 24 18                            |
    | shl dword [rax + 1 * r12], 0x01                                    | 42 d1 24 20                            |
    | shl dword [rax + 1 * r13], 0x01                                    | 42 d1 24 28                            |
    | shl dword [rax + 1 * r14], 0x01                                    | 42 d1 24 30                            |
    | shl dword [rax + 1 * r15], 0x01                                    | 42 d1 24 38                            |
    | shl dword [rax + 2 * rcx], 0x01                                    | d1 24 48                               |
    | shl dword [rax + 4 * rcx], 0x01                                    | d1 24 88                               |
    | shl dword [rax + 8 * rcx], 0x01                                    | d1 24 c8                               |
    | shl dword [r8 + 1 * r9], 0x01                                      | 43 d1 24 08                            |
    | shl dword [r8 + 2 * r9], 0x01                                      | 43 d1 24 48                            |
    | shl dword [r8 + 4 * r9], 0x01                                      | 43 d1 24 88                            |
    | shl dword [r8 + 8 * r9], 0x01                                      | 43 d1 24 c8                            |
    | shl dword [1 * rcx], 0x01                                          | d1 24 0d 00 00 00 00                   |
    | shl dword [2 * rcx], 0x01                                          | d1 24 4d 00 00 00 00                   |
    | shl dword [4 * rcx], 0x01                                          | d1 24 8d 00 00 00 00                   |
    | shl dword [8 * rcx], 0x01                                          | d1 24 cd 00 00 00 00                   |
    | shl dword [1 * r9], 0x01                                           | 42 d1 24 0d 00 00 00 00                |
    | shl dword [2 * r9], 0x01                                           | 42 d1 24 4d 00 00 00 00                |
    | shl dword [4 * r9], 0x01                                           | 42 d1 24 8d 00 00 00 00                |
    | shl dword [8 * r9], 0x01                                           | 42 d1 24 cd 00 00 00 00                |
    | shl dword [r13 + 8 * r12], 0x01                                    | 43 d1 64 e5 00                         |
    | shl dword [rsp + 4 * r15], 0x01                                    | 42 d1 24 bc                            |
    | shl dword [rax + 1 * rcx + 0x00], 0x01                             | d1 64 08 00                            |
    | shl dword [rax + 1 * rcx - 0x00], 0x01                             | d1 64 08 00                            |
    | shl dword [rax + 1 * rcx + 0x01], 0x01                             | d1 64 08 01                            |
    | shl dword [rax + 1 * rcx - 0x01], 0x01                             | d1 64 08 ff                            |
    | shl dword [rax + 1 * rcx + 0x00000001], 0x01                       | d1 a4 08 01 00 00 00                   |
    | shl dword [rax + 1 * rcx - 0x00000001], 0x01                       | d1 a4 08 ff ff ff ff                   |
    | shl dword [rax + 1 * rcx + 0x7f], 0x01                             | d1 64 08 7f                            |
    | shl dword [rax + 1 * rcx - 0x7f], 0x01                             | d1 64 08 81                            |
    | shl dword [rax + 1 * rcx + 0x80], 0x01                             | d1 a4 08 80 00 00 00                   |
    | shl dword [rax + 1 * rcx - 0x80], 0x01                             | d1 64 08 80                            |
    | shl dword [rax + 1 * rcx - 0x81], 0x01                             | d1 a4 08 7f ff ff ff                   |
    | shl dword [rax + 1 * rcx + 0xff], 0x01                             | d1 a4 08 ff 00 00 00                   |
    | shl dword [rax + 1 * rcx - 0xff], 0x01                             | d1 a4 08 01 ff ff ff                   |
    | shl dword [rax + 1 * rcx + 0x7fffffff], 0x01                       | d1 a4 08 ff ff ff 7f                   |
    | shl dword [rax + 1 * rcx - 0x7fffffff], 0x01                       | d1 a4 08 01 00 00 80                   |
    | shl dword [rax + 1 * rcx - 0x80000000], 0x01                       | d1 a4 08 00 00 00 80                   |
    | shl dword [r10 + 0x7f], 0x01                                       | 41 d1 62 7f                            |
    | shl dword [r10 + 0x80], 0x01                                       | 41 d1 a2 80 00 00 00                   |
    | shl dword [r10 - 0x80], 0x01                                       | 41 d1 62 80                            |
    | shl dword [r10 - 0x81], 0x01                                       | 41 d1 a2 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; shl dword [rel @prev5], 0x01      | 90 90 90 90 90 d1 25 f5 ff ff ff       |
    | .prev1: nop; shl dword [rel @prev1], 0x01                          | 90 d1 25 f9 ff ff ff                   |
    | shl dword [rel @next1], 0x01; nop; .next1: nop                     | d1 25 01 00 00 00 90 90                |
    | shl dword [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | d1 25 05 00 00 00 90 90 90 90 90 90    |
    | shl dword [rax], 0x00                                              | c1 20 00                               |
    | shl dword [rax], 0x7f                                              | c1 20 7f                               |
    | shl dword [rax], 0x80                                              | c1 20 80                               |
    | shl dword [rax], 0xff                                              | c1 20 ff                               |
    | shl dword [rcx], 0x7f                                              | c1 21 7f                               |
    | shl dword [rdx], 0x80                                              | c1 22 80                               |
    | shl dword [rbx], 0xff                                              | c1 23 ff                               |
    | shl dword [rsp], 0x00                                              | c1 24 24 00                            |
    | shl dword [rsi], 0x7f                                              | c1 26 7f                               |
    | shl dword [rdi], 0x80                                              | c1 27 80                               |
    | shl dword [r8], 0xff                                               | 41 c1 20 ff                            |
    | shl dword [r9], 0x00                                               | 41 c1 21 00                            |
    | shl dword [r11], 0x7f                                              | 41 c1 23 7f                            |
    | shl dword [r12], 0x80                                              | 41 c1 24 24 80                         |
    | shl dword [r13], 0xff                                              | 41 c1 65 00 ff                         |
    | shl dword [r14], 0x00                                              | 41 c1 26 00                            |
    | shl dword [rax + 1 * rcx], 0x7f                                    | c1 24 08 7f                            |
    | shl dword [rcx + 1 * rcx], 0x80                                    | c1 24 09 80                            |
    | shl dword [rdx + 1 * rcx], 0xff                                    | c1 24 0a ff                            |
    | shl dword [rbx + 1 * rcx], 0x00                                    | c1 24 0b 00                            |
    | shl dword [rbp + 1 * rcx], 0x7f                                    | c1 64 0d 00 7f                         |
    | shl dword [rsi + 1 * rcx], 0x80                                    | c1 24 0e 80                            |
    | shl dword [rdi + 1 * rcx], 0xff                                    | c1 24 0f ff                            |
    | shl dword [r8 + 1 * rcx], 0x00                                     | 41 c1 24 08 00                         |
    | shl dword [r10 + 1 * rcx], 0x7f                                    | 41 c1 24 0a 7f                         |
    | shl dword [r11 + 1 * rcx], 0x80                                    | 41 c1 24 0b 80                         |
    | shl dword [r12 + 1 * rcx], 0xff                                    | 41 c1 24 0c ff                         |
    | shl dword [r13 + 1 * rcx], 0x00                                    | 41 c1 64 0d 00 00                      |
    | shl dword [r15 + 1 * rcx], 0x7f                                    | 41 c1 24 0f 7f                         |
    | shl dword [rax + 1 * rax], 0x80                                    | c1 24 00 80                            |
    | shl dword [rax + 1 * rdx], 0xff                                    | c1 24 10 ff                            |
    | shl dword [rax + 1 * rbx], 0x00                                    | c1 24 18 00                            |
    | shl dword [rax + 1 * rsi], 0x7f                                    | c1 24 30 7f                            |
    | shl dword [rax + 1 * rdi], 0x80                                    | c1 24 38 80                            |
    | shl dword [rax + 1 * r8], 0xff                                     | 42 c1 24 00 ff                         |
    | shl dword [rax + 1 * r9], 0x00                                     | 42 c1 24 08 00                         |
    | shl dword [rax + 1 * r11], 0x7f                                    | 42 c1 24 18 7f                         |
    | shl dword [rax + 1 * r12], 0x80                                    | 42 c1 24 20 80                         |
    | shl dword [rax + 1 * r13], 0xff                                    | 42 c1 24 28 ff                         |
    | shl dword [rax + 1 * r14], 0x00                                    | 42 c1 24 30 00                         |
    | shl dword [rax + 2 * rcx], 0x7f                                    | c1 24 48 7f                            |
    | shl dword [rax + 4 * rcx], 0x80                                    | c1 24 88 80                            |
    | shl dword [rax + 8 * rcx], 0xff                                    | c1 24 c8 ff                            |
    | shl dword [r8 + 1 * r9], 0x00                                      | 43 c1 24 08 00                         |
    | shl dword [r8 + 4 * r9], 0x7f                                      | 43 c1 24 88 7f                         |
    | shl dword [r8 + 8 * r9], 0x80                                      | 43 c1 24 c8 80                         |
    | shl dword [1 * rcx], 0xff                                          | c1 24 0d 00 00 00 00 ff                |
    | shl dword [2 * rcx], 0x00                                          | c1 24 4d 00 00 00 00 00                |
    | shl dword [8 * rcx], 0x7f                                          | c1 24 cd 00 00 00 00 7f                |
    | shl dword [1 * r9], 0x80                                           | 42 c1 24 0d 00 00 00 00 80             |
    | shl dword [2 * r9], 0xff                                           | 42 c1 24 4d 00 00 00 00 ff             |
    | shl dword [4 * r9], 0x00                                           | 42 c1 24 8d 00 00 00 00 00             |
    | shl dword [r13 + 8 * r12], 0x7f                                    | 43 c1 64 e5 00 7f                      |
    | shl dword [rsp + 4 * r15], 0x80                                    | 42 c1 24 bc 80                         |
    | shl dword [rax + 1 * rcx + 0x00], 0xff                             | c1 64 08 00 ff                         |
    | shl dword [rax + 1 * rcx - 0x00], 0x00                             | c1 64 08 00 00                         |
    | shl dword [rax + 1 * rcx - 0x01], 0x7f                             | c1 64 08 ff 7f                         |
    | shl dword [rax + 1 * rcx + 0x00000001], 0x80                       | c1 a4 08 01 00 00 00 80                |
    | shl dword [rax + 1 * rcx - 0x00000001], 0xff                       | c1 a4 08 ff ff ff ff ff                |
    | shl dword [rax + 1 * rcx + 0x7f], 0x00                             | c1 64 08 7f 00                         |
    | shl dword [rax + 1 * rcx + 0x80], 0x7f                             | c1 a4 08 80 00 00 00 7f                |
    | shl dword [rax + 1 * rcx - 0x80], 0x80                             | c1 64 08 80 80                         |
    | shl dword [rax + 1 * rcx - 0x81], 0xff                             | c1 a4 08 7f ff ff ff ff                |
    | shl dword [rax + 1 * rcx + 0xff], 0x00                             | c1 a4 08 ff 00 00 00 00                |
    | shl dword [rax + 1 * rcx + 0x7fffffff], 0x7f                       | c1 a4 08 ff ff ff 7f 7f                |
    | shl dword [rax + 1 * rcx - 0x7fffffff], 0x80                       | c1 a4 08 01 00 00 80 80                |
    | shl dword [rax + 1 * rcx - 0x80000000], 0xff                       | c1 a4 08 00 00 00 80 ff                |
    | shl dword [r10 + 0x7f], 0x00                                       | 41 c1 62 7f 00                         |
    | shl dword [r10 - 0x80], 0x7f                                       | 41 c1 62 80 7f                         |
    | shl dword [r10 - 0x81], 0x80                                       | 41 c1 a2 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; shl dword [rel @prev5], 0xff      | 90 90 90 90 90 c1 25 f4 ff ff ff ff    |
    | .prev1: nop; shl dword [rel @prev1], 0x00                          | 90 c1 25 f8 ff ff ff 00                |
    | shl dword [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | c1 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ------------------------------------------------------------------ | -------------------------------------- |
"""


def can_encode_shl_addr32_imm8():
    encode(SHL_ADDR32_IMM8)


SHL_ADDR32_CL = """
    | ---------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                      | encoding                            |
    | ---------------------------------------------------------------- | ----------------------------------- |
    | shl dword [rax], cl                                              | d3 20                               |
    | shl dword [rcx], cl                                              | d3 21                               |
    | shl dword [rdx], cl                                              | d3 22                               |
    | shl dword [rbx], cl                                              | d3 23                               |
    | shl dword [rsp], cl                                              | d3 24 24                            |
    | shl dword [rbp], cl                                              | d3 65 00                            |
    | shl dword [rsi], cl                                              | d3 26                               |
    | shl dword [rdi], cl                                              | d3 27                               |
    | shl dword [r8], cl                                               | 41 d3 20                            |
    | shl dword [r9], cl                                               | 41 d3 21                            |
    | shl dword [r10], cl                                              | 41 d3 22                            |
    | shl dword [r11], cl                                              | 41 d3 23                            |
    | shl dword [r12], cl                                              | 41 d3 24 24                         |
    | shl dword [r13], cl                                              | 41 d3 65 00                         |
    | shl dword [r14], cl                                              | 41 d3 26                            |
    | shl dword [r15], cl                                              | 41 d3 27                            |
    | shl dword [rax + 1 * rcx], cl                                    | d3 24 08                            |
    | shl dword [rcx + 1 * rcx], cl                                    | d3 24 09                            |
    | shl dword [rdx + 1 * rcx], cl                                    | d3 24 0a                            |
    | shl dword [rbx + 1 * rcx], cl                                    | d3 24 0b                            |
    | shl dword [rsp + 1 * rcx], cl                                    | d3 24 0c                            |
    | shl dword [rbp + 1 * rcx], cl                                    | d3 64 0d 00                         |
    | shl dword [rsi + 1 * rcx], cl                                    | d3 24 0e                            |
    | shl dword [rdi + 1 * rcx], cl                                    | d3 24 0f                            |
    | shl dword [r8 + 1 * rcx], cl                                     | 41 d3 24 08                         |
    | shl dword [r9 + 1 * rcx], cl                                     | 41 d3 24 09                         |
    | shl dword [r10 + 1 * rcx], cl                                    | 41 d3 24 0a                         |
    | shl dword [r11 + 1 * rcx], cl                                    | 41 d3 24 0b                         |
    | shl dword [r12 + 1 * rcx], cl                                    | 41 d3 24 0c                         |
    | shl dword [r13 + 1 * rcx], cl                                    | 41 d3 64 0d 00                      |
    | shl dword [r14 + 1 * rcx], cl                                    | 41 d3 24 0e                         |
    | shl dword [r15 + 1 * rcx], cl                                    | 41 d3 24 0f                         |
    | shl dword [rax + 1 * rax], cl                                    | d3 24 00                            |
    | shl dword [rax + 1 * rdx], cl                                    | d3 24 10                            |
    | shl dword [rax + 1 * rbx], cl                                    | d3 24 18                            |
    | shl dword [rax + 1 * rbp], cl                                    | d3 24 28                            |
    | shl dword [rax + 1 * rsi], cl                                    | d3 24 30                            |
    | shl dword [rax + 1 * rdi], cl                                    | d3 24 38                            |
    | shl dword [rax + 1 * r8], cl                                     | 42 d3 24 00                         |
    | shl dword [rax + 1 * r9], cl                                     | 42 d3 24 08                         |
    | shl dword [rax + 1 * r10], cl                                    | 42 d3 24 10                         |
    | shl dword [rax + 1 * r11], cl                                    | 42 d3 24 18                         |
    | shl dword [rax + 1 * r12], cl                                    | 42 d3 24 20                         |
    | shl dword [rax + 1 * r13], cl                                    | 42 d3 24 28                         |
    | shl dword [rax + 1 * r14], cl                                    | 42 d3 24 30                         |
    | shl dword [rax + 1 * r15], cl                                    | 42 d3 24 38                         |
    | shl dword [rax + 2 * rcx], cl                                    | d3 24 48                            |
    | shl dword [rax + 4 * rcx], cl                                    | d3 24 88                            |
    | shl dword [rax + 8 * rcx], cl                                    | d3 24 c8                            |
    | shl dword [r8 + 1 * r9], cl                                      | 43 d3 24 08                         |
    | shl dword [r8 + 2 * r9], cl                                      | 43 d3 24 48                         |
    | shl dword [r8 + 4 * r9], cl                                      | 43 d3 24 88                         |
    | shl dword [r8 + 8 * r9], cl                                      | 43 d3 24 c8                         |
    | shl dword [1 * rcx], cl                                          | d3 24 0d 00 00 00 00                |
    | shl dword [2 * rcx], cl                                          | d3 24 4d 00 00 00 00                |
    | shl dword [4 * rcx], cl                                          | d3 24 8d 00 00 00 00                |
    | shl dword [8 * rcx], cl                                          | d3 24 cd 00 00 00 00                |
    | shl dword [1 * r9], cl                                           | 42 d3 24 0d 00 00 00 00             |
    | shl dword [2 * r9], cl                                           | 42 d3 24 4d 00 00 00 00             |
    | shl dword [4 * r9], cl                                           | 42 d3 24 8d 00 00 00 00             |
    | shl dword [8 * r9], cl                                           | 42 d3 24 cd 00 00 00 00             |
    | shl dword [r13 + 8 * r12], cl                                    | 43 d3 64 e5 00                      |
    | shl dword [rsp + 4 * r15], cl                                    | 42 d3 24 bc                         |
    | shl dword [rax + 1 * rcx + 0x00], cl                             | d3 64 08 00                         |
    | shl dword [rax + 1 * rcx - 0x00], cl                             | d3 64 08 00                         |
    | shl dword [rax + 1 * rcx + 0x01], cl                             | d3 64 08 01                         |
    | shl dword [rax + 1 * rcx - 0x01], cl                             | d3 64 08 ff                         |
    | shl dword [rax + 1 * rcx + 0x00000001], cl                       | d3 a4 08 01 00 00 00                |
    | shl dword [rax + 1 * rcx - 0x00000001], cl                       | d3 a4 08 ff ff ff ff                |
    | shl dword [rax + 1 * rcx + 0x7f], cl                             | d3 64 08 7f                         |
    | shl dword [rax + 1 * rcx - 0x7f], cl                             | d3 64 08 81                         |
    | shl dword [rax + 1 * rcx + 0x80], cl                             | d3 a4 08 80 00 00 00                |
    | shl dword [rax + 1 * rcx - 0x80], cl                             | d3 64 08 80                         |
    | shl dword [rax + 1 * rcx - 0x81], cl                             | d3 a4 08 7f ff ff ff                |
    | shl dword [rax + 1 * rcx + 0xff], cl                             | d3 a4 08 ff 00 00 00                |
    | shl dword [rax + 1 * rcx - 0xff], cl                             | d3 a4 08 01 ff ff ff                |
    | shl dword [rax + 1 * rcx + 0x7fffffff], cl                       | d3 a4 08 ff ff ff 7f                |
    | shl dword [rax + 1 * rcx - 0x7fffffff], cl                       | d3 a4 08 01 00 00 80                |
    | shl dword [rax + 1 * rcx - 0x80000000], cl                       | d3 a4 08 00 00 00 80                |
    | shl dword [r10 + 0x7f], cl                                       | 41 d3 62 7f                         |
    | shl dword [r10 + 0x80], cl                                       | 41 d3 a2 80 00 00 00                |
    | shl dword [r10 - 0x80], cl                                       | 41 d3 62 80                         |
    | shl dword [r10 - 0x81], cl                                       | 41 d3 a2 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; shl dword [rel @prev5], cl      | 90 90 90 90 90 d3 25 f5 ff ff ff    |
    | .prev1: nop; shl dword [rel @prev1], cl                          | 90 d3 25 f9 ff ff ff                |
    | shl dword [rel @next1], cl; nop; .next1: nop                     | d3 25 01 00 00 00 90 90             |
    | shl dword [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | d3 25 05 00 00 00 90 90 90 90 90 90 |
    | ---------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_shl_addr32_cl():
    encode(SHL_ADDR32_CL)


SHL_ADDR16_IMM8 = """
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | instruction                                                       | encoding                                  |
    | ----------------------------------------------------------------- | ----------------------------------------- |
    | shl word [rax], 0x01                                              | 66 d1 20                                  |
    | shl word [rcx], 0x01                                              | 66 d1 21                                  |
    | shl word [rdx], 0x01                                              | 66 d1 22                                  |
    | shl word [rbx], 0x01                                              | 66 d1 23                                  |
    | shl word [rsp], 0x01                                              | 66 d1 24 24                               |
    | shl word [rbp], 0x01                                              | 66 d1 65 00                               |
    | shl word [rsi], 0x01                                              | 66 d1 26                                  |
    | shl word [rdi], 0x01                                              | 66 d1 27                                  |
    | shl word [r8], 0x01                                               | 66 41 d1 20                               |
    | shl word [r9], 0x01                                               | 66 41 d1 21                               |
    | shl word [r10], 0x01                                              | 66 41 d1 22                               |
    | shl word [r11], 0x01                                              | 66 41 d1 23                               |
    | shl word [r12], 0x01                                              | 66 41 d1 24 24                            |
    | shl word [r13], 0x01                                              | 66 41 d1 65 00                            |
    | shl word [r14], 0x01                                              | 66 41 d1 26                               |
    | shl word [r15], 0x01                                              | 66 41 d1 27                               |
    | shl word [rax + 1 * rcx], 0x01                                    | 66 d1 24 08                               |
    | shl word [rcx + 1 * rcx], 0x01                                    | 66 d1 24 09                               |
    | shl word [rdx + 1 * rcx], 0x01                                    | 66 d1 24 0a                               |
    | shl word [rbx + 1 * rcx], 0x01                                    | 66 d1 24 0b                               |
    | shl word [rsp + 1 * rcx], 0x01                                    | 66 d1 24 0c                               |
    | shl word [rbp + 1 * rcx], 0x01                                    | 66 d1 64 0d 00                            |
    | shl word [rsi + 1 * rcx], 0x01                                    | 66 d1 24 0e                               |
    | shl word [rdi + 1 * rcx], 0x01                                    | 66 d1 24 0f                               |
    | shl word [r8 + 1 * rcx], 0x01                                     | 66 41 d1 24 08                            |
    | shl word [r9 + 1 * rcx], 0x01                                     | 66 41 d1 24 09                            |
    | shl word [r10 + 1 * rcx], 0x01                                    | 66 41 d1 24 0a                            |
    | shl word [r11 + 1 * rcx], 0x01                                    | 66 41 d1 24 0b                            |
    | shl word [r12 + 1 * rcx], 0x01                                    | 66 41 d1 24 0c                            |
    | shl word [r13 + 1 * rcx], 0x01                                    | 66 41 d1 64 0d 00                         |
    | shl word [r14 + 1 * rcx], 0x01                                    | 66 41 d1 24 0e                            |
    | shl word [r15 + 1 * rcx], 0x01                                    | 66 41 d1 24 0f                            |
    | shl word [rax + 1 * rax], 0x01                                    | 66 d1 24 00                               |
    | shl word [rax + 1 * rdx], 0x01                                    | 66 d1 24 10                               |
    | shl word [rax + 1 * rbx], 0x01                                    | 66 d1 24 18                               |
    | shl word [rax + 1 * rbp], 0x01                                    | 66 d1 24 28                               |
    | shl word [rax + 1 * rsi], 0x01                                    | 66 d1 24 30                               |
    | shl word [rax + 1 * rdi], 0x01                                    | 66 d1 24 38                               |
    | shl word [rax + 1 * r8], 0x01                                     | 66 42 d1 24 00                            |
    | shl word [rax + 1 * r9], 0x01                                     | 66 42 d1 24 08                            |
    | shl word [rax + 1 * r10], 0x01                                    | 66 42 d1 24 10                            |
    | shl word [rax + 1 * r11], 0x01                                    | 66 42 d1 24 18                            |
    | shl word [rax + 1 * r12], 0x01                                    | 66 42 d1 24 20                            |
    | shl word [rax + 1 * r13], 0x01                                    | 66 42 d1 24 28                            |
    | shl word [rax + 1 * r14], 0x01                                    | 66 42 d1 24 30                            |
    | shl word [rax + 1 * r15], 0x01                                    | 66 42 d1 24 38                            |
    | shl word [rax + 2 * rcx], 0x01                                    | 66 d1 24 48                               |
    | shl word [rax + 4 * rcx], 0x01                                    | 66 d1 24 88                               |
    | shl word [rax + 8 * rcx], 0x01                                    | 66 d1 24 c8                               |
    | shl word [r8 + 1 * r9], 0x01                                      | 66 43 d1 24 08                            |
    | shl word [r8 + 2 * r9], 0x01                                      | 66 43 d1 24 48                            |
    | shl word [r8 + 4 * r9], 0x01                                      | 66 43 d1 24 88                            |
    | shl word [r8 + 8 * r9], 0x01                                      | 66 43 d1 24 c8                            |
    | shl word [1 * rcx], 0x01                                          | 66 d1 24 0d 00 00 00 00                   |
    | shl word [2 * rcx], 0x01                                          | 66 d1 24 4d 00 00 00 00                   |
    | shl word [4 * rcx], 0x01                                          | 66 d1 24 8d 00 00 00 00                   |
    | shl word [8 * rcx], 0x01                                          | 66 d1 24 cd 00 00 00 00                   |
    | shl word [1 * r9], 0x01                                           | 66 42 d1 24 0d 00 00 00 00                |
    | shl word [2 * r9], 0x01                                           | 66 42 d1 24 4d 00 00 00 00                |
    | shl word [4 * r9], 0x01                                           | 66 42 d1 24 8d 00 00 00 00                |
    | shl word [8 * r9], 0x01                                           | 66 42 d1 24 cd 00 00 00 00                |
    | shl word [r13 + 8 * r12], 0x01                                    | 66 43 d1 64 e5 00                         |
    | shl word [rsp + 4 * r15], 0x01                                    | 66 42 d1 24 bc                            |
    | shl word [rax + 1 * rcx + 0x00], 0x01                             | 66 d1 64 08 00                            |
    | shl word [rax + 1 * rcx - 0x00], 0x01                             | 66 d1 64 08 00                            |
    | shl word [rax + 1 * rcx + 0x01], 0x01                             | 66 d1 64 08 01                            |
    | shl word [rax + 1 * rcx - 0x01], 0x01                             | 66 d1 64 08 ff                            |
    | shl word [rax + 1 * rcx + 0x00000001], 0x01                       | 66 d1 a4 08 01 00 00 00                   |
    | shl word [rax + 1 * rcx - 0x00000001], 0x01                       | 66 d1 a4 08 ff ff ff ff                   |
    | shl word [rax + 1 * rcx + 0x7f], 0x01                             | 66 d1 64 08 7f                            |
    | shl word [rax + 1 * rcx - 0x7f], 0x01                             | 66 d1 64 08 81                            |
    | shl word [rax + 1 * rcx + 0x80], 0x01                             | 66 d1 a4 08 80 00 00 00                   |
    | shl word [rax + 1 * rcx - 0x80], 0x01                             | 66 d1 64 08 80                            |
    | shl word [rax + 1 * rcx - 0x81], 0x01                             | 66 d1 a4 08 7f ff ff ff                   |
    | shl word [rax + 1 * rcx + 0xff], 0x01                             | 66 d1 a4 08 ff 00 00 00                   |
    | shl word [rax + 1 * rcx - 0xff], 0x01                             | 66 d1 a4 08 01 ff ff ff                   |
    | shl word [rax + 1 * rcx + 0x7fffffff], 0x01                       | 66 d1 a4 08 ff ff ff 7f                   |
    | shl word [rax + 1 * rcx - 0x7fffffff], 0x01                       | 66 d1 a4 08 01 00 00 80                   |
    | shl word [rax + 1 * rcx - 0x80000000], 0x01                       | 66 d1 a4 08 00 00 00 80                   |
    | shl word [r10 + 0x7f], 0x01                                       | 66 41 d1 62 7f                            |
    | shl word [r10 + 0x80], 0x01                                       | 66 41 d1 a2 80 00 00 00                   |
    | shl word [r10 - 0x80], 0x01                                       | 66 41 d1 62 80                            |
    | shl word [r10 - 0x81], 0x01                                       | 66 41 d1 a2 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; shl word [rel @prev5], 0x01      | 90 90 90 90 90 66 d1 25 f4 ff ff ff       |
    | .prev1: nop; shl word [rel @prev1], 0x01                          | 90 66 d1 25 f8 ff ff ff                   |
    | shl word [rel @next1], 0x01; nop; .next1: nop                     | 66 d1 25 01 00 00 00 90 90                |
    | shl word [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | 66 d1 25 05 00 00 00 90 90 90 90 90 90    |
    | shl word [rax], 0x00                                              | 66 c1 20 00                               |
    | shl word [rax], 0x7f                                              | 66 c1 20 7f                               |
    | shl word [rax], 0x80                                              | 66 c1 20 80                               |
    | shl word [rax], 0xff                                              | 66 c1 20 ff                               |
    | shl word [rcx], 0x7f                                              | 66 c1 21 7f                               |
    | shl word [rdx], 0x80                                              | 66 c1 22 80                               |
    | shl word [rbx], 0xff                                              | 66 c1 23 ff                               |
    | shl word [rsp], 0x00                                              | 66 c1 24 24 00                            |
    | shl word [rsi], 0x7f                                              | 66 c1 26 7f                               |
    | shl word [rdi], 0x80                                              | 66 c1 27 80                               |
    | shl word [r8], 0xff                                               | 66 41 c1 20 ff                            |
    | shl word [r9], 0x00                                               | 66 41 c1 21 00                            |
    | shl word [r11], 0x7f                                              | 66 41 c1 23 7f                            |
    | shl word [r12], 0x80                                              | 66 41 c1 24 24 80                         |
    | shl word [r13], 0xff                                              | 66 41 c1 65 00 ff                         |
    | shl word [r14], 0x00                                              | 66 41 c1 26 00                            |
    | shl word [rax + 1 * rcx], 0x7f                                    | 66 c1 24 08 7f                            |
    | shl word [rcx + 1 * rcx], 0x80                                    | 66 c1 24 09 80                            |
    | shl word [rdx + 1 * rcx], 0xff                                    | 66 c1 24 0a ff                            |
    | shl word [rbx + 1 * rcx], 0x00                                    | 66 c1 24 0b 00                            |
    | shl word [rbp + 1 * rcx], 0x7f                                    | 66 c1 64 0d 00 7f                         |
    | shl word [rsi + 1 * rcx], 0x80                                    | 66 c1 24 0e 80                            |
    | shl word [rdi + 1 * rcx], 0xff                                    | 66 c1 24 0f ff                            |
    | shl word [r8 + 1 * rcx], 0x00                                     | 66 41 c1 24 08 00                         |
    | shl word [r10 + 1 * rcx], 0x7f                                    | 66 41 c1 24 0a 7f                         |
    | shl word [r11 + 1 * rcx], 0x80                                    | 66 41 c1 24 0b 80                         |
    | shl word [r12 + 1 * rcx], 0xff                                    | 66 41 c1 24 0c ff                         |
    | shl word [r13 + 1 * rcx], 0x00                                    | 66 41 c1 64 0d 00 00                      |
    | shl word [r15 + 1 * rcx], 0x7f                                    | 66 41 c1 24 0f 7f                         |
    | shl word [rax + 1 * rax], 0x80                                    | 66 c1 24 00 80                            |
    | shl word [rax + 1 * rdx], 0xff                                    | 66 c1 24 10 ff                            |
    | shl word [rax + 1 * rbx], 0x00                                    | 66 c1 24 18 00                            |
    | shl word [rax + 1 * rsi], 0x7f                                    | 66 c1 24 30 7f                            |
    | shl word [rax + 1 * rdi], 0x80                                    | 66 c1 24 38 80                            |
    | shl word [rax + 1 * r8], 0xff                                     | 66 42 c1 24 00 ff                         |
    | shl word [rax + 1 * r9], 0x00                                     | 66 42 c1 24 08 00                         |
    | shl word [rax + 1 * r11], 0x7f                                    | 66 42 c1 24 18 7f                         |
    | shl word [rax + 1 * r12], 0x80                                    | 66 42 c1 24 20 80                         |
    | shl word [rax + 1 * r13], 0xff                                    | 66 42 c1 24 28 ff                         |
    | shl word [rax + 1 * r14], 0x00                                    | 66 42 c1 24 30 00                         |
    | shl word [rax + 2 * rcx], 0x7f                                    | 66 c1 24 48 7f                            |
    | shl word [rax + 4 * rcx], 0x80                                    | 66 c1 24 88 80                            |
    | shl word [rax + 8 * rcx], 0xff                                    | 66 c1 24 c8 ff                            |
    | shl word [r8 + 1 * r9], 0x00                                      | 66 43 c1 24 08 00                         |
    | shl word [r8 + 4 * r9], 0x7f                                      | 66 43 c1 24 88 7f                         |
    | shl word [r8 + 8 * r9], 0x80                                      | 66 43 c1 24 c8 80                         |
    | shl word [1 * rcx], 0xff                                          | 66 c1 24 0d 00 00 00 00 ff                |
    | shl word [2 * rcx], 0x00                                          | 66 c1 24 4d 00 00 00 00 00                |
    | shl word [8 * rcx], 0x7f                                          | 66 c1 24 cd 00 00 00 00 7f                |
    | shl word [1 * r9], 0x80                                           | 66 42 c1 24 0d 00 00 00 00 80             |
    | shl word [2 * r9], 0xff                                           | 66 42 c1 24 4d 00 00 00 00 ff             |
    | shl word [4 * r9], 0x00                                           | 66 42 c1 24 8d 00 00 00 00 00             |
    | shl word [r13 + 8 * r12], 0x7f                                    | 66 43 c1 64 e5 00 7f                      |
    | shl word [rsp + 4 * r15], 0x80                                    | 66 42 c1 24 bc 80                         |
    | shl word [rax + 1 * rcx + 0x00], 0xff                             | 66 c1 64 08 00 ff                         |
    | shl word [rax + 1 * rcx - 0x00], 0x00                             | 66 c1 64 08 00 00                         |
    | shl word [rax + 1 * rcx - 0x01], 0x7f                             | 66 c1 64 08 ff 7f                         |
    | shl word [rax + 1 * rcx + 0x00000001], 0x80                       | 66 c1 a4 08 01 00 00 00 80                |
    | shl word [rax + 1 * rcx - 0x00000001], 0xff                       | 66 c1 a4 08 ff ff ff ff ff                |
    | shl word [rax + 1 * rcx + 0x7f], 0x00                             | 66 c1 64 08 7f 00                         |
    | shl word [rax + 1 * rcx + 0x80], 0x7f                             | 66 c1 a4 08 80 00 00 00 7f                |
    | shl word [rax + 1 * rcx - 0x80], 0x80                             | 66 c1 64 08 80 80                         |
    | shl word [rax + 1 * rcx - 0x81], 0xff                             | 66 c1 a4 08 7f ff ff ff ff                |
    | shl word [rax + 1 * rcx + 0xff], 0x00                             | 66 c1 a4 08 ff 00 00 00 00                |
    | shl word [rax + 1 * rcx + 0x7fffffff], 0x7f                       | 66 c1 a4 08 ff ff ff 7f 7f                |
    | shl word [rax + 1 * rcx - 0x7fffffff], 0x80                       | 66 c1 a4 08 01 00 00 80 80                |
    | shl word [rax + 1 * rcx - 0x80000000], 0xff                       | 66 c1 a4 08 00 00 00 80 ff                |
    | shl word [r10 + 0x7f], 0x00                                       | 66 41 c1 62 7f 00                         |
    | shl word [r10 - 0x80], 0x7f                                       | 66 41 c1 62 80 7f                         |
    | shl word [r10 - 0x81], 0x80                                       | 66 41 c1 a2 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; shl word [rel @prev5], 0xff      | 90 90 90 90 90 66 c1 25 f3 ff ff ff ff    |
    | .prev1: nop; shl word [rel @prev1], 0x00                          | 90 66 c1 25 f7 ff ff ff 00                |
    | shl word [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | 66 c1 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | ----------------------------------------- |
"""


def can_encode_shl_addr16_imm8():
    encode(SHL_ADDR16_IMM8)


SHL_ADDR16_CL = """
    | --------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                     | encoding                               |
    | --------------------------------------------------------------- | -------------------------------------- |
    | shl word [rax], cl                                              | 66 d3 20                               |
    | shl word [rcx], cl                                              | 66 d3 21                               |
    | shl word [rdx], cl                                              | 66 d3 22                               |
    | shl word [rbx], cl                                              | 66 d3 23                               |
    | shl word [rsp], cl                                              | 66 d3 24 24                            |
    | shl word [rbp], cl                                              | 66 d3 65 00                            |
    | shl word [rsi], cl                                              | 66 d3 26                               |
    | shl word [rdi], cl                                              | 66 d3 27                               |
    | shl word [r8], cl                                               | 66 41 d3 20                            |
    | shl word [r9], cl                                               | 66 41 d3 21                            |
    | shl word [r10], cl                                              | 66 41 d3 22                            |
    | shl word [r11], cl                                              | 66 41 d3 23                            |
    | shl word [r12], cl                                              | 66 41 d3 24 24                         |
    | shl word [r13], cl                                              | 66 41 d3 65 00                         |
    | shl word [r14], cl                                              | 66 41 d3 26                            |
    | shl word [r15], cl                                              | 66 41 d3 27                            |
    | shl word [rax + 1 * rcx], cl                                    | 66 d3 24 08                            |
    | shl word [rcx + 1 * rcx], cl                                    | 66 d3 24 09                            |
    | shl word [rdx + 1 * rcx], cl                                    | 66 d3 24 0a                            |
    | shl word [rbx + 1 * rcx], cl                                    | 66 d3 24 0b                            |
    | shl word [rsp + 1 * rcx], cl                                    | 66 d3 24 0c                            |
    | shl word [rbp + 1 * rcx], cl                                    | 66 d3 64 0d 00                         |
    | shl word [rsi + 1 * rcx], cl                                    | 66 d3 24 0e                            |
    | shl word [rdi + 1 * rcx], cl                                    | 66 d3 24 0f                            |
    | shl word [r8 + 1 * rcx], cl                                     | 66 41 d3 24 08                         |
    | shl word [r9 + 1 * rcx], cl                                     | 66 41 d3 24 09                         |
    | shl word [r10 + 1 * rcx], cl                                    | 66 41 d3 24 0a                         |
    | shl word [r11 + 1 * rcx], cl                                    | 66 41 d3 24 0b                         |
    | shl word [r12 + 1 * rcx], cl                                    | 66 41 d3 24 0c                         |
    | shl word [r13 + 1 * rcx], cl                                    | 66 41 d3 64 0d 00                      |
    | shl word [r14 + 1 * rcx], cl                                    | 66 41 d3 24 0e                         |
    | shl word [r15 + 1 * rcx], cl                                    | 66 41 d3 24 0f                         |
    | shl word [rax + 1 * rax], cl                                    | 66 d3 24 00                            |
    | shl word [rax + 1 * rdx], cl                                    | 66 d3 24 10                            |
    | shl word [rax + 1 * rbx], cl                                    | 66 d3 24 18                            |
    | shl word [rax + 1 * rbp], cl                                    | 66 d3 24 28                            |
    | shl word [rax + 1 * rsi], cl                                    | 66 d3 24 30                            |
    | shl word [rax + 1 * rdi], cl                                    | 66 d3 24 38                            |
    | shl word [rax + 1 * r8], cl                                     | 66 42 d3 24 00                         |
    | shl word [rax + 1 * r9], cl                                     | 66 42 d3 24 08                         |
    | shl word [rax + 1 * r10], cl                                    | 66 42 d3 24 10                         |
    | shl word [rax + 1 * r11], cl                                    | 66 42 d3 24 18                         |
    | shl word [rax + 1 * r12], cl                                    | 66 42 d3 24 20                         |
    | shl word [rax + 1 * r13], cl                                    | 66 42 d3 24 28                         |
    | shl word [rax + 1 * r14], cl                                    | 66 42 d3 24 30                         |
    | shl word [rax + 1 * r15], cl                                    | 66 42 d3 24 38                         |
    | shl word [rax + 2 * rcx], cl                                    | 66 d3 24 48                            |
    | shl word [rax + 4 * rcx], cl                                    | 66 d3 24 88                            |
    | shl word [rax + 8 * rcx], cl                                    | 66 d3 24 c8                            |
    | shl word [r8 + 1 * r9], cl                                      | 66 43 d3 24 08                         |
    | shl word [r8 + 2 * r9], cl                                      | 66 43 d3 24 48                         |
    | shl word [r8 + 4 * r9], cl                                      | 66 43 d3 24 88                         |
    | shl word [r8 + 8 * r9], cl                                      | 66 43 d3 24 c8                         |
    | shl word [1 * rcx], cl                                          | 66 d3 24 0d 00 00 00 00                |
    | shl word [2 * rcx], cl                                          | 66 d3 24 4d 00 00 00 00                |
    | shl word [4 * rcx], cl                                          | 66 d3 24 8d 00 00 00 00                |
    | shl word [8 * rcx], cl                                          | 66 d3 24 cd 00 00 00 00                |
    | shl word [1 * r9], cl                                           | 66 42 d3 24 0d 00 00 00 00             |
    | shl word [2 * r9], cl                                           | 66 42 d3 24 4d 00 00 00 00             |
    | shl word [4 * r9], cl                                           | 66 42 d3 24 8d 00 00 00 00             |
    | shl word [8 * r9], cl                                           | 66 42 d3 24 cd 00 00 00 00             |
    | shl word [r13 + 8 * r12], cl                                    | 66 43 d3 64 e5 00                      |
    | shl word [rsp + 4 * r15], cl                                    | 66 42 d3 24 bc                         |
    | shl word [rax + 1 * rcx + 0x00], cl                             | 66 d3 64 08 00                         |
    | shl word [rax + 1 * rcx - 0x00], cl                             | 66 d3 64 08 00                         |
    | shl word [rax + 1 * rcx + 0x01], cl                             | 66 d3 64 08 01                         |
    | shl word [rax + 1 * rcx - 0x01], cl                             | 66 d3 64 08 ff                         |
    | shl word [rax + 1 * rcx + 0x00000001], cl                       | 66 d3 a4 08 01 00 00 00                |
    | shl word [rax + 1 * rcx - 0x00000001], cl                       | 66 d3 a4 08 ff ff ff ff                |
    | shl word [rax + 1 * rcx + 0x7f], cl                             | 66 d3 64 08 7f                         |
    | shl word [rax + 1 * rcx - 0x7f], cl                             | 66 d3 64 08 81                         |
    | shl word [rax + 1 * rcx + 0x80], cl                             | 66 d3 a4 08 80 00 00 00                |
    | shl word [rax + 1 * rcx - 0x80], cl                             | 66 d3 64 08 80                         |
    | shl word [rax + 1 * rcx - 0x81], cl                             | 66 d3 a4 08 7f ff ff ff                |
    | shl word [rax + 1 * rcx + 0xff], cl                             | 66 d3 a4 08 ff 00 00 00                |
    | shl word [rax + 1 * rcx - 0xff], cl                             | 66 d3 a4 08 01 ff ff ff                |
    | shl word [rax + 1 * rcx + 0x7fffffff], cl                       | 66 d3 a4 08 ff ff ff 7f                |
    | shl word [rax + 1 * rcx - 0x7fffffff], cl                       | 66 d3 a4 08 01 00 00 80                |
    | shl word [rax + 1 * rcx - 0x80000000], cl                       | 66 d3 a4 08 00 00 00 80                |
    | shl word [r10 + 0x7f], cl                                       | 66 41 d3 62 7f                         |
    | shl word [r10 + 0x80], cl                                       | 66 41 d3 a2 80 00 00 00                |
    | shl word [r10 - 0x80], cl                                       | 66 41 d3 62 80                         |
    | shl word [r10 - 0x81], cl                                       | 66 41 d3 a2 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; shl word [rel @prev5], cl      | 90 90 90 90 90 66 d3 25 f4 ff ff ff    |
    | .prev1: nop; shl word [rel @prev1], cl                          | 90 66 d3 25 f8 ff ff ff                |
    | shl word [rel @next1], cl; nop; .next1: nop                     | 66 d3 25 01 00 00 00 90 90             |
    | shl word [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | 66 d3 25 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_shl_addr16_cl():
    encode(SHL_ADDR16_CL)


SHL_ADDR8_IMM8 = """
    | ----------------------------------------------------------------- | -------------------------------------- |
    | instruction                                                       | encoding                               |
    | ----------------------------------------------------------------- | -------------------------------------- |
    | shl byte [rax], 0x01                                              | d0 20                                  |
    | shl byte [rcx], 0x01                                              | d0 21                                  |
    | shl byte [rdx], 0x01                                              | d0 22                                  |
    | shl byte [rbx], 0x01                                              | d0 23                                  |
    | shl byte [rsp], 0x01                                              | d0 24 24                               |
    | shl byte [rbp], 0x01                                              | d0 65 00                               |
    | shl byte [rsi], 0x01                                              | d0 26                                  |
    | shl byte [rdi], 0x01                                              | d0 27                                  |
    | shl byte [r8], 0x01                                               | 41 d0 20                               |
    | shl byte [r9], 0x01                                               | 41 d0 21                               |
    | shl byte [r10], 0x01                                              | 41 d0 22                               |
    | shl byte [r11], 0x01                                              | 41 d0 23                               |
    | shl byte [r12], 0x01                                              | 41 d0 24 24                            |
    | shl byte [r13], 0x01                                              | 41 d0 65 00                            |
    | shl byte [r14], 0x01                                              | 41 d0 26                               |
    | shl byte [r15], 0x01                                              | 41 d0 27                               |
    | shl byte [rax + 1 * rcx], 0x01                                    | d0 24 08                               |
    | shl byte [rcx + 1 * rcx], 0x01                                    | d0 24 09                               |
    | shl byte [rdx + 1 * rcx], 0x01                                    | d0 24 0a                               |
    | shl byte [rbx + 1 * rcx], 0x01                                    | d0 24 0b                               |
    | shl byte [rsp + 1 * rcx], 0x01                                    | d0 24 0c                               |
    | shl byte [rbp + 1 * rcx], 0x01                                    | d0 64 0d 00                            |
    | shl byte [rsi + 1 * rcx], 0x01                                    | d0 24 0e                               |
    | shl byte [rdi + 1 * rcx], 0x01                                    | d0 24 0f                               |
    | shl byte [r8 + 1 * rcx], 0x01                                     | 41 d0 24 08                            |
    | shl byte [r9 + 1 * rcx], 0x01                                     | 41 d0 24 09                            |
    | shl byte [r10 + 1 * rcx], 0x01                                    | 41 d0 24 0a                            |
    | shl byte [r11 + 1 * rcx], 0x01                                    | 41 d0 24 0b                            |
    | shl byte [r12 + 1 * rcx], 0x01                                    | 41 d0 24 0c                            |
    | shl byte [r13 + 1 * rcx], 0x01                                    | 41 d0 64 0d 00                         |
    | shl byte [r14 + 1 * rcx], 0x01                                    | 41 d0 24 0e                            |
    | shl byte [r15 + 1 * rcx], 0x01                                    | 41 d0 24 0f                            |
    | shl byte [rax + 1 * rax], 0x01                                    | d0 24 00                               |
    | shl byte [rax + 1 * rdx], 0x01                                    | d0 24 10                               |
    | shl byte [rax + 1 * rbx], 0x01                                    | d0 24 18                               |
    | shl byte [rax + 1 * rbp], 0x01                                    | d0 24 28                               |
    | shl byte [rax + 1 * rsi], 0x01                                    | d0 24 30                               |
    | shl byte [rax + 1 * rdi], 0x01                                    | d0 24 38                               |
    | shl byte [rax + 1 * r8], 0x01                                     | 42 d0 24 00                            |
    | shl byte [rax + 1 * r9], 0x01                                     | 42 d0 24 08                            |
    | shl byte [rax + 1 * r10], 0x01                                    | 42 d0 24 10                            |
    | shl byte [rax + 1 * r11], 0x01                                    | 42 d0 24 18                            |
    | shl byte [rax + 1 * r12], 0x01                                    | 42 d0 24 20                            |
    | shl byte [rax + 1 * r13], 0x01                                    | 42 d0 24 28                            |
    | shl byte [rax + 1 * r14], 0x01                                    | 42 d0 24 30                            |
    | shl byte [rax + 1 * r15], 0x01                                    | 42 d0 24 38                            |
    | shl byte [rax + 2 * rcx], 0x01                                    | d0 24 48                               |
    | shl byte [rax + 4 * rcx], 0x01                                    | d0 24 88                               |
    | shl byte [rax + 8 * rcx], 0x01                                    | d0 24 c8                               |
    | shl byte [r8 + 1 * r9], 0x01                                      | 43 d0 24 08                            |
    | shl byte [r8 + 2 * r9], 0x01                                      | 43 d0 24 48                            |
    | shl byte [r8 + 4 * r9], 0x01                                      | 43 d0 24 88                            |
    | shl byte [r8 + 8 * r9], 0x01                                      | 43 d0 24 c8                            |
    | shl byte [1 * rcx], 0x01                                          | d0 24 0d 00 00 00 00                   |
    | shl byte [2 * rcx], 0x01                                          | d0 24 4d 00 00 00 00                   |
    | shl byte [4 * rcx], 0x01                                          | d0 24 8d 00 00 00 00                   |
    | shl byte [8 * rcx], 0x01                                          | d0 24 cd 00 00 00 00                   |
    | shl byte [1 * r9], 0x01                                           | 42 d0 24 0d 00 00 00 00                |
    | shl byte [2 * r9], 0x01                                           | 42 d0 24 4d 00 00 00 00                |
    | shl byte [4 * r9], 0x01                                           | 42 d0 24 8d 00 00 00 00                |
    | shl byte [8 * r9], 0x01                                           | 42 d0 24 cd 00 00 00 00                |
    | shl byte [r13 + 8 * r12], 0x01                                    | 43 d0 64 e5 00                         |
    | shl byte [rsp + 4 * r15], 0x01                                    | 42 d0 24 bc                            |
    | shl byte [rax + 1 * rcx + 0x00], 0x01                             | d0 64 08 00                            |
    | shl byte [rax + 1 * rcx - 0x00], 0x01                             | d0 64 08 00                            |
    | shl byte [rax + 1 * rcx + 0x01], 0x01                             | d0 64 08 01                            |
    | shl byte [rax + 1 * rcx - 0x01], 0x01                             | d0 64 08 ff                            |
    | shl byte [rax + 1 * rcx + 0x00000001], 0x01                       | d0 a4 08 01 00 00 00                   |
    | shl byte [rax + 1 * rcx - 0x00000001], 0x01                       | d0 a4 08 ff ff ff ff                   |
    | shl byte [rax + 1 * rcx + 0x7f], 0x01                             | d0 64 08 7f                            |
    | shl byte [rax + 1 * rcx - 0x7f], 0x01                             | d0 64 08 81                            |
    | shl byte [rax + 1 * rcx + 0x80], 0x01                             | d0 a4 08 80 00 00 00                   |
    | shl byte [rax + 1 * rcx - 0x80], 0x01                             | d0 64 08 80                            |
    | shl byte [rax + 1 * rcx - 0x81], 0x01                             | d0 a4 08 7f ff ff ff                   |
    | shl byte [rax + 1 * rcx + 0xff], 0x01                             | d0 a4 08 ff 00 00 00                   |
    | shl byte [rax + 1 * rcx - 0xff], 0x01                             | d0 a4 08 01 ff ff ff                   |
    | shl byte [rax + 1 * rcx + 0x7fffffff], 0x01                       | d0 a4 08 ff ff ff 7f                   |
    | shl byte [rax + 1 * rcx - 0x7fffffff], 0x01                       | d0 a4 08 01 00 00 80                   |
    | shl byte [rax + 1 * rcx - 0x80000000], 0x01                       | d0 a4 08 00 00 00 80                   |
    | shl byte [r10 + 0x7f], 0x01                                       | 41 d0 62 7f                            |
    | shl byte [r10 + 0x80], 0x01                                       | 41 d0 a2 80 00 00 00                   |
    | shl byte [r10 - 0x80], 0x01                                       | 41 d0 62 80                            |
    | shl byte [r10 - 0x81], 0x01                                       | 41 d0 a2 7f ff ff ff                   |
    | .prev5: nop; nop; nop; nop; nop; shl byte [rel @prev5], 0x01      | 90 90 90 90 90 d0 25 f5 ff ff ff       |
    | .prev1: nop; shl byte [rel @prev1], 0x01                          | 90 d0 25 f9 ff ff ff                   |
    | shl byte [rel @next1], 0x01; nop; .next1: nop                     | d0 25 01 00 00 00 90 90                |
    | shl byte [rel @next5], 0x01; nop; nop; nop; nop; nop; .next5: nop | d0 25 05 00 00 00 90 90 90 90 90 90    |
    | shl byte [rax], 0x00                                              | c0 20 00                               |
    | shl byte [rax], 0x7f                                              | c0 20 7f                               |
    | shl byte [rax], 0x80                                              | c0 20 80                               |
    | shl byte [rax], 0xff                                              | c0 20 ff                               |
    | shl byte [rcx], 0x7f                                              | c0 21 7f                               |
    | shl byte [rdx], 0x80                                              | c0 22 80                               |
    | shl byte [rbx], 0xff                                              | c0 23 ff                               |
    | shl byte [rsp], 0x00                                              | c0 24 24 00                            |
    | shl byte [rsi], 0x7f                                              | c0 26 7f                               |
    | shl byte [rdi], 0x80                                              | c0 27 80                               |
    | shl byte [r8], 0xff                                               | 41 c0 20 ff                            |
    | shl byte [r9], 0x00                                               | 41 c0 21 00                            |
    | shl byte [r11], 0x7f                                              | 41 c0 23 7f                            |
    | shl byte [r12], 0x80                                              | 41 c0 24 24 80                         |
    | shl byte [r13], 0xff                                              | 41 c0 65 00 ff                         |
    | shl byte [r14], 0x00                                              | 41 c0 26 00                            |
    | shl byte [rax + 1 * rcx], 0x7f                                    | c0 24 08 7f                            |
    | shl byte [rcx + 1 * rcx], 0x80                                    | c0 24 09 80                            |
    | shl byte [rdx + 1 * rcx], 0xff                                    | c0 24 0a ff                            |
    | shl byte [rbx + 1 * rcx], 0x00                                    | c0 24 0b 00                            |
    | shl byte [rbp + 1 * rcx], 0x7f                                    | c0 64 0d 00 7f                         |
    | shl byte [rsi + 1 * rcx], 0x80                                    | c0 24 0e 80                            |
    | shl byte [rdi + 1 * rcx], 0xff                                    | c0 24 0f ff                            |
    | shl byte [r8 + 1 * rcx], 0x00                                     | 41 c0 24 08 00                         |
    | shl byte [r10 + 1 * rcx], 0x7f                                    | 41 c0 24 0a 7f                         |
    | shl byte [r11 + 1 * rcx], 0x80                                    | 41 c0 24 0b 80                         |
    | shl byte [r12 + 1 * rcx], 0xff                                    | 41 c0 24 0c ff                         |
    | shl byte [r13 + 1 * rcx], 0x00                                    | 41 c0 64 0d 00 00                      |
    | shl byte [r15 + 1 * rcx], 0x7f                                    | 41 c0 24 0f 7f                         |
    | shl byte [rax + 1 * rax], 0x80                                    | c0 24 00 80                            |
    | shl byte [rax + 1 * rdx], 0xff                                    | c0 24 10 ff                            |
    | shl byte [rax + 1 * rbx], 0x00                                    | c0 24 18 00                            |
    | shl byte [rax + 1 * rsi], 0x7f                                    | c0 24 30 7f                            |
    | shl byte [rax + 1 * rdi], 0x80                                    | c0 24 38 80                            |
    | shl byte [rax + 1 * r8], 0xff                                     | 42 c0 24 00 ff                         |
    | shl byte [rax + 1 * r9], 0x00                                     | 42 c0 24 08 00                         |
    | shl byte [rax + 1 * r11], 0x7f                                    | 42 c0 24 18 7f                         |
    | shl byte [rax + 1 * r12], 0x80                                    | 42 c0 24 20 80                         |
    | shl byte [rax + 1 * r13], 0xff                                    | 42 c0 24 28 ff                         |
    | shl byte [rax + 1 * r14], 0x00                                    | 42 c0 24 30 00                         |
    | shl byte [rax + 2 * rcx], 0x7f                                    | c0 24 48 7f                            |
    | shl byte [rax + 4 * rcx], 0x80                                    | c0 24 88 80                            |
    | shl byte [rax + 8 * rcx], 0xff                                    | c0 24 c8 ff                            |
    | shl byte [r8 + 1 * r9], 0x00                                      | 43 c0 24 08 00                         |
    | shl byte [r8 + 4 * r9], 0x7f                                      | 43 c0 24 88 7f                         |
    | shl byte [r8 + 8 * r9], 0x80                                      | 43 c0 24 c8 80                         |
    | shl byte [1 * rcx], 0xff                                          | c0 24 0d 00 00 00 00 ff                |
    | shl byte [2 * rcx], 0x00                                          | c0 24 4d 00 00 00 00 00                |
    | shl byte [8 * rcx], 0x7f                                          | c0 24 cd 00 00 00 00 7f                |
    | shl byte [1 * r9], 0x80                                           | 42 c0 24 0d 00 00 00 00 80             |
    | shl byte [2 * r9], 0xff                                           | 42 c0 24 4d 00 00 00 00 ff             |
    | shl byte [4 * r9], 0x00                                           | 42 c0 24 8d 00 00 00 00 00             |
    | shl byte [r13 + 8 * r12], 0x7f                                    | 43 c0 64 e5 00 7f                      |
    | shl byte [rsp + 4 * r15], 0x80                                    | 42 c0 24 bc 80                         |
    | shl byte [rax + 1 * rcx + 0x00], 0xff                             | c0 64 08 00 ff                         |
    | shl byte [rax + 1 * rcx - 0x00], 0x00                             | c0 64 08 00 00                         |
    | shl byte [rax + 1 * rcx - 0x01], 0x7f                             | c0 64 08 ff 7f                         |
    | shl byte [rax + 1 * rcx + 0x00000001], 0x80                       | c0 a4 08 01 00 00 00 80                |
    | shl byte [rax + 1 * rcx - 0x00000001], 0xff                       | c0 a4 08 ff ff ff ff ff                |
    | shl byte [rax + 1 * rcx + 0x7f], 0x00                             | c0 64 08 7f 00                         |
    | shl byte [rax + 1 * rcx + 0x80], 0x7f                             | c0 a4 08 80 00 00 00 7f                |
    | shl byte [rax + 1 * rcx - 0x80], 0x80                             | c0 64 08 80 80                         |
    | shl byte [rax + 1 * rcx - 0x81], 0xff                             | c0 a4 08 7f ff ff ff ff                |
    | shl byte [rax + 1 * rcx + 0xff], 0x00                             | c0 a4 08 ff 00 00 00 00                |
    | shl byte [rax + 1 * rcx + 0x7fffffff], 0x7f                       | c0 a4 08 ff ff ff 7f 7f                |
    | shl byte [rax + 1 * rcx - 0x7fffffff], 0x80                       | c0 a4 08 01 00 00 80 80                |
    | shl byte [rax + 1 * rcx - 0x80000000], 0xff                       | c0 a4 08 00 00 00 80 ff                |
    | shl byte [r10 + 0x7f], 0x00                                       | 41 c0 62 7f 00                         |
    | shl byte [r10 - 0x80], 0x7f                                       | 41 c0 62 80 7f                         |
    | shl byte [r10 - 0x81], 0x80                                       | 41 c0 a2 7f ff ff ff 80                |
    | .prev5: nop; nop; nop; nop; nop; shl byte [rel @prev5], 0xff      | 90 90 90 90 90 c0 25 f4 ff ff ff ff    |
    | .prev1: nop; shl byte [rel @prev1], 0x00                          | 90 c0 25 f8 ff ff ff 00                |
    | shl byte [rel @next5], 0x7f; nop; nop; nop; nop; nop; .next5: nop | c0 25 05 00 00 00 7f 90 90 90 90 90 90 |
    | ----------------------------------------------------------------- | -------------------------------------- |
"""


def can_encode_shl_addr8_imm8():
    encode(SHL_ADDR8_IMM8)


SHL_ADDR8_CL = """
    | --------------------------------------------------------------- | ----------------------------------- |
    | instruction                                                     | encoding                            |
    | --------------------------------------------------------------- | ----------------------------------- |
    | shl byte [rax], cl                                              | d2 20                               |
    | shl byte [rcx], cl                                              | d2 21                               |
    | shl byte [rdx], cl                                              | d2 22                               |
    | shl byte [rbx], cl                                              | d2 23                               |
    | shl byte [rsp], cl                                              | d2 24 24                            |
    | shl byte [rbp], cl                                              | d2 65 00                            |
    | shl byte [rsi], cl                                              | d2 26                               |
    | shl byte [rdi], cl                                              | d2 27                               |
    | shl byte [r8], cl                                               | 41 d2 20                            |
    | shl byte [r9], cl                                               | 41 d2 21                            |
    | shl byte [r10], cl                                              | 41 d2 22                            |
    | shl byte [r11], cl                                              | 41 d2 23                            |
    | shl byte [r12], cl                                              | 41 d2 24 24                         |
    | shl byte [r13], cl                                              | 41 d2 65 00                         |
    | shl byte [r14], cl                                              | 41 d2 26                            |
    | shl byte [r15], cl                                              | 41 d2 27                            |
    | shl byte [rax + 1 * rcx], cl                                    | d2 24 08                            |
    | shl byte [rcx + 1 * rcx], cl                                    | d2 24 09                            |
    | shl byte [rdx + 1 * rcx], cl                                    | d2 24 0a                            |
    | shl byte [rbx + 1 * rcx], cl                                    | d2 24 0b                            |
    | shl byte [rsp + 1 * rcx], cl                                    | d2 24 0c                            |
    | shl byte [rbp + 1 * rcx], cl                                    | d2 64 0d 00                         |
    | shl byte [rsi + 1 * rcx], cl                                    | d2 24 0e                            |
    | shl byte [rdi + 1 * rcx], cl                                    | d2 24 0f                            |
    | shl byte [r8 + 1 * rcx], cl                                     | 41 d2 24 08                         |
    | shl byte [r9 + 1 * rcx], cl                                     | 41 d2 24 09                         |
    | shl byte [r10 + 1 * rcx], cl                                    | 41 d2 24 0a                         |
    | shl byte [r11 + 1 * rcx], cl                                    | 41 d2 24 0b                         |
    | shl byte [r12 + 1 * rcx], cl                                    | 41 d2 24 0c                         |
    | shl byte [r13 + 1 * rcx], cl                                    | 41 d2 64 0d 00                      |
    | shl byte [r14 + 1 * rcx], cl                                    | 41 d2 24 0e                         |
    | shl byte [r15 + 1 * rcx], cl                                    | 41 d2 24 0f                         |
    | shl byte [rax + 1 * rax], cl                                    | d2 24 00                            |
    | shl byte [rax + 1 * rdx], cl                                    | d2 24 10                            |
    | shl byte [rax + 1 * rbx], cl                                    | d2 24 18                            |
    | shl byte [rax + 1 * rbp], cl                                    | d2 24 28                            |
    | shl byte [rax + 1 * rsi], cl                                    | d2 24 30                            |
    | shl byte [rax + 1 * rdi], cl                                    | d2 24 38                            |
    | shl byte [rax + 1 * r8], cl                                     | 42 d2 24 00                         |
    | shl byte [rax + 1 * r9], cl                                     | 42 d2 24 08                         |
    | shl byte [rax + 1 * r10], cl                                    | 42 d2 24 10                         |
    | shl byte [rax + 1 * r11], cl                                    | 42 d2 24 18                         |
    | shl byte [rax + 1 * r12], cl                                    | 42 d2 24 20                         |
    | shl byte [rax + 1 * r13], cl                                    | 42 d2 24 28                         |
    | shl byte [rax + 1 * r14], cl                                    | 42 d2 24 30                         |
    | shl byte [rax + 1 * r15], cl                                    | 42 d2 24 38                         |
    | shl byte [rax + 2 * rcx], cl                                    | d2 24 48                            |
    | shl byte [rax + 4 * rcx], cl                                    | d2 24 88                            |
    | shl byte [rax + 8 * rcx], cl                                    | d2 24 c8                            |
    | shl byte [r8 + 1 * r9], cl                                      | 43 d2 24 08                         |
    | shl byte [r8 + 2 * r9], cl                                      | 43 d2 24 48                         |
    | shl byte [r8 + 4 * r9], cl                                      | 43 d2 24 88                         |
    | shl byte [r8 + 8 * r9], cl                                      | 43 d2 24 c8                         |
    | shl byte [1 * rcx], cl                                          | d2 24 0d 00 00 00 00                |
    | shl byte [2 * rcx], cl                                          | d2 24 4d 00 00 00 00                |
    | shl byte [4 * rcx], cl                                          | d2 24 8d 00 00 00 00                |
    | shl byte [8 * rcx], cl                                          | d2 24 cd 00 00 00 00                |
    | shl byte [1 * r9], cl                                           | 42 d2 24 0d 00 00 00 00             |
    | shl byte [2 * r9], cl                                           | 42 d2 24 4d 00 00 00 00             |
    | shl byte [4 * r9], cl                                           | 42 d2 24 8d 00 00 00 00             |
    | shl byte [8 * r9], cl                                           | 42 d2 24 cd 00 00 00 00             |
    | shl byte [r13 + 8 * r12], cl                                    | 43 d2 64 e5 00                      |
    | shl byte [rsp + 4 * r15], cl                                    | 42 d2 24 bc                         |
    | shl byte [rax + 1 * rcx + 0x00], cl                             | d2 64 08 00                         |
    | shl byte [rax + 1 * rcx - 0x00], cl                             | d2 64 08 00                         |
    | shl byte [rax + 1 * rcx + 0x01], cl                             | d2 64 08 01                         |
    | shl byte [rax + 1 * rcx - 0x01], cl                             | d2 64 08 ff                         |
    | shl byte [rax + 1 * rcx + 0x00000001], cl                       | d2 a4 08 01 00 00 00                |
    | shl byte [rax + 1 * rcx - 0x00000001], cl                       | d2 a4 08 ff ff ff ff                |
    | shl byte [rax + 1 * rcx + 0x7f], cl                             | d2 64 08 7f                         |
    | shl byte [rax + 1 * rcx - 0x7f], cl                             | d2 64 08 81                         |
    | shl byte [rax + 1 * rcx + 0x80], cl                             | d2 a4 08 80 00 00 00                |
    | shl byte [rax + 1 * rcx - 0x80], cl                             | d2 64 08 80                         |
    | shl byte [rax + 1 * rcx - 0x81], cl                             | d2 a4 08 7f ff ff ff                |
    | shl byte [rax + 1 * rcx + 0xff], cl                             | d2 a4 08 ff 00 00 00                |
    | shl byte [rax + 1 * rcx - 0xff], cl                             | d2 a4 08 01 ff ff ff                |
    | shl byte [rax + 1 * rcx + 0x7fffffff], cl                       | d2 a4 08 ff ff ff 7f                |
    | shl byte [rax + 1 * rcx - 0x7fffffff], cl                       | d2 a4 08 01 00 00 80                |
    | shl byte [rax + 1 * rcx - 0x80000000], cl                       | d2 a4 08 00 00 00 80                |
    | shl byte [r10 + 0x7f], cl                                       | 41 d2 62 7f                         |
    | shl byte [r10 + 0x80], cl                                       | 41 d2 a2 80 00 00 00                |
    | shl byte [r10 - 0x80], cl                                       | 41 d2 62 80                         |
    | shl byte [r10 - 0x81], cl                                       | 41 d2 a2 7f ff ff ff                |
    | .prev5: nop; nop; nop; nop; nop; shl byte [rel @prev5], cl      | 90 90 90 90 90 d2 25 f5 ff ff ff    |
    | .prev1: nop; shl byte [rel @prev1], cl                          | 90 d2 25 f9 ff ff ff                |
    | shl byte [rel @next1], cl; nop; .next1: nop                     | d2 25 01 00 00 00 90 90             |
    | shl byte [rel @next5], cl; nop; nop; nop; nop; nop; .next5: nop | d2 25 05 00 00 00 90 90 90 90 90 90 |
    | --------------------------------------------------------------- | ----------------------------------- |
"""


def can_encode_shl_addr8_cl():
    encode(SHL_ADDR8_CL)
