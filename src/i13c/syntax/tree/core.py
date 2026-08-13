from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, TypeVar

PathNode = TypeVar("PathNode")


class Path:
    def __init__(self) -> None:
        self._count: int = 0
        self._nodes: list[Any] = []

    @contextmanager
    def push(self, node: Any) -> Generator[Path]:

        if len(self._nodes) == self._count:
            self._count += 1
            self._nodes.append(node)
        else:
            self._nodes[self._count] = node
            self._count += 1

        try:
            yield self
        finally:
            self._count -= 1

    def contains(self, type: type[PathNode]) -> bool:
        for i in range(self._count - 1, -1, -1):
            node = self._nodes[i]
            if isinstance(node, type):
                return True

        return False

    def find(self, type: type[PathNode]) -> PathNode:
        for i in range(self._count - 1, -1, -1):
            node = self._nodes[i]
            if isinstance(node, type):
                return node

        raise ValueError(f"Node of type {type} not found in path")

    def is_empty(self) -> bool:
        return self._count == 0
