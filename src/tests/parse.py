from i13c import source, lex, parse


def can_parse_instruction_without_operands():
    code = source.open_text("syscall;")
    tokens = lex.tokenize(code)

    program = parse.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 1
    instruction = program.instructions[0]

    assert instruction.mnemonic == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_instruction_with_operands():
    code = source.open_text("mov rax, rbx;")
    tokens = lex.tokenize(code)

    program = parse.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 1
    instruction = program.instructions[0]

    assert instruction.mnemonic == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, parse.ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, parse.ast.Register)
    assert operand2.name == b"rbx"


def can_parse_instruction_with_immediate():
    code = source.open_text("mov rax, 0x1234;")
    tokens = lex.tokenize(code)

    program = parse.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 1
    instruction = program.instructions[0]

    assert instruction.mnemonic == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, parse.ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, parse.ast.Immediate)
    assert operand2.value == 0x1234


def can_parse_multiple_instructions():
    code = source.open_text("mov rax, rbx; syscall;")
    tokens = lex.tokenize(code)

    program = parse.parse(code, tokens)
    assert program is not None

    assert len(program.instructions) == 2

    instruction1 = program.instructions[0]
    assert instruction1.mnemonic == b"mov"
    assert len(instruction1.operands) == 2

    instruction2 = program.instructions[1]
    assert instruction2.mnemonic == b"syscall"
    assert len(instruction2.operands) == 0
