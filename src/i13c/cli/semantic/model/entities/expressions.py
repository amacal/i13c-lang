from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId


class ExpressionListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[ExpressionId, Expression]]:
        return artifacts.semantic_graph().basic.expressions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Expression ID",
            "name": "Expression Name",
        }

    @staticmethod
    def rows(entry: Tuple[ExpressionId, Expression]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].ident),
        }
