from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.resolutions.instructions import InstructionResolution
from tests.semantic import prepare_program


def prepare_resolution(code: str) -> InstructionResolution:
    _, program = prepare_program(code)
    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 1
    _, value = instructions.peak()

    return value


def can_do_nothing_without_any_snippet():
    _, program = prepare_program(
        """
            fn main() noreturn { }
        """
    )

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0


def can_do_nothing_without_any_instruction():
    _, program = prepare_program(
        """
            asm main() noreturn { }
        """
    )

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0


def can_do_nothing_with_ambiguous_reference():
    _, program = prepare_program(
        """
            asm main(value@imm: u8, value@rax: u16) noreturn { nop @value; }
        """
    )

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    instructions = semantic.indices.resolution_by_instruction

    assert instructions.size() == 0
