from i13c import ast, err, lex, par, res, src


def can_parse_asm_instruction_without_operands():
    code = src.open_text("asm main() { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"main"
    assert function.terminal is False

    assert len(function.instructions) == 1
    instruction = function.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_asm_instruction_with_operands():
    code = src.open_text("asm main() { mov rax, rbx; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"main"
    assert function.terminal is False

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


def can_parse_asm_instruction_with_immediate():
    code = src.open_text("asm main() { mov rax, 0x1234; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"main"
    assert function.terminal is False

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


def can_parse_multiple_asm_instructions():
    code = src.open_text("asm main() { mov rax, rbx; syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"main"
    assert function.terminal is False
    assert len(function.instructions) == 2

    instruction1 = function.instructions[0]
    assert instruction1.mnemonic.name == b"mov"
    assert len(instruction1.operands) == 2

    instruction2 = function.instructions[1]
    assert instruction2.mnemonic.name == b"syscall"
    assert len(instruction2.operands) == 0


def can_parse_asm_functions_with_single_arg():
    code = src.open_text("asm exit(code@rdi: u32) { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"exit"
    assert function.terminal is False
    assert len(function.instructions) == 1

    instruction = function.instructions[0]
    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0

    parameters = function.parameters
    assert len(parameters) == 1

    parameter = parameters[0]
    assert parameter.name == b"code"
    assert parameter.type.name == b"u32"
    assert parameter.bind.name == b"rdi"


def can_parse_asm_functions_with_multiple_args():
    code = src.open_text("asm exit(code@rdi: u32, id@rax: u16) { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"exit"
    assert function.terminal is False
    assert len(function.instructions) == 1

    instruction = function.instructions[0]
    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0

    parameters = function.parameters
    assert len(parameters) == 2

    parameter1 = parameters[0]
    assert parameter1.name == b"code"
    assert parameter1.type.name == b"u32"
    assert parameter1.bind.name == b"rdi"

    parameter2 = parameters[1]
    assert parameter2.name == b"id"
    assert parameter2.type.name == b"u16"
    assert parameter2.bind.name == b"rax"


def can_parse_asm_functions_with_clobbers():
    code = src.open_text("asm aux() clobbers rax, rbx { mov rax, rbx; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"aux"
    assert function.terminal is False
    assert len(function.clobbers) == 2

    assert function.clobbers[0].name == b"rax"
    assert function.clobbers[1].name == b"rbx"

    assert len(function.instructions) == 1
    instruction = function.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2


def can_parse_asm_functions_with_no_return():
    code = src.open_text("asm halt() noreturn { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"halt"
    assert function.terminal is True

    assert len(function.instructions) == 1
    instruction = function.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_asm_functions_with_no_return_with_clobbers():
    code = src.open_text("asm halt() noreturn clobbers rax { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.AsmFunction)
    assert function.name == b"halt"
    assert function.terminal is True

    clobbers = function.clobbers
    assert len(clobbers) == 1
    assert clobbers[0].name == b"rax"

    assert len(function.instructions) == 1
    instruction = function.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_handle_empty_program():
    code = src.open_text("")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 0


def can_parse_reg_function_without_statements():
    code = src.open_text("fn main() { }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.RegFunction)
    assert function.name == b"main"
    assert function.terminal is False
    assert len(function.statements) == 0


def can_parse_reg_function_with_statements():
    code = src.open_text("fn main() { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.RegFunction)
    assert function.name == b"main"
    assert function.terminal is False
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, ast.CallStatement)
    assert statement.name == b"exit"
    assert len(statement.arguments) == 1

    argument = statement.arguments[0]
    assert isinstance(argument, ast.IntegerLiteral)
    assert argument.value == 0x1


def can_parse_reg_function_with_single_parameter():
    code = src.open_text("fn main(id: u16) { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.RegFunction)
    assert function.name == b"main"
    assert function.terminal is False
    assert len(function.parameters) == 1

    parameter = function.parameters[0]
    assert parameter.name == b"id"
    assert parameter.type.name == b"u16"


def can_parse_reg_function_with_multiple_parameters():
    code = src.open_text("fn main(code: u32, id: u16) { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.RegFunction)
    assert function.name == b"main"
    assert function.terminal is False
    assert len(function.parameters) == 2

    parameter1 = function.parameters[0]
    assert parameter1.name == b"code"
    assert parameter1.type.name == b"u32"

    parameter2 = function.parameters[1]
    assert parameter2.name == b"id"
    assert parameter2.type.name == b"u16"


def can_parse_reg_function_with_flags_noreturn():
    code = src.open_text("fn main() noreturn { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.RegFunction)
    assert function.name == b"main"
    assert function.terminal is True
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, ast.CallStatement)
    assert statement.name == b"exit"
    assert len(statement.arguments) == 1

    argument = statement.arguments[0]
    assert isinstance(argument, ast.IntegerLiteral)
    assert argument.value == 0x1


def can_handle_end_of_tokens():
    code = src.open_text("asm main() { mov rax, rbx")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2000
    assert diagnostic.ref.offset == len(code.data)
    assert diagnostic.ref.length == 0


def can_handle_unexpected_token():
    code = src.open_text("asm main() { mov rax rbx\nsyscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2001
    assert diagnostic.ref.offset == 21  # offset of "rbx"
    assert diagnostic.ref.length == 3  # length of "rbx"


def can_detect_unknown_function_keyword():
    code = src.open_text("noreturn main { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2002
    assert diagnostic.ref.offset == 0  # offset of "noreturn"
    assert diagnostic.ref.length == 8  # length of "noreturn"


def can_detect_duplicated_asm_flags_noreturn():
    code = src.open_text("asm halt() noreturn noreturn { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2003
    assert diagnostic.ref.offset == 20  # offset of 2nd "noreturn"
    assert diagnostic.ref.length == 8  # length of 2nd "noreturn


def can_detect_duplicated_asm_flags_clobbers():
    code = src.open_text("asm aux() clobbers rax clobbers rcx { mov rax, rbx; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2003
    assert diagnostic.ref.offset == 23  # offset of 2nd "clobbers"
    assert diagnostic.ref.length == 8  # length of 2nd "clobbers"


def can_detect_duplicated_asm_flags_clobbers_with_noreturn_after():
    code = src.open_text(
        "asm aux() clobbers rax clobbers rbx noreturn { mov rax, rbx; }"
    )

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2003
    assert diagnostic.ref.offset == 23  # offset of 2nd "clobbers"
    assert diagnostic.ref.length == 8  # length of 2nd "clobbers"


def can_detect_duplicated_asm_flags_noreturn_with_clobbers_after():
    code = src.open_text("asm halt() noreturn noreturn clobbers rax { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2003
    assert diagnostic.ref.offset == 20  # offset of 2nd "noreturn"
    assert diagnostic.ref.length == 8  # length of 2nd "noreturn"
