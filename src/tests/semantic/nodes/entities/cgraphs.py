from tests.semantic.nodes.entities import prepare_entities


def can_detect_cgraph_in_a_snippet():
    entities = prepare_entities(
        """
            asm main() { mov rax, rbx; }
        """
    )

    assert entities.cgraphs is not None
    assert entities.cgraphs.size() == 1
    _, cgraph = entities.cgraphs.peak()

    assert len(cgraph.forward) == 0
    assert len(cgraph.backward) == 0


def can_detect_cgraph_in_empty_function():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.cgraphs is not None
    assert entities.cgraphs.size() == 1
    _, cgraph = entities.cgraphs.peak()

    assert len(cgraph.forward) == 0
    assert len(cgraph.backward) == 0


def can_detect_cflow_with_a_callsite():
    entities = prepare_entities(
        """
            asm foo() { mov rax, rbx; }
            fn main() { foo(); }
        """
    )

    assert entities.cgraphs is not None
    assert entities.cgraphs.size() == 2

    for cgraph in entities.cgraphs.values():
        if cgraph.target.name == b"main":
            assert len(cgraph.forward) == 1
            assert len(cgraph.backward) == 0

        else:
            assert len(cgraph.forward) == 0
            assert len(cgraph.backward) == 1


def can_detect_cflow_with_multiple_callsites():
    entities = prepare_entities(
        """
            asm foo() { mov rax, rbx; }
            fn main() { foo(); foo(); }
        """
    )

    assert entities.cgraphs is not None
    assert entities.cgraphs.size() == 2

    for cgraph in entities.cgraphs.values():
        if cgraph.target.name == b"main":
            assert len(cgraph.forward) == 2
            assert len(cgraph.backward) == 0

        else:
            assert len(cgraph.forward) == 0
            assert len(cgraph.backward) == 2


def can_detect_cflow_with_three_callsites():
    entities = prepare_entities(
        """
            asm foo() { mov rax, rbx; }
            fn bar() { foo(); }
            fn main() { foo(); bar(); }
        """
    )

    assert entities.cgraphs is not None
    assert entities.cgraphs.size() == 3

    for cgraph in entities.cgraphs.values():
        if cgraph.target.name == b"main":
            assert len(cgraph.forward) == 2
            assert len(cgraph.backward) == 0

        elif cgraph.target.name == b"bar":
            assert len(cgraph.forward) == 1
            assert len(cgraph.backward) == 1

        else:
            assert len(cgraph.forward) == 0
            assert len(cgraph.backward) == 2
