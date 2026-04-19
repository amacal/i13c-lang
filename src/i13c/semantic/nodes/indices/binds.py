from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.binds import BindId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.resolutions.binds import BindAcceptance


def configure_binds_by_parameters() -> GraphNode:
    return GraphNode(
        builder=build_binds_by_parameters,
        constraint=None,
        produces=("indices/binds/parameters",),
        requires=frozenset(
            {
                ("binds", "resolutions/binds/accepted"),
            }
        ),
    )


def build_binds_by_parameters(
    binds: OneToOne[BindId, BindAcceptance],
) -> OneToOne[ParameterId, BindAcceptance]:
    index: Dict[ParameterId, BindAcceptance] = {}

    for _, entry in binds.items():
        index[entry.ctx] = entry

    return OneToOne[ParameterId, BindAcceptance].instance(index)
