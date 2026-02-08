from dataclasses import dataclass
from typing import Any, Callable, FrozenSet, Tuple

CallgraphBuilder = Callable[..., Any]


@dataclass(kw_only=True, frozen=True)
class Configuration:
    builder: CallgraphBuilder
    produces: Tuple[str, ...]
    requires: FrozenSet[Tuple[str, str]]
