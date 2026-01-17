from i13c import ir
from i13c.lowering.build import build_low_level_graph
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_lower_syscall_program():
    _, program = prepare_program(
        """
            asm syscall() noreturn { syscall; }
            fn main() noreturn { syscall(); }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 1  # just one syscall


def can_lower_mov_program():
    _, program = prepare_program(
        """
            asm foo() noreturn { mov rax, 0x1234; }
            fn main() noreturn { foo(); }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 1  # one mov only


def can_lower_mov_with_register_bound_slot():
    _, program = prepare_program(
        """
            asm set(dst@rax: u64, val@imm: u8) noreturn { mov dst, val; }
            fn main() noreturn { set(0x01, 0x42); }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 2  # one inlined mov and one passed as an argument


def can_lower_shl_program():
    _, program = prepare_program(
        """
            asm shl() noreturn { shl rax, 0x41; }
            fn main() noreturn { shl(); }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 1  # just one shl


def can_lower_multiple_callsites():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(); bar(); }
            asm foo() { mov rax, 0x01; }
            asm bar() noreturn { syscall; }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 2  # one mov and one syscall


def can_lower_function_final_statement_to_stop():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(); }
            asm foo() noreturn { syscall; }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 1  # just one syscall


def can_lower_function_calling_another_function():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(); }
            fn foo() noreturn { bar(); }
            asm bar() noreturn { syscall; }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 2  # one call and one syscall


def can_lower_function_calling_another_function_reusing():
    _, program = prepare_program(
        """
            fn main() noreturn { foo1(); foo2(); }
            fn foo1() noreturn { foo3(); }
            fn foo2() noreturn { foo3(); }
            fn foo3() noreturn { bar(); }
            asm bar() noreturn { syscall; }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    instrs = [item for item in flow if not isinstance(item, ir.Label)]
    assert len(instrs) == 3  # two calls and one syscall
