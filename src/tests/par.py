from i13c import lex, par, src, res


def can_parse_instruction_without_operands():
    code = src.open_text("asm main() { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert function.name == b"main"
    assert len(function.instructions) == 1
    instruction = function.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_instruction_with_operands():
    code = src.open_text("asm main() { mov rax, rbx; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert function.name == b"main"
    assert len(function.instructions) == 1
    instruction = function.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, par.ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, par.ast.Register)
    assert operand2.name == b"rbx"


def can_parse_instruction_with_immediate():
    code = src.open_text("asm main() { mov rax, 0x1234; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert function.name == b"main"
    assert len(function.instructions) == 1
    instruction = function.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, par.ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, par.ast.Immediate)
    assert operand2.value == 0x1234


def can_parse_multiple_instructions():
    code = src.open_text("asm main() { mov rax, rbx; syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert function.name == b"main"
    assert len(function.instructions) == 2

    instruction1 = function.instructions[0]
    assert instruction1.mnemonic.name == b"mov"
    assert len(instruction1.operands) == 2

    instruction2 = function.instructions[1]
    assert instruction2.mnemonic.name == b"syscall"
    assert len(instruction2.operands) == 0


def can_handle_empty_program():
    code = src.open_text("")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 0


def can_handle_end_of_tokens():
    code = src.open_text("asm main() { mov rax, rbx")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "P001"


def can_handle_unexpected_token():
    code = src.open_text("asm main() { mov rax rbx\nsyscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "P002"
