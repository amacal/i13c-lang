from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Union

from i13c.sem.typing.entities.functions import Statement


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

    def nodes(self) -> Set[FlowNode]:
        values = (next for edge in self.edges.values() for next in edge)
        nodes = set(self.edges.keys()) | set(values)

        return nodes

    def describe(self) -> str:
        # compute unique nodes
        nodes = self.nodes()

        # count number of edges
        edges = sum(len(v) for v in self.edges.values())
        return f"nodes={len(nodes)}, edges={edges}"

    def show(self) -> Iterable[str]:
        path: List[str] = []
        node: Optional[FlowNode] = self.entry

        # simplified path traversal
        while node is not None:
            path.append(node.identify(2))
            node = self.edges[node][0] if node in self.edges else None

        return path
