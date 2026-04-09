from i13c.llvm.typing.instructions.core import Immediate, Register
from i13c.llvm.typing.instructions.math import SUB
from tests.encoding import encode_instruction, samples


@samples(
    """
        | --- | ---------- | -------------------- | --- | ---- | ---------- | -------------------- |
        | dst | imm32      | encoding             | *** | dst  | imm32      | encoding             |
        | --- | ---------- | -------------------- | --- | ---- | ---------- | -------------------- |
        | rax | 0x12345678 | 48 2d 78 56 34 12    | *** | r8   | 0x12345678 | 49 81 e8 78 56 34 12 |
        | rcx | 0x12345678 | 48 81 e9 78 56 34 12 | *** | r12  | 0x12345678 | 49 81 ec 78 56 34 12 |
        | eax | 0x12345678 | 2d 78 56 34 12       | *** | r10d | 0x12345678 | 41 81 ea 78 56 34 12 |
        | esi | 0x12345678 | 81 ee 78 56 34 12    | *** | r11d | 0x12345678 | 41 81 eb 78 56 34 12 |
        | ax  | 0x1234     | 66 2d 34 12          | *** | r12w | 0x5678     | 66 41 81 ec 78 56    |
        | dx  | 0x1234     | 66 81 ea 34 12       | *** | r13w | 0x5678     | 66 41 81 ed 78 56    |
        | al  | 0x12       | 2c 12                | *** | r12b | 0x78       | 41 80 ec 78          |
        | ah  | 0x12       | 80 ec 12             | *** | r15b | 0x08       | 41 80 ef 08          |
        | --- | ---------- | -------------------- | --- | ---- | ---------- | -------------------- |
    """
)
def can_encode_sub_reg_imm(dst: str, imm32: bytes, encoding: bytes):
    encode_instruction(
        SUB(
            dst=Register.auto(dst),
            src=Immediate.auto(imm32),
        ),
        encoding,
    )
