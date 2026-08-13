
from i13c.core.generator import Generator
from i13c.llvm.typing.instructions import InstructionEntry
from i13c.semantic.model import SemanticGraph


def lower_instance(
    graph: SemanticGraph,
    generator: Generator,
    target: None,
) -> list[InstructionEntry]:
    out: list[InstructionEntry] = []

    # # values
    # rewritten: Dict[OperandId, Operand] = target.operands
    # instrs = graph.entities.snippets.get(target.target).body

    # # lower all instructions
    # for iid in instrs:
    #     if isinstance(iid, InstructionId):
    #         instr = graph.entities.instructions.get(iid)
    #         out.append(lower_instruction(generator, graph.entities.operands, instr, rewritten))

    return out
