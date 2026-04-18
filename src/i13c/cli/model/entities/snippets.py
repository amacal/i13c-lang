from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId


class SnippetListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[SnippetId, Snippet]]:
        return artifacts.semantic_graph().entities.snippets.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Snippet ID",
            "sign": "Signature",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(entry: Tuple[SnippetId, Snippet]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "sign": entry[1].signature.identify(1),
            "instrs": str(len(entry[1].instructions)),
        }
