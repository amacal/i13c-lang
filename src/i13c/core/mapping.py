from collections.abc import Iterable, Iterator
from dataclasses import dataclass


@dataclass(kw_only=True)
class OneToOne[SemanticId, SemanticNode]:
    data: dict[SemanticId, SemanticNode]

    @staticmethod
    def instance(
        data: dict[SemanticId, SemanticNode],
    ) -> OneToOne[SemanticId, SemanticNode]:
        return OneToOne(data=data)

    def size(self) -> int:
        return len(self.data)

    def contains(self, key: SemanticId) -> bool:
        return key in self.data

    def __iter__(self) -> Iterator[SemanticId]:
        return iter(self.data)

    def pop(self) -> tuple[SemanticId, SemanticNode]:
        return self.data.popitem()

    def peek(self) -> tuple[SemanticId, SemanticNode]:
        return next(iter(self.data.items()))

    def get(self, key: SemanticId) -> SemanticNode:
        return self.data[key]

    def find(self, key: SemanticId) -> SemanticNode | None:
        return self.data.get(key)

    def keys(self) -> Iterable[SemanticId]:
        return self.data.keys()

    def values(self) -> Iterable[SemanticNode]:
        return self.data.values()

    def items(self) -> Iterable[tuple[SemanticId, SemanticNode]]:
        return self.data.items()


@dataclass(kw_only=True)
class OneToMany[SemanticId, SemanticNode]:
    data: dict[SemanticId, list[SemanticNode]]

    @staticmethod
    def instance(
        data: dict[SemanticId, list[SemanticNode]],
    ) -> OneToMany[SemanticId, SemanticNode]:
        return OneToMany(data=data)

    def size(self) -> int:
        return len(self.data)

    def keys(self) -> Iterable[SemanticId]:
        return self.data.keys()

    def pop(self) -> tuple[SemanticId, list[SemanticNode]]:
        return self.data.popitem()

    def peek(self) -> tuple[SemanticId, list[SemanticNode]]:
        return next(iter(self.data.items()))

    def get(self, key: SemanticId) -> list[SemanticNode]:
        return self.data[key]

    def find(self, key: SemanticId) -> list[SemanticNode]:
        return self.data.get(key, [])

    def values(self) -> Iterable[list[SemanticNode]]:
        return self.data.values()

    def items(self) -> Iterable[tuple[SemanticId, list[SemanticNode]]]:
        return self.data.items()
