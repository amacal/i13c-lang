from typing import Dict, Iterable, Tuple

from i13c.ast import Snippet
from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId


class SnippetListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, Snippet]]:
        return artifacts.syntax_graph().snippets.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "name": "Snippet Name",
            "slots": "Slots",
            "clbbrs": "Clobbers",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, Snippet]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "name": str(entry[1].name.decode()),
            "slots": str(len(entry[1].slots)),
            "clbbrs": str(len(entry[1].clobbers)),
            "instrs": str(len(entry[1].instructions)),
        }
