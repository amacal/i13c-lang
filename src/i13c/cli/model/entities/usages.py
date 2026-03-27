from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.indices.usages import Usage, UsageId


class UsageListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[UsageId, Usage]]:
        return artifacts.semantic_graph().basic.usages.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Usage ID",
            "name": "Usage Name",
        }

    @staticmethod
    def rows(entry: Tuple[UsageId, Usage]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].ident),
        }
