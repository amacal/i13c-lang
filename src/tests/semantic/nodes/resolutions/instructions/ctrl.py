from typing import List, Optional

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples(
    """
        | ----------- | -------- | ------- | -------- | ---------------- |
        | instruction | mnemonic | variant | status   | reason           |
        | ----------- | -------- | ------- | -------- | ---------------- |
        | jmp @x      | jmp      | rel     | accepted | -                |
        | jmp rax     | jmp      | reg64   | accepted | -                |
        | jmp 0x1234  | jmp      | imm16   | rejected | variant-mismatch |
        | ----------- | -------- | ------- | -------- | ---------------- |
    """
)
def can_handle_jmp(instruction: str, mnemonic: str, variant: List[str], status: bool, reason: Optional[str]):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)


@samples(
    """
        | ----------- | -------- | ------- | -------- | -------------- |
        | instruction | mnemonic | variant | status   | reason         |
        | ----------- | -------- | ------- | -------- | -------------- |
        | syscall     | syscall  |         | accepted | -              |
        | syscall rax | syscall  | reg64   | rejected | arity-mismatch |
        | ----------- | -------- | ------- | -------- | -------------- |
    """
)
def can_handle_syscall(instruction: str, mnemonic: str, variant: List[str], status: bool, reason: Optional[str]):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)
