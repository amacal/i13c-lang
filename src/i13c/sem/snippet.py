from dataclasses import dataclass
from typing import Dict, List

from i13c.sem.asm import InstructionId, Register
from i13c.sem.core import Identifier, Type
from i13c.sem.syntax import SyntaxGraph
from i13c.src import Span


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int


@dataclass(kw_only=True)
class Slot:
    name: Identifier
    type: Type
    bind: Register


@dataclass(kw_only=True)
class Snippet:
    ref: Span
    identifier: Identifier
    noreturn: bool
    slots: List[Slot]
    clobbers: List[Register]
    instructions: List[InstructionId]


def build_snippets(graph: SyntaxGraph) -> Dict[SnippetId, Snippet]:
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
            slots.append(
                Slot(
                    name=Identifier(name=slot.name),
                    type=Type(name=slot.type.name),
                    bind=Register(name=slot.bind.name),
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

    return snippets
