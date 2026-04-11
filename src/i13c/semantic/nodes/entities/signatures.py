from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.signatures import Signature, SignatureId
from i13c.semantic.typing.entities.slots import SlotId
from i13c.syntax.tree.snippet import Slot


def configure_signatures() -> GraphNode:
    return GraphNode(
        builder=build_signatures,
        constraint=None,
        produces=("entities/signatures",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_signatures(
    graph: SyntaxGraph,
) -> OneToOne[SignatureId, Signature]:
    signatures: Dict[SignatureId, Signature] = {}

    for nid, entry in graph.signatures.items():
        # derive signature ID from globally unique node ID
        signature_id = SignatureId(value=nid.value)

        # reverse mapping to slot ID
        def map_slot(slot: Slot) -> SlotId:
            nid = graph.slots.get_by_node(slot)
            return SlotId(value=nid.value)

        signatures[signature_id] = Signature(
            ref=entry.ref,
            name=entry.name,
            slots=[map_slot(slot) for slot in entry.slots],
        )

    return OneToOne[SignatureId, Signature].instance(signatures)
