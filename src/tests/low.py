from i13c import ir, low, res
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

    unit = low.lower(model)
    assert isinstance(unit, res.Ok)
    assert unit.value.entry == 0

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1
    assert isinstance(instructions[0], ir.SysCall)


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

    unit = low.lower(model)
    assert isinstance(unit, res.Ok)
    assert unit.value.entry == 0

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1

    instruction = instructions[0]
    assert isinstance(instruction, ir.MovRegImm)

    assert instruction.dst == 0
    assert instruction.imm == 0x1234


def can_lower_function_statements_to_codeblocks():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(); bar(); }
            asm foo() { mov rax, 0x01; }
            asm bar() noreturn { syscall; }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    unit = low.lower(model)
    assert isinstance(unit, res.Ok)

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 2

    # first block ends with fallthrough
    assert isinstance(codeblocks[0].terminator, ir.FallThrough)
    assert codeblocks[0].terminator.target == 1

    # last block ends with stop
    assert isinstance(codeblocks[-1].terminator, ir.Stop)


def can_lower_function_final_statement_to_stop():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(); }
            asm foo() noreturn { syscall; }
        """
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    unit = low.lower(model)
    assert isinstance(unit, res.Ok)

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    # single block ends with stop
    assert isinstance(codeblocks[0].terminator, ir.Stop)
