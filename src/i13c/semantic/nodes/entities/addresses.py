from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.addresses import Address, AddressId, Offset
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax import tree


def configure_addresses() -> GraphNode:
    return GraphNode(
        builder=build_addresses,
        constraint=None,
        produces=("entities/addresses",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_addresses(
    graph: SyntaxGraph,
) -> OneToOne[AddressId, Address]:
    addresses: dict[AddressId, Address] = {}

    for nid, entry in graph.snippet.addresses.items():
        # derive address ID from globally unique node ID
        address_id = AddressId(value=nid.value)

        # reverse mapping to base register ID
        if isinstance(entry.base, tree.snippet.Register):
            base = graph.snippet.registers.get_by_node(entry.base)
            base_id = RegisterId(value=base.value)
        else:
            base = graph.snippet.references.get_by_node(entry.base)
            base_id = ReferenceId(value=base.value)

        # reverse mapping to immediate ID
        if entry.offset is not None:
            offset = graph.snippet.immediates.get_by_node(entry.offset.value)
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


class ListExtractor:
    def __init__(self, data: OneToOne[AddressId, Address]):
        self.data = data

    def extract(self) -> Iterable[tuple[AddressId, Address]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "base": "Base",
            "okind": "Offset Kind",
            "ovalue": "Offset Value",
        }

    @staticmethod
    def rows(key: AddressId, entry: Address) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "base": entry.base.identify(1),
            "okind": str(entry.offset.kind) if entry.offset else "",
            "ovalue": entry.offset.value.identify(1) if entry.offset else "",
        }
