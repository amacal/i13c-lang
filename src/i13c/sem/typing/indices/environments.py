from dataclasses import dataclass
from typing import Dict

from i13c.sem.core import Identifier
from i13c.sem.typing.indices.variables import VariableId


@dataclass(kw_only=True)
class Environment:
    variables: Dict[Identifier, VariableId]

    def describe(self) -> str:
        return f"variables={len(self.variables)}"

    @staticmethod
    def empty() -> Environment:
        return Environment(variables={})
