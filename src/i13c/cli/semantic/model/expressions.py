from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.expressions import Expression, ExpressionId


class ExpressionListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[ExpressionId, Expression]]:
        return graph.basic.expressions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Expression ID",
            "name": "Expression Name",
        }

    @staticmethod
    def rows(key: ExpressionId, value: Expression) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "name": str(value.ident),
        }
