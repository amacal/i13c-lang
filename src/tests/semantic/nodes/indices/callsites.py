from tests.semantic.nodes.indices import prepare_indices


def can_index_one_callsite_by_called_signature():
    source, indices = prepare_indices(
        """
            asm foo() { mov rax, rbx; }
            fn main() { foo(); }
        """
    )

    assert indices.callsites_by_signatures is not None
    assert indices.callsites_by_signatures.size() == 1

    _, acceptance = indices.callsites_by_signatures.peak()

    assert len(acceptance) == 1
    assert len(acceptance[0].arguments) == 0

    assert acceptance[0].signature.name == b"foo"
    assert source.extract(acceptance[0].ref) == b"foo()"


def can_index_two_callsite_by_called_signature():
    source, indices = prepare_indices(
        """
            asm foo() { mov rax, rbx; }
            fn main() { foo(); foo(); }
        """
    )

    assert indices.callsites_by_signatures is not None
    assert indices.callsites_by_signatures.size() == 1

    _, acceptance = indices.callsites_by_signatures.peak()

    assert len(acceptance) == 2

    for entry in acceptance:
        assert len(entry.arguments) == 0
        assert entry.signature.name == b"foo"
        assert source.extract(entry.ref) == b"foo()"


def can_index_immediate_callsite_by_called_signature():
    source, indices = prepare_indices(
        """
            asm foo(v@imm: u16) { mov rax, @v; }
            fn main() { foo(0x0000); foo(0x0001); }
        """
    )

    assert indices.callsites_by_signatures is not None
    assert indices.callsites_by_signatures.size() == 1

    _, acceptance = indices.callsites_by_signatures.peak()

    assert len(acceptance) == 2

    for entry in acceptance:
        assert len(entry.arguments) == 1
        assert entry.signature.name == b"foo"
        assert source.extract(entry.ref) in (b"foo(0x0000)", b"foo(0x0001)")
