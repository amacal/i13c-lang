from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.references import Reference, ReferenceId
from i13c.semantic.typing.entities.snippets import SnippetId


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

        # look up for the snippet context of this reference
        snippet = graph.references.get_ctx(id)
        nid = graph.snippets.get_by_node(snippet)
        snippet_id = SnippetId(value=nid.value)

        references[reference_id] = Reference(
            ref=entry.ref,
            name=entry.name,
            ctx=snippet_id,
        )

    return OneToOne[ReferenceId, Reference].instance(references)
