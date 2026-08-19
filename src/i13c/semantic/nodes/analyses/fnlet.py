from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cflows import ControlFlows, FlowNode
from i13c.semantic.typing.analyses.fnlet import Fnlet, FnletBlock, FnletInstruction
from i13c.semantic.typing.analyses.frames import StackFrame
from i13c.semantic.typing.analyses.llvm import (
    DecreaseStackPointer,
    IncreaseStackPointer,
    Move,
    PopFromStackPointer,
    PushToStackPointer,
    Register,
    Return,
    Slot,
)
from i13c.semantic.typing.analyses.statements import StatementLlvm
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.syntax.source import Span


def configure_fnlets() -> GraphNode:
    return GraphNode(
        builder=build_fnlets,
        constraint=None,
        produces=("analyses/fnlets",),
        requires=frozenset(
            {
                ("cflows", "analyses/cflows"),
                ("frames", "analyses/frames"),
                ("statements", "analyses/statements"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_fnlets(
    cflows: OneToOne[FunctionId, ControlFlows],
    frames: OneToOne[FunctionId, StackFrame],
    statements: OneToOne[StatementId, StatementLlvm],
) -> OneToOne[FunctionId, Fnlet]:
    fnlets: dict[FunctionId, Fnlet] = {}

    for fid, cflow in cflows.items():
        instructions: list[FnletInstruction] = []
        frame = frames.get(fid)
        cflow = cflows.get(fid)

        emit_prologue(instructions, frame)
        emit_body(instructions, statements, cflow)
        emit_epilogue(instructions, frame)

        fnlets[fid] = Fnlet(
            ref=cflow.ref,
            target=fid,
            blocks=[
                FnletBlock(instructions=instructions),
            ],
        )

    return OneToOne[FunctionId, Fnlet].instance(fnlets)


def emit_prologue(instructions: list[FnletInstruction], frame: StackFrame):
    for entry in frame.saved:
        instructions.append(PushToStackPointer(src=Register(name=entry.name)))

    if frame.slots > 0:
        instructions.append(DecreaseStackPointer(slots=frame.slots))

    for entry in frame.spill:
        instructions.append(
            Move(variant=(Slot(idx=entry.slot), Register(name=entry.name)))
        )

    for entry in frame.moved:
        instructions.append(
            Move(variant=(Register(name=entry.dst), Register(name=entry.src)))
        )


def emit_epilogue(instructions: list[FnletInstruction], frame: StackFrame):
    if frame.slots > 0:
        instructions.append(IncreaseStackPointer(slots=frame.slots))

    for entry in reversed(frame.saved):
        instructions.append(PopFromStackPointer(dst=Register(name=entry.name)))

    instructions.append(Return())


def emit_body(
    instructions: list[FnletInstruction],
    statements: OneToOne[StatementId, StatementLlvm],
    cflow: ControlFlows,
):
    worklist: list[int] = [cflow.entry]

    while worklist:
        idx = worklist.pop()
        node = cflow.nodes[idx]

        # schedule direct successors
        worklist.extend(cflow.forward.get(idx, []))

        if not isinstance(node, FlowNode):
            continue

        # copy already emitted instructions
        entry = statements.get(node.target)
        instructions.extend(entry.instructions)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Fnlet]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[tuple[FunctionId, Span], tuple[int, FnletBlock]]]:
        for fid, fnlet in self.data.items():
            for idx, block in enumerate(fnlet.blocks):
                yield (fid, fnlet.ref), (idx, block)

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "function": "Function",
            "idx": "Block Index",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(
        key: tuple[FunctionId, Span], entry: tuple[int, FnletBlock]
    ) -> dict[str, str]:
        return {
            "ref": str(key[1]),
            "function": key[0].identify(1),
            "idx": str(entry[0]),
            "instrs": str(len(entry[1].instructions)),
        }
