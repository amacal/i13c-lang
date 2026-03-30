from typing import Dict, List

from i13c.core.generator import Generator
from i13c.llvm.nodes.instructions import lower_instruction
from i13c.llvm.typing.instructions import InstructionEntry
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.indices.instances import Instance


def lower_instance(
    graph: SemanticGraph,
    generator: Generator,
    target: Instance,
) -> List[InstructionEntry]:
    out: List[InstructionEntry] = []

    # values
    rewritten: Dict[OperandId, Operand] = target.operands
    instrs = graph.basic.snippets.get(target.target).instructions

    # lower all instructions
    for iid in instrs:
        instr = graph.basic.instructions.get(iid)
        out.append(lower_instruction(generator, graph.basic.operands, instr, rewritten))

    return out
