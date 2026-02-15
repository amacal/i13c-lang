from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.rules.semantic import SemanticListExtractor

RULES: Dict[str, AbstractListExtractor[Any]] = {
    "rules/semantic": SemanticListExtractor(),
}
