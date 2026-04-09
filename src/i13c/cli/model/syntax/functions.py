from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId
from i13c.syntax import tree


class FunctionListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[NodeId, tree.function.Function]]:
        return artifacts.syntax_graph().functions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "name": "Function Name",
            "noreturn": "No Return",
            "params": "Parameters",
            "stmts": "Statements",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, tree.function.Function]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "name": str(entry[1].name.decode()),
            "noreturn": str(entry[1].noreturn).lower(),
            "params": str(len(entry[1].parameters)),
            "stmts": str(len(entry[1].statements)),
        }
