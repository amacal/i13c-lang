from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.flags import Flags, FlagsId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax import tree


def configure_flags() -> GraphNode:
    return GraphNode(
        builder=build_flags,
        constraint=None,
        produces=("entities/flags",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_flags(
    graph: SyntaxGraph,
) -> OneToOne[FlagsId, Flags]:
    flags: Dict[FlagsId, Flags] = {}

    for nid, entry in graph.snippet.flags.items():
        # derive flags ID from globally unique node ID
        flags_id = FlagsId(value=nid.value)

        # reverse mapping to register ID
        def map_register(register: tree.snippet.Register) -> RegisterId:
            nid = graph.snippet.registers.get_by_node(register)
            return RegisterId(value=nid.value)

        flags[flags_id] = Flags(
            ref=entry.ref,
            noreturn=entry.noreturn,
            clobbers=(
                [map_register(register) for register in entry.clobbers]
                if entry.clobbers is not None
                else None
            ),
        )

    return OneToOne[FlagsId, Flags].instance(flags)
