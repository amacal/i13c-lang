from typing import List

from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.bindings import lower_callsite_bindings
from i13c.lowering.nodes.instances import lower_instance
from i13c.lowering.typing.blocks import Block, BlockInstruction
from i13c.lowering.typing.flows import CallFlow
from i13c.lowering.typing.instructions import Call
from i13c.lowering.typing.terminators import Terminator
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.snippets import SnippetId


def lower_callsite(
    ctx: LowLevelContext,
    cid: CallSiteId,
    terminator: Terminator,
) -> Block:
    instructions: List[BlockInstruction] = []

    # retrieve callsite resolution
    resolution = ctx.graph.indices.resolution_by_callsite.get(cid)

    # we expected no ambiguity here
    assert len(resolution.accepted) == 1

    if isinstance(resolution.accepted[0].callable.target, SnippetId):
        instance = ctx.graph.indices.instance_by_callsite.get(cid)

        # append callsite specific bindings
        instructions.extend(lower_callsite_bindings(ctx, instance.bindings))

        # append instance instructions
        instructions.extend(lower_instance(ctx, instance))

    else:

        # append callsite specific bindings
        instructions.extend(lower_callsite_bindings(ctx, []))

        # append callsite call instructions
        instructions.extend([CallFlow(target=resolution.accepted[0].callable.target)])

    return Block(
        origin=cid,
        instructions=instructions,
        terminator=terminator,
    )


def patch_all_callsites(ctx: LowLevelContext) -> None:
    for block in ctx.nodes.values():
        # only callsite blocks may have calls
        if not isinstance(block.origin, CallSiteId):
            continue

        # patch all calls within block
        for idx, instr in enumerate(block.instructions):
            if isinstance(instr, CallFlow):
                block.instructions[idx] = Call(target=ctx.entry[instr.target])
