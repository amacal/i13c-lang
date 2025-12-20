import pytest

from i13c import lex, par, sem, src


def can_accept_operands_arity_of_syscall():
    code = src.open_text("syscall;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)
    sem.validate(program)


def can_accept_operands_arity_of_mov():
    code = src.open_text("mov rax, 0x1234;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)
    sem.validate(program)


def can_detect_invalid_arity_of_xyz():
    code = src.open_text("xyz rax;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)

    with pytest.raises(sem.UnknownInstruction) as ex:
        sem.validate(program)

    assert ex.value.ref.offset == 0


def can_detect_invalid_operand_types_of_mov():
    code = src.open_text("mov 0x1234, 0x5678;")
    tokens = lex.tokenize(code)

    program = par.parse(code, tokens)

    with pytest.raises(sem.InvalidOperandTypes) as ex:
        sem.validate(program)

    assert ex.value.ref.offset == 0
    assert ex.value.found == ["Immediate", "Immediate"]
