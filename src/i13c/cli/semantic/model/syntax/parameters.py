from typing import Dict, Iterable, Tuple

from i13c.ast import Parameter
from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId


class ParameterListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, Parameter]]:
        return artifacts.syntax_graph().parameters.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "name": "Parameter Name",
            "type": "Parameter Type",
            "range": "Parameter Range",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, Parameter]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "name": entry[1].name.decode(),
            "type": entry[1].type.name.decode(),
            "range": (
                f"{entry[1].type.range.lower:#06x}..{entry[1].type.range.upper:#06x}"
                if entry[1].type.range
                else ""
            ),
        }
