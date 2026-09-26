from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.llvm.nodes.cflows import ControlFlowVisitor
from i13c.llvm.nodes.dflows import CALL, MOV, PROLOG, DataFlowSolver
from i13c.llvm.typing.cflows import ControlFlow
from i13c.llvm.typing.dflows import DataFlow
from i13c.llvm.typing.liveness import Liveness, LivenessSegment
from i13c.semantic.typing.analyses import llvm
from i13c.semantic.typing.analyses.fnlets import Fnlet, FnletInstruction
from i13c.semantic.typing.entities.functions import FunctionId


def configure_liveness() -> GraphNode:
    return GraphNode(
        builder=build_liveness,
        constraint=None,
        produces=("llvm/liveness",),
        requires=frozenset(
            {
                ("fnlets", "analyses/fnlets"),
                ("cflows", "llvm/cflows"),
                ("dflows", "llvm/dflows"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_liveness(
    fnlets: OneToOne[FunctionId, Fnlet],
    cflows: OneToOne[FunctionId, ControlFlow],
    dflows: OneToOne[FunctionId, DataFlow],
) -> OneToOne[FunctionId, Liveness]:
    liveness: dict[FunctionId, Liveness] = {}
    visitor = LivenessVisitor()

    for fid, dflow in dflows.items():
        liveness[fid] = visitor.visit(
            fnlet=fnlets[fid],
            cflow=cflows[fid],
            dflow=dflow,
        )

    return OneToOne[FunctionId, Liveness].instance(liveness)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Liveness]) -> None:
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[tuple[FunctionId, int, int], tuple[Liveness, LivenessSegment]]]:
        for fid, liveness in self.data.items():
            for idx, segment in enumerate(liveness.segments):
                for iid in range(len(segment.live_in)):
                    yield ((fid, idx, iid), (liveness, segment))

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "fn": "Function",
            "seg": "Segment",
            "iid": "Instruction",
            "clobs": "Clobbers",
            "in": "Live In",
            "out": "Live Out",
        }

    @staticmethod
    def rows(
        key: tuple[FunctionId, int, int], entry: tuple[Liveness, LivenessSegment]
    ) -> dict[str, str]:
        def from_list(registers: list[bytes], data: Iterable[int]) -> str:
            return ", ".join(sorted([registers[i].decode() for i in data])).replace(
                "'", ""
            )

        return {
            "fn": key[0].identify(1),
            "seg": str(key[1]),
            "iid": str(key[2]),
            "clobs": str(from_list(entry[0].registers, entry[1].clobbers[key[2]])),
            "in": str(from_list(entry[0].registers, entry[1].live_in[key[2]])),
            "out": str(from_list(entry[0].registers, entry[1].live_out[key[2]])),
        }


class FnletLikeBlock(Protocol):
    @property
    def instructions(self) -> Sequence[FnletInstruction]: ...


class FnletLike(Protocol):
    @property
    def blocks(self) -> Sequence[FnletLikeBlock]: ...


class ControlFlowLikeSegment(Protocol):
    @property
    def forward(self) -> Sequence[int]: ...

    @property
    def backward(self) -> Sequence[int]: ...


class ControlFlowLike(Protocol):
    @property
    def gates(self) -> Sequence[int]: ...

    @property
    def segments(self) -> Sequence[ControlFlowLikeSegment]: ...


class DataFlowLikeSegment(Protocol):
    @property
    def defs(self) -> list[list[int]]: ...

    @property
    def uses(self) -> list[list[int]]: ...

    @property
    def clobbers(self) -> list[list[int]]: ...


class DataFlowLike(Protocol):
    @property
    def registers(self) -> list[bytes]: ...

    @property
    def segments(self) -> Sequence[DataFlowLikeSegment]: ...

    @property
    def seeds(self) -> list[tuple[int, int]]: ...  # it will be fully referenced


class LivenessVisitor:
    def visit(
        self,
        fnlet: FnletLike,
        cflow: ControlFlowLike,
        dflow: DataFlowLike,
    ) -> Liveness:
        worklist: list[tuple[int, int]] = []
        segments: list[LivenessSegment] = []

        # combine corresponding segments from fnlet, and dflow
        instructions = [len(block.instructions) for block in fnlet.blocks]

        # first, we need to execute the processing of each segment
        for idx, dsegment in enumerate(dflow.segments):
            # worklist must include all instructions of the current segment
            worklist.extend([(idx, i) for i in range(instructions[idx])])

            # each segment has empty live_in and live_out sets initially
            # and all defs and clobbers are taken from the data flow segment
            segments.append(
                LivenessSegment(
                    live_in=[set() for _ in range(instructions[idx])],
                    live_out=[set() for _ in range(instructions[idx])],
                    clobbers=dsegment.clobbers,
                )
            )

        # iterate until no changes occur
        while worklist:
            sid, iid = worklist.pop()

            # compute live_out for the current instruction using next instruction
            if iid < len(segments[sid].live_out) - 1:
                segments[sid].live_out[iid].update(segments[sid].live_in[iid + 1])

            # compute live_out as union of live_in of successors' first instruction
            else:
                for successor in cflow.segments[sid].forward:
                    if segments[successor].live_in:
                        segments[sid].live_out[iid].update(segments[successor].live_in[0])

            # compute live_in as union of uses and live_out minus all defs of the segment
            defined = segments[sid].live_out[iid] - set(dflow.segments[sid].defs[iid])
            recomputed = set(dflow.segments[sid].uses[iid]).union(defined)

            # if live_in has changed retry all predecessors
            if recomputed != segments[sid].live_in[iid]:
                segments[sid].live_in[iid] = recomputed

                # worklist must include all instructions of the given segment
                for idx in cflow.segments[sid].backward:
                    worklist.extend([(idx, i) for i in range(instructions[idx])])

        return Liveness(
            segments=segments,
            registers=dflow.registers,
            seeds=dflow.seeds,
        )


@dataclass(kw_only=True, repr=False)
class FnletBlockMock:
    instructions: list[FnletInstruction]


@dataclass(kw_only=True, repr=False)
class FnletMock:
    blocks: list[FnletBlockMock]


@dataclass(kw_only=True, repr=False)
class ControlFlowMockSegment:
    forward: list[int]
    backward: list[int]


@dataclass(kw_only=True, repr=False)
class ControlFlowMock:
    gates: list[int]
    segments: list[ControlFlowMockSegment]


@dataclass(kw_only=True, repr=False)
class DataFlowMockSegment:
    defs: list[list[int]]
    uses: list[list[int]]
    clobbers: list[list[int]]


@dataclass(kw_only=True, repr=False)
class DataFlowMock:
    registers: list[bytes]
    segments: list[DataFlowMockSegment]
    seeds: list[tuple[int, int]]


def can_visit_fnlet_with_no_body():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare cvisitor and fnlet
    fid = FunctionId(value=10)
    fnlet = FnletMock(blocks=[entry, exit])
    cvisitor = ControlFlowVisitor()

    # prepare solver
    solver = DataFlowSolver()
    solver.register(PROLOG())

    dflow = solver.solve(fid, fnlet)
    cflow = cvisitor.visit(fnlet)

    visitor = LivenessVisitor()
    liveness = visitor.visit(fnlet, cflow, dflow)

    assert liveness.registers == []
    assert len(liveness.segments) == 2

    # PROLOG has no binds and EPILOG touches nothing, so nothing is ever live
    assert liveness.seeds == []

    assert liveness.segments[0].live_in == [set()]
    assert liveness.segments[0].live_out == [set()]
    assert liveness.segments[0].clobbers == [[]]

    assert liveness.segments[1].live_in == [set()]
    assert liveness.segments[1].live_out == [set()]
    assert liveness.segments[1].clobbers == [[]]


def can_visit_fnlet_with_an_empty_successor_block():
    entry = FnletBlockMock(instructions=[llvm.PROLOG(operands=(), binds={}, preserves=[])])
    empty = FnletBlockMock(instructions=[])
    fnlet = FnletMock(blocks=[entry, empty])

    # a mock cflow/dflow, bypassing ControlFlowVisitor/DataFlowSolver: a
    # real empty block already fails to build a real control-flow graph,
    # so this exercises LivenessVisitor's own contract directly
    cflow = ControlFlowMock(
        gates=[],
        segments=[
            ControlFlowMockSegment(forward=[1], backward=[]),
            ControlFlowMockSegment(forward=[], backward=[0]),
        ],
    )
    dflow = DataFlowMock(
        registers=[],
        segments=[
            DataFlowMockSegment(defs=[[]], uses=[[]], clobbers=[[]]),
            DataFlowMockSegment(defs=[], uses=[], clobbers=[]),
        ],
        seeds=[],
    )

    visitor = LivenessVisitor()
    liveness = visitor.visit(fnlet, cflow, dflow)

    # segment1 has no instructions to contribute, so segment0's own
    # instruction just sees an empty live_out from its empty successor
    assert liveness.segments[0].live_in == [set()]
    assert liveness.segments[0].live_out == [set()]
    assert liveness.segments[1].live_in == []
    assert liveness.segments[1].live_out == []


def can_visit_fnlet_with_binds():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(
                operands=(),
                binds={
                    b"v0": llvm.Register(name=b"rdi"),
                    b"v1": llvm.Register(name=b"rsi"),
                },
                preserves=[],
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare cvisitor and fnlet
    fid = FunctionId(value=10)
    fnlet = FnletMock(blocks=[entry, exit])
    cvisitor = ControlFlowVisitor()

    # prepare solver
    solver = DataFlowSolver()
    solver.register(PROLOG())

    dflow = solver.solve(fid, fnlet)
    cflow = cvisitor.visit(fnlet)

    visitor = LivenessVisitor()
    liveness = visitor.visit(fnlet, cflow, dflow)

    assert liveness.registers == [b"rdi", b"v0", b"rsi", b"v1"]
    assert len(liveness.segments) == 2

    # v0 is bound from rdi, v1 from rsi
    assert liveness.seeds == [(0, 1), (2, 3)]

    # v0/v1 are bound but never used before EPILOG, so nothing is live
    assert liveness.segments[0].live_in == [set()]
    assert liveness.segments[0].live_out == [set()]
    assert liveness.segments[0].clobbers == [[]]

    assert liveness.segments[1].live_in == [set()]
    assert liveness.segments[1].live_out == [set()]
    assert liveness.segments[1].clobbers == [[]]


def can_visit_fnlet_with_a_parameterless_call():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[],
                args={},
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare cvisitor and fnlet
    fid = FunctionId(value=10)
    fnlet = FnletMock(blocks=[entry, body, exit])
    cvisitor = ControlFlowVisitor()

    # prepare solver
    solver = DataFlowSolver()
    solver.register(PROLOG())
    solver.register(CALL())

    dflow = solver.solve(fid, fnlet)
    cflow = cvisitor.visit(fnlet)

    visitor = LivenessVisitor()
    liveness = visitor.visit(fnlet, cflow, dflow)

    # the call has no clobbers or args, so nothing ever touches a
    # register: the list stays empty and nothing seeds the entry block
    assert liveness.registers == []
    assert len(liveness.segments) == 3

    assert liveness.seeds == []

    assert liveness.segments[0].live_in == [set()]
    assert liveness.segments[0].live_out == [set()]
    assert liveness.segments[0].clobbers == [[]]

    assert liveness.segments[1].live_in == [set()]
    assert liveness.segments[1].live_out == [set()]
    assert liveness.segments[1].clobbers == [[]]


def can_visit_fnlet_with_a_call_and_params():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(
                operands=(),
                binds={
                    b"v0": llvm.Register(name=b"rdi"),
                    b"v1": llvm.Register(name=b"rsi"),
                },
                preserves=[],
            ),
        ]
    )

    body = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"r11", b"rcx"],
                args={
                    b"rdi": llvm.Register(name=b"v1"),
                    b"rsi": llvm.Register(name=b"v0"),
                    b"rdx": llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare cvisitor and fnlet
    fid = FunctionId(value=10)
    fnlet = FnletMock(blocks=[entry, body, exit])
    cvisitor = ControlFlowVisitor()

    # prepare solver
    solver = DataFlowSolver()
    solver.register(PROLOG())
    solver.register(CALL())

    dflow = solver.solve(fid, fnlet)
    cflow = cvisitor.visit(fnlet)

    visitor = LivenessVisitor()
    liveness = visitor.visit(fnlet, cflow, dflow)

    assert liveness.registers == [b"rdi", b"v0", b"rsi", b"v1", b"rdx", b"r11", b"rcx"]
    assert len(liveness.segments) == 3

    # v0 is bound from rdi, v1 from rsi, same as with_binds
    assert liveness.seeds == [(0, 1), (2, 3)]

    # v0/v1 survive from the bind straight into the call
    assert liveness.segments[0].live_in == [set()]
    assert liveness.segments[0].live_out == [{1, 3}]
    assert liveness.segments[0].clobbers == [[]]

    # the call consumes both as arguments and clobbers r11/rcx; nothing
    # survives past it
    assert liveness.segments[1].live_in == [{1, 3}]
    assert liveness.segments[1].live_out == [set()]
    assert liveness.segments[1].clobbers == [[5, 6]]


def can_visit_fnlet_with_multiline_instructions():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body1 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v0"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v1"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"rsi"],
                args={
                    b"rdi": llvm.Register(name=b"v0"),
                    b"rsi": llvm.Register(name=b"v1"),
                },
            ),
        ]
    )

    body2 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v2"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"rdi"],
                args={
                    b"rdi": llvm.Register(name=b"v2"),
                    b"rsi": llvm.Register(name=b"v0"),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare cvisitor and fnlet
    fid = FunctionId(value=10)
    fnlet = FnletMock(blocks=[entry, body1, body2, exit])
    cvisitor = ControlFlowVisitor()

    # prepare solver
    solver = DataFlowSolver()
    solver.register(PROLOG())
    solver.register(CALL())
    solver.register(MOV())

    dflow = solver.solve(fid, fnlet)
    cflow = cvisitor.visit(fnlet)

    visitor = LivenessVisitor()
    liveness = visitor.visit(fnlet, cflow, dflow)

    assert liveness.registers == [b"v0", b"v1", b"rdi", b"rsi", b"v2"]
    assert len(liveness.segments) == 4

    # no binds, so nothing seeds the entry block
    assert liveness.seeds == []

    assert liveness.segments[0].live_in == [set()]
    assert liveness.segments[0].live_out == [set()]
    assert liveness.segments[0].clobbers == [[]]

    # v0 survives the call (needed again in body2), v1 dies here, and
    # rsi — its own destination — is what the call clobbers
    assert liveness.segments[1].live_in == [set(), {0}, {0, 1}]
    assert liveness.segments[1].live_out == [{0}, {0, 1}, {0}]
    assert liveness.segments[1].clobbers == [[], [], [3]]

    # v0 (still alive from body1) and the freshly-defined v2 both feed
    # this call; rdi is clobbered but nothing survives past this block
    assert liveness.segments[2].live_in == [{0}, {0, 4}]
    assert liveness.segments[2].live_out == [{0, 4}, set()]
    assert liveness.segments[2].clobbers == [[], [2]]

    assert liveness.segments[3].live_in == [set()]
    assert liveness.segments[3].live_out == [set()]
    assert liveness.segments[3].clobbers == [[]]
