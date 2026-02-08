from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.callsites import CallSite, CallSiteId
from i13c.sem.typing.indices.instances import Instance


class InstanceListExtractor:
    @staticmethod
    def extract(
        graph: SemanticGraph,
    ) -> Iterable[Tuple[CallSiteId, CallSite, Instance]]:
        return (
            (cid, graph.basic.callsites.get(cid), instance)
            for cid, instance in graph.indices.instance_by_callsite.items()
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
