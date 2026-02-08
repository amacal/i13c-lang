from typing import Dict, Iterable, Tuple

from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId


class SnippetListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[SnippetId, Snippet]]:
        return graph.basic.snippets.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Snippet ID",
            "name": "Snippet Name",
            "slots": "Slots",
            "clbbrs": "Clobbers",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(entry: Tuple[SnippetId, Snippet]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "slots": str(len(entry[1].slots)),
            "clbbrs": str(len(entry[1].clobbers)),
            "instrs": str(len(entry[1].instructions)),
        }
