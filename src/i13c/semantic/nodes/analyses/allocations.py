from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.allocations import Allocation
from i13c.semantic.typing.analyses.callings import CallingClobber
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

    # fmt: off
    system_v: dict[bytes, int] = {
        b"rdi": 0, b"rsi": 1, b"rdx": 2, b"rcx": 3, b"r8": 4, b"r9": 5, b"r10": 6, b"r11": 7,
        b"rax": 8, b"rbx": 9, b"rbp": 10, b"r12": 11, b"r13": 12, b"r14": 13, b"r15": 14,
    }
    # fmt: on

    for fid, live in liveness.items():
        graph: dict[int, set[int]] = {}
        worklist: list[int] = []
        targets: set[int] = set()

        for idx in range(len(live.values)):
            graph[idx] = set()

        for idx in range(len(live.nodes)):
            values = live.live_in[idx].union(live.live_out[idx]).union(live.clobbers[idx])
            pairs = [(a, b) for a in values for b in values if a != b]

            targets.update(values)

            for a, b in pairs:
                graph[a].add(b)
                graph[b].add(a)

        for idx in graph.keys() - targets:
            del graph[idx]

        count = 0
        spills: dict[int, int] = {}
        colors: dict[int, int] = {}
        copy = {k: set(v) for k, v in graph.items()}

        for clobbers in live.clobbers.values():
            for idx in clobbers:
                if idx in graph:
                    # for neighbor in graph[idx]:
                    #     graph[neighbor].remove(idx)

                    # del graph[idx]
                    value = live.values[idx]
                    count = count + 1

                    assert isinstance(value, CallingClobber)
                    colors[idx] = system_v[value.name]

        while len(graph) > count:
            broken = False

            for idx, edges in list(graph.items()):
                if isinstance(live.values[idx], CallingClobber):
                    continue

                if len(edges) < len(system_v):
                    worklist.append(idx)

                    for neighbor in graph[idx]:
                        graph[neighbor].remove(idx)

                    del graph[idx]
                    broken = True
                    break

            if not broken:
                for idx in list(graph.keys()):
                    if isinstance(live.values[idx], CallingClobber):
                        continue

                    spills[idx] = 0

                    for neighbor in graph[idx]:
                        graph[neighbor].remove(idx)

                    del graph[idx]
                    break

        while worklist:
            node = worklist.pop()

            palette = set(range(len(system_v)))
            used = {colors[neighbor] for neighbor in copy[node] if neighbor in colors}

            available = palette - used
            colors[node] = min(available)

        for idx in list(copy.keys()):
            if isinstance(live.values[idx], CallingClobber):
                continue

            if idx not in spills:
                for neighbor in copy[idx]:
                    if idx != neighbor:
                        copy[neighbor].remove(idx)

                del copy[idx]

        graph = copy
        copy = {k: set(v) for k, v in graph.items()}
        spills.clear()

        for idx, value in enumerate(live.values):
            if isinstance(value, CallingClobber):
                del colors[idx]

        while len(graph) > count:
            for idx, edges in list(graph.items()):
                if isinstance(live.values[idx], CallingClobber):
                    continue

                worklist.append(idx)

                for neighbor in graph[idx]:
                    graph[neighbor].remove(idx)

                del graph[idx]
                break

        while worklist:
            node = worklist.pop()

            palette = set(range(len(live.values)))
            used = {spills[neighbor] for neighbor in copy[node] if neighbor in spills}

            available = palette - used
            spills[node] = min(available)

        allocations[fid] = Allocation(
            ref=live.ref,
            target=fid,
            values=live.values,
            colors=colors,
            spills=spills,
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
