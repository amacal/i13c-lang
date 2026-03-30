from i13c.syntax.tree import IntegerLiteral, ValueStatement
from tests.syntax.parsing import parse_program


def can_accept_value_without_whitespace_around_equals():
    _, program = parse_program("fn main() { val value:u32=0x10; }")

    function = program.functions[0]
    assert len(function.statements) == 1

    statement = function.statements[0]
    assert isinstance(statement, ValueStatement)
    assert statement.name == b"value"
    assert statement.type.name == b"u32"

    assert isinstance(statement.expr, IntegerLiteral)
    assert statement.expr.value == 0x10
