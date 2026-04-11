from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.binds import BindId
from i13c.semantic.typing.entities.slots import Slot, SlotId
from i13c.semantic.typing.entities.types import TypeId


def configure_slots() -> GraphNode:
    return GraphNode(
        builder=build_slots,
        constraint=None,
        produces=("entities/slots",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_slots(
    graph: SyntaxGraph,
) -> OneToOne[SlotId, Slot]:
    slots: Dict[SlotId, Slot] = {}

    for nid, entry in graph.slots.items():
        # derive slot ID from globally unique node ID
        slot_id = SlotId(value=nid.value)

        # reverse mapping to bind ID
        nid = graph.binds.get_by_node(entry.bind)
        bind_id = BindId(value=nid.value)

        # reverse mapping to type ID
        nid = graph.types.get_by_node(entry.type)
        type_id = TypeId(value=nid.value)

        slots[slot_id] = Slot(
            ref=entry.ref,
            name=entry.name,
            bind=bind_id,
            type=type_id,
        )

    return OneToOne[SlotId, Slot].instance(slots)
