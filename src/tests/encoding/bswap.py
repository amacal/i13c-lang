from tests.encoding.core import encode, exhaust


def can_exhaust_bswap():
    exhaust(
        BSWAP_REG32,
        BSWAP_REG64,
    )


BSWAP_REG64 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | bswap rax   | 48 0f c8 | *** | bswap r8    | 49 0f c8 |
    | bswap rcx   | 48 0f c9 | *** | bswap r9    | 49 0f c9 |
    | bswap rdx   | 48 0f ca | *** | bswap r10   | 49 0f ca |
    | bswap rbx   | 48 0f cb | *** | bswap r11   | 49 0f cb |
    | bswap rsp   | 48 0f cc | *** | bswap r12   | 49 0f cc |
    | bswap rbp   | 48 0f cd | *** | bswap r13   | 49 0f cd |
    | bswap rsi   | 48 0f ce | *** | bswap r14   | 49 0f ce |
    | bswap rdi   | 48 0f cf | *** | bswap r15   | 49 0f cf |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_bswap_reg64():
    encode(BSWAP_REG64)


BSWAP_REG32 = """
    | ----------- | -------- | --- | ----------- | -------- |
    | instruction | encoding | *** | instruction | encoding |
    | ----------- | -------- | --- | ----------- | -------- |
    | bswap eax   | 0f c8    | *** | bswap r8d   | 41 0f c8 |
    | bswap ecx   | 0f c9    | *** | bswap r9d   | 41 0f c9 |
    | bswap edx   | 0f ca    | *** | bswap r10d  | 41 0f ca |
    | bswap ebx   | 0f cb    | *** | bswap r11d  | 41 0f cb |
    | bswap esp   | 0f cc    | *** | bswap r12d  | 41 0f cc |
    | bswap ebp   | 0f cd    | *** | bswap r13d  | 41 0f cd |
    | bswap esi   | 0f ce    | *** | bswap r14d  | 41 0f ce |
    | bswap edi   | 0f cf    | *** | bswap r15d  | 41 0f cf |
    | ----------- | -------- | --- | ----------- | -------- |
"""


def can_encode_bswap_reg32():
    encode(BSWAP_REG32)
