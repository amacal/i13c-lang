from typing import Dict, List

from i13c.sem.core import Identifier, Type, default_ranges, default_width
from i13c.sem.infra import Configuration, OneToOne
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.instructions import Binding, InstructionId
from i13c.sem.typing.entities.operands import Register
from i13c.sem.typing.entities.snippets import Slot, Snippet, SnippetId


def configure_snippets() -> Configuration:
    return Configuration(
        builder=build_snippets,
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
            clobbers.append(Register(name=reg.name))

        # collect slots
        for slot in snippet.slots:
            # default width and ranges for declared type
            width = default_width(slot.type.name)
            ranges = default_ranges(slot.type.name)

            # construct slot type with range or default width
            type = Type(
                name=slot.type.name,
                width=width,
                lower=slot.type.range.lower if slot.type.range else ranges[0],
                upper=slot.type.range.upper if slot.type.range else ranges[1],
            )

            if slot.bind.name == b"imm":
                binding = Binding.immediate()
            else:
                binding = Binding.register(name=slot.bind.name)

            slots.append(
                Slot(
                    name=Identifier(name=slot.name),
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
            identifier=Identifier(name=snippet.name),
            noreturn=snippet.noreturn,
            slots=slots,
            clobbers=clobbers,
            instructions=instructions,
        )

    return OneToOne[SnippetId, Snippet].instance(snippets)
