from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
)

CallgraphBuilder = Callable[..., Any]


@dataclass(kw_only=True, frozen=True)
class Configuration:
    builder: CallgraphBuilder
    produces: Tuple[str, ...]
    requires: FrozenSet[Tuple[str, str]]


class Identified(Protocol):
    @property
    def value(self) -> int: ...

    def identify(self, length: int) -> str: ...


class Descriptive(Protocol):
    def describe(self) -> str: ...


SemanticId = TypeVar("SemanticId", bound=Identified)
SemanticNode = TypeVar("SemanticNode", bound=Descriptive)


@dataclass(kw_only=True)
class OneToOne(Generic[SemanticId, SemanticNode]):
    data: Dict[SemanticId, SemanticNode]

    @staticmethod
    def instance(
        data: Dict[SemanticId, SemanticNode],
    ) -> OneToOne[SemanticId, SemanticNode]:
        return OneToOne(data=data)

    def size(self) -> int:
        return len(self.data)

    def pop(self) -> Tuple[SemanticId, SemanticNode]:
        return self.data.popitem()

    def peak(self) -> Tuple[SemanticId, SemanticNode]:
        return next(iter(self.data.items()))

    def get(self, key: SemanticId) -> SemanticNode:
        return self.data[key]

    def find(self, key: SemanticId) -> Optional[SemanticNode]:
        return self.data.get(key)

    def keys(self) -> Iterable[SemanticId]:
        return self.data.keys()

    def values(self) -> Iterable[SemanticNode]:
        return self.data.values()

    def items(self) -> Iterable[Tuple[SemanticId, SemanticNode]]:
        return self.data.items()


@dataclass(kw_only=True)
class OneToMany[SemanticId, SemanticNode]:
    data: Dict[SemanticId, List[SemanticNode]]

    @staticmethod
    def instance(
        data: Dict[SemanticId, List[SemanticNode]],
    ) -> OneToMany[SemanticId, SemanticNode]:
        return OneToMany(data=data)

    def size(self) -> int:
        return len(self.data)

    def pop(self) -> Tuple[SemanticId, List[SemanticNode]]:
        return self.data.popitem()

    def get(self, key: SemanticId) -> List[SemanticNode]:
        return self.data[key]

    def find(self, key: SemanticId) -> List[SemanticNode]:
        return self.data.get(key, [])

    def values(self) -> Iterable[List[SemanticNode]]:
        return self.data.values()

    def items(self) -> Iterable[Tuple[SemanticId, List[SemanticNode]]]:
        return self.data.items()
