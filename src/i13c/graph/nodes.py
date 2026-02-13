from i13c.ast import Program
from i13c.core.dag import GraphGroup, evaluate
from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.graph import configure_semantic_graph
from i13c.semantic.syntax import configure_syntax_graph


def run(program: Program) -> GraphArtifacts:
    nodes = GraphGroup(
        nodes=[
            configure_syntax_graph(),
            configure_semantic_graph(),
        ],
    )

    artifacts = evaluate(
        nodes.flatten(),
        initial={
            "ast/program": program,
        },
    )

    return GraphArtifacts(data=artifacts)
