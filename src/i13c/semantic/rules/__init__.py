from dataclasses import dataclass
from typing import Dict, List

from i13c.core.dag import GraphNode, Prefix
from i13c.diag import Diagnostic


def configure_e3xxx() -> GraphNode:
    return GraphNode(
        builder=build,
        produces=("rules/semantic",),
        requires=frozenset({("rules", Prefix(value="rules/e3"))}),
    )


@dataclass(kw_only=True)
class SemanticRules:
    data: Dict[str, List[Diagnostic]]


def build(rules: Dict[str, List[Diagnostic]]) -> SemanticRules:
    return SemanticRules(data=rules)
