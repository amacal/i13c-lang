from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.allocations import Allocation
from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.analyses.frames import (
    StackFrame,
    StackFrameMove,
    StackFrameSave,
    StackFrameSpill,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance


def configure_frames() -> GraphNode:
    return GraphNode(
        builder=build_frames,
        constraint=None,
        produces=("analyses/frames",),
        requires=frozenset(
            {
                ("allocations", "analyses/allocations"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_frames(
    allocations: OneToOne[FunctionId, Allocation],
) -> OneToOne[FunctionId, StackFrame]:
    frames: dict[FunctionId, StackFrame] = {}

    # fmt: off
    system_v: dict[int, bytes] = {
        0: b"rdi", 1: b"rsi", 2: b"rdx", 3: b"rcx", 4: b"r8", 5: b"r9", 6: b"r10", 7: b"r11",
        8: b"rax", 9: b"rbx", 10: b"rbp", 11: b"r12", 12: b"r13", 13: b"r14", 14: b"r15",
    }

    callee_saved: set[bytes] = {
        name for idx, name in system_v.items() if idx >= 9
    }
    # fmt: on

    for fid, allocation in allocations.items():
        moved: list[StackFrameMove] = []
        spill: list[StackFrameSpill] = []
        saved: list[StackFrameSave] = []

        # save callee-saved registers that are used in the function
        for idx in sorted(set(allocation.colors.values())):
            if idx >= 9:
                saved.append(
                    StackFrameSave(
                        name=system_v[idx],
                    )
                )

        def is_already_saved(saved: list[StackFrameSave], name: bytes) -> bool:
            return any(entry.name == name for entry in saved)

        # save clobbered registers that are used in the function
        for calling in allocation.values:
            if isinstance(calling, Calling):
                for clobber in calling.clobbers:
                    if not is_already_saved(saved, clobber.name):  # noqa: SIM102
                        if clobber.name in callee_saved:
                            saved.append(
                                StackFrameSave(
                                    name=clobber.name,
                                )
                            )

        # spill parameters are spilled to their new location
        for idx, slot in allocation.spills.items():
            target = allocation.values[idx]

            if isinstance(target, ParameterAcceptance):
                spill.append(
                    StackFrameSpill(
                        name=system_v[idx],
                        slot=slot,
                    )
                )

        # colored parameters are moved to their new location
        idx = 0
        for param in allocation.values:
            if isinstance(param, ParameterAcceptance):
                if idx in allocation.colors:
                    moved.append(
                        StackFrameMove(
                            src=system_v[idx],
                            dst=system_v[allocation.colors[idx]],
                        )
                    )

                idx += 1

        frames[fid] = StackFrame(
            ref=allocation.ref,
            slots=len(set(allocation.spills.values())),
            target=fid,
            moved=moved,
            spill=spill,
            saved=saved,
        )

    return OneToOne[FunctionId, StackFrame].instance(frames)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, StackFrame]) -> None:
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, StackFrame]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "moved": "Moved",
            "spill": "Spill",
        }

    @staticmethod
    def rows(key: FunctionId, entry: StackFrame) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "moved": ",".join([m.src.decode() for m in entry.moved]),
            "spill": ",".join([s.name.decode() for s in entry.spill]),
        }
