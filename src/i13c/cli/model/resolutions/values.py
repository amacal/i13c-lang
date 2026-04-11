from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.resolutions.values import (
    ValueResolution,
)


class ValueResolutionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[ValueId, Value, ValueResolution]]:
        graph = artifacts.semantic_graph()
        index = graph.indices.resolution_by_value
        values = graph.entities.values

        return ((vid, values.get(vid), resolution) for vid, resolution in index.items())

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Value ID",
            "name": "Value Name",
            "type": "Value Type",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(
        entry: Tuple[ValueId, Value, ValueResolution],
    ) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].ident),
            "type": str(entry[1].type),
            "accepted": (
                str(entry[2].accepted.binding.identify(1)) if entry[2].accepted else ""
            ),
            "rejected": (
                str(entry[2].rejected.reason.decode()) if entry[2].rejected else ""
            ),
        }
