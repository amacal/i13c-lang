from i13c.core.result import Err, Ok
from i13c.syntax import tree
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import open_text
from tests.syntax.parsing import parse_program


def can_parse_function_without_statements():
    _, program = parse_program("fn main() { }")

    assert len(program.functions) == 1
    function = program.functions[0]

    assert isinstance(function, tree.function.Function)
    assert function.name == b"main"
    assert function.noreturn is False
    assert len(function.statements) == 0


def can_parse_function_with_statements():
    _, program = parse_program("fn main() { exit(0x01); }")

    assert len(program.functions) == 1
    function = program.functions[0]

    assert isinstance(function, tree.function.Function)
    assert function.name == b"main"
    assert function.noreturn is False
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, tree.function.CallStatement)
    assert statement.name == b"exit"
    assert len(statement.arguments) == 1

    argument = statement.arguments[0]
    assert isinstance(argument, tree.function.IntegerLiteral)
    assert argument.value == bytes([0x01])


def can_parse_function_with_single_parameter():
    _, program = parse_program("fn main(id: u16) { exit(0x01); }")

    assert len(program.functions) == 1
    function = program.functions[0]

    assert isinstance(function, tree.function.Function)
    assert function.name == b"main"
    assert function.noreturn is False
    assert len(function.parameters) == 1

    parameter = function.parameters[0]
    assert parameter.name == b"id"
    assert parameter.type.name == b"u16"


def can_parse_function_with_multiple_parameters():
    _, program = parse_program("fn main(code: u32, id: u16) { exit(0x01); }")

    assert len(program.functions) == 1
    function = program.functions[0]

    assert isinstance(function, tree.function.Function)
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
    _, program = parse_program("fn main() noreturn { exit(0x01); }")

    assert len(program.functions) == 1
    function = program.functions[0]

    assert isinstance(function, tree.function.Function)
    assert function.name == b"main"
    assert function.noreturn is True
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, tree.function.CallStatement)
    assert statement.name == b"exit"
    assert len(statement.arguments) == 1

    argument = statement.arguments[0]
    assert isinstance(argument, tree.function.IntegerLiteral)
    assert argument.value == bytes([0x01])


def can_parse_function_with_ranged_parameter():
    _, program = parse_program("fn main(value: u8[0x10..0x20]) { }")

    assert len(program.functions) == 1
    function = program.functions[0]

    assert isinstance(function, tree.function.Function)
    assert len(function.parameters) == 1

    parameter = function.parameters[0]
    assert parameter.name == b"value"
    assert parameter.type.name == b"u8"
    assert parameter.type.range is not None
    assert parameter.type.range.lower.hex() == "0x10"
    assert parameter.type.range.upper.hex() == "0x20"


def can_handle_function_missing_parameter_comma():
    code = open_text("fn main(a: u8 b: u8) { exit(0x01); }")

    tokens = tokenize(code)
    assert isinstance(tokens, Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2001"
    assert diagnostic.ref.offset == 14  # offset of "b"
    assert diagnostic.ref.length == 1  # length of "b"
