from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.cflows import ControlFlow, ControlFlowSegment
from i13c.semantic.typing.analyses import llvm
from i13c.semantic.typing.analyses.fnlets import Fnlet, FnletInstruction
from i13c.semantic.typing.entities.functions import FunctionId


def configure_control_flows() -> GraphNode:
    return GraphNode(
        builder=build_control_flows,
        constraint=None,
        produces=("llvm/cflows",),
        requires=frozenset(
            {
                ("fnlets", "analyses/fnlets"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_control_flows(
    fnlets: OneToOne[FunctionId, Fnlet],
) -> OneToOne[FunctionId, ControlFlow]:
    cflows: dict[FunctionId, ControlFlow] = {}
    visitor = ControlFlowVisitor()

    for fid, entry in fnlets.items():
        cflows[fid] = visitor.visit(entry)

    return OneToOne[FunctionId, ControlFlow].instance(cflows)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, ControlFlow]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[
        tuple[tuple[FunctionId, int], tuple[ControlFlow, ControlFlowSegment]]
    ]:
        for fid, cflow in self.data.items():
            for idx, segment in enumerate(cflow.segments):
                yield (fid, idx), (cflow, segment)

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "fn": "Function",
            "idx": "Block",
            "gate": "Role",
            "forward": "Forward",
            "backward": "Backward",
        }

    @staticmethod
    def rows(
        key: tuple[FunctionId, int], entry: tuple[ControlFlow, ControlFlowSegment]
    ) -> dict[str, str]:
        def into_gate(gate: int, gates: list[int]) -> str:
            if gate == gates[0]:
                return "entry"

            if gate in gates[1:]:
                return "exit"

            return ""

        return {
            "fn": key[0].identify(1),
            "idx": str(key[1]),
            "gate": into_gate(key[1], entry[0].gates),
            "forward": ", ".join(map(str, entry[1].forward)),
            "backward": ", ".join(map(str, entry[1].backward)),
        }


class FnletLikeBlock(Protocol):
    @property
    def instructions(self) -> Sequence[FnletInstruction]: ...


class FnletLike(Protocol):
    @property
    def blocks(self) -> Sequence[FnletLikeBlock]: ...


class ControlFlowVisitor:
    def visit(self, fnlet: FnletLike) -> ControlFlow:
        visited: set[int] = set()
        worklist: list[int] = [0]

        # initial control flow graph containing all blocks
        cflow = ControlFlow.create(len(fnlet.blocks))

        while worklist:
            idx = worklist.pop()
            if idx in visited:
                continue

            visited.add(idx)

            # get the last instruction of the current block
            instr: FnletInstruction | None = (
                fnlet.blocks[idx].instructions[-1]
                if fnlet.blocks[idx].instructions
                else None
            )

            # declare as fall-through to the next block if there is no instruction
            if instr is None and idx + 1 < len(fnlet.blocks):
                    worklist.append(idx + 1)
                    cflow.add_edge(idx, idx + 1)

            # inspect JMP instructions
            if instr and isinstance(instr, llvm.JMP):
                assert len(instr.operands) == 1
                assert isinstance(instr.operands[0], llvm.Relocation)

                # extend worklist and forward edges
                worklist.append(instr.operands[0].block)
                cflow.add_edge(idx, instr.operands[0].block)

            # inspect fall-through to the next block
            if instr and not isinstance(instr, (llvm.JMP, llvm.EPILOG)):
                if idx + 1 < len(fnlet.blocks):
                    worklist.append(idx + 1)
                    cflow.add_edge(idx, idx + 1)

            # the EPILOG indicates the exit block
            if instr and isinstance(instr, llvm.EPILOG):
                cflow.set_exit(idx)

        return cflow


@dataclass(kw_only=True, repr=False)
class FnletBlockMock:
    instructions: list[FnletInstruction]


@dataclass(kw_only=True, repr=False)
class FnletMock:
    blocks: list[FnletBlockMock]


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

    fnlet = FnletMock(blocks=[entry, exit])
    visitor = ControlFlowVisitor()
    cflow = visitor.visit(fnlet)

    # PROLOG falls through into EPILOG, so entry is the sole gate in and
    # exit is the sole gate out
    assert cflow.gates == [0, 1]
    assert len(cflow.segments) == 2

    assert cflow.segments[0].forward == [1]
    assert cflow.segments[0].backward == []

    assert cflow.segments[1].forward == []
    assert cflow.segments[1].backward == [0]


def can_visit_fnlet_with_single_mov_instruction():
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

    fnlet = FnletMock(blocks=[entry, body, exit])
    visitor = ControlFlowVisitor()
    cflow = visitor.visit(fnlet)

    # MOV isn't a JMP or EPILOG, so it just falls through to the next block
    assert cflow.gates == [0, 2]
    assert len(cflow.segments) == 3

    assert cflow.segments[0].forward == [1]
    assert cflow.segments[0].backward == []

    assert cflow.segments[1].forward == [2]
    assert cflow.segments[1].backward == [0]

    assert cflow.segments[2].forward == []
    assert cflow.segments[2].backward == [1]


def can_visit_fnlet_with_single_jmp_relocation():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body = FnletBlockMock(
        instructions=[
            llvm.JMP(operands=(llvm.Relocation(block=0),)),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    fnlet = FnletMock(blocks=[entry, body, exit])
    visitor = ControlFlowVisitor()
    cflow = visitor.visit(fnlet)

    # entry falls through to body, whose JMP loops back to entry — a
    # cycle, so the worklist never reaches exit and no exit gate is set
    assert cflow.gates == [0]
    assert len(cflow.segments) == 3

    assert cflow.segments[0].forward == [1]
    assert cflow.segments[0].backward == [1]

    assert cflow.segments[1].forward == [0]
    assert cflow.segments[1].backward == [0]

    # unreachable: nothing ever jumps or falls through into it
    assert cflow.segments[2].forward == []
    assert cflow.segments[2].backward == []


def can_visit_fnlet_with_ret_followed_by_block():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"rax"),
                    llvm.Register(name=b"rbx"),
                )
            ),
        ]
    )

    fnlet = FnletMock(blocks=[entry, body, exit])
    visitor = ControlFlowVisitor()
    cflow = visitor.visit(fnlet)

    # body's EPILOG ends the only reachable path, so exit is never reached
    # and stays dead — same as the trailing block after an infinite loop
    assert cflow.gates == [0, 1]
    assert len(cflow.segments) == 3

    assert cflow.segments[0].forward == [1]
    assert cflow.segments[0].backward == []

    assert cflow.segments[1].forward == []
    assert cflow.segments[1].backward == [0]

    assert cflow.segments[2].forward == []
    assert cflow.segments[2].backward == []


def can_visit_fnlet_with_no_terminator_on_the_last_block():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    last = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"rax"),
                    llvm.Register(name=b"rbx"),
                )
            ),
        ]
    )

    fnlet = FnletMock(blocks=[entry, last])
    visitor = ControlFlowVisitor()
    cflow = visitor.visit(fnlet)

    # the last block's MOV isn't a JMP or EPILOG, so it would normally fall
    # through to the next block — but there is no next block, so it has
    # no successor at all rather than pointing past the end
    assert cflow.gates == [0]
    assert cflow.segments[0].forward == [1]
    assert cflow.segments[0].backward == []

    assert cflow.segments[1].forward == []
    assert cflow.segments[1].backward == [0]


def can_visit_fnlet_with_an_empty_successor_block():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )
    body = FnletBlockMock(
        instructions=[],
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    fnlet = FnletMock(blocks=[entry, body, exit])
    visitor = ControlFlowVisitor()
    cflow = visitor.visit(fnlet)

    # an empty block has no terminator to inspect, so it should just fall
    # through to the next one, same as any other non-JMP/EPILOG block
    assert cflow.gates == [0, 2]
    assert len(cflow.segments) == 3

    assert cflow.segments[0].forward == [1]
    assert cflow.segments[0].backward == []

    assert cflow.segments[1].forward == [2]
    assert cflow.segments[1].backward == [0]

    assert cflow.segments[2].forward == []
    assert cflow.segments[2].backward == [1]
