from typing import Dict, List

from i13c.lowering.nodes.instructions import lower_instruction
from i13c.lowering.typing.instructions import Instruction
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.indices.instances import Instance


def lower_instance(
    graph: SemanticGraph,
    target: Instance,
) -> List[Instruction]:
    out: List[Instruction] = []

    # values
    operands: Dict[OperandId, Operand] = target.operands
    instrs = graph.basic.snippets.get(target.target).instructions

    # lower all instructions
    for iid in instrs:
        instr = graph.basic.instructions.get(iid)
        out.append(lower_instruction(graph, instr, operands))

    return out
