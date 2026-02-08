from typing import Tuple

from i13c.core.dag import GraphNode, evaluate


def can_evaluate_one_node_without_dependencies():
    node: GraphNode = GraphNode(
        builder=lambda: 42,
        produces=("abc",),
        requires=frozenset(),
    )

    artifacts = evaluate([node], initial={})

    assert len(artifacts) == 1
    assert artifacts["abc"] == 42


def can_evaluate_multiple_nodes_with_dependencies():
    node1: GraphNode = GraphNode(
        builder=lambda: 42,
        produces=("abc",),
        requires=frozenset(),
    )

    def consume(x: int) -> int:
        return x + 1

    node2: GraphNode = GraphNode(
        builder=consume,
        produces=("cde",),
        requires=frozenset({("x", "abc")}),
    )

    artifacts = evaluate([node1, node2], initial={})

    assert len(artifacts) == 2
    assert artifacts["abc"] == 42
    assert artifacts["cde"] == 43


def can_produce_multiple_artifacts():
    def produce_multiple() -> Tuple[int, str]:
        return 42, "hello"

    node: GraphNode = GraphNode(
        builder=produce_multiple,
        produces=("abc", "cde"),
        requires=frozenset(),
    )

    artifacts = evaluate([node], initial={})

    assert len(artifacts) == 2
    assert artifacts["abc"] == 42
    assert artifacts["cde"] == "hello"


def can_consume_multiple_artifacts():
    node1: GraphNode = GraphNode(
        builder=lambda: 42,
        produces=("abc",),
        requires=frozenset(),
    )

    node2: GraphNode = GraphNode(
        builder=lambda: "world",
        produces=("cde",),
        requires=frozenset(),
    )

    def consume_multiple(x: int, y: str) -> str:
        return f"{x} {y}"

    node3: GraphNode = GraphNode(
        builder=consume_multiple,
        produces=("efg",),
        requires=frozenset({("x", "abc"), ("y", "cde")}),
    )

    artifacts = evaluate([node1, node2, node3], initial={})

    assert len(artifacts) == 3
    assert artifacts["abc"] == 42
    assert artifacts["cde"] == "world"
    assert artifacts["efg"] == "42 world"


def can_use_initial_artifacts():
    def consume_initial(x: int) -> int:
        return x + 1

    node: GraphNode = GraphNode(
        builder=consume_initial,
        produces=("abc",),
        requires=frozenset({("x", "x")}),
    )

    artifacts = evaluate([node], initial={"x": 41})

    assert len(artifacts) == 2
    assert artifacts["x"] == 41
    assert artifacts["abc"] == 42
