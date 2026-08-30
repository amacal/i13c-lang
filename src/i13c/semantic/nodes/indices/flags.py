
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.resolutions.flags import FlagsAcceptance


def configure_flags_by_nid() -> GraphNode:
    return GraphNode(
        builder=build_flags_by_nid,
        constraint=None,
        produces=("indices/flags/nid",),
        requires=frozenset(
            {
                ("flags", "resolutions/flags/accepted"),
            }
        ),
    )


def build_flags_by_nid(
    flags: OneToOne[FlagsId, FlagsAcceptance],
) -> OneToOne[NodeId, FlagsAcceptance]:
    index: dict[NodeId, FlagsAcceptance] = {}

    for entry in flags.values():
        index[entry.nid] = entry

    return OneToOne[NodeId, FlagsAcceptance].instance(index)
