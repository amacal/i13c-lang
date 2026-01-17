from dataclasses import dataclass
from typing import Union

from i13c.sem.typing.entities.functions import FunctionId


@dataclass(kw_only=True, frozen=True)
class BlockId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("block", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class CallFlow:
    target: FunctionId


Flow = Union[CallFlow]
