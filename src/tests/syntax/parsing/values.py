from i13c.syntax import tree
from tests.syntax.parsing import parse_program


def can_accept_value_without_whitespace_around_equals():
    _, program = parse_program("fn main() { val value:u32=0x10; }")

    function = program.functions[0]
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, tree.function.ValueStatement)
    assert statement.name == b"value"
    assert statement.type.name == b"u32"

    assert isinstance(statement.expr, tree.function.IntegerLiteral)
    assert statement.expr.value == bytes([0x10])


def can_accept_value_with_whitespace_around_equals():
    _, program = parse_program("fn main() { val value: u32 = 0x10; }")

    function = program.functions[0]
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, tree.function.ValueStatement)
    assert statement.name == b"value"
    assert statement.type.name == b"u32"

    assert isinstance(statement.expr, tree.function.IntegerLiteral)
    assert statement.expr.value.hex() == "0x10"
