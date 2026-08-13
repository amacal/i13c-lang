from collections.abc import Iterable
from typing import Protocol, TypeVar

ListKey = TypeVar("ListKey")
ListEntry = TypeVar("ListEntry")


class AbstractListExtractor(Protocol[ListKey, ListEntry]):
    def extract(self) -> Iterable[tuple[ListKey, ListEntry]]: ...

    @staticmethod
    def headers() -> dict[str, str]: ...

    @staticmethod
    def rows(key: ListKey, entry: ListEntry) -> dict[str, str]: ...
