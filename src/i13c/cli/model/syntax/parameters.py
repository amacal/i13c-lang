from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId
from i13c.syntax import tree


class ParameterListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, tree.function.Parameter]]:
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
    def rows(entry: Tuple[NodeId, tree.function.Parameter]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "name": entry[1].name.decode(),
            "type": entry[1].type.name.decode(),
            "range": (
                f"0x{entry[1].type.range.lower.hex()}..0x{entry[1].type.range.upper.hex()}"
                if entry[1].type.range
                else ""
            ),
        }
