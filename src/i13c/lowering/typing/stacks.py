from dataclasses import dataclass


@dataclass(kw_only=True)
class StackFrame:
    size: int

    def describe(self) -> str:
        return f"size={self.size}"
