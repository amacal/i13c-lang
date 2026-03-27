from typing import List, Set

from i13c import err
from i13c.core import diagnostics
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId


def configure_e3005() -> GraphNode:
    return GraphNode(
        builder=validate_duplicated_snippet_clobbers,
        constraint=None,
        produces=("rules/e3005",),
        requires=frozenset({("snippets", "entities/snippets")}),
    )


def validate_duplicated_snippet_clobbers(
    snippets: OneToOne[SnippetId, Snippet],
) -> List[diagnostics.Diagnostic]:
    diagnostics: List[diagnostics.Diagnostic] = []

    for snippet in snippets.values():
        seen: Set[bytes] = set()

        for reg in snippet.clobbers:
            if reg.name in seen:
                diagnostics.append(
                    err.report_e3005_duplicated_snippet_clobbers(
                        snippet.ref,
                        reg.name,
                    )
                )
            else:
                seen.add(reg.name)

    return diagnostics
