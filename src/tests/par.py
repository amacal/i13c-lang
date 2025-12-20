import pytest

from i13c import lex, par, src


def can_parse_instruction_without_operands():
    code = src.open_text("syscall;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 1
    instruction = program.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_instruction_with_operands():
    code = src.open_text("mov rax, rbx;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 1
    instruction = program.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, par.ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, par.ast.Register)
    assert operand2.name == b"rbx"


def can_parse_instruction_with_immediate():
    code = src.open_text("mov rax, 0x1234;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 1
    instruction = program.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, par.ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, par.ast.Immediate)
    assert operand2.value == 0x1234


def can_parse_multiple_instructions():
    code = src.open_text("mov rax, rbx; syscall;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 2

    instruction1 = program.instructions[0]
    assert instruction1.mnemonic.name == b"mov"
    assert len(instruction1.operands) == 2

    instruction2 = program.instructions[1]
    assert instruction2.mnemonic.name == b"syscall"
    assert len(instruction2.operands) == 0


def can_handle_empty_program():
    code = src.open_text("")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 0


def can_handle_end_of_tokens():
    code = src.open_text("mov rax, rbx")
    tokens = lex.tokenize(code)

    with pytest.raises(par.UnexpectedEndOfTokens):
        par.parse(code, tokens)


def can_handle_unexpected_token():
    code = src.open_text("mov rax rbx\nsyscall;")
    tokens = lex.tokenize(code)

    with pytest.raises(par.UnexpectedTokenCode):
        par.parse(code, tokens)
