from dataclasses import dataclass
from typing import Dict, List, Union, Iterable

from i13c.sem.function import Function, FunctionId, Statement


@dataclass(kw_only=True, frozen=True)
class FlowEntry:
    def identify(self, length: int) -> str:
        return "entry"


@dataclass(kw_only=True, frozen=True)
class FlowExit:
    def identify(self, length: int) -> str:
        return "exit"


FlowNode = Union[FlowEntry, FlowExit, Statement]


@dataclass(kw_only=True)
class FlowGraph:
    entry: FlowEntry
    exit: FlowExit
    edges: Dict[FlowNode, List[FlowNode]]

    def describe(self) -> str:
        # compute unique nodes
        values = (next for edge in self.edges.values() for next in edge)
        nodes = set(self.edges.keys()) | set(values)

        # count number of edges
        edges = sum(len(v) for v in self.edges.values())
        return f"nodes={len(nodes)}, edges={edges}"

    def show(self) -> Iterable[str]:
        path: List[str] = []
        node: FlowNode = self.entry

        # simplified path traversal
        while node != self.exit:
            path.append(node.identify(2))
            node = self.edges[node][0]

        return path


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
                edges[predecessor] = [successor]

            edges[stmts[-1]] = [exit]

        flowgraphs[fid] = FlowGraph(
            entry=entry,
            exit=exit,
            edges=edges,
        )

    return flowgraphs
