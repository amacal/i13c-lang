from typing import Any, Dict

from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.resolutions.binds import configure_bind_resolution
from i13c.semantic.nodes.resolutions.callsites import configure_resolution_by_callsite
from i13c.semantic.nodes.resolutions.instructions import (
    configure_resolution_by_instruction,
)
from i13c.semantic.nodes.resolutions.ranges import configure_range_resolution
from i13c.semantic.nodes.resolutions.signatures import configure_signature_resolution
from i13c.semantic.nodes.resolutions.slots import configure_slot_resolution
from i13c.semantic.nodes.resolutions.types import configure_type_resolution
from i13c.semantic.nodes.resolutions.values import configure_resolution_by_value
from i13c.semantic.typing.resolutions import ResolutionNodes


def configure_resolutions() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_bind_resolution(),
            configure_range_resolution(),
            configure_resolution_by_callsite(),
            configure_resolution_by_instruction(),
            configure_resolution_by_value(),
            configure_signature_resolution(),
            configure_slot_resolution(),
            configure_type_resolution(),
        ]
    )

def parse_resolutions(resolutions: Dict[str, Any]) -> ResolutionNodes:
    return ResolutionNodes(
            binds=resolutions.get("resolutions/binds"),
            ranges=resolutions.get("resolutions/ranges"),
            signatures=resolutions.get("resolutions/signatures"),
            slots=resolutions.get("resolutions/slots"),
            types=resolutions.get("resolutions/types"),
        )
