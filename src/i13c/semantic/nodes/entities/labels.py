from typing import Dict, Iterable, Tuple

from i13c.core.graph import AbstractListExtractor, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.labels import (
    EndOfSnippet,
    Label,
    LabelId,
    LabelTarget,
)
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId


def configure_labels() -> GraphNode:
    return GraphNode(
        builder=build_labels,
        constraint=None,
        produces=("entities/labels",),
        requires=frozenset(
            {
                ("graph", "syntax/graph"),
                ("snippets", "entities/snippets"),
            }
        ),
        views=GraphViews(list=list_labels),
    )


def build_labels(
    graph: SyntaxGraph,
    snippets: OneToOne[SnippetId, Snippet],
) -> OneToOne[LabelId, Label]:
    labels: Dict[LabelId, Label] = {}

    for id, entry in graph.snippet.labels.items():
        # derive label ID from globally unique node ID
        label_id = LabelId(value=id.value)

        snippet = graph.snippet.labels.get_ctx(id)
        snipept_nid = graph.snippet.snippets.get_by_node(snippet)
        snippet_id = SnippetId(value=snipept_nid.value)

        index, idx = -1, 0
        instruction: LabelTarget = EndOfSnippet()

        for iid in snippets.get(snippet_id).body:
            if isinstance(iid, InstructionId):
                idx += 1

            if iid == label_id:
                index = idx

            elif index >= 0 and isinstance(iid, InstructionId):
                instruction = iid
                break

        labels[label_id] = Label(
            ref=entry.ref,
            name=entry.name,
            snippet=snipept_nid,
            target=instruction,
            index=index,
        )

    return OneToOne[LabelId, Label].instance(labels)


class ListExtractor:
    def __init__(self, data: OneToOne[LabelId, Label]):
        self.data = data

    def extract(self) -> Iterable[Tuple[LabelId, Label]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "idx": "Index",
            "name": "Name",
            "target": "Target",
            "snippet": "Snippet",
        }

    @staticmethod
    def rows(key: LabelId, entry: Label) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "idx": str(entry.index),
            "name": entry.name.decode(),
            "target": entry.target.identify(1),
            "snippet": entry.get_snippet(SnippetId.from_context).identify(1),
        }


def list_labels(
    data: OneToOne[LabelId, Label],
) -> AbstractListExtractor[LabelId, Label]:
    return ListExtractor(data)
