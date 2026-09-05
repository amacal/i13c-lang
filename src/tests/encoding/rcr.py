from tests.encoding.core import encode, exhaust


def can_exhaust_rcr():
    exhaust(
        RCR_ADDR16_CL,
        RCR_ADDR16_IMM8,
        RCR_ADDR32_CL,
        RCR_ADDR32_IMM8,
        RCR_ADDR64_CL,
        RCR_ADDR64_IMM8,
        RCR_ADDR8_CL,
        RCR_ADDR8_IMM8,
        RCR_REG16_CL,
        RCR_REG16_IMM8,
        RCR_REG32_CL,
        RCR_REG32_IMM8,
        RCR_REG64_CL,
        RCR_REG64_IMM8,
        RCR_REG8_CL,
        RCR_REG8_IMM8,
    )


RCR_REG64_IMM8 = """
    | ------------- | ----------- | --- | ------------- | ----------- |
    | instruction   | encoding    | *** | instruction   | encoding    |
    | ------------- | ----------- | --- | ------------- | ----------- |
    | rcr rax, 0x01 | 48 d1 d8    | *** | rcr rax, 0x00 | 48 c1 d8 00 |
    | rcr rcx, 0x01 | 48 d1 d9    | *** | rcr rax, 0x7f | 48 c1 d8 7f |
    | rcr rdx, 0x01 | 48 d1 da    | *** | rcr rax, 0x80 | 48 c1 d8 80 |
    | rcr rbx, 0x01 | 48 d1 db    | *** | rcr rax, 0xff | 48 c1 d8 ff |
    | rcr rsp, 0x01 | 48 d1 dc    | *** | rcr rcx, 0x7f | 48 c1 d9 7f |
    | rcr rbp, 0x01 | 48 d1 dd    | *** | rcr rdx, 0x80 | 48 c1 da 80 |
    | rcr rsi, 0x01 | 48 d1 de    | *** | rcr rbx, 0xff | 48 c1 db ff |
    | rcr rdi, 0x01 | 48 d1 df    | *** | rcr rsp, 0x00 | 48 c1 dc 00 |
    | rcr r8, 0x01  | 49 d1 d8    | *** | rcr rsi, 0x7f | 48 c1 de 7f |
    | rcr r9, 0x01  | 49 d1 d9    | *** | rcr rdi, 0x80 | 48 c1 df 80 |
    | rcr r10, 0x01 | 49 d1 da    | *** | rcr r8, 0xff  | 49 c1 d8 ff |
    | rcr r11, 0x01 | 49 d1 db    | *** | rcr r9, 0x00  | 49 c1 d9 00 |
    | rcr r12, 0x01 | 49 d1 dc    | *** | rcr r11, 0x7f | 49 c1 db 7f |
    | rcr r13, 0x01 | 49 d1 dd    | *** | rcr r12, 0x80 | 49 c1 dc 80 |
    | rcr r14, 0x01 | 49 d1 de    | *** | rcr r13, 0xff | 49 c1 dd ff |
    | rcr r15, 0x01 | 49 d1 df    | *** | rcr r14, 0x00 | 49 c1 de 00 |
    | ------------- | ----------- | --- | ------------- | ----------- |
"""


def can_encode_rcr_reg64_imm8():
    encode(RCR_REG64_IMM8)


RCR_REG64_CL = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | rcr rax, cl | 48 d3 d8 | *** | rcr r8, cl  | 49 d3 d8 |
    | rcr rcx, cl | 48 d3 d9 | *** | rcr r9, cl  | 49 d3 d9 |
    | rcr rdx, cl | 48 d3 da | *** | rcr r10, cl | 49 d3 da |
    | rcr rbx, cl | 48 d3 db | *** | rcr r11, cl | 49 d3 db |
    | rcr rsp, cl | 48 d3 dc | *** | rcr r12, cl | 49 d3 dc |
    | rcr rbp, cl | 48 d3 dd | *** | rcr r13, cl | 49 d3 dd |
    | rcr rsi, cl | 48 d3 de | *** | rcr r14, cl | 49 d3 de |
    | rcr rdi, cl | 48 d3 df | *** | rcr r15, cl | 49 d3 df |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_rcr_reg64_cl():
    encode(RCR_REG64_CL)


RCR_REG32_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | rcr eax, 0x01  | d1 d8       | *** | rcr eax, 0x00  | c1 d8 00    |
    | rcr ecx, 0x01  | d1 d9       | *** | rcr eax, 0x7f  | c1 d8 7f    |
    | rcr edx, 0x01  | d1 da       | *** | rcr eax, 0x80  | c1 d8 80    |
    | rcr ebx, 0x01  | d1 db       | *** | rcr eax, 0xff  | c1 d8 ff    |
    | rcr esp, 0x01  | d1 dc       | *** | rcr ecx, 0x7f  | c1 d9 7f    |
    | rcr ebp, 0x01  | d1 dd       | *** | rcr edx, 0x80  | c1 da 80    |
    | rcr esi, 0x01  | d1 de       | *** | rcr ebx, 0xff  | c1 db ff    |
    | rcr edi, 0x01  | d1 df       | *** | rcr esp, 0x00  | c1 dc 00    |
    | rcr r8d, 0x01  | 41 d1 d8    | *** | rcr esi, 0x7f  | c1 de 7f    |
    | rcr r9d, 0x01  | 41 d1 d9    | *** | rcr edi, 0x80  | c1 df 80    |
    | rcr r10d, 0x01 | 41 d1 da    | *** | rcr r8d, 0xff  | 41 c1 d8 ff |
    | rcr r11d, 0x01 | 41 d1 db    | *** | rcr r9d, 0x00  | 41 c1 d9 00 |
    | rcr r12d, 0x01 | 41 d1 dc    | *** | rcr r11d, 0x7f | 41 c1 db 7f |
    | rcr r13d, 0x01 | 41 d1 dd    | *** | rcr r12d, 0x80 | 41 c1 dc 80 |
    | rcr r14d, 0x01 | 41 d1 de    | *** | rcr r13d, 0xff | 41 c1 dd ff |
    | rcr r15d, 0x01 | 41 d1 df    | *** | rcr r14d, 0x00 | 41 c1 de 00 |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_rcr_reg32_imm8():
    encode(RCR_REG32_IMM8)


RCR_REG32_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | rcr eax, cl  | d3 d8    | *** | rcr r8d, cl  | 41 d3 d8 |
    | rcr ecx, cl  | d3 d9    | *** | rcr r9d, cl  | 41 d3 d9 |
    | rcr edx, cl  | d3 da    | *** | rcr r10d, cl | 41 d3 da |
    | rcr ebx, cl  | d3 db    | *** | rcr r11d, cl | 41 d3 db |
    | rcr esp, cl  | d3 dc    | *** | rcr r12d, cl | 41 d3 dc |
    | rcr ebp, cl  | d3 dd    | *** | rcr r13d, cl | 41 d3 dd |
    | rcr esi, cl  | d3 de    | *** | rcr r14d, cl | 41 d3 de |
    | rcr edi, cl  | d3 df    | *** | rcr r15d, cl | 41 d3 df |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_rcr_reg32_cl():
    encode(RCR_REG32_CL)


RCR_REG16_IMM8 = """
    | -------------- | -------------- | --- | -------------- | -------------- |
    | instruction    | encoding       | *** | instruction    | encoding       |
    | -------------- | -------------- | --- | -------------- | -------------- |
    | rcr ax, 0x01   | 66 d1 d8       | *** | rcr ax, 0x00   | 66 c1 d8 00    |
    | rcr cx, 0x01   | 66 d1 d9       | *** | rcr ax, 0x7f   | 66 c1 d8 7f    |
    | rcr dx, 0x01   | 66 d1 da       | *** | rcr ax, 0x80   | 66 c1 d8 80    |
    | rcr bx, 0x01   | 66 d1 db       | *** | rcr ax, 0xff   | 66 c1 d8 ff    |
    | rcr sp, 0x01   | 66 d1 dc       | *** | rcr cx, 0x7f   | 66 c1 d9 7f    |
    | rcr bp, 0x01   | 66 d1 dd       | *** | rcr dx, 0x80   | 66 c1 da 80    |
    | rcr si, 0x01   | 66 d1 de       | *** | rcr bx, 0xff   | 66 c1 db ff    |
    | rcr di, 0x01   | 66 d1 df       | *** | rcr sp, 0x00   | 66 c1 dc 00    |
    | rcr r8w, 0x01  | 66 41 d1 d8    | *** | rcr si, 0x7f   | 66 c1 de 7f    |
    | rcr r9w, 0x01  | 66 41 d1 d9    | *** | rcr di, 0x80   | 66 c1 df 80    |
    | rcr r10w, 0x01 | 66 41 d1 da    | *** | rcr r8w, 0xff  | 66 41 c1 d8 ff |
    | rcr r11w, 0x01 | 66 41 d1 db    | *** | rcr r9w, 0x00  | 66 41 c1 d9 00 |
    | rcr r12w, 0x01 | 66 41 d1 dc    | *** | rcr r11w, 0x7f | 66 41 c1 db 7f |
    | rcr r13w, 0x01 | 66 41 d1 dd    | *** | rcr r12w, 0x80 | 66 41 c1 dc 80 |
    | rcr r14w, 0x01 | 66 41 d1 de    | *** | rcr r13w, 0xff | 66 41 c1 dd ff |
    | rcr r15w, 0x01 | 66 41 d1 df    | *** | rcr r14w, 0x00 | 66 41 c1 de 00 |
    | -------------- | -------------- | --- | -------------- | -------------- |
"""


def can_encode_rcr_reg16_imm8():
    encode(RCR_REG16_IMM8)


RCR_REG16_CL = """
    | ------------ | ----------- | --- | ------------ | ----------- |
    | instruction  | encoding    | *** | instruction  | encoding    |
    | ------------ | ----------- | --- | ------------ | ----------- |
    | rcr ax, cl   | 66 d3 d8    | *** | rcr r8w, cl  | 66 41 d3 d8 |
    | rcr cx, cl   | 66 d3 d9    | *** | rcr r9w, cl  | 66 41 d3 d9 |
    | rcr dx, cl   | 66 d3 da    | *** | rcr r10w, cl | 66 41 d3 da |
    | rcr bx, cl   | 66 d3 db    | *** | rcr r11w, cl | 66 41 d3 db |
    | rcr sp, cl   | 66 d3 dc    | *** | rcr r12w, cl | 66 41 d3 dc |
    | rcr bp, cl   | 66 d3 dd    | *** | rcr r13w, cl | 66 41 d3 dd |
    | rcr si, cl   | 66 d3 de    | *** | rcr r14w, cl | 66 41 d3 de |
    | rcr di, cl   | 66 d3 df    | *** | rcr r15w, cl | 66 41 d3 df |
    | ------------ | ----------- | --- | ------------ | ----------- |
"""


def can_encode_rcr_reg16_cl():
    encode(RCR_REG16_CL)


RCR_REG8_IMM8 = """
    | -------------- | ----------- | --- | -------------- | ----------- |
    | instruction    | encoding    | *** | instruction    | encoding    |
    | -------------- | ----------- | --- | -------------- | ----------- |
    | rcr al, 0x01   | d0 d8       | *** | rcr al, 0x00   | c0 d8 00    |
    | rcr cl, 0x01   | d0 d9       | *** | rcr al, 0x7f   | c0 d8 7f    |
    | rcr dl, 0x01   | d0 da       | *** | rcr al, 0x80   | c0 d8 80    |
    | rcr bl, 0x01   | d0 db       | *** | rcr al, 0xff   | c0 d8 ff    |
    | rcr spl, 0x01  | 40 d0 dc    | *** | rcr cl, 0x7f   | c0 d9 7f    |
    | rcr bpl, 0x01  | 40 d0 dd    | *** | rcr dl, 0x80   | c0 da 80    |
    | rcr sil, 0x01  | 40 d0 de    | *** | rcr bl, 0xff   | c0 db ff    |
    | rcr dil, 0x01  | 40 d0 df    | *** | rcr spl, 0x00  | 40 c0 dc 00 |
    | rcr r8b, 0x01  | 41 d0 d8    | *** | rcr sil, 0x7f  | 40 c0 de 7f |
    | rcr r9b, 0x01  | 41 d0 d9    | *** | rcr dil, 0x80  | 40 c0 df 80 |
    | rcr r10b, 0x01 | 41 d0 da    | *** | rcr r8b, 0xff  | 41 c0 d8 ff |
    | rcr r11b, 0x01 | 41 d0 db    | *** | rcr r9b, 0x00  | 41 c0 d9 00 |
    | rcr r12b, 0x01 | 41 d0 dc    | *** | rcr r11b, 0x7f | 41 c0 db 7f |
    | rcr r13b, 0x01 | 41 d0 dd    | *** | rcr r12b, 0x80 | 41 c0 dc 80 |
    | rcr r14b, 0x01 | 41 d0 de    | *** | rcr r13b, 0xff | 41 c0 dd ff |
    | rcr r15b, 0x01 | 41 d0 df    | *** | rcr r14b, 0x00 | 41 c0 de 00 |
    | rcr ah, 0x01   | d0 dc       | *** | rcr ah, 0x7f   | c0 dc 7f    |
    | rcr ch, 0x01   | d0 dd       | *** | rcr ch, 0x80   | c0 dd 80    |
    | rcr dh, 0x01   | d0 de       | *** | rcr dh, 0xff   | c0 de ff    |
    | rcr bh, 0x01   | d0 df       | *** | rcr bh, 0x00   | c0 df 00    |
    | -------------- | ----------- | --- | -------------- | ----------- |
"""


def can_encode_rcr_reg8_imm8():
    encode(RCR_REG8_IMM8)


RCR_REG8_CL = """
    | ------------ | -------- | --- | ------------ | -------- |
    | instruction  | encoding | *** | instruction  | encoding |
    | ------------ | -------- | --- | ------------ | -------- |
    | rcr al, cl   | d2 d8    | *** | rcr r10b, cl | 41 d2 da |
    | rcr cl, cl   | d2 d9    | *** | rcr r11b, cl | 41 d2 db |
    | rcr dl, cl   | d2 da    | *** | rcr r12b, cl | 41 d2 dc |
    | rcr bl, cl   | d2 db    | *** | rcr r13b, cl | 41 d2 dd |
    | rcr spl, cl  | 40 d2 dc | *** | rcr r14b, cl | 41 d2 de |
    | rcr bpl, cl  | 40 d2 dd | *** | rcr r15b, cl | 41 d2 df |
    | rcr sil, cl  | 40 d2 de | *** | rcr ah, cl   | d2 dc    |
    | rcr dil, cl  | 40 d2 df | *** | rcr ch, cl   | d2 dd    |
    | rcr r8b, cl  | 41 d2 d8 | *** | rcr dh, cl   | d2 de    |
    | rcr r9b, cl  | 41 d2 d9 | *** | rcr bh, cl   | d2 df    |
    | ------------ | -------- | --- | ------------ | -------- |
"""


def can_encode_rcr_reg8_cl():
    encode(RCR_REG8_CL)


RCR_ADDR64_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | rcr qword [rax], 0x01                        | 48 d1 18                   |
    | rcr qword [rcx], 0x01                        | 48 d1 19                   |
    | rcr qword [rdx], 0x01                        | 48 d1 1a                   |
    | rcr qword [rbx], 0x01                        | 48 d1 1b                   |
    | rcr qword [rsp], 0x01                        | 48 d1 1c 24                |
    | rcr qword [rbp], 0x01                        | 48 d1 5d 00                |
    | rcr qword [rsi], 0x01                        | 48 d1 1e                   |
    | rcr qword [rdi], 0x01                        | 48 d1 1f                   |
    | rcr qword [r8], 0x01                         | 49 d1 18                   |
    | rcr qword [r9], 0x01                         | 49 d1 19                   |
    | rcr qword [r10], 0x01                        | 49 d1 1a                   |
    | rcr qword [r11], 0x01                        | 49 d1 1b                   |
    | rcr qword [r12], 0x01                        | 49 d1 1c 24                |
    | rcr qword [r13], 0x01                        | 49 d1 5d 00                |
    | rcr qword [r14], 0x01                        | 49 d1 1e                   |
    | rcr qword [r15], 0x01                        | 49 d1 1f                   |
    | rcr qword [rax + 1 * rcx], 0x01              | 48 d1 1c 08                |
    | rcr qword [rcx + 1 * rcx], 0x01              | 48 d1 1c 09                |
    | rcr qword [rdx + 1 * rcx], 0x01              | 48 d1 1c 0a                |
    | rcr qword [rbx + 1 * rcx], 0x01              | 48 d1 1c 0b                |
    | rcr qword [rsp + 1 * rcx], 0x01              | 48 d1 1c 0c                |
    | rcr qword [rbp + 1 * rcx], 0x01              | 48 d1 5c 0d 00             |
    | rcr qword [rsi + 1 * rcx], 0x01              | 48 d1 1c 0e                |
    | rcr qword [rdi + 1 * rcx], 0x01              | 48 d1 1c 0f                |
    | rcr qword [r8 + 1 * rcx], 0x01               | 49 d1 1c 08                |
    | rcr qword [r9 + 1 * rcx], 0x01               | 49 d1 1c 09                |
    | rcr qword [r10 + 1 * rcx], 0x01              | 49 d1 1c 0a                |
    | rcr qword [r11 + 1 * rcx], 0x01              | 49 d1 1c 0b                |
    | rcr qword [r12 + 1 * rcx], 0x01              | 49 d1 1c 0c                |
    | rcr qword [r13 + 1 * rcx], 0x01              | 49 d1 5c 0d 00             |
    | rcr qword [r14 + 1 * rcx], 0x01              | 49 d1 1c 0e                |
    | rcr qword [r15 + 1 * rcx], 0x01              | 49 d1 1c 0f                |
    | rcr qword [rax + 1 * rax], 0x01              | 48 d1 1c 00                |
    | rcr qword [rax + 1 * rdx], 0x01              | 48 d1 1c 10                |
    | rcr qword [rax + 1 * rbx], 0x01              | 48 d1 1c 18                |
    | rcr qword [rax + 1 * rbp], 0x01              | 48 d1 1c 28                |
    | rcr qword [rax + 1 * rsi], 0x01              | 48 d1 1c 30                |
    | rcr qword [rax + 1 * rdi], 0x01              | 48 d1 1c 38                |
    | rcr qword [rax + 1 * r8], 0x01               | 4a d1 1c 00                |
    | rcr qword [rax + 1 * r9], 0x01               | 4a d1 1c 08                |
    | rcr qword [rax + 1 * r10], 0x01              | 4a d1 1c 10                |
    | rcr qword [rax + 1 * r11], 0x01              | 4a d1 1c 18                |
    | rcr qword [rax + 1 * r12], 0x01              | 4a d1 1c 20                |
    | rcr qword [rax + 1 * r13], 0x01              | 4a d1 1c 28                |
    | rcr qword [rax + 1 * r14], 0x01              | 4a d1 1c 30                |
    | rcr qword [rax + 1 * r15], 0x01              | 4a d1 1c 38                |
    | rcr qword [rax + 2 * rcx], 0x01              | 48 d1 1c 48                |
    | rcr qword [rax + 4 * rcx], 0x01              | 48 d1 1c 88                |
    | rcr qword [rax + 8 * rcx], 0x01              | 48 d1 1c c8                |
    | rcr qword [r8 + 1 * r9], 0x01                | 4b d1 1c 08                |
    | rcr qword [r8 + 2 * r9], 0x01                | 4b d1 1c 48                |
    | rcr qword [r8 + 4 * r9], 0x01                | 4b d1 1c 88                |
    | rcr qword [r8 + 8 * r9], 0x01                | 4b d1 1c c8                |
    | rcr qword [1 * rcx], 0x01                    | 48 d1 1c 0d 00 00 00 00    |
    | rcr qword [2 * rcx], 0x01                    | 48 d1 1c 4d 00 00 00 00    |
    | rcr qword [4 * rcx], 0x01                    | 48 d1 1c 8d 00 00 00 00    |
    | rcr qword [8 * rcx], 0x01                    | 48 d1 1c cd 00 00 00 00    |
    | rcr qword [1 * r9], 0x01                     | 4a d1 1c 0d 00 00 00 00    |
    | rcr qword [2 * r9], 0x01                     | 4a d1 1c 4d 00 00 00 00    |
    | rcr qword [4 * r9], 0x01                     | 4a d1 1c 8d 00 00 00 00    |
    | rcr qword [8 * r9], 0x01                     | 4a d1 1c cd 00 00 00 00    |
    | rcr qword [r13 + 8 * r12], 0x01              | 4b d1 5c e5 00             |
    | rcr qword [rsp + 4 * r15], 0x01              | 4a d1 1c bc                |
    | rcr qword [rax + 1 * rcx + 0x00], 0x01       | 48 d1 5c 08 00             |
    | rcr qword [rax + 1 * rcx - 0x00], 0x01       | 48 d1 5c 08 00             |
    | rcr qword [rax + 1 * rcx + 0x01], 0x01       | 48 d1 5c 08 01             |
    | rcr qword [rax + 1 * rcx - 0x01], 0x01       | 48 d1 5c 08 ff             |
    | rcr qword [rax + 1 * rcx + 0x00000001], 0x01 | 48 d1 9c 08 01 00 00 00    |
    | rcr qword [rax + 1 * rcx - 0x00000001], 0x01 | 48 d1 9c 08 ff ff ff ff    |
    | rcr qword [rax + 1 * rcx + 0x7f], 0x01       | 48 d1 5c 08 7f             |
    | rcr qword [rax + 1 * rcx - 0x7f], 0x01       | 48 d1 5c 08 81             |
    | rcr qword [rax + 1 * rcx + 0x80], 0x01       | 48 d1 9c 08 80 00 00 00    |
    | rcr qword [rax + 1 * rcx - 0x80], 0x01       | 48 d1 5c 08 80             |
    | rcr qword [rax + 1 * rcx - 0x81], 0x01       | 48 d1 9c 08 7f ff ff ff    |
    | rcr qword [rax + 1 * rcx + 0xff], 0x01       | 48 d1 9c 08 ff 00 00 00    |
    | rcr qword [rax + 1 * rcx - 0xff], 0x01       | 48 d1 9c 08 01 ff ff ff    |
    | rcr qword [rax + 1 * rcx + 0x7fffffff], 0x01 | 48 d1 9c 08 ff ff ff 7f    |
    | rcr qword [rax + 1 * rcx - 0x7fffffff], 0x01 | 48 d1 9c 08 01 00 00 80    |
    | rcr qword [rax + 1 * rcx - 0x80000000], 0x01 | 48 d1 9c 08 00 00 00 80    |
    | rcr qword [r10 + 0x7f], 0x01                 | 49 d1 5a 7f                |
    | rcr qword [r10 + 0x80], 0x01                 | 49 d1 9a 80 00 00 00       |
    | rcr qword [r10 - 0x80], 0x01                 | 49 d1 5a 80                |
    | rcr qword [r10 - 0x81], 0x01                 | 49 d1 9a 7f ff ff ff       |
    | rcr qword [rax], 0x00                        | 48 c1 18 00                |
    | rcr qword [rax], 0x7f                        | 48 c1 18 7f                |
    | rcr qword [rax], 0x80                        | 48 c1 18 80                |
    | rcr qword [rax], 0xff                        | 48 c1 18 ff                |
    | rcr qword [rcx], 0x7f                        | 48 c1 19 7f                |
    | rcr qword [rdx], 0x80                        | 48 c1 1a 80                |
    | rcr qword [rbx], 0xff                        | 48 c1 1b ff                |
    | rcr qword [rsp], 0x00                        | 48 c1 1c 24 00             |
    | rcr qword [rsi], 0x7f                        | 48 c1 1e 7f                |
    | rcr qword [rdi], 0x80                        | 48 c1 1f 80                |
    | rcr qword [r8], 0xff                         | 49 c1 18 ff                |
    | rcr qword [r9], 0x00                         | 49 c1 19 00                |
    | rcr qword [r11], 0x7f                        | 49 c1 1b 7f                |
    | rcr qword [r12], 0x80                        | 49 c1 1c 24 80             |
    | rcr qword [r13], 0xff                        | 49 c1 5d 00 ff             |
    | rcr qword [r14], 0x00                        | 49 c1 1e 00                |
    | rcr qword [rax + 1 * rcx], 0x7f              | 48 c1 1c 08 7f             |
    | rcr qword [rcx + 1 * rcx], 0x80              | 48 c1 1c 09 80             |
    | rcr qword [rdx + 1 * rcx], 0xff              | 48 c1 1c 0a ff             |
    | rcr qword [rbx + 1 * rcx], 0x00              | 48 c1 1c 0b 00             |
    | rcr qword [rbp + 1 * rcx], 0x7f              | 48 c1 5c 0d 00 7f          |
    | rcr qword [rsi + 1 * rcx], 0x80              | 48 c1 1c 0e 80             |
    | rcr qword [rdi + 1 * rcx], 0xff              | 48 c1 1c 0f ff             |
    | rcr qword [r8 + 1 * rcx], 0x00               | 49 c1 1c 08 00             |
    | rcr qword [r10 + 1 * rcx], 0x7f              | 49 c1 1c 0a 7f             |
    | rcr qword [r11 + 1 * rcx], 0x80              | 49 c1 1c 0b 80             |
    | rcr qword [r12 + 1 * rcx], 0xff              | 49 c1 1c 0c ff             |
    | rcr qword [r13 + 1 * rcx], 0x00              | 49 c1 5c 0d 00 00          |
    | rcr qword [r15 + 1 * rcx], 0x7f              | 49 c1 1c 0f 7f             |
    | rcr qword [rax + 1 * rax], 0x80              | 48 c1 1c 00 80             |
    | rcr qword [rax + 1 * rdx], 0xff              | 48 c1 1c 10 ff             |
    | rcr qword [rax + 1 * rbx], 0x00              | 48 c1 1c 18 00             |
    | rcr qword [rax + 1 * rsi], 0x7f              | 48 c1 1c 30 7f             |
    | rcr qword [rax + 1 * rdi], 0x80              | 48 c1 1c 38 80             |
    | rcr qword [rax + 1 * r8], 0xff               | 4a c1 1c 00 ff             |
    | rcr qword [rax + 1 * r9], 0x00               | 4a c1 1c 08 00             |
    | rcr qword [rax + 1 * r11], 0x7f              | 4a c1 1c 18 7f             |
    | rcr qword [rax + 1 * r12], 0x80              | 4a c1 1c 20 80             |
    | rcr qword [rax + 1 * r13], 0xff              | 4a c1 1c 28 ff             |
    | rcr qword [rax + 1 * r14], 0x00              | 4a c1 1c 30 00             |
    | rcr qword [rax + 2 * rcx], 0x7f              | 48 c1 1c 48 7f             |
    | rcr qword [rax + 4 * rcx], 0x80              | 48 c1 1c 88 80             |
    | rcr qword [rax + 8 * rcx], 0xff              | 48 c1 1c c8 ff             |
    | rcr qword [r8 + 1 * r9], 0x00                | 4b c1 1c 08 00             |
    | rcr qword [r8 + 4 * r9], 0x7f                | 4b c1 1c 88 7f             |
    | rcr qword [r8 + 8 * r9], 0x80                | 4b c1 1c c8 80             |
    | rcr qword [1 * rcx], 0xff                    | 48 c1 1c 0d 00 00 00 00 ff |
    | rcr qword [2 * rcx], 0x00                    | 48 c1 1c 4d 00 00 00 00 00 |
    | rcr qword [8 * rcx], 0x7f                    | 48 c1 1c cd 00 00 00 00 7f |
    | rcr qword [1 * r9], 0x80                     | 4a c1 1c 0d 00 00 00 00 80 |
    | rcr qword [2 * r9], 0xff                     | 4a c1 1c 4d 00 00 00 00 ff |
    | rcr qword [4 * r9], 0x00                     | 4a c1 1c 8d 00 00 00 00 00 |
    | rcr qword [r13 + 8 * r12], 0x7f              | 4b c1 5c e5 00 7f          |
    | rcr qword [rsp + 4 * r15], 0x80              | 4a c1 1c bc 80             |
    | rcr qword [rax + 1 * rcx + 0x00], 0xff       | 48 c1 5c 08 00 ff          |
    | rcr qword [rax + 1 * rcx - 0x00], 0x00       | 48 c1 5c 08 00 00          |
    | rcr qword [rax + 1 * rcx - 0x01], 0x7f       | 48 c1 5c 08 ff 7f          |
    | rcr qword [rax + 1 * rcx + 0x00000001], 0x80 | 48 c1 9c 08 01 00 00 00 80 |
    | rcr qword [rax + 1 * rcx - 0x00000001], 0xff | 48 c1 9c 08 ff ff ff ff ff |
    | rcr qword [rax + 1 * rcx + 0x7f], 0x00       | 48 c1 5c 08 7f 00          |
    | rcr qword [rax + 1 * rcx + 0x80], 0x7f       | 48 c1 9c 08 80 00 00 00 7f |
    | rcr qword [rax + 1 * rcx - 0x80], 0x80       | 48 c1 5c 08 80 80          |
    | rcr qword [rax + 1 * rcx - 0x81], 0xff       | 48 c1 9c 08 7f ff ff ff ff |
    | rcr qword [rax + 1 * rcx + 0xff], 0x00       | 48 c1 9c 08 ff 00 00 00 00 |
    | rcr qword [rax + 1 * rcx + 0x7fffffff], 0x7f | 48 c1 9c 08 ff ff ff 7f 7f |
    | rcr qword [rax + 1 * rcx - 0x7fffffff], 0x80 | 48 c1 9c 08 01 00 00 80 80 |
    | rcr qword [rax + 1 * rcx - 0x80000000], 0xff | 48 c1 9c 08 00 00 00 80 ff |
    | rcr qword [r10 + 0x7f], 0x00                 | 49 c1 5a 7f 00             |
    | rcr qword [r10 - 0x80], 0x7f                 | 49 c1 5a 80 7f             |
    | rcr qword [r10 - 0x81], 0x80                 | 49 c1 9a 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_rcr_addr64_imm8():
    encode(RCR_ADDR64_IMM8)


RCR_ADDR64_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | rcr qword [rax], cl                        | 48 d3 18                |
    | rcr qword [rcx], cl                        | 48 d3 19                |
    | rcr qword [rdx], cl                        | 48 d3 1a                |
    | rcr qword [rbx], cl                        | 48 d3 1b                |
    | rcr qword [rsp], cl                        | 48 d3 1c 24             |
    | rcr qword [rbp], cl                        | 48 d3 5d 00             |
    | rcr qword [rsi], cl                        | 48 d3 1e                |
    | rcr qword [rdi], cl                        | 48 d3 1f                |
    | rcr qword [r8], cl                         | 49 d3 18                |
    | rcr qword [r9], cl                         | 49 d3 19                |
    | rcr qword [r10], cl                        | 49 d3 1a                |
    | rcr qword [r11], cl                        | 49 d3 1b                |
    | rcr qword [r12], cl                        | 49 d3 1c 24             |
    | rcr qword [r13], cl                        | 49 d3 5d 00             |
    | rcr qword [r14], cl                        | 49 d3 1e                |
    | rcr qword [r15], cl                        | 49 d3 1f                |
    | rcr qword [rax + 1 * rcx], cl              | 48 d3 1c 08             |
    | rcr qword [rcx + 1 * rcx], cl              | 48 d3 1c 09             |
    | rcr qword [rdx + 1 * rcx], cl              | 48 d3 1c 0a             |
    | rcr qword [rbx + 1 * rcx], cl              | 48 d3 1c 0b             |
    | rcr qword [rsp + 1 * rcx], cl              | 48 d3 1c 0c             |
    | rcr qword [rbp + 1 * rcx], cl              | 48 d3 5c 0d 00          |
    | rcr qword [rsi + 1 * rcx], cl              | 48 d3 1c 0e             |
    | rcr qword [rdi + 1 * rcx], cl              | 48 d3 1c 0f             |
    | rcr qword [r8 + 1 * rcx], cl               | 49 d3 1c 08             |
    | rcr qword [r9 + 1 * rcx], cl               | 49 d3 1c 09             |
    | rcr qword [r10 + 1 * rcx], cl              | 49 d3 1c 0a             |
    | rcr qword [r11 + 1 * rcx], cl              | 49 d3 1c 0b             |
    | rcr qword [r12 + 1 * rcx], cl              | 49 d3 1c 0c             |
    | rcr qword [r13 + 1 * rcx], cl              | 49 d3 5c 0d 00          |
    | rcr qword [r14 + 1 * rcx], cl              | 49 d3 1c 0e             |
    | rcr qword [r15 + 1 * rcx], cl              | 49 d3 1c 0f             |
    | rcr qword [rax + 1 * rax], cl              | 48 d3 1c 00             |
    | rcr qword [rax + 1 * rdx], cl              | 48 d3 1c 10             |
    | rcr qword [rax + 1 * rbx], cl              | 48 d3 1c 18             |
    | rcr qword [rax + 1 * rbp], cl              | 48 d3 1c 28             |
    | rcr qword [rax + 1 * rsi], cl              | 48 d3 1c 30             |
    | rcr qword [rax + 1 * rdi], cl              | 48 d3 1c 38             |
    | rcr qword [rax + 1 * r8], cl               | 4a d3 1c 00             |
    | rcr qword [rax + 1 * r9], cl               | 4a d3 1c 08             |
    | rcr qword [rax + 1 * r10], cl              | 4a d3 1c 10             |
    | rcr qword [rax + 1 * r11], cl              | 4a d3 1c 18             |
    | rcr qword [rax + 1 * r12], cl              | 4a d3 1c 20             |
    | rcr qword [rax + 1 * r13], cl              | 4a d3 1c 28             |
    | rcr qword [rax + 1 * r14], cl              | 4a d3 1c 30             |
    | rcr qword [rax + 1 * r15], cl              | 4a d3 1c 38             |
    | rcr qword [rax + 2 * rcx], cl              | 48 d3 1c 48             |
    | rcr qword [rax + 4 * rcx], cl              | 48 d3 1c 88             |
    | rcr qword [rax + 8 * rcx], cl              | 48 d3 1c c8             |
    | rcr qword [r8 + 1 * r9], cl                | 4b d3 1c 08             |
    | rcr qword [r8 + 2 * r9], cl                | 4b d3 1c 48             |
    | rcr qword [r8 + 4 * r9], cl                | 4b d3 1c 88             |
    | rcr qword [r8 + 8 * r9], cl                | 4b d3 1c c8             |
    | rcr qword [1 * rcx], cl                    | 48 d3 1c 0d 00 00 00 00 |
    | rcr qword [2 * rcx], cl                    | 48 d3 1c 4d 00 00 00 00 |
    | rcr qword [4 * rcx], cl                    | 48 d3 1c 8d 00 00 00 00 |
    | rcr qword [8 * rcx], cl                    | 48 d3 1c cd 00 00 00 00 |
    | rcr qword [1 * r9], cl                     | 4a d3 1c 0d 00 00 00 00 |
    | rcr qword [2 * r9], cl                     | 4a d3 1c 4d 00 00 00 00 |
    | rcr qword [4 * r9], cl                     | 4a d3 1c 8d 00 00 00 00 |
    | rcr qword [8 * r9], cl                     | 4a d3 1c cd 00 00 00 00 |
    | rcr qword [r13 + 8 * r12], cl              | 4b d3 5c e5 00          |
    | rcr qword [rsp + 4 * r15], cl              | 4a d3 1c bc             |
    | rcr qword [rax + 1 * rcx + 0x00], cl       | 48 d3 5c 08 00          |
    | rcr qword [rax + 1 * rcx - 0x00], cl       | 48 d3 5c 08 00          |
    | rcr qword [rax + 1 * rcx + 0x01], cl       | 48 d3 5c 08 01          |
    | rcr qword [rax + 1 * rcx - 0x01], cl       | 48 d3 5c 08 ff          |
    | rcr qword [rax + 1 * rcx + 0x00000001], cl | 48 d3 9c 08 01 00 00 00 |
    | rcr qword [rax + 1 * rcx - 0x00000001], cl | 48 d3 9c 08 ff ff ff ff |
    | rcr qword [rax + 1 * rcx + 0x7f], cl       | 48 d3 5c 08 7f          |
    | rcr qword [rax + 1 * rcx - 0x7f], cl       | 48 d3 5c 08 81          |
    | rcr qword [rax + 1 * rcx + 0x80], cl       | 48 d3 9c 08 80 00 00 00 |
    | rcr qword [rax + 1 * rcx - 0x80], cl       | 48 d3 5c 08 80          |
    | rcr qword [rax + 1 * rcx - 0x81], cl       | 48 d3 9c 08 7f ff ff ff |
    | rcr qword [rax + 1 * rcx + 0xff], cl       | 48 d3 9c 08 ff 00 00 00 |
    | rcr qword [rax + 1 * rcx - 0xff], cl       | 48 d3 9c 08 01 ff ff ff |
    | rcr qword [rax + 1 * rcx + 0x7fffffff], cl | 48 d3 9c 08 ff ff ff 7f |
    | rcr qword [rax + 1 * rcx - 0x7fffffff], cl | 48 d3 9c 08 01 00 00 80 |
    | rcr qword [rax + 1 * rcx - 0x80000000], cl | 48 d3 9c 08 00 00 00 80 |
    | rcr qword [r10 + 0x7f], cl                 | 49 d3 5a 7f             |
    | rcr qword [r10 + 0x80], cl                 | 49 d3 9a 80 00 00 00    |
    | rcr qword [r10 - 0x80], cl                 | 49 d3 5a 80             |
    | rcr qword [r10 - 0x81], cl                 | 49 d3 9a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_rcr_addr64_cl():
    encode(RCR_ADDR64_CL)


RCR_ADDR32_IMM8 = """
    | -------------------------------------------- | -------------------------- |
    | instruction                                  | encoding                   |
    | -------------------------------------------- | -------------------------- |
    | rcr dword [rax], 0x01                        | d1 18                      |
    | rcr dword [rcx], 0x01                        | d1 19                      |
    | rcr dword [rdx], 0x01                        | d1 1a                      |
    | rcr dword [rbx], 0x01                        | d1 1b                      |
    | rcr dword [rsp], 0x01                        | d1 1c 24                   |
    | rcr dword [rbp], 0x01                        | d1 5d 00                   |
    | rcr dword [rsi], 0x01                        | d1 1e                      |
    | rcr dword [rdi], 0x01                        | d1 1f                      |
    | rcr dword [r8], 0x01                         | 41 d1 18                   |
    | rcr dword [r9], 0x01                         | 41 d1 19                   |
    | rcr dword [r10], 0x01                        | 41 d1 1a                   |
    | rcr dword [r11], 0x01                        | 41 d1 1b                   |
    | rcr dword [r12], 0x01                        | 41 d1 1c 24                |
    | rcr dword [r13], 0x01                        | 41 d1 5d 00                |
    | rcr dword [r14], 0x01                        | 41 d1 1e                   |
    | rcr dword [r15], 0x01                        | 41 d1 1f                   |
    | rcr dword [rax + 1 * rcx], 0x01              | d1 1c 08                   |
    | rcr dword [rcx + 1 * rcx], 0x01              | d1 1c 09                   |
    | rcr dword [rdx + 1 * rcx], 0x01              | d1 1c 0a                   |
    | rcr dword [rbx + 1 * rcx], 0x01              | d1 1c 0b                   |
    | rcr dword [rsp + 1 * rcx], 0x01              | d1 1c 0c                   |
    | rcr dword [rbp + 1 * rcx], 0x01              | d1 5c 0d 00                |
    | rcr dword [rsi + 1 * rcx], 0x01              | d1 1c 0e                   |
    | rcr dword [rdi + 1 * rcx], 0x01              | d1 1c 0f                   |
    | rcr dword [r8 + 1 * rcx], 0x01               | 41 d1 1c 08                |
    | rcr dword [r9 + 1 * rcx], 0x01               | 41 d1 1c 09                |
    | rcr dword [r10 + 1 * rcx], 0x01              | 41 d1 1c 0a                |
    | rcr dword [r11 + 1 * rcx], 0x01              | 41 d1 1c 0b                |
    | rcr dword [r12 + 1 * rcx], 0x01              | 41 d1 1c 0c                |
    | rcr dword [r13 + 1 * rcx], 0x01              | 41 d1 5c 0d 00             |
    | rcr dword [r14 + 1 * rcx], 0x01              | 41 d1 1c 0e                |
    | rcr dword [r15 + 1 * rcx], 0x01              | 41 d1 1c 0f                |
    | rcr dword [rax + 1 * rax], 0x01              | d1 1c 00                   |
    | rcr dword [rax + 1 * rdx], 0x01              | d1 1c 10                   |
    | rcr dword [rax + 1 * rbx], 0x01              | d1 1c 18                   |
    | rcr dword [rax + 1 * rbp], 0x01              | d1 1c 28                   |
    | rcr dword [rax + 1 * rsi], 0x01              | d1 1c 30                   |
    | rcr dword [rax + 1 * rdi], 0x01              | d1 1c 38                   |
    | rcr dword [rax + 1 * r8], 0x01               | 42 d1 1c 00                |
    | rcr dword [rax + 1 * r9], 0x01               | 42 d1 1c 08                |
    | rcr dword [rax + 1 * r10], 0x01              | 42 d1 1c 10                |
    | rcr dword [rax + 1 * r11], 0x01              | 42 d1 1c 18                |
    | rcr dword [rax + 1 * r12], 0x01              | 42 d1 1c 20                |
    | rcr dword [rax + 1 * r13], 0x01              | 42 d1 1c 28                |
    | rcr dword [rax + 1 * r14], 0x01              | 42 d1 1c 30                |
    | rcr dword [rax + 1 * r15], 0x01              | 42 d1 1c 38                |
    | rcr dword [rax + 2 * rcx], 0x01              | d1 1c 48                   |
    | rcr dword [rax + 4 * rcx], 0x01              | d1 1c 88                   |
    | rcr dword [rax + 8 * rcx], 0x01              | d1 1c c8                   |
    | rcr dword [r8 + 1 * r9], 0x01                | 43 d1 1c 08                |
    | rcr dword [r8 + 2 * r9], 0x01                | 43 d1 1c 48                |
    | rcr dword [r8 + 4 * r9], 0x01                | 43 d1 1c 88                |
    | rcr dword [r8 + 8 * r9], 0x01                | 43 d1 1c c8                |
    | rcr dword [1 * rcx], 0x01                    | d1 1c 0d 00 00 00 00       |
    | rcr dword [2 * rcx], 0x01                    | d1 1c 4d 00 00 00 00       |
    | rcr dword [4 * rcx], 0x01                    | d1 1c 8d 00 00 00 00       |
    | rcr dword [8 * rcx], 0x01                    | d1 1c cd 00 00 00 00       |
    | rcr dword [1 * r9], 0x01                     | 42 d1 1c 0d 00 00 00 00    |
    | rcr dword [2 * r9], 0x01                     | 42 d1 1c 4d 00 00 00 00    |
    | rcr dword [4 * r9], 0x01                     | 42 d1 1c 8d 00 00 00 00    |
    | rcr dword [8 * r9], 0x01                     | 42 d1 1c cd 00 00 00 00    |
    | rcr dword [r13 + 8 * r12], 0x01              | 43 d1 5c e5 00             |
    | rcr dword [rsp + 4 * r15], 0x01              | 42 d1 1c bc                |
    | rcr dword [rax + 1 * rcx + 0x00], 0x01       | d1 5c 08 00                |
    | rcr dword [rax + 1 * rcx - 0x00], 0x01       | d1 5c 08 00                |
    | rcr dword [rax + 1 * rcx + 0x01], 0x01       | d1 5c 08 01                |
    | rcr dword [rax + 1 * rcx - 0x01], 0x01       | d1 5c 08 ff                |
    | rcr dword [rax + 1 * rcx + 0x00000001], 0x01 | d1 9c 08 01 00 00 00       |
    | rcr dword [rax + 1 * rcx - 0x00000001], 0x01 | d1 9c 08 ff ff ff ff       |
    | rcr dword [rax + 1 * rcx + 0x7f], 0x01       | d1 5c 08 7f                |
    | rcr dword [rax + 1 * rcx - 0x7f], 0x01       | d1 5c 08 81                |
    | rcr dword [rax + 1 * rcx + 0x80], 0x01       | d1 9c 08 80 00 00 00       |
    | rcr dword [rax + 1 * rcx - 0x80], 0x01       | d1 5c 08 80                |
    | rcr dword [rax + 1 * rcx - 0x81], 0x01       | d1 9c 08 7f ff ff ff       |
    | rcr dword [rax + 1 * rcx + 0xff], 0x01       | d1 9c 08 ff 00 00 00       |
    | rcr dword [rax + 1 * rcx - 0xff], 0x01       | d1 9c 08 01 ff ff ff       |
    | rcr dword [rax + 1 * rcx + 0x7fffffff], 0x01 | d1 9c 08 ff ff ff 7f       |
    | rcr dword [rax + 1 * rcx - 0x7fffffff], 0x01 | d1 9c 08 01 00 00 80       |
    | rcr dword [rax + 1 * rcx - 0x80000000], 0x01 | d1 9c 08 00 00 00 80       |
    | rcr dword [r10 + 0x7f], 0x01                 | 41 d1 5a 7f                |
    | rcr dword [r10 + 0x80], 0x01                 | 41 d1 9a 80 00 00 00       |
    | rcr dword [r10 - 0x80], 0x01                 | 41 d1 5a 80                |
    | rcr dword [r10 - 0x81], 0x01                 | 41 d1 9a 7f ff ff ff       |
    | rcr dword [rax], 0x00                        | c1 18 00                   |
    | rcr dword [rax], 0x7f                        | c1 18 7f                   |
    | rcr dword [rax], 0x80                        | c1 18 80                   |
    | rcr dword [rax], 0xff                        | c1 18 ff                   |
    | rcr dword [rcx], 0x7f                        | c1 19 7f                   |
    | rcr dword [rdx], 0x80                        | c1 1a 80                   |
    | rcr dword [rbx], 0xff                        | c1 1b ff                   |
    | rcr dword [rsp], 0x00                        | c1 1c 24 00                |
    | rcr dword [rsi], 0x7f                        | c1 1e 7f                   |
    | rcr dword [rdi], 0x80                        | c1 1f 80                   |
    | rcr dword [r8], 0xff                         | 41 c1 18 ff                |
    | rcr dword [r9], 0x00                         | 41 c1 19 00                |
    | rcr dword [r11], 0x7f                        | 41 c1 1b 7f                |
    | rcr dword [r12], 0x80                        | 41 c1 1c 24 80             |
    | rcr dword [r13], 0xff                        | 41 c1 5d 00 ff             |
    | rcr dword [r14], 0x00                        | 41 c1 1e 00                |
    | rcr dword [rax + 1 * rcx], 0x7f              | c1 1c 08 7f                |
    | rcr dword [rcx + 1 * rcx], 0x80              | c1 1c 09 80                |
    | rcr dword [rdx + 1 * rcx], 0xff              | c1 1c 0a ff                |
    | rcr dword [rbx + 1 * rcx], 0x00              | c1 1c 0b 00                |
    | rcr dword [rbp + 1 * rcx], 0x7f              | c1 5c 0d 00 7f             |
    | rcr dword [rsi + 1 * rcx], 0x80              | c1 1c 0e 80                |
    | rcr dword [rdi + 1 * rcx], 0xff              | c1 1c 0f ff                |
    | rcr dword [r8 + 1 * rcx], 0x00               | 41 c1 1c 08 00             |
    | rcr dword [r10 + 1 * rcx], 0x7f              | 41 c1 1c 0a 7f             |
    | rcr dword [r11 + 1 * rcx], 0x80              | 41 c1 1c 0b 80             |
    | rcr dword [r12 + 1 * rcx], 0xff              | 41 c1 1c 0c ff             |
    | rcr dword [r13 + 1 * rcx], 0x00              | 41 c1 5c 0d 00 00          |
    | rcr dword [r15 + 1 * rcx], 0x7f              | 41 c1 1c 0f 7f             |
    | rcr dword [rax + 1 * rax], 0x80              | c1 1c 00 80                |
    | rcr dword [rax + 1 * rdx], 0xff              | c1 1c 10 ff                |
    | rcr dword [rax + 1 * rbx], 0x00              | c1 1c 18 00                |
    | rcr dword [rax + 1 * rsi], 0x7f              | c1 1c 30 7f                |
    | rcr dword [rax + 1 * rdi], 0x80              | c1 1c 38 80                |
    | rcr dword [rax + 1 * r8], 0xff               | 42 c1 1c 00 ff             |
    | rcr dword [rax + 1 * r9], 0x00               | 42 c1 1c 08 00             |
    | rcr dword [rax + 1 * r11], 0x7f              | 42 c1 1c 18 7f             |
    | rcr dword [rax + 1 * r12], 0x80              | 42 c1 1c 20 80             |
    | rcr dword [rax + 1 * r13], 0xff              | 42 c1 1c 28 ff             |
    | rcr dword [rax + 1 * r14], 0x00              | 42 c1 1c 30 00             |
    | rcr dword [rax + 2 * rcx], 0x7f              | c1 1c 48 7f                |
    | rcr dword [rax + 4 * rcx], 0x80              | c1 1c 88 80                |
    | rcr dword [rax + 8 * rcx], 0xff              | c1 1c c8 ff                |
    | rcr dword [r8 + 1 * r9], 0x00                | 43 c1 1c 08 00             |
    | rcr dword [r8 + 4 * r9], 0x7f                | 43 c1 1c 88 7f             |
    | rcr dword [r8 + 8 * r9], 0x80                | 43 c1 1c c8 80             |
    | rcr dword [1 * rcx], 0xff                    | c1 1c 0d 00 00 00 00 ff    |
    | rcr dword [2 * rcx], 0x00                    | c1 1c 4d 00 00 00 00 00    |
    | rcr dword [8 * rcx], 0x7f                    | c1 1c cd 00 00 00 00 7f    |
    | rcr dword [1 * r9], 0x80                     | 42 c1 1c 0d 00 00 00 00 80 |
    | rcr dword [2 * r9], 0xff                     | 42 c1 1c 4d 00 00 00 00 ff |
    | rcr dword [4 * r9], 0x00                     | 42 c1 1c 8d 00 00 00 00 00 |
    | rcr dword [r13 + 8 * r12], 0x7f              | 43 c1 5c e5 00 7f          |
    | rcr dword [rsp + 4 * r15], 0x80              | 42 c1 1c bc 80             |
    | rcr dword [rax + 1 * rcx + 0x00], 0xff       | c1 5c 08 00 ff             |
    | rcr dword [rax + 1 * rcx - 0x00], 0x00       | c1 5c 08 00 00             |
    | rcr dword [rax + 1 * rcx - 0x01], 0x7f       | c1 5c 08 ff 7f             |
    | rcr dword [rax + 1 * rcx + 0x00000001], 0x80 | c1 9c 08 01 00 00 00 80    |
    | rcr dword [rax + 1 * rcx - 0x00000001], 0xff | c1 9c 08 ff ff ff ff ff    |
    | rcr dword [rax + 1 * rcx + 0x7f], 0x00       | c1 5c 08 7f 00             |
    | rcr dword [rax + 1 * rcx + 0x80], 0x7f       | c1 9c 08 80 00 00 00 7f    |
    | rcr dword [rax + 1 * rcx - 0x80], 0x80       | c1 5c 08 80 80             |
    | rcr dword [rax + 1 * rcx - 0x81], 0xff       | c1 9c 08 7f ff ff ff ff    |
    | rcr dword [rax + 1 * rcx + 0xff], 0x00       | c1 9c 08 ff 00 00 00 00    |
    | rcr dword [rax + 1 * rcx + 0x7fffffff], 0x7f | c1 9c 08 ff ff ff 7f 7f    |
    | rcr dword [rax + 1 * rcx - 0x7fffffff], 0x80 | c1 9c 08 01 00 00 80 80    |
    | rcr dword [rax + 1 * rcx - 0x80000000], 0xff | c1 9c 08 00 00 00 80 ff    |
    | rcr dword [r10 + 0x7f], 0x00                 | 41 c1 5a 7f 00             |
    | rcr dword [r10 - 0x80], 0x7f                 | 41 c1 5a 80 7f             |
    | rcr dword [r10 - 0x81], 0x80                 | 41 c1 9a 7f ff ff ff 80    |
    | -------------------------------------------- | -------------------------- |
"""


def can_encode_rcr_addr32_imm8():
    encode(RCR_ADDR32_IMM8)


RCR_ADDR32_CL = """
    | ------------------------------------------ | ----------------------- |
    | instruction                                | encoding                |
    | ------------------------------------------ | ----------------------- |
    | rcr dword [rax], cl                        | d3 18                   |
    | rcr dword [rcx], cl                        | d3 19                   |
    | rcr dword [rdx], cl                        | d3 1a                   |
    | rcr dword [rbx], cl                        | d3 1b                   |
    | rcr dword [rsp], cl                        | d3 1c 24                |
    | rcr dword [rbp], cl                        | d3 5d 00                |
    | rcr dword [rsi], cl                        | d3 1e                   |
    | rcr dword [rdi], cl                        | d3 1f                   |
    | rcr dword [r8], cl                         | 41 d3 18                |
    | rcr dword [r9], cl                         | 41 d3 19                |
    | rcr dword [r10], cl                        | 41 d3 1a                |
    | rcr dword [r11], cl                        | 41 d3 1b                |
    | rcr dword [r12], cl                        | 41 d3 1c 24             |
    | rcr dword [r13], cl                        | 41 d3 5d 00             |
    | rcr dword [r14], cl                        | 41 d3 1e                |
    | rcr dword [r15], cl                        | 41 d3 1f                |
    | rcr dword [rax + 1 * rcx], cl              | d3 1c 08                |
    | rcr dword [rcx + 1 * rcx], cl              | d3 1c 09                |
    | rcr dword [rdx + 1 * rcx], cl              | d3 1c 0a                |
    | rcr dword [rbx + 1 * rcx], cl              | d3 1c 0b                |
    | rcr dword [rsp + 1 * rcx], cl              | d3 1c 0c                |
    | rcr dword [rbp + 1 * rcx], cl              | d3 5c 0d 00             |
    | rcr dword [rsi + 1 * rcx], cl              | d3 1c 0e                |
    | rcr dword [rdi + 1 * rcx], cl              | d3 1c 0f                |
    | rcr dword [r8 + 1 * rcx], cl               | 41 d3 1c 08             |
    | rcr dword [r9 + 1 * rcx], cl               | 41 d3 1c 09             |
    | rcr dword [r10 + 1 * rcx], cl              | 41 d3 1c 0a             |
    | rcr dword [r11 + 1 * rcx], cl              | 41 d3 1c 0b             |
    | rcr dword [r12 + 1 * rcx], cl              | 41 d3 1c 0c             |
    | rcr dword [r13 + 1 * rcx], cl              | 41 d3 5c 0d 00          |
    | rcr dword [r14 + 1 * rcx], cl              | 41 d3 1c 0e             |
    | rcr dword [r15 + 1 * rcx], cl              | 41 d3 1c 0f             |
    | rcr dword [rax + 1 * rax], cl              | d3 1c 00                |
    | rcr dword [rax + 1 * rdx], cl              | d3 1c 10                |
    | rcr dword [rax + 1 * rbx], cl              | d3 1c 18                |
    | rcr dword [rax + 1 * rbp], cl              | d3 1c 28                |
    | rcr dword [rax + 1 * rsi], cl              | d3 1c 30                |
    | rcr dword [rax + 1 * rdi], cl              | d3 1c 38                |
    | rcr dword [rax + 1 * r8], cl               | 42 d3 1c 00             |
    | rcr dword [rax + 1 * r9], cl               | 42 d3 1c 08             |
    | rcr dword [rax + 1 * r10], cl              | 42 d3 1c 10             |
    | rcr dword [rax + 1 * r11], cl              | 42 d3 1c 18             |
    | rcr dword [rax + 1 * r12], cl              | 42 d3 1c 20             |
    | rcr dword [rax + 1 * r13], cl              | 42 d3 1c 28             |
    | rcr dword [rax + 1 * r14], cl              | 42 d3 1c 30             |
    | rcr dword [rax + 1 * r15], cl              | 42 d3 1c 38             |
    | rcr dword [rax + 2 * rcx], cl              | d3 1c 48                |
    | rcr dword [rax + 4 * rcx], cl              | d3 1c 88                |
    | rcr dword [rax + 8 * rcx], cl              | d3 1c c8                |
    | rcr dword [r8 + 1 * r9], cl                | 43 d3 1c 08             |
    | rcr dword [r8 + 2 * r9], cl                | 43 d3 1c 48             |
    | rcr dword [r8 + 4 * r9], cl                | 43 d3 1c 88             |
    | rcr dword [r8 + 8 * r9], cl                | 43 d3 1c c8             |
    | rcr dword [1 * rcx], cl                    | d3 1c 0d 00 00 00 00    |
    | rcr dword [2 * rcx], cl                    | d3 1c 4d 00 00 00 00    |
    | rcr dword [4 * rcx], cl                    | d3 1c 8d 00 00 00 00    |
    | rcr dword [8 * rcx], cl                    | d3 1c cd 00 00 00 00    |
    | rcr dword [1 * r9], cl                     | 42 d3 1c 0d 00 00 00 00 |
    | rcr dword [2 * r9], cl                     | 42 d3 1c 4d 00 00 00 00 |
    | rcr dword [4 * r9], cl                     | 42 d3 1c 8d 00 00 00 00 |
    | rcr dword [8 * r9], cl                     | 42 d3 1c cd 00 00 00 00 |
    | rcr dword [r13 + 8 * r12], cl              | 43 d3 5c e5 00          |
    | rcr dword [rsp + 4 * r15], cl              | 42 d3 1c bc             |
    | rcr dword [rax + 1 * rcx + 0x00], cl       | d3 5c 08 00             |
    | rcr dword [rax + 1 * rcx - 0x00], cl       | d3 5c 08 00             |
    | rcr dword [rax + 1 * rcx + 0x01], cl       | d3 5c 08 01             |
    | rcr dword [rax + 1 * rcx - 0x01], cl       | d3 5c 08 ff             |
    | rcr dword [rax + 1 * rcx + 0x00000001], cl | d3 9c 08 01 00 00 00    |
    | rcr dword [rax + 1 * rcx - 0x00000001], cl | d3 9c 08 ff ff ff ff    |
    | rcr dword [rax + 1 * rcx + 0x7f], cl       | d3 5c 08 7f             |
    | rcr dword [rax + 1 * rcx - 0x7f], cl       | d3 5c 08 81             |
    | rcr dword [rax + 1 * rcx + 0x80], cl       | d3 9c 08 80 00 00 00    |
    | rcr dword [rax + 1 * rcx - 0x80], cl       | d3 5c 08 80             |
    | rcr dword [rax + 1 * rcx - 0x81], cl       | d3 9c 08 7f ff ff ff    |
    | rcr dword [rax + 1 * rcx + 0xff], cl       | d3 9c 08 ff 00 00 00    |
    | rcr dword [rax + 1 * rcx - 0xff], cl       | d3 9c 08 01 ff ff ff    |
    | rcr dword [rax + 1 * rcx + 0x7fffffff], cl | d3 9c 08 ff ff ff 7f    |
    | rcr dword [rax + 1 * rcx - 0x7fffffff], cl | d3 9c 08 01 00 00 80    |
    | rcr dword [rax + 1 * rcx - 0x80000000], cl | d3 9c 08 00 00 00 80    |
    | rcr dword [r10 + 0x7f], cl                 | 41 d3 5a 7f             |
    | rcr dword [r10 + 0x80], cl                 | 41 d3 9a 80 00 00 00    |
    | rcr dword [r10 - 0x80], cl                 | 41 d3 5a 80             |
    | rcr dword [r10 - 0x81], cl                 | 41 d3 9a 7f ff ff ff    |
    | ------------------------------------------ | ----------------------- |
"""


def can_encode_rcr_addr32_cl():
    encode(RCR_ADDR32_CL)


RCR_ADDR16_IMM8 = """
    | ------------------------------------------- | ----------------------------- |
    | instruction                                 | encoding                      |
    | ------------------------------------------- | ----------------------------- |
    | rcr word [rax], 0x01                        | 66 d1 18                      |
    | rcr word [rcx], 0x01                        | 66 d1 19                      |
    | rcr word [rdx], 0x01                        | 66 d1 1a                      |
    | rcr word [rbx], 0x01                        | 66 d1 1b                      |
    | rcr word [rsp], 0x01                        | 66 d1 1c 24                   |
    | rcr word [rbp], 0x01                        | 66 d1 5d 00                   |
    | rcr word [rsi], 0x01                        | 66 d1 1e                      |
    | rcr word [rdi], 0x01                        | 66 d1 1f                      |
    | rcr word [r8], 0x01                         | 66 41 d1 18                   |
    | rcr word [r9], 0x01                         | 66 41 d1 19                   |
    | rcr word [r10], 0x01                        | 66 41 d1 1a                   |
    | rcr word [r11], 0x01                        | 66 41 d1 1b                   |
    | rcr word [r12], 0x01                        | 66 41 d1 1c 24                |
    | rcr word [r13], 0x01                        | 66 41 d1 5d 00                |
    | rcr word [r14], 0x01                        | 66 41 d1 1e                   |
    | rcr word [r15], 0x01                        | 66 41 d1 1f                   |
    | rcr word [rax + 1 * rcx], 0x01              | 66 d1 1c 08                   |
    | rcr word [rcx + 1 * rcx], 0x01              | 66 d1 1c 09                   |
    | rcr word [rdx + 1 * rcx], 0x01              | 66 d1 1c 0a                   |
    | rcr word [rbx + 1 * rcx], 0x01              | 66 d1 1c 0b                   |
    | rcr word [rsp + 1 * rcx], 0x01              | 66 d1 1c 0c                   |
    | rcr word [rbp + 1 * rcx], 0x01              | 66 d1 5c 0d 00                |
    | rcr word [rsi + 1 * rcx], 0x01              | 66 d1 1c 0e                   |
    | rcr word [rdi + 1 * rcx], 0x01              | 66 d1 1c 0f                   |
    | rcr word [r8 + 1 * rcx], 0x01               | 66 41 d1 1c 08                |
    | rcr word [r9 + 1 * rcx], 0x01               | 66 41 d1 1c 09                |
    | rcr word [r10 + 1 * rcx], 0x01              | 66 41 d1 1c 0a                |
    | rcr word [r11 + 1 * rcx], 0x01              | 66 41 d1 1c 0b                |
    | rcr word [r12 + 1 * rcx], 0x01              | 66 41 d1 1c 0c                |
    | rcr word [r13 + 1 * rcx], 0x01              | 66 41 d1 5c 0d 00             |
    | rcr word [r14 + 1 * rcx], 0x01              | 66 41 d1 1c 0e                |
    | rcr word [r15 + 1 * rcx], 0x01              | 66 41 d1 1c 0f                |
    | rcr word [rax + 1 * rax], 0x01              | 66 d1 1c 00                   |
    | rcr word [rax + 1 * rdx], 0x01              | 66 d1 1c 10                   |
    | rcr word [rax + 1 * rbx], 0x01              | 66 d1 1c 18                   |
    | rcr word [rax + 1 * rbp], 0x01              | 66 d1 1c 28                   |
    | rcr word [rax + 1 * rsi], 0x01              | 66 d1 1c 30                   |
    | rcr word [rax + 1 * rdi], 0x01              | 66 d1 1c 38                   |
    | rcr word [rax + 1 * r8], 0x01               | 66 42 d1 1c 00                |
    | rcr word [rax + 1 * r9], 0x01               | 66 42 d1 1c 08                |
    | rcr word [rax + 1 * r10], 0x01              | 66 42 d1 1c 10                |
    | rcr word [rax + 1 * r11], 0x01              | 66 42 d1 1c 18                |
    | rcr word [rax + 1 * r12], 0x01              | 66 42 d1 1c 20                |
    | rcr word [rax + 1 * r13], 0x01              | 66 42 d1 1c 28                |
    | rcr word [rax + 1 * r14], 0x01              | 66 42 d1 1c 30                |
    | rcr word [rax + 1 * r15], 0x01              | 66 42 d1 1c 38                |
    | rcr word [rax + 2 * rcx], 0x01              | 66 d1 1c 48                   |
    | rcr word [rax + 4 * rcx], 0x01              | 66 d1 1c 88                   |
    | rcr word [rax + 8 * rcx], 0x01              | 66 d1 1c c8                   |
    | rcr word [r8 + 1 * r9], 0x01                | 66 43 d1 1c 08                |
    | rcr word [r8 + 2 * r9], 0x01                | 66 43 d1 1c 48                |
    | rcr word [r8 + 4 * r9], 0x01                | 66 43 d1 1c 88                |
    | rcr word [r8 + 8 * r9], 0x01                | 66 43 d1 1c c8                |
    | rcr word [1 * rcx], 0x01                    | 66 d1 1c 0d 00 00 00 00       |
    | rcr word [2 * rcx], 0x01                    | 66 d1 1c 4d 00 00 00 00       |
    | rcr word [4 * rcx], 0x01                    | 66 d1 1c 8d 00 00 00 00       |
    | rcr word [8 * rcx], 0x01                    | 66 d1 1c cd 00 00 00 00       |
    | rcr word [1 * r9], 0x01                     | 66 42 d1 1c 0d 00 00 00 00    |
    | rcr word [2 * r9], 0x01                     | 66 42 d1 1c 4d 00 00 00 00    |
    | rcr word [4 * r9], 0x01                     | 66 42 d1 1c 8d 00 00 00 00    |
    | rcr word [8 * r9], 0x01                     | 66 42 d1 1c cd 00 00 00 00    |
    | rcr word [r13 + 8 * r12], 0x01              | 66 43 d1 5c e5 00             |
    | rcr word [rsp + 4 * r15], 0x01              | 66 42 d1 1c bc                |
    | rcr word [rax + 1 * rcx + 0x00], 0x01       | 66 d1 5c 08 00                |
    | rcr word [rax + 1 * rcx - 0x00], 0x01       | 66 d1 5c 08 00                |
    | rcr word [rax + 1 * rcx + 0x01], 0x01       | 66 d1 5c 08 01                |
    | rcr word [rax + 1 * rcx - 0x01], 0x01       | 66 d1 5c 08 ff                |
    | rcr word [rax + 1 * rcx + 0x00000001], 0x01 | 66 d1 9c 08 01 00 00 00       |
    | rcr word [rax + 1 * rcx - 0x00000001], 0x01 | 66 d1 9c 08 ff ff ff ff       |
    | rcr word [rax + 1 * rcx + 0x7f], 0x01       | 66 d1 5c 08 7f                |
    | rcr word [rax + 1 * rcx - 0x7f], 0x01       | 66 d1 5c 08 81                |
    | rcr word [rax + 1 * rcx + 0x80], 0x01       | 66 d1 9c 08 80 00 00 00       |
    | rcr word [rax + 1 * rcx - 0x80], 0x01       | 66 d1 5c 08 80                |
    | rcr word [rax + 1 * rcx - 0x81], 0x01       | 66 d1 9c 08 7f ff ff ff       |
    | rcr word [rax + 1 * rcx + 0xff], 0x01       | 66 d1 9c 08 ff 00 00 00       |
    | rcr word [rax + 1 * rcx - 0xff], 0x01       | 66 d1 9c 08 01 ff ff ff       |
    | rcr word [rax + 1 * rcx + 0x7fffffff], 0x01 | 66 d1 9c 08 ff ff ff 7f       |
    | rcr word [rax + 1 * rcx - 0x7fffffff], 0x01 | 66 d1 9c 08 01 00 00 80       |
    | rcr word [rax + 1 * rcx - 0x80000000], 0x01 | 66 d1 9c 08 00 00 00 80       |
    | rcr word [r10 + 0x7f], 0x01                 | 66 41 d1 5a 7f                |
    | rcr word [r10 + 0x80], 0x01                 | 66 41 d1 9a 80 00 00 00       |
    | rcr word [r10 - 0x80], 0x01                 | 66 41 d1 5a 80                |
    | rcr word [r10 - 0x81], 0x01                 | 66 41 d1 9a 7f ff ff ff       |
    | rcr word [rax], 0x00                        | 66 c1 18 00                   |
    | rcr word [rax], 0x7f                        | 66 c1 18 7f                   |
    | rcr word [rax], 0x80                        | 66 c1 18 80                   |
    | rcr word [rax], 0xff                        | 66 c1 18 ff                   |
    | rcr word [rcx], 0x7f                        | 66 c1 19 7f                   |
    | rcr word [rdx], 0x80                        | 66 c1 1a 80                   |
    | rcr word [rbx], 0xff                        | 66 c1 1b ff                   |
    | rcr word [rsp], 0x00                        | 66 c1 1c 24 00                |
    | rcr word [rsi], 0x7f                        | 66 c1 1e 7f                   |
    | rcr word [rdi], 0x80                        | 66 c1 1f 80                   |
    | rcr word [r8], 0xff                         | 66 41 c1 18 ff                |
    | rcr word [r9], 0x00                         | 66 41 c1 19 00                |
    | rcr word [r11], 0x7f                        | 66 41 c1 1b 7f                |
    | rcr word [r12], 0x80                        | 66 41 c1 1c 24 80             |
    | rcr word [r13], 0xff                        | 66 41 c1 5d 00 ff             |
    | rcr word [r14], 0x00                        | 66 41 c1 1e 00                |
    | rcr word [rax + 1 * rcx], 0x7f              | 66 c1 1c 08 7f                |
    | rcr word [rcx + 1 * rcx], 0x80              | 66 c1 1c 09 80                |
    | rcr word [rdx + 1 * rcx], 0xff              | 66 c1 1c 0a ff                |
    | rcr word [rbx + 1 * rcx], 0x00              | 66 c1 1c 0b 00                |
    | rcr word [rbp + 1 * rcx], 0x7f              | 66 c1 5c 0d 00 7f             |
    | rcr word [rsi + 1 * rcx], 0x80              | 66 c1 1c 0e 80                |
    | rcr word [rdi + 1 * rcx], 0xff              | 66 c1 1c 0f ff                |
    | rcr word [r8 + 1 * rcx], 0x00               | 66 41 c1 1c 08 00             |
    | rcr word [r10 + 1 * rcx], 0x7f              | 66 41 c1 1c 0a 7f             |
    | rcr word [r11 + 1 * rcx], 0x80              | 66 41 c1 1c 0b 80             |
    | rcr word [r12 + 1 * rcx], 0xff              | 66 41 c1 1c 0c ff             |
    | rcr word [r13 + 1 * rcx], 0x00              | 66 41 c1 5c 0d 00 00          |
    | rcr word [r15 + 1 * rcx], 0x7f              | 66 41 c1 1c 0f 7f             |
    | rcr word [rax + 1 * rax], 0x80              | 66 c1 1c 00 80                |
    | rcr word [rax + 1 * rdx], 0xff              | 66 c1 1c 10 ff                |
    | rcr word [rax + 1 * rbx], 0x00              | 66 c1 1c 18 00                |
    | rcr word [rax + 1 * rsi], 0x7f              | 66 c1 1c 30 7f                |
    | rcr word [rax + 1 * rdi], 0x80              | 66 c1 1c 38 80                |
    | rcr word [rax + 1 * r8], 0xff               | 66 42 c1 1c 00 ff             |
    | rcr word [rax + 1 * r9], 0x00               | 66 42 c1 1c 08 00             |
    | rcr word [rax + 1 * r11], 0x7f              | 66 42 c1 1c 18 7f             |
    | rcr word [rax + 1 * r12], 0x80              | 66 42 c1 1c 20 80             |
    | rcr word [rax + 1 * r13], 0xff              | 66 42 c1 1c 28 ff             |
    | rcr word [rax + 1 * r14], 0x00              | 66 42 c1 1c 30 00             |
    | rcr word [rax + 2 * rcx], 0x7f              | 66 c1 1c 48 7f                |
    | rcr word [rax + 4 * rcx], 0x80              | 66 c1 1c 88 80                |
    | rcr word [rax + 8 * rcx], 0xff              | 66 c1 1c c8 ff                |
    | rcr word [r8 + 1 * r9], 0x00                | 66 43 c1 1c 08 00             |
    | rcr word [r8 + 4 * r9], 0x7f                | 66 43 c1 1c 88 7f             |
    | rcr word [r8 + 8 * r9], 0x80                | 66 43 c1 1c c8 80             |
    | rcr word [1 * rcx], 0xff                    | 66 c1 1c 0d 00 00 00 00 ff    |
    | rcr word [2 * rcx], 0x00                    | 66 c1 1c 4d 00 00 00 00 00    |
    | rcr word [8 * rcx], 0x7f                    | 66 c1 1c cd 00 00 00 00 7f    |
    | rcr word [1 * r9], 0x80                     | 66 42 c1 1c 0d 00 00 00 00 80 |
    | rcr word [2 * r9], 0xff                     | 66 42 c1 1c 4d 00 00 00 00 ff |
    | rcr word [4 * r9], 0x00                     | 66 42 c1 1c 8d 00 00 00 00 00 |
    | rcr word [r13 + 8 * r12], 0x7f              | 66 43 c1 5c e5 00 7f          |
    | rcr word [rsp + 4 * r15], 0x80              | 66 42 c1 1c bc 80             |
    | rcr word [rax + 1 * rcx + 0x00], 0xff       | 66 c1 5c 08 00 ff             |
    | rcr word [rax + 1 * rcx - 0x00], 0x00       | 66 c1 5c 08 00 00             |
    | rcr word [rax + 1 * rcx - 0x01], 0x7f       | 66 c1 5c 08 ff 7f             |
    | rcr word [rax + 1 * rcx + 0x00000001], 0x80 | 66 c1 9c 08 01 00 00 00 80    |
    | rcr word [rax + 1 * rcx - 0x00000001], 0xff | 66 c1 9c 08 ff ff ff ff ff    |
    | rcr word [rax + 1 * rcx + 0x7f], 0x00       | 66 c1 5c 08 7f 00             |
    | rcr word [rax + 1 * rcx + 0x80], 0x7f       | 66 c1 9c 08 80 00 00 00 7f    |
    | rcr word [rax + 1 * rcx - 0x80], 0x80       | 66 c1 5c 08 80 80             |
    | rcr word [rax + 1 * rcx - 0x81], 0xff       | 66 c1 9c 08 7f ff ff ff ff    |
    | rcr word [rax + 1 * rcx + 0xff], 0x00       | 66 c1 9c 08 ff 00 00 00 00    |
    | rcr word [rax + 1 * rcx + 0x7fffffff], 0x7f | 66 c1 9c 08 ff ff ff 7f 7f    |
    | rcr word [rax + 1 * rcx - 0x7fffffff], 0x80 | 66 c1 9c 08 01 00 00 80 80    |
    | rcr word [rax + 1 * rcx - 0x80000000], 0xff | 66 c1 9c 08 00 00 00 80 ff    |
    | rcr word [r10 + 0x7f], 0x00                 | 66 41 c1 5a 7f 00             |
    | rcr word [r10 - 0x80], 0x7f                 | 66 41 c1 5a 80 7f             |
    | rcr word [r10 - 0x81], 0x80                 | 66 41 c1 9a 7f ff ff ff 80    |
    | ------------------------------------------- | ----------------------------- |
"""


def can_encode_rcr_addr16_imm8():
    encode(RCR_ADDR16_IMM8)


RCR_ADDR16_CL = """
    | ----------------------------------------- | -------------------------- |
    | instruction                               | encoding                   |
    | ----------------------------------------- | -------------------------- |
    | rcr word [rax], cl                        | 66 d3 18                   |
    | rcr word [rcx], cl                        | 66 d3 19                   |
    | rcr word [rdx], cl                        | 66 d3 1a                   |
    | rcr word [rbx], cl                        | 66 d3 1b                   |
    | rcr word [rsp], cl                        | 66 d3 1c 24                |
    | rcr word [rbp], cl                        | 66 d3 5d 00                |
    | rcr word [rsi], cl                        | 66 d3 1e                   |
    | rcr word [rdi], cl                        | 66 d3 1f                   |
    | rcr word [r8], cl                         | 66 41 d3 18                |
    | rcr word [r9], cl                         | 66 41 d3 19                |
    | rcr word [r10], cl                        | 66 41 d3 1a                |
    | rcr word [r11], cl                        | 66 41 d3 1b                |
    | rcr word [r12], cl                        | 66 41 d3 1c 24             |
    | rcr word [r13], cl                        | 66 41 d3 5d 00             |
    | rcr word [r14], cl                        | 66 41 d3 1e                |
    | rcr word [r15], cl                        | 66 41 d3 1f                |
    | rcr word [rax + 1 * rcx], cl              | 66 d3 1c 08                |
    | rcr word [rcx + 1 * rcx], cl              | 66 d3 1c 09                |
    | rcr word [rdx + 1 * rcx], cl              | 66 d3 1c 0a                |
    | rcr word [rbx + 1 * rcx], cl              | 66 d3 1c 0b                |
    | rcr word [rsp + 1 * rcx], cl              | 66 d3 1c 0c                |
    | rcr word [rbp + 1 * rcx], cl              | 66 d3 5c 0d 00             |
    | rcr word [rsi + 1 * rcx], cl              | 66 d3 1c 0e                |
    | rcr word [rdi + 1 * rcx], cl              | 66 d3 1c 0f                |
    | rcr word [r8 + 1 * rcx], cl               | 66 41 d3 1c 08             |
    | rcr word [r9 + 1 * rcx], cl               | 66 41 d3 1c 09             |
    | rcr word [r10 + 1 * rcx], cl              | 66 41 d3 1c 0a             |
    | rcr word [r11 + 1 * rcx], cl              | 66 41 d3 1c 0b             |
    | rcr word [r12 + 1 * rcx], cl              | 66 41 d3 1c 0c             |
    | rcr word [r13 + 1 * rcx], cl              | 66 41 d3 5c 0d 00          |
    | rcr word [r14 + 1 * rcx], cl              | 66 41 d3 1c 0e             |
    | rcr word [r15 + 1 * rcx], cl              | 66 41 d3 1c 0f             |
    | rcr word [rax + 1 * rax], cl              | 66 d3 1c 00                |
    | rcr word [rax + 1 * rdx], cl              | 66 d3 1c 10                |
    | rcr word [rax + 1 * rbx], cl              | 66 d3 1c 18                |
    | rcr word [rax + 1 * rbp], cl              | 66 d3 1c 28                |
    | rcr word [rax + 1 * rsi], cl              | 66 d3 1c 30                |
    | rcr word [rax + 1 * rdi], cl              | 66 d3 1c 38                |
    | rcr word [rax + 1 * r8], cl               | 66 42 d3 1c 00             |
    | rcr word [rax + 1 * r9], cl               | 66 42 d3 1c 08             |
    | rcr word [rax + 1 * r10], cl              | 66 42 d3 1c 10             |
    | rcr word [rax + 1 * r11], cl              | 66 42 d3 1c 18             |
    | rcr word [rax + 1 * r12], cl              | 66 42 d3 1c 20             |
    | rcr word [rax + 1 * r13], cl              | 66 42 d3 1c 28             |
    | rcr word [rax + 1 * r14], cl              | 66 42 d3 1c 30             |
    | rcr word [rax + 1 * r15], cl              | 66 42 d3 1c 38             |
    | rcr word [rax + 2 * rcx], cl              | 66 d3 1c 48                |
    | rcr word [rax + 4 * rcx], cl              | 66 d3 1c 88                |
    | rcr word [rax + 8 * rcx], cl              | 66 d3 1c c8                |
    | rcr word [r8 + 1 * r9], cl                | 66 43 d3 1c 08             |
    | rcr word [r8 + 2 * r9], cl                | 66 43 d3 1c 48             |
    | rcr word [r8 + 4 * r9], cl                | 66 43 d3 1c 88             |
    | rcr word [r8 + 8 * r9], cl                | 66 43 d3 1c c8             |
    | rcr word [1 * rcx], cl                    | 66 d3 1c 0d 00 00 00 00    |
    | rcr word [2 * rcx], cl                    | 66 d3 1c 4d 00 00 00 00    |
    | rcr word [4 * rcx], cl                    | 66 d3 1c 8d 00 00 00 00    |
    | rcr word [8 * rcx], cl                    | 66 d3 1c cd 00 00 00 00    |
    | rcr word [1 * r9], cl                     | 66 42 d3 1c 0d 00 00 00 00 |
    | rcr word [2 * r9], cl                     | 66 42 d3 1c 4d 00 00 00 00 |
    | rcr word [4 * r9], cl                     | 66 42 d3 1c 8d 00 00 00 00 |
    | rcr word [8 * r9], cl                     | 66 42 d3 1c cd 00 00 00 00 |
    | rcr word [r13 + 8 * r12], cl              | 66 43 d3 5c e5 00          |
    | rcr word [rsp + 4 * r15], cl              | 66 42 d3 1c bc             |
    | rcr word [rax + 1 * rcx + 0x00], cl       | 66 d3 5c 08 00             |
    | rcr word [rax + 1 * rcx - 0x00], cl       | 66 d3 5c 08 00             |
    | rcr word [rax + 1 * rcx + 0x01], cl       | 66 d3 5c 08 01             |
    | rcr word [rax + 1 * rcx - 0x01], cl       | 66 d3 5c 08 ff             |
    | rcr word [rax + 1 * rcx + 0x00000001], cl | 66 d3 9c 08 01 00 00 00    |
    | rcr word [rax + 1 * rcx - 0x00000001], cl | 66 d3 9c 08 ff ff ff ff    |
    | rcr word [rax + 1 * rcx + 0x7f], cl       | 66 d3 5c 08 7f             |
    | rcr word [rax + 1 * rcx - 0x7f], cl       | 66 d3 5c 08 81             |
    | rcr word [rax + 1 * rcx + 0x80], cl       | 66 d3 9c 08 80 00 00 00    |
    | rcr word [rax + 1 * rcx - 0x80], cl       | 66 d3 5c 08 80             |
    | rcr word [rax + 1 * rcx - 0x81], cl       | 66 d3 9c 08 7f ff ff ff    |
    | rcr word [rax + 1 * rcx + 0xff], cl       | 66 d3 9c 08 ff 00 00 00    |
    | rcr word [rax + 1 * rcx - 0xff], cl       | 66 d3 9c 08 01 ff ff ff    |
    | rcr word [rax + 1 * rcx + 0x7fffffff], cl | 66 d3 9c 08 ff ff ff 7f    |
    | rcr word [rax + 1 * rcx - 0x7fffffff], cl | 66 d3 9c 08 01 00 00 80    |
    | rcr word [rax + 1 * rcx - 0x80000000], cl | 66 d3 9c 08 00 00 00 80    |
    | rcr word [r10 + 0x7f], cl                 | 66 41 d3 5a 7f             |
    | rcr word [r10 + 0x80], cl                 | 66 41 d3 9a 80 00 00 00    |
    | rcr word [r10 - 0x80], cl                 | 66 41 d3 5a 80             |
    | rcr word [r10 - 0x81], cl                 | 66 41 d3 9a 7f ff ff ff    |
    | ----------------------------------------- | -------------------------- |
"""


def can_encode_rcr_addr16_cl():
    encode(RCR_ADDR16_CL)


RCR_ADDR8_IMM8 = """
    | ------------------------------------------- | -------------------------- |
    | instruction                                 | encoding                   |
    | ------------------------------------------- | -------------------------- |
    | rcr byte [rax], 0x01                        | d0 18                      |
    | rcr byte [rcx], 0x01                        | d0 19                      |
    | rcr byte [rdx], 0x01                        | d0 1a                      |
    | rcr byte [rbx], 0x01                        | d0 1b                      |
    | rcr byte [rsp], 0x01                        | d0 1c 24                   |
    | rcr byte [rbp], 0x01                        | d0 5d 00                   |
    | rcr byte [rsi], 0x01                        | d0 1e                      |
    | rcr byte [rdi], 0x01                        | d0 1f                      |
    | rcr byte [r8], 0x01                         | 41 d0 18                   |
    | rcr byte [r9], 0x01                         | 41 d0 19                   |
    | rcr byte [r10], 0x01                        | 41 d0 1a                   |
    | rcr byte [r11], 0x01                        | 41 d0 1b                   |
    | rcr byte [r12], 0x01                        | 41 d0 1c 24                |
    | rcr byte [r13], 0x01                        | 41 d0 5d 00                |
    | rcr byte [r14], 0x01                        | 41 d0 1e                   |
    | rcr byte [r15], 0x01                        | 41 d0 1f                   |
    | rcr byte [rax + 1 * rcx], 0x01              | d0 1c 08                   |
    | rcr byte [rcx + 1 * rcx], 0x01              | d0 1c 09                   |
    | rcr byte [rdx + 1 * rcx], 0x01              | d0 1c 0a                   |
    | rcr byte [rbx + 1 * rcx], 0x01              | d0 1c 0b                   |
    | rcr byte [rsp + 1 * rcx], 0x01              | d0 1c 0c                   |
    | rcr byte [rbp + 1 * rcx], 0x01              | d0 5c 0d 00                |
    | rcr byte [rsi + 1 * rcx], 0x01              | d0 1c 0e                   |
    | rcr byte [rdi + 1 * rcx], 0x01              | d0 1c 0f                   |
    | rcr byte [r8 + 1 * rcx], 0x01               | 41 d0 1c 08                |
    | rcr byte [r9 + 1 * rcx], 0x01               | 41 d0 1c 09                |
    | rcr byte [r10 + 1 * rcx], 0x01              | 41 d0 1c 0a                |
    | rcr byte [r11 + 1 * rcx], 0x01              | 41 d0 1c 0b                |
    | rcr byte [r12 + 1 * rcx], 0x01              | 41 d0 1c 0c                |
    | rcr byte [r13 + 1 * rcx], 0x01              | 41 d0 5c 0d 00             |
    | rcr byte [r14 + 1 * rcx], 0x01              | 41 d0 1c 0e                |
    | rcr byte [r15 + 1 * rcx], 0x01              | 41 d0 1c 0f                |
    | rcr byte [rax + 1 * rax], 0x01              | d0 1c 00                   |
    | rcr byte [rax + 1 * rdx], 0x01              | d0 1c 10                   |
    | rcr byte [rax + 1 * rbx], 0x01              | d0 1c 18                   |
    | rcr byte [rax + 1 * rbp], 0x01              | d0 1c 28                   |
    | rcr byte [rax + 1 * rsi], 0x01              | d0 1c 30                   |
    | rcr byte [rax + 1 * rdi], 0x01              | d0 1c 38                   |
    | rcr byte [rax + 1 * r8], 0x01               | 42 d0 1c 00                |
    | rcr byte [rax + 1 * r9], 0x01               | 42 d0 1c 08                |
    | rcr byte [rax + 1 * r10], 0x01              | 42 d0 1c 10                |
    | rcr byte [rax + 1 * r11], 0x01              | 42 d0 1c 18                |
    | rcr byte [rax + 1 * r12], 0x01              | 42 d0 1c 20                |
    | rcr byte [rax + 1 * r13], 0x01              | 42 d0 1c 28                |
    | rcr byte [rax + 1 * r14], 0x01              | 42 d0 1c 30                |
    | rcr byte [rax + 1 * r15], 0x01              | 42 d0 1c 38                |
    | rcr byte [rax + 2 * rcx], 0x01              | d0 1c 48                   |
    | rcr byte [rax + 4 * rcx], 0x01              | d0 1c 88                   |
    | rcr byte [rax + 8 * rcx], 0x01              | d0 1c c8                   |
    | rcr byte [r8 + 1 * r9], 0x01                | 43 d0 1c 08                |
    | rcr byte [r8 + 2 * r9], 0x01                | 43 d0 1c 48                |
    | rcr byte [r8 + 4 * r9], 0x01                | 43 d0 1c 88                |
    | rcr byte [r8 + 8 * r9], 0x01                | 43 d0 1c c8                |
    | rcr byte [1 * rcx], 0x01                    | d0 1c 0d 00 00 00 00       |
    | rcr byte [2 * rcx], 0x01                    | d0 1c 4d 00 00 00 00       |
    | rcr byte [4 * rcx], 0x01                    | d0 1c 8d 00 00 00 00       |
    | rcr byte [8 * rcx], 0x01                    | d0 1c cd 00 00 00 00       |
    | rcr byte [1 * r9], 0x01                     | 42 d0 1c 0d 00 00 00 00    |
    | rcr byte [2 * r9], 0x01                     | 42 d0 1c 4d 00 00 00 00    |
    | rcr byte [4 * r9], 0x01                     | 42 d0 1c 8d 00 00 00 00    |
    | rcr byte [8 * r9], 0x01                     | 42 d0 1c cd 00 00 00 00    |
    | rcr byte [r13 + 8 * r12], 0x01              | 43 d0 5c e5 00             |
    | rcr byte [rsp + 4 * r15], 0x01              | 42 d0 1c bc                |
    | rcr byte [rax + 1 * rcx + 0x00], 0x01       | d0 5c 08 00                |
    | rcr byte [rax + 1 * rcx - 0x00], 0x01       | d0 5c 08 00                |
    | rcr byte [rax + 1 * rcx + 0x01], 0x01       | d0 5c 08 01                |
    | rcr byte [rax + 1 * rcx - 0x01], 0x01       | d0 5c 08 ff                |
    | rcr byte [rax + 1 * rcx + 0x00000001], 0x01 | d0 9c 08 01 00 00 00       |
    | rcr byte [rax + 1 * rcx - 0x00000001], 0x01 | d0 9c 08 ff ff ff ff       |
    | rcr byte [rax + 1 * rcx + 0x7f], 0x01       | d0 5c 08 7f                |
    | rcr byte [rax + 1 * rcx - 0x7f], 0x01       | d0 5c 08 81                |
    | rcr byte [rax + 1 * rcx + 0x80], 0x01       | d0 9c 08 80 00 00 00       |
    | rcr byte [rax + 1 * rcx - 0x80], 0x01       | d0 5c 08 80                |
    | rcr byte [rax + 1 * rcx - 0x81], 0x01       | d0 9c 08 7f ff ff ff       |
    | rcr byte [rax + 1 * rcx + 0xff], 0x01       | d0 9c 08 ff 00 00 00       |
    | rcr byte [rax + 1 * rcx - 0xff], 0x01       | d0 9c 08 01 ff ff ff       |
    | rcr byte [rax + 1 * rcx + 0x7fffffff], 0x01 | d0 9c 08 ff ff ff 7f       |
    | rcr byte [rax + 1 * rcx - 0x7fffffff], 0x01 | d0 9c 08 01 00 00 80       |
    | rcr byte [rax + 1 * rcx - 0x80000000], 0x01 | d0 9c 08 00 00 00 80       |
    | rcr byte [r10 + 0x7f], 0x01                 | 41 d0 5a 7f                |
    | rcr byte [r10 + 0x80], 0x01                 | 41 d0 9a 80 00 00 00       |
    | rcr byte [r10 - 0x80], 0x01                 | 41 d0 5a 80                |
    | rcr byte [r10 - 0x81], 0x01                 | 41 d0 9a 7f ff ff ff       |
    | rcr byte [rax], 0x00                        | c0 18 00                   |
    | rcr byte [rax], 0x7f                        | c0 18 7f                   |
    | rcr byte [rax], 0x80                        | c0 18 80                   |
    | rcr byte [rax], 0xff                        | c0 18 ff                   |
    | rcr byte [rcx], 0x7f                        | c0 19 7f                   |
    | rcr byte [rdx], 0x80                        | c0 1a 80                   |
    | rcr byte [rbx], 0xff                        | c0 1b ff                   |
    | rcr byte [rsp], 0x00                        | c0 1c 24 00                |
    | rcr byte [rsi], 0x7f                        | c0 1e 7f                   |
    | rcr byte [rdi], 0x80                        | c0 1f 80                   |
    | rcr byte [r8], 0xff                         | 41 c0 18 ff                |
    | rcr byte [r9], 0x00                         | 41 c0 19 00                |
    | rcr byte [r11], 0x7f                        | 41 c0 1b 7f                |
    | rcr byte [r12], 0x80                        | 41 c0 1c 24 80             |
    | rcr byte [r13], 0xff                        | 41 c0 5d 00 ff             |
    | rcr byte [r14], 0x00                        | 41 c0 1e 00                |
    | rcr byte [rax + 1 * rcx], 0x7f              | c0 1c 08 7f                |
    | rcr byte [rcx + 1 * rcx], 0x80              | c0 1c 09 80                |
    | rcr byte [rdx + 1 * rcx], 0xff              | c0 1c 0a ff                |
    | rcr byte [rbx + 1 * rcx], 0x00              | c0 1c 0b 00                |
    | rcr byte [rbp + 1 * rcx], 0x7f              | c0 5c 0d 00 7f             |
    | rcr byte [rsi + 1 * rcx], 0x80              | c0 1c 0e 80                |
    | rcr byte [rdi + 1 * rcx], 0xff              | c0 1c 0f ff                |
    | rcr byte [r8 + 1 * rcx], 0x00               | 41 c0 1c 08 00             |
    | rcr byte [r10 + 1 * rcx], 0x7f              | 41 c0 1c 0a 7f             |
    | rcr byte [r11 + 1 * rcx], 0x80              | 41 c0 1c 0b 80             |
    | rcr byte [r12 + 1 * rcx], 0xff              | 41 c0 1c 0c ff             |
    | rcr byte [r13 + 1 * rcx], 0x00              | 41 c0 5c 0d 00 00          |
    | rcr byte [r15 + 1 * rcx], 0x7f              | 41 c0 1c 0f 7f             |
    | rcr byte [rax + 1 * rax], 0x80              | c0 1c 00 80                |
    | rcr byte [rax + 1 * rdx], 0xff              | c0 1c 10 ff                |
    | rcr byte [rax + 1 * rbx], 0x00              | c0 1c 18 00                |
    | rcr byte [rax + 1 * rsi], 0x7f              | c0 1c 30 7f                |
    | rcr byte [rax + 1 * rdi], 0x80              | c0 1c 38 80                |
    | rcr byte [rax + 1 * r8], 0xff               | 42 c0 1c 00 ff             |
    | rcr byte [rax + 1 * r9], 0x00               | 42 c0 1c 08 00             |
    | rcr byte [rax + 1 * r11], 0x7f              | 42 c0 1c 18 7f             |
    | rcr byte [rax + 1 * r12], 0x80              | 42 c0 1c 20 80             |
    | rcr byte [rax + 1 * r13], 0xff              | 42 c0 1c 28 ff             |
    | rcr byte [rax + 1 * r14], 0x00              | 42 c0 1c 30 00             |
    | rcr byte [rax + 2 * rcx], 0x7f              | c0 1c 48 7f                |
    | rcr byte [rax + 4 * rcx], 0x80              | c0 1c 88 80                |
    | rcr byte [rax + 8 * rcx], 0xff              | c0 1c c8 ff                |
    | rcr byte [r8 + 1 * r9], 0x00                | 43 c0 1c 08 00             |
    | rcr byte [r8 + 4 * r9], 0x7f                | 43 c0 1c 88 7f             |
    | rcr byte [r8 + 8 * r9], 0x80                | 43 c0 1c c8 80             |
    | rcr byte [1 * rcx], 0xff                    | c0 1c 0d 00 00 00 00 ff    |
    | rcr byte [2 * rcx], 0x00                    | c0 1c 4d 00 00 00 00 00    |
    | rcr byte [8 * rcx], 0x7f                    | c0 1c cd 00 00 00 00 7f    |
    | rcr byte [1 * r9], 0x80                     | 42 c0 1c 0d 00 00 00 00 80 |
    | rcr byte [2 * r9], 0xff                     | 42 c0 1c 4d 00 00 00 00 ff |
    | rcr byte [4 * r9], 0x00                     | 42 c0 1c 8d 00 00 00 00 00 |
    | rcr byte [r13 + 8 * r12], 0x7f              | 43 c0 5c e5 00 7f          |
    | rcr byte [rsp + 4 * r15], 0x80              | 42 c0 1c bc 80             |
    | rcr byte [rax + 1 * rcx + 0x00], 0xff       | c0 5c 08 00 ff             |
    | rcr byte [rax + 1 * rcx - 0x00], 0x00       | c0 5c 08 00 00             |
    | rcr byte [rax + 1 * rcx - 0x01], 0x7f       | c0 5c 08 ff 7f             |
    | rcr byte [rax + 1 * rcx + 0x00000001], 0x80 | c0 9c 08 01 00 00 00 80    |
    | rcr byte [rax + 1 * rcx - 0x00000001], 0xff | c0 9c 08 ff ff ff ff ff    |
    | rcr byte [rax + 1 * rcx + 0x7f], 0x00       | c0 5c 08 7f 00             |
    | rcr byte [rax + 1 * rcx + 0x80], 0x7f       | c0 9c 08 80 00 00 00 7f    |
    | rcr byte [rax + 1 * rcx - 0x80], 0x80       | c0 5c 08 80 80             |
    | rcr byte [rax + 1 * rcx - 0x81], 0xff       | c0 9c 08 7f ff ff ff ff    |
    | rcr byte [rax + 1 * rcx + 0xff], 0x00       | c0 9c 08 ff 00 00 00 00    |
    | rcr byte [rax + 1 * rcx + 0x7fffffff], 0x7f | c0 9c 08 ff ff ff 7f 7f    |
    | rcr byte [rax + 1 * rcx - 0x7fffffff], 0x80 | c0 9c 08 01 00 00 80 80    |
    | rcr byte [rax + 1 * rcx - 0x80000000], 0xff | c0 9c 08 00 00 00 80 ff    |
    | rcr byte [r10 + 0x7f], 0x00                 | 41 c0 5a 7f 00             |
    | rcr byte [r10 - 0x80], 0x7f                 | 41 c0 5a 80 7f             |
    | rcr byte [r10 - 0x81], 0x80                 | 41 c0 9a 7f ff ff ff 80    |
    | ------------------------------------------- | -------------------------- |
"""


def can_encode_rcr_addr8_imm8():
    encode(RCR_ADDR8_IMM8)


RCR_ADDR8_CL = """
    | ----------------------------------------- | ----------------------- |
    | instruction                               | encoding                |
    | ----------------------------------------- | ----------------------- |
    | rcr byte [rax], cl                        | d2 18                   |
    | rcr byte [rcx], cl                        | d2 19                   |
    | rcr byte [rdx], cl                        | d2 1a                   |
    | rcr byte [rbx], cl                        | d2 1b                   |
    | rcr byte [rsp], cl                        | d2 1c 24                |
    | rcr byte [rbp], cl                        | d2 5d 00                |
    | rcr byte [rsi], cl                        | d2 1e                   |
    | rcr byte [rdi], cl                        | d2 1f                   |
    | rcr byte [r8], cl                         | 41 d2 18                |
    | rcr byte [r9], cl                         | 41 d2 19                |
    | rcr byte [r10], cl                        | 41 d2 1a                |
    | rcr byte [r11], cl                        | 41 d2 1b                |
    | rcr byte [r12], cl                        | 41 d2 1c 24             |
    | rcr byte [r13], cl                        | 41 d2 5d 00             |
    | rcr byte [r14], cl                        | 41 d2 1e                |
    | rcr byte [r15], cl                        | 41 d2 1f                |
    | rcr byte [rax + 1 * rcx], cl              | d2 1c 08                |
    | rcr byte [rcx + 1 * rcx], cl              | d2 1c 09                |
    | rcr byte [rdx + 1 * rcx], cl              | d2 1c 0a                |
    | rcr byte [rbx + 1 * rcx], cl              | d2 1c 0b                |
    | rcr byte [rsp + 1 * rcx], cl              | d2 1c 0c                |
    | rcr byte [rbp + 1 * rcx], cl              | d2 5c 0d 00             |
    | rcr byte [rsi + 1 * rcx], cl              | d2 1c 0e                |
    | rcr byte [rdi + 1 * rcx], cl              | d2 1c 0f                |
    | rcr byte [r8 + 1 * rcx], cl               | 41 d2 1c 08             |
    | rcr byte [r9 + 1 * rcx], cl               | 41 d2 1c 09             |
    | rcr byte [r10 + 1 * rcx], cl              | 41 d2 1c 0a             |
    | rcr byte [r11 + 1 * rcx], cl              | 41 d2 1c 0b             |
    | rcr byte [r12 + 1 * rcx], cl              | 41 d2 1c 0c             |
    | rcr byte [r13 + 1 * rcx], cl              | 41 d2 5c 0d 00          |
    | rcr byte [r14 + 1 * rcx], cl              | 41 d2 1c 0e             |
    | rcr byte [r15 + 1 * rcx], cl              | 41 d2 1c 0f             |
    | rcr byte [rax + 1 * rax], cl              | d2 1c 00                |
    | rcr byte [rax + 1 * rdx], cl              | d2 1c 10                |
    | rcr byte [rax + 1 * rbx], cl              | d2 1c 18                |
    | rcr byte [rax + 1 * rbp], cl              | d2 1c 28                |
    | rcr byte [rax + 1 * rsi], cl              | d2 1c 30                |
    | rcr byte [rax + 1 * rdi], cl              | d2 1c 38                |
    | rcr byte [rax + 1 * r8], cl               | 42 d2 1c 00             |
    | rcr byte [rax + 1 * r9], cl               | 42 d2 1c 08             |
    | rcr byte [rax + 1 * r10], cl              | 42 d2 1c 10             |
    | rcr byte [rax + 1 * r11], cl              | 42 d2 1c 18             |
    | rcr byte [rax + 1 * r12], cl              | 42 d2 1c 20             |
    | rcr byte [rax + 1 * r13], cl              | 42 d2 1c 28             |
    | rcr byte [rax + 1 * r14], cl              | 42 d2 1c 30             |
    | rcr byte [rax + 1 * r15], cl              | 42 d2 1c 38             |
    | rcr byte [rax + 2 * rcx], cl              | d2 1c 48                |
    | rcr byte [rax + 4 * rcx], cl              | d2 1c 88                |
    | rcr byte [rax + 8 * rcx], cl              | d2 1c c8                |
    | rcr byte [r8 + 1 * r9], cl                | 43 d2 1c 08             |
    | rcr byte [r8 + 2 * r9], cl                | 43 d2 1c 48             |
    | rcr byte [r8 + 4 * r9], cl                | 43 d2 1c 88             |
    | rcr byte [r8 + 8 * r9], cl                | 43 d2 1c c8             |
    | rcr byte [1 * rcx], cl                    | d2 1c 0d 00 00 00 00    |
    | rcr byte [2 * rcx], cl                    | d2 1c 4d 00 00 00 00    |
    | rcr byte [4 * rcx], cl                    | d2 1c 8d 00 00 00 00    |
    | rcr byte [8 * rcx], cl                    | d2 1c cd 00 00 00 00    |
    | rcr byte [1 * r9], cl                     | 42 d2 1c 0d 00 00 00 00 |
    | rcr byte [2 * r9], cl                     | 42 d2 1c 4d 00 00 00 00 |
    | rcr byte [4 * r9], cl                     | 42 d2 1c 8d 00 00 00 00 |
    | rcr byte [8 * r9], cl                     | 42 d2 1c cd 00 00 00 00 |
    | rcr byte [r13 + 8 * r12], cl              | 43 d2 5c e5 00          |
    | rcr byte [rsp + 4 * r15], cl              | 42 d2 1c bc             |
    | rcr byte [rax + 1 * rcx + 0x00], cl       | d2 5c 08 00             |
    | rcr byte [rax + 1 * rcx - 0x00], cl       | d2 5c 08 00             |
    | rcr byte [rax + 1 * rcx + 0x01], cl       | d2 5c 08 01             |
    | rcr byte [rax + 1 * rcx - 0x01], cl       | d2 5c 08 ff             |
    | rcr byte [rax + 1 * rcx + 0x00000001], cl | d2 9c 08 01 00 00 00    |
    | rcr byte [rax + 1 * rcx - 0x00000001], cl | d2 9c 08 ff ff ff ff    |
    | rcr byte [rax + 1 * rcx + 0x7f], cl       | d2 5c 08 7f             |
    | rcr byte [rax + 1 * rcx - 0x7f], cl       | d2 5c 08 81             |
    | rcr byte [rax + 1 * rcx + 0x80], cl       | d2 9c 08 80 00 00 00    |
    | rcr byte [rax + 1 * rcx - 0x80], cl       | d2 5c 08 80             |
    | rcr byte [rax + 1 * rcx - 0x81], cl       | d2 9c 08 7f ff ff ff    |
    | rcr byte [rax + 1 * rcx + 0xff], cl       | d2 9c 08 ff 00 00 00    |
    | rcr byte [rax + 1 * rcx - 0xff], cl       | d2 9c 08 01 ff ff ff    |
    | rcr byte [rax + 1 * rcx + 0x7fffffff], cl | d2 9c 08 ff ff ff 7f    |
    | rcr byte [rax + 1 * rcx - 0x7fffffff], cl | d2 9c 08 01 00 00 80    |
    | rcr byte [rax + 1 * rcx - 0x80000000], cl | d2 9c 08 00 00 00 80    |
    | rcr byte [r10 + 0x7f], cl                 | 41 d2 5a 7f             |
    | rcr byte [r10 + 0x80], cl                 | 41 d2 9a 80 00 00 00    |
    | rcr byte [r10 - 0x80], cl                 | 41 d2 5a 80             |
    | rcr byte [r10 - 0x81], cl                 | 41 d2 9a 7f ff ff ff    |
    | ----------------------------------------- | ----------------------- |
"""


def can_encode_rcr_addr8_cl():
    encode(RCR_ADDR8_CL)
