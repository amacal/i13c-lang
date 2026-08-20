from collections.abc import Callable, Iterable
from dataclasses import dataclass

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
from i13c.semantic.typing.analyses.fnlets import Fnlet
from i13c.semantic.typing.analyses.llvm import (
    AND,
    BSWAP,
    JMP,
    LEA,
    LOOP,
    MOV,
    NOP,
    OR,
    RET,
    SHL,
    SHR,
    SYSCALL,
    XCHG,
    Address,
    Immediate,
    Register,
    Relocation,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span


def configure_blocklets() -> GraphNode:
    return GraphNode(
        builder=build_blocklets,
        constraint=None,
        produces=("analyses/blocklets",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("asmlets", "analyses/asmlets"),
                ("fnlets", "analyses/fnlets"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_blocklets(
    generator: Generator,
    asmlets: OneToOne[AsmletId, Asmlet],
    fnlets: OneToOne[FunctionId, Fnlet],
) -> OneToOne[BlockletId, Blocklet]:
    blocklets: dict[BlockletId, Blocklet] = {}

    for bid, blocklet in emit_asmlets(generator, asmlets):
        blocklets[bid] = blocklet

    for bid, blocklet in emit_fnlets(generator, fnlets):
        blocklets[bid] = blocklet

    return OneToOne[BlockletId, Blocklet].instance(blocklets)


@dataclass(kw_only=True, repr=False)
class EmitRelocation:
    target: EmitRelocatable
    offset: int


EmitRelocatable = LOOP | JMP
EmitRelocated = tuple[BlockletInstruction, EmitRelocation | None]
EmitSignature = Callable[[list[AsmletOperand]], EmitRelocated]


def emit_asmlets(
    generator: Generator,
    asmlets: OneToOne[AsmletId, Asmlet],
) -> Iterable[tuple[BlockletId, Blocklet]]:

    dispatch: dict[bytes, EmitSignature] = {
        b"mov": emit_mov,
        b"bswap": emit_bswap,
        b"xchg": emit_xchg,
        b"nop": emit_nop,
        b"jmp": emit_jmp,
        b"syscall": emit_syscall,
        b"and": emit_and,
        b"or": emit_or,
        b"lea": emit_lea,
        b"ret": emit_ret,
        b"shr": emit_shr,
        b"shl": emit_shl,
        b"loop": emit_loop,
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

    dst = accept_reg(operands[0])
    src = accept_reg(operands[1])

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


def emit_jmp(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1
    assert isinstance(operands[0].target, AsmletOperandRelocation)

    instruction = JMP(operands=(Relocation(block=0),))
    relocation = EmitRelocation(target=instruction, offset=operands[0].target.offset)

    return instruction, relocation


def emit_syscall(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 0

    # just emit a SYSCALL instruction
    return SYSCALL(), None


def emit_and(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg(operands[0])
    src = accept_reg_imm(operands[1])

    return AND(operands=(dst, src)), None


def emit_or(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg(operands[0])
    src = accept_reg_imm(operands[1])

    return OR(operands=(dst, src)), None


def emit_lea(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg(operands[0])
    src = accept_addr(operands[1])

    return LEA(operands=(dst, src)), None


def emit_shr(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg(operands[0])
    src = accept_reg_imm(operands[1])

    return SHR(operands=(dst, src)), None


def emit_shl(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    dst = accept_reg(operands[0])
    src = accept_reg_imm(operands[1])

    return SHL(operands=(dst, src)), None


def emit_loop(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    assert isinstance(operands[0].target, AsmletOperandRelocation)

    instruction = LOOP(operands=(Relocation(block=0),))
    relocation = EmitRelocation(target=instruction, offset=operands[0].target.offset)

    return instruction, relocation


def accept_reg(operand: AsmletOperand) -> Register:
    # sanity checks
    assert isinstance(operand.target, AsmletOperandRegister)

    return Register(name=operand.target.name)


def accept_addr(operand: AsmletOperand) -> Address:
    # sanity checks
    assert isinstance(operand.target, AsmletOperandAddress)

    return Address(
        base=Register(name=operand.target.base.name),
        disp=operand.target.displacement,
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

    if isinstance(operand.target, AsmletOperandAddress):
        return Address(
            base=Register(name=operand.target.base.name),
            disp=operand.target.displacement,
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

    if isinstance(operand.target, AsmletOperandImmediate):
        return Immediate(value=operand.target.value)

    if isinstance(operand.target, AsmletOperandAddress):
        return Address(
            base=Register(name=operand.target.base.name),
            disp=operand.target.displacement,
        )

    return Register(name=operand.target.name)


def emit_fnlets(
    generator: Generator,
    fnlets: OneToOne[FunctionId, Fnlet],
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
