from typing import List, Optional, Set

from i13c.ir import Emit, InstructionFlow, Jump, Label, Stop, Terminator
from i13c.lowering.build import LowLevelGraph
from i13c.lowering.nodes import BlockId


def build_instruction_flow(graph: LowLevelGraph) -> List[InstructionFlow]:
    visited: Set[BlockId] = set()
    ordered: List[BlockId] = []
    emited: List[InstructionFlow] = []

    def visit(bid: BlockId) -> None:
        if bid not in visited:
            visited.add(bid)
            ordered.append(bid)

            for next in graph.edges.get(bid):
                visit(next)

    visit(graph.entry)

    for idx, bid in enumerate(ordered):
        # emit label for block
        emited.append(Label(id=idx))

        # emit all instructions
        for instr in graph.nodes.get(bid).instructions:
            emited.append(instr)

        # determine control transfer
        block = graph.nodes.get(bid)
        successors = graph.edges.get(bid)

        next = ordered[idx + 1] if idx + 1 < len(ordered) else None
        args = (block.terminator, successors, next)

        # emit control transfer if needed
        if jump := emit_control_transfer(*args):
            emited.append(jump)

    return emited


def emit_control_transfer(
    term: Terminator,
    successors: List[BlockId],
    next: Optional[BlockId],
) -> Optional[Jump]:

    # stop terminator, nothing to emit
    if isinstance(term, Stop):
        assert len(successors) == 0
        return None

    if isinstance(term, Emit):
        assert len(successors) > 0
        return None

    # expecting only single successor
    assert len(successors) == 1

    # we are ok with fallthrough
    if next is not None and successors[0].value == next.value:
        return None

    # otherwise emit jump
    return Jump(label=successors[0].value)
