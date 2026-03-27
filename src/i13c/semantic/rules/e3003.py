from typing import List, Set

from i13c import err
from i13c.core import diagnostics
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId


def configure_e3003() -> GraphNode:
    return GraphNode(
        builder=validate_duplicated_slot_bindings,
        constraint=None,
        produces=("rules/e3003",),
        requires=frozenset({("snippets", "entities/snippets")}),
    )


def validate_duplicated_slot_bindings(
    snippets: OneToOne[SnippetId, Snippet],
) -> List[diagnostics.Diagnostic]:
    diagnostics: List[diagnostics.Diagnostic] = []

    for snippet in snippets.values():
        seen: Set[bytes] = set()

        for slot in snippet.slots:

            # ignore immediate bindings
            # they are non-unique by nature
            if slot.bind.via_immediate():
                continue

            if slot.bind.name in seen:
                diagnostics.append(
                    err.report_e3003_duplicated_slot_bindings(
                        snippet.ref,
                        slot.bind.name,
                    )
                )
            else:
                seen.add(slot.bind.name)

    return diagnostics
