from tests.semantic.nodes.entities import prepare_entities


def can_detect_a_snippet_flags_noreturn_true():
    entities = prepare_entities("""
        asm main() noreturn { mov rax, rbx; }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 1
    _, value = entities.noreturns.peak()

    assert value.outcome is True
    assert len(value.path) == 0


def can_detect_a_snippet_flags_noreturn_false():
    entities = prepare_entities("""
        asm main() { mov rax, rbx; }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 1
    _, value = entities.noreturns.peak()

    assert value.outcome is False
    assert len(value.path) == 0


def can_detect_a_function_noreturn_false():
    entities = prepare_entities("""
        fn main() { }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 1
    _, value = entities.noreturns.peak()

    assert value.outcome is False
    assert len(value.path) == 0


def can_detect_a_function_noreturn_false_even_with_noreturn_flag():
    entities = prepare_entities("""
        fn main() noreturn { }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 1
    _, value = entities.noreturns.peak()

    assert value.outcome is False
    assert len(value.path) == 0


def can_detect_a_function_noreturn_true_when_called_noreturn_callsite():
    entities = prepare_entities("""
        asm exit() noreturn { }
        fn main() { exit(); }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 2

    for entry in entities.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 2

            assert entry.path[0].name == b"main"
            assert entry.path[1].name == b"exit"


def can_detect_a_function_noreturn_false_when_called_return_callsite():
    entities = prepare_entities("""
        asm exit() { }
        fn main() { exit(); }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 2

    for entry in entities.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is False
            assert len(entry.path) == 0


def can_detect_a_function_noreturn_true_due_to_first_callsite():
    entities = prepare_entities("""
        asm foo() noreturn { }
        asm bar() { }
        fn main() { foo(); bar(); }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 3

    for entry in entities.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 2

            assert entry.path[0].name == b"main"
            assert entry.path[1].name == b"foo"


def can_detect_a_function_noreturn_true_due_to_second_callsite():
    entities = prepare_entities("""
        asm foo() { }
        asm bar() noreturn{ }
        fn main() { foo(); bar(); }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 3

    for entry in entities.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 2

            assert entry.path[0].name == b"main"
            assert entry.path[1].name == b"bar"


def can_detect_a_function_noreturn_true_forward():
    entities = prepare_entities("""
        fn main() { foo(); bar(); }
        asm bar() noreturn{ }
        asm foo() { }
    """)

    assert entities.noreturns is not None
    assert entities.noreturns.size() == 3

    for entry in entities.noreturns.values():
        if entry.signature.name == b"main":
            assert entry.outcome is True
            assert len(entry.path) == 2

            assert entry.path[0].name == b"main"
            assert entry.path[1].name == b"bar"


def can_handle_a_missing_callsite():
    entities = prepare_entities("""
        asm foo() { }
        fn main() { foo(); bar(); }
    """)

    assert entities.noreturns is None
