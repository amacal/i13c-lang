from tests.encoding.core import encode, exhaust


def can_exhaust_sar():
    exhaust(
        SAR_ADDR16_CL,
        SAR_ADDR16_IMM8,
        SAR_ADDR32_CL,
        SAR_ADDR32_IMM8,
        SAR_ADDR64_CL,
        SAR_ADDR64_IMM8,
        SAR_ADDR8_CL,
        SAR_ADDR8_IMM8,
        SAR_REG16_CL,
        SAR_REG16_IMM8,
        SAR_REG32_CL,
        SAR_REG32_IMM8,
        SAR_REG64_CL,
        SAR_REG64_IMM8,
        SAR_REG8_CL,
        SAR_REG8_IMM8,
    )


SAR_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | sar rax, 0x01 | 48 d1 f8    | *** | sar rax, 0x00 | 48 c1 f8 00 |
    | sar rcx, 0x01 | 48 d1 f9    | *** | sar rax, 0x7f | 48 c1 f8 7f |
    | sar rdx, 0x01 | 48 d1 fa    | *** | sar rax, 0x80 | 48 c1 f8 80 |
    | sar rbx, 0x01 | 48 d1 fb    | *** | sar rax, 0xff | 48 c1 f8 ff |
    | sar rsp, 0x01 | 48 d1 fc    | *** | sar rcx, 0x7f | 48 c1 f9 7f |
    | sar rbp, 0x01 | 48 d1 fd    | *** | sar rdx, 0x80 | 48 c1 fa 80 |
    | sar rsi, 0x01 | 48 d1 fe    | *** | sar rbx, 0xff | 48 c1 fb ff |
    | sar rdi, 0x01 | 48 d1 ff    | *** | sar rsp, 0x00 | 48 c1 fc 00 |
    | sar r8, 0x01  | 49 d1 f8    | *** | sar rsi, 0x7f | 48 c1 fe 7f |
    | sar r9, 0x01  | 49 d1 f9    | *** | sar rdi, 0x80 | 48 c1 ff 80 |
    | sar r10, 0x01 | 49 d1 fa    | *** | sar r8, 0xff  | 49 c1 f8 ff |
    | sar r11, 0x01 | 49 d1 fb    | *** | sar r9, 0x00  | 49 c1 f9 00 |
    | sar r12, 0x01 | 49 d1 fc    | *** | sar r11, 0x7f | 49 c1 fb 7f |
    | sar r13, 0x01 | 49 d1 fd    | *** | sar r12, 0x80 | 49 c1 fc 80 |
    | sar r14, 0x01 | 49 d1 fe    | *** | sar r13, 0xff | 49 c1 fd ff |
    | sar r15, 0x01 | 49 d1 ff    | *** | sar r14, 0x00 | 49 c1 fe 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_sar_reg64_imm8():
    encode(SAR_REG64_IMM8)


SAR_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | sar rax, cl | 48 d3 f8 | *** | sar r8, cl  | 49 d3 f8 |
    | sar rcx, cl | 48 d3 f9 | *** | sar r9, cl  | 49 d3 f9 |
    | sar rdx, cl | 48 d3 fa | *** | sar r10, cl | 49 d3 fa |
    | sar rbx, cl | 48 d3 fb | *** | sar r11, cl | 49 d3 fb |
    | sar rsp, cl | 48 d3 fc | *** | sar r12, cl | 49 d3 fc |
    | sar rbp, cl | 48 d3 fd | *** | sar r13, cl | 49 d3 fd |
    | sar rsi, cl | 48 d3 fe | *** | sar r14, cl | 49 d3 fe |
    | sar rdi, cl | 48 d3 ff | *** | sar r15, cl | 49 d3 ff |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_sar_reg64_cl():
    encode(SAR_REG64_CL)


SAR_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sar eax, 0x01  | d1 f8       | *** | sar eax, 0x00  | c1 f8 00    |
    | sar ecx, 0x01  | d1 f9       | *** | sar eax, 0x7f  | c1 f8 7f    |
    | sar edx, 0x01  | d1 fa       | *** | sar eax, 0x80  | c1 f8 80    |
    | sar ebx, 0x01  | d1 fb       | *** | sar eax, 0xff  | c1 f8 ff    |
    | sar esp, 0x01  | d1 fc       | *** | sar ecx, 0x7f  | c1 f9 7f    |
    | sar ebp, 0x01  | d1 fd       | *** | sar edx, 0x80  | c1 fa 80    |
    | sar esi, 0x01  | d1 fe       | *** | sar ebx, 0xff  | c1 fb ff    |
    | sar edi, 0x01  | d1 ff       | *** | sar esp, 0x00  | c1 fc 00    |
    | sar r8d, 0x01  | 41 d1 f8    | *** | sar esi, 0x7f  | c1 fe 7f    |
    | sar r9d, 0x01  | 41 d1 f9    | *** | sar edi, 0x80  | c1 ff 80    |
    | sar r10d, 0x01 | 41 d1 fa    | *** | sar r8d, 0xff  | 41 c1 f8 ff |
    | sar r11d, 0x01 | 41 d1 fb    | *** | sar r9d, 0x00  | 41 c1 f9 00 |
    | sar r12d, 0x01 | 41 d1 fc    | *** | sar r11d, 0x7f | 41 c1 fb 7f |
    | sar r13d, 0x01 | 41 d1 fd    | *** | sar r12d, 0x80 | 41 c1 fc 80 |
    | sar r14d, 0x01 | 41 d1 fe    | *** | sar r13d, 0xff | 41 c1 fd ff |
    | sar r15d, 0x01 | 41 d1 ff    | *** | sar r14d, 0x00 | 41 c1 fe 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sar_reg32_imm8():
    encode(SAR_REG32_IMM8)


SAR_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | sar eax, cl  | d3 f8    | *** | sar r8d, cl  | 41 d3 f8 |
    | sar ecx, cl  | d3 f9    | *** | sar r9d, cl  | 41 d3 f9 |
    | sar edx, cl  | d3 fa    | *** | sar r10d, cl | 41 d3 fa |
    | sar ebx, cl  | d3 fb    | *** | sar r11d, cl | 41 d3 fb |
    | sar esp, cl  | d3 fc    | *** | sar r12d, cl | 41 d3 fc |
    | sar ebp, cl  | d3 fd    | *** | sar r13d, cl | 41 d3 fd |
    | sar esi, cl  | d3 fe    | *** | sar r14d, cl | 41 d3 fe |
    | sar edi, cl  | d3 ff    | *** | sar r15d, cl | 41 d3 ff |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_sar_reg32_cl():
    encode(SAR_REG32_CL)


SAR_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | sar ax, 0x01   | 66 d1 f8       | *** | sar ax, 0x00   | 66 c1 f8 00    |
    | sar cx, 0x01   | 66 d1 f9       | *** | sar ax, 0x7f   | 66 c1 f8 7f    |
    | sar dx, 0x01   | 66 d1 fa       | *** | sar ax, 0x80   | 66 c1 f8 80    |
    | sar bx, 0x01   | 66 d1 fb       | *** | sar ax, 0xff   | 66 c1 f8 ff    |
    | sar sp, 0x01   | 66 d1 fc       | *** | sar cx, 0x7f   | 66 c1 f9 7f    |
    | sar bp, 0x01   | 66 d1 fd       | *** | sar dx, 0x80   | 66 c1 fa 80    |
    | sar si, 0x01   | 66 d1 fe       | *** | sar bx, 0xff   | 66 c1 fb ff    |
    | sar di, 0x01   | 66 d1 ff       | *** | sar sp, 0x00   | 66 c1 fc 00    |
    | sar r8w, 0x01  | 66 41 d1 f8    | *** | sar si, 0x7f   | 66 c1 fe 7f    |
    | sar r9w, 0x01  | 66 41 d1 f9    | *** | sar di, 0x80   | 66 c1 ff 80    |
    | sar r10w, 0x01 | 66 41 d1 fa    | *** | sar r8w, 0xff  | 66 41 c1 f8 ff |
    | sar r11w, 0x01 | 66 41 d1 fb    | *** | sar r9w, 0x00  | 66 41 c1 f9 00 |
    | sar r12w, 0x01 | 66 41 d1 fc    | *** | sar r11w, 0x7f | 66 41 c1 fb 7f |
    | sar r13w, 0x01 | 66 41 d1 fd    | *** | sar r12w, 0x80 | 66 41 c1 fc 80 |
    | sar r14w, 0x01 | 66 41 d1 fe    | *** | sar r13w, 0xff | 66 41 c1 fd ff |
    | sar r15w, 0x01 | 66 41 d1 ff    | *** | sar r14w, 0x00 | 66 41 c1 fe 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_sar_reg16_imm8():
    encode(SAR_REG16_IMM8)


SAR_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | sar ax, cl   | 66 d3 f8    | *** | sar r8w, cl  | 66 41 d3 f8 |
    | sar cx, cl   | 66 d3 f9    | *** | sar r9w, cl  | 66 41 d3 f9 |
    | sar dx, cl   | 66 d3 fa    | *** | sar r10w, cl | 66 41 d3 fa |
    | sar bx, cl   | 66 d3 fb    | *** | sar r11w, cl | 66 41 d3 fb |
    | sar sp, cl   | 66 d3 fc    | *** | sar r12w, cl | 66 41 d3 fc |
    | sar bp, cl   | 66 d3 fd    | *** | sar r13w, cl | 66 41 d3 fd |
    | sar si, cl   | 66 d3 fe    | *** | sar r14w, cl | 66 41 d3 fe |
    | sar di, cl   | 66 d3 ff    | *** | sar r15w, cl | 66 41 d3 ff |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_sar_reg16_cl():
    encode(SAR_REG16_CL)


SAR_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | sar al, 0x01   | d0 f8       | *** | sar al, 0x00   | c0 f8 00    |
    | sar cl, 0x01   | d0 f9       | *** | sar al, 0x7f   | c0 f8 7f    |
    | sar dl, 0x01   | d0 fa       | *** | sar al, 0x80   | c0 f8 80    |
    | sar bl, 0x01   | d0 fb       | *** | sar al, 0xff   | c0 f8 ff    |
    | sar spl, 0x01  | 40 d0 fc    | *** | sar cl, 0x7f   | c0 f9 7f    |
    | sar bpl, 0x01  | 40 d0 fd    | *** | sar dl, 0x80   | c0 fa 80    |
    | sar sil, 0x01  | 40 d0 fe    | *** | sar bl, 0xff   | c0 fb ff    |
    | sar dil, 0x01  | 40 d0 ff    | *** | sar spl, 0x00  | 40 c0 fc 00 |
    | sar r8b, 0x01  | 41 d0 f8    | *** | sar sil, 0x7f  | 40 c0 fe 7f |
    | sar r9b, 0x01  | 41 d0 f9    | *** | sar dil, 0x80  | 40 c0 ff 80 |
    | sar r10b, 0x01 | 41 d0 fa    | *** | sar r8b, 0xff  | 41 c0 f8 ff |
    | sar r11b, 0x01 | 41 d0 fb    | *** | sar r9b, 0x00  | 41 c0 f9 00 |
    | sar r12b, 0x01 | 41 d0 fc    | *** | sar r11b, 0x7f | 41 c0 fb 7f |
    | sar r13b, 0x01 | 41 d0 fd    | *** | sar r12b, 0x80 | 41 c0 fc 80 |
    | sar r14b, 0x01 | 41 d0 fe    | *** | sar r13b, 0xff | 41 c0 fd ff |
    | sar r15b, 0x01 | 41 d0 ff    | *** | sar r14b, 0x00 | 41 c0 fe 00 |
    | sar ah, 0x01   | d0 fc       | *** | sar ah, 0x7f   | c0 fc 7f    |
    | sar ch, 0x01   | d0 fd       | *** | sar ch, 0x80   | c0 fd 80    |
    | sar dh, 0x01   | d0 fe       | *** | sar dh, 0xff   | c0 fe ff    |
    | sar bh, 0x01   | d0 ff       | *** | sar bh, 0x00   | c0 ff 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_sar_reg8_imm8():
    encode(SAR_REG8_IMM8)


SAR_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | sar al, cl   | d2 f8    | *** | sar r10b, cl | 41 d2 fa |
    | sar cl, cl   | d2 f9    | *** | sar r11b, cl | 41 d2 fb |
    | sar dl, cl   | d2 fa    | *** | sar r12b, cl | 41 d2 fc |
    | sar bl, cl   | d2 fb    | *** | sar r13b, cl | 41 d2 fd |
    | sar spl, cl  | 40 d2 fc | *** | sar r14b, cl | 41 d2 fe |
    | sar bpl, cl  | 40 d2 fd | *** | sar r15b, cl | 41 d2 ff |
    | sar sil, cl  | 40 d2 fe | *** | sar ah, cl   | d2 fc    |
    | sar dil, cl  | 40 d2 ff | *** | sar ch, cl   | d2 fd    |
    | sar r8b, cl  | 41 d2 f8 | *** | sar dh, cl   | d2 fe    |
    | sar r9b, cl  | 41 d2 f9 | *** | sar bh, cl   | d2 ff    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_sar_reg8_cl():
    encode(SAR_REG8_CL)


SAR_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sar qword [rax], 0x01                        | 48 d1 38                   |
    | sar qword [rcx], 0x01                        | 48 d1 39                   |
    | sar qword [rdx], 0x01                        | 48 d1 3a                   |
    | sar qword [rbx], 0x01                        | 48 d1 3b                   |
    | sar qword [rsp], 0x01                        | 48 d1 3c 24                |
    | sar qword [rbp], 0x01                        | 48 d1 7d 00                |
    | sar qword [rsi], 0x01                        | 48 d1 3e                   |
    | sar qword [rdi], 0x01                        | 48 d1 3f                   |
    | sar qword [r8], 0x01                         | 49 d1 38                   |
    | sar qword [r9], 0x01                         | 49 d1 39                   |
    | sar qword [r10], 0x01                        | 49 d1 3a                   |
    | sar qword [r11], 0x01                        | 49 d1 3b                   |
    | sar qword [r12], 0x01                        | 49 d1 3c 24                |
    | sar qword [r13], 0x01                        | 49 d1 7d 00                |
    | sar qword [r14], 0x01                        | 49 d1 3e                   |
    | sar qword [r15], 0x01                        | 49 d1 3f                   |
    | sar qword [rax + 1 * rcx], 0x01              | 48 d1 3c 08                |
    | sar qword [rcx + 1 * rcx], 0x01              | 48 d1 3c 09                |
    | sar qword [rdx + 1 * rcx], 0x01              | 48 d1 3c 0a                |
    | sar qword [rbx + 1 * rcx], 0x01              | 48 d1 3c 0b                |
    | sar qword [rsp + 1 * rcx], 0x01              | 48 d1 3c 0c                |
    | sar qword [rbp + 1 * rcx], 0x01              | 48 d1 7c 0d 00             |
    | sar qword [rsi + 1 * rcx], 0x01              | 48 d1 3c 0e                |
    | sar qword [rdi + 1 * rcx], 0x01              | 48 d1 3c 0f                |
    | sar qword [r8 + 1 * rcx], 0x01               | 49 d1 3c 08                |
    | sar qword [r9 + 1 * rcx], 0x01               | 49 d1 3c 09                |
    | sar qword [r10 + 1 * rcx], 0x01              | 49 d1 3c 0a                |
    | sar qword [r11 + 1 * rcx], 0x01              | 49 d1 3c 0b                |
    | sar qword [r12 + 1 * rcx], 0x01              | 49 d1 3c 0c                |
    | sar qword [r13 + 1 * rcx], 0x01              | 49 d1 7c 0d 00             |
    | sar qword [r14 + 1 * rcx], 0x01              | 49 d1 3c 0e                |
    | sar qword [r15 + 1 * rcx], 0x01              | 49 d1 3c 0f                |
    | sar qword [rax + 1 * rax], 0x01              | 48 d1 3c 00                |
    | sar qword [rax + 1 * rdx], 0x01              | 48 d1 3c 10                |
    | sar qword [rax + 1 * rbx], 0x01              | 48 d1 3c 18                |
    | sar qword [rax + 1 * rbp], 0x01              | 48 d1 3c 28                |
    | sar qword [rax + 1 * rsi], 0x01              | 48 d1 3c 30                |
    | sar qword [rax + 1 * rdi], 0x01              | 48 d1 3c 38                |
    | sar qword [rax + 1 * r8], 0x01               | 4a d1 3c 00                |
    | sar qword [rax + 1 * r9], 0x01               | 4a d1 3c 08                |
    | sar qword [rax + 1 * r10], 0x01              | 4a d1 3c 10                |
    | sar qword [rax + 1 * r11], 0x01              | 4a d1 3c 18                |
    | sar qword [rax + 1 * r12], 0x01              | 4a d1 3c 20                |
    | sar qword [rax + 1 * r13], 0x01              | 4a d1 3c 28                |
    | sar qword [rax + 1 * r14], 0x01              | 4a d1 3c 30                |
    | sar qword [rax + 1 * r15], 0x01              | 4a d1 3c 38                |
    | sar qword [rax + 2 * rcx], 0x01              | 48 d1 3c 48                |
    | sar qword [rax + 4 * rcx], 0x01              | 48 d1 3c 88                |
    | sar qword [rax + 8 * rcx], 0x01              | 48 d1 3c c8                |
    | sar qword [r8 + 1 * r9], 0x01                | 4b d1 3c 08                |
    | sar qword [r8 + 2 * r9], 0x01                | 4b d1 3c 48                |
    | sar qword [r8 + 4 * r9], 0x01                | 4b d1 3c 88                |
    | sar qword [r8 + 8 * r9], 0x01                | 4b d1 3c c8                |
    | sar qword [1 * rcx], 0x01                    | 48 d1 3c 0d 00 00 00 00    |
    | sar qword [2 * rcx], 0x01                    | 48 d1 3c 4d 00 00 00 00    |
    | sar qword [4 * rcx], 0x01                    | 48 d1 3c 8d 00 00 00 00    |
    | sar qword [8 * rcx], 0x01                    | 48 d1 3c cd 00 00 00 00    |
    | sar qword [1 * r9], 0x01                     | 4a d1 3c 0d 00 00 00 00    |
    | sar qword [2 * r9], 0x01                     | 4a d1 3c 4d 00 00 00 00    |
    | sar qword [4 * r9], 0x01                     | 4a d1 3c 8d 00 00 00 00    |
    | sar qword [8 * r9], 0x01                     | 4a d1 3c cd 00 00 00 00    |
    | sar qword [r13 + 8 * r12], 0x01              | 4b d1 7c e5 00             |
    | sar qword [rsp + 4 * r15], 0x01              | 4a d1 3c bc                |
    | sar qword [rax + 1 * rcx + 0x00], 0x01       | 48 d1 7c 08 00             |
    | sar qword [rax + 1 * rcx - 0x00], 0x01       | 48 d1 7c 08 00             |
    | sar qword [rax + 1 * rcx + 0x01], 0x01       | 48 d1 7c 08 01             |
    | sar qword [rax + 1 * rcx - 0x01], 0x01       | 48 d1 7c 08 ff             |
    | sar qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 d1 bc 08 01 00 00 00    |
    | sar qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 d1 bc 08 ff ff ff ff    |
    | sar qword [rax + 1 * rcx + 0x7f], 0x01       | 48 d1 7c 08 7f             |
    | sar qword [rax + 1 * rcx - 0x7f], 0x01       | 48 d1 7c 08 81             |
    | sar qword [rax + 1 * rcx + 0x80], 0x01       | 48 d1 bc 08 80 00 00 00    |
    | sar qword [rax + 1 * rcx - 0x80], 0x01       | 48 d1 7c 08 80             |
    | sar qword [rax + 1 * rcx - 0x81], 0x01       | 48 d1 bc 08 7f ff ff ff    |
    | sar qword [rax + 1 * rcx + 0xff], 0x01       | 48 d1 bc 08 ff 00 00 00    |
    | sar qword [rax + 1 * rcx - 0xff], 0x01       | 48 d1 bc 08 01 ff ff ff    |
    | sar qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 d1 bc 08 ff ff ff 7f    |
    | sar qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 d1 bc 08 01 00 00 80    |
    | sar qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 d1 bc 08 00 00 00 80    |
    | sar qword [r10 + 0x7f], 0x01                 | 49 d1 7a 7f                |
    | sar qword [r10 + 0x80], 0x01                 | 49 d1 ba 80 00 00 00       |
    | sar qword [r10 - 0x80], 0x01                 | 49 d1 7a 80                |
    | sar qword [r10 - 0x81], 0x01                 | 49 d1 ba 7f ff ff ff       |
    | sar qword [rax], 0x00                        | 48 c1 38 00                |
    | sar qword [rax], 0x7f                        | 48 c1 38 7f                |
    | sar qword [rax], 0x80                        | 48 c1 38 80                |
    | sar qword [rax], 0xff                        | 48 c1 38 ff                |
    | sar qword [rcx], 0x7f                        | 48 c1 39 7f                |
    | sar qword [rdx], 0x80                        | 48 c1 3a 80                |
    | sar qword [rbx], 0xff                        | 48 c1 3b ff                |
    | sar qword [rsp], 0x00                        | 48 c1 3c 24 00             |
    | sar qword [rsi], 0x7f                        | 48 c1 3e 7f                |
    | sar qword [rdi], 0x80                        | 48 c1 3f 80                |
    | sar qword [r8], 0xff                         | 49 c1 38 ff                |
    | sar qword [r9], 0x00                         | 49 c1 39 00                |
    | sar qword [r11], 0x7f                        | 49 c1 3b 7f                |
    | sar qword [r12], 0x80                        | 49 c1 3c 24 80             |
    | sar qword [r13], 0xff                        | 49 c1 7d 00 ff             |
    | sar qword [r14], 0x00                        | 49 c1 3e 00                |
    | sar qword [rax + 1 * rcx], 0x7f              | 48 c1 3c 08 7f             |
    | sar qword [rcx + 1 * rcx], 0x80              | 48 c1 3c 09 80             |
    | sar qword [rdx + 1 * rcx], 0xff              | 48 c1 3c 0a ff             |
    | sar qword [rbx + 1 * rcx], 0x00              | 48 c1 3c 0b 00             |
    | sar qword [rbp + 1 * rcx], 0x7f              | 48 c1 7c 0d 00 7f          |
    | sar qword [rsi + 1 * rcx], 0x80              | 48 c1 3c 0e 80             |
    | sar qword [rdi + 1 * rcx], 0xff              | 48 c1 3c 0f ff             |
    | sar qword [r8 + 1 * rcx], 0x00               | 49 c1 3c 08 00             |
    | sar qword [r10 + 1 * rcx], 0x7f              | 49 c1 3c 0a 7f             |
    | sar qword [r11 + 1 * rcx], 0x80              | 49 c1 3c 0b 80             |
    | sar qword [r12 + 1 * rcx], 0xff              | 49 c1 3c 0c ff             |
    | sar qword [r13 + 1 * rcx], 0x00              | 49 c1 7c 0d 00 00          |
    | sar qword [r15 + 1 * rcx], 0x7f              | 49 c1 3c 0f 7f             |
    | sar qword [rax + 1 * rax], 0x80              | 48 c1 3c 00 80             |
    | sar qword [rax + 1 * rdx], 0xff              | 48 c1 3c 10 ff             |
    | sar qword [rax + 1 * rbx], 0x00              | 48 c1 3c 18 00             |
    | sar qword [rax + 1 * rsi], 0x7f              | 48 c1 3c 30 7f             |
    | sar qword [rax + 1 * rdi], 0x80              | 48 c1 3c 38 80             |
    | sar qword [rax + 1 * r8], 0xff               | 4a c1 3c 00 ff             |
    | sar qword [rax + 1 * r9], 0x00               | 4a c1 3c 08 00             |
    | sar qword [rax + 1 * r11], 0x7f              | 4a c1 3c 18 7f             |
    | sar qword [rax + 1 * r12], 0x80              | 4a c1 3c 20 80             |
    | sar qword [rax + 1 * r13], 0xff              | 4a c1 3c 28 ff             |
    | sar qword [rax + 1 * r14], 0x00              | 4a c1 3c 30 00             |
    | sar qword [rax + 2 * rcx], 0x7f              | 48 c1 3c 48 7f             |
    | sar qword [rax + 4 * rcx], 0x80              | 48 c1 3c 88 80             |
    | sar qword [rax + 8 * rcx], 0xff              | 48 c1 3c c8 ff             |
    | sar qword [r8 + 1 * r9], 0x00                | 4b c1 3c 08 00             |
    | sar qword [r8 + 4 * r9], 0x7f                | 4b c1 3c 88 7f             |
    | sar qword [r8 + 8 * r9], 0x80                | 4b c1 3c c8 80             |
    | sar qword [1 * rcx], 0xff                    | 48 c1 3c 0d 00 00 00 00 ff |
    | sar qword [2 * rcx], 0x00                    | 48 c1 3c 4d 00 00 00 00 00 |
    | sar qword [8 * rcx], 0x7f                    | 48 c1 3c cd 00 00 00 00 7f |
    | sar qword [1 * r9], 0x80                     | 4a c1 3c 0d 00 00 00 00 80 |
    | sar qword [2 * r9], 0xff                     | 4a c1 3c 4d 00 00 00 00 ff |
    | sar qword [4 * r9], 0x00                     | 4a c1 3c 8d 00 00 00 00 00 |
    | sar qword [r13 + 8 * r12], 0x7f              | 4b c1 7c e5 00 7f          |
    | sar qword [rsp + 4 * r15], 0x80              | 4a c1 3c bc 80             |
    | sar qword [rax + 1 * rcx + 0x00], 0xff       | 48 c1 7c 08 00 ff          |
    | sar qword [rax + 1 * rcx - 0x00], 0x00       | 48 c1 7c 08 00 00          |
    | sar qword [rax + 1 * rcx - 0x01], 0x7f       | 48 c1 7c 08 ff 7f          |
    | sar qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 c1 bc 08 01 00 00 00 80 |
    | sar qword [rax + 1 * rcx - 0x00000001], 0xff | 48 c1 bc 08 ff ff ff ff ff |
    | sar qword [rax + 1 * rcx + 0x7f], 0x00       | 48 c1 7c 08 7f 00          |
    | sar qword [rax + 1 * rcx + 0x80], 0x7f       | 48 c1 bc 08 80 00 00 00 7f |
    | sar qword [rax + 1 * rcx - 0x80], 0x80       | 48 c1 7c 08 80 80          |
    | sar qword [rax + 1 * rcx - 0x81], 0xff       | 48 c1 bc 08 7f ff ff ff ff |
    | sar qword [rax + 1 * rcx + 0xff], 0x00       | 48 c1 bc 08 ff 00 00 00 00 |
    | sar qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 c1 bc 08 ff ff ff 7f 7f |
    | sar qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 c1 bc 08 01 00 00 80 80 |
    | sar qword [rax + 1 * rcx - 0x80000000], 0xff | 48 c1 bc 08 00 00 00 80 ff |
    | sar qword [r10 + 0x7f], 0x00                 | 49 c1 7a 7f 00             |
    | sar qword [r10 - 0x80], 0x7f                 | 49 c1 7a 80 7f             |
    | sar qword [r10 - 0x81], 0x80                 | 49 c1 ba 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sar_addr64_imm8():
    encode(SAR_ADDR64_IMM8)


SAR_ADDR64_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | sar qword [rax], cl                        | 48 d3 38                |
    | sar qword [rcx], cl                        | 48 d3 39                |
    | sar qword [rdx], cl                        | 48 d3 3a                |
    | sar qword [rbx], cl                        | 48 d3 3b                |
    | sar qword [rsp], cl                        | 48 d3 3c 24             |
    | sar qword [rbp], cl                        | 48 d3 7d 00             |
    | sar qword [rsi], cl                        | 48 d3 3e                |
    | sar qword [rdi], cl                        | 48 d3 3f                |
    | sar qword [r8], cl                         | 49 d3 38                |
    | sar qword [r9], cl                         | 49 d3 39                |
    | sar qword [r10], cl                        | 49 d3 3a                |
    | sar qword [r11], cl                        | 49 d3 3b                |
    | sar qword [r12], cl                        | 49 d3 3c 24             |
    | sar qword [r13], cl                        | 49 d3 7d 00             |
    | sar qword [r14], cl                        | 49 d3 3e                |
    | sar qword [r15], cl                        | 49 d3 3f                |
    | sar qword [rax + 1 * rcx], cl              | 48 d3 3c 08             |
    | sar qword [rcx + 1 * rcx], cl              | 48 d3 3c 09             |
    | sar qword [rdx + 1 * rcx], cl              | 48 d3 3c 0a             |
    | sar qword [rbx + 1 * rcx], cl              | 48 d3 3c 0b             |
    | sar qword [rsp + 1 * rcx], cl              | 48 d3 3c 0c             |
    | sar qword [rbp + 1 * rcx], cl              | 48 d3 7c 0d 00          |
    | sar qword [rsi + 1 * rcx], cl              | 48 d3 3c 0e             |
    | sar qword [rdi + 1 * rcx], cl              | 48 d3 3c 0f             |
    | sar qword [r8 + 1 * rcx], cl               | 49 d3 3c 08             |
    | sar qword [r9 + 1 * rcx], cl               | 49 d3 3c 09             |
    | sar qword [r10 + 1 * rcx], cl              | 49 d3 3c 0a             |
    | sar qword [r11 + 1 * rcx], cl              | 49 d3 3c 0b             |
    | sar qword [r12 + 1 * rcx], cl              | 49 d3 3c 0c             |
    | sar qword [r13 + 1 * rcx], cl              | 49 d3 7c 0d 00          |
    | sar qword [r14 + 1 * rcx], cl              | 49 d3 3c 0e             |
    | sar qword [r15 + 1 * rcx], cl              | 49 d3 3c 0f             |
    | sar qword [rax + 1 * rax], cl              | 48 d3 3c 00             |
    | sar qword [rax + 1 * rdx], cl              | 48 d3 3c 10             |
    | sar qword [rax + 1 * rbx], cl              | 48 d3 3c 18             |
    | sar qword [rax + 1 * rbp], cl              | 48 d3 3c 28             |
    | sar qword [rax + 1 * rsi], cl              | 48 d3 3c 30             |
    | sar qword [rax + 1 * rdi], cl              | 48 d3 3c 38             |
    | sar qword [rax + 1 * r8], cl               | 4a d3 3c 00             |
    | sar qword [rax + 1 * r9], cl               | 4a d3 3c 08             |
    | sar qword [rax + 1 * r10], cl              | 4a d3 3c 10             |
    | sar qword [rax + 1 * r11], cl              | 4a d3 3c 18             |
    | sar qword [rax + 1 * r12], cl              | 4a d3 3c 20             |
    | sar qword [rax + 1 * r13], cl              | 4a d3 3c 28             |
    | sar qword [rax + 1 * r14], cl              | 4a d3 3c 30             |
    | sar qword [rax + 1 * r15], cl              | 4a d3 3c 38             |
    | sar qword [rax + 2 * rcx], cl              | 48 d3 3c 48             |
    | sar qword [rax + 4 * rcx], cl              | 48 d3 3c 88             |
    | sar qword [rax + 8 * rcx], cl              | 48 d3 3c c8             |
    | sar qword [r8 + 1 * r9], cl                | 4b d3 3c 08             |
    | sar qword [r8 + 2 * r9], cl                | 4b d3 3c 48             |
    | sar qword [r8 + 4 * r9], cl                | 4b d3 3c 88             |
    | sar qword [r8 + 8 * r9], cl                | 4b d3 3c c8             |
    | sar qword [1 * rcx], cl                    | 48 d3 3c 0d 00 00 00 00 |
    | sar qword [2 * rcx], cl                    | 48 d3 3c 4d 00 00 00 00 |
    | sar qword [4 * rcx], cl                    | 48 d3 3c 8d 00 00 00 00 |
    | sar qword [8 * rcx], cl                    | 48 d3 3c cd 00 00 00 00 |
    | sar qword [1 * r9], cl                     | 4a d3 3c 0d 00 00 00 00 |
    | sar qword [2 * r9], cl                     | 4a d3 3c 4d 00 00 00 00 |
    | sar qword [4 * r9], cl                     | 4a d3 3c 8d 00 00 00 00 |
    | sar qword [8 * r9], cl                     | 4a d3 3c cd 00 00 00 00 |
    | sar qword [r13 + 8 * r12], cl              | 4b d3 7c e5 00          |
    | sar qword [rsp + 4 * r15], cl              | 4a d3 3c bc             |
    | sar qword [rax + 1 * rcx + 0x00], cl       | 48 d3 7c 08 00          |
    | sar qword [rax + 1 * rcx - 0x00], cl       | 48 d3 7c 08 00          |
    | sar qword [rax + 1 * rcx + 0x01], cl       | 48 d3 7c 08 01          |
    | sar qword [rax + 1 * rcx - 0x01], cl       | 48 d3 7c 08 ff          |
    | sar qword [rax + 1 * rcx + 0x00000001], cl | 48 d3 bc 08 01 00 00 00 |
    | sar qword [rax + 1 * rcx - 0x00000001], cl | 48 d3 bc 08 ff ff ff ff |
    | sar qword [rax + 1 * rcx + 0x7f], cl       | 48 d3 7c 08 7f          |
    | sar qword [rax + 1 * rcx - 0x7f], cl       | 48 d3 7c 08 81          |
    | sar qword [rax + 1 * rcx + 0x80], cl       | 48 d3 bc 08 80 00 00 00 |
    | sar qword [rax + 1 * rcx - 0x80], cl       | 48 d3 7c 08 80          |
    | sar qword [rax + 1 * rcx - 0x81], cl       | 48 d3 bc 08 7f ff ff ff |
    | sar qword [rax + 1 * rcx + 0xff], cl       | 48 d3 bc 08 ff 00 00 00 |
    | sar qword [rax + 1 * rcx - 0xff], cl       | 48 d3 bc 08 01 ff ff ff |
    | sar qword [rax + 1 * rcx + 0x7fffffff], cl | 48 d3 bc 08 ff ff ff 7f |
    | sar qword [rax + 1 * rcx - 0x7fffffff], cl | 48 d3 bc 08 01 00 00 80 |
    | sar qword [rax + 1 * rcx - 0x80000000], cl | 48 d3 bc 08 00 00 00 80 |
    | sar qword [r10 + 0x7f], cl                 | 49 d3 7a 7f             |
    | sar qword [r10 + 0x80], cl                 | 49 d3 ba 80 00 00 00    |
    | sar qword [r10 - 0x80], cl                 | 49 d3 7a 80             |
    | sar qword [r10 - 0x81], cl                 | 49 d3 ba 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_sar_addr64_cl():
    encode(SAR_ADDR64_CL)


SAR_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | sar dword [rax], 0x01                        | d1 38                      |
    | sar dword [rcx], 0x01                        | d1 39                      |
    | sar dword [rdx], 0x01                        | d1 3a                      |
    | sar dword [rbx], 0x01                        | d1 3b                      |
    | sar dword [rsp], 0x01                        | d1 3c 24                   |
    | sar dword [rbp], 0x01                        | d1 7d 00                   |
    | sar dword [rsi], 0x01                        | d1 3e                      |
    | sar dword [rdi], 0x01                        | d1 3f                      |
    | sar dword [r8], 0x01                         | 41 d1 38                   |
    | sar dword [r9], 0x01                         | 41 d1 39                   |
    | sar dword [r10], 0x01                        | 41 d1 3a                   |
    | sar dword [r11], 0x01                        | 41 d1 3b                   |
    | sar dword [r12], 0x01                        | 41 d1 3c 24                |
    | sar dword [r13], 0x01                        | 41 d1 7d 00                |
    | sar dword [r14], 0x01                        | 41 d1 3e                   |
    | sar dword [r15], 0x01                        | 41 d1 3f                   |
    | sar dword [rax + 1 * rcx], 0x01              | d1 3c 08                   |
    | sar dword [rcx + 1 * rcx], 0x01              | d1 3c 09                   |
    | sar dword [rdx + 1 * rcx], 0x01              | d1 3c 0a                   |
    | sar dword [rbx + 1 * rcx], 0x01              | d1 3c 0b                   |
    | sar dword [rsp + 1 * rcx], 0x01              | d1 3c 0c                   |
    | sar dword [rbp + 1 * rcx], 0x01              | d1 7c 0d 00                |
    | sar dword [rsi + 1 * rcx], 0x01              | d1 3c 0e                   |
    | sar dword [rdi + 1 * rcx], 0x01              | d1 3c 0f                   |
    | sar dword [r8 + 1 * rcx], 0x01               | 41 d1 3c 08                |
    | sar dword [r9 + 1 * rcx], 0x01               | 41 d1 3c 09                |
    | sar dword [r10 + 1 * rcx], 0x01              | 41 d1 3c 0a                |
    | sar dword [r11 + 1 * rcx], 0x01              | 41 d1 3c 0b                |
    | sar dword [r12 + 1 * rcx], 0x01              | 41 d1 3c 0c                |
    | sar dword [r13 + 1 * rcx], 0x01              | 41 d1 7c 0d 00             |
    | sar dword [r14 + 1 * rcx], 0x01              | 41 d1 3c 0e                |
    | sar dword [r15 + 1 * rcx], 0x01              | 41 d1 3c 0f                |
    | sar dword [rax + 1 * rax], 0x01              | d1 3c 00                   |
    | sar dword [rax + 1 * rdx], 0x01              | d1 3c 10                   |
    | sar dword [rax + 1 * rbx], 0x01              | d1 3c 18                   |
    | sar dword [rax + 1 * rbp], 0x01              | d1 3c 28                   |
    | sar dword [rax + 1 * rsi], 0x01              | d1 3c 30                   |
    | sar dword [rax + 1 * rdi], 0x01              | d1 3c 38                   |
    | sar dword [rax + 1 * r8], 0x01               | 42 d1 3c 00                |
    | sar dword [rax + 1 * r9], 0x01               | 42 d1 3c 08                |
    | sar dword [rax + 1 * r10], 0x01              | 42 d1 3c 10                |
    | sar dword [rax + 1 * r11], 0x01              | 42 d1 3c 18                |
    | sar dword [rax + 1 * r12], 0x01              | 42 d1 3c 20                |
    | sar dword [rax + 1 * r13], 0x01              | 42 d1 3c 28                |
    | sar dword [rax + 1 * r14], 0x01              | 42 d1 3c 30                |
    | sar dword [rax + 1 * r15], 0x01              | 42 d1 3c 38                |
    | sar dword [rax + 2 * rcx], 0x01              | d1 3c 48                   |
    | sar dword [rax + 4 * rcx], 0x01              | d1 3c 88                   |
    | sar dword [rax + 8 * rcx], 0x01              | d1 3c c8                   |
    | sar dword [r8 + 1 * r9], 0x01                | 43 d1 3c 08                |
    | sar dword [r8 + 2 * r9], 0x01                | 43 d1 3c 48                |
    | sar dword [r8 + 4 * r9], 0x01                | 43 d1 3c 88                |
    | sar dword [r8 + 8 * r9], 0x01                | 43 d1 3c c8                |
    | sar dword [1 * rcx], 0x01                    | d1 3c 0d 00 00 00 00       |
    | sar dword [2 * rcx], 0x01                    | d1 3c 4d 00 00 00 00       |
    | sar dword [4 * rcx], 0x01                    | d1 3c 8d 00 00 00 00       |
    | sar dword [8 * rcx], 0x01                    | d1 3c cd 00 00 00 00       |
    | sar dword [1 * r9], 0x01                     | 42 d1 3c 0d 00 00 00 00    |
    | sar dword [2 * r9], 0x01                     | 42 d1 3c 4d 00 00 00 00    |
    | sar dword [4 * r9], 0x01                     | 42 d1 3c 8d 00 00 00 00    |
    | sar dword [8 * r9], 0x01                     | 42 d1 3c cd 00 00 00 00    |
    | sar dword [r13 + 8 * r12], 0x01              | 43 d1 7c e5 00             |
    | sar dword [rsp + 4 * r15], 0x01              | 42 d1 3c bc                |
    | sar dword [rax + 1 * rcx + 0x00], 0x01       | d1 7c 08 00                |
    | sar dword [rax + 1 * rcx - 0x00], 0x01       | d1 7c 08 00                |
    | sar dword [rax + 1 * rcx + 0x01], 0x01       | d1 7c 08 01                |
    | sar dword [rax + 1 * rcx - 0x01], 0x01       | d1 7c 08 ff                |
    | sar dword [rax + 1 * rcx + 0x00000001], 0x01 | d1 bc 08 01 00 00 00       |
    | sar dword [rax + 1 * rcx - 0x00000001], 0x01 | d1 bc 08 ff ff ff ff       |
    | sar dword [rax + 1 * rcx + 0x7f], 0x01       | d1 7c 08 7f                |
    | sar dword [rax + 1 * rcx - 0x7f], 0x01       | d1 7c 08 81                |
    | sar dword [rax + 1 * rcx + 0x80], 0x01       | d1 bc 08 80 00 00 00       |
    | sar dword [rax + 1 * rcx - 0x80], 0x01       | d1 7c 08 80                |
    | sar dword [rax + 1 * rcx - 0x81], 0x01       | d1 bc 08 7f ff ff ff       |
    | sar dword [rax + 1 * rcx + 0xff], 0x01       | d1 bc 08 ff 00 00 00       |
    | sar dword [rax + 1 * rcx - 0xff], 0x01       | d1 bc 08 01 ff ff ff       |
    | sar dword [rax + 1 * rcx + 0x7fffffff], 0x01 | d1 bc 08 ff ff ff 7f       |
    | sar dword [rax + 1 * rcx - 0x7fffffff], 0x01 | d1 bc 08 01 00 00 80       |
    | sar dword [rax + 1 * rcx - 0x80000000], 0x01 | d1 bc 08 00 00 00 80       |
    | sar dword [r10 + 0x7f], 0x01                 | 41 d1 7a 7f                |
    | sar dword [r10 + 0x80], 0x01                 | 41 d1 ba 80 00 00 00       |
    | sar dword [r10 - 0x80], 0x01                 | 41 d1 7a 80                |
    | sar dword [r10 - 0x81], 0x01                 | 41 d1 ba 7f ff ff ff       |
    | sar dword [rax], 0x00                        | c1 38 00                   |
    | sar dword [rax], 0x7f                        | c1 38 7f                   |
    | sar dword [rax], 0x80                        | c1 38 80                   |
    | sar dword [rax], 0xff                        | c1 38 ff                   |
    | sar dword [rcx], 0x7f                        | c1 39 7f                   |
    | sar dword [rdx], 0x80                        | c1 3a 80                   |
    | sar dword [rbx], 0xff                        | c1 3b ff                   |
    | sar dword [rsp], 0x00                        | c1 3c 24 00                |
    | sar dword [rsi], 0x7f                        | c1 3e 7f                   |
    | sar dword [rdi], 0x80                        | c1 3f 80                   |
    | sar dword [r8], 0xff                         | 41 c1 38 ff                |
    | sar dword [r9], 0x00                         | 41 c1 39 00                |
    | sar dword [r11], 0x7f                        | 41 c1 3b 7f                |
    | sar dword [r12], 0x80                        | 41 c1 3c 24 80             |
    | sar dword [r13], 0xff                        | 41 c1 7d 00 ff             |
    | sar dword [r14], 0x00                        | 41 c1 3e 00                |
    | sar dword [rax + 1 * rcx], 0x7f              | c1 3c 08 7f                |
    | sar dword [rcx + 1 * rcx], 0x80              | c1 3c 09 80                |
    | sar dword [rdx + 1 * rcx], 0xff              | c1 3c 0a ff                |
    | sar dword [rbx + 1 * rcx], 0x00              | c1 3c 0b 00                |
    | sar dword [rbp + 1 * rcx], 0x7f              | c1 7c 0d 00 7f             |
    | sar dword [rsi + 1 * rcx], 0x80              | c1 3c 0e 80                |
    | sar dword [rdi + 1 * rcx], 0xff              | c1 3c 0f ff                |
    | sar dword [r8 + 1 * rcx], 0x00               | 41 c1 3c 08 00             |
    | sar dword [r10 + 1 * rcx], 0x7f              | 41 c1 3c 0a 7f             |
    | sar dword [r11 + 1 * rcx], 0x80              | 41 c1 3c 0b 80             |
    | sar dword [r12 + 1 * rcx], 0xff              | 41 c1 3c 0c ff             |
    | sar dword [r13 + 1 * rcx], 0x00              | 41 c1 7c 0d 00 00          |
    | sar dword [r15 + 1 * rcx], 0x7f              | 41 c1 3c 0f 7f             |
    | sar dword [rax + 1 * rax], 0x80              | c1 3c 00 80                |
    | sar dword [rax + 1 * rdx], 0xff              | c1 3c 10 ff                |
    | sar dword [rax + 1 * rbx], 0x00              | c1 3c 18 00                |
    | sar dword [rax + 1 * rsi], 0x7f              | c1 3c 30 7f                |
    | sar dword [rax + 1 * rdi], 0x80              | c1 3c 38 80                |
    | sar dword [rax + 1 * r8], 0xff               | 42 c1 3c 00 ff             |
    | sar dword [rax + 1 * r9], 0x00               | 42 c1 3c 08 00             |
    | sar dword [rax + 1 * r11], 0x7f              | 42 c1 3c 18 7f             |
    | sar dword [rax + 1 * r12], 0x80              | 42 c1 3c 20 80             |
    | sar dword [rax + 1 * r13], 0xff              | 42 c1 3c 28 ff             |
    | sar dword [rax + 1 * r14], 0x00              | 42 c1 3c 30 00             |
    | sar dword [rax + 2 * rcx], 0x7f              | c1 3c 48 7f                |
    | sar dword [rax + 4 * rcx], 0x80              | c1 3c 88 80                |
    | sar dword [rax + 8 * rcx], 0xff              | c1 3c c8 ff                |
    | sar dword [r8 + 1 * r9], 0x00                | 43 c1 3c 08 00             |
    | sar dword [r8 + 4 * r9], 0x7f                | 43 c1 3c 88 7f             |
    | sar dword [r8 + 8 * r9], 0x80                | 43 c1 3c c8 80             |
    | sar dword [1 * rcx], 0xff                    | c1 3c 0d 00 00 00 00 ff    |
    | sar dword [2 * rcx], 0x00                    | c1 3c 4d 00 00 00 00 00    |
    | sar dword [8 * rcx], 0x7f                    | c1 3c cd 00 00 00 00 7f    |
    | sar dword [1 * r9], 0x80                     | 42 c1 3c 0d 00 00 00 00 80 |
    | sar dword [2 * r9], 0xff                     | 42 c1 3c 4d 00 00 00 00 ff |
    | sar dword [4 * r9], 0x00                     | 42 c1 3c 8d 00 00 00 00 00 |
    | sar dword [r13 + 8 * r12], 0x7f              | 43 c1 7c e5 00 7f          |
    | sar dword [rsp + 4 * r15], 0x80              | 42 c1 3c bc 80             |
    | sar dword [rax + 1 * rcx + 0x00], 0xff       | c1 7c 08 00 ff             |
    | sar dword [rax + 1 * rcx - 0x00], 0x00       | c1 7c 08 00 00             |
    | sar dword [rax + 1 * rcx - 0x01], 0x7f       | c1 7c 08 ff 7f             |
    | sar dword [rax + 1 * rcx + 0x00000001], 0x80 | c1 bc 08 01 00 00 00 80    |
    | sar dword [rax + 1 * rcx - 0x00000001], 0xff | c1 bc 08 ff ff ff ff ff    |
    | sar dword [rax + 1 * rcx + 0x7f], 0x00       | c1 7c 08 7f 00             |
    | sar dword [rax + 1 * rcx + 0x80], 0x7f       | c1 bc 08 80 00 00 00 7f    |
    | sar dword [rax + 1 * rcx - 0x80], 0x80       | c1 7c 08 80 80             |
    | sar dword [rax + 1 * rcx - 0x81], 0xff       | c1 bc 08 7f ff ff ff ff    |
    | sar dword [rax + 1 * rcx + 0xff], 0x00       | c1 bc 08 ff 00 00 00 00    |
    | sar dword [rax + 1 * rcx + 0x7fffffff], 0x7f | c1 bc 08 ff ff ff 7f 7f    |
    | sar dword [rax + 1 * rcx - 0x7fffffff], 0x80 | c1 bc 08 01 00 00 80 80    |
    | sar dword [rax + 1 * rcx - 0x80000000], 0xff | c1 bc 08 00 00 00 80 ff    |
    | sar dword [r10 + 0x7f], 0x00                 | 41 c1 7a 7f 00             |
    | sar dword [r10 - 0x80], 0x7f                 | 41 c1 7a 80 7f             |
    | sar dword [r10 - 0x81], 0x80                 | 41 c1 ba 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_sar_addr32_imm8():
    encode(SAR_ADDR32_IMM8)


SAR_ADDR32_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | sar dword [rax], cl                        | d3 38                   |
    | sar dword [rcx], cl                        | d3 39                   |
    | sar dword [rdx], cl                        | d3 3a                   |
    | sar dword [rbx], cl                        | d3 3b                   |
    | sar dword [rsp], cl                        | d3 3c 24                |
    | sar dword [rbp], cl                        | d3 7d 00                |
    | sar dword [rsi], cl                        | d3 3e                   |
    | sar dword [rdi], cl                        | d3 3f                   |
    | sar dword [r8], cl                         | 41 d3 38                |
    | sar dword [r9], cl                         | 41 d3 39                |
    | sar dword [r10], cl                        | 41 d3 3a                |
    | sar dword [r11], cl                        | 41 d3 3b                |
    | sar dword [r12], cl                        | 41 d3 3c 24             |
    | sar dword [r13], cl                        | 41 d3 7d 00             |
    | sar dword [r14], cl                        | 41 d3 3e                |
    | sar dword [r15], cl                        | 41 d3 3f                |
    | sar dword [rax + 1 * rcx], cl              | d3 3c 08                |
    | sar dword [rcx + 1 * rcx], cl              | d3 3c 09                |
    | sar dword [rdx + 1 * rcx], cl              | d3 3c 0a                |
    | sar dword [rbx + 1 * rcx], cl              | d3 3c 0b                |
    | sar dword [rsp + 1 * rcx], cl              | d3 3c 0c                |
    | sar dword [rbp + 1 * rcx], cl              | d3 7c 0d 00             |
    | sar dword [rsi + 1 * rcx], cl              | d3 3c 0e                |
    | sar dword [rdi + 1 * rcx], cl              | d3 3c 0f                |
    | sar dword [r8 + 1 * rcx], cl               | 41 d3 3c 08             |
    | sar dword [r9 + 1 * rcx], cl               | 41 d3 3c 09             |
    | sar dword [r10 + 1 * rcx], cl              | 41 d3 3c 0a             |
    | sar dword [r11 + 1 * rcx], cl              | 41 d3 3c 0b             |
    | sar dword [r12 + 1 * rcx], cl              | 41 d3 3c 0c             |
    | sar dword [r13 + 1 * rcx], cl              | 41 d3 7c 0d 00          |
    | sar dword [r14 + 1 * rcx], cl              | 41 d3 3c 0e             |
    | sar dword [r15 + 1 * rcx], cl              | 41 d3 3c 0f             |
    | sar dword [rax + 1 * rax], cl              | d3 3c 00                |
    | sar dword [rax + 1 * rdx], cl              | d3 3c 10                |
    | sar dword [rax + 1 * rbx], cl              | d3 3c 18                |
    | sar dword [rax + 1 * rbp], cl              | d3 3c 28                |
    | sar dword [rax + 1 * rsi], cl              | d3 3c 30                |
    | sar dword [rax + 1 * rdi], cl              | d3 3c 38                |
    | sar dword [rax + 1 * r8], cl               | 42 d3 3c 00             |
    | sar dword [rax + 1 * r9], cl               | 42 d3 3c 08             |
    | sar dword [rax + 1 * r10], cl              | 42 d3 3c 10             |
    | sar dword [rax + 1 * r11], cl              | 42 d3 3c 18             |
    | sar dword [rax + 1 * r12], cl              | 42 d3 3c 20             |
    | sar dword [rax + 1 * r13], cl              | 42 d3 3c 28             |
    | sar dword [rax + 1 * r14], cl              | 42 d3 3c 30             |
    | sar dword [rax + 1 * r15], cl              | 42 d3 3c 38             |
    | sar dword [rax + 2 * rcx], cl              | d3 3c 48                |
    | sar dword [rax + 4 * rcx], cl              | d3 3c 88                |
    | sar dword [rax + 8 * rcx], cl              | d3 3c c8                |
    | sar dword [r8 + 1 * r9], cl                | 43 d3 3c 08             |
    | sar dword [r8 + 2 * r9], cl                | 43 d3 3c 48             |
    | sar dword [r8 + 4 * r9], cl                | 43 d3 3c 88             |
    | sar dword [r8 + 8 * r9], cl                | 43 d3 3c c8             |
    | sar dword [1 * rcx], cl                    | d3 3c 0d 00 00 00 00    |
    | sar dword [2 * rcx], cl                    | d3 3c 4d 00 00 00 00    |
    | sar dword [4 * rcx], cl                    | d3 3c 8d 00 00 00 00    |
    | sar dword [8 * rcx], cl                    | d3 3c cd 00 00 00 00    |
    | sar dword [1 * r9], cl                     | 42 d3 3c 0d 00 00 00 00 |
    | sar dword [2 * r9], cl                     | 42 d3 3c 4d 00 00 00 00 |
    | sar dword [4 * r9], cl                     | 42 d3 3c 8d 00 00 00 00 |
    | sar dword [8 * r9], cl                     | 42 d3 3c cd 00 00 00 00 |
    | sar dword [r13 + 8 * r12], cl              | 43 d3 7c e5 00          |
    | sar dword [rsp + 4 * r15], cl              | 42 d3 3c bc             |
    | sar dword [rax + 1 * rcx + 0x00], cl       | d3 7c 08 00             |
    | sar dword [rax + 1 * rcx - 0x00], cl       | d3 7c 08 00             |
    | sar dword [rax + 1 * rcx + 0x01], cl       | d3 7c 08 01             |
    | sar dword [rax + 1 * rcx - 0x01], cl       | d3 7c 08 ff             |
    | sar dword [rax + 1 * rcx + 0x00000001], cl | d3 bc 08 01 00 00 00    |
    | sar dword [rax + 1 * rcx - 0x00000001], cl | d3 bc 08 ff ff ff ff    |
    | sar dword [rax + 1 * rcx + 0x7f], cl       | d3 7c 08 7f             |
    | sar dword [rax + 1 * rcx - 0x7f], cl       | d3 7c 08 81             |
    | sar dword [rax + 1 * rcx + 0x80], cl       | d3 bc 08 80 00 00 00    |
    | sar dword [rax + 1 * rcx - 0x80], cl       | d3 7c 08 80             |
    | sar dword [rax + 1 * rcx - 0x81], cl       | d3 bc 08 7f ff ff ff    |
    | sar dword [rax + 1 * rcx + 0xff], cl       | d3 bc 08 ff 00 00 00    |
    | sar dword [rax + 1 * rcx - 0xff], cl       | d3 bc 08 01 ff ff ff    |
    | sar dword [rax + 1 * rcx + 0x7fffffff], cl | d3 bc 08 ff ff ff 7f    |
    | sar dword [rax + 1 * rcx - 0x7fffffff], cl | d3 bc 08 01 00 00 80    |
    | sar dword [rax + 1 * rcx - 0x80000000], cl | d3 bc 08 00 00 00 80    |
    | sar dword [r10 + 0x7f], cl                 | 41 d3 7a 7f             |
    | sar dword [r10 + 0x80], cl                 | 41 d3 ba 80 00 00 00    |
    | sar dword [r10 - 0x80], cl                 | 41 d3 7a 80             |
    | sar dword [r10 - 0x81], cl                 | 41 d3 ba 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_sar_addr32_cl():
    encode(SAR_ADDR32_CL)


SAR_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | sar word [rax], 0x01                        | 66 d1 38                      |
    | sar word [rcx], 0x01                        | 66 d1 39                      |
    | sar word [rdx], 0x01                        | 66 d1 3a                      |
    | sar word [rbx], 0x01                        | 66 d1 3b                      |
    | sar word [rsp], 0x01                        | 66 d1 3c 24                   |
    | sar word [rbp], 0x01                        | 66 d1 7d 00                   |
    | sar word [rsi], 0x01                        | 66 d1 3e                      |
    | sar word [rdi], 0x01                        | 66 d1 3f                      |
    | sar word [r8], 0x01                         | 66 41 d1 38                   |
    | sar word [r9], 0x01                         | 66 41 d1 39                   |
    | sar word [r10], 0x01                        | 66 41 d1 3a                   |
    | sar word [r11], 0x01                        | 66 41 d1 3b                   |
    | sar word [r12], 0x01                        | 66 41 d1 3c 24                |
    | sar word [r13], 0x01                        | 66 41 d1 7d 00                |
    | sar word [r14], 0x01                        | 66 41 d1 3e                   |
    | sar word [r15], 0x01                        | 66 41 d1 3f                   |
    | sar word [rax + 1 * rcx], 0x01              | 66 d1 3c 08                   |
    | sar word [rcx + 1 * rcx], 0x01              | 66 d1 3c 09                   |
    | sar word [rdx + 1 * rcx], 0x01              | 66 d1 3c 0a                   |
    | sar word [rbx + 1 * rcx], 0x01              | 66 d1 3c 0b                   |
    | sar word [rsp + 1 * rcx], 0x01              | 66 d1 3c 0c                   |
    | sar word [rbp + 1 * rcx], 0x01              | 66 d1 7c 0d 00                |
    | sar word [rsi + 1 * rcx], 0x01              | 66 d1 3c 0e                   |
    | sar word [rdi + 1 * rcx], 0x01              | 66 d1 3c 0f                   |
    | sar word [r8 + 1 * rcx], 0x01               | 66 41 d1 3c 08                |
    | sar word [r9 + 1 * rcx], 0x01               | 66 41 d1 3c 09                |
    | sar word [r10 + 1 * rcx], 0x01              | 66 41 d1 3c 0a                |
    | sar word [r11 + 1 * rcx], 0x01              | 66 41 d1 3c 0b                |
    | sar word [r12 + 1 * rcx], 0x01              | 66 41 d1 3c 0c                |
    | sar word [r13 + 1 * rcx], 0x01              | 66 41 d1 7c 0d 00             |
    | sar word [r14 + 1 * rcx], 0x01              | 66 41 d1 3c 0e                |
    | sar word [r15 + 1 * rcx], 0x01              | 66 41 d1 3c 0f                |
    | sar word [rax + 1 * rax], 0x01              | 66 d1 3c 00                   |
    | sar word [rax + 1 * rdx], 0x01              | 66 d1 3c 10                   |
    | sar word [rax + 1 * rbx], 0x01              | 66 d1 3c 18                   |
    | sar word [rax + 1 * rbp], 0x01              | 66 d1 3c 28                   |
    | sar word [rax + 1 * rsi], 0x01              | 66 d1 3c 30                   |
    | sar word [rax + 1 * rdi], 0x01              | 66 d1 3c 38                   |
    | sar word [rax + 1 * r8], 0x01               | 66 42 d1 3c 00                |
    | sar word [rax + 1 * r9], 0x01               | 66 42 d1 3c 08                |
    | sar word [rax + 1 * r10], 0x01              | 66 42 d1 3c 10                |
    | sar word [rax + 1 * r11], 0x01              | 66 42 d1 3c 18                |
    | sar word [rax + 1 * r12], 0x01              | 66 42 d1 3c 20                |
    | sar word [rax + 1 * r13], 0x01              | 66 42 d1 3c 28                |
    | sar word [rax + 1 * r14], 0x01              | 66 42 d1 3c 30                |
    | sar word [rax + 1 * r15], 0x01              | 66 42 d1 3c 38                |
    | sar word [rax + 2 * rcx], 0x01              | 66 d1 3c 48                   |
    | sar word [rax + 4 * rcx], 0x01              | 66 d1 3c 88                   |
    | sar word [rax + 8 * rcx], 0x01              | 66 d1 3c c8                   |
    | sar word [r8 + 1 * r9], 0x01                | 66 43 d1 3c 08                |
    | sar word [r8 + 2 * r9], 0x01                | 66 43 d1 3c 48                |
    | sar word [r8 + 4 * r9], 0x01                | 66 43 d1 3c 88                |
    | sar word [r8 + 8 * r9], 0x01                | 66 43 d1 3c c8                |
    | sar word [1 * rcx], 0x01                    | 66 d1 3c 0d 00 00 00 00       |
    | sar word [2 * rcx], 0x01                    | 66 d1 3c 4d 00 00 00 00       |
    | sar word [4 * rcx], 0x01                    | 66 d1 3c 8d 00 00 00 00       |
    | sar word [8 * rcx], 0x01                    | 66 d1 3c cd 00 00 00 00       |
    | sar word [1 * r9], 0x01                     | 66 42 d1 3c 0d 00 00 00 00    |
    | sar word [2 * r9], 0x01                     | 66 42 d1 3c 4d 00 00 00 00    |
    | sar word [4 * r9], 0x01                     | 66 42 d1 3c 8d 00 00 00 00    |
    | sar word [8 * r9], 0x01                     | 66 42 d1 3c cd 00 00 00 00    |
    | sar word [r13 + 8 * r12], 0x01              | 66 43 d1 7c e5 00             |
    | sar word [rsp + 4 * r15], 0x01              | 66 42 d1 3c bc                |
    | sar word [rax + 1 * rcx + 0x00], 0x01       | 66 d1 7c 08 00                |
    | sar word [rax + 1 * rcx - 0x00], 0x01       | 66 d1 7c 08 00                |
    | sar word [rax + 1 * rcx + 0x01], 0x01       | 66 d1 7c 08 01                |
    | sar word [rax + 1 * rcx - 0x01], 0x01       | 66 d1 7c 08 ff                |
    | sar word [rax + 1 * rcx + 0x00000001], 0x01 | 66 d1 bc 08 01 00 00 00       |
    | sar word [rax + 1 * rcx - 0x00000001], 0x01 | 66 d1 bc 08 ff ff ff ff       |
    | sar word [rax + 1 * rcx + 0x7f], 0x01       | 66 d1 7c 08 7f                |
    | sar word [rax + 1 * rcx - 0x7f], 0x01       | 66 d1 7c 08 81                |
    | sar word [rax + 1 * rcx + 0x80], 0x01       | 66 d1 bc 08 80 00 00 00       |
    | sar word [rax + 1 * rcx - 0x80], 0x01       | 66 d1 7c 08 80                |
    | sar word [rax + 1 * rcx - 0x81], 0x01       | 66 d1 bc 08 7f ff ff ff       |
    | sar word [rax + 1 * rcx + 0xff], 0x01       | 66 d1 bc 08 ff 00 00 00       |
    | sar word [rax + 1 * rcx - 0xff], 0x01       | 66 d1 bc 08 01 ff ff ff       |
    | sar word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 d1 bc 08 ff ff ff 7f       |
    | sar word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 d1 bc 08 01 00 00 80       |
    | sar word [rax + 1 * rcx - 0x80000000], 0x01 | 66 d1 bc 08 00 00 00 80       |
    | sar word [r10 + 0x7f], 0x01                 | 66 41 d1 7a 7f                |
    | sar word [r10 + 0x80], 0x01                 | 66 41 d1 ba 80 00 00 00       |
    | sar word [r10 - 0x80], 0x01                 | 66 41 d1 7a 80                |
    | sar word [r10 - 0x81], 0x01                 | 66 41 d1 ba 7f ff ff ff       |
    | sar word [rax], 0x00                        | 66 c1 38 00                   |
    | sar word [rax], 0x7f                        | 66 c1 38 7f                   |
    | sar word [rax], 0x80                        | 66 c1 38 80                   |
    | sar word [rax], 0xff                        | 66 c1 38 ff                   |
    | sar word [rcx], 0x7f                        | 66 c1 39 7f                   |
    | sar word [rdx], 0x80                        | 66 c1 3a 80                   |
    | sar word [rbx], 0xff                        | 66 c1 3b ff                   |
    | sar word [rsp], 0x00                        | 66 c1 3c 24 00                |
    | sar word [rsi], 0x7f                        | 66 c1 3e 7f                   |
    | sar word [rdi], 0x80                        | 66 c1 3f 80                   |
    | sar word [r8], 0xff                         | 66 41 c1 38 ff                |
    | sar word [r9], 0x00                         | 66 41 c1 39 00                |
    | sar word [r11], 0x7f                        | 66 41 c1 3b 7f                |
    | sar word [r12], 0x80                        | 66 41 c1 3c 24 80             |
    | sar word [r13], 0xff                        | 66 41 c1 7d 00 ff             |
    | sar word [r14], 0x00                        | 66 41 c1 3e 00                |
    | sar word [rax + 1 * rcx], 0x7f              | 66 c1 3c 08 7f                |
    | sar word [rcx + 1 * rcx], 0x80              | 66 c1 3c 09 80                |
    | sar word [rdx + 1 * rcx], 0xff              | 66 c1 3c 0a ff                |
    | sar word [rbx + 1 * rcx], 0x00              | 66 c1 3c 0b 00                |
    | sar word [rbp + 1 * rcx], 0x7f              | 66 c1 7c 0d 00 7f             |
    | sar word [rsi + 1 * rcx], 0x80              | 66 c1 3c 0e 80                |
    | sar word [rdi + 1 * rcx], 0xff              | 66 c1 3c 0f ff                |
    | sar word [r8 + 1 * rcx], 0x00               | 66 41 c1 3c 08 00             |
    | sar word [r10 + 1 * rcx], 0x7f              | 66 41 c1 3c 0a 7f             |
    | sar word [r11 + 1 * rcx], 0x80              | 66 41 c1 3c 0b 80             |
    | sar word [r12 + 1 * rcx], 0xff              | 66 41 c1 3c 0c ff             |
    | sar word [r13 + 1 * rcx], 0x00              | 66 41 c1 7c 0d 00 00          |
    | sar word [r15 + 1 * rcx], 0x7f              | 66 41 c1 3c 0f 7f             |
    | sar word [rax + 1 * rax], 0x80              | 66 c1 3c 00 80                |
    | sar word [rax + 1 * rdx], 0xff              | 66 c1 3c 10 ff                |
    | sar word [rax + 1 * rbx], 0x00              | 66 c1 3c 18 00                |
    | sar word [rax + 1 * rsi], 0x7f              | 66 c1 3c 30 7f                |
    | sar word [rax + 1 * rdi], 0x80              | 66 c1 3c 38 80                |
    | sar word [rax + 1 * r8], 0xff               | 66 42 c1 3c 00 ff             |
    | sar word [rax + 1 * r9], 0x00               | 66 42 c1 3c 08 00             |
    | sar word [rax + 1 * r11], 0x7f              | 66 42 c1 3c 18 7f             |
    | sar word [rax + 1 * r12], 0x80              | 66 42 c1 3c 20 80             |
    | sar word [rax + 1 * r13], 0xff              | 66 42 c1 3c 28 ff             |
    | sar word [rax + 1 * r14], 0x00              | 66 42 c1 3c 30 00             |
    | sar word [rax + 2 * rcx], 0x7f              | 66 c1 3c 48 7f                |
    | sar word [rax + 4 * rcx], 0x80              | 66 c1 3c 88 80                |
    | sar word [rax + 8 * rcx], 0xff              | 66 c1 3c c8 ff                |
    | sar word [r8 + 1 * r9], 0x00                | 66 43 c1 3c 08 00             |
    | sar word [r8 + 4 * r9], 0x7f                | 66 43 c1 3c 88 7f             |
    | sar word [r8 + 8 * r9], 0x80                | 66 43 c1 3c c8 80             |
    | sar word [1 * rcx], 0xff                    | 66 c1 3c 0d 00 00 00 00 ff    |
    | sar word [2 * rcx], 0x00                    | 66 c1 3c 4d 00 00 00 00 00    |
    | sar word [8 * rcx], 0x7f                    | 66 c1 3c cd 00 00 00 00 7f    |
    | sar word [1 * r9], 0x80                     | 66 42 c1 3c 0d 00 00 00 00 80 |
    | sar word [2 * r9], 0xff                     | 66 42 c1 3c 4d 00 00 00 00 ff |
    | sar word [4 * r9], 0x00                     | 66 42 c1 3c 8d 00 00 00 00 00 |
    | sar word [r13 + 8 * r12], 0x7f              | 66 43 c1 7c e5 00 7f          |
    | sar word [rsp + 4 * r15], 0x80              | 66 42 c1 3c bc 80             |
    | sar word [rax + 1 * rcx + 0x00], 0xff       | 66 c1 7c 08 00 ff             |
    | sar word [rax + 1 * rcx - 0x00], 0x00       | 66 c1 7c 08 00 00             |
    | sar word [rax + 1 * rcx - 0x01], 0x7f       | 66 c1 7c 08 ff 7f             |
    | sar word [rax + 1 * rcx + 0x00000001], 0x80 | 66 c1 bc 08 01 00 00 00 80    |
    | sar word [rax + 1 * rcx - 0x00000001], 0xff | 66 c1 bc 08 ff ff ff ff ff    |
    | sar word [rax + 1 * rcx + 0x7f], 0x00       | 66 c1 7c 08 7f 00             |
    | sar word [rax + 1 * rcx + 0x80], 0x7f       | 66 c1 bc 08 80 00 00 00 7f    |
    | sar word [rax + 1 * rcx - 0x80], 0x80       | 66 c1 7c 08 80 80             |
    | sar word [rax + 1 * rcx - 0x81], 0xff       | 66 c1 bc 08 7f ff ff ff ff    |
    | sar word [rax + 1 * rcx + 0xff], 0x00       | 66 c1 bc 08 ff 00 00 00 00    |
    | sar word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 c1 bc 08 ff ff ff 7f 7f    |
    | sar word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 c1 bc 08 01 00 00 80 80    |
    | sar word [rax + 1 * rcx - 0x80000000], 0xff | 66 c1 bc 08 00 00 00 80 ff    |
    | sar word [r10 + 0x7f], 0x00                 | 66 41 c1 7a 7f 00             |
    | sar word [r10 - 0x80], 0x7f                 | 66 41 c1 7a 80 7f             |
    | sar word [r10 - 0x81], 0x80                 | 66 41 c1 ba 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_sar_addr16_imm8():
    encode(SAR_ADDR16_IMM8)


SAR_ADDR16_CL = """
    | ----------------------------------------- | -------------------------- |
    | instruction                               | encoding                   |
    | ----------------------------------------- | -------------------------- |
    | sar word [rax], cl                        | 66 d3 38                   |
    | sar word [rcx], cl                        | 66 d3 39                   |
    | sar word [rdx], cl                        | 66 d3 3a                   |
    | sar word [rbx], cl                        | 66 d3 3b                   |
    | sar word [rsp], cl                        | 66 d3 3c 24                |
    | sar word [rbp], cl                        | 66 d3 7d 00                |
    | sar word [rsi], cl                        | 66 d3 3e                   |
    | sar word [rdi], cl                        | 66 d3 3f                   |
    | sar word [r8], cl                         | 66 41 d3 38                |
    | sar word [r9], cl                         | 66 41 d3 39                |
    | sar word [r10], cl                        | 66 41 d3 3a                |
    | sar word [r11], cl                        | 66 41 d3 3b                |
    | sar word [r12], cl                        | 66 41 d3 3c 24             |
    | sar word [r13], cl                        | 66 41 d3 7d 00             |
    | sar word [r14], cl                        | 66 41 d3 3e                |
    | sar word [r15], cl                        | 66 41 d3 3f                |
    | sar word [rax + 1 * rcx], cl              | 66 d3 3c 08                |
    | sar word [rcx + 1 * rcx], cl              | 66 d3 3c 09                |
    | sar word [rdx + 1 * rcx], cl              | 66 d3 3c 0a                |
    | sar word [rbx + 1 * rcx], cl              | 66 d3 3c 0b                |
    | sar word [rsp + 1 * rcx], cl              | 66 d3 3c 0c                |
    | sar word [rbp + 1 * rcx], cl              | 66 d3 7c 0d 00             |
    | sar word [rsi + 1 * rcx], cl              | 66 d3 3c 0e                |
    | sar word [rdi + 1 * rcx], cl              | 66 d3 3c 0f                |
    | sar word [r8 + 1 * rcx], cl               | 66 41 d3 3c 08             |
    | sar word [r9 + 1 * rcx], cl               | 66 41 d3 3c 09             |
    | sar word [r10 + 1 * rcx], cl              | 66 41 d3 3c 0a             |
    | sar word [r11 + 1 * rcx], cl              | 66 41 d3 3c 0b             |
    | sar word [r12 + 1 * rcx], cl              | 66 41 d3 3c 0c             |
    | sar word [r13 + 1 * rcx], cl              | 66 41 d3 7c 0d 00          |
    | sar word [r14 + 1 * rcx], cl              | 66 41 d3 3c 0e             |
    | sar word [r15 + 1 * rcx], cl              | 66 41 d3 3c 0f             |
    | sar word [rax + 1 * rax], cl              | 66 d3 3c 00                |
    | sar word [rax + 1 * rdx], cl              | 66 d3 3c 10                |
    | sar word [rax + 1 * rbx], cl              | 66 d3 3c 18                |
    | sar word [rax + 1 * rbp], cl              | 66 d3 3c 28                |
    | sar word [rax + 1 * rsi], cl              | 66 d3 3c 30                |
    | sar word [rax + 1 * rdi], cl              | 66 d3 3c 38                |
    | sar word [rax + 1 * r8], cl               | 66 42 d3 3c 00             |
    | sar word [rax + 1 * r9], cl               | 66 42 d3 3c 08             |
    | sar word [rax + 1 * r10], cl              | 66 42 d3 3c 10             |
    | sar word [rax + 1 * r11], cl              | 66 42 d3 3c 18             |
    | sar word [rax + 1 * r12], cl              | 66 42 d3 3c 20             |
    | sar word [rax + 1 * r13], cl              | 66 42 d3 3c 28             |
    | sar word [rax + 1 * r14], cl              | 66 42 d3 3c 30             |
    | sar word [rax + 1 * r15], cl              | 66 42 d3 3c 38             |
    | sar word [rax + 2 * rcx], cl              | 66 d3 3c 48                |
    | sar word [rax + 4 * rcx], cl              | 66 d3 3c 88                |
    | sar word [rax + 8 * rcx], cl              | 66 d3 3c c8                |
    | sar word [r8 + 1 * r9], cl                | 66 43 d3 3c 08             |
    | sar word [r8 + 2 * r9], cl                | 66 43 d3 3c 48             |
    | sar word [r8 + 4 * r9], cl                | 66 43 d3 3c 88             |
    | sar word [r8 + 8 * r9], cl                | 66 43 d3 3c c8             |
    | sar word [1 * rcx], cl                    | 66 d3 3c 0d 00 00 00 00    |
    | sar word [2 * rcx], cl                    | 66 d3 3c 4d 00 00 00 00    |
    | sar word [4 * rcx], cl                    | 66 d3 3c 8d 00 00 00 00    |
    | sar word [8 * rcx], cl                    | 66 d3 3c cd 00 00 00 00    |
    | sar word [1 * r9], cl                     | 66 42 d3 3c 0d 00 00 00 00 |
    | sar word [2 * r9], cl                     | 66 42 d3 3c 4d 00 00 00 00 |
    | sar word [4 * r9], cl                     | 66 42 d3 3c 8d 00 00 00 00 |
    | sar word [8 * r9], cl                     | 66 42 d3 3c cd 00 00 00 00 |
    | sar word [r13 + 8 * r12], cl              | 66 43 d3 7c e5 00          |
    | sar word [rsp + 4 * r15], cl              | 66 42 d3 3c bc             |
    | sar word [rax + 1 * rcx + 0x00], cl       | 66 d3 7c 08 00             |
    | sar word [rax + 1 * rcx - 0x00], cl       | 66 d3 7c 08 00             |
    | sar word [rax + 1 * rcx + 0x01], cl       | 66 d3 7c 08 01             |
    | sar word [rax + 1 * rcx - 0x01], cl       | 66 d3 7c 08 ff             |
    | sar word [rax + 1 * rcx + 0x00000001], cl | 66 d3 bc 08 01 00 00 00    |
    | sar word [rax + 1 * rcx - 0x00000001], cl | 66 d3 bc 08 ff ff ff ff    |
    | sar word [rax + 1 * rcx + 0x7f], cl       | 66 d3 7c 08 7f             |
    | sar word [rax + 1 * rcx - 0x7f], cl       | 66 d3 7c 08 81             |
    | sar word [rax + 1 * rcx + 0x80], cl       | 66 d3 bc 08 80 00 00 00    |
    | sar word [rax + 1 * rcx - 0x80], cl       | 66 d3 7c 08 80             |
    | sar word [rax + 1 * rcx - 0x81], cl       | 66 d3 bc 08 7f ff ff ff    |
    | sar word [rax + 1 * rcx + 0xff], cl       | 66 d3 bc 08 ff 00 00 00    |
    | sar word [rax + 1 * rcx - 0xff], cl       | 66 d3 bc 08 01 ff ff ff    |
    | sar word [rax + 1 * rcx + 0x7fffffff], cl | 66 d3 bc 08 ff ff ff 7f    |
    | sar word [rax + 1 * rcx - 0x7fffffff], cl | 66 d3 bc 08 01 00 00 80    |
    | sar word [rax + 1 * rcx - 0x80000000], cl | 66 d3 bc 08 00 00 00 80    |
    | sar word [r10 + 0x7f], cl                 | 66 41 d3 7a 7f             |
    | sar word [r10 + 0x80], cl                 | 66 41 d3 ba 80 00 00 00    |
    | sar word [r10 - 0x80], cl                 | 66 41 d3 7a 80             |
    | sar word [r10 - 0x81], cl                 | 66 41 d3 ba 7f ff ff ff    |
    | ----------------------------------------- | -------------------------- |
"""


def can_encode_sar_addr16_cl():
    encode(SAR_ADDR16_CL)


SAR_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | sar byte [rax], 0x01                        | d0 38                      |
    | sar byte [rcx], 0x01                        | d0 39                      |
    | sar byte [rdx], 0x01                        | d0 3a                      |
    | sar byte [rbx], 0x01                        | d0 3b                      |
    | sar byte [rsp], 0x01                        | d0 3c 24                   |
    | sar byte [rbp], 0x01                        | d0 7d 00                   |
    | sar byte [rsi], 0x01                        | d0 3e                      |
    | sar byte [rdi], 0x01                        | d0 3f                      |
    | sar byte [r8], 0x01                         | 41 d0 38                   |
    | sar byte [r9], 0x01                         | 41 d0 39                   |
    | sar byte [r10], 0x01                        | 41 d0 3a                   |
    | sar byte [r11], 0x01                        | 41 d0 3b                   |
    | sar byte [r12], 0x01                        | 41 d0 3c 24                |
    | sar byte [r13], 0x01                        | 41 d0 7d 00                |
    | sar byte [r14], 0x01                        | 41 d0 3e                   |
    | sar byte [r15], 0x01                        | 41 d0 3f                   |
    | sar byte [rax + 1 * rcx], 0x01              | d0 3c 08                   |
    | sar byte [rcx + 1 * rcx], 0x01              | d0 3c 09                   |
    | sar byte [rdx + 1 * rcx], 0x01              | d0 3c 0a                   |
    | sar byte [rbx + 1 * rcx], 0x01              | d0 3c 0b                   |
    | sar byte [rsp + 1 * rcx], 0x01              | d0 3c 0c                   |
    | sar byte [rbp + 1 * rcx], 0x01              | d0 7c 0d 00                |
    | sar byte [rsi + 1 * rcx], 0x01              | d0 3c 0e                   |
    | sar byte [rdi + 1 * rcx], 0x01              | d0 3c 0f                   |
    | sar byte [r8 + 1 * rcx], 0x01               | 41 d0 3c 08                |
    | sar byte [r9 + 1 * rcx], 0x01               | 41 d0 3c 09                |
    | sar byte [r10 + 1 * rcx], 0x01              | 41 d0 3c 0a                |
    | sar byte [r11 + 1 * rcx], 0x01              | 41 d0 3c 0b                |
    | sar byte [r12 + 1 * rcx], 0x01              | 41 d0 3c 0c                |
    | sar byte [r13 + 1 * rcx], 0x01              | 41 d0 7c 0d 00             |
    | sar byte [r14 + 1 * rcx], 0x01              | 41 d0 3c 0e                |
    | sar byte [r15 + 1 * rcx], 0x01              | 41 d0 3c 0f                |
    | sar byte [rax + 1 * rax], 0x01              | d0 3c 00                   |
    | sar byte [rax + 1 * rdx], 0x01              | d0 3c 10                   |
    | sar byte [rax + 1 * rbx], 0x01              | d0 3c 18                   |
    | sar byte [rax + 1 * rbp], 0x01              | d0 3c 28                   |
    | sar byte [rax + 1 * rsi], 0x01              | d0 3c 30                   |
    | sar byte [rax + 1 * rdi], 0x01              | d0 3c 38                   |
    | sar byte [rax + 1 * r8], 0x01               | 42 d0 3c 00                |
    | sar byte [rax + 1 * r9], 0x01               | 42 d0 3c 08                |
    | sar byte [rax + 1 * r10], 0x01              | 42 d0 3c 10                |
    | sar byte [rax + 1 * r11], 0x01              | 42 d0 3c 18                |
    | sar byte [rax + 1 * r12], 0x01              | 42 d0 3c 20                |
    | sar byte [rax + 1 * r13], 0x01              | 42 d0 3c 28                |
    | sar byte [rax + 1 * r14], 0x01              | 42 d0 3c 30                |
    | sar byte [rax + 1 * r15], 0x01              | 42 d0 3c 38                |
    | sar byte [rax + 2 * rcx], 0x01              | d0 3c 48                   |
    | sar byte [rax + 4 * rcx], 0x01              | d0 3c 88                   |
    | sar byte [rax + 8 * rcx], 0x01              | d0 3c c8                   |
    | sar byte [r8 + 1 * r9], 0x01                | 43 d0 3c 08                |
    | sar byte [r8 + 2 * r9], 0x01                | 43 d0 3c 48                |
    | sar byte [r8 + 4 * r9], 0x01                | 43 d0 3c 88                |
    | sar byte [r8 + 8 * r9], 0x01                | 43 d0 3c c8                |
    | sar byte [1 * rcx], 0x01                    | d0 3c 0d 00 00 00 00       |
    | sar byte [2 * rcx], 0x01                    | d0 3c 4d 00 00 00 00       |
    | sar byte [4 * rcx], 0x01                    | d0 3c 8d 00 00 00 00       |
    | sar byte [8 * rcx], 0x01                    | d0 3c cd 00 00 00 00       |
    | sar byte [1 * r9], 0x01                     | 42 d0 3c 0d 00 00 00 00    |
    | sar byte [2 * r9], 0x01                     | 42 d0 3c 4d 00 00 00 00    |
    | sar byte [4 * r9], 0x01                     | 42 d0 3c 8d 00 00 00 00    |
    | sar byte [8 * r9], 0x01                     | 42 d0 3c cd 00 00 00 00    |
    | sar byte [r13 + 8 * r12], 0x01              | 43 d0 7c e5 00             |
    | sar byte [rsp + 4 * r15], 0x01              | 42 d0 3c bc                |
    | sar byte [rax + 1 * rcx + 0x00], 0x01       | d0 7c 08 00                |
    | sar byte [rax + 1 * rcx - 0x00], 0x01       | d0 7c 08 00                |
    | sar byte [rax + 1 * rcx + 0x01], 0x01       | d0 7c 08 01                |
    | sar byte [rax + 1 * rcx - 0x01], 0x01       | d0 7c 08 ff                |
    | sar byte [rax + 1 * rcx + 0x00000001], 0x01 | d0 bc 08 01 00 00 00       |
    | sar byte [rax + 1 * rcx - 0x00000001], 0x01 | d0 bc 08 ff ff ff ff       |
    | sar byte [rax + 1 * rcx + 0x7f], 0x01       | d0 7c 08 7f                |
    | sar byte [rax + 1 * rcx - 0x7f], 0x01       | d0 7c 08 81                |
    | sar byte [rax + 1 * rcx + 0x80], 0x01       | d0 bc 08 80 00 00 00       |
    | sar byte [rax + 1 * rcx - 0x80], 0x01       | d0 7c 08 80                |
    | sar byte [rax + 1 * rcx - 0x81], 0x01       | d0 bc 08 7f ff ff ff       |
    | sar byte [rax + 1 * rcx + 0xff], 0x01       | d0 bc 08 ff 00 00 00       |
    | sar byte [rax + 1 * rcx - 0xff], 0x01       | d0 bc 08 01 ff ff ff       |
    | sar byte [rax + 1 * rcx + 0x7fffffff], 0x01 | d0 bc 08 ff ff ff 7f       |
    | sar byte [rax + 1 * rcx - 0x7fffffff], 0x01 | d0 bc 08 01 00 00 80       |
    | sar byte [rax + 1 * rcx - 0x80000000], 0x01 | d0 bc 08 00 00 00 80       |
    | sar byte [r10 + 0x7f], 0x01                 | 41 d0 7a 7f                |
    | sar byte [r10 + 0x80], 0x01                 | 41 d0 ba 80 00 00 00       |
    | sar byte [r10 - 0x80], 0x01                 | 41 d0 7a 80                |
    | sar byte [r10 - 0x81], 0x01                 | 41 d0 ba 7f ff ff ff       |
    | sar byte [rax], 0x00                        | c0 38 00                   |
    | sar byte [rax], 0x7f                        | c0 38 7f                   |
    | sar byte [rax], 0x80                        | c0 38 80                   |
    | sar byte [rax], 0xff                        | c0 38 ff                   |
    | sar byte [rcx], 0x7f                        | c0 39 7f                   |
    | sar byte [rdx], 0x80                        | c0 3a 80                   |
    | sar byte [rbx], 0xff                        | c0 3b ff                   |
    | sar byte [rsp], 0x00                        | c0 3c 24 00                |
    | sar byte [rsi], 0x7f                        | c0 3e 7f                   |
    | sar byte [rdi], 0x80                        | c0 3f 80                   |
    | sar byte [r8], 0xff                         | 41 c0 38 ff                |
    | sar byte [r9], 0x00                         | 41 c0 39 00                |
    | sar byte [r11], 0x7f                        | 41 c0 3b 7f                |
    | sar byte [r12], 0x80                        | 41 c0 3c 24 80             |
    | sar byte [r13], 0xff                        | 41 c0 7d 00 ff             |
    | sar byte [r14], 0x00                        | 41 c0 3e 00                |
    | sar byte [rax + 1 * rcx], 0x7f              | c0 3c 08 7f                |
    | sar byte [rcx + 1 * rcx], 0x80              | c0 3c 09 80                |
    | sar byte [rdx + 1 * rcx], 0xff              | c0 3c 0a ff                |
    | sar byte [rbx + 1 * rcx], 0x00              | c0 3c 0b 00                |
    | sar byte [rbp + 1 * rcx], 0x7f              | c0 7c 0d 00 7f             |
    | sar byte [rsi + 1 * rcx], 0x80              | c0 3c 0e 80                |
    | sar byte [rdi + 1 * rcx], 0xff              | c0 3c 0f ff                |
    | sar byte [r8 + 1 * rcx], 0x00               | 41 c0 3c 08 00             |
    | sar byte [r10 + 1 * rcx], 0x7f              | 41 c0 3c 0a 7f             |
    | sar byte [r11 + 1 * rcx], 0x80              | 41 c0 3c 0b 80             |
    | sar byte [r12 + 1 * rcx], 0xff              | 41 c0 3c 0c ff             |
    | sar byte [r13 + 1 * rcx], 0x00              | 41 c0 7c 0d 00 00          |
    | sar byte [r15 + 1 * rcx], 0x7f              | 41 c0 3c 0f 7f             |
    | sar byte [rax + 1 * rax], 0x80              | c0 3c 00 80                |
    | sar byte [rax + 1 * rdx], 0xff              | c0 3c 10 ff                |
    | sar byte [rax + 1 * rbx], 0x00              | c0 3c 18 00                |
    | sar byte [rax + 1 * rsi], 0x7f              | c0 3c 30 7f                |
    | sar byte [rax + 1 * rdi], 0x80              | c0 3c 38 80                |
    | sar byte [rax + 1 * r8], 0xff               | 42 c0 3c 00 ff             |
    | sar byte [rax + 1 * r9], 0x00               | 42 c0 3c 08 00             |
    | sar byte [rax + 1 * r11], 0x7f              | 42 c0 3c 18 7f             |
    | sar byte [rax + 1 * r12], 0x80              | 42 c0 3c 20 80             |
    | sar byte [rax + 1 * r13], 0xff              | 42 c0 3c 28 ff             |
    | sar byte [rax + 1 * r14], 0x00              | 42 c0 3c 30 00             |
    | sar byte [rax + 2 * rcx], 0x7f              | c0 3c 48 7f                |
    | sar byte [rax + 4 * rcx], 0x80              | c0 3c 88 80                |
    | sar byte [rax + 8 * rcx], 0xff              | c0 3c c8 ff                |
    | sar byte [r8 + 1 * r9], 0x00                | 43 c0 3c 08 00             |
    | sar byte [r8 + 4 * r9], 0x7f                | 43 c0 3c 88 7f             |
    | sar byte [r8 + 8 * r9], 0x80                | 43 c0 3c c8 80             |
    | sar byte [1 * rcx], 0xff                    | c0 3c 0d 00 00 00 00 ff    |
    | sar byte [2 * rcx], 0x00                    | c0 3c 4d 00 00 00 00 00    |
    | sar byte [8 * rcx], 0x7f                    | c0 3c cd 00 00 00 00 7f    |
    | sar byte [1 * r9], 0x80                     | 42 c0 3c 0d 00 00 00 00 80 |
    | sar byte [2 * r9], 0xff                     | 42 c0 3c 4d 00 00 00 00 ff |
    | sar byte [4 * r9], 0x00                     | 42 c0 3c 8d 00 00 00 00 00 |
    | sar byte [r13 + 8 * r12], 0x7f              | 43 c0 7c e5 00 7f          |
    | sar byte [rsp + 4 * r15], 0x80              | 42 c0 3c bc 80             |
    | sar byte [rax + 1 * rcx + 0x00], 0xff       | c0 7c 08 00 ff             |
    | sar byte [rax + 1 * rcx - 0x00], 0x00       | c0 7c 08 00 00             |
    | sar byte [rax + 1 * rcx - 0x01], 0x7f       | c0 7c 08 ff 7f             |
    | sar byte [rax + 1 * rcx + 0x00000001], 0x80 | c0 bc 08 01 00 00 00 80    |
    | sar byte [rax + 1 * rcx - 0x00000001], 0xff | c0 bc 08 ff ff ff ff ff    |
    | sar byte [rax + 1 * rcx + 0x7f], 0x00       | c0 7c 08 7f 00             |
    | sar byte [rax + 1 * rcx + 0x80], 0x7f       | c0 bc 08 80 00 00 00 7f    |
    | sar byte [rax + 1 * rcx - 0x80], 0x80       | c0 7c 08 80 80             |
    | sar byte [rax + 1 * rcx - 0x81], 0xff       | c0 bc 08 7f ff ff ff ff    |
    | sar byte [rax + 1 * rcx + 0xff], 0x00       | c0 bc 08 ff 00 00 00 00    |
    | sar byte [rax + 1 * rcx + 0x7fffffff], 0x7f | c0 bc 08 ff ff ff 7f 7f    |
    | sar byte [rax + 1 * rcx - 0x7fffffff], 0x80 | c0 bc 08 01 00 00 80 80    |
    | sar byte [rax + 1 * rcx - 0x80000000], 0xff | c0 bc 08 00 00 00 80 ff    |
    | sar byte [r10 + 0x7f], 0x00                 | 41 c0 7a 7f 00             |
    | sar byte [r10 - 0x80], 0x7f                 | 41 c0 7a 80 7f             |
    | sar byte [r10 - 0x81], 0x80                 | 41 c0 ba 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_sar_addr8_imm8():
    encode(SAR_ADDR8_IMM8)


SAR_ADDR8_CL = """
    | ----------------------------------------- | ----------------------- |
    | instruction                               | encoding                |
    | ----------------------------------------- | ----------------------- |
    | sar byte [rax], cl                        | d2 38                   |
    | sar byte [rcx], cl                        | d2 39                   |
    | sar byte [rdx], cl                        | d2 3a                   |
    | sar byte [rbx], cl                        | d2 3b                   |
    | sar byte [rsp], cl                        | d2 3c 24                |
    | sar byte [rbp], cl                        | d2 7d 00                |
    | sar byte [rsi], cl                        | d2 3e                   |
    | sar byte [rdi], cl                        | d2 3f                   |
    | sar byte [r8], cl                         | 41 d2 38                |
    | sar byte [r9], cl                         | 41 d2 39                |
    | sar byte [r10], cl                        | 41 d2 3a                |
    | sar byte [r11], cl                        | 41 d2 3b                |
    | sar byte [r12], cl                        | 41 d2 3c 24             |
    | sar byte [r13], cl                        | 41 d2 7d 00             |
    | sar byte [r14], cl                        | 41 d2 3e                |
    | sar byte [r15], cl                        | 41 d2 3f                |
    | sar byte [rax + 1 * rcx], cl              | d2 3c 08                |
    | sar byte [rcx + 1 * rcx], cl              | d2 3c 09                |
    | sar byte [rdx + 1 * rcx], cl              | d2 3c 0a                |
    | sar byte [rbx + 1 * rcx], cl              | d2 3c 0b                |
    | sar byte [rsp + 1 * rcx], cl              | d2 3c 0c                |
    | sar byte [rbp + 1 * rcx], cl              | d2 7c 0d 00             |
    | sar byte [rsi + 1 * rcx], cl              | d2 3c 0e                |
    | sar byte [rdi + 1 * rcx], cl              | d2 3c 0f                |
    | sar byte [r8 + 1 * rcx], cl               | 41 d2 3c 08             |
    | sar byte [r9 + 1 * rcx], cl               | 41 d2 3c 09             |
    | sar byte [r10 + 1 * rcx], cl              | 41 d2 3c 0a             |
    | sar byte [r11 + 1 * rcx], cl              | 41 d2 3c 0b             |
    | sar byte [r12 + 1 * rcx], cl              | 41 d2 3c 0c             |
    | sar byte [r13 + 1 * rcx], cl              | 41 d2 7c 0d 00          |
    | sar byte [r14 + 1 * rcx], cl              | 41 d2 3c 0e             |
    | sar byte [r15 + 1 * rcx], cl              | 41 d2 3c 0f             |
    | sar byte [rax + 1 * rax], cl              | d2 3c 00                |
    | sar byte [rax + 1 * rdx], cl              | d2 3c 10                |
    | sar byte [rax + 1 * rbx], cl              | d2 3c 18                |
    | sar byte [rax + 1 * rbp], cl              | d2 3c 28                |
    | sar byte [rax + 1 * rsi], cl              | d2 3c 30                |
    | sar byte [rax + 1 * rdi], cl              | d2 3c 38                |
    | sar byte [rax + 1 * r8], cl               | 42 d2 3c 00             |
    | sar byte [rax + 1 * r9], cl               | 42 d2 3c 08             |
    | sar byte [rax + 1 * r10], cl              | 42 d2 3c 10             |
    | sar byte [rax + 1 * r11], cl              | 42 d2 3c 18             |
    | sar byte [rax + 1 * r12], cl              | 42 d2 3c 20             |
    | sar byte [rax + 1 * r13], cl              | 42 d2 3c 28             |
    | sar byte [rax + 1 * r14], cl              | 42 d2 3c 30             |
    | sar byte [rax + 1 * r15], cl              | 42 d2 3c 38             |
    | sar byte [rax + 2 * rcx], cl              | d2 3c 48                |
    | sar byte [rax + 4 * rcx], cl              | d2 3c 88                |
    | sar byte [rax + 8 * rcx], cl              | d2 3c c8                |
    | sar byte [r8 + 1 * r9], cl                | 43 d2 3c 08             |
    | sar byte [r8 + 2 * r9], cl                | 43 d2 3c 48             |
    | sar byte [r8 + 4 * r9], cl                | 43 d2 3c 88             |
    | sar byte [r8 + 8 * r9], cl                | 43 d2 3c c8             |
    | sar byte [1 * rcx], cl                    | d2 3c 0d 00 00 00 00    |
    | sar byte [2 * rcx], cl                    | d2 3c 4d 00 00 00 00    |
    | sar byte [4 * rcx], cl                    | d2 3c 8d 00 00 00 00    |
    | sar byte [8 * rcx], cl                    | d2 3c cd 00 00 00 00    |
    | sar byte [1 * r9], cl                     | 42 d2 3c 0d 00 00 00 00 |
    | sar byte [2 * r9], cl                     | 42 d2 3c 4d 00 00 00 00 |
    | sar byte [4 * r9], cl                     | 42 d2 3c 8d 00 00 00 00 |
    | sar byte [8 * r9], cl                     | 42 d2 3c cd 00 00 00 00 |
    | sar byte [r13 + 8 * r12], cl              | 43 d2 7c e5 00          |
    | sar byte [rsp + 4 * r15], cl              | 42 d2 3c bc             |
    | sar byte [rax + 1 * rcx + 0x00], cl       | d2 7c 08 00             |
    | sar byte [rax + 1 * rcx - 0x00], cl       | d2 7c 08 00             |
    | sar byte [rax + 1 * rcx + 0x01], cl       | d2 7c 08 01             |
    | sar byte [rax + 1 * rcx - 0x01], cl       | d2 7c 08 ff             |
    | sar byte [rax + 1 * rcx + 0x00000001], cl | d2 bc 08 01 00 00 00    |
    | sar byte [rax + 1 * rcx - 0x00000001], cl | d2 bc 08 ff ff ff ff    |
    | sar byte [rax + 1 * rcx + 0x7f], cl       | d2 7c 08 7f             |
    | sar byte [rax + 1 * rcx - 0x7f], cl       | d2 7c 08 81             |
    | sar byte [rax + 1 * rcx + 0x80], cl       | d2 bc 08 80 00 00 00    |
    | sar byte [rax + 1 * rcx - 0x80], cl       | d2 7c 08 80             |
    | sar byte [rax + 1 * rcx - 0x81], cl       | d2 bc 08 7f ff ff ff    |
    | sar byte [rax + 1 * rcx + 0xff], cl       | d2 bc 08 ff 00 00 00    |
    | sar byte [rax + 1 * rcx - 0xff], cl       | d2 bc 08 01 ff ff ff    |
    | sar byte [rax + 1 * rcx + 0x7fffffff], cl | d2 bc 08 ff ff ff 7f    |
    | sar byte [rax + 1 * rcx - 0x7fffffff], cl | d2 bc 08 01 00 00 80    |
    | sar byte [rax + 1 * rcx - 0x80000000], cl | d2 bc 08 00 00 00 80    |
    | sar byte [r10 + 0x7f], cl                 | 41 d2 7a 7f             |
    | sar byte [r10 + 0x80], cl                 | 41 d2 ba 80 00 00 00    |
    | sar byte [r10 - 0x80], cl                 | 41 d2 7a 80             |
    | sar byte [r10 - 0x81], cl                 | 41 d2 ba 7f ff ff ff    |
    | ----------------------------------------- | ----------------------- |
"""


def can_encode_sar_addr8_cl():
    encode(SAR_ADDR8_CL)
