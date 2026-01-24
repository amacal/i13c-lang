from i13c.sem import model, syntax
from tests.sem import prepare_program


def can_do_nothing_without_any_snippet():
    _, program = prepare_program("""
            fn main() noreturn { }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0


def can_do_nothing_without_any_instruction():
    _, program = prepare_program("""
            asm main() noreturn { }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0


def can_do_nothing_with_ambiguous_reference():
    _, program = prepare_program("""
            asm main(val@imm: u8, val@rax: u16) noreturn { nop val; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0
