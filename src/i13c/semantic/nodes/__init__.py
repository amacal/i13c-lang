from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.analyses import configure_analyses
from i13c.semantic.nodes.entities import configure_entities
from i13c.semantic.nodes.indices.asmlets import configure_asmlets_by_signatures
from i13c.semantic.nodes.indices.binds import configure_binds_by_parameters
from i13c.semantic.nodes.indices.callsites import (
    configure_callsites_by_signatures,
    configure_callsites_by_statements,
)
from i13c.semantic.nodes.indices.cflows import configure_control_flows_by_signatures
from i13c.semantic.nodes.indices.cpaths import configure_control_paths_by_signatures
from i13c.semantic.nodes.indices.environments import configure_environments_by_snippets
from i13c.semantic.nodes.indices.signatures import configure_signatures_by_names
from i13c.semantic.nodes.indices.values import configure_values_by_statements
from i13c.semantic.nodes.resolutions import configure_resolutions


def configure_nodes() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_asmlets_by_signatures(),
            configure_binds_by_parameters(),
            configure_callsites_by_signatures(),
            configure_callsites_by_statements(),
            configure_control_flows_by_signatures(),
            configure_control_paths_by_signatures(),
            configure_entities(),
            configure_analyses(),
            configure_environments_by_snippets(),
            configure_resolutions(),
            configure_signatures_by_names(),
            configure_values_by_statements(),
        ]
    )
