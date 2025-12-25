from dataclasses import dataclass


@dataclass(kw_only=True)
class Type:
    name: bytes


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True)
class Immediate:
    value: int


@dataclass(kw_only=True)
class Literal:
    value: int
