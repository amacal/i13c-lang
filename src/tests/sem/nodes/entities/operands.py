from i13c.sem import model, syntax
from i13c.sem.typing.entities.operands import (
    Immediate,
    Operand,
    OperandId,
    Reference,
    Register,
)
from tests.sem import prepare_program


def can_do_nothing_without_any_instruction():
    _, program = prepare_program("""
            asm main() noreturn { }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 0


def can_do_nothing_without_any_operand():
    _, program = prepare_program("""
            asm main() noreturn { nop; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 0


def can_detect_an_immediate_operand_one_byte():
    _, program = prepare_program("""
            asm main() noreturn { nop 0x42; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.pop()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"immediate"
    assert isinstance(value.target, Immediate)

    assert value.target.value == 0x42
    assert value.target.width == 8


def can_detect_an_immediate_operand_four_bytes():
    _, program = prepare_program("""
            asm main() noreturn { nop 0x1122334455667788; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.pop()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"immediate"
    assert isinstance(value.target, Immediate)

    assert value.target.value == 0x1122334455667788
    assert value.target.width == 64


def can_detect_a_register_operand():
    _, program = prepare_program("""
            asm main() noreturn { nop rax; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.pop()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"register"
    assert isinstance(value.target, Register)

    assert value.target.name == b"rax"
    assert value.target.width == 64


def can_detect_a_reference_operand():
    _, program = prepare_program("""
            asm main() noreturn { nop var; }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.pop()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"reference"
    assert isinstance(value.target, Reference)

    assert value.target.name == b"var"
