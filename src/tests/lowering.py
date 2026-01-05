from i13c import ir
from i13c.lowering.build import build_low_level_graph
from i13c.lowering.linear import build_instruction_flow
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph
from tests.sem import prepare_program


def can_lower_syscall_program():
    _, program = prepare_program(
        """
            asm main() noreturn {
                syscall;
            }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = build_instruction_flow(llg)

    assert llg.nodes.size() == 1
    assert len(flow) == 2

    assert isinstance(flow[0], ir.Label)
    assert isinstance(flow[1], ir.SysCall)


def can_lower_mov_program():
    _, program = prepare_program(
        """
            asm main() noreturn {
                mov rax, 0x1234;
            }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = build_instruction_flow(llg)

    assert llg.nodes.size() == 1
    assert len(flow) == 2

    assert isinstance(flow[0], ir.Label)
    assert isinstance(flow[1], ir.MovRegImm)


def can_lower_shl_program():
    _, program = prepare_program(
        """
            asm main() noreturn {
                shl rax, 0x41;
            }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    llg = build_low_level_graph(model)
    flow = build_instruction_flow(llg)

    assert llg.nodes.size() == 1
    assert len(flow) == 2

    assert isinstance(flow[0], ir.Label)
    assert isinstance(flow[1], ir.ShlRegImm)


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
    flow = build_instruction_flow(llg)

    assert llg.nodes.size() == 3  # functions with one block each
    assert len(flow) == 5  # 3 labels + 2 instructions

    assert isinstance(flow[2], ir.MovRegImm)
    assert isinstance(flow[4], ir.SysCall)


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
    flow = build_instruction_flow(llg)

    assert llg.nodes.size() == 2  # functions with one block each
    assert len(flow) == 3  # 2 labels + 1 instruction

    assert isinstance(flow[2], ir.SysCall)
