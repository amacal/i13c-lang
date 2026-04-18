from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.operands import Operand, OperandId


class OperandListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[OperandId, Operand]]:
        return artifacts.semantic_graph().entities.operands.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Operand ID",
            "kind": "Operand Kind",
            "target": "Operand Target",
        }

    @staticmethod
    def rows(entry: Tuple[OperandId, Operand]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "kind": entry[1].kind,
            "target": entry[1].target.identify(1),
        }
