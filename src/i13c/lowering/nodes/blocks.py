from typing import Dict, List, Optional, Set

from i13c.lowering.graph import LowLevelContext
from i13c.lowering.typing.flows import BlockId, Flow
from i13c.lowering.typing.instructions import Call, Instruction, Jump, Label, Return
from i13c.lowering.typing.terminators import (
    ExitTerminator,
    JumpTerminator,
    Terminator,
    TrapTerminator,
)


def emit_all_blocks(ctx: LowLevelContext, entry: BlockId) -> None:
    # emit entrypoint first
    ctx.flows[entry] = emit_instructions(ctx, entry)

    # emit all other functions
    for fid in ctx.entry.keys():
        if ctx.entry[fid] != entry:
            ctx.flows[ctx.entry[fid]] = emit_instructions(ctx, ctx.entry[fid])

    # collect active labels
    active: Set[int] = {
        instr.target.value
        for flow in ctx.flows.values()
        for instr in flow
        if isinstance(instr, Call)
    }

    # remove inactive labels
    for fid in ctx.flows.keys():
        ctx.flows[fid] = [
            instr
            for instr in ctx.flows[fid]
            if not isinstance(instr, Label) or instr.id.value in active
        ]


def linearize_blocks(
    entry: BlockId, edges: Dict[BlockId, List[BlockId]]
) -> List[BlockId]:
    visited: Set[BlockId] = set()
    queue: List[BlockId] = [entry]
    ordered: List[BlockId] = []

    # naive BFS to determine block order
    while queue:
        bid = queue.pop(0)

        if bid not in visited:
            visited.add(bid)
            ordered.append(bid)

            for next in edges[bid]:
                queue.append(next)

    # success
    return ordered


def emit_instructions(ctx: LowLevelContext, entry: BlockId) -> List[Instruction]:
    emited: List[Instruction] = []
    ordered: List[BlockId] = linearize_blocks(entry, ctx.forward)

    # emit instructions in order
    for idx, bid in enumerate(ordered):
        # emit label for block
        emited.append(Label(id=bid))

        # emit all instructions
        for instr in ctx.nodes[bid].instructions:
            assert not isinstance(instr, Flow), str(instr)
            emited.append(instr)

        # determine next block in order
        next = ordered[idx + 1] if idx + 1 < len(ordered) else None
        args = (ctx.nodes[bid].terminator, next)

        # emit control transfer if needed
        if derived := emit_control_transfer(*args):
            emited.append(derived)

    # success
    return emited


def emit_control_transfer(
    term: Terminator, next: Optional[BlockId]
) -> Optional[Instruction]:

    # stop terminator, nothing to emit
    if isinstance(term, TrapTerminator):
        return None

    # exit terminator, nothing to emit
    if isinstance(term, ExitTerminator):
        return Return()

    # accept only jump terminator
    assert isinstance(term, JumpTerminator)

    # are ok with fallthrough?
    if next is not None and term.target.value == next.value:
        return None

    # otherwise emit jump
    return Jump(target=term.target)


def patch_registers(ctx: LowLevelContext):
    changed = True
    while changed:
        changed = False

        for bid in ctx.nodes.keys():
            if predecessors := ctx.backward[bid]:
                inputs = set(ctx.nodes[predecessors[0]].registers.outputs)

                for pred in predecessors[1:]:
                    inputs.intersection_update(ctx.nodes[pred].registers.outputs)

            else:
                inputs = ctx.nodes[bid].registers.inputs

            outputs = inputs - ctx.nodes[bid].registers.clobbered
            outputs = outputs.union(ctx.nodes[bid].registers.generated)

            if inputs != ctx.nodes[bid].registers.inputs:
                ctx.nodes[bid].registers.inputs = inputs
                changed = True

            if outputs != ctx.nodes[bid].registers.outputs:
                ctx.nodes[bid].registers.outputs = outputs
                changed = True
