from i13c import err, semantic
from i13c.semantic.model import build_semantic_graph
from i13c.semantic.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_survive_non_terminal_callee_symbol():
    _, program = prepare_program("""
            asm foo() { }
            fn bar() { foo(); }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3010.validate_called_symbol_terminality(model)

    assert len(diagnostics) == 0


def can_detect_non_terminal_caller_symbol():
    source, program = prepare_program("""
            asm foo() { }
            fn bar() noreturn { foo(); }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3010.validate_called_symbol_terminality(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3010
    assert source.extract(diagnostic.ref) == b"bar()"


def can_survive_non_terminal_caller_symbol_not_last_call():
    _, program = prepare_program("""
            asm foo1() noreturn { }
            asm foo2() { }
            fn bar() noreturn { foo1(); foo2(); }
        """)

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = semantic.e3010.validate_called_symbol_terminality(model)

    assert len(diagnostics) == 0
