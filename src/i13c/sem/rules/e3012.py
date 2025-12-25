from typing import List

from i13c import diag, err
from i13c.sem.nodes import Function


def validate_entrypoint_never_returns(
    functions: List[Function],
) -> List[diag.Diagnostic]:

    for fn in functions:
        if fn.name == b"main":
            if not fn.noreturn:
                return [
                    err.report_e3012_non_terminal_entrypoint_function(
                        fn.ref,
                    )
                ]

    return []
