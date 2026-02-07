from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.literals import Literal, LiteralId


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
    def rows(key: LiteralId, value: Literal) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "kind": value.kind.decode(),
            "hex-value": str(value.target.value),
            "hex-width": str(value.target.width),
        }
