from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.syntax.expressions import ExpressionListExtractor
from i13c.cli.semantic.model.syntax.functions import FunctionListExtractor
from i13c.cli.semantic.model.syntax.instructions import InstructionListExtractor
from i13c.cli.semantic.model.syntax.literals import (
    LiteralIntegersListExtractor,
    LiteralListExtractor,
)
from i13c.cli.semantic.model.syntax.operands import OperandListExtractor
from i13c.cli.semantic.model.syntax.parameters import ParameterListExtractor
from i13c.cli.semantic.model.syntax.snippets import SnippetListExtractor
from i13c.cli.semantic.model.syntax.statements import (
    StatementCallsListExtractor,
    StatementListExtractor,
)

SYNTAX: Dict[str, AbstractListExtractor[Any]] = {
    "syntax/expressions": ExpressionListExtractor,
    "syntax/functions": FunctionListExtractor,
    "syntax/instructions": InstructionListExtractor,
    "syntax/literals": LiteralListExtractor,
    "syntax/literals/integers": LiteralIntegersListExtractor,
    "syntax/operands": OperandListExtractor,
    "syntax/parameters": ParameterListExtractor,
    "syntax/snippets": SnippetListExtractor,
    "syntax/statements": StatementListExtractor,
    "syntax/statements/calls": StatementCallsListExtractor,
}
