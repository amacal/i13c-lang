from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.indices.controlflows import FlowNode
from i13c.semantic.typing.indices.dataflows import DataFlow


class DataFlowListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, FlowNode, DataFlow]]:
        return (
            (
                fid,
                artifacts.semantic_graph().basic.functions.get(fid),
                flownode,
                artifacts.semantic_graph().indices.dataflow_by_flownode.get(flownode),
            )
            for fid, controlflow in artifacts.semantic_graph().indices.flowgraph_by_function.items()
            for flownode in sorted(controlflow.nodes(), key=lambda n: n.identify(1))
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Function ID",
            "name": "Function Name",
            "node": "ControlFlow Node",
            "declares": "DataFlow Declares",
            "uses": "DataFlow Uses",
            "drops": "DataFlow Drops",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, FlowNode, DataFlow]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "node": entry[2].identify(1),
            "declares": str(len(entry[3].declares)),
            "uses": str(len(entry[3].uses)),
            "drops": str(len(entry[3].drops)),
        }
