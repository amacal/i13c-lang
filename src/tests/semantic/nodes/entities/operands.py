from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.operands import (
    Address,
    Immediate,
    Offset,
    Operand,
    OperandId,
    Reference,
    Register,
)
from tests.semantic import prepare_program


def can_do_nothing_without_any_instruction():
    _, program = prepare_program("""
        asm main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 0


def can_do_nothing_without_any_operand():
    _, program = prepare_program("""
        asm main() noreturn { nop; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 0


def can_detect_an_immediate_operand_one_byte():
    _, program = prepare_program("""
        asm main() noreturn { nop 0x42; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.peak()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"immediate"
    assert isinstance(value.target, Immediate)

    assert value.target.data == bytes([0x42])
    assert value.target.width == 8


def can_detect_an_immediate_operand_four_bytes():
    _, program = prepare_program("""
        asm main() noreturn { nop 0x1122334455667788; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.peak()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"immediate"
    assert isinstance(value.target, Immediate)

    assert value.target.width == 64
    assert value.target.data.hex(" ") == "11 22 33 44 55 66 77 88"


def can_detect_a_register_operand():
    _, program = prepare_program("""
        asm main() noreturn { nop rax; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.peak()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"register"
    assert isinstance(value.target, Register)

    assert value.target.name == b"rax"
    assert value.target.width == 64


def can_detect_an_address_operand_without_offset():
    _, program = prepare_program("""
        asm main() noreturn { nop [rax]; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.peak()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"address"
    assert isinstance(value.target, Address)

    assert value.target.base.name == b"rax"
    assert value.target.offset is None



def can_detect_an_address_operand_with_positive_offset():
    _, program = prepare_program("""
        asm main() noreturn { nop [rax + 0x10]; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.peak()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"address"
    assert isinstance(value.target, Address)

    assert value.target.base.name == b"rax"
    assert isinstance(value.target.offset, Offset)

    assert value.target.offset.kind == "forward"
    assert value.target.offset.value.width == 8
    assert value.target.offset.value.data.hex(" ") == "10"


def can_detect_an_address_operand_with_negative_offset():
    _, program = prepare_program("""
        asm main() noreturn { nop [rax - 0x10]; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.peak()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"address"
    assert isinstance(value.target, Address)

    assert value.target.base.name == b"rax"
    assert isinstance(value.target.offset, Offset)

    assert value.target.offset.kind == "backward"
    assert value.target.offset.value.width == 8
    assert value.target.offset.value.data.hex(" ") == "10"


def can_detect_a_reference_operand():
    _, program = prepare_program("""
        asm main() noreturn { nop @var; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    operands = semantic.basic.operands

    assert operands.size() == 1
    id, value = operands.peak()

    assert isinstance(id, OperandId)
    assert isinstance(value, Operand)

    assert value.kind == b"reference"
    assert isinstance(value.target, Reference)

    assert value.target.name == b"var"
