from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.indices.controlflows import ControlFlowListExtractor
from i13c.cli.semantic.model.indices.dataflows import DataFlowListExtractor
from i13c.cli.semantic.model.indices.instances import InstanceListExtractor
from i13c.cli.semantic.model.indices.resolutions import (
    CallSiteResolutionListExtractor,
    InstructionResolutionListExtractor,
)
from i13c.cli.semantic.model.indices.terminalities import TerminalityListExtractor
from i13c.cli.semantic.model.indices.variables import ParameterVariablesListExtractor

INDICES: Dict[str, AbstractListExtractor[Any]] = {
    "indices/controlflow-by-function": ControlFlowListExtractor,
    "indices/dataflow-by-flownode": DataFlowListExtractor,
    "indices/instance-by-callsite": InstanceListExtractor,
    "indices/resolution-by-callsite": CallSiteResolutionListExtractor,
    "indices/resolution-by-instruction": InstructionResolutionListExtractor,
    "indices/variables-by-parameter": ParameterVariablesListExtractor,
    "indices/terminality-by-function": TerminalityListExtractor,
}
