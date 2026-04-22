from dataclasses import dataclass
from typing import Any, Dict, List

from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.entities.snippets import SnippetId


@dataclass(kw_only=True)
class Instance:
    target: SnippetId
    bindings: List[Any]
    operands: Dict[OperandId, Operand]
