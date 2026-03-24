from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.entities.bindings import BindingsListExtractor
from i13c.cli.semantic.model.entities.callsites import CallSiteListExtractor
from i13c.cli.semantic.model.entities.expressions import ExpressionListExtractor
from i13c.cli.semantic.model.entities.functions import FunctionListExtractor
from i13c.cli.semantic.model.entities.instructions import InstructionListExtractor
from i13c.cli.semantic.model.entities.literals import LiteralListExtractor
from i13c.cli.semantic.model.entities.operands import OperandListExtractor
from i13c.cli.semantic.model.entities.parameters import ParameterListExtractor
from i13c.cli.semantic.model.entities.snippets import SnippetListExtractor
from i13c.cli.semantic.model.entities.values import ValueListExtractor
from i13c.cli.semantic.model.entities.variables import VariableListExtractor

ENTITIES: Dict[str, AbstractListExtractor[Any]] = {
    "entities/bindings": BindingsListExtractor,
    "entities/callsites": CallSiteListExtractor,
    "entities/expressions": ExpressionListExtractor,
    "entities/functions": FunctionListExtractor,
    "entities/instructions": InstructionListExtractor,
    "entities/literals": LiteralListExtractor,
    "entities/operands": OperandListExtractor,
    "entities/parameters": ParameterListExtractor,
    "entities/snippets": SnippetListExtractor,
    "entities/values": ValueListExtractor,
    "entities/variables": VariableListExtractor,
}
