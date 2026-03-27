from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.bindings import CallSiteBinding, CallSiteBindings
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId


class BindingsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[CallSiteId, CallSite, CallSiteBindings, CallSiteBinding]]:
        graph = artifacts.semantic_graph()

        for cid, bindings in graph.basic.bindings.items():
            for binding in bindings.entries:
                yield (cid, graph.basic.callsites.get(cid), bindings, binding)

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Callsite ID",
            "name": "Callee Name",
            "target": "Callee Target",
            "dst": "Binding Destination",
            "src": "Binding Source",
        }

    @staticmethod
    def rows(
        entry: Tuple[CallSiteId, CallSite, CallSiteBindings, CallSiteBinding],
    ) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].callee),
            "target": entry[2].callable.target.identify(1),
            "dst": str(entry[3].dst),
            "src": entry[3].src.identify(1),
        }
