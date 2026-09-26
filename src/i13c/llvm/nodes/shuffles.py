from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.allocations import Allocation
from i13c.llvm.typing.cflows import ControlFlow
from i13c.llvm.typing.shuffles import (
    Coloring,
    InMemory,
    InRegister,
    Location,
    Shuffle,
    ShuffleInstruction,
    ShuffleSegment,
)
from i13c.semantic.typing.analyses import llvm
from i13c.semantic.typing.entities.functions import FunctionId


def configure_shuffles() -> GraphNode:
    return GraphNode(
        builder=build_shuffles,
        constraint=None,
        produces=("llvm/shuffles",),
        requires=frozenset(
            {
                ("cflows", "llvm/cflows"),
                ("allocations", "llvm/allocations"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_shuffles(
    cflows: OneToOne[FunctionId, ControlFlow],
    allocations: OneToOne[FunctionId, Allocation],
) -> OneToOne[FunctionId, Shuffle]:
    shuffles: dict[FunctionId, Shuffle] = {}

    for fid, allocation in allocations.items():
        cflow: ControlFlow = cflows.get(fid)
        shuffles[fid] = shuffle(cflow, allocation)

    return OneToOne[FunctionId, Shuffle].instance(shuffles)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Shuffle]) -> None:
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[tuple[FunctionId, int, str, int], ShuffleInstruction]]:
        for fid, shuffle in self.data.items():
            for idx, segment in enumerate(shuffle.segments):
                if segment is None:
                    continue

                for phase, instructions in (
                    ("before", segment.before),
                    ("after", segment.after),
                ):
                    for position, instruction in enumerate(instructions):
                        yield (fid, idx, phase, position), instruction

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "fn": "Function",
            "segment": "Segment",
            "phase": "Before/After",
            "position": "Position",
            "instruction": "Instruction",
        }

    @staticmethod
    def rows(
        key: tuple[FunctionId, int, str, int], entry: ShuffleInstruction
    ) -> dict[str, str]:
        return {
            "fn": key[0].identify(1),
            "segment": str(key[1]),
            "phase": key[2],
            "position": str(key[3]),
            "instruction": str(entry),
        }


def address(offset: int) -> llvm.Address:
    # short offsets can use 8-bit displacement
    width = 8 if offset < 128 else 32

    return llvm.Address(
        size=64,
        base=llvm.Register(name=b"rsp"),
        indx=None,
        disp=llvm.Displacement(
            width=width,
            direction="forward",
            offset=offset.to_bytes(width // 8, "little"),
        ),
    )


def handle_operands(
    scratch: InRegister,
    src: Location,
    dst: Location,
) -> list[tuple[llvm.Register | llvm.Address, llvm.Register | llvm.Address]]:

    # operands for the MOV instruction
    op1: llvm.Register | llvm.Address | None = None
    op2: llvm.Register | llvm.Address | None = None

    # loads are easy to handle without any collisions
    if isinstance(src, InMemory) and isinstance(dst, InRegister):
        op1 = llvm.Register(name=dst.name)
        op2 = address(8 * src.slot)

    # stores are easy to handle without any collisions
    elif isinstance(dst, InMemory) and isinstance(src, InRegister):
        op1 = address(8 * dst.slot)
        op2 = llvm.Register(name=src.name)

    # the same about registers
    elif isinstance(src, InRegister) and isinstance(dst, InRegister):
        op1 = llvm.Register(name=dst.name)
        op2 = llvm.Register(name=src.name)

    # mem-to-mem needs a temporary register
    elif isinstance(src, InMemory) and isinstance(dst, InMemory):

        # use the scratch register as a temporary for mem-to-mem moves
        tmp = llvm.Register(name=scratch.name)

        # tmp <-> src, dst <-> tmp
        return [
            (tmp, address(8 * src.slot)),
            (address(8 * dst.slot), tmp),
        ]

    assert op1 and op2
    return [(op1, op2)]


def handle_move(
    scratch: InRegister, src: Location, dst: Location
) -> list[ShuffleInstruction]:

    ops = handle_operands(scratch, src, dst)
    return [llvm.MOV(operands=(op1, op2)) for op1, op2 in ops]


def handle_exchange(
    scratch: InRegister, src: Location, dst: Location
) -> list[ShuffleInstruction]:

    # deterministic ordering
    if str(src) > str(dst):
        src, dst = dst, src

    ops = handle_operands(scratch, src, dst)

    # mem-to-mem needs load, exchange, writeback -- not two exchanges
    if len(ops) == 2:
        mov1 = llvm.MOV(operands=(ops[0][0], ops[0][1]))
        xchg = llvm.XCHG(operands=(ops[1][1], ops[1][0]))
        mov2 = llvm.MOV(operands=(ops[0][1], ops[0][0]))

        return [mov1, xchg, mov2]

    return [llvm.XCHG(operands=(op1, op2)) for op1, op2 in ops]


def transfer(
    scratch: InRegister,
    exit: Coloring,
    entry: Coloring,
) -> list[ShuffleInstruction]:

    actions: list[tuple[bytes, Location, Location]] = []
    instructions: list[ShuffleInstruction] = []

    for vreg, src in exit.items():
        if vreg in entry and src != entry[vreg]:
            actions.append((vreg, src, entry[vreg]))

    def order(item: tuple[bytes, Location, Location]) -> int:
        lregister = 0 if isinstance(item[1], InRegister) else 4
        rregister = 0 if isinstance(item[2], InRegister) else 8

        lr11 = 0 if isinstance(item[1], InRegister) and item[1].name == b"r11" else 1
        rr11 = 0 if isinstance(item[2], InRegister) and item[2].name == b"r11" else 2

        return lregister + rregister + lr11 + rr11

    actions.sort(key=order)

    while actions:
        changed = False

        # first pass: non-colliding moves and loads
        for idx, (vreg, src, dst) in enumerate(actions):
            # does dst collide with a remaining src?
            collides = any(dst == src for _, src, _ in actions)

            if src == dst:
                del actions[idx]
                changed = True

            elif not collides:
                del actions[idx]
                changed = True

                # extend the instructions with the move operations
                instructions.extend(handle_move(scratch, src, dst))

        if changed:
            continue

        # second pass: register or memory exchanges
        for idx, (vreg, src, dst) in enumerate(actions):
            collides = any(dst == src for _, src, _ in actions)

            if not collides:
                continue

            del actions[idx]
            changed = True

            # extend the instructions with the exchange operations
            instructions.extend(handle_exchange(scratch, src, dst))

            # the exchange already satisfies whoever wanted dst
            for idx, (v, s, d) in enumerate(actions):
                if s == dst:
                    actions[idx] = (v, src, d)

            break

    return instructions


class ControlFlowLikeSegment(Protocol):
    @property
    def backward(self) -> Sequence[int]: ...

    @property
    def forward(self) -> Sequence[int]: ...


class ControlFlowLike(Protocol):
    @property
    def gates(self) -> Sequence[int]: ...

    @property
    def segments(self) -> Sequence[ControlFlowLikeSegment]: ...


class AllocationLikeSegment(Protocol):
    @property
    def colors(self) -> dict[int, int]: ...

    @property
    def spills(self) -> dict[int, int]: ...


class AllocationLike(Protocol):
    @property
    def registers(self) -> Sequence[bytes]: ...

    @property
    def palette(self) -> Sequence[bytes]: ...

    @property
    def segments(self) -> Sequence[AllocationLikeSegment]: ...


def shuffle(cflow: ControlFlowLike, allocation: AllocationLike) -> Shuffle:
    registers = allocation.registers
    palette = allocation.palette

    segments: list[dict[bytes, Location]] = []
    shuffles: list[ShuffleSegment | None] = []
    slots: set[int] = set()

    for segment in allocation.segments:
        mapping: dict[bytes, Location] = {}

        for idx, color in segment.colors.items():
            mapping[registers[idx]] = InRegister(name=palette[color])

        for idx, slot in segment.spills.items():
            mapping[registers[idx]] = InMemory(slot=slot)
            slots.add(slot)

        segments.append(mapping)
        shuffles.append(None)

    for idx, segment in enumerate(cflow.segments):
        exit: dict[bytes, Location] = {}
        entry: dict[bytes, Location] = segments[idx]
        expected: dict[bytes, Location] | None = None

        # the exit is the output of the first predecessor
        if cflow.segments[idx].backward:
            exit = segments[cflow.segments[idx].backward[0]]

        if cflow.segments[idx].forward:
            succs = cflow.segments[idx].forward[0]
            preds = cflow.segments[succs].backward

            # if idx is not the first predecessor of its successor
            if preds[0] != idx:
                expected = segments[preds[0]]

        # pinned r11 as the scratch register
        scratch = InRegister(name=b"r11")

        # after block is present only if two different mappings need to be reconciled
        if expected is not None:
            after = transfer(scratch, entry, expected)
        else:
            after = []

        shuffles[idx] = ShuffleSegment(
            before=transfer(scratch, exit, entry),
            after=after,
        )

    return Shuffle(segments=shuffles, transfer=transfer)


def can_address_uses_an_8_bit_displacement_below_128():
    assert str(address(127)) == "qword [rsp + 0x7f]"


def can_address_uses_a_32_bit_displacement_from_128():
    assert str(address(128)) == "qword [rsp + 0x80000000]"


def can_transfer_without_vregs():
    entry: dict[bytes, Location] = {}
    exit: dict[bytes, Location] = {}

    # nothing is live across this boundary, so there's nothing to shuffle
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert shuffle == []


def can_transfer_same_vreg_in_reg():
    entry: dict[bytes, Location] = {b"v0": InRegister(name=b"rdi")}
    exit: dict[bytes, Location] = {b"v0": InRegister(name=b"rdi")}

    # same register on both sides, so nothing needs to move
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert shuffle == []


def can_transfer_same_vreg_in_mem():
    entry: dict[bytes, Location] = {b"v0": InMemory(slot=0)}
    exit: dict[bytes, Location] = {b"v0": InMemory(slot=0)}

    # same slot on both sides, so nothing needs to move
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert shuffle == []


def can_transfer_vreg_moves_from_reg_to_reg():
    entry: dict[bytes, Location] = {b"v0": InRegister(name=b"rdi")}
    exit: dict[bytes, Location] = {b"v0": InRegister(name=b"rsi")}

    # v0 lives in rsi at exit but must be in rdi at entry: a plain move
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert [str(i) for i in shuffle] == ["mov rdi, rsi"]


def can_transfer_vreg_moves_from_mem_to_reg():
    entry: dict[bytes, Location] = {b"v0": InRegister(name=b"rdi")}
    exit: dict[bytes, Location] = {b"v0": InMemory(slot=0)}

    # v0 is spilled at exit but must be live in rdi at entry: a load
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert [str(i) for i in shuffle] == ["mov rdi, qword [rsp + 0x00]"]


def can_transfer_vreg_moves_from_reg_to_mem():
    entry: dict[bytes, Location] = {b"v0": InMemory(slot=0)}
    exit: dict[bytes, Location] = {b"v0": InRegister(name=b"rdi")}

    # v0 is live in rdi at exit but must be spilled at entry: a store
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert [str(i) for i in shuffle] == ["mov qword [rsp + 0x00], rdi"]


def can_transfer_vreg_exchanges_two_vregs():
    entry: dict[bytes, Location] = {
        b"v0": InRegister(name=b"rdi"),
        b"v1": InRegister(name=b"rsi"),
    }
    exit: dict[bytes, Location] = {
        b"v0": InRegister(name=b"rsi"),
        b"v1": InRegister(name=b"rdi"),
    }

    # neither move is safe alone; resolved as an exchange
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert [str(i) for i in shuffle] == ["xchg rsi, rdi"]


def can_transfer_vreg_exchanges_four_vregs():
    entry: dict[bytes, Location] = {
        b"v0": InRegister(name=b"rdi"),
        b"v1": InRegister(name=b"rsi"),
        b"v2": InRegister(name=b"rdx"),
        b"v3": InRegister(name=b"rcx"),
    }
    exit: dict[bytes, Location] = {
        b"v0": InRegister(name=b"rsi"),
        b"v1": InRegister(name=b"rdi"),
        b"v2": InRegister(name=b"rcx"),
        b"v3": InRegister(name=b"rdx"),
    }

    # two independent swaps, each its own exchange
    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    assert [str(i) for i in shuffle] == ["xchg rsi, rdi", "xchg rdx, rcx"]


def can_transfer_move_blocked_only_by_a_pending_store_is_not_an_exchange():
    # v0's store and v1's move are unrelated, not a cycle
    exit: dict[bytes, Location] = {
        b"v0": InRegister(name=b"rdi"),
        b"v1": InRegister(name=b"rsi"),
    }

    entry: dict[bytes, Location] = {
        b"v0": InMemory(slot=0),
        b"v1": InRegister(name=b"rdi"),
    }

    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    # store must precede the move; no exchange needed
    assert [str(i) for i in shuffle] == [
        "mov qword [rsp + 0x00], rdi",
        "mov rdi, rsi",
    ]


def can_transfer_store_reading_a_register_must_precede_a_load_clobbering_it():
    entry: dict[bytes, Location] = {
        b"v0": InRegister(name=b"rdx"),
        b"v1": InMemory(slot=1),
    }
    exit: dict[bytes, Location] = {
        b"v0": InMemory(slot=2),
        b"v1": InRegister(name=b"rdx"),
    }

    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    # v1's store must read rdx before v0's load overwrites rdx with slot 2
    assert [str(i) for i in shuffle] == [
        "mov qword [rsp + 0x08], rdx",
        "mov rdx, qword [rsp + 0x10]",
    ]


def can_transfer_orders_a_chain_of_loads_and_stores_sharing_registers_and_slots():
    entry: dict[bytes, Location] = {
        b"v0": InMemory(slot=1),
        b"v1": InRegister(name=b"rdi"),
        b"v2": InMemory(slot=0),
    }
    exit: dict[bytes, Location] = {
        b"v0": InRegister(name=b"rsi"),
        b"v1": InMemory(slot=1),
        b"v2": InRegister(name=b"rdi"),
    }

    shuffle = transfer(InRegister(name=b"scratch"), exit, entry)

    # order matters: v2's store, then v1's load, then v0's store
    assert [str(i) for i in shuffle] == [
        "mov qword [rsp + 0x00], rdi",
        "mov rdi, qword [rsp + 0x08]",
        "mov qword [rsp + 0x08], rsi",
    ]


def can_transfer_mem_to_mem_uses_a_free_scratch_register_to_load_and_store():
    # a free register loads slot0, then stores into slot1
    exit: dict[bytes, Location] = {b"v0": InMemory(slot=0)}
    entry: dict[bytes, Location] = {b"v0": InMemory(slot=1)}

    result = transfer(InRegister(name=b"r10"), exit, entry)

    assert [str(i) for i in result] == [
        "mov r10, qword [rsp + 0x00]",
        "mov qword [rsp + 0x08], r10",
    ]


def can_transfer_mem_to_mem_with_r11_matches_real_shuffle_usage():
    # shuffle() always passes r11 specifically as scratch; confirm transfer()
    # resolves mem-to-mem the same way with the exact register real callers use
    exit: dict[bytes, Location] = {b"v0": InMemory(slot=0)}
    entry: dict[bytes, Location] = {b"v0": InMemory(slot=1)}

    result = transfer(InRegister(name=b"r11"), exit, entry)

    assert [str(i) for i in result] == [
        "mov r11, qword [rsp + 0x00]",
        "mov qword [rsp + 0x08], r11",
    ]


def can_transfer_register_memory_swap_resolves_as_a_single_exchange():
    # a single XCHG reg,mem swaps both halves; no scratch needed
    exit: dict[bytes, Location] = {
        b"v0": InRegister(name=b"r8"),
        b"v1": InMemory(slot=0),
    }
    entry: dict[bytes, Location] = {
        b"v0": InMemory(slot=0),
        b"v1": InRegister(name=b"r8"),
    }

    result = transfer(InRegister(name=b"r10"), exit, entry)

    assert [str(i) for i in result] == ["xchg r8, qword [rsp + 0x00]"]


def can_transfer_memory_memory_swap_must_not_corrupt_the_source_slot():
    # slot0 must be read (not exchanged) first, or it ends up with garbage
    exit: dict[bytes, Location] = {
        b"v0": InMemory(slot=0),
        b"v1": InMemory(slot=1),
    }

    entry: dict[bytes, Location] = {
        b"v0": InMemory(slot=1),
        b"v1": InMemory(slot=0),
    }

    result = transfer(InRegister(name=b"r10"), exit, entry)

    assert [str(i) for i in result] == [
        "mov r10, qword [rsp + 0x00]",
        "xchg r10, qword [rsp + 0x08]",
        "mov qword [rsp + 0x00], r10",
    ]


@dataclass(kw_only=True, repr=False)
class AllocationMock:
    registers: list[bytes]
    palette: list[bytes]
    segments: list[AllocationSegmentMock]


@dataclass(kw_only=True, repr=False)
class AllocationSegmentMock:
    colors: dict[int, int]
    spills: dict[int, int]


@dataclass(kw_only=True, repr=False)
class ControlFlowMock:
    gates: list[int]
    segments: list[ControlFlowMockSegment]


@dataclass(kw_only=True, repr=False)
class ControlFlowMockSegment:
    forward: list[int]
    backward: list[int]


def can_shuffle_across_a_linear_boundary_needing_a_store_move_and_exchange():
    cflow = ControlFlowMock(
        gates=[0, 1],
        segments=[
            ControlFlowMockSegment(
                forward=[1],
                backward=[],
            ),
            ControlFlowMockSegment(
                forward=[],
                backward=[0],
            ),
        ],
    )

    allocation = AllocationMock(
        registers=[b"v0", b"v1", b"v2", b"v3"],
        palette=[b"rdi", b"rsi", b"rdx", b"rcx"],
        segments=[
            AllocationSegmentMock(
                colors={
                    0: 0,
                    1: 1,
                    2: 2,
                    3: 3,
                },
                spills={},
            ),
            AllocationSegmentMock(
                colors={
                    1: 0,
                    2: 3,
                    3: 2,
                },
                spills={
                    0: 1,
                },
            ),
        ],
    )

    result = shuffle(cflow, allocation)

    assert len(result.segments) == 2
    assert result.segments[0] is not None
    assert result.segments[1] is not None

    # segment0 is the entry: no predecessor, so nothing to reconcile
    assert result.segments[0].before == []
    assert result.segments[0].after == []

    # v0 spilled, v1 moves in, v2/v3 swap via one exchange
    assert [str(i) for i in result.segments[1].before] == [
        "mov qword [rsp + 0x08], rdi",
        "mov rdi, rsi",
        "xchg rdx, rcx",
    ]
    assert result.segments[1].after == []


def can_shuffle_a_merge_point_where_two_predecessors_disagree_on_a_live_vreg():
    # diamond 0 -> {1,2} -> 3; v0 in rdi via segment1, rsi via segment2
    cflow = ControlFlowMock(
        gates=[0, 3],
        segments=[
            ControlFlowMockSegment(forward=[1, 2], backward=[]),
            ControlFlowMockSegment(forward=[3], backward=[0]),
            ControlFlowMockSegment(forward=[3], backward=[0]),
            ControlFlowMockSegment(forward=[], backward=[1, 2]),
        ],
    )

    allocation = AllocationMock(
        registers=[b"v0"],
        palette=[b"rdi", b"rsi"],
        segments=[
            AllocationSegmentMock(colors={0: 0}, spills={}),
            AllocationSegmentMock(colors={0: 0}, spills={}),
            AllocationSegmentMock(colors={0: 1}, spills={}),
            AllocationSegmentMock(colors={0: 0}, spills={}),
        ],
    )

    result = shuffle(cflow, allocation)

    assert len(result.segments) == 4
    assert result.segments[0] is not None
    assert result.segments[1] is not None
    assert result.segments[2] is not None
    assert result.segments[3] is not None

    # segment0 is the entry: no predecessor, so nothing to reconcile
    assert result.segments[0].before == []
    assert result.segments[0].after == []

    # segment1 is the primary predecessor of segment3: no-op
    assert result.segments[1].before == []
    assert result.segments[1].after == []

    # segment2 must undo its own rdi->rsi before the merge
    assert [str(i) for i in result.segments[2].before] == ["mov rsi, rdi"]
    assert [str(i) for i in result.segments[2].after] == ["mov rdi, rsi"]

    # segment3 receives rdi from its primary predecessor: no-op
    assert result.segments[3].before == []
    assert result.segments[3].after == []


def can_shuffle_a_merge_point_where_predecessors_spill_to_different_slots():
    # same diamond, v0 spilled to slot0 (primary) vs slot1 (secondary)
    cflow = ControlFlowMock(
        gates=[0, 3],
        segments=[
            ControlFlowMockSegment(forward=[1, 2], backward=[]),
            ControlFlowMockSegment(forward=[3], backward=[0]),
            ControlFlowMockSegment(forward=[3], backward=[0]),
            ControlFlowMockSegment(forward=[], backward=[1, 2]),
        ],
    )

    allocation = AllocationMock(
        registers=[b"v0"],
        palette=[b"rdi"],
        segments=[
            AllocationSegmentMock(colors={}, spills={0: 0}),
            AllocationSegmentMock(colors={}, spills={0: 0}),
            AllocationSegmentMock(colors={}, spills={0: 1}),
            AllocationSegmentMock(colors={}, spills={0: 0}),
        ],
    )

    result = shuffle(cflow, allocation)

    assert len(result.segments) == 4
    assert result.segments[0] is not None
    assert result.segments[1] is not None
    assert result.segments[2] is not None
    assert result.segments[3] is not None

    # segment0 is the entry: no predecessor, so nothing to reconcile
    assert result.segments[0].before == []
    assert result.segments[0].after == []

    # segment1 is the primary predecessor of segment3: no-op
    assert result.segments[1].before == []
    assert result.segments[1].after == []

    # segment2 loads slot0 into r11 and stores it to its own slot1;
    # shuffle() always uses r11 as scratch, regardless of the palette
    assert [str(i) for i in result.segments[2].before] == [
        "mov r11, qword [rsp + 0x00]",
        "mov qword [rsp + 0x08], r11",
    ]

    # segment2 must undo its own slot1 back into slot0 before the merge
    assert [str(i) for i in result.segments[2].after] == [
        "mov r11, qword [rsp + 0x08]",
        "mov qword [rsp + 0x00], r11",
    ]

    # segment3 receives slot0 from its primary predecessor: no-op
    assert result.segments[3].before == []
    assert result.segments[3].after == []


def can_shuffle_always_uses_r11_even_with_plenty_of_free_registers():
    # a large, entirely-unused palette must not change the scratch choice;
    # shuffle() always reaches for r11, never an opportunistically free one
    cflow = ControlFlowMock(
        gates=[0, 3],
        segments=[
            ControlFlowMockSegment(forward=[1, 2], backward=[]),
            ControlFlowMockSegment(forward=[3], backward=[0]),
            ControlFlowMockSegment(forward=[3], backward=[0]),
            ControlFlowMockSegment(forward=[], backward=[1, 2]),
        ],
    )

    allocation = AllocationMock(
        registers=[b"v0"],
        palette=[b"rdi", b"rsi", b"rdx", b"rcx", b"r8", b"r9", b"r10"],
        segments=[
            AllocationSegmentMock(colors={}, spills={0: 0}),
            AllocationSegmentMock(colors={}, spills={0: 0}),
            AllocationSegmentMock(colors={}, spills={0: 1}),
            AllocationSegmentMock(colors={}, spills={0: 0}),
        ],
    )

    result = shuffle(cflow, allocation)

    assert result.segments[2] is not None
    assert [str(i) for i in result.segments[2].before] == [
        "mov r11, qword [rsp + 0x00]",
        "mov qword [rsp + 0x08], r11",
    ]
