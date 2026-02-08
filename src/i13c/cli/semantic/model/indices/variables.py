from typing import Dict, Iterable, Tuple

from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.indices.variables import VariableId


class ParameterVariablesListExtractor:
    @staticmethod
    def extract(
        graph: SemanticGraph,
    ) -> Iterable[Tuple[ParameterId, VariableId, Parameter]]:
        return (
            (pid, vid, graph.basic.parameters.get(pid))
            for pid, vid in graph.indices.variables_by_parameter.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "pid": "Parameter ID",
            "name": "Parameter Name",
            "vid": "Variable ID",
        }

    @staticmethod
    def rows(entry: Tuple[ParameterId, VariableId, Parameter]) -> Dict[str, str]:
        return {
            "ref": str(entry[2].ref),
            "pid": entry[0].identify(1),
            "name": str(entry[2].ident),
            "vid": entry[1].identify(1),
        }
