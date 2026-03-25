from dataclasses import dataclass
from typing import Literal as Kind
from typing import Optional, Union

from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.indices.variables import VariableId

ValueRejectionReason = Kind[b"type-mismatch", b"unbound"]
ValueBinding = Union[LiteralId, VariableId]


@dataclass(kw_only=True)
class ValueAcceptance:
    binding: ValueBinding


@dataclass(kw_only=True)
class ValueRejection:
    reason: ValueRejectionReason


@dataclass(kw_only=True)
class ValueResolution:
    accepted: Optional[ValueAcceptance]
    rejected: Optional[ValueRejection]
