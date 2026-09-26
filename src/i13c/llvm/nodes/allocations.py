from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.llvm.nodes.cflows import ControlFlowVisitor
from i13c.llvm.nodes.dflows import CALL, MOV, PROLOG, DataFlowSolver
from i13c.llvm.nodes.liveness import LivenessVisitor
from i13c.llvm.typing.allocations import Allocation, AllocationSegment
from i13c.llvm.typing.liveness import Liveness, LivenessSegment
from i13c.semantic.typing.analyses import llvm
from i13c.semantic.typing.analyses.fnlets import FnletInstruction
from i13c.semantic.typing.entities.functions import FunctionId


def configure_allocations() -> GraphNode:
    return GraphNode(
        builder=build_allocations,
        constraint=None,
        produces=("llvm/allocations",),
        requires=frozenset(
            {
                ("liveness", "llvm/liveness"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def create_systemv_palette() -> Palette:
    # fmt: off
    return Palette([
        b"rdi", b"rsi", b"rdx", b"rcx", b"r8", b"r9", b"r10",
        b"rax", b"rbx", b"rbp", b"r12", b"r13", b"r14", b"r15",
    ])
    # fmt: on


def build_allocations(
    liveness: OneToOne[FunctionId, Liveness],
) -> OneToOne[FunctionId, Allocation]:
    allocations: dict[FunctionId, Allocation] = {}
    palette = create_systemv_palette()

    for fid, live in liveness.items():
        allocations[fid] = allocate(live, palette)

    return OneToOne[FunctionId, Allocation].instance(allocations)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Allocation]) -> None:
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[tuple[FunctionId, int], tuple[Allocation, AllocationSegment]]]:
        for fid, allocation in self.data.items():
            for idx, segment in enumerate(allocation.segments):
                yield (fid, idx), (allocation, segment)

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "fn": "Function",
            "block": "Block",
            "colors": "Colors",
            "spills": "Spills",
        }

    @staticmethod
    def rows(
        key: tuple[FunctionId, int], entry: tuple[Allocation, AllocationSegment]
    ) -> dict[str, str]:
        palette = Palette(entry[0].palette)

        return {
            "fn": key[0].identify(1),
            "block": str(key[1]),
            "colors": str(
                {
                    entry[0].registers[k].decode(): palette.find_by_id(v).decode()
                    for k, v in entry[1].colors.items()
                }
            ),
            "spills": str(
                {entry[0].registers[k].decode(): v for k, v in entry[1].spills.items()}
            ),
        }


class LivenessLikeSegment(Protocol):
    def instructions(self) -> int: ...

    @property
    def clobbers(self) -> Sequence[Sequence[int]]: ...

    @property
    def live_in(self) -> Sequence[set[int]]: ...

    @property
    def live_out(self) -> Sequence[set[int]]: ...


@dataclass(kw_only=True, repr=False)
class FnletBlockMock:
    instructions: list[FnletInstruction]


@dataclass(kw_only=True, repr=False)
class FnletMock:
    blocks: list[FnletBlockMock]


class Palette:
    def __init__(self, registers: list[bytes]):
        self._registers = registers
        self._by_name = {name: idx for idx, name in enumerate(registers)}
        self._by_id = {idx: name for idx, name in enumerate(registers)}

    def size(self) -> int:
        return len(self._registers)

    def registers(self) -> list[bytes]:
        return self._registers

    def contains(self, name: bytes) -> bool:
        return name in self._by_name

    def find_by_id(self, idx: int) -> bytes:
        return self._by_id[idx]

    def find_by_name(self, name: bytes) -> int:
        return self._by_name[name]


@dataclass(kw_only=True)
class Seeds:
    colors: list[tuple[int, int]]
    spills: list[tuple[int, int]]

    @staticmethod
    def empty() -> Seeds:
        return Seeds(colors=[], spills=[])


@dataclass(kw_only=True)
class Precolored:
    colors: dict[int, int]
    spills: dict[int, int]

    @staticmethod
    def empty() -> Precolored:
        return Precolored(colors={}, spills={})


@dataclass(kw_only=True)
class PhysicalRegister:
    name: bytes


@dataclass(kw_only=True)
class VirtualRegister:
    name: bytes


InterferenceNode = VirtualRegister | PhysicalRegister
InterferenceEdge = tuple[InterferenceNode, InterferenceNode]


def into_registers(
    palette: Palette, values: Iterable[bytes]
) -> Iterable[InterferenceNode]:
    for value in values:
        if palette.contains(value) or value in (b"r11", b"rsp"):
            yield PhysicalRegister(name=value)
        else:
            yield VirtualRegister(name=value)


@staticmethod
def into_graph(
    palette: Palette,
    registers: Iterable[bytes],
    segment: LivenessLikeSegment,
    seeds: Seeds,
) -> tuple[InterferenceGraph, Precolored]:
    graph = InterferenceGraph()
    mapping = list(into_registers(palette, registers))

    colors: dict[int, int] = {}
    spills: dict[int, int] = {}

    for iid in range(segment.instructions()):
        clobbers = set(segment.clobbers[iid])
        live_in = segment.live_in[iid]
        live_out = segment.live_out[iid]

        vals1 = clobbers.union(live_out)
        vals2 = live_out.union(live_in)

        pairs1 = {(a, b) for a in vals1 for b in vals1 if a < b}
        pairs2 = {(a, b) for a in vals2 for b in vals2 if a < b}

        for idx in sorted(vals1.union(vals2)):
            graph.add(mapping[idx])

        # seeding initial registers maybe added
        # but we skip adding them to the edges
        for reg, color in seeds.colors:
            if reg in vals1 or reg in vals2:
                reg = graph.map(mapping[reg])
                colors[reg] = color

        # regular interference
        for left, right in pairs1:
            graph.insert((mapping[left], mapping[right]))

        # regular interference
        for left, right in pairs2:
            graph.insert((mapping[left], mapping[right]))

    # remap spills according to the graph
    for reg, color in seeds.spills:
        spills[graph.map(mapping[reg])] = color

    return graph, Precolored(colors=colors, spills=spills)


def allocate(liveness: Liveness, palette: Palette) -> Allocation:
    segments: list[AllocationSegment] = []
    nametoid: dict[bytes, int] = {}
    idtoname: dict[int, bytes] = {}
    clobbers: set[bytes] = set()

    for idx, name in enumerate(liveness.registers):
        nametoid[name] = idx
        idtoname[idx] = name

    # initially seed is physical reg -> virtual reg
    # and needs to be changed to virtual reg -> color
    colors: list[tuple[int, int]] = [
        (dst, palette.find_by_name(idtoname[src])) for src, dst in liveness.seeds
    ]

    seeds: Seeds = Seeds(
        colors=colors,
        spills=[],
    )

    for segment in liveness.segments:
        graph, hints = into_graph(palette, liveness.registers, segment, seeds)
        lcolors, lspills, _ = solve(graph, palette, precolors=hints)

        gcolors: dict[int, int] = {}
        gspills: dict[int, int] = {}

        for idx, color in lcolors.items():
            node: InterferenceNode = graph.at(idx)
            if isinstance(node, VirtualRegister):
                gcolors[nametoid[node.name]] = color

        for idx, color in lspills.items():
            node: InterferenceNode = graph.at(idx)
            if isinstance(node, VirtualRegister):
                gspills[nametoid[node.name]] = color

        seeds.colors = [(idx, color) for idx, color in gcolors.items()]
        seeds.spills = [(idx, color) for idx, color in gspills.items()]

        for regs in segment.clobbers:
            for reg in regs:
                clobbers.add(liveness.registers[reg])

        segments.append(AllocationSegment(colors=gcolors, spills=gspills))

    return Allocation(
        registers=liveness.registers,
        segments=segments,
        seeds=liveness.seeds,
        palette=palette.registers(),
        clobbers=sorted(clobbers),
    )


def reshuffle(
    graph: InterferenceGraph,
    data: dict[int, int],
    /,
    precolors: dict[int, int] = {},
    clobbers: set[int] = set(),
) -> dict[int, int]:
    mapping: dict[int, int] = {}

    # preserve clobbered colors in the mapping
    # to avoid remapping clobbered colors
    for color in clobbers:
        mapping[color] = color

    # preserve precolors nodes in the mapping
    for idx, color in sorted(data.items(), key=lambda x: x[0]):
        if color not in mapping:
            if idx in precolors and precolors[idx] not in mapping.values():
                mapping[color] = precolors[idx]

    # determine the set of colors that are not yet mapped
    colors = {v for v in data.values() if v not in mapping.values()}
    palette: list[int] = sorted(colors, reverse=True)

    # build mapping from remaining colors
    for idx, _ in graph.nodes():
        if idx in data and data[idx] not in mapping:
            mapping[data[idx]] = palette.pop()

    # remap old colors to new colors using the built mapping
    return {idx: mapping[color] for idx, color in data.items()}


def solve(
    graph: InterferenceGraph,
    palette: Palette,
    /,
    precolors: Precolored = Precolored.empty(),
) -> tuple[dict[int, int], dict[int, int], dict[int, int]]:
    # prepare graph and solver
    copy: InterferenceGraph = graph.copy()
    solver = InterferenceSolver(graph, copy)

    # solve first time to get colors/spills
    solver.preprocess(palette, precolors.colors)
    solver.pass_zero(palette=palette.size())
    solver.pass_one(palette=palette.size())
    solver.pass_two(palette=palette.size())

    # extract exact colors from the first pass
    colors: dict[int, int] = {reg: color for reg, color in solver.colors()}
    clobbers: dict[int, int] = {reg: color for reg, color in solver.clobbers()}

    colors = reshuffle(
        copy,
        colors,
        precolors=precolors.colors,
        clobbers=set(clobbers.values()),
    )

    # remove colored nodes from the copy to prepare for the second round
    for reg, _ in solver.colors():
        copy.remove(reg)

    # prepare 2nd round
    graph, copy = copy, copy.copy()
    solver = InterferenceSolver(graph, copy)
    required = graph.size() + 1

    # solve again with the full palette to handle spills
    solver.preprocess(palette, {})
    solver.pass_zero(palette=required)
    solver.pass_one(palette=required)
    solver.pass_two(palette=required)

    # extract exact spills from the second pass
    spills: dict[int, int] = {reg: color for reg, color in solver.colors()}
    spills = reshuffle(copy, spills, precolors=precolors.spills)

    # combine the results from both passes
    return colors, spills, clobbers


class InterferenceGraph:
    def __init__(self) -> None:
        self._nodes: set[int] = set()
        self._edges: dict[int, set[int]] = {}
        self._mapping: list[InterferenceNode] = []

    def copy(self) -> InterferenceGraph:
        graph = InterferenceGraph()

        # deep copy the nodes and edges
        graph._mapping = self._mapping.copy()
        graph._nodes = self._nodes.copy()
        graph._edges = {k: v.copy() for k, v in self._edges.items()}

        return graph

    def size(self) -> int:
        return len(self._nodes)

    def at(self, index: int) -> InterferenceNode:
        return self._mapping[index]

    def nodes(self) -> Iterable[tuple[int, InterferenceNode]]:
        yield from ((idx, self._mapping[idx]) for idx in self._nodes)

    def edges(
        self,
        /,
        node_spec: type[InterferenceNode] | None = VirtualRegister,
        neighbor_spec: type[InterferenceNode] | None = VirtualRegister,
    ) -> Iterable[tuple[int, set[int]]]:
        yield from (
            (idx, self.neighbors(idx, neighbor_spec))
            for idx, node in self.nodes()
            if node_spec is None or isinstance(node, node_spec)
        )

    def neighbors(
        self,
        node: int,
        spec: type[InterferenceNode] | None = VirtualRegister,
    ) -> set[int]:
        if spec is None:
            return self._edges.get(node, set())
        else:
            return {
                neighbor
                for neighbor in self._edges.get(node, set())
                if isinstance(self._mapping[neighbor], spec)
            }

    def find(self, node: InterferenceNode) -> int:
        return self._mapping.index(node)

    def map(self, node: InterferenceNode) -> int:
        # add new mapping if it is not already present
        if node not in self._mapping:
            self._mapping.append(node)
            idx = len(self._mapping) - 1
        else:
            idx = self._mapping.index(node)

        # return the index of the added or existing node
        return idx

    def add(self, node: InterferenceNode) -> int:
        # map the node to an index
        idx = self.map(node)

        # add the node index to the set of nodes
        self._nodes.add(idx)

        # return the index of the added or existing node
        return idx

    def insert(self, edge: InterferenceEdge):
        # find the indices of the both nodes
        left = self._mapping.index(edge[0])
        right = self._mapping.index(edge[1])

        # add the left node to the edges
        if left not in self._edges:
            self._edges[left] = set()

        # add the right node to the edges
        if right not in self._edges:
            self._edges[right] = set()

        # add the adjacency edge
        self._edges[left].add(right)
        self._edges[right].add(left)

    def remove(self, node: int):
        for neighbor in self._edges.get(node, set()):
            self._edges[neighbor].remove(node)

        self._edges.pop(node, None)
        self._nodes.remove(node)


class InterferenceSolver:
    def __init__(self, graph: InterferenceGraph, copy: InterferenceGraph):
        self._graph = graph
        self._copy = copy

        # processed nodes count
        self._count: int = 0
        self._worklist: list[int] = []

        # dictionaries to store spills and colors for nodes
        self._spills: dict[int, int] = {}
        self._colors: dict[int, int] = {}
        self._precolors: dict[int, int] = {}

    def colors(self) -> Iterable[tuple[int, int]]:
        return (
            (node, color)
            for node, color in self._colors.items()
            if isinstance(self._graph.at(node), VirtualRegister)
        )

    def clobbers(self) -> Iterable[tuple[int, int]]:
        return (
            (node, color)
            for node, color in self._colors.items()
            if isinstance(self._graph.at(node), PhysicalRegister)
        )

    def preprocess(self, palette: Palette, colors: dict[int, int]):
        # precolor clobbered physical registers
        for idx, reg in list(self._graph.nodes()):
            if isinstance(reg, PhysicalRegister):
                if palette.contains(reg.name):
                    self._count = self._count + 1
                    self._colors[idx] = palette.find_by_name(reg.name)
                else:
                    self._count = self._count + 1
                    self._colors[idx] = -1

        # try to reserve color candidates
        for idx, color in colors.items():
            if color not in self._colors.values():
                self._precolors[idx] = color

    def pass_zero(self, /, palette: int = 15):
        specs: dict[str, type | None] = {
            "node_spec": VirtualRegister,
            "neighbor_spec": None,
        }

        # decide which nodes can be certainly colored
        # and which one are candidates for spilling
        while self._graph.size() > self._count:
            broken = False

            for node, edges in reversed(list(self._graph.edges(**specs))):
                if len(edges) < palette:
                    self._worklist.append(node)
                    self._graph.remove(node)

                    broken = True
                    break

            if not broken:
                for node, edges in reversed(list(self._graph.edges(**specs))):
                    self._spills[node] = 0
                    self._graph.remove(node)
                    break

    def pass_one(self, /, palette: int = 15):
        # assign colors to perfect candidates
        while self._worklist:
            node = self._worklist.pop()
            available = self._available_colors(node, palette)

            # allocate available color
            self._colors[node] = min(available)

    def pass_two(self, /, palette: int = 15):
        # assign colors to spill candidates if possible
        for idx in reversed(list(self._spills.keys())):
            # determine available colors for the current node
            available = self._available_colors(idx, palette)

            if len(available) > 0:
                # allocate either preferred color or the minimum available color
                self._colors[idx] = min(available)

                # no longer spilled
                del self._spills[idx]

    def _available_colors(self, node: int, palette: int) -> set[int]:
        # collect colors used by neighboring nodes
        used = {
            self._colors[neighbor]
            for neighbor in self._copy.neighbors(node, spec=None)
            if neighbor in self._colors
        }

        # if the node is already pre-colored, try return its color immediately
        if node in self._precolors:
            # but if its color is already used by neighbors, we cannot keep it
            if self._precolors[node] in used:
                self._precolors.pop(node)

            # otherwise, we can keep its pre-colored value
            else:
                color = self._precolors[node]
                self._precolors.pop(node)
                return {color}

        # try to avoid using colors that are already pre-colored
        # and we have still capacity to give out a new color
        if used and self._precolors:
            # try to reduced set of colors if we can afford to avoid pre-colored ones
            if available := set(range(palette)) - used - set(self._precolors.values()):
                return available

        # determine available colors for the current node
        return set(range(palette)) - used


def can_detect_physical_registers():
    regs1 = [b"rax", b"rbx", b"rcx", b"rdx", b"rsi", b"rdi", b"rsp", b"rbp"]
    regs2 = [b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15"]

    # use the System V calling convention palette
    palette = create_systemv_palette()

    # every name here is a real SYSV register (or rsp, handled alongside
    # it as a special case), so into_registers must classify all of them
    # as physical rather than virtual
    for reg in into_registers(palette, regs1):
        assert isinstance(reg, PhysicalRegister)

    for reg in into_registers(palette, regs2):
        assert isinstance(reg, PhysicalRegister)


def can_detect_virtual_registers():
    vregs = [b"v0", b"v1", b"v2", b"v3", b"v4", b"v5", b"v6", b"v7"]

    # use the System V calling convention palette
    palette = create_systemv_palette()

    # none of these names appear in SYSV or match rsp, so into_registers
    # must classify all of them as virtual
    for reg in into_registers(palette, vregs):
        assert isinstance(reg, VirtualRegister)


def can_construct_empty_interference_graph():
    graph = InterferenceGraph()

    assert graph.size() == 0
    assert list(graph.nodes()) == []
    assert len(list(graph.edges())) == 0


def can_construct_one_pair_interference_graph():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")

    graph.add(node1)
    graph.add(node2)
    graph.insert((node1, node2))

    assert graph.size() == 2
    assert list(graph.nodes()) == [(0, node1), (1, node2)]
    assert len(list(graph.edges())) == 2

    # inserting an edge is symmetric: each node ends up in the other's
    # neighbor set
    assert list(graph.neighbors(0)) == [1]
    assert list(graph.neighbors(1)) == [0]


def can_construct_no_pair_interference_graph():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")

    graph.add(node1)
    graph.add(node2)

    assert graph.size() == 2
    assert list(graph.nodes()) == [(0, node1), (1, node2)]

    # edges() yields one entry per node, not per actual edge — with none
    # inserted, both entries just carry an empty neighbor set
    assert len(list(graph.edges())) == 2
    assert list(graph.neighbors(0)) == []
    assert list(graph.neighbors(1)) == []


def can_remove_node_from_interference_graph():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")
    node3 = VirtualRegister(name=b"v2")

    graph.add(node1)
    graph.add(node2)
    graph.add(node3)

    graph.insert((node1, node2))
    graph.insert((node2, node3))
    graph.insert((node1, node3))

    graph.remove(1)

    assert graph.size() == 2
    assert list(graph.nodes()) == [(0, node1), (2, node3)]
    assert len(list(graph.edges())) == 2

    # removing v1 clears it from v0/v2's adjacency too; querying its own
    # (now-gone) neighbors just returns empty rather than raising
    assert list(graph.neighbors(0)) == [2]
    assert list(graph.neighbors(1)) == []
    assert list(graph.neighbors(2)) == [0]


def can_reshuffle_colors_unchanged_when_nothing_is_pinned():
    graph = InterferenceGraph()

    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")
    v1 = VirtualRegister(name=b"v1")

    graph.add(rdi)
    graph.add(v0)
    graph.add(v1)

    graph.insert((rdi, v0))
    graph.insert((v0, v1))

    colors = {1: 1, 2: 2}
    reshufled = reshuffle(graph, colors)

    # no clobbers/hints to protect, so reshuffle just renumbers colors in
    # graph-traversal order, which here happens to match the input already
    assert reshufled == {1: 1, 2: 2}


def can_reshuffle_refuse_to_reuse_a_clobbered_color():
    graph = InterferenceGraph()

    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")
    v1 = VirtualRegister(name=b"v1")

    graph.add(rdi)
    graph.add(v0)
    graph.add(v1)

    graph.insert((rdi, v0))
    graph.insert((v0, v1))

    colors, clobbers = {1: 1, 2: 0}, {0}
    reshufled = reshuffle(graph, colors, clobbers=clobbers)

    # color 0 is marked as a clobber, so it's pinned to itself; v1 (idx 2)
    # keeps it even though nothing precolors v1 directly
    assert reshufled == {1: 1, 2: 0}


def can_reshuffle_refuse_to_reuse_a_clobbered_color_even_with_a_matching_hint():
    graph = InterferenceGraph()

    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")
    v1 = VirtualRegister(name=b"v1")

    graph.add(rdi)
    graph.add(v0)
    graph.add(v1)

    graph.insert((rdi, v0))
    graph.insert((v0, v1))

    colors, clobbers, hints = {1: 1, 2: 0}, {0}, {0: 0}
    reshufled = reshuffle(graph, colors, clobbers=clobbers, precolors=hints)

    # hinting rdi's own node to its own color is redundant: the clobber
    # pin already reserves color 0, so the result is unchanged
    assert reshufled == {1: 1, 2: 0}


def can_reshuffle_reorder_colors_to_match_node_order():
    graph = InterferenceGraph()

    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")
    v1 = VirtualRegister(name=b"v1")

    graph.add(rdi)
    graph.add(v0)
    graph.add(v1)

    graph.insert((rdi, v0))
    graph.insert((v0, v1))

    colors = {1: 9, 2: 5}
    reshufled = reshuffle(graph, colors)

    # reshuffle canonicalizes by node order: v0 (idx 1) gets the smaller
    # value, v1 (idx 2) the larger — the reverse of the raw input
    assert reshufled == {1: 5, 2: 9}


def can_reshuffle_apply_two_independent_hints_without_collision():
    graph = InterferenceGraph()

    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")
    v1 = VirtualRegister(name=b"v1")

    graph.add(rdi)
    graph.add(v0)
    graph.add(v1)

    graph.insert((rdi, v0))
    graph.insert((v0, v1))

    colors, hints = {1: 7, 2: 3}, {1: 2, 2: 9}
    reshufled = reshuffle(graph, colors, precolors=hints)

    # each node has its own distinct hint, so both get applied independently
    assert reshufled == {1: 2, 2: 9}


def can_reshuffle_reject_a_hint_colliding_with_another_nodes_hint():
    graph = InterferenceGraph()

    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")
    v1 = VirtualRegister(name=b"v1")

    graph.add(rdi)
    graph.add(v0)
    graph.add(v1)

    graph.insert((rdi, v0))
    graph.insert((v0, v1))

    colors, hints = {1: 3, 2: 7}, {1: 5, 2: 5}
    reshufled = reshuffle(graph, colors, precolors=hints)

    # v0 and v1 interfere, so they can't both take hint color 5; v0 is
    # processed first and keeps it, v1's colliding hint is rejected and it
    # keeps its own raw color instead
    assert reshufled == {1: 5, 2: 3}


def can_solve_interference_graph_two_nodes_no_pair():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")

    graph.add(node1)
    graph.add(node2)

    palette = Palette([b"rdi", b"rsi"])
    colors, spills, clobbers = solve(graph, palette)

    # v0 and v1 never interfere, so they're free to share the same color
    assert colors == {0: 0, 1: 0}
    assert spills == {}
    assert clobbers == {}


def can_solve_interference_graph_two_nodes_with_pair():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")

    graph.add(node1)
    graph.add(node2)
    graph.insert((node1, node2))

    palette = Palette([b"rdi", b"rsi"])
    colors, spills, clobbers = solve(graph, palette)

    # v0 and v1 interfere, and with exactly 2 colors available they must
    # take the two different ones
    assert colors == {0: 0, 1: 1}
    assert spills == {}
    assert clobbers == {}


def can_solve_interference_graph_three_paired_nodes():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")
    node3 = VirtualRegister(name=b"v2")

    graph.add(node1)
    graph.add(node2)
    graph.add(node3)
    graph.insert((node1, node2))
    graph.insert((node2, node3))
    graph.insert((node1, node3))

    palette = Palette([b"rdi", b"rsi", b"rdx"])
    colors, spills, clobbers = solve(graph, palette)

    # a 3-clique needs 3 distinct colors, and palette=3 has exactly enough
    # room for one each, so nothing spills
    assert colors == {0: 0, 1: 1, 2: 2}
    assert spills == {}
    assert clobbers == {}


def can_solve_interference_graph_three_paired_nodes_with_two_colors():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")
    node3 = VirtualRegister(name=b"v2")

    graph.add(node1)
    graph.add(node2)
    graph.add(node3)
    graph.insert((node1, node2))
    graph.insert((node2, node3))
    graph.insert((node1, node3))

    palette = Palette([b"rdi", b"rsi"])
    colors, spills, clobbers = solve(graph, palette)

    # a 3-clique can't be colored with only 2, so one node (v2) spills;
    # v0/v1 are left with degree 1 each and split the two colors
    assert colors == {0: 0, 1: 1}
    assert spills == {2: 0}
    assert clobbers == {}


def can_solve_interference_graph_three_pairs_with_one_physical():
    graph = InterferenceGraph()

    node1 = PhysicalRegister(name=b"rax")
    node2 = VirtualRegister(name=b"v1")
    node3 = VirtualRegister(name=b"v2")

    graph.add(node1)
    graph.add(node2)
    graph.add(node3)
    graph.insert((node1, node2))
    graph.insert((node2, node3))
    graph.insert((node1, node3))

    palette = Palette([b"rax", b"rdi", b"rsi"])
    colors, spills, clobbers = solve(graph, palette)

    # rax sits inside this 3-slot palette (index 0), so v1/v2 must both
    # avoid it as well as each other — with exactly 3 slots total, they
    # still fit without spilling
    assert colors == {1: 1, 2: 2}
    assert spills == {}
    assert clobbers == {0: palette.find_by_name(b"rax")}


def can_solve_interference_graph_three_pairs_precolors():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")
    node3 = VirtualRegister(name=b"v2")

    graph.add(node1)
    graph.add(node2)
    graph.add(node3)
    graph.insert((node1, node2))
    graph.insert((node2, node3))
    graph.insert((node1, node3))

    palette = Palette([b"rdi", b"rsi", b"rdx"])
    precolors = Precolored(colors={2: 0}, spills={})
    colors, spills, clobbers = solve(graph, palette, precolors=precolors)

    # v2 is pinned to color 0; v0/v1 still interfere with it (checked
    # against the untouched copy), so they split the remaining colors
    assert colors == {0: 1, 1: 2, 2: 0}
    assert spills == {}
    assert clobbers == {}


def can_solve_interference_graph_drop_a_conflicting_hint_to_avoid_a_spill():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")
    node3 = VirtualRegister(name=b"v2")

    graph.add(node1)
    graph.add(node2)
    graph.add(node3)
    graph.insert((node1, node3))
    graph.insert((node2, node3))

    palette = Palette([b"rdi", b"rsi"])
    precolors = Precolored(colors={0: 0, 1: 1}, spills={})
    colors, spills, clobbers = solve(graph, palette, precolors=precolors)

    # v1's hint (1) collides with v2, which already holds it; v1 falls
    # back to the other color instead, which is fine since v0 and v1 never
    # interfere with each other — no need to spill anything
    assert colors == {0: 0, 1: 0, 2: 1}
    assert spills == {}
    assert clobbers == {}


def can_solve_interference_graph_three_pairs_two_spilled():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")
    node3 = VirtualRegister(name=b"v2")

    graph.add(node1)
    graph.add(node2)
    graph.add(node3)
    graph.insert((node1, node2))
    graph.insert((node2, node3))
    graph.insert((node1, node3))

    palette = Palette([b"rdi"])
    colors, spills, clobbers = solve(graph, palette)

    # palette=1 colors only v0; v1/v2 fall through to the spill-slot pass,
    # which is sized to fit both with distinct slots
    assert colors == {0: 0}
    assert spills == {1: 0, 2: 1}
    assert clobbers == {}


def can_solve_interference_graph_no_pairs_precolors():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")

    graph.add(node1)
    graph.add(node2)

    palette = Palette([b"rdi", b"rsi"])
    precolors = Precolored(colors={1: 0}, spills={})
    colors, spills, clobbers = solve(graph, palette, precolors=precolors)

    # v0 and v1 don't interfere, so v1's precolors 0 leaves v0 free to
    # take the same color too
    assert colors == {0: 0, 1: 0}
    assert spills == {}
    assert clobbers == {}


def can_solve_interference_graph_no_pairs_precolors_different():
    graph = InterferenceGraph()

    node1 = VirtualRegister(name=b"v0")
    node2 = VirtualRegister(name=b"v1")

    graph.add(node1)
    graph.add(node2)

    palette = Palette([b"rdi", b"rsi"])
    precolors = Precolored(colors={1: 1}, spills={})
    colors, spills, clobbers = solve(graph, palette, precolors=precolors)

    # same as above but v1 is precolors 1 instead; v0 still just takes
    # the cheapest free color since the two don't interfere
    assert colors == {0: 0, 1: 1}
    assert spills == {}
    assert clobbers == {}


def can_solve_interference_graph_chain_with_one_physical():
    graph = InterferenceGraph()

    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")
    v1 = VirtualRegister(name=b"v1")

    graph.add(rdi)
    graph.add(v0)
    graph.add(v1)

    graph.insert((rdi, v0))
    graph.insert((v0, v1))

    palette = Palette(
        [b"rdi", b"rsi", b"rdx", b"rcx", b"r8", b"r9", b"r10", b"r11", b"r12", b"r13"]
    )
    colors, spills, clobbers = solve(graph, palette)

    # v0 interferes with rdi and must avoid color 0; v1 only interferes
    # with v0, so it's free to reuse rdi's color
    assert colors == {1: 1, 2: 0}
    assert spills == {}
    assert clobbers == {0: palette.find_by_name(b"rdi")}


def can_solve_interference_graph_avoid_two_distinct_physical_registers():
    graph = InterferenceGraph()

    rax = PhysicalRegister(name=b"rax")
    rdi = PhysicalRegister(name=b"rdi")
    v0 = VirtualRegister(name=b"v0")

    graph.add(rax)
    graph.add(rdi)
    graph.add(v0)

    graph.insert((rax, v0))
    graph.insert((rdi, v0))

    palette = create_systemv_palette()
    colors, spills, clobbers = solve(graph, palette)

    # v0 interferes with both rax and rdi, so it must avoid both real
    # colors and takes the next free one instead
    assert colors == {2: 1}
    assert spills == {}

    assert clobbers == {
        0: palette.find_by_name(b"rax"),
        1: palette.find_by_name(b"rdi"),
    }


def can_allocate_keep_a_spilled_vregs_slot_stable_across_segments():
    registers = [b"v0", b"v1", b"v2"]
    palette = Palette([b"rax"])

    # segment0: v0/v2 interfere, palette=1, v2 spills alone to slot 0
    segment0 = LivenessSegment(
        live_in=[{0, 2}],
        live_out=[{0, 2}],
        clobbers=[[]],
    )

    # segment1: v0/v1/v2 interfere, v0 still takes the one register, but
    # v1 now competes with v2 for a spill slot too
    segment1 = LivenessSegment(
        live_in=[{0, 1, 2}],
        live_out=[{0, 1, 2}],
        clobbers=[[]],
    )

    liveness = Liveness(
        registers=registers,
        segments=[segment0, segment1],
        seeds=[],
    )

    allocation = allocate(liveness, palette)
    assert allocation.segments[0].spills == {2: 0}

    # v2 was already spilled to slot 0; it must keep that same slot here,
    # not be bumped just because v1 also needs a slot in this segment
    assert allocation.segments[1].spills == {1: 1, 2: 0}


def prepare_liveness(fnlet: FnletMock):
    cvisitor = ControlFlowVisitor()
    lvisitor = LivenessVisitor()

    solver = DataFlowSolver()
    solver.register(PROLOG())
    solver.register(CALL())
    solver.register(MOV())

    cflow = cvisitor.visit(fnlet)
    dflow = solver.solve(FunctionId(value=10), fnlet)
    liveness = lvisitor.visit(fnlet, cflow, dflow)

    return liveness


def can_handle_graphs_from_empty_fnlet():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare fnlet and liveness
    fnlet = FnletMock(blocks=[entry, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    # no binds and no body: nothing is ever live, so every graph, hint,
    # color, spill and clobber below stays empty
    graph0, hints0 = into_graph(
        palette, liveness.registers, liveness.segments[0], Seeds.empty()
    )
    graph1, hints1 = into_graph(
        palette, liveness.registers, liveness.segments[1], Seeds.empty()
    )

    assert graph0.size() == 0
    assert graph1.size() == 0

    assert hints0.colors == {}

    assert hints0.spills == {}
    assert hints1.colors == {}
    assert hints1.spills == {}

    colors0, spills0, clobbers0 = solve(graph0, palette)
    colors1, spills1, clobbers1 = solve(graph1, palette)

    assert colors0 == {}
    assert spills0 == {}
    assert clobbers0 == {}

    assert colors1 == {}
    assert spills1 == {}
    assert clobbers1 == {}

    # allocate registers
    allocation = allocate(liveness, palette)
    assert len(allocation.segments) == 2

    # no binds at all, so nothing seeds the allocation either
    assert allocation.seeds == []

    assert allocation.segments[0].colors == {}
    assert allocation.segments[0].spills == {}
    assert allocation.segments[1].colors == {}
    assert allocation.segments[1].spills == {}


def can_handle_graphs_from_fnlet_with_binds():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(
                operands=(),
                binds={
                    b"v0": llvm.Register(name=b"rdi"),
                    b"v1": llvm.Register(name=b"rsi"),
                },
                preserves=[],
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare fnlet and liveness
    fnlet = FnletMock(blocks=[entry, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    assert liveness.registers == [b"rdi", b"v0", b"rsi", b"v1"]
    assert liveness.seeds == [(0, 1), (2, 3)]

    # v0/v1 are bound at entry but never used before EPILOG, so they're dead
    # on arrival and never enter any segment's interference graph
    graph0, hints0 = into_graph(
        palette,
        liveness.registers,
        liveness.segments[0],
        Seeds(colors=[(0, 1), (2, 3)], spills=[]),
    )

    graph1, hints1 = into_graph(
        palette,
        liveness.registers,
        liveness.segments[1],
        Seeds.empty(),
    )

    assert graph0.size() == 0
    assert graph1.size() == 0

    assert hints0.colors == {}

    assert hints0.spills == {}
    assert hints1.colors == {}
    assert hints1.spills == {}

    colors0, spills0, clobbers0 = solve(graph0, palette)
    colors1, spills1, clobbers1 = solve(graph1, palette)

    assert colors0 == {}
    assert spills0 == {}
    assert clobbers0 == {}

    assert colors1 == {}
    assert spills1 == {}
    assert clobbers1 == {}

    # allocate registers
    allocation = allocate(liveness, palette)
    assert len(allocation.segments) == 2

    # same seeds as liveness: v0 from rdi, v1 from rsi
    assert allocation.seeds == [(0, 1), (2, 3)]

    assert allocation.registers[1] == b"v0"
    assert allocation.registers[3] == b"v1"

    # not used so can be overwritten
    assert allocation.segments[0].colors == {}
    assert allocation.segments[0].spills == {}
    assert allocation.segments[1].colors == {}
    assert allocation.segments[1].spills == {}


def can_handle_graphs_from_fnlet_with_call_and_params():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(
                operands=(),
                binds={
                    b"v0": llvm.Register(name=b"rdi"),
                    b"v1": llvm.Register(name=b"rsi"),
                },
                preserves=[],
            ),
        ]
    )

    body = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"r11", b"rcx"],
                args={
                    b"rdi": llvm.Register(name=b"v1"),
                    b"rsi": llvm.Register(name=b"v0"),
                    b"rdx": llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare fnlet and liveness
    fnlet = FnletMock(blocks=[entry, body, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    graph0, hints0 = into_graph(
        palette,
        liveness.registers,
        liveness.segments[0],
        Seeds(
            colors=[
                (1, palette.find_by_name(b"rdi")),
                (3, palette.find_by_name(b"rsi")),
            ],
            spills=[],
        ),
    )

    # graph1/graph2 are checked here with no seeds of their own — only
    # allocate() below actually carries hints across segment boundaries
    graph1, hints1 = into_graph(
        palette, liveness.registers, liveness.segments[1], Seeds.empty()
    )
    graph2, hints2 = into_graph(
        palette, liveness.registers, liveness.segments[2], Seeds.empty()
    )

    assert graph0.size() == 2
    assert graph1.size() == 4
    assert graph2.size() == 0

    assert hints0.colors == {
        0: palette.find_by_name(b"rdi"),
        1: palette.find_by_name(b"rsi"),
    }
    assert hints0.spills == {}

    assert hints1.colors == {}

    assert hints1.spills == {}
    assert hints2.colors == {}
    assert hints2.spills == {}

    colors0, spills0, clobbers0 = solve(graph0, palette)
    colors1, spills1, clobbers1 = solve(graph1, palette)
    colors2, spills2, clobbers2 = solve(graph2, palette)

    assert graph0.at(0) == VirtualRegister(name=b"v0")
    assert graph0.at(1) == VirtualRegister(name=b"v1")

    # hints are honored directly since nothing else claims rdi/rsi yet
    assert colors0 == {0: 0, 1: 1}
    assert spills0 == {}
    assert clobbers0 == {}

    assert graph1.at(0) == VirtualRegister(name=b"v0")
    assert graph1.at(1) == VirtualRegister(name=b"v1")
    assert graph1.at(2) == PhysicalRegister(name=b"r11")
    assert graph1.at(3) == PhysicalRegister(name=b"rcx")

    # this call clobbers r11/rcx only, never rdi/rsi, so v0/v1 keep their
    # hinted registers with no forced move
    assert colors1 == {0: 0, 1: 1}
    assert spills1 == {}

    # r11 isn't in the palette, so its clobber precolors to -1, not a real index
    assert clobbers1 == {
        2: -1,
        3: palette.find_by_name(b"rcx"),
    }

    assert colors2 == {}
    assert spills2 == {}
    assert clobbers2 == {}

    # allocate registers
    allocation = allocate(liveness, palette)
    assert len(allocation.segments) == 3

    # v0 is bound from rdi, v1 from rsi
    assert allocation.seeds == [(0, 1), (2, 3)]

    assert allocation.registers[1] == b"v0"
    assert allocation.registers[3] == b"v1"

    # no clobber here ever touches rdi/rsi, so v0/v1 keep the same
    # registers across every segment
    assert allocation.segments[0].colors == {
        1: palette.find_by_name(b"rdi"),
        3: palette.find_by_name(b"rsi"),
    }
    assert allocation.segments[0].spills == {}
    assert allocation.segments[1].colors == {
        1: palette.find_by_name(b"rdi"),
        3: palette.find_by_name(b"rsi"),
    }
    assert allocation.segments[1].spills == {}
    assert allocation.segments[2].colors == {}
    assert allocation.segments[2].spills == {}


def can_handle_graphs_from_fnlet_with_multiline_instructions():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body1 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v0"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v1"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"rsi"],
                args={
                    b"rdi": llvm.Register(name=b"v0"),
                    b"rsi": llvm.Register(name=b"v1"),
                },
            ),
        ]
    )

    body2 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v2"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"rdi"],
                args={
                    b"rdi": llvm.Register(name=b"v2"),
                    b"rsi": llvm.Register(name=b"v0"),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare fnlet and liveness
    fnlet = FnletMock(blocks=[entry, body1, body2, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    graph0, hints0 = into_graph(
        palette, liveness.registers, liveness.segments[0], Seeds.empty()
    )
    graph1, hints1 = into_graph(
        palette, liveness.registers, liveness.segments[1], Seeds.empty()
    )
    graph2, hints2 = into_graph(
        palette, liveness.registers, liveness.segments[2], Seeds.empty()
    )
    graph3, hints3 = into_graph(
        palette, liveness.registers, liveness.segments[3], Seeds.empty()
    )

    assert graph0.size() == 0
    assert graph1.size() == 3
    assert graph2.size() == 3
    assert graph3.size() == 0

    assert hints0.colors == {}

    assert hints0.spills == {}
    assert hints1.colors == {}
    assert hints1.spills == {}
    assert hints2.colors == {}
    assert hints2.spills == {}
    assert hints3.colors == {}
    assert hints3.spills == {}

    colors0, spills0, clobbers0 = solve(graph0, palette)
    colors1, spills1, clobbers1 = solve(graph1, palette)
    colors2, spills2, clobbers2 = solve(graph2, palette)
    colors3, spills3, clobbers3 = solve(graph3, palette)

    # no instructions before the MOVs, so nothing is live yet
    assert colors0 == {}
    assert spills0 == {}
    assert clobbers0 == {}

    assert graph1.at(0) == VirtualRegister(name=b"v0")
    assert graph1.at(1) == VirtualRegister(name=b"v1")
    assert graph1.at(2) == PhysicalRegister(name=b"rsi")

    # v1 is only a call argument here and dies at the call, so it can
    # freely share rsi's color even though rsi is what gets clobbered
    assert colors1 == {0: 0, 1: 1}
    assert spills1 == {}
    assert clobbers1 == {2: palette.find_by_name(b"rsi")}

    assert graph2.at(0) == VirtualRegister(name=b"v0")
    assert graph2.at(1) == VirtualRegister(name=b"v2")
    assert graph2.at(2) == PhysicalRegister(name=b"rdi")

    # same reasoning for rdi: v0 dies here too, so it can share the slot
    assert colors2 == {0: 0, 1: 1}
    assert spills2 == {}
    assert clobbers2 == {2: palette.find_by_name(b"rdi")}

    assert colors3 == {}
    assert spills3 == {}
    assert clobbers3 == {}

    # allocate registers
    allocation = allocate(liveness, palette)
    assert len(allocation.segments) == 4

    # no binds, so nothing seeds the allocation
    assert allocation.seeds == []

    assert allocation.registers[0] == b"v0"
    assert allocation.registers[1] == b"v1"
    assert allocation.registers[4] == b"v2"

    # neither call forces v0 to move, so this matches the raw solves above
    assert allocation.segments[0].colors == {}
    assert allocation.segments[0].spills == {}
    assert allocation.segments[1].colors == {
        0: palette.find_by_name(b"rdi"),
        1: palette.find_by_name(b"rsi"),
    }
    assert allocation.segments[1].spills == {}
    assert allocation.segments[2].colors == {
        0: palette.find_by_name(b"rdi"),
        4: palette.find_by_name(b"rsi"),
    }
    assert allocation.segments[2].spills == {}
    assert allocation.segments[3].colors == {}
    assert allocation.segments[3].spills == {}


def can_handle_graphs_from_fnlet_with_multiline_clobbers():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body1 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v0"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v1"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"rsi", b"rdi"],
                args={
                    b"rdi": llvm.Register(name=b"v0"),
                    b"rsi": llvm.Register(name=b"v1"),
                },
            ),
        ]
    )

    body2 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v2"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"rdi", b"rsi"],
                args={
                    b"rdi": llvm.Register(name=b"v1"),
                    b"rsi": llvm.Register(name=b"v2"),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare fnlet and liveness
    fnlet = FnletMock(blocks=[entry, body1, body2, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    graph0, hints0 = into_graph(
        palette, liveness.registers, liveness.segments[0], Seeds.empty()
    )
    graph1, hints1 = into_graph(
        palette, liveness.registers, liveness.segments[1], Seeds.empty()
    )
    graph2, hints2 = into_graph(
        palette, liveness.registers, liveness.segments[2], Seeds.empty()
    )
    graph3, hints3 = into_graph(
        palette, liveness.registers, liveness.segments[3], Seeds.empty()
    )

    assert graph0.size() == 0
    assert graph1.size() == 4
    assert graph2.size() == 4
    assert graph3.size() == 0

    assert hints0.colors == {}

    assert hints0.spills == {}
    assert hints1.colors == {}
    assert hints1.spills == {}
    assert hints2.colors == {}
    assert hints2.spills == {}
    assert hints3.colors == {}
    assert hints3.spills == {}

    colors0, spills0, clobbers0 = solve(graph0, palette)
    colors1, spills1, clobbers1 = solve(graph1, palette)
    colors2, spills2, clobbers2 = solve(graph2, palette)
    colors3, spills3, clobbers3 = solve(graph3, palette)

    # no instructions before the MOVs, so nothing is live yet
    assert colors0 == {}
    assert spills0 == {}
    assert clobbers0 == {}

    assert graph1.at(0) == VirtualRegister(name=b"v0")
    assert graph1.at(1) == VirtualRegister(name=b"v1")

    # this clobbers both rdi and rsi; v1 survives into body2 so it must
    # avoid both and lands on rdx, while v0 dies here and shares rdi's slot
    assert colors1 == {0: 0, 1: 2}
    assert spills1 == {}
    assert clobbers1 == {
        2: palette.find_by_name(b"rdi"),
        3: palette.find_by_name(b"rsi"),
    }

    assert graph2.at(0) == VirtualRegister(name=b"v1")
    assert graph2.at(1) == VirtualRegister(name=b"v2")

    # neither v1 nor v2 survives past this call, so neither avoids the
    # clobbers — they only need to differ from each other
    assert colors2 == {0: 0, 1: 1}
    assert spills2 == {}
    assert clobbers2 == {
        2: palette.find_by_name(b"rdi"),
        3: palette.find_by_name(b"rsi"),
    }

    assert colors3 == {}
    assert spills3 == {}
    assert clobbers3 == {}

    # allocate registers
    allocation = allocate(liveness, palette)
    assert len(allocation.segments) == 4

    # no binds, so nothing seeds the allocation
    assert allocation.seeds == []

    assert allocation.registers[0] == b"v0"
    assert allocation.registers[1] == b"v1"
    assert allocation.registers[4] == b"v2"

    # v1's rdx hint carries forward and is still free here, so it keeps it;
    # v2 only interferes with v1, so it lands on rdi
    assert allocation.segments[0].colors == {}
    assert allocation.segments[0].spills == {}
    assert allocation.segments[1].colors == {
        0: palette.find_by_name(b"rdi"),
        1: palette.find_by_name(b"rdx"),
    }
    assert allocation.segments[1].spills == {}
    assert allocation.segments[2].colors == {
        1: palette.find_by_name(b"rdx"),
        4: palette.find_by_name(b"rdi"),
    }
    assert allocation.segments[2].spills == {}
    assert allocation.segments[3].colors == {}
    assert allocation.segments[3].spills == {}


def can_handle_graphs_from_fnlet_with_a_hinted_survivor_colliding_with_a_clobber():
    # v0 must be hinted at rdi
    # v1 must be hinted at rsi
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(
                operands=(),
                binds={
                    b"v0": llvm.Register(name=b"rdi"),
                    b"v1": llvm.Register(name=b"rsi"),
                },
                preserves=[],
            ),
        ]
    )

    # rdi -> v0 -> rdi, but clobbered during the call and needed later
    # rsi -> v1 -> rsi, can die we don't need it later
    body1 = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[b"rdi"],
                args={
                    b"rdi": llvm.Register(name=b"v0"),
                    b"rsi": llvm.Register(name=b"v1"),
                },
            ),
        ]
    )

    # v0 will not come in rdi, nor rsi
    # v2 will be loaded into some register
    body2 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v2"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[],
                args={
                    b"rdi": llvm.Register(name=b"v0"),
                    b"rsi": llvm.Register(name=b"v2"),
                },
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare fnlet and liveness
    fnlet = FnletMock(blocks=[entry, body1, body2, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    assert liveness.registers == [b"rdi", b"v0", b"rsi", b"v1", b"v2"]
    assert liveness.seeds == [(0, 1), (2, 3)]

    graph0, hints0 = into_graph(
        palette,
        liveness.registers,
        liveness.segments[0],
        Seeds(
            colors=[
                (1, palette.find_by_name(b"rdi")),
                (3, palette.find_by_name(b"rsi")),
            ],
            spills=[],
        ),
    )

    graph1, hints1 = into_graph(
        palette,
        liveness.registers,
        liveness.segments[1],
        Seeds(
            colors=[
                (1, palette.find_by_name(b"rdi")),
                (3, palette.find_by_name(b"rsi")),
            ],
            spills=[],
        ),
    )

    graph2, hints2 = into_graph(
        palette, liveness.registers, liveness.segments[2], Seeds.empty()
    )
    graph3, hints3 = into_graph(
        palette, liveness.registers, liveness.segments[3], Seeds.empty()
    )

    assert graph0.size() == 2
    assert graph1.size() == 3
    assert graph2.size() == 2
    assert graph3.size() == 0

    assert graph0.at(0) == VirtualRegister(name=b"v0")
    assert graph0.at(1) == VirtualRegister(name=b"v1")

    # v0 is hinted at rdi, v1 is hinted at rsi
    assert hints0.colors == {
        0: palette.find_by_name(b"rdi"),
        1: palette.find_by_name(b"rsi"),
    }
    assert hints0.spills == {}

    assert graph1.at(1) == VirtualRegister(name=b"v0")
    assert graph1.at(2) == VirtualRegister(name=b"v1")

    # v0 is still at rdi, v1 is still at rsi
    assert hints1.colors == {
        1: palette.find_by_name(b"rdi"),
        2: palette.find_by_name(b"rsi"),
    }
    assert hints1.spills == {}

    assert hints2.colors == {}

    assert hints2.spills == {}
    assert hints3.colors == {}
    assert hints3.spills == {}

    colors0, spills0, clobbers0 = solve(graph0, palette)
    colors1, spills1, clobbers1 = solve(graph1, palette)
    colors2, spills2, clobbers2 = solve(graph2, palette)
    colors3, spills3, clobbers3 = solve(graph3, palette)

    assert graph0.at(0) == VirtualRegister(name=b"v0")
    assert graph0.at(1) == VirtualRegister(name=b"v1")

    # v0 <> v1 because they interfere with each other
    # no clobbers so the colors are straightforward
    assert colors0 == {0: 0, 1: 1}
    assert spills0 == {}
    assert clobbers0 == {}

    assert graph1.at(0) == PhysicalRegister(name=b"rdi")
    assert graph1.at(1) == VirtualRegister(name=b"v0")
    assert graph1.at(2) == VirtualRegister(name=b"v1")

    # v0 survives in not clobbered
    # v1 doesn't care about survival
    assert colors1 == {1: 1, 2: 0}
    assert spills1 == {}
    assert clobbers1 == {0: palette.find_by_name(b"rdi")}

    assert graph2.at(0) == VirtualRegister(name=b"v0")
    assert graph2.at(1) == VirtualRegister(name=b"v2")

    # v0 got rdi, v2 got rsi
    # both don't need to survive
    assert colors2 == {0: 0, 1: 1}
    assert spills2 == {}
    assert clobbers2 == {}

    assert colors3 == {}
    assert spills3 == {}
    assert clobbers3 == {}

    # allocate registers
    allocation = allocate(liveness, palette)
    assert len(allocation.segments) == 4

    # same seeds as liveness: v0 from rdi, v1 from rsi
    assert allocation.seeds == [(0, 1), (2, 3)]

    assert allocation.registers[1] == b"v0"
    assert allocation.registers[3] == b"v1"
    assert allocation.registers[4] == b"v2"

    # v0 -> rdi, v1 -> rsi as hinted
    assert allocation.segments[0].colors == {
        1: palette.find_by_name(b"rdi"),
        3: palette.find_by_name(b"rsi"),
    }

    assert allocation.segments[0].spills == {}

    # v0 -> rdx, must be moved because it needs to survive, but rdi is clobbered
    # v1 -> rsi, v1 can be in the rsi, it doesn't survive
    assert allocation.segments[1].colors == {
        1: palette.find_by_name(b"rdx"),
        3: palette.find_by_name(b"rsi"),
    }

    assert allocation.segments[1].spills == {}

    # v0 -> rdx, can be left there
    # v2 -> rdi, can be loaded here
    assert allocation.segments[2].colors == {
        1: palette.find_by_name(b"rdx"),
        4: palette.find_by_name(b"rdi"),
    }

    assert allocation.segments[2].spills == {}

    assert allocation.segments[3].colors == {}
    assert allocation.segments[3].spills == {}


def can_handle_graphs_from_fnlet_when_a_survivor_outlives_a_full_register_clobber():
    entry = FnletBlockMock(
        instructions=[
            llvm.PROLOG(operands=(), binds={}, preserves=[]),
        ]
    )

    body1 = FnletBlockMock(
        instructions=[
            llvm.MOV(
                operands=(
                    llvm.Register(name=b"v0"),
                    llvm.Immediate.derive(bytes([0x00, 0x00, 0x00, 0x00])),
                )
            ),
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[
                    b"rdi",
                    b"rsi",
                    b"rdx",
                    b"rcx",
                    b"r8",
                    b"r9",
                    b"r10",
                    b"r11",
                    b"rax",
                    b"rbx",
                    b"rbp",
                    b"r12",
                    b"r13",
                    b"r14",
                    b"r15",
                ],
                args={},
            ),
        ]
    )

    body2 = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                clobbers=[],
                args={b"rdi": llvm.Register(name=b"v0")},
            ),
        ]
    )

    exit = FnletBlockMock(
        instructions=[
            llvm.EPILOG(operands=(), preserves=[]),
        ]
    )

    # prepare fnlet and liveness
    fnlet = FnletMock(blocks=[entry, body1, body2, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    graph0, hints0 = into_graph(
        palette, liveness.registers, liveness.segments[0], Seeds.empty()
    )
    graph1, hints1 = into_graph(
        palette, liveness.registers, liveness.segments[1], Seeds.empty()
    )
    graph2, hints2 = into_graph(
        palette, liveness.registers, liveness.segments[2], Seeds.empty()
    )
    graph3, hints3 = into_graph(
        palette, liveness.registers, liveness.segments[3], Seeds.empty()
    )

    assert graph0.size() == 0
    assert graph1.size() == 16
    assert graph2.size() == 1
    assert graph3.size() == 0

    assert hints0.colors == {}

    assert hints0.spills == {}
    assert hints1.colors == {}
    assert hints1.spills == {}
    assert hints2.colors == {}
    assert hints2.spills == {}
    assert hints3.colors == {}
    assert hints3.spills == {}

    colors0, spills0, clobbers0 = solve(graph0, palette)
    colors1, spills1, clobbers1 = solve(graph1, palette)
    colors2, spills2, clobbers2 = solve(graph2, palette)
    colors3, spills3, clobbers3 = solve(graph3, palette)

    assert colors0 == {}
    assert spills0 == {}
    assert clobbers0 == {}

    assert graph1.at(0) == VirtualRegister(name=b"v0")

    assert colors1 == {}

    # r11 isn't in the palette, so only 14 real registers compete for low
    # slots; v0's spill lands on 14, one less than when r11 was allocatable
    assert spills1 == {0: 14}

    # every real register is clobbered here, so v0 needs a spill slot;
    # r11 precolors to -1 since it isn't part of the allocatable palette
    assert clobbers1 == {
        1: palette.find_by_name(b"rdi"),
        2: palette.find_by_name(b"rsi"),
        3: palette.find_by_name(b"rdx"),
        4: palette.find_by_name(b"rcx"),
        5: palette.find_by_name(b"r8"),
        6: palette.find_by_name(b"r9"),
        7: palette.find_by_name(b"r10"),
        8: -1,
        9: palette.find_by_name(b"rax"),
        10: palette.find_by_name(b"rbx"),
        11: palette.find_by_name(b"rbp"),
        12: palette.find_by_name(b"r12"),
        13: palette.find_by_name(b"r13"),
        14: palette.find_by_name(b"r14"),
        15: palette.find_by_name(b"r15"),
    }

    assert graph2.at(0) == VirtualRegister(name=b"v0")

    # spill slots aren't carried forward as hints, and nothing clobbers
    # here, so v0 just takes the cheapest free color
    assert colors2 == {0: palette.find_by_name(b"rdi")}
    assert spills2 == {}
    assert clobbers2 == {}

    assert colors3 == {}
    assert spills3 == {}
    assert clobbers3 == {}

    # allocate registers
    allocation = allocate(liveness, palette)
    assert len(allocation.segments) == 4

    # no binds, so nothing seeds the allocation
    assert allocation.seeds == []

    assert allocation.registers[0] == b"v0"

    assert allocation.segments[0].colors == {}
    assert allocation.segments[0].spills == {}

    # matches the raw solve above: v0 has no real register left, so it spills
    assert allocation.segments[1].colors == {}
    assert allocation.segments[1].spills == {0: 14}

    # a fresh allocation with no hint and no interference: cheapest register
    assert allocation.segments[2].colors == {0: palette.find_by_name(b"rdi")}
    assert allocation.segments[2].spills == {}

    assert allocation.segments[3].colors == {}
    assert allocation.segments[3].spills == {}


def can_allocate_collect_no_clobbers_when_no_call_exists():
    entry = FnletBlockMock(
        instructions=[llvm.PROLOG(operands=(), binds={}, preserves=[])]
    )
    exit = FnletBlockMock(instructions=[llvm.EPILOG(operands=(), preserves=[])])

    fnlet = FnletMock(blocks=[entry, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    allocation = allocate(liveness, palette)

    assert allocation.clobbers == []


def can_allocate_collect_clobbers_from_a_single_call():
    entry = FnletBlockMock(
        instructions=[llvm.PROLOG(operands=(), binds={}, preserves=[])]
    )
    body = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                args={},
                clobbers=[b"rax", b"rcx"],
            ),
        ]
    )
    exit = FnletBlockMock(instructions=[llvm.EPILOG(operands=(), preserves=[])])

    fnlet = FnletMock(blocks=[entry, body, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    allocation = allocate(liveness, palette)

    assert allocation.clobbers == [b"rax", b"rcx"]


def can_allocate_collect_the_union_of_clobbers_across_multiple_calls():
    entry = FnletBlockMock(
        instructions=[llvm.PROLOG(operands=(), binds={}, preserves=[])]
    )
    body = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                args={},
                clobbers=[b"rax", b"rbx"],
            ),
            llvm.CALL(
                operands=(FunctionId(value=12),),
                args={},
                clobbers=[b"rbx", b"rcx"],
            ),
        ]
    )
    exit = FnletBlockMock(instructions=[llvm.EPILOG(operands=(), preserves=[])])

    fnlet = FnletMock(blocks=[entry, body, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    allocation = allocate(liveness, palette)

    # rbx is clobbered by both calls but must not be duplicated
    assert allocation.clobbers == [b"rax", b"rbx", b"rcx"]


def can_allocate_collect_a_clobber_outside_the_palette():
    entry = FnletBlockMock(
        instructions=[llvm.PROLOG(operands=(), binds={}, preserves=[])]
    )
    body = FnletBlockMock(
        instructions=[
            llvm.CALL(
                operands=(FunctionId(value=11),),
                args={},
                clobbers=[b"r11"],
            ),
        ]
    )
    exit = FnletBlockMock(instructions=[llvm.EPILOG(operands=(), preserves=[])])

    fnlet = FnletMock(blocks=[entry, body, exit])
    liveness = prepare_liveness(fnlet)
    palette = create_systemv_palette()

    allocation = allocate(liveness, palette)

    # r11 is the scratch register, never in the palette, but it's still a
    # real clobber that must be recorded
    assert allocation.clobbers == [b"r11"]
