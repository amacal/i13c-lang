from typing import List, Set

from i13c import diag, err
from i13c.sem.graph import Graph


def validate_duplicated_snippet_clobbers(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for snid, rids in graph.edges.snippet_clobbers.items():
        seen: Set[bytes] = set()

        for clobber in graph.nodes.registers.find_by_ids(rids):
            if clobber.name in seen:
                if snippet := graph.nodes.snippets.find_by_id(snid):
                    diagnostics.append(
                        err.report_e3005_duplicated_snippet_clobbers(
                            snippet.ref,
                            clobber.name,
                        )
                    )
            else:
                seen.add(clobber.name)

    return diagnostics
