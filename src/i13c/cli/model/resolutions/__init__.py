from typing import Any, Dict

from i13c.cli.model.abstract import AbstractListExtractor
from i13c.cli.model.resolutions.instructions import InstructionResolutionListExtractor

RESOLUTIONS: Dict[str, AbstractListExtractor[Any]] = {
    "resolutions/instructions": InstructionResolutionListExtractor,
}
