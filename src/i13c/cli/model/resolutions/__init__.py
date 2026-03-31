from typing import Any, Dict

from i13c.cli.model.abstract import AbstractListExtractor
from i13c.cli.model.resolutions.callsites import (
    AcceptedCallSiteResolutionListExtractor,
    BindingsOfCallSiteResolutionListExtractor,
    CallSiteResolutionListExtractor,
)
from i13c.cli.model.resolutions.instructions import InstructionResolutionListExtractor
from i13c.cli.model.resolutions.values import ValueResolutionListExtractor

RESOLUTIONS: Dict[str, AbstractListExtractor[Any]] = {
    "resolutions/callsites": CallSiteResolutionListExtractor,
    "resolutions/callsites/accepted": AcceptedCallSiteResolutionListExtractor,
    "resolutions/callsites/accepted/bindings": BindingsOfCallSiteResolutionListExtractor,
    "resolutions/instructions": InstructionResolutionListExtractor,
    "resolutions/values": ValueResolutionListExtractor,
}
