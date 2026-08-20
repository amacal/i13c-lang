from i13c.semantic.typing.analyses.asmlets import AsmletId
from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_blocklets_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.blocklets is not None
    assert analyses.blocklets.size() == 1
    _, blocklet = analyses.blocklets.peek()

    assert len(blocklet.blocks) == 1
    assert blocklet.listing() == [
        "ret",
    ]


def can_detect_blocklets_of_asm_snippet():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) clobbers rdi {
            mov rdi, rax;
            bswap rdi;
        }

        fn main() { foo(0x42); }
    """)

    assert analyses.blocklets is not None
    assert analyses.blocklets.size() == 2

    for blocklet in analyses.blocklets.values():
        if isinstance(blocklet.target, AsmletId):
            assert len(blocklet.blocks) == 1
            assert blocklet.listing() == [
                "mov rdi, rax",
                "bswap rdi",
            ]


def can_detect_blocklets_of_asm_snippet_with_bits():
    _, analyses = prepare_analyses("""
        asm foo(x@rax: u8) clobbers rdi {
            and eax, 0xffffffff;
            shr rax, 0x0f;
            or   ax, 0x0042;
            ret;
        }

        fn main() { foo(0x42); }
    """)

    assert analyses.blocklets is not None
    assert analyses.blocklets.size() == 2

    for blocklet in analyses.blocklets.values():
        if isinstance(blocklet.target, AsmletId):
            assert len(blocklet.blocks) == 1
            assert blocklet.listing() == [
                "and eax, 0xffffffff",
                "shr rax, 0x0f",
                "or ax, 0x0042",
                "ret",
            ]


def can_detect_blocklets_of_asm_snippet_with_loop_to_entry():
    _, analyses = prepare_analyses("""
        asm foo(x@rcx: u8) clobbers rdi, rcx {
            .entry:
                mov rdi, rax;
                bswap rdi;
                loop @entry;
        }

        fn main() { foo(0x42); }
    """)

    assert analyses.blocklets is not None
    assert analyses.blocklets.size() == 2

    for blocklet in analyses.blocklets.values():
        if isinstance(blocklet.target, AsmletId):
            assert len(blocklet.blocks) == 1
            assert blocklet.listing() == [
                "mov rdi, rax",
                "bswap rdi",
                "loop #0",
            ]


def can_detect_blocklets_of_asm_snippet_with_loop_to_middle():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8) clobbers rdi, rcx {
                mov rcx, rdi;
            .middle:
                mov rdi, rax;
                bswap rdi;
                loop @middle;
        }

        fn main() { foo(0x42); }
    """)

    assert analyses.blocklets is not None
    assert analyses.blocklets.size() == 2

    for blocklet in analyses.blocklets.values():
        if isinstance(blocklet.target, AsmletId):
            assert len(blocklet.blocks) == 2
            assert blocklet.listing() == [
                "mov rcx, rdi",
                "mov rdi, rax",
                "bswap rdi",
                "loop #1",
            ]


def can_detect_blocklets_of_asm_snippet_with_jmp_at_the_end():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8) clobbers rdi, rcx {
                mov rcx, rdi;
                jmp @done;
            .middle:
                mov rdi, rax;
                bswap rdi;
                jmp @middle;
            .done:
                ret;
        }

        fn main() { foo(0x42); }
    """)

    assert analyses.blocklets is not None
    assert analyses.blocklets.size() == 2

    for blocklet in analyses.blocklets.values():
        if isinstance(blocklet.target, AsmletId):
            assert len(blocklet.blocks) == 3
            assert blocklet.listing() == [
                "mov rcx, rdi",
                "jmp #2",
                "mov rdi, rax",
                "bswap rdi",
                "jmp #1",
                "ret",
            ]
