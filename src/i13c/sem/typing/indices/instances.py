from dataclasses import dataclass
from typing import Dict, List

from i13c.sem.typing.entities.operands import Operand, OperandId
from i13c.sem.typing.entities.snippets import SnippetId
from i13c.sem.typing.resolutions.callsites import CallSiteBinding


@dataclass(kw_only=True)
class Instance:
    target: SnippetId
    bindings: List[CallSiteBinding]
    operands: Dict[OperandId, Operand]

    def describe(self) -> str:
        return f"target={self.target.value} bindings={len(self.bindings)} operands={len(self.operands)}"
