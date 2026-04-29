from tests.semantic.nodes.indices import prepare_indices


def can_index_one_asmlet_by_its_signature():
    source, indices = prepare_indices(
        """
            asm foo() { mov rax, rbx; }
            fn main() { foo(); }
        """
    )

    assert indices.asmlets_by_signatures is not None
    assert indices.asmlets_by_signatures.size() == 1

    _, asmlets = indices.asmlets_by_signatures.peak()

    assert len(asmlets) == 1
    assert len(asmlets[0].instructions) == 1
    assert len(asmlets[0].parameters) == 0
    assert len(asmlets[0].binding) == 0

    assert asmlets[0].name == b"foo"
    assert source.extract(asmlets[0].ref) == b"foo()"


def can_index_two_callsite_by_called_signature():
    source, indices = prepare_indices(
        """
            asm foo() { mov rax, rbx; }
            fn main() { foo(); foo(); }
        """
    )

    assert indices.asmlets_by_signatures is not None
    assert indices.asmlets_by_signatures.size() == 1

    _, asmlets = indices.asmlets_by_signatures.peak()

    assert len(asmlets) == 1
    assert len(asmlets[0].instructions) == 1
    assert len(asmlets[0].parameters) == 0
    assert len(asmlets[0].binding) == 0

    assert asmlets[0].name == b"foo"
    assert source.extract(asmlets[0].ref) == b"foo()"


def can_index_immediate_callsite_by_called_signature():
    source, indices = prepare_indices(
        """
            asm foo(v@imm: u16) { mov rax, @v; }
            fn main() { foo(0x0000); foo(0x0001); }
        """
    )

    assert indices.asmlets_by_signatures is not None
    assert indices.asmlets_by_signatures.size() == 1

    _, asmlets = indices.asmlets_by_signatures.peak()

    assert len(asmlets) == 2

    for entry in asmlets:
        assert len(entry.parameters) == 0
        assert len(entry.binding) == 0
        assert len(entry.instructions) == 1

        assert entry.name == b"foo"
        assert source.extract(entry.ref) == b"foo(v@imm: u16)"
