from typing import Dict, Iterable, Tuple

from i13c.ast import IntegerLiteral, Literal
from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId


class LiteralListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, Literal]]:
        return artifacts.syntax_graph().literals.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "kind": "Literal Kind",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, Literal]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "kind": type(entry[1]).__name__,
        }


class LiteralIntegersListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, IntegerLiteral]]:
        return artifacts.syntax_graph().literals.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "value": "Integer Value",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, IntegerLiteral]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "value": str(entry[1].value),
        }
