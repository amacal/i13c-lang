from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Union

from i13c.sem.typing.entities.functions import Statement


@dataclass(kw_only=True, frozen=True)
class FlowEntry:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("entry", f"{self.value:<{length}}"))


@dataclass(kw_only=True, frozen=True)
class FlowExit:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("exit", f"{self.value:<{length}}"))


FlowNode = Union[FlowEntry, FlowExit, Statement]


@dataclass(kw_only=True)
class FlowGraph:
    entry: FlowEntry
    exit: FlowExit

    forward: Dict[FlowNode, List[FlowNode]]
    backward: Dict[FlowNode, List[FlowNode]]

    def nodes(self) -> Set[FlowNode]:
        values = (next for edge in self.forward.values() for next in edge)
        nodes = set(self.forward.keys()) | set(values)

        return nodes

    def describe(self) -> str:
        # compute unique nodes
        nodes = self.nodes()

        # count number of edges
        forward = sum(len(v) for v in self.forward.values())
        backward = sum(len(v) for v in self.backward.values())

        return f"nodes={len(nodes)}, forward={forward}, backward={backward}"

    def show(self) -> Iterable[str]:
        path: List[str] = []
        node: Optional[FlowNode] = self.entry

        # simplified path traversal
        while node is not None:
            path.append(node.identify(2))
            node = self.forward[node][0] if node in self.forward else None

        return path
