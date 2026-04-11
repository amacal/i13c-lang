from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.values import Value, ValueId


class ValueListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[ValueId, Value]]:
        return artifacts.semantic_graph().entities.values.items()

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Value ID",
            "name": "Value Name",
            "kind": "Expression Kind",
            "target": "Expression Target",
        }

    @staticmethod
    def rows(entry: Tuple[ValueId, Value]) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].ident),
            "kind": entry[1].expr.kind.decode(),
            "target": entry[1].expr.target.identify(1),
        }
