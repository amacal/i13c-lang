from tests.encoding.core import encode, exhaust


def can_exhaust_ror():
    exhaust(
        ROR_ADDR16_CL,
        ROR_ADDR16_IMM8,
        ROR_ADDR32_CL,
        ROR_ADDR32_IMM8,
        ROR_ADDR64_CL,
        ROR_ADDR64_IMM8,
        ROR_ADDR8_CL,
        ROR_ADDR8_IMM8,
        ROR_REG16_CL,
        ROR_REG16_IMM8,
        ROR_REG32_CL,
        ROR_REG32_IMM8,
        ROR_REG64_CL,
        ROR_REG64_IMM8,
        ROR_REG8_CL,
        ROR_REG8_IMM8,
    )


ROR_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | ror rax, 0x01 | 48 d1 c8    | *** | ror rax, 0x00 | 48 c1 c8 00 |
    | ror rcx, 0x01 | 48 d1 c9    | *** | ror rax, 0x7f | 48 c1 c8 7f |
    | ror rdx, 0x01 | 48 d1 ca    | *** | ror rax, 0x80 | 48 c1 c8 80 |
    | ror rbx, 0x01 | 48 d1 cb    | *** | ror rax, 0xff | 48 c1 c8 ff |
    | ror rsp, 0x01 | 48 d1 cc    | *** | ror rcx, 0x7f | 48 c1 c9 7f |
    | ror rbp, 0x01 | 48 d1 cd    | *** | ror rdx, 0x80 | 48 c1 ca 80 |
    | ror rsi, 0x01 | 48 d1 ce    | *** | ror rbx, 0xff | 48 c1 cb ff |
    | ror rdi, 0x01 | 48 d1 cf    | *** | ror rsp, 0x00 | 48 c1 cc 00 |
    | ror r8, 0x01  | 49 d1 c8    | *** | ror rsi, 0x7f | 48 c1 ce 7f |
    | ror r9, 0x01  | 49 d1 c9    | *** | ror rdi, 0x80 | 48 c1 cf 80 |
    | ror r10, 0x01 | 49 d1 ca    | *** | ror r8, 0xff  | 49 c1 c8 ff |
    | ror r11, 0x01 | 49 d1 cb    | *** | ror r9, 0x00  | 49 c1 c9 00 |
    | ror r12, 0x01 | 49 d1 cc    | *** | ror r11, 0x7f | 49 c1 cb 7f |
    | ror r13, 0x01 | 49 d1 cd    | *** | ror r12, 0x80 | 49 c1 cc 80 |
    | ror r14, 0x01 | 49 d1 ce    | *** | ror r13, 0xff | 49 c1 cd ff |
    | ror r15, 0x01 | 49 d1 cf    | *** | ror r14, 0x00 | 49 c1 ce 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_ror_reg64_imm8():
    encode(ROR_REG64_IMM8)


ROR_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | ror rax, cl | 48 d3 c8 | *** | ror r8, cl  | 49 d3 c8 |
    | ror rcx, cl | 48 d3 c9 | *** | ror r9, cl  | 49 d3 c9 |
    | ror rdx, cl | 48 d3 ca | *** | ror r10, cl | 49 d3 ca |
    | ror rbx, cl | 48 d3 cb | *** | ror r11, cl | 49 d3 cb |
    | ror rsp, cl | 48 d3 cc | *** | ror r12, cl | 49 d3 cc |
    | ror rbp, cl | 48 d3 cd | *** | ror r13, cl | 49 d3 cd |
    | ror rsi, cl | 48 d3 ce | *** | ror r14, cl | 49 d3 ce |
    | ror rdi, cl | 48 d3 cf | *** | ror r15, cl | 49 d3 cf |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_ror_reg64_cl():
    encode(ROR_REG64_CL)


ROR_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | ror eax, 0x01  | d1 c8       | *** | ror eax, 0x00  | c1 c8 00    |
    | ror ecx, 0x01  | d1 c9       | *** | ror eax, 0x7f  | c1 c8 7f    |
    | ror edx, 0x01  | d1 ca       | *** | ror eax, 0x80  | c1 c8 80    |
    | ror ebx, 0x01  | d1 cb       | *** | ror eax, 0xff  | c1 c8 ff    |
    | ror esp, 0x01  | d1 cc       | *** | ror ecx, 0x7f  | c1 c9 7f    |
    | ror ebp, 0x01  | d1 cd       | *** | ror edx, 0x80  | c1 ca 80    |
    | ror esi, 0x01  | d1 ce       | *** | ror ebx, 0xff  | c1 cb ff    |
    | ror edi, 0x01  | d1 cf       | *** | ror esp, 0x00  | c1 cc 00    |
    | ror r8d, 0x01  | 41 d1 c8    | *** | ror esi, 0x7f  | c1 ce 7f    |
    | ror r9d, 0x01  | 41 d1 c9    | *** | ror edi, 0x80  | c1 cf 80    |
    | ror r10d, 0x01 | 41 d1 ca    | *** | ror r8d, 0xff  | 41 c1 c8 ff |
    | ror r11d, 0x01 | 41 d1 cb    | *** | ror r9d, 0x00  | 41 c1 c9 00 |
    | ror r12d, 0x01 | 41 d1 cc    | *** | ror r11d, 0x7f | 41 c1 cb 7f |
    | ror r13d, 0x01 | 41 d1 cd    | *** | ror r12d, 0x80 | 41 c1 cc 80 |
    | ror r14d, 0x01 | 41 d1 ce    | *** | ror r13d, 0xff | 41 c1 cd ff |
    | ror r15d, 0x01 | 41 d1 cf    | *** | ror r14d, 0x00 | 41 c1 ce 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_ror_reg32_imm8():
    encode(ROR_REG32_IMM8)


ROR_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | ror eax, cl  | d3 c8    | *** | ror r8d, cl  | 41 d3 c8 |
    | ror ecx, cl  | d3 c9    | *** | ror r9d, cl  | 41 d3 c9 |
    | ror edx, cl  | d3 ca    | *** | ror r10d, cl | 41 d3 ca |
    | ror ebx, cl  | d3 cb    | *** | ror r11d, cl | 41 d3 cb |
    | ror esp, cl  | d3 cc    | *** | ror r12d, cl | 41 d3 cc |
    | ror ebp, cl  | d3 cd    | *** | ror r13d, cl | 41 d3 cd |
    | ror esi, cl  | d3 ce    | *** | ror r14d, cl | 41 d3 ce |
    | ror edi, cl  | d3 cf    | *** | ror r15d, cl | 41 d3 cf |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_ror_reg32_cl():
    encode(ROR_REG32_CL)


ROR_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | ror ax, 0x01   | 66 d1 c8       | *** | ror ax, 0x00   | 66 c1 c8 00    |
    | ror cx, 0x01   | 66 d1 c9       | *** | ror ax, 0x7f   | 66 c1 c8 7f    |
    | ror dx, 0x01   | 66 d1 ca       | *** | ror ax, 0x80   | 66 c1 c8 80    |
    | ror bx, 0x01   | 66 d1 cb       | *** | ror ax, 0xff   | 66 c1 c8 ff    |
    | ror sp, 0x01   | 66 d1 cc       | *** | ror cx, 0x7f   | 66 c1 c9 7f    |
    | ror bp, 0x01   | 66 d1 cd       | *** | ror dx, 0x80   | 66 c1 ca 80    |
    | ror si, 0x01   | 66 d1 ce       | *** | ror bx, 0xff   | 66 c1 cb ff    |
    | ror di, 0x01   | 66 d1 cf       | *** | ror sp, 0x00   | 66 c1 cc 00    |
    | ror r8w, 0x01  | 66 41 d1 c8    | *** | ror si, 0x7f   | 66 c1 ce 7f    |
    | ror r9w, 0x01  | 66 41 d1 c9    | *** | ror di, 0x80   | 66 c1 cf 80    |
    | ror r10w, 0x01 | 66 41 d1 ca    | *** | ror r8w, 0xff  | 66 41 c1 c8 ff |
    | ror r11w, 0x01 | 66 41 d1 cb    | *** | ror r9w, 0x00  | 66 41 c1 c9 00 |
    | ror r12w, 0x01 | 66 41 d1 cc    | *** | ror r11w, 0x7f | 66 41 c1 cb 7f |
    | ror r13w, 0x01 | 66 41 d1 cd    | *** | ror r12w, 0x80 | 66 41 c1 cc 80 |
    | ror r14w, 0x01 | 66 41 d1 ce    | *** | ror r13w, 0xff | 66 41 c1 cd ff |
    | ror r15w, 0x01 | 66 41 d1 cf    | *** | ror r14w, 0x00 | 66 41 c1 ce 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_ror_reg16_imm8():
    encode(ROR_REG16_IMM8)


ROR_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | ror ax, cl   | 66 d3 c8    | *** | ror r8w, cl  | 66 41 d3 c8 |
    | ror cx, cl   | 66 d3 c9    | *** | ror r9w, cl  | 66 41 d3 c9 |
    | ror dx, cl   | 66 d3 ca    | *** | ror r10w, cl | 66 41 d3 ca |
    | ror bx, cl   | 66 d3 cb    | *** | ror r11w, cl | 66 41 d3 cb |
    | ror sp, cl   | 66 d3 cc    | *** | ror r12w, cl | 66 41 d3 cc |
    | ror bp, cl   | 66 d3 cd    | *** | ror r13w, cl | 66 41 d3 cd |
    | ror si, cl   | 66 d3 ce    | *** | ror r14w, cl | 66 41 d3 ce |
    | ror di, cl   | 66 d3 cf    | *** | ror r15w, cl | 66 41 d3 cf |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_ror_reg16_cl():
    encode(ROR_REG16_CL)


ROR_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | ror al, 0x01   | d0 c8       | *** | ror al, 0x00   | c0 c8 00    |
    | ror cl, 0x01   | d0 c9       | *** | ror al, 0x7f   | c0 c8 7f    |
    | ror dl, 0x01   | d0 ca       | *** | ror al, 0x80   | c0 c8 80    |
    | ror bl, 0x01   | d0 cb       | *** | ror al, 0xff   | c0 c8 ff    |
    | ror spl, 0x01  | 40 d0 cc    | *** | ror cl, 0x7f   | c0 c9 7f    |
    | ror bpl, 0x01  | 40 d0 cd    | *** | ror dl, 0x80   | c0 ca 80    |
    | ror sil, 0x01  | 40 d0 ce    | *** | ror bl, 0xff   | c0 cb ff    |
    | ror dil, 0x01  | 40 d0 cf    | *** | ror spl, 0x00  | 40 c0 cc 00 |
    | ror r8b, 0x01  | 41 d0 c8    | *** | ror sil, 0x7f  | 40 c0 ce 7f |
    | ror r9b, 0x01  | 41 d0 c9    | *** | ror dil, 0x80  | 40 c0 cf 80 |
    | ror r10b, 0x01 | 41 d0 ca    | *** | ror r8b, 0xff  | 41 c0 c8 ff |
    | ror r11b, 0x01 | 41 d0 cb    | *** | ror r9b, 0x00  | 41 c0 c9 00 |
    | ror r12b, 0x01 | 41 d0 cc    | *** | ror r11b, 0x7f | 41 c0 cb 7f |
    | ror r13b, 0x01 | 41 d0 cd    | *** | ror r12b, 0x80 | 41 c0 cc 80 |
    | ror r14b, 0x01 | 41 d0 ce    | *** | ror r13b, 0xff | 41 c0 cd ff |
    | ror r15b, 0x01 | 41 d0 cf    | *** | ror r14b, 0x00 | 41 c0 ce 00 |
    | ror ah, 0x01   | d0 cc       | *** | ror ah, 0x7f   | c0 cc 7f    |
    | ror ch, 0x01   | d0 cd       | *** | ror ch, 0x80   | c0 cd 80    |
    | ror dh, 0x01   | d0 ce       | *** | ror dh, 0xff   | c0 ce ff    |
    | ror bh, 0x01   | d0 cf       | *** | ror bh, 0x00   | c0 cf 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_ror_reg8_imm8():
    encode(ROR_REG8_IMM8)


ROR_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | ror al, cl   | d2 c8    | *** | ror r10b, cl | 41 d2 ca |
    | ror cl, cl   | d2 c9    | *** | ror r11b, cl | 41 d2 cb |
    | ror dl, cl   | d2 ca    | *** | ror r12b, cl | 41 d2 cc |
    | ror bl, cl   | d2 cb    | *** | ror r13b, cl | 41 d2 cd |
    | ror spl, cl  | 40 d2 cc | *** | ror r14b, cl | 41 d2 ce |
    | ror bpl, cl  | 40 d2 cd | *** | ror r15b, cl | 41 d2 cf |
    | ror sil, cl  | 40 d2 ce | *** | ror ah, cl   | d2 cc    |
    | ror dil, cl  | 40 d2 cf | *** | ror ch, cl   | d2 cd    |
    | ror r8b, cl  | 41 d2 c8 | *** | ror dh, cl   | d2 ce    |
    | ror r9b, cl  | 41 d2 c9 | *** | ror bh, cl   | d2 cf    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_ror_reg8_cl():
    encode(ROR_REG8_CL)


ROR_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | ror qword [rax], 0x01                        | 48 d1 08                   |
    | ror qword [rcx], 0x01                        | 48 d1 09                   |
    | ror qword [rdx], 0x01                        | 48 d1 0a                   |
    | ror qword [rbx], 0x01                        | 48 d1 0b                   |
    | ror qword [rsp], 0x01                        | 48 d1 0c 24                |
    | ror qword [rbp], 0x01                        | 48 d1 4d 00                |
    | ror qword [rsi], 0x01                        | 48 d1 0e                   |
    | ror qword [rdi], 0x01                        | 48 d1 0f                   |
    | ror qword [r8], 0x01                         | 49 d1 08                   |
    | ror qword [r9], 0x01                         | 49 d1 09                   |
    | ror qword [r10], 0x01                        | 49 d1 0a                   |
    | ror qword [r11], 0x01                        | 49 d1 0b                   |
    | ror qword [r12], 0x01                        | 49 d1 0c 24                |
    | ror qword [r13], 0x01                        | 49 d1 4d 00                |
    | ror qword [r14], 0x01                        | 49 d1 0e                   |
    | ror qword [r15], 0x01                        | 49 d1 0f                   |
    | ror qword [rax + 1 * rcx], 0x01              | 48 d1 0c 08                |
    | ror qword [rcx + 1 * rcx], 0x01              | 48 d1 0c 09                |
    | ror qword [rdx + 1 * rcx], 0x01              | 48 d1 0c 0a                |
    | ror qword [rbx + 1 * rcx], 0x01              | 48 d1 0c 0b                |
    | ror qword [rsp + 1 * rcx], 0x01              | 48 d1 0c 0c                |
    | ror qword [rbp + 1 * rcx], 0x01              | 48 d1 4c 0d 00             |
    | ror qword [rsi + 1 * rcx], 0x01              | 48 d1 0c 0e                |
    | ror qword [rdi + 1 * rcx], 0x01              | 48 d1 0c 0f                |
    | ror qword [r8 + 1 * rcx], 0x01               | 49 d1 0c 08                |
    | ror qword [r9 + 1 * rcx], 0x01               | 49 d1 0c 09                |
    | ror qword [r10 + 1 * rcx], 0x01              | 49 d1 0c 0a                |
    | ror qword [r11 + 1 * rcx], 0x01              | 49 d1 0c 0b                |
    | ror qword [r12 + 1 * rcx], 0x01              | 49 d1 0c 0c                |
    | ror qword [r13 + 1 * rcx], 0x01              | 49 d1 4c 0d 00             |
    | ror qword [r14 + 1 * rcx], 0x01              | 49 d1 0c 0e                |
    | ror qword [r15 + 1 * rcx], 0x01              | 49 d1 0c 0f                |
    | ror qword [rax + 1 * rax], 0x01              | 48 d1 0c 00                |
    | ror qword [rax + 1 * rdx], 0x01              | 48 d1 0c 10                |
    | ror qword [rax + 1 * rbx], 0x01              | 48 d1 0c 18                |
    | ror qword [rax + 1 * rbp], 0x01              | 48 d1 0c 28                |
    | ror qword [rax + 1 * rsi], 0x01              | 48 d1 0c 30                |
    | ror qword [rax + 1 * rdi], 0x01              | 48 d1 0c 38                |
    | ror qword [rax + 1 * r8], 0x01               | 4a d1 0c 00                |
    | ror qword [rax + 1 * r9], 0x01               | 4a d1 0c 08                |
    | ror qword [rax + 1 * r10], 0x01              | 4a d1 0c 10                |
    | ror qword [rax + 1 * r11], 0x01              | 4a d1 0c 18                |
    | ror qword [rax + 1 * r12], 0x01              | 4a d1 0c 20                |
    | ror qword [rax + 1 * r13], 0x01              | 4a d1 0c 28                |
    | ror qword [rax + 1 * r14], 0x01              | 4a d1 0c 30                |
    | ror qword [rax + 1 * r15], 0x01              | 4a d1 0c 38                |
    | ror qword [rax + 2 * rcx], 0x01              | 48 d1 0c 48                |
    | ror qword [rax + 4 * rcx], 0x01              | 48 d1 0c 88                |
    | ror qword [rax + 8 * rcx], 0x01              | 48 d1 0c c8                |
    | ror qword [r8 + 1 * r9], 0x01                | 4b d1 0c 08                |
    | ror qword [r8 + 2 * r9], 0x01                | 4b d1 0c 48                |
    | ror qword [r8 + 4 * r9], 0x01                | 4b d1 0c 88                |
    | ror qword [r8 + 8 * r9], 0x01                | 4b d1 0c c8                |
    | ror qword [1 * rcx], 0x01                    | 48 d1 0c 0d 00 00 00 00    |
    | ror qword [2 * rcx], 0x01                    | 48 d1 0c 4d 00 00 00 00    |
    | ror qword [4 * rcx], 0x01                    | 48 d1 0c 8d 00 00 00 00    |
    | ror qword [8 * rcx], 0x01                    | 48 d1 0c cd 00 00 00 00    |
    | ror qword [1 * r9], 0x01                     | 4a d1 0c 0d 00 00 00 00    |
    | ror qword [2 * r9], 0x01                     | 4a d1 0c 4d 00 00 00 00    |
    | ror qword [4 * r9], 0x01                     | 4a d1 0c 8d 00 00 00 00    |
    | ror qword [8 * r9], 0x01                     | 4a d1 0c cd 00 00 00 00    |
    | ror qword [r13 + 8 * r12], 0x01              | 4b d1 4c e5 00             |
    | ror qword [rsp + 4 * r15], 0x01              | 4a d1 0c bc                |
    | ror qword [rax + 1 * rcx + 0x00], 0x01       | 48 d1 4c 08 00             |
    | ror qword [rax + 1 * rcx - 0x00], 0x01       | 48 d1 4c 08 00             |
    | ror qword [rax + 1 * rcx + 0x01], 0x01       | 48 d1 4c 08 01             |
    | ror qword [rax + 1 * rcx - 0x01], 0x01       | 48 d1 4c 08 ff             |
    | ror qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 d1 8c 08 01 00 00 00    |
    | ror qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 d1 8c 08 ff ff ff ff    |
    | ror qword [rax + 1 * rcx + 0x7f], 0x01       | 48 d1 4c 08 7f             |
    | ror qword [rax + 1 * rcx - 0x7f], 0x01       | 48 d1 4c 08 81             |
    | ror qword [rax + 1 * rcx + 0x80], 0x01       | 48 d1 8c 08 80 00 00 00    |
    | ror qword [rax + 1 * rcx - 0x80], 0x01       | 48 d1 4c 08 80             |
    | ror qword [rax + 1 * rcx - 0x81], 0x01       | 48 d1 8c 08 7f ff ff ff    |
    | ror qword [rax + 1 * rcx + 0xff], 0x01       | 48 d1 8c 08 ff 00 00 00    |
    | ror qword [rax + 1 * rcx - 0xff], 0x01       | 48 d1 8c 08 01 ff ff ff    |
    | ror qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 d1 8c 08 ff ff ff 7f    |
    | ror qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 d1 8c 08 01 00 00 80    |
    | ror qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 d1 8c 08 00 00 00 80    |
    | ror qword [r10 + 0x7f], 0x01                 | 49 d1 4a 7f                |
    | ror qword [r10 + 0x80], 0x01                 | 49 d1 8a 80 00 00 00       |
    | ror qword [r10 - 0x80], 0x01                 | 49 d1 4a 80                |
    | ror qword [r10 - 0x81], 0x01                 | 49 d1 8a 7f ff ff ff       |
    | ror qword [rax], 0x00                        | 48 c1 08 00                |
    | ror qword [rax], 0x7f                        | 48 c1 08 7f                |
    | ror qword [rax], 0x80                        | 48 c1 08 80                |
    | ror qword [rax], 0xff                        | 48 c1 08 ff                |
    | ror qword [rcx], 0x7f                        | 48 c1 09 7f                |
    | ror qword [rdx], 0x80                        | 48 c1 0a 80                |
    | ror qword [rbx], 0xff                        | 48 c1 0b ff                |
    | ror qword [rsp], 0x00                        | 48 c1 0c 24 00             |
    | ror qword [rsi], 0x7f                        | 48 c1 0e 7f                |
    | ror qword [rdi], 0x80                        | 48 c1 0f 80                |
    | ror qword [r8], 0xff                         | 49 c1 08 ff                |
    | ror qword [r9], 0x00                         | 49 c1 09 00                |
    | ror qword [r11], 0x7f                        | 49 c1 0b 7f                |
    | ror qword [r12], 0x80                        | 49 c1 0c 24 80             |
    | ror qword [r13], 0xff                        | 49 c1 4d 00 ff             |
    | ror qword [r14], 0x00                        | 49 c1 0e 00                |
    | ror qword [rax + 1 * rcx], 0x7f              | 48 c1 0c 08 7f             |
    | ror qword [rcx + 1 * rcx], 0x80              | 48 c1 0c 09 80             |
    | ror qword [rdx + 1 * rcx], 0xff              | 48 c1 0c 0a ff             |
    | ror qword [rbx + 1 * rcx], 0x00              | 48 c1 0c 0b 00             |
    | ror qword [rbp + 1 * rcx], 0x7f              | 48 c1 4c 0d 00 7f          |
    | ror qword [rsi + 1 * rcx], 0x80              | 48 c1 0c 0e 80             |
    | ror qword [rdi + 1 * rcx], 0xff              | 48 c1 0c 0f ff             |
    | ror qword [r8 + 1 * rcx], 0x00               | 49 c1 0c 08 00             |
    | ror qword [r10 + 1 * rcx], 0x7f              | 49 c1 0c 0a 7f             |
    | ror qword [r11 + 1 * rcx], 0x80              | 49 c1 0c 0b 80             |
    | ror qword [r12 + 1 * rcx], 0xff              | 49 c1 0c 0c ff             |
    | ror qword [r13 + 1 * rcx], 0x00              | 49 c1 4c 0d 00 00          |
    | ror qword [r15 + 1 * rcx], 0x7f              | 49 c1 0c 0f 7f             |
    | ror qword [rax + 1 * rax], 0x80              | 48 c1 0c 00 80             |
    | ror qword [rax + 1 * rdx], 0xff              | 48 c1 0c 10 ff             |
    | ror qword [rax + 1 * rbx], 0x00              | 48 c1 0c 18 00             |
    | ror qword [rax + 1 * rsi], 0x7f              | 48 c1 0c 30 7f             |
    | ror qword [rax + 1 * rdi], 0x80              | 48 c1 0c 38 80             |
    | ror qword [rax + 1 * r8], 0xff               | 4a c1 0c 00 ff             |
    | ror qword [rax + 1 * r9], 0x00               | 4a c1 0c 08 00             |
    | ror qword [rax + 1 * r11], 0x7f              | 4a c1 0c 18 7f             |
    | ror qword [rax + 1 * r12], 0x80              | 4a c1 0c 20 80             |
    | ror qword [rax + 1 * r13], 0xff              | 4a c1 0c 28 ff             |
    | ror qword [rax + 1 * r14], 0x00              | 4a c1 0c 30 00             |
    | ror qword [rax + 2 * rcx], 0x7f              | 48 c1 0c 48 7f             |
    | ror qword [rax + 4 * rcx], 0x80              | 48 c1 0c 88 80             |
    | ror qword [rax + 8 * rcx], 0xff              | 48 c1 0c c8 ff             |
    | ror qword [r8 + 1 * r9], 0x00                | 4b c1 0c 08 00             |
    | ror qword [r8 + 4 * r9], 0x7f                | 4b c1 0c 88 7f             |
    | ror qword [r8 + 8 * r9], 0x80                | 4b c1 0c c8 80             |
    | ror qword [1 * rcx], 0xff                    | 48 c1 0c 0d 00 00 00 00 ff |
    | ror qword [2 * rcx], 0x00                    | 48 c1 0c 4d 00 00 00 00 00 |
    | ror qword [8 * rcx], 0x7f                    | 48 c1 0c cd 00 00 00 00 7f |
    | ror qword [1 * r9], 0x80                     | 4a c1 0c 0d 00 00 00 00 80 |
    | ror qword [2 * r9], 0xff                     | 4a c1 0c 4d 00 00 00 00 ff |
    | ror qword [4 * r9], 0x00                     | 4a c1 0c 8d 00 00 00 00 00 |
    | ror qword [r13 + 8 * r12], 0x7f              | 4b c1 4c e5 00 7f          |
    | ror qword [rsp + 4 * r15], 0x80              | 4a c1 0c bc 80             |
    | ror qword [rax + 1 * rcx + 0x00], 0xff       | 48 c1 4c 08 00 ff          |
    | ror qword [rax + 1 * rcx - 0x00], 0x00       | 48 c1 4c 08 00 00          |
    | ror qword [rax + 1 * rcx - 0x01], 0x7f       | 48 c1 4c 08 ff 7f          |
    | ror qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 c1 8c 08 01 00 00 00 80 |
    | ror qword [rax + 1 * rcx - 0x00000001], 0xff | 48 c1 8c 08 ff ff ff ff ff |
    | ror qword [rax + 1 * rcx + 0x7f], 0x00       | 48 c1 4c 08 7f 00          |
    | ror qword [rax + 1 * rcx + 0x80], 0x7f       | 48 c1 8c 08 80 00 00 00 7f |
    | ror qword [rax + 1 * rcx - 0x80], 0x80       | 48 c1 4c 08 80 80          |
    | ror qword [rax + 1 * rcx - 0x81], 0xff       | 48 c1 8c 08 7f ff ff ff ff |
    | ror qword [rax + 1 * rcx + 0xff], 0x00       | 48 c1 8c 08 ff 00 00 00 00 |
    | ror qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 c1 8c 08 ff ff ff 7f 7f |
    | ror qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 c1 8c 08 01 00 00 80 80 |
    | ror qword [rax + 1 * rcx - 0x80000000], 0xff | 48 c1 8c 08 00 00 00 80 ff |
    | ror qword [r10 + 0x7f], 0x00                 | 49 c1 4a 7f 00             |
    | ror qword [r10 - 0x80], 0x7f                 | 49 c1 4a 80 7f             |
    | ror qword [r10 - 0x81], 0x80                 | 49 c1 8a 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_ror_addr64_imm8():
    encode(ROR_ADDR64_IMM8)


ROR_ADDR64_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | ror qword [rax], cl                        | 48 d3 08                |
    | ror qword [rcx], cl                        | 48 d3 09                |
    | ror qword [rdx], cl                        | 48 d3 0a                |
    | ror qword [rbx], cl                        | 48 d3 0b                |
    | ror qword [rsp], cl                        | 48 d3 0c 24             |
    | ror qword [rbp], cl                        | 48 d3 4d 00             |
    | ror qword [rsi], cl                        | 48 d3 0e                |
    | ror qword [rdi], cl                        | 48 d3 0f                |
    | ror qword [r8], cl                         | 49 d3 08                |
    | ror qword [r9], cl                         | 49 d3 09                |
    | ror qword [r10], cl                        | 49 d3 0a                |
    | ror qword [r11], cl                        | 49 d3 0b                |
    | ror qword [r12], cl                        | 49 d3 0c 24             |
    | ror qword [r13], cl                        | 49 d3 4d 00             |
    | ror qword [r14], cl                        | 49 d3 0e                |
    | ror qword [r15], cl                        | 49 d3 0f                |
    | ror qword [rax + 1 * rcx], cl              | 48 d3 0c 08             |
    | ror qword [rcx + 1 * rcx], cl              | 48 d3 0c 09             |
    | ror qword [rdx + 1 * rcx], cl              | 48 d3 0c 0a             |
    | ror qword [rbx + 1 * rcx], cl              | 48 d3 0c 0b             |
    | ror qword [rsp + 1 * rcx], cl              | 48 d3 0c 0c             |
    | ror qword [rbp + 1 * rcx], cl              | 48 d3 4c 0d 00          |
    | ror qword [rsi + 1 * rcx], cl              | 48 d3 0c 0e             |
    | ror qword [rdi + 1 * rcx], cl              | 48 d3 0c 0f             |
    | ror qword [r8 + 1 * rcx], cl               | 49 d3 0c 08             |
    | ror qword [r9 + 1 * rcx], cl               | 49 d3 0c 09             |
    | ror qword [r10 + 1 * rcx], cl              | 49 d3 0c 0a             |
    | ror qword [r11 + 1 * rcx], cl              | 49 d3 0c 0b             |
    | ror qword [r12 + 1 * rcx], cl              | 49 d3 0c 0c             |
    | ror qword [r13 + 1 * rcx], cl              | 49 d3 4c 0d 00          |
    | ror qword [r14 + 1 * rcx], cl              | 49 d3 0c 0e             |
    | ror qword [r15 + 1 * rcx], cl              | 49 d3 0c 0f             |
    | ror qword [rax + 1 * rax], cl              | 48 d3 0c 00             |
    | ror qword [rax + 1 * rdx], cl              | 48 d3 0c 10             |
    | ror qword [rax + 1 * rbx], cl              | 48 d3 0c 18             |
    | ror qword [rax + 1 * rbp], cl              | 48 d3 0c 28             |
    | ror qword [rax + 1 * rsi], cl              | 48 d3 0c 30             |
    | ror qword [rax + 1 * rdi], cl              | 48 d3 0c 38             |
    | ror qword [rax + 1 * r8], cl               | 4a d3 0c 00             |
    | ror qword [rax + 1 * r9], cl               | 4a d3 0c 08             |
    | ror qword [rax + 1 * r10], cl              | 4a d3 0c 10             |
    | ror qword [rax + 1 * r11], cl              | 4a d3 0c 18             |
    | ror qword [rax + 1 * r12], cl              | 4a d3 0c 20             |
    | ror qword [rax + 1 * r13], cl              | 4a d3 0c 28             |
    | ror qword [rax + 1 * r14], cl              | 4a d3 0c 30             |
    | ror qword [rax + 1 * r15], cl              | 4a d3 0c 38             |
    | ror qword [rax + 2 * rcx], cl              | 48 d3 0c 48             |
    | ror qword [rax + 4 * rcx], cl              | 48 d3 0c 88             |
    | ror qword [rax + 8 * rcx], cl              | 48 d3 0c c8             |
    | ror qword [r8 + 1 * r9], cl                | 4b d3 0c 08             |
    | ror qword [r8 + 2 * r9], cl                | 4b d3 0c 48             |
    | ror qword [r8 + 4 * r9], cl                | 4b d3 0c 88             |
    | ror qword [r8 + 8 * r9], cl                | 4b d3 0c c8             |
    | ror qword [1 * rcx], cl                    | 48 d3 0c 0d 00 00 00 00 |
    | ror qword [2 * rcx], cl                    | 48 d3 0c 4d 00 00 00 00 |
    | ror qword [4 * rcx], cl                    | 48 d3 0c 8d 00 00 00 00 |
    | ror qword [8 * rcx], cl                    | 48 d3 0c cd 00 00 00 00 |
    | ror qword [1 * r9], cl                     | 4a d3 0c 0d 00 00 00 00 |
    | ror qword [2 * r9], cl                     | 4a d3 0c 4d 00 00 00 00 |
    | ror qword [4 * r9], cl                     | 4a d3 0c 8d 00 00 00 00 |
    | ror qword [8 * r9], cl                     | 4a d3 0c cd 00 00 00 00 |
    | ror qword [r13 + 8 * r12], cl              | 4b d3 4c e5 00          |
    | ror qword [rsp + 4 * r15], cl              | 4a d3 0c bc             |
    | ror qword [rax + 1 * rcx + 0x00], cl       | 48 d3 4c 08 00          |
    | ror qword [rax + 1 * rcx - 0x00], cl       | 48 d3 4c 08 00          |
    | ror qword [rax + 1 * rcx + 0x01], cl       | 48 d3 4c 08 01          |
    | ror qword [rax + 1 * rcx - 0x01], cl       | 48 d3 4c 08 ff          |
    | ror qword [rax + 1 * rcx + 0x00000001], cl | 48 d3 8c 08 01 00 00 00 |
    | ror qword [rax + 1 * rcx - 0x00000001], cl | 48 d3 8c 08 ff ff ff ff |
    | ror qword [rax + 1 * rcx + 0x7f], cl       | 48 d3 4c 08 7f          |
    | ror qword [rax + 1 * rcx - 0x7f], cl       | 48 d3 4c 08 81          |
    | ror qword [rax + 1 * rcx + 0x80], cl       | 48 d3 8c 08 80 00 00 00 |
    | ror qword [rax + 1 * rcx - 0x80], cl       | 48 d3 4c 08 80          |
    | ror qword [rax + 1 * rcx - 0x81], cl       | 48 d3 8c 08 7f ff ff ff |
    | ror qword [rax + 1 * rcx + 0xff], cl       | 48 d3 8c 08 ff 00 00 00 |
    | ror qword [rax + 1 * rcx - 0xff], cl       | 48 d3 8c 08 01 ff ff ff |
    | ror qword [rax + 1 * rcx + 0x7fffffff], cl | 48 d3 8c 08 ff ff ff 7f |
    | ror qword [rax + 1 * rcx - 0x7fffffff], cl | 48 d3 8c 08 01 00 00 80 |
    | ror qword [rax + 1 * rcx - 0x80000000], cl | 48 d3 8c 08 00 00 00 80 |
    | ror qword [r10 + 0x7f], cl                 | 49 d3 4a 7f             |
    | ror qword [r10 + 0x80], cl                 | 49 d3 8a 80 00 00 00    |
    | ror qword [r10 - 0x80], cl                 | 49 d3 4a 80             |
    | ror qword [r10 - 0x81], cl                 | 49 d3 8a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_ror_addr64_cl():
    encode(ROR_ADDR64_CL)


ROR_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | ror dword [rax], 0x01                        | d1 08                      |
    | ror dword [rcx], 0x01                        | d1 09                      |
    | ror dword [rdx], 0x01                        | d1 0a                      |
    | ror dword [rbx], 0x01                        | d1 0b                      |
    | ror dword [rsp], 0x01                        | d1 0c 24                   |
    | ror dword [rbp], 0x01                        | d1 4d 00                   |
    | ror dword [rsi], 0x01                        | d1 0e                      |
    | ror dword [rdi], 0x01                        | d1 0f                      |
    | ror dword [r8], 0x01                         | 41 d1 08                   |
    | ror dword [r9], 0x01                         | 41 d1 09                   |
    | ror dword [r10], 0x01                        | 41 d1 0a                   |
    | ror dword [r11], 0x01                        | 41 d1 0b                   |
    | ror dword [r12], 0x01                        | 41 d1 0c 24                |
    | ror dword [r13], 0x01                        | 41 d1 4d 00                |
    | ror dword [r14], 0x01                        | 41 d1 0e                   |
    | ror dword [r15], 0x01                        | 41 d1 0f                   |
    | ror dword [rax + 1 * rcx], 0x01              | d1 0c 08                   |
    | ror dword [rcx + 1 * rcx], 0x01              | d1 0c 09                   |
    | ror dword [rdx + 1 * rcx], 0x01              | d1 0c 0a                   |
    | ror dword [rbx + 1 * rcx], 0x01              | d1 0c 0b                   |
    | ror dword [rsp + 1 * rcx], 0x01              | d1 0c 0c                   |
    | ror dword [rbp + 1 * rcx], 0x01              | d1 4c 0d 00                |
    | ror dword [rsi + 1 * rcx], 0x01              | d1 0c 0e                   |
    | ror dword [rdi + 1 * rcx], 0x01              | d1 0c 0f                   |
    | ror dword [r8 + 1 * rcx], 0x01               | 41 d1 0c 08                |
    | ror dword [r9 + 1 * rcx], 0x01               | 41 d1 0c 09                |
    | ror dword [r10 + 1 * rcx], 0x01              | 41 d1 0c 0a                |
    | ror dword [r11 + 1 * rcx], 0x01              | 41 d1 0c 0b                |
    | ror dword [r12 + 1 * rcx], 0x01              | 41 d1 0c 0c                |
    | ror dword [r13 + 1 * rcx], 0x01              | 41 d1 4c 0d 00             |
    | ror dword [r14 + 1 * rcx], 0x01              | 41 d1 0c 0e                |
    | ror dword [r15 + 1 * rcx], 0x01              | 41 d1 0c 0f                |
    | ror dword [rax + 1 * rax], 0x01              | d1 0c 00                   |
    | ror dword [rax + 1 * rdx], 0x01              | d1 0c 10                   |
    | ror dword [rax + 1 * rbx], 0x01              | d1 0c 18                   |
    | ror dword [rax + 1 * rbp], 0x01              | d1 0c 28                   |
    | ror dword [rax + 1 * rsi], 0x01              | d1 0c 30                   |
    | ror dword [rax + 1 * rdi], 0x01              | d1 0c 38                   |
    | ror dword [rax + 1 * r8], 0x01               | 42 d1 0c 00                |
    | ror dword [rax + 1 * r9], 0x01               | 42 d1 0c 08                |
    | ror dword [rax + 1 * r10], 0x01              | 42 d1 0c 10                |
    | ror dword [rax + 1 * r11], 0x01              | 42 d1 0c 18                |
    | ror dword [rax + 1 * r12], 0x01              | 42 d1 0c 20                |
    | ror dword [rax + 1 * r13], 0x01              | 42 d1 0c 28                |
    | ror dword [rax + 1 * r14], 0x01              | 42 d1 0c 30                |
    | ror dword [rax + 1 * r15], 0x01              | 42 d1 0c 38                |
    | ror dword [rax + 2 * rcx], 0x01              | d1 0c 48                   |
    | ror dword [rax + 4 * rcx], 0x01              | d1 0c 88                   |
    | ror dword [rax + 8 * rcx], 0x01              | d1 0c c8                   |
    | ror dword [r8 + 1 * r9], 0x01                | 43 d1 0c 08                |
    | ror dword [r8 + 2 * r9], 0x01                | 43 d1 0c 48                |
    | ror dword [r8 + 4 * r9], 0x01                | 43 d1 0c 88                |
    | ror dword [r8 + 8 * r9], 0x01                | 43 d1 0c c8                |
    | ror dword [1 * rcx], 0x01                    | d1 0c 0d 00 00 00 00       |
    | ror dword [2 * rcx], 0x01                    | d1 0c 4d 00 00 00 00       |
    | ror dword [4 * rcx], 0x01                    | d1 0c 8d 00 00 00 00       |
    | ror dword [8 * rcx], 0x01                    | d1 0c cd 00 00 00 00       |
    | ror dword [1 * r9], 0x01                     | 42 d1 0c 0d 00 00 00 00    |
    | ror dword [2 * r9], 0x01                     | 42 d1 0c 4d 00 00 00 00    |
    | ror dword [4 * r9], 0x01                     | 42 d1 0c 8d 00 00 00 00    |
    | ror dword [8 * r9], 0x01                     | 42 d1 0c cd 00 00 00 00    |
    | ror dword [r13 + 8 * r12], 0x01              | 43 d1 4c e5 00             |
    | ror dword [rsp + 4 * r15], 0x01              | 42 d1 0c bc                |
    | ror dword [rax + 1 * rcx + 0x00], 0x01       | d1 4c 08 00                |
    | ror dword [rax + 1 * rcx - 0x00], 0x01       | d1 4c 08 00                |
    | ror dword [rax + 1 * rcx + 0x01], 0x01       | d1 4c 08 01                |
    | ror dword [rax + 1 * rcx - 0x01], 0x01       | d1 4c 08 ff                |
    | ror dword [rax + 1 * rcx + 0x00000001], 0x01 | d1 8c 08 01 00 00 00       |
    | ror dword [rax + 1 * rcx - 0x00000001], 0x01 | d1 8c 08 ff ff ff ff       |
    | ror dword [rax + 1 * rcx + 0x7f], 0x01       | d1 4c 08 7f                |
    | ror dword [rax + 1 * rcx - 0x7f], 0x01       | d1 4c 08 81                |
    | ror dword [rax + 1 * rcx + 0x80], 0x01       | d1 8c 08 80 00 00 00       |
    | ror dword [rax + 1 * rcx - 0x80], 0x01       | d1 4c 08 80                |
    | ror dword [rax + 1 * rcx - 0x81], 0x01       | d1 8c 08 7f ff ff ff       |
    | ror dword [rax + 1 * rcx + 0xff], 0x01       | d1 8c 08 ff 00 00 00       |
    | ror dword [rax + 1 * rcx - 0xff], 0x01       | d1 8c 08 01 ff ff ff       |
    | ror dword [rax + 1 * rcx + 0x7fffffff], 0x01 | d1 8c 08 ff ff ff 7f       |
    | ror dword [rax + 1 * rcx - 0x7fffffff], 0x01 | d1 8c 08 01 00 00 80       |
    | ror dword [rax + 1 * rcx - 0x80000000], 0x01 | d1 8c 08 00 00 00 80       |
    | ror dword [r10 + 0x7f], 0x01                 | 41 d1 4a 7f                |
    | ror dword [r10 + 0x80], 0x01                 | 41 d1 8a 80 00 00 00       |
    | ror dword [r10 - 0x80], 0x01                 | 41 d1 4a 80                |
    | ror dword [r10 - 0x81], 0x01                 | 41 d1 8a 7f ff ff ff       |
    | ror dword [rax], 0x00                        | c1 08 00                   |
    | ror dword [rax], 0x7f                        | c1 08 7f                   |
    | ror dword [rax], 0x80                        | c1 08 80                   |
    | ror dword [rax], 0xff                        | c1 08 ff                   |
    | ror dword [rcx], 0x7f                        | c1 09 7f                   |
    | ror dword [rdx], 0x80                        | c1 0a 80                   |
    | ror dword [rbx], 0xff                        | c1 0b ff                   |
    | ror dword [rsp], 0x00                        | c1 0c 24 00                |
    | ror dword [rsi], 0x7f                        | c1 0e 7f                   |
    | ror dword [rdi], 0x80                        | c1 0f 80                   |
    | ror dword [r8], 0xff                         | 41 c1 08 ff                |
    | ror dword [r9], 0x00                         | 41 c1 09 00                |
    | ror dword [r11], 0x7f                        | 41 c1 0b 7f                |
    | ror dword [r12], 0x80                        | 41 c1 0c 24 80             |
    | ror dword [r13], 0xff                        | 41 c1 4d 00 ff             |
    | ror dword [r14], 0x00                        | 41 c1 0e 00                |
    | ror dword [rax + 1 * rcx], 0x7f              | c1 0c 08 7f                |
    | ror dword [rcx + 1 * rcx], 0x80              | c1 0c 09 80                |
    | ror dword [rdx + 1 * rcx], 0xff              | c1 0c 0a ff                |
    | ror dword [rbx + 1 * rcx], 0x00              | c1 0c 0b 00                |
    | ror dword [rbp + 1 * rcx], 0x7f              | c1 4c 0d 00 7f             |
    | ror dword [rsi + 1 * rcx], 0x80              | c1 0c 0e 80                |
    | ror dword [rdi + 1 * rcx], 0xff              | c1 0c 0f ff                |
    | ror dword [r8 + 1 * rcx], 0x00               | 41 c1 0c 08 00             |
    | ror dword [r10 + 1 * rcx], 0x7f              | 41 c1 0c 0a 7f             |
    | ror dword [r11 + 1 * rcx], 0x80              | 41 c1 0c 0b 80             |
    | ror dword [r12 + 1 * rcx], 0xff              | 41 c1 0c 0c ff             |
    | ror dword [r13 + 1 * rcx], 0x00              | 41 c1 4c 0d 00 00          |
    | ror dword [r15 + 1 * rcx], 0x7f              | 41 c1 0c 0f 7f             |
    | ror dword [rax + 1 * rax], 0x80              | c1 0c 00 80                |
    | ror dword [rax + 1 * rdx], 0xff              | c1 0c 10 ff                |
    | ror dword [rax + 1 * rbx], 0x00              | c1 0c 18 00                |
    | ror dword [rax + 1 * rsi], 0x7f              | c1 0c 30 7f                |
    | ror dword [rax + 1 * rdi], 0x80              | c1 0c 38 80                |
    | ror dword [rax + 1 * r8], 0xff               | 42 c1 0c 00 ff             |
    | ror dword [rax + 1 * r9], 0x00               | 42 c1 0c 08 00             |
    | ror dword [rax + 1 * r11], 0x7f              | 42 c1 0c 18 7f             |
    | ror dword [rax + 1 * r12], 0x80              | 42 c1 0c 20 80             |
    | ror dword [rax + 1 * r13], 0xff              | 42 c1 0c 28 ff             |
    | ror dword [rax + 1 * r14], 0x00              | 42 c1 0c 30 00             |
    | ror dword [rax + 2 * rcx], 0x7f              | c1 0c 48 7f                |
    | ror dword [rax + 4 * rcx], 0x80              | c1 0c 88 80                |
    | ror dword [rax + 8 * rcx], 0xff              | c1 0c c8 ff                |
    | ror dword [r8 + 1 * r9], 0x00                | 43 c1 0c 08 00             |
    | ror dword [r8 + 4 * r9], 0x7f                | 43 c1 0c 88 7f             |
    | ror dword [r8 + 8 * r9], 0x80                | 43 c1 0c c8 80             |
    | ror dword [1 * rcx], 0xff                    | c1 0c 0d 00 00 00 00 ff    |
    | ror dword [2 * rcx], 0x00                    | c1 0c 4d 00 00 00 00 00    |
    | ror dword [8 * rcx], 0x7f                    | c1 0c cd 00 00 00 00 7f    |
    | ror dword [1 * r9], 0x80                     | 42 c1 0c 0d 00 00 00 00 80 |
    | ror dword [2 * r9], 0xff                     | 42 c1 0c 4d 00 00 00 00 ff |
    | ror dword [4 * r9], 0x00                     | 42 c1 0c 8d 00 00 00 00 00 |
    | ror dword [r13 + 8 * r12], 0x7f              | 43 c1 4c e5 00 7f          |
    | ror dword [rsp + 4 * r15], 0x80              | 42 c1 0c bc 80             |
    | ror dword [rax + 1 * rcx + 0x00], 0xff       | c1 4c 08 00 ff             |
    | ror dword [rax + 1 * rcx - 0x00], 0x00       | c1 4c 08 00 00             |
    | ror dword [rax + 1 * rcx - 0x01], 0x7f       | c1 4c 08 ff 7f             |
    | ror dword [rax + 1 * rcx + 0x00000001], 0x80 | c1 8c 08 01 00 00 00 80    |
    | ror dword [rax + 1 * rcx - 0x00000001], 0xff | c1 8c 08 ff ff ff ff ff    |
    | ror dword [rax + 1 * rcx + 0x7f], 0x00       | c1 4c 08 7f 00             |
    | ror dword [rax + 1 * rcx + 0x80], 0x7f       | c1 8c 08 80 00 00 00 7f    |
    | ror dword [rax + 1 * rcx - 0x80], 0x80       | c1 4c 08 80 80             |
    | ror dword [rax + 1 * rcx - 0x81], 0xff       | c1 8c 08 7f ff ff ff ff    |
    | ror dword [rax + 1 * rcx + 0xff], 0x00       | c1 8c 08 ff 00 00 00 00    |
    | ror dword [rax + 1 * rcx + 0x7fffffff], 0x7f | c1 8c 08 ff ff ff 7f 7f    |
    | ror dword [rax + 1 * rcx - 0x7fffffff], 0x80 | c1 8c 08 01 00 00 80 80    |
    | ror dword [rax + 1 * rcx - 0x80000000], 0xff | c1 8c 08 00 00 00 80 ff    |
    | ror dword [r10 + 0x7f], 0x00                 | 41 c1 4a 7f 00             |
    | ror dword [r10 - 0x80], 0x7f                 | 41 c1 4a 80 7f             |
    | ror dword [r10 - 0x81], 0x80                 | 41 c1 8a 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_ror_addr32_imm8():
    encode(ROR_ADDR32_IMM8)


ROR_ADDR32_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | ror dword [rax], cl                        | d3 08                   |
    | ror dword [rcx], cl                        | d3 09                   |
    | ror dword [rdx], cl                        | d3 0a                   |
    | ror dword [rbx], cl                        | d3 0b                   |
    | ror dword [rsp], cl                        | d3 0c 24                |
    | ror dword [rbp], cl                        | d3 4d 00                |
    | ror dword [rsi], cl                        | d3 0e                   |
    | ror dword [rdi], cl                        | d3 0f                   |
    | ror dword [r8], cl                         | 41 d3 08                |
    | ror dword [r9], cl                         | 41 d3 09                |
    | ror dword [r10], cl                        | 41 d3 0a                |
    | ror dword [r11], cl                        | 41 d3 0b                |
    | ror dword [r12], cl                        | 41 d3 0c 24             |
    | ror dword [r13], cl                        | 41 d3 4d 00             |
    | ror dword [r14], cl                        | 41 d3 0e                |
    | ror dword [r15], cl                        | 41 d3 0f                |
    | ror dword [rax + 1 * rcx], cl              | d3 0c 08                |
    | ror dword [rcx + 1 * rcx], cl              | d3 0c 09                |
    | ror dword [rdx + 1 * rcx], cl              | d3 0c 0a                |
    | ror dword [rbx + 1 * rcx], cl              | d3 0c 0b                |
    | ror dword [rsp + 1 * rcx], cl              | d3 0c 0c                |
    | ror dword [rbp + 1 * rcx], cl              | d3 4c 0d 00             |
    | ror dword [rsi + 1 * rcx], cl              | d3 0c 0e                |
    | ror dword [rdi + 1 * rcx], cl              | d3 0c 0f                |
    | ror dword [r8 + 1 * rcx], cl               | 41 d3 0c 08             |
    | ror dword [r9 + 1 * rcx], cl               | 41 d3 0c 09             |
    | ror dword [r10 + 1 * rcx], cl              | 41 d3 0c 0a             |
    | ror dword [r11 + 1 * rcx], cl              | 41 d3 0c 0b             |
    | ror dword [r12 + 1 * rcx], cl              | 41 d3 0c 0c             |
    | ror dword [r13 + 1 * rcx], cl              | 41 d3 4c 0d 00          |
    | ror dword [r14 + 1 * rcx], cl              | 41 d3 0c 0e             |
    | ror dword [r15 + 1 * rcx], cl              | 41 d3 0c 0f             |
    | ror dword [rax + 1 * rax], cl              | d3 0c 00                |
    | ror dword [rax + 1 * rdx], cl              | d3 0c 10                |
    | ror dword [rax + 1 * rbx], cl              | d3 0c 18                |
    | ror dword [rax + 1 * rbp], cl              | d3 0c 28                |
    | ror dword [rax + 1 * rsi], cl              | d3 0c 30                |
    | ror dword [rax + 1 * rdi], cl              | d3 0c 38                |
    | ror dword [rax + 1 * r8], cl               | 42 d3 0c 00             |
    | ror dword [rax + 1 * r9], cl               | 42 d3 0c 08             |
    | ror dword [rax + 1 * r10], cl              | 42 d3 0c 10             |
    | ror dword [rax + 1 * r11], cl              | 42 d3 0c 18             |
    | ror dword [rax + 1 * r12], cl              | 42 d3 0c 20             |
    | ror dword [rax + 1 * r13], cl              | 42 d3 0c 28             |
    | ror dword [rax + 1 * r14], cl              | 42 d3 0c 30             |
    | ror dword [rax + 1 * r15], cl              | 42 d3 0c 38             |
    | ror dword [rax + 2 * rcx], cl              | d3 0c 48                |
    | ror dword [rax + 4 * rcx], cl              | d3 0c 88                |
    | ror dword [rax + 8 * rcx], cl              | d3 0c c8                |
    | ror dword [r8 + 1 * r9], cl                | 43 d3 0c 08             |
    | ror dword [r8 + 2 * r9], cl                | 43 d3 0c 48             |
    | ror dword [r8 + 4 * r9], cl                | 43 d3 0c 88             |
    | ror dword [r8 + 8 * r9], cl                | 43 d3 0c c8             |
    | ror dword [1 * rcx], cl                    | d3 0c 0d 00 00 00 00    |
    | ror dword [2 * rcx], cl                    | d3 0c 4d 00 00 00 00    |
    | ror dword [4 * rcx], cl                    | d3 0c 8d 00 00 00 00    |
    | ror dword [8 * rcx], cl                    | d3 0c cd 00 00 00 00    |
    | ror dword [1 * r9], cl                     | 42 d3 0c 0d 00 00 00 00 |
    | ror dword [2 * r9], cl                     | 42 d3 0c 4d 00 00 00 00 |
    | ror dword [4 * r9], cl                     | 42 d3 0c 8d 00 00 00 00 |
    | ror dword [8 * r9], cl                     | 42 d3 0c cd 00 00 00 00 |
    | ror dword [r13 + 8 * r12], cl              | 43 d3 4c e5 00          |
    | ror dword [rsp + 4 * r15], cl              | 42 d3 0c bc             |
    | ror dword [rax + 1 * rcx + 0x00], cl       | d3 4c 08 00             |
    | ror dword [rax + 1 * rcx - 0x00], cl       | d3 4c 08 00             |
    | ror dword [rax + 1 * rcx + 0x01], cl       | d3 4c 08 01             |
    | ror dword [rax + 1 * rcx - 0x01], cl       | d3 4c 08 ff             |
    | ror dword [rax + 1 * rcx + 0x00000001], cl | d3 8c 08 01 00 00 00    |
    | ror dword [rax + 1 * rcx - 0x00000001], cl | d3 8c 08 ff ff ff ff    |
    | ror dword [rax + 1 * rcx + 0x7f], cl       | d3 4c 08 7f             |
    | ror dword [rax + 1 * rcx - 0x7f], cl       | d3 4c 08 81             |
    | ror dword [rax + 1 * rcx + 0x80], cl       | d3 8c 08 80 00 00 00    |
    | ror dword [rax + 1 * rcx - 0x80], cl       | d3 4c 08 80             |
    | ror dword [rax + 1 * rcx - 0x81], cl       | d3 8c 08 7f ff ff ff    |
    | ror dword [rax + 1 * rcx + 0xff], cl       | d3 8c 08 ff 00 00 00    |
    | ror dword [rax + 1 * rcx - 0xff], cl       | d3 8c 08 01 ff ff ff    |
    | ror dword [rax + 1 * rcx + 0x7fffffff], cl | d3 8c 08 ff ff ff 7f    |
    | ror dword [rax + 1 * rcx - 0x7fffffff], cl | d3 8c 08 01 00 00 80    |
    | ror dword [rax + 1 * rcx - 0x80000000], cl | d3 8c 08 00 00 00 80    |
    | ror dword [r10 + 0x7f], cl                 | 41 d3 4a 7f             |
    | ror dword [r10 + 0x80], cl                 | 41 d3 8a 80 00 00 00    |
    | ror dword [r10 - 0x80], cl                 | 41 d3 4a 80             |
    | ror dword [r10 - 0x81], cl                 | 41 d3 8a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_ror_addr32_cl():
    encode(ROR_ADDR32_CL)


ROR_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | ror word [rax], 0x01                        | 66 d1 08                      |
    | ror word [rcx], 0x01                        | 66 d1 09                      |
    | ror word [rdx], 0x01                        | 66 d1 0a                      |
    | ror word [rbx], 0x01                        | 66 d1 0b                      |
    | ror word [rsp], 0x01                        | 66 d1 0c 24                   |
    | ror word [rbp], 0x01                        | 66 d1 4d 00                   |
    | ror word [rsi], 0x01                        | 66 d1 0e                      |
    | ror word [rdi], 0x01                        | 66 d1 0f                      |
    | ror word [r8], 0x01                         | 66 41 d1 08                   |
    | ror word [r9], 0x01                         | 66 41 d1 09                   |
    | ror word [r10], 0x01                        | 66 41 d1 0a                   |
    | ror word [r11], 0x01                        | 66 41 d1 0b                   |
    | ror word [r12], 0x01                        | 66 41 d1 0c 24                |
    | ror word [r13], 0x01                        | 66 41 d1 4d 00                |
    | ror word [r14], 0x01                        | 66 41 d1 0e                   |
    | ror word [r15], 0x01                        | 66 41 d1 0f                   |
    | ror word [rax + 1 * rcx], 0x01              | 66 d1 0c 08                   |
    | ror word [rcx + 1 * rcx], 0x01              | 66 d1 0c 09                   |
    | ror word [rdx + 1 * rcx], 0x01              | 66 d1 0c 0a                   |
    | ror word [rbx + 1 * rcx], 0x01              | 66 d1 0c 0b                   |
    | ror word [rsp + 1 * rcx], 0x01              | 66 d1 0c 0c                   |
    | ror word [rbp + 1 * rcx], 0x01              | 66 d1 4c 0d 00                |
    | ror word [rsi + 1 * rcx], 0x01              | 66 d1 0c 0e                   |
    | ror word [rdi + 1 * rcx], 0x01              | 66 d1 0c 0f                   |
    | ror word [r8 + 1 * rcx], 0x01               | 66 41 d1 0c 08                |
    | ror word [r9 + 1 * rcx], 0x01               | 66 41 d1 0c 09                |
    | ror word [r10 + 1 * rcx], 0x01              | 66 41 d1 0c 0a                |
    | ror word [r11 + 1 * rcx], 0x01              | 66 41 d1 0c 0b                |
    | ror word [r12 + 1 * rcx], 0x01              | 66 41 d1 0c 0c                |
    | ror word [r13 + 1 * rcx], 0x01              | 66 41 d1 4c 0d 00             |
    | ror word [r14 + 1 * rcx], 0x01              | 66 41 d1 0c 0e                |
    | ror word [r15 + 1 * rcx], 0x01              | 66 41 d1 0c 0f                |
    | ror word [rax + 1 * rax], 0x01              | 66 d1 0c 00                   |
    | ror word [rax + 1 * rdx], 0x01              | 66 d1 0c 10                   |
    | ror word [rax + 1 * rbx], 0x01              | 66 d1 0c 18                   |
    | ror word [rax + 1 * rbp], 0x01              | 66 d1 0c 28                   |
    | ror word [rax + 1 * rsi], 0x01              | 66 d1 0c 30                   |
    | ror word [rax + 1 * rdi], 0x01              | 66 d1 0c 38                   |
    | ror word [rax + 1 * r8], 0x01               | 66 42 d1 0c 00                |
    | ror word [rax + 1 * r9], 0x01               | 66 42 d1 0c 08                |
    | ror word [rax + 1 * r10], 0x01              | 66 42 d1 0c 10                |
    | ror word [rax + 1 * r11], 0x01              | 66 42 d1 0c 18                |
    | ror word [rax + 1 * r12], 0x01              | 66 42 d1 0c 20                |
    | ror word [rax + 1 * r13], 0x01              | 66 42 d1 0c 28                |
    | ror word [rax + 1 * r14], 0x01              | 66 42 d1 0c 30                |
    | ror word [rax + 1 * r15], 0x01              | 66 42 d1 0c 38                |
    | ror word [rax + 2 * rcx], 0x01              | 66 d1 0c 48                   |
    | ror word [rax + 4 * rcx], 0x01              | 66 d1 0c 88                   |
    | ror word [rax + 8 * rcx], 0x01              | 66 d1 0c c8                   |
    | ror word [r8 + 1 * r9], 0x01                | 66 43 d1 0c 08                |
    | ror word [r8 + 2 * r9], 0x01                | 66 43 d1 0c 48                |
    | ror word [r8 + 4 * r9], 0x01                | 66 43 d1 0c 88                |
    | ror word [r8 + 8 * r9], 0x01                | 66 43 d1 0c c8                |
    | ror word [1 * rcx], 0x01                    | 66 d1 0c 0d 00 00 00 00       |
    | ror word [2 * rcx], 0x01                    | 66 d1 0c 4d 00 00 00 00       |
    | ror word [4 * rcx], 0x01                    | 66 d1 0c 8d 00 00 00 00       |
    | ror word [8 * rcx], 0x01                    | 66 d1 0c cd 00 00 00 00       |
    | ror word [1 * r9], 0x01                     | 66 42 d1 0c 0d 00 00 00 00    |
    | ror word [2 * r9], 0x01                     | 66 42 d1 0c 4d 00 00 00 00    |
    | ror word [4 * r9], 0x01                     | 66 42 d1 0c 8d 00 00 00 00    |
    | ror word [8 * r9], 0x01                     | 66 42 d1 0c cd 00 00 00 00    |
    | ror word [r13 + 8 * r12], 0x01              | 66 43 d1 4c e5 00             |
    | ror word [rsp + 4 * r15], 0x01              | 66 42 d1 0c bc                |
    | ror word [rax + 1 * rcx + 0x00], 0x01       | 66 d1 4c 08 00                |
    | ror word [rax + 1 * rcx - 0x00], 0x01       | 66 d1 4c 08 00                |
    | ror word [rax + 1 * rcx + 0x01], 0x01       | 66 d1 4c 08 01                |
    | ror word [rax + 1 * rcx - 0x01], 0x01       | 66 d1 4c 08 ff                |
    | ror word [rax + 1 * rcx + 0x00000001], 0x01 | 66 d1 8c 08 01 00 00 00       |
    | ror word [rax + 1 * rcx - 0x00000001], 0x01 | 66 d1 8c 08 ff ff ff ff       |
    | ror word [rax + 1 * rcx + 0x7f], 0x01       | 66 d1 4c 08 7f                |
    | ror word [rax + 1 * rcx - 0x7f], 0x01       | 66 d1 4c 08 81                |
    | ror word [rax + 1 * rcx + 0x80], 0x01       | 66 d1 8c 08 80 00 00 00       |
    | ror word [rax + 1 * rcx - 0x80], 0x01       | 66 d1 4c 08 80                |
    | ror word [rax + 1 * rcx - 0x81], 0x01       | 66 d1 8c 08 7f ff ff ff       |
    | ror word [rax + 1 * rcx + 0xff], 0x01       | 66 d1 8c 08 ff 00 00 00       |
    | ror word [rax + 1 * rcx - 0xff], 0x01       | 66 d1 8c 08 01 ff ff ff       |
    | ror word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 d1 8c 08 ff ff ff 7f       |
    | ror word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 d1 8c 08 01 00 00 80       |
    | ror word [rax + 1 * rcx - 0x80000000], 0x01 | 66 d1 8c 08 00 00 00 80       |
    | ror word [r10 + 0x7f], 0x01                 | 66 41 d1 4a 7f                |
    | ror word [r10 + 0x80], 0x01                 | 66 41 d1 8a 80 00 00 00       |
    | ror word [r10 - 0x80], 0x01                 | 66 41 d1 4a 80                |
    | ror word [r10 - 0x81], 0x01                 | 66 41 d1 8a 7f ff ff ff       |
    | ror word [rax], 0x00                        | 66 c1 08 00                   |
    | ror word [rax], 0x7f                        | 66 c1 08 7f                   |
    | ror word [rax], 0x80                        | 66 c1 08 80                   |
    | ror word [rax], 0xff                        | 66 c1 08 ff                   |
    | ror word [rcx], 0x7f                        | 66 c1 09 7f                   |
    | ror word [rdx], 0x80                        | 66 c1 0a 80                   |
    | ror word [rbx], 0xff                        | 66 c1 0b ff                   |
    | ror word [rsp], 0x00                        | 66 c1 0c 24 00                |
    | ror word [rsi], 0x7f                        | 66 c1 0e 7f                   |
    | ror word [rdi], 0x80                        | 66 c1 0f 80                   |
    | ror word [r8], 0xff                         | 66 41 c1 08 ff                |
    | ror word [r9], 0x00                         | 66 41 c1 09 00                |
    | ror word [r11], 0x7f                        | 66 41 c1 0b 7f                |
    | ror word [r12], 0x80                        | 66 41 c1 0c 24 80             |
    | ror word [r13], 0xff                        | 66 41 c1 4d 00 ff             |
    | ror word [r14], 0x00                        | 66 41 c1 0e 00                |
    | ror word [rax + 1 * rcx], 0x7f              | 66 c1 0c 08 7f                |
    | ror word [rcx + 1 * rcx], 0x80              | 66 c1 0c 09 80                |
    | ror word [rdx + 1 * rcx], 0xff              | 66 c1 0c 0a ff                |
    | ror word [rbx + 1 * rcx], 0x00              | 66 c1 0c 0b 00                |
    | ror word [rbp + 1 * rcx], 0x7f              | 66 c1 4c 0d 00 7f             |
    | ror word [rsi + 1 * rcx], 0x80              | 66 c1 0c 0e 80                |
    | ror word [rdi + 1 * rcx], 0xff              | 66 c1 0c 0f ff                |
    | ror word [r8 + 1 * rcx], 0x00               | 66 41 c1 0c 08 00             |
    | ror word [r10 + 1 * rcx], 0x7f              | 66 41 c1 0c 0a 7f             |
    | ror word [r11 + 1 * rcx], 0x80              | 66 41 c1 0c 0b 80             |
    | ror word [r12 + 1 * rcx], 0xff              | 66 41 c1 0c 0c ff             |
    | ror word [r13 + 1 * rcx], 0x00              | 66 41 c1 4c 0d 00 00          |
    | ror word [r15 + 1 * rcx], 0x7f              | 66 41 c1 0c 0f 7f             |
    | ror word [rax + 1 * rax], 0x80              | 66 c1 0c 00 80                |
    | ror word [rax + 1 * rdx], 0xff              | 66 c1 0c 10 ff                |
    | ror word [rax + 1 * rbx], 0x00              | 66 c1 0c 18 00                |
    | ror word [rax + 1 * rsi], 0x7f              | 66 c1 0c 30 7f                |
    | ror word [rax + 1 * rdi], 0x80              | 66 c1 0c 38 80                |
    | ror word [rax + 1 * r8], 0xff               | 66 42 c1 0c 00 ff             |
    | ror word [rax + 1 * r9], 0x00               | 66 42 c1 0c 08 00             |
    | ror word [rax + 1 * r11], 0x7f              | 66 42 c1 0c 18 7f             |
    | ror word [rax + 1 * r12], 0x80              | 66 42 c1 0c 20 80             |
    | ror word [rax + 1 * r13], 0xff              | 66 42 c1 0c 28 ff             |
    | ror word [rax + 1 * r14], 0x00              | 66 42 c1 0c 30 00             |
    | ror word [rax + 2 * rcx], 0x7f              | 66 c1 0c 48 7f                |
    | ror word [rax + 4 * rcx], 0x80              | 66 c1 0c 88 80                |
    | ror word [rax + 8 * rcx], 0xff              | 66 c1 0c c8 ff                |
    | ror word [r8 + 1 * r9], 0x00                | 66 43 c1 0c 08 00             |
    | ror word [r8 + 4 * r9], 0x7f                | 66 43 c1 0c 88 7f             |
    | ror word [r8 + 8 * r9], 0x80                | 66 43 c1 0c c8 80             |
    | ror word [1 * rcx], 0xff                    | 66 c1 0c 0d 00 00 00 00 ff    |
    | ror word [2 * rcx], 0x00                    | 66 c1 0c 4d 00 00 00 00 00    |
    | ror word [8 * rcx], 0x7f                    | 66 c1 0c cd 00 00 00 00 7f    |
    | ror word [1 * r9], 0x80                     | 66 42 c1 0c 0d 00 00 00 00 80 |
    | ror word [2 * r9], 0xff                     | 66 42 c1 0c 4d 00 00 00 00 ff |
    | ror word [4 * r9], 0x00                     | 66 42 c1 0c 8d 00 00 00 00 00 |
    | ror word [r13 + 8 * r12], 0x7f              | 66 43 c1 4c e5 00 7f          |
    | ror word [rsp + 4 * r15], 0x80              | 66 42 c1 0c bc 80             |
    | ror word [rax + 1 * rcx + 0x00], 0xff       | 66 c1 4c 08 00 ff             |
    | ror word [rax + 1 * rcx - 0x00], 0x00       | 66 c1 4c 08 00 00             |
    | ror word [rax + 1 * rcx - 0x01], 0x7f       | 66 c1 4c 08 ff 7f             |
    | ror word [rax + 1 * rcx + 0x00000001], 0x80 | 66 c1 8c 08 01 00 00 00 80    |
    | ror word [rax + 1 * rcx - 0x00000001], 0xff | 66 c1 8c 08 ff ff ff ff ff    |
    | ror word [rax + 1 * rcx + 0x7f], 0x00       | 66 c1 4c 08 7f 00             |
    | ror word [rax + 1 * rcx + 0x80], 0x7f       | 66 c1 8c 08 80 00 00 00 7f    |
    | ror word [rax + 1 * rcx - 0x80], 0x80       | 66 c1 4c 08 80 80             |
    | ror word [rax + 1 * rcx - 0x81], 0xff       | 66 c1 8c 08 7f ff ff ff ff    |
    | ror word [rax + 1 * rcx + 0xff], 0x00       | 66 c1 8c 08 ff 00 00 00 00    |
    | ror word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 c1 8c 08 ff ff ff 7f 7f    |
    | ror word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 c1 8c 08 01 00 00 80 80    |
    | ror word [rax + 1 * rcx - 0x80000000], 0xff | 66 c1 8c 08 00 00 00 80 ff    |
    | ror word [r10 + 0x7f], 0x00                 | 66 41 c1 4a 7f 00             |
    | ror word [r10 - 0x80], 0x7f                 | 66 41 c1 4a 80 7f             |
    | ror word [r10 - 0x81], 0x80                 | 66 41 c1 8a 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_ror_addr16_imm8():
    encode(ROR_ADDR16_IMM8)


ROR_ADDR16_CL = """
    | ----------------------------------------- | -------------------------- |
    | instruction                               | encoding                   |
    | ----------------------------------------- | -------------------------- |
    | ror word [rax], cl                        | 66 d3 08                   |
    | ror word [rcx], cl                        | 66 d3 09                   |
    | ror word [rdx], cl                        | 66 d3 0a                   |
    | ror word [rbx], cl                        | 66 d3 0b                   |
    | ror word [rsp], cl                        | 66 d3 0c 24                |
    | ror word [rbp], cl                        | 66 d3 4d 00                |
    | ror word [rsi], cl                        | 66 d3 0e                   |
    | ror word [rdi], cl                        | 66 d3 0f                   |
    | ror word [r8], cl                         | 66 41 d3 08                |
    | ror word [r9], cl                         | 66 41 d3 09                |
    | ror word [r10], cl                        | 66 41 d3 0a                |
    | ror word [r11], cl                        | 66 41 d3 0b                |
    | ror word [r12], cl                        | 66 41 d3 0c 24             |
    | ror word [r13], cl                        | 66 41 d3 4d 00             |
    | ror word [r14], cl                        | 66 41 d3 0e                |
    | ror word [r15], cl                        | 66 41 d3 0f                |
    | ror word [rax + 1 * rcx], cl              | 66 d3 0c 08                |
    | ror word [rcx + 1 * rcx], cl              | 66 d3 0c 09                |
    | ror word [rdx + 1 * rcx], cl              | 66 d3 0c 0a                |
    | ror word [rbx + 1 * rcx], cl              | 66 d3 0c 0b                |
    | ror word [rsp + 1 * rcx], cl              | 66 d3 0c 0c                |
    | ror word [rbp + 1 * rcx], cl              | 66 d3 4c 0d 00             |
    | ror word [rsi + 1 * rcx], cl              | 66 d3 0c 0e                |
    | ror word [rdi + 1 * rcx], cl              | 66 d3 0c 0f                |
    | ror word [r8 + 1 * rcx], cl               | 66 41 d3 0c 08             |
    | ror word [r9 + 1 * rcx], cl               | 66 41 d3 0c 09             |
    | ror word [r10 + 1 * rcx], cl              | 66 41 d3 0c 0a             |
    | ror word [r11 + 1 * rcx], cl              | 66 41 d3 0c 0b             |
    | ror word [r12 + 1 * rcx], cl              | 66 41 d3 0c 0c             |
    | ror word [r13 + 1 * rcx], cl              | 66 41 d3 4c 0d 00          |
    | ror word [r14 + 1 * rcx], cl              | 66 41 d3 0c 0e             |
    | ror word [r15 + 1 * rcx], cl              | 66 41 d3 0c 0f             |
    | ror word [rax + 1 * rax], cl              | 66 d3 0c 00                |
    | ror word [rax + 1 * rdx], cl              | 66 d3 0c 10                |
    | ror word [rax + 1 * rbx], cl              | 66 d3 0c 18                |
    | ror word [rax + 1 * rbp], cl              | 66 d3 0c 28                |
    | ror word [rax + 1 * rsi], cl              | 66 d3 0c 30                |
    | ror word [rax + 1 * rdi], cl              | 66 d3 0c 38                |
    | ror word [rax + 1 * r8], cl               | 66 42 d3 0c 00             |
    | ror word [rax + 1 * r9], cl               | 66 42 d3 0c 08             |
    | ror word [rax + 1 * r10], cl              | 66 42 d3 0c 10             |
    | ror word [rax + 1 * r11], cl              | 66 42 d3 0c 18             |
    | ror word [rax + 1 * r12], cl              | 66 42 d3 0c 20             |
    | ror word [rax + 1 * r13], cl              | 66 42 d3 0c 28             |
    | ror word [rax + 1 * r14], cl              | 66 42 d3 0c 30             |
    | ror word [rax + 1 * r15], cl              | 66 42 d3 0c 38             |
    | ror word [rax + 2 * rcx], cl              | 66 d3 0c 48                |
    | ror word [rax + 4 * rcx], cl              | 66 d3 0c 88                |
    | ror word [rax + 8 * rcx], cl              | 66 d3 0c c8                |
    | ror word [r8 + 1 * r9], cl                | 66 43 d3 0c 08             |
    | ror word [r8 + 2 * r9], cl                | 66 43 d3 0c 48             |
    | ror word [r8 + 4 * r9], cl                | 66 43 d3 0c 88             |
    | ror word [r8 + 8 * r9], cl                | 66 43 d3 0c c8             |
    | ror word [1 * rcx], cl                    | 66 d3 0c 0d 00 00 00 00    |
    | ror word [2 * rcx], cl                    | 66 d3 0c 4d 00 00 00 00    |
    | ror word [4 * rcx], cl                    | 66 d3 0c 8d 00 00 00 00    |
    | ror word [8 * rcx], cl                    | 66 d3 0c cd 00 00 00 00    |
    | ror word [1 * r9], cl                     | 66 42 d3 0c 0d 00 00 00 00 |
    | ror word [2 * r9], cl                     | 66 42 d3 0c 4d 00 00 00 00 |
    | ror word [4 * r9], cl                     | 66 42 d3 0c 8d 00 00 00 00 |
    | ror word [8 * r9], cl                     | 66 42 d3 0c cd 00 00 00 00 |
    | ror word [r13 + 8 * r12], cl              | 66 43 d3 4c e5 00          |
    | ror word [rsp + 4 * r15], cl              | 66 42 d3 0c bc             |
    | ror word [rax + 1 * rcx + 0x00], cl       | 66 d3 4c 08 00             |
    | ror word [rax + 1 * rcx - 0x00], cl       | 66 d3 4c 08 00             |
    | ror word [rax + 1 * rcx + 0x01], cl       | 66 d3 4c 08 01             |
    | ror word [rax + 1 * rcx - 0x01], cl       | 66 d3 4c 08 ff             |
    | ror word [rax + 1 * rcx + 0x00000001], cl | 66 d3 8c 08 01 00 00 00    |
    | ror word [rax + 1 * rcx - 0x00000001], cl | 66 d3 8c 08 ff ff ff ff    |
    | ror word [rax + 1 * rcx + 0x7f], cl       | 66 d3 4c 08 7f             |
    | ror word [rax + 1 * rcx - 0x7f], cl       | 66 d3 4c 08 81             |
    | ror word [rax + 1 * rcx + 0x80], cl       | 66 d3 8c 08 80 00 00 00    |
    | ror word [rax + 1 * rcx - 0x80], cl       | 66 d3 4c 08 80             |
    | ror word [rax + 1 * rcx - 0x81], cl       | 66 d3 8c 08 7f ff ff ff    |
    | ror word [rax + 1 * rcx + 0xff], cl       | 66 d3 8c 08 ff 00 00 00    |
    | ror word [rax + 1 * rcx - 0xff], cl       | 66 d3 8c 08 01 ff ff ff    |
    | ror word [rax + 1 * rcx + 0x7fffffff], cl | 66 d3 8c 08 ff ff ff 7f    |
    | ror word [rax + 1 * rcx - 0x7fffffff], cl | 66 d3 8c 08 01 00 00 80    |
    | ror word [rax + 1 * rcx - 0x80000000], cl | 66 d3 8c 08 00 00 00 80    |
    | ror word [r10 + 0x7f], cl                 | 66 41 d3 4a 7f             |
    | ror word [r10 + 0x80], cl                 | 66 41 d3 8a 80 00 00 00    |
    | ror word [r10 - 0x80], cl                 | 66 41 d3 4a 80             |
    | ror word [r10 - 0x81], cl                 | 66 41 d3 8a 7f ff ff ff    |
    | ----------------------------------------- | -------------------------- |
"""


def can_encode_ror_addr16_cl():
    encode(ROR_ADDR16_CL)


ROR_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | ror byte [rax], 0x01                        | d0 08                      |
    | ror byte [rcx], 0x01                        | d0 09                      |
    | ror byte [rdx], 0x01                        | d0 0a                      |
    | ror byte [rbx], 0x01                        | d0 0b                      |
    | ror byte [rsp], 0x01                        | d0 0c 24                   |
    | ror byte [rbp], 0x01                        | d0 4d 00                   |
    | ror byte [rsi], 0x01                        | d0 0e                      |
    | ror byte [rdi], 0x01                        | d0 0f                      |
    | ror byte [r8], 0x01                         | 41 d0 08                   |
    | ror byte [r9], 0x01                         | 41 d0 09                   |
    | ror byte [r10], 0x01                        | 41 d0 0a                   |
    | ror byte [r11], 0x01                        | 41 d0 0b                   |
    | ror byte [r12], 0x01                        | 41 d0 0c 24                |
    | ror byte [r13], 0x01                        | 41 d0 4d 00                |
    | ror byte [r14], 0x01                        | 41 d0 0e                   |
    | ror byte [r15], 0x01                        | 41 d0 0f                   |
    | ror byte [rax + 1 * rcx], 0x01              | d0 0c 08                   |
    | ror byte [rcx + 1 * rcx], 0x01              | d0 0c 09                   |
    | ror byte [rdx + 1 * rcx], 0x01              | d0 0c 0a                   |
    | ror byte [rbx + 1 * rcx], 0x01              | d0 0c 0b                   |
    | ror byte [rsp + 1 * rcx], 0x01              | d0 0c 0c                   |
    | ror byte [rbp + 1 * rcx], 0x01              | d0 4c 0d 00                |
    | ror byte [rsi + 1 * rcx], 0x01              | d0 0c 0e                   |
    | ror byte [rdi + 1 * rcx], 0x01              | d0 0c 0f                   |
    | ror byte [r8 + 1 * rcx], 0x01               | 41 d0 0c 08                |
    | ror byte [r9 + 1 * rcx], 0x01               | 41 d0 0c 09                |
    | ror byte [r10 + 1 * rcx], 0x01              | 41 d0 0c 0a                |
    | ror byte [r11 + 1 * rcx], 0x01              | 41 d0 0c 0b                |
    | ror byte [r12 + 1 * rcx], 0x01              | 41 d0 0c 0c                |
    | ror byte [r13 + 1 * rcx], 0x01              | 41 d0 4c 0d 00             |
    | ror byte [r14 + 1 * rcx], 0x01              | 41 d0 0c 0e                |
    | ror byte [r15 + 1 * rcx], 0x01              | 41 d0 0c 0f                |
    | ror byte [rax + 1 * rax], 0x01              | d0 0c 00                   |
    | ror byte [rax + 1 * rdx], 0x01              | d0 0c 10                   |
    | ror byte [rax + 1 * rbx], 0x01              | d0 0c 18                   |
    | ror byte [rax + 1 * rbp], 0x01              | d0 0c 28                   |
    | ror byte [rax + 1 * rsi], 0x01              | d0 0c 30                   |
    | ror byte [rax + 1 * rdi], 0x01              | d0 0c 38                   |
    | ror byte [rax + 1 * r8], 0x01               | 42 d0 0c 00                |
    | ror byte [rax + 1 * r9], 0x01               | 42 d0 0c 08                |
    | ror byte [rax + 1 * r10], 0x01              | 42 d0 0c 10                |
    | ror byte [rax + 1 * r11], 0x01              | 42 d0 0c 18                |
    | ror byte [rax + 1 * r12], 0x01              | 42 d0 0c 20                |
    | ror byte [rax + 1 * r13], 0x01              | 42 d0 0c 28                |
    | ror byte [rax + 1 * r14], 0x01              | 42 d0 0c 30                |
    | ror byte [rax + 1 * r15], 0x01              | 42 d0 0c 38                |
    | ror byte [rax + 2 * rcx], 0x01              | d0 0c 48                   |
    | ror byte [rax + 4 * rcx], 0x01              | d0 0c 88                   |
    | ror byte [rax + 8 * rcx], 0x01              | d0 0c c8                   |
    | ror byte [r8 + 1 * r9], 0x01                | 43 d0 0c 08                |
    | ror byte [r8 + 2 * r9], 0x01                | 43 d0 0c 48                |
    | ror byte [r8 + 4 * r9], 0x01                | 43 d0 0c 88                |
    | ror byte [r8 + 8 * r9], 0x01                | 43 d0 0c c8                |
    | ror byte [1 * rcx], 0x01                    | d0 0c 0d 00 00 00 00       |
    | ror byte [2 * rcx], 0x01                    | d0 0c 4d 00 00 00 00       |
    | ror byte [4 * rcx], 0x01                    | d0 0c 8d 00 00 00 00       |
    | ror byte [8 * rcx], 0x01                    | d0 0c cd 00 00 00 00       |
    | ror byte [1 * r9], 0x01                     | 42 d0 0c 0d 00 00 00 00    |
    | ror byte [2 * r9], 0x01                     | 42 d0 0c 4d 00 00 00 00    |
    | ror byte [4 * r9], 0x01                     | 42 d0 0c 8d 00 00 00 00    |
    | ror byte [8 * r9], 0x01                     | 42 d0 0c cd 00 00 00 00    |
    | ror byte [r13 + 8 * r12], 0x01              | 43 d0 4c e5 00             |
    | ror byte [rsp + 4 * r15], 0x01              | 42 d0 0c bc                |
    | ror byte [rax + 1 * rcx + 0x00], 0x01       | d0 4c 08 00                |
    | ror byte [rax + 1 * rcx - 0x00], 0x01       | d0 4c 08 00                |
    | ror byte [rax + 1 * rcx + 0x01], 0x01       | d0 4c 08 01                |
    | ror byte [rax + 1 * rcx - 0x01], 0x01       | d0 4c 08 ff                |
    | ror byte [rax + 1 * rcx + 0x00000001], 0x01 | d0 8c 08 01 00 00 00       |
    | ror byte [rax + 1 * rcx - 0x00000001], 0x01 | d0 8c 08 ff ff ff ff       |
    | ror byte [rax + 1 * rcx + 0x7f], 0x01       | d0 4c 08 7f                |
    | ror byte [rax + 1 * rcx - 0x7f], 0x01       | d0 4c 08 81                |
    | ror byte [rax + 1 * rcx + 0x80], 0x01       | d0 8c 08 80 00 00 00       |
    | ror byte [rax + 1 * rcx - 0x80], 0x01       | d0 4c 08 80                |
    | ror byte [rax + 1 * rcx - 0x81], 0x01       | d0 8c 08 7f ff ff ff       |
    | ror byte [rax + 1 * rcx + 0xff], 0x01       | d0 8c 08 ff 00 00 00       |
    | ror byte [rax + 1 * rcx - 0xff], 0x01       | d0 8c 08 01 ff ff ff       |
    | ror byte [rax + 1 * rcx + 0x7fffffff], 0x01 | d0 8c 08 ff ff ff 7f       |
    | ror byte [rax + 1 * rcx - 0x7fffffff], 0x01 | d0 8c 08 01 00 00 80       |
    | ror byte [rax + 1 * rcx - 0x80000000], 0x01 | d0 8c 08 00 00 00 80       |
    | ror byte [r10 + 0x7f], 0x01                 | 41 d0 4a 7f                |
    | ror byte [r10 + 0x80], 0x01                 | 41 d0 8a 80 00 00 00       |
    | ror byte [r10 - 0x80], 0x01                 | 41 d0 4a 80                |
    | ror byte [r10 - 0x81], 0x01                 | 41 d0 8a 7f ff ff ff       |
    | ror byte [rax], 0x00                        | c0 08 00                   |
    | ror byte [rax], 0x7f                        | c0 08 7f                   |
    | ror byte [rax], 0x80                        | c0 08 80                   |
    | ror byte [rax], 0xff                        | c0 08 ff                   |
    | ror byte [rcx], 0x7f                        | c0 09 7f                   |
    | ror byte [rdx], 0x80                        | c0 0a 80                   |
    | ror byte [rbx], 0xff                        | c0 0b ff                   |
    | ror byte [rsp], 0x00                        | c0 0c 24 00                |
    | ror byte [rsi], 0x7f                        | c0 0e 7f                   |
    | ror byte [rdi], 0x80                        | c0 0f 80                   |
    | ror byte [r8], 0xff                         | 41 c0 08 ff                |
    | ror byte [r9], 0x00                         | 41 c0 09 00                |
    | ror byte [r11], 0x7f                        | 41 c0 0b 7f                |
    | ror byte [r12], 0x80                        | 41 c0 0c 24 80             |
    | ror byte [r13], 0xff                        | 41 c0 4d 00 ff             |
    | ror byte [r14], 0x00                        | 41 c0 0e 00                |
    | ror byte [rax + 1 * rcx], 0x7f              | c0 0c 08 7f                |
    | ror byte [rcx + 1 * rcx], 0x80              | c0 0c 09 80                |
    | ror byte [rdx + 1 * rcx], 0xff              | c0 0c 0a ff                |
    | ror byte [rbx + 1 * rcx], 0x00              | c0 0c 0b 00                |
    | ror byte [rbp + 1 * rcx], 0x7f              | c0 4c 0d 00 7f             |
    | ror byte [rsi + 1 * rcx], 0x80              | c0 0c 0e 80                |
    | ror byte [rdi + 1 * rcx], 0xff              | c0 0c 0f ff                |
    | ror byte [r8 + 1 * rcx], 0x00               | 41 c0 0c 08 00             |
    | ror byte [r10 + 1 * rcx], 0x7f              | 41 c0 0c 0a 7f             |
    | ror byte [r11 + 1 * rcx], 0x80              | 41 c0 0c 0b 80             |
    | ror byte [r12 + 1 * rcx], 0xff              | 41 c0 0c 0c ff             |
    | ror byte [r13 + 1 * rcx], 0x00              | 41 c0 4c 0d 00 00          |
    | ror byte [r15 + 1 * rcx], 0x7f              | 41 c0 0c 0f 7f             |
    | ror byte [rax + 1 * rax], 0x80              | c0 0c 00 80                |
    | ror byte [rax + 1 * rdx], 0xff              | c0 0c 10 ff                |
    | ror byte [rax + 1 * rbx], 0x00              | c0 0c 18 00                |
    | ror byte [rax + 1 * rsi], 0x7f              | c0 0c 30 7f                |
    | ror byte [rax + 1 * rdi], 0x80              | c0 0c 38 80                |
    | ror byte [rax + 1 * r8], 0xff               | 42 c0 0c 00 ff             |
    | ror byte [rax + 1 * r9], 0x00               | 42 c0 0c 08 00             |
    | ror byte [rax + 1 * r11], 0x7f              | 42 c0 0c 18 7f             |
    | ror byte [rax + 1 * r12], 0x80              | 42 c0 0c 20 80             |
    | ror byte [rax + 1 * r13], 0xff              | 42 c0 0c 28 ff             |
    | ror byte [rax + 1 * r14], 0x00              | 42 c0 0c 30 00             |
    | ror byte [rax + 2 * rcx], 0x7f              | c0 0c 48 7f                |
    | ror byte [rax + 4 * rcx], 0x80              | c0 0c 88 80                |
    | ror byte [rax + 8 * rcx], 0xff              | c0 0c c8 ff                |
    | ror byte [r8 + 1 * r9], 0x00                | 43 c0 0c 08 00             |
    | ror byte [r8 + 4 * r9], 0x7f                | 43 c0 0c 88 7f             |
    | ror byte [r8 + 8 * r9], 0x80                | 43 c0 0c c8 80             |
    | ror byte [1 * rcx], 0xff                    | c0 0c 0d 00 00 00 00 ff    |
    | ror byte [2 * rcx], 0x00                    | c0 0c 4d 00 00 00 00 00    |
    | ror byte [8 * rcx], 0x7f                    | c0 0c cd 00 00 00 00 7f    |
    | ror byte [1 * r9], 0x80                     | 42 c0 0c 0d 00 00 00 00 80 |
    | ror byte [2 * r9], 0xff                     | 42 c0 0c 4d 00 00 00 00 ff |
    | ror byte [4 * r9], 0x00                     | 42 c0 0c 8d 00 00 00 00 00 |
    | ror byte [r13 + 8 * r12], 0x7f              | 43 c0 4c e5 00 7f          |
    | ror byte [rsp + 4 * r15], 0x80              | 42 c0 0c bc 80             |
    | ror byte [rax + 1 * rcx + 0x00], 0xff       | c0 4c 08 00 ff             |
    | ror byte [rax + 1 * rcx - 0x00], 0x00       | c0 4c 08 00 00             |
    | ror byte [rax + 1 * rcx - 0x01], 0x7f       | c0 4c 08 ff 7f             |
    | ror byte [rax + 1 * rcx + 0x00000001], 0x80 | c0 8c 08 01 00 00 00 80    |
    | ror byte [rax + 1 * rcx - 0x00000001], 0xff | c0 8c 08 ff ff ff ff ff    |
    | ror byte [rax + 1 * rcx + 0x7f], 0x00       | c0 4c 08 7f 00             |
    | ror byte [rax + 1 * rcx + 0x80], 0x7f       | c0 8c 08 80 00 00 00 7f    |
    | ror byte [rax + 1 * rcx - 0x80], 0x80       | c0 4c 08 80 80             |
    | ror byte [rax + 1 * rcx - 0x81], 0xff       | c0 8c 08 7f ff ff ff ff    |
    | ror byte [rax + 1 * rcx + 0xff], 0x00       | c0 8c 08 ff 00 00 00 00    |
    | ror byte [rax + 1 * rcx + 0x7fffffff], 0x7f | c0 8c 08 ff ff ff 7f 7f    |
    | ror byte [rax + 1 * rcx - 0x7fffffff], 0x80 | c0 8c 08 01 00 00 80 80    |
    | ror byte [rax + 1 * rcx - 0x80000000], 0xff | c0 8c 08 00 00 00 80 ff    |
    | ror byte [r10 + 0x7f], 0x00                 | 41 c0 4a 7f 00             |
    | ror byte [r10 - 0x80], 0x7f                 | 41 c0 4a 80 7f             |
    | ror byte [r10 - 0x81], 0x80                 | 41 c0 8a 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_ror_addr8_imm8():
    encode(ROR_ADDR8_IMM8)


ROR_ADDR8_CL = """
    | ----------------------------------------- | ----------------------- |
    | instruction                               | encoding                |
    | ----------------------------------------- | ----------------------- |
    | ror byte [rax], cl                        | d2 08                   |
    | ror byte [rcx], cl                        | d2 09                   |
    | ror byte [rdx], cl                        | d2 0a                   |
    | ror byte [rbx], cl                        | d2 0b                   |
    | ror byte [rsp], cl                        | d2 0c 24                |
    | ror byte [rbp], cl                        | d2 4d 00                |
    | ror byte [rsi], cl                        | d2 0e                   |
    | ror byte [rdi], cl                        | d2 0f                   |
    | ror byte [r8], cl                         | 41 d2 08                |
    | ror byte [r9], cl                         | 41 d2 09                |
    | ror byte [r10], cl                        | 41 d2 0a                |
    | ror byte [r11], cl                        | 41 d2 0b                |
    | ror byte [r12], cl                        | 41 d2 0c 24             |
    | ror byte [r13], cl                        | 41 d2 4d 00             |
    | ror byte [r14], cl                        | 41 d2 0e                |
    | ror byte [r15], cl                        | 41 d2 0f                |
    | ror byte [rax + 1 * rcx], cl              | d2 0c 08                |
    | ror byte [rcx + 1 * rcx], cl              | d2 0c 09                |
    | ror byte [rdx + 1 * rcx], cl              | d2 0c 0a                |
    | ror byte [rbx + 1 * rcx], cl              | d2 0c 0b                |
    | ror byte [rsp + 1 * rcx], cl              | d2 0c 0c                |
    | ror byte [rbp + 1 * rcx], cl              | d2 4c 0d 00             |
    | ror byte [rsi + 1 * rcx], cl              | d2 0c 0e                |
    | ror byte [rdi + 1 * rcx], cl              | d2 0c 0f                |
    | ror byte [r8 + 1 * rcx], cl               | 41 d2 0c 08             |
    | ror byte [r9 + 1 * rcx], cl               | 41 d2 0c 09             |
    | ror byte [r10 + 1 * rcx], cl              | 41 d2 0c 0a             |
    | ror byte [r11 + 1 * rcx], cl              | 41 d2 0c 0b             |
    | ror byte [r12 + 1 * rcx], cl              | 41 d2 0c 0c             |
    | ror byte [r13 + 1 * rcx], cl              | 41 d2 4c 0d 00          |
    | ror byte [r14 + 1 * rcx], cl              | 41 d2 0c 0e             |
    | ror byte [r15 + 1 * rcx], cl              | 41 d2 0c 0f             |
    | ror byte [rax + 1 * rax], cl              | d2 0c 00                |
    | ror byte [rax + 1 * rdx], cl              | d2 0c 10                |
    | ror byte [rax + 1 * rbx], cl              | d2 0c 18                |
    | ror byte [rax + 1 * rbp], cl              | d2 0c 28                |
    | ror byte [rax + 1 * rsi], cl              | d2 0c 30                |
    | ror byte [rax + 1 * rdi], cl              | d2 0c 38                |
    | ror byte [rax + 1 * r8], cl               | 42 d2 0c 00             |
    | ror byte [rax + 1 * r9], cl               | 42 d2 0c 08             |
    | ror byte [rax + 1 * r10], cl              | 42 d2 0c 10             |
    | ror byte [rax + 1 * r11], cl              | 42 d2 0c 18             |
    | ror byte [rax + 1 * r12], cl              | 42 d2 0c 20             |
    | ror byte [rax + 1 * r13], cl              | 42 d2 0c 28             |
    | ror byte [rax + 1 * r14], cl              | 42 d2 0c 30             |
    | ror byte [rax + 1 * r15], cl              | 42 d2 0c 38             |
    | ror byte [rax + 2 * rcx], cl              | d2 0c 48                |
    | ror byte [rax + 4 * rcx], cl              | d2 0c 88                |
    | ror byte [rax + 8 * rcx], cl              | d2 0c c8                |
    | ror byte [r8 + 1 * r9], cl                | 43 d2 0c 08             |
    | ror byte [r8 + 2 * r9], cl                | 43 d2 0c 48             |
    | ror byte [r8 + 4 * r9], cl                | 43 d2 0c 88             |
    | ror byte [r8 + 8 * r9], cl                | 43 d2 0c c8             |
    | ror byte [1 * rcx], cl                    | d2 0c 0d 00 00 00 00    |
    | ror byte [2 * rcx], cl                    | d2 0c 4d 00 00 00 00    |
    | ror byte [4 * rcx], cl                    | d2 0c 8d 00 00 00 00    |
    | ror byte [8 * rcx], cl                    | d2 0c cd 00 00 00 00    |
    | ror byte [1 * r9], cl                     | 42 d2 0c 0d 00 00 00 00 |
    | ror byte [2 * r9], cl                     | 42 d2 0c 4d 00 00 00 00 |
    | ror byte [4 * r9], cl                     | 42 d2 0c 8d 00 00 00 00 |
    | ror byte [8 * r9], cl                     | 42 d2 0c cd 00 00 00 00 |
    | ror byte [r13 + 8 * r12], cl              | 43 d2 4c e5 00          |
    | ror byte [rsp + 4 * r15], cl              | 42 d2 0c bc             |
    | ror byte [rax + 1 * rcx + 0x00], cl       | d2 4c 08 00             |
    | ror byte [rax + 1 * rcx - 0x00], cl       | d2 4c 08 00             |
    | ror byte [rax + 1 * rcx + 0x01], cl       | d2 4c 08 01             |
    | ror byte [rax + 1 * rcx - 0x01], cl       | d2 4c 08 ff             |
    | ror byte [rax + 1 * rcx + 0x00000001], cl | d2 8c 08 01 00 00 00    |
    | ror byte [rax + 1 * rcx - 0x00000001], cl | d2 8c 08 ff ff ff ff    |
    | ror byte [rax + 1 * rcx + 0x7f], cl       | d2 4c 08 7f             |
    | ror byte [rax + 1 * rcx - 0x7f], cl       | d2 4c 08 81             |
    | ror byte [rax + 1 * rcx + 0x80], cl       | d2 8c 08 80 00 00 00    |
    | ror byte [rax + 1 * rcx - 0x80], cl       | d2 4c 08 80             |
    | ror byte [rax + 1 * rcx - 0x81], cl       | d2 8c 08 7f ff ff ff    |
    | ror byte [rax + 1 * rcx + 0xff], cl       | d2 8c 08 ff 00 00 00    |
    | ror byte [rax + 1 * rcx - 0xff], cl       | d2 8c 08 01 ff ff ff    |
    | ror byte [rax + 1 * rcx + 0x7fffffff], cl | d2 8c 08 ff ff ff 7f    |
    | ror byte [rax + 1 * rcx - 0x7fffffff], cl | d2 8c 08 01 00 00 80    |
    | ror byte [rax + 1 * rcx - 0x80000000], cl | d2 8c 08 00 00 00 80    |
    | ror byte [r10 + 0x7f], cl                 | 41 d2 4a 7f             |
    | ror byte [r10 + 0x80], cl                 | 41 d2 8a 80 00 00 00    |
    | ror byte [r10 - 0x80], cl                 | 41 d2 4a 80             |
    | ror byte [r10 - 0x81], cl                 | 41 d2 8a 7f ff ff ff    |
    | ----------------------------------------- | ----------------------- |
"""


def can_encode_ror_addr8_cl():
    encode(ROR_ADDR8_CL)
