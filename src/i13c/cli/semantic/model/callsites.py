from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.callsites import CallSite, CallSiteId


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
    def rows(key: CallSiteId, value: CallSite) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "name": str(value.callee),
            "args": str(len(value.arguments)),
        }
