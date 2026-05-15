from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance


@dataclass(kw_only=True)
class ControlPaths:
    flows: ControlFlowAcceptance
    paths: List[List[int]]
