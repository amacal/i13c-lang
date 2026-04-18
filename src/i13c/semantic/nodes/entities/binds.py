from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.binds import Bind, BindId
from i13c.semantic.typing.entities.slots import SlotId


def configure_binds() -> GraphNode:
    return GraphNode(
        builder=build_binds,
        constraint=None,
        produces=("entities/binds",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_binds(
    graph: SyntaxGraph,
) -> OneToOne[BindId, Bind]:
    binds: Dict[BindId, Bind] = {}

    for nid, entry in graph.binds.items():
        # find the parent slot
        slot = graph.binds.get_ctx(nid)
        ctx = graph.slots.get_by_node(slot)
        slot_id = SlotId(value=ctx.value)

        # derive bind ID from globally unique node ID
        bind_id = BindId(value=nid.value)

        binds[bind_id] = Bind(
            ref=entry.ref,
            ctx=slot_id,
            src=slot.name,
            dst=entry.name,
        )

    return OneToOne[BindId, Bind].instance(binds)
