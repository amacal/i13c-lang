from dataclasses import dataclass

from i13c.semantic.typing.identifiers.flags import FlagsId
from i13c.semantic.typing.identifiers.functions import FunctionId
from i13c.semantic.typing.identifiers.signatures import SignatureId
from i13c.semantic.typing.identifiers.statements import StatementId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Function:
    ref: Span
    id: FunctionId

    signature: SignatureId
    flags: FlagsId | None
    statements: list[StatementId]
