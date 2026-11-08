from dataclasses import dataclass

from i13c.semantic.syntax import NodeId


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int

    @staticmethod
    def from_context(nid: NodeId) -> SnippetId:
        return SnippetId(value=nid.value)

    def identify(self, length: int) -> str:
        return "#".join(("snippet", f"{self.value:<{length}}"))
