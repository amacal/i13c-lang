from typing import Dict, List

from i13c.sem.infra import Configuration, OneToOne
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.instructions import Instruction, InstructionId, Mnemonic
from i13c.sem.typing.entities.operands import OperandId


def configure_instructions() -> Configuration:
    return Configuration(
        builder=build_instructions,
        produces=("entities/instructions",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_instructions(
    graph: SyntaxGraph,
) -> OneToOne[InstructionId, Instruction]:
    instructions: Dict[InstructionId, Instruction] = {}

    for nid, instruction in graph.instructions.items():
        operands: List[OperandId] = []

        # collect operand IDs from reverse mapping
        for operand in instruction.operands:
            oid = graph.operands.get_by_node(operand)
            operands.append(OperandId(value=oid.value))

        # derive instruction ID from globally unique node ID
        instruction_id = InstructionId(value=nid.value)

        # append to instructions map
        instructions[instruction_id] = Instruction(
            ref=instruction.ref,
            mnemonic=Mnemonic(name=instruction.mnemonic.name),
            operands=operands,
        )

    return OneToOne[InstructionId, Instruction].instance(instructions)
