from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.analyses.calls import CallInstruction, CallLlvm
from i13c.semantic.typing.analyses.llvm import (
    Call,
    Exchange,
    Immediate,
    Move,
    Register,
    Slot,
)
from i13c.semantic.typing.analyses.shuffles import (
    ShuffleCallSite,
    ShuffleExchange,
    ShuffleImmediate,
    ShuffleLoad,
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
    # before any call we need to pass the arguments
    if shuffle := shuffles.find(entry.target.callsite):

        # first direct register moves
        for move in shuffle.moves:
            if isinstance(move, ShuffleMove):
                instructions.append(
                    Move(
                        variant=(
                            Register(name=move.dst),
                            Register(name=move.src),
                        )
                    )
                )

        # then register exchanges
        for move in shuffle.moves:
            if isinstance(move, ShuffleExchange):
                instructions.append(
                    Exchange(
                        dst=Register(name=move.dst),
                        src=Register(name=move.src),
                    )
                )

        # then register loads from memory
        for move in shuffle.moves:
            if isinstance(move, ShuffleLoad):
                instructions.append(
                    Move(
                        variant=(
                            Register(name=move.dst),
                            Slot(idx=move.src),
                        )
                    )
                )

        # finally direct immediate moves
        for move in shuffle.moves:
            if isinstance(move, ShuffleImmediate):
                instructions.append(
                    Move(
                        variant=(
                            Register(name=move.dst),
                            Immediate(value=move.src),
                        )
                    )
                )

    if asmlet := asmlets.find(entry.target.callsite):
        instructions.append(Call(target=asmlet.id))

    elif function := functions.find(entry.target.callsite):
        instructions.append(Call(target=function.id))


class ListExtractor:
    def __init__(self, data: OneToOne[CallId, CallLlvm]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[CallId, CallLlvm]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(key: CallId, entry: CallLlvm) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "instrs": str(len(entry.instructions)),
        }
