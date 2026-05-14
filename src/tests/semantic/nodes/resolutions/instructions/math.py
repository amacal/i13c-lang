from typing import List, Optional

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples(
    """
        | ------------------- | -------- | ------------ | -------- | ---------------- |
        | instruction         | mnemonic | variant      | status   | reason           |
        | ------------------- | -------- | ------------ | -------- | ---------------- |
        | add rax, 0x12345678 | add      | reg64, imm32 | accepted | -                |
        | add eax, 0x12345678 | add      | reg32, imm32 | accepted | -                |
        | add rax, rbx        | add      | reg64, reg64 | accepted | -                |
        | add rax             | add      | reg64        | rejected | arity-mismatch   |
        | ------------------- | -------- | ------------ | -------- | ---------------- |
    """
)
def can_handle_add(instruction: str, mnemonic: str, variant: List[str], status: bool, reason: Optional[str]):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)
