from typing import Dict, Iterable, Protocol, Tuple, TypeVar

ListKey = TypeVar("ListKey")
ListEntry = TypeVar("ListEntry")


class AbstractListExtractor(Protocol[ListKey, ListEntry]):
    def extract(self) -> Iterable[Tuple[ListKey, ListEntry]]: ...

    @staticmethod
    def headers() -> Dict[str, str]: ...

    @staticmethod
    def rows(key: ListKey, entry: ListEntry) -> Dict[str, str]: ...
