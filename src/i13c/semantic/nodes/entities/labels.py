from typing import Dict

from i13c.core.graph import GraphNode
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
