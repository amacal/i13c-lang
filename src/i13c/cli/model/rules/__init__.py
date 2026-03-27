from typing import Any, Dict

from i13c.cli.model.abstract import AbstractListExtractor
from i13c.cli.model.rules.semantic import SemanticListExtractor

RULES: Dict[str, AbstractListExtractor[Any]] = {
    "rules/semantic": SemanticListExtractor(),
}
