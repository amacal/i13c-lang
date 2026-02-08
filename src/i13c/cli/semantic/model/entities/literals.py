from typing import Dict, Iterable, Tuple

from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.literals import Literal, LiteralId


class LiteralListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[LiteralId, Literal]]:
        return graph.basic.literals.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Literal ID",
            "kind": "Literal Kind",
            "hex-value": "Hex Value",
            "hex-width": "Hex Width",
        }

    @staticmethod
    def rows(entry: Tuple[LiteralId, Literal]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "kind": entry[1].kind.decode(),
            "hex-value": str(entry[1].target.value),
            "hex-width": str(entry[1].target.width),
        }
