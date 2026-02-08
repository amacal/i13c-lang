from dataclasses import dataclass

from i13c.semantic.typing.entities.callables import CallableKind, CallableTarget

EntryPointName: bytes = b"main"


@dataclass
class EntryPoint:
    kind: CallableKind
    target: CallableTarget

    def describe(self) -> str:
        return f"kind={self.kind.decode()}"
