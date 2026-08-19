
from i13c.semantic.typing.analyses.llvm import Call, Move
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_statements_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.statements is not None
    assert analyses.statements.size() == 0


def can_detect_statements_pure_assign_and_call():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) { }
        fn main() { val x: u8 = 0x42; foo(x); }
    """)

    assert analyses.statements is not None
    assert analyses.statements.size() == 2

    for idx, statement in enumerate(analyses.statements.values()):
        if isinstance(statement.acceptance.target, AssignAcceptance):
            assert idx == 0
            assert len(statement.instructions) == 1

            # move to rax
            assert isinstance(statement.instructions[0], Move)
            assert str(statement.instructions[0].variant[0]) == "rdi"
            assert str(statement.instructions[0].variant[1]) == "0x42"

        else:
            assert idx == 1
            assert len(statement.instructions) == 2

            # move to rdi
            assert isinstance(statement.instructions[0], Move)
            assert str(statement.instructions[0].variant[0]) == "rax"
            assert str(statement.instructions[0].variant[1]) == "rdi"

            # call
            assert isinstance(statement.instructions[1], Call)


def can_detect_statements_assign_with_spills():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8)
            clobbers
                rdi, rsi, rdx, rcx, r8, r9, r10, r11,
                r12, r13, r14, r15, rbx, rax, rbp { }

        fn main() { val x: u8 = 0x42; foo(x); }
    """)

    assert analyses.statements is not None
    assert analyses.statements.size() == 2

    for idx, statement in enumerate(analyses.statements.values()):
        if isinstance(statement.acceptance.target, AssignAcceptance):
            assert idx == 0
            assert len(statement.instructions) == 2

            # move to rax
            assert isinstance(statement.instructions[0], Move)
            assert str(statement.instructions[0].variant[0]) == "r11"
            assert str(statement.instructions[0].variant[1]) == "0x42"

            # move to stack
            assert isinstance(statement.instructions[1], Move)
            assert str(statement.instructions[1].variant[0]) == "#0"
            assert str(statement.instructions[1].variant[1]) == "r11"

        else:
            assert idx == 1
            assert len(statement.instructions) == 2

            # move to rdi
            assert isinstance(statement.instructions[0], Move)
            assert str(statement.instructions[0].variant[0]) == "rax"
            assert str(statement.instructions[0].variant[1]) == "#0"

            # call
            assert isinstance(statement.instructions[1], Call)
