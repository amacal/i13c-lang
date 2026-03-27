from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.indices.instances import Instance


class InstanceListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[CallSiteId, CallSite, Instance]]:
        return (
            (cid, artifacts.semantic_graph().basic.callsites.get(cid), instance)
            for cid, instance in artifacts.semantic_graph().indices.instance_by_callsite.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Callsite ID",
            "name": "Callee Name",
            "target": "Target",
            "bindings": "Bindings",
            "operands": "Operands",
        }

    @staticmethod
    def rows(entry: Tuple[CallSiteId, CallSite, Instance]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].callee),
            "target": entry[2].target.identify(1),
            "bindings": str(len(entry[2].bindings)),
            "operands": str(len(entry[2].operands)),
        }
