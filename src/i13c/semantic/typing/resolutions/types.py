from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Optional, Union

from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.ranges import RangeAcceptance
from i13c.syntax.source import Span

TypeRejectionReason = Kind[
    "unknown-type",
    "inconsistent-widths",
]

TypeWidth = Kind[8, 16, 32, 64]


@dataclass(kw_only=True)
class TypeRejection:
    ref: Span
    reason: TypeRejectionReason


@dataclass(kw_only=True)
class TypeAcceptance:
    ref: Span
    id: TypeId

    name: bytes
    width: TypeWidth
    range: Optional[RangeAcceptance]

    def accepts(self, value: Union[LiteralAcceptance, TypeAcceptance]) -> bool:
        if isinstance(value, LiteralAcceptance):
            if value.target.width != self.width:
                return False

            if self.range is not None:
                if Hex.greater(value.target.data, self.range.upper.data):
                    return False

                if Hex.lesser(value.target.data, self.range.lower.data):
                    return False

        else:
            if value.width != self.width:
                return False

            if self.range is not None:
                if value.range is None:
                    return False

                if Hex.greater(value.range.upper.data, self.range.upper.data):
                    return False

                if Hex.lesser(value.range.lower.data, self.range.lower.data):
                    return False

        return True


@dataclass(kw_only=True)
class TypeResolution:
    accepted: List[TypeAcceptance]
    rejected: List[TypeRejection]
