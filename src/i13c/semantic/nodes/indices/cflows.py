from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance


def configure_control_flows_by_signatures() -> GraphNode:
    return GraphNode(
        builder=build_control_flows_by_signatures,
        constraint=None,
        produces=("indices/cflows/signatures",),
        requires=frozenset(
            {
                ("cflows", "resolutions/cflows/accepted"),
            }
        ),
    )


def build_control_flows_by_signatures(
    cflows: OneToOne[FunctionId, ControlFlowAcceptance],
) -> OneToOne[SignatureId, ControlFlowAcceptance]:
    index: Dict[SignatureId, ControlFlowAcceptance] = {}

    for _, entry in cflows.items():
        index[entry.signature] = entry

    return OneToOne[SignatureId, ControlFlowAcceptance].instance(index)
