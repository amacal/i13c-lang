from typing import List, Optional

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples("""
    | --------------------------- | -------- | ------------------- | -------- | ---------------- |
    | instruction                 | mnemonic | variant             | status   | reason           |
    | --------------------------- | -------- | ------------------- | -------- | ---------------- |
    | mov rax, 0x0123456789abcdef | mov      | reg64, imm64        | accepted | -                |
    | mov rax, 0x01234567         | mov      | reg64, imm32        | accepted | -                |
    | mov eax, 0x01234567         | mov      | reg32, imm32        | accepted | -                |
    | mov rax, rbx                | mov      | reg64, reg64        | accepted | -                |
    | mov 0x01234567, rax         | mov      | imm32, reg64        | rejected | variant-mismatch |
    | mov rax                     | mov      | reg64               | rejected | arity-mismatch   |
    | mov rax, rbx, rcx           | mov      | reg64, reg64, reg64 | rejected | arity-mismatch   |
    | --------------------------- | -------- | ------------------- | -------- | ---------------- |
""")
def can_handle_mov(instruction: str, mnemonic: str, variant: List[str], status: bool, reason: Optional[str]):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)
