from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId


class InstructionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[InstructionId, Instruction]]:
        return artifacts.semantic_graph().basic.instructions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Instruction ID",
            "mnemonic": "Mnemonic",
            "ops": "Operands",
        }

    @staticmethod
    def rows(entry: Tuple[InstructionId, Instruction]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "mnemonic": str(entry[1].mnemonic),
            "ops": str(len(entry[1].operands)),
        }
