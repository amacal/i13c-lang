from i13c.syntax import tree
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
    assert isinstance(operand1, tree.snippet.Register)
    assert operand1.name == b"rax"

    operand2 = instructions[0].operands[1]
    assert isinstance(operand2, tree.snippet.Register)
    assert operand2.name == b"rbx"


def can_parse_instruction_with_operands_reference():
    instructions = parse_instructions("asm main() { mov rax, @left; }")

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 2

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, tree.snippet.Register)
    assert operand1.name == b"rax"

    operand2 = instructions[0].operands[1]
    assert isinstance(operand2, tree.snippet.Reference)
    assert operand2.name == b"left"


def can_parse_instruction_with_immediate():
    instructions = parse_instructions("asm main() { mov rax, 0x1234; }")

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 2

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, tree.snippet.Register)
    assert operand1.name == b"rax"

    operand2 = instructions[0].operands[1]
    assert isinstance(operand2, tree.snippet.Immediate)
    assert operand2.value.digits.hex() == "1234"


def can_parse_multiple_instructions():
    instructions = parse_instructions("asm main() { mov rax, rbx; syscall; }")
    assert len(instructions) == 2

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 2

    assert instructions[1].mnemonic.name == b"syscall"
    assert len(instructions[1].operands) == 0
