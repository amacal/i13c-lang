from typing import Dict, Iterable, Tuple

from i13c.core.graph import GraphNode, GraphViews
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
        views=GraphViews(list=ListExtractor),
    )


def build_references(
    graph: SyntaxGraph,
) -> OneToOne[ReferenceId, Reference]:
    references: Dict[ReferenceId, Reference] = {}

    for id, entry in graph.snippet.references.items():
        # derive reference ID from globally unique node ID
        reference_id = ReferenceId(value=id.value)

        # look up for the snippet context of this reference
        snippet = graph.snippet.references.get_ctx(id)
        snid = graph.snippet.snippets.get_by_node(snippet)

        references[reference_id] = Reference(
            ref=entry.ref,
            name=entry.name,
            snippet=snid,
        )

    return OneToOne[ReferenceId, Reference].instance(references)


class ListExtractor:
    def __init__(self, data: OneToOne[ReferenceId, Reference]):
        self.data = data

    def extract(self) -> Iterable[Tuple[ReferenceId, Reference]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "snippet": "Snippet",
        }

    @staticmethod
    def rows(key: ReferenceId, entry: Reference) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "snippet": entry.get_snippet(SnippetId.from_context).identify(1),
        }
