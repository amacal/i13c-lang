from dataclasses import dataclass

from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.callings import Calling, CallingTarget
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class ShuffleMove:
    src: bytes
    dst: bytes


@dataclass(kw_only=True)
class ShuffleExchange:
    src: bytes
    dst: bytes


@dataclass(kw_only=True)
class ShuffleLoad:
    src: int
    dst: bytes


@dataclass(kw_only=True)
class ShuffleImmediate:
    src: Hex
    dst: bytes


ShuffleTarget = CallingTarget
ShuffleMoves = ShuffleMove | ShuffleExchange | ShuffleLoad | ShuffleImmediate


@dataclass(kw_only=True)
class ShuffleCallSite:
    calling: Calling
    target: ShuffleTarget
    moves: list[ShuffleMoves]


@dataclass(kw_only=True)
class Shuffle:
    ref: Span
    target: FunctionId

    callsites: list[ShuffleCallSite]
