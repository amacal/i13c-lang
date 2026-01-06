from typing import List, Set

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_duplicated_slot_bindings(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for snippet in graph.basic.snippets.values():
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
