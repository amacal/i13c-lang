from typing import Dict, Iterable, List, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.indices.usages import UsageId


class UsagesByExpressionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[ExpressionId, Expression, List[UsageId]]]:
        graph = artifacts.semantic_graph()
        index = graph.indices.usages_by_expression

        return (
            (eid, graph.entities.expressions.get(eid), uids) for eid, uids in index.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "eid": "Expression ID",
            "name": "Expression Name",
            "uids": "Usage IDs",
        }

    @staticmethod
    def rows(entry: Tuple[ExpressionId, Expression, List[UsageId]]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "eid": entry[0].identify(1),
            "name": str(entry[1].ident),
            "uids": " ".join(uid.identify(1) for uid in entry[2]),
        }
