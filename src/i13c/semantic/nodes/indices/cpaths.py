from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cpaths import ControlPaths
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId


def configure_control_paths_by_signatures() -> GraphNode:
    return GraphNode(
        builder=build_control_cpaths_by_signatures,
        constraint=None,
        produces=("indices/cpaths/signatures",),
        requires=frozenset({("cpaths", "analyses/cpaths")}),
    )


def build_control_cpaths_by_signatures(
    cpaths: OneToOne[FunctionId, ControlPaths],
) -> OneToOne[SignatureId, ControlPaths]:
    index: Dict[SignatureId, ControlPaths] = {}

    for _, entry in cpaths.items():
        index[entry.flows.signature] = entry

    return OneToOne[SignatureId, ControlPaths].instance(index)
