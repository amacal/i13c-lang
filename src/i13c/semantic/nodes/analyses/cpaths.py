from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cpaths import ControlPaths
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance


def configure_control_paths() -> GraphNode:
    return GraphNode(
        builder=build_control_paths,
        constraint=None,
        produces=("analyses/cpaths",),
        requires=frozenset({("cflows", "resolutions/cflows/accepted")}),
    )


def build_control_paths(
    cflows: OneToOne[FunctionId, ControlFlowAcceptance],
) -> OneToOne[FunctionId, ControlPaths]:
    cpaths: Dict[FunctionId, ControlPaths] = {}

    for fid, entry in cflows.items():
        cpaths[fid] = ControlPaths(
            flows=entry,
            paths=analyze_flows(entry),
        )

    return OneToOne[FunctionId, ControlPaths].instance(cpaths)


def analyze_flows(flows: ControlFlowAcceptance) -> List[List[int]]:
    stack: List[List[int]] = [[flows.source.entry]]
    paths: List[List[int]] = []

    while stack:
        path = stack.pop()
        node = path[-1]

        while True:
            if forward := flows.source.forward.get(node, []):
                if len(forward) > 1:
                    for target in forward[1:]:
                        stack.append(path + [target])

                # dispatch next iteration
                path.append(forward[0])
                node = forward[0]

            if len(forward) == 0 or node == flows.source.exit:
                paths.append(path)
                break

    return paths
