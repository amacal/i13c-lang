from dataclasses import dataclass

from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance


@dataclass(kw_only=True)
class ControlPaths:
    flows: ControlFlowAcceptance
    paths: list[list[int]]
