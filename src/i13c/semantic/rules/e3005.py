from typing import List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.syntax.source import SpanLike


def configure_e3005() -> GraphNode:
    return GraphNode(
        builder=validate_duplicated_snippet_clobbers,
        constraint=None,
        produces=("rules/e3005",),
        requires=frozenset({("snippets", "entities/snippets")}),
    )


def validate_duplicated_snippet_clobbers(
    snippets: OneToOne[SnippetId, Snippet],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for snippet in snippets.values():
        seen: Set[bytes] = set()

        for reg in snippet.clobbers:
            if reg.name in seen:
                diagnostics.append(
                    report_e3005_duplicated_snippet_clobbers(
                        snippet.ref,
                        reg.name,
                    )
                )
            else:
                seen.add(reg.name)

    return diagnostics


def report_e3005_duplicated_snippet_clobbers(ref: SpanLike, found: bytes) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3005",
        message=f"Duplicated clobber registers for ({str(found)}) at offset {ref.offset}",
    )
