from typing import Dict, Iterable, Tuple

from i13c.ast import Expression
from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId


class ExpressionListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, Expression]]:
        return artifacts.syntax_graph().expressions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "name": "Expression Name",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, Expression]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "name": entry[1].name.decode(),
        }
