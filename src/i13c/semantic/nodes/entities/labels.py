from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.labels import Label, LabelId


def configure_labels() -> GraphNode:
    return GraphNode(
        builder=build_labels,
        constraint=None,
        produces=("entities/labels",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_labels(
    graph: SyntaxGraph,
) -> OneToOne[LabelId, Label]:
    labels: Dict[LabelId, Label] = {}

    for id, entry in graph.labels.items():
        # derive label ID from globally unique node ID
        label_id = LabelId(value=id.value)

        labels[label_id] = Label(
            ref=entry.ref,
            name=entry.name,
        )

    return OneToOne[LabelId, Label].instance(labels)
