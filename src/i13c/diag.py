from dataclasses import dataclass


@dataclass(kw_only=True)
class Diagnostic:
    offset: int
    code: str
    message: str
