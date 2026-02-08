from typing import Dict, Iterable, Tuple

from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.functions import Function, FunctionId


class FunctionListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[FunctionId, Function]]:
        return graph.basic.functions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Function ID",
            "name": "Function Name",
            "params": "Parameters",
            "stmts": "Statements",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "params": str(len(entry[1].parameters)),
            "stmts": str(len(entry[1].statements)),
        }
