from i13c.core.result import Ok
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import open_text


def can_handle_empty_program():
    code = open_text("")

    tokens = tokenize(code)
    assert isinstance(tokens, Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, Ok)

    assert len(program.value.functions) == 0
