from dataclasses import dataclass

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


ShuffleTarget = CallingTarget
ShuffleMoveOrExchange = ShuffleMove | ShuffleExchange


@dataclass(kw_only=True)
class ShuffleCallSite:
    calling: Calling
    target: ShuffleTarget
    moves: list[ShuffleMoveOrExchange]


@dataclass(kw_only=True)
class Shuffle:
    ref: Span
    target: FunctionId

    callsites: list[ShuffleCallSite]
