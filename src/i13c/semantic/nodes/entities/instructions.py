from typing import Dict, Iterable, List, Tuple

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.mnemonics import MnemonicId
from i13c.semantic.typing.entities.operands import OperandId
from i13c.semantic.typing.entities.snippets import SnippetId


def configure_instructions() -> GraphNode:
    return GraphNode(
        builder=build_instructions,
        constraint=None,
        produces=("entities/instructions",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_instructions(
    graph: SyntaxGraph,
) -> OneToOne[InstructionId, Instruction]:
    instructions: Dict[InstructionId, Instruction] = {}

    for nid, instruction in graph.snippet.instructions.items():
        operands: List[OperandId] = []

        # collect operand IDs from reverse mapping
        for operand in instruction.operands:
            oid = graph.snippet.operands.get_by_node(operand)
            operands.append(OperandId(value=oid.value))

        # derive instruction ID from globally unique node ID
        instruction_id = InstructionId(value=nid.value)

        # derive mnemonic ID from globally unique node ID
        oid = graph.snippet.mnemonics.get_by_node(instruction.mnemonic)
        mnemonic_id = MnemonicId(value=oid.value)

        # derive snippet ID from globally unique node ID
        snippet = graph.snippet.instructions.get_ctx(nid)
        snipept_nid = graph.snippet.snippets.get_by_node(snippet)

        # append to instructions map
        instructions[instruction_id] = Instruction(
            ref=instruction.ref,
            snippet=snipept_nid,
            mnemonic=mnemonic_id,
            operands=operands,
        )

    return OneToOne[InstructionId, Instruction].instance(instructions)


class ListExtractor:
    def __init__(self, data: OneToOne[InstructionId, Instruction]):
        self.data = data

    def extract(self) -> Iterable[Tuple[InstructionId, Instruction]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "mnemonic": "Mnemonic",
            "operands": "Operands",
            "snippet": "Snippet",
        }

    @staticmethod
    def rows(key: InstructionId, entry: Instruction) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "mnemonic": entry.mnemonic.identify(1),
            "operands": str(len(entry.operands)),
            "snippet": entry.get_snippet(SnippetId.from_context).identify(1),
        }
