from tests.semantic.nodes.analyses import prepare_analyses


def can_detect_cgraph_in_a_snippet():
    _, analyses = prepare_analyses("""
        asm main() { mov rax, rbx; }
    """)

    assert analyses.cgraphs is not None
    assert analyses.cgraphs.size() == 1
    _, cgraph = analyses.cgraphs.peak()

    assert len(cgraph.forward) == 0
    assert len(cgraph.backward) == 0


def can_detect_cgraph_in_empty_function():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.cgraphs is not None
    assert analyses.cgraphs.size() == 1
    _, cgraph = analyses.cgraphs.peak()

    assert len(cgraph.forward) == 0
    assert len(cgraph.backward) == 0


def can_detect_cflow_with_a_callsite():
    _, analyses = prepare_analyses("""
        asm foo() { mov rax, rbx; }
        fn main() { foo(); }
    """)

    assert analyses.cgraphs is not None
    assert analyses.cgraphs.size() == 2

    for cgraph in analyses.cgraphs.values():
        if cgraph.target.name == b"main":
            assert len(cgraph.forward) == 1
            assert len(cgraph.backward) == 0

        else:
            assert len(cgraph.forward) == 0
            assert len(cgraph.backward) == 1


def can_detect_cflow_with_multiple_callsites():
    _, analyses = prepare_analyses("""
        asm foo() { mov rax, rbx; }
        fn main() { foo(); foo(); }
    """)

    assert analyses.cgraphs is not None
    assert analyses.cgraphs.size() == 2

    for cgraph in analyses.cgraphs.values():
        if cgraph.target.name == b"main":
            assert len(cgraph.forward) == 2
            assert len(cgraph.backward) == 0

        else:
            assert len(cgraph.forward) == 0
            assert len(cgraph.backward) == 2


def can_detect_cflow_with_three_callsites():
    _, analyses = prepare_analyses("""
        asm foo() { mov rax, rbx; }
        fn bar() { foo(); }
        fn main() { foo(); bar(); }
    """)

    assert analyses.cgraphs is not None
    assert analyses.cgraphs.size() == 3

    for cgraph in analyses.cgraphs.values():
        if cgraph.target.name == b"main":
            assert len(cgraph.forward) == 2
            assert len(cgraph.backward) == 0

        elif cgraph.target.name == b"bar":
            assert len(cgraph.forward) == 1
            assert len(cgraph.backward) == 1

        else:
            assert len(cgraph.forward) == 0
            assert len(cgraph.backward) == 2
