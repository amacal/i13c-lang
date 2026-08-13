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

    return OneToOne[FunctionId, Liveness].instance(liveness)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, DataFlows]):
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, DataFlows]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "values": "values",
            "forward": "Forward",
            "backward": "Backward",
        }

    @staticmethod
    def rows(key: FunctionId, entry: DataFlows) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "values": str(len(entry.values)),
            "forward": str(len(entry.forward)),
            "backward": str(len(entry.backward)),
        }
