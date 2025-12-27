from typing import List

from i13c import diag, err
from i13c.sem.asm import Immediate
from i13c.sem.model import SemanticGraph


def validate_immediate_out_of_range(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for instruction in graph.instructions.values():
        for operand in instruction.operands:
            if operand.kind == b"immediate":

                # satisfy type checker
                assert isinstance(operand.target, Immediate)

                if operand.target.width is None:
                    diagnostics.append(
                        err.report_e3001_immediate_out_of_range(
                            instruction.ref,
                            operand.target.value,
                        )
                    )

    return diagnostics
