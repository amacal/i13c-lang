from typing import Dict, Iterable, Tuple

from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId


class CallSiteListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[CallSiteId, CallSite]]:
        return graph.basic.callsites.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Callsite ID",
            "name": "Callee Name",
            "args": "Arguments",
        }

    @staticmethod
    def rows(entry: Tuple[CallSiteId, CallSite]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].callee),
            "args": str(len(entry[1].arguments)),
        }
