from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int


@dataclass(kw_only=True, frozen=True)
class SlotId:
    value: int


@dataclass(kw_only=True, frozen=True)
class ParameterId:
    value: int


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int


@dataclass(kw_only=True, frozen=True)
class RegisterId:
    value: int


@dataclass(kw_only=True, frozen=True)
class CallId:
    value: int


@dataclass(kw_only=True, frozen=True)
class StatementId:
    value: int


@dataclass(kw_only=True, frozen=True)
class ArgumentId:
    value: int
