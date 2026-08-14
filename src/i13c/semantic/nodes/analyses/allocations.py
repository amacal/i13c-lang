from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.allocations import Allocation
from i13c.semantic.typing.analyses.liveness import Liveness
from i13c.semantic.typing.entities.functions import FunctionId


def configure_allocations() -> GraphNode:
    return GraphNode(
        builder=build_allocations,
        constraint=None,
        produces=("analyses/allocations",),
        requires=frozenset(
            {
                ("liveness", "analyses/liveness"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_allocations(
    liveness: OneToOne[FunctionId, Liveness],
) -> OneToOne[FunctionId, Allocation]:
    allocations: dict[FunctionId, Allocation] = {}

    for fid, live in liveness.items():
        graph: dict[int, set[int]] = {}
        worklist: list[int] = []
        targets: set[int] = set()

        for idx in range(len(live.values)):
            graph[idx] = set()

        for idx in range(len(live.nodes)):
            values = live.live_in[idx].union(live.live_out[idx])
            pairs = [(a, b) for a in values for b in values if a != b]

            targets.update(values)

            for a, b in pairs:
                graph[a].add(b)
                graph[b].add(a)

        for idx in graph.keys() - targets:
            del graph[idx]

        spills: set[int] = set()
        colors: dict[int, int] = {}
        copy = {k: set(v) for k, v in graph.items()}

        while graph:
            broken = False

            for idx, edges in list(graph.items()):
                if len(edges) < 8:
                    worklist.append(idx)

                    for neighbor in graph[idx]:
                        graph[neighbor].remove(idx)

                    del graph[idx]
                    broken = True
                    break

            if not broken:
                for idx in list(graph.keys()):
                    spills.add(idx)

                    for neighbor in graph[idx]:
                        graph[neighbor].remove(idx)

                    del graph[idx]
                    break

        while worklist:
            node = worklist.pop()

            pallet = set(range(8))
            used = {colors[neighbor] for neighbor in copy[node] if neighbor in colors}

            available = pallet - used
            colors[node] = min(available)

        allocations[fid] = Allocation(
            ref=live.ref,
            target=fid,
            values=live.values,
            colors=colors,
        )

    return OneToOne[FunctionId, Allocation].instance(allocations)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Allocation]) -> None:
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, Allocation]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "values": "Values",
            "colors": "Colors",
        }

    @staticmethod
    def rows(key: FunctionId, entry: Allocation) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "values": str(len(entry.values)),
            "colors": str(len(entry.colors)),
        }
