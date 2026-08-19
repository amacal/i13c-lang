from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_entrypoint_from_a_snippet():
    _, analyses = prepare_analyses("""
        asm main() noreturn { mov rax, rbx; }
    """)

    assert analyses.entrypoints is not None
    assert analyses.entrypoints.size() == 1
    _, value = analyses.entrypoints.peek()

    assert value.target.signature.name == b"main"


def can_detect_entrypoint_from_a_function():
    _, analyses = prepare_analyses("""
        asm exit() noreturn { }
        fn main() noreturn { exit(); }
    """)

    assert analyses.entrypoints is not None
    assert analyses.entrypoints.size() == 1
    _, value = analyses.entrypoints.peek()

    assert value.target.signature.name == b"main"


def can_reject_entrypoint_from_a_snippet_without_noreturn():
    _, analyses = prepare_analyses("""
        asm main() { mov rax, rbx; }
    """)

    assert analyses.entrypoints is not None
    assert analyses.entrypoints.size() == 0


def can_reject_entrypoint_from_a_snippet_with_parameters():
    _, analyses = prepare_analyses("""
        asm main(x@rbx: u8) noreturn { mov rax, rbx; }
    """)

    assert analyses.entrypoints is not None
    assert analyses.entrypoints.size() == 0


def can_reject_entrypoint_from_a_function_without_noreturn():
    _, analyses = prepare_analyses("""
        asm exit() { }
        fn main() { exit(); }
    """)

    assert analyses.entrypoints is not None
    assert analyses.entrypoints.size() == 0


def can_reject_entrypoint_from_a_function_with_parameters():
    _, analyses = prepare_analyses("""
        asm exit() noreturn { }
        fn main(x: u8) noreturn { exit(); }
    """)

    assert analyses.entrypoints is not None
    assert analyses.entrypoints.size() == 0
