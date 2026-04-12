from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.environments import Environment, EnvironmentId
from i13c.semantic.typing.entities.labels import LabelId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId


def configure_environments() -> GraphNode:
    return GraphNode(
        builder=build_environments,
        constraint=None,
        produces=("entities/environments",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_environments(
    graph: SyntaxGraph,
) -> OneToOne[EnvironmentId, Environment]:
    environments: Dict[EnvironmentId, Environment] = {}

    for id, entry in graph.snippets.items():
        # derive environment ID from globally unique node ID
        environment_id = EnvironmentId(value=id.value)

        # look up for the snippet context of this environment
        snippet_id = SnippetId(value=id.value)

        # append empty environment for now, the entries will be filled in the next steps
        environments[environment_id] = Environment(
            ref=entry.ref,
            kind="snippet",
            entries=[],
            ctx=snippet_id,
        )

    # append signatures to the environments of their snippet contexts
    for id, entry in graph.signatures.items():
        # derive signature ID from globally unique node ID
        signature_id = SignatureId(value=id.value)

        # look up for the snippet context of this signature
        snippet = graph.signatures.get_ctx(id)
        nid = graph.snippets.get_by_node(snippet)
        snippet_id = SnippetId(value=nid.value)

        # append this signature to the environment of the snippet context
        environment_id = EnvironmentId(value=nid.value)
        environments[environment_id].entries.append(signature_id)

    # append labels to the environments of their snippet contexts
    for id, entry in graph.labels.items():
        # derive label ID from globally unique node ID
        label_id = LabelId(value=id.value)

        # look up for the snippet context of this label
        snippet = graph.labels.get_ctx(id)
        nid = graph.snippets.get_by_node(snippet)
        snippet_id = SnippetId(value=nid.value)

        # append this label to the environment of the snippet context
        environment_id = EnvironmentId(value=nid.value)
        environments[environment_id].entries.append(label_id)

    return OneToOne[EnvironmentId, Environment].instance(environments)
