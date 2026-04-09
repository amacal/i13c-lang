from i13c.syntax import tree
from tests.syntax.parsing import parse_instructions


def can_parse_address_with_address_operand_without_offset():
    instructions = parse_instructions(
        """
            asm main() { mov [rax]; }
        """
    )

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, tree.snippet.Address)

    assert operand1.base.name == b"rax"
    assert operand1.offset is None


def can_parse_address_with_address_operand_with_positive_offset():
    instructions = parse_instructions(
        """
            asm main() { mov [rax + 0x04]; }
        """
    )

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, tree.snippet.Address)

    assert operand1.base.name == b"rax"
    assert isinstance(operand1.offset, tree.snippet.Offset)

    assert operand1.offset.value.data == bytes([0x04])
    assert operand1.offset.kind == "forward"



def can_parse_address_with_address_operand_with_negative_offset():
    instructions = parse_instructions(
        """
            asm main() { mov [rax - 0x04]; }
        """
    )

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1, tree.snippet.Address)

    assert operand1.base.name == b"rax"
    assert isinstance(operand1.offset, tree.snippet.Offset)

    assert operand1.offset.value.data == bytes([0x04])
    assert operand1.offset.kind == "backward"
