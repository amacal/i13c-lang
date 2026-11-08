from dataclasses import dataclass

from i13c.semantic.syntax import NodeId


@dataclass(kw_only=True, frozen=True)
class StatementId:
    value: int

    @staticmethod
    def from_context(nid: NodeId) -> StatementId:
        return StatementId(value=nid.value)

    def identify(self, length: int) -> str:
        return "#".join(("statement", f"{self.value:<{length}}"))
