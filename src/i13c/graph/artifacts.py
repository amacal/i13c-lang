from dataclasses import dataclass
from typing import Any, Dict, Optional

from i13c.lowering.graph import LowLevelGraph
from i13c.semantic.model import SemanticGraph
from i13c.semantic.rules import SemanticRules
from i13c.semantic.syntax import SyntaxGraph


@dataclass(kw_only=True)
class GraphArtifacts:
    data: Dict[str, Any]

    def syntax_graph(self) -> SyntaxGraph:
        return self.data["syntax/graph"]

    def semantic_graph(self) -> SemanticGraph:
        return self.data["semantic/graph"]

    def rules(self) -> SemanticRules:
        return self.data["rules/semantic"]

    def llvm_graph(self) -> Optional[LowLevelGraph]:
        return self.data["llvm/graph"]
