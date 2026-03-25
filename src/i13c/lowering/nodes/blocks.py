from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Set, Tuple, Type, Union

from i13c.core.dag import GraphNode, Prefix
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.abstracts import (
    AbstractEntry,
    Abstracts,
    EnterFrame,
    ExitFrame,
    Preserve,
    Restore,
)
from i13c.lowering.typing.blocks import (
    Block,
    BlockInstruction,
    BlockInstructionId,
    InstructionPosition,
    Registers,
)
from i13c.lowering.typing.flows import (
    BindingFlow,
    BlockId,
    Flow,
    FlowId,
    ImmediateFlow,
    SnapshotFlow,
)
from i13c.lowering.typing.instructions import (
    AddRegImm,
    Call,
    Instruction,
    Jump,
    Label,
    MovOffReg,
    MovRegOff,
    Nop,
    Return,
    SubRegImm,
)
from i13c.lowering.typing.intervals import IntervalPressure, RegisterInterval
from i13c.lowering.typing.registers import IR_REGISTER_FORWARD
from i13c.lowering.typing.terminators import (
    ExitTerminator,
    JumpTerminator,
    Terminator,
    TrapTerminator,
)
from i13c.semantic.typing.entities.functions import FunctionId


class AbstractConverter(Protocol):
    def __call__(self, abstract: Abstracts) -> List[Instruction]: ...


def dispatch_enter_frame(abstract: EnterFrame) -> List[Instruction]:
    if abstract.size > 0:
        return [SubRegImm(dst=IR_REGISTER_FORWARD[b"rsp"], imm=abstract.size)]

    else:
        return []


def dispatch_exit_frame(abstract: ExitFrame) -> List[Instruction]:
    if abstract.size > 0:
        return [AddRegImm(dst=IR_REGISTER_FORWARD[b"rsp"], imm=abstract.size)]

    else:
        return []


def dispatch_preserve(abstract: Preserve) -> List[Instruction]:
    return [
        MovOffReg(dst=IR_REGISTER_FORWARD[b"rsp"], src=reg, off=idx * 8)
        for idx, reg in abstract.registers.items()
    ]


def dispatch_restore(abstract: Restore) -> List[Instruction]:
    return [
        MovRegOff(dst=reg, src=IR_REGISTER_FORWARD[b"rsp"], off=idx * 8)
        for idx, reg in abstract.registers.items()
    ]


DISPATCH_TABLE: Dict[Type[Abstracts], AbstractConverter] = {
    EnterFrame: dispatch_enter_frame,
    ExitFrame: dispatch_exit_frame,
    Preserve: dispatch_preserve,
    Restore: dispatch_restore,
}  # pyright: ignore[reportAssignmentType]


@dataclass(kw_only=True)
class Context:
    flows: Dict[BlockId, List[Instruction]]
    entries: OneToOne[FunctionId, BlockId]
    blocks: OneToOne[BlockId, Block]
    forward: OneToMany[BlockId, BlockId]
    instructions: OneToMany[BlockId, BlockInstruction]
    patching: Dict[str, OneToMany[FlowId, AbstractEntry]]


def configure_instruction_emission() -> GraphNode:
    return GraphNode(
        builder=emit_all_instructions,
        constraint=None,
        produces=("assembler/instructions",),
        requires=frozenset(
            {
                ("entrypoint", "llvm/entrypoint"),
                ("entries", "llvm/functions/entries"),
                ("blocks", "llvm/blocks"),
                ("forward", "llvm/blocks/forward"),
                ("instructions", "llvm/instructions"),
                ("patching", Prefix(value="llvm/patches/")),
            }
        ),
    )


def emit_all_instructions(
    entrypoint: BlockId,
    entries: OneToOne[FunctionId, BlockId],
    blocks: OneToOne[BlockId, Block],
    forward: OneToMany[BlockId, BlockId],
    instructions: OneToMany[BlockId, BlockInstruction],
    patching: Dict[str, OneToMany[FlowId, AbstractEntry]],
) -> OneToMany[BlockId, Instruction]:

    result: Dict[BlockId, List[Instruction]] = {}
    ctx = Context(
        flows=result,
        entries=entries,
        blocks=blocks,
        forward=forward,
        patching=patching,
        instructions=instructions,
    )

    # emit entrypoint first
    result[entrypoint] = emit_instructions(ctx, entrypoint)

    # emit all other functions
    for fid, bid in entries.items():
        if bid != entrypoint:
            result[bid] = emit_instructions(ctx, bid)

    # collect active labels
    active: Set[int] = {
        instr.target.value
        for flow in result.values()
        for instr in flow
        if isinstance(instr, Call)
    }

    # remove inactive labels
    for fid in result.keys():
        result[fid] = [
            instr
            for instr in result[fid]
            if not isinstance(instr, Label) or instr.id.value in active
        ]

    return OneToMany[BlockId, Instruction].instance(result)


def linearize_blocks(
    entry: BlockId, forward: OneToMany[BlockId, BlockId]
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

            for next in forward.get(bid):
                queue.append(next)

    # success
    return ordered


def emit_instructions(ctx: Context, entry: BlockId) -> List[Instruction]:
    emited: List[Instruction] = []
    ordered: List[BlockId] = linearize_blocks(entry, ctx.forward)

    # emit instructions in order
    for idx, bid in enumerate(ordered):
        # emit label for block
        emited.append(Label(id=bid))

        # emit all instructions
        for fid, instr in ctx.instructions.get(bid):
            entries: List[Union[Instruction, Abstracts]] = []

            # check if the instruction has been patched
            if isinstance(instr, Flow):
                for _, mapping in ctx.patching.items():
                    assert isinstance(fid, FlowId)

                    # if patched, obtain the patched abstract entry
                    if items := mapping.find(fid):
                        entries.extend(entry for _, entry in items)
                        break

            else:
                entries.append(instr)

            # all flows should be handled by patching
            assert not all(
                isinstance(instr, Flow) for instr in entries
            ), f"Unpatched flow {instr} in block {bid}"

            for instr in entries:
                if isinstance(instr, Abstracts):
                    emited.extend(DISPATCH_TABLE[type(instr)](instr))

                elif not isinstance(instr, Nop):
                    emited.append(instr)

        # determine next block in order
        next = ordered[idx + 1] if idx + 1 < len(ordered) else None
        args = (ctx.blocks.get(bid).terminator, next)

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


def configure_function_blocks() -> GraphNode:
    return GraphNode(
        builder=build_function_blocks,
        constraint=None,
        produces=("llvm/functions/blocks",),
        requires=frozenset(
            {
                ("forward", "llvm/blocks/forward"),
                ("entries", "llvm/functions/entries"),
            }
        ),
    )


def build_function_blocks(
    forward: OneToMany[BlockId, BlockId],
    entries: OneToOne[FunctionId, BlockId],
) -> OneToMany[FunctionId, BlockId]:

    result: Dict[FunctionId, List[BlockId]] = {}

    for fid, bid in entries.items():
        result[fid] = linearize_blocks(bid, forward)

    return OneToMany[FunctionId, BlockId].instance(result)


def configure_function_instructions() -> GraphNode:
    return GraphNode(
        builder=build_function_instructions,
        constraint=None,
        produces=("llvm/functions/instructions",),
        requires=frozenset(
            {
                ("blocks", "llvm/functions/blocks"),
                ("instructions", "llvm/instructions"),
            }
        ),
    )


def build_function_instructions(
    blocks: OneToMany[FunctionId, BlockId],
    instructions: OneToMany[BlockId, BlockInstruction],
) -> OneToMany[FunctionId, InstructionPosition]:

    result: Dict[FunctionId, List[InstructionPosition]] = {}

    for fid, bids in blocks.items():
        index: int = 0
        order: List[InstructionPosition] = []

        for bid in bids:
            for iid, _ in instructions.get(bid):
                order.append(InstructionPosition(target=iid, block=bid, index=index))
                index += 1

        result[fid] = order

    return OneToMany[FunctionId, InstructionPosition].instance(result)


def configure_register_intervals() -> GraphNode:
    return GraphNode(
        builder=build_register_intervals,
        constraint=None,
        produces=("llvm/functions/intervals",),
        requires=frozenset(
            {
                ("instructions", "llvm/functions/instructions"),
                ("idef", "llvm/instructions/registers/def"),
                ("iout", "llvm/instructions/registers/out"),
            }
        ),
    )


def build_register_intervals(
    instructions: OneToMany[FunctionId, InstructionPosition],
    idef: OneToOne[BlockInstructionId, Registers],
    iout: OneToOne[BlockInstructionId, Registers],
) -> OneToMany[FunctionId, RegisterInterval]:

    intervals: Dict[FunctionId, List[RegisterInterval]] = {}

    for fid, positions in instructions.items():
        ending: Dict[int, int] = {}
        starting: Dict[int, int] = {}
        maximum: int = 0

        for position in positions:
            if maximum < position.index:
                maximum = position.index

            for reg in idef.get(position.target).items:
                starting[reg] = position.index

            for reg in iout.get(position.target).items:
                ending[reg] = position.index

        intervals[fid] = [
            RegisterInterval(
                vreg=reg,
                start=starting[reg],
                end=ending.get(reg, maximum),
            )
            for reg in starting.keys() | ending.keys()
        ]

    return OneToMany[FunctionId, RegisterInterval].instance(intervals)


def configure_register_interval_pressure() -> GraphNode:
    return GraphNode(
        builder=build_register_interval_pressure,
        constraint=None,
        produces=("llvm/functions/intervals/pressure",),
        requires=frozenset(
            {
                ("intervals", "llvm/functions/intervals"),
            }
        ),
    )


def build_register_interval_pressure(
    intervals: OneToMany[FunctionId, RegisterInterval],
) -> OneToMany[FunctionId, IntervalPressure]:

    pressure: Dict[FunctionId, List[IntervalPressure]] = {}

    for fid, ivs in intervals.items():
        datapoints = max(iv.end for iv in ivs) + 1 if ivs else 0
        instructions = [0] * datapoints

        for iv in ivs:
            for idx in range(iv.start, iv.end + 1):
                instructions[idx] += 1

        pressure[fid] = [
            IntervalPressure(
                index=idx,
                pressure=pres,
                registers=[iv.vreg for iv in ivs if iv.start <= idx <= iv.end],
            )
            for idx, pres in enumerate(instructions)
        ]

    return OneToMany[FunctionId, IntervalPressure].instance(pressure)


def configure_defined_and_used_registers_for_instructions() -> GraphNode:
    return GraphNode(
        builder=find_defined_and_used_registers_for_instructions,
        constraint=None,
        produces=(
            "llvm/instructions/registers/def",
            "llvm/instructions/registers/use",
        ),
        requires=frozenset(
            {
                ("instructions", "llvm/instructions"),
            }
        ),
    )


def find_defined_and_used_registers_for_instructions(
    instructions: OneToMany[BlockId, BlockInstruction],
) -> Tuple[
    OneToOne[BlockInstructionId, Registers],
    OneToOne[BlockInstructionId, Registers],
]:

    defined: Dict[BlockInstructionId, Registers] = {}
    usages: Dict[BlockInstructionId, Registers] = {}

    # we want to carefully cover all instructions to determine defined and used registers
    # we can only scan for move and binding flows for now

    for _, batch in instructions.items():
        for iid, instr in batch:
            if isinstance(instr, SnapshotFlow) or isinstance(instr, ImmediateFlow):
                defined[iid] = Registers(items={instr.dst})
            else:
                defined[iid] = Registers.empty()

            if isinstance(instr, BindingFlow):
                usages[iid] = Registers(items={instr.src})
            else:
                usages[iid] = Registers.empty()

    return (
        OneToOne[BlockInstructionId, Registers].instance(defined),
        OneToOne[BlockInstructionId, Registers].instance(usages),
    )


def configure_defined_and_used_registers_for_blocks() -> GraphNode:
    return GraphNode(
        builder=find_defined_and_used_registers_for_blocks,
        constraint=None,
        produces=(
            "llvm/blocks/registers/def",
            "llvm/blocks/registers/use",
        ),
        requires=frozenset(
            {
                ("instructions", "llvm/instructions"),
                ("idef", "llvm/instructions/registers/def"),
                ("iuse", "llvm/instructions/registers/use"),
            }
        ),
    )


def find_defined_and_used_registers_for_blocks(
    instructions: OneToMany[BlockId, BlockInstruction],
    idef: OneToOne[BlockInstructionId, Registers],
    iuse: OneToOne[BlockInstructionId, Registers],
) -> Tuple[OneToOne[BlockId, Registers], OneToOne[BlockId, Registers]]:

    bdef: Dict[BlockId, Registers] = {}
    buse: Dict[BlockId, Registers] = {}

    # block level is simply the union of all instruction level

    for bid, batch in instructions.items():
        sdef: Set[int] = set()
        suse: Set[int] = set()

        for iid, _ in batch:
            sdef.update(idef.get(iid).items)
            suse.update(iuse.get(iid).items)

        bdef[bid] = Registers(items=sdef)
        buse[bid] = Registers(items=suse)

    return (
        OneToOne[BlockId, Registers].instance(bdef),
        OneToOne[BlockId, Registers].instance(buse),
    )


def configure_in_and_out_registers_for_blocks() -> GraphNode:
    return GraphNode(
        builder=find_in_and_out_registers_for_blocks,
        constraint=None,
        produces=(
            "llvm/blocks/registers/in",
            "llvm/blocks/registers/out",
        ),
        requires=frozenset(
            {
                ("backward", "llvm/blocks/backward"),
                ("buse", "llvm/blocks/registers/use"),
            }
        ),
    )


def find_in_and_out_registers_for_blocks(
    backward: OneToMany[BlockId, BlockId],
    buse: OneToOne[BlockId, Registers],
) -> Tuple[OneToOne[BlockId, Registers], OneToOne[BlockId, Registers]]:

    iin: Dict[BlockId, Registers] = {}
    iout: Dict[BlockId, Registers] = {}

    for bid in buse.keys():
        iin[bid] = Registers.empty()
        iout[bid] = Registers.empty()

    regout: Set[int]
    changed = True

    while changed:
        changed = False

        for bid in buse.keys():
            regin = set(buse.get(bid).items)  # start with used-registers
            regin.update(iout[bid].items)  # add out-registers from previous iteration

            if predecessors := backward.get(bid):
                regout = set(
                    iin[predecessors[0]].items
                )  # start with in-registers of first predecessor

                for pred in predecessors[1:]:
                    regout.update(
                        iin[pred].items
                    )  # add in-registers of other predecessors

            else:
                regout = set()

            if regin != iin[bid].items:
                iin[bid] = Registers(items=regin)
                changed = True

            if regout != iout[bid].items:
                iout[bid] = Registers(items=regout)
                changed = True

    return (
        OneToOne[BlockId, Registers].instance(iin),
        OneToOne[BlockId, Registers].instance(iout),
    )


def configure_in_and_out_registers_for_instructions() -> GraphNode:
    return GraphNode(
        builder=find_in_and_out_registers_for_instructions,
        constraint=None,
        produces=(
            "llvm/instructions/registers/in",
            "llvm/instructions/registers/out",
        ),
        requires=frozenset(
            {
                ("instructions", "llvm/instructions"),
                ("iuse", "llvm/instructions/registers/use"),
                ("bout", "llvm/blocks/registers/out"),
            }
        ),
    )


def find_in_and_out_registers_for_instructions(
    instructions: OneToMany[BlockId, BlockInstruction],
    iuse: OneToOne[BlockInstructionId, Registers],
    bout: OneToOne[BlockId, Registers],
) -> Tuple[
    OneToOne[BlockInstructionId, Registers], OneToOne[BlockInstructionId, Registers]
]:

    iin: Dict[BlockInstructionId, Registers] = {}
    iout: Dict[BlockInstructionId, Registers] = {}

    for bid, batch in instructions.items():
        live = set(bout.get(bid).items)

        for iid, _ in reversed(batch):
            iout[iid] = Registers(items=live.copy())
            live.update(iuse.get(iid).items)
            iin[iid] = Registers(items=live.copy())

    return (
        OneToOne[BlockInstructionId, Registers].instance(iin),
        OneToOne[BlockInstructionId, Registers].instance(iout),
    )
