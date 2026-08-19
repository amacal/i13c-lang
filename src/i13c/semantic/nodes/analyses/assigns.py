from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.allocations import Allocation
from i13c.semantic.typing.analyses.assigns import AssignInstruction, AssignLlvm
from i13c.semantic.typing.analyses.llvm import Immediate, Move, Register, Slot
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance


def configure_assigns() -> GraphNode:
    return GraphNode(
        builder=build_assigns,
        constraint=None,
        produces=("analyses/assigns",),
        requires=frozenset(
            {
                ("assigns", "resolutions/assigns/accepted"),
                ("allocations", "analyses/allocations"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_assigns(
    assigns: OneToOne[AssignId, AssignAcceptance],
    allocations: OneToOne[FunctionId, Allocation],
) -> OneToOne[AssignId, AssignLlvm]:
    llvm: dict[AssignId, AssignLlvm] = {}

    for eid, entry in assigns.items():
        instructions: list[AssignInstruction] = []
        allocation = allocations.get(entry.fn)

        emit(instructions, allocation, entry)

        llvm[eid] = AssignLlvm(
            ref=entry.ref,
            target=entry,
            instructions=instructions,
        )

    return OneToOne[AssignId, AssignLlvm].instance(llvm)


def emit(
    instructions: list[AssignInstruction],
    allocation: Allocation,
    entry: AssignAcceptance,
):
    # fmt: off
    system_v: dict[int, bytes] = {
        0: b"rdi", 1: b"rsi", 2: b"rdx", 3: b"rcx", 4: b"r8", 5: b"r9", 6: b"r10", 7: b"r11",
        8: b"rax", 9: b"rbx", 10: b"rbp", 11: b"r12", 12: b"r13", 13: b"r14", 14: b"r15",
    }
    # fmt: on

    # lookup for destination
    idx = allocation.values.index(entry.destination)

    if idx in allocation.colors:
        dst = Register(name=system_v[allocation.colors[idx]])
    else:
        dst = Register(name=system_v[allocation.scratch])

    # lookup for source
    if isinstance(entry.expression, LiteralAcceptance):
        src = Immediate(value=entry.expression.target)
    else:
        idx = allocation.values.index(entry.expression.target)

        if idx in allocation.colors:
            src = Register(name=system_v[allocation.colors[idx]])
        else:
            src = Slot(idx=allocation.spills[idx])

    # emit single instruction
    instructions.append(Move(variant=(dst, src)))


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
