from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.dflows import DataFlows
from i13c.semantic.typing.analyses.liveness import Liveness
from i13c.semantic.typing.entities.functions import FunctionId


def configure_liveness() -> GraphNode:
    return GraphNode(
        builder=build_liveness,
        constraint=None,
        produces=("analyses/liveness",),
        requires=frozenset(
            {
                ("dflows", "analyses/dflows"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_liveness(
    dflows: OneToOne[FunctionId, DataFlows],
) -> OneToOne[FunctionId, Liveness]:
    liveness: dict[FunctionId, Liveness] = {}

    for dflow in dflows.values():
        worklist = list(range(len(dflow.control.nodes)))
        clobbers: dict[int, set[int]] = {node: set() for node in worklist}
        live_in: dict[int, set[int]] = {node: set() for node in worklist}
        live_out: dict[int, set[int]] = {node: set() for node in worklist}

        # iterate until no changes occur
        while worklist:
            node = worklist.pop()

            # compute live_out as union of live_in of successors
            for successor in dflow.control.forward.get(node, []):
                live_out[node].update(live_in[successor])

            # compute live_in as union of uses and live_out minus defs
            defined = live_out[node] - set(dflow.defs[node])
            new_live_in = set(dflow.uses[node]).union(defined)

            # if live_in[node] has changed
            if new_live_in != live_in[node]:
                live_in[node] = new_live_in
                worklist.extend(dflow.control.backward.get(node, []))

        for node, items in dflow.clobbers.items():
            clobbers[node].update(items)

        liveness[dflow.target] = Liveness(
            ref=dflow.ref,
            target=dflow.target,
            entry=dflow.entry,
            exit=dflow.exit,
            nodes=dflow.control.nodes,
            values=dflow.values,
            live_in=live_in,
            live_out=live_out,
            clobbers=clobbers,
        )

    return OneToOne[FunctionId, Liveness].instance(liveness)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Liveness]) -> None:
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, Liveness]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "entry": "Entry",
            "exit": "Exit",
            "nodes": "Nodes",
            "values": "Values",
            "in": "Live In",
            "out": "Live Out",
        }

    @staticmethod
    def rows(key: FunctionId, entry: Liveness) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "entry": str(entry.entry),
            "exit": str(entry.exit),
            "nodes": str(len(entry.nodes)),
            "values": str(len(entry.values)),
            "in": str(len(entry.live_in)),
            "out": str(len(entry.live_out)),
        }
