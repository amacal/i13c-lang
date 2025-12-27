from typing import List

from i13c import diag
from i13c.sem.model import SemanticGraph


def validate_immediate_out_of_range(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    # for snippet in graph.snippets.values():
    #     for instruction in snippet.instructions:
    #         for operand in instruction.operands:
    #             if operand.kind == b"immediate":

    #                 # satisfy type checker
    #                 assert isinstance(operand.target, Immediate)

    #                 if operand.target.width is None:
    #                     diagnostics.append(
    #                         err.report_e3001_immediate_out_of_range(
    #                             instruction.ref,
    #                             operand.target.value,
    #                         )
    #                     )

    return diagnostics
