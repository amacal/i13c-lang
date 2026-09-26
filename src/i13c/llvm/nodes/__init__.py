from typing import Any

from i13c.core.graph import GraphGroup
from i13c.llvm.nodes.allocations import configure_allocations
from i13c.llvm.nodes.cflows import configure_control_flows
from i13c.llvm.nodes.dflows import configure_data_flows
from i13c.llvm.nodes.liveness import configure_liveness
from i13c.llvm.nodes.shuffles import configure_shuffles
from i13c.llvm.typing import LlvmNodes


def configure_llvm() -> GraphGroup:
    return GraphGroup(
    nodes=[
            configure_allocations(),
            configure_control_flows(),
            configure_data_flows(),
            configure_liveness(),
            configure_shuffles(),
        ]
    )


def parse_llvm(analyses: dict[str, Any]) -> LlvmNodes:
    return LlvmNodes(
        allocations=analyses.get("llvm/allocations"),
        cflows=analyses.get("llvm/cflows"),
        dflows=analyses.get("llvm/dflows"),
        liveness=analyses.get("llvm/liveness"),
        shuffles=analyses.get("llvm/shuffles"),
    )
