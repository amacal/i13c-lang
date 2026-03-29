from collections import defaultdict
from dataclasses import dataclass
from logging import Logger, getLogger
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


class CyclicDependencyError(Exception):
    def __init__(self) -> None:
        super().__init__("graph contains cyclic dependencies")


class MissingPrefixProducerError(Exception):
    def __init__(self, prefix: Prefix) -> None:
        self.prefix = prefix
        super().__init__(f"no producer found for prefix {prefix.value}")


class MissingArtifactProducerError(Exception):
    def __init__(self, node: GraphNode, artifact: str) -> None:
        self.node = node
        self.artifact = artifact
        super().__init__(f"no producer found for artifact {artifact}")


class DuplicateArtifactError(Exception):
    def __init__(self, artifact: str, producers: List[GraphNode]) -> None:
        self.artifact = artifact
        self.producers = producers
        super().__init__(f"artifact {artifact} has multiple producers")


class InvalidDatasetArityError(Exception):
    def __init__(self, node: GraphNode, expected: int, actual: int) -> None:
        self.node = node
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"builder for node producing {expected} artifacts returned {actual} values"
        )


@dataclass(kw_only=True, frozen=True)
class Prefix:
    value: str

    def find(self, nodes: Iterable[str]) -> Set[str]:
        return {node for node in nodes if node.startswith(self.value)}


GraphBuilder = Callable[..., Union[Any, Tuple[Any, ...]]]
GraphConstraint = Optional[Callable[..., bool]]
Requirement = FrozenSet[Tuple[str, Union[str, Prefix]]]


@dataclass(kw_only=True, frozen=True)
class GraphNode:
    builder: GraphBuilder
    constraint: GraphConstraint
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

            # check if product already has a producer, if so raise error
            if product in producer:
                raise DuplicateArtifactError(product, [producer[product], node])

            producer[product] = node

    # build dependency graph
    edges: Dict[GraphNode, List[GraphNode]] = defaultdict(list)
    indeg: Dict[GraphNode, int] = {node: 0 for node in nodes}

    for node in nodes:
        for _, req in node.requires:
            # make sure all requirements are some keys
            if isinstance(req, Prefix):
                reqs = list(req.find(producer.keys()))

                if not reqs:
                    raise MissingPrefixProducerError(req)
            else:
                reqs = [req]

            # now make dependencies
            for item in reqs:
                # make sure all requirements are produced by some node
                if item not in producer:
                    raise MissingArtifactProducerError(node, item)

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

    # diff length of output with input means there is a cycle in the graph
    if len(out) != len(nodes):
        raise CyclicDependencyError()

    return out


def evaluate(nodes: List[GraphNode], initial: Dict[str, Any]) -> Dict[str, Any]:
    artifacts: Dict[str, Any] = {}
    logger: Logger = getLogger("dag")

    def seed(value: Any) -> Callable[[], Any]:
        return lambda: value

    # make copy to avoid mutating input list`
    nodes = list(nodes)

    # seed initial artifacts
    for key, value in initial.items():
        nodes.append(
            GraphNode(
                builder=seed(value),
                constraint=None,
                produces=(key,),
                requires=frozenset(),
            )
        )

    def expand(req: Union[str, Prefix]) -> Optional[Any]:
        if isinstance(req, Prefix):
            return {key: artifacts[key] for key in req.find(artifacts.keys())} or None
        else:
            return artifacts.get(req, None)

    for node in reorder_configurations(nodes):
        for target in node.produces:
            logger.info(f"producing {target} ...")

        # prepare arguments
        args = {name: expand(req) for name, req in node.requires}
        ready = all(arg is not None for arg in args.values())

        # optionally build dataset
        if ready and (not node.constraint or node.constraint(**args)):
            dataset = node.builder(**args)

            if not isinstance(dataset, tuple):
               dataset = (dataset,)
            else:
               dataset = tuple(dataset) # type: ignore

            if len(dataset) != len(node.produces):
                raise InvalidDatasetArityError(
                    node=node,
                    expected=len(node.produces),
                    actual=len(dataset),
                )

            for idx, producer in enumerate(node.produces):
                artifacts[producer] = dataset[idx]

    return artifacts
