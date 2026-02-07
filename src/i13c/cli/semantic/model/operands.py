from typing import Dict, Iterable, Tuple

from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.operands import (
    Immediate,
    Operand,
    OperandId,
    Reference,
    Register,
)


class OperandListExtractor:
    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[Tuple[OperandId, Operand]]:
        return graph.basic.operands.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Operand ID",
            "kind": "Operand Kind",
            "reg_name": "Register Name",
            "reg_width": "Register Width",
            "imm_value": "Immediate Value",
            "imm_width": "Immediate Width",
            "ref_name": "Reference Name",
        }

    @staticmethod
    def rows(key: OperandId, value: Operand) -> Dict[str, str]:
        return {
            "ref": str(value.ref),
            "id": key.identify(1),
            "kind": value.kind.decode(),
            "reg_name": (
                value.target.name.decode() if isinstance(value.target, Register) else ""
            ),
            "reg_width": (
                str(value.target.width) if isinstance(value.target, Register) else ""
            ),
            "imm_value": (
                str(value.target.value) if isinstance(value.target, Immediate) else ""
            ),
            "imm_width": (
                str(value.target.width) if isinstance(value.target, Immediate) else ""
            ),
            "ref_name": (
                value.target.name.decode()
                if isinstance(value.target, Reference)
                else ""
            ),
        }
