from i13c.syntax import tree
from tests.syntax.parsing import parse_instructions


def can_parse_address_with_address_operand_without_disp():
    instructions = parse_instructions("""
        asm main() { mov [rax]; }
    """)

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1.target, tree.snippet.Address)

    assert operand1.target.base is not None
    assert operand1.target.base.name == b"rax"
    assert operand1.target.indx is None
    assert operand1.target.disp is None


def can_parse_address_with_address_operand_with_indx():
    instructions = parse_instructions("""
        asm main() { mov [rax + rbx]; }
    """)

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1.target, tree.snippet.Address)

    assert operand1.target.base is not None
    assert operand1.target.base.name == b"rax"
    assert operand1.target.disp is None

    assert operand1.target.indx is not None
    assert operand1.target.indx.target.name == b"rbx"


def can_parse_address_with_address_operand_with_indx_and_scale():
    instructions = parse_instructions("""
        asm main() { mov [rax + 7*rbx]; }
    """)

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1.target, tree.snippet.Address)

    assert operand1.target.base is not None
    assert operand1.target.base.name == b"rax"
    assert operand1.target.disp is None

    assert operand1.target.indx is not None
    assert operand1.target.indx.target.name == b"rbx"
    assert operand1.target.indx.scale == 7


def can_parse_address_with_address_operand_with_index_but_no_base():
    instructions = parse_instructions("""
        asm main() { mov [7*rbx]; }
    """)

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1.target, tree.snippet.Address)

    assert operand1.target.base is None
    assert operand1.target.disp is None

    assert operand1.target.indx is not None
    assert operand1.target.indx.target.name == b"rbx"
    assert operand1.target.indx.scale == 7


def can_parse_address_with_address_operand_with_positive_disp():
    instructions = parse_instructions("""
        asm main() { mov [rax + 0x04]; }
    """)

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1.target, tree.snippet.Address)

    assert operand1.target.base is not None
    assert operand1.target.base.name == b"rax"
    assert operand1.target.indx is None

    assert isinstance(operand1.target.disp, tree.snippet.Displacement)
    assert operand1.target.disp.offset.digits.hex() == "04"
    assert operand1.target.disp.kind == "forward"


def can_parse_address_with_address_operand_with_negative_disp():
    instructions = parse_instructions("""
        asm main() { mov [rax - 0x04]; }
    """)

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1.target, tree.snippet.Address)

    assert operand1.target.base is not None
    assert operand1.target.base.name == b"rax"

    assert operand1.target.indx is None
    assert isinstance(operand1.target.disp, tree.snippet.Displacement)

    assert operand1.target.disp.offset.digits.hex() == "04"
    assert operand1.target.disp.kind == "backward"


def can_parse_address_with_relative_address():
    instructions = parse_instructions("""
        asm main() { mov [rel @abc]; }
    """)

    assert instructions[0].mnemonic.name == b"mov"
    assert len(instructions[0].operands) == 1

    operand1 = instructions[0].operands[0]
    assert isinstance(operand1.target, tree.snippet.Address)

    assert operand1.target.base is None
    assert operand1.target.indx is None

    assert isinstance(operand1.target.disp, tree.snippet.Reference)
    assert operand1.target.disp.name == b"abc"
