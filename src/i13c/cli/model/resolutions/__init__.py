from typing import Any, Dict

from i13c.cli.model.abstract import AbstractListExtractor
from i13c.cli.model.resolutions.values import ValueResolutionListExtractor

RESOLUTIONS: Dict[str, AbstractListExtractor[Any]] = {
    "resolutions/values": ValueResolutionListExtractor,
}
