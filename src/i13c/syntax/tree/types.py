from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True, eq=False)
class Type:
    name: bytes
    range: Optional[Range]


@dataclass(kw_only=True, eq=False)
class Range:
    lower: bytes
    upper: bytes
