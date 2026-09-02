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

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    asmlet, _ = analyses.asmlets.peek()

    for idx, statement in enumerate(analyses.statements.values()):
        if isinstance(statement.acceptance.target, AssignAcceptance):
            assert idx == 0
            assert statement.listing() == [
                "mov edi, 0x00000042",
            ]

        else:
            assert idx == 1
            assert statement.listing() == [
                "mov rax, rdi",
                f"call {asmlet.identify(1)}",
            ]


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

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    asmlet, _ = analyses.asmlets.peek()

    for idx, statement in enumerate(analyses.statements.values()):
        if isinstance(statement.acceptance.target, AssignAcceptance):
            assert idx == 0
            assert statement.listing() == [
                "mov r11d, 0x00000042",
                "mov qword [rsp + 0x00], r11",
            ]

        else:
            assert idx == 1
            assert statement.listing() == [
                "mov rax, qword [rsp + 0x00]",
                f"call {asmlet.identify(1)}",
            ]
