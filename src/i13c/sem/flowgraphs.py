from dataclasses import dataclass
from typing import Dict, List, Union

from i13c.sem.function import Function, FunctionId, Statement


@dataclass(kw_only=True, frozen=True)
class FlowEntry:
    pass


@dataclass(kw_only=True, frozen=True)
class FlowExit:
    pass


FlowNode = Union[FlowEntry, FlowExit, Statement]


@dataclass(kw_only=True)
class FlowGraph:
    entry: FlowEntry
    exit: FlowExit
    edges: Dict[FlowNode, List[FlowNode]]


def build_flowgraphs(
    functions: Dict[FunctionId, Function],
) -> Dict[FunctionId, FlowGraph]:

    flowgraphs: Dict[FunctionId, FlowGraph] = {}

    for fid, function in functions.items():
        entry, exit = FlowEntry(), FlowExit()
        edges: Dict[FlowNode, List[FlowNode]] = {}

        if not function.statements:
            edges[entry] = [exit]

        else:

            stmts = function.statements
            edges[entry] = [stmts[0]]

            for predecessor, successor in zip(stmts, stmts[1:]):
                edges.setdefault(predecessor, []).append(successor)

            edges[stmts[-1]] = [exit]

        flowgraphs[fid] = FlowGraph(
            entry=entry,
            exit=exit,
            edges=edges,
        )

    return flowgraphs
