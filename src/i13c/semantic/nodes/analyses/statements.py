from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.assigns import AssignLlvm
from i13c.semantic.typing.analyses.calls import CallLlvm
from i13c.semantic.typing.analyses.llvm import MOV, Address, Register
from i13c.semantic.typing.analyses.spills import SpillOp
from i13c.semantic.typing.analyses.statements import StatementInstruction, StatementLlvm
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.calls import CallId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.calls import CallAcceptance
from i13c.semantic.typing.resolutions.statements import StatementAcceptance


def configure_statements() -> GraphNode:
    return GraphNode(
        builder=build_statements,
        constraint=None,
        produces=("analyses/statements",),
        requires=frozenset(
            {
                ("calls", "analyses/calls"),
                ("spills", "indices/spills/statements"),
                ("assigns", "analyses/assigns"),
                ("statements", "resolutions/statements/accepted"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_statements(
    calls: OneToOne[CallId, CallLlvm],
    spills: OneToMany[StatementId, SpillOp],
    assigns: OneToOne[AssignId, AssignLlvm],
    statements: OneToOne[StatementId, StatementAcceptance],
) -> OneToOne[StatementId, StatementLlvm]:
    llvm: dict[StatementId, StatementLlvm] = {}

    for eid, entry in statements.items():
        instructions: list[StatementInstruction] = []

        if isinstance(entry.target, CallAcceptance):
            instructions.extend(calls.get(entry.target.id).instructions)

        if isinstance(entry.target, AssignAcceptance):
            instructions.extend(assigns.get(entry.target.id).instructions)

        # some statements may cause spills
        for spill in spills.find(eid):
            instructions.append(
                MOV(
                    operands=(
                        Address(
                            base=Register(name=b"rsp"),
                            disp=Hex.smallest(spill.slot),
                        ),
                        Register(name=spill.src),
                    )
                )
            )

        llvm[eid] = StatementLlvm(
            ref=entry.ref,
            acceptance=entry,
            instructions=instructions,
        )

    return OneToOne[StatementId, StatementLlvm].instance(llvm)


class ListExtractor:
    def __init__(self, data: OneToOne[StatementId, StatementLlvm]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[StatementId, StatementLlvm]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(key: StatementId, entry: StatementLlvm) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "instrs": str(len(entry.instructions)),
        }
