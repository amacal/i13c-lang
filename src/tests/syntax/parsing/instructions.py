from i13c.syntax.tree import Immediate, Reference, Register
from tests.syntax.parsing import parse_instructions


def can_parse_instruction_without_operands():
    instructions = parse_instructions(
        """
            asm main() { syscall; }
        """
    )

    assert instructions[0].mnemonic.name == b"syscall"
    assert len(instructions[0].operands) == 0


def can_parse_instruction_with_operands():
    instructions = parse_instructions("asm main() { mov rax, rbx; }")

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 2

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, Register)
    assert operand1.name == b"rax"

    operand2 = instructions[0].operands[1]
    assert isinstance(operand2, Register)
    assert operand2.name == b"rbx"


def can_parse_instruction_with_operands_reference():
    instructions = parse_instructions("asm main() { mov rax, @left; }")

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 2

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, Register)
    assert operand1.name == b"rax"

    operand2 = instructions[0].operands[1]
    assert isinstance(operand2, Reference)
    assert operand2.name == b"left"


def can_parse_instruction_with_immediate():
    instructions = parse_instructions("asm main() { mov rax, 0x1234; }")

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 2

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, Register)
    assert operand1.name == b"rax"

    operand2 = instructions[0].operands[1]
    assert isinstance(operand2, Immediate)
    assert operand2.data == bytes([0x12, 0x34])


def can_parse_multiple_instructions():
    instructions = parse_instructions("asm main() { mov rax, rbx; syscall; }")
    assert len(instructions) == 2

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 2

    assert instructions[1].mnemonic.name == b"syscall"
    assert len(instructions[1].operands) == 0
