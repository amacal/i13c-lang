from tests.semantic.nodes.indices import prepare_indices


def can_index_a_bind_by_slot():
    source, indices = prepare_indices(
        """
            asm main(v@rax: u8) { }
        """
    )

    assert indices.binds_by_slots is not None
    assert indices.binds_by_slots.size() == 1

    _, acceptance = indices.binds_by_slots.peak()

    assert acceptance.mode == "register"
    assert acceptance.src == b"v"
    assert acceptance.dst == b"rax"

    assert source.extract(acceptance.ref) == b"rax"


def can_ignore_binds_in_a_function():
    _, indices = prepare_indices(
        """
            fn main(x: u8) { }
        """
    )

    assert indices.binds_by_slots is not None
    assert indices.binds_by_slots.size() == 0
