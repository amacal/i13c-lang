from typing import Any

from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.analyses.allocations import configure_allocations
from i13c.semantic.nodes.analyses.asmlets import configure_asmlets
from i13c.semantic.nodes.analyses.callings import configure_callings
from i13c.semantic.nodes.analyses.cflows import configure_control_flows
from i13c.semantic.nodes.analyses.cgraphs import configure_call_graphs
from i13c.semantic.nodes.analyses.cpaths import configure_control_paths
from i13c.semantic.nodes.analyses.dflows import configure_data_flows
from i13c.semantic.nodes.analyses.entrypoints import configure_entrypoints
from i13c.semantic.nodes.analyses.liveness import configure_liveness
from i13c.semantic.nodes.analyses.noreturns import configure_noreturns
from i13c.semantic.typing.analyses.core import AnalysisNodes


def configure_analyses() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_allocations(),
            configure_asmlets(),
            configure_call_graphs(),
            configure_callings(),
            configure_control_flows(),
            configure_control_paths(),
            configure_data_flows(),
            configure_entrypoints(),
            configure_liveness(),
            configure_noreturns(),
        ]
    )


def parse_analyses(analyses: dict[str, Any]) -> AnalysisNodes:
    return AnalysisNodes(
        allocations=analyses.get("analyses/allocations"),
        asmlets=analyses.get("analyses/asmlets"),
        callings=analyses.get("analyses/callings"),
        cflows=analyses["analyses/cflows"],
        cgraphs=analyses.get("analyses/cgraphs"),
        cpaths=analyses.get("analyses/cpaths"),
        dflows=analyses.get("analyses/dflows"),
        entrypoints=analyses.get("analyses/entrypoints"),
        liveness=analyses.get("analyses/liveness"),
        noreturns=analyses.get("analyses/noreturns"),
    )
