from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_a_snippet_flags_noreturn_true():
    _, analyses = prepare_analyses("""
        asm main() noreturn { mov rax, rbx; }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 1
    _, value = analyses.noreturns.peak()

    assert value.outcome is True
    assert len(value.path) == 0


def can_detect_a_snippet_flags_noreturn_false():
    _, analyses = prepare_analyses("""
        asm main() { mov rax, rbx; }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 1
    _, value = analyses.noreturns.peak()

    assert value.outcome is False
    assert len(value.path) == 0


def can_detect_a_function_noreturn_false():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 1
    _, value = analyses.noreturns.peak()

    assert value.outcome is False
    assert len(value.path) == 0


def can_detect_a_function_noreturn_false_even_with_noreturn_flag():
    _, analyses = prepare_analyses("""
        fn main() noreturn { }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 1
    _, value = analyses.noreturns.peak()

    assert value.outcome is False
    assert len(value.path) == 0


def can_detect_a_function_noreturn_true_when_called_noreturn_callsite():
    _, analyses = prepare_analyses("""
        asm exit() noreturn { }
        fn main() { exit(); }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 2

    for entry in analyses.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 1

            assert entry.path[0].name == b"exit"


def can_detect_a_function_noreturn_false_when_called_return_callsite():
    _, analyses = prepare_analyses("""
        asm exit() { }
        fn main() { exit(); }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 2

    for entry in analyses.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is False
            assert len(entry.path) == 0


def can_detect_a_function_noreturn_true_due_to_first_callsite():
    _, analyses = prepare_analyses("""
        asm foo() noreturn { }
        asm bar() { }
        fn main() { foo(); bar(); }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 3

    for entry in analyses.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 1

            assert entry.path[0].name == b"foo"


def can_detect_a_function_noreturn_true_due_to_second_callsite():
    _, analyses = prepare_analyses("""
        asm foo() { }
        asm bar() noreturn{ }
        fn main() { foo(); bar(); }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 3

    for entry in analyses.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 1

            assert entry.path[0].name == b"bar"


def can_detect_a_function_noreturn_true_forward():
    _, analyses = prepare_analyses("""
        fn main() { foo(); bar(); }
        asm bar() noreturn{ }
        asm foo() { }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 3

    for entry in analyses.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 1

            assert entry.path[0].name == b"bar"


def can_detect_a_function_noreturn_true_long_path():
    _, analyses = prepare_analyses("""
        fn main() { foo(); }
        fn foo() { bar(); }
        asm bar() noreturn { }
    """)

    assert analyses.noreturns is not None
    assert analyses.noreturns.size() == 3

    for entry in analyses.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 2

            assert entry.path[0].name == b"foo"
            assert entry.path[1].name == b"bar"


def can_handle_a_missing_callsite():
    _, analyses = prepare_analyses("""
        asm foo() { }
        fn main() { foo(); bar(); }
    """)

    assert analyses.noreturns is None
