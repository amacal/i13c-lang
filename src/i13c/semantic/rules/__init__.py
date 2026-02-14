from dataclasses import dataclass
from typing import Dict, List

from i13c.core.dag import GraphGroup, GraphNode, Prefix
from i13c.diag import Diagnostic
from i13c.semantic.rules.e3000 import configure_e3000
from i13c.semantic.rules.e3001 import configure_e3001
from i13c.semantic.rules.e3002 import configure_e3002
from i13c.semantic.rules.e3003 import configure_e3003
from i13c.semantic.rules.e3004 import configure_e3004
from i13c.semantic.rules.e3005 import configure_e3005
from i13c.semantic.rules.e3006 import configure_e3006
from i13c.semantic.rules.e3007 import configure_e3007
from i13c.semantic.rules.e3008 import configure_e3008
from i13c.semantic.rules.e3010 import configure_e3010
from i13c.semantic.rules.e3011 import configure_e3011
from i13c.semantic.rules.e3012 import configure_e3012


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


def configure_rules() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_e3000(),
            configure_e3001(),
            configure_e3002(),
            configure_e3003(),
            configure_e3004(),
            configure_e3005(),
            configure_e3006(),
            configure_e3007(),
            configure_e3008(),
            configure_e3010(),
            configure_e3011(),
            configure_e3012(),
            configure_e3xxx(),
        ]
    )
