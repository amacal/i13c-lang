from dataclasses import dataclass

from i13c import src


@dataclass(kw_only=True)
class Diagnostic:
    ref: src.SpanLike
    code: str
    message: str
