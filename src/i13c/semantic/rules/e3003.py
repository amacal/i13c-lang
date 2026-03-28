from typing import List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.syntax.source import SpanLike


def configure_e3003() -> GraphNode:
    return GraphNode(
        builder=validate_duplicated_slot_bindings,
        constraint=None,
        produces=("rules/e3003",),
        requires=frozenset({("snippets", "entities/snippets")}),
    )


def validate_duplicated_slot_bindings(
    snippets: OneToOne[SnippetId, Snippet],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for snippet in snippets.values():
        seen: Set[bytes] = set()

        for slot in snippet.slots:

            # ignore immediate bindings
            # they are non-unique by nature
            if slot.bind.via_immediate():
                continue

            if slot.bind.name in seen:
                diagnostics.append(
                    report_e3003_duplicated_slot_bindings(
                        snippet.ref,
                        slot.bind.name,
                    )
                )
            else:
                seen.add(slot.bind.name)

    return diagnostics


def report_e3003_duplicated_slot_bindings(ref: SpanLike, found: bytes) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3003",
        message=f"Duplicated parameter bindings for ({str(found)}) at offset {ref.offset}",
    )
