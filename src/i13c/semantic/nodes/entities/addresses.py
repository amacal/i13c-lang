from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.addresses import Address, AddressId, Offset
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.registers import RegisterId


def configure_addresses() -> GraphNode:
    return GraphNode(
        builder=build_addresses,
        constraint=None,
        produces=("entities/addresses",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_addresses(
    graph: SyntaxGraph,
) -> OneToOne[AddressId, Address]:
    addresses: Dict[AddressId, Address] = {}

    for nid, entry in graph.addresses.items():
        # derive address ID from globally unique node ID
        address_id = AddressId(value=nid.value)

        # reverse mapping to base register ID
        base = graph.registers.get_by_node(entry.base)
        base_id = RegisterId(value=base.value)

        # reverse mapping to immediate ID
        if entry.offset is not None:
            offset = graph.immediates.get_by_node(entry.offset.value)
            offset_id = ImmediateId(value=offset.value)

            offset = Offset(
                kind=entry.offset.kind,
                value=offset_id,
            )

        else:
            offset = None

        addresses[address_id] = Address(
            ref=entry.ref,
            base=base_id,
            offset=offset,
        )

    return OneToOne[AddressId, Address].instance(addresses)
