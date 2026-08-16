from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.allocations import Allocation
from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.analyses.dflows import DataFlows
from i13c.semantic.typing.analyses.spills import Spill, SpillOp, SpillReg, SpillScratch
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.values import ValueAcceptance


def configure_spills() -> GraphNode:
    return GraphNode(
        builder=build_spills,
        constraint=None,
        produces=("analyses/spills",),
        requires=frozenset(
            {
                ("allocations", "analyses/allocations"),
                ("cflows", "analyses/cflows"),
                ("dflows", "analyses/dflows"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_spills(
    allocations: OneToOne[FunctionId, Allocation],
    cflows: OneToOne[FunctionId, ControlFlows],
    dflows: OneToOne[FunctionId, DataFlows],
) -> OneToOne[FunctionId, Spill]:
    spills: dict[FunctionId, Spill] = {}

    # fmt: off
    system_v: dict[int, bytes] = {
        0: b"rdi", 1: b"rsi", 2: b"rdx", 3: b"rcx", 4: b"r8", 5: b"r9", 6: b"r10", 7: b"r11",
        8: b"rax", 9: b"rbx", 10: b"rbp", 11: b"r12", 12: b"r13", 13: b"r14", 14: b"r15",
    }
    # fmt: on

    for fid, allocation in allocations.items():
        entries: dict[int, list[SpillOp]] = {}
        cflow = cflows.get(fid)
        dflow = dflows.get(fid)

        worklist: list[int] = [cflow.entry]
        visited: set[int] = set()

        while worklist:
            idx = worklist.pop()
            visited.add(idx)

            # prepare node
            entries[idx] = []

            # schedule successors
            for successor in cflow.forward.get(idx, []):
                if successor not in visited:
                    worklist.append(successor)

            for value in dflow.defs[idx]:
                if value in allocation.spills:  # noqa: SIM102
                    if isinstance(dflow.values[value], ValueAcceptance):
                        assert value in dflow.backward
                        assert len(dflow.backward[value]) <= 1

                        if dflow.backward[value]:
                            source = dflow.backward[value][0]
                            if source in allocation.colors:
                                entries[idx].append(
                                    SpillReg(
                                        slot=allocation.spills[value],
                                        src=system_v[allocation.colors[source]],
                                    )
                                )

                            else:
                                entries[idx].append(
                                    SpillScratch(
                                        slot=allocation.spills[value],
                                        src=system_v[allocation.scratch],
                                    )
                                )


        spills[fid] = Spill(
            ref=allocation.ref,
            target=fid,
            entry=cflow.entry,
            exit=cflow.exit,
            nodes=cflow.nodes,
            values=allocation.values,
            forward=cflow.forward,
            backward=cflow.backward,
            spills=entries,
        )

    return OneToOne[FunctionId, Spill].instance(spills)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Spill]) -> None:
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, Spill]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "function": "Function",
            "spills": "Spills",
        }

    @staticmethod
    def rows(key: FunctionId, entry: Spill) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "function": key.identify(1),
            "spills": str(len(entry.spills)),
        }
