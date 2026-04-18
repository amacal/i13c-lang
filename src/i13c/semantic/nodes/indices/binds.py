from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.binds import BindId
from i13c.semantic.typing.entities.slots import SlotId
from i13c.semantic.typing.resolutions.binds import BindAcceptance


def configure_binds_by_slots() -> GraphNode:
    return GraphNode(
        builder=build_binds_by_slots,
        constraint=None,
        produces=("indices/binds/slots",),
        requires=frozenset(
            {
                ("binds", "resolutions/binds/accepted"),
            }
        ),
    )


def build_binds_by_slots(
    binds: OneToOne[BindId, BindAcceptance],
) -> OneToOne[SlotId, BindAcceptance]:
    index: Dict[SlotId, BindAcceptance] = {}

    for _, entry in binds.items():
        index[entry.ctx] = entry

    return OneToOne[SlotId, BindAcceptance].instance(index)
