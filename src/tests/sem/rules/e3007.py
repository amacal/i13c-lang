from i13c import err, sem
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_detect_overloaded_symbol_by_arity():
    source, program = prepare_program(
        """
            asm foo(abc@rax: u32) { }
            fn main() { foo(); }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3007.validate_called_symbol_resolved(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3007
    assert source.extract(diagnostic.ref) == b"foo()"


def can_detect_overloaded_symbol_by_range():
    source, program = prepare_program(
        """
            asm foo(abc@rax: u32[0x01..0x09]) { }
            fn main() { foo(0x10); }
        """
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3007.validate_called_symbol_resolved(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3007
    assert source.extract(diagnostic.ref) == b"foo(0x10)"
