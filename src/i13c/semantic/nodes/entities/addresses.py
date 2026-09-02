from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.addresses import Address, AddressId, BaseRegister
from i13c.semantic.typing.entities.displacements import DisplacementId
from i13c.semantic.typing.entities.indices import IndexId
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

        # optionally available index or offset information
        base_id: BaseRegister | None = None
        indx_id: IndexId | None = None
        disp_id: DisplacementId | None = None

        # reverse mapping to base register ID
        if isinstance(entry.base, tree.snippet.Register):
            base_nid = graph.snippet.registers.get_by_node(entry.base)
            base_id = RegisterId(value=base_nid.value)

        if isinstance(entry.base, tree.snippet.Reference):
            base_nid = graph.snippet.references.get_by_node(entry.base)
            base_id = ReferenceId(value=base_nid.value)

        # reverse mapping to index register ID
        if entry.indx is not None:
            indx_nid = graph.snippet.indices.get_by_node(entry.indx)
            indx_id = IndexId(value=indx_nid.value)

        # reverse mapping to immediate ID
        if entry.disp is not None:
            offset_nid = graph.snippet.displacements.get_by_node(entry.disp)
            disp_id = DisplacementId(value=offset_nid.value)

        addresses[address_id] = Address(
            ref=entry.ref,
            size=entry.size,
            base=base_id,
            indx=indx_id,
            disp=disp_id,
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
            "size": "Size",
            "base": "Base",
            "indx": "Index",
            "disp": "Displacement",
        }

    @staticmethod
    def rows(key: AddressId, entry: Address) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "size": entry.size.decode() if entry.size else "",
            "base": entry.base.identify(1) if entry.base else "",
            "indx": entry.indx.identify(1) if entry.indx else "",
            "disp": entry.disp.identify(1) if entry.disp else "",
        }
