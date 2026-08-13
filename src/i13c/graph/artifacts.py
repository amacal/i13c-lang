from dataclasses import dataclass
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import AbstractListExtractor, GraphViews
from i13c.llvm.graph import LowLevelGraph
from i13c.semantic.model import SemanticGraph, SemanticRules
from i13c.semantic.syntax import SyntaxGraph


@dataclass(kw_only=True)
class GraphArtifacts:
    data: dict[str, Any]
    views: dict[str, GraphViews]

    def syntax_graph(self) -> SyntaxGraph:
        return self.data["syntax/graph"]

    def semantic_graph(self) -> SemanticGraph:
        for x in self.rules().enumerate():
            print(x.code, x.message)

        return self.data["semantic/graph"]

    def rules(self) -> SemanticRules:
        return self.data["rules/semantic"]

    def rule_by_name(self, name: str) -> list[Diagnostic]:
        return self.rules().get(name)

    def llvm_graph(self) -> LowLevelGraph:
        return self.data["llvm/graph"]

    def list_view(self, name: str) -> AbstractListExtractor[Any, Any] | None:
        if view := self.views.get(name): # noqa: SIM102
            if list := view.list: # noqa: SIM102
                if data := self.data.get(name):
                    return list(data)

        return None
