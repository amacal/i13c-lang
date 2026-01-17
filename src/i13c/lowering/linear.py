from typing import List, Optional, Set

from i13c.lowering.graph import LowLevelContext
from i13c.lowering.typing.flows import BlockId, Flow
from i13c.lowering.typing.instructions import Instruction, Label, Return
from i13c.lowering.typing.terminators import ExitTerminator, Terminator, TrapTerminator


def build_instruction_flow(ctx: LowLevelContext, entry: BlockId) -> List[Instruction]:

    visited: Set[BlockId] = set()
    queue: List[BlockId] = [entry]

    ordered: List[BlockId] = []
    emited: List[Instruction] = []

    while queue:
        bid = queue.pop(0)

        if bid not in visited:
            visited.add(bid)
            ordered.append(bid)

            for next in ctx.edges[bid]:
                queue.append(next)

    for idx, bid in enumerate(ordered):
        # emit label for block
        emited.append(Label(id=bid))

        # emit all instructions
        for instr in ctx.nodes[bid].instructions:
            assert not isinstance(instr, Flow)
            emited.append(instr)

        # determine control transfer
        block = ctx.nodes[bid]
        successors = ctx.edges[bid]

        next = ordered[idx + 1] if idx + 1 < len(ordered) else None
        args = (block.terminator, successors, next)

        # emit control transfer if needed
        if derived := emit_control_transfer(*args):
            emited.append(derived)

    return emited


def emit_control_transfer(
    term: Terminator,
    successors: List[BlockId],
    next: Optional[BlockId],
) -> Optional[Instruction]:

    # stop terminator, nothing to emit
    if isinstance(term, TrapTerminator):
        assert len(successors) == 0
        return None

    # exit terminator, nothing to emit
    if isinstance(term, ExitTerminator):
        assert len(successors) == 0
        return Return()

    # expecting only single successor
    assert len(successors) == 1

    # we are ok with fallthrough
    if next is not None and successors[0].value == next.value:
        return None

    # otherwise emit jump
    assert False, "Jump emission not implemented yet"
