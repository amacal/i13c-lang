from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.nodes.analyses.dflows import DataFlows
from i13c.semantic.typing.analyses.assigns import AssignInstruction, AssignLlvm
from i13c.semantic.typing.analyses.llvm import MOV, Immediate, Register
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.expressions import ExpressionAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance


def configure_assigns() -> GraphNode:
    return GraphNode(
        builder=build_assigns,
        constraint=None,
        produces=("analyses/assigns",),
        requires=frozenset(
            {
                ("assigns", "resolutions/assigns/accepted"),
                ("dflows", "analyses/dflows"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_assigns(
    dflows: OneToOne[FunctionId, DataFlows],
    assigns: OneToOne[AssignId, AssignAcceptance],
) -> OneToOne[AssignId, AssignLlvm]:
    llvm: dict[AssignId, AssignLlvm] = {}

    for eid, entry in assigns.items():
        instructions: list[AssignInstruction] = []
        dflow = dflows.get(entry.fn)

        emit(instructions, dflow, entry)

        llvm[eid] = AssignLlvm(
            ref=entry.ref,
            target=entry,
            instructions=instructions,
        )

    return OneToOne[AssignId, AssignLlvm].instance(llvm)


def emit(
    instructions: list[AssignInstruction],
    dflow: DataFlows,
    entry: AssignAcceptance,
):
    # to emit assignment instruction, we need to determine
    # the source and destination operands for the assignment

    # lookup for destination
    idx = dflow.values.index(entry.destination)
    dst = Register(name=dflow.vregs[idx])

    # lookup for source, literal emits immediate
    if isinstance(entry.expression, LiteralAcceptance):
        src = Immediate(value=entry.expression.target)

    # expression emits dest <- vreg of the expression's value
    # the value of the expression is already stored in a vreg
    elif isinstance(entry.expression, ExpressionAcceptance):
        idx = dflow.values.index(entry.expression.target)
        src = Register(name=dflow.vregs[idx])

    # callsite emits dest <- vreg of the callsite's output
    # the callsite must be called first to have its output
    else:
        assert entry.expression.output is not None
        idx = dflow.values.index(entry.expression.output)
        src = Register(name=dflow.vregs[idx])

    # emit single instruction
    instructions.append(MOV(operands=(dst, src)))


class ListExtractor:
    def __init__(self, data: OneToOne[AssignId, AssignLlvm]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[AssignId, AssignLlvm]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(key: AssignId, entry: AssignLlvm) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "instrs": str(len(entry.instructions)),
        }
