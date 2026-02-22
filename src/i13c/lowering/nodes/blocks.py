from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Set, Tuple, Type

from i13c.core.dag import GraphNode, Prefix
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes.registers import IR_REGISTER_MAP
from i13c.lowering.typing.abstracts import (
    AbstractEntry,
    Abstracts,
    EnterFrame,
    ExitFrame,
    Preserve,
    Restore,
)
from i13c.lowering.typing.blocks import Block, BlockInstruction, Registers
from i13c.lowering.typing.flows import BlockId, Flow, FlowId
from i13c.lowering.typing.instructions import (
    AddRegImm,
    Call,
    Instruction,
    Jump,
    Label,
    MovOffReg,
    MovRegOff,
    Return,
    SubRegImm,
)
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
    return [SubRegImm(dst=IR_REGISTER_MAP[b"rsp"], imm=abstract.size)]


def dispatch_exit_frame(abstract: ExitFrame) -> List[Instruction]:
    return [AddRegImm(dst=IR_REGISTER_MAP[b"rsp"], imm=abstract.size)]


def dispatch_preserve(abstract: Preserve) -> List[Instruction]:
    return [
        MovOffReg(dst=IR_REGISTER_MAP[b"rsp"], src=reg, off=idx * 8)
        for idx, reg in abstract.registers.items()
    ]


def dispatch_restore(abstract: Restore) -> List[Instruction]:
    return [
        MovRegOff(dst=reg, src=IR_REGISTER_MAP[b"rsp"], off=idx * 8)
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
    patching: Dict[str, OneToOne[FlowId, AbstractEntry]]


def configure_instruction_emission() -> GraphNode:
    return GraphNode(
        builder=emit_all_instructions,
        constraint=None,
        produces=("llvm/instructions",),
        requires=frozenset(
            {
                ("entrypoint", "llvm/entrypoint"),
                ("entries", "llvm/functions/entries"),
                ("blocks", "llvm/blocks"),
                ("forward", "llvm/blocks/forward"),
                ("instructions", "llvm/blocks/instructions"),
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
    patching: Dict[str, OneToOne[FlowId, AbstractEntry]],
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
            # check if the instruction has been patched
            if isinstance(instr, Flow):
                for _, mapping in ctx.patching.items():
                    assert isinstance(fid, FlowId)

                    # if patched, obtain the patched abstract entry
                    if mapping.contains(fid):
                        fid, instr = mapping.get(fid)
                        break

            # all flows should be handled by patching
            assert not isinstance(instr, Flow)

            if isinstance(instr, Abstracts):
                emited.extend(DISPATCH_TABLE[type(instr)](instr))
            else:
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


def configure_register_patching() -> GraphNode:
    return GraphNode(
        builder=patch_registers,
        constraint=None,
        produces=("llvm/registers/inputs", "llvm/registers/outputs"),
        requires=frozenset(
            {
                ("blocks", "llvm/blocks"),
                ("backward", "llvm/blocks/backward"),
                ("clobbers", "llvm/registers/clobbers"),
            }
        ),
    )


def patch_registers(
    blocks: OneToOne[BlockId, Block],
    backward: OneToMany[BlockId, BlockId],
    clobbers: OneToOne[BlockId, Registers],
) -> Tuple[OneToOne[BlockId, Registers], OneToOne[BlockId, Registers]]:

    inputs: Dict[BlockId, Registers] = {}
    outputs: Dict[BlockId, Registers] = {}

    for bid in blocks.keys():
        inputs[bid] = Registers.empty()
        outputs[bid] = Registers.empty()

    changed = True
    while changed:
        changed = False

        for bid in blocks.keys():
            if predecessors := backward.get(bid):
                regin = set(outputs[predecessors[0]].items)

                for pred in predecessors[1:]:
                    regin.intersection_update(outputs[pred].items)

            else:
                regin = inputs[bid].items

            regout = regin - clobbers.get(bid).items
            # regout = regout.union(ctx.nodes[bid].registers.generated)

            if regin != inputs.get(bid, Registers.empty()).items:
                inputs[bid] = Registers(items=regin)
                changed = True

            if regout != outputs.get(bid, Registers.empty()).items:
                outputs[bid] = Registers(items=regout)
                changed = True

    return (
        OneToOne[BlockId, Registers].instance(inputs),
        OneToOne[BlockId, Registers].instance(outputs),
    )
