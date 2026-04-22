from typing import Any, Dict

from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.entities.addresses import configure_addresses
from i13c.semantic.nodes.entities.bindings import configure_bindings
from i13c.semantic.nodes.entities.binds import configure_binds
from i13c.semantic.nodes.entities.callsites import configure_callsites
from i13c.semantic.nodes.entities.cflows import configure_control_flows
from i13c.semantic.nodes.entities.environments import configure_environments
from i13c.semantic.nodes.entities.expressions import configure_expressions
from i13c.semantic.nodes.entities.flags import configure_flags
from i13c.semantic.nodes.entities.functions import configure_functions
from i13c.semantic.nodes.entities.immediates import configure_immediates
from i13c.semantic.nodes.entities.instructions import configure_instructions
from i13c.semantic.nodes.entities.labels import configure_labels
from i13c.semantic.nodes.entities.literals import configure_literals
from i13c.semantic.nodes.entities.mnemonics import configure_mnemonics
from i13c.semantic.nodes.entities.operands import configure_operands
from i13c.semantic.nodes.entities.parameters import configure_parameters
from i13c.semantic.nodes.entities.ranges import configure_ranges
from i13c.semantic.nodes.entities.references import configure_references
from i13c.semantic.nodes.entities.registers import configure_registers
from i13c.semantic.nodes.entities.signatures import configure_signatures
from i13c.semantic.nodes.entities.snippets import configure_snippets
from i13c.semantic.nodes.entities.types import configure_types
from i13c.semantic.nodes.entities.values import configure_values
from i13c.semantic.typing.entities import EntityNodes


def configure_entities() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_addresses(),
            configure_binds(),
            configure_bindings(),
            configure_callsites(),
            configure_control_flows(),
            configure_environments(),
            configure_expressions(),
            configure_flags(),
            configure_functions(),
            configure_immediates(),
            configure_instructions(),
            configure_labels(),
            configure_literals(),
            configure_mnemonics(),
            configure_operands(),
            configure_parameters(),
            configure_ranges(),
            configure_references(),
            configure_registers(),
            configure_snippets(),
            configure_signatures(),
            configure_types(),
            configure_values(),
        ]
    )


def parse_entities(entities: Dict[str, Any]) -> EntityNodes:
    return EntityNodes(
        addresses=entities["entities/addresses"],
        binds=entities["entities/binds"],
        callsites=entities["entities/callsites"],
        cflows=entities["entities/cflows"],
        environments=entities["entities/environments"],
        expressions=entities["entities/expressions"],
        flags=entities["entities/flags"],
        functions=entities["entities/functions"],
        immediates=entities["entities/immediates"],
        instructions=entities["entities/instructions"],
        labels=entities["entities/labels"],
        literals=entities["entities/literals"],
        mnemonics=entities["entities/mnemonics"],
        operands=entities["entities/operands"],
        parameters=entities["entities/parameters"],
        ranges=entities["entities/ranges"],
        references=entities["entities/references"],
        registers=entities["entities/registers"],
        signatures=entities["entities/signatures"],
        snippets=entities["entities/snippets"],
        types=entities["entities/types"],
        usages=entities["entities/usages"],
        values=entities["entities/values"],
        variables=entities["entities/variables"],
    )
