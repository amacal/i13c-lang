from i13c import ast, err, lex, par, res, src


def can_parse_instruction_without_operands():
    code = src.open_text("asm main() { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"main"
    assert snippet.noreturn is False

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_instruction_with_operands():
    code = src.open_text("asm main() { mov rax, rbx; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"main"
    assert snippet.noreturn is False

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, ast.Register)
    assert operand2.name == b"rbx"


def can_parse_instruction_with_operands_reference():
    code = src.open_text("asm main() { mov rax, left; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"main"
    assert snippet.noreturn is False

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand1 = instruction.operands[0]
    assert isinstance(operand1, par.ast.Register)
    assert operand1.name == b"rax"

    operand2 = instruction.operands[1]
    assert isinstance(operand2, par.ast.Reference)
    assert operand2.name == b"left"


def can_parse_instruction_with_immediate():
    code = src.open_text("asm main() { mov rax, 0x1234; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"main"
    assert snippet.noreturn is False

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

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

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"main"
    assert snippet.noreturn is False
    assert len(snippet.instructions) == 2

    instruction1 = snippet.instructions[0]
    assert instruction1.mnemonic.name == b"mov"
    assert len(instruction1.operands) == 2

    instruction2 = snippet.instructions[1]
    assert instruction2.mnemonic.name == b"syscall"
    assert len(instruction2.operands) == 0


def can_parse_snippets_with_single_arg():
    code = src.open_text("asm exit(code@rdi: u32) { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"exit"
    assert snippet.noreturn is False
    assert len(snippet.instructions) == 1

    instruction = snippet.instructions[0]
    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0

    slots = snippet.slots
    assert len(slots) == 1

    slot = slots[0]
    assert slot.name == b"code"
    assert slot.type.name == b"u32"

    assert isinstance(slot.bind, ast.Binding)
    assert slot.bind.name == b"rdi"


def can_parse_snippets_with_multiple_args():
    code = src.open_text("asm exit(code@rdi: u32, id@rax: u16) { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"exit"
    assert snippet.noreturn is False
    assert len(snippet.instructions) == 1

    instruction = snippet.instructions[0]
    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0

    slots = snippet.slots
    assert len(slots) == 2

    slot1 = slots[0]
    assert slot1.name == b"code"
    assert slot1.type.name == b"u32"

    assert isinstance(slot1.bind, ast.Binding)
    assert slot1.bind.name == b"rdi"

    slot2 = slots[1]
    assert slot2.name == b"id"
    assert slot2.type.name == b"u16"

    assert isinstance(slot2.bind, ast.Binding)
    assert slot2.bind.name == b"rax"


def can_parse_snippets_with_bind_to_immediate():
    code = src.open_text("asm exit(code@imm: u32) { }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"exit"
    assert snippet.noreturn is False
    assert len(snippet.instructions) == 0

    slots = snippet.slots
    assert len(slots) == 1

    slot = slots[0]
    assert slot.name == b"code"
    assert slot.type.name == b"u32"

    assert isinstance(slot.bind, ast.Binding)
    assert slot.bind.name == b"imm"


def can_parse_snippets_with_clobbers():
    code = src.open_text("asm aux() clobbers rax, rbx { mov rax, rbx; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"aux"
    assert snippet.noreturn is False
    assert len(snippet.clobbers) == 2

    assert snippet.clobbers[0].name == b"rax"
    assert snippet.clobbers[1].name == b"rbx"

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2


def can_parse_snippets_with_no_return():
    code = src.open_text("asm halt() noreturn { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"halt"
    assert snippet.noreturn is True

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_snippets_with_no_return_with_clobbers():
    code = src.open_text("asm halt() noreturn clobbers rax { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert snippet.name == b"halt"
    assert snippet.noreturn is True

    clobbers = snippet.clobbers
    assert len(clobbers) == 1
    assert clobbers[0].name == b"rax"

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_snipper_with_ranged_parameter():
    code = src.open_text("asm main(value@rdi: u8[0x10..0x20]) { }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.snippets) == 1
    snippet = program.value.snippets[0]

    assert isinstance(snippet, ast.Snippet)
    assert len(snippet.slots) == 1

    slot = snippet.slots[0]
    assert slot.name == b"value"
    assert slot.type.name == b"u8"
    assert slot.type.range is not None
    assert slot.type.range.lower == 0x10
    assert slot.type.range.upper == 0x20


def can_handle_empty_program():
    code = src.open_text("")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 0


def can_parse_function_without_statements():
    code = src.open_text("fn main() { }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.Function)
    assert function.name == b"main"
    assert function.noreturn is False
    assert len(function.statements) == 0


def can_parse_function_with_statements():
    code = src.open_text("fn main() { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.Function)
    assert function.name == b"main"
    assert function.noreturn is False
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, ast.CallStatement)
    assert statement.name == b"exit"
    assert len(statement.arguments) == 1

    argument = statement.arguments[0]
    assert isinstance(argument, ast.IntegerLiteral)
    assert argument.value == 0x1


def can_parse_function_with_single_parameter():
    code = src.open_text("fn main(id: u16) { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.Function)
    assert function.name == b"main"
    assert function.noreturn is False
    assert len(function.parameters) == 1

    parameter = function.parameters[0]
    assert parameter.name == b"id"
    assert parameter.type.name == b"u16"


def can_parse_function_with_multiple_parameters():
    code = src.open_text("fn main(code: u32, id: u16) { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.Function)
    assert function.name == b"main"
    assert function.noreturn is False
    assert len(function.parameters) == 2

    parameter1 = function.parameters[0]
    assert parameter1.name == b"code"
    assert parameter1.type.name == b"u32"

    parameter2 = function.parameters[1]
    assert parameter2.name == b"id"
    assert parameter2.type.name == b"u16"


def can_parse_function_with_flags_noreturn():
    code = src.open_text("fn main() noreturn { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.Function)
    assert function.name == b"main"
    assert function.noreturn is True
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, ast.CallStatement)
    assert statement.name == b"exit"
    assert len(statement.arguments) == 1

    argument = statement.arguments[0]
    assert isinstance(argument, ast.IntegerLiteral)
    assert argument.value == 0x1


def can_parse_function_with_ranged_parameter():
    code = src.open_text("fn main(value: u8[0x10..0x20]) { }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Ok)

    assert len(program.value.functions) == 1
    function = program.value.functions[0]

    assert isinstance(function, ast.Function)
    assert len(function.parameters) == 1

    parameter = function.parameters[0]
    assert parameter.name == b"value"
    assert parameter.type.name == b"u8"
    assert parameter.type.range is not None
    assert parameter.type.range.lower == 0x10
    assert parameter.type.range.upper == 0x20


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


def can_handle_missing_parameter_comma():
    code = src.open_text("fn main(a: u8 b: u8) { exit(0x1); }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2001
    assert diagnostic.ref.offset == 14  # offset of "b"
    assert diagnostic.ref.length == 1  # length of "b"


def can_handle_missing_slot_comma():
    code = src.open_text("asm exit(code@rdi: u32 id@rax: u16) { syscall; }")

    tokens = lex.tokenize(code)
    assert isinstance(tokens, res.Ok)

    program = par.parse(code, tokens.value)
    assert isinstance(program, res.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == err.ERROR_2001
    assert diagnostic.ref.offset == 23  # offset of "id"
    assert diagnostic.ref.length == 2  # length of "id"


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


def can_detect_duplicated_flags_noreturn():
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


def can_detect_duplicated_flags_clobbers():
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


def can_detect_duplicated_flags_clobbers_with_noreturn_after():
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


def can_detect_duplicated_flags_noreturn_with_clobbers_after():
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
