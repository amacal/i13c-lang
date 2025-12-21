from dataclasses import dataclass
from typing import Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class Ok(Generic[A]):
    value: A


@dataclass(frozen=True)
class Err(Generic[B]):
    error: B


Result = Ok[A] | Err[B]
