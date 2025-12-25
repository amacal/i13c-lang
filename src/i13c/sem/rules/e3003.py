from typing import List, Set

from i13c import diag, err
from i13c.sem.graph import Graph


def validate_duplicated_slot_bindings(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for snid, slots in graph.edges.snippet_slots.items():
        seen: Set[bytes] = set()

        for slid in slots:
            if rid := graph.edges.slot_bindings.find_by_id(slid):
                if register := graph.nodes.registers.find_by_id(rid):
                    if register.name in seen:
                        if snippet := graph.nodes.snippets.find_by_id(snid):
                            diagnostics.append(
                                err.report_e3003_duplicated_slot_bindings(
                                    snippet.ref,
                                    register.name,
                                )
                            )
                    else:
                        seen.add(register.name)

    return diagnostics
