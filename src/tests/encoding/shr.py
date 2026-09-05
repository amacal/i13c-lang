from tests.encoding.core import encode, exhaust


def can_exhaust_shr():
    exhaust(
        SHR_ADDR16_CL,
        SHR_ADDR16_IMM8,
        SHR_ADDR32_CL,
        SHR_ADDR32_IMM8,
        SHR_ADDR64_CL,
        SHR_ADDR64_IMM8,
        SHR_ADDR8_CL,
        SHR_ADDR8_IMM8,
        SHR_REG16_CL,
        SHR_REG16_IMM8,
        SHR_REG32_CL,
        SHR_REG32_IMM8,
        SHR_REG64_CL,
        SHR_REG64_IMM8,
        SHR_REG8_CL,
        SHR_REG8_IMM8,
    )


SHR_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | shr rax, 0x01 | 48 d1 e8    | *** | shr rax, 0x00 | 48 c1 e8 00 |
    | shr rcx, 0x01 | 48 d1 e9    | *** | shr rax, 0x7f | 48 c1 e8 7f |
    | shr rdx, 0x01 | 48 d1 ea    | *** | shr rax, 0x80 | 48 c1 e8 80 |
    | shr rbx, 0x01 | 48 d1 eb    | *** | shr rax, 0xff | 48 c1 e8 ff |
    | shr rsp, 0x01 | 48 d1 ec    | *** | shr rcx, 0x7f | 48 c1 e9 7f |
    | shr rbp, 0x01 | 48 d1 ed    | *** | shr rdx, 0x80 | 48 c1 ea 80 |
    | shr rsi, 0x01 | 48 d1 ee    | *** | shr rbx, 0xff | 48 c1 eb ff |
    | shr rdi, 0x01 | 48 d1 ef    | *** | shr rsp, 0x00 | 48 c1 ec 00 |
    | shr r8, 0x01  | 49 d1 e8    | *** | shr rsi, 0x7f | 48 c1 ee 7f |
    | shr r9, 0x01  | 49 d1 e9    | *** | shr rdi, 0x80 | 48 c1 ef 80 |
    | shr r10, 0x01 | 49 d1 ea    | *** | shr r8, 0xff  | 49 c1 e8 ff |
    | shr r11, 0x01 | 49 d1 eb    | *** | shr r9, 0x00  | 49 c1 e9 00 |
    | shr r12, 0x01 | 49 d1 ec    | *** | shr r11, 0x7f | 49 c1 eb 7f |
    | shr r13, 0x01 | 49 d1 ed    | *** | shr r12, 0x80 | 49 c1 ec 80 |
    | shr r14, 0x01 | 49 d1 ee    | *** | shr r13, 0xff | 49 c1 ed ff |
    | shr r15, 0x01 | 49 d1 ef    | *** | shr r14, 0x00 | 49 c1 ee 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_shr_reg64_imm8():
    encode(SHR_REG64_IMM8)


SHR_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | shr rax, cl | 48 d3 e8 | *** | shr r8, cl  | 49 d3 e8 |
    | shr rcx, cl | 48 d3 e9 | *** | shr r9, cl  | 49 d3 e9 |
    | shr rdx, cl | 48 d3 ea | *** | shr r10, cl | 49 d3 ea |
    | shr rbx, cl | 48 d3 eb | *** | shr r11, cl | 49 d3 eb |
    | shr rsp, cl | 48 d3 ec | *** | shr r12, cl | 49 d3 ec |
    | shr rbp, cl | 48 d3 ed | *** | shr r13, cl | 49 d3 ed |
    | shr rsi, cl | 48 d3 ee | *** | shr r14, cl | 49 d3 ee |
    | shr rdi, cl | 48 d3 ef | *** | shr r15, cl | 49 d3 ef |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_shr_reg64_cl():
    encode(SHR_REG64_CL)


SHR_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | shr eax, 0x01  | d1 e8       | *** | shr eax, 0x00  | c1 e8 00    |
    | shr ecx, 0x01  | d1 e9       | *** | shr eax, 0x7f  | c1 e8 7f    |
    | shr edx, 0x01  | d1 ea       | *** | shr eax, 0x80  | c1 e8 80    |
    | shr ebx, 0x01  | d1 eb       | *** | shr eax, 0xff  | c1 e8 ff    |
    | shr esp, 0x01  | d1 ec       | *** | shr ecx, 0x7f  | c1 e9 7f    |
    | shr ebp, 0x01  | d1 ed       | *** | shr edx, 0x80  | c1 ea 80    |
    | shr esi, 0x01  | d1 ee       | *** | shr ebx, 0xff  | c1 eb ff    |
    | shr edi, 0x01  | d1 ef       | *** | shr esp, 0x00  | c1 ec 00    |
    | shr r8d, 0x01  | 41 d1 e8    | *** | shr esi, 0x7f  | c1 ee 7f    |
    | shr r9d, 0x01  | 41 d1 e9    | *** | shr edi, 0x80  | c1 ef 80    |
    | shr r10d, 0x01 | 41 d1 ea    | *** | shr r8d, 0xff  | 41 c1 e8 ff |
    | shr r11d, 0x01 | 41 d1 eb    | *** | shr r9d, 0x00  | 41 c1 e9 00 |
    | shr r12d, 0x01 | 41 d1 ec    | *** | shr r11d, 0x7f | 41 c1 eb 7f |
    | shr r13d, 0x01 | 41 d1 ed    | *** | shr r12d, 0x80 | 41 c1 ec 80 |
    | shr r14d, 0x01 | 41 d1 ee    | *** | shr r13d, 0xff | 41 c1 ed ff |
    | shr r15d, 0x01 | 41 d1 ef    | *** | shr r14d, 0x00 | 41 c1 ee 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_shr_reg32_imm8():
    encode(SHR_REG32_IMM8)


SHR_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | shr eax, cl  | d3 e8    | *** | shr r8d, cl  | 41 d3 e8 |
    | shr ecx, cl  | d3 e9    | *** | shr r9d, cl  | 41 d3 e9 |
    | shr edx, cl  | d3 ea    | *** | shr r10d, cl | 41 d3 ea |
    | shr ebx, cl  | d3 eb    | *** | shr r11d, cl | 41 d3 eb |
    | shr esp, cl  | d3 ec    | *** | shr r12d, cl | 41 d3 ec |
    | shr ebp, cl  | d3 ed    | *** | shr r13d, cl | 41 d3 ed |
    | shr esi, cl  | d3 ee    | *** | shr r14d, cl | 41 d3 ee |
    | shr edi, cl  | d3 ef    | *** | shr r15d, cl | 41 d3 ef |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_shr_reg32_cl():
    encode(SHR_REG32_CL)


SHR_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | shr ax, 0x01   | 66 d1 e8       | *** | shr ax, 0x00   | 66 c1 e8 00    |
    | shr cx, 0x01   | 66 d1 e9       | *** | shr ax, 0x7f   | 66 c1 e8 7f    |
    | shr dx, 0x01   | 66 d1 ea       | *** | shr ax, 0x80   | 66 c1 e8 80    |
    | shr bx, 0x01   | 66 d1 eb       | *** | shr ax, 0xff   | 66 c1 e8 ff    |
    | shr sp, 0x01   | 66 d1 ec       | *** | shr cx, 0x7f   | 66 c1 e9 7f    |
    | shr bp, 0x01   | 66 d1 ed       | *** | shr dx, 0x80   | 66 c1 ea 80    |
    | shr si, 0x01   | 66 d1 ee       | *** | shr bx, 0xff   | 66 c1 eb ff    |
    | shr di, 0x01   | 66 d1 ef       | *** | shr sp, 0x00   | 66 c1 ec 00    |
    | shr r8w, 0x01  | 66 41 d1 e8    | *** | shr si, 0x7f   | 66 c1 ee 7f    |
    | shr r9w, 0x01  | 66 41 d1 e9    | *** | shr di, 0x80   | 66 c1 ef 80    |
    | shr r10w, 0x01 | 66 41 d1 ea    | *** | shr r8w, 0xff  | 66 41 c1 e8 ff |
    | shr r11w, 0x01 | 66 41 d1 eb    | *** | shr r9w, 0x00  | 66 41 c1 e9 00 |
    | shr r12w, 0x01 | 66 41 d1 ec    | *** | shr r11w, 0x7f | 66 41 c1 eb 7f |
    | shr r13w, 0x01 | 66 41 d1 ed    | *** | shr r12w, 0x80 | 66 41 c1 ec 80 |
    | shr r14w, 0x01 | 66 41 d1 ee    | *** | shr r13w, 0xff | 66 41 c1 ed ff |
    | shr r15w, 0x01 | 66 41 d1 ef    | *** | shr r14w, 0x00 | 66 41 c1 ee 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_shr_reg16_imm8():
    encode(SHR_REG16_IMM8)


SHR_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | shr ax, cl   | 66 d3 e8    | *** | shr r8w, cl  | 66 41 d3 e8 |
    | shr cx, cl   | 66 d3 e9    | *** | shr r9w, cl  | 66 41 d3 e9 |
    | shr dx, cl   | 66 d3 ea    | *** | shr r10w, cl | 66 41 d3 ea |
    | shr bx, cl   | 66 d3 eb    | *** | shr r11w, cl | 66 41 d3 eb |
    | shr sp, cl   | 66 d3 ec    | *** | shr r12w, cl | 66 41 d3 ec |
    | shr bp, cl   | 66 d3 ed    | *** | shr r13w, cl | 66 41 d3 ed |
    | shr si, cl   | 66 d3 ee    | *** | shr r14w, cl | 66 41 d3 ee |
    | shr di, cl   | 66 d3 ef    | *** | shr r15w, cl | 66 41 d3 ef |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_shr_reg16_cl():
    encode(SHR_REG16_CL)


SHR_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | shr al, 0x01   | d0 e8       | *** | shr al, 0x00   | c0 e8 00    |
    | shr cl, 0x01   | d0 e9       | *** | shr al, 0x7f   | c0 e8 7f    |
    | shr dl, 0x01   | d0 ea       | *** | shr al, 0x80   | c0 e8 80    |
    | shr bl, 0x01   | d0 eb       | *** | shr al, 0xff   | c0 e8 ff    |
    | shr spl, 0x01  | 40 d0 ec    | *** | shr cl, 0x7f   | c0 e9 7f    |
    | shr bpl, 0x01  | 40 d0 ed    | *** | shr dl, 0x80   | c0 ea 80    |
    | shr sil, 0x01  | 40 d0 ee    | *** | shr bl, 0xff   | c0 eb ff    |
    | shr dil, 0x01  | 40 d0 ef    | *** | shr spl, 0x00  | 40 c0 ec 00 |
    | shr r8b, 0x01  | 41 d0 e8    | *** | shr sil, 0x7f  | 40 c0 ee 7f |
    | shr r9b, 0x01  | 41 d0 e9    | *** | shr dil, 0x80  | 40 c0 ef 80 |
    | shr r10b, 0x01 | 41 d0 ea    | *** | shr r8b, 0xff  | 41 c0 e8 ff |
    | shr r11b, 0x01 | 41 d0 eb    | *** | shr r9b, 0x00  | 41 c0 e9 00 |
    | shr r12b, 0x01 | 41 d0 ec    | *** | shr r11b, 0x7f | 41 c0 eb 7f |
    | shr r13b, 0x01 | 41 d0 ed    | *** | shr r12b, 0x80 | 41 c0 ec 80 |
    | shr r14b, 0x01 | 41 d0 ee    | *** | shr r13b, 0xff | 41 c0 ed ff |
    | shr r15b, 0x01 | 41 d0 ef    | *** | shr r14b, 0x00 | 41 c0 ee 00 |
    | shr ah, 0x01   | d0 ec       | *** | shr ah, 0x7f   | c0 ec 7f    |
    | shr ch, 0x01   | d0 ed       | *** | shr ch, 0x80   | c0 ed 80    |
    | shr dh, 0x01   | d0 ee       | *** | shr dh, 0xff   | c0 ee ff    |
    | shr bh, 0x01   | d0 ef       | *** | shr bh, 0x00   | c0 ef 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_shr_reg8_imm8():
    encode(SHR_REG8_IMM8)


SHR_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | shr al, cl   | d2 e8    | *** | shr r10b, cl | 41 d2 ea |
    | shr cl, cl   | d2 e9    | *** | shr r11b, cl | 41 d2 eb |
    | shr dl, cl   | d2 ea    | *** | shr r12b, cl | 41 d2 ec |
    | shr bl, cl   | d2 eb    | *** | shr r13b, cl | 41 d2 ed |
    | shr spl, cl  | 40 d2 ec | *** | shr r14b, cl | 41 d2 ee |
    | shr bpl, cl  | 40 d2 ed | *** | shr r15b, cl | 41 d2 ef |
    | shr sil, cl  | 40 d2 ee | *** | shr ah, cl   | d2 ec    |
    | shr dil, cl  | 40 d2 ef | *** | shr ch, cl   | d2 ed    |
    | shr r8b, cl  | 41 d2 e8 | *** | shr dh, cl   | d2 ee    |
    | shr r9b, cl  | 41 d2 e9 | *** | shr bh, cl   | d2 ef    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_shr_reg8_cl():
    encode(SHR_REG8_CL)


SHR_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | shr qword [rax], 0x01                        | 48 d1 28                   |
    | shr qword [rcx], 0x01                        | 48 d1 29                   |
    | shr qword [rdx], 0x01                        | 48 d1 2a                   |
    | shr qword [rbx], 0x01                        | 48 d1 2b                   |
    | shr qword [rsp], 0x01                        | 48 d1 2c 24                |
    | shr qword [rbp], 0x01                        | 48 d1 6d 00                |
    | shr qword [rsi], 0x01                        | 48 d1 2e                   |
    | shr qword [rdi], 0x01                        | 48 d1 2f                   |
    | shr qword [r8], 0x01                         | 49 d1 28                   |
    | shr qword [r9], 0x01                         | 49 d1 29                   |
    | shr qword [r10], 0x01                        | 49 d1 2a                   |
    | shr qword [r11], 0x01                        | 49 d1 2b                   |
    | shr qword [r12], 0x01                        | 49 d1 2c 24                |
    | shr qword [r13], 0x01                        | 49 d1 6d 00                |
    | shr qword [r14], 0x01                        | 49 d1 2e                   |
    | shr qword [r15], 0x01                        | 49 d1 2f                   |
    | shr qword [rax + 1 * rcx], 0x01              | 48 d1 2c 08                |
    | shr qword [rcx + 1 * rcx], 0x01              | 48 d1 2c 09                |
    | shr qword [rdx + 1 * rcx], 0x01              | 48 d1 2c 0a                |
    | shr qword [rbx + 1 * rcx], 0x01              | 48 d1 2c 0b                |
    | shr qword [rsp + 1 * rcx], 0x01              | 48 d1 2c 0c                |
    | shr qword [rbp + 1 * rcx], 0x01              | 48 d1 6c 0d 00             |
    | shr qword [rsi + 1 * rcx], 0x01              | 48 d1 2c 0e                |
    | shr qword [rdi + 1 * rcx], 0x01              | 48 d1 2c 0f                |
    | shr qword [r8 + 1 * rcx], 0x01               | 49 d1 2c 08                |
    | shr qword [r9 + 1 * rcx], 0x01               | 49 d1 2c 09                |
    | shr qword [r10 + 1 * rcx], 0x01              | 49 d1 2c 0a                |
    | shr qword [r11 + 1 * rcx], 0x01              | 49 d1 2c 0b                |
    | shr qword [r12 + 1 * rcx], 0x01              | 49 d1 2c 0c                |
    | shr qword [r13 + 1 * rcx], 0x01              | 49 d1 6c 0d 00             |
    | shr qword [r14 + 1 * rcx], 0x01              | 49 d1 2c 0e                |
    | shr qword [r15 + 1 * rcx], 0x01              | 49 d1 2c 0f                |
    | shr qword [rax + 1 * rax], 0x01              | 48 d1 2c 00                |
    | shr qword [rax + 1 * rdx], 0x01              | 48 d1 2c 10                |
    | shr qword [rax + 1 * rbx], 0x01              | 48 d1 2c 18                |
    | shr qword [rax + 1 * rbp], 0x01              | 48 d1 2c 28                |
    | shr qword [rax + 1 * rsi], 0x01              | 48 d1 2c 30                |
    | shr qword [rax + 1 * rdi], 0x01              | 48 d1 2c 38                |
    | shr qword [rax + 1 * r8], 0x01               | 4a d1 2c 00                |
    | shr qword [rax + 1 * r9], 0x01               | 4a d1 2c 08                |
    | shr qword [rax + 1 * r10], 0x01              | 4a d1 2c 10                |
    | shr qword [rax + 1 * r11], 0x01              | 4a d1 2c 18                |
    | shr qword [rax + 1 * r12], 0x01              | 4a d1 2c 20                |
    | shr qword [rax + 1 * r13], 0x01              | 4a d1 2c 28                |
    | shr qword [rax + 1 * r14], 0x01              | 4a d1 2c 30                |
    | shr qword [rax + 1 * r15], 0x01              | 4a d1 2c 38                |
    | shr qword [rax + 2 * rcx], 0x01              | 48 d1 2c 48                |
    | shr qword [rax + 4 * rcx], 0x01              | 48 d1 2c 88                |
    | shr qword [rax + 8 * rcx], 0x01              | 48 d1 2c c8                |
    | shr qword [r8 + 1 * r9], 0x01                | 4b d1 2c 08                |
    | shr qword [r8 + 2 * r9], 0x01                | 4b d1 2c 48                |
    | shr qword [r8 + 4 * r9], 0x01                | 4b d1 2c 88                |
    | shr qword [r8 + 8 * r9], 0x01                | 4b d1 2c c8                |
    | shr qword [1 * rcx], 0x01                    | 48 d1 2c 0d 00 00 00 00    |
    | shr qword [2 * rcx], 0x01                    | 48 d1 2c 4d 00 00 00 00    |
    | shr qword [4 * rcx], 0x01                    | 48 d1 2c 8d 00 00 00 00    |
    | shr qword [8 * rcx], 0x01                    | 48 d1 2c cd 00 00 00 00    |
    | shr qword [1 * r9], 0x01                     | 4a d1 2c 0d 00 00 00 00    |
    | shr qword [2 * r9], 0x01                     | 4a d1 2c 4d 00 00 00 00    |
    | shr qword [4 * r9], 0x01                     | 4a d1 2c 8d 00 00 00 00    |
    | shr qword [8 * r9], 0x01                     | 4a d1 2c cd 00 00 00 00    |
    | shr qword [r13 + 8 * r12], 0x01              | 4b d1 6c e5 00             |
    | shr qword [rsp + 4 * r15], 0x01              | 4a d1 2c bc                |
    | shr qword [rax + 1 * rcx + 0x00], 0x01       | 48 d1 6c 08 00             |
    | shr qword [rax + 1 * rcx - 0x00], 0x01       | 48 d1 6c 08 00             |
    | shr qword [rax + 1 * rcx + 0x01], 0x01       | 48 d1 6c 08 01             |
    | shr qword [rax + 1 * rcx - 0x01], 0x01       | 48 d1 6c 08 ff             |
    | shr qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 d1 ac 08 01 00 00 00    |
    | shr qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 d1 ac 08 ff ff ff ff    |
    | shr qword [rax + 1 * rcx + 0x7f], 0x01       | 48 d1 6c 08 7f             |
    | shr qword [rax + 1 * rcx - 0x7f], 0x01       | 48 d1 6c 08 81             |
    | shr qword [rax + 1 * rcx + 0x80], 0x01       | 48 d1 ac 08 80 00 00 00    |
    | shr qword [rax + 1 * rcx - 0x80], 0x01       | 48 d1 6c 08 80             |
    | shr qword [rax + 1 * rcx - 0x81], 0x01       | 48 d1 ac 08 7f ff ff ff    |
    | shr qword [rax + 1 * rcx + 0xff], 0x01       | 48 d1 ac 08 ff 00 00 00    |
    | shr qword [rax + 1 * rcx - 0xff], 0x01       | 48 d1 ac 08 01 ff ff ff    |
    | shr qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 d1 ac 08 ff ff ff 7f    |
    | shr qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 d1 ac 08 01 00 00 80    |
    | shr qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 d1 ac 08 00 00 00 80    |
    | shr qword [r10 + 0x7f], 0x01                 | 49 d1 6a 7f                |
    | shr qword [r10 + 0x80], 0x01                 | 49 d1 aa 80 00 00 00       |
    | shr qword [r10 - 0x80], 0x01                 | 49 d1 6a 80                |
    | shr qword [r10 - 0x81], 0x01                 | 49 d1 aa 7f ff ff ff       |
    | shr qword [rax], 0x00                        | 48 c1 28 00                |
    | shr qword [rax], 0x7f                        | 48 c1 28 7f                |
    | shr qword [rax], 0x80                        | 48 c1 28 80                |
    | shr qword [rax], 0xff                        | 48 c1 28 ff                |
    | shr qword [rcx], 0x7f                        | 48 c1 29 7f                |
    | shr qword [rdx], 0x80                        | 48 c1 2a 80                |
    | shr qword [rbx], 0xff                        | 48 c1 2b ff                |
    | shr qword [rsp], 0x00                        | 48 c1 2c 24 00             |
    | shr qword [rsi], 0x7f                        | 48 c1 2e 7f                |
    | shr qword [rdi], 0x80                        | 48 c1 2f 80                |
    | shr qword [r8], 0xff                         | 49 c1 28 ff                |
    | shr qword [r9], 0x00                         | 49 c1 29 00                |
    | shr qword [r11], 0x7f                        | 49 c1 2b 7f                |
    | shr qword [r12], 0x80                        | 49 c1 2c 24 80             |
    | shr qword [r13], 0xff                        | 49 c1 6d 00 ff             |
    | shr qword [r14], 0x00                        | 49 c1 2e 00                |
    | shr qword [rax + 1 * rcx], 0x7f              | 48 c1 2c 08 7f             |
    | shr qword [rcx + 1 * rcx], 0x80              | 48 c1 2c 09 80             |
    | shr qword [rdx + 1 * rcx], 0xff              | 48 c1 2c 0a ff             |
    | shr qword [rbx + 1 * rcx], 0x00              | 48 c1 2c 0b 00             |
    | shr qword [rbp + 1 * rcx], 0x7f              | 48 c1 6c 0d 00 7f          |
    | shr qword [rsi + 1 * rcx], 0x80              | 48 c1 2c 0e 80             |
    | shr qword [rdi + 1 * rcx], 0xff              | 48 c1 2c 0f ff             |
    | shr qword [r8 + 1 * rcx], 0x00               | 49 c1 2c 08 00             |
    | shr qword [r10 + 1 * rcx], 0x7f              | 49 c1 2c 0a 7f             |
    | shr qword [r11 + 1 * rcx], 0x80              | 49 c1 2c 0b 80             |
    | shr qword [r12 + 1 * rcx], 0xff              | 49 c1 2c 0c ff             |
    | shr qword [r13 + 1 * rcx], 0x00              | 49 c1 6c 0d 00 00          |
    | shr qword [r15 + 1 * rcx], 0x7f              | 49 c1 2c 0f 7f             |
    | shr qword [rax + 1 * rax], 0x80              | 48 c1 2c 00 80             |
    | shr qword [rax + 1 * rdx], 0xff              | 48 c1 2c 10 ff             |
    | shr qword [rax + 1 * rbx], 0x00              | 48 c1 2c 18 00             |
    | shr qword [rax + 1 * rsi], 0x7f              | 48 c1 2c 30 7f             |
    | shr qword [rax + 1 * rdi], 0x80              | 48 c1 2c 38 80             |
    | shr qword [rax + 1 * r8], 0xff               | 4a c1 2c 00 ff             |
    | shr qword [rax + 1 * r9], 0x00               | 4a c1 2c 08 00             |
    | shr qword [rax + 1 * r11], 0x7f              | 4a c1 2c 18 7f             |
    | shr qword [rax + 1 * r12], 0x80              | 4a c1 2c 20 80             |
    | shr qword [rax + 1 * r13], 0xff              | 4a c1 2c 28 ff             |
    | shr qword [rax + 1 * r14], 0x00              | 4a c1 2c 30 00             |
    | shr qword [rax + 2 * rcx], 0x7f              | 48 c1 2c 48 7f             |
    | shr qword [rax + 4 * rcx], 0x80              | 48 c1 2c 88 80             |
    | shr qword [rax + 8 * rcx], 0xff              | 48 c1 2c c8 ff             |
    | shr qword [r8 + 1 * r9], 0x00                | 4b c1 2c 08 00             |
    | shr qword [r8 + 4 * r9], 0x7f                | 4b c1 2c 88 7f             |
    | shr qword [r8 + 8 * r9], 0x80                | 4b c1 2c c8 80             |
    | shr qword [1 * rcx], 0xff                    | 48 c1 2c 0d 00 00 00 00 ff |
    | shr qword [2 * rcx], 0x00                    | 48 c1 2c 4d 00 00 00 00 00 |
    | shr qword [8 * rcx], 0x7f                    | 48 c1 2c cd 00 00 00 00 7f |
    | shr qword [1 * r9], 0x80                     | 4a c1 2c 0d 00 00 00 00 80 |
    | shr qword [2 * r9], 0xff                     | 4a c1 2c 4d 00 00 00 00 ff |
    | shr qword [4 * r9], 0x00                     | 4a c1 2c 8d 00 00 00 00 00 |
    | shr qword [r13 + 8 * r12], 0x7f              | 4b c1 6c e5 00 7f          |
    | shr qword [rsp + 4 * r15], 0x80              | 4a c1 2c bc 80             |
    | shr qword [rax + 1 * rcx + 0x00], 0xff       | 48 c1 6c 08 00 ff          |
    | shr qword [rax + 1 * rcx - 0x00], 0x00       | 48 c1 6c 08 00 00          |
    | shr qword [rax + 1 * rcx - 0x01], 0x7f       | 48 c1 6c 08 ff 7f          |
    | shr qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 c1 ac 08 01 00 00 00 80 |
    | shr qword [rax + 1 * rcx - 0x00000001], 0xff | 48 c1 ac 08 ff ff ff ff ff |
    | shr qword [rax + 1 * rcx + 0x7f], 0x00       | 48 c1 6c 08 7f 00          |
    | shr qword [rax + 1 * rcx + 0x80], 0x7f       | 48 c1 ac 08 80 00 00 00 7f |
    | shr qword [rax + 1 * rcx - 0x80], 0x80       | 48 c1 6c 08 80 80          |
    | shr qword [rax + 1 * rcx - 0x81], 0xff       | 48 c1 ac 08 7f ff ff ff ff |
    | shr qword [rax + 1 * rcx + 0xff], 0x00       | 48 c1 ac 08 ff 00 00 00 00 |
    | shr qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 c1 ac 08 ff ff ff 7f 7f |
    | shr qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 c1 ac 08 01 00 00 80 80 |
    | shr qword [rax + 1 * rcx - 0x80000000], 0xff | 48 c1 ac 08 00 00 00 80 ff |
    | shr qword [r10 + 0x7f], 0x00                 | 49 c1 6a 7f 00             |
    | shr qword [r10 - 0x80], 0x7f                 | 49 c1 6a 80 7f             |
    | shr qword [r10 - 0x81], 0x80                 | 49 c1 aa 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_shr_addr64_imm8():
    encode(SHR_ADDR64_IMM8)


SHR_ADDR64_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | shr qword [rax], cl                        | 48 d3 28                |
    | shr qword [rcx], cl                        | 48 d3 29                |
    | shr qword [rdx], cl                        | 48 d3 2a                |
    | shr qword [rbx], cl                        | 48 d3 2b                |
    | shr qword [rsp], cl                        | 48 d3 2c 24             |
    | shr qword [rbp], cl                        | 48 d3 6d 00             |
    | shr qword [rsi], cl                        | 48 d3 2e                |
    | shr qword [rdi], cl                        | 48 d3 2f                |
    | shr qword [r8], cl                         | 49 d3 28                |
    | shr qword [r9], cl                         | 49 d3 29                |
    | shr qword [r10], cl                        | 49 d3 2a                |
    | shr qword [r11], cl                        | 49 d3 2b                |
    | shr qword [r12], cl                        | 49 d3 2c 24             |
    | shr qword [r13], cl                        | 49 d3 6d 00             |
    | shr qword [r14], cl                        | 49 d3 2e                |
    | shr qword [r15], cl                        | 49 d3 2f                |
    | shr qword [rax + 1 * rcx], cl              | 48 d3 2c 08             |
    | shr qword [rcx + 1 * rcx], cl              | 48 d3 2c 09             |
    | shr qword [rdx + 1 * rcx], cl              | 48 d3 2c 0a             |
    | shr qword [rbx + 1 * rcx], cl              | 48 d3 2c 0b             |
    | shr qword [rsp + 1 * rcx], cl              | 48 d3 2c 0c             |
    | shr qword [rbp + 1 * rcx], cl              | 48 d3 6c 0d 00          |
    | shr qword [rsi + 1 * rcx], cl              | 48 d3 2c 0e             |
    | shr qword [rdi + 1 * rcx], cl              | 48 d3 2c 0f             |
    | shr qword [r8 + 1 * rcx], cl               | 49 d3 2c 08             |
    | shr qword [r9 + 1 * rcx], cl               | 49 d3 2c 09             |
    | shr qword [r10 + 1 * rcx], cl              | 49 d3 2c 0a             |
    | shr qword [r11 + 1 * rcx], cl              | 49 d3 2c 0b             |
    | shr qword [r12 + 1 * rcx], cl              | 49 d3 2c 0c             |
    | shr qword [r13 + 1 * rcx], cl              | 49 d3 6c 0d 00          |
    | shr qword [r14 + 1 * rcx], cl              | 49 d3 2c 0e             |
    | shr qword [r15 + 1 * rcx], cl              | 49 d3 2c 0f             |
    | shr qword [rax + 1 * rax], cl              | 48 d3 2c 00             |
    | shr qword [rax + 1 * rdx], cl              | 48 d3 2c 10             |
    | shr qword [rax + 1 * rbx], cl              | 48 d3 2c 18             |
    | shr qword [rax + 1 * rbp], cl              | 48 d3 2c 28             |
    | shr qword [rax + 1 * rsi], cl              | 48 d3 2c 30             |
    | shr qword [rax + 1 * rdi], cl              | 48 d3 2c 38             |
    | shr qword [rax + 1 * r8], cl               | 4a d3 2c 00             |
    | shr qword [rax + 1 * r9], cl               | 4a d3 2c 08             |
    | shr qword [rax + 1 * r10], cl              | 4a d3 2c 10             |
    | shr qword [rax + 1 * r11], cl              | 4a d3 2c 18             |
    | shr qword [rax + 1 * r12], cl              | 4a d3 2c 20             |
    | shr qword [rax + 1 * r13], cl              | 4a d3 2c 28             |
    | shr qword [rax + 1 * r14], cl              | 4a d3 2c 30             |
    | shr qword [rax + 1 * r15], cl              | 4a d3 2c 38             |
    | shr qword [rax + 2 * rcx], cl              | 48 d3 2c 48             |
    | shr qword [rax + 4 * rcx], cl              | 48 d3 2c 88             |
    | shr qword [rax + 8 * rcx], cl              | 48 d3 2c c8             |
    | shr qword [r8 + 1 * r9], cl                | 4b d3 2c 08             |
    | shr qword [r8 + 2 * r9], cl                | 4b d3 2c 48             |
    | shr qword [r8 + 4 * r9], cl                | 4b d3 2c 88             |
    | shr qword [r8 + 8 * r9], cl                | 4b d3 2c c8             |
    | shr qword [1 * rcx], cl                    | 48 d3 2c 0d 00 00 00 00 |
    | shr qword [2 * rcx], cl                    | 48 d3 2c 4d 00 00 00 00 |
    | shr qword [4 * rcx], cl                    | 48 d3 2c 8d 00 00 00 00 |
    | shr qword [8 * rcx], cl                    | 48 d3 2c cd 00 00 00 00 |
    | shr qword [1 * r9], cl                     | 4a d3 2c 0d 00 00 00 00 |
    | shr qword [2 * r9], cl                     | 4a d3 2c 4d 00 00 00 00 |
    | shr qword [4 * r9], cl                     | 4a d3 2c 8d 00 00 00 00 |
    | shr qword [8 * r9], cl                     | 4a d3 2c cd 00 00 00 00 |
    | shr qword [r13 + 8 * r12], cl              | 4b d3 6c e5 00          |
    | shr qword [rsp + 4 * r15], cl              | 4a d3 2c bc             |
    | shr qword [rax + 1 * rcx + 0x00], cl       | 48 d3 6c 08 00          |
    | shr qword [rax + 1 * rcx - 0x00], cl       | 48 d3 6c 08 00          |
    | shr qword [rax + 1 * rcx + 0x01], cl       | 48 d3 6c 08 01          |
    | shr qword [rax + 1 * rcx - 0x01], cl       | 48 d3 6c 08 ff          |
    | shr qword [rax + 1 * rcx + 0x00000001], cl | 48 d3 ac 08 01 00 00 00 |
    | shr qword [rax + 1 * rcx - 0x00000001], cl | 48 d3 ac 08 ff ff ff ff |
    | shr qword [rax + 1 * rcx + 0x7f], cl       | 48 d3 6c 08 7f          |
    | shr qword [rax + 1 * rcx - 0x7f], cl       | 48 d3 6c 08 81          |
    | shr qword [rax + 1 * rcx + 0x80], cl       | 48 d3 ac 08 80 00 00 00 |
    | shr qword [rax + 1 * rcx - 0x80], cl       | 48 d3 6c 08 80          |
    | shr qword [rax + 1 * rcx - 0x81], cl       | 48 d3 ac 08 7f ff ff ff |
    | shr qword [rax + 1 * rcx + 0xff], cl       | 48 d3 ac 08 ff 00 00 00 |
    | shr qword [rax + 1 * rcx - 0xff], cl       | 48 d3 ac 08 01 ff ff ff |
    | shr qword [rax + 1 * rcx + 0x7fffffff], cl | 48 d3 ac 08 ff ff ff 7f |
    | shr qword [rax + 1 * rcx - 0x7fffffff], cl | 48 d3 ac 08 01 00 00 80 |
    | shr qword [rax + 1 * rcx - 0x80000000], cl | 48 d3 ac 08 00 00 00 80 |
    | shr qword [r10 + 0x7f], cl                 | 49 d3 6a 7f             |
    | shr qword [r10 + 0x80], cl                 | 49 d3 aa 80 00 00 00    |
    | shr qword [r10 - 0x80], cl                 | 49 d3 6a 80             |
    | shr qword [r10 - 0x81], cl                 | 49 d3 aa 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_shr_addr64_cl():
    encode(SHR_ADDR64_CL)


SHR_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | shr dword [rax], 0x01                        | d1 28                      |
    | shr dword [rcx], 0x01                        | d1 29                      |
    | shr dword [rdx], 0x01                        | d1 2a                      |
    | shr dword [rbx], 0x01                        | d1 2b                      |
    | shr dword [rsp], 0x01                        | d1 2c 24                   |
    | shr dword [rbp], 0x01                        | d1 6d 00                   |
    | shr dword [rsi], 0x01                        | d1 2e                      |
    | shr dword [rdi], 0x01                        | d1 2f                      |
    | shr dword [r8], 0x01                         | 41 d1 28                   |
    | shr dword [r9], 0x01                         | 41 d1 29                   |
    | shr dword [r10], 0x01                        | 41 d1 2a                   |
    | shr dword [r11], 0x01                        | 41 d1 2b                   |
    | shr dword [r12], 0x01                        | 41 d1 2c 24                |
    | shr dword [r13], 0x01                        | 41 d1 6d 00                |
    | shr dword [r14], 0x01                        | 41 d1 2e                   |
    | shr dword [r15], 0x01                        | 41 d1 2f                   |
    | shr dword [rax + 1 * rcx], 0x01              | d1 2c 08                   |
    | shr dword [rcx + 1 * rcx], 0x01              | d1 2c 09                   |
    | shr dword [rdx + 1 * rcx], 0x01              | d1 2c 0a                   |
    | shr dword [rbx + 1 * rcx], 0x01              | d1 2c 0b                   |
    | shr dword [rsp + 1 * rcx], 0x01              | d1 2c 0c                   |
    | shr dword [rbp + 1 * rcx], 0x01              | d1 6c 0d 00                |
    | shr dword [rsi + 1 * rcx], 0x01              | d1 2c 0e                   |
    | shr dword [rdi + 1 * rcx], 0x01              | d1 2c 0f                   |
    | shr dword [r8 + 1 * rcx], 0x01               | 41 d1 2c 08                |
    | shr dword [r9 + 1 * rcx], 0x01               | 41 d1 2c 09                |
    | shr dword [r10 + 1 * rcx], 0x01              | 41 d1 2c 0a                |
    | shr dword [r11 + 1 * rcx], 0x01              | 41 d1 2c 0b                |
    | shr dword [r12 + 1 * rcx], 0x01              | 41 d1 2c 0c                |
    | shr dword [r13 + 1 * rcx], 0x01              | 41 d1 6c 0d 00             |
    | shr dword [r14 + 1 * rcx], 0x01              | 41 d1 2c 0e                |
    | shr dword [r15 + 1 * rcx], 0x01              | 41 d1 2c 0f                |
    | shr dword [rax + 1 * rax], 0x01              | d1 2c 00                   |
    | shr dword [rax + 1 * rdx], 0x01              | d1 2c 10                   |
    | shr dword [rax + 1 * rbx], 0x01              | d1 2c 18                   |
    | shr dword [rax + 1 * rbp], 0x01              | d1 2c 28                   |
    | shr dword [rax + 1 * rsi], 0x01              | d1 2c 30                   |
    | shr dword [rax + 1 * rdi], 0x01              | d1 2c 38                   |
    | shr dword [rax + 1 * r8], 0x01               | 42 d1 2c 00                |
    | shr dword [rax + 1 * r9], 0x01               | 42 d1 2c 08                |
    | shr dword [rax + 1 * r10], 0x01              | 42 d1 2c 10                |
    | shr dword [rax + 1 * r11], 0x01              | 42 d1 2c 18                |
    | shr dword [rax + 1 * r12], 0x01              | 42 d1 2c 20                |
    | shr dword [rax + 1 * r13], 0x01              | 42 d1 2c 28                |
    | shr dword [rax + 1 * r14], 0x01              | 42 d1 2c 30                |
    | shr dword [rax + 1 * r15], 0x01              | 42 d1 2c 38                |
    | shr dword [rax + 2 * rcx], 0x01              | d1 2c 48                   |
    | shr dword [rax + 4 * rcx], 0x01              | d1 2c 88                   |
    | shr dword [rax + 8 * rcx], 0x01              | d1 2c c8                   |
    | shr dword [r8 + 1 * r9], 0x01                | 43 d1 2c 08                |
    | shr dword [r8 + 2 * r9], 0x01                | 43 d1 2c 48                |
    | shr dword [r8 + 4 * r9], 0x01                | 43 d1 2c 88                |
    | shr dword [r8 + 8 * r9], 0x01                | 43 d1 2c c8                |
    | shr dword [1 * rcx], 0x01                    | d1 2c 0d 00 00 00 00       |
    | shr dword [2 * rcx], 0x01                    | d1 2c 4d 00 00 00 00       |
    | shr dword [4 * rcx], 0x01                    | d1 2c 8d 00 00 00 00       |
    | shr dword [8 * rcx], 0x01                    | d1 2c cd 00 00 00 00       |
    | shr dword [1 * r9], 0x01                     | 42 d1 2c 0d 00 00 00 00    |
    | shr dword [2 * r9], 0x01                     | 42 d1 2c 4d 00 00 00 00    |
    | shr dword [4 * r9], 0x01                     | 42 d1 2c 8d 00 00 00 00    |
    | shr dword [8 * r9], 0x01                     | 42 d1 2c cd 00 00 00 00    |
    | shr dword [r13 + 8 * r12], 0x01              | 43 d1 6c e5 00             |
    | shr dword [rsp + 4 * r15], 0x01              | 42 d1 2c bc                |
    | shr dword [rax + 1 * rcx + 0x00], 0x01       | d1 6c 08 00                |
    | shr dword [rax + 1 * rcx - 0x00], 0x01       | d1 6c 08 00                |
    | shr dword [rax + 1 * rcx + 0x01], 0x01       | d1 6c 08 01                |
    | shr dword [rax + 1 * rcx - 0x01], 0x01       | d1 6c 08 ff                |
    | shr dword [rax + 1 * rcx + 0x00000001], 0x01 | d1 ac 08 01 00 00 00       |
    | shr dword [rax + 1 * rcx - 0x00000001], 0x01 | d1 ac 08 ff ff ff ff       |
    | shr dword [rax + 1 * rcx + 0x7f], 0x01       | d1 6c 08 7f                |
    | shr dword [rax + 1 * rcx - 0x7f], 0x01       | d1 6c 08 81                |
    | shr dword [rax + 1 * rcx + 0x80], 0x01       | d1 ac 08 80 00 00 00       |
    | shr dword [rax + 1 * rcx - 0x80], 0x01       | d1 6c 08 80                |
    | shr dword [rax + 1 * rcx - 0x81], 0x01       | d1 ac 08 7f ff ff ff       |
    | shr dword [rax + 1 * rcx + 0xff], 0x01       | d1 ac 08 ff 00 00 00       |
    | shr dword [rax + 1 * rcx - 0xff], 0x01       | d1 ac 08 01 ff ff ff       |
    | shr dword [rax + 1 * rcx + 0x7fffffff], 0x01 | d1 ac 08 ff ff ff 7f       |
    | shr dword [rax + 1 * rcx - 0x7fffffff], 0x01 | d1 ac 08 01 00 00 80       |
    | shr dword [rax + 1 * rcx - 0x80000000], 0x01 | d1 ac 08 00 00 00 80       |
    | shr dword [r10 + 0x7f], 0x01                 | 41 d1 6a 7f                |
    | shr dword [r10 + 0x80], 0x01                 | 41 d1 aa 80 00 00 00       |
    | shr dword [r10 - 0x80], 0x01                 | 41 d1 6a 80                |
    | shr dword [r10 - 0x81], 0x01                 | 41 d1 aa 7f ff ff ff       |
    | shr dword [rax], 0x00                        | c1 28 00                   |
    | shr dword [rax], 0x7f                        | c1 28 7f                   |
    | shr dword [rax], 0x80                        | c1 28 80                   |
    | shr dword [rax], 0xff                        | c1 28 ff                   |
    | shr dword [rcx], 0x7f                        | c1 29 7f                   |
    | shr dword [rdx], 0x80                        | c1 2a 80                   |
    | shr dword [rbx], 0xff                        | c1 2b ff                   |
    | shr dword [rsp], 0x00                        | c1 2c 24 00                |
    | shr dword [rsi], 0x7f                        | c1 2e 7f                   |
    | shr dword [rdi], 0x80                        | c1 2f 80                   |
    | shr dword [r8], 0xff                         | 41 c1 28 ff                |
    | shr dword [r9], 0x00                         | 41 c1 29 00                |
    | shr dword [r11], 0x7f                        | 41 c1 2b 7f                |
    | shr dword [r12], 0x80                        | 41 c1 2c 24 80             |
    | shr dword [r13], 0xff                        | 41 c1 6d 00 ff             |
    | shr dword [r14], 0x00                        | 41 c1 2e 00                |
    | shr dword [rax + 1 * rcx], 0x7f              | c1 2c 08 7f                |
    | shr dword [rcx + 1 * rcx], 0x80              | c1 2c 09 80                |
    | shr dword [rdx + 1 * rcx], 0xff              | c1 2c 0a ff                |
    | shr dword [rbx + 1 * rcx], 0x00              | c1 2c 0b 00                |
    | shr dword [rbp + 1 * rcx], 0x7f              | c1 6c 0d 00 7f             |
    | shr dword [rsi + 1 * rcx], 0x80              | c1 2c 0e 80                |
    | shr dword [rdi + 1 * rcx], 0xff              | c1 2c 0f ff                |
    | shr dword [r8 + 1 * rcx], 0x00               | 41 c1 2c 08 00             |
    | shr dword [r10 + 1 * rcx], 0x7f              | 41 c1 2c 0a 7f             |
    | shr dword [r11 + 1 * rcx], 0x80              | 41 c1 2c 0b 80             |
    | shr dword [r12 + 1 * rcx], 0xff              | 41 c1 2c 0c ff             |
    | shr dword [r13 + 1 * rcx], 0x00              | 41 c1 6c 0d 00 00          |
    | shr dword [r15 + 1 * rcx], 0x7f              | 41 c1 2c 0f 7f             |
    | shr dword [rax + 1 * rax], 0x80              | c1 2c 00 80                |
    | shr dword [rax + 1 * rdx], 0xff              | c1 2c 10 ff                |
    | shr dword [rax + 1 * rbx], 0x00              | c1 2c 18 00                |
    | shr dword [rax + 1 * rsi], 0x7f              | c1 2c 30 7f                |
    | shr dword [rax + 1 * rdi], 0x80              | c1 2c 38 80                |
    | shr dword [rax + 1 * r8], 0xff               | 42 c1 2c 00 ff             |
    | shr dword [rax + 1 * r9], 0x00               | 42 c1 2c 08 00             |
    | shr dword [rax + 1 * r11], 0x7f              | 42 c1 2c 18 7f             |
    | shr dword [rax + 1 * r12], 0x80              | 42 c1 2c 20 80             |
    | shr dword [rax + 1 * r13], 0xff              | 42 c1 2c 28 ff             |
    | shr dword [rax + 1 * r14], 0x00              | 42 c1 2c 30 00             |
    | shr dword [rax + 2 * rcx], 0x7f              | c1 2c 48 7f                |
    | shr dword [rax + 4 * rcx], 0x80              | c1 2c 88 80                |
    | shr dword [rax + 8 * rcx], 0xff              | c1 2c c8 ff                |
    | shr dword [r8 + 1 * r9], 0x00                | 43 c1 2c 08 00             |
    | shr dword [r8 + 4 * r9], 0x7f                | 43 c1 2c 88 7f             |
    | shr dword [r8 + 8 * r9], 0x80                | 43 c1 2c c8 80             |
    | shr dword [1 * rcx], 0xff                    | c1 2c 0d 00 00 00 00 ff    |
    | shr dword [2 * rcx], 0x00                    | c1 2c 4d 00 00 00 00 00    |
    | shr dword [8 * rcx], 0x7f                    | c1 2c cd 00 00 00 00 7f    |
    | shr dword [1 * r9], 0x80                     | 42 c1 2c 0d 00 00 00 00 80 |
    | shr dword [2 * r9], 0xff                     | 42 c1 2c 4d 00 00 00 00 ff |
    | shr dword [4 * r9], 0x00                     | 42 c1 2c 8d 00 00 00 00 00 |
    | shr dword [r13 + 8 * r12], 0x7f              | 43 c1 6c e5 00 7f          |
    | shr dword [rsp + 4 * r15], 0x80              | 42 c1 2c bc 80             |
    | shr dword [rax + 1 * rcx + 0x00], 0xff       | c1 6c 08 00 ff             |
    | shr dword [rax + 1 * rcx - 0x00], 0x00       | c1 6c 08 00 00             |
    | shr dword [rax + 1 * rcx - 0x01], 0x7f       | c1 6c 08 ff 7f             |
    | shr dword [rax + 1 * rcx + 0x00000001], 0x80 | c1 ac 08 01 00 00 00 80    |
    | shr dword [rax + 1 * rcx - 0x00000001], 0xff | c1 ac 08 ff ff ff ff ff    |
    | shr dword [rax + 1 * rcx + 0x7f], 0x00       | c1 6c 08 7f 00             |
    | shr dword [rax + 1 * rcx + 0x80], 0x7f       | c1 ac 08 80 00 00 00 7f    |
    | shr dword [rax + 1 * rcx - 0x80], 0x80       | c1 6c 08 80 80             |
    | shr dword [rax + 1 * rcx - 0x81], 0xff       | c1 ac 08 7f ff ff ff ff    |
    | shr dword [rax + 1 * rcx + 0xff], 0x00       | c1 ac 08 ff 00 00 00 00    |
    | shr dword [rax + 1 * rcx + 0x7fffffff], 0x7f | c1 ac 08 ff ff ff 7f 7f    |
    | shr dword [rax + 1 * rcx - 0x7fffffff], 0x80 | c1 ac 08 01 00 00 80 80    |
    | shr dword [rax + 1 * rcx - 0x80000000], 0xff | c1 ac 08 00 00 00 80 ff    |
    | shr dword [r10 + 0x7f], 0x00                 | 41 c1 6a 7f 00             |
    | shr dword [r10 - 0x80], 0x7f                 | 41 c1 6a 80 7f             |
    | shr dword [r10 - 0x81], 0x80                 | 41 c1 aa 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_shr_addr32_imm8():
    encode(SHR_ADDR32_IMM8)


SHR_ADDR32_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | shr dword [rax], cl                        | d3 28                   |
    | shr dword [rcx], cl                        | d3 29                   |
    | shr dword [rdx], cl                        | d3 2a                   |
    | shr dword [rbx], cl                        | d3 2b                   |
    | shr dword [rsp], cl                        | d3 2c 24                |
    | shr dword [rbp], cl                        | d3 6d 00                |
    | shr dword [rsi], cl                        | d3 2e                   |
    | shr dword [rdi], cl                        | d3 2f                   |
    | shr dword [r8], cl                         | 41 d3 28                |
    | shr dword [r9], cl                         | 41 d3 29                |
    | shr dword [r10], cl                        | 41 d3 2a                |
    | shr dword [r11], cl                        | 41 d3 2b                |
    | shr dword [r12], cl                        | 41 d3 2c 24             |
    | shr dword [r13], cl                        | 41 d3 6d 00             |
    | shr dword [r14], cl                        | 41 d3 2e                |
    | shr dword [r15], cl                        | 41 d3 2f                |
    | shr dword [rax + 1 * rcx], cl              | d3 2c 08                |
    | shr dword [rcx + 1 * rcx], cl              | d3 2c 09                |
    | shr dword [rdx + 1 * rcx], cl              | d3 2c 0a                |
    | shr dword [rbx + 1 * rcx], cl              | d3 2c 0b                |
    | shr dword [rsp + 1 * rcx], cl              | d3 2c 0c                |
    | shr dword [rbp + 1 * rcx], cl              | d3 6c 0d 00             |
    | shr dword [rsi + 1 * rcx], cl              | d3 2c 0e                |
    | shr dword [rdi + 1 * rcx], cl              | d3 2c 0f                |
    | shr dword [r8 + 1 * rcx], cl               | 41 d3 2c 08             |
    | shr dword [r9 + 1 * rcx], cl               | 41 d3 2c 09             |
    | shr dword [r10 + 1 * rcx], cl              | 41 d3 2c 0a             |
    | shr dword [r11 + 1 * rcx], cl              | 41 d3 2c 0b             |
    | shr dword [r12 + 1 * rcx], cl              | 41 d3 2c 0c             |
    | shr dword [r13 + 1 * rcx], cl              | 41 d3 6c 0d 00          |
    | shr dword [r14 + 1 * rcx], cl              | 41 d3 2c 0e             |
    | shr dword [r15 + 1 * rcx], cl              | 41 d3 2c 0f             |
    | shr dword [rax + 1 * rax], cl              | d3 2c 00                |
    | shr dword [rax + 1 * rdx], cl              | d3 2c 10                |
    | shr dword [rax + 1 * rbx], cl              | d3 2c 18                |
    | shr dword [rax + 1 * rbp], cl              | d3 2c 28                |
    | shr dword [rax + 1 * rsi], cl              | d3 2c 30                |
    | shr dword [rax + 1 * rdi], cl              | d3 2c 38                |
    | shr dword [rax + 1 * r8], cl               | 42 d3 2c 00             |
    | shr dword [rax + 1 * r9], cl               | 42 d3 2c 08             |
    | shr dword [rax + 1 * r10], cl              | 42 d3 2c 10             |
    | shr dword [rax + 1 * r11], cl              | 42 d3 2c 18             |
    | shr dword [rax + 1 * r12], cl              | 42 d3 2c 20             |
    | shr dword [rax + 1 * r13], cl              | 42 d3 2c 28             |
    | shr dword [rax + 1 * r14], cl              | 42 d3 2c 30             |
    | shr dword [rax + 1 * r15], cl              | 42 d3 2c 38             |
    | shr dword [rax + 2 * rcx], cl              | d3 2c 48                |
    | shr dword [rax + 4 * rcx], cl              | d3 2c 88                |
    | shr dword [rax + 8 * rcx], cl              | d3 2c c8                |
    | shr dword [r8 + 1 * r9], cl                | 43 d3 2c 08             |
    | shr dword [r8 + 2 * r9], cl                | 43 d3 2c 48             |
    | shr dword [r8 + 4 * r9], cl                | 43 d3 2c 88             |
    | shr dword [r8 + 8 * r9], cl                | 43 d3 2c c8             |
    | shr dword [1 * rcx], cl                    | d3 2c 0d 00 00 00 00    |
    | shr dword [2 * rcx], cl                    | d3 2c 4d 00 00 00 00    |
    | shr dword [4 * rcx], cl                    | d3 2c 8d 00 00 00 00    |
    | shr dword [8 * rcx], cl                    | d3 2c cd 00 00 00 00    |
    | shr dword [1 * r9], cl                     | 42 d3 2c 0d 00 00 00 00 |
    | shr dword [2 * r9], cl                     | 42 d3 2c 4d 00 00 00 00 |
    | shr dword [4 * r9], cl                     | 42 d3 2c 8d 00 00 00 00 |
    | shr dword [8 * r9], cl                     | 42 d3 2c cd 00 00 00 00 |
    | shr dword [r13 + 8 * r12], cl              | 43 d3 6c e5 00          |
    | shr dword [rsp + 4 * r15], cl              | 42 d3 2c bc             |
    | shr dword [rax + 1 * rcx + 0x00], cl       | d3 6c 08 00             |
    | shr dword [rax + 1 * rcx - 0x00], cl       | d3 6c 08 00             |
    | shr dword [rax + 1 * rcx + 0x01], cl       | d3 6c 08 01             |
    | shr dword [rax + 1 * rcx - 0x01], cl       | d3 6c 08 ff             |
    | shr dword [rax + 1 * rcx + 0x00000001], cl | d3 ac 08 01 00 00 00    |
    | shr dword [rax + 1 * rcx - 0x00000001], cl | d3 ac 08 ff ff ff ff    |
    | shr dword [rax + 1 * rcx + 0x7f], cl       | d3 6c 08 7f             |
    | shr dword [rax + 1 * rcx - 0x7f], cl       | d3 6c 08 81             |
    | shr dword [rax + 1 * rcx + 0x80], cl       | d3 ac 08 80 00 00 00    |
    | shr dword [rax + 1 * rcx - 0x80], cl       | d3 6c 08 80             |
    | shr dword [rax + 1 * rcx - 0x81], cl       | d3 ac 08 7f ff ff ff    |
    | shr dword [rax + 1 * rcx + 0xff], cl       | d3 ac 08 ff 00 00 00    |
    | shr dword [rax + 1 * rcx - 0xff], cl       | d3 ac 08 01 ff ff ff    |
    | shr dword [rax + 1 * rcx + 0x7fffffff], cl | d3 ac 08 ff ff ff 7f    |
    | shr dword [rax + 1 * rcx - 0x7fffffff], cl | d3 ac 08 01 00 00 80    |
    | shr dword [rax + 1 * rcx - 0x80000000], cl | d3 ac 08 00 00 00 80    |
    | shr dword [r10 + 0x7f], cl                 | 41 d3 6a 7f             |
    | shr dword [r10 + 0x80], cl                 | 41 d3 aa 80 00 00 00    |
    | shr dword [r10 - 0x80], cl                 | 41 d3 6a 80             |
    | shr dword [r10 - 0x81], cl                 | 41 d3 aa 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_shr_addr32_cl():
    encode(SHR_ADDR32_CL)


SHR_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | shr word [rax], 0x01                        | 66 d1 28                      |
    | shr word [rcx], 0x01                        | 66 d1 29                      |
    | shr word [rdx], 0x01                        | 66 d1 2a                      |
    | shr word [rbx], 0x01                        | 66 d1 2b                      |
    | shr word [rsp], 0x01                        | 66 d1 2c 24                   |
    | shr word [rbp], 0x01                        | 66 d1 6d 00                   |
    | shr word [rsi], 0x01                        | 66 d1 2e                      |
    | shr word [rdi], 0x01                        | 66 d1 2f                      |
    | shr word [r8], 0x01                         | 66 41 d1 28                   |
    | shr word [r9], 0x01                         | 66 41 d1 29                   |
    | shr word [r10], 0x01                        | 66 41 d1 2a                   |
    | shr word [r11], 0x01                        | 66 41 d1 2b                   |
    | shr word [r12], 0x01                        | 66 41 d1 2c 24                |
    | shr word [r13], 0x01                        | 66 41 d1 6d 00                |
    | shr word [r14], 0x01                        | 66 41 d1 2e                   |
    | shr word [r15], 0x01                        | 66 41 d1 2f                   |
    | shr word [rax + 1 * rcx], 0x01              | 66 d1 2c 08                   |
    | shr word [rcx + 1 * rcx], 0x01              | 66 d1 2c 09                   |
    | shr word [rdx + 1 * rcx], 0x01              | 66 d1 2c 0a                   |
    | shr word [rbx + 1 * rcx], 0x01              | 66 d1 2c 0b                   |
    | shr word [rsp + 1 * rcx], 0x01              | 66 d1 2c 0c                   |
    | shr word [rbp + 1 * rcx], 0x01              | 66 d1 6c 0d 00                |
    | shr word [rsi + 1 * rcx], 0x01              | 66 d1 2c 0e                   |
    | shr word [rdi + 1 * rcx], 0x01              | 66 d1 2c 0f                   |
    | shr word [r8 + 1 * rcx], 0x01               | 66 41 d1 2c 08                |
    | shr word [r9 + 1 * rcx], 0x01               | 66 41 d1 2c 09                |
    | shr word [r10 + 1 * rcx], 0x01              | 66 41 d1 2c 0a                |
    | shr word [r11 + 1 * rcx], 0x01              | 66 41 d1 2c 0b                |
    | shr word [r12 + 1 * rcx], 0x01              | 66 41 d1 2c 0c                |
    | shr word [r13 + 1 * rcx], 0x01              | 66 41 d1 6c 0d 00             |
    | shr word [r14 + 1 * rcx], 0x01              | 66 41 d1 2c 0e                |
    | shr word [r15 + 1 * rcx], 0x01              | 66 41 d1 2c 0f                |
    | shr word [rax + 1 * rax], 0x01              | 66 d1 2c 00                   |
    | shr word [rax + 1 * rdx], 0x01              | 66 d1 2c 10                   |
    | shr word [rax + 1 * rbx], 0x01              | 66 d1 2c 18                   |
    | shr word [rax + 1 * rbp], 0x01              | 66 d1 2c 28                   |
    | shr word [rax + 1 * rsi], 0x01              | 66 d1 2c 30                   |
    | shr word [rax + 1 * rdi], 0x01              | 66 d1 2c 38                   |
    | shr word [rax + 1 * r8], 0x01               | 66 42 d1 2c 00                |
    | shr word [rax + 1 * r9], 0x01               | 66 42 d1 2c 08                |
    | shr word [rax + 1 * r10], 0x01              | 66 42 d1 2c 10                |
    | shr word [rax + 1 * r11], 0x01              | 66 42 d1 2c 18                |
    | shr word [rax + 1 * r12], 0x01              | 66 42 d1 2c 20                |
    | shr word [rax + 1 * r13], 0x01              | 66 42 d1 2c 28                |
    | shr word [rax + 1 * r14], 0x01              | 66 42 d1 2c 30                |
    | shr word [rax + 1 * r15], 0x01              | 66 42 d1 2c 38                |
    | shr word [rax + 2 * rcx], 0x01              | 66 d1 2c 48                   |
    | shr word [rax + 4 * rcx], 0x01              | 66 d1 2c 88                   |
    | shr word [rax + 8 * rcx], 0x01              | 66 d1 2c c8                   |
    | shr word [r8 + 1 * r9], 0x01                | 66 43 d1 2c 08                |
    | shr word [r8 + 2 * r9], 0x01                | 66 43 d1 2c 48                |
    | shr word [r8 + 4 * r9], 0x01                | 66 43 d1 2c 88                |
    | shr word [r8 + 8 * r9], 0x01                | 66 43 d1 2c c8                |
    | shr word [1 * rcx], 0x01                    | 66 d1 2c 0d 00 00 00 00       |
    | shr word [2 * rcx], 0x01                    | 66 d1 2c 4d 00 00 00 00       |
    | shr word [4 * rcx], 0x01                    | 66 d1 2c 8d 00 00 00 00       |
    | shr word [8 * rcx], 0x01                    | 66 d1 2c cd 00 00 00 00       |
    | shr word [1 * r9], 0x01                     | 66 42 d1 2c 0d 00 00 00 00    |
    | shr word [2 * r9], 0x01                     | 66 42 d1 2c 4d 00 00 00 00    |
    | shr word [4 * r9], 0x01                     | 66 42 d1 2c 8d 00 00 00 00    |
    | shr word [8 * r9], 0x01                     | 66 42 d1 2c cd 00 00 00 00    |
    | shr word [r13 + 8 * r12], 0x01              | 66 43 d1 6c e5 00             |
    | shr word [rsp + 4 * r15], 0x01              | 66 42 d1 2c bc                |
    | shr word [rax + 1 * rcx + 0x00], 0x01       | 66 d1 6c 08 00                |
    | shr word [rax + 1 * rcx - 0x00], 0x01       | 66 d1 6c 08 00                |
    | shr word [rax + 1 * rcx + 0x01], 0x01       | 66 d1 6c 08 01                |
    | shr word [rax + 1 * rcx - 0x01], 0x01       | 66 d1 6c 08 ff                |
    | shr word [rax + 1 * rcx + 0x00000001], 0x01 | 66 d1 ac 08 01 00 00 00       |
    | shr word [rax + 1 * rcx - 0x00000001], 0x01 | 66 d1 ac 08 ff ff ff ff       |
    | shr word [rax + 1 * rcx + 0x7f], 0x01       | 66 d1 6c 08 7f                |
    | shr word [rax + 1 * rcx - 0x7f], 0x01       | 66 d1 6c 08 81                |
    | shr word [rax + 1 * rcx + 0x80], 0x01       | 66 d1 ac 08 80 00 00 00       |
    | shr word [rax + 1 * rcx - 0x80], 0x01       | 66 d1 6c 08 80                |
    | shr word [rax + 1 * rcx - 0x81], 0x01       | 66 d1 ac 08 7f ff ff ff       |
    | shr word [rax + 1 * rcx + 0xff], 0x01       | 66 d1 ac 08 ff 00 00 00       |
    | shr word [rax + 1 * rcx - 0xff], 0x01       | 66 d1 ac 08 01 ff ff ff       |
    | shr word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 d1 ac 08 ff ff ff 7f       |
    | shr word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 d1 ac 08 01 00 00 80       |
    | shr word [rax + 1 * rcx - 0x80000000], 0x01 | 66 d1 ac 08 00 00 00 80       |
    | shr word [r10 + 0x7f], 0x01                 | 66 41 d1 6a 7f                |
    | shr word [r10 + 0x80], 0x01                 | 66 41 d1 aa 80 00 00 00       |
    | shr word [r10 - 0x80], 0x01                 | 66 41 d1 6a 80                |
    | shr word [r10 - 0x81], 0x01                 | 66 41 d1 aa 7f ff ff ff       |
    | shr word [rax], 0x00                        | 66 c1 28 00                   |
    | shr word [rax], 0x7f                        | 66 c1 28 7f                   |
    | shr word [rax], 0x80                        | 66 c1 28 80                   |
    | shr word [rax], 0xff                        | 66 c1 28 ff                   |
    | shr word [rcx], 0x7f                        | 66 c1 29 7f                   |
    | shr word [rdx], 0x80                        | 66 c1 2a 80                   |
    | shr word [rbx], 0xff                        | 66 c1 2b ff                   |
    | shr word [rsp], 0x00                        | 66 c1 2c 24 00                |
    | shr word [rsi], 0x7f                        | 66 c1 2e 7f                   |
    | shr word [rdi], 0x80                        | 66 c1 2f 80                   |
    | shr word [r8], 0xff                         | 66 41 c1 28 ff                |
    | shr word [r9], 0x00                         | 66 41 c1 29 00                |
    | shr word [r11], 0x7f                        | 66 41 c1 2b 7f                |
    | shr word [r12], 0x80                        | 66 41 c1 2c 24 80             |
    | shr word [r13], 0xff                        | 66 41 c1 6d 00 ff             |
    | shr word [r14], 0x00                        | 66 41 c1 2e 00                |
    | shr word [rax + 1 * rcx], 0x7f              | 66 c1 2c 08 7f                |
    | shr word [rcx + 1 * rcx], 0x80              | 66 c1 2c 09 80                |
    | shr word [rdx + 1 * rcx], 0xff              | 66 c1 2c 0a ff                |
    | shr word [rbx + 1 * rcx], 0x00              | 66 c1 2c 0b 00                |
    | shr word [rbp + 1 * rcx], 0x7f              | 66 c1 6c 0d 00 7f             |
    | shr word [rsi + 1 * rcx], 0x80              | 66 c1 2c 0e 80                |
    | shr word [rdi + 1 * rcx], 0xff              | 66 c1 2c 0f ff                |
    | shr word [r8 + 1 * rcx], 0x00               | 66 41 c1 2c 08 00             |
    | shr word [r10 + 1 * rcx], 0x7f              | 66 41 c1 2c 0a 7f             |
    | shr word [r11 + 1 * rcx], 0x80              | 66 41 c1 2c 0b 80             |
    | shr word [r12 + 1 * rcx], 0xff              | 66 41 c1 2c 0c ff             |
    | shr word [r13 + 1 * rcx], 0x00              | 66 41 c1 6c 0d 00 00          |
    | shr word [r15 + 1 * rcx], 0x7f              | 66 41 c1 2c 0f 7f             |
    | shr word [rax + 1 * rax], 0x80              | 66 c1 2c 00 80                |
    | shr word [rax + 1 * rdx], 0xff              | 66 c1 2c 10 ff                |
    | shr word [rax + 1 * rbx], 0x00              | 66 c1 2c 18 00                |
    | shr word [rax + 1 * rsi], 0x7f              | 66 c1 2c 30 7f                |
    | shr word [rax + 1 * rdi], 0x80              | 66 c1 2c 38 80                |
    | shr word [rax + 1 * r8], 0xff               | 66 42 c1 2c 00 ff             |
    | shr word [rax + 1 * r9], 0x00               | 66 42 c1 2c 08 00             |
    | shr word [rax + 1 * r11], 0x7f              | 66 42 c1 2c 18 7f             |
    | shr word [rax + 1 * r12], 0x80              | 66 42 c1 2c 20 80             |
    | shr word [rax + 1 * r13], 0xff              | 66 42 c1 2c 28 ff             |
    | shr word [rax + 1 * r14], 0x00              | 66 42 c1 2c 30 00             |
    | shr word [rax + 2 * rcx], 0x7f              | 66 c1 2c 48 7f                |
    | shr word [rax + 4 * rcx], 0x80              | 66 c1 2c 88 80                |
    | shr word [rax + 8 * rcx], 0xff              | 66 c1 2c c8 ff                |
    | shr word [r8 + 1 * r9], 0x00                | 66 43 c1 2c 08 00             |
    | shr word [r8 + 4 * r9], 0x7f                | 66 43 c1 2c 88 7f             |
    | shr word [r8 + 8 * r9], 0x80                | 66 43 c1 2c c8 80             |
    | shr word [1 * rcx], 0xff                    | 66 c1 2c 0d 00 00 00 00 ff    |
    | shr word [2 * rcx], 0x00                    | 66 c1 2c 4d 00 00 00 00 00    |
    | shr word [8 * rcx], 0x7f                    | 66 c1 2c cd 00 00 00 00 7f    |
    | shr word [1 * r9], 0x80                     | 66 42 c1 2c 0d 00 00 00 00 80 |
    | shr word [2 * r9], 0xff                     | 66 42 c1 2c 4d 00 00 00 00 ff |
    | shr word [4 * r9], 0x00                     | 66 42 c1 2c 8d 00 00 00 00 00 |
    | shr word [r13 + 8 * r12], 0x7f              | 66 43 c1 6c e5 00 7f          |
    | shr word [rsp + 4 * r15], 0x80              | 66 42 c1 2c bc 80             |
    | shr word [rax + 1 * rcx + 0x00], 0xff       | 66 c1 6c 08 00 ff             |
    | shr word [rax + 1 * rcx - 0x00], 0x00       | 66 c1 6c 08 00 00             |
    | shr word [rax + 1 * rcx - 0x01], 0x7f       | 66 c1 6c 08 ff 7f             |
    | shr word [rax + 1 * rcx + 0x00000001], 0x80 | 66 c1 ac 08 01 00 00 00 80    |
    | shr word [rax + 1 * rcx - 0x00000001], 0xff | 66 c1 ac 08 ff ff ff ff ff    |
    | shr word [rax + 1 * rcx + 0x7f], 0x00       | 66 c1 6c 08 7f 00             |
    | shr word [rax + 1 * rcx + 0x80], 0x7f       | 66 c1 ac 08 80 00 00 00 7f    |
    | shr word [rax + 1 * rcx - 0x80], 0x80       | 66 c1 6c 08 80 80             |
    | shr word [rax + 1 * rcx - 0x81], 0xff       | 66 c1 ac 08 7f ff ff ff ff    |
    | shr word [rax + 1 * rcx + 0xff], 0x00       | 66 c1 ac 08 ff 00 00 00 00    |
    | shr word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 c1 ac 08 ff ff ff 7f 7f    |
    | shr word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 c1 ac 08 01 00 00 80 80    |
    | shr word [rax + 1 * rcx - 0x80000000], 0xff | 66 c1 ac 08 00 00 00 80 ff    |
    | shr word [r10 + 0x7f], 0x00                 | 66 41 c1 6a 7f 00             |
    | shr word [r10 - 0x80], 0x7f                 | 66 41 c1 6a 80 7f             |
    | shr word [r10 - 0x81], 0x80                 | 66 41 c1 aa 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_shr_addr16_imm8():
    encode(SHR_ADDR16_IMM8)


SHR_ADDR16_CL = """
    | ----------------------------------------- | -------------------------- |
    | instruction                               | encoding                   |
    | ----------------------------------------- | -------------------------- |
    | shr word [rax], cl                        | 66 d3 28                   |
    | shr word [rcx], cl                        | 66 d3 29                   |
    | shr word [rdx], cl                        | 66 d3 2a                   |
    | shr word [rbx], cl                        | 66 d3 2b                   |
    | shr word [rsp], cl                        | 66 d3 2c 24                |
    | shr word [rbp], cl                        | 66 d3 6d 00                |
    | shr word [rsi], cl                        | 66 d3 2e                   |
    | shr word [rdi], cl                        | 66 d3 2f                   |
    | shr word [r8], cl                         | 66 41 d3 28                |
    | shr word [r9], cl                         | 66 41 d3 29                |
    | shr word [r10], cl                        | 66 41 d3 2a                |
    | shr word [r11], cl                        | 66 41 d3 2b                |
    | shr word [r12], cl                        | 66 41 d3 2c 24             |
    | shr word [r13], cl                        | 66 41 d3 6d 00             |
    | shr word [r14], cl                        | 66 41 d3 2e                |
    | shr word [r15], cl                        | 66 41 d3 2f                |
    | shr word [rax + 1 * rcx], cl              | 66 d3 2c 08                |
    | shr word [rcx + 1 * rcx], cl              | 66 d3 2c 09                |
    | shr word [rdx + 1 * rcx], cl              | 66 d3 2c 0a                |
    | shr word [rbx + 1 * rcx], cl              | 66 d3 2c 0b                |
    | shr word [rsp + 1 * rcx], cl              | 66 d3 2c 0c                |
    | shr word [rbp + 1 * rcx], cl              | 66 d3 6c 0d 00             |
    | shr word [rsi + 1 * rcx], cl              | 66 d3 2c 0e                |
    | shr word [rdi + 1 * rcx], cl              | 66 d3 2c 0f                |
    | shr word [r8 + 1 * rcx], cl               | 66 41 d3 2c 08             |
    | shr word [r9 + 1 * rcx], cl               | 66 41 d3 2c 09             |
    | shr word [r10 + 1 * rcx], cl              | 66 41 d3 2c 0a             |
    | shr word [r11 + 1 * rcx], cl              | 66 41 d3 2c 0b             |
    | shr word [r12 + 1 * rcx], cl              | 66 41 d3 2c 0c             |
    | shr word [r13 + 1 * rcx], cl              | 66 41 d3 6c 0d 00          |
    | shr word [r14 + 1 * rcx], cl              | 66 41 d3 2c 0e             |
    | shr word [r15 + 1 * rcx], cl              | 66 41 d3 2c 0f             |
    | shr word [rax + 1 * rax], cl              | 66 d3 2c 00                |
    | shr word [rax + 1 * rdx], cl              | 66 d3 2c 10                |
    | shr word [rax + 1 * rbx], cl              | 66 d3 2c 18                |
    | shr word [rax + 1 * rbp], cl              | 66 d3 2c 28                |
    | shr word [rax + 1 * rsi], cl              | 66 d3 2c 30                |
    | shr word [rax + 1 * rdi], cl              | 66 d3 2c 38                |
    | shr word [rax + 1 * r8], cl               | 66 42 d3 2c 00             |
    | shr word [rax + 1 * r9], cl               | 66 42 d3 2c 08             |
    | shr word [rax + 1 * r10], cl              | 66 42 d3 2c 10             |
    | shr word [rax + 1 * r11], cl              | 66 42 d3 2c 18             |
    | shr word [rax + 1 * r12], cl              | 66 42 d3 2c 20             |
    | shr word [rax + 1 * r13], cl              | 66 42 d3 2c 28             |
    | shr word [rax + 1 * r14], cl              | 66 42 d3 2c 30             |
    | shr word [rax + 1 * r15], cl              | 66 42 d3 2c 38             |
    | shr word [rax + 2 * rcx], cl              | 66 d3 2c 48                |
    | shr word [rax + 4 * rcx], cl              | 66 d3 2c 88                |
    | shr word [rax + 8 * rcx], cl              | 66 d3 2c c8                |
    | shr word [r8 + 1 * r9], cl                | 66 43 d3 2c 08             |
    | shr word [r8 + 2 * r9], cl                | 66 43 d3 2c 48             |
    | shr word [r8 + 4 * r9], cl                | 66 43 d3 2c 88             |
    | shr word [r8 + 8 * r9], cl                | 66 43 d3 2c c8             |
    | shr word [1 * rcx], cl                    | 66 d3 2c 0d 00 00 00 00    |
    | shr word [2 * rcx], cl                    | 66 d3 2c 4d 00 00 00 00    |
    | shr word [4 * rcx], cl                    | 66 d3 2c 8d 00 00 00 00    |
    | shr word [8 * rcx], cl                    | 66 d3 2c cd 00 00 00 00    |
    | shr word [1 * r9], cl                     | 66 42 d3 2c 0d 00 00 00 00 |
    | shr word [2 * r9], cl                     | 66 42 d3 2c 4d 00 00 00 00 |
    | shr word [4 * r9], cl                     | 66 42 d3 2c 8d 00 00 00 00 |
    | shr word [8 * r9], cl                     | 66 42 d3 2c cd 00 00 00 00 |
    | shr word [r13 + 8 * r12], cl              | 66 43 d3 6c e5 00          |
    | shr word [rsp + 4 * r15], cl              | 66 42 d3 2c bc             |
    | shr word [rax + 1 * rcx + 0x00], cl       | 66 d3 6c 08 00             |
    | shr word [rax + 1 * rcx - 0x00], cl       | 66 d3 6c 08 00             |
    | shr word [rax + 1 * rcx + 0x01], cl       | 66 d3 6c 08 01             |
    | shr word [rax + 1 * rcx - 0x01], cl       | 66 d3 6c 08 ff             |
    | shr word [rax + 1 * rcx + 0x00000001], cl | 66 d3 ac 08 01 00 00 00    |
    | shr word [rax + 1 * rcx - 0x00000001], cl | 66 d3 ac 08 ff ff ff ff    |
    | shr word [rax + 1 * rcx + 0x7f], cl       | 66 d3 6c 08 7f             |
    | shr word [rax + 1 * rcx - 0x7f], cl       | 66 d3 6c 08 81             |
    | shr word [rax + 1 * rcx + 0x80], cl       | 66 d3 ac 08 80 00 00 00    |
    | shr word [rax + 1 * rcx - 0x80], cl       | 66 d3 6c 08 80             |
    | shr word [rax + 1 * rcx - 0x81], cl       | 66 d3 ac 08 7f ff ff ff    |
    | shr word [rax + 1 * rcx + 0xff], cl       | 66 d3 ac 08 ff 00 00 00    |
    | shr word [rax + 1 * rcx - 0xff], cl       | 66 d3 ac 08 01 ff ff ff    |
    | shr word [rax + 1 * rcx + 0x7fffffff], cl | 66 d3 ac 08 ff ff ff 7f    |
    | shr word [rax + 1 * rcx - 0x7fffffff], cl | 66 d3 ac 08 01 00 00 80    |
    | shr word [rax + 1 * rcx - 0x80000000], cl | 66 d3 ac 08 00 00 00 80    |
    | shr word [r10 + 0x7f], cl                 | 66 41 d3 6a 7f             |
    | shr word [r10 + 0x80], cl                 | 66 41 d3 aa 80 00 00 00    |
    | shr word [r10 - 0x80], cl                 | 66 41 d3 6a 80             |
    | shr word [r10 - 0x81], cl                 | 66 41 d3 aa 7f ff ff ff    |
    | ----------------------------------------- | -------------------------- |
"""


def can_encode_shr_addr16_cl():
    encode(SHR_ADDR16_CL)


SHR_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | shr byte [rax], 0x01                        | d0 28                      |
    | shr byte [rcx], 0x01                        | d0 29                      |
    | shr byte [rdx], 0x01                        | d0 2a                      |
    | shr byte [rbx], 0x01                        | d0 2b                      |
    | shr byte [rsp], 0x01                        | d0 2c 24                   |
    | shr byte [rbp], 0x01                        | d0 6d 00                   |
    | shr byte [rsi], 0x01                        | d0 2e                      |
    | shr byte [rdi], 0x01                        | d0 2f                      |
    | shr byte [r8], 0x01                         | 41 d0 28                   |
    | shr byte [r9], 0x01                         | 41 d0 29                   |
    | shr byte [r10], 0x01                        | 41 d0 2a                   |
    | shr byte [r11], 0x01                        | 41 d0 2b                   |
    | shr byte [r12], 0x01                        | 41 d0 2c 24                |
    | shr byte [r13], 0x01                        | 41 d0 6d 00                |
    | shr byte [r14], 0x01                        | 41 d0 2e                   |
    | shr byte [r15], 0x01                        | 41 d0 2f                   |
    | shr byte [rax + 1 * rcx], 0x01              | d0 2c 08                   |
    | shr byte [rcx + 1 * rcx], 0x01              | d0 2c 09                   |
    | shr byte [rdx + 1 * rcx], 0x01              | d0 2c 0a                   |
    | shr byte [rbx + 1 * rcx], 0x01              | d0 2c 0b                   |
    | shr byte [rsp + 1 * rcx], 0x01              | d0 2c 0c                   |
    | shr byte [rbp + 1 * rcx], 0x01              | d0 6c 0d 00                |
    | shr byte [rsi + 1 * rcx], 0x01              | d0 2c 0e                   |
    | shr byte [rdi + 1 * rcx], 0x01              | d0 2c 0f                   |
    | shr byte [r8 + 1 * rcx], 0x01               | 41 d0 2c 08                |
    | shr byte [r9 + 1 * rcx], 0x01               | 41 d0 2c 09                |
    | shr byte [r10 + 1 * rcx], 0x01              | 41 d0 2c 0a                |
    | shr byte [r11 + 1 * rcx], 0x01              | 41 d0 2c 0b                |
    | shr byte [r12 + 1 * rcx], 0x01              | 41 d0 2c 0c                |
    | shr byte [r13 + 1 * rcx], 0x01              | 41 d0 6c 0d 00             |
    | shr byte [r14 + 1 * rcx], 0x01              | 41 d0 2c 0e                |
    | shr byte [r15 + 1 * rcx], 0x01              | 41 d0 2c 0f                |
    | shr byte [rax + 1 * rax], 0x01              | d0 2c 00                   |
    | shr byte [rax + 1 * rdx], 0x01              | d0 2c 10                   |
    | shr byte [rax + 1 * rbx], 0x01              | d0 2c 18                   |
    | shr byte [rax + 1 * rbp], 0x01              | d0 2c 28                   |
    | shr byte [rax + 1 * rsi], 0x01              | d0 2c 30                   |
    | shr byte [rax + 1 * rdi], 0x01              | d0 2c 38                   |
    | shr byte [rax + 1 * r8], 0x01               | 42 d0 2c 00                |
    | shr byte [rax + 1 * r9], 0x01               | 42 d0 2c 08                |
    | shr byte [rax + 1 * r10], 0x01              | 42 d0 2c 10                |
    | shr byte [rax + 1 * r11], 0x01              | 42 d0 2c 18                |
    | shr byte [rax + 1 * r12], 0x01              | 42 d0 2c 20                |
    | shr byte [rax + 1 * r13], 0x01              | 42 d0 2c 28                |
    | shr byte [rax + 1 * r14], 0x01              | 42 d0 2c 30                |
    | shr byte [rax + 1 * r15], 0x01              | 42 d0 2c 38                |
    | shr byte [rax + 2 * rcx], 0x01              | d0 2c 48                   |
    | shr byte [rax + 4 * rcx], 0x01              | d0 2c 88                   |
    | shr byte [rax + 8 * rcx], 0x01              | d0 2c c8                   |
    | shr byte [r8 + 1 * r9], 0x01                | 43 d0 2c 08                |
    | shr byte [r8 + 2 * r9], 0x01                | 43 d0 2c 48                |
    | shr byte [r8 + 4 * r9], 0x01                | 43 d0 2c 88                |
    | shr byte [r8 + 8 * r9], 0x01                | 43 d0 2c c8                |
    | shr byte [1 * rcx], 0x01                    | d0 2c 0d 00 00 00 00       |
    | shr byte [2 * rcx], 0x01                    | d0 2c 4d 00 00 00 00       |
    | shr byte [4 * rcx], 0x01                    | d0 2c 8d 00 00 00 00       |
    | shr byte [8 * rcx], 0x01                    | d0 2c cd 00 00 00 00       |
    | shr byte [1 * r9], 0x01                     | 42 d0 2c 0d 00 00 00 00    |
    | shr byte [2 * r9], 0x01                     | 42 d0 2c 4d 00 00 00 00    |
    | shr byte [4 * r9], 0x01                     | 42 d0 2c 8d 00 00 00 00    |
    | shr byte [8 * r9], 0x01                     | 42 d0 2c cd 00 00 00 00    |
    | shr byte [r13 + 8 * r12], 0x01              | 43 d0 6c e5 00             |
    | shr byte [rsp + 4 * r15], 0x01              | 42 d0 2c bc                |
    | shr byte [rax + 1 * rcx + 0x00], 0x01       | d0 6c 08 00                |
    | shr byte [rax + 1 * rcx - 0x00], 0x01       | d0 6c 08 00                |
    | shr byte [rax + 1 * rcx + 0x01], 0x01       | d0 6c 08 01                |
    | shr byte [rax + 1 * rcx - 0x01], 0x01       | d0 6c 08 ff                |
    | shr byte [rax + 1 * rcx + 0x00000001], 0x01 | d0 ac 08 01 00 00 00       |
    | shr byte [rax + 1 * rcx - 0x00000001], 0x01 | d0 ac 08 ff ff ff ff       |
    | shr byte [rax + 1 * rcx + 0x7f], 0x01       | d0 6c 08 7f                |
    | shr byte [rax + 1 * rcx - 0x7f], 0x01       | d0 6c 08 81                |
    | shr byte [rax + 1 * rcx + 0x80], 0x01       | d0 ac 08 80 00 00 00       |
    | shr byte [rax + 1 * rcx - 0x80], 0x01       | d0 6c 08 80                |
    | shr byte [rax + 1 * rcx - 0x81], 0x01       | d0 ac 08 7f ff ff ff       |
    | shr byte [rax + 1 * rcx + 0xff], 0x01       | d0 ac 08 ff 00 00 00       |
    | shr byte [rax + 1 * rcx - 0xff], 0x01       | d0 ac 08 01 ff ff ff       |
    | shr byte [rax + 1 * rcx + 0x7fffffff], 0x01 | d0 ac 08 ff ff ff 7f       |
    | shr byte [rax + 1 * rcx - 0x7fffffff], 0x01 | d0 ac 08 01 00 00 80       |
    | shr byte [rax + 1 * rcx - 0x80000000], 0x01 | d0 ac 08 00 00 00 80       |
    | shr byte [r10 + 0x7f], 0x01                 | 41 d0 6a 7f                |
    | shr byte [r10 + 0x80], 0x01                 | 41 d0 aa 80 00 00 00       |
    | shr byte [r10 - 0x80], 0x01                 | 41 d0 6a 80                |
    | shr byte [r10 - 0x81], 0x01                 | 41 d0 aa 7f ff ff ff       |
    | shr byte [rax], 0x00                        | c0 28 00                   |
    | shr byte [rax], 0x7f                        | c0 28 7f                   |
    | shr byte [rax], 0x80                        | c0 28 80                   |
    | shr byte [rax], 0xff                        | c0 28 ff                   |
    | shr byte [rcx], 0x7f                        | c0 29 7f                   |
    | shr byte [rdx], 0x80                        | c0 2a 80                   |
    | shr byte [rbx], 0xff                        | c0 2b ff                   |
    | shr byte [rsp], 0x00                        | c0 2c 24 00                |
    | shr byte [rsi], 0x7f                        | c0 2e 7f                   |
    | shr byte [rdi], 0x80                        | c0 2f 80                   |
    | shr byte [r8], 0xff                         | 41 c0 28 ff                |
    | shr byte [r9], 0x00                         | 41 c0 29 00                |
    | shr byte [r11], 0x7f                        | 41 c0 2b 7f                |
    | shr byte [r12], 0x80                        | 41 c0 2c 24 80             |
    | shr byte [r13], 0xff                        | 41 c0 6d 00 ff             |
    | shr byte [r14], 0x00                        | 41 c0 2e 00                |
    | shr byte [rax + 1 * rcx], 0x7f              | c0 2c 08 7f                |
    | shr byte [rcx + 1 * rcx], 0x80              | c0 2c 09 80                |
    | shr byte [rdx + 1 * rcx], 0xff              | c0 2c 0a ff                |
    | shr byte [rbx + 1 * rcx], 0x00              | c0 2c 0b 00                |
    | shr byte [rbp + 1 * rcx], 0x7f              | c0 6c 0d 00 7f             |
    | shr byte [rsi + 1 * rcx], 0x80              | c0 2c 0e 80                |
    | shr byte [rdi + 1 * rcx], 0xff              | c0 2c 0f ff                |
    | shr byte [r8 + 1 * rcx], 0x00               | 41 c0 2c 08 00             |
    | shr byte [r10 + 1 * rcx], 0x7f              | 41 c0 2c 0a 7f             |
    | shr byte [r11 + 1 * rcx], 0x80              | 41 c0 2c 0b 80             |
    | shr byte [r12 + 1 * rcx], 0xff              | 41 c0 2c 0c ff             |
    | shr byte [r13 + 1 * rcx], 0x00              | 41 c0 6c 0d 00 00          |
    | shr byte [r15 + 1 * rcx], 0x7f              | 41 c0 2c 0f 7f             |
    | shr byte [rax + 1 * rax], 0x80              | c0 2c 00 80                |
    | shr byte [rax + 1 * rdx], 0xff              | c0 2c 10 ff                |
    | shr byte [rax + 1 * rbx], 0x00              | c0 2c 18 00                |
    | shr byte [rax + 1 * rsi], 0x7f              | c0 2c 30 7f                |
    | shr byte [rax + 1 * rdi], 0x80              | c0 2c 38 80                |
    | shr byte [rax + 1 * r8], 0xff               | 42 c0 2c 00 ff             |
    | shr byte [rax + 1 * r9], 0x00               | 42 c0 2c 08 00             |
    | shr byte [rax + 1 * r11], 0x7f              | 42 c0 2c 18 7f             |
    | shr byte [rax + 1 * r12], 0x80              | 42 c0 2c 20 80             |
    | shr byte [rax + 1 * r13], 0xff              | 42 c0 2c 28 ff             |
    | shr byte [rax + 1 * r14], 0x00              | 42 c0 2c 30 00             |
    | shr byte [rax + 2 * rcx], 0x7f              | c0 2c 48 7f                |
    | shr byte [rax + 4 * rcx], 0x80              | c0 2c 88 80                |
    | shr byte [rax + 8 * rcx], 0xff              | c0 2c c8 ff                |
    | shr byte [r8 + 1 * r9], 0x00                | 43 c0 2c 08 00             |
    | shr byte [r8 + 4 * r9], 0x7f                | 43 c0 2c 88 7f             |
    | shr byte [r8 + 8 * r9], 0x80                | 43 c0 2c c8 80             |
    | shr byte [1 * rcx], 0xff                    | c0 2c 0d 00 00 00 00 ff    |
    | shr byte [2 * rcx], 0x00                    | c0 2c 4d 00 00 00 00 00    |
    | shr byte [8 * rcx], 0x7f                    | c0 2c cd 00 00 00 00 7f    |
    | shr byte [1 * r9], 0x80                     | 42 c0 2c 0d 00 00 00 00 80 |
    | shr byte [2 * r9], 0xff                     | 42 c0 2c 4d 00 00 00 00 ff |
    | shr byte [4 * r9], 0x00                     | 42 c0 2c 8d 00 00 00 00 00 |
    | shr byte [r13 + 8 * r12], 0x7f              | 43 c0 6c e5 00 7f          |
    | shr byte [rsp + 4 * r15], 0x80              | 42 c0 2c bc 80             |
    | shr byte [rax + 1 * rcx + 0x00], 0xff       | c0 6c 08 00 ff             |
    | shr byte [rax + 1 * rcx - 0x00], 0x00       | c0 6c 08 00 00             |
    | shr byte [rax + 1 * rcx - 0x01], 0x7f       | c0 6c 08 ff 7f             |
    | shr byte [rax + 1 * rcx + 0x00000001], 0x80 | c0 ac 08 01 00 00 00 80    |
    | shr byte [rax + 1 * rcx - 0x00000001], 0xff | c0 ac 08 ff ff ff ff ff    |
    | shr byte [rax + 1 * rcx + 0x7f], 0x00       | c0 6c 08 7f 00             |
    | shr byte [rax + 1 * rcx + 0x80], 0x7f       | c0 ac 08 80 00 00 00 7f    |
    | shr byte [rax + 1 * rcx - 0x80], 0x80       | c0 6c 08 80 80             |
    | shr byte [rax + 1 * rcx - 0x81], 0xff       | c0 ac 08 7f ff ff ff ff    |
    | shr byte [rax + 1 * rcx + 0xff], 0x00       | c0 ac 08 ff 00 00 00 00    |
    | shr byte [rax + 1 * rcx + 0x7fffffff], 0x7f | c0 ac 08 ff ff ff 7f 7f    |
    | shr byte [rax + 1 * rcx - 0x7fffffff], 0x80 | c0 ac 08 01 00 00 80 80    |
    | shr byte [rax + 1 * rcx - 0x80000000], 0xff | c0 ac 08 00 00 00 80 ff    |
    | shr byte [r10 + 0x7f], 0x00                 | 41 c0 6a 7f 00             |
    | shr byte [r10 - 0x80], 0x7f                 | 41 c0 6a 80 7f             |
    | shr byte [r10 - 0x81], 0x80                 | 41 c0 aa 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_shr_addr8_imm8():
    encode(SHR_ADDR8_IMM8)


SHR_ADDR8_CL = """
    | ----------------------------------------- | ----------------------- |
    | instruction                               | encoding                |
    | ----------------------------------------- | ----------------------- |
    | shr byte [rax], cl                        | d2 28                   |
    | shr byte [rcx], cl                        | d2 29                   |
    | shr byte [rdx], cl                        | d2 2a                   |
    | shr byte [rbx], cl                        | d2 2b                   |
    | shr byte [rsp], cl                        | d2 2c 24                |
    | shr byte [rbp], cl                        | d2 6d 00                |
    | shr byte [rsi], cl                        | d2 2e                   |
    | shr byte [rdi], cl                        | d2 2f                   |
    | shr byte [r8], cl                         | 41 d2 28                |
    | shr byte [r9], cl                         | 41 d2 29                |
    | shr byte [r10], cl                        | 41 d2 2a                |
    | shr byte [r11], cl                        | 41 d2 2b                |
    | shr byte [r12], cl                        | 41 d2 2c 24             |
    | shr byte [r13], cl                        | 41 d2 6d 00             |
    | shr byte [r14], cl                        | 41 d2 2e                |
    | shr byte [r15], cl                        | 41 d2 2f                |
    | shr byte [rax + 1 * rcx], cl              | d2 2c 08                |
    | shr byte [rcx + 1 * rcx], cl              | d2 2c 09                |
    | shr byte [rdx + 1 * rcx], cl              | d2 2c 0a                |
    | shr byte [rbx + 1 * rcx], cl              | d2 2c 0b                |
    | shr byte [rsp + 1 * rcx], cl              | d2 2c 0c                |
    | shr byte [rbp + 1 * rcx], cl              | d2 6c 0d 00             |
    | shr byte [rsi + 1 * rcx], cl              | d2 2c 0e                |
    | shr byte [rdi + 1 * rcx], cl              | d2 2c 0f                |
    | shr byte [r8 + 1 * rcx], cl               | 41 d2 2c 08             |
    | shr byte [r9 + 1 * rcx], cl               | 41 d2 2c 09             |
    | shr byte [r10 + 1 * rcx], cl              | 41 d2 2c 0a             |
    | shr byte [r11 + 1 * rcx], cl              | 41 d2 2c 0b             |
    | shr byte [r12 + 1 * rcx], cl              | 41 d2 2c 0c             |
    | shr byte [r13 + 1 * rcx], cl              | 41 d2 6c 0d 00          |
    | shr byte [r14 + 1 * rcx], cl              | 41 d2 2c 0e             |
    | shr byte [r15 + 1 * rcx], cl              | 41 d2 2c 0f             |
    | shr byte [rax + 1 * rax], cl              | d2 2c 00                |
    | shr byte [rax + 1 * rdx], cl              | d2 2c 10                |
    | shr byte [rax + 1 * rbx], cl              | d2 2c 18                |
    | shr byte [rax + 1 * rbp], cl              | d2 2c 28                |
    | shr byte [rax + 1 * rsi], cl              | d2 2c 30                |
    | shr byte [rax + 1 * rdi], cl              | d2 2c 38                |
    | shr byte [rax + 1 * r8], cl               | 42 d2 2c 00             |
    | shr byte [rax + 1 * r9], cl               | 42 d2 2c 08             |
    | shr byte [rax + 1 * r10], cl              | 42 d2 2c 10             |
    | shr byte [rax + 1 * r11], cl              | 42 d2 2c 18             |
    | shr byte [rax + 1 * r12], cl              | 42 d2 2c 20             |
    | shr byte [rax + 1 * r13], cl              | 42 d2 2c 28             |
    | shr byte [rax + 1 * r14], cl              | 42 d2 2c 30             |
    | shr byte [rax + 1 * r15], cl              | 42 d2 2c 38             |
    | shr byte [rax + 2 * rcx], cl              | d2 2c 48                |
    | shr byte [rax + 4 * rcx], cl              | d2 2c 88                |
    | shr byte [rax + 8 * rcx], cl              | d2 2c c8                |
    | shr byte [r8 + 1 * r9], cl                | 43 d2 2c 08             |
    | shr byte [r8 + 2 * r9], cl                | 43 d2 2c 48             |
    | shr byte [r8 + 4 * r9], cl                | 43 d2 2c 88             |
    | shr byte [r8 + 8 * r9], cl                | 43 d2 2c c8             |
    | shr byte [1 * rcx], cl                    | d2 2c 0d 00 00 00 00    |
    | shr byte [2 * rcx], cl                    | d2 2c 4d 00 00 00 00    |
    | shr byte [4 * rcx], cl                    | d2 2c 8d 00 00 00 00    |
    | shr byte [8 * rcx], cl                    | d2 2c cd 00 00 00 00    |
    | shr byte [1 * r9], cl                     | 42 d2 2c 0d 00 00 00 00 |
    | shr byte [2 * r9], cl                     | 42 d2 2c 4d 00 00 00 00 |
    | shr byte [4 * r9], cl                     | 42 d2 2c 8d 00 00 00 00 |
    | shr byte [8 * r9], cl                     | 42 d2 2c cd 00 00 00 00 |
    | shr byte [r13 + 8 * r12], cl              | 43 d2 6c e5 00          |
    | shr byte [rsp + 4 * r15], cl              | 42 d2 2c bc             |
    | shr byte [rax + 1 * rcx + 0x00], cl       | d2 6c 08 00             |
    | shr byte [rax + 1 * rcx - 0x00], cl       | d2 6c 08 00             |
    | shr byte [rax + 1 * rcx + 0x01], cl       | d2 6c 08 01             |
    | shr byte [rax + 1 * rcx - 0x01], cl       | d2 6c 08 ff             |
    | shr byte [rax + 1 * rcx + 0x00000001], cl | d2 ac 08 01 00 00 00    |
    | shr byte [rax + 1 * rcx - 0x00000001], cl | d2 ac 08 ff ff ff ff    |
    | shr byte [rax + 1 * rcx + 0x7f], cl       | d2 6c 08 7f             |
    | shr byte [rax + 1 * rcx - 0x7f], cl       | d2 6c 08 81             |
    | shr byte [rax + 1 * rcx + 0x80], cl       | d2 ac 08 80 00 00 00    |
    | shr byte [rax + 1 * rcx - 0x80], cl       | d2 6c 08 80             |
    | shr byte [rax + 1 * rcx - 0x81], cl       | d2 ac 08 7f ff ff ff    |
    | shr byte [rax + 1 * rcx + 0xff], cl       | d2 ac 08 ff 00 00 00    |
    | shr byte [rax + 1 * rcx - 0xff], cl       | d2 ac 08 01 ff ff ff    |
    | shr byte [rax + 1 * rcx + 0x7fffffff], cl | d2 ac 08 ff ff ff 7f    |
    | shr byte [rax + 1 * rcx - 0x7fffffff], cl | d2 ac 08 01 00 00 80    |
    | shr byte [rax + 1 * rcx - 0x80000000], cl | d2 ac 08 00 00 00 80    |
    | shr byte [r10 + 0x7f], cl                 | 41 d2 6a 7f             |
    | shr byte [r10 + 0x80], cl                 | 41 d2 aa 80 00 00 00    |
    | shr byte [r10 - 0x80], cl                 | 41 d2 6a 80             |
    | shr byte [r10 - 0x81], cl                 | 41 d2 aa 7f ff ff ff    |
    | ----------------------------------------- | ----------------------- |
"""


def can_encode_shr_addr8_cl():
    encode(SHR_ADDR8_CL)
