from i13c.sem import model, syntax
from i13c.sem.typing.entities.instructions import Instruction, InstructionId
from tests.sem import prepare_program


def can_do_nothing_without_any_instruction():
    _, program = prepare_program(
        """
            asm main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 0


def can_build_an_instruction_with_no_operands():
    _, program = prepare_program(
        """
            asm main() noreturn { nop; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 1
    id, value = instructions.pop()

    assert isinstance(id, InstructionId)
    assert isinstance(value, Instruction)

    assert value.mnemonic.name == b"nop"
    assert len(value.operands) == 0


def can_build_an_instruction_with_multiple_operands():
    _, program = prepare_program(
        """
            asm main() noreturn { mov rax, 0x42; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 1
    id, value = instructions.pop()

    assert isinstance(id, InstructionId)
    assert isinstance(value, Instruction)

    assert value.mnemonic.name == b"mov"
    assert len(value.operands) == 2


def can_build_an_instruction_with_reference_operand():
    _, program = prepare_program(
        """
            asm main() noreturn { mov rax, src; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instructions = semantic.basic.instructions

    assert instructions.size() == 1
    id, value = instructions.pop()

    assert isinstance(id, InstructionId)
    assert isinstance(value, Instruction)

    assert value.mnemonic.name == b"mov"
    assert len(value.operands) == 2
