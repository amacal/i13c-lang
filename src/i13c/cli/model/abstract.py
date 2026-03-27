from typing import Dict, Iterable, Protocol, TypeVar

from i13c.graph.artifacts import GraphArtifacts

ListItem = TypeVar("ListItem")


class AbstractListExtractor(Protocol[ListItem]):
    @staticmethod
    def headers() -> Dict[str, str]: ...

    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[ListItem]: ...

    @staticmethod
    def rows(entry: ListItem) -> Dict[str, str]: ...
