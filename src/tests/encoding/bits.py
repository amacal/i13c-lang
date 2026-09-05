from i13c.semantic.typing.analyses.llvm import BSWAP
from tests.encoding import RegisterInfo, encode_instruction, samples


@samples("""
    | --- | -------- | --- | ---- | -------- |
    | dst | encoding | *** | dst  | encoding |
    | --- | -------- | --- | ---- | -------- |
    | rax | 48 0f c8 | *** | r8   | 49 0f c8 |
    | rcx | 48 0f c9 | *** | r9   | 49 0f c9 |
    | rdx | 48 0f ca | *** | r10  | 49 0f ca |
    | rbx | 48 0f cb | *** | r11  | 49 0f cb |
    | esp | 0f cc    | *** | r12d | 41 0f cc |
    | ebp | 0f cd    | *** | r13d | 41 0f cd |
    | esi | 0f ce    | *** | r14d | 41 0f ce |
    | edi | 0f cf    | *** | r15d | 41 0f cf |
    | --- | -------- | --- | ---- | -------- |
    """)
def can_encode_bswap(dst: str, encoding: bytes):
    encode_instruction(BSWAP(operands=(RegisterInfo.auto(dst),)), encoding)
