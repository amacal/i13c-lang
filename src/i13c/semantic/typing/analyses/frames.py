from dataclasses import dataclass

from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class StackFrameMove:
    src: bytes
    dst: bytes


@dataclass(kw_only=True)
class StackFrameSpill:
    name: bytes
    slot: int


@dataclass(kw_only=True)
class StackFrameSave:
    name: bytes


@dataclass(kw_only=True)
class StackFrame:
    ref: Span
    target: FunctionId

    slots: int
    moved: list[StackFrameMove]
    spill: list[StackFrameSpill]
    saved: list[StackFrameSave]
