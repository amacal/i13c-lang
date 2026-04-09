from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId
from i13c.syntax import tree


class LiteralListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[NodeId, tree.function.Literal]]:
        return artifacts.syntax_graph().literals.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "kind": "Literal Kind",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, tree.function.Literal]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "kind": type(entry[1]).__name__,
        }


class LiteralIntegersListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[NodeId, tree.function.IntegerLiteral]]:
        return artifacts.syntax_graph().literals.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "value": "Integer Value",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, tree.function.IntegerLiteral]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "value": f"0x{entry[1].value.hex()}",
        }
