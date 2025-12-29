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
