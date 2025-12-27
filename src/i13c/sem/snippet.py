from dataclasses import dataclass
from typing import Dict, List

from i13c import ast
from i13c.sem.asm import Instruction, InstructionId, Mnemonic, Operand, Register
from i13c.sem.core import Identifier, Type
from i13c.sem.syntax import SyntaxGraph


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
    identifier: Identifier
    noreturn: bool
    slots: List[Slot]
    instructions: List[Instruction]


def build_snippets(graph: SyntaxGraph) -> Dict[SnippetId, Snippet]:
    snippets: Dict[SnippetId, Snippet] = {}

    for nid, snippet in graph.nodes.snippets.items():
        slots: List[Slot] = []
        instructions: List[Instruction] = []

        # derive snippet ID from globally unique node ID
        id = SnippetId(value=nid.value)

        for slot in snippet.slots:
            slots.append(
                Slot(
                    name=Identifier(name=slot.name),
                    type=Type(name=slot.type.name),
                    bind=Register(name=slot.bind.name),
                )
            )

        for instruction in snippet.instructions:
            operands: List[Operand] = []

            for operand in instruction.operands:
                match operand:
                    case ast.Register() as reg:
                        operands.append(Operand.register(name=reg.name))
                    case ast.Immediate() as imm:
                        operands.append(Operand.immediate(value=imm.value))

            # derive instruction ID from globally unique node ID
            node = graph.nodes.instructions.get_by_node(instruction)
            iid = InstructionId(value=node.value)

            instructions.append(
                Instruction(
                    id=iid,
                    ref=instruction.ref,
                    mnemonic=Mnemonic(name=instruction.mnemonic.name),
                    operands=operands,
                )
            )

        snippets[id] = Snippet(
            identifier=Identifier(name=snippet.name),
            noreturn=snippet.noreturn,
            slots=slots,
            instructions=instructions,
        )

    return snippets
