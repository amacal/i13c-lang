from typing import Dict, List, Set

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.abstracts import (
    AbstractEntry,
    AbstractId,
    EnterFrame,
    ExitFrame,
)
from i13c.lowering.typing.blocks import BlockInstruction
from i13c.lowering.typing.flows import (
    BlockId,
    EpilogueFlow,
    FlowId,
    PrologueFlow,
)
from i13c.lowering.typing.intervals import IntervalPressure
from i13c.lowering.typing.stacks import StackFrame
from i13c.semantic.typing.entities.functions import FunctionId


def configure_stack_frames() -> GraphNode:
    return GraphNode(
        builder=build_stack_frames,
        constraint=None,
        produces=("llvm/functions/stackframes",),
        requires=frozenset({("pressures", "llvm/functions/intervals/pressure")}),
    )


def build_stack_frames(
    pressures: OneToMany[FunctionId, IntervalPressure],
) -> OneToOne[FunctionId, StackFrame]:

    frames: Dict[FunctionId, StackFrame] = {}

    for fid, entries in pressures.items():
        size: int = max(entry.pressure for entry in entries) if entries else 0
        previous: Set[int] = set()

        allocated: Dict[int, int] = {}
        available: List[int] = list(range(size))

        for entry in entries:
            # append new used anymore registers
            for reg in previous:
                if reg not in entry.registers:
                    available.append(reg)

            # allocate newly appeared registers
            for reg in sorted(entry.registers, reverse=True):
                if reg not in allocated:
                    allocated[reg] = available.pop()

        frames[fid] = StackFrame(size=8 * size, regs=allocated)

    return OneToOne[FunctionId, StackFrame].instance(frames)


def configure_stack_patching() -> GraphNode:
    return GraphNode(
        builder=patch_stack_frames,
        constraint=None,
        produces=("llvm/patches/stacks",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("blocks", "llvm/functions/blocks"),
                ("instructions", "llvm/instructions"),
                ("stackframes", "llvm/functions/stackframes"),
            }
        ),
    )


def patch_stack_frames(
    generator: Generator,
    blocks: OneToMany[FunctionId, BlockId],
    stackframes: OneToOne[FunctionId, StackFrame],
    instructions: OneToMany[BlockId, BlockInstruction],
) -> OneToMany[FlowId, AbstractEntry]:

    result: Dict[FlowId, List[AbstractEntry]] = {}

    # then patch all prologues/epilogues
    for fid, bids in blocks.items():
        for bid in bids:
            for iid, instr in instructions.get(bid):
                if not isinstance(iid, FlowId):
                    continue

                if isinstance(instr, PrologueFlow):
                    stackframe = stackframes.get(fid)
                    aid = AbstractId(value=generator.next())
                    result[iid] = [(aid, EnterFrame(size=stackframe.size))]

                if isinstance(instr, EpilogueFlow):
                    stackframe = stackframes.get(fid)
                    aid = AbstractId(value=generator.next())
                    result[iid] = [(aid, ExitFrame(size=stackframe.size))]

    return OneToMany[FlowId, AbstractEntry].instance(result)
