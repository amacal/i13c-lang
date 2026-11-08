from dataclasses import dataclass

from i13c.semantic.typing.identifiers.types import TypeId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Parameter:
    ref: Span
    name: bytes
    type: TypeId
