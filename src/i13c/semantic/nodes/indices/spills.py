from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.analyses.cflows import FlowNode
from i13c.semantic.typing.analyses.spills import Spill, SpillOp
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.statements import StatementId


def configure_spills_by_statements() -> GraphNode:
    return GraphNode(
        builder=build_spills_by_statements,
        constraint=None,
        produces=("indices/spills/statements",),
        requires=frozenset(
            {
                ("spills", "analyses/spills"),
            }
        ),
    )


def build_spills_by_statements(
    spills: OneToOne[FunctionId, Spill],
) -> OneToMany[StatementId, SpillOp]:
    index: dict[StatementId, list[SpillOp]] = {}

    for spill in spills.values():
        for idx, node in enumerate(spill.nodes):
            if isinstance(node, FlowNode):
                index[node.target] = spill.spills[idx]

    return OneToMany[StatementId, SpillOp].instance(index)
