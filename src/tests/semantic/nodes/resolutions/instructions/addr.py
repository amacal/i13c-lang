from typing import List, Optional

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples(
    """
        | -------------- | -------- | ----------- | -------- | ---------------- |
        | instruction    | mnemonic | variant     | status   | reason           |
        | -------------- | -------- | ----------- | -------- | ---------------- |
        | lea rax, [rbx] | lea      | reg64, addr | accepted | -                |
        | lea ecx, [rbx] | lea      | reg32, addr | accepted | -                |
        | lea dx, [rbx]  | lea      | reg16, addr | rejected | variant-mismatch |
        | lea rax        | lea      | reg64       | rejected | arity-mismatch   |
        | -------------- | -------- | ----------- | -------- | ---------------- |
    """
)
def can_handle_lea(instruction: str, mnemonic: str, variant: List[str], status: bool, reason: Optional[str]):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)
