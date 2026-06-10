from typing import Any, Dict

from i13c.core.graph import GraphGroup
from i13c.semantic.nodes.analyses.asmlets import configure_asmlets
from i13c.semantic.nodes.analyses.callings import configure_callings
from i13c.semantic.nodes.analyses.cflows import configure_control_flows
from i13c.semantic.nodes.analyses.cgraphs import configure_call_graphs
from i13c.semantic.nodes.analyses.cpaths import configure_control_paths
from i13c.semantic.nodes.analyses.entrypoints import configure_entrypoints
from i13c.semantic.nodes.analyses.noreturns import configure_noreturns
from i13c.semantic.typing.analyses.core import AnalysisNodes


def configure_analyses() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_asmlets(),
            configure_call_graphs(),
            configure_callings(),
            configure_control_flows(),
            configure_control_paths(),
            configure_entrypoints(),
            configure_noreturns(),
        ]
    )


def parse_analyses(analyses: Dict[str, Any]) -> AnalysisNodes:
    return AnalysisNodes(
        asmlets=analyses.get("analyses/asmlets"),
        callings=analyses.get("analyses/callings"),
        cflows=analyses["analyses/cflows"],
        cgraphs=analyses.get("analyses/cgraphs"),
        cpaths=analyses.get("analyses/cpaths"),
        entrypoints=analyses.get("analyses/entrypoints"),
        noreturns=analyses.get("analyses/noreturns"),
    )
