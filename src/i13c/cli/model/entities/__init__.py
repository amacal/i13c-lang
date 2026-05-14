from typing import Any, Dict

from i13c.cli.model.abstract import AbstractListExtractor
from i13c.cli.model.entities.callsites import CallSiteListExtractor
from i13c.cli.model.entities.expressions import ExpressionListExtractor
from i13c.cli.model.entities.functions import FunctionListExtractor
from i13c.cli.model.entities.instructions import InstructionListExtractor
from i13c.cli.model.entities.literals import LiteralListExtractor
from i13c.cli.model.entities.operands import OperandListExtractor
from i13c.cli.model.entities.parameters import ParameterListExtractor
from i13c.cli.model.entities.values import ValueListExtractor

ENTITIES: Dict[str, AbstractListExtractor[Any]] = {
    "entities/callsites": CallSiteListExtractor,
    "entities/expressions": ExpressionListExtractor,
    "entities/functions": FunctionListExtractor,
    "entities/instructions": InstructionListExtractor,
    "entities/literals": LiteralListExtractor,
    "entities/operands": OperandListExtractor,
    "entities/parameters": ParameterListExtractor,
    "entities/values": ValueListExtractor,
}
