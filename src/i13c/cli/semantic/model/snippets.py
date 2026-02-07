from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.snippets import Snippet, SnippetId


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
    def rows(key: SnippetId, value: Snippet) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "name": str(value.identifier),
            "slots": str(len(value.slots)),
            "clbbrs": str(len(value.clobbers)),
            "instrs": str(len(value.instructions)),
        }
