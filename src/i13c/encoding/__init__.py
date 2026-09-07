from collections import defaultdict
from collections.abc import Iterable
from typing import Protocol

from i13c.encoding import addr, bits, ctrl, math, move, shifts, stack
from i13c.encoding.core import RelocationInfo
from i13c.semantic.typing.analyses import llvm
from i13c.semantic.typing.analyses.blocklets import (
    Blocklet,
    BlockletInstruction,
    BlockletTarget,
)

RelocationEntry = tuple[int, int, int]


def encode(blocklets: Iterable[Blocklet]) -> bytes:
    bytecode = bytearray()

    # collected global relocations
    global_relocations: dict[BlockletTarget, set[RelocationEntry]] = defaultdict(set)
    global_symbols: dict[BlockletTarget, int] = {}

    def serialize(value: int, width: int) -> bytes:
        return value.to_bytes(width, byteorder="little", signed=True)

    for blocklet in blocklets:
        # collect local relocations
        local_relocations: dict[int, set[RelocationEntry]] = defaultdict(set)
        local_symbols: dict[int, int] = {}

        # record the symbol of this blocklet
        global_symbols[blocklet.target] = len(bytecode)

        # handle each block, blocks are indexed by their position
        for idx, block in enumerate(blocklet.blocks):
            # record the symbol of this block
            local_symbols[idx] = len(bytecode)

            # encode each instruction in the block
            for instruction in block.instructions:
                if relocation := DISPATCH_TABLE[type(instruction)](
                    instruction, bytecode
                ):
                    # the end of the instruction, and the offset of the displacement
                    entry = (len(bytecode), relocation.offset, relocation.width)

                    # record the relocation in the appropriate table
                    if isinstance(relocation.target, int):
                        local_relocations[relocation.target].add(entry)
                    else:
                        global_relocations[relocation.target].add(entry)

        # resolve local relocations
        for block, entries in local_relocations.items():
            for next, offset, width in entries:
                low, high, target = offset, offset + width, local_symbols[block] - next
                bytecode[low:high] = serialize(target, width)

    # resolve global relocations
    for block, entries in global_relocations.items():
        for next, offset, width in entries:
            low, high, target = offset, offset + width, global_symbols[block] - next
            bytecode[low:high] = serialize(target, width)

    return bytes(bytecode)


class Encoder(Protocol):
    def __call__(
        self, instruction: BlockletInstruction, out: bytearray
    ) -> RelocationInfo | None: ...


DISPATCH_TABLE: dict[type[BlockletInstruction], Encoder] = {
    llvm.ADC: math.encode_adc,
    llvm.ADD: math.encode_add,
    llvm.AND: math.encode_and,
    llvm.BSWAP: bits.encode_bswap,
    llvm.CALL: ctrl.encode_call,
    llvm.CMP: math.encode_cmp,
    llvm.JMP: ctrl.encode_jmp,
    llvm.LEA: addr.encode_lea,
    llvm.LOOP: ctrl.encode_loop,
    llvm.LOOPE: ctrl.encode_loope,
    llvm.LOOPNE: ctrl.encode_loopne,
    llvm.MOV: move.encode_mov,
    llvm.NOP: ctrl.encode_nop,
    llvm.OR: math.encode_or,
    llvm.POP: stack.encode_pop,
    llvm.PUSH: stack.encode_push,
    llvm.RCL: shifts.encode_rcl,
    llvm.RCR: shifts.encode_rcr,
    llvm.RET: ctrl.encode_ret,
    llvm.ROL: shifts.encode_rol,
    llvm.ROR: shifts.encode_ror,
    llvm.SAL: shifts.encode_sal,
    llvm.SAR: shifts.encode_sar,
    llvm.SBB: math.encode_sbb,
    llvm.SHL: shifts.encode_shl,
    llvm.SHR: shifts.encode_shr,
    llvm.SUB: math.encode_sub,
    llvm.SYSCALL: ctrl.encode_syscall,
    llvm.XCHG: move.encode_xchg,
    llvm.XOR: math.encode_xor,
}  # pyright: ignore[reportAssignmentType]
