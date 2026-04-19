from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.functions import Function, FunctionId


class FunctionListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[FunctionId, Function]]:
        return artifacts.semantic_graph().entities.functions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Function ID",
            "stmts": "Statements",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "stmts": str(len(entry[1].statements)),
        }
