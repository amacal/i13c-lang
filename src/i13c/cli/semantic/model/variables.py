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
    def rows(key: VariableId, value: Variable) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "name": str(value.ident),
            "type": str(value.type),
            "kind": value.kind.decode(),
            "src": value.source.identify(1),
        }
