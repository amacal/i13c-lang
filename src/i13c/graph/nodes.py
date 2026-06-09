from typing import Optional

from i13c.core.generator import Generator
from i13c.core.graph import GraphGroup, evaluate
from i13c.graph.artifacts import GraphArtifacts
from i13c.llvm.build import configure_llvm_graph
from i13c.semantic.graph import configure_semantic_graph
from i13c.semantic.syntax import configure_syntax_graph
from i13c.syntax.tree import Program


def run(program: Program, target: Optional[str] = None) -> GraphArtifacts:
    nodes = GraphGroup(
        nodes=[
            configure_syntax_graph(),
            configure_semantic_graph(),
            configure_llvm_graph(),
        ],
    )

    views, artifacts = evaluate(
        nodes.flatten(),
        initial={
            "core/generator": Generator(),
            "ast/program": program,
        },
        targets={target} if target else set(),
    )

    return GraphArtifacts(data=artifacts, views=views)
