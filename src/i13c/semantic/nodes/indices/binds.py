from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.identifiers.binds import BindId
from i13c.semantic.typing.identifiers.parameters import ParameterId
from i13c.semantic.typing.identifiers.results import ResultId
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
    index: dict[ParameterId, BindAcceptance] = {}

    for entry in binds.values():
        if isinstance(entry.ctx, ParameterId):
            index[entry.ctx] = entry

    return OneToOne[ParameterId, BindAcceptance].instance(index)


def configure_binds_by_results() -> GraphNode:
    return GraphNode(
        builder=build_binds_by_results,
        constraint=None,
        produces=("indices/binds/results",),
        requires=frozenset(
            {
                ("binds", "resolutions/binds/accepted"),
            }
        ),
    )


def build_binds_by_results(
    binds: OneToOne[BindId, BindAcceptance],
) -> OneToOne[ResultId, BindAcceptance]:
    index: dict[ResultId, BindAcceptance] = {}

    for entry in binds.values():
        if isinstance(entry.ctx, ResultId):
            index[entry.ctx] = entry

    return OneToOne[ResultId, BindAcceptance].instance(index)
