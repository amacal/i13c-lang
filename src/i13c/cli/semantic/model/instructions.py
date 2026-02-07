from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.instructions import Instruction, InstructionId


class InstructionListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[InstructionId, Instruction]]:
        return graph.basic.instructions.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Instruction ID",
            "mnemonic": "Mnemonic",
            "ops": "Operands",
        }

    @staticmethod
    def rows(key: InstructionId, value: Instruction) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "mnemonic": str(value.mnemonic),
            "ops": str(len(value.operands)),
        }
