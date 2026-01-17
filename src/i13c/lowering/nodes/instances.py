from typing import Dict, List

from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.instructions import lower_instruction
from i13c.lowering.typing.instructions import Instruction
from i13c.sem.typing.entities.operands import Operand, OperandId
from i13c.sem.typing.indices.instances import Instance


def lower_instance(
    ctx: LowLevelContext,
    target: Instance,
) -> List[Instruction]:
    out: List[Instruction] = []

    # values
    operands: Dict[OperandId, Operand] = target.operands
    instrs = ctx.graph.basic.snippets.get(target.target).instructions

    # lower all instructions
    for iid in instrs:
        instr = ctx.graph.basic.instructions.get(iid)
        out.append(lower_instruction(ctx.graph, instr, operands))

    return out
