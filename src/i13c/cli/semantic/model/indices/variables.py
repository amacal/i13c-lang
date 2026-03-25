from typing import Dict, Iterable, Optional, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.indices.variables import VariableId, VariableSource
from i13c.src import Span


class ParameterVariablesListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[
        Tuple[VariableSource, VariableId, Optional[Parameter], Optional[Value]]
    ]:
        graph = artifacts.semantic_graph()
        index = graph.indices.variables_by_parameter

        parameters = graph.basic.parameters
        values = graph.basic.values

        def get_parameter(sid: VariableSource) -> Optional[Parameter]:
            return parameters.find(sid) if isinstance(sid, ParameterId) else None

        def get_value(sid: VariableSource) -> Optional[Value]:
            return values.find(sid) if isinstance(sid, ValueId) else None

        return (
            (sid, vid, get_parameter(sid), get_value(sid)) for sid, vid in index.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "sid": "Source ID",
            "name": "Source Name",
            "vid": "Variable ID",
        }

    @staticmethod
    def rows(
        entry: Tuple[VariableSource, VariableId, Optional[Parameter], Optional[Value]],
    ) -> Dict[str, str]:
        def into_source() -> Optional[Span]:
            entity = entry[2] or entry[3]
            return entity.ref if entity else None

        def into_name() -> Optional[str]:
            entity = entry[2] or entry[3]
            return str(entity.ident) if entity else None

        return {
            "ref": str(into_source()),
            "sid": entry[0].identify(1),
            "name": str(into_name()),
            "vid": entry[1].identify(1),
        }
