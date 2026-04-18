from typing import List

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples(
    """
        | --------------------------- | -------- | ------------ | -------- |
        | instruction                 | mnemonic | variant      | status   |
        | --------------------------- | -------- | ------------ | -------- |
        | mov rax, 0x0123456789abcdef | mov      | reg64, imm64 | accepted |
        | mov rax, 0x01234567         | mov      | reg64, imm32 | accepted |
        | mov eax, 0x01234567         | mov      | reg32, imm32 | accepted |
        | mov rax, rbx                | mov      | reg64, reg64 | accepted |
        | mov 0x01234567, rax         | mov      | imm32, reg64 | rejected |
        | --------------------------- | -------- | ------------ | -------- |
    """
)
def can_handle_mov(instruction: str, mnemonic: str, variant: List[str], status: bool):
    verify_instruction_resolution(instruction, mnemonic, variant, status)
