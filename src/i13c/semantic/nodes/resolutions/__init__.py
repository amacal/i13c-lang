from typing import Any, Dict

from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.resolutions.addresses import configure_address_resolution
from i13c.semantic.nodes.resolutions.assigns import configure_assign_resolution
from i13c.semantic.nodes.resolutions.bindings import configure_binding_resolution
from i13c.semantic.nodes.resolutions.binds import configure_bind_resolution
from i13c.semantic.nodes.resolutions.callsites import configure_callsite_resolution
from i13c.semantic.nodes.resolutions.cflows import configure_control_flow_resolution
from i13c.semantic.nodes.resolutions.environments import (
    configure_environment_resolution,
)
from i13c.semantic.nodes.resolutions.expressions import configure_expression_resolution
from i13c.semantic.nodes.resolutions.flags import configure_flags_resolution
from i13c.semantic.nodes.resolutions.immediates import configure_immediate_resolution
from i13c.semantic.nodes.resolutions.instructions import (
    configure_instruction_resolution,
)
from i13c.semantic.nodes.resolutions.labels import configure_label_resolution
from i13c.semantic.nodes.resolutions.literals import configure_literal_resolution
from i13c.semantic.nodes.resolutions.mnemonics import configure_mnemonic_resolution
from i13c.semantic.nodes.resolutions.operands import configure_operand_resolution
from i13c.semantic.nodes.resolutions.parameters import configure_parameter_resolution
from i13c.semantic.nodes.resolutions.ranges import configure_range_resolution
from i13c.semantic.nodes.resolutions.references import configure_reference_resolution
from i13c.semantic.nodes.resolutions.registers import configure_register_resolution
from i13c.semantic.nodes.resolutions.signatures import configure_signature_resolution
from i13c.semantic.nodes.resolutions.snippets import configure_snippet_resolution
from i13c.semantic.nodes.resolutions.types import configure_type_resolution
from i13c.semantic.nodes.resolutions.values import configure_value_resolution
from i13c.semantic.typing.resolutions import ResolutionNodes


def configure_resolutions() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_address_resolution(),
            configure_assign_resolution(),
            configure_bind_resolution(),
            configure_binding_resolution(),
            configure_callsite_resolution(),
            configure_control_flow_resolution(),
            configure_environment_resolution(),
            configure_expression_resolution(),
            configure_flags_resolution(),
            configure_immediate_resolution(),
            configure_instruction_resolution(),
            configure_label_resolution(),
            configure_literal_resolution(),
            configure_mnemonic_resolution(),
            configure_operand_resolution(),
            configure_parameter_resolution(),
            configure_range_resolution(),
            configure_reference_resolution(),
            configure_register_resolution(),
            configure_signature_resolution(),
            configure_snippet_resolution(),
            configure_type_resolution(),
            configure_value_resolution(),
        ]
    )


def parse_resolutions(resolutions: Dict[str, Any]) -> ResolutionNodes:
    return ResolutionNodes(
        assigns=resolutions.get("resolutions/assigns"),
        addresses=resolutions.get("resolutions/addresses"),
        bindings=resolutions.get("resolutions/bindings"),
        binds=resolutions.get("resolutions/binds"),
        callsites=resolutions.get("resolutions/callsites"),
        cflows=resolutions.get("resolutions/cflows"),
        environments=resolutions.get("resolutions/environments"),
        expressions=resolutions.get("resolutions/expressions"),
        flags=resolutions.get("resolutions/flags"),
        immediates=resolutions.get("resolutions/immediates"),
        instructions=resolutions.get("resolutions/instructions"),
        labels=resolutions.get("resolutions/labels"),
        literals=resolutions.get("resolutions/literals"),
        mnemonics=resolutions.get("resolutions/mnemonics"),
        operands=resolutions.get("resolutions/operands"),
        ranges=resolutions.get("resolutions/ranges"),
        references=resolutions.get("resolutions/references"),
        registers=resolutions.get("resolutions/registers"),
        signatures=resolutions.get("resolutions/signatures"),
        parameters=resolutions.get("resolutions/parameters"),
        snippets=resolutions.get("resolutions/snippets"),
        types=resolutions.get("resolutions/types"),
        values=resolutions.get("resolutions/values"),
    )
