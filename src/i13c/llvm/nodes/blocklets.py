from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from functools import partial
from typing import Protocol

from i13c.core.generator import Generator
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.llvm.nodes.shuffles import transfer
from i13c.llvm.typing.allocations import Allocation, AllocationSegment
from i13c.llvm.typing.blocklets import (
    Blocklet,
    BlockletBlock,
    BlockletId,
    BlockletInstruction,
    BlockletTarget,
)
from i13c.llvm.typing.shuffles import (
    Coloring,
    InMemory,
    InRegister,
    Location,
    Shuffle,
    Transfer,
)
from i13c.semantic.typing.analyses.asmlets import (
    Asmlet,
    AsmletId,
    AsmletOperand,
    AsmletOperandAddress,
    AsmletOperandDisplacement,
    AsmletOperandImmediate,
    AsmletOperandRegister,
    AsmletOperandRelocation,
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
    EPILOG,
    JMP,
    LEA,
    LOOP,
    LOOPE,
    LOOPNE,
    MOV,
    NOP,
    OR,
    POP,
    PROLOG,
    PUSH,
    RCL,
    RCR,
    RET,
    ROL,
    ROR,
    SAL,
    SAR,
    SBB,
    SHL,
    SHR,
    SUB,
    SYSCALL,
    XCHG,
    XOR,
    Address,
    Displacement,
    Group1Instruction,
    Group1Operands,
    Group2Instruction,
    Group2Operands,
    Immediate,
    Index,
    LoopInstruction,
    LoopOperands,
    Register,
    Relocation,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.syntax.source import Span


def configure_blocklets() -> GraphGroup:
    configure = GraphNode(
        builder=build_configuration,
        constraint=None,
        produces=("configuration/blocklets",),
        requires=frozenset({}),
        views=GraphViews(list=ConfigurationExtractor),
    )

    resolve = GraphNode(
        builder=build_blocklets,
        constraint=None,
        produces=("analyses/blocklets",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("entrypoints", "analyses/entrypoints"),
                ("asmlets", "analyses/asmlets"),
                ("fnlets", "analyses/fnlets"),
                ("shuffles", "llvm/shuffles"),
                ("allocations", "llvm/allocations"),
                ("configuration", "configuration/blocklets"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )

    return GraphGroup(nodes=[configure, resolve])


GROUP1: list[tuple[bytes, type[Group1Instruction]]] = [
    (b"adc", ADC),
    (b"add", ADD),
    (b"and", AND),
    (b"cmp", CMP),
    (b"or", OR),
    (b"sbb", SBB),
    (b"sub", SUB),
    (b"xor", XOR),
]

GROUP2: list[tuple[bytes, type[Group2Instruction]]] = [
    (b"rol", ROL),
    (b"ror", ROR),
    (b"sal", SAL),
    (b"sar", SAR),
    (b"shl", SHL),
    (b"shr", SHR),
    (b"rcl", RCL),
    (b"rcr", RCR),
]

LOOPS: list[tuple[bytes, type[LoopInstruction]]] = [
    (b"loop", LOOP),
    (b"loope", LOOPE),
    (b"loopne", LOOPNE),
]


def build_configuration() -> OneToOne[bytes, BlockletEmit]:
    data: dict[bytes, BlockletEmit] = {}

    dispatch: dict[bytes, EmitSignature] = {
        b"bswap": emit_bswap,
        b"call": emit_call,
        b"jmp": emit_jmp,
        b"lea": emit_lea,
        b"mov": emit_mov,
        b"nop": emit_nop,
        b"pop": emit_pop,
        b"push": emit_push,
        b"ret": emit_ret,
        b"syscall": emit_syscall,
        b"xchg": emit_xchg,
    }

    # group 1 registration
    for mnemonic, clazz in GROUP1:
        data[mnemonic] = BlockletEmit(
            mnemonic=mnemonic,
            signature=partial(emit_group1, clazz),
        )

    # group 2 registration
    for mnemonic, clazz in GROUP2:
        data[mnemonic] = BlockletEmit(
            mnemonic=mnemonic,
            signature=partial(emit_group2, clazz),
        )

    # loop registration
    for mnemonic, clazz in LOOPS:
        data[mnemonic] = BlockletEmit(
            mnemonic=mnemonic,
            signature=partial(emit_loop, clazz),
        )

    # free instruction registration
    for mnemonic, signature in dispatch.items():
        data[mnemonic] = BlockletEmit(
            mnemonic=mnemonic,
            signature=signature,
        )

    return OneToOne[bytes, BlockletEmit].instance(data)


def build_blocklets(
    generator: Generator,
    configuration: OneToOne[bytes, BlockletEmit],
    entrypoints: OneToOne[SignatureId, Entrypoint],
    asmlets: OneToOne[AsmletId, Asmlet],
    fnlets: OneToOne[FunctionId, Fnlet],
    shuffles: OneToOne[FunctionId, Shuffle],
    allocations: OneToOne[FunctionId, Allocation],
) -> OneToOne[BlockletId, Blocklet]:
    blocklets: dict[BlockletId, Blocklet] = {}

    for bid, blocklet in emit_asmlets(generator, asmlets, entrypoints, configuration):
        blocklets[bid] = blocklet

    for bid, blocklet in emit_fnlets(
        generator, fnlets, entrypoints, shuffles, allocations
    ):
        blocklets[bid] = blocklet

    return OneToOne[BlockletId, Blocklet].instance(blocklets)


@dataclass(kw_only=True, repr=False)
class EmitRelocation:
    target: BlockletInstruction
    placeholder: Relocation
    offset: int


EmitRelocated = tuple[BlockletInstruction, list[EmitRelocation]]
EmitSignature = Callable[[list[AsmletOperand]], EmitRelocated]
Relocatable = tuple[Relocation, int]


@dataclass(kw_only=True, repr=False)
class BlockletEmit:
    mnemonic: bytes
    signature: EmitSignature


def into_relocations(
    relocations: list[Relocatable], target: BlockletInstruction
) -> list[EmitRelocation]:
    return [
        EmitRelocation(target=target, placeholder=entry[0], offset=entry[1])
        for entry in relocations
    ]


def emit_asmlets(
    generator: Generator,
    asmlets: OneToOne[AsmletId, Asmlet],
    entrypoints: OneToOne[SignatureId, Entrypoint],
    configuration: OneToOne[bytes, BlockletEmit],
) -> Iterable[tuple[BlockletId, Blocklet]]:

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

                if isinstance(operand.target, AsmletOperandAddress):
                    if isinstance(operand.target.disp, AsmletOperandRelocation):
                        fixes[idx + operand.target.disp.offset] = 0

        # emit all instructions, and collect relocations
        for idx, instr in enumerate(entry.instructions):
            emit = configuration.get(instr.mnemonic)
            instruction, relocation = emit.signature(instr.operands)

            # start a new block if this instruction is a split point
            if idx in fixes and instructions:
                blocks.append(BlockletBlock(instructions=instructions))
                fixes[idx] = len(blocks)
                instructions = []

            for rel in relocation or []:
                relocations.append((idx, rel))

            instructions.append(instruction)

        # if there are any remaining instructions, add them as a block
        if instructions:
            blocks.append(BlockletBlock(instructions=instructions))

        # apply relocations to the instructions
        for idx, relocation in relocations:
            relocation.placeholder.block = fixes[idx + relocation.offset]

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

    # two operands
    dst = accept_reg_addr(operands[0])
    src = accept_reg_imm_addr(operands[1])

    # prepare a list to collect relocations
    relocations: list[Relocatable] = []

    # unwrap destination if it contains a relocation
    if isinstance(dst, tuple):
        assert isinstance(dst[0].disp, Relocation)
        relocations.append((dst[0].disp, dst[1]))
        dst = dst[0]

    # unwrap source if it contains a relocation
    if isinstance(src, tuple):
        assert isinstance(src[0].disp, Relocation)
        relocations.append((src[0].disp, src[1]))
        src = src[0]

    # create the instruction
    instruction = MOV(operands=(dst, src))

    # convert relocations to EmitRelocation instances
    return (instruction, into_relocations(relocations, instruction))


def emit_bswap(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # one operand
    dst = accept_reg(operands[0])

    # create the instruction
    return BSWAP(operands=(dst,)), []


def emit_xchg(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    # extract operands
    dst = accept_reg_addr(operands[0])
    src = accept_reg_addr(operands[1])

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap destination if relocated
    if isinstance(dst, tuple):
        assert isinstance(dst[0].disp, Relocation)
        relocations.append((dst[0].disp, dst[1]))
        dst = dst[0]

    # unwrap source if relocated
    if isinstance(src, tuple):
        assert isinstance(src[0].disp, Relocation)
        relocations.append((src[0].disp, src[1]))
        src = src[0]

    # create the instruction
    instruction = XCHG(operands=(dst, src))

    # convert relocations to EmitRelocation instances
    return (instruction, into_relocations(relocations, instruction))


def emit_nop(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 0

    # just emit a NOP instruction
    return NOP(operands=()), []


def emit_ret(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 0

    # just emit a RET instruction
    return RET(operands=()), []


def emit_call(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # the target must be either a relocation or an address
    target = accept_reg_addr_rel(operands[0])

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap target if relocated
    if isinstance(target, tuple):
        if isinstance(target[0], Relocation):
            relocations.append((target[0], target[1]))
            target = target[0]
        else:
            assert isinstance(target[0].disp, Relocation)
            relocations.append((target[0].disp, target[1]))
            target = target[0]

    # create the CALL instruction
    instruction = CALL(operands=(target,), args={}, clobbers=[])

    # convert relocations to EmitRelocation instances
    return instruction, into_relocations(relocations, instruction)


def emit_jmp(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # the target must be either a relocation or an address
    target = accept_reg_addr_rel(operands[0])

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap target if relocated
    if isinstance(target, tuple):
        if isinstance(target[0], Relocation):
            relocations.append((target[0], target[1]))
            target = target[0]
        else:
            assert isinstance(target[0].disp, Relocation)
            relocations.append((target[0].disp, target[1]))
            target = target[0]

    # create the JMP instruction
    instruction = JMP(operands=(target,))

    # convert relocations to EmitRelocation instances
    return instruction, into_relocations(relocations, instruction)


def emit_syscall(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 0

    # just emit a SYSCALL instruction
    return SYSCALL(operands=()), []


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

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap destination if relocated
    if isinstance(dst, tuple):
        assert isinstance(dst[0].disp, Relocation)
        relocations.append((dst[0].disp, dst[1]))
        dst = dst[0]

    # unwrap source if relocated
    if isinstance(src, tuple):
        assert isinstance(src[0].disp, Relocation)
        relocations.append((src[0].disp, src[1]))
        src = src[0]

    # create the instruction
    instruction = op(operands=(dst, src))

    # convert relocations to EmitRelocation instances
    return instruction, into_relocations(relocations, instruction)


def emit_group2[T: Group2Instruction](
    op: Group2Constructor[T],
    operands: list[AsmletOperand],
) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    # two operands
    dst = accept_reg_addr(operands[0])
    src = accept_reg_imm(operands[1])

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap destination if relocated
    if isinstance(dst, tuple):
        assert isinstance(dst[0].disp, Relocation)
        relocations.append((dst[0].disp, dst[1]))
        dst = dst[0]

    # create the instruction
    instruction = op(operands=(dst, src))

    # convert relocations to EmitRelocation instances
    return instruction, into_relocations(relocations, instruction)


def emit_loop[T: LoopInstruction](
    op: LoopConstructor[T],
    operands: list[AsmletOperand],
) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # one relocation operand
    assert isinstance(operands[0].target, AsmletOperandRelocation)

    # one operand
    target = operands[0].target

    placeholder = Relocation(block=0)
    instruction = op(operands=(placeholder,))

    relocation = EmitRelocation(
        target=instruction,
        placeholder=placeholder,
        offset=target.offset,
    )

    return instruction, [relocation]


def emit_lea(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 2

    # two operands
    dst = accept_reg(operands[0])
    src = accept_addr(operands[1])

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap source if relocated
    if isinstance(src, tuple):
        assert isinstance(src[0].disp, Relocation)
        relocations.append((src[0].disp, src[1]))
        src = src[0]

    # create the instruction
    instruction = LEA(operands=(dst, src))

    # convert relocations to EmitRelocation instances
    return instruction, into_relocations(relocations, instruction)


def emit_pop(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # one operand
    dst = accept_reg_addr(operands[0])

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap destination if relocated
    if isinstance(dst, tuple):
        assert isinstance(dst[0].disp, Relocation)
        relocations.append((dst[0].disp, dst[1]))
        dst = dst[0]

    # create the instruction
    instruction = POP(operands=(dst,))

    # convert relocations to EmitRelocation instances
    return instruction, into_relocations(relocations, instruction)


def emit_push(operands: list[AsmletOperand]) -> EmitRelocated:
    # sanity checks
    assert len(operands) == 1

    # one operand
    dst = accept_reg_imm_addr(operands[0])

    # prepare relocations list
    relocations: list[Relocatable] = []

    # unwrap destination if relocated
    if isinstance(dst, tuple):
        assert isinstance(dst[0].disp, Relocation)
        relocations.append((dst[0].disp, dst[1]))
        dst = dst[0]

    # create the instruction
    instruction = PUSH(operands=(dst,))

    # convert relocations to EmitRelocation instances
    return instruction, into_relocations(relocations, instruction)


def convert_addr(operand: AsmletOperandAddress) -> Address | tuple[Address, int]:
    index = (
        Index(
            scale=operand.indx.scale,
            reg=Register(name=operand.indx.reg.name),
        )
        if operand.indx is not None
        else None
    )

    # default values
    disp: Displacement | Relocation | None = None
    relocation: int | None = None

    # decide if the displacement is a regular displacement
    if isinstance(operand.disp, AsmletOperandDisplacement):
        disp = Displacement(
            width=operand.disp.width,
            offset=operand.disp.offset,
            direction=operand.disp.direction,
        )

    # decide if the displacement has to be relocated
    if isinstance(operand.disp, AsmletOperandRelocation):
        disp, relocation = Relocation(block=0), operand.disp.offset

    address = Address(
        size=operand.size,
        base=(Register(name=operand.base.name) if operand.base is not None else None),
        indx=index,
        disp=disp,
    )

    # decide if to return just address or address with relocation
    if relocation is not None:
        return address, relocation

    else:
        return address


def accept_reg(operand: AsmletOperand) -> Register:
    # sanity checks
    assert isinstance(operand.target, AsmletOperandRegister)

    return Register(name=operand.target.name)


def accept_addr(operand: AsmletOperand) -> Address | tuple[Address, int]:
    # sanity checks
    assert isinstance(operand.target, AsmletOperandAddress)

    # follow address path
    return convert_addr(operand.target)


def accept_reg_addr(operand: AsmletOperand) -> Register | Address | tuple[Address, int]:
    # sanity checks
    assert isinstance(
        operand.target,
        (
            AsmletOperandRegister,
            AsmletOperandAddress,
        ),
    )

    if isinstance(operand.target, AsmletOperandRegister):
        return Register(name=operand.target.name)

    return convert_addr(operand.target)


def accept_reg_addr_rel(
    operand: AsmletOperand,
) -> Register | Address | tuple[Relocation, int] | tuple[Address, int]:
    # sanity checks
    assert isinstance(
        operand.target,
        (
            AsmletOperandRegister,
            AsmletOperandAddress,
            AsmletOperandRelocation,
        ),
    )

    if isinstance(operand.target, AsmletOperandAddress):
        return convert_addr(operand.target)

    elif isinstance(operand.target, AsmletOperandRelocation):
        return Relocation(block=0), operand.target.offset

    else:
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


def accept_reg_imm_addr(
    operand: AsmletOperand,
) -> Register | Immediate | Address | tuple[Address, int]:
    # sanity checks
    assert isinstance(
        operand.target,
        (
            AsmletOperandRegister,
            AsmletOperandImmediate,
            AsmletOperandAddress,
        ),
    )

    if isinstance(operand.target, AsmletOperandAddress):
        return convert_addr(operand.target)

    elif isinstance(operand.target, AsmletOperandImmediate):
        return Immediate(value=operand.target.value)

    else:
        return Register(name=operand.target.name)


def emit_fnlets(
    generator: Generator,
    fnlets: OneToOne[FunctionId, Fnlet],
    entrypoints: OneToOne[SignatureId, Entrypoint],
    shuffles: OneToOne[FunctionId, Shuffle],
    allocations: OneToOne[FunctionId, Allocation],
) -> Iterable[tuple[BlockletId, Blocklet]]:

    for fid, fnlet in fnlets.items():
        blocks: list[BlockletBlock] = []
        shuffle: Shuffle = shuffles.get(fid)
        allocation: Allocation = allocations.get(fid)

        for idx, block in enumerate(fnlet.blocks):
            instructions: list[BlockletInstruction] = []
            segment: AllocationSegment = allocation.segments[idx]

            palette = allocation.palette
            registers = allocation.registers

            scratch = Register(name=b"r11")
            transfer = shuffle.transfer

            if before := shuffle.segments[idx]:
                instructions.extend(before.before)

            # rewrite the instructions for the block according to the colors
            for instruction in block.instructions:
                match instruction:
                    case PROLOG():
                        instructions.extend(
                            emit_prologue(
                                allocation,
                                instruction.preserves,
                            )
                        )

                    case EPILOG():
                        instructions.extend(
                            emit_epilogue(
                                allocation,
                                instruction.preserves,
                            )
                        )

                    case MOV():
                        instructions.extend(
                            rewrite_mov(
                                instruction,
                                scratch,
                                registers,
                                palette,
                                segment,
                            )
                        )

                    case CALL():
                        instructions.extend(
                            rewrite_call(
                                instruction,
                                transfer,
                                scratch,
                                registers,
                                palette,
                                segment,
                            )
                        )

                    case instr:
                        instructions.append(instr)

            # construct the blocklet block with the accumulated instructions
            blocks.append(BlockletBlock(instructions=instructions))

            if after := shuffle.segments[idx]:
                instructions.extend(after.after)

        blocklet = Blocklet(
            ref=fnlet.ref,
            target=fid,
            id=BlockletId(value=generator.next()),
            entrypoint=entrypoints.contains(fnlet.signature.id),
            blocks=blocks,
        )

        yield blocklet.id, blocklet


def emit_prologue(
    allocation: Allocation,
    preserves: list[Register],
) -> list[BlockletInstruction]:
    instructions: list[BlockletInstruction] = []
    used = allocation.get_used()

    # save preserved registers
    for reg in preserves:
        if reg.name in used:
            instructions.append(PUSH(operands=(reg,)))

    # reserve stack space for local variables
    if slots := allocation.get_slots():
        width = slots * 8

        instructions.append(
            SUB(
                operands=(
                    Register(name=b"rsp"),
                    Immediate.derive(width.to_bytes(4, "big")),
                )
            )
        )

    return instructions


def emit_epilogue(
    allocation: Allocation,
    preserves: list[Register],
) -> list[BlockletInstruction]:
    instructions: list[BlockletInstruction] = []
    used: set[bytes] = allocation.get_used()

    # release stack space for local variables
    if slots := allocation.get_slots():
        width = slots * 8

        instructions.append(
            ADD(
                operands=(
                    Register(name=b"rsp"),
                    Immediate.derive(width.to_bytes(4, "big")),
                )
            ),
        )

    # restore preserved registers
    for reg in reversed(preserves):
        if reg.name in used:
            instructions.append(POP(operands=(reg,)))

    instructions.append(
        RET(operands=()),
    )

    return instructions


def rewrite_call(
    instruction: CALL,
    transfer: Transfer,
    scratch: Register,
    registers: list[bytes],
    palette: list[bytes],
    segment: AllocationSegment,
) -> Sequence[CALL | MOV | XCHG]:
    def into_location(src: bytes) -> Location:
        idx = registers.index(src)

        if idx not in segment.colors:
            return InMemory(slot=segment.spills[idx])
        else:
            return InRegister(name=palette[segment.colors[idx]])

    src: Coloring = {
        dst: into_location(src.name)
        for dst, src in instruction.args.items()
        if isinstance(src, Register)
    }

    dst: Coloring = {
        dst: InRegister(name=dst)
        for dst, src in instruction.args.items()
        if isinstance(src, Register)
    }

    # perform the transfer using the scratch register
    instructions = transfer(InRegister(name=scratch.name), src, dst)

    # handle immediate operands separately
    for op1, op2 in instruction.args.items():
        if isinstance(op2, Immediate):
            op1 = Register(name=op1)

            if op2.width() < 64:
                op1 = op1.resize(32)

                if op2.width() < 32:
                    op2 = op2.resize(32)

            instructions.append(MOV(operands=(op1, op2)))

    call = CALL(
        operands=instruction.operands,
        args={},
        clobbers=[],
    )

    return instructions + [call]


def address(offset: int) -> Address:
    # short offsets can use 8-bit displacement
    width = 8 if offset < 128 else 32

    return Address(
        size=64,
        base=Register(name=b"rsp"),
        indx=None,
        disp=Displacement(
            width=width,
            direction="forward",
            offset=offset.to_bytes(width // 8, "big"),
        ),
    )


def rewrite_mov(
    instruction: MOV,
    scratch: Register,
    registers: list[bytes],
    palette: list[bytes],
    segment: AllocationSegment,
) -> list[MOV]:
    changed: bool = False
    results: list[MOV] = [instruction]

    # extract operands
    dst: Register | Address | None = instruction.operands[0]
    src: Register | Address | Immediate | None = instruction.operands[1]

    # dst has to be changed
    if isinstance(dst, Register):
        if dst.name in registers:
            idx = registers.index(dst.name)
            if idx in segment.colors:
                dst = Register(name=palette[segment.colors[idx]])
                changed = True

            elif idx in segment.spills:
                dst = address(8 * segment.spills[idx])
                changed = True

    # src has to be changed
    if isinstance(src, Register):
        if src.name in registers:
            idx = registers.index(src.name)
            if idx in segment.colors:
                src = Register(name=palette[segment.colors[idx]])
                changed = True

            elif idx in segment.spills:
                src = address(8 * segment.spills[idx])
                changed = True

    # not colored register indicates dead code
    if isinstance(dst, Register):
        if dst.name not in palette:
            dst, changed = None, True

    # not colored register indicates dead code
    if isinstance(src, Register):
        if src.name not in palette:
            src, changed = None, True

    # both operands must be resized
    if isinstance(src, Immediate) and dst is not None:
        if src.width() < 64:
            dst = dst.resize(32)
            changed = True

            if src.width() < 32:
                src = src.resize(32)

    # dead code? emit nothing
    if src is None or dst is None:
        return []

    # anything changed, try to optimize the move
    elif changed:
        if str(dst) == str(src):
            results = []
        else:
            results = [MOV(operands=(dst, src))]

    if results:
        src_is_address = isinstance(results[0].operands[1], Address)
        dst_is_address = isinstance(results[0].operands[0], Address)

        # there is no mem-to-mem move, use the scratch register to avoid it
        if src_is_address and dst_is_address:
            results = [
                MOV(operands=(scratch, results[0].operands[1])),
                MOV(operands=(results[0].operands[0], scratch)),
            ]

        # there is no imm64-to-mem move, use the scratch register to avoid it
        elif dst_is_address:
            if isinstance(results[0].operands[1], Immediate):
                if results[0].operands[1].width() == 64:
                    results = [
                        MOV(operands=(scratch, results[0].operands[1])),
                        MOV(operands=(results[0].operands[0], scratch)),
                    ]

    return results


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


class ConfigurationExtractor:
    def __init__(self, data: OneToOne[bytes, BlockletEmit]):
        self.data = data

    def extract(self) -> Iterable[tuple[bytes, BlockletEmit]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {"mnemonic": "Mnemonic", "emit": "Emitter"}

    @staticmethod
    def rows(key: bytes, entry: BlockletEmit) -> dict[str, str]:
        return {
            "mnemonic": key.decode("utf-8"),
            "emit": str(entry),
        }


def can_rewrite_mov_leave_a_move_between_two_untracked_physical_registers_unchanged():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={}, spills={})
    instruction = MOV(operands=(Register(name=b"rdx"), Register(name=b"rax")))

    # neither side is a tracked vreg, so nothing here is a candidate for
    # recoloring, resizing, or dead-code elimination
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert result == [instruction]


def can_rewrite_mov_recolor_both_operands_of_a_register_to_register_move():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 0, 1: 1}, spills={})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"v1")))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov rdi, rsi"]


def can_rewrite_mov_eliminate_a_register_move_that_becomes_a_self_move_after_recoloring():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # v0 and v1 land in the same palette register: the copy is a no-op
    segment = AllocationSegment(colors={0: 0, 1: 0}, spills={})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"v1")))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert result == []


def can_rewrite_mov_recolor_only_the_side_that_is_a_tracked_vreg():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 2}, spills={})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"rax")))

    # rax is already a real register, never a vreg, so only v0 is recolored
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov rdx, rax"]


def can_rewrite_mov_keep_a_full_width_immediate_untouched_when_dst_is_colored():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 4}, spills={})
    immediate = Immediate.derive(
        bytes([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF])
    )
    instruction = MOV(operands=(Register(name=b"v0"), immediate))

    # a 64-bit-wide immediate never enters the narrowing branch at all
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov rax, 0x0123456789abcdef"]


def can_rewrite_mov_eliminate_a_dead_store_of_a_full_width_immediate():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # v0 never appears in colors or spills: liveness already decided it's dead
    segment = AllocationSegment(colors={}, spills={})
    immediate = Immediate.derive(
        bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05])
    )
    instruction = MOV(operands=(Register(name=b"v0"), immediate))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert result == []


def can_rewrite_mov_eliminate_a_dead_register_to_register_copy():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={}, spills={})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"v1")))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert result == []


def can_rewrite_mov_eliminate_a_move_when_only_its_destination_is_dead():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # v1 is perfectly live elsewhere; it's v0 (the destination) that's dead,
    # and a dead destination makes the whole store pointless regardless
    segment = AllocationSegment(colors={1: 1}, spills={})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"v1")))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert result == []


def can_rewrite_mov_pass_a_genuine_memory_to_memory_move_through_the_scratch_register():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # neither operand is a Register at all here, so this exercises the
    # mem-to-mem branch directly, independent of any vreg recoloring
    segment = AllocationSegment(colors={}, spills={})
    instruction = MOV(operands=(address(0), address(8)))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == [
        "mov r11, qword [rsp + 0x08]",
        "mov qword [rsp + 0x00], r11",
    ]


def can_rewrite_mov_resize_a_memory_destination_when_storing_a_narrow_immediate():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={}, spills={})
    immediate = Immediate.derive(bytes([0x01]))
    instruction = MOV(operands=(address(0), immediate))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov dword [rsp + 0x00], 0x00000001"]


def can_rewrite_mov_store_an_immediate_into_a_spilled_destination():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # v0 is spilled and live; x86-64 has no mov-mem-imm64 encoding, so a
    # 64-bit-wide value must route through the scratch register
    segment = AllocationSegment(colors={}, spills={0: 0})
    immediate = Immediate.derive(
        bytes([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF])
    )
    instruction = MOV(operands=(Register(name=b"v0"), immediate))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == [
        "mov r11, 0x0123456789abcdef",
        "mov qword [rsp + 0x00], r11",
    ]


def can_rewrite_mov_load_a_spilled_source_into_a_colored_destination():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 0}, spills={1: 3})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"v1")))

    # v1's value sits in memory now, so reading it must be a load, not a drop
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov rdi, qword [rsp + 0x18]"]


def can_rewrite_mov_load_a_spilled_source_through_a_32_bit_displacement():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 0}, spills={1: 16})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"v1")))

    # slot 16 sits at offset 128, one past what an 8-bit displacement can reach
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov rdi, qword [rsp + 0x00000080]"]


def can_rewrite_mov_shuffle_a_spill_to_spill_move_through_the_scratch_register():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # both sides are live values that happen to be spilled to different
    # slots: the value must still cross memory via the scratch register
    segment = AllocationSegment(colors={}, spills={0: 0, 1: 1})
    instruction = MOV(operands=(Register(name=b"v0"), Register(name=b"v1")))

    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == [
        "mov r11, qword [rsp + 0x08]",
        "mov qword [rsp + 0x00], r11",
    ]


def can_rewrite_mov_keep_a_colored_destination_alive_when_narrowing_a_sub_32_bit_immediate():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 4}, spills={})
    immediate = Immediate.derive(bytes([0x2A]))
    instruction = MOV(operands=(Register(name=b"v0"), immediate))

    # v0 is a live, correctly-colored register; narrowing rax to eax for a
    # short encoding must not be mistaken for an uncolored (dead) destination
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov eax, 0x0000002a"]


def can_rewrite_mov_keep_a_colored_destination_alive_when_narrowing_a_32_bit_immediate():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 1}, spills={})
    immediate = Immediate.derive(bytes([0x00, 0x00, 0x12, 0x34]))
    instruction = MOV(operands=(Register(name=b"v0"), immediate))

    # only the destination needs narrowing here; the immediate is already 32 bits
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert [str(m) for m in result] == ["mov esi, 0x00001234"]


def can_rewrite_mov_eliminate_a_dead_store_with_a_narrow_immediate():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={}, spills={})
    immediate = Immediate.derive(bytes([0x01]))
    instruction = MOV(operands=(Register(name=b"v0"), immediate))

    # v0 is dead, the instruction should be eliminated
    result = rewrite_mov(instruction, scratch, registers, palette, segment)

    assert result == []


def can_rewrite_call_move_a_colored_argument_into_its_required_register():
    registers = [b"v0"]
    palette = [b"rdi", b"rsi", b"rdx"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 1}, spills={})
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rdi": Register(name=b"v0")},
        clobbers=[],
    )

    result = rewrite_call(instruction, transfer, scratch, registers, palette, segment)

    assert [str(i) for i in result] == ["mov rdi, rsi", "call function#1"]


def can_rewrite_call_skip_the_move_when_the_argument_is_already_in_place():
    registers = [b"v0"]
    palette = [b"rdi", b"rsi", b"rdx"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 0}, spills={})
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rdi": Register(name=b"v0")},
        clobbers=[],
    )

    # v0 is already colored to rdi, exactly where the call needs it
    result = rewrite_call(instruction, transfer, scratch, registers, palette, segment)

    assert [str(i) for i in result] == ["call function#1"]


def can_rewrite_call_exchange_two_arguments_that_need_to_swap_registers():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi"]
    scratch = Register(name=b"r11")

    # v0 wants rdi but sits in rsi, v1 wants rsi but sits in rdi: a cycle
    segment = AllocationSegment(colors={0: 1, 1: 0}, spills={})
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rdi": Register(name=b"v0"), b"rsi": Register(name=b"v1")},
        clobbers=[],
    )

    result = rewrite_call(instruction, transfer, scratch, registers, palette, segment)

    assert [str(i) for i in result] == ["xchg rsi, rdi", "call function#1"]


def can_rewrite_call_load_an_immediate_argument_directly():
    # narrows to edi: mov r64,imm32 sign-extends, mov r32,imm32 zero-extends
    segment = AllocationSegment(colors={}, spills={})
    immediate = Immediate.derive(bytes([0x00, 0x00, 0x00, 0x2A]))
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rdi": immediate},
        clobbers=[],
    )

    result = rewrite_call(
        instruction, transfer, Register(name=b"r11"), [], [b"rdi", b"rsi"], segment
    )

    assert [str(i) for i in result] == ["mov edi, 0x0000002a", "call function#1"]


def can_rewrite_call_widen_a_byte_sized_immediate_argument_to_fit_its_register():
    # x86-64 has no mov r64, imm8 -- an 8-bit-wide argument value must be
    # widened to 32 bits, same as rewrite_mov already does for plain moves
    segment = AllocationSegment(colors={}, spills={})
    immediate = Immediate.derive(bytes([0x42]))
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rdi": immediate},
        clobbers=[],
    )

    result = rewrite_call(
        instruction, transfer, Register(name=b"r11"), [], [b"rdi", b"rsi"], segment
    )

    assert [str(i) for i in result] == ["mov edi, 0x00000042", "call function#1"]


def can_rewrite_call_widen_a_word_sized_immediate_argument_to_fit_its_register():
    # x86-64 has no mov r64, imm16 either -- same widening applies
    segment = AllocationSegment(colors={}, spills={})
    immediate = Immediate.derive(bytes([0x12, 0x34]))
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rdi": immediate},
        clobbers=[],
    )

    result = rewrite_call(
        instruction, transfer, Register(name=b"r11"), [], [b"rdi", b"rsi"], segment
    )

    assert [str(i) for i in result] == [
        "mov edi, 0x00001234",
        "call function#1",
    ]


def can_rewrite_call_combine_a_colored_register_argument_with_an_immediate_argument():
    registers = [b"v0"]
    palette = [b"rdi", b"rsi", b"rdx"]
    scratch = Register(name=b"r11")
    segment = AllocationSegment(colors={0: 2}, spills={})
    immediate = Immediate.derive(bytes([0x00, 0x00, 0x00, 0x07]))
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rdi": Register(name=b"v0"), b"rsi": immediate},
        clobbers=[],
    )

    result = rewrite_call(instruction, transfer, scratch, registers, palette, segment)

    assert [str(i) for i in result] == [
        "mov rdi, rdx",
        "mov esi, 0x00000007",
        "call function#1",
    ]


def can_rewrite_call_emit_a_bare_call_when_there_are_no_arguments():
    segment = AllocationSegment(colors={}, spills={})
    instruction = CALL(operands=(FunctionId(value=1),), args={}, clobbers=[])

    result = rewrite_call(
        instruction, transfer, Register(name=b"r11"), [], [b"rdi"], segment
    )

    assert [str(i) for i in result] == ["call function#1"]


def can_rewrite_call_strip_the_original_args_and_clobbers_from_the_rewritten_call():
    segment = AllocationSegment(colors={}, spills={})
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={},
        clobbers=[b"rax", b"rcx"],
    )

    result = rewrite_call(
        instruction, transfer, Register(name=b"r11"), [], [b"rdi"], segment
    )

    # the rewritten call carries no args/clobbers: they were only ever
    # needed to drive the reconciliation above, not the real call site
    call = result[-1]
    assert isinstance(call, CALL)
    assert call.args == {}
    assert call.clobbers == []


def can_rewrite_call_load_a_spilled_argument_from_its_assigned_slot_not_its_index():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # v0's registers-list index is 0, but it's spilled to slot 5 -- reading
    # it must use the slot, not the index that happens to also be a number
    segment = AllocationSegment(colors={}, spills={0: 5})
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rax": Register(name=b"v0")},
        clobbers=[],
    )

    result = rewrite_call(instruction, transfer, scratch, registers, palette, segment)

    assert [str(i) for i in result] == [
        "mov rax, qword [rsp + 0x28]",
        "call function#1",
    ]


def can_rewrite_call_load_two_spilled_arguments_whose_indices_and_slots_never_match():
    registers = [b"v0", b"v1"]
    palette = [b"rdi", b"rsi", b"rdx", b"rcx", b"rax"]
    scratch = Register(name=b"r11")

    # v0 (index 0) is spilled to slot 3, v1 (index 1) to slot 0: indices and
    # slots are fully crossed, so a slot-vs-index mixup can't hide by luck
    segment = AllocationSegment(colors={}, spills={0: 3, 1: 0})
    instruction = CALL(
        operands=(FunctionId(value=1),),
        args={b"rax": Register(name=b"v0"), b"rdi": Register(name=b"v1")},
        clobbers=[],
    )

    result = rewrite_call(instruction, transfer, scratch, registers, palette, segment)

    assert [str(i) for i in result] == [
        "mov rax, qword [rsp + 0x18]",
        "mov rdi, qword [rsp + 0x00]",
        "call function#1",
    ]


def can_emit_prologue_save_a_callee_saved_register_the_function_actually_uses():
    # v0 is colored to rbx, a callee-saved register the ABI requires this
    # function to preserve for its own caller
    allocation = Allocation(
        registers=[b"v0"],
        palette=[b"rbx", b"rbp"],
        clobbers=[],
        segments=[AllocationSegment(colors={0: 0}, spills={})],
        seeds=[],
    )

    preserves = [Register(name=b"rbx"), Register(name=b"rbp")]
    result = emit_prologue(allocation, preserves)

    # rbp is never colored anywhere, so it needs no save
    assert [str(i) for i in result] == ["push rbx"]


def can_emit_prologue_skip_callee_saved_registers_the_function_never_uses():
    allocation = Allocation(
        registers=[b"v0"],
        palette=[b"rdi"],
        clobbers=[],
        segments=[AllocationSegment(colors={0: 0}, spills={})],
        seeds=[],
    )

    preserves = [Register(name=b"rbx"), Register(name=b"rbp")]
    result = emit_prologue(allocation, preserves)

    # neither rbx nor rbp is ever colored, so no push is needed at all
    assert result == []


def can_emit_prologue_push_saved_registers_before_reserving_spill_slots():
    allocation = Allocation(
        registers=[b"v0", b"v1"],
        palette=[b"rbx"],
        clobbers=[],
        segments=[
            AllocationSegment(colors={0: 0}, spills={1: 0}),
        ],
        seeds=[],
    )

    preserves = [Register(name=b"rbx")]
    result = emit_prologue(allocation, preserves)

    # the push must come first: spill offsets are computed relative to rsp
    # as it stands after the frame is reserved, not before
    assert [str(i) for i in result] == [
        "push rbx",
        "sub rsp, 0x00000008",
    ]


def can_emit_prologue_save_a_callee_saved_register_clobbered_by_an_inner_call():
    # rbx is never colored to any vreg here -- an inner call to another
    # function is the only thing that touches it, e.g. a call whose own
    # argument-passing writes straight into rbx
    allocation = Allocation(
        registers=[],
        palette=[b"rbx"],
        clobbers=[b"rbx"],
        segments=[AllocationSegment(colors={}, spills={})],
        seeds=[],
    )

    preserves = [Register(name=b"rbx")]
    result = emit_prologue(allocation, preserves)

    assert [str(i) for i in result] == ["push rbx"]


def can_emit_epilogue_restore_callee_saved_registers_in_reverse_order():
    allocation = Allocation(
        registers=[b"v0", b"v1"],
        palette=[b"rbx", b"rbp"],
        clobbers=[],
        segments=[AllocationSegment(colors={0: 0, 1: 1}, spills={})],
        seeds=[],
    )

    preserves = [Register(name=b"rbx"), Register(name=b"rbp")]
    result = emit_epilogue(allocation, preserves)

    # last pushed, first popped -- otherwise the stack discipline breaks
    assert [str(i) for i in result] == [
        "pop rbp",
        "pop rbx",
        "ret",
    ]


def can_emit_epilogue_restore_saved_registers_after_releasing_spill_slots():
    allocation = Allocation(
        registers=[b"v0", b"v1"],
        palette=[b"rbx"],
        clobbers=[],
        segments=[AllocationSegment(colors={0: 0}, spills={1: 0})],
        seeds=[],
    )

    preserves = [Register(name=b"rbx")]
    result = emit_epilogue(allocation, preserves)

    # the frame must be released before rbx is popped back off the stack
    assert [str(i) for i in result] == [
        "add rsp, 0x00000008",
        "pop rbx",
        "ret",
    ]


def can_emit_epilogue_restore_a_callee_saved_register_clobbered_by_an_inner_call():
    allocation = Allocation(
        registers=[],
        palette=[b"rbx"],
        clobbers=[b"rbx"],
        segments=[AllocationSegment(colors={}, spills={})],
        seeds=[],
    )

    preserves = [Register(name=b"rbx")]
    result = emit_epilogue(allocation, preserves)

    assert [str(i) for i in result] == ["pop rbx", "ret"]
