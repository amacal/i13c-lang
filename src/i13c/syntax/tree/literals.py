from dataclasses import dataclass


@dataclass(kw_only=True, eq=False)
class Hex:
    digits: bytes
