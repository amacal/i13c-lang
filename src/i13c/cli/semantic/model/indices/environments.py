from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.indices.controlflows import FlowNode
from i13c.semantic.typing.indices.environments import Environment


class EnvironmentListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, FlowNode, Environment]]:
        functions = artifacts.semantic_graph().basic.functions
        flows = artifacts.semantic_graph().indices.flowgraph_by_function
        environments = artifacts.semantic_graph().indices.environment_by_flownode

        for fid, flowgraph in flows.items():
            for node in flowgraph.nodes():
                function = functions.get(fid)
                if environment := environments.get(node):
                    yield (fid, function, node, environment)

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "fid": "Function ID",
            "name": "Function Name",
            "flow": "Flow Node",
            "owner": "Owner",
            "idents": "Identifiers",
        }

    @staticmethod
    def rows(
        entry: Tuple[FunctionId, Function, FlowNode, Environment],
    ) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "fid": str(entry[0].identify(1)),
            "name": str(entry[1].identifier),
            "flow": str(entry[2].identify(1)),
            "owner": str(entry[3].owner.identify(1)),
            "idents": " ".join(str(ident) for ident in entry[3].variables.keys()),
        }
