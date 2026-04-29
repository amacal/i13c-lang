from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.entities import configure_entities
from i13c.semantic.nodes.indices.asmlets import configure_asmlets_by_signatures
from i13c.semantic.nodes.indices.binds import configure_binds_by_parameters
from i13c.semantic.nodes.indices.callsites import configure_callsites_by_signatures
from i13c.semantic.nodes.indices.controlflows import configure_flowgraph_by_function
from i13c.semantic.nodes.indices.dataflows import configure_dataflow_by_flownode
from i13c.semantic.nodes.indices.entrypoints import configure_entrypoint_by_callable
from i13c.semantic.nodes.indices.environments import (
    configure_environment_by_flownode,
    configure_environments_by_snippets,
)
from i13c.semantic.nodes.indices.instances import configure_instance_by_callsite
from i13c.semantic.nodes.indices.signatures import configure_signatures_by_names
from i13c.semantic.nodes.indices.terminalities import configure_terminality_by_function
from i13c.semantic.nodes.indices.usages import configure_usages_by_expression
from i13c.semantic.nodes.indices.values import configure_values_by_statements
from i13c.semantic.nodes.indices.variables import configure_variables_by_parameters
from i13c.semantic.nodes.resolutions import configure_resolutions


def configure_nodes() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_asmlets_by_signatures(),
            configure_binds_by_parameters(),
            configure_callsites_by_signatures(),
            configure_dataflow_by_flownode(),
            configure_entities(),
            configure_entrypoint_by_callable(),
            configure_environment_by_flownode(),
            configure_environments_by_snippets(),
            configure_flowgraph_by_function(),
            configure_instance_by_callsite(),
            configure_resolutions(),
            configure_signatures_by_names(),
            configure_values_by_statements(),
            configure_terminality_by_function(),
            configure_usages_by_expression(),
            configure_variables_by_parameters(),
        ]
    )
