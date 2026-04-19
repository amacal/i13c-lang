from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.signatures import Signature, SignatureId
from i13c.syntax import tree


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

    for nid, entry in graph.snippet.signatures.items():
        # derive signature ID from globally unique node ID
        signature_id = SignatureId(value=nid.value)

        # find the context of the signature entry
        snippet = graph.snippet.signatures.get_ctx(nid)
        nid = graph.snippet.snippets.get_by_node(snippet)

        # reverse mapping to parameter ID
        def map_slot(slot: tree.snippet.Slot) -> ParameterId:
            nid = graph.snippet.slots.get_by_node(slot)
            return ParameterId(value=nid.value)

        signatures[signature_id] = Signature(
            ref=entry.ref,
            name=entry.name,
            parameters=[map_slot(slot) for slot in entry.slots],
        )

    for nid, entry in graph.function.signatures.items():
        # derive signature ID from globally unique node ID
        signature_id = SignatureId(value=nid.value)

        # find the context of the signature entry
        function = graph.function.signatures.get_ctx(nid)
        nid = graph.function.functions.get_by_node(function)

        # reverse mapping to slot ID
        def map_param(param: tree.function.Parameter) -> ParameterId:
            nid = graph.function.parameters.get_by_node(param)
            return ParameterId(value=nid.value)

        signatures[signature_id] = Signature(
            ref=entry.ref,
            name=entry.name,
            parameters=[map_param(param) for param in entry.params],
        )

    return OneToOne[SignatureId, Signature].instance(signatures)
