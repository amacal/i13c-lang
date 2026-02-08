from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.indices.variables import Variable, VariableId


class VariableListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[VariableId, Variable]]:
        return graph.basic.variables.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Variable ID",
            "name": "Variable Name",
            "type": "Variable Type",
            "kind": "Variable Kind",
            "src": "Variable Source",
        }

    @staticmethod
    def rows(entry: Tuple[VariableId, Variable]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].ident),
            "type": str(entry[1].type),
            "kind": entry[1].kind.decode(),
            "src": entry[1].source.identify(1),
        }
