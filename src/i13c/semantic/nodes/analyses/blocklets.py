from collections.abc import Callable, Iterable
from dataclasses import dataclass
from functools import partial
from typing import Protocol

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import (
    Asmlet,
    AsmletId,
    AsmletOperand,
    AsmletOperandAddress,
    AsmletOperandImmediate,
    AsmletOperandRegister,
    AsmletOperandRelocation,
)
from i13c.semantic.typing.analyses.blocklets import (
    Blocklet,
    BlockletBlock,
    BlockletId,
    BlockletInstruction,
    BlockletTarget,
)
from i13c.semantic.typing.analyses.entrypoints import Entrypoint
from i13c.semantic.typing.analyses.fnlets import Fnlet
from i13c.semantic.typing.analyses.llvm import (
    ADC,
    ADD,
    AND,
    BSWAP,
    CALL,
    CMP,
    JMP,
    LEA,
    LOOP,
    LOOPE,
    LOOPNE,
    MOV,
    NOP,
    OR,
    POP,
    PUSH,
    RET,
    SBB,
    SHL,
    SHR,
    SUB,
    SYSCALL,
    XCHG,
    XOR,
    ROL,
    ROR,
    RCL,
    RCR,
    SAR,
    SAL,
    Address,
    Displacement,
    Group1Instruction,
    Group2Instruction,
    Group1Operands,
    Group2Operands,
    Immediate,
    Index,
    Register,
    Relocation,
    LoopOperands,
    LoopInstruction,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.syntax.source import Span


def configure_blocklets() -> GraphNode:
    return GraphNode(
        builder=build_blocklets,
        constraint=None,
        produces=("analyses/blocklets",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("entrypoints", "analyses/entrypoints"),
                ("asmlets", "analyses/asmlets"),
                ("fnlets", "analyses/fnlets"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_blocklets(
    generator: Generator,
    entrypoints: OneToOne[SignatureId, Entrypoint],
    asmlets: OneToOne[AsmletId, Asmlet],
    fnlets: OneToOne[FunctionId, Fnlet],
) -> OneToOne[BlockletId, Blocklet]:
    blocklets: dict[BlockletId, Blocklet] = {}

    for bid, blocklet in emit_asmlets(generator, asmlets, entrypoints):
        blocklets[bid] = blocklet

    for bid, blocklet in emit_fnlets(generator, fnlets, entrypoints):
        blocklets[bid] = blocklet

    return OneToOne[BlockletId, Blocklet].instance(blocklets)


@dataclass(kw_only=True, repr=False)
class EmitRelocation:
    target: EmitRelocatable
    offset: int


EmitRelocatable = LoopInstruction | JMP | CALL
EmitRelocated = tuple[BlockletInstruction, EmitRelocation | None]
EmitSignature = Callable[[list[AsmletOperand]], EmitRelocated]


def emit_asmlets(
    generator: Generator,
    asmlets: OneToOne[AsmletId, Asmlet],
    entrypoints: OneToOne[SignatureId, Entrypoint],
) -> Iterable[tuple[BlockletId, Blocklet]]:

    dispatch: dict[bytes, EmitSignature] = {
        b"adc": partial(emit_group1, ADC),
        b"add": partial(emit_group1, ADD),
        b"and": partial(emit_group1, AND),
        b"bswap": emit_bswap,
        b"call": emit_call,
        b"cmp": partial(emit_group1, CMP),
        b"jmp": emit_jmp,
        b"lea": emit_lea,
        b"loop": partial(emit_loop, LOOP),
        b"loope": partial(emit_loop, LOOPE),
        b"loopne": partial(emit_loop, LOOPNE),
        b"mov": emit_mov,
        b"nop": emit_nop,
        b"or": partial(emit_group1, OR),
        b"pop": emit_pop,
        b"push": emit_push,
        b"rcl": partial(emit_group2, RCL),
        b"rcr": partial(emit_group2, RCR),
        b"ret": emit_ret,
        b"rol": partial(emit_group2, ROL),
        b"ror": partial(emit_group2, ROR),
        b"sal": partial(emit_group2, SAL),
        b"sar": partial(emit_group2, SAR),
        b"sbb": partial(emit_group1, SBB),
        b"shl": partial(emit_group2, SHL),
        b"shr": partial(emit_group2, SHR),
        b"sub": partial(emit_group1, SUB),
        b"syscall": emit_syscall,
        b"xchg": emit_xchg,
        b"xor": partial(emit_group1, XOR),
    }

    for eid, entry in asmlets.items():
        blocks: list[BlockletBlock] = []
        instructions: list[BlockletInstruction] = []
        relocations: list[tuple[int, EmitRelocation]] = []
        fixes: dict[int, int] = {}

        # find all instructions that have relocations and mark them for splitting
        for idx, instr in enumerate(entry.instructions):
            for operand in instr.operands:
                if isinstance(operand.target, AsmletOperandRelocation):
                    fixes[idx + operand.target.offset] = 0

        # emit all instructions, and collect relocations
        for idx, instr in enumerate(entry.instructions):
            instruction, relocation = dispatch[instr.mnemonic](instr.operands)

            # start a new block if this instruction is a split point
            if idx in fixes and instructions:
                blocks.append(BlockletBlock(instructions=instructions))
                fixes[idx] = len(blocks)
                instructions = []

            if relocation is not None:
                relocations.append((idx, relocation))

            instructions.append(instruction)

        # if there are any remaining instructions, add them as a block
        if instructions:
            blocks.append(BlockletBlock(instructions=instructions))

        # apply relocations to the instructions
        for idx, relocation in relocations:
            relocation.target.operands = (
                Relocation(block=fixes[idx + relocation.offset]),
            )

        blocklet = Blocklet(
            ref=entry.ref,
            target=eid,
            entrypoint=entrypoints.contains(entry.signature.id),
            id=BlockletId(value=generator.next()),
            blocks=blocks,
        )

        yield blocklet.id, blocklet


def emit_mov(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg_addr(operands[0])
    src = accept_reg_imm_addr(operands[1])

    return MOV(operands=(dst, src)), None


def emit_bswap(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    dst = accept_reg(operands[0])

    return BSWAP(operands=(dst,)), None


def emit_xchg(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg_addr(operands[0])
    src = accept_reg_addr(operands[1])

    return (XCHG(operands=(dst, src)), None)


def emit_nop(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 0

    # just emit a NOP instruction
    return NOP(), None


def emit_ret(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 0

    # just emit a RET instruction
    return RET(), None


def emit_call(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # the target must be either a relocation or an address
    target = accept_reg_addr_rel(operands[0])

    if isinstance(target, tuple):
        instruction = CALL(operands=(target[0],))
        relocation = EmitRelocation(target=instruction, offset=target[1])

    else:
        instruction = CALL(operands=(target,))
        relocation = None

    return instruction, relocation


def emit_jmp(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # the target must be either a relocation or an address
    target = accept_reg_addr_rel(operands[0])

    if isinstance(target, tuple):
        instruction = JMP(operands=(target[0],))
        relocation = EmitRelocation(target=instruction, offset=target[1])

    else:
        instruction = JMP(operands=(target,))
        relocation = None

    return instruction, relocation


def emit_syscall(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 0

    # just emit a SYSCALL instruction
    return SYSCALL(), None


class Group1Constructor[T: Group1Instruction](Protocol):
    def __call__(self, *, operands: Group1Operands) -> T: ...


class Group2Constructor[T: Group2Instruction](Protocol):
    def __call__(self, *, operands: Group2Operands) -> T: ...


class LoopConstructor[T: LoopInstruction](Protocol):
    def __call__(self, *, operands: LoopOperands) -> T: ...


def emit_group1[T: Group1Instruction](
    op: Group1Constructor[T],
    operands: list[AsmletOperand],
) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    # two operands
    dst = accept_reg_addr(operands[0])
    src = accept_reg_imm_addr(operands[1])

    # no relocation
    return op(operands=(dst, src)), None


def emit_group2[T: Group2Instruction](
    op: Group2Constructor[T],
    operands: list[AsmletOperand],
) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    # two operands
    dst = accept_reg_addr(operands[0])
    src = accept_reg_imm(operands[1])

    # no relocation
    return op(operands=(dst, src)), None


def emit_loop[T: LoopInstruction](
    op: LoopConstructor[T],
    operands: list[AsmletOperand],
) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # one relocation operand
    assert isinstance(operands[0].target, AsmletOperandRelocation)

    instruction = op(operands=(Relocation(block=0),))
    relocation = EmitRelocation(target=instruction, offset=operands[0].target.offset)

    return instruction, relocation


def emit_lea(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg(operands[0])
    src = accept_addr(operands[1])

    return LEA(operands=(dst, src)), None


def emit_pop(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    dst = accept_reg_addr(operands[0])

    return POP(operands=(dst,)), None


def emit_push(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    dst = accept_reg_imm_addr(operands[0])

    return PUSH(operands=(dst,)), None


def accept_reg(operand: AsmletOperand) -> Register:
    # sanity checks
    assert isinstance(operand.target, AsmletOperandRegister)

    return Register(name=operand.target.name)


def accept_addr(operand: AsmletOperand) -> Address:
    # sanity checks
    assert isinstance(operand.target, AsmletOperandAddress)

    index = (
        Index(
            scale=operand.target.indx.scale,
            reg=Register(name=operand.target.indx.reg.name),
        )
        if operand.target.indx is not None
        else None
    )

    disp = (
        Displacement(
            width=operand.target.disp.width,
            offset=operand.target.disp.offset,
            direction=operand.target.disp.direction,
        )
        if operand.target.disp is not None
        else None
    )

    return Address(
        size=operand.target.size,
        base=(
            Register(name=operand.target.base.name)
            if operand.target.base is not None
            else None
        ),
        indx=index,
        disp=disp,
    )


def accept_reg_addr(operand: AsmletOperand) -> Register | Address:
    # sanity checks
    assert isinstance(
        operand.target,
        (
            AsmletOperandRegister,
            AsmletOperandAddress,
        ),
    )

    index: Index | None = None

    if isinstance(operand.target, AsmletOperandAddress):
        index = (
            Index(
                scale=operand.target.indx.scale,
                reg=Register(name=operand.target.indx.reg.name),
            )
            if operand.target.indx is not None
            else None
        )

    if isinstance(operand.target, AsmletOperandAddress):
        disp = (
            Displacement(
                width=operand.target.disp.width,
                offset=operand.target.disp.offset,
                direction=operand.target.disp.direction,
            )
            if operand.target.disp is not None
            else None
        )

        return Address(
            size=operand.target.size,
            base=(
                Register(name=operand.target.base.name)
                if operand.target.base is not None
                else None
            ),
            indx=index,
            disp=disp,
        )

    return Register(name=operand.target.name)


def accept_reg_addr_rel(operand: AsmletOperand) -> Register | Address | tuple[Relocation, int]:
    # sanity checks
    assert isinstance(
        operand.target,
        (
            AsmletOperandRegister,
            AsmletOperandAddress,
            AsmletOperandRelocation,
        ),
    )

    index: Index | None = None

    if isinstance(operand.target, AsmletOperandRelocation):
        return Relocation(block=0), operand.target.offset

    if isinstance(operand.target, AsmletOperandAddress):
        index = (
            Index(
                scale=operand.target.indx.scale,
                reg=Register(name=operand.target.indx.reg.name),
            )
            if operand.target.indx is not None
            else None
        )

    if isinstance(operand.target, AsmletOperandAddress):
        disp = (
            Displacement(
                width=operand.target.disp.width,
                offset=operand.target.disp.offset,
                direction=operand.target.disp.direction,
            )
            if operand.target.disp is not None
            else None
        )

        return Address(
            size=operand.target.size,
            base=(
                Register(name=operand.target.base.name)
                if operand.target.base is not None
                else None
            ),
            indx=index,
            disp=disp,
        )

    return Register(name=operand.target.name)


def accept_reg_imm(operand: AsmletOperand) -> Register | Immediate:
    # sanity checks
    assert isinstance(
        operand.target,
        (
            AsmletOperandRegister,
            AsmletOperandImmediate,
        ),
    )

    if isinstance(operand.target, AsmletOperandImmediate):
        return Immediate(value=operand.target.value)

    return Register(name=operand.target.name)


def accept_reg_imm_addr(operand: AsmletOperand) -> Register | Immediate | Address:
    # sanity checks
    assert isinstance(
        operand.target,
        (
            AsmletOperandRegister,
            AsmletOperandImmediate,
            AsmletOperandAddress,
        ),
    )

    index: Index | None = None

    if isinstance(operand.target, AsmletOperandAddress):
        index = (
            Index(
                scale=operand.target.indx.scale,
                reg=Register(name=operand.target.indx.reg.name),
            )
            if operand.target.indx is not None
            else None
        )

    if isinstance(operand.target, AsmletOperandImmediate):
        return Immediate(value=operand.target.value)

    if isinstance(operand.target, AsmletOperandAddress):
        disp = (
            Displacement(
                width=operand.target.disp.width,
                offset=operand.target.disp.offset,
                direction=operand.target.disp.direction,
            )
            if operand.target.disp is not None
            else None
        )

        return Address(
            size=operand.target.size,
            base=(
                Register(name=operand.target.base.name)
                if operand.target.base is not None
                else None
            ),
            indx=index,
            disp=disp,
        )

    return Register(name=operand.target.name)


def emit_fnlets(
    generator: Generator,
    fnlets: OneToOne[FunctionId, Fnlet],
    entrypoints: OneToOne[SignatureId, Entrypoint],
) -> Iterable[tuple[BlockletId, Blocklet]]:

    for fid, fnlet in fnlets.items():
        blocks: list[BlockletBlock] = []

        for block in fnlet.blocks:
            blocks.append(
                BlockletBlock(
                    instructions=[instruction for instruction in block.instructions]
                )
            )

        blocklet = Blocklet(
            ref=fnlet.ref,
            target=fid,
            id=BlockletId(value=generator.next()),
            entrypoint=entrypoints.contains(fnlet.signature.id),
            blocks=blocks,
        )

        yield blocklet.id, blocklet


class ListExtractor:
    def __init__(self, data: OneToOne[BlockletId, Blocklet]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[
        tuple[tuple[BlockletId, Span, BlockletTarget], tuple[int, BlockletBlock]]
    ]:
        for bid, blocklet in self.data.items():
            for idx, block in enumerate(blocklet.blocks):
                yield (bid, blocklet.ref, blocklet.target), (idx, block)

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "blocklet": "Blocklet",
            "target": "Target",
            "idx": "Block Index",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(
        key: tuple[BlockletId, Span, BlockletTarget], entry: tuple[int, BlockletBlock]
    ) -> dict[str, str]:
        return {
            "ref": str(key[1]),
            "blocklet": key[0].identify(1),
            "target": key[2].identify(1),
            "idx": str(entry[0]),
            "instrs": str(len(entry[1].instructions)),
        }
