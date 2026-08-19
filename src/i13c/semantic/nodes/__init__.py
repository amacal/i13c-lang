from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.analyses.core import configure_analyses
from i13c.semantic.nodes.entities import configure_entities
from i13c.semantic.nodes.indices import configure_indices
from i13c.semantic.nodes.resolutions import configure_resolutions


def configure_nodes() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_entities(),
            configure_analyses(),
            configure_indices(),
            configure_resolutions(),
        ]
    )
