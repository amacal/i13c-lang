from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.rules.summary import SummaryListExtractor

RULES: Dict[str, AbstractListExtractor[Any]] = {
    "rules/semantic": SummaryListExtractor(),
}
