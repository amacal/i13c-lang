from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.entities.bindings import configure_bindings
from i13c.semantic.nodes.entities.binds import configure_binds
from i13c.semantic.nodes.entities.callsites import configure_callsites
from i13c.semantic.nodes.entities.expressions import configure_expressions
from i13c.semantic.nodes.entities.functions import configure_functions
from i13c.semantic.nodes.entities.instructions import configure_instructions
from i13c.semantic.nodes.entities.literals import configure_literals
from i13c.semantic.nodes.entities.operands import configure_operands
from i13c.semantic.nodes.entities.parameters import configure_parameters
from i13c.semantic.nodes.entities.ranges import configure_ranges
from i13c.semantic.nodes.entities.slots import configure_slots
from i13c.semantic.nodes.entities.snippets import configure_snippets
from i13c.semantic.nodes.entities.types import configure_types
from i13c.semantic.nodes.entities.values import configure_values


def configure_entities() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_binds(),
            configure_bindings(),
            configure_callsites(),
            configure_expressions(),
            configure_functions(),
            configure_instructions(),
            configure_literals(),
            configure_operands(),
            configure_parameters(),
            configure_ranges(),
            configure_snippets(),
            configure_slots(),
            configure_types(),
            configure_values(),
        ]
    )
