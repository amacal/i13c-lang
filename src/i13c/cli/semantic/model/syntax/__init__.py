from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.syntax.functions import FunctionListExtractor

SYNTAX: Dict[str, AbstractListExtractor[Any]] = {
    "syntax/functions": FunctionListExtractor,
}
