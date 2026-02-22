from typing import Dict

from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes.blocks import linearize_blocks
from i13c.lowering.typing.abstracts import (
    AbstractEntry,
    AbstractId,
    EnterFrame,
    ExitFrame,
    Preserve,
    Restore,
)
from i13c.lowering.typing.blocks import Block, BlockInstruction, Registers
from i13c.lowering.typing.flows import (
    BlockId,
    EpilogueFlow,
    FlowId,
    PreserveFlow,
    PrologueFlow,
    RestoreFlow,
)
from i13c.lowering.typing.stacks import StackFrame
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.functions import FunctionId


def configure_stack_patching() -> GraphNode:
    return GraphNode(
        builder=patch_stack_frames,
        constraint=None,
        produces=("llvm/patches/stacks",),
        requires=frozenset(
            {
                ("graph", "semantic/graph"),
                ("blocks", "llvm/blocks"),
                ("entries", "llvm/functions/entries"),
                ("forward", "llvm/blocks/forward"),
                ("inputs", "llvm/registers/inputs"),
                ("outputs", "llvm/registers/outputs"),
                ("instructions", "llvm/blocks/instructions"),
            }
        ),
    )


def patch_stack_frames(
    graph: SemanticGraph,
    blocks: OneToOne[BlockId, Block],
    entries: OneToOne[FunctionId, BlockId],
    forward: OneToMany[BlockId, BlockId],
    inputs: OneToOne[BlockId, Registers],
    outputs: OneToOne[BlockId, Registers],
    instructions: OneToMany[BlockId, BlockInstruction],
) -> OneToOne[FlowId, AbstractEntry]:
    stacks: Dict[FunctionId, StackFrame] = {}
    result: Dict[FlowId, AbstractEntry] = {}

    # first determine all stack frame
    for fid in entries.keys():
        # initialize maximum preserved size
        preserves = 0

        # analyze function blocks for stack usage
        for bid in linearize_blocks(entries.get(fid), forward):
            registers = inputs.get(bid).items - outputs.get(bid).items
            preserves = max(preserves, 8 * len(registers))

        # determine stack frame for function
        stacks[fid] = StackFrame(size=preserves)

    # then patch all prologues/epilogues
    for bid in blocks.keys():
        for fid, instruction in instructions.get(bid):
            if not isinstance(fid, FlowId):
                continue

            if isinstance(instruction, PrologueFlow):
                stackframe = stacks[instruction.target]
                aid = AbstractId(value=graph.generator.next())
                result[fid] = (aid, EnterFrame(size=stackframe.size))

            if isinstance(instruction, EpilogueFlow):
                stackframe = stacks[instruction.target]
                aid = AbstractId(value=graph.generator.next())
                result[fid] = (aid, ExitFrame(size=stackframe.size))

            if isinstance(instruction, PreserveFlow):
                # determine affected registers
                registers = inputs.get(bid).items - outputs.get(bid).items

                # generate preserve instruction
                aid = AbstractId(value=graph.generator.next())
                mapping = {idx: reg for idx, reg in enumerate(sorted(registers))}

                # append preserve entry to be patched later
                result[fid] = (aid, Preserve(registers=mapping))

            if isinstance(instruction, RestoreFlow):
                # determine affected registers
                registers = inputs.get(bid).items - outputs.get(bid).items

                # generate restore instruction
                aid = AbstractId(value=graph.generator.next())
                mapping = {idx: reg for idx, reg in enumerate(sorted(registers))}

                # append restore entry to be patched later
                result[fid] = (aid, Restore(registers=mapping))

    return OneToOne[FlowId, AbstractEntry].instance(result)
