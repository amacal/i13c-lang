from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.indices.terminalities import Terminality


class TerminalityListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, Terminality]]:
        return (
            (fid, artifacts.semantic_graph().basic.functions.get(fid), terminality)
            for fid, terminality in artifacts.semantic_graph().indices.terminality_by_function.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Function ID",
            "name": "Function Name",
            "fnotret": "Function NoReturn",
            "tnoret": "Terminality NoReturn",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, Terminality]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "fnotret": str(entry[1].noreturn).lower(),
            "tnoret": str(entry[2].noreturn).lower(),
        }
