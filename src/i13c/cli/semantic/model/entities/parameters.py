from typing import Dict, Iterable, Tuple

from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId


class ParameterListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[ParameterId, Parameter]]:
        return graph.basic.parameters.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Parameter ID",
            "name": "Parameter Name",
            "type": "Parameter Type",
        }

    @staticmethod
    def rows(entry: Tuple[ParameterId, Parameter]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].ident),
            "type": str(entry[1].type),
        }
