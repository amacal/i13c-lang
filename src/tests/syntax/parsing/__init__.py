from typing import List, Tuple

from i13c.core import diagnostics, result
from i13c.syntax import tree
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import SourceCode, open_text


def reject_program(data: str) -> Tuple[SourceCode, List[diagnostics.Diagnostic]]:
    code = open_text(data)

    tokens = tokenize(code)
    assert isinstance(tokens, result.Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, result.Err)

    return code, program.error


def parse_program(data: str) -> Tuple[SourceCode, tree.Program]:
    code = open_text(data)

    tokens = tokenize(code)
    assert isinstance(tokens, result.Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, result.Ok)

    return code, program.value


def parse_snippet(data: str) -> tree.snippet.Snippet:
    _, program = parse_program(data)
    assert isinstance(program, tree.Program)

    assert len(program.snippets) == 1
    return program.snippets[0]


def parse_instructions(data: str) -> Tuple[tree.snippet.Instruction, ...]:
    snippet = parse_snippet(data)

    assert len(snippet.body) >= 1
    return tuple(
        entry for entry in snippet.body if isinstance(entry, tree.snippet.Instruction)
    )


def can_handle_end_of_tokens():
    code = open_text("asm main() { mov rax, rbx")

    tokens = tokenize(code)
    assert isinstance(tokens, result.Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, result.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2000"
    assert diagnostic.ref.offset == len(code.data)
    assert diagnostic.ref.length == 0


def can_handle_unexpected_token():
    code = open_text("asm main() { mov rax rbx\nsyscall; }")

    tokens = tokenize(code)
    assert isinstance(tokens, result.Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, result.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2001"
    assert diagnostic.ref.offset == 21  # offset of "rbx"
    assert diagnostic.ref.length == 3  # length of "rbx"


def can_detect_unknown_function_keyword():
    code = open_text("noreturn main { syscall; }")

    tokens = tokenize(code)
    assert isinstance(tokens, result.Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, result.Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2002"
    assert diagnostic.ref.offset == 0  # offset of "noreturn"
    assert diagnostic.ref.length == 8  # length of "noreturn"
