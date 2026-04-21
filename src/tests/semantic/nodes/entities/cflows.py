from i13c.semantic.typing.entities.cflows import FlowEntry, FlowExit, FlowNode
from tests.semantic.nodes.entities import prepare_entities


def can_detect_cflow_in_empty_function():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.cflows.size() == 1
    _, cflows = entities.cflows.peak()

    assert len(cflows.nodes) == 2
    assert len(cflows.forward) == 1
    assert len(cflows.backward) == 1

    assert isinstance(cflows.nodes[0], FlowEntry)
    assert isinstance(cflows.nodes[1], FlowExit)

    assert 0 in cflows.forward
    assert len(cflows.forward[0]) == 1
    assert cflows.forward[0][0] == 1

    assert 1 in cflows.backward
    assert len(cflows.backward[1]) == 1
    assert cflows.backward[1][0] == 0


def can_detect_cflow_with_a_callsite():
    entities = prepare_entities(
        """
            fn main() { foo(0x42); }
        """
    )

    assert entities.cflows.size() == 1
    _, cflows = entities.cflows.peak()

    assert len(cflows.nodes) == 3
    assert len(cflows.forward) == 2
    assert len(cflows.backward) == 2

    assert isinstance(cflows.nodes[0], FlowEntry)
    assert isinstance(cflows.nodes[1], FlowNode)
    assert isinstance(cflows.nodes[2], FlowExit)

    assert 0 in cflows.forward
    assert len(cflows.forward[0]) == 1
    assert cflows.forward[0][0] == 1

    assert 1 in cflows.forward
    assert len(cflows.forward[1]) == 1
    assert cflows.forward[1][0] == 2

    assert 2 in cflows.backward
    assert len(cflows.backward[2]) == 1
    assert cflows.backward[2][0] == 1

    assert 1 in cflows.backward
    assert len(cflows.backward[1]) == 1
    assert cflows.backward[1][0] == 0
