from dataclasses import dataclass
from typing import Dict, List

from i13c import src


@dataclass(kw_only=True)
class SigType:
    name: bytes


@dataclass(kw_only=True)
class SigParameter:
    name: bytes
    type: SigType


@dataclass(kw_only=True)
class SymbolFunction:
    parameters: List[SigParameter]


@dataclass(kw_only=True)
class SymbolTableEntry:
    ref: src.Span
    name: bytes
    target: SymbolFunction


@dataclass(kw_only=True)
class SymbolTable:
    entries: Dict[bytes, SymbolTableEntry]
