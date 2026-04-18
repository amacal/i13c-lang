from typing import List

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples(
    """
        | -------------- | -------- | ----------- | -------- |
        | instruction    | mnemonic | variant     | status   |
        | -------------- | -------- | ----------- | -------- |
        | lea rax, [rbx] | lea      | reg64, addr | accepted |
        | lea ecx, [rbx] | lea      | reg32, addr | accepted |
        | lea dx, [rbx]  | lea      | reg16, addr | rejected |
        | lea rax        | lea      | reg64       | rejected |
        | -------------- | -------- | ----------- | -------- |
    """
)
def can_handle_lea(instruction: str, mnemonic: str, variant: List[str], status: bool):
    verify_instruction_resolution(instruction, mnemonic, variant, status)
