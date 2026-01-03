from dataclasses import dataclass


@dataclass(kw_only=True)
class Generator:
    id: int = 0

    def next(self) -> int:
        self.id += 1
        return self.id
