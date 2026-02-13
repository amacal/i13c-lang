from typing import Dict, Iterable, Tuple

from i13c.ast import CallStatement, Statement
from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId


class StatementListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[NodeId, Statement]]:
        return artifacts.syntax_graph().statements.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "kind": "Statement Kind",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, Statement]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "kind": type(entry[1]).__name__,
        }


class StatementCallsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[NodeId, CallStatement]]:
        return artifacts.syntax_graph().statements.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "callee": "Callee",
            "args": "Arguments",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, CallStatement]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "callee": entry[1].name.decode(),
            "args": str(len(entry[1].arguments)),
        }
