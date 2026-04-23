from tests.semantic.nodes.indices import prepare_indices


def can_index_value_by_its_statement():
    source, indices = prepare_indices(
        """
            fn main() { val x: u8 = 0x42; }
        """
    )

    assert indices.values_by_statements is not None
    assert indices.values_by_statements.size() == 1

    _, acceptance = indices.values_by_statements.peak()

    assert len(acceptance) == 1
    assert acceptance[0].name == b"x"
    assert acceptance[0].type.name == b"u8"
    assert acceptance[0].type.width == 8

    assert source.extract(acceptance[0].ref) == b"x: u8"
