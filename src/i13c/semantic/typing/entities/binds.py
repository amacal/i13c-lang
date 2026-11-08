from dataclasses import dataclass

from i13c.semantic.typing.identifiers.parameters import ParameterId
from i13c.semantic.typing.identifiers.results import ResultId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Bind:
    ref: Span
    ctx: ParameterId | ResultId

    src: bytes
    dst: bytes
