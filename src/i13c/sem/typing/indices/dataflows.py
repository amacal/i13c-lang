from dataclasses import dataclass
from typing import List

from i13c.sem.typing.indices.variables import VariableId


@dataclass(kw_only=True)
class DataFlow:
    declares: List[VariableId]
    reads: List[VariableId]
    writes: List[VariableId]
