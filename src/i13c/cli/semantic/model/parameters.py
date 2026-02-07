from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.parameters import Parameter, ParameterId


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
    def rows(key: ParameterId, value: Parameter) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "name": str(value.ident),
            "type": str(value.type),
        }
