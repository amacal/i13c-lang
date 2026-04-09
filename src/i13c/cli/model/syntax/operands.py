from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId
from i13c.syntax import tree


class OperandListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[NodeId, tree.snippet.Operand]]:
        return artifacts.syntax_graph().operands.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "kind": "Operand Kind",
            "reg_name": "Register Name",
            "imm_value": "Immediate Value",
            "ref_name": "Reference Name",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, tree.snippet.Operand]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "kind": type(entry[1]).__name__.lower(),
            "reg_name": (
                entry[1].name.decode()
                if isinstance(entry[1], tree.snippet.Register)
                else ""
            ),
            "imm_value": (
                str(entry[1]) if isinstance(entry[1], tree.snippet.Immediate) else ""
            ),
            "ref_name": (
                entry[1].name.decode()
                if isinstance(entry[1], tree.snippet.Reference)
                else ""
            ),
        }
