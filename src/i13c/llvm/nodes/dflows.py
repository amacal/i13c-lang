from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.dflows import DataFlow, DataFlowSegment
from i13c.semantic.typing.analyses import llvm
from i13c.semantic.typing.analyses.fnlets import Fnlet, FnletInstruction
from i13c.semantic.typing.entities.functions import FunctionId


def configure_data_flows() -> GraphNode:
    return GraphNode(
        builder=build_data_flows,
        constraint=None,
        produces=("llvm/dflows",),
        requires=frozenset(
            {
                ("fnlets", "analyses/fnlets"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_data_flows(
    fnlets: OneToOne[FunctionId, Fnlet],
) -> OneToOne[FunctionId, DataFlow]:
    dflows: dict[FunctionId, DataFlow] = {}

    # construct the data flow solver
    solver = DataFlowSolver()
    solver.register(CALL())
    solver.register(MOV())
    solver.register(PROLOG())

    # process each function's control flow
    for fid, entry in fnlets.items():
        dflows[fid] = solver.solve(fid, entry)

    return OneToOne[FunctionId, DataFlow].instance(dflows)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, DataFlow]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[tuple[FunctionId, int], tuple[DataFlow, DataFlowSegment]]]:
        return (
            ((fid, idx), (dflow, segment))
            for fid, dflow in self.data.items()
            for idx, segment in enumerate(dflow.segments)
        )

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "fn": "Function",
            "idx": "Index",
            "vregs": "Registers",
            "forward": "Forward",
            "backward": "Backward",
            "defs": "Definitions",
            "uses": "Usages",
            "clobbers": "Clobbers",
        }

    @staticmethod
    def rows(
        key: tuple[FunctionId, int],
        entry: tuple[DataFlow, DataFlowSegment],
    ) -> dict[str, str]:

        def from_dict(
            registers: list[bytes],
            data: dict[int, list[int]],
        ) -> str:
            result = {
                registers[k].decode(): [registers[i].decode() for i in v]
                for k, v in data.items()
            }

            return str(result).replace("'", "")

        def from_list(
            registers: list[bytes],
            data: list[list[int]],
        ) -> str:
            result = [[registers[i].decode() for i in sublist] for sublist in data]
            return str(result).replace("'", "")

        def reduce_registers(
            registers: list[bytes], segment: DataFlowSegment
        ) -> list[str]:
            seen: set[int] = set()

            for idx in segment.forward.values():
                seen.update(idx)

            for idx in segment.backward.values():
                seen.update(idx)

            for idx in segment.defs + segment.uses + segment.clobbers:
                seen.update(idx)

            return [registers[i].decode() for i in sorted(seen)]

        return {
            "fn": key[0].identify(1),
            "idx": str(key[1]),
            "vregs": ", ".join(reduce_registers(entry[0].registers, entry[1])),
            "forward": str(from_dict(entry[0].registers, entry[1].forward)),
            "backward": str(from_dict(entry[0].registers, entry[1].backward)),
            "defs": str(from_list(entry[0].registers, entry[1].defs)),
            "uses": str(from_list(entry[0].registers, entry[1].uses)),
            "clobbers": str(from_list(entry[0].registers, entry[1].clobbers)),
        }


class DataFlowHandler[T: FnletInstruction](Protocol):
    def target(self) -> type[FnletInstruction]: ...

    def handle(
        self,
        dflow: tuple[DataFlow, DataFlowSegment],
        instr: tuple[int, T],
    ): ...


class FnletLikeBlock(Protocol):
    @property
    def instructions(self) -> Sequence[FnletInstruction]: ...


class FnletLike(Protocol):
    @property
    def blocks(self) -> Sequence[FnletLikeBlock]: ...


class DataFlowSolver:
    def __init__(self, /):
        self._handlers: dict[type[FnletInstruction], Any] = {}

    def register[T: FnletInstruction](self, handler: DataFlowHandler[T]):
        self._handlers[handler.target()] = handler

    def solve(self, fid: FunctionId, fnlet: FnletLike) -> DataFlow:
        dflow = DataFlow(
            segments=[],
            registers=[],
            seeds=[],
        )

        for block in fnlet.blocks:
            # create a new data flow segment
            segment = dflow.add_segment()
            args = (dflow, segment)

            # handle all instructions
            for iid, instr in enumerate(block.instructions):
                # always append instruction
                segment.add_instruction()

                # but only handle it if a handler exists
                if type(instr) in self._handlers:
                    self._handlers[type(instr)].handle(args, (iid, instr))

        return dflow


class PROLOG:
    def target(self) -> type[FnletInstruction]:
        return llvm.PROLOG

    def handle(
        self,
        dflow: tuple[DataFlow, DataFlowSegment],
        instr: tuple[int, llvm.PROLOG],
    ):
        for dst, src in instr[1].binds.items():
            # add both registers
            src = dflow[0].add_register(src.name)
            dst = dflow[0].add_register(dst)

            # seed the virtual registers
            dflow[0].add_seed(src, dst)

            # mark only virtual registers
            dflow[1].add_def(instr[0], dst)


class MOV:
    def target(self) -> type[FnletInstruction]:
        return llvm.MOV

    def handle(
        self,
        dflow: tuple[DataFlow, DataFlowSegment],
        instr: tuple[int, llvm.MOV],
    ):
        dst, src = None, None

        if isinstance(instr[1].operands[0], llvm.Register):
            name = instr[1].operands[0].name
            dst = dflow[0].add_register(name)
            dflow[1].add_def(instr[0], dst)

        if isinstance(instr[1].operands[1], llvm.Register):
            name = instr[1].operands[1].name
            src = dflow[0].add_register(name)
            dflow[1].add_use(instr[0], src)

        if src is not None and dst is not None:
            dflow[1].add_edge(src, dst)


class CALL:
    def target(self) -> type[FnletInstruction]:
        return llvm.CALL

    def handle(
        self,
        dflow: tuple[DataFlow, DataFlowSegment],
        instr: tuple[int, llvm.CALL],
    ):
        for dst, src in instr[1].args.items():
            if isinstance(src, llvm.Register):
                src = dflow[0].add_register(src.name)
                dst = dflow[0].add_register(dst)

                dflow[1].add_def(instr[0], dst)
                dflow[1].add_use(instr[0], src)
                dflow[1].add_edge(src, dst)

            else:
                dst = dflow[0].add_register(dst)
                dflow[1].add_def(instr[0], dst)

        # all clobbers must be also exposed
        for clobber in instr[1].clobbers:
            idx = dflow[0].add_register(clobber)
            dflow[1].add_clobber(instr[0], idx)


@dataclass(kw_only=True, repr=False)
class FnletBlockMock:
    instructions: list[FnletInstruction]


@dataclass(kw_only=True, repr=False)
class FnletMock:
    blocks: list[FnletBlockMock]


def can_solve_fnlet_with_no_body():
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

    fid = FunctionId(value=10)
    fnlet = FnletMock(blocks=[entry, exit])

    # prepare solver
    solver = DataFlowSolver()
    solver.register(PROLOG())

    # trigger it
    dflow = solver.solve(fid, fnlet)

    assert len(dflow.segments) == 2
    assert dflow.registers == []

    # PROLOG has no binds and EPILOG touches nothing, so nothing is ever
    # defined, used or clobbered
    assert dflow.segments[0].forward == {}
    assert dflow.segments[0].backward == {}
    assert dflow.segments[0].defs == [[]]
    assert dflow.segments[0].uses == [[]]
    assert dflow.segments[0].clobbers == [[]]

    assert dflow.segments[1].forward == {}
    assert dflow.segments[1].backward == {}
    assert dflow.segments[1].defs == [[]]
    assert dflow.segments[1].uses == [[]]
    assert dflow.segments[1].clobbers == [[]]


def can_solve_fnlet_with_binds():
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

    fid = FunctionId(value=10)
    fnlet = FnletMock(blocks=[entry, exit])

    # prepare solver
    solver = DataFlowSolver()
    solver.register(PROLOG())

    # trigger it
    dflow = solver.solve(fid, fnlet)
    assert len(dflow.segments) == 2

    # v0 is bound from rdi, v1 from rsi
    assert dflow.registers == [b"rdi", b"v0", b"rsi", b"v1"]
    assert dflow.seeds == [(0, 1), (2, 3)]

    # a bind defines its virtual register but never uses or forwards
    # anything, so there's no def-use edge to record
    assert dflow.segments[0].forward == {}
    assert dflow.segments[0].backward == {}
    assert dflow.segments[0].defs == [[1, 3]]
    assert dflow.segments[0].uses == [[]]
    assert dflow.segments[0].clobbers == [[]]

    assert dflow.segments[1].forward == {}
    assert dflow.segments[1].backward == {}
    assert dflow.segments[1].defs == [[]]
    assert dflow.segments[1].uses == [[]]
    assert dflow.segments[1].clobbers == [[]]


def can_solve_fnlet_with_single_mov_instruction():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"rax"),
                    llvm.Register(name=b"rbx"),
                )
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    fid = FunctionId(value=11)
    fnlet = FnletMock(blocks=[entry, body, exit])

    solver = DataFlowSolver()
    solver.register(MOV())
    solver.register(PROLOG())

    # trigger it
    dflow = solver.solve(fid, fnlet)

    assert len(dflow.segments) == 3
    assert dflow.registers == [b"rax", b"rbx"]

    assert dflow.segments[0].forward == {}
    assert dflow.segments[0].backward == {}
    assert dflow.segments[0].defs == [[]]
    assert dflow.segments[0].uses == [[]]
    assert dflow.segments[0].clobbers == [[]]

    # rbx's value flows into rax, so the DFG edge goes src(rbx)->dst(rax)
    assert dflow.segments[1].forward == {1: [0]}
    assert dflow.segments[1].backward == {0: [1]}
    assert dflow.segments[1].defs == [[0]]
    assert dflow.segments[1].uses == [[1]]
    assert dflow.segments[1].clobbers == [[]]

    assert dflow.segments[2].forward == {}
    assert dflow.segments[2].backward == {}
    assert dflow.segments[2].defs == [[]]
    assert dflow.segments[2].uses == [[]]
    assert dflow.segments[2].clobbers == [[]]


def can_solve_fnlet_with_single_call():
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

    fid = FunctionId(value=11)
    fnlet = FnletMock(blocks=[entry, body, exit])

    solver = DataFlowSolver()
    solver.register(CALL())
    solver.register(PROLOG())

    # trigger it
    dflow = solver.solve(fid, fnlet)

    assert len(dflow.segments) == 3
    assert dflow.registers == []

    assert dflow.segments[0].forward == {}
    assert dflow.segments[0].backward == {}
    assert dflow.segments[0].defs == [[]]
    assert dflow.segments[0].uses == [[]]
    assert dflow.segments[0].clobbers == [[]]

    # no args and no clobbers, so the call never touches a register
    assert dflow.segments[1].forward == {}
    assert dflow.segments[1].backward == {}
    assert dflow.segments[1].defs == [[]]
    assert dflow.segments[1].uses == [[]]
    assert dflow.segments[1].clobbers == [[]]

    assert dflow.segments[2].forward == {}
    assert dflow.segments[2].backward == {}
    assert dflow.segments[2].defs == [[]]
    assert dflow.segments[2].uses == [[]]
    assert dflow.segments[2].clobbers == [[]]


def can_solve_fnlet_with_single_call_with_clobbers():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"r11", b"r8"],
                args={},
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    fid = FunctionId(value=11)
    fnlet = FnletMock(blocks=[entry, body, exit])

    solver = DataFlowSolver()
    solver.register(CALL())
    solver.register(PROLOG())

    # trigger it
    dflow = solver.solve(fid, fnlet)

    assert len(dflow.segments) == 3
    # clobbers still register the physical names, in declaration order
    assert dflow.registers == [b"r11", b"r8"]

    assert dflow.segments[0].forward == {}
    assert dflow.segments[0].backward == {}
    assert dflow.segments[0].defs == [[]]
    assert dflow.segments[0].uses == [[]]
    assert dflow.segments[0].clobbers == [[]]

    # no args, so nothing is defined/used — only clobbered
    assert dflow.segments[1].forward == {}
    assert dflow.segments[1].backward == {}
    assert dflow.segments[1].defs == [[]]
    assert dflow.segments[1].uses == [[]]
    assert dflow.segments[1].clobbers == [[0, 1]]

    assert dflow.segments[2].forward == {}
    assert dflow.segments[2].backward == {}
    assert dflow.segments[2].defs == [[]]
    assert dflow.segments[2].uses == [[]]
    assert dflow.segments[2].clobbers == [[]]


def can_solve_fnlet_with_single_call_with_arguments():
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
                args={
                    b"rdi": llvm.Register(name=b"v0"),
                    b"rsi": llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    fid = FunctionId(value=11)
    fnlet = FnletMock(blocks=[entry, body, exit])

    solver = DataFlowSolver()
    solver.register(CALL())
    solver.register(PROLOG())

    # trigger it
    dflow = solver.solve(fid, fnlet)

    assert len(dflow.segments) == 3
    assert dflow.registers == [b"v0", b"rdi", b"rsi"]

    assert dflow.segments[0].forward == {}
    assert dflow.segments[0].backward == {}
    assert dflow.segments[0].defs == [[]]
    assert dflow.segments[0].uses == [[]]
    assert dflow.segments[0].clobbers == [[]]

    # rdi gets v0's value (edge v0->rdi); rsi gets an immediate instead,
    # so it's still defined but has no source register to use or link
    assert dflow.segments[1].forward == {0: [1]}
    assert dflow.segments[1].backward == {1: [0]}
    assert dflow.segments[1].defs == [[1, 2]]
    assert dflow.segments[1].uses == [[0]]
    assert dflow.segments[1].clobbers == [[]]

    assert dflow.segments[2].forward == {}
    assert dflow.segments[2].backward == {}
    assert dflow.segments[2].defs == [[]]
    assert dflow.segments[2].uses == [[]]
    assert dflow.segments[2].clobbers == [[]]


def can_solve_fnlet_with_multiple_mov_followed_by_call():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body = FnletBlockMock(
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
                clobbers=[],
                args={
                    b"rdi": llvm.Register(name=b"v0"),
                    b"rsi": llvm.Register(name=b"v1"),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    fid = FunctionId(value=11)
    fnlet = FnletMock(blocks=[entry, body, exit])

    solver = DataFlowSolver()
    solver.register(PROLOG())
    solver.register(MOV())
    solver.register(CALL())

    # trigger it
    dflow = solver.solve(fid, fnlet)

    assert len(dflow.segments) == 3
    assert dflow.registers == [b"v0", b"v1", b"rdi", b"rsi"]

    assert dflow.segments[0].forward == {}
    assert dflow.segments[0].backward == {}
    assert dflow.segments[0].defs == [[]]
    assert dflow.segments[0].uses == [[]]
    assert dflow.segments[0].clobbers == [[]]

    # the two MOVs define v0/v1 from immediates (no uses, no edges); the
    # call then uses both as args, defining rdi/rsi and linking each
    # (v0->rdi, v1->rsi)
    assert dflow.segments[1].forward == {0: [2], 1: [3]}
    assert dflow.segments[1].backward == {2: [0], 3: [1]}
    assert dflow.segments[1].defs == [[0], [1], [2, 3]]
    assert dflow.segments[1].uses == [[], [], [0, 1]]
    assert dflow.segments[1].clobbers == [[], [], []]

    assert dflow.segments[2].forward == {}
    assert dflow.segments[2].backward == {}
    assert dflow.segments[2].defs == [[]]
    assert dflow.segments[2].uses == [[]]
    assert dflow.segments[2].clobbers == [[]]
