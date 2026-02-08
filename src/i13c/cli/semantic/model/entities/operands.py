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
    def rows(entry: Tuple[OperandId, Operand]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "kind": entry[1].kind.decode(),
            "reg_name": (
                entry[1].target.name.decode()
                if isinstance(entry[1].target, Register)
                else ""
            ),
            "reg_width": (
                str(entry[1].target.width)
                if isinstance(entry[1].target, Register)
                else ""
            ),
            "imm_value": (
                str(entry[1].target.value)
                if isinstance(entry[1].target, Immediate)
                else ""
            ),
            "imm_width": (
                str(entry[1].target.width)
                if isinstance(entry[1].target, Immediate)
                else ""
            ),
            "ref_name": (
                entry[1].target.name.decode()
                if isinstance(entry[1].target, Reference)
                else ""
            ),
        }
