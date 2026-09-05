from tests.encoding.core import encode, exhaust


def can_exhaust_rol():
    exhaust(
        ROL_ADDR16_CL,
        ROL_ADDR16_IMM8,
        ROL_ADDR32_CL,
        ROL_ADDR32_IMM8,
        ROL_ADDR64_CL,
        ROL_ADDR64_IMM8,
        ROL_ADDR8_CL,
        ROL_ADDR8_IMM8,
        ROL_REG16_CL,
        ROL_REG16_IMM8,
        ROL_REG32_CL,
        ROL_REG32_IMM8,
        ROL_REG64_CL,
        ROL_REG64_IMM8,
        ROL_REG8_CL,
        ROL_REG8_IMM8,
    )


ROL_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | rol rax, 0x01 | 48 d1 c0    | *** | rol rax, 0x00 | 48 c1 c0 00 |
    | rol rcx, 0x01 | 48 d1 c1    | *** | rol rax, 0x7f | 48 c1 c0 7f |
    | rol rdx, 0x01 | 48 d1 c2    | *** | rol rax, 0x80 | 48 c1 c0 80 |
    | rol rbx, 0x01 | 48 d1 c3    | *** | rol rax, 0xff | 48 c1 c0 ff |
    | rol rsp, 0x01 | 48 d1 c4    | *** | rol rcx, 0x7f | 48 c1 c1 7f |
    | rol rbp, 0x01 | 48 d1 c5    | *** | rol rdx, 0x80 | 48 c1 c2 80 |
    | rol rsi, 0x01 | 48 d1 c6    | *** | rol rbx, 0xff | 48 c1 c3 ff |
    | rol rdi, 0x01 | 48 d1 c7    | *** | rol rsp, 0x00 | 48 c1 c4 00 |
    | rol r8, 0x01  | 49 d1 c0    | *** | rol rsi, 0x7f | 48 c1 c6 7f |
    | rol r9, 0x01  | 49 d1 c1    | *** | rol rdi, 0x80 | 48 c1 c7 80 |
    | rol r10, 0x01 | 49 d1 c2    | *** | rol r8, 0xff  | 49 c1 c0 ff |
    | rol r11, 0x01 | 49 d1 c3    | *** | rol r9, 0x00  | 49 c1 c1 00 |
    | rol r12, 0x01 | 49 d1 c4    | *** | rol r11, 0x7f | 49 c1 c3 7f |
    | rol r13, 0x01 | 49 d1 c5    | *** | rol r12, 0x80 | 49 c1 c4 80 |
    | rol r14, 0x01 | 49 d1 c6    | *** | rol r13, 0xff | 49 c1 c5 ff |
    | rol r15, 0x01 | 49 d1 c7    | *** | rol r14, 0x00 | 49 c1 c6 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_rol_reg64_imm8():
    encode(ROL_REG64_IMM8)


ROL_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | rol rax, cl | 48 d3 c0 | *** | rol r8, cl  | 49 d3 c0 |
    | rol rcx, cl | 48 d3 c1 | *** | rol r9, cl  | 49 d3 c1 |
    | rol rdx, cl | 48 d3 c2 | *** | rol r10, cl | 49 d3 c2 |
    | rol rbx, cl | 48 d3 c3 | *** | rol r11, cl | 49 d3 c3 |
    | rol rsp, cl | 48 d3 c4 | *** | rol r12, cl | 49 d3 c4 |
    | rol rbp, cl | 48 d3 c5 | *** | rol r13, cl | 49 d3 c5 |
    | rol rsi, cl | 48 d3 c6 | *** | rol r14, cl | 49 d3 c6 |
    | rol rdi, cl | 48 d3 c7 | *** | rol r15, cl | 49 d3 c7 |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_rol_reg64_cl():
    encode(ROL_REG64_CL)


ROL_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | rol eax, 0x01  | d1 c0       | *** | rol eax, 0x00  | c1 c0 00    |
    | rol ecx, 0x01  | d1 c1       | *** | rol eax, 0x7f  | c1 c0 7f    |
    | rol edx, 0x01  | d1 c2       | *** | rol eax, 0x80  | c1 c0 80    |
    | rol ebx, 0x01  | d1 c3       | *** | rol eax, 0xff  | c1 c0 ff    |
    | rol esp, 0x01  | d1 c4       | *** | rol ecx, 0x7f  | c1 c1 7f    |
    | rol ebp, 0x01  | d1 c5       | *** | rol edx, 0x80  | c1 c2 80    |
    | rol esi, 0x01  | d1 c6       | *** | rol ebx, 0xff  | c1 c3 ff    |
    | rol edi, 0x01  | d1 c7       | *** | rol esp, 0x00  | c1 c4 00    |
    | rol r8d, 0x01  | 41 d1 c0    | *** | rol esi, 0x7f  | c1 c6 7f    |
    | rol r9d, 0x01  | 41 d1 c1    | *** | rol edi, 0x80  | c1 c7 80    |
    | rol r10d, 0x01 | 41 d1 c2    | *** | rol r8d, 0xff  | 41 c1 c0 ff |
    | rol r11d, 0x01 | 41 d1 c3    | *** | rol r9d, 0x00  | 41 c1 c1 00 |
    | rol r12d, 0x01 | 41 d1 c4    | *** | rol r11d, 0x7f | 41 c1 c3 7f |
    | rol r13d, 0x01 | 41 d1 c5    | *** | rol r12d, 0x80 | 41 c1 c4 80 |
    | rol r14d, 0x01 | 41 d1 c6    | *** | rol r13d, 0xff | 41 c1 c5 ff |
    | rol r15d, 0x01 | 41 d1 c7    | *** | rol r14d, 0x00 | 41 c1 c6 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_rol_reg32_imm8():
    encode(ROL_REG32_IMM8)


ROL_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | rol eax, cl  | d3 c0    | *** | rol r8d, cl  | 41 d3 c0 |
    | rol ecx, cl  | d3 c1    | *** | rol r9d, cl  | 41 d3 c1 |
    | rol edx, cl  | d3 c2    | *** | rol r10d, cl | 41 d3 c2 |
    | rol ebx, cl  | d3 c3    | *** | rol r11d, cl | 41 d3 c3 |
    | rol esp, cl  | d3 c4    | *** | rol r12d, cl | 41 d3 c4 |
    | rol ebp, cl  | d3 c5    | *** | rol r13d, cl | 41 d3 c5 |
    | rol esi, cl  | d3 c6    | *** | rol r14d, cl | 41 d3 c6 |
    | rol edi, cl  | d3 c7    | *** | rol r15d, cl | 41 d3 c7 |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_rol_reg32_cl():
    encode(ROL_REG32_CL)


ROL_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | rol ax, 0x01   | 66 d1 c0       | *** | rol ax, 0x00   | 66 c1 c0 00    |
    | rol cx, 0x01   | 66 d1 c1       | *** | rol ax, 0x7f   | 66 c1 c0 7f    |
    | rol dx, 0x01   | 66 d1 c2       | *** | rol ax, 0x80   | 66 c1 c0 80    |
    | rol bx, 0x01   | 66 d1 c3       | *** | rol ax, 0xff   | 66 c1 c0 ff    |
    | rol sp, 0x01   | 66 d1 c4       | *** | rol cx, 0x7f   | 66 c1 c1 7f    |
    | rol bp, 0x01   | 66 d1 c5       | *** | rol dx, 0x80   | 66 c1 c2 80    |
    | rol si, 0x01   | 66 d1 c6       | *** | rol bx, 0xff   | 66 c1 c3 ff    |
    | rol di, 0x01   | 66 d1 c7       | *** | rol sp, 0x00   | 66 c1 c4 00    |
    | rol r8w, 0x01  | 66 41 d1 c0    | *** | rol si, 0x7f   | 66 c1 c6 7f    |
    | rol r9w, 0x01  | 66 41 d1 c1    | *** | rol di, 0x80   | 66 c1 c7 80    |
    | rol r10w, 0x01 | 66 41 d1 c2    | *** | rol r8w, 0xff  | 66 41 c1 c0 ff |
    | rol r11w, 0x01 | 66 41 d1 c3    | *** | rol r9w, 0x00  | 66 41 c1 c1 00 |
    | rol r12w, 0x01 | 66 41 d1 c4    | *** | rol r11w, 0x7f | 66 41 c1 c3 7f |
    | rol r13w, 0x01 | 66 41 d1 c5    | *** | rol r12w, 0x80 | 66 41 c1 c4 80 |
    | rol r14w, 0x01 | 66 41 d1 c6    | *** | rol r13w, 0xff | 66 41 c1 c5 ff |
    | rol r15w, 0x01 | 66 41 d1 c7    | *** | rol r14w, 0x00 | 66 41 c1 c6 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_rol_reg16_imm8():
    encode(ROL_REG16_IMM8)


ROL_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | rol ax, cl   | 66 d3 c0    | *** | rol r8w, cl  | 66 41 d3 c0 |
    | rol cx, cl   | 66 d3 c1    | *** | rol r9w, cl  | 66 41 d3 c1 |
    | rol dx, cl   | 66 d3 c2    | *** | rol r10w, cl | 66 41 d3 c2 |
    | rol bx, cl   | 66 d3 c3    | *** | rol r11w, cl | 66 41 d3 c3 |
    | rol sp, cl   | 66 d3 c4    | *** | rol r12w, cl | 66 41 d3 c4 |
    | rol bp, cl   | 66 d3 c5    | *** | rol r13w, cl | 66 41 d3 c5 |
    | rol si, cl   | 66 d3 c6    | *** | rol r14w, cl | 66 41 d3 c6 |
    | rol di, cl   | 66 d3 c7    | *** | rol r15w, cl | 66 41 d3 c7 |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_rol_reg16_cl():
    encode(ROL_REG16_CL)


ROL_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | rol al, 0x01   | d0 c0       | *** | rol al, 0x00   | c0 c0 00    |
    | rol cl, 0x01   | d0 c1       | *** | rol al, 0x7f   | c0 c0 7f    |
    | rol dl, 0x01   | d0 c2       | *** | rol al, 0x80   | c0 c0 80    |
    | rol bl, 0x01   | d0 c3       | *** | rol al, 0xff   | c0 c0 ff    |
    | rol spl, 0x01  | 40 d0 c4    | *** | rol cl, 0x7f   | c0 c1 7f    |
    | rol bpl, 0x01  | 40 d0 c5    | *** | rol dl, 0x80   | c0 c2 80    |
    | rol sil, 0x01  | 40 d0 c6    | *** | rol bl, 0xff   | c0 c3 ff    |
    | rol dil, 0x01  | 40 d0 c7    | *** | rol spl, 0x00  | 40 c0 c4 00 |
    | rol r8b, 0x01  | 41 d0 c0    | *** | rol sil, 0x7f  | 40 c0 c6 7f |
    | rol r9b, 0x01  | 41 d0 c1    | *** | rol dil, 0x80  | 40 c0 c7 80 |
    | rol r10b, 0x01 | 41 d0 c2    | *** | rol r8b, 0xff  | 41 c0 c0 ff |
    | rol r11b, 0x01 | 41 d0 c3    | *** | rol r9b, 0x00  | 41 c0 c1 00 |
    | rol r12b, 0x01 | 41 d0 c4    | *** | rol r11b, 0x7f | 41 c0 c3 7f |
    | rol r13b, 0x01 | 41 d0 c5    | *** | rol r12b, 0x80 | 41 c0 c4 80 |
    | rol r14b, 0x01 | 41 d0 c6    | *** | rol r13b, 0xff | 41 c0 c5 ff |
    | rol r15b, 0x01 | 41 d0 c7    | *** | rol r14b, 0x00 | 41 c0 c6 00 |
    | rol ah, 0x01   | d0 c4       | *** | rol ah, 0x7f   | c0 c4 7f    |
    | rol ch, 0x01   | d0 c5       | *** | rol ch, 0x80   | c0 c5 80    |
    | rol dh, 0x01   | d0 c6       | *** | rol dh, 0xff   | c0 c6 ff    |
    | rol bh, 0x01   | d0 c7       | *** | rol bh, 0x00   | c0 c7 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_rol_reg8_imm8():
    encode(ROL_REG8_IMM8)


ROL_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | rol al, cl   | d2 c0    | *** | rol r10b, cl | 41 d2 c2 |
    | rol cl, cl   | d2 c1    | *** | rol r11b, cl | 41 d2 c3 |
    | rol dl, cl   | d2 c2    | *** | rol r12b, cl | 41 d2 c4 |
    | rol bl, cl   | d2 c3    | *** | rol r13b, cl | 41 d2 c5 |
    | rol spl, cl  | 40 d2 c4 | *** | rol r14b, cl | 41 d2 c6 |
    | rol bpl, cl  | 40 d2 c5 | *** | rol r15b, cl | 41 d2 c7 |
    | rol sil, cl  | 40 d2 c6 | *** | rol ah, cl   | d2 c4    |
    | rol dil, cl  | 40 d2 c7 | *** | rol ch, cl   | d2 c5    |
    | rol r8b, cl  | 41 d2 c0 | *** | rol dh, cl   | d2 c6    |
    | rol r9b, cl  | 41 d2 c1 | *** | rol bh, cl   | d2 c7    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_rol_reg8_cl():
    encode(ROL_REG8_CL)


ROL_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | rol qword [rax], 0x01                        | 48 d1 00                   |
    | rol qword [rcx], 0x01                        | 48 d1 01                   |
    | rol qword [rdx], 0x01                        | 48 d1 02                   |
    | rol qword [rbx], 0x01                        | 48 d1 03                   |
    | rol qword [rsp], 0x01                        | 48 d1 04 24                |
    | rol qword [rbp], 0x01                        | 48 d1 45 00                |
    | rol qword [rsi], 0x01                        | 48 d1 06                   |
    | rol qword [rdi], 0x01                        | 48 d1 07                   |
    | rol qword [r8], 0x01                         | 49 d1 00                   |
    | rol qword [r9], 0x01                         | 49 d1 01                   |
    | rol qword [r10], 0x01                        | 49 d1 02                   |
    | rol qword [r11], 0x01                        | 49 d1 03                   |
    | rol qword [r12], 0x01                        | 49 d1 04 24                |
    | rol qword [r13], 0x01                        | 49 d1 45 00                |
    | rol qword [r14], 0x01                        | 49 d1 06                   |
    | rol qword [r15], 0x01                        | 49 d1 07                   |
    | rol qword [rax + 1 * rcx], 0x01              | 48 d1 04 08                |
    | rol qword [rcx + 1 * rcx], 0x01              | 48 d1 04 09                |
    | rol qword [rdx + 1 * rcx], 0x01              | 48 d1 04 0a                |
    | rol qword [rbx + 1 * rcx], 0x01              | 48 d1 04 0b                |
    | rol qword [rsp + 1 * rcx], 0x01              | 48 d1 04 0c                |
    | rol qword [rbp + 1 * rcx], 0x01              | 48 d1 44 0d 00             |
    | rol qword [rsi + 1 * rcx], 0x01              | 48 d1 04 0e                |
    | rol qword [rdi + 1 * rcx], 0x01              | 48 d1 04 0f                |
    | rol qword [r8 + 1 * rcx], 0x01               | 49 d1 04 08                |
    | rol qword [r9 + 1 * rcx], 0x01               | 49 d1 04 09                |
    | rol qword [r10 + 1 * rcx], 0x01              | 49 d1 04 0a                |
    | rol qword [r11 + 1 * rcx], 0x01              | 49 d1 04 0b                |
    | rol qword [r12 + 1 * rcx], 0x01              | 49 d1 04 0c                |
    | rol qword [r13 + 1 * rcx], 0x01              | 49 d1 44 0d 00             |
    | rol qword [r14 + 1 * rcx], 0x01              | 49 d1 04 0e                |
    | rol qword [r15 + 1 * rcx], 0x01              | 49 d1 04 0f                |
    | rol qword [rax + 1 * rax], 0x01              | 48 d1 04 00                |
    | rol qword [rax + 1 * rdx], 0x01              | 48 d1 04 10                |
    | rol qword [rax + 1 * rbx], 0x01              | 48 d1 04 18                |
    | rol qword [rax + 1 * rbp], 0x01              | 48 d1 04 28                |
    | rol qword [rax + 1 * rsi], 0x01              | 48 d1 04 30                |
    | rol qword [rax + 1 * rdi], 0x01              | 48 d1 04 38                |
    | rol qword [rax + 1 * r8], 0x01               | 4a d1 04 00                |
    | rol qword [rax + 1 * r9], 0x01               | 4a d1 04 08                |
    | rol qword [rax + 1 * r10], 0x01              | 4a d1 04 10                |
    | rol qword [rax + 1 * r11], 0x01              | 4a d1 04 18                |
    | rol qword [rax + 1 * r12], 0x01              | 4a d1 04 20                |
    | rol qword [rax + 1 * r13], 0x01              | 4a d1 04 28                |
    | rol qword [rax + 1 * r14], 0x01              | 4a d1 04 30                |
    | rol qword [rax + 1 * r15], 0x01              | 4a d1 04 38                |
    | rol qword [rax + 2 * rcx], 0x01              | 48 d1 04 48                |
    | rol qword [rax + 4 * rcx], 0x01              | 48 d1 04 88                |
    | rol qword [rax + 8 * rcx], 0x01              | 48 d1 04 c8                |
    | rol qword [r8 + 1 * r9], 0x01                | 4b d1 04 08                |
    | rol qword [r8 + 2 * r9], 0x01                | 4b d1 04 48                |
    | rol qword [r8 + 4 * r9], 0x01                | 4b d1 04 88                |
    | rol qword [r8 + 8 * r9], 0x01                | 4b d1 04 c8                |
    | rol qword [1 * rcx], 0x01                    | 48 d1 04 0d 00 00 00 00    |
    | rol qword [2 * rcx], 0x01                    | 48 d1 04 4d 00 00 00 00    |
    | rol qword [4 * rcx], 0x01                    | 48 d1 04 8d 00 00 00 00    |
    | rol qword [8 * rcx], 0x01                    | 48 d1 04 cd 00 00 00 00    |
    | rol qword [1 * r9], 0x01                     | 4a d1 04 0d 00 00 00 00    |
    | rol qword [2 * r9], 0x01                     | 4a d1 04 4d 00 00 00 00    |
    | rol qword [4 * r9], 0x01                     | 4a d1 04 8d 00 00 00 00    |
    | rol qword [8 * r9], 0x01                     | 4a d1 04 cd 00 00 00 00    |
    | rol qword [r13 + 8 * r12], 0x01              | 4b d1 44 e5 00             |
    | rol qword [rsp + 4 * r15], 0x01              | 4a d1 04 bc                |
    | rol qword [rax + 1 * rcx + 0x00], 0x01       | 48 d1 44 08 00             |
    | rol qword [rax + 1 * rcx - 0x00], 0x01       | 48 d1 44 08 00             |
    | rol qword [rax + 1 * rcx + 0x01], 0x01       | 48 d1 44 08 01             |
    | rol qword [rax + 1 * rcx - 0x01], 0x01       | 48 d1 44 08 ff             |
    | rol qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 d1 84 08 01 00 00 00    |
    | rol qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 d1 84 08 ff ff ff ff    |
    | rol qword [rax + 1 * rcx + 0x7f], 0x01       | 48 d1 44 08 7f             |
    | rol qword [rax + 1 * rcx - 0x7f], 0x01       | 48 d1 44 08 81             |
    | rol qword [rax + 1 * rcx + 0x80], 0x01       | 48 d1 84 08 80 00 00 00    |
    | rol qword [rax + 1 * rcx - 0x80], 0x01       | 48 d1 44 08 80             |
    | rol qword [rax + 1 * rcx - 0x81], 0x01       | 48 d1 84 08 7f ff ff ff    |
    | rol qword [rax + 1 * rcx + 0xff], 0x01       | 48 d1 84 08 ff 00 00 00    |
    | rol qword [rax + 1 * rcx - 0xff], 0x01       | 48 d1 84 08 01 ff ff ff    |
    | rol qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 d1 84 08 ff ff ff 7f    |
    | rol qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 d1 84 08 01 00 00 80    |
    | rol qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 d1 84 08 00 00 00 80    |
    | rol qword [r10 + 0x7f], 0x01                 | 49 d1 42 7f                |
    | rol qword [r10 + 0x80], 0x01                 | 49 d1 82 80 00 00 00       |
    | rol qword [r10 - 0x80], 0x01                 | 49 d1 42 80                |
    | rol qword [r10 - 0x81], 0x01                 | 49 d1 82 7f ff ff ff       |
    | rol qword [rax], 0x00                        | 48 c1 00 00                |
    | rol qword [rax], 0x7f                        | 48 c1 00 7f                |
    | rol qword [rax], 0x80                        | 48 c1 00 80                |
    | rol qword [rax], 0xff                        | 48 c1 00 ff                |
    | rol qword [rcx], 0x7f                        | 48 c1 01 7f                |
    | rol qword [rdx], 0x80                        | 48 c1 02 80                |
    | rol qword [rbx], 0xff                        | 48 c1 03 ff                |
    | rol qword [rsp], 0x00                        | 48 c1 04 24 00             |
    | rol qword [rsi], 0x7f                        | 48 c1 06 7f                |
    | rol qword [rdi], 0x80                        | 48 c1 07 80                |
    | rol qword [r8], 0xff                         | 49 c1 00 ff                |
    | rol qword [r9], 0x00                         | 49 c1 01 00                |
    | rol qword [r11], 0x7f                        | 49 c1 03 7f                |
    | rol qword [r12], 0x80                        | 49 c1 04 24 80             |
    | rol qword [r13], 0xff                        | 49 c1 45 00 ff             |
    | rol qword [r14], 0x00                        | 49 c1 06 00                |
    | rol qword [rax + 1 * rcx], 0x7f              | 48 c1 04 08 7f             |
    | rol qword [rcx + 1 * rcx], 0x80              | 48 c1 04 09 80             |
    | rol qword [rdx + 1 * rcx], 0xff              | 48 c1 04 0a ff             |
    | rol qword [rbx + 1 * rcx], 0x00              | 48 c1 04 0b 00             |
    | rol qword [rbp + 1 * rcx], 0x7f              | 48 c1 44 0d 00 7f          |
    | rol qword [rsi + 1 * rcx], 0x80              | 48 c1 04 0e 80             |
    | rol qword [rdi + 1 * rcx], 0xff              | 48 c1 04 0f ff             |
    | rol qword [r8 + 1 * rcx], 0x00               | 49 c1 04 08 00             |
    | rol qword [r10 + 1 * rcx], 0x7f              | 49 c1 04 0a 7f             |
    | rol qword [r11 + 1 * rcx], 0x80              | 49 c1 04 0b 80             |
    | rol qword [r12 + 1 * rcx], 0xff              | 49 c1 04 0c ff             |
    | rol qword [r13 + 1 * rcx], 0x00              | 49 c1 44 0d 00 00          |
    | rol qword [r15 + 1 * rcx], 0x7f              | 49 c1 04 0f 7f             |
    | rol qword [rax + 1 * rax], 0x80              | 48 c1 04 00 80             |
    | rol qword [rax + 1 * rdx], 0xff              | 48 c1 04 10 ff             |
    | rol qword [rax + 1 * rbx], 0x00              | 48 c1 04 18 00             |
    | rol qword [rax + 1 * rsi], 0x7f              | 48 c1 04 30 7f             |
    | rol qword [rax + 1 * rdi], 0x80              | 48 c1 04 38 80             |
    | rol qword [rax + 1 * r8], 0xff               | 4a c1 04 00 ff             |
    | rol qword [rax + 1 * r9], 0x00               | 4a c1 04 08 00             |
    | rol qword [rax + 1 * r11], 0x7f              | 4a c1 04 18 7f             |
    | rol qword [rax + 1 * r12], 0x80              | 4a c1 04 20 80             |
    | rol qword [rax + 1 * r13], 0xff              | 4a c1 04 28 ff             |
    | rol qword [rax + 1 * r14], 0x00              | 4a c1 04 30 00             |
    | rol qword [rax + 2 * rcx], 0x7f              | 48 c1 04 48 7f             |
    | rol qword [rax + 4 * rcx], 0x80              | 48 c1 04 88 80             |
    | rol qword [rax + 8 * rcx], 0xff              | 48 c1 04 c8 ff             |
    | rol qword [r8 + 1 * r9], 0x00                | 4b c1 04 08 00             |
    | rol qword [r8 + 4 * r9], 0x7f                | 4b c1 04 88 7f             |
    | rol qword [r8 + 8 * r9], 0x80                | 4b c1 04 c8 80             |
    | rol qword [1 * rcx], 0xff                    | 48 c1 04 0d 00 00 00 00 ff |
    | rol qword [2 * rcx], 0x00                    | 48 c1 04 4d 00 00 00 00 00 |
    | rol qword [8 * rcx], 0x7f                    | 48 c1 04 cd 00 00 00 00 7f |
    | rol qword [1 * r9], 0x80                     | 4a c1 04 0d 00 00 00 00 80 |
    | rol qword [2 * r9], 0xff                     | 4a c1 04 4d 00 00 00 00 ff |
    | rol qword [4 * r9], 0x00                     | 4a c1 04 8d 00 00 00 00 00 |
    | rol qword [r13 + 8 * r12], 0x7f              | 4b c1 44 e5 00 7f          |
    | rol qword [rsp + 4 * r15], 0x80              | 4a c1 04 bc 80             |
    | rol qword [rax + 1 * rcx + 0x00], 0xff       | 48 c1 44 08 00 ff          |
    | rol qword [rax + 1 * rcx - 0x00], 0x00       | 48 c1 44 08 00 00          |
    | rol qword [rax + 1 * rcx - 0x01], 0x7f       | 48 c1 44 08 ff 7f          |
    | rol qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 c1 84 08 01 00 00 00 80 |
    | rol qword [rax + 1 * rcx - 0x00000001], 0xff | 48 c1 84 08 ff ff ff ff ff |
    | rol qword [rax + 1 * rcx + 0x7f], 0x00       | 48 c1 44 08 7f 00          |
    | rol qword [rax + 1 * rcx + 0x80], 0x7f       | 48 c1 84 08 80 00 00 00 7f |
    | rol qword [rax + 1 * rcx - 0x80], 0x80       | 48 c1 44 08 80 80          |
    | rol qword [rax + 1 * rcx - 0x81], 0xff       | 48 c1 84 08 7f ff ff ff ff |
    | rol qword [rax + 1 * rcx + 0xff], 0x00       | 48 c1 84 08 ff 00 00 00 00 |
    | rol qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 c1 84 08 ff ff ff 7f 7f |
    | rol qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 c1 84 08 01 00 00 80 80 |
    | rol qword [rax + 1 * rcx - 0x80000000], 0xff | 48 c1 84 08 00 00 00 80 ff |
    | rol qword [r10 + 0x7f], 0x00                 | 49 c1 42 7f 00             |
    | rol qword [r10 - 0x80], 0x7f                 | 49 c1 42 80 7f             |
    | rol qword [r10 - 0x81], 0x80                 | 49 c1 82 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_rol_addr64_imm8():
    encode(ROL_ADDR64_IMM8)


ROL_ADDR64_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | rol qword [rax], cl                        | 48 d3 00                |
    | rol qword [rcx], cl                        | 48 d3 01                |
    | rol qword [rdx], cl                        | 48 d3 02                |
    | rol qword [rbx], cl                        | 48 d3 03                |
    | rol qword [rsp], cl                        | 48 d3 04 24             |
    | rol qword [rbp], cl                        | 48 d3 45 00             |
    | rol qword [rsi], cl                        | 48 d3 06                |
    | rol qword [rdi], cl                        | 48 d3 07                |
    | rol qword [r8], cl                         | 49 d3 00                |
    | rol qword [r9], cl                         | 49 d3 01                |
    | rol qword [r10], cl                        | 49 d3 02                |
    | rol qword [r11], cl                        | 49 d3 03                |
    | rol qword [r12], cl                        | 49 d3 04 24             |
    | rol qword [r13], cl                        | 49 d3 45 00             |
    | rol qword [r14], cl                        | 49 d3 06                |
    | rol qword [r15], cl                        | 49 d3 07                |
    | rol qword [rax + 1 * rcx], cl              | 48 d3 04 08             |
    | rol qword [rcx + 1 * rcx], cl              | 48 d3 04 09             |
    | rol qword [rdx + 1 * rcx], cl              | 48 d3 04 0a             |
    | rol qword [rbx + 1 * rcx], cl              | 48 d3 04 0b             |
    | rol qword [rsp + 1 * rcx], cl              | 48 d3 04 0c             |
    | rol qword [rbp + 1 * rcx], cl              | 48 d3 44 0d 00          |
    | rol qword [rsi + 1 * rcx], cl              | 48 d3 04 0e             |
    | rol qword [rdi + 1 * rcx], cl              | 48 d3 04 0f             |
    | rol qword [r8 + 1 * rcx], cl               | 49 d3 04 08             |
    | rol qword [r9 + 1 * rcx], cl               | 49 d3 04 09             |
    | rol qword [r10 + 1 * rcx], cl              | 49 d3 04 0a             |
    | rol qword [r11 + 1 * rcx], cl              | 49 d3 04 0b             |
    | rol qword [r12 + 1 * rcx], cl              | 49 d3 04 0c             |
    | rol qword [r13 + 1 * rcx], cl              | 49 d3 44 0d 00          |
    | rol qword [r14 + 1 * rcx], cl              | 49 d3 04 0e             |
    | rol qword [r15 + 1 * rcx], cl              | 49 d3 04 0f             |
    | rol qword [rax + 1 * rax], cl              | 48 d3 04 00             |
    | rol qword [rax + 1 * rdx], cl              | 48 d3 04 10             |
    | rol qword [rax + 1 * rbx], cl              | 48 d3 04 18             |
    | rol qword [rax + 1 * rbp], cl              | 48 d3 04 28             |
    | rol qword [rax + 1 * rsi], cl              | 48 d3 04 30             |
    | rol qword [rax + 1 * rdi], cl              | 48 d3 04 38             |
    | rol qword [rax + 1 * r8], cl               | 4a d3 04 00             |
    | rol qword [rax + 1 * r9], cl               | 4a d3 04 08             |
    | rol qword [rax + 1 * r10], cl              | 4a d3 04 10             |
    | rol qword [rax + 1 * r11], cl              | 4a d3 04 18             |
    | rol qword [rax + 1 * r12], cl              | 4a d3 04 20             |
    | rol qword [rax + 1 * r13], cl              | 4a d3 04 28             |
    | rol qword [rax + 1 * r14], cl              | 4a d3 04 30             |
    | rol qword [rax + 1 * r15], cl              | 4a d3 04 38             |
    | rol qword [rax + 2 * rcx], cl              | 48 d3 04 48             |
    | rol qword [rax + 4 * rcx], cl              | 48 d3 04 88             |
    | rol qword [rax + 8 * rcx], cl              | 48 d3 04 c8             |
    | rol qword [r8 + 1 * r9], cl                | 4b d3 04 08             |
    | rol qword [r8 + 2 * r9], cl                | 4b d3 04 48             |
    | rol qword [r8 + 4 * r9], cl                | 4b d3 04 88             |
    | rol qword [r8 + 8 * r9], cl                | 4b d3 04 c8             |
    | rol qword [1 * rcx], cl                    | 48 d3 04 0d 00 00 00 00 |
    | rol qword [2 * rcx], cl                    | 48 d3 04 4d 00 00 00 00 |
    | rol qword [4 * rcx], cl                    | 48 d3 04 8d 00 00 00 00 |
    | rol qword [8 * rcx], cl                    | 48 d3 04 cd 00 00 00 00 |
    | rol qword [1 * r9], cl                     | 4a d3 04 0d 00 00 00 00 |
    | rol qword [2 * r9], cl                     | 4a d3 04 4d 00 00 00 00 |
    | rol qword [4 * r9], cl                     | 4a d3 04 8d 00 00 00 00 |
    | rol qword [8 * r9], cl                     | 4a d3 04 cd 00 00 00 00 |
    | rol qword [r13 + 8 * r12], cl              | 4b d3 44 e5 00          |
    | rol qword [rsp + 4 * r15], cl              | 4a d3 04 bc             |
    | rol qword [rax + 1 * rcx + 0x00], cl       | 48 d3 44 08 00          |
    | rol qword [rax + 1 * rcx - 0x00], cl       | 48 d3 44 08 00          |
    | rol qword [rax + 1 * rcx + 0x01], cl       | 48 d3 44 08 01          |
    | rol qword [rax + 1 * rcx - 0x01], cl       | 48 d3 44 08 ff          |
    | rol qword [rax + 1 * rcx + 0x00000001], cl | 48 d3 84 08 01 00 00 00 |
    | rol qword [rax + 1 * rcx - 0x00000001], cl | 48 d3 84 08 ff ff ff ff |
    | rol qword [rax + 1 * rcx + 0x7f], cl       | 48 d3 44 08 7f          |
    | rol qword [rax + 1 * rcx - 0x7f], cl       | 48 d3 44 08 81          |
    | rol qword [rax + 1 * rcx + 0x80], cl       | 48 d3 84 08 80 00 00 00 |
    | rol qword [rax + 1 * rcx - 0x80], cl       | 48 d3 44 08 80          |
    | rol qword [rax + 1 * rcx - 0x81], cl       | 48 d3 84 08 7f ff ff ff |
    | rol qword [rax + 1 * rcx + 0xff], cl       | 48 d3 84 08 ff 00 00 00 |
    | rol qword [rax + 1 * rcx - 0xff], cl       | 48 d3 84 08 01 ff ff ff |
    | rol qword [rax + 1 * rcx + 0x7fffffff], cl | 48 d3 84 08 ff ff ff 7f |
    | rol qword [rax + 1 * rcx - 0x7fffffff], cl | 48 d3 84 08 01 00 00 80 |
    | rol qword [rax + 1 * rcx - 0x80000000], cl | 48 d3 84 08 00 00 00 80 |
    | rol qword [r10 + 0x7f], cl                 | 49 d3 42 7f             |
    | rol qword [r10 + 0x80], cl                 | 49 d3 82 80 00 00 00    |
    | rol qword [r10 - 0x80], cl                 | 49 d3 42 80             |
    | rol qword [r10 - 0x81], cl                 | 49 d3 82 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_rol_addr64_cl():
    encode(ROL_ADDR64_CL)


ROL_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | rol dword [rax], 0x01                        | d1 00                      |
    | rol dword [rcx], 0x01                        | d1 01                      |
    | rol dword [rdx], 0x01                        | d1 02                      |
    | rol dword [rbx], 0x01                        | d1 03                      |
    | rol dword [rsp], 0x01                        | d1 04 24                   |
    | rol dword [rbp], 0x01                        | d1 45 00                   |
    | rol dword [rsi], 0x01                        | d1 06                      |
    | rol dword [rdi], 0x01                        | d1 07                      |
    | rol dword [r8], 0x01                         | 41 d1 00                   |
    | rol dword [r9], 0x01                         | 41 d1 01                   |
    | rol dword [r10], 0x01                        | 41 d1 02                   |
    | rol dword [r11], 0x01                        | 41 d1 03                   |
    | rol dword [r12], 0x01                        | 41 d1 04 24                |
    | rol dword [r13], 0x01                        | 41 d1 45 00                |
    | rol dword [r14], 0x01                        | 41 d1 06                   |
    | rol dword [r15], 0x01                        | 41 d1 07                   |
    | rol dword [rax + 1 * rcx], 0x01              | d1 04 08                   |
    | rol dword [rcx + 1 * rcx], 0x01              | d1 04 09                   |
    | rol dword [rdx + 1 * rcx], 0x01              | d1 04 0a                   |
    | rol dword [rbx + 1 * rcx], 0x01              | d1 04 0b                   |
    | rol dword [rsp + 1 * rcx], 0x01              | d1 04 0c                   |
    | rol dword [rbp + 1 * rcx], 0x01              | d1 44 0d 00                |
    | rol dword [rsi + 1 * rcx], 0x01              | d1 04 0e                   |
    | rol dword [rdi + 1 * rcx], 0x01              | d1 04 0f                   |
    | rol dword [r8 + 1 * rcx], 0x01               | 41 d1 04 08                |
    | rol dword [r9 + 1 * rcx], 0x01               | 41 d1 04 09                |
    | rol dword [r10 + 1 * rcx], 0x01              | 41 d1 04 0a                |
    | rol dword [r11 + 1 * rcx], 0x01              | 41 d1 04 0b                |
    | rol dword [r12 + 1 * rcx], 0x01              | 41 d1 04 0c                |
    | rol dword [r13 + 1 * rcx], 0x01              | 41 d1 44 0d 00             |
    | rol dword [r14 + 1 * rcx], 0x01              | 41 d1 04 0e                |
    | rol dword [r15 + 1 * rcx], 0x01              | 41 d1 04 0f                |
    | rol dword [rax + 1 * rax], 0x01              | d1 04 00                   |
    | rol dword [rax + 1 * rdx], 0x01              | d1 04 10                   |
    | rol dword [rax + 1 * rbx], 0x01              | d1 04 18                   |
    | rol dword [rax + 1 * rbp], 0x01              | d1 04 28                   |
    | rol dword [rax + 1 * rsi], 0x01              | d1 04 30                   |
    | rol dword [rax + 1 * rdi], 0x01              | d1 04 38                   |
    | rol dword [rax + 1 * r8], 0x01               | 42 d1 04 00                |
    | rol dword [rax + 1 * r9], 0x01               | 42 d1 04 08                |
    | rol dword [rax + 1 * r10], 0x01              | 42 d1 04 10                |
    | rol dword [rax + 1 * r11], 0x01              | 42 d1 04 18                |
    | rol dword [rax + 1 * r12], 0x01              | 42 d1 04 20                |
    | rol dword [rax + 1 * r13], 0x01              | 42 d1 04 28                |
    | rol dword [rax + 1 * r14], 0x01              | 42 d1 04 30                |
    | rol dword [rax + 1 * r15], 0x01              | 42 d1 04 38                |
    | rol dword [rax + 2 * rcx], 0x01              | d1 04 48                   |
    | rol dword [rax + 4 * rcx], 0x01              | d1 04 88                   |
    | rol dword [rax + 8 * rcx], 0x01              | d1 04 c8                   |
    | rol dword [r8 + 1 * r9], 0x01                | 43 d1 04 08                |
    | rol dword [r8 + 2 * r9], 0x01                | 43 d1 04 48                |
    | rol dword [r8 + 4 * r9], 0x01                | 43 d1 04 88                |
    | rol dword [r8 + 8 * r9], 0x01                | 43 d1 04 c8                |
    | rol dword [1 * rcx], 0x01                    | d1 04 0d 00 00 00 00       |
    | rol dword [2 * rcx], 0x01                    | d1 04 4d 00 00 00 00       |
    | rol dword [4 * rcx], 0x01                    | d1 04 8d 00 00 00 00       |
    | rol dword [8 * rcx], 0x01                    | d1 04 cd 00 00 00 00       |
    | rol dword [1 * r9], 0x01                     | 42 d1 04 0d 00 00 00 00    |
    | rol dword [2 * r9], 0x01                     | 42 d1 04 4d 00 00 00 00    |
    | rol dword [4 * r9], 0x01                     | 42 d1 04 8d 00 00 00 00    |
    | rol dword [8 * r9], 0x01                     | 42 d1 04 cd 00 00 00 00    |
    | rol dword [r13 + 8 * r12], 0x01              | 43 d1 44 e5 00             |
    | rol dword [rsp + 4 * r15], 0x01              | 42 d1 04 bc                |
    | rol dword [rax + 1 * rcx + 0x00], 0x01       | d1 44 08 00                |
    | rol dword [rax + 1 * rcx - 0x00], 0x01       | d1 44 08 00                |
    | rol dword [rax + 1 * rcx + 0x01], 0x01       | d1 44 08 01                |
    | rol dword [rax + 1 * rcx - 0x01], 0x01       | d1 44 08 ff                |
    | rol dword [rax + 1 * rcx + 0x00000001], 0x01 | d1 84 08 01 00 00 00       |
    | rol dword [rax + 1 * rcx - 0x00000001], 0x01 | d1 84 08 ff ff ff ff       |
    | rol dword [rax + 1 * rcx + 0x7f], 0x01       | d1 44 08 7f                |
    | rol dword [rax + 1 * rcx - 0x7f], 0x01       | d1 44 08 81                |
    | rol dword [rax + 1 * rcx + 0x80], 0x01       | d1 84 08 80 00 00 00       |
    | rol dword [rax + 1 * rcx - 0x80], 0x01       | d1 44 08 80                |
    | rol dword [rax + 1 * rcx - 0x81], 0x01       | d1 84 08 7f ff ff ff       |
    | rol dword [rax + 1 * rcx + 0xff], 0x01       | d1 84 08 ff 00 00 00       |
    | rol dword [rax + 1 * rcx - 0xff], 0x01       | d1 84 08 01 ff ff ff       |
    | rol dword [rax + 1 * rcx + 0x7fffffff], 0x01 | d1 84 08 ff ff ff 7f       |
    | rol dword [rax + 1 * rcx - 0x7fffffff], 0x01 | d1 84 08 01 00 00 80       |
    | rol dword [rax + 1 * rcx - 0x80000000], 0x01 | d1 84 08 00 00 00 80       |
    | rol dword [r10 + 0x7f], 0x01                 | 41 d1 42 7f                |
    | rol dword [r10 + 0x80], 0x01                 | 41 d1 82 80 00 00 00       |
    | rol dword [r10 - 0x80], 0x01                 | 41 d1 42 80                |
    | rol dword [r10 - 0x81], 0x01                 | 41 d1 82 7f ff ff ff       |
    | rol dword [rax], 0x00                        | c1 00 00                   |
    | rol dword [rax], 0x7f                        | c1 00 7f                   |
    | rol dword [rax], 0x80                        | c1 00 80                   |
    | rol dword [rax], 0xff                        | c1 00 ff                   |
    | rol dword [rcx], 0x7f                        | c1 01 7f                   |
    | rol dword [rdx], 0x80                        | c1 02 80                   |
    | rol dword [rbx], 0xff                        | c1 03 ff                   |
    | rol dword [rsp], 0x00                        | c1 04 24 00                |
    | rol dword [rsi], 0x7f                        | c1 06 7f                   |
    | rol dword [rdi], 0x80                        | c1 07 80                   |
    | rol dword [r8], 0xff                         | 41 c1 00 ff                |
    | rol dword [r9], 0x00                         | 41 c1 01 00                |
    | rol dword [r11], 0x7f                        | 41 c1 03 7f                |
    | rol dword [r12], 0x80                        | 41 c1 04 24 80             |
    | rol dword [r13], 0xff                        | 41 c1 45 00 ff             |
    | rol dword [r14], 0x00                        | 41 c1 06 00                |
    | rol dword [rax + 1 * rcx], 0x7f              | c1 04 08 7f                |
    | rol dword [rcx + 1 * rcx], 0x80              | c1 04 09 80                |
    | rol dword [rdx + 1 * rcx], 0xff              | c1 04 0a ff                |
    | rol dword [rbx + 1 * rcx], 0x00              | c1 04 0b 00                |
    | rol dword [rbp + 1 * rcx], 0x7f              | c1 44 0d 00 7f             |
    | rol dword [rsi + 1 * rcx], 0x80              | c1 04 0e 80                |
    | rol dword [rdi + 1 * rcx], 0xff              | c1 04 0f ff                |
    | rol dword [r8 + 1 * rcx], 0x00               | 41 c1 04 08 00             |
    | rol dword [r10 + 1 * rcx], 0x7f              | 41 c1 04 0a 7f             |
    | rol dword [r11 + 1 * rcx], 0x80              | 41 c1 04 0b 80             |
    | rol dword [r12 + 1 * rcx], 0xff              | 41 c1 04 0c ff             |
    | rol dword [r13 + 1 * rcx], 0x00              | 41 c1 44 0d 00 00          |
    | rol dword [r15 + 1 * rcx], 0x7f              | 41 c1 04 0f 7f             |
    | rol dword [rax + 1 * rax], 0x80              | c1 04 00 80                |
    | rol dword [rax + 1 * rdx], 0xff              | c1 04 10 ff                |
    | rol dword [rax + 1 * rbx], 0x00              | c1 04 18 00                |
    | rol dword [rax + 1 * rsi], 0x7f              | c1 04 30 7f                |
    | rol dword [rax + 1 * rdi], 0x80              | c1 04 38 80                |
    | rol dword [rax + 1 * r8], 0xff               | 42 c1 04 00 ff             |
    | rol dword [rax + 1 * r9], 0x00               | 42 c1 04 08 00             |
    | rol dword [rax + 1 * r11], 0x7f              | 42 c1 04 18 7f             |
    | rol dword [rax + 1 * r12], 0x80              | 42 c1 04 20 80             |
    | rol dword [rax + 1 * r13], 0xff              | 42 c1 04 28 ff             |
    | rol dword [rax + 1 * r14], 0x00              | 42 c1 04 30 00             |
    | rol dword [rax + 2 * rcx], 0x7f              | c1 04 48 7f                |
    | rol dword [rax + 4 * rcx], 0x80              | c1 04 88 80                |
    | rol dword [rax + 8 * rcx], 0xff              | c1 04 c8 ff                |
    | rol dword [r8 + 1 * r9], 0x00                | 43 c1 04 08 00             |
    | rol dword [r8 + 4 * r9], 0x7f                | 43 c1 04 88 7f             |
    | rol dword [r8 + 8 * r9], 0x80                | 43 c1 04 c8 80             |
    | rol dword [1 * rcx], 0xff                    | c1 04 0d 00 00 00 00 ff    |
    | rol dword [2 * rcx], 0x00                    | c1 04 4d 00 00 00 00 00    |
    | rol dword [8 * rcx], 0x7f                    | c1 04 cd 00 00 00 00 7f    |
    | rol dword [1 * r9], 0x80                     | 42 c1 04 0d 00 00 00 00 80 |
    | rol dword [2 * r9], 0xff                     | 42 c1 04 4d 00 00 00 00 ff |
    | rol dword [4 * r9], 0x00                     | 42 c1 04 8d 00 00 00 00 00 |
    | rol dword [r13 + 8 * r12], 0x7f              | 43 c1 44 e5 00 7f          |
    | rol dword [rsp + 4 * r15], 0x80              | 42 c1 04 bc 80             |
    | rol dword [rax + 1 * rcx + 0x00], 0xff       | c1 44 08 00 ff             |
    | rol dword [rax + 1 * rcx - 0x00], 0x00       | c1 44 08 00 00             |
    | rol dword [rax + 1 * rcx - 0x01], 0x7f       | c1 44 08 ff 7f             |
    | rol dword [rax + 1 * rcx + 0x00000001], 0x80 | c1 84 08 01 00 00 00 80    |
    | rol dword [rax + 1 * rcx - 0x00000001], 0xff | c1 84 08 ff ff ff ff ff    |
    | rol dword [rax + 1 * rcx + 0x7f], 0x00       | c1 44 08 7f 00             |
    | rol dword [rax + 1 * rcx + 0x80], 0x7f       | c1 84 08 80 00 00 00 7f    |
    | rol dword [rax + 1 * rcx - 0x80], 0x80       | c1 44 08 80 80             |
    | rol dword [rax + 1 * rcx - 0x81], 0xff       | c1 84 08 7f ff ff ff ff    |
    | rol dword [rax + 1 * rcx + 0xff], 0x00       | c1 84 08 ff 00 00 00 00    |
    | rol dword [rax + 1 * rcx + 0x7fffffff], 0x7f | c1 84 08 ff ff ff 7f 7f    |
    | rol dword [rax + 1 * rcx - 0x7fffffff], 0x80 | c1 84 08 01 00 00 80 80    |
    | rol dword [rax + 1 * rcx - 0x80000000], 0xff | c1 84 08 00 00 00 80 ff    |
    | rol dword [r10 + 0x7f], 0x00                 | 41 c1 42 7f 00             |
    | rol dword [r10 - 0x80], 0x7f                 | 41 c1 42 80 7f             |
    | rol dword [r10 - 0x81], 0x80                 | 41 c1 82 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_rol_addr32_imm8():
    encode(ROL_ADDR32_IMM8)


ROL_ADDR32_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | rol dword [rax], cl                        | d3 00                   |
    | rol dword [rcx], cl                        | d3 01                   |
    | rol dword [rdx], cl                        | d3 02                   |
    | rol dword [rbx], cl                        | d3 03                   |
    | rol dword [rsp], cl                        | d3 04 24                |
    | rol dword [rbp], cl                        | d3 45 00                |
    | rol dword [rsi], cl                        | d3 06                   |
    | rol dword [rdi], cl                        | d3 07                   |
    | rol dword [r8], cl                         | 41 d3 00                |
    | rol dword [r9], cl                         | 41 d3 01                |
    | rol dword [r10], cl                        | 41 d3 02                |
    | rol dword [r11], cl                        | 41 d3 03                |
    | rol dword [r12], cl                        | 41 d3 04 24             |
    | rol dword [r13], cl                        | 41 d3 45 00             |
    | rol dword [r14], cl                        | 41 d3 06                |
    | rol dword [r15], cl                        | 41 d3 07                |
    | rol dword [rax + 1 * rcx], cl              | d3 04 08                |
    | rol dword [rcx + 1 * rcx], cl              | d3 04 09                |
    | rol dword [rdx + 1 * rcx], cl              | d3 04 0a                |
    | rol dword [rbx + 1 * rcx], cl              | d3 04 0b                |
    | rol dword [rsp + 1 * rcx], cl              | d3 04 0c                |
    | rol dword [rbp + 1 * rcx], cl              | d3 44 0d 00             |
    | rol dword [rsi + 1 * rcx], cl              | d3 04 0e                |
    | rol dword [rdi + 1 * rcx], cl              | d3 04 0f                |
    | rol dword [r8 + 1 * rcx], cl               | 41 d3 04 08             |
    | rol dword [r9 + 1 * rcx], cl               | 41 d3 04 09             |
    | rol dword [r10 + 1 * rcx], cl              | 41 d3 04 0a             |
    | rol dword [r11 + 1 * rcx], cl              | 41 d3 04 0b             |
    | rol dword [r12 + 1 * rcx], cl              | 41 d3 04 0c             |
    | rol dword [r13 + 1 * rcx], cl              | 41 d3 44 0d 00          |
    | rol dword [r14 + 1 * rcx], cl              | 41 d3 04 0e             |
    | rol dword [r15 + 1 * rcx], cl              | 41 d3 04 0f             |
    | rol dword [rax + 1 * rax], cl              | d3 04 00                |
    | rol dword [rax + 1 * rdx], cl              | d3 04 10                |
    | rol dword [rax + 1 * rbx], cl              | d3 04 18                |
    | rol dword [rax + 1 * rbp], cl              | d3 04 28                |
    | rol dword [rax + 1 * rsi], cl              | d3 04 30                |
    | rol dword [rax + 1 * rdi], cl              | d3 04 38                |
    | rol dword [rax + 1 * r8], cl               | 42 d3 04 00             |
    | rol dword [rax + 1 * r9], cl               | 42 d3 04 08             |
    | rol dword [rax + 1 * r10], cl              | 42 d3 04 10             |
    | rol dword [rax + 1 * r11], cl              | 42 d3 04 18             |
    | rol dword [rax + 1 * r12], cl              | 42 d3 04 20             |
    | rol dword [rax + 1 * r13], cl              | 42 d3 04 28             |
    | rol dword [rax + 1 * r14], cl              | 42 d3 04 30             |
    | rol dword [rax + 1 * r15], cl              | 42 d3 04 38             |
    | rol dword [rax + 2 * rcx], cl              | d3 04 48                |
    | rol dword [rax + 4 * rcx], cl              | d3 04 88                |
    | rol dword [rax + 8 * rcx], cl              | d3 04 c8                |
    | rol dword [r8 + 1 * r9], cl                | 43 d3 04 08             |
    | rol dword [r8 + 2 * r9], cl                | 43 d3 04 48             |
    | rol dword [r8 + 4 * r9], cl                | 43 d3 04 88             |
    | rol dword [r8 + 8 * r9], cl                | 43 d3 04 c8             |
    | rol dword [1 * rcx], cl                    | d3 04 0d 00 00 00 00    |
    | rol dword [2 * rcx], cl                    | d3 04 4d 00 00 00 00    |
    | rol dword [4 * rcx], cl                    | d3 04 8d 00 00 00 00    |
    | rol dword [8 * rcx], cl                    | d3 04 cd 00 00 00 00    |
    | rol dword [1 * r9], cl                     | 42 d3 04 0d 00 00 00 00 |
    | rol dword [2 * r9], cl                     | 42 d3 04 4d 00 00 00 00 |
    | rol dword [4 * r9], cl                     | 42 d3 04 8d 00 00 00 00 |
    | rol dword [8 * r9], cl                     | 42 d3 04 cd 00 00 00 00 |
    | rol dword [r13 + 8 * r12], cl              | 43 d3 44 e5 00          |
    | rol dword [rsp + 4 * r15], cl              | 42 d3 04 bc             |
    | rol dword [rax + 1 * rcx + 0x00], cl       | d3 44 08 00             |
    | rol dword [rax + 1 * rcx - 0x00], cl       | d3 44 08 00             |
    | rol dword [rax + 1 * rcx + 0x01], cl       | d3 44 08 01             |
    | rol dword [rax + 1 * rcx - 0x01], cl       | d3 44 08 ff             |
    | rol dword [rax + 1 * rcx + 0x00000001], cl | d3 84 08 01 00 00 00    |
    | rol dword [rax + 1 * rcx - 0x00000001], cl | d3 84 08 ff ff ff ff    |
    | rol dword [rax + 1 * rcx + 0x7f], cl       | d3 44 08 7f             |
    | rol dword [rax + 1 * rcx - 0x7f], cl       | d3 44 08 81             |
    | rol dword [rax + 1 * rcx + 0x80], cl       | d3 84 08 80 00 00 00    |
    | rol dword [rax + 1 * rcx - 0x80], cl       | d3 44 08 80             |
    | rol dword [rax + 1 * rcx - 0x81], cl       | d3 84 08 7f ff ff ff    |
    | rol dword [rax + 1 * rcx + 0xff], cl       | d3 84 08 ff 00 00 00    |
    | rol dword [rax + 1 * rcx - 0xff], cl       | d3 84 08 01 ff ff ff    |
    | rol dword [rax + 1 * rcx + 0x7fffffff], cl | d3 84 08 ff ff ff 7f    |
    | rol dword [rax + 1 * rcx - 0x7fffffff], cl | d3 84 08 01 00 00 80    |
    | rol dword [rax + 1 * rcx - 0x80000000], cl | d3 84 08 00 00 00 80    |
    | rol dword [r10 + 0x7f], cl                 | 41 d3 42 7f             |
    | rol dword [r10 + 0x80], cl                 | 41 d3 82 80 00 00 00    |
    | rol dword [r10 - 0x80], cl                 | 41 d3 42 80             |
    | rol dword [r10 - 0x81], cl                 | 41 d3 82 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_rol_addr32_cl():
    encode(ROL_ADDR32_CL)


ROL_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | rol word [rax], 0x01                        | 66 d1 00                      |
    | rol word [rcx], 0x01                        | 66 d1 01                      |
    | rol word [rdx], 0x01                        | 66 d1 02                      |
    | rol word [rbx], 0x01                        | 66 d1 03                      |
    | rol word [rsp], 0x01                        | 66 d1 04 24                   |
    | rol word [rbp], 0x01                        | 66 d1 45 00                   |
    | rol word [rsi], 0x01                        | 66 d1 06                      |
    | rol word [rdi], 0x01                        | 66 d1 07                      |
    | rol word [r8], 0x01                         | 66 41 d1 00                   |
    | rol word [r9], 0x01                         | 66 41 d1 01                   |
    | rol word [r10], 0x01                        | 66 41 d1 02                   |
    | rol word [r11], 0x01                        | 66 41 d1 03                   |
    | rol word [r12], 0x01                        | 66 41 d1 04 24                |
    | rol word [r13], 0x01                        | 66 41 d1 45 00                |
    | rol word [r14], 0x01                        | 66 41 d1 06                   |
    | rol word [r15], 0x01                        | 66 41 d1 07                   |
    | rol word [rax + 1 * rcx], 0x01              | 66 d1 04 08                   |
    | rol word [rcx + 1 * rcx], 0x01              | 66 d1 04 09                   |
    | rol word [rdx + 1 * rcx], 0x01              | 66 d1 04 0a                   |
    | rol word [rbx + 1 * rcx], 0x01              | 66 d1 04 0b                   |
    | rol word [rsp + 1 * rcx], 0x01              | 66 d1 04 0c                   |
    | rol word [rbp + 1 * rcx], 0x01              | 66 d1 44 0d 00                |
    | rol word [rsi + 1 * rcx], 0x01              | 66 d1 04 0e                   |
    | rol word [rdi + 1 * rcx], 0x01              | 66 d1 04 0f                   |
    | rol word [r8 + 1 * rcx], 0x01               | 66 41 d1 04 08                |
    | rol word [r9 + 1 * rcx], 0x01               | 66 41 d1 04 09                |
    | rol word [r10 + 1 * rcx], 0x01              | 66 41 d1 04 0a                |
    | rol word [r11 + 1 * rcx], 0x01              | 66 41 d1 04 0b                |
    | rol word [r12 + 1 * rcx], 0x01              | 66 41 d1 04 0c                |
    | rol word [r13 + 1 * rcx], 0x01              | 66 41 d1 44 0d 00             |
    | rol word [r14 + 1 * rcx], 0x01              | 66 41 d1 04 0e                |
    | rol word [r15 + 1 * rcx], 0x01              | 66 41 d1 04 0f                |
    | rol word [rax + 1 * rax], 0x01              | 66 d1 04 00                   |
    | rol word [rax + 1 * rdx], 0x01              | 66 d1 04 10                   |
    | rol word [rax + 1 * rbx], 0x01              | 66 d1 04 18                   |
    | rol word [rax + 1 * rbp], 0x01              | 66 d1 04 28                   |
    | rol word [rax + 1 * rsi], 0x01              | 66 d1 04 30                   |
    | rol word [rax + 1 * rdi], 0x01              | 66 d1 04 38                   |
    | rol word [rax + 1 * r8], 0x01               | 66 42 d1 04 00                |
    | rol word [rax + 1 * r9], 0x01               | 66 42 d1 04 08                |
    | rol word [rax + 1 * r10], 0x01              | 66 42 d1 04 10                |
    | rol word [rax + 1 * r11], 0x01              | 66 42 d1 04 18                |
    | rol word [rax + 1 * r12], 0x01              | 66 42 d1 04 20                |
    | rol word [rax + 1 * r13], 0x01              | 66 42 d1 04 28                |
    | rol word [rax + 1 * r14], 0x01              | 66 42 d1 04 30                |
    | rol word [rax + 1 * r15], 0x01              | 66 42 d1 04 38                |
    | rol word [rax + 2 * rcx], 0x01              | 66 d1 04 48                   |
    | rol word [rax + 4 * rcx], 0x01              | 66 d1 04 88                   |
    | rol word [rax + 8 * rcx], 0x01              | 66 d1 04 c8                   |
    | rol word [r8 + 1 * r9], 0x01                | 66 43 d1 04 08                |
    | rol word [r8 + 2 * r9], 0x01                | 66 43 d1 04 48                |
    | rol word [r8 + 4 * r9], 0x01                | 66 43 d1 04 88                |
    | rol word [r8 + 8 * r9], 0x01                | 66 43 d1 04 c8                |
    | rol word [1 * rcx], 0x01                    | 66 d1 04 0d 00 00 00 00       |
    | rol word [2 * rcx], 0x01                    | 66 d1 04 4d 00 00 00 00       |
    | rol word [4 * rcx], 0x01                    | 66 d1 04 8d 00 00 00 00       |
    | rol word [8 * rcx], 0x01                    | 66 d1 04 cd 00 00 00 00       |
    | rol word [1 * r9], 0x01                     | 66 42 d1 04 0d 00 00 00 00    |
    | rol word [2 * r9], 0x01                     | 66 42 d1 04 4d 00 00 00 00    |
    | rol word [4 * r9], 0x01                     | 66 42 d1 04 8d 00 00 00 00    |
    | rol word [8 * r9], 0x01                     | 66 42 d1 04 cd 00 00 00 00    |
    | rol word [r13 + 8 * r12], 0x01              | 66 43 d1 44 e5 00             |
    | rol word [rsp + 4 * r15], 0x01              | 66 42 d1 04 bc                |
    | rol word [rax + 1 * rcx + 0x00], 0x01       | 66 d1 44 08 00                |
    | rol word [rax + 1 * rcx - 0x00], 0x01       | 66 d1 44 08 00                |
    | rol word [rax + 1 * rcx + 0x01], 0x01       | 66 d1 44 08 01                |
    | rol word [rax + 1 * rcx - 0x01], 0x01       | 66 d1 44 08 ff                |
    | rol word [rax + 1 * rcx + 0x00000001], 0x01 | 66 d1 84 08 01 00 00 00       |
    | rol word [rax + 1 * rcx - 0x00000001], 0x01 | 66 d1 84 08 ff ff ff ff       |
    | rol word [rax + 1 * rcx + 0x7f], 0x01       | 66 d1 44 08 7f                |
    | rol word [rax + 1 * rcx - 0x7f], 0x01       | 66 d1 44 08 81                |
    | rol word [rax + 1 * rcx + 0x80], 0x01       | 66 d1 84 08 80 00 00 00       |
    | rol word [rax + 1 * rcx - 0x80], 0x01       | 66 d1 44 08 80                |
    | rol word [rax + 1 * rcx - 0x81], 0x01       | 66 d1 84 08 7f ff ff ff       |
    | rol word [rax + 1 * rcx + 0xff], 0x01       | 66 d1 84 08 ff 00 00 00       |
    | rol word [rax + 1 * rcx - 0xff], 0x01       | 66 d1 84 08 01 ff ff ff       |
    | rol word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 d1 84 08 ff ff ff 7f       |
    | rol word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 d1 84 08 01 00 00 80       |
    | rol word [rax + 1 * rcx - 0x80000000], 0x01 | 66 d1 84 08 00 00 00 80       |
    | rol word [r10 + 0x7f], 0x01                 | 66 41 d1 42 7f                |
    | rol word [r10 + 0x80], 0x01                 | 66 41 d1 82 80 00 00 00       |
    | rol word [r10 - 0x80], 0x01                 | 66 41 d1 42 80                |
    | rol word [r10 - 0x81], 0x01                 | 66 41 d1 82 7f ff ff ff       |
    | rol word [rax], 0x00                        | 66 c1 00 00                   |
    | rol word [rax], 0x7f                        | 66 c1 00 7f                   |
    | rol word [rax], 0x80                        | 66 c1 00 80                   |
    | rol word [rax], 0xff                        | 66 c1 00 ff                   |
    | rol word [rcx], 0x7f                        | 66 c1 01 7f                   |
    | rol word [rdx], 0x80                        | 66 c1 02 80                   |
    | rol word [rbx], 0xff                        | 66 c1 03 ff                   |
    | rol word [rsp], 0x00                        | 66 c1 04 24 00                |
    | rol word [rsi], 0x7f                        | 66 c1 06 7f                   |
    | rol word [rdi], 0x80                        | 66 c1 07 80                   |
    | rol word [r8], 0xff                         | 66 41 c1 00 ff                |
    | rol word [r9], 0x00                         | 66 41 c1 01 00                |
    | rol word [r11], 0x7f                        | 66 41 c1 03 7f                |
    | rol word [r12], 0x80                        | 66 41 c1 04 24 80             |
    | rol word [r13], 0xff                        | 66 41 c1 45 00 ff             |
    | rol word [r14], 0x00                        | 66 41 c1 06 00                |
    | rol word [rax + 1 * rcx], 0x7f              | 66 c1 04 08 7f                |
    | rol word [rcx + 1 * rcx], 0x80              | 66 c1 04 09 80                |
    | rol word [rdx + 1 * rcx], 0xff              | 66 c1 04 0a ff                |
    | rol word [rbx + 1 * rcx], 0x00              | 66 c1 04 0b 00                |
    | rol word [rbp + 1 * rcx], 0x7f              | 66 c1 44 0d 00 7f             |
    | rol word [rsi + 1 * rcx], 0x80              | 66 c1 04 0e 80                |
    | rol word [rdi + 1 * rcx], 0xff              | 66 c1 04 0f ff                |
    | rol word [r8 + 1 * rcx], 0x00               | 66 41 c1 04 08 00             |
    | rol word [r10 + 1 * rcx], 0x7f              | 66 41 c1 04 0a 7f             |
    | rol word [r11 + 1 * rcx], 0x80              | 66 41 c1 04 0b 80             |
    | rol word [r12 + 1 * rcx], 0xff              | 66 41 c1 04 0c ff             |
    | rol word [r13 + 1 * rcx], 0x00              | 66 41 c1 44 0d 00 00          |
    | rol word [r15 + 1 * rcx], 0x7f              | 66 41 c1 04 0f 7f             |
    | rol word [rax + 1 * rax], 0x80              | 66 c1 04 00 80                |
    | rol word [rax + 1 * rdx], 0xff              | 66 c1 04 10 ff                |
    | rol word [rax + 1 * rbx], 0x00              | 66 c1 04 18 00                |
    | rol word [rax + 1 * rsi], 0x7f              | 66 c1 04 30 7f                |
    | rol word [rax + 1 * rdi], 0x80              | 66 c1 04 38 80                |
    | rol word [rax + 1 * r8], 0xff               | 66 42 c1 04 00 ff             |
    | rol word [rax + 1 * r9], 0x00               | 66 42 c1 04 08 00             |
    | rol word [rax + 1 * r11], 0x7f              | 66 42 c1 04 18 7f             |
    | rol word [rax + 1 * r12], 0x80              | 66 42 c1 04 20 80             |
    | rol word [rax + 1 * r13], 0xff              | 66 42 c1 04 28 ff             |
    | rol word [rax + 1 * r14], 0x00              | 66 42 c1 04 30 00             |
    | rol word [rax + 2 * rcx], 0x7f              | 66 c1 04 48 7f                |
    | rol word [rax + 4 * rcx], 0x80              | 66 c1 04 88 80                |
    | rol word [rax + 8 * rcx], 0xff              | 66 c1 04 c8 ff                |
    | rol word [r8 + 1 * r9], 0x00                | 66 43 c1 04 08 00             |
    | rol word [r8 + 4 * r9], 0x7f                | 66 43 c1 04 88 7f             |
    | rol word [r8 + 8 * r9], 0x80                | 66 43 c1 04 c8 80             |
    | rol word [1 * rcx], 0xff                    | 66 c1 04 0d 00 00 00 00 ff    |
    | rol word [2 * rcx], 0x00                    | 66 c1 04 4d 00 00 00 00 00    |
    | rol word [8 * rcx], 0x7f                    | 66 c1 04 cd 00 00 00 00 7f    |
    | rol word [1 * r9], 0x80                     | 66 42 c1 04 0d 00 00 00 00 80 |
    | rol word [2 * r9], 0xff                     | 66 42 c1 04 4d 00 00 00 00 ff |
    | rol word [4 * r9], 0x00                     | 66 42 c1 04 8d 00 00 00 00 00 |
    | rol word [r13 + 8 * r12], 0x7f              | 66 43 c1 44 e5 00 7f          |
    | rol word [rsp + 4 * r15], 0x80              | 66 42 c1 04 bc 80             |
    | rol word [rax + 1 * rcx + 0x00], 0xff       | 66 c1 44 08 00 ff             |
    | rol word [rax + 1 * rcx - 0x00], 0x00       | 66 c1 44 08 00 00             |
    | rol word [rax + 1 * rcx - 0x01], 0x7f       | 66 c1 44 08 ff 7f             |
    | rol word [rax + 1 * rcx + 0x00000001], 0x80 | 66 c1 84 08 01 00 00 00 80    |
    | rol word [rax + 1 * rcx - 0x00000001], 0xff | 66 c1 84 08 ff ff ff ff ff    |
    | rol word [rax + 1 * rcx + 0x7f], 0x00       | 66 c1 44 08 7f 00             |
    | rol word [rax + 1 * rcx + 0x80], 0x7f       | 66 c1 84 08 80 00 00 00 7f    |
    | rol word [rax + 1 * rcx - 0x80], 0x80       | 66 c1 44 08 80 80             |
    | rol word [rax + 1 * rcx - 0x81], 0xff       | 66 c1 84 08 7f ff ff ff ff    |
    | rol word [rax + 1 * rcx + 0xff], 0x00       | 66 c1 84 08 ff 00 00 00 00    |
    | rol word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 c1 84 08 ff ff ff 7f 7f    |
    | rol word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 c1 84 08 01 00 00 80 80    |
    | rol word [rax + 1 * rcx - 0x80000000], 0xff | 66 c1 84 08 00 00 00 80 ff    |
    | rol word [r10 + 0x7f], 0x00                 | 66 41 c1 42 7f 00             |
    | rol word [r10 - 0x80], 0x7f                 | 66 41 c1 42 80 7f             |
    | rol word [r10 - 0x81], 0x80                 | 66 41 c1 82 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_rol_addr16_imm8():
    encode(ROL_ADDR16_IMM8)


ROL_ADDR16_CL = """
    | ----------------------------------------- | -------------------------- |
    | instruction                               | encoding                   |
    | ----------------------------------------- | -------------------------- |
    | rol word [rax], cl                        | 66 d3 00                   |
    | rol word [rcx], cl                        | 66 d3 01                   |
    | rol word [rdx], cl                        | 66 d3 02                   |
    | rol word [rbx], cl                        | 66 d3 03                   |
    | rol word [rsp], cl                        | 66 d3 04 24                |
    | rol word [rbp], cl                        | 66 d3 45 00                |
    | rol word [rsi], cl                        | 66 d3 06                   |
    | rol word [rdi], cl                        | 66 d3 07                   |
    | rol word [r8], cl                         | 66 41 d3 00                |
    | rol word [r9], cl                         | 66 41 d3 01                |
    | rol word [r10], cl                        | 66 41 d3 02                |
    | rol word [r11], cl                        | 66 41 d3 03                |
    | rol word [r12], cl                        | 66 41 d3 04 24             |
    | rol word [r13], cl                        | 66 41 d3 45 00             |
    | rol word [r14], cl                        | 66 41 d3 06                |
    | rol word [r15], cl                        | 66 41 d3 07                |
    | rol word [rax + 1 * rcx], cl              | 66 d3 04 08                |
    | rol word [rcx + 1 * rcx], cl              | 66 d3 04 09                |
    | rol word [rdx + 1 * rcx], cl              | 66 d3 04 0a                |
    | rol word [rbx + 1 * rcx], cl              | 66 d3 04 0b                |
    | rol word [rsp + 1 * rcx], cl              | 66 d3 04 0c                |
    | rol word [rbp + 1 * rcx], cl              | 66 d3 44 0d 00             |
    | rol word [rsi + 1 * rcx], cl              | 66 d3 04 0e                |
    | rol word [rdi + 1 * rcx], cl              | 66 d3 04 0f                |
    | rol word [r8 + 1 * rcx], cl               | 66 41 d3 04 08             |
    | rol word [r9 + 1 * rcx], cl               | 66 41 d3 04 09             |
    | rol word [r10 + 1 * rcx], cl              | 66 41 d3 04 0a             |
    | rol word [r11 + 1 * rcx], cl              | 66 41 d3 04 0b             |
    | rol word [r12 + 1 * rcx], cl              | 66 41 d3 04 0c             |
    | rol word [r13 + 1 * rcx], cl              | 66 41 d3 44 0d 00          |
    | rol word [r14 + 1 * rcx], cl              | 66 41 d3 04 0e             |
    | rol word [r15 + 1 * rcx], cl              | 66 41 d3 04 0f             |
    | rol word [rax + 1 * rax], cl              | 66 d3 04 00                |
    | rol word [rax + 1 * rdx], cl              | 66 d3 04 10                |
    | rol word [rax + 1 * rbx], cl              | 66 d3 04 18                |
    | rol word [rax + 1 * rbp], cl              | 66 d3 04 28                |
    | rol word [rax + 1 * rsi], cl              | 66 d3 04 30                |
    | rol word [rax + 1 * rdi], cl              | 66 d3 04 38                |
    | rol word [rax + 1 * r8], cl               | 66 42 d3 04 00             |
    | rol word [rax + 1 * r9], cl               | 66 42 d3 04 08             |
    | rol word [rax + 1 * r10], cl              | 66 42 d3 04 10             |
    | rol word [rax + 1 * r11], cl              | 66 42 d3 04 18             |
    | rol word [rax + 1 * r12], cl              | 66 42 d3 04 20             |
    | rol word [rax + 1 * r13], cl              | 66 42 d3 04 28             |
    | rol word [rax + 1 * r14], cl              | 66 42 d3 04 30             |
    | rol word [rax + 1 * r15], cl              | 66 42 d3 04 38             |
    | rol word [rax + 2 * rcx], cl              | 66 d3 04 48                |
    | rol word [rax + 4 * rcx], cl              | 66 d3 04 88                |
    | rol word [rax + 8 * rcx], cl              | 66 d3 04 c8                |
    | rol word [r8 + 1 * r9], cl                | 66 43 d3 04 08             |
    | rol word [r8 + 2 * r9], cl                | 66 43 d3 04 48             |
    | rol word [r8 + 4 * r9], cl                | 66 43 d3 04 88             |
    | rol word [r8 + 8 * r9], cl                | 66 43 d3 04 c8             |
    | rol word [1 * rcx], cl                    | 66 d3 04 0d 00 00 00 00    |
    | rol word [2 * rcx], cl                    | 66 d3 04 4d 00 00 00 00    |
    | rol word [4 * rcx], cl                    | 66 d3 04 8d 00 00 00 00    |
    | rol word [8 * rcx], cl                    | 66 d3 04 cd 00 00 00 00    |
    | rol word [1 * r9], cl                     | 66 42 d3 04 0d 00 00 00 00 |
    | rol word [2 * r9], cl                     | 66 42 d3 04 4d 00 00 00 00 |
    | rol word [4 * r9], cl                     | 66 42 d3 04 8d 00 00 00 00 |
    | rol word [8 * r9], cl                     | 66 42 d3 04 cd 00 00 00 00 |
    | rol word [r13 + 8 * r12], cl              | 66 43 d3 44 e5 00          |
    | rol word [rsp + 4 * r15], cl              | 66 42 d3 04 bc             |
    | rol word [rax + 1 * rcx + 0x00], cl       | 66 d3 44 08 00             |
    | rol word [rax + 1 * rcx - 0x00], cl       | 66 d3 44 08 00             |
    | rol word [rax + 1 * rcx + 0x01], cl       | 66 d3 44 08 01             |
    | rol word [rax + 1 * rcx - 0x01], cl       | 66 d3 44 08 ff             |
    | rol word [rax + 1 * rcx + 0x00000001], cl | 66 d3 84 08 01 00 00 00    |
    | rol word [rax + 1 * rcx - 0x00000001], cl | 66 d3 84 08 ff ff ff ff    |
    | rol word [rax + 1 * rcx + 0x7f], cl       | 66 d3 44 08 7f             |
    | rol word [rax + 1 * rcx - 0x7f], cl       | 66 d3 44 08 81             |
    | rol word [rax + 1 * rcx + 0x80], cl       | 66 d3 84 08 80 00 00 00    |
    | rol word [rax + 1 * rcx - 0x80], cl       | 66 d3 44 08 80             |
    | rol word [rax + 1 * rcx - 0x81], cl       | 66 d3 84 08 7f ff ff ff    |
    | rol word [rax + 1 * rcx + 0xff], cl       | 66 d3 84 08 ff 00 00 00    |
    | rol word [rax + 1 * rcx - 0xff], cl       | 66 d3 84 08 01 ff ff ff    |
    | rol word [rax + 1 * rcx + 0x7fffffff], cl | 66 d3 84 08 ff ff ff 7f    |
    | rol word [rax + 1 * rcx - 0x7fffffff], cl | 66 d3 84 08 01 00 00 80    |
    | rol word [rax + 1 * rcx - 0x80000000], cl | 66 d3 84 08 00 00 00 80    |
    | rol word [r10 + 0x7f], cl                 | 66 41 d3 42 7f             |
    | rol word [r10 + 0x80], cl                 | 66 41 d3 82 80 00 00 00    |
    | rol word [r10 - 0x80], cl                 | 66 41 d3 42 80             |
    | rol word [r10 - 0x81], cl                 | 66 41 d3 82 7f ff ff ff    |
    | ----------------------------------------- | -------------------------- |
"""


def can_encode_rol_addr16_cl():
    encode(ROL_ADDR16_CL)


ROL_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | rol byte [rax], 0x01                        | d0 00                      |
    | rol byte [rcx], 0x01                        | d0 01                      |
    | rol byte [rdx], 0x01                        | d0 02                      |
    | rol byte [rbx], 0x01                        | d0 03                      |
    | rol byte [rsp], 0x01                        | d0 04 24                   |
    | rol byte [rbp], 0x01                        | d0 45 00                   |
    | rol byte [rsi], 0x01                        | d0 06                      |
    | rol byte [rdi], 0x01                        | d0 07                      |
    | rol byte [r8], 0x01                         | 41 d0 00                   |
    | rol byte [r9], 0x01                         | 41 d0 01                   |
    | rol byte [r10], 0x01                        | 41 d0 02                   |
    | rol byte [r11], 0x01                        | 41 d0 03                   |
    | rol byte [r12], 0x01                        | 41 d0 04 24                |
    | rol byte [r13], 0x01                        | 41 d0 45 00                |
    | rol byte [r14], 0x01                        | 41 d0 06                   |
    | rol byte [r15], 0x01                        | 41 d0 07                   |
    | rol byte [rax + 1 * rcx], 0x01              | d0 04 08                   |
    | rol byte [rcx + 1 * rcx], 0x01              | d0 04 09                   |
    | rol byte [rdx + 1 * rcx], 0x01              | d0 04 0a                   |
    | rol byte [rbx + 1 * rcx], 0x01              | d0 04 0b                   |
    | rol byte [rsp + 1 * rcx], 0x01              | d0 04 0c                   |
    | rol byte [rbp + 1 * rcx], 0x01              | d0 44 0d 00                |
    | rol byte [rsi + 1 * rcx], 0x01              | d0 04 0e                   |
    | rol byte [rdi + 1 * rcx], 0x01              | d0 04 0f                   |
    | rol byte [r8 + 1 * rcx], 0x01               | 41 d0 04 08                |
    | rol byte [r9 + 1 * rcx], 0x01               | 41 d0 04 09                |
    | rol byte [r10 + 1 * rcx], 0x01              | 41 d0 04 0a                |
    | rol byte [r11 + 1 * rcx], 0x01              | 41 d0 04 0b                |
    | rol byte [r12 + 1 * rcx], 0x01              | 41 d0 04 0c                |
    | rol byte [r13 + 1 * rcx], 0x01              | 41 d0 44 0d 00             |
    | rol byte [r14 + 1 * rcx], 0x01              | 41 d0 04 0e                |
    | rol byte [r15 + 1 * rcx], 0x01              | 41 d0 04 0f                |
    | rol byte [rax + 1 * rax], 0x01              | d0 04 00                   |
    | rol byte [rax + 1 * rdx], 0x01              | d0 04 10                   |
    | rol byte [rax + 1 * rbx], 0x01              | d0 04 18                   |
    | rol byte [rax + 1 * rbp], 0x01              | d0 04 28                   |
    | rol byte [rax + 1 * rsi], 0x01              | d0 04 30                   |
    | rol byte [rax + 1 * rdi], 0x01              | d0 04 38                   |
    | rol byte [rax + 1 * r8], 0x01               | 42 d0 04 00                |
    | rol byte [rax + 1 * r9], 0x01               | 42 d0 04 08                |
    | rol byte [rax + 1 * r10], 0x01              | 42 d0 04 10                |
    | rol byte [rax + 1 * r11], 0x01              | 42 d0 04 18                |
    | rol byte [rax + 1 * r12], 0x01              | 42 d0 04 20                |
    | rol byte [rax + 1 * r13], 0x01              | 42 d0 04 28                |
    | rol byte [rax + 1 * r14], 0x01              | 42 d0 04 30                |
    | rol byte [rax + 1 * r15], 0x01              | 42 d0 04 38                |
    | rol byte [rax + 2 * rcx], 0x01              | d0 04 48                   |
    | rol byte [rax + 4 * rcx], 0x01              | d0 04 88                   |
    | rol byte [rax + 8 * rcx], 0x01              | d0 04 c8                   |
    | rol byte [r8 + 1 * r9], 0x01                | 43 d0 04 08                |
    | rol byte [r8 + 2 * r9], 0x01                | 43 d0 04 48                |
    | rol byte [r8 + 4 * r9], 0x01                | 43 d0 04 88                |
    | rol byte [r8 + 8 * r9], 0x01                | 43 d0 04 c8                |
    | rol byte [1 * rcx], 0x01                    | d0 04 0d 00 00 00 00       |
    | rol byte [2 * rcx], 0x01                    | d0 04 4d 00 00 00 00       |
    | rol byte [4 * rcx], 0x01                    | d0 04 8d 00 00 00 00       |
    | rol byte [8 * rcx], 0x01                    | d0 04 cd 00 00 00 00       |
    | rol byte [1 * r9], 0x01                     | 42 d0 04 0d 00 00 00 00    |
    | rol byte [2 * r9], 0x01                     | 42 d0 04 4d 00 00 00 00    |
    | rol byte [4 * r9], 0x01                     | 42 d0 04 8d 00 00 00 00    |
    | rol byte [8 * r9], 0x01                     | 42 d0 04 cd 00 00 00 00    |
    | rol byte [r13 + 8 * r12], 0x01              | 43 d0 44 e5 00             |
    | rol byte [rsp + 4 * r15], 0x01              | 42 d0 04 bc                |
    | rol byte [rax + 1 * rcx + 0x00], 0x01       | d0 44 08 00                |
    | rol byte [rax + 1 * rcx - 0x00], 0x01       | d0 44 08 00                |
    | rol byte [rax + 1 * rcx + 0x01], 0x01       | d0 44 08 01                |
    | rol byte [rax + 1 * rcx - 0x01], 0x01       | d0 44 08 ff                |
    | rol byte [rax + 1 * rcx + 0x00000001], 0x01 | d0 84 08 01 00 00 00       |
    | rol byte [rax + 1 * rcx - 0x00000001], 0x01 | d0 84 08 ff ff ff ff       |
    | rol byte [rax + 1 * rcx + 0x7f], 0x01       | d0 44 08 7f                |
    | rol byte [rax + 1 * rcx - 0x7f], 0x01       | d0 44 08 81                |
    | rol byte [rax + 1 * rcx + 0x80], 0x01       | d0 84 08 80 00 00 00       |
    | rol byte [rax + 1 * rcx - 0x80], 0x01       | d0 44 08 80                |
    | rol byte [rax + 1 * rcx - 0x81], 0x01       | d0 84 08 7f ff ff ff       |
    | rol byte [rax + 1 * rcx + 0xff], 0x01       | d0 84 08 ff 00 00 00       |
    | rol byte [rax + 1 * rcx - 0xff], 0x01       | d0 84 08 01 ff ff ff       |
    | rol byte [rax + 1 * rcx + 0x7fffffff], 0x01 | d0 84 08 ff ff ff 7f       |
    | rol byte [rax + 1 * rcx - 0x7fffffff], 0x01 | d0 84 08 01 00 00 80       |
    | rol byte [rax + 1 * rcx - 0x80000000], 0x01 | d0 84 08 00 00 00 80       |
    | rol byte [r10 + 0x7f], 0x01                 | 41 d0 42 7f                |
    | rol byte [r10 + 0x80], 0x01                 | 41 d0 82 80 00 00 00       |
    | rol byte [r10 - 0x80], 0x01                 | 41 d0 42 80                |
    | rol byte [r10 - 0x81], 0x01                 | 41 d0 82 7f ff ff ff       |
    | rol byte [rax], 0x00                        | c0 00 00                   |
    | rol byte [rax], 0x7f                        | c0 00 7f                   |
    | rol byte [rax], 0x80                        | c0 00 80                   |
    | rol byte [rax], 0xff                        | c0 00 ff                   |
    | rol byte [rcx], 0x7f                        | c0 01 7f                   |
    | rol byte [rdx], 0x80                        | c0 02 80                   |
    | rol byte [rbx], 0xff                        | c0 03 ff                   |
    | rol byte [rsp], 0x00                        | c0 04 24 00                |
    | rol byte [rsi], 0x7f                        | c0 06 7f                   |
    | rol byte [rdi], 0x80                        | c0 07 80                   |
    | rol byte [r8], 0xff                         | 41 c0 00 ff                |
    | rol byte [r9], 0x00                         | 41 c0 01 00                |
    | rol byte [r11], 0x7f                        | 41 c0 03 7f                |
    | rol byte [r12], 0x80                        | 41 c0 04 24 80             |
    | rol byte [r13], 0xff                        | 41 c0 45 00 ff             |
    | rol byte [r14], 0x00                        | 41 c0 06 00                |
    | rol byte [rax + 1 * rcx], 0x7f              | c0 04 08 7f                |
    | rol byte [rcx + 1 * rcx], 0x80              | c0 04 09 80                |
    | rol byte [rdx + 1 * rcx], 0xff              | c0 04 0a ff                |
    | rol byte [rbx + 1 * rcx], 0x00              | c0 04 0b 00                |
    | rol byte [rbp + 1 * rcx], 0x7f              | c0 44 0d 00 7f             |
    | rol byte [rsi + 1 * rcx], 0x80              | c0 04 0e 80                |
    | rol byte [rdi + 1 * rcx], 0xff              | c0 04 0f ff                |
    | rol byte [r8 + 1 * rcx], 0x00               | 41 c0 04 08 00             |
    | rol byte [r10 + 1 * rcx], 0x7f              | 41 c0 04 0a 7f             |
    | rol byte [r11 + 1 * rcx], 0x80              | 41 c0 04 0b 80             |
    | rol byte [r12 + 1 * rcx], 0xff              | 41 c0 04 0c ff             |
    | rol byte [r13 + 1 * rcx], 0x00              | 41 c0 44 0d 00 00          |
    | rol byte [r15 + 1 * rcx], 0x7f              | 41 c0 04 0f 7f             |
    | rol byte [rax + 1 * rax], 0x80              | c0 04 00 80                |
    | rol byte [rax + 1 * rdx], 0xff              | c0 04 10 ff                |
    | rol byte [rax + 1 * rbx], 0x00              | c0 04 18 00                |
    | rol byte [rax + 1 * rsi], 0x7f              | c0 04 30 7f                |
    | rol byte [rax + 1 * rdi], 0x80              | c0 04 38 80                |
    | rol byte [rax + 1 * r8], 0xff               | 42 c0 04 00 ff             |
    | rol byte [rax + 1 * r9], 0x00               | 42 c0 04 08 00             |
    | rol byte [rax + 1 * r11], 0x7f              | 42 c0 04 18 7f             |
    | rol byte [rax + 1 * r12], 0x80              | 42 c0 04 20 80             |
    | rol byte [rax + 1 * r13], 0xff              | 42 c0 04 28 ff             |
    | rol byte [rax + 1 * r14], 0x00              | 42 c0 04 30 00             |
    | rol byte [rax + 2 * rcx], 0x7f              | c0 04 48 7f                |
    | rol byte [rax + 4 * rcx], 0x80              | c0 04 88 80                |
    | rol byte [rax + 8 * rcx], 0xff              | c0 04 c8 ff                |
    | rol byte [r8 + 1 * r9], 0x00                | 43 c0 04 08 00             |
    | rol byte [r8 + 4 * r9], 0x7f                | 43 c0 04 88 7f             |
    | rol byte [r8 + 8 * r9], 0x80                | 43 c0 04 c8 80             |
    | rol byte [1 * rcx], 0xff                    | c0 04 0d 00 00 00 00 ff    |
    | rol byte [2 * rcx], 0x00                    | c0 04 4d 00 00 00 00 00    |
    | rol byte [8 * rcx], 0x7f                    | c0 04 cd 00 00 00 00 7f    |
    | rol byte [1 * r9], 0x80                     | 42 c0 04 0d 00 00 00 00 80 |
    | rol byte [2 * r9], 0xff                     | 42 c0 04 4d 00 00 00 00 ff |
    | rol byte [4 * r9], 0x00                     | 42 c0 04 8d 00 00 00 00 00 |
    | rol byte [r13 + 8 * r12], 0x7f              | 43 c0 44 e5 00 7f          |
    | rol byte [rsp + 4 * r15], 0x80              | 42 c0 04 bc 80             |
    | rol byte [rax + 1 * rcx + 0x00], 0xff       | c0 44 08 00 ff             |
    | rol byte [rax + 1 * rcx - 0x00], 0x00       | c0 44 08 00 00             |
    | rol byte [rax + 1 * rcx - 0x01], 0x7f       | c0 44 08 ff 7f             |
    | rol byte [rax + 1 * rcx + 0x00000001], 0x80 | c0 84 08 01 00 00 00 80    |
    | rol byte [rax + 1 * rcx - 0x00000001], 0xff | c0 84 08 ff ff ff ff ff    |
    | rol byte [rax + 1 * rcx + 0x7f], 0x00       | c0 44 08 7f 00             |
    | rol byte [rax + 1 * rcx + 0x80], 0x7f       | c0 84 08 80 00 00 00 7f    |
    | rol byte [rax + 1 * rcx - 0x80], 0x80       | c0 44 08 80 80             |
    | rol byte [rax + 1 * rcx - 0x81], 0xff       | c0 84 08 7f ff ff ff ff    |
    | rol byte [rax + 1 * rcx + 0xff], 0x00       | c0 84 08 ff 00 00 00 00    |
    | rol byte [rax + 1 * rcx + 0x7fffffff], 0x7f | c0 84 08 ff ff ff 7f 7f    |
    | rol byte [rax + 1 * rcx - 0x7fffffff], 0x80 | c0 84 08 01 00 00 80 80    |
    | rol byte [rax + 1 * rcx - 0x80000000], 0xff | c0 84 08 00 00 00 80 ff    |
    | rol byte [r10 + 0x7f], 0x00                 | 41 c0 42 7f 00             |
    | rol byte [r10 - 0x80], 0x7f                 | 41 c0 42 80 7f             |
    | rol byte [r10 - 0x81], 0x80                 | 41 c0 82 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_rol_addr8_imm8():
    encode(ROL_ADDR8_IMM8)


ROL_ADDR8_CL = """
    | ----------------------------------------- | ----------------------- |
    | instruction                               | encoding                |
    | ----------------------------------------- | ----------------------- |
    | rol byte [rax], cl                        | d2 00                   |
    | rol byte [rcx], cl                        | d2 01                   |
    | rol byte [rdx], cl                        | d2 02                   |
    | rol byte [rbx], cl                        | d2 03                   |
    | rol byte [rsp], cl                        | d2 04 24                |
    | rol byte [rbp], cl                        | d2 45 00                |
    | rol byte [rsi], cl                        | d2 06                   |
    | rol byte [rdi], cl                        | d2 07                   |
    | rol byte [r8], cl                         | 41 d2 00                |
    | rol byte [r9], cl                         | 41 d2 01                |
    | rol byte [r10], cl                        | 41 d2 02                |
    | rol byte [r11], cl                        | 41 d2 03                |
    | rol byte [r12], cl                        | 41 d2 04 24             |
    | rol byte [r13], cl                        | 41 d2 45 00             |
    | rol byte [r14], cl                        | 41 d2 06                |
    | rol byte [r15], cl                        | 41 d2 07                |
    | rol byte [rax + 1 * rcx], cl              | d2 04 08                |
    | rol byte [rcx + 1 * rcx], cl              | d2 04 09                |
    | rol byte [rdx + 1 * rcx], cl              | d2 04 0a                |
    | rol byte [rbx + 1 * rcx], cl              | d2 04 0b                |
    | rol byte [rsp + 1 * rcx], cl              | d2 04 0c                |
    | rol byte [rbp + 1 * rcx], cl              | d2 44 0d 00             |
    | rol byte [rsi + 1 * rcx], cl              | d2 04 0e                |
    | rol byte [rdi + 1 * rcx], cl              | d2 04 0f                |
    | rol byte [r8 + 1 * rcx], cl               | 41 d2 04 08             |
    | rol byte [r9 + 1 * rcx], cl               | 41 d2 04 09             |
    | rol byte [r10 + 1 * rcx], cl              | 41 d2 04 0a             |
    | rol byte [r11 + 1 * rcx], cl              | 41 d2 04 0b             |
    | rol byte [r12 + 1 * rcx], cl              | 41 d2 04 0c             |
    | rol byte [r13 + 1 * rcx], cl              | 41 d2 44 0d 00          |
    | rol byte [r14 + 1 * rcx], cl              | 41 d2 04 0e             |
    | rol byte [r15 + 1 * rcx], cl              | 41 d2 04 0f             |
    | rol byte [rax + 1 * rax], cl              | d2 04 00                |
    | rol byte [rax + 1 * rdx], cl              | d2 04 10                |
    | rol byte [rax + 1 * rbx], cl              | d2 04 18                |
    | rol byte [rax + 1 * rbp], cl              | d2 04 28                |
    | rol byte [rax + 1 * rsi], cl              | d2 04 30                |
    | rol byte [rax + 1 * rdi], cl              | d2 04 38                |
    | rol byte [rax + 1 * r8], cl               | 42 d2 04 00             |
    | rol byte [rax + 1 * r9], cl               | 42 d2 04 08             |
    | rol byte [rax + 1 * r10], cl              | 42 d2 04 10             |
    | rol byte [rax + 1 * r11], cl              | 42 d2 04 18             |
    | rol byte [rax + 1 * r12], cl              | 42 d2 04 20             |
    | rol byte [rax + 1 * r13], cl              | 42 d2 04 28             |
    | rol byte [rax + 1 * r14], cl              | 42 d2 04 30             |
    | rol byte [rax + 1 * r15], cl              | 42 d2 04 38             |
    | rol byte [rax + 2 * rcx], cl              | d2 04 48                |
    | rol byte [rax + 4 * rcx], cl              | d2 04 88                |
    | rol byte [rax + 8 * rcx], cl              | d2 04 c8                |
    | rol byte [r8 + 1 * r9], cl                | 43 d2 04 08             |
    | rol byte [r8 + 2 * r9], cl                | 43 d2 04 48             |
    | rol byte [r8 + 4 * r9], cl                | 43 d2 04 88             |
    | rol byte [r8 + 8 * r9], cl                | 43 d2 04 c8             |
    | rol byte [1 * rcx], cl                    | d2 04 0d 00 00 00 00    |
    | rol byte [2 * rcx], cl                    | d2 04 4d 00 00 00 00    |
    | rol byte [4 * rcx], cl                    | d2 04 8d 00 00 00 00    |
    | rol byte [8 * rcx], cl                    | d2 04 cd 00 00 00 00    |
    | rol byte [1 * r9], cl                     | 42 d2 04 0d 00 00 00 00 |
    | rol byte [2 * r9], cl                     | 42 d2 04 4d 00 00 00 00 |
    | rol byte [4 * r9], cl                     | 42 d2 04 8d 00 00 00 00 |
    | rol byte [8 * r9], cl                     | 42 d2 04 cd 00 00 00 00 |
    | rol byte [r13 + 8 * r12], cl              | 43 d2 44 e5 00          |
    | rol byte [rsp + 4 * r15], cl              | 42 d2 04 bc             |
    | rol byte [rax + 1 * rcx + 0x00], cl       | d2 44 08 00             |
    | rol byte [rax + 1 * rcx - 0x00], cl       | d2 44 08 00             |
    | rol byte [rax + 1 * rcx + 0x01], cl       | d2 44 08 01             |
    | rol byte [rax + 1 * rcx - 0x01], cl       | d2 44 08 ff             |
    | rol byte [rax + 1 * rcx + 0x00000001], cl | d2 84 08 01 00 00 00    |
    | rol byte [rax + 1 * rcx - 0x00000001], cl | d2 84 08 ff ff ff ff    |
    | rol byte [rax + 1 * rcx + 0x7f], cl       | d2 44 08 7f             |
    | rol byte [rax + 1 * rcx - 0x7f], cl       | d2 44 08 81             |
    | rol byte [rax + 1 * rcx + 0x80], cl       | d2 84 08 80 00 00 00    |
    | rol byte [rax + 1 * rcx - 0x80], cl       | d2 44 08 80             |
    | rol byte [rax + 1 * rcx - 0x81], cl       | d2 84 08 7f ff ff ff    |
    | rol byte [rax + 1 * rcx + 0xff], cl       | d2 84 08 ff 00 00 00    |
    | rol byte [rax + 1 * rcx - 0xff], cl       | d2 84 08 01 ff ff ff    |
    | rol byte [rax + 1 * rcx + 0x7fffffff], cl | d2 84 08 ff ff ff 7f    |
    | rol byte [rax + 1 * rcx - 0x7fffffff], cl | d2 84 08 01 00 00 80    |
    | rol byte [rax + 1 * rcx - 0x80000000], cl | d2 84 08 00 00 00 80    |
    | rol byte [r10 + 0x7f], cl                 | 41 d2 42 7f             |
    | rol byte [r10 + 0x80], cl                 | 41 d2 82 80 00 00 00    |
    | rol byte [r10 - 0x80], cl                 | 41 d2 42 80             |
    | rol byte [r10 - 0x81], cl                 | 41 d2 82 7f ff ff ff    |
    | ----------------------------------------- | ----------------------- |
"""


def can_encode_rol_addr8_cl():
    encode(ROL_ADDR8_CL)
