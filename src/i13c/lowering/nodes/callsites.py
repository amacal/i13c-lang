from typing import List, Set, Tuple

from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.bindings import lower_callsite_bindings
from i13c.lowering.nodes.instances import lower_instance
from i13c.lowering.nodes.registers import IR_REGISTER_MAP
from i13c.lowering.typing.blocks import BlockInstruction
from i13c.lowering.typing.flows import CallFlow, PreserveFlow, RestoreFlow
from i13c.lowering.typing.instructions import Call
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.snippets import SnippetId


def lower_callsite(
    ctx: LowLevelContext,
    cid: CallSiteId,
) -> Tuple[List[BlockInstruction], Set[int]]:

    # prepare result containers
    clobbers: Set[int] = set()
    instructions: List[BlockInstruction] = []

    # retrieve callsite resolution
    resolution = ctx.graph.indices.resolution_by_callsite.get(cid)

    # we expected no ambiguity here
    assert len(resolution.accepted) == 1

    # append preserve instructions
    instructions.append(PreserveFlow())

    if isinstance(resolution.accepted[0].callable.target, SnippetId):
        instance = ctx.graph.indices.instance_by_callsite.get(cid)
        snippet = ctx.graph.basic.snippets.get(instance.target)

        # append callsite specific bindings
        instructions.extend(lower_callsite_bindings(ctx, instance.bindings))

        # append emitted instructions
        instructions.extend(lower_instance(ctx, instance))

        # update clobbered registers
        clobbers.update(
            [IR_REGISTER_MAP[register.name] for register in snippet.clobbers]
        )

    else:

        # append callsite specific bindings
        instructions.extend(lower_callsite_bindings(ctx, []))

        # extract successfully resolved target
        target = resolution.accepted[0].callable.target

        # append callsite call instructions
        instructions.extend([CallFlow(target=target)])

        # all IR registers are clobbered by function calls
        clobbers.update(set(IR_REGISTER_MAP.values()))

    # append restore instructions
    instructions.append(RestoreFlow())

    # callsite instructions and clobbers
    return instructions, clobbers


def patch_all_callsites(ctx: LowLevelContext) -> None:
    for block in ctx.nodes.values():
        # only callsite blocks may have calls
        if not isinstance(block.origin, CallSiteId):
            continue

        # patch all calls within block
        for idx, instr in enumerate(block.instructions):
            if isinstance(instr, CallFlow):
                block.instructions[idx] = Call(target=ctx.entry[instr.target])
