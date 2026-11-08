from dataclasses import dataclass

from i13c.semantic.syntax import NodeId


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int

    @staticmethod
    def from_context(nid: NodeId) -> FunctionId:
        return FunctionId(value=nid.value)

    def identify(self, length: int) -> str:
        return "#".join(("function", f"{self.value:<{length}}"))

    def __str__(self) -> str:
        return self.identify(1)
