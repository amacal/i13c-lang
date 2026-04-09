from dataclasses import dataclass
from typing import Optional

from i13c.syntax.tree.literals import Hex


@dataclass(kw_only=True, eq=False)
class Type:
    name: bytes
    range: Optional[Range]


@dataclass(kw_only=True, eq=False)
class Range:
    lower: Hex
    upper: Hex
