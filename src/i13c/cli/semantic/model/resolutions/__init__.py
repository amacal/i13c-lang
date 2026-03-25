from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.resolutions.values import ValueResolutionListExtractor

RESOLUTIONS: Dict[str, AbstractListExtractor[Any]] = {
    "resolutions/values": ValueResolutionListExtractor,
}
