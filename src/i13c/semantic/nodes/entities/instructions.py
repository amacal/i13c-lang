from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.mnemonics import MnemonicId
from i13c.semantic.typing.entities.operands import OperandId


def configure_instructions() -> GraphNode:
    return GraphNode(
        builder=build_instructions,
        constraint=None,
        produces=("entities/instructions",),
        requires=frozenset({("graph", "syntax/graph")}),
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
