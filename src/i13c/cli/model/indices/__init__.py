from typing import Any, Dict

from i13c.cli.model.abstract import AbstractListExtractor
from i13c.cli.model.indices.instances import InstanceListExtractor
from i13c.cli.model.indices.usages import UsagesByExpressionListExtractor
from i13c.cli.model.indices.variables import ParameterVariablesListExtractor

INDICES: Dict[str, AbstractListExtractor[Any]] = {
    "indices/instance-by-callsite": InstanceListExtractor,
    "indices/usages-by-expression": UsagesByExpressionListExtractor,
    "indices/variables-by-source": ParameterVariablesListExtractor,
}
