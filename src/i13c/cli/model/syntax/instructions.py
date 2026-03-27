from typing import Dict, Iterable, Tuple

from i13c.ast import Instruction
from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.syntax import NodeId


class InstructionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[NodeId, Instruction]]:
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
    def rows(entry: Tuple[NodeId, Instruction]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": f"#{entry[0].value}",
            "mnemonic": str(entry[1].mnemonic.name.decode()),
            "ops": str(len(entry[1].operands)),
        }
