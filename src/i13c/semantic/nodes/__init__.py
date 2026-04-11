from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.analyses.callables import configure_callables_live
from i13c.semantic.nodes.analyses.callgraphs import configure_callgraphs_live
from i13c.semantic.nodes.analyses.controlflows import configure_flowgraphs_live
from i13c.semantic.nodes.entities import configure_entities
from i13c.semantic.nodes.indices.callgraphs import configure_callgraphs
from i13c.semantic.nodes.indices.controlflows import configure_flowgraph_by_function
from i13c.semantic.nodes.indices.dataflows import configure_dataflow_by_flownode
from i13c.semantic.nodes.indices.entrypoints import configure_entrypoint_by_callable
from i13c.semantic.nodes.indices.environments import configure_environment_by_flownode
from i13c.semantic.nodes.indices.instances import configure_instance_by_callsite
from i13c.semantic.nodes.indices.terminalities import configure_terminality_by_function
from i13c.semantic.nodes.indices.usages import configure_usages_by_expression
from i13c.semantic.nodes.indices.variables import configure_variables_by_parameters
from i13c.semantic.nodes.resolutions.binds import configure_bind_resolution
from i13c.semantic.nodes.resolutions.callsites import configure_resolution_by_callsite
from i13c.semantic.nodes.resolutions.instructions import (
    configure_resolution_by_instruction,
)
from i13c.semantic.nodes.resolutions.ranges import configure_range_resolution
from i13c.semantic.nodes.resolutions.types import configure_type_resolution
from i13c.semantic.nodes.resolutions.values import configure_resolution_by_value


def configure_nodes() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_entities(),
            configure_bind_resolution(),
            configure_callables_live(),
            configure_callgraphs_live(),
            configure_callgraphs(),
            configure_dataflow_by_flownode(),
            configure_entrypoint_by_callable(),
            configure_environment_by_flownode(),
            configure_flowgraph_by_function(),
            configure_flowgraphs_live(),
            configure_instance_by_callsite(),
            configure_range_resolution(),
            configure_resolution_by_callsite(),
            configure_resolution_by_instruction(),
            configure_resolution_by_value(),
            configure_terminality_by_function(),
            configure_type_resolution(),
            configure_usages_by_expression(),
            configure_variables_by_parameters(),
        ]
    )
