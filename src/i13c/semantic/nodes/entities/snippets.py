from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex, Identifier, Range, Type, Width, default_range
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.instructions import Binding, InstructionId
from i13c.semantic.typing.entities.operands import Register
from i13c.semantic.typing.entities.snippets import Slot, Snippet, SnippetId


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

    for nid, snippet in graph.snippets.items():
        slots: List[Slot] = []
        clobbers: List[Register] = []
        instructions: List[InstructionId] = []

        # collect clobbers
        for reg in snippet.clobbers:
            clobbers.append(Register(name=reg.name, width=64))

        # collect slots
        for slot in snippet.signature.slots:
            # default width and ranges for declared type
            range: Range = default_range(slot.type.name)

            # override ranges if specified
            if slot.type.range is not None:
                range = Range(
                    lower=Hex.derive(slot.type.range.lower.digits),
                    upper=Hex.derive(slot.type.range.upper.digits),
                )

            # derive width from ranges
            width: Width = max(range.lower.width, range.upper.width)

            # construct slot type with range or default width
            type = Type(
                name=slot.type.name,
                width=width,
                range=range,
            )

            if slot.bind.name == b"imm":
                binding = Binding.immediate()
            else:
                binding = Binding.register(name=slot.bind.name)

            slots.append(
                Slot(
                    name=Identifier(data=slot.name),
                    bind=binding,
                    type=type,
                )
            )

        for instruction in snippet.instructions:
            # identify instruction ID from globally unique node ID
            instruction_node = graph.instructions.get_by_node(instruction)
            instructions.append(InstructionId(value=instruction_node.value))

        # derive snippet ID from globally unique node ID
        snippet_id = SnippetId(value=nid.value)

        snippets[snippet_id] = Snippet(
            ref=snippet.ref,
            identifier=Identifier(data=snippet.signature.name),
            noreturn=snippet.noreturn,
            slots=slots,
            clobbers=clobbers,
            instructions=instructions,
        )

    return OneToOne[SnippetId, Snippet].instance(snippets)
