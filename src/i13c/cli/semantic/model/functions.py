from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.functions import Function, FunctionId


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
    def rows(key: FunctionId, value: Function) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "name": str(value.identifier),
            "params": str(len(value.parameters)),
            "stmts": str(len(value.statements)),
        }
