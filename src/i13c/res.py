from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class Ok(Generic[A]):
    value: A


@dataclass(frozen=True)
class Err(Generic[B]):
    error: B


Result = Ok[A] | Err[B]


def unwrap(r: Result[A, B], callback: Callable[[B], A]) -> A:
    match r:
        case Ok(v):
            return v
        case Err(e):
            return callback(e)
