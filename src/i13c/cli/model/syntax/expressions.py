from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId
from i13c.syntax import tree


class ExpressionListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, tree.function.Expression]]:
        return artifacts.syntax_graph().expressions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "name": "Expression Name",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, tree.function.Expression]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "name": entry[1].name.decode(),
        }
