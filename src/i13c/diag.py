from dataclasses import dataclass
from i13c import ast


@dataclass(kw_only=True)
class Diagnostic:
    ref: ast.Reference
    code: str
    message: str
