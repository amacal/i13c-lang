from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.allocations import Allocation, AllocationValue
from i13c.semantic.typing.analyses.callings import Calling, CallingArgument
from i13c.semantic.typing.analyses.shuffles import (
    Shuffle,
    ShuffleCallSite,
    ShuffleExchange,
    ShuffleImmediate,
    ShuffleLoad,
    ShuffleMove,
    ShuffleMoves,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance


def configure_shuffles() -> GraphNode:
    return GraphNode(
        builder=build_shuffles,
        constraint=None,
        produces=("analyses/shuffles",),
        requires=frozenset(
            {
                ("allocations", "analyses/allocations"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_shuffles(
    allocations: OneToOne[FunctionId, Allocation],
) -> OneToOne[FunctionId, Shuffle]:
    shuffles: dict[FunctionId, Shuffle] = {}

    # fmt: off
    system_v: dict[int, bytes] = {
        0: b"rdi", 1: b"rsi", 2: b"rdx", 3: b"rcx", 4: b"r8", 5: b"r9", 6: b"r10", 7: b"r11",
        8: b"rax", 9: b"rbx", 10: b"rbp", 11: b"r12", 12: b"r13", 13: b"r14", 14: b"r15",
    }
    # fmt: on

    for fid, allocation in allocations.items():
        callsites: list[ShuffleCallSite] = []

        for calling in allocation.values:
            if isinstance(calling, Calling):
                colors = {
                    idx: system_v[color] for idx, color in allocation.colors.items()
                }

                arguments = {
                    bind.name: arg
                    for arg, bind in zip(calling.arguments, calling.bindings)
                }

                moves = build_moves(
                    build_mapping(
                        allocation.values, colors, allocation.spills, arguments
                    )
                )

                callsites.append(
                    ShuffleCallSite(
                        calling=calling,
                        target=calling.target,
                        moves=moves,
                    )
                )

        shuffles[fid] = Shuffle(
            ref=allocation.ref,
            target=allocation.target,
            callsites=callsites,
        )

    return OneToOne[FunctionId, Shuffle].instance(shuffles)


ShuffleMapping = list[tuple[bytes | Hex | int, bytes]]


def build_mapping(
    values: list[AllocationValue],
    colors: dict[int, bytes],
    spills: dict[int, int],
    arguments: dict[bytes, CallingArgument],
) -> ShuffleMapping:
    # mapping of src register to dst register
    mapping: ShuffleMapping = []

    # build mapping from allocation values to calling arguments
    for dst, argument in arguments.items():
        if isinstance(argument, LiteralAcceptance):
            mapping.append((argument.target, dst))

        if isinstance(argument, (ParameterAcceptance, ValueAcceptance)):
            idx = values.index(argument)

            # param/value may be colored
            if idx in colors:
                mapping.append((colors[idx], dst))

            # or spilled to memory
            else:
                mapping.append((spills[idx], dst))

    return mapping


def build_moves(mapping: ShuffleMapping) -> list[ShuffleMoves]:
    moves: list[ShuffleMoves] = []

    while mapping:
        changed = False

        for src, dst in list(mapping):
            # literal values can be moved directly to the destination
            if isinstance(src, Hex):
                moves.append(ShuffleImmediate(src=src, dst=dst))
                mapping.remove((src, dst))
                changed = True

            # spilled values can be loaded directly to the destination
            elif isinstance(src, int):
                moves.append(ShuffleLoad(src=src, dst=dst))
                mapping.remove((src, dst))
                changed = True

            # nothing to move if the source and destination are the same
            elif src == dst:
                mapping.remove((src, dst))
                changed = True

            # if the destination is not a source, we can move it directly
            elif not any(dst == src for src, _ in mapping):
                moves.append(ShuffleMove(src=src, dst=dst))
                mapping.remove((src, dst))
                changed = True

        # if we can't find a direct move, we need to exchange
        if not changed:
            break

    while mapping:
        src, dst = mapping.pop(0)
        assert isinstance(src, bytes)

        # xchg may caused a no-op
        if src == dst:
            continue

        moves.append(ShuffleExchange(src=src, dst=dst))

        # update the mapping to reflect the exchange
        for idx, (a, b) in enumerate(list(mapping)):
            if a == dst:
                mapping[idx] = (src, b)

    return moves


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Shuffle]):
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, ShuffleCallSite]]:
        for fid, shuffle in self.data.items():
            for callsite in shuffle.callsites:
                yield fid, callsite

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "function": "Function",
            "callsite": "Callsite",
            "moves": "Moves",
        }

    @staticmethod
    def rows(key: FunctionId, entry: ShuffleCallSite) -> dict[str, str]:
        return {
            "ref": str(entry.calling.ref),
            "function": key.identify(1),
            "callsite": entry.target.id.identify(1),
            "moves": str(len(entry.moves)),
        }
