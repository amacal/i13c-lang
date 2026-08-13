from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Ok[A]:
    value: A


@dataclass(frozen=True)
class Err[B]:
    error: B


type Result[A, B] = Ok[A] | Err[B]


def unwrap[A, B](r: Result[A, B], callback: Callable[[B], A]) -> A:
    match r:
        case Ok(v):
            return v
        case Err(e):
            return callback(e)
