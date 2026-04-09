from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId
from i13c.syntax import tree


class InstructionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[NodeId, tree.snippet.Instruction]]:
        return artifacts.syntax_graph().instructions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Node ID",
            "mnemonic": "Mnemonic",
            "ops": "Operands",
        }

    @staticmethod
    def rows(entry: Tuple[NodeId, tree.snippet.Instruction]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "mnemonic": str(entry[1].mnemonic.name.decode()),
            "ops": str(len(entry[1].operands)),
        }
