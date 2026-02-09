from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from tests.sem import prepare_program


def can_do_nothing_without_any_instruction():
    _, program = prepare_program("""
            asm main() noreturn { }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 0


def can_build_an_instruction_with_no_operands():
    _, program = prepare_program("""
            asm main() noreturn { nop; }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 1
    id, value = instructions.pop()

    assert isinstance(id, InstructionId)
    assert isinstance(value, Instruction)

    assert value.mnemonic.name == b"nop"
    assert len(value.operands) == 0


def can_build_an_instruction_with_multiple_operands():
    _, program = prepare_program("""
            asm main() noreturn { mov rax, 0x42; }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 1
    id, value = instructions.pop()

    assert isinstance(id, InstructionId)
    assert isinstance(value, Instruction)

    assert value.mnemonic.name == b"mov"
    assert len(value.operands) == 2


def can_build_an_instruction_with_reference_operand():
    _, program = prepare_program("""
            asm main() noreturn { mov rax, src; }
        """)

    semantic = run_graph(program)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 1
    id, value = instructions.pop()

    assert isinstance(id, InstructionId)
    assert isinstance(value, Instruction)

    assert value.mnemonic.name == b"mov"
    assert len(value.operands) == 2
