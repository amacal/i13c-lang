from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.indices.controlflows import FlowGraph


class ControlFlowListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, FlowGraph]]:
        return (
            (fid, artifacts.semantic_graph().basic.functions.get(fid), flowgraph)
            for fid, flowgraph in artifacts.semantic_graph().indices.flowgraph_by_function.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Function ID",
            "name": "Function Name",
            "nodes": "Nodes",
            "edges": "Edges",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, FlowGraph]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "nodes": str(len(entry[2].nodes())),
            "edges": str(sum(1 for _ in entry[2].edges())),
        }
