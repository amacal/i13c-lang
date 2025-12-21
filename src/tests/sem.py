from i13c import lex, par, sem, src, res


def can_accept_operands_arity_of_syscall():
    code = src.open_text("syscall;")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    diagnostics = sem.validate(program.value)
    assert len(diagnostics) == 0


def can_accept_operands_arity_of_mov():
    code = src.open_text("mov rax, 0x1234;")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    diagnostics = sem.validate(program.value)
    assert len(diagnostics) == 0


def can_detect_invalid_instruction():
    code = src.open_text("xyz rax;")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    # force invalid mnemonic
    tokens.value[0] = lex.Token(code=lex.TOKEN_MNEMONIC, offset=0, length=3)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    diagnostics = sem.validate(program.value)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 0
    assert diagnostic.code == "V001"


def can_detect_immediate_out_of_range():
    code = src.open_text("mov rax, 0x1ffffffffffffffff;")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    diagnostics = sem.validate(program.value)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 0
    assert diagnostic.code == "V002"


def can_detect_invalid_operand_types_of_mov():
    code = src.open_text("mov 0x1234, 0x5678;")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    diagnostics = sem.validate(program.value)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 0
    assert diagnostic.code == "V003"
