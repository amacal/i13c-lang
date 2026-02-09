from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, FrozenSet, Iterable, List, Set, Tuple, Union


@dataclass(kw_only=True, frozen=True)
class Prefix:
    value: str

    def find(self, nodes: Iterable[str]) -> Set[str]:
        return {node for node in nodes if node.startswith(self.value)}


GraphBuilder = Callable[..., Any]
Requirement = FrozenSet[Tuple[str, Union[str, Prefix]]]


@dataclass(kw_only=True, frozen=True)
class GraphNode:
    builder: GraphBuilder
    produces: Tuple[str, ...]
    requires: Requirement


@dataclass(kw_only=True, frozen=True)
class GraphGroup:
    nodes: List[Union[GraphNode, GraphGroup]]

    def flatten(self) -> List[GraphNode]:
        out: List[GraphNode] = []

        for node in self.nodes:
            if isinstance(node, GraphGroup):
                out.extend(node.flatten())
            else:
                out.append(node)

        return out


def reorder_configurations(nodes: List[GraphNode]) -> List[GraphNode]:
    # build producer map
    producer: Dict[str, GraphNode] = {}

    for node in nodes:
        for product in node.produces:
            producer[product] = node

    # build dependency graph
    edges: Dict[GraphNode, List[GraphNode]] = defaultdict(list)
    indeg: Dict[GraphNode, int] = {node: 0 for node in nodes}

    for node in nodes:
        for _, req in node.requires:
            # make sure all requirements are some keys
            if isinstance(req, Prefix):
                reqs = list(req.find(producer.keys()))
            else:
                reqs = [req]

            # now make dependencies
            for item in reqs:
                dep = producer[item]
                edges[dep].append(node)
                indeg[node] += 1

    # topological sorting
    queue = [node for node in nodes if indeg[node] == 0]
    out: List[GraphNode] = []

    while queue:
        c = queue.pop()
        out.append(c)

        for nxt in edges[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)

    return out


def evaluate(nodes: List[GraphNode], initial: Dict[str, Any]) -> Dict[str, Any]:
    artifacts: Dict[str, Any] = {}

    # seed initial artifacts
    for key, value in initial.items():
        nodes.append(
            GraphNode(
                builder=(lambda: value),
                produces=(key,),
                requires=frozenset(),
            )
        )

    def expand(req: Union[str, Prefix]) -> Any:
        if isinstance(req, Prefix):
            return {key: artifacts[key] for key in req.find(artifacts.keys())}
        else:
            return artifacts[req]

    for node in reorder_configurations(nodes):
        # prepare arguments
        args = {name: expand(req) for name, req in node.requires}

        # build dataset
        dataset = node.builder(**args)

        # store single artifact
        for producer in node.produces:
            artifacts[producer] = dataset

        # store multiple artifacts
        if len(node.produces) > 1:
            for idx, producer in enumerate(node.produces):
                artifacts[producer] = dataset[idx]

    return artifacts
