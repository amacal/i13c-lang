from typing import List, Optional

from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples("""
    | -------------- | -------- | ------------ | -------- | ---------------- |
    | instruction    | mnemonic | variant      | status   | reason           |
    | -------------- | -------- | ------------ | -------- | ---------------- |
    | bswap rax      | bswap    | reg64        | accepted | -                |
    | bswap eax      | bswap    | reg32        | accepted | -                |
    | bswap ax       | bswap    | reg16        | rejected | variant-mismatch |
    | bswap al       | bswap    | reg8         | rejected | variant-mismatch |
    | bswap [rax]    | bswap    | addr         | rejected | variant-mismatch |
    | bswap rax, rbx | bswap    | reg64, reg64 | rejected | arity-mismatch   |
    | -------------- | -------- | ------------ | -------- | ---------------- |
""")
def can_handle_bswap(
    instruction: str,
    mnemonic: str,
    variant: List[str],
    status: bool,
    reason: Optional[str],
):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)


@samples("""
    | --------------- | -------- | ----------- | -------- | ---------------- |
    | instruction     | mnemonic | variant     | status   | reason           |
    | --------------- | -------- | ----------- | -------- | ---------------- |
    | shl rax, 0x01   | shl      | reg64, imm8 | accepted | -                |
    | shl eax, 0x01   | shl      | reg32, imm8 | accepted | -                |
    | shl ax, 0x01    | shl      | reg16, imm8 | accepted | -                |
    | shl al, 0x01    | shl      | reg8, imm8  | accepted | -                |
    | shl [rax], 0x01 | shl      | addr, imm8  | rejected | variant-mismatch |
    | shl rax         | shl      | reg64       | rejected | arity-mismatch   |
    | --------------- | -------- | ----------- | -------- | ---------------- |
""")
def can_handle_shl(
    instruction: str,
    mnemonic: str,
    variant: List[str],
    status: bool,
    reason: Optional[str],
):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)
