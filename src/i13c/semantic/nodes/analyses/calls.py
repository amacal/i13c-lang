from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.analyses.calls import CallInstruction, CallLlvm
from i13c.semantic.typing.analyses.llvm import (
    CALL,
    CallArguments,
    CallClobbers,
    CallOperands,
    Immediate,
    Register,
)
from i13c.semantic.typing.analyses.shuffles import (
    ShuffleCallSite,
    ShuffleImmediate,
    ShuffleMove,
)
from i13c.semantic.typing.entities.calls import CallId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import Function
from i13c.semantic.typing.resolutions.calls import CallAcceptance


def configure_calls() -> GraphNode:
    return GraphNode(
        builder=build_calls,
        constraint=None,
        produces=("analyses/calls",),
        requires=frozenset(
            {
                ("calls", "resolutions/calls/accepted"),
                ("asmlets", "indices/asmlets/callsites"),
                ("functions", "indices/functions/callsites"),
                ("shuffles", "indices/shuffles/callsites"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_calls(
    calls: OneToOne[CallId, CallAcceptance],
    asmlets: OneToOne[CallSiteId, Asmlet],
    functions: OneToOne[CallSiteId, Function],
    shuffles: OneToOne[CallSiteId, ShuffleCallSite],
) -> OneToOne[CallId, CallLlvm]:
    llvm: dict[CallId, CallLlvm] = {}

    for eid, entry in calls.items():
        instructions: list[CallInstruction] = []

        emit(instructions, shuffles, asmlets, functions, entry)

        llvm[eid] = CallLlvm(
            ref=entry.ref,
            target=entry,
            instructions=instructions,
        )

    return OneToOne[CallId, CallLlvm].instance(llvm)


def emit(
    instructions: list[CallInstruction],
    shuffles: OneToOne[CallSiteId, ShuffleCallSite],
    asmlets: OneToOne[CallSiteId, Asmlet],
    functions: OneToOne[CallSiteId, Function],
    entry: CallAcceptance,
):
    # blank dict for call arguments
    args: CallArguments = {}
    clobbers: CallClobbers | None = None
    operands: CallOperands | None = None

    # before any call we need to pass the arguments
    if shuffle := shuffles.find(entry.target.callsite):
        for move in shuffle.moves:
            if isinstance(move, ShuffleMove):
                args[move.dst] = Register(name=move.src)

            elif isinstance(move, ShuffleImmediate):
                args[move.dst] = Immediate(value=move.src)

    # handle asmlet callsite
    if asmlet := asmlets.find(entry.target.callsite):
        operands = (asmlet.id,)
        clobbers = [reg.name for reg in asmlet.clobbers]

    # handle function callsite
    elif function := functions.find(entry.target.callsite):
        operands = (function.id,)
        clobbers = [reg.name for reg in entry.target.clobbers]

    # emit the call instruction if we have both operands and clobbers
    if clobbers is not None and operands is not None:
        instructions.append(CALL(operands=operands, args=args, clobbers=clobbers))


class ListExtractor:
    def __init__(self, data: OneToOne[CallId, CallLlvm]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[CallId, tuple[CallLlvm, CALL]]]:
        for key, entry in self.data.items():
            for instruction in entry.instructions:
                yield key, (entry, instruction)

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "target": "Target",
            "args": "Arguments",
        }

    @staticmethod
    def rows(key: CallId, entry: tuple[CallLlvm, CALL]) -> dict[str, str]:
        return {
            "ref": str(entry[0].ref),
            "id": key.identify(1),
            "target": str(entry[1].operands[0]),
            "args": str({k.decode(): str(v) for k, v in entry[1].args.items()}),
        }
