from i13c.syntax.tree import CallStatement, IntegerLiteral
from tests.syntax.parsing import parse_program


def can_accept_callsite_with_hex_literal():
    parse_program("fn main() { exit(0xdeadbeef); }")


def can_accept_callsite_with_parameter_reference():
    parse_program("fn main(code: u32) { exit(code); }")

def can_parse_argument_span_without_trailing_whitespace():
    code, program = parse_program("fn main() { exit(0x01 ); }")

    function = program.functions[0]
    statement = function.statements[0]

    assert isinstance(statement, CallStatement)
    argument = statement.arguments[0]

    assert isinstance(argument, IntegerLiteral)
    assert argument.value == bytes([0x01])
    assert code.extract(argument.ref) == b"0x01"

    assert argument.ref.length == len(b"0x01")
    assert argument.ref.offset == code.data.find(b"0x01")
