from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.references import Reference, ReferenceId


def configure_references() -> GraphNode:
    return GraphNode(
        builder=build_references,
        constraint=None,
        produces=("entities/references",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_references(
    graph: SyntaxGraph,
) -> OneToOne[ReferenceId, Reference]:
    references: Dict[ReferenceId, Reference] = {}

    for id, entry in graph.references.items():
        # derive reference ID from globally unique node ID
        reference_id = ReferenceId(value=id.value)

        references[reference_id] = Reference(
            ref=entry.ref,
            name=entry.name,
        )

    return OneToOne[ReferenceId, Reference].instance(references)
