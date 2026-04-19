from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId


class ParameterListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[ParameterId, Parameter]]:
        return artifacts.semantic_graph().entities.parameters.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Parameter ID",
            "type": "Parameter Type",
        }

    @staticmethod
    def rows(entry: Tuple[ParameterId, Parameter]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "type": entry[1].type.identify(1),
        }
