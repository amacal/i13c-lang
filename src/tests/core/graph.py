from typing import Dict, Tuple

from pytest import raises

from i13c.core.graph import (
    CyclicDependencyError,
    DuplicateArtifactError,
    GraphGroup,
    GraphNode,
    InvalidDatasetArityError,
    MissingArtifactProducerError,
    MissingPrefixProducerError,
    Prefix,
    evaluate,
)


def can_evaluate_one_node_without_dependencies():
    node: GraphNode = GraphNode(
        builder=lambda: 42,
        constraint=None,
        produces=("abc",),
        requires=frozenset(),
    )

    artifacts = evaluate([node], initial={})

    assert len(artifacts) == 1
    assert artifacts["abc"] == 42


def can_evaluate_multiple_nodes_with_dependencies():
    node1: GraphNode = GraphNode(
        builder=lambda: 42,
        constraint=None,
        produces=("abc",),
        requires=frozenset(),
    )

    def consume(x: int) -> int:
        return x + 1

    node2: GraphNode = GraphNode(
        builder=consume,
        constraint=None,
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
        constraint=None,
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
        constraint=None,
        produces=("abc",),
        requires=frozenset(),
    )

    node2: GraphNode = GraphNode(
        builder=lambda: "world",
        constraint=None,
        produces=("cde",),
        requires=frozenset(),
    )

    def consume_multiple(x: int, y: str) -> str:
        return f"{x} {y}"

    node3: GraphNode = GraphNode(
        builder=consume_multiple,
        constraint=None,
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
        constraint=None,
        produces=("abc",),
        requires=frozenset({("x", "x")}),
    )

    artifacts = evaluate([node], initial={"x": 41})

    assert len(artifacts) == 2
    assert artifacts["x"] == 41
    assert artifacts["abc"] == 42


def can_evaluate_group():
    node1: GraphNode = GraphNode(
        builder=lambda: 42,
        constraint=None,
        produces=("abc",),
        requires=frozenset(),
    )

    def consume(x: int) -> int:
        return x + 1

    node2: GraphNode = GraphNode(
        builder=consume,
        constraint=None,
        produces=("cde",),
        requires=frozenset({("x", "abc")}),
    )

    group: GraphGroup = GraphGroup(nodes=[node1, node2])
    artifacts = evaluate(group.flatten(), initial={})

    assert len(artifacts) == 2
    assert artifacts["abc"] == 42
    assert artifacts["cde"] == 43


def can_consume_prefix_from_single_multi_producer():
    def produce_entities():
        return 1, 2, 3

    producer = GraphNode(
        builder=produce_entities,
        constraint=None,
        produces=(
            "entities/a",
            "entities/b",
            "entities/c",
        ),
        requires=frozenset(),
    )

    def consume_entities(entities: Dict[str, int]) -> int:
        # Prefix should give all artifacts at once
        return sum(entities.values())

    consumer = GraphNode(
        builder=consume_entities,
        constraint=None,
        produces=("result",),
        requires=frozenset(
            {
                ("entities", Prefix(value="entities/")),
            }
        ),
    )

    artifacts = evaluate([producer, consumer], initial={})

    assert artifacts["entities/a"] == 1
    assert artifacts["entities/b"] == 2
    assert artifacts["entities/c"] == 3
    assert artifacts["result"] == 6


def can_evaluate_without_mutating_input_nodes_list():
    node: GraphNode = GraphNode(
        builder=lambda: 42,
        constraint=None,
        produces=("abc",),
        requires=frozenset(),
    )

    nodes = [node]
    artifacts = evaluate(nodes, initial={"x": 41})

    assert artifacts["x"] == 41
    assert artifacts["abc"] == 42
    assert len(nodes) == 1
    assert nodes[0] is node


def can_detect_cyclic_dependencies():
    def build(x: int) -> int:
        return x + 1

    node1: GraphNode = GraphNode(
        builder=build,
        constraint=None,
        produces=("abc",),
        requires=frozenset({("x", "cde")}),
    )

    node2: GraphNode = GraphNode(
        builder=build,
        constraint=None,
        produces=("cde",),
        requires=frozenset({("x", "abc")}),
    )

    with raises(CyclicDependencyError) as error:
        evaluate([node1, node2], initial={})

    assert isinstance(error.value, CyclicDependencyError)


def can_reject_multiple_nodes_producing_same_artifact():
    node1: GraphNode = GraphNode(
        builder=lambda: 1,
        constraint=None,
        produces=("abc",),
        requires=frozenset(),
    )
    node2: GraphNode = GraphNode(
        builder=lambda: 2,
        constraint=None,
        produces=("abc",),
        requires=frozenset(),
    )

    with raises(DuplicateArtifactError) as error:
        evaluate([node1, node2], initial={})

    assert isinstance(error.value, DuplicateArtifactError)
    assert error.value.artifact == "abc"
    assert set(error.value.producers) == {node1, node2}


def can_reject_single_node_producing_duplicate_artifacts():
    node: GraphNode = GraphNode(
        builder=lambda: 42,
        constraint=None,
        produces=("abc", "abc"),
        requires=frozenset(),
    )

    with raises(DuplicateArtifactError) as error:
        evaluate([node], initial={})

    assert isinstance(error.value, DuplicateArtifactError)
    assert error.value.artifact == "abc"
    assert set(error.value.producers) == {node}


def can_reject_missing_prefix_dependency():
    def build(entities: Dict[str, int]) -> int:
        return len(entities)

    consumer = GraphNode(
        builder=build,
        constraint=None,
        produces=("result",),
        requires=frozenset(
            {
                ("entities", Prefix(value="entities/")),
            }
        ),
    )

    with raises(MissingPrefixProducerError) as error:
        evaluate([consumer], initial={})

    assert isinstance(error.value, MissingPrefixProducerError)
    assert error.value.prefix.value == "entities/"


def can_not_consume_prefix_if_no_prefix_artifacts_were_produced():
    def build(entities: Dict[str, int]) -> int:
        return len(entities)

    producer = GraphNode(
        builder=lambda: 1,
        constraint=lambda: False,
        produces=("entities/a",),
        requires=frozenset(),
    )

    consumer = GraphNode(
        builder=build,
        constraint=None,
        produces=("result",),
        requires=frozenset(
            {
                ("entities", Prefix(value="entities/")),
            }
        ),
    )

    # producer didn't produce any artifacts, so consumer should be skipped
    assert evaluate([producer, consumer], initial={}) == {}


def can_reject_missing_artifact_dependency():
    def build(x: int) -> int:
        return x

    consumer = GraphNode(
        builder=build,
        constraint=None,
        produces=("result",),
        requires=frozenset({("value", "entities/a")}),
    )

    with raises(MissingArtifactProducerError) as error:
        evaluate([consumer], initial={})

    assert isinstance(error.value, MissingArtifactProducerError)
    assert error.value.artifact == "entities/a"
    assert error.value.node is consumer


def can_reject_multi_artifact_node_returning_non_tuple():
    node: GraphNode = GraphNode(
        builder=lambda: 42,
        constraint=None,
        produces=("abc", "cde"),
        requires=frozenset(),
    )

    with raises(InvalidDatasetArityError) as error:
        evaluate([node], initial={})

    assert isinstance(error.value, InvalidDatasetArityError)
    assert error.value.node is node
    assert error.value.expected == 2
    assert error.value.actual == 1


def can_reject_multi_artifact_node_returning_wrong_tuple_arity():
    node: GraphNode = GraphNode(
        builder=lambda: (42,),
        constraint=None,
        produces=("abc", "cde"),
        requires=frozenset(),
    )

    with raises(InvalidDatasetArityError) as error:
        evaluate([node], initial={})

    assert isinstance(error.value, InvalidDatasetArityError)
    assert error.value.node is node
    assert error.value.expected == 2
    assert error.value.actual == 1
