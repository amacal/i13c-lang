from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.environments import EnvironmentId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.environments import EnvironmentAcceptance


def configure_environments_by_snippets() -> GraphNode:
    return GraphNode(
        builder=build_environments_by_snippets,
        constraint=None,
        produces=("indices/environments/snippets",),
        requires=frozenset({("environments", "resolutions/environments/accepted")}),
    )


def build_environments_by_snippets(
    environments: OneToOne[EnvironmentId, EnvironmentAcceptance],
) -> OneToOne[SnippetId, EnvironmentAcceptance]:
    index: Dict[SnippetId, EnvironmentAcceptance] = {}

    for _, entry in environments.items():
        index[entry.ctx] = entry

    return OneToOne[SnippetId, EnvironmentAcceptance].instance(index)
