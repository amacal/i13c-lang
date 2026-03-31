from typing import Any, Dict

from i13c.cli.model.abstract import AbstractListExtractor
from i13c.cli.model.indices.controlflows import ControlFlowListExtractor
from i13c.cli.model.indices.dataflows import DataFlowListExtractor
from i13c.cli.model.indices.environments import EnvironmentListExtractor
from i13c.cli.model.indices.instances import InstanceListExtractor
from i13c.cli.model.indices.terminalities import TerminalityListExtractor
from i13c.cli.model.indices.usages import UsagesByExpressionListExtractor
from i13c.cli.model.indices.variables import ParameterVariablesListExtractor

INDICES: Dict[str, AbstractListExtractor[Any]] = {
    "indices/controlflow-by-function": ControlFlowListExtractor,
    "indices/dataflow-by-flownode": DataFlowListExtractor,
    "indices/environment-by-flownode": EnvironmentListExtractor,
    "indices/instance-by-callsite": InstanceListExtractor,
    "indices/terminality-by-function": TerminalityListExtractor,
    "indices/usages-by-expression": UsagesByExpressionListExtractor,
    "indices/variables-by-source": ParameterVariablesListExtractor,
}
