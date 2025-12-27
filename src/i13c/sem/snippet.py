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

    for nid, snippet in graph.nodes.snippets.items():
        slots: List[Slot] = []
        clobbers: List[Register] = []
        instructions: List[InstructionId] = []

        # derive snippet ID from globally unique node ID
        id = SnippetId(value=nid.value)

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
            # derive instruction ID from globally unique node ID
            node = graph.nodes.instructions.get_by_node(instruction)
            instructions.append(InstructionId(value=node.value))

        snippets[id] = Snippet(
            ref=snippet.ref,
            identifier=Identifier(name=snippet.name),
            noreturn=snippet.noreturn,
            slots=slots,
            clobbers=clobbers,
            instructions=instructions,
        )

    return snippets
