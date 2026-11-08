from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.analyses.calls import CallInstruction, CallLlvm
from i13c.semantic.typing.analyses.dflows import DataFlows
from i13c.semantic.typing.analyses.llvm import (
    CALL,
    CallArguments,
    CallClobbers,
    CallOperands,
    CallOutputs,
    Immediate,
    Register,
)
from i13c.semantic.typing.analyses.shuffles import (
    ShuffleCallSite,
    ShuffleImmediate,
    ShuffleMove,
)
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.calls import CallId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.calls import CallAcceptance


def configure_calls() -> GraphNode:
    return GraphNode(
        builder=build_calls,
        constraint=None,
        produces=("analyses/calls",),
        requires=frozenset(
            {
                ("calls", "resolutions/calls/accepted"),
                ("assigns", "resolutions/assigns/accepted"),
                ("asmlets", "indices/asmlets/callsites"),
                ("callings", "analyses/callings"),
                ("functions", "indices/functions/callsites"),
                ("shuffles", "indices/shuffles/callsites"),
                ("dflows", "analyses/dflows"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_calls(
    calls: OneToOne[CallId, CallAcceptance],
    assigns: OneToOne[AssignId, AssignAcceptance],
    asmlets: OneToOne[CallSiteId, Asmlet],
    callings: OneToOne[CallSiteId, Calling],
    functions: OneToOne[CallSiteId, Function],
    shuffles: OneToOne[CallSiteId, ShuffleCallSite],
    dflows: OneToOne[FunctionId, DataFlows],
) -> OneToOne[CallSiteId, CallLlvm]:
    llvm: dict[CallSiteId, CallLlvm] = {}

    for entry in calls.values():
        instructions: list[CallInstruction] = []

        # generate call instructions for the current call entry
        emit(instructions, shuffles, asmlets, functions, entry.target)

        llvm[entry.target.callsite] = CallLlvm(
            ref=entry.ref,
            target=entry,
            instructions=instructions,
        )

    for entry in assigns.values():
        instructions: list[CallInstruction] = []

        # generate call instructions for the current call entry
        # only when an assignment involves a callsite

        # expect exactly one node in the expression
        node = entry.expression.get_node()

        if isinstance(node, CallSiteId):
            calling = callings.get(node)

            # emit a call for a given calling, with passed
            # data flow which contains info about call outputs

            emit(
                instructions,
                shuffles,
                asmlets,
                functions,
                calling,
                dflow=dflows.get(entry.fn),
            )

            llvm[calling.callsite] = CallLlvm(
                ref=entry.ref,
                target=entry,
                instructions=instructions,
            )

    return OneToOne[CallSiteId, CallLlvm].instance(llvm)


def emit(
    instructions: list[CallInstruction],
    shuffles: OneToOne[CallSiteId, ShuffleCallSite],
    asmlets: OneToOne[CallSiteId, Asmlet],
    functions: OneToOne[CallSiteId, Function],
    calling: Calling,
    /,
    dflow: DataFlows | None = None,
):
    # blank dict for call arguments
    args: CallArguments = {}
    outs: CallOutputs = {}
    clobbers: CallClobbers | None = None
    operands: CallOperands | None = None

    # before any call we need to pass the arguments
    if shuffle := shuffles.find(calling.callsite):
        for move in shuffle.moves:
            if isinstance(move, ShuffleMove):
                args[move.dst] = Register(name=move.src)

            elif isinstance(move, ShuffleImmediate):
                args[move.dst] = Immediate(value=move.src)

    # handle asmlet callsite
    if asmlet := asmlets.find(calling.callsite):
        operands = (asmlet.id,)
        clobbers = [reg.name for reg in asmlet.clobbers]

        assert len(asmlet.outputs) == len(calling.outputs)

        if dflow is not None:
            for output in zip(calling.outputs, asmlet.outputs):
                idx = dflow.values.index(output[0].target)
                outs[output[1].dst] = Register(name=f"v{idx}".encode())

        # else:
        #     assert len(asmlet.outputs) == 0, asmlet.outputs

    # handle function callsite
    elif function := functions.find(calling.callsite):
        operands = (function.id,)
        clobbers = [reg.name for reg in calling.clobbers]

    # emit the call instruction if we have both operands and clobbers
    if clobbers is not None and operands is not None:
        instructions.append(
            CALL(
                operands=operands,
                clobbers=clobbers,
                args=args,
                outs=outs,
            )
        )


class ListExtractor:
    def __init__(self, data: OneToOne[CallSiteId, CallLlvm]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[CallSiteId, tuple[CallLlvm, CALL]]]:
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
            "outs": "Outputs",
        }

    @staticmethod
    def rows(key: CallSiteId, entry: tuple[CallLlvm, CALL]) -> dict[str, str]:
        return {
            "ref": str(entry[0].ref),
            "id": key.identify(1),
            "target": str(entry[1].operands[0]),
            "args": str({k.decode(): str(v) for k, v in entry[1].args.items()}),
            "outs": str({k.decode(): str(v) for k, v in entry[1].outs.items()}),
        }
