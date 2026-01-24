from dataclasses import dataclass
from typing import List

from i13c.sem.typing.indices.variables import VariableId


@dataclass(kw_only=True)
class DataFlow:
    declares: List[VariableId]
    uses: List[VariableId]
    drops: List[VariableId]

    def describe(self) -> str:
        return f"declares={len(self.declares)}, uses={len(self.uses)}, drops={len(self.drops)}"
