from typing import List

from i13c import diag, err
from i13c.sem.nodes import Function


def validate_entrypoint_exists(
    functions: List[Function],
) -> List[diag.Diagnostic]:
    for fn in functions:
        if fn.name == b"main":
            return []

    return [err.report_e3011_missing_entrypoint_function()]
