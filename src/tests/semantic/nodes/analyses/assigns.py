
from i13c.semantic.typing.analyses.llvm import MOV
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_assigns_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.assigns is not None
    assert analyses.assigns.size() == 0


def can_detect_assigns_using_literal():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main() { val x: u8 = 0x42; foo(x); }
    """)

    assert analyses.assigns is not None
    assert analyses.assigns.size() == 1
    _, assign = analyses.assigns.peek()

    assert len(assign.instructions) == 1
    assert isinstance(assign.instructions[0], MOV)

    assert str(assign.instructions[0].operands[0]) == "rdi"
    assert str(assign.instructions[0].operands[1]) == "0x42"


def can_detect_assigns_using_parameter():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main(abc: u8) { val x: u8 = abc; foo(x); }
    """)

    assert analyses.assigns is not None
    assert analyses.assigns.size() == 1
    _, assign = analyses.assigns.peek()

    assert len(assign.instructions) == 1
    assert isinstance(assign.instructions[0], MOV)

    assert str(assign.instructions[0].operands[0]) == "rdi"
    assert str(assign.instructions[0].operands[1]) == "rsi"
