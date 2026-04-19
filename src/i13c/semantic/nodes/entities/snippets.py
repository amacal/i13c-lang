from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.syntax import tree


def configure_snippets() -> GraphNode:
    return GraphNode(
        builder=build_snippets,
        constraint=None,
        produces=("entities/snippets",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_snippets(
    graph: SyntaxGraph,
) -> OneToOne[SnippetId, Snippet]:
    snippets: Dict[SnippetId, Snippet] = {}

    for nid, node in graph.snippet.snippets.items():
        # derive snippet ID from globally unique node ID
        snippet_id = SnippetId(value=nid.value)
        instructions: List[InstructionId] = []

        # identify signature ID from globally unique node ID
        nid = graph.snippet.signatures.get_by_node(node.signature)
        signature_id = SignatureId(value=nid.value)

        # identify flags ID from globally unique node ID
        if node.flags is not None:
            nid = graph.snippet.flags.get_by_node(node.flags)
            flags_id = FlagsId(value=nid.value)
        else:
            flags_id = None

        for instruction in node.body:
            if isinstance(instruction, tree.snippet.Instruction):
                # identify instruction ID from globally unique node ID
                instruction_node = graph.snippet.instructions.get_by_node(instruction)
                instructions.append(InstructionId(value=instruction_node.value))

        snippets[snippet_id] = Snippet(
            ref=node.ref,
            flags=flags_id,
            signature=signature_id,
            instructions=instructions,
        )

    return OneToOne[SnippetId, Snippet].instance(snippets)
