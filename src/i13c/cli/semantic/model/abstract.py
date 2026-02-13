from typing import Dict, Iterable, Protocol, TypeVar

from i13c.semantic.model import SemanticGraph

ListItem = TypeVar("ListItem")


class AbstractListExtractor(Protocol[ListItem]):
    @staticmethod
    def headers() -> Dict[str, str]: ...

    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[ListItem]: ...

    @staticmethod
    def rows(entry: ListItem) -> Dict[str, str]: ...
