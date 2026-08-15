from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.allocations import Allocation, AllocationValue
from i13c.semantic.typing.analyses.callings import Calling, CallingArgument
from i13c.semantic.typing.analyses.shuffles import (
    Shuffle,
    ShuffleCallSite,
    ShuffleExchange,
    ShuffleMove,
    ShuffleMoveOrExchange,
)
from i13c.semantic.typing.entities.functions import FunctionId
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
                        values=allocation.values, colors=colors, arguments=arguments
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


def build_mapping(
    values: list[AllocationValue],
    colors: dict[int, bytes],
    arguments: dict[bytes, CallingArgument],
) -> list[tuple[bytes, bytes]]:
    # mapping of src register to dst register
    mapping: list[tuple[bytes, bytes]] = []

    # build mapping from allocation values to calling arguments
    for dst, argument in arguments.items():
        if isinstance(argument, (ParameterAcceptance, ValueAcceptance)):
            try:
                mapping.append((colors[values.index(argument)], dst))
            except KeyError:
                # TODO: spilling is not yet supported
                pass

    return mapping


def build_moves(mapping: list[tuple[bytes, bytes]]) -> list[ShuffleMoveOrExchange]:
    moves: list[ShuffleMoveOrExchange] = []

    while mapping:
        changed = False

        for src, dst in list(mapping):
            # nothing to move if the source and destination are the same
            if src == dst:
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
