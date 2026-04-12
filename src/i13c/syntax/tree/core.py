from contextlib import contextmanager
from typing import Any, Iterator, List


class Path:
    def __init__(self) -> None:
        self._count: int = 0
        self._nodes: List[Any] = []

    @contextmanager
    def push(self, node: Any) -> Iterator["Path"]:

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
