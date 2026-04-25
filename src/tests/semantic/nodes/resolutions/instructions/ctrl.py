from typing import List

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples(
    """
        | ----------- | -------- | ------- | -------- |
        | instruction | mnemonic | variant | status   |
        | ----------- | -------- | ------- | -------- |
        | jmp @x      | jmp      | rel     | accepted |
        | jmp rax     | jmp      | reg64   | accepted |
        | jmp 0x1234  | jmp      | imm16   | rejected |
        | ----------- | -------- | ------- | -------- |
    """
)
def can_handle_jmp(instruction: str, mnemonic: str, variant: List[str], status: bool):
    verify_instruction_resolution(instruction, mnemonic, variant, status)


@samples(
    """
        | ----------- | -------- | ------- | -------- |
        | instruction | mnemonic | variant | status   |
        | ----------- | -------- | ------- | -------- |
        | syscall     | syscall  |         | accepted |
        | syscall rax | syscall  | reg64   | rejected |
        | ----------- | -------- | ------- | -------- |
    """
)
def can_handle_syscall(instruction: str, mnemonic: str, variant: List[str], status: bool):
    verify_instruction_resolution(instruction, mnemonic, variant, status)
