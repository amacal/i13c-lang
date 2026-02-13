from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.operands import Immediate, Operand, Register
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from tests.sem import prepare_program


def can_do_nothing_without_any_snippet():
    _, program = prepare_program("""
        fn main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    snippets = semantic.basic.snippets

    assert snippets.size() == 0


def can_build_a_snippet_with_no_instruction():
    _, program = prepare_program("""
        asm main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    snippets = semantic.basic.snippets

    assert snippets.size() == 1
    id, value = snippets.pop()

    assert isinstance(id, SnippetId)
    assert isinstance(value, Snippet)

    assert value.identifier.name == b"main"
    assert len(value.instructions) == 0


def can_build_a_snippet_with_no_noreturn():
    _, program = prepare_program("""
        asm main() { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    snippets = semantic.basic.snippets

    assert snippets.size() == 1
    id, value = snippets.pop()

    assert isinstance(id, SnippetId)
    assert isinstance(value, Snippet)

    assert value.identifier.name == b"main"
    assert value.noreturn is False


def can_build_a_snippet_with_noreturn():
    _, program = prepare_program("""
        asm main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    snippets = semantic.basic.snippets

    assert snippets.size() == 1
    id, value = snippets.pop()

    assert isinstance(id, SnippetId)
    assert isinstance(value, Snippet)

    assert value.identifier.name == b"main"
    assert value.noreturn is True


def can_build_a_snippet_with_clobber_list():
    _, program = prepare_program("""
        asm main() clobbers rax, rbx { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    snippets = semantic.basic.snippets

    assert snippets.size() == 1
    id, value = snippets.pop()

    assert isinstance(id, SnippetId)
    assert isinstance(value, Snippet)

    assert value.identifier.name == b"main"
    assert len(value.clobbers) == 2

    assert value.clobbers[0].name == b"rax"
    assert value.clobbers[1].name == b"rbx"


def can_build_a_snippet_with_mov_instruction():
    _, program = prepare_program("""
        asm main() { mov rax, 0x1234; }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    snippets = semantic.basic.snippets

    operands = semantic.basic.operands
    assert operands.size() == 2

    assert snippets.size() == 1
    id, value = snippets.pop()

    assert isinstance(id, SnippetId)
    assert isinstance(value, Snippet)

    assert value.identifier.name == b"main"
    assert value.noreturn is False

    assert len(value.instructions) == 1
    iid = value.instructions[0]

    assert isinstance(iid, InstructionId)
    instruction = semantic.basic.instructions.get(iid)

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand0 = operands.get(instruction.operands[0])
    assert isinstance(operand0, Operand)

    assert operand0.kind == b"register"
    assert isinstance(operand0.target, Register)
    assert operand0.target.name == b"rax"

    operand1 = operands.get(instruction.operands[1])
    assert isinstance(operand1, Operand)

    assert operand1.kind == b"immediate"
    assert isinstance(operand1.target, Immediate)
    assert operand1.target.value == 0x1234


def can_build_a_snippet_with_properly_derived_types():
    _, program = prepare_program("""
        asm main(
            r1@rax: u64[0x0000..0xffff],
            r2@rbx: u8[0x00..0x10]
        ) {}
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    snippets = semantic.basic.snippets

    assert snippets.size() == 1
    _, value = snippets.peak()

    assert value.identifier.name == b"main"
    assert len(value.slots) == 2

    slot1 = value.slots[0]
    assert slot1.name.name == b"r1"
    assert slot1.bind.name == b"rax"
    assert slot1.type.name == b"u64"
    assert slot1.type.width == 16
    assert slot1.type.range.lower == 0x0000
    assert slot1.type.range.upper == 0xFFFF

    slot2 = value.slots[1]
    assert slot2.name.name == b"r2"
    assert slot2.bind.name == b"rbx"
    assert slot2.type.name == b"u8"
    assert slot2.type.width == 8
    assert slot2.type.range.lower == 0x00
    assert slot2.type.range.upper == 0x10
