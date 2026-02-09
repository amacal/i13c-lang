from typing import List

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.semantic.model import SemanticGraph


def configure_e3000() -> GraphNode:
    return GraphNode(
        builder=validate_assembly_mnemonic,
        produces=("rules/e3000",),
        requires=frozenset({("graph", "semantic/graph")}),
    )


def validate_assembly_mnemonic(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for iid, resolution in graph.indices.resolution_by_instruction.items():
        if not resolution.accepted and not resolution.rejected:
            diagnostics.append(
                err.report_e3000_unknown_instruction(
                    graph.basic.instructions.get(iid).ref
                )
            )

    return diagnostics
